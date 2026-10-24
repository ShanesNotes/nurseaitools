# Students hub

The students hub is the long-form page for students and new grads. It links three guides and lists education tools.

## Sub-features

- `students-guides` links the three guides.
- `students-phi` states the patient-information rule.
- `students-list` lists education and study tools with a reality check.

## How to get to it (user POV)

Choose Students in the header. The path is `/students`.

## Driving it

`verify.py` checks `/students` and each guide in the sitemap for status 200 and head tags, and runs the style audit on `/students` at both widths.

## Gotchas

The guide pages get HTTP checks only, not browser drives.
