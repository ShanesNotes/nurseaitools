# Submit a tool

The submit page is a form. A successful post is reviewed later. The preview does not store it.

## Sub-features

- `submit-form` shows the fields and the submit button.
- `submit-validate` refuses a bad URL in the browser.
- `submit-post` gets a JSON reply from the worker.

## How to get to it (user POV)

Choose Submit a tool in the header. The path is `/submit`.

## Driving it

`verify.py` checks status, head tags, and the style audit on `/submit`. `npm test` walks the form machine from idle through error and success without a browser. The skill does not post a submission.

## Gotchas

A live Kit call never happens from a submission, and the review queue is not part of this check.
