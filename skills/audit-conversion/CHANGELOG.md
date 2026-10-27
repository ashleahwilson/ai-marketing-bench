# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-24)
- The earlier `dim-conversion.json` is backed up to `audits/<domain>/history/` instead of `dim-conversion.before.json`, so marketing-audit's scorer can't pick up the old score. Integration change, not re-run.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 61/61). Fixes for problems the grader saw outside the expectations:
- Evidence lines quote the page, never inspection output or scoring-rule wording.
- Self-check: page-wide statements list the pages they hold for; no pronouns the pages don't state; no test that contradicts the plan.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 60/61, Opus 60/61; no skill 35 and 38; page-cro 31):
- Never names a skill, script or procedure in the reply, even when the environment asks for skills to be announced (4 replies did).
- Guided mode names each page's primary action separately, and doesn't assume an unsupplied page exists.
- A sound page's limit of three optional suggestions includes the plan.
- A named quote already live beside a form with unconfirmed permission is a 48-hour action.
- Self-check: verify "on every page" claims page by page; describe missing facts in plain words, not file names.
- Report drops the "same checks as the marketing audit" line; US spelling check adds "labelled", "modelling".

## 1.0.0 (2026-10-24)
- First release:
  - Page-by-page conversion audit: primary action per page, competing actions, CTA wording and placement, forms field by field (required vs optional, labels, input types, autofill, error handling, submit text, privacy notice, what happens next), pricing clarity, broken promises across pages, proof near the ask with naming permission, mobile basics and speed signals visible in the HTML.
  - Scores the full marketing audit's six conversion checks unchanged (no founder-led relief) and writes `dim-conversion.json` in its format; keeps an earlier file as `dim-conversion.before.json` and lists every changed check.
  - `conversion.md` with fixed sections: verdict, top three, page by page, forms, funnel, what's working, a 48-hour / 2-week / 3-month plan, a test backlog (hypothesis, change, metric), what wasn't observable, and the checklist score last.
  - Draft and Guided modes.
  - `inspect_conversion.py` (page and form facts, cross-page conflicts), `funnel.py` (drop-off by step and segment from an analytics export, tracking and sample-size flags), `check_report.py` (format, score arithmetic, no predicted lifts, no unobserved conversion rates, client spelling, no internals).
