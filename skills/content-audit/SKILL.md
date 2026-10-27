---
name: content-audit
description: Audits an existing content library (blog posts, guides, landing pages) from what the user supplies, such as a CSV export of URLs with metrics, a sitemap or a folder of the posts, and decides for every piece whether to keep, update, merge, redirect or remove it, with the reason and the evidence. Finds pieces competing for the same keyword or topic, facts brand memory says have changed (old prices, discontinued offers, held claims, withdrawn proof), pieces that serve no audience, and topic gaps against the audiences in brand memory. Never estimates traffic it wasn't given; with no metrics it decides only what the content supports. Writes a prioritized action list, audits/content/inventory.csv and audits/content/AUDIT.md, and never deletes or edits the content. Use when the user wants a content audit, inventory or pruning, "what should we cut", "which posts are outdated", "are our posts competing", "should we keep this post", or topic gaps to brief. Not for checking a draft before publishing, or writing posts.
license: MIT
compatibility: Tested on large and small models. In the final round one large-model run described page titles it hadn't seen (export and sitemap only); 1.2.1 adds a rule for this that isn't yet re-tested. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Content audit

Decides what happens to every piece in a content library, and proves each decision with the user's own numbers and brand memory. It doesn't delete, rewrite or redirect anything itself. It hands over a list someone can act on.

## Ground rules

1. **Never invent a metric.** Every sessions, clicks, conversions or impressions figure comes from the export, exactly as written. No estimates, projections, "likely" traffic, search volumes or rankings. If a metric wasn't supplied, say so once and decide without it.
2. **Missing stays missing.** With no metrics, decide only what the content itself supports (a wrong price, a duplicate, a dated announcement) and mark the rest `needs data`, naming the data that would decide it. With no brand memory, facts can't be checked against it: say so, and mark the audit provisional.
3. **Low traffic is not a reason on its own.** Before anything is removed, check its conversions, notes (sales use, links from emails), age and audience. A page with conversions, a sales use, or published under six months ago is never removed. Merge or redirect a piece that has an equivalent, so its links and visitors land somewhere.
4. **Brand memory decides what's true.** A price, offer, claim or quote in a piece is checked against `brand/`. A figure that matches only a history, discontinued or withdrawn line is outdated, even if the same number is current elsewhere for something else (read the sentence: "$299 for a single location" is not the "$299 per location" group rate).
5. **Push back with evidence, not refusal.** If the user asks for a blanket rule ("delete everything under 100 sessions"), don't apply it blindly and don't refuse. Show which pieces the rule would wrongly catch and why, and give them the list that's safe to act on.
6. **Never touch the content or the user's files.** Never delete, move or edit posts, the export or the sitemap, even when asked to "delete them": the deliverable is the list. Reports go in `audits/content/`. If an earlier `inventory.csv` or `AUDIT.md` is there, copy it to `inventory.prev.csv` / `AUDIT.prev.md` before writing.
7. **Describe only what you read.** With an export or sitemap and no posts, you have URLs and numbers, not titles or text: never say what a page "says", "promises" or is titled unless the export has a title column or you read the post. Say "the URL suggests…" and that the page itself wasn't checked.
8. **Don't invent problems either.** A piece that converts, is current and serves an audience is `keep`. Text overlap alone is a prompt to look, not a reason to merge.

## Pick the mode

| The user wants… | Mode |
|---|---|
| An audit, an inventory, "what should we keep or cut" (the default) | **Draft:** decide every piece, write both files, reply with the top actions |
| To make the calls themselves: "walk me through it", "I want to decide the merges", "before you write anything" | **Guided:** fact fixes are stated, not asked. Merges, redirects, removals and `needs data` items become numbered questions, each with the sessions (or clicks) and conversions of every piece it names, and your recommendation. Write only `audits/content/inventory-draft.csv` until they answer |
| Only topic gaps: "what are we missing", "what should we write next" | **Gaps:** steps 1, 2 and 4; write `audits/content/AUDIT.md` with the Topic gaps and How this was done sections (a later full audit fills the rest). Always write the file: the gaps are the hand-off for briefs |
| A verdict on one or two pieces: "should we keep this post?" | **Check:** decide those pieces only, in the reply, under 200 words. No files unless asked |
| A blanket rule ("delete everything under X") | **Draft**, leading with what the rule would get wrong (rule 5), in a short reply |

## Workflow

```
- [ ] 1. Load: export, sitemap, posts folder, brand/, any earlier audit in audits/content/
- [ ] 2. Run scripts/audit_content.py (analysis + draft inventory)
- [ ] 3. Decide every piece with judgment (references/judgment.md)
- [ ] 4. Find topic gaps against brand/audiences.md and offer.md
- [ ] 5. Prioritize the top 10
- [ ] 6. Write inventory.csv and AUDIT.md (references/output.md), then run the check
- [ ] 7. Reply in the fixed shape
```

### 1. Load

List the project folder recursively before saying anything is missing. Find: a CSV export (any column names: the script maps "Sessions (90 days)", "Clicks", "Key events", "Top pages" and the like), a sitemap (`sitemap.xml`), a folder of posts (`.md` or `.html`), and `brand/` (`offer.md`, `audiences.md`, `proof.md`, `claims.md`, `rules.md`). Note the export's period from its column names or the user's message. If `audits/content/` already holds an audit, this is a re-audit: copy the old files first (rule 6), then read them.

### 2. Run the analysis

```bash
python3 scripts/audit_content.py --csv <export> --posts <folder> --sitemap <sitemap> --brand brand/ \
    --today <YYYY-MM-DD> --draft audits/content/inventory.csv
```

Leave out what wasn't supplied. Use today's date, or the date the user gives. `--draft` overwrites its file, so on a re-audit copy the old files first (step 1). In Check mode, leave out `--draft`. Thresholds the user names ("treat under 50 sessions as low") go in as `--set low_traffic=50`; the defaults are in the script's header. In Guided mode, draft to `audits/content/inventory-draft.csv` instead.

The output lists every piece with its metrics and flags (NEW, STALE, THIN, LOW-TRAFFIC, CONVERTS, NOTE, OLD-YEAR, OLD-FIGURE, RETIRED, HELD, EXCLUDED-AUDIENCE?, NO-DATA, NOT-IN-SITEMAP), competing pairs, every price in the posts beside the closest brand-memory line, sitemap gaps, and a suggested decision per piece. **The suggestions are rules, not answers.** Step 3 confirms or changes every one. The flag codes are for you: never copy them into the reply or AUDIT.md.

### 3. Decide every piece

Work through [references/judgment.md](references/judgment.md) for each piece: is it true (brand memory), is it alone on its topic, does anyone it's written for exist in brand memory, and do the numbers justify its place. Then edit the draft inventory: fill `audience` (the segment or persona it serves, `none: <why>`, or `unknown` without brand memory), set `decision`, `target` for merges and redirects, a one-line `reason`, and `evidence` quoting the numbers or the line (`1800 sessions; 22 conversions; "A single location is $299/month" vs offer.md: $349/month from 2026-10-01`).

### 4. Topic gaps

Compare what the library covers with each audience, persona (pains, triggers, what they're measured on) and offer line in `brand/`. A gap is something brand memory says a served audience cares about, or an offer it sells, with no piece covering it. Name the brand line each gap serves and the nearest existing piece. Never propose a gap for an audience brand memory excludes, and never attach a search volume. No brand memory: say gaps can't be judged against audiences, and list only questions the existing posts raise but don't answer.

### 5. Prioritize

Order actions by risk first, then reach: wrong or retired facts on pages people visit or convert from; merges of competing pairs; updates to stale pages with traffic or conversions; redirects; removals; `needs data` last. Within a band, more conversions and traffic first. At most 10 in the top list; the inventory has everything.

### 6. Write and check

Write `audits/content/inventory.csv` and `audits/content/AUDIT.md` in the shapes in [references/output.md](references/output.md). Then:

```bash
python3 scripts/audit_content.py --check audits/content/inventory.csv --report audits/content/AUDIT.md \
    --csv <export> --posts <folder> --sitemap <sitemap> --today <YYYY-MM-DD>
```

It fails on: a piece missing from the inventory, an empty reason, evidence or audience, a metric that doesn't match the export, a removal of a piece that converts or is under six months old, a merge with no target or into a piece that's itself going away, a figure in the report that isn't in the export, a traffic estimate, more than 10 top actions, or a report that mentions internals. A FAIL means fix the file and run it again, not explain it away.

Then the judgment check: every decision would survive the owner asking "why?"; nothing removed that sales uses; every outdated fact quotes both the piece and the brand line; no metric, URL, price or audience appears that the inputs don't contain.

### 7. Reply

```
**Recommendation:** <one sentence: what to do first and the shape of the rest, e.g. "Fix the wrong price on your second-best page this week; merge three competing pairs; remove two pages; keep nine.">

**Top actions**
1. <Decision> <URL> · <why, with the numbers or the brand line> · <what to do>
(up to 10)

**Decisions:** keep N · update N · merge N · redirect N · remove N · needs data N
**Topic gaps:** <up to 3, each with the audience or offer line it serves>
**Not supplied:** <only if something was missing: metrics, conversions, brand memory, posts; and what it would decide>

Files: audits/content/AUDIT.md (full audit), audits/content/inventory.csv (every piece, with decisions).
```

- Lead with the answer. For a blanket rule, the first line says what not to do and why, in plain numbers ("Don't delete all six: three of them bring in 12 of your conversions").
- Under 300 words; count before saving and cut the gaps and "Not supplied" lines to one line each if over. Check mode: decision, reason, the exact line to change, under 200 words.
- **Blanket rule:** under 250 words. The top actions cover only the pieces the rule catches, plus at most two wrong-fact fixes; everything else stays in the files.
- Second person. Never mention the script, its flags, similarity scores, the check, or any skill name, in the reply or in either file. Give file paths relative to the project folder (`audits/content/AUDIT.md`), never absolute paths.
- No brand memory: say so right after the recommendation, mark the audit provisional, and offer to set one up from the website or a short interview.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The owner can hand the inventory to whoever runs the site and every row is actionable without a question. Every number in it came from their export. Nothing that converts or that sales relies on is on the removal list. The wrong price is at the top, quoted next to the right one.

A worked example (a Pipewise blog audit) is in [assets/examples/pipewise/](assets/examples/pipewise/README.md).
