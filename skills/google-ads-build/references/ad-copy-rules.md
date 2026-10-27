# Ad copy rules

## Contents
- Responsive search ads
- Claims: what ad text can say
- Requests to hold back
- Competitor and third-party trademarks
- Editorial and policy basics
- Assets: sitelinks, callouts, structured snippets

## Responsive search ads

| Element | Limit | How many |
|---|---|---|
| Headline | 30 characters | 3–15; write 10–15 |
| Description | 90 characters | 2–4; write 3–4 |
| Path 1, Path 2 | 15 characters each | optional |

Google mixes headlines in any order, three at a time, and descriptions two at a time. So:
- Every headline must stand on its own and read well next to any other.
- Cover different jobs: 2–3 with the ad group's keyword, 2–3 on what's offered, 2–3 on proof the brand can back, 1–2 on price or offer, 2 calls to action, 1 brand name.
- No two headlines that say the same thing in different words. Exact duplicates are rejected.
- Descriptions add what a headline can't: who it's for, what's included, the next step.
- Spell the way the brand does (`voice.md`). Without brand memory, follow the user's own spelling.

**Pinning.** Pin only when something must always show: a required disclaimer, or the brand name in position 1 when the user insists. Pin two or three headlines to the same position rather than one, so Google still has choices. Never pin everything: it turns the ad into a fixed ad and ad strength drops.

## Claims: what ad text can say

Every claim in an ad comes from brand memory or the user. Check each one:
- **Numbers** (prices, percentages, counts, times): the exact figure must be in `brand/` or the user's message, and right for this ad. A group rate is not a single-location price.
- **A segment's price names the segment in the same line.** Headlines are shown in any combination, so "From $299/Location/Month" can read as everyone's price. Write "Groups: From $299/Location" or keep it in a description that names the groups.
- **Don't imply a channel or step the offer doesn't have** ("Call us", "Talk to a bookkeeper today") unless brand memory says it exists.
- **Qualifiers travel with the number.** "From $299 per location per month" stays "from" and "per location"; a flat $349 never becomes "from $349". Don't add a frequency or scope brand memory doesn't state ("monthly filings" when it only says "filings").
- **Claims marked "needs substantiation"** in `claims.md`, or banned in `rules.md`, stay out of the ads until they're substantiated, even if the website uses them.
- **Customer names and quotes** run only when `proof.md` records permission to name them.
- **Superlatives and rankings** ("#1", "best", "leading", "fastest", "most trusted", "cheapest") need proof a reader could check: a named ranking, an award, a published comparison. Brand memory almost never has it. A softened version ("a leading", "top-rated") is the same claim: don't suggest one.
- **Guarantees** ("guaranteed", "risk-free", "100%") only if the offer really includes one, in brand memory.
- **Results** ("save 10 hours", "cut food cost 20%") need a measured customer result in `results.md` or `proof.md`. A plausible number is still invented.
- **Compliance and security claims** (HIPAA, SOC 2, PCI, "bank-level security") only from brand memory.

What usually can run: what the product does, who it's for, what's included, the price, the entry offer, the team's real background, integrations by name. These make strong ads.

## Requests to hold back

When the user asks for a claim that can't run, do the rest of the work and hold that line:
1. Leave it out of the ad text and the CSV.
2. Under "Held back", one line each: what was asked, why it can't run, and what would let it run ("a published ranking we can cite", "a client's measured close time"). Don't lecture.
3. Put a supported line in its place.

Same for invented data: if the user wants volumes, CPCs or a forecast without data, give the keyword list marked unvalidated and say how to get the data.

## Competitor and third-party trademarks

- **Never in ad text,** including headlines, descriptions, paths, sitelinks and callouts. Google can restrict ads that use a trademark the owner has registered with them, and the owner can complain. Comparisons ("cheaper than X", "X alternative") also need proof about the competitor that brand memory rarely has.
- **As keywords:** usually allowed. Offer it as the user's decision, in its own campaign with its own capped budget, with generic ad text about the brand's own strengths. Expect higher costs and lower conversion rates than brand or non-brand.
- **Software and platform names** the brand integrates with (Toast, Square, Shopify) can appear in ad text as a factual integration statement ("Works with Toast and Square") when brand memory confirms the integration. Never imply partnership or endorsement.

## Editorial and policy basics

- No exclamation marks in headlines; at most one in the whole ad.
- No repeated punctuation, emoji or decorative symbols.
- No ALL CAPS words for emphasis (normal acronyms like P&L and POS are fine).
- No "click here". Name the action: "Book your free review".
- No phone numbers in ad text: use a call asset.
- The landing page must deliver what the ad says: same price, same offer.
- Restricted categories (health, finance, legal, alcohol, gambling) may need certification or extra disclosures. Flag it; don't guess the rule.

## Assets: sitelinks, callouts, structured snippets

| Asset | Limit | How many |
|---|---|---|
| Sitelink text | 25 characters | 4–8 |
| Sitelink description lines | 35 characters each (both or neither) | |
| Callout | 25 characters | 4–10 |
| Structured snippet value | 25 characters | at least 3 per header |

- Sitelinks point to real pages the user or brand memory names. With only one or two pages known, list the sitelinks they'd need as an open item instead of inventing URLs.
- Callouts are short facts: "Named bookkeeper", "No setup fee". Same claim rules as ads.
- Snippet headers must be one of Google's: Amenities, Brands, Courses, Degree programs, Destinations, Featured hotels, Insurance coverage, Models, Neighborhoods, Service catalog, Shows, Styles, Types. For a service business, "Service catalog" or "Types" usually fits.
