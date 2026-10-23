# Submit a tool

The submit page is a form. A successful post is reviewed later. The preview does not store it.

## Sub-features

- `submit-form` shows the fields and the submit button.
- `submit-validate` refuses a bad URL in the browser.
- `submit-post` gets a JSON reply from the worker.

## How to get to it (user POV)

Choose Submit a tool in the header, or the submit door on home. The path is `/submit`.

## Driving it with the preview

Preconditions:

- The preview is up.

- **Record.** Run `python3 shoot.py`. `shots/submit-desktop.png` and `shots/submit-mobile.png` show the form. scrollWidth is `ok`.
- **Validate.** `npm test` walks the form from idle through error and success without a browser.

## Gotchas

A POST to `/api/submit` can return a message, and the stub database does not keep the row. A live Kit call does not happen. Both are verified-unreachable from this preview.
