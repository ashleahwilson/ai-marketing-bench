---
name: agency-brief
description: Writes the brief a company sends to an outside agency, freelancer or contractor, and reviews what comes back. The brief covers background, business objective, audience, deliverables with specs, mandatories (voice and rules, approved claims, claims not to use, legal, accessibility, ownership of accounts and files), what not to do, budget and payment, timeline with review rounds, approvals, success metrics, assets and the questions the agency must answer. Builds a shareable brand pack with only what an outsider needs, leaving out customer lists, margins, internal prices, credentials, unconfirmed proof and anything marked internal, and says what it left out. Asks instead of inventing a budget, timeline or target. Reviews a proposal or first draft against the brief: deliverables, mandatories, claims, budget, timeline, terms and red flags such as guaranteed rankings or agency-owned accounts. Use when the user wants an agency brief, a freelancer or RFP brief, a brand pack for a contractor, or a proposal reviewed.
license: MIT
compatibility: Recommended for large models. On small models it occasionally invents a minor problem in a review (a date mismatch, a rewrite of the brand's own approved line), so check review points. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Agency brief

Writes the brief that goes to an outside agency, freelancer or contractor, the brand pack that goes with it, and the review of what they send back. The brief decides what the agency must deliver, within which rules, for how much and by when. It doesn't do the agency's work.

## Ground rules

1. **Facts come from the user or confirmed brand memory.** Every name, price, date, figure and claim in the brief traces to the request or a `confirmed` line in `brand/`. Unknowns are `TBD: <what's missing>`. A plausible guess is still an invention.
2. **Budget, timeline and targets are the user's.** Never estimate a budget, a fee, a date or a success target. Missing budget or timeline means asking (see Modes). A metric with no target says "target to agree in kickoff".
3. **Outsiders get only what they need.** Customer lists, margins, floor and internal prices, credentials, internal results, unannounced changes, unconfirmed proof and anything marked internal stay out of every file the agency sees, even when the user asks to include them. Say what you left out and what to share instead, in a line each ([references/sharing.md](references/sharing.md)). No lecture, and no refusing the brief.
4. **Unapproved claims are listed as claims not to use.** A claim brand memory holds as unsubstantiated goes in the brief quoted, marked "not approved for use", so the agency doesn't copy it from the website. It never appears as a selling point.
5. **The company owns its accounts, data and final files.** Every brief proposes that, with the agency working through user access, never shared passwords. Review mode treats the opposite as a red flag.
6. **The client's conventions win.** Spelling, tone and terms follow brand memory (US spelling if brand memory says so), not the environment's defaults. With no brand memory, keep the user's own conventions.
7. **Never overwrite or edit.** Brand memory is read only. A file that exists gets `-v2`.
8. **The user and the agency see the business, not the machinery.** Never mention scripts, checks, file internals, source tags, status labels or skill names in the reply or in any file the agency reads.

## Modes

| The request… | Mode |
|---|---|
| Has the deliverable, budget and timeline | **Write** (default): brief + brand pack |
| Is missing the budget or the timeline (or what's being made) | **Ask:** one round, at most five short questions, no file. Show in two lines what you can already fill from brand memory, and offer to draft now with the gaps marked `TBD` |
| Says "just draft it", "fill in what you can" | **Write with gaps:** `Status: draft (gaps marked TBD)`, gaps listed first in the reply |
| Asks only for a brand pack ("brand info for the freelancer", "nothing else") | **Pack only:** the brand pack, no brief |
| Gives a proposal or a first draft to check | **Review** ([references/review.md](references/review.md)) |
| Says "walk me through it" | **Guided:** confirm objective and deliverables, then budget and terms, then write |

## Workflow

```
- [ ] 1. Load: the request, brand/, the brief and proposal if reviewing
- [ ] 2. Pick the mode; ask now if budget or timeline is missing
- [ ] 3. Fact list: every fact the brief uses, with its source; everything left out, with why
- [ ] 4. Draft the brand pack, then edit it for the reader
- [ ] 5. Write the brief
- [ ] 6. Self-check both files
- [ ] 7. Reply in the fixed shape
```

### 1. Load

List the project folder and look for `brand/` even if the user didn't mention it. Read `BRAND.md`, `offer.md`, `audiences.md`, `positioning.md`, `proof.md`, `claims.md`, `rules.md`, `voice.md`. Open any file the user asks you to attach, so you know what it contains and can leave it out properly.

**No `brand/`?** Write from the request only, mark the brief `Status: provisional (no brand memory)`, and put brand guidelines, approved claims and assets under `TBD` with a question each. Don't write a brand pack from nothing: say what it needs. The last line of the reply always offers to set up brand memory so the next brief starts from it. Don't add facts about the event, venue, market or industry from general knowledge.

### 3. The fact list

Before writing, list each fact with its source (the request, or the brand file and status). Cut anything without one. Separately list what you're leaving out of the agency's files and why: this becomes the "Left out" lines in the reply.

### 4. The brand pack

```bash
python3 scripts/agency_brief.py extract brand/ --out briefs/agency/<project>-brand-extract.md --for "<recipient>" --contact "<approver>"
```

It drafts the pack from confirmed lines, strips source tags, leaves out internal files and lines, credentials, `TBD`s and assumed facts, lists unapproved claims under "Claims not to make", and adds a naming note to unconfirmed proof. It prints what it left out. Then read the draft and edit it for the reader: merge duplicates, cut lines the recipient doesn't need, and keep only what the work calls for. The format is in [references/brief-format.md](references/brief-format.md).

### 5. The brief

Write `briefs/agency/<project>.md` in the fixed format in [references/brief-format.md](references/brief-format.md), with all twelve sections. Anything you propose that the user didn't state (review rounds, accessibility standard, ownership clause, response date, an extra deliverable) goes in plainly and is listed under "Before you send" for the user to confirm. Review rounds are never left `TBD`: if the user gave none, propose them (for example two rounds, with the company's turnaround in business days) and list them to confirm. "Before you send", gap lists and notes about brand memory belong in the reply only, never inside the brief or the pack.

### 6. Self-check

```bash
python3 scripts/agency_brief.py check briefs/agency/<project>.md --kind brief --brand brand/ --exclude <files the user asked to attach>
python3 scripts/agency_brief.py check briefs/agency/<project>-brand-extract.md --kind extract --brand brand/ --exclude <same>
```

Fix every FAIL and rerun. Then check by judgment:
- Is every budget figure, date, name and target one the user gave? Nothing estimated?
- Does any unapproved claim appear as anything but "not approved for use"?
- Could the brief be forwarded to a competitor without harm?
- Could the agency deliver from it without asking a question, apart from the `TBD`s?
- Does the spelling follow the brand's convention?

### Review mode

```bash
python3 scripts/agency_brief.py review --brief briefs/agency/<project>.md --proposal <file>
```

It lists each deliverable as covered or possibly missing, the money figures side by side, red-flag phrases, phrases the brief bans, and sample ad lines over the platform's character limits. Confirm each line by reading the proposal: a match is a lead, not a verdict. For ad length, trust the measured lines: each `|`-separated part of a headline is its own headline. The proposal's own date, formatting and writing style are never problems. Then score it with [references/review.md](references/review.md), and write the review to `briefs/agency/<project>-review-<agency>.md`. If there's no brief, review against what the user tells you and say which checks couldn't run.

## Reply shapes

**Write / Write with gaps / Pack only**

```
**Ready to send** | **Draft: <n> gaps to fill before sending** | **Brand pack ready**: <one line on what it's for>

**Files:** briefs/agency/<project>.md · briefs/agency/<project>-brand-extract.md

**Left out of what they'll see** (only if something was)
- <item>: <why, in a few words>. <what to share instead>

**Before you send**
1. <gap or proposal to confirm>
```

Under 200 words. The gap count in the first line equals the number of items under "Before you send". If the request names the offer or outcome ("ads for our free month-end review"), write the objective from it rather than listing it as a gap. If a credential was found in brand memory, the first "Left out" line says to remove it from brand memory and change it. Never repeat the credential.

**Ask**

```
Before I write this, I need:
1. <question>
...
From brand memory I already have <two lines>. Say "draft it" and I'll write it now with those marked TBD.
```

**Review**

```
**Recommendation:** Accept | Accept with changes | Send back | Decline: <one-line reason>

| Area | Result |
|---|---|
| Deliverables | <n of n, missing #> |
| Mandatories | ... |
| Claims | ... |
| Budget | <their total vs the brief> |
| Timeline and terms | ... |

**Red flags** (quote · why it matters · ask for)
**Send back to them** (a numbered list 1, 2, 3, never bullets, paste-ready)
**Fine as proposed:** one line
```

For Accept, the reply is the recommendation, the table and at most three clarifications, under 200 words; detail goes in the review file. An Accept has nothing "required before signing": if something must change first, the recommendation is Accept with changes. Never paste the review file into the reply; the reply summarizes it. Any other review reply stays under 400 words.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The agency could start work from the brief and the pack without a follow-up call, and nothing in either would hurt the company if forwarded. Every number in the brief is one the user gave. A bad proposal comes back with the exact lines to change; a good one comes back as Accept in a short table.

A worked example (a Tallyhouse brief for a food photographer, with its brand pack) is in [assets/examples/tallyhouse-photo/](assets/examples/tallyhouse-photo/README.md).
