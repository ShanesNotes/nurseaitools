import { test } from 'node:test';
import assert from 'node:assert/strict';
import { decide, encodeReply, formAt, send } from '../web/contract.js';

const BAD_REQUEST = { reply: { ok: false, error: 'Bad request' }, save: null };

test('bad JSON is refused and saves nothing', () => {
  assert.deepEqual(decide('subscribe', '{nope'), BAD_REQUEST);
});

test('JSON null, numbers, booleans, and strings are refused instead of crashing', () => {
  assert.deepEqual(
    ['null', '42', 'true', '"rn@example.org"'].map((body) => decide('submit', body)),
    [BAD_REQUEST, BAD_REQUEST, BAD_REQUEST, BAD_REQUEST],
  );
});

test('a JSON array takes the field path and fails the field check', () => {
  assert.deepEqual(decide('subscribe', '[]'), { reply: { ok: false, error: 'Please enter a valid email.' }, save: null });
  assert.deepEqual(decide('submit', '["Sully"]'), { reply: { ok: false, error: 'Tool name and a valid URL are required.' }, save: null });
});

test('the honeypot runs before the email check', () => {
  assert.deepEqual(decide('subscribe', '{"email":"not-an-email","hp":"bot"}'), { reply: { ok: true, message: 'Thanks!' }, save: null });
});

test('a filled honeypot on the submit form saves nothing', () => {
  assert.deepEqual(decide('submit', '{"name":"Sully","url":"https://sully.ai","hp":"x"}'), { reply: { ok: true, message: 'Thanks!' }, save: null });
});

test('an invalid email is refused with the form copy', () => {
  assert.deepEqual(decide('subscribe', '{"email":"a@b"}'), { reply: { ok: false, error: 'Please enter a valid email.' }, save: null });
});

test('a valid email is normalized and saved', () => {
  assert.deepEqual(decide('subscribe', '{"email":"  RN@Example.ORG ","hp":""}'), {
    reply: { ok: true, message: "You're subscribed. Thanks!" },
    save: { kind: 'subscriber', email: 'rn@example.org' },
  });
});

test('a submission without an http URL is refused', () => {
  assert.deepEqual(decide('submit', '{"name":"Sully","url":"sully.ai"}'), {
    reply: { ok: false, error: 'Tool name and a valid URL are required.' },
    save: null,
  });
});

test('a valid submission is trimmed and saved', () => {
  assert.deepEqual(decide('submit', '{"name":" Sully ","url":" https://sully.ai ","category":"Ambient documentation","notes":"","email":""}'), {
    reply: { ok: true, message: 'Thanks! Your submission is in the review queue.' },
    save: { kind: 'submission', name: 'Sully', url: 'https://sully.ai', category: 'Ambient documentation', notes: '', email: '' },
  });
});

test('submission fields are cut to their column limits', () => {
  const body = JSON.stringify({ name: 'n'.repeat(250), url: `https://${'u'.repeat(600)}`, category: 'c'.repeat(150), notes: 'x'.repeat(3500), email: 'e'.repeat(250) });
  const { save } = decide('submit', body);
  assert.deepEqual(
    save && save.kind === 'submission' ? [save.name.length, save.url.length, save.category.length, save.notes.length, save.email.length] : null,
    [200, 500, 100, 3000, 200],
  );
});

test('a refusal encodes as status 400 with an error body', async () => {
  const res = encodeReply({ ok: false, error: 'Bad request' });
  assert.equal(res.status, 400);
  assert.equal(res.headers.get('content-type'), 'application/json');
  assert.deepEqual(await res.json(), { error: 'Bad request' });
});

test('an acceptance encodes as status 200 with a message body', async () => {
  const res = encodeReply({ ok: true, message: "You're subscribed. Thanks!" });
  assert.equal(res.status, 200);
  assert.deepEqual(await res.json(), { message: "You're subscribed. Thanks!" });
});

test('form paths route to their form and nothing else does', () => {
  assert.deepEqual(['/api/subscribe', '/api/submit', '/api/other', '/'].map(formAt), ['subscribe', 'submit', null, null]);
});

test('send posts the raw fields as JSON to the form endpoint', async () => {
  /** @type {Array<[string, RequestInit | undefined]>} */
  const posts = [];
  /** @type {typeof fetch} */
  const fetchImpl = async (url, init) => {
    posts.push([String(url), init]);
    return encodeReply({ ok: true, message: 'Thanks! Your submission is in the review queue.' });
  };
  const reply = await send('submit', { name: ' Sully ', url: 'https://sully.ai' }, fetchImpl);
  assert.deepEqual(reply, { ok: true, message: 'Thanks! Your submission is in the review queue.' });
  assert.deepEqual(
    posts.map(([url, init]) => [url, init?.method, init?.headers, init?.body]),
    [['/api/submit', 'POST', { 'content-type': 'application/json' }, '{"name":" Sully ","url":"https://sully.ai"}']],
  );
});

test('a failed reply with no error string reads "Something went wrong."', async () => {
  const reply = await send('subscribe', { email: 'rn@example.org' }, async () => new Response('<h1>Bad gateway</h1>', { status: 502 }));
  assert.deepEqual(reply, { ok: false, error: 'Something went wrong.' });
});

test('an ok reply with an unreadable body reads "Thanks!"', async () => {
  const reply = await send('subscribe', { email: 'rn@example.org' }, async () => new Response('ok', { status: 200 }));
  assert.deepEqual(reply, { ok: true, message: 'Thanks!' });
});
