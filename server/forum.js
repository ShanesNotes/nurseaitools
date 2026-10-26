// @ts-check
// Forum routes and session helpers. Server only: build.py inlines this file into deploy.js,
// so it must not import anything. See docs/adr/0001-forum-router-and-sessions.md.

/**
 * The slice of the D1 API this module uses.
 * @typedef {{ prepare(sql: string): D1Stmt }} D1Like
 * @typedef {{ bind(...values: unknown[]): D1Stmt, first<T = Record<string, unknown>>(): Promise<T | null>, run(): Promise<unknown> }} D1Stmt
 */

/** @typedef {{ readonly title: string, readonly desc: string, readonly body: string, readonly path: string }} View */
/** @typedef {{ readonly shell: string, readonly notFound: string }} Pages */
/** @typedef {{ readonly id: number, readonly handle: string }} Member */
/** @typedef {{ readonly user: Member, readonly expiresAt: string, readonly refreshed: boolean }} Session */

export const SESSION_COOKIE = '__Host-sid';
const DAY = 86_400_000;
export const SESSION_TTL = 30 * DAY;
const SESSION_REFRESH = 15 * DAY;

const PREFIXES = ['/discuss', '/login', '/auth', '/api/auth', '/api/forum', '/api/account', '/u'];
const MEMBER_POSTS = ['/api/forum/', '/api/account/', '/api/auth/logout'];

/**
 * @param {string} p a pathname with trailing slashes already removed
 */
export function isForumPath(p) {
  return PREFIXES.some((prefix) => p === prefix || p.startsWith(prefix + '/'));
}

/**
 * Order: method, then same-origin Origin on every POST, then a session on member POSTs.
 * Routes from later units (F2 auth, F3 threads) answer 404 until they exist.
 * @param {Request} req
 * @param {{ DB: D1Like }} env
 * @param {string} p
 * @param {Pages} pages
 * @returns {Promise<Response>}
 */
export async function forum(req, env, p, pages) {
  const api = p.startsWith('/api/');
  if (api && req.method !== 'POST') return json(405, { error: 'Method not allowed.' }, { allow: 'POST' });
  if (!api && req.method !== 'GET' && req.method !== 'HEAD') return new Response(null, { status: 405, headers: { allow: 'GET, HEAD' } });

  if (api) {
    if (!sameOrigin(req)) return json(403, { error: 'Cross-site request refused.' });
    const session = await readSession(env.DB, req);
    if (!session && MEMBER_POSTS.some((m) => p === m || p.startsWith(m))) return json(401, { error: 'Sign in first.' });
    return withSession(json(404, { error: 'Not found.' }), session);
  }

  const session = await readSession(env.DB, req);
  if (p === '/discuss') return withSession(html(200, render(pages.shell, discussIndex()), session), session);
  return withSession(html(404, pages.notFound, session), session);
}

/** @returns {View} */
function discussIndex() {
  return {
    title: 'Discuss | Nurse AI Tools',
    desc: 'An open forum for nurses, nursing students and new grads to talk about AI at work and in school.',
    path: '/discuss',
    body: '<section class=deck><p class=kicker>Forum / open to nurses and students</p><h1>Discuss</h1><p class=lede>An open floor for nurses, students and new grads to talk about AI on the job and in school.</p></section>'
      + '<div class=prose><h2>Threads</h2><p data-forum-empty>No threads yet.</p></div>',
  };
}

/**
 * Fills the page() shell from build.py. Values are escaped here; `body` is trusted markup.
 * @param {string} shell
 * @param {View} view
 */
export function render(shell, view) {
  return shell
    .split('%%TITLE%%').join(escapeHtml(view.title))
    .split('%%DESC%%').join(escapeHtml(view.desc))
    .split('%%PATH%%').join(escapeHtml(view.path))
    .split('%%BODY%%').join(view.body);
}

/** @param {string} s */
export function escapeHtml(s) {
  return s.replace(/[&<>"']/g, (c) => `&#${c.charCodeAt(0)};`);
}

/**
 * Browsers send Origin on every POST. A missing or foreign Origin is refused.
 * @param {Request} req
 */
export function sameOrigin(req) {
  return req.headers.get('origin') === new URL(req.url).origin;
}

// Sessions (Lucia-style): the cookie holds a random token, D1 holds only its SHA-256.

export function newSessionToken() {
  const bytes = crypto.getRandomValues(new Uint8Array(32));
  return btoa(String.fromCharCode(...bytes)).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

/** @param {string} token */
export async function hashToken(token) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(token));
  return [...new Uint8Array(digest)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

/**
 * @param {string} token
 * @param {number} [maxAgeMs]
 */
export function sessionCookie(token, maxAgeMs = SESSION_TTL) {
  return `${SESSION_COOKIE}=${token}; Path=/; Max-Age=${Math.floor(maxAgeMs / 1000)}; HttpOnly; Secure; SameSite=Lax`;
}

export function clearSessionCookie() {
  return `${SESSION_COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`;
}

/** @param {Request} req */
export function sessionToken(req) {
  for (const part of (req.headers.get('cookie') || '').split(';')) {
    const [name, ...rest] = part.trim().split('=');
    if (name === SESSION_COOKIE) return rest.join('=') || null;
  }
  return null;
}

/**
 * @param {D1Like} db
 * @param {number} userId
 * @param {number} [now]
 */
export async function createSession(db, userId, now = Date.now()) {
  const token = newSessionToken();
  const expiresAt = new Date(now + SESSION_TTL).toISOString();
  await db.prepare('INSERT INTO sessions(id_hash,user_id,expires_at,created_at) VALUES(?,?,?,?)')
    .bind(await hashToken(token), userId, expiresAt, new Date(now).toISOString()).run();
  return { token, expiresAt, cookie: sessionCookie(token) };
}

/**
 * Returns the member, or null. Expired sessions and sessions of deleted users are removed.
 * A session with under 15 days left slides forward to 30 days.
 * @param {D1Like} db
 * @param {string} token
 * @param {number} [now]
 * @returns {Promise<Session | null>}
 */
export async function validateSession(db, token, now = Date.now()) {
  const idHash = await hashToken(token);
  const row = await db.prepare('SELECT s.expires_at, u.id, u.handle, u.deleted_at FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.id_hash = ?')
    .bind(idHash).first();
  if (!row) return null;
  const expires = Date.parse(String(row.expires_at));
  if (!(expires > now) || row.deleted_at) {
    await invalidateSession(db, token);
    return null;
  }
  const user = { id: Number(row.id), handle: String(row.handle) };
  if (expires - now >= SESSION_REFRESH) return { user, expiresAt: String(row.expires_at), refreshed: false };
  const expiresAt = new Date(now + SESSION_TTL).toISOString();
  await db.prepare('UPDATE sessions SET expires_at = ? WHERE id_hash = ?').bind(expiresAt, idHash).run();
  return { user, expiresAt, refreshed: true };
}

/**
 * @param {D1Like} db
 * @param {string} token
 */
export async function invalidateSession(db, token) {
  await db.prepare('DELETE FROM sessions WHERE id_hash = ?').bind(await hashToken(token)).run();
}

/**
 * @param {D1Like} db
 * @param {Request} req
 * @returns {Promise<(Session & { token: string }) | null>}
 */
async function readSession(db, req) {
  const token = sessionToken(req);
  if (!token) return null;
  const session = await validateSession(db, token);
  return session && { ...session, token };
}

/**
 * Signed-in responses are private; a slid session gets a fresh cookie.
 * @param {Response} res
 * @param {(Session & { token: string }) | null} session
 */
function withSession(res, session) {
  if (!session) return res;
  res.headers.set('cache-control', 'private, no-store');
  if (session.refreshed) res.headers.append('set-cookie', sessionCookie(session.token));
  return res;
}

/**
 * @param {number} status
 * @param {string} body
 * @param {unknown} session
 */
function html(status, body, session) {
  const cache = status === 200 && !session ? 'public, max-age=30' : 'private, no-store';
  return new Response(body, { status, headers: { 'content-type': 'text/html;charset=utf-8', 'cache-control': cache } });
}

/**
 * @param {number} status
 * @param {Record<string, string>} body
 * @param {Record<string, string>} [extra]
 */
function json(status, body, extra = {}) {
  return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', ...extra } });
}
