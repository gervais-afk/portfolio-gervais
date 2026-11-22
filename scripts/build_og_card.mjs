// Render scripts/og-card.html to assets/images/og-card.png (1200×630) with a local Edge/Chrome.
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath, pathToFileURL} from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const browsers = [
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe'
];
const exe = browsers.find(file => fs.existsSync(file));
if (!exe) throw new Error('Edge or Chrome is required');
const out = path.join(root, 'assets/images/og-card.png');
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'og-card-'));
execFileSync(exe, ['--headless=new', '--user-data-dir=' + profile, '--no-first-run', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
  '--allow-file-access-from-files', '--virtual-time-budget=3000', '--window-size=1200,630',
  '--screenshot=' + out, pathToFileURL(path.join(root, 'scripts/og-card.html')).href], {stdio: 'ignore', timeout: 60000});
try { fs.rmSync(profile, {recursive: true, force: true, maxRetries: 5, retryDelay: 300}); } catch { /* browser may still hold the temp profile */ }
console.log('Wrote ' + out + ' (' + fs.statSync(out).size + ' bytes)');
