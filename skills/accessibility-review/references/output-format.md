# Report file, fixed copy and accessibility statements

## Contents
- The report file
- The fixed copy
- Accessibility statements

## The report file

Write it to `audits/accessibility/<page>-a11y.md`, where `<page>` is the file name without its extension (`review-landing.html` → `audits/accessibility/review-landing-a11y.md`). Create the folders if they don't exist. If a report for the page already exists, overwrite only that report, and say what changed since it in one line.

Other work (a final content check, a developer ticket, a client hand-over) links to this file, so keep the headings exactly as below.

```markdown
# Accessibility review: <page file>

Reviewed: <YYYY-MM-DD> · Standard: WCAG 2.2 level AA · Type: web page | HTML email
Brand memory: used (<files read>) | none found (brand-specific checks provisional)

## Recommendation
<Fix before launch | Improve when you can | No issues found in the source checks>: <one line>

## Must fix
| # | WCAG | Element | Problem | Fix |
|---|---|---|---|---|
| 1 | 1.4.3 Contrast (Minimum) (AA) | line 45, `<button class="btn">` "Book my free review" | White on #3FA7A3 is 2.89:1; needs 4.5:1 | Background #31827f (4.54:1) |

## Worth fixing (best practice, not WCAG failures)
| # | Element | Problem | Fix |

## Needs your input
- <what's needed, from whom> (for example: alt text for hero.jpg: what the photo shows)

## Passed in the source
<one line>

## Not testable from source
- <item>: <how to test it>

## Manual test plan
1. Keyboard only: <the paths on this page to tab through>
2. Screen reader: <what to listen for on this page>
3. <other items that apply>
```

Rules for the file:
- The same findings as the reply, in the same order. No extra issues that the reply leaves out.
- Every Must fix row has the SC number, name and level, a located element (line number and a short quote), the problem and a pasteable fix.
- Never write "compliant", "conformant", "certified" or "fully accessible" about the page. "No issues found in the source checks" is the strongest finding.
- No mention of how the checks were run (tools, scripts, rule names).

## The fixed copy

Only when the user asks for fixes ("fix it", "fix what you can", "apply the fixes", "clean it up"). A report alone doesn't answer that request.

Write `<page>-a11y-fixed.<ext>` beside the original. Never change the original or `brand/`.

Apply fixes that need no new facts:
- `lang` on `<html>` (the page's language; `en` when the copy is English and nothing says which variety)
- Remove positive `tabindex`; restore a visible focus style (delete `outline: none` rules, or add `outline: 2px solid` in a passing colour)
- `alt=""` on decorative images; alt text for logo links and image-only links from their destination and the page's words
- Labels from a field's own placeholder or nearby words; fix `for`/`id` mismatches; remove broken `aria-labelledby`
- Titles for iframes from the heading or sentence that introduces them
- Descriptive link text from the page's words; real `<button>` elements for `role="button"` divs; remove invalid roles and `aria-hidden` on focusable content
- `role="presentation"` on email layout tables; `<th scope="col">` on a data table's header row
- Passing colours: the computed value nearest the original, with its ratio
- Remove `autoplay` (or add `muted` and `controls`)

Leave and list anything that needs input: alt text for photos, screenshots and charts you can't see; words inside images; captions; brand colour decisions the user may want to make themselves. Don't put a placeholder alt such as "TODO" in the copy: leave the attribute as it was and list it.

Then check the copy again the same way as the original, and report what's fixed and what's still open.

## Accessibility statements

When asked to confirm, certify or state that a page is compliant, say in one or two sentences why you can't: a source review finds problems, but conformance can only be established by testing the live page with a keyboard and assistive technology, ideally in an expert audit. Then help. Report what you found, and offer a statement that's true today:

```
We want everyone to be able to use this site, and we're working to meet WCAG 2.2 level AA. If something on the site doesn't work for you, tell us at <contact from the page or brand memory> and we'll help and fix it.
```

- The contact comes from the page or brand memory. If neither has one, write `TBD: contact email` and say so.
- Never add an audit date, an auditor, a certification, a conformance level achieved or a list of tested assistive technologies unless the user supplied them.
- Under 300 words for the whole reply; put the full findings in the report file. No lecture about legal risk: one line that a conformance claim should follow an audit is enough.
