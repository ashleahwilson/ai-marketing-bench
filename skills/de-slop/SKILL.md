---
name: de-slop
description: Removes what makes writing read as AI-generated, from empty claims and borrowed rhetorical moves down to stock words, without inventing a single detail, and catches the overcorrections (fragments, one-line paragraph stacks, performed candour) that heavy-handed clean-ups produce. Returns the cleaned text, or a scored audit of the AI tells. Use when the user wants text to sound human or less generic, for example "de-slop this", "make this sound less AI", "humanize this", "does this read like ChatGPT", "score this for AI tells", "clean up this draft". Works on emails, posts, web copy, proposals and documents, and keeps each one in its register. Not for applying a specific brand's voice (use brand-voice-gate, which runs this pass and then the brand's own rules) or for writing from nothing.
license: MIT
compatibility: Recommended for large models. On small models it can still add or widen a claim occasionally, so check the revision against the draft. See evals/scorecard.json.
metadata:
  version: "1.1.1"
  author: "Ashleah Wilson"
---

# De-slop

Makes text read as written by a person, by fixing what it claims before how it's worded. Swapping words in a paragraph that says nothing produces well-dressed emptiness.

This is the first half of brand-voice-gate, on its own. If the project has a `brand/` folder and the user wants the text to sound like their brand, say brand-voice-gate does both passes.

## Ground rules

1. **Add no facts.** Every name, number, claim and benefit in the output must be in the draft. A detail that makes copy feel grounded is still an invention if the user didn't supply it. That includes stories, feelings and anecdotes ("I almost quit" doesn't get a date or a reason).
2. **Never edit a quotation.** A customer's words stay exactly as written, even when they're full of stock phrases. Clean the copy around them.
3. **Don't fix what works.** Specific, plain text comes back unchanged, with one line saying so. Changing a sentence needs a reason you could name.
4. **Keep the writer's conventions.** Their spelling (US, UK, Canadian), their formatting, their person. Don't impose a house style.
5. **Never overwrite the original.** Deliver the revision in the reply, or in `<name>-clean.md` beside the draft.

## Pick the mode

| The user wants… | Mode |
|---|---|
| Cleaner text: "de-slop", "humanize", "make it sound less AI" (the default) | **Fix:** the revision, then a short note only if something needs their attention |
| A verdict: "score this", "audit this", "flag the AI tells", "don't rewrite" | **Score:** the report below, no rewrite |
| New text that mustn't read as generated | **Write:** apply every rule while drafting, from facts the user gave |

## Workflow

```
- [ ] 1. Register: what is this (email, post, web, proposal, document)?
- [ ] 2. Specificity gate: is anything checkable being said?
- [ ] 3. Layers 1–5, deepest first, then the overcorrection guard
- [ ] 4. Trace and check (Fix and Write modes)
- [ ] 5. Reply
```

**1–3.** Follow [references/subtractive.md](references/subtractive.md): pick the register, run the specificity gate, then the five layers and the overcorrection guard. If the gate fails (under two named things, numbers or consequences per 100 words), say so in one sentence, then either return a much shorter version built only from what's there or ask for the specific facts you'd need.

**4. Trace and check.** Save the revision as `<name>-clean.md` (for pasted text, save the draft as `.deslop/draft.md` and the revision as `.deslop/draft-clean.md`). Write `<name>-trace.md`: a `TRACE` block quoting each sentence of the revision with the words from the draft that support it (or `no claim`), and a `CHANGES` block quoting the original words of each change. The format is at the top of `scripts/check_trace.py`. Then run:

```bash
python3 scripts/check_trace.py <name>-clean.md --trace <name>-trace.md --original <draft>
python3 scripts/check_voice.py <name>-clean.md --original <draft>
```

Fix every FAIL by changing the revision, never by loosening the trace. If the draft supports the sentence somewhere you didn't quote, add that quote. Otherwise cut it or narrow it to the draft's own words: a flagged term means you swapped in a word the cited text doesn't use. Ignore the checker's note that there's no brand memory: this skill doesn't use one.

**5. Reply.**

**Fix mode.** The revised text first, in the draft's own format. Then, only if needed, one short block (60 words at most):
- **Check:** claims in the draft that look unsupported (a statistic, "trusted by 500+"), kept or cut as you judged, and facts you'd need to strengthen it.

No preamble, no list of every change, no offer to adjust the tone. If the draft was already clean, say so in one line and return it.

**Score mode:**

```
AI-tell rating: Low | Moderate | High | Severe
Specificity: <named things, numbers, consequences per 100 words>

Claims: <flagged lines, or "clean">
Moves: <flagged lines, each with the pattern named>
Shape: <flagged lines>
Sentences: <flagged lines>
Words: <clusters only, not single instances>
Overcorrection: <flagged lines, or "none">

Biggest problem: <one sentence>
```

Quote each offending line and name its pattern. Skip explaining why the pattern is bad.

Never mention the checkers, their output or the trace file in the reply.

## When asked for something this skill won't do

**"Add a story", "add some stats", "make it relatable" with no material:** say in one sentence that you'd need the real thing, and ask the two or three questions that would get it (which client, what changed, was it measured). Still return the cleaned version. A clearly marked hypothetical ("say a three-chair clinic") is fine if the user wants one. No lecture.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The writer reads the revision and recognises their own point, said plainly, with nothing added they'd have to defend. A clean draft comes back unchanged in two lines. Nothing in it would make a reader think "a machine wrote this", including the tells of a machine trying not to sound like one.

A worked example is in [assets/examples/quote-email/](assets/examples/quote-email/README.md).
