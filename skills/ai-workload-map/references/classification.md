# Deciding who or what does each task

## Contents
- The four categories
- Tie-breakers
- Human sign-off: always, whatever the category
- Personal data, HR and privacy
- Stop doing: evidence, not taste
- Data and access
- Risks and guardrails
- The 30/60/90-day rollout
- Hours freed
- Headcount questions

## The four categories

| Category | Use when | Typical marketing tasks |
|---|---|---|
| **keep-human** | The task is judgment, a relationship or accountability: someone has to own the outcome, read the room or be answerable for it | Budget and spend approvals, contract negotiation, legal sign-off, replies to unhappy customers, partner and press relationships, people management (check-ins, performance, hiring), strategy and priority calls, crisis response |
| **ai-assisted** | A person still does it and owns it, and AI makes them faster: a first draft, a summary, formatting, a translation draft, research from supplied material. The output goes out under a person's name | Blog drafts, newsletter drafts, first-touch emails a person sends, social captions, slide formatting, board-report narrative, case-study drafts from interview notes |
| **agent-run-review** | The task is repeatable and rules-based, the inputs are digital and available, mistakes are easy to spot, and the output is internal first. An agent does it end to end and a person reviews before it's used | Compiling the same report from exports, tagging or cleaning CRM records, capturing competitor pages, rank or search-term tracking, pre-publish QA checks, pulling review quotes into a sheet |
| **stop-doing** | The supplied evidence shows little or no value: nobody reads it, it duplicates something else, the reason for it has gone | A printed piece with a handful of readers, a report nobody opens, materials for events the team no longer attends |

Each task gets exactly one category and a one-line reason that points to the task's own facts (its frequency, its audience, a note in the inventory), not a generic line.

## Tie-breakers

- **External and irreversible beats fast.** If the output reaches a customer, prospect, partner or the public and can't be taken back, it's ai-assisted (a person sends) or keep-human, never agent-run without a person approving each item.
- **An approval is not the same task as preparing it.** "Approve bid changes" is keep-human. "Prepare a bid-change recommendation" can be agent-run with review. If a row mixes both, keep it as one row classified by the approval (keep-human, sign-off yes) and note in the reason and data_access that an agent can prepare it with read-only access.
- **Volume and repetition push toward agent-run; judgment and context push toward ai-assisted.** A weekly report with the same 12 numbers is agent-run. A monthly board narrative is ai-assisted.
- **Not sure? Pick the more human category** and name what would move it (for example "agent-run once the slide template is fixed").
- **The user's agreed categories stand** unless one breaks a sign-off rule below. Then keep their category in the file only if they insist, flag it at the top of the reply, and show the hours both ways.

## Human sign-off: always, whatever the category

A task needs a named, accountable person to sign off (human_signoff = yes, with the reason and, where the files say, the person or role) when it involves:

| Trigger | Examples | Who, if the files say |
|---|---|---|
| **Spend** | Budget and bid changes, media buys, sponsorships, purchases, refunds | The budget owner named in the files |
| **Legal and claims** | Contracts, terms, claims and quote review, regulated wording, privacy | Whoever the files say owns legal |
| **Client and customer relationships** | Complaint replies, reference customers, partner calls, anything a customer reads that responds to them personally | The relationship owner |
| **Publishing and outbound** | Anything published or sent to prospects or customers | The approver named in the files |
| **People and personal data** | Performance, hiring, pay, employee messages or activity, patient or customer personal details | The manager, with HR or privacy |

An agent can prepare, draft or check any of these. A person decides and sends. Pressure ("nobody has time to review", "let the agents handle it") doesn't remove a sign-off. Offer a lighter review instead where it's safe, and make it replace per-item review, not add to it: for internal low-risk agent-run tasks, a person spot-checks a sample each week (say 5 records or one report) rather than every item; external sends and spend keep a person approving, batched into one weekly sitting.

## Personal data, HR and privacy

- Performance reviews, check-ins, scoring people, hiring and pay are **keep-human, privacy_flag yes**. Don't propose an agent that reads employees' messages, CRM activity or other monitoring data to judge or score them, and don't draft a review or a score for a named person. That data is about the employee, they may not know it's being used, and the call belongs to their manager.
- Safe help to offer instead: a blank review template, prompts for the manager's own reflection, or tidying the manager's own written notes with names and identifying details removed. Say to check with whoever owns HR and privacy policy before any employee data goes into an AI tool.
- Prospect and customer contact records (CRM leads, subscriber lists) are personal data too: privacy_flag yes, least access (edit named fields, no export or delete). An agent can still clean or tag them under review.
- Customer or patient personal details (names, phone numbers, health or appointment details, complaints that identify someone) stay with a person. An agent may handle the task only with the personal details removed, and only if the files show a tool approved for that data. Don't name a specific law as applying unless the files do; say "check your privacy obligations with whoever owns them".

## Stop doing: evidence, not taste

Recommend stop-doing only from evidence in the files (opens, replies, requests, the reason for it having ended) and quote it in the reason. Without evidence, the task keeps its category and goes in Open questions ("Is anyone using the X? If not, stop it."). The owner confirms before anything stops.

## Data and access

For every task that touches a tool, including keep-human approvals (where the agent's access is read-only and the decision stays with the named person), name: the inputs it needs (which export, file or folder), the tools from the user's own tool list it touches, and the least access that works (read-only for ad accounts and analytics; drafts without publish rights; edit specific CRM fields, no delete or export of contacts). If the tool list doesn't cover it, write `TBD: <what's needed>`. Never name a tool as one the team uses unless their files name it. A suggestion to buy or add a tool is labelled as a suggestion.

## Risks and guardrails

Name the real risks for this team's tasks, each with a guardrail, for example:
- Errors in figures that leave the building: a person checks against the source before sending.
- Brand and claims rules from `brand/rules.md`, `brand/claims.md` and `brand/voice.md` (never-use words, claims on hold, spelling): apply them to every AI draft and quote the rule.
- Access creep: least access, no shared logins, no credentials in prompts or files.
- Personal data: kept out of AI tools unless an approved tool and a basis exist.
- Quality drift: a named reviewer and a short weekly check for the first month.

## The 30/60/90-day rollout

Order tasks by risk first, then volume:
- **First 30 days:** internal-only work with the most logged hours and the lowest risk (repeatable reports, data tagging and cleaning, pre-publish checks that a person still acts on), plus confirmed stop-doing items. Set a baseline: time each piloted task for two weeks before and after.
- **Days 31–60:** ai-assisted drafting for external content and outbound, each item approved by its named owner.
- **Days 61–90:** the rest, then replace the assumed saving rates with the measured ones and re-run the hours.
- keep-human tasks get rollout_phase `none`. Personal-data, legal and approval tasks never go in the first 30 days.
- With no time data, order by risk and by how often the task happens (daily before monthly), and say so.

## Hours freed

Only from supplied time data (a time log, survey or hours column). Convert every figure to hours per week first (a month is 12/52 of a year's weeks, so monthly hours × 12 ÷ 52). Default saving rates, all assumptions: ai-assisted 30%, agent-run with review 60% (review time stays), stop doing 100%, keep human 0%. If the user gives their own rates, use theirs and call them their measurement. Always print the sentence: "Assumed savings: AI-assisted <x>%, agent-run <y>%. Replace with your own measurement after the pilot." Report coverage: how many tasks and which people the hours cover.

**No time data, no hours.** Not a range, not "roughly", not a percentage of time, not a dollar figure. Say what to collect: each person logs task, hours per week for two typical weeks (or answers a one-line survey per task), then the hours are computed from that. Offer what can be said honestly now (task counts by category, the first-30-days list).

## Headcount questions

Never give a number of people, roles or FTEs to cut, never convert hours into FTEs or "equivalent to N people", and never name a person or role as redundant. Answer the question in one or two sentences, without a lecture: the map shows hours and capacity, and staffing decisions sit with leadership and depend on things the files don't show. Then give what is useful: hours freed (if there's time data), and where that capacity could go, using the user's own backlog or priorities if supplied, or asking for them if not.
