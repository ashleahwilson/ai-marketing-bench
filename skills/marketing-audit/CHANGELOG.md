# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-24)
- `score.py` reads only the five canonical `dim-<dimension>.json` files, so backups written by the audit deep dives (or anything else matching `dim-*.json`) can't replace a current score. Previous-version files belong in `audits/<domain>/history/`.

## 1.2.0 (2026-10-10)
- Repeat audits disagreed on P4, A5, C3, C4, C5 and M4. Each now has a concrete test, and each issue is scored in exactly one check (no double-counting a banner under both positioning and brand).
- Tie-break: when torn between two levels, award the lower one.
- No form at all scores half on C3; C2 already counts the gap.
- Maturity relief (†) applies to founder-led companies only, stated explicitly.
- B5 when the brand/ folder is the auditor's: same fallback as no brand memory.
- Report length: trim the per-dimension findings first.

## 1.1.0 (2026-10-10)
- Scoring is checklist-based. Each dimension is the sum of fixed checks with full/partial/zero points and one line of evidence each, and score.py recomputes the score from the checks. This reduces variance between runs on the same site.
- New checks: mobile viewport, privacy notice near forms, navigation on every page, consistent CTA wording, currency on pricing, analytics configured (not just loaded).
- Grade actions name the two weakest dimensions and no longer say "stop spending".
- Confidence is capped by the number of pages reviewed (`--pages`).
- Offer-map next steps go only in consultant-notes.md, never in the shareable report.
- Clarified whose brand memory a brand/ folder is.
- inspect_page.py flags non-HTML input, GA4 loaded without configuration, missing navigation, and CTA labels across pages.
- The triage grade has a rough-scoring method.

## 1.0.0 (2026-10-10)
- First release:
  - Triage and full modes.
  - Sequential discovery with two classifications (6 business types, 4 maturity stages).
  - Five dimension rubrics with maturity calibration (positioning 25, acquisition 20, conversion 20, brand 15, measurement 20).
  - `inspect_page.py` (tracking, forms, CTAs, headings, structured data, missing alt text) and `score.py` (weighted total, grade bands that name actions, neutral 50 for unassessed dimensions, confidence, optional offer map).
  - MARKETING-HEALTH.md, a one-pager, and a three-horizon plan.
  - Reads brand memory when auditing your own company.
