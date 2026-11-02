// AuraWake light-language cut-outs (owner, 2026-11-02) → deck/assets/aurawake/lights/*.png: the transparent studio renders
// in deck/out/blender (also in Media/05-AuraWake/OfficialMedia/Renders/Transparent), trimmed to the object, 560 px wide;
// the four LED shots are aura.py `real <out> led plastic wide state=<green|red|night|white>`, with a soft halo of the
// LED's own colour so it reads at thumbnail size. Run from the repo root: node deck/export_lights.mjs
import sharp from 'sharp'; import fs from 'fs';
const S = 'deck/out/blender', O = 'deck/assets/aurawake/lights'; fs.mkdirSync(O, { recursive: true });
const JOBS = [['led-green', 'aurawake-led-green-wide-plastic.png', 1], ['led-red', 'aurawake-led-red-wide-plastic.png', 1], ['led-night', 'aurawake-led-night-wide-plastic.png', 1], ['led-white', 'aurawake-led-white-wide-plastic.png', 1],
  ['strip-night', 'aurawake-strip-night-plastic.png'], ['strip-off', 'aurawake-strip-off-plastic.png'], ['strip-dawn', 'aurawake-strip-dawn-plastic.png'], ['strip-white', 'aurawake-strip-white-plastic.png'], ['time', 'aurawake-time-plastic.png']];
for (const [name, src, bloom] of JOBS) {
  let img = sharp(`${S}/${src}`).ensureAlpha();
  if (bloom) {   // the LED's glow, as a camera would catch it: a soft halo of its own colour around it
    const { data, info } = await img.clone().raw().toBuffer({ resolveWithObject: true });
    const CX = 1293, CY = 910;   // the LED, same place in all four wide renders (aura.py led wide)
    let c = [0, 0, 0], best = -1;
    for (let y = CY - 6; y <= CY + 6; y++) for (let x = CX - 6; x <= CX + 6; x++) { const i = (y * info.width + x) * 4, v = data[i] + data[i + 1] + data[i + 2]; if (v > best) { best = v; c = [data[i], data[i + 1], data[i + 2]]; } }
    const mx = Math.max(...c) || 1; c = c.map((v) => Math.round(v * 255 / mx));   // its hue at full brightness
    const halo = (r, a) => Buffer.from(`<svg xmlns="http://www.w3.org/2000/svg" width="${info.width}" height="${info.height}"><defs><radialGradient id="g"><stop offset="0" stop-color="rgb(${c})" stop-opacity="${a}"/><stop offset=".35" stop-color="rgb(${c})" stop-opacity="${a * 0.35}"/><stop offset="1" stop-color="rgb(${c})" stop-opacity="0"/></radialGradient></defs><circle cx="${CX}" cy="${CY}" r="${r}" fill="url(#g)"/></svg>`);
    img = sharp(await sharp(`${S}/${src}`).ensureAlpha().composite([{ input: halo(150, 0.7), blend: 'screen' }, { input: halo(45, 1), blend: 'screen' }]).png().toBuffer());
  }
  const out = `${O}/${name}.png`;
  await sharp(await img.png().toBuffer()).trim({ threshold: 1 }).resize({ width: 560 }).png({ compressionLevel: 9, palette: false }).toFile(out);
  const m = await sharp(out).metadata(); console.log(name, m.width + 'x' + m.height, fs.statSync(out).size);
}
