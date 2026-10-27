# Campaign design

## Contents
- Structure: brand, non-brand, competitor
- Ad groups by intent theme
- Keywords and match types
- Negative keywords
- Settings: networks, locations, languages, bidding
- Budget split and the test frame
- Keyword data: with and without it
- Conversion-tracking checklist
- Rebuilding from an audit fixes list

## Structure: brand, non-brand, competitor

| Campaign | What's in it | Why separate |
|---|---|---|
| Brand | The brand name and its misspellings (exact and phrase) | Brand clicks are cheap and convert well. Mixed in, they hide how non-brand is really doing, and they soak up budget meant for new demand |
| Non-brand | Searches for the problem or service, by theme | This is where new customers come from, and where most of the budget goes |
| Competitor (only with the user's OK) | Competitor names as keywords | Different intent, lower conversion rate, higher risk of complaints. Its own budget so it can't starve the rest |

- Name campaigns plainly: `Search | Brand`, `Search | Restaurant Bookkeeping`, `Search | Competitor`.
- Skip the brand campaign only for a brand nobody searches yet, or a budget too small to split (under about $20/day). Say which.
- Fewer campaigns is better on a small budget. Each campaign needs enough clicks to learn from.

## Ad groups by intent theme

One ad group per theme a searcher would recognize: the service ("restaurant bookkeeping services"), the job to be done ("catch-up bookkeeping"), the role ("restaurant accountant"), the price question ("restaurant bookkeeping cost"). Each ad group gets:
- 5–20 tightly related keywords,
- its own RSA whose headlines repeat the theme's words,
- the landing page that answers that search. Use only pages the user or brand memory names. If no page matches a theme, send it to the closest named page and list "a page for <theme>" as an open item. Never invent a URL.

Split an ad group when its keywords need different headlines. Merge two when they'd share one ad and one page.

## Keywords and match types

| Match | Use for | Default |
|---|---|---|
| Exact `[restaurant bookkeeping]` | The highest-intent terms, and brand | Yes |
| Phrase `"restaurant bookkeeping"` | The core of each theme | Yes |
| Broad | Only with conversion tracking working, smart bidding and a full negative list | No, for a new build |

- Never a single-word broad keyword ("bookkeeping", "accounting"). It buys every meaning of the word.
- Every non-brand keyword names the audience or category ("restaurant bookkeeping", not "month-end bookkeeping review" or "bookkeeping"). A keyword without it buys searches from businesses the brand doesn't serve.
- Keep keywords specific to what's sold and who it's for (from `offer.md` and `audiences.md`). A term for something the brand doesn't offer (payroll when payroll isn't in `offer.md`) stays out, or goes on the open list as "confirm you offer this".
- Informational searches ("template", "calculator", "what is") rarely convert on a paid click. Leave them out or flag them as a content opportunity, not a main ad group.
- Third-party brand names (software, competitors) as keywords are legal to bid on in most markets, but they're the user's call: put them in their own campaign, and never in ad text.

## Negative keywords

A shared list applied to every non-brand campaign, plus campaign negatives where needed. Phrase match by default. Starter themes, kept only where they fit the business:
- Jobs: jobs, careers, hiring, salary, resume, course, certification, training
- Free and DIY: free, template, example, sample, download, diy (drop "free" if the offer itself is free, such as a free review or trial)
- Wrong product: login, sign in, support, phone number (for other companies' tools)
- Not for: every segment in `audiences.md` "Not for" or `offer.md` "We don't do" (for example retail, e-commerce, franchise). Don't call a service "not offered" unless brand memory says so; a negative added on assumption is labelled as one in the plan
- Other brands' login and support terms ("quickbooks login")

Check every negative against every positive keyword in the campaigns it applies to: a negative that blocks your own keyword is a bug. The brand campaign gets the non-brand terms as negatives only if traffic overlaps.

## Settings: networks, locations, languages, bidding

- **Networks:** Google Search only. Turn off Search Partners and the Display Network for a new search campaign: they spend on lower-intent placements before there's data to judge them.
- **Locations:** where the business sells (`audiences.md`, or the user). Location option: **Presence** (people in or regularly in the area), never "presence or interest".
- **Languages:** the languages the ads and landing pages are written in. In Canada, mention French only as a separate campaign with French ads and pages; don't target French with English ads.
- **Bidding, new account or no conversion history:** Maximize clicks, with a maximum CPC set from Keyword Planner's high top-of-page bid when there is data (no cap and a week-one review when there isn't). Move to Maximize conversions once tracking is verified and the campaign has about 30 conversions in 30 days. An account that already has conversion history can start on Maximize conversions.
- **Ad schedule:** all hours to start, unless the user only answers calls in business hours.
- **Status:** everything is imported Paused. Nothing goes live until the user turns it on.

## Budget split and the test frame

Without the user's own cost data, every budget is a test. Say so, and say what the test is for: learning cost per click and cost per conversion on these terms.

Rules of thumb (state them as rules of thumb, never as data):
- Brand: 5–15% of the budget, or whatever its searches use. Brand demand is limited.
- Non-brand: the rest, weighted toward the highest-intent theme.
- Competitor (only if approved): at most 15–20%, as its own line.
- Daily budget = monthly ÷ 30.4. Google can spend up to twice the daily budget on a given day but no more than the monthly total.
- A campaign needs roughly 10 or more clicks a day to learn anything in a few weeks. With planner bids, clicks per day ≈ daily budget ÷ average of the top-of-page bid range. If that's under about 10, cut themes or regions instead of spreading thin.
- Review point: after 2 weeks for search terms and negatives, after 4 weeks for cost per conversion. Then rebalance.

Never forecast conversions, signups, revenue or ROAS from a budget. Without the account's own conversion rate there's nothing to base it on. Say what the test will measure instead.

## Keyword data: with and without it

**Without data** (the usual case): list keywords with match types and mark the list **unvalidated**. State no volumes, CPCs or competition figures, not even ranges "from experience". Tell the user how to get them: in Google Ads, Tools > Keyword Planner > "Get search volume and forecasts", paste the list, set the locations, download the CSV. Offer to update the plan from that file.

**With a Keyword Planner export:** quote volumes and bid ranges exactly as the file gives them. Keywords not in the file stay unvalidated. Use the file to:
- drop or deprioritize terms with no volume or no bid data,
- move off-intent high-volume terms (jobs, templates) to negatives,
- set the maximum CPC from the high top-of-page bid,
- show the budget arithmetic: daily budget, bid range, clicks per day.

## Conversion-tracking checklist

Put this in every plan, with the brand's real conversion named:
- [ ] One primary conversion: the action that means a lead or sale (booked review, demo request, trial start, purchase). Page views and clicks are secondary or not tracked.
- [ ] The conversion fires on the thank-you or confirmation step, not the form page. Test it with a real submission and see it in Google Ads (Tools > Conversions) within a day.
- [ ] Google tag (or Google Tag Manager) on every landing page; auto-tagging on; Google Ads linked to Analytics if they use it.
- [ ] Enhanced conversions for leads, if forms collect an email and their privacy policy allows it.
- [ ] Count: "one" per click for leads, "every" for purchases.
- [ ] Phone calls: a call asset and call conversions only if they take calls.
- [ ] Value: a conversion value only if they know what a lead is worth. Don't make one up.

## Rebuilding from an audit fixes list

Read `audits/google-ads/<account>/fixes.md`. Each line is `<n>. [P1|P2|P3] <area> · <problem> · <fix>`; `## Account facts` gives current budget, geo, networks, bidding and conversion actions.
- Build every P1 and P2 fix, then P3 where it fits.
- A fix marked `(confirm first)` is not built. List it under "Needs your decision".
- A fix that breaks a brand rule or uses an unsupported claim is not built. Say which rule.
- Keep the account's current budget unless the user changes it.
- In the plan, tag each change with its fix number ("Fix 4"), and add a short table: fix, status (done / held / not built), where.
