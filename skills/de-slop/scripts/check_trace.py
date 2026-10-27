#!/usr/bin/env python3
"""Check that every sentence of a revision traces to the draft or to confirmed brand memory. Standard library only.

Usage:
    python3 scripts/check_trace.py drafts/post-gated.md --trace drafts/post-trace.md --original drafts/post.md --brand brand/

Trace file format (two blocks):

    TRACE
    - "I was a restaurant controller before I co-founded Tallyhouse" | brand/proof.md: "Dev Patel, former restaurant controller"
    - "Your sales are reconciled every day" | draft: "reconciles your sales from Toast, Square and Lightspeed" + brand/offer.md: "Daily sales reconciled automatically"
    - "Send me a message and I'll set it up." | no claim

    CHANGES
    - removed: "AI-powered platform" | brand never-use list
    - changed: "we've got you covered" | stock phrasing

Each TRACE line quotes a sentence (or its opening words) from the revision, then its evidence: one or more
`draft: "<words>"` or `brand/<file>: "<words>"` quotes joined by +, or `no claim` for a sentence that states no fact.

FAIL when:
    - a revision sentence has no TRACE line
    - an evidence quote isn't found word for word in the draft or the named brand file
    - brand evidence comes from voice.md or rules.md (voice examples and rules are not facts), or from a line that is
      provisional, assumed, TBD, unsubstantiated, or under a "Needs substantiation" or "Restricted" heading
    - a sentence contains a number, or a widening word (every, all, clients, team...), that none of its evidence has
    - a sentence uses a fact term from the draft or brand memory (e.g. "prime cost") that its own evidence doesn't
      contain: the swapped-noun case, where every word looks sourced but the claim isn't
    - evidence quoted from a customer's own words (a quotation in proof.md) supports a sentence that doesn't quote or
      name that customer: one customer's experience isn't a promise to every reader
    - a "no claim" sentence contains a number, a widening word or a name not in the draft
    - a CHANGES quote isn't in the draft, or a "removed" quote is still in the revision

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import os
import re
import sys

WIDENING = ["every", "everyone", "everybody", "everything", "all", "always", "never", "each", "most",
            "clients", "customers", "owners", "restaurants", "merchants", "team", "guarantee", "guaranteed",
            "nobody", "no one", "whole", "entire", "only", "fastest", "best", "leading"]
BAD_LINE = re.compile(r"provisional|assumed|\bTBD\b|needs substantiation|not yet substantiated|unconfirmed claim", re.I)
BAD_SECTION = re.compile(r"^#+\s*(needs substantiation|restricted|price history)", re.I)
NOT_FACTS = ("voice.md", "rules.md")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[*_`#>\[\]]", "", s)
    return re.sub(r"[\s\-–—]+", " ", s.lower()).strip(" .,:;!?\"'")


def units(text):
    """Sentences, headings and list items of the revision, minus greetings, sign-offs and hashtag lines."""
    out = []
    for line in text.splitlines():
        line = line.strip()
        if not line or re.match(r"^(#\w+\s*)+$", line) or line == "---":
            continue
        line = re.sub(r"^(subject\s*:\s*|#+\s*|[-*]\s+)", "", line, flags=re.I)
        for part in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(\[])", line):
            if len(re.findall(r"\w+", part)) > 3:
                out.append(part.strip())
    return out


def numbers(s):
    return {n.replace(",", "") for n in re.findall(r"\d[\d,.]*\d|\d", s)}


DETERMINERS = {"the", "a", "an", "your", "our", "their", "his", "her", "its", "my", "this", "that", "these", "those",
               "one", "every", "each", "per", "on", "of", "with", "and"}
GENERIC = {"message", "messages", "note", "step", "time", "question", "questions", "call", "chat", "reply", "look",
           "way", "thing", "things", "day", "week", "today", "tomorrow", "link", "details", "detail", "doc", "email",
           "post", "page", "site", "inbox", "calendar invite", "minute", "minutes", "chance", "idea", "start", "end",
           "same", "rest", "most", "lot", "bit", "own", "back", "next", "other", "new", "more", "less", "first", "last",
           "best", "good", "great", "real", "right", "few", "many", "much", "all", "it", "you", "me", "us", "them",
           "is", "are", "was", "be", "to", "for", "in", "at", "by", "from", "or", "not", "no", "so", "if", "as", "up"}


def stem(w):
    w = w.lower().strip("'s")
    return w[:5] if len(w) > 5 else w


def fact_terms(s):
    """Content words in the noun phrases of a sentence: up to two words after a determiner or preposition."""
    toks = re.findall(r"[A-Za-z&%][\w&%'-]*", s.replace("’", "'"))
    out = set()
    for i, t in enumerate(toks):
        if t.lower() in DETERMINERS:
            for nxt in toks[i + 1:i + 3]:
                n = nxt.lower()
                if n in DETERMINERS or n in GENERIC or len(n) < 3:
                    break
                out.add(n)
    return out


COMMON_VERBS = set("""has have had gives give gave shows show showed works work worked covers cover will would can could
should may might must means mean understands understand gets get got keeps keep does do did makes make made takes take
took sends send sent sees see saw knows know knew helps help needs need wants want uses use used goes go went comes come
lets let runs run puts put says say said finds find tells tell feels feel becomes become stays stay starts start brings
bring includes include adds add pays pay costs handles handle offers offer""".split())


def words_of(s):
    return re.findall(r"[A-Za-z&%][\w&%'-]*", s.replace("’", "'"))


def missing_terms(unit, evidence, vocabulary):
    """Fact terms the sources use elsewhere, appearing in this sentence but not in its own evidence (a swapped noun)."""
    ev = {stem(w) for w in words_of(evidence)}
    caps = {w.lower() for w in words_of(unit) if w[0].isupper() and not w.isupper()}
    return sorted(t for t in fact_terms(unit)
                  if t not in COMMON_VERBS and t not in caps and stem(t) in vocabulary and stem(t) not in ev)


def widening(s):
    low = " " + re.sub(r"\bevery (day|week|month|year|morning|night|plan)\b", "", norm(s)) + " "
    return {w for w in WIDENING if f" {w} " in low}


def brand_line_ok(path, quote):
    """Return (found, problem) for a quote inside a brand file."""
    if not os.path.isfile(path):
        return False, f"{os.path.basename(path)} doesn't exist"
    section = ""
    for line in read(path).splitlines():
        if line.startswith("#"):
            section = line
        if norm(quote) and norm(quote) in norm(line):
            if BAD_SECTION.match(section):
                return True, f"it's under '{section.strip('# ')}' in {os.path.basename(path)}"
            if BAD_LINE.search(line):
                return True, f"that line in {os.path.basename(path)} isn't confirmed"
            m = re.search(r"[\"“]([^\"”]+)[\"”]", line)
            if m and norm(quote) in norm(m.group(1)):
                speaker = {w for w in re.findall(r"\b[A-Z][a-z]+\b", line[:m.start()])}
                return True, ("QUOTE", speaker)
            return True, None
    return False, f"not found word for word in {os.path.basename(path)}"


def parse_trace(text):
    trace, changes, mode = [], [], None
    for line in text.splitlines():
        s = line.strip()
        if re.match(r"^TRACE\b", s):
            mode = "trace"
            continue
        if re.match(r"^CHANGES\b", s):
            mode = "changes"
            continue
        if not s.startswith("-") or mode is None:
            continue
        s = s[1:].strip()
        if mode == "trace":
            m = re.match(r'^["“](.+?)["”]\s*\|\s*(.+)$', s)
            if m:
                trace.append((m.group(1), m.group(2)))
        else:
            m = re.match(r'^(removed|changed|added|kept)\s*:\s*["“](.+?)["”]', s, re.I)
            if m:
                changes.append((m.group(1).lower(), m.group(2)))
    return trace, changes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("revision")
    ap.add_argument("--trace", required=True)
    ap.add_argument("--original", required=True)
    ap.add_argument("--brand", default="")
    a = ap.parse_args()
    try:
        revision, draft, trace_text = read(a.revision), read(a.original), read(a.trace)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    revision = re.split(r"(?m)^---\s*\n(?=\s*\*\*Verdict)", revision)[0]
    trace, changes = parse_trace(trace_text)
    if not trace:
        print("FAIL trace: no TRACE lines found")
        return 1
    findings = []
    fail = lambda msg: findings.append(("FAIL", msg))
    sources = draft
    if a.brand and os.path.isdir(a.brand):
        for name in os.listdir(a.brand):
            if name.endswith(".md") and name not in NOT_FACTS:
                sources += "\n" + read(os.path.join(a.brand, name))
    vocabulary = {stem(w) for w in words_of(sources)}

    for unit in units(revision):
        nu = norm(unit)
        entries = [(q, ev) for q, ev in trace if norm(q) and (norm(q) in nu or nu in norm(q))]
        if not entries:
            fail(f"untraced sentence: \"{unit[:70]}\"")
            continue
        evidence_text = ""
        for q, ev in entries:
            if norm(ev) == "no claim":
                extra = (numbers(unit) - numbers(draft)) | {w for w in widening(unit) if w not in widening(draft)}
                names = {n for n in re.findall(r"(?<=[a-z,] )[A-Z][a-z]+", unit) if n.lower() not in draft.lower()}
                if extra or names:
                    fail(f"marked 'no claim' but adds {', '.join(sorted(extra | names))}: \"{unit[:60]}\"")
                evidence_text = None
                break
            for src, quote in re.findall(r"(draft|brand/[\w.-]+)\s*:\s*[\"“](.+?)[\"”]", ev):
                if src == "draft":
                    if norm(quote) not in norm(draft):
                        fail(f"evidence not in the draft: \"{quote[:60]}\"")
                        continue
                else:
                    fname = src.split("/", 1)[1]
                    if fname in NOT_FACTS:
                        fail(f"{fname} is voice guidance, not a fact: \"{quote[:50]}\" can't support a claim")
                        continue
                    found, problem = brand_line_ok(os.path.join(a.brand, fname), quote)
                    if isinstance(problem, tuple):
                        speaker = problem[1]
                        if not (re.search(r"[\"“]", unit) or any(w in unit for w in speaker)):
                            fail(f"a customer's words support only a sentence that quotes or names them: \"{unit[:60]}\"")
                            continue
                        problem = None
                    if problem:
                        fail(f"evidence \"{quote[:50]}\": {problem}")
                        continue
                evidence_text += " " + quote
        if evidence_text is None:
            continue
        if not evidence_text.strip():
            fail(f"no usable evidence for: \"{unit[:70]}\"")
            continue
        new_nums = numbers(unit) - numbers(evidence_text)
        new_wide = widening(unit) - widening(evidence_text)
        if new_nums:
            fail(f"number(s) {', '.join(sorted(new_nums))} not in the evidence for: \"{unit[:60]}\"")
        if new_wide:
            fail(f"widened ('{', '.join(sorted(new_wide))}' isn't in the evidence): \"{unit[:60]}\"")
        swapped = missing_terms(unit, evidence_text, vocabulary)
        if swapped:
            fail(f"term(s) {', '.join(swapped)} not in this sentence's evidence: \"{unit[:60]}\"")

    for kind, quote in changes:
        if kind in ("removed", "changed") and norm(quote) not in norm(draft):
            fail(f"CHANGES quotes text that isn't in the draft: \"{quote[:60]}\"")
        elif kind == "removed" and norm(quote) in norm(revision):
            fail(f"CHANGES says removed, but it's still in the revision: \"{quote[:60]}\"")

    for level, msg in findings:
        print(f"{level} {msg}")
    n = len(findings)
    print(f"{'FAIL' if n else 'PASS'}: {n} problem(s); {len(units(revision))} sentences, {len(trace)} trace lines, {len(changes)} changes")
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(main())
