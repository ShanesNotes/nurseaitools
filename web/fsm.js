// @ts-check

/**
 * @template {{ readonly kind: string }} S
 * @template E
 * @typedef {object} Machine
 * @property {S} initial  a resting state: enter(initial) returns null
 * @property {(state: S, event: E) => S} next
 *   Pure and total. Returns `state` itself when `event` does not apply in `state`.
 * @property {(state: S) => E | Promise<E> | null} enter
 *   The work a state starts, as the event that ends it. Null means the state waits for the
 *   visitor. A returned promise must not reject.
 */

/**
 * @template {{ readonly kind: string }} S
 * @template E
 * @typedef {object} Running
 * @property {() => S} current
 * @property {(event: E) => Promise<S>} send
 *   Resolves with the state once this event's entry work has finished and the machine rests.
 *   An ignored event resolves with the current state at once.
 */

/**
 * @template {{ readonly kind: string }} S
 * @template E
 * @param {Machine<S, E>} machine
 * @param {(state: S) => void} onState
 * @returns {Running<S, E>}
 */
export function drive(machine, onState) {
  let state = machine.initial;
  onState(state);

  /**
   * @param {E} event
   * @returns {Promise<S>}
   */
  async function send(event) {
    const next = machine.next(state, event);
    if (next === state) return state;
    const entered = next.kind !== state.kind;
    state = next;
    onState(next);
    const work = entered ? machine.enter(next) : null;
    if (work === null) return next;
    return send(work instanceof Promise ? await work : work);
  }

  return { current: () => state, send };
}
