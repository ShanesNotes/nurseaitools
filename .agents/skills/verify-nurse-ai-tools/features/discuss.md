# Forum (discuss)

The forum foundation (F1): an empty `/discuss` page in the site shell, the forum routes, and the session helpers. Sign-in (F2) and threads (F3) are not built yet.

## Sub-features

- `discuss-page` renders the empty index from the `page()` shell at request time.
- `forum-gates` refuses a POST with a foreign or missing `Origin` (403) and a member POST without a valid session (401).
- `forum-schema` is `migrations/0002_forum.sql`. It has no report, mod, role, ban, or hold tables or columns.

## How to get to it (user POV)

Go to `/discuss`. It is not in the nav or the sitemap yet.

## Driving it

`verify.py` applies the migration to the fresh local D1, checks `/discuss` and both gates over HTTP, runs the style audit on `/discuss` at both widths, and saves `discuss-desktop.png` and `discuss-mobile.png`. `test/forum.test.js` covers sessions, cookie flags, sliding expiry, and the schema against the inlined `deploy.js` worker in Miniflare.

## Gotchas

No forum route sets a cookie yet except the sliding refresh. A real sign-in loop arrives with F2.
