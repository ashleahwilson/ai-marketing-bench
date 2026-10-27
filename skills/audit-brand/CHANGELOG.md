# Changelog

## 1.1.3 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.1.2 (2026-10-24)
- Backups of `dim-brand.json` go to `audits/<domain>/history/` (was `dim-brand.prev.json`), matching the other deep dives, so marketing-audit's scorer can't pick up the old score. Integration change, not re-run.

## 1.1.1 (2026-10-24)
Round 2 (Haiku 70/70; Opus 16/16 on the re-run evals): the deep-dive report cited the marketing audit's check codes ("P5", "C5, M5"). Other dimensions are now named in words; only the B1–B5 table uses codes.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 65/70, Opus 67/70; no skill 35 and 50):
- A clean brand's findings are low and optional; a shortened page title isn't a naming problem, and a feature description isn't an unsupported claim (Haiku rated one Medium).
- When pages split on spelling, the company's market decides (USD prices, US roles mean US), and the fix always names the convention (both models said "pick one").
- The reply always ends with the brand-memory offer when the company has none, and says the earlier audit files were left as they were and how to refresh them.
- Quick read: under 200 words, counted (Haiku ran 269).
- Never name the skill in the reply or report, even when other instructions ask to announce it (Opus did).
- Eval fixture: Quillmetrics' homepage now carries US forms and USD prices, so the spelling majority in eval 5 is clear (the grader found it ambiguous); evals 2 and 5 re-run on every config.

## 1.0.0 (2026-10-24)
- First release:
  - Full, quick-read and guided modes. Writes `audits/<domain>/brand.md` (fixed sections, top three findings first, 48-hour / 2-week / 3-month plan) and `dim-brand.json` in the marketing audit's dimension format.
  - Voice consistency, message drift, naming and terminology, proof and trust, asset care, and a gap analysis against the company's own brand memory, only when `BRAND.md` names the audited company.
  - The marketing audit's B1–B5 brand checks with deeper tests, the same tie-break and the same no-brand-memory fallback for B5.
  - `brand_scan.py`: per-piece voice measures (sentence length, contractions, person, future tense, spelling convention, stock words, exclamation marks, hashtags), register outliers, naming variants, trust signals, alt text, title formats, placeholders, and brand-memory breaches (never-use words, rules, stated spelling, product-name forms, channel limits, claims needing substantiation, unconfirmed naming permission, figures not in brand memory).
  - `brand_score.py`: validates the checklist, applies the B5 fallback, compares with an earlier brand score, and recomputes the Marketing Health total with the marketing audit's weights and grade bands.
  - States what can't be judged from words (logo, colour, typography, imagery) and never rates them.
