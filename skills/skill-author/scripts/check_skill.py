#!/usr/bin/env python3
"""Check a skill folder against the build items of the Bench Standard. Standard library only.

Usage:
    python3 scripts/check_skill.py skills/<name>
    python3 scripts/check_skill.py skills/<name> --eval-commands [--source PATH_TO_PUBLIC_SKILL]

Checks: name format and folder match, description length, person and "use when", frontmatter keys,
licence and version, SKILL.md length, links, reference depth and tables of contents, script imports,
evals count, traps, expectations and fixture files, worked examples, changelog, provisional marking.

Prints PASS / WARN / FAIL lines. Exit code 0 if no FAIL, 1 if any FAIL, 2 on bad input.
--eval-commands also prints the commands to run blind evals. It never runs them and never reports results.
"""

import argparse
import json
import os
import re
import sys

NAME_MAX, DESC_MAX = 64, 1024
BODY_TARGET, BODY_MAX = 200, 500
TOC_THRESHOLD = 100
MIN_EVALS, MIN_TRAPS = 8, 2
PORTABLE = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
FIRST_PERSON = re.compile(r"^(i|i'm|i'll|we|we're|you|my|our)\b|\b(i will|i write|i help|i can|i'll|let me)\b", re.I)
STDLIB_EXTRA = {"__future__"}


def stdlib(mod):
    names = getattr(sys, "stdlib_module_names", None)
    if names is not None:
        return mod in names or mod in STDLIB_EXTRA
    return mod in sys.builtin_module_names or mod in {
        "argparse", "collections", "csv", "datetime", "glob", "html", "json", "math", "os", "pathlib",
        "re", "statistics", "string", "sys", "textwrap", "unicodedata", "urllib", "itertools", "functools"}


def frontmatter(text):
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    raw, body = text[3:end].strip("\n"), text[end + 4:]
    data, key, block, nested = {}, None, None, None
    for line in raw.splitlines():
        if block is not None:
            if line.startswith((" ", "\t")) or not line.strip():
                block.append(line.strip())
                data[key] = " ".join(b for b in block if b)
                continue
            block = None
        if nested is not None and line.startswith((" ", "\t")):
            m = re.match(r"^\s+([\w.-]+)\s*:\s*(.*)$", line)
            if m:
                nested[m.group(1)] = m.group(2).strip().strip("\"'")
            continue
        nested = None
        m = re.match(r"^([\w-]+)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val in ("|", ">", "|-", ">-"):
            block, data[key] = [], ""
        elif val == "":
            nested = {}
            data[key] = nested
        else:
            data[key] = val.strip("\"'")
    return data, body


def check(path):
    out = []
    add = lambda lvl, msg: out.append((lvl, msg))
    folder = os.path.basename(os.path.abspath(path))
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", folder):
        add("FAIL", f"folder name '{folder}' must be lowercase letters, digits and single hyphens")
    sm = os.path.join(path, "SKILL.md")
    if not os.path.isfile(sm):
        add("FAIL", "no SKILL.md")
        return out
    fm, body = frontmatter(open(sm, encoding="utf-8").read())
    if fm is None:
        add("FAIL", "SKILL.md has no frontmatter block")
        return out

    name = fm.get("name", "")
    if not name:
        add("FAIL", "frontmatter has no name")
    else:
        if len(name) > NAME_MAX or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            add("FAIL", f"name '{name}' must be lowercase letters, digits and single hyphens (max {NAME_MAX})")
        if name != folder:
            add("FAIL", f"name '{name}' doesn't match the folder name '{folder}'")
        if re.search(r"anthropic|claude", name):
            add("FAIL", "name uses a reserved word (anthropic, claude)")

    desc = fm.get("description", "")
    if not desc:
        add("FAIL", "frontmatter has no description")
    else:
        if len(desc) > DESC_MAX:
            add("FAIL", f"description is {len(desc)} characters (max {DESC_MAX})")
        if re.search(r"<[^>]+>", desc):
            add("FAIL", "description contains angle-bracket tags")
        if FIRST_PERSON.search(desc.strip()):
            add("FAIL", "description isn't in the third person (write 'Writes…', not 'I write…' or 'You…')")
        if not re.search(r"\buse (this |it )?(when|for|whenever)\b|\bwhen the user\b", desc, re.I):
            add("FAIL", "description doesn't say when to use the skill ('Use when…')")

    extra = sorted(set(fm) - PORTABLE)
    if extra:
        add("FAIL", f"non-portable frontmatter keys: {', '.join(extra)}")
    if not fm.get("license"):
        add("WARN", "no license field")
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    ver = meta.get("version", "")
    if not SEMVER.match(ver):
        add("FAIL", "metadata.version missing or not semantic (e.g. \"1.0.0\")")
    if not meta.get("author"):
        add("WARN", "metadata.author missing")
    provisional = ver.startswith("0.") or re.search(r"^\W*(status:\s*)?provisional\b", body, re.I | re.M)

    n = body.count("\n") + 1
    if n > BODY_MAX:
        add("FAIL", f"SKILL.md body is {n} lines (max {BODY_MAX}); move detail into references/")
    elif n > BODY_TARGET:
        add("WARN", f"SKILL.md body is {n} lines (target under {BODY_TARGET})")

    for target in re.findall(r"\]\(([^)#\s]+)\)", body):
        if re.match(r"^[a-z]+://|^mailto:", target):
            continue
        if "\\" in target:
            add("FAIL", f"backslash in link path: {target}")
        if not os.path.exists(os.path.join(path, target)):
            add("FAIL", f"linked file doesn't exist: {target}")

    refs = os.path.join(path, "references")
    for root, _, files in os.walk(refs):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, path).replace(os.sep, "/")
            if os.path.relpath(root, refs) != ".":
                add("FAIL", f"reference nested more than one level deep: {rel}")
            if f.endswith(".md"):
                t = open(p, encoding="utf-8").read()
                if t.count("\n") + 1 > TOC_THRESHOLD and not re.search(r"^##\s+contents\b", t, re.I | re.M):
                    add("FAIL", f"{rel} is over {TOC_THRESHOLD} lines with no '## Contents' section")
                if f"]({rel})" not in body:
                    add("WARN", f"{rel} isn't linked from SKILL.md")

    for root, _, files in os.walk(os.path.join(path, "scripts")):
        for f in files:
            if f.endswith(".py"):
                src = open(os.path.join(root, f), encoding="utf-8").read()
                bad = sorted({m for m in re.findall(r"^\s*(?:import|from)\s+(\w+)", src, re.M) if not stdlib(m)})
                if bad:
                    add("FAIL", f"scripts/{f} imports non-standard-library modules: {', '.join(bad)}")

    ev = os.path.join(path, "evals", "evals.json")
    if not os.path.isfile(ev):
        add("FAIL", "no evals/evals.json")
    else:
        try:
            evals = json.load(open(ev, encoding="utf-8")).get("evals", [])
        except (ValueError, AttributeError) as e:
            add("FAIL", f"evals/evals.json isn't valid: {e}")
            evals = []
        traps = sum(1 for e in evals if e.get("trap"))
        if len(evals) < MIN_EVALS:
            add("WARN" if provisional else "FAIL", f"{len(evals)} evals (need at least {MIN_EVALS})")
        if traps < MIN_TRAPS:
            add("WARN" if provisional else "FAIL", f"{traps} evals marked \"trap\": true (need at least {MIN_TRAPS})")
        for e in evals:
            if not e.get("expectations"):
                add("FAIL", f"eval {e.get('id')} has no expectations")
            if not e.get("prompt"):
                add("FAIL", f"eval {e.get('id')} has no prompt")
            for rel in e.get("files", []):
                if not os.path.isfile(os.path.join(path, rel)):
                    add("FAIL", f"eval {e.get('id')} names a file that doesn't exist: {rel}")

    ex = os.path.join(path, "assets", "examples")
    if not (os.path.isdir(ex) and any(files for _, _, files in os.walk(ex))):
        add("FAIL", "no worked example in assets/examples/")
    cl = os.path.join(path, "CHANGELOG.md")
    if not os.path.isfile(cl):
        add("FAIL", "no CHANGELOG.md")
    elif ver and ver not in open(cl, encoding="utf-8").read():
        add("WARN", f"CHANGELOG.md has no entry for version {ver}")
    if provisional:
        add("WARN", "marked provisional: not ready to publish until the gaps above are closed")
    return out


def find_bench(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isfile(os.path.join(d, "bench", "plan.py")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def eval_commands(path, source):
    name = os.path.basename(os.path.abspath(path))
    root = find_bench(path)
    print("\nBlind eval commands (not run; no results exist until these are run and graded by someone else):")
    if root:
        src = f",comparison-skill:haiku --comparison {source}" if source else ""
        print(f"  cd {root}")
        print(f"  python3 bench/plan.py skills/{name} ../ai-marketing-bench-runs/{name} --iteration 1 "
              f"--configs with-skill:haiku,no-skill:haiku,with-skill:opus,no-skill:opus{src}")
        print(f"  python3 bench/run_headless.py ../ai-marketing-bench-runs/{name}/iteration-1 --parallel 3")
        print("  Grade with bench/prompts/grader.md in a fresh agent that didn't write the skill, then:")
        print(f"  python3 bench/aggregate.py ../ai-marketing-bench-runs/{name}/iteration-1")
    else:
        print("  1. For each eval in evals/evals.json, copy its files into a fresh folder per configuration.")
        print("  2. Give the prompt to a fresh agent with the skill, and to a fresh agent without it"
              + (f", and one with {source}" if source else "") + ". Never show them the expectations.")
        print("  3. Have a separate agent, one that didn't write the skill, grade every output against the")
        print("     expectations, quoting evidence for each pass or fail.")
        print("  4. Record every config's totals, and every lost expectation, in evals/scorecard.json.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_dir")
    ap.add_argument("--eval-commands", action="store_true")
    ap.add_argument("--source")
    a = ap.parse_args()
    if not os.path.isdir(a.skill_dir):
        print(f"not a folder: {a.skill_dir}")
        return 2
    res = check(a.skill_dir)
    fails = sum(1 for lvl, _ in res if lvl == "FAIL")
    warns = sum(1 for lvl, _ in res if lvl == "WARN")
    print(f"[{'FAIL' if fails else ('WARN' if warns else 'PASS')}] {os.path.basename(os.path.abspath(a.skill_dir))}"
          f"  ({fails} fail, {warns} warn)")
    for lvl, msg in res:
        print(f"  {lvl}: {msg}")
    if a.eval_commands:
        eval_commands(a.skill_dir, a.source)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
