# Consent and compliance for lifecycle email

Practical guidance, not legal advice. Laws change; when stakes are high, tell the user to confirm with counsel or the regulator's own guidance. Apply the rules of the **recipient's** country. If it's unknown, assume the strictest likely regime and say so in one line.

## Contents
- First question: how did these people get on the list?
- Consent by country
- Marketing email versus service email
- What every marketing email needs
- Honest subject lines and honest urgency
- What to say when the list has no consent

## First question: how did these people get on the list?

| Source | Lifecycle sequence? |
|---|---|
| Ticked an opt-in box, subscribed, or asked to hear from you | Yes: express consent. Record the wording and date if you have them |
| Downloaded a lead magnet with no marketing checkbox | Deliver the download. In Canada, marketing emails after that rely on implied consent from the inquiry, which lasts 6 months; in the US, allowed with an opt-out. Say which applies |
| Paying customer or active trial user | Yes for service email. In Canada, marketing to customers relies on implied consent from the purchase, which lasts 2 years after it |
| Registered for an event, no marketing checkbox | Send what they registered for. No marketing follow-ups to Canadians without consent |
| Bought, rented, scraped, enriched, or "from LinkedIn" | **No.** This is cold outreach, not a lifecycle sequence. See the last section |
| Unknown | Draft the sequence, put `Consent basis: TBD` in the file, and ask one question about the signup source |

## Consent by country

| Recipient in | Marketing email allowed when | Opt-outs honoured within |
|---|---|---|
| **Canada (CASL)** | Express consent, or implied consent (a purchase in the last 2 years, an inquiry in the last 6 months, or a conspicuously published business address with a relevant message). The sender must be able to prove it. A bought list carries no consent from the people on it | 10 business days |
| **United States (CAN-SPAM)** | No prior consent needed, but every message needs an accurate sender, a non-deceptive subject, a postal address and a working opt-out | 10 business days |
| **UK and EU (PECR, GDPR)** | Consent, or the "soft opt-in" for existing customers marketed similar products with an opt-out every time | Promptly |
| **Australia (Spam Act)** | Express or inferred consent, plus sender identity and a working unsubscribe | 5 working days |

Quebec: ask whether the emails should also be in French.

## Marketing email versus service email

- **Service** (CASL's "transactional" exemptions, CAN-SPAM's "transactional or relationship" messages): receipts, delivery of something requested, account and safety notices, onboarding steps for a product they bought. No unsubscribe is legally required, but an address and a way to reach a person are good practice.
- **Marketing:** anything whose purpose is to promote, including upsells, case studies, offers, the newsletter, and a mixed email whose main purpose is promotional. Needs the full footer.
- When in doubt, treat it as marketing and include the footer. It costs nothing.

## What every marketing email needs

1. **The sender's real name** in the From line and sign-off.
2. **A physical mailing address** (CAN-SPAM, CASL). Take it from `brand/senders.md`. If it isn't there, use the marked placeholder `[mailing address: needed before sending]` and list it as open. Never write a plausible address.
3. **A working unsubscribe**: the sending tool's link or merge tag (use the one in `brand/senders.md` if recorded), or a clear instruction. Honour it across every sequence.
4. **A subject line that matches the content.**

## Honest subject lines and honest urgency

- No fake "Re:" or "Fwd:", no fake account or invoice notices, no subject that promises something the email doesn't contain.
- **Scarcity and deadlines must be real.** "Only 3 spots left", a countdown timer, or "ends Friday" goes in only when the user or brand memory gives the actual limit or date. Otherwise it misleads subscribers and breaks advertising rules (the Competition Act in Canada, the FTC Act in the US).
- Real reasons to act now that usually exist: a trial end date, an event date, the next month-end or season, a price change on record, a sunset ("we'll stop emailing you after this unless you click"), or simply the cost of waiting, in the reader's terms.
- If the user asks for invented urgency: write the sequence without it, say why in one sentence, ask whether a real limit or date exists, and offer to add it the moment they confirm one.

## What to say when the list has no consent

Keep it short and helpful, not a lecture:

1. One line: these people haven't agreed to hear from you, so a nurture sequence to them is cold outreach (name the law that applies to their country).
2. Route it: one-to-one cold outreach with its own consent and compliance check belongs to the library's `reach-out` skill.
3. Offer the consent path: invite them to something they opt into (the lead magnet, the newsletter, an event) through a channel that's allowed, and they enter the sequence once they've opted in.
4. Don't write the sequence for the bought list, and don't schedule anything.
