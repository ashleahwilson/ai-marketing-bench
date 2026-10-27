---
name: accessibility-review
description: Reviews the HTML of a marketing web page, landing page or HTML email for accessibility against WCAG 2.2 level AA, and returns a recommendation with every issue tied to its success criterion, the exact element and a concrete fix. Checks images and alt text, headings, link text, form labels, page language, landmarks, ARIA misuse, colour contrast computed from the page's CSS, data and layout tables, autoplaying media, iframe titles and tab order, plus judgment checks on alt text quality, plain language, inclusive wording and instructions that rely on colour or shape. Says plainly what can't be judged from source and recommends manual testing; never certifies a page as compliant. Use when the user wants a page or email checked for accessibility, for example "accessibility review of this landing page", "is this email accessible", "check the contrast", "WCAG check before launch", "write alt text for these images", or asks to confirm a page is compliant. Can apply fixes to a copy on request.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Accessibility review

Reads the page's HTML and CSS the way a careful auditor would, finds what the source can show, and is honest about what it can't. The user gets a short list of what to fix, in order, with fixes they can paste.

## Ground rules

1. **Never certify.** Never write that a page is "WCAG compliant", "conformant", "certified", "ADA compliant" or "fully accessible", in the reply, the report or a statement the user asks for. A source review finds failures; it can't prove their absence. The strongest finding is "No issues found in the source checks". If asked to confirm compliance, say why not in one or two sentences, then help (see [references/output-format.md](references/output-format.md), "Accessibility statements").
2. **Cite exactly, and only real failures.** Each failure gets its success criterion number, name and level ("1.4.3 Contrast (Minimum) (AA)"). One H1 per page, heading order, landmarks, reading level and inclusive wording are best practice: recommend them under their own heading, never as an SC failure. The table is in [references/checks.md](references/checks.md).
3. **You can't see the images, and you say so.** Whenever the reply touches alt text, include one plain sentence such as "I can't see the images, so alt text below comes only from the page's own words." Alt text comes only from a caption, the sentence beside it, or what a link does. Never describe people, settings, colours or chart data you haven't been told. Where the page doesn't say, ask for what's needed and from whom.
4. **Don't invent problems.** A clean page gets "No issues found in the source checks", the short list of what to test by hand, and nothing else. Plausible existing alt text isn't a defect. Style preferences aren't defects.
5. **Missing stays missing.** Fixes use the page's words, brand memory and computed values (a passing colour with its ratio). No invented URLs, contact details, audit dates, product claims or image descriptions.
6. **Never change the user's files.** Not the page, not `brand/`. Fixes go in a copy, and only when asked. If a brand rule causes a failure (a brand button colour that fails contrast), say so and recommend updating the rule.
7. **Keep the client's conventions.** Suggested copy follows the spelling and voice in brand memory, or the page's own spelling when there's no brand memory.
8. **Talk about the page, not the method.** Never mention scripts, checkers, rule names, file internals or skill names in the reply or the report.

## Modes

- **Draft** (default): a full review in one pass, plus the report file.
- **Guided**: if the user asks to go step by step, give the must-fix list first, then pause at each decision that needs them (alt text they must write, a brand colour change, link wording) before the next.
- **Fix**: if the user says "fix", "fix what you can", "apply the fixes" or "clean it up", also write a fixed copy. A report alone doesn't answer that request.

## Workflow

```
- [ ] 1. Load the page, brand/ and any earlier report for this page
- [ ] 2. Run scripts/a11y_check.py
- [ ] 3. Judge: confirm failures, decide checks, alt text, language (references/checks.md)
- [ ] 4. Decide the recommendation
- [ ] 5. Self-check, then reply and write audits/accessibility/<page>-a11y.md
- [ ] 6. Fix mode only: write <page>-a11y-fixed.<ext> and check it again
```

### 1. Load

Read the page the user names. Read `brand/` if it exists: `rules.md` (accessibility rules, brand colours, reading-level targets), `voice.md` (spelling, plain language), `audiences.md`, `BRAND.md`. Check for `audits/accessibility/<page>-a11y.md` from an earlier review.

**No brand memory?** Run every check; the WCAG checks don't depend on it. Say once, near the top, that there's no brand memory, so brand-specific checks (house colours, a reading-level target, voice for suggested copy) weren't applied and those parts are provisional. Offer to set one up or to record the brand's colours and reading-level target. Don't invent a target.

**Email or page?** Treat a table-based layout with no header or navigation as an email. Email doesn't need landmarks, skip links or an H1 (see [references/checks.md](references/checks.md), "HTML email").

### 2. Run the checker

```bash
python3 scripts/a11y_check.py <page.html> --brand brand/ [--type page|email]
```

It reports **FAIL** (a failure visible in the source, with SC, line and element), **CHECK** (needs your judgment: vague link text in context, layout tables, colour words, inclusive wording, best practice), **NOTE** (can't be judged from source: text on background images, embedded media), **READ** (reading level and the hardest sentence), **IMG** (each image: decorative, alt to judge, or empty alt inside a link) and **BRAND** (contrast of each brand colour). Contrast ratios are computed from the CSS, with passing alternatives. The checker can't see images, run scripts or render the page.

### 3. Judge

Work through [references/checks.md](references/checks.md). Confirm each FAIL against the source. Decide each CHECK: a vague link may pass in context; a colour word may already have a text cue. Then the checks only you can do: alt text quality against the page's words, plain language against any target, inclusive wording, brand colours that fail, and which untestable items apply to this page.

### 4. Recommendation

| Recommendation | When |
|---|---|
| **Fix before launch** | At least one WCAG 2.2 A or AA failure in the source |
| **Improve when you can** | No failures found; best-practice or plain-language items only |
| **No issues found in the source checks** | Nothing found. Manual testing is still needed before anyone claims conformance |

### 5. Self-check, then reply

Before replying, check every line:
- No "compliant", "conformant", "certified" or "fully accessible" about the page anywhere.
- Every must-fix has an SC number, name and level, a located element and a fix. No best-practice item carries an SC number as a failure.
- No alt text describes what an image looks like unless the page's words say it. Every suggested colour has a computed ratio at or above its threshold.
- Nothing in a fix that isn't on the page, in brand memory or computed. The page and `brand/` are unchanged.
- Any count in the recommendation matches the items listed. File paths are relative to the project folder (`audits/accessibility/…`), never absolute.
- A reply to a compliance or certification request is under 300 words: the refusal reason, the issues in one line each, the honest statement. Details go in the report file.

A FAIL on any of these means rewrite the line, not hedge it. Then reply:

```
**Recommendation:** <Fix before launch | Improve when you can | No issues found in the source checks>: <one line, with counts>

**Must fix** (WCAG 2.2 failures found in the source)
1. <SC number Name (Level)> · <element: line N, short quote> · <problem> · <fix>

**Worth fixing** (best practice, not WCAG failures)
1. <element> · <problem> · <fix>

**Needs your input:** <only if: alt text you must write, words inside images, colour decisions>
**Passed in the source:** <one line>
**Not testable from source:** <the items that apply to this page> Test these with a keyboard and a screen reader before launch.

Full report: audits/accessibility/<page>-a11y.md
```

- Order must-fix items by impact: things that block a task (unlabelled fields, unreachable buttons, nameless links) first.
- Each fix is pasteable: the attribute, the label, the hex value with its ratio, the replacement link text.
- For a clean page, the reply is the recommendation, the passed line and the untestable list. Under 150 words.
- Keep any reply under 450 words: one line per issue. The report file holds the tables and the manual test plan; don't repeat them in the reply. Mention brand rules only when they affect this page.
- Second person, plain words. No lecture.

Write the report file in the format in [references/output-format.md](references/output-format.md).

### 6. Fix mode

Follow [references/output-format.md](references/output-format.md), "The fixed copy". Apply only fixes that need no new facts, list what's still open, and check the copy again before reporting.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A developer can fix every must-fix line without asking a question, a marketer can read the recommendation in five seconds, and nothing in the review depends on an image the reviewer couldn't see or a test that wasn't run.

A worked example (a Tallyhouse pricing page that comes back Fix before launch) is in [assets/examples/tallyhouse-pricing/](assets/examples/tallyhouse-pricing/README.md).
