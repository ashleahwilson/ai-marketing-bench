# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables; caution note added to the header. Integration change, not re-run.

## 1.2.0 (2026-10-26)
Round 2 (Haiku 64/64): extra copies of the version and packet appeared in two runs (likely overlapping runs in one folder, but one packet carried a model-name suffix).
- Write exactly one new version and one packet at the consolidator's names; stop and report if an unexpected one appears.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 63/64, Opus 64/64; no skill 45/64 and 53/64):
- "Decided by" may only name a reviewer, the approvals list's decider, a brand rule, or "you": Haiku logged a decision as made by a name taken from outside the review.
- No "Using the … skill" line and no citing internal rules, even when the environment asks to announce skills (Opus leaked it twice).
- Search all of brand/ before raising something as unsupported (Opus flagged a confirmed fact).
- Check date logic before naming the faster route; for a missing permission, say how to get it and who asks.

## 1.0.0 (2026-10-24)
- First release:
  - Consolidates reviewer feedback by reviewer and location, classifies each comment (must fix, should fix, preference, question), merges duplicates and surfaces conflicts with the decider from the approval rules.
  - Applies agreed changes to `<name>-v<n>.md`, never the original; writes `<name>-review.md` with the approval state, open decisions, comments, decision log and sign-offs.
  - Defines a parseable approvals list (`## Approvals` in `brand/rules.md`, or `approvals.md`) and a reviewer feedback file format (`references/approvals-format.md`).
  - Reads `<name>-qa.md` blockers and `<name>-gated.md` text as hand-offs.
  - Draft, Guided and Status modes; an optional editor pass, always labelled and never a sign-off.
  - `review_cycle.py`: consolidate (IDs, anchors, duplicates, conflicts, figure tracing, approval state, next version name) and check (decision coverage, deciders, approval consistency, untraced figures, leftovers in the version).
