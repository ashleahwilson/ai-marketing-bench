#!/usr/bin/env python3
"""Recompute the measurement checklist score (M1-M5) and its effect on a Marketing Health total. Standard library only.

Usage:
    python3 scripts/score_measurement.py audits/<domain>/dim-measurement.json --pages 5
    python3 scripts/score_measurement.py audits/<domain>/dim-measurement.json --pages 4 --container no \
        --prev audits/<domain>/history/dim-measurement-2026-10-17.json --health audits/<domain>/score.json
    add --founder-led to allow partial credit on M3 (the only check marked † in the measurement rubric)

What it does:
  - Checks that M1-M5 are all present, once each, with the rubric's maximums (30, 30, 15, 15, 10) and an allowed
    level (full, partial or 0; M3 partial instead of 0 only with --founder-led).
  - Sets "score" to the sum of the check points and writes the file back (the dimension file is the skill's own output).
  - Confidence: under 4 pages Low, 4-5 Medium, 6+ High; one level lower if Tag Manager is present and no container
    export was read (--container no); "not assessable" if no HTML source was available (set assessable false yourself).
  - --prev: prints each check's change from an earlier dimension file.
  - --health: recomputes the Marketing Health total and grade from that score.json with this measurement score,
    using the marketing-audit weights and bands. It prints the result and never edits score.json.
"""

import json
import sys

MAX = {"M1": 30, "M2": 30, "M3": 15, "M4": 15, "M5": 10}
PARTIAL = {"M1": 15, "M2": 15, "M3": 8, "M4": 8, "M5": 5}
WEIGHTS = {"positioning": 25, "acquisition": 20, "conversion": 20, "brand": 15, "measurement": 20}
BANDS = [(85, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "F")]
LEVELS = ["Low", "Medium", "High"]


def opt(args, name, default=None):
    if name in args:
        i = args.index(name)
        val = args[i + 1]
        del args[i:i + 2]
        return val
    return default


def main():
    args = sys.argv[1:]
    founder = "--founder-led" in args
    args = [a for a in args if a != "--founder-led"]
    pages, container = opt(args, "--pages"), opt(args, "--container", "n/a")
    prev_path, health_path = opt(args, "--prev"), opt(args, "--health")
    if len(args) != 1:
        print(__doc__)
        return 2
    path = args[0]
    d = json.load(open(path, encoding="utf-8"))
    problems = []
    if str(d.get("dimension", "")).lower() != "measurement":
        problems.append("dimension must be \"measurement\"")
    if d.get("assessable") is False:
        print("Measurement: not assessable. " + str(d.get("reason", "Give the reason in the file.")))
        print("A Marketing Health total counts it as a neutral 50.")
        return 0
    checks = {c.get("id"): c for c in d.get("checks", [])}
    ids = [c.get("id") for c in d.get("checks", [])]
    for cid in MAX:
        if ids.count(cid) != 1:
            problems.append(f"{cid} must appear exactly once (found {ids.count(cid)})")
    for cid, c in checks.items():
        if cid not in MAX:
            problems.append(f"{cid} is not a measurement check")
            continue
        allowed = {MAX[cid], PARTIAL[cid], 0}
        if c.get("points") not in allowed:
            problems.append(f"{cid}: {c.get('points')} points isn't a rubric level ({MAX[cid]}, {PARTIAL[cid]} or 0)")
        if c.get("max") != MAX[cid]:
            problems.append(f"{cid}: max should be {MAX[cid]}")
        if not str(c.get("evidence", "")).strip():
            problems.append(f"{cid}: evidence is empty")
        if cid == "M3" and c.get("points") == PARTIAL["M3"] and "founder" in str(c.get("evidence", "")).lower() and not founder:
            problems.append("M3 cites founder-led relief: rerun with --founder-led if the maturity is founder-led")
    if problems:
        print("FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    score = sum(checks[c]["points"] for c in MAX)
    if d.get("score") != score:
        print(f"NOTE: score {d.get('score')} replaced by the sum of the checks ({score})")
    d["score"] = score
    level = 2
    if pages is not None:
        n = int(pages)
        level = 0 if n < 4 else 1 if n < 6 else 2
    if container == "no":
        level = max(0, level - 1)
    d["confidence"] = LEVELS[level].lower()
    json.dump(d, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"Measurement: {score}/100 · confidence {LEVELS[level]}")
    print("| Check | Points | Max |\n|---|---|---|")
    for cid in MAX:
        print(f"| {cid} | {checks[cid]['points']} | {MAX[cid]} |")
    if prev_path:
        p = json.load(open(prev_path, encoding="utf-8"))
        old = {c["id"]: c.get("points", 0) for c in p.get("checks", [])}
        old_score = sum(old.get(c, 0) for c in MAX) if p.get("checks") else p.get("score")
        print(f"\nEarlier measurement score: {old_score} -> now {score} ({score - (old_score or 0):+d})")
        for cid in MAX:
            if old.get(cid) != checks[cid]["points"]:
                print(f"  {cid}: {old.get(cid)} -> {checks[cid]['points']}")
    if health_path:
        h = json.load(open(health_path, encoding="utf-8"))
        dims = h.get("dimensions", {})
        def total(m):
            t = 0.0
            for name, w in WEIGHTS.items():
                s = m if name == "measurement" else (dims.get(name, {}).get("score") if dims.get(name, {}).get("assessed", True) else 50)
                t += (50 if s is None else s) * w / 100
            return round(t)
        before, after = h.get("total", total(dims.get("measurement", {}).get("score", 50))), total(score)
        grade = lambda t: next(g for cut, g in BANDS if t >= cut)
        print(f"\nMarketing Health total: {before} (grade {grade(before)}) -> {after} (grade {grade(after)}) with measurement at {score}")
        print("score.json is unchanged. Rerun the full audit's scoring to update it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
