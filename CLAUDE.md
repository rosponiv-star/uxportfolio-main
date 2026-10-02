# Valerio Rosponi — Portfolio

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

- `src/pages/index.astro`: Work page, which is also the home: full-screen hero, Selected work (filters, project count,
  Grid/Index switch, grid of cards in a 12 / 6+6 rhythm), "How I work" principles.
- `src/components/Section.astro`: the single section pattern used on every page (see "Layout system").
- `src/pages/work/[slug].astro`: case study template.
- `src/pages/about.astro`, `src/pages/playground.astro`, `src/pages/404.astro`.
- `src/content/projects/NN-name.mdx`: one file per case study. The `NN-` prefix is stripped from the URL.
- `src/data/site.ts`: personal info (email, LinkedIn, CV path).
- `src/styles/global.css`: tokens, type scale, motion primitives.
- `Media/`: raw source material from the owner. It is git-ignored. Copy processed assets into
  `src/assets/` (images, optimised by Astro) or `public/` (video, PDF).

## Writing a case study (MDX)

Frontmatter is validated by `src/content.config.ts`: title, order, tagline, year, type, platform,
role, timeline, team, tools, tone (placeholder cover colour), toneDark, cover {image|video, alt},
glance {problem, approach, outcome}, placeholder (set to `false` once the content is real).

Components available in MDX without imports:
- `<Chapter title="…">…</Chapter>`: a numbered chapter. Titles feed the Contents list automatically.
- `<Note label="Decision" text="Why…">paragraph(s)</Note>`: wraps the content it annotates. The content
  goes in tracks A–B and the note in track C, top-aligned.
- `<Figure src={img} alt="" caption="" ratio="16/9" size="wide|text" />`: `wide` (the default) spans the
  whole body lane. Import the image at the top of the MDX file. A `video="/media/x.mp4"` prop is also
  supported.
- `<Metrics items={[{ value, label }]} />` and `<Insights items={[{ title, text }]} />`.
- `<Reframes items={[{ client, problem, idea? }]} />`: problem-reframing cycles. The last item is shown as the final framing.
- `<Archetypes items={[{ name, alias?, quote, traits: [{ label, text }] }]} />`: behavioural archetypes.
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
  work; case study → Overview, Key insights, Outcome; About → What I bring. Keep inner rules to a
  minimum (only between repeated rows, never above the first one).
- Collection sections (Selected work, Experiments) use `stacked`: the title sits on its own row inside
  cols 1–3, with the content below.
- Spacing comes only from the tokens in global.css: `--space-1…6`, `--space-block` (between blocks),
  `--space-item` (between cards) and `--space-section` (between sections).
- To verify alignment, measure element edges against the column lines in the browser (a JS audit).
  Do not judge it by eye.

## Type scale (strict)

Use only the size tokens in global.css: mega, h2 (48), h3 (28), lead (~22), body (17), small (15)
and label (12, Geist Medium uppercase, 8% tracking). Never hard-code a font size. The only exceptions are graphics: the cover
title, the footer wordmark and the nav micro-numbers.

- Section titles and project card titles use h2. Other item titles (principles, insights, rows) use h3.
- Running text uses body. Navigation, index, notes, captions and secondary facts use small.
- An item row (principles, insights, About rows) is always: title in track A, text in tracks B–C.

## Work section

- Filters come from `categories` in each MDX file. The vocabulary is fixed in `lib/projects.ts → CATEGORIES` and in
  the enum in `content.config.ts`. Only categories in use are shown, with their counts.
- The selected filter or view turns ink and is underlined (name and count separately). The others stay grey.
- Grid rhythm: full width (2:1), then two halves (4:3 each), repeating. A half left alone becomes full. The script
  re-flows the rhythm on the filtered set.
- Card: cover, then title (h3) with the year on the right, then "type, platform" in small grey text.
- Index view: a table (No., project, type, role, year). On hover the cover follows the cursor. The chosen view is
  remembered in localStorage.
- The owner rejected these, so do not bring them back: a facts block right-aligned under the cover; facts unfolding
  in an index; the sticky side index next to the cards.

Status:
- JustCook (01) is written with real data.
- The other four MDX files still carry INVENTED placeholder facts (year, type, platform, role, timeline, team,
  tools). Replace them with the real ones when each case study is written.

## Case-study content rules (agreed with the owner)

- Use the official numbers from the project reports. Never inflate them.
- Present projected metrics as targets, never as results.
- Show a confident result and the process behind it. Don't narrate every setback (e.g. a partner who
  didn't join). Keep honest limits for the Reflection chapter.
- Cover and figure boards are composed from the owner's official media (renders, posts, flyers) on a warm
  #e9e3d6 ground. Source PDFs are rendered with headless Chrome + pdf.js (scripts live in the session
  scratchpad, not in the repo).

## Design rules (agreed with the owner)

- Swiss editorial base + tech precision (mono labels, registration marks, hairline rules), with a
  touch of brutalism (oversized type) and one experimental gesture (the cursor-reactive registration field).
- Background `#f5f5f0`. One accent `--signal` (#3d5a73), used sparingly. No gradients and no
  fluorescent colours.
- Type: Geist Medium for headings (H2 ≈ 48px), labels in Geist Medium at 12px, uppercase, 8% tracking,
  tabular figures. Use contrast between
  ink and grey to build hierarchy.
- Animation level is medium. Always respect `prefers-reduced-motion`.
- Never use skill percentages, skill bars or proficiency ratings for skills or tools.
- No filler: every label or element must carry real information. That rules out decorative counters,
  status chips, local clocks, "(01)" section indices and taglines that repeat nearby content.
  Exception, requested by the owner: the small numbers (01, 02…) in the nav and in the Work index stay.
- Hero statement: short, a single dark colour, 48px.
- Do not tell the owner's personal/educational backstory (school history, internships,
  certifications). The CV covers that. Keep the focus on projects and process.
- Voice: professional, direct, human. Write about the product in the third person or impersonally,
  and about process in the first person. Light irony is allowed only in Playground.
