#!/usr/bin/env python3
"""Check a Meta ads build file and export a bulk-upload style CSV. Standard library only.

Usage:
    python3 scripts/check_build.py ads/meta/<campaign>/build.md --brand brand/ [--csv ads/meta/<campaign>/ads.csv]

Checks (FAIL means rewrite before replying; WARN means judge it; OPEN is a fact only the user has):
  - required header lines, ad set fields and ad fields (see references/build-file.md)
  - headline <= 40 characters, description <= 30, primary text <= 2,200, the hook and the offer in the
    first 125 characters of the primary text, a real Meta CTA button
  - copy that asserts or implies a personal attribute (finances, health, age, religion, identity...)
  - policy-risk words, never-use words, brand-rule phrases, unconfirmed names, quotes not on record
  - every figure in the copy traced to FACTS or brand memory (and not to an unsubstantiated claim)
  - special ad categories: copy that looks like employment, housing, credit/financial or social issues
    with no category declared, and targeting the category doesn't allow (age, gender, radius, lookalikes)
  - custom audiences with no consent basis, or built from bought, rented, scraped or third-party lists
Exit code: 0 no FAIL, 1 FAIL, 2 bad input.
"""

import argparse
import csv
import os
import re
import sys

HEADER = ["campaign", "special ad category", "countries", "objective", "optimization event", "daily budget", "offer"]
ADSET_REQ = ["audience", "age", "gender", "location", "placements"]
AD_REQ = ["ad set", "concept", "hook", "primary text", "headline", "description", "cta button", "url", "format",
          "aspect ratios", "on screen"]
FIELDS = sorted(set(HEADER + ADSET_REQ + AD_REQ + [
    "status", "mode", "account", "landing page", "budget level", "detailed targeting", "detailed targeting exclusions",
    "custom audiences", "lookalikes", "exclusions", "budget", "proof used", "length", "notes", "fixes"]), key=len, reverse=True)
FIELD_RE = re.compile(r"^\s*(" + "|".join(re.escape(f) for f in FIELDS) + r")\s*:\s?(.*)$", re.I)

HEADLINE_MAX, DESC_MAX, PRIMARY_MAX, FOLD = 40, 30, 2200, 125
CTA_BUTTONS = {"apply now", "book now", "buy now", "call now", "contact us", "donate now", "download", "get access",
               "get directions", "get offer", "get promotions", "get quote", "get showtimes", "get started", "inquire now",
               "install now", "learn more", "listen now", "order now", "play game", "request time", "see menu",
               "send message", "send whatsapp message", "shop now", "sign up", "subscribe", "use app", "watch more",
               "book a test drive", "get updates", "see more"}
CATEGORIES = {"none": "none", "employment": "employment", "housing": "housing", "credit": "financial",
              "financial": "financial", "financial products and services": "financial",
              "social issues": "social", "social issues, elections or politics": "social", "politics": "social"}

ATTR = [
    (r"\b(are|were)\s+you\b[^.?!]{0,60}?\b(in debt|drowning|broke|bankrupt|struggling|poor|unemployed|depressed|anxious|"
     r"diabetic|overweight|obese|pregnant|gay|lesbian|bisexual|trans|christian|muslim|jewish|hindu|sikh|catholic|"
     r"single|divorced|over \d+|under \d+|in your \d0s|disabled|sick|addicted|an alcoholic|arrested|convicted|a felon|"
     r"black|latino|latina|asian|an immigrant|a senior|a veteran)\b", "asks whether the reader has a personal attribute"),
    (r"\byour\s+(debts?|credit score|bad credit|bankruptcy|diagnosis|depression|anxiety|weight|disability|illness|"
     r"medical condition|religion|faith|sexuality|sexual orientation|age|divorce|criminal record|arrest|"
     r"financial (struggles?|problems?|trouble|stress|situation)|money (problems?|troubles?)|cash[- ]flow (problems?|crunch|crisis))\b",
     "refers to the reader's own personal attribute"),
    (r"(^|[.!?]\s+)(struggling|drowning|tired of being|sick of being|behind on|buried in|can'?t afford|broke)\b[^.?!]*\?",
     "a question that implies the reader's situation"),
    (r"\b(drowning in debt|in debt\?|struggling (with|to pay) (your )?(cash|cash flow|money|debts?|bills|rent|payroll)|behind on (your )?(bills|rent|payments)|bad credit\??|people like you|"
     r"other (christians|muslims|jews|seniors|singles|moms|dads|veterans))\b", "implies the reader's personal attribute"),
]
AGE_GENDER_CODED = r"\b(young|youthful|energetic|digital natives?|recent grads?|mature|seasoned|guys|gals|ladies|" \
                   r"girls|boys|moms?|dads?|he or she|salesman|waitress|millennials?|gen z)\b"
RISK = r"\b(guarantee[ds]?|risk[- ]free|free money|get rich|cure[sd]?|miracle|#1|number one|best in|lose weight|" \
       r"before and after|no\.? ?1|100% (free|safe|effective)|act now|limited time|only \d+ (spots|left))\b"
CATEGORY_HINT = {
    "employment": r"\b(we'?re hiring|now hiring|job openings?|apply now|salary|per hour|careers?|join our team|position)\b",
    "housing": r"\b(apartments? for rent|for rent|home for sale|homes for sale|realtor|mortgage|condo|rental)\b",
    "financial": r"\b(loans?|line of credit|credit cards?|financing|apr\b|insurance|credit score|cash advance|mortgage)\b",
    "social": r"\b(vote|election|candidate|ballot|referendum|petition|legislation)\b",
}
FIGURE = re.compile(r"(?<![\w/])\$?\d[\d,]*(?:\.\d+)?\s?(?:%|k\b|x\b|\+)?(?:\s?(?:/|per\s)\s?\w+)?")
PLACEHOLDER = re.compile(r"\[[^\]]*(tbd|needed|link|url|placeholder|confirm)[^\]]*\]|TBD", re.I)
BAD_SOURCE = re.compile(r"\b(bought|purchased|rented|scraped|data vendor|list vendor|broker|third[- ]party list|"
                        r"patients?|partner'?s list|clinic'?s list|enriched)\b", re.I)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def section(text, heading):
    m = re.search(rf"^(#+)\s*{re.escape(heading)}\s*$", text, re.M | re.I)
    if not m:
        return ""
    rest = text[m.end():]
    stop = re.search(rf"^#{{1,{len(m.group(1))}}}\s", rest, re.M)
    return rest[:stop.start()] if stop else rest


def load_brand(path):
    b = {"corpus": "", "never": [], "banned": [], "unnamed": [], "files": {}}
    if not path or not os.path.isdir(path):
        return b
    for n in sorted(os.listdir(path)):
        if n.endswith(".md"):
            b["files"][n] = read(os.path.join(path, n))
    b["corpus"] = "\n".join(b["files"].values())
    for line in section(b["files"].get("voice.md", ""), "Words we never use").splitlines():
        line = re.sub(r"\[source:[^\]]*\]", "", line).strip("-* \t")
        b["never"] += [w.strip(" .") for w in line.split(",") if w.strip(" .")]
    for line in b["files"].get("rules.md", "").splitlines():
        if re.match(r"\s*-\s*(never|don'?t|do not|avoid)\b", line, re.I):
            b["banned"] += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line)
    for line in b["files"].get("proof.md", "").splitlines():
        if re.search(r"named:\s*(no|unconfirmed)", line, re.I):
            head = line.split(":")[0]
            b["unnamed"] += [n.strip() for n in re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", head)]
    return b


def parse_fields(lines):
    fields, cur = {}, None
    for line in lines:
        m = FIELD_RE.match(line)
        if m:
            cur = m.group(1).lower()
            fields[cur] = m.group(2).strip()
        elif cur and line.strip() and not line.startswith("#"):
            fields[cur] += "\n" + line.strip()
    return fields


def parse(text):
    parts = re.split(r"^##\s+(Ad set|Ad)\s*:\s*(.*)$", text, flags=re.M | re.I)
    head = parts[0]
    facts = ""
    m = re.search(r"^FACTS\s*$(.*?)(?=^OPEN\s*$|^##|\Z)", head, re.S | re.M)
    if m:
        facts = m.group(1)
    head_fields = parse_fields(head.split("FACTS")[0].splitlines())
    title = re.search(r"^#\s+(.*)$", head, re.M)
    if title and "campaign" not in head_fields:
        head_fields["campaign"] = re.sub(r"^meta build:\s*", "", title.group(1), flags=re.I)
    adsets, ads = [], []
    for i in range(1, len(parts), 3):
        kind, name, body = parts[i].lower(), parts[i + 1].strip(), parts[i + 2]
        f = parse_fields(body.splitlines())
        f["_name"] = name
        (adsets if kind == "ad set" else ads).append(f)
    return head_fields, facts, adsets, ads


def figure_ok(fig, known):
    digits = re.sub(r"[^\d.]", "", fig).strip(".")
    if re.search(r"\d\s?k\b", fig, re.I) and digits.isdigit():
        digits = str(int(digits) * 1000)
    if not digits:
        return "ok"
    hits = [l for l in known.splitlines() if re.search(rf"(?<![\d.]){re.escape(digits)}(?![\d])", l.replace(",", ""))
            and ("%" not in fig or "%" in l) and ("$" not in fig or "$" in l)]
    if not hits:
        return "missing"
    if all(re.search(r"needs substantiation|·\s*assumed|don'?t use|never", l, re.I) for l in hits):
        return "unsupported"
    return "ok"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--brand", default="brand" if os.path.isdir("brand") else None)
    ap.add_argument("--csv")
    a = ap.parse_args()
    try:
        text = read(a.file)
    except OSError as e:
        print(f"cannot read {a.file}: {e}")
        return 2
    brand = load_brand(a.brand)
    head, facts, adsets, ads = parse(text)
    known = facts + "\n" + brand["corpus"] + "\n" + "\n".join(v for k, v in head.items() if k != "offer")
    out = []
    add = lambda lvl, where, msg: out.append((lvl, where, msg))

    for k in HEADER:
        if not head.get(k):
            add("FAIL", "header", f"missing '{k.capitalize()}:' line")
    cat = CATEGORIES.get(head.get("special ad category", "").strip().lower().rstrip("."), None)
    if head.get("special ad category") and cat is None:
        add("WARN", "header", f"special ad category '{head['special ad category']}' not recognized "
                              "(none, employment, housing, financial products and services, social issues)")
    if re.search(r"link clicks?|landing page views?|impressions|reach", head.get("optimization event", ""), re.I) \
            and re.search(r"lead|sale|conversion|trial|sign", head.get("objective", "") + head.get("offer", ""), re.I):
        add("WARN", "header", "optimizing for clicks or views while the goal is a conversion")
    for k in ("daily budget", "optimization event", "countries", "landing page"):
        if PLACEHOLDER.search(head.get(k, "")):
            add("OPEN", "header", f"{k} not confirmed: {head[k]}")
    if not adsets:
        add("FAIL", "structure", "no '## Ad set:' blocks")
    if not ads:
        add("FAIL", "structure", "no '## Ad:' blocks")
    budget = re.search(r"\$?\s?([\d,]+(?:\.\d+)?)", head.get("daily budget", ""))
    if budget and len(adsets) > 2 and float(budget.group(1).replace(",", "")) < 150:
        add("WARN", "structure", f"{len(adsets)} ad sets on {head['daily budget']}: each may be too small to exit learning")

    # Ad sets
    for s in adsets:
        where = f"ad set '{s['_name']}'"
        for k in ADSET_REQ:
            if not s.get(k):
                add("FAIL", where, f"missing '{k.capitalize()}:'")
        aud = "\n".join(s.get(k, "") for k in ("custom audiences", "lookalikes", "exclusions", "audience"))
        for entry in re.split(r"\n|;", s.get("custom audiences", "") + "\n" + s.get("lookalikes", "")):
            e = entry.strip("-* ")
            if not e or re.match(r"^(none|n/?a|no)\b", e, re.I):
                continue
            if BAD_SOURCE.search(e) and not re.search(r"\b(not used|excluded from use|removed|dropped)\b", e, re.I):
                add("FAIL", where, f"audience built from data you don't have consent to use: \"{e[:80]}\"")
            elif s.get("custom audiences") and e in s.get("custom audiences", "") and not re.search(r"consent|pixel|website|visitors|engag|video view|lead form|seed", e, re.I):
                add("FAIL", where, f"custom audience with no consent basis recorded: \"{e[:80]}\"")
        if re.search(r"\b(debt relief|bankruptcy|payday|credit repair|disabilit|chronic|cancer|diabetes|depression|"
                     r"religio|sexual orientation|lgbt|ethnic)\w*", s.get("detailed targeting", "") + s.get("audience", ""), re.I):
            add("FAIL", where, "detailed targeting on a sensitive personal attribute")
        if cat and cat != "none":
            age = s.get("age", "").replace(" ", "").replace("–", "-")
            if age and not re.match(r"^(18-65\+?|18\+|all|18andover)", age, re.I):
                add("FAIL", where, f"age '{s['age']}' isn't allowed in a special ad category (use 18-65+)")
            if s.get("gender") and not re.match(r"^\s*all", s["gender"], re.I):
                add("FAIL", where, f"gender '{s['gender']}' isn't allowed in a special ad category (use all)")
            if s.get("lookalikes") and not re.match(r"^\s*(none|n/?a|no)\b", s["lookalikes"], re.I):
                add("FAIL", where, "lookalikes aren't available in a special ad category")
            if s.get("detailed targeting exclusions") and not re.match(r"^\s*(none|n/?a|no)\b", s["detailed targeting exclusions"], re.I):
                add("FAIL", where, "detailed targeting exclusions aren't allowed in a special ad category")
            for n, unit in re.findall(r"(\d+(?:\.\d+)?)\s*(km|kilometres|kilometers|mi|miles?)\b", s.get("location", ""), re.I):
                if (unit.lower().startswith("k") and float(n) < 25) or (unit.lower().startswith("mi") and float(n) < 15):
                    add("FAIL", where, f"radius {n} {unit} is under the 15-mile (25 km) minimum for a special ad category")
            if re.search(r"\b(postal|zip)\s*codes?\b", s.get("location", ""), re.I):
                add("FAIL", where, "postal or ZIP code targeting isn't allowed in a special ad category")

    # Ads
    for ad in ads:
        where = f"ad {ad['_name']}"
        for k in AD_REQ:
            if not ad.get(k):
                add("FAIL", where, f"missing '{k.capitalize() if k != 'cta button' else 'CTA button'}:'")
        pt, hl, ds = ad.get("primary text", ""), ad.get("headline", ""), ad.get("description", "")
        hook, cta = ad.get("hook", ""), ad.get("cta button", "").strip().lower().rstrip(".")
        if len(hl) > HEADLINE_MAX:
            add("FAIL", where, f"headline is {len(hl)} characters (max {HEADLINE_MAX}; it gets cut off in feed)")
        if len(ds) > DESC_MAX:
            add("FAIL", where, f"description is {len(ds)} characters (max {DESC_MAX})")
        if len(pt) > PRIMARY_MAX:
            add("FAIL", where, f"primary text is {len(pt)} characters (max {PRIMARY_MAX})")
        fold = pt[:FOLD].lower()
        if hook and hook.lower()[:40].strip(" .?!") not in fold and not hook.lower().startswith("[visual"):
            if hook.lower()[:40].strip(" .?!") not in pt.lower():
                add("WARN", where, "the hook line isn't in the primary text (fine for a video hook; check)")
            else:
                add("FAIL", where, f"the hook starts after character {FOLD}: front-load it")
        offer = head.get("offer", "").lower().strip()
        if offer and not PLACEHOLDER.search(offer):
            words = [w for w in re.findall(r"[a-z0-9$]+", offer) if len(w) > 3][:3] or [offer]
            if not all(w in fold for w in words):
                add("FAIL", where, f"the offer ('{head['offer']}') isn't in the first {FOLD} characters of the primary text")
        if cta and cta not in CTA_BUTTONS:
            add("FAIL", where, f"'{ad['cta button']}' isn't a Meta CTA button (for example Learn more, Sign up, Book now, Apply now)")
        copy = "\n".join([hook, pt, hl, ds, ad.get("on screen", "")])
        for pat, why in ATTR:
            m = re.search(pat, copy, re.I | re.M)
            if m:
                add("FAIL", where, f"personal attributes: \"{m.group(0).strip()[:60]}\" {why}")
        m = re.search(RISK, copy, re.I)
        if m:
            add("WARN", where, f"policy-risk wording \"{m.group(0)}\": keep only if it's literally true and on record")
        for kind, pat in CATEGORY_HINT.items():
            if re.search(pat, copy, re.I) and cat in (None, "none") and kind != cat:
                add("FAIL", where, f"copy looks like {'an' if kind[0] in 'aeiou' else 'a'} {kind} ad but no special ad category is declared")
        if cat == "employment":
            m = re.search(AGE_GENDER_CODED, copy, re.I)
            if m:
                add("FAIL", where, f"age- or gender-coded wording in a job ad: \"{m.group(0)}\"")
        for w in brand["never"]:
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", copy, re.I):
                add("FAIL", where, f"never-use word \"{w}\"")
        for p in brand["banned"]:
            pat = re.escape(p).replace(r"\-", "[- ]?").replace(r"\ ", r"[\s-]+")
            if re.search(pat, copy, re.I):
                add("FAIL", where, f"\"{p}\" is banned by a brand rule")
        for name in brand["unnamed"]:
            if name.lower() in copy.lower():
                add("FAIL", where, f"names {name}, but permission to name them isn't confirmed")
        words_copy = "\n".join([hook, pt, hl, ds])
        screen = re.sub(r"\b\d+(\.\d+)?\s*(-|to)\s*\d+(\.\d+)?\s*s(ec(onds?)?)?\b|\b\d+\s*s(ec(onds?)?)?\b|\b\d+:\d+\b", " ",
                        ad.get("on screen", ""))
        for q in re.findall(r"[\"“]([^\"”]{15,300})[\"”]", "\n".join([pt, hl, ds])):
            if re.sub(r"\W+", " ", q.lower()) not in re.sub(r"\W+", " ", known.lower()):
                add("FAIL", where, f"quote not on record word for word: \"{q[:60]}\"")
        if re.search(r"\b(testimonial|ugc|customer review|customer story)\b", ad.get("concept", ""), re.I) \
                and not ad.get("proof used", "").strip():
            add("FAIL", where, "a testimonial or UGC concept with no 'Proof used:' line tracing it to brand memory")
        overlay = " ".join(re.findall(r"[\"“]([^\"”]{1,120})[\"”]", screen)) + " " + " ".join(re.findall(r"\$\d[\d,.]*", screen))
        for m in FIGURE.finditer(words_copy + "\n" + overlay):
            fig = m.group(0).strip()
            if re.fullmatch(r"\d{1,2}:\d{1,2}", fig) or len(re.sub(r"\D", "", fig)) == 0:
                continue
            res = figure_ok(fig, known)
            if res == "missing":
                add("FAIL", where, f"figure \"{fig}\" isn't in FACTS or brand memory")
            elif res == "unsupported":
                add("FAIL", where, f"figure \"{fig}\" only traces to an unsubstantiated or banned claim")
        for m in PLACEHOLDER.finditer(copy + "\n" + ad.get("url", "")):
            add("OPEN", where, f"placeholder to fill before launch: {m.group(0)}")

    for lvl in ("FAIL", "WARN", "OPEN"):
        for l, w, msg in out:
            if l == lvl:
                print(f"{l:5} {w}: {msg}")
    fails = sum(1 for o in out if o[0] == "FAIL")
    print(f"\n{len(adsets)} ad set(s), {len(ads)} ad(s): {fails} FAIL, "
          f"{sum(1 for o in out if o[0] == 'WARN')} WARN, {sum(1 for o in out if o[0] == 'OPEN')} OPEN")

    if a.csv:
        by_name = {s["_name"]: s for s in adsets}
        cols = ["Campaign Name", "Special Ad Categories", "Campaign Objective", "Optimization Goal", "Countries",
                "Daily Budget", "Ad Set Name", "Location", "Age", "Gender", "Audience", "Custom Audiences",
                "Lookalikes", "Exclusions", "Placements", "Ad Name", "Body", "Title", "Link Description",
                "Call to Action", "Link", "Creative Format", "Aspect Ratios", "Creative Brief"]
        os.makedirs(os.path.dirname(os.path.abspath(a.csv)), exist_ok=True)
        with open(a.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for ad in ads:
                s = by_name.get(ad.get("ad set", "").strip(), adsets[0] if adsets else {})
                w.writerow([head.get("campaign", ""), head.get("special ad category", ""), head.get("objective", ""),
                            head.get("optimization event", ""), head.get("countries", ""), head.get("daily budget", ""),
                            s.get("_name", ""), s.get("location", ""), s.get("age", ""), s.get("gender", ""),
                            s.get("audience", ""), s.get("custom audiences", ""), s.get("lookalikes", ""),
                            s.get("exclusions", ""), s.get("placements", ""), ad["_name"], ad.get("primary text", ""),
                            ad.get("headline", ""), ad.get("description", ""), ad.get("cta button", ""), ad.get("url", ""),
                            ad.get("format", ""), ad.get("aspect ratios", ""), ad.get("on screen", "")])
        print(f"wrote {a.csv} ({len(ads)} rows)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
