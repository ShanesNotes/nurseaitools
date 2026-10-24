import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

// Drives the built worker, so run `python3 build.py` after editing landing.py or tools.py.
/** @type {{ fetch: (req: Request, env: object, ctx: object) => Promise<Response> }} */
const worker = (await import(new URL('../dist/worker.js', import.meta.url).href)).default;
/** @type {{ slug: string, name: string, what: string, hipaa: string }[]} */
const tools = JSON.parse(readFileSync(new URL('../tools.json', import.meta.url), 'utf8'));
const BASE = 'https://nurseaitools.com';
const GUIDES = ['/students/best-ai-nclex-prep', '/students/free-nclex-prep', '/students/ngn-practice-tools', '/students/chatgpt-for-nclex'];

/** @param {string} path */
async function get(path) {
  const res = await worker.fetch(new Request(BASE + path), {}, { waitUntil() {} });
  return { status: res.status, html: await res.text() };
}

/** @param {string} s */
const unescape = (s) => s.replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');

test('each landing page is 200 with its own title, description, canonical, h1, and the newsletter form', async () => {
  const titles = new Set();
  const descriptions = new Set();
  for (const path of GUIDES) {
    const { status, html } = await get(path);
    assert.equal(status, 200, path);
    const title = html.match(/<title>([^<]+)<\/title>/)?.[1] ?? '';
    const description = html.match(/<meta name=description content="([^"]+)"/)?.[1] ?? '';
    assert.ok(title.endsWith(' | Nurse AI Tools'), `${path} title ${title}`);
    assert.ok(description.length > 50 && description.length <= 160, `${path} description is ${description.length} chars`);
    titles.add(title);
    descriptions.add(description);
    assert.ok(html.includes(`<link rel=canonical href="${BASE}${path}">`), `${path} canonical`);
    assert.equal(html.match(/<h1[ >]/g)?.length, 1, `${path} h1`);
    assert.ok(html.includes('<form action="/api/subscribe"'), `${path} newsletter form`);
    assert.ok(html.includes('href="/"'), `${path} links the directory`);
  }
  assert.equal(titles.size, GUIDES.length, 'titles are unique');
  assert.equal(descriptions.size, GUIDES.length, 'descriptions are unique');
});

test('every quote on a landing page is copied from a tools.json entry', async () => {
  const sources = tools.flatMap((t) => [t.what, t.hipaa]);
  for (const path of GUIDES) {
    const { html } = await get(path);
    const quotes = [...html.matchAll(/<q>([^<]+)<\/q>/g)].map((m) => unescape(m[1] ?? ''));
    assert.ok(quotes.length > 0, `${path} has quotes`);
    const prompts = quotes.filter((q) => !sources.some((s) => s.includes(q)));
    // The only quotes not from tools.json are the study prompts on the ChatGPT page.
    if (path !== '/students/chatgpt-for-nclex') assert.deepEqual(prompts, [], `${path} quotes something tools.json does not say`);
    else assert.equal(prompts.length, 3, `${path} has exactly the 3 study prompts outside tools.json`);
  }
});

test('landing pages link only to tool pages that exist', async () => {
  const slugs = new Set(tools.map((t) => t.slug));
  for (const path of GUIDES) {
    const { html } = await get(path);
    const linked = [...html.matchAll(/href="\/tools\/([^"]+)"/g)].map((m) => m[1] ?? '');
    assert.ok(linked.length >= 3, `${path} links tools`);
    for (const slug of linked) assert.ok(slugs.has(slug), `${path} links /tools/${slug}`);
  }
});

test('the students hub, the older guides, and the sitemap link every landing page', async () => {
  const hub = (await get('/students')).html;
  const tutors = (await get('/students/nclex-ai-tutors')).html;
  const free = (await get('/students/best-free-ai')).html;
  const sitemap = (await get('/sitemap.xml')).html;
  for (const path of GUIDES) {
    assert.ok(hub.includes(`href="${path}"`), `/students links ${path}`);
    assert.ok(tutors.includes(`href="${path}"`), `/students/nclex-ai-tutors links ${path}`);
    assert.ok(free.includes(`href="${path}"`), `/students/best-free-ai links ${path}`);
    assert.ok(sitemap.includes(`<loc>${BASE}${path}</loc>`), `sitemap lists ${path}`);
  }
});
