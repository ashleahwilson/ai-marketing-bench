# Measurement checks

The deep dive scores the same five checks as the full marketing audit, with the same points. What changes is how far it looks before awarding them. Each section below says what to inspect, how a finding maps to a check, and what's never observable.

## Contents
- The checklist (identical to the full audit)
- Scoring rules
- Tags: loaded, configured, firing
- Conversions: is it a real outcome?
- Consent signals
- UTM handling
- Forms
- Tag Manager container exports
- Analytics exports
- Not observable
- Severity and the top three

## The checklist (identical to the full audit)

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| M1 | Analytics configured on every page | 30: present and configured on every page (for GA4, the library and a `config` call, or a Tag Manager container) | 15: on some pages, or loaded without configuration | None |
| M2 | Conversions tracked | 30: conversion events in the source for the primary action | 15: tracking via Tag Manager that can't be seen in the source (say so) | None |
| M3 † | Ad platform tags | 15: tags present where there's paid activity, or no paid activity observed | 8: some missing | Paid activity with no tags |
| M4 | Hygiene | 15: no retired (Universal Analytics) or duplicated tags | 8: one of these | Both, or several duplicates (an unconfigured tag belongs to M1) |
| M5 | Consent basics | 10: a privacy policy link sitewide, and a consent mechanism where required | 5: a policy link only | Neither |

If only rendered text or markdown is available, with no HTML source, measurement is not assessable: set `"assessable": false` and say what's needed (raw HTML, a container export or analytics access).

## Scoring rules

1. **One line of evidence per check:** a page, a tag ID, a quoted line of source, a container tag name or an export row.
2. **Score each issue once.** Unconfigured analytics belongs to M1. A conversion that fires on the wrong thing belongs to M2. Duplicates and retired tags belong to M4. Consent belongs to M5. Personal data in an event has no check of its own: it's still a finding, usually in the top three, but it doesn't move the score.
3. **When torn between two levels, award the lower** and say why.
4. **Founder-led relief applies to M3 only:** a founder-led company that would score 0 gets 8. No relief anywhere else.
5. **The deeper reading of M2.** Full needs an event that fires on the outcome itself: a thank-you page view, a server-confirmed success, a completed booking. An event in the source or the container that fires on a click, a submit attempt, or every page counts as partial at most, with the reason in the evidence. Tag Manager present, no container export: partial, and say it can't be seen.
6. **The deeper reading of M5.** A banner that loads after the tags and doesn't hold them, with no consent mode default, isn't a consent mechanism: score it as a policy link only. "Where required" depends on the audience (see `privacy.md`). With a US-only audience, a sitewide policy link scores full.
7. **The deeper reading of M4.** "Duplicated" means the same ID sends pageviews twice: two `config` calls on one page, a hard-coded tag plus a container tag for the same ID, or a Google tag plus a `page_view` event tag. Suspected but unverifiable (Tag Manager and a hard-coded tag, no export) is a finding with a request for the export, not a deduction.

## Tags: loaded, configured, firing

Three different states. Report each one separately.
- **Loaded:** the library is requested (`gtag/js?id=G-…`, `fbevents.js`, `insight.min.js`).
- **Configured:** something tells it to send (`gtag('config', 'G-…')`, `fbq('init', …)`, a partner ID). GA4 loaded without a `config` call and without a Tag Manager container sends no pageviews from that code. Say so plainly, and give the exact missing line.
- **Firing on the right thing:** events exist for the outcomes that matter (next section).

For every tag found, list: name, ID, pages, loaded or configured, and whether it loads before a consent choice. Tags you can't see in the HTML (anything inside a container) are "inside Tag Manager, not visible without the export".

## Conversions: is it a real outcome?

A conversion counts something the business would pay for: a booked review, a demo request that reached the backend, a created account, an order. Check each conversion-like event:

| It fires on | Verdict |
|---|---|
| A thank-you page view, or a success callback after the server confirms | Real outcome |
| A form `submit` listener before the response | Attempt: counts failed and invalid submits |
| A button `onclick` | Click: counts intent, not the outcome |
| Every click, every page, or a scroll | Not a conversion |
| An automatic event marked as a key event (`page_view`, `session_start`, `first_visit`, `scroll`, `click`) | Not a conversion; inflates every report that uses key events |

A key event with zero events in an export usually means nothing sends that name: compare it with the event names in the source.

## Consent signals

Report what the source shows, not what the law requires:
- A banner or consent platform: present or not, and where it loads relative to the tags.
- Consent mode: is there a `gtag('consent', 'default', …)` call before the tags? Is anything updated on accept?
- Blocked scripts: tags with `type="text/plain"` or a platform's blocking attribute wait for consent.
- Tags that load before any consent choice: list them by name.

Whether that matters depends on the audience. See `privacy.md`.

## UTM handling

- **Internal links with UTMs** (`/pricing?utm_source=homepage…`) start a new session and overwrite the visitor's real source. Fix: remove the UTMs and use an event or a content-group parameter for the banner click.
- **UTMs on outbound links** help the other site's analytics, not this one. Don't flag their absence.
- **Campaign links in an export** that look internal (`website / banner`) confirm the problem with a number from the export.
- A naming convention (lowercase, one separator, no spaces) belongs in the tracking plan when campaigns are in scope.

## Forms

For every form: fields, which are personal (email, name, phone, address), where it submits (a thank-you URL or JavaScript), and which event, if any, fires and when. A form posting to a thank-you page is the easiest conversion to track: a page view of that URL. A form that confirms inline needs the event in the success callback.

## Tag Manager container exports

Run the inspection script on the JSON with the site HTML beside it. Then check:
- **Tags with no firing trigger** never fire. Name each one.
- **Paused tags.**
- **Duplicate pageviews:** a Google tag plus a `page_view` event tag on All Pages, or a container tag plus a hard-coded `config` for the same ID.
- **Conversions on broad triggers:** a lead, signup or purchase event on All Elements clicks, All Pages, or a form-submission trigger without validation.
- **Unused triggers and variables:** often the right trigger already exists. Say which tag should use it.
- **Personal data:** parameters or variables that read form fields (email, name, phone) or identity values.
- **Consent settings:** whether any tag waits for consent.

## Analytics exports

Numbers come only from here, quoted exactly, with the period and the report they came from. Never extrapolate to another period, never add users across rows, and never turn a click count into an outcome count. If a requested figure isn't in the export, it's "not in the export". When the export's event counts something other than what was asked (clicks for trials), say what it counts, give the figure as that, and say where the real figure lives (the product's signup records, billing, the CRM).

## Not observable

From page HTML: traffic, visitors, sessions, conversions, conversion rates, what a tag actually sends at run time, anything inside a Tag Manager container, server-side tracking, the analytics property's settings (key events, filters, retention), and ad spend. List these in every report, with the access that would answer each one.

## Severity and the top three

- **High:** a check worth 30 at 0, a conversion that counts the wrong thing, personal data sent to analytics or ad tags, tags before consent where the audience requires consent, or analytics that sends nothing.
- **Medium:** a partial on a 30-point check, a duplicate, a retired tag, internal UTMs.
- **Low:** the rest.

Pick the top three by severity, then by how much reporting each one corrupts, then by how fast it can be fixed.
