---
name: brand-voice-gate
description: Checks a draft before it ships and fixes it in two passes, first removing what makes writing read as AI-generated or generic, then applying the brand's own voice, words, channel rules and approved claims from brand memory, and returns a verdict (ready, ready after fixes, or hold) with the revised text and what to check. Use when the user wants a draft checked, cleaned up, de-slopped, made "sound like us", humanized or approved before it goes out, for example "gate this post", "does this sound like us", "clean up this email before I send it", "make this less generic", "de-slop this", "check this against our voice", "is this on-brand". Works on emails, LinkedIn posts, web pages, ads and proposals. Also use for a check-only review ("don't rewrite, just tell me what's wrong"). Not for writing a first draft from nothing or for setting up brand memory itself.
license: MIT
compatibility: Recommended for large models. On small models it can still add or widen a claim occasionally, so check the revision against the draft. See evals/scorecard.json.
metadata:
  version: "1.5.1"
  author: "Ashleah Wilson"
---

# Brand voice gate

The last check before something goes out. Two passes, in this order:
1. **Subtract:** take out what makes the text read as generated or generic.
2. **Add:** put the brand back in, from its own voice and rules in `brand/`.

The brand decides how the text sounds. The gate decides whether it's true and whether it reads as written by a person. When they seem to conflict, the brand wins on style and the gate wins on facts.

## Ground rules

1. **Add no facts.** The revised text may only use names, numbers and claims that are in the draft or recorded as `confirmed` in `brand/`. A claim listed under "Needs substantiation", or held by a rule, is never added, even though it's written in `brand/`. A plausible detail that makes the copy feel grounded is still an invention. Don't widen a fact either: one customer's quote isn't what "clients" say, and a feature doesn't get a benefit the draft never claimed ("cuts double-booking", "as it comes in"). If the text is empty without specifics, cut it shorter or ask for them.
2. **Claims need a source.** A result, statistic, customer count or promise ("no hidden fees", "trusted by 500+") that isn't in `brand/proof.md`, `claims.md` or `offer.md` is flagged under "Check before publishing". Remove it from the revision, or hold the piece if the copy depends on it. Facts specific to one client or one email (a contact's name, their numbers, a meeting time) come from the author: keep them and don't flag them.
3. **Never edit a quotation.** Customer quotes are reproduced exactly as recorded in `proof.md`. If the draft misquotes one, restore the recorded wording. If the quote isn't recorded, keep it and flag it. Also leave alone anything the user calls approved, trademarked or legal copy.
4. **Don't fix what works.** A specific, on-voice draft gets "Ready" with no changes. Changing a sentence needs a reason you could name. Rewriting for the sake of it is a failure.
5. **Never overwrite the original.** Deliver the revision in the reply, or in a new file beside the draft (`<name>-gated.md`). Replace the original only when the user asks.
6. **Do what was asked.** "Just tell me what's wrong" gets the check without a rewrite. "Add stats" gets real stats or none (see "When the user asks for something the gate won't do").

## Pick the mode

| The user wants… | Mode |
|---|---|
| A cleaned-up or approved version: "gate", "clean up", "fix", "de-slop", "make it sound like us" (the default) | **Fix:** both passes, then the revised text |
| A verdict without changes: "just tell me", "does this pass", "score this", "review" | **Check:** the same passes, reported as flags with no rewrite |
| To decide as you go, or a long piece where fixes change meaning | **Guided:** list the decisions (a claim to cut, a section to restructure), ask, then apply. Offer this when the draft is over 1,000 words |

## Workflow

```
- [ ] 1. Load: the draft, brand/ (voice, rules, claims, proof, offer), the channel
- [ ] 2. Facts: list every name, number and claim in the draft, each marked sourced / author's / unsupported
- [ ] 3. Subtract: the five layers in references/subtractive.md
- [ ] 4. Add: voice, words, channel rules and claims in references/additive.md
- [ ] 5. Check: run scripts/check_voice.py, then the judgment checks below
- [ ] 6. Reply in the fixed shape
```

### 1. Load

List the project folder first and look for `brand/`, even if the user didn't mention it. Never report that brand memory is missing without having listed the folder. Read `brand/voice.md`, `rules.md`, `claims.md`, `proof.md` and `offer.md` (the brand-memory format). Work out the channel (email, LinkedIn, website, ad, proposal) from the request or the draft, and the sender if it's signed.

**No `brand/` folder?** Do the subtractive pass only. Keep the draft's own spelling exactly ("color" stays "color", "colour" stays "colour") and its conventions; don't impose a house style. The reply must say, right after the verdict, that there's no brand memory, so only the general clean-up was applied and the voice is provisional. End by offering to set one up (the brand-memory skill) or to record three voice rules from this draft. Don't skip this, even when the clean-up went well.

### 2. Facts

Before changing anything, list the facts the draft relies on. Mark each one:
- **sourced:** it matches a line in `brand/`.
- **author's:** it's specific to this piece (a client's numbers, a date, a contact).
- **unsupported:** a general claim about the business that `brand/` doesn't back.
- **conflicts:** it contradicts `brand/` (a wrong price, a misquote, a banned claim).

Fix conflicts from `brand/`, and say what brand memory says and why the draft's version is wrong (for example "$299 is the 2–15 location rate; a single location is $349"). Unsupported claims come out of the revision and go in "Check before publishing". Then count named things, numbers and consequences: under two per 100 words, the draft has no content to polish (see [references/subtractive.md](references/subtractive.md), "The specificity gate"). Say so plainly in the reply ("the original makes no claim a reader could check") before offering the shorter version.

### 3. Subtract

Follow [references/subtractive.md](references/subtractive.md): work from the deepest layer (is anything being claimed?) to the shallowest (word choice). Then run its overcorrection guard. Fragments, broetry and performed candour are their own tells.

### 4. Add

**If the channel rule names who writes** (for example "first person, by a founder"), rewrite in that person's first-person voice ("I"), using only details about them from `brand/`. Don't hand that job back to the user.

Follow [references/additive.md](references/additive.md): apply the brand's spelling, words it uses and never uses, channel rules, sender and claim status. Respect each rule's scope. An email rule doesn't apply to a LinkedIn post, and a reach-out rule doesn't apply to the website.

### 5. Check

Save the revision as `<name>-gated.md` beside the draft. If the draft was pasted into the chat, first save it as `.gate/draft.md` in the project folder and the revision as `.gate/draft-gated.md`.

**a. Write the trace.** In `<name>-trace.md`, write a `TRACE` block with one line per sentence, heading and list item of the revision, quoting it and then the exact words that support it, and a `CHANGES` block quoting the original words of each change. The format is at the top of `scripts/check_trace.py`:

```
TRACE
- "All our bookkeepers have worked in hospitality finance." | brand/positioning.md: "bookkeepers who all worked in hospitality finance"
- "Send me a message and I'll set it up." | no claim
CHANGES
- removed: "Close your books in 3 days, not 3 weeks" | held claim
```

Evidence is the draft or a confirmed line in a brand fact file (offer, proof, positioning, audiences, claims, BRAND). `voice.md` and `rules.md` are guidance, never evidence: a voice example such as "You'll know your prime cost before month-end" is not a promise you can make.

**b. Run both checks:**

```bash
python3 scripts/check_trace.py <name>-gated.md --trace <name>-trace.md --original <draft> --brand brand/
python3 scripts/check_voice.py <name>-gated.md --brand brand/ --channel <email|linkedin|website|ad|proposal> --original <draft>
```

`check_trace.py` fails any sentence with no trace, evidence that isn't word for word in its source, evidence from an unconfirmed or held line, and any number or widening word (every, all, team, clients…) the evidence doesn't contain. It also fails a change that misquotes the draft. `check_voice.py` catches never-use words, stock phrases, channel limits, spelling, repeated sentence lengths and misquoted quotes.

**Fix a FAIL by changing the revision, never by loosening the trace.** First check whether the sentence is supported somewhere you didn't cite: if a confirmed line says it, add that quote. Otherwise cut the sentence or narrow it to the words its evidence uses. A flagged term such as "prime cost" means the evidence you cited is about something else ("food cost"): use the evidence's own term. A customer's quote supports only a sentence that quotes or names that customer, never a promise to the reader. Build "What changed" in the reply from the `CHANGES` block. In Check mode, skip the trace and run only `check_voice.py` on the draft.

Then answer every line of this checklist for yourself before replying. Each "no" means fix the revision or add a line to "Check before publishing". Don't put the checklist in the reply.

```
- [ ] I listed the project folder and read brand/ (or confirmed it doesn't exist)
- [ ] Every price and offer matches offer.md for THIS reader; a wrong figure is corrected AND the reply says which plan it belongs to
- [ ] Every claim not confirmed in brand/ (results, counts, "no hidden fees", superlatives, held claims) is out of the revision, and "Check before publishing" names each one and says it needs a source
- [ ] Every quote matches proof.md word for word, and any named customer whose permission is "no" or "unconfirmed" is flagged
- [ ] Nothing in the revision is new or widened: no added benefit, no single quote turned into "clients"
- [ ] Spelling follows voice.md, or the draft's own spelling if there's no brand memory
- [ ] Channel rules applied: length, person (a named founder writes as "I"), exclamation marks, hashtags, sign-off
- [ ] Would the sender say this out loud to one reader without performing?
```

### 6. Reply

Use this shape. Lead with the verdict.

```
**Verdict:** Ready | Ready after fixes | Hold: <the one reason>

<the revised text, in the draft's own format; omitted in Check mode>

**What changed:** up to 5 short lines, grouped (banned words, claims, structure, voice)
**Check before publishing:** unsupported claims, conflicts with brand memory, naming permission, anything assumed. "Nothing" if nothing.
```

- **Ready:** no changes, or trivial ones. Don't pad the reply. If you rewrote most of the text, it's never Ready.
- **Ready after fixes:** the revision can ship as is.
- **Hold:** the piece depends on something that can't ship yet, such as an unsupported number in the headline or a quote without permission. Still give the best revision possible without it.

In **Check** mode, replace the revised text and "What changed" with **Issues**: each one quotes the line, names the problem, and cites the brand-memory line or the general rule it breaks.

Rules for the reply:
- **"What changed" must be checkable against the draft.** Each line quotes the original words it changed. Only list changes you can point to in the original. Count anything you quantify (hashtags, exclamation marks, words) instead of estimating. Call a word banned only if it's on the brand's list; otherwise call it stock phrasing.
- **Cite only what the file says.** Don't say a claim is "in claims.md" unless it is.
- **Talk to the user,** in the second person. No narration such as "The user asked…".
- **No internals.** Never mention the checker, scripts, their results or source tags ("passed check_voice.py", "0 FAIL"). Mention file names only where the user needs to act.

## When the user asks for something the gate won't do

- **"Add some stats" or "make it more impressive" with no results in `brand/`:** say in one sentence that brand memory has no recorded results to cite. Deliver the stronger version from what's real (the team, the method, a recorded quote). Offer the fast route to real proof: ask the best client what changed and whether it was measured. No lecture.
- **"Use this claim anyway":** write it if the user insists, flag it under "Check before publishing", and keep the verdict at Hold if a brand rule bans it.
- **A correction from the user** ("we never say X", "that's our product name"): apply it, and offer to record it in `brand/rules.md` so every skill follows it.

## Hand-off

`<name>-gated.md` contains only the revised text, ready to publish: no verdict, notes or checklist in it. The verdict and checks go in the reply. A content QA or publishing step reads the gated file, and `<name>-trace.md` stays beside it as the record of where every sentence came from. Don't write any other copies (no `-revised.md`).

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The sender reads the revision and recognises their own point, said the way their brand says it, with nothing added they'd have to defend. A clean draft comes back marked Ready in two lines. Every claim in the final text traces to the draft or to `brand/`.

A worked example (a Tallyhouse LinkedIn post, gated) is in [assets/examples/tallyhouse/](assets/examples/tallyhouse/README.md).
