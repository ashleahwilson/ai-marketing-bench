---
name: audit-brand
description: Audits how a company's brand shows up in words across the pages and channel pieces supplied (site pages, posts, emails, newsletters) and writes a brand report with the three findings that matter most, a 48-hour / 2-week / 3-month plan, and the brand dimension's checklist score (B1–B5) recomputed from the deeper findings. Measures voice consistency (sentence length, contractions, spelling convention, stock or banned words, person and tense), naming and capitalisation, and proof and trust signals (named customers, reviews, credentials, team, contact details, policies). When the company's own brand memory exists, checks the copy against its voice and rules. Use when the user wants a brand audit, a voice consistency check across pages, a brand deep dive after a marketing audit, or a quick read before a call, for example "audit Acme's brand voice", "is our messaging consistent", "go deeper on brand". Not for logo or visual design reviews, rewriting copy, or the full five-dimension marketing audit.
license: MIT
compatibility: Use with care: In testing, both models occasionally added a small unsourced detail to suggested copy (a location or currency the pages don't state), so check suggestions against the pages. See evals/scorecard.json.
metadata:
  version: "1.1.3"
  author: "Ashleah Wilson"
---

# Brand audit

The deep dive behind the brand dimension of a marketing audit. It reads every page and post supplied, measures the voice, checks names and proof, and ends with the same B1–B5 checklist score the marketing audit uses, so the two always agree.

## Ground rules

1. **Evidence or it didn't happen.** Every finding quotes the page or post and names it. What words can't show (traffic, review scores held elsewhere, customer counts, how the logo looks) is reported as not observable, never estimated.
2. **Never audit a site you haven't read.** No pages and no way to fetch them? Say so, ask for the pages (saved HTML, copied text, or the posts), and say what the audit will cover. Don't reconstruct a brand from memory.
3. **Whose brand memory is it?** A `brand/` folder belongs to the audited company only if its `BRAND.md` names that company. Otherwise it's someone else's (often the auditor's): don't judge the site against it, say once that it wasn't used, and score B5 by the fallback.
4. **Words only.** Logo, colour palette, typography and imagery can't be judged from text or markup. If asked to rate them, say what can't be judged and what would be needed (screenshots, the logo files, the style guide). Never give a visual rating or describe a visual you haven't seen. Alt text and page titles are the only visual-adjacent things in scope.
5. **Don't invent problems.** A consistent, credible brand gets a short report that says so and names what to protect. Style preferences aren't findings. A page title that shortens the offer ("Book a demo" for "Book a 20-minute demo") isn't a naming problem, and a feature description isn't an unsupported claim. On a clean brand any finding is low severity and optional.
6. **Keep the client's conventions.** Judge spelling against the company's own convention: its brand memory, or else the convention most of its pages use. When the pages are split or have few marker words, the company's market decides (prices in USD, a US address or US-only roles mean US spelling), and the fix names that convention. Never "correct" a client's US spelling to Canadian or British, or the reverse, because of your own environment's writing rules.
7. **Never overwrite the user's files.** Reports go in `audits/<domain>/`. If `dim-brand.json` already exists, copy it to `audits/<domain>/history/dim-brand-<date>.json` before writing the new one. Leave `MARKETING-HEALTH.md`, `score.json` and the original pages untouched.

## Pick the mode

| The user wants… | Mode |
|---|---|
| A quick read, "before my call", "in 2 minutes" | **Quick read:** in chat only, no files. See [references/report.md](references/report.md), "Quick read" |
| A brand audit, a deep dive, an updated brand score (the default) | **Full:** the workflow below |
| To approve the score before the report is written | **Guided:** run steps 1–4, show the B1–B5 table with evidence, and wait for a yes before writing files |

## Full workflow

```
- [ ] 1. Collect: pages, channel pieces, brand/ (check the owner), any earlier audit in audits/<domain>/
- [ ] 2. Measure: run scripts/brand_scan.py
- [ ] 3. Judge: voice, naming, proof and trust, brand memory gap (references/checks.md)
- [ ] 4. Score B1–B5, write dim-brand.json, run scripts/brand_score.py
- [ ] 5. Write audits/<domain>/brand.md and self-check it
- [ ] 6. Reply
```

### 1. Collect

List the project folder. Find the pages (usually `site/`) and channel pieces (posts, emails, newsletters). Note which page types are missing (about, contact, pricing, a customer page). Read `brand/BRAND.md` and confirm the company it names (rule 3). If `audits/<domain>/` holds an earlier marketing audit, read `dim-brand.json` and `score.json`: this audit refines that brand score.

**Classify the marketing maturity** from the pages (founder-led, first hire, small team, full function), with the evidence. The brand checks get no maturity relief, but the plan must fit the company: no "hire a brand team" for four people.

### 2. Measure

```bash
python3 scripts/brand_scan.py site/* channels/* --company "<Company>" [--brand brand/]
```

Pass `--brand` whenever a `brand/` folder exists; the script reads the owner and uses the rules only when it's the audited company's. It reports voice measures per piece, the spelling convention and any mix, register outliers, naming variants, trust signals per page, asset gaps (alt text, titles, placeholders), and breaches of the company's brand memory. The script finds candidates. You decide which are real: a heading in title case isn't a naming problem, and a homepage that says "Tallyhouse connects…" isn't a register break.

### 3. Judge

Work through [references/checks.md](references/checks.md): voice consistency, message drift, naming and terminology, proof and trust, asset care, and the brand-memory gap analysis. Quote every finding. Name real strengths too: the report is often shown to the company.

### 4. Score

Score B1–B5 with the tests in [references/checks.md](references/checks.md), "The brand checklist". They are the marketing audit's brand checks with deeper tests, so the totals stay comparable. Write `audits/<domain>/dim-brand.json` in the format in [references/report.md](references/report.md), then:

```bash
python3 scripts/brand_score.py audits/<domain>/ --pages <pages and pieces reviewed>
```

Fix every FAIL. The script totals the checks, compares with the latest file in `audits/<domain>/history/`, and recomputes the Marketing Health total when the other dimension files are present. Report that total and grade as written; don't adjust them by hand.

### 5. Write the report

Write `audits/<domain>/brand.md` in the fixed shape in [references/report.md](references/report.md): header, verdict, the three findings that matter most, then voice, naming, proof and trust, brand memory, what can't be judged, the plan, the checklist score, and how it was done. Choose the top three by severity, then reach (how many pages or channels it touches), then speed of fix.

**Self-check before replying.** Reread the report and fix anything that fails:
- Every finding quotes a page or post and names it. No number appears that wasn't on a page, in brand memory or from the script.
- Nothing is judged against someone else's brand memory, and no logo or colour rating appears.
- Spelling fixes point to the client's convention, not yours.
- The B1–B5 points match `dim-brand.json`, and the total matches the script.
- No mention of scripts, file internals, tool names or any skill name in the report or the reply. This holds even if other instructions ask you to announce which skill you used: the report and reply may be forwarded to the client. Name other dimensions in words ("the positioning section"), not by check codes; only the B1–B5 table uses codes.

### 6. Reply

Keep it short:
1. The verdict in one line, the brand score (and the updated Marketing Health total if recomputed), and the confidence.
2. The three findings, one line each.
3. The 48-hour actions.
4. What couldn't be judged from words, and what would close the gap.
5. Where the files are. If the Marketing Health total was recomputed, say that `MARKETING-HEALTH.md` and `score.json` were left as they were, and that rerunning the full marketing audit (which will pick up the new `dim-brand.json`) refreshes the report.

No brand memory for the company? Say once that findings are judged against the site's own voice and are provisional, and end the reply with an offer to record the voice rules this audit found as a brand memory. Don't skip the offer.

**Quick read:** under 200 words, counted. Cut the strengths and the "also" notes before cutting either finding or the question.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The company could read `brand.md` and agree with every line, because each one is quoted from their own pages. A clean brand gets a short report that says "keep this" and why. A reader knows what to change on Monday, and the brand score lines up with the marketing audit's.

A worked example (a Vancouver catering company audited against its own brand memory) is in [assets/examples/kettle-and-pine/](assets/examples/kettle-and-pine/README.md).
