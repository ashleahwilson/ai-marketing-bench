---
name: brand-voice-codify
description: Builds or updates a brand's voice guide (brand/voice.md, the brand-memory format) from evidence, such as samples of its best writing, examples it dislikes, before-and-after edits a founder made to drafts, and feedback like "we never say X". Derives principles, do and don't, words used and never used, the spelling convention, channel rules and on-voice examples, with every rule tagged to the sample or feedback it came from. Rules with thin evidence are marked provisional, contradictions between samples are put to the user instead of settled silently, existing confirmed rules are kept, and changes are logged in brand/changelog.md. Use when the user wants to write, codify, document, update or check their brand voice, for example "turn these posts into a voice guide", "Dana's edits show how we write, capture that", "add these voice rules", "is our voice.md usable". Not for checking or rewriting a draft against the voice (use brand-voice-gate) or for setting up the rest of brand memory.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Brand voice codify

Turns evidence of how a brand writes into `brand/voice.md`, the file brand-voice-gate and every writing skill reads. The guide is only as good as its evidence, so every rule says where it came from, thin evidence stays provisional, and disagreements go back to the person who decides.

## Ground rules

1. **Every rule traces to evidence.** Each bullet ends in `[source: <sample, edit pair or feedback>, <date> · confirmed | provisional]`. A rule nobody showed or said doesn't go in, however sensible it sounds. Unknowns are `TBD: <what evidence would settle it>`. Missing stays missing.
2. **Status follows the evidence** ([references/evidence.md](references/evidence.md)). Confirmed: the user or a named approver stated it, or three or more independent pieces show it with no counterexample. Everything else is provisional. Never `assumed`.
3. **Contradictions go to the user.** When samples disagree, or new evidence conflicts with a confirmed rule, or the user's stated rule conflicts with their own samples, don't pick a side. Leave a TBD line and ask, with both sides quoted.
4. **Keep confirmed rules.** Never reword, re-tag or delete an existing confirmed rule: leave the whole line, tag included, exactly as it was. Any new evidence that replaces a word or habit a confirmed rule calls for is a conflict to ask about, even if the two seem compatible to you. Log every change in `brand/changelog.md`.
5. **Only the brand's own writing is evidence.** A customer quote inside a sample, a fact or price in a sample, a line that breaks `brand/rules.md`, another company's copy, your own taste, and your own or the user's personal house style (a spelling preference in your instructions applies to your writing, not to the brand's file) are not. Set them aside and say so.
6. **Never edit the user's samples or evidence files.** Write only `brand/voice.md`, `brand/changelog.md` and a working copy in `.codify/`. In Guided or Check mode, write nothing to `brand/` until asked.
7. **Push back without refusing.** Asked to copy another brand, to cover channels with no evidence, or to "just make it complete", do what the evidence supports, explain in one sentence, and offer the fastest route to the missing evidence. No lecture.

## Pick the mode

| The user wants… | Mode |
|---|---|
| A voice guide written or updated: "turn these into our voice", "add these rules" (the default) | **Draft:** derive, write `voice.md` and the changelog, ask the rulings |
| To approve rules first: "walk me through it", "don't write anything yet" | **Guided:** propose every rule with its source in the reply, list the decisions, write nothing until they approve |
| A check of an existing file: "is our voice.md usable", "just tell me" | **Check:** report what other skills would misread, leftovers, unsourced rules and gaps; change nothing |

## Workflow

```
- [ ] 1. Load: list the folder; read brand/ (voice, rules, claims, BRAND) and every evidence file
- [ ] 2. Sort the evidence: stated rules, edit pairs, approved samples, rejected samples, not evidence
- [ ] 3. Measure: python3 scripts/voice_check.py stats <evidence files>
- [ ] 4. Derive rules, count their evidence, set status; find contradictions
- [ ] 5. Write voice.md and changelog.md (Draft), or the proposal (Guided), or the report (Check)
- [ ] 6. Check: python3 scripts/voice_check.py check brand/voice.md ... ; then the judgment list
- [ ] 7. Reply in the fixed shape
```

### 1. Load

List the project folder first and look for `brand/`, even if the user didn't mention it. Read `brand/voice.md` if it exists (its confirmed rules are fixed), `rules.md` and `claims.md` (lines that break them can't be examples), and `BRAND.md` for the brand name and channels. Read every evidence file the user points to, whole.

**No `brand/` folder?** Create `brand/voice.md` and `brand/changelog.md` only, not the rest of brand memory. Say in the reply that the rest of brand memory (offer, audiences, proof) doesn't exist yet and offer to set it up.

### 2. Sort the evidence

Label each file, and each part of a file, using the table in [references/evidence.md](references/evidence.md): stated rule, edit pair, approved sample, rejected sample. Pull out what isn't evidence: customer quotes, facts and promises, lines that break `rules.md`, other companies' copy. Note who approved or edited each piece, and its date.

### 3. Measure

```bash
python3 scripts/voice_check.py stats <file> <file> ...
```

Per file: sentence length, contractions per 100 words, exclamation and question marks, hashtags, I/we/you, and spelling markers. Run it per file, not only in total, so a disagreement between two samples shows. The numbers are evidence; you still decide what they mean.

### 4. Derive

Work section by section ([references/evidence.md](references/evidence.md), "Reading the evidence"). For each rule, count the independent pieces behind it and check for a counterexample. Then look for contradictions: on exclamation marks, contractions, spelling, person, length, and any word used in one place and banned in another. Check every new never-use word against the words-we-use list: a banned word inside a product name would flag the product everywhere.

**Thin evidence** (one or two samples, under about 300 words, or one channel): write only what shows, all provisional, with specific TBD lines for the rest. Add no channel the evidence doesn't cover.

### 5. Write

**Draft:** write `brand/voice.md` in the format in [references/format.md](references/format.md): all seven sections, one spelling convention named once, gate-readable channel limits ("Under 120 words", "No exclamation marks", "At most one exclamation mark", "No hashtags"), examples quoted word for word from approved samples. Updating an existing file: keep every confirmed rule word for word, add sections it's missing, and follow "Updating an existing voice.md". Add a line per change to `brand/changelog.md`.

**Guided:** put the proposed rules in the reply, grouped by section, each with its source and status. Then the decisions. Write nothing to `brand/`. The reply's last line asks them to approve or change the rules before anything is written.

**Check:** report in the order in [references/format.md](references/format.md), "Check mode report". Don't invent sources for untagged rules; say they need one.

### 6. Check

In Draft mode, run:

```bash
python3 scripts/voice_check.py check brand/voice.md --evidence <evidence files> [--previous <copy of the old voice.md>]
```

Before editing an existing `voice.md`, copy it to `.codify/voice-before.md` in the project folder and pass it as `--previous`. The check fails a missing section, a template leftover, an untagged rule, a channel outside a `###` subsection, a never-use entry with a reason in it, a never-use word inside a word on the use list, two spelling conventions, a TBD line that states a limit, an example not found word for word in the evidence, and a confirmed rule that's gone. **Fix a FAIL in voice.md, never by loosening a tag or dropping a check.**

Then answer each line for yourself. A "no" means fix the file or the reply. Don't put the list in the reply.

```
- [ ] Every rule names the evidence it came from, and I could point to it in that file
- [ ] Nothing in voice.md came from a customer quote, a fact, another company, or my own taste
- [ ] Rules from one or two pieces, or only from a rejected sample, are provisional
- [ ] Every contradiction is a TBD line in voice.md AND a question in the reply; I picked no side
- [ ] Every confirmed rule from before is still there, word for word, tag included
- [ ] Every edit or sample that swaps out something a confirmed rule asks for is a ruling, not a judgment call I made
- [ ] Rules only from a rejected sample are provisional, even if the rejection note says "too loud" or "not us"
- [ ] Examples are voice lines, not facts: no price, number or feature claim in an example
- [ ] Spelling is stated only if the samples show it, and named once
- [ ] No channel section exists without evidence for that channel
- [ ] Thin evidence: the reply says so first and asks for specific evidence. A simple update from stated rules or edits doesn't open with "thin"; it opens with what changed
- [ ] Check mode: every untagged rule is named one by one, quoted
```

### 7. Reply

Lead with the recommendation. Use this shape:

```
**Recommendation:** <one line: what was written or proposed, how solid it is, and what's needed to finish>

**Rulings needed:** numbered; each quotes both sides with their source and asks one question with options. "None" if none.

**What's in voice.md:** a few lines by section: rules added, kept and changed, how many confirmed and provisional, what's still TBD. (Guided: **Proposed rules**, each with its source. Check: **Problems**, in priority order, each quoting the line.)

**Thin or missing evidence:** what would confirm the provisional rules or fill the gaps, named specifically. Omit if nothing.

**Not used:** evidence set aside and why (a customer's quote, a line that breaks a rule, another brand's lines). Omit if nothing.
```

- Talk to the user in the second person. Plain words: "seen in one sample, so provisional", not tag syntax.
- Keep it under about 300 words, unless Guided mode needs the full list of proposed rules.
- Never mention the script, its output, its checks, how other tools parse the file, thresholds ("the 300-word line") or other skills by name. Mention file names only where the user needs to act.

## Hand-off

brand-voice-gate reads `brand/voice.md`: "Words we never use" (split on commas), "By channel" with `### <Channel>` subsections and their limits, and the spelling convention ("US spelling", "UK spelling" or "Canadian spelling"). Every writing skill reads the Principles, Do, Don't and Examples. `brand/changelog.md` records what changed and why. Nothing else is written.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A writer who has never seen the brand can read `voice.md` and write something the founder wouldn't edit, and can see which rules are settled and which are still a hunch. Every rule points to the sample or the sentence of feedback behind it. Where the evidence disagrees, the file says so and the founder has been asked.

A worked example (a Tallyhouse newsletter channel codified from three issues and one founder edit, with one ruling) is in [assets/examples/tallyhouse-newsletter/](assets/examples/tallyhouse-newsletter/README.md).
