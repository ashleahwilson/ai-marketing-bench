# Worked example: a Tallyhouse brief for catch-up bookkeeping

Tallyhouse is a fictional restaurant bookkeeping firm. The files:
- `request.md`: what the user asked for
- `brand/`: the parts of brand memory the skill reads
- `briefs/catch-up-bookkeeping.md`: the brief it wrote, which content-qa-gate later checks the finished post against

## The reply the user saw

**Brief written:** `briefs/catch-up-bookkeeping.md` (ready)

**Recommendation:** pitch it as "catching up one month at a time", because brand memory confirms catch-up is quoted per month of backlog, and the free review tells owners how far behind they are before they commit.

**Before it goes to a writer:** nothing blocking. The keyword "catch-up bookkeeping" is unvalidated: no search data was supplied, so check it and the two alternatives in your keyword tool or Search Console before publishing.

**Kept out:** the "3 days, not 3 weeks" claim (held until substantiated), any catch-up price (none is recorded), and the Lantern quote (it's about prime cost, and naming permission is unconfirmed).

## Why it's built this way

| Choice | Reason |
|---|---|
| Audience narrowed to single-location owners | The request said "restaurant owners"; the goal (the free review) and the $349 price fit single locations. Groups would need the $299/location rate |
| Must-includes are four offer lines | Each is tagged confirmed in `offer.md`. Nothing provisional or held is a must-include |
| No "how many owners are behind" statistic | None is recorded. The outline tells the writer not to add one |
| The owner's pain points used as the reader's situation, not as claims | They're provisional in `audiences.md` |
| Keyword marked unvalidated, no volumes | No keyword data was supplied, and estimates would be invented |
| Writer section under `## For the writer`, with no bullet starting "Audience:" or "Goal:" | content-qa-gate reads every `- Field:` line and keeps the last one |
