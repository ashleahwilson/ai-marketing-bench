#!/usr/bin/env python3
"""Check a skill folder against the build items of the Bench Standard (B9, B12, A8, C13). Standard library only.

Usage:
    python3 scripts/lint_skill.py skills/reach-out
    python3 scripts/lint_skill.py skills/*            # every skill
    python3 scripts/lint_skill.py skills/* --strict   # treat WARN as FAIL (use before publishing)

Exit code: 0 clean, 1 if any FAIL, 2 on bad input.
"""

import importlib.util
import json
import os
import re
import sys
import sysconfig

# Limits from the Agent Skills specification and Anthropic's authoring guidance.
NAME_MAX, DESC_MAX, COMPAT_MAX = 64, 1024, 500
BODY_MAX_LINES = 500          # keep SKILL.md under 500 lines; split into references beyond that
TOC_THRESHOLD = 100           # reference files longer than this need a table of contents
MIN_EVALS, MIN_TRAPS = 8, 2   # Bench Standard C13
PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def is_stdlib(mod):
    """True if the module ships with Python (works on 3.8+, where sys.stdlib_module_names may not exist)."""
    names = getattr(sys, "stdlib_module_names", None)
    if names is not None:
        return mod in names
    if mod in sys.builtin_module_names:
        return True
    spec = importlib.util.find_spec(mod)
    if spec is None or spec.origin is None:
        return False
    if spec.origin in ("built-in", "frozen"):
        return True
    return spec.origin.startswith(sysconfig.get_paths()["stdlib"]) and "site-packages" not in spec.origin


def parse_frontmatter(text):
    """Minimal YAML subset: top-level 'key: value' (incl. quoted), '|'/'>' blocks, and one nested map (metadata)."""
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
                nested[m.group(1)] = m.group(2).strip().strip('"\'')
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
            data[key] = val.strip('"\'')
    return data, body


def lint(path):
    out = []
    add = lambda lvl, code, msg: out.append((lvl, code, msg))
    folder = os.path.basename(os.path.normpath(path))
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        add("FAIL", "B9", "no SKILL.md")
        return out
    text = open(skill_md, encoding="utf-8").read()
    fm, body = parse_frontmatter(text)
    if fm is None:
        add("FAIL", "B9", "SKILL.md has no YAML frontmatter")
        return out

    name = fm.get("name", "")
    if not name:
        add("FAIL", "B9", "frontmatter has no name")
    else:
        if len(name) > NAME_MAX or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name):
            add("FAIL", "B9", f"name '{name}' must be lowercase letters, digits and single hyphens, max {NAME_MAX}")
        if name != folder:
            add("FAIL", "B9", f"name '{name}' doesn't match folder '{folder}'")
        if re.search(r"anthropic|claude", name):
            add("FAIL", "B9", "name contains a reserved word (anthropic, claude)")

    desc = fm.get("description", "")
    if not desc:
        add("FAIL", "B9", "frontmatter has no description")
    else:
        if len(desc) > DESC_MAX:
            add("FAIL", "B9", f"description is {len(desc)} characters (max {DESC_MAX})")
        if re.search(r"<[^>]+>", desc):
            add("FAIL", "B9", "description contains XML/HTML tags")
        if re.match(r"^(i|you|we)\b", desc.strip(), re.I):
            add("WARN", "B9", "description should be third person ('Drafts…', not 'I/You/We…')")
        if not re.search(r"\buse (this |it )?(when|for|whenever)\b|\bwhen the user\b", desc, re.I):
            add("WARN", "B9", "description doesn't say when to use the skill ('Use when…')")

    unknown = set(fm) - PORTABLE_KEYS
    if unknown:
        add("WARN", "B9", f"non-portable frontmatter keys (ignored by other agents): {', '.join(sorted(unknown))}")
    if "compatibility" in fm and len(str(fm["compatibility"])) > COMPAT_MAX:
        add("FAIL", "B9", f"compatibility is over {COMPAT_MAX} characters")

    lines = body.count("\n") + 1
    if lines > BODY_MAX_LINES:
        add("FAIL", "B9", f"SKILL.md body is {lines} lines (max {BODY_MAX_LINES}); move detail to references/")

    # Links: exist, forward slashes, one level deep from SKILL.md
    for target in re.findall(r"\]\(([^)#\s]+)\)", body):
        if re.match(r"^[a-z]+://|^mailto:", target):
            continue
        if "\\" in target:
            add("FAIL", "B9", f"backslash in path: {target}")
        if not os.path.exists(os.path.join(path, target)):
            add("FAIL", "B9", f"linked file doesn't exist: {target}")
    for root, _, files in os.walk(os.path.join(path, "references")):
        for f in files:
            if not f.endswith(".md"):
                continue
            p = os.path.join(root, f)
            if os.path.relpath(root, path).count(os.sep) > 0:
                add("WARN", "B9", f"reference nested more than one level deep: {os.path.relpath(p, path)}")
            ref = open(p, encoding="utf-8").read()
            if ref.count("\n") + 1 > TOC_THRESHOLD and not re.search(r"^##\s+contents\b", ref, re.I | re.M):
                add("WARN", "B9", f"{os.path.relpath(p, path)} is over {TOC_THRESHOLD} lines with no '## Contents'")
            if f"]({os.path.relpath(p, path)})" not in body and f"]({os.path.relpath(p, path).replace(os.sep, '/')})" not in body:
                add("WARN", "B9", f"{os.path.relpath(p, path)} isn't linked from SKILL.md")

    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    if not SEMVER.match(meta.get("version", "")):
        add("FAIL", "B12", "metadata.version missing or not semantic (e.g. \"1.0.0\")")
    if not os.path.isfile(os.path.join(path, "CHANGELOG.md")):
        add("WARN", "B12", "no CHANGELOG.md")
    if not fm.get("license"):
        add("WARN", "B10", "no license field")

    ex = os.path.join(path, "assets", "examples")
    if not (os.path.isdir(ex) and os.listdir(ex)):
        add("WARN", "A8", "no worked examples in assets/examples/")

    ev = os.path.join(path, "evals", "evals.json")
    if not os.path.isfile(ev):
        add("FAIL", "C13", "no evals/evals.json")
    else:
        try:
            evals = json.load(open(ev, encoding="utf-8")).get("evals", [])
        except (json.JSONDecodeError, AttributeError) as e:
            add("FAIL", "C13", f"evals.json is invalid: {e}")
            evals = []
        if len(evals) < MIN_EVALS:
            add("FAIL", "C13", f"{len(evals)} evals (need at least {MIN_EVALS})")
        traps = sum(1 for e in evals if e.get("trap"))
        if traps < MIN_TRAPS:
            add("WARN", "C13", f"{traps} evals marked \"trap\": true (need at least {MIN_TRAPS})")
        for e in evals:
            if not e.get("expectations"):
                add("FAIL", "C13", f"eval {e.get('id')} has no expectations")

    for root, _, files in os.walk(os.path.join(path, "scripts")):
        for f in files:
            if f.endswith(".py"):
                src = open(os.path.join(root, f), encoding="utf-8").read()
                third = [m for m in re.findall(r"^\s*(?:import|from)\s+([\w]+)", src, re.M)
                         if not is_stdlib(m)]
                if third:
                    add("WARN", "B11", f"{f} imports non-standard-library modules: {', '.join(sorted(set(third)))}")
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--strict"]
    strict = "--strict" in sys.argv
    if not args:
        print(__doc__)
        return 2
    worst = 0
    for path in args:
        if not os.path.isdir(path):
            continue
        res = lint(path)
        fails = sum(1 for r in res if r[0] == "FAIL" or (strict and r[0] == "WARN"))
        status = "FAIL" if fails else ("WARN" if res else "PASS")
        print(f"[{status}] {os.path.basename(os.path.normpath(path))}")
        for lvl, code, msg in res:
            print(f"    {lvl} {code}: {msg}")
        worst = max(worst, 1 if fails else 0)
    return worst


if __name__ == "__main__":
    sys.exit(main())
