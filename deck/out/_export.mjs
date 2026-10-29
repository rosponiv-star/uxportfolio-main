// Final AuraWake renders → deck/assets/aurawake (views/*.jpg, render-*.jpg) and Media/…/Renders (+ Transparent/).
// Run from deck/: node out/_export.mjs
import sharp from 'sharp';
import fs from 'node:fs';
const SRC = 'out/blender', A = 'assets/aurawake', MEDIA = '../Media/05-AuraWake/OfficialMedia/Renders';
const jobs = fs.readFileSync(`${SRC}/final-jobs.txt`, 'utf8').trim().split('\n').map((l) => l.trim().split(/\s+/));
const RENDERS = ['front', 'back', 'persp', 'persp_back', 'lit', 'top'];
for (const [shot, , st] of jobs) {
  const state = st ? st.split('=')[1] : '', name = state ? `${shot}-${state}` : shot;
  const png = `${SRC}/aurawake-${shot}${state ? '-' + state : ''}-plastic.png`;
  const white = await sharp(png).flatten({ background: '#ffffff' }).jpeg({ quality: 92 }).toBuffer();
  if (shot === 'dawn') {
    fs.writeFileSync(`${A}/render-dawn.jpg`, white); fs.writeFileSync(`${MEDIA}/AuraWake-scene-dawn.jpg`, white); continue;
  }
  fs.writeFileSync(`${A}/views/${name}.jpg`, white);
  if (RENDERS.includes(name)) fs.writeFileSync(`${A}/render-${name}.jpg`, white);
  if (name === 'persp') fs.writeFileSync(`${A}/render-persp-plastic.jpg`, white);
  fs.writeFileSync(`${MEDIA}/AuraWake-${name}.jpg`, white);
  fs.copyFileSync(png, `${MEDIA}/Transparent/AuraWake-${name}.png`);
  console.log(name);
}
