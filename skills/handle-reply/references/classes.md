# Reply classes

## Contents
- Precedence
- The classes at a glance
- Class by class
- Follow-up dates
- Answering questions from sources

## Precedence

When a reply carries more than one signal, the first match in this list decides what you say to that person:

1. **bounce**: a delivery failure, not a person
2. **unsubscribe**: any request to stop, in any words
3. **hostile**: anger, "spam", threats to report, with or without an explicit stop
4. **out-of-office**: an automatic reply
5. **referral**: "talk to X", with a name
6. **interested**: wants to talk, see it, or get pricing
7. **question**: asks something specific without committing
8. **objection**: pushes back on need, price, timing of value, or an incumbent
9. **not-now**: interested later, or "try me in January"
10. **wrong-person**: "not me", with no name

The lower signal still gets handled. "Not me, talk to Talia. Also take me off your list" is an unsubscribe for the writer, and a referral you may act on for Talia (state only what was said, and check her consent basis).

## The classes at a glance

| Class | Action | Message | Suppress? | Follow-up |
|---|---|---|---|---|
| interested | reply | answer + one next step, ≤ 90 words | no | 3 business days |
| question | reply or hold | answer from sources; hold the rest, ≤ 90 words | no | 3 business days, or the date you promised |
| objection | reply | one reply, ≤ 90 words, one ask | no | one closing note after 5 business days, then stop |
| not-now | hold | optional acknowledgement, ≤ 40 words | no | the time they named |
| referral | reply | thanks to the referrer (optional, ≤ 30 words) + first email to the new person | no | 3 business days for the new person |
| wrong-person | reply or none | one-line thanks; may ask once who handles it | no | none |
| out-of-office | none | nothing | no | after their return date |
| unsubscribe | confirm or none | one line, ≤ 20 words, or nothing | yes, now | none |
| hostile | none, or confirm | nothing; or a factual line on where the address came from and that it's removed, ≤ 50 words | yes, now | none |
| bounce | none | nothing | yes (hard); retry once (soft) | soft: 3 days |

## Class by class

**interested.** Answer anything they asked (see "Answering questions"), then one next step: the entry offer from `offer.md`, or "what day suits you?". Never invent a booking link, a meeting length, or time slots. If they asked for pricing and it's listed, give it exactly as listed, including "from".

**question.** Same rules as interested, without pushing a meeting. If every question is unanswerable, the whole reply is a holding reply: thank them and name what you'll confirm. Don't promise a day in the draft; the follow-up date (two business days out is a sensible default) goes in the log and in Needs you.

**objection.** One reply, never a debate. Acknowledge their position in their words, without arguing and without running down whoever does it today (their current tool, agency or in-house person). Give one or two differences that are true and on record in `brand/` (offer, positioning, proof with permission). No invented customer stories, savings or percentages: there is no "others felt the same way" without a real, cleared example. End with one low-pressure ask. If they object again, close the loop politely and stop.

**not-now.** Stop the sequence. Set the follow-up for the time they named. An acknowledgement is optional and short: thanks, and when you'll check back. No pitch, no "in the meantime" resource unless they asked for one.

**referral.** Two parts:
1. To the referrer: an optional thank-you, at most 30 words, no pitch. Skip it if they also opted out (a confirmation line replaces it).
2. To the new person: a first email that follows cold first-touch rules (50 to 90 words, plain text, the sender's full signature, mailing address and opt-out line). Open with the referral stated exactly: "Ruth said you run sales ops at Halden." Then the reason for writing, one fact from sources, one ask. Check the suppression list first. Flag the consent basis for the new address (see compliance.md).

**wrong-person.** A one-line thanks. You may ask once, in that same line, who looks after it. Then stop.

**out-of-office.** Draft nothing. Pause the sequence and set the follow-up after their return date. A colleague named "for urgent matters" is logged as a note, not contacted: the auto-reply exists to route urgent business, and a cold pitch isn't that. If the reply says they've left the company, log it and suggest finding the right person as a new contact, without claiming anyone sent you.

**unsubscribe.** Suppress the address now, across every sequence and sender. A confirmation is optional; if you write one, it's one line with no question, link, offer, or "if you ever change your mind": "Done, you're off the list. Maya". If the user asks for a door-opener, write the confirmation, say in one sentence why the rest is left out (they asked to stop; anything more is a new commercial message to someone who opted out, and a complaint risk), and leave it there.

**hostile.** Suppress now. Don't argue, don't defend the product, don't explain the law to them. Default: no reply. If they asked how you got their address, a factual answer can calm things down, and in some places they're entitled to it: one or two sentences giving the source on record in the ledger (for example "It was listed on your company's team page") and confirming removal. Never claim they signed up or opted in when they didn't. In your report to the user, say both: there's a complaint risk (name the regulator they threatened, if any), and keep the dated record of where the address was published. Don't leave either in the file only.

**bounce.** Hard bounce (user unknown, address rejected, 5.1.1): suppress the address with reason `bounce`, draft nothing, and suggest finding a current address for that company as a new contact. Soft bounce (mailbox full, temporary failure): retry once in 3 days, then treat as hard.

## Follow-up dates

Use today's date, and write dates as YYYY-MM-DD.

- **Out of office with a return date:** the second business day after they're back (back Monday 7 December → Wednesday 9 December). Without a date: 7 days.
- **Not now, with a month or season:** the first Tuesday of that month (April 2027 → 2027-04-06). "After the holidays" → the first Tuesday of January. "Next quarter" → the first Tuesday of the quarter. No time given: 90 days.
- **A holding reply:** two business days, shown in Needs you as the date to answer by. The draft itself names no day unless the user gives one.
- **Interested or question with a full answer:** 3 business days.
- **Objection:** one closing note after 5 business days, then stop.

## Answering questions from sources

For each question, find the line that answers it:

| Source | Use it as |
|---|---|
| `brand/` fact tagged `confirmed` | fact |
| `brand/` fact tagged `provisional` | fact, flagged in the report for the user to check |
| `brand/` fact tagged `assumed`, or `TBD:` | unknown |
| `claims.md` "Needs substantiation" or restricted, or banned in `rules.md` | not usable, even if the prospect asks about it directly |
| the original outreach email | what was already said; repeat it, don't extend it |
| the prospect's own words | their facts (locations, tools, timing) |

If nothing answers it, it's unknown. Typical unknowns: a price for a case outside the price list, a discount, a start date or onboarding time, an integration not named, a security certification or compliance standard, data residency, a contract term, a policy about who does what. For each one:
- the reply says what you'll confirm and when;
- it goes under `NEEDS YOU` with the exact question and who asked;
- the reply gives what *is* on record nearby, if it helps ("we sync with Salesforce and HubSpot today"), without implying an answer to the part that isn't.

Hold neutrally. "I'll confirm whether we handle X or you keep your current provider for it" is fine; "I'll confirm how we work alongside your provider" answers the question by assuming it.

Answer at the level of the source. "Syncs deals from HubSpot" doesn't become "two-way HubSpot sync". "From $49 per user" stays "from"; it doesn't become a quote.
