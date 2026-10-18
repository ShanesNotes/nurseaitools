# Design

Nurse AI Tools uses the marketforever.dev system. The page is dark and flat and set in one monospace face. It reads as a clinical reference sheet. A nurse scans the index, filters it, opens a tool, and reads the RN reality check.

The tokens are on `:root` in the CSS string in `build.py`. No color, size, or space is written outside `:root`. `python3 test_style.py` builds the site and checks every rule below against the shipped CSS and pages.

## Color

| Token | Hex | Use |
| --- | --- | --- |
| `--color-bg` | `#0a0c10` | Page |
| `--color-surface` | `#11141a` | Index sheet, reality-check panel, newsletter panel, buttons |
| `--color-thead` | `#141821` | Index column head |
| `--color-hover` | `#1d222c` | Hovered or focused index row |
| `--color-text` | `#e7e9ee` | Body text, 13.12:1 on the hover row |
| `--color-muted` | `#8b93a1` | Secondary text, labels, the dashed caution edge, 5.15:1 on hover |
| `--color-faint` | `#868d99` | Placeholders, 4.77:1 on hover |
| `--color-line` | `#3a4250` | Row rules |
| `--color-line-strong` | `#5c6578` | Inputs, pane edges, the header and footer rules |
| `--color-mark` | `#e6c87e` | The focus ring |
| `--color-accent` / `--color-accent-text` | `#e7e9ee` / `#0a0c10` | The filled button and the skip link |

Every text color clears 4.7:1 on the page, the panel, the table head, and the hover row. Selected text is page color on text color.

Four accents are edges only. Each has one job.

- `--accent-blue` `#4aa3ff` marks the RN reality check. It is the rule under the column-head group on the index and the left edge of the panel on a tool page.
- `--accent-green` `#3fae5c` is the solid edge around "Mentions HIPAA".
- `--accent-red` `#e87878` is the left edge of the PHI rule on student pages and the border of an invalid field.
- `--accent-yellow` `#e6c87e` appears only in the stripe.

All four sit in the 4px stripe at the top of every page. No accent is used as text or as a fill.

A reality-check value is plain when it is a fact (Nurses, Education only). Unknown and Not for patient info get a dashed edge. Mentions HIPAA gets a solid green edge. The words carry the meaning, the edge style carries it a second time, and the hue a third.

## Type

One family, `ui-monospace, "Cascadia Mono", "Segoe UI Mono", Menlo, Consolas, monospace`. No webfont. Ligatures are off and numbers are tabular with a slashed zero.

Six sizes. 12px for column heads and reality-check labels. 13px for row meta, index values, notes, and the footer. 14px for descriptions, nav, labels, and buttons. 16px for body copy, fields, tool names, and tool-page values. 20px for the wordmark and section heads. 24px for page titles.

## Space and shape

Spacing is 4, 8, 12, 16, 24, and 32px (`--space-2` to `--space-7`). The gutter is 16px. Corners are 0 or 2px. Edges are 1px, and the focus ring and accent edges are 2px. There is no shadow, gradient, blur, or animation.

## Layout

The index is one sheet with five columns at desktop: tool, what it does, built for, HIPAA status, and bedside fit. The last three sit under an "RN reality check" group head. The head sticks while the list scrolls. At 960px and below the head hides and each row stacks, with the three reality-check values in a labeled row. At 560px and below those values become label and value lines. The page never scrolls sideways at 390px.

## Keyboard and touch

Every page opens with a skip link to `main`. Every link, field, select, checkbox, and button shows the same 2px gold ring, and no rule restyles it. Controls are at least 44px tall. A filter toggle is a labeled native checkbox. When checked, its border turns text color.

## Copy

No emoji. No hero, feature cards, or counts beyond the tool count the build computes. The words unlock, elevate, seamless, powerful, robust, next-gen, journey, dashboard, empower, effortless, cutting-edge, game-changer, transform, and the phrase "curated by" stay out of shipped pages, scripts, and CSS. So do em dashes and curly quotes.
