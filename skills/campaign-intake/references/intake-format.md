# Intake format

The intake is one Markdown file, `intake/<slug>.md`. The top part is a fixed list of `- Field: value` lines that the brief and build steps read. The sections below it hold the reasoning a person needs. The format is stable: change it only with a version bump.

## Contents

- The file
- The fields
- Value conventions
- Status
- Route vocabulary
- The sections
- How the next steps read it

## The file

```markdown
# Intake: January catch-up campaign

Status: needs answers
Today: 2026-11-02
Brand memory: brand/ (read 2026-11-02)
Sources: requests/catchup-email.md (Dev Patel, 2026-10-30)

## Fields

- Campaign: January catch-up campaign
- Requested by: Dev Patel [source: requests/catchup-email.md]
- Objective: sign new catch-up bookkeeping clients [source: Dev Patel, 2026-10-30]
- Business result: 40 new catch-up clients by 2027-02-26 [source: Dev Patel, 2026-10-30]
- Audience: independent restaurants 1–15 locations that are behind on their books [source: Dev Patel; capped by brand/audiences.md]
- Brand audience match: Independent restaurants and small groups, 1–15 locations (brand/audiences.md)
- Offer: free month-end review, then catch-up quoted per month of backlog [source: brand/offer.md · confirmed]
- CTA: "Book a free month-end review" → unknown: landing page URL (ask: Dev)
- Channels: email; Google Ads; LinkedIn posts
- Deadline: 2027-01-11
- Key dates: 2027-01-11 launch; 2027-02-26 goal date
- Budget: 4000 CAD (Google Ads, January)
- Assets existing: newsletter list, about 1,900 opted-in subscribers; pricing page; Lantern Noodle Bar quote (naming unconfirmed)
- Assets needed: landing page for the review offer; 3 emails; Google Ads search campaign; 2 LinkedIn posts
- Approvals: Hannah Ruiz (all ad copy) [source: Dev Patel, 2026-10-30]
- Decision owner: Dev Patel
- Success metric: catch-up clients signed by 2027-02-26 (target 40)
- Measured by: unknown: where signed clients are counted (ask: Dev)
- Route: content brief (landing page, emails); email sequence (3 emails); Google Ads campaign (search, January); LinkedIn posts (2, Dev's profile); claims review (ad copy, before Hannah's sign-off)

## Feasibility
## Conflicts
## Claims and brand checks
## Assumptions to confirm
## Questions
## Risks
## For the next step
## Updates
```

## The fields

All 19 are required. A field with no answer is written `unknown: <what's missing> (ask: <who>)`, never left out or left blank.

| Field | Write it as |
|---|---|
| Campaign | A short name. Becomes the slug |
| Requested by | Name and role from the request |
| Objective | What the campaign should get people to do, in one line |
| Business result | The business number it serves (clients, revenue, renewals), with a date if given |
| Audience | One specific audience. Narrowed to what the brand serves; the narrowing is noted |
| Brand audience match | The matching segment quoted from `brand/audiences.md`, or `none: <why>` (no brand memory, or no segment fits) |
| Offer | What the audience gets for acting. Only confirmed brand facts or the request |
| CTA | `"<action text>" → <URL>` or `→ unknown: URL (ask: <who>)` |
| Channels | Semicolon-separated |
| Deadline | `YYYY-MM-DD`: the date it must be live |
| Key dates | `YYYY-MM-DD <label>` separated by semicolons. A date already past is labelled `(past)` |
| Budget | A number, see below |
| Assets existing | What the requester says exists, with any condition on its use |
| Assets needed | Each deliverable the plan requires, with a count where known |
| Approvals | `<name> (<what they approve>)`, semicolon-separated |
| Decision owner | Who settles a conflict or approves a scope change. `unknown` if nobody is named |
| Success metric | The one number that says it worked, with its target and date |
| Measured by | Where that number is counted |
| Route | The next pieces of work, in order, from the route vocabulary |

## Value conventions

| Situation | Write |
|---|---|
| Known | `<value> [source: <file or person>, <date>]` (the source tag is optional on Channels, Deadline, Key dates, Budget, Route) |
| Not given and it matters | `unknown: <what's missing> (ask: <who>)` |
| Not given, a safe working default exists | `assumed: <value> (confirm: <who>)`, and the same line under Assumptions to confirm |
| Stakeholders disagree | `open: <short summary> (see Conflicts <n>)` |
| Deliberately nothing | `none (<why>)`, for example `Budget: none (organic)` |

**Dates** are ISO (`2027-01-11`). Resolve a date with no year to the next occurrence after Today. "End of Feb" is the last calendar day of February. A vague date ("before the holidays") stays `unknown` or becomes `assumed:` with a real date.

**Budget** is digits only, no `$`, `k` or commas: `4000 CAD (Google Ads, January)`, `2500 CAD per month (Meta, Dec–Jan; 5000 total)`, `10000-15000 USD (to confirm)`. Currency only if the request gives one.

## Status

| Status | When |
|---|---|
| `ready` | Nothing blocks the next step. Open items, if any, don't change the plan |
| `needs answers` | A question or conflict changes the audience, offer, channels, budget or date |
| `scoped down: needs approval` | The full ask can't be done by the deadline; the fields describe the scoped version, and the full ask is under Feasibility |
| `hold` | The campaign as asked can't run (an audience or offer the brand rules out, a claim it can't make) and there's no version to scope down to |

## Route vocabulary

Each route item starts with one of these terms, then the specifics in brackets:

`content brief`, `email sequence`, `LinkedIn posts`, `Google Ads campaign`, `Meta ads campaign`, `outreach`, `claims review`, `disclosure check`, `accessibility review`, `voice check`, `QA before publish`, `brand memory update`, `agency brief`, `approval routing`, `prospect list`, `ICP`, `competitor profile`.

Work with no step here (video production, landing page design, LinkedIn ads, webinar production, print) is written `other: <work>`.

Order: anything that unblocks the rest first (a brand memory update, a claims review of a headline), then briefs, then builds, then checks before launch.

## The sections

- **Feasibility.** Working days from Today to Deadline, the deliverables, and the verdict: fits, tight, or doesn't fit. If it doesn't fit: the reason in one line, the scoped-down version, and what moves later or drops.
- **Conflicts.** One numbered item per disagreement: the topic, each person's position quoted or closely paraphrased with the date, what each choice changes, and who decides. Never a blended answer.
- **Claims and brand checks.** Every headline, claim, price and quote the request wants used, each with its status in brand memory (confirmed, needs substantiation, banned by a rule, naming unconfirmed, not in brand memory) and what would clear it.
- **Assumptions to confirm.** One line per `assumed:` value.
- **Questions.** The blocking questions only, at most four, each with what changes depending on the answer.
- **Risks.** Consent for the list, stale assets, past dates, dependencies on people who are away, anything that could stop launch.
- **For the next step.** One line per route item: what it takes from this intake (for example "content brief: landing page; goal and CTA as above; must include the free month-end review; publish 2027-01-08").
- **Updates.** `YYYY-MM-DD | what changed | who said so`, newest first. Empty on the first write.

## How the next steps read it

| Next step | Reads |
|---|---|
| A content brief | Objective → Goal; Audience; one brief per channel piece in Assets needed; Offer and confirmed claims → must-include candidates; CTA; Key dates → publish date; Claims and brand checks → Avoid |
| An email sequence | Audience; the list in Assets existing and its consent basis from Risks; Offer; CTA; Key dates for send timing |
| LinkedIn posts | Whose profile; Offer; confirmed proof only |
| A Google Ads or Meta ads campaign | Budget, Deadline and Key dates for flighting; Audience; Offer; CTA URL; Success metric and Measured by for the conversion action |
| A claims or disclosure check | Claims and brand checks |

A next step treats any `unknown`, `assumed` or `open` value as not settled: it asks, or carries it forward as a `TBD`. It never fills one in.
