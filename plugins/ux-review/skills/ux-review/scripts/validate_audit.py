#!/usr/bin/env python3
"""Check a ux-review audit.json before it becomes a report.

Usage: python validate_audit.py audit.json

Errors (exit 1) break the report or the skill's rules; warnings (exit 0)
are worth a look. Standard library only.
"""
import json
import re
import sys

ICONS = {"heur", "walk", "ia", "copy", "form", "state", "trust", "dec", "a11y", "mob"}
GROUPS = {"base", "find", "act", "decide", "reach"}
LANGS = {"uk", "en"}
STATUSES = {"ok", "demo", "no"}
OUTCOMES = {"ok", "hard", "fail", "stop"}
CW = {"y", "p", "n", None}
HEUR = {f"H{i}" for i in range(1, 11)}
TOKENS = re.compile(r"\{(health|qw|n|conf|done|tasks|blockers)\}")
TEXT_KEYS = ["headline", "lead", "lensesH", "walkH", "heurH", "matrixH", "opsH", "nextH", "planH", "testH", "dataH"]
SUBMIT = re.compile(r"\b(submit|send|book|sign ?up|register|pay|checkout|відправ|надісл|оплат|зареєстр)", re.I)


def validate(a):
    err, warn = [], []
    E, W = err.append, warn.append

    if not isinstance(a, dict):
        return ["the file is not a JSON object"], []

    if a.get("lang") not in LANGS:
        W(f"lang '{a.get('lang')}' has no interface dictionary; labels fall back to English (add an entry to UI and HEUR in the template)")

    text = a.get("text") or {}
    for k in TEXT_KEYS:
        if not str(text.get(k, "")).strip():
            E(f"text.{k} is missing: every section needs a heading that states its point")
    if "<" in json.dumps(text, ensure_ascii=False):
        W("text contains '<': HTML is shown as plain text; use [[...]] to highlight words in the headline")
    if not a.get("persona"):
        W("persona is missing: say whose tasks were walked (role, company size, device)")

    # lenses
    lenses = a.get("lenses") or []
    if len(lenses) != 10:
        W(f"{len(lenses)} lenses instead of 10")
    for i, l in enumerate(lenses):
        p = f"lenses[{i}]"
        if l.get("i") not in ICONS:
            E(f"{p}.i '{l.get('i')}' is not an icon id ({', '.join(sorted(ICONS))})")
        if l.get("g") not in GROUPS:
            E(f"{p}.g '{l.get('g')}' is not a group ({', '.join(sorted(GROUPS))})")
        s = l.get("s")
        if not isinstance(s, (int, float)) or not 0 <= s <= 100:
            E(f"{p}.s must be a number 0-100")
        if not l.get("k"):
            E(f"{p}.k (short name) is missing")

    # tasks (header picture + walkthrough)
    tasks = a.get("tasks") or []
    if not tasks:
        E("tasks is empty: walk at least one key task step by step")
    elif not 3 <= len(tasks) <= 7:
        W(f"{len(tasks)} key tasks; 3-7 keeps the header readable")
    tids = set()
    for i, t in enumerate(tasks):
        p = f"tasks[{i}]"
        if not t.get("id") or not t.get("t"):
            E(f"{p} needs id (e.g. T1) and t (task in the persona's words)")
        tids.add(t.get("id"))
        if t.get("out") not in OUTCOMES:
            E(f"{p}.out must be ok, hard, fail or stop")
        steps = t.get("steps") or []
        if len(steps) < 2:
            E(f"{p} needs at least 2 steps")
        for j, s in enumerate(steps):
            q = f"{p}.steps[{j}]"
            if not s.get("s"):
                E(f"{q}.s (what the person does) is missing")
            f = s.get("f")
            if f is not None and f not in (0, 1, 2, 3):
                E(f"{q}.f must be 0-3 or null (not tested)")
            for k in ("k", "see", "rec"):
                if s.get(k) not in CW:
                    E(f"{q}.{k} must be y, p, n or null")
            if f is not None and f >= 2 and not str(s.get("note", "")).strip():
                E(f"{q} has friction {f} but no note: say what you saw")
        if t.get("out") == "ok" and any((s.get("f") or 0) >= 3 for s in steps):
            W(f"{p} has a blocker step but outcome ok")
        if t.get("out") == "stop" and steps and steps[-1].get("f") is not None and SUBMIT.search(steps[-1].get("s", "")):
            W(f"{p} stopped before submit, but the last step has a friction score: use f: null for the step you did not perform")

    # opportunities / issues
    ops = a.get("ops") or []
    if not ops:
        E("ops is empty")
    seen_pts = {}
    detail = a.get("detail") or {}
    for i, o in enumerate(ops):
        p, oid = f"ops[{i}] (#{i + 1})", i + 1
        for k in ("I", "C", "E"):
            v = o.get(k)
            if not isinstance(v, int) or not 1 <= v <= 10:
                E(f"{p}.{k} must be a whole number 1-10")
        sev = o.get("sev")
        if sev not in (1, 2, 3, 4):
            E(f"{p}.sev must be 1 cosmetic, 2 minor, 3 major or 4 blocker")
        elif isinstance(o.get("I"), int):
            if sev == 4 and o["I"] < 7:
                W(f"{p} is a blocker (sev 4) with impact {o['I']}: impact should be 7 or more")
            if sev == 1 and o["I"] > 5:
                W(f"{p} is cosmetic (sev 1) with impact {o['I']}: check the scores")
        if o.get("x") not in ("opt", "ex"):
            E(f"{p}.x must be opt (fix) or ex (rethink)")
        if o.get("ev") not in ("obs", "hyp"):
            E(f"{p}.ev must be obs (observed) or hyp (hypothesis)")
        if o.get("l") not in ICONS:
            E(f"{p}.l '{o.get('l')}' is not a lens icon id")
        if not o.get("t") or not o.get("ln"):
            E(f"{p} needs t (title) and ln (lens label)")
        hs = o.get("h") or []
        bad = [h for h in hs if h not in HEUR]
        if bad:
            E(f"{p}.h has unknown heuristics {bad}: use H1-H10")
        if not hs:
            W(f"{p} names no heuristic (h): most UX issues break at least one")
        if o.get("task") and tids and o["task"] not in tids:
            E(f"{p}.task '{o['task']}' is not a task id")
        if o.get("task") and o.get("step"):
            t = next((t for t in tasks if t.get("id") == o["task"]), None)
            if t and not 1 <= o["step"] <= len(t.get("steps") or []):
                E(f"{p}.step {o['step']} is outside task {o['task']}")
        if isinstance(o.get("I"), int) and isinstance(o.get("E"), int):
            seen_pts.setdefault((o["E"], o["I"]), []).append(oid)
        d = detail.get(str(oid))
        if not d:
            E(f"{p} has no detail[\"{oid}\"]: every issue needs its evidence and steps")
            continue
        if not str(d.get("why", "")).strip():
            E(f"detail[\"{oid}\"].why is empty: every finding must point to evidence")
        if not str(d.get("change", "")).strip():
            E(f"detail[\"{oid}\"].change is empty: say what the new experience is")
        if len(d.get("steps") or []) < 2:
            E(f"detail[\"{oid}\"].steps needs at least 2 concrete steps")
        for k in ("metric", "effort", "risk"):
            if not str(d.get(k, "")).strip():
                E(f"detail[\"{oid}\"].{k} is missing")
        v = d.get("test") or {}
        if not v.get("task") or not v.get("success"):
            E(f"detail[\"{oid}\"].test needs task and success: how a real user will confirm the fix")
        if o.get("ev") == "hyp" and isinstance(o.get("C"), int) and o["C"] > 7:
            W(f"{p} is a hypothesis with confidence {o['C']}: confidence above 7 needs evidence")
    for pt, ids in seen_pts.items():
        if len(ids) > 2:
            W(f"issues {ids} share one matrix point (effort {11 - pt[0]}, impact {pt[1]}); the dots are spread, but check the scores")
    for k in detail:
        if not k.isdigit() or not 1 <= int(k) <= len(ops):
            E(f"detail[\"{k}\"] does not match any issue")

    def ice(o):
        return o.get("I", 0) * o.get("C", 0) * o.get("E", 0)
    ranked = sorted(range(1, len(ops) + 1), key=lambda j: (-ice(ops[j - 1]), -(ops[j - 1].get("sev") or 0), j))
    for oid in ranked[:3]:
        pl = (a.get("plans") or {}).get(str(oid))
        if not pl or not all(str(pl.get(k, "")).strip() for k in ("h", "m", "t")):
            E(f"top-3 issue #{oid} needs plans[\"{oid}\"] with h (hypothesis), m (metric), t (cheapest check)")
        d = detail.get(str(oid)) or {}
        for k in ("alt", "rtype", "thr", "pm"):
            if not d.get(k):
                E(f"top-3 issue #{oid} needs detail.{k} (alternatives, risk type, threshold, pre-mortem)")

    # usability-test plan
    tp = a.get("testplan")
    if not tp:
        E("testplan is missing: the review ships a 5-task usability-test plan")
    else:
        tt = tp.get("tasks") or []
        if len(tt) != 5:
            E(f"testplan.tasks has {len(tt)} tasks; the plan has exactly 5")
        for i, t in enumerate(tt):
            for k in ("t", "success"):
                if not str(t.get(k, "")).strip():
                    E(f"testplan.tasks[{i}].{k} is missing")
            if re.search(r"\b(click|press|tap|натисн|клікн)\b", t.get("t", ""), re.I):
                W(f"testplan.tasks[{i}] tells the participant what to click; describe the goal, not the UI")
        if not tp.get("who"):
            E("testplan.who is missing: say who to recruit")

    # sources and numbers
    sources = a.get("sources") or []
    names = {s.get("name") for s in sources}
    if not sources:
        E("sources is empty: list what was used and what was missing")
    for i, s in enumerate(sources):
        if s.get("status") not in STATUSES:
            E(f"sources[{i}].status must be ok, demo or no")
    for i, k in enumerate(a.get("kpis") or []):
        if k.get("v") is None:
            continue
        v = str(k.get("v", ""))
        if not TOKENS.search(v) and re.search(r"\d", v):
            if not k.get("src"):
                E(f"kpis[{i}] '{k.get('v')}' has a number but no src: name the source it came from")
            elif k["src"] not in names:
                E(f"kpis[{i}].src '{k['src']}' is not in sources")
            elif next((s for s in sources if s.get("name") == k["src"]), {}).get("status") == "no":
                E(f"kpis[{i}] cites '{k['src']}', which is marked as not available")

    for i, q in enumerate(a.get("answers") or []):
        if not q.get("q") or not q.get("a"):
            E(f"answers[{i}] needs q and a (for a skipped question, a = the assumption taken)")

    gl = a.get("glossary") or {}
    for k, v in gl.items():
        if not v.get("g") or not v.get("d"):
            E(f"glossary['{k}'] needs g (short gloss) and d (definition)")
    if not gl:
        W("glossary is empty: terms will have no tooltips")
    return err, warn


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        try:
            a = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[ERROR] not valid JSON: {e}")
            return 1
    err, warn = validate(a)
    for e in err:
        print("[ERROR]", e)
    for w in warn:
        print("[WARN] ", w)
    print("OK" if not err else f"{len(err)} error(s)")
    return 1 if err else 0


if __name__ == "__main__":
    sys.exit(main())
