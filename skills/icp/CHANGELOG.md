# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
- `icp/scoring.md` now uses the line format the build-list skill parses: a short header, `| Criterion | Points | Evidence |` tables, criteria written `Field: a, b`, `Field 2–15`, `Field 15+`, `Field over 15`, `Field under 10` or `Field 1`, `DQ` for disqualifiers, and a `Tiers: A 70+, B 50+` line. Header and notes lines never end in a bare number, so the list builder can't misread them as criteria. Groups are gone: size bands simply don't overlap (`scoring.py check` fails on overlapping ranges), and Max points is the best criterion per field.
- The eval 7 fixture (an existing version 1 rubric) was converted to the new format.
- Round 3 (Haiku 64/66, Opus 66/66): added the compatibility note; small mislabelled counts and unsourced asides remain (see evals/scorecard.json).
- Round 2 (v1.1.0: Haiku 61/66, Opus 66/66): Haiku left a 0-of-4 segment able to outscore single-location clinics when there was no brand memory, didn't flag blank verticals, named no source for a churn benchmark, and didn't label small segments in Guided mode. Now: zero-win segments with 4+ losses pointing the same way are disqualifiers with or without brand memory; blank segment fields are reported; one source named per market figure asked for; Guided findings mark segments under 10 records; 10+ records is never called "too few".

## 1.1.0 (2026-10-23)
Round 1 (Haiku 64/66, Opus 65/66): both with-skill runs gave 20+ location groups negative points with no Disqualifiers section (eval 8), Haiku labelled small segments only as "hypothesis" (eval 9), and the grader found mislabelled figures (a cross-tab row quoted as a whole band), a few hand counts, and small leaks of the method.
- Figures must carry the exact row label they came from; no hand counts or summed rows (rerun the analysis instead).
- `check_icp.py` lists every "k of n" outcome count the analysis didn't print, for tracing.
- The rubric always has a `## Disqualifiers` section (`scoring.py check` fails without it); zero-win segments with four or more losses pointing the same way become disqualifiers.
- Replies say small samples in plain words, don't explain the rubric's own rules, and drop "Kept out" when nothing was left out.

## 1.0.0 (2026-10-23)
- First release:
  - Modes: Draft, Provisional (no customer data), Update, Personas, Guided.
  - `analyze_customers.py`: matches CRM columns by common names, drops open deals, duplicates and rows with no outcome, and reports win rate, churn, deal size and cycle by segment and by industry x size, with sample-size labels (anecdote under 5, hypothesis 5-9, evidence 10+; percentages only on 10+).
  - `scoring.py`: parses, checks, applies and back-tests the `icp/scoring.md` rubric (criteria, groups, points, thresholds, disqualifiers), documented in references/scoring-format.md for the list builder.
  - `check_icp.py`: fails on untraced or small-sample percentages, market-size and benchmark figures, quotes not found in a source, untagged audience bullets, evidence without counts, and internals in the reply.
  - Writes `brand/audiences.md` in the brand memory format, keeps old versions in `icp/history/`, and adds a changelog line.
