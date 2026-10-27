#!/usr/bin/env python3
"""Static quality scan of public skill libraries. Standard library only. Reads files; never executes them.

Usage:
    python3 bench/scan_library.py OUT_DIR LIB_DIR [LIB_DIR ...]

Each LIB_DIR is a cloned skill repository. Every SKILL.md under it (excluding template folders) is scored
0-100 on five categories, then graded A-F. Writes OUT_DIR/results.json, results.csv and summary.md.

What this measures: whether a skill is built to be found, loaded, ported and trusted.
What it can't measure: whether the skill makes an agent's output better. That needs evals (see bench/README.md).

Categories (points):
  Routing     30  can an agent tell when to use it? (description present, length, "use when" triggers,
                  third person, near-miss "not for" scope)
  Structure   20  name valid and matching its folder, body under 500 lines, links resolve, references one level deep
  Portability 20  portable frontmatter only, no hard-wired vendor tools or machine paths, no dependency installs
  Evidence    20  tests defined (8+), test results published, worked examples, versioned
  Safety      10  no risky patterns (pipe-to-shell, rm -rf, eval/exec, hard-coded secrets)
"""

import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from lint_skill import parse_frontmatter, is_stdlib  # noqa: E402

GRADES = [(85, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "F")]
PORTABLE = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
TRIGGER = re.compile(r"\buse (this skill |this |it )?(when|for|whenever|if)\b|\bwhen (the )?(user|you|someone)\b|\btrigger(s|ed)?\b|\binvoke when\b", re.I)
NEAR_MISS = re.compile(r"\b(not for|don'?t use|do not use|isn'?t for|instead use|use .{0,40} instead)\b", re.I)
VENDOR_TOOL = re.compile(r"\b(swan|hubspot|apollo|clay|salesforce|attio|instantly|smartlead)-[a-z]+(-[a-z]+)+\b|\bmcp__[\w-]+", re.I)
MACHINE_PATH = re.compile(r"(/Users/[\w.-]+|/home/[\w.-]+|C:\\\\Users)", re.I)
INSTALL = re.compile(r"\b(pip3? install|npm install|brew install|apt(-get)? install|uv add|poetry add)\b", re.I)
RISKY = [
    (re.compile(r"curl[^\n|]*\|\s*(ba)?sh"), "pipes a download into a shell"),
    (re.compile(r"\brm\s+-rf\s+[/~$]"), "rm -rf on a broad path"),
    (re.compile(r"(?<![\w.])(eval|exec)\("), "eval/exec on dynamic input"),
    (re.compile(r"(api[_-]?key|secret|token|password)\s*[:=]\s*['\"](?!your|<|x{4}|example|placeholder|changeme)[A-Za-z0-9_\-]{16,}['\"]", re.I), "hard-coded secret"),
    (re.compile(r"--dangerously|--no-verify|chmod\s+777"), "disables a safety check"),
]
RESULT_FILES = re.compile(r"(scorecard|benchmark|results?|grading)\.(json|md|csv)$", re.I)
TOPICS = [
    ("outbound", r"cold email|outbound|prospect|sequence|linkedin (dm|outreach)|reply|lead list|sdr|abm|signal"),
    ("sales & deals", r"\bdeal|pipeline|forecast|objection|negotiat|discovery call|close plan|battlecard|win.?loss"),
    ("revops & data", r"revops|crm hygiene|enrich|data quality|routing|lead scor|attribution model"),
    ("ads", r"google ads|meta ads|facebook ads|ppc|paid (search|social|media)|ad creative|campaign budget|roas"),
    ("seo & aeo", r"\bseo\b|search console|keyword|backlink|schema markup|answer engine|\baeo\b|\bgeo\b|ai search"),
    ("cro & pages", r"\bcro\b|conversion|landing page|signup|onboarding flow|pricing page|a/b|ab test|popup|form"),
    ("content & copy", r"copywrit|content|blog|newsletter|editorial|article|social post|video script|email copy"),
    ("brand & positioning", r"brand|positioning|messaging|voice|tone|value prop|icp|persona"),
    ("analytics & reporting", r"analytics|ga4|dashboard|report|looker|tracking|utm|kpi|metric"),
    ("research", r"research|competitor|market (map|analysis)|intel|scrape"),
    ("strategy & planning", r"strategy|marketing plan|gtm plan|launch|roadmap|okr|budget"),
    ("compliance & legal", r"complian|gdpr|casl|can-spam|accessib|wcag|disclos|claim substant|legal"),
    ("team & workflow", r"approval|workflow|intake|brief|handoff|skill (author|creat)|agent|automation"),
]


def grade(score):
    return next(g for cut, g in GRADES if score >= cut)


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return ""


def library_versions(lib):
    """Some libraries keep versions in a root VERSIONS.md table rather than in frontmatter."""
    vf = os.path.join(lib, "VERSIONS.md")
    out = {}
    for m in re.finditer(r"^\|\s*([a-z0-9-]+)\s*\|\s*(\d+\.\d+\.\d+)\s*\|", read(vf), re.M):
        out[m.group(1)] = m.group(2)
    return out


def score_skill(skill_dir, lib_versions):
    text = read(os.path.join(skill_dir, "SKILL.md"))
    fm, body = parse_frontmatter(text)
    fm = fm or {}
    folder = os.path.basename(skill_dir)
    flags, pts = [], {}
    desc = str(fm.get("description", "") or "")
    name = str(fm.get("name", "") or "")

    # Routing (30)
    r = 0
    if desc:
        r += 5 if 50 <= len(desc) <= 1024 else (2 if len(desc) <= 1024 else 0)
        if len(desc) > 1024:
            flags.append("description over 1,024 characters")
        if len(desc) < 50:
            flags.append("description under 50 characters")
        if TRIGGER.search(desc):
            r += 10
        else:
            flags.append("description doesn't say when to use it")
        r += 5 if len(desc.split()) >= 15 else 2
        if re.match(r"^\s*(i|you|we|my|our)\b", desc, re.I):
            flags.append("description not in third person")
        else:
            r += 5
        if NEAR_MISS.search(desc):
            r += 5
    else:
        flags.append("no description")
    pts["routing"] = r

    # Structure (20)
    s = 0
    if name and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and len(name) <= 64 and name == folder:
        s += 5
    else:
        flags.append("name invalid or doesn't match folder")
    lines = body.count("\n") + 1
    if lines <= 500:
        s += 5
    elif lines <= 800:
        s += 2
        flags.append(f"SKILL.md body {lines} lines (over 500)")
    else:
        flags.append(f"SKILL.md body {lines} lines (over 500)")
    links = [t for t in re.findall(r"\]\(([^)#\s]+)\)", body) if not re.match(r"^[a-z]+://|^mailto:", t)]
    broken = [t for t in links if not os.path.exists(os.path.join(skill_dir, t))]
    if broken:
        flags.append(f"{len(broken)} broken internal link(s)")
    else:
        s += 5
    deep, no_toc = 0, 0
    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = [d for d in dirs if d not in ("evals", ".git")]
        rel = os.path.relpath(root, skill_dir)
        for f in files:
            if f.endswith(".md") and f != "SKILL.md":
                if rel.split(os.sep)[0] == "references" and rel.count(os.sep) >= 1:
                    deep += 1
                t = read(os.path.join(root, f))
                if t.count("\n") > 100 and not re.search(r"^#+\s*(contents|table of contents)\b", t, re.I | re.M):
                    no_toc += 1
    s += 5 if not deep and not no_toc else (2 if deep + no_toc <= 2 else 0)
    if deep:
        flags.append("references nested more than one level")
    if no_toc:
        flags.append(f"{no_toc} long reference file(s) without contents")
    pts["structure"] = s

    # Portability (20)
    p = 0
    extra = set(fm) - PORTABLE
    p += 5 if not extra else (3 if len(extra) <= 2 else 1)
    if extra:
        flags.append("non-portable frontmatter: " + ", ".join(sorted(extra)))
    allsrc = text + "".join(read(os.path.join(rt, f)) for rt, _, fs in os.walk(skill_dir) for f in fs if f.endswith(".md") and f != "SKILL.md")
    vend = set(m.group(0).lower() for m in VENDOR_TOOL.finditer(allsrc))
    paths = MACHINE_PATH.search(allsrc)
    if vend:
        flags.append(f"hard-wired vendor tools ({len(vend)})")
    if paths:
        flags.append("machine-specific file paths")
    p += 10 if not vend and not paths else (5 if len(vend) <= 3 and not paths else 0)
    deps = bool(INSTALL.search(allsrc))
    for rt, _, fs in os.walk(skill_dir):
        for f in fs:
            if f.endswith(".py"):
                mods = re.findall(r"^\s*(?:import|from)\s+(\w+)", read(os.path.join(rt, f)), re.M)
                if any(not is_stdlib(m) for m in mods if m not in ("lint_skill",)):
                    deps = True
            if f in ("package.json", "requirements.txt", "pyproject.toml"):
                deps = True
    if deps:
        flags.append("needs package installs")
    else:
        p += 5
    pts["portability"] = p

    # Evidence (20)
    e = 0
    n_evals = 0
    ev = os.path.join(skill_dir, "evals", "evals.json")
    if os.path.isfile(ev):
        try:
            n_evals = len(json.load(open(ev, encoding="utf-8")).get("evals", []))
        except (ValueError, AttributeError):
            n_evals = 0
    e += 8 if n_evals >= 8 else (4 if n_evals else 0)
    if not n_evals:
        flags.append("no tests defined")
    # Only count result files inside an evals/ folder; "scorecard.md" in references/ is usually a content template.
    published = any(RESULT_FILES.search(f) for rt, _, fs in os.walk(os.path.join(skill_dir, "evals")) for f in fs)
    if published:
        e += 6
    else:
        flags.append("no published test results")
    has_ex = any("example" in d.lower() for _, ds, _ in os.walk(skill_dir) for d in ds) or bool(re.search(r"^#+\s*examples?\b", body, re.I | re.M))
    e += 4 if has_ex else 0
    meta = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
    version = meta.get("version") or fm.get("version") or lib_versions.get(folder, "")
    e += 2 if version else 0
    pts["evidence"] = e

    # Safety (10)
    # eval/exec only count in code; other patterns also count in markdown, where instructions are copied and run.
    code_src = "".join(read(os.path.join(rt, f)) for rt, _, fs in os.walk(skill_dir) for f in fs
                       if f.endswith((".py", ".sh", ".js", ".ts")))
    md_src = "".join(read(os.path.join(rt, f)) for rt, _, fs in os.walk(skill_dir) for f in fs if f.endswith(".md"))
    hits = [label for rx, label in RISKY
            if rx.search(code_src) or (not label.startswith("eval") and rx.search(md_src))]
    pts["safety"] = max(0, 10 - 5 * len(hits))
    flags += [f"safety: {h}" for h in hits]

    total = sum(pts.values())
    topic = next((t for t, rx in TOPICS if re.search(rx, f"{name} {desc}", re.I)), "other")
    return {
        "name": name or folder, "folder": folder, "topic": topic, "score": total, "grade": grade(total),
        **pts, "description_chars": len(desc), "body_lines": lines, "evals": n_evals,
        "published_results": published, "version": version, "flags": flags,
    }


def find_skills(lib):
    for root, dirs, files in os.walk(lib):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "templates", "template")]
        if "SKILL.md" in files:
            yield root


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    out_dir, libs = sys.argv[1], sys.argv[2:]
    os.makedirs(out_dir, exist_ok=True)
    rows = []
    for lib in libs:
        lib_name = os.path.basename(os.path.normpath(lib))
        versions = library_versions(lib)
        for sd in sorted(find_skills(lib)):
            rows.append({"library": lib_name, "path": os.path.relpath(sd, lib), **score_skill(sd, versions)})

    json.dump(rows, open(os.path.join(out_dir, "results.json"), "w"), indent=1)
    cols = ["library", "name", "topic", "score", "grade", "routing", "structure", "portability", "evidence",
            "safety", "description_chars", "body_lines", "evals", "published_results", "version", "path"]
    with open(os.path.join(out_dir, "results.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    # Summary
    def pct(n, d):
        return f"{round(100 * n / d)}%" if d else "-"
    L = ["# Skill library scan", "", f"{len(rows)} skills across {len(libs)} libraries. Static checks only: this measures whether a skill is built to be found, loaded, ported and trusted, not whether it improves output.", "",
         "## By library", "", "| Library | Skills | Avg score | A | B | C | D | F | Tests defined | Results published |", "|---|---|---|---|---|---|---|---|---|---|"]
    for lib in sorted({r["library"] for r in rows}):
        rs = [r for r in rows if r["library"] == lib]
        g = {x: sum(r["grade"] == x for r in rs) for x in "ABCDF"}
        L.append(f"| {lib} | {len(rs)} | {sum(r['score'] for r in rs) / len(rs):.0f} | " + " | ".join(str(g[x]) for x in "ABCDF")
                 + f" | {pct(sum(r['evals'] > 0 for r in rs), len(rs))} | {pct(sum(r['published_results'] for r in rs), len(rs))} |")
    L += ["", "## Category averages (points / max)", "", "| Library | Routing /30 | Structure /20 | Portability /20 | Evidence /20 | Safety /10 |", "|---|---|---|---|---|---|"]
    for lib in sorted({r["library"] for r in rows}):
        rs = [r for r in rows if r["library"] == lib]
        L.append(f"| {lib} | " + " | ".join(f"{sum(r[c] for r in rs) / len(rs):.1f}" for c in ["routing", "structure", "portability", "evidence", "safety"]) + " |")
    from collections import Counter
    fc = Counter(f.split(" (")[0].split(":")[0] for r in rows for f in r["flags"])
    L += ["", "## Most common defects", "", "| Defect | Skills | Share |", "|---|---|---|"]
    L += [f"| {k} | {v} | {pct(v, len(rows))} |" for k, v in fc.most_common(15)]
    tc = Counter((r["topic"], r["library"]) for r in rows)
    topics = sorted({r["topic"] for r in rows})
    libs_sorted = sorted({r["library"] for r in rows})
    L += ["", "## Coverage by topic", "", "| Topic | " + " | ".join(libs_sorted) + " | Total |", "|---|" + "---|" * (len(libs_sorted) + 1)]
    for t in sorted(topics, key=lambda t: -sum(tc[(t, l)] for l in libs_sorted)):
        L.append(f"| {t} | " + " | ".join(str(tc[(t, l)]) for l in libs_sorted) + f" | {sum(tc[(t, l)] for l in libs_sorted)} |")
    top = sorted(rows, key=lambda r: -r["score"])[:15]
    L += ["", "## Highest scoring", "", "| Skill | Library | Score | Grade |", "|---|---|---|---|"]
    L += [f"| {r['name']} | {r['library']} | {r['score']} | {r['grade']} |" for r in top]
    open(os.path.join(out_dir, "summary.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L[:20]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
