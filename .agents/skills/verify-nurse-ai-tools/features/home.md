# Home directory

The home page is the directory. A nurse reads the title, then searches and filters the list of every tool.

## Sub-features

- `home-read` shows the title and the tool count from the build.
- `home-search` narrows the list as the query is typed.
- `home-filter` narrows the list by category.
- `home-empty` shows the empty state when nothing matches, and Clear restores the list.

## How to get to it (user POV)

Open `/`, or choose Directory in the header.

## Driving it

`verify.py` checks that the count reads `<N> tools` and that there are N rows, where N is the length of `tools.json`. It types `abridge` and expects exactly the rows whose name, vendor, or description contain it. It picks the tool page's category and expects the same row count as `tools.json`. It types a nonsense query, expects the empty state, then clicks Clear and expects N rows again.

`drive_home.py` is the small manual version of the search drive, for a preview you started yourself.

## Gotchas

The search runs in the browser. Reloading the page clears it. There is no server round trip.
