# Worked example: a renovation quote email

Northpine Renovations is fictional. Leah drafted `draft.md`, a quote email to a homeowner. The skill wrote `draft-clean.md` and the trace `draft-trace.md`.

## The reply

> Subject: Your kitchen renovation quote
>
> Hi Daniel,
>
> Thanks for having us out on May 6. Your quote for the full kitchen renovation is $38,400, which covers cabinets, quartz counters and new lighting.
>
> We can start on June 16, and the work will take about five weeks. If anything in the quote needs explaining, call or reply here.
>
> Leah

That's the whole reply. Nothing needed flagging, so there's no "Check" block.

## What happened

- **Specificity gate:** the draft passes, because the third paragraph carries everything: the visit date, the price, the scope, the start date and the duration. The rest of the email surrounds those facts with filler.
- **Layer 1 (claims):** "exceptional craftsmanship" and "transforming your space into something truly special" fail the swap test, since any contractor could write them. They're cut, not reworded.
- **Register (transactional email):** the greeting theatre, the two exclamation marks and the "don't hesitate to reach out" sign-off are gone.
- **Nothing added:** every sentence in the revision traces to the draft (see `draft-trace.md`). The closing line asks for nothing new and claims nothing.

The message went from 118 words to 51 (not counting the subject, greeting and sign-off), and every number survived.
