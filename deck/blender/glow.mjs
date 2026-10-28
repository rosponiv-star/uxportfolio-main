// Soft camera-like glow around the front LED: only the LED's own pixels (opaque, and bright or clearly coloured) are
// blurred and screened back, so the white background never bleeds onto the body.
//   node deck/blender/glow.mjs <in.png> <out.jpg> [sigma] [tint #rrggbb]  (tint: the glow takes the state's colour)
import sharp from 'sharp';
const [src, dst, sigma = '8', tint] = process.argv.slice(2);
const T = tint ? [1, 3, 5].map((k) => parseInt(tint.slice(k, k + 2), 16)) : null;
const { data, info } = await sharp(src).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
const hl = Buffer.alloc(info.width * info.height * 3);
for (let i = 0, j = 0; i < data.length; i += 4, j += 3) {
  const r = data[i], g = data[i + 1], b = data[i + 2], a = data[i + 3], mx = Math.max(r, g, b), mn = Math.min(r, g, b);
  if (a === 255 && (mx > 225 || (mx - mn > 45 && mx > 110))) { const c = T || [r, g, b]; hl[j] = c[0]; hl[j + 1] = c[1]; hl[j + 2] = c[2]; }
}
const raw = { width: info.width, height: info.height, channels: 3 };
const g1 = await sharp(hl, { raw }).blur(+sigma).linear(2.4, 0).raw().toBuffer();
const g2 = await sharp(hl, { raw }).blur(+sigma * 3).linear(1.6, 0).raw().toBuffer();
await sharp(src).flatten({ background: '#ffffff' })
  .composite([{ input: g1, raw, blend: 'screen' }, { input: g2, raw, blend: 'screen' }]).jpeg({ quality: 92 }).toFile(dst);
