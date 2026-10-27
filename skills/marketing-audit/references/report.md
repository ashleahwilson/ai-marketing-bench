# The report

## Contents
- MARKETING-HEALTH.md
- The one-pager
- Triage output
- Writing rules

## MARKETING-HEALTH.md

Save it to `audits/<domain>/MARKETING-HEALTH.md`. Keep it under about 1,000 words: the per-dimension detail lives in the `dim-*.json` files. If a draft runs long, cut the "By dimension" findings to the top one or two, never the top three or the plan. Use the script's action line as written, because it names the weakest dimensions. Sections, in this order:

```
# Marketing Health: <Company>
<date> · <business type> · <maturity> · Confidence: <level>

## Score
<total>/100 · Grade <letter> · <the grade's action, one line>

| Dimension | Weight | Score | Headline |
|---|---|---|---|
| Positioning | 25% | … | one line |
| Acquisition | 20% | … | … |
| Conversion | 20% | … | … |
| Brand | 15% | … | … |
| Measurement | 20% | … | … |

## The three things that matter most
1. <finding, evidence, fix>  (highest severity, highest weight first)
2. …
3. …

## By dimension
### Positioning
Strengths (one line) · Up to 3 findings, one line each (severity, evidence, fix) · Not observable (one line)
… (repeat for each dimension)

## Plan
- Next 48 hours: <1–3 actions anyone can take now>
- Next 2 weeks: <2–4 actions>
- Next 1–3 months: <2–4 actions>

## How this was scored
Pages reviewed, pages missing, what wasn't observable, how the classifications were made, confidence and why.
```

## The one-pager

Save it to `audits/<domain>/one-pager.md`. It's for sharing with the company: under about 250 words, with no scoring jargon beyond the grade.
- The score and grade.
- Three findings, each one line with its fix.
- What the first 48 hours should be.
- One line on how the audit was done.

## Triage output

Return it in chat; don't save files. Under about 200 words:
- One line on what the company is and its likely maturity.
- A rough grade (A–F, marked "triage"), with a note that a full audit can move it by one band.
- The two findings that matter most, each with evidence.
- One question to ask on the call.
- Whether a full audit is worth running.

## Writing rules

- **Lead with the decision,** not the method.
- **Quote evidence;** don't paraphrase it.
- **Name the page.**
- **Fixes are concrete actions** someone could start this week ("cut the form to 4 fields: name, email, restaurant, locations"), not principles ("reduce friction").
- **Be fair.** Name real strengths in each dimension. An audit that finds nothing good won't be believed.
- **The confidence label is the script's.** It already accounts for how many pages were reviewed. Don't print "High" and then hedge it in prose.
- **Don't invent numbers.** No traffic, conversion rates or benchmarks presented as their data. Industry benchmarks are labelled as such, with their source.
