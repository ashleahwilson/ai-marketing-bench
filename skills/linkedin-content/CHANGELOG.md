# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Round 2 (Haiku 68/71): Haiku still ran a needs-input and a guided reply over 200 words, skipped the brand-memory offer with no brand/, flagged the user's `.example` links as placeholders, and said "Ready to post" with checks still open.
- `check_post.py --reply` measures short replies; over 200 words means cut.
- The no-brand line now carries the brand-memory offer in the reply shape.
- User- and brand-supplied links count as real, including test domains.
- "Ready to post" only when nothing is left to check; brand-voice-gate named only when the user asks for a check.
- Questions ask about what really happened, never about a made-up premise.

## 1.1.0 (2026-10-23)
Round 1 (Haiku 66/71, Opus 70/71): Haiku ended series posts on closing questions, dropped a launch date that had passed, and ran a "needs your input" reply to 260 words; both models explained the declined bait twice.
- Closing questions only when the user asks for discussion; at most one per series.
- Past dates stay in, in the past tense.
- "Needs your input first" says what brand memory has on the subject and stays under 200 words, counted.
- Declined requests are explained once, in "Left out".

## 1.0.0 (2026-10-23)
- First release:
  - Single posts, 2–5 post series and carousel outlines for a named person or a company page, from the user's own material.
  - Draft and Guided modes; a fixed reply led by a recommendation (Ready to post, Ready once you…, Needs your input first), with two alternative openings per post and a first comment when the link isn't in the body.
  - Fact list with held, unsure, needs-permission and missing facts; no invented stories, clients, numbers or quotes; naming permission from `proof.md`.
  - `check_post.py`: LinkedIn length against the brand rule, hashtags, exclamation marks, engagement bait, broetry, population openers, never-use words and banned phrases, untraced numbers, uncleared names, placeholders, and warnings for performed candour, stock phrasing, links and person.
  - Writes text-only post files under `linkedin/` for brand-voice-gate.
