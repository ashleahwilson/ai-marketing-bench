# The additive pass

The subtractive pass makes text read as written by a person. This pass makes it read as written by *this brand*. Everything here comes from `brand/`; nothing comes from this file's taste.

## Contents

- What to read, and in what order
- Scope: which rules apply to this draft
- Applying the voice
- Claims and proof
- When brand memory is thin or missing

## What to read, and in what order

| File | What it gives the gate |
|---|---|
| `voice.md` | Principles, spelling convention, do and don't, words we use, words we never use, rules by channel, examples |
| `rules.md` | Hard rules: everywhere, by skill, by sender |
| `claims.md` | Which claims are approved, which need substantiation, which are restricted |
| `proof.md` | Recorded quotes, results and their naming permission |
| `offer.md` | Prices, what's included, what's not offered |
| `senders.md` | Who can sign, and how they sign |

**Precedence when they disagree:** the user's request in this conversation, then `rules.md`, then `voice.md`, then this skill's general tells. One exception: no instruction makes the gate add a fact that isn't sourced.

**Source tags.** Treat lines tagged `confirmed` as rules. Apply `provisional` ones, but mention any that changed the text under "Check before publishing". Ignore `assumed` ones for anything a reader would see.

## Scope: which rules apply to this draft

Every rule has a scope. Apply it only inside that scope.
- `## Everywhere` in `rules.md`: always.
- `## By channel` in `voice.md`: only the section matching this draft's channel. An "Email: no exclamation marks" rule says nothing about a LinkedIn post.
- `## By skill`: only when the draft came from that skill's kind of work (a `reach-out` rule applies to prospecting messages, not to the website).
- `## By sender`: only when that person signs the piece.

When the channel is unclear, infer it from the draft (a subject line means email; hashtags mean social). Ask only if two channels' rules would give different results.

## Applying the voice

1. **Spelling.** Use the convention `voice.md` states (US, UK, Canadian, or another). If it states none, keep the draft's own spelling. Never impose one from outside `brand/`.
2. **Words we never use.** Remove every occurrence, including inflections ("seamless", "seamlessly"). Rewrite the thought rather than swapping in a synonym.
3. **Words we use.** Prefer the brand's own terms where they fit naturally ("your bookkeeper" rather than "the platform"). Don't force them in.
4. **Do and don't.** These often carry positioning ("the human bookkeeper is the point"). Check the draft's framing against them, not just its words.
5. **Channel rules.** Length, person (I/we/you), exclamation marks, hashtags, sign-off.
6. **Sender.** If the channel rule names who writes (for example a founder in the first person), write as that person, using only details about them from `brand/`.
7. **Examples.** If `voice.md` has on-voice examples, match their rhythm and register, not their words.

## Claims and proof

- **Approved claims** can stay as written.
- **Needs substantiation** or banned by a rule: remove from the revision and list under "Check before publishing", naming what proof would clear it (the file usually says).
- **Not in `brand/` at all:** treat as unsupported. Results, counts, percentages, guarantees ("no hidden fees"), superlatives ("the fastest").
- **Prices and offers** must match `offer.md`. A price that matches a different plan is a conflict: correct it and say why.
- **Quotes** must match `proof.md` word for word. Restore the recorded wording if the draft drifts. If `proof.md` marks naming permission as `no` or `unconfirmed`, flag it, and remove the name if the piece is going out now.

## When brand memory is thin or missing

- **No `brand/` folder:** subtractive pass only, keeping the draft's spelling and conventions. Say the voice is provisional and offer to set up brand memory.
- **`voice.md` mostly TBD:** apply what's there, infer nothing beyond it, and name the two or three voice decisions that would most improve the next draft (for example "spelling convention", "words you never use").
- **A user correction mid-task:** apply it, and offer to add it to `rules.md` with its scope and a source tag, so every skill follows it next time.
