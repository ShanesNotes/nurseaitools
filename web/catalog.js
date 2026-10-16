// @ts-check
// The directory filter machine. Trait and category names are opaque strings from build.py,
// so adding a filter row in Python needs no edit here.

/** @import { Machine } from './fsm.js' */

/**
 * One index row, read from its data-* attributes by page.js.
 * @typedef {object} CatalogItem
 * @property {string} id        tool slug, unique
 * @property {string} category  exact category label
 * @property {string} text      lowercase name, vendor, and description
 * @property {readonly string[]} traits  keys from build.py's TRAITS table, such as "nurses"
 */

/**
 * @typedef {object} Filters
 * @property {string} query     as typed; matching trims and lowercases it
 * @property {string | null} category  null means every category
 * @property {readonly string[]} traits  a row must carry every listed trait
 */

/**
 * idle       no filter is active, so every row shows
 * filtering  a filter is active and at least one row matches, in page order
 * empty      a filter is active and no row matches
 *
 * @typedef {{ readonly kind: 'idle' }
 *   | { readonly kind: 'filtering', readonly filters: Filters, readonly visible: readonly [string, ...string[]] }
 *   | { readonly kind: 'empty', readonly filters: Filters }} CatalogState
 */

/**
 * Every event carries the control's new value, never a toggle, so a repeated DOM event
 * lands on the same state.
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
 * Every state accepts every event: apply the event to the current filters, then classify.
 * Idle is one shared object, so an event that leaves the catalog idle is ignored by `drive`.
 * @param {readonly CatalogItem[]} items  in page order
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
 * The filters a state stands for. Idle stands for no filters.
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
 * The only place a CatalogState is built.
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
 * Active means a non-blank query, a category, or at least one trait.
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
    item.text.includes(filters.query.trim().toLowerCase()) &&
    filters.traits.every((trait) => item.traits.includes(trait))
  );
}
