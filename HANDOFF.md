# HANDOFF — Valerio Rosponi portfolio

This file hands the project over between Claude sessions — LOCAL (Windows PC, has `Media/`) and CLOUD
(claude.ai/code, no `Media/`) — so a new session reaches the same operational awareness as the one that just ended.
Read this file **in full**, then read `CLAUDE.md` (persistent rules, auto-loaded every session). Where the two
disagree, this file is newer and wins.

**New chat: read §0 first (current state: website §0.A, Polimi PDF §0.B, research how-to §0.C, tooling §0.D), then sync git as §10 describes, then re-read this file** — another session may have pushed a
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

## 0. Current state — 2026-10-27 (read this first; it overrides older details in §1–§9)

Two workstreams live in this repo:
- **A. The website** (Astro, live at https://www.valeriorosponi.com): case studies for recruiters and hiring managers.
- **B. The portfolio PDF for the Politecnico di Milano application** (`deck/`, started 2026-10-27): a 16:9 deck built
  from HTML and printed to PDF. Not published on the site. Details in **§0.B** below.

**Git:** `main` = `origin/main`, clean at the end of the 2026-10-27 session (last commits: deck work + this HANDOFF).
**Deploy:** Cloudflare **Worker** `uxportfolio-main` (Workers Builds from GitHub `main`, ~2–4 min). `wrangler.jsonc` +
`worker/index.js` 301-redirect `http://` and the bare domain to `https://www.valeriorosponi.com`; everything else is
served from `dist/` (ASSETS binding, `404-page`, `auto-trailing-slash`). `astro.config.mjs` has `trailingSlash:
'always'`: every internal link ends with "/". Connected MCPs: Figma, Cloudflare (workers/KV/R2/D1/docs only).

### 0.1 Who the owner is and the vision (both workstreams)
- **Valerio Rosponi**, 3rd-year BSc student in Interfaces and Communication Technologies (L-20), University of Trento;
  diploma in Informatics and Telecommunications (Istituto Tecnico C.A. Pilati, Cles); based in Trentino; Italian native,
  English B2 (Cambridge). CV: `C:\Users\rospo\Downloads\CV_Valerio_Rosponi.pdf` (contains the phone number: never put it
  in public material). Recognition (from the CV): UX Challenge 2026 Social Impact Award (Trentino Innovation Hub, for
  Gruppo Spes, team leader + UX designer), AI2B University AI Championship 2026 (participant), Italian Olympiads in
  Informatics 2022 (participant), 2022 internship as UI developer (front-end of a Java school-management system in a
  startup simulation).
- **Positioning:** interaction and UX designer with a computer-science background: designs end to end, from research in
  people's real context to interfaces he can also build and test (Figma, Claude/Codex coding agents, Unity, Meta Quest,
  Affinity/Illustrator, Git).
- **Vision of the site:** show case studies, process and mindset; not a "hire me" site; contact stays discreet. Swiss
  editorial base + tech precision + a touch of brutalism (oversized type); one accent (`--signal` #3d5a73); no
  gradients, no fluorescent colours; medium motion; restraint over clever interaction.
- **Vision of the PDF:** get into the MSc Digital and Interaction Design (DID) at Politecnico di Milano. **PROCESS IS
  THE FOCUS** (owner, in capitals): the approach and skills must show through how each project is explained, not
  through separate slides. The course is about interactive systems with physical, connected, tangible and embodied
  parts: every project must show its **system** and its **prototypes**, not only screens.

### 0.2 Working with the owner (current, both workstreams)
- Italian to him; English in all site/PDF copy. He often asks for **"caveman mode"**: terse answers, tokens spent on the
  work. He is short on credits: batch edits, avoid re-reading big files, take only the screenshots you need.
- **"Se hai domande falle, non lasciare nulla al caso"**: ask (AskUserQuestion, 1–4 questions with options and a
  "(Recommended)" pick) before guessing facts, purposes or placements. **Never invent facts or numbers.**
- He reviews by **annotated screenshots** (red notes on the page). Do every note, then show proof (screenshots).
  Short reactions: "rimetti com'era" / "torna indietro" / "scuri come prima!" = revert exactly.
- For taste questions show quick visual options and implement only his pick. He edits Figma himself.
- LOCAL sessions push `main` after every change and add an Appendix A entry each time. Commit trailer:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` (or whatever the current system reminder says).
- **Rejected in the last sessions (do not bring back):** hand-held phone mockups in JustCook (all of them, after many
  attempts), scroll-linked zoom on images, chips of any kind (step chips, number chips, pill tags), rules/dividers above
  `###` groups, uppercase-label group titles, big faint "6 → 1" cycle numbers, pastel project colours in the PDF,
  arrow lines on links (now small chevrons), tinted boxes for dense comparisons.

### 0.A The website

**Projects (`src/content/projects/`)**
| File | Status |
|---|---|
| `01-justcook.mdx` | **Live, complete.** Interfaces = owner's Figma **Redesign v3** (file `9kVAJhXfvlz569AYMRGGCn`, page `2056:180`). No mockups on the page. Structure in "JustCook page" below. |
| `02-rehabeat.mdx` | **Live** since 2026-10-12. Real text (`notes/02-rehab.md`); Result showcase from Figma `xmb1334lJ54M35DwB9PFnl`. Still placeholders: Design Features rows 01, 02, 03, 05. To-do: a working-prototype section. **Not** in the PDF line-up. |
| `03-smart-home-hub.mdx` | Text written (PIG = "Progettazione di Interfacce Grafiche", Sep–Dec 2025, 3 students, Android MD3); `notes/03-smart-home-hub.md`. `placeholder: true` (Coming soon) until the owner sends interfaces. **Main project 01 in the PDF.** |
| `04-realiti.mdx` | Placeholder with INVENTED facts (only the name "Realiti" is real; XR / Meta Quest project). Sources in `Media/04-Realiti/`. **Additional project 04 in the PDF.** |
| `05-aurawake.mdx` | Text written (HCI 1, spring 2024, team of 2, mobile app + alarm + wearable); `notes/05-aurawake.md`. Coming soon. **Additional project 05 in the PDF.** |

**Case-study structure "B-mix" (owner, 2026-10-20; full rules in CLAUDE.md "Writing a case study")**
- Intro (back link with a small chevron) → cover → **Overview** as one cell grid (3 sentence cells + 6 fact cells, no
  rule above) → **Result** (unchanged: showcase + bare numbers) → **Process** = clickable index rows (number, h3 title,
  summary, chevron that steps on hover) → chapters.
- Chapters: sticky title in the head lane; body starts with `<Key>` (h2 Regular); `###` groups = h3 Medium sentence-case
  titles, **no rule above**; paragraphs `--fs-read`; numbers/findings/cycles = hairline **cells** (`.cells`/`.cell` in
  global.css, 6 units); numbered lists = plain list (number + point, light hairlines); item titles inside cells/rows =
  lead Medium; sequence numbers = small signal labels, never chips.
- Components changed: `Key` (h2 Regular), `BigStat` (full-width cell), `Metrics` (cells in chapters, bare in Result),
  `Insights` (cells 2×2 / thirds / 3+2), `Reframes` (row of cells with subgrid; `cycles` no longer drawn), `Archetypes`
  (light: continuous row hairlines, no boxes/tints/column rules), `Chips` (light row; `cards` = About-style tool tiles
  with optional `logo` raw SVG), `Features` (rows: device on the hairline, text centred; new `also`/`alsoAlt` = two
  screens side by side, `note` = quiet line under the text), `Closing` (bold sentence in mega, all ink: owner loved it),
  `ProcessIndex` (index rows + fixed bar), `Gallery` (no hairline under the last cutout group; cutout groups are swipe
  rows on phones). `Spot` exists but is unused.
- Logos: `src/assets/logos/` (Simple Icons CC0 + a hand-drawn `qr.svg`; Instagram/WhatsApp/TikTok added 2026-10-20).

**JustCook page (`01-justcook.mdx`) — exact current structure**
- Cover `cover-app.png` (3 phones on #f5f5f5). Result showcase: Tonight (trio) · From box to stamp (trio stagger) · Live
  Activity (pair crop 0.4) · Widgets (quad crop 0.5) · Buy boxes (quad) · The week (quad).
- Research: Methods cells (41 / 4 / 3) + Analysis boxed cells (8 themes, 36 codes = "short tags marking what each passage
  of an interview or field note is about; the same 36 applied to all of them").
- Design, app part: Note (Decision) → `Features` alternate crop 0.82: 01 Adaptive planning · 02 Swap tonight's box ·
  03 A timely nudge (widget, crop 0.32) · 04 One code per box (flat `lid-code.png`) · 05 Focus mode · 06 **Hold to stamp**
  = pair row (`meal-stamp.png` + `meal-stamped.png`, text: "Dinner ends with a gesture, not a checkbox: press and hold
  today, and the stamp lands on the week like on a loyalty card.", note Principle: "A reward people perform themselves
  feels earned. Right after the stamp, tomorrow's meal and its reminder are one tap away.") · 07 Streaks with friends.
  Then `### Outside the app` (Gallery cutout in four moments incl. the 19:45 notification `out-notif-start-cooking.png`,
  Figma 2319:5724) → Brand and campaign (Channels = tool tiles with Instagram, WhatsApp, QR, TikTok logos) → launch plan
  → Reflection ("If I started again" plain list) → Closing in mega.
- The stamp is an **emotional gesture**, not a safety lock (owner's guidelines
  `C:\Users\rospo\Documents\Designing\1percent\1percent-design-guidelines.md` §8–§9). Never invent data for it.
- Mockup source photos kept only locally in `Media/01-JustCook/mockups-source/` (none in use).

**Home, About** unchanged since 2026-10-16 (home hero with per-word blur reveal: "lasciamola così"; About: drawn column
hairlines + two-sentence statement + B/W portrait + five accordion sections).

### 0.B The portfolio PDF for Politecnico di Milano (`deck/`)

**Admission facts (verified 2026-10-27; re-check the new admission guide published ~21/22 April each year)**
- Source: School of Design "Open Day LM 2026 — Modalità di ammissione" deck
  (https://www.design.polimi.it/fileadmin/user_upload/upload/News_2026/Open_Day_LM_2026_Presentazione_Modalita_Ammissione.pdf).
- Documents: **portfolio PDF max 20 MB, no imposed graphic format**; CV PDF max 4 MB (must highlight extra training and
  professional activities); motivation letter PDF max 4 MB; bachelor study plan PDF max 4 MB (other universities).
  Italian or English. **File names without special characters, hyphen included** (use `Rosponi_Valerio_Portfolio.pdf`).
- Scoring: **portfolio max 50** (below 30/50 = declared not eligible, whatever the GPA) + **CV max 20** + weighted GPA
  (in 30ths) + **5-point bonus** if DID is the first choice. DID has **50 places** (Italian/EU), taught in English at
  Bovisa, sections DID1/DID2. Applications ~**22 June – 7 July**, 12:00 (to be confirmed), rankings ~31 July.
- Prerequisites: weighted average ≥ 25/30 for other Italian universities; ≥ 145 CFU by the application date for
  undergraduates; English certificate uploaded by the deadline (Cambridge ≥ B2 First grade B or ≥ C1 Advanced grade C,
  IELTS ≥ 6, TOEFL iBT ≥ 78…; `C:\Users\rospo\Documents\Magistrali\Polimi\requisito inglese.pdf`).
- Curricular requirement (helpdesk ticket #101683052, 19 Oct 2026, saved in `…\Magistrali\Polimi\`): the 36 CFU in
  CEAR-08/D + IINF-05 can include Informatics (INFO-01/A) credits; then he is evaluated with candidates who need no
  curricular integration, provided GPA ≥ 25/30 and a valid English certificate.
- **Course profile** (manifesto `…\Magistrali\Polimi\manifestoDID.pdf` + https://www.polimi.it/en/education/laurea-magistrale-programmes/programme-detail/digital-and-interaction-design):
  designing and developing interactive artefacts, digital AND physical: interactive and connected products, responsive
  environments, tangible and multimedia interfaces. Year 1: Embodied Interaction Studio (Design of Interactive Systems,
  Design of Blended Interaction, Tangible and Embedded Technologies) or Envisioning AI through Design; Digital Design
  Studio; Hardware & Software Technologies for Design; UX Design; Cognitive Science for UX; Digital Art. Year 2: Final
  Design Studio (complex products/systems, technologies for connected products, envisioning interactive scenarios; or
  Smart Wearables), Living Interaction Design or Virtual & Physical Prototyping, electives, internship, thesis. The
  school has a prototyping lab with microcontrollers and sensors.
- **Reference:** Silvia Gori's accepted portfolio, `…\Magistrali\Polimi\SILVIA_GORI_Portfolio.pdf` (19 MB, 59 slides
  16:9, same UniTrento BSc, opened with her UX Challenge 2025 Social Impact Award project). Good content model (cover,
  contents, about, internship, case studies with overview & role, process, solution, outcome, learnings, additional
  projects incl. programming/ML, "what sets me apart"); graphically loose (alternating green/white/black, small text,
  bullets, no constant grid): that is where we beat it.

**Owner's decisions so far**
- English. Site identity + a strong accent. No photo of him. A short "Where I'm heading" slide (course themes ↔ projects;
  personal motivations stay in the motivation letter). AI2B and the Olympiads = participation only. No thesis yet.
- Removed on purpose: "How I approach design" and "What I bring" (must show through the projects: PROCESS FIRST).
- Recognition: highlights only in "Who I am" (room for 8, 4 per row); the full list goes in the CV (scored separately).
- **Line-up:** main **01 Smart Home Hub**, **02 JustCook**, **03 UX Challenge 2026 (Gruppo Spes, app/web only) OR a new
  thesis project (to be decided)**; additional **04 Realiti**, **05 AuraWake**. Rehabeat is out (flagged to the owner as
  the closest to the course; he chose this line-up).
- The owner has prototype material for Realiti (XR), AuraWake and Smart Home; a small new physical prototype
  (Arduino/ESP32 + sensor) before July is "maybe, to evaluate" (it would fill the biggest gap vs the course).
- Colours: cover ultramarine `#1f3c88`; projects **dark** with white type: 01 teal `#2b5c6b`, 02 terracotta `#b04a32`,
  03 aubergine `#5a3a5e`, 04 forest `#2e5e4e`, 05 ochre `#8f6519`. Pastels were tried and rejected ("scuri come prima!").

**The system (deck/deck.css + deck/index.html)**
- Canvas **1920×1080**; **12 columns** of 122 px, **24 px** gutters, **96 px** side margins; 8 px rhythm.
- **Chrome** on every slide at y 56: section (signal number + name) left, sub-title centre, page "NN / NN" right.
  **Content frame** y 144 → 984 (`.frame`, a 12-col grid).
- Type (site scale ×1.5): label 18 (uppercase Medium 8%), small 22, body 26, lead 34, h3 44, h2 72, display **88**
  (statements: one sentence per line across the 12 columns), mega 232 (cover name at 312, project-cover title 136).
- Site rules reused: Geist only (local woff2 from `node_modules/@fontsource-variable/geist`), paper #fdfdfc, ink greys,
  `--signal` for small sequence numbers, hairline **cells** (label top, content bottom), light **rows**, grey hatched /
  grey-text **placeholders** (`.ph`, `.ph-box`).
- **Colour slides** (`.slide--color`, `--pc`): full-bleed colour, white type, the 12 columns drawn as faint hairlines
  (`.cols`, the site About motif). Project covers (`.pcover`) add a tone-on-tone mega number bleeding off the
  bottom-right corner (`.pcover__num`, 860 px, colour = 78% --pc + black).
- **Generated by the inline script** (so the deck scales): page numbers; the Contents (three groups: About · Main
  projects · Additional projects, with colour swatches, all links); the Selected projects index (3 large main images
  3:4 + 2 smaller additional 16:10 in the last track, number + title only; placeholder = the project colour). Sources:
  slides with `data-intro` (About entries) and every `section.pcover` (`data-num`, `data-kind` main|additional,
  `data-title`, `data-sub`, `data-ph`, `--pc`). **Adding a project = adding a cover section; its content slides go
  right after it.**
- `?grid` draws the columns (preview only); `?accent=hex` overrides `--accent`.

**Current slides (10):** 01 Cover (ultramarine, name 312 px, "Interaction and UX designer with a background in computer
science.", application + contact) · 02 Contents · 03 Who I am ("Useful to as many people as possible. / Beautiful
enough to make them stay." + Profile / Education / Details + Recognition row) · 04 Where I'm heading ("Designing the
experience, / and building the technology behind it." + 3 cells: Connected products and systems → Smart Home Hub,
AuraWake · Tangible and embodied interaction → AuraWake, Realiti, JustCook · Physical and virtual prototyping →
Realiti, Smart Home Hub) · 05 Selected projects · 06 cover 01 · **07–17 main-project TEMPLATE** (below) · 18–21
covers 02–05 (real facts from the MDX; Realiti and project 03 still placeholders) · **22–25 AuraWake content** (below).

**AuraWake (05, additional) — 4 slides after its cover (2026-10-27).** Chosen for its physical interaction (objects,
states, signals, links). Sources: `notes/05-aurawake.md` + `C:\Users\rospo\Documents\ClaudeCode\Design\AuraWake\AuraWake - Interaction Design Spec.md`
(Oct 2026 spec; owner: "usa le info, non importa di quando sono"). Slides (`data-page`: colour + name from the cover,
no process bar): **System** (SVG map: phone, bracelet → base (hub) → lamp, shutters, diffuser; cloud optional; links
labelled Wi-Fi local / BLE 5 / Thread-Matter) · **One night** (swimlane generated from data in the script: 9 moments
21:30→07:10 not to scale; lanes You/Bracelet/Base/Phone = events, Lamp (amber area)/Shutters/Sound (indigo)/Scent =
0–100% areas; smart-window band 06:00–06:30) · **Gestures and signals** (take the bracelet / palm 2 s / put it back,
illustration placeholders; light-line states drawn as waveforms) · **App and safety** (3 phone placeholders Evening
21:40 / Night 03:12 / Morning 07:10 + "What if…" list). Product colours used only here: `--night` #7a86e8,
`--dawn` #f2c074 (from the spec). **Placeholders:** object illustrations (owner has "un'idea complessa" for them) and
app screens (redesign in Figma `SVEGLIA-1 › Redesign · Home`). Physical prototype: owner decides later.

**Main-project template (2026-10-27, owner: "pagine mockup con la struttura generale")** — 11 slides after cover 01
(ids `p01-*`), all copy grey placeholder saying what goes where; to be filled with Smart Home Hub only when the owner
says ("un progetto alla volta, per ora aspetta"), then copied for 02/03. Order: Overview (h2 sentence + cell grid:
Problem/Approach/Outcome + Course/Timeline/Team/My role/Methods/Tools) · 01 Context (text + 2 stat cells | photo
16:10) · 02 Research (3 photos 5:2 + 4 method stat cells) · 03 Insights (quote + 4 cells: number, title, evidence,
stat) · 04 Framing (HMW in h2; two personas compared on rows | 3 design principles) · 05 Ideas (4 square sketches,
the chosen one outlined in --pc) · 06 System (legend | SVG map: people → touchpoints → hub → devices, dashed data,
dashed space boundary; generic, redraw per project) · 07 Prototypes (3 iterations: image, fidelity, tested, changed) ·
08 Solution (4 phones on a hairline + captions) · 08 Solution, key interaction (Trigger/Action/Feedback/Why | photo
16:10) · 09 Outcome (2 stat cells | "If I started again" list).
Mechanics: a content slide has `data-step` (key from `STEPS` in the script; "" = overview); the script copies `--pc`
and "NN Title" (`[data-proj]`) from the preceding cover, writes the kicker (`[data-kick]` = step number in --pc +
name) and appends the **process bar** (`.steps`, bottom 36 px: 9 segments, done = grey line, current = --pc line +
ink label). On those slides the frame ends at y 952 (`bottom: 128px`). New token `--fs-stat` 136 (`.stat`).
`build.mjs` now empties `out/preview/` each run. Contact-sheet helper (git-ignored): `deck/out/_sheet.mjs <dir> <out.jpg>
<regex> [w] [cols]`.

**Build**
```bash
node deck/build.mjs              # → deck/out/Rosponi_Valerio_Portfolio.pdf + deck/out/preview/NN-id.png (1920×1080)
node deck/build.mjs --grid       # previews with the column grid → deck/out/preview-grid/
node deck/build.mjs --accent=1f3c88
```
`puppeteer-core` is a devDependency; Chrome path from `CHROME` env (default the Windows install). `deck/out/` is
git-ignored: rebuild it. The script warns if the PDF exceeds 20 MB. Internal `<a href="#id">` links and mail/web links
stay clickable in the PDF. Contact sheet for review: resize the previews with sharp (640×360 each, 3 per row).

**Next for the PDF (in order)** — see also §9
1. **Template built (07–17), waiting for the owner's review.** Then fill it with **01 Smart Home Hub** only when he
   says so. Material: only what is in the report (`Media/03-Smart Home Ecosystem/REPORT FINALE PIG.pdf`: sketches,
   Design Space, flows; owner 2026-10-27) + interfaces still undecided (original report MD3 screens vs the Oct 2026
   Figma redesign in `om273DJAb0sL3whUHJE0IO`, notes in `C:\Users\rospo\Documents\ClaudeCode\Design\HANDOFF-PIG-REDESIGN.md`):
   ask. Additional projects need a shorter template (~3–4 slides).
2. Decide project 03 (UX Challenge 2026 vs thesis) and get its material (the owner has UX Challenge material).
3. Real photos for the Selected projects index and, if wanted, the covers (objects, contexts, devices: not only phones).
4. Closing slide (contact, thank you) — not built yet. Final check: size < 20 MB, file name, links, typos.
5. Optional: propose a concrete small physical prototype (Arduino/ESP32) tied to one project.

### 0.C How to research and read sources
- **Web:** `WebSearch` (mode "standard" first; "extended" for thin or niche results) and `WebFetch` for a page.
  Official sources: www.polimi.it (programme pages), www.design.polimi.it (School of Design: guides under
  Didattica → Documenti → Guide alla carriera; manifesti; news with rankings), www.digitalinteractiondesign.polimi.it.
  Reddit/aggregators had nothing reliable on portfolio tips.
- **PDFs from the web:** `WebFetch` on a PDF returns binary, but saves it under
  `C:\Users\rospo\.claude\projects\C--Users-rospo-Documents-ClaudeCode-Websites-uxportfolio\<session>\tool-results\webfetch-*.pdf`;
  read that saved file with the `Read` tool (small PDFs read whole, text + page images).
- **Local PDFs:** `Read` works without `pages` for small files. `pdftoppm` is NOT installed, so `pages` fails; for big PDFs
  render them with **`Media/_tools/pdfrender.mjs`** (pdf.js inside headless Chrome via a tiny local HTTP server):
  `node pdfrender.mjs <pdf> <outdir> 1000` from a scratchpad with `puppeteer-core` + `pdfjs-dist@4.10.38` (+ `sharp` for
  contact sheets) installed (`npm i puppeteer-core sharp pdfjs-dist@4.10.38`).
- Owner's application folder: `C:\Users\rospo\Documents\Magistrali\Polimi\` (manifestoDID.pdf, helpdesk ticket,
  requisito inglese.pdf, SILVIA_GORI_Portfolio.pdf).

### 0.D Tooling on this PC (both workstreams)
- Build the site with PowerShell `npx astro build` (Git Bash cannot load Rolldown). Dev server: `preview_start` name
  `portfolio` (`.claude/launch.json`, autoPort: often 4322/4323). **The dev server's HMR often serves stale scoped CSS
  after component edits: restart it (preview_stop + preview_start) before trusting screenshots.**
- Screenshots: puppeteer-core + Chrome (`C:/Program Files/Google/Chrome/Application/chrome.exe`). Chrome full-page shots
  break above ~16 384 px (tiles repeat): capture **per element** (`el.screenshot()` on `section#id`), hiding `header` and
  `[data-pbar]` and making `.sec__sticky` static. Scroll the page first so reveals fire. Review as contact sheets made
  with sharp. Scripts from this session were in the (now cleaned) scratchpad; `Media/_tools/sec.mjs` is the older
  equivalent; rewrite small ones as needed.
- **Shell pitfalls:** long `node -e "…"` with backticks, `$`, `!` or nested quotes breaks in Git Bash: write the script
  with the Write tool into the scratchpad and run it. Never `cat > file` without a heredoc (it waits on stdin).
- Image recipes (Figma export at 960 px via clone + rescale; screen-into-photo warps; glass masks; ground lightening):
  scripts in `Media/_tools/` (warp2.js, glass.mjs, ground.mjs, comp.mjs, handmask.js, desat.js, grid.js, refine.js,
  outline.js). Figma export: load the `figma:figma-use` skill, `use_figma` → `clone()` the device, `rescale(960 / w)`,
  park at x ≥ 8000 named `TMP export · …`, `get_screenshot` (maxDimension 1963, contentsOnly), curl, delete the clone.
  For a bare screen clone the `Screen` instance and `rescale(3)` → 1206×2622.
- Memory files (auto-loaded): `portfolio-project-goal`, `design-taste-feedback`, `rehabeat-prototype-todo`,
  `polimi-portfolio-deck`.

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
| 02 Rehabeat (ex Rehab) | **Live** (2026-10-12): text, cover, Result showcase done; Design-chapter Features still placeholders (real facts, `notes/02-rehab.md`; literature numbers in Challenge). Interfaces are placeholders until the owner sends the final screens → still `placeholder: true` / Coming soon. |
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
| `--soon` | `#a6463c` (muted brick red) | **only** for "Coming soon" (cursor label background, touch note, nav "Soon"). White on it = 5.9:1. |

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
| `--fs-lead` | ~19→23px | lead paragraphs; card titles (Medium); chapter group headings `###` (Medium, no number) |
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
   MDX `### Title` → title alone in lead Medium (a signal "01.1" number was tried the same day and removed: "troppi
   numeri"). Proximity: `--space-item` before a group, `--space-3` heading → content, `--space-block` inside. Notes are
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

**Rejected 2026-10-12 → 16 (do not re-propose):** home statement entrances other than the blur word reveal (single
mask wipe, word rise); "living" hero concepts (wireframe → text, spec annotations, X-ray lens, variable-weight cursor,
rotating role); hero structures (typographic index, bento grid, statement + interface strip, floating covers depth field);
simple hero variants (bottom poster with grey tail, section-style label + statement, name and description side by side,
statement + footer line). About portrait colour lens following the cursor (now a simple colour fade). Rehabeat Result
scene full-bleed 100svh with scroll zoom (back in the grid). Role/Team/Timeline line under the case-study tagline
(removed). Zoom-in hover on photo covers (all zoom out now).

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

> 2026-10-16: `main` is clean and pushed; everything in §0 is live. The snapshot below is older history.

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
    screens/*.png                 Redesign v3 cut-outs (960×1963) + 5 *-crop.png for the Design Gallery
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
1. ~~LinkedIn URL~~ — set 2026-10-13.
2. **CV may contain his phone number** (`public/cv/Valerio-Rosponi-CV.pdf`) — he was told, may want a redacted copy.
3. ~~UX/UI filter~~ — resolved 2026-10-09: the vocabulary is now All / Mobile / XR / Product / Multi-screen.
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

> **2026-10-27 next steps.** The active workstream is the **Politecnico portfolio PDF** (§0.B). (1) Ask the owner for
> Smart Home Hub interfaces + prototype material, then design the repeatable project template (process first, system
> map, prototypes, UI as payoff) and build project 01. (2) Owner decides project 03 (UX Challenge 2026 vs thesis).
> (3) Photos for the project index/covers, closing slide, final checks (< 20 MB, file name, links). Website side, only
> on request: Smart Home Hub / AuraWake interfaces → covers, showcase, Features images, `placeholder: false` (the same
> material serves the PDF); Realiti real facts (`Media/04-Realiti/`); Rehabeat Features 01/02/03/05 + prototype
> section. Open items: CV has the phone number; no Lighthouse/accessibility pass yet.

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

- **2026-10-27 · LOCAL (10)** · AuraWake base **redesigned on the owner's Mac mini refs**: 11 × 11 × 4.4 cm, matte black
  bead-blasted aluminium, tapered black speaker-grille plinth (slits on sides + radial ring underneath, foot disc with
  "AuraWake"), thin continuous light strip between body and plinth, front LED right at mid height, time 5×7 dots behind
  micro-perforations (invisible when off), back = figure-8 power inlet with "~" + Bluetooth pairing button with its
  glyph (no power button: it turns on when plugged in), top flat (no cradle) with the band lying open on it like an
  Apple Watch on its puck. Studio renders like Apple's (white, no shadows, near-flat perspective):
  `deck/assets/aurawake/render-front|back|top|bottom|cable.jpg` + `render-night|dawn.jpg` (room moods); hero dropped.
  Schema (slide 22): base drawn light grey so time/LED read; **no platforms** — related objects inside one hairline
  outline each ("Bedroom · Thread / Matter" amber: diffuser, shutters, lamp along one iso axis; "With you" grey: phone,
  bracelet; cloud dashed); keys 1–4 on the base + 05 Back in the list; legend top right. Known: the bottom-view
  "AuraWake" may read mirrored (check). Renders still not placed in the PDF: ask the owner where.

- **2026-10-27 · LOCAL (9)** · AuraWake objects designed and modelled in **Blender 5.2** (installed via winget):
  `deck/blender/aura.py` builds base (rounded square block, black anodised aluminium, Mac mini proportions, TE
  restraint: power cable only, small front LED, time 5×7 dots behind micro-perforations, cradle on top, light line
  underneath), bracelet (standing band loop + pod in the cradle), phone, bulb, roller shutter, diffuser (same family).
  `-- real <out> hero|night|dawn [preview]` → Cycles renders (GPU RTX 5060); `-- line <out>` → true-isometric
  technical drawings (flat 3-tone fills + Freestyle lines, Walkman/TE style) + `anchors.json`. Outputs in
  `deck/assets/aurawake/` (iso-*.png, render-hero|night|dawn.jpg). **System slide (22) rebuilt** as an isometric
  plan: drawings on platforms coloured by protocol (grey Wi-Fi, indigo BLE, amber Thread, dashed cloud), dotted flows
  along iso axes, numbered keys on the base (1–5) listed under the title, legend. Renders **not placed yet**: ask the
  owner where (AuraWake cover / gestures). Owner prefers parallel runs and few tokens (870% of his 5-hour limit).

- **2026-10-27 · LOCAL (8)** · Deck: **AuraWake** 4 content slides (system map, one-night swimlane, gestures + light
  language, app + what-if) from the Interaction Design Spec; details in §0.B. Owner: 3–4 slides, use the spec facts
  regardless of date, objects as placeholders for now, prototype decided later. Pending: object illustrations, app
  screens, owner review.

- **2026-10-27 · LOCAL (7)** · Deck: **main-project template** = 11 grey placeholder slides after cover 01 (overview,
  context, research, insights, framing, ideas, system map, prototypes, solution ×2, outcome) with a process bar at the
  bottom (current step in the project colour); details in §0.B. Owner: one project at a time, wait before filling
  Smart Home Hub; prototype material = only the report; project 03 still undecided. Pending: owner review of the
  template.

- **2026-10-27 · LOCAL (6)** · **Full HANDOFF rewrite for a new chat:** §0 now has 0.1 owner + vision, 0.2 working with
  the owner (incl. everything rejected lately), 0.A the website (projects, B-mix structure, components, JustCook), 0.B
  the Polimi PDF (admission rules, course profile, reference portfolio, owner's decisions, line-up, colours, the deck
  system, slides, build, next steps), 0.C how to research (web, PDFs, local files), 0.D tooling and pitfalls. §9 next
  steps updated. CLAUDE.md points to `deck/`. `Media/_tools/pdfrender.mjs` saved (render any PDF to JPGs).

- **2026-10-27 · LOCAL (5)** · Pastel project colours rejected ("scuri come prima!"): reverted to the dark palette with
  white type (01 teal 2b5c6b, 02 terracotta b04a32, 03 aubergine 5a3a5e, 04 forest 2e5e4e, 05 ochre 8f6519). Do not
  propose pastels again.

- **2026-10-27 · LOCAL (3)** · Deck aligned with the course: DID is strongly about interactive systems with physical,
  connected, tangible and embodied parts (Embodied Interaction Studio, Tangible and Embedded Technologies, Hardware &
  Software Technologies for Design, Final Design Studio on connected products, Virtual & Physical Prototyping, Smart
  Wearables). Owner's line-up: **main 01 Smart Home Hub (teal 2b5c6b), 02 JustCook (terracotta b04a32), 03 UX Challenge
  2026 or a new thesis project (aubergine, to be decided); additional 04 Realiti (forest 2e5e4e), 05 AuraWake (ochre
  8f6519)**. Rehabeat is out. Covers carry the real facts from the MDX (Realiti still placeholders: its MDX facts are
  invented). "Where I'm heading" now uses the course's words: connected products and systems · tangible and embodied
  interaction · physical and virtual prototyping, each with its related projects. For every project: show the SYSTEM
  (devices, data, physical touchpoints, use in space) and the PROTOTYPES, not only screens. The UX Challenge project is
  app/web only. The owner has prototype material for Realiti (XR), AuraWake and Smart Home; a small new physical
  prototype (Arduino/ESP32) before July is "maybe, to evaluate".

- **2026-10-27 · LOCAL (2)** · Deck round 2 (owner): **3 main projects + 2 additional**, each opening on a full-bleed cover
  in its own colour (01 terracotta b04a32, 02 forest 2e5e4e, 03 aubergine 5a3a5e, 04 ochre 8f6519, 05 teal 2b5c6b;
  placeholders except 01 = UX Challenge 2026); cover in ultramarine 1f3c88 with the name at 312 px; the 12 columns drawn
  as faint hairlines on colour slides; tone-on-tone mega project number bleeding off the corner. Removed "What I bring"
  and "How I approach design": **the approach must show through the project explanations, PROCESS IS THE FOCUS**
  (owner, in capitals; also saved in memory). Who I am now holds profile, education, details and a 4-cell
  "Recognition and experience" row (highlights only: the full list belongs in the CV, which is scored separately).
  Contents in three groups (About · Main projects · Additional projects) with colour swatches; Selected projects =
  photos and white space only (3 large main images, the 2 additional smaller in the last track; placeholders = the
  project colour). Display size in the deck = 88 px, one sentence per line. 10 slides, 0.2 MB. The contents, the
  project index and the page numbers are generated from the `.pcover` sections (data-num, data-kind, data-title,
  data-sub, --pc): adding a project = adding a cover. Next: the project content slides (process first).

- **2026-10-27 · LOCAL** · **New: portfolio PDF for the Politecnico di Milano application** (MSc Digital and Interaction
  Design). Rules (School of Design Open Day 2026 deck): portfolio PDF max 20 MB, no imposed format, IT or EN, no special
  characters in the file name (hyphen included); score = portfolio max 50 (below 30/50 = not eligible) + CV max 20 +
  GPA, +5 if first choice; DID has 50 places; applications about 22 June – 7 July. Reference: Silvia Gori's accepted
  portfolio (same UniTrento BSc, 59 slides 16:9, clear but loose grid). Owner's choices: English; site identity + a
  strong accent for section dividers; no photo; a short "Where I'm heading" slide linking the course themes to the
  projects; AI2B and the Olympiads as participation only; no thesis yet; projects as placeholders for now (the UX
  Challenge 2026 project for Gruppo Spes will be a case study: the owner has material).
  Built in `deck/` (not published by Astro): `index.html` (1920×1080 slides; 12 columns of 122 px, 24 px gutters,
  96 px margins; chrome at y 56; content frame 144 → 984), `deck.css` (site tokens, type scale ×1.5, cells, rows,
  placeholders), `build.mjs` (puppeteer-core devDependency → `deck/out/Rosponi_Valerio_Portfolio.pdf` + PNG previews;
  `--grid` draws the columns, `--accent=hex`). Page numbers, the contents and the divider lists are generated by the
  inline script from `data-part` / `data-sub`. 9 intro slides: cover, contents, About divider, who I am, how I work,
  what I bring, recognition, where I'm heading, selected projects (placeholders). `deck/out/` is git-ignored
  (regenerate). **Pending: the accent colour** (rendered options: ultramarine 1f3c88 = current default, deep blue 24405c,
  terracotta b5482f, ink 111111), then the project slides.

- **2026-10-20 · LOCAL (12)** · Numbered lists in chapters ("If I started again") back to a plain list on the A–B
  measure (number + point, light hairlines), not cells (owner). Pushed `main`.

- **2026-10-20 · LOCAL (11)** · Owner review round 3: chevrons instead of arrows (Process rows, All work); no rule above
  any `###` group; group titles now h3 Medium sentence case (sub-chapters), item titles inside cells/rows lead Medium;
  stamp row lighter (one-sentence text, Principle as a quiet line, shortened: the "8 of 10 meals" clause dropped);
  no hairline under the last Outside-the-app gallery group; channel cards as About-style tool tiles. Pushed `main`.

- **2026-10-20 · LOCAL (10)** · Owner's annotated review of B-mix: no rule above Overview; thinner arrows (Process +
  All work); number cells without the fixed min-height; Research "Codes" explained ("short tags marking what each
  passage … is about; the same 36 applied to all"); Archetypes rows as continuous light hairlines (no column rules);
  `###` groups on a strong full-width hairline, Chips labels as lead sub-headings; Features back to the previous
  rhythm (text centred on the screen, device on the line) + new `also`/`note` fields: Hold to stamp and Thursday
  stamped side by side in one row with the Principle note under the text; channel cards with logos (Instagram,
  WhatsApp, TikTok from Simple Icons, a drawn QR). Owner liked the mega Closing: "tutta la pagina punta ad avere
  questa vibe" (a compliment: nothing else to scale up). Pushed `main`.

- **2026-10-20 · LOCAL (9)** · **Case-study structure "B-mix" implemented** (owner's pick from the three prototypes in
  `notes/proposals/`): rules and text levels of B (cells), Overview as cells, Result untouched, Process = clickable
  index rows (A, with a drawn arrow), sticky chapter titles kept, Key in h2 Regular, `###` groups as uppercase labels,
  numbers/insights/cycles/numbered lists as hairline cells (`.cells` in global.css), no chips anywhere (sequence numbers
  = small signal labels), Archetypes and priority Chips lightened (no boxes/tints), Features as A rows with the
  alternating sides, Closing = bold sentence in mega, all ink. Reframes no longer draws "6 → 1". All five case studies
  share the components. Checked JustCook at 1440 and 375 (no overflow, Rehabeat too). Pushed `main`.

- **2026-10-20 · LOCAL (8)** · Owner: case-study pages are confusing (no entry point, unclear order and hierarchy of
  text, labels, numbers, boxes). Three full structural proposals built with real JustCook content in
  `notes/proposals/case-structure.html` (?p=A|B|C): **A Index rows** (no sticky title lane; title cols 1–4, text 5–10,
  media 5–12; one stat size in data rows), **B Cells** (everything in one hairline cell grid, label top / number
  bottom), **C One column** (text cols 3–10 in lead size, numbers gathered in full-width data rows). A|B|C
  comparisons per section in `notes/proposals/cmp/`. **Waiting for the owner to pick**; nothing on the site changed yet.

- **2026-10-20 · LOCAL (7)** · JustCook: stamp hand mockup dropped (owner: "torna indietro"). The two stamp screens are
  flat Features rows 06 Hold to stamp and 07 The day, stamped (between Focus mode and Streaks); the Principle note
  follows the Features. No mockups left on the page. Pushed `main`.

- **2026-10-20 · LOCAL (6)** · JustCook stamp figure, owner: screen corners now follow the real glass of the hand
  phone exactly (mask from the measured glass profile), ground lightened to #efefef, phones slightly smaller and
  centred with equal 700 px margins on all sides (image 2000×1848). Pushed `main`.

- **2026-10-20 · LOCAL (5)** · JustCook The stamp figure inverted (owner): "Thursday, stamped" in a new hand photo
  (hand-grey.png) on the right, flat "Hold today to stamp it" device on the left, same scale. Pushed `main`.

- **2026-10-20 · LOCAL (4)** · JustCook The stamp: backlit Spot replaced by a wide Figure (owner): his frontal hand photo
  with "Hold today to stamp it" + the flat "Thursday, stamped" device beside it at the same scale. Pushed `main`.

- **2026-10-20 · LOCAL (3)** · JustCook, owner: scroll zoom and lid mockup removed (Spot `zoom` prop deleted); the lid
  code is a flat Features row "One code per box" between A timely nudge and Focus mode. New stamp mockup from the
  owner's backlit hand photo (`mockups/hand-stamp.jpg`, 1800×2250) as a Spot "After dinner" in The stamp. Pushed `main`.

- **2026-10-20 · LOCAL (2)** · JustCook, owner: removed the In hand duo from Result, the 19:45 hand Spot and the stamp
  finger Figure (files deleted). 19:45 notification exported from Figma (2319:5724) as `out-notif-start-cooking.png`
  (0.53 bottom crop) into Outside the app: Dinner split into Before dinner + While cooking. Spot takes `zoom="x% y%"`
  (CSS scroll-driven `animation-timeline: view()`, 1 → 1.4, cover 20–60%, off for reduced motion / unsupported), used
  on the lid code. Gallery cutout groups are swipe rows on phones. Phone check of JustCook at 375 px: no overflow.
  **Pending: the owner will send a new stamp mockup** for The stamp. Pushed `main`.

- **2026-10-20 · LOCAL** · HANDOFF §0 and §9 rewritten for a new chat (full current state of all five projects, the
  exact JustCook structure, new components, image recipes). Mockup source photos copied to
  `Media/01-JustCook/mockups-source/`, image scripts to `Media/_tools/` (both git-ignored, local only). Pushed `main`.

- **2026-10-19 · LOCAL** · JustCook hand mockups (owner photos, `assets/projects/justcook/mockups/hand-*.jpg`): screens
  exported 3× without bezel from Figma, warped by homography, fingers kept on top via a skin mask, Dynamic Island
  restored or painted. Result opens with a new Showcase layout `duo` (Home + Plan in hand). Design: new `case/Spot.astro`
  (photo on B–C, framing text on A, baseline hairline) for "One code per box" and the 19:45 notification; "The stamp"
  group with the finger mockup as a wide Figure + a Principle note. Stamp copy rewritten after the owner: the long
  press is emotional (doing it yourself = pride and completion, from his `1percent-design-guidelines.md` §8: participation
  over spectatorship, retention ask inside the peak), not a safety lock. Features rows for code/stamp removed; table
  and old hands mockups deleted. Outside the app groups relabelled by time of day. Pushed `main`.

- **2026-10-18 · LOCAL (6)** · JustCook Design "Outside the app" back, as a day narrative: intro line, the table mockup,
  then a Gallery (cutout, cols 3) in four moments: Morning (08:30 use it today, 09:00 boxes ready, large widget) ·
  During the day (3 streak widgets) · Before dinner (medium widget, 19:45 notification) · While cooking (Live Activity
  compact + expanded). All pieces are `screens/out-*.png`, one uniform 0.53 crop (notifications from the bottom, the
  rest from the top). Features rows 08–10 removed (now in the narrative). Pushed `main`.

- **2026-10-18 · LOCAL (5)** · JustCook Result: the one mockup is now the hands photo (`mockup-hands.jpg`, full photo with
  its grey ground, no fades) as scene "In hand"; the table mockup moved to the end of the Design app rows (wide Figure).
  Widgets group → quad (small, small ending, medium, large). Meal stamped re-exported (owner edit). Widget small ending
  is now a full shot (Design row crop 0.36). Pushed `main`.

- **2026-10-18 · LOCAL (4)** · Hands mockup moved to the end of the app group (after the Features rows, before Brand and
  campaign), full body-lane width. Features `anchor: bottom` fixed (img flex-shrink 0: the phone’s bottom edge now
  shows, cut at the top); notification rows crop 0.85. Pushed `main`.

- **2026-10-18 · LOCAL (3)** · JustCook mockups (owner-supplied photos): `mockup-table.jpg` = Result scene "The nudge"
  (start-cooking lock screen warped into the table photo, Dynamic Island pasted back, 16:9 crop; the only mockup in
  Result). `mockup-hands.png` = hands photo with the Today screen, background cut by flood fill, edges faded, shown as a
  `size=text` Figure under the Design "The app" note. Features now take per-item `crop` and `anchor: bottom`: global
  0.82, widget rows 0.32/0.72-of-half, notification rows bottom 0.7 of the 40% crops. "Outside the app" Gallery removed
  (its items became Features rows 08–10). Figma clones removed. Pushed `main`.

- **2026-10-18 · LOCAL (2)** · JustCook Result "From box to stamp" → trio: lid code (re-exported: now with the keyboard),
  hold to stamp, Thursday stamped (re-exported, owner edit). Dropped code accepted + dinner served (files deleted).
  All 23 original screens had already been replaced from Redesign v3 in the previous entry. Pushed `main`.

- **2026-10-18 · LOCAL** · JustCook screens replaced with the owner’s **Redesign v3** (Figma file `9kVAJhXfvlz569AYMRGGCn`,
  page "JustCook — Redesign v3" 2056:180: 28 device frames in 5 flows, Home / Cook / Buy / Plan and pantry / Widgets).
  Export recipe: get_screenshot never upscales, so clone each device frame, `rescale(960/w)`, screenshot at 1963,
  delete the clones (done; nothing left in the file). `screens/*.png` = 960×1963 transparent cut-outs. Cover recomposed
  with the same three screens (home, home scrolled, boxes; 869×1776 each, same centres). Result: new quad "From box to
  stamp" (lid code, code accepted, served, stamped). Design: Features 4 → 7 rows (+ swap box, one code per box, hold to
  stamp) and a new group "Outside the app" (Gallery cutout: 3 notifications cropped to the bottom 40%, 2 streak
  widgets cropped to the top 50%, `*-crop.png`). Owner: the lid code is unique per box and validates that a box was
  really cooked (recipes stay browsable); the stamp confirms the meal for the streak. Pushed `main`.

- **2026-10-16 · LOCAL (3)** · AuraWake (05) written from the two AuraWake PDFs: short page (no research existed, so no
  Research/Insights chapters), Reflection says research would come first now. Same pattern as Smart Home Hub: text
  complete, interfaces as placeholders, Coming soon. `render.mjs` now loads the PDF once (88 MB PDFs crashed it).
  Timeline: spring 2024 (owner). Rehabeat and AuraWake both name the course "Human–Computer Interaction 1". Pushed `main`.

- **2026-10-16 · LOCAL (2)** · Smart Home Hub (03) written from the PIG final report: Challenge (brief + stakeholders),
  Research (8 situations, 6 proto-personas, 16 pain points), Insights, Define (Marco vs Franco archetypes, 5 problems
  taken on, "universal remote" dropped), Ideate (solo sketches → design space), Design (4 placeholder Features rows +
  slider / Cancel-emphasis decisions), Reflection + Closing. System ideas (e-commerce shipping code, automatic emergency call,
  smoke defence) shown in Design under "Beyond the screens", as ideas, not interfaces. Still Coming soon. Report rendered with `render.mjs` (puppeteer +
  pdf.js, session scratchpad). Archetype `goal` words must be short ("Less to remember" broke mid-word). Pushed `main`.

- **2026-10-13 · LOCAL (6)** · The site is the Cloudflare **Worker** `uxportfolio-main` (Workers Builds from git, static assets).
  Added `wrangler.jsonc` + `worker/index.js`: worker runs first and 301-redirects http:// and valeriorosponi.com to
  https://www.valeriorosponi.com (same path/query); everything else goes to the ASSETS binding (dist/, 404 page).
  Pushed `main`.

- **2026-10-13 · LOCAL (5)** · Google Search Console: 1 "duplicate without user-selected canonical" + 2 "page with redirect".
  Causes: internal links without trailing slash (/about → 307 → /about/) and the apex domain valeriorosponi.com
  serving the site with 200 instead of redirecting to www. Fixed in code: `trailingSlash: always`, nav and `hrefOf` end
  with "/" (no internal link redirects any more). Apex → www now handled by the Worker itself (see next entry). Pushed `main`.

- **2026-10-13 · LOCAL (4)** · Wide TV frame 4564:3022: the knee-angle bar column (4564:3078) was double-shifted by a
  constraint resize; now centred on the frame (728.5), re-exported. Affinity mark = the new "a" logo the owner sent,
  built as a masked SVG (`src/assets/logos/affinity.svg`, takes currentColor). Pushed `main`.

- **2026-10-13 · LOCAL (3)** · Rehabeat TV screen now comes from a **wide Figma frame**: node 4564:3022 "TV-2 · wide
  2.02:1" (1457×720, duplicate of 4404:1524 under it; backgrounds stretched, centre scene +89, right column +177 so
  side margins stay 64), exported ×3 into the dark living room (`tv-living-room.jpg`). Scene back inside the grid
  (no full-bleed / scroll zoom). Home statement back to the blur word reveal. Affinity logo → Affinity Designer mark.
  Back arrow 1.5px. Design step 04 shows the TV-2 screen (`tv-workout.jpg`; Features: `device: 'tv'` images are not
  cropped). Pushed `main`.

- **2026-10-13 · LOCAL (2)** · Recruiter pass: OG/Twitter large images on every page; at-a-glance Role/Team/Timeline
  under each case-study tagline; editorial back link. All card hovers zoom out (bleed covers from 1.07). Labels: JustCook
  "Product & communication design, iOS app + physical box", Realiti "VR experimental experience, Meta Quest", AuraWake
  "Gradual alarm, Mobile app". Home statement word by word (rise + fade). About: simpler portrait hover; tools + Affinity
  & Illustrator. Rehabeat: living-room scene full-bleed 100svh with scroll zoom; TV-2 rebuilt 4370×2160 with the corner
  UI moved outwards (clean plate + alpha, scratchpad `rbtv/widen3.mjs`); Euleria moved to Ideate as a `Reference`
  tile with its logo; "The system" is now `SystemMap`. Owner to-do in memory: a working-prototype section for
  Rehabeat. Lighthouse not run (only a manual check). Pushed `main`.

- **2026-10-13 · LOCAL** · About rebuilt (see CLAUDE.md Structure): column-line hero + statement "Useful to as many
  people as possible. / Beautiful enough to make them stay." + portrait colour lens; 5 accordion sections, all closed,
  one open at a time; tools with logos (Figma, Claude & Codex, local AI/Ollama, Unity, Meta Developer Hub, Git);
  "Looking for" removed; "What I bring" → 14 skills in Research & strategy / Structure & interaction / Interface &
  delivery. LinkedIn set (linkedin.com/in/valerio-rosponi). Home: statement enters with a single mask wipe (per-word
  blur removed); depth texture drifts by itself on touch. Card labels: new `labels` frontmatter, one chip each;
  Smart Home Ecosystem → **Smart Home Hub** (file 03-smart-home-hub.mdx). Owner wrote "Reality": kept the project
  name **Realiti**. Verified with puppeteer 1440/390. Pushed `main`.

- **2026-10-12 · LOCAL (5)** · (1) Card hover: the 0.95 zoom-out left ugly tone borders around Rehabeat's photographic
  cover. New `cover.bleed` flag (content.config.ts → ProjectCard → Card `bleed`): bleed covers zoom in to 1.04 on
  hover instead; JustCook (flat ground) keeps the zoom-out. (2) Home hero statement now reads "Valerio Rosponi, UX and
  digital product designer studying Interfaces & Communication at the University of Trento, based in Trentino,
  Italy." (was "I'm Valerio Rosponi, a UX and…"). Verified with puppeteer at 1440. Pushed `main`.

- **2026-10-12 · LOCAL (4)** · Owner: "rendi il progetto disponibile" → Rehabeat `placeholder: false`: card and index
  row linked, in the sitemap, no noindex, JustCook's Next band now points to it. Known gap, published anyway at the
  owner's request: the 5 Design-chapter Features rows still show placeholder frames (no final screens yet). Pushed `main`.

- **2026-10-12 · LOCAL (3)** · Rehabeat Result filled with the final Figma screens (`result.showcase`, assets in
  `src/assets/projects/rehabeat/screens/`): 01 "The coach on the TV" = TV-2 in the owner's dark living-room mockup
  (1569×911 webp, upscaled to 2880; glass 563.5,261 · 1092.5,522.5, ~2.02:1, so the 16:9 screen is widened with its
  own blurred dark edges instead of stretched; light reflections from the upper right; scratchpad `rbtv/dark.mjs`),
  new layout `scene`; 02 "The app" = Home, Week 2 report, Week 2 data (trio, stagger); 03 "Before and after a
  session" = the Home and Session-done (node 4107:1735) phones cropped to their bottom 20% (new `anchor: bottom`),
  side by side with captions (new `caption`). Order picked by the owner (TV first). Also fixed an old mobile bug:
  stacked section heads kept cols 1–3 below 960px, so "Result" broke as "Resu/lt" (JustCook too). Still Coming soon:
  Design-chapter Features placeholders remain. Pushed `main`.

- **2026-10-12 · LOCAL (2)** · Owner changed idea: Rehabeat cover is now the **living-room mockup** (owner's webp,
  2000×1337: wall-mounted TV, wooden console, two tall speakers, sofa) with the same TV-2 "Leg flexion" screen. The
  photo is upscaled to 3840 wide and cropped to 16:10 (80px off the top); the 4K screen is projected onto the glass
  (inner edge measured on the 2000×1337 photo, expanded ~1.5px to cover the original Apple TV UI: 654.4,258.8 ·
  1347.4,258.2 · 1343.1,649.8 · 658.2,650.1), 3×3 supersampled. Card tone #d9d4d2. Script: scratchpad
  `rbtv/room.mjs`. Supersedes the studio TV versions below. Pushed `main`.
  Follow-up (owner: zoom so the TV is centred, add light realistic reflections): crop 1500×938 of the photo from
  x 251, y 0 (TV centre at 48.5% height, ×2.56); on the glass, screen-blended: the room mirrored left–right and blurred
  (σ 60) at 7.5%, plus a soft diagonal window-light sheen and a faint top-edge glow at 11% (owner asked for them a
  little less bright than the first 10%/15% pass; scratchpad `rbtv/room2.mjs 1500 0.11 0.075`).
- **2026-10-12 · LOCAL** · Rehabeat cover REDONE a third time, at the owner's request: **only a TV**, the photographic
  studio mockup ("image 1", node 4535:1499, raw 2312×1732, page "Redesign") showing **TV-2 "Workout · Leg flexion · rep 4
  of 10"** (node 4404:1524, exported ×3 = 3840×2160). The screen is re-projected onto the glass with a homography (glass
  = inner edge of the front bezel, measured on the 2312×1732 photo: 401,171 · 1939,40 · 1940,1198 · 401,1118), then the
  photo's own glare and rainbow light are screen-blended back over the UI at 45% (owner: "mantieni l'aura
  cinematografica e luminosa"). The 4:3 photo becomes 16:10 by filling each side row by row with a band 60–140px inside
  the photo, feathered over 160px (the outer columns had resampling artefacts). This is the one exception to the flat
  #f5f5f5 covers: a lit studio photo, card tone #e8ebef. Scripts: session scratchpad `rbtv/make.mjs`. Pushed `main`.
  Follow-up (owner: "tieni solo la TV, togli il tavolino"): the media console was removed (`rbtv/clean.mjs`): TV + its
  L-shaped stand kept (stand traced as polygons, metal pixels only), the area below the TV rebuilt as the studio
  gradient with a faint contact shadow; the photo is scaled ×0.94 and the TV+stand group centred vertically.
  NOTE: Cloudflare had stopped deploying after `280321c` (live site still showed "Rehab", `/work/rehabeat` 404) even
  though a clean clone builds fine; cause not found yet (the owner said "ora va" for localhost, Cloudflare log still
  to read). Also: never delete `.astro`/`node_modules/.astro` while the dev server is running, it empties the content
  store (home shows no projects) until restart.
- **2026-10-10 · LOCAL (2)** · Rehabeat cover REDONE with the owner's TV mockup (a 2000×1500 webp of a slim
  3/4-perspective TV on a flat #e8e8e8 ground): **TV on the left, the two phones large on the right**, one ground line,
  group centred, side margins ~480px (4:3 card safe). The mockup body was upscaled ×2 and cut out (neutral greys ≥172
  removed by flood fill, which also drops its faint contact shadow: covers stay flat); the 4K TV screen from Figma was
  re-projected onto the glass with a homography (glass corners measured on the mockup: 526,218 · 1308,392 ·
  1344,1052 · 571,1197), so the UI is sharp. The drawn minimal TV from the entry below is superseded. Pushed `main`.
- **2026-10-10 · LOCAL** · Rehabeat cover (`src/assets/projects/rehabeat/cover.png`, 3840×2400, tone #f5f5f5). Source:
  Figma file `xmb1334lJ54M35DwB9PFnl` (page "Redesign"), nodes 4106:1552 "Mockup · Home · iPhone 16 Pro (official
  bezel)", 4115:2142 "Mockup · Week 2 data …", 4349:1524 "TV / Get ready · thumbs up recognized (TV-10)" (exported
  via the Figma MCP, ×4 phones, ×3 TV). Phones cut out of their #f5f5f5 frame (flood fill); TV screen set in a drawn
  minimal TV (near-black bezel 1.2%, thin neck + rounded base, no shadows). Layout picked by the owner from 3
  concepts (triptych / TV in front / lineup): **"B · TV in primo piano"** with the stand: TV centred, phones in front of
  its lower corners, all standing on one ground line, group vertically centred. Side margins ~505px so the 4:3 home
  card crop (−320px per side) never cuts a phone. These Figma screens are the FINAL interfaces (the old UI in
  `Media/02-Rehab` is not). Still Coming soon until the Result/Features screens are placed. Pushed `main`.
- **2026-10-09 · LOCAL (3)** · Case study 02 written as **Rehabeat** (renamed; `02-rehabeat.mdx`, `/work/rehabeat`).
  Sources: `Media/02-Rehab/hci.pdf` (HCI report, 58 pp., Italian, image-only → rendered with pdf.js in Chrome) and
  `old-portfolio-rehab.pdf`; all facts + owner answers in `notes/02-rehab.md`. Owner decisions: research = desk +
  clinical literature + physio protocols + heuristic review (apps not named; Euleria = reference, not competitor);
  literature numbers allowed (Ardern 2014 65%, Argent 2018 30–50%, Terry 2020 139 studies, all verified); role
  End-to-end UX designer; Figma + FigJam; year 2024 (Oct 2024 – Jan 2025); type "Connected health system";
  archetypes kept, flagged as synthesised; Result numbers = system facts; target 18–50 and sensors (bands + floor mat
  + phone camera) written as Decisions with my rationale (owner asked me to judge). No Validate chapter (no testing).
  Interfaces: placeholders only (Features now accepts items without `image`). Stays Coming soon. Pushed `main`.
  → Next: owner sends the final Rehabeat screens (phone + TV) → Result showcase + Features images, cover, then
  `placeholder: false`.
- **2026-10-09 · LOCAL (2)** · (1) Group numbers "01.1" removed ("troppi numeri"); titles stay. (2) JustCook copy
  pass: tighter Challenge intro, "at least one portion of fruit", Analysis wording, the missing "about half throw food
  away" fact added to insight 3, archetypes flagged as synthesised from the data (honest, see Appendix B), "Next" →
  "Nice-to-haves", simpler Ideate Key + heading, Conad pickup framed as "in the prototype" (never confirmed),
  Reflection without repeating the Challenge Key. (3) Unfinished work: placeholder projects + Playground visible but
  not openable, red "Coming soon" cursor label (`--soon`), touch note, pages built but noindex + out of sitemap, Next
  band only to finished projects (JustCook now has none). (4) Filters: All, Mobile, XR, Product, Multi-screen (Rehab =
  phone + TV together; its platform now "Mobile + TV"). Verified with puppeteer (1440, 390, 360). Pushed `main`.
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
