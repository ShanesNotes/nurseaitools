# Canonicals and the sitemap

Search Console reports some URLs as "Alternate page with proper canonical". That is its label for a copy that points at another URL as the original. It is expected for the copies below, and it is not an indexing error.

## Where the copies come from

- **Trailing slashes.** The worker strips trailing slashes before the route lookup, so `/students/` and `/students//` serve the `/students` page with a 200. It does not redirect.
- **Query strings.** The query is ignored, so `/?q=sepsis` and `/tools/abridge?utm_source=x` serve the clean page.
- **www.** `www.nurseaitools.com` gets a 301 to the apex with the path and query kept. Live https was spot-checked by hand on 2026-10-25: `https://www.nurseaitools.com/students/?q=1` 301s to `https://nurseaitools.com/students/?q=1`.
- **workers.dev.** `workers_dev = true` in `wrangler.toml`, so the worker also answers on its `*.workers.dev` host. Those copies point at the apex.
- **http.** The worker does not redirect http to https. That is up to the zone's "Always Use HTTPS" setting, which this skill cannot see.

Each copy names `https://nurseaitools.com<clean path>` as its canonical, so Google folds it into the original.

## What verify.py checks

See SKILL.md step 5. Every built page names itself. The sitemap equals the set of canonicals. Every page's four copies point back at it. www 301s, workers.dev copies point at the apex, and internal links use the canonical form.

## Known site bug

The 404 page (`NOT_FOUND` in `build.py`) is built with `page(..., "/")`, so it says canonical `https://nurseaitools.com/`. It is served with status 404, which Google drops, so it does not cause the Search Console label. It is still wrong. The check is a SKIP until `build.py` drops it.
