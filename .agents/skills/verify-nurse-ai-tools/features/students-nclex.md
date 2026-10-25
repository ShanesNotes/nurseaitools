# Students NCLEX guides

Four guides for nursing students preparing for the NCLEX. `landing.py` builds them from `tools.json`: it picks the tools by rules over each entry, and every claim about a tool is a `<q>` quote from that entry. The build fails if a quote is not found.

| Path | What it is |
| --- | --- |
| `/students/best-ai-nclex-prep` | NCLEX tools with an AI feature, side by side: AI, NGN, free or paid. |
| `/students/free-nclex-prep` | NCLEX tools that mention a free plan, tier, or trial. |
| `/students/ngn-practice-tools` | Tools whose entry mentions Next Generation NCLEX items. |
| `/students/chatgpt-for-nclex` | Study use of ChatGPT, Claude, and Gemini without patient information. |

## Sub-features

- `nclex-compare` lists tools in a `dl.spec`, each name linking to its `/tools/<slug>` page.
- `nclex-phi` states the patient-information rule.
- `nclex-related` links the other student guides and the directory on `/`.
- `nclex-signup` has the newsletter form at the foot.

## How to get to it (user POV)

Choose Students in the header, then pick a guide from the hub. Each guide links the others under Related guides.

## Driving it

`verify.py`:

- checks each guide is in the sitemap and answers 200 with a title, description, canonical, and one `h1`;
- in Chrome at 1280 wide, light, checks the hub and each guide for exactly one visible `h1`; at least one tool link, each naming a slug in `tools.json`; every on-site link answering 200; the newsletter form; and no script errors. The hub must link all four guides;
- runs the style audit on each guide at 390 and 1280 wide, light and dark: one visible `h1`, no sideways scroll, text size, 44px controls, link targets, and contrast;
- signs up from `/students/best-ai-nclex-prep` at 390 wide, dark, to the local server. Local D1 must then hold exactly the home address and this one.

`test/landing.test.js` (in `npm test`) checks each route's content against the built worker.

## Gotchas

- The guide list is `GUIDES` at the top of `verify.py`. Add a new guide there, or it gets HTTP checks only, from the sitemap.
- The guides are long. At 390 wide a full-page screenshot is 5,000 to 6,500px tall, so open the desktop shots first.
