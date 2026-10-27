#!/usr/bin/env python3
"""Check and total the brand checklist (B1-B5), and recompute the Marketing Health score if the other
dimensions are on disk. Standard library only. The checks, weights and grade bands match the marketing audit.

Usage:
    python3 scripts/brand_score.py audits/<domain>/ --pages 6

Reads audits/<domain>/dim-brand.json:
    {"dimension": "brand", "assessable": true, "confidence": "high|medium|low",
     "brand_memory": "company|none|auditor",
     "checks": [{"id": "B1", "points": 12, "max": 25, "evidence": "..."}, ...],
     "score": 47, "findings": [...], "strengths": [...], "not_observable": [...]}

Checks:
    FAIL  a check missing or repeated, points not one of the allowed levels, empty evidence
    FAIL  B5 not following the fallback when the brand memory is not the company's (10 if B1 and B2 are both
          full, otherwise 5)
    FIX   score replaced by the sum of the checks (the file is rewritten with the sum)
    NOTE  confidence above what the page count allows (under 4 pieces: Low; 4-5: Medium; 6+: High)
Then prints the change from the latest audits/<domain>/history/dim-brand-*.json if one exists, and the recomputed Marketing Health total and grade
if dim-positioning/acquisition/conversion/measurement.json are in the same folder (missing ones count as 50).

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import json
import os
import sys

LEVELS = {"B1": (25, 12, 0), "B2": (25, 12, 0), "B3": (20, 10, 0), "B4": (20, 10, 0), "B5": (10, 5, 0)}
WEIGHTS = {"positioning": 25, "acquisition": 20, "conversion": 20, "brand": 15, "measurement": 20}
NEUTRAL = 50
BANDS = [(85, "A", "Optimise: protect what works and test at the margins."),
         (70, "B", "Fix {w1} before adding anything new."),
         (55, "C", "Rework {w1} and {w2} before putting more into growth."),
         (40, "D", "Rebuild the foundations, starting with {w1} and {w2}."),
         (0, "F", "Get the basics in place ({w1}, {w2}) before investing in growth.")]
CONF = ["Very Low", "Low", "Medium", "High"]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    args = sys.argv[1:]
    pages = None
    if "--pages" in args:
        i = args.index("--pages")
        pages = int(args[i + 1])
        del args[i:i + 2]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__)
        return 2
    folder = args[0]
    path = os.path.join(folder, "dim-brand.json")
    if not os.path.isfile(path):
        print(f"error: {path} not found")
        return 2
    try:
        d = load(path)
    except ValueError as e:
        print(f"FAIL: dim-brand.json is not valid JSON: {e}")
        return 1
    fails = []
    if d.get("dimension", "").lower() != "brand":
        fails.append("dimension must be \"brand\"")
    checks = {}
    for c in d.get("checks", []):
        cid = str(c.get("id", "")).upper()
        if cid in checks:
            fails.append(f"{cid} appears twice")
        checks[cid] = c
    for cid, (full, part, zero) in LEVELS.items():
        c = checks.get(cid)
        if not c:
            fails.append(f"{cid} is missing")
            continue
        if c.get("points") not in (full, part, zero):
            fails.append(f"{cid} has {c.get('points')} points; allowed: {full}, {part} or {zero}")
        if c.get("max") != full:
            fails.append(f"{cid} max should be {full}")
        if not str(c.get("evidence", "")).strip():
            fails.append(f"{cid} has no evidence")
    owner = str(d.get("brand_memory", "")).lower()
    if owner not in ("company", "none", "auditor"):
        fails.append("brand_memory must be \"company\", \"none\" or \"auditor\"")
    elif owner != "company" and all(k in checks for k in ("B1", "B2", "B5")):
        want = 10 if checks["B1"].get("points") == 25 and checks["B2"].get("points") == 25 else 5
        if checks["B5"].get("points") != want:
            fails.append(f"B5 should be {want}: there is no brand memory for this company, so B5 follows B1 and B2")
    total = sum(c.get("points", 0) for c in checks.values() if c.get("id", "").upper() in LEVELS)
    if d.get("score") != total:
        print(f"FIX: score {d.get('score')} replaced by the sum of the checks ({total})")
        d["score"] = total
        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=1, ensure_ascii=False)
    if pages is not None:
        cap = 1 if pages < 4 else 2 if pages < 6 else 3
        stated = str(d.get("confidence", "")).capitalize()
        if stated and stated in CONF and CONF.index(stated) > cap:
            print(f"NOTE: confidence '{stated}' is above what {pages} pieces allow; use {CONF[cap]}")
    for f in fails:
        print(f"FAIL: {f}")

    print(f"\nBrand: {total}/100")
    print("| Check | Points | Max |\n|---|---|---|")
    for cid, (full, _, _) in LEVELS.items():
        print(f"| {cid} | {checks.get(cid, {}).get('points', '-')} | {full} |")

    import glob as _glob
    _hist = sorted(_glob.glob(os.path.join(folder, "history", "dim-brand-*.json")))
    prev = _hist[-1] if _hist else os.path.join(folder, "history", "dim-brand-none.json")
    if os.path.isfile(prev):
        p = load(prev)
        pc = {str(c.get("id", "")).upper(): c.get("points") for c in p.get("checks", [])}
        print(f"\nChange from the earlier brand score: {p.get('score')} -> {total}")
        for cid in LEVELS:
            if pc.get(cid) != checks.get(cid, {}).get("points"):
                print(f"  {cid}: {pc.get(cid)} -> {checks.get(cid, {}).get('points')}")

    others = {}
    for name in WEIGHTS:
        if name == "brand":
            continue
        fp = os.path.join(folder, f"dim-{name}.json")
        if os.path.isfile(fp):
            try:
                od = load(fp)
                if od.get("assessable", True) and od.get("checks"):
                    others[name] = sum(c.get("points", 0) for c in od["checks"])
                elif od.get("assessable", True) and isinstance(od.get("score"), (int, float)):
                    others[name] = od["score"]
            except ValueError:
                pass
    if others:
        scores = {n: others.get(n, NEUTRAL) for n in WEIGHTS}
        scores["brand"] = total
        overall = round(sum(scores[n] * w / 100 for n, w in WEIGHTS.items()))
        cut, grade, action = next(b for b in BANDS if overall >= b[0])
        weakest = sorted(scores, key=lambda n: scores[n])
        print(f"\nMarketing Health with the new brand score: {overall}/100 · Grade {grade}")
        print(action.format(w1=weakest[0], w2=weakest[1]))
        print("| Dimension | Weight | Score |\n|---|---|---|")
        for n, w in WEIGHTS.items():
            note = "" if n == "brand" or n in others else " (not on disk, counted as 50)"
            print(f"| {n.title()} | {w}% | {scores[n]}{note} |")
        sp = os.path.join(folder, "score.json")
        if os.path.isfile(sp):
            try:
                old = load(sp)
                print(f"Earlier total in score.json: {old.get('total')} (Grade {old.get('grade')}). score.json is left as it was.")
            except ValueError:
                pass
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
