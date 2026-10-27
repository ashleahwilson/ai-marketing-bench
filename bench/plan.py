#!/usr/bin/env python3
"""Set up an eval iteration: one folder per eval x config, prompt files without expectations, and runner prompts.

Usage:
    python3 bench/plan.py SKILL_DIR WORKSPACE --iteration N [--configs with-skill:opus,with-skill:haiku,no-skill:haiku]
                         [--comparison PATH_TO_COMPARISON_SKILL] [--evals 1,2,9]

Eval "files" (paths relative to the skill) are copied into each run's project folder, under "files_dest" if set,
or per source folder with "files_dest_map" ({"tallyhouse-site": "site/", "tallyhouse-brand/brand": "brand/"}).

Writes:
    WORKSPACE/iteration-N/eval-<id>/prompt.txt                  the task only (no expectations)
    WORKSPACE/iteration-N/eval-<id>/<config>-<model>/outputs/   where the runner writes response.md
    WORKSPACE/iteration-N/runs.json                             one entry per run: dir, model, runner prompt

Hand each runs.json entry to a fresh agent (a subagent, or `claude -p` via bench/run_headless.sh), then grade
with bench/prompts/grader.md and summarise with bench/aggregate.py.
"""

import argparse
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def templates():
    text = open(os.path.join(HERE, "prompts", "runner.md"), encoding="utf-8").read()
    out = {}
    for name in ("with-skill", "no-skill"):
        m = re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
        out[name] = m.group(1).strip()
    out["comparison-skill"] = out["with-skill"] + "\nWhere the skill calls for tools that aren't available, do the closest sensible thing yourself."
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("workspace")
    ap.add_argument("--iteration", type=int, required=True)
    ap.add_argument("--configs", default="with-skill:opus,with-skill:haiku,no-skill:haiku")
    ap.add_argument("--comparison", "--source", dest="comparison", help="path to the public skill to compare against, used by comparison-skill configs")
    ap.add_argument("--evals", help="comma-separated eval ids (default: all)")
    a = ap.parse_args()

    skill_dir = os.path.abspath(a.skill_dir)
    evals = json.load(open(os.path.join(skill_dir, "evals", "evals.json"), encoding="utf-8"))["evals"]
    if a.evals:
        keep = {int(x) for x in a.evals.split(",")}
        evals = [e for e in evals if e["id"] in keep]
    tpl = templates()
    it_dir = os.path.abspath(os.path.join(a.workspace, f"iteration-{a.iteration}"))
    runs = []
    for e in evals:
        e_dir = os.path.join(it_dir, f"eval-{e['id']}")
        os.makedirs(e_dir, exist_ok=True)
        prompt_path = os.path.join(e_dir, "prompt.txt")
        open(prompt_path, "w", encoding="utf-8").write(e["prompt"])
        for cfg in a.configs.split(","):
            kind, model = cfg.split(":")
            if kind == "comparison-skill" and not a.comparison:
                raise SystemExit("--comparison is required for comparison-skill configs")
            out_dir = os.path.join(e_dir, f"{kind}-{model}", "outputs")
            os.makedirs(out_dir, exist_ok=True)
            dmap = e.get("files_dest_map", {})
            for rel in e.get("files", []):
                sub = next((v for k, v in sorted(dmap.items(), key=lambda kv: -len(kv[0])) if f"/{k}/" in f"/{rel}"), e.get("files_dest", ""))
                dest = os.path.join(out_dir, sub)
                os.makedirs(dest, exist_ok=True)
                shutil.copy(os.path.join(skill_dir, rel), os.path.join(dest, os.path.basename(rel)))
            sp = os.path.abspath(a.comparison) if kind == "comparison-skill" else skill_dir
            prompt = tpl[kind].format(prompt_path=prompt_path, skill_path=sp, out_dir=out_dir)
            runs.append({"eval": e["id"], "config": f"{kind}-{model}", "model": model, "out_dir": out_dir,
                         "skill_dir": sp if kind != "no-skill" else None, "prompt": prompt})
    json.dump(runs, open(os.path.join(it_dir, "runs.json"), "w"), indent=2)
    print(f"{len(runs)} runs planned in {it_dir}/runs.json ({len(evals)} evals x {len(a.configs.split(','))} configs)")


if __name__ == "__main__":
    main()
