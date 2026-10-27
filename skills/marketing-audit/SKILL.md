---
name: marketing-audit
description: Audits a company's marketing from its website and public footprint and returns a scored Marketing Health report (0–100, graded A–F) across positioning, acquisition, conversion, brand and measurement, calibrated to the business type and marketing maturity, with evidence for every finding and a 48-hour / 2-week / 3-month plan. Use when the user wants to audit, assess, review, score or diagnose a website's or company's marketing, for example "audit acme.com's marketing", "what's wrong with our marketing", "score this prospect before my call", "quick read on this company's website", "marketing health check". It has a fast triage mode for before a call. Not for SEO-only technical crawls, paid-ad account audits inside the ad platforms, or writing new copy.
license: MIT
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Marketing audit

Turns a URL into a decision: a weighted score, a grade that names the next move, the three findings that matter most (each with evidence), and a three-horizon plan.

## Ground rules

1. **Evidence or it didn't happen.** Every finding quotes a page or cites a measured fact. What you can't see from outside (traffic, conversion rates, spend, team process) is reported as not observable, never estimated as fact. Industry benchmarks are labelled as benchmarks, with their source.
2. **Never audit a site you haven't read.** If you can't fetch pages and the user hasn't provided them, say so and ask for them. Don't reconstruct a site from memory or from what similar companies usually have.
3. **Calibrate to maturity.** A founder-led company is scored against what good looks like for a founder-led company. See [references/discovery.md](references/discovery.md).
4. **The score is a formula, not a feeling.** Run `scripts/score.py`. Don't adjust the total or the grade by hand, even if asked. If the user disagrees with a dimension score, re-examine that dimension's evidence and re-score it.
5. **Be fair.** Name real strengths. The audit is often shown to the company itself.

## Pick the mode

| The user wants… | Mode |
|---|---|
| A quick read, triage, "before my call", "in 10 minutes" | **Triage:** one pass over the homepage plus up to 2 key pages. Rate each dimension 1–5 against its rubric, multiply by 20, and apply the same weights for a rough grade, marked "triage" with confidence Low. Output in chat (see [references/report.md](references/report.md), "Triage output") |
| An audit, a health check, a report, a score (the default) | **Full:** the workflow below |

## Full audit workflow

```
- [ ] 1. Discovery (sequential): collect pages, extract, classify business type and maturity, write briefing.md
- [ ] 2. Analysis (parallel): score the five dimensions from the briefing
- [ ] 3. Score: run scripts/score.py
- [ ] 4. Report: MARKETING-HEALTH.md + one-pager
- [ ] 5. Reply: lead with the score and the three findings
```

### 1. Discovery

Follow [references/discovery.md](references/discovery.md). Collect up to 8 pages. Run `python3 scripts/inspect_page.py <pages>` on the HTML. Classify the business type and the marketing maturity, giving evidence for each. Write `audits/<domain>/briefing.md`.

**Whose brand memory is it?** A `brand/` folder belongs to the audited company only if its `BRAND.md` names that company. Otherwise it's the auditor's: use it only for the offer map, and never judge the audited site against it.

**Auditing the user's own company?** If its `brand/` folder exists (the brand-memory format), read it. The brand dimension then also checks the site against it. Use connected analytics or Search Console read-only, if available, to fill in what's otherwise not observable.

### 2. Analysis

Score each dimension using its section in [references/dimensions.md](references/dimensions.md):

| Dimension | Weight |
|---|---|
| Positioning | 25% |
| Acquisition | 20% |
| Conversion | 20% |
| Brand | 15% |
| Measurement | 20% |

**If you can run subagents,** give each one the briefing plus its dimension's section, and run all five in parallel. **If you can't,** score them one after another from the same briefing. Either way, each writes `audits/<domain>/dim-<name>.json` in the format at the end of `dimensions.md`.

**If a dimension can't be assessed or its analysis fails,** mark it `"assessable": false` with the reason. Don't guess. It counts as a neutral 50, and confidence drops.

### 3. Score

```bash
python3 scripts/score.py audits/<domain>/ --pages <number of pages reviewed>
```

`audits/<domain>/` sits in the user's project folder. If there's no domain, use a short slug of the company name. Reviewing fewer pages caps the confidence (under 4 pages: Low; 4–5: Medium).

If the auditor has an offer map, add `--offers <path to brand/rules.md>`. That's a `### marketing-audit` section in their own brand memory with lines like `C: Strategy engagement`. Put the matching next step **only** in `audits/<domain>/consultant-notes.md` and in your reply to the user. Never put it in `MARKETING-HEALTH.md` or the one-pager, which may be shared with the company.

| Grade | Score | Action |
|---|---|---|
| A | 85+ | Optimise: protect what works and test at the margins |
| B | 70–84 | Fix the weakest dimension before adding anything new |
| C | 55–69 | Rework the two weakest dimensions before putting more into growth |
| D | 40–54 | Rebuild the foundations, starting with the two weakest dimensions |
| F | under 40 | Get the basics in place before investing in growth |

### 4. Report

Write `audits/<domain>/MARKETING-HEALTH.md` and `one-pager.md` using [references/report.md](references/report.md). Choose the three findings that matter most by severity, then dimension weight, then how quickly they can be fixed. The plan horizons are 48 hours, 2 weeks and 1–3 months, and each action is concrete enough to start this week.

### 5. Reply

Keep the reply short. It covers:
1. The score, the grade and its action line, the classification, and the confidence.
2. The three findings.
3. The 48-hour actions.
4. Where the files are.
5. What wasn't observable, and what data would raise confidence.

Don't paste the full report into the chat.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The company could read the one-pager and agree with it, even when the grade is low, because every point is quoted from their own pages and the strengths are real. A reader knows what to do on Monday. No number appears that wasn't observed.

A worked example, a full audit of a fictional restaurant bookkeeping firm, is in [assets/examples/tallyhouse/](assets/examples/tallyhouse/MARKETING-HEALTH.md).
