# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables. Integration change, not re-run.

## 1.2.1 (2026-10-27)
Round 3 (Haiku 69/74): two losses came from the brand-pack draft labelling unconfirmed audience lines "not yet confirmed", a status word in the agency's copy.
- `extract` now writes "(our working view)" instead. Not re-run: the bench rounds were used up, so this fix is untested.

## 1.2.0 (2026-10-27)
Round 2 (Haiku 70/74, Opus 74/74): Haiku miscounted two pipe-separated headlines as one, called items "required before signing" in an Accept, pasted the review file into the reply, left review rounds TBD, skipped the brand-memory offer with no brand memory, and copied its "Before you send" list into an agency-facing brief.
- Ad length trusts the measured lines; a proposal's date and style are never problems.
- Accept has nothing required before signing; the reply summarizes the review file.
- Review rounds are always proposed, never TBD; the brand-memory offer is the reply's last line when there is none.
- Gap lists and brand-memory notes stay in the reply, never in the brief or the pack.

## 1.1.0 (2026-10-27)
Round 1 (Haiku 71/74, Opus 74/74; no skill 51 and 61): Haiku used bullets for the send-back list, ran an Accept review to 365 words, named only "final deliverables" for a website's ownership, and listed an objective as a gap when the request named the offer. No run caught a sample ad description over Google's 90-character limit.
- The send-back list must be numbered; an Accept reply stays under 200 words, other reviews under 400.
- Ownership items are named per work type (website: domain, code, design files, content, hosting and CMS accounts).
- The objective comes from the request when it names the offer; the gap count matches the list.
- `review` measures sample ad headlines (30) and descriptions (90).

## 1.0.0 (2026-10-24)
- First release:
  - Modes: Write, Ask (budget or timeline missing), Write with gaps, Pack only, Review, Guided.
  - A fixed twelve-section brief (`briefs/agency/<project>.md`) with mandatories for voice, approved claims, claims not to use, legal, accessibility, and ownership of accounts, data and files.
  - A shareable brand pack (`<project>-brand-extract.md`) that leaves out customer lists, margins, internal prices, credentials, internal results, unannounced changes, unconfirmed proof and anything marked internal, with the user told what was left out and what to share instead.
  - Review mode: scores a proposal or first draft against the brief (deliverables, mandatories, claims, budget, timeline and terms) and lists red flags with what to ask for.
  - `agency_brief.py`: `extract` drafts the brand pack; `check` catches secrets, internal values, paths, tags, unapproved claims and missing sections; `review` maps deliverables, money, terms, red-flag and banned phrases.
