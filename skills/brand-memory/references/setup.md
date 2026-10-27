# Setting up brand memory

Pick the richest source available. Sources can be combined: start with the website, then ask about the gaps.

## Contents
- From a website or documents
- From an interview
- Migrating an existing profile
- Finishing setup

## From a website or documents

1. **Read the pages you're given, or fetch them if browsing is available:** home, about, pricing, product or services, case studies or customers, and careers. Careers pages often show who they hire for, and so who they sell to.
2. **Extract facts into the files.** Tag the site's own descriptive facts (prices, locations, team, features, who they serve) `website <page>, <date> · confirmed`. Tag performance and superlative claims ("in 3 days", "saves 10 hours", "the best") `provisional`, and add them to `claims.md` with `needs substantiation`. Tag inferences (for example, the audience from who the copy addresses) `provisional`.
3. **Quotes and logos go into `proof.md`** with `named: unconfirmed` unless the user confirms permission. A testimonial on their own site is usually fine to reuse, but say so rather than assume it.
4. **Record what they don't do.** Exclusions on the site ("we don't serve…") go under `## We don't do` in `offer.md` and as excluded segments in `audiences.md`.
5. **Draft `voice.md` from the copy itself.** Note sentence length, formality, recurring words, and what's absent. Mark it `provisional`: a website shows the voice but doesn't say what the rules are.
6. **Don't fill gaps from general knowledge.** Competitors, results and personas the site doesn't mention stay `TBD`.

## From an interview

Ask once, in a single message, with no more than 8 questions. Skip any the conversation has already answered:

1. What do you sell, and what changes for the customer afterwards? (one or two sentences)
2. Who buys it: industry, size, region, and the job title that signs off?
3. Who should we not sell to?
4. What would a buyer use instead of you, including doing nothing?
5. Your best two or three results: customer, number, and whether we can name them.
6. Three words for how you want to sound, and one phrase you never want used.
7. Who sends outreach? Name, role and mailing address for the signature.
8. Anything we must not claim, for legal, compliance or client reasons?

Create the skeleton straight away, with every file present (marked `skeleton` in `BRAND.md`'s file table) and `TBD` where the answers will go, and mark `BRAND.md` as `Status: provisional`. Fill it in as the answers arrive.

## Migrating an existing profile

For an `outreach-profile.md` from the reach-out skill:

| Profile section | Goes to |
|---|---|
| Sender | `senders.md` |
| What we sell: offer | `offer.md` |
| Buyers, personas | `audiences.md` |
| Language and spelling | `voice.md` under `## Principles` |
| Proof | `proof.md`, keeping the `named:` status and numbers exactly |
| Voice rules | `rules.md` under `### reach-out` (they were written for outreach), plus `voice.md` `## Do` / `## Don't` only if they clearly apply to all writing |
| Signal rules | `rules.md` under `## By skill` → `### reach-out` |
| Cadence | `rules.md` under `### reach-out` |
| Results | `results.md`, unchanged |
| Approved examples | `voice.md` `## Examples` |

Tag migrated facts `source: outreach-profile.md (<the original source it gives, e.g. case study>), <its Last updated date>`, so the original source survives. Keep any status the file gives. If it gives none, tag the fact `provisional` and list in your report the facts the user should confirm. Keep each rule's scope exactly as written: a rule from the outreach profile goes under `### reach-out` unless it clearly applies to all writing. Then compare field by field: every line of the old file must appear somewhere in `brand/`. Don't delete the old file. Add a first line pointing to `brand/` (`> Moved to brand/ on <date>. Edit there.`) so a skill that still reads it finds the pointer.

## Finishing setup

- Write `BRAND.md` last, from the other files.
- Add the first `changelog.md` line.
- Run `scripts/check_brand.py brand/`.
- Tell the user what's complete, what's provisional, and the three gaps that matter most, each as a question.
