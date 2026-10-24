// Local preview: serves dist/worker.js on :8787 (or $PORT) with a stub DB (no Kit key, so nothing leaves the box).
import http from 'node:http';
const { default: worker } = await import(new URL('./dist/worker.js?' + Date.now(), import.meta.url));
const PORT = Number(process.env.PORT) || 8787;
const DB = { prepare: () => ({ bind: () => ({ run: async () => ({}) }) }) };
http.createServer(async (req, res) => {
  const chunks = []; for await (const c of req) chunks.push(c);
  const r = await worker.fetch(new Request(`http://localhost:${PORT}` + req.url, { method: req.method, headers: req.headers, body: req.method === 'POST' ? Buffer.concat(chunks) : undefined }), { DB }, { waitUntil() {} });
  res.writeHead(r.status, Object.fromEntries(r.headers)); res.end(Buffer.from(await r.arrayBuffer()));
}).listen(PORT, () => console.log(`http://localhost:${PORT}`));
