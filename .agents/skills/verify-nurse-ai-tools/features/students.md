# Students hub

The students hub is the long-form page for students and new grads. It links the student guides, including the four NCLEX guides in `students-nclex.md`, and lists education tools.

## Sub-features

- `students-guides` links every student guide.
- `students-phi` states the patient-information rule.
- `students-list` lists education and study tools with a reality check.

## How to get to it (user POV)

Choose Students in the header. The path is `/students`.

## Driving it

`verify.py` checks `/students` and each guide in the sitemap for status 200 and head tags. In Chrome it checks the hub for one visible `h1`, tool links that name slugs in `tools.json`, every on-site link answering 200, links to all four NCLEX guides, the newsletter form, and no script errors. It runs the style audit on `/students` at both widths in both schemes.

## Gotchas

The three older guides (`best-free-ai`, `ai-care-plan-tools`, `nclex-ai-tutors`) get HTTP checks only. The four NCLEX guides get browser drives.
