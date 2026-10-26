# Newsletter signup

The newsletter section sits at the foot of home, every tool page, and the guides. It posts JSON to `/api/subscribe`.

## Sub-features

- `signup-ok` thanks the reader and stores the address.
- `signup-bad` refuses a bad address in the browser and posts nothing.

## How to get to it (user POV)

Scroll to the end of any page.

## Driving it

`verify.py` fills the home form at 1280 wide, light, with `verify+<time>@example.invalid`, submits it to the local server, and expects "subscribed". It submits `not-an-email` and expects an error and no POST. Then it fills the same form on `/students/best-ai-nclex-prep` at 390 wide, dark, with `verify+<time>-phone@example.invalid`. Each good submit must make exactly one POST, to the local `/api/subscribe`. With the default wrangler harness it then reads the local D1 `subscribers` table and expects exactly those two addresses. The style audit covers the form's 44px field and button on every audited page.

## Gotchas

The local worker has no Kit key, so it never calls Kit. The live Kit signup is verified-unreachable here. Never point this drive at the live site.
