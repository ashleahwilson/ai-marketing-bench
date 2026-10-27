# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-10)
- Templates no longer carry commented placeholder lines, and the checker now also catches placeholders inside comments.
- Proof keeps full attribution in the memory even when permission to name is unconfirmed.
- File creation is consistent: only real files from a website or migration; a full skeleton from an interview.
- Round-2 evals (Haiku): 40/42 with the skill vs 26/42 without.

## 1.1.0 (2026-10-10)
- A company's own performance claims are no longer "confirmed" by its own website. They go into claims.md as provisional, needing substantiation.
- Migrations keep the original source and the original rule scope; facts with no status become provisional and are listed for the user to confirm.
- Future prices: today's price stays live, and the new one is added as "Scheduled".
- Shared briefs carry warnings in the text the recipient reads.
- No template leftovers; no opt-out or voice filled from defaults; no unrequested folder; no checker jargon in reports; offers to remove secrets found in an audit.
- The checker flags template placeholders and a BRAND.md file table that doesn't match the files.
- The worked example is corrected to match.

## 1.0.0 (2026-10-10)
- First release:
  - **Schema:** 12 files, with a source tag on every fact (confirmed / provisional / assumed) and `TBD` for gaps.
  - **Setup:** from a website or documents, by interview, or by migrating an `outreach-profile.md`.
  - **Maintenance:** history-preserving updates, conflict checks, and a feedback-to-rules routing.
  - **Audit and sharing guidance.**
  - **`scripts/check_brand.py`:** flags secrets, staleness, missing sources, placeholders, unconfirmed naming permission and conflicting numbers.
