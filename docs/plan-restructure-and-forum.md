# Plan: site restructure, design system, and forum

Status: DRAFT v0.2 (forum revised to Shane's open, free-speech direction), Thu Oct 22 2026. For Shane to iterate with pstack today; Opus agents build tomorrow.
Nothing in this doc has been built, deployed or posted. Live is still version 10 (b494ac4c), rollback version 9 (6707778b).

How to use this doc: each section ends with "Decide" bullets. Edit those in place during the pstack pass. Section 6 is the build list; every unit there is meant to go to one agent.

---

## 0. Brand thesis (draft, needs Shane's OK)

**AI should run the rules in the background so nurses can run the care.**

Pillars (from call-log-2026-10-22.md part 2; paraphrase, not quotes):

| Key | Pillar | Short form |
| --- | --- | --- |
| `background` | Compliance runs in the background. Evidence-backed rules (Joint Commission, CMS, cadences) are encoded in the documentation, not checkbox theater. | Rules in the background |
| `informs` | AI informs, humans decide. No hard stops in documentation (sepsis alerts are the example). | No hard stops |
| `workarounds` | Count workarounds removed, not minutes saved. Quality of care shows up in outcomes over time. | Workarounds, not minutes |
| `builder` | Bedside-to-builder. Frontline nurses translate workflows into plain English for engineers. | Bedside to builder |
| `privacy` | Privacy without identifiers. Clinical LLM use doesn't always need patient identifiers; distrust is about who owns the model. | No identifiers needed |
| `digging` | Students: grade the digging, not the paper. Frontier models are the backhoe. | Use the backhoe |
| `oracle` | North star: the night-shift oracle (continuous vitals + full H&P, notes, labs in one context). | The night-shift oracle |

Rule: the site quotes Shane only from shane-takes.md verbatim entries. Paraphrased pillars appear as "we believe" copy, never in quotation marks.

---

## 1. Current site (inspected from code, commit 926e820)

Source of truth: `build.py` renders every page into a JSON map `PAGES` that `worker.template.js` serves. There is no runtime templating; every page is static HTML baked into the worker.

### 1.1 Routes

| Path | Built at | What it holds |
| --- | --- | --- |
| `/` | build.py `home` | H1 "AI tools for nurses, reviewed by a nurse", lede, tool count, then the full directory: search box, category select, two trait checkboxes ("Built for nurses", "HIPAA-ready"), one sheet with 74 rows (tool, what it does, RN reality check: Built for / HIPAA status / Bedside fit), then the newsletter panel |
| `/tools/<slug>` (74) | build.py loop | Back link, h1, vendor, RN reality check panel, spec list (what it does, category, vendor, site, EHR, HIPAA/BAA), corrections line, newsletter panel |
| `/students` | `stu()` | Hub: deck, "no star ratings" rule, 3 guide links, the PHI rule panel, picks of Education / NCLEX + Study & care plans tools |
| `/students/best-free-ai` | `stu()` | Guide + picks (NotebookLM, Knowt, NurseSavvy, ChatGPT, Claude, Gemini, Quizlet, StudyFetch, OpenEvidence) |
| `/students/ai-care-plan-tools` | `stu()` | Research summary + how-to + picks |
| `/students/nclex-ai-tutors` | `stu()` | What to compare + picks (GoodNurse, NCLEXIT, NurseSavvy, UWorld, Archer, Kaplan, SimpleNursing, Lecturio) + future-commission disclosure |
| `/submit` | build.py `sub` | Tool submission form -> `POST /api/submit` |
| `/about` | build.py `ab` | Curator (RN, 14 years critical care), how listings work |
| 404 | `NOT_FOUND` | "Page not found" |
| `POST /api/subscribe` | web/contract.js | D1 `subscribers` insert, then Kit (`KIT_API_KEY`, `KIT_TAG_ID`) via `ctx.waitUntil` |
| `POST /api/submit` | web/contract.js | D1 `submissions` insert |
| `/js/*.js` | `SCRIPTS` | web/fsm.js, catalog.js, form.js, contract.js, page.js |
| `/sitemap.xml`, `/robots.txt`, `/22108e5ac38312c5b3b7a578b9d42a4b.txt` (IndexNow key), `www` -> apex 301 | worker | Kept by test/routes.test.js |

Total: 81 pages. Nav: Directory, Students, Submit a tool, About. Footer: independence + "Not medical advice. Always follow your facility's policies."

### 1.2 Data

- `tools.py`: 74 tools (the "71" figure is stale), 8 categories: Ambient documentation 15, Education / NCLEX 13, Patient communication 11, Clinical decision support 9, Scheduling & staffing 8, Handoff & summaries 6, General LLMs 6, Study & care plans 6.
- `reality.py`: `R[name] = (built_for, bedside_fit)`. HIPAA status is computed in build.py from vendor-site evidence. Value sets are fixed by PRODUCT.md (Built for: Nurses/Physicians/Both/General/Unknown; HIPAA: Mentions HIPAA/Not for patient info/Unknown; Bedside fit: Bedside/mobile, Desk or charting only, Education only, Unknown).
- `schema.sql`: `subscribers`, `submissions`. D1 binding `DB`, database `nurseaitools` (76c61476-...).

### 1.3 Build and deploy constraints the plan must respect

- `deploy.js` is the connector path: one module, no bundler. build.py inlines `web/contract.js`. **Any new server module (forum, auth) must also be inlined by build.py**, or the connector deploy breaks.
- Deploys go through the Cloudflare connector with `/workspace/deploy-fn.txt` and `keep_bindings`, regenerated after each build so the Kit secrets survive. New bindings (secrets for email, Turnstile) must be added the same way.
- `dist/` is missing in the working tree (git shows `D dist/worker.js`), so `python3 build.py` fails with FileNotFoundError until `mkdir -p dist`. Unit B0 fixes this.
- Tests: `npm test` = 39 node tests, all passing today. `python3 test_style.py` checks DESIGN.md rules (tokens on :root only, contrast, banned words, no em dashes, 44px targets, 390px layout).
- Copy rules (DESIGN.md / PRODUCT.md): no emoji, no em dashes or curly quotes, banned word list, "Unknown" when unverified, never invent tool facts, nothing is medical advice.

### 1.4 What's weak today

1. The home page is a directory with no point of view. Nothing says what we believe.
2. The reality check answers "is this for nurses / HIPAA / bedside", but not the three questions from the call: does it remove workarounds, does it inform or act (hard stops), does it need identifiers.
3. Students are the core audience but sit one click deep, with three guides and no framework.
4. The newsletter is a footer panel on every page with no promise of what's in it.
5. There's nowhere for nurses to talk, so no return visits and no way to collect frontline insight (the bedside-to-builder moat).

---

## 2. Proposed information architecture

### 2.1 New site map

```
/                          Home: thesis, 3 doors (Students, Directory, Discuss), latest take, newsletter
/believe                   What we believe: the 7 pillars, one short block each
/tools                     Directory (moved from /), adds the lens filters
/tools/<slug>              Tool page, adds the lens panel
/students                  Students hub, leads with the backhoe guide
/students/backhoe          "Use the backhoe": how to use AI to get better, not to cheat
/students/nclex            NCLEX tools (rename of nclex-ai-tutors; 301 old path)
/students/best-free-ai     kept
/students/ai-care-plan-tools kept
/newsletter                What the note is, issue archive, signup
/newsletter/<n>            Issue pages (optional, phase 2)
/discuss                   Forum (section 4)
/submit                    kept
/about                     kept, links to /believe
```

Nav (5 items, fits 390px in two lines max): Students, Tools, Discuss, Newsletter, About. "Submit a tool" moves into Tools and the footer.

Redirects: `/students/nclex-ai-tutors` -> `/students/nclex` (301). `/` keeps a short directory teaser and a search box that submits to `/tools?q=`, so existing search habits survive. All `/tools/<slug>` URLs are unchanged (SEO).

### 2.2 Ideas ranked (impact vs effort)

| # | Idea | Impact | Effort | Why |
| --- | --- | --- | --- | --- |
| 1 | **Home led by the thesis**: one-line POV, three doors, latest verbatim take, newsletter. Directory moves to `/tools`. | High | S | Turns a list into a brand. Mandate from Shane: "part of the solution", not a trend echo. |
| 2 | **Reality-check lens** (3 new fields per tool): Removes workarounds? / Informs or acts? / Needs identifiers? Plus filters. | High | M | Our moat. A neighbor can't copy it without the judgment. Starts with ambient + decision support rows (24 tools). |
| 3 | **Students hub led by "Use the backhoe"** guide; NCLEX tools page with affiliate-ready slots (Lecturio, SimpleNursing, Archer, UWorld). | High | M | Core audience and the money path. Guide doubles as the newsletter lead magnet. |
| 4 | **Design system swap to the real Market site system** (section 3). | Med-High | M | Shane's call; also fixes credibility for long reading. |
| 5 | **"What we believe" page** (`/believe`). | Med | S | Anchors every post, the newsletter and forum categories. Paraphrase copy, Shane approves. |
| 6 | **Newsletter page** with a clear promise: one take, one tool through the lens, one student tip. | Med | S | Gives the signup a reason. Kit wiring stays as is. |
| 7 | **Forum** (`/discuss`), open free-speech forum. | High (long term) | L | Community, return visits, frontline insight. Main risks: cold start and spam. |
| 8 | Recurring "tool that doesn't exist yet" page (night-shift oracle) tracking tools that get close. | Low-Med | S | Fun, linkable, feeds X. Phase 2. |

### 2.3 Lens field definitions (for reality.py)

Add a second dict `L[name] = (workarounds, acts, identifiers)` so existing `R` tuples and tests don't change.

| Field | Values | Rule |
| --- | --- | --- |
| Removes workarounds | `Removes a workaround` / `Moves the clicks` / `Unknown` | Only "Removes" when the vendor names a specific task the nurse stops doing (e.g. re-keying vitals into a flowsheet). Default Unknown. |
| Informs or acts | `Informs` / `Acts with review` / `Hard stop` / `Unknown` | "Hard stop" only when the vendor describes blocking or interruptive alerts. |
| Needs identifiers | `No patient info` / `De-identified` / `Needs PHI (BAA)` / `Unknown` | Education and general study tools are `No patient info` by rule. |

Same discipline as today: from vendor or public info only; Unknown when unverified. Accent jobs: `Hard stop` and `Needs PHI` get the red edge (caution), `Informs` gets nothing (plain fact), Unknown stays dashed.

Decide:
- Is the directory at `/tools` with a teaser on `/`, or does `/` keep the full directory below the thesis?
- Lens value wording (above) OK?

---

## 3. Design system: the Market site, curated for nurses

Shane wants the redesign to follow the design system in `ShanesNotes/market` (the marketforever.dev landing page). Read read-only at commit 64b7d28.

Files drawn from:
- `site/style.css` (tokens on `:root`, Levkas light + Carbon dark, all components)
- `docs/site/voice-and-design.md` (palette with measured contrast, type, spacing, look rules, voice)
- `docs/site/information-architecture.md` (nav and page pattern)
- `site/index.html` (landing structure: halftone, announce window, hero, thesis blocks)
- `site/tests/test_style.py` (how the system is enforced)
- `site/fonts/*.woff2` + OFL texts (faces)
- Not used: root `DESIGN.md` and `.impeccable/design.json`, which describe the in-game addon UI (WoW client frame, Friz Quadrata), not the website.

### 3.1 Important finding

Our live `DESIGN.md` says "marketforever.dev system", but what we shipped (commit b24afad) is a different reading of it: dark-only, system monospace, no webfonts, accents as edges, a 4px RGBY stripe. The actual Market site is **light-first (Levkas) with a dark theme (Carbon) on `prefers-color-scheme`**, three self-hosted faces, square 1px ink frames with **hard offset shadows**, and one main accent (cinnabar). So this is a real redesign, not a tweak.

### 3.2 Token mapping

| Market token (`site/style.css`) | Levkas / Carbon | Nurse AI Tools role |
| --- | --- | --- |
| `--paper` | `#f8f7f4` / `#121211` | Page ground |
| `--leaf` | `#ffffff` / `#1b1b1a` | Sheets: directory index, reality-check panel, forum thread card, newsletter panel |
| `--sunk` | `#efede7` / `#232321` | Table head, window bar, code, forum reply indent rail |
| `--hover` | `#f0eee8` / `#262523` | Hovered row |
| `--ink` | `#1e1e1e` / `#f4f4f0` | Text and every 1px frame (`--rule`) |
| `--soft` | `#4f4d47` / `#b4b2aa` | Secondary text, labels |
| `--pencil` | `#64625b` / `#97958d` | Unknown values, timestamps, "not verified" (Market's "what we did not see" maps exactly to our Unknown rule) |
| `--rule-soft` | `#dedede` / `#3a3a37` | Decorative hairlines only |
| `--cinnabar` / `--cinnabar-ink` | `#c8401f` `#a8321a` / `#e2603f` `#f08266` | **Red**: the PHI rule, invalid fields, `Hard stop` / `Needs PHI` lens edges, thesis labels. Never losses-style alarm copy. |
| `--lapis` / `--lapis-ink` | `#2b4c9b` / `#93acec` | **Blue**: links, the focus ring, the RN reality check rule |
| `--verde` / `--verde-ink` | `#5f8467` `#3b6248` / `#7fa587` `#9cc2a4` | **Green**: "Mentions HIPAA", `No patient info`, `Removes a workaround` |
| `--gold` / `--gold-ink` | `#c9a13b` `#7d5d10` / `#d9b65a` `#e1c27a` | **Yellow**: fill only (gold is 2.3:1 on paper), the stripe, the RN badge fill later, pinned-thread mark |
| `--shadow-hard` / `--shadow-window` | 2px / 3px offset, no blur | Buttons; the one featured panel per page |
| `--space-1..9` | 4 8 12 16 24 32 48 64 96 | Replaces our `--space-2..7` (4..32). Sections 64px apart. |
| `--text-*` | 10 12 15 18 22 28 36 64 128 | See 3.4 for the clinical subset |
| `--measure` 68ch, `--wrap` 1200px | | Same |
| `--radius-0`, `--radius-hair` | 0 / 2px | Same as ours |

Keep the sparse four accents, each with one job, and keep the "words, then edge style, then hue" triple encoding from our DESIGN.md so meaning never rides on color alone.

### 3.3 Component mapping

| Market component (style.css selector) | Use on Nurse AI Tools |
| --- | --- |
| `.cover-bar` / `.bar` / `.wordmark` (Host Grotesk 500 28px) | Masthead. Nav from 2.1. |
| `.halftone` + `.announce` window | Home only, once. Calm version: lapis or soft-ink dots at lower density instead of cinnabar, or drop it (Decide). Announce window holds the latest take or newsletter line. |
| `.hero` / `.hero-title` / `.eyebrow` | Home thesis. Eyebrow: "Students · Tools · Discuss". Hero size capped lower (see 3.4). |
| `.thesis` (rubric label left, body right) | `/believe` pillars, one block each; home's three doors; tool page sections. |
| `.steps` (numbered 01, 02) | "Use the backhoe" guide. |
| `.window-bar` | Directory sheet head ("RN reality check"), forum thread header (category, age, replies). |
| `.button` / `.button.red` (ink fill primary) | Subscribe, Post, Reply. Keep hard shadow; drop the hover translate for calm (see 3.4). |
| `.seg` segmented control | Forum sort (Top / New / Unanswered); directory lens toggles. |
| `.badge` (1px currentColor, uppercase 12px) | Category chips, self-reported `RN` badge later, `Seed`, `Shane`. |
| `.stats` dl, `.group-label` | Reality-check panel and lens panel on tool pages. |
| `.tabs` | Students hub (Guides / NCLEX tools / Free tools). |
| `.release` details card | Newsletter issue archive; forum seed-thread cards. |
| `.site-foot` | Footer (existing text unchanged). |
| Voice rule "humor only on bad moments" | Allowed on 404 and error lines, never on clinical copy, never about patients. |

### 3.4 Adapt for a clinical audience

- **Readability.** Market sets body copy in Fragment Mono 18px. Long guides and forum threads in mono tire readers. Use Host Grotesk 400 for prose (guides, `/believe`, forum bodies, at 18px / 1.5), Fragment Mono for controls, labels and table rows, JetBrains Mono for figures and column heads. Keep ligatures off and tabular slashed-zero numbers.
- **Size floor.** Nothing under 12px; the 10px token is for decorative marks only. Body 18px, forum and table rows 15px minimum. Hero clamp capped at 64px (not 128px). This is a reference site, not a launch page.
- **Contrast.** Keep Market's 4.7:1 floor (already above AA's 4.5) on paper, leaf, sunk and hover in both themes, recomputed by test_style.py.
- **Light first, dark for nights.** Levkas leads; Carbon follows `prefers-color-scheme`. A night-shift nurse on a dark phone gets Carbon automatically. Optional manual toggle later.
- **Calm tone.** No hover jump (`transform`) on buttons: keep the shadow, drop the motion. One halftone at most, muted. Red reserved for real caution (PHI, hard stops, invalid input), never decoration or urgency. No countdowns, no badges for "hot".
- **Targets.** Keep our 44px minimum (Market uses 36 to 40). Gloved hands, phones, small screens.
- **Fonts weight.** Six woff2 files total about 110 KB. Serve them from the worker under `/fonts/*` with long cache headers, and include the OFL texts. This reverses our Oct "drop webfonts" decision, so it's listed in Open questions.
- **Unknown = pencil.** Market's rule "grey with its reason for what it did not see" fits exactly: every Unknown in the reality check is pencil plus a reason ("not on vendor site, Oct 2026").
- **Voice.** Market's "plain, short, dry; say what it is and stop" fits. Keep our banned word list and add Market's; no em dashes.

Decide:
- Halftone on home: muted lapis, muted cinnabar, or none?
- Grotesk for prose (recommended) or all-mono like Market?

---

## 4. Forum (`/discuss`)

Direction from Shane (Oct 22): an open, free-speech forum. We are not building Reddit's governance structure. No reporting, no moderators, no mod queue or action log, no posting rules enforced by people, no gated launch. The only automated protection is plain anti-spam and bot protection (Turnstile + rate limits). The patient-info check is a browser nudge only.

### 4.1 Build vs off-the-shelf (honest)

| Option | Cost | Pros | Cons | Fit |
| --- | --- | --- | --- | --- |
| **Build on Workers + D1** | $0 on current plan at our scale | Same domain (SEO), same design, open by default with no imposed governance, owns the data, ties into directory and newsletter, categories = pillars | We own auth, spam protection and bugs. L effort. | **Recommended** |
| Flarum (self-host) | Hosting cost | Free software, nice UI | PHP + MySQL, not Cloudflare-native; a server to patch; ships moderation-centric defaults | No |
| Subreddit | Free | Zero build, Reddit discovery | Reddit's content policy and governance are exactly what we're not doing; not our domain or data | No (maybe a feeder link later) |
| Discord | Free | Real-time, students like it | Chat not threads, not indexed by search, platform rules apply | No |

Recommendation: build a small Reddit-style forum on the existing Worker + D1, open to anyone with an account from day one, seeded with threads at launch.

### 4.2 Auth: options and pick

| Option | Notes | Verdict |
| --- | --- | --- |
| **Magic link email + D1 sessions** | Email a one-time link (token hashed in D1, 15 min TTL, single use). On click, set an httpOnly, Secure, SameSite=Lax session cookie backed by a `sessions` row (30-day sliding). Hand-rolled "Lucia-style" sessions (Lucia the library is deprecated; its session pattern is the guide). No passwords to store. | **Pick** |
| Email sender: Cloudflare Email Sending vs Resend | Workers' `send_email` binding historically only reaches verified addresses; check whether Cloudflare's newer Email Sending service is enabled on this account. Resend has a free tier (about 100/day at the time of writing) and a simple fetch API. | Try Cloudflare first; Resend free as fallback. A new vendor signup needs Shane's OK even at $0. |
| Passkeys (WebAuthn) | Best UX and security, but adds a library and edge cases on shared hospital computers. | Phase 2 add-on to an account that already exists via magic link |
| Supabase Auth | Solid, but a second backend and data store outside Cloudflare, plus another vendor. | No |
| Google/Apple OAuth | Easy for students; extra consent screens and app registration. | Phase 2 maybe |

Usernames: handle only, no real names required. A friendly tip on signup: "You don't need your real name or your hospital's name here."

### 4.3 Features

**MVP (launch, open)**
- Accounts: magic link sign-in, handle, optional bio; sign out; delete own account (posts show "[deleted]").
- Threads: title (max 140), body (Markdown subset, max 10k chars, no images in MVP, links `rel=nofollow ugc`), category (required), optional tool tag (links a `/tools/<slug>`).
- Replies: nested to depth 4 (then "continue thread"), stored as adjacency list with a materialized `path` for ordering.
- Voting: up votes on threads and replies. One vote per user per item; score cached on the row. Votes only rank; they never hide anything.
- Sort: Top (score with time decay), New, Unanswered.
- Categories = pillars + audience: `Students & new grads`, `NCLEX`, `Rules in the background`, `No hard stops`, `Workarounds, not minutes`, `Bedside to builder`, `Privacy & identifiers`, `Tool talk`, `The night-shift oracle`, `Open floor`.
- Authors can edit (within 24h) and delete their own posts. Nobody else can.
- Patient-info nudge (4.7), Turnstile + rate limits (4.6).
- Seed threads at launch (4.8).
- Email: magic links only. No notification emails in MVP.

**Phase 2**
- Reply notifications (opt-in, daily digest), passkeys, saved threads, search (D1 FTS5).
- Optional self-described badge (`RN`, `NP`, `Student`), labeled self-reported. License verification only if Shane wants it later.
- Down votes or "helpful" reactions (ranking only).
- Weekly "best of /discuss" block in the newsletter; X posts quoting threads only with the author's permission.
- "Bedside to builder" structured post template (workflow, pain point, what the tool should do).

### 4.4 D1 schema (MVP)

File `migrations/0002_forum.sql`. Existing `subscribers` and `submissions` are untouched.

```sql
CREATE TABLE users(
  id INTEGER PRIMARY KEY,
  email TEXT UNIQUE NOT NULL COLLATE NOCASE,
  handle TEXT UNIQUE NOT NULL COLLATE NOCASE CHECK(length(handle) BETWEEN 3 AND 24),
  bio TEXT CHECK(bio IS NULL OR length(bio) <= 280),
  badge TEXT CHECK(badge IN ('RN','NP','Student')),  -- self-reported, phase 2
  deleted_at TEXT,
  created_at TEXT NOT NULL
);
CREATE TABLE login_tokens(
  token_hash TEXT PRIMARY KEY,           -- SHA-256 of the emailed token
  email TEXT NOT NULL COLLATE NOCASE,
  expires_at TEXT NOT NULL,
  used_at TEXT,
  ip_hash TEXT
);
CREATE TABLE sessions(
  id_hash TEXT PRIMARY KEY,              -- SHA-256 of the cookie value
  user_id INTEGER NOT NULL REFERENCES users(id),
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE TABLE categories(
  slug TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  pillar TEXT,                           -- background|informs|workarounds|builder|privacy|digging|oracle|NULL
  description TEXT NOT NULL,
  sort INTEGER NOT NULL
);
CREATE TABLE threads(
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  category TEXT NOT NULL REFERENCES categories(slug),
  tool_slug TEXT,                        -- optional link to /tools/<slug>
  title TEXT NOT NULL CHECK(length(title) BETWEEN 8 AND 140),
  body TEXT NOT NULL CHECK(length(body) <= 10000),
  score INTEGER NOT NULL DEFAULT 0,
  reply_count INTEGER NOT NULL DEFAULT 0,
  seed INTEGER NOT NULL DEFAULT 0,       -- seeded at launch
  deleted_at TEXT,                       -- author's own delete only
  created_at TEXT NOT NULL,
  last_activity_at TEXT NOT NULL,
  edited_at TEXT
);
CREATE INDEX threads_cat_activity ON threads(category, last_activity_at DESC);
CREATE INDEX threads_score ON threads(score DESC);
CREATE TABLE replies(
  id INTEGER PRIMARY KEY,
  thread_id INTEGER NOT NULL REFERENCES threads(id),
  parent_id INTEGER REFERENCES replies(id),
  user_id INTEGER NOT NULL REFERENCES users(id),
  depth INTEGER NOT NULL CHECK(depth BETWEEN 0 AND 4),
  path TEXT NOT NULL,                    -- zero-padded ids joined by '/', for ordered tree reads
  body TEXT NOT NULL CHECK(length(body) <= 10000),
  score INTEGER NOT NULL DEFAULT 0,
  deleted_at TEXT,                       -- author's own delete only
  created_at TEXT NOT NULL,
  edited_at TEXT
);
CREATE INDEX replies_thread_path ON replies(thread_id, path);
CREATE TABLE votes(
  user_id INTEGER NOT NULL REFERENCES users(id),
  target_type TEXT NOT NULL CHECK(target_type IN ('thread','reply')),
  target_id INTEGER NOT NULL,
  value INTEGER NOT NULL CHECK(value = 1),
  created_at TEXT NOT NULL,
  PRIMARY KEY(user_id, target_type, target_id)
);
CREATE TABLE rate_events(
  key TEXT NOT NULL,                     -- e.g. 'post:u:12', 'login:ip:<hash>'
  at INTEGER NOT NULL                    -- epoch seconds
);
CREATE INDEX rate_events_key_at ON rate_events(key, at);
```

Privacy: store IPs only as salted hashes (salt in a secret), never raw, and only for rate limiting. Emails are never shown. Prune `rate_events` older than 1 day and used/expired `login_tokens` on write or in a cron trigger. The patient-info nudge stores nothing.

### 4.5 Routes

HTML pages are server-rendered by the worker at request time (forum pages can't be baked into `PAGES`), using the same `page()` shell exported from build.py as a template string.

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| GET | `/discuss` | public | Index: categories, sort `?sort=top|new|unanswered`, `?page=` |
| GET | `/discuss/c/<category>` | public | Category listing |
| GET | `/discuss/t/<id>/<slug>` | public | Thread + reply tree |
| GET | `/discuss/new` | member | New thread form |
| GET | `/login` | public | Email form (Turnstile) |
| POST | `/api/auth/request` | public | Send magic link. Always replies "Check your email" (no account enumeration) |
| GET | `/auth/verify?t=` | public | Consume token, create user if new (then `/welcome` to pick handle), set session cookie |
| POST | `/api/auth/logout` | member | Delete session |
| POST | `/api/forum/threads` | member | Create thread (Turnstile, rate limit) |
| POST | `/api/forum/replies` | member | Create reply (rate limit) |
| POST | `/api/forum/vote` | member | Toggle vote |
| POST | `/api/forum/edit` | author | Edit own post within 24h |
| POST | `/api/forum/delete` | author | Soft delete own post |
| POST | `/api/account/delete` | member | Delete own account |
| GET | `/u/<handle>` | public | Profile: handle, badge, posts |

CSRF: all POSTs require same-origin `Origin` header plus SameSite=Lax cookie. Forms work without JS (progressive enhancement), matching today's form machine pattern in `web/form.js`.

Caching: public GETs `cache-control: public, max-age=30` for signed-out users; `private, no-store` when a session cookie is present.

SEO: thread pages are indexable; `/discuss/t/*` added to a dynamic sitemap section. Author-deleted items return 410.

### 4.6 Anti-spam and bot protection (not moderation)

These stop bots and floods. They don't judge content.
- Turnstile (free) on `/login`, new thread, and the first 5 replies of a new account. Server verifies via `siteverify` with `TURNSTILE_SECRET` (new secret; add to deploy-fn.txt keep_bindings like the Kit secrets).
- D1-backed sliding window (`rate_events`), or the Workers Rate Limiting binding if available on the plan:
  - Magic link: 3 per email per 15 min, 10 per IP hash per hour.
  - Threads: 3 per user per day for accounts under 7 days old, 10 per day after.
  - Replies: 20 per user per hour.
  - Votes: 200 per user per hour.
- Link limit: max 3 links per post (a spam-bot pattern, not a content rule).
- Honeypot field kept (same as the current forms).
- Over a limit -> HTTP 429 with a plain "Slow down a little, try again in N minutes." Nothing is held or queued.

### 4.7 Patient-info nudge (browser only, non-blocking)

- `web/phi.js`: a pure function that runs in the browser on the compose box (and is unit-tested). It looks for likely patient identifiers: MRN-like numbers (6 to 10 digits), SSN pattern, phone numbers, emails, full dates and DOB phrases, "Mr./Mrs./Ms. Name", "pt name", "room/rm/bed <n>", ages 90+, street addresses.
- When it matches, it shows a short inline note under the compose box, e.g. "Heads up: this might include a patient detail (room 412). You may want to change it before posting." The Post button stays enabled. One click posts as written.
- The server never runs it, never holds, rejects, flags or stores anything from it. There is no review queue. Disabled JS = no nudge, post works normally.
- Uses the red accent edge on the note (our PHI rule color), calm wording, no modal.

### 4.8 Cold start (seed threads)

1. Launch open with 8 to 12 seed threads, one per pillar plus 3 student threads (from call-prep-2026-10-22.md themes 1 to 6 and the closers: "What's a legit way for a student to use ChatGPT?", "What tool doesn't exist yet that you'd want on a night shift?", "What can't the NCLEX teach that you learned your first ICU year?"). Opening posts use Shane's verbatim takes where they exist, labeled as his; otherwise they're posted as the question.
2. Invite people in (not gate them): newsletter subscribers, people who reply to @nurseaitools, nursing student contacts Shane names.
3. Weekly prompt: the Saturday riff prompt becomes a new thread each week; Shane's reply is the first comment.
4. Cross-link: every tool page gets "Discuss this tool" (threads tagged with `tool_slug`).

### 4.9 Pages needed at launch

`/privacy` (what we store: email, handle, salted IP hash for rate limits; how to delete your account) and a short `/terms` (you own what you post and grant us a license to display it; open forum). Drafted by us, reviewed by Shane. The existing site footer stays as it is today.

---

## 5. Newsletter

- `/newsletter` page: promise ("One take from a critical care RN, one tool through the reality check, one student tip. Weekly."), signup, archive placeholder.
- Same `POST /api/subscribe` and Kit wiring; add an optional hidden `source` field (home, students-backhoe, forum-beta) mapped to Kit tags later. Contract change is backward compatible.
- Stays held until real subscribers, as today.

---

## 6. Build units for tomorrow (one Opus agent each)

Rules for every unit: work on a branch `build/<unit>`, never deploy, never touch `deploy-fn.txt` or secrets, keep all 39 existing tests green, add tests, run `python3 build.py && npm test && npm run check && python3 test_style.py`, open a PR or leave the branch for review. No copy in quotation marks attributed to Shane unless copied from shane-takes.md.

Dependency order: B0 -> (B1, B2, B3 in parallel) -> (B4, B5, B6) -> F1 -> F2 -> F3 -> (F4, F5). Forum units can start in parallel with B4 to B6 once B0 lands.

### B0. Build hygiene (small, first)
- `mkdir -p dist` in build.py; make `test_style.py` and `npm test` runnable from a clean clone; split build.py page bodies into a `pages/` module only if needed for later units (optional).
- Accept: clean clone builds with "74 tools 81 pages"; all tests pass; no output diff in `dist/worker.js` vs current except the dist fix.

### B1. Design system swap (from section 3)
- Replace `:root` tokens with Levkas + Carbon (section 3.2), add `/fonts/*` route serving the six woff2 files and OFL texts (base64-embedded so deploy.js still works), Host Grotesk for prose, Fragment Mono for controls, JetBrains Mono for figures. Port components from 3.3: bar, wordmark, button (hard shadow, no translate), thesis block, steps, window-bar, seg, badge, eyebrow. Accent jobs per 3.2. Update DESIGN.md to the new system and cite `ShanesNotes/market site/style.css` and `docs/site/voice-and-design.md`.
- Tests: rewrite test_style.py checks to the new rules: tokens only on `:root`; every text ink clears 4.7:1 on paper/leaf/sunk/hover in BOTH themes; accents never used as text except `-ink` variants; no text under 12px except decorative; 44px targets; no sideways scroll at 390px (shoot.py screenshot at 390 and 1280, both themes); banned words; no em dashes; no `transform` on hover; fonts served with `content-type: font/woff2` and immutable cache.
- Accept: screenshots for home, a tool page, students hub in light and dark; all checks green; data-* hooks unchanged so web/*.js tests pass untouched.

### B2. Lens data (reality.py + build.py)
- Add `L` dict and the three fields (2.3) for the 15 ambient + 9 decision support + 6 handoff tools first; everything else `Unknown`/rule-based. Each non-Unknown value gets a one-line evidence note and source URL in a new `LENS_NOTES`. Show a "Reality check lens" panel on tool pages; add filter checkboxes "Removes a workaround", "Informs only (no hard stops)", "No patient info needed" via `TRAITS`.
- Tests: every tool has all three fields with allowed values; every non-Unknown value has a note and URL; education tools are `No patient info`; filters match expected counts (catalog test fixture).
- Accept: no invented facts (spot check 5 rows against vendor pages, listed in the PR).

### B3. Copy drafts (no code): `/believe`, home thesis, backhoe guide, newsletter page, forum seed threads, privacy/terms
- Write `content/*.md` drafts in the Market voice adapted (plain, short, dry; no em dashes; banned words). `/believe` = 7 thesis blocks. Backhoe guide = 6 to 8 numbered steps (`.steps`) on using AI to study without shortcutting learning, with the PHI rule. 8 to 12 seed threads (4.8). Short `/privacy` and `/terms` (4.9).
- Accept: passes the banned-word and em-dash lint; every Shane quote matches shane-takes.md byte for byte; marked DRAFT for Shane's review.

### B4. New IA and pages (needs B1, B3)
- Routes from 2.1: home (thesis, three doors, latest take, newsletter), `/tools` (directory moved, `?q=` prefill), `/believe`, `/students` restructured with tabs, `/students/backhoe`, `/students/nclex` + 301 from old path, `/newsletter`. Nav per 2.1. Sitemap updated.
- Tests: route test asserts every old URL returns 200 or 301 to the right target; sitemap contains all new pages; nav has 5 items; home has exactly one h1; existing form endpoints unchanged.
- Accept: page count reported by build; screenshots 390/1280 light/dark.

### B5. NCLEX page affiliate slots (needs B4)
- Structured comparison rows for Lecturio, SimpleNursing, Archer Review, UWorld (+ existing NCLEX tools) with a `affiliate_url` field that falls back to the vendor URL when empty. Disclosure line already on the page is kept and shown near any affiliate link. `rel="sponsored nofollow"` on affiliate links.
- Tests: no affiliate link renders without the disclosure on the same page; empty affiliate_url falls back.
- Accept: no affiliate URLs filled in (we don't have approvals yet).

### B6. Newsletter source tagging (small)
- Optional `source` field in `web/contract.js` subscriber parse (allow-list), stored in D1 (`ALTER TABLE subscribers ADD COLUMN source TEXT`), passed to Kit only if a tag map env var exists.
- Tests: contract tests for valid/invalid source; old payloads still accepted; routes test for the Kit call unchanged.

### F1. Forum foundation: schema, router, session, page shell (needs B0)
- `migrations/0002_forum.sql` (4.4), applied to local D1 only. Worker router extension for `/discuss*`, `/login`, `/auth/*`, `/api/auth/*`, `/api/forum/*`, `/api/account/*`, `/u/*`, inlined by build.py so deploy.js keeps working. Session helpers (hash, cookie, sliding expiry). Server-rendered page shell reusing `page()`.
- Tests: miniflare/`wrangler dev --local` or `@cloudflare/vitest-pool-workers` (pick one, document it) integration tests: migration applies cleanly; unauthenticated POST returns 401; bad Origin returns 403; session cookie flags are HttpOnly, Secure, SameSite=Lax.
- Accept: `wrangler dev` serves an empty `/discuss`; existing routes test green; the schema has no report, mod, role, ban or hold tables or columns.

### F2. Auth: magic link (needs F1)
- `/login`, `/api/auth/request`, `/auth/verify`, `/welcome` (pick handle), logout, delete own account. Email sender behind an interface `sendMail(env, to, subject, text)` with a `console` driver for local dev and stub drivers for Cloudflare Email Sending and Resend (no keys, not wired to a live account). Sign-up is open to anyone; no invite codes.
- Tests: token single-use; expired token rejected; request response identical for known and unknown emails; 4th request in 15 min returns 429; handle rules (3 to 24 chars, unique, reserved: admin, shane, nurseaitools); account delete anonymizes posts to "[deleted]".
- Accept: full sign-in loop works locally with the console driver.

### F3. Threads, replies, votes, categories (needs F1; F2 for writes)
- Seed `categories` (4.3 list). Create/read thread, nested replies to depth 4 with `path` ordering, up votes, sorts (top with decay, new, unanswered), pagination, tool tag link. Markdown subset renderer with escaping (no raw HTML, `rel="nofollow ugc"`). Authors edit within 24h and soft delete their own posts; no one else can change or remove a post.
- Tests: XSS payloads render inert; depth 5 reply is rejected or flattened; vote toggle is idempotent and score cache stays correct; sort order fixtures; a non-author edit or delete returns 403; author-deleted items show "[deleted]" in the tree and 410 on direct URL.

### F4. Anti-spam and the patient-info nudge (needs F3)
- Turnstile verify helper with a test-mode secret; rate limiter (4.6) with 429 replies; link-count and honeypot checks. `web/phi.js` (pure) plus the inline browser note (4.7).
- Tests: Turnstile failure blocks the post (bot check); limits enforced exactly at the boundaries; `phi.js` flags a synthetic corpus of 40+ fake identifiers (fake MRNs, dates, "Mr. Smith in room 412", ages 90+) and stays quiet on 40+ clean nursing discussions (dosing concepts, NCLEX questions, "q2h turns") with under 10% false positives; a post containing flagged text is accepted by the server and visible immediately (server-side test); the Post button stays enabled while the note shows (DOM test); no server code imports `phi.js`.
- Accept: no code path holds, rejects, queues or logs a post based on its content.

### F5. Seed threads and launch content (needs F3, B3)
- Seed script inserts 8 to 12 threads from B3 drafts (marked `seed=1`, author `nurseaitools`). `/privacy` and `/terms` pages (4.9). "Discuss this tool" links on tool pages.
- Tests: seed is idempotent; every seed post quoting Shane matches shane-takes.md byte for byte; tool-page links point to existing category/thread routes.
- Accept: Shane reviews the seed threads before anything goes live.

### D1. Deploy prep (last, a human-approved step, NOT done by agents)
- Checklist only: apply migration to remote D1, add `TURNSTILE_SECRET`, `TURNSTILE_SITEKEY`, mail-sender secret, `IP_SALT` to the keep_bindings list in deploy-fn.txt, regenerate, deploy through the connector, verify, note the new version id and the rollback id. Done by me after Shane OKs.

---

## 7. Open questions for Shane (max 5)

1. **Home page:** lead with the thesis and move the full directory to `/tools`, or keep the directory on the home page under the thesis?
2. **Design swap:** go light-first like the real Market site (dark automatically at night), with webfonts and Host Grotesk for reading, which reverses the Oct "no webfonts, dark only" choice? And keep a halftone band (muted) or skip it?
3. **Forum launch timing:** open the forum together with the restructure, or a week after so the seed threads and the first few members are in place?
4. **Email for sign-in:** OK to set up a free email sender (Cloudflare first, Resend free tier as backup) for magic links? It's $0 but a new account.
5. **Your voice on the site:** OK to use the draft line "AI should run the rules in the background so nurses can run the care," and can you give 3 to 5 one-liners in your own words for the pillars so the site and the seed threads quote you, not me?
