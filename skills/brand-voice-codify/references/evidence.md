# Evidence: what counts, how much, and what to do when it disagrees

## Contents
- Kinds of evidence
- How a rule earns its status
- What isn't evidence
- Reading the evidence, section by section
- Contradictions
- Thin evidence
- Requests to sound like another company

## Kinds of evidence

| Kind | What it is | What it can support |
|---|---|---|
| **Stated rule** | The user or a named approver says it: "we never say X", "emails are signed with a first name", a note on a rejected draft | Any section. The person's word is the rule |
| **Edit pair** | Before and after, where an approver changed someone's draft | What they removed (Don't, Words we never use) and what they put in (Do, Words we use). One pair is one piece of evidence |
| **Approved sample** | Writing the brand calls its best or on-voice | Principles, Do, Words we use, channel rules, Examples. One sample is one piece |
| **Rejected sample** | Writing the brand disliked | Don't only, as a provisional pattern. A general note ("too loud", "this isn't us") doesn't say which words or habits they meant, so rules from it stay provisional unless they name the word |

Note who approved or edited each piece and the date, if the file says. That goes in the source tag.

## How a rule earns its status

Every rule bullet ends in `[source: <where>, <YYYY-MM-DD> · confirmed | provisional]`. `<where>` names the evidence exactly: the file name, "edit pairs 1 and 3 (Tomas Reyes)", "feedback, Priya Nand", "user". The date is the day you recorded it, unless the evidence carries its own date.

- **confirmed:** the user or a named approver stated it, or it shows in **three or more** independent pieces of evidence with no counterexample.
- **provisional:** one or two pieces of evidence; anything taken only from a rejected sample; a direction the user wants but no sample shows yet.
- **Never `assumed`.** A voice rule nobody showed or said is not a rule. Write `TBD: <what evidence would settle it>` instead.

Count pieces, not mentions: three sentences in one email are one piece. Two edit pairs that make the same change are two pieces.

## What isn't evidence

Set these aside and say so in the reply under **Not used**:
- **Words inside a sample that the brand didn't write:** a customer's quote, a review, a reply from a prospect. A gushing testimonial with three exclamation marks says nothing about how the brand writes.
- **Facts and promises in the samples:** prices, dates, results, "by the 5th". Those belong in offer, proof and claims, not in voice. Never turn a fact into a voice rule or an example.
- **Lines that break an existing rule in `brand/rules.md` or a claim in `brand/claims.md`** (for example a sample promising "real-time" when a rule says never to). Don't use them as examples or words we use; flag the conflict.
- **Another company's copy or style guide,** and your own taste. Generic "good writing" advice (avoid jargon, use active voice) is not a brand rule unless their evidence shows it.

## Reading the evidence, section by section

Run the stats first (sentence length, contractions, exclamation and question marks, hashtags, I/we/you, spelling markers), per file. Then read for what numbers can't show.

- **Principles (3 to 5):** the patterns that hold across most pieces. One line each, in plain words, with the evidence count behind it. Include the spelling convention here.
- **Spelling:** state it only if the samples contain words that show it. The brand's evidence decides, never your own or the user's personal style. `-our`/`-re` with `-ize` is Canadian; `-our`/`-re` with `-ise` is UK; `-or`/`-er` is US. `-our` with no `-ize` or `-ise` word can't tell UK from Canadian: say that, unless the user says which. No marker words at all: `TBD: spelling convention (the samples have no words that show it)`.
- **Do and Don't:** habits, not single words. "Questions as the call to action ("Worth a 15-minute look?")", "No 'we are excited to' openers".
- **Words we use:** terms the brand uses consistently, including product names with their casing.
- **Words we never use:** words an approver removed or banned. Plain words only. The reason goes in Don't.
- **By channel:** one `### <Channel>` per channel the evidence covers. Length, person (I or we), sign-off, exclamation marks, hashtags. Write limits so another skill can read them: "Under 120 words", "No exclamation marks", "At most one exclamation mark", "No hashtags", "At most two hashtags".
- **Examples:** at most three per channel, quoted word for word from approved samples (never from a rejected one, never rewritten).

## Contradictions

A contradiction is two pieces of evidence pointing opposite ways on the same thing: exclamation marks, contractions, spelling, person, length, a word used in one and banned in another. Also new evidence against an existing confirmed rule, and a stated rule against the samples the user supplied.

Never pick a side silently. For each one:
1. In `voice.md`, write the open point as a TBD line in the right section, worded so it states no limit: `- TBD: ruling needed on exclamation marks on the website (the two approved pages disagree)`. Not "no exclamation marks vs five": another skill would read that as a rule.
2. In the reply, under **Rulings needed**, quote both sides with their sources and counts, and ask one question with the options ("keep none, allow one per page, or allow them on launch pages only?").
3. Keep everything else moving. One contradiction doesn't stop the rest of the file.

Special cases:
- **Existing confirmed rule vs new evidence:** keep the rule exactly as it is. Flag the new evidence as a possible change. A single edit doesn't overturn a confirmed rule. If an edit swaps out the very word or habit a confirmed rule asks for ("your bookkeeper" changed to "our team"), it's a ruling even if you think both fit the rule: the approver may have meant something, so ask.
- **The user states a rule their own samples break:** record the rule (they said it, so it's confirmed), and say plainly which samples break it, with a count or a quote. Ask whether to edit those samples, scope the rule to some channels, or drop it. Don't use the breaking lines as examples until they rule.
- **A banned word inside a name they use** ("never say seamless" when the product is Seamless Sync): don't add the bare word to the never-use list, where it would flag the product name everywhere. Ask, or write it in Don't with the exception spelled out.

## Thin evidence

Thin means one or two samples, under about 300 words in total, or one channel only. Then:
- Write only what the evidence shows, all provisional. Leave everything else as specific `TBD:` lines.
- Add no channel the evidence doesn't cover. A request to cover "emails, website, ads" from one LinkedIn post gets `TBD` for those channels, not guesses.
- Say in the first line of the reply that the guide is thin and provisional, and ask for the next evidence by name: three to five pieces they're proud of across their main channels, two or three drafts an approver edited, words they never use, and one piece they disliked with what they disliked about it.

## Requests to sound like another company

"Make us sound exactly like Apple" is a direction, not evidence. Rules have to come from the brand's own writing, and another company's slogans and lines aren't theirs to reuse.
- Don't write the other company's name, slogans, taglines or lines into `voice.md`, and don't quote or attribute specific lines or rules to them from memory.
- Describe in a sentence or two the qualities the user seems to want (plainer, warmer, more humour, shorter), as questions.
- Offer the route that works: they write or pick two or three of their own pieces in that direction, or an approver edits a draft toward it, and you codify that. If they want, record the direction itself in their words as a provisional principle tagged `user`.
- Leave existing confirmed rules alone.
