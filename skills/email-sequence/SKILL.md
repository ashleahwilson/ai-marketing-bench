---
name: email-sequence
description: Writes lifecycle email sequences for people who opted in or are customers, including welcome and onboarding series, nurture after a lead magnet, trial-to-paid, re-engagement, post-purchase, event follow-up and newsletters. Each email gets its job, trigger and timing, subject and preview text, body, one call to action, and exit or branch rules, with the consent basis, unsubscribe and mailing address built in (CASL, CAN-SPAM). Every figure, result, deadline and quote traces to brand memory or the user; it never invents proof, scarcity or urgency. Use when the user wants an email sequence, drip, nurture, onboarding emails, a welcome series, a win-back or re-engagement flow, webinar follow-ups, or wants an existing sequence checked and fixed, for example "write the emails for people who download the guide", "trial-to-paid emails", "follow up with webinar attendees". Writes the sequence to a file a reviewer or sending tool can use. Not for cold outreach to people who haven't opted in (use reach-out).
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Email sequence

Writes the emails people get after they sign up, buy, register or go quiet. Each email has one job, every fact is true, and the sequence knows when to stop.

## Ground rules

1. **Consent comes first.** A lifecycle sequence goes only to people who opted in, are customers, or asked for something. A bought, rented, scraped or enriched list is cold outreach: don't write the sequence for it. Say so in a line, route the cold part to `reach-out`, and offer a way to get those people to opt in. See [references/compliance.md](references/compliance.md).
2. **Every fact has a source.** Figures, results, prices, names, quotes, URLs, dates, limits, deadlines, product features, service details (call lengths, setup times, who answers) and options offered to the reader ("get fewer emails") come from the user, the brief or `brand/`. Missing stays missing: use a marked placeholder (`[link: setup page]`) and list it. A plausible guess is still an invention.
3. **No invented proof or urgency.** No made-up customers, results or testimonials, even when asked to "make them sound real". No countdown, "only N spots left" or deadline unless the limit or date is on record. Write the sequence without it, say why in one sentence, ask whether a real one exists, and give every email a true reason to act now drawn from the facts (the next month-end, a trial end date, an event date).
4. **Brand rules beat the brief.** If a brief asks for a claim `brand/rules.md` bans or `claims.md` hasn't substantiated, leave it out and tell the user about the conflict.
5. **Every marketing email carries the footer**: the sender's mailing address and a working unsubscribe. Never write a plausible address; use `[mailing address: needed before sending]`.
6. **Push back without refusing or lecturing.** Do the part that's sound, decline the part that isn't in a sentence, and give the honest alternative.
7. **Nothing goes out.** Never send, schedule or load anything into a sending tool. Never overwrite the user's files: fixes go in a new file.

## Modes

- **Draft** (default): the full sequence, written to a file, ready for review.
- **Guided** (the user asks to be walked through it, or a material decision is missing such as the goal or the entry offer): give the recommendation and the sequence plan (each email's job and timing, the exit rule), ask at most five questions, and stop. Count question marks: five in total, one per numbered item, no sub-questions. Write no email bodies until they answer. Don't propose an incentive as fact; ask whether one exists.
- **Check and fix** (the user gives an existing sequence): run steps 5 and 6 on it, write the fixed version to `<name>-fixed.md`, and report what changed and what's still open. Keep every email and fix it in place: never delete an email or merge two. Keep the user's working URLs and confirmed facts. Name every problem you fixed, including each email that was over the word limit (with its count).

## Workflow

```
- [ ] 1. Consent: who receives it, and how did they get on the list?
- [ ] 2. Load: brief, brand/, and anything the user points to
- [ ] 3. Ledger: FACTS and OPEN
- [ ] 4. Map: type, emails, jobs, timing, exits (Guided mode stops here)
- [ ] 5. Write: email/sequence-<slug>.md
- [ ] 6. Check: script, then judgment checks
- [ ] 7. Reply in the fixed shape
```

### 1. Consent

Find out how the recipients got on the list and where they are. Use the table in [references/compliance.md](references/compliance.md). Bought or scraped list: still read the brief and brand memory, then stop, and reply with the pushback in ground rule 1 (under 250 words, measured, no sequence and no email copy). Unknown: draft anyway, write `Consent basis: TBD`, and ask one question. Mixed segments (for example event registrants with and without the marketing checkbox): split them, and give the no-consent segment only what they asked for.

### 2. Load

Read `brand/` (the brand-memory format): `BRAND.md`, `offer.md`, `audiences.md`, `proof.md`, `claims.md`, `voice.md` (especially "By channel" → "Email"), `senders.md` and `rules.md`. Use `confirmed` facts as fact, flag `provisional` ones, never state `assumed` ones. Proof marked `named: no` is used without the name or any detail that identifies the customer. Proof whose permission to reuse or name is `unconfirmed` stays out of the copy entirely, quote included: list it under Check before sending as proof to clear. Never imply a customer relationship that isn't on record ("an owner we work with").

**No `brand/`?** Draft from the conversation, mark the file `Status: provisional`, use placeholders for the sender's address and every link you weren't given, and after the reply offer to set up brand memory (the `brand-memory` skill).

### 3. Ledger

List every fact the emails may use, with its source, and every gap. This goes at the top of the sequence file ([references/sequence-file.md](references/sequence-file.md)). A real deadline, limit or sunset rule gets its own `deadline:`, `limit:` or `sunset:` line.

### 4. Map

Pick the type and start from its default shape in [references/sequence-types.md](references/sequence-types.md), then cut. For each email: its job (one), trigger and timing, the call to action, and the exit or branch condition. Everyone exits on unsubscribe and when they do what the sequence asks (the goal, not an earlier step: completing a setup step skips that step's emails, it doesn't end a trial-to-paid sequence). Say what happens after the last email. Timing is relative to the trigger, so never hard-code a calendar date in a relative-timed email: a reason to act now must be true for everyone who receives it ("before your next month-end", not "before October 31").

### 5. Write

Write each email to the rules in [references/writing.md](references/writing.md): subject (60 characters at most) and preview text that adds to it, a body inside the brand's email word limit, one call to action with one link, the sign-off the voice asks for, and the footer. Use only the unsubscribe link or merge tag recorded in `brand/senders.md`; without one, write `[unsubscribe link: from your email tool]`. Save the whole sequence, ledger first, to one file, `email/sequence-<slug>.md`; if you revise it, overwrite your own file rather than leaving a second version beside it. in the format in [references/sequence-file.md](references/sequence-file.md).

### 6. Check

```bash
python3 scripts/check_sequence.py email/sequence-<slug>.md --brand brand/
```

Add `--max-words N` when the user sets a limit. Fix every FAIL and rerun until it passes: a FAIL means rewrite, not hedge. OPEN items need a fact only the user has: list them, don't fill them. Then run the judgment checks at the end of [references/writing.md](references/writing.md): one job per email, exit logic, consent per segment, facts, voice.

### 7. Reply

```
**Recommendation:** <one line: the sequence, how many emails over how long, the goal> (or: Hold, and why, in one line)

**The sequence**
| # | Job | Timing | Subject | CTA | Exit or branch |

**Emails:** in email/sequence-<slug>.md (paste them here too if there are 3 or fewer, or the user asked)

**Consent and compliance:** consent basis, footer (address, unsubscribe), any segment held back and why.

**Changed from your request:** only if something was left out (a banned claim, invented urgency, proof that doesn't exist), one line each with the honest alternative.

**Check before sending:** at most 4 items, OPEN items first (address, links, proof).
```

- Lead with the recommendation. Keep the reply under about 350 words plus any pasted emails.
- In Guided mode, the reply is the recommendation, the plan table, and the questions.
- For a pushback with no sequence (a bought list), the reply is the recommendation line, why in two or three sentences, and the alternatives.
- Talk to the user in the second person. Never mention this skill, the checker, its levels, the ledger format, or which tools or skills are installed. Refer to `reach-out` as the cold outreach skill, without saying whether it's available; say what's missing in plain words ("the mailing address isn't in brand memory").

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A subscriber gets emails they expected, each one useful on its own, and stops getting them the moment they act or leave. A reviewer can approve the file without a follow-up question. Nothing in it depends on a fact the skill guessed.

A worked example (a Tallyhouse post-purchase sequence for catch-up bookkeeping clients) is in [assets/examples/tallyhouse-catch-up/](assets/examples/tallyhouse-catch-up/README.md).
