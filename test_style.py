import base64
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
subprocess.run([sys.executable, "build.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
WORKER = (ROOT / "dist" / "worker.js").read_text(encoding="utf-8")
BASE = "https://nurseaitools.com"


def const(name):
    return json.loads(re.search(rf"^const {name} = (.*);$", WORKER, re.M).group(1))


PAGES = const("PAGES")
SCRIPTS = const("SCRIPTS")
ALL_PAGES = {**PAGES, "404": const("NOT_FOUND")}
CSS = re.search(r"<style>(.*?)</style>", PAGES["/"], re.S).group(1)
TOOLS = json.loads((ROOT / "tools.json").read_text(encoding="utf-8"))
FIGS = [
    ("nurses", sum(t["built"] == "Nurses" for t in TOOLS), "are built for nurses"),
    ("hipaa", sum(t["hstat"] == "Mentions HIPAA" for t in TOOLS), "mention HIPAA on their website"),
    ("bedside", sum(t["fit"] == "Bedside/mobile workflow" for t in TOOLS), "fit a bedside or mobile workflow"),
    ("unknown", sum(t["hstat"] == "Unknown" for t in TOOLS), "do not state a HIPAA status on their homepage"),
]

BANNED = re.compile(
    r"\b(?:unlock|elevate|seamless|powerful|robust|next-gen|journey|dashboard|empower|effortless|"
    r"cutting-edge|game-changer|transform)\w*|curated by",
    re.I,
)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")
SLOP_PUNCT = re.compile("[—–“”‘’]")
TYPE = {
    "display": "clamp(44px,7.4vw,112px)", "headline": "clamp(36px,4.6vw,64px)", "proof": "clamp(36px,5vw,72px)",
    "title": "28px", "lead": "clamp(20px,1.8vw,24px)", "body": "18px", "figure": "15px", "small": "15px", "micro": "12px",
    "button-size": "18px",
}
FONT_SIZES = set(TYPE.values())
SPACES = {"0", "auto", "2px", "4px", "8px", "12px", "16px", "24px", "32px", "48px", "64px", "96px"}
GROUNDS = ("ground", "panel", "raised", "hover", "bar")
TEXT = ("text", "soft", "pencil", "accent")
LIGHT = {
    "ground": "#f6f1e8", "panel": "#efe8db", "raised": "#fffaf3", "hover": "#e9e1d2", "bar": "#dfd3bc",
    "rule": "#8a7d68", "edge": "#6b5e4a", "text": "#1c1611", "soft": "#5c5348", "pencil": "#5e584e",
    "accent": "#1f5550", "menu": "#1c1611", "menuText": "#ece5d3", "bandSoft": "#b9b09c",
}
DARK = {
    "ground": "#1c1611", "panel": "#211a14", "raised": "#221f18", "hover": "#2c281f", "bar": "#2a2318",
    "rule": "#7d7262", "edge": "#7d7262", "text": "#ffffff", "soft": "#a49d89", "pencil": "#9a9a9a",
    "accent": "#7dbab0", "menu": "#0b0a08", "menuText": "#ece5d3", "bandSoft": "#b9b09c",
}
NEUTRAL_CHROMA = 40
DISPLAY = '"Host Grotesk","Helvetica Neue",Arial,sans-serif'

failures = []


def check(ok, message):
    if not ok:
        failures.append(message)


def rules(css, media=""):
    i = 0
    while i < len(css):
        open_at = css.find("{", i)
        if open_at < 0:
            return
        prelude = css[i:open_at].strip()
        depth, j = 1, open_at + 1
        while depth:
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
        inner = css[open_at + 1:j - 1]
        if prelude.startswith("@media"):
            yield from rules(inner, prelude)
        else:
            decls = [tuple(part.strip() for part in d.split(":", 1)) for d in inner.split(";") if ":" in d]
            yield media, prelude, decls
        i = j


RULES = list(rules(CSS))


def root_tokens(dark):
    for media, selector, decls in RULES:
        is_dark = "prefers-color-scheme" in media and "dark" in media
        if selector == ":root" and is_dark == dark:
            return {k[2:]: v for k, v in decls if k.startswith("--")}, dict(decls)
    return {}, {}


LIGHT_TOKENS, ROOT_DECLS = root_tokens(False)
DARK_TOKENS, _DARK_ROOT = root_tokens(True)
TOKENS = LIGHT_TOKENS
THEMES = {"light": LIGHT_TOKENS, "dark": {**LIGHT_TOKENS, **DARK_TOKENS}}
STYLED = [(m, s, d) for m, s, d in RULES if s != ":root"]


def resolve(value):
    while "var(" in value:
        value = re.sub(r"var\(--([A-Za-z0-9-]+)\)", lambda m: TOKENS[m.group(1)], value)
    return value.replace("!important", "").strip()


def lum(hex_color):
    def channel(c):
        c = int(c, 16) / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(hex_color[i:i + 2]) for i in (1, 3, 5))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fore, back):
    hi, lo = sorted((lum(fore), lum(back)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def token_of(value):
    m = re.fullmatch(r"var\(--([A-Za-z0-9-]+)\)", value.replace("!important", "").strip())
    return m.group(1) if m else None


for theme, expect in (("light", LIGHT), ("dark", DARK)):
    got = THEMES[theme]
    for name, hex_value in expect.items():
        check(got.get(name, "").lower() == hex_value, f"{theme} --{name} is {got.get(name)}, want {hex_value}")
check(ROOT_DECLS.get("color-scheme") == "light dark", "color-scheme is not light dark")
check(TOKENS.get("f-display") == DISPLAY, "the statement face is not Host Grotesk")
check(TOKENS.get("f-body") == DISPLAY, "the reading face is not Host Grotesk")
check("JetBrains Mono" in TOKENS.get("f-figure", ""), "figures are not JetBrains Mono")
check(TOKENS.get("reach") == "44px", "reach is not 44px")
for name, size in TYPE.items():
    check(TOKENS.get(name) == size, f"--{name} is {TOKENS.get(name)}, want {size}")
    check(min(int(n) for n in re.findall(r"(\d+)px", size)) >= 12, f"--{name} can render under 12px")
for name in ("s-xs", "s-s", "s-m", "s-l", "s-xl", "s-2xl", "s-3xl", "s-4xl", "s-5xl", "s-6xl", "section"):
    check(TOKENS.get(name) in SPACES, f"--{name} left the spacing scale")
body = dict(next(d for m, s, d in STYLED if s == "body"))
check(body.get("font-variant-ligatures") == "none", "ligatures are not off")
check("tabular-nums" in body.get("font-variant-numeric", ""), "numbers are not tabular")
check(resolve(body.get("background", "")) == LIGHT["ground"], "the page ground is not --ground")
faces = [dict(d).get("font-family", "").strip('"') for m, s, d in STYLED if s == "@font-face"]
check(faces.count("Host Grotesk") == 3 and faces.count("JetBrains Mono") == 2 and "Fragment Mono" not in faces,
      f"font faces are {faces}")

pairs, loose_colors, grounds, band_colors = [], set(), set(GROUNDS), set()
for media, selector, decls in STYLED:
    d = dict(decls)
    if selector.startswith(".news ") and token_of(d.get("color", "")) and not d.get("background"):
        band_colors.add(token_of(d["color"]))
        continue
    fore = token_of(d.get("color", ""))
    back = token_of(d.get("background", d.get("background-color", "")))
    if fore and back:
        pairs.append((selector, fore, back))
    elif fore:
        loose_colors.add(fore)
    elif back and back in GROUNDS:
        grounds.add(back)
for back in GROUNDS:
    check(f"var(--{back})" in CSS, f"--{back} is never painted")
for theme, got in THEMES.items():
    for fore in sorted(loose_colors | set(TEXT)):
        for back in sorted(grounds):
            value = ratio(got[fore], got[back])
            check(value >= 4.5, f"{theme} --{fore} on --{back} is {value:.2f}:1")
    for fore in sorted(band_colors):
        value = ratio(got[fore], got["menu"])
        check(value >= 4.5, f"{theme} band --{fore} on --menu is {value:.2f}:1")
    for selector, fore, back in pairs:
        value = ratio(got[fore], got[back])
        check(value >= 4.5, f"{theme} {selector}: --{fore} on --{back} is {value:.2f}:1")
    for name in ("edge", "accent", "pencil"):
        for back in ("ground", "raised", "bar"):
            value = ratio(got[name], got[back])
            check(value >= 3.0, f"{theme} --{name} on --{back} is {value:.2f}:1, under the 3:1 edge floor")
check(any(f == "menuText" and b == "menu" for s, f, b in pairs), "no menu button pair found")

hues = set()
for theme, got in THEMES.items():
    for name, value in got.items():
        if re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            channels = [int(value[i:i + 2], 16) for i in (1, 3, 5)]
            if max(channels) - min(channels) > NEUTRAL_CHROMA:
                hues.add(name)
check(hues == {"accent"}, f"tokens with a hue are {sorted(hues)}, want only --accent")
for name in ("accent", "pencil"):
    check(f"var(--{name})" in CSS, f"--{name} is declared but never drawn")

fonts = const("FONTS")
flat = re.compile(r"text-shadow|box-shadow|gradient|blur\(|@import|(?<![\w-])(backdrop-)?filter\s*:|(?<![\w-])transform\s*:", re.I)
for path, page in ALL_PAGES.items():
    for m in flat.finditer(page):
        check(False, f"{path}: {m.group(0)}")
for path, page in ALL_PAGES.items():
    for src in re.findall(r"/fonts/[A-Za-z0-9.-]+", page):
        check(src in fonts, f"{path} references {src}, which the worker does not serve")
check(len(fonts) == 9, f"{len(fonts)} font files, want 9")
for path, file in fonts.items():
    if path.endswith(".woff2"):
        check(base64.b64decode(file["b64"])[:4] == b"wOF2", f"{path} is not a woff2")
    else:
        check("SIL Open Font License" in file.get("text", ""), f"{path} is missing the OFL text")

for media, selector, decls in STYLED:
    for prop, value in decls:
        where = f"{selector} {{{prop}:{value}}}"
        check(not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(", value), f"hard-coded color outside :root: {where}")
        check(not re.search(r"(?<![\w-])\d*\.?\d+(px|rem|em|ch|vw|vh|dvh|pt)\b", value), f"hard-coded size outside :root: {where}")
        real = resolve(value)
        if prop == "border-radius":
            check(real in {"0", "2px"}, f"radius {real}: {where}")
        elif prop == "font-size":
            check(real in FONT_SIZES, f"font size {real}: {where}")
        elif prop == "font" and real != "inherit":
            size = re.match(r"(?:\d{3}\s+)?(clamp\([^)]*\)|\d+px)", real)
            check(size and size.group(1) in FONT_SIZES, f"font size in {real}: {where}")
        elif re.fullmatch(r"(padding|margin)(-(top|right|bottom|left|inline|block)(-(start|end))?)?|gap|row-gap|column-gap", prop):
            for part in real.split():
                check(part in SPACES, f"spacing {part}: {where}")

focusable = re.compile(r"<(?:a|button|input|select|textarea|summary)\b[^>]*>")
for path, page in ALL_PAGES.items():
    first = focusable.search(page.split("<body>", 1)[1])
    check(first and first.group(0) == '<a class=skip href="#main">', f"{path}: first focusable is {first and first.group(0)}")
    check(re.search(r"<main id=main\b", page), f"{path}: no <main id=main>")
rings = [dict(d) for m, s, d in STYLED if s == ":focus-visible"]
check(rings and rings[0].get("outline", "").replace(" ", "") == "var(--ring)solidvar(--accent)", "focus ring is not the accent ring")
for media, selector, decls in STYLED:
    for prop, value in decls:
        if prop.startswith("outline"):
            ok = selector == ":focus-visible" or (selector.endswith(" :focus-visible") and prop == "outline-color")
            check(ok, f"{selector} restyles the focus outline: {prop}:{value}")

for name, raw in [*ALL_PAGES.items(), *SCRIPTS.items(), ("style", CSS)]:
    for m in BANNED.finditer(raw):
        check(False, f"{name}: banned word {m.group(0)!r}")
    for m in EMOJI.finditer(raw):
        check(False, f"{name}: emoji U+{ord(m.group(0)):04X}")
    for m in SLOP_PUNCT.finditer(raw):
        check(False, f"{name}: U+{ord(m.group(0)):04X} in shipped copy")

tool_pages = [p for p in PAGES if p.startswith("/tools/")]
check(len(tool_pages) == len(TOOLS), f"{len(tool_pages)} tool pages for {len(TOOLS)} tools")
for t in TOOLS:
    page = PAGES.get("/tools/" + t["slug"], "")
    for field in ("name", "vendor", "what", "url", "ehr", "hipaa", "built", "hstat", "fit"):
        check(html.escape(t[field]) in page, f"/tools/{t['slug']} is missing its {field}")
home = PAGES["/"]
for hook in ("data-catalog", "data-filter-query", "data-filter-category", "data-filter-trait", "data-filter-clear",
             "data-catalog-count", "data-catalog-empty", "data-form-message", 'action="/api/subscribe"', "name=hp"):
    check(hook in home, f"home is missing {hook}")
check(home.count("data-card") == len(TOOLS), "home does not list every tool")
check("AI should run the rules in the background so nurses can run the care." in home, "home is missing the brand line")
check('<a href="/students">' in home, "home does not link the students hub")
for name, value, label in FIGS:
    check(f"<b>{value}</b><span>{label}</span>" in home, f"home figure {label!r} is not {value}")
for selector in ("button", "input:not([type=checkbox]),select,textarea", ".mast nav a", ".skip", ".toggle", ".acts a"):
    decls = [dict(d) for m, s, d in STYLED if s == selector]
    check(any(item.get("min-height") == "var(--reach)" for item in decls), f"{selector} is under 44px")
check('action="/api/submit"' in PAGES.get("/submit", ""), "the submit form is gone")
check("14 years of critical care" in PAGES.get("/about", ""), "the About page lost the RN fact")
for path in ("/students", "/students/best-free-ai", "/students/ai-care-plan-tools", "/students/nclex-ai-tutors"):
    check(path in PAGES, f"{path} is missing")
for path, page in PAGES.items():
    for tag in (f'<link rel=canonical href="{BASE}{path}">', "<title>", "<meta name=description", "<meta property=og:title",
                "<meta property=og:description", f'<meta property=og:url content="{BASE}{path}">'):
        check(tag in page, f"{path} is missing {tag}")

if failures:
    print("\n".join(failures))
    print(f"FAIL {len(failures)}")
    sys.exit(1)
print(f"ok {len(ALL_PAGES)} pages, {len(TOOLS)} tools, {len(loose_colors)} text colors on {len(grounds)} grounds, "
      f"{len(pairs)} painted pairs, one accent")
