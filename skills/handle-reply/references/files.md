# Files

All three live in the project's `outreach/` folder (create it if needed), beside the outreach drafts. Other skills read them: the cold outreach skill should skip anyone in `suppression.csv` and anyone with an open follow-up in `reply-log.csv`.

## outreach/replies-YYYY-MM-DD.txt

One block per person who replied, blocks separated by a line of `=====`. Inside a block, the header comes first; each drafted message follows a line of `---`. Blocks with no message (out of office, bounce, a hold with no acknowledgement) still get written, so the file is the full record.

```
Status: provisional            (only when there's no brand memory; first line of the file)
=====
CONTACT: Luis Ortega <luis@corbel.example> | Corbel Software
CLASS: interested
ACTION: reply
NEXT: answer pricing; confirm Pipedrive and data location with Maya
FOLLOW-UP: 2026-11-17
REPLY:
> What does it cost for 12 reps, and do you work with Pipedrive?
FACTS
- price: Team plan $49/user/month, billed annually | brand/offer.md
- integrations: Salesforce and HubSpot | brand/offer.md
NEEDS YOU
- Does Pipewise work with Pipedrive? Only Salesforce and HubSpot are on record.
---
To: luis@corbel.example
Kind: reply
Subject: Re: forecast calls

Hi Luis,

The Team plan is $49 per user a month, billed annually...

Maya
=====
```

- `CLASS`: interested, question, objection, not-now, referral, wrong-person, out-of-office, unsubscribe, hostile, bounce.
- `ACTION`: `reply` (a drafted answer), `hold` (a holding reply or acknowledgement, or a dated hold), `confirm` (an opt-out confirmation), `none` (nothing drafted).
- `FOLLOW-UP`: a date, or `none`. Out-of-office and not-now always have a date; unsubscribe and hostile never do.
- `REPLY`: their words, each line starting `> `.
- `FACTS`: one line per fact the drafts use, ending in `| <source>` (`brand/<file>`, `thread`, or `prospect`). Write `- none` if there are none.
- `NEEDS YOU`: one line per question only the user can answer. Write `- none` if there are none.
- Message `Kind`: `reply`, `holding`, `confirm`, `ack` (not-now acknowledgement), `thanks` (to a referrer), `referral-first` (first email to a referred person; its `To:` is the new person).

## outreach/suppression.csv

```
email,name,company,date,reason,source
greg@talvo.example,Greg Pollard,Talvo,2026-11-12,unsubscribe,"replied ""Stop emailing me."""
sales@oldharbour.example,,Old Harbour Supply,2026-11-12,bounce,550 5.1.1 user unknown
```

`reason`: unsubscribe, hostile or bounce. `date`: the date of their reply. Append only. Never delete or edit a row; if the user wants someone removed from it, that's their call to make by hand.

## outreach/reply-log.csv

```
date,contact,email,company,class,action,next_step,follow_up,notes
2026-11-12,Ines Varga,ines@brightline.example,Brightline,out-of-office,none,resume after return,2026-11-25,"auto-reply names a colleague for urgent matters; not contacted"
```

One row per reply, plus one for each referred person you drafted to (class `referral`, with `notes` saying who referred them and what they said). Append only; a later status for the same person is a new row.
