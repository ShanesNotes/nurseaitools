// @ts-check
// The form wire contract. The worker imports decide, encodeReply, and formAt. The browser
// imports check and send. Endpoint paths, field rules, and reply copy live only here, so the
// client check and the server check cannot drift.

/**
 * Field values as typed, keyed by input name. A missing key reads as "".
 * @typedef {Readonly<Record<string, string>>} Fields
 */

/** @typedef {string & { readonly __brand: 'Email' }} Email */
/** @typedef {string & { readonly __brand: 'HttpUrl' }} HttpUrl */

/**
 * A validated row. Only `check` builds one, so nothing can store unchecked input.
 * @typedef {{ readonly kind: 'subscriber', readonly email: Email }
 *   | { readonly kind: 'submission', readonly name: string, readonly url: HttpUrl,
 *       readonly category: string, readonly notes: string, readonly email: string }} Entry
 */

/**
 * The outcome the visitor sees. Status 200 carries `message`, status 400 carries `error`.
 * @typedef {{ readonly ok: true, readonly message: string }
 *   | { readonly ok: false, readonly error: string }} Reply
 */

/**
 * @template T
 * @typedef {{ readonly ok: true, readonly value: T }
 *   | { readonly ok: false, readonly error: string, readonly invalid?: readonly string[] }} Checked
 */

/**
 * What the worker does with one POST. A refusal never saves. An accepted reply saves its
 * entry, except on the honeypot path where `save` is null.
 * @typedef {{ readonly reply: Extract<Reply, { ok: false }>, readonly save: null }
 *   | { readonly reply: Extract<Reply, { ok: true }>, readonly save: Entry | null }} Decision
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
const TRAPPED = 'Thanks!';
const UNREACHABLE = "We couldn't reach the server. Check your connection and try again.";
const FAILED = 'Something went wrong.';
const BAD_EMAIL = 'Please enter a valid email.';
const BAD_TOOL = 'Tool name and a valid URL are required.';
const EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const HTTP = /^https?:\/\//;
const SEND_TIMEOUT_MS = 15000;

/**
 * Routes a worker pathname, or a form's action attribute, to its form.
 * @param {string} pathname  trailing slashes already stripped
 * @returns {FormKind | null}
 */
export function formAt(pathname) {
  return KINDS.find((kind) => FORMS[kind].path === pathname) ?? null;
}

/**
 * The single validator. The browser runs it in the `validating` state. `decide` runs it on
 * the server. Normalizing twice gives the same entry, so the client can send raw fields.
 * @param {FormKind} kind
 * @param {Fields} fields
 * @returns {Checked<Entry>}
 */
export function check(kind, fields) {
  return FORMS[kind].parse(fields);
}

/**
 * The whole server decision for one POST body. Pure, no clock, no headers, no database.
 *
 *   body is not JSON, or JSON null, a number, a boolean, or a string   refuse "Bad request"
 *   hp is non-empty                                                    accept "Thanks!", save null
 *   check(kind, fields) fails                                          refuse with its error
 *   otherwise                                                          accept, save the entry
 *
 * A JSON array is an object, so it takes the field path like the original worker did.
 * @param {FormKind} kind
 * @param {string} body  raw request text
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
 * The wire encoding of a reply. The client and the deployed site both depend on these exact
 * shapes, so they do not change.
 * @param {Reply} reply
 * @returns {Response}
 */
export function encodeReply(reply) {
  const [status, body] = reply.ok ? [200, { message: reply.message }] : [400, { error: reply.error }];
  return new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
}

/**
 * Posts raw fields as JSON to the form's endpoint and reads the reply. Never rejects. A
 * network failure or a timeout becomes a refusal with UNREACHABLE, so the error state always
 * has a message. `fetchImpl` is called as a bare function because a browser's fetch throws
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
 * Inverse of encodeReply. An unreadable body counts as an empty object, so an ok reply with no
 * message reads "Thanks!" and a failed reply with no error reads "Something went wrong.".
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
 * Trims and lowercases the email. Rejects anything outside EMAIL or longer than 200
 * characters.
 * @param {Fields} fields
 * @returns {Checked<Entry>}
 */
function parseSubscriber(fields) {
  const email = field(fields, 'email').trim().toLowerCase();
  if (email.length > 200 || !EMAIL.test(email)) return { ok: false, error: BAD_EMAIL, invalid: ['email'] };
  return { ok: true, value: { kind: 'subscriber', email: /** @type {Email} */ (email) } };
}

/**
 * name is trimmed, cut to 200, and must be non-empty. url is trimmed, cut to 500, and must
 * start with http:// or https://. category, notes, and email are cut to 100, 3000, and 200
 * and stored as given.
 * @param {Fields} fields
 * @returns {Checked<Entry>}
 */
function parseSubmission(fields) {
  const name = field(fields, 'name').trim().slice(0, 200);
  const url = field(fields, 'url').trim().slice(0, 500);
  /** @type {string[]} */
  const invalid = [];
  if (!name) invalid.push('name');
  if (!HTTP.test(url)) invalid.push('url');
  if (invalid.length) return { ok: false, error: BAD_TOOL, invalid };
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
 * Each JSON value becomes String(value || ''), the coercion the original worker applied.
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
