---
name: verify-nurse-ai-tools
description: Prove the Nurse AI Tools preview by building the worker, running the test suites, serving it locally, and shooting the home, tool, students, and submit pages. Use when a visual or page change needs evidence from the running site.
---

# Verify Nurse AI Tools

The site is a static worker. `python3 build.py` writes `dist/worker.js`. `node serve.mjs` serves that file on port 8787 with a stub database. Nothing in that preview calls Kit, and the stub does not store rows.

## Launch

From the repo root:

```bash
python3 build.py
node serve.mjs
```

Ready when the process prints `http://localhost:8787` and `curl -sf http://localhost:8787/` contains `Nurse AI Tools`.

One preview owns port 8787. Do not start a second one.

## Doctor

```bash
curl -sf -o /dev/null -w '%{http_code}\n' http://localhost:8787/
curl -sf http://localhost:8787/ | grep -c 'AI should run the rules in the background'
curl -sf -D - -o /dev/null http://localhost:8787/fonts/host-grotesk-latin-400-normal.woff2 | head -n 5
```

The page status is `200`. The brand line appears once. The font status is `200` and the type is `font/woff2`.

If the font is 404, the running process loaded an old worker. Stop it and start `node serve.mjs` again after `python3 build.py`.

## Drive

Automated checks, in this order:

```bash
npm test
python3 test_style.py
python3 shoot.py
python3 .agents/skills/verify-nurse-ai-tools/drive_home.py
```

`npm test` drives the catalog and form state machines in Node. `test_style.py` checks tokens, both themes, contrast, type size, tap-target rules, and page copy. `shoot.py` opens home, one tool page (GCLEX), the students hub, and submit at 1280 and 390 and fails if `scrollWidth` exceeds the viewport. It also shoots the directory in view and the newsletter signup section. `drive_home.py` types `abridge` into the home search and checks that the count changes.

`COLOR_SCHEME=dark python3 shoot.py` repeats the shots in the dark theme. `SHOTS` sets the directory. The default is `shots/`.

## Evidence

`shoot.py` writes `shots/home-desktop.png`, `shots/home-mobile.png`, `shots/tool-desktop.png`, `shots/tool-mobile.png`, `shots/students-desktop.png`, `shots/students-mobile.png`, `shots/submit-desktop.png`, `shots/submit-mobile.png`, `shots/directory-desktop.png`, `shots/directory-mobile.png`, `shots/signup-desktop.png`, and `shots/signup-mobile.png`.

`drive_home.py` writes `shots/verify/home-search.png` and prints the count before and after the query.

These files are the proof. They are gitignored. Do not delete them during cleanup.

## Cleanup

Stop the preview you started. If it is the only `serve.mjs` you launched in this session, end that process by its pid. Do not kill every `node` on the machine. Leave `shots/` in place.

## Helpers

`python3 .agents/skills/verify-nurse-ai-tools/drive_home.py` drives the home search. The preview must already be running. `BASE` defaults to `http://localhost:8787`. `CHROME` defaults to `/usr/bin/google-chrome`.

## What this does not check

- A live Kit signup. `serve.mjs` has no `KIT_API_KEY`, so the worker never calls Kit. Verified-unreachable.
- A stored D1 row. The preview stub resolves `run()` without a database. Verified-unreachable.
- A deployed worker. This environment has no deploy access.
