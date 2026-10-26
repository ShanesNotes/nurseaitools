# UX pass, Oct 25, 2026

A user-experience pass on Nurse AI Tools, walked as four people: a staff nurse, a nurse manager, a nursing student, and a nurse educator. The yardstick is Shane's: does this help a nurse or student find the right AI for their situation and start using it well?

- Stories with steps, expected outcomes and acceptance checks: [user-stories.md](user-stories.md)
- The Playwright suite that encodes them: [`e2e/`](../../e2e)
- Finding screenshots: [`screenshots/findings/`](screenshots/findings), epic prototypes: [`screenshots/prototypes/`](screenshots/prototypes), fix after-shots: [`screenshots/fixes/`](screenshots/fixes)
- How the shots and prototypes were made: [`prototypes/shoot.py`](prototypes/shoot.py). Prototypes are the real pages with markup injected in the browser, so they use the shipped CSS. Dates and copy in prototypes are placeholders, not facts about any tool.

## Run the suite

```sh
npm install                 # once per checkout; @playwright/test is a devDependency
npm run e2e                 # local build: python3 build.py, then wrangler dev --local with a fresh local D1
npm run e2e -- -g SN-2      # one story
npm run e2e:live            # read-only against https://nurseaitools.com
```

- **Local** (default). `playwright.config.ts` starts `python3 build.py && node e2e/serve.mjs`. `serve.mjs` seeds a temp D1 from `schema.sql` and runs `wrangler dev --local` on 127.0.0.1, with `CF_*`, `CLOUDFLARE_*` and `KIT_*` removed from the env, as `verify.py` does. The browser aborts and reports any request that leaves the local server. Signups go to the local D1 only.
- **Live** (`E2E_LIVE=1`). GET and navigation only. Every non-GET request is aborted in the browser before it leaves, and the test fails if one was attempted. Signup specs fill the field and stop before Subscribe. `ALL.a` proves the guard by trying a `POST /api/submit` and checking that it was blocked. Live loads Cloudflare Web Analytics; the suite blocks that beacon too and does not count it as a failure.
- Four projects: `phone-light`, `phone-dark` (390x844), `desktop-light`, `desktop-dark` (1280x800). Two workers, so a busy box is not overloaded. Chrome is `/usr/bin/google-chrome` or `$CHROME`; nothing is downloaded.
- Other env: `E2E_PORT` (default 8812), `E2E_BASE_URL` (use a server that is already running), `E2E_WORKERS`.
- Open findings are encoded with `test.fail()` and the issue number. They report as expected failures. When a fix lands, the test reports "Expected to fail, but passed"; then delete that `test.fail()` line.

## Results

See the PR for the exact runs: head sha, command, and counts.

| Mode | Result |
| --- | --- |
| Local, main build (`npm run e2e`) | 156 tests: 100 passed, 48 expected failures (the 12 open checks x 4 projects), 8 skipped (live-only), 0 unexpected. 2.3 min, 2 workers |
| Live, read-only (`npm run e2e:live`, deploy 25cf14a) | 156 tests: 104 passed, 48 expected failures, 4 skipped (local-only signup), 0 unexpected. Every open check reproduces on live. No POST left the browser |
| Fix branches | `SN-2.c` and `SN-3.c` pass against [#34](https://github.com/ShanesNotes/nurseaitools/pull/34) in all four projects |

## Severity

- **S1** blocks the core job or gives unsafe information. None found.
- **S2** misleads the reader or breaks a core flow.
- **S3** friction with a workaround, or a missing step in a core story.
- **S4** polish.

## Findings

| Sev | Issue | Story | Where | Fix |
| --- | --- | --- | --- | --- |
| S2 | [#13](https://github.com/ShanesNotes/nurseaitools/issues/13) After Back, the list shows every tool under filters that look applied | SN-2.c | main + live | [#34](https://github.com/ShanesNotes/nurseaitools/pull/34) |
| S2 | [#14](https://github.com/ShanesNotes/nurseaitools/issues/14) "HIPAA-ready" filter promises more than the data | SN-4.b | main + live | [#35](https://github.com/ShanesNotes/nurseaitools/pull/35) |
| S3 | [#15](https://github.com/ShanesNotes/nurseaitools/issues/15) No checked date on Unknown and study-tool pages | SN-4.c | main + live | epic [#8](https://github.com/ShanesNotes/nurseaitools/issues/8) |
| S3 | [#16](https://github.com/ShanesNotes/nurseaitools/issues/16) Tool pages do not link how listings work | SN-4.d | main + live | epic [#8](https://github.com/ShanesNotes/nurseaitools/issues/8) |
| S3 | [#17](https://github.com/ShanesNotes/nurseaitools/issues/17) "Reviewed by a nurse" vs vendor-sourced listings | NM-4 | main + live | Shane's call |
| S3 | [#18](https://github.com/ShanesNotes/nurseaitools/issues/18) "charting" finds nothing | SN-2.d | main + live | epic [#9](https://github.com/ShanesNotes/nurseaitools/issues/9) |
| S3 | [#19](https://github.com/ShanesNotes/nurseaitools/issues/19) Multi-word search is exact phrase | NM-2.b | main + live | epic [#9](https://github.com/ShanesNotes/nurseaitools/issues/9) |
| S3 | [#20](https://github.com/ShanesNotes/nurseaitools/issues/20) `?q=` links ignored | NM-1.c | main + live | epic [#9](https://github.com/ShanesNotes/nurseaitools/issues/9) |
| S3 | [#21](https://github.com/ShanesNotes/nurseaitools/issues/21) Back link lands on the hero | SN-3.c | main + live | [#34](https://github.com/ShanesNotes/nurseaitools/pull/34) |
| S3 | [#22](https://github.com/ShanesNotes/nurseaitools/issues/22) Tool page is a dead end | SN-3.d | main + live | epic [#12](https://github.com/ShanesNotes/nurseaitools/issues/12) |
| S3 | [#23](https://github.com/ShanesNotes/nurseaitools/issues/23) Phone: filters scroll away in 79 rows | ST-2 | main + live | epic [#9](https://github.com/ShanesNotes/nurseaitools/issues/9) |
| S3 | [#24](https://github.com/ShanesNotes/nurseaitools/issues/24) Home newsletter after all 79 rows | SN-5 | main + live | epic [#10](https://github.com/ShanesNotes/nurseaitools/issues/10) |
| S4 | [#25](https://github.com/ShanesNotes/nurseaitools/issues/25) 404: canonical "/", no noindex, Directory current | ALL.f | main + live | [#32](https://github.com/ShanesNotes/nurseaitools/pull/32) |
| S4 | [#26](https://github.com/ShanesNotes/nurseaitools/issues/26) Search Console "Alternate page with proper canonical" explained | SN-1.e | live | [#33](https://github.com/ShanesNotes/nurseaitools/pull/33), [#36](https://github.com/ShanesNotes/nurseaitools/pull/36) |
| S4 | [#27](https://github.com/ShanesNotes/nurseaitools/issues/27) Sitemap lastmod fixed at 2026-10-17 | NM-1 | main + live | proposed |
| S4 | [#28](https://github.com/ShanesNotes/nurseaitools/issues/28) Empty state wording, no next step | NM-2 | main + live | epic [#9](https://github.com/ShanesNotes/nurseaitools/issues/9) |
| S4 | [#29](https://github.com/ShanesNotes/nurseaitools/issues/29) Search clear "x" is Chrome blue | SN-2 | main + live | proposed |
| S4 | [#30](https://github.com/ShanesNotes/nurseaitools/issues/30) Abridge does not link Abridge for Nurses | SN-3 | main + live | epic [#12](https://github.com/ShanesNotes/nurseaitools/issues/12) |
| S4 | [#31](https://github.com/ShanesNotes/nurseaitools/issues/31) Official site opens a new tab without saying so | SN-3 | main + live | proposed |

Epics, each with a proposed design and prototype shots: [#8](https://github.com/ShanesNotes/nurseaitools/issues/8) trust and vetting signals, [#9](https://github.com/ShanesNotes/nurseaitools/issues/9) discovery (task-first browsing, search, filters), [#10](https://github.com/ShanesNotes/nurseaitools/issues/10) newsletter value proposition, [#11](https://github.com/ShanesNotes/nurseaitools/issues/11) entry points for managers and educators, [#12](https://github.com/ShanesNotes/nurseaitools/issues/12) starter steps and comparisons.

Main vs live: every finding above reproduces on both. The only main-only difference seen is content: main lists 79 tools (Healthleap added Oct 25), and live lists 78.

No manual browser-walk log (`/workspace/lanes/logs/ux-browser-walk.md`) existed when this pass ran, so there was nothing to fold in.

## Gallery

Main at the commit in the PR. 390x844 and 1280x800, first screen.

| Page | 390 light | 390 dark | 1280 light | 1280 dark |
| --- | --- | --- | --- | --- |
| home | ![](screenshots/gallery/home-390-light.png) | ![](screenshots/gallery/home-390-dark.png) | ![](screenshots/gallery/home-1280-light.png) | ![](screenshots/gallery/home-1280-dark.png) |
| directory-filtered | ![](screenshots/gallery/directory-filtered-390-light.png) | ![](screenshots/gallery/directory-filtered-390-dark.png) | ![](screenshots/gallery/directory-filtered-1280-light.png) | ![](screenshots/gallery/directory-filtered-1280-dark.png) |
| tool | ![](screenshots/gallery/tool-390-light.png) | ![](screenshots/gallery/tool-390-dark.png) | ![](screenshots/gallery/tool-1280-light.png) | ![](screenshots/gallery/tool-1280-dark.png) |
| students | ![](screenshots/gallery/students-390-light.png) | ![](screenshots/gallery/students-390-dark.png) | ![](screenshots/gallery/students-1280-light.png) | ![](screenshots/gallery/students-1280-dark.png) |
| guide | ![](screenshots/gallery/guide-390-light.png) | ![](screenshots/gallery/guide-390-dark.png) | ![](screenshots/gallery/guide-1280-light.png) | ![](screenshots/gallery/guide-1280-dark.png) |
| about | ![](screenshots/gallery/about-390-light.png) | ![](screenshots/gallery/about-390-dark.png) | ![](screenshots/gallery/about-1280-light.png) | ![](screenshots/gallery/about-1280-dark.png) |
| submit | ![](screenshots/gallery/submit-390-light.png) | ![](screenshots/gallery/submit-390-dark.png) | ![](screenshots/gallery/submit-1280-light.png) | ![](screenshots/gallery/submit-1280-dark.png) |
| 404 | ![](screenshots/gallery/404-390-light.png) | ![](screenshots/gallery/404-390-dark.png) | ![](screenshots/gallery/404-1280-light.png) | ![](screenshots/gallery/404-1280-dark.png) |
