# ADR-0001: Forum router and session helpers inside the one Worker

**Status:** Accepted (F1)
**Date:** 2026-10-24
**Deciders:** Shane

## Context

The forum (`/discuss`, plan section 4) needs request-time HTML, a D1-backed session, and POST endpoints. The site is one Worker. `dist/worker.js` is what `wrangler dev` and `wrangler deploy` read, and wrangler bundles its imports. `deploy.js` is the connector upload: one module, no bundler, so build.py has to paste every server module into it. Every file in `web/` is served to browsers at `/js/*` and modulepreloaded on every page, so server-only code cannot live there.

## Decision

- Server code lives in `server/forum.js`. It imports nothing. `worker.template.js` imports it, and build.py inlines every relative import from the template into `deploy.js`, with `export` removed. Build asserts fail if an inlined module has its own `import`, or if two inlined modules declare the same top-level name.
- The template sends `/discuss*`, `/login`, `/auth/*`, `/api/auth/*`, `/api/forum/*`, `/api/account/*`, and `/u/*` to `forum()` before any other route. The new paths do not overlap the existing routes.
- `forum()` checks in a fixed order: method, then same-origin `Origin` on every POST (403), then a valid session on member POSTs (401), then the handler. Routes from later units return 404 until they are built.
- Pages: build.py renders `page()` once with `%%TITLE%%`, `%%DESC%%`, `%%BODY%%`, and `%%PATH%%` placeholders and ships it as `SHELL`. The worker fills them in with escaped values. The forum gets the same markup, CSS, and nav as the baked pages, with no second template.
- Sessions follow the Lucia guide. The cookie holds 32 random bytes in base64url. D1 stores only the SHA-256 hex of that value (`sessions.id_hash`). Cookie: `__Host-sid`, `HttpOnly; Secure; SameSite=Lax; Path=/`, 30-day Max-Age. Sessions slide: when fewer than 15 days remain, `expires_at` moves to now + 30 days and the cookie is set again. Expired sessions and sessions of deleted users are removed when read.
- Schema: `migrations/0002_forum.sql`, copied from plan 4.4. `schema.sql` (subscribers, submissions) is left alone. No report, mod, role, ban, or hold tables or columns. A test enforces this.
- Integration tests: `node --test` drives the inlined `deploy.js` worker in Miniflare (pinned to the version wrangler 3 already ships), with an in-memory D1 and the migration applied. That tests the exact artifact the connector deploys. `wrangler dev --local` plus `wrangler d1 migrations apply --local` is covered by the verify skill.

## Options considered

| Option | Complexity | Fits deploy.js | Notes |
| --- | --- | --- | --- |
| A. One import-free `server/forum.js`, inlined (chosen) | Low | Yes | Same pattern as `web/contract.js`. One file for now. |
| B. Several server modules that import each other, with a build-time resolver | Medium | Yes, with work | Build order and name-collision handling, which F1 does not need. Revisit at F2 or F3 if forum.js gets long. |
| C. Add a bundler (esbuild) for deploy.js | Medium | Yes | Adds a build dependency and changes the deploy artifact Shane already trusts. |
| D. Put the forum in `web/` | Low | Yes | Ships server code to every browser and preloads it on every page. Rejected. |

Testing: `@cloudflare/vitest-pool-workers` needs vitest and wrangler 3.x pool pinning, which means a second test runner. Miniflare under `node --test` reuses the runner and the dependency tree the repo already has.

## Consequences

- Easier: F2 to F4 add handlers inside `forum()` behind the same Origin and session gates, and `deploy.js` keeps working with no change to the deploy step.
- Harder: everything inlined shares one scope, so names must stay unique. The build asserts it.
- Revisit: split `server/forum.js` (option B) once auth and threads make it long. When D1 deploy prep runs, apply `0002_forum.sql` to the remote database. That is a human step.
