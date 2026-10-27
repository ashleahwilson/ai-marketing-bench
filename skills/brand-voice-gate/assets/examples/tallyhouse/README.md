# Worked example: a Tallyhouse LinkedIn post

Tallyhouse is a fictional restaurant bookkeeping firm. Its brand memory (the parts the gate reads) is in `brand/`. Dev Patel, a co-founder, drafted `linkedin-post.md`. The gate's output file is `linkedin-post-gated.md`, and `linkedin-post-trace.md` is the trace that shows where every sentence came from.

## The reply

**Verdict:** Ready after fixes

> I was a restaurant controller before I co-founded Tallyhouse.
>
> At Tallyhouse, your sales from Toast, Square or Lightspeed are reconciled every day. All our bookkeepers have worked in hospitality finance. Yours closes the month and sends your P&L, with food cost and labour % on one dashboard.
>
> If you run between one and fifteen locations, the first step is a free month-end review. Send me a message and I'll set it up.
>
> #restaurants #bookkeeping

**What changed:**
- Banned words: "AI-powered" and "seamlessly" are out. The post now leads with the bookkeeper, since the brand's point is the person, not the automation.
- Claims: the 3-day close is removed (see below).
- Voice: written as Dev in the first person, per the LinkedIn rule, using his controller background from brand memory. 85 words.
- Structure: cut the stock opener, the "not just X, we're Y" line, the staged question and three hashtags.

**Check before publishing:** "Close your books in 3 days, not 3 weeks" is held by a brand rule until it's substantiated. Average close time across clients, or one client case study, would clear it.

## Why each change was made

| Draft | Problem | Source |
|---|---|---|
| "AI-powered platform" | On the never-use list, and a rule bans it everywhere | `voice.md`, `rules.md` |
| "seamlessly reconciles" | Never-use word | `voice.md` |
| "Close your books in 3 days, not 3 weeks" | Needs substantiation; a rule holds it | `claims.md`, `rules.md` |
| "In today's fast-paced restaurant landscape" | Stock opener that says nothing (fails the swap test) | general |
| "not just a bookkeeping service — we're a partner" | Borrowed "not X, it's Y" move | general |
| "The result?" | Staged question | general |
| Five hashtags | LinkedIn limit is two | `voice.md`, by channel |
| Third-person "we" | LinkedIn posts are first person from a founder | `voice.md`, by channel |

Every fact in the revision is in the draft or in `brand/`: Dev's controller background and the hospitality-finance bookkeepers are in `proof.md` and `positioning.md`; Toast, Square, Lightspeed, the P&L, food cost and labour %, the 1–15 locations and the free month-end review are in `offer.md` and `audiences.md`.
