# Output format: AUDIT.md and fixes.md

## Contents
- AUDIT.md
- fixes.md (the hand-off to the build step)
- Plan horizons

Both files go in `audits/meta-ads/<account>/`, beside `metrics.json`, `checks.json` and `score.json`. Never write into the exports folder.

## AUDIT.md

```markdown
# Meta ads audit: <account name>

<period start> to <period end> (<days> days) · <currency> · audited <date>
**Score:** <n>/100 (<band>) · **Confidence:** <level> (<reason>) · **Compliance:** Clear | Blocker: <one line>
**Status:** final | provisional (no brand memory: goal assumed to be <goal>)

**Recommendation:** <the single most important move, one sentence>

## Top three findings
1. **<finding in plain words>.** <computed evidence: names and figures>. **Fix:** <what to change>. (fixes.md F<n>)
2. …
3. …

## Plan
### Next 48 hours
- <action> (F<n>)
### Next 2 weeks
- <action> (F<n>)
### Next 3 months
- <action, and what to measure>

## All ten checks
| Check | Status | Evidence |
|---|---|---|
| Objective vs goal | fail | … |
(all ten, in the order of references/checks.md)

## The numbers
Totals for the period: spend, results, conversions, cost per result, CTR, CPM, frequency. One short table per campaign and per ad set with spend, results, cost per result, results per week. All computed from the export.

## What the business count shows
Only if the user gave their own count: Meta's count, the business count, the ratio, the reported and the real cost per conversion.

## Not assessed
Each `na` check and the export that would cover it. What would raise confidence (a longer range, more conversions).

## Assumptions
Anything inferred rather than given (the goal, what an event records), each marked as an assumption.
```

Rules:
- A compliance blocker is always finding 1, whatever the score.
- Each finding names the exact campaign, ad set or ad as it appears in the export.
- No benchmark without its named source. No forecast, target or promised result. If the user asked for one, the Recommendation or the plan gives the baseline and a check date instead.
- A sound account gets a short report: say what's working, give at most three minor changes, and recommend keeping the structure.

## fixes.md (the hand-off to the build step)

The build step reads this file to make the changes, so keep the shape exact.

```markdown
# Meta ads fixes: <account name>

Source: AUDIT.md (<period start> to <period end>) · Status: proposed, nothing applied · Every fix needs the account owner's approval before it's made.

## Account facts
- Currency: <code> · Period: <start> to <end> · Spend: <computed> · Conversions: <computed>
- Countries: <from settings, or not in export>
- Optimized events: <event per campaign, from settings>
- Pixel / Conversions API: <what Events Manager shows: connections, event ID coverage> (verified from export | not verified)
- Daily budgets: <per ad set, from settings, or not in export>
- Special ad categories declared: <per campaign>

## Fixes
F1 · <area> · <priority> · <horizon> · Target: <exact name, or "account"> · <finding with computed evidence> · Fix: <what to change>
F2 · …
```

- **area:** objective | structure | budget | audience | placements | creative | tracking | compliance
- **priority:** blocker | high | medium | low. Order the list by priority first (all blockers, then all high, then medium, then low), and by horizon only within the same priority. Compliance blockers are always F1.
- **horizon:** 48h | 2w | 3m
- **Target:** an exact campaign, ad set or ad name as it appears in the export, or `account` for account-wide changes, including tracking fixes (name the dataset and event in the finding, not in Target).
- One change per line. No dollar figure that isn't in the export or computed from it, and no target cost, forecast or promised result.
- A fix that depends on another says so ("after F2: switch optimization to StartTrial once it's receiving events").
- In a sound account, fixes.md has at most three lines, all low priority, or says "No changes recommended." The same three are the only changes in AUDIT.md: no extra "if present" or "keep doing" items dressed as changes.

## Plan horizons

- **48 hours:** stop the bleeding and the risk: hold a non-compliant campaign, stop scaling, fix deduplication, remove a stray pixel, exclude a costly placement.
- **2 weeks:** restructure: consolidate ad sets, change objectives, move optimization to the right event once it fires, add creative in a second format, align attribution.
- **3 months:** test and measure: an Advantage+ test with a set end date, a creative testing rhythm, a monthly check of Meta's count against the business count.
