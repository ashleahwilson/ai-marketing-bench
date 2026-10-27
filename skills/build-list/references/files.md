# Files in and out

## Contents
- Sources the builder reads
- Exclusions
- The list CSV
- The excluded CSV and the summary
- Adding to an earlier list

## Sources the builder reads

**CSV exports** from a CRM, database, directory, event or webinar. Headers are matched by name, any case, punctuation ignored:

| Meaning | Headers recognized |
|---|---|
| Company | company, account, account name, organization, business, employer, restaurant, clinic, practice, store, shop, brand, merchant |
| Website | website, domain, url, site |
| Email | email, email address, work email, contact email, owner email |
| Person | name, full name, contact, attendee, owner, or first name + last name |
| Title | title, job title, role, position |
| Location | city; province, state or region; country |
| Do not contact | do not contact, dnc, opt out, unsubscribed (yes, true, 1, x) |
| Customer stage | lifecycle stage, stage, status, account type, relationship = customer or client |

Every other column (locations, POS, employees, CRM, platform) is carried into the list as is and can be named in the rubric. If a file has `name` and no company column, `name` is the company.

**URL lists:** a `.txt` file with one URL per line. Each becomes an account with a domain and nothing else; everything else is missing until the user or a connected tool supplies it.

**How accounts merge:** two rows are one account when they share a domain (from the website, a business email, or a company column that holds a domain), or when their names match after removing legal suffixes (Inc., Ltd., LLC, Co., GmbH), punctuation, "the", and treating "&" and "and" alike, provided their domains don't differ. A company name that matches a domain's main part ("Lantern Noodle Bar Inc." and "lanternnoodlebar.example") also merges. Same name with different domains is listed as a possible duplicate instead.

**Country from province:** a Canadian province code with no country is read as Canada and flagged. Nothing else is inferred.

## Exclusions

- **Suppression files:** any cell holding an email suppresses that person; a domain suppresses the whole company; a company name in a company column suppresses the company.
- **Customer files:** names, domains or emails. Clients named only in brand memory are passed by name.
- **Rubric disqualifiers:** applied after suppression and customers.

## The list CSV

`lists/<name>.csv`, one row per kept account, best first. The outreach step reads these columns:

| Column | Holds |
|---|---|
| rank, tier, score | position, tier letter, points from known data |
| max_possible | the score if every missing field turned out in its favour |
| status | `new` or `on existing list` (only when adding to an earlier list) |
| company, domain, country, region, city | from the sources |
| <other source columns> | as exported (locations, POS, employees…) |
| contact_name, contact_title, contact_email | the primary contact: a business email first |
| email_type | business, role (info@, sales@), or personal (withheld: the address is in flags, not in contact_email) |
| other_contacts | the account's other contacts: `Name (Title) <email>; …` |
| reasons | each point earned, with the value: `+30 Locations (6)` |
| missing | fields the rubric needed that were blank |
| flags | conflicts, personal email, could reach a higher tier, no contact left after suppression |
| sources | file and row for every row merged into the account |

Name the file after the job and date: `lists/expo-2026-10.csv`.

## The excluded CSV and the summary

- `lists/<name>-excluded.csv`: company, domain, reason (suppression list, existing customer, disqualified by rubric), detail, sources. Suppressed people are counted and named in the reply; they never appear in the list CSV.
- `lists/<name>-summary.md`: the reply, word for word.
- `lists/<name>-criteria.md`: only when the rubric was reworded or came from the user's message or brand memory.

## Adding to an earlier list

Pass the earlier list with `--existing`. It's read first, so its company names and contacts win, and it's never written to. Every account gets a `status`. The reply says how many accounts are new, and names incoming rows that were already on the list. The output is a new file (`lists/prospects-2026-10.csv`), never the old one.
