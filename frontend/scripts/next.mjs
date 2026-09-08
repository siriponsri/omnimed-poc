import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const args = process.argv.slice(2).filter(a => a !== '--strictPort').map(a => a === '--host' ? '--hostname' : a);
if (!args.includes('--hostname') && ['dev','start'].includes(args[0])) args.push('--hostname','127.0.0.1');
const cli = fileURLToPath(new URL('../node_modules/next/dist/bin/next', import.meta.url));
const child = spawn(process.execPath, [cli, ...args], { stdio: 'inherit', env: { ...process.env, NEXT_TELEMETRY_DISABLED: '1' } });
child.on('error', () => process.exit(1));
child.on('exit', code => process.exit(code ?? 1));
for (const signal of ['SIGINT','SIGTERM']) process.on(signal, () => child.kill(signal));
