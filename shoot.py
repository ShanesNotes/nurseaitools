# Usage: python3 build.py && node serve.mjs &  then  /workspace/side-hustle/.venv/bin/python shoot.py [base]
import sys, os
from playwright.sync_api import sync_playwright
base = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8787'
out = '/workspace/nurseaitools/shots'; os.makedirs(out, exist_ok=True)
pages = [('home', '/'), ('tool', '/tools/notebooklm'), ('students', '/students'), ('nclex', '/students/nclex-ai-tutors'), ('submit', '/submit'), ('about', '/about')]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
    for vname, w, h in [('desktop', 1280, 800), ('mobile', 390, 844)]:
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        for name, path in pages:
            pg.goto(base + path); pg.wait_for_load_state('networkidle')
            sw = pg.evaluate('document.documentElement.scrollWidth')
            print(vname, name, 'scrollWidth', sw, 'OVERFLOW' if sw > w else 'ok')
            pg.screenshot(path=f'{out}/{name}-{vname}.png', full_page=True)
    b.close()
