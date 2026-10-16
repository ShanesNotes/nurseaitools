// @ts-check

/**
 * @typedef {Readonly<Record<string, string>>} Fields
 */

/** @typedef {string & { readonly __brand: 'Email' }} Email */
/** @typedef {string & { readonly __brand: 'HttpUrl' }} HttpUrl */

/**
 * @typedef {{ readonly kind: 'subscriber', readonly email: Email }
 *   | { readonly kind: 'submission', readonly name: string, readonly url: HttpUrl,
 *       readonly category: string, readonly notes: string, readonly email: string }} Entry
 */

/**
 * @typedef {{ readonly ok: true, readonly message: string }
 *   | { readonly ok: false, readonly error: string }} Reply
 */

/**
 * @template T
 * @typedef {{ readonly ok: true, readonly value: T }
 *   | { readonly ok: false, readonly error: string, readonly invalidControls?: readonly string[] }} Checked
 */

/**
 * @typedef {{ readonly reply: Extract<Reply, { ok: false }>, readonly save: null }
 *   | { readonly reply: Extract<Reply, { ok: true }>, readonly save: Entry }
 *   | { readonly reply: { readonly ok: true, readonly message: 'Thanks!' }, readonly save: null }} Decision
 */

/**
 * @typedef {object} FormSpec
 * @property {string} path
 * @property {string} thanks
 * @property {(fields: Fields) => Checked<Entry>} parse
 */

const FORMS = /** @satisfies {Record<string, FormSpec>} */ ({
  subscribe: { path: '/api/subscribe', thanks: "You're subscribed. Thanks!", parse: parseSubscriber },
  submit: { path: '/api/submit', thanks: 'Thanks! Your submission is in the review queue.', parse: parseSubmission },
});

/** @typedef {keyof typeof FORMS} FormKind */

const KINDS = /** @type {readonly FormKind[]} */ (Object.keys(FORMS));
const BAD_REQUEST = 'Bad request';
const TRAPPED = /** @type {'Thanks!'} */ ('Thanks!');
const UNREACHABLE = "We couldn't reach the server. Check your connection and try again.";
const FAILED = 'Something went wrong.';
const BAD_EMAIL = 'Please enter a valid email.';
const BAD_TOOL = 'Tool name and a valid URL are required.';
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const HTTP = /^https?:\/\//;
const SEND_TIMEOUT_MS = 15000;

/**
 * @param {string} pathname
 * @returns {FormKind | null}
 */
export function formAt(pathname) {
  const path = pathname.replace(/\/+$/, '') || '/';
  return KINDS.find((kind) => FORMS[kind].path === path) ?? null;
}

/**
 * @param {FormKind} kind
 * @param {Fields} fields
 * @returns {Checked<Entry>}
 */
export function check(kind, fields) {
  return FORMS[kind].parse(fields);
}

/**
 * @param {FormKind} kind
 * @param {string} body
 * @returns {Decision}
 */
export function decide(kind, body) {
  /** @type {unknown} */
  let data;
  try {
    data = JSON.parse(body);
  } catch {
    return refuse(BAD_REQUEST);
  }
  if (typeof data !== 'object' || data === null) return refuse(BAD_REQUEST);
  const fields = toFields(data);
  if (field(fields, 'hp')) return { reply: { ok: true, message: TRAPPED }, save: null };
  const checked = check(kind, fields);
  if (!checked.ok) return refuse(checked.error);
  return { reply: { ok: true, message: FORMS[kind].thanks }, save: checked.value };
}

/**
 * @param {Reply} reply
 * @returns {Response}
 */
export function encodeReply(reply) {
  const [status, body] = reply.ok ? [200, { message: reply.message }] : [400, { error: reply.error }];
  return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
}

/**
 * `fetchImpl` is called as a bare function because a browser's fetch throws
 * "Illegal invocation" when called as a method of another object.
 * @param {FormKind} kind
 * @param {Fields} fields
 * @param {typeof fetch} fetchImpl
 * @returns {Promise<Reply>}
 */
export async function send(kind, fields, fetchImpl) {
  /** @type {Response} */
  let res;
  try {
    res = await fetchImpl(FORMS[kind].path, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(fields),
      signal: AbortSignal.timeout(SEND_TIMEOUT_MS),
    });
  } catch {
    return { ok: false, error: UNREACHABLE };
  }
  return decodeReply(res);
}

/**
 * @param {Response} res
 * @returns {Promise<Reply>}
 */
async function decodeReply(res) {
  /** @type {unknown} */
  const body = await res.json().catch(() => ({}));
  if (res.ok) return { ok: true, message: textAt(body, 'message') ?? TRAPPED };
  return { ok: false, error: textAt(body, 'error') ?? FAILED };
}

/**
 * @param {Fields} fields
 * @returns {Checked<Entry>}
 */
function parseSubscriber(fields) {
  const email = field(fields, 'email').trim().toLowerCase();
  if (email.length > 200 || !EMAIL.test(email)) return { ok: false, error: BAD_EMAIL, invalidControls: ['email'] };
  return { ok: true, value: { kind: 'subscriber', email: /** @type {Email} */ (email) } };
}

/**
 * @param {Fields} fields
 * @returns {Checked<Entry>}
 */
function parseSubmission(fields) {
  const name = field(fields, 'name').trim().slice(0, 200);
  const url = field(fields, 'url').trim().slice(0, 500);
  /** @type {string[]} */
  const invalidControls = [];
  if (!name) invalidControls.push('name');
  if (!HTTP.test(url)) invalidControls.push('url');
  if (invalidControls.length) return { ok: false, error: BAD_TOOL, invalidControls };
  return {
    ok: true,
    value: {
      kind: 'submission',
      name,
      url: /** @type {HttpUrl} */ (url),
      category: field(fields, 'category').slice(0, 100),
      notes: field(fields, 'notes').slice(0, 3000),
      email: field(fields, 'email').slice(0, 200),
    },
  };
}

/**
 * @param {object} data
 * @returns {Fields}
 */
function toFields(data) {
  return Object.fromEntries(Object.entries(data).map(([name, value]) => [name, String(value || '')]));
}

/**
 * @param {Fields} fields
 * @param {string} name
 */
function field(fields, name) {
  return fields[name] ?? '';
}

/**
 * @param {unknown} body
 * @param {string} key
 * @returns {string | undefined}
 */
function textAt(body, key) {
  if (typeof body !== 'object' || body === null) return undefined;
  const value = /** @type {Record<string, unknown>} */ (body)[key];
  return typeof value === 'string' ? value : undefined;
}

/**
 * @param {string} error
 * @returns {Decision}
 */
function refuse(error) {
  return { reply: { ok: false, error }, save: null };
}
