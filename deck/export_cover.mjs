// AuraWake cover drawing (owner, 2026-11-02): the base with the bracelet on its pins, in outline, with a hint of shading
// in the cover's own ochre. Inputs (aura.py, real mode, same camera):
//   persp_band plastic showtime clock=sun ledoff outline docked   → white lines (Freestyle over holdouts)
//   persp_band plastic showtime clock=sun ledoff docked           → the shading pass: only its light is used (with the
//                                                                    grille holes: a whisper of the base's texture)
// Output: deck/assets/aurawake/cover-sketch.png (1440×810, transparent; the SVG places it as 2400×1350 × 0.48). Run from the repo root: node deck/export_cover.mjs
import sharp from 'sharp';
const S = 'deck/out/cover/aurawake-persp_band-ledoff-';
const lines = await sharp(`${S}outline-docked-timesun0630-plastic.png`).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
const shade = await sharp(`${S}docked-timesun0630-plastic.png`).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
const { width, height } = lines.info, out = Buffer.alloc(width * height * 4);
const DARK = [0x3d, 0x2a, 0x07];   // the cover's ochre, darker: shadows in the same yellow
for (let i = 0; i < out.length; i += 4) {
  const a = shade.data[i + 3] / 255, L = (0.2126 * shade.data[i] + 0.7152 * shade.data[i + 1] + 0.0722 * shade.data[i + 2]) / 255;
  let r = DARK[0], g = DARK[1], b = DARK[2], al = a * (0.06 + 0.40 * (1 - L));                  // a light veil, deeper on the dark faces
  if (L > 0.55) { const k = (L - 0.55) / 0.45; r = g = b = 255; al = a * 0.13 * k; }              // the lit top: a whisper lighter
  const la = lines.data[i + 3] / 255;                                                               // white lines on top
  const A = la + al * (1 - la);
  out[i] = A ? (255 * la + r * al * (1 - la)) / A : 0; out[i + 1] = A ? (255 * la + g * al * (1 - la)) / A : 0; out[i + 2] = A ? (255 * la + b * al * (1 - la)) / A : 0;
  out[i + 3] = Math.round(A * 255);
}
await sharp(out, { raw: { width, height, channels: 4 } }).resize({ width: 1440 }).png({ compressionLevel: 9 }).toFile('deck/assets/aurawake/cover-sketch.png');   // shown ~1150 px wide
const { info } = await sharp('deck/assets/aurawake/cover-sketch.png').trim({ threshold: 1 }).toBuffer({ resolveWithObject: true });
console.log('bounds (1440 px)', -info.trimOffsetLeft, -info.trimOffsetTop, info.width, info.height);
