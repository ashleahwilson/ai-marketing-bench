# Rubric format

The ICP scoring rubric lives at `icp/scoring.md`. The skill that defines the ICP writes it; this skill reads it. It's plain text so a person can edit it too.

## Contents
- The format to write
- Other forms that are read
- What can be scored
- Rewording lines that can't be scored
- Tiers
- Criteria from somewhere else

## The format to write

One criterion per line: `criterion | points`. A Markdown table with the same two columns also works.

```
# ICP scoring: <company>

Written <date> from <source>. Owner: <name>.

| Criterion | Points |
|---|---|
| Locations: 2–15 | 30 |
| Locations: 1 | 15 |
| Country: Canada | 20 |
| POS: Toast, Square, Lightspeed | 25 |
| Title: owner, controller, finance | 15 |

## Disqualifiers

| Criterion | Points |
|---|---|
| Locations over 15 | DQ |
| Industry: retail, e-commerce | DQ |

Tiers: A 70+, B 45+
```

- **Points** are whole numbers. Negative points subtract. `DQ` (or disqualify, exclude) removes the account.
- Lines under a heading that contains "Disqualifiers", "Exclusions" or "Knockouts" are DQ even without a points cell.
- The criterion names a field that matches a column in the data, then the values.

## Other forms that are read

- `- Locations 2–15: +30` and `+30 Locations 2–15` (bullets)
- `Locations 2-15 | 30` (no table)
- `Disqualify: Platform: WooCommerce` (a DQ line)
- Headers and blank lines are ignored, and so are lines with no points outside a disqualifier section.

## What can be scored

| Criterion form | Means | Example |
|---|---|---|
| `Field: a, b, c` | the field contains any of the values (whole words, any case) | `POS: Toast, Square` |
| `Field 2–15`, `Field: 2 to 15`, `between 2 and 15` | number in the range | `Employees 50-500` |
| `Field 15+`, `at least 15`, `15 or more` | number at or above | `Monthly orders 1000+` |
| `Field over 15`, `more than 15`, `> 15` | number above | `Locations over 15` |
| `Field under 10`, `less than 10`, `< 10` | number below | `Dentists under 3` |
| `Field 1` | exactly that number | `Locations 1` |

- **Fields** match a column by name, ignoring case and punctuation, with common synonyms: locations (sites, units, outlets), employees (headcount, staff), title (role, job title), province (state, region), POS (point of sale).
- **Title** criteria check every contact on the account who hasn't been suppressed.
- **Country** values are normalized (CA, Canada, CAN are the same; US, USA, United States are the same).
- **A blank field** is unknown, never a fail. Its points go into `max_possible` and the field is listed as missing.
- **A value that straddles a range** (employees "11-50" against "20+") is treated as unknown.

## Rewording lines that can't be scored

When a line can't be read, or names a field no column holds, write `lists/<name>-criteria.md` in the format above and score from that. Each line ends with where it came from:

```
Country: US, Canada | 15 | from icp/scoring.md "North America | 15"
CRM: Salesforce, HubSpot | 25 | from icp/scoring.md "Uses Salesforce or HubSpot | 25"
```

- Reword only when the meaning is clear. "North America" means US and Canada (and Mexico if the user sells there: ask if unsure).
- A judgment line with no column ("Growing fast", "Good culture fit") isn't scored. Propose a stand-in from a real column ("Last funding: 2026, 2025" or "Employees growing" if there's a growth column) and get approval before using it. Until then, list it as not scored.
- Never edit `icp/scoring.md`.

## Tiers

`Tiers: A 70+, B 45+` sets the thresholds. Without a tier line, A is 70% of the maximum possible score and B is 40%; everything else is C. Accounts whose `max_possible` would reach a higher tier are flagged "could reach tier A once missing data is filled".

## Criteria from somewhere else

- **The user's message:** write them as rubric lines in `lists/<name>-criteria.md`, citing "from your message". Use even points unless the user ranks them.
- **Brand memory only:** `audiences.md` segments become positive lines and "Not for" or `offer.md` "We don't do" lines become DQ lines. Mark the list provisional and say the weights are a starting point.
