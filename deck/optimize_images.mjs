// Lighter PDF (owner, 2026-11-02: "solo se la perdita di qualità è impercettibile"). Chrome puts JPEGs into the PDF as
// they are, while PNGs go in as raw pixels: so every PNG with no transparency becomes a JPEG (mozjpeg q90, 4:4:4: no
// colour blur on text or thin lines), only when that saves at least 25 %; references in index.html / deck.css follow.
// PNGs with transparency stay PNG (lossless) but are scaled down to twice the size they are shown at, when they are
// larger than that (deck/out/_shown.json: the widest each image is drawn on any slide, measured in Chrome).
// Re-run after any asset is re-exported. Check afterwards: node deck/compare_previews.mjs <before-dir>
// Run from the repo root: node deck/optimize_images.mjs
import sharp from 'sharp';
import fs from 'fs';
const FILES = ['deck/index.html', 'deck/deck.css'];
const text = FILES.map((f) => fs.readFileSync(f, 'utf8')).join('\n');
const used = [...new Set(text.match(/assets\/[^"'`) ]+?\.png/g) || [])];
let saved = 0; const done = [];
for (const rel of used) {
  const p = `deck/${rel}`; if (!fs.existsSync(p)) continue;
  const m = await sharp(p).metadata();
  if (m.hasAlpha && !(await sharp(p).stats()).isOpaque) continue;              // transparency: keep the PNG
  const jpg = await sharp(p).flatten({ background: '#ffffff' }).jpeg({ quality: 90, mozjpeg: true, chromaSubsampling: '4:4:4' }).toBuffer();
  const sz = fs.statSync(p).size; if (jpg.length > sz * 0.75) continue;
  const relJ = rel.replace(/\.png$/, '.jpg'); if (fs.existsSync(`deck/${relJ}`)) { console.log('skip, exists', relJ); continue; }
  fs.writeFileSync(`deck/${relJ}`, jpg); fs.unlinkSync(p);
  saved += sz - jpg.length; done.push([rel, relJ]);
}
// transparent PNGs: down to 2× their shown width (lossless; the PDF keeps every pixel of an image, shown or not)
const shown = await (async () => {
  const puppeteer = (await import('puppeteer-core')).default, path = await import('path'), { pathToFileURL } = await import('url');
  const b = await puppeteer.launch({ executablePath: process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe', args: ['--allow-file-access-from-files'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 1920, height: 1080 });
  await pg.goto(pathToFileURL(path.resolve('deck/index.html')).href, { waitUntil: 'networkidle0' });
  const r = await pg.evaluate(() => { const o = {}; for (const im of document.querySelectorAll('img, svg image')) { const s = im.getAttribute('src') || im.getAttribute('href'), w = im.getBoundingClientRect().width; if (s && w) o[s] = Math.max(o[s] || 0, w); } return o; });
  await b.close(); return r;
})();
for (const [rel, w] of Object.entries(shown)) {
  const p = `deck/${rel}`; if (!rel.endsWith('.png') || !fs.existsSync(p)) continue;
  const m = await sharp(p).metadata(), target = Math.round(w * 2);
  if (m.width <= target * 1.1) continue;
  const sz = fs.statSync(p).size, buf = await sharp(p).resize({ width: target }).png({ compressionLevel: 9 }).toBuffer();
  fs.writeFileSync(p, buf); saved += sz - buf.length; console.log('  smaller', rel, `${m.width} → ${target} px`);
}
for (const f of FILES) { let s = fs.readFileSync(f, 'utf8'); for (const [a, b] of done) s = s.split(a).join(b); fs.writeFileSync(f, s); }
console.log(done.length, 'PNG → JPEG,', (saved / 1048576).toFixed(2), 'MB less');
done.forEach(([a]) => console.log(' ', a));
