---
name: disclosure-check
description: Checks marketing content for the disclosures it needs and whether each one is clear and placed where a reader will see it, then gives the exact fix text and placement. Covers affiliate links, sponsored content and paid partnerships, influencer and creator posts (#ad buried in hashtags or after the "more" cut-off), testimonials and reviews with a material connection (employees, investors, free product, incentives), "from" prices, mandatory fees and billing terms, free trials that renew automatically, contests and giveaways (no purchase necessary, rules, skill-testing question in Canada), email sender identification and unsubscribe, and AI-generated imagery where brand rules require a label. Names the Canadian or US rule behind each finding, never as legal advice. Use when the user asks "does this need a disclosure", "is the #ad OK", "check this caption, ad, email, pricing page or giveaway before it goes out", or wants a disclosure removed. Can write a fixed copy on request.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Disclosure check

Finds what a piece has to tell the reader (it's paid, the reviewer works here, the trial renews, there's a fee, the contest has rules) and checks the reader will actually see it. It doesn't rewrite the piece. It says what's missing or buried, the exact words to add, and exactly where.

## Ground rules

1. **Present isn't enough.** A disclosure counts only if a reader sees it before they act: first line of a caption, before the first affiliate link, beside the price or the sign-up button, with the quote. `#ad` as the 18th hashtag, a footnote 20 lines below the price, or a line at the end of the post is buried, so it's a finding.
2. **Every fix is paste-ready.** Exact text plus exact placement ("first line of the caption, before 'Month-end'"). Use the brand's wording from `brand/rules.md` word for word when it exists.
3. **Missing stays missing.** Facts in a fix (a renewal price, a prize value, a mailing address, what a customer received) come from the piece or brand memory. If they aren't there, leave a marked blank and list it under **Needs your input**. Never invent a URL, price, date, address, relationship or replacement testimonial. Terms stated for one plan or price (a footnote on Starter and Growth) don't carry over to another (a trial plan with no price on the page). Notes inside the piece itself (a deal line, a source tag, a brief) are the user's facts: use them, don't question them.
4. **Some problems a disclosure can't fix.** A testimonial from someone who doesn't exist (a generated person, an invented customer), a trial or offer that isn't in brand memory, a creator claim the brand couldn't make itself. Say so and recommend removing or confirming it, rather than adding a label.
5. **The disclosure stays.** If the user or their client asks to remove, shrink or move a required disclosure, keep it, give the reason in one or two sentences, and offer a lighter compliant version as paste-ready text. Lighter means shorter or smaller, never vaguer or later. No lecture, no refusal. See [references/fixes.md](references/fixes.md), "When the client wants the disclosure gone".
6. **Don't invent problems.** A piece that's clearly disclosed gets **Ready**, with at most two optional suggestions. Don't demand extra hashtags, repeat disclosures or terms the piece already shows.
7. **Rule names, not legal advice.** Name the rule (Competition Act, Ad Standards' influencer guidelines, CASL, the FTC Endorsement Guides, ROSCA, CAN-SPAM) and what it expects. Don't cite section numbers you aren't sure of or declare anything illegal. One line at the end says it isn't legal advice; contests and regulated offers get one sentence recommending a lawyer looks at the rules.
8. **Never edit the original.** Reports and fixed copies are new files.

## Modes

- **Draft** (default): the full check in one pass, with every fix written out.
- **Guided** (when the user asks to go step by step): stop after each **Hold** item and ask for the missing fact before writing its fix.

Neither mode publishes, sends or changes anything outside the new files.

## Workflow

```
- [ ] 1. Load: the piece, brand/ (BRAND.md, audiences.md, senders.md, offer.md, proof.md, rules.md)
- [ ] 2. Run scripts/disclosure_scan.py
- [ ] 3. Judge each trigger (references/rules.md), and find the ones a pattern can't
- [ ] 4. Write each fix (references/fixes.md)
- [ ] 5. Self-check, then reply and write <name>-disclosures.md
- [ ] 6. On request: write the fixed copy <name>-disclosed.<ext>
```

### 1. Load

Read the piece and everything in `brand/`. Countries come from `BRAND.md`, `audiences.md` or `senders.md`; house disclosure wording from `rules.md`; relationships and incentives behind each testimonial from `proof.md`; prices and offers from `offer.md`; mailing address and opt-out line from `senders.md`.

**No brand memory?** Check against both Canada and the US and use the stricter requirement. Say in the reply that the result is provisional because the countries they sell in, house wording and testimonial relationships aren't recorded, and ask where they sell. Offer to set up a brand memory. Keep the piece's own spelling and conventions in any fix text.

### 2. Run the scanner

```bash
python3 scripts/disclosure_scan.py <piece> --channel <social|email|web|blog|ad|newsletter> --brand brand/
```

It reports the jurisdiction found in brand memory, the brand's house wording and sender details, every trigger (affiliate link, paid term, discount code, testimonial, price, fee, trial, contest, email, AI imagery), each disclosure **FOUND** with its position, and what's **MISSING** or **BURIED** (after the links, past the ~125-character cut-off, inside a trailing hashtag block, in a footnote far from the price). For each testimonial it shows the matching `proof.md` line. It can't judge meaning: you check every line in step 3.

### 3. Judge

For each trigger, decide with [references/rules.md](references/rules.md): is a disclosure required, is the one there clear, and will the reader see it in time? Then look for what a pattern misses:
- An attribution that hides a connection (an employee shown as "owner" of a business that closed).
- "No strings", "risk-free" or "cancel anytime" contradicting the terms.
- A plan, trial, discount or prize the piece promotes that isn't in `offer.md`.
- A creator or testimonial claim that brand rules or `claims.md` bar. The brand is responsible for what its paid creators say.
- An email subject that fakes a reply ("Re:").

Verdict:

| Verdict | When |
|---|---|
| **Ready** | Every required disclosure is present, clear and seen in time |
| **Fix first** | Disclosures are missing or buried, and every fix can be pasted from facts on hand |
| **Hold** | A fix needs a fact only the user has (a price, a relationship, rules), or a disclosure can't fix it (fake testimonial, unconfirmed offer, barred claim). A side question that doesn't block the disclosure goes under **Needs your input**, not into the verdict |

### 4. Write the fixes

Use [references/fixes.md](references/fixes.md). Brand wording first, word for word. Fill brackets only from the piece or brand memory; show the basis for any figure you compute (12 × $349 = $4,188). One finding per line, located by a short quote. For affiliate links, list every affiliate link by name with its marker (`?ref=`, `?aff=`, `/go/`), and name the links that aren't affiliate links.

### 5. Self-check, then reply

Before replying, check every line of your draft:
- Each finding has exact text and an exact place. Each fact in a fix traces to the piece or `brand/`, or is a marked blank listed under **Needs your input**.
- No fix moves a disclosure later, makes it vaguer, or removes one.
- No term is written for an offer brand memory doesn't confirm, including generic renewal or cancellation wording.
- Nothing already compliant is listed as required.
- No mention of the scanner, its output, file internals, or any skill name, including this one. The reply and the report go to clients and creators.

If any check fails, rewrite that line. Reply in this shape, and write the same content to `<name>-disclosures.md` beside the piece:

```
**Verdict:** Ready | Fix first | Hold: <one-line reason>
**Checked against:** <Canada and/or US rules, named> · <from brand memory | provisional: no brand memory, ask where they sell>

**Fix these**
1. <where: short quote> · <what's missing or buried, and why it matters to the reader> · Fix: "<exact text>" · Place: <exact placement>

**A disclosure won't fix these** (only if any)
1. <where> · <why> · <remove, or what to confirm>

**Needs your input** (only if any): <each fact only the user has>
**Already clear:** <one line>
<one line: this checks against the rules named above and isn't legal advice>
```

For **Ready**, the reply is the verdict, the "Checked against" line, "Already clear" and the last line: under 120 words. When the user wants a disclosure removed, lead with the recommendation (keep it) and the lighter version, under 200 words.

### 6. Fixed copy, when asked

"Add the disclosures", "fix it" or "save a fixed version" means write `<name>-disclosed.<ext>` beside the original. Apply every fix that needs no new facts, using the brand's wording. Remove what a disclosure can't fix (a fake testimonial) and say so. Where a fix needs a fact you don't have, leave a marked blank such as `[price after trial]` and list it. An offer that isn't in `offer.md` (a trial, a discount, a plan) gets no terms in the copy at all, not even generic ones such as "Renews automatically" or "Cancel anytime", and no charge date worked out from the trial length: keep the offer line with a marked blank such as `[trial terms: confirm the trial exists, then add price after trial, first charge date, how to cancel]`, or remove it, and say which. Then scan the copy again and report what's fixed and what's still open. Refer to files by their names relative to the project folder, never full system paths, and don't describe your own re-checks.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The person approving the piece can paste every fix without asking a question, and nothing in a fix is a guess. A clean piece comes back Ready in four lines. A worked example (a Ferncliff LinkedIn post with an investor testimonial and a buried referral link) is in [assets/examples/ferncliff/](assets/examples/ferncliff/README.md).
