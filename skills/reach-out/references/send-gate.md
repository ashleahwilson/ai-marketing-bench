# Send gate: compliance and deliverability

Run this before staging anything. It **warns, it does not block**: put every failed item at the top of "Check before sending" with the specific rule, and let the user decide. This is practical guidance, not legal advice. Laws change, so when stakes are high, tell the user to confirm with counsel or the regulator's own guidance.

## Contents
- Compliance by recipient jurisdiction
- The footer
- Deliverability
- Batch size

## Compliance by recipient jurisdiction

Use the recipient's country, not the sender's. If it's unknown, assume the strictest regime among the likely options and say so.

| Recipient in | Cold B2B email allowed when | Every message needs | Opt-outs honoured within |
|---|---|---|---|
| **Canada (CASL)** | Implied consent:<br>1. The address was conspicuously published by the person or their employer (not scraped from a directory or bought on a list).<br>2. There's no "no unsolicited messages" notice.<br>3. The message relates to their role.<br><br>Or: an existing business relationship, or a referral where the referrer is named and knows both parties.<br><br>The sender must be able to prove the basis. | Sender name, a mailing address, and a phone number, email or website, all valid for 60 days. A working unsubscribe. | 10 business days |
| **United States (CAN-SPAM)** | No prior consent needed | Accurate sender and subject line, a physical postal address, a clear way to opt out | 10 business days |
| **United Kingdom (PECR + UK GDPR)** | Corporate addresses at limited companies: allowed with an easy opt-out. Sole traders and partnerships are treated like consumers and need consent. | Sender identity, an opt-out, and a basis under legitimate interests | Promptly |
| **EU (GDPR + national rules)** | Varies by country. Some, such as Germany, effectively require consent even for B2B. Default to the most cautious reading. | Sender identity, an opt-out, information on where the data came from if asked | Promptly |
| **Australia (Spam Act)** | Inferred consent from a conspicuously published address, with the message relevant to their role | Sender identity and a functional unsubscribe | 5 working days |

**Quebec:** for recipients in Quebec, ask whether to write in French. Many expect it, and Quebec's language law applies to commercial communication.

Apply a country's rules only when the recipient is in that country. If the country is unknown, write one item, "Recipient country unknown: confirm before sending", rather than a conditional warning for each regime. Batch size and sequence length are deliverability issues, not legal ones. Label them that way.

**Warn when:**
- A Canadian recipient's address came from a list, a directory or an enrichment tool with no published source.
- The recipient is in the EU and no consent basis is recorded.
- The sequence has no opt-out wording.
- The first email has no postal address in the signature.

## The footer

Cold messages need the full footer. Replies to someone who wrote to you (inbound, a reply in their thread) and notes to people you already work with need a normal signature. The opt-out line is optional there.

A cold one-to-one email doesn't need a marketing-style footer. A plain signature can carry what the law requires:

```
[Your name], [role], [Company]
[Street address, city]
If this isn't relevant to you, reply "no" and I won't follow up.
```

Leave the website out of the first email's signature, because it counts as a link. Put the sender's real details in `outreach-profile.md` once, and every draft inherits them. The full signature goes on the first email of a thread. Replies in the same thread can sign with a name only, as long as the opt-out still works. If the sending tool adds its own unsubscribe link, say so and skip the reply-"no" line.

## Deliverability

Spam complaints, not reply rates, now set the limit on cold email. Since February 2024, Gmail and Yahoo require bulk senders to keep complaint rates under 0.3%, and recommend under 0.1%. Microsoft's consumer Outlook.com applies similar authentication rules. Copy and sequence choices affect this directly:

- **Plain text.** No images, no HTML layout, and no tracking pixels in the first touch. Measure replies, not opens.
- **No links in the first email.** Offer the asset and send it when they reply. Links in later touches are fine.
- **Short sequences.** Complaint and unsubscribe rates climb sharply after the third email. Default to 3 touches, make step 2 a reply in the same thread, and give a reason for any fourth.
- **Respect every opt-out instantly** across every sequence and sender.
- **Never fake a reply.** Don't use "Re:" or "Fwd:" on a first touch.

## Batch size

Smaller, tighter batches get more replies and fewer complaints. Above about 50 recipients for one angle, warn and suggest splitting by persona or signal. For lists:
- Build the merge in a CSV, with one draft file per contact.
- Check at least five rendered contacts per persona, or all of them if a persona has fewer.
- Spread sends across days rather than sending all at once.
