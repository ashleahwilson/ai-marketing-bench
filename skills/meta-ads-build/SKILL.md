---
name: meta-ads-build
description: Builds a Meta (Facebook and Instagram) ad campaign ready to load, or rebuilds one from a Meta ads audit's fixes list, or checks and fixes existing ad drafts. Sets the objective and optimization event, campaign and ad set structure with budget reasoning, audiences (broad or Advantage+, custom audiences only from consented first-party lists, lookalikes), placements, and several creative concepts, each with a hook, primary text, headline, description, CTA button and an image or video brief. Builds compliance in, including special ad categories (employment, housing, credit, social issues) and their targeting limits, and Meta's personal-attributes rule. Proof comes only from brand memory; it never invents testimonials or UGC. Use when the user wants Facebook or Instagram ads, a Meta campaign, ad copy for Meta, a recruiting or hiring ad on Meta, a rebuild after an audit, or drafts checked before loading. Writes the build and a bulk-upload CSV. Not for Google or LinkedIn ads.
license: MIT
compatibility: Tested on large and small models. On large models it occasionally adds small unsourced details (what a demo involves, an assumed retargeting audience), so check feature and audience lines. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Meta ads build

Builds the campaign someone can load into Ads Manager without a follow-up question: the settings, the reasons, the ads and the creative brief. Every claim in every ad is true, and the ads pass Meta's review the first time.

## Ground rules

1. **Every fact has a source.** Figures, prices, names, quotes, results, offer details, dates and features come from the user, the brief, the audit or `brand/`. Missing stays missing: a marked placeholder (`[link: landing page]`) listed under OPEN. A plausible guess is still an invention, and that includes a cost per lead, a trial length or a benefit the job posting doesn't mention.
2. **No invented proof.** No made-up customers, quotes, results or "UGC" where a creator plays a customer, even when asked. Proof whose naming permission is `unconfirmed` or `no` stays out of the ads, quote included. Brand rules and unsubstantiated claims in `claims.md` stay out even when the brief asks for them.
3. **Compliance is built in, not flagged afterwards.** Personal attributes, special ad categories and audience consent follow [references/policy.md](references/policy.md). If the request breaks one, build the compliant version and say what changed in a sentence or two.
4. **Push back without refusing or lecturing.** Do the sound part, change the unsound part, give the honest alternative, and still deliver usable ads.
5. **Nothing goes live.** Never load, publish or spend. Never edit the user's drafts, briefs or audit files: write new files.

## Modes

- **Draft** (default): the full build, written to files.
- **Guided** (the user asks to be walked through it or to decide step by step): give the recommended shape (objective, event, structure, audience approach, offer), then ask at most five questions in total, one per numbered item, no sub-questions. Write no ad copy, and no build file, until they answer.
- **Rebuild** (an audit fixes list exists in `audits/meta-ads/<account>/`, or the user asks to rebuild from an audit): the full build, with every fix mapped to a change.
- **Check and fix** (the user gives drafts): keep their ads and concepts, fix each one in place in `<file>-fixed.md`, and report each problem fixed and what's still open.

## Workflow

```
- [ ] 1. Load: request, brief, brand/, audit fixes, drafts, audience notes
- [ ] 2. Ledger: FACTS and OPEN
- [ ] 3. Compliance first: category, personal attributes, audience consent, proof
- [ ] 4. Decide: objective, event, structure, budget, audiences, placements
- [ ] 5. Write: concepts and creative briefs into the build file
- [ ] 6. Check: script, then the judgment checks
- [ ] 7. Reply in the fixed shape
```

### 1. Load

List the project folder. Read the brief or request, `brand/` (`BRAND.md`, `offer.md`, `audiences.md`, `proof.md`, `results.md`, `claims.md`, `rules.md`, `voice.md`), any `audits/meta-ads/<account>/fixes.md`, and any audience or drafts files the user points to. Use `confirmed` facts as fact, flag `provisional` ones, never state `assumed` ones. A brand file that doesn't exist means nothing is on record for it (no proof file: no proof). Brand memory that exists but is marked provisional still counts: set the build to `Status: draft` and flag the provisional facts you use. Follow the brand's spelling and voice in the ads, even when it differs from yours.

**No `brand/`?** Build from the conversation, mark the build `Status: provisional`, use placeholders for every URL and fact you weren't given, and say in the reply, in one line, that there's no brand memory so the build is provisional, then offer to set it up. Keep the client's own conventions (spelling, currency) as given.

### 2. Ledger

List every fact the ads may use with its source, and every gap, at the top of the build file ([references/build-file.md](references/build-file.md)).

### 3. Compliance first

Before any copy, work through [references/policy.md](references/policy.md):
- Does the ad offer jobs, housing, credit or financial products, or touch social issues or politics? Declare the category and apply its targeting limits.
- Does any requested hook or targeting assert or imply the reader's finances, health, age, identity or beliefs? Replace it.
- Does every custom audience have a consent basis? Leave out bought, rented, scraped and other people's lists.
- Is every piece of proof on record, with permission to name?

### 4. Decide

Follow [references/campaign.md](references/campaign.md): objective and optimization event (a conversion that already fires, never link clicks when one does), one campaign and as few ad sets as the budget can feed, with the learning-phase reasoning; broad or Advantage+ audience first; Advantage+ placements with 1:1 or 4:5 and 9:16 assets. Never state a cost per result, lead count or return as fact: give the formula and label any number you use as an assumption.

### 5. Write

Three to five distinct concepts (in Rebuild mode, enough to replace the ads the audit names). Every concept has a 9:16 version for Stories and Reels plus a 1:1 or 4:5 version for feeds. Each gets a hook, primary text with the hook and the offer in the first 125 characters, a headline of 40 characters or fewer, a description of 30 or fewer, a Meta CTA button, the URL, and a creative brief: format, aspect ratios and what's on screen. Save everything to `ads/meta/<campaign-slug>/build.md` in the format in [references/build-file.md](references/build-file.md). If you revise, overwrite your own file.

### 6. Check

```bash
python3 scripts/check_build.py ads/meta/<campaign-slug>/build.md --brand brand/ --csv ads/meta/<campaign-slug>/ads.csv
```

Fix every FAIL and rerun until none is left: a FAIL means rewrite, not hedge. Judge every WARN. OPEN items need a fact only the user has: list them. Then the judgment checks:
- Could any line be read as telling the reader what they are or what they're going through?
- Does every figure, name and quote trace to FACTS? Is anything a guess dressed as a fact?
- Is the objective's event real and tested, and can the budget feed every ad set?
- Are the concepts different reasons to act, in the brand's voice, matching the landing page? Does every one have a 9:16 version?
- Is every price stated with its conditions as on record ("$49/user/month, billed annually")? Does a creative brief use another company's logo or name without permission on record? Say "logo use needs permission" or leave it out.
- Does any line claim something about the product or the people in the ad that isn't in FACTS, or broaden a fact ("your POS" when the record names three systems): a feature, a differentiator ("built for X, not adapted"), a call length, a creator's or actor's experience with the product? Cut it.
- In Rebuild mode, is every fix number addressed? In Check and fix mode, is every original ad still there, and is the user's file untouched?

### 7. Reply

```
**Recommendation:** <one line: objective and event, structure, budget, audience approach> (Guided: the recommended shape)

**Set-up**
| Level | Setting | Why |   (campaign, ad set(s): category, objective, event, budget, audience, exclusions, placements)

**Ads**
| # | Concept | Hook | Headline | CTA |
(Full copy and creative briefs in ads/meta/<slug>/build.md, upload file ads.csv. Paste the full copy here too if there are 3 ads or fewer, or the user asked.)

**Changed from your request:** one line each for anything left out or changed (a hook, targeting, a claim, a list, proof), with the honest alternative. Only if something changed.

**Before launch:** at most 5 items, OPEN items first (event to confirm, URL, proof to clear, assets to shoot).
```

- Lead with the recommendation. Keep the reply under about 400 words, not counting the tables and any pasted ads. Paste full copy only for 3 ads or fewer; otherwise the table and the file path are enough. Give file paths relative to the project folder, never absolute. Rebuild mode adds a **Fixes** table (`F# | change`). Check and fix mode replaces **Ads** with **Fixed** (`ad | problem | fix`).
- Guided mode: the recommendation, a short plan table, then the numbered questions. Nothing else.
- Talk to the user in the second person. Never mention this skill, the checker or its results ("0 FAIL", "the build check passes"), the ledger format, or other skills by name; say what's missing in plain words ("Maria's OK to use her quote isn't on record").

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A media buyer can load the CSV, attach the creative and launch without asking a question. The ads pass review the first time because nothing in them asserts who the reader is, every targeting choice is allowed for the category, and every claim is on record. Nothing depends on a number the build guessed.

A worked example (a physiotherapy clinic campaign where the requested hook implied a health condition) is in [assets/examples/harbourline-physio/](assets/examples/harbourline-physio/README.md).
