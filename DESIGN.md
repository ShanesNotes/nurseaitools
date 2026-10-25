# Design

Nurse AI Tools keeps the Market token structure and Ink Rule from `docs/design/market-source/DESIGN.md` (market@64b7d286). That file is the source of truth. This page records only what the nursing site changes, and why. The type scale and spacing follow `docs/design/north-star.md`.

The page is light first, on warm paper. A dark theme follows `prefers-color-scheme`. Near-black on paper, or white on dark, is what the directory could verify. Pencil is what it could not, with the word Unknown beside it. There is one accent, spruce, and everything else is a warm neutral. Frames are square and 1px, and sections are marked by corner brackets rather than boxes. There is no shadow, gradient, or blur.

`python3 test_style.py` checks the shipped CSS against the values below.

## What stayed

From Market: the token structure, the ground names (`ground`, `panel`, `raised`, `hover`, `bar`), the ink names (`text`, `soft`, `pencil`), the Ink Rule, square corners, 1px rules, and no shadow, gradient, or blur.

## Color: one accent (2026-10-25)

Shane asked the site to step away from the blue, green, yellow, and red highlights. Market's gold labels, blue links, green HIPAA edge, and red harm edge are gone, along with the unpainted quality, coin, and pace tokens. The palette is now warm neutrals plus one accent.

| Token | Light | Dark | Job |
| --- | --- | --- | --- |
| `ground`, `panel`, `raised`, `hover`, `bar` | `#f6f1e8`, `#efe8db`, `#fffaf3`, `#e9e1d2`, `#dfd3bc` | `#1c1611`, `#211a14`, `#221f18`, `#2c281f`, `#2a2318` | Paper, the empty state, fields, row hover, the checked filter. |
| `rule`, `edge` | `#8a7d68`, `#6b5e4a` | `#7d7262`, `#7d7262` | Row hairlines and control frames, at least 3:1. |
| `text` | `#1c1611` | `#ffffff` | Everything the directory verified, and every heading. |
| `soft` | `#5c5348` | `#a49d89` | Labels, kickers, column heads, secondary lines. |
| `pencil` | `#5e584e` | `#9a9a9a` | Unknown, always with the word beside it. |
| `accent` | `#1f5550` | `#7dbab0` | Spruce. Links, the focus ring, the checked filter, the RN reality check column rule, guide numbers, hero action hover. Nothing else. |
| `menu`, `menuText`, `bandSoft` | `#1c1611`, `#ece5d3`, `#b9b09c` | `#0b0a08`, `#ece5d3`, `#b9b09c` | The newsletter band and the skip link. |

Spruce was picked from three options shot on home and a tool page in both themes: spruce, aubergine (`#5a3a5c`), and slate (`#3d4a52`). Slate sat too close to the ink to mark a link. Aubergine read as decorative. Spruce reads as clinical without being bright. The accent clears 5.7:1 on every light ground and 6.6:1 on every dark one.

`test_style.py` fails if any token other than `accent` has a hue, meaning a channel spread over 40.

## Type and space, after the north star (2026-10-24)

The October pass kept Market's 12 to 18px range, so the h1 was 18px and the page had no hierarchy. `docs/design/north-star.md` records why that changed. The scale now has big steps, like the reference page, and every size is a token that `test_style.py` pins.

| Token | Size | Face | Job |
| --- | --- | --- | --- |
| `display` | `clamp(44px,7.4vw,112px)` | Host Grotesk 500 | The home h1 only. Line height 0.92, tracking -0.035em. |
| `headline` | `clamp(36px,4.6vw,64px)` | Host Grotesk 500 | Inner page h1s and section heads. |
| `proof` | `clamp(36px,5vw,72px)` | JetBrains Mono | The four counts on home. |
| `title` | 28px | Host Grotesk 500 | Prose h2s, the hero actions, the newsletter head, reality-check values on a tool page. |
| `lead` | `clamp(20px,1.8vw,24px)` | Host Grotesk | Ledes, the search field, guide links, the wordmark. |
| `body` | 18px | Host Grotesk | Rows, prose, fields, buttons. |
| `figure`, `small` | 15px | Mono, Host Grotesk | Row values and counts; filters, nav, footnotes. |
| `micro` | 12px | JetBrains Mono, 0.02em tracking, mixed case | Labels, column heads, kickers, vendor lines. Nothing smaller ships. |

Spacing keeps 2, 4, 8, 12, and 16px and adds 24, 32, 48, 64, and 96px. `--section` is 96px between sections, 64px at 720px and below. The column is 1240px with 24px gutters.

Headings are `text`, so the largest words carry the most ink. Labels are `soft`.

## What changed

| Token | Old | New | Why |
| --- | --- | --- | --- |
| `micro` size | 11px | 12px | Nothing on the site is under 12px. |
| `button` size | 11px | 18px | The control is 44px tall and sits beside 18px field text. |
| `body` size | 13px | 18px | A row is a sentence a nurse reads, not an auction cell. |
| Display, title, lead, figure | 18, 14, 18, 15px | See the type table | The north-star scale. `trackerHead` and `trackerLine` are gone, since nothing here draws a tracker. |
| Display, title, button, and tracker faces | Friz Quadrata | Host Grotesk | The client face cannot be shipped. |
| Body, lead, small, and micro faces | Arial Narrow | Host Grotesk | There is no Arial Narrow file, and a condensed face fights long paragraphs. |
| Figure face | Arial Narrow | JetBrains Mono | Figures keep a second face. This is the licensed one already on the worker. |
| Control reach | 24px | 44px | Nurse tap target. The row is the hit target for its name. |
| Focus ring | 1px `accent` | 2px `accent` | A 1px ring is easy to miss. |

## Ink on the page

Home opens with a mono kicker, the h1, the brand line, and two hero actions set as large underlined words. Under them, four counts inside corner marks: built for nurses, mentions HIPAA, bedside fit, and no HIPAA statement. The build computes them from `tools.json`. The last count is pencil with a dashed rule, because it counts what the directory could not verify. The counts stay smaller than the h1 at every width. Then the directory, with a 56px search field and a flowsheet-style column head.

Values in rows are mono and do not wrap. A tool page keeps its lede, reality check, and spec table to one 860px column. Unknown is pencil with a dashed underline. "Not for patient info" has a solid 2px ink underline, the one caution mark. "Mentions HIPAA" is plain ink, like any other stated fact. Shape and the words carry the meaning, not hue. The "One rule before any of these" note keeps a 2px ink rule on its left. On a tool page the same three values are 28px, each under a mono label with a left rule, inside corner marks.

The newsletter is a full-width band on `menu` with `menuText` ink and `bandSoft` (#b9b09c, 8.8:1 on light `menu`) for its secondary text. It is the only inverted section. Inside it the focus ring switches to `menuText`. The empty directory state sits on `panel`.

Hover and focus changes fade over 0.15s. Under `prefers-reduced-motion: reduce` there are no transitions.

At 960px and below, the column head hides and each row stacks. At 560px and below, the reality-check values become label and value lines, the hero actions stack, and the category filter stacks. The page does not scroll sideways at 390px.

Every page opens with a skip link to `main`. Links in the mast, the hero actions, the guides, the tool spec, buttons, fields, and the filter toggles are at least 44px tall.

## Copy

No emoji. The brand line on home is "AI should run the rules in the background so nurses can run the care." The words unlock, elevate, seamless, powerful, robust, next-gen, journey, dashboard, empower, effortless, cutting-edge, game-changer, transform, and the phrase "curated by" stay out of shipped pages, scripts, and CSS. So do em dashes and curly quotes.
