# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-24)
Round 3 (Haiku 80/83, Opus 82/83) found three gaps; these text-only fixes were not re-run (the round limit was reached):
- A segment's price names the segment in the same headline ("Groups: From $299/Location"); both models ran a standalone "From $299/Location/Month" headline.
- No implied channel or step the offer doesn't have ("Talk to a Bookkeeper").
- Without brand memory the reply itself offers to set it up (Haiku said provisional in the plan only).

## 1.2.0 (2026-10-24)
Round 2 (Haiku 82/83, Opus 82/83): Haiku dropped the confirmed 15-minute refresh because the check treated any rules line containing "never" as banning its numbers; one reply didn't say why competitor names stay out of ads; Opus built the competitor campaign as its own recommendation.
- Fix: a number is blocked by a rule only when the rule bans that claim, or every source for it is unsubstantiated; a confirmed source clears it.
- The competitor reason is one sentence (restriction or trademark complaint), and a competitor campaign is offered as the user's call.
- Numbers are matched with their unit ("3 days", "$299 per location"), so a common digit elsewhere in brand memory no longer clears an unsupported claim, and a price missing its unit is caught.
- Price qualifiers ("from", "per location") travel with the number; no invented frequency or scope.
- "Not offered" negatives only from brand memory; others labelled as assumptions.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 79/83, Opus 82/83): Haiku kept two countries and a QuickBooks campaign on a $300/month budget, and kept a bare "bookkeeping" keyword; Opus's guided reply ran to 347 words; one guided reply named the skill.
- A concrete small-budget setup (under about $20/day): one campaign, one or two ad groups, one country, no brand or competitor campaign, led by the recommendation.
- Every non-brand keyword names the audience or category.
- Guided turns under 250 words, counted.
- Never name the skill, its scripts or spec file to the user, or cite internal guidelines.
- A confirmed fact runs in the form a rule allows (Haiku held back the confirmed 15-minute refresh).
- Fix: a shared negative list applied to "non-brand" wrote a stray campaign row named "non-brand" in the Editor CSV; it now lists the real campaign names.
- Without brand memory, spelling follows the market or the user.

## 1.0.0 (2026-10-23)
- First release:
  - Builds a Google Ads search campaign, or rebuilds one from a Google Ads audit's fixes list: brand split from non-brand, ad groups by intent theme with a landing page each, phrase and exact keywords, shared negatives, RSAs, sitelinks, callouts, structured snippets, settings, a budget split framed as a test, and a conversion-tracking checklist.
  - Draft and Guided modes.
  - Never states volumes, CPCs or forecasts without the user's data; holds back superlatives, unproven results, banned claims and competitor names in ad text, with the reason and what would unlock each.
  - `build_ads.py`: character limits, duplicate headlines, pins, policy-risk words, competitor and never-use words, numbers traced to brand memory and the user's facts, keyword data checked against a Keyword Planner export, negatives that block keywords, settings and budget totals; writes a Google Ads Editor import CSV, everything Paused.
  - Reads `audits/google-ads/<account>/fixes.md`; writes `ads/google/<campaign>/` (plan.md, campaign.json, editor-import.csv).
