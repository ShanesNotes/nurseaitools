// deploy.js is what production deploys run, through the Cloudflare API. It does not read wrangler.toml,
// so these tests run it against a fake `cloudflare` client and check every request it would make.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const read = (/** @type {string} */ f) => readFileSync(new URL('../' + f, import.meta.url), 'utf8');

/** @typedef {{ method: string, path: string, body?: unknown }} Req */

/** Run deploy.js with a fake client that answers success to everything. */
async function requests() {
  /** @type {Req[]} */
  const sent = [];
  const cloudflare = { request: async (/** @type {Req} */ r) => (sent.push(r), { success: true, errors: [] }) };
  const run = new Function('cloudflare', 'accountId', 'return (' + read('deploy.js') + ')')(cloudflare, 'acct');
  await run();
  return sent;
}

test('wrangler.toml keeps workers.dev off', () => {
  assert.match(read('wrangler.toml'), /^workers_dev = false$/m);
});

test('deploy.js uploads the worker, then turns the workers.dev subdomain and its previews off', async () => {
  const sent = await requests();
  assert.deepEqual(sent.map((r) => `${r.method} ${r.path}`), [
    'PUT /accounts/acct/workers/scripts/nurseaitools',
    'POST /accounts/acct/workers/scripts/nurseaitools/subdomain',
  ]);
  assert.deepEqual(sent[1]?.body, { enabled: false, previews_enabled: false });
});

test('deploy.js never sends enabled: true to any endpoint', async () => {
  for (const r of await requests()) {
    if (typeof r.body === 'string') continue; // The multipart worker upload.
    assert.doesNotMatch(JSON.stringify(r.body ?? {}), /"(enabled|previews_enabled)":true/, `${r.method} ${r.path}`);
  }
});
