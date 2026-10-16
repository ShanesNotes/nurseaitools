// @ts-check

/** @import { Machine } from './fsm.js' */

/**
 * @typedef {object} CatalogItem
 * @property {string} id
 * @property {string} category
 * @property {string} text
 * @property {readonly string[]} traits
 */

/**
 * @typedef {object} Filters
 * @property {string} query
 * @property {string | null} category
 * @property {readonly string[]} traits
 */

/**
 * @typedef {{ readonly kind: 'idle' }
 *   | { readonly kind: 'filtering', readonly filters: Filters, readonly visible: readonly [string, ...string[]] }
 *   | { readonly kind: 'empty', readonly filters: Filters }} CatalogState
 */

/**
 * @typedef {{ readonly type: 'query', readonly text: string }
 *   | { readonly type: 'category', readonly category: string | null }
 *   | { readonly type: 'trait', readonly trait: string, readonly on: boolean }
 *   | { readonly type: 'clear' }} CatalogEvent
 */

/** @type {Filters} */
const NO_FILTERS = { query: '', category: null, traits: [] };

/** @type {CatalogState} */
const IDLE = { kind: 'idle' };

/**
 * @param {readonly CatalogItem[]} items
 * @returns {Machine<CatalogState, CatalogEvent>}
 */
export function catalogMachine(items) {
  return {
    initial: IDLE,
    next: (state, event) => classify(items, apply(filtersOf(state), event)),
    enter: () => null,
  };
}

/**
 * @param {CatalogState} state
 * @returns {Filters}
 */
export function filtersOf(state) {
  return state.kind === 'idle' ? NO_FILTERS : state.filters;
}

/**
 * @param {Filters} filters
 * @param {CatalogEvent} event
 * @returns {Filters}
 */
function apply(filters, event) {
  switch (event.type) {
    case 'query':
      return { ...filters, query: event.text };
    case 'category':
      return { ...filters, category: event.category };
    case 'trait': {
      const others = filters.traits.filter((trait) => trait !== event.trait);
      return { ...filters, traits: event.on ? [...others, event.trait] : others };
    }
    case 'clear':
      return NO_FILTERS;
    default:
      return /** @type {never} */ (event);
  }
}

/**
 * @param {readonly CatalogItem[]} items
 * @param {Filters} filters
 * @returns {CatalogState}
 */
function classify(items, filters) {
  if (!isActive(filters)) return IDLE;
  const [first, ...rest] = items.filter((item) => matches(item, filters)).map((item) => item.id);
  return first === undefined ? { kind: 'empty', filters } : { kind: 'filtering', filters, visible: [first, ...rest] };
}

/**
 * @param {Filters} filters
 * @returns {boolean}
 */
function isActive(filters) {
  return filters.query.trim() !== '' || filters.category !== null || filters.traits.length > 0;
}

/**
 * @param {CatalogItem} item
 * @param {Filters} filters
 * @returns {boolean}
 */
function matches(item, filters) {
  return (
    (filters.category === null || item.category === filters.category) &&
    item.text.toLowerCase().includes(filters.query.trim().toLowerCase()) &&
    filters.traits.every((trait) => item.traits.includes(trait))
  );
}
