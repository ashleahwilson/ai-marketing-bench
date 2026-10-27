# Pipeline Search: Google Ads build plan
**Recommendation:** Import paused, confirm the demo booking is tracked as the primary conversion, then run a 4-week test at $65.80/day.
**Status:** Draft

## Held back
- **Rosa Lim's "Best tool we've bought all year" as a headline.** "Best" is a ranking claim nobody can check, and Google disapproves exclamation marks in headlines. Unlocked by: a factual line from Rosa about what changed for her team (permission to name her is already on file).
- **Search volumes per keyword.** No Keyword Planner or account data was supplied, so every keyword is unvalidated. Unlocked by: in Google Ads, Tools > Keyword Planner > "Get search volume and forecasts", paste the keywords below, location United States, download the CSV. The plan will be updated from it.

## Before you launch
1. **Conversion tracking (needed first).** Is a booked demo tracked as a conversion in Google Ads? Assumed: "Demo booked" fires on the booking confirmation page.
2. **A fourth landing page.** Brand memory names /, /pricing and /demo. A forecasting page would give the forecasting ad group a closer match and a fourth sitelink.
3. **Locations.** Assumed United States only, as asked; brand memory agrees.

## Settings
| Campaign | Networks | Locations | Languages | Bid strategy | Daily budget |
|---|---|---|---|---|---|
| Search \| Brand | Google Search only | United States, Presence | English | Maximize clicks | $6.50 |
| Search \| Sales Pipeline | Google Search only | United States, Presence | English | Maximize clicks (move to Maximize conversions after about 30 demos in 30 days) | $59.30 |

## Structure
| Campaign | Ad group | Theme | Landing page |
|---|---|---|---|
| Search \| Brand | Brand | People searching for Pipewise | https://pipewise.example/ |
| Search \| Sales Pipeline | Pipeline software | Looking for pipeline software | https://pipewise.example/demo |
| Search \| Sales Pipeline | Sales forecasting | Looking for forecasting by rep | https://pipewise.example/demo |
| Search \| Sales Pipeline | Pricing | Comparing what it costs | https://pipewise.example/pricing |

## Keywords
All keywords are **unvalidated**: no volume or cost data yet.
- **Brand:** [pipewise], "pipewise", "pipe wise crm"
- **Pipeline software:** "sales pipeline software", [sales pipeline software], "pipeline management software", "b2b sales pipeline tool", "deal pipeline software"
- **Sales forecasting:** "sales forecasting software", "sales forecast by rep", "b2b sales forecasting tool", [pipeline forecasting software]
- **Pricing:** "sales pipeline software pricing", "pipeline software cost", "sales pipeline tool price per user"

## Negative keywords
Shared list "Non-brand negatives", phrase match, on Search | Sales Pipeline: jobs, salary, course (job seekers and students); template, free, excel (DIY searches); email marketing, marketing automation (Pipewise doesn't do them); login (other tools' users).

## Ads
**Pipeline software** (Final URL /demo, path /pipeline/demo)
Headlines: Sales Pipeline Software (23) · Pipeline Software for B2B (25) · See Which Deals Are Real (24) · Forecasts by Rep (16) · Weekly Pipeline Review View (27) · $45 Per Rep Per Month (21) · Every Feature, Every Rep (24) · Cancel Any Month (16) · No Setup Fee (12) · Price on the Site, No Calls (27) · Book a 30-Minute Demo (21) · Pipewise Pipeline Software (26). No pins.
Descriptions: Deal stages, forecasts by rep and a weekly pipeline review for B2B sales teams. (80) · One plan: $45 per rep per month, every feature for every rep. Cancel any month. (80) · No setup fee and no sales call to see the price. Book a 30-minute demo. (71)

The Brand, Sales forecasting and Pricing ads follow the same pattern (10–11 headlines, 3 descriptions each); the full text is in the import file.

## Assets
- **Sitelinks:** Pricing (/pricing) · Book a Demo (/demo) · Pipewise Home (/). A fourth waits on a new page.
- **Callouts:** No Setup Fee · Cancel Any Month · Every Feature, Every Rep · Price Shown Upfront
- **Structured snippet (Types):** Deal stages; Forecasts by rep; Pipeline reviews

## Budget
$2,000 a month is $65.80 a day across 30.4 days. Brand gets $6.50 (about 10%): brand searches are limited and cheap, and splitting them out keeps non-brand results honest. Non-brand gets $59.30. This is a **test**: there's no cost data yet, so it's not possible to say how many clicks or demos it will buy. It measures cost per click by theme in weeks 1–2 (review search terms and add negatives) and cost per demo booked by week 4 (then move budget toward the ad groups that book demos).

## Conversion tracking
- [ ] Primary conversion: Demo booked, firing on the booking confirmation step. Page views are not conversions.
- [ ] Test it with a real booking and see it in Tools > Conversions within a day.
- [ ] Google tag on /, /pricing and /demo; auto-tagging on.
- [ ] Enhanced conversions for leads if the demo form collects an email and the privacy policy allows it.
- [ ] Count "one" per click.
- [ ] No conversion value until you know what a demo is worth.

## Facts used
- $45 per rep per month, one plan, every feature for every rep, cancel any month, no setup fee, price shown without sales: offer.md (website /pricing, 2026-08-20)
- Deal stages, forecasts by rep, weekly pipeline review view: offer.md (website /product, 2026-08-20)
- 30-minute demo: offer.md (Jordan Lee, 2026-09-02)
- B2B sales teams, United States: BRAND.md
- "See which deals are real": paraphrases Rosa Lim's quote in proof.md ("knows which deals are real"), without naming her or the superlative
