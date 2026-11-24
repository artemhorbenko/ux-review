Start every session by reading this file and STATUS.md, then continue from Next. End every session by updating STATUS.md and committing.

# ux-review — notes for Claude and contributors

A public Claude skill (Claude Code plugin + Claude app skill ZIP) that reviews the UX of one digital product: it walks the key user tasks step by step (cognitive walkthrough), applies 10 UX lenses and Nielsen's 10 heuristics, and outputs from one `audit.json` a visual HTML report for people, a Markdown hands-off brief for AI agents (`handoff.md` + `tasks.json`) and a 5-task usability-test plan. Visual polish belongs to `ui-review`, strategy to `product-lens-audit`, competitors to `competitor-teardown`.

## Layout

```
.claude-plugin/marketplace.json        this repo is a plugin marketplace
plugins/ux-review/                     the only folder that ships to users
  .claude-plugin/plugin.json
  skills/ux-review/
    SKILL.md                           the process Claude follows
    references/                        lenses, data sources, report spec, audit.schema.json
    assets/                            report-template.html, example audit, example hands-off
    scripts/                           validate_audit, build_report, build_handoff, check_report
evals/                                 scenarios, trigger prompts, results log (anonymised)
docs/                                  README screenshots
ux-review-skill.zip                    Claude app upload, rebuilt on every skill change
CLAUDE.md, STATUS.md, CHANGELOG.md     repo docs; never move them into plugins/
```

## Rules

- Respond to the maintainer in Ukrainian; code, docs and commits in English.
- Never invent numbers. Missing data shows as "no data" (`v: null`, `f: null`) and lowers confidence.
- Audit only the production domain the user names. Subdomains (`get.`, `go.`, `lp.`, `staging.`) are often old A/B tests or staging copies: note them, do not review them. Prove a page is missing with menus, the sitemap and same-origin requests, never from a `no-cors` response.
- One product per review. Never open or quote competitors' or review sites; a "compare with X" task becomes "find why to choose this product": is there a comparison or "why us" page, and can the navigation reach it?
- Real audits stay private (artifacts or local files). Nothing in this repo may name a real audited site, client data or private links; log runs in `evals/results.md` anonymised.
- Public demos use fictional products only (current: "Parcelly").
- Claude writes only `audit.json`; the template and scripts render everything. When layout breaks, change the template, not the data.
- Keep `SKILL.md` short; details go to `references/`.
- Use data sources read-only. Never submit real forms, payments, messages or sign-ups; stop before the final button and mark that step "not tested". Reject non-essential cookies.

## Build and check

```
S=plugins/ux-review/skills/ux-review
python $S/scripts/validate_audit.py audit.json
python $S/scripts/build_report.py audit.json report.html
python $S/scripts/build_handoff.py audit.json handoff.md --json tasks.json
python $S/scripts/check_report.py report.html --out ./report-check   # needs playwright + Chromium, or --browser /path/to/chrome
```

Before committing a template or script change, run all four on `assets/example-audit.en.json`, regenerate `assets/example-handoff.en.md`, re-embed the example JSON in `assets/report-template.html` if the example changed, and check that a deliberately broken input fails validation.

## Release

1. Bump the version in `.claude-plugin/marketplace.json` and `plugins/ux-review/.claude-plugin/plugin.json`.
2. Add a section to `CHANGELOG.md` (user-facing changes only).
3. Rebuild the ZIP: `rm -f ux-review-skill.zip && cd plugins/ux-review/skills && zip -qr ../../../ux-review-skill.zip ux-review -x '*__pycache__*'`
4. `claude plugin validate .`
5. Commit and push. Tags and GitHub releases are created by the maintainer.

## Related repos

All under github.com/artemhorbenko, same report core and design: `product-lens-audit` (strategy; the shared core changes land there first, then are copied), `seo-audit`, `qa-audit`, `ui-review` (visual polish), `competitor-teardown` (competitor comparisons).
