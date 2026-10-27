# The sequence file

The skill writes one file per sequence: `email/sequence-<slug>.md` in the project (create `email/` if it doesn't exist). A reviewer can read it top to bottom, and a person or a sending tool can load it email by email. It's plain text, so any email tool works.

## Contents
- Header
- The FACTS and OPEN ledger
- One block per email
- Conventions
- Who reads it

## Header

```
SEQUENCE: <name>
Type: welcome | onboarding | nurture | trial | re-engagement | post-purchase | event | newsletter
Status: draft | provisional (no brand memory) | plan only (guided mode)
Audience: <who enters, and which segment>
Consent basis: <how they agreed, with the wording or source> | TBD: <question>
Sender: <name, role, company>
Mailing address: <from brand/senders.md> | [mailing address: needed before sending]
Goal: <the one action the sequence is for>
Entry: <the trigger>
After the last email: <newsletter, suppression, nothing>
Suppress: <who never enters: customers, people in another sequence, no-consent segments>
```

## The FACTS and OPEN ledger

```
FACTS
- offer: free month-end review, a 30-minute call | brand/offer.md · confirmed
- url: https://tallyhouse.example/review | brand/offer.md · confirmed
- deadline: trial ends day 14 | user
OPEN
- mailing address | not in brand memory: ask the user
- customer result for email 4 | none in brand memory
```

Every figure, name, link and quote in the emails appears under FACTS with its source. A line starting `deadline:`, `limit:` or `sunset:` is what licenses deadline, scarcity or "last email" language. Anything missing goes under OPEN, and its slot in the copy is a marked placeholder.

## One block per email

Blocks are separated by a line containing only `---`. The footer starts at a line containing only `--`.

```
---
Email: 2
Job: help them use the checklist on last month's numbers
Trigger: in the sequence, hasn't booked a review
Timing: day 2, 9:00 local
Kind: marketing
Subject: Fill in line 3 first
Preview: Prime cost is food plus labour. Here's the order that saves time.
CTA: Book a free month-end review -> https://tallyhouse.example/review
Exit: books a review (leaves) · unsubscribes (leaves)
Branch: none

Hi {{first_name|there}},

<body>

Hannah
--
Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8
Unsubscribe: {{unsubscribe_link}}
```

## Conventions

- `Kind: service` marks a message tied to something the person bought or requested (receipt, onboarding step, recording they registered for). Everything else is `marketing` and carries the full footer.
- Placeholders are in square brackets and say what's needed: `[link: calendar setup page]`, `[mailing address: needed before sending]`. Merge tags use double braces.
- Branches name the condition and the destination: `Branch: calendar connected → skip to email 4`.
- Timing is from the trigger (day 0), not calendar dates, unless the sequence is tied to a dated event.

## Who reads it

- **A reviewer** reads the header and ledger first, then the emails.
- **Whoever loads it into the email tool** copies each block's subject, preview and body, and sets the trigger, timing, exit and branch rules from the fields.
- **brand-voice-gate** or **content-qa-gate** can check it as a draft before it's loaded.
- **brand-memory** receives feedback: when the user confirms a missing fact (an address, an unsubscribe tag, a real result), suggest recording it in `brand/`.
