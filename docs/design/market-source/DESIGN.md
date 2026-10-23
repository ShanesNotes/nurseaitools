---
name: Market
description: The classic World of Warcraft client's dark frame, written in white ink for what Market saw and grey pencil for what it did not.
# Normative tokens. Colours mirror the one look in MATERIALS in addon/market/UI.lua exactly
# (ADR 0085), keyed by token. Checked both ways by
# .scratch/ui-overhaul/evidence/check_design_tokens.py <repo root>. heading, muted, button,
# text, up, down, orange, yellow and green are the client's own colours read at load (U.NATIVE,
# R15); the hex here is their fallback (ADR 0085, 2026-10-17).
colors:
  ground: "#1c1611"
  panel: "#211a14"
  raised: "#221f18"
  hover: "#2c281f"
  rule: "#332d23"
  text: "#ffffff"
  soft: "#a49d89"
  muted: "#ffd100"
  pencil: "#9a9a9a"
  accent: "#e2b55c"
  line: "#e2b55c"
  up: "#72c48e"
  down: "#e4705f"
  fresh: "#72c48e"
  buy: "#6a95d8"
  sale: "#c9925a"
  gold: "#ffd700"
  silver: "#c7c7cf"
  copper: "#eda55f"
  frame: "#1a1712"
  edge: "#4a4234"
  bar: "#2a2318"
  heading: "#ffd100"
  trim: "#c9a24a"
  trimDark: "#6b5220"
  tab: "#1c1912"
  button: "#ffd100"
  skill: "#2f237c"
  menu: "#0b0a08"
  menuEdge: "#8e8671"
  menuText: "#ece5d3"
  objective: "#eeeeee"
  complete: "#28ff28"
  orange: "#ff8040"
  yellow: "#ffff00"
  green: "#40bf40"
  gray: "#808080"
  q0: "#9d9d9d"
  q1: "#ffffff"
  q2: "#1eff00"
  q3: "#0070dd"
  q4: "#a335ee"
  q5: "#ff8000"
  q6: "#e6cc80"
  q7: "#00ccff"
  pace1: "#28ff28"
  pace2: "#40bf40"
  pace3: "#ffff00"
  pace4: "#ff6a50"
  pace5: "#e8655c"
typography:
  # TYPE in UI.lua. Faces are client files: Friz Quadrata = Fonts\FRIZQT__.TTF,
  # Arial Narrow = Fonts\ARIALN.TTF. A face the client lacks falls back to Friz Quadrata.
  # Sizes are pixels at UI scale 1.
  display:
    fontFamily: "Friz Quadrata"
    fontSize: "18px"
  title:
    fontFamily: "Friz Quadrata"
    fontSize: "14px"
  body:
    fontFamily: "Arial Narrow"
    fontSize: "13px"
  figure:
    fontFamily: "Arial Narrow"
    fontSize: "15px"
  lead:
    fontFamily: "Arial Narrow"
    fontSize: "18px"
  small:
    fontFamily: "Arial Narrow"
    fontSize: "12px"
  micro:
    fontFamily: "Arial Narrow"
    fontSize: "11px"
  button:
    fontFamily: "Friz Quadrata"
    fontSize: "11px"
  trackerHead:
    fontFamily: "Friz Quadrata"
    fontSize: "12px"
  trackerLine:
    fontFamily: "Friz Quadrata"
    fontSize: "10px"
spacing:
  # U.STYLE.space
  xs: "2px"
  s: "4px"
  m: "8px"
  l: "12px"
  xl: "16px"
components:
  # U.control kinds, U.tab, U.header and U.panel kinds in the one look (ADR 0085). Rules, alphas,
  # blends and reach are in the prose and in .impeccable/design.json.
  frame:
    backgroundColor: "{colors.frame}"
  frame-title:
    backgroundColor: "{colors.bar}"
    textColor: "{colors.heading}"
    height: "19px"
  tab:
    backgroundColor: "{colors.tab}"
    textColor: "{colors.heading}"
    typography: "{typography.title}"
    height: "28px"
  tab-selected:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
  section-header:
    backgroundColor: "{colors.bar}"
    textColor: "{colors.heading}"
    typography: "{typography.title}"
  inset:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.text}"
  control-tab:
    textColor: "{colors.soft}"
    typography: "{typography.title}"
    height: "24px"
  control-tab-selected:
    textColor: "{colors.text}"
  control-section:
    textColor: "{colors.muted}"
    typography: "{typography.title}"
    height: "24px"
  control-section-selected:
    textColor: "{colors.text}"
  control-segment:
    textColor: "{colors.soft}"
    typography: "{typography.body}"
    height: "24px"
  control-segment-selected:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
  control-segment-group:
    # U.group: ranges, periods, the guide scope. Cells 24x24 at least, side by side on one raised
    # fill in the rule, sharing their rules; the chosen cell on the hover fill.
    backgroundColor: "{colors.raised}"
    textColor: "{colors.soft}"
    typography: "{typography.body}"
    height: "24px"
    width: "24px"
  control-action:
    textColor: "{colors.button}"
    typography: "{typography.button}"
    height: "24px"
    padding: "0 8px"
  control-action-fallback:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
  control-dropdown:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.text}"
    typography: "{typography.body}"
    height: "24px"
  control-item:
    backgroundColor: "{colors.menu}"
    textColor: "{colors.menuText}"
    typography: "{typography.body}"
    height: "24px"
  control-item-selected:
    textColor: "{colors.heading}"
  control-disabled:
    textColor: "{colors.pencil}"
  panel-region:
    backgroundColor: "{colors.panel}"
  panel-sheet:
    backgroundColor: "{colors.raised}"
  panel-menu:
    backgroundColor: "{colors.menu}"
    textColor: "{colors.menuText}"
  row:
    height: "20px"
  row-hover:
    # Added (ADD) beneath the words, never blended over a label.
    backgroundColor: "{colors.hover}"
  row-selected:
    # The client list's gold glow line along the row's foot.
    borderColor: "{colors.heading}"
---

# Design System: Market

Records the system as built for ADR 0085 (one look: the client's dark frame), on the overhaul's
type sizes, contrast floors, 24-unit targets, segment groups and slots (ADR 0079).
Sources: `addon/market/UI.lua` (`MATERIALS`, `TYPE`, `CHART`, `U.STYLE`, the primitives),
`addon/market/Layout.lua`, ADRs 0037, 0068, 0074, 0078, 0079 and 0085, and
`tools/terminal-dev/static/style.css` (the browser preview, which paints the same tokens).
Where this file and the code differ, the code wins; rerun the token check.

## Overview

**Creative North Star: "A page of the classic client"**

Market's window is the profession window's own frame: its stone and metal border over the rock,
a centred gold title in the band, two dark insets, the recipe list's header bars, red buttons, bottom tabs, and
white words for what Market saw beside grey words, with their reason, for what it did not. Beside
the Tailoring frame (the live reference, R13) it reads as the same craftsman's work; Market's
identity is the Ink Rule, not a costume. One look (`MATERIALS.dark`); views pass token and kind
names, never colours. Density is a two-page spread per view at 13 px body type. Everything is
drawn with client widgets, client fonts and guarded client art; no art file or font ships.

**Key Characteristics:**
- The profession window's frame (R15): its metal border and title band, close button and bottom tabs; two insets with a gap. The dark dialog is the fallback.
- White for what Market saw, grey with its reason for what it did not, † for AHledger; red only for losses.
- Client fonts only: Friz Quadrata headings and labels, Arial Narrow figures and cells.
- Classic controls: `UIPanelButtonTemplate` actions, `PanelTabButtonTemplate` tabs, the classic dark dropdown list, the classic scroll bar, the size grabber.
- No shadows, no gradients, no radius; depth is the client's own art.
- Hover lies beneath the words; every control answers clicks across at least 24 units (gamepad cursor).

## Colors

Warm near-black grounds, the client's white and gold inks. Hex values live only in the
frontmatter (normative) and `MATERIALS`.

### Primary
- **Seen** (`text`, the client's `GameFontHighlight` white): every observed value and selected control.
- **Insets** (`ground`, `panel`): an inset's dark fill and a region's box inside it. `raised` is the sheet slip and the selected tab, `hover` the flat hover added beneath a row's words.

### Secondary
- **Pencil** (`pencil`): the only grey: carries, unknowns, estimates, leaders. Never a label, always beside a reason word.
- **Gold** (`heading`, `muted`, the client's `GameFontNormal` gold): titles, section headers, labels and column heads. `soft` is the secondary warm grey (basis notes, idle segments).
- **Loss** (`down`): losses only. `up` and `fresh` the classic green; `accent` a selected toolbar tab, a selected personal chart marker and the minimap badge.

### Tertiary
- **Frame** (`frame`, `bar`, `edge`, `trim`, `trimDark`, `tab`): the dialog's flat fill under its art, the title bar and section-header bars, the insets' 1 px border, Market's gold edge where the client's border is missing, the title rule and header edge, and Market's own tab where the client's is missing.
- **Coin inks** (`gold`, `silver`, `copper`) and **quality inks** (`q0`-`q7`, the client's own values; names take `ITEM_QUALITY_COLORS`).
- **Zones** (`buy`, `sale`): the player's own plan bands on the chart.
- **Pace** (`pace1`-`pace5`): the item tooltip's pace mark and Shift's "Sells:" words, clears very fast to barely moves; each reads 4.5:1 on every ground and the tooltip's (ADR 0180).

### Neutral
- **Classic satellites** (`menu`, `menuEdge`, `menuText`, `button`): the classic dark list, the world frames' fill and the red button's gold label.
- **Rules** (`rule`): hairlines inside a view.

### Named Rules
**The Ink Rule.** White is what Market saw; grey is what it did not, with its reason (ADR 0047 LM4, LM12; R13). The text model and the chart display list name each value's ink; no painter guesses. Every ink reads at least 4.5:1 on `ground`, `panel`, `raised` and `hover` (flat, and added at 0.3 where rows and controls stand), pencil at least 3:1 on the ground; the chart's carries and the "Last seen" rule read 3:1 after their alpha (part `materials-contrast`). A pencil figure always has a reason word beside it. Red is only for a loss.

The client's own colours (`U.NATIVE`: `NORMAL_FONT_COLOR` for `heading`, `muted` and `button`, `HIGHLIGHT_FONT_COLOR` for `text`, `GREEN_FONT_COLOR` for `up`, `RED_FONT_COLOR` for `down`, the `DIFFICULT_`, `FAIR_` and `EASY_DIFFICULTY_COLOR` for `orange`, `yellow` and `green`) are read at load and exempt from the 4.5:1 floor as the client gives them; their fallback hex keeps it (ADR 0085, 2026-10-17).

Item names keep the client's exact quality colours (`q0`–`q7`), exempt from the 4.5:1 ink floor. `materials-contrast` checks them at 3:1 on resting `ground`, `panel` and sheet (`raised`) only; transient hover is exempt, as in the client's list highlight (ADR 0085, 2026-10-15).

**The One-Table Rule.** Every colour, face and piece of client art comes from the one entry in `U.STYLE.materials` (ADR 0085). A source test fails on any colour outside it; the token check refuses a second look.

**The Classic-Up Rule.** Start from the classic client and build up; never take from retail and build down (Shane's doctrine, 2026-10-11). A new control is a classic control with a facelift.

**The One-Register Rule.** The window and the world are one register (R13). The world frames wear the tooltip-border family (`U.classicBackdrop`: the client's tooltip border and background on the `menu` fill at 0.92, Market's `menu` panel where `BackdropTemplate` is missing): the Scan bar, the alert banner (`GameFontNormal` over `GameFontHighlight`), and the bag value tab and its panel. The guide tracker is the exception: it borrows Questie's tracker grammar (R15; see Guide tracker). The dropdown list and GameTooltip are dark; popups use the client's frame templates.

The bag value panel is 420 units wide, with measured counts beside compact values so names take
the remaining width. Its basis reads "at last asks"; one pencil footer keeps the omitted value,
price ages and bank state ("+6 more 9s 22c · prices 18–21m · bank 1h", or "bank ?"). Each 24-unit
row keeps the native item tooltip. Every Market line on an item tooltip is a label pair, the
client's gold label with its colon ("Market Price:", "Best Exit:", "Sells:") and the figure right
in white. The head reads "Market Price:" and its pace mark (▲▲ `pace1`, ▲ `pace2`, ◆ `pace3`, ▼
`pace4`, ▼▼ `pace5`, a `pencil` dot when unknown) on every budget, then one unit value and age; an
AHledger median and its table age stay on that line in pencil. Shift's "Sells:" words take the
mark's ink (ADR 0180). "Stack of N:" appears only for quantities over one, read from bags, mail and
vendor offers; the rounding listing is gone.
Under native auto, a loaded AHledger addon suppresses only the duplicate median value, keeping
the stack total. The Trading hint appears only under Shift at an open AH or Market window,
never on Market's own rows (ADRs 0013 and 0081, 2026-10-16 R14 amendment).

## Typography

**Display Font:** Friz Quadrata (client `Fonts\FRIZQT__.TTF`)
**Body Font:** Arial Narrow (client `Fonts\ARIALN.TTF`)
**Label Font:** Friz Quadrata for action buttons; the window's title in `GameFontNormal`

**Character:** the client's own: gold Friz over white narrow figures. No Morpheus.

### Hierarchy
- **Display** (18 px Friz): the Trading item name, the Gold page's net line.
- **Title** (14 px Friz): headings and section headers (gold), tabs, sections.
- **Lead** (18 px, the figure face): the one price a page leads with (Trading's header price, R9).
- **Figure** (15 px): standalone figures (the header ask, the Gold page net value, Position cells).
- **Body** (13 px): every cell, label, note, segment and dropdown, primary figures in rows included.
- **Small** (12 px): the chart's words and the world satellites' lines.
- **Micro** (11 px): axis ticks, column headings (gold), tallies, footnotes. Nothing else.
- **Button** (11 px Friz Quadrata): `UIPanelButtonTemplate` labels.

### Named Rules
**The Client-Faces Rule.** Only the client's fonts. A face the client lacks falls back to Friz Quadrata (`SetFont` returns false); the preview's stand-ins are layout evidence only.

**The Plain-Glyph Rule.** Player text is ASCII plus `·`, `—`, `–`, `×` and the footnote dagger `†`; a cut reads "..." (ADR 0037 phase A, ADR 0047 LM13).

## Layout

- **Window:** `M.TERMINAL_SIZE` 760x540 to 3440x1440. First open is about 65% of screen height, width 55% of the screen held between 1.3 and 1.9 times that height. Geometry is saved per account and reopens clamped to the screen.
- **Viewports checked:** compact 760x540, large 1024x700, auction 792x482 (content at 4,29), hd 1056x702 (first open on 1920x1080), ultrawide 1778x936 (first open on 3440x1440). The preview adds 1440x900.
- **Frame:** the client's dark dialog stops 22 above the window's foot (the tab strip). Chrome 6 left and right, 26 above (the 6-unit border and the 19-unit title bar with its 1 px rule), 28 below (border and strip). The close button is 26 at the top-right; the bottom tabs stand left-aligned 12 in, 28 tall, widths 96, 84, 92, 112, 2 apart, over the frame's lower edge; the "?" (Feedback) is 22 at the strip's right end, 26 in from the window's edge. The AH host draws no frame and no bottom tabs.
- **Insets and spread:** the frame's inside is two insets, the dark `ground` in a 1 px `edge`, with a 6-unit gap (the gutter); each page is its inset's writing area, 8 in at the sides and 4 above and below. One status place per view (LM17).
- **Rhythm:** space 2, 4, 8, 12, 16; rows and heads 20, icons 16; controls 24 high, pad 8, gap 2, groups 12 apart. Row insets and column gaps are `space.m`. The toolbar, the range strip and the Book's tabs are 24 tall. A compact page drops optional columns before it shrinks type.
- **Slots:** every view places every cell as a named Layout slot that both painters must read (ADR 0074; Trading's `header`, `strip`, `position`, `rail`, `book` and the Gold page's `period`, `income`, `spending`, `net`, `lists` by ADR 0079). The Tools sheet is 502x292 (`M.TERMINAL_TOOLS`).
- **Measure:** the Gold page's ledger column is at most 420 units, centred on its page; a wider page pads its margins and the leaders stop at the column. A page narrower than 420 is its column.

## Elevation & Depth

Flat, by the client's art. The frame's depth is the profession window's own (R15, ADR 0085's
2026-10-17 amendment, `U.chrome`): the client's `ButtonFrameTemplateNoPortrait` NineSlice metal on
Market's own child frame, the tiled `UI-Background-Rock` below the 21-unit band and its
`_UI-Frame-TopTileStreaks`. Where that art is missing, the gold dialog border
(`Interface\DialogFrame\UI-DialogBox-Gold-Border`) over its dark background
(`UI-DialogBox-Background-Dark`); a client without the backdrop keeps the flat `frame` fill in
Market's 2 px `trim` edge. Insets are a 1 px `edge` on the dark `ground`. The selected bottom tab is
the template's raised active art. Layering is draw order (insets at background sublevels -8 and
-7) and frame strata for satellites. Client art is guarded: each art key lists candidate files,
and a missing file leaves the flat token colour (LM8).

**The No-Fake-Depth Rule.** Client bevels or nothing. The preview's box-shadows (the Details slip, the tooltip stand-in, the coin discs) are not in the addon and are not part of the system.

## Shapes

Rectangles. The addon sets no corner radius; the client's own art (tabs, buttons, the dialog border) brings its own shapes. Nothing is pointed or pill-shaped. The preview rounds tabs and buttons as stand-ins for client art; that is not canonical.

## Components

### Buttons (`action`)
- **Shape:** the client's red `UIPanelButtonTemplate`, its own art; gold `button` label in Friz 11.
- **Fallback:** without the template, Market's raised fill in a `muted` hairline at 0.6 with `text` ink.
- **Open:** Overview's Positions, Movers and Professions headings are 24-unit controls opening their tabs (ADR 0185).

### Bottom tabs (`U.tab`)
- The client's `PanelTabButtonTemplate` under the frame: the selected tab in the template's active art with a white label, the rest gold. Without the template, Market's `index` control: the `tab` fill in `trim`, the selected one `raised` and open to the frame above. A disabled tab is pencil and says why in its tooltip.

### Tabs, sections and segments
- **`tab`** (AH host toolbar): title type, `soft` idle; selected in `text` over a 2 px `accent` rule.
- **`section`** (Positions, History, Listings, Sessions; Tools tabs): title type, `muted` idle; selected in `text` over a 1 px `soft` rule.
- **`segment`** (the watch rail's sort and window, the "?"): body type, `soft` idle with no fill; selected in `text` on the `raised` fill.
- **Segment group** (`U.group`: ranges, periods, the guide scope): one classic segmented control. Cells at least 24x24, side by side on one `raised` fill in a `rule` line, sharing their rules (only the last draws its right); the chosen cell on the `hover` fill.
- **Section header** (`U.header`): the Tailoring frame's category header, gold Friz on the recipe list's own header bar (`common-button-list-collapseExpand`), its collapse minus and plus at its right where the section folds (R15). Where that atlas is missing, the dark brown `bar` over a 1 px `trim` gold edge and the client's plus-minus buttons. The Overview's headings wear it.

### Dropdowns (`dropdown`, `item`)
- The choice beside the classic scroll-down arrow on the raised fill in a hairline. Its list is a `menu` panel: `menu` fill at 0.95 in a `menuEdge` line, choices 24 tall and 25 apart in `menuText`, the chosen one in `heading` gold.

### Panels
- **`region`:** the panel fill in a hairline. **`sheet`:** a slip laid over a view (Tools): the raised fill in a `rule` line. **`menu`:** the classic dark list.

### Rows and tables
- `U.row`: the hover lies beneath the words: the client's list highlight (`UI-QuestTitleHighlight`) tinted `hover` at 0.3, or the flat `hover` at 0.3, added (ADD) in the HIGHLIGHT layer, never blended over a label. A selected row wears the client list's gold glow line (`U.mark`): the client's list highlight (`UI-Listbox-Highlight2`) tinted gold and added beneath the words over a 1 px `heading` line along its foot, the flat line alone where the art is missing. Rows are 20 tall and answer across 24. One pooled table painter (`U.table`) with `micro` gold headings and `body` cells; it hosts the classic scroll bar (`U.scroll`, `U.scrollTable`: the client's knob and arrows, 24 units each, flat fills with "^" and "v" where missing).
- The Gold page: headings over a rule, dotted pencil leaders to each figure, double-ruled totals, the net the largest line (LM14).

### Gold page
- **Ownership:** the left page of Overview (ADR 0185), with Today, 7 days, 30 days and Session periods and the character scope. The window's size limits and first-open size stay unchanged.
- **Headline:** “Net today”, “Net, 7 days”, “Net, 30 days” or “Net this session”, then the signed net in `up` or `down`. Unknown figures stay in `pencil` with their reason.
- **Day row:** the existing “Each day, last 7” row sits below the headline. Recorded days keep their signed compact tally and loss ink; missing days keep the existing pencil reason. No new bar chart.
- **Reasons:** Income and Spending split the ledger's reason groups by sign. Coins align at the right, and each section ends with its total above a rule. Unexplained remains pencil. The ledger's rollups, recent-ring limits and attribution rules are unchanged.
- **Drill:** selecting a reason marks its left edge in gold and replaces the Next page with its Item, Count and Gold evidence. AH reasons stay in this drill. “‹ Next” returns to the Next page. Drill selection is runtime only; a period or character change clears it. Missing recent-ring evidence stays pencil with its reason.
- **Targets:** period controls, reason controls and the return control keep 24-unit reach. The ledger column stays at most 420 units wide, centred on its page; the scope moves beneath the periods when needed.

### The chart
- **One chart** (ADR 0092): 1D, 7D (default) and 30D, no other control. Over history the line is AHledger's median in `pencil`, 2 px; the player's asks are 6 px `line` ink dots on it, each bucket's lowest; the listed quantity is a band of `pencil` bars at `partialAlpha` in the plot's lowest fifth. With no history the table's median is a dashed `pencil` rule over its 30-day low-to-high band, `pencil` at `gridAlpha` ruled at both edges at `partialAlpha`.
- **Line:** with asks alone, observed joins in `line` ink, 2 px. **Carries:** pencil dashes, 4 on 3 off, 1 px at 0.7 (3:1 after alpha on the inset). A dot only where the line alone cannot show the vertex (R4): the newest ask's 7 px marker and a 4 px dot on a lone ask with no ink join either side ("A lone dot is one ask." in the key's tooltip). No scattered unlabelled dots.
- **Plot:** on the inset's dark fill (plot 0.85, no wash beneath the line: fill 0), ruled at the price ticks only with faint `pencil` rules at 0.07 and no other grid line (R10). "Last seen" is a `pencil` rule at 0.7, 3:1 after alpha, with its words in micro pencil. The price tag goes pencil with its age once carried or an hour old (LM31).
- **Zones:** the player's buy and sale bands in `buy` and `sale` as ruled edges with their words in the margin, never a wash (`zoneAlpha` 0, `zoneEdgeAlpha` 1; R4).
- **Sparklines:** `U.sparkline`, the same display list at 1 px, carries in pencil.

### Trading page
- **This item** (ADR 0080, R13): the name in its quality ink and the going price in `lead` on one line, the basis under them in w3-prices' words ("Lowest ask · 7s" `soft`, "AHledger median · 9h" `pencil`); then the **action row**: Watch, Tools and Refresh as red `UIPanelButtonTemplate` buttons, each sized to its label, side by side under the item. No slip covers the list; Plan and Listed are lines of the header's tooltip, only when they exist.
- **The strip:** the ranges' segment group, 1D, 7D and 30D, and nothing else (ADR 0092).
- **The key:** one line above the plot, each mark a swatch drawn as the chart draws it: a `pencil` rule for "median † 1h", a `line` dot for "yours 7s" (a 2 px `line` rule with asks alone), a `pencil` bar for "Listed †", `pencil` dashes and a band for a table's "median † 30m · 30-day range"; "† AHledger" once on the note's line with the reason no history stands; its tooltip says what each mark is. The note under it (a thinned range, untimed prices, a newer quote) wraps on a compact page. Zone words stand only in the margin column; with no room for one they are not drawn. The tag never covers a price label: the label moves past it.
- **Position strip:** three cells side by side at the page's foot, `micro` gold labels "Held · Avg cost · P&L" over full-width `figure` values; the percentage stands beside the label and a compact amount replaces coin art when needed; "bank ?" in `pencil` beside Held only while the bank is unread; unknown-cost Avg cost and P&L values stay absent; the tooltip names their source and reason (R14, ADR 0093). Where the units are, what the cost covers and the 5% AH cut stand in each cell's tooltip.
- **My book:** the search box with Lists beside it; the watchlist's groups are section headers (`U.header`) with the client's minus and plus, the rows with no evidence folded into "+29 unpriced" in `text` ink beside its plus; the change column's head cycles 24h, 7d and each sorted by the biggest move, `text` while sorted; a sparkline with no observed move is blank. The Book's tabs over one `U.table` behind the classic scroll bar (`U.scrollTable`) showing every row; on Positions the Book takes height before the rail. R14 (ADR 0093) gives Positions one Source column, AH, Vendor, Crafted, Looted or pencil "?", its quantities and reason on hover. Only this character's tradeable held rows appear; unpriced rows fold into "+N unpriced". The scrollbar always has its own 24-unit lane. Below 720 units of usable table width, the name takes its own line over Held, Source, Avg cost and P&L, with 24-unit lines; at 720 or wider, Positions uses one row. Unknown costs and P&L stay absent. AHledger's footnote stands once, at the right page's foot: "† AHledger · 25m · sells ~412/day".
- **Tabs:** the bottom tabs read Overview, Trading, Professions; the AH host keeps its two pages.

### Overview page
- **Spread:** Gold on the left, Next on the right (ADR 0185). Bottom tabs are Overview, Trading and Professions. A saved or dispatched `gold` view resolves to Overview. The separate Session block and Ledger tab are removed.
- **Next order:** Alerts, Positions, Movers, Professions, each with the shared section header. Empty Alerts collapses. Alerts show at most three rows, Positions four and Movers five; overflow counts stay explicit.
- **Positions:** one row per holding, with icon, item, held, average cost and P&L. The heading names held count and estimated worth. Partial P&L and units not bought on AH retain their pencil reasons and the held-position rules (ADR 0065).
- **Movers:** watch-change rows with item, sparkline, price and change. Their title opens Trading, as does Positions. Professions shows the active guide's next line and its title opens Professions; skill bars and the separate red Open buttons are removed.
- **Drill:** the selected Gold reason replaces Next, with “‹ Next” above its evidence. All cells remain named Layout slots and Window records them in `M.window.cells` (ADRs 0074, 0078). Hosts never write Store while painting; composing a ready Overview still marks alerts seen.

### Professions page
- **Reading order** (ADR 0084, amended 2026-10-15): next, then the trainer, each fact once. The left page lists the learned lines as status bars, the route's section header (`U.header`, the line's name), the steps, and the credit at the foot. The right page is the "Reagents" section header with the scope segment group on its bar, the shopping table, then directly under its last drawn row the summary and the red "Watch these"; the AHledger footnote stands at the page's foot.
- **Status bars:** each learned line is one 24-unit row holding the shared `U.statusBar` (the client's `Interface\TargetingFrame\UI-StatusBar` art and flat fallback tinted `skill` #2f237c at 0.6) over a `ground` track, its words inside and centred in `body` `text`: "Tailoring 131/150", the rank over the current max, one denominator. The open line wears the selection's gold line; a dismissed line reads "First Aid · hidden" in `pencil` with no fill, and a line this character no longer has stands last, "Skinning · dropped at 150" in `pencil`, with no bar (R14). The open line's trainer ticks stand as 1 px `pencil` marks in the row's margin above the bar, each with a 24x24 target naming the cap its rank trains to ("Journeyman to 150", R14); the route's scale only in the last tick's tooltip ("The route runs to 225").
- **Steps:** 24 tall. The done steps fold into one row, "8 steps done", with the client's plus and minus (`M.plusMinus`); opened, they stand struck in `pencil`. The current step is one row in `title` type with a 2 px `text` margin mark (never the selection mark, R12): "Create Gloves of Meditation ×12 · about · yellow" in w3-guides' words, its skill range at the right in micro `pencil` ("skill 125-140") and its progress in `text` only once started ("· 2/20"); the title takes the row less the detail's measured words and its tooltip carries the full title; a current title longer than that wraps onto a second step row in the same `title` type (never smaller), the detail and the alternates arrow keeping the first line and the steps under it one row down. The alternates are the classic dropdown's arrow (24 units) on the current row, the cheaper alternate in its tooltip; no hint words on the page. Other steps read "<name> ×<crafts>" with their range; the next steps and the next trainer row in `text`; every step after the next trainer in `pencil`, with no reason word ("not yet" is the page's reading). A trainer row reads "Train Expert · 45s · Stormwind" (the cost once Market has seen the trainer, the city without "City"), its unmet requirements at the right in micro `pencil` ("needs skill 125, level 20"; a met one, or a zero, never shows; a later trainer "Train Artisan · needs skill 200", R14); its tooltip names the player's own faction's trainer, its city, quarter and coordinates, and the requirements, one short line each.
- **Credit:** "Route from WoW-Professions" in `micro` `pencil`, `text` on hover, at the left page's foot; a click opens the route-credit popup. Never a button: red is for actions.
- **Summary:** two lines under the table's last drawn row: the total in `figure` (15) `text` ink ("20g 12s 53c this bracket") with "· ~29s 59c/point" in `body` after its measured words, then the oldest price's age, an unpriced count only when there is one, and the bank note whole in micro `pencil` ("prices 9h old · 2 unpriced"); Watch these under them.
- **Shopping table:** `U.table` behind the classic scroll bar (`U.scrollTable`) at its right when the rows outrun the page; the columns and the rows' hover leave the bar its 24 units.
- **Unknowns:** an output or item with no learned name reads "loading" in `pencil`, never "Item 7026"; a missing price reads "no price".

### Guide tracker
- **Grammar** (R15; ADR 0096, ADR 0068 and 0087 amendments, 2026-10-17): Questie's tracker, with no box. Market's own unnamed frame, anchored read-only `TOPLEFT` 4 under Questie's tracker frame's `BOTTOMLEFT` at its width (180-400) while Questie is loaded and that frame shows; else 260 wide, 10 under `ObjectiveTrackerFrame`'s NineSlice while it shows (ADR 0089 (e)); else at its saved place; never below the screen's bottom edge.
- **Header:** one small line, "Profession Guide: 2" (the guided professions shown) in `trackerHead` (Friz 12) `heading` gold, no bar; the module collapse atlas at the right (`M.plusMinus`'s art, then a glyph, where missing). Left click collapses to the header alone; right click hides.
- **Blocks:** per profession a zone line, "Enchanting 141/150", in `trackerHead` `heading` (a click folds it for the session); the step as the title, "Create Lesser Intellect ×15", in `trackerLine` (Friz 10) and the current recipe's colour (`orange` #ff8040, `yellow` #ffff00, `green` #40bf40, `gray` #808080; `objective` for a train or gather step, `pencil` while loading) after the client's 12-unit plus/minus (a click folds its objectives); then objectives 15 in from the step's words in `trackerLine` `objective` #eeeeee with no dash: "Lesser Magic Essence: 15/60" per reagent, "Buy the recipe from a vendor" or "Learn from a trainer", and the next trainer near a cap. When the bags cover every reagent of a learned step, the reagent lines fold into one "Ready to create" in `complete` #28ff28. No line wraps; a long name is cut, the whole step in its tooltip.
- **Targets:** the header, each zone line, each step and each reagent line answer across 24 units; other lines are the font's own 14; no gap after a step. A hovered reagent turns `text` white with the item's tooltip and no fill; a click opens Trading on it. Five professions at most; "+N more" only past that, on its own line.
### Profession window marks (ADR 0089)
- **Inside the client's window** Market adds a margin note only in the client's own hand, and never moves a word Blizzard wrote. Each recipe row gets a 6x6 dot at its right edge in its margin's tier (`M.marginRead`, R15): `up` over +10% of cost, `pencil` within 1%, `yellow` down to -30%, `down` below that. A row without a margin gets a `pencil` "?" in `GameFontHighlightSmall`. When 7-day history exists, a "+" or "-" trend in `up` or `down` stands left of the dot. The selected row adds "+21s 34c (+31%)" in `GameFontHighlightSmall` only when it fits right of the label's drawn words. Otherwise the hover carries it.
- **The hover and detail line** is one line of compact coins: "cost 14s 16c · makes 14s 73c † after 5% cut · margin +57c (+4%) · sells fast †". Labels and separators are `soft`, values `text`, the margin in its tier's ink, always signed, and unknowns ("?", "enchant") `pencil`. The hover is the client's `GameTooltip` with the recipe's name over it. The detail line sits under the recipe's name in the schematic form.
- **The dock** wears the profession window's own frame (`U.chrome`, R15) beside the window, right of its side tabs, never over them: "Profit · Tailoring" in its title band (the tooltip frame and a `U.header` where the art is missing), a micro `pencil` note naming the cut, and the one table (`U.scrollTable`) of 24-unit rows: Recipe, Margin, Per point. A recipe to learn reads "Learn from a trainer" or "Buy the recipe from a vendor" in `pencil` in the last column, its name in `soft`.

### Frame and grip
- The profession window's metal and rock with "Market" centred in its band in `GameFontNormal` gold (R15; the dark dialog in its gold border and its title bar where the art is missing), the client's `UIPanelCloseButton`, the bottom tabs, the "?", and the classic size grabber in a 32-unit target (ADR 0085).

## Do's and Don'ts

### Do:
- **Do** take every colour, face and art key from the one entry in `U.STYLE.materials`.
- **Do** name each value's ink in the text model or display list; pencil for carried, estimated, unknown or old.
- **Do** say why an unknown is unknown in plain words: "?" for a day with no record, "open your bank to count", "not bought on AH" (LM15, LM24; ADR 0082).
- **Do** use the client's templates and art: `UIPanelButtonTemplate`, `UIPanelCloseButton`, `PanelTabButtonTemplate`, the dialog border, the size grabber, the scroll bar and arrows, quality colours, coin icons on standalone figures.
- **Do** keep every hover beneath the words: added, never a fill blended over a label.
- **Do** give every control and row a 24-unit target (`U.reach`, LM22, LM30).
- **Do** footnote an AHledger figure with † and its table age at the page's foot (LM13, LM33).

### Don't:
- **Don't** use fluorescent or off-palette accents, gradient or glass shading, or pointed and pill shapes (doctrine).
- **Don't** draw flat, borderless web panels, or copy a retail widget where a classic one exists.
- **Don't** use red for anything but a loss.
- **Don't** ship art or fonts, or bring back a second look, parchment, leather, brass or Morpheus.
- **Don't** put a coin icon in a row, column or axis; rows use compact coin letters.
- **Don't** put `·` in a title, label or button, or use glyphs outside the plain set.

Not canonized (craft-floor defects the build carries, not rules): none.
