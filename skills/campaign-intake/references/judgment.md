# Judgment

The checker validates the file. These calls need reading. Work through all six before writing the reply.

## Contents

- Which questions to ask
- Feasibility
- Conflicting asks
- Claims, offers and proof
- Audience against brand memory
- Risks worth naming
- Self-check

## Which questions to ask

Ask a question only if a different answer would change the plan: the audience, the offer, the channels, the budget, the deadline, or who decides. Everything else becomes an `assumed:` value with a sensible default, or an `unknown:` that the next step can carry.

| Ask | Don't ask, assume or carry forward |
|---|---|
| Two stakeholders want different audiences | The exact number of LinkedIn posts ("assumed: 2") |
| The deadline is vague and the scope depends on it | Which day of the week emails send |
| Who the list is (customers or prospects), when it decides consent | Tone, when brand memory has a voice guide |
| A budget is missing and the plan includes paid channels | A budget for an organic-only plan (`none (organic)`) |
| Where the success number is counted, only when there's no obvious place | Approval steps already named in brand memory |

- At most four questions, in one round. Fewer is better. A clean request gets none: when the requester has given the objective, audience, offer, channels, date, budget, approvals and success metric, ask nothing. Definitions (what counts as "active"), list exports, baselines and owners of a check are assumptions or risks, not questions.
- **Two candidate success metrics** ("registrants, SQLs") with no word on which one counts: mark Success metric `open` or `unknown` and ask which one decides success. It sets the conversion action the ads optimize for. Don't silently pick one.
- Each question says what changes: "Customers or prospects? Prospects need a consent check before any email, and change the offer."
- Where brand memory suggests the likely answer, offer it: "Likely: single-location owners (brand/audiences.md)."
- Write the intake anyway, with the open fields marked, unless the user asked to be walked through it first. A question in the reply and an `unknown:` in the file must match.

## Feasibility

1. Count working days (Monday to Friday) from Today to Deadline. The checker prints the count and a rough floor for the route. Public holidays aren't counted: subtract any you know of.
2. Find the longest chain, not the sum: a brief before a build, production before an ad, approval before launch, platform ad review before going live. Add any constraint in the request (a person away, footage that doesn't exist yet).
3. Verdict:
   - **Fits:** the floor plus approvals is comfortably inside the days available.
   - **Tight:** it fits only if nothing slips. Say what has to happen by when.
   - **Doesn't fit:** say so in the first line of the reply, with the reason in plain words ("4 working days, and the case study needs customer sign-off that takes a week"). Never "ambitious" or "tight" for something that can't be done.
   The floors are rough. A floor within about three days of the days available is **tight**, not "doesn't fit". Reserve "doesn't fit" for a clear gap or a hard constraint (footage that doesn't exist, a person away, an event three days out).
4. For a scope that doesn't fit, build the **scoped-down version**. It ships something by the original date whenever anything can: work that reuses what already exists (an email or two to an existing list, a search campaign pointing at an existing page, static ads from existing screenshots) can usually go in a day or two. Name exactly what goes live by the deadline. Only if nothing at all can, say so and give the earliest real date. Never move a date the requester fixed for an event (a webinar, a launch, a sale) to fit the floor: cut scope for that date instead, and never create a clash with another key date. Say what moves to a later date (with the date it could realistically go) and what drops. Set Status to `scoped down: needs approval`, put the scoped version in the fields, and keep the full ask under Feasibility. Never promise the scoped version will hit the original target; say the target needs revisiting if the scope shrinks.

Lead-time defaults (working days, a planning floor, replace with the team's own when brand memory or the user gives them):

| Work | Days |
|---|---|
| content brief | 1 |
| email sequence (up to 3 emails / 4–6) | 3 / 5 |
| LinkedIn posts | 2 |
| Google Ads campaign (build and platform review) | 3 |
| Meta ads campaign, existing creative / new video | 3 / 10 |
| landing page, new | 5 |
| webinar, new (topic, speakers, promotion) | 10 |
| claims review, disclosure check | 2 |
| each named approval round | 2 |

## Conflicting asks

When two people ask for different things in the same thread (audience, offer, goal, budget, channels, dates, what can be said):

- Record each position separately, attributed and dated, under Conflicts. Quote the deciding words where you can.
- Mark every field the conflict touches `open: … (see Conflicts n)`. Don't fill it with one side, a blend ("both groups and single locations"), or a compromise of your own.
- Say what each choice changes (a different audience changes the offer, the channels and the success metric).
- Name who decides: the Decision owner in the request or brand memory, otherwise ask the user who does.
- Fields both people agree on are settled. Record them as settled.
- If one side's ask breaks a brand rule or rests on an unsupported claim, say so under Claims: that's a fact for the decider, not a reason to pick the other side yourself.

## Claims, offers and proof

Check every headline, claim, price, discount, quote and customer name the request wants used against brand memory:

| Brand memory says | Do |
|---|---|
| Confirmed in `offer.md`, `proof.md` with `named: yes`, or `claims.md` Approved | Use it |
| `claims.md` Needs substantiation, or a rule holds it | Don't put it in the fields as the headline or offer. List it under Claims with the evidence that would clear it, offer directions built only from confirmed facts, and route a claims review if the requester still wants it |
| Banned by `rules.md` | Same, quoting the rule |
| A quote with `named: unconfirmed` or `no` | Usable only without the name, or once the customer agrees. Say which |
| Not in brand memory but stated by the requester (a new discount, a launch date) | Use it as the requester's fact, sourced to them, and add `brand memory update` to the route |
| A superlative or comparison ("cheapest", "#1") or a third-party or executive statistic ("our CEO said 25%") | Not usable until there's a source. Don't confirm it from memory |
| A compliance or certification claim ("HIPAA certified", "GDPR approved") | Flag for legal review. Don't confirm it, and don't suggest a reworded version as safe |

Never invent the replacement: no new statistic, quote, result or customer name. Directions for a headline use confirmed facts only.

## Audience against brand memory

- Match the requested audience to a segment in `brand/audiences.md` and quote it in Brand audience match.
- If the request goes beyond what the brand serves (groups of 25 when it serves 1–15, a country it doesn't sell in, a segment listed under "We don't do" or "Not for"), narrow the audience to the served part, say so under Risks or Conflicts with the brand memory line, and ask only if the out-of-range part was the point of the campaign.
- No brand memory: write `none: no brand memory`, use the requester's audience as given, and mark the intake provisional.

## Risks worth naming

- **Consent:** an email to prospects or a bought list needs a consent basis (CASL in Canada; CAN-SPAM opt-out in the US). An opted-in newsletter list is fine.
- **Past dates:** any key date on or before Today. Label it `(past)` and say what it means (is registration already open?).
- **Stale assets:** last year's deck, an old price, proof older than about 18 months.
- **People:** someone the plan depends on is away, or an approver with no time before launch.
- **Measurement:** a success metric with nowhere to count it.

## Self-check

Answer each before replying. A "no" means fix the file, not add a caveat.

1. Does every field have a value, an `unknown:`, an `assumed:`, an `open:` or a `none`?
2. Does every fact trace to the request or a brand memory line? No price, rate, forecast, date or name came from you.
3. If the scope can't be done by the deadline, does the first line of the reply say so, with the reason and a scoped version?
4. Is every disagreement recorded as a conflict, with no field quietly taking one side?
5. Is every held, banned or unsourced claim kept out of the fields and listed with what clears it?
6. Are there at most four questions, each changing the plan, and do they match the `unknown:`s in the file?
