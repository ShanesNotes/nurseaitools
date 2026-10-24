# Nurse AI Tools

Nurse AI Tools is a directory of AI tools for nurses, served at https://nurseaitools.com. `build.py` renders every page into one Cloudflare Worker, `dist/worker.js`.

## Set up

Install Node 22 and Python 3. Then install the dev dependencies:

```sh
npm install
```

## Build the site

```sh
python3 build.py
```

The build prints `78 tools 85 pages <n> bytes`. It writes `dist/worker.js`, `tools.json`, and the worker embedded in `deploy.js`.

Edit tool facts in `tools.py` and the reality check judgments in `reality.py`. Edit markup and CSS in `build.py`. Edit browser behavior in `web/`.

To add a checkbox filter, add a row to `TRAITS` in `build.py`. The browser code needs no change.

## Run the tests

```sh
npm test
```

`node --test` runs `test/*.test.js` against the same `web/*.js` files the browser loads. To type-check the JSDoc types in `web/` and `test/`, run `npm run check`.

To prove a change end to end on this machine, run the verification skill. It builds, runs both suites, serves the worker with `wrangler dev --local` and a fresh local D1, drives the site in Chrome, and prints `VERIFY PASS` or `VERIFY FAIL`:

```sh
/workspace/.pwvenv/bin/python .agents/skills/verify-nurse-ai-tools/verify.py
```

See `.agents/skills/verify-nurse-ai-tools/SKILL.md`.

## Run the site locally

`wrangler dev` serves `dist/worker.js` as it is on disk. It does not run the build, so build first:

```sh
python3 build.py
npx wrangler dev
```

Open http://localhost:8787. After each edit, run `python3 build.py` again. `wrangler dev` reloads when `dist/worker.js` changes. Pages are served with a five-minute cache, so hard-reload the browser.

The forms write to a local D1 database. To create its tables, run this once:

```sh
npx wrangler d1 execute nurseaitools --local --file schema.sql
```

## Deploy

```sh
python3 build.py
npx wrangler deploy
```

`wrangler.toml` deploys the worker `nurseaitools` with the D1 binding `DB` on the database `nurseaitools`. The worker imports `web/contract.js`, and wrangler bundles that import. Do not set `no_bundle = true`, because the import then fails.

Apply `schema.sql` once on the remote database if the tables are not already there:

```sh
npx wrangler d1 execute nurseaitools --remote --file schema.sql
```

A subscribe still inserts into D1. When the secret `KIT_API_KEY` is set, the worker then posts the address to Kit after that insert. `KIT_TAG_ID` is optional. Leave both unset and Kit is skipped.

```sh
npx wrangler secret put KIT_API_KEY
npx wrangler secret put KIT_TAG_ID
```

`deploy.js` is a second deploy path for a connector that uploads one module through the Cloudflare API with no bundler. `build.py` writes the worker into it with `web/contract.js` inlined in place of the import. Run the build before you use it.

## Reference

### Files

- `build.py` reads the tool data, renders the pages and CSS, and fills `worker.template.js`.
- `worker.template.js` routes requests, serves `/js/*`, and holds the only SQL in the project.
- `web/contract.js` owns the endpoint paths, field rules, reply copy, and `decide`, the pure server decision for one POST.
- `web/fsm.js` defines the machine shape and `drive`, the loop that runs a machine.
- `web/catalog.js` is the directory filter machine, with the states `idle`, `filtering`, and `empty`.
- `web/form.js` is the form machine, with the states `idle`, `validating`, `submitting`, `success`, and `error`.
- `web/page.js` is the browser entry and the only module that touches the DOM.
- `test_style.py` builds the site and checks the shipped CSS and pages against the design rules in `DESIGN.md`.

`page.js` finds controls by these attributes: `data-catalog`, `data-card`, `data-filter-query`, `data-filter-category`, `data-filter-trait`, `data-filter-clear`, `data-catalog-count`, `data-catalog-empty`, and `data-form-message`. Keep them when you edit the markup in `build.py`.

### Design

The look is documented in `DESIGN.md`. The tokens live on `:root` in the CSS string in `build.py`. The worker serves Host Grotesk and JetBrains Mono from `fonts/` at `/fonts/*`, with their OFL licenses. To check the look after an edit, run:

```sh
python3 test_style.py
```
