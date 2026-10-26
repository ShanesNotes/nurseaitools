// Serves the local build for the e2e suite the same way verify.py does:
// a fresh local D1 in a temp dir, seeded from schema.sql, and wrangler dev --local on 127.0.0.1.
// Cloudflare and Kit credentials are removed from the env, so nothing here can reach a remote account.
import { spawn, spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const port = process.env.E2E_PORT || '8812';
const env = Object.fromEntries(Object.entries(process.env).filter(([k]) => !/^(CF_|CLOUDFLARE_|KIT_)/.test(k)));
env.WRANGLER_SEND_METRICS = 'false';

const persist = mkdtempSync(join(tmpdir(), 'nai-e2e-d1-'));
writeFileSync(join(tmpdir(), `nai-e2e-${port}.persist`), persist);
const seed = spawnSync('npx', ['wrangler', 'd1', 'execute', 'nurseaitools', '--local', '--persist-to', persist, '--file', 'schema.sql'], { env, stdio: 'inherit' });
if (seed.status !== 0) process.exit(seed.status ?? 1);

const child = spawn('npx', ['wrangler', 'dev', '--local', '--persist-to', persist, '--ip', '127.0.0.1', '--port', port,
  '--inspector-port', String(Number(port) + 1000), '--show-interactive-dev-session=false'], { env, stdio: 'inherit' });
const stop = () => child.kill('SIGTERM');
process.on('SIGTERM', stop);
process.on('SIGINT', stop);
child.on('exit', (code) => process.exit(code ?? 0));
