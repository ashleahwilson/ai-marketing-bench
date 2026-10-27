# Campaign decisions

## Contents
- Objective and optimization event
- Structure and budget
- Audiences
- Placements
- Concepts and creative
- Rebuilding from an audit

## Objective and optimization event

Optimize for the action the business wants, as close to revenue as the account's data allows.

| Goal | Objective | Optimization event |
|---|---|---|
| Booked calls, demos, quotes, form fills | Leads | Lead (or Schedule / a custom event) on the confirmation page; or an instant form when the landing page is weak |
| Trials, sign-ups | Sales or Leads | StartTrial / CompleteRegistration / a custom event that fires after sign-up |
| Purchases | Sales | Purchase, with value |
| Job applicants | Leads (or Traffic to the posting), Employment category | Lead or a custom event on the application confirmation; Traffic only if nothing fires |

- Never optimize for link clicks or landing page views when a conversion event fires: the delivery system finds clickers, not buyers.
- The event must already fire and be tested. If the brief or audit says it is, record where. If not, put `[TBD: confirm the <event> fires on <page>]` in OPEN and say it's the first thing to fix. Recommend the Conversions API alongside the pixel when it isn't verified.
- If the event is too rare for the budget (see below), optimize one step up the funnel for now and say when to switch.

## Structure and budget

Default: **one campaign, one ad set, three to six ads.** Add a second ad set only for a real difference in audience or offer (for example prospecting and retargeting), never to "test interests" on a small budget.

Learning rule of thumb (Meta's guidance): an ad set needs about 50 optimization events in a week to leave the learning phase and deliver steadily. So:

- daily budget per ad set should be roughly `50 × cost per result ÷ 7`.
- You don't know the cost per result. Use the user's or the audit's number if one is on record and cite it. Otherwise don't invent one: give the formula, say what budget it implies at a few cost levels **labelled as assumptions**, or ask.
- If the budget can't plausibly reach 50 a week, consolidate to one ad set, use campaign budget, and accept a longer learning period, or optimize for a more frequent event.
- More than two ad sets under about $150/day is almost always too fragmented. Say so.
- Changes: raise budgets by 20 to 30% at a time, a few days apart; big edits reset learning.

Never write a forecast (leads, cost per lead, ROAS) as fact. Name the metric to judge by and when (for example "judge on cost per booked review after about two weeks or 50 leads, whichever is later").

## Audiences

In order of preference for prospecting:
1. **Broad or Advantage+ audience**: country or region, age 18-65+, all genders, no detailed targeting, with the creative doing the targeting. Add audience suggestions only as hints.
2. **Lookalike** seeded from consented customers (best customers or paying customers, not all leads or visitors). Not available in a special ad category.
3. **Detailed targeting**: a few clearly relevant interests or job-related signals, when broad has had a fair run and failed. Never sensitive attributes.

Retargeting: website visitors (30 to 180 days), video viewers, engagers. Small audiences, so keep it to one ad set and a modest share of budget, and only when the audience is large enough to spend (a few thousand people at least).

Exclusions: current customers and recent converters from prospecting. Consent rules for every customer list are in [policy.md](policy.md).

## Placements

Default to Advantage+ placements with assets in both shapes: 1:1 or 4:5 for feeds, 9:16 for Stories and Reels. Choose manual placements only for a reason (a brand-safety rule, no vertical asset at all), and say the reason.

## Concepts and creative

Three to five concepts, each a different reason to act, not three rewordings. Useful angles: the outcome, the problem in the reader's day (described as a situation, not their attribute), how it works, proof on record, the offer itself, the objection answered.

For each concept:
- **Hook**: the first line or first three seconds. Specific, concrete, in the brand's voice. A question is fine if it doesn't assert a personal attribute.
- **Primary text**: hook and offer in the first 125 characters; then one supporting fact from FACTS; then the call to action. Short sentences.
- **Headline** (40 or fewer): the offer or the outcome. **Description** (30 or fewer): a supporting detail or reassurance from FACTS.
- **CTA button**: the one that matches the action (Book now for a booked call, Sign up for a trial, Apply now for a job, Learn more when nothing else fits).
- **Creative brief**: format, aspect ratios, what's on screen, overlay text, and for video a beat list (0 to 3 s hook, then the point, then the CTA) with captions. Phone-shot is fine; say what to film. Never a stock-photo "customer" or an actor presented as a customer.

Match the landing page: the ad's offer and wording should be what the reader sees after the click.

## Rebuilding from an audit

Read `audits/meta-ads/<account>/fixes.md`: an `Account facts` block (currency, period, spend, conversions, countries, optimized events, pixel and CAPI status, budgets, special ad categories) and numbered fixes:

`F1 · <area> · <priority> · <horizon> · Target: <campaign / ad set / ad> · <finding with evidence> · Fix: <what to change>`

- Account facts are sourced facts: cite them as `audit: Account facts`.
- Fixes are proposals, not applied changes. Address every one, blockers first, and record the mapping in a `Fixes:` field in the build header, one line per fix: `F3 → ads A1-A4 rewritten without "real-time"`. If you disagree with a fix or can't apply it (it needs a fact you don't have), say so on its line.
- A compliance blocker (for example a missing special ad category) comes first and the rebuild doesn't scale spend until it's fixed.
- Keep the account's budget unless a fix changes it; never invent targets or forecasts the audit didn't give.
