# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 63/64): a second dataset sending Lead got a hedged "remove it if redundant"; replies named the mode, workflow steps and working files; one reply said ad sets were "in learning" without a learning column.
- A second dataset sending the same event: recommend removing it, keeping the one the ad sets optimize on.
- "Below Meta's learning guideline", never "in learning" unless the export says so.
- Replies don't name modes, steps, working files or audit-rule names, and agree with AUDIT.md and fixes.md.
- The deduplicated event total is labelled an estimate.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 62/64, Opus 62/64): fixes.md was sorted by horizon instead of priority; tracking fixes named an event instead of a target; on a clean account Opus recommended four changes; a tracking blocker still scored 84 (Sound); replies mentioned fix IDs and point weights.
- fixes.md: sorted by priority, then horizon; Target is an exact export name or `account`.
- A sound account gets at most three changes across the whole audit.
- Any blocker caps the score at 69 (Needs work).
- Replies never mention fix IDs, check counts or point weights.

## 1.0.0 (2026-10-24)
- First release:
  - Ten checks: objective against goal, conversion events (wrong optimized event, dead events, browser and server duplicates, stray datasets), attribution, structure and learning against Meta's published guideline of about 50 optimization events per ad set per week, audience overlap, frequency and fatigue from the account's own trend, creative volume and variety, placements, Advantage+ use, and special ad categories as a compliance blocker.
  - Modes: Draft (full audit), Guided (pauses after loading with at most three questions), Export guide (no exports: what to export and how, no findings).
  - `meta_audit.py`: `analyze` computes every figure from Ads Manager and Events Manager CSVs; `score` turns check statuses into the 0-100 score; `verify` lists any figure in the report that doesn't trace to a computed number.
  - Writes `audits/meta-ads/<account>/AUDIT.md` and `fixes.md` (Account facts plus F-lines) for the meta-ads-build skill.
