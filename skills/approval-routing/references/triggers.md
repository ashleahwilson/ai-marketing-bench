# Approval triggers: how to judge them

The content decides who else has to see it. Read the whole piece, line by line, and decide for each candidate whether it really is a trigger. Quote the exact words in the route.

## Contents
- The nine triggers
- What is not a trigger
- Blockers no sign-off can clear
- Requester and self-approval
- Versions and stale sign-offs
- No approval rule

## The nine triggers

| Trigger | It is one when the piece… | Examples | Reviewer checks |
|---|---|---|---|
| **performance claim** | states a result, speed, saving or outcome the reader is meant to believe | "cuts no-shows by 38%", "close in 3 days", "40% less time", "from 19 days to 4", a customer's measured result | Substantiation on file for every number: an approved line in `claims.md`, a confirmed result in `proof.md`, or a cited source |
| **comparative claim** | compares itself with a competitor, an alternative or the market, or uses a superlative | "faster than spreadsheets", "better than calling patients yourself", "the fastest way", "the only", "#1" | The comparison is substantiated and fair; the competitor is described accurately |
| **price or offer** | states a price, discount, trial, free item, promo or guarantee | "$349 a month", "30% off", "14-day free trial", "free month-end review" | Every price matches `offer.md` for that audience; terms and end dates are stated |
| **customer named** | names a customer, quotes a customer, or shows their logo | a testimonial with a name, a case study, "Lantern Noodle Bar uses…" | Consent on record in `proof.md` (`named: yes`). See "Customer consent records" in the format file |
| **regulated health** | gives health or medical guidance, or makes a claim about patient data or privacy law | "HIPAA-compliant", "reduces anxiety", patient-record handling | The claim is accurate and supportable; required wording is present |
| **regulated financial** | gives tax, accounting, investment or credit guidance the reader might act on | "tips are taxable income", "you can deduct…", "report them to CRA" | Guidance is general, says it isn't advice, matches current rules |
| **regulated employment** | gives guidance on wages, tips, overtime, hiring or firing | "tip pooling is legal as long as…", "overtime is paid on the base wage" | Statements are general and say the rules vary by place |
| **spend over a threshold** | is paid media whose budget is over the matrix's amount | "Budget: $18,000" against `spend over 10000` | The spend is inside the approved budget |
| **brand change** | changes the logo, name, tagline, colours or other brand assets, or the user says it does | "our new tagline", a rebrand announcement | The change matches the brand decision on file |

A piece can trip several triggers, and one line can trip two ("The fastest way, free for 14 days" is comparative and an offer). List each.

## What is not a trigger

Over-routing wastes the reviewers' week and teaches people to skip the process. These don't add a reviewer on their own:
- **A product feature recorded as confirmed in `offer.md`**, stated plainly: "reconciles Toast, Square and Lightspeed sales automatically every day", "refreshes every 15 minutes". A feature is a description, not a performance claim. It becomes one when it promises an outcome ("so you close in 3 days").
- **General advice with no regulated angle:** "count inventory on the same day every month".
- **The audience description:** "US Shopify merchants doing $1M to $20M a year" is targeting, not a price.
- **A passing mention of a regulated word:** "sales tax filings included" describes a service. Telling the reader what to do about their taxes is guidance.
- **The author's own observation**, not presented as a measured result: "the 20th rolls around and you still don't know how last month went."

When a call is close, list it under the trigger with "(judgment call)" and say what would settle it. Don't add the reviewer silently, and don't drop it silently.

## Blockers no sign-off can clear

These stop the piece whatever anyone signs. Each goes under Blockers with the fastest fix:
- **A brand-rule breach.** A phrase `brand/rules.md` bans ("3 days, not 3 weeks", "real-time", "AI-powered"). The fix is to change the words. An approver can't sign around a standing rule; only the rule's owner can change the rule.
- **No customer consent on record** for a named customer or quote.
- **No eligible signer** for a required role (the requester holds it and there's no backup).
- **An unsubstantiated claim the user wants to publish anyway.** It needs the reviewer the matrix names. The fastest path is usually cutting the claim, which can also drop that reviewer from the route.

Never offer a softened version of a claim ("up to", "many clients", "a leading") as the fix. A softened claim is still a claim. Offer: cut it, or get it substantiated and reviewed.

## Requester and self-approval

- The requester is whoever asked for the piece to go out or wrote it: the user, an `Author:` line, or the name in the request. If it isn't clear and the requester holds a role on the route, ask.
- When self-approval is `no` (or not set), the requester's own sign-off never counts, for any role. Say so in one line, plainly.
- Use the role's `backup:` if the line has one. If not, the role is `TBD` and the route is blocked: ask who signs instead. You can mention who the matrix names elsewhere (for example a backup on another content type) as a question, never as the answer.

## Versions and stale sign-offs

- A sign-off covers the file and version on its `Reviewed:` line, nothing later.
- If the piece changed after sign-off, every required role signs the new version, not only the reviewer whose area changed, unless the matrix says otherwise.
- If the change added a trigger (a new offer, a new claim, a new customer), the new reviewer joins the route for the new version.
- Never rewrite an old route file. A new version gets its own route file; the old one stays as the record of what was signed.

## No approval rule

No `## Approvals` in `brand/rules.md` and no approvals file: the status is **Unknown: no approval rule**. Still do the useful part:
- List every trigger in the content with its quote, and what kind of reviewer would usually check it (for example "someone who can confirm the 38% figure", "whoever handles patient-privacy claims").
- Ask who signs off for this content type and who checks each trigger. Number the questions.
- Don't put anyone's name on the route who the user didn't name. Don't treat the requester as the approver.
- Offer to record the answers as approval lines (see the checklist at the end of the format file).
- Without brand memory, consent can't be on record: a named customer is a blocker until the user confirms written consent.
