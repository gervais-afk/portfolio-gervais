// Render the French no-JavaScript fallback from the same source as the browser.
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const context = vm.createContext({window: {}});
for (const file of ['translations.js', 'renderers.js']) vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), context, {filename: file});
const data = context.window.PORTFOLIO_CONTENT.fr;
const render = context.window.PORTFOLIO_RENDER;
const blocks = Object.fromEntries(['secondary','journey','skills','articles'].map(key => [key, render[key](data)]));
for (const id of ['k1','archi','dataset']) blocks['project-' + id] = render.projectText(data, id);
const file = path.join(root, 'index.html');
let html = fs.readFileSync(file, 'utf8');
for (const [key, body] of Object.entries(blocks)) {
  const expression = new RegExp(`<!-- STATIC:${key} -->[\\s\\S]*?<!-- /STATIC:${key} -->`);
  if (!expression.test(html)) throw new Error(`Missing marker ${key}`);
  html = html.replace(expression, () => `<!-- STATIC:${key} -->\n${body}\n<!-- /STATIC:${key} -->`);
}
// data-i18n elements intentionally contain plain text only, never nested markup.
let labels = 0;
html = html.replace(/(<([a-z][\w:-]*)\b[^>]*\bdata-i18n="([^"]+)"[^>]*>)[\s\S]*?(<\/\2>)/gi, (_, open, tag, key, close) => {
  if (data.ui[key] === undefined) throw new Error(`Unknown French label ${key}`);
  labels++;
  return open + render.escape(data.ui[key]) + close;
});
html = html.replace(/<title>[\s\S]*?<\/title>/, '<title>' + render.escape(data.ui.page_title) + '</title>');
html = html.replace(/(<meta name="description" content=")[^"]*(">)/, (_, open, close) => open + render.escape(data.ui.page_description) + close);
const versionAssets = source => source.replace(/((?:src|href)=")([^"?#]+\.(?:js|css))(?:\?[^\"]*)?(\")/g, (match, open, asset, close) => {
  if (/^[a-z]+:/i.test(asset)) return match;
  const digest = createHash('sha256').update(fs.readFileSync(path.join(root, asset))).digest('hex').slice(0, 10);
  return open + asset + '?v=' + digest + close;
});
fs.writeFileSync(file, versionAssets(html));
const cvFile = path.join(root, 'cv.html');
fs.writeFileSync(cvFile, versionAssets(fs.readFileSync(cvFile, 'utf8')));
console.log(`French static fallback synchronised: ${Object.keys(blocks).length} blocks, ${labels} labels. CSS/JS cache versions updated.`);
