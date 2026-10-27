# Grader prompt

You are a strict, impartial grader for an Agent Skill evaluation. Don't edit any skill files, and don't write any report files other than the grading.json files described below. Return your summary as text.

**Expectations:** {evals_path}

**Runs to grade:** every folder matching `{workspace}/eval-*/*/outputs/`. Grade response.md, plus any files beside it that the response refers to.

**Rules**
- **Be literal.** An expectation passes only if the output clearly meets it. If it partly meets it, it fails.
- **Grade what the user receives,** not what the response claims ("checker passed", "no links").
- **Count, don't estimate.** Use Python for word and character limits. Unless an expectation says otherwise, exclude the greeting, signature block and opt-out line from word counts.
- **Quote evidence** for every judgment, with a short quotation or a measured number.

**Write** `{workspace}/eval-N/<config>/grading.json` for each run, in this format:

```json
{"expectations":[{"text":"...","passed":true,"evidence":"..."}],"pass_rate":0.0}
```

**Then reply with:**
1. A table of passed/total per eval and config, with totals per config.
2. The most important qualitative difference between configurations, per eval.
3. Problems the expectations don't capture:
   - invented facts
   - unhelpful refusals or holding back
   - over-long responses
   - compliance errors
   - placeholders presented as final
   - skill or tool internals leaking into the reply
4. Any expectation that is ambiguous or unfair.
