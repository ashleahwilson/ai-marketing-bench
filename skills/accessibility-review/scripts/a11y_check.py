#!/usr/bin/env python3
"""Mechanical accessibility checks for one HTML page or HTML email, against WCAG 2.2. Standard library only.

Usage:
    python3 scripts/a11y_check.py PAGE.html [--type page|email] [--brand brand/]

Prints FAIL (a WCAG A/AA failure visible in the source), CHECK (needs judgment, or best practice),
NOTE (can't be judged from source) and a PASS summary. Each line names the success criterion,
the line number and the element. Colour contrast is computed from inline styles, <style> blocks and
legacy colour attributes; text over a background image can't be computed and is listed as a NOTE.
Never edits the input. Exit 0, or 2 if the file can't be read.
"""

import argparse
import importlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
globals().update({k: v for k, v in vars(importlib.import_module("a11y_lib")).items() if not k.startswith("__")})  # helpers, same folder


def check(path, kind, brand):
    p = Parser()
    p.feed(open(path, encoding="utf-8", errors="replace").read())
    root, out, passed = p.root, [], []
    rules, focus = parse_css("\n".join(p.css))
    st = compute_styles(root, rules)
    nodes = list(root.walk())
    ids = {}
    for n in nodes:
        if n.get("id"):
            ids.setdefault(n.get("id"), n)
    if kind == "auto":
        kind = "email" if any(n.tag == "table" for n in nodes) and not any(n.tag in ("main", "nav", "header") for n in nodes) else "page"

    def add(level, sc, n, msg):
        out.append((level, sc, n.line if n else 0, snippet(n) if n else "", msg))

    html = next((n for n in nodes if n.tag == "html"), None)
    lang = html.get("lang", "").strip() if html else ""
    if not lang:
        add("FAIL", "3.1.1", html, "no lang attribute on <html>; screen readers may read the page in the wrong language")
    elif not re.fullmatch(r"[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*", lang):
        add("FAIL", "3.1.1", html, f"lang=\"{lang}\" isn't a valid language code (use e.g. \"en\" or \"en-CA\")")
    else:
        passed.append(f'lang="{lang}"')
    title = next((n for n in nodes if n.tag == "title"), None)
    if not title or not text_of(title):
        add("FAIL" if kind == "page" else "CHECK", "2.4.2" if kind == "page" else "BP", title, "no page <title>" if kind == "page" else "no <title>; some email clients and web views show it")
    else:
        passed.append("page title")
    for n in nodes:
        if n.tag == "meta" and n.get("name", "").lower() == "viewport":
            c = n.get("content", "").lower().replace(" ", "")
            ms = re.search(r"maximum-scale=([\d.]+)", c)
            if "user-scalable=no" in c or "user-scalable=0" in c or (ms and float(ms.group(1)) < 2):
                add("FAIL", "1.4.4", n, "viewport blocks pinch zoom (user-scalable=no or maximum-scale below 2)")
        if n.tag == "meta" and n.get("http-equiv", "").lower() == "refresh":
            add("FAIL", "2.2.1", n, "page refreshes or redirects on a timer")
        if n.tag in ("marquee", "blink"):
            add("FAIL", "2.2.2", n, f"<{n.tag}> moves with no way to pause it")

    # images
    n_img = n_dec = 0
    reviews = []
    for n in nodes:
        if n.tag == "img" or (n.tag == "input" and n.get("type") == "image") or n.tag == "area":
            n_img += 1
            alt = n.get("alt")
            src = os.path.basename(n.get("src", ""))
            hidden = n.get("aria-hidden") == "true" or n.get("role") in ("presentation", "none")
            if alt is None and not hidden:
                add("FAIL", "1.1.1", n, "image has no alt attribute (add a description, or alt=\"\" if it's decorative)")
            elif alt is not None and alt.strip() == "" or hidden:
                wrap = next((x for x in n.ancestors() if x.tag in ("a", "button")), None)
                if wrap is not None and not acc_name(wrap, ids):
                    reviews.append(f"empty alt but it's the only content of a link or button, so not decorative: line {n.line} {src}")
                else:
                    n_dec += 1
                    reviews.append(f"decorative: line {n.line} {src or snippet(n)}")
            else:
                a = alt.strip().lower()
                if a in BAD_ALT or re.search(r"\.(png|jpe?g|gif|svg|webp)$", a) or re.fullmatch(r"(img|dsc|image|photo)[-_ ]?\d+.*", a) or a == src.lower():
                    add("FAIL", "1.1.1", n, f"alt=\"{alt}\" doesn't describe the image (a placeholder word or file name)")
                else:
                    reviews.append(f"alt to judge in context: line {n.line} alt=\"{alt}\" ({src})")
        if n.tag == "svg" and n.get("role") == "img" and not acc_name(n, ids):
            add("FAIL", "1.1.1", n, "svg with role=img has no accessible name (aria-label or <title>)")
    if n_img:
        passed.append(f"{n_img} images ({n_dec} marked decorative)")

    # headings
    heads = []
    for n in nodes:
        if re.fullmatch(r"h[1-6]", n.tag) and not st[id(n)]["hidden"]:
            heads.append((int(n.tag[1]), n))
        elif n.get("role") == "heading":
            if not n.get("aria-level"):
                add("CHECK", "4.1.2", n, "role=heading has no aria-level (use a real <h2>–<h6> instead)")
            heads.append((int(n.get("aria-level") or 2), n))
    for lvl, n in heads:
        if not acc_name(n, ids):
            add("CHECK", "2.4.6", n, "empty heading")
    h1 = [n for lvl, n in heads if lvl == 1]
    if kind == "page":
        if not h1:
            add("CHECK", "BP", heads[0][1] if heads else None, "no H1; give the page one main heading")
        elif len(h1) > 1:
            add("CHECK", "BP", h1[1], f"{len(h1)} H1 headings; use one H1 and H2s below it")
    for (a, _), (b, n) in zip(heads, heads[1:]):
        if b > a + 1:
            add("CHECK", "BP", n, f"heading level skips from H{a} to H{b}; don't skip levels")
    if heads:
        passed.append(f"{len(heads)} headings")

    # links and buttons
    seen = {}
    n_links = 0
    for n in nodes:
        if n.tag == "a" and "href" in n.attrs:
            n_links += 1
            name = acc_name(n, ids)
            href = n.get("href", "").strip()
            if not name:
                add("FAIL", "2.4.4", n, "link has no text a screen reader can announce (image with empty or no alt, or an icon)")
            elif name.lower().strip(" .!?:→›>") in VAGUE:
                ctx = n.parent
                while ctx is not None and ctx.tag not in ("p", "li", "td", "th", "div", "body"):
                    ctx = ctx.parent
                other = text_of(ctx, True).replace(name, "").strip(" .!?:") if ctx is not None else ""
                add("FAIL" if len(other) < 12 else "CHECK", "2.4.4", n, f"vague link text \"{name}\"" + ("" if len(other) < 12 else " (the sentence around it may give context; descriptive text is still better)"))
            if name and href:
                key = name.lower().strip(" .!?:→›>")
                seen.setdefault(key, {})[href.rstrip("/")] = n
            if href in ("#", "") or href.lower().startswith("javascript:"):
                add("CHECK", "4.1.2", n, f"link href=\"{href}\" goes nowhere; if it acts as a button, use <button>")
    for key, hrefs in seen.items():
        if len(hrefs) > 1:
            ns = list(hrefs.values())
            add("CHECK", "2.4.4", ns[1], f"link text \"{key}\" is used for {len(hrefs)} different destinations: " + ", ".join(hrefs))
    if n_links:
        passed.append(f"{n_links} links")
    for n in nodes:
        role = n.get("role", "").strip().lower()
        if n.tag == "button" or (n.tag == "input" and n.get("type") in ("submit", "button", "reset")) or role == "button":
            if not acc_name(n, ids):
                add("FAIL", "4.1.2", n, "button has no accessible name (icon only, no text or aria-label)")
        if role:
            first = role.split()[0]
            if first not in ROLES:
                add("FAIL", "4.1.2", n, f"role=\"{role}\" isn't a valid ARIA role")
            elif first in WIDGET_ROLES and not is_focusable(n) and n.tag not in ("a", "button", "input", "select", "textarea"):
                add("FAIL", "2.1.1", n, f"role=\"{first}\" on a <{n.tag}> that can't be reached by keyboard (use a real <{'a' if first == 'link' else 'button'}>)")
            elif first in ("presentation", "none", "heading", "img", "listitem", "paragraph") and n.tag in ("a", "button", "input", "select", "textarea"):
                add("FAIL", "4.1.2", n, f"role=\"{first}\" on an interactive <{n.tag}> hides what it is from screen readers")
        if "onclick" in n.attrs and n.tag in ("div", "span", "li", "td", "img", "p") and not role and not is_focusable(n):
            add("FAIL", "2.1.1", n, f"click handler on a <{n.tag}> with no role or tabindex: mouse only")
        ti = n.get("tabindex", "")
        if ti.isdigit() and int(ti) > 0:
            add("FAIL", "2.4.3", n, f"tabindex=\"{ti}\" changes the tab order; use 0 or remove it")
        if n.get("aria-hidden") == "true":
            inner = [x for x in [n] + list(n.walk()) if is_focusable(x)]
            if inner:
                add("FAIL", "4.1.2", n, f"aria-hidden=\"true\" on content that still takes keyboard focus ({snippet(inner[0])})")
        if n.get("aria-label") and n.tag in ("div", "span", "p") and not role:
            add("CHECK", "4.1.2", n, "aria-label on an element with no role is ignored by most screen readers")
        for attr in ("aria-labelledby", "aria-describedby", "aria-controls"):
            for ref in n.get(attr, "").split():
                if ref not in ids:
                    add("FAIL" if attr == "aria-labelledby" else "CHECK", "4.1.2", n, f"{attr} points to id \"{ref}\", which doesn't exist")

    # forms
    labels = {}
    for n in nodes:
        if n.tag == "label" and n.get("for"):
            labels.setdefault(n.get("for"), []).append(n)
            if n.get("for") not in ids:
                add("FAIL", "1.3.1", n, f"label for=\"{n.get('for')}\" points to an id that doesn't exist")
    n_fields = n_ok = 0
    for n in nodes:
        if n.tag in ("select", "textarea") or (n.tag == "input" and n.get("type", "text") not in ("hidden", "submit", "button", "reset", "image")):
            n_fields += 1
            ok = (n.get("id") in labels and any(text_of(l, True) for l in labels[n.get("id")])) or any(a.tag == "label" and text_of(a, True) for a in n.ancestors()) or n.get("aria-label", "").strip() or (n.get("aria-labelledby") and acc_name(n, ids)) or n.get("title", "").strip()
            if not ok:
                ph = n.get("placeholder")
                add("FAIL", "4.1.2", n, "form field has no label" + (f" (placeholder \"{ph}\" disappears when typing and isn't a label)" if ph else ""))
            else:
                n_ok += 1
            nm = (n.get("name", "") + " " + n.get("id", "")).lower()
            if n.tag == "input" and not n.get("autocomplete") and (n.get("type") in ("email", "tel") or re.search(r"\b(e-?mail|phone|tel|first[-_]?name|last[-_]?name|full[-_]?name|fname|lname)\b", nm)):
                add("CHECK", "1.3.5", n, "personal-information field has no autocomplete attribute (e.g. autocomplete=\"email\")")
    if n_fields:
        passed.append(f"{n_ok} of {n_fields} form fields labelled")

    # landmarks
    if kind == "page":
        has_main = any(n.tag == "main" or n.get("role") == "main" for n in nodes)
        skip = any(n.tag == "a" and n.get("href", "").startswith("#") and "skip" in text_of(n).lower() for n in nodes)
        if not has_main:
            add("CHECK", "BP", None, "no <main> landmark" + ("" if skip else " and no skip link; add <main> so screen reader and keyboard users can jump to the content (headings alone may meet 2.4.1)"))
        else:
            passed.append("main landmark")

    # tables
    for n in nodes:
        if n.tag != "table":
            continue
        role = n.get("role", "")
        inner = list(n.walk())
        if role in ("presentation", "none"):
            if any(x.tag in ("th", "caption") for x in inner if not any(t.tag == "table" and t is not n for t in x.ancestors() if t in inner)):
                add("CHECK", "1.3.1", n, "table marked presentation but has header cells or a caption")
            continue
        if any(x.tag == "th" or x.get("scope") or x.get("headers") for x in inner):
            passed.append(f"data table at line {n.line} has headers")
            continue
        rows = [x for x in inner if x.tag == "tr" and next((a for a in x.ancestors() if a.tag == "table"), None) is n]
        cells = [[c for c in r.children if isinstance(c, Node) and c.tag in ("td", "th")] for r in rows]
        nested = any(x.tag == "table" for x in inner)
        blocky = any(x.tag in ("img", "h1", "h2", "h3", "p", "div", "button") for x in inner)
        short = all(len(text_of(c)) <= 60 for r in cells for c in r)
        if len(rows) >= 2 and min((len(r) for r in cells), default=0) >= 2 and not nested and not blocky and short:
            add("FAIL", "1.3.1", n, f"data table ({len(rows)} rows) has no header cells; mark the header row with <th scope=\"col\">")
        elif kind == "email" or nested or blocky:
            add("CHECK", "1.3.1", n, "layout table without role=\"presentation\"; screen readers may announce rows and columns")

    # media
    for n in nodes:
        if n.tag in ("video", "audio"):
            if "autoplay" in n.attrs and (n.tag == "audio" or "muted" not in n.attrs):
                add("FAIL", "1.4.2", n, "autoplays without muted: any sound starts on its own (fails if it has audio longer than 3 seconds; add muted or remove autoplay)")
            if "autoplay" in n.attrs and "controls" not in n.attrs and n.tag == "video":
                add("FAIL" if "loop" in n.attrs else "CHECK", "2.2.2", n, "moving video starts on its own with no controls to pause it" + ("" if "loop" in n.attrs else " (fails if it runs longer than 5 seconds)"))
            if n.tag == "video" and not any(isinstance(c, Node) and c.tag == "track" and c.get("kind") in ("captions", "subtitles") for c in n.children):
                add("NOTE", "1.2.2", n, "no captions track in the source; captions may be burned in, so check the video itself")
        if n.tag == "iframe":
            if not n.get("title", "").strip() and not n.get("aria-label") and n.get("aria-hidden") != "true":
                add("FAIL", "4.1.2", n, "iframe has no title describing its content")
            if re.search(r"[?&](autoplay|auto_play)=1", n.get("src", "")):
                add("CHECK", "1.4.2", n, "embedded media set to autoplay")
            add("NOTE", "1.2.2", n, "embedded content (captions, controls, keyboard use) can't be checked from this page's source")

    # focus styles
    for sel, d in focus:
        if re.search(r"\b(none|0)\b", d.get("outline", "")) and not any(k in d for k in ("box-shadow", "border", "border-color", "background", "background-color", "text-decoration", "outline-color")):
            add("FAIL", "2.4.7", None, f"CSS rule \"{sel}\" removes the focus outline with no replacement")

    # text: contrast, sensory, inclusive, reading level
    pairs, body_text = {}, []
    for n in nodes:
        s = st[id(n)]
        own = " ".join(c.strip() for c in n.children if isinstance(c, str) and c.strip())
        if not own or s["hidden"]:
            continue
        if n.tag in ("p", "li", "td", "span", "a", "strong", "em", "b", "div", "h2", "h3", "label", "dd", "blockquote", "figcaption"):
            body_text.append(own if re.search(r"[.!?:]['\"”’)]?$", own) else own + ".")
        bg = effective_bg(n, st)
        large = s["size"] >= 24 or (s["size"] >= 18.66 and s["bold"])
        if bg is None:
            add("NOTE", "1.4.3", n, f"text \"{own[:40]}\" sits on a background image or gradient; contrast can't be computed from source")
            continue
        fg = blend(s["color"], bg) if s["color"][3] < 1 else s["color"]
        r = ratio(fg, bg)
        key = (hexc(fg), hexc(bg), large)
        if key not in pairs:
            pairs[key] = (r, n, own)
    fails = 0
    for (f, b, large), (r, n, own) in pairs.items():
        need = 3.0 if large else 4.5
        if r < need:
            fails += 1
            add("FAIL", "1.4.3", n, f"text {f} on {b} is {r:.2f}:1, needs {need}:1 ({'large' if large else 'normal'} text, \"{own[:40]}\"). Passing options: {suggest(parse_color(f), parse_color(b), need)}")
    passed.append(f"{len(pairs) - fails} of {len(pairs)} text colour pairs meet contrast")
    full = " ".join(body_text)
    for pat in SENSORY:
        for m in re.finditer(pat, full, re.I):
            sent = next((s for s in re.split(r"(?<=[.!?])\s+", full) if m.group(0) in s), m.group(0))
            add("CHECK", "1.4.1" if re.search(r"red|green|blue|orange|yellow|purple|grey|gray", m.group(0), re.I) else "1.3.3", None, f"instruction may rely on colour, shape or position: \"{sent[:120]}\"")
    low = full.lower()
    for w in INCLUSIVE:
        if re.search(r"\b" + re.escape(w), low):
            i = low.find(w)
            add("CHECK", "BP", None, f"wording to review for inclusive language: \"…{full[max(0, i - 40):i + 50]}…\"")
    grade, sents = fk_grade(full)
    long = [s for s in sents if len(s.split()) > 25]
    note_rl = f"reading level about grade {grade} (Flesch-Kincaid, {len(sents)} sentences)" if grade is not None else "too little body copy for a reading-level estimate"
    if long:
        note_rl += f"; {len(long)} sentence(s) over 25 words, longest: \"{max(long, key=len)[:140]}\""
    graded = [(sentence_grade(x), x) for x in sents if len(x.split()) >= 12]
    if graded and max(graded)[0] >= 14:
        g, x = max(graded)
        note_rl += f"; hardest sentence (about grade {g}): \"{x[:160]}\""

    order = {"FAIL": 0, "CHECK": 1, "NOTE": 2}
    print(f"Accessibility source check: {os.path.basename(path)} (type: {kind})")
    for lvl, sc, line, snip, msg in sorted(out, key=lambda o: (order[o[0]], o[2])):
        print(f"{lvl:5} {sc} {SC[sc]} · line {line} · {snip} · {msg}" if line else f"{lvl:5} {sc} {SC[sc]} · {msg}")
    print("READ  " + note_rl)
    for r in reviews:
        print("IMG   " + r)
    print("PASS  " + "; ".join(passed))
    if brand and os.path.isdir(brand):
        for f in sorted(os.listdir(brand)):
            if f.endswith(".md"):
                for ln in open(os.path.join(brand, f), encoding="utf-8"):
                    for h in re.findall(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b", ln):
                        c = parse_color(h)
                        print(f"BRAND {f}: {h} with white {ratio(c, (255, 255, 255, 1)):.2f}:1, with black {ratio(c, (0, 0, 0, 1)):.2f}:1 · \"{ln.strip()[:100]}\"")
    print(f"TOTAL {sum(1 for o in out if o[0] == 'FAIL')} FAIL, {sum(1 for o in out if o[0] == 'CHECK')} CHECK, {sum(1 for o in out if o[0] == 'NOTE')} NOTE")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("page")
    ap.add_argument("--type", default="auto", choices=("auto", "page", "email"))
    ap.add_argument("--brand", default=None)
    a = ap.parse_args()
    if not os.path.isfile(a.page):
        print(f"can't read {a.page}")
        return 2
    check(a.page, a.type, a.brand)
    return 0


if __name__ == "__main__":
    sys.exit(main())
