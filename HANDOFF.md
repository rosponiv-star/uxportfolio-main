# HANDOFF — Valerio Rosponi portfolio

This file hands the project over between Claude sessions — LOCAL (Windows PC, has `Media/`) and CLOUD
(claude.ai/code, no `Media/`) — so a new session reaches the same operational awareness as the one that just ended.
Read this file **in full**, then read `CLAUDE.md` (persistent rules, auto-loaded every session). Where the two
disagree, this file is newer and wins.

**Before anything else: sync git as §10 describes, then re-read this file** — another session may have pushed a
newer version while you were away.

Structure of this document (10 fixed sections + two appendices):
1. Overview & Global Architecture — what the site is and what already works
2. Art Direction, UI/UX & Style Rules — the design system, verbatim
3. Development Rules & Working Style — how the owner works, how to write code here
4. Discarded Approaches & Anti-patterns — do not re-propose these
5. Git Status & Recent History — snapshot at last update
6. Detailed File Map — exact paths, what each one owns
7. Technical Context, Bugs & Tech Debt — open issues, accepted shortcuts
8. Run & Test Commands — exact commands, copy-paste ready
9. Immediate Task & Roadmap — the unambiguous next step
10. Hybrid Flow (Local ↔ Cloud) — the sync protocol, read this one every session
- Appendix A — Session log (newest first)
- Appendix B — JustCook verified facts + how to write the next case studies

---

## 1. Overview & Global Architecture

**What the site is.** A personal portfolio for Valerio Rosponi (junior UX / digital product / visual designer, 3rd
year BSc "Interfaces & Communication" at the University of Trento). It exists to show **case studies, process and
mindset** to recruiters and hiring managers — not a self-promotion or "hire me" site, so contact stays discreet (no
sticky CTA, no "available for work" banner). Target companies the owner cited: Belka, Bending Spoons, Apple, Google,
Deda, DXC, GPI, Meta, Microsoft. Preferred sectors: health, fintech, fashion, wellbeing. Open to remote, not to
relocating right now. Lives between Malè and Rovereto (TN).

**Exact stack.**
- **Astro 7** (static output, no SSR/SSG islands framework — plain Astro components + vanilla `<script>` for
  interactivity), `@astrojs/mdx` (case studies are `.mdx`), `@astrojs/sitemap`.
- **Hand-written CSS only** — no Tailwind, no Bootstrap, no CSS-in-JS. One global stylesheet
  (`src/styles/global.css`) holds every design token; components use Astro's native scoped `<style>` blocks.
- **Font:** Geist only, self-hosted via `@fontsource-variable/geist` (variable font, so weights are picked with
  `font-weight`, not separate files). Geist Mono was installed early on and later **uninstalled** — do not
  reintroduce monospace type.
- **TypeScript** for the few vanilla scripts (`src/scripts/site.ts`, inline `<script>` blocks in components —
  Astro transpiles these).
- **No component framework** (no React/Vue/Svelte islands) — everything is `.astro` templates + plain DOM scripts.
- **Node 24** on the local machine.

**Deploy.** GitHub `rosponiv-star/uxportfolio-main`, branch `main` → **Cloudflare** (Pages/Workers; build
`npm run build`, output `dist`). Domain in code: `https://www.valeriorosponi.com` (`astro.config.mjs` → `site`,
`public/robots.txt`). `main` is what Cloudflare actually deploys — pushing there is publishing to the live site.

**Pages implemented and working today:**
- **Home `/`** (`src/pages/index.astro`) — also the Work listing. Hero statement over an animated depth-texture
  background (no solid band), a two-column project grid with a rich hover state, "How I work" principles, footer.
  Fully built, see §2 for the exact spec.
- **Case study template `/work/[slug]`** (`src/pages/work/[slug].astro`) — intro, Overview, Result (showcase or
  placeholder), a process index with a sticky reading bar, then MDX chapters, then a "next case study" band. A
  library of ~14 purpose-built components renders the chapters (see §6). **JustCook (`01-justcook.mdx`) is fully
  written with real data and a real cover/Result/Design gallery** — treat it as the reference implementation for
  tone, structure and component usage when writing the next four case studies.
- **About `/about`**, **Playground `/playground`**, **404** — built, stable, not a current focus.

**Content status (projects):**

| Project | Status |
|---|---|
| 01 JustCook | **Done.** Real research data, real cover, real Result showcase, real Design chapter with product photography. Reference implementation. |
| 02 Rehab | Placeholder — invented frontmatter facts, MDX skeleton only. |
| 03 Smart Home Ecosystem | Placeholder — invented frontmatter facts, MDX skeleton only. |
| 04 Realiti | Placeholder — invented frontmatter facts, dark tone, MDX skeleton only. |
| 05 AuraWake | Placeholder text, **real cover** (2 app screens on a flat ground). |

**What "working" means concretely** (so a new session doesn't re-build what exists): the full case-study component
library below is implemented, styled, responsive and verified with headless-Chrome screenshots at 1440×900 and
390×844 — don't rebuild these, extend or reuse them:
`Chapter`, `Key`, `Note`, `Figure`, `Metrics` (+ `Stat` count-up), `Insights`, `Reframes` (stepped funnel), `Archetypes`
(side-by-side comparison), `Chips` (item row / card variants, hover note or image preview), `BigStat`, `Features`
(alternating device rows), `Gallery` (mosaic with 2×2 hero tiles), `BoxStrip` (colour-block product panels),
`Closing`, `ProcessIndex` (inline + sticky reading bar), `Showcase` (Result device presentation). All live in
`src/components/case/`.

---

## 2. Art Direction, UI/UX & Style Rules

**Philosophy:** Swiss editorial base + tech precision (hairline rules, precise alignment, uppercase micro-labels)
with a touch of brutalism (oversized display type) and exactly **one** experimental gesture — the hero's depth
texture (parallax grain, see below). Everything else stays restrained. The owner consistently rejects decorative
noise, "clever" interaction for its own sake, dark overlays and showy motion. He likes clean grids, generous but not
scattered space, fluid and subtle motion. **When in doubt, propose the more restrained option first.**

### Colour (`global.css :root`) — exact values, do not approximate
| Token | Value | Use |
|---|---|---|
| `--paper` | `#fdfdfc` | page background (near-white, slightly cool) |
| `--paper-2` | `#f2f2ef` | placeholder surfaces, hover fills |
| `--paper-3` | `#e8e8e4` | tertiary surface |
| `--paper-alt` | `#f3f3f0` | tinted bands (How I work, case-study Result + Insights, About "What I bring") |
| `--ink` | `#111111` | primary text |
| `--ink-2` | `#33332f` | secondary text |
| `--ink-3` | `#6b6b65` | tertiary text / muted |
| `--ink-4` | `#8a8a84` | quaternary text / faintest |
| `--rule` | `rgb(17 17 17 / .08)` | row hairlines |
| `--rule-strong` | `rgb(17 17 17 / .22)` | section rules, card borders |
| `--signal` | `#3d5a73` (slate blue) | the **single** accent colour — sequence numbers, active states, progress fills. Used sparingly, never as a background fill for large areas. |

Colour history (do not re-propose): background went `#f5f5f0` → `#fafaf8` → `#fcfcfb` → `#fdfdfc`. Accent went
orange `#c93a14` → green `#2b9e4d` (rejected) → slate `#3d5a73` (kept, derived from cover tones). **No gradients, no
fluorescent colours, no dark background sections except the inverted "Next case study" band and the final box of a
Reframes funnel.**

### Typography (Geist only) — exact size tokens, never hard-code a font-size
| Token | Size | Use |
|---|---|---|
| `--fs-mega` | clamp → ~168px | case-study title, footer wordmark, "Next" band title |
| `--fs-display` | 30→60px, **Regular 400**, lh 1.1 | page-opening statements only (home hero, About, Playground, 404) |
| `--fs-h2` | 32→48px, Medium | section titles ("Selected work", "How I work", chapter titles) |
| `--fs-h3` | 22→28px | item titles (principles, insights, index rows); case-study `<Key>` sentence (Regular 400) |
| `--fs-lead` | ~19→23px | lead paragraphs; card titles (Medium); chapter group headings `###` (Medium, with a signal "01.1" number) |
| `--fs-body` | 17px | running text in non-case-study contexts; text inside case-study blocks (archetype quotes/traits, insight evidence, reframe values) |
| `--fs-read` | 17→19px, lh 1.55 | case-study **chapter paragraphs only** (the longer reading measure) |
| `--fs-stat` | 56→104px, Medium, tight tracking | key numbers only (`Metrics`, insight `stat`); affixes (%, min, signs) sit at 0.42–0.55em, proportional figures (clean "1", no tabular foot) |
| `--fs-small` | 16px | nav, filters, meta, notes, captions |
| `--fs-label` | 12px | `.label` class: Geist **Medium 500**, uppercase, 8% letter-spacing, tabular figures |

**Label roles — never give two different kinds of information the same visual treatment** (owner correction,
2026-10-04, after "Cycle 01" and "Problem" looked identical):
- `.label` (signal colour) = a **number or step in a sequence** — "01", "Cycle 02", chapter numbers.
- `.label.label--group` (ink colour) = the **heading of a group** — "Targets for a pilot", "Must-haves", "Channels".
- `.field` (small, grey `--ink-3`, sentence case, **not** uppercase) = the **name of a field inside an item** —
  "Problem", "Idea", "Friction", a number's caption.

Type history: tried Regular-weight labels at 6% tracking with a no-wrap card eyebrow, **reverted** — labels stay
Medium 500. Selected filter/view underline is exactly **1.5px**.

### Layout system (strict — verify numerically, never by eye)
- **12-column grid.** `--margin` = clamp(16–48px), `--gutter` = clamp(16–24px).
- **The section pattern** (`components/Section.astro`, used everywhere): a full-width top rule, title in the head
  lane (columns 1–3, `position: sticky`), content in the body lane (columns 4–12). `tone="alt"` swaps the rule for a
  full-bleed `--paper-alt` band (no rule before or after a band). `stacked` puts the title on its own row (used by
  `Collection`).
- **The body lane splits into three equal tracks** via `.trio`: A = cols 4–6, B = 7–9, C = 10–12. Every element
  must start and end exactly on a track edge — `span-2` spans B–C, full-width spans A–C. Running text uses the A–B
  measure (not A–C — text that wide is hard to read). Boxes, figures, metrics and data rows span A–C.
- **Spacing is token-only**, never a raw px/rem value in a component: `--space-1…6` (8/16/24/32/48/64px),
  `--space-block` (vertical rhythm between blocks inside a section), `--space-item` (between cards),
  `--space-section` (between sections).
- **Alignment verification:** always measure element edges against the column lines with a small JS audit in the
  browser (`getBoundingClientRect()` compared to grid math) — the owner explicitly rejected "looks aligned" as a
  verification method.

### Motion
- Medium overall level. **Always** respect `prefers-reduced-motion` — every animated component has a static
  fallback branch.
- Current calibration (owner, 2026-10-04, after an "evident/premium" request was walked back): **motion must be
  barely noticeable** — his words: *"se uno non ci vuole fare caso non ci fa caso"* (if you don't want to notice it,
  you won't). Concretely: no entrance/reveal choreography on the Result showcase, only a ~24px-max inertial
  parallax and a 4px hover lift. **Always start from the smallest plausible motion amplitude, never the largest** —
  he will ask to reduce it, rarely to increase it (the one exception was the home hero texture intensity, see §3
  Appendix/log).
- Page view-transitions are on (Astro's native `<ClientRouter>`-less transition API via CSS).
- Hero words use a blur-fade focus-in per word (a masked slide-up was tried and rejected — it cut letters).
- The cursor label ("Read case study" etc.) follows the pointer over linked cards/bands; it inverts to light-on-dark
  over dark surfaces (`data-cursor-theme="light"`).
- The **depth texture** (`components/DepthTexture.astro`) is the one permitted "experimental gesture": three
  canvas-drawn grain layers that drift in parallax with the pointer and "breathe" (brighten) near the cursor. Props:
  `intensity` (dot opacity multiplier, home uses **1.25** — raised twice from an initial 0.5 after "rendili più
  visibili") and `parallax` (travel-distance multiplier per layer, home uses **1.6**). Static on touch / reduced
  motion. Do not add new experimental gestures elsewhere — this is the only one.

### Responsive rules
- Two breakpoints used throughout case-study components: **960px** (tablet — grid collapses or simplifies) and
  **640px** (phone — single column, horizontal swipe rows for anything that was a multi-column grid, i.e.
  `Showcase`, `Gallery`, `Chips`).
- The Work/Playground grid is two columns of 4:3 cards, one column on phones.
- Card entrance never changes its footprint (no layout shift): the cover fades in at full size while the inner
  image settles from `scale(1.06)`.

### Component construction conventions (how `.astro` files here should be built)
- **Props:** a TypeScript `interface Props` at the top of the frontmatter fence, destructured with sane defaults
  (`const { items, variant = 'plain' } = Astro.props;`).
- **Styling:** Astro's native scoped `<style>` block per component. Reach for `:global(...)` only when styling
  markup injected via `<slot />` or an imported sub-component's output. Class names follow a loose BEM pattern —
  `.component`, `.component__part`, `.component--variant` (e.g. `.chips--cards`, `.step--final`).
  No CSS modules, no utility classes beyond the shared `.label`, `.field`, `.muted`, `.trio`, `.span-2` primitives
  in `global.css`.
- **Grid placement:** components that live inside a case-study chapter body use `.trio` + explicit `grid-column`
  inline styles when a component needs custom spans (e.g. `Reframes`' stepped funnel, `Archetypes`' comparison
  columns) — see those two files for the pattern of computing `grid-column` from an index.
- **Entrance reveals:** add `data-reveal` (optionally `data-reveal="group"` or similar for a custom observer) to
  opt an element into the site-wide `IntersectionObserver` fade-up in `site.ts`; stagger with `style="--d: {i}"`
  which the global CSS reads as a transition-delay multiplier. Components with their own bespoke motion (the
  `Showcase` parallax, `Stat`'s count-up) manage their own `IntersectionObserver` instead.
- **Images:** always `astro:assets` `<Image>` (never a raw `<img src>`), always pass `widths` + `sizes` for
  responsive output, always a real `alt`.
- **Numbers:** any number shown at a large size goes through `<Stat value="…" />`, never raw text — it handles the
  count-up, the proportional-figure "1" fix, and prefix/suffix sizing consistently.

### Information architecture of a case study (fixed order — owner's brief, 2026-10-03)
*"More concise, more impactful, no filler; a recruiter sees interface and result at first glance, and can dig into
the whole process and way of thinking if they want."*
1. Back button (outlined pill, static chevron — no animated arrow).
2. Title (`--fs-mega`) + one-sentence tagline (`--fs-lead`).
3. Cover (16:10).
4. **Overview** — no band, ink top rule (other sections get a grey one); Problem/Approach/Outcome, one sentence
   each; then the facts grid; separated by whitespace only (hairlines between them were tried and rejected as "too
   many lines").
5. **Result** — alt band. If `result.showcase` exists (JustCook), it's a full-width device presentation via
   `Showcase.astro`; otherwise a simpler placeholder layout. This is the "30-second read" — interface + outcome
   before any process explanation.
6. **Process** — `ProcessIndex.astro`: steps hanging off an ink line, each numbered with a 2–4-word summary pulled
   from the MDX `<Chapter summary="…">` attribute. Once scrolled past, a slim fixed bar under the header takes over
   as a reading progress indicator (replacing a plain progress bar).
7. **Chapters** (from MDX): Challenge → Research → Insights (alt band) → Define → Ideate → Design → [Validate, only
   if usability testing happened] → Reflection → `Closing`. Each chapter opens with a `<Key>` sentence (h3 size,
   Regular, ink) then short paragraphs (2–3 lines, `--fs-read`). No filler — cut anything that doesn't carry a fact, a
   decision or a reason.
   **One reading column** (owner, 2026-10-09, after "il testo è caotico, l'occhio cerca il prossimo testo"): text
   reads top to bottom from the left edge of track A, nothing parked in track C. Chapters are split into groups with
   MDX `### Title` → signal number "01.1" (CSS counter `group` inside the page's `chapter` counter) + title in lead
   Medium. Proximity: `--space-item` before a group, `--space-3` heading → content, `--space-block` inside. Notes are
   tinted callouts under the content; BigStat/Reframes/Closing captions sit under their numbers; Chips and Insights
   stack (Insights `variant="compact"` for the launch plan). Wide media still spans A–C.
8. "Next case study" full-bleed band (inverted colours, cover image of the next project).

---

## 3. Development Rules & Working Style

**The owner never edits code.** Every change goes through Claude — always build, verify, commit and push before
reporting back; never leave work uncommitted at the end of a turn.

**Language:** talk to the owner **in Italian**, always. All site copy is in **English**, always. This HANDOFF file
and `CLAUDE.md` are written in English (matching the codebase's own comments/docs convention) — keep it that way for
continuity even though the owner himself is addressed in Italian.

**Iteration style:** the owner gives short, blunt visual feedback — *"non mi piace"*, *"torna alla versione
precedente"*, *"nessuna"*. **Revert immediately** when told, no argument. When he asks for options on something
visual/taste-based, **do not just describe them in text** — show **live interactive concepts** with the
`mcp__visualize__show_widget` tool (load `read_me` with the `interactive` module first), then implement only the
option he picks. When he explicitly asks to "ask questions" (or a decision is genuinely his to make, not inferable
from the repo), use `AskUserQuestion` with 2–4 concise options, one marked "(Recommended)".

**Autonomy level:** high on implementation and technical decisions; low on taste/content calls. Make the obvious
engineering choice yourself and proceed; stop and ask (via widget or `AskUserQuestion`) only for things that are
genuinely subjective or where getting it wrong means redoing real work (new colours, new layout concepts, content
claims about the owner's life/work). Default to the more restrained option when proposing something new (§2
philosophy).

**Verification discipline:** headless Chrome via **puppeteer-core**
(`C:/Program Files/Google/Chrome/Application/chrome.exe`) is the reliable way to check visual work — the in-app
Browser pane is too narrow/scaled for pixel-accurate review. Standard checks: screenshot at 1440×900 and 390×844
(mobile viewport with `isMobile`/`hasTouch`), measure alignment/gaps/visibility numerically in page-evaluated JS,
never eyeball it. See §8 for the exact gotchas (lazy images, `data-reveal` classes, stale dev-server cache).

**End every reply with a short Italian summary**: what changed, what was verified (and, honestly, what was *not*
verified), and any open choices. Use tables when they make it scannable.

**Commit discipline:**
- Build **before** every commit (PowerShell command, §8) — never commit a broken build.
- One logical change per commit where practical; commit messages in English, imperative, with a short body when the
  change needs explaining.
- **Attribution line is MANDATORY on every commit and PR** and changes depending on which model is active this
  session — check the system reminder at the top of the conversation for the current line. As of this update it is:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  ```
  (Earlier commits in this repo used `Claude Opus 5.5` — that's fine, don't rewrite history, just use whatever the
  *current* session's system prompt specifies going forward.)
- Use `git commit -q -F -` with a heredoc (commit messages often contain quotes/apostrophes that break `-m`).
  PowerShell `-m @'...'@` has broken before — avoid it.
- **HANDOFF.md and CLAUDE.md updates are their own commit discipline**: after any change that touches design
  system, file map, or decisions, update the relevant sections here (not just the session log) *in the same session*
  and commit that too. An out-of-date HANDOFF is worse than none.

**Content conventions (MDX / frontmatter):** see `CLAUDE.md` "Writing a case study" section for the exact schema
(`src/content.config.ts`) and the full list of components usable in MDX without imports — it is kept perfectly in
sync with the component library and is the single source of truth for prop shapes; this file does not duplicate it.

---

## 4. Discarded Approaches & Anti-patterns

**Do not re-propose any of these unless the owner explicitly asks.** Grouped by area.

**Home hero:**
Full-screen statement only; compact hero; registration-mark field background (replaced by the depth texture);
masked word slide-up animation (cut letters); 6 full hero layouts (monumental name, dark band, project thumbnails
inside the sentence, split with a role column, merged straight into Selected work); 4 hero→work transition devices
(curtain sheet, statement shrinking into the title, typographic "05 case studies" bridge, horizon filter bar) — he
said *"nessuna"* to all of them. New divider-effect concepts between hero and work (dot horizon, rippling line,
halftone dissolve) were shown and declined — "just show more of the existing texture" was the accepted answer.

**Work grid / cards:**
13 scroll concepts for the project list (clip reveal + inner parallax, focus/blur, stacking deck, horizontal pinned
track, inertia+skew, sticky index with preview, expanding window, focus carousel, 4 accordion-strip variants,
editorial collage) — all rejected, plain two-column grid stays. Grid rhythm experiments (12-col, 6+6) before
settling on all-half cards. A sticky side index next to the cards; facts blocks right-aligned under a cover; facts
unfolding inside the index view; a "N of N projects, years" count line; corner marks on covers; a "Read case study"
CTA chip under cards; card text sitting above the cover.

**Card hover** (final answer: zoom-out + paper "chip" captions, see §2/§6): a dark scrim over the cover (hard no,
repeated request); a paper caption bar sliding up and *covering* the cover; the cover shrinking to make room for a
bar; title/meta living inside the cursor label itself ("E2") and its tech-editorial variants (tabbed card
"E3", crosshair "E4", typographic "E5"); a translucent corner tag (variant "B3" was the runner-up); a technical spec
sheet ("B4"); a traced/drawn frame ("B5"); a full-width "ruler strip" ("B6"); free-floating text with no container;
a slim single-line bar. The winning design — square paper chips rising bottom-left on hover, cover zooming to 0.95
— beat all of the above.

**Typography / colour:**
Geist Mono entirely (removed from the project); Regular-weight labels at 6% tracking with a no-wrap eyebrow
(reverted to Medium 500); accent colours orange (`#c93a14`) and green (`#2b9e4d`).

**Chrome / navigation:**
An animated back arrow; a "Back to top" footer link; an in-page "Next" section styled with an arrow; a
registration-field pattern as the "Next" band background (the real cover image was restored instead).

**Case study structure:**
`PhoneScroll` — a sticky scroll-driven device scene with screen-dissolve transitions — was fully built, then
**removed entirely** by the owner (2026-10-03, *"togli il cellulare interattivo"*). Do not reintroduce it; the
"realistic hand photo" idea that was pending for it is now moot. Overview laid out with gutter hairlines between
the three tracks ("too many lines"); Overview as a dark band; Overview as stacked full-width sentences; Overview as
a text+data two-column split. Process index as a plain row table-of-contents with key sentences; as a dotted
book-style TOC; as a sticky side index (same objection as the card-grid version).

**Case-study text layout (2026-10-09):** notes and captions in a side column (track C) beside the text they annotate
— the eye had to hunt for them. Concepts shown and not picked: "A · Righe indice" (block titles in track A, content in
B–C) and "C · Sintesi prima" (3 big takeaways per chapter, details small below). The owner chose "B · Una colonna",
with more breathing room.

**Result showcase (device presentation):**
A dark ink background band — tried, then reverted *"era meglio prima"* (it was better before). Entrance
choreography of any real size — first 80px rises + scale, then even a reduced 24px fade-up, both rejected down to
**no entrance animation at all**, only a quiet ~24px parallax. Letting device groups break out of the 12-column grid
("dentro la griglia" — inside the grid — was his explicit preference).

**Case-study media / covers:**
Any simulated photographic "depth" on covers — radial studio light/vignette, cast shadows under phones, a diffuse
halo — all tried and rejected; **flat, evenly-lit ground only**. Media boards embedded inside the JustCook body text
(removed for now, *"ci penseremo dopo"* — the Result showcase and Design-chapter galleries replaced the need).

**Reframing / archetypes:**
A plain unstyled list of the six reframing cycles (replaced by the stepped-funnel treatment); a timeline layout and
a simple "before → after" two-box layout for the funnel were both considered and passed over in favour of the
stepped funnel with a big "N → 1" header. For archetypes: a light+dark paired box pair, and a horizontal "spectrum"
layout with the two archetypes at opposite poles, were both considered and passed over in favour of two light boxes
compared side by side with a shared row grid.

---

## 5. Git Status & Recent History

*(Snapshot taken at the time of this update — re-run `git status`/`git log` at the start of your session, don't
trust this as current.)*

- **Branch:** `main` (this is a LOCAL session; LOCAL always works on and pushes to `main` directly — see §10).
- **Working tree:** clean after the 2026-10-09 push.
- **HEAD commit:** `447dbe152dd578381847c8fc06884cff1c3a8f03` —
  *"JustCook Design: colour-block box strip, bigger alternating screens, campaign mosaic"*
  (author `rosponiv-star`, committed 2026-10-05 00:14:04 +0200; co-authored by Claude Opus 5.5, the model active in
  that session).
- **No unmerged `claude/*` branches** at last check (`git branch -r --no-merged main` returned nothing) — if a new
  one exists when you start, that's cloud work waiting to be merged, see §10.

**Last 15 commits (oldest-relevant→newest), for orientation:**
```
447dbe1 JustCook Design: colour-block box strip, bigger alternating screens, campaign mosaic
0dc5d93 JustCook: drawn arrow, proportional figures, perspective box renders
abd1d01 JustCook closing line: "Design the easy path, and people will take it."
997be11 JustCook: close the case study with a statement and the lesson to remember
fbb83f8 JustCook: featured stat, richer Design with screens and brand gallery, launch plan
4f81927 Case study: label roles, bolder numbers, archetype contrast, scannable text
41f6a17 Case study: data with character, archetypes compared, reframing as a funnel
15b9fe2 Home texture: fade only near the bottom so more of it shows
cb119ec Home texture: dots clearly visible (intensity 1.25)
fbd2b50 Home texture: a little more visible, stronger pointer parallax
3dcbafb HANDOFF: log the first local merge of cloud work
1f108f8 Home hero: drop the grey band, stronger texture fading out above Selected work
8145aea HANDOFF: owner's rule for cloud-to-local handovers
84a235a HANDOFF: log the first local merge of cloud work
226c3c5 HANDOFF: cloud/local session protocol and session log
```

This commit train tells the story of the current focus: the home hero was reworked (band removed, texture tuned up
twice), then JustCook's case-study chapters got three successive passes of visual-impact work (data/numbers →
archetypes/reframing → Design chapter product photography), each one driven by direct owner feedback on the
previous pass. **Expect the owner to keep iterating on JustCook's visual polish** before the project moves to case
studies 02–05.

---

## 6. Detailed File Map

```
astro.config.mjs            site URL, mdx + sitemap integrations, prefetch config, devToolbar off
src/styles/global.css       ALL design tokens (colour, type scale, spacing), grid primitives (.trio, .span-2),
                             prose styles, the .label/.field/.muted primitives, reveal-animation CSS, view transitions
src/layouts/Base.astro      <head>, Header, Footer (showContact prop), global <script> include
src/scripts/site.ts         reveals (IntersectionObserver, rootMargin -1%), header hide-on-scroll, cursor label
                             (data-cursor / data-cursor-theme / data-cursor-style / data-cursor-image), scroll-spy,
                             video autoplay. NOTE: the old plain progress bar is superseded on case-study pages by
                             ProcessIndex's own sticky reading bar.
src/data/site.ts             name, email (rosponiv@gmail.com), LinkedIn (STILL A PLACEHOLDER URL — open item),
                             CV path, nav entries

src/components/
  Header.astro                name left; nav "01 Work / 02 Playground / 03 About" with signal-coloured active state
  Footer.astro                contact row (email, LinkedIn, Résumé PDF), giant "Valerio Rosponi" wordmark, ©
  Section.astro                THE section pattern — see §2. Props: title, id, class, bodyClass, stacked, tone
  Collection.astro             shared Work/Playground block: title, filters, Grid/Index switch, grid slot, index
                                table + its own script (localStorage view preference)
  Card.astro                   generic card: media slot; hover = cover zooms to .95 + paper "chip" captions rising
                                bottom-left (title/type/year), staggered 60ms. Touch/unlinked cards: text below.
  ProjectCard.astro            Card + Cover wired to a project's frontmatter
  Cover.astro                  project cover: real image/video, or a placeholder (tone colour + faint grid + title)
  DepthTexture.astro           the hero's grain/parallax canvas — props intensity, parallax (see §2 Motion)
  RegistrationField.astro      the old cursor-reactive "+" field — now lives on only as the Playground experiment

  case/                        — the case-study component library, all in src/components/case/
    Chapter.astro               a numbered chapter wrapper; title + summary feed the Process index
    Key.astro                   the chapter's opening key sentence (lead size, ink)
    Note.astro                  an annotated aside (A–B content, C-track note, e.g. "Decision", "Discarded", "Plan")
    Figure.astro                a captioned image/video figure
    Metrics.astro                large bare numbers on an ink hairline; optional title (group heading) and
                                 variant="boxed" (tinted boxes, for a second class of number in the same chapter)
    Stat.astro                   the shared "big number" renderer: splits prefix/digits/suffix, drives the
                                 one-time count-up (~1.2s, IntersectionObserver-triggered), proportional figures
    Insights.astro               numbered findings; an item may carry stat/statLabel to lead with a number
    Reframes.astro               the stepped-funnel reframing-cycles display; cycles prop opens with a big "N → 1"
                                 (drawn hairline + chevron arrow, NOT a text arrow — see §4); each item can carry a
                                 real cycle number n shown large and faint behind the box; discarded ideas struck
                                 through; the last item is the dark "final framing" box
    Archetypes.astro             two archetypes compared side by side: row labels in track A (right-aligned, with a
                                 hairline leader into the boxes), a tinted header band, optional large goal row
                                 ("Less effort" vs "Less waste"), quote, then shared trait rows
    Chips.astro                  a short list pulled out of prose as an item row: label + intro in track A, chips in
                                 B–C. variant="chips" (hover shows a sentence-case note or an image preview in the
                                 cursor label) or variant="cards" (the note is always visible, used for channels)
    BigStat.astro                the one number a chapter hinges on — mega size across A–B, caption+source in C
    Features.astro               product features paired with their screen; alternate prop flips device side
                                 row-by-row for rhythm; crop prop controls how much of the device height shows
    Gallery.astro                brand/campaign material in a tinted full-width panel; groups of items, kind
                                 cutout|tile; an item can take span:2 for a 2×2 hero tile in a dense mosaic
    BoxStrip.astro                a product line as solid colour panels (one per product, its own brand colour),
                                 the product cut-out large inside; hover cross-fades to a second image (e.g.
                                 perspective view ↔ front view)
    Closing.astro                 the case study's last word: a display-size statement, then a hairline and the one
                                 lesson to remember in h2 size
    ProcessIndex.astro            inline process list + the fixed sticky reading bar that replaces it on scroll
    Showcase.astro                 the Result section's device presentation (grouped screenshots, crop/stagger
                                    options, quiet parallax)
    Todo.astro                     a visible "still to write" placeholder block — remove as real content arrives

src/lib/
  projects.ts                  getProjects, slugOf/hrefOf/numOf, chapterId/chaptersOf (reads <Chapter> tags from
                                MDX for the Process index), CATEGORIES (re-exports categoryId)
  collection.ts                categoryId, gridSizes (currently always 'half'), yearSpan (unused)

src/content.config.ts          the project frontmatter schema — SINGLE SOURCE OF TRUTH for every prop shape used
                                by MDX components; keep CLAUDE.md's "Writing a case study" section in sync with it
src/content/projects/
  01-justcook.mdx               REAL — reference implementation, read it before writing 02–05
  02-rehab.mdx, 03-smart-home-ecosystem.mdx, 04-realiti.mdx, 05-aurawake.mdx    PLACEHOLDER frontmatter + MDX

src/pages/
  index.astro                   home: hero (DepthTexture) + Collection(work) + "How I work" + footer
  work/[slug].astro             case-study template — wires frontmatter + MDX body into the section order in §2
  about.astro, playground.astro, 404.astro

src/assets/
  valerio-rosponi.png            About portrait
  projects/justcook/
    cover-app.png                 the case-study cover (3 redesigned app screens composed together)
    screens/*.png                 14 cut-out device PNGs used by the Result Showcase
    boxes/
      box-a.png … box-d.png        front-view cut-outs, 800px
      box-a-3q.png … box-d-3q.png  perspective-view cut-outs, 900px (used by BoxStrip + Gallery)
    brand/
      post-box-a.jpg … post-tris.jpg, post-4box.jpg, post-app-verde.jpg, post-app-arancione.jpg
      volantino-pubblicita-*.jpg, questionare-flyer.jpg
      (all resized JPGs exported from the old session scratchpad's render/out folder)
    cover.jpg, fieldwork.jpg, box-family.jpg, flyers.jpg, social.jpg     UNUSED leftovers from an earlier pass
  projects/aurawake/
    cover.png                      2 app screens on a flat #f4f4f2 ground

public/cv/Valerio-Rosponi-CV.pdf   contains his phone number — owner was told, may want a redacted version (open item)

Media/                          RAW owner material, git-ignored, LOCAL-ONLY (never exists in a cloud clone)
  01-JustCook/                   reports (PDF/DOCX/XLSX), OfficialMedia/{Packaging,Flyers,SocialPosts,Interfaces}
                                  — Interfaces holds 17 Figma device exports (3x scale, 1342×2741), e.g.
                                  HomeFirstScreen.png, FocusMode.png, LiveActivityExpanded.png, BuyReviewOrder.png
  05-AuraWake/OfficialMedia/Interfaces/   Home.png, AlarmSet1.png (3x)

.claude/launch.json              dev-server config — see §8
CLAUDE.md                        persistent rules, auto-loaded every session — the schema/component reference
HANDOFF.md                       this file
```

**How layout/logic is actually split**, for a session about to touch something:
- **Tokens and primitives** (colour, type, spacing, `.trio`/`.span-2`, `.label`/`.field`) live **only** in
  `global.css` — never redefine a size or colour locally in a component.
- **Page-level structure** (which sections exist, in what order, with what frontmatter wiring) lives in
  `src/pages/*.astro` — these files are thin: they import `case/*` components and lay out the fixed section order.
- **Chapter *content*** lives in the MDX files (`src/content/projects/*.mdx`) as a sequence of component
  invocations — a session writing/editing case-study text works almost entirely in MDX, rarely touching `.astro`.
- **Reusable visual logic** (how a stat counts up, how a funnel narrows, how a gallery mosaic packs) lives in
  `case/*.astro` components — a session asked to change *how something looks or behaves* (not *what it says*)
  touches these instead.

---

## 7. Technical Context, Bugs & Tech Debt

**Environment quirks (not bugs, but will burn time if unknown):**
- **Run all `astro` CLI commands through PowerShell**, not Git Bash — Rolldown's native binding fails to load there
  ("Cannot find native binding"). See §8 for the exact command.
- **Dev server serves stale CSS/data after edits** (Vite cache). If a screenshot doesn't reflect a just-made change:
  `preview_stop` then `preview_start` again. After a *schema* change, also delete
  `.astro`, `node_modules/.astro`, `node_modules/.vite` first.
- **In dev, an image keeps the same URL when its source file changes** (no content hash), so the browser serves the
  old cached bytes — hard-refresh or clear the dirs above. **Production URLs are hashed**, so this is dev-only.
- `.claude/launch.json` runs `npm run dev -- --ignore-lock` with `autoPort` so a local session's dev server can run
  alongside another chat's server without a port clash; `astro.config.mjs` reads `PORT` from the environment to
  match.
- **Before any full-page screenshot:** add the `is-in` class to every `[data-reveal]` element (otherwise entrance
  CSS hides them) and, since images are lazy-loaded, either scroll through the page first or set `loading='eager'`
  on the `<img>`s — otherwise captured screenshots come out blank below the fold.
- The old puppeteer verification scripts live in a **previous session's scratchpad**
  (`C:\Users\rospo\AppData\Local\Temp\claude\...\734cf2a2-...\scratchpad\render\`) — they may no longer exist by the
  time you read this; recreate them if so (the pattern is simple: launch `puppeteer-core` pointed at the system
  Chrome binary, navigate, set viewport, screenshot).
- `pdf-lib`, `pdfjs-dist` + headless Chrome, and `sharp` are the toolchain used to extract/compose imagery from the
  owner's raw `Media/` PDFs — poppler and python are **not** installed. The Read tool fails on PDFs over 20MB, so
  split or render first. All of this tooling lives in the scratchpad, never in the repo.
- **Media (images) read with the Read tool get stripped from context later** ("media removed") — when extracting
  facts from an image-only PDF, write notes to a file immediately after reading each part, don't rely on
  remembering it later in the same session.
- Higgsfield image generation is connected but the owner's plan is free-tier and can't generate — don't attempt it
  without asking first (it would also cost credits even if it could).

**Open questions / pending decisions** (ask the owner, don't guess):
1. **LinkedIn URL** in `src/data/site.ts` is still the literal placeholder `https://www.linkedin.com/in/`.
2. **CV may contain his phone number** (`public/cv/Valerio-Rosponi-CV.pdf`) — he was told, may want a redacted copy.
3. **UX/UI filter** is present on every single project, so it doesn't actually discriminate anything in the
   Work-page filter bar — flagged to the owner, still unresolved whether to drop it.
4. **JustCook tools list** currently reads "Figma, Miro" — owner was asked whether to add others, no answer yet.
5. **Hero cover-glimpse at 1280×720** measures only 38px (target ~80px, which it hits at every other tested
   viewport: 80px @1440, 95px @1920, 84px on mobile). Low priority, but a `--peek` tweak would fix it if raised.

**Accepted tech debt / deliberate shortcuts:**
- `Reframes` shows only 3 of JustCook's real 6 reframing cycles (opening, one discard, final framing) — a
  deliberate edit for length, not a bug; the `cycles` prop still correctly renders "6 → 1" as the header.
- `Archetypes` trims each archetype to a quote + 2 traits (Friction/Opportunity) even though the source research
  had more dimensions — same reasoning, kept for scannability.
- Case studies 02–05 still carry **entirely invented** frontmatter facts (year, type, platform, role, timeline,
  team, tools) — these must be replaced through the interview process (Appendix B) before `placeholder: false`.
- `PhoneScroll` removal left no dangling references, confirmed — but the "realistic hand photo" asset idea that was
  attached to it is now simply moot, don't revisit it.
- Box-profile colour hex values used in `BoxStrip`/`Chips` (A `#ffa91e`, B `#488863`, C `#ff7257`, D `#29bcff`) were
  **sampled from the rendered packaging images**, not pulled from an official brand palette file — close enough
  visually, flagged here in case an authoritative source ever turns up.

---

## 8. Run & Test Commands

**Start the dev server** (always via the Claude Code preview tool, never raw `npm run dev` in a bash tool call):
```
mcp__Claude_Browser__preview_start {name: "portfolio"}
```
This reads `.claude/launch.json` → `npm run dev -- --ignore-lock` with `autoPort`.

**Build (verification before every commit) — PowerShell only:**
```powershell
powershell -NoProfile -Command "npx astro build 2>&1 | Select-String -Pattern 'ERROR|page\(s\) built'"
```
A successful build prints `N page(s) built` with no `ERROR` lines.

**Commit pattern** (heredoc avoids quote-escaping issues; attribution line per §3 — check current model before
copying this verbatim):
```bash
git add -A && git commit -q -F - <<'EOF'
<Imperative summary line>

<Optional body explaining the why>

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
git push
```

**Visual verification (puppeteer-core, headless Chrome):**
```js
import puppeteer from 'puppeteer-core';
const b = await puppeteer.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
const p = await b.newPage();
await p.setViewport({ width: 1440, height: 900 }); // also check 390×844 with isMobile:true, hasTouch:true
await p.goto('http://localhost:<port>/work/justcook', { waitUntil: 'networkidle0' });
await p.evaluate(() => {
  document.querySelectorAll('[data-reveal]').forEach((e) => e.classList.add('is-in'));
  document.querySelectorAll('img').forEach((i) => (i.loading = 'eager'));
});
await new Promise((r) => setTimeout(r, 1500)); // let images settle
await p.screenshot({ path: 'out.png', fullPage: true });
await b.close();
```
Use `page.evaluate(() => ({...}))` to pull `getBoundingClientRect()` numbers for alignment/gap verification instead
of judging screenshots by eye.

**Git session-start sync** — see §10 for the full protocol; the short version for LOCAL:
```bash
git fetch origin
git checkout main && git pull
git branch -r --no-merged main        # anything origin/claude/* listed here is unmerged cloud work
git merge origin/claude/<branch>      # for each one found
npm install                           # only if package.json changed
# build (command above) → if OK:
git push
```

---

## 9. Immediate Task & Roadmap

**First step, unambiguous:** run the LOCAL session-start sync from §10 right now — `git fetch origin`, check
`git branch -r --no-merged main` for any cloud work waiting, merge it in, build, push. Only after that is the
working tree guaranteed current. Then re-read this file once more (the merge may have changed it) and check
Appendix A for the latest session-log entry — it states explicitly whether there is an open request from the other
side.

**Next 2–3 steps, in likely priority order:**
1. **Continue polishing JustCook's visual impact if the owner keeps iterating** — the last several sessions were a
   tight feedback loop on exactly this (data/numbers → archetypes/reframing → Design-chapter photography). Expect
   more small, specific visual-direction requests before he considers it finished. Show widget concepts for
   anything genuinely subjective (§3).
2. **Once JustCook is settled, start case study 02 (Rehab)** using the process in Appendix B: read everything in
   `Media/02-Rehab/`, write facts to a notes file as you go, interview the owner about gaps/contradictions, draft
   the MDX with the real chapter skeleton and the `result` frontmatter, replace every invented fact, set
   `placeholder: false`, build/verify/push.
3. **Resolve the small open items in §7** opportunistically — LinkedIn URL, CV redaction, UX/UI filter, JustCook
   tools list — none are blocking, but ask next time the owner is in a decision-making mood rather than letting
   them go stale indefinitely.

---

## 10. Hybrid Flow (Local ↔ Cloud)

**This file is the only memory the two environments share — read this section every session, before touching
anything else.**

| | **CLOUD session** | **LOCAL session** |
|---|---|---|
| Where | claude.ai/code, Linux container, fresh clone each time | the owner's Windows 11 PC (Claude Code desktop/CLI) |
| How to tell which you are | working dir `/home/user/...`, no `Media/` folder | path `C:\Users\rospo\...`, `Media/` folder exists |
| Has `Media/` (raw reports, PDFs, exports) | **No** — git-ignored, never present in the clone | **Yes** |
| Figma MCP / browser automation | Figma MCP may be connected; Chromium via Playwright | Figma MCP; Chrome via puppeteer-core |
| Git permissions | may push **only** to its own `claude/*` branch — check `git branch -r` for the current name, a fresh cloud session may get a different one | pushes directly to `main` |
| Deploy | its work is **NOT live** until merged into `main` | `main` = what Cloudflare actually deploys |
| Best suited for | code, layout, CSS, copy, MDX writing from facts already in the repo or pasted into chat | anything needing `Media/`: reading raw reports, extracting facts, composing covers/boards, Figma exports, image cut-outs; **merging cloud work into `main`** |

The owner's actual routine: he usually works in the cloud; when a task needs `Media/` (or local tooling), he opens a
local session, states what's needed, and says "read HANDOFF.md". He may then return to the cloud. **Both sides must
leave this file fully up to date at the end of every change, written as if the very next message will come from the
other environment.**

### At the start of every session (and every new task inside a long session)

**LOCAL:**
```bash
git fetch origin
git checkout main && git pull
git branch -r --no-merged main        # any origin/claude/* listed = cloud work not yet in main
git merge origin/claude/<branch>      # for each one listed — resolve conflicts per the rule below
npm install                           # only if package.json changed
# build (§8) → if it passes:
git push
```
Then re-read this entire file (the merge may have changed it) and Appendix A. **Tell the owner explicitly that the
cloud work is now live** (pushed to `main`, which Cloudflare deploys).

**Your primary job when resuming a LOCAL session after cloud work exists is exactly this:** read what the cloud
session produced (from the merge diff and from its Appendix A entries), physically reconcile/update the local
files if the merge needs any manual follow-up (e.g. a cloud session left a `REQUEST → LOCAL` for an asset it
couldn't produce without `Media/`), and commit/push whatever is needed to bring the repository to a single
consistent, deployed state. Don't just merge mechanically — verify the result builds and looks right.

**CLOUD:**
```bash
git fetch origin main && git merge origin/main     # bring in local-only work (new assets, notes, fixes)
```
Then re-read this file and Appendix A. **Never push to `main`** (not permitted) — push your `claude/*` branch.

### At the end of every change (both sides)
1. Build, verify, commit, push — LOCAL → `main`; CLOUD → its own `claude/*` branch.
2. Add a new entry at the **top** of Appendix A: date, CLOUD or LOCAL, what changed, what's still pending, and any
   explicit **request for the other side**. Also update whichever of §1–§9 the change actually touches — not just
   the log entry. A session log without updated reference sections is only half a handoff.
3. Commit and push the HANDOFF update **too**, as its own or combined commit. Uncommitted = lost — a cloud
   container is thrown away at the end of its session.
4. **CLOUD only:** always tell the owner explicitly when a change is **not live yet** and needs a LOCAL session (or
   a merged PR) before it reaches the real site.

### Owner's explicit rule for cloud→local handovers (2026-10-04)
When a CLOUD session hits something that needs the local environment, it must:
1. **Say so explicitly** in its reply to the owner, in Italian — what's missing and why it needs `Media/` or local
   tooling.
2. **Do everything else it can first** — code, layout, MDX with `<Todo>` placeholders, asset paths already wired up
   to where the file *will* live — so the local session only has to fill in the gap, not build around it.
3. Leave a precise `REQUEST → LOCAL` entry in Appendix A stating exactly what to produce and where it goes (e.g.
   *"Rehab cover 3840×2400 → `src/assets/projects/rehab/cover.png`"*, *"facts from the Rehab report →
   `notes/02-rehab.md`"*).
4. Push, then give the owner a ready-to-paste message for opening the local chat.

### Passing facts across the boundary
- **Facts extracted from `Media/` go into the repo as plain text**, so the cloud side can use them without ever
  touching the raw files: `notes/NN-name.md`, one file per project — numbers with their source and page, team,
  role, timeline, tools, open questions for the owner. `notes/` is **not** published by Astro (not under `src/`).
- Processed images go to `src/assets/projects/<name>/` as usual (optimised by Astro), video/PDF to `public/`. Raw
  `Media/` itself always stays git-ignored, local-only.

### Finishing a request, and conflicts
- **LOCAL finished a cloud request:** mark it `DONE` in Appendix A, push `main`. The cloud session picks it up by
  merging `origin/main` at its next task start.
- **Conflicts** will almost always be confined to Appendix A (the session log). Resolution: **keep both entries**,
  newest-first, never drop one. For actual code conflicts: prefer whichever side has the more recent stated intent,
  cross-checked against the log — and when genuinely unsure, ask the owner rather than guessing.
- **Never force-push `main`. Never rebase someone else's history.** This is a two-sided shared repo with no PR
  review step in between — a bad rewrite breaks the other side silently.

---

## Appendix A — Session log (newest first; keep ~15 entries, fold older facts into §1–§9 above)

- **2026-10-09 · LOCAL** · Owner: JustCook chapter text "caotico, l'occhio cerca il prossimo testo". Three concepts
  shown (A index rows, B one column, C summary first); owner picked **B, with more breathing room**. Implemented as a
  system, not just for JustCook: `###` groups numbered 01.1… (global.css), Key at h3 Regular, Note = callout under its
  content (self-closing allowed), BigStat/Reframes/Closing captions stacked, Chips stacked, Insights stacked + new
  `compact` variant. JustCook MDX regrouped (no content cut; one new Key in Insights: "Four findings, each one a
  constraint the solution had to respect."; Reflection lead-ins became group titles). Verified with puppeteer at
  1440 and 390. Features still alternate sides (media layout, left as is). Pushed `main`. No open requests.

- **2026-10-05 · LOCAL** · Design chapter made visually impactful (owner meant Design, not Ideate; typographic
  concepts were declined: "intendo impattante visivamente"). The box opens with a BoxStrip: four solid panels in the
  box colours, perspective box inside, hover turns it to the front view (replaces the profile chips; no drop
  shadow). Features: alternate sides, crop .72, devices one full track wide. Gallery: "Campaign" mosaic (the 4-box
  post as a 2×2 tile + 4 box posts + So good + Tris + 2 app posts), then the 4 maze flyers; packaging group dropped
  (the strip shows the boxes). Ideate unchanged apart from the arrow. Pushed `main`.
- **2026-10-05 · LOCAL** · "6 → 1" arrow is now a drawn hairline + chevron (the text arrow was rejected). All Stat
  numbers use proportional figures (clean "1", no tabular foot). Perspective box renders (`boxes/box-*-3q.png`, old
  render/box-*-R.png) added: gallery shows front + perspective rows, box chips preview the perspective view.
  Ideate redesign concepts shown (A sieve of 6 rows, B manifesto of 6 numerals, C before → after): the owner then
  clarified he meant the **Design** chapter, not Ideate — see the entry above. Pushed `main`.
- **2026-10-05 · (this update)** · HANDOFF.md fully restructured at the owner's request into the 10 fixed sections
  above (overview/architecture, art direction, dev rules, anti-patterns, git status, file map, tech debt, commands,
  roadmap, hybrid flow) plus this session log as Appendix A and the JustCook facts as Appendix B. No content was
  dropped — everything from the previous numbered-section version was folded in somewhere. Session was switched to
  model `claude-sonnet-5` (`/model claude-sonnet-5`) partway through — commit attribution going forward reads
  "Claude Sonnet 5" per the active system reminder; §3 and §8 note to re-check this each session rather than
  hard-trusting the line shown there. No site changes. No open requests.
- **2026-10-04 · LOCAL** · JustCook ends with a `Closing`: "JustCook is still a concept… The next version would be a
  tested one." in display size, then "What I take with me — Design the easy path, and people will take it." (owner
  picked it over "Make the right thing the easy thing.") Pushed `main`.
- **2026-10-04 · LOCAL** · Third pass on JustCook: BigStat, Research groups, archetype leaders, Chips with hover
  notes/images, Ideate "6 → 1" + giant cycle numbers, Features with screens, channel cards, brand Gallery, launch
  plan (as a plan), human Reflection; cursor label gains note/image variants. Pushed `main`.
- **2026-10-04 · LOCAL** · Second pass on the case-study text: label roles (sequence / group / field), bigger
  numbers with context lines, archetype "Wants" row + tinted headers, Chips component, plain paragraphs turned into
  metrics, chips, rows, a pull quote and a list (no content removed). Pushed `main`.
- **2026-10-04 · LOCAL** · Case-study text with more character: new `Stat` (count-up), `--fs-stat` token, Metrics
  redesigned, Insights `stat`, Archetypes as a side-by-side comparison of two light boxes, Reframes as a stepped
  funnel with an ink final box. JustCook: Challenge desk-research numbers pulled into Metrics, insight stats added.
  Pushed `main`.
- **2026-10-04 · LOCAL** · Owner: show more of the existing texture (no new divider effect: concepts "dot horizon",
  "rippling line", "halftone dissolve" were shown and declined). Hero texture mask now opaque to 78% (was 50%), so
  the fade happens only near the bottom, in the gap above Selected work. Pushed `main`.
- **2026-10-04 · LOCAL** · Owner: "rendili più visibili" → home texture intensity 0.85 → 1.25. Pushed `main`.
- **2026-10-04 · LOCAL** · Home texture a bit more visible (intensity 0.7 → 0.85) and stronger pointer parallax:
  new `parallax` prop on DepthTexture (layer travel × P), home uses 1.6 (near layer 34 → ~54px). Pushed `main`.
- **2026-10-04 · LOCAL** · Merged `origin/claude/stoic-ride-lj7woi` (fast-forward: hero without band + handover
  rule), build OK, checked with puppeteer at 1440 and 390 (hero transparent, texture fade, cover glimpse 80/84px),
  pushed `main` → live. Note: the dev server served the old hero until restarted (Vite cache). No open requests.
- **2026-10-04 · CLOUD** · Home hero: removed the grey `--paper-alt` band; depth texture intensity 0.5 → 0.7; the
  texture now runs into the gap above Selected work and fades out (mask, opaque to 50%) before it. Verified at
  1440×900 (headless Chromium): hero background transparent, fade ends at the Selected work top, cover glimpse still
  ~81px. → LOCAL: merge `origin/claude/stoic-ride-lj7woi` into `main` to put it live. No other requests.
- **2026-10-04 · CLOUD** · Merged `origin/main` (fast-forward). Added the owner's rule to §10 "Handing work across":
  cloud says explicitly when the local chat is needed, does all it can first, then hands over. No site changes.
  → LOCAL: merge `origin/claude/stoic-ride-lj7woi` at your next start. No open requests.
- **2026-10-04 · LOCAL** · First run of the §10 protocol: `git fetch`, fast-forward merge of
  `origin/claude/stoic-ride-lj7woi` into `main` (only HANDOFF/CLAUDE.md), build OK, pushed. No other unmerged
  `claude/*` branches. No site changes. No open requests.
- **2026-10-04 · CLOUD** · Added the cloud/local protocol and this log; one line in `CLAUDE.md` points to it. No
  site changes. Cloud branch `claude/stoic-ride-lj7woi` = `main` + this HANDOFF/CLAUDE.md update → LOCAL: merge it
  at your next start. No open requests.

---

## Appendix B — JustCook verified facts & the process for the next case studies

### JustCook facts (verified with the owner — the ground truth for `01-justcook.mdx`)
- University project, Sept 2024 – May 2025, across three courses: semiotics of visual representation, sociology of
  communication, psychology of communication.
- Team of 4: Ippoliti Noemi, Pajola Giorgia, Rosponi Valerio, Scognamiglio Marco (sociology coursework was without
  Noemi). Valerio did a bit of everything — his own description: "End-to-end UX designer".
- Research (official report numbers): **41 survey responses, 4 in-kitchen interviews, 3 field observations**;
  thematic grid of 8 themes and 36 codes.
- Key stats: >60% shop once a week; ~50% waste food; of those trying to avoid waste, 95% cite packs too big for one
  person. Desk research: >60% take-away weekly; 44% eat ≥1 fruit portion a day; 92% change habits after moving
  (Lupi et al., 2015).
- Process: CPS with 6 reframing cycles (the "healthy ready-made food" idea was discarded along the way), then a VPD
  (value proposition design) canvas. The two archetypes ("Efficiency seeker", "Conscious aspirer") were synthesised
  **afterwards**, for the portfolio, from the real underlying data — not collected as personas during research.
- Solution: a service built from 4 pre-dosed single-portion boxes (A orange "proteica", B green "energica", C red
  "leggera", D blue "comfort"; 4–5 ingredients, up to 10 recipes, ready in ~20 min, a code inside) plus an app
  (adaptive weekly planning, a reminder timed backwards from the recipe duration, a vertical focus-mode video feed,
  streaks with friends). Brand: the name plays on "Just Eat"; maze-themed flyers; Instagram posts.
- **No usability testing was done** — only a Figma prototype exists. The numbers in the Result section are
  **targets**, never results: −40% food waste in the first month, <20 min box-to-plate, >60% still active at day 30.
- Owner's own reflection on the project: next time, better data analysis, more interviews, actual usability tests,
  more realistic (less ambitious) predictions.
- Tools listed: Figma, Miro — owner was asked whether there were others, no answer received yet (§7 open item).
- Launch plan (written as a **plan**, conditional tense, not a past result — Conad Rovereto was *approached* for a
  pickup-point partnership but it was never confirmed, so never claim it happened): one city first — Rovereto,
  starting with DiPSCo students; one pickup point at Conad Rovereto; word-of-mouth channels (student group chats,
  study-room flyers, shareable posts); signals to watch (boxes collected, codes registered, streaks kept).

### Process for writing the next case studies (what worked for JustCook — repeat this)
1. Read everything in `Media/0N-*/`, writing extracted facts to a notes file (`notes/0N-name.md`) as you go — don't
   rely on holding it all in context, and remember images get stripped from context later (§7).
2. **Interview the owner** about contradictions and gaps found in the raw material: team composition, individual
   roles, exact numbers, whether testing happened, actual results vs targets, what media assets exist.
3. Write the MDX with the real chapter skeleton: Challenge → Research → Insights (alt band) → Define → Ideate →
   Design → [Validate, only if testing happened] → Reflection → `Closing`, plus the full `result` frontmatter. Keep
   it concise — a `<Key>` sentence per chapter, then short paragraphs; pull every number out into a `Metrics`/`Stat`
   instead of burying it in prose (§2 information architecture + the "data with character" pass documented in
   Appendix A).
4. Replace every invented frontmatter fact, set `placeholder: false`, update `categories` to match the real
   project.
5. Build, verify visually with puppeteer at both viewports, push.

### Persistent memory pointer
`C:\Users\rospo\.claude\projects\C--Users-rospo-Documents-ClaudeCode-Websites-uxportfolio\memory\` —
`portfolio-project-goal.md`, `design-taste-feedback.md`. Update these when the owner reveals a new **durable**
preference (not a one-off request) — e.g. the motion-calibration and flat-cover rules now recorded there.
