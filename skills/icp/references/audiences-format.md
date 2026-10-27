# The audiences file (brand/audiences.md)

`brand/audiences.md` is the brand memory's audience file. Every other skill reads it for who to write to, so it keeps the brand memory format: one fact per bullet, each ending in a source tag, unknowns as `TBD: <what's missing>`.

## Contents
- Before you edit
- The layout
- Source tags for ICP facts
- Personas
- History and the changelog
- No brand memory

## Before you edit

Copy the current file to `icp/history/audiences-<YYYY-MM-DD>.md` first. Then edit `brand/audiences.md` in place. Keep every section and bullet the user wrote that the evidence doesn't contradict. A contradicted bullet moves to `## History` with the date and the reason, it isn't deleted.

## The layout

```
# Audiences

Last reviewed: <YYYY-MM-DD>
Evidence base: <records and notes, with counts> (or: no customer data; hypothesis from brand memory)

## Segments
- <segment: industry, size, region>: <why, with counts> [source: <file>, <date> · confirmed | provisional]

## Triggers and signals
- <what makes now the time>: <how many notes or records show it> [source: …]

## Not for
- <disqualifier>: <reason> [source: …]

## Personas
### <Role> (<segment>)
- Measured on: … [source: …]
- Pains: … [source: …]
- Triggers: … [source: …]
- Objections: … [source: …]
- Their words: "<verbatim>" [source: <notes file>, <person>, <date> · confirmed]

## History
- <date>: <superseded bullet> (replaced because <reason, with counts>)
```

Order segments by priority, top tier first. Write each one so a salesperson can recognize it: "Dental groups with 5–19 locations", not "Segment A".

## Source tags for ICP facts

| The fact comes from | Tag |
|---|---|
| The customer data, 10+ closed records behind it | `[source: data/customers.csv, 2026-10-23 · confirmed]` |
| The customer data, under 10 records behind it | `[source: data/customers.csv, 2026-10-23 · provisional]` and the bullet says "hypothesis" |
| Win/loss or call notes | `[source: data/call-notes.md, Dana Whitford, 2026-07-22 · confirmed]` for what was said; `provisional` for a pattern drawn from 1–2 notes |
| The user's decision | `[source: user, 2026-10-23 · confirmed]` |
| Brand memory only, no data | `[source: brand/offer.md, 2026-10-23 · provisional]`, or `assumed` for a working guess |

Every number in a bullet carries its count: "10 of 12 won", "median deal $14,550 (n=10)". Percentages only where the denominator is 10 or more.

## Personas

One persona per buying role the evidence shows. For each field, write what a source says, tagged; anything no source says is `TBD: <what would tell us>`.

- **Their words** are copied character for character from a call note, win/loss note, review, reply or `brand/proof.md`. Never tidy, merge or paraphrase inside quote marks. A role with no recorded words gets `Their words: TBD: no conversations with a <role> on record`.
- A role the user asks for but no source covers is still written, every field `TBD` or tagged `assumed`, with a line saying how to get the evidence (for example "interview the CFO at a won group").
- No invented names, ages, backstories or "day in the life". A persona is a summary of evidence, not a character.

## History and the changelog

Add one line to `brand/changelog.md` (newest first): `- <date>: audiences.md rebuilt from <n> closed records (<file>); ICP scoring v<N> written to icp/scoring.md`. Don't edit any other brand file.

## No brand memory

If there's no `brand/` folder, create only `brand/audiences.md` in this format (don't build the rest of the folder), mark the header `Status: provisional (no other brand memory)`, and offer to set the rest up.
