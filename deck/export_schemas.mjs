// Saves every AuraWake schema on its own, without the slide's kicker, headline or captions (owner, 2026-10-30), into
// Media/05-AuraWake/Schemi/ (git-ignored, the owner's folder). Run after any change, from the repo root:
//   node deck/export_schemas.mjs
// Each entry: the file name, the slide it lives on and the element that IS the schema. PNGs at 2× (3840 px wide
// for a full-width schema). Renders (scenes, exploded) are copied as they are; a numbered version is shot too.
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const dest = path.join(here, '..', 'Media', '05-AuraWake', 'Schemi');
fs.mkdirSync(dest, { recursive: true });

const SHOTS = [   // [file, selector] — the selector is the schema itself, nothing around it
  ['01-sistema', '#p05-system [data-iso]'],
  ['02-una-notte', '#p05-night [data-night]'],
  ['04-gesto-01-prendi-il-bracciale', '#p05-gestures [data-gest="1"]'],
  ['04-gesto-02-palmo-tenuto-3s', '#p05-gestures [data-gest="4"]'],
  ['04-gesto-03-palmo-tocco', '#p05-gestures [data-gest="2"]'],
  ['04-gesto-04-rimetti-il-bracciale', '#p05-gestures [data-gest="3"]'],
  ['05-linguaggio-della-luce', '#p05-light [data-waves]'],
  ['06-esploso-linee-numerato', '#p05-inside [data-explode]'],
  ['07-esploso-render-numerato', '#p05-inside-real [data-explode-real]'],
  ['08-fallimento-sicuro', '#p05-app [data-failsafe]'],
];
const COPIES = [  // [file, source in deck/assets/aurawake] — clean images, no numbers or text
  ['03-scenario-1-2200.jpg', 'room1.jpg'], ['03-scenario-2-2240.jpg', 'room2.jpg'], ['03-scenario-3-0312.jpg', 'room3.jpg'],
  ['03-scenario-4-0614.jpg', 'room4.jpg'], ['03-scenario-5-0616.jpg', 'room5.jpg'],
  ['06-esploso-linee.png', 'iso-explode.png'], ['07-esploso-render.jpg', 'explode-real.jpg'],
];

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--allow-file-access-from-files'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
await page.goto(pathToFileURL(path.join(here, 'index.html')).href, { waitUntil: 'networkidle0' });
await page.evaluate(() => document.fonts.ready);
for (const [name, sel] of SHOTS) {
  const el = await page.$(sel);
  if (!el) { console.log('missing', sel); continue; }
  await el.screenshot({ path: path.join(dest, `${name}.png`), omitBackground: false });
  console.log(name);
}
await browser.close();
for (const [name, src] of COPIES) {
  const from = path.join(here, 'assets', 'aurawake', src);
  if (fs.existsSync(from)) { fs.copyFileSync(from, path.join(dest, name)); console.log(name); } else console.log('missing', src);
}
