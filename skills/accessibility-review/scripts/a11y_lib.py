"""Shared helpers for a11y_check.py: HTML tree, CSS cascade, colour contrast, accessible names. Standard library only."""

import colorsys
import re
from html.parser import HTMLParser

SC = {
    "1.1.1": "Non-text Content (A)", "1.2.2": "Captions (Prerecorded) (A)", "1.3.1": "Info and Relationships (A)",
    "1.3.3": "Sensory Characteristics (A)", "1.3.5": "Identify Input Purpose (AA)", "1.4.1": "Use of Color (A)",
    "1.4.2": "Audio Control (A)", "1.4.3": "Contrast (Minimum) (AA)", "1.4.4": "Resize Text (AA)",
    "2.1.1": "Keyboard (A)", "2.2.1": "Timing Adjustable (A)", "2.2.2": "Pause, Stop, Hide (A)",
    "2.4.1": "Bypass Blocks (A)", "2.4.2": "Page Titled (A)", "2.4.3": "Focus Order (A)",
    "2.4.4": "Link Purpose (In Context) (A)", "2.4.6": "Headings and Labels (AA)", "2.4.7": "Focus Visible (AA)",
    "3.1.1": "Language of Page (A)", "3.3.2": "Labels or Instructions (A)", "4.1.2": "Name, Role, Value (A)",
    "BP": "Best practice (not a WCAG failure)",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FOCUSABLE = {"button", "select", "textarea", "iframe", "summary"}
ROLES = set("""alert alertdialog application article banner blockquote button caption cell checkbox code columnheader
combobox complementary contentinfo definition deletion dialog directory document emphasis feed figure form generic grid
gridcell group heading img insertion link list listbox listitem log main marquee math menu menubar menuitem
menuitemcheckbox menuitemradio meter navigation none note option paragraph presentation progressbar radio radiogroup
region row rowgroup rowheader scrollbar search searchbox separator slider spinbutton status strong subscript superscript
switch tab table tablist tabpanel term textbox time timer toolbar tooltip tree treegrid treeitem""".split())
WIDGET_ROLES = {"button", "link", "checkbox", "radio", "switch", "tab", "menuitem", "option", "slider", "textbox", "combobox"}
VAGUE = {"click here", "here", "read more", "more", "learn more", "this", "link", "details", "continue", "go",
         "find out more", "more info", "this page", "click", "see more"}
BAD_ALT = {"image", "img", "photo", "picture", "graphic", "icon", "banner", "spacer", "placeholder", "untitled",
           "pic", "logo", "chart", "screenshot", "badge", "button", "hero", "header image", "banner image", "image of", "photo of", "alt", "null", "undefined"}
NAMES = {"white": "ffffff", "black": "000000", "red": "ff0000", "green": "008000", "blue": "0000ff", "gray": "808080",
         "grey": "808080", "silver": "c0c0c0", "yellow": "ffff00", "orange": "ffa500", "navy": "000080",
         "teal": "008080", "maroon": "800000", "purple": "800080", "lightgray": "d3d3d3", "lightgrey": "d3d3d3",
         "darkgray": "a9a9a9", "darkgrey": "a9a9a9", "dimgray": "696969", "whitesmoke": "f5f5f5", "pink": "ffc0cb"}
SENSORY = [r"\b(?:in|marked in|shown in|highlighted in|marked with|with)\s+(?:an? |the )?(?:red|green|blue|orange|yellow|purple|grey|gray)\b",
           r"\bthe\s+(?:red|green|blue|orange|yellow|purple|round|square|circular)\s+(?:button|link|icon|text|box|items?)\b",
           r"\b(?:red|green|blue|orange)\s+(?:items?|fields?|text|rows?)\s+(?:are|is|mean|show)\b",
           r"\b(?:on|to) the (?:right|left)\b", r"\b(?:above|below) (?:the )?(?:image|chart|picture|graphic)\b"]
INCLUSIVE = ["grandma", "grandpa", "crazy", "insane", "lame", "ocd", "blind to", "turn a blind eye", "deaf to",
             "dumb", "crippl", "spaz", "psycho", "guys", "manpower", "sanity check", "tone-deaf", "falls on deaf ears"]
HEADING_SIZE = {"h1": 32, "h2": 24, "h3": 18.72, "h4": 16, "h5": 13.28, "h6": 10.72}


class Node:
    def __init__(self, tag, attrs, line, parent):
        self.tag, self.attrs, self.line, self.parent, self.children = tag, attrs, line, parent, []

    def get(self, k, d=None):
        return self.attrs.get(k, d)

    def walk(self):
        for c in self.children:
            if isinstance(c, Node):
                yield c
                yield from c.walk()

    def ancestors(self):
        n = self.parent
        while n is not None:
            yield n
            n = n.parent


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, 0, None)
        self.cur, self.css = self.root, []

    def handle_starttag(self, tag, attrs, closed=False):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag in ("p", "li", "option") and self.cur.tag == tag:
            self.cur = self.cur.parent
        n = Node(tag, a, self.getpos()[0], self.cur)
        self.cur.children.append(n)
        if tag not in VOID and not closed:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, d):
        if self.cur.tag == "style":
            self.css.append(d)
        elif self.cur.tag not in ("script", "noscript"):
            self.cur.children.append(d)


# ---------- colour ----------
def parse_color(v):
    v = (v or "").strip().lower()
    if v in NAMES:
        v = "#" + NAMES[v]
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        if len(h) in (6, 8):
            a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
    m = re.fullmatch(r"rgba?\(\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)(?:[\s,/]+([\d.]+%?))?\s*\)", v)
    if m:
        a = m.group(4)
        a = 1.0 if a is None else (float(a[:-1]) / 100 if a.endswith("%") else float(a))
        return (float(m.group(1)), float(m.group(2)), float(m.group(3)), a)
    return None


def blend(fg, bg):
    a = fg[3]
    return tuple(fg[i] * a + bg[i] * (1 - a) for i in range(3)) + (1.0,)


def lum(c):
    def ch(x):
        x /= 255
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexc(c):
    return "#%02x%02x%02x" % tuple(int(round(x)) for x in c[:3])


def suggest(fg, bg, target):
    """Smallest lightness change to the text colour (or, failing that, the background) that meets the target."""
    out = []
    for which, base, other in (("text", fg, bg), ("background", bg, fg)):
        h, l, s = colorsys.rgb_to_hls(*(x / 255 for x in base[:3]))
        sign = 1 if lum(base) >= lum(other) else -1   # keep polarity: move away from the other colour
        for step in range(1, 101):
            nl = min(1, max(0, l + sign * step / 100))
            c = tuple(x * 255 for x in colorsys.hls_to_rgb(h, nl, s)) + (1.0,)
            if ratio(c, other) >= target:
                out.append(f"{which} {hexc(c)} ({ratio(c, other):.2f}:1)")
                break
            if nl in (0, 1):
                break
    return " or ".join(out) or "no single-colour change reaches the target; change both colours"


# ---------- CSS ----------
def strip_at_blocks(css):
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0
    while i < len(css):
        if css[i] == "@":
            j = css.find("{", i)
            k = css.find(";", i)
            if j == -1 or (k != -1 and k < j):
                i = (k + 1) if k != -1 else len(css)
                continue
            depth, j = 1, j + 1
            while j < len(css) and depth:
                depth += {"{": 1, "}": -1}.get(css[j], 0)
                j += 1
            i = j
            continue
        out.append(css[i])
        i += 1
    return "".join(out)


def decls(body):
    d = {}
    for part in body.split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            d[k.strip().lower()] = v.replace("!important", "").strip()
    return d


def parse_comp(s):
    if s == "*":
        return {"tag": None, "id": None, "cls": []}
    m = re.fullmatch(r"([a-z][a-z0-9]*)?((?:[#.][\w-]+)*)", s)
    if not m:
        return None
    rest = m.group(2)
    return {"tag": m.group(1), "id": next(iter(re.findall(r"#([\w-]+)", rest)), None), "cls": re.findall(r"\.([\w-]+)", rest)}


def comp_match(n, c):
    if c is None or n.tag.startswith("#"):
        return False
    if c["tag"] and c["tag"] != n.tag:
        return False
    if c["id"] and n.get("id") != c["id"]:
        return False
    classes = n.get("class", "").split()
    return all(x in classes for x in c["cls"])


def sel_match(n, sel):
    parts = sel.replace(">", " ").split()
    if not parts or not comp_match(n, parse_comp(parts[-1])):
        return False
    i = len(parts) - 2
    for anc in n.ancestors():
        if i < 0:
            break
        if comp_match(anc, parse_comp(parts[i])):
            i -= 1
    return i < 0


def spec(sel):
    return (len(re.findall(r"#", sel)), len(re.findall(r"\.", sel)), len(re.findall(r"(?:^|[\s>])[a-z]", sel)))


def parse_css(text):
    rules, focus = [], []
    for order, m in enumerate(re.finditer(r"([^{}]+)\{([^{}]*)\}", strip_at_blocks(text))):
        d = decls(m.group(2))
        for sel in m.group(1).split(","):
            sel = sel.strip().lower()
            if ":focus" in sel:
                focus.append((sel, d))
            elif ":" not in sel and "[" not in sel:
                rules.append((spec(sel), order, sel, d))
    rules.sort(key=lambda r: (r[0], r[1]))
    return rules, focus


# ---------- styles ----------
def font_px(v, parent):
    v = v.strip().lower()
    kw = {"small": 13, "medium": 16, "large": 18, "x-large": 24, "xx-large": 32, "x-small": 10, "smaller": parent / 1.2, "larger": parent * 1.2}
    if v in kw:
        return kw[v]
    m = re.fullmatch(r"([\d.]+)(px|pt|em|rem|%)?", v)
    if not m:
        return parent
    n, u = float(m.group(1)), m.group(2) or "px"
    return {"px": n, "pt": n * 4 / 3, "em": n * parent, "rem": n * 16, "%": n * parent / 100}[u]


def compute_styles(root, rules):
    st = {}

    def visit(n, inh):
        d = {}
        for _, _, sel, dd in rules:
            if sel_match(n, sel):
                d.update(dd)
        if n.tag in ("td", "th", "table", "body", "tr") and n.get("bgcolor"):
            d.setdefault("background-color", n.get("bgcolor"))
        if n.tag == "font" and n.get("color"):
            d.setdefault("color", n.get("color"))
        if n.tag == "body" and n.get("text"):
            d.setdefault("color", n.get("text"))
        d.update(decls(n.get("style", "")))
        s = dict(inh)
        s["bgcolor"], s["bgimage"] = None, False
        if "color" in d and parse_color(d["color"]):
            s["color"] = parse_color(d["color"])
        bg = d.get("background-color") or d.get("background", "")
        if "url(" in bg or "gradient" in bg or "url(" in d.get("background-image", "") or n.get("background"):
            s["bgimage"] = True
        for tok in re.split(r"\s+(?![^(]*\))", bg):
            if parse_color(tok):
                s["bgcolor"] = parse_color(tok)
        size = HEADING_SIZE.get(n.tag)
        s["size"] = font_px(d["font-size"], inh["size"]) if "font-size" in d else (size or inh["size"])
        w = d.get("font-weight", "")
        if w:
            s["bold"] = w in ("bold", "bolder") or (w.isdigit() and int(w) >= 700)
        elif n.tag in HEADING_SIZE or n.tag in ("b", "strong", "th"):
            s["bold"] = True
        s["hidden"] = inh["hidden"] or d.get("display") == "none" or d.get("visibility") == "hidden" or n.tag in ("head", "title", "template") or "hidden" in n.attrs
        st[id(n)] = s
        for c in n.children:
            if isinstance(c, Node):
                visit(c, s)

    visit(root, {"color": (0, 0, 0, 1.0), "size": 16.0, "bold": False, "hidden": False, "bgcolor": None, "bgimage": False})
    return st


def effective_bg(n, st):
    for x in [n] + list(n.ancestors()):
        s = st.get(id(x))
        if s is None:
            continue
        if s["bgimage"] and not (s["bgcolor"] and s["bgcolor"][3] == 1):
            return None
        if s["bgcolor"] and s["bgcolor"][3] > 0:
            if s["bgcolor"][3] < 1:
                parent = effective_bg(x.parent, st) if x.parent else (255, 255, 255, 1.0)
                return blend(s["bgcolor"], parent or (255, 255, 255, 1.0))
            return s["bgcolor"]
    return (255, 255, 255, 1.0)


# ---------- text and names ----------
def text_of(n, names=False):
    out = []
    for c in n.children:
        if isinstance(c, str):
            out.append(c)
        elif c.get("aria-hidden") == "true":
            continue
        elif names and c.tag in ("img", "area") or (c.tag == "input" and c.get("type") == "image"):
            out.append(c.get("alt", ""))
        elif names and c.tag == "svg" and (c.get("aria-label") or any(isinstance(k, Node) and k.tag == "title" for k in c.children)):
            out.append(c.get("aria-label") or next(text_of(k) for k in c.children if isinstance(k, Node) and k.tag == "title"))
        else:
            out.append(text_of(c, names))
    return re.sub(r"\s+", " ", " ".join(out)).strip()


def acc_name(n, ids):
    if n.get("aria-labelledby"):
        t = " ".join(text_of(ids[i], True) for i in n.get("aria-labelledby").split() if i in ids)
        if t.strip():
            return t.strip()
    if n.get("aria-label", "").strip():
        return n.get("aria-label").strip()
    if n.tag == "input":
        return n.get("value", "") or ({"submit": "Submit", "reset": "Reset"}.get(n.get("type", ""), "")) or n.get("title", "")
    return text_of(n, True) or n.get("title", "").strip()


def snippet(n):
    keep = ("id", "class", "href", "src", "alt", "type", "name", "role", "for", "tabindex", "aria-hidden", "aria-label", "title", "placeholder", "autoplay", "lang")
    a = " ".join(f'{k}="{v}"' if v != "" or k == "alt" else k for k, v in n.attrs.items() if k in keep)
    s = f"<{n.tag}{' ' + a if a else ''}>"
    return s if len(s) <= 90 else s[:87] + "…>"


def is_focusable(n):
    ti = n.get("tabindex")
    if ti is not None and ti.lstrip("-").isdigit():
        return int(ti) >= 0
    if "disabled" in n.attrs:
        return False
    return (n.tag == "a" and "href" in n.attrs) or n.tag in FOCUSABLE or (n.tag == "input" and n.get("type") != "hidden") or n.tag in ("audio", "video") and "controls" in n.attrs


def syllables(w):
    w = w.lower().strip("'")
    g = len(re.findall(r"[aeiouy]+", w)) - (1 if w.endswith("e") and not w.endswith("le") and len(w) > 3 else 0)
    return max(1, g)


def sentence_grade(sent):
    words = re.findall(r"[A-Za-z']+", sent)
    return round(0.39 * len(words) + 11.8 * sum(syllables(w) for w in words) / max(1, len(words)) - 15.59, 1)


def fk_grade(text):
    sents = [s for s in re.split(r"(?<=[.!?])\s+", text) if re.search(r"[a-zA-Z]", s)]
    words = re.findall(r"[A-Za-z']+", text)
    if len(sents) < 2 or len(words) < 30:
        return None, sents

    s = sum(syllables(w) for w in words)
    return round(0.39 * len(words) / len(sents) + 11.8 * s / len(words) - 15.59, 1), sents


# ---------- checks ----------
