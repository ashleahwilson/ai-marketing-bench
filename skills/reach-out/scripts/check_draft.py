#!/usr/bin/env python3
"""Mechanical checks for outreach drafts. Standard library only.

Usage:
    python3 scripts/check_draft.py drafts.txt
    python3 scripts/check_draft.py drafts.txt --facts          # check names/numbers against the FACTS block
    python3 scripts/check_draft.py drafts.txt --max-words 70   # user or profile word limit
    python3 scripts/check_draft.py drafts.txt --summary        # one-line result to paste into the reply
    cat drafts.txt | python3 scripts/check_draft.py -

File format: an optional ledger block, then messages, all separated by lines containing only ---.

    FACTS
    - prospect: Lakeshore plans to double technicians in Ontario | user
    - proof: Arctic Air (180 techs) cut unbilled return visits 31% | user
    ASSUMED
    - Lakeshore has under 500 employees | not given
    ---
    Channel: email            # email | linkedin-dm | connection   (default: email)
    Type: first               # first | follow-up | breakup        (default: inferred)
    Motion: event             # optional; "inbound", "event", "referral" or "champion" allow naming the shared context
    Subject: return visits at 2x

    Body text...
    ---
    Channel: email
    Type: follow-up
    Subject: Re: return visits at 2x

    Shorter follow-up...

Word counts measure the message itself: the greeting, signature block and opt-out line are excluded.
If Type is omitted, the first email is "first" and later emails are "follow-up".
Label the last step "Type: breakup" to get breakup length checks.

Exit code: 0 if no FAIL findings, 1 if any FAIL, 2 on bad input.
"""

import re
import sys

# --- Thresholds (and why) ---------------------------------------------------
# First touches that get replies cluster around 50-90 words in recent large
# samples; past ~110 they read as a pitch. Executives warrant under ~60.
FIRST_TARGET_MIN, FIRST_TARGET_MAX, FIRST_HARD_MAX = 50, 90, 110
# A closing note needs room for a sentence or two, not a new pitch.
BREAKUP_MIN, BREAKUP_MAX = 15, 50
# LinkedIn caps connection notes at 300 characters; first DMs read best under 500.
CONNECTION_MAX_CHARS, DM_MAX_CHARS = 300, 500
# Subjects that read like an internal note are 1-4 words; 5 is the outer edge.
SUBJECT_TARGET_MAX, SUBJECT_HARD_MAX = 4, 5

WARM_MOTIONS = ("inbound", "event", "referral", "champion", "reply")

OPENER_BANS = [
    (r"\bcongrat", "congratulation as the opener", "champion"),
    (r"\bi (just )?(noticed|saw)\b", "'I noticed / I saw' opener", "warm"),
    (r"\bcame across\b", "'came across' opener", None),
    (r"\bhope (this|you|all)\b.*\b(finds|well|great)\b", "greeting filler", None),
    (r"\b(i'?m|i am|i wanted to|just) reach(ing)? out\b", "'reaching out' opener", None),
    (r"\bquick question\b", "'quick question' opener", None),
    (r"\bmy name is\b", "self-introduction opener", None),
]

TRACKING = [
    (r"\b(visited|visiting|were on|been on|browsing|checked out) (our|the) (site|website|pricing|page|blog)", "names a website visit"),
    (r"\bchecked (us|our \w+) out\b", "names a website visit"),
    (r"\b(saw|noticed|see) (that )?you (liked|commented|reacted|viewed|visited|downloaded|were researching|have been researching|are researching)", "surveillance framing"),
    (r"\bviewed (my|your) profile\b", "names a profile view"),
    (r"\b(g2|bombora|6sense|builtwith|intent data|intent signal|technographic)\b", "names a tracking or data source"),
    (r"\byour team (has been|is|was) researching\b", "names intent research"),
    (r"\b(our data|we can see|we see|looks like) (shows? )?(you|your team|that you)\b", "reports an observation about them"),
]

FOLLOWUP_FILLER = [
    r"\bjust following up\b", r"\bfollowing up on my\b", r"\bcircling back\b", r"\bbumping (this|that)\b",
    r"\btouching base\b", r"\bdid you (get|have) a chance\b", r"\bchecking in\b", r"\bjust wanted to follow up\b",
]

STOCK = [
    "streamline", "unlock", "leverage", "seamless", "game-changer", "game changer", "fast-paced",
    "navigate the complexities", "elevate", "robust", "cutting-edge", "synergy", "supercharge",
    "revolutionize", "revolutionise", "empower", "best-in-class", "world-class", "delve",
]

INTERNAL_CAVEATS = [
    r"\bsame thread\b", r"\bdifferent angle\b", r"\bnew angle\b", r"\bstep \d\b", r"^\s*(follow-?up|breakup|touch \d)\s*:",
    r"\btreat (this|it|its \w+) as\b", r"\bnot a forecast\b", r"\bfor reference only\b", r"\btodo\b",
    r"\[(check|confirm|verify|tbd|company|product)[^\]]*\]", r"\bplaceholder\b", r"\bif (this|that) (exists|is true)\b",
]

# "the NetSuite move", "the raise", "the go-live": claims knowledge of their specific event.
DEFINITE_EVENT = r"\bthe (?:[A-Z][\w-]+ )?(move|migration|go-live|golive|switch|raise|round|launch|rollout|reorg|acquisition|implementation)\b"
SUBJECT_EVENT = r"\b(congrat\w*|raise|raised|series [a-e]|funding|round|acquisition|new role|promotion)\b"
OPT_OUT = r"(unsubscribe|opt[ -]?out|rather not hear|won'?t follow up|reply (with )?[\"“']?(no|stop)|not the right person|isn'?t relevant)"
ROLE_ECHO = r"\bas (the|a|an) (vp|vice president|head|director|ceo|cfo|cto|coo|cmo|cro|founder|manager|leader)\b"

COMMON_SUBJECT_STARTS = {"quick", "a", "an", "the", "your", "our", "following", "checking", "hello", "hi",
                         "introducing", "intro", "one", "idea", "thoughts", "question", "time"}

# Capitalised words that are not names needing a source.
NAME_ALLOW = {
    "i", "i'm", "i'd", "i'll", "i've", "hi", "hey", "hello", "dear", "thanks", "thank", "best", "cheers", "regards",
    "re", "fwd", "ps", "linkedin", "email", "ai", "ok", "okay", "yes", "no", "monday", "tuesday", "wednesday",
    "thursday", "friday", "saturday", "sunday", "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december", "q1", "q2", "q3", "q4", "ceo", "cfo", "cto",
    "coo", "cmo", "cro", "vp", "sdr", "sdrs", "crm", "roi", "saas", "b2b", "us", "uk", "eu", "your", "name", "role",
}

GREETING = re.compile(r"^\s*((hi|hey|hello|dear|good (morning|afternoon))\b[^,\n]{0,40}|[A-Z][\w'’-]{0,30})\s*[,!]?\s*$", re.I)
SKIP_NUMBER_LINE = re.compile(r"(\bstreet\b|\bst\.|\bave\b|\bavenue\b|\broad\b|\brd\.|\bsuite\b|\bblvd\b|po box|\baddress\b|https?://|www\.|@)", re.I)
SKIP_NUMBER = re.compile(r"^\d{1,2}(:\d\d)?\s?(am|pm)$|^\d{1,2}:\d\d$", re.I)


def word_count(s):
    return len(re.findall(r"[A-Za-z0-9'’]+", s))


def sentences(s):
    parts = re.split(r"(?<=[.!?])\s+|\n+", s.strip())
    return [p for p in parts if re.search(r"\w", p)]


def strip_greeting(body):
    lines = body.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and GREETING.match(lines[0]) and word_count(lines[0]) <= 5:
        lines.pop(0)
    elif lines:
        lines[0] = re.sub(r"^\s*(hi|hey|hello|dear)\s+[\w'’-]+\s*,\s*", "", lines[0], flags=re.I)
    return "\n".join(lines)


SIGNATURE_START = re.compile(r"^\s*(\[?your name\]?|best|thanks|thank you|cheers|regards|kind regards|warmly|--)\b|^\s*[A-Z][\w'’-]+( [A-Z][\w'’-]+)?\s*,?\s*$", re.I)


def strip_signature(body):
    """Cut the signature block (sign-off, name, title, address) so word targets measure the message itself."""
    lines = body.splitlines()
    for idx in range(1, len(lines)):
        if SIGNATURE_START.match(lines[idx]) and any(re.search(r"\w", l) for l in lines[:idx]):
            return "\n".join(lines[:idx])
    return body


def drop_optout_sentences(text):
    """Remove opt-out sentences (not whole paragraphs) so they don't count as the message or its ask."""
    kept = []
    for line in text.splitlines():
        parts = re.split(r"(?<=[.!?])\s+", line)
        parts = [p for p in parts if not re.search(OPT_OUT, p.lower()) and not re.match(r"^\s*not the right person\??\s*$", p, re.I)]
        kept.append(" ".join(parts))
    return "\n".join(kept)


def message_text(body):
    """The message itself: no greeting, signature block or opt-out sentence."""
    return strip_signoff(drop_optout_sentences(strip_signoff(strip_signature(strip_greeting(body)))))


def strip_signoff(body):
    lines = [l for l in body.splitlines() if l.strip()]
    while lines and word_count(lines[-1]) <= 3 and "?" not in lines[-1]:
        lines.pop()
    return "\n".join(lines)


def split_blocks(text):
    return [b.strip("\n") for b in re.split(r"(?m)^---\s*$", text) if b.strip()]


def parse_ledger(block):
    """Return (facts_text, assumed_text) if the block is a FACTS ledger, else None."""
    if not re.match(r"^\s*facts\b", block, re.I):
        return None
    facts, assumed, mode = [], [], "facts"
    for line in block.splitlines():
        if re.match(r"^\s*facts\b", line, re.I):
            mode = "facts"
            continue
        if re.match(r"^\s*assumed\b", line, re.I):
            mode = "assumed"
            continue
        (facts if mode == "facts" else assumed).append(line)
    return "\n".join(facts), "\n".join(assumed)


def parse_message(block):
    headers, body, in_body = {}, [], False
    for line in block.splitlines():
        m = re.match(r"^(channel|type|subject|step|day|to|motion)\s*:\s*(.*)$", line, re.I)
        if not in_body and m:
            headers[m.group(1).lower()] = m.group(2).strip()
            continue
        if not in_body and not line.strip():
            if headers:
                in_body = True
            continue
        in_body = True
        body.append(line)
    return headers, "\n".join(body).strip()


def norm_num(tok):
    return tok.replace(",", "").rstrip(".").lower().lstrip("$").rstrip("%")


WORD_NUMBERS = {"two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
                "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "dozen": "12", "twenty": "20",
                "thirty": "30", "forty": "40", "fifty": "50", "hundred": "100"}
MULTIPLIERS = {"double": "2", "doubling": "2", "doubled": "2", "twice": "2", "triple": "3", "tripling": "3",
               "tripled": "3", "half": "50", "halved": "50"}


def ledger_numbers(facts):
    nums = {norm_num(t) for t in re.findall(r"\$?\d[\d,]*(?:\.\d+)?%?", facts)}
    low = facts.lower()
    for w, n in {**WORD_NUMBERS, **MULTIPLIERS}.items():
        if re.search(r"\b" + w + r"\b", low):
            nums.add(n)
    return nums


def unsourced_word_numbers(text, facts_nums):
    hits = []
    for w, n in WORD_NUMBERS.items():
        for m in re.finditer(r"\b" + w + r"\b", text, re.I):
            # "one" and small counts in idioms ("a couple", "two weeks") are left to judgment; flag counts of things
            nxt = text[m.end():m.end() + 20].lower()
            if re.match(r"\s+(day|days|week|weeks|month|months|minute|minutes|hour|hours|business days|steps|lines|questions)\b", nxt):
                continue
            if n not in facts_nums:
                hits.append(m.group(0))
    return hits


def unsourced_numbers(text, facts_nums):
    found = []
    text = re.sub(r"https?://\S+|www\.\S+|\S+@\S+", " ", text)
    for line in text.splitlines():
        if SKIP_NUMBER_LINE.search(line) and word_count(line) < 14:
            continue  # signature address lines
        for m in re.finditer(r"\$?\d[\d,]*(?:\.\d+)?%?(?:\s?(?:am|pm))?", line, re.I):
            tok = m.group(0).strip()
            if SKIP_NUMBER.match(tok):
                continue
            after = line[m.end():m.end() + 9].lower()
            if re.match(r"\s?(min|mins|minute|minutes)\b", after):
                continue  # a meeting length is an offer, not a claim
            if re.match(r"x\b", line[m.end():m.end() + 2].lower()) and norm_num(tok) in facts_nums:
                continue
            if norm_num(tok) not in facts_nums:
                found.append(tok)
    return found


def unsourced_names(text, facts_low):
    hits = []
    for sent in sentences(text):
        toks = re.findall(r"[A-Za-z][\w'’&-]*", sent)
        for i, t in enumerate(toks):
            if i == 0 or not t[0].isupper():
                continue
            t = re.sub(r"['’]s$", "", t)
            if t.lower() in NAME_ALLOW or t.lower() in facts_low:
                continue
            hits.append(t)
    return sorted(set(hits))


def subject_case_issue(subj):
    ws = re.findall(r"[A-Za-z0-9'’]+", subj)
    if not ws:
        return None
    caps = [w for w in ws if w[:1].isupper()]
    if len(ws) >= 3 and len(caps) == len(ws):
        return "subject is in Title Case"
    if ws[0][:1].isupper() and ws[0].lower() in COMMON_SUBJECT_STARTS:
        return "subject starts with a capitalised common word"
    return None


def check(messages, ledger=None, use_facts=False, max_words=None):
    findings = []
    prev_email_words, seen_first, any_optout, first_subject, any_cold = None, False, False, None, False
    facts_text = ledger[0] if ledger else ""
    facts_low = facts_text.lower()
    facts_nums = ledger_numbers(facts_text)

    if use_facts and ledger is None:
        findings.append((0, "WARN", "no FACTS block at the top of the file; add one so names and numbers can be traced"))

    for i, (h, body) in enumerate(messages, 1):
        add = lambda lvl, msg: findings.append((i, lvl, msg))
        channel = (h.get("channel") or "email").lower().replace(" ", "-")
        mtype = (h.get("type") or "").lower()
        motion = (h.get("motion") or "").lower()
        warm = motion.startswith(WARM_MOTIONS)
        if channel == "email" and not mtype:
            mtype = "follow-up" if seen_first else "first"
        if not body:
            add("FAIL", "empty body")
            continue
        low = body.lower()
        content = strip_signoff(strip_signature(strip_greeting(body)))
        content = drop_optout_sentences(content)
        content = strip_signoff(content)
        wc = word_count(content)
        sents = sentences(strip_greeting(body))
        first = sents[0].lower() if sents else ""
        if re.search(OPT_OUT, low):
            any_optout = True

        # Length
        if max_words and channel in ("email", "linkedin-dm", "linkedin", "dm") and wc > max_words:
            add("FAIL", f"{wc} words, over the --max-words limit of {max_words}")
        if channel == "email":
            if mtype == "first":
                if wc > FIRST_HARD_MAX:
                    add("FAIL", f"first email is {wc} words (target {FIRST_TARGET_MIN}-{FIRST_TARGET_MAX}, max {FIRST_HARD_MAX})")
                elif wc > FIRST_TARGET_MAX:
                    add("WARN", f"first email is {wc} words (target {FIRST_TARGET_MIN}-{FIRST_TARGET_MAX}); trim if you can")
                elif wc < FIRST_TARGET_MIN and not warm and not max_words:
                    add("WARN", f"first email is {wc} words (target {FIRST_TARGET_MIN}-{FIRST_TARGET_MAX}, or 35-60 for executives); fine if the reason and ask both land")
                if re.search(r"https?://|www\.", content):
                    add("WARN", "link in the first email; offer it and send on reply (deliverability)")
            elif mtype == "breakup":
                if wc > BREAKUP_MAX:
                    add("FAIL", f"closing email is {wc} words (max {BREAKUP_MAX})")
                elif wc < BREAKUP_MIN:
                    add("WARN", f"closing email is {wc} words (target {BREAKUP_MIN}-{BREAKUP_MAX})")
            if mtype in ("follow-up", "breakup") and prev_email_words is not None and wc >= prev_email_words:
                add("FAIL", f"{mtype} is {wc} words, not shorter than the previous email ({prev_email_words})")
            prev_email_words, seen_first = wc, True
        elif channel == "connection" and len(body) > CONNECTION_MAX_CHARS:
            add("FAIL", f"connection note is {len(body)} characters (LinkedIn max {CONNECTION_MAX_CHARS})")
        elif channel in ("linkedin-dm", "linkedin", "dm") and len(body) > DM_MAX_CHARS:
            add("FAIL", f"DM is {len(body)} characters (max {DM_MAX_CHARS})")

        # Subject
        subj = h.get("subject")
        if not warm:
            any_cold = True
        if channel == "email" and mtype == "first" and subj:
            first_subject = subj.strip().lower()
        if channel == "email" and mtype in ("follow-up", "breakup") and subj and first_subject:
            m_re = re.match(r"^\s*re\s*:\s*(.*)$", subj, re.I)
            if m_re and m_re.group(1).strip().lower() != first_subject:
                add("WARN", f"'{subj}' doesn't match the first email's subject ('{first_subject}'); the thread will break")
        if channel == "email" and mtype == "first":
            if not subj:
                add("WARN", "first email has no Subject line")
            elif re.match(r"^\s*(re|fwd?)\s*:", subj, re.I):
                add("FAIL", "first email uses Re:/Fwd: (fakes a thread)")
        if subj and not re.match(r"^\s*(re|fwd?)\s*:", subj, re.I):
            sw = len(re.findall(r"[A-Za-z0-9'’]+", subj))
            if sw > SUBJECT_HARD_MAX:
                add("FAIL", f"subject is {sw} words (target 1-{SUBJECT_TARGET_MAX}): '{subj}'")
            elif sw > SUBJECT_TARGET_MAX:
                add("WARN", f"subject is {sw} words (target 1-{SUBJECT_TARGET_MAX}): '{subj}'")
            issue = subject_case_issue(subj)
            if issue:
                add("WARN", f"{issue}: '{subj}'")
            if "!" in subj or "?" in subj:
                add("WARN", f"subject punctuation reads as marketing: '{subj}'")
            if re.search(SUBJECT_EVENT, subj, re.I) and not motion.startswith("champion"):
                add("WARN", f"subject names the event; lead with what it means instead: '{subj}'")

        # Opener
        for pat, label, exempt in OPENER_BANS:
            if (exempt == "warm" and warm) or (exempt == "champion" and motion.startswith("champion")):
                continue
            if re.search(pat, first):
                add("FAIL", f"opener: {label} -> '{sents[0][:80]}'")

        # Tracking language
        for pat, label in TRACKING:
            m = re.search(pat, low)
            if m:
                add("FAIL", f"{label}: '{m.group(0)}'")

        for pat in FOLLOWUP_FILLER:
            m = re.search(pat, low)
            if m:
                add("FAIL", f"empty follow-up phrase: '{m.group(0)}'")

        close = sentences(content)[-2:]
        if any(re.search(r"\bworth\b", s.lower()) for s in close):
            add("FAIL", "the close uses 'worth' ('worth a chat'); ask for the thing itself")

        q = content.count("?")
        if q > 1:
            add("WARN", f"{q} question marks; make sure there's one ask")

        toks = [w.lower() for w in re.findall(r"[A-Za-z'’]+", content)]
        you = sum(t in ("you", "your", "you're", "yours", "you’re") for t in toks)
        us = sum(t in ("i", "we", "our", "us", "me", "my", "i'm", "we're", "i’m", "we’re", "i've", "we've") for t in toks)
        if us > you:
            add("WARN", f"I/we ({us}) outnumber you/your ({you})")

        if re.search(r"\*\*|__|^#+\s|^\s*[-*•]\s|^\s*\d+[.)]\s", body, re.M):
            add("FAIL", "markdown or a bullet/numbered list in the body")
        dashes = body.count("—") + body.count(" -- ")
        if dashes > 1:
            add("WARN", f"{dashes} em dashes (target 0-1)")
        if "!" in content and mtype == "first":
            add("WARN", "exclamation mark in a first touch")

        m = re.search(DEFINITE_EVENT, content)
        if m and not warm:
            add("WARN", f"'{m.group(0)}' claims their specific event; write it as a pattern ('after a …') unless it's public and in the ledger")
        for pat in INTERNAL_CAVEATS:
            m = re.search(pat, low, re.M)
            if m:
                add("WARN", f"internal note left in prospect copy: '{m.group(0)}'")
        m = re.search(ROLE_ECHO, low)
        if m:
            add("WARN", f"describes the reader's role back to them: '{m.group(0)}'")
        hits = [b for b in STOCK if re.search(r"\b" + re.escape(b) + r"\b", low)]
        if hits:
            add("WARN", f"stock vocabulary: {', '.join(hits)}")
        if re.search(r"\{\{|\[(first ?name|company)\]", body, re.I):
            add("WARN", "unfilled merge field; fine in a template, never in a staged send")
        if re.search(r"\b(attached|attachment|see attached)\b", low):
            add("WARN", "mentions an attachment; link or send on reply instead")

        # Fact tracing
        if use_facts and ledger is not None:
            nums = unsourced_numbers(content + "\n" + (subj or ""), facts_nums)
            if nums:
                add("FAIL", f"number(s) not in FACTS: {', '.join(sorted(set(nums)))}")
            wnums = unsourced_word_numbers(content, facts_nums)
            if wnums:
                add("WARN", f"counted thing(s) not in FACTS, check the number is sourced: {', '.join(sorted(set(wnums)))}")
            names = unsourced_names(content, facts_low)
            if names:
                add("WARN", f"capitalised name(s) not in FACTS, check they're sourced: {', '.join(names)}")

    if messages and any_cold and not any_optout and any((h.get("channel") or "email").lower() == "email" for h, _ in messages):
        findings.append((0, "WARN", "no opt-out wording anywhere in the sequence (see send-gate.md)"))
    return findings


def main():
    args = sys.argv[1:]
    use_facts = "--facts" in args
    summary = "--summary" in args
    args = [a for a in args if a not in ("--facts", "--summary")]
    max_words = None
    if "--max-words" in args:
        i = args.index("--max-words")
        try:
            max_words = int(args[i + 1])
        except (IndexError, ValueError):
            print("--max-words needs a whole number, e.g. --max-words 70")
            return 2
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__)
        return 2
    try:
        text = sys.stdin.read() if args[0] == "-" else open(args[0], encoding="utf-8").read()
    except OSError as e:
        print(f"Cannot read input: {e}")
        return 2

    blocks = split_blocks(text)
    ledger = parse_ledger(blocks[0]) if blocks else None
    if ledger is not None:
        blocks = blocks[1:]
    messages = [parse_message(b) for b in blocks]
    if not messages:
        print("No messages found. Separate messages with a line containing only ---")
        return 2

    findings = check(messages, ledger, use_facts, max_words)
    fails = sum(f[1] == "FAIL" for f in findings)
    warns = sum(f[1] == "WARN" for f in findings)

    if summary:
        top = "; ".join(sorted({f[2].split(":")[0].split(" (")[0] for f in findings})[:3])
        status = "PASS" if not fails else "FAIL"
        print(f"check_draft: {status}, {len(messages)} message(s), {fails} fail, {warns} warn" + (f" ({top})" if top else ""))
        return 1 if fails else 0

    for g in [f for f in findings if f[0] == 0]:
        print(f"[{g[1]}] sequence: {g[2]}")
    for i, (h, body) in enumerate(messages, 1):
        label = h.get("channel", "email") + (f" / {h['type']}" if h.get("type") else "")
        mine = [f for f in findings if f[0] == i]
        status = "FAIL" if any(f[1] == "FAIL" for f in mine) else ("WARN" if mine else "OK")
        print(f"[{status}] message {i} ({label}, {word_count(message_text(body))} words)")
        for _, lvl, msg in mine:
            print(f"    {lvl}: {msg}")
    print(f"\n{len(messages)} message(s): {fails} FAIL, {warns} WARN")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
