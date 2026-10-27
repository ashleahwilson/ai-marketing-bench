# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables. Integration change, not re-run.

## 1.2.0 (2026-10-26)
Round 2 (Haiku 71/72): Haiku excused "plans marked with a green badge" because the badge also has text, drafted screenshot alt text from a nearby feature paragraph, and wrote replies over 500 words.
- A sentence that tells people to find something by colour fails 1.4.1 even when the item has a text label.
- A nearby paragraph about a feature isn't a description of a screenshot or photo.
- Replies stay under 450 words; the tables and test plan live only in the report file; brand rules come up only when they affect the page.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 70/72, Opus 72/72; no skill: Haiku 57, Opus 62): Haiku ran a certification reply to 454 words and didn't say it couldn't see the images; one reply's count didn't match its list, and some replies gave absolute file paths.
- The reply says outright that the images can't be seen whenever it covers alt text.
- A compliance or certification reply stays under 300 words, with details in the report file.
- Self-check: counts match the list; paths are relative to the project folder.

## 1.0.0 (2026-10-24)
- First release:
  - Reviews a web page, landing page or HTML email against WCAG 2.2 AA, with a fixed reply (recommendation first; must fix, worth fixing, needs your input, passed, not testable from source) and a report at `audits/accessibility/<page>-a11y.md`.
  - `a11y_check.py`: page language, title, alt text (missing, placeholder words, file names, empty alt inside links), headings, link names and vague or repeated link text, button names, form labels and broken label or ARIA references, invalid roles, `aria-hidden` on focusable content, keyboard-unreachable widgets, positive tabindex, landmarks, data versus layout tables, autoplay, iframe titles, zoom-blocking viewports, removed focus outlines, colour contrast computed from the CSS with passing alternatives, colour and position words, inclusive-language candidates, reading level, and the contrast of brand colours.
  - Never certifies a page as compliant; separates WCAG failures from best practice; never describes an image it can't see.
  - Fix mode writes `<page>-a11y-fixed.<ext>` with fixes that need no new facts.
