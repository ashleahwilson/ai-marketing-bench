# Privacy and personal data

Two separate questions: whether tracking waits for consent, and whether personal data goes into analytics or ad tags. Neither answer is legal advice. Report what the source shows and why it matters for this audience, and leave the legal judgment to whoever handles privacy for the company.

## Where is the audience?

Take it from `brand/audiences.md` or `brand/BRAND.md`, the user, or a clear statement on the site (an address alone isn't the audience). Then:

| Audience | Tags before consent |
|---|---|
| Includes Canada, the EU or the UK | Flag, high severity: list the tags that load before any choice, and recommend holding them until consent (consent mode defaults set to denied, or blocked scripts released on accept) |
| US only | Note it as a fact in one line, not a finding. M5 doesn't require a consent mechanism |
| Unknown | Note it conditionally: "if you serve visitors in Canada, the EU or the UK, these tags load before any consent choice". Ask where the audience is |

Wording to use: "loads before any consent choice", "worth reviewing with whoever handles privacy". Wording never to use: "compliant", "non-compliant", "illegal", "you are breaking", "this violates", or a named law presented as a conclusion about the company.

## Personal data in analytics and ad tags

Never put these in an event parameter, user property, page URL, page title or custom dimension: email, name, phone, street address, the free-text contents of a form field, or a password. That includes "just the email so we can see who converted".

When asked to send them, push back in two or three sentences, then deliver the rest:
1. **Why, concretely:** analytics tools' terms prohibit sending personal data, it puts identity into a system most of the team can read and export, and in Canada, the EU or the UK it raises consent questions. One reason is enough.
2. **How to see who converted anyway:** identity stays in the form backend or CRM. Generate a non-identifying submission ID on success, store it with the record, and send only that ID (or nothing) with the event. Reports show counts and sources; the CRM shows the people.
3. **Ad platform matching** (hashed matching features some platforms offer) is a separate decision for whoever owns privacy, set up under consent and the platform's own terms. Mention it in one line at most; never put raw values in a tag.
4. **Still deliver:** the event, its non-personal parameters (form ID, plan, team-size band, location count), where it fires, and which platforms receive it.

Company name and team size aren't personal data on their own. Keep them only if a report will use them.

## Checking an existing setup

Flag, with the tag or page: a parameter or variable that reads a form field, an email or phone in a URL (`/thanks?email=…`), a user ID that is an email, and a custom HTML tag that scrapes the form. Each is a high-severity finding with the fix: remove the parameter or variable, and republish.
