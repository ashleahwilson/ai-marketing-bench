#!/usr/bin/env python3
"""Compute every number a Meta ads audit uses, from Ads Manager and Events Manager exports. Standard library only.

Usage:
    python3 scripts/meta_audit.py analyze EXPORTS... [--backend EVENT=COUNT] [--json OUT.json]
    python3 scripts/meta_audit.py score CHECKS.json
    python3 scripts/meta_audit.py verify AUDIT.md --metrics OUT.json [--allow 40] [--allow 25.00]

analyze  Reads CSV exports (files or folders) and recognises each by its headers: campaign, ad set and ad level
         performance, a day breakdown, a placement breakdown, a settings export (objective, special ad
         categories, optimization event, targeting) and an Events Manager export (event, connection, count).
         --backend Lead=190 compares Meta's count of an event with the business's own count (CRM, store, app).
score    Turns the ten check statuses (pass, warn, fail, blocker, na) into the 0-100 score and band.
verify   Lists every dollar figure, percentage and multiplier in the report that doesn't match a computed
         number (or an --allow value the user supplied). Exit 1 if any are untraced.
The ad set learning line uses Meta's published guideline of about 50 optimization events per ad set per week.
"""

import argparse
import csv
import datetime as dt
import glob
import json
import os
import re
import sys

LEARNING_EVENTS_PER_WEEK = 50  # Meta's published guideline, Business Help Centre "About the learning phase"
ALIASES = {
    "campaign": ["campaign name"], "adset": ["ad set name"], "ad": ["ad name"],
    "spend": ["amount spent", "spend"], "impressions": ["impressions"], "reach": ["reach"],
    "frequency": ["frequency"], "clicks": ["link clicks"], "results": ["results"],
    "indicator": ["result indicator", "result type"], "objective": ["objective", "campaign objective"],
    "attribution": ["attribution setting", "attribution spec"],
    "sac": ["special ad categories", "special ad category"],
    "sac_country": ["special ad category country", "special ad category countries"],
    "start": ["reporting starts"], "end": ["reporting ends"], "day": ["day", "date"],
    "placement": ["placement"], "platform": ["platform"],
    "opt_goal": ["optimization goal"], "event": ["custom event type", "conversion event", "optimized event"],
    "countries": ["countries", "locations"], "age_min": ["age min"], "age_max": ["age max"],
    "audiences": ["custom audiences", "audiences"], "adv_audience": ["advantage+ audience", "advantage audience"],
    "placements": ["placements"], "budget": ["daily budget", "ad set budget", "budget"],
    "format": ["format", "ad format", "creative type"],
    "headline": ["headline", "title"], "body": ["body", "primary text"],
    "ev_name": ["event name", "event"], "connection": ["connection", "connection method", "integration"],
    "ev_count": ["events received", "total events", "event count"],
    "ev_id": ["event id coverage", "event id sent"], "emq": ["event match quality"],
    "dataset": ["dataset", "dataset id", "pixel id", "pixel"],
    "delivery": ["campaign delivery", "ad set delivery", "ad delivery", "delivery"],
}
NOT_CONVERSION = re.compile(r"click|impression|reach|view|engagement|thruplay|landing|like|follow", re.I)
SAC_TERMS = {
    "employment": r"\bhiring\b|\bwe'?re hiring\b|\bjobs?\b|\bcareers?\b|\bapply now\b|\brecruit\w*|\bvacanc\w*|\bsalary\b|\bjoin our team\b|\bwanted\b",
    "housing": r"\brent(al|als)?\b|\bapartments?\b|\bcondos?\b|\breal estate\b|\bhomes? for sale\b|\blistings?\b",
    "credit / financial products": r"\bloans?\b|\bcredit cards?\b|\bfinancing\b|\bline of credit\b|\bmortgages?\b",
    "social issues, elections or politics": r"\bvote\b|\belection\w*|\bcandidate\b|\bballot\b|\bpetition\b",
}


def norm(h):
    h = re.sub(r"\([^)]*\)", "", h or "").strip().lower()
    return re.sub(r"\s+", " ", h)


def num(v):
    v = (v or "").strip().replace(",", "").replace("$", "").replace("%", "")
    try:
        return float(v)
    except ValueError:
        return 0.0


def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        return None
    heads = list(rows[0].keys())
    cmap = {}
    for key, names in ALIASES.items():
        for h in heads:
            if norm(h) in names and key not in cmap:
                cmap[key] = h
    cur = next((re.search(r"\(([A-Z]{3})\)", h).group(1) for h in heads if norm(h) in ALIASES["spend"] and re.search(r"\(([A-Z]{3})\)", h)), "")
    data = [{k: r.get(h, "") for k, h in cmap.items()} for r in rows]
    data = [d for d in data if any((v or "").strip() for v in d.values())]
    has = set(cmap)
    if {"ev_name", "connection"} <= has:
        kind = "events"
    elif "spend" not in has and ({"opt_goal", "sac", "event"} & has):
        kind = "settings"
    elif "day" in has:
        kind = "daily"
    elif {"placement", "platform"} & has:
        kind = "placement"
    elif "ad" in has:
        kind = "ad"
    elif "adset" in has:
        kind = "adset"
    elif "campaign" in has:
        kind = "campaign"
    else:
        kind = "unknown"
    return {"path": path, "kind": kind, "rows": data, "currency": cur}


def money(x):
    return f"${x:,.2f}"


def r2(x):
    return round(x + 0.0, 2)


def stats(rows, days):
    s = {k: sum(num(r.get(k)) for r in rows) for k in ("spend", "impressions", "clicks", "results", "reach")}
    out = {"spend": r2(s["spend"]), "impressions": int(s["impressions"]), "link_clicks": int(s["clicks"]),
           "results": int(s["results"])}
    out["cost_per_result"] = r2(s["spend"] / s["results"]) if s["results"] else None
    out["ctr_pct"] = r2(s["clicks"] / s["impressions"] * 100) if s["impressions"] else None
    out["cpm"] = r2(s["spend"] / s["impressions"] * 1000) if s["impressions"] else None
    out["cpc"] = r2(s["spend"] / s["clicks"]) if s["clicks"] else None
    if len(rows) == 1 and num(rows[0].get("frequency")):
        out["frequency"] = r2(num(rows[0].get("frequency")))
    elif s["reach"]:
        out["frequency"] = r2(s["impressions"] / s["reach"])
    if days:
        out["results_per_week"] = r2(s["results"] / days * 7)
    return out


def group(rows, key):
    g = {}
    for r in rows:
        g.setdefault((r.get(key) or "").strip(), []).append(r)
    return g


def period(files):
    starts, ends, daily = [], [], set()
    for f in files:
        for r in f["rows"]:
            for k, lst in (("start", starts), ("end", ends)):
                try:
                    lst.append(dt.date.fromisoformat((r.get(k) or "").strip()[:10]))
                except ValueError:
                    pass
            if f["kind"] == "daily" and r.get("day"):
                daily.add(r["day"].strip()[:10])
    if starts and ends:
        return str(min(starts)), str(max(ends)), (max(ends) - min(starts)).days + 1
    if daily:
        d = sorted(daily)
        return d[0], d[-1], len(d)
    return None, None, 0


def analyze(paths, backend):
    files = []
    for p in paths:
        for f in (sorted(glob.glob(os.path.join(p, "**", "*.csv"), recursive=True)) if os.path.isdir(p) else [p]):
            lf = load_csv(f)
            if lf:
                files.append(lf)
    by = {}
    for f in files:
        by.setdefault(f["kind"], []).extend(f["rows"])
    start, end, days = period(files)
    m = {"files": {os.path.basename(f["path"]): f["kind"] for f in files},
         "currency": next((f["currency"] for f in files if f["currency"]), "not stated"),
         "period": {"start": start, "end": end, "days": days}}
    top = by.get("campaign") or by.get("adset") or by.get("ad") or []
    conv_rows = [r for r in top if not NOT_CONVERSION.search(r.get("indicator") or "")]
    m["account"] = stats(top, days)
    m["conversion_results"] = int(sum(num(r.get("results")) for r in conv_rows))
    m["conversion_spend"] = r2(sum(num(r.get("spend")) for r in conv_rows))
    settings = by.get("settings", [])
    s_camp = {(r.get("campaign") or "").strip(): r for r in settings}
    s_adset = {(r.get("adset") or "").strip(): r for r in settings if r.get("adset")}
    total = m["account"]["spend"] or 1
    camps = []
    for name, rows in group(by.get("campaign") or top, "campaign").items():
        c = stats(rows, days)
        st = s_camp.get(name, {})
        c.update(name=name, objective=rows[0].get("objective") or st.get("objective") or "not in export",
                 result_indicator=rows[0].get("indicator") or "not in export",
                 special_ad_categories=(st.get("sac") or rows[0].get("sac") or "not in export"),
                 spend_share_pct=r2(c["spend"] / total * 100))
        camps.append(c)
    m["campaigns"] = sorted(camps, key=lambda c: -c["spend"])
    ads = by.get("ad", [])
    adsets = []
    for name, rows in group(by.get("adset", []), "adset").items():
        a = stats(rows, days)
        st = s_adset.get(name, {})
        mine = [x for x in ads if (x.get("adset") or "").strip() == name]
        a.update(name=name, campaign=rows[0].get("campaign", ""), attribution=rows[0].get("attribution") or st.get("attribution") or "not in export",
                 optimization=" / ".join(v for v in (st.get("opt_goal"), st.get("event")) if v) or "not in export",
                 ads=len(mine) if ads else None,
                 formats=sorted({(x.get("format") or "").strip() for x in mine if x.get("format")}),
                 spend_share_pct=r2(a["spend"] / total * 100))
        conv = not NOT_CONVERSION.search(rows[0].get("indicator") or "")
        a["learning_limited"] = bool(conv and days and a["results_per_week"] < LEARNING_EVENTS_PER_WEEK)
        for k in ("countries", "age_min", "age_max", "audiences", "adv_audience", "placements", "budget"):
            if st.get(k):
                a[k] = st[k]
        adsets.append(a)
    m["ad_sets"] = sorted(adsets, key=lambda a: -a["spend"])
    m["ad_sets_learning_limited"] = sum(1 for a in adsets if a["learning_limited"])
    m["attribution_settings"] = sorted({a["attribution"] for a in adsets} | {(r.get("attribution") or "").strip() for r in top if r.get("attribution")} - {"not in export", ""})
    m["ads"] = sorted([dict(stats([r], days), name=r.get("ad", ""), ad_set=r.get("adset", ""), format=r.get("format", ""))
                       for r in ads], key=lambda a: -a["spend"])
    m["formats"] = {f: sum(1 for a in ads if (a.get("format") or "").strip() == f) for f in sorted({(a.get("format") or "").strip() for a in ads} - {""})}
    m["trends"] = trends(by.get("daily", []))
    m["placements"] = placements(by.get("placement", []))
    m["events"] = events(by.get("events", []))
    m["backend"] = compare_backend(backend, m, by, s_adset)
    m["special_ad_category_flags"] = sac_flags(files, s_camp, s_adset)
    cr = m["conversion_results"]
    reasons = []
    if days < 14:
        reasons.append(f"{days} days of data")
    if cr < 30:
        reasons.append(f"{cr} conversions")
    if not reasons and (days < 28 or cr < 100):
        reasons.append(f"{days} days, {cr} conversions")
    level = "Low" if (days < 14 or cr < 30) else ("Medium" if (days < 28 or cr < 100) else "High")
    m["confidence"] = {"level": level, "reason": ", ".join(reasons) or f"{days} days, {cr} conversions"}
    return m


def trends(rows):
    out = []
    key = "adset" if any(r.get("adset") for r in rows) else "campaign"
    for name, rs in group(rows, key).items():
        days = sorted({(r.get("day") or "")[:10] for r in rs})
        if len(days) < 4:
            continue
        half = len(days) // 2
        first = [r for r in rs if (r.get("day") or "")[:10] in days[:half]]
        second = [r for r in rs if (r.get("day") or "")[:10] in days[-half:]]
        a, b = stats(first, 0), stats(second, 0)
        t = {"name": name, "first_half": f"{days[0]} to {days[half - 1]}", "second_half": f"{days[-half]} to {days[-1]}",
             "ctr_first_pct": a["ctr_pct"], "ctr_second_pct": b["ctr_pct"],
             "cpr_first": a["cost_per_result"], "cpr_second": b["cost_per_result"]}
        if a["ctr_pct"] and b["ctr_pct"] is not None:
            t["ctr_change_pct"] = r2((b["ctr_pct"] - a["ctr_pct"]) / a["ctr_pct"] * 100)
        if a["cost_per_result"] and b["cost_per_result"]:
            t["cpr_change_pct"] = r2((b["cost_per_result"] - a["cost_per_result"]) / a["cost_per_result"] * 100)
        out.append(t)
    return out


def placements(rows):
    out = {}
    for camp, rs in group(rows, "campaign").items():
        tot = stats(rs, 0)
        lst = []
        for (pf, pl), prs in sorted(group_two(rs).items()):
            p = stats(prs, 0)
            p.update(platform=pf, placement=pl, spend_share_pct=r2(p["spend"] / (tot["spend"] or 1) * 100))
            if p["cost_per_result"] and tot["cost_per_result"]:
                p["cpr_vs_campaign_x"] = r2(p["cost_per_result"] / tot["cost_per_result"])
            lst.append(p)
        out[camp or "account"] = {"total": tot, "rows": sorted(lst, key=lambda p: -p["spend"])}
    return out


def group_two(rows):
    g = {}
    for r in rows:
        g.setdefault(((r.get("platform") or "").strip(), (r.get("placement") or "").strip()), []).append(r)
    return g


def events(rows):
    out = []
    for name, rs in group(rows, "ev_name").items():
        conns = {}
        for r in rs:
            c = (r.get("connection") or "").strip().lower()
            k = "server" if "server" in c or "api" in c else "browser" if "browser" in c or "pixel" in c else c
            conns.setdefault(k, {"count": 0, "event_id_coverage_pct": [], "datasets": set()})
            conns[k]["count"] += int(num(r.get("ev_count")))
            if (r.get("ev_id") or "").strip():
                conns[k]["event_id_coverage_pct"].append(num(r.get("ev_id")))
            conns[k]["datasets"].add((r.get("dataset") or "").strip())
        datasets = sorted({(r.get("dataset") or "").strip() for r in rs} - {""})
        e = {"event": name, "datasets": datasets, "total_received": sum(c["count"] for c in conns.values())}
        for k, c in conns.items():
            e[k] = c["count"]
            if c["event_id_coverage_pct"]:
                e[f"{k}_event_id_coverage_pct"] = min(c["event_id_coverage_pct"])
        emq = [num(r.get("emq")) for r in rs if (r.get("emq") or "").strip()]
        if emq:
            e["event_match_quality"] = min(emq)
        flags = []
        if len(datasets) > 1:
            flags.append(f"received in {len(datasets)} datasets")
        if "browser" in conns and "server" in conns:
            cov = [e.get("browser_event_id_coverage_pct"), e.get("server_event_id_coverage_pct")]
            if any(c is None or c < 90 for c in cov):
                flags.append("browser and server both send it without event IDs on both: deduplication can't work")
        if "browser" in conns and "server" in conns and not any("deduplication" in f for f in flags):
            e["total_received"] = max(e["browser"], e["server"])  # deduplicated: the pair counts once
            e["total_note"] = "estimate: browser and server deduplicated, so the larger of the two; Events Manager shows the exact total"
        e["flags"] = flags
        out.append(e)
    return out


def compare_backend(backend, m, by, s_adset):
    out = []
    top = by.get("campaign") or by.get("adset") or by.get("ad") or []
    for item in backend or []:
        if "=" not in item:
            continue
        ev, n = item.split("=", 1)
        n = num(n)
        word = re.sub(r"[^a-z]", "", ev.lower())[:5]
        rows = [r for r in top if word and word in re.sub(r"[^a-z]", "", (r.get("indicator") or "").lower())]
        meta = sum(num(r.get("results")) for r in rows)
        spend = sum(num(r.get("spend")) for r in rows)
        e = next((x for x in m["events"] if x["event"].lower() == ev.lower()), None)
        row = {"event": ev, "business_count": int(n), "ads_manager_results": int(meta),
               "ads_manager_spend": r2(spend)}
        if n:
            row["ads_manager_vs_business_x"] = r2(meta / n)
            row["cost_per_result_reported"] = r2(spend / meta) if meta else None
            row["cost_per_business_conversion"] = r2(spend / n)
            if e:
                row["events_received_vs_business_x"] = r2(e["total_received"] / n)
        out.append(row)
    return out


def sac_flags(files, s_camp, s_adset):
    texts = {}
    for f in files:
        if f["kind"] in ("events", "daily", "placement"):
            continue
        for r in f["rows"]:
            c = (r.get("campaign") or "").strip()
            if c:
                texts.setdefault(c, set()).update(v for v in (r.get("campaign"), r.get("adset"), r.get("ad"), r.get("headline"), r.get("body")) if v)
    out = []
    for camp, ts in texts.items():
        blob = " | ".join(sorted(ts))
        declared = (s_camp.get(camp, {}).get("sac") or "").strip()
        for cat, rx in SAC_TERMS.items():
            hits = sorted({h.lower() for h in re.findall(rx, blob, re.I)})
            if hits:
                tgt = [{k: v for k, v in st.items() if k in ("adset", "age_min", "age_max", "audiences", "countries", "adv_audience")}
                       for st in s_adset.values() if (st.get("campaign") or "").strip() == camp]
                out.append({"campaign": camp, "category": cat, "terms_found": hits,
                            "declared": declared or "not in export", "ad_set_targeting": tgt})
    return out


WEIGHTS = {"objective": 10, "conversion_events": 15, "attribution": 5, "structure_learning": 15,
           "audience_overlap": 5, "frequency_fatigue": 10, "creative": 15, "placements": 10,
           "advantage_plus": 5, "special_ad_categories": 10}
VALUE = {"pass": 1.0, "warn": 0.5, "fail": 0.0, "blocker": 0.0}
BANDS = [(85, "Strong", "Protect what works and test at the margins."),
         (70, "Sound", "Fix the weak checks before adding budget."),
         (50, "Needs work", "Fix tracking and structure before adding budget."),
         (0, "Rebuild", "Fix the foundations before spending more.")]


def score(path):
    d = json.load(open(path, encoding="utf-8"))
    checks = d.get("checks", d)
    got = tot = 0.0
    na, blockers, unknown = [], [], []
    for k, w in WEIGHTS.items():
        st = str((checks.get(k) or {}).get("status", "na")).lower()
        if st not in VALUE:
            if st != "na":
                unknown.append(k)
            na.append(k)
            continue
        tot += w
        got += w * VALUE[st]
        if st == "blocker":
            blockers.append(k)
    s = round(got / tot * 100) if tot else 0
    if blockers:
        s = min(s, 69)  # a blocker caps the band at Needs work, whatever else is sound
    band = next(b for b in BANDS if s >= b[0])
    print(f"Score: {s}/100 · {band[1]}: {band[2]}")
    if blockers:
        print(f"BLOCKED by {', '.join(blockers)}: lead with this and recommend no budget increase until it's fixed.")
    na_w = sum(WEIGHTS[k] for k in na)
    if na:
        print(f"Not assessed ({na_w} of 100 points left out): {', '.join(na)}")
    if na_w > 30:
        print("Confidence: at most Low (more than 30 points not assessed).")
    if unknown:
        print(f"WARN: unknown status for {', '.join(unknown)} (use pass, warn, fail, blocker or na)")
    json.dump({"score": s, "band": band[1], "action": band[2], "blockers": blockers, "not_assessed": na},
              open(os.path.join(os.path.dirname(os.path.abspath(path)), "score.json"), "w"), indent=1)


def numbers(obj, acc):
    if isinstance(obj, bool):
        return acc
    if isinstance(obj, (int, float)):
        acc.add(float(obj))
    elif isinstance(obj, dict):
        for v in obj.values():
            numbers(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            numbers(v, acc)
    elif isinstance(obj, str):
        for x in re.findall(r"\d[\d,]*\.?\d*", obj):
            acc.add(num(x))
    return acc


def verify(report, metrics, allow):
    known = numbers(json.load(open(metrics, encoding="utf-8")), set()) | {num(a) for a in allow}
    bad = 0
    rx = re.compile(r"(?:[A-Z]{0,2}\$\s?(\d[\d,]*(?:\.\d+)?))|(?:(\d[\d,]*(?:\.\d+)?)\s?%)|(?:\b(\d+(?:\.\d+)?)x\b)")
    for i, line in enumerate(open(report, encoding="utf-8"), 1):
        for mt in rx.finditer(line):
            raw = next(g for g in mt.groups() if g)
            v = num(raw)
            dec = len(raw.split(".")[1]) if "." in raw else 0
            if not any(abs(round(k, dec) - v) < 1e-9 or abs(k - v) < 1e-9 for k in known):
                bad += 1
                print(f"UNTRACED line {i}: {mt.group(0).strip()}  ->  {line.strip()[:110]}")
    print("PASS: every figure traces to the export" if not bad else f"FAIL: {bad} figure(s) don't trace to a computed number")
    return 1 if bad else 0


def show(m):
    a = m["account"]
    p = m["period"]
    print(f"Files: " + ", ".join(f"{k} ({v})" for k, v in m["files"].items()))
    print(f"Period: {p['start']} to {p['end']} ({p['days']} days) · currency {m['currency']}")
    print(f"Account: spend {money(a['spend'])}, results {a['results']}, conversions {m['conversion_results']}, "
          f"CTR {a['ctr_pct']}%, CPM {a['cpm']}, frequency {a.get('frequency')}")
    print(f"Confidence: {m['confidence']['level']} ({m['confidence']['reason']})")
    print("\nCampaigns:")
    for c in m["campaigns"]:
        print(f"  {c['name']} · {c['objective']} · {c['result_indicator']} · spend {money(c['spend'])} ({c['spend_share_pct']}%) · "
              f"results {c['results']} · CPR {c['cost_per_result']} · special ad categories: {c['special_ad_categories']}")
    print(f"\nAd sets ({m['ad_sets_learning_limited']} under {LEARNING_EVENTS_PER_WEEK} optimization events/week):")
    for s in m["ad_sets"]:
        print(f"  {s['name']} · spend {money(s['spend'])} · results {s['results']} ({s.get('results_per_week')}/wk"
              f"{', LEARNING-LIMITED' if s['learning_limited'] else ''}) · CPR {s['cost_per_result']} · CTR {s['ctr_pct']}% · "
              f"freq {s.get('frequency')} · ads {s['ads']} {s['formats']} · {s['attribution']} · {s['optimization']}")
    print(f"\nAttribution settings in use: {m['attribution_settings'] or 'not in export'}")
    print(f"Ad formats: {m['formats'] or 'not in export'}")
    for t in m["trends"]:
        print(f"Trend {t['name']}: CTR {t['ctr_first_pct']}% -> {t['ctr_second_pct']}% ({t.get('ctr_change_pct')}%), "
              f"CPR {t['cpr_first']} -> {t['cpr_second']} ({t.get('cpr_change_pct')}%)")
    for camp, pl in m["placements"].items():
        print(f"\nPlacements, {camp} (CPR {pl['total']['cost_per_result']}):")
        for r in pl["rows"]:
            print(f"  {r['platform']} {r['placement']} · spend {money(r['spend'])} ({r['spend_share_pct']}%) · results {r['results']} · "
                  f"CPR {r['cost_per_result']} ({r.get('cpr_vs_campaign_x')}x)")
    for e in m["events"]:
        print(f"Event {e['event']}: {e} ")
    for b in m["backend"]:
        print(f"Business vs Meta: {b}")
    for f in m["special_ad_category_flags"]:
        print(f"SPECIAL AD CATEGORY CHECK: {f}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("paths", nargs="+")
    a.add_argument("--backend", action="append", default=[])
    a.add_argument("--json")
    s = sub.add_parser("score")
    s.add_argument("checks")
    v = sub.add_parser("verify")
    v.add_argument("report")
    v.add_argument("--metrics", required=True)
    v.add_argument("--allow", action="append", default=[])
    args = ap.parse_args()
    if args.cmd == "analyze":
        m = analyze(args.paths, args.backend)
        if not m["files"]:
            sys.exit("No CSV exports found. Nothing to audit yet: ask for the exports (references/exports.md).")
        show(m)
        if args.json:
            os.makedirs(os.path.dirname(os.path.abspath(args.json)), exist_ok=True)
            json.dump(m, open(args.json, "w"), indent=1, default=list)
    elif args.cmd == "score":
        score(args.checks)
    else:
        sys.exit(verify(args.report, args.metrics, args.allow))


if __name__ == "__main__":
    main()
