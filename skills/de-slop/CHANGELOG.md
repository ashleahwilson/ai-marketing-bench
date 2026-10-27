# Changelog

## 1.1.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.1.0 (2026-10-11)
- Shared `check_trace.py` now fails swapped nouns: a sentence using a term from the draft that its own cited evidence doesn't contain (Haiku turned "helping reduce no-shows" and similar into wider claims in 1.0.0).
- How to fix each FAIL: quote the supporting text, or use the draft's own words, or cut.

## 1.0.0 (2026-10-11)
- First release, as a standalone version of brand-voice-gate's subtractive pass:
  - Fix, Score and Write modes. Fix returns the text with at most a 60-word note.
  - The specificity gate, five layers from claims to words, the overcorrection guard, and register by channel.
  - Every revision ships with a trace; `check_trace.py` fails any sentence not supported word for word by the draft, and any change that misquotes it.
- `references/subtractive.md`, `scripts/check_voice.py` and `scripts/check_trace.py` are copies of brand-voice-gate's; `scripts/sync_shared.py` in the repo keeps them identical.
- Adapted from the author's own de-slop skill.
