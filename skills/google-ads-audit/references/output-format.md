# Output and hand-off formats

## Contents
- AUDIT.md
- fixes.md (read by google-ads-build)
- The reply
- Guided mode checkpoint

## AUDIT.md

Path: `audits/google-ads/<account>/AUDIT.md`, where `<account>` is the business name in lowercase with hyphens. Sections in this order, all present even when short:

```markdown
# Google Ads audit: <Account>

**Score: <n>/100 (<grade>)<on Low confidence add ", provisional: low confidence"> · Confidence: <High|Medium|Low> (<days> days, <n> real conversions) · <start> to <end> · Spend <$total>**
<One sentence: the recommendation. What to do first and why.>
<If no brand memory: "Provisional: written without brand memory; relevance and brand-rule judgments are marked as assumptions.">

## Top three findings
1. **<Finding in plain words>.** Evidence: <the numbers and names from the export>. Fix: <the concrete change>. At stake: <$ from the script, or "no dollar figure: <why>">.
2. …
3. …

## Scorecard
| Check | Status | Key number |
|---|---|---|
| Conversion tracking | FAIL | <the key figure, e.g. "x of y conversions are page views"> |
… all 11 rows, in the order of references/checks.md, including NOT CHECKED and INSUFFICIENT DATA rows …

## Findings by check
### 1. Conversion tracking
<What the data shows, quoted figures, why it matters, the fix.>
… one subsection per check, same order; a PASS gets one line …

## Plan
**Next 48 hours:** <settings and tracking fixes that stop loss now: negatives, Display off, Presence, demote non-outcome actions>
**Next 2 weeks:** <restructure, ad and asset rewrites, landing page changes, budget moves>
**Next 3 months:** <re-run the audit on clean conversion data; bid strategy changes once volume supports them; tests>

## Not checked
<Each check or judgment that couldn't run and the export or fact that would let it. "Nothing" if all ran.>

## Sources and assumptions
- Exports: <file names, date range>
- Brand memory: <files read, or "none: provisional">
- Assumptions: <each one, labelled>
- Rules of thumb used: <thresholds, labelled as this audit's, not Google's>
- Read-only: no changes were made to the account.
```

Rules for the report:
- Every dollar figure comes from the script output. A sum of figures is fine (state the parts). No projections: no "per year", "per month" or "if you fix this you'll get…" figures, ever. On a short export say "in these <n> days".
- Every finding names the campaign, ad group, keyword, term or setting, with its number.
- Top three: the three with the most money or the most risk at stake, tracking first when it's broken (every other number depends on it).
- Recommend doing nothing where nothing is wrong. A PASS check gets one line.

## fixes.md (read by google-ads-build)

Path: `audits/google-ads/<account>/fixes.md`. Exact shape:

```markdown
# Fixes: <Account>
Source: AUDIT.md (<YYYY-MM-DD>) · Date range: <start> to <end> · Confidence: <High|Medium|Low>

1. [P1] negatives · <terms> cost <$> with 0 conversions; <existing negative and why it misses them> · Add "<word>" as a phrase-match negative to <campaign or shared list>
2. [P1] settings · Display Network is on in <campaign>: <$>, <n> conversions · Turn off Display Network in <campaign>
3. [P2] ads · … · … (confirm first)

## Account facts
- Budgets: <campaign: $/day> …
- Geo: <locations, Presence or Presence or interest, per campaign>
- Networks: <per campaign>
- Bid strategies: <per campaign, with targets>
- Conversion actions: <name: primary/secondary, category>
- Brand terms: <list, or TBD: confirm brand terms>
```

- One line per fix: `<n>. [P1|P2|P3] <area> · <problem with evidence and $> · <fix naming the campaign/ad group and the exact value>`.
- Areas, exactly: structure, keywords, negatives, ads, assets, settings, budget, tracking, landing.
- P1 = next 48 hours, P2 = next 2 weeks, P3 = next 3 months (same as the plan).
- One negative or one setting per line where practical. Negatives always state the match type and the level (campaign, ad group, or shared list).
- End a fix with `(confirm first)` when it needs a human decision: a borderline term, a budget increase, a bid strategy change, anything depending on an assumption. google-ads-build holds those.
- Account facts hold only facts from the export or brand memory; unknowns are `TBD: <what's missing>`.

## The reply

Under 250 words unless the user asked for more. Second person.

```
**<Score>/100 (<grade>), confidence <level>.** (On Low, say the score is provisional and why.) <The recommendation in one sentence.>

**Top three**
1. <finding> · <$ or number> · <fix>
2. …
3. …

**Do in the next 48 hours:** <2–4 items>

<Where the files are: "Full audit and a fixes list are in audits/google-ads/<account>/.">
<Not checked / provisional / one question, only if needed.>
```

Never mention the scripts, their output, statuses as code words, or file internals beyond the two file names.

## Guided mode checkpoint

Guided mode stops once, after the script's first run and before any dollar figure goes in a report:

```
**Before I put numbers in the report, three things to confirm:**

1. **Brand terms:** I'll treat <terms> as brand searches. Anything to add (misspellings, product names)?
2. **Search terms I'd count as waste** (<n> terms, $<script total>):
   - "<term>" · $<cost> · <reason, citing brand memory where it applies>
3. **Borderline, your call** (not counted yet):
   - "<term>" · $<cost>, <conversions> conversions · <why it's unclear>

Reply with changes, or "go ahead".
```

Write no AUDIT.md or fixes.md until they answer. Draft mode (the default) makes these calls itself, lists borderline terms as excluded from the waste total, and finishes.
