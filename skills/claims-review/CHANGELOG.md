# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables; caution note added to the header. Integration change, not re-run.

## 1.2.1 (2026-10-27)
Round 3 (Haiku 82/83, Opus 82/83): Opus rewrote "Cancel anytime" as "Cancel before day 15 and you won't be charged", a term brand memory doesn't record.
- Rewrites of terms state only recorded terms; otherwise Cut and ask. Not re-run after this change.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 82/83): mixed messages about whether legal review was needed, no pointer to the saved review, the review pasted twice, unlisted features cut instead of queried, a correct price filed as Restricted, and one mention of the skill's own reference.
- One fixed sentence for Hold for legal review, and the reply ends with where the full review is saved.
- Unlisted feature descriptions are "confirm before launch"; only the problem claim goes into claims.md.
- No mention of reference files.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 76/83, Opus 82/83; no skill 60 and 69): Haiku named only Canadian rules for a Canada-and-US brand, sent brand-rule breaches to legal, and over-flagged a clean email (currency, re-confirming brand facts, conditions on a free offer with none recorded).
- Two markets in brand memory: every legal-review line names a rule for each.
- Brand-rule breaches stay off the legal list.
- A sharper "don't invent problems" rule: confirmed facts as recorded, the brand's description of its own service, unconditional "free" offers and endorsers' personal taste aren't issues.
- No market recorded: name Canada and US rules side by side instead of assuming one. No brand memory: whole review provisional, no references to missing files, explicit offer to set one up.
- Long reviews: one line per claim in the reply, full detail in the file. Rewrites carry no placeholders and quote facts exactly as recorded.
- Replacing a `TBD:` placeholder line in claims.md when adding the first real entry.

## 1.0.0 (2026-10-24)
- First release:
  - Extracts every claim in a piece (performance, comparative, superlative, free and pricing, guarantees, testimonials and endorsements, ratings, environmental, health, financial, AI and capability, certification), rates its risk, and checks it against brand memory (claims, proof, offer, rules).
  - For each claim: evidence needed, missing qualifier or disclosure, and a rewrite from supported facts only (or Cut).
  - Names Canadian (Competition Act, Canadian Code of Advertising Standards) and US (FTC Act and guides) rules for the markets in brand memory; high-risk claims go to a legal review list. Never signs off.
  - Recommendation: Clear to use, Revise first, Hold for legal review.
  - Draft and Guided modes.
  - `claims_scan.py`: candidate claims with tags, closest brand-memory line and status, banned phrases, missing paid-endorser disclosure, market hints.
  - Writes `claims/<name>-claims-review.md`; proposes `brand/claims.md` additions in brand-memory format and applies them only on request, never into Approved without evidence.
