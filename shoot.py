"""Usage: python3 build.py && node serve.mjs &  then  python3 shoot.py [base]

Writes full-page PNGs and prints scrollWidth. Exits 1 if a page is wider than its viewport.
SHOTS sets the output directory. COLOR_SCHEME is light or dark. CHROME is the browser binary.
"""
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
    ("tool", "/tools/abridge-for-nurses"),
    ("students", "/students"),
    ("submit", "/submit"),
]
failed = False
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome)
    for vname, width, height in (("desktop", 1280, 800), ("mobile", 390, 844)):
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1, color_scheme=scheme)
        for name, path in pages:
            page.goto(base + path, wait_until="networkidle")
            scroll = page.evaluate("document.documentElement.scrollWidth")
            overflow = scroll > width
            failed = failed or overflow
            print(vname, name, "scrollWidth", scroll, "OVERFLOW" if overflow else "ok")
            suffix = "" if scheme == "light" else f"-{scheme}"
            page.screenshot(path=f"{out}/{name}-{vname}{suffix}.png", full_page=True)
        page.close()
    browser.close()
print("wrote", out)
sys.exit(1 if failed else 0)
