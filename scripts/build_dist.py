#!/usr/bin/env python3
"""Build distribution artifacts from packs.json and skills/. Standard library only.

Usage:
    python3 scripts/build_dist.py            # writes marketplace.json, dist/ zips, dist/INSTALL.md, dist/catalog.json

Outputs:
    .claude-plugin/marketplace.json   one Claude Code plugin per pack, plus "all"
    dist/skills/<skill>.zip           single skill, ready to upload to claude.ai (evals excluded)
    dist/packs/<pack>.zip             every built skill in the pack
    dist/INSTALL.md                   install commands per skill and per pack
    dist/catalog.json                 data for the website (skills, packs, versions, scorecards)

Only skills that exist and pass lint_skill.py are published; planned skills are listed as "planned".
"""

import json
import os
import re
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUDE_DIRS = {"evals", "__pycache__", ".git"}   # tests stay in the repo, not in user downloads


def frontmatter(path):
    text = open(os.path.join(path, "SKILL.md"), encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    get = lambda k: (re.search(rf"^{k}:\s*(.+)$", fm, re.M) or [None, ""])[1].strip().strip('"')
    ver = re.search(r'^\s+version:\s*"?([\d.]+)"?', fm, re.M)
    return {"name": get("name"), "description": get("description"), "version": ver.group(1) if ver else ""}


def lint_ok(path):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "lint_skill.py"), path, "--strict"],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout


def zip_skill(zf, skill_dir, arc_prefix):
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f == ".DS_Store":
                continue
            full = os.path.join(root, f)
            zf.write(full, os.path.join(arc_prefix, os.path.relpath(full, skill_dir)))


def scorecard(skill_dir):
    p = os.path.join(skill_dir, "evals", "scorecard.json")
    return json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else None


def main():
    cfg = json.load(open(os.path.join(ROOT, "packs.json"), encoding="utf-8"))
    repo, market = cfg["repo"], cfg["marketplace"]
    skills_root = os.path.join(ROOT, "skills")
    os.makedirs(os.path.join(ROOT, "dist", "skills"), exist_ok=True)
    os.makedirs(os.path.join(ROOT, "dist", "packs"), exist_ok=True)

    built, skipped = {}, {}
    for name in sorted(os.listdir(skills_root)):
        d = os.path.join(skills_root, name)
        if not os.path.isdir(d):
            continue
        ok, out = lint_ok(d)
        if not ok:
            skipped[name] = out.strip()
            continue
        built[name] = {**frontmatter(d), "scorecard": scorecard(d)}
        with zipfile.ZipFile(os.path.join(ROOT, "dist", "skills", f"{name}.zip"), "w", zipfile.ZIP_DEFLATED) as zf:
            zip_skill(zf, d, name)

    plugins, packs_out = [], []
    for pack in cfg["packs"]:
        live = [s for s in pack["skills"] if s in built]
        packs_out.append({**pack, "live": live, "planned": [s for s in pack["skills"] if s not in built]})
        if not live:
            continue
        plugins.append({"name": pack["name"], "description": pack["description"], "source": "./",
                        "strict": False, "skills": [f"./skills/{s}" for s in live]})
        with zipfile.ZipFile(os.path.join(ROOT, "dist", "packs", f"{pack['name']}.zip"), "w", zipfile.ZIP_DEFLATED) as zf:
            for s in live:
                zip_skill(zf, os.path.join(skills_root, s), s)
    if built:
        plugins.append({"name": "all", "description": "Every published skill in the library.", "source": "./",
                        "strict": False, "skills": [f"./skills/{s}" for s in sorted(built)]})

    marketplace = {"name": market, "owner": {"name": cfg["owner"]},
                   "metadata": {"description": cfg["description"]}, "plugins": plugins}
    os.makedirs(os.path.join(ROOT, ".claude-plugin"), exist_ok=True)
    json.dump(marketplace, open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), "w"), indent=2)

    lines = ["# Install", "", "## Claude Code: by capability", "",
             "```bash", f"/plugin marketplace add {repo}", "```", ""]
    for p in packs_out:
        if p["live"]:
            lines += [f"**{p['title']}**: {', '.join(p['live'])}", "", "```bash",
                      f"/plugin install {p['name']}@{market}", "```", ""]
    lines += ["## Any agent (Claude Code, Codex, Cursor and others)", ""]
    for p in packs_out:
        if p["live"]:
            flags = " ".join(f"--skill {s}" for s in p["live"])
            lines += [f"**{p['title']}**", "", "```bash", f"npx skills add {repo} {flags}", "```", ""]
    lines += ["## One skill at a time", ""]
    for s in sorted(built):
        lines += [f"**{s}** (v{built[s]['version']})", "", "```bash", f"npx skills add {repo} --skill {s}", "```",
                  f"Or download `dist/skills/{s}.zip` and upload it in claude.ai under Settings → Capabilities → Skills.", ""]
    open(os.path.join(ROOT, "dist", "INSTALL.md"), "w").write("\n".join(lines))

    catalog = {"marketplace": market, "repo": repo, "skills": built, "packs": packs_out}
    json.dump(catalog, open(os.path.join(ROOT, "dist", "catalog.json"), "w"), indent=2)

    print(f"Built {len(built)} skill(s): {', '.join(sorted(built)) or 'none'}")
    print(f"Packs with live skills: {', '.join(p['name'] for p in packs_out if p['live']) or 'none'}")
    for name, out in skipped.items():
        print(f"Skipped {name} (fails lint --strict):\n{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
