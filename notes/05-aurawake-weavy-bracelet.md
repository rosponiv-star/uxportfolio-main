# AuraWake bracelet in Weavy: what to do (2026-11-07)

The owner makes the photographic bracelet images in Weavy; Claude then places them and matches the Blender model
(line drawings, system, gestures, room scenes, exploded) to them.

## Decisions (owner, 2026-11-07)

- Design stays: one continuous woven strap, light-blue melange (Sport Loop type), flat black satin steel loop, the
  strap folds over the loop's outer bar, hook-and-loop closure on the side opposite the sensors; the sensor module sits
  inside the strap right next to the loop, hidden from outside, visible from the wrist side.
- Charging: the bracelet lies on the base closed, as a ring (its axis vertical, the strap standing on its lower edge).
  Where the module is, the lower edge carries 3 small gold contact pads in a row (4 mm apart); they sit on the base's
  3 gold spring pins, which are in a row parallel to the front. Two magnets in the base pull the module onto the pins.
- Module size to aim for: about 36 × 19 × 6 mm (sensor, battery for 2–3 nights, Bluetooth chip). It does not vibrate.
- The bracelet goes on: product slide (57), exploded (63), cover drawing, plus system, gestures and room scenes.

## Setup in Weavy (once)

1. New file. Add one **Import / Image** node per reference image (below) and drag the file in.
2. Add a **Prompt** node and a model node **Nano Banana Pro** (Google Gemini image). Connect the images and the prompt
   to the model.
3. Settings: aspect ratio as written for each shot, highest resolution (2K or 4K), 1–2 outputs per run.
4. Export each result as PNG and save it in `Media/05-AuraWake/Weavy/` with the shot name (e.g. `B1-hero.png`).
   Tell Claude when they are there.

Reference images (all in the repo, `deck/assets/aurawake/`):
- `render-band.jpg` — the shape (Blender v7): ring, loop, fold. Use in every shot.
- `bracelet-weavy-v2.jpg` — the fabric we liked. Use in every shot.
- `product-hero.png` — the base, for shot B4.
- `view-top.png` — the base from above with the 3 pins, for shot B3 and B4.

## The common description (paste it at the start of every prompt)

> Product photograph of a sleep-tracking bracelet. One continuous woven nylon strap, light-blue melange with tiny
> white flecks, 19 mm tall, with corded edges. A flat black satin-steel rectangular loop; the strap passes through the
> loop and folds visibly over its outer bar; the tail closes with hook-and-loop on the outside, on the side opposite
> the sensors. A slim graphite sensor module (36 × 19 × 6 mm, soft corners, matte) sits inside the strap right next to
> the loop: hidden from outside, visible only on the wrist side, with a small dark glossy optical sensor window. On the
> module's lower edge, three small gold contact pads in a row, 4 mm apart. No screen, no buttons, no lights, no logo.
> Match the shape of the first reference and the fabric of the second exactly.

## Shots

**B1 · hero** (4:3) — common description +
> The bracelet closed as a ring, lying on its edge on an invisible surface, three-quarter view from slightly above,
> the loop and the inside of the module visible. Pure white seamless background, soft studio light from the top left,
> a very soft contact shadow only. Sharp focus, true colours, photorealistic, no props, no text.

**B2 · wrist side** (4:3) — common description +
> Close-up of the inside of the ring at the module: the graphite face and the dark sensor window, the strap fabric
> around it, the steel loop beside it. Pure white background, soft studio light, shallow depth of field kept sharp on
> the sensor window. Photorealistic, no text.

**B3 · charging edge** (4:3) — common description +
> Close-up from below and the side of the module's lower edge: the three gold contact pads in a row, 4 mm apart, flush
> with the graphite, the fabric edge around them. Pure white background, soft studio light. Photorealistic, no text.

**B4 · on the base** (4:3) — common description + (add `product-hero.png` and `view-top.png` as references)
> The bracelet resting on the top of the graphite alarm base from the third reference, closed as a ring and lying on
> its edge, the module's lower edge sitting on the three gold pins of the base (the pins are in a row parallel to the
> front, centred). Same camera, light and white background as the third reference; the base must stay exactly as it
> is. Photorealistic, no text.

## If a result is wrong

Add one short line at the end and run again, for example: "The module must be next to the loop, not opposite it.",
"The strap must fold over the loop's outer bar.", "No logo, no text.", "Keep the base exactly as in the reference."
If two runs miss, send the best one to Claude: small fixes can be done afterwards.
