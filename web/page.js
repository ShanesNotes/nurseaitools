// @ts-check
// Browser entry, loaded as <script type=module src="/js/page.js">. The only module that
// touches the DOM. It finds controls by data-* hooks, never by styling classes.

import { drive } from './fsm.js';
import { catalogMachine, filtersOf } from './catalog.js';
import { formMachine } from './form.js';
import { formAt } from './contract.js';

/** @import { CatalogItem, CatalogState } from './catalog.js' */
/** @import { FormState } from './form.js' */
/** @import { Fields, FormKind } from './contract.js' */

/**
 * @typedef {object} CatalogView
 * @property {HTMLElement} root
 * @property {ReadonlyMap<string, HTMLElement>} rows  by item id
 * @property {HTMLElement} count
 * @property {HTMLElement} empty
 * @property {HTMLInputElement} query
 * @property {HTMLSelectElement} category
 * @property {readonly HTMLInputElement[]} traits
 */

/**
 * @typedef {object} FormView
 * @property {HTMLFormElement} form
 * @property {HTMLElement} message
 * @property {HTMLButtonElement} button
 * @property {string} label  the button's resting text
 */

boot(document);

/** @param {Document} doc */
function boot(doc) {
  const catalog = doc.querySelector('[data-catalog]');
  if (catalog instanceof HTMLElement) bindCatalog(catalog);
  for (const form of doc.forms) {
    const kind = formAt(form.getAttribute('action') ?? '');
    if (kind) bindForm(form, kind);
  }
}

/** @param {HTMLElement} root */
function bindCatalog(root) {
  const view = readCatalogView(root);
  const items = [...view.rows.values()].map(readItem);
  const catalog = drive(catalogMachine(items), (state) => renderCatalog(view, state));

  root.addEventListener('input', (e) => {
    if (e.target === view.query) void catalog.send({ type: 'query', text: view.query.value });
  });
  root.addEventListener('change', (e) => {
    const t = e.target;
    if (t === view.category) void catalog.send({ type: 'category', category: view.category.value || null });
    else if (t instanceof HTMLInputElement && t.dataset.filterTrait) {
      void catalog.send({ type: 'trait', trait: t.dataset.filterTrait, on: t.checked });
    }
  });
  root.addEventListener('click', (e) => {
    if (e.target instanceof Element && e.target.closest('[data-filter-clear]')) void catalog.send({ type: 'clear' });
  });
}

/**
 * @param {HTMLFormElement} form
 * @param {FormKind} kind
 */
function bindForm(form, kind) {
  const view = readFormView(form);
  const machine = drive(formMachine(kind), (state) => renderForm(view, state));

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    void machine.send({ type: 'submit', fields: readFields(form) });
  });
  form.addEventListener('input', () => void machine.send({ type: 'edit' }));
}

/**
 * DOM boundary for the catalog. Throws before any render if a hook is missing, which leaves
 * the server-rendered rows visible and static.
 * @param {HTMLElement} root
 * @returns {CatalogView}
 */
function readCatalogView(root) {
  return {
    root,
    rows: new Map([...root.querySelectorAll('[data-card]')].map((el) => {
      const row = hook(el, HTMLElement);
      return [row.dataset.id ?? '', row];
    })),
    count: hook(root.querySelector('[data-catalog-count]'), HTMLElement),
    empty: hook(root.querySelector('[data-catalog-empty]'), HTMLElement),
    query: hook(root.querySelector('input[data-filter-query]'), HTMLInputElement),
    category: hook(root.querySelector('select[data-filter-category]'), HTMLSelectElement),
    traits: [...root.querySelectorAll('input[data-filter-trait]')].map((box) => hook(box, HTMLInputElement)),
  };
}

/**
 * @template {Element} T
 * @param {Element | null} el
 * @param {new () => T} type
 * @returns {T}
 */
function hook(el, type) {
  if (!(el instanceof type)) throw new Error(`missing ${type.name} hook`);
  return el;
}

/**
 * @param {HTMLElement} row
 * @returns {CatalogItem}
 */
function readItem(row) {
  return {
    id: row.dataset.id ?? '',
    category: row.dataset.category ?? '',
    text: (row.dataset.text ?? '').toLowerCase(),
    traits: (row.dataset.traits ?? '').split(' ').filter(Boolean),
  };
}

/**
 * @param {HTMLFormElement} form
 * @returns {FormView}
 */
function readFormView(form) {
  const button = hook(form.querySelector('button'), HTMLButtonElement);
  return { form, button, label: button.textContent ?? '', message: hook(form.querySelector('[data-form-message]'), HTMLElement) };
}

/**
 * @param {HTMLFormElement} form
 * @returns {Fields}
 */
function readFields(form) {
  return Object.fromEntries([...new FormData(form)].map(([name, value]) => [name, typeof value === 'string' ? value : '']));
}

/**
 * @param {CatalogView} view
 * @param {CatalogState} state
 */
function renderCatalog(view, state) {
  const filters = filtersOf(state);
  const shown = state.kind === 'filtering' ? new Set(state.visible) : null;
  const total = view.rows.size;
  view.root.dataset.state = state.kind;
  for (const [id, row] of view.rows) row.hidden = state.kind === 'empty' || (shown !== null && !shown.has(id));
  view.count.textContent = state.kind === 'idle' ? `${total} tools` : `${shown?.size ?? 0} of ${total} tools`;
  view.empty.hidden = state.kind !== 'empty';
  if (view.query.value.trim() !== filters.query.trim()) view.query.value = filters.query;
  view.category.value = filters.category ?? '';
  for (const box of view.traits) box.checked = filters.traits.includes(box.dataset.filterTrait ?? '');
}

/**
 * @param {FormView} view
 * @param {FormState} state
 */
function renderForm(view, state) {
  const busy = state.kind === 'validating' || state.kind === 'submitting';
  const invalid = state.kind === 'error' ? state.invalid : [];
  view.form.dataset.state = state.kind;
  view.form.setAttribute('aria-busy', String(busy));
  view.button.disabled = busy;
  view.button.textContent = state.kind === 'submitting' ? 'Sending' : view.label;
  view.message.textContent = state.kind === 'success' || state.kind === 'error' ? state.message : '';
  if (!view.message.id) view.message.id = 'form-msg';
  for (const el of view.form.querySelectorAll('input, select, textarea')) {
    if (!isField(el) || !el.name || el.name === 'hp') continue;
    if (invalid.includes(el.name)) {
      el.setAttribute('aria-invalid', 'true');
      el.setAttribute('aria-describedby', view.message.id);
    } else {
      el.removeAttribute('aria-invalid');
      el.removeAttribute('aria-describedby');
    }
  }
  if (state.kind === 'success') view.form.reset();
}

/**
 * @param {Element} el
 * @returns {el is HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement}
 */
function isField(el) {
  return el instanceof HTMLInputElement || el instanceof HTMLTextAreaElement || el instanceof HTMLSelectElement;
}
