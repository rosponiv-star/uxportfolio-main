// AuraWake light-language cut-outs (owner, 2026-11-02) → deck/assets/aurawake/lights/*.png: the transparent studio renders
// in deck/out/blender (also in Media/05-AuraWake/OfficialMedia/Renders/Transparent), trimmed to the object, 560 px wide;
// the four LED shots are aura.py `real <out> led plastic wide state=<green|red|night|white>`, cropped closer to the LED
// (no halo, owner 2026-11-02). Run from the repo root: node deck/export_lights.mjs
import sharp from 'sharp'; import fs from 'fs';
const S = 'deck/out/blender', O = 'deck/assets/aurawake/lights'; fs.mkdirSync(O, { recursive: true });
const JOBS = [['led-green', 'aurawake-led-green-wide-plastic.png', 1], ['led-red', 'aurawake-led-red-wide-plastic.png', 1], ['led-night', 'aurawake-led-night-wide-plastic.png', 1], ['led-white', 'aurawake-led-white-wide-plastic.png', 1],
  ['strip-night', 'aurawake-strip-night-plastic.png'], ['strip-off', 'aurawake-strip-off-plastic.png'], ['strip-dawn', 'aurawake-strip-dawn-plastic.png'], ['strip-white', 'aurawake-strip-white-plastic.png'], ['time', 'aurawake-front-ledoff-time-ringdawn-plastic.png']];
for (const [name, src, bloom] of JOBS) {
  let img = sharp(`${S}/${src}`).ensureAlpha();
  if (bloom) {   // a closer view (owner, 2026-11-02): the front with the LED, the side and the edge of the top; no halo
    img = sharp(await sharp(`${S}/${src}`).extract({ left: 850, top: 560, width: 900, height: 530 }).png().toBuffer());
  }
  const out = `${O}/${name}.png`;
  await sharp(await img.png().toBuffer()).trim({ threshold: 1 }).resize({ width: 560 }).png({ compressionLevel: 9, palette: false }).toFile(out);
  const m = await sharp(out).metadata(); console.log(name, m.width + 'x' + m.height, fs.statSync(out).size);
}
