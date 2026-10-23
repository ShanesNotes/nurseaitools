#!/usr/bin/env python3
import os
import sys

from playwright.sync_api import sync_playwright

base = os.environ.get("BASE", "http://localhost:8787")
out = os.environ.get("SHOTS", "shots/verify")
chrome = os.environ.get("CHROME", "/usr/bin/google-chrome")
os.makedirs(out, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=chrome)
    page = browser.new_page(viewport={"width": 1280, "height": 800}, device_scale_factor=1)
    page.goto(base + "/", wait_until="networkidle")
    before = page.locator("[data-catalog-count]").inner_text()
    page.locator("[data-filter-query]").fill("abridge")
    page.locator("[data-catalog-count]").wait_for()
    after = page.locator("[data-catalog-count]").inner_text()
    visible = page.locator("[data-card]:visible").count()
    page.screenshot(path=os.path.join(out, "home-search.png"))
    browser.close()

print("before", before)
print("after", after)
print("visible", visible)
if before == after or visible < 1 or not after.endswith("of " + before):
    sys.exit(1)
print("ok")
