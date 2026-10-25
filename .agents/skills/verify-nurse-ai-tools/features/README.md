# Feature map

`verify.py` drives every row below against the worker from `python3 build.py`, served on a free local port.

| Feature | Path | Automated drive |
| --- | --- | --- |
| Home directory | `/` (there is no `/tools` index; it is 404 for now) | Count, rows, search, category filter, empty state, clear. See `home.md`. |
| Tool page | `/tools/<slug>` | Every tool page for status and title. One page in the browser. See `tool.md`. |
| Newsletter signup | `/` and every page with the newsletter section | Local subscribe from home (desktop, light) and from an NCLEX guide (390 wide, dark), bad address, D1 rows. See `signup.md`. |
| Students hub | `/students` | Status, head tags, one visible `h1`, tool links, on-site links, guide links, and the style audit. See `students.md`. |
| Students NCLEX guides | `/students/best-ai-nclex-prep`, `/students/free-nclex-prep`, `/students/ngn-practice-tools`, `/students/chatgpt-for-nclex` | Sitemap, one visible `h1`, tool links, on-site links, newsletter form, signup, and the style audit at both widths in both schemes. See `students-nclex.md`. |
| Forum | `/discuss` | Empty page, 401 and 403 gates, migration applied, style audit, screenshots. See `discuss.md`. |
| Submit a tool | `/submit` | Status, head tags, and the style audit. The form machine is `npm test`. See `submit.md`. |
| Canonicals and sitemap | every page, plus `/`, `//`, `?query`, www, and workers.dev copies | One self canonical per built page, sitemap equals the canonicals, copies point at the clean URL, www 301, internal links canonical, 404 canonical (known SKIP). See `canonical.md`. |
