# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Round 2 (Haiku 69/69). The grader's remaining notes: replies of 570 to 760 words, absolute paths in replies, a price without its billing conditions, third-party logos in a brief, a broadened fact ("your POS"), and "no brand memory" said only in the build file.
- Full copy pasted only for 3 ads or fewer; relative file paths only.
- Judgment checks for price conditions, third-party logos and broadened facts.
- With no brand memory, the reply itself says the build is provisional.

## 1.1.0 (2026-10-23)
Round 1 (Haiku and Opus each 68/69; no skill 46 and 50, ad-creative 50): Haiku's month-end build had no vertical asset and its replies mentioned the check results; Opus wrote a creator who'd "spent a week" with the product and one unsourced differentiator. Runners reported checker false positives.
- Every concept needs a 9:16 version and a feed version.
- Creators and actors never claim experience with the product unless it's on record; paid partnerships disclosed.
- Judgment check for unsourced features and differentiators.
- Replies never mention the check or its results; the 400-word limit excludes tables and pasted ads.
- Missing brand files mean nothing on record; provisional brand memory gives a `draft` build with provisional facts flagged.
- Checker: production specs in creative briefs (seconds, safe-zone percentages) no longer count as claims, only overlay text and prices do; quotes are checked in primary text, headline and description, not video scripts; "$58K" matches "$58,000".

## 1.0.0 (2026-10-23)
- First release:
  - Modes: Draft, Guided (recommendation plus at most five questions, no copy), Rebuild (from `audits/meta-ads/<account>/fixes.md`, every fix mapped), and Check and fix (drafts fixed in a copy).
  - Campaign decisions: objective and a tested optimization event, one campaign and as few ad sets as the budget can feed (learning-phase reasoning, no invented costs), broad or Advantage+ audiences first, consented custom audiences and lookalikes only, Advantage+ placements with feed and vertical assets.
  - Creative: three to five distinct concepts with hook, primary text (hook and offer in the first 125 characters), headline (40 or fewer), description (30 or fewer), a Meta CTA button and an image or video brief.
  - Compliance built in: personal attributes, special ad categories and their targeting limits, audience consent, proof and UGC rules, policy-risk wording.
  - `check_build.py`: lengths, front-loading, CTA buttons, personal-attribute phrasing, policy-risk words, never-use words, brand-rule phrases, unconfirmed names, quotes on record, figures traced to brand memory, special-category targeting, audience consent; exports `ads.csv`.
