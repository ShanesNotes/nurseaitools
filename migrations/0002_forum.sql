-- Forum schema (plan 4.4). Open forum: no report, mod, role, ban or hold tables or columns.
-- subscribers and submissions stay in schema.sql and are untouched.
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
