# Tool page

A tool page is one listing. The reality check is the part a nurse came to read.

## Sub-features

- `tool-facts` shows the name, vendor, what it does, and the RN reality check.
- `tool-source` links to the vendor site.

## How to get to it (user POV)

Open a tool from the directory, or go to `/tools/<slug>`.

## Driving it

Over HTTP, `verify.py` loads every `/tools/<slug>` in `tools.json` and checks status 200, head tags, one `h1`, and a title that names the tool. In the browser it opens one page, the first Education / NCLEX tool unless `--tool` says otherwise, and checks the `h1`, the vendor, the description, the reality check, and that the official site link matches `tools.json`.

## Gotchas

Only one tool page is screenshotted. `test_style.py` checks every tool page's facts as HTML.
