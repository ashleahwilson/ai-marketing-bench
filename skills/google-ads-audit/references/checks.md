# The 11 checks

## Contents
- Statuses and the score
- Confidence
- 1 Conversion tracking (20)
- 2 Wasted spend and negatives (15)
- 3 Match-type mix (5)
- 4 Budget limits (8)
- 5 Bid strategy against conversion volume (10)
- 6 Quality Score (8)
- 7 Responsive search ad coverage (6)
- 8 Location targeting (8)
- 9 Network settings (7)
- 10 Brand and non-brand split (5)
- 11 Landing page match (8)
- Brand rules in live ads
- Benchmarks and thresholds

## Statuses and the score

Each check is PASS (1 point), WARN (0.5) or FAIL (0), times its weight (in brackets). A check without the data is NOT CHECKED and leaves the denominator. Bid strategy on a Low-confidence account is INSUFFICIENT DATA, also unscored. Score = points ÷ weights checked × 100. Grade: A 85+, B 70–84, C 55–69, D 40–54, F under 40. Fewer than 6 checks scored: call the score partial.

The script sets the status. Change one only for a reason you can quote from the data (for example, a flagged landing page that you can show is the right page), and say so in the finding. Never change it because the user would like a better grade.

## Confidence

High: 60+ days and 30+ real conversions (real outcomes, duplicates counted once). Medium: 28+ days and 15+. Low: anything less, or an unknown date range. These are this audit's rules of thumb. State confidence and its basis in the verdict line. On Low: no verdict on bid strategy, no annualized or monthly projections, and say which findings would change with more data (usually none of the settings findings: Display on a Search campaign is wrong at any volume).

## 1 Conversion tracking (20)

What it catches: a primary action that isn't a business outcome (page views, scrolls, video views, time on site, engagement), two primary actions that count the same event (the same lead form tracked by the Google Ads tag and imported from GA4), lead actions counted "Every", and conversion values that are a fixed assigned number rather than revenue.

Why it leads: Smart Bidding optimizes to whatever is primary. Inflated conversions make CPA look good and teach bidding to buy page views. Always report both figures the script gives: the reported CPA and the cost per real outcome counted once. When two duplicate actions disagree, give the range (the script's low and high).

Fixed values: say ROAS in the account is assigned value ÷ cost, not revenue return. Ask what a conversion is actually worth or whether real values can be passed. Never call it real ROAS.

## 2 Wasted spend and negatives (15)

The script auto-flags zero-conversion terms with a universal junk modifier (jobs, salary, course, template, free, login…). It lists every other zero-conversion term for you to judge against the business: the offer, who it's for and who it's not for in brand memory. Write the ones that are clearly irrelevant to a file (pattern plus reason) and rerun with `--irrelevant`. Only the rerun total goes in the report.

- **Clearly irrelevant:** a different buyer (homeowners searching for a plumber when you sell software to plumbing firms), a segment brand memory excludes (wholesale when you serve shops), job seekers, students, existing-customer logins, a different product.
- **Borderline:** plausible buyers with off-centre intent, or terms that converted. Don't add them to the waste total. List them separately with their cost and ask.
- Junk-modifier terms that converted are listed for review: never call them waste.
- Existing negatives: the script shows a negative that should block a term but doesn't because of its match type (an exact-match `[careers]` doesn't block "plumbing software careers"). Name it: it's a common, cheap fix.
- Search Partners spend and search-term waste may overlap (the search terms report can include partner traffic), and the exports don't show by how much: never add them together, and never say one contains the other.
- The fix is a negative at the right level (campaign, or a shared list for account-wide junk) and match type (usually phrase).

## 3 Match-type mix (5)

Report spend share by match type. Broad match on Manual CPC or Maximize clicks is a FAIL: nothing steers it. Heavy broad match is a FAIL when conversion tracking is also failing, because bidding is learning from bad signals. Otherwise heavy broad is a WARN, not an error.

## 4 Budget limits (8)

A campaign losing 10%+ of search impression share to budget is limited (25%+ is FAIL). Before recommending more budget: is its own waste larger than nothing? Is its cost per conversion better than non-brand traffic in the other campaigns? Compare with non-brand, not the blended account CPA, which brand searches pull down. The dollar figure to give is money that can move (waste in the same campaign, or spend in a weaker campaign), never a forecast of extra conversions.

## 5 Bid strategy against conversion volume (10)

Conversions per 30 days per campaign. Rule of thumb this audit uses (not a Google requirement): Target CPA or Target ROAS wants 15+ per campaign per 30 days; Maximize conversions under 15 is a WARN; Manual CPC or Maximize clicks with 30+ is a WARN (Smart Bidding is an option). If conversion tracking failed, the volumes shown are inflated: say so, and judge on real outcomes where you can. On Low confidence, give no verdict: say what data would settle it.

## 6 Quality Score (8)

Spend-weighted Quality Score, share of spend on keywords at 4 or below, and spend by component rated Below average. Name every keyword at 4 or below with its score, ad group and spend. Point at the component: Exp. CTR is the ad's job, Ad relevance is the ad group's theme, Landing page exp. is the page. Don't claim a Quality Score change will cut CPC by a set percentage.

## 7 Responsive search ad coverage (6)

Per ad group with spend: number of responsive search ads, the most headlines and descriptions in one, ad strength. An ad group with spend and no responsive search ad is a FAIL. This audit's rule of thumb: 8+ headlines and 3+ descriptions (Google allows 15 and 4). Suggested new headlines use only facts in brand memory or the account's existing ads.

## 8 Location targeting (8)

"Presence or interest" lets people outside the targeted area see ads. With a user-locations export, the script gives spend outside the targets: that's the figure. Without one, it's a WARN and the fix is the same (switch to Presence). Check targets against who brand memory says the business serves.

## 9 Network settings (7)

Display Network switched on in a Search campaign is a FAIL. Search Partners is a WARN, or a FAIL when the network report shows partner spend with zero conversions. Give the segment spend.

## 10 Brand and non-brand split (5)

Brand terms come from brand memory (company and product names, common misspellings) or the user. A campaign spending on both brand and non-brand keywords hides the real cost of new demand: brand searchers convert cheaply. Give brand CPA, non-brand CPA and the blended figure. No brand terms: NOT CHECKED, and ask for them.

## 11 Landing page match (8)

The script flags non-brand ad groups sent to the homepage, and ad groups where Landing page exp. is Below average on half or more of the spend (plus a URL that shares no word with the ad group). These are leads: name the ad group, its keywords and the URL, and say what page would match. A dedicated offer page (a booking or review page) is fine for every ad group if it matches the promise in the ad. You can't see the page unless it's supplied: don't describe its content.

## Brand rules in live ads

Read every headline and description against `brand/rules.md`, `claims.md` and `voice.md` (never-use words). A live ad that breaks a brand rule or uses an unsubstantiated claim is a finding under responsive search ad coverage, with the exact text quoted. No brand memory: skip this and say so under "Not checked".

## Benchmarks and thresholds

The thresholds in this file are the audit's own rules of thumb: call them that. An industry benchmark (average CTR, CPC, conversion rate for a sector) appears only with a named source and date the user supplied or brand memory holds. Otherwise leave it out. Platform facts (15 headlines, 4 descriptions, what each setting does) are fine.
