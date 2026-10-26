// Integration tests for the forum foundation (F1). They run the worker that deploy.js uploads
// (every module inlined by build.py) in Miniflare with an in-memory D1 and the forum migration applied.
// Run `python3 build.py` first; npm test reads the committed deploy.js.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { Miniflare } from 'miniflare';
import { isForumPath, hashToken, sessionCookie, SESSION_COOKIE, SESSION_TTL } from '../server/forum.js';

const ORIGIN = 'https://nurseaitools.com';
const DAY = 86_400_000;
const read = (/** @type {string} */ f) => readFileSync(new URL('../' + f, import.meta.url), 'utf8');

/** The worker source embedded in deploy.js as `const code="..."`. */
function deployedCode() {
  const src = read('deploy.js');
  const start = src.indexOf('const code=') + 'const code='.length;
  let i = start + 1;
  while (src[i] !== '"') i += src[i] === '\\' ? 2 : 1;
  return /** @type {string} */ (JSON.parse(src.slice(start, i + 1)));
}

/** @param {string} sql */
function statements(sql) {
  return sql.replace(/--.*$/gm, '').split(';').map((s) => s.trim()).filter(Boolean);
}

/**
 * @param {string} sql
 * @returns {Promise<Record<string, unknown>[]>}
 */
async function rows(sql) {
  return (await db.prepare(sql).all()).results;
}

/** @type {Miniflare} */
let mf;
/** @type {Awaited<ReturnType<Miniflare['getD1Database']>>} */
let db;
let migrated = /** @type {unknown} */ (null);

before(async () => {
  mf = new Miniflare({ modules: true, script: deployedCode(), compatibilityDate: '2025-07-18', d1Databases: { DB: 'nurseaitools-test' } });
  db = await mf.getD1Database('DB');
  const all = [...statements(read('schema.sql')), ...statements(read('migrations/0002_forum.sql'))];
  migrated = await db.batch(all.map((s) => db.prepare(s)));
});

after(() => mf.dispose());

/**
 * @param {string} path
 * @param {{ method?: string, origin?: string | null, cookie?: string, body?: string }} [opts]
 */
function hit(path, { method = 'GET', origin = ORIGIN, cookie, body } = {}) {
  /** @type {Record<string, string>} */
  const headers = {};
  if (method !== 'GET' && origin) headers.origin = origin;
  if (cookie) headers.cookie = cookie;
  if (method !== 'GET') headers['content-type'] = 'application/json';
  return mf.dispatchFetch(ORIGIN + path, { method, headers, body: method === 'GET' ? undefined : body ?? '{}' });
}

let nextUser = 1;
/**
 * @param {{ expiresIn: number, deleted?: boolean }} opts
 */
async function member({ expiresIn, deleted = false }) {
  const id = nextUser++;
  const now = new Date().toISOString();
  await db.prepare('INSERT INTO users(id,email,handle,created_at,deleted_at) VALUES(?,?,?,?,?)')
    .bind(id, `user${id}@example.invalid`, `member${id}`, now, deleted ? now : null).run();
  const token = `test-token-${id}`;
  await db.prepare('INSERT INTO sessions(id_hash,user_id,expires_at,created_at) VALUES(?,?,?,?)')
    .bind(await hashToken(token), id, new Date(Date.now() + expiresIn).toISOString(), now).run();
  return { token, cookie: `${SESSION_COOKIE}=${token}` };
}

test('the forum migration applies cleanly on top of schema.sql', async () => {
  assert.ok(Array.isArray(migrated) && migrated.every((r) => r.success), 'every statement succeeded');
  const tables = await rows("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%' ORDER BY name");
  assert.deepEqual(tables.map((r) => r.name), ['categories', 'login_tokens', 'rate_events', 'replies', 'sessions', 'submissions', 'subscribers', 'threads', 'users', 'votes']);
});

test('the schema has no report, mod, role, ban or hold tables or columns', async () => {
  const objects = await rows("SELECT type, name FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' AND name NOT LIKE '_cf_%'");
  const names = objects.map((o) => String(o.name));
  for (const t of objects.filter((o) => o.type === 'table')) {
    const cols = await rows(`SELECT name FROM pragma_table_info('${t.name}')`);
    names.push(...cols.map((c) => `${t.name}.${c.name}`));
  }
  assert.ok(names.length > 60, `${names.length} names inspected`);
  const banned = names.filter((n) => /report|mod|role|ban|hold/i.test(n));
  assert.deepEqual(banned, []);
});

test('GET /discuss serves the empty forum in the site shell', async () => {
  const res = await hit('/discuss');
  assert.equal(res.status, 200);
  assert.equal(res.headers.get('cache-control'), 'public, max-age=30');
  assert.equal(res.headers.get('set-cookie'), null);
  const page = await res.text();
  const home = await (await hit('/')).text();
  const css = (/** @type {string} */ s) => s.match(/<style>([\s\S]*?)<\/style>/)?.[1];
  assert.ok(css(page) && css(page) === css(home), 'same stylesheet as the baked pages');
  assert.match(page, /<title>Discuss \| Nurse AI Tools<\/title>/);
  assert.match(page, /<link rel=canonical href="https:\/\/nurseaitools\.com\/discuss">/);
  assert.equal(page.match(/<h1\b/g)?.length, 1);
  assert.match(page, /data-forum-empty>No threads yet\./);
  assert.doesNotMatch(page, /%%[A-Z]+%%/);
  assert.equal((await hit('/discuss/')).status, 200);
});

test('forum paths that later units build answer 404 for now, and unrelated paths are untouched', async () => {
  for (const p of ['/login', '/u/someone', '/discuss/c/nclex', '/auth/verify']) assert.equal((await hit(p)).status, 404, p);
  assert.equal(isForumPath('/discussion'), false);
  assert.equal(isForumPath('/user'), false);
  assert.equal(isForumPath('/api/subscribe'), false);
  assert.equal((await hit('/discussion')).status, 404);
  const sub = await hit('/api/subscribe', { method: 'POST', body: JSON.stringify({ email: 'f1@example.invalid' }) });
  assert.equal(sub.status, 200, 'the newsletter form still posts');
});

test('an unauthenticated POST to a member endpoint returns 401', async () => {
  for (const p of ['/api/forum/threads', '/api/forum/replies', '/api/forum/vote', '/api/forum/edit', '/api/forum/delete', '/api/account/delete', '/api/auth/logout']) {
    const res = await hit(p, { method: 'POST' });
    assert.equal(res.status, 401, p);
    assert.deepEqual(await res.json(), { error: 'Sign in first.' });
  }
  const forged = await hit('/api/forum/threads', { method: 'POST', cookie: `${SESSION_COOKIE}=not-a-session` });
  assert.equal(forged.status, 401, 'an unknown session token');
});

test('a POST with a missing or foreign Origin returns 403, even when signed in', async () => {
  const { cookie } = await member({ expiresIn: 20 * DAY });
  for (const origin of ['https://evil.example', 'http://nurseaitools.com', 'null', null]) {
    for (const p of ['/api/forum/threads', '/api/auth/request', '/api/account/delete']) {
      const res = await hit(p, { method: 'POST', origin, cookie });
      assert.equal(res.status, 403, `${p} from ${origin}`);
    }
  }
  assert.equal((await hit('/api/forum/threads')).status, 405, 'GET on an API path');
});

test('a valid session passes the gates and its responses are private', async () => {
  const { cookie } = await member({ expiresIn: 20 * DAY });
  const post = await hit('/api/forum/threads', { method: 'POST', cookie });
  assert.equal(post.status, 404, 'past the 401 gate; threads arrive in F3');
  const page = await hit('/discuss', { cookie });
  assert.equal(page.status, 200);
  assert.equal(page.headers.get('cache-control'), 'private, no-store');
  assert.equal(page.headers.get('set-cookie'), null, 'no refresh with 20 days left');
});

test('a session near expiry slides forward and resets an HttpOnly, Secure, SameSite=Lax cookie', async () => {
  const { token, cookie } = await member({ expiresIn: 2 * DAY });
  const res = await hit('/discuss', { cookie });
  assert.equal(res.status, 200);
  const set = res.headers.get('set-cookie') ?? '';
  const attrs = set.split(';').map((s) => s.trim());
  assert.equal(attrs[0], `${SESSION_COOKIE}=${token}`);
  assert.ok(attrs.includes('HttpOnly'), set);
  assert.ok(attrs.includes('Secure'), set);
  assert.ok(attrs.includes('SameSite=Lax'), set);
  assert.ok(attrs.includes('Path=/'), set);
  assert.ok(attrs.includes(`Max-Age=${SESSION_TTL / 1000}`), set);
  assert.ok(!attrs.some((a) => /^domain=/i.test(a)), '__Host- cookies carry no Domain');
  const row = await db.prepare('SELECT expires_at FROM sessions WHERE id_hash = ?').bind(await hashToken(token)).first();
  assert.ok(Date.parse(String(row?.expires_at)) > Date.now() + 29 * DAY, 'expires_at moved to 30 days out');
  assert.equal(sessionCookie('x'), `${SESSION_COOKIE}=x; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`);
});

test('expired sessions and sessions of deleted accounts are refused and removed', async () => {
  for (const opts of [{ expiresIn: -DAY }, { expiresIn: 20 * DAY, deleted: true }]) {
    const { token, cookie } = await member(opts);
    assert.equal((await hit('/api/forum/vote', { method: 'POST', cookie })).status, 401, JSON.stringify(opts));
    const row = await db.prepare('SELECT 1 AS n FROM sessions WHERE id_hash = ?').bind(await hashToken(token)).first();
    assert.equal(row, null);
  }
});

test('the database stores only a SHA-256 of the session token', async () => {
  assert.equal(await hashToken('abc'), 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad');
  const { token } = await member({ expiresIn: 20 * DAY });
  const raw = await db.prepare('SELECT COUNT(*) AS n FROM sessions WHERE id_hash = ?').bind(token).first();
  assert.equal(raw?.n, 0);
});
