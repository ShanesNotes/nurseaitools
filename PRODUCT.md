# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Nurses looking up an AI tool before they trust it on a shift, in school, or on a unit. Confirmed by the live directory and the owner's brief. The owner is a critical care registered nurse. Inferred from the reality-check fields and the About page: the primary job is a bedside or student nurse deciding whether a tool is built for nurses, what its HIPAA posture is, and whether it fits the work in front of them. Nurse leaders and vendors who submit a tool are secondary. That split was not confirmed in an interview.

## Product Purpose

Nurse AI Tools is an independent directory of 57 AI tools nurses actually run into. Each listing carries an RN reality check: who it is built for, its HIPAA status, and whether it fits bedside work. Success is a nurse who can find a tool and read that check without wading through vendor language.

## Positioning

Most clinical AI is built for physicians. This directory says, from public vendor information only, which tools are built for nurses and what is safe to use. A neighboring catalog could not truthfully copy the RN reality check without the same labeled, unverified-means-Unknown rule.

## Operating Context

A nurse searches or filters the directory, opens a tool page, and may subscribe to a weekly note or submit a tool. Confirmed filters: Built for nurses, Mentions HIPAA, and category. The second was labeled HIPAA-ready until Oct 25, 2026; it was renamed because the data only says the vendor site mentions HIPAA. Confirmed categories, from the source list: Ambient documentation, Handoff & summaries, Clinical decision support, Education / NCLEX, Scheduling & staffing, Patient communication, General LLMs for nurses.

## Capabilities and Constraints

Confirmed stack, already in the repo: `python3 build.py` emits `dist/worker.js`. The owner deploys with `wrangler deploy`. Cloudflare Worker name `nurseaitools`, D1 binding `DB`, database name `nurseaitools`. Tables `subscribers` and `submissions` stay as in `schema.sql`. `pages/*.html` and `urls.txt` are the Oct 15 research dump. The build does not read them. `deploy.js` is a second copy of the worker for a connector upload. The build does not write it. Keep `wrangler deploy` as the path the README documents. If `deploy.js` stays in the repo, the build must refresh the embedded worker so the two copies cannot drift.

Endpoints that must keep working: `POST /api/subscribe`, `POST /api/submit`, `GET /sitemap.xml`, `GET /robots.txt`, HTML pages, `www` to apex 301. Canonical origin `https://nurseaitools.com`.

Reality-check values already in the data, not to be invented or renamed: Built for is Nurses, Physicians, Both, General, or Unknown. HIPAA status is Mentions HIPAA, Not for patient info, or Unknown. Bedside fit is Bedside/mobile workflow, Desk or charting only, Education only, or Unknown. The Mentions HIPAA filter (key `hipaa`) matches Mentions HIPAA. The string "BAA offered per vendor" appears in that filter and is never assigned. Built for nurses matches Built for equal to Nurses. Both and General do not count.

The short HIPAA badge and the long HIPAA sentence are different rules. Keep that split. Education tools show the badge "Not for patient info" and the long line "Not publicly stated on vendor homepage; verify with vendor." Only General LLMs get the consumer-PHI sentence. Do not reconcile them.

Remove the hero sentence "Curated by a critical care RN." It is the third line of the home hero, inside `<p class=muted>`, not the h1. The h1 stays "AI tools for nurses, reviewed by a nurse" unless a later direction contract changes the wording without adding claims. Keep the curator fact on the About page, including the about title. Keep every tool fact. Do not invent tool facts. Do not write em dashes in visitor copy.

Search and filter UI states are explicit: idle, filtering, empty results. Newsletter and submit-tool forms are explicit: idle, validating, submitting, success, error. No boolean soup.

## Brand Commitments

Name: Nurse AI Tools. The owner asked for a look that is distinctive, credible, and handcrafted, like a serious clinical reference that also has personality, and said the current site looks like generic AI slop. That character is binding.

The October 2026 dark-only, one-monospace reading is recorded in DECISIONS.md and is no longer the system. The site keeps the Market token structure, type roles, spacing scale, and ink rules in `docs/design/market-source/DESIGN.md`, tuned for long-form nursing text. It is light first, dark when the device asks for it, with Host Grotesk for words, JetBrains Mono for figures, square frames, and no shadow. Contrast, focus states, and the 390px phone layout are required. `DESIGN.md` documents the tuned values and `test_style.py` checks them.

## Evidence on Hand

`tools.py` and `reality.py` are the authored tool facts. `tools.json` is generated. Live site: https://nurseaitools.com. About page states the curator is a registered nurse with 14 years of critical care experience. HIPAA lines are computed from a vendor-homepage check dated Oct 15, 2026, or from the category rule for education and general LLMs. Do not fabricate testimonials, sponsorships, BAAs, or bedside outcomes.

## Product Principles

Say Unknown when a fact was not verified. Keep the directory independent of the vendors it lists. Nothing on the site is medical advice. A nurse on a phone should be able to filter and read a reality check. Personality lives in the reference voice, not in invented claims.
