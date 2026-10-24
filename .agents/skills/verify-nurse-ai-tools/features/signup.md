# Newsletter signup

The newsletter section sits at the foot of home, every tool page, and the guides. It posts JSON to `/api/subscribe`.

## Sub-features

- `signup-ok` thanks the reader and stores the address.
- `signup-bad` refuses a bad address in the browser and posts nothing.

## How to get to it (user POV)

Scroll to the end of any page.

## Driving it

`verify.py` fills the home form with `verify+<time>@example.invalid`, submits it to the local server, and expects "subscribed". With the default wrangler harness it then reads the local D1 `subscribers` table and expects exactly that address. It submits `not-an-email` and expects an error and no POST.

## Gotchas

The local worker has no Kit key, so it never calls Kit. The live Kit signup is verified-unreachable here. Never point this drive at the live site.
