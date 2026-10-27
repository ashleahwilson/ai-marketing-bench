# Worked example: a Tallyhouse list from a CRM export and a festival vendor list

Tallyhouse is a fictional restaurant bookkeeping firm. The request:

> Build a list from data/crm.csv and the Halifax Seaport Food Festival vendor list (data/festival-vendors.csv). Unsubscribes are in data/unsubscribes.csv. Score it with icp/scoring.md.

The files:
- `data/`: the two exports and the unsubscribe list (read only)
- `icp/scoring.md`: the rubric, in the `criterion | points` format
- `brand/`: the parts of brand memory the skill reads (who it's for, named clients)
- `lists/atlantic-2026-10.csv`: the scored list, one row per account
- `lists/atlantic-2026-10-excluded.csv`: what was left out and why
- `lists/atlantic-2026-10-summary.md`: the summary, which is also the reply

## What it caught

| In the files | What happened | Why |
|---|---|---|
| "Saltwater Oyster Co. Ltd." in the CRM and "Saltwater Oyster Company" on the vendor list | One account, two contacts | Same domain; the legal suffix and "Co./Company" don't make a different business |
| "Gannet Rock Brewing Co" and "Gannet Rock Brewing" | One account | Same domain |
| Cal Doucette, Gannet Rock's controller | Removed from every file | He's on the unsubscribe list. The account stays, flagged: the remaining contact runs events, so the reply says to find the finance contact first |
| Kelp & Co Seafood Market | Excluded | The CRM marks it Customer |
| Tidepool Tacos' Hotmail address | Kept, flagged | It's in the user's own file, but it's personal: not for cold email without consent |
| Lighthouse Diner Group, no location count | Scored 35, flagged "could reach tier A" | "Group" in the name isn't evidence of how many locations it has. The blank stays blank |

## What it didn't do

- **Guess.** Northern Lights Coffee Roasters and Tidepool Tacos have no country on the vendor list. Halifax and Dartmouth suggest Nova Scotia, but the list doesn't say so, so country stays missing.
- **Drop the coffee roaster.** It matches on title alone and may be a supplier. It's kept and flagged for a person to decide.
- **Pretend the retail check ran.** Neither file has an industry column, so the summary says that disqualifier couldn't be checked.
- **Touch the inputs.** Everything it wrote is in `lists/`.
