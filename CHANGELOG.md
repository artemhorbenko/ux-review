# Changelog

## 1.0.0 - 2026-11-24

First public release.

- 10 UX lenses in 5 groups: Nielsen's 10 heuristics, key task walkthroughs (cognitive walkthrough: know / see / recover), information architecture and navigation, content and microcopy, forms and friction, error and empty states, trust and reassurance, decision support, accessibility basics, mobile ergonomics.
- Process: data-source check (ok / demo / no), up to 4 skippable start questions, live walk of every task at desktop and phone width with a keyboard pass, issues labelled observed or hypothesis, Nielsen severity (1-4) and ICE, top 3 with alternatives, threshold and pre-mortem.
- Report template (same look as product-lens-audit): tasks as rows of steps coloured by friction, lens radar, walkthrough tables, heuristics breakdown, impact-effort matrix, issues table with severity filter, full plan with proposed change and a usability check per issue, 5-task usability-test plan, data and confidence. Tooltips for every term, stacked tables on phones, dark theme, English and Ukrainian labels, "no data" for unknown numbers.
- `scripts/validate_audit.py`, `build_report.py`, `build_handoff.py` (handoff.md + tasks.json with task/step, heuristics, proposed change and test script), `check_report.py` (desktop, tablet, phone).
- Example: fictional "Parcelly" (`assets/example-audit.en.json`, `assets/example-handoff.en.md`).
- Tested on a real B2B SaaS marketing site (public pages, 5 buyer tasks); see `evals/results.md`.
