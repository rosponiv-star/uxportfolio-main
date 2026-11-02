// Compares deck/out/preview with an earlier copy of it, slide by slide (PSNR, dB; ≥ 40 dB reads as identical, ∞ = same
// pixels). Run from the repo root: node deck/compare_previews.mjs <before-dir>
import sharp from 'sharp';
import fs from 'fs';
const before = process.argv[2], now = 'deck/out/preview';
const rows = [];
for (const f of fs.readdirSync(now).filter((f) => f.endsWith('.png'))) {
  if (!fs.existsSync(`${before}/${f}`)) { rows.push([f, 'new']); continue; }
  const [a, b] = await Promise.all([sharp(`${before}/${f}`).removeAlpha().raw().toBuffer(), sharp(`${now}/${f}`).removeAlpha().raw().toBuffer()]);
  if (a.length !== b.length) { rows.push([f, 'size differs']); continue; }
  let se = 0, mx = 0; for (let i = 0; i < a.length; i++) { const d = a[i] - b[i]; se += d * d; if (Math.abs(d) > mx) mx = Math.abs(d); }
  const mse = se / a.length; rows.push([f, mse ? (10 * Math.log10(255 * 255 / mse)).toFixed(1) : '∞', mx]);
}
rows.filter((r) => r[1] !== '∞').forEach((r) => console.log(r.join('  ')));
console.log(rows.filter((r) => r[1] === '∞').length, 'slides pixel-identical of', rows.length);
