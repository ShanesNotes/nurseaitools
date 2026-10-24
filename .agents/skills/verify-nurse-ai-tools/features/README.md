# Feature map

`verify.py` drives every row below against the worker from `python3 build.py`, served on a free local port.

| Feature | Path | Automated drive |
| --- | --- | --- |
| Home directory | `/` | Count, rows, search, category filter, empty state, clear. See `home.md`. |
| Tool page | `/tools/<slug>` | Every tool page for status and title. One page in the browser. See `tool.md`. |
| Newsletter signup | `/` and every page with the newsletter section | Local subscribe, bad address, D1 row. See `signup.md`. |
| Students hub | `/students` | Status, head tags, and the style audit. See `students.md`. |
| Submit a tool | `/submit` | Status, head tags, and the style audit. The form machine is `npm test`. See `submit.md`. |
