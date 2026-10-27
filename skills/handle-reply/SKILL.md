---
name: handle-reply
description: Handles replies to B2B prospecting outreach. Sorts each reply (interested, question, objection, not now, referral or wrong person, out of office, unsubscribe, hostile, bounce) and does the right thing for each: a short reply that answers only what was asked, a hold with a follow-up date, or nothing. Opt-outs are honoured at once: no pitch, at most a one-line confirmation, and the address goes on a suppression list. Answers come only from brand memory and the original thread; a question they can't answer (an unlisted price, a feature, a security certification) gets a holding reply and a note to the user, never a guess. Referrals get a first email to the new person that states the referral truthfully. Writes reply drafts, a status log and the suppression list; never sends. Use when a prospect writes back, for example "handle these replies", "she replied, what do I send", "he said remove me", "answer his pricing question". Not for first-touch outreach (use reach-out) or customer support threads.
license: MIT
compatibility: Recommended for large models. On small models it can occasionally add an unsupported claim to a draft, so check claims before sending. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Handle reply

Turns a prospect's reply into the right next move: a short, true answer, a dated hold, or silence. The person who wrote back is treated like someone you'll meet again.

## Ground rules

1. **Never send anything.** Drafts only, even with a sending tool connected. Every reply stops the automated sequence to that person, whatever it says.
2. **An opt-out wins.** If a reply asks to stop in any words ("remove me", "take me off", "stop emailing"), that person is suppressed now: no pitch, no question, no "in case you change your mind", no link. At most a one-line confirmation. This holds even when the user asks for a door-opener: write the confirmation, say in one sentence why the rest is left out, and move on. Don't lecture.
3. **Answers come only from sources:** `brand/` facts tagged `confirmed` (or `provisional`, flagged), and the thread itself (what the outreach said, what the prospect said). A price, feature, integration, timeline, certification or policy that isn't there is unknown. The reply says you'll confirm it, and the question goes to the user under **Needs you**. Never multiply a listed price for a case the price list doesn't cover, and never say "yes" or "no" to a certification you can't see. A plausible guess is still an invention.
4. **Referrals are stated exactly as given.** Write to the new person only with what the referrer actually said ("Dana said you run sales ops"). Never "recommended", "suggested we talk" or "introduced". A referral from a prospect is not consent to email the new address: flag the basis (see [references/compliance.md](references/compliance.md)).
5. **An out-of-office is not a referral.** A colleague named "for urgent matters" stays a note in the log. Don't email them as if referred; if the user wants to reach them, it's a fresh cold email with its own consent basis.
6. **Proof follows its permission.** `named: yes` may be named; `named: no` is used without identifying details; `unconfirmed` stays out. Brand rules and restricted claims apply to replies too.
7. **Never overwrite the user's files.** Add rows to the suppression list and status log; never delete, reorder or rewrite existing rows. Never remove anyone from suppression.
8. **Check the suppression list before drafting to anyone,** including a referred person. If they're on it, draft nothing and say why.

## Modes

- **Draft** (default): classify every reply, write the drafts, the log and the suppression rows, check, and report.
- **Guided** (the user asks to review first, "walk me through", "before you draft"): classify every reply and show the triage with the proposed action and the facts each answer would use, flag anything blocked, ask at most three questions, and stop. Write no reply drafts yet. Opt-outs are still added to the suppression list straight away, because honouring them can't wait for approval.

## Workflow

```
- [ ] 1. Load: replies, the original outreach (drafts and FACTS ledger), brand/, suppression list, status log
- [ ] 2. Classify each reply (references/classes.md)
- [ ] 3. Decide the action, follow-up date and facts per reply
- [ ] 4. Draft, and write outreach/replies-<date>.txt
- [ ] 5. Update outreach/suppression.csv and outreach/reply-log.csv
- [ ] 6. Check: script, then judgment checks
- [ ] 7. Reply in the fixed shape
```

### 1. Load

Find the replies: pasted in the conversation, or a file the user names. Find the thread: the outreach drafts file for that prospect or list (`outreach/drafts-*.txt`, with a `FACTS` ledger at the top), any contacts CSV beside it, or the original email the user pastes. The ledger tells you what was already said and where each address came from.

Read `brand/` (the brand-memory format): `offer.md`, `proof.md`, `claims.md`, `rules.md`, `voice.md` (especially "By channel" → "Email"), `senders.md`, `positioning.md`. Read `outreach/suppression.csv` and `outreach/reply-log.csv` if they exist (formats in [references/files.md](references/files.md)).

**No `brand/`?** Work from the thread and the conversation only, sign with the sender's name from the original email, mark the reply-file `Status: provisional`, and say in the report that these drafts are provisional because there's no brand memory. End the report with an offer, phrased as a question: "Want me to set up brand memory (offer, prices, proof) so the next answers have a source?"

### 2. Classify

Use the classes and precedence in [references/classes.md](references/classes.md). One reply can carry two classes (an opt-out plus a referral, interest plus questions): the higher one decides what you say to that person, and the other still gets handled.

### 3. Decide

For each reply, set the action (`reply`, `hold`, `confirm` or `none`), the next step, and the follow-up date, using the class's row in [references/classes.md](references/classes.md). Use today's date. List the facts the answer may use, each with its source, and every question you can't answer under `NEEDS YOU`.

### 4. Draft

- Answer what they asked, in the order they asked it, and nothing else. No re-pitch of the original email.
- Interested, question and objection replies: at most 90 words, one ask. Not-now acknowledgements: at most 40. Thanks to a referrer: at most 30. Opt-out confirmations: one line, at most 20 words.
- A holding line is specific about *what* you'll confirm, but never commits the sender to a deadline nobody set: "I'll confirm where customer data is stored and come back to you." Never "great question". Put the follow-up date in the log, and in Needs you as "answer by <date> to keep the thread warm", so the user decides. Word it neutrally: it must not presuppose either answer ("how we work alongside your current provider" assumes they keep it).
- Next step: offer the entry offer from `offer.md`, or ask when suits them. Never invent a booking link, meeting length or time slot.
- Subject: `Re:` plus the thread's subject. Replies in a thread sign as the voice asks (often a first name). A first email to a referred person carries the sender's full signature, mailing address and opt-out line from `senders.md`.
- Follow the brand's email voice: word limits, spelling, banned words, exclamation marks.

Write every block, drafted or not, to `outreach/replies-<YYYY-MM-DD>.txt` in the format in [references/files.md](references/files.md). Revising? Overwrite your own file; don't leave a second version beside it.

### 5. Update the lists

Append to `outreach/suppression.csv`: every unsubscribe, every hostile reply, every hard bounce. Append one row per reply to `outreach/reply-log.csv`, plus a row for any referred person you drafted to. Create either file with its header if it doesn't exist.

### 6. Check

```bash
python3 scripts/check_replies.py outreach/replies-<date>.txt --today <YYYY-MM-DD> --brand brand/ --suppression outreach/suppression.csv --log outreach/reply-log.csv --thread outreach/drafts-<name>.txt
```

Fix every FAIL and rerun until it passes: a FAIL means rewrite, not hedge. Then the judgment checks:
1. **Did it answer the question?** Read their reply, then yours. Every question is answered from a source or held, none skipped.
2. **Trace every claim.** Each figure, feature, integration and timeline in the draft is in `FACTS` with a source. Anything else comes out.
3. **Would this annoy someone who said no?** Any opt-out reply that does more than confirm is rewritten.
4. **Read the referral line aloud.** If the referrer would wince at how you quoted them, cut it back to what they said.

### 7. Reply

```
**Recommendation:** <one line: N replies: what to send first, what's on hold, what gets no reply>

**Triage**
| Contact | Class | What happens | Follow-up |

**Drafts** (ready to copy; also in outreach/replies-<date>.txt)
To: … · Subject: …
<body>

**Needs you**: <question, who asked, what the holding reply said you'd confirm> (at most 4 items)

**Updated:** suppression list (+N: who), status log (N rows). <Compliance: one line per flag.>
```

- Lead with the recommendation. Keep everything outside the drafts under about 300 words.
- In Guided mode: the recommendation, the triage with proposed answers in a line each, anything blocked, and the questions.
- Compliance line: for a hostile reply, tell the user plainly about the complaint risk and to keep the dated record of where the address was published. For a referral or out-of-office colleague, say what consent basis needs confirming.
- Talk to the user in the second person. Never mention this skill, the checker or whether it passed, the file format, scratch files, brand-memory file names (`proof.md`, `senders.md`), the limits in this file, or other skills by name; say "your outreach drafts", "the suppression list", "brand memory has no customer proof".
- A holding reply can go now: say so. Don't tell the user to wait for answers before sending it.
- Never write a made-up value anywhere, including the log: an unknown email address is `unknown`, not a look-alike address.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

Every person who wrote back gets the reply a careful founder would send: short, true and on their terms, or nothing at all when that's what they asked for. Nobody who said stop hears from you again. The user can send each draft after a glance, and knows exactly which answers only they can give.

A worked example (Pipewise, three replies: a demo request with a security question, a referral, and an opt-out) is in [assets/examples/pipewise/](assets/examples/pipewise/README.md).
