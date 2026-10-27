# The voice.md format

`brand/voice.md` follows the brand-memory format. brand-voice-gate and other skills parse it, so the headings and a few phrasings are fixed.

## Shape

```
# Voice

Last reviewed: 2026-10-23

## Principles

- Short sentences, about 10 words on average; contractions throughout [source: best-email.md, best-linkedin.md, home.md, 2026-10-23 · confirmed]
- Canadian spelling (colour, cancelled) [source: best-email.md, home.md, 2026-10-23 · provisional]

## Do

- Use questions as the call to action [source: edit pair 3 (Tomas Reyes), best-email.md, 2026-10-23 · provisional]

## Don't

- Don't promise zero no-shows; say Ferncliff reduces them [source: feedback, Tomas Reyes, 2026-10-20 · confirmed]

## Words we use

- clinic, wait list, front desk [source: feedback, Priya Nand; home.md; best-email.md, 2026-10-23 · confirmed]

## Words we never use

- practice [source: feedback, Priya Nand, 2026-10-20 · confirmed]
- utilize [source: edit pair 1 (Tomas Reyes), 2026-10-23 · provisional]

## By channel

### Email
- Signed with a first name [source: feedback, Priya Nand, 2026-10-20 · confirmed]
- TBD: length limit (two samples, 60 and 110 words; not enough to set one)

### LinkedIn
- First person, by a founder. No hashtags [source: best-linkedin.md, 2026-10-23 · provisional]

## Examples

- Email: "Questions? Reply to this email. It comes to me." [source: best-email.md, 2026-10-23 · confirmed]
```

## Fixed rules

- **All seven `##` sections, always,** in this order. A section with no evidence gets one `- TBD: <what evidence would fill it>` line, never a template default.
- **One bullet per rule,** ending in its source tag. Several sources go in one tag, separated by commas or semicolons. Status is `confirmed` or `provisional`.
- **Spelling:** name exactly one convention, in the words "US spelling", "UK spelling" or "Canadian spelling", once in the file. Other skills read the first match, so don't mention a second convention anywhere, not even in a TBD line or an example. If it's unknown: `- TBD: spelling convention (the samples have no words that show it)`.
- **Words we never use:** each bullet is a plain comma-separated list of words or short phrases, then the tag. No reasons, quotes or parentheses in the list (another skill splits it on commas). Reasons go in Don't. Never list a word that's part of a name on the use list.
- **By channel:** only `### <Channel>` subsections (`### Email`, `### LinkedIn`, `### Website`, `### Ad`, `### Proposal`, or the brand's own channel names). Write limits as: "Under 120 words", "No exclamation marks", "At most one exclamation mark", "No hashtags", "At most two hashtags". A TBD line in a channel never contains those phrases.
- **Examples:** quoted word for word from an approved sample, prefixed with the channel, at most three per channel. Pick lines that show how the brand sounds, not lines that carry a price, number or feature claim.
- **Last reviewed:** today's date when you change the file.

## Updating an existing voice.md

- Keep every confirmed rule exactly as it is, tag included: don't add a source to it, reword it, move it to TBD or delete it. New evidence that supports it needs no change; new evidence that conflicts becomes a ruling.
- A provisional rule that new evidence supports can become confirmed (three pieces or a stated rule). Add the new source to its tag.
- A provisional rule that new evidence contradicts becomes a ruling, not a silent deletion.
- Add missing sections with TBD lines. Fix format problems (a `####` channel heading, a never-use entry with a reason in it) without changing what the rule says.
- Untagged rules you inherit: don't invent a source. Tag them `[source: voice.md before <today>, origin not recorded, <today> · provisional]` and ask who set them.

## changelog.md

`brand/changelog.md`, one line per change, newest first, under any existing header. Keep the existing lines.

```
2026-10-23 | voice.md | added Website channel (2 rules, provisional); exclamation marks left open | from home.md and launch-page.md
2026-10-23 | voice.md | "clients" added to Words we never use | Maya, team meeting 2026-10-23
```

If `brand/changelog.md` doesn't exist, create it with a `# Changelog` title first.

## Check mode report

When asked only to check a voice.md, report problems in this order: anything another skill would misread (missing or misnamed sections, two spelling conventions, never-use entries with reasons in them, channel headings at the wrong level, vague limits), template leftovers, untagged or unsourced rules, rules the evidence doesn't support, then gaps. Change nothing unless asked.
