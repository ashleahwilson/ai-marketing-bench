# The contacts file

`accounts/<company-slug>/contacts.md` is the hand-off to outreach. Whoever drafts the emails reads each contact's name, role, persona, source and signal from it, so every field has one fixed name and every fact has a dated source. If the user's sources already sit in `accounts/<slug>/`, write the file there. Otherwise create the folder, using a lowercase, hyphenated company name (`copperpot-hospitality`).

## Template

```markdown
# Contacts: <Company>

As of: <today, YYYY-MM-DD>
Account: <what the sources say about the company: size, locations, region> [source: <file>, <date>]
Brand memory: brand/ (personas from audiences.md) | none: personas provisional
Fit: in audience | outside audience: <why, from brand memory> | unknown
Sources:
- <file name> | <what it is> | <date saved, exported or held>

## Contact order
1. <Name>: <role>. <why first, in one line>. <when, e.g. day 0>
2. <Name>: <role>. <why, and what to wait for>. <when>

## Contacts

### <Full name, exactly as in the source>
- Title: <current title> [source: <file>, <date>]
- Role: <one or two of: economic buyer, champion, user, technical evaluator, blocker, influencer, unknown>
- Confidence: high | medium | low (<what it rests on: call notes, CRM activity, title only>)
- Persona: <persona name> (brand/audiences.md) | provisional: <label> | none
- Status: current | left | stale | unconfirmed
- Evidence: <quote or fact> [source: <file>, <date>]
- Signal: <the checkable reason to write to them now> [source: <file>, <date>] | none
- Channel: <work email> (on file) [source: <file>, <date>] | <guess> (unverified guess from pattern <pattern>) | LinkedIn | none on file
- Source: <file>, <date>; <file>, <date>

## Not contacting
### <Name>
(same fields; Status left or stale; say why and what to do instead)

## Gaps
- <Role>: nobody known. Look for: <titles>. Where: <how to find them>.

## Check before outreach
- <at most five items: stale data, records to update, fit questions, unverified addresses>
```

## Field rules

- **Name:** spelled as in the source. If two sources disagree on spelling, use the newer and note the other.
- **Title:** the newest dated source wins. When an older source disagrees, say so in the Evidence line ("CRM shows Sales Ops Analyst, last updated 2025-11").
- **Role:** only the seven values above. "Unknown" is a real answer. In Guided mode an unsettled role is the likely value plus `(proposed)`, for example `economic buyer (proposed)`. A person can hold two roles (for example champion and technical evaluator).
- **Confidence:** high only when a call, an email, CRM activity or an org chart says it. A title alone is at most medium.
- **Persona:** the name of a persona in `brand/audiences.md`. With no brand memory, or no persona that fits, write `provisional: <plain label>` and never borrow a persona name the brand doesn't have.
- **Status:** `left` when a source says they've gone (a LinkedIn export with a new employer, a bounce, a call note). `stale` when the newest source about them is over 12 months old. `unconfirmed` when only one old or indirect source mentions them.
- **Signal:** the one fact an outreach writer could use: an event attended, a trial started, a reply, a question they asked, a hiring post they own. Write `none` rather than stretching a title into a signal.
- **Channel:** a work address or number only if a source has it, with that source. A guessed address only when the user asked for guesses, and then on one line with `unverified guess` and the pattern. Never a personal address or mobile number, even when a source contains one.
- **Source:** every file the contact's facts came from, each with its date. A file with no date gets the date the user gave, or `undated` in Check before outreach.

People who left, or who aren't at this company at all, go under **Not contacting** (left) or are left out entirely (a different company), with one line in the reply saying who was excluded and why. Never put them in the contact order.
