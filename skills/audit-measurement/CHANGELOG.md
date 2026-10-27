# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 55/56): in Guided mode Haiku said consent "needs review" without saying how tags should wait; plan rows named pages that don't exist (a /thanks page on a site that sends users to its dashboard) and a made-up campaign value.
- Guided mode includes the consent recommendation when the audience needs it.
- Plan rows use only pages, URLs and values from the files; anything new is marked "(new page)".

## 1.1.0 (2026-10-24)
Round 1 (Haiku 54/56, Opus 56/56): Haiku's yes/no answer ran 307 words, a "behaviour" slipped into a US-spelling dimension file, a reply used checklist codes and described the skill's own procedure, and one report pointed to "the ID on line 8" instead of the ID.
- Answer mode is under 200 words, checked with `check_report.py --max-words`.
- The self-check runs on every written file, JSON and the reply included, with the spelling taken from brand memory or the company's site.
- Replies name checks in plain words, never describe the procedure, and always give the real tag ID.

## 1.0.0 (2026-10-24)
- First release:
  - Modes: Draft (full deep dive), Answer (a number or a yes/no, no files), Guided (stops before deciding the conversion), Plan (tracking plan).
  - The marketing audit's measurement checklist (M1-M5), same points and rules, with deeper readings: a conversion must fire on the outcome, a banner that doesn't hold tags isn't a consent mechanism, suspected duplicates aren't deducted without the container.
  - `inspect_tracking.py`: tags and IDs per page, loaded versus configured, duplicate config calls, consent banner and consent mode signals, tags before consent, events with parameters and triggers, forms and personal fields, internal UTMs; Tag Manager container exports (no-trigger and paused tags, duplicate pageviews, conversions on broad triggers, personal data, unused triggers and variables, consent settings); analytics CSV exports (automatic events as key events, zero-count key events, internal-looking sources).
  - `score_measurement.py`: validates and sums M1-M5, sets confidence, compares with an earlier dimension file, and recomputes the Marketing Health total and grade.
  - `check_report.py`: section order, checklist sum, personal data in the plan, legal conclusions, internals, untraced counts, spelling convention.
  - Writes `measurement.md`, `tracking-plan.md` and `dim-measurement.json` (the full audit's format), backing up an earlier dimension file to `history/`.
