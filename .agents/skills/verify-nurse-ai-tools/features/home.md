# Home directory

The home page is the directory. A nurse reads the brand line, picks a door, or searches and filters the list.

## Sub-features

- `home-read` shows the title, the brand line, and the three doors.
- `home-search` narrows the list as the query is typed.
- `home-empty` shows the empty state when nothing matches.

## How to get to it (user POV)

Open `/`.

## Driving it with the preview

Preconditions:

- `node serve.mjs` is serving the worker just built.
- `curl -sf http://localhost:8787/` contains the brand line.

- **Read.** Run `python3 shoot.py`. `shots/home-desktop.png` and `shots/home-mobile.png` show the title and the brand line. scrollWidth is `ok`.
- **Search.** Run `python3 .agents/skills/verify-nurse-ai-tools/drive_home.py`. The printed `after` count is smaller than `before`, and `shots/verify/home-search.png` shows the query `abridge`.
- **Empty.** The node catalog tests cover a query that matches nothing. This browser script does not.

## Gotchas

The search runs in the browser. Reloading the page clears it. There is no server round trip.
