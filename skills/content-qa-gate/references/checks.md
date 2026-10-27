# Judgment checks

The checker finds what a pattern can find. These checks need reading. Work through all five.

## Contents

- Brief fit
- Claims
- Compliance and brand rules
- Voice
- The reader's path

## Brief fit

Read the brief line by line against the piece.

| Brief field | Check | A miss is… |
|---|---|---|
| Goal | Would a reader of this piece be moved toward it? | Hold if the piece serves a different goal |
| Audience | Is it written to that reader (their situation, their size, their words)? | Hold if it's written for a different audience |
| Key message | Is it stated plainly, early? | Fix |
| Must include | Is each item there, and accurate? | Hold for each missing item |
| CTA | Same wording intent, same URL or action as the brief | Hold if it's a different action or URL |
| Primary keyword | In the title, H1 and first 100 words (search channels only) | Fix |
| Length | Inside the range | Fix; Hold only if it's so short the must-includes can't fit |

Never fill a missing must-include yourself in the report: say it's missing and what the brief asked for.

## Claims

Go through every CLAIM line from the checker, plus any claim without a number ("trusted by owners across Canada", "clients tell us…", "we're adding PayPal next").

For each one:
1. **Is it in brand memory as confirmed, in the brief, or cited with a link in the piece?** If not, it's a blocker. The fix is either a source link the user supplies, or deleting the line.
2. **Is it right for this context?** A price that's in `offer.md` can still be the wrong plan for this reader ($299 is the group rate; single-location is $349). That's a blocker, and the fix states the right figure.
3. **Quotes.** The wording must match `proof.md` exactly. Check the naming permission there: if it's `no` or `unconfirmed`, it's a blocker until the customer agrees, or until the name is removed.
4. **Third-party statistics** need a link to the original source in the piece. Don't confirm them from memory, even when they sound familiar.
5. **Roadmap and future claims** ("we're adding PayPal next", "coming soon") need a source in brand memory or the user's confirmation.
6. **Superlatives and rankings** ("#1", "the leading", "the only") need proof that would hold up if a competitor complained. Otherwise they're a blocker.

The author's own specifics (a client's comment in a client newsletter, a meeting time, an event date) are not claims to source. Leave them alone.

## Compliance and brand rules

- **Rules in `brand/rules.md` → Everywhere** are hard rules. A breach is a blocker. Quote the rule in the fix.
- **Affiliate and sponsored links** (`?ref=`, `?aff=`, `/go/`, partner offers) need a clear disclosure where the brand's rules say. If the rules don't say, put it before the first such link.
- **Testimonials and endorsements** need a recorded source and permission. A testimonial that isn't in `proof.md` is a blocker.
- **Regulated claims** (health, finance, legal, guarantees, "free" with conditions) need whatever `claims.md` → Restricted says. If it says nothing and the claim is a promise of an outcome, flag it for review.

## Voice

- If brand-voice-gate already ran (`<name>-gated.md` with a trace beside it), skip voice. Say "voice: already gated".
- If not, check only the hard voice rules: never-use words (the checker lists them), the brand's spelling convention, and the channel rules in `voice.md` (length, person, exclamation marks). List voice problems as fixes, and suggest running brand-voice-gate for a full pass. Don't rewrite.

## The reader's path

- Is there exactly one primary action, and is it the brief's?
- Does every link go where its text says? (Check the URLs read sensibly; you can't click them.)
- Any dates, offers or events that will already have passed on the publish date?
- Would a reader reach the end without hitting a placeholder, a broken image or a dead end?
