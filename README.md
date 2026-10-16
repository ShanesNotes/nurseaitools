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

The build prints `57 tools 60 pages <n> bytes`. It writes `dist/worker.js`, `tools.json`, and the worker embedded in `deploy.js`.

Edit tool facts in `tools.py` and the reality check judgments in `reality.py`. Edit markup and CSS in `build.py`. Edit browser behavior in `web/`.

To add a checkbox filter, add a row to `TRAITS` in `build.py`. The browser code needs no change.

## Run the tests

```sh
npm test
```

`node --test` runs `test/*.test.js` against the same `web/*.js` files the browser loads. To type-check the JSDoc types in `web/` and `test/`, run `npm run check`.

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

`deploy.js` is a second deploy path for a connector that uploads one module through the Cloudflare API with no bundler. `build.py` writes the worker into it with `web/contract.js` inlined in place of the import. Run the build before you use it.

## Reference

### Files

- `build.py` reads the tool data, renders the pages and CSS, and fills `worker.template.js`.
- `worker.template.js` routes requests, serves `/js/*` and `/fonts/*`, and holds the only SQL in the project.
- `web/contract.js` owns the endpoint paths, field rules, reply copy, and `decide`, the pure server decision for one POST.
- `web/fsm.js` defines the machine shape and `drive`, the loop that runs a machine.
- `web/catalog.js` is the directory filter machine, with the states `idle`, `filtering`, and `empty`.
- `web/form.js` is the form machine, with the states `idle`, `validating`, `submitting`, `success`, and `error`.
- `web/page.js` is the browser entry and the only module that touches the DOM.
- `fonts/` holds the self-hosted WOFF2 files that the worker serves at `/fonts/`.

`page.js` finds controls by these attributes: `data-catalog`, `data-card`, `data-filter-query`, `data-filter-category`, `data-filter-trait`, `data-filter-clear`, `data-catalog-count`, `data-catalog-empty`, and `data-form-message`. Keep them when you edit the markup in `build.py`.

### Design tokens

The page CSS in `build.py` declares these custom properties on `:root`.

| Property | Value | Use |
| --- | --- | --- |
| `--paper` | `#e7eef2` | Page background |
| `--ink` | `#14202b` | Body text, 14:1 on paper |
| `--field` | `#123655` | Masthead, primary buttons, links, focus ring, text selection |
| `--ivory` | `#f4f1e6` | Wordmark, input wells, focus ring on blue |
| `--copper` | `#8c4a32` | The status plate rule, and nothing else |
| `--amber` | `#7a4e00` | Text for Unknown, Not for patient info, and form errors |
| `--amber-bg` | `#f8edd4` | Plate bay behind amber text |
| `--teal` | `#0c5c4c` | Text for Mentions HIPAA and form success |
| `--teal-bg` | `#e4f3ee` | Plate bay behind teal text |
| `--line` | `#737d85` | Control borders, 3.58:1 on paper |
| `--hair` | `#b9c1c6` | Row hairlines, where text carries the meaning |
| `--muted` | `#535e67` | Secondary text and placeholders, 5.66:1 on paper |
| `--cut` | `10px` | Size of the one chamfered corner on each control |

The fonts are self-hosted. The page loads no font stylesheet from another origin.

| File | Face | Use |
| --- | --- | --- |
| `fonts/syncopate-700.woff2` | Syncopate 700 | Wordmark, page titles, section headings, the index column head, and plate labels at 0.8125rem |
| `fonts/source-sans-3-400.woff2` | Source Sans 3 400 | Body text |
| `fonts/source-sans-3-600.woff2` | Source Sans 3 600 | Tool names in the index, field labels, buttons, plate values |

### Direction

The site is drawn as a 1971 clinical futures manual. It reads as a credible reference a nurse can scan. It is not a neon synthwave template, and the index is not a grid of icon cards.

- The status plate is the signature element. Each tool shows three bays labeled Built for, HIPAA status, and Bedside fit, in the words stored in `reality.py` and the HIPAA rule in `build.py`. Amber marks Unknown and Not for patient info. Teal marks Mentions HIPAA. Nurses is never colored as a grade. Plate labels are Syncopate 700 at 0.8125rem and may wrap to two lines inside the bay.
- Page titles and section headings use Syncopate 700. Tool names in the index stay Source Sans 3 600 so a nurse can scan fifty-seven rows. At desktop the index has a ruled column head, Tool, What it does, and RN reality check. Below 52rem that head is hidden and each row stacks.
- A form error names the field that failed, sets `aria-invalid` and `aria-describedby` on that control, and draws an amber edge. The HTTP reply text from `/api/subscribe` and `/api/submit` is unchanged.
- The copper rule is a 2px line across the top of each plate, and it is the only motion on the site. It is visible by default. When the directory enters the `filtering` state, the rule on each visible plate draws once from the left in 180ms ease-out.
- Under `prefers-reduced-motion: reduce`, the rule does not animate.
- The masthead is full-bleed field blue with a 1px diagonal security tint. The wordmark is the largest type on the page. No other surface has texture. There is no glow, glass, or gradient text.
- Controls are ordinary inputs and buttons with one chamfered corner. The chamfer comes from `clip-path`, which would clip an outline, so the 2px focus ring is drawn inside the control.
