---
name: build-list
description: Builds a scored prospect account list from data the user already has, such as CRM or database CSV exports, directory or event attendee exports, and lists of URLs. Merges duplicates hidden by company name and domain variants, removes suppressed contacts and existing customers, scores every account against the ICP rubric (icp/scoring.md) or criteria the user states, gives a reason for each score, flags missing data instead of guessing it, and returns a ranked CSV plus a short summary with the lawful basis needed for outreach (CASL, CAN-SPAM, GDPR). Use when the user wants a target, prospect, account or lead list built, cleaned, deduped, merged, scored or tiered, for example "build a list from this export", "score these accounts", "clean up the attendee list", "check this against our suppression list", "add these leads to last month's list", or "get me 200 CFOs with emails". Never invents companies, people, emails, revenue or headcount: with no data it explains what's needed. Not for writing the outreach itself.
license: MIT
compatibility: Recommended for large models. On small models it can state a slightly wrong reason or run over its word limit, so check the summary against the CSV. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Build list

Turns the user's own exports into one ranked, deduped, suppression-checked account list that a rep can work from today. Every value in it comes from a file the user gave, or from a connected tool that is named beside the value.

## Ground rules

1. **Missing stays missing.** Never add a company, person, email, phone, revenue, headcount, location count or tool from memory, or infer one from a company name, city or domain ("Kingston Smiles" is not evidence of Ontario; "Harvest Table Group" is not evidence of several locations). Never guess an email from a pattern such as firstname@domain. A blank gets flagged, scored as unknown, and listed as research to do.
2. **No data, no list.** If the user asks for a list and supplies no file and no data tool is connected, don't produce names, not even real companies you know of. Reply with the "No list yet" shape below: what to bring, the columns, how it will be scored, anything in the request that doesn't fit the ICP, and the lawful basis. Then offer to run it as soon as a file arrives. Name sources generically (a CRM export, a licensed data provider), never a vendor or a connected tool the user didn't mention.
3. **Suppression and customers come first.** A suppressed person is removed from every list file; the reply names them only under "Contacts removed", so the user knows why. A suppressed company or domain removes the whole account, all contacts included. Existing customers are excluded wherever they're recorded: a customer file, a CRM stage of Customer, or a client named in `brand/proof.md` or `brand/results.md`. (`named: unconfirmed` in proof means permission to name them publicly isn't confirmed; they're still a client.)
4. **No personal emails for cold outreach.** Never look up or add personal addresses (Gmail, Hotmail, home addresses), even when asked. Personal addresses already in the user's file are kept, flagged, and marked not for cold email without consent. Decline in one sentence that names the reason, using the law for the countries in the list: CASL (Canada) and GDPR or PECR (UK, EU) need consent; for US contacts, a personal address isn't a business contact and the person never offered it for that. Then offer what works instead (the business's published contact, a work address from the user's own licensed data tool with its source recorded, LinkedIn, phone, or asking for consent).
5. **Never overwrite the user's files.** Inputs are read only. Output goes in `lists/`. Adding to an earlier list writes a new dated file.
6. **Pressure changes the length, not the data.** In a hurry, keep the reply under 200 words and lead with the fastest honest path: score what's known, show each account's best possible score, and list the accounts that need data. Don't estimate blanks to make the sheet look complete.
7. **Read before asking.** Check the folder, `brand/` and `icp/` before asking for anything. Ask only for what decides the result.

## Modes

- **Draft** (default): the full pass, then the reply.
- **Guided**: when the user wants to go step by step or approve the criteria first, or when rubric lines worth more than a third of the points can't be scored from the columns. Stop after step 2: report what's in the files (rows, unique accounts, duplicates, suppressed and excluded), show how each rubric line will be scored and against which column, propose a measurable version of each line you can't score, and ask at most three questions. Show no scores, tiers or ranking yet, not even as a preview: a ranked table is the list the user asked to approve first. Build nothing final until the user approves.

## Workflow

```
- [ ] 1. Load: sources, exclusions, brand/, icp/scoring.md
- [ ] 2. Criteria: settle the rubric; write lists/<name>-criteria.md if it needed rewording
- [ ] 3. Build: run scripts/build_list.py build
- [ ] 4. Judge: merges, possible duplicates, rows that aren't the buyer, conflicts, missing data
- [ ] 5. Self-check: run scripts/build_list.py verify, then the judgment checks
- [ ] 6. Reply, and write lists/<name>-summary.md
```

### 1. Load

List the project folder. Sort files into three groups (details in [references/files.md](references/files.md)):
- **Sources:** CSV exports (CRM, database, directory, event attendees, webinar registrants) and text files of URLs. An earlier list the user wants to add to is an *existing* list.
- **Exclusions:** files named like suppression, unsubscribe, opt-out, do-not-contact or bounces go to `--suppress`; customer or client lists go to `--customers`; clients named in brand memory go to `--customer-name`.
- **Context:** `brand/` (read `audiences.md` for who it's for and not for, `offer.md` for "we don't do", `proof.md` and `results.md` for named clients, `rules.md`) and `icp/scoring.md`.

No `brand/`? Build anyway, mark the list provisional, and offer at the end to set up brand memory. A connected enrichment or search tool may fill a gap: write what it returns to `lists/<name>-enrichment.csv` (company, domain, the fields found, and a `source_notes` column naming the tool and date) and pass that file as another `--source`. It never adds a personal email. With no tool connected, work only from the files and say which accounts need research and what to look up.

### 2. Criteria

Use the first that exists: criteria the user states in this conversation, then `icp/scoring.md`, then `brand/audiences.md` with `offer.md` "we don't do" lines (marked provisional), then ask.

The rubric format, the forms the builder can read, and how to reword lines are in [references/rubric-format.md](references/rubric-format.md). If any line needs rewording to be scored (for example "North America" becomes "Country: US, Canada"), or the criteria come from the user's message or brand memory, write `lists/<name>-criteria.md`, one line per criterion, each citing where it came from. Never edit `icp/scoring.md`.

A line that needs judgment and has no column behind it ("growing fast", "good culture fit") is not scored. Say so, and propose a stand-in from a real column (for example "Last funding in the past 12 months") for the user to approve.

Check the request against brand memory too. If the user asks for a job title or a company size the ICP rarely has (CFOs at groups of 1 to 15 restaurants), say so in one line, quoting the ICP range from brand memory, and say plainly who to target instead ("target owners, operators and controllers instead").

### 3. Build

```bash
python3 scripts/build_list.py build --source <export.csv> [--source …] [--urls <urls.txt>] [--existing <old-list.csv>] \
  [--suppress <file>] [--customers <file>] [--customer-name "<client from brand memory>"] \
  --rubric <icp/scoring.md or lists/<name>-criteria.md> --out lists/<name>.csv
```

It merges accounts by domain and by company name with legal suffixes, punctuation and "&/and" removed (so "Lantern Noodle Bar Inc." and "lanternnoodlebar.example" become one account), but never merges two accounts with different domains: it lists those as possible duplicates. It removes suppressed and do-not-contact people, excludes suppressed companies, customers and disqualified accounts, scores each kept account with a reason per point, and writes `lists/<name>.csv` and `lists/<name>-excluded.csv`. It prints the counts the reply needs. Column definitions are in [references/files.md](references/files.md).

### 4. Judge

- **Merges:** confirm each one is the same business. **Possible duplicates** (same name, different domain or city) stay separate and go in "Check before outreach".
- **Rows that pass the rubric but aren't the buyer**, on the row's own words (a food distributor's sales rep at a restaurant expo, a tour company): keep them, flag them, and say why.
- **Conflicts** between sources: keep the first value and list the conflict.
- **Missing data:** the CSV shows `max_possible` and flags accounts that could reach a higher tier once filled. Never fill a blank to settle it.

### 5. Self-check

Run `python3 scripts/build_list.py verify lists/<name>.csv` with the same `--source`, `--urls` and `--suppress` arguments. A FAIL means fix the list, not explain it. Then check:
- The reply is within its word limit (checked, not estimated).
- Every count in the reply is copied from the build report, and every tier or score named in the reply matches the CSV.
- No suppressed person appears anywhere: CSV, summary or reply.
- Every kept account has a reason, and every exclusion has one.
- The reply names no company, person or number that isn't in the files.
- The lawful-basis note names the law for every country in the list (Germany: GDPR, plus its prior-consent rule), and treats each source as what it is. A sign-up, registration or attendee list is never stated as consent: say what to check (what the form said).

### 6. Reply

Write the same content to `lists/<name>-summary.md`. Lead with the recommendation, and don't paste the CSV. **Length:** at most 300 words; 250 for "No list yet" or Guided; 180 when the user is in a hurry. Top tier table: at most five rows. One line per bullet. Check with `python3 scripts/build_list.py words lists/<name>-summary.md --max <limit>` (for a reply with no list, write it to `lists/reply-draft.md` first) and cut until it passes: drop detail the CSV already holds, never the lawful-basis line or the removed contacts.

```
**List ready:** <n> accounts scored, <a> in the top tier. <the one thing to do first>
(Guided: **Criteria to approve:** … · No data: **No list yet:** <why, one line>)

**Top tier**
| # | Account | Score | Why | Contact |

**In and out**
- In: <rows> rows from <files> → <unique> unique accounts (<m> duplicates merged: <one example>)
- Adding to an earlier list: "<k> new accounts added: <names>", and the incoming rows already on the list
- Excluded: <n>, by reason, with names (suppression list, existing customers, disqualified)
- Contacts removed: <name, reason>

**Missing data:** <field: n accounts>; <accounts that could move up a tier once filled>

**Check before outreach**
- Lawful basis: one line per country or regime in the list (see references/compliance.md)
- Personal or role emails flagged; possible duplicates; rows that may not be the buyer

**Files:** lists/<name>.csv · lists/<name>-excluded.csv · lists/<name>-summary.md
```

**No list yet** (no data supplied): what to bring (two or three kinds of source, named generically), the columns it needs (company, website, contact name, title, email, country, plus each rubric field), how it will be scored, the one-line ICP check, and the lawful basis. Offer to run it the moment a file arrives. No placeholder rows, no sample names.

Write to the user in the second person, with file paths relative to their folder. Never mention the builder, its report, its flags or rerunning it.

Lawful-basis notes are in [references/compliance.md](references/compliance.md): flag what applies in one line each, without a lecture.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A rep opens the CSV and works top to bottom without checking anything twice: no suppressed person, no customer, no duplicate, a reason beside every score, and blanks that say what to find. The summary tells a manager in thirty seconds what went in, what came out and why. Nothing in either file was guessed.

A worked example (a Tallyhouse list built from a CRM export and a festival vendor list) is in [assets/examples/tallyhouse-atlantic/](assets/examples/tallyhouse-atlantic/README.md).
