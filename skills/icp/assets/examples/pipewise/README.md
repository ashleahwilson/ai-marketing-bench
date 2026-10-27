# Worked example: Pipewise

Pipewise (fictional) sells a weekly pipeline review to B2B sales teams. The founder exported 28 deals and asked who to go after and for a rubric the list builder can use.

| File | What it is |
|---|---|
| [request.md](request.md) | What the user asked |
| [data/deals.csv](data/deals.csv), [data/win-loss.md](data/win-loss.md), [data/calls.md](data/calls.md) | The evidence |
| [brand/offer.md](brand/offer.md) | Brand memory: the "under 5 reps" exclusion |
| [icp/history/audiences-2026-10-20.md](icp/history/audiences-2026-10-20.md) | The audiences file before the update, kept |
| [brand/audiences.md](brand/audiences.md) | The audiences file after: segments with counts, a trigger, exclusions, personas with source tags |
| [icp/scoring.md](icp/scoring.md) | The rubric the list builder reads |
| [reply.md](reply.md) | The reply the user sees |

What to notice:
- Every number carries its count, and percentages appear only where 10+ deals sit behind them.
- The 10–49 employee and manufacturing findings rest on under 10 deals, so they're labelled hypotheses and weighted lightly instead of becoming hard exclusions.
- The second persona has no recorded conversation, so its fields are `TBD` with a way to fill them. No quote is written for it.
- The rubric was back-tested on the company's own deals before it was handed over.
