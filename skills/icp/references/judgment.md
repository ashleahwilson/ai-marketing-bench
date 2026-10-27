# Judgment: from the numbers to an ICP

## Contents
- Read the analysis before believing it
- How much the data can say
- Choosing the segments
- Disqualifiers
- Triggers and signals
- Building the rubric
- Hard situations
- Self-check questions

## Read the analysis before believing it

Check the top of the analysis first:
- **Columns used.** Is each mapping right? A column called "Value" might be MRR, not annual value; "Size" might be locations, not headcount. Rerun with `--map` if not, and say in the reply which column you read as what.
- **Excluded rows.** Say how many and why (open deals, duplicates, no outcome). Rows with a blank segment field show as "unknown": name how many.
- **Missing fields.** No churn column means no retention finding; say so instead of guessing. A date-format warning means the cycle figures assume month/day: say it once.
- **Outcome meaning.** "Won" counts customers who later churned, so a segment can win often and still be a bad bet. Read win rate, churn and deal size together.

## How much the data can say

| Closed records behind a finding | Call it | Write it as |
|---|---|---|
| Under 5 | anecdote | counts only ("0 of 4 won"); never a reason on its own, except alongside a brand-memory exclusion |
| 5–9 | hypothesis | counts only ("9 of 9 won"), labelled hypothesis |
| 10+ | evidence | counts, and a percentage if useful ("10 of 12 won (83%)") |

Under 10 closed records in the whole file, the entire ICP is a hypothesis: status `provisional`, counts only, no "converts best" verdict. Say what would firm it up: roughly 30 closed records including losses, with outcome, segment fields, deal value and close dates.

A difference between two segments is worth reporting only when both have 10+ records and the gap is large (for example 1 of 10 churned against 6 of 11). Otherwise report the counts and say it's too early to tell.

## Choosing the segments

Rank segments on three things together, in this order:
1. **Do they stay?** Churn among won customers. A segment that churns at twice the overall rate can't be the top tier on the data alone.
2. **Do they buy?** Win rate on closed deals.
3. **Is it worth it?** Median deal size, then cycle length.

The top tier is usually the segment that's good on all three, not the one that's best on one. Fast, cheap wins that churn are a cost, not a segment. Name the segments in the buyer's terms (industry, size, region) and give each its counts.

## Disqualifiers

- Everything brand memory rules out (`We don't do`, `Not for`, a missing certification) becomes a disqualifier with its reason.
- A segment with zero wins becomes a disqualifier when there's a known reason: brand memory rules it out, or four or more losses point the same way (procurement, a security review, an enterprise suite, a requirement you can't meet). Two losses with different reasons is a watch item: give it negative points instead.
- The rubric always has a `## Disqualifiers` section. If nothing qualifies, leave it empty and say why in Notes.
- A disqualifier needs a reason a salesperson would accept, in one line.

## Triggers and signals

Triggers come from the notes and the data: what happened at the customer just before they bought (a new location, a new operations hire, the person who held the schedule leaving, a contract ending). Count how many notes mention each. One note is a provisional trigger; three or more is worth points. Turn each into a signal criterion (`Signal new location: yes`) the list builder can look for, and say what it would look for (a job post, an announcement).

## Building the rubric

- Use only fields a list builder can fill before contact (industry, size, location, current tool, signals). Lead source only for scoring inbound or CRM lists.
- Points follow evidence. The top segment's defining criterion gets the most points (25–40). A criterion resting on a hypothesis gets 10 or fewer and says "hypothesis".
- Write size bands so they don't overlap (`Locations 1`, `Locations 2–4`, `Locations 5–19`): every matching row is added up.
- Set thresholds, then back-test: apply the rubric to the customer file itself. Retained customers should land mostly in the top tier and lost or churned ones lower. If they don't, adjust weights before handing it over, and report the back-test in one line ("of 22 retained customers, 12 score A and none of the churned do").

## Hard situations

**No customer data.** Build a provisional hypothesis from brand memory: firmographics only from what brand memory states, triggers and disqualifiers tagged `assumed`, personas with `Their words: TBD`. Status `provisional`. No win rates, percentages, deal sizes or cycle lengths. List exactly what data would confirm it (a customer list with outcome won / lost / churned, industry, size, region, deal value, created and closed dates, churn date; plus five call notes).

**A tiny sample.** Give counts, never percentages. Don't name a best segment; say what the counts are and that they could flip with a handful more deals. Write the rubric as provisional, and keep brand-memory exclusions as disqualifiers.

**The user wants a segment the data argues against.** It's their call. In the reply, first say what's true in their view (it closes fastest, it's growing), then the counter-evidence in two or three lines with counts and the churn reasons. Write their version: their segment as the top tier, status `user-directed`, and a Notes line stating what the data shows. Recommend once, concretely: either a different top tier, or a guard that keeps their segment but filters the churn risk (a staff-count floor, a second location, an office manager in place). Don't repeat the warning, don't refuse, don't moralize.

**Asked for market size, TAM or industry benchmarks.** Say once that you don't have a source and won't estimate, name where it could come from (an industry association or regulator count, a licensed company database, analyst research, their own list-building tool's counts), and deliver everything else. Their own churn, win rate and deal size from the data are fine to report, with counts. Don't label anything "typical" or "industry average".

**Asked for persona quotes the notes don't have.** Quote only what's recorded, word for word. A role with no recorded conversation gets no quotes and a TBD, with a way to get them. Don't write lines "they might say".

**Updating an existing ICP.** Copy the old rubric to `icp/history/scoring-v<N>.md` and the old audiences file to `icp/history/`. Rerun the analysis on the new data. Report what moved, old count against new ("single-location churn: 4 of 11 in July, 6 of 11 now"). Bump the version, update the date and basis, keep the user's notes, and change weights only where the evidence moved.

## Self-check questions

Answer each before replying. A "no" means fix the files, not add a caveat.
1. Does every number in the files and the reply carry its count, and is every percentage on a denominator of 10 or more?
2. Is every quote copied word for word from a source, and does every role without one say TBD?
3. Is there no market size, TAM, company count or benchmark anywhere?
4. Would the top tier still be the top tier if you looked at churn first? If not, is that the user's stated choice, recorded as such?
5. Does the back-test put retained customers higher than churned and lost ones?
6. Are the user's previous files preserved and their notes kept?
