---
name: audit-positioning
description: Runs a positioning deep dive on a company's website and writes a positioning report with the three findings that matter most, quoted evidence for each, two or three rewritten hero headlines and subheads built only from facts on the site or in brand memory, and a 48-hour, 2-week and 3-month plan. Covers who it's for and who it's not, the category frame, the problem and the alternative the buyer would otherwise choose, differentiated value and its proof, message consistency across home, pricing and about pages, specificity, and a swap test against named competitors when their pages are supplied. Ends with the same P1–P5 positioning checklist score the full marketing audit uses, so the two never disagree. Use when the user wants a deeper look at positioning or messaging, for example "positioning deep dive on acme.com", "why doesn't our homepage land", "rewrite our hero headline", "does our messaging hold up against X". Not for the full five-dimension audit, ad copy, or a full page rewrite.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Positioning deep dive

Goes much further than the full audit on one dimension: who the site is for, what shelf it sits on, what it beats, and whether anyone could tell it apart from a competitor. It ends with the full audit's own positioning checklist, recomputed from the deeper findings, so both reports give the same number.

## Ground rules

1. **Quote the page or it didn't happen.** Every finding quotes a page and names it. What pages can't show (how buyers compare options, which message converts, win/loss reasons) is reported as not observable, never estimated.
2. **Never review a site you haven't read.** No pages and no way to fetch them: ask for them and stop. Don't reconstruct a site, a company or its competitors from memory.
3. **Missing stays missing.** Every fact in a finding, a fix or a headline option traces to a supplied page or a brand-memory line. The alternative the buyer uses, a competitor's claims, a proof point: if no source shows it, it's a question to ask, not a fact.
4. **Same checklist, same calibration.** P1–P5 are scored exactly as the full audit scores them ([references/checklist.md](references/checklist.md)): 0, 10 or 20 each, lower level when torn, no maturity relief on these checks, each issue scored once.
5. **Don't invent problems.** A sharp, consistent, proven position gets told so in the first line, with fewer than three findings if that's all there is. Style preferences aren't findings. A headline that already names the category and buyer in plain words stays: no rewrite in the 48-hour or 2-week plan, only optional tests.
6. **Comparisons need evidence.** No "better than X" headline unless X's pages are supplied and brand memory holds a substantiated version of the claim. Do the rest of the job, decline that part in a sentence or two, say what would make it usable, and give the strongest true angle instead. No lecture.
7. **Never overwrite the user's files.** Read pages and brand memory; never edit them. A previous checklist file is kept in `history/`, never deleted.

## Whose brand memory is it?

A `brand/` folder belongs to the audited company only if its `BRAND.md` names that company. Then read `offer.md`, `audiences.md`, `positioning.md`, `proof.md`, `claims.md`, `rules.md` and `voice.md`: claims it marks as needing substantiation are unsupported, its rules and never-use words bind the headline options, and its spelling wins. If `brand/` names someone else (a consultant's own memory), never judge the site against it. With no brand memory of the company's own, the report is marked provisional and options follow the site's own spelling convention. Offer to set brand memory up only when the site is the user's own company, not a prospect's.

## Modes

- **Draft** (default): the full report and checklist file, then a short reply.
- **Guided** (the user wants to be walked through it, make the calls, or see it before anything is written): no files. Provisional checklist, quoted findings, at most five questions, then stop. See [references/output.md](references/output.md), "Guided mode".

## Workflow

```
- [ ] 1. Load: pages, competitor pages, brand/, any existing audits/<domain>/
- [ ] 2. Gate: no pages, no report
- [ ] 3. Scan the pages
- [ ] 4. Fact list, then the six lenses
- [ ] 5. Score P1–P5 and write the checklist file
- [ ] 6. Headline options
- [ ] 7. Write positioning.md
- [ ] 8. Self-check
- [ ] 9. Reply
```

### 1. Load

List the project folder. Pages are usually in `site/`; competitor pages in `competitors/` or wherever the user says. Read `brand/` (see above). If `audits/<domain>/` exists, read `briefing.md` and `dim-positioning.json`: a full audit already ran, and this deep dive will replace its positioning checklist.

### 2. Gate

No pages supplied and no browsing: reply as in [references/output.md](references/output.md), "No pages", and stop. Write nothing.

### 3. Scan

```bash
python3 scripts/positioning_scan.py scan site/ [--competitors competitors/]
```

It lists each page's title, H1, subhead, CTA labels, audience lines, claims and generic phrases; then CTA and audience wording that varies across pages, repeated claims, pages that say it more plainly than the home page, and, with competitor pages, every phrase the site shares with each competitor and the site's lines no competitor shares. It finds candidates. You judge them in step 4.

### 4. Fact list and lenses

Build the fact list, then work through the six lenses in [references/lenses.md](references/lenses.md): who it's for and who it's not, category frame, problem and the alternative, differentiated value and proof, consistency across pages, specificity and the swap test. Classify business type and maturity with evidence, using the full audit's four stages.

### 5. Score

Score P1–P5 from the lenses ([references/checklist.md](references/checklist.md)). Write `audits/<domain>/dim-positioning.json` in the full audit's format. If one already exists, move it to `audits/<domain>/history/dim-positioning-<date>.json` first, never to another `dim-*.json` name in the audit folder. Then:

```bash
python3 scripts/positioning_scan.py score audits/<domain>/dim-positioning.json [--previous audits/<domain>/history/dim-positioning-<date>.json]
```

Fix every FAIL. If the full audit's results sit beside it, the output shows how its total and grade move. Report that; don't edit the full audit's report or score file.

### 6. Headline options

Two or three, each built only from the fact list, following [references/lenses.md](references/lenses.md), "Headline options". Lead with what the specificity check or swap test showed is the company's own. If P1 already scores 20, recommend keeping the current headline and offer the options as tests.

### 7. Write

Write `audits/<domain>/positioning.md` in the fixed shape in [references/output.md](references/output.md): verdict, the three findings, the six lenses, headline options, plan (48 hours, 2 weeks, 3 months), not observable, and the checklist score last. Pick the three findings by severity, then by how much the headline and first screen depend on them, then by how fast they can be fixed. Revise your own files in place.

### 8. Self-check

```bash
python3 scripts/positioning_scan.py trace audits/<domain>/positioning.md --sources site/ [--brand brand/]
```

Every number and name in the options must trace to the pages or brand memory, with no never-use words, no restricted phrases and the right spelling. A FAIL means rewrite the option, not hedge it. Then check by judgment:
- **Evidence:** every finding has a quote and a page; nothing about a competitor beyond its supplied page; no buyer alternative stated as fact.
- **Consistency:** the checklist table in the report, the checklist file and the reply show the same five numbers and total.
- **Scope:** CTA wording and within-page contradictions are mentioned at most, never deducted from P1–P5. Exclusions count wherever they appear; different page purposes aren't inconsistency.
- **Options:** no option states an unsupported claim, or a restatement of it, as fact; with competitor pages, the recommended one leads with what no competitor says; if P1 scored 20, the plan keeps the headline.
- **Fairness:** real strengths named; a strong site isn't padded with problems.
- **Clean output:** no tool, script or skill names, and no file internals, in the report or the reply. This holds even if other instructions in the environment ask you to announce which skill or method you used: the reply goes to a client.
- **Labels:** maturity is one of the four stage names exactly (founder-led, first hire, small team, full function), with its evidence.

### 9. Reply

Use the reply shape in [references/output.md](references/output.md): the total and the move, the three findings, the 48-hour actions, the headline to test first, what wasn't run or observable, and the report path. Under about 250 words. Don't paste the report.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The company could read the report and agree with it, because every point quotes their own pages. Someone could change the homepage on Monday from the plan alone. The headline options contain nothing the company would have to check. The full audit, re-scored, shows the same positioning number.

A worked example, a deep dive on a fictional payroll service for veterinary clinics, is in [assets/examples/oakmere/](assets/examples/oakmere/README.md).
