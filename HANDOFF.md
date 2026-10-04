# HANDOFF — Valerio Rosponi portfolio

This file hands the project over between Claude sessions. Read it fully, then read `CLAUDE.md`, the persistent
rules that load automatically. Where the two disagree, this file is newer (last update: 2026-10-04).

**First: sync git (§00), THEN read this file again.** Another session may have pushed a newer HANDOFF.

---

## 00. Two kinds of session: CLOUD and LOCAL (read first, every time)

The owner works with Claude in two places, and alternates between them. This file is the only memory they share.

| | **CLOUD session** | **LOCAL session** |
|---|---|---|
| Where | claude.ai/code, Linux container, fresh clone | the owner's Windows 11 PC (Claude Code desktop/CLI) |
| How to tell | working dir `/home/user/...`, no `Media/` folder | path `C:\Users\rospo\...`, `Media/` folder exists |
| Has `Media/` (reports, PDFs, raw exports) | **no** (git-ignored, never in the clone) | **yes** |
| Figma MCP / headless Chrome | Figma MCP may be connected; Chromium via Playwright | Figma MCP, Chrome via puppeteer-core |
| Git | may push **only** to its `claude/*` branch (now `claude/stoic-ride-lj7woi`; a new cloud session may get another `claude/*` name: check `git branch -r`) | pushes to `main` |
| Deploy | its work is **not live** until merged into `main` | `main` = what Cloudflare deploys |
| Good for | code, layout, CSS, copy, MDX writing from facts already in the repo or pasted in chat | anything that needs `Media/`: reading reports, extracting facts, composing covers/boards, cut-outs, Figma exports; merging cloud work into `main` |

The owner's routine: he works in the cloud; when something needs `Media/`, he opens a local chat, says what he needs
and "read HANDOFF.md". Then he may come back to the cloud. So **both sides must leave this file up to date at the end of
every change**, as if the next message came from the other side.

### Start of every session (and of every new task in a long session)
- **LOCAL:**
  ```
  git fetch origin
  git checkout main && git pull
  git branch -r --no-merged main        # any origin/claude/* listed = cloud work not yet in main
  git merge origin/claude/<branch>      # for each one listed; resolve conflicts (see below)
  npm install                           # if package.json changed
  build (PowerShell, §2) → if OK: git push
  ```
  Then re-read HANDOFF.md (the merge may have changed it) and the **Session log** (§01). Tell the owner that the cloud
  work is now live (pushed to `main`).
- **CLOUD:**
  ```
  git fetch origin main && git merge origin/main     # bring in local work (Media assets, notes, fixes)
  ```
  Then re-read HANDOFF.md and §01. Never push to `main` (not allowed); push the `claude/*` branch.

### End of every change (both sides)
1. Build, verify, commit, push (LOCAL → `main`; CLOUD → its `claude/*` branch).
2. Add an entry at the **top** of the Session log (§01): date, CLOUD/LOCAL, what changed, what is pending, and any
   **request for the other side**. Also update the sections it touches (§3 file map, §4–§5, §7, §8, §9) and `CLAUDE.md`.
3. Commit and push the HANDOFF update too. Uncommitted = lost (the cloud container is thrown away).
4. CLOUD only: tell the owner when his change is **not live yet** and needs a local session (or a merged PR) to deploy.

### Handing work across
- **Owner's rule (2026-10-04):** when a request needs the local session, the CLOUD session must **say so explicitly**
  in its reply (in Italian: what is missing and why it needs `Media/` or the local machine), do **everything it can**
  first (code, layout, MDX with `<Todo>` placeholders, asset paths wired up), leave a precise `REQUEST → LOCAL` entry
  in §01, push, and give the owner a ready-to-paste message for the local chat. The local chat finishes the job.
- **Cloud needs something from `Media/`:** write a `REQUEST → LOCAL` entry in §01 saying exactly what to produce and
  where to put it (e.g. "Rehab cover 3840×2400 → `src/assets/projects/rehab/cover.png`"; "facts from the Rehab report →
  `notes/02-rehab.md`"). Tell the owner in Italian what to ask the local chat.
- **Facts from `Media/` go into the repo as text**, so the cloud can use them: `notes/NN-name.md` (one file per project:
  numbers with their source and page, team, role, timeline, tools, open questions for the owner). `notes/` is not
  published by Astro. Processed images go to `src/assets/projects/<name>/`, video/PDF to `public/`, as usual. Raw
  `Media/` stays git-ignored.
- **Local finished a request:** mark it `DONE` in §01, push `main`. The cloud merges `origin/main` at its next task.
- **Conflicts:** usually only in HANDOFF.md §01. Keep both entries, newest first. For code, prefer the newer intent and
  check the log. Never force-push `main`; never rebase someone else's history.

---

## 01. Session log (newest first, keep ~15 entries; move older facts into the sections below)

- **2026-10-04 · LOCAL** · JustCook ends with a `Closing`: "JustCook is still a concept… The next version would be a
  tested one." in display size, then "What I take with me — Make the right thing the easy thing." Pushed `main`.
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
  "rippling line", "halftone dissolve" were shown and declined). Hero texture mask now opaque to 78% (was 50%), so the
  fade happens only near the bottom, in the gap above Selected work. Pushed `main`.
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
- **2026-10-04 · CLOUD** · Merged `origin/main` (fast-forward). Added the owner's rule to §00 "Handing work across":
  cloud says explicitly when the local chat is needed, does all it can first, then hands over. No site changes.
  → LOCAL: merge `origin/claude/stoic-ride-lj7woi` at your next start. No open requests.
- **2026-10-04 · LOCAL** · First run of the §00 protocol: `git fetch`, fast-forward merge of
  `origin/claude/stoic-ride-lj7woi` into `main` (only HANDOFF/CLAUDE.md), build OK, pushed. No other unmerged
  `claude/*` branches. No site changes. No open requests.
- **2026-10-04 · CLOUD** · Added §00 (cloud/local protocol) and this log; one line in `CLAUDE.md` points to it. No site
  changes. Cloud branch `claude/stoic-ride-lj7woi` = `main` + this HANDOFF/CLAUDE.md update → LOCAL: merge it at your
  next start. No open requests.

---

## 0. How to work with the owner (read first)

- **Owner:** Valerio Rosponi. Junior UX / digital product / visual designer, 3rd-year BSc "Interfaces & Communication"
  (officially "Interfacce e Tecnologie della Comunicazione") at the University of Trento.
  Git identity: `rosponiv-star` / rosponiv@gmail.com.
- **Language:** always talk to him in **Italian**. All site copy is in **English**.
- **He never edits code.** Every change goes through Claude, so after each change build, commit and push (and log it in §01).
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
- **Repo:** `https://github.com/rosponiv-star/uxportfolio-main`, branch `main` (cloud sessions push to a `claude/*`
  branch instead, see §00). Locally, push works with cached Git
  Credential Manager credentials. `gh` CLI is NOT installed.
- **Deploy:** the owner connects the repo to **Cloudflare** (Pages/Workers: build `npm run build`, output `dist`).
  Domain configured in code: `https://www.valeriorosponi.com` (`astro.config.mjs` `site`, `public/robots.txt`). The
  owner has his own domain on Cloudflare; confirm the exact domain with him if it matters.
- **Machine (LOCAL session):** Windows 11, Node 24. **Run `astro` commands through PowerShell**, because in Git Bash Rolldown's native
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
  - Images are lazy-loaded: before a full-page screenshot, scroll through the page (or set `loading='eager'` on the
    imgs) and wait, otherwise they come out blank.
  - In dev, an image keeps the same URL when its file changes, so the browser shows the old one: hard refresh, or
    `rm -rf .astro node_modules/.astro node_modules/.vite` and restart the server. Production URLs are hashed.
- **Figma** (official MCP, tools `mcp__242ab3dc-…__*`): `get_metadata` to find nodes, `download_assets` with
  `defaultFormat: png, defaultScale: 3` to export, then `curl` the URL (short-lived). JustCook file
  `9kVAJhXfvlz569AYMRGGCn`, canvas "JustCook — Redesign v3" (node 2056:180): use the "… · device" frames (with bezel).
  Exports carry the frame fill #f5f5f5: cut it out with `render/cutout.cjs` (old scratchpad) for use on other grounds.
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
                            (data-cursor / data-cursor-theme), scroll-spy, progress bar (no longer used on case pages:
                            ProcessIndex's bar replaces it), video autoplay
src/data/site.ts            name, email rosponiv@gmail.com, LinkedIn (STILL A PLACEHOLDER URL), CV path, nav
src/components/
  Header.astro              name left; nav 01 Work / 02 Playground / 03 About (micro numbers, active = signal colour)
  Footer.astro              Contact row (email, LinkedIn, Résumé PDF), giant "Valerio Rosponi" wordmark, ©
  Section.astro             THE section pattern (rule, title cols 1–3 sticky, body cols 4–12; `stacked`, `tone="alt"`)
  Collection.astro          shared Work/Playground block: title, filters, Grid/Index switch, grid slot, index table + script
  Card.astro                generic card: media slot; hover = cover zooms out to .95 + paper chips (title/type/year)
  ProjectCard.astro         Card + Cover for a project
  Cover.astro               project cover: real image/video or placeholder (tone colour + faint grid + title)
  DepthTexture.astro        hero background: 3-layer grain, parallax + "breath" near cursor (home: intensity 1.25, parallax 1.6×)
  RegistrationField.astro   old cursor-reactive "+" field; now only the Playground experiment
  case/*.astro              Chapter (title + summary), Key, Note, Figure, Metrics, Insights, Reframes, Archetypes, Todo,
                            ProcessIndex (process line + fixed reading bar), Showcase (Result interface presentation),
                            Stat (big number with a one-time count-up, used by Metrics and Insights), Chips (row or
                            cards, hover note/image), BigStat, Features (feature + cropped screen), Gallery, Closing
src/lib/projects.ts         getProjects, slugOf/hrefOf/numOf, chapterId/chaptersOf, CATEGORIES (re-exports categoryId)
src/lib/collection.ts       categoryId, gridSizes (all 'half'), yearSpan (unused now)
src/content.config.ts       projects schema (categories enum, glance, result {text, media|showcase, metrics})
src/content/projects/       01-justcook.mdx (REAL), 02-rehab, 03-smart-home-ecosystem, 04-realiti, 05-aurawake (PLACEHOLDERS)
src/pages/index.astro       home: hero band + Collection(work) + How I work
src/pages/work/[slug].astro case study template
src/pages/about.astro, playground.astro, 404.astro
src/assets/valerio-rosponi.png   portrait (About)
src/assets/projects/justcook/    cover-app.png (cover: 3 redesigned screens), screens/*.png (14 cut-out devices for the
                                 Result showcase); cover.jpg, fieldwork.jpg, box-family.jpg, flyers.jpg, social.jpg UNUSED
src/assets/projects/justcook/boxes/   box-a…d.png (packaging cut-outs, 800px; hover images + gallery)
src/assets/projects/justcook/brand/   posts (post-box-a…d, post-so-good, post-tris, post-4box, post-app-verde) and
                                 flyers (volantino-pubblicita-*, questionare-flyer), resized JPGs from the old render/out
src/assets/projects/aurawake/    cover.png (2 screens on #f4f4f2)
public/cv/Valerio-Rosponi-CV.pdf  CV (contains his phone number — owner was told; may want a version without it)
Media/                      raw owner material, git-ignored. 01-JustCook: reports, OfficialMedia/{Packaging,Flyers,
                            SocialPosts,Interfaces}; Interfaces holds 17 Figma device exports (3x, 1342×2741), named
                            like HomeFirstScreen.png, FocusMode.png, LiveActivityExpanded.png, BuyReviewOrder.png.
                            05-AuraWake/OfficialMedia/Interfaces: Home.png, AlarmSet1.png (3x).
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
| `--paper-alt` | `#f3f3f0` | tinted bands (How I work, case Result + Insights, About "What I bring") |
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
| `--fs-read` | 17→19px, lh 1.55 | case-study chapter paragraphs only |
| `--fs-stat` | 56→104px, Medium, tight | key numbers (Metrics, insight stats); sign/unit at .42–.55em |
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
- The owner's latest motion calibration (2026-10-04): motion must be barely noticeable — "se uno non ci vuole fare caso
  non ci fa caso". Big rises, scale-ins and reveal choreography were rejected on the case-study showcase.

---

## 5. Pages (current state)

### Home `/`
1. **Hero**: NO background since 2026-10-04 (the grey `--paper-alt` band was removed); `DepthTexture` (intensity
   1.25, parallax 1.6×; was 0.5 / 1×) extends ~56–96px below the hero and fades out with a mask before Selected work. Statement in `.display` spanning
   **cols 1–11**:
   > I'm Valerio Rosponi, a UX and digital product designer studying Interfaces & Communication at the University of
   > Trento, based in Trentino, Italy.

   Height is `min-height: max(360px, 100svh − --peek)`, where `--peek` = gap + `--work-head` (122px; 180px under
   960px) + space-item + ~56–96px. The goal: at scroll 0 the hero dominates and the Selected work header plus the top
   **~80px of the first row of covers** peek in. Measured last: 80px on laptop, 84px on mobile, 95px at 1920, 41px at
   1280×720.
   - Location reads "based in Trentino" (owner's choice, to avoid repeating "Trento").
   - Re-measured after cols 1–11 (2026-10-03): 80px at 1440, 95px at 1920, 84px mobile, only 38px at 1280×720.
2. **Selected work** (`Collection`): no top rule on home: the texture fade separates it.
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
   and full width: one-line text (body lane) → `case/Showcase.astro` → targets. Showcase (owner, 2026-10-04: grey band (a dark ink band was tried and REJECTED, "era meglio prima"),
   small numbered labels, inside the grid, light parallax): 01 Tonight (Home, Focus mode, Streak; trio on tracks
   A/B/C, staggered), 02 Live Activity (pair, full 12 cols, devices cropped to the top 40% on a hairline), 03 Widgets
   (trio cropped to 50%), 04 Buy boxes (quad, 12 cols), 05 The week (Home scrolled, Plan, Boxes, Ingredients; quad, staggered). Shots are
   the Figma "… · device" frames exported 3x into `Media/01-JustCook/OfficialMedia/Interfaces/*.png`, cut out from the
   #f5f5f5 frame fill (flood fill + rim un-blend, old scratchpad `render/cutout.cjs`) and resized to 960px wide into
   `src/assets/projects/justcook/screens/`. Phones: one swipe row per group.
   Motion: NO entrance/reveal animation (owner, 2026-10-04: "leggere animazioni fluide brevemente visibili, se uno
   non ci vuole fare caso non ci fa caso"). Only a quiet inertial parallax on uncropped groups (max 24px, speeds
   .01/.035/.02/.045, desktop) and a 4px hover lift. Rejected: 80px rises + scale, 24px fade-up reveals, crop emerge.
   Without a showcase (placeholder projects): three phone-ratio screens + one wide board (placeholders until real
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
   Data with character (owner, 2026-10-04: numbers must catch the eye, archetypes/reframing more impactful, with boxes):
   Metrics = big bare numbers on a hairline with a ~1.2s one-time count-up (picked over boxed numbers and number +
   bar); numbers buried in paragraphs were pulled out (Challenge: >60% / 44% / 92% desk research; Insights: >60%, 95%,
   ≤3 via `stat`). Archetypes = two LIGHT boxes compared side by side (picked over light+dark boxes and a spectrum).
   Reframes = stepped funnel A–C → B–C → C, discarded ideas struck through, final framing in an ink box (picked over
   a timeline and before→after).
   Second pass (owner: "Cycle 01 and Problem look the same", more impact, less plain text, keep all content):
   label roles fixed site-wide (see CLAUDE.md); numbers bigger (56→104) on ink hairlines, with captions + context
   lines; archetypes get a tinted header and a "Wants" row (Less effort / Less waste, h2); plain text turned into
   scannable blocks: Research methods into the metrics + 8 themes / 36 codes, VPC priorities and launch channels as
   Chips, box specs as Metrics (4–5 / 10 / ~20 min) + profile Chips with box colours (approximate: A #e2843a,
   B #3f8f5b, C #d8503d, D #3b7fc4), app features as numbered rows, the Just Eat line as a pull quote, Reflection
   as a numbered list.
   Third pass (2026-10-04): 92% as a BigStat (Lupi et al. 2015, 258 students); Research split into "Methods" and
   "What came out of it" (boxed); archetype row labels right-aligned with hairline leaders to the boxes; Chips as
   item rows with context and hover notes; Ideate opens with "6 → 1", real cycle numbers 01/05/06 large and faint;
   Design: app features with their screens (Plan, widget, Focus mode, Streak), box chips show the box photo on
   hover (real colours sampled: A #ffa91e, B #488863, C #ff7257, D #29bcff), channel cards (Instagram, WhatsApp,
   QR flyers, short videos) with post/flyer on hover, a Gallery (packaging, maze flyers, 6 posts), a "Launch plan:
   one city first" block (Rovereto/DiPSCo, pickup at Conad Rovereto, word of mouth, signals) written as a PLAN in the
   conditional: the Conad collaboration was proposed but never confirmed, and the owner chose to present it as the
   launch plan; Reflection rewritten in a warmer first person (surprise, own bias, what I'd do, honest close).
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
| 01 JustCook | **Written, real data; real cover** | Cover (2026-10-04) = 3 device screens from Figma page "JustCook — Redesign v3" (frames "Home · first screen · device", "Home · scrolled · device", "Boxes · device", exported PNG 3x = 1342×2741, saved as `Media/01-JustCook/OfficialMedia/Interfaces/HomeFirstScreen.png`, `HomeScrolled.png`, `Boxes.png`). The exports carry the Figma frame fill #f5f5f5, so the cover ground and tone are #f5f5f5 (no cut-out needed). `src/assets/projects/justcook/cover-app.png`, 3840×2400, phones 1800px tall, 96px gaps. Older prepared boards stay unused in the same folder. Result = interface showcase (see §5); "Home · change box" was removed from it by the owner. "Home · scrolled" was updated in Figma on 2026-10-04 and re-exported (cover + showcase). |
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
- Media boards inside JustCook (removed for now: "ci penseremo dopo"). The Result showcase uses app screens instead.
- Card hover: paper caption bar covering the cover; cover shrinking to fit the bar; title/meta inside the cursor
  label (E2) and its tech-editorial variants (E3 tabbed card, E4 crosshair, E5 typographic); corner tag (B, B3
  translucent was runner-up), B4 spec sheet, B5 traced frame, B6 ruler strip; free text; slim line. Chips won.
- Case study: PhoneScroll device scene; Overview with gutter hairlines ("too many lines"), as a dark band, as stacked
  sentences, as text + data column; process index as row TOC, dotted book TOC, sticky side index.
- Covers: any "depth" (radial studio light / vignette, cast shadows under phones, diffuse halo). Flat ground only.
- Result showcase: dark ink band ("era meglio prima"); entrance animations of any size (80px + scale, then 24px
  fade-ups, crop emerge); breaking out of the grid (he chose "dentro la griglia").

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
   - DONE (2026-10-04): the screens of canvas "JustCook — Redesign v3" were exported and used for the cover and the
     Result showcase. Further edits in Figma → re-export the changed frame and replace it everywhere it appears.
5. **Covers:** JustCook and AuraWake have real covers; Rehab, Smart Home, Realiti still placeholders.
6. **Case studies 02–05**: the full interview-then-write process.
7. **Filters:** decide whether to drop UX/UI (it is on every project). Confirm the categories per project.
8. **CV** may contain his phone number; he may want a version without it.
9. **Tools** list for JustCook: ask whether to add others besides Figma and Miro.
10. Keep `CLAUDE.md` AND this file in sync after every change, including the file map (§3), the design tables (§4)
    and the rejected list (§8), not only the section being worked on. (The old stale CLAUDE.md lines were fixed.)
11. JustCook: chapter figures are still text-only; the Design chapter could use a few of the exported screens if the
    owner wants (none is placed in the chapters yet).

---

## 10. Memory

Persistent memory dir: `C:\Users\rospo\.claude\projects\C--Users-rospo-Documents-ClaudeCode-Websites-uxportfolio\memory\`
(`portfolio-project-goal.md`, `design-taste-feedback.md`). Update it when the owner reveals new durable preferences.
