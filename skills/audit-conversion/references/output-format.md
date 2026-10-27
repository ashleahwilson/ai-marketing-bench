# Output format

## Contents
- conversion.md
- dim-conversion.json
- The test backlog
- The reply
- Writing rules

## conversion.md

Save to `audits/<domain>/conversion.md`. Use the domain from the canonical tag or the user; if there's none, a short slug of the company name. Keep it under about 1,500 words: trim page-by-page detail first, never the top three or the plan. Sections, in this order, with these exact headings:

```
# Conversion audit: <Company>
<date> · <business type> · <maturity> · Pages reviewed: <n> · Confidence: <High|Medium|Low> · <"Provisional: no brand guidelines on file", if so>

## Verdict
Conversion checklist score <total>/100. <One sentence: the single change that matters most, or "No changes needed" for a sound page.>

## The three findings that matter most
1. **<finding>** Evidence, <page>: "<quote>". Fix: <a concrete action someone can start this week>.
2. …
3. …
(Fewer than three only when the pages are sound. Never pad.)

## Page by page
### <page file or path> · primary action: "<CTA text>" → <destination>
- <area>: "<quote or markup fact>". <issue, or "fine">. Fix: <action>.
(One block per page. A sound page gets one line.)

## Forms
Per form: fields (required / optional), labels, input types and autofill, error handling seen in the HTML, submit text, privacy notice near it, what-happens-next text.

## Funnel
With an export: the step table, the biggest drop, segments, tracking problems, and which page facts might explain each drop (labelled as hypotheses). Without one: "Not observable: no analytics export supplied. Send <the steps and a date range> to see where visitors drop off."

## What's working
Real strengths, each with a quote.

## Plan
- Next 48 hours: <1–3 actions anyone can do now>
- Next 2 weeks: <2–4 actions>
- Next 3 months: <1–3 actions>

## Test backlog
| # | Hypothesis | Change | Metric |
|---|---|---|---|

## Not observable and how this was done
What couldn't be seen (conversion rates without analytics, rendered layout, load times, what happens after submit), the pages reviewed and missing, how business type and maturity were judged, and why the confidence is what it is.

## Conversion checklist score
| Check | Points | Max | Evidence |
|---|---|---|---|
| C1 Primary CTA | … | 20 | … |
| C2 Path to a lead | … | 20 | … |
| C3 Form friction | … | 20 | … |
| C4 Pricing clarity | … | 15 | … |
| C5 Trust at the decision point | … | 15 | … |
| C6 Mobile ready | … | 10 | … |
**Total: <sum>/100**
<If an earlier conversion score exists: "Earlier score <n>/100. Changed: C3 20 → 0 (the earlier score used the demo form; the trial signup is the primary path and requires phone, revenue and card)." One line per changed check.>
```

**Confidence:** High with 4 or more HTML pages including the page with the primary form; Medium with 2–3 pages, or when the primary form's page is missing; Low with one page, markdown only, or any check scored "not observable".

**The plan's horizons** match the full audit (48 hours, 2 weeks, up to 3 months), so its actions can merge into a later full report. Each action names the page and the change.

## dim-conversion.json

Write `audits/<domain>/dim-conversion.json` in the full audit's format so the overall Marketing Health score can use it directly:

```json
{"dimension": "conversion", "assessable": true, "confidence": "high|medium|low",
 "checks": [{"id": "C1", "points": 10, "max": 20, "evidence": "…"}, "… C2 to C6"],
 "score": 0,
 "findings": [{"severity": "high", "check": "C3", "finding": "…", "evidence": "…", "fix": "…"}],
 "strengths": ["…"], "not_observable": ["…"], "pages_reviewed": ["…"]}
```

`score` is the sum of the points. Findings are the checklist findings (3–5, worst first); deep-dive findings that don't move a check stay in `conversion.md`.

**An earlier dim-conversion.json exists?** Read it first. Before writing yours, copy it to `audits/<domain>/history/dim-conversion-<date>.json`, so the earlier audit stays intact. List every check whose points changed, old → new, with the reason, in the checklist section and in the reply.

## The test backlog

Three to six rows, highest-stakes first. Each row:
- **Hypothesis:** what you think is happening and why, tied to a quoted page fact ("Visitors who clicked 'no credit card required' abandon when the signup asks for a card").
- **Change:** the one thing to change.
- **Metric:** the step that should move, named so it can be read from their analytics (for example `form_start → form_submit` on mobile, trial signups per signup-page visit).

Never a predicted lift, expected percentage, confidence of winning or number of extra leads. Nobody can know it from the pages, and a guessed number gets repeated in a board deck as a promise.

**Fixes aren't tests.** A broken promise, a missing viewport tag or a required phone field gets fixed, not A/B tested. The backlog is for changes where the answer is uncertain (one CTA vs two, form on page vs separate page).

**Low traffic:** if an export shows a step with under a few hundred visitors a month, say a split test would take too long to read, and suggest making the change and comparing the same funnel step before and after over equal periods.

**A sound page** may need no backlog. Say "Nothing worth testing until there's an analytics baseline" rather than inventing tests.

## The reply

Short, under about 250 words. It covers:
1. **Conversion checklist score <total>/100** and the one-line verdict.
2. The three findings, one line each with the fix.
3. The 48-hour actions.
4. What wasn't observable, and the data that would fill it.
5. Where the files are, and any score changes from an earlier audit.

If the user asked for a predicted conversion rate or lift, answer that first, in two or three sentences: it can't be predicted from the pages; what can be done instead (measure the current rate for the primary step from their analytics over a fixed period, make the changes, and compare the same step over an equal period). Then the audit. Don't lecture.

Don't paste the report into the chat.

## Writing rules

- **Lead with the decision.** The verdict line, then evidence.
- **Quote, don't paraphrase,** and name the page.
- **Fixes are concrete** ("Cut the signup to name, email, password and store URL; ask for phone on the onboarding call"), not principles ("reduce friction").
- **Suggested CTA or button text uses words already on the site.**
- **No numbers that weren't observed.** No conversion rates, benchmarks or lifts unless they come from the user's export (benchmarks only with a named source, labelled as a benchmark).
- **Spelling follows the client.** With brand memory, its voice file. Without one, the spelling the site itself uses, even if your environment prefers another.
- **Talk about the site, not the method.** No script names, check levels or file internals in the report or the reply.
