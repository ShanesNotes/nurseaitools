# Students hub

The students hub is the long-form page for students and new grads. It links three guides and lists education tools.

## Sub-features

- `students-guides` links the three guides.
- `students-phi` states the patient-information rule.
- `students-list` lists education and study tools with a reality check.

## How to get to it (user POV)

Choose Students in the header, or the students door on home. The path is `/students`.

## Driving it with the preview

Preconditions:

- The preview is up.

- **Record.** Run `python3 shoot.py`. `shots/students-desktop.png` and `shots/students-mobile.png` show the hub. scrollWidth is `ok`.

## Gotchas

The three guide pages are not separate screenshots. `test_style.py` checks that those paths exist.
