# AuraWake bracelet in Weavy: the node chain (2026-11-07)

The owner makes the photographic bracelet images in Weavy; Claude then places them (slides 57, 63, cover) and
matches the Blender model (line drawings, system, gestures, room scenes, exploded) to them.

## Decisions (owner, 2026-11-07)

- Design stays: one continuous woven strap, light-blue melange (Sport Loop type), flat black satin-steel loop; the
  strap folds over the loop's outer bar and closes with hook-and-loop on the side opposite the sensors.
- The sensor module is set into the strap, framed by the fabric, flush (as in `bracelet-weavy-v2.jpg`), right next to
  the loop; hidden from outside, visible from the wrist side (only a small dark sensor window).
- Charging: the bracelet lies on the base closed, as a ring standing on its lower edge. A small graphite foot leaves
  the module and sticks out just below the strap's lower edge (as in v2); 3 gold pads, 4 mm apart, on its underside,
  sit on the base's 3 gold pins (a row parallel to the front). Two magnets in the base pull it onto the pins.
- Module about 34 × 12.5 × 3 mm, the strap itself rising around it. It does not vibrate. No screen, buttons, lights, logo.

---

## 0. Current method (2026-11-08): Blender render as the shape, Nano Banana for the photo

The chain below let the model invent the shape (pads in the wrong place, a chip on the fabric, a fake closure). Blender
gets the parts right but looks fake. So: one Nano Banana Pro node per shot, with the render as the FIRST image and
`bracelet-weavy-v2.jpg` as the SECOND. Guides in `Media/05-AuraWake/Weavy/`: `guide-outside.jpg`, `guide-under.jpg`.
Settings: 4K, 4:3. The Figma/Weave connector in Claude Code is out of free runs: run it in the Weavy app.

**Prompt, `guide-outside.jpg`** (save as `B1-outside.png`)

```
Turn the FIRST image into a real studio product photograph of the same bracelet. The first image is a 3D render that fixes the layout: keep exactly the same camera angle, framing, proportions, the position of the black loop and the position of the fold. Do not add, remove or move any part. Do not show any sensor, module or electronics: from this side only the fabric and the loop are visible. The render looks rigid and fake, so make it a real soft object: the woven strap relaxes a little, with a gentle, slightly irregular curve instead of a perfect oval, soft rounded corded edges, real fabric thickness, and natural tension where it passes through the loop and folds back on itself, closing with hook-and-loop. Copy the material exactly from the SECOND image: the same chunky woven nylon, light-blue melange with white heathered threads, same corded edges, and the same flat black satin-steel loop. Use the second image only for material, never for its shape or its visible sensor. Pure white seamless background, soft studio light from the top left, one very soft contact shadow, sharp focus, true colours, photorealistic. No logo, no text.
```

**Prompt, `guide-under.jpg`** (save as `B2-under.png`)

```
Turn the FIRST image into a real studio product photograph of the same bracelet. The first image is a 3D render that fixes the layout: keep exactly the same camera angle, framing, proportions, the position of the black loop and the position of the fold. Do not add, remove or move any part. From this low angle the only hardware besides the loop is the small flat graphite charging foot under the strap, with exactly three small round gold contact pads in a row, exactly where they are in the first image: keep it, same size, same place. Do not show any sensor window or other electronics. The render looks rigid and fake, so make it a real soft object: the woven strap relaxes a little, with a gentle, slightly irregular curve instead of a perfect oval, soft rounded corded edges, real fabric thickness, and natural tension where it passes through the loop and folds back on itself, closing with hook-and-loop. Copy the material exactly from the SECOND image: the same chunky woven nylon, light-blue melange with white heathered threads, same corded edges, and the same flat black satin-steel loop. Use the second image only for material, never for its shape or its visible sensor. Pure white seamless background, soft studio light from the top left, one very soft contact shadow, sharp focus, true colours, photorealistic. No logo, no text.
```

## 1. How the chain works

For each shot, four rounds. Each round = an image model draws or corrects, then a vision LLM inspects the result
against a 12-point checklist and writes exactly what to fix; the next image model applies only that fix.

```
 REFERENCES ─┐
 SPEC + SHOT ─┴─► [NB1 generate] ─► img1 ─► [LLM check 1] ─► review1
                                     img1 + review1 ─► [NB2 fix: structure] ─► img2 ─► [LLM check 2] ─► review2
                                     img2 + review2 ─► [NB3 fix: foot & pads] ─► img3 ─► [LLM check 3] ─► review3
                                     img3 + review3 ─► [NB4 fix: finish]      ─► img4 ─► [LLM final]   ─► report
```

- NB = **Nano Banana Pro** node. LLM = Weavy's **LLM node with image input** (it may be called "Run Any LLM",
  "Any LLM" or "LLM"; choose a model that can see images: Gemini 2.5 Pro / Gemini 3 Pro, Claude, GPT-4o/GPT-5).
- Each fix round has a focus, so problems are attacked one family at a time: round 2 the structure (module position,
  fold, module set into the fabric), round 3 the charging foot and the pads, round 4 material and photo finish.
- Texts are joined with the **Prompt Concatenator** node (it may be called "Concatenate" / "Text Concat"); fixed texts
  live in **Text** nodes (or "Prompt" nodes) so you paste them once.
- Cost per shot: 4 Nano Banana Pro runs + 4 LLM runs. Four shots: 16 + 16.

---

## 2. Build it once (shot B1), step by step

Lay the canvas out in columns from left to right, so you can read the chain.

**Column A · references (4 Import / Image nodes)**
1. `A1` ← `deck/assets/aurawake/bracelet-weavy-v2.jpg` (fabric, module set in, foot, fold). It is the MAIN reference.
2. `A2` ← `deck/assets/aurawake/render-band.jpg` (overall ring shape and the loop).
3. `A3` ← `deck/assets/aurawake/product-hero.png` (the base; only shot B4).
4. `A4` ← `deck/assets/aurawake/view-top.png` (the 3 pins from above; only shot B4).

**Column B · fixed texts (Text nodes; paste the texts from section 3)**
5. `T-SPEC` ← text **SPEC**.
6. `T-SHOT` ← text **SHOT B1** (for the other shots you change only this node).
7. `T-CHECK` ← text **CHECK**.
8. `T-FIX2` ← text **FIX · round 2 (structure)**.
9. `T-FIX3` ← text **FIX · round 3 (foot and pads)**.
10. `T-FIX4` ← text **FIX · round 4 (finish)**.
11. `T-FINAL` ← text **FINAL REPORT**.

**Column C · generate**
12. Concatenator `C-GEN`: inputs in this order `T-SPEC`, `T-SHOT`.
13. `NB1` (Nano Banana Pro): images in this order `A1`, `A2`; prompt ← `C-GEN`.
    Settings: aspect ratio 4:3, highest resolution (2K or 4K), 1 output (2 if you want to choose).

**Column D · check 1**
14. Concatenator `C-CHK`: `T-CHECK`, `T-SPEC`, `T-SHOT` (built once, reused by every check).
15. `LLM1`: images in this order **`NB1` output, `A1`**; prompt ← `C-CHK`. Output: text `review1`.

**Column E · fix 2 (structure)**
16. Concatenator `C-FIX2`: `T-FIX2`, `T-SPEC`, `T-SHOT`, `LLM1` output.
17. `NB2`: images in this order **`NB1` output, `A1`, `A2`**; prompt ← `C-FIX2`. Same settings as NB1.

**Column F · check 2**
18. `LLM2`: images **`NB2` output, `A1`**; prompt ← `C-CHK`.

**Column G · fix 3 (foot and pads)**
19. Concatenator `C-FIX3`: `T-FIX3`, `T-SPEC`, `T-SHOT`, `LLM2` output.
20. `NB3`: images **`NB2` output, `A1`**; prompt ← `C-FIX3`.

**Column H · check 3**
21. `LLM3`: images **`NB3` output, `A1`**; prompt ← `C-CHK`.

**Column I · fix 4 (finish)**
22. Concatenator `C-FIX4`: `T-FIX4`, `T-SPEC`, `T-SHOT`, `LLM3` output.
23. `NB4`: images **`NB3` output, `A1`**; prompt ← `C-FIX4`.

**Column J · final report**
24. Concatenator `C-FIN`: `T-FINAL`, `T-SPEC`, `T-SHOT`.
25. `LLM4`: images **`NB4` output, `A1`**; prompt ← `C-FIN`. Output: the PASS/FAIL table for you.

Image order matters: the image to correct is ALWAYS the first one, the references come after. The texts say "the
first image" and "the second image" on that basis.

## 3. Running it

1. Run node by node the first time (Run on NB1, then LLM1, then NB2…), so you can look at each step. Once it works,
   use "Run all".
2. After each LLM node read the review: if a FAIL is wrong (the LLM saw badly), you can type in the next round's
   concatenator an extra Text node with "Ignore item N of the review." before running the fix.
3. If a fix round makes things worse, re-run that NB node (each run varies) or feed the previous image to the next
   round instead (reconnect).
4. When LLM4 says all PASS, or only cosmetic FAILs remain, download NB4's output as PNG.
5. If after the chain something is still wrong, duplicate the last pair (check + fix) and add a fifth round, focus on
   what is left: use FIX · round 4 with its first line changed to the problem.

## 4. Other shots

1. Select everything (column A–J), copy, paste below. In the copy change only `T-SHOT` (B2, B3, B4).
2. **B4**: connect also `A3` and `A4` to NB1 (images `A1`, `A2`, `A3`, `A4`), to every fix NB (after the image to fix)
   and to every LLM (after the image to check), and add the text **CHECK · B4 extra** to `C-CHK` and `C-FIN`.
3. Save as `Media/05-AuraWake/Weavy/B1-hero.png`, `B2-wrist.png`, `B3-pads.png`, `B4-on-base.png`; also keep NB1
   outputs if you like them (`B1-hero-raw.png`…), Claude can compare. Tell Claude when they are there.

---

## 5. The texts (copy each into its Text node, as they are)

### SPEC

```
SPECIFICATION — sleep-tracking bracelet, product photograph.
Build it exactly like the reference image of the bracelet (the woven light-blue one), with two changes only.
S1 Strap: one continuous woven nylon strap, light-blue melange with fine white flecks, about 19 mm tall, soft corded (piped) top and bottom edges, slightly matte, visible weave.
S2 Loop: one flat black satin-steel rectangular loop with soft corners, about 21 mm inside, thin.
S3 Closure: the strap passes through the loop, folds back over the loop's outer bar and lies flat on itself on the outside of the ring, closing with hook-and-loop. The strap end is hidden under the folded layer; nothing sticks out of the ring; no loose end, no second buckle.
S4 Module: a matte graphite sensor module, about 36 × 19 × 6 mm, soft corners, set INTO the strap: the fabric frames it on all sides with a neat stitched border, its face flush with the fabric. It is not a separate metal plate clipped or glued on top of the strap. No shiny chrome.
S5 Position (change 1): the module sits on the inside of the ring RIGHT NEXT TO the loop (its end 5–10 mm from the loop), never on the opposite side of the ring.
S6 Wrist face: on the module's inner face only one small dark glossy optical sensor window, centred. Nothing else on that face: no pads, no pins, no text.
S7 Charging foot: a small flat graphite foot leaves the lower end of the module and sticks out about 3 mm below the strap's lower edge, like in the reference.
S8 Pads (change 2): exactly three small round gold contact pads in a row, 4 mm apart, on the UNDERSIDE of that foot, facing down towards the surface the ring stands on. They are the only gold on the bracelet.
S9 Nothing else: no screen, no buttons, no lights, no logo, no text, no other hardware.
S10 Photo: pure white seamless background (#FFFFFF), soft studio light from the top left, a very soft contact shadow only, sharp focus, true colours, photorealistic, no props.
```

### SHOT B1

```
SHOT B1 · hero, 4:3. The bracelet closed as a ring, standing on its lower edge on an invisible white surface, three-quarter view from slightly above. The loop, the fold over it and the inside of the module (its sensor window) must all be visible; the foot just visible at the bottom of the module.
```

### SHOT B2

```
SHOT B2 · wrist side, 4:3. Close-up of the inside of the ring at the module: the graphite face with its dark sensor window, the fabric border that frames it, the steel loop just beside it, the top of the foot below. Sharp on the sensor window.
```

### SHOT B3

```
SHOT B3 · charging foot, 4:3. Close-up from below and slightly to the side of the module's lower end: the small graphite foot sticking out below the strap's lower edge and, on its underside, the three gold pads in a row, 4 mm apart; the fabric edge and the module above it.
```

### SHOT B4

```
SHOT B4 · on the base, 4:3. The bracelet resting on the top of the graphite alarm base shown in the third image, closed as a ring and standing on its lower edge, its charging foot sitting on the three gold pins of the base. The pins are in a row parallel to the front of the base, centred, as in the fourth image. Same camera, light and white background as the third image; the base must stay exactly as it is.
```

### CHECK

```
You are a strict quality inspector for industrial-design product photos. The FIRST image is a generated photo to inspect. The SECOND image is the reference bracelet: copy it for the fabric, the module set into the strap, the charging foot and the fold over the loop; its module POSITION and its pad layout are NOT to be copied (see S5 and S8).
Inspect the first image against the specification and the shot below. Look closely and zoom in mentally on the module, the foot, the loop and the strap end. Do not be lenient: if you are not sure, it is a FAIL.
Answer in English, in exactly this format and nothing else:
C1 Strap fabric, colour, flecks, corded edges match the reference (S1): PASS or FAIL – reason
C2 Loop flat black satin steel, rectangular, soft corners (S2): PASS or FAIL – reason
C3 Real closure: strap through the loop, folded over its outer bar, lying flat on itself, end hidden, nothing sticking out (S3): PASS or FAIL – reason
C4 Module set into the strap, framed by fabric, flush, matte graphite, not a plate on top (S4): PASS or FAIL – reason
C5 Module right next to the loop, not opposite (S5): PASS or FAIL – reason
C6 Wrist face: only one small dark sensor window, no pads or pins (S6): PASS or FAIL – reason
C7 Charging foot sticking out about 3 mm below the strap's lower edge (S7): PASS or FAIL – reason
C8 Exactly three gold pads, in a row, on the underside of the foot, no gold elsewhere (S8): PASS or FAIL – reason
C9 No screen, buttons, lights, logo, text, extra hardware (S9): PASS or FAIL – reason
C10 Geometry is physically possible: no melted or merged fabric, no duplicated or floating parts, strap continuous all round: PASS or FAIL – reason
C11 Pure white background, soft light, soft contact shadow, sharp, photorealistic (S10): PASS or FAIL – reason
C12 Framing and view as asked by the shot: PASS or FAIL – reason
EDIT: one paragraph for an image editor saying exactly what to change in the first image to fix every FAIL, most important first, each with where it is in the picture (left, right, top, bottom, near the loop…). Say also what must NOT change. If everything is PASS write: EDIT: NO CHANGES.
```

### CHECK · B4 extra (only for B4, add after CHECK)

```
Also check, for the B4 shot (the THIRD image is the base reference, the FOURTH the base from above):
C13 The base is identical to the third image: same graphite colour, size, proportions, holes, front LED, nothing added: PASS or FAIL – reason
C14 The bracelet's charging foot sits on the three gold pins of the base, which are in a row parallel to the front, centred: PASS or FAIL – reason
Put these two lines before the EDIT line and include their fixes in the EDIT.
```

### FIX · round 2 (structure)

```
Edit the FIRST image. It is a product photo that is partly right. Keep everything that is already correct exactly as it is: same camera, framing, light, background, colours, fabric. Change only what the inspection report at the end marks as FAIL, following its EDIT paragraph.
In this round give priority to the STRUCTURE: the module set into the strap and framed by the fabric (not a plate on top), the module right next to the loop, the strap really folded over the loop's outer bar with its end hidden. Copy these from the SECOND image (the reference bracelet), except the module position, which must be next to the loop.
If the EDIT paragraph says NO CHANGES, return the first image unchanged.
The specification and the shot follow, then the inspection report.
```

### FIX · round 3 (foot and pads)

```
Edit the FIRST image. Keep everything that is already correct exactly as it is: same camera, framing, light, background, colours, fabric, module, loop and fold. Change only what the inspection report at the end marks as FAIL, following its EDIT paragraph.
In this round give priority to the CHARGING FOOT and the PADS: a small flat graphite foot leaving the lower end of the module and sticking out about 3 mm below the strap's lower edge (like the foot in the SECOND image); exactly three small round gold pads in a row, 4 mm apart, on the underside of that foot only; the module's wrist face shows only the small dark sensor window. Remove any pads, pins or gold anywhere else.
If the EDIT paragraph says NO CHANGES, return the first image unchanged.
The specification and the shot follow, then the inspection report.
```

### FIX · round 4 (finish)

```
Edit the FIRST image. Keep the object exactly as it is: shape, parts, positions, colours. Change only what the inspection report at the end marks as FAIL, following its EDIT paragraph.
In this round give priority to MATERIAL and PHOTO FINISH: crisp continuous weave matching the SECOND image, clean corded edges, a neat stitched fabric border around the module, matte graphite (no chrome), flat black satin steel loop, no logo or text, pure white background, soft light from the top left, one very soft contact shadow, sharp focus, true colours, no artefacts.
If the EDIT paragraph says NO CHANGES, return the first image unchanged.
The specification and the shot follow, then the inspection report.
```

### FINAL REPORT

```
You are a strict quality inspector. The FIRST image is the final product photo; the SECOND is the reference bracelet (copy its fabric, module set into the strap, foot and fold; not its module position or pad layout).
Use the same checks C1–C12 (and C13–C14 for B4) against the specification and shot below, in the same PASS/FAIL format. Then write:
VERDICT: READY (all PASS, or only tiny cosmetic issues) or NOT READY.
REMAINING: the issues still open, most important first, one line each, in Italian.
```

---

## 6. If there is no LLM node that can see images

Keep the four Nano Banana Pro rounds and do the checks yourself with the CHECK list (C1–C12): write the EDIT paragraph
by hand in a Text node and connect it where the LLM output would go. The fix texts work the same way.
