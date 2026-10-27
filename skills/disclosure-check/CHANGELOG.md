# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 59/60): named only the first affiliate link, applied the Starter/Growth footnote terms to a trial plan with no price, held a sendable newsletter over a side question, and doubted a discount code the draft's own deal note recorded.
- Every affiliate link is listed with its marker, and non-affiliate links are named.
- Terms for one plan never carry over to another.
- Notes inside the piece count as the user's facts.
- Side questions go under Needs your input, not into a Hold verdict.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 59/60, Opus 59/60; no skill 40 and 51): both fixed copies of the holiday ad wrote trial terms nobody had confirmed ("billed automatically from day 31", "Renews automatically. Cancel anytime.").
- An offer missing from brand memory gets a marked blank or is removed in a fixed copy; no generic renewal or cancellation wording and no computed charge dates.
- Files are named relative to the project folder, never full system paths; no mention of internal re-checks.

## 1.0.0 (2026-10-24)
- First release:
  - Checks affiliate links, sponsored and creator posts, testimonials with a material connection, "from" prices and mandatory fees, auto-renewing trials, contests and giveaways, commercial email, and AI imagery where brand rules require a label.
  - Verdicts: Ready, Fix first, Hold. Every finding has exact fix text and placement; facts in fixes come only from the piece or brand memory.
  - Keeps a required disclosure when asked to drop it, and offers a lighter compliant version.
  - Names Canadian and US rules at the rule level, never as legal advice.
  - `disclosure_scan.py`: triggers, disclosure position (before the first affiliate link, the ~125-character social cut-off, trailing hashtag blocks, footnotes far from a price), contest and email elements, house wording and sender details from brand memory, testimonial relationships from `proof.md`, prices and trials against `offer.md`.
  - Writes `<name>-disclosures.md`; on request, a fixed copy `<name>-disclosed.<ext>`.
