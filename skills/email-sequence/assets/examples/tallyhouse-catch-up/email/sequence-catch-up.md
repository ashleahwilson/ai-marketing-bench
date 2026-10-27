SEQUENCE: Catch-up bookkeeping, new client
Type: post-purchase
Status: draft
Audience: restaurants that just bought catch-up bookkeeping, Canada and US
Consent basis: paying clients. Emails 1-3 are service messages about the work they bought. Email 4 is marketing, sent on implied consent from the purchase (CASL: 2 years from purchase), with the full footer.
Sender: Hannah Ruiz, Co-founder, Tallyhouse
Mailing address: Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8
Goal: statements uploaded for every backlog month, then the monthly plan
Entry: catch-up bookkeeping purchase confirmed
After the last email: no further sequence. Monthly-plan clients get onboarding instead.
Suppress: anyone already on a monthly plan

FACTS
- offer: catch-up bookkeeping, quoted per month of backlog | brand/offer.md · confirmed
- offer: single location $349/month; groups of 2-15 from $299/location/month | brand/offer.md · confirmed
- offer: monthly P&L, sales tax filings and a named bookkeeper on every plan | brand/offer.md · confirmed
- offer: daily sales reconciled automatically from Toast, Square and Lightspeed | brand/offer.md · confirmed
- url: https://tallyhouse.example/upload | user
- sender: Hannah Ruiz, signature and address | brand/senders.md · confirmed
OPEN
- how long catch-up takes once statements are in | not in brand memory: ask before promising a date
- link to start the monthly plan | not given: email 4 uses a reply as the call to action instead

---
Email: 1
Job: confirm the purchase and ask for the statements
Trigger: catch-up purchase confirmed
Timing: immediately
Kind: service
Subject: Your catch-up: what we need from you
Preview: Bank and POS statements for each month we're catching up.
CTA: Upload your statements -> https://tallyhouse.example/upload
Exit: all backlog months uploaded (skip to email 3)

Hi {{first_name|there}},

Thanks for choosing Tallyhouse to catch up your books. Your bookkeeper starts as soon as we have two things for each month in the backlog: your bank statement and your POS sales report.

Upload them here: https://tallyhouse.example/upload

If a month is missing, upload what you have. Your bookkeeper will tell you what's left.

Hannah
--
Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8

---
Email: 2
Job: remind them about missing statements
Trigger: some backlog months still missing statements
Timing: day 3, then day 7 if still missing
Kind: service
Subject: Still missing a few statements
Preview: Your bookkeeper can't close those months until they're in.
CTA: Upload the missing months -> https://tallyhouse.example/upload
Exit: all backlog months uploaded (go to email 3)

Hi {{first_name|there}},

A few months of your catch-up are still missing a bank statement or a POS report. Your bookkeeper can't close those months until they arrive.

Upload the missing ones here: https://tallyhouse.example/upload

Can't find a statement? Reply and your bookkeeper will help you get it from the bank.

Hannah
--
Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8

---
Email: 3
Job: confirm everything is in and say what happens next
Trigger: all backlog months uploaded
Timing: same day
Kind: service
Subject: We have everything we need
Preview: Your bookkeeper is working through the backlog now.
CTA: Reply with any questions -> reply to this email
Exit: catch-up delivered (go to email 4)

Hi {{first_name|there}},

Every month of your backlog is in. Your bookkeeper is working through it now and will send your P&L for each month when they're done.

[timing: how long catch-up takes, confirm before sending]

Questions in the meantime? Reply to this email and it goes to your bookkeeper.

Hannah
--
Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8

---
Email: 4
Job: invite them onto the monthly plan so they don't fall behind again
Trigger: catch-up delivered
Timing: 3 days after delivery
Kind: marketing
Subject: Stay caught up from here
Preview: Your books are current. A monthly plan keeps them that way.
CTA: Reply "monthly" to start -> reply to this email
Exit: replies or starts a plan (leaves) · unsubscribes (leaves) · no reply (sequence ends)

Hi {{first_name|there}},

Your books are current now. The monthly plan keeps them that way: a P&L every month, sales tax filings, and the same named bookkeeper who just did your catch-up.

Daily sales come in automatically from Toast, Square and Lightspeed. A single location is $349/month.

Reply "monthly" and your bookkeeper will set it up.

Hannah
--
Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8
Unsubscribe: {{unsubscribe_link}}
