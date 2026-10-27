#!/usr/bin/env python3
"""Mechanical help for agency briefs. Standard library only.

    extract  BRAND_DIR --out FILE [--for NAME] [--contact NAME]
        Draft the shareable brand pack from brand/: confirmed facts only, source tags stripped,
        internal files and lines, secrets, TBDs and unapproved claims left out. Prints what was
        left out and why (secret values are never printed).

    check    FILE [--kind brief|extract] [--brand BRAND_DIR] [--exclude PATH ...]
        Check a brief or brand pack before it goes out: required sections, TBDs, secrets, internal
        labels and paths, values from excluded files or internal brand lines, unapproved claims and
        never-use words used outside a prohibition.

    review   --brief BRIEF --proposal PROPOSAL
        Check a proposal against the brief: each deliverable covered or not, money figures side by
        side, red-flag phrases, and phrases the brief bans.

Exit code: 1 if any FAIL, else 0.
"""

import argparse
import csv
import os
import re
import sys

TAG = re.compile(r"\s*\[source:[^\]]*\]")
STATUS = re.compile(r"·\s*(confirmed|provisional|assumed)\b")
SECRET = re.compile(
    r"\b(password|passwd|pwd|api[ _-]?key|secret key|access token|token|bearer)\s*(:|=|\bis\b)\s*\S+"
    r"|\bAIza[0-9A-Za-z_\-]{10,}|\bsk_(live|test)_\w+|\bghp_\w{10,}|\bxox[bp]-\w+",
    re.I,
)
INTERNAL = re.compile(
    r"\binternal\b|confidential|do not (share|forward)|don'?t (share|forward|mention)|leadership only"
    r"|not yet announced|until (the )?announce|\bmargins?\b|floor price|cost to serve|\bCAC\b|\bLTV\b"
    r"|\bMRR\b|\bARR\b|\bchurn(ed)?\b|capacity",
    re.I,
)
EXCLUDED_FILES = {
    "results.md": "internal results data",
    "senders.md": "sender addresses and account details",
    "changelog.md": "internal change history",
    "competitors.md": "internal competitor notes",
}
SKIP_HEADINGS = re.compile(r"^(by skill|by sender|price history|history|reach-out|.*superseded.*)$", re.I)
SECTION_TITLES = [
    ("offer.md", "What we sell"),
    ("audiences.md", "Who it's for (and who it isn't)"),
    ("positioning.md", "Why customers choose us"),
    ("voice.md", "How we sound"),
    ("rules.md", "Rules"),
    ("claims.md", "Claims you can make"),
    ("proof.md", "Proof you can use"),
]
PROHIBIT = re.compile(r"\b(never|don'?t|do not|not to|avoid|no |not approved|banned|not use|claims not)", re.I)
REQUIRED = [
    "background", "objective", "audience", "deliverables", "mandatories", "what not to do",
    "budget", "timeline", "approvals", "success metrics", "assets", "response",
]
RED_FLAGS = [
    ("guarantee", r"guarantee[ds]?|#\s?1\b|number one|first page|page one|top (3|three) (spot|position|ranking)"),
    ("ownership", r"(remain|become)s? (the )?(property|owned)|owned by (us|the agency|[A-Z]\w+)|agency[- ]owned"
                  r"|our (agency )?(manager|MCC|account)|under our|read-only|we (will )?own|retain (all )?(rights|ownership)"),
    ("lock-in", r"\d+[- ]month (agreement|contract|minimum|term|commitment)|auto-?renew\w*|cancell?ation fee|early termination|non-?refundable"),
    ("media markup", r"mark-?up|billed through|plus \d+\s?%"),
    ("credentials", r"password|login details|send (us )?(your )?(login|credentials)|email us your"),
    ("fake reviews or followers", r"(five|5)[- ]star reviews|post \d+ .*reviews|buy(ing)? (reviews|followers|likes)|review (seeding|boost)"),
    ("link schemes", r"\bPBN\b|private blog network|link (package|bundle)|backlink package"),
    ("vague scope", r"as needed|ongoing optimi[sz]ation|various|best efforts|unlimited|and more\b|etc\.?"),
    ("unverifiable claims", r"\d+\+? (businesses|clients|brands)|proprietary AI|outperform|dominate"),
]
MONEY = re.compile(r"\$\s?\d[\d,]*(\.\d+)?\s?(k|K)?(\s?[-–]\s?\$?\d[\d,]*\s?(k|K)?)?(\s?/\s?\w+|\s(a|per) (month|year|location))?")
STOP = set("with from into that this your their have will each over under within built about per the and for our ads".split())


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def mask(line):
    return SECRET.sub(lambda m: m.group(0).split()[0] + " [hidden]", line)


def clean(line):
    line = TAG.sub("", line)
    line = re.sub(r"\s*\((see \w+\.md|date captured)\)", "", line)
    line = re.sub(r"\s*\|\s*(as of|needs substantiation|named):[^|]*", "", line)
    return line.rstrip(" |")


def cmd_extract(a):
    brand = a.brand_dir
    files = sorted(f for f in os.listdir(brand) if f.endswith(".md"))
    company = "Company"
    if "BRAND.md" in files:
        m = re.search(r"^#\s*Brand memory:\s*(.+)$", read(os.path.join(brand, "BRAND.md")), re.M)
        if m:
            company = m.group(1).strip()
    left_out, gaps, secrets = [], [], []
    sections, dont_claim = {}, []
    for f in files:
        text = read(os.path.join(brand, f))
        for i, raw in enumerate(text.splitlines(), 1):
            if SECRET.search(raw):
                secrets.append(f"{f}:{i}")
        if f == "BRAND.md":
            continue
        if f in EXCLUDED_FILES:
            if re.search(r"^\s*-\s", text, re.M):
                left_out.append(f"{f}: whole file ({EXCLUDED_FILES[f]})")
            continue
        heading, skip = "", False
        for raw in text.splitlines():
            line = raw.strip()
            if line.startswith("#"):
                heading = line.lstrip("#").strip()
                skip = bool(SKIP_HEADINGS.match(heading))
                if re.match(r"#{2,3} ", line) and not skip and f != "claims.md":
                    sections.setdefault(f, []).append(f"### {heading}")
                continue
            if not line.startswith("- ") or line.lower().startswith("last reviewed"):
                continue
            if skip:
                left_out.append(f"{f} [{heading}]: internal working rule")
                continue
            if "TBD" in line:
                gaps.append(f"{f}: {clean(line)[2:]}")
                continue
            if SECRET.search(line):
                left_out.append(f"{f}: credential (value hidden)")
                continue
            if INTERNAL.search(line):
                left_out.append(f"{f}: internal line: {mask(clean(line))[2:][:90]}")
                continue
            st = STATUS.search(line)
            status = st.group(1) if st else "untagged"
            body = clean(line)
            needs = f == "claims.md" and re.search(r"substantiation|restricted", heading, re.I)
            if needs or (status == "provisional" and (f in ("claims.md", "offer.md") or "claim" in line.lower())):
                dont_claim.append(body)
                continue
            if status == "assumed" or status == "untagged":
                left_out.append(f"{f}: {status} line: {body[2:][:80]}")
                continue
            if f == "proof.md":
                if re.search(r"named:\s*no\b", line, re.I):
                    left_out.append(f"{f}: proof without permission to name")
                    continue
                if re.search(r"named:\s*(unconfirmed|unknown|tbd)", line, re.I):
                    body += f" Check with {a.contact or 'us'} before naming this customer."
            if status == "provisional":
                body += " (our working view)"
            sections.setdefault(f, []).append(body)
    out = [f"# {company} brand pack", "",
           f"For {a.recipient or 'the people working on this project'}. Please don't share beyond the people working on this project.", ""]
    for f, title in SECTION_TITLES:
        raw = [x for x in sections.get(f, []) if x.strip()]
        lines = [x for j, x in enumerate(raw) if not x.startswith("###") or (j + 1 < len(raw) and raw[j + 1].startswith("- "))]
        if not any(x.startswith("- ") for x in lines):
            continue
        body = []
        for x in lines:
            body += ["", x] if x.startswith("###") else [x]
        out += [f"## {title}"] + body + [""]
    if dont_claim:
        out += ["## Claims not to make", "", "These appear in some of our material but aren't approved for use:", ""]
        out += [re.sub(r"^- (Claimed: )?", "- ", x) + " Not approved for use." for x in dont_claim] + [""]
    out += ["## Questions", "", f"Ask {a.contact or '<contact name>'} before using anything not in this pack.", ""]
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    if os.path.exists(a.out):
        sys.exit(f"FAIL {a.out} exists; pick a new name (never overwrite)")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    print(f"WROTE {a.out}")
    for s in secrets:
        print(f"FAIL credential stored in brand memory at {s}: left out; tell the user to remove it and change it")
    for x in left_out:
        print(f"LEFT OUT {x}")
    for x in dont_claim:
        print(f"NOT APPROVED (listed as a claim not to make) {clean(x)[2:][:90]}")
    for g in gaps:
        print(f"GAP {g}")
    return 1 if secrets else 0


def values_from(path):
    """Distinctive values in an excluded file: names in a CSV's first columns, emails, money and percentages."""
    vals = set()
    text = read(path)
    if path.endswith(".csv"):
        rows = list(csv.reader(text.splitlines()))
        for r in rows[1:]:
            for cell in r[:3]:
                if len(cell) > 3 and not re.fullmatch(r"[\d.,$-]+", cell):
                    vals.add(cell)
    vals.update(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", text))
    vals.update(re.findall(r"\$\s?\d[\d,]*", text))
    vals.update(re.findall(r"\b\d+(?:\.\d+)?%", text))
    return vals


def sections_of(text):
    out, cur = {}, ""
    for line in text.splitlines():
        m = re.match(r"^##\s+(?:\d+\.\s*)?(.+)$", line)
        if m:
            cur = m.group(1).strip().lower()
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def cmd_check(a):
    text = read(a.file)
    lines = text.splitlines()
    fails = 0

    def report(level, msg):
        nonlocal fails
        fails += level == "FAIL"
        print(f"{level} {msg}")

    for i, line in enumerate(lines, 1):
        if SECRET.search(line):
            report("FAIL", f"line {i}: looks like a credential: {mask(line)[:80]}")
        if TAG.search(line) or STATUS.search(line):
            report("FAIL", f"line {i}: source tag or status label left in")
        if re.search(r"\bbrand/|\b\w+\.(md|csv|json)\b", line) and "brand-extract" not in line:
            report("FAIL", f"line {i}: file path or file name the recipient doesn't need: {line.strip()[:80]}")
        if INTERNAL.search(line) and not PROHIBIT.search(line):
            report("WARN", f"line {i}: internal-sounding word, confirm it's meant for the recipient: {line.strip()[:80]}")
        if re.search(r"\bTBD\b", line):
            report("WARN" if a.kind == "brief" else "FAIL", f"line {i}: TBD: {line.strip()[:80]}")
    proof = ""
    if a.brand and os.path.exists(os.path.join(a.brand, "proof.md")):
        proof = read(os.path.join(a.brand, "proof.md"))
    for path in a.exclude or []:
        for v in sorted(values_from(path)):
            if v in text and v in proof:
                print(f"NOTE {v} is in the excluded file and also in brand memory's proof: fine only with its naming note")
            elif v in text:
                report("FAIL", f"value from {os.path.basename(path)} appears: {v}")
    if a.brand and os.path.isdir(a.brand):
        for f in sorted(os.listdir(a.brand)):
            if not f.endswith(".md"):
                continue
            btext = read(os.path.join(a.brand, f))
            for raw in btext.splitlines():
                internal = f in EXCLUDED_FILES or INTERNAL.search(raw) or SECRET.search(raw)
                if internal and raw.strip().startswith("- "):
                    for v in re.findall(r"\$\s?\d[\d,]*|\b\d+(?:\.\d+)?%|[\w.+-]+@[\w-]+\.[\w.]+", raw):
                        if v in text:
                            report("FAIL", f"internal value from brand memory appears: {v}")
                    for w in re.findall(r"(?:password|api key|key):?\s*(\S{6,})", raw, re.I):
                        if w.strip("[]") in text:
                            report("FAIL", "a credential from brand memory appears (value hidden)")
            if f == "claims.md":
                for claim in re.findall(r'"([^"]{8,})"', btext.split("## Needs substantiation")[-1] if "## Needs substantiation" in btext else ""):
                    for i, line in enumerate(lines, 1):
                        if claim.lower()[:20] in line.lower() and not PROHIBIT.search(line) and "claims not" not in (prev_heading(lines, i) or ""):
                            report("FAIL", f"line {i}: unapproved claim used without a prohibition: {claim[:60]}")
            if f == "voice.md":
                m = re.search(r"## Words we never use\s*\n-\s*(.+)", btext)
                if m:
                    for w in [x.strip() for x in TAG.sub("", m.group(1)).split(",") if x.strip()]:
                        for i, line in enumerate(lines, 1):
                            if re.search(rf"\b{re.escape(w)}\b", line, re.I) and not PROHIBIT.search(line) and "never use" not in (prev_heading(lines, i) or ""):
                                report("WARN", f"line {i}: never-use word '{w}' outside a prohibition")
    if a.kind == "brief":
        secs = sections_of(text)
        for need in REQUIRED:
            if not any(need in s for s in secs):
                report("FAIL", f"missing section: {need}")
        budget = next((v for k, v in secs.items() if "budget" in k), [])
        if budget and not re.search(r"\$|TBD|€|£", "\n".join(budget)):
            report("FAIL", "budget section has no figure and no TBD")
        timeline = next((v for k, v in secs.items() if "timeline" in k), [])
        if timeline and not re.search(r"\d{4}|TBD|January|February|March|April|May|June|July|August|September|October|November|December", "\n".join(timeline)):
            report("FAIL", "timeline section has no date and no TBD")
        if timeline and not re.search(r"review|round|feedback", "\n".join(timeline), re.I):
            report("WARN", "timeline names no review rounds")
    print("RESULT", "FAIL" if fails else "PASS")
    return 1 if fails else 0


def prev_heading(lines, i):
    for line in reversed(lines[: i - 1]):
        if line.startswith("#"):
            return line.lower()
    return ""


def key_terms(s):
    words = re.findall(r"[a-z][a-z-]{3,}", s.lower())
    return [w[:6] for w in words if w not in STOP]


def cmd_review(a):
    brief, prop = read(a.brief), read(a.proposal)
    plow = prop.lower()
    secs = sections_of(brief)
    deliv = next((v for k, v in secs.items() if "deliverable" in k), [])
    n = 0
    for row in deliv:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) < 2 or not cells[0].isdigit():
            continue
        n += 1
        terms = key_terms(cells[1])
        hit = [t for t in terms if t in plow]
        state = "COVERED" if terms and len(hit) * 2 >= len(terms) + 1 else "MISSING?"
        print(f"{state} deliverable {cells[0]}: {cells[1]} (matched {len(hit)}/{len(terms)} key words)")
    if not n:
        print("WARN no deliverables table found in the brief")
    budget = "\n".join(next((v for k, v in secs.items() if "budget" in k), []))
    print("MONEY brief:", "; ".join(m.group(0).strip() for m in MONEY.finditer(budget)) or "none")
    print("MONEY proposal:", "; ".join(m.group(0).strip() for m in MONEY.finditer(prop)) or "none")
    seen = set()
    for name, pat in RED_FLAGS:
        for m in re.finditer(pat, prop, re.I):
            start = prop.rfind("\n", 0, m.start()) + 1
            end = prop.find("\n", m.end())
            line = prop[start:end if end > 0 else None].strip()
            if (name, line) in seen:
                continue
            seen.add((name, line))
            if name == "guarantee" and re.search(r"(don'?t|do not|doesn'?t|no|not|never|can'?t|cannot) (offer |make |give )?(a )?guarantee", line, re.I):
                print(f"NOTE guarantee disclaimed, not a red flag: {line[:120]}")
            else:
                print(f"RED FLAG {name}: {line[:120]}")
    banned = set()
    for k, v in secs.items():
        if not any(x in k for x in ("not to do", "mandator")):
            continue
        sub = ""
        for line in v:
            if line.startswith("###"):
                sub = line.lower()
                continue
            if "not to do" in k or "claims not" in sub or PROHIBIT.search(line):
                banned.update(re.findall(r'"([^"]{3,})"', line))
    for phrase in sorted(banned):
        core = phrase.lower().strip(".")
        if core in plow or (len(core) > 12 and core[:14] in plow):
            print(f"BANNED PHRASE in proposal: \"{phrase}\"")
        elif len(core.split()) >= 4:
            words = [w for w in re.findall(r"[a-z0-9]+", core) if len(w) > 2]
            if words and sum(w in plow for w in words) >= len(words) - 1:
                print(f"BANNED PHRASE (close variant) in proposal: \"{phrase}\"")
    for raw in prop.splitlines():
        if not raw.startswith(">"):
            continue
        body = raw.lstrip("> ").strip()
        m = re.fullmatch(r"\*\*(.+)\*\*", body)
        parts = [x.strip() for x in m.group(1).split("|")] if m else [body]
        limit = 30 if m else 90
        for part in parts:
            if part and len(part) > limit:
                kind = "headline" if m else "description"
                print(f"AD LENGTH {kind} is {len(part)} characters (search ad limit {limit}): {part[:80]}")
    for term in re.findall(r"(\d+)[- ]month trial|trial: (\d+) months", brief, re.I):
        print(f"TERM brief trial: {next(t for t in term if t)} months")
    for m in re.finditer(r"\d+[- ]month (agreement|contract|minimum|term|trial)|month to month|auto-?renew\w*", prop, re.I):
        print(f"TERM proposal: {m.group(0)}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract")
    e.add_argument("brand_dir")
    e.add_argument("--out", required=True)
    e.add_argument("--for", dest="recipient")
    e.add_argument("--contact")
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("--kind", choices=["brief", "extract"], default="brief")
    c.add_argument("--brand")
    c.add_argument("--exclude", nargs="*")
    r = sub.add_parser("review")
    r.add_argument("--brief", required=True)
    r.add_argument("--proposal", required=True)
    a = ap.parse_args()
    sys.exit({"extract": cmd_extract, "check": cmd_check, "review": cmd_review}[a.cmd](a))


if __name__ == "__main__":
    main()
