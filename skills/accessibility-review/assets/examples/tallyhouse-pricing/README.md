# Worked example: Tallyhouse pricing page

Fictional company. No real results are claimed.

**Request:** "Accessibility check on site/pricing.html before we update the live page. Brand memory is in brand/."

**Inputs:** `site/pricing.html`, `brand/` (BRAND.md, rules.md, voice.md, offer.md).

**Output:** the reply below, and `audits/accessibility/pricing-a11y.md`. The page and `brand/` were not changed.

## The reply

**Recommendation:** Fix before launch: 4 WCAG failures in the source, all quick fixes.

**Must fix** (WCAG 2.2 failures found in the source)
1. 2.1.1 Keyboard (A) · line 29, the "Questions? Chat with your bookkeeper" `<div>` · opens on click only, so keyboard users can't start a chat · make it `<button type="button" class="chat">`.
2. 1.3.1 Info and Relationships (A) · line 21, the plan and price table · no header cells · make the first row `<th scope="col">Plan</th><th scope="col">Price</th>`.
3. 1.4.3 Contrast (Minimum) (AA) · line 28, "Prices effective October 10, 2026." · #b0b0b0 on white is 2.17:1, needs 4.5:1 · use #757575 (4.58:1).
4. 1.1.1 Non-text Content (A) · line 27, `pricing-badge.png` with `alt="badge"` · doesn't say what the badge says · see below.

**Worth fixing** (best practice, not WCAG failures)
1. The "here" link to /review · clear in its sentence, unclear in a link list · link the words "Start with a free month-end review".

**Needs your input:** what pricing-badge.png says. If it has words, put them in the alt text; if it's decoration, use `alt=""`.

**Passed in the source:** page language, title, one H1, main landmark, logo alt text, 3 of 4 colour pairs.

**Not testable from source:** the chat widget's keyboard and screen reader behaviour once it's a button, whether the badge contains text, and the table at 200% zoom on a phone. Test these with a keyboard and a screen reader before launch.

One brand note: the brand teal button rule (#3FA7A3 with white text) is 2.89:1 and fails contrast wherever it's used. It's not on this page, but consider updating it to #31827f (4.54:1).

Full report: audits/accessibility/pricing-a11y.md
