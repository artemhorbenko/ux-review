# Status

Living state of the work. Update at the end of every session. Public repo: no real site names, client data or private links here.

**Version:** 1.2.0 (2026-11-24)

## Done recently

- 1.0.0: 10 UX lenses, cognitive walkthrough of key tasks, Nielsen heuristics and severity, ICE; report template with tasks as rows of steps coloured by friction; 5-task usability-test plan; hands-off file (`handoff.md` + `tasks.json`) with task/step, heuristics, proposed change and a usability check per issue; `check_report.py` for desktop, tablet and phone.
- 1.0.1: review only the named production domain; prove missing pages with menus, sitemap and same-origin requests.
- 1.1.0–1.2.0: one product per review; a competitor task is reframed as "find why to choose this product" (comparison or "why us" page reachable from the navigation).
- Public demo with the fictional product "Parcelly".
- First real run: B2B SaaS marketing site, public pages, buyer persona, 5 tasks (logged anonymised in `evals/results.md`).

## In progress

- Nothing open in this repo.

## Next

1. Maintainer: create git tags v1.0.0–v1.2.0 and a GitHub Release (the session cannot push tags).
2. Maintainer: share the public demo artifact publicly (it is published but private until shared).
3. Test the install in Claude Code desktop and in the Claude app (upload the ZIP).
4. Run trigger evals from `evals/trigger-evals.json` with the skill-creator skill; tune the description.
5. Add a Ukrainian demo (`example-audit.json` with `lang: uk`) and a screenshots-only scenario run.
6. Run a real phone check (touch, real viewport) instead of a 390px frame; add an accessibility scanner run when the shell can reach the site.

## Open questions

- Should the report also render a funnel when analytics are connected, next to the task strip?
- Move the shared report core into its own repo once the sibling skills stabilise?

## Links

- Public demo (EN): https://claude.ai/artifact/XFAybtaGhMsL5E9EEuadcA
