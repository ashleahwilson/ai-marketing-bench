---
name: google-ads-audit
description: Audits a Google Ads account from CSV exports (campaigns, keywords, search terms, ads, conversion actions, settings), or read-only through a connected Google Ads tool, and returns a scored report (0–100, graded A–F) with the top three findings first and a 48-hour / 2-week / 3-month plan. Checks conversion tracking (non-outcome or duplicate primary actions), wasted spend on irrelevant search terms and missing negatives, match types, budget-limited campaigns, bid strategy against conversion volume, Quality Score, responsive search ad coverage, location and network settings, brand and non-brand mixing, and landing page match. Every dollar figure is computed from the export, never estimated, and confidence drops with short date ranges or few conversions. Use when the user wants a Google Ads, AdWords, PPC or search ads account audited, reviewed or diagnosed, for example "audit our Google Ads", "where are we wasting ad spend". Never changes the account; writes a fixes list for google-ads-build.
license: MIT
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Google Ads audit

Turns a folder of Google Ads exports into a decision: what's costing money, what's wrong with the signals bidding learns from, and what to change first. It reads. It never changes the account.

## Ground rules

1. **No data, no findings.** Without exports (or a connected tool), don't audit from what accounts like this usually get wrong. Send the export list in [references/exports.md](references/exports.md), with where to find each report in Google Ads, and stop. No score, no "likely" findings, no AUDIT.md.
2. **Every dollar figure comes from the script.** Waste, spend outside the target area, partner and Display spend, CPA: run `scripts/ads_audit.py` and use its numbers. Sums of its figures are fine. Never estimate, extrapolate, annualize or project ("per year", "per month", "you'll save", "you'll get").
3. **Never promise a result.** No ROAS, CPA, revenue or conversion forecast, even when asked for one "for the CEO". Say what the data supports instead: the current figure, the dollars going to waste, and what would make a forecast possible.
4. **Confidence follows the data.** Short date range or few real conversions means Low confidence: say so in the verdict line, give no bid-strategy verdict, and keep findings to what the data shows.
5. **Missing stays missing.** A check without its export is "Not checked", with the export that would let it run. Benchmarks appear only with a named source the user or brand memory gave; the audit's thresholds are labelled as its own rules of thumb.
6. **Read-only.** Even with a connected tool, even when asked to "just push the negatives live". Say once that the audit doesn't change the account, then hand over the fixes list. Never say a change was made.
7. **Never edit the user's files.** Exports stay as they are. Output goes to `audits/google-ads/<account>/`.

## Pick the mode

| The user wants… | Mode |
|---|---|
| An audit, a review, a health check (the default) | **Draft:** run the whole workflow, make the relevance calls yourself, list borderline terms separately |
| To confirm calls first ("guided", "check with me before…", "I want to confirm the junk terms") | **Guided:** stop once after step 3 with the checkpoint in [references/output-format.md](references/output-format.md). Write no files until they answer |

## Workflow

```
- [ ] 1. Load: find the exports; read brand/ if it exists
- [ ] 2. Run scripts/ads_audit.py
- [ ] 3. Judge: search-term relevance, borderline terms, brand rules in live ads, landing pages
- [ ] 4. Rerun with --irrelevant; write AUDIT.md and fixes.md
- [ ] 5. Self-check with scripts/check_audit.py; fix every FAIL
- [ ] 6. Reply
```

### 1. Load

List the project folder. Exports are CSVs anywhere in it (often `exports/`, `google-ads/` or `ads-data/`). No CSVs and no connected tool: follow ground rule 1.

Read `brand/` if present (`BRAND.md`, `offer.md`, `audiences.md`, `rules.md`, `claims.md`, `voice.md`). It gives the account name, brand terms, what the business sells, who it's for and not for, and the rules live ads must follow. **No brand memory?** Run the audit anyway. Mark the report provisional, label relevance calls as assumptions from the account itself, take brand terms from the account name in the ads, and skip the brand-rule read (say so under "Not checked").

### 2. Run the script

```bash
python3 scripts/ads_audit.py <export-folder> --brand "<brand term>,<misspelling>" --json audits/google-ads/<account>/working/metrics.json
```

It recognizes each report by its columns, reads the date range, skips "Total" rows, and returns: account totals, confidence, all 11 checks with a status and their figures, and the score. The check definitions, thresholds and what to say for each are in [references/checks.md](references/checks.md). Read it before judging.

### 3. Judge

The script can't know the business. You decide, citing brand memory or the account:
- **Search-term relevance.** Go through the zero-conversion terms it lists. Clearly irrelevant ones (a different buyer, a segment the business doesn't serve, job seekers, a different product) go in `audits/google-ads/<account>/working/irrelevant.txt`, one pattern per line with `# reason`. Borderline ones (plausible buyers, or terms that converted) stay out of the waste total and are listed with their cost as the user's call.
- **Brand rules in live ads.** Read every headline and description against `rules.md`, `claims.md` and the never-use words. Quote any breach.
- **Borderline terms.** Also look at terms that converted but sit outside the offer (a service the business doesn't list, a different product), and zero-conversion terms close to something the offer mentions (a tool the product connects to). They are never waste: list them with cost and conversions as the user's call.
- **Budget-limited campaigns.** Compare a limited campaign's cost per conversion with the non-brand cost per conversion elsewhere, not the blended account figure: brand traffic makes the blend look cheap. If it beats non-brand elsewhere, recommend moving money to it from waste or weaker campaigns.
- **Brand terms.** Use names from brand memory, the account (keywords, search terms, ads) or the user. Never add misspellings that appear nowhere in the data.
- **Landing pages.** Confirm or dismiss each flagged ad group from its keywords and URL. You can't see the page: don't describe it.
- **Conversion values.** If the script says values are fixed, any ROAS in the account is assigned value ÷ cost, not revenue. Say so plainly.

Guided mode stops here.

### 4. Write

Rerun the script with `--irrelevant audits/google-ads/<account>/working/irrelevant.txt` and the same `--json`. Use the rerun's figures and score; don't adjust the score by hand. Then write, in the shapes in [references/output-format.md](references/output-format.md):
- `audits/google-ads/<account>/AUDIT.md`: verdict line, top three findings, scorecard of all 11 checks, findings by check, the 48-hour / 2-week / 3-month plan, not checked, sources and assumptions.
- `audits/google-ads/<account>/fixes.md`: numbered fixes `<n>. [P1|P2|P3] <area> · <problem> · <fix>` plus account facts, for google-ads-build. Anything needing a human decision ends `(confirm first)`.

### 5. Self-check

```bash
python3 scripts/check_audit.py audits/google-ads/<account>/AUDIT.md --metrics audits/google-ads/<account>/working/metrics.json --fixes audits/google-ads/<account>/fixes.md --allow <prices quoted from brand memory, comma-separated>
```

It fails any dollar figure that doesn't trace to a computed figure, a missing section, a promise or forecast, and a malformed fix line. A FAIL means rewrite the line, not hedge it. Then check by hand:
- Top three come first, each with a named campaign, term or setting and its number.
- Nothing in the report claims a change was made, forecasts a result, or states a benchmark without a source.
- On Low confidence: no bid-strategy verdict, no projection, and the verdict line says why.
- No term is called waste that converted or that brand memory says is in scope.
- No two figures that may overlap are added together or described as containing each other (search-term waste and Search Partners spend). No cause stated that the data doesn't show ("broad match is how these got through" is a guess unless the match types prove it).
- No `TBD` inside a fix line: if a value is unknown (a URL, a brand term), the fix says what's needed and ends `(confirm first)`.
- The reply and AUDIT.md say the same thing (for example, both say "no verdict" on bid strategy when confidence is Low; a Low-confidence score is labelled as such).
- No mention of scripts or working files in the reply, AUDIT.md or fixes.md. Export file names belong only under "Sources and assumptions".

### 6. Reply

Lead with the score, grade and confidence, then the recommendation in one sentence, the top three, and what to do in the next 48 hours. Under 250 words unless asked for more. Point to the two files. Talk to the user in the second person. Never mention the scripts, their output, check names in capitals, or other skills by name.

**Pushback, without lecturing:**
- **Asked to promise ROAS:** one sentence on why no one can honestly promise it from this data (and, if values are fixed, that the account's ROAS isn't revenue), then what you can stand behind: the current figure and the dollars that are recoverable now.
- **Asked to make the changes:** the audit is read-only (say it as how it works, not as a missing connection); the fixes list is ready for whoever applies them, with the exact negatives and settings. If they ask to "pause the junk keywords", explain that the junk is search terms, blocked with negatives, while the keywords that matched them also bring conversions and should stay on.
- **Asked for a yearly waste figure from a short export:** give the figure for the days you have, and the export that would support a longer view.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The person running the account can act on every line without asking a question, and every number can be found in the export. A clean account scores well and the report says so in a few lines. Nothing in it depends on a fact the audit guessed.

A worked example (a physiotherapy clinic's account) is in [assets/examples/brightwater/](assets/examples/brightwater/README.md).
