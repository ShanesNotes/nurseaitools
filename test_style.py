"""The shipped look stays on the dark system, readable, and plain. Run: python3 test_style.py"""
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

BANNED = re.compile(
    r"\b(?:unlock|elevate|seamless|powerful|robust|next-gen|journey|dashboard|empower|effortless|"
    r"cutting-edge|game-changer|transform)\w*|curated by",
    re.I,
)
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍]")
SLOP_PUNCT = re.compile("[—–“”‘’]")
FONT_SIZES = {"12px", "13px", "14px", "16px", "20px", "24px"}
SPACES = {"0", "auto", "4px", "8px", "12px", "16px", "24px", "32px"}
GROUNDS = {"color-bg": "#0a0c10", "color-surface": "#11141a", "color-thead": "#141821", "color-hover": "#1d222c"}
PALETTE = {
    **GROUNDS,
    "color-text": "#e7e9ee", "color-muted": "#8b93a1", "color-faint": "#868d99",
    "color-line": "#3a4250", "color-line-strong": "#5c6578", "color-mark": "#e6c87e",
    "color-accent": "#e7e9ee", "color-accent-text": "#0a0c10",
}
ACCENTS = ("accent-red", "accent-blue", "accent-green", "accent-yellow")
STACK = 'ui-monospace,"Cascadia Mono","Segoe UI Mono",Menlo,Consolas,monospace'

failures = []


def check(ok, message):
    if not ok:
        failures.append(message)


def rules(css, media=""):
    """Yield (media, selector, [(property, value)]) for every rule, descending into @media."""
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
ROOT_DECLS = dict(next(d for m, s, d in RULES if s == ":root"))
TOKENS = {k[2:]: v for k, v in ROOT_DECLS.items() if k.startswith("--")}
STYLED = [(m, s, d) for m, s, d in RULES if s != ":root"]


def resolve(value):
    while "var(" in value:
        value = re.sub(r"var\(--([a-z0-9-]+)\)", lambda m: TOKENS[m.group(1)], value)
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
    m = re.fullmatch(r"var\(--([a-z0-9-]+)\)", value.replace("!important", "").strip())
    return m.group(1) if m else None


# Palette and type are the market system.
for name, hex_value in PALETTE.items():
    check(TOKENS.get(name, "").lower() == hex_value, f"--{name} is {TOKENS.get(name)}, want {hex_value}")
for name in ACCENTS:
    check(re.fullmatch(r"#[0-9a-f]{6}", TOKENS.get(name, "")), f"--{name} token is missing")
check(ROOT_DECLS.get("color-scheme") == "dark", "color-scheme is not dark")
check(TOKENS.get("font") == STACK, "the font stack is not the system monospace stack")
body = dict(next(d for m, s, d in STYLED if s == "body"))
check(body.get("font-variant-ligatures") == "none", "ligatures are not off")
check("tabular-nums" in body.get("font-variant-numeric", ""), "numbers are not tabular")
check(resolve(body.get("background", "")) == GROUNDS["color-bg"], "the page ground is not --color-bg")

# Contrast. A rule that paints its own ground is checked against that ground. Every other text
# color is checked against every ground painted by a rule that leaves the text color alone.
pairs, loose_colors, grounds = [], set(), set(GROUNDS)
for media, selector, decls in STYLED:
    d = dict(decls)
    fore = token_of(d.get("color", ""))
    back = token_of(d.get("background", d.get("background-color", "")))
    if fore and back:
        pairs.append((selector, fore, back))
    elif fore:
        loose_colors.add(fore)
    elif back:
        grounds.add(back)
for back in GROUNDS:
    check(f"var(--{back})" in CSS, f"--{back} is never painted")
loose_colors.add("color-text")
for fore in sorted(loose_colors):
    for back in sorted(grounds):
        value = ratio(TOKENS[fore], TOKENS[back])
        check(value >= 4.7, f"--{fore} on --{back} is {value:.2f}:1")
for selector, fore, back in pairs:
    value = ratio(TOKENS[fore], TOKENS[back])
    check(value >= 4.7, f"{selector}: --{fore} on --{back} is {value:.2f}:1")
check(any(f == "color-accent-text" and b == "color-accent" for s, f, b in pairs), "no filled button pair found")
for name, backs in [("color-line-strong", ("color-bg", "color-surface", "color-thead")), ("color-mark", GROUNDS),
                    *((a, GROUNDS) for a in ACCENTS)]:
    for back in backs:
        value = ratio(TOKENS[name], TOKENS[back])
        check(value >= 3.0, f"--{name} on --{back} is {value:.2f}:1, under the 3:1 non-text floor")

# Accents are edges and margin highlights, and sparse.
accent_rules = set()
for media, selector, decls in STYLED:
    for prop, value in decls:
        for name in ACCENTS:
            if f"var(--{name})" not in value:
                continue
            accent_rules.add(selector)
            if prop == "color":
                check(name in loose_colors, f"{selector}: --{name} as text was not contrast-checked")
            else:
                check(re.fullmatch(r"border(-(top|right|bottom|left))?(-color)?", prop), f"{selector}: --{name} used in {prop}")
for name in ACCENTS:
    check(f"var(--{name})" in CSS, f"--{name} is declared but never drawn")
check(len(accent_rules) <= 10, f"accents appear in {len(accent_rules)} rules, which is not sparse: {sorted(accent_rules)}")

# Flat: no depth effects and no webfonts, in the stylesheet or any page.
flat = re.compile(r"box-shadow|text-shadow|gradient|blur\(|@font-face|@import|woff|/fonts/|(?<![\w-])(backdrop-)?filter\s*:", re.I)
for path, page in ALL_PAGES.items():
    for m in flat.finditer(page):
        check(False, f"{path}: {m.group(0)}")
fonts = const("FONTS")
check(len(fonts) == 9, f"{len(fonts)} font files, want 9")
for path, file in fonts.items():
    if path.endswith(".woff2"):
        check(base64.b64decode(file["b64"])[:4] == b"wOF2", f"{path} is not a woff2")
    else:
        check("SIL Open Font License" in file.get("text", ""), f"{path} is missing the OFL text")

# Scale: every size, space, radius and color comes from :root.
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
            size = re.match(r"(?:\d{3}\s+)?(\d+px)", real)
            check(size and size.group(1) in FONT_SIZES, f"font size in {real}: {where}")
        elif re.fullmatch(r"(padding|margin)(-(top|right|bottom|left|inline|block)(-(start|end))?)?|gap|row-gap|column-gap", prop):
            for part in real.split():
                check(part in SPACES, f"spacing {part}: {where}")
for name, value in TOKENS.items():
    if name.startswith("text-"):
        check(value in FONT_SIZES, f"--{name} is {value}")
    if name.startswith("space-"):
        check(value in SPACES, f"--{name} is {value}")

# Keyboard: a skip link first, a main to land on, and one gold ring that nothing removes.
focusable = re.compile(r"<(?:a|button|input|select|textarea|summary)\b[^>]*>")
for path, page in ALL_PAGES.items():
    first = focusable.search(page.split("<body>", 1)[1])
    check(first and first.group(0) == '<a class=skip href="#main">', f"{path}: first focusable is {first and first.group(0)}")
    check(re.search(r"<main id=main\b", page), f"{path}: no <main id=main>")
rings = [dict(d) for m, s, d in STYLED if s == ":focus-visible"]
check(rings and resolve(rings[0].get("outline", "")) == "2px solid #e6c87e", "no :focus-visible rule with a 2px gold outline")
for media, selector, decls in STYLED:
    for prop, value in decls:
        if prop.startswith("outline"):
            check(selector == ":focus-visible", f"{selector} restyles the focus outline: {prop}:{value}")

# Copy: no banned pitch, no emoji, no em dash or curly quote anywhere a reader or a script sees.
for name, raw in [*ALL_PAGES.items(), *SCRIPTS.items(), ("style", CSS)]:
    for m in BANNED.finditer(raw):
        check(False, f"{name}: banned word {m.group(0)!r}")
    for m in EMOJI.finditer(raw):
        check(False, f"{name}: emoji U+{ord(m.group(0)):04X}")
    for m in SLOP_PUNCT.finditer(raw):
        check(False, f"{name}: U+{ord(m.group(0)):04X} in shipped copy")

# Content survives: every tool page carries every fact and the full reality check.
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
      f"{len(pairs)} painted pairs, accents in {len(accent_rules)} rules")
