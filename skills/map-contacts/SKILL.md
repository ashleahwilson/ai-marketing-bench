---
name: map-contacts
description: Maps the buying committee at one target account from information the user supplies, such as a saved team page, an org chart, CRM contacts, a LinkedIn export, call notes or job postings. Assigns each person a role (economic buyer, champion, user, technical evaluator, blocker, influencer) with the evidence and its date, matches them to brand-memory personas, recommends who to contact first and in what order, names the roles nobody known fills, and flags stale data such as someone who has left or a title older than its source. Writes a contacts file per account for outreach drafting. Use when the user asks who to contact at an account, wants a buying committee or stakeholder map, asks "who signs off at X", "who else should we talk to", "re-map this account", or wants contacts organized before outreach. Never invents people or contact details, never sources personal emails or mobile numbers, and labels any guessed work email unverified. Not for writing the outreach itself or for building a list of accounts.
license: MIT
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Map contacts

Turns what the user already has about one account into a buying committee they can act on: who matters, what role each person plays, who to write to first, and what's missing. Every person and every claim about them comes from a dated source the user supplied.

## Ground rules

1. **Missing stays missing.** Name only people who appear in a source. Never add a likely CFO, a LinkedIn URL, a tenure, a priority or an email that no source contains. A plausible guess is still an invention. No sources at all means no names: say what to supply.
2. **Every role carries its evidence.** A quote or fact, the file it came from, and its date. A title alone is a hint, never proof, and never grounds for calling someone a blocker.
3. **No personal contact data.** Never find, guess or pass on a personal email or mobile number, even when asked or when a source holds one. Decline in one or two sentences, and one of them names the consent risk: texting or emailing someone at a personal address without their agreement breaks anti-spam and texting consent rules. Then offer work channels (see [references/contact-data.md](references/contact-data.md)). No lecture.
4. **Guessed work emails only on request.** Don't offer a pattern or a guess the user didn't ask for. When asked, label each one `unverified guess` with the pattern evidence, in the reply and the file.
5. **Newest dated source wins.** Someone a newer source puts elsewhere has left: they come out of the contact order. Flag titles older than a newer source, and sources over 12 months old.
6. **Push back, don't refuse.** If the account is outside the brand's audience, the user's assumption is out of date ("start with Alicia again"), or the data can't support a role, say so first, then deliver the map anyway.
7. **Never edit the user's files.** CRM exports and notes stay as they are. Say what to update.
8. **Don't guess pronouns.** Refer to people by name, or as "they", unless a source states their pronouns. A first name doesn't tell you someone's pronouns.

## Modes

- **Draft** (default): the full map, the order and the contacts file in one pass.
- **Guided:** when the user asks to go step by step, check with them, or says they know these people. Show the people found with proposed roles and evidence, then ask at most three questions about the decisions that change the map (who signs, whether someone is a blocker). A role you're unsure of is written as the likely value plus `(proposed)`, never as a pick presented as settled. The "Start with" line names only someone already in motion; otherwise write "Start with: pending your answers". Label any order "provisional until you answer". Don't write the contacts file yet: say you'll save it once they answer.

## Workflow

```
- [ ] 1. Load: sources for this account, brand/ memory
- [ ] 2. Fact list: every person, title, quote and date, with its source
- [ ] 3. Clean: who left, stale titles, wrong-company rows, fit
- [ ] 4. Assign roles, confidence and personas
- [ ] 5. Order and gaps
- [ ] 6. Write accounts/<company>/contacts.md and run the checker
- [ ] 7. Self-check, then reply
```

### 1. Load

List the project folder. Read every source for the account (usually `accounts/<company>/`), and note each file's date: a save date on a page, an export date, a call date. A file with no date is `undated`: write `undated` where the date would go and say so in Check before outreach. Read `brand/BRAND.md` and `brand/audiences.md` for segments, who the brand is not for, and personas. No `brand/` folder: carry on, mark persona matches `provisional`, and offer to set brand memory up once at the end.

**No sources for the account?** Don't name anyone. Reply with: what to supply (a team or leadership page, CRM contacts, a LinkedIn export, an org chart, call notes, job postings), and the titles to look for per role for a company of that kind, clearly labelled as titles to find. If there's no `brand/` folder either, say persona matches would be provisional. No contacts file with people in it, no email patterns. Under 250 words.

### 2. Fact list

Before judging anything, list each person with every fact about them and where it came from:

```
Marcus Lee | Director of Finance | team-page.md 2026-10-02; crm-export.csv 2026-10-09
  "I'd have to take it to her with a recommendation" | call-notes 2026-10-09
```

Only these facts can appear in the output, each cited to the file that actually says it. Keep dates honest: a page's save date isn't the date a job was posted or a title started. Count rows rather than estimating.

### 3. Clean

Work through [references/contact-data.md](references/contact-data.md): people who left (and whether a past champion who moved is an opportunity at the new company), titles older than a newer source, sources over 12 months old, rows at a different company with a similar name, personal contact details in a source, and fit against the brand's audience.

### 4. Roles

Assign roles from evidence using [references/roles.md](references/roles.md). Seven values only: economic buyer, champion, user, technical evaluator, blocker, influencer, unknown. Give a confidence (high needs a call, reply, CRM activity or org chart; a title alone is medium at best). Match each person to a persona in `brand/audiences.md` by role and what they're measured on; if none fits, write `provisional: <label>`.

### 5. Order and gaps

Lead with whoever is already in motion, then the likely champion, then the economic buyer from a different angle a few days later. Plan how a blocker is brought in rather than writing to them cold. Honour any timing a source gives. For each role nobody known fills, name the titles to look for and where. A role being hired is a gap with a date.

### 6. Write and check

Write `accounts/<company>/contacts.md` in the format in [references/contacts-format.md](references/contacts-format.md). Then run:

```bash
python3 scripts/check_contacts.py accounts/<company>/contacts.md --sources accounts/<company>/
```

Add `--allow "<Name>"` for a person the user named in the conversation rather than a file. Fix every FAIL and rerun. A WARN is something to mention or fix.

### 7. Self-check, then reply

Before replying, check:
- Every name, title, quote and date in the reply is on the fact list.
- No email, phone, URL or tenure appears that a source didn't give; every guess says `unverified`.
- Nobody who left or belongs to another company is in the order.
- No blocker without evidence; no champion called confirmed before they've engaged.
- The first line answers "who first".

Any failure means fix and recheck, not hedge.

## Reply

```
**Start with:** <Name, title>: <one line on why, with the evidence>. <Channel on file, or "no work email on file: <route>">.

**Buying committee**
| Name | Title | Role | Confidence | Persona | Evidence (source, date) |

**Order**
1. <Name>: <why, and when>

**Gaps:** <role: titles to look for, where>
**Stale or excluded:** <who, and why> (only if any)
**Check before outreach:** at most three items: fit, records to update, unverified addresses, old sources.

Saved: accounts/<company>/contacts.md
```

- With no `brand/` folder, the Check line always includes "personas are provisional: no brand memory. I can set one up if you'd like", whatever else the reply says.
- Lead with the pushback when there is one (fit, someone left, the user's premise), in one or two sentences, then the map.
- Keep it under about 300 words outside the table. The table carries a short evidence phrase per person, not the full file: the detail lives in the contacts file. In Guided mode, replace Order with the questions.
- Speak about the brand as the user's ("your audience"), and give the saved path relative to the project folder.
- Talk to the user about the account, never about this skill, its checker, its references or file internals. "Saved: <path>" is enough.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The user knows who to write to on Monday, why, and through which channel, and can see the evidence behind every role. Nothing in the map is a guess presented as fact. The person drafting outreach can open the contacts file and start without asking a question.

A worked example (Quillmetrics mapping Oakline Outfitters) is in [assets/examples/oakline/](assets/examples/oakline/README.md).
