# Output

## Contents
- measurement.md
- tracking-plan.md
- dim-measurement.json
- Reply shapes
- Writing rules

## measurement.md

Save to `audits/<domain>/measurement.md`. Under about 1,000 words. Sections, in this order:

```
# Measurement: <Company>
<date> · Sources: <n HTML pages; container export yes/no; analytics export <period> or none> · Confidence: <level>
<"Provisional: no brand memory, audience assumed <x>" when brand/ is missing>

## Verdict
<One or two sentences: what the site can measure today, and the first thing to fix.>
Measurement score: <n>/100 (M1 <a>/30 · M2 <b>/30 · M3 <c>/15 · M4 <d>/15 · M5 <e>/10)

## The three things that matter most
1. **<finding>** Evidence: <page, tag ID or quoted line>. Fix: <a concrete action>.
2. …
3. …

## What the site can measure today
| Tag | ID | Pages | State | Before consent? |
|---|---|---|---|---|
Conversions: <each conversion-like event, what it fires on, and whether that's a real outcome>
Forms: <each form, its fields, and whether a submission is tracked>
UTM handling: <internal UTMs, campaign naming>
<Container: tags, triggers and variables that matter, when an export was read>
<From the export: figures quoted exactly, with the period, when one was supplied>

## Privacy and consent
<What loads before consent, the audience it matters for, personal data found. One line: this is a flag to review, not legal advice.>

## Not observable
<What the files can't show, and the access that would show each item.>

## Plan
- Next 48 hours: <1–3 actions>
- Next 2 weeks: <2–4 actions>
- Next 3 months: <2–4 actions>

## Measurement checklist
| ID | Check | Points | Evidence |
|---|---|---|---|
| M1 | Analytics configured on every page | <a>/30 | … |
| M2 | Conversions tracked | <b>/30 | … |
| M3 | Ad platform tags | <c>/15 | … |
| M4 | Hygiene | <d>/15 | … |
| M5 | Consent basics | <e>/10 | … |
Score: <n>/100. <If an earlier audit exists: earlier <x>/100; Marketing Health total <before> → <after>, grade <g>.>
```

## tracking-plan.md

Save to `audits/<domain>/tracking-plan.md`. One row per event. Keep it to the events a decision depends on: usually 4–8.

```
# Tracking plan: <Company>
<date> · Analytics: <tool and ID> · Ad tags: <names> · Status key: keep / fix / new

| Event | Fires when | Where | Parameters | Conversion? | Sent to | Status |
|---|---|---|---|---|---|---|
| generate_lead | /thanks page view after the review form posts | thanks.html | form_id, locations | Yes (key event) | GA4, Meta (Lead) | new |

Naming: lowercase with underscores, object then action where there's no standard name. Use the analytics tool's recommended names where one exists (generate_lead, sign_up, purchase).
Parameters never include email, name, phone, address or free-text form contents.
Campaign links: utm_source, utm_medium, utm_campaign in lowercase; never on internal links.
Verify: <how to confirm each event fires once, e.g. a test submission in DebugView>.
```

Every row names the exact page, URL or callback where it fires, taken from the files (a form's action, a success callback, a confirmation URL the site states). A page that doesn't exist yet is marked "(new page)", and a value you'd otherwise invent (a campaign name, a URL) is copied from the source or left for the user to fill. "On form submit" is not enough: say whether it's the thank-you page, the success callback or the submit attempt.

## dim-measurement.json

The hand-off to the full marketing audit, in its format. Save to `audits/<domain>/dim-measurement.json`:

```json
{"dimension": "measurement", "assessable": true, "confidence": "medium",
 "checks": [{"id": "M1", "points": 30, "max": 30, "evidence": "…"}],
 "score": 73,
 "findings": [{"severity": "high", "check": "M2", "finding": "…", "evidence": "…", "fix": "…"}],
 "strengths": ["…"], "not_observable": ["…"], "source": "measurement deep dive, <date>"}
```

If the file already exists, copy it first to `audits/<domain>/history/dim-measurement-<date>.json` (the history folder keeps it out of the full audit's scoring), then write the new one. Never edit `score.json`, `MARKETING-HEALTH.md` or the one-pager: report the new total and say the full audit's scoring needs rerunning to update them.

## Reply shapes

**Draft (the default).** Under about 250 words:
1. The verdict and the measurement score (with the earlier score and the total's change, if any).
2. The three findings, one line each.
3. The 48-hour actions.
4. What wasn't observable, and what access would raise confidence.
5. Where the files are.

**Answer (a question about numbers, or "is X working").** Under 200 words (check it), no files unless asked:
1. The direct answer in the first sentence: the count isn't visible in page HTML; or "No, it isn't configured".
2. What the source does show that bears on the question (the tag, the event, what it would collect).
3. What would answer it: the access or export, or the one-line fix and how to verify it.
4. An offer of the full deep dive.
Anything else you noticed (a consent flag, an untracked form) gets one line at most, or waits for the deep dive.

**Guided.** Findings so far (what loads, what's tracked, the gaps), the candidate conversions with a recommendation and the reason, the consent recommendation when the audience includes Canada, the EU or the UK (hold the tags until consent: consent mode defaults set to denied, or scripts released on accept), then at most three questions, the first being which event counts as the conversion. Stop. No tracking plan or score until they answer.

**Plan (set up tracking).** The tracking plan, plus three lines on what exists today. If the request includes personal data, the pushback comes first, in two or three sentences, then the plan without it.

## Writing rules

- Lead with the decision, not the method.
- Name the page, the tag and the ID. Quote source lines exactly.
- Fixes are actions someone can start this week, with the exact line or setting where possible.
- Spelling and style follow the company's brand memory (`brand/voice.md`). With no brand memory, follow the conventions of the company's own site.
- Never mention scripts, checks by file name, skill names or how the report was produced beyond "from the page source" and "from the container export".
- In replies, name checks in plain words ("consent basics drops to 5 of 10"), not by code alone, and never describe your own procedure ("no score until you answer"): say what you need from them and why.
- Always write the real tag ID from the source (`290018833471652`), never a pointer such as "the ID on line 8".
- The spelling convention applies to every file you write, including `dim-measurement.json`.
