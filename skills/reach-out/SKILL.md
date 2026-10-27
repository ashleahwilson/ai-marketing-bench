---
name: reach-out
description: Drafts B2B prospecting outreach, including cold and warm emails, LinkedIn connection notes and DMs, follow-ups and short sequences, for a named contact, an account, a list or a buying signal. Every claim is traced to a source, and drafts are checked for compliance and deliverability before being staged for approval. Use when the user wants to email, message, follow up with, re-engage or get in front of a prospect, even without the word "outreach", for example "write to the CFO at Acme", "draft a sequence for these leads", "follow up with webinar attendees", "message her about her post", "reach out to accounts that just raised". Also use for outreach strategy questions such as cadence, subject lines or tone, and when the user gives feedback on a draft. Not for replying to an existing customer thread or for marketing newsletters.
license: MIT
metadata:
  version: "3.2.1"
  author: "Ashleah Wilson"
---

# Reach out

Turns a reason to contact someone into outreach a person would write: short, specific and true. Nothing goes out without the user's say-so.

## Ground rules

These hold at every step.

1. **Never send, schedule or enrol anyone** unless the user says so in this conversation. With a sending tool connected, create drafts only.
2. **Every fact in the copy has a source.** That covers the prospect, the proof, the sender and the signal, from brand memory, the user or a cited source. If you can't say where a detail came from, it doesn't go in. A plausible guess is still an invention.
3. **Deliver what was asked.** One email gets one email, plus an offer of the rest. A rewrite gets the rewrite. A list gets the list.
4. **When instructions conflict,** follow this order: the user's request in this conversation, then `outreach-profile.md`, then the [signal matrix](references/signal-matrix.md), then this file.
5. **If the user asks for something this skill advises against** (for example "open by congratulating them"), write their version, give one sentence on how the reader is likely to react, say which version you'd send, and write the alternative underneath. Don't refuse, and don't lecture.
6. **Every contact the user supplies gets an outcome:** drafted, or held with a reason and a draft ready.

## Workflow

```
- [ ] 1. Profile: load outreach-profile.md
- [ ] 2. Signal: find the row in the signal matrix
- [ ] 3. Ledger: list the facts the copy may use
- [ ] 4. Draft
- [ ] 5. Check: run the script, then the judgment checks
- [ ] 6. Gate: compliance and deliverability
- [ ] 7. Stage: present for approval
```

### 1. Profile

Look for a `brand/` folder in the project (the brand-memory format): read `BRAND.md`, `offer.md`, `audiences.md`, `proof.md`, `voice.md`, `senders.md`, `rules.md` and `results.md`. Use facts tagged `confirmed` as fact. Flag `provisional` facts under "Check before sending". Never state `assumed` facts. Treat proof marked `named: no` or `unconfirmed` as anonymous.

No `brand/`? Read `outreach-profile.md` if it exists (the older single-file format), and suggest moving it into brand memory. Sender details, proof and rules the user gives in the conversation count as profile data for this draft. If there's neither, draft anyway: use `[Your name]` and `[your role]`, mark the voice provisional, and after the draft offer the three-question setup in [references/learning.md](references/learning.md).

**Before drafting to anyone, check who must not be contacted.** Skip anyone listed in `outreach/suppression.csv` (opt-outs from the handle-reply skill), anyone with an open follow-up date in `outreach/reply-log.csv` (draft the follow-up then, not a new first touch), and anyone under "Not contacting" in an `accounts/<company>/contacts.md` file. Report each one as held, with the reason. If a contacts file exists, use its Role, Persona, Signal and Source fields for the ledger.

Check connected tools (CRM, email, enrichment, search) for what's already known before researching. If there's an unsent draft to the same person, edit it rather than starting a new one.

### 2. Signal

Open [references/signal-matrix.md](references/signal-matrix.md) and find the row for why you're writing today. The row decides five things: whether the copy can name the signal, how fresh it must be, who to write to, how strong the ask is, and the default number of touches. For more than one recipient, also open [references/lists.md](references/lists.md).

**If the signal is weak:**
- **Only persona pain is available:** draft from it, say in the reasoning that it's the weakest kind of hook, and name the one fact that would strengthen it.
- **No persona and no signal** (for example "email these 500 companies"): don't draft for the whole list. Propose narrower slices and ask which to use.
- **A persona but no signal** (for example "60 HR directors at hospitals"): draft the persona template on persona pain, flag it as the weakest hook, and suggest signals that would sharpen it. Don't refuse.

### 3. Ledger

Before drafting, list every fact the copy may use, with its source. Put it at the top of the drafts file:

```
FACTS
- prospect: Lakeshore plans to double technicians in Ontario | user, 2026-10-02
- proof: Arctic Air (180 techs) cut unbilled return visits 31% in Q1 | user | named: unconfirmed
- sender: [Your name], Fieldline | profile missing
ASSUMED
- Lakeshore has fewer than 500 employees | not given
```

Anything the user didn't give and you can't cite goes under `ASSUMED` and into "Check before sending". It must not appear in the copy as fact. Don't add details to proof: if the user said "cut close from 12 to 5 days", don't add how they did it.

### 4. Draft

Each first message makes a three-part argument in as few words as possible: **why you, why now, why us.** The signal answers "why now", the persona answers "why you", and one proof point answers "why us".

**First email**
- 50 to 90 words, not counting the greeting, signature or opt-out line. For executives, 35 to 60. A limit set by the user or profile overrides both.
- Two subject lines to choose from, each 1 to 4 words, lowercase except proper nouns. They should read like an internal note, never like a headline.
- Plain text. No links, images or attachments.
- Open with what the signal means for the reader, in their terms.
- One proof point at most, with a name or a number, sized near the reader's company. If there's no proof, leave it out. Never use a placeholder or "teams like yours".
- One ask. The default is an interest question ("open to a look at …?"). Use a concrete offer when you can deliver it. Use a meeting ask only for inbound and strong warm signals.
- Pitch at the reader's level: executives care about risk and money, managers about throughput, practitioners about their workload.
- Write in the language and spelling the profile specifies. Sign off with the profile's sender, or `[Your name]`.

**LinkedIn**
- Connection note: none, or under 300 characters.
- First DM: under 500 characters. Say who you are in one line, respond to their topic, and end with a question. No product pitch or statistics.

**Follow-ups**
- Use the matrix's touch count. The default is three, on days 0, 3 and 8.
- Step 2 is a reply in the same thread with a new angle, shorter than step 1. Its subject is "Re: " plus step 1's subject, exactly. A new angle means a different point, not step 1's proof again.
- The last step closes the loop in under 50 words and adds no new pitch.
- Add a fourth step only with a reason, because complaint rates climb after three.

### 5. Check

Write the drafts, with the ledger at the top, to a file in the working folder named after the prospect (for example `outreach/drafts-lakeshore.txt`). Then run:

```bash
python3 scripts/check_draft.py drafts.txt --facts
```

Add `--max-words N` when the user or the profile sets a word limit, and `--summary` to get a single line for the reply. Fix every FAIL and rerun until it passes. Treat WARNs as things to look at. The file format is in the script's header.

Then make the checks a script can't:
1. **Read from the second sentence.** If nothing is lost, the opener was throat-clearing. Cut it.
2. **Swap the company.** If the email still works for a competitor of the prospect, it isn't specific enough.
3. **Trace the facts.** Every claim should be in the ledger. Write tool adoption as a pattern ("after a NetSuite move"), not as their event ("after the NetSuite move").
4. **Read it for AI tells.** Run [references/writing-check.md](references/writing-check.md).

### 6. Gate

Run [references/send-gate.md](references/send-gate.md): consent basis by recipient country, the required signature and opt-out, plain text and links, sequence length, and batch size. It warns rather than blocks. Failed items go first in "Check before sending".

### 7. Stage

Keep the reply short:

1. **Send this one:** the recommended message or sequence, ready to copy.
2. **Why:** recipient, signal (with source and date), persona angle, and voice (from the profile or provisional). Three or four lines.
3. **Alternatives:** only if useful, such as the second subject line or the user's requested variant.
4. **Check before sending:** at most three items, compliance warnings first, then assumptions and assets the copy promises. List anything beyond three in one line.
5. **Checked:** one plain line saying what was verified, for example "Checked: length, subject, sources, opt-out". Mention any open warning in plain words.

Keep everything outside the copy short: about 120 words for a single email, and about 250 for a sequence or list, beyond the templates. Write about the outreach, never about this skill, its rules, files or scripts. The prospect's copy contains only what the prospect should read: no planning notes ("same thread, new angle") and no internal caveats. Fill every placeholder the user has already answered (company, product, sender). Use the proof as the user gave it. If permission to name a customer is unknown, keep the name and flag it, rather than anonymising it silently.

When the user reacts to a draft, follow [references/learning.md](references/learning.md) so the lesson is saved in the profile.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The prospect could reply in one line, and wants to. Every sentence is about them, true, and traceable. A stranger reading the draft couldn't swap in another company's name. The user approves it with a small edit. The next draft is already better, because that edit became a rule in the profile.
