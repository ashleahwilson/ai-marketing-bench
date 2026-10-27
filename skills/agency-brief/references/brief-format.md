# Brief and brand-pack formats

## Contents
- The brief: `briefs/agency/<project>.md`
- How to fill each section
- The brand pack: `briefs/agency/<project>-brand-extract.md`
- The review: `briefs/agency/<project>-review-<agency>.md`

## The brief: `briefs/agency/<project>.md`

`<project>` is a short lowercase slug (`google-ads-trial`, `booth-design-2027`). If the file exists, add `-v2` rather than overwrite. The numbered headings are fixed: the review mode reads them.

```
# Agency brief: <project name>

Company: <name> · Contact: <name, role> · Date: <YYYY-MM-DD>
Status: ready to send | draft (gaps marked TBD) | provisional (no brand memory)
Response due: <date> | TBD

## 1. Background
## 2. Business objective
## 3. Audience
## 4. Deliverables
| # | Deliverable | Specs | Quantity | Due |
|---|---|---|---|---|
## 5. Mandatories
### Brand voice and rules
### Approved claims
### Claims not to use
### Legal and compliance
### Accessibility
### Ownership and access
## 6. What not to do
## 7. Budget and payment
## 8. Timeline and review rounds
## 9. Approvals
## 10. Success metrics
## 11. Assets provided
## 12. Your response
## Attached
- <project>-brand-extract.md
```

## How to fill each section

| Section | Comes from | Rules |
|---|---|---|
| 1. Background | `BRAND.md`, `offer.md`, `positioning.md`, the request | Three to six sentences. Public facts only: what the company sells, to whom, what's prompting this project |
| 2. Business objective | The request | The business result, not the activity ("more booked month-end reviews from single-location owners", not "run ads"). If the user gave no objective, `TBD` and ask |
| 3. Audience | `audiences.md` | Segments, who it's not for, the buyer's words. Provisional personas carry "our working view" in the text. Never a customer list |
| 4. Deliverables | The request | One row per deliverable, with the specs the user gave (format, size, length, channel, quantity). An unknown spec is `TBD`. Don't add deliverables the user didn't ask for: suggest them under "Before you send" |
| 5. Mandatories | `voice.md`, `rules.md`, `claims.md`, `proof.md`, the request | See below |
| 6. What not to do | `rules.md`, never-use words, the request | Short list. Quote banned phrases exactly |
| 7. Budget and payment | The user only | The figure or range exactly as given, what it covers (fees, media, production, travel), who pays media, payment schedule and terms. Never estimate one |
| 8. Timeline and review rounds | The user only | Start, key dates, final delivery, and the review rounds (how many, how long the company takes to give feedback). Dates the user didn't give are `TBD` |
| 9. Approvals | The user | Who decides what, by name. One final decision-maker |
| 10. Success metrics | The user | Metric and target as given. No target given: name the metric and write "target to agree in kickoff" or `TBD`. Never invent a number |
| 11. Assets provided | The request, `brand/` | What the company will hand over: the brand pack, logos, photography, account access. Only what exists |
| 12. Your response | Standard questions plus project-specific ones | What the agency must send back, and by when |

### Mandatories in detail

- **Brand voice and rules:** the voice principles, spelling convention, channel rules that apply to this work, and `rules.md` "Everywhere" rules. Not "By skill" or "By sender" rules: those are internal.
- **Approved claims:** only lines in `claims.md` under "Approved", and confirmed offer facts such as published prices. If none are approved, say so: "No performance claims are approved yet. Product facts in the brand pack may be used."
- **Claims not to use:** every claim under "Needs substantiation" or "Restricted", quoted, with "not approved for use". This keeps the agency from repeating a claim it finds on the website.
- **Proof:** a customer quote whose naming permission is unconfirmed goes in with "check with <contact> before naming this customer" in the text the agency reads. Permission "no": leave it out.
- **Legal and compliance:** only requirements the user or `rules.md` gives, plus the ones that follow from the work itself and are true everywhere: ads and endorsements must be truthful and substantiated; paid partnerships are disclosed; reviews and testimonials are never fabricated or bought. Don't cite a statute or a regulator unless the user or brand memory names it.
- **Accessibility:** for web, email, social and video work, recommend WCAG 2.2 AA (captions for video, alt text, contrast, keyboard use). Put it in the brief and list it under "Before you send" for the user to confirm.
- **Ownership and access:** name the items concretely for the work type. Website: the domain, code, design files, content, and hosting and CMS accounts. Ads: the ad, analytics and tag accounts, campaigns, audiences and data. Content and creative: the final files, editable source files and usage rights. The company owns all of them. The agency works through user access the company grants, never shared passwords, and never builds the company's campaigns in an account the agency owns. List under "Before you send" for the user to confirm.

### Things the skill proposes

Anything the brief contains that the user didn't state (review rounds, the accessibility standard, the ownership clause, a response deadline, a suggested extra deliverable) is a proposal. Put it in the brief in plain words, and list each one under "Before you send" so the user confirms it. Don't write "(proposed)" in the brief the agency reads.

### Standard response questions

Pick the ones that fit, then add project-specific ones:
1. Who will do the work, by name and role, and will any of it be subcontracted?
2. Two or three examples of similar work, with a contact we can call.
3. Your approach and plan for the first 30 days.
4. A cost breakdown against the budget: fees, production, media (if any) and any markup, and what's out of scope.
5. Your timeline against ours, including review rounds.
6. How you'll report on the success metrics, and how often.
7. Confirmation that accounts, data and final files stay ours.
8. Anything in this brief you'd push back on.

## The brand pack: `briefs/agency/<project>-brand-extract.md`

Written for the outsider, never about the files. No paths, source tags, status words or `TBD`s. Headings, in this order, skipping any with nothing to say:

```
# <Company> brand pack
For <recipient or project>. Prepared <date>. Please don't share beyond the people working on this project.

## What we sell
## Who it's for (and who it isn't)
## Why customers choose us
## How we sound
## Words we use / words we never use
## Rules
## Claims you can make
## Claims not to make
## Proof you can use
## Questions
Ask <contact name> before using anything not in this pack.
```

## The review: `briefs/agency/<project>-review-<agency>.md`

The same content as the review reply (shape in SKILL.md), for whoever signs off.
