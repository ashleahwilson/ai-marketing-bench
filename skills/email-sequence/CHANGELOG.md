# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Fixes from round 2 (Haiku 54/55, Opus 55/55):
- Relative-timed emails never hard-code a calendar date; the reason to act now must be true for every recipient (Haiku wrote a fixed month-end date).
- Proof with unconfirmed reuse permission stays out entirely, quote included; no implied customer relationships (Opus reused the Lantern quote unattributed).
- Exits follow the sequence goal, not an earlier setup step (Haiku's trial sequence exited on activation and skipped the upgrade emails).
- Unsubscribe tag only from senders.md, else a marked placeholder; one sequence file, overwritten on revision.

## 1.1.0 (2026-10-23)
Fixes from round 1 (Haiku 52/55, Opus 51/55):
- Guided mode: five questions at most, counted by question marks.
- Invented urgency removed: every email still gets a true reason to act now from the facts.
- Check and fix: keep and fix every email (Opus deleted one), keep the user's working URLs, name each over-length email.
- Bought list: read the brief anyway; the pushback stays under 250 words.
- Facts now explicitly include product features, service details and options offered to the reader (Haiku offered a "less often" option that doesn't exist); unnamed proof drops identifying details.
- Never mention the skill, the checker or which tools are installed.

## 1.0.0 (2026-10-23)
- First release:
  - Writes welcome, onboarding, nurture, trial-to-paid, re-engagement, post-purchase, event follow-up and newsletter sequences: each email with its job, trigger and timing, subject, preview, body, one call to action, and exit or branch rules.
  - Consent first: bought, rented or scraped lists are routed to reach-out with a consent-based alternative; mixed event segments are split by consent.
  - Never invents proof, scarcity or deadlines; brand rules beat the brief.
  - Modes: Draft, Guided (plan and questions, no copy), and Check and fix (writes `<name>-fixed.md`, original untouched).
  - `check_sequence.py`: required fields, subject and preview, one link per email, unsubscribe and mailing address, word limit and exclamation marks from the brand's email voice, never-use words and banned phrases, unnamed proof, scarcity language without a recorded limit, figures and quotes traced to the ledger or brand memory, placeholders, bought-list consent.
  - Writes `email/sequence-<slug>.md` (format in `references/sequence-file.md`) for reviewers and sending tools.
