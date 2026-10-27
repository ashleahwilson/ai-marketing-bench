---
name: content-qa-gate
description: Runs the last check on a finished content piece before it's published, such as a blog post, landing page, newsletter or article, and returns a verdict (Publish, Fix first, or Hold) with every problem located and a concrete fix. Checks the piece against its brief, traces every statistic, price, quote and claim to brand memory or a cited source, and catches broken or placeholder links, missing CTAs, required disclosures, brand rules, search and accessibility basics (title, description, headings, alt text, link text), stale dates and leftover placeholders. Use when the user wants content checked, QA'd, proofed or approved before it goes live, for example "QA this post", "is this ready to publish", "final check before it goes out", "approve this page", "check this against the brief". Can apply the fixes to a copy on request. Not for rewriting copy for voice (use brand-voice-gate) or writing the piece.
license: MIT
compatibility: Recommended for large models. On small models it can occasionally guess (a suggested alt text or replacement claim), so check its suggested fixes. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Content QA gate

The last stop before publishing. It doesn't rewrite the piece. It decides whether the piece can go out, and if not, exactly what has to change first.

## Ground rules

1. **Every claim needs a source.** A statistic, result, price, ranking, superlative or customer quote must trace to brand memory (`brand/`), the brief, or a citation linked in the piece. If it doesn't, it's a blocker. Facts specific to the piece that the author would know (a client's comment, an event date) are the author's: don't block them.
2. **Never verify from memory.** Don't confirm a third-party statistic ("the ADA estimates…") because it sounds right. Ask for the source link.
3. **Never fill a gap with an invention.** No made-up URLs, statistics, alt text for an image you can't see, or replacement testimonials. Name what's needed and who has it.
4. **Don't invent problems.** A piece that meets its brief and the rules gets **Publish**. Style preferences are not defects. Report at most three optional nits.
5. **Pressure doesn't change the verdict, but it changes the help.** If the user is in a hurry, keep the verdict honest, keep the reply under 200 words, and lead with the fastest way to publish on time: usually deleting the blocking lines, then naming the confirmed facts that can stay. A softened superlative ("the most trusted") is still an unsupported claim, so don't suggest one. No lecture.
6. **Never edit the original.** Fixes go in a copy, and only when the user asks.
7. **The brief's and brand's domains are the real site, even reserved test names such as `.example`.** Don't flag a link because its domain looks unfamiliar or is a reserved name such as `.example`. Flag it when it's empty, `#`, a placeholder, or points somewhere other than the brief says.

## Workflow

```
- [ ] 1. Load: the piece, its brief, brand/, and whether brand-voice-gate already ran
- [ ] 2. Run scripts/qa_check.py
- [ ] 3. Judge: brief fit, claims, compliance, voice (references/checks.md)
- [ ] 4. Decide the verdict
- [ ] 5. Reply, and write <name>-qa.md
- [ ] 6. On request: apply fixes to <name>-qa-fixed.<ext>
```

### 1. Load

List the project folder. Find the brief: one the user names, or a file whose name matches the piece in `briefs/` or beside it (the format is in [references/brief-format.md](references/brief-format.md)). Read `brand/` (`offer.md`, `proof.md`, `claims.md`, `rules.md`, `voice.md`). If `<name>-gated.md` and `<name>-trace.md` exist, brand-voice-gate already checked the voice: don't redo it.

**No brief or no brand memory?** Run everything else, and say in the reply which checks couldn't run and why. Don't invent a brief or a target keyword and grade against it. Offer to check again once they exist.

### 2. Run the checker

```bash
python3 scripts/qa_check.py <piece> --brief <brief> --brand brand/ --channel <blog|landing|web|email|newsletter|social>
```

It lists each figure with the brand-memory line it matches, and it checks quotes for naming permission. It reports **BLOCKER** (placeholders, dead or `#` links, the brief's CTA URL missing, a phrase a brand rule forbids, an affiliate link with no disclosure), **FIX** (headings, alt text, vague link text, title and description length, repeated words, length against the brief, primary keyword, dates before publishing, never-use words) and **CLAIM** (every figure, superlative and quote, marked as found or not found in brand memory and the brief). The checker can't judge whether a claim is true: you check every CLAIM line in step 3.

### 3. Judge

Work through [references/checks.md](references/checks.md): brief fit, claims, compliance, voice, and the reader's path. These need judgment the script can't give: a price can appear in brand memory and still be wrong for this reader, and a quote can be recorded but not cleared to name.

### 4. Verdict

| Verdict | When |
|---|---|
| **Publish** | No blockers and no fixes, or only optional nits |
| **Fix first** | Fixes only: structure, search, accessibility, mechanics. Nothing false, missing or non-compliant |
| **Hold** | Any blocker: an unsupported or wrong claim, a compliance or brand-rule breach, a broken or placeholder link, a missing CTA, a brief miss on audience or goal |

### 5. Reply

```
**Verdict:** Publish | Fix first | Hold: <the one-line reason>

**Blockers** (Hold only)
1. <where: heading or quoted line> · <problem> · <fix>

**Fixes**
1. <where> · <problem> · <fix>

**Nits** (optional, at most 3)

**Checked and fine:** one line naming what passed (for example "brief must-includes, CTA link, prices, disclosures").
**Not checked:** only if something couldn't be (no brief, no brand memory, an image you can't see).
```

- Each problem gets its own line, located by heading or a short quote, with a fix the user can paste. A suggested title, description or heading uses only words and facts already on the page. For a missing image description, say what's needed ("add alt text describing what the image shows"), never a guessed description: you can't see the image. Where the fix needs something only they have (a source link, a URL, permission), say exactly what.
- For **Publish**, the reply is the verdict and the "Checked" line. Under 100 words.
- Never mention the checker, its output, its levels or rerunning it. Talk to the user in the second person.

Write the same content to `<name>-qa.md` beside the piece for whoever publishes it.

### 6. Fixing, when asked

If the request says "fix", "fix whatever you can", "apply the fixes" or "clean it up", you must write the fixed copy. A report alone doesn't answer it.

Apply only fixes that need no new facts: correct a figure to match brand memory, link the CTA to the brief's URL, rename vague link text, fix headings, repeated words, title and description length (built from the piece's own words). Write the result to `<name>-qa-fixed.<ext>`. Remove or keep (and list) anything that needs input: never invent a URL, a source, a statistic or alt text. Alt text needs someone who can see the image: list it as open, don't write a guess. The copy must have no dead or `#` links and must link the brief's CTA. Then rerun the checker on the copy and report what's fixed and what's still open.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The person publishing it can act on every line without asking a question. A clean piece comes back as Publish in three lines. Nothing in the verdict depends on a fact the QA gate guessed.

A worked example (a Tallyhouse blog post that comes back Hold) is in [assets/examples/tallyhouse/](assets/examples/tallyhouse/README.md).
