// Smart Home Hub research boards: each deck/boards/<id>.html is a standalone 1920×1080 board (its own CSS and
// script). This copies them into deck/index.html as <template class="shb"> next to their slide; the loader in
// index.html mounts each one in a shadow root, so the board's CSS can't leak into the deck and its text stays live.
//   node deck/boards/embed.mjs        (then node deck/build.mjs)
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
const indexPath = path.join(here, '..', 'index.html');
let index = fs.readFileSync(indexPath, 'utf8');

for (const file of fs.readdirSync(here).filter((f) => f.endsWith('.html'))) {
  const id = file.replace(/\.html$/, '');
  let src = fs.readFileSync(path.join(here, file), 'utf8');
  const style = [...src.matchAll(/<style>([\s\S]*?)<\/style>/g)].map((m) => m[1]).join('\n')
    .replace(/@font-face\s*{[^}]*}/g, '')                      // the deck already loads Geist
    .replace(/html\s*,\s*body\s*{/g, ':host {')
    .replace(/:root\b/g, ':host');                              // tokens such as --sig live on the host
  const body = src.slice(src.indexOf('<body>') + 6, src.lastIndexOf('</body>'))
    .replace(/<script>/g, '<script type="text/shb">');          // run by the loader, not on clone
  const tpl = `<template class="shb" data-host="shb-${id}"><style>:host { all: initial; display: block; position: absolute; inset: 0; } /* nothing inherited from the deck: the board looks as it does on its own */
${style}</style>${body}</template>`;
  const re = new RegExp(`<!-- shb:${id} -->[\\s\\S]*?<!-- /shb:${id} -->`);
  if (!re.test(index)) { console.warn(`no marker for ${id} in index.html`); continue; }
  index = index.replace(re, () => `<!-- shb:${id} -->${tpl}<!-- /shb:${id} -->`);
}
fs.writeFileSync(indexPath, index);
console.log('boards embedded');
