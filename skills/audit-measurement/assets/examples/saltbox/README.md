# Worked example: Saltbox Coffee Roasters

Saltbox is a fictional coffee roaster that sells online, only in Canada. The files:
- `site/`: the three saved pages (home, product, order confirmed)
- `brand/BRAND.md`: its brand memory, which says where it sells and that it uses Canadian spelling
- `audits/saltbox.example/measurement.md`: the report
- `audits/saltbox.example/tracking-plan.md`: the tracking plan
- `audits/saltbox.example/dim-measurement.json`: the checklist result, in the full audit's format

## Why a 95 still leads with two high-severity findings

The checklist scores what the full audit scores: analytics on every page, a conversion that fires on the outcome, ad tags, hygiene and consent basics. Saltbox does most of that well. Two problems sit outside the points or only cost a few:

| Finding | Why it leads | Points |
|---|---|---|
| `customer_email` in the purchase push | Personal data headed for analytics or ad tags. No check of its own, so it costs no points, but it's the first fix | none |
| Meta Pixel before the cookie banner | The audience is Canada, and consent mode only holds Google tags | M5 drops to 5 |

## What it didn't do

- **No order or traffic numbers.** No export was supplied, so none appear.
- **No guess about the container.** GTM-SB31KQ may forward the purchase event to GA4 and Meta; without the export that's listed as not observable, and the 48-hour plan asks for it.
- **No legal verdict.** The privacy section says what loads before consent and why it matters for a Canadian audience, and leaves the judgment to whoever handles privacy.
