# The report, the reply and guided mode

## Contents
- positioning.md
- The reply
- Guided mode
- No pages
- Writing rules

## positioning.md

Save it to `audits/<domain>/positioning.md` (no domain: a short slug of the company name). Keep it under about 1,200 words. The full audit links to it, so the sections and their order never change. If a section has nothing to report, keep the heading and say so in one line.

```
# Positioning: <Company>
<date> · <business type> · <maturity> · Pages reviewed: <list> · Brand memory: <the company's | none, so this is provisional> · Competitor pages: <list | none>

## Verdict
<checklist total>/100 on the positioning checklist · <one line: the move>

## The three findings that matter most
1. **<finding>.** Evidence, <page>: "<quote>". Fix: <a concrete change someone can make this week>.
2. …
3. …
(Fewer than three real problems? List only those and say so. Strengths you'd protect can fill the space, labelled as strengths. On a strong site (total 80 or more) the first line says it's strong and what to protect, and no finding is high severity unless a check scored 0.)

## Who it's for, and who it's not
## Category frame
## Problem and the alternative
## Differentiated value and proof
## Consistency across pages
| Page | Headline | Audience | Core benefit | CTA label |
## Specificity and the swap test
(Each main claim: specific or generic, quoted. Then the named swap test, or "Not run: no competitor pages supplied. Send their home pages to run it.")

## Headline options
**A.** Headline: "…" · Subhead: "…"
Built from: <fact IDs or quotes with pages>
**B.** …
(Recommend one. If the current headline already scores full on P1, recommend keeping it and label these as optional tests.)

## Plan
- Next 48 hours: <1–3 actions>
- Next 2 weeks: <2–4 actions>
- Next 3 months: <2–4 actions>

## Not observable
<what pages can't show: how buyers actually compare options, win/loss reasons, which message converts>, and what would show it.

## Checklist score (same checks as the full marketing audit)
| Check | Points | Evidence |
|---|---|---|
| P1 Headline says what it is | x/20 | quote, page |
| P2 Audience named | x/20 | … |
| P3 Differentiation from the alternative | x/20 | … |
| P4 Consistency across pages | x/20 | … |
| P5 Claims supported | x/20 | … |
| **Total** | **x/100** | Positioning is 25% of the full audit's score. |
(If a full audit already ran: "Previous checklist: <old>. Full audit total moves from <old> to <new> when re-scored.")
```

Each lens section is 2–5 lines: the answer, the quotes behind it, and the fix if there is one. Don't restate the three findings.

## The reply

Short, under about 250 words, in this order:

```
**Positioning: <total>/100** · <the move, one line>

**The three findings**
1. <one line, with the quote that proves it>
2. …
3. …

**Next 48 hours:** <the actions>
**Headline to test first:** "<headline>" / "<subhead>"
**Not run or not observable:** <one line: swap test without competitor pages, buyer comparisons, anything you declined and why>
Report: audits/<domain>/positioning.md
```

When you declined part of the request (a comparative claim without evidence, an invented figure), say so in one or two sentences in the reply, say what would make it possible, and point to the defensible option you gave instead.

## Guided mode

Use it when the user asks to be walked through it, to make the calls, or to see it before anything is written. Write no files. Reply with:
1. The pages read and whose brand memory, if any.
2. A provisional checklist (P1–P5 with one quote each) and the main findings, each quoted.
3. At most five questions, each a call that's theirs: which audience to lead with when pages disagree, whether an unsubstantiated claim stays in the headline until proof arrives, whether a named competitor's pages are available for the swap test, anything brand memory leaves `TBD`. Count the question marks: no rhetorical questions elsewhere in the reply.
4. One line: "Once you answer, I'll write the report and the headline options."

## No pages

If no pages were supplied and you can't fetch them, don't write a report. In under about 120 words: say you can't review a site you haven't read, ask for the home, pricing and about pages (saved HTML, pasted copy, or browsing access), and list what the deep dive will cover. Say nothing about what the company does, even if its name suggests it.

## Writing rules

- Lead with the verdict, not the method.
- Quote evidence; don't paraphrase it. Name the page.
- Fixes are concrete edits ("move 'Built for independent restaurants and small groups (1–15 locations)' into the H1"), not principles ("clarify your audience").
- Be fair. Name real strengths. A site with good positioning gets told so in the first line.
- Match the company's spelling in the report and the reply too: its brand memory's convention, or with none, the site's own (a US site gets US spelling), never your environment's default.
- Give the report path relative to the project folder (`audits/<domain>/positioning.md`), never a full machine path.
- No scoring jargon beyond the checklist table: say "brand consistency" or "conversion", never a check code such as B2 or C1. No mention of how the report was produced, of any tool or script, or of internal file names other than the report's own path.
- No traffic, conversion or benchmark figures. No facts about competitors beyond their supplied pages.
