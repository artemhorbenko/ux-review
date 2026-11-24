# Results

Scores 1-5: **E** evidence (every issue traces to a page and step), **H** honesty about missing data and untested steps, **P** fixes specific to the product, **T** usability-test plan usable as is, **R** report renders on desktop, tablet and phone.

| Date | Version | Scenario | Product | E | H | P | T | R | Time | What broke |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | 1.0.0 | public-only, persona and 5 tasks given, stop-before-submit | B2B SaaS marketing site (referral platform), English | 5 | 5 | 4 | 4 | 5 | ~60 min | Window could not be resized in the user's Chrome, so phone width was checked in a 390px same-origin frame (marked partial). The shell could not reach the site, so no accessibility scanner; keyboard walk instead. A comparison page still listed in search returned 404 - became the top issue. Report: the "stopped at submit" badge overlapped the task strip and the walkthrough title broke on phones; both fixed, and check_report now covers the task strip. |
