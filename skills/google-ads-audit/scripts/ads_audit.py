#!/usr/bin/env python3
"""Compute every figure for a Google Ads audit from CSV exports. Read-only; standard library only.

Usage:
    python3 ads_audit.py EXPORT_DIR [--brand "tallyhouse,tally house"] [--irrelevant FILE]
                         [--days N] [--json OUT.json]

EXPORT_DIR holds CSV downloads from the Google Ads UI (campaigns, keywords, search terms, ads,
conversion actions, campaign settings, network segment, negative keywords, user locations).
Files are recognized by their columns, not their names. Title and date-range lines above the
header and "Total:" rows are handled.

--irrelevant FILE: one pattern per line (a word, phrase or full search term) judged irrelevant
for this business, optional "# reason". Matching is whole-word and case-insensitive.
Prints a plain-text report; --json writes every figure for the self-check.
"""
import argparse, csv, json, os, re, sys
from collections import defaultdict

JUNK = ["jobs", "job", "career", "careers", "salary", "salaries", "hiring", "internship", "course", "courses",
        "certification", "training", "template", "templates", "free", "login", "log in", "sign in", "diy",
        "pdf", "wikipedia", "definition", "meaning", "how to become"]
NON_OUTCOME_CATS = {"page view", "engagement", "other"}
NON_OUTCOME_WORDS = ["page view", "pageview", "scroll", "time on", "session", "video", "watched", "visit", "view"]
LEAD_CATS = {"submit lead form", "request quote", "book appointment", "sign-up", "contact", "qualified lead", "converted lead", "phone call", "purchase"}
SMART = ["target cpa", "target roas", "maximize conversions", "maximize conversion value"]
WEIGHTS = {"conversion_tracking": 20, "wasted_spend": 15, "match_types": 5, "budget": 8, "bid_strategy": 10,
           "quality_score": 8, "rsa_coverage": 6, "location": 8, "networks": 7, "brand_split": 5, "landing_pages": 8}
PTS = {"PASS": 1.0, "WARN": 0.5, "FAIL": 0.0}
MONTHS = "january february march april may june july august september october november december".split()
STOP = {"for", "and", "the", "with", "your", "near", "best", "software", "service", "services", "tool", "app"}


def num(v):
    if v is None:
        return None
    s = str(v).strip().replace(",", "").replace("$", "").replace("%", "").replace("<", "").replace(">", "").strip()
    if s in ("", "--", "-", " --"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def money(x): return f"${x:,.2f}"
def norm(h): return re.sub(r"\s+", " ", h.strip().lower())


def parse_date(s):  # "July 1, 2026" or "2026-07-01"
    m = re.match(r"([a-z]+)\s+(\d{1,2}),\s*(\d{4})", s.strip().lower())
    if m and m.group(1) in MONTHS:
        return int(m.group(3)), MONTHS.index(m.group(1)) + 1, int(m.group(2))
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s.strip())
    return (int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None

def days_between(a, b): return (__import__("datetime").date(*b) - __import__("datetime").date(*a)).days + 1


def load(path):
    rows = list(csv.reader(open(path, encoding="utf-8-sig", errors="replace")))
    hdr_i, dr = None, None
    for i, r in enumerate(rows[:6]):
        cells = [norm(c) for c in r]
        if len([c for c in cells if c]) >= 2 and any(c in cells for c in ("campaign", "search term", "conversion action", "keyword", "negative keyword", "country/territory (user location)", "country")):
            hdr_i = i
            break
        joined = " ".join(r)
        if " - " in joined and parse_date(joined.split(" - ")[0]):
            parts = joined.split(" - ")
            a, b = parse_date(parts[0]), parse_date(parts[1])
            if a and b:
                dr = (a, b)
    if hdr_i is None:
        return None
    hdr = [norm(c) for c in rows[hdr_i]]
    data = []
    for r in rows[hdr_i + 1:]:
        if not r or not any(c.strip() for c in r) or r[0].strip().lower().startswith("total"):
            continue
        data.append({hdr[j]: (r[j].strip() if j < len(r) else "") for j in range(len(hdr))})
    return {"path": path, "header": hdr, "rows": data, "daterange": dr}


def kind(t):
    h = set(t["header"])
    if "conversion action" in h:
        return "conversions"
    if "negative keyword" in h:
        return "negatives"
    if "search term" in h:
        return "search_terms"
    if any(x.startswith("headline") for x in h) or "ad type" in h:
        return "ads"
    if any("user location" in x for x in h) or ("country" in h and "campaign" not in h):
        return "locations"
    if any(x.startswith("network (") for x in h) or ("network" in h and "cost" in h):
        return "network"
    if "keyword" in h:
        return "keywords"
    if "location targeting" in h or ("networks" in h and "cost" not in h):
        return "settings"
    if "campaign" in h and "cost" in h:
        return "campaigns"
    return None


def g(r, *names):
    for n in names:
        if n in r and r[n] not in ("",):
            return r[n]
    return ""


def cost(r): return num(g(r, "cost", "spend")) or 0.0
def conv(r): return num(g(r, "conversions", "conv.")) or 0.0
def words(s): return re.findall(r"[a-z0-9']+", s.lower())


def has_phrase(term, pat):
    t, p = words(term), words(pat)
    return any(t[i:i + len(p)] == p for i in range(len(t) - len(p) + 1)) if p else False


def neg_blocks(term, neg, mt):
    mt = mt.lower()
    if "exact" in mt:
        return words(term) == words(neg)
    if "phrase" in mt:
        return has_phrase(term, neg)
    return set(words(neg)) <= set(words(term))


def check(status, figures, notes): return {"status": status, "figures": figures, "notes": notes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("export_dir")
    ap.add_argument("--brand", default="")
    ap.add_argument("--irrelevant")
    ap.add_argument("--days", type=int)
    ap.add_argument("--json")
    a = ap.parse_args()

    T = defaultdict(list)
    dr = None
    for root, _, files in os.walk(a.export_dir):
        for f in sorted(files):
            if f.lower().endswith(".csv"):
                t = load(os.path.join(root, f))
                if t and kind(t):
                    T[kind(t)].append(t)
                    dr = dr or t["daterange"]
    rows = {k: [r for t in v for r in t["rows"]] for k, v in T.items()}
    found = {k: [os.path.basename(t["path"]) for t in v] for k, v in T.items()}
    if not rows:
        print("NO DATA: no recognizable Google Ads CSV exports in", a.export_dir)
        sys.exit(2)

    days = a.days or (days_between(*dr) if dr else None)
    brand = [b.strip().lower() for b in a.brand.split(",") if b.strip()]
    camps = rows.get("campaigns", [])
    kws = rows.get("keywords", [])
    sts = rows.get("search_terms", [])
    total_cost = sum(cost(r) for r in camps) if camps else sum(cost(r) for r in kws or sts)
    total_conv = sum(conv(r) for r in camps) if camps else sum(conv(r) for r in kws or sts)
    total_val = sum(num(g(r, "conv. value")) or 0 for r in camps)
    C = {}
    out_c = [{"campaign": g(r, "campaign"), "budget_per_day": num(g(r, "budget")), "bid_strategy": g(r, "bid strategy type"),
              "target": g(r, "target cpa / roas", "target cpa", "target roas"), "cost": cost(r), "conversions": conv(r),
              "cpa_reported": round(cost(r) / conv(r), 2) if conv(r) else None} for r in camps]
    out = {"files": found, "date_range": dr, "days": days, "total_cost": round(total_cost, 2),
           "total_conversions": total_conv, "cpa_reported": round(total_cost / total_conv, 2) if total_conv else None,
           "conv_value": round(total_val, 2), "roas_reported_pct": round(100 * total_val / total_cost, 1) if total_cost and total_val else None, "campaigns": out_c}

    # 1 conversion tracking
    ca = rows.get("conversions", [])
    outcome_conv = None
    if ca:
        prim = [r for r in ca if "primary" in g(r, "action optimization", "include in \"conversions\"", "goal").lower() or g(r, "include in \"conversions\"").lower() == "yes"]
        bad, dupes, every, static = [], [], [], []
        for r in prim:
            cat, nm = g(r, "category").lower(), g(r, "conversion action").lower()
            if cat in NON_OUTCOME_CATS or (cat not in LEAD_CATS and any(w in nm for w in NON_OUTCOME_WORDS)):
                bad.append(r)
            if g(r, "count").lower() == "every" and cat in LEAD_CATS - {"purchase"}:
                every.append(r)
        groups = defaultdict(list)
        for r in prim:
            if r not in bad:
                groups[g(r, "category").lower()].append(r)
        for cat, rs in groups.items():
            if len(rs) > 1 and cat != "purchase":
                dupes.append(rs)
        for r in ca:
            v = g(r, "value", "value setting").lower()
            if "same value" in v or "default value" in v:
                static.append(r)
        ok = [r for r in prim if r not in bad]
        outcome_conv = sum(conv(r) for r in ok) - sum(sum(conv(x) for x in rs) - max(conv(x) for x in rs) for rs in dupes)
        st = "FAIL" if bad or dupes else ("WARN" if every or static or not prim else "PASS")
        fig = {"primary_actions": [(g(r, "conversion action"), g(r, "category"), conv(r)) for r in prim],
               "non_outcome_primary": [(g(r, "conversion action"), conv(r)) for r in bad],
               "possible_duplicates": [[(g(x, "conversion action"), g(x, "source"), conv(x)) for x in rs] for rs in dupes],
               "count_every_on_leads": [g(r, "conversion action") for r in every],
               "static_value_actions": [(g(r, "conversion action"), g(r, "value", "value setting")) for r in static],
               "primary_conversions_reported": sum(conv(r) for r in prim),
               "outcome_conversions_deduplicated": outcome_conv,
               "cpa_on_outcomes_deduplicated": round(total_cost / outcome_conv, 2) if outcome_conv else None}
        if dupes:
            fig["cpa_if_each_duplicate_counted_once_low_high"] = [round(total_cost / (outcome_conv - max(conv(x) for x in rs) + min(conv(x) for x in rs)), 2) for rs in dupes[:1]] + [fig["cpa_on_outcomes_deduplicated"]]
        notes = []
        if static:
            notes.append("Conversion value is a fixed assigned value, so any ROAS shown is assigned value / cost, not revenue.")
        C["conversion_tracking"] = check(st, fig, notes)
    else:
        C["conversion_tracking"] = check("NOT CHECKED", {}, ["No conversion actions export."])

    # confidence
    basis = outcome_conv if outcome_conv is not None else total_conv
    conf = "Low" if days is None else ("High" if days >= 60 and basis >= 30 else "Medium" if days >= 28 and basis >= 15 else "Low")
    out["confidence"] = conf
    out["confidence_basis"] = f"{days if days else 'unknown'} days, {basis:g} conversions (real outcomes, counted once)"

    # 2 wasted spend
    if sts:
        pats = []
        if a.irrelevant:
            for line in open(a.irrelevant, encoding="utf-8"):
                p = line.split("#")[0].strip().strip('"').lower()
                if p:
                    pats.append((p, line.split("#", 1)[1].strip() if "#" in line else ""))
        negs = rows.get("negatives", [])
        waste, review, unrev = [], [], []
        for r in sts:
            term = g(r, "search term")
            hit = next((p for p in JUNK if has_phrase(term, p)), None)
            mine = next((p for p, _ in pats if has_phrase(term, p) or term.lower() == p), None)
            if (hit and conv(r) == 0) or mine:
                blocked, near = None, []
                for n in negs:
                    nc = g(n, "campaign")
                    if nc and nc != g(r, "campaign"):
                        continue
                    nk, nm = g(n, "negative keyword"), g(n, "match type")
                    if neg_blocks(term, nk, nm):
                        blocked = f"{nk} ({nm})"
                    elif set(words(nk)) <= set(words(term)):
                        near.append(f"{nk} ({nm}, {g(n, 'level') or 'campaign'})")
                waste.append({"term": term, "campaign": g(r, "campaign"), "ad_group": g(r, "ad group"), "cost": cost(r),
                              "conversions": conv(r), "reason": "built-in: " + hit if hit and not mine else "judged: " + mine,
                              "suggested_negative": f'"{hit or mine}" phrase', "existing_negative_that_misses_it": near, "already_blocked_by": blocked})
            elif hit:
                review.append({"term": term, "campaign": g(r, "campaign"), "cost": cost(r), "conversions": conv(r), "modifier": hit})
            elif conv(r) == 0 and cost(r) > 0:
                unrev.append({"term": term, "campaign": g(r, "campaign"), "cost": cost(r)})
        wsum = round(sum(w["cost"] for w in waste), 2)
        stc = sum(cost(r) for r in sts)
        by_c = defaultdict(float)
        for w in waste:
            by_c[w["campaign"]] += w["cost"]
        share = wsum / stc if stc else 0
        st = "FAIL" if share >= 0.10 else ("WARN" if share >= 0.03 or unrev else "PASS")
        if not a.irrelevant and unrev:
            st = "WARN" if st == "PASS" else st
        C["wasted_spend"] = check(st, {"waste_total": wsum, "search_terms_cost": round(stc, 2), "waste_share_pct": round(100 * share, 1),
                                       "waste_by_campaign": {k: round(v, 2) for k, v in by_c.items()},
                                       "waste_terms": sorted(waste, key=lambda w: -w["cost"]),
                                       "junk_modifier_terms_with_conversions_review": review,
                                       "zero_conversion_terms_not_yet_judged": sorted(unrev, key=lambda u: -u["cost"])[:25],
                                       "zero_conversion_not_judged_cost": round(sum(u["cost"] for u in unrev), 2)},
                                  [] if a.irrelevant else ["Account-specific relevance not judged yet: review the zero-conversion list, write --irrelevant, rerun."])
    else:
        C["wasted_spend"] = check("NOT CHECKED", {}, ["No search terms export."])

    # 3 match types
    if kws:
        mt = defaultdict(float)
        for r in kws:
            mt[g(r, "match type", "keyword match type").lower().replace(" match", "") or "unknown"] += cost(r)
        kc = sum(mt.values())
        broad = mt.get("broad", 0) / kc if kc else 0
        manual = [g(r, "campaign") for r in (camps or rows.get("settings", [])) if g(r, "bid strategy type").lower() in ("manual cpc", "enhanced cpc", "maximize clicks")]
        broad_manual = round(sum(cost(r) for r in kws if "broad" in g(r, "match type").lower() and g(r, "campaign") in manual), 2)
        st = "FAIL" if broad_manual > 0.1 * kc or (broad > 0.6 and C["conversion_tracking"]["status"] == "FAIL") else ("WARN" if broad > 0.6 else "PASS")
        C["match_types"] = check(st, {"cost_by_match_type": {k: round(v, 2) for k, v in mt.items()}, "broad_share_pct": round(100 * broad, 1),
                                      "broad_cost_on_manual_or_click_bidding": broad_manual},
                                 ["Broad match relies on Smart Bidding and accurate conversions to choose queries."])
    else:
        C["match_types"] = check("NOT CHECKED", {}, ["No keywords export."])

    # 4 budget
    if camps and any(g(r, "search lost is (budget)") for r in camps):
        lim = []
        for r in camps:
            lb = num(g(r, "search lost is (budget)")) or 0
            if lb >= 10:
                cpa = cost(r) / conv(r) if conv(r) else None
                lim.append({"campaign": g(r, "campaign"), "lost_is_budget_pct": lb, "budget_per_day": num(g(r, "budget")),
                            "avg_spend_per_day": round(cost(r) / days, 2) if days else None, "cost": cost(r), "conversions": conv(r),
                            "cpa_reported": round(cpa, 2) if cpa else None})
        st = "FAIL" if any(l["lost_is_budget_pct"] >= 25 for l in lim) else ("WARN" if lim else "PASS")
        C["budget"] = check(st, {"budget_limited": lim, "account_cpa_reported": out["cpa_reported"]},
                            ["Before adding budget, move spend from waste in the same campaign. No conversion forecast is made."])
    else:
        C["budget"] = check("NOT CHECKED", {}, ["No 'Search lost IS (budget)' column."])

    # 5 bid strategy
    srcs = camps or rows.get("settings", [])
    if srcs and any(g(r, "bid strategy type") for r in srcs):
        if conf == "Low":
            C["bid_strategy"] = check("INSUFFICIENT DATA", {"days": days, "conversions": basis},
                                      ["Too little data for a verdict on bid strategy. Re-run with at least 30 days and 15 real conversions."])
        else:
            res, worst = [], "PASS"
            for r in camps:
                bs = g(r, "bid strategy type").lower()
                per30 = conv(r) / days * 30 if days else 0
                if any(s in bs for s in ("target cpa", "target roas")) and per30 < 15:
                    v = "FAIL"
                elif any(s in bs for s in SMART) and per30 < 15:
                    v = "WARN"
                elif any(s in bs for s in ("manual", "maximize clicks")) and per30 >= 30:
                    v = "WARN"
                else:
                    v = "PASS"
                res.append({"campaign": g(r, "campaign"), "bid_strategy": g(r, "bid strategy type"), "target": g(r, "target cpa / roas", "target cpa", "target roas"),
                            "conversions": conv(r), "conversions_per_30_days": round(per30, 1), "verdict": v})
                worst = min(worst, v, key=lambda x: PTS[x])
            notes = ["Rule of thumb used by this audit (not a Google requirement): target-based bidding wants 15+ conversions per 30 days per campaign."]
            if C["conversion_tracking"]["figures"].get("non_outcome_primary") or C["conversion_tracking"]["figures"].get("possible_duplicates"):
                notes.append("Campaign conversion counts include non-outcome or duplicate actions, so real volume is lower than shown.")
            C["bid_strategy"] = check(worst, {"campaigns": res}, notes)
    else:
        C["bid_strategy"] = check("NOT CHECKED", {}, ["No bid strategy column."])

    # 6 quality score
    qk = [r for r in kws if num(g(r, "quality score", "qual. score")) and cost(r) > 0]
    if qk:
        qc = sum(cost(r) for r in qk)
        wqs = sum(num(g(r, "quality score", "qual. score")) * cost(r) for r in qk) / qc
        low = sum(cost(r) for r in qk if num(g(r, "quality score", "qual. score")) <= 4)
        comp = {}
        for c in ("exp. ctr", "ad relevance", "landing page exp."):
            comp[c] = round(sum(cost(r) for r in qk if "below" in g(r, c).lower()), 2)
        lows = [(g(r, "campaign"), g(r, "ad group"), g(r, "keyword"), num(g(r, "quality score")), cost(r)) for r in qk if num(g(r, "quality score")) <= 4]
        st = "FAIL" if wqs < 5 or low / qc > 0.30 else ("PASS" if wqs >= 7 and low / qc < 0.10 else "WARN")
        C["quality_score"] = check(st, {"spend_weighted_qs": round(wqs, 1), "cost_on_qs_4_or_less": round(low, 2), "share_on_qs_4_or_less_pct": round(100 * low / qc, 1),
                                        "below_average_cost_by_component": comp, "low_qs_keywords": lows}, [])
    else:
        C["quality_score"] = check("NOT CHECKED", {}, ["No Quality Score column."])

    # 7 RSA coverage + 11 landing pages
    ads = rows.get("ads", [])
    agcost = defaultdict(float)
    for r in kws or sts:
        agcost[(g(r, "campaign"), g(r, "ad group"))] += cost(r)
    if ads:
        by_ag = defaultdict(list)
        for r in ads:
            by_ag[(g(r, "campaign"), g(r, "ad group"))].append(r)
        cov = []
        for k in sorted(set(by_ag) | set(agcost)):
            rs = [r for r in by_ag.get(k, []) if "responsive search" in g(r, "ad type").lower()]
            hcount = max((sum(1 for i in range(1, 16) if g(r, f"headline {i}")) for r in rs), default=0)
            dcount = max((sum(1 for i in range(1, 5) if g(r, f"description {i}")) for r in rs), default=0)
            strength = ", ".join(sorted({g(r, "ad strength") for r in rs})) or "--"
            issue = []
            if not rs:
                issue.append("no responsive search ad")
            else:
                if hcount < 8: issue.append(f"{hcount} of 15 headlines")
                if dcount < 3: issue.append(f"{dcount} of 4 descriptions")
                if "poor" in strength.lower(): issue.append("ad strength Poor")
            cov.append({"campaign": k[0], "ad_group": k[1], "rsas": len(rs), "headlines": hcount, "descriptions": dcount,
                        "ad_strength": strength, "cost": round(agcost.get(k, 0), 2), "issues": issue})
        bad = [c for c in cov if c["issues"] and c["cost"] > 0]
        st = "FAIL" if any("no responsive" in " ".join(c["issues"]) for c in bad) else ("WARN" if bad else "PASS")
        C["rsa_coverage"] = check(st, {"ad_groups": cov}, ["Audit rule of thumb: 8+ headlines and 3+ descriptions per ad group. Google allows up to 15 and 4."])
        lp = []
        for k, rs in by_ag.items():
            urls = sorted({g(r, "final url") for r in rs if g(r, "final url")})
            agk = [r for r in kws if (g(r, "campaign"), g(r, "ad group")) == k]
            kc = sum(cost(r) for r in agk)
            below = sum(cost(r) for r in agk if "below" in g(r, "landing page exp.").lower())
            isbrand = any(b.replace(" ", "") in k[1].lower().replace(" ", "") for b in brand) or k[1].lower() == "brand"
            for u in urls:
                path = re.sub(r"^https?://[^/]+", "", u).strip("/").lower()
                toks = {w for w in words(k[1]) if len(w) > 3 and w not in STOP}
                reasons = []
                lpbad = kc and below / kc >= 0.5
                if not path and not isbrand:
                    reasons.append("non-brand ad group sends traffic to the homepage")
                elif lpbad and path and toks and not any(t[:5] in path for t in toks) and not isbrand:
                    reasons.append(f"URL path '/{path}' shares no word with the ad group name")
                if lpbad:
                    reasons.append(f"Landing page exp. Below average on {100 * below / kc:.0f}% of the ad group's spend")
                if reasons:
                    lp.append({"campaign": k[0], "ad_group": k[1], "final_url": u, "cost": round(agcost.get(k, 0), 2), "reasons": reasons})
        st = "FAIL" if any(len(x["reasons"]) > 1 for x in lp) else ("WARN" if lp else "PASS")
        C["landing_pages"] = check(st, {"flagged": lp}, ["Flags are leads to check by opening the page, not proof of a mismatch."])
    else:
        C["rsa_coverage"] = check("NOT CHECKED", {}, ["No ads export."])
        C["landing_pages"] = check("NOT CHECKED", {}, ["No ads export (final URLs)."])

    # 8 location + 9 networks
    sets = rows.get("settings", [])
    if sets:
        interest = [g(r, "campaign") for r in sets if "interest" in g(r, "location targeting").lower()]
        targets = {x.strip().lower() for r in sets for x in re.split(r"[;|]", g(r, "locations")) if x.strip()}
        locs = rows.get("locations", [])
        outside = []
        if locs:
            for r in locs:
                ctry = g(r, "country/territory (user location)", "country", "location")
                if ctry.lower() not in targets:
                    outside.append((ctry, cost(r), conv(r)))
        osum = round(sum(o[1] for o in outside), 2)
        st = "FAIL" if interest and osum > 0 else ("WARN" if interest or osum else "PASS")
        C["location"] = check(st, {"presence_or_interest_campaigns": interest, "targeted_locations": sorted(targets),
                                   "cost_outside_targets": osum, "outside_rows": outside},
                              [] if locs else ["No user-locations export, so spend outside the targets can't be measured."])
        disp = [g(r, "campaign") for r in sets if "display" in g(r, "networks").lower()]
        part = [g(r, "campaign") for r in sets if "partner" in g(r, "networks").lower()]
        net = rows.get("network", [])
        seg = defaultdict(lambda: [0.0, 0.0])
        for r in net:
            n = g(r, "network (with search partners)", "network").lower()
            key = "search_partners" if "partner" in n else ("display" if "display" in n else "google_search")
            seg[(g(r, "campaign"), key)][0] += cost(r)
            seg[(g(r, "campaign"), key)][1] += conv(r)
        segf = [{"campaign": k[0], "network": k[1], "cost": round(v[0], 2), "conversions": v[1]} for k, v in seg.items() if k[1] != "google_search"]
        pz = sum(s["cost"] for s in segf if s["network"] == "search_partners" and s["conversions"] == 0)
        dz = sum(s["cost"] for s in segf if s["network"] == "display")
        st = "FAIL" if disp or pz > 0 else ("WARN" if part else "PASS")
        C["networks"] = check(st, {"display_on_search_campaigns": disp, "search_partner_campaigns": part, "segments": segf,
                                   "partner_cost_zero_conversions": round(pz, 2), "display_cost": round(dz, 2),
                                   "partner_plus_display_cost": round(pz + dz, 2)},
                              [] if net else ["No network-segmented report, so partner and Display spend can't be measured."])
    else:
        C["location"] = check("NOT CHECKED", {}, ["No campaign settings export (locations, location option)."])
        C["networks"] = check("NOT CHECKED", {}, ["No campaign settings export (networks)."])

    # 10 brand split
    if brand and (kws or sts):
        src = kws or sts
        field = "keyword" if kws else "search term"
        per = defaultdict(lambda: {"brand_cost": 0.0, "brand_conv": 0.0, "nonbrand_cost": 0.0, "nonbrand_conv": 0.0})
        for r in src:
            isb = any(b.replace(" ", "") in g(r, field).lower().replace(" ", "") for b in brand)
            p = per[g(r, "campaign")]
            p["brand_cost" if isb else "nonbrand_cost"] += cost(r)
            p["brand_conv" if isb else "nonbrand_conv"] += conv(r)
        mixed = []
        for c, p in per.items():
            if p["brand_cost"] > 0 and p["nonbrand_cost"] > 0:
                bc = p["brand_cost"] / p["brand_conv"] if p["brand_conv"] else None
                nc = p["nonbrand_cost"] / p["nonbrand_conv"] if p["nonbrand_conv"] else None
                bl = (p["brand_cost"] + p["nonbrand_cost"]) / (p["brand_conv"] + p["nonbrand_conv"]) if p["brand_conv"] + p["nonbrand_conv"] else None
                mixed.append({"campaign": c, **{k: round(v, 2) for k, v in p.items()}, "brand_cpa": round(bc, 2) if bc else None,
                              "nonbrand_cpa": round(nc, 2) if nc else None, "blended_cpa": round(bl, 2) if bl else None})
        st = "FAIL" if any(m["brand_cpa"] and m["nonbrand_cpa"] and m["brand_cpa"] < 0.5 * m["nonbrand_cpa"] for m in mixed) else ("WARN" if mixed else "PASS")
        C["brand_split"] = check(st, {"brand_terms": brand, "mixed_campaigns": mixed, "basis": f"{field}s report (search-network spend only)"}, [])
    else:
        C["brand_split"] = check("NOT CHECKED", {}, ["No brand terms given (--brand)." if not brand else "No keywords or search terms export."])

    # score
    scored = {k: v for k, v in C.items() if v["status"] in PTS}
    den = sum(WEIGHTS[k] for k in scored)
    score = round(100 * sum(WEIGHTS[k] * PTS[v["status"]] for k, v in scored.items()) / den) if den else None
    grade = None if score is None else ("A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D" if score >= 40 else "F")
    out.update({"score": score, "grade": grade, "checks_scored": len(scored), "partial": len(scored) < 6, "checks": C})

    # print
    p = print
    p(f"FILES: " + "; ".join(f"{k}={','.join(v)}" for k, v in found.items()))
    p(f"DATE RANGE: {dr[0] if dr else '?'} to {dr[1] if dr else '?'} ({days or 'unknown'} days)")
    p(f"TOTALS: cost {money(total_cost)} · conversions {total_conv:g} · reported CPA {money(out['cpa_reported']) if out['cpa_reported'] else 'n/a'}"
      + (f" · conv. value {money(total_val)} · reported ROAS {out['roas_reported_pct']}%" if total_val else ""))
    for c in out_c:
        p(f"CAMPAIGN: {c['campaign']} · budget {c['budget_per_day']}/day · {c['bid_strategy']} {c['target']} · cost {money(c['cost'])} · conv {c['conversions']:g}")
    p(f"CONFIDENCE: {conf} ({out['confidence_basis']})")
    p(f"SCORE: {score if score is not None else 'n/a'}/100 grade {grade or 'n/a'} ({len(scored)} of 11 checks scored{'; PARTIAL' if out['partial'] else ''})")
    for k, v in C.items():
        p(f"\n[{v['status']}] {k} (weight {WEIGHTS[k]})")
        for fk, fv in v["figures"].items():
            p(f"  {fk}: {json.dumps(fv, default=str)}")
        for n in v["notes"]:
            p(f"  NOTE: {n}")
    if a.json:
        json.dump(out, open(a.json, "w", encoding="utf-8"), indent=1, default=str)
        p(f"\nJSON: {a.json}")


if __name__ == "__main__":
    main()
