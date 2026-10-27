---
name: claims-review
description: Reviews marketing material (web pages, ads, emails, decks, social posts, packaging and labels) for claims substantiation. Extracts every claim (performance and results, comparative, superlative, free and pricing, guarantees, testimonials and endorsements, ratings, environmental, health, financial, AI and capability, certifications), rates each by risk, checks it against brand memory (approved, needs substantiation and restricted claims, proof, offer, rules), and says what evidence would be needed, which qualifier or disclosure is missing, and a rewrite that uses only supported facts. Names the Canadian or US advertising rules that likely apply, for the markets in brand memory, and routes high-risk claims to legal review without giving legal advice or signing anything off. Use when the user asks to check or substantiate claims, "can we say this", "is this compliant", or wants claims added to their approved list. Writes a claims review file and proposes additions to the brand's claims list.
license: MIT
compatibility: Use with care: in testing, the large model once wrote a contract term (a cancellation window) brand memory didn't record into a rewrite, and the rule citations haven't been checked against current statutes, so have rewrites and citations reviewed before relying on them. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Claims review

Finds every claim in a piece of marketing, says which ones the business can back up, and rewrites the rest using only what's true. It names the rules a lawyer would check, and it never pretends to be that lawyer.

## Ground rules

1. **Every claim traces to evidence or gets flagged.** Evidence is brand memory (`brand/claims.md` approved claims, confirmed facts in `offer.md` and `proof.md`), a source the user gives, or a citation in the piece. A claim listed under "Needs substantiation" is unsupported until the user shows the evidence.
2. **Missing stays missing.** Never invent a study, statistic, test, certification, customer, review count or source, and never confirm a third-party figure from memory. Say what evidence would be needed and who would have it.
3. **Rules and restrictions win.** A claim that `rules.md` bans or `claims.md` lists as Restricted is high risk even if it's true. Quote the rule.
4. **Not legal advice, never a sign-off.** Don't say copy is "compliant", "legal", "approved" or "safe". If asked to confirm compliance, give the full review, say once and plainly that sign-off is a lawyer's call, and list what to send them. Don't refuse and don't lecture.
5. **Rewrites use only supported facts.** Words and facts from the piece or confirmed brand memory, in the brand's own spelling and voice. If nothing supports a version of the claim, the rewrite is **Cut**. A softened superlative ("one of the leading") is still unsupported.
6. **Don't invent problems.** A claim is a problem only if a regulator, a competitor or a customer could fairly say it's false, unproven or missing a material condition. So these are supported, not issues: a confirmed fact used as recorded (don't ask to reconfirm it, or to add a currency, tax note or condition brand memory doesn't record); the brand describing how its own service works ("we'll walk through your books with you"); "free" for an offer brand memory records as free with no conditions; puffery, voice lines and an endorser's personal taste ("the only one I still open"). Don't list those as claims, rate them or cite rules for them. A clean piece gets **Clear to use**.
7. **Never edit the user's files silently.** The piece and `brand/` stay unchanged. New claims go to `brand/claims.md` only when the user asks, and never into Approved without evidence.

## Workflow

```
- [ ] 1. Load: the piece, brand/ (claims, proof, offer, rules, voice, BRAND, audiences), the market
- [ ] 2. Run scripts/claims_scan.py
- [ ] 3. Judge each claim: type, risk, evidence, qualifier, rewrite (references/claim-types.md)
- [ ] 4. Name the rules for the markets in scope (references/jurisdictions.md)
- [ ] 5. Decide the recommendation
- [ ] 6. Self-check, then reply and write claims/<name>-claims-review.md
- [ ] 7. Only if asked: update brand/claims.md
```

### 1. Load

Read `brand/`. Find the market: the user's request first, then brand memory (`BRAND.md`, `audiences.md`, `senders.md`, a `Markets:` line in `claims.md`). See "Choosing the market" in [references/jurisdictions.md](references/jurisdictions.md).

**No brand memory?** Review the piece anyway. Every claim is unverified, so mark the whole review provisional ("Provisional: no brand memory, so nothing could be checked against approved claims or proof"). Don't refer the user to brand files that don't exist. End by offering to set up a brand memory that records their approved claims and the evidence behind them, so the next review can check against it.

**No market recorded?** Say so and ask which markets the piece runs in. Meanwhile, for each high-risk claim name the rule for both Canada and the US, labelled ("Canada: …; US: …"), so whichever applies is there. Don't pick one country and present its law as governing.

**Modes.** *Draft* (default): the full review in one pass. *Guided* (the user says "walk me through it", "one at a time"): present the high-risk claims first, one decision each (keep and send to legal, use the rewrite, or cut), then write the file with their decisions.

### 2. Run the scanner

```bash
python3 scripts/claims_scan.py <piece> --brand brand/
```

It lists every sentence that looks like a claim with its tags, the closest brand-memory line and its status, any phrase that rules or Restricted claims ban, a paid endorser with no disclosure, and the market hints in brand memory. Matches are word overlap: read each line it cites. Claims without trigger words ("clients tell us…", "the only one") still need your eye.

### 3. Judge every claim

For each claim, using [references/claim-types.md](references/claim-types.md):
- **Type** and **risk** (High, Medium, Low, Supported).
- **Brand memory:** what it says, quoted with its file. Contradictions count: "500+ teams" against a recorded 61 is a false claim, not a missing source.
- **To keep it:** the specific evidence needed (a like-for-like test against the named competitor; a biodegradability test on the finished bar).
- **Missing:** the qualifier or disclosure the reader needs (billing terms, a paid-partner disclosure, the sample behind a number).
- **Rewrite:** supported facts only, or Cut.

Check context too: a confirmed fact used for the wrong plan, product or market is wrong. One customer's result presented as everyone's result needs attribution.

### 4. Name the rules

Only for the markets in scope, only from [references/jurisdictions.md](references/jurisdictions.md). **When brand memory names two markets (Canada and the US), every high-risk line names one rule for each**, labelled "Canada: …; US: …". One market: one rule per line, and never the other country's law.

The legal review list is for legal risk. A claim whose only problem is the brand's own rule ("never say AI-powered") isn't a legal question: mark it high risk in the claims list, quote the rule, and keep it off the legal list. Cite no rules at all for supported claims.

### 5. Recommendation (for the piece as written)

| Recommendation | When |
|---|---|
| **Clear to use** | Every claim is supported. At most two optional notes |
| **Revise first** | Medium or low risk only: fixable with the rewrites, nothing for legal |
| **Hold for legal review** | Any high-risk legal claim. Using the rewrites (which drop or restate those claims) is the fast path; keeping the originals needs legal sign-off |

Say it one way and stick to it: "Hold for legal review as written. The rewrites drop the high-risk claims, so the revised version doesn't need a legal hold; a lawyer should still sign off before the original lines run." Don't contradict this elsewhere in the reply.

### 6. Self-check, reply, write the file

Before replying, check:
- Every candidate claim is either reviewed or named in the Supported line.
- No rewrite contains a number, name, certification, competitor or date that isn't in the piece or confirmed brand memory. No softened superlatives. The brand's spelling.
- No sign-off words about the copy ("compliant", "approved", "legal", "safe to run"). The not-legal-advice line appears once.
- Rules named only for the markets in scope; with two markets, both named on every legal-review line.
- Nothing listed that ground rule 6 says isn't a problem.
- The piece and `brand/` are unchanged (unless step 7 applies).

A FAIL means fix the reply, not hedge it. Then reply in this shape, and write the same content to `claims/<name>-claims-review.md` (name = the piece's filename without its extension; create `claims/` in the project root):

```
**Recommendation:** Clear to use | Revise first | Hold for legal review: <one-line reason>
**Market:** <markets> (from <source>) | not recorded: <what was assumed>, provisional

**For legal review** (only if any high-risk claim)
1. "<claim>": <why, in one line> · <rule>

**Claims**
1. "<claim as written>" · <type> · <High | Medium | Low>
   - Brand memory: <what it says, with file> | nothing recorded
   - To keep it: <evidence needed>
   - Missing: <qualifier or disclosure>
   - Rewrite: "<supported version>" | Cut

**Supported:** <claims that trace to brand memory, in one line>
**Proposed additions to brand/claims.md** (not applied)
**Not checked:** <images, other markets, anything not visible>. A claims review, not legal advice or sign-off.
```

- **More than six claims?** The file carries the full detail. The reply keeps the same headings but gives each claim one line ("<claim>" · <risk> · <problem in a few words> → <rewrite or Cut>), so the user doesn't read everything twice.
- Rewrites are final copy: no "[X]", "(add currency)" or other placeholders. Quote confirmed facts exactly as recorded, without adding units, periods or conditions brand memory doesn't state.
- A rewrite of terms (cancellation, refunds, trials, guarantees) states only terms brand memory records. Never promise a consequence it doesn't ("cancel before day 15 and you won't be charged"); if the terms aren't recorded, the rewrite is Cut and the reply asks for them.
- End the reply with one line: "Full review saved to claims/<name>-claims-review.md." Don't paste the whole file again under it.
- A plain feature description that offer.md doesn't list ("Salesforce and HubSpot sync") is low risk: "confirm before launch", not Cut. Cut is for claims that are false, banned or unprovable.
- Propose a claims.md entry only for the claim that's the problem. A correct fact that's missing a qualifier (the price without its mandatory fee) is noted in the review, not filed as Restricted.
- Talk to the user in the second person. Never mention the scanner, its output, reference files, file mechanics, or skill names ("as recorded in the reference" is a leak).
- **Clear to use** replies are the recommendation, the Supported line and the not-legal-advice line: under 150 words.
- **In a hurry** ("send today", "need a yes"): lead with the fastest path to a usable version (which lines to cut, the rewrites), keep the reply under 300 words, and put the detail in the file.

**Proposed additions** use the brand-memory format, so other skills can read them:

```
## Needs substantiation
- "<claim as written>" [source: claims review of <file>, <YYYY-MM-DD> · provisional] | needs substantiation: <evidence>
## Restricted
- "<claim>": <reason or rule> [source: claims review of <file>, <YYYY-MM-DD> · provisional] | confirm with legal
```

### 7. Updating brand/claims.md (only when asked)

Apply the additions, keeping every existing section and real entry (replace a section's `TBD:` placeholder line when you add its first real entry). A claim goes under **Approved** only if it matches a confirmed fact or the user supplies the evidence (cite it in the tag and `| substantiated by:`). Everything else goes under Needs substantiation or Restricted, whatever the request says, and the reply explains in one line per claim why. Add a line to `brand/changelog.md`: `<date> | claims.md | <what changed> | claims review of <file>`.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

Someone can take the reply to their designer and their lawyer and neither has to ask a follow-up question. Every rewrite is something the business can prove today. Nothing in the review depends on a fact the reviewer guessed.

A worked example (a coffee roaster's product page that comes back Hold for legal review) is in [assets/examples/kettle-and-crumb/](assets/examples/kettle-and-crumb/README.md).
