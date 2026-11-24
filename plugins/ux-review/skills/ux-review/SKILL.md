---
name: ux-review
description: UX review of a website, web app, SaaS flow or app screenshots - walk the key user tasks step by step (cognitive walkthrough) and check Nielsen's 10 heuristics, information architecture and navigation, microcopy, forms, trust, accessibility basics, mobile ergonomics, decision support (pricing, comparison) and error states. Delivers a visual report with friction per task step, prioritized fixes, a 5-task usability-test plan, and a hands-off file for AI agents. Use when someone asks for a UX review, usability audit, heuristic evaluation, "why can't people find / do X on my site", or to check a flow before a launch. Not for visual polish (ui-review) or product strategy (product-lens-audit).
---

# UX Review

Walk the tasks that matter to one persona, step by step, and find where people cannot tell what to do, cannot see that it worked, or cannot recover. Turn that into a short, prioritized list of fixes in a visual report, a hands-off file for whoever implements them, and a usability-test plan to check the fixes with real people.

Respond in the user's language, and write the report in it too.

**Scope.** Can people find, understand, decide and act? Leave visual polish to a UI review (`ui-review`) and strategy, pricing models and growth to `product-lens-audit`. A visual or pricing point is in scope only when it blocks a task (see `references/lenses.md`).

Files next to this SKILL.md (read each when its step comes, not up front):
- `references/data-sources.md` - which tools to look for, how to walk a site in a browser, phone width and keyboard checks, fallbacks (steps 0-2).
- `references/lenses.md` - the 10 UX lenses, Nielsen's heuristics H1-H10, the walkthrough questions, severity, icon and group ids (steps 2-3).
- `references/report-spec.md` and `references/audit.schema.json` - the report's sections and the shape of its data (step 5).
- `assets/report-template.html` - the report page; it renders everything from one JSON block. `assets/example-audit.en.json` is a full example (fictional product "Parcelly"); `assets/example-handoff.en.md` is its hands-off file.
- `scripts/validate_audit.py`, `scripts/build_report.py`, `scripts/build_handoff.py`, `scripts/check_report.py` - data check, page build, hands-off build, render check.

## 0. Check which data sources are connected

Look at the tools this session actually has (search the tool list / ToolSearch; never assume). The browser is the main source; analytics, session recordings, accessibility scanners and support data sharpen severity. Build a source list with a status for each: `ok` (connected and used), `demo` (partial: a sample, a screenshot, a frame instead of a real phone), `no` (not connected, or returning an error). Use every source read-only. If an important source is missing, say which in one line and continue; never fill the gap with invented numbers.

## 0.5 Ask the requester (up to 4 questions, every one skippable)

First look for saved context: a `ux-review-context.md` or a previous `audit.json` in the project or attached. Read it and ask only about what it does not cover. With a previous `audit.json`, say in the report what changed: which issues were fixed, which tasks now pass.

Skip any question the request already answers. Ask the rest in one round, with a multiple-choice tool when available (AskUserQuestion or similar) and a "Skip" option on each; otherwise in plain text. Never block: if the person skips or does not answer, state the assumption and continue.
- **Who is the user** (role, company size, device, first visit or returning)?
- **Which 3-7 tasks matter most** right now (in the user's words, with an end point)?
- **What data can you share**: analytics, recordings, support questions, earlier tests? Screenshots are fine.
- **What was tested or changed already**, and anything you must not touch (a form that must not be submitted, a login)?

Record each answer in `answers`; a skipped one shows "Skipped" plus the assumption.

## 1. Gather (before judging)

- **Walk each task live** as the persona: in a browser, step by step, from a neutral start (the home page or a web search). Note the page, what you clicked, what you saw. Screenshots of each step help.
- **Repeat at phone width** (390px) for the key steps; if the window cannot be resized, use a 390px same-origin frame or a headless browser (`references/data-sources.md`).
- **Keyboard pass**: Tab through the header and one key task and log the focus order.
- **Read forms and hidden content from the page**: fields, required, input types, autocomplete, labels; collapsed FAQ; menu items.
- **Stay on the domain the person named.** Subdomains (`get.`, `go.`, `lp.`, `staging.`) are often old A/B variants or staging copies; if search sends the persona there, note it and ask the owner, but judge the main site. Before saying a page does not exist, check the menus, the sitemap and likely addresses with a same-origin request (`references/data-sources.md`).
- **Never submit real forms**, payments, messages, sign-ups or newsletter boxes, and reject non-essential cookies. Stop before the final button; mark that step `f: null` (not tested) and the task outcome `stop`.
- **Screenshots, recordings, analytics** the user shares count as evidence; note the date range.

## 2. Walk each task (cognitive walkthrough)

For every step ask: **Know** - will the person know what to do? **See** - will they see it worked? **Recover** - can they get back from a wrong turn? Mark `y`, `p`, `n` or `null`; rate friction 0 none, 1 minor, 2 major, 3 blocker, and write what you saw for every step with friction 2 or more. Give each task an outcome: `ok`, `hard`, `fail`, `stop`. These steps become the report's header picture.

## 3. Apply the 10 lenses and tag heuristics

Read `references/lenses.md` and go through all 10 lenses in 5 groups: foundations (Nielsen's heuristics, task walkthroughs), find and understand (IA and navigation, content and microcopy), act and recover (forms, error and empty states), decide with confidence (trust, decision support), reach everyone (accessibility basics, mobile). For each, write 1-3 findings tied to a page and step, and score it 0-100. Tag every issue with the heuristics it breaks (H1-H10).

## 4. Prioritize

One table: issue, lens, task and step, heuristics, evidence, **severity** (1 cosmetic, 2 minor, 3 major, 4 blocker), Impact, Confidence, Ease (1-10 each), ICE, type, observed/hypothesis.

- Severity says how bad it is for the person; ICE decides the order of work. Keep them consistent (a blocker has impact 7+).
- Type = **fix** (`opt`, change what is there) or **rethink** (`ex`, a different solution that needs a prototype and a test first). A healthy plan is mostly fixes.
- Label each issue **observed** (seen on the product or in data) or **hypothesis** (an effect not seen yet). Hypotheses keep confidence at 7 or below.
- Every issue gets a **proposed change** (the new experience, not just "fix it"), 2-5 concrete steps naming the real pages and controls, a metric, effort, risk, and a **usability check**: the task to give a real user and what success looks like.
- For the top 3, compare at least 2 alternatives, write the experiment with its risk type (value, usability, viability, feasibility) and a success threshold, and run a short pre-mortem ("it is 3 months later and this failed - why?"). When the fix is wording, give 2 copy variants with a reason each.
- Write the **5-task usability-test plan**: who to recruit (the persona), how many, the format, and five tasks written as goals in the user's words (never "click X"), each with a start point, success criteria, what to watch and what to ask afterwards; plus what to measure and what to do with the results.

## 5. Output: report, hands-off file, test plan

Read `references/report-spec.md`. Write the review as one `audit.json` that follows `references/audit.schema.json` (start from `assets/example-audit.en.json`). You write data only; the template draws every chart, table and label and computes ICE, the UX index, quick wins, heuristic counts and confidence.

- **With a shell:** `python scripts/build_report.py audit.json report.html`. It runs `validate_audit.py` first and refuses to build on errors (an issue without evidence, proposed change or usability check, a high-friction step without a note, a test plan without 5 tasks, a KPI number with no source, a top-3 fix without alternatives or pre-mortem). Fix the data, not the template.
- **Hands-off:** `python scripts/build_handoff.py audit.json handoff.md --json tasks.json`. Context, persona, sources, rules for the implementer, then every issue as a task in priority order (dependencies first) with the user task and step, heuristics broken, evidence, proposed change, steps, acceptance criteria, the usability-test script, risks; then the 5-task test plan. Add `accept`, `depends` (handoff ids `UX01`...) and top-level `rules` when the defaults are not specific enough. Deliver it as a file next to the report, and say in one line what it is for.
- **Without a shell** (Claude app without code execution): copy `assets/report-template.html`, set `<html lang>` and `<title>`, replace the content of its `<script type="application/json" id="audit">` block with your JSON (write `<\/` instead of `</` inside strings), check the rules from `validate_audit.py` yourself, and write the hands-off file by hand in the same structure as `assets/example-handoff.en.md`.

Interface labels come from the template's `UI` and `HEUR` dictionaries chosen by `<html lang>` (`uk`, `en`; add an entry with the same keys for another language). Save `audit.json` next to the report: the next run compares against it.

Deliver one self-contained HTML page: publish it as an artifact when an artifact tool exists (private unless the person asks otherwise), otherwise send the .html file. In chat, reply with 3-5 summary bullets, the link or file, and one line on what was checked and what was not.

## 6. Check before delivering

1. **Facts.** Every quote, count and number in `tasks`, `detail` and `kpis` must trace to the walk, a source in `sources` or the owner's answers. In Claude Code, give this check to a separate subagent that has not seen your reasoning: pass it `audit.json` and the raw notes or page text and ask it to list every claim it cannot trace. Elsewhere, do the pass yourself, claim by claim. Fix or remove what does not trace.
2. **Script.** `node --check` on the template's main script if you edited anything beyond the JSON.
3. **Render**, when Python and a Chromium-based browser are available (`pip install playwright`, `playwright install chromium`, or `--browser /path/to/chrome`): `python scripts/check_report.py report.html --out ./report-check`. It opens desktop (1280px), tablet (820px, touch) and phone (390px, touch) and fails on page errors, sideways scroll, an empty task strip, radar or matrix, overlapping or overflowing labels, a heuristics list without 10 rows, a test plan without 5 tasks, tooltips that do not open on hover or tap, table cells not wrapped in one `.cv`, filters that break the table. It saves screenshots, including dark mode.
4. **Look at the screenshots**: the task strip, the walkthrough tables on a phone, the plan, dark-theme contrast.
5. **Fix and re-check**, at most twice. If something still fails, say what in one line.
6. **No headless browser:** open the published page with any browser tool at desktop and narrow width and check by looking; otherwise say plainly which visual checks were not done.

## Rules
- Every issue points to a page and step you saw, or is clearly marked as a hypothesis.
- Never submit real forms, payments or messages; never log in to someone's account; reject non-essential cookies.
- Judge the domain the person named; a page found on another subdomain is a note, not the product.
- Never invent numbers, quotes, testimonials, response times or prices, in findings or in suggested copy. Unknown metrics show "no data" (`v: null` in a KPI).
- Do not recommend dark patterns (fake urgency, confirmshaming, pre-ticked consent, hidden costs) even if they would raise conversion.
- Prefer fewer, sharper issues over long lists; merge duplicates that share a cause.
- Usability-test tasks describe goals, not clicks, and never lead the participant to the answer.
- Lens scores are judgments: base each on findings and keep the scale consistent (below 40 = people struggle, 40-60 = friction, above 60 = solid).
