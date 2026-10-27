#!/usr/bin/env python3
"""Check a Google Ads search campaign spec and write a Google Ads Editor import CSV. Standard library only.

Usage:
    python3 scripts/build_ads.py ads/google/<campaign>/campaign.json --brand brand/ [--planner research/kp.csv]

The spec format is in references/spec-format.md. The CSV is written beside the spec as editor-import.csv,
only when there are no BLOCKER lines. Everything is imported Paused.

Levels:
    BLOCKER  over character limits, duplicate headlines, too few headlines/descriptions, bad pins, superlatives
             or guarantees without an approved claim, exclamation marks in headlines, competitor names in ad text,
             never-use words, numbers in ad text not found in brand memory or the user's facts, numbers that brand
             memory says need substantiation or a rule forbids, volumes or CPCs with no planner file (or not
             matching it), negatives that block a positive keyword, missing landing pages
    FIX      Display or Search Partners on, 'presence or interest', fewer than 8 headlines, all headlines pinned,
             single-word broad keywords, duplicate keywords, competitor keywords outside a competitor campaign,
             budget split not matching the monthly budget, spelling convention, few assets, ALL CAPS words
    CLAIM    every number in ad text with the source line it matched (judge whether it fits this ad)
    INFO     keywords without planner data (unvalidated), counts

Exit code: 0 if no BLOCKER, 1 if any BLOCKER, 2 on bad input.
"""

import argparse
import csv
import json
import os
import re
import sys

LIMITS = {"headline": 30, "description": 90, "path": 15, "sitelink": 25, "sitelink_desc": 35, "callout": 25, "snippet": 25}
SNIPPET_HEADERS = {"amenities", "brands", "courses", "degree programs", "destinations", "featured hotels",
                   "insurance coverage", "models", "neighborhoods", "service catalog", "shows", "styles", "types"}
SUPERLATIVE = re.compile(r"#\s?1\b|\bno\.?\s?1\b|\bnumber one\b|\b(best|leading|top-rated|top rated|fastest|cheapest|"
                         r"lowest price|the only|most trusted|largest|award-winning|world-class|guarantee[ds]?|"
                         r"risk-free|100%)", re.I)
ACRONYMS = {"P&L", "POS", "CPA", "USA", "CAD", "USD", "SMS", "API", "CRM", "FAQ", "HST", "GST", "PST", "QBO", "AI"}
SPELLING = [("analyse", "analyze"), ("analysed", "analyzed"), ("colour", "color"), ("optimise", "optimize"),
            ("labour", "labor"), ("centre", "center"), ("organisation", "organization"), ("organise", "organize"),
            ("behaviour", "behavior"), ("favourite", "favorite"), ("cheque", "check"), ("licence", "license")]
WRONG_SPELLING = {
    "US": [b for b, _ in SPELLING],
    "Canadian": ["color", "labor", "center", "behavior", "favorite"],
    "UK": ["color", "labor", "center", "behavior", "favorite", "analyze", "optimize", "organization"],
}
NUM = re.compile(r"(?<![A-Za-z])\$?\d[\d,]*(?:\.\d+)?%?(?![A-Za-z])")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_brand(folder):
    """Return (lines [(file, text, section)], never_words, approved_claim_lines, competitors, spelling)."""
    lines, never, approved, comps, spelling = [], set(), [], set(), None
    if not folder or not os.path.isdir(folder):
        return lines, never, approved, comps, spelling
    for name in sorted(os.listdir(folder)):
        if not name.endswith(".md"):
            continue
        section = ""
        for raw in read(os.path.join(folder, name)).splitlines():
            if raw.startswith("#"):
                section = raw.lstrip("#").strip().lower()
                if name == "competitors.md" and raw.startswith("## "):
                    comps.add(raw[3:].strip())
                continue
            text = raw.strip()
            if not text:
                continue
            lines.append((name, text, section))
            body = re.sub(r"\[source:[^\]]*\]", "", text)
            if "never use" in section or "never-use" in section:
                for w in re.split(r",", body.lstrip("- ")):
                    if w.strip():
                        never.add(w.strip().lower())
            if name == "rules.md":
                for q in re.findall(r'[Nn]ever (?:describe|call|say)[^"]*"([^"]+)"', body):
                    never.add(q.lower())
            if name == "claims.md" and section.startswith("approved") and "TBD" not in text:
                approved.append(body)
            if name == "voice.md":
                if re.search(r"\bUS spelling\b|American spelling", body, re.I):
                    spelling = "US"
                elif re.search(r"Canadian spelling", body, re.I):
                    spelling = "Canadian"
                elif re.search(r"\bUK spelling\b|British spelling", body, re.I):
                    spelling = "UK"
    return lines, never, approved, comps, spelling


def norm_num(tok):
    return tok.replace("$", "").replace(",", "").rstrip("%").rstrip(".")


def planner_rows(path):
    rows = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            k = (r.get("Keyword") or r.get("keyword") or "").strip().lower()
            if k:
                rows[k] = r
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--brand", default="brand")
    ap.add_argument("--planner")
    ap.add_argument("--out", help="CSV path (default: editor-import.csv beside the spec)")
    a = ap.parse_args()
    try:
        spec = json.loads(read(a.spec))
    except (OSError, ValueError) as e:
        print(f"Can't read spec: {e}")
        return 2

    out = []
    add = lambda lvl, msg: out.append((lvl, msg))
    blines, never, approved, comps, brand_spelling = load_brand(a.brand)
    if not blines:
        add("INFO", "No brand memory found: every claim must come from the user's facts; mark the plan provisional")
    comps |= {c for c in spec.get("competitors", []) if c}
    spelling = spec.get("spelling") or brand_spelling
    user_facts = [str(x) for x in spec.get("user_facts", [])]
    planner_path = a.planner or spec.get("keyword_data")
    planner = None
    if planner_path:
        if os.path.exists(planner_path):
            planner = planner_rows(planner_path)
        else:
            add("BLOCKER", f"Keyword data file not found: {planner_path}")
    domain = (spec.get("domain") or "").lower().replace("https://", "").replace("http://", "").strip("/")

    def text_checks(where, text, kind):
        lim = LIMITS[kind]
        if len(text) > lim:
            add("BLOCKER", f"{where}: '{text}' is {len(text)} chars (limit {lim})")
        if not text.strip():
            add("BLOCKER", f"{where}: empty text")
        m = SUPERLATIVE.search(text)
        if m and not any(m.group(0).lower() in c.lower() for c in approved):
            add("BLOCKER", f"{where}: '{m.group(0)}' in '{text}' is a superlative, ranking or guarantee with no approved claim")
        if kind == "headline" and "!" in text:
            add("BLOCKER", f"{where}: exclamation mark in a headline ('{text}'); Google disapproves these")
        if "!!" in text or "??" in text:
            add("BLOCKER", f"{where}: repeated punctuation in '{text}'")
        if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text):
            add("BLOCKER", f"{where}: emoji or symbol in '{text}'")
        for c in comps:
            if re.search(rf"\b{re.escape(c)}\b", text, re.I):
                add("BLOCKER", f"{where}: competitor name '{c}' in ad text ('{text}')")
        for w in never:
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", text, re.I):
                add("BLOCKER", f"{where}: '{w}' is a word or phrase brand memory says never to use ('{text}')")
        for tok in re.findall(r"\b[A-Z]{4,}\b", text):
            if tok not in ACRONYMS:
                add("FIX", f"{where}: ALL CAPS '{tok}' (Google limits capitalization for emphasis)")
        if re.search(r"\bclick here\b", text, re.I):
            add("FIX", f"{where}: 'click here' is vague; name the action")
        if re.search(r"\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}", text):
            add("FIX", f"{where}: phone number in ad text; use a call asset instead")
        for bad in WRONG_SPELLING.get(spelling, []):
            if re.search(rf"\b{bad}\b", text, re.I):
                add("FIX", f"{where}: '{bad}' doesn't match the {spelling} spelling convention")
        for mt in NUM.finditer(text):
            tok = mt.group(0)
            n = norm_num(tok)
            if not n or n in ("0",):
                continue
            um = re.match(r"[\s/-]*(?:per\s+)?([A-Za-z]+)", text[mt.end():])
            unit = um.group(1).lower().rstrip("s") if um else ""
            unit = {"mo": "mo", "month": "mo", "hr": "h", "hour": "h", "min": "min", "minute": "min",
                    "yr": "y", "year": "y", "wk": "w", "week": "w"}.get(unit, unit)
            if unit in ("a", "an", "the", "and", "or", "to", "in", "for", "of"):
                unit = ""
            if unit:
                pat = re.compile(rf"(?<![\d.]){re.escape(n)}%?[\s/-]*(?:per\s+|a\s+)?{re.escape(unit)}", re.I)
            else:
                pat = re.compile(rf"(?<![\d.]){re.escape(n)}(?![\d])")
            hits = [(f, t, s) for f, t, s in blines if pat.search(t.replace(",", ""))]
            uhits = [u for u in user_facts if pat.search(u.replace(",", ""))]
            if not hits and not uhits:
                plain = re.compile(rf"(?<![\d.]){re.escape(n)}(?![\d])")
                near = [(f, t) for f, t, _ in blines if plain.search(t.replace(",", ""))] if unit else []
                if near:
                    add("BLOCKER", f"{where}: '{tok} {unit}' in '{text}' isn't how brand memory states it; closest: {near[0][0]}: {near[0][1][:140]}")
                else:
                    add("BLOCKER", f"{where}: '{tok}' in '{text}' is not in brand memory or the user's facts")
                continue
            unproven = re.compile(r"needs substantiation|not yet substantiated|see claims\.md|^-?\s*claimed:", re.I)
            bad = [h for h in hits if (h[0] == "claims.md" and "substantiation" in h[2]) or unproven.search(h[1]) or
                   (h[0] == "rules.md" and re.search(r"(don't|do not) use .*claim", h[1], re.I))]
            good = [h for h in hits if h not in bad and h[0] != "rules.md" and "confirmed" in h[1]]
            if bad and not good and not uhits:
                add("BLOCKER", f"{where}: '{tok}' in '{text}' matches a claim brand memory says can't be used yet: {bad[0][0]}: {bad[0][1][:140]}")
            unit = [h for h in hits if re.search(r"/location|per location|per rep|per user|per seat|per clinic", h[1], re.I)]
            if unit and len(unit) == len(hits) and not uhits and not re.search(r"location|rep|user|seat|clinic", text, re.I):
                add("FIX", f"{where}: '{tok}' is a per-unit price in brand memory ({unit[0][1][:90]}); say what it's per")
            src = f"{hits[0][0]}: {hits[0][1][:140]}" if hits else f"user: {uhits[0][:140]}"
            add("CLAIM", f"{where}: '{tok}' in '{text}' -> {src}")

    def url_check(where, url):
        if not url:
            add("BLOCKER", f"{where}: no landing page")
            return
        host = url.lower().replace("https://", "").replace("http://", "").split("/")[0]
        if domain and not (host == domain or host.endswith("." + domain)):
            add("BLOCKER", f"{where}: landing page {url} is not on {domain}")

    campaigns = spec.get("campaigns", [])
    if not campaigns:
        add("BLOCKER", "No campaigns in the spec")
    if not any(c.get("type") == "brand" for c in campaigns):
        add("INFO", "No brand campaign: say why in the plan (for example a budget too small, or a new brand)")
    monthly = spec.get("monthly_budget")
    daily_total = sum(float(c.get("daily_budget") or 0) for c in campaigns)
    if monthly:
        implied = round(daily_total * 30.4, 2)
        if abs(implied - float(monthly)) > 0.05 * float(monthly):
            add("FIX", f"Daily budgets total {daily_total:.2f}/day = {implied:.0f}/month, but the monthly budget is {monthly}")
        else:
            add("INFO", f"Daily budgets total {daily_total:.2f}/day, about {implied:.0f}/month (30.4 days)")
    shared = spec.get("shared_negatives", [])
    rows = []
    seen_kw = {}
    n_heads = n_kw = 0
    unvalidated = []

    def neg_blocks(neg, kw):
        nt, kt = neg["text"].lower().strip(), kw["text"].lower().strip()
        m = neg.get("match", "phrase").lower()
        if m == "exact":
            return nt == kt
        if m == "phrase":
            return re.search(rf"(?<!\S){re.escape(nt)}(?!\S)", kt) is not None
        return all(w in kt.split() for w in nt.split())

    for c in campaigns:
        cn = c.get("name", "?")
        nets = " ".join(c.get("networks", ["Google search"])).lower() if isinstance(c.get("networks"), list) else str(c.get("networks", "")).lower()
        if "display" in nets or "partner" in nets:
            add("FIX", f"{cn}: Display Network or Search Partners on; use Google Search only for a new search campaign")
        opt = str(c.get("location_option", "presence")).lower()
        if "interest" in opt:
            add("FIX", f"{cn}: location option is 'presence or interest'; use presence")
        if not c.get("locations"):
            add("BLOCKER", f"{cn}: no locations")
        if not c.get("languages"):
            add("FIX", f"{cn}: no languages set")
        applied = [s for s in shared if cn in s.get("campaigns", []) or s.get("campaigns") == ["all"] or
                   (s.get("campaigns") == ["non-brand"] and c.get("type") != "brand")]
        negs = list(c.get("negatives", [])) + [k for s in applied for k in s.get("keywords", [])]
        rows.append({"Campaign": cn, "Campaign Type": "Search", "Networks": "Google search",
                     "Budget": c.get("daily_budget", ""), "Budget type": "Daily",
                     "Bid Strategy Type": c.get("bid_strategy", ""), "Languages": ";".join(c.get("languages", [])),
                     "Campaign Status": "Paused"})
        for loc in c.get("locations", []):
            rows.append({"Campaign": cn, "Location": loc, "Targeting method": "Location of presence"})
        for n in c.get("negatives", []):
            rows.append({"Campaign": cn, "Keyword": n["text"], "Criterion Type": "Campaign Negative " + n.get("match", "phrase").title()})
        groups = c.get("ad_groups", [])
        if not groups:
            add("BLOCKER", f"{cn}: no ad groups")
        for g in groups:
            gn = f"{cn} > {g.get('name', '?')}"
            url_check(gn, g.get("landing_page"))
            rows.append({"Campaign": cn, "Ad Group": g.get("name", ""), "Ad Group Status": "Paused"})
            kws = g.get("keywords", [])
            if not kws:
                add("BLOCKER", f"{gn}: no keywords")
            for k in kws:
                n_kw += 1
                text, match = k["text"].strip(), k.get("match", "phrase").lower()
                if match not in ("exact", "phrase", "broad"):
                    add("BLOCKER", f"{gn}: '{text}' has match type '{match}'")
                key = (text.lower(), match)
                if key in seen_kw:
                    add("FIX", f"{gn}: '{text}' [{match}] duplicates {seen_kw[key]}")
                seen_kw[key] = gn
                if match == "broad" and len(text.split()) == 1:
                    add("FIX", f"{gn}: single-word broad keyword '{text}' will match far too widely")
                for comp in comps:
                    if comp.lower() in text.lower() and c.get("type") != "competitor":
                        add("FIX", f"{gn}: competitor keyword '{text}' belongs in its own competitor campaign, with the user's OK")
                for n in negs:
                    if neg_blocks(n, k):
                        add("BLOCKER", f"{gn}: negative '{n['text']}' [{n.get('match', 'phrase')}] blocks keyword '{text}'")
                has_data = any(k.get(f) not in (None, "") for f in ("volume", "cpc_low", "cpc_high"))
                prow = planner.get(text.lower()) if planner is not None else None
                if has_data and planner is None:
                    add("BLOCKER", f"{gn}: '{text}' has a volume or CPC but there's no keyword data file")
                elif has_data and prow is None:
                    add("BLOCKER", f"{gn}: '{text}' has a volume or CPC but isn't in the keyword data file")
                elif has_data:
                    for f, col in (("volume", "Avg. monthly searches"), ("cpc_low", "Top of page bid (low range)"),
                                   ("cpc_high", "Top of page bid (high range)")):
                        if k.get(f) not in (None, "") and norm_num(str(k[f])) != norm_num(str(prow.get(col, ""))):
                            add("BLOCKER", f"{gn}: '{text}' {f} {k[f]} doesn't match the file ({prow.get(col, '')})")
                if prow is None:
                    unvalidated.append(text)
                rows.append({"Campaign": cn, "Ad Group": g.get("name", ""), "Keyword": text, "Criterion Type": match.title(),
                             "Final URL": g.get("landing_page", "")})
            ads = g.get("ads", [])
            if not ads:
                add("BLOCKER", f"{gn}: no responsive search ad")
            for i, ad in enumerate(ads, 1):
                where = f"{gn} RSA {i}"
                hs, ds = ad.get("headlines", []), ad.get("descriptions", [])
                n_heads += len(hs)
                if not 3 <= len(hs) <= 15:
                    add("BLOCKER", f"{where}: {len(hs)} headlines (need 3-15)")
                elif len(hs) < 8:
                    add("FIX", f"{where}: only {len(hs)} headlines; aim for 10-15")
                if not 2 <= len(ds) <= 4:
                    add("BLOCKER", f"{where}: {len(ds)} descriptions (need 2-4)")
                seen = {}
                for j, h in enumerate(hs, 1):
                    t = h["text"] if isinstance(h, dict) else h
                    text_checks(f"{where} H{j}", t, "headline")
                    k2 = re.sub(r"[^a-z0-9]", "", t.lower())
                    if k2 in seen:
                        add("BLOCKER", f"{where}: H{j} '{t}' duplicates H{seen[k2]}")
                    seen[k2] = j
                for j, d in enumerate(ds, 1):
                    text_checks(f"{where} D{j}", d["text"] if isinstance(d, dict) else d, "description")
                pins = [h.get("pin") for h in hs if isinstance(h, dict) and h.get("pin")]
                dpins = [d.get("pin") for d in ds if isinstance(d, dict) and d.get("pin")]
                if any(p not in (1, 2, 3) for p in pins) or any(p not in (1, 2) for p in dpins):
                    add("BLOCKER", f"{where}: headline pins must be 1-3, description pins 1-2")
                if hs and len(pins) == len(hs):
                    add("FIX", f"{where}: every headline is pinned; pin only what must show")
                for p in set(pins):
                    if pins.count(p) == 1 and len(pins) > 0:
                        add("INFO", f"{where}: one headline pinned to position {p}; that text shows in every ad")
                for pk in ("path1", "path2"):
                    if ad.get(pk):
                        text_checks(f"{where} {pk}", ad[pk], "path")
                row = {"Campaign": cn, "Ad Group": g.get("name", ""), "Ad type": "Responsive search ad",
                       "Final URL": ad.get("final_url") or g.get("landing_page", ""), "Path 1": ad.get("path1", ""),
                       "Path 2": ad.get("path2", ""), "Status": "Paused"}
                for j, h in enumerate(hs, 1):
                    row[f"Headline {j}"] = h["text"] if isinstance(h, dict) else h
                    if isinstance(h, dict) and h.get("pin"):
                        row[f"Headline {j} position"] = h["pin"]
                for j, d in enumerate(ds, 1):
                    row[f"Description {j}"] = d["text"] if isinstance(d, dict) else d
                    if isinstance(d, dict) and d.get("pin"):
                        row[f"Description {j} position"] = d["pin"]
                rows.append(row)

    for s in shared:
        for k in s.get("keywords", []):
            rows.append({"Shared set": s.get("name", "Negatives"), "Keyword": k["text"],
                         "Criterion Type": "Negative " + k.get("match", "phrase").title()})
        targets = s.get("campaigns", [])
        if targets == ["all"]:
            names = [c.get("name", "") for c in campaigns]
        elif targets == ["non-brand"]:
            names = [c.get("name", "") for c in campaigns if c.get("type") != "brand"]
        else:
            names = [t for t in targets if any(t == c.get("name") for c in campaigns)]
            for t in targets:
                if t not in names:
                    add("BLOCKER", f"Shared list '{s.get('name')}' applies to '{t}', which isn't a campaign name")
        for n in names:
            rows.append({"Shared set": s.get("name", "Negatives"), "Campaign": n})

    assets = spec.get("assets", {})
    sl, co, sn = assets.get("sitelinks", []), assets.get("callouts", []), assets.get("snippets", [])
    if len(sl) < 4:
        add("FIX", f"{len(sl)} sitelinks; add at least 4")
    if len(co) < 4:
        add("FIX", f"{len(co)} callouts; add at least 4")
    for i, s in enumerate(sl, 1):
        text_checks(f"Sitelink {i}", s.get("text", ""), "sitelink")
        for dk in ("desc1", "desc2"):
            if s.get(dk):
                text_checks(f"Sitelink {i} {dk}", s[dk], "sitelink_desc")
        if bool(s.get("desc1")) != bool(s.get("desc2")):
            add("FIX", f"Sitelink {i}: give both description lines or neither")
        url_check(f"Sitelink {i}", s.get("url"))
        rows.append({"Campaign": s.get("campaign", ""), "Link Text": s.get("text", ""), "Description Line 1": s.get("desc1", ""),
                     "Description Line 2": s.get("desc2", ""), "Final URL": s.get("url", "")})
    for i, t in enumerate(co, 1):
        t = t["text"] if isinstance(t, dict) else t
        text_checks(f"Callout {i}", t, "callout")
        rows.append({"Callout text": t})
    for i, s in enumerate(sn, 1):
        if s.get("header", "").lower() not in SNIPPET_HEADERS:
            add("BLOCKER", f"Snippet {i}: header '{s.get('header')}' isn't one of Google's headers")
        vals = s.get("values", [])
        if len(vals) < 3:
            add("BLOCKER", f"Snippet {i}: needs at least 3 values")
        for v in vals:
            text_checks(f"Snippet {i}", v, "snippet")
        rows.append({"Header": s.get("header", ""), "Snippet Values": ";".join(vals)})

    if unvalidated:
        add("INFO", f"{len(unvalidated)} keywords unvalidated (no keyword data): mark them so in the plan")
    if not spec.get("conversion_actions") or not any(x.get("primary") for x in spec.get("conversion_actions", [])):
        add("FIX", "No primary conversion action named")

    order = {"BLOCKER": 0, "FIX": 1, "CLAIM": 2, "INFO": 3}
    out.sort(key=lambda x: order[x[0]])
    for lvl, msg in out:
        print(f"{lvl:8} {msg}")
    nb = sum(1 for l, _ in out if l == "BLOCKER")
    print(f"\nSUMMARY  {len(campaigns)} campaigns, {n_kw} keywords, {n_heads} headlines · "
          f"{nb} BLOCKER, {sum(1 for l, _ in out if l == 'FIX')} FIX")
    if nb:
        print("CSV not written: fix every BLOCKER first")
        return 1
    cols = []
    for r in rows:
        for k in r:
            if k not in cols:
                cols.append(k)
    path = a.out or os.path.join(os.path.dirname(os.path.abspath(a.spec)), "editor-import.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"CSV written: {path} ({len(rows)} rows, everything Paused)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
