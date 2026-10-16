// @ts-check
// The form machine. The newsletter and the submit-a-tool form share it; `kind` picks the
// contract.

import { check, send } from './contract.js';

/** @import { Machine } from './fsm.js' */
/** @import { FormKind, Fields } from './contract.js' */

/**
 * idle        waiting for the visitor
 * validating  running check() on the fields the visitor submitted
 * submitting  one POST in flight with those fields
 * success     the server accepted; `message` is its copy
 * error       a check failure, a server refusal, or a network failure; `message` says which.
 *             `invalid` names the controls to mark. A refusal that is not a field check leaves it empty.
 *
 * @typedef {{ readonly kind: 'idle' }
 *   | { readonly kind: 'validating', readonly fields: Fields }
 *   | { readonly kind: 'submitting', readonly fields: Fields }
 *   | { readonly kind: 'success', readonly message: string }
 *   | { readonly kind: 'error', readonly message: string, readonly invalid: readonly string[] }} FormState
 */

/**
 * submit and edit come from the visitor. valid, invalid, accepted, and refused come only
 * from entry work.
 * @typedef {{ readonly type: 'submit', readonly fields: Fields }
 *   | { readonly type: 'valid' }
 *   | { readonly type: 'invalid', readonly error: string, readonly invalid: readonly string[] }
 *   | { readonly type: 'accepted', readonly message: string }
 *   | { readonly type: 'refused', readonly error: string }
 *   | { readonly type: 'edit' }} FormEvent
 */

/** @type {FormState} */
const IDLE = { kind: 'idle' };

/**
 * The sentence a check failure shows. HTTP replies keep the contract strings. A submit-form
 * failure names the field that failed. Subscribe keeps the contract sentence and still marks email.
 * @param {FormKind} kind
 * @param {readonly string[]} invalid
 * @param {string} error
 */
function visitorCopy(kind, invalid, error) {
  if (kind === 'submit') {
    const name = invalid.includes('name');
    const url = invalid.includes('url');
    if (name && url) return 'Enter a tool name and a URL that starts with http:// or https://.';
    if (name) return 'Enter the tool name.';
    if (url) return 'Enter a URL that starts with http:// or https://.';
  }
  return error;
}

/**
 * Every pair not listed returns the same state object, which is what blocks a second submit
 * while one is in flight.
 *
 *   idle, success, error   submit     validating   entry: check(kind, fields), synchronous
 *   validating             valid      submitting   entry: send(kind, fields), never rejects
 *   validating             invalid    error        message names the failed fields
 *   submitting             accepted   success
 *   submitting             refused    error        invalid is empty
 *   success, error         edit       idle
 *
 * @param {FormKind} kind
 * @param {typeof fetch} [fetchImpl]  tests pass a fake; the browser uses the global
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
          if (event.type === 'invalid') return { kind: 'error', message: event.error, invalid: event.invalid };
          return state;
        case 'submitting':
          if (event.type === 'accepted') return { kind: 'success', message: event.message };
          if (event.type === 'refused') return { kind: 'error', message: event.error, invalid: [] };
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
          const invalid = checked.invalid ?? [];
          return { type: 'invalid', error: visitorCopy(kind, invalid, checked.error), invalid };
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
