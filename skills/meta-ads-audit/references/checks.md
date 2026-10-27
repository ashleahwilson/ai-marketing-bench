# The ten checks

## Contents
- How to judge
- 1. Objective against the business goal (10 points)
- 2. Conversion events (15)
- 3. Attribution setting (5)
- 4. Structure, budget and learning (15)
- 5. Audience overlap (5)
- 6. Frequency and creative fatigue (10)
- 7. Creative volume and variety (15)
- 8. Placements (10)
- 9. Advantage+ use (5)
- 10. Special ad categories (10)
- checks.json format

## How to judge

Each check gets one status (any blocker caps the score at 69, Needs work): `pass` (nothing to change), `warn` (worth fixing, not costing much), `fail` (costing money or corrupting the data), `blocker` (compliance, or tracking so broken the account is optimizing on noise), `na` (no data: say which export would cover it). Evidence is one line quoting a computed figure or a file. Thresholds marked "audit rule" are this audit's working rules, not industry benchmarks: say so if you mention one.

When confidence is Low (under 14 days or under 30 conversions), performance checks (6, 7 and 8) can't reach `fail` on cost differences alone; structural checks (1, 2, 4 and 10) still can.

## 1. Objective against the business goal

Meta's objectives are Awareness, Traffic, Engagement, Leads, App promotion and Sales. A conversion goal (leads, trials, purchases) needs Leads or Sales optimizing the event that represents that conversion.
- **fail:** a campaign with a conversion goal runs on Traffic, Engagement or Awareness (it optimizes clicks or views, so Meta finds clickers, not buyers). Quote its spend and its conversions.
- **warn:** an objective that fits but optimizes a softer event than the goal (see check 2) or a retargeting campaign on a different objective with no reason given.
- A Traffic or Awareness campaign with a stated awareness or audience-building purpose can pass.

## 2. Conversion events

Compare four things: the event each ad set optimizes (settings: optimization goal and conversion event), what that event actually records (tracking notes, `brand/`, the user), how Events Manager receives it, and the business's own count.
- **Wrong optimized event:** the ad sets optimize an event that isn't the business conversion (a newsletter signup counted as Lead when the goal is trials). fail.
- **Dead event:** the goal's event shows 0 or near-zero received while the business recorded conversions. fail: the account can't optimize for it until it fires.
- **Duplicates:** an event received from browser and server without event IDs on both (coverage well under 90%) isn't deduplicated, so it's counted up to twice. The same event from two datasets (an old agency pixel) adds more: recommend removing the extra dataset's code from the site and keeping the one the ad sets optimize on, unless the user says otherwise. fail, or blocker when the inflated event is the one being optimized. Quote the counts by connection and the Meta-to-business ratio.
- **Browser only:** no Conversions API (server) events at all. warn: signal lost to browsers and ad blockers.
- Event match quality, if shown: note it; don't grade on it without other problems.
- With the business's count, give both costs: Meta's reported cost per result and spend divided by the business count. The second is the real one.

## 3. Attribution setting

- **warn:** ad sets in the same account use different attribution settings (1-day click on some, 7-day click or 1-day view on others). Their results aren't comparable, so don't rank ad sets across settings.
- Note that platform-attributed results won't match the business's count exactly; a gap of 2x is a tracking problem (check 2), not attribution.

## 4. Structure, budget and learning

Meta's published guideline: an ad set needs about 50 optimization events in a 7-day period to exit the learning phase. The analysis gives each conversion ad set's results per week.
- **fail:** most of a campaign's budget sits in ad sets far below 50 a week, especially many small ad sets in one campaign. Quote the count and the weekly figures. Recommend consolidating into fewer ad sets (or one with Advantage+ audience), and say whether even the combined total reaches 50 a week; if it doesn't, recommend optimizing a higher-volume event only if it still predicts the business conversion.
- **warn:** one small ad set below the guideline, such as a retargeting pool, which is normal when the pool is small.
- **pass:** the main ad sets are at or above the guideline.
- Say "below Meta's learning guideline", not "in learning": the export only shows learning status if the delivery column says so.

## 5. Audience overlap

Without Meta's Audience Overlap tool output, overlap can only be inferred from settings: nested lookalike ranges (1% and 3% of the same seed), the same interest or custom audience in several ad sets, prospecting that doesn't exclude retargeting pools or customers.
- **warn:** an overlap visible from the settings, named.
- **na:** nothing in the settings to judge, and no overlap export.

## 6. Frequency and creative fatigue

There's no universal frequency limit. Judge fatigue from the account's own trend: compare the first and second half of the period for the same ad set.
- **fail:** high frequency for the period and CTR down and cost per result up between halves (audit rule: CTR down 20% or more and cost per result up 20% or more). Quote the frequency, both CTRs and both costs.
- **warn:** frequency rising with CTR slipping, cost still steady.
- **na:** no day breakdown.

## 7. Creative volume and variety

Count ads per ad set and formats (single image, video, carousel) from the ad export.
- **fail:** most ad sets run one or two ads in a single format, so there's nothing to test and fatigue sets in fast.
- **warn:** several ads but one format, or one ad set with a single ad.
- **pass:** several ads per main ad set across at least two formats.
Don't judge the creative itself from names alone.

## 8. Placements

From the placement breakdown, each placement's share of spend and its cost per result against its campaign.
- **fail:** a placement takes a material share of spend at a much higher cost per result (audit rule: 10% or more of spend at 1.5x the campaign cost or worse). Quote share, cost and multiple. Audience Network on a lead or trial goal is the usual case.
- **warn:** a manual placement list that excludes the placements doing best, or a large share on a placement with a small result count.
- Small placements with a handful of results can't be judged on cost.

## 9. Advantage+ use

Note what's in use: Advantage+ audience, Advantage+ placements, Advantage+ sales or leads campaigns. Not using them isn't a failure.
- **warn:** many narrow manual ad sets in learning where Advantage+ audience would pool the budget, or manual placements adding a costly placement.
- **pass:** in use, or manual choices with a visible reason.
- Recommend a test (one Advantage+ ad set against the current structure, same budget, set end date), not a switch.

## 10. Special ad categories

Meta requires a special ad category for ads about employment, housing, credit (financial products and services), and social issues, elections or politics, including in the US and Canada; requirements by country change, so the user should confirm the current list in Ads Manager. With employment, housing or credit declared, age, gender and postcode targeting are locked, location needs a minimum radius, and lookalike audiences aren't available.
- The analysis lists campaigns whose names or ad text contain category terms (hiring, apply now, careers, rent, mortgage, loan, vote…) and what's declared. Judge each: "hiring" in a job ad is employment; "job" in "jobs to be done" isn't.
- **blocker:** a campaign that clearly falls in a category with the category set to None. Lead the report with it. Say: don't scale it; recreate it with the category declared; its current targeting (quote the age range, lookalike or postcode targeting) won't be available, so its current cost per result won't carry over. Don't make legal claims beyond Meta's policy.
- **pass:** declared where needed, or no campaign falls in a category (say "not required").

## checks.json format

```json
{"account": "quillmetrics", "checks": {
  "objective": {"status": "fail", "evidence": "Prospecting | Free trial | Traffic: Traffic objective, $1,680.00, 0 trials"},
  "conversion_events": {"status": "blocker", "evidence": "..."},
  "attribution": {"status": "warn", "evidence": "..."},
  "structure_learning": {"status": "fail", "evidence": "..."},
  "audience_overlap": {"status": "na", "evidence": "no overlap export; no nested audiences in settings"},
  "frequency_fatigue": {"status": "pass", "evidence": "..."},
  "creative": {"status": "warn", "evidence": "..."},
  "placements": {"status": "pass", "evidence": "..."},
  "advantage_plus": {"status": "pass", "evidence": "..."},
  "special_ad_categories": {"status": "pass", "evidence": "not required: no campaign advertises jobs, housing, credit or social issues"}
}}
```
