#!/usr/bin/env python3
"""Post-deploy live check: the site is up on the apex, and workers.dev does not serve it.

Usage, from the repo root, after every deploy:
  NAT_WORKERS_DEV_URL=https://<workers-dev-subdomain>/ python3 .agents/skills/verify-nurse-ai-tools/live_check.py

Plain HTTPS GETs only. No Cloudflare API, no token. Prints LIVE PASS or LIVE FAIL and exits 0 or 1.
The workers.dev host is NAT_WORKERS_DEV_URL. It has no default. Unset, that GET is skipped
and the check still covers the public custom domain.
wrangler.toml sets workers_dev = false and deploy.js sends {enabled:false, previews_enabled:false}.
If a deploy turns the subdomain back on, workers.dev serves a second copy of the site, and this fails.
"""
import os
import sys
import urllib.error
import urllib.request

APEX = "https://nurseaitools.com/"
# The account workers.dev host is not stored in the repo. Set NAT_WORKERS_DEV_URL
# to that origin to check it. There is no default. Unset, this script checks only
# the public custom domain.
WORKERS_DEV = os.environ.get("NAT_WORKERS_DEV_URL", "").strip()
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
passed = []
skipped = []


def check(name, ok, detail):
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    (passed if ok else failed).append(name)


def skip(name, detail):
    print(f"SKIP {name}: {detail}")
    skipped.append(name)


st, body = get(APEX)
check("apex serves the site", st == 200 and is_site(body), f"GET {APEX} -> {st}")

if WORKERS_DEV:
    st, body = get(WORKERS_DEV)
    code = "1042" if "1042" in body else ""
    detail = f"GET {WORKERS_DEV} -> {st if st is not None else 'no reply (' + body + ')'}{' error ' + code if code else ''}"
    # Pass on a 4xx/5xx or no reply, with none of the site's markup. A 2xx or 3xx means workers.dev answers for the site again.
    check("workers.dev does not serve the site", (st is None or st >= 400) and not is_site(body), detail)
else:
    skip(
        "workers.dev does not serve the site",
        "NAT_WORKERS_DEV_URL is unset, so no workers.dev host is requested. The apex check uses the public custom domain.",
    )

if failed:
    print(f"LIVE FAIL: {', '.join(failed)}. If workers.dev is serving, the last deploy turned the subdomain on; see SKILL.md.")
    sys.exit(1)
summary = f"{len(passed)} passed" + (f", {len(skipped)} skipped" if skipped else "")
print(f"LIVE PASS: {summary}")
