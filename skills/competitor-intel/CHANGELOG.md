# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Round 2 (Haiku 54/55, Opus 54/55): Haiku wrote an empty Price history heading with an untagged TBD line; Opus's guided plan mentioned the prospect's $249 quote without asking how to treat it.
- Guided mode turns every call that's the user's (hearsay, prospect-reported figures that differ from the page, conflicting sources) into a question.
- Price history only when there's an old price.
- The trace check covers the reply and superlatives; price comparisons must be like for like.
- The reply never names the mode or tag notation.
- Round 3 (Haiku 53/55, Opus 54/55): marked recommended for large models after small widened facts in Haiku outputs.

## 1.1.0 (2026-10-23)
Round 1 (Haiku 53/55, Opus 55/55): Haiku dropped "from" when it restated a price, and filled a no-material skeleton's strengths from win/loss reasons.
- Price conditions are repeated wherever a price appears, including the reply.
- No material: no battlecard file unless a skeleton is asked for; win/loss reasons go under When we lose only.
- Only brand/competitors.md and brand/changelog.md are written; no other brand file.
- An undated export is undated, not stale.
- A gap backed by deal notes and a review can be stated with its evidence; only the flat, unattributed claim stays out.

## 1.0.0 (2026-10-23)
- First release:
  - Builds a battlecard (`competitors/<name>-battlecard.md`, twelve fixed sections) and merges a sourced profile into `brand/competitors.md`.
  - Every competitor fact carries a source, capture date and status; prices copied with their conditions; "not shown" where sources are silent.
  - Won't profile a competitor from memory; leaves out rumours and comparison claims brand memory can't support, and says why.
  - Win/loss counting with sample-size caveats; landmines only on evidenced gaps; objection responses grounded in brand-memory proof.
  - Draft, Guided and Refresh modes; refresh keeps price history and marks unseen facts stale.
  - `check_intel.py`: sections, source tags, prices without sources, rumour terms, unsubstantiated comparisons, "No" for not-shown features, cited files, stale captures.
