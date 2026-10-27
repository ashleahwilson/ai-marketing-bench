# Keeping brand memory true

## Contents
- Updates
- Feedback from other skills
- Audit
- Sharing

## Updates

When the user gives new information:

1. **Find every place it belongs.** A price change touches `offer.md`, and maybe `BRAND.md` and `claims.md`.
2. **Change it, don't overwrite history.**
   - **Prices:** move the old value to `## Price history`, with dates.
   - **Proof:** replace a result and mark the old line `superseded`.
3. **Tag the new fact:** `[source: user, <date> · confirmed]`. For a change that starts in the future, keep the current value as the live line until the date, and add the new value below it as `Scheduled: <value> from <date>`. A skill reading the folder today must still quote today's value. Note anything public that will need updating on that date, such as the pricing page.
4. **Look for conflicts.** Search the folder for anything the update contradicts: the old price in `BRAND.md`, a banned phrase in `voice.md` examples, a claim in `claims.md`. Fix it or report it.
5. **Log it** in `changelog.md`.
6. **Confirm in one or two lines** what changed and in which files.

## Feedback from other skills

When the user corrects a draft from any skill, that skill should record the lesson here:
- **A one-off fix:** apply it, don't save it.
- **A standing preference:** add it to `rules.md` in the narrowest scope that fits: `Everywhere`, `By skill`, or `By sender`. Write it as a rule that would hold for a different piece of work next month, keep the user's condition, and add the date.
- **About voice in general:** also add it to `voice.md` under `## Do` or `## Don't`.

## Audit

Run `scripts/check_brand.py brand/`, then review what a script can't catch. Report in priority order:

1. **Secrets:** any credential in any file. Tell the user to remove it **and rotate it**, because it may already be in a repo or a shared drive, and offer to remove it from the file now.
2. **Contradictions:** the same fact stated differently in two places (a number, a timeframe, a price).
3. **Permission:** named customers with `named: unconfirmed` or `no` that are being used as if they're named.
4. **Staleness:** files not reviewed in about 6 months, and proof or awards older than about 18 months.
5. **Untagged, mis-tagged and assumed facts:** bullets with no source, the company's own performance claims tagged `confirmed` without evidence, and `assumed` facts that other files treat as confirmed.
6. **Gaps:** missing core files (`offer`, `audiences`, `positioning`, `proof`, `voice`), and `TBD`s or placeholders.

Recommend fixing the first three before the memory is shared outside the team.

## Sharing

Brand memory is often handed to freelancers, agencies or new hires. When producing something to send outside the team:
- Use only `confirmed` facts as fact, and leave out `assumed` ones. For a `provisional` fact or claim, either leave it out, or keep it with a plain-language note **in the text the recipient reads** ("confirm before using"). A warning that only the user sees protects no one.
- Describe permission accurately. "Unconfirmed" means "check before naming", not "we may not name them".
- Leave out sender addresses, results data and internal rules unless the recipient needs them.
- Write for the reader, not about the files. No paths, tags or statuses in the output.
