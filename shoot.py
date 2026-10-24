import os
import sys

from playwright.sync_api import sync_playwright

base = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8787"
out = os.environ.get("SHOTS", "shots")
scheme = os.environ.get("COLOR_SCHEME", "light")
chrome = os.environ.get("CHROME", "/usr/bin/google-chrome")
os.makedirs(out, exist_ok=True)
pages = [
    ("home", "/"),
    ("tool", "/tools/gclex"),
    ("students", "/students"),
    ("submit", "/submit"),
]
failed = False
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome)
    for vname, width, height in (("desktop", 1280, 800), ("mobile", 390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1, color_scheme=scheme)
        suffix = "" if scheme == "light" else f"-{scheme}"
        for name, path in pages:
            page.goto(base + path, wait_until="networkidle")
            scroll = page.evaluate("document.documentElement.scrollWidth")
            overflow = scroll > width
            failed = failed or overflow
            print(vname, name, "scrollWidth", scroll, "OVERFLOW" if overflow else "ok")
            page.screenshot(path=f"{out}/{name}-{vname}{suffix}.png", full_page=True)
        page.goto(base + "/", wait_until="networkidle")
        page.evaluate("document.querySelector('[data-catalog]').scrollIntoView()")
        page.screenshot(path=f"{out}/directory-{vname}{suffix}.png")
        page.locator("section.news").screenshot(path=f"{out}/signup-{vname}{suffix}.png")
        print(vname, "directory and signup")
        page.close()
    browser.close()
print("wrote", out)
sys.exit(1 if failed else 0)
