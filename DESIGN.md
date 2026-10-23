# Design

Nurse AI Tools keeps the Market token structure, type roles, spacing scale, and ink rules from `docs/design/market-source/DESIGN.md` (market@64b7d286). That file is the source of truth. This page records only what the nursing site changes, and why.

The page is light first, on warm paper. A dark theme follows `prefers-color-scheme` and uses the spec's dark inks except the two edges named below. White, or near-black on paper, is what the directory could verify. Pencil is what it could not, with the word Unknown beside it. Gold is for titles, navigation, and column heads. Red is only the harm edge. Green is only the "Mentions HIPAA" edge. Blue is the link color and the reality-check edge. Frames are square and 1px. There is no shadow, gradient, or blur.

`python3 test_style.py` checks the shipped CSS against the values below.

## What stayed

Color names, including `ground`, `panel`, `raised`, `hover`, `text`, `soft`, `pencil`, `heading`, `up`, `down`, and `buy`. The spacing scale is 2, 4, 8, 12, and 16px. Type roles stay `display`, `title`, `body`, `figure`, `lead`, `small`, `micro`, `button`, `trackerHead`, and `trackerLine`. Display, title, and lead stay 18, 14, and 18px. Figure stays 15px. Small stays 12px. Dark `text`, `heading`, `pencil`, `soft`, `up`, `down`, and `buy` keep the spec hexes. Quality, coin, pace, and skill tokens keep the spec hexes and are not painted.

## What changed

| Token | Old | New | Why |
| --- | --- | --- | --- |
| `micro` size | 11px | 12px | Nothing on the site is under 12px. |
| `button` size | 11px | 18px | The control is 44px tall and sits beside 18px field text. |
| `trackerLine` size | 10px | 12px | Same floor. This role is not drawn here. |
| `body` size | 13px | 18px | A row is a sentence a nurse reads, not an auction cell. |
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

Home opens with the title, the brand line, three doors, then the directory. The title and the wordmark are `heading`. The brand line and the rows are `text` at `body`. Unknown is a dashed `pencil` edge. "Not for patient info" is a solid `down` edge. "Mentions HIPAA" is a solid `up` edge. The words still say which is which.

At 960px and below, the column head hides and each row stacks. At 560px and below, the reality-check values become label and value lines, and the category filter stacks. The page does not scroll sideways at 390px.

Every page opens with a skip link to `main`. Links in the mast, the doors, the guides, the tool spec, buttons, fields, and the filter toggles are at least 44px tall.

## Copy

No emoji. The brand line on home is "AI should run the rules in the background so nurses can run the care." The words unlock, elevate, seamless, powerful, robust, next-gen, journey, dashboard, empower, effortless, cutting-edge, game-changer, transform, and the phrase "curated by" stay out of shipped pages, scripts, and CSS. So do em dashes and curly quotes.
