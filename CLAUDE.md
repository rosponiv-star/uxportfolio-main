# Valerio Rosponi — Portfolio

> New session? Read HANDOFF.md first: it has the full history, decisions, rejected ideas and open items.
> Work is split between CLOUD sessions (no `Media/`, push a `claude/*` branch) and LOCAL ones (have `Media/`, push
> `main`). Before anything, sync git as HANDOFF §00 says; after every change, add an entry to the HANDOFF §01 log.

Personal portfolio of Valerio Rosponi (UX / digital product / visual designer, junior).
The site exists to show **case studies, process and mindset** to recruiters and hiring
managers. It is not a self-promotion or "hire me" site: contact stays discreet.

The owner never edits code by hand; every change goes through Claude. Talk to him in Italian;
all site copy is in **English**.

## Stack

- Astro 7 (static output) + MDX + sitemap. No CSS framework: hand-written CSS.
- Font: Geist only, via Fontsource (self-hosted). Geist Mono was removed.
- Deploy: GitHub `rosponiv-star/uxportfolio-main` → Cloudflare (build `npm run build`, output `dist`).
  Domain: www.valeriorosponi.com.
- Note: on this machine run `astro` commands from PowerShell. In Git Bash, Rolldown's native
  binding fails to load.

## Structure

- `src/pages/index.astro`: Work page, which is also the home: near full-screen hero band (statement "Valerio Rosponi, UX and digital product designer studying…" (owner, 2026-10-12), entering word by word with the original blur-to-focus reveal (restored by the owner, 2026-10-13), centred + depth texture; at scroll 0 the Selected work header and the top ~80px of the first row of covers peek in at the bottom; --peek / --work-head in index.astro), Selected work (filters,
  Grid/Index switch, two-column grid of cards), "How I work" principles.
- `src/components/Section.astro`: the single section pattern used on every page (see "Layout system").
- `src/pages/work/[slug].astro`: case study template. The PhoneScroll device scene was removed by the owner (2026-10-03).
- `src/pages/about.astro` (owner, 2026-10-13): hero = the 12 columns drawn as hairlines + a two-sentence statement
  (graphic size exception, 36→76px) + B/W portrait that turns to colour and eases to 1.03 on hover; then five accordion sections,
  all closed, one open at a time (grid-rows 0fr→1fr; closed panels inert): approach (3 steps), skills (3 groups, 14
  skills), tools (logo tiles, Simple Icons CC0 in `src/assets/logos/`, monochrome → signal on hover), now, contact.
- `src/pages/playground.astro`, `src/pages/404.astro`.
- `src/content/projects/NN-name.mdx`: one file per case study. The `NN-` prefix is stripped from the URL.
- `src/data/site.ts`: personal info (email, LinkedIn, CV path).
- `src/styles/global.css`: tokens, type scale, motion primitives.
- `Media/`: raw source material from the owner. It is git-ignored. Copy processed assets into
  `src/assets/` (images, optimised by Astro) or `public/` (video, PDF).

## Writing a case study (MDX)

Frontmatter is validated by `src/content.config.ts`: title, order, tagline, year, type, platform,
role, timeline, team, tools, tone (placeholder cover colour), toneDark, cover {image|video, alt},
glance {problem, approach, outcome} (one short sentence each), result {text, media [{label, image?, kind: screen|wide}],
showcase?, metricsLabel, metrics}, placeholder (set to `false` once the content is real).

Page order (owner, 2026-10-03): title + tagline → cover → Overview (one cell grid, owner 2026-10-20: three cells
Problem/Approach/Outcome with the sentence pinned to the bottom, then six fact cells, three per row) →
**Result** (alt band: screens/boards, 1–2 sentences, key numbers; placeholders until images exist) → Process (`case/ProcessIndex.astro`:
a clickable index, one row per chapter: number, title (h3), the chapter `summary` (2–4 words) and a drawn arrow that stretches on hover; once it scrolls away a slim fixed bar under the header shows the steps, fills each
segment in --signal as its chapter is read and replaces the progress bar) → chapters. Recruiters must see interface and result first; the full process stays one scroll away.

Chapters: Challenge, Research, Insights (tone="alt"), Define, Ideate, Design, [Validate, only if tested], Reflection.
**Structure "B-mix" (owner, 2026-10-20, chosen from three prototypes in `notes/proposals/`):** the chapter title stays
sticky in the head lane; the body lane starts with the `<Key>` sentence (h2 size, Regular, ink: where reading starts),
then groups. A group = `### Title` rendered as an uppercase ink label, one short intro paragraph, then its content.
Numbers, findings, cycles and numbered lists are CELLS: one hairline grid across the body lane (`.cells` / `.cell` in
global.css, 6 units: third = 2, half = 3), label top-left, number or caption pinned to the bottom, consecutive cell
blocks join into one grid. Sequence numbers are small signal labels (01), never chips: the owner rejected chips of any
kind ("tolgono l'aria di editorialità"). Dense comparisons stay light (Archetypes, priority Chips: hairlines only, no
boxes or tints). Tinted `<Note>` boxes stay for the few notes worth highlighting; don't overuse them.
Text levels: Key (h2 Regular) → group label → paragraphs (read 17→19, ink-2) → cell titles (h3) → cell text (body 17)
→ numbers (stat, one size everywhere) → captions (small, grey). No filler: cut anything that doesn't carry a fact, a decision or a reason.

**One reading column (owner, 2026-10-09):** chapter text reads strictly top to bottom from the left edge of track A;
nothing is parked in track C for the eye to hunt for (notes, captions, kickers sit right under what they refer to).
A chapter is split into groups with `### Title`, rendered as an uppercase ink label (group numbers like 01.1
were tried and rejected, 2026-10-09: "troppi numeri"). Proximity carries the structure: `--space-item` before a group, `--space-3` from its heading to its
content, `--space-block` inside it. Wide media (strips, galleries, metric rows, funnels) may still span A–C.

Components available in MDX without imports:
- `<Chapter title="…" summary="2–4 words">…</Chapter>`: a numbered chapter. Title and summary feed the Process index.
- `<Key>…</Key>`: the chapter's key sentence (h2 Regular), first thing in a chapter.
- `<Note label="Decision" text="Why…">paragraph(s)</Note>`: the content it annotates, then the note
  right below it as a tinted callout on the A–B measure. Self-closing `<Note … />` renders the callout alone.
- `<Figure src={img} alt="" caption="" ratio="16/9" size="wide|text" />`: `wide` (the default) spans the
  whole body lane. Import the image at the top of the MDX file. A `video="/media/x.mp4"` prop is also
  supported.
- `<Metrics items={[{ value, label, text? }]} />`: in a chapter, a row of equal cells (number on top, label + context
  pinned to the bottom); in the Result, bare numbers on ink hairlines (unchanged). Sign/unit small (unit raised,
  leading sign centred); digits count up once (~1.2s, `case/Stat.astro`; ranges like "4–5" do not count). Use it
  wherever there are numbers, never bury them in prose.
- `<Chips label="…" intro="…" items={[{ label, note?, color?, image? }]} variant="chips|cards" />`: a light row, no
  boxes: label + one line of context on track A, the items as plain lead lines on B–C. Hover shows `note` in the cursor
  label, or `image` (e.g. the box) with the note as caption. `cards` = cells, two per row, note visible (channels).
- `<Closing kicker? line?>statement</Closing>`: the case study's last word, at the end of Reflection: the plain
  sentence as a lead-in, the **bold** sentence alone in mega size, all ink; then a hairline, the kicker and the one
  lesson to remember in h2.
- `<BoxStrip items={[{ name, role, color, image, hover?, alt }]} />`: a product line as solid colour panels (one per
  product, its own colour), the product cut-out large inside; hover cross-fades to a second view (front ↔ perspective).
- `<Features … alternate crop={0.82} />`: bigger devices that switch side row by row; items may override `crop` and take
  `anchor: 'bottom'` (widgets need ~0.3, lock-screen notifications show the bottom share).
- Gallery items may take `span: 2` (a 2×2 hero tile; the grid packs densely around it).
- `<BigStat value label source? />`: the one number a chapter hinges on, as a full-width cell (same stat size as all
  numbers), caption + source pinned to the bottom; a `<Metrics>` right after it joins the same grid.
- `<Features items={[{ title, text, image, alt }]} />`: product features as rows, each opening on a strong hairline:
  number/title/text at the top of B–C, the screen cropped and standing on the row's bottom edge in track A.
- `<Gallery groups={[{ label, kind: cutout|tile, cols?, items: [{ image, alt, caption? }] }]} />`: brand material
  (packaging cut-outs on a hairline, flyers, posts) in a tinted panel across A–C.
- Metrics also take `title` (prefer a `###` group instead) and `variant="boxed"` (tinted boxes, for a second kind of number).
  Reframes take a real cycle number `n` per item (`cycles` is accepted but no longer drawn).
- Cursor label variants (scripts/site.ts): `data-cursor` text; `data-cursor-style="note"` = sentence-case note;
  `data-cursor-image="url"` = image preview with `data-cursor` as caption. Clamped inside the viewport.
- `<Insights items={[{ title, text, stat?, statLabel? }]} />`: cells (4 = 2×2, 3 = thirds, 5 = 3 + 2): number,
  title, evidence, and the stat pinned to the bottom of the cell. `variant="compact"`: a lighter list (number + lead title on one line, text below) for plans.
- `<Reframes items={[{ client, problem, idea? }]} />`: one row of cells read left to right (subgrid keeps the fields
  aligned); earlier ideas are struck through as discarded; the last cell, the final framing, is inked in. Show ~3 key cycles.
- `<Archetypes items={[{ name, alias?, quote, traits: [{ label, text }] }]} />`: a light comparison, no boxes
  (row labels in track A, archetypes in B and C under an ink rule, hairlines between rows; optional `goal` row in h2 size, e.g. "Less
  effort" vs "Less waste"; quote in lead size). Same trait labels, same order, for both.
- `result.showcase` (frontmatter, not MDX): labelled groups of device shots rendered by `case/Showcase.astro`:
  `{ label, layout: trio|pair|quad|scene, crop?, anchor?: top|bottom, stagger?, items: [{ image, alt, caption? }] }`.
  Trio = tracks A/B/C beside the label; pair/quad = all 12 columns; scene = one wide photo (a device in its setting)
  across 12 columns; crop shows the top share of the device on a hairline, `anchor: bottom` the bottom share with the
  cut at the top (sticky bars, before/after); caption = a short field under a shot. Use cut-out device PNGs (960px).
- `<Reference logo={img} name role? text />`: a product used as a reference, as an editorial tile with its logo in
  monochrome (alpha as mask). `<SystemMap />`: Rehabeat's wiring diagram (nodes + arrows, hover lights the links).
- Showcase `duo` = two photos side by side (6 + 6 cols, stacked on phones). `<Spot image alt label?>text</Spot>`: a key
  screen in someone’s hand, photo on B–C, framing text on A sitting on a hairline at the photo’s baseline. Gallery cutout groups become swipe rows on phones.
- Showcase `scene` stays inside the 12-col grid (full-bleed 100svh + scroll zoom was tried and reverted, 2026-10-13).
- Case-study intro: back link = hairline arrow + label (role/team/timeline live only in the Overview, owner 2026-10-16).
  Every page has an Open Graph image (Base `image` prop; case studies pass their cover, default JustCook's).
- `<Todo>…</Todo>`: visible placeholder. Remove these as the real content arrives.

Cover media: put the image in `src/assets/projects/<name>/` and reference it in the frontmatter
`cover.image` with a relative path. Put looping videos (mp4/webm, muted) in `public/media/<name>/`
and use `cover.video`.

## Layout system (strict)

- 12-column grid. Every section uses `<Section>`: a full-width rule, the title in the head lane
  (cols 1–3, sticky), and the content in the body lane (cols 4–12).
- The body lane splits into three equal tracks A (4–6), B (7–9) and C (10–12) through `.trio`.
  Every element must start and end on a track edge. Running text uses the A–B measure. Boxes, figures,
  metrics and rows span A–C.
- Section separation: a rule by default, or a full-bleed tinted band (`tone="alt"` on `<Section>` or
  `<Chapter>`). Neither a band nor the section after it has a rule. Use bands sparingly: Home → How I
  work; case study → Result, Insights; About → What I bring. Keep inner rules to a
  minimum (only between repeated rows, never above the first one).
- Spacing comes only from the tokens in global.css: `--space-1…6`, `--space-block` (between blocks),
  `--space-item` (between cards) and `--space-section` (between sections).
- To verify alignment, measure element edges against the column lines in the browser (a JS audit).
  Do not judge it by eye.

## Type scale (strict)

Use only the size tokens in global.css: mega, display (30→60, page-opening statements, Geist Regular), h2 (48), h3 (28), lead (~22), body (17), small (16)
and label (12, Geist Medium uppercase, 8% tracking); read (17→19) is case-study chapter text only; stat (56→104, Medium) is for key numbers only.

Label roles (owner, 2026-10-04: never give two levels the same look): `.label` + signal = a number or step in a
sequence (01, Cycle 02); `.label.label--group` (ink) = the heading of a group (Targets for a pilot, Must-haves);
`.field` (small, grey, sentence case) = a field name inside an item (Problem, Idea, Friction) and number captions. Never hard-code a font size. The only exceptions are graphics: the cover
title, the footer wordmark and the nav micro-numbers.

- Section titles use h2. Item titles (principles, insights, rows, index) use h3. Card titles use lead (Medium).
- Running text uses body. Navigation, index, notes, captions and secondary facts use small.
- An item row (principles, insights, About rows) is always: title in track A, text in tracks B–C.

## Collections (Work and Playground)

- `components/Collection.astro` is shared by the Work page (projects) and the Playground (experiments): title,
  filters, Grid/Index switch, grid and index table. The page renders its cards in the slot, each wrapped in
  `.work__slot` (sizes from `gridSizes()` in `lib/collection.ts`). `components/Card.astro` is the generic card;
  `ProjectCard` wraps it with the project cover. Playground experiments are defined in `playground.astro`, with their
  own filter vocabulary, and their live demo is the card media.
- No project count line (removed by the owner). Covers have no corner marks.
- Dividers are translucent ink: `--rule` 8% (row hairlines), `--rule-strong` 22% (section rules).
- Small text (filters, counts, meta, nav, notes) is 16px through `--fs-small`. The selected option has a 1.5px underline.

- Filters come from `categories` in each MDX file. The vocabulary is fixed in `lib/projects.ts → CATEGORIES` and in
  the enum in `content.config.ts`. Only categories in use are shown, with their counts. Vocabulary (owner, 2026-10-09):
  All, Mobile (JustCook, Rehab, Smart Home Hub, AuraWake), XR (Realiti), Product (Smart Home, JustCook), Multi-screen
  (Rehab: phone and TV used together).
- The selected filter or view turns ink and is underlined (name and count separately). The others stay grey.
- Grid: two columns, every card half width (4:3). One column on phones.
- Collection header: row 1 = title; row 2 = filters (left, cols 1–9) and Grid/Index switch (right, cols 10–12) on one baseline.
  Cards sit close together: 8px gap in both directions (rows open up to 48px on touch, where text is below). Card
  entrance never changes the footprint: cover fades in at full size while its image settles from scale 1.06; the
  second card of a row is delayed 120ms.
- Card: the cover fills the card. On hover/focus the cover zooms out to 0.95 over the project tone (Card `tone`) and
  square paper chips rise in at the bottom-left, staggered: title (Medium, ink), one chip per label (frontmatter
  `labels`, default [type, platform]), year (greys).
  Photographic full-bleed covers (`cover.bleed: true`, e.g. Rehabeat) rest at scale 1.07 and zoom out to 1 on hover:
  same gesture, no tone border (owner, 2026-10-13: all hovers zoom out). The cursor label still says "Read case study". Touch devices and unlinked cards (Playground) keep the text below the
  cover. The image is never darkened. Rejected: caption bar covering the cover; cover shrinking to fit the bar; info
  inside the cursor label (E2).
- Home hero has no background (owner, 2026-10-04: the --paper-alt band was removed). Only the depth texture
  (intensity 1.25, parallax 1.6×) marks it; it runs into the gap above Selected work and fades out (mask) before the section, which
  therefore has no top rule on the home page.
- Index view: a table (No., project, type, role, year). On hover the cover follows the cursor. The chosen view is
  remembered in localStorage.
- The owner rejected these, so do not bring them back: a facts block right-aligned under the cover; facts unfolding
  in an index; the sticky side index next to the cards.

Status:
- JustCook (01) is written with real data.
- Rehabeat (02, ex "Rehab", file `02-rehabeat.mdx`) is written with real facts (notes/02-rehab.md) and verified literature
  numbers in Challenge, but its interfaces are placeholders (Result media labels, Features without `image`) until the
  owner sends the final screens. Published (`placeholder: false`) on 2026-10-12 at the owner's request; the Result showcase
  uses the final Figma screens, only the Design-chapter Features rows are still placeholders. Do NOT use the UI in
  Media/02-Rehab (old versions). `<Features>` items accept no `image` + `placeholder` label + `device: phone|tv`.
- Unfinished work is visible but not openable (owner, 2026-10-09): a project with `placeholder: true` gets a card and
  an index row with no link, no zoom and no preview; the cursor label turns `--soon` red with "Coming soon" (on touch,
  a red "Coming soon" line under the facts). Its page is still built but never linked: `noindex`, out of the sitemap
  (astro.config.mjs reads the flag), and the "Next case study" band skips it (no band if nothing is finished).
  Playground: same treatment in the nav (`soon: true` in data/site.ts: grey, "Soon" in place of the micro-number).
  Setting `placeholder: false` re-enables everything for a project.
- Smart Home Hub (03) text is written from the PIG report (notes/03-smart-home-hub.md) but stays Coming soon until
  the owner sends its interfaces. AuraWake (05) likewise (notes/05-aurawake.md). Realiti (04) still carries INVENTED placeholder facts (year, type, platform, role, timeline, team,
  tools). Replace them with the real ones when each case study is written.

## Case-study content rules (agreed with the owner)

- Use the official numbers from the project reports. Never inflate them.
- Present projected metrics as targets, never as results.
- Show a confident result and the process behind it. Don't narrate every setback. Keep honest limits for the
  Reflection chapter. JustCook's pickup partner Conad may be named (owner, 2026-10-04).
- Cover and figure boards are composed from the owner's official media (renders, posts, flyers) on a warm
  #e9e3d6 ground. Source PDFs are rendered with headless Chrome + pdf.js (scripts live in the session
  scratchpad, not in the repo).

## Design rules (agreed with the owner)

- Swiss editorial base + tech precision (mono labels, registration marks, hairline rules), with a
  touch of brutalism (oversized type) and one experimental gesture (the hero depth texture: three layers of near-invisible grain that drift in parallax with the cursor and surface slightly around it, components/DepthTexture.astro; the old registration field lives on in Playground).
- Background `#fdfdfc` (near-white, slightly cool). One accent `--signal` (#3d5a73), used sparingly. No gradients and no
  fluorescent colours. The only other colour is `--soon` (#a6463c, muted brick red), reserved for "Coming soon".
- Type: Geist Medium for headings (H2 ≈ 48px), labels in Geist Medium at 12px, uppercase, 8% tracking,
  tabular figures. Use contrast between
  ink and grey to build hierarchy.
- Animation level is medium. Always respect `prefers-reduced-motion`.
- Never use skill percentages, skill bars or proficiency ratings for skills or tools.
- No filler: every label or element must carry real information. That rules out decorative counters,
  status chips, local clocks, "(01)" section indices and taglines that repeat nearby content.
  Exception, requested by the owner: the small numbers (01, 02…) in the nav and in the Work index stay.
- Page-opening statements (home hero, About, Playground, 404) use `.display`: larger than section titles but Regular
  and airier, so they read as a voice. Section titles stay h2 Medium.
- Do not tell the owner's personal/educational backstory (school history, internships,
  certifications). The CV covers that. Keep the focus on projects and process.
- Voice: professional, direct, human. Write about the product in the third person or impersonally,
  and about process in the first person. Light irony is allowed only in Playground.
