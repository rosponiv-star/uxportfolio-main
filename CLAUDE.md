# Valerio Rosponi — Portfolio

Personal portfolio of Valerio Rosponi (UX / digital product / visual designer, junior).
The site exists to show **case studies, process and mindset** to recruiters and hiring
managers. It is not a self-promotion or "hire me" site: contact stays discreet.

The owner never edits code by hand; every change goes through Claude. Talk to him in Italian;
all site copy is in **English**.

## Stack

- Astro 7 (static output) + MDX + sitemap. No CSS framework: hand-written CSS.
- Fonts: Geist / Geist Mono via Fontsource (self-hosted).
- Deploy: GitHub `rosponiv-star/uxportfolio-main` → Cloudflare (build `npm run build`, output `dist`).
  Domain: www.valeriorosponi.com.
- Note: on this machine run `astro` commands from PowerShell. In Git Bash, Rolldown's native
  binding fails to load.

## Structure

- `src/pages/index.astro`: Work page, which is also the home: hero, case studies, "How I work" principles, "Now".
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
- `<Note label="Decision">…</Note>`: margin annotation. Put it right before the paragraph it annotates.
- `<Figure src={img} alt="" caption="" ratio="16/9" size="text|wide|full" />`. Import the image at
  the top of the MDX file. A `video="/media/x.mp4"` prop is also supported.
- `<Metrics items={[{ value, label }]} />` and `<Insights items={[{ title, text }]} />`.
- `<Todo>…</Todo>`: visible placeholder. Remove these as the real content arrives.

Cover media: put the image in `src/assets/projects/<name>/` and reference it in the frontmatter
`cover.image` with a relative path. Put looping videos (mp4/webm, muted) in `public/media/<name>/`
and use `cover.video`.

## Design rules (agreed with the owner)

- Swiss editorial base + tech precision (mono labels, registration marks, hairline rules), with a
  touch of brutalism (oversized type) and one experimental gesture (the cursor-reactive registration field).
- Background `#f5f5f0`. One accent `--signal` (#c93a14), used sparingly. No gradients and no
  fluorescent colours.
- Type: Geist Medium for headings (H2 ≈ 48px), Geist Mono Bold for small labels. Use contrast between
  ink and grey to build hierarchy.
- Animation level is medium. Always respect `prefers-reduced-motion`.
- Never use skill percentages, skill bars or proficiency ratings for skills or tools.
- Do not tell the owner's personal/educational backstory (school history, internships,
  certifications). The CV covers that. Keep the focus on projects and process.
- Voice: professional, direct, human. Write about the product in the third person or impersonally,
  and about process in the first person. Light irony is allowed only in Playground.
