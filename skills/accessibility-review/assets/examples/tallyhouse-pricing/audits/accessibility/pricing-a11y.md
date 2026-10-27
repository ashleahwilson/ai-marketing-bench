# Accessibility review: pricing.html

Reviewed: 2026-10-24 · Standard: WCAG 2.2 level AA · Type: web page
Brand memory: used (BRAND.md, rules.md, voice.md, offer.md)

## Recommendation
Fix before launch: 4 WCAG failures in the source (a table, a contrast pair, a mouse-only chat button, an image), plus 1 best-practice fix.

## Must fix
| # | WCAG | Element | Problem | Fix |
|---|---|---|---|---|
| 1 | 2.1.1 Keyboard (A) | line 29, `<div class="chat">` "Questions? Chat with your bookkeeper" | Opens on click only; keyboard users can't reach or start the chat | Use `<button type="button" class="chat">Questions? Chat with your bookkeeper</button>` |
| 2 | 1.3.1 Info and Relationships (A) | line 21, the plan and price `<table>` | Data table with no header cells, so screen readers don't announce "Plan" and "Price" with each row | Make the first row `<tr><th scope="col">Plan</th><th scope="col">Price</th></tr>` |
| 3 | 1.4.3 Contrast (Minimum) (AA) | line 28, `<p class="was">` "Prices effective October 10, 2026." | #b0b0b0 on white is 2.17:1; needs 4.5:1 | Text colour #757575 (4.58:1) |
| 4 | 1.1.1 Non-text Content (A) | line 27, `<img src="pricing-badge.png" alt="badge">` | "badge" says what kind of image it is, not what it says | Needs your input (below) |

## Worth fixing (best practice, not WCAG failures)
| # | Element | Problem | Fix |
|---|---|---|---|
| 1 | line 30, link "here" to /review | Passes in context (the sentence names the review), but "here" is unclear out of context in a screen reader's link list | "Not sure which plan fits? `<a href="/review">Start with a free month-end review</a>`." |

## Needs your input
- pricing-badge.png: what the badge says. If it has words on it, the alt text should be those words; if it's decoration, use `alt=""`.

## Passed in the source
Page language (en-CA), title, one H1, main landmark and navigation label, logo link alt text, 3 of 4 text colour pairs, 5 links with names.

## Not testable from source
- Chat widget: whether it opens, traps focus or announces itself once fixed (test with a keyboard and a screen reader)
- Whether the badge image contains text
- Zoom to 200% and reflow on a phone-width screen (the price table may overflow)

## Manual test plan
1. Keyboard only: tab from the top through the navigation, the price table, the chat button and the review link. Check every stop has a visible focus outline and Enter opens the chat.
2. Screen reader (VoiceOver or NVDA): read the price table row by row and confirm "Plan" and "Price" are announced with each cell.
3. Zoom to 200% and narrow the window to 320px: confirm the table and prices stay readable without sideways scrolling.

Note on brand memory: brand teal #3FA7A3 with white text (rules.md) measures 2.89:1 and would fail 1.4.3 wherever it's used for button text. It isn't used on this page. Consider updating the rule to #31827f (4.54:1 with white).
