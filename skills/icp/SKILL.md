---
name: icp
description: Builds and maintains the ideal customer profile and buyer personas from evidence (brand memory, a customer list or CRM export, win/loss and call notes) and writes a points-based scoring rubric another skill can apply to a prospect list. Computes which segments win, stay and pay from the data, says how many records every finding rests on, and labels small samples as hypotheses. Updates brand/audiences.md in the brand memory format and writes icp/scoring.md in a documented, parseable format (criteria, points, thresholds, disqualifiers). Never invents market size, TAM, benchmarks or persona quotes. With no customer data it writes a clearly provisional hypothesis and says what data would confirm it. Use when the user wants an ICP, target segments, buyer personas, a lead or account scoring rubric, "who should we target", "which customers are our best", or to update the ICP from a new export. Not for building the prospect list itself, writing outreach, or researching one company.
license: MIT
compatibility: Recommended for large models. Small models occasionally mislabel a segment count or paraphrase inside quote marks, and both sizes sometimes add a small unsourced aside, so check counts against the analysis. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# ICP

Turns customer evidence into three things: who to go after (and who not to), the people who buy, and a rubric that scores a list the same way every time. The data decides what's true; the user decides what to do about it.

## Ground rules

1. **Every finding carries its count.** "10 of 12 won", "median deal $14,550 (n=10)". A percentage only when the denominator is 10 or more. Under 5 closed records behind a finding is an anecdote, 5–9 a hypothesis. Under 10 closed records in total, the whole ICP is a hypothesis: counts only, status provisional.
2. **Never invent market data.** No TAM, SAM, SOM, market size, number of companies in a market, growth rate or "industry average". If asked, say once you don't have a source and won't estimate, name where each figure asked for could come from (one source per figure), and deliver the rest.
3. **Quotes are copied, never written.** A persona's words come word for word from call notes, win/loss notes, replies, reviews or `brand/proof.md`. A role with no recorded words gets `TBD`, and its other details are tagged assumed.
4. **Missing stays missing.** An unknown is `TBD: <what would tell us>`. A plausible guess is still an invention, and so is a persona backstory.
5. **The user decides the target.** When they want a segment the data argues against, show the evidence in counts, write their version (status `user-directed`), and recommend once. Never refuse, never lecture.
6. **Brand memory's exclusions are disqualifiers.** Anything `offer.md` or `audiences.md` says the business doesn't do or serve goes into the rubric as a disqualifier with its reason.
7. **Never overwrite the user's files.** Before editing `brand/audiences.md` or `icp/scoring.md`, copy the current version to `icp/history/`. Other brand files are read only, except one new line in `brand/changelog.md`.

## Pick the mode

| The request… | Mode |
|---|---|
| Has customer data (a CSV or export) and asks for an ICP, segments or a rubric | **Draft** (default): analyze, write both files |
| Has no customer data | **Provisional:** a hypothesis ICP from brand memory and the request, status provisional, plus the data that would confirm it |
| Has an existing `icp/scoring.md` and new data | **Update:** rerun, report what moved, bump the version |
| Asks only for personas | **Personas:** update the personas in `brand/audiences.md`; leave the rubric alone |
| Says "walk me through it", "decide together", "before anything gets written" | **Guided:** findings with counts, then 2–4 decisions, each with a recommendation. No files until they answer |

## Workflow

```
- [ ] 1. Load: brand/, the data files, any notes, any existing icp/
- [ ] 2. Analyze the customer data (script)
- [ ] 3. Read the notes for triggers, objections and exact quotes
- [ ] 4. Decide segments, disqualifiers, triggers, personas (references/judgment.md)
- [ ] 5. Write brand/audiences.md and icp/scoring.md, after copying old versions to icp/history/
- [ ] 6. Back-test and self-check (scripts, then the questions in judgment.md)
- [ ] 7. Reply in the fixed shape
```

### 1. Load

List the project folder, including subfolders, even if the user named one file. Read `brand/BRAND.md`, `audiences.md`, `offer.md`, `positioning.md`, `proof.md` and `rules.md` where they exist. Find every CSV and every notes file (win/loss, calls, interviews, reviews).

**No `brand/` folder?** Work from the data and the request. Say in the reply that there's no brand memory, mark anything not drawn from the data as provisional, create only `brand/audiences.md`, and offer to set up the rest.

### 2. Analyze

```bash
python3 scripts/analyze_customers.py <customers.csv> --out icp/analysis.json
```

It matches columns by common names, drops open deals, duplicates and rows with no outcome, and reports win rate, churn, deal size and cycle by segment, with the sample-size labels applied. Read its header first: which column it read as what, how many rows it excluded and why, which fields are missing, any date warning. If a mapping is wrong, rerun with `--map outcome="Deal Stage",deal="ARR"`.

If any segment field is blank on some rows (they show as "unknown"), say how many and which field under "Before you use it".

Use only figures it printed, each with the exact label of the row it came from. "General dentistry / 1" (one industry at one size) is not "1" (every single-location clinic), and the two have different counts. Never count or add rows by hand: if you need a figure it didn't print (a combined segment, a different cut), rerun with `--by` or `--cross`, or leave it out.

No CSV at all: skip to step 3 and use Provisional mode.

### 3. Read the notes

Pull out what happened before each purchase (triggers), why deals were lost and customers left, what each role is measured on, and their objections. Copy quotes exactly, with who said it and when. Count how many notes support each trigger.

### 4. Decide

Follow [references/judgment.md](references/judgment.md): check the analysis, rank segments on retention, then win rate, then deal size; pick triggers; build one persona per role the evidence shows. Two rules hold with or without brand memory:
- **Disqualifiers:** every brand-memory exclusion, plus any segment with 0 wins in 4 or more closed records whose loss reasons point the same way (procurement, security reviews, an enterprise suite). A zero-win segment must never be able to outscore a segment that wins.
- **Sample labels:** 10+ closed records is evidence; say it plainly and don't call it "too few". Under 10 is "too few to be sure", every time it's mentioned. It also covers the hard cases: no data, a tiny sample, a user who insists on a segment, requests for market size, and quotes that don't exist.

### 5. Write the files

- **`brand/audiences.md`**, in the brand memory format: segments in priority order, triggers, Not for, personas, history. Layout and source tags in [references/audiences-format.md](references/audiences-format.md).
- **`icp/scoring.md`**, the rubric the list builder reads: a short header (version, date, status, basis, max points, tiers), then `| Criterion | Points | Evidence |` tables for criteria and disqualifiers. Each criterion is written in the list builder's grammar (`Industry: a, b`, `Locations 5–19`, `Locations 20+`, `Signal new location: yes`) and disqualifiers score `DQ`. Format in [references/scoring-format.md](references/scoring-format.md). Keep any Notes the user wrote.
- **`brand/changelog.md`**: one new dated line.

### 6. Back-test and self-check

```bash
python3 scripts/scoring.py check icp/scoring.md
python3 scripts/scoring.py backtest icp/scoring.md <customers.csv>
python3 scripts/check_icp.py --scoring icp/scoring.md --audiences brand/audiences.md --analysis icp/analysis.json --sources <notes files> brand/proof.md icp/history/* --reply response.md
```

`check` validates the rubric in the list builder's grammar, the points and the tiers. `backtest` scores the customer file with the rubric: retained customers should sit higher than churned and lost ones; if not, adjust the weights. `check_icp.py` fails on untraced or small-sample percentages, market figures, quotes not found in a source, untagged audience bullets, evidence without counts, and internals in the reply. Fix every FAIL and rerun. For every CHECK line, trace the figure to the analysis row or note it came from, or delete it. Then answer the self-check questions in judgment.md. Skip `--analysis` and `backtest` when there's no CSV.

### 7. Reply

```
**ICP:** <written | updated to version N | provisional hypothesis | your version, with a recommendation | not written yet> (brand/audiences.md, icp/scoring.md)

**Recommendation:** one line: who to go after first, and the count behind it.

**What the data shows:** 3–5 bullets, each with its count. First bullet is the basis ("46 closed records; 3 open deals and 1 duplicate left out").

**Before you use it:** numbered: small samples, gaps, decisions for the user, data that would confirm it.

**Kept out:** one line on what was deliberately left out and why (market size without a source, quotes no one said). Omit if nothing.
```

- **Guided:** the "ICP" line says not written yet; then the findings (mark each segment under 10 records "too few to be sure"), then the numbered decisions, each with your recommendation. Nothing else.
- **User-directed:** acknowledge what's true in their view, give the counter-evidence in two or three lines with counts, say the rubric follows their call, recommend once.
- Keep the reply under 300 words. The detail is in the files.
- Say small samples in plain words: "only 6 records, too few to be sure", not just "hypothesis".
- Don't explain how the rubric is built (point caps, labels, thresholds for evidence). Give the finding and what it means for who to call.
- "Kept out" names only what the user asked for, or what the evidence held, that you left out. If nothing, drop the line.
- Never mention the scripts, the analysis file, source-tag statuses, these references or any skill by name. Say "the rubric your list builder reads", not a tool's name. Talk to the user in the second person.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A salesperson can read `brand/audiences.md` in two minutes and know who to call, who to skip and what that buyer cares about. Every number traces to a count in the data, every quote to a note, and every gap is a visible `TBD`. The rubric scores a list the same way twice, and scores the company's own best customers highest.

A worked example (Pipewise, a pipeline-review tool, from 28 deals) is in [assets/examples/pipewise/](assets/examples/pipewise/README.md).
