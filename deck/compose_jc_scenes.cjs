// JustCook scenic mockups for the deck (owner, 2026-11-11: "qualche mockup scenico"): box renders + final screens on the
// warm ground of the site covers (#e9e3d6), no hands. node deck/compose_jc_scenes.cjs → deck/assets/justcook/scene-*.jpg
const sharp = require('sharp');
const A = 'src/assets/projects/justcook/', OUT = 'deck/assets/justcook/';
const W = 2400, H = 1350, BG = '#e9e3d6';
const shadow = (w, h, o = 0.28) => Buffer.from(`<svg width="${w}" height="${h}"><defs><filter id="b"><feGaussianBlur stdDeviation="${h / 5}"/></filter></defs><ellipse cx="${w / 2}" cy="${h / 2}" rx="${w / 2.6}" ry="${h / 4.2}" fill="rgba(60,45,25,${o})" filter="url(#b)"/></svg>`);
async function img(f, h) { const b = await sharp(A + f).resize({ height: h }).toBuffer(); const m = await sharp(b).metadata(); return { b, w: m.width, h: m.height }; }
async function scene(name, items) {
  const layers = [];
  for (const it of items) {
    const im = await img(it.f, it.h);
    const left = Math.round(it.cx - im.w / 2), top = Math.round(it.base - im.h);
    const sw = Math.round(im.w * (it.sw || 1.1)), sh = Math.round(im.h * 0.16);
    layers.push({ input: shadow(sw, sh, it.so), left: Math.round(it.cx - sw / 2), top: Math.round(it.base - sh / 2 - 4) });
    layers.push({ input: im.b, left, top });
  }
  await sharp({ create: { width: W, height: H, channels: 3, background: BG } }).composite(layers).jpeg({ quality: 86 }).toFile(OUT + name);
  console.log(name);
}
(async () => {
  // The week: four boxes, tonight's plan in the middle.
  await scene('scene-week.jpg', [
    { f: 'boxes/box-a-3q.png', h: 520, cx: 330, base: 1150 }, { f: 'boxes/box-b-3q.png', h: 520, cx: 730, base: 1190 },
    { f: 'boxes/box-c-3q.png', h: 520, cx: 1680, base: 1190 }, { f: 'boxes/box-d-3q.png', h: 520, cx: 2080, base: 1150 },
    { f: 'screens/home-first-screen.png', h: 1100, cx: 1205, base: 1250, sw: 1.3, so: 0.34 },
  ]);
  // Tonight: the code from the lid, the box, focus mode.
  await scene('scene-tonight.jpg', [
    { f: 'screens/lid-code.png', h: 1100, cx: 560, base: 1250, sw: 1.3, so: 0.34 },
    { f: 'boxes/box-d-3q.png', h: 640, cx: 1220, base: 1200, sw: 1.15 },
    { f: 'screens/focus-mode.png', h: 1100, cx: 1860, base: 1250, sw: 1.3, so: 0.34 },
  ]);
})();
