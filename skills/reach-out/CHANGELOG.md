# Changelog

## 3.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 3.2.0 (2026-10-24)
- Reads the suppression list and reply log written by handle-reply, and the "Not contacting" section of map-contacts' contacts file, before drafting; held contacts are reported with a reason. Uses the contacts file's Role, Persona, Signal and Source fields. Integration change, not re-run against the evals.

## 3.1.0 (2026-10-10)
- Reads brand memory (`brand/`) first, using confirmed facts as fact and flagging provisional ones. Falls back to `outreach-profile.md`. Feedback is filed into `brand/rules.md` when brand memory exists.

## 3.0.0 (2026-10-10)
Rewritten from scratch.
- Signal matrix replaces per-motion playbooks. Covers 12 signals, including reply received, champion moved, re-engagement and referral.
- Fact ledger. Every name and number in the copy traces to a source, and the checker fails unsourced numbers.
- Send gate. Consent rules by recipient country (CASL, CAN-SPAM, PECR, GDPR, Spam Act) plus deliverability defaults. Warns, never blocks.
- Evidence-based defaults. 50–90 words (35–60 for executives), subjects of 1–4 words, an interest-question ask, 3 touches with step 2 sent as an in-thread reply.
- Response shape. "Send this one" first, at most three pre-send checks, and no mention of skill internals.
- Checker. Fact tracing, thread-subject matching, planning notes left in copy, signature-aware word counts, `--summary`.
- Results: 70/77 on Haiku across 12 evals; 21/23 against 16/23 for no skill on the 4 new evals.

## 2.2.0
Lists, rule conflicts, and rules that the user overrides. Superseded.

## 2.0.0
First stack-agnostic rebuild. Superseded.
