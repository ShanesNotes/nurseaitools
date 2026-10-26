import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const worker = readFileSync(new URL('../worker.template.js', import.meta.url), 'utf8');

test('the worker keeps the public routes', () => {
  assert.match(worker, /u\.hostname === 'www\.nurseaitools\.com'/);
  assert.match(worker, /Response\.redirect\(u\.toString\(\), 301\)/);
  assert.match(worker, /p === '\/sitemap\.xml'/);
  assert.match(worker, /p === '\/robots\.txt'/);
  assert.match(worker, /p === '\/22108e5ac38312c5b3b7a578b9d42a4b\.txt'/);
  assert.match(worker, /new Response\('22108e5ac38312c5b3b7a578b9d42a4b'/);
});

test('a trailing slash on a GET or HEAD redirects to the clean path, keeping the query', () => {
  assert.match(worker, /if \(p !== u\.pathname && \(req\.method === 'GET' \|\| req\.method === 'HEAD'\)\) \{ u\.pathname = p; return Response\.redirect\(u\.toString\(\), 301\); \}/);
});

test('a subscriber is sent to Kit only after the insert, and only when the key is set', () => {
  assert.match(worker, /await persist\(env\.DB, save/);
  assert.match(worker, /save\.kind === 'subscriber' && env\.KIT_API_KEY\) ctx\.waitUntil\(kitAdd\(env, save\.email\)\.catch\(\(\) => \{\}\)\)/);
  assert.match(worker, /https:\/\/api\.kit\.com\/v4\/subscribers/);
  assert.match(worker, /'X-Kit-Api-Key': env\.KIT_API_KEY/);
  assert.match(worker, /email_address: email, state: 'active'/);
  assert.match(worker, /if \(!env\.KIT_TAG_ID\) return/);
  assert.match(worker, /https:\/\/api\.kit\.com\/v4\/tags\/\$\{env\.KIT_TAG_ID\}\/subscribers/);
});
