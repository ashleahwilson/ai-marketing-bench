---
name: meta-ads-audit
description: Audits a Meta (Facebook and Instagram) ads account from the Ads Manager and Events Manager exports the user supplies (or read-only from a connected tool) and returns a scored report (0–100) that leads with the top three findings and a 48-hour / 2-week / 3-month plan. Checks objective against the business goal, pixel and Conversions API setup (duplicate events, the optimized event), attribution, structure and budget fragmentation against Meta's guideline of about 50 optimization events per ad set per week, audience overlap, frequency and creative fatigue, creative volume and variety, placements, Advantage+ use, and special ad categories (employment, housing, credit, social issues). Every dollar and rate is computed from the export. Use when the user wants a Meta, Facebook or Instagram ads account audited, reviewed or diagnosed, for example "audit our Meta ads", "why is our cost per lead so high", "Meta says 380 leads but our CRM has 190". Writes a fix list for the build step. Never changes the account.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Meta ads audit

Turns an ad account's exports into a decision: what's broken, what it's costing, and what to change first. It reads, computes and recommends. It never edits, pauses or creates anything in the account.

## Ground rules

1. **No export, no findings.** Without exports (or a connected read-only tool), there is nothing to audit. Say exactly what to export and how ([references/exports.md](references/exports.md)), ask for the business's own conversion count, and stop. Don't guess causes and present them as findings, and don't compute anything from a spend figure the user mentions in passing.
2. **Every number is computed, never estimated.** Spend, results, cost per result, CTR, CPM, frequency, shares, weekly event rates, trends and ratios come from the export through the analysis step. If a number can't be computed from what was supplied, it's "not in export", not a guess.
3. **Benchmarks only with a named source.** Meta's published learning guideline (about 50 optimization events per ad set per week) is the one built-in reference, and it's labelled as Meta's guideline. Don't quote industry CTR, CPM or cost-per-lead averages from memory. Use one only if the user or `brand/` supplies it with its source; otherwise compare the account with itself (period halves, ad set against ad set, placement against campaign).
4. **Compliance comes first.** An ad about jobs, housing, credit or social issues running without its special ad category is a **blocker**: it leads the report, ahead of any performance finding, and the advice is not to scale it until it's fixed, however well it performs. See [references/checks.md](references/checks.md), check 10.
5. **Confidence follows the data.** Under 14 days or under 30 conversions is Low confidence: don't declare winners or losers between ad sets, and say what data would settle it. Structural problems (wrong objective, broken tracking, missing category) don't need volume to be real.
6. **No promises.** Never commit to a future cost per lead, cost per purchase or ROAS, even when asked to put one in the report. Say why in one or two sentences, then give what can be committed to: the computed baseline, the fixes, the metric to watch and a date to check it. Don't refuse the audit and don't lecture.
7. **Read-only, always.** With a connected tool, use read and report actions only. Never overwrite the user's exports. Every fix is a proposal that needs the account owner's approval.

## Pick the mode

| The user wants… | Mode |
|---|---|
| An audit, a review, "what's wrong" (the default) | **Draft:** the full workflow below, one pass |
| "Step by step", "check with me first", "before you judge anything" | **Guided:** run steps 1–2, report what loaded with the computed headline figures (period, spend, results), ask at most three questions that change the verdict (the business goal and what counts as a conversion; the business's own count; anything missing), then stop. No score, no AUDIT.md until they answer |
| No exports attached | **Export guide:** ground rule 1. Under 250 words |
| One narrow question ("why does Meta show double our leads") | Draft mode, but the reply answers that question first and keeps the rest short |

## Workflow

```
- [ ] 1. Load: exports, brand/, the business goal and the business's own conversion count
- [ ] 2. Analyze: python3 scripts/meta_audit.py analyze ...
- [ ] 3. Judge the ten checks (references/checks.md); write checks.json
- [ ] 4. Score: python3 scripts/meta_audit.py score ...
- [ ] 5. Write AUDIT.md and fixes.md (references/output-format.md)
- [ ] 6. Verify: python3 scripts/meta_audit.py verify ...; fix every untraced figure
- [ ] 7. Reply
```

### 1. Load

List the project folder. Find the exports (CSV files from Ads Manager and Events Manager, and any notes or screenshots the user added). Read `brand/` if it exists (the brand-memory format: facts carry `[source: …]` tags, gaps are `TBD:`): `offer.md` says what the paid conversion should be, and any target cost has to come from there or the user. **No `brand/`?** Work from the prompt and the exports, mark the report provisional, state the goal you assumed, and offer to set up brand memory.

Note the business's own count of the conversion (CRM leads, app trials, store orders) if the user gives it. It's the only way to catch double counting.

### 2. Analyze

```bash
python3 scripts/meta_audit.py analyze <exports folder> --backend <Event>=<business count> --json audits/meta-ads/<account>/metrics.json
```

`<account>` is a short lowercase slug of the business or ad account name. The analysis recognises each CSV by its headers and computes the period, totals, every campaign, ad set and ad, results per week against the learning guideline, first-half against second-half trends, placement costs against the campaign, Events Manager counts by connection with event ID coverage, the Meta-to-business ratio, special ad category terms found in names and ad text, and the confidence level. Read its output in full: it's the only source of numbers for the report.

### 3. Judge

Work through the ten checks in [references/checks.md](references/checks.md). Each gets a status (`pass`, `warn`, `fail`, `blocker`, `na`) and one line of evidence quoting a computed figure or a file. Write them to `audits/meta-ads/<account>/checks.json` in the format at the end of that file. A check with no data is `na` with the reason ("no Audience Overlap export"), never a guess.

### 4. Score

```bash
python3 scripts/meta_audit.py score audits/meta-ads/<account>/checks.json
```

The score is the weighted formula, not a feeling. Don't adjust it by hand. A blocker leads the report whatever the score.

### 5. Write

Write `audits/meta-ads/<account>/AUDIT.md` and `audits/meta-ads/<account>/fixes.md` using [references/output-format.md](references/output-format.md). Pick the top three findings by: compliance blockers, then anything that corrupts the data the account optimizes on (tracking, the optimized event, objective), then money at stake (computed spend), then speed to fix. In a sound account, say so: the top findings can be minor, "keep the structure" is a valid recommendation, and the whole audit recommends at most three changes. Don't invent problems to fill three slots.

### 6. Verify

```bash
python3 scripts/meta_audit.py verify audits/meta-ads/<account>/AUDIT.md --metrics audits/meta-ads/<account>/metrics.json [--allow <figure the user gave>]
```

Run it on `fixes.md` too. Every untraced dollar figure, percentage or multiplier is either fixed to the computed value or removed. Then check by reading: no promised result, no unsourced benchmark, the blocker (if any) first, the plan has all three horizons, nothing claims a change was made.

### 7. Reply

```
**Score:** <n>/100 (<band>) · **Confidence:** <level> (<reason>)
**Compliance blocker:** <only if there is one, in one line>
**Recommendation:** <one line: the single most important move>

**Top three findings**
1. <finding> · <computed evidence> · <fix>
2. …
3. …

**Next 48 hours:** <2–4 actions>

**Files:** audits/meta-ads/<account>/AUDIT.md (full report and plan), fixes.md (the change list for whoever builds it)
**Not assessed:** <checks with no data, and the export that would cover them>
```

- Answer the user's actual question in the first lines when they asked one ("which ad set should I kill": the answer, then why).
- Under 350 words. Don't paste the full report. The reply, AUDIT.md and fixes.md must agree (same plan horizons, same not-assessed list); if nothing is unassessed, say "Not assessed: none" and stop there.
- Talk about the account, not the method. Never mention the analysis script, its output, the check count, point weights or fix IDs (F1, F2) in the reply; say "computed from your export". Fix IDs belong in the files. Don't name the mode, the workflow steps, working files (metrics.json, checks.json) or audit-rule names either; give paths relative to the project folder.
- Use the export's currency. In a client deliverable with no brand memory, keep the client's own spelling conventions.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A media buyer can open `fixes.md` on Monday and act on every line without asking a question. Every dollar in the report can be found by re-adding the export. The account owner learns the uncomfortable thing first (a compliance gap, double-counted conversions) even when they asked about something else, and nobody is promised a number the audit can't deliver.

A worked example, a full audit of a fictional kayak retailer, is in [assets/examples/harbourline/](assets/examples/harbourline/README.md).
