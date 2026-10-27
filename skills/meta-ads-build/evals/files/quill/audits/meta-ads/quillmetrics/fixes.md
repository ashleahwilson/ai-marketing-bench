# Meta ads fixes: Quillmetrics
Source: AUDIT.md (2026-09-16 to 2026-10-15) · Status: proposed, nothing applied · Every fix needs the account owner's approval

## Account facts
- Currency: USD. Period: 2026-09-16 to 2026-10-15. Total spend: $2,700. Conversions: 46 trial starts (computed)
- Countries: US only
- Optimized event: link clicks (Traffic objective)
- Pixel: StartTrial custom event fires on /welcome after trial signup (verified 2026-10-15 with Events Manager test events). CAPI: not verified
- Daily budgets: six ad sets at $15/day each ($90/day)
- Special ad categories declared: none
- Current customers: 1,840 paying merchants, emails in the billing system (customers agreed to marketing contact at signup)

## Fixes
F1 · objective · high · 48h · Target: QM_Prospecting_Traffic · Traffic objective optimizing for link clicks: 31,200 clicks, 46 trial starts in 30 days · Fix: switch to an objective that optimizes for StartTrial.
F2 · structure · high · 2w · Target: all six interest ad sets · No ad set got more than 11 trial starts in any week; all stayed in learning · Fix: consolidate to one or two ad sets.
F3 · compliance · high · 48h · Target: ads QM_A1, QM_A2, QM_A3 · Copy says "real-time revenue"; brand rules forbid promising real-time data · Fix: rewrite.
F4 · audience · high · 48h · Target: custom audience "Shopify owners 40k" and "LAL 1% Shopify owners 40k" · Uploaded from a purchased list (vendor: LeadHarbor) · Fix: remove both; seed any lookalike from paying customers.
F5 · creative · medium · 2w · Target: QM_A4 · Headline "See every dollar from Shopify and Stripe in one dashboard" is cut off in feed · Fix: shorten headlines.
F6 · audience · medium · 2w · Target: all prospecting ad sets · Current customers aren't excluded · Fix: exclude them.
F7 · placements · low · 3m · Target: all ad sets · Manual placements, Facebook Feed only; no vertical assets · Fix: Advantage+ placements with 1:1/4:5 and 9:16 assets.
