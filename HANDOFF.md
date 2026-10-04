# HANDOFF — Valerio Rosponi portfolio

This file hands the project over between Claude sessions. Read it fully, then read `CLAUDE.md`, the persistent
rules that load automatically. Where the two disagree, this file is newer (last update: 2026-10-03).

---

## 0. How to work with the owner (read first)

- **Owner:** Valerio Rosponi. Junior UX / digital product / visual designer, 3rd-year BSc "Interfaces & Communication"
  (officially "Interfacce e Tecnologie della Comunicazione") at the University of Trento.
  Git identity: `rosponiv-star` / rosponiv@gmail.com.
- **Language:** always talk to him in **Italian**. All site copy is in **English**.
- **He never edits code.** Every change goes through Claude, so after each change build, commit and push.
- **Iteration style:** he gives short visual feedback ("non mi piace", "torna alla versione precedente", "nessuna").
  - Revert immediately when asked.
  - When he asks for options, show **live interactive concepts** with the `mcp__visualize__show_widget` tool (load
    `read_me` with the interactive module first), then implement only the one he picks.
  - When he asks you to "ask questions", use `AskUserQuestion` with 2–4 concise options and a "(Recommended)" one.
- **Taste:** restraint and the Swiss editorial look win. He rejects noise, filler labels, dark overlays and showy
  motion that serves no purpose. He likes clean grids, precise alignment, generous but not scattered space, and fluid,
  subtle motion.
- **End each reply** with a short Italian summary: what changed, what you verified, and open choices or caveats. Keep
  it scannable, with tables when useful. Say honestly what you did not verify.

---

## 1. Purpose of the site

The portfolio shows **case studies, process and mindset** to recruiters and hiring managers for UX, digital product
and visual design roles (art direction is secondary). It is **not** a "hire me" or self-promotion site, so contact
stays discreet.

Target companies he cited: Belka, Bending Spoons, Apple, Google, Deda, DXC, GPI, Meta and Microsoft. Preferred sectors:
health, fintech, fashion and wellbeing. He is open to remote work but not to relocating for now. He lives between Malè
and Rovereto (TN).

**Hard content rules:**
- No personal or educational backstory: no school history, internships or certifications. The CV covers those.
- No skill percentages, skill bars or proficiency ratings.
- No filler: every element must carry information. The exception he asked for is the small 01/02/03 numbers in the
  nav and in the index.
- Case studies use real numbers only. Projected metrics are presented as **targets**. Show a confident result and the
  process; keep limits for the Reflection chapter. Don't narrate setbacks. Conad: the owner decided on 2026-10-04 to
  NAME Conad as the JustCook pickup store (it appears in the UI and in the Design chapter); still never say it didn't join.

---

## 2. Stack, repo, deploy, environment

- **Framework:** Astro 7 (static) + `@astrojs/mdx` + `@astrojs/sitemap`. Hand-written CSS, no framework. Font: **Geist
  only** (`@fontsource-variable/geist`). Geist Mono was uninstalled.
- **Repo:** `https://github.com/rosponiv-star/uxportfolio-main`, branch `main`. Push works with cached Git
  Credential Manager credentials. `gh` CLI is NOT installed.
- **Deploy:** the owner connects the repo to **Cloudflare** (Pages/Workers: build `npm run build`, output `dist`).
  Domain configured in code: `https://www.valeriorosponi.com` (`astro.config.mjs` `site`, `public/robots.txt`). The
  owner has his own domain on Cloudflare; confirm the exact domain with him if it matters.
- **Machine:** Windows 11, Node 24. **Run `astro` commands through PowerShell**, because in Git Bash Rolldown's native
  binding fails ("Cannot find native binding"). The pattern used everywhere:
  ```
  powershell -NoProfile -Command "npx astro build 2>&1 | Select-String -Pattern 'ERROR|page\(s\) built'"
  git add -A && git commit -q -F - <<'EOF' ... Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com> EOF
  git push
  ```
  Commit messages contain quotes, so use `git commit -F -` with a heredoc. PowerShell `-m @'...'@` broke once.
- **Dev server:** `.claude/launch.json` defines `portfolio` (`npm run dev -- --ignore-lock`, `autoPort`; `astro.config.mjs` reads `PORT`), so it can run next to another chat's server. Start it with
  `mcp__Claude_Browser__preview_start {name:"portfolio"}`.
  - **Known issue:** the dev server often serves **stale CSS/data** after edits (Vite cache). If a screenshot doesn't
    reflect a change, `preview_stop` then `preview_start`.
  - After schema changes, also `rm -rf .astro node_modules/.astro node_modules/.vite`.
- **Verification method that works best:** headless Chrome via **puppeteer-core** (`C:/Program Files/Google/Chrome/
  Application/chrome.exe`). Scripts live in the old session scratchpad
  (`C:\Users\rospo\AppData\Local\Temp\claude\...\734cf2a2-...\scratchpad\render\`). They may be gone; recreate them if
  so.
  - The in-app Browser pane is narrow and its screenshots are tiny or scaled, so it is not reliable for visual checks.
  - Use puppeteer to take clipped screenshots at 1440×900, 1920×1080, 1280×720 and 390×844 (mobile with
    `isMobile/hasTouch`), and to **measure** things in JS: alignment to columns, gaps, how much of the first cover is
    visible at scroll 0.
  - Before screenshots, add class `is-in` to `[data-reveal]` elements, otherwise entrance animations hide content.
- **PDF tooling** (for the owner's media), all in the scratchpad and never in the repo:
  - poppler and python are absent;
  - `pdf-lib` splits PDFs and dumps embedded images;
  - `pdfjs-dist` + headless Chrome renders pages (`chrome-render.mjs`);
  - `sharp` composes boards, contact sheets and cutouts;
  - the Read tool fails on PDFs over 20MB, so split or render them first.
- **Media not kept in context:** images read with the Read tool get stripped from context later ("media removed").
  When extracting facts from image-only PDFs, **write notes to a file right after reading each part**.
- **Higgsfield image generation** is connected but the owner's plan is **free** ("Requires basic plan or higher").
  Nothing can be generated without his upgrade, and it costs credits, so ask first.

---

## 3. File map (what matters)

```
astro.config.mjs            site URL, mdx, sitemap, prefetch, devToolbar off
src/styles/global.css       ALL tokens (colour, type scale, spacing), grid primitives, prose, reveals, view transitions
src/layouts/Base.astro      <head>, Header, Footer(showContact), global script
src/scripts/site.ts         reveals (IntersectionObserver rootMargin -1%), header hide-on-scroll, cursor label
                            (data-cursor / data-cursor-theme), scroll-spy, progress bar, video autoplay
src/data/site.ts            name, email rosponiv@gmail.com, LinkedIn (STILL A PLACEHOLDER URL), CV path, nav
src/components/
  Header.astro              name left; nav 01 Work / 02 Playground / 03 About (micro numbers, active = signal colour)
  Footer.astro              Contact row (email, LinkedIn, Résumé PDF), giant "Valerio Rosponi" wordmark, ©
  Section.astro             THE section pattern (rule, title cols 1–3 sticky, body cols 4–12; `stacked`, `tone="alt"`)
  Collection.astro          shared Work/Playground block: title, filters, Grid/Index switch, grid slot, index table + script
  Card.astro                generic card (media slot + hover caption bar)
  ProjectCard.astro         Card + Cover for a project
  Cover.astro               project cover: real image/video or placeholder (tone colour + faint grid + title)
  DepthTexture.astro        hero background: 3-layer grain, parallax + "breath" near cursor (intensity 0.5)
  RegistrationField.astro   old cursor-reactive "+" field; now only the Playground experiment
  case/*.astro              Chapter, Note, Figure, Metrics, Insights, Reframes, Archetypes, Todo
src/lib/projects.ts         getProjects, slugOf/hrefOf/numOf, chapterId/chaptersOf, CATEGORIES (re-exports categoryId)
src/lib/collection.ts       categoryId, gridSizes (all 'half'), yearSpan (unused now)
src/content.config.ts       projects schema (incl. categories enum)
src/content/projects/       01-justcook.mdx (REAL), 02-rehab, 03-smart-home-ecosystem, 04-realiti, 05-aurawake (PLACEHOLDERS)
src/pages/index.astro       home: hero band + Collection(work) + How I work
src/pages/work/[slug].astro case study template
src/pages/about.astro, playground.astro, 404.astro
src/assets/valerio-rosponi.png   portrait (About)
src/assets/projects/justcook/    cover.jpg, fieldwork.jpg, box-family.jpg, flyers.jpg, social.jpg (prepared, CURRENTLY UNUSED)
public/cv/Valerio-Rosponi-CV.pdf  CV (contains his phone number — owner was told; may want a version without it)
Media/                      raw owner material, git-ignored (01-JustCook/... reports, OfficialMedia/ packaging, flyers, posts, Interfaces/)
CLAUDE.md                   persistent rules (auto-loaded)
```

---

## 4. Design system (current state)

### Colour (`global.css :root`)
| Token | Value | Use |
|---|---|---|
| `--paper` | `#fdfdfc` | page background (near-white, slightly cool) |
| `--paper-2` | `#f2f2ef` | placeholder surfaces, hover fills |
| `--paper-3` | `#e8e8e4` | |
| `--paper-alt` | `#f3f3f0` | tinted bands (home hero, How I work, case Overview/Key insights/Outcome, About "What I bring") |
| `--ink` | `#111111` | text |
| `--ink-2/3/4` | `#33332f / #6b6b65 / #8a8a84` | secondary text greys |
| `--rule` | `rgb(17 17 17 / .08)` | row hairlines |
| `--rule-strong` | `rgb(17 17 17 / .22)` | section rules |
| `--signal` | `#3d5a73` slate | single accent, sparingly (active numbers, progress bars) |

History: the background went `#f5f5f0` → `#fafaf8` → `#fcfcfb` → `#fdfdfc` (2026-10-03, "ancora leggermente più bianco"). The accent went orange `#c93a14` → green `#2b9e4d`
(he didn't like it) → slate `#3d5a73`, chosen from colours derived from the cover tones. No gradients, no
fluorescent colours.

### Type (Geist only)
| Token | Size | Use |
|---|---|---|
| `--fs-mega` | clamp → ~168px | case-study title, footer wordmark, Next band title |
| `--fs-display` | 30→60px, **Regular 400**, lh 1.1 | page-opening statements (home hero, About, Playground, 404) |
| `--fs-h2` | 32→48px, Medium | section titles ("Selected work", "How I work", chapters) |
| `--fs-h3` | 22→28px | item titles (principles, insights, rows, index titles) |
| `--fs-lead` | ~19→23px | leads; **card titles** use lead/Medium |
| `--fs-body` | 17px | running text |
| `--fs-small` | **16px** | nav, filters, meta, notes, captions |
| `--fs-label` | 12px | `.label`: Geist **Medium 500**, uppercase, 8% tracking, tabular figures |

He tried Regular-weight labels with 6% tracking and a no-wrap card eyebrow, then **reverted**: keep labels at 500.
The selected filter or view underline is **1.5px** (he asked for something between 1px and 2px).

### Layout
- 12 columns, `--margin` clamp(16–48px), `--gutter` clamp(16–24px).
- Spacing tokens: `--space-1…6` (8/16/24/32/48/64), `--space-block`, `--space-item`, `--space-section`.
- Case-study sections: title in cols 1–3, body in 4–12 split into 3 tracks (`.trio`). Verify alignment with a JS
  audit, not by eye.

### Motion
- Medium level. Always respect `prefers-reduced-motion`.
- Hero words: blur-fade focus-in per word. The earlier masked slide-up cut the letters and was rejected.
- Page view transitions are on.
- Cursor label "Read case study" follows the pointer over links; it inverts on dark next-bands.

---

## 5. Pages (current state)

### Home `/`
1. **Hero band**: full-bleed `--paper-alt`, `DepthTexture` (intensity 0.5), statement in `.display` spanning
   **cols 1–11**:
   > I'm Valerio Rosponi, a UX and digital product designer studying Interfaces & Communication at the University of
   > Trento, based in Trentino, Italy.

   Height is `min-height: max(360px, 100svh − --peek)`, where `--peek` = gap + `--work-head` (122px; 180px under
   960px) + space-item + ~56–96px. The goal: at scroll 0 the hero dominates and the Selected work header plus the top
   **~80px of the first row of covers** peek in. Measured last: 80px on laptop, 84px on mobile, 95px at 1920, 41px at
   1280×720.
   - Location reads "based in Trentino" (owner's choice, to avoid repeating "Trento").
   - Re-measured after cols 1–11 (2026-10-03): 80px at 1440, 95px at 1920, 84px mobile, only 38px at 1280×720.
2. **Selected work** (`Collection`): no top rule on home, because the band edge separates it.
   - Row 1: title.
   - Row 2: filters on the left (cols 1–9) and the Grid/Index switch on the right (cols 10–12), on one baseline.
   - Filters: `All 5 · UX/UI 5 · Service design 1 · Product 3 · XR 1 · Research 1` (counts come from each project's
     `categories`). UX/UI is on every project, so the owner was told it doesn't discriminate; it is unresolved.
   - **Grid:** two equal columns of 4:3 covers with an **8px gap in both directions**.
   - **Card hover (chips, 2026-10-03):** inspired by a reference the owner sent. The cover zooms out to 0.95 over
     the project tone and three square paper chips (1px --rule inset) rise in bottom-left, staggered 60ms: title, type +
     platform, year. Cursor label stays plain "Read case study". Focus-visible = hover. Unlinked cards: text below.
     Rejected on the way: paper bar covering the cover; cover shrinking to fit the bar; E2 rich cursor label ("too
     particular vs simple"); corner tag, free text, slim line; tech-editorial variants E3/E4/E5/B4/B5/B6.
   - **Touch:** text sits below the cover and rows get a 48px gap.
   - **Card entrance:** full-size fade with the inner image settling from scale 1.06; the 2nd card of a row is delayed
     120ms. The old clip-path "curtain" made cards look narrow before animating and was rejected.
   - **Index view:** table (No., Title, Type, Role, Year); the cover preview follows the cursor; the view is remembered
     in localStorage (`view:work`).
3. **How I work** (band `tone="alt"`): five principles, each with an "In practice" line.
4. **Footer**: contact row, wordmark, ©. "Back to top" was removed.

### Case study `/work/[slug]` (in order; restructured 2026-10-03)
Owner's brief: "more concise, more impactful, no filler; a recruiter sees interface and result at first glance, and
can dig into the whole process and way of thinking if they want".
1. **Back button**: outlined pill with a static chevron (animated arrow rejected).
2. **Title** (mega) + **tagline** (lead, one sentence).
3. **Cover** (16:10).
4. **Overview** (no band): ink top rule (other sections have a grey one), Problem / Approach / Outcome (one sentence
   each), then the facts grid, separated by space only. Gutter hairlines were tried and judged "too many lines".
5. **Result** (alt band): `result` frontmatter. When `result.showcase` exists (JustCook), the section is stacked
   and full width: one-line text (body lane) → `case/Showcase.astro` → targets. Showcase (owner, 2026-10-04: grey band,
   small numbered labels, inside the grid, light parallax): 01 Tonight (Home, Change box, Focus mode; trio on tracks
   A/B/C, staggered), 02 Live Activity (pair, full 12 cols, devices cropped to the top 40% on a hairline), 03 Widgets
   (trio cropped to 50%), 04 Buy boxes (quad, 12 cols), 05 The week (Plan, Streak, Ingredients; staggered). Shots are
   the Figma "… · device" frames exported 3x into `Media/01-JustCook/OfficialMedia/Interfaces/*.png`, cut out from the
   #f5f5f5 frame fill (flood fill + rim un-blend, old scratchpad `render/cutout.cjs`) and resized to 960px wide into
   `src/assets/projects/justcook/screens/`. Phones: one swipe row per group.
   Motion ("more evident, smooth, premium, never attention-grabbing", 2026-10-04): each group reveals as a whole once
   20% into the viewport (own IntersectionObserver). Full devices rise 80px and settle from scale .96 (1.6s ease-out,
   140ms apart); cropped groups draw their hairline, then the devices emerge from behind it (translateY 42% → 0,
   1.7s). Inertial parallax (lerp .09, speeds .02/.1/.05/.13, max 72px) on uncropped groups, desktop only. Hover lifts
   a device 8px. Everything off with reduced motion. Otherwise (placeholder projects): Three phone-ratio screens + one wide board (placeholders until real
   images: the owner chose placeholders for now, NOT the prepared JustCook boards), 1–2 sentences, key numbers
   (JustCook: "Targets for a pilot"). On phones the screens become a horizontal swipe row.
6. **Process** (`case/ProcessIndex.astro`, owner picked option C "process line", in house style): steps hang from an
   ink line on 10px ticks, each with number, title (lead) and a 2–4 word `summary` from the MDX Chapter tag (the
   bare version looked "scarna"). When the inline index has scrolled away, a slim fixed bar under the header shows the same
   steps; each segment fills in --signal as its chapter is read (replaces the 2px progress bar), current step in ink.
   Sticky chapter titles and scroll-padding move down while the bar is on (`html.has-pbar`, `--pbar-h`). Phones:
   vertical list; bar = segments + "04 / 07 DEFINE". Rejected alternatives shown: row TOC with key sentence, dotted
   book TOC, sticky side index; Overview as dark band, stacked sentences, text + data column.
7. **Chapters**: Challenge, Research, Insights (alt), Define, Ideate, Design, [Validate], Reflection. Each opens with
   `<Key>` (lead, ink), then short paragraphs at --fs-read (19px). Archetypes trimmed to quote + 2 traits; Reframes to
   3 of 6 cycles. Owner chose short paragraphs over bullets or collapsible details.
8. **Next case study band** (unchanged).

PhoneScroll (sticky device scene) was **removed** by the owner on 2026-10-03.

### About `/about`
`.display` statement, Approach (portrait in grayscale that turns colour on hover, plus 3 paragraphs), What I bring
(alt band, 6 strengths), Toolkit (Figma; Stitch & AI tools; Unity; IDEs), Now (studying, based in, looking for),
Contact. The footer contact row is hidden on this page.

### Playground `/playground`
`.display` "Things made for the joy of it." plus a lead. A `Collection` "Experiments" with its own vocabulary
(Interaction, Generative, Motion, Typography, Code). One experiment, the live **Registration field** canvas, as a Card
without link.

---

## 6. PhoneScroll

Removed on 2026-10-03 ("togli il cellulare interattivo"). The hand-photo idea is moot. Do not reintroduce.

---

## 7. Content status

| Project | Status | Notes |
|---|---|---|
| 01 JustCook | **Written, real data; real cover** | Cover (2026-10-04) = 3 device screens from Figma page "JustCook — Redesign v3" (frames "Home · first screen · device", "Home · scrolled · device", "Boxes · device", exported PNG 3x = 1342×2741, saved as `Media/01-JustCook/OfficialMedia/Interfaces/HomeFirstScreen.png`, `HomeScrolled.png`, `Boxes.png`). The exports carry the Figma frame fill #f5f5f5, so the cover ground and tone are #f5f5f5 (no cut-out needed). `src/assets/projects/justcook/cover-app.png`, 3840×2400, phones 1800px tall, 96px gaps. Older prepared boards stay unused in the same folder. Result = interface showcase (see §5). |
| 02 Rehab | placeholder | invented facts (Digital health service, 2026, Product Designer, team lead…) |
| 03 Smart Home Ecosystem | placeholder | invented facts |
| 04 Realiti | placeholder | invented facts, dark tone |
| 05 AuraWake | placeholder text, **real cover** | cover = Home + AlarmSet1 side by side, 3840×2400, from the 3x PNGs in `Media/05-AuraWake/OfficialMedia/Interfaces`. Flat #f4f4f2 ground (= tone), phones only. Depth experiments were REJECTED (2026-10-03): radial studio light/vignette, cast shadows under the phones, diffuse halo. Do not re-propose. Note: in dev the image URL has no hash, so after replacing an image the browser may need a hard refresh. |

### JustCook facts (verified with the owner)
- University project, Sept 2024 – May 2025, across three courses: semiotics of visual representation, sociology of
  communication, psychology of communication.
- Team of 4: Ippoliti Noemi, Pajola Giorgia, Rosponi Valerio, Scognamiglio Marco (Sociology without Noemi). Valerio did
  a bit of everything: "End-to-end UX designer".
- Research (official report numbers): **41 survey responses, 4 in-kitchen interviews, 3 field observations**; thematic
  grid of 8 themes and 36 codes.
- Key stats: >60% shop once a week; ~50% waste food; of those trying to avoid waste, 95% cite packs too big for one
  person. Desk research: >60% take-away weekly; 44% eat ≥1 fruit portion a day; 92% change habits after moving
  (Lupi et al. 2015).
- Process: CPS with 6 reframing cycles (the "healthy ready-made food" idea was discarded), then the VPD canvas.
  Archetypes ("Efficiency seeker", "Conscious aspirer") were synthesised **afterwards** for the portfolio from real
  data.
- Solution: service = 4 pre-dosed single-portion boxes (A orange "proteica", B green "energica", C red "leggera", D blue
  "comfort"; 4–5 ingredients, up to 10 recipes, ready in ~20 min, code inside) plus an app (adaptive weekly planning,
  reminder timed backwards from the recipe duration, focus-mode vertical video, streaks with friends). Brand: the name
  plays on "Just Eat"; maze flyers; Instagram posts.
- **No usability testing** was done. Only a Figma prototype exists. Targets (not results): −40% waste in the first
  month, <20 min box to plate, >60% active at day 30.
- Owner's reflection: next time, better data analysis, more interviews, usability tests, realistic predictions.
- Tools listed: Figma, Miro. The owner was asked whether there were others; no answer yet.

### Process for the next case studies (what worked for JustCook)
1. Read everything in `Media/0N-*`, writing facts to a notes file as you go.
2. **Interview the owner** about contradictions and gaps: team, role, numbers, testing, results, materials.
3. Write the MDX with the chapter skeleton: Challenge, Research, Insights (alt), Define, Ideate, Design, [Validate],
   Reflection, plus the `result` frontmatter. Keep it concise: Key sentence + short paragraphs.
4. Replace the invented frontmatter facts, set `placeholder: false` and update `categories`.
5. Build, verify with puppeteer, push.

---

## 8. Things tried and REJECTED (do not re-propose unless asked)

- Hero: full-screen statement only (he later wanted the work visible, then a middle ground); compact hero;
  registration-mark field background (replaced by the depth texture); masked word animation; 6 hero layouts
  (monumental name, dark band, project thumbnails inside the sentence, split with role column, merged with Selected
  work); 4 hero→work transitions (curtain sheet, statement shrinking into title, typographic "05 case studies" bridge,
  horizon filter bar). He said "nessuna" to all of these. The current near-full-screen band with a glimpse of covers is
  the accepted compromise.
- Work scroll concepts (13 in total): clip reveal + inner parallax, focus/blur, stacking deck, horizontal pinned track,
  inertia + skew, sticky index with preview, expanding window, focus carousel, accordion strips (and variants with
  labels, tabs and rows), editorial collage. All rejected; the plain grid stays.
- Grid layouts: 12 / 6+6 rhythm, then all-half (kept); a sticky side index next to the cards; facts blocks under the
  cover (right-aligned); facts unfolding in the index; the "N of N projects, years" count line; corner marks on
  covers; a "Read case study" CTA under cards; card text above the cover (moved back below, then into the hover
  bar).
- A **dark scrim on card hover**.
- Mono labels (Geist Mono removed); Regular labels with 6% tracking.
- Accent colours orange and green.
- Animated back arrow; "Back to top" link.
- Next-project band: the in-page "Next" section with an arrow; a registration-field background in the band
  (the cover image background was restored).
- Media boards inside JustCook (removed for now: "ci penseremo dopo").

---

## 9. Open items / next steps

1. **Hero glimpse at 1280×720** is 38px (target ~80). Offer a tweak to --peek if the owner cares.
2. **LinkedIn URL** in `src/data/site.ts` is still a placeholder (`https://www.linkedin.com/in/`). Ask for it.
3. ~~Hand photo for PhoneScroll~~: moot, PhoneScroll removed.
4. **JustCook interfaces redesigned in Figma** (2026-10-03): file `9kVAJhXfvlz569AYMRGGCn`
   (https://www.figma.com/design/9kVAJhXfvlz569AYMRGGCn), page **"JustCook — Redesign"**. The owner asked to turn his
   junior screens into senior-level ones; original screens stay untouched on "Page 1". Choices: English copy, refined
   brand green (not a new direction), full flow + mini design system, Conad kept as pickup store.
   - Variables "JustCook / Color" (brand green 900/700/500/100/50, neutrals, text, box A–D strong/tint/ink, warning,
     dark); SF Pro text styles on the iOS scale ("JustCook/…"); components: Status Bar, Home Indicator, Button (Label,
     Icon swap, Show icon), Tab Bar (Active=Today/Plan/Boxes/Profile), Box Badge (A–D), 25 Icon/* components.
   - Screens (402×874): 01 Today, 02 Plan, 03 Boxes, 04 Focus mode, 05 Buy · method (sheet), 06 Buy · choose boxes,
     07 Review order, 08 Reminder notification. Boards: 00 Foundations, Components.
   - One consistent story across screens: Thu 14, Box D tonight at 20:00, Friday + next Monday without a box, pantry
     A1 B1 C1 D3, cart A2 C2 D1, pickup tomorrow at Conad, Via Rosmini 56.
   - Gotcha: when binding a colour variable in the plugin API, also set the paint's colour to the resolved value, or
     Figma may render the black fallback.
   - Next: owner review; then export screens (2x/3x PNG) for the JustCook Result section and figures.
5. **Covers:** JustCook and AuraWake have real covers; Rehab, Smart Home, Realiti still placeholders.
6. **Case studies 02–05**: the full interview-then-write process.
7. **Filters:** decide whether to drop UX/UI (it is on every project). Confirm the categories per project.
8. **CV** may contain his phone number; he may want a version without it.
9. **Tools** list for JustCook: ask whether to add others besides Figma and Miro.
10. Keep `CLAUDE.md` in sync after every change. It has a few stale lines to fix:
    - the Structure section still mentions "project count";
    - the Type scale says "small (15)" (it is 16) and "project card titles use h2" (cards use lead size);
    - "Collection sections use `stacked`" is outdated (Collection has its own header).

---

## 10. Memory

Persistent memory dir: `C:\Users\rospo\.claude\projects\C--Users-rospo-Documents-ClaudeCode-Websites-uxportfolio\memory\`
(`portfolio-project-goal.md`, `design-taste-feedback.md`). Update it when the owner reveals new durable preferences.
