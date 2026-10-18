import { formAt, decide, encodeReply } from '../web/contract.js';

const PAGES = __PAGES__;
const NOT_FOUND = __NOT_FOUND__;
const SITEMAP = __SITEMAP__;
const SCRIPTS = __SCRIPTS__;
const HTML = { 'content-type': 'text/html;charset=utf-8', 'cache-control': 'public,max-age=300' };
const SCRIPT = { 'content-type': 'text/javascript;charset=utf-8', 'cache-control': 'public,max-age=300' };

export default {
  async fetch(req, env, ctx) {
    const u = new URL(req.url);
    if (u.hostname === 'www.nurseaitools.com') { u.hostname = 'nurseaitools.com'; return Response.redirect(u.toString(), 301); }
    const p = u.pathname.replace(/\/+$/, '') || '/';

    const form = req.method === 'POST' ? formAt(p) : null;
    if (form) {
      const { reply, save } = decide(form, await req.text());
      if (save) {
        await persist(env.DB, save, { at: new Date().toISOString(), userAgent: (req.headers.get('user-agent') || '').slice(0, 200) });
        if (save.kind === 'subscriber' && env.KIT_API_KEY) ctx.waitUntil(kitAdd(env, save.email).catch(() => {}));
      }
      return encodeReply(reply);
    }

    if (SCRIPTS[p]) return new Response(SCRIPTS[p], { headers: SCRIPT });
    if (p === '/sitemap.xml') return new Response(SITEMAP, { headers: { 'content-type': 'application/xml' } });
    if (p === '/robots.txt') return new Response('User-agent: *\nAllow: /\nSitemap: __BASE__/sitemap.xml\n');
    if (p === '/22108e5ac38312c5b3b7a578b9d42a4b.txt') return new Response('22108e5ac38312c5b3b7a578b9d42a4b', { headers: { 'content-type': 'text/plain;charset=utf-8' } });
    if (PAGES[p]) return new Response(PAGES[p], { headers: HTML });
    return new Response(NOT_FOUND, { status: 404, headers: { 'content-type': 'text/html;charset=utf-8' } });
  },
};

/**
 * @param {{ KIT_API_KEY?: string, KIT_TAG_ID?: string }} env
 * @param {string} email
 */
async function kitAdd(env, email) {
  const headers = { 'content-type': 'application/json', 'X-Kit-Api-Key': env.KIT_API_KEY };
  await fetch('https://api.kit.com/v4/subscribers', {
    method: 'POST',
    headers,
    body: JSON.stringify({ email_address: email, state: 'active' }),
  });
  if (!env.KIT_TAG_ID) return;
  await fetch(`https://api.kit.com/v4/tags/${env.KIT_TAG_ID}/subscribers`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ email_address: email }),
  });
}

/**
 * @param {D1Database} db
 * @param {import('../web/contract.js').Entry} entry
 * @param {{ at: string, userAgent: string }} meta
 */
async function persist(db, entry, meta) {
  switch (entry.kind) {
    case 'subscriber':
      return db.prepare('INSERT OR IGNORE INTO subscribers(email,created_at,user_agent) VALUES(?,?,?)')
        .bind(entry.email, meta.at, meta.userAgent).run();
    case 'submission':
      return db.prepare('INSERT INTO submissions(name,url,category,notes,email,created_at,user_agent) VALUES(?,?,?,?,?,?,?)')
        .bind(entry.name, entry.url, entry.category, entry.notes, entry.email, meta.at, meta.userAgent).run();
  }
}
