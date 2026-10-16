---
name: Nurse AI Tools
description: A 1971 clinical futures manual for a nurse scanning an AI tool index.
colors:
  field: "#123655"
  copper: "#8c4a32"
  amber: "#7a4e00"
  amber-bg: "#f8edd4"
  teal: "#0c5c4c"
  teal-bg: "#e4f3ee"
  paper: "#e7eef2"
  ink: "#14202b"
  ivory: "#f4f1e6"
  line: "#737d85"
  hair: "#b9c1c6"
  muted: "#535e67"
typography:
  display:
    fontFamily: "Syncopate, \"Source Sans 3\", sans-serif"
    fontSize: "clamp(1.25rem, 0.1rem + 7.2vw, 3rem)"
    fontWeight: 700
    lineHeight: 1.05
    letterSpacing: "0.02em"
  headline:
    fontFamily: "Syncopate, \"Source Sans 3\", sans-serif"
    fontSize: "clamp(1.35rem, 1.05rem + 0.8vw, 1.75rem)"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0.03em"
  title:
    fontFamily: "Source Sans 3, sans-serif"
    fontSize: "1.1875rem"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "normal"
  body:
    fontFamily: "Source Sans 3, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Source Sans 3, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 600
    lineHeight: 1.5
    letterSpacing: "normal"
rounded:
  none: "0"
spacing:
  tight: "0.375rem"
  control: "0.5rem"
  row: "0.75rem"
  inset: "0.875rem"
  stack: "1rem"
  section: "1.5rem"
  band: "2.5rem"
components:
  button-primary:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.5rem 1.25rem"
    height: "2.75rem"
  button-primary-hover:
    backgroundColor: "#1d4a72"
    textColor: "{colors.ivory}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.5rem 1.25rem"
    height: "2.75rem"
  button:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.875rem"
    height: "2.75rem"
  input:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.875rem"
    height: "2.75rem"
  input-search:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.5rem 1rem"
    height: "3.25rem"
  select:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
    padding: "0.5rem 2.5rem 0.5rem 0.875rem"
    height: "2.75rem"
  toggle:
    backgroundColor: "{colors.ivory}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.5rem 1.125rem 0.5rem 0.875rem"
    height: "2.75rem"
  toggle-checked:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.5rem 1.125rem 0.5rem 0.875rem"
    height: "2.75rem"
  bay-caution:
    backgroundColor: "{colors.amber-bg}"
    textColor: "{colors.amber}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.625rem 0.625rem"
  bay-stated:
    backgroundColor: "{colors.teal-bg}"
    textColor: "{colors.teal}"
    rounded: "{rounded.none}"
    padding: "0.5rem 0.625rem 0.625rem"
  mast:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ivory}"
    typography: "{typography.display}"
    rounded: "{rounded.none}"
    padding: "clamp(1.35rem, 2.5vw, 2rem) clamp(1rem, 4vw, 2.5rem)"
---

# Design System: Nurse AI Tools

## Overview

**Creative North Star: "The 1971 Clinical Futures Manual"**

This is a clinical index drawn as a 1971 futures manual. The page sits on cool daylight paper. A full-bleed field-blue masthead carries an ivory wordmark, and the only texture on the site is a 1px diagonal security tint inside that masthead. The directory below is a ruled list a nurse can scan.

The signature is the three-bay status plate, labeled Built for, HIPAA status, and Bedside fit in the words the data already uses. A copper rule runs across the top. It is visible at rest, and when a filter settles it draws once from the left in 180ms ease-out. That animation is removed under prefers-reduced-motion. Controls stay ordinary inputs and buttons, each with a single top-right chamfer and an inset focus ring.

The retro-futurist pin is held as this manual: a credible clinical reference with personality. It refuses neon, glow, glass, gradient text, emoji, and kickers. Contrast, a visible focus state, and reduced motion belong to the material. Nurses is never colored as a grade.

**Key Characteristics:**

- Cool daylight paper, a field-blue masthead, and an ivory wordmark
- Syncopate 700 for display, Source Sans 3 for reading and for scannable tool names
- Square corners, with one 10px top-right chamfer on controls
- A three-bay status plate whose copper rule is the only motion
- Flat depth from the masthead, 2px ink rules, and hairlines

## Colors

The palette is cool clinical daylight. Field blue does the structural work. Copper, amber, and teal are reserved for one job each. The scheme is light only. Selected text is field blue on ivory. The caret is field blue.

### Primary

- **Field Blue** (`colors.field`): Masthead, primary buttons, text links, the unclipped focus outline, and text selection. The browser theme color matches it. The primary button's hover fill is a darker field blue (`#1d4a72`) on `button-primary-hover`, and that fill stays on the primary button.

### Secondary

- **Plate Copper** (`colors.copper`): The 2px rule across the top of the status plate.

### Tertiary

- **Caution Amber** (`colors.amber`) on **Caution Wash** (`colors.amber-bg`): The reality-check values Unknown and Not for patient info. The same amber ink colors a form error and the border of an invalid control that is not focused.
- **Stated Teal** (`colors.teal`) on **Stated Wash** (`colors.teal-bg`): The reality-check value Mentions HIPAA. The same teal ink colors a form success message.

### Neutral

- **Daylight Paper** (`colors.paper`): Page background and the surface under untoned plate bays.
- **Manual Ink** (`colors.ink`): Body text, tool names, and the 2px rules.
- **Ivory** (`colors.ivory`): Wordmark, masthead link text, input wells, primary button text, selection text, and the focus ring on a field-blue control.
- **Rule Line** (`colors.line`): Resting control borders and the scrollbar.
- **Hairline** (`colors.hair`): Dividers between index rows, plate bays, and definition rows.
- **Muted Ink** (`colors.muted`): Secondary text, placeholders, the result count, and plate labels on an untoned bay.

### Named Rules

**The Plate Copper Rule.** Copper is the 2px line across the status plate and nothing else.

**The Grade Tone Rule.** On a reality-check value, amber means Unknown or Not for patient info, and teal means Mentions HIPAA. Nurses is never colored as a grade, and neither are Physicians, Both, General, or a bedside-fit phrase other than Unknown. Form errors reuse amber and form success reuses teal. Those messages are not grades.

## Typography

**Display Font:** Syncopate (with Source Sans 3, then sans-serif)
**Body Font:** Source Sans 3 (with sans-serif)
**Label Font:** Source Sans 3 at weight 600

**Character:** Syncopate is the wide uppercase manual face, used with tight tracking. Source Sans 3 does the reading. The index stays scannable because tool names never switch to the display face. Both families are self-hosted, Syncopate at 700 only, Source Sans 3 at 400 and 600. The page loads no font from another origin.

### Hierarchy

- **Display** (700, `clamp(1.25rem, 0.1rem + 7.2vw, 3rem)`, line-height 1.05, tracking 0.02em, uppercase): The wordmark. It is the largest type on the page.
- **Headline** (700, `clamp(1.35rem, 1.05rem + 0.8vw, 1.75rem)`, line-height 1.25, tracking 0.03em, uppercase): Page titles, held to about 16em and balanced across lines. Section headings use the same face, weight, tracking, and uppercase, at 1.0625rem for the closing band, 1rem in prose, and 0.9375rem over the reality check.
- **Title** (600, 1.1875rem, line-height 1.25): Index tool names, in Source Sans 3 and Manual Ink. They are not underlined until the row is hovered.
- **Body** (400, 1.0625rem, line-height 1.5): Page text. The opening lede steps up to `clamp(1.125rem, 1rem + 0.5vw, 1.3125rem)` at line-height 1.45. The "what it does" line stays within about 62ch. Prose columns sit near 42rem, and a tool article near 46rem.
- **Label** (600, 1.0625rem, line-height 1.5): Field labels, filter labels, and buttons, in Source Sans 3. Plate values are the same weight at 0.9375rem and line-height 1.25. Plate labels and the index column head are the display face at 0.8125rem, uppercase, tracking 0.03em. On an untoned bay the label is Muted Ink. Inside an index row the label reserves 2.5em so it can wrap to two lines. On a tool page it does not reserve that height.

### Named Rules

**The Display Budget Rule.** Syncopate 700 is the wordmark, page titles, section headings, the index column head, and plate labels at 0.8125rem. Index tool names, field labels, buttons, and plate values stay Source Sans 3.

## Layout

The page is one column in a 72rem wrap. Inline padding is `clamp(1rem, 4vw, 2.5rem)`. The masthead is full bleed. The wordmark and the site links share the bottom edge of that band, with 0.85rem of row gap and 2.5rem of column gap, wrapping when they no longer fit.

The index is a three-column grid: `minmax(11rem, 15rem)` for the tool, `minmax(0, 1fr)` for what it does, and `minmax(20.5rem, 26rem)` for the reality check. The column gap is `clamp(1.25rem, 3vw, 2.5rem)`. A 2px Manual Ink rule closes the column head. Each row is separated by a hairline, with 1.125rem of padding above and 1.25rem below.

At 52rem the column head is hidden, the index itself takes the 2px ink rule along its top, and each row stacks tool, description, then plate. The closing band stacks to one column.

At 32rem the plate stacks to one bay per row. Each bay becomes a 7.5rem label beside the value, divided by a hairline along the top instead of a left border. The category control grows to the full row, the count drops to its own line, and the tool specification list stacks.

The result count is a muted, tabular-numeric line at the end of the filter row. It is not a display number. The footer is muted 0.875rem copy under a hairline.

The spacing rhythm that actually repeats is tight stacks at 0.375rem, control block padding at 0.5rem, filter and deck gaps at 0.75rem, control inline padding at 0.875rem, a 1rem stack, a 1.5rem section break, and a 2.5rem band gap.

### Named Rules

**The Ruled Index Rule.** The directory is a three-column ruled list at desktop and a stack below 52rem. It is not a card grid.

## Elevation & Depth

The manual is flat. Nothing lifts, and there is no drop shadow. Depth comes from tone and rules. The field-blue masthead sits on the paper page. A 2px Manual Ink rule closes the column head, opens the stacked index, and separates the closing band. Hairlines divide rows, bays, and specification lines.

The masthead's only texture is a security tint: a 1px ivory line at 5% opacity, on a 135 degree diagonal, repeating every 5px. No other surface is textured.

The only box-shadow in the system is the inset focus ring on a chamfered control, documented in Shapes. It is a stroke, not elevation.

### Named Rules

**The Flat Manual Rule.** Surfaces do not lift. Do not add a drop shadow, a glow, or glass. The inset ring is a focus stroke.

**The Hatch Rule.** The masthead carries a 1px diagonal security tint, ivory at 5% opacity, 135 degrees, repeating every 5px. No other surface is textured.

## Shapes

Corners are square. `rounded.none` is 0, and every control sets that radius. Inputs, selects, textareas, buttons, and filter toggles share one chamfer: a 10px cut at the top-right, clipped with a polygon that runs from the top edge to the right edge. The other three corners stay square. A border-box gradient paints a 1px stroke along that diagonal, because a normal border does not follow the clip. The diagonal inset used for that stroke is the cut multiplied by 0.7071.

Rows, bays, the plate, the masthead, and the page itself are not chamfered.

The toggle's check is a separate mark inside an unclipped 1.125rem square. The select's caret is a 12 by 8 pixel hairline drawn in the control. Neither is a general icon style.

### Named Rules

**The One Chamfer Rule.** Controls have square corners and one 10px cut at the top-right. Nothing else is chamfered.

**The Inset Focus Rule.** Clip-path clips outlines, so chamfered controls clear the outline and draw focus inside the shape. The border turns Field Blue and a 1px Field Blue inset ring completes the stroke. Primary buttons and checked toggles draw a 2px Ivory inset ring instead. Unclipped links and index rows keep a 2px Field Blue outline, offset 2px. On the masthead that outline is Ivory.

## Components

Controls share one shell: an ivory well, Manual Ink text, a Rule Line border, a 2.75rem minimum height, padding of 0.5rem 0.875rem, and the single chamfer. Buttons and toggles set Source Sans 3 to 600. Fields stay at 400.

### Buttons

- **Shape:** Square, with the 10px top-right chamfer.
- **Primary:** Field Blue fill, Ivory text, Source Sans 3 600, minimum height 2.75rem, padding 0.5rem 1.25rem. Hover moves the fill to `#1d4a72` and keeps the Field Blue edge. Focus draws the 2px Ivory inset ring.
- **Default:** The ivory shell with a Rule Line border, used for a quiet action such as clearing filters. Hover turns the border Manual Ink. Focus uses the 1px Field Blue inset stroke from the Inset Focus Rule.

### Filter toggles

The same chamfered shell, set inline, with Source Sans 3 600 and padding 0.5rem 1.125rem 0.5rem 0.875rem. An unchecked toggle is an ivory well with Manual Ink text. Its mark is a 1.125rem square with a 1.5px border in the current color, and a clipped check that appears when the box is on. A checked toggle uses the Field Blue fill and Ivory text, and focuses like a primary button. Hover on an unchecked toggle turns the border Manual Ink. A checked toggle keeps the Field Blue edge.

### Text fields

Ivory well, Manual Ink text, Rule Line border, the chamfer, full width, minimum height 2.75rem, padding 0.5rem 0.875rem. Placeholder text is Muted Ink. Focus uses the inset Field Blue stroke. When a field is invalid and not focused, the border turns Caution Amber. Textareas use this shell and resize vertically. The search field is the same shell at a 3.25rem minimum height, 1.125rem type, and 1rem of inline padding. Its native cancel glyph is removed.

### Selects

The text-field shell, with the native arrow removed and a 12 by 8 pixel Manual Ink caret placed 0.875rem from the right. Inline padding on the right is 2.5rem so the value clears the caret. In the filter row the select sizes to its label, with a 15rem minimum, until the 32rem stack.

### Links

Text links are Field Blue, with a 1px underline offset 0.2em. Hover thickens the underline to 2px. Focus is the 2px Field Blue outline, offset 2px. Masthead links are Ivory and have no underline until hover or the current page, where the underline is 1px, offset 0.4em. Their focus outline is Ivory.

### Navigation

The masthead is full-bleed Field Blue with the security tint. The wordmark is the display face in Ivory, with no underline. The site links sit on the same baseline: Directory, Submit a tool, and About. A skip link sits at the top left of the page, Ivory on Manual Ink, and is hidden until focused.

### Status plate

The signature. Three bays in one row: Built for, HIPAA status, and Bedside fit. A 2px Plate Copper rule lies across the top and is visible at rest. A hairline closes the bottom. Bays are separated by a left hairline, and the first bay has none. Labels are Syncopate 700 at 0.8125rem. Values are Source Sans 3 600 at 0.9375rem. An untoned bay has no wash: the label is Muted Ink and the value is Manual Ink. A caution bay fills with Caution Wash and sets both label and value in Caution Amber. A stated bay fills with Stated Wash and sets both in Stated Teal.

While the directory is filtering, the copper rule draws once from the left, from scale 0 to full, in 180ms ease-out. Under prefers-reduced-motion the animation is removed and the rule stays put. Below 32rem the bays stack, and each bay becomes a 7.5rem label beside its value.

### Index row

Three columns, as in Layout. The tool name is a link stretched across the row, Manual Ink, with no underline until the row is hovered. Vendor and category sit under the name in Muted Ink at 0.9375rem. Focusing the name clears the link outline and draws the 2px Field Blue outline around the whole row, offset 2px.

### Definition rows

A tool specification is two columns, `minmax(8rem, 13rem)` and the remainder, opened by a 1px Manual Ink rule. Each term and value has 0.75rem of block padding and a hairline underneath. The term is Source Sans 3 600. At 32rem the rows stack and the term drops its own bottom rule.

### Messages

A form message is Source Sans 3 600. An error is Caution Amber. A success is Stated Teal. An empty message is not shown.

## Do's and Don'ts

### Do:

- Do paint the page in Daylight Paper and the masthead in Field Blue, with the Ivory wordmark on that field.
- Do keep Plate Copper to the 2px status-plate rule.
- Do use Caution Amber for Unknown, Not for patient info, invalid edges, and form errors, and Stated Teal for Mentions HIPAA and form success.
- Do leave Nurses untoned, along with Physicians, Both, General, and any bedside-fit phrase other than Unknown.
- Do set Syncopate 700 on the wordmark, page titles, section headings, the column head, and plate labels, and Source Sans 3 600 on index tool names, labels, buttons, and plate values.
- Do chamfer controls once at the top-right by 10px and draw their focus inside the clip.
- Do draw the copper rule in 180ms ease-out while the directory is filtering, and remove that animation under prefers-reduced-motion.

### Don't:

- Don't use neon, glow, glass, gradient text, emoji, or kickers.
- Don't add a drop shadow, and don't put texture anywhere but the masthead hatch.
- Don't color Nurses as a grade.
- Don't set index tool names in Syncopate.
- Don't round controls. The corner radius stays 0.
- Don't turn the index into an icon-card grid.
- Don't put copper on a button, a link, or body text.
