# Feature map

The preview is the worker from `python3 build.py`, served by `node serve.mjs` on port 8787.

| Feature | Path | Automated drive |
| --- | --- | --- |
| Home directory | `/` | `drive_home.py` types a query. `shoot.py` records the page. |
| Tool page | `/tools/abridge-for-nurses` | `shoot.py` records the page. Facts are checked by `test_style.py`. |
| Students hub | `/students` | `shoot.py` records the page. |
| Submit a tool | `/submit` | `shoot.py` records the page. The form state machine is `npm test`. |
