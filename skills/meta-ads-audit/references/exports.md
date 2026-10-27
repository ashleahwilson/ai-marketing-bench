# What to export

Send this list when there's nothing to audit yet, or when an export is missing. Ask for the same date range in every file: the last 30 days at least, ideally the last 60 to 90. Under 14 days, or under 30 conversions, the audit can still catch setup problems but can't compare ad sets.

## From Ads Manager (Campaigns tab)

1. Set the date range (top right). Turn off any filters so paused campaigns that spent in the period are included.
2. **Columns:** choose Customize columns and add: Objective, Attribution setting, Results, Result indicator, Cost per result, Amount spent, Impressions, Reach, Frequency, Link clicks, CTR (link click-through rate), CPM. Save the column set so all three levels use it.
3. **Export three times, one per tab:** Campaigns, Ad sets, Ads. Reports > Export table data > CSV, with "Include summary row" off.
4. **Breakdowns, two more exports:** at campaign level, Breakdown > By delivery > Placement (export it); then Breakdown > By time > Day at ad set level (export it).
5. **Settings:** the bulk export (select all campaigns > Export & import > Export selected, CSV) carries objective, special ad categories, optimization goal and conversion event, attribution, countries, age range, custom audiences, Advantage+ audience, placements and budgets. If that's not possible, a screenshot of each ad set's settings works.

Ad text (headline and primary text) helps the special ad category check. It's in the bulk export, or in the Ads tab with the Headline and Body columns.

## From Events Manager

For each dataset (pixel) connected to the account: the Overview tab, with each event's count split by connection method (Browser, Server / Conversions API), the event match quality, and the deduplication or event ID coverage shown in the event's details. A screenshot is fine. If there are two datasets, send both: a leftover pixel is a common cause of double counting.

## From the business

- What counts as a conversion for paid ads (a demo request, a trial, a purchase) and which Meta event should represent it.
- The business's own count of that conversion for the same period (CRM, booking system, app or store), from all sources.
- Any target cost per result, and where it comes from.
- Whether any campaign advertises jobs, housing, credit or financial products, or social issues, elections or politics, and which countries it runs in.

## Connected tool instead of exports

If an ads tool is connected, pull the same fields with read and report actions only, for the same date range. Never call an action that edits, pauses, duplicates or creates anything, even to test.
