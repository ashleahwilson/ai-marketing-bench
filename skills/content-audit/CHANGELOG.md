# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables. Integration change, not re-run.

## 1.2.1 (2026-10-27)
Round 3 on 1.2.0 (Haiku 63/63, Opus 62/63). Fixes for the open issues, **not yet re-tested**:
- New ground rule: with no posts or title column, describe only URLs and numbers, never what a page says or is titled (Opus described unseen titles in eval 4).
- No similarity scores in client files, and only relative file paths in replies (Haiku leaked both once).

## 1.2.0 (2026-10-27)
Round 2 (Haiku 61/63, Opus 63/63; no invented facts):
- New Gaps mode: a gaps-only request still writes AUDIT.md with the gaps, since that file is the hand-off for briefs (Haiku answered in the reply only).
- Every Guided question carries sessions and conversions for each piece it names, redirects included.
- A sitemap lastmod is never read as a publish date, and any stated ranking is computed from the export (two Opus slips).

## 1.1.0 (2026-10-26)
Round 1 (Haiku 62/63, Opus 63/63; no skill 54 and 52, copy-editing 49):
- Blanket-rule replies ("delete everything under X") stay under 250 words and list only the pieces the rule catches, plus at most two fact fixes (Haiku wrote 372 words).
- Two blog posts competing for one keyword still merge when both convert: conversions protect from removal, not from a merge (Haiku declined the merge in Guided mode).
- The draft inventory uses plain flag words, not upper-case codes, so client files carry no internal vocabulary.

## 1.0.0 (2026-10-24)
- First release:
  - Decides keep, update, merge, redirect or remove (or needs data) for every piece, with a reason and quoted evidence.
  - Finds competing pieces (same keyword, near-identical titles, text overlap to check), outdated facts against brand memory (price history, discontinued offers, held claims, withdrawn proof, dated announcements), pieces written for excluded audiences, and topic gaps against personas and offers.
  - Never estimates traffic; with no metrics it decides only what the content supports; conversions, sales-use notes and age protect a page from removal.
  - Modes: Draft, Guided (merges and removals as questions), Check (one piece), with pushback on blanket rules such as "delete everything under 100 sessions".
  - `audit_content.py`: maps any export's column names, matches posts to rows, checks every price against brand memory, finds pairs, staleness and sitemap gaps, writes a draft inventory, and checks the finished inventory and report (no invented metrics, no unsafe removals, no internals).
  - Re-audits copy the earlier files to `.prev` and report what's still open.
  - Writes `audits/content/inventory.csv` and `audits/content/AUDIT.md`; the "Topic gaps" section is the hand-off for briefs.
