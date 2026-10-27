# The report

## Contents

- brand.md
- dim-brand.json
- Quick read
- Writing rules

## brand.md

Save it to `audits/<domain>/brand.md` (no domain: a short slug of the company name). Keep it under about 1,200 words. If it runs long, cut detail inside the sections, never the top three, the plan or the score. Sections, in this order, always present (write "Nothing to report" or "Not assessed: <reason>" rather than dropping one):

```
# Brand audit: <Company>
<date> · <maturity> · Pages and pieces reviewed: <n> · Brand memory: <the company's | none | <owner>'s, not used> · Confidence: <level>

## Verdict
<one line: what to do, e.g. "Consistent and credible: protect it, fix two small gaps." or "Fix the about page and the banner before adding new channels.">
Brand score: <total>/100 (B1–B5 below). <If recomputed: Marketing Health <old> -> <new>, Grade <letter>.>

## The three things that matter most
1. **<finding>.** Evidence, <page>: "<quote>". Fix: <action>.
2. …
3. …
(For a clean brand: the strengths to protect, and at most one or two low findings.)

## Voice
| Piece | Words | Avg sentence | Contractions /100 | Person | Spelling | Notes |
<one row per page or post, then 2–4 lines on what's consistent and what breaks, quoted>

## Naming and terminology
<each term with more than one form: the forms, where, and the form to use; or "Consistent: <names checked>">

## Proof and trust
<proof items and trust signals by page, credible or weak, with quotes; what's missing; anything asked for that isn't observable>

## Against brand memory
<the gap analysis, each breach quoting the brand-memory line and the page line; or "No brand memory for <Company>: findings are judged against the site's own voice and are provisional. The voice rules found here can be recorded as a brand memory on request"; or "The brand/ folder belongs to <owner>, not <Company>, so it wasn't used">

## What can't be judged from words
<logo, colour palette, typography, imagery; alt text and titles if no HTML; what would close each gap>

## Plan
- Next 48 hours: <1–3 actions anyone can take now>
- Next 2 weeks: <2–4 actions>
- Next 3 months: <2–3 actions>

## Brand score (marketing audit checklist)
| Check | Points | Max | Evidence |
|---|---|---|---|
| B1 Voice consistency | … | 25 | … |
| B2 No message drift | … | 25 | … |
| B3 Proof credibility | … | 20 | … |
| B4 Asset care | … | 20 | … |
| B5 Matches brand memory | … | 10 | … |
| **Total** | **…** | **100** | |
<If an earlier score exists: "Earlier brand score: <n>. Changed: <checks and why>.">

## How this was done
Pages and pieces reviewed, page types missing, how maturity was classified, confidence and why, and that only words and markup were assessed.
```

**Confidence:** under 4 pages and pieces reviewed, Low; 4–5, Medium; 6 or more, High. Drop one level if the main pages (home and about) are missing.

## dim-brand.json

Save it beside the report. It's the marketing audit's dimension format, with one extra key, so a later full audit can reuse it:

```json
{"dimension": "brand", "assessable": true, "confidence": "high|medium|low",
 "brand_memory": "company|none|auditor",
 "checks": [{"id": "B1", "points": 12, "max": 25, "evidence": "about.html: no contractions, 'Tallyhouse Inc. is committed to…'; every other page says we and you"},
            {"id": "B2", "points": 0, "max": 25, "evidence": "…"},
            {"id": "B3", "points": 10, "max": 20, "evidence": "…"},
            {"id": "B4", "points": 10, "max": 20, "evidence": "…"},
            {"id": "B5", "points": 0, "max": 10, "evidence": "…"}],
 "score": 32,
 "findings": [{"severity": "high", "check": "B2", "finding": "…", "evidence": "…", "fix": "…"}],
 "strengths": ["…"], "not_observable": ["logo", "colour palette", "…"]}
```

If `dim-brand.json` already exists, copy it to `audits/<domain>/history/dim-brand-<date>.json` first.

## Quick read

In chat only, no files. Under 200 words, counted before you reply:
- One line on the brand as it reads now, and the likely maturity.
- A rough brand score out of 100, marked "quick read" (a full audit can move it by 10 points or so).
- The two findings that matter most, each with a quoted line and its page.
- One question to ask on the call.
- Whether a full brand audit is worth running.

## Writing rules

- **Lead with the decision,** not the method.
- **Quote, don't paraphrase,** and name the page or post.
- **Fixes are actions someone could start this week** ("rewrite the about page's first paragraph in 'we' and 'you', in short sentences"), not principles ("align the tone").
- **Be fair.** Name real strengths. An audit that finds nothing good won't be believed, and one that invents problems on a clean brand won't either.
- **The client's spelling** in quotes and recommended fixes. The report's own prose follows the user's house style.
- **No invented numbers:** no traffic, review scores, customer counts or benchmarks that weren't observed.
- **Talk about the business,** never about scripts, file internals or tools.
