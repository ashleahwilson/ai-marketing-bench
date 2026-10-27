# Writing the emails, and the judgment checks

## Contents
- Subject and preview
- Body
- The one call to action
- Proof and facts
- Judgment checks before replying

## Subject and preview

- Subject: say what's inside. Under 50 characters where possible, 60 at most. Plain words, no clickbait, no all caps, no emoji unless the voice uses them.
- Preview text: the line after the subject in the inbox. It adds to the subject, never repeats it. 35 to 140 characters.
- Name the thing ("Your Prime Cost Checklist") on delivery emails. On later emails, name the reader's problem or the next step.

## Body

- Open with the reader, not with you. The first line says why this email, today.
- Short paragraphs, plain text feel. One idea per email.
- Keep the brand's email word limit (`brand/voice.md`, "By channel" → "Email"). Without one, aim for 50-125 words for an action email and up to about 200 for a teaching email.
- Follow the voice: spelling, banned words, exclamation marks, sign-off. A rule in `brand/rules.md` beats a brief.
- Sign off as the sender in brand memory, the way the voice says (for example first name only).
- Merge fields need a fallback (`{{first_name|there}}` or "Hi there").

## The one call to action

- Each email has one primary call to action, with one link (the same link may appear twice). A secondary link competes with it: cut it or move it to another email.
- The call to action matches the email's job. A delivery email links the download; a conversion email links the offer.
- Button or link text says what happens: "Book your free review", not "Click here".
- Use only URLs the user or brand memory gives. Missing URL: `[link: <what it points to>]`, listed as open.

## Proof and facts

- Every figure, result, price, name, date and quote traces to the user, the brief, or `brand/` (FACTS block in the file). Missing stays missing.
- Proof marked `named: no` or `unconfirmed` is used without the name or company, or not at all.
- A claim in `claims.md` under "Needs substantiation", or banned in `rules.md`, stays out even if the brief asks for it. Tell the user about the conflict.
- Asked to write a case study or testimonial that doesn't exist: don't. Write the email around honest proof that does exist (how the product works, who does the work, a feature on record), mark the proof slot as open, and say what real proof would take (one customer, one before-and-after number, their permission). Never "sound real".
- Facts from the user's notes (an event, a Q&A answer) can be used as given, not embellished.

## Judgment checks before replying

The checker counts and matches. These need judgment:

1. **One job each.** Read each email's job line. Could two emails merge? Is any email doing two jobs?
2. **Would they expect it?** Read email 1 as the subscriber. Does it deliver what they signed up for, straight away?
3. **Read from the second sentence.** If nothing is lost, the opener was throat-clearing. Cut it.
4. **Exit logic.** Can someone who already booked, bought or upgraded still get a "book now" email? Fix the exit.
5. **Consent per segment.** Does any segment get marketing email it didn't agree to?
6. **Facts.** Is there a figure, name, result, deadline or limit that isn't in FACTS? Remove it or mark it open.
7. **Voice.** Does it sound like the examples in `brand/voice.md`, not like a template?
