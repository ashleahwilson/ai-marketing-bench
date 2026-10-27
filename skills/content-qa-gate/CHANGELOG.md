# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-23)
- Fix: multi-word brand-rule and never-use phrases ("3 days, not 3 weeks", "actionable insights") never matched in `qa_check.py`; single words did. Found by the content-brief builder.

## 1.2.0 (2026-10-11)
Round 2 (Haiku 46 and 47/53, Opus 53/53): Haiku answered "fix whatever you can" with a report only, and suggested alt text and descriptions that guessed at content.
- A fix request requires the fixed copy.
- Suggested titles, descriptions and headings use only the page's own words; alt text is requested, never guessed.

## 1.1.0 (2026-10-11)
Fixes from round 1 (Haiku 42/53, Opus 52/53):
- The checker shows the brand-memory line behind each figure, so a price from the wrong plan is visible ($299 is the group rate).
- Quotes are checked for naming permission; an unconfirmed or unrecorded quote is a blocker.
- The brief's and brand's domains count as the real site (Haiku flagged reserved `.example` test domains as broken).
- Under time pressure: under 200 words, fastest path first, no softened superlatives as fixes.
- Fix mode: no guessed alt text; the copy must link the brief's CTA with no dead links.

## 1.0.0 (2026-10-11)
- First release:
  - Verdicts: Publish, Fix first, Hold, with every problem located and given a concrete fix.
  - Judgment checks for brief fit, claims (sourcing, right-for-this-reader prices, quote wording and naming permission, third-party statistics, superlatives, roadmap claims), compliance and brand rules, voice (skipped when brand-voice-gate already ran), and the reader's path.
  - `qa_check.py`: placeholders, dead and `#` links, the brief's CTA URL, affiliate links without disclosure, brand-rule phrases, H1 and heading order, title and description length, alt text, vague link text, repeated words, length and keyword against the brief, dates before publishing, never-use words, and every figure, superlative and quote listed for review.
  - Writes `<name>-qa.md`; on request, applies fixes that need no new facts to `<name>-qa-fixed.<ext>`.
  - A brief format (`references/brief-format.md`) for the content-brief skill to write.
