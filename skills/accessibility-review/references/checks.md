# Judgment checks

## Contents
- Failure or best practice
- Success criteria this review uses
- Images and alt text
- Links, buttons and forms
- Colour, contrast and sensory instructions
- Plain language and inclusive language
- HTML email
- What the source can't show

## Failure or best practice

Only call something a WCAG failure when a success criterion clearly fails. Label everything else as best practice, and never attach an SC number to it as if it failed.

| Best practice, not a WCAG 2.2 failure | Why |
|---|---|
| One H1 per page; no skipped heading levels | WCAG doesn't require either. Recommend them, plainly labelled |
| A `<main>` landmark or skip link | 2.4.1 can be met by headings; recommend `<main>` |
| Inclusive wording, reading level | Not in WCAG AA. Real barriers for readers, so still worth fixing |
| Duplicate ids | 4.1.1 Parsing was removed in WCAG 2.2. Only matters when a label or ARIA reference points at the duplicate |
| `target="_blank"` without a warning | Advisory only |

A vague link such as "Read more" fails 2.4.4 only when the surrounding sentence doesn't make the destination clear. Say which it is. Either way, give descriptive text.

## Success criteria this review uses

| SC | Name (level) | Typical source evidence |
|---|---|---|
| 1.1.1 | Non-text Content (A) | `<img>` with no alt, a placeholder alt, or an image-only link with `alt=""` |
| 1.2.2 | Captions (Prerecorded) (A) | Video with no captions track (confirm on the video) |
| 1.3.1 | Info and Relationships (A) | Data table with no `<th>`, label not tied to its field, layout table read as data |
| 1.3.3 | Sensory Characteristics (A) | "the button on the right", "the round icon" |
| 1.3.5 | Identify Input Purpose (AA) | Email, name or phone field with no `autocomplete` |
| 1.4.1 | Use of Color (A) | "fields in red are required", "items in green are included" |
| 1.4.2 | Audio Control (A) | `autoplay` without `muted` |
| 1.4.3 | Contrast (Minimum) (AA) | Text below 4.5:1, or large text below 3:1 |
| 1.4.4 | Resize Text (AA) | Viewport with `user-scalable=no` or `maximum-scale` below 2 |
| 1.4.5 | Images of Text (AA) | Can't be confirmed without seeing the image |
| 2.1.1 | Keyboard (A) | `role="button"` or `onclick` on a `div`/`span` with no tabindex |
| 2.2.2 | Pause, Stop, Hide (A) | Autoplaying or looping video with no controls |
| 2.4.2 | Page Titled (A) | No `<title>` (web pages) |
| 2.4.3 | Focus Order (A) | `tabindex` above 0 |
| 2.4.4 | Link Purpose (In Context) (A) | Link with no name; vague text with no context |
| 2.4.6 | Headings and Labels (AA) | Empty or misleading headings and labels |
| 2.4.7 | Focus Visible (AA) | `:focus { outline: none }` with no replacement |
| 3.1.1 | Language of Page (A) | No or invalid `lang` on `<html>` |
| 3.3.2 | Labels or Instructions (A) | Field with only a placeholder; required fields shown by colour only |
| 4.1.2 | Name, Role, Value (A) | Unlabelled fields, icon-only buttons, untitled iframes, invalid roles, `aria-hidden` on focusable content, broken `aria-labelledby` |

Large text is at least 24px, or at least 18.66px (14pt) and bold.

## Images and alt text

You can't see any image. Decide each one from the page's own words:

| The page tells you | Do this |
|---|---|
| The image is the only content of a link or button | Alt text says where the link goes or what the button does, from its destination and nearby words ("Tallyhouse home" for a logo linking to `/`). If the image is a graphic with words on it, ask for those words |
| A caption or adjacent text already says what's in it | `alt=""` (the caption carries it) or the caption's own words. No appearance details |
| It's decoration (divider, spacer, background flourish) | `alt=""` |
| Nothing: a photo, screenshot or chart with no description (a paragraph about the feature nearby doesn't count: it says what the product does, not what the picture shows) | Say what's needed and who has it: "add alt text that says what the photo shows" or, for a chart, "the figures or the main finding it shows". Never guess at people, settings, colours or data |

Existing alt text that reads plausibly ("Seamless Sync settings screen") can't be confirmed against the picture. Leave it alone, and list "alt text matches the images" under what the source can't show. Flag alt text only when the source shows the problem: a placeholder word ("image", "photo", "chart", "Screenshot"), a file name, or `alt=""` on an image that is the only content of a link.

A banner or button image may contain words. Text in an image must also be in the alt text (1.1.1), and images of text should be real text where possible (1.4.5). You can't tell from source, so ask.

## Links, buttons and forms

- Replacement link text uses words already on the page or the destination's own name from the page ("See catch-up pricing" for `/catch-up/pricing` beside a sentence about pricing).
- An icon-only button needs an accessible name. Name it from what it does in the page (a close button on a banner: `aria-label="Close banner"`).
- A field's label can reuse its placeholder's words as a visible `<label>`. Fix a `for` that doesn't match by changing either side so they match.
- Required fields: add the word "required" or an asterisk explained in text, not colour alone.
- `aria-hidden="true"` on anything containing a link, button or field: remove it, or make the content truly hidden.

## Colour, contrast and sensory instructions

- Report the computed ratio to two decimals and the threshold. 4.48:1 fails 4.5:1. Don't round up, and don't call a near miss "basically fine".
- Give a passing colour as a hex value with its ratio, keeping the design's direction (darken the text, or darken a button's background behind white text).
- **Brand colours.** If a failing colour comes from brand memory (a rule such as "buttons use teal #3FA7A3 with white text"), say so, give the nearest passing version, and recommend the brand rule be updated. Don't edit `brand/` yourself.
- Text over a background image or gradient can't be measured from source. Say so and ask for it to be checked on the rendered page. Never estimate a ratio for it.
- Instructions that rely on colour, shape or position ("in green", "the round button", "on the right") need a text cue too. Suggest wording that adds it. If the sentence tells people to find something by its colour ("plans marked with a green badge"), it fails 1.4.1 even when the item also carries a text label: the instruction itself still points at colour. Fix the sentence to name the label ("plans marked Most popular").

## Plain language and inclusive language

- Reading level: if brand memory sets a target, compare against it; if not, mention a hard sentence only when it would stop a reader. Rewrites use only facts already on the page. If the page has a plainer sentence that says the same thing, point to it.
- Inclusive wording: flag phrases that use age, disability or mental-health terms as jokes or shorthand ("even your grandma could", "a little OCD", "crazy fast"). Offer a replacement built from the page's own claim. These are best-practice fixes, not WCAG failures.
- Don't flag ordinary words that only resemble these.

## HTML email

- Required: `lang` on `<html>`, alt text on every image (`alt=""` for spacers), `role="presentation"` on layout tables, real header cells on data tables, contrast, descriptive links, no colour-only instructions.
- Not expected in email: `<main>` or other landmarks, skip links, a single H1. A `<title>` is good practice, not 2.4.2.
- Image-only buttons are common in email: the link's name comes from the alt text, so `alt=""` there means a nameless link.

## What the source can't show

Pick the items that apply to this page, so the list isn't boilerplate:

- Keyboard-only use: tab order, focus visibility on the rendered page, traps in menus or pop-ups
- Screen reader output (NVDA, JAWS, VoiceOver): reading order, announcements, form errors
- Zoom to 200% and reflow at 320px wide (1.4.4, 1.4.10)
- Contrast of text on images or gradients, and of focus indicators and borders (1.4.11)
- Whether alt text matches the images, and whether images contain text
- Video and audio: caption and transcript content and accuracy
- Embedded content (iframes, third-party widgets)
- Rendering in email clients, including dark mode and images turned off
- Linked PDFs: tagging and reading order
- Behaviour driven by scripts: error messages, timeouts, dynamic content

Recommend testing these with a keyboard and at least one screen reader, and, before any public conformance claim, an expert audit that includes people who use assistive technology.
