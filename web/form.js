// @ts-check

import { check, send } from './contract.js';

/** @import { Machine } from './fsm.js' */
/** @import { FormKind, Fields } from './contract.js' */

/**
 * @typedef {{ readonly kind: 'idle' }
 *   | { readonly kind: 'validating', readonly fields: Fields }
 *   | { readonly kind: 'submitting', readonly fields: Fields }
 *   | { readonly kind: 'success', readonly message: string }
 *   | { readonly kind: 'error', readonly message: string, readonly invalidControls: readonly string[] }} FormState
 */

/**
 * @typedef {{ readonly type: 'submit', readonly fields: Fields }
 *   | { readonly type: 'edit' }} VisitorEvent
 */

/**
 * @typedef {{ readonly type: 'valid' }
 *   | { readonly type: 'invalid', readonly error: string, readonly invalidControls: readonly string[] }
 *   | { readonly type: 'accepted', readonly message: string }
 *   | { readonly type: 'refused', readonly error: string }} EntryEvent
 */

/** @typedef {VisitorEvent | EntryEvent} FormEvent */

/** @type {FormState} */
const IDLE = { kind: 'idle' };

/**
 * @param {FormKind} kind
 * @param {readonly string[]} invalidControls
 * @param {string} error
 */
function visitorCopy(kind, invalidControls, error) {
  if (kind === 'submit') {
    const name = invalidControls.includes('name');
    const url = invalidControls.includes('url');
    if (name && url) return 'Enter a tool name and a URL that starts with http:// or https://.';
    if (name) return 'Enter the tool name.';
    if (url) return 'Enter a URL that starts with http:// or https://.';
  }
  return error;
}

/**
 * @param {FormKind} kind
 * @param {typeof fetch} [fetchImpl]
 * @returns {Machine<FormState, FormEvent>}
 */
export function formMachine(kind, fetchImpl = globalThis.fetch) {
  return {
    initial: IDLE,
    next(state, event) {
      switch (state.kind) {
        case 'idle':
          return event.type === 'submit' ? { kind: 'validating', fields: event.fields } : state;
        case 'validating':
          if (event.type === 'valid') return { kind: 'submitting', fields: state.fields };
          if (event.type === 'invalid') return { kind: 'error', message: event.error, invalidControls: event.invalidControls };
          return state;
        case 'submitting':
          if (event.type === 'accepted') return { kind: 'success', message: event.message };
          if (event.type === 'refused') return { kind: 'error', message: event.error, invalidControls: [] };
          return state;
        case 'success':
        case 'error':
          if (event.type === 'submit') return { kind: 'validating', fields: event.fields };
          if (event.type === 'edit') return IDLE;
          return state;
        default:
          return /** @type {never} */ (state);
      }
    },
    enter(state) {
      switch (state.kind) {
        case 'validating': {
          const checked = check(kind, state.fields);
          if (checked.ok) return { type: 'valid' };
          const invalidControls = checked.invalidControls ?? [];
          return { type: 'invalid', error: visitorCopy(kind, invalidControls, checked.error), invalidControls };
        }
        case 'submitting':
          return send(kind, state.fields, fetchImpl).then((reply) =>
            reply.ok ? { type: 'accepted', message: reply.message } : { type: 'refused', error: reply.error },
          );
        default:
          return null;
      }
    },
  };
}
