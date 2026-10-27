# Changelog

## 1.5.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.5.0 (2026-10-11)
Closing the Haiku gap: rounds 7–8 still had small widened facts where a noun was swapped ("prime cost" on a dashboard confirmed for food cost).
- `check_trace.py` fails a sentence that uses a fact term from the draft or brand memory that its own evidence doesn't contain. Tested on the 30 round 7–9 traces: it caught every swapped-noun widening the graders found, and its other flags on clean runs were fixable by citing the missing line.
- A customer's quote in proof.md can support only a sentence that quotes or names that customer, so one customer's words can't become a promise to every reader.
- The skill says how to fix each kind of FAIL: cite the missing confirmed line, or use the evidence's own term, or cut.

## 1.4.0 (2026-10-11)
The fact-list fix. Rounds 1–6 showed Haiku still added or widened facts in some runs, and misdescribed its own changes.
- Every revision now ships with `<name>-trace.md`: each sentence quoted with the exact words in the draft or confirmed brand memory that support it, plus the changes, each quoting the original.
- New `check_trace.py` fails untraced sentences, evidence not found word for word, evidence from voice.md, rules.md or unconfirmed and held lines, numbers or widening words (every, all, team, clients…) missing from the evidence, and changes that misquote the draft.
- Pasted drafts are saved to `.gate/` so the same checks run.
- The worked example's own "like everyone on our team" widening was caught by the new check and fixed.

## 1.3.0 (2026-10-11)
Rounds 3–4 (56/67, 61/67) repeated a few misses, and one run re-added a held claim because it was written in brand/.
- Only `confirmed` brand facts may be added; claims needing substantiation or held by a rule never are.
- A channel rule that names the writer means rewriting in that person's first person, not asking the user to.
- Checklist: say which plan a wrong price belongs to; name each removed claim as needing a source.
- `<name>-gated.md` holds only the publishable text; the verdict and checks stay in the reply.

## 1.2.0 (2026-10-11)
Round 2 regressed (56/67): one run never looked for brand/ and reported it missing, others skipped the naming-permission check or changed US spelling.
- A required pre-reply checklist (folder listed, prices for this reader, unsupported claims, quotes and permission, nothing widened, spelling, channel rules, accurate "What changed").
- List the project folder before concluding there's no brand memory.
- With no brand memory, the draft's spelling is kept exactly.
- "What changed" lines quote the original words.

## 1.1.0 (2026-10-11)
Fixes from the first blind-graded round:
- No widening facts: one customer's quote isn't "clients", and features don't gain benefits the draft didn't claim.
- With no brand memory, the reply must say so after the verdict and offer to set one up (round 1 missed this on every run).
- A conflict with brand memory is explained, not just corrected (for example which plan a wrong price belongs to).
- A content-free draft is named as such, and a mostly rewritten draft is never "Ready".
- "What changed" lists only changes checkable against the draft, with measured counts; no checker or script names in replies; no third-person narration.

## 1.0.0 (2026-10-11)
- First release:
  - Two passes: subtractive (five layers, from "is anything claimed?" down to word choice, plus an overcorrection guard) and additive (spelling, never-use and preferred words, channel rules, sender, claims and quotes from brand memory).
  - Fix, Check and Guided modes; a fixed reply shape that leads with a verdict (Ready, Ready after fixes, Hold).
  - Rule scope: everywhere, by channel, by skill, by sender.
  - `check_voice.py`: never-use words, rule-forbidden phrases, channel limits, spelling convention, stock phrasing, repeated sentence lengths, quotes not recorded in proof.md, and numbers or names that aren't in the draft or brand memory.
  - Writes `<name>-gated.md` for the next step; never overwrites the original.
- The subtractive pass is adapted from the author's own de-slop skill, rewritten to take its voice from brand memory instead of house defaults.
