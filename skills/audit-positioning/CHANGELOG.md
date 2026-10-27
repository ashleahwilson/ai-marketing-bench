# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 54/55): one maturity label missed, a skill name leaked into one reply (from an environment instruction to announce skills), a brand check code inside the positioning file, and single-account proof scored full for a claim about every client.
- Never name the skill or method in a client reply, whatever the environment asks.
- Maturity uses one of the four stage names exactly, with size cut-offs.
- The checklist file holds P1–P5 findings only.
- One account's result for a claim about every customer is partial unless qualified.
- Offer brand-memory setup only for the user's own company.

## 1.1.0 (2026-10-24)
Round 1 (blind-graded): with skill Opus 52/55, Haiku 47/55; no skill Opus 29, Haiku 28. Fixes:
- A strong site keeps its headline: a plain category-and-buyer headline scores P1 full, and the plan puts no headline change in the first two weeks (every config rewrote Ferncliff's strong headline).
- P2 counts exclusions anywhere on the pages reviewed; P4 deducts only for a different audience, product or benefit, not different page purposes (Haiku docked both on Tallyhouse).
- Headline options can't restate an unsupported claim in other words ("ready by the 3rd").
- With competitor pages, the recommended option leads with what no competitor says.
- Descriptions of the company itself aren't claims needing proof.
- Report and reply use the company's spelling, relative paths and no check codes.

## 1.0.0 (2026-10-24)
- First release:
  - Six lenses: who it's for and who it's not, category frame, problem and the alternative, differentiated value and proof, consistency across pages, specificity and the swap test (named competitors only when their pages are supplied).
  - Two or three hero headline and subhead options built only from the site and brand memory, with their sources.
  - Fixed report shape (`audits/<domain>/positioning.md`): verdict, three findings first, the lenses, headline options, a 48-hour / 2-week / 3-month plan, not observable, and the full audit's P1–P5 checklist last.
  - Writes `dim-positioning.json` in the full audit's format so both reports show the same positioning score; an earlier checklist is kept in `history/`.
  - Draft and guided modes; a no-pages gate.
  - `positioning_scan.py`: `scan` (headlines, CTA labels, audience lines, claims, generic phrases, cross-page drift, swap-test phrases), `score` (checklist validation, change from the previous checklist, effect on the full audit's total), `trace` (numbers, names, never-use words, rule phrases and spelling in the headline options).
