# Tool page

A tool page is one listing. The reality check is the part a nurse came to read.

## Sub-features

- `tool-facts` shows the name, vendor, reality check, and the long HIPAA line.
- `tool-source` links to the vendor site.

## How to get to it (user POV)

Open a tool from the directory, or go to `/tools/abridge-for-nurses`.

## Driving it with the preview

Preconditions:

- The preview is up.

- **Record.** Run `python3 shoot.py`. `shots/tool-desktop.png` and `shots/tool-mobile.png` show Abridge for Nurses. scrollWidth is `ok`.
- **Facts.** `python3 test_style.py` fails if a tool page drops a fact field.

## Gotchas

`shoot.py` always opens Abridge for Nurses. Other tools are checked as HTML by `test_style.py`, not as screenshots.
