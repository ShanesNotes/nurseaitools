#!/usr/bin/env python3
"""Build the worker, serve it on this box, drive it in Chrome, and print PASS or FAIL.

Usage, from the repo root:
  /workspace/.pwvenv/bin/python .agents/skills/verify-nurse-ai-tools/verify.py [options]

Exit code 0 means every check passed. Exit code 1 means at least one failed.
Nothing here talks to Cloudflare, Kit, or the live site. See SKILL.md.
"""
import argparse
import json
import os
import re
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import http.client

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LIVE = "https://nurseaitools.com"

ap = argparse.ArgumentParser()
ap.add_argument("--harness", choices=["wrangler", "serve"], default="wrangler",
                help="wrangler: wrangler dev --local with a fresh local D1. serve: node serve.mjs with a stub DB.")
ap.add_argument("--tool", default="", help="slug for the tool page drive. Default: the first Education / NCLEX tool.")
ap.add_argument("--min-font", type=float, default=12, help="smallest rendered text size in px. Both designs say 12.")
ap.add_argument("--min-control", type=float, default=44, help="smallest button, field, and select height in px. Both designs say 44.")
ap.add_argument("--min-link", type=float, default=24, help="WCAG 2.5.8 target size in px for stand-alone links. Smaller passes if nothing else is within its circle. Links in a sentence are exempt.")
ap.add_argument("--min-contrast", type=float, default=4.5, help="text contrast floor. Large text uses 3.")
ap.add_argument("--schemes", default="light,dark", help="color schemes to audit, comma separated.")
ap.add_argument("--skip-unit", action="store_true", help="skip npm test and test_style.py.")
ap.add_argument("--shots", default=os.path.join(ROOT, "shots", "verify"))
args = ap.parse_args()

results = []
started = time.time()


def check(name, ok, detail=""):
    results.append({"check": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""), flush=True)
    return ok


def note(name, detail):
    results.append({"check": name, "ok": None, "detail": detail})
    print("SKIP " + name + ": " + detail, flush=True)


def summary_and_exit():
    failed = [r for r in results if r["ok"] is False]
    passed = [r for r in results if r["ok"] is True]
    skipped = [r for r in results if r["ok"] is None]
    os.makedirs(args.shots, exist_ok=True)
    rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    with open(os.path.join(args.shots, "report.json"), "w") as f:
        json.dump({"revision": rev, "dirty": dirty, "harness": args.harness, "results": results}, f, indent=1)
    print()
    print(f"revision {rev}{' (uncommitted changes)' if dirty else ''}, harness {args.harness}, {time.time() - started:.0f}s, evidence {os.path.relpath(args.shots, ROOT)}/")
    if failed:
        print(f"VERIFY FAIL: {len(failed)} failed, {len(passed)} passed, {len(skipped)} skipped")
        for r in failed:
            print("  FAIL " + r["check"] + (": " + r["detail"] if r["detail"] else ""))
        sys.exit(1)
    print(f"VERIFY PASS: {len(passed)} passed, {len(skipped)} skipped")
    sys.exit(0)


try:
    from playwright.sync_api import sync_playwright
except ImportError:
    check("setup: playwright importable", False, f"run this with a Python that has playwright, e.g. /workspace/.pwvenv/bin/python, not {sys.executable}")
    summary_and_exit()


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def local_env():
    # The box has Cloudflare credentials in its env. A local verify never needs them, so no child sees them.
    env = {k: v for k, v in os.environ.items() if not re.match(r"^(CF_|CLOUDFLARE_|KIT_)", k)}
    env["WRANGLER_SEND_METRICS"] = "false"
    return env


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"user-agent": "verify-nurse-ai-tools"}), timeout=15) as r:
            return r.status, dict(r.headers), r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return err.code, dict(err.headers), err.read().decode("utf-8", "replace")


def raw(url, host):
    """GET without following redirects, with a Host header, so www and workers.dev can be faked locally."""
    u = urllib.parse.urlsplit(url)
    c = http.client.HTTPConnection(u.hostname, u.port, timeout=15)
    c.request("GET", u.path + (("?" + u.query) if u.query else ""), headers={"Host": host, "user-agent": "verify-nurse-ai-tools"})
    r = c.getresponse()
    out = r.status, {k.lower(): v for k, v in r.getheaders()}, r.read().decode("utf-8", "replace")
    c.close()
    return out


def post(url, origin):
    headers = {"user-agent": "verify-nurse-ai-tools", "content-type": "application/json"}
    if origin:
        headers["origin"] = origin
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=b"{}", headers=headers, method="POST"), timeout=15) as r:
            return r.status
    except urllib.error.HTTPError as err:
        return err.code


CANON = re.compile(r'<link rel=canonical href="([^"]*)"')


tools = json.load(open(os.path.join(ROOT, "tools.json")))
N = len(tools)
# The NCLEX guides from landing.py. A guide missing from the sitemap fails the students checks below.
GUIDES = ["/students/best-ai-nclex-prep", "/students/free-nclex-prep", "/students/ngn-practice-tools", "/students/chatgpt-for-nclex"]

# 1. Build.
b = run(["python3", "build.py"])
m = re.search(r"(\d+) tools (\d+) pages", b.stdout)
check("build: python3 build.py exits 0", b.returncode == 0, (b.stdout.strip() or b.stderr.strip())[-200:])
check("build: tool count matches tools.json", bool(m) and int(m.group(1)) == N, f"build says {m.group(1) if m else '?'}, tools.json has {N}")

# 2. Unit and style suites already in the repo. They check whichever design the checkout ships.
if args.skip_unit:
    note("unit: npm test", "--skip-unit")
    note("unit: python3 test_style.py", "--skip-unit")
else:
    t = run(["npm", "test", "--silent"], env=local_env())
    counts = dict(re.findall(r"^# (pass|fail) (\d+)", t.stdout, re.M))
    check("unit: npm test", t.returncode == 0, f"pass {counts.get('pass', '?')}, fail {counts.get('fail', '?')}")
    s = run(["python3", "test_style.py"])
    check("unit: python3 test_style.py", s.returncode == 0, (s.stdout.strip().splitlines() or [s.stderr.strip()[-200:]])[-1])

# 3. Serve on this box.
for f in (".dev.vars", ".env"):
    p = os.path.join(ROOT, f)
    if os.path.exists(p) and "KIT_API_KEY" in open(p).read():
        check("setup: no Kit key in local vars", False, f"{f} sets KIT_API_KEY, so a local signup would reach Kit. Remove it and rerun.")
        summary_and_exit()
port = free_port()
base = f"http://127.0.0.1:{port}"
persist = tempfile.mkdtemp(prefix="nai-verify-d1-")
log = open(os.path.join(tempfile.gettempdir(), f"nai-verify-{port}.log"), "w")
if args.harness == "wrangler":
    seed = run(["npx", "wrangler", "d1", "execute", "nurseaitools", "--local", "--persist-to", persist, "--file", "schema.sql"], env=local_env())
    check("serve: local D1 seeded from schema.sql", seed.returncode == 0, persist)
    mig = run(["npx", "wrangler", "d1", "migrations", "apply", "nurseaitools", "--local", "--persist-to", persist], env=local_env(), stdin=subprocess.DEVNULL)
    applied = re.findall(r"(\d{4}_\w+\.sql)\s*│\s*✅", mig.stdout)
    check("serve: migrations apply cleanly to the local D1", mig.returncode == 0 and applied == sorted(os.listdir(os.path.join(ROOT, "migrations"))), f"applied {applied}")
    cmd = ["npx", "wrangler", "dev", "--local", "--persist-to", persist, "--ip", "127.0.0.1", "--port", str(port),
           "--inspector-port", str(free_port()), "--show-interactive-dev-session=false"]
else:
    cmd = ["node", "serve.mjs"]
env = local_env()
env["PORT"] = str(port)
server = subprocess.Popen(cmd, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)


def stop():
    try:
        os.killpg(server.pid, signal.SIGTERM)
        server.wait(10)
    except Exception:
        pass


ready = False
for _ in range(120):
    if server.poll() is not None:
        break
    try:
        if get(base + "/")[0] == 200:
            ready = True
            break
    except Exception:
        pass
    time.sleep(0.5)
if not check(f"serve: {' '.join(cmd[:3])} answers on {base}", ready, f"log {log.name}"):
    stop()
    summary_and_exit()

try:
    # 4. Status codes and head tags for every page in the sitemap.
    st, _, sm = get(base + "/sitemap.xml")
    paths = [u.replace(LIVE, "") or "/" for u in re.findall(r"<loc>([^<]+)</loc>", sm)]
    check("http: /sitemap.xml 200", st == 200, f"{len(paths)} urls")
    for slug in (t["slug"] for t in tools):
        if "/tools/" + slug not in paths:
            check(f"http: /tools/{slug} in sitemap", False)
    missing = [g for g in GUIDES if g not in paths]
    check("http: the four NCLEX guides are in the sitemap", not missing, f"missing {missing}" if missing else "")
    bad = []
    served = {}
    for p in paths:
        st, _, html = get(base + p)
        served[p] = CANON.findall(html)
        title = re.search(r"<title>([^<]+)</title>", html)
        problems = [x for x, ok in (
            (f"status {st}", st == 200),
            ("no title", bool(title and title.group(1).strip())),
            ("no meta description", re.search(r'<meta name=description content="[^"]+"', html)),
            ("canonical not " + LIVE + p, f'<link rel=canonical href="{LIVE}{p}"' in html),
            ("not exactly one h1", len(re.findall(r"<h1[ >]", html)) == 1),
        ) if not ok]
        if problems:
            bad.append(f"{p} ({', '.join(problems)})")
    check("http: every sitemap page is 200 with title, description, canonical, one h1", not bad, f"{len(paths)} pages" + ("; " + "; ".join(bad[:5]) if bad else ""))
    names_bad = [t["slug"] for t in tools if t["name"] not in re.sub(r"&amp;", "&", get(base + "/tools/" + t["slug"])[2].split("</title>")[0])]
    check("http: each tool title names its tool", not names_bad, f"{N} tools" + (f"; missing {names_bad[:5]}" if names_bad else ""))
    st, _, _ = get(base + "/no-such-page-verify")
    check("http: unknown path is 404", st == 404, f"status {st}")
    st, _, _ = get(base + "/tools")
    check("http: /tools is 404, the directory lives on /", st == 404, f"status {st}. If a /tools route has shipped on purpose, update this check and SKILL.md")
    st, _, robots = get(base + "/robots.txt")
    check("http: /robots.txt 200 and names the sitemap", st == 200 and "sitemap.xml" in robots.lower(), f"status {st}")
    # 4b. Canonicals. Search Console labels trailing-slash, query, and other-host copies
    # "Alternate page with proper canonical". That is fine as long as every indexable page
    # names itself on the apex and the sitemap lists exactly those URLs.
    built = open(os.path.join(ROOT, "dist", "worker.js")).read()
    built_pages = json.loads(re.search(r"^const PAGES = (\{.*\});$", built, re.M).group(1))
    not_found = json.loads(re.search(r"^const NOT_FOUND = (\".*\");$", built, re.M).group(1))
    bad = []
    for p, html in built_pages.items():
        found = CANON.findall(html)
        c = urllib.parse.urlsplit(found[0]) if len(found) == 1 else None
        og = re.search(r'<meta property=og:url content="([^"]*)"', html)
        problems = [x for x, ok in (
            (f"{len(found)} canonicals", len(found) == 1 and len(re.findall(r"rel=.?canonical", html)) == 1),
            (f"points to {found[0] if found else None}", found == [LIVE + p]),
            ("not https apex", c and c.scheme == "https" and c.netloc == "nurseaitools.com"),
            ("has query or fragment", c and not c.query and not c.fragment),
            ("trailing slash", c and (c.path == "/" or not c.path.endswith("/"))),
            ("og:url differs", og and found and og.group(1) == found[0]),
            ("noindex", not re.search(r"noindex", html, re.I)),
        ) if not ok]
        if problems:
            bad.append(f"{p} ({', '.join(problems)})")
    check("canonical: every built page has one canonical, to itself on " + LIVE, not bad, f"{len(built_pages)} pages in dist/worker.js" + ("; " + "; ".join(bad[:5]) if bad else ""))
    locs = re.findall(r"<loc>([^<]+)</loc>", sm)
    canon_set = {LIVE + p for p in built_pages}
    check("canonical: sitemap URLs equal the built pages' canonicals", len(locs) == len(set(locs)) and set(locs) == canon_set,
          f"{len(locs)} urls, {len(set(locs))} unique, {len(canon_set)} canonicals"
          + (f"; only in sitemap {sorted(set(locs) - canon_set)[:3]}; only built {sorted(canon_set - set(locs))[:3]}" if set(locs) != canon_set else ""))
    mism = [(p, served.get(p)) for p in paths if served.get(p) != [LIVE + p]]
    check("canonical: each served sitemap page's canonical equals its sitemap URL", not mism, f"{len(paths)} pages" + (f"; {mism[:3]}" if mism else ""))
    bad = []
    for p in paths:
        for v in ([p + "/", p + "//", p + "/?utm_source=verify"] if p != "/" else []) + [p + "?q=verify"]:
            st, _, html = get(base + v)
            if st != 200 or CANON.findall(html) != [LIVE + p]:
                bad.append(f"{v} ({st}, {CANON.findall(html)})")
    check("canonical: trailing-slash and query copies are 200 and point at the clean URL", not bad, f"{len(paths)} pages x 4 variants" + ("; " + "; ".join(bad[:3]) if bad else ""))
    st, h, _ = raw(base + "/students/?q=verify", "www.nurseaitools.com")
    loc = urllib.parse.urlsplit(h.get("location", ""))
    check("canonical: www 301s to the apex, keeping path and query", st == 301 and loc.netloc == "nurseaitools.com" and loc.path == "/students/" and loc.query == "q=verify",
          f"{st} -> {h.get('location')}. The scheme follows the request (http here); live https was not checked by this script")
    st, _, html = raw(base + "/students", "nurseaitools.verify.workers.dev")
    check("canonical: a workers.dev copy points at the apex", st == 200 and CANON.findall(html) == [LIVE + "/students"], f"{st}, {CANON.findall(html)}. Faked with a Host header; wrangler.toml sets workers_dev = false")
    offsite = sorted({(p, a) for p, html in built_pages.items() for a in re.findall(r'<a [^>]*href="?([^" >]+)', html)
                      if (a.startswith("/") and not a.startswith("//") and ("?" in a or (a != "/" and a.split("#")[0].endswith("/"))))
                      or re.match(r"(https?:)?//(www\.)?nurseaitools\.com", a)})
    check("canonical: internal links use the canonical form", not offsite, f"{len(built_pages)} pages" + (f"; {offsite[:5]}" if offsite else ""))
    st, _, html = get(base + "/no-such-page-verify")
    check("canonical: the 404 page is 404 with no canonical, noindex, and no current nav item",
          st == 404 and not CANON.findall(html) and "<meta name=robots content=noindex>" in html and not re.search(r"<a [^>]*aria-current", html),
          f"status {st}, canonical {CANON.findall(html)}, noindex {'noindex' in html}, current nav {bool(re.search(r"<a [^>]*aria-current", html))}")
    check("canonical: the built 404 body matches what is served", CANON.findall(not_found) == CANON.findall(html))
    st, h, forum = get(base + "/discuss")
    check("forum: /discuss 200, one h1, the empty state, the site stylesheet",
          st == 200 and len(re.findall(r"<h1[ >]", forum)) == 1 and "data-forum-empty" in forum
          and re.search(r"<style>(.*?)</style>", forum, re.S).group(1) == re.search(r"<style>(.*?)</style>", get(base + "/")[2], re.S).group(1),
          f"status {st}, cache {h.get('cache-control', h.get('Cache-Control'))}")
    codes = {o: post(base + "/api/forum/threads", o) for o in (base, "https://evil.example", None)}
    check("forum: unauthenticated POST /api/forum/threads is 401", codes[base] == 401, f"status {codes[base]}")
    check("forum: POST with a foreign or missing Origin is 403", codes["https://evil.example"] == 403 and codes[None] == 403, f"foreign {codes['https://evil.example']}, missing {codes[None]}")

    for s in sorted(set(re.findall(r'src="(/js/[^"]+)"|href="(/js/[^"]+)"', get(base + "/")[2]))):
        src = s[0] or s[1]
        st, h, _ = get(base + src)
        check(f"http: {src} 200 javascript", st == 200 and "javascript" in h.get("content-type", h.get("Content-Type", "")), f"status {st}")
    home_html = get(base + "/")[2]
    fonts = sorted(set(re.findall(r'url\("?(/fonts/[^")]+)"?\)', home_html)))
    if fonts:
        bad = [f for f in fonts if get(base + f)[0] != 200]
        check("http: self-hosted fonts 200", not bad, f"{len(fonts)} faces" + (f"; missing {bad}" if bad else ""))
    else:
        note("http: self-hosted fonts", "this design loads no webfont")

    tool = next((t for t in tools if t["slug"] == args.tool), None) if args.tool else None
    tool = tool or next((t for t in tools if "NCLEX" in t["category"]), tools[0])

    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ.get("CHROME", "/usr/bin/google-chrome"))
        offbox = []

        def guard(route):
            # The browser may only reach this local server. Anything else is blocked and reported.
            if route.request.url.startswith(base):
                route.continue_()
            else:
                offbox.append(route.request.url)
                route.abort()

        def new_page(width, height, scheme="light"):
            ctx = browser.new_context(viewport={"width": width, "height": height}, color_scheme=scheme, device_scale_factor=1)
            ctx.route("**/*", guard)
            return ctx.new_page()

        os.makedirs(args.shots, exist_ok=True)
        page = new_page(1280, 800)
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))

        # 5. Home and the directory.
        page.goto(base + "/", wait_until="networkidle")
        check("home: title present", bool(page.title().strip()), page.title())
        count = page.locator("[data-catalog-count]").inner_text().strip()
        check("home: count reads tools.json total", count == f"{N} tools", f"{count!r}")
        cards = page.locator("[data-card]").count()
        check("home: one directory row per tool", cards == N, f"{cards} rows, {N} tools")
        text = page.locator("[data-catalog]").inner_text()
        missing = [t["name"] for t in tools if t["name"] not in text]
        check("home: every tool name is in the directory", not missing, f"missing {missing[:5]}" if missing else f"{N} names")
        page.screenshot(path=os.path.join(args.shots, "home-desktop.png"))

        q = page.locator("[data-filter-query]")
        q.fill("abridge")
        page.wait_for_function("el => el.textContent.includes(' of ')", arg=page.locator("[data-catalog-count]").element_handle())
        after = page.locator("[data-catalog-count]").inner_text().strip()
        visible = page.locator("[data-card]:visible").count()
        expect = sum(1 for t in tools if "abridge" in (t["name"] + " " + t["vendor"] + " " + t["what"]).lower())
        check("directory: search narrows to matching rows", after == f"{visible} of {N} tools" and visible == expect and visible > 0, f"{after!r}, {visible} visible, {expect} expected from tools.json")
        page.screenshot(path=os.path.join(args.shots, "directory-search.png"))
        q.fill("")
        cat = tool["category"]
        page.locator("[data-filter-category]").select_option(label=cat)
        page.wait_for_timeout(200)
        want = sum(1 for t in tools if t["category"] == cat)
        got = page.locator("[data-card]:visible").count()
        check("directory: category filter matches tools.json", got == want, f"{cat}: {got} visible, {want} in tools.json")
        page.locator("[data-filter-category]").select_option(value="")
        q.fill("zzqx-no-tool-matches")
        page.wait_for_timeout(200)
        empty = page.locator("[data-catalog-empty]").is_visible()
        check("directory: empty state shows when nothing matches", empty and page.locator("[data-card]:visible").count() == 0)
        page.locator("[data-filter-clear]").click()
        page.wait_for_timeout(200)
        check("directory: clear restores every row", page.locator("[data-card]:visible").count() == N and q.input_value() == "")
        check("directory: no script errors", not errors, "; ".join(errors[:3]))

        # 6. One tool page.
        page.goto(base + "/tools/" + tool["slug"], wait_until="networkidle")
        h1 = page.locator("h1").inner_text().strip()
        check(f"tool: /tools/{tool['slug']} h1 is the tool name", h1 == tool["name"], repr(h1))
        body = page.locator("main").inner_text()
        check("tool: vendor, what it does, and RN reality check shown", tool["vendor"] in body and tool["what"][:60] in body and "RN reality check" in body)
        href = page.locator(f'main a[href="{tool["url"]}"]').count()
        check("tool: official site link matches tools.json", href >= 1, tool["url"])
        page.screenshot(path=os.path.join(args.shots, "tool-desktop.png"), full_page=True)

        # 7. Students hub and the NCLEX guides.
        slugs = {t["slug"] for t in tools}
        resolved = {}

        def resolves(href):
            if href not in resolved:
                resolved[href] = get(base + href)[0]
            return resolved[href] == 200

        for p in ["/students"] + GUIDES:
            errors.clear()
            page.goto(base + p, wait_until="networkidle")
            h1s = [x.strip() for x in page.locator("h1:visible").all_inner_texts()]
            check(f"students: {p} has one visible h1", len(h1s) == 1 and bool(h1s[0]), repr(h1s))
            hrefs = page.eval_on_selector_all("a[href^='/']", "els => [...new Set(els.map(a => a.getAttribute('href')))]")
            tool_links = [h for h in hrefs if h.startswith("/tools/")]
            unknown = [h for h in tool_links if h[len("/tools/"):] not in slugs]
            check(f"students: {p} tool links name tools in tools.json", tool_links and not unknown, f"{len(tool_links)} tool links" + (f"; unknown {unknown[:5]}" if unknown else ""))
            dead = [h for h in hrefs if not resolves(h)]
            check(f"students: {p} every on-site link is 200", not dead, f"{len(hrefs)} links" + (f"; dead {[(h, resolved[h]) for h in dead[:5]]}" if dead else ""))
            check(f"students: {p} has the newsletter form", page.locator('form[action="/api/subscribe"]').count() == 1)
            if p == "/students":
                missing = [g for g in GUIDES if g not in hrefs]
                check("students: hub links all four NCLEX guides", not missing, f"missing {missing}" if missing else "")
            check(f"students: {p} no script errors", not errors, "; ".join(errors[:3]))

        # 8. Newsletter signup, against this local server only.
        posts = []
        page.on("request", lambda r: posts.append(r.url) if r.method == "POST" else None)

        def signup(email, pg=page, path="/"):
            pg.goto(base + path, wait_until="networkidle")
            posts.clear()
            form = pg.locator('form[action="/api/subscribe"]')
            form.locator("input[type=email]").fill(email)
            form.locator("button").click()
            msg = form.locator("[data-form-message]")
            pg.wait_for_function("el => el.textContent.trim().length > 0", arg=msg.element_handle())
            pg.wait_for_load_state("networkidle")
            return list(posts), msg.inner_text().strip()

        page.goto(base + "/", wait_until="networkidle")
        forms = page.locator('form[action="/api/subscribe"]').count()
        if not check("signup: newsletter form on home posts to /api/subscribe", forms == 1, f"{forms} forms"):
            raise RuntimeError("no newsletter form to drive")
        email = f"verify+{int(time.time())}@example.invalid"
        sent, msg = signup(email)
        check("signup: local subscribe succeeds", sent == [base + "/api/subscribe"] and "subscribed" in msg.lower(), f"posted {len(sent)}, {msg!r}")
        page.locator("section.news, form[action='/api/subscribe']").first.screenshot(path=os.path.join(args.shots, "signup-desktop.png"))
        sent, msg = signup("not-an-email")
        check("signup: bad address is refused before it is sent", not sent and "subscribed" not in msg.lower(), f"posted {len(sent)}, {msg!r}")
        # The same form on a guide, on a phone, in dark.
        phone = new_page(390, 844, "dark")
        phone.on("request", lambda r: posts.append(r.url) if r.method == "POST" else None)
        email2 = f"verify+{int(time.time())}-phone@example.invalid"
        sent, msg = signup(email2, phone, GUIDES[0])
        check(f"signup: local subscribe succeeds from {GUIDES[0]} mobile dark", sent == [base + "/api/subscribe"] and "subscribed" in msg.lower(), f"posted {len(sent)}, {msg!r}")
        phone.locator("form[action='/api/subscribe']").screenshot(path=os.path.join(args.shots, "signup-mobile-dark.png"))
        phone.context.close()
        if args.harness == "wrangler":
            rows = run(["npx", "wrangler", "d1", "execute", "nurseaitools", "--local", "--persist-to", persist, "--json",
                        "--command", "select email from subscribers"], env=local_env())
            stored = re.findall(r'"email": "([^"]+)"', rows.stdout)
            check("signup: both rows stored in local D1, nothing else", sorted(stored) == sorted([email, email2]), f"rows {stored}")
        else:
            note("signup: row stored", "serve.mjs stub DB stores nothing, verified-unreachable with --harness serve")

        # 9. Layout, type size, control size, and contrast on rendered pages.
        audit_js = open(os.path.join(os.path.dirname(__file__), "audit.js")).read()
        targets = ["/", "/tools/" + tool["slug"], "/students"] + GUIDES + ["/submit", "/discuss"]
        for scheme in [s for s in args.schemes.split(",") if s]:
            for vname, w, h in (("desktop", 1280, 800), ("mobile", 390, 844)):
                shots = {"/": "home", "/tools/" + tool["slug"]: "tool", "/students": "students", "/discuss": "discuss"} if scheme == "light" or len(args.schemes.split(",")) == 1 else {}
                for p in targets:
                    # A fresh tab per page keeps Chrome small. The box runs other lanes and a reused tab has crashed here.
                    pg = new_page(w, h, scheme)
                    pg.goto(base + p, wait_until="networkidle")
                    r = pg.evaluate(audit_js, {"minFont": args.min_font, "minControl": args.min_control, "minLink": args.min_link, "minContrast": args.min_contrast})
                    where = f"{p} {vname} {scheme}"
                    h1s = pg.locator("h1:visible").count()
                    check(f"style: one visible h1 {where}", h1s == 1, f"{h1s} visible")
                    check(f"style: no sideways scroll {where}", r["scrollWidth"] <= w, f"scrollWidth {r['scrollWidth']}")
                    check(f"style: text >= {args.min_font:g}px {where}", not r["small"], "; ".join(r["small"][:3]))
                    check(f"style: controls >= {args.min_control:g}px, links meet {args.min_link:g}px target spacing {where}", not r["short"], "; ".join(r["short"][:3]))
                    check(f"style: text contrast >= {args.min_contrast:g}:1 {where}", not r["low"], f"{r['texts']} text nodes" + ("; " + "; ".join(r["low"][:3]) if r["low"] else ""))
                    if p in shots:
                        pg.screenshot(path=os.path.join(args.shots, f"{shots[p]}-{vname}.png"), full_page=(p != "/"))
                    if p in GUIDES:
                        pg.screenshot(path=os.path.join(args.shots, f"guide-{p.rsplit('/', 1)[1]}-{vname}-{scheme}.png"), full_page=True)
                    pg.context.close()

        check("safety: the browser made no off-box requests", not offbox, "; ".join(sorted(set(offbox))[:3]))
        browser.close()
except Exception as err:
    check("run: no unexpected error", False, f"{type(err).__name__}: {str(err).splitlines()[0][:300]}")
finally:
    stop()
summary_and_exit()
