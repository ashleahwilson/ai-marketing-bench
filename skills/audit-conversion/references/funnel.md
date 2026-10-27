# Reading an analytics export

Conversion rates and drop-off exist only in the user's analytics. Use them when the user supplies an export; never estimate them otherwise.

## What to ask for

A CSV (or a pasted table) with one row per funnel step, and optionally per device or channel, for one date range. For example: `step,device,users` with steps such as landing page view, form start, form submit, thank-you view, meeting booked. Ask for the date range if the file doesn't say.

## How to read it

1. Run the funnel calculation on the file. Use its numbers as printed; don't recompute by hand.
2. **Tracking first.** A step larger than the step before it (more thank-you views than submits) means double counting or a step tracked elsewhere. Report it, and don't draw conclusions from that step until it's fixed.
3. **Biggest drop.** Name the transition that loses the largest share, overall and per segment.
4. **Segments.** If one segment (usually mobile) is far worse at the same step, say so with both numbers.
5. **Small numbers.** A step with under 100 behind it is too few to compare or conclude from. Say so.
6. **Tie drops to page facts, as hypotheses.** "Mobile form completion is 12.9% against 30.1% on desktop, and the page has no viewport tag. A likely cause, worth fixing first." Never state a cause as proven.

## What not to do

- Don't project the numbers forward, annualise them or turn them into revenue.
- Don't estimate what the rate would be after a fix.
- Don't compare with an industry benchmark unless the user asks, and then only with a named source, labelled as a benchmark.
- Don't fill a missing step with a guess. Missing stays missing: say which step to add to tracking.
