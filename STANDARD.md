# The Bench Standard

Every skill in this library has to meet this standard before it's published. It combines the design patterns that make skills reliable with public evidence that they work. Most libraries claim rigour; this one shows its test results.

## A. How the skill behaves

1. **It reads the shared brand memory.** Every skill reads the same brand memory (offer, audience, proof, voice, rules) instead of asking again. It still works without one: it marks its output provisional and offers to set one up.
2. **It keeps a fact list. Missing stays missing.** Every name, number and claim in the output traces to the user, the brand memory or a cited source. Anything unknown is flagged as an assumption, never invented. A plausible guess still counts as an invention.
3. **It checks its own output.** Before anything reaches the user, the skill runs its own check: a script for anything mechanical, plus written judgment checks for the rest. A FAIL means rewrite, not hedge.
4. **Its output has a fixed shape.** The output always has the same named sections, so it can be skimmed, compared and handed to the next skill. It opens with the recommendation, not the reasoning.
5. **It knows when not to act.** It pushes back on bad inputs, flags compliance risk, and can recommend doing nothing. It never refuses outright, and never lectures.
6. **It hands off to the next skill.** When one skill's output feeds another (an audit feeds a brief, a brief feeds a draft), it writes a named file the next skill reads.
7. **It has two modes where it matters.** *Guided* pauses at each material decision. *Draft* produces a full first pass for review. Nothing external happens without the user's approval.
8. **It includes worked examples.** At least one complete example input and output ships in `assets/examples/`, with fictional companies and no claimed results.

## B. How the skill is built

9. **It meets the spec.** It follows the [Agent Skills specification](https://agentskills.io/specification):
   - `name` matches the folder.
   - `description` is written in the third person, says what the skill does and when to use it, and is at most 1,024 characters.
   - SKILL.md stays under 500 lines, with reference files one level deep and a table of contents on any reference file over 100 lines.
   - Only portable frontmatter fields are used.
10. **It's original or credited.** It's either written from scratch, or keeps the licence notice of the work it's derived from.
11. **It works without dependencies.** Scripts use the Python standard library only. The skill names no particular CRM or vendor, and uses whatever tools are connected.
12. **It's versioned.** `metadata.version` follows semantic versioning, with a changelog in `CHANGELOG.md` inside the skill folder.

## C. How it's proven

13. **Tests.** At least 8 tests in `evals/evals.json`, each with its expectations written before the runs. At least 2 are traps, where the right answer is to push back, hold or warn.
14. **Comparisons.** Each test runs with the skill, without any skill, and with the comparison skill where one exists, on a large model and a small one.
15. **Blind grading.** A separate grader scores every run against the expectations, with evidence for each judgment.
16. **The bar to publish:**
    - It beats no skill and the comparison skill on total score.
    - It's never worse on safety and compliance tests.
    - No invented facts in any output.
    - It passes `scripts/lint_skill.py`.
17. **A published scorecard.** The scorecard goes on the skill's page, including every test the skill lost.

## Checklist

```
- [ ] A1 brand memory   - [ ] A2 fact list      - [ ] A3 self-check   - [ ] A4 fixed output shape
- [ ] A5 knows limits   - [ ] A6 handoffs       - [ ] A7 two modes    - [ ] A8 worked examples
- [ ] B9 spec lint      - [ ] B10 original/credited  - [ ] B11 no dependencies  - [ ] B12 versioned
- [ ] C13 tests + traps - [ ] C14 comparisons   - [ ] C15 blind grading  - [ ] C16 bar met  - [ ] C17 scorecard
```
