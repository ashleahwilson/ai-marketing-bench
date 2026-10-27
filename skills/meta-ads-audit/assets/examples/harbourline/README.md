# Worked example: Harbourline Kayak Co.

Harbourline Kayak Co. is a fictional Canadian online kayak retailer. No results are claimed; every figure comes from the fictional exports in `exports/`.

**The request:** "Audit our Meta account for August. Exports are in exports/. The store recorded 164 orders from all sources in August." No brand memory, so the report is marked provisional.

**What the audit found:** a sound account (74/100, High confidence) with clean tracking and the right objective. The top findings are a worn-out cart retargeting ad (frequency 9.4, cost per purchase from $14.15 to $97.55 between the two halves of the month), a camping interest ad set too small to learn, and too few ads to test.

**The files:**
- `exports/`: the Ads Manager and Events Manager exports (campaign, ad set and ad level, day and placement breakdowns, settings, events)
- `audits/meta-ads/harbourline/AUDIT.md`: the full report
- `audits/meta-ads/harbourline/fixes.md`: the change list for the build step
- `audits/meta-ads/harbourline/metrics.json`, `checks.json`, `score.json`: the computed numbers, the ten check statuses and the score

**The reply the user got:**

> **Score:** 74/100 (Sound) · **Confidence:** High (31 days, 107 conversions)
> **Recommendation:** Refresh the cart retargeting ad and fold the camping ad set into the Advantage+ ad set before adding budget.
>
> **Top three findings**
> 1. The cart retargeting ad has worn out: frequency 9.4, CTR down from 2.01% to 1.21% and cost per purchase up from $14.15 to $97.55 between the first and second half of August. Add two new ads.
> 2. Kayaks | Interest: camping got 9 purchases for $930.00 ($103.33 each, 2.03 a week, far under Meta's guideline of about 50 a week per ad set). Pause it and move its budget to the Advantage+ ad set ($54.71 per purchase).
> 3. Four ads in total, two ad sets with a single image ad. Add video and carousel ads.
>
> **Next 48 hours:** new retargeting ads; pause the camping ad set and move its $30.00 daily budget.
>
> **Files:** audits/meta-ads/harbourline/AUDIT.md (full report and plan), fixes.md (the change list)
> **Not assessed:** audience overlap (send the Audience Overlap export and ad set exclusions). Tracking is clean: purchases are deduplicated between browser and server.
