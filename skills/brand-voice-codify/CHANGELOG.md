# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Round 2 (Haiku 62/63): Check mode named three of four untagged rules; simple updates opened with "the evidence is thin" as boilerplate; a reply explained how other tools parse the file.
- Check mode quotes every untagged rule one by one.
- Only thin builds open with "thin"; updates open with what changed.
- Replies describe problems in the user's terms, not parser behaviour.

## 1.1.0 (2026-10-23)
Round 1 (Haiku 58/63, Opus 62/63; no skill 35 and 37): Haiku dismissed an edit that swapped "your bookkeeper" for "our team" as compatible, confirmed rules from a rejected draft's general "too loud" note, and re-tagged existing confirmed rules; Opus used a feature fact as an example; replies named other skills and thresholds; a Haiku run weighed the user's own spelling preference against the client's.
- An edit that swaps out what a confirmed rule asks for is always a ruling.
- Rules from a rejected sample stay provisional even with a general rejection note.
- Confirmed rules are left exactly as they were, tag included.
- Examples carry voice, not prices, numbers or feature claims.
- The brand's evidence decides spelling, never the user's own house style.
- Guided mode ends by asking for approval; replies don't name skills or thresholds.
- Eval 1's spelling expectation clarified for every config: "colour" and "cancelled" fit UK as well as Canadian, so asking which counts.

## 1.0.0 (2026-10-23)
- First release:
  - Draft, Guided and Check modes for building, proposing or auditing `brand/voice.md`.
  - Evidence rules: stated rules, edit pairs, approved and rejected samples; confirmed only when stated or shown in three or more pieces; customer quotes, facts, rule-breaking lines and other brands' copy set aside.
  - Contradictions (between samples, against confirmed rules, or a stated rule against the user's own samples) become TBD lines and questions, never silent choices.
  - `voice_check.py`: `check` for the format brand-voice-gate reads (sections, tags, channel subsections and limits, never-use list format, one spelling convention, verbatim examples, confirmed rules kept) and `stats` for sentence length, contractions, punctuation, person and spelling markers per sample.
  - Worked example: a Tallyhouse newsletter channel.
