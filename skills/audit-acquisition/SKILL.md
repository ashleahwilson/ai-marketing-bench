---
name: audit-acquisition
description: Audits how people find a business, from its web pages and writes an acquisition report that leads with the three findings that matter most and a 48-hour / 2-week / 3-month plan. Covers indexability (robots meta, canonical, robots.txt and sitemap when supplied), per-page titles, descriptions, H1s and internal links, content that answers real buyer questions, AI-search and answer-engine readiness (entity facts, FAQ, structured data), local listing signals for local businesses, and channels visible from the site. Analyses Search Console or analytics exports when supplied, and never estimates traffic, rankings or search volume without them. Ends with the acquisition checklist score used by the full marketing health audit, recomputed from the deeper findings. Use when the user wants an SEO audit, a search or acquisition review, "why aren't we ranking", "how do people find us", "are we ready for AI search", or a read on a Search Console export. Not for paid-ad account audits or writing the content itself.
license: MIT
compatibility: Use with care: in testing, both models occasionally overstated a detail from the pages (a count or a word the page doesn't use), so check findings against the quoted evidence. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Acquisition audit

The deep dive behind the acquisition dimension of a marketing health audit. It answers one question: can the right buyers find this business, and if not, what's in the way? It reads pages, measures what can be measured, and ends with the same six-check score the full audit uses, so the two always agree.

## Ground rules

1. **Evidence or it didn't happen.** Every finding quotes a page or cites a measured fact, and names the page.
2. **Never audit a site you haven't read.** No pages and no way to fetch them: say so, ask for the pages (saved HTML is best), and say what the audit will cover. Never reconstruct a site from memory or from what similar sites usually have.
3. **Traffic, rankings, search volume, backlinks, ad spend and what AI assistants answer are not observable from outside.** Report them only from a Search Console, analytics or rank export the user supplied, with its date range. Otherwise list them under "Not observable" with the data that would show them. No estimates, ranges or "roughly", even when asked for numbers.
4. **No promises.** Nobody controls rankings, so never guarantee a position, traffic or an AI citation, even for a proposal. Offer what can be committed to instead: fixes shipped by a date, pages published, and what will be measured from a baseline.
5. **Indexability first.** A key page set to noindex, blocked in robots.txt, or canonicalised to another URL is a blocker: it leads the verdict and the plan, ahead of whatever the user asked about.
6. **The score is a formula.** Use the six checks in [references/scoring.md](references/scoring.md) and run the scoring script. Don't adjust it by hand, even if asked; re-examine the evidence instead.
7. **Calibrate to maturity.** Founder-led companies get relief on the two marked checks only.
8. **Never overwrite the user's files.** Earlier audit files, pages and exports stay as they are.
9. **Restate facts at the page's own scope.** "A team of 14" stays a team of 14, not "14 bookkeepers". Never describe what an image shows, and never assume a listing, profile or partnership exists that the pages don't show: ask ("Are you listed in Toast's partner directory? If so, link it") instead of recommending you link it.
10. **The domains in the pages are the real site,** even reserved test names such as `.example`. Don't question or flag a domain for looking unfamiliar.

**Whose brand memory is it?** A `brand/` folder belongs to the audited company only if its `BRAND.md` names that company. Then read `offer.md`, `audiences.md`, `claims.md` and `rules.md`: buyer questions come from the audience, and suggested titles and descriptions never use a claim marked unsubstantiated or a phrase a rule forbids. If there's no brand memory (or it's the auditor's own), audit from the pages alone, mark the report provisional, keep the company's own spelling in suggested copy, and offer to set up a short file of confirmed facts (offer, audience, approved claims) for next time. Don't use the term "brand memory" with the user unless they did.

## Pick the mode

| The user wants… | Mode |
|---|---|
| A quick read, "before my call", "in 10 minutes" | **Quick read:** one pass, answer in chat, no files ([references/output.md](references/output.md), "Quick read") |
| An audit, a deep dive, a report (the default) | **Draft:** the full workflow below, one complete pass for review |
| "Walk me through it", or the key pages are unclear | **Guided:** confirm the key pages and the buyer it should be found by before scoring, then run the workflow |

In Draft mode, take the key pages to be home, pricing, product or services, contact or booking, demo and location pages, and say so in "How this was done".

## Workflow

```
- [ ] 1. Collect: pages, robots.txt, sitemap, exports, brand/, any earlier audit in audits/<domain>/
- [ ] 2. Measure the pages: scripts/check_pages.py
- [ ] 3. If an export was supplied: scripts/search_data.py
- [ ] 4. Judge each area (references/checks.md)
- [ ] 5. Score: write acquisition-checks.json, run scripts/score_acquisition.py
- [ ] 6. Write acquisition.md, then self-check with scripts/check_report.py
- [ ] 7. Reply
```

### 1. Collect

Paths the user names (`site/`, `gsc/`, `robots.txt`) are relative to the project folder: the user's working folder, where `audits/` and your reply go, not the skill's folder. List the project folder **recursively**, including subfolders such as `site/`, `gsc/`, `brand/` and `audits/` (for example a recursive glob of `**/*`). Never tell the user files are missing until a recursive search has come back empty. Use raw HTML where you can: robots meta, canonical tags and structured data only show in the source. If `audits/<domain>/briefing.md` exists from an earlier full audit, reuse its business type and maturity, quoting its evidence. Note the audit date (today, or the date the user gives).

### 2. Measure the pages

```bash
python3 scripts/check_pages.py site/*.html --robots robots.txt --sitemap sitemap.xml --date <audit date>
```

Leave out `--robots` or `--sitemap` if they weren't supplied; add `--key /,/pricing,/contact` to name the key pages (include service and location pages), and `--domain example.com` (bare host) if the pages have no canonical tags. In a quick read, running it is fine; just don't write files. It prints a per-page table and BLOCKER, ISSUE and NOTE lines. It can't judge whether a sentence is clear, whether content answers a buyer's question, or whether a phone number is the right one: that's step 4.

### 3. Search data (only if supplied)

```bash
python3 scripts/search_data.py --queries Queries.csv --pages Pages.csv --brand "<brand terms>"
```

Use its numbers exactly, with the export's period. Ask for the brand terms if they aren't obvious from the company name.

### 4. Judge

Work through [references/checks.md](references/checks.md) in order: indexability, on-page basics per page, buyer questions and content, AI search and answer engines, local listings (local businesses only), channels, paid presence (only from supplied data or visible ad tags), search data.

### 5. Score

Classify the maturity first, using the definitions in [references/scoring.md](references/scoring.md), and quote the evidence. Decide each of the six checks from the findings, one evidence line each, and save `audits/<domain>/acquisition-checks.json` in the format in [references/scoring.md](references/scoring.md). Then:

```bash
python3 scripts/score_acquisition.py audits/<domain>/
```

Fix any FAIL and rerun. If an earlier full audit is in the folder, the script prints the earlier acquisition score, the checks that moved, and what the overall score and grade would become. Report that change with the reason for each moved check. Don't edit the earlier files.

### 6. Write and self-check

Write `audits/<domain>/acquisition.md` in the fixed shape (paste-ready titles and descriptions, when asked for, go in "Indexability and on-page basics"; issues outside acquisition, such as analytics tags, get one line in "How this was done") in [references/output.md](references/output.md): verdict, top three findings, the area sections, the checklist score, the plan, what wasn't observable, and how it was done. Then:

```bash
python3 scripts/check_report.py audits/<domain>/acquisition.md        # add --data if an export was supplied
```

A FAIL means rewrite the section, not hedge it. Then read it once more as the company would: every number traced to a page, the score or the export; every suggested title under 60 characters and description under 160 (count them); no claim the brand memory marks unsubstantiated; real strengths named.

### 7. Reply

Lead with the verdict line and the score, then the three findings, the 48-hour actions, where the files are (naming acquisition.md and acquisition-checks.json in the reply is fine; they're the user's files), and what wasn't observable with the data that would show it. If the request asked for something the audit won't do (numbers with no data, a guarantee), say so in a sentence or two, give the alternative, and deliver the rest. Never mention scripts, internal rules, check codes (A1-A6), "relief" or the names of any skills in the reply, and none of these except the check names in the score table go in the report: it may go straight to a client. Say "the content check" and "credit for a small team", not codes and rule names. For a quick read, count the words: under 200.

## Hand-offs

- **Reads:** `brand/` (offer, audiences, claims, rules), and from an earlier full audit `audits/<domain>/briefing.md`, `dim-acquisition.json` and `score.json`.
- **Writes:** `audits/<domain>/acquisition.md` and `audits/<domain>/acquisition-checks.json`, which uses the full audit's dimension-file format. Copying it over `dim-acquisition.json` updates the full score; offer that, don't do it. The proposed buyer-question topics in acquisition.md are written to be picked up as content briefs.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The company reads the file and agrees with it, because every point is quoted from its own pages or its own export. A blocked pricing page is the first thing they see, not the twelfth. Nobody finds a number that wasn't measured, or a promise nobody can keep.

A worked example, a local caterer with a Search Console export, is in [assets/examples/copperkettle/](assets/examples/copperkettle/README.md).
