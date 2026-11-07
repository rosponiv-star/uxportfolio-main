// Saves every schema on its own, without the slide's kicker, headline or captions (owner, 2026-10-30), into the
// project's Media folder: Media/05-AuraWake/Schemi/, Media/01-JustCook/Schemi/ (git-ignored, the owner's folders).
// Run after any change, from the repo root:
//   node deck/export_schemas.mjs
// Each entry: the file name, the slide it lives on and the element that IS the schema. PNGs at 2× (3840 px wide
// for a full-width schema). Renders (scenes, exploded) are copied as they are; a numbered version is shot too.
import puppeteer from 'puppeteer-core';
import fs from 'fs';
import path from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const MEDIA = path.join(here, '..', 'Media');
const AW = path.join(MEDIA, '05-AuraWake', 'Schemi'), JC = path.join(MEDIA, '01-JustCook', 'Schemi');
const SH = path.join(MEDIA, '03-Smart Home Ecosystem', 'Schemi');
for (const d of [AW, JC, SH]) fs.mkdirSync(d, { recursive: true });

const SHOTS = [   // [folder, file, selector] — the selector is the schema itself, nothing around it
  // Smart Home Hub research boards live in shadow roots (deck/boards): 'host >> selector' shoots inside one
  [SH, '00-indice-ricerca', 'shb-s0i-index >> .slide'],
  [SH, '01-stakeholder', 'shb-s00-stakeholders >> #s'],
  [SH, '02-artifact-model', 'shb-s0a-artifact >> #m'],
  [SH, '03-sequence-flow-sette-modelli', 'shb-s04-sequence-all >> #m'],
  [SH, '03-sequence-flow-entrare-in-casa', 'shb-s05-sequence-enter >> .cols'],
  [SH, '04-physical-model-spaccato', 'shb-s01-physical-cut >> .slide'],
  [SH, '04-physical-model-pianta', 'shb-s02-physical-top >> .slide'],
  [SH, '04-physical-model-esterno-zone', 'shb-s03-physical-views >> .slide'],
  [SH, '05-pain-point-per-persona', 'shb-s06-pain-points >> .m'],
  [SH, '06-personas', 'shb-s07-personas >> .slide'],
  [SH, '06-personas-giorgia', 'shb-s08-giorgia >> .slide'],
  [SH, '07-personas-a-confronto', '#p01-framing .arch'],
  [SH, '08-sistema-degli-accessi', '#p01-system [data-shh="sys"]'],
  [JC, '01-sistema-app-e-box', '#p02-system [data-jcflow]'],
  [JC, '02-cicli-di-riformulazione', '#p02-ideas ol.cells'],
  [JC, '03-insight', '#p02-insights ol.cells'],
  [JC, '04-archetipi', '#p02-framing .arch'],
  [JC, '05-ricerca-numeri', '#p02-research .cells'],
  [JC, '06-prototipo-corso-2025', '#p02-prototypes .iter:nth-of-type(1)'],
  [JC, '07-design-finale', '#p02-prototypes .iter:nth-of-type(2)'],
  [AW, '01-sistema', '#p05-system [data-iso]'],
  [AW, '02-una-notte', '#p05-night [data-night]'],
  [AW, '04-gesto-01-prendi-il-bracciale', '#p05-gestures [data-gest="1"]'],
  [AW, '04-gesto-02-palmo-tenuto-3s', '#p05-gestures [data-gest="4"]'],
  [AW, '04-gesto-03-palmo-tocco', '#p05-gestures [data-gest="2"]'],
  [AW, '04-gesto-04-rimetti-il-bracciale', '#p05-gestures [data-gest="3"]'],
  [AW, '05-linguaggio-della-luce', '#p05-light [data-waves]'],
  [AW, '07-esploso-render-numerato', '#p05-inside [data-explode-real]'],
  [AW, '08-fallimento-sicuro', '#p05-app [data-failsafe]'],
];
const COPIES = [  // [folder, file, source in deck/assets/aurawake] — clean images, no numbers or text
  [AW, '03-scenario-1-2200.jpg', 'room1.jpg'], [AW, '03-scenario-2-2240.jpg', 'room2.jpg'], [AW, '03-scenario-3-0312.jpg', 'room3.jpg'],
  [AW, '03-scenario-4-0614.jpg', 'room4.jpg'], [AW, '03-scenario-5-0616.jpg', 'room5.jpg'],
  [AW, '00-copertina-disegno.png', 'cover-sketch.png'],   // the cover drawing alone (transparent), node deck/export_cover.mjs
  [AW, '06-esploso-linee.png', 'iso-explode.png'],   // the line drawing is off the deck (2026-11-02); 06-esploso-linee-numerato.png stays from its last export [AW, '07-esploso-render.jpg', 'explode-real.jpg'],
];

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe',
  headless: true, args: ['--allow-file-access-from-files'],
});
const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
await page.goto(pathToFileURL(path.join(here, 'index.html')).href, { waitUntil: 'networkidle0' });
await page.evaluate(() => document.fonts.ready);
for (const [dest, name, sel] of SHOTS) {
  const [host, inner] = sel.split(' >> ');
  const el = inner
    ? (await page.evaluateHandle((h, q) => document.getElementById(h)?.shadowRoot?.querySelector(q), host, inner)).asElement()
    : await page.$(sel);
  if (!el) { console.log('missing', sel); continue; }
  try { await el.screenshot({ path: path.join(dest, `${name}.png`), omitBackground: false }); console.log(name); }
  catch (e) { console.log('skipped (file open elsewhere?)', name, e.code); }   // a locked file must not stop the rest
}
await browser.close();
for (const [dest, name, src] of COPIES) {
  const from = path.join(here, 'assets', 'aurawake', src);
  if (fs.existsSync(from)) { fs.copyFileSync(from, path.join(dest, name)); console.log(name); } else console.log('missing', src);
}
