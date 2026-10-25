# North star: what the typesafe.ai landing page does well

Studied live on 2026-10-24 at 1440 and 390 wide, in headless Chromium, with computed styles read from the page. These are the moves it makes, written so they can be checked on our pages. We copy none of its brand, copy, art, or color. Our version of each move is under it.

1. **One sentence, set huge.** The hero is one 18-word sentence at 150px with an 0.8 line height, weight 500, and nothing beside it. The next size down is 64px. Body is 22px. Labels are 12px. That is four sizes with big jumps between them, roughly 7 : 3 : 1 : 0.5.
   *Ours:* the h1 is the largest thing on the page by a wide margin. Four sizes do the work, and the steps between them are big.

2. **Two faces, two jobs.** A grotesk carries every statement and paragraph. A monospace at 12 to 13px carries labels, categories, and footnotes, and nothing else. You can tell what a piece of text is before you read it.
   *Ours:* Host Grotesk for words. JetBrains Mono for labels, counts, and the reality-check values a nurse scans for.

3. **A label, a hairline, a block.** Each text block has a small mono label above it and one 1px vertical rule on its left. There are no boxes or cards. The rules carry the structure.
   *Ours:* reality-check values and guide sections use a mono label and a left rule instead of bordered panels.

4. **Corner marks instead of frames.** Sections are framed by four small corner brackets, like registration marks on a print, not a full border.
   *Ours:* the proof figures and the reality check sit inside corner marks. Nothing gets a full border unless it is a control.

5. **Proof is a number.** The page's second headline is "193.6x faster, 444.6x cheaper", with a footnote and a Proof link. A side-by-side shows the cost and time of each option. Big claims come with a figure.
   *Ours:* the directory's own counts, computed at build time from `tools.json`: how many tools are built for nurses, how many mention HIPAA, how many fit bedside work, and how many we could not verify. Every figure links to the filter that shows it.

6. **Few words.** The page is about 930 words across 10,800px. Section heads are 3 to 6 words. Body blocks are 2 to 5 sentences.
   *Ours:* one line per idea. Cut every sentence that restates the one before it.

7. **Color belongs to sections, not words.** Text is one near-black ink, with secondary text at 86% of it. Color comes as whole flat grounds per section: white, then pink, green, and black. There are no accent colors inside running text.
   *Ours:* paper ink on warm paper, one inverted ink band for the reality-check explainer, and the Market rule that red means harm and green means a stated HIPAA posture. Nothing else is colored.

8. **Room to breathe.** Sections are 150 to 250px apart at 1440. Content sits in a 1240px column with 100px margins, and blocks are placed on a grid with deliberate empty columns.
   *Ours:* a spacing scale that reaches 96px and 128px for sections, and a 12-column grid where the reading column stays near 62ch.

9. **Actions are words.** "Create Account" and "Join Discord" are 64px underlined text, not pill buttons.
   *Ours:* the two hero actions are large underlined links. Real buttons stay for forms, where a nurse expects one.

10. **Texture from the audience's world.** Its texture is the developer's: terminal windows, base64 strings, a Game of Life glider. It tells the reader the page knows them.
    *Ours:* the nurse's world. Column heads read like a flowsheet, the reality check reads like a chart entry, and values are set in mono like a MAR.

11. **The phone keeps the hierarchy.** At 390 the hero drops to about 48px and still dominates. Columns stack. Labels keep their size.
    *Ours:* same order and the same four sizes, scaled with `clamp()`. The first tool row stays reachable with one thumb scroll.

12. **Quiet motion.** A clock ticks and a glider steps. Nothing flies in on scroll.
    *Ours:* hover and focus changes only, and none under `prefers-reduced-motion`.

## What we keep from our own system

Market's Ink Rule stays the core: what the directory verified is in full ink, what it could not verify is pencil with the word Unknown beside it. Square corners, 1px rules, no shadows, gradients, or blur. Light warm paper first, dark when the device asks. 44px controls. Contrast at least 4.5:1 for text.
