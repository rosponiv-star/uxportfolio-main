// Builds the portfolio PDF (16:9, 1920×1080 pages) from deck/index.html, plus PNG previews.
//   node deck/build.mjs                 → deck/out/Rosponi_Valerio_Portfolio.pdf + deck/out/preview/*.png
//   node deck/build.mjs --grid          → previews with the 12-column grid drawn on top
//   node deck/build.mjs --accent=1f3c88 → override the divider accent
// Chrome path: CHROME env var, default the Windows install. File name: no hyphens or special
// characters (Politecnico upload rule); the PDF must stay under 20 MB.
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).map((a) => a.replace(/^--/, '').split('=')).map(([k, v]) => [k, v ?? true]));
const out = path.join(here, 'out');
const prev = path.join(out, args.grid ? 'preview-grid' : 'preview');
fs.rmSync(prev, { recursive: true, force: true }); // no stale previews after slides move
fs.mkdirSync(prev, { recursive: true });

const q = new URLSearchParams();
if (args.grid) q.set('grid', '');
if (args.accent) q.set('accent', args.accent);
const url = pathToFileURL(path.join(here, 'index.html')).href + (q.toString() ? `?${q}` : '');

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true,
  args: ['--allow-file-access-from-files'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });
await page.goto(url, { waitUntil: 'networkidle0' });
await page.evaluate(() => document.fonts.ready);

// Previews: one PNG per slide.
const ids = await page.$$eval('.slide', (s) => s.map((e) => e.id));
for (const [i, id] of ids.entries()) {
  const el = await page.$(`#${id}`);
  await el.screenshot({ path: path.join(prev, `${String(i + 1).padStart(2, '0')}-${id}.png`) });
}

if (!args.grid) {
  const pdf = path.join(out, 'Rosponi_Valerio_Portfolio.pdf');
  await page.emulateMediaType('print');
  await page.pdf({ path: pdf, width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
  const mb = fs.statSync(pdf).size / 1024 / 1024;
  console.log(`PDF ${ids.length} pages, ${mb.toFixed(2)} MB${mb > 20 ? '  ← OVER THE 20 MB LIMIT' : ''}`);
}
await browser.close();
console.log('previews', prev);
