# AI Marketing Bench

Tested marketing and go-to-market skills for AI agents, by Ashleah Wilson. Website: [aimarketingbench.com](https://aimarketingbench.com). Install one skill, or install a whole capability.

Each skill is a folder with a `SKILL.md` that follows the open [Agent Skills specification](https://agentskills.io/specification), so it works in Claude (claude.ai, Claude Code, the API), Codex, Cursor and other agents that support the format. No skill assumes a particular CRM, data provider or sending tool.

## What makes these different

Every skill is built and tested to [the Bench Standard](STANDARD.md) and ships with its test results:
- It reads one shared brand memory, traces every claim to a source, checks its own output before you see it, and knows when to push back.
- It's tested with the skill, without it, and against the public skill it replaces, on a large model and a small one, with blind grading.
- The scorecard is published in `evals/scorecard.json`, including the tests it lost. Where a skill hasn't fully cleared the bar yet, the scorecard says so.

## Capabilities

| Capability | Skills | Status |
|---|---|---|
| **Outbound** | reach-out · handle-reply · competitor-intel · icp · build-list · map-contacts | live, 6 skills |
| **Marketing Audit** | marketing-audit + positioning, acquisition, conversion, brand and measurement deep dives | live, 6 skills |
| **Brand** | brand-memory · brand-voice-codify · de-slop · brand-voice-gate | live, 4 skills |
| **Content Ops** | content-brief · content-qa-gate · editorial-review-cycle · content-audit · email-sequence · linkedin-content | live, 6 skills |
| **Paid Ads** | google-ads-audit · google-ads-build · meta-ads-audit · meta-ads-build | live, 4 skills |
| **Team Ops** | skill-author · ai-workload-map · campaign-intake · approval-routing · agency-brief | live, 5 skills |
| **Claims & Compliance** | claims-review · accessibility-review · disclosure-check | live, 3 skills |

Some skills carry a note in their `SKILL.md` ("Recommended for large models" or "Use with care"). The scorecard explains why.

## Install

**One capability in Claude Code**

```bash
/plugin marketplace add ashleahwilson/ai-marketing-bench
```

```bash
/plugin install outbound@ai-marketing-bench
```

**Any agent: one skill or several**

```bash
npx skills add ashleahwilson/ai-marketing-bench --skill reach-out
```

**claude.ai:** download a skill's zip from the website and upload it under Settings → Capabilities → Skills.

The full list of commands is generated in `dist/INSTALL.md`.

## For contributors

```bash
python3 scripts/lint_skill.py skills/* --strict
```

```bash
python3 scripts/build_dist.py
```

`packs.json` defines the capabilities. The build regenerates `.claude-plugin/marketplace.json`, the zips, the install guide and `dist/catalog.json`, which the website reads. A skill is published only once it passes the strict lint.

## Licence

MIT. See [LICENSE](LICENSE).
