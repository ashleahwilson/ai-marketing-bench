# Writing the evals

## Contents
- How many and what kind
- Building them from the real work
- The file format
- Fixtures
- Expectations that can be graded
- If there isn't enough material

## How many and what kind

At least 8 evals, at least 2 of them traps. Across the set, include:
- every method rule tested at least once (put the eval ids in the ledger);
- **traps**, where the right answer is to push back, hold, ask or leave a gap. The best traps come straight from corrections: the moment the user said "no" is the moment a model without the skill gets it wrong;
- one case with no brand memory, where the output must be marked provisional;
- one case where the facts needed aren't given, so the skill must not invent them;
- one case that tests a mode or a hand-off file, if the skill has one;
- one clean case where the right answer is to do the job with no drama (so the skill isn't rewarded for finding problems that aren't there).

## Building them from the real work

Turn each real case in the source into an eval, with the real details replaced by fictional stand-ins. Then add cases that vary one thing at a time: missing data, a rule that pulls the other way, a user in a hurry. Every eval should be something a real user of the skill would plausibly ask.

Make some expectations hard enough that a strong model without the skill can fail them. A test every configuration passes can't tell a good skill from a bad one. The corrections tell you where those are: the user had to correct a capable assistant, so the uncorrected behaviour is the default.

## The file format

```json
{
  "skill_name": "<name>",
  "evals": [
    {
      "id": 1,
      "trap": true,
      "prompt": "The user's request, word for word as they'd type it",
      "expected_output": "One or two sentences on what a good answer does",
      "files": ["evals/files/<case>/<file>.md"],
      "files_dest": "work/",
      "expectations": ["Literal, gradeable statements about the output"]
    }
  ]
}
```

- `files` are paths relative to the skill folder. Every one must exist.
- `files_dest` puts them all in one project subfolder. `files_dest_map` (`{"<case>/brand": "brand/", "<case>": "work/"}`) sends different source folders to different places.
- Leave `trap` out for ordinary evals.

## Fixtures

- Small: a short transcript, one draft, a few brand memory lines. A test that needs a 3,000-word input tests patience, not the skill.
- Fictional companies and people, with reserved domains (`.example`). Never the real client from the source material.
- Plant specific, checkable problems: an exact figure the output must not round, a name without permission, a word over the limit.
- Brand memory fixtures use source tags: `[source: <where>, <date> · confirmed | provisional | assumed]`.

## Expectations that can be graded

- **Literal:** "States the cap as 350 words" is gradeable. "Handles length well" isn't.
- **From the output alone,** without reading the transcript of how it got there.
- **Measured where possible:** "The reply is under 200 words (measured)".
- **Negative expectations for the traps:** "Does not invent a figure for the time saved", "Does not name the customer".
- Written before any run, and not loosened later to make a run pass. Clarify one only if a grader shows it's genuinely ambiguous, and then re-grade every configuration on it.

## If there isn't enough material

With one real case, write only the evals the material supports (often one or two), mark the set as incomplete in the ledger, and list the cases needed to reach 8. Never present invented cases as if they came from the user's work. If you add placeholder cases to show the shape, label them `"provisional": true` and say in the reply that they need real inputs.
