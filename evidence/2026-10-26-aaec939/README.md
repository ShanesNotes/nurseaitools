# Proof for fix/trailing-slash-301 at aaec939

- Revision: aaec939 (merge of origin/main 78c622f into 6c0171f)
- Surface: local worker, wrangler dev --local, fresh local D1, Chrome at 390 and 1280, light and dark
- Commands: `python3 build.py && npm test && npm run check && python3 test_style.py` (suites.txt), then `/workspace/.pwvenv/bin/python .agents/skills/verify-nurse-ai-tools/verify.py` (verify.txt, report.json)
- Result: suites exit 0. `VERIFY PASS: 233 passed, 0 skipped`. verify.txt shows trailing-slash copies 301 to the clean path (90 pages x 3 variants) and query copies stay 200 with the clean canonical.
- Not verified: the live site (no deploy)
