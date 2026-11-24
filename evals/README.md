# Evals

- `evals.json` - end-to-end scenarios: what the run must do (`expectations`) and must not do (`forbidden`). Run each in a fresh session with the plugin installed, then grade the result against the lists.
- `trigger-evals.json` - prompts that should and should not start the skill. With the skill-creator skill installed, ask it to run trigger evals on `plugins/ux-review/skills/ux-review` with this file; it can also tune the description.
- `results.md` - one row per run.

Every report must also pass the automatic checks:

```
python plugins/ux-review/skills/ux-review/scripts/validate_audit.py audit.json
python plugins/ux-review/skills/ux-review/scripts/check_report.py report.html
```

Real sites stay private: record the scenario and the scores here, not the site's name or data.
