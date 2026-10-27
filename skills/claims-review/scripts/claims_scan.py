#!/usr/bin/env python3
"""List the candidate claims in a marketing piece and match each one against brand memory. Standard library only.

Usage:
    python3 scripts/claims_scan.py content/home-hero.md --brand brand/
    python3 scripts/claims_scan.py ad.txt                       # no brand memory: lists candidates only
    python3 scripts/claims_scan.py page.html --brand brand/ --json

What it does:
    1. Splits the piece into sentences and tags each one that looks like a claim: numbers, comparatives,
       superlatives, absolutes ("guaranteed", "always", "100%"), "proven"/scientific words, free and pricing
       words, environmental, health, financial, testimonial, endorsement, popularity, AI/capability and
       certification words.
    2. Reads brand/claims.md (Approved / Needs substantiation / Restricted), rules.md, proof.md and offer.md,
       and shows the closest brand-memory line for each candidate, with its section and status.
    3. Flags any phrase that claims.md (Restricted) or rules.md quotes as banned.
    4. Lists lines in brand memory that name a country or market, as jurisdiction hints.

It can't judge truth or risk. Every candidate still needs a reviewer's judgment, and a sentence with no tag
can still be a claim ("clients tell us...").

Exit code: 0 on success (whatever it finds), 2 on bad input.
"""

import argparse
import html
import json
import os
import re
import sys

TAGS = [
    ("number", r"\d+(?:[.,]\d+)?\s?%|\$\s?\d|\b\d+(?:\.\d+)?x\b|\b\d[\d,]*\+|\b(?:twice|double|triple|half|three times)\b|"
               r"\b\d+\s*(?:hours?|days?|weeks?|minutes?|months?)\b|\bfrom an? \w+ to an? \w+|"
               r"\b(?:one|two|three|four|five|ten|fifteen|twenty|fifty|hundred|thousand)\b"),
    ("comparative", r"\b(?:faster|better|cheaper|more accurate|more \w+(?: \w+)?|less|fewer|higher|lower|easier|stronger|smarter)\s+than\b|"
                    r"\bvs\.?\s|\bversus\b|\bcompared (?:to|with)\b|\b(?:twice|\d+x|three times) as\b|\bnot \d+ \w+\b"),
    ("superlative", r"#\s?1\b|\bnumber one\b|\b(?:best|leading|top-rated|fastest|most \w+|the only|largest|cheapest|"
                    r"unbeatable|world-class|unmatched|first-ever)\b"),
    ("absolute", r"\bguarantee[ds]?\b|\balways\b|\bnever\b|\b100\s?%|\brisk[- ]free\b|\bno (?:hidden )?(?:fees|risk|strings)\b|"
                 r"\bforever\b|\bevery\b|\bcancel anytime\b"),
    ("proven/scientific", r"\bproven\b|\bclinical(?:ly)?\b|\bscientific(?:ally)?\b|\btested\b|\bstud(?:y|ies)\b|\blab(?:oratory)?\b|"
                          r"\bresearch shows\b"),
    ("endorsement", r"\brecommended\b|\bdermatologist|\bdoctors?\b|\bdentists?\b|\bexperts?\b|\bendorsed\b|\bapproved by\b|"
                    r"\bpartner\b|#ad\b|\bsponsored\b"),
    ("free/pricing", r"\bfree\b|\btrial\b|\bsave\b|\bwas \$|\bnow (?:just |only )?\$|\bdiscount|\b\d+% off\b|\bprice|\bfees?\b|"
                     r"\bmoney[- ]back\b|\brefund"),
    ("environmental", r"\beco\b|\beco-|\bgreen\b|\bsustainab|\bcarbon\b|\bnet[- ]zero\b|\bclimate\b|\brecyclable\b|\brecycled\b|"
                      r"\bbiodegradable\b|\bcompostable\b|\bplastic[- ]free\b|\bnatural\b|\bnon-toxic\b|\borganic\b|\bchemical-free\b"),
    ("health/safety", r"\bcures?\b|\bheal|\btreats?\b|\bsooth|\brelie(?:f|ve)|\beczema\b|\bpsoriasis\b|\bacne\b|\bimmun|\bdetox|"
                      r"\bsafe (?:for|enough)\b|\bgentle enough\b|\bhypoallergenic\b|\bbab(?:y|ies)\b|\bitch"),
    ("financial/results", r"\brevenue\b|\bROI\b|\breturn\b|\bearn|\bincome\b|\bprofit|\bcosts?\b|\bpaid for itself\b|\bup \d"),
    ("testimonial", r"[\"“][^\"”]{8,}[\"”]|^\s*>"),
    ("popularity", r"\btrusted by\b|\b\d[\d,]*\+?\s+(?:customers|teams|users|merchants|clinics|brands|companies|reviews)\b|"
                   r"\bstars?\b|\brated\b|\breviews\b"),
    ("AI/capability", r"\bAI\b|\bAI-|\bartificial intelligence\b|\bmachine[- ]learning\b|\balgorithm|\bautomat|\bpredicts?\b|"
                      r"\breal[- ]time\b|\binstant"),
    ("certification", r"\bHIPAA\b|\bGDPR\b|\bSOC ?2\b|\bPIPEDA\b|\bcompliant\b|\bcertified\b|\bISO \d"),
]
TAGS = [(name, re.compile(rx, re.I | re.M)) for name, rx in TAGS]
COUNTRY = re.compile(r"\b(Canada|Canadian|Quebec|Québec|United States|U\.S\.|US|USA|America|North America|UK|United Kingdom|"
                     r"EU|Europe|Australia)\b")
STOP = set("""a an the and or of to for in on at by with from your our you we is are be it its this that as not no
any all every on into than then them they their there here what when who how per each over under about only just""".split())
DISCLOSURE = re.compile(r"#ad\b|#sponsored\b|paid partner(ship)?|sponsored|in partnership with|#partner\b|gifted|"
                        r"affiliate|we may earn|commission", re.I)
PAID = re.compile(r"paid (partner|per post)|affiliate|sponsor|gifted|commission|ambassador", re.I)
SECTION_STATUS = {"approved": "approved", "needs substantiation": "needs substantiation", "restricted": "restricted"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def plain(text, path):
    if path.lower().endswith((".html", ".htm")):
        text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
        text = re.sub(r"<(br|p|li|h[1-6]|div|tr)\b[^>]*>", "\n", text, flags=re.I)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return text


def sentences(text):
    """Yield (line_no, sentence) pairs. Markdown markers are stripped; quotes stay whole."""
    for n, line in enumerate(text.splitlines(), 1):
        raw = line.strip()
        if not raw:
            continue
        clean = re.sub(r"^(#+|[-*]|\d+\.)\s+", "", raw)
        clean = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", clean).replace("**", "")
        clean = re.sub(r"</?[a-zA-Z][^>]*>", "", clean).strip()
        parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"“])", clean) if not re.search(r"[\"“]", clean) else [clean]
        for p in parts:
            if p.strip():
                yield n, p.strip()


def words(s):
    return {w for w in re.findall(r"[a-z][a-z0-9-]+", s.lower()) if w not in STOP and len(w) > 2}


def quoted(s):
    return [q.strip() for q in re.findall(r"[\"“]([^\"”]{3,})[\"”]", s)]


def load_brand(brand_dir):
    """Return a list of entries: {file, section, status, text, quotes, words}."""
    entries, hints = [], []
    if not brand_dir or not os.path.isdir(brand_dir):
        return entries, hints
    for fname in sorted(os.listdir(brand_dir)):
        if not fname.endswith(".md"):
            continue
        section = ""
        for line in read(os.path.join(brand_dir, fname)).splitlines():
            h = re.match(r"^#{2,}\s+(.*)", line)
            if h:
                section = h.group(1).strip()
                continue
            if COUNTRY.search(line) and not line.startswith("#"):
                hints.append(f"{fname}: {line.strip()[:140]}")
            if not line.lstrip().startswith("- "):
                continue
            text = line.strip()[2:]
            if fname not in ("claims.md", "rules.md", "proof.md", "offer.md", "BRAND.md", "positioning.md"):
                continue
            tag = re.search(r"·\s*(confirmed|provisional|assumed)", text)
            status = SECTION_STATUS.get(section.lower(), "") if fname == "claims.md" else ""
            if fname == "rules.md":
                status = "rule (" + section + ")"
            if text.startswith("TBD"):
                status = "TBD"
            body = re.sub(r"\[source:[^\]]*\]", "", text)
            keys = [k.strip().lower() for grp in re.findall(r"\(([^)]*)\)", body) for k in grp.split(",") if k.strip()]
            entries.append({"file": fname, "section": section, "status": status or (tag.group(1) if tag else "untagged"),
                            "text": text, "quotes": quoted(text), "words": words(body), "keys": keys})
    return entries, hints


def numbers(s):
    return set(re.findall(r"\d[\d,.]*", s))


def match(sentence, entries):
    """Best brand-memory line for a sentence, plus any banned phrase it contains."""
    sw, sn = words(sentence), numbers(sentence)
    best, best_score, banned = None, 0.0, []
    for e in entries:
        low = sentence.lower()
        restricted = e["file"] == "rules.md" or e["status"] == "restricted"
        if restricted and (any(q.lower() in low for q in e["quotes"]) or
                           any(re.search(r"\b" + re.escape(k) + r"\b", low) for k in e["keys"] if len(k) > 3)):
            banned.append(e)
        overlap = len(sw & e["words"])
        score = overlap / max(3, len(sw)) + (0.5 if overlap and sn & numbers(e["text"]) else 0)
        if any(q.lower() in low for q in e["quotes"]):
            score += 1
        if score > best_score:
            best, best_score = e, score
    if best_score < 0.34:
        best = None
    return best, best_score, banned


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("piece")
    ap.add_argument("--brand", help="path to the brand/ folder")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not os.path.isfile(a.piece):
        print(f"No such file: {a.piece}", file=sys.stderr)
        return 2
    text = plain(read(a.piece), a.piece)
    entries, hints = load_brand(a.brand)
    has_claims = any(e["file"] == "claims.md" for e in entries)
    out = []
    for n, s in sentences(text):
        tags = [name for name, rx in TAGS if rx.search(s)]
        if not tags:
            continue
        best, score, banned = match(s, entries)
        out.append({"line": n, "sentence": s, "tags": tags,
                    "closest": None if not best else {"file": best["file"], "section": best["section"], "status": best["status"],
                                                     "text": best["text"][:200], "strength": "strong" if score >= 0.8 else "possible"},
                    "banned": [{"file": b["file"], "text": b["text"][:200]} for b in banned]})
    disclosure = []
    for e in entries:
        if PAID.search(e["text"]):
            names = re.findall(r"@\w+", e["text"]) + re.findall(r"^([A-Z][a-z]+ [A-Z][a-z]+)", e["text"])
            if any(n.lower() in text.lower() or n.split()[0].lower() in text.lower() for n in names) and not DISCLOSURE.search(text):
                disclosure.append(f"{e['file']}: {e['text'][:160]}")
    if a.json:
        print(json.dumps({"brand": bool(entries), "claims_md": has_claims, "jurisdiction_hints": hints,
                          "missing_disclosure": disclosure, "candidates": out}, indent=1))
        return 0
    print(f"Piece: {a.piece}")
    if not entries:
        print("Brand memory: none found. Nothing can be matched; every candidate is unverified.")
    else:
        print(f"Brand memory: {a.brand} ({'claims.md found' if has_claims else 'no claims.md'})")
    print("Jurisdiction hints: " + ("none in brand memory" if not hints else ""))
    for h in hints[:8]:
        print(f"  {h}")
    for d in disclosure:
        print(f"NO DISCLOSURE: the piece names a paid or connected endorser and has no disclosure ({d})")
    print()
    for c in out:
        print(f"L{c['line']} [{', '.join(c['tags'])}] \"{c['sentence']}\"")
        for b in c["banned"]:
            print(f"    BANNED PHRASE ({b['file']}): {b['text']}")
        if c["closest"]:
            cl = c["closest"]
            sec = f" / {cl['section']}" if cl["section"] else ""
            print(f"    closest ({cl['strength']}): {cl['file']}{sec} [{cl['status']}]: {cl['text']}")
        elif entries:
            print("    closest: nothing in brand memory")
    print(f"\n{len(out)} candidate claims; {sum(1 for c in out if c['banned'])} contain a banned phrase; "
          f"{sum(1 for c in out if not c['closest'])} have no brand-memory match.")
    print("Matches are word overlap, not proof: read each closest line before relying on it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
