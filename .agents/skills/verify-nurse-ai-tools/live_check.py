#!/usr/bin/env python3
"""Post-deploy live check: the site is up on the apex, and workers.dev does not serve it.

Usage, from the repo root, after every deploy:
  python3 .agents/skills/verify-nurse-ai-tools/live_check.py

Plain HTTPS GETs only. No Cloudflare API, no token. Prints LIVE PASS or LIVE FAIL and exits 0 or 1.
wrangler.toml sets workers_dev = false and deploy.js sends {enabled:false, previews_enabled:false}.
If a deploy turns the subdomain back on, workers.dev serves a second copy of the site, and this fails.
"""
import sys
import urllib.error
import urllib.request

APEX = "https://nurseaitools.com/"
WORKERS_DEV = "https://nurseaitools.lectionary-web.workers.dev/"
# Markup only the site's own pages carry. Cloudflare's error pages carry none of it.
SITE_MARKERS = ('href="https://nurseaitools.com/"', "Nurse AI Tools")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def get(url):
    """(status, body) without following redirects. status is None if no HTTP reply came back."""
    req = urllib.request.Request(url, headers={"User-Agent": "nurseaitools-live-check/1"})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError) as e:
        return None, str(e)


def is_site(body):
    return any(m in body for m in SITE_MARKERS)


failed = []


def check(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        failed.append(name)


st, body = get(APEX)
check("apex serves the site", st == 200 and is_site(body), f"GET {APEX} -> {st}")

st, body = get(WORKERS_DEV)
code = "1042" if "1042" in body else ""
detail = f"GET {WORKERS_DEV} -> {st if st is not None else 'no reply (' + body + ')'}{' error ' + code if code else ''}"
# Pass on a 4xx/5xx or no reply, with none of the site's markup. A 2xx or 3xx means workers.dev answers for the site again.
check("workers.dev does not serve the site", (st is None or st >= 400) and not is_site(body), detail)

if failed:
    print(f"LIVE FAIL: {', '.join(failed)}. If workers.dev is serving, the last deploy turned the subdomain on; see SKILL.md.")
    sys.exit(1)
print("LIVE PASS: 2 passed")
