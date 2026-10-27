#!/usr/bin/env python3
"""Combine dimension results into the Marketing Health score, grade and confidence. Standard library only.

Usage:
    python3 scripts/score.py audits/<domain>/                      # reads dim-*.json in that folder
    python3 scripts/score.py audits/<domain>/ --offers brand/rules.md   # also map the grade to the auditor's offer
    python3 scripts/score.py audits/<domain>/ --pages 4                 # pages reviewed (of up to 8) caps confidence

Rules:
  - Weights: positioning 25, acquisition 20, conversion 20, brand 15, measurement 20.
  - A dimension that is missing, unassessable or failed counts as a neutral 50, and lowers confidence.
  - Confidence starts from how many dimensions were actually assessed (5 High, 4 Medium, 3 Low, fewer Very Low),
    then drops one level if most assessed dimensions report low confidence themselves, and is capped by page
    coverage: under 4 pages reviewed -> at most Low; 4-5 pages -> at most Medium; 6+ -> no cap.
Writes score.json in the same folder and prints a markdown score table.
"""

import glob
import json
import os
import re
import sys

WEIGHTS = {"positioning": 25, "acquisition": 20, "conversion": 20, "brand": 15, "measurement": 20}
NEUTRAL = 50  # an unassessed dimension neither helps nor hurts the total
BANDS = [
    (85, "A", "Optimise: protect what works and test at the margins."),
    (70, "B", "Fix {w1} before adding anything new."),
    (55, "C", "Rework {w1} and {w2} before putting more into growth."),
    (40, "D", "Rebuild the foundations, starting with {w1} and {w2}."),
    (0, "F", "Get the basics in place ({w1}, {w2}) before investing in growth."),
]
LEVELS = ["Very Low", "Low", "Medium", "High"]


def load(folder):
    dims = {}
    # Only the five canonical files: backups such as dim-brand.prev.json or anything in history/ are ignored,
    # so an old score can never replace the current one.
    names = ("positioning", "acquisition", "conversion", "brand", "measurement")
    for f in [os.path.join(folder, f"dim-{n}.json") for n in names if os.path.isfile(os.path.join(folder, f"dim-{n}.json"))]:
        try:
            d = json.load(open(f, encoding="utf-8"))
            dims[d["dimension"].lower()] = d
        except (ValueError, KeyError) as e:
            print(f"WARN: couldn't read {f}: {e}")
    return dims


def offer_map(path):
    """Read lines like 'A: retainer conversation' under a '### marketing-audit' heading."""
    if not path or not os.path.isfile(path):
        return {}
    text = open(path, encoding="utf-8").read()
    m = re.search(r"^###\s*marketing-audit\s*$(.*?)(?=^#{2,3}\s|\Z)", text, re.M | re.S | re.I)
    if not m:
        return {}
    out = {}
    for g, action in re.findall(r"^-?\s*(?:grade\s*)?([A-F](?:\+|-)?)\s*(?:and above|or below|\+)?\s*[:=→-]+\s*(.+)$", m.group(1), re.M | re.I):
        out[g.upper()[0]] = action.strip()
    return out


def main():
    args = sys.argv[1:]
    offers_path, pages = None, None
    if "--pages" in args:
        i = args.index("--pages")
        pages = int(args[i + 1])
        del args[i:i + 2]
    if "--offers" in args:
        i = args.index("--offers")
        offers_path = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1 or not os.path.isdir(args[0]):
        print(__doc__)
        return 2
    folder = args[0]
    dims = load(folder)
    rows, total, assessed, low = [], 0.0, 0, 0
    for name, w in WEIGHTS.items():
        d = dims.get(name)
        if d and d.get("assessable", True) and d.get("checks"):
            summed = sum(c.get("points", 0) for c in d["checks"])
            if summed != d.get("score"):
                print(f"NOTE: {name} score {d.get('score')} replaced by the sum of its checks ({summed})")
            d["score"] = summed
        ok = bool(d) and d.get("assessable", True) and isinstance(d.get("score"), (int, float))
        score = max(0, min(100, d["score"])) if ok else NEUTRAL
        assessed += ok
        low += ok and str(d.get("confidence", "")).lower() == "low"
        total += score * w / 100
        rows.append((name, w, score, ok))
    total = round(total)
    level = {5: 3, 4: 2, 3: 1}.get(assessed, 0)
    if assessed and low > assessed / 2:
        level = max(0, level - 1)
    if pages is not None:
        level = min(level, 1 if pages < 4 else 2 if pages < 6 else 3)
    cut, grade, action = next(b for b in BANDS if total >= b[0])
    weakest = [n for n, _, s, ok in sorted(rows, key=lambda r: (r[2] if r[3] else 101)) if ok] or ["the unassessed dimensions"]
    action = action.format(w1=weakest[0], w2=weakest[1] if len(weakest) > 1 else weakest[0])
    offers = offer_map(offers_path)
    result = {
        "pages_reviewed": pages, "total": total, "grade": grade, "action": action, "confidence": LEVELS[level],
        "assessed": assessed, "unassessed": [n for n, _, _, ok in rows if not ok],
        "dimensions": {n: {"weight": w, "score": s, "assessed": ok} for n, w, s, ok in rows},
    }
    # score.json sits beside the shareable report, so the offer-map next step is printed only, never saved there.
    json.dump(result, open(os.path.join(folder, "score.json"), "w"), indent=2)
    next_step = offers.get(grade, "")
    print(f"Marketing Health: {total}/100 · Grade {grade} · Confidence: {LEVELS[level]}")
    print(f"{action}")
    if next_step:
        print(f"Next step (from your offer map, for consultant-notes.md only): {next_step}")
    print("\n| Dimension | Weight | Score |\n|---|---|---|")
    for n, w, s, ok in rows:
        print(f"| {n.title()} | {w}% | {s if ok else f'{NEUTRAL} (not assessed)'} |")
    if result["unassessed"]:
        print(f"\nNot assessed (counted as {NEUTRAL}): {', '.join(result['unassessed'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
