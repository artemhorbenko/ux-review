# Changelog

## 1.1.0 - 2026-11-24

- One product per review: no competitors' sites, review sites or comparisons with other products; a competitor task is dropped with a note and replaced with a task on the product itself.
- Decision support now covers the product's own plans, setup path and integrations.
- Data sources: "Search results and third-party pages" replaced with "Outside the product: not used".
- Evals: "competitor-task" scenario; "subdomain-trap" no longer involves a competitor.

## 1.0.1 - 2026-11-24

- Stay on the domain the person named: subdomains such as `get.` or `staging.` are noted, not reviewed as the product.
- Before reporting a missing page, check menus, the sitemap and likely URLs with a same-origin request; a `no-cors` response (status 0) is not evidence.
- Eval: "subdomain-trap" scenario.

## 1.0.0 - 2026-11-24

First public release.

- 10 UX lenses in 5 groups: Nielsen's 10 heuristics, key task walkthroughs (cognitive walkthrough: know / see / recover), information architecture and navigation, content and microcopy, forms and friction, error and empty states, trust and reassurance, decision support, accessibility basics, mobile ergonomics.
- Process: data-source check (ok / demo / no), up to 4 skippable start questions, live walk of every task at desktop and phone width with a keyboard pass, issues labelled observed or hypothesis, Nielsen severity (1-4) and ICE, top 3 with alternatives, threshold and pre-mortem.
- Report template (same look as product-lens-audit): tasks as rows of steps coloured by friction, lens radar, walkthrough tables, heuristics breakdown, impact-effort matrix, issues table with severity filter, full plan with proposed change and a usability check per issue, 5-task usability-test plan, data and confidence. Tooltips for every term, stacked tables on phones, dark theme, English and Ukrainian labels, "no data" for unknown numbers.
- `scripts/validate_audit.py`, `build_report.py`, `build_handoff.py` (handoff.md + tasks.json with task/step, heuristics, proposed change and test script), `check_report.py` (desktop, tablet, phone).
- Example: fictional "Parcelly" (`assets/example-audit.en.json`, `assets/example-handoff.en.md`).
- Tested on a real B2B SaaS marketing site (public pages, 5 buyer tasks); see `evals/results.md`.
