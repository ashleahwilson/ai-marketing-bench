#!/usr/bin/env python3
"""Find disclosure triggers in a piece of marketing content and check whether a disclosure appears, and where.
Standard library only.

Usage:
    python3 scripts/disclosure_scan.py content/caption.md --channel social --brand brand/
    python3 scripts/disclosure_scan.py pricing-page.md --channel web

Channels: social, email, web, blog, ad, newsletter. Social captions are checked against a ~125-character "more" cut-off.

Prints:
    JURISDICTION   countries found in brand memory (or "unknown")
    HOUSE          disclosure wording from brand/rules.md
    TRIGGER        each trigger: affiliate link, sponsored/paid term, discount code, testimonial, price, fee,
                   trial or auto-renewal, contest, email, AI imagery; with line number
    FOUND          each disclosure found, with its position
    MISSING        a required element not found
    BURIED         a disclosure found in a place readers won't see it (after the links, after the cut-off,
                   inside a trailing hashtag block, in a footnote far from the price)
    PROOF          brand/proof.md lines that match a quoted person and mention a connection or incentive

Exit code: 0 if no MISSING or BURIED, 1 otherwise, 2 on bad input. The script finds patterns; judge every line.
"""

import argparse
import os
import re
import sys

CUTOFF = 125
AFFILIATE = re.compile(r"[?&](ref|aff|affiliate|affid|via|tag|partner|irclickid|clickid)=|/go/|/recommends/|/refer/|amzn\.to/", re.I)
CLEAR_AD = re.compile(r"(^|[\s·|(\[])(#?ad|#?sponsored|paid partnership|paid promotion|advertisement|sponsored by)(\b|$)", re.I)
WEAK_AD = re.compile(r"#(sp|spon|collab|partner|ambassador|thanks)\b|\bthanks to\b|\bin collaboration with\b", re.I)
AFFILIATE_DISC = re.compile(r"commission|affiliate|we may earn|we earn|paid if you buy|earn a fee", re.I)
PAID_TERMS = re.compile(r"\b(sponsored|paid partnership|paid post|flat fee|commission|gifted|free product|in exchange for|"
                        r"brand ambassador|#ad)\b", re.I)
CODE = re.compile(r"\b(use|with) (my |the )?code\b|\bpromo code\b|\bdiscount code\b|\bcode [A-Z0-9]{4,}\b", re.I)
QUOTE_ATTR = re.compile(r"^\s*>?\s*[—–-]{1,2}\s*([A-Z][\w'.-]+(?:\s+[A-Z][\w'.-]+)+)|[\"\u201d]\s*\(([A-Z][\w'.-]+)(?:\s+[A-Z][\w'.-]+)*,\s", re.M)
CONNECTION = re.compile(r"employee|works? (at|for)|staff|bookkeeper at|founder|investor|shareholder|family|friend|"
                        r"incentive|in exchange|free (months?|year|product|service)|received|gift card|discount|paid|commission|"
                        r"affiliate|closed in", re.I)
PRICE = re.compile(r"(from|starting at|starts at|as low as|only)?\s*\$\s?\d[\d,]*(\.\d\d)?\s*(/|per\s)?\s*(user|seat|location|month|mo|year|yr)?", re.I)
FROM_PRICE = re.compile(r"\b(from|starting at|starts at|as low as)\s*\$\s?\d", re.I)
BILLING = re.compile(r"billed (annually|yearly|monthly)|per year|/year|annual (plan|billing|commitment)|minimum \d+|min\. \d+|"
                     r"plus (tax|fees)|\+ ?(tax|fees)", re.I)
FEE = re.compile(r"(setup|set-up|onboarding|implementation|activation|service|processing|admin) fee|one-time \$|(?<!flat )\bfee\b", re.I)
NOTE_LINE = re.compile(r"^\s*(deal|source|note|internal|platform paid-partnership label)\b.*:", re.I)
TRIAL = re.compile(r"free (for )?\d+[- ]days?|\d+[- ]day free|free trial|try (it |\w+ )?free|start free|"
                   r"continues automatically|auto-?renew|renews automatically|billed automatically|no strings", re.I)
RENEW_PRICE = re.compile(r"(then|after (the|your) trial[^.]{0,40}?)\s*\$\s?\d|renews at \$|\$\s?\d[^.]{0,40}after (the|your) trial", re.I)
RENEW_WHEN = re.compile(r"(charged|billed|renews?) (on|at the end of|when|after) |day \d+|trial ends on|before the trial ends", re.I)
CANCEL = re.compile(r"cancel", re.I)
CONTEST = re.compile(r"\b(giveaway|give-away|contest|sweepstakes?|win a|win an|to enter|winner|prize|prize draw|draw (for|to win))\b", re.I)
CONTEST_REQ = {
    "no purchase necessary": re.compile(r"no purchase (is )?(necessary|required)", re.I),
    "skill-testing question (Canada)": re.compile(r"skill[- ]testing", re.I),
    "link to full rules": re.compile(r"(official |full )?rules|terms and conditions|t&cs?", re.I),
    "who can enter (eligibility)": re.compile(r"open to|residents of|eligib|must be \d+|18\+|age of majority", re.I),
    "closing date and time": re.compile(r"(closes|ends|deadline|until)\b[^.\n]{0,40}(\d{1,2}(:\d\d)?\s*(a\.?m\.?|p\.?m\.?)|[ap]m\b|ET|PT|EST|PST)", re.I),
    "odds / how the winner is chosen": re.compile(r"odds|chances of winning|depend on the number", re.I),
    "prize value": re.compile(r"(approximate|retail) value|valued at|value of \$|\$[\d,]+ value", re.I),
    "platform release (not sponsored by the platform)": re.compile(r"not (sponsored|endorsed|administered)|in no way (sponsored|associated)", re.I),
}
EMAIL_REQ = {
    "unsubscribe mechanism": re.compile(r"unsubscribe|opt[- ]out|reply \"?stop\"?|manage (your )?preferences|won't hear from", re.I),
    "physical mailing address": re.compile(r"\d+\s+\w+.*\b(st|street|ave|avenue|rd|road|blvd|suite|ste|way|dr|drive)\b.*", re.I),
}
FAKE_REPLY = re.compile(r"^subject:\s*(re|fwd?|fw):", re.I | re.M)
AI_IMAGE = re.compile(r"\b(generated|midjourney|dall-?e|stable diffusion|firefly|ai[- ]generated|ai image|synthetic|imagen|"
                      r"sora|runway|altered|retouched|face[- ]?swap)\b", re.I)
AI_LABEL = re.compile(r"ai-generated image|ai generated image|made with ai|generated with ai|digitally (created|altered)|ai info", re.I)
COUNTRIES = {"Canada": re.compile(r"\bCanad(a|ian)\b|\bOntario\b|\bToronto\b|\bVancouver\b|\bQuebec\b"),
             "US": re.compile(r"\b(US|USA|U\.S\.|United States|America)\b")}
HASHTAG = re.compile(r"#\w+")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def brand_info(brand):
    """Return (countries {name: file}, house wording lines, proof lines, offer text or None)."""
    countries, house, proof, offer = {}, [], [], None
    if not brand or not os.path.isdir(brand):
        return countries, house, proof, offer
    if os.path.exists(os.path.join(brand, "offer.md")):
        offer = read(os.path.join(brand, "offer.md"))
    for name in ("BRAND.md", "audiences.md", "senders.md", "offer.md", "proof.md"):
        p = os.path.join(brand, name)
        if os.path.exists(p):
            text = read(p)
            for c, rx in COUNTRIES.items():
                if c not in countries and rx.search(text):
                    countries[c] = name
    p = os.path.join(brand, "rules.md")
    if os.path.exists(p):
        section = ""
        for line in read(p).splitlines():
            if line.startswith("#"):
                section = line.lower()
            elif line.strip().startswith("-") and ("disclos" in section or re.search(r"disclos|label|#ad|sponsored|affiliate|unsubscribe|ai-generated", line, re.I)):
                house.append(line.strip("- ").strip())
    p = os.path.join(brand, "senders.md")
    if os.path.exists(p):
        for line in read(p).splitlines():
            if re.match(r"^\s*-\s*(mailing address|opt-out line|signature)\s*:", line, re.I) and "TBD" not in line:
                house.append("sender " + line.strip("- ").strip())
    p = os.path.join(brand, "proof.md")
    if os.path.exists(p):
        proof = [l.strip("- ").strip() for l in read(p).splitlines() if l.strip().startswith("-")]
    return countries, house, proof, offer


def caption_of(text):
    """For social posts: the text under a '## Caption' heading if there is one, else the whole text minus headings."""
    m = re.search(r"^#+\s*caption\s*$(.*?)(?=^#+\s|\Z)", text, re.I | re.M | re.S)
    body = m.group(1) if m else "\n".join(l for l in text.splitlines() if not l.startswith("#") and not re.match(r"^\w[\w -]*:\s", l))
    return body.strip()


def line_of(text, idx):
    return text.count("\n", 0, idx) + 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("piece")
    ap.add_argument("--channel", default="web", choices=["social", "email", "web", "blog", "ad", "newsletter"])
    ap.add_argument("--brand")
    a = ap.parse_args()
    if not os.path.exists(a.piece):
        print(f"ERROR: {a.piece} not found")
        return 2
    text = read(a.piece)
    out = []
    add = out.append

    countries, house, proof, offer = brand_info(a.brand)
    if countries:
        add("JURISDICTION  " + ", ".join(f"{c} (brand/{f})" for c, f in countries.items()))
    else:
        add("JURISDICTION  unknown: no countries in brand memory" + ("" if a.brand and os.path.isdir(a.brand) else " (no brand memory)")
            + ". Check against both Canada and the US, mark provisional, ask.")
    for h in house:
        add(f"HOUSE         {h}")

    # Affiliate links
    links = [(m.group(1), m.group(2), m.start()) for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text)]
    links += [("", m.group(0), m.start()) for m in re.finditer(r"(?<!\()https?://\S+", text) if not any(m.start() >= l[2] and m.start() < l[2] + len(l[0]) + len(l[1]) + 4 for l in links)]
    brand_name = ""
    if a.brand and os.path.exists(os.path.join(a.brand, "BRAND.md")):
        m = re.search(r"brand memory:\s*(\S+)", read(os.path.join(a.brand, "BRAND.md")), re.I)
        brand_name = m.group(1).lower() if m else ""
    def own_tag(u):
        host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0].lower()
        return bool(brand_name) and host.startswith(brand_name) and not re.search(r"/go/|/recommends/|/refer/", u, re.I)
    for t, u, i in links:
        if AFFILIATE.search(u) and own_tag(u):
            add(f"INFO          line {line_of(text, i)}: '{t or u}' is on the brand's own domain: a tracking tag, probably not an affiliate link")
    aff = [l for l in links if AFFILIATE.search(l[1]) and not own_tag(l[1])]
    for t, u, i in aff:
        add(f"TRIGGER       line {line_of(text, i)}: affiliate link '{t or u}' -> {u}")
    clean = [l for l in links if not AFFILIATE.search(l[1])]
    if aff:
        add("INFO          not affiliate (no tracking parameter): " + (", ".join(f"'{t or u}'" for t, u, _ in clean) or "none"))
        first = min(i for _, _, i in aff)
        discs = [m.start() for m in AFFILIATE_DISC.finditer(text)] + [m.start() for m in CLEAR_AD.finditer(text)]
        before = [d for d in discs if d < first]
        if before:
            add(f"FOUND         affiliate/paid disclosure at line {line_of(text, before[0])}, before the first affiliate link (line {line_of(text, first)})")
        elif discs:
            add(f"BURIED        affiliate disclosure at line {line_of(text, discs[0])} comes AFTER the first affiliate link (line {line_of(text, first)}); move it before")
        else:
            add("MISSING       affiliate disclosure (none found); place it before the first affiliate link")

    # Social placement
    if a.channel == "social":
        cap = caption_of(text)
        tags = HASHTAG.findall(cap)
        found_clear = list(CLEAR_AD.finditer(cap))
        tail = re.search(r"((?:#\w+\s*){3,})\s*$", cap)
        if found_clear:
            m = found_clear[0]
            pos = m.start(2)
            term = m.group(2)
            where = f"character {pos} of {len(cap)}"
            if term.startswith("#") and term in tags:
                where += f", hashtag {tags.index(term) + 1} of {len(tags)}"
            in_tail = tail and pos >= tail.start()
            if pos > CUTOFF or in_tail:
                add(f"BURIED        social disclosure '{term}' at {where}" + (" inside the trailing hashtag block" if in_tail else "")
                    + f"; past the ~{CUTOFF}-character 'more' cut-off. Put a clear disclosure at the start of the caption")
            else:
                add(f"FOUND         social disclosure '{term}' at {where}, before the ~{CUTOFF}-character cut-off")
        elif PAID_TERMS.search(text) or CODE.search(cap) or aff:
            add("MISSING       social disclosure: paid relationship or code present but no clear 'Ad' / 'Paid partnership' term")
        for m in WEAK_AD.finditer(cap):
            add(f"BURIED        ambiguous disclosure term '{m.group(0)}': not clear on its own")
        if re.search(r"paid[- ]partnership label:\s*on", text, re.I):
            add("FOUND         platform paid-partnership label: on")
        elif PAID_TERMS.search(text):
            add("INFO          platform paid-partnership label not mentioned: recommend turning it on as well")

    # Paid relationship and codes (any channel)
    for m in PAID_TERMS.finditer(text):
        add(f"TRIGGER       line {line_of(text, m.start())}: paid/sponsored term '{m.group(0)}'")
    for m in CODE.finditer(text):
        add(f"TRIGGER       line {line_of(text, m.start())}: discount or referral code '{m.group(0)}' (a material connection)")

    # Testimonials
    names = set()
    for m in QUOTE_ATTR.finditer(text):
        names.add((m.group(1) or m.group(2)).strip())
    for n in sorted(names):
        add(f"TRIGGER       testimonial attributed to '{n}'")
        first = n.split()[0]
        hits = [p for p in proof if first in p]
        if not proof:
            add(f"INFO          no brand/proof.md: can't check {n} for a connection")
        elif not hits:
            add(f"PROOF         '{n}' not found in brand/proof.md")
        for p in hits:
            flag = "connection or incentive recorded" if CONNECTION.search(p.split("]", 1)[-1]) else "no connection recorded"
            add(f"PROOF         {flag}: {p}")

    # Prices and fees
    seen = set()
    for m in FROM_PRICE.finditer(text):
        ln = line_of(text, m.start())
        if ln in seen:
            continue
        seen.add(ln)
        lines = text.splitlines()
        near = "\n".join(lines[max(0, ln - 2): ln + 1])
        if BILLING.search(near):
            add(f"FOUND         line {ln}: 'from' price with billing terms beside it")
        else:
            star = "*" in lines[ln - 1]
            foot = next((i + 1 for i, l in enumerate(lines) if i + 1 > ln and re.match(r"^\s*(<small>)?\s*\*(?!\*)", l)), None)
            if star and foot:
                add(f"BURIED        line {ln}: 'from' price; its terms are in a footnote at line {foot} ({foot - ln} lines away): '{lines[foot - 1].strip()}'")
            else:
                add(f"MISSING       line {ln}: 'from' price with no billing terms (billing period, minimums) beside it")
    seen = set()
    for m in FEE.finditer(text):
        ln = line_of(text, m.start())
        if ln in seen:
            continue
        seen.add(ln)
        ctx = text.splitlines()[ln - 1].strip()
        if NOTE_LINE.match(ctx):
            continue
        if re.search(r"\$\s?\d", ctx):
            add(f"TRIGGER       line {ln}: fee: '{ctx[:120]}' (a mandatory fee must be shown with the price, not only in an FAQ or footnote)")

    if offer is not None:
        for amt in sorted(set(re.findall(r"\$\s?\d[\d,]*(?:\.\d\d)?", text))):
            if NOTE_LINE.match(next((l for l in text.splitlines() if amt in l), "")):
                continue
            hit = next((l.strip("- ").strip() for l in offer.splitlines() if amt.replace(" ", "") in l), None)
            add(f"PRICE         {amt}: " + (f"in brand/offer.md: {hit[:140]}" if hit else "not found in brand/offer.md"))

    # Trials and auto-renewal
    trial = [m for m in TRIAL.finditer(text)]
    for m in trial:
        add(f"TRIGGER       line {line_of(text, m.start())}: trial / renewal term '{m.group(0)}'")
    if trial:
        if offer is not None and not re.search(r"trial", offer, re.I):
            add("MISSING       trial: no trial offer found in brand/offer.md (confirm it exists before promoting it)")
        if not RENEW_PRICE.search(text):
            add("MISSING       trial: the price charged after the trial")
        if not RENEW_WHEN.search(text):
            add("MISSING       trial: when the first charge happens")
        if not CANCEL.search(text):
            add("MISSING       trial: how to cancel before being charged")
        if re.search(r"no strings|no commitment|no catch", text, re.I) and re.search(r"card required|continues automatically|auto-?renew|fee", text, re.I):
            add("MISSING       trial: 'no strings / no commitment' sits beside a card requirement, auto-renewal or fee")

    # Contests
    if CONTEST.search(text):
        add(f"TRIGGER       line {line_of(text, CONTEST.search(text).start())}: contest or giveaway")
        for k, rx in CONTEST_REQ.items():
            add(("FOUND         contest: " if rx.search(text) else "MISSING       contest: ") + k)

    # Email
    if a.channel in ("email", "newsletter") or re.search(r"^subject:", text, re.I | re.M):
        for k, rx in EMAIL_REQ.items():
            add(("FOUND         email: " if rx.search(text) else "MISSING       email: ") + k)
        if FAKE_REPLY.search(text):
            add(f"MISSING       email: subject line '{FAKE_REPLY.search(text).group(0)}' implies an existing conversation (misleading)")
        if not re.search(r"^from:", text, re.I | re.M):
            add("MISSING       email: sender identification (From line)")

    # AI imagery
    seen = set()
    for m in AI_IMAGE.finditer(text):
        ln = line_of(text, m.start())
        if ln in seen:
            continue
        seen.add(ln)
        add(f"TRIGGER       line {ln}: AI-generated or altered imagery: '{text.splitlines()[ln - 1].strip()[:120]}'")
    if AI_IMAGE.search(text):
        add("FOUND         AI image label" if AI_LABEL.search(text) else "MISSING       AI image label (check brand rules for the required wording)")
        if names:
            add("INFO          a testimonial sits beside a generated image: check the person is real and recorded")

    for line in out:
        print(line)
    bad = any(l.startswith(("MISSING", "BURIED")) for l in out)
    print(f"SUMMARY       {sum(l.startswith('TRIGGER') for l in out)} triggers, "
          f"{sum(l.startswith('MISSING') for l in out)} missing, {sum(l.startswith('BURIED') for l in out)} buried")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
