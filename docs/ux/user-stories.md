# Nurse AI Tools: end-to-end user stories

The yardstick for every story, from Shane (Oct 25, 2026): Nurse AI Tools exists to help nurses and nursing students surface, discover and use AI in their healthcare journey. A story passes only if the person finds the right AI for their situation and can start using it well, not just if the page renders.

Each story has steps, an expected outcome, and acceptance checks. Every check has an ID, like `SN-2.c`. The Playwright suite in `e2e/` uses the same IDs in its test titles, so `npx playwright test -g SN-2` runs one story. A check marked **open** fails today and is linked to its issue. The suite encodes it with `test.fail()`, so it reports as an expected failure until the fix lands, and then flags itself to be flipped.

Walked on Oct 25, 2026 at `e41961a` (main), local build, headless Chrome at 390 and 1280 wide, light and dark. Live (`https://nurseaitools.com`) was walked read-only. Live is an older deploy (78 tools; main has 79), so each finding says whether it is on main, live, or both.

## Personas

| Code | Who | Situation | What "found the right AI" means for them |
| --- | --- | --- | --- |
| SN | **Staff nurse**, med-surg nights, 6 years in | Saw a reply on X about ambient charting for nurses. Has 5 minutes on break, on a phone. | Knows within one screen whether a tool is built for nurses, what it says about HIPAA, and whether it fits bedside work. Knows what to ask the unit educator next. |
| NM | **Nurse manager**, 32-bed step-down unit | Was asked to look at AI for documentation burden and staffing. Searches on a laptop at a desk. | Can shortlist 2 or 3 tools for one problem, compare them, and trust where the facts came from well enough to bring them to informatics. |
| ST | **Nursing student**, last semester, NCLEX in 8 weeks | Searches "best AI NCLEX prep" on a phone. Budget matters. | Lands on a guide that compares AI NCLEX tools, finds a free option, and knows the one PHI rule before using any of them. |
| ED | **Nurse educator**, clinical instructor for a BSN program | Students keep asking which AI is allowed. Wants something to hand them. | Finds a page to link students to that sets safe-use rules and points at vetted study tools. Knows how the directory decides what it says. |

## Story map

| Story | SN | NM | ST | ED |
| --- | --- | --- | --- | --- |
| 1. Arrive from X (a link in a reply) | SN-1 | | | ED-1 |
| 2. Arrive from search (deep link) | | NM-1 | ST-1 | ED-2 |
| 3. Browse and filter the directory | SN-2 | NM-2 | ST-2 | |
| 4. Read a tool page | SN-3 | NM-3 | ST-3 | |
| 5. Decide whether to trust it | SN-4 | NM-4 | | ED-3 |
| 6. Sign up for the newsletter | SN-5 | | ST-4 | |

---

## Staff nurse

### SN-1. Arrive on a tool page from a reply on X

**Steps**

1. On a phone (390 wide), tap a link in an X reply: `https://nurseaitools.com/tools/abridge-for-nurses?utm_source=x&utm_medium=social`.
2. Read the first screen.

**Expected.** The page loads the tool, not a generic home. The first screen says what the tool is, who it is built for, and the HIPAA status. Tracking parameters do not create a different page.

**Acceptance checks**

- `SN-1.a` The URL with `utm_*` answers 200 and the canonical is the clean `https://nurseaitools.com/tools/<slug>`.
- `SN-1.b` The h1 is the tool name.
- `SN-1.c` The RN reality check (Built for, HIPAA status, Bedside fit) is on the page with three values.
- `SN-1.d` No sideways scroll at 390, in light and dark.
- `SN-1.e` A trailing-slash copy (`/tools/<slug>/`) leads to the clean URL. **Open ([#26](https://github.com/ShanesNotes/nurseaitools/issues/26)):** today it is a 200 copy, not a 301. See the SEO issue and the trailing-slash PR.

### SN-2. Find nurse-built tools for charting

**Steps**

1. From home, tap "Browse 79 tools".
2. Type `charting` in the search.
3. Clear it. Pick the category "Ambient documentation" and check "Built for nurses".
4. Open one tool, then press Back.

**Expected.** Search finds the ambient documentation tools when a nurse types the word a nurse would use. Filters narrow the list and the count says how many are shown. After Back, the list still matches the filters that were set.

**Acceptance checks**

- `SN-2.a` "Browse 79 tools" moves focus to the directory.
- `SN-2.b` Category plus trait narrows the rows and the count reads `<n> of 79 tools`.
- `SN-2.c` After opening a tool and pressing Back, the visible rows match the filters shown in the controls. **Open ([#13](https://github.com/ShanesNotes/nurseaitools/issues/13)):** the controls are restored but every row shows.
- `SN-2.d` Searching `charting` finds at least one ambient documentation tool. **Open ([#18](https://github.com/ShanesNotes/nurseaitools/issues/18)):** 0 results, because search reads only the name, vendor and description.

### SN-3. Read a tool page on a phone

**Steps**

1. Open `/tools/abridge-for-nurses` at 390 wide.
2. Scroll to the end.

**Expected.** The reality check, the official site, EHR integrations and the HIPAA line are readable. There is a way to see similar tools.

**Acceptance checks**

- `SN-3.a` The official site link matches `tools.json`, opens in a new tab, and has `rel` with `noopener`.
- `SN-3.b` The EHR and HIPAA / BAA rows are present.
- `SN-3.c` "Back to the directory" returns to the directory list, not the top of the hero. **Open ([#21](https://github.com/ShanesNotes/nurseaitools/issues/21)).**
- `SN-3.d` The page links at least one other tool in the same category. **Open ([#22](https://github.com/ShanesNotes/nurseaitools/issues/22)):** a tool page is a dead end.

### SN-4. Decide whether to trust the HIPAA line

**Steps**

1. On a tool with "Mentions HIPAA", read the reality check and the HIPAA / BAA row.
2. Look for when it was checked, by whom, and how.

**Expected.** The nurse can tell the claim is "the vendor's website mentions HIPAA", not "this is HIPAA compliant", and when it was checked.

**Acceptance checks**

- `SN-4.a` The HIPAA / BAA row says the BAA is not confirmed.
- `SN-4.b` The filter that selects these tools does not promise more than the data. **Open ([#14](https://github.com/ShanesNotes/nurseaitools/issues/14)):** it is labeled "HIPAA-ready", but the data only says the vendor website mentions HIPAA.
- `SN-4.c` Every tool page shows when the listing was checked, including one whose HIPAA status is Unknown (`/tools/abridge`). **Open ([#15](https://github.com/ShanesNotes/nurseaitools/issues/15)):** only the "Mentions HIPAA" line carries "(checked Oct 2026)". Tools with Unknown or "Not for patient info" show no date anywhere on the page.
- `SN-4.d` The tool page links to how listings work (`/about`). **Open ([#16](https://github.com/ShanesNotes/nurseaitools/issues/16)).**

### SN-5. Sign up for the weekly note from a tool page

**Steps**

1. At the end of a tool page, type an email and tap Subscribe.

**Expected.** A bad address is refused in the browser. A good one gets a plain confirmation. On live, the suite fills the field and stops before submitting.

**Acceptance checks**

- `SN-5.a` The form posts to `/api/subscribe`. A bad address shows "Please enter a valid email." and nothing is posted.
- `SN-5.b` Local only: a good address makes exactly one POST to the local worker and shows "You're subscribed. Thanks!".
- `SN-5.c` Live only: the field and button are present and the button is enabled. The suite never clicks it.

---

## Nurse manager

### NM-1. Arrive from search on a category need

**Steps**

1. At 1280 wide, arrive on home from a search for "AI nurse scheduling tools".

**Expected.** Within the first screen, or one scroll, the manager sees that the directory covers scheduling and staffing and how to get to it.

**Acceptance checks**

- `NM-1.a` Home has one h1, a meta description, and a self canonical.
- `NM-1.b` The category list includes "Scheduling & staffing".
- `NM-1.c` A deep link with a query, `/?q=scheduling`, opens with the search filled in and the list narrowed. **Open ([#20](https://github.com/ShanesNotes/nurseaitools/issues/20)):** the query is ignored. (Search Console already lists `?q=` copies, so someone shares these links.)

### NM-2. Shortlist tools for one problem

**Steps**

1. Pick "Scheduling & staffing". Then type `staffing scheduling` in the search.

**Expected.** Multi-word searches match tools that contain all the words, not only the exact phrase.

**Acceptance checks**

- `NM-2.a` The category filter shows exactly the rows `tools.json` has in that category.
- `NM-2.b` A two-word query matches rows containing both words in any order. **Open ([#19](https://github.com/ShanesNotes/nurseaitools/issues/19)):** search is an exact-phrase match, so `nclex free` finds 0.
- `NM-2.c` A nonsense query shows the empty state, and "Clear filters" brings every row back.

### NM-3. Compare two tools

**Steps**

1. Open two scheduling tools in turn.

**Expected.** The same fields in the same order on both, so the manager can compare them.

**Acceptance checks**

- `NM-3.a` Every tool page has the same five spec rows in the same order: Official site, EHR integrations, HIPAA / BAA status, Category, Vendor.

### NM-4. Check who is behind the directory

**Steps**

1. Follow the home "How listings work" link.

**Expected.** The page says who runs the site, how facts are gathered, what Unknown means, and that listings are independent.

**Acceptance checks**

- `NM-4.a` `/about` says who runs it, how listings work, and what Unknown means.
- `NM-4.b` The footer says the directory is independent and not medical advice on every page.

---

## Nursing student

### ST-1. Arrive on an NCLEX guide from search

**Steps**

1. On a phone in dark mode, open `/students/best-ai-nclex-prep` from a search result.

**Expected.** The guide compares AI NCLEX tools side by side, links each to its tool page, and keeps the PHI rule close.

**Acceptance checks**

- `ST-1.a` One visible h1 and a self canonical.
- `ST-1.b` Every `/tools/<slug>` link on the guide names a tool in `tools.json` and answers 200.
- `ST-1.c` The guide links the free NCLEX guide and back to the students hub.
- `ST-1.d` Text meets 4.5:1 contrast in dark mode (sampled on the lede and body).

### ST-2. Find a free NCLEX tool in the directory

**Steps**

1. From the students hub, open "Free NCLEX prep tools", then a tool.
2. On home, pick "Education / NCLEX".

**Expected.** Free options are easy to find from the hub. The category filter lists the education tools.

**Acceptance checks**

- `ST-2.a` The students hub links all seven guides.
- `ST-2.b` The free guide lists at least one tool with a free plan.
- `ST-2.c` The "Education / NCLEX" filter shows the same count as `tools.json`.

### ST-3. Read the safe-use rule before using a tool

**Steps**

1. Open an Education / NCLEX tool page.

**Expected.** The HIPAA line tells a student to never enter real patient information.

**Acceptance checks**

- `ST-3.a` The HIPAA / BAA row on a study tool says to never enter real patient information.
- `ST-3.b` The HIPAA status reads "Not for patient info".

### ST-4. Sign up from a guide on a phone

**Steps**

1. At the end of `/students/free-nclex-prep`, at 390 wide and dark, subscribe.

**Expected.** Same as SN-5, at phone size.

**Acceptance checks**

- `ST-4.a` The email field and Subscribe button are at least 44px tall.
- `ST-4.b` Local only: a good address shows the subscribed message.

---

## Nurse educator

### ED-1. Arrive on the students hub from X

**Steps**

1. Tap `https://nurseaitools.com/students?utm_source=x` at 1280 wide.

**Expected.** A page the educator can hand to students: what helps, where it goes wrong, and the PHI rule.

**Acceptance checks**

- `ED-1.a` The URL with `utm_*` answers 200 with the clean canonical.
- `ED-1.b` The hub shows the "One rule before any of these" PHI section.
- `ED-1.c` The hub says there are no star ratings and the facts are from vendor sites.

### ED-2. Arrive on the care plan guide from search

**Steps**

1. Open `/students/ai-care-plan-tools`.

**Expected.** It cites the research it summarizes and tells students to ask their instructor.

**Acceptance checks**

- `ED-2.a` The guide mentions the scoping review and tells students to ask the instructor whether AI drafts are allowed.

### ED-3. Find a page for educators

**Steps**

1. From home, look for an entry point for educators or managers.

**Expected.** There is a path for someone who chooses AI for other people, not only for themselves.

**Acceptance checks**

- `ED-3.a` The site nav has an entry for educators or leaders. **Open ([#11](https://github.com/ShanesNotes/nurseaitools/issues/11)):** only Students exists. See the persona entry points epic.

---

## Site-wide checks

These hold on every story's pages, and the suite runs them on each page it visits.

- `ALL.a` No request leaves the server under test. In local mode, the browser blocks and reports anything else.
- `ALL.b` No script errors.
- `ALL.c` Exactly one visible h1.
- `ALL.d` No sideways scroll at 390 or 1280.
- `ALL.e` Every button, field and select is at least 44px tall.
- `ALL.f` The 404 page answers 404, has no canonical, says noindex, and does not mark a nav item current. **Open ([#25](https://github.com/ShanesNotes/nurseaitools/issues/25))** until the 404 PR merges.
