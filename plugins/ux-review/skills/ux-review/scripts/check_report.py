#!/usr/bin/env python3
"""Render-check a ux-review report in a headless browser.

Usage:
    python check_report.py report.html [--out ./report-check] [--browser /path/to/chrome]

Opens the page as desktop (1280px), tablet (820px, touch) and phone (390px, touch),
runs the checks from SKILL.md step 6, saves screenshots and prints a summary.
Exit code 0 = all checks passed, 1 = something failed, 2 = could not run.

Needs: pip install playwright && playwright install chromium
(or pass --browser with the path to an installed Chrome/Chromium).
"""
import argparse
import asyncio
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

VIEWS = [
    ("desktop", dict(viewport={"width": 1280, "height": 900})),
    ("tablet", dict(viewport={"width": 820, "height": 1100}, is_mobile=True, has_touch=True)),
    ("phone", dict(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True, device_scale_factor=2)),
]

# Returns a dict of simple facts about the rendered page.
PROBE = """() => {
  const q = s => document.querySelector(s);
  const svgKids = s => { const e = q(s + ' svg'); return e ? e.childElementCount : 0; };
  const cells = [...document.querySelectorAll('.stack td')];
  return {
    scrollWidth: document.documentElement.scrollWidth,
    width: innerWidth,
    radar: svgKids('#radar'),
    matrix: svgKids('#mx'),
    funnelRows: document.querySelectorAll('#friction .trow').length,
    segs: document.querySelectorAll('#friction .sg').length,
    walkTables: document.querySelectorAll('#walkList table').length,
    heurRows: document.querySelectorAll('#heurList .hr').length,
    testCards: document.querySelectorAll('#tpTasks .tpc').length,
    kpis: [...document.querySelectorAll('#kpis .num')].filter(n => n.textContent.trim()).length,
    rows: document.querySelectorAll('#tbody tr').length,
    badCells: cells.filter(td => !(td.children.length === 1 && td.firstElementChild.classList.contains('cv'))).length,
    tableTerms: document.querySelectorAll('#tbody .t').length,
    terms: document.querySelectorAll('.t').length,
    overflows: [...document.querySelectorAll('.trow .lab, .trow .lab small, .kpi small, .kpi .num, .card h3, .tpc h3, .hr span, .task h3')].filter(e => e.offsetParent && e.scrollWidth > e.clientWidth + 2).length,
    overlaps: [...document.querySelectorAll('#friction .trow, .kpi, .task h3')].reduce((n, box) => {
      const kids = [...box.querySelectorAll('span, small, b, .sg, .out')].filter(e => e.offsetParent && e.textContent.trim());
      for (let i = 0; i < kids.length; i++) for (let j = i + 1; j < kids.length; j++) {
        if (kids[i].contains(kids[j]) || kids[j].contains(kids[i])) continue;
        const a = kids[i].getBoundingClientRect(), b = kids[j].getBoundingClientRect();
        if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) n++;
      }
      return n;
    }, 0),
  };
}"""

TIP_VISIBLE = "() => getComputedStyle(document.getElementById('tip') || document.body).display !== 'none' && !!document.getElementById('tip')"


def script_check(html: str) -> str | None:
    """Return an error string if the last <script> does not parse (needs node)."""
    node = shutil.which("node")
    if not node or "<script>" not in html:
        return None
    src = html[html.rindex("<script>") + 8: html.rindex("</script>")]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(src)
    r = subprocess.run([node, "--check", f.name], capture_output=True, text=True)
    return None if r.returncode == 0 else r.stderr.strip().splitlines()[-1]


async def check_view(browser, url, name, ctx_args, out):
    fails, notes = [], []
    ctx = await browser.new_context(**ctx_args)
    page = await ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
    page.on("console", lambda m: errors.append(f"console: {m.text}") if m.type == "error" else None)
    await page.goto(url)
    await page.wait_for_timeout(1500)
    p = await page.evaluate(PROBE)

    if p["scrollWidth"] > p["width"] + 1:
        fails.append(f"sideways scroll: page is {p['scrollWidth']}px wide in a {p['width']}px viewport")
    for key, label in [("radar", "radar chart"), ("matrix", "impact-effort matrix")]:
        if not p[key]:
            fails.append(f"{label} is empty")
    if not p["funnelRows"] or not p["segs"]:
        fails.append("task friction strip is empty")
    if not p["walkTables"]:
        fails.append("walkthrough has no task tables")
    if p["heurRows"] != 10:
        fails.append(f"heuristics list has {p['heurRows']} rows instead of 10")
    if p["testCards"] and p["testCards"] != 5:
        fails.append(f"usability-test plan shows {p['testCards']} tasks instead of 5")
    if not p["kpis"]:
        fails.append("KPI row has no numbers")
    if not p["rows"]:
        fails.append("opportunities table is empty")
    if p["badCells"]:
        fails.append(f"{p['badCells']} table cells are not wrapped in one .cv (breaks the phone layout)")
    if p["overflows"]:
        fails.append(f"{p['overflows']} labels overflow their box (text runs into the next column)")
    if p["overlaps"]:
        fails.append(f"{p['overlaps']} overlapping text labels in the task strip, KPIs or task titles")
    if not p["terms"]:
        notes.append("no tooltip terms found (.t)")

    await page.screenshot(path=str(out / f"{name}-top.png"))

    # Tooltip: hover on desktop, tap (and second tap closes) on touch.
    term = await page.query_selector("#ops .t") or await page.query_selector(".t")
    if term:
        await term.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)
        if name == "desktop":
            await term.hover()
        else:
            await term.tap()
        await page.wait_for_timeout(250)
        if not await page.evaluate(TIP_VISIBLE):
            fails.append("tooltip does not open on " + ("hover" if name == "desktop" else "tap"))
        else:
            await page.screenshot(path=str(out / f"{name}-tooltip.png"))
            if name != "desktop":
                await term.tap()
                await page.wait_for_timeout(250)
                if await page.evaluate(TIP_VISIBLE):
                    fails.append("tooltip does not close on a second tap")

    # Filters: each chip re-renders the table; cells and tooltips must survive.
    chips = await page.query_selector_all("#ops .chip[data-f]")
    for chip in chips:
        f = await chip.get_attribute("data-f")
        await chip.click()
        await page.wait_for_timeout(200)
        p2 = await page.evaluate(PROBE)
        if p2["rows"] == 0 and f == "all":
            fails.append("filter 'all' leaves the table empty")
        if p2["badCells"]:
            fails.append(f"after filter '{f}' table cells lose their .cv wrapper")
        if p["tableTerms"] and p2["rows"] and p2["tableTerms"] == 0 and f == "all":
            fails.append("tooltips disappear from the table after filtering")
    if chips:
        await chips[0].click()
        await page.wait_for_timeout(200)

    for sel, label in [("#walk", "walk"), ("#ops", "table"), ("#plan", "plan"), ("#test", "test")]:
        if await page.query_selector(sel):
            await page.evaluate(f"document.querySelector('{sel}').scrollIntoView()")
            await page.wait_for_timeout(200)
            await page.screenshot(path=str(out / f"{name}-{label}.png"))

    if name == "phone":
        await page.emulate_media(color_scheme="dark")
        await page.evaluate("scrollTo(0,0)")
        await page.wait_for_timeout(300)
        await page.screenshot(path=str(out / "phone-dark.png"))

    fails += errors
    await ctx.close()
    return {"view": name, "ok": not fails, "fails": fails, "notes": notes, "facts": p}


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out", default="report-check")
    ap.add_argument("--browser", help="path to Chrome/Chromium if Playwright's own is not installed")
    a = ap.parse_args()

    path = pathlib.Path(a.report).resolve()
    if not path.exists():
        print(f"not found: {path}")
        return 2
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    results = []
    err = script_check(path.read_text(encoding="utf-8"))
    if err:
        results.append({"view": "script", "ok": False, "fails": [f"script does not parse: {err}"]})

    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("playwright is not installed: pip install playwright && playwright install chromium")
        return 2

    async with async_playwright() as pw:
        launch = {"args": ["--no-sandbox"]}
        exe = a.browser or next((shutil.which(b) for b in ("google-chrome", "chromium", "chromium-browser") if shutil.which(b)), None)
        try:
            browser = await pw.chromium.launch(**launch)
        except Exception:
            if not exe:
                print("no browser: run `playwright install chromium` or pass --browser")
                return 2
            browser = await pw.chromium.launch(executable_path=exe, **launch)
        for name, ctx_args in VIEWS:
            results.append(await check_view(browser, path.as_uri(), name, ctx_args, out))
        await browser.close()

    ok = all(r["ok"] for r in results)
    for r in results:
        status = "PASS" if r["ok"] else "FAIL"
        print(f"[{status}] {r['view']}")
        for f in r.get("fails", []):
            print(f"   - {f}")
        for n in r.get("notes", []):
            print(f"   note: {n}")
    print(f"screenshots: {out.resolve()}")
    (out / "result.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
