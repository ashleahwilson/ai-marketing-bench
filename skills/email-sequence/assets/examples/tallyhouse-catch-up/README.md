# Worked example: a post-purchase sequence for catch-up bookkeeping

Tallyhouse is a fictional restaurant bookkeeping firm. The files:
- `request.md`: what the user asked
- `brand/`: the parts of brand memory the skill reads (offer, voice, rules, senders, proof, claims)
- `email/sequence-catch-up.md`: the sequence file the skill wrote
- `reply.md`: the reply the user got

## Choices worth noticing

| Choice | Why |
|---|---|
| Emails 1 to 3 are `Kind: service`, email 4 is `marketing` | The first three are about work the client bought. Only the monthly-plan invitation promotes something, so only it needs the unsubscribe |
| Email 2 repeats on day 7 only if statements are still missing, and everyone skips to email 3 once uploads are complete | Behaviour drives the sequence, not the calendar |
| Email 3 has a marked gap for the turnaround time | Brand memory doesn't say how long catch-up takes. A promised date would be an invention |
| Email 4 asks for a reply instead of linking a sign-up page | No sign-up URL was given, and one wasn't guessed |
| No speed claim and no customer quote | "3 days, not 3 weeks" is banned until substantiated, and the Lantern quote isn't cleared to name |
| The $349 price appears, the group rate doesn't | The audience is mostly single locations; one price keeps the email to one idea |

Every email is under 120 words, has no exclamation marks, and signs off "Hannah", as the brand's email voice asks.
