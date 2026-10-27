# Brand memory schema

## Contents
- The folder
- The source tag
- File by file
- Which skills read what

## The folder

```
brand/
  BRAND.md        one-page summary and index (read this first)
  offer.md        what we sell, prices, outcomes, what we don't do
  audiences.md    segments, personas, triggers, objections, their words
  positioning.md  category, alternatives, why us, messaging pillars
  proof.md        results, testimonials, logos, credentials, with permission status
  voice.md        voice rules, vocabulary, banned phrases, register by channel
  claims.md       approved claims and what substantiates them; restricted claims
  competitors.md  named competitors and sourced facts about them
  senders.md      who sends outreach: name, role, signature, mailing address, countries
  rules.md        standing rules from feedback, scoped by where they apply
  results.md      what was tested and what happened
  changelog.md    dated record of changes to this folder
```

Only `BRAND.md` is required. When setting up from a website, documents or a migration, create a file only when there's something real to put in it, and mark the rest `missing` in `BRAND.md`. When setting up from an interview, create the full skeleton so the answers have somewhere to go, and mark those files `skeleton` in `BRAND.md`. The template for every file is in `assets/template/brand/`.

Every file starts with a `# Title` and a `Last reviewed: YYYY-MM-DD` line.

## The source tag

Every fact is one bullet ending in a source tag:

```
- Single location: $349/month [source: website /pricing, 2026-10-10 · confirmed]
```

The tag has three parts:
- **Where it came from:** `user`, `website <page>`, `doc <name>`, `CRM`, `case study <name>`, `interview <date>`, or `inferred from <what>`.
- **When:** the date it was captured or last verified.
- **Status**, one of three:

| Status | Means | Other skills may |
|---|---|---|
| `confirmed` | The user said it, or a source that's authoritative **for that kind of fact**: their own site for prices, locations, team and what they offer; a signed case study or the CRM for a customer result | Use it as fact |
| `provisional` | Inferred from public material or a draft; not yet reviewed by the user | Use it, but flag it for review |
| `assumed` | A gap filled with a working assumption | Never state it as fact; list it as an assumption |

Unknowns are written as `TBD: <what's missing>`, never filled with a guess.

**A company's own claims about its performance are not confirmed by its own website.** "Books closed in 3 days", "40% faster", "the #1 platform" are claims. Record them in `claims.md` as `provisional`, with `needs substantiation: <what would prove it>`, until the user points to evidence (a case study, data, an audit). Prices, addresses, team facts and product features stated on the site can be `confirmed`.

## File by file

**BRAND.md:** one page, under about 300 words. Name, one-line offer, who it's for, positioning statement, three voice words, the strongest proof, and a list of files with their status (complete, partial, missing). Update it whenever another file changes materially.

**offer.md:** a bullet per product or service. For each: what it is, the outcome, price (only if public or user-given), who it's for, and an `effective` date for prices. Keep a short `## Price history` instead of overwriting old prices. End with `## We don't do`.

**audiences.md:** `## Segments` (industry, size, region, why they buy) and `## Personas`. Each persona gets a role, what they're measured on, their pains, the triggers that make them look, their objections, and the words they use. Their words come from real sources (calls, reviews, replies), each tagged.

**positioning.md:** the category, the alternatives the buyer would otherwise use (including doing nothing), what's uniquely true of us against each, and three or four messaging pillars, each linked to proof in `proof.md`.

**proof.md:** one bullet per item:
```
- <Customer or source, size>: <result with a number, or the quote> [source: …] | named: yes / no / unconfirmed | as of: YYYY-MM
```
Record who said it or whose result it is in full (person, role, company), even when `named: unconfirmed` or `no`. The memory needs the attribution. It's skills writing for an audience that leave the name out until permission is confirmed. Results older than about 18 months are stale. Keep them, but mark them `stale` until they're reverified.

**voice.md:**
- `## Principles` (3–5)
- `## Do` and `## Don't`
- `## Words we use` and `## Words we never use`
- `## By channel` (for example email, LinkedIn, web, proposals)
- `## Examples`, with at most 3 approved samples per channel, each dated

**claims.md:** `## Approved claims`, each with what substantiates it. `## Restricted`: claims that need legal or compliance review, or that are banned outright, each with the reason.

**competitors.md:** one section per competitor. Facts only, each tagged with its source and date. Opinions go under `## Our read`, labelled as such.

**senders.md:** per sender: name, role, the signature block, mailing address, the opt-out line, and the countries they send to. **Never credentials.** No API keys, passwords, tokens or login links. Those belong in a password manager, the tool's own connection settings, or environment variables.

**rules.md:** standing rules from feedback, grouped by scope:
- `## Everywhere`
- `## By skill`, then `### <skill>`
- `## By sender`

Each rule is one line with its condition, the date, and who set it.

**results.md:** one line per test: `date | what | variants | result | decision`.

**changelog.md:** one line per change: `date | file | what changed | why`, newest first.

## Which skills read what

| Skill | Reads |
|---|---|
| reach-out | BRAND.md, offer, audiences, proof, voice, senders, rules, results |
| content and copy skills | BRAND.md, offer, audiences, positioning, proof, voice, claims, rules |
| marketing-audit | BRAND.md, offer, audiences, positioning, competitors |
| brand-voice-gate | voice, claims, rules |
| competitor-intel | competitors, positioning, offer |

A skill that finds no `brand/` folder works from the conversation and marks its output provisional. If it finds `outreach-profile.md` instead, it reads that and suggests migrating it (see `setup.md`).
