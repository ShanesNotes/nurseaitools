---
name: verify-nurse-ai-tools
description: Prove a Nurse AI Tools change on this box. Builds the worker, runs the unit and style suites, serves it with wrangler dev --local and a fresh local D1, drives home, the directory, one tool page, the students hub, the four NCLEX guides, and the newsletter signup in Chrome at 390 and 1280 wide, in light and dark, checks status codes, content, type size, control size, and contrast, and prints VERIFY PASS or VERIFY FAIL with an exit code. Use before opening or merging any site change.
---

# Verify Nurse AI Tools

The site is one Cloudflare Worker. `python3 build.py` writes `dist/worker.js` from `tools.py`, `reality.py`, and the markup and CSS in `build.py`. This skill proves the build on this box. It never deploys and never talks to the live site, Cloudflare, or Kit.

## Run it

From the repo root:

```bash
/workspace/.pwvenv/bin/python .agents/skills/verify-nurse-ai-tools/verify.py
```

Use any Python that has `playwright`. Chrome is `/usr/bin/google-chrome`, or set `CHROME`. Run `npm install` once in each new checkout first; see Gotchas. A full run takes about a minute on this box (67s at 25cf14a). The time is on the revision line.

The last line is `VERIFY PASS: <n> passed, <k> skipped` with exit code 0, or `VERIFY FAIL: ...` with exit code 1 and the failed checks listed again under it.

Options:

- `--harness serve` uses `node serve.mjs` instead of wrangler. Its stub database stores nothing, so the D1 row check is skipped as verified-unreachable. Use it only if wrangler will not start.
- `--skip-unit` skips `npm test` and `python3 test_style.py`, for fast reruns while you work. Do not skip them for evidence.
- `--tool <slug>` picks the tool page. The default is the first Education / NCLEX tool.
- `--schemes light` audits one color scheme. The default audits light and dark.
- `--min-font`, `--min-control`, `--min-link`, `--min-contrast` set the floors. The defaults are what both the current `DESIGN.md` and the Market redesign say: 12px text, 44px controls, 4.5:1 text (3:1 for large text), and the WCAG 2.5.8 24px target rule for stand-alone links.
- `--shots <dir>` sets the evidence directory. The default is `shots/verify/`.

## What it does

1. **Build.** `python3 build.py` exits 0 and prints the same tool count as `tools.json`.
2. **Suites.** `npm test` (the catalog and form machines) and `python3 test_style.py` (the rules in whichever `DESIGN.md` the checkout ships) both pass.
3. **Serve.** Seeds a new local D1 in a temp dir from `schema.sql`, then starts `wrangler dev --local` on a free port bound to 127.0.0.1. Every child process gets an env with `CF_*`, `CLOUDFLARE_*`, and `KIT_*` removed, so it cannot authenticate to Cloudflare or post to Kit. If `.dev.vars` or `.env` sets `KIT_API_KEY`, the run stops before the signup.
4. **HTTP.** The four NCLEX guides are in `/sitemap.xml`. Every URL in it returns 200 with a title, a meta description, a canonical to `https://nurseaitools.com<path>`, and exactly one `h1`. Every tool in `tools.json` is in the sitemap and its title names it. An unknown path is 404. `/tools` is 404 too: the directory lives on `/` and there is no `/tools` index. Do not read that 404 as a bug. If a `/tools` route ships on purpose, change that check and this line. `/robots.txt` and every `/js/*` module load. If the page declares `/fonts/*` faces, each must load. A design with no webfont skips that check.
5. **Home and directory.** The count reads `<N> tools` and there are N rows, one per name in `tools.json`. Search `abridge` narrows to exactly the rows whose name, vendor, or description match. The category filter shows the same number of rows as `tools.json` has in that category. A nonsense query shows the empty state, and Clear brings back every row. No script errors.
6. **Tool page.** The `h1` is the tool name. The vendor, description, and RN reality check are shown. The official site link matches `tools.json`.
7. **Students.** In Chrome at 1280 wide, `/students` and each NCLEX guide (`/students/best-ai-nclex-prep`, `/students/free-nclex-prep`, `/students/ngn-practice-tools`, `/students/chatgpt-for-nclex`) has exactly one visible `h1`. It has at least one tool link, and every `/tools/<slug>` link names a slug in `tools.json`. Every on-site link answers 200. It has the newsletter form and no script errors. The hub links all four guides.
8. **Signup.** Fills the home newsletter form at 1280 wide, light, with `verify+<time>@example.invalid`. Then it fills the form on `/students/best-ai-nclex-prep` at 390 wide, dark, with `verify+<time>-phone@example.invalid`. Each good submit makes exactly one POST, to the local `/api/subscribe`, and the reply says subscribed. Those two addresses are the only rows in the local D1 `subscribers` table. A bad address is refused in the browser and nothing is posted.
9. **Style.** On home, the tool page, `/students`, the four NCLEX guides, and `/submit`, at 1280 and 390 wide, in each scheme, each in a fresh tab: exactly one visible `h1`; no sideways scroll; no rendered text under the minimum size; every button, field, select, and checkbox label at least the control height; stand-alone links meet the WCAG 2.5.8 target rule; every visible text node meets the contrast floor against its composited background.
10. **Safety.** The browser blocks and reports any request that is not to the local server. The check passes only if there were none.

These hooks are shared by both designs and are what the script keys on: `data-catalog`, `data-card`, `data-filter-query`, `data-filter-category`, `data-filter-clear`, `data-catalog-count`, `data-catalog-empty`, `data-form-message`, and `form[action="/api/subscribe"]`. The script reads computed styles, not token names, so a token rename does not break it.

## Evidence

`shots/verify/` holds:

- `report.json`: revision, harness, every check, and its detail.
- `home-desktop.png` and `home-mobile.png`.
- `tool-desktop.png` and `tool-mobile.png`.
- `students-desktop.png` and `students-mobile.png`.
- `guide-<slug>-<desktop|mobile>-<light|dark>.png`: 16 full-page shots of the NCLEX guides.
- `directory-search.png`.
- `signup-desktop.png` and `signup-mobile-dark.png`.

Every shot except the home pair is full page. `shots/` is gitignored. Copy what you need into the PR.

Quote in the PR: the revision line, the `VERIFY PASS` line, the command, and any SKIP lines.

A change to this skill keeps a small copy of its own proof in `evidence/<date>-<revision>/`: the output, `report.json`, and a few shots. Site changes do not commit evidence here.

## Cleanup

The script stops the server it started by process group. The temp D1 dir and the server log under `/tmp/nai-verify-*` are left for inspection and are safe to delete. It never kills other `node` or `wrangler` processes.

## Manual preview

To look at the site yourself:

```bash
python3 build.py
node serve.mjs            # http://localhost:8787, or PORT=<n> node serve.mjs
```

`python3 .agents/skills/verify-nurse-ai-tools/drive_home.py` types a query into the home search of that preview and checks the count changes. `verify.py` already does this and more.

## Gotchas

- Ports 8790, 8791, and 8799 on this box belong to the sandbox egress tunnel. A request there returns 400 from the tunnel, not from the worker. The script picks a free port, so it is not affected.
- wrangler 3 warns that its runtime is older than `compatibility_date`. The worker does not use newer features, so the warning is harmless here.
- `serve.mjs` and wrangler both read `dist/worker.js` once at start. Rebuild, then restart.
- A fresh checkout has no `node_modules`. Without `npm install`, `npx wrangler` finds a newer global wrangler on the box. Its workerd may not support the worker's `compatibility_date`. The server never answers, and the log says `requires compatibility date "2026-10-01"`. Run `npm install`, which pins wrangler 3, and rerun. This is setup, not a site bug.
- The box runs other lanes, and Chrome has run out of memory here when one tab audited every page. The style pass opens a fresh tab per page. If you see `Target crashed`, check `free -g` before you suspect the site.
- The fonts check used to be the run's one skip, because the old design loaded no webfont. The Market redesign self-hosts its fonts, so it now runs, and a normal wrangler run has no skips. A new SKIP line means something changed. Explain it in the PR.

## What this does not check

- A live Kit signup. No Kit key reaches the local worker. Verified-unreachable.
- The remote D1 database and a deployed worker. This skill has no deploy path. Verified-unreachable.
- Real phones and Safari. The phone pass is Chrome at 390 wide.
