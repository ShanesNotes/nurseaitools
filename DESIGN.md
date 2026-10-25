# Design

Nurse AI Tools keeps the Market token structure, color names, and ink rules from `docs/design/market-source/DESIGN.md` (market@64b7d286). That file is the source of truth. This page records only what the nursing site changes, and why. The type scale and spacing follow `docs/design/north-star.md`.

The page is light first, on warm paper. A dark theme follows `prefers-color-scheme` and uses the spec's dark inks except the two edges named below. White, or near-black on paper, is what the directory could verify. Pencil is what it could not, with the word Unknown beside it. Gold is for labels, kickers, and column heads. Red is only the harm edge. Green is only the "Mentions HIPAA" edge. Blue is the link color. Frames are square and 1px, and sections are marked by corner brackets rather than boxes. There is no shadow, gradient, or blur.

`python3 test_style.py` checks the shipped CSS against the values below.

## What stayed

Color names, including `ground`, `panel`, `raised`, `hover`, `text`, `soft`, `pencil`, `heading`, `up`, `down`, and `buy`, and every color hex in the table below. Dark `text`, `heading`, `pencil`, `soft`, `up`, `down`, and `buy` keep the spec hexes. Quality, coin, pace, and skill tokens keep the spec hexes and are not painted. The Ink Rule, square corners, 1px rules, and no shadow, gradient, or blur.

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

Gold (`heading`) moved off headings and onto labels and column heads, where Market puts it anyway. Headings are `text`, so the largest words carry the most ink.

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
| Dark `edge` and `rule` | `#4a4234`, `#332d23` | `#7d7262` | The spec edge is about 1.5:1 on the ground. With no client frame art, the sheet would disappear. |
| Light `ground` | `#1c1611` | `#f6f1e8` | Warm paper for long text. The spec has one dark look. |
| Light `panel` | `#211a14` | `#efe8db` | The mast, one step off the paper. |
| Light `raised` | `#221f18` | `#fffaf3` | Sheets, fields, and doors. |
| Light `hover` | `#2c281f` | `#e9e1d2` | The hover sits under the words. |
| Light `rule` | `#332d23` | `#8a7d68` | Row hairline, still 3:1 on paper. |
| Light `text` | `#ffffff` | `#1c1611` | Seen ink. The dark ground hex moves to the text. |
| Light `soft` | `#a49d89` | `#5c5348` | Secondary text clears 4.5:1 on paper. |
| Light `pencil` | `#9a9a9a` | `#5e584e` | Unknown ink clears 4.5:1. Dark pencil already does, and stays. |
| Light `heading`, `muted`, `button` | `#ffd100` | `#6e4e0c` | Pigment gold is about 2:1 on paper. |
| Light `accent`, `line`, `trim` | `#e2b55c`, `#c9a24a` | `#6e4e0c` | The focus ring has to clear 4.5:1. |
| Light `up`, `fresh`, `complete` | `#72c48e`, `#28ff28` | `#1f6b3a` | Green text and the HIPAA edge. |
| Light `down` | `#e4705f` | `#8d2c1e` | The harm edge. |
| Light `buy` | `#6a95d8` | `#1e3f86` | Links and the reality-check edge. |
| Light `frame` | `#1a1712` | `#e7dfd0` | Unused as a costume. Kept so the name still exists. |
| Light `edge`, `menuEdge` | `#4a4234`, `#8e8671` | `#6b5e4a` | The 1px frame. |
| Light `bar`, `tab` | `#2a2318`, `#1c1912` | `#dfd3bc`, `#efe8db` | Column heads and the reality-check head. |
| Light `menu` | `#0b0a08` | `#1c1611` | Filled button and skip link. `menuText` stays `#ece5d3`. |
| Light `objective` | `#eeeeee` | `#1c1611` | Not painted. Kept off neon on paper. |

## Ink on the page

Home opens with a mono kicker, the h1, the brand line, and two hero actions set as large underlined words. Under them, four counts inside corner marks: built for nurses, mentions HIPAA, bedside fit, and no HIPAA statement. The build computes them from `tools.json`. The last count is pencil with a dashed rule, because it counts what the directory could not verify. The counts stay smaller than the h1 at every width. Then the directory, with a 56px search field and a flowsheet-style column head.

Values in rows are mono and do not wrap. A tool page keeps its lede, reality check, and spec table to one 860px column. Unknown is pencil with a dashed underline. "Not for patient info" has a solid `down` underline. "Mentions HIPAA" has a solid `up` underline. The words still say which is which. On a tool page the same three values are 28px, each under a mono label with a left rule, inside corner marks.

The newsletter is a full-width band on `menu` with `menuText` ink and `bandSoft` (#b9b09c, 8.8:1 on light `menu`) for its secondary text. It is the only inverted section. Inside it the focus ring switches to `menuText`. The empty directory state sits on `panel`.

Hover and focus changes fade over 0.15s. Under `prefers-reduced-motion: reduce` there are no transitions.

At 960px and below, the column head hides and each row stacks. At 560px and below, the reality-check values become label and value lines, the hero actions stack, and the category filter stacks. The page does not scroll sideways at 390px.

Every page opens with a skip link to `main`. Links in the mast, the hero actions, the guides, the tool spec, buttons, fields, and the filter toggles are at least 44px tall.

## Copy

No emoji. The brand line on home is "AI should run the rules in the background so nurses can run the care." The words unlock, elevate, seamless, powerful, robust, next-gen, journey, dashboard, empower, effortless, cutting-edge, game-changer, transform, and the phrase "curated by" stay out of shipped pages, scripts, and CSS. So do em dashes and curly quotes.
