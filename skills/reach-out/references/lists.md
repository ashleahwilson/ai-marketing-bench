# Lists and several contacts

Use this file when writing to more than one person at once: a list, a segment, or several people at one company.

## One angle per persona, one true line per contact

Group the list by **persona** (what the person is measured on) and by **signal** (why now). Write one draft per persona-and-signal pair. Then add one line per contact that is specific, checkable and connected to the problem, such as a public fact about their company, a role they're hiring for, or their own post. Headcount alone doesn't count. If you can't find a checkable line for a contact, leave the line out. Don't fill the gap with "I noticed" or "came across your profile".

Typical persona angles:
- **Executive (CFO, VP, C-level):** risk, cost, or the plan they've committed to. Under 60 words, softest ask.
- **Manager or owner (controller, head of, director):** throughput, team load, the deadline that slips.
- **Practitioner:** the task that eats their week. Be concrete. They'll know if you're guessing.

## Several people at one company

- Every person the user supplied gets a draft, or is held with a stated reason and a draft ready. Never drop a name silently.
- Lead with the person who owns the problem day to day. Start the executive two business days later, from a different angle.
- Never send two people the same email. They compare notes.
- If someone replies, pause everyone else at that company.

## Slices that don't hold together

If the list has a clear persona but no timing signal, still write the persona template and the merge plan. Flag the hook as persona pain, and suggest one or two signals the user could filter for to sharpen the next run.

If the list shares nothing beyond firmographics (industry, size, country) and has no persona either, there is no "why now". Say so, propose two or three narrower slices the user could filter for (a shared tool, a recent event, a job opening), and ask which one to use. One clearly labelled sample for the strongest slice is fine. Never stage a send to the whole unsegmented list.

## Mechanics

- If the user describes the list but hasn't shared the rows, write the persona template with a `{{varying_line}}` merge field, give the CSV headers, and say what each contact's varying line should be drawn from. Ask for the rows to finish the merge.

- Build the merge in a CSV, with columns for contact, persona, signal, the contact's varying line, and the draft path. Write one draft file per contact so the checker can test each sequence in order.
- In chat, show one template per persona plus a table of contacts with their varying line and start date. Don't paste every rendered email.
- Offer the CSV as an export for whatever sending tool the user has.
- For batches over about 50 recipients on one angle, see the batch size section of [send-gate.md](send-gate.md).

## After the run

When results come in, compare reply rates by persona and by signal, not by individual email. Retire the angle that lost and tighten the slice that won, then record both in the profile under `## Results`.
