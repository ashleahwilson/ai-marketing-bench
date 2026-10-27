#!/usr/bin/env python3
"""Summarise graded runs into a table, and optionally write the skill's published scorecard.

Usage:
    python3 bench/aggregate.py WORKSPACE/iteration-N
    python3 bench/aggregate.py WORKSPACE/iteration-N --scorecard SKILL_DIR --version 3.0.0

Reads every eval-*/<config>/grading.json (format in bench/prompts/grader.md).
--scorecard writes SKILL_DIR/evals/scorecard.json with per-config totals and every failed expectation,
because the Bench Standard publishes losses as well as wins.
"""

import argparse
import datetime
import glob
import json
import os
import re


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iteration_dir")
    ap.add_argument("--scorecard", help="skill folder to write evals/scorecard.json into")
    ap.add_argument("--version", default="")
    a = ap.parse_args()

    cells, fails = {}, []
    for g in sorted(glob.glob(os.path.join(a.iteration_dir, "eval-*", "*", "grading.json"))):
        cfg = os.path.basename(os.path.dirname(g))
        ev = int(re.search(r"eval-(\d+)", g).group(1))
        data = json.load(open(g, encoding="utf-8"))
        ex = data.get("expectations", [])
        passed = sum(1 for x in ex if x.get("passed"))
        cells[(ev, cfg)] = (passed, len(ex))
        fails += [{"eval": ev, "config": cfg, "expectation": x["text"], "evidence": x.get("evidence", "")}
                  for x in ex if not x.get("passed")]
    if not cells:
        raise SystemExit("No grading.json files found.")

    evs = sorted({e for e, _ in cells})
    cfgs = sorted({c for _, c in cells})
    print("| Eval | " + " | ".join(cfgs) + " |")
    print("|---|" + "---|" * len(cfgs))
    for e in evs:
        print(f"| {e} | " + " | ".join(f"{cells[(e, c)][0]}/{cells[(e, c)][1]}" if (e, c) in cells else "–" for c in cfgs) + " |")
    totals = {}
    for c in cfgs:
        p = sum(cells[k][0] for k in cells if k[1] == c)
        t = sum(cells[k][1] for k in cells if k[1] == c)
        n = sum(1 for k in cells if k[1] == c)
        totals[c] = {"evals": n, "passed": p, "total": t, "rate": round(p / t, 3) if t else 0}
    print("| **Total** | " + " | ".join(f"**{totals[c]['passed']}/{totals[c]['total']} ({totals[c]['rate']:.0%})**" for c in cfgs) + " |")

    if a.scorecard:
        sc = {
            "skill": os.path.basename(os.path.normpath(a.scorecard)),
            "version": a.version,
            "date": datetime.date.today().isoformat(),
            "source_iteration": os.path.basename(os.path.normpath(a.iteration_dir)),
            "method": "Each eval runs per config in a fresh agent that never sees the expectations; a separate grader scores every expectation with evidence.",
            "results": [{"config": c, **totals[c]} for c in cfgs],
            "failed_expectations": fails,
        }
        path = os.path.join(a.scorecard, "evals", "scorecard.json")
        json.dump(sc, open(path, "w"), indent=2)
        print(f"\nWrote {path}")


if __name__ == "__main__":
    main()
