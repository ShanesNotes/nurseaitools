import { test } from 'node:test';
import assert from 'node:assert/strict';
import { drive } from '../web/fsm.js';
import { catalogMachine } from '../web/catalog.js';

/** @import { CatalogState, CatalogEvent } from '../web/catalog.js' */

const items = [
  { id: 'sully', category: 'Ambient documentation', text: 'sully sully.ai ambient charting', traits: ['hipaa'] },
  { id: 'nurse-handoff', category: 'Handoff & summaries', text: 'nurse handoff shift report', traits: ['nurses'] },
  { id: 'nclex-tutor', category: 'Education / NCLEX', text: 'nclex tutor practice questions', traits: ['nurses'] },
];

/** @type {CatalogState} */
const IDLE = { kind: 'idle' };

/**
 * @param {CatalogState} state
 * @param {...CatalogEvent} events
 * @returns {CatalogState}
 */
function after(state, ...events) {
  const { next } = catalogMachine(items);
  return events.reduce(next, state);
}

test('starts idle', () => {
  assert.deepEqual(catalogMachine(items).initial, { kind: 'idle' });
});

test('a trait filter shows matching rows in page order', () => {
  assert.deepEqual(after(IDLE, { type: 'trait', trait: 'nurses', on: true }), {
    kind: 'filtering',
    filters: { query: '', category: null, traits: ['nurses'] },
    visible: ['nurse-handoff', 'nclex-tutor'],
  });
});

test('a category narrows a trait filter', () => {
  assert.deepEqual(after(IDLE, { type: 'trait', trait: 'nurses', on: true }, { type: 'category', category: 'Education / NCLEX' }), {
    kind: 'filtering',
    filters: { query: '', category: 'Education / NCLEX', traits: ['nurses'] },
    visible: ['nclex-tutor'],
  });
});

test('turning a trait on twice keeps one copy of it', () => {
  const on = /** @type {const} */ ({ type: 'trait', trait: 'hipaa', on: true });
  assert.deepEqual(after(IDLE, on, on), {
    kind: 'filtering',
    filters: { query: '', category: null, traits: ['hipaa'] },
    visible: ['sully'],
  });
});

test('turning the last trait off returns to idle', () => {
  assert.deepEqual(after(IDLE, { type: 'trait', trait: 'hipaa', on: true }, { type: 'trait', trait: 'hipaa', on: false }), { kind: 'idle' });
});

test('a query matches trimmed and case-insensitive', () => {
  assert.deepEqual(after(IDLE, { type: 'query', text: '  NCLEX ' }), {
    kind: 'filtering',
    filters: { query: '  NCLEX ', category: null, traits: [] },
    visible: ['nclex-tutor'],
  });
});

test('a query no row contains is empty', () => {
  assert.deepEqual(after(IDLE, { type: 'query', text: 'sepsis' }), {
    kind: 'empty',
    filters: { query: 'sepsis', category: null, traits: [] },
  });
});

test('a blank query with no other filter is idle', () => {
  assert.deepEqual(after(IDLE, { type: 'query', text: '   ' }), { kind: 'idle' });
});

test('clear from empty returns to idle', () => {
  assert.deepEqual(after(IDLE, { type: 'query', text: 'sepsis' }, { type: 'clear' }), { kind: 'idle' });
});

test('drive renders once per change and skips an event that leaves the catalog idle', async () => {
  /** @type {string[]} */
  const seen = [];
  const catalog = drive(catalogMachine(items), (s) => seen.push(s.kind));
  await catalog.send({ type: 'clear' });
  await catalog.send({ type: 'category', category: 'Ambient documentation' });
  await catalog.send({ type: 'query', text: 'sepsis' });
  await catalog.send({ type: 'clear' });
  assert.deepEqual(seen, ['idle', 'filtering', 'empty', 'idle']);
});
