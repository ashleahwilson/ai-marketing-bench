---
name: campaign-intake
description: Turns a messy campaign request (an email, Slack thread, meeting notes or half-filled form) into a structured intake saved in intake/, covering objective and the business result it serves, audience matched to brand memory, offer, CTA, channels, deadline and key dates, budget as a number, assets that exist and assets needed, approvals and who decides, the success metric and where it's measured, risks, and the next pieces of work in order. Asks only the questions whose answers change the plan, in one short round, and records everything else as an assumption to confirm. Checks feasibility (the deadline against the work), checks offers, claims and quotes against brand memory, and surfaces conflicting asks from different stakeholders instead of merging them. Use when the user wants a campaign request turned into a plan or intake, for example "turn this thread into an intake", "scope this campaign", "what do we need to start on this", "can we do this by Friday". Not for writing the brief or the campaign itself.
license: MIT
compatibility: Recommended for large models. On small models it can occasionally assume a value without marking it (a budget currency), so check the Budget line. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Campaign intake

Turns a request into an intake the team can start from without another meeting: what's being asked, whether it can be done by the date, what's still undecided, and what happens next. It doesn't write briefs, copy or ads. It decides what they need to be.

## Ground rules

1. **Missing stays missing.** Every value traces to the request or a line in `brand/`. Anything not given is `unknown: <what> (ask: <who>)`, or `assumed: <value> (confirm: <who>)` when a safe default exists. No invented prices, budgets, dates, conversion rates, forecasts, lead names or results. A plausible guess is still an invention.
2. **Ask only what changes the plan.** One round, at most four questions, each saying what changes with the answer. A clean request gets none. Everything else is an assumption to confirm.
3. **Say when it can't be done.** If the scope can't be delivered by the deadline, the first line of the reply says so, with the reason in plain words, and offers a scoped-down version that can. "Tight" is for things that can be done.
4. **Surface conflicts, never merge them.** When two people ask for different things, record both positions, attributed, mark the affected fields `open`, and name who decides. Don't pick a side, blend them, or invent a compromise.
5. **Brand memory decides what can be said.** A held, banned or unsourced claim, an uncleared customer name, or an audience the brand doesn't serve stays out of the fields and is flagged with what would clear it. Push back in a line, offer what does work, and carry on with the rest of the intake. Never refuse, never lecture.
6. **Names come from the files.** Every person in the intake is named in the request, the user's message or `brand/`. If the user says "we decided" without naming who, write "you". Never use a name from anywhere else, including the environment you run in.
7. **Never overwrite the user's files.** The request files and `brand/` are read, never edited. An intake with the same slug is updated only in Update mode, with a line under Updates.

## Pick the mode

| The request… | Mode |
|---|---|
| A request to turn into an intake (default) | **Draft:** write the full intake, open items marked, questions in the reply |
| "Walk me through it", "ask me first", "before you write anything" | **Guided:** the questions only (at most four, each with the likely answer from brand memory), no file yet |
| Answers or decisions on an existing `intake/<slug>.md` | **Update:** apply them to that file, re-check everything they touch, log them under Updates |

## Workflow

```
- [ ] 1. Load: the request files, brand/, any existing intake/ file
- [ ] 2. Build the fact list: every value with its source
- [ ] 3. Judge: questions, feasibility, conflicts, claims, audience, risks (references/judgment.md)
- [ ] 4. Write intake/<slug>.md (references/intake-format.md)
- [ ] 5. Self-check: run scripts/check_intake.py, then the six questions in judgment.md
- [ ] 6. Reply in the fixed shape
```

### 1. Load

List the project folder and look for `brand/`, even if the user didn't mention it. Read `BRAND.md`, `audiences.md`, `offer.md`, `proof.md`, `claims.md` and `rules.md` where they exist. Read every request file in full, including who wrote each message and when.

Today is the date the user gives. Otherwise use the current date. Write it in the file header: every date check depends on it.

**No `brand/` folder?** Work from the request only. Write `Brand memory: none (provisional)`, set Brand audience match to `none: no brand memory`, don't add any fact about the company that isn't in the request, and end the reply by offering to set up brand memory from what the request already says.

### 2. The fact list

Before writing, list each value and where it came from: a named person in the request with the date of their message, or `brand/<file>` with its status. Resolve dates to `YYYY-MM-DD` relative to today. Write budgets as digits (`$4k` → `4000`, `$2,500/month for two months` → `2500 per month; 5000 total`).

### 3. Judge

Work through [references/judgment.md](references/judgment.md) in order:
- **Questions:** which unknowns change the plan, and which become assumptions.
- **Feasibility:** working days available against the longest chain of work, any constraint in the request (a person away, footage that doesn't exist). Decide fits, tight or doesn't fit, and build the scoped-down version if needed.
- **Conflicts:** every point where two people want different things.
- **Claims:** every headline, claim, price, discount, quote and name the request wants used, against brand memory.
- **Audience:** match to a brand memory segment; narrow anything outside what the brand serves.
- **Risks:** consent, past dates, stale assets, people, measurement.

### 4. Write the intake

Follow [references/intake-format.md](references/intake-format.md) exactly: the header, the 19 `- Field: value` lines under `## Fields`, then Feasibility, Conflicts, Claims and brand checks, Assumptions to confirm, Questions, Risks, For the next step, Updates. Slug: lowercase, hyphenated, two to five words from the campaign name (`intake/january-catch-up.md`). Write exactly one intake file per request. Inside the file, describe the reasoning in plain words ("about 6 working days of work"), never the method ("the lead-time table", "the checker").

Route the work with the plain-language route terms in the format file, in order: unblocking work first (a brand memory update, a claims review), then briefs, then builds, then pre-launch checks. Work with no step here is `other: <work>`. Describe work in plain words; never write internal tool names in the file or the reply.

### 5. Self-check

```bash
python3 scripts/check_intake.py intake/<slug>.md --today <YYYY-MM-DD> --brand brand/ --request <request files>
```

Fix every FAIL and rerun. Act on each WARN: a floor above the days available means the feasibility verdict must say so. For every CLAIM line, make sure the intake handles it under Claims and brand checks (a discount or target the requester set is their fact; a performance claim, comparison or certification needs a source or legal review). Then answer the six self-check questions at the end of judgment.md. A "no" means fix the file.

### 6. Reply

```
**Intake:** written to intake/<slug>.md (<status>) | not written yet: <one line why>

**Recommendation:** <one or two lines: go as asked / go with the scoped version / decide X first. If the deadline can't be met, this line says so and why.>

**Questions** (only if any; at most 4)
1. <question>: <what changes with the answer>. Likely: <answer from brand memory> (only when brand memory actually suggests one; otherwise leave "Likely" out)

**Flags**
1. <feasibility, conflict, claim or risk, one line each, with where it comes from>

**Assumed until you say otherwise:** <one line>

**Next:** <the route, in plain words, in order>
```

- Lead with the decision the user has to make. The detail is in the file, not the reply.
- **Length:** a `ready` intake: under 150 words (at most three flags). Update mode: under 200 words. Anything else: under 300 words. Count before sending; cut flags, not the recommendation.
- **Flags** are only what changes a decision or could stop launch: at most five, one line each. Leave housekeeping (who owns a check, timing advice, footers the next step adds anyway) in the file. URLs the user or brand memory gives are real, even reserved test domains such as `.example`.
- **Guided:** the "Intake" line says not written yet, then the questions. Nothing else.
- **Update:** what changed (one line), the new status, and anything the answers broke or still leave open (for example a customer name that still needs permission). Under 200 words.
- Talk to the user in the second person. Never mention the checker, this skill, its references or other tools by name.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

Someone who wasn't in the thread reads the intake in three minutes and knows what's being built, by when, for whom, with what money, and what's still undecided and who decides it. Every number traces to a person or a brand memory line. Disagreements are visible, not smoothed over. If the date can't work, the team learns that today, along with what can be done instead.

A worked example (a Tallyhouse patio-season campaign that comes back ready, with its headline claim held) is in [assets/examples/tallyhouse-patio/](assets/examples/tallyhouse-patio/README.md).
