---
name: audit-measurement
description: Audits what a website can actually measure and returns a measurement report that leads with the top three findings, a 48-hour / 2-week / 3-month plan, a tracking plan (events, their parameters, which are conversions, where each fires) and the marketing audit's measurement checklist (M1-M5) recomputed. Works from saved page HTML (GA4, Google Tag Manager, Meta Pixel, LinkedIn Insight and other tags; loaded versus configured; consent banners and consent mode; UTMs on internal links; whether form submissions are tracked), and from a Tag Manager container export or analytics exports when supplied. Flags tracking that loads before consent for audiences in Canada, the EU or the UK without giving legal advice, and keeps personal data out of analytics. Use when the user wants tracking, GA4, GTM, pixels, conversions or UTMs audited or planned, for example "is our GA4 working", "audit our GTM container", "set up conversion tracking", "go deeper on measurement". Never reports numbers it can't see.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Measurement audit

The deep dive behind the measurement fifth of a marketing audit. It answers one question: what can this site count today, and is what it counts true? It reads source and exports, never live data, and it scores the same checklist the full audit scores.

## Ground rules

1. **What loads is not what was collected.** Page HTML shows which tags load and what they're told to send. It never shows visitors, sessions, conversions or rates. Don't estimate them, give a range, or present a benchmark as theirs. Numbers come only from an export the user supplied: quote them exactly, with the period, and never extrapolate.
2. **Loaded, configured and firing on the outcome are three states.** GA4 loaded without a `config` call (and no Tag Manager) sends nothing. An event on a button click counts clicks, not leads. Say which state each tag is in.
3. **Same checklist, same points as the full audit.** M1–M5 with the rubric in [references/checks.md](references/checks.md). Score each issue once, take the lower level when torn, give founder-led relief on M3 only. The score is the sum of the checks.
4. **Personal data never goes into analytics or ad tags.** No email, name, phone, address or form text in any event, parameter or URL, even when asked. Push back in two or three sentences, offer a way to see who converted (the CRM, joined on a non-identifying ID), and deliver the rest. See [references/privacy.md](references/privacy.md).
5. **Privacy points are flags, not legal advice.** Report what loads before consent and why it matters for this audience (Canada, the EU or the UK). Never call a site compliant or non-compliant.
6. **Never overwrite the user's files.** Their pages and exports are read-only. An earlier `dim-measurement.json` is copied to `audits/<domain>/history/` before the new one is written.
7. **Client-facing files and replies never mention scripts, skill names or how the report was produced** beyond "from the page source" and "from the container export".

## Pick the mode

| The user wants… | Mode |
|---|---|
| A deep dive, an audit, "what can we measure", "go deeper on measurement" (the default) | **Draft:** the full workflow below |
| A number ("how many visitors last month") with no export, or a yes/no ("is GA4 working?") | **Answer:** steps 1–2, then the Answer reply in [references/output.md](references/output.md). No files unless asked |
| "Step by step", "check with me first", "before you decide what counts" | **Guided:** steps 1–3, then report what you found, recommend a conversion with the reason, say how tags should wait for consent if the audience needs it, ask at most three questions (the first: which event counts as the conversion) and stop |
| "Set up tracking", "write a tracking plan" | **Plan:** steps 1–2, then the tracking plan and three lines on what exists today |

## Workflow

```
- [ ] 1. Load: pages, container export, analytics exports, brand/, earlier audit files
- [ ] 2. Inspect: python3 scripts/inspect_tracking.py <files>
- [ ] 3. Judge: references/checks.md, references/privacy.md
- [ ] 4. Score: write dim-measurement.json, run scripts/score_measurement.py
- [ ] 5. Write measurement.md and tracking-plan.md (references/output.md)
- [ ] 6. Self-check: python3 scripts/check_report.py, plus the judgment checks
- [ ] 7. Reply
```

### 1. Load

List the project folder. Collect:
- **Page HTML** (raw source, not rendered text). Tags only show in the source. With rendered text or markdown only, measurement isn't assessable: say what's needed (raw HTML, the container export, analytics access) and stop.
- **A Tag Manager container export** (`GTM-*.json`), if supplied. Without one, anything inside the container is not observable: ask for it when it matters.
- **Analytics exports** (CSV), if supplied. They're the only source of numbers.
- **`brand/`** (the brand-memory format: facts carry `[source: …]` tags, gaps are `TBD:`). Read `audiences.md` or `BRAND.md` for where the audience is, `offer.md` for what counts as a conversion, and `voice.md` for spelling. **No `brand/`?** Mark the report provisional, say what you assumed about the audience, follow the spelling of the company's own site, and offer to set up brand memory.
- **Earlier audit files** in `audits/<domain>/`: `briefing.md`, `dim-measurement.json`, `score.json`. Read them; the deep dive refines them.

`<domain>` is the site's domain (`tallyhouse.example`). With no domain, use a short slug of the company name.

### 2. Inspect

```bash
python3 scripts/inspect_tracking.py site/*.html [gtm/GTM-XXXX.json] [data/*.csv]
```

It lists, per page, every tag and ID, whether GA4 is configured (and how many times), whether Tag Manager and a hard-coded tag both load, consent banner and consent mode signals, tags that load before any consent choice, events in the source with their parameters and what triggers them, forms and their personal fields, and internal links carrying UTMs. For a container it lists tags, triggers and variables, and flags tags with no trigger, paused tags, duplicate pageviews, conversions on broad triggers, personal data and unused triggers. For exports it prints every row and flags automatic events marked as key events, key events with zero count, and sources that look like internal UTMs. Read all of it: these are observations, and your report can't contain a tag or number that isn't in them or in the files.

### 3. Judge

Work through [references/checks.md](references/checks.md). The script can't judge whether an event fires on the real outcome, whether a duplicate is confirmed or only suspected, or whether consent matters for this audience. Decide each one with the evidence written down.

### 4. Score

Write `audits/<domain>/dim-measurement.json` in the format in [references/output.md](references/output.md) (copy any earlier one to `audits/<domain>/history/dim-measurement-<date>.json` first). Then:

```bash
python3 scripts/score_measurement.py audits/<domain>/dim-measurement.json --pages <n> --container <yes|no|n/a> [--prev <earlier file>] [--health audits/<domain>/score.json] [--founder-led]
```

`--container no` when Tag Manager is present and no export was read. With an earlier audit, `--prev` shows what changed per check and `--health` gives the new Marketing Health total and grade. Use its numbers as printed. Never edit `score.json` or the full audit's report.

### 5. Write

`audits/<domain>/measurement.md` and `audits/<domain>/tracking-plan.md`, with the sections in [references/output.md](references/output.md). The three findings come first, by severity. Every finding names a page, a tag and ID, a container tag, or an export row. Every tracking-plan row says exactly where it fires (the thank-you page, the success callback), never just "on submit".

### 6. Self-check

```bash
python3 scripts/check_report.py <every file you wrote, including dim-measurement.json and response.md> [--exports data/*.csv] [--spelling us|ca|uk] [--max-words 200 in Answer mode]
```

Pass `--spelling` from `brand/voice.md`, or from the company's own site when there's no brand memory. A FAIL means rewrite, then rerun. Then check by reading:
- Every number traces to an export row or column total. No export, no counts.
- No tracking-plan parameter, snippet or URL carries personal data.
- The audience behind every consent flag comes from `brand/`, the user or the site, and is named.
- Suspected problems (a possible duplicate inside an unseen container) are worded as suspected, with the export requested.
- The plan's actions can each start this week, and the 48-hour ones need no new tools.
- Every page, URL and campaign name in a fix or plan row exists in the files, or is marked as new.

### 7. Reply

Use the reply shape for the mode in [references/output.md](references/output.md). Lead with the answer or the verdict. Keep it under about 250 words and don't paste the report into the chat.

## Hand-offs

- **Reads:** `brand/` (audience, offer, voice); the full audit's `audits/<domain>/briefing.md`, `dim-measurement.json` and `score.json`.
- **Writes:** `audits/<domain>/measurement.md`, `audits/<domain>/tracking-plan.md`, and `audits/<domain>/dim-measurement.json` in the full audit's dimension format, so the full audit's scoring picks up the deeper result.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The person who maintains the site can act on every line without asking a question. Nobody can find a number in the report that the files didn't contain. A site that measures well gets a high score and still hears about the one thing that would embarrass it.

A worked example (an online coffee roaster that scores 95 and still leads with two high-severity findings) is in [assets/examples/saltbox/](assets/examples/saltbox/README.md).
