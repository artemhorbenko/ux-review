#!/usr/bin/env python3
"""Turn a ux-review audit.json into a hands-off file for an AI agent or a developer.

Usage: python build_handoff.py audit.json handoff.md [--json tasks.json]

The report page is for people; this file is for whoever implements the fixes.
Plain Markdown, no design: context, persona, sources, rules, then one task per
issue in priority order with the user task and step, the heuristics broken,
evidence, the proposed change, steps, acceptance criteria, a usability-test
script to verify it, and dependencies. Optional tasks.json carries the same
tasks for a tracker. Standard library only.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from validate_audit import validate  # noqa: E402

TOKENS = re.compile(r"\{(health|qw|n|conf|done|tasks|blockers)\}")
HEUR = {
    "en": ["Visibility of system status", "Match with the real world", "User control and freedom", "Consistency and standards", "Error prevention",
           "Recognition rather than recall", "Flexibility and efficiency", "Minimalist design", "Recognize and recover from errors", "Help and documentation"],
    "uk": ["Видимість стану системи", "Мова користувача", "Контроль і свобода", "Узгодженість і стандарти", "Запобігання помилкам",
           "Впізнавання замість пригадування", "Гнучкість і ефективність", "Мінімалістичний дизайн", "Розпізнати й виправити помилку", "Довідка й документація"],
}
L = {
    "en": dict(title="Hands-off", intro="Implementation brief generated from the UX review. Work top to bottom: tasks are ordered by ICE, and a task always comes after the ones it depends on. Every task ends with a short usability check; a fix is done when real users pass it, not when the code ships. Treat \"rethink\" and \"hypothesis\" tasks as experiments: prototype and test before building.",
               context="Context", finding="Main finding", persona="Persona", conf="Confidence", walked="Key tasks walked", out={"ok": "done", "hard": "done with trouble", "fail": "failed", "stop": "stopped at submit"},
               answers="Owner answers and assumptions", skipped="skipped", sources="Data sources", missing="Missing, so lower confidence",
               rules="Rules for the implementer", order="Suggested order", tasks="Tasks", task="Task", ice="ICE", type="Type", sev="Severity", evidence="Evidence",
               type_o="fix", type_x="rethink", ev_o="observed", ev_h="hypothesis", lens="Lens", where="Where", step="step", heur="Heuristics broken",
               why="What we saw", change="Proposed change", steps="Steps", accept="Acceptance criteria", verify="Verify with users", vtask="Task script", vok="Success when", vwatch="Watch for",
               cheap="Cheapest check", metric="Metric", effort="Effort", risk="Risk / guardrail", alt="Alternatives rejected", pm="Pre-mortem", hypo="Hypothesis",
               copy="Copy variants", top="top 3", dep="Depends on", glossary="Glossary", testplan="Usability-test plan (5 tasks)", who="Participants", n="How many", method="Format", before="Before the session",
               start="Start", ok="Success", watch="Watch for", ask="Ask afterwards", measure="Measure", after="After the sessions",
               sevn=["", "cosmetic", "minor", "major", "blocker"], nsteps="steps", worstf="worst friction",
               default_rules=["Do not submit real forms, payments or messages while testing; use staging or a test mode.",
                              "Keep URLs; if a page moves, add a 301 redirect from the old address.",
                              "For every change record before/after screenshots at 1280px and 390px and a keyboard pass (Tab, Enter, Escape).",
                              "Do not invent prices, numbers, testimonials or promises; use only what the business confirms.",
                              "Stay within UX: visual polish belongs to a UI review, strategy to a product review.",
                              "When a task is a hypothesis, run its usability check first and stop if the threshold is not met."]),
    "uk": dict(title="Hands-off", intro="Бриф на впровадження, згенерований з UX-рев'ю. Ідіть згори донизу: задачі впорядковано за ICE, і кожна стоїть після тих, від яких залежить. Кожна задача закінчується короткою перевіркою з користувачами; виправлення готове, коли люди її проходять, а не коли код у проді. Задачі «переосмислити» і «гіпотеза» — експерименти: спершу прототип і тест.",
               context="Контекст", finding="Головна знахідка", persona="Персона", conf="Впевненість", walked="Пройдені ключові задачі", out={"ok": "виконано", "hard": "з труднощами", "fail": "не вдалося", "stop": "зупинено перед відправкою"},
               answers="Відповіді власника й припущення", skipped="пропущено", sources="Джерела даних", missing="Бракує, тому впевненість нижча",
               rules="Правила для виконавця", order="Рекомендований порядок", tasks="Задачі", task="Задача", ice="ICE", type="Тип", sev="Серйозність", evidence="Доказ",
               type_o="виправити", type_x="переосмислити", ev_o="спостережено", ev_h="гіпотеза", lens="Лінза", where="Де", step="крок", heur="Порушені евристики",
               why="Що побачили", change="Запропонована зміна", steps="Кроки", accept="Критерії приймання", verify="Перевірити з користувачами", vtask="Сценарій завдання", vok="Успіх, якщо", vwatch="Що спостерігати",
               cheap="Найдешевша перевірка", metric="Метрика", effort="Зусилля", risk="Ризик / запобіжник", alt="Відкинуті альтернативи", pm="Pre-mortem", hypo="Гіпотеза",
               copy="Варіанти тексту", top="топ-3", dep="Залежить від", glossary="Глосарій", testplan="План юзабіліті-тесту (5 завдань)", who="Учасники", n="Скільки", method="Формат", before="Перед сесією",
               start="Старт", ok="Успіх", watch="Що спостерігати", ask="Спитати після", measure="Що вимірювати", after="Після сесій",
               sevn=["", "косметична", "дрібна", "серйозна", "блокер"], nsteps="кроків", worstf="найбільше тертя",
               default_rules=["Не відправляти справжні форми, платежі чи повідомлення під час тестів; використовувати staging або тестовий режим.",
                              "Зберігати URL; якщо сторінка переїжджає — 301-редирект зі старої адреси.",
                              "Для кожної зміни — скріншоти до й після на 1280px і 390px та прохід клавіатурою (Tab, Enter, Escape).",
                              "Не вигадувати ціни, цифри, відгуки чи обіцянки; лише те, що підтвердив бізнес.",
                              "Лишатися в межах UX: візуальне полірування — це UI-рев'ю, стратегія — продуктове рев'ю.",
                              "Якщо задача — гіпотеза, спершу її перевірка з користувачами; зупинитися, якщо поріг не досягнуто."]),
}


def clean(s, ctx):
    s = TOKENS.sub(lambda m: str(ctx.get(m.group(1), m.group(0))), str(s))
    return s.replace("[[", "**").replace("]]", "**")


def build(a):
    lang = (a.get("lang") or "en")[:2]
    t = L.get(lang, L["en"])
    hn = HEUR.get(lang, HEUR["en"])
    ops = a.get("ops") or []
    detail, plans = a.get("detail") or {}, a.get("plans") or {}
    lenses = a.get("lenses") or []
    sources = a.get("sources") or []
    utasks = a.get("tasks") or []
    by_tid = {u.get("id"): u for u in utasks}
    health = round(sum(l.get("s", 0) for l in lenses) / len(lenses)) if lenses else 0
    conf = round(sum({"ok": 1, "demo": .6}.get(s.get("status"), 0) for s in sources) / len(sources) * 100) if sources else 0
    qw = sum(1 for o in ops if o.get("I", 0) >= 6 and 11 - o.get("E", 0) <= 5)
    done = sum(1 for u in utasks if u.get("out") == "ok")
    blockers = sum(1 for u in utasks for s in (u.get("steps") or []) if s.get("f") == 3)
    ctx = dict(health=health, qw=qw, n=len(ops), conf=conf, done=done, tasks=len(utasks), blockers=blockers)
    text = a.get("text") or {}

    def where(o):
        u = by_tid.get(o.get("task"))
        if not u:
            return ""
        s = f"{u['id']} {u.get('t', '')}"
        st = o.get("step")
        if st and 1 <= st <= len(u.get("steps") or []):
            step = u["steps"][st - 1]
            s += f" → {t['step']} {st}: {step.get('s', '')}" + (f" ({step['page']})" if step.get("page") else "")
        return s

    tasks = []
    for i, o in enumerate(ops, 1):
        d = detail.get(str(i), {})
        p = plans.get(str(i), {})
        accept = list(d.get("accept") or [])
        if not accept:
            if d.get("thr"):
                accept.append(d["thr"])
            if d.get("metric"):
                accept.append(f"{t['metric']}: {d['metric']}")
        v = d.get("test") or {}
        tasks.append(dict(
            id=f"UX{i:02d}", n=i, title=o.get("t"), lens=o.get("ln"), lens_id=o.get("l"),
            type="rethink" if o.get("x") == "ex" else "fix",
            evidence_type="hypothesis" if o.get("ev") == "hyp" else "observed",
            severity=o.get("sev"), heuristics=o.get("h") or [],
            user_task=o.get("task"), user_step=o.get("step"), where=where(o),
            impact=o.get("I"), confidence=o.get("C"), ease=o.get("E"),
            ice=o.get("I", 0) * o.get("C", 0) * o.get("E", 0),
            evidence=d.get("why", ""), change=d.get("change", ""), steps=d.get("steps") or [], acceptance=accept,
            usability_test={"task": v.get("task", ""), "success": v.get("success", ""), "watch": v.get("watch", "")},
            cheapest_check=p.get("t") or d.get("verify") or "", hypothesis=p.get("h", ""),
            metric=d.get("metric", ""), effort=d.get("effort", ""), risk=d.get("risk", ""),
            alternatives=d.get("alt") or [], risk_type=d.get("rtype", ""), pre_mortem=d.get("pm", ""),
            copy=d.get("copy") or [], depends_on=d.get("depends") or [],
        ))
    tasks.sort(key=lambda x: (-x["ice"], -(x["severity"] or 0), x["n"]))
    by_id, done_ids, ordered = {tk["id"]: tk for tk in tasks}, set(), []

    def place(tk, seen=()):
        if tk["id"] in done_ids or tk["id"] in seen:
            return
        for dep in tk["depends_on"]:
            if dep in by_id:
                place(by_id[dep], seen + (tk["id"],))
        done_ids.add(tk["id"])
        ordered.append(tk)
    for tk in tasks:
        place(tk)
    tasks = ordered
    for rank, tk in enumerate(tasks, 1):
        tk["rank"] = rank

    out = []
    w = out.append
    w(f"# {t['title']}: {a.get('title', '')}".rstrip(": "))
    w("")
    w(t["intro"])
    w("")
    w(f"## {t['context']}")
    w("")
    if text.get("headline"):
        w(f"- **{t['finding']}:** {clean(text['headline'], ctx).replace('**', '')}")
    if text.get("lead"):
        w(f"- {clean(text['lead'], ctx)}")
    if a.get("persona"):
        w(f"- **{t['persona']}:** {a['persona']}")
    w(f"- **{t['conf']}:** {conf}%")
    w("")
    if utasks:
        w(f"### {t['walked']}")
        w("")
        for u in utasks:
            worst = max((s.get("f") or 0 for s in u.get("steps") or []), default=0)
            w(f"- {u['id']} {u.get('t')} — {t['out'].get(u.get('out'), u.get('out'))}; {len(u.get('steps') or [])} {t['nsteps']}, {t['worstf']} {worst}/3")
        w("")
    if a.get("answers"):
        w(f"### {t['answers']}")
        w("")
        for q in a["answers"]:
            mark = f" ({t['skipped']})" if q.get("skipped") else ""
            w(f"- {q.get('q')}{mark}: {q.get('a')}")
        w("")
    if sources:
        w(f"### {t['sources']}")
        w("")
        for s in sources:
            w(f"- [{s.get('status')}] {s.get('name')}" + (f" — {s['note']}" if s.get("note") else ""))
        miss = [s.get("name") for s in sources if s.get("status") == "no"]
        if miss:
            w("")
            w(f"{t['missing']}: {', '.join(miss)}.")
        w("")
    w(f"## {t['rules']}")
    w("")
    for r in (a.get("rules") or t["default_rules"]):
        w(f"- {r}")
    w("")
    w(f"## {t['order']}")
    w("")
    w(f"| # | ID | {t['task']} | {t['where']} | {t['sev']} | {t['ice']} | {t['type']} | {t['evidence']} |")
    w("|---|---|---|---|---|---|---|---|")
    for tk in tasks:
        top = f" ({t['top']})" if tk["rank"] <= 3 else ""
        loc = f"{tk['user_task']}" + (f" · {t['step']} {tk['user_step']}" if tk["user_step"] else "") if tk["user_task"] else "—"
        w(f"| {tk['rank']} | {tk['id']} | {tk['title']}{top} | {loc} | {tk['severity']} {t['sevn'][tk['severity'] or 0]} | {tk['ice']} | {t['type_x'] if tk['type'] == 'rethink' else t['type_o']} | {t['ev_h'] if tk['evidence_type'] == 'hypothesis' else t['ev_o']} |")
    w("")
    w(f"## {t['tasks']}")
    for tk in tasks:
        w("")
        w(f"### {tk['rank']}. {tk['id']} — {tk['title']}")
        w("")
        w(f"- {t['lens']}: {tk['lens']} · {t['sev']}: {tk['severity']} {t['sevn'][tk['severity'] or 0]} · {t['ice']} {tk['ice']} = {tk['impact']}×{tk['confidence']}×{tk['ease']} · {t['type_x'] if tk['type'] == 'rethink' else t['type_o']} · {t['ev_h'] if tk['evidence_type'] == 'hypothesis' else t['ev_o']}")
        if tk["where"]:
            w(f"- {t['where']}: {tk['where']}")
        if tk["heuristics"]:
            w(f"- {t['heur']}: " + "; ".join(f"{h} {hn[int(h[1:]) - 1]}" for h in tk["heuristics"] if re.fullmatch(r"H(10|[1-9])", h)))
        if tk["effort"]:
            w(f"- {t['effort']}: {tk['effort']}")
        if tk["depends_on"]:
            w(f"- {t['dep']}: {', '.join(tk['depends_on'])}")
        w("")
        if tk["evidence"]:
            w(f"**{t['why']}.** {tk['evidence']}")
            w("")
        if tk["change"]:
            w(f"**{t['change']}.** {tk['change']}")
            w("")
        if tk["hypothesis"]:
            w(f"**{t['hypo']}.** {tk['hypothesis']}")
            w("")
        if tk["steps"]:
            w(f"**{t['steps']}:**")
            w("")
            for j, s in enumerate(tk["steps"], 1):
                w(f"{j}. {s}")
            w("")
        if tk["acceptance"]:
            w(f"**{t['accept']}:**")
            w("")
            for c in tk["acceptance"]:
                w(f"- [ ] {c}")
            w("")
        ut = tk["usability_test"]
        if ut["task"]:
            w(f"**{t['verify']}:**")
            w("")
            w(f"- {t['vtask']}: {ut['task']}")
            if ut["success"]:
                w(f"- {t['vok']}: {ut['success']}")
            if ut["watch"]:
                w(f"- {t['vwatch']}: {ut['watch']}")
            w("")
        if tk["cheapest_check"]:
            w(f"**{t['cheap']}:** {tk['cheapest_check']}")
            w("")
        if tk["metric"]:
            w(f"**{t['metric']}:** {tk['metric']}")
            w("")
        if tk["risk"]:
            w(f"**{t['risk']}:** {tk['risk']}")
            w("")
        if tk["alternatives"]:
            w(f"**{t['alt']}:**")
            w("")
            for x in tk["alternatives"]:
                w(f"- {x}")
            w("")
        if tk["pre_mortem"]:
            w(f"**{t['pm']}:** {tk['pre_mortem']}")
            w("")
        if tk["copy"]:
            w(f"**{t['copy']}:**")
            w("")
            for x in tk["copy"]:
                w(f"- {x}")
            w("")
    tp = a.get("testplan")
    if tp:
        w(f"## {t['testplan']}")
        w("")
        for k in ("who", "n", "method", "before"):
            if tp.get(k):
                w(f"- **{t[k]}:** {tp[k]}")
        w("")
        for i, x in enumerate(tp.get("tasks") or [], 1):
            w(f"{i}. **{x.get('t')}**")
            if x.get("start"):
                w(f"   - {t['start']}: {x['start']}")
            if x.get("success"):
                w(f"   - {t['ok']}: {x['success']}")
            if x.get("watch"):
                w(f"   - {t['watch']}: {x['watch']}")
            if x.get("ask"):
                w(f"   - {t['ask']}: " + " / ".join(x["ask"]))
        w("")
        if tp.get("measure"):
            w(f"**{t['measure']}:** " + "; ".join(tp["measure"]) + ".")
            w("")
        if tp.get("after"):
            w(f"**{t['after']}:** {tp['after']}")
            w("")
    gl = a.get("glossary") or {}
    if gl:
        w(f"## {t['glossary']}")
        w("")
        for k, v in gl.items():
            w(f"- **{k}** ({v.get('g')}): {v.get('d')}")
        w("")
    return "\n".join(out).rstrip() + "\n", tasks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audit")
    ap.add_argument("out")
    ap.add_argument("--json", help="also write tasks as JSON for a tracker")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    with open(a.audit, encoding="utf-8") as f:
        audit = json.load(f)
    err, _ = validate(audit)
    if err and not a.force:
        for e in err:
            print("[ERROR]", e)
        print("Not built. Fix audit.json or pass --force.")
        return 1
    md, tasks = build(audit)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(md)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"title": audit.get("title"), "lang": audit.get("lang"), "persona": audit.get("persona"),
                       "tasks": tasks, "usability_test_plan": audit.get("testplan")}, f, ensure_ascii=False, indent=1)
    print(f"Written {a.out} ({len(tasks)} tasks)" + (f" and {a.json}" if a.json else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
