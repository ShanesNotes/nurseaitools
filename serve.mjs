// Local preview: serves dist/worker.js on :8787 with a stub DB (no Kit key, so nothing leaves the box).
import http from 'node:http';
const { default: worker } = await import(new URL('./dist/worker.js?' + Date.now(), import.meta.url));
const DB = { prepare: () => ({ bind: () => ({ run: async () => ({}) }) }) };
http.createServer(async (req, res) => {
  const chunks = []; for await (const c of req) chunks.push(c);
  const r = await worker.fetch(new Request('http://localhost:8787' + req.url, { method: req.method, headers: req.headers, body: req.method === 'POST' ? Buffer.concat(chunks) : undefined }), { DB }, { waitUntil() {} });
  res.writeHead(r.status, Object.fromEntries(r.headers)); res.end(Buffer.from(await r.arrayBuffer()));
}).listen(8787, () => console.log('http://localhost:8787'));
