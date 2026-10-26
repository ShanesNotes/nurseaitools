PR #37 Codex follow-up, 2026-10-26
Code under test: b4cc686 (branch ux/e2e-stories rebased on origin/main 78c622f) plus the working-tree edits committed with this file
(e2e/site.spec.ts drops the ALL.f test.fail marker; docs/ux README and user-stories).
Surface: local build only, wrangler dev --local with a fresh temp D1. No live site, Cloudflare or Kit.

1. python3 build.py && npm test && npm run check && python3 test_style.py   -> exit 0 (suite.log). npm test 43/43.
2. /workspace/.pwvenv/bin/python .agents/skills/verify-nurse-ai-tools/verify.py   -> VERIFY PASS: 232 passed, 0 skipped, exit 0 (verify.log).
   Ran at b4cc686; the later edits touch only e2e specs and docs, which verify.py does not read.
   Its 26 screenshots stay on the box in shots/verify/pr37/ (gitignored); nothing visual changed.
3. npm run e2e   -> exit 0: 104 passed, 44 expected failures (11 open checks x 4 projects), 8 skipped (live-only), 0 unexpected (e2e.log).
   First run before dropping the marker: 4 unexpected passes of ALL.f, because #32 fixed the 404 on main.
4. Guard check: with a .dev.vars containing KIT_API_KEY=dummy, node e2e/serve.mjs prints the refusal and exits 1 before seeding D1. File removed after.
Not verified: live e2e (npm run e2e:live) not rerun; nothing in this change reaches the live site.
