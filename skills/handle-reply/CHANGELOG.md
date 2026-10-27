# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Fixes from round 2 (Haiku 63/64, Opus 64/64):
- Holding replies no longer commit the sender to a day ("by Tuesday"); the follow-up date goes in the log and in Needs you for the user to decide.
- No brand memory: the report ends with an explicit offer, phrased as a question, to set it up (Haiku only told the user to do it).
- No internals in the report: no brand-memory file names, no limits in brackets. A holding reply is marked as ready to send now.
- Compliance note on in-thread replies: CASL's exemption for responses to an inquiry; CAN-SPAM when a reply is mainly a pitch.

## 1.1.0 (2026-10-23)
Fixes from round 1 (Haiku 63/64, Opus 63/64):
- Never mention the checker or whether it passed, or show scratch files (Haiku reported "checker passed" in two evals).
- Hostile replies: the report tells the user both the complaint risk and to keep the dated record of where the address was published (Haiku left the record-keeping in the file only).
- Holding lines are worded neutrally and never presuppose the answer (Opus wrote "how we work alongside your own accountant").
- No look-alike placeholder values anywhere, including the status log (Opus logged a made-up address); unknown is written as `unknown`.

## 1.0.0 (2026-10-23)
- First release:
  - Classifies replies to prospecting outreach (interested, question, objection, not now, referral, wrong person, out of office, unsubscribe, hostile, bounce) with a fixed precedence, so an opt-out always wins.
  - Drafts short replies that answer only from brand memory and the original thread; anything else gets a holding line and goes to the user under Needs you.
  - Opt-outs: suppressed at once, at most a one-line confirmation, no pitch even when asked for one. Hostile replies: suppressed, no argument, optional factual line on the address source.
  - Referrals: a first email to the new person that states the referral exactly as given, with the cold footer and a consent-basis flag. Out-of-office colleagues are logged, never treated as referrals.
  - Modes: Draft (default) and Guided (triage and questions, no drafts; opt-outs still suppressed straight away).
  - Writes `outreach/replies-<date>.txt`, appends to `outreach/suppression.csv` and `outreach/reply-log.csv` (formats in `references/files.md`).
  - `check_replies.py`: class cross-checks (opt-out, bounce, out-of-office wording), follow-up dates against today and return dates, suppression and log coverage, opt-out confirmations (length, questions, pitch, links), referral wording and footer, word limits by message kind, figures and links traced to FACTS and sources, brand never-use words, banned claims, uncleared proof names, exclamation marks.
