# The scoring rubric format (icp/scoring.md)

## Contents
- What it's for
- The layout
- The header
- Criteria
- Disqualifiers
- Writing a criterion
- Field names
- How a row is scored
- A complete example

## What it's for

`icp/scoring.md` is the hand-off to whatever builds or scores a prospect list. A person can read and edit it, and the list builder parses it line by line. The grammar below is the one the list builder reads: `Criterion | Points` table rows, points a whole number or `DQ`, and a `Tiers:` line. `scripts/scoring.py` parses, checks, applies and back-tests it with the same rules.

## The layout

```
# ICP scoring rubric: <company>

Version <n>, written <YYYY-MM-DD>. Status: <evidence-based | provisional | user-directed>.
Basis: <records and sources the rubric rests on, with counts>.
Max points: <n> (unknown values score nothing).
Tiers: A 70+, B 50+, C 30+

## Criteria

| Criterion | Points | Evidence |
|---|---|---|
| Locations 5–19 | 40 | 11 of 13 won; 1 of 11 churned |

## Disqualifiers

| Criterion | Points | Reason | Evidence |
|---|---|---|---|
| Locations 20+ | DQ | enterprise security reviews need a SOC 2 report we don't have | 0 of 4 won; brand/offer.md |

## Notes

- Free text. Keep anything the user wrote here.
```

Keep the header lines and Notes ending in a full stop or a word, never a bare number: the list builder reads any line ending in a number as a criterion with points.

## The header

| Part | Meaning |
|---|---|
| Version | Starts at 1; every update adds 1. The previous version is kept in `icp/history/` |
| written | The date the rubric was written |
| Status | `evidence-based`: built from 10+ closed records. `provisional`: no customer data, or under 10 closed records; criteria are hypotheses. `user-directed`: the user chose a weighting the data doesn't support; Notes say what the data shows |
| Basis | What it rests on, with counts: "46 closed records from data/customers.csv (3 open, 1 duplicate excluded); 8 win/loss notes; 3 call notes." Provisional: "no customer data; brand memory only." |
| Max points | The most a row can score: the best criterion on each field, added up. Use 100 |
| Tiers | Highest first. A row's tier is the first one it reaches; below the last tier, don't contact |

## Criteria

- One table row per criterion: the criterion, its points, and the evidence with its count ("10 of 12 won; 1 of 10 churned"), or `provisional`, `assumed` or `user`. Under 10 records, add "hypothesis".
- Points follow the evidence: the segment that wins, stays and pays most gets the most.
- Negative points are allowed for a risk (a churn-prone profile, a competitor's customer).
- Criteria on the same field are alternatives (size bands). Write them so they don't overlap: `Locations 1`, `Locations 2–4`, `Locations 5–19`.

## Disqualifiers

A disqualifier removes a row whatever it scores. Points is `DQ`, and every row has a reason a salesperson would accept. The `## Disqualifiers` heading stays even when the table is empty (say why in Notes).

## Writing a criterion

| Form | Means | Example |
|---|---|---|
| `Field: a, b, c` | the field contains any of the values (whole words, any case) | `Industry: general dentistry, orthodontics` |
| `Field 2–15` or `Field: 2 to 15` | a number in the range, inclusive | `Employees 50–199` |
| `Field 15+` | at or above | `Locations 20+` |
| `Field over 15` | above | `Employees over 200` |
| `Field under 10` | below | `Sales reps under 5` |
| `Field 1` | exactly | `Locations 1` |

Nothing else goes in the Criterion cell: no labels, ids or notes. A judgment ("growing fast") isn't a criterion; turn it into a signal field.

## Field names

The field names a column the list will have. Use plain names the list builder matches by synonym: `Industry`, `Employees`, `Locations`, `Country`, `Province` or `State`, `Revenue`, the tool they use today (`Current scheduling`, `POS`, `CRM`), and `Lead source` only for inbound or CRM lists.

Triggers become signal fields filled yes or no: `Signal new location: yes`, `Signal new ops hire: yes`. Say in the evidence what the list builder should look for (a job post, an announcement).

Use only fields a list builder can fill before first contact. Something learned on a call (budget, pain) belongs in qualification, not in the rubric.

## How a row is scored

1. If any disqualifier matches, the row is disqualified.
2. Otherwise add the points of every matching criterion.
3. The tier is the first one the total reaches.
4. A blank field is unknown: it scores nothing and is listed so someone can fill it.

`python3 scripts/scoring.py apply icp/scoring.md list.csv --out scored.csv` adds `icp_score`, `icp_tier`, `icp_disqualified_by`, `icp_matched` and `icp_unknown`. `backtest` runs the rubric over the customer file and shows tiers against outcomes.

## A complete example

```
# ICP scoring rubric: Pipewise

Version 1, written 2026-10-20. Status: evidence-based.
Basis: 26 closed records from data/deals.csv (2 open excluded); 5 win/loss notes; 1 call note.
Max points: 100 (unknown values score nothing).
Tiers: A 70+, B 45+, C 25+

## Criteria

| Criterion | Points | Evidence |
|---|---|---|
| Employees 50–199 | 40 | 12 of 15 won; 1 of 12 churned |
| Employees 20–49 | 10 | 4 of 9 won in the 10–49 band, 2 of 4 churned (hypothesis) |
| Industry: software | 30 | 12 of 16 won; 2 of 12 churned |
| Industry: manufacturing, logistics | -20 | manufacturing 0 of 3 won, logistics 0 of 1 (hypothesis) |
| Signal new sales leader: yes | 30 | 3 of 3 win notes (hypothesis) |

## Disqualifiers

| Criterion | Points | Reason | Evidence |
|---|---|---|---|
| Sales reps under 5 | DQ | the review needs a manager to run it | brand/offer.md |
```
