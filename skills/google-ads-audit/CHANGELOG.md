# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-24)
Round 3 (Haiku 64/64, Opus 63/64). Opus said Search Partners spend was "already inside" the waste total and stated a cause the data didn't show; the 1.1.0 wording on overlap invited the first.
- Overlap wording corrected: the figures may overlap, by an unknown amount; never add them or say one contains the other.
- Self-check: no causes stated that the data doesn't show. Text-only change, not re-tested.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 63/64): Haiku didn't give the Quality Score of the low-scoring keywords; working files sat beside the client files; the self-check contradicted the report template on export file names; borderline calls varied between runs on the same data.
- Working files (search-term judgments, computed figures) go in a `working/` subfolder.
- Every keyword at Quality Score 4 or below is named with its score.
- Export file names are allowed under Sources only.
- A zero-conversion term close to something the offer mentions is borderline, not waste.
- A Low-confidence score is labelled provisional in the verdict line and reply.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 61/64, Opus 64/64): Haiku compared a budget-limited campaign with the blended account CPA and said hold the budget; gave a Google Ads location for only one report when there was no data; didn't explain that "junk keywords" are search terms to negate; dropped converting borderline terms from the guided checkpoint; left script and file names and `TBD` values in client files.
- Budget-limited campaigns are compared with non-brand cost per conversion elsewhere, not the blended figure.
- The no-data reply includes where to find every report.
- "Pause the junk keywords" gets the search-terms-versus-keywords explanation; read-only is stated as how the audit works.
- Borderline terms include converting terms outside the offer; brand misspellings only from the data; overlapping figures never added.
- `check_audit.py` fails internal names in client files and `TBD` inside fix lines.

## 1.0.0 (2026-10-23)
- First release:
  - 11 checks from Google Ads CSV exports: conversion tracking, wasted spend and negatives, match types, budget limits, bid strategy against volume, Quality Score, responsive search ad coverage, location targeting, network settings, brand and non-brand split, landing page match. Plus brand rules in live ads.
  - `ads_audit.py`: recognizes reports by their columns, reads the date range, skips total rows, computes every dollar figure, the confidence level and the weighted score.
  - `check_audit.py`: fails untraced dollar figures, promises or forecasts, missing sections and malformed fix lines.
  - Draft and guided modes. Read-only. Writes `AUDIT.md` and `fixes.md` (the format google-ads-build reads).
