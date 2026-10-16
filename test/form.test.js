import { test } from 'node:test';
import assert from 'node:assert/strict';
import { drive } from '../web/fsm.js';
import { formMachine } from '../web/form.js';
import { decide, encodeReply, formAt } from '../web/contract.js';

/** @import { FormState } from '../web/form.js' */
/** @import { FormKind } from '../web/contract.js' */

/** @type {typeof fetch} */
const worker = async (url, init) => {
  const kind = formAt(String(url));
  assert.ok(kind, `no form at ${url}`);
  return encodeReply(decide(kind, String(init?.body)).reply);
};

/**
 * @param {FormKind} kind
 * @param {typeof fetch} fetchImpl
 */
function run(kind, fetchImpl) {
  /** @type {string[]} */
  const seen = [];
  const form = drive(formMachine(kind, fetchImpl), (s) => seen.push(s.kind));
  return { form, seen };
}

test('a valid signup walks idle, validating, submitting, success', async () => {
  const { form, seen } = run('subscribe', worker);
  const end = await form.send({ type: 'submit', fields: { email: 'rn@example.org', hp: '' } });
  assert.deepEqual(end, { kind: 'success', message: "You're subscribed. Thanks!" });
  assert.deepEqual(seen, ['idle', 'validating', 'submitting', 'success']);
});

test('a valid tool submission ends in success with the server message', async () => {
  const { form } = run('submit', worker);
  const end = await form.send({ type: 'submit', fields: { name: 'Sully', url: 'https://sully.ai', category: 'Ambient documentation', notes: '', email: '', hp: '' } });
  assert.deepEqual(end, { kind: 'success', message: 'Thanks! Your submission is in the review queue.' });
});

test('an invalid email stops in error without a request', async () => {
  let calls = 0;
  const { form, seen } = run('subscribe', async (...a) => (calls++, worker(...a)));
  const end = await form.send({ type: 'submit', fields: { email: 'rn@' } });
  assert.deepEqual(end, { kind: 'error', message: 'Please enter a valid email.', invalidControls: ['email'] });
  assert.deepEqual(seen, ['idle', 'validating', 'error']);
  assert.equal(calls, 0);
});

test('a server refusal ends in error with the server copy', async () => {
  const { form, seen } = run('subscribe', async () => encodeReply({ ok: false, error: 'Bad request' }));
  const end = await form.send({ type: 'submit', fields: { email: 'rn@example.org' } });
  assert.deepEqual(end, { kind: 'error', message: 'Bad request', invalidControls: [] });
  assert.deepEqual(seen, ['idle', 'validating', 'submitting', 'error']);
});

test('a network failure ends in error with a message', async () => {
  const { form } = run('submit', async () => { throw new TypeError('Failed to fetch'); });
  const end = await form.send({ type: 'submit', fields: { name: 'Sully', url: 'https://sully.ai' } });
  assert.deepEqual(end, { kind: 'error', message: "We couldn't reach the server. Check your connection and try again.", invalidControls: [] });
});

test('a second submit while submitting is ignored and sends one request', async () => {
  let calls = 0;
  const { form } = run('subscribe', async (...a) => (calls++, worker(...a)));
  const first = form.send({ type: 'submit', fields: { email: 'rn@example.org' } });
  const second = await form.send({ type: 'submit', fields: { email: 'rn@example.org' } });
  assert.equal(second.kind, 'submitting');
  assert.deepEqual(await first, { kind: 'success', message: "You're subscribed. Thanks!" });
  assert.equal(calls, 1);
});

test('an edit after an error clears it and a corrected submit succeeds', async () => {
  const { form, seen } = run('subscribe', worker);
  await form.send({ type: 'submit', fields: { email: 'rn@' } });
  await form.send({ type: 'edit' });
  const end = await form.send({ type: 'submit', fields: { email: 'rn@example.org' } });
  assert.deepEqual(end, { kind: 'success', message: "You're subscribed. Thanks!" });
  assert.deepEqual(seen, ['idle', 'validating', 'error', 'idle', 'validating', 'submitting', 'success']);
});

test('a blank tool name names that field and sends nothing', async () => {
  let calls = 0;
  const { form } = run('submit', async (...a) => (calls++, worker(...a)));
  const end = await form.send({ type: 'submit', fields: { name: '  ', url: 'https://sully.ai' } });
  assert.deepEqual(end, { kind: 'error', message: 'Enter the tool name.', invalidControls: ['name'] });
  assert.equal(calls, 0);
});

test('a url that does not start with http names that field', async () => {
  let calls = 0;
  const { form } = run('submit', async (...a) => (calls++, worker(...a)));
  const end = await form.send({ type: 'submit', fields: { name: 'Example', url: 'notaurl' } });
  assert.deepEqual(end, { kind: 'error', message: 'Enter a URL that starts with http:// or https://.', invalidControls: ['url'] });
  assert.equal(calls, 0);
});

test('a submission missing the name and the url names both fields', async () => {
  const { form } = run('submit', async () => { throw new Error('no request'); });
  const end = await form.send({ type: 'submit', fields: { name: '', url: '' } });
  assert.deepEqual(end, {
    kind: 'error',
    message: 'Enter a tool name and a URL that starts with http:// or https://.',
    invalidControls: ['name', 'url'],
  });
});

test('next returns the same object for an event the state ignores', () => {
  const machine = formMachine('subscribe', worker);
  /** @type {FormState} */
  const submitting = { kind: 'submitting', fields: { email: 'rn@example.org' } };
  assert.equal(machine.next(submitting, { type: 'edit' }), submitting);
  assert.deepEqual(machine.next({ kind: 'error', message: 'x', invalidControls: [] }, { type: 'edit' }), { kind: 'idle' });
});
