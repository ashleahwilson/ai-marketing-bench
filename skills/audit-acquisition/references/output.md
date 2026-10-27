# The acquisition file and the reply

## Contents
- acquisition.md
- Quick read (chat only)
- The reply
- Writing rules

## acquisition.md

Save it to `audits/<domain>/acquisition.md` (no domain: a short slug of the company name). It may be shared with the company, so it never names tools, scripts, files other than the pages, or process. Keep it under about 1,500 words. Sections, in this order, all present even when one is short:

```
# Acquisition audit: <Company>
<audit date> · <business type> · <maturity> · Pages reviewed: <n> · Data: <none supplied | Search Console export, <period>> · Confidence: <High|Medium|Low>

## Verdict
<one line: the decision. With a blocker: "Fix indexing before anything else: <page> is set to noindex.">
Acquisition checklist score: <n>/100<, plus " · Blocker: <one line>" if any>

## Top three findings
1. **<finding>.** Evidence: <quote or measured fact, page>. Fix: <concrete action>.
2. ...
3. ...

## Indexability and on-page basics
<per-page table: Page | Title (chars) | Meta description | H1 | Canonical | Robots | Links in>
<robots.txt and sitemap: what they show, or "not supplied, not checked">
<up to 4 more findings, one line each>

## Buyer questions and content
<newest dated content and its age> <whether content answers buyer questions> <3-5 proposed topics, each a buyer question tied to a site or brand fact>

## AI search and answer engines
<the quotable what-we-do-for-whom sentence, or where it's buried> <FAQ> <structured data found and what to add, using only page facts>

## Local listings
<per-location NAP, hours, map, structured data; or "Not a local business: not assessed.">

## Channels
<kinds visible, quoted; what's missing for this type and maturity>

## Search data
<from the export: branded split, CTR by position band, pages losing clicks, impressions without clicks, each with the period; or "No Search Console or analytics export supplied: traffic, rankings and queries not assessed.">

## Checklist score
| Check | Points | Evidence |
|---|---|---|
| A1 Titles and meta descriptions | x/20 | ... |
| A2 On-page structure | x/15 | ... |
| A3 Answer-engine readiness | x/15 | ... |
| A4 Content engine | x/20 | ... |
| A5 Channel evidence | x/15 | ... |
| A6 Navigation and linking | x/15 | ... |
| **Total** | **n/100** | <maturity relief, if applied> |
<If an earlier full audit exists: earlier score -> new score, why each changed check moved, and the overall score and grade it would produce.>

## Plan
- Next 48 hours: <1-3 actions; any blocker fix goes here first>
- Next 2 weeks: <2-4 actions>
- Next 3 months: <2-4 actions>

## Not observable
<traffic, rankings, search volume, and whatever else couldn't be seen, each with the data that would show it>

## How this was done
<pages read; robots.txt, sitemap and exports supplied or not; how maturity was classified; why the confidence>
```

**Confidence:** High with 6 or more pages and the key pages present; Medium with 4-5 pages or a key page missing; Low under 4 pages, or with copy only (no HTML, so titles, robots meta, canonical and structured data can't be checked: mark A1 and A2 as not assessable rather than guessing, and say the score covers the remaining checks only).

**Choosing the top three:** blockers first, then by severity, then by how many searches the fix touches (key pages before minor pages), then by how fast it can be done.

## Quick read (chat only)

For "quick read", "before my call", "in 10 minutes": one pass over what's supplied, no files written. Under about 200 words:
- One line on what the business is and its likely maturity.
- Any blocker, first.
- The two findings that matter most, each with its evidence.
- What isn't observable, if the user asked for it (traffic, rankings), and what would show it.
- One question to ask on the call that would surface the missing data.

## The reply

Short. It covers, in order:
1. The verdict line and the checklist score (and any blocker).
2. The three findings, one line each.
3. The 48-hour actions.
4. Where the files are.
5. What wasn't observable, and what data would raise confidence.

Don't paste the full file into chat. If the user asked for something the audit won't do (a ranking guarantee, traffic numbers with no data), say so in one or two sentences in the reply, give the alternative, and carry on with the audit.

## Writing rules

- Lead with the decision, not the method.
- Quote evidence; don't paraphrase it. Name the page.
- Fixes are actions someone could start this week ("add a meta description to /pricing: ..."), not principles ("improve metadata").
- Name real strengths. An audit that finds nothing good won't be believed.
- Every number traces to a page, the measured page facts, the score, or a supplied export with its period.
- No promises about rankings, traffic or AI citations. Commit to actions and to what will be measured.
- If the business has no brand memory, keep its own spelling and conventions in suggested copy.
