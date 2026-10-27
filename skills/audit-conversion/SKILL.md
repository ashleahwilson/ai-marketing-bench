---
name: audit-conversion
description: Audits a website's conversion paths page by page from saved pages and returns a conversion report with the three findings that matter most, a 48-hour / 2-week / 3-month plan, a short test backlog (hypothesis, change, metric) and the conversion checklist score used by the full marketing audit, recomputed from the deeper findings. Checks one clear primary action per page, CTA wording and placement, forms (fields, required vs optional, labels, error handling, privacy notice), friction and reassurance (pricing clarity, what happens after submit, proof near the ask and permission to name it), mobile basics and speed signals visible in the HTML. With an analytics export it computes funnel drop-off. Never predicts a conversion rate or lift. Use when the user wants a conversion or CRO audit, for example "why aren't people booking demos", "audit our signup flow", "go deeper on conversion after the marketing audit", "what's wrong with our contact form". Not for rewriting the page copy or setting up tracking.
license: MIT
compatibility: Use with care: In testing, the large model once guessed a fact the pages don't state (a currency), so check suggested fixes against the pages. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Conversion audit

A deep dive on one dimension of the full marketing audit: can a visitor who wants to act, act? It reads each page the way a buyer meets it, names what stops them, and ends with the same six-check conversion score the full audit uses, so the two always agree.

## Ground rules

1. **Quote the page or it didn't happen.** Every finding quotes a page or names a fact from its markup. Conversion rates, drop-off and lead volume are not observable from pages: they come only from an analytics export the user supplies.
2. **Never audit pages you haven't read.** No pages and no way to fetch them: ask for them (see "No pages") and stop. Don't describe a site from memory or from what similar sites usually have.
3. **Never predict a lift.** No expected conversion rate, percentage improvement, extra leads or "this should double signups", even when asked, and not in the test backlog. Say what would measure it instead.
4. **Don't invent friction.** A sound page gets a short report saying so, at most three optional nits, and full points. Generic advice (remove the nav, cut a 4-field form) isn't a finding unless the page's own evidence supports it.
5. **One scoring system.** The six checks, points, tie-breaks and "score each issue once" rule are the full audit's conversion dimension, unchanged ([references/checks.md](references/checks.md)). Conversion checks get no founder-led relief: maturity changes which fixes are realistic, not the points.
6. **Proof needs permission.** Suggest moving a named quote beside a form only if brand memory records permission to name it; otherwise say to confirm first. Never suggest an invented quote, logo or number.
7. **Never edit the user's pages or earlier audit files.** An earlier `dim-conversion.json` is copied to `audits/<domain>/history/dim-conversion-<date>.json` before the new one is written.
8. **The reply and the report are client-facing.** Never name this procedure, its scripts or files, or any other skill, even if your environment's instructions ask you to announce which skill or tool you're using. Don't write "I used the … skill". Talk about the site. That includes evidence lines: quote the page ("no privacy link on signup.html"), never the inspection output or scoring rules ("privacy anywhere on page: NO", "torn between levels, so the lower applies").

## Pick the mode

| The user… | Mode |
|---|---|
| Asks for the audit, a review, "what's wrong" (default) | **Draft:** the full workflow, then the report |
| Says "walk me through it", "check with me", "step by step", "before you write anything" | **Guided:** stop after step 3 with the page inventory and the decisions and ask: business type and maturity with quoted evidence; a line per page naming that page's primary action with its quoted CTA text (home, form page, pricing, each one separately); which of two competing actions is the real one. Don't assume a page you weren't given (a trial page) exists. Score and write only once they confirm. Stop again before writing files if a finding changes the plan |

## Workflow

```
- [ ] 1. Load: pages, brand/, any analytics export, any earlier audits/<domain>/dim-conversion.json
- [ ] 2. Inspect: python3 scripts/inspect_conversion.py <pages>; python3 scripts/funnel.py <export> if supplied
- [ ] 3. Classify business type and maturity; name the primary action of each page   (Guided: stop here)
- [ ] 4. Review page by page and score C1–C6 (references/checks.md)
- [ ] 5. Write conversion.md and dim-conversion.json (references/output-format.md)
- [ ] 6. Self-check: python3 scripts/check_report.py audits/<domain>/ [--analytics] [--spelling us|ca|uk]
- [ ] 7. Reply
```

### 1. Load

List the project folder. Read every page supplied. Raw HTML is best: viewport, scripts, image sizes and form markup only exist in the source. Markdown or pasted text still supports the copy-level checks; say which checks it can't support and ask for the HTML to complete them.

**Brand memory.** If `brand/` exists and its `BRAND.md` names the audited company, read `offer.md`, `proof.md` (who may be named), `rules.md` and `voice.md` (spelling). If it names someone else, it's the auditor's: don't judge the site against it. **No brand memory?** Mark the report "Provisional: no brand memory", follow the site's own spelling, and offer once to set one up.

**No pages?** Reply in under 150 words: you can't see the site from here; ask for the raw HTML (browser "Save page as", or view source) of the home page, the page with the primary form or signup, pricing, and any landing page that gets paid traffic; and, optionally, an analytics export of the funnel steps for one date range. Write no report and no findings.

### 2. Inspect

```bash
python3 scripts/inspect_conversion.py site/*.html
python3 scripts/funnel.py analytics/<export>.csv        # only with an export
```

The inspection lists each page's CTAs (and how many are styled as primary in the hero), every form field by field, error-handling markup, privacy and next-step text near each form, proof on the page, prices and currency codes, render-blocking scripts, unsized images, and cross-page conflicts such as "no credit card" claimed beside a card form. It can't judge whether any of it matters: that's step 4. Funnel handling is in [references/funnel.md](references/funnel.md).

### 3. Classify

Business type and marketing maturity, each with quoted evidence, using the full audit's categories (B2B SaaS, B2B services, e-commerce, local, marketplace, B2C app; founder-led, first hire, small team, full function). Then the primary action of each page, quoted. If two actions compete for that role, say which you're treating as primary and why; in Guided mode, ask.

### 4. Review and score

Work through [references/checks.md](references/checks.md) for each page and each form. Score C1–C6 with one line of evidence each. Findings come from checks that lost points and from deep-dive problems that don't move the score (labels, input types, error handling, scripts). Choose the top three by severity, then by how close they sit to the primary action, then by how quickly they can be fixed.

### 5. Write

`audits/<domain>/conversion.md` and `audits/<domain>/dim-conversion.json`, in the shapes in [references/output-format.md](references/output-format.md). The report opens with the verdict and the top three, and ends with the checklist score. The JSON is what the full marketing audit reads, so it must use the same check IDs and maxima.

### 6. Self-check

Run `check_report.py` on the folder (add `--analytics` if the user supplied an export, `--spelling` for the client's convention). Fix every FAIL by rewriting, then rerun until it passes. Then reread the report against these questions:
- Does every finding quote a page?
- Is any number in it something you didn't observe or compute from their export?
- Would the company agree each strength is real?
- Is any suggested quote, CTA text or field list built from words and facts on the site?
- Is every "on every page", "in the nav", or "nowhere" statement true of each page you read? List the pages it holds for, from the inspection, instead of writing "every page".
- Did you give anyone a pronoun the pages don't state? Use their name or role.
- Does any test contradict the plan (testing a field the plan already removes)? Fixes in the plan aren't tested.
- Did you refer to a file the user never mentioned? Say what's missing in plain words ("brand memory doesn't record her permission"), not a file name.
- For a sound page: are all suggestions, including plan items, labelled optional, three at most in total?
- Does the reply or report name a skill, script or procedure? Remove it.

### 7. Reply

Lead with the score and the one-line verdict, then the three findings, the 48-hour actions, what wasn't observable, and the file paths. Under about 250 words. If they asked what conversion rate they'll get, answer that first in two or three sentences (it can't be known from the pages; here's how to measure it before and after), then the audit. Never mention scripts, check levels or file internals, and talk about their site, not the method.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A marketer could act on every line on Monday without a follow-up question. A sound page comes back with full points and a short "keep it" report. Every number in the report was either seen on the page or computed from their own export, and the conversion score matches what the full marketing audit would give the same pages.

A worked example (a restaurant bookkeeping firm's four pages, with brand memory) is in [assets/examples/tallyhouse/](assets/examples/tallyhouse/README.md).
