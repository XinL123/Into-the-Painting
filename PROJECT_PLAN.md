# Project plan — pilot: 清明上河图, one scene

## 1. Recommended MVP

One painting (the Song original of 清明上河图), one immersive scene (the Rainbow Bridge and the boat,
framed through to the great willow; see [SCENE_SELECTION.md](SCENE_SELECTION.md)), reached through a
small gallery and a full-scroll overview.

### In scope

- Gallery page with one live painting and quiet placeholders for future ones
- Overview of the full scroll, pannable, with the one enterable scene indicated
- Enter transition: zoom to the scene, then depth appears
- The scene: 5 broad layers, pointer/drag parallax, slight zoom, 2–3 subtle motion systems
- Exit transition back to the overview
- Short caption and credit line (title, artist, dynasty, collection, image source)
- Desktop first; touch drag supported; reduced-motion fallback (static scene, no parallax drift)

### Out of scope

- Any other section of the scroll being interactive; multiple hotspots or branches
- Individually animated people or objects; walking figures
- Free camera, rotation, walking, 360° view
- True 3D geometry, lighting, shadows
- Other paintings (placeholders only)
- Sound, narration, annotations/tour, CMS, accounts, analytics
- Generative alteration or upscaling of the artwork

## 2. User journey

```
┌───────────┐   select    ┌────────────────┐  click marked  ┌──────────────┐
│  GALLERY  │ ──────────▶ │   OVERVIEW     │ ─────────────▶ │    SCENE     │
│ paintings │             │ the full scroll│    scene       │ depth+motion │
│ as brushed│ ◀────────── │ pan left/right │ ◀───────────── │ look around  │
│ windows   │    back     │ one scene mark │  back / Esc /  │              │
└───────────┘             └────────────────┘  zoom out      └──────────────┘
```

1. Arrive at the gallery: paper ground, a few brushed windows, one of them alive.
2. Select 清明上河图; its window opens out into the whole scroll (overview).
3. Pan along the scroll (drag / wheel / arrow keys). It is shown flat, as itself.
4. One section carries a quiet mark (a thin brushed bracket and a small label "入画 · Enter").
5. Click it: the view glides and zooms until that section fills the screen.
6. For a beat it is still the flat painting. Then the layers ease apart and the water begins to move.
7. Move the pointer or drag: the view leans left/right, slightly up/down. Scroll/pinch: slight zoom.
8. Leave with Esc, a back control, or zooming out past the minimum: depth settles to flat, the view
   pulls back to the overview.

## 3. Interaction model inside the scene

"Leaning into the painting and looking around slightly."

```
            look range (the whole of it)
        ◀──────────── pan ────────────▶          The scene crop is wider than the screen.
   ┌───────────────────────────────────────┐      Pan moves the window across it, softly
   │      ┌─────────────────────┐          │      clamped at both ends.
   │      │   what you see      │  ↕ small │
   │      │                     │    tilt  │      Zoom: 1.0× – about 1.25×, eased.
   │      └─────────────────────┘          │      No rotation. No walking.
   └───────────────────────────────────────┘
```

| Input | Effect | Limit |
|---|---|---|
| Pointer move (desktop) | Viewpoint leans; layers shift by depth | a few % of the view; eased, never 1:1 |
| Drag / touch drag | Pan left/right across the wide crop | clamped to crop edges with soft resistance |
| Wheel / pinch | Slight zoom | about 1.0–1.25× |
| Idle | Very slow breathing drift so the scene is never frozen | amplitude smaller than pointer parallax |
| Esc / back / zoom out at minimum | Exit | — |

Rule of thumb for strength: the front-most layer moves no more than about 2–3 % of the screen width
relative to the back layer at full lean.

## 4. Layers and motion

```
  side view (viewer on the left)

  eye ▷      L4 willow     L3 rooftops    L2 bridge+street    L1 river+boat    L0 far bank
             │             │              ╲ (tilted: near end  │                │
             │             │               ╲ closer)           │                │
  near ◀─────┴─────────────┴────────────────╲──────────────────┴────────────────┴────▶ far
              moves most                                                   moves least
```

Motion systems (start with the first two; add the third only if the scene still feels still):

1. **Water** — a slow, low-amplitude distortion and light shimmer confined to the river mask. It moves
   the painted water lines; it does not draw new ones.
2. **The boat** — rocks a degree or so and drifts a few pixels on a long period.
3. **Willow twigs** — sway increasing toward the twig tips, driven by slow noise.

People do not move in the MVP.

## 5. Transition logic

The transitions rely on one fact: **with layer separation at zero, the scene is pixel-identical to
the flat crop.**

```
 ENTER
 overview (flat scroll)                                   scene
 ┌─────────────────────────────┐   1 glide+zoom    ┌──────────────┐   3 separate   ┌──────────────┐
 │        ┌╌╌╌╌╌╌┐             │ ───────────────▶  │ flat crop    │ ─────────────▶ │ ▓▒░ layers   │
 │        ┆scene ┆             │   (same image)    │ fills screen │  depth 0 → 1   │ parallax on  │
 │        └╌╌╌╌╌╌┘             │                   └──────────────┘  motion fades  └──────────────┘
 └─────────────────────────────┘     2 swap: flat image → layered scene            in
                                       (invisible, they match exactly)

 EXIT = the same steps in reverse: motion fades out → depth 1 → 0 → swap → pull back to overview
```

1. **Glide and zoom** (about 1.4 s, slow ease): the overview scales and translates so the scene's
   rectangle fills the viewport; the rest of the scroll dims toward paper at the edges.
2. **Swap**: the layered scene, at zero separation, replaces the flat image. No visible change.
3. **Awaken** (about 2 s): separation eases 0 → 1 while the camera pushes in a little; water motion
   fades in last. UI (back control, caption) appears afterwards, small.

Interruptible: exit requested mid-enter simply reverses the timeline.

## 6. Technical approach

### Options compared

| Approach | Preserves artwork | Depth quality | Motion (water etc.) | Complexity | Verdict |
|---|---|---|---|---|---|
| **A. Layered images, CSS transforms** (+ GSAP) | Excellent | Good for flat bands; cannot tilt a layer | Poor: no real water distortion (SVG filters are slow and coarse) | Lowest | Good for the gallery/overview, not enough for the scene |
| **B. Single image + depth-map displacement** (shader) | Good, but stretches pixels at depth edges ("rubber" artefacts around the bridge rail and twigs) | Continuous, but needs a clean depth map, which AI estimators do badly on scroll projection | Fine | Medium | Not alone |
| **C. Layered planes in WebGL** (a handful of textured quads at different depths, perspective camera) | Excellent: each layer is unstretched original pixels | Real parallax from real camera movement; a layer can be tilted or gently displaced | Excellent: small fragment/vertex shaders per layer | Medium | **Core of the recommendation** |
| **D. Canvas 2D layers** | Excellent | Same as A | Per-pixel water is too slow on a 4K canvas | Low–medium | No advantage over A or C |
| **E. Full 3D reconstruction** (models, projection mapping) | Poor: must repaint what the painter did not paint | "True", and wrong for this art | — | Very high | Rejected (see README) |
| **F. React Three Fiber** | same as C | same as C | same as C | Adds React for one canvas | Unjustified here |

### Recommendation: a hybrid, kept small

- **Gallery and overview: plain DOM + CSS** (mask-image for brush shapes, transforms for pan/zoom),
  with **GSAP** for timelines. Text stays real text; images stay images; it is light and accessible.
- **Scene: one WebGL canvas with Three.js**, containing about five textured planes at different
  depths and a perspective camera with a tightly limited range. Approach **C**, borrowing one idea
  from **B**: a layer that crosses depth (the bridge, the river surface) gets a simple hand-authored
  depth gradient so it tilts instead of sitting flat.
- **Build: Vite, vanilla JavaScript (ES modules)**. No framework.

Why this and not something simpler: CSS layers would give the parallax, but not the two things that
make the scene feel alive without adding anything foreign, namely water that moves *within the painted
lines* and twigs that bend rather than slide. Those need per-pixel/per-vertex control, which is what
a shader gives. WebGL is used only where it earns its place.

Why not something heavier: there is no geometry, lighting or scene graph to manage; a React layer or
a 3D asset pipeline would be overhead with no visual return. Three.js is chosen over smaller WebGL
libraries (OGL, PixiJS) for documentation and longevity; the scene uses a very small part of it, and
the choice is easy to revisit since each layer is just a quad with a shader.

Performance budget: 5–6 textures at most 4,096 px wide, one draw call each, 60 fps on an integrated
GPU; render only while something is moving; half-resolution textures on small screens.

## 7. Suggested architecture

Extensible by data, not by abstraction: a painting is a folder and a manifest; the code for the pilot
stays specific and readable.

```
3D painting/
  index.html                      gallery (single page; overview and scene are states of it)
  src/
    main.js                       state machine: gallery ⇄ overview ⇄ scene
    gallery/                      brushed windows, hover/selection
    overview/                     scroll pan/zoom, scene marker
    scene/
      stage.js                    renderer, camera, limits, render-on-demand
      layers.js                   builds planes from the manifest
      motion/                     water, sway, bob (small shader snippets)
    transitions/                  enter/exit timelines
    paintings/
      index.js                    list of paintings (one live, others "forthcoming")
      qingming/painting.json      title, credits, overview image, scene rect, layers, depths, motion
  assets/                         see ASSET_PLAN.md
  scripts/                        asset preparation
```

Sketch of what the manifest holds (shape only, not final):

```
painting:  id, titles (zh/en), artist, dynasty, collection, credit, overview image
scene:     id, name, rect within the overview, look limits, zoom limits
layers[]:  image, depth (0 far … 1 near), optional depth-gradient image, optional motion {type, mask, strength}
```

Adding a second painting later means a new folder and manifest, plus whatever new motion type that
painting needs. Nothing more general is built until that second painting asks for it.

Where it lives: this folder sits inside the portfolio repo under `playground/`. The plan assumes it
is built as a self-contained sub-project here and linked from the portfolio's playground later.

## 8. Risks and trade-offs

| Risk | Effect | Mitigation |
|---|---|---|
| Source resolution (1,800 px tall) | Soft at 4K or with strong zoom | Cap zoom at about 1.25×; show the scene letterboxed on paper rather than upscaled on very large screens; pursue a licensed museum master later |
| Image provenance | The open file is not museum-issued | Verify against the Palace Museum viewer; record source and checksum; clear credit; licence application as an option |
| Bridge crosses depth | A flat bridge layer looks like a cardboard cut-out | Depth gradient on that layer; small parallax; build it last, keep the option of leaving it on the river layer |
| Mask edges (twigs, rail, crowd) | Halos or cut figures break the illusion | Soft, slightly inset masks; keep parallax within what the edges tolerate; you review edges |
| Revealed gaps behind layers | Smears or holes at full lean | Small parallax; tone-extension fills; no invented painting |
| Over-animation | It stops feeling like the painting | Global "liveliness" dial; default low; review with motion off vs on |
| Cut-out look | Layers read as paper theatre, not as one painting | Shared silk grain over the whole composite; very small separation; soft edges |
| Scope creep | More hotspots, moving people, more scenes | This document's out-of-scope list; one scene until it is right |
| Mobile GPU / memory | Large textures fail or stutter | 4,096 px cap, half-size set, render on demand |

## 9. Phases

Detailed tasks are in [TASKS.md](TASKS.md).

| Phase | Outcome | You review |
|---|---|---|
| 0. Research and decisions | These documents; approved source, scene, stack | The decisions below |
| 1. Structure and static viewer | Project skeleton; approved master stored; scene crop visible flat in the browser | Crop framing |
| 2. Gallery and overview | Brushed gallery; full scroll pannable; scene marker | Look and feel of the gallery |
| 3. Enter/exit transition | Glide-zoom into the flat crop and back | Timing and feel |
| 4. Depth and parallax | Layers separated; look-around working | Depth strength, mask edges |
| 5. Subtle animation | Water, boat, willow | Motion strength |
| 6. Polish and review | Loading, reduced motion, touch, credits, performance | Final pass |

**First implementation milestone (end of Phase 1):** the project runs locally and shows the approved
scene crop full-screen on a paper ground, flat and untouched, with the asset folders and the source
record in place. It proves the source quality and the framing before any effect is built.

## Approved decisions and adjustments (2026-10-02)

These override anything above that disagrees.

1. **Scene:** Rainbow Bridge / boat / willow. Crop fixed at master pixels x 18240–22040, y 24–1772
   (3,800 × 1,748, 2.17 : 1): wide enough for a visible left/right lean, no wider.
2. **Stack:** Vite, vanilla JS, DOM/CSS for gallery and overview, GSAP for transitions, Three.js only
   for the immersive scene. No React.
3. **Source:** the Wikimedia Commons Song-original file, verified against the Palace Museum reference
   and recorded in `assets/paintings/qingming/SOURCE.md`. No museum licence application for the prototype.
4. **Construction:** 3–5 broad layers; assisted segmentation allowed; **no generative inpainting**.
   Hidden edges: small camera movement, conservative bleed/extension from adjacent source pixels, and
   less parallax if gaps show. Preserving the artwork outranks camera range.
5. **Build order:** (1) source and crop, (2) scene composition, (3) seamless flat-to-depth transition,
   (4) parallax and limited viewpoint, (5) subtle motion, (6) polish. **No water shader or other motion
   until layered planes, depth separation, parallax and enter/exit are convincing on their own.**
6. **Transition:** perceptually seamless is the bar, not literally pixel-identical rendering.
7. **Interaction:** a restrained left/right shift, a small vertical response if useful, slight zoom.
   No free camera, rotation, walking, large pans or multiple hotspots.
8. **Gallery:** no five-painting gallery. 清明上河图 is the only real, selectable work. The page may
   hint at a future collection with optional abstract ink silhouettes as composition only; no named
   future works, no "coming soon" cards. It must feel complete with one painting.
9. **Folder:** renamed `3D painting` → `painting`.
10. **Repository:** the master and the lossless crop are git-ignored (re-downloadable / regenerable);
    web derivatives, `scene.json` and `SOURCE.md` are tracked.

## Direction change after the Milestone 1 review (2026-10-02)

These override everything above, including the approved list.

1. **No artwork page, no Enter button, no overview stop.** The journey is: gallery → click the
   painting itself → that same image expands, the gallery fades → it settles on the Rainbow Bridge →
   the flat painting eases into depth. One continuous move. Leaving reverses it.
2. **Gallery of about five paintings** in brushed openings on one sheet. Only 清明上河图 can be
   entered. The other four are real paintings (Cleveland Museum of Art, CC0), shown and credited on
   hover: Mi Youren *Cloudy Mountains*, Juran *Buddhist Retreat by Stream and Mountains*, Muqi
   *Dragon*, anonymous *Birds on a Peach Branch*. Any of them can be swapped.
3. **Crop reframed** so the bridge is the subject, a little right of centre: master x 17745–20845,
   y 24–1772 (3,100 × 1,748). The great willow at the far right is no longer in frame.
4. **Depth, as built:** three broad layers (everything / the bridge / foreground rooftops and
   willows), each with a smooth hand-authored depth map. Layers are flat grids nudged in screen space
   by depth; with separation 0 they sit exactly on the flat painting. Three.js draws them; there is
   no 3D geometry or perspective camera.
5. **Still deferred:** water, boat and willow motion; phone layout; sound.

## Second review (2026-10-02): 立体画卷 / painting diorama

Overrides points 2 and 4 of the section above.

- **Gallery:** five upright brush strokes side by side, alike in size and each different; the
  painting's name appears beneath its stroke on hover. No commentary text.
- **Scene = painting diorama.** The crop is cut into five cards, far to near: ground (far bank, river,
  street) · the bridge · the boat · the near bank (pavilion, parasols, moored boat) · foreground
  rooftops and willows. The cards stand at different distances along Z and a real perspective camera
  (22° lens) orbits them by up to 8° left/right and 4.5° up/down around the bridge, so near cards
  cross in front of far ones. Each point is placed so that from the resting camera it lands exactly
  where it is in the flat painting; with separation 0 the cards lie in one plane.
- Nothing is modelled: every card is the original picture's own pixels.

## Third review (2026-10-02): stronger diorama

- Same method (cut-out cards + orbiting perspective camera), pushed further.
- **Crop widened** to master x 17345–21245 (3,900 × 1,748). The extra scroll on each side is what the
  camera sees past the edges when it swings; the resting view is unchanged.
- **Six cards**, far to near: ground · barge under the arch · bridge · boat · near bank (with the
  wind-vane pole) · foreground rooftops. The bare willows are no longer lifted (twigs too fine to cut).
- **Cuts follow the painting:** each rough outline is snapped to the painted silhouette with GrabCut
  on an "ink density" image; holes are filled; cards run on a little under the cards in front.
- **Swing:** 13° left/right, 4° up/down; nearest and farthest slide about 13% of the view width
  against each other. (An over-strict edge check had been cutting the depth to about an eighth of
  what was intended; fixed.)

## Fourth review (2026-10-02): travel, more cards, fill allowed, life and sound

User: the diorama still felt flat and narrow; "really like being one in the painting". Agreed after
discussion: generated/cloned fill behind cut-outs is allowed; the viewer travels along the river;
water, small figure motion and ambient sound are welcome.

- **Travel, not tilt.** The camera now moves sideways past the cards (drag, wheel, arrow keys) and a
  little with the pointer; it no longer orbits. Parallax comes from passing things, as from a train
  window. Range about ±600 px of scroll at 1440 wide.
- **Six-thousand-pixel stretch** (master x 16545–22545): from the decorated gate 彩楼欢门 on the left
  to the great willow on the right. At rest the view is as wide as the window allows (no zoom-in).
- **Eight cards:** ground · barge · bridge · boat · near bank · things · gate · foreground. "Things" is
  found automatically from ink density (58 pieces: figures, stalls, parasols, small boats) and each
  piece stands upright on its own base; the willows lift only their ink.
- **Fill:** under the large cards, source pixels mirrored across the edge; under figures and twigs,
  the local bare-silk tone with the weave tiled from a patch of open water. No AI generation.
- **Depth cues:** far cards pale toward the silk, near cards a touch darker, nearest cards slightly
  soft (mip bias).
- **Life:** the river stirs within its painted lines (ground card only, masked); the boat rocks;
  single figures shift their weight by under a pixel. All off at rest, all off with reduced motion.
- **Sound:** a synthesised river (filtered noise with a slow swell), starts on entering, fades on
  leaving, toggle 水声 top right. No recording.

## Fifth review (2026-10-02): from diorama to discovery

The user set the 3D direction aside: "the strength of Qingming Shanghe Tu is how many tiny scenes of
everyday life are hidden throughout the scroll." The project is now an English-language discovery
experience. Overrides everything above about the scene.

- **Language:** all user-facing text in English; Chinese only as secondary artwork detail (titles
  under the strokes, 入画 beside the English mark, 出画 beside Leave).
- **Exploration canvas:** a 14,000 × 1,748 px stretch of the Song original (master x 11600–25600),
  from the town-edge shops past the Ten-Thousand-Cash tavern and the Rainbow Bridge to the moored
  grain boats. The bridge sits at about 60 % across the window at rest. Drag / wheel / arrow keys
  unroll it; ctrl-wheel or pinch zooms up to 1 master pixel per CSS pixel.
- **Drawn on a canvas,** only the visible part each frame. (A single scaled image layer reached
  16,000 px wide at full zoom and stopped painting on the GPU.)
- **Marks:** small cinnabar dots with a breathing ring; the title appears on hover; a row of dots at
  the bottom records which have been found.
- **Spotlight:** choosing a mark eases the view in (card takes the far side), the rest of the scroll
  darkens through a soft elliptical veil, the moment is redrawn from a full-resolution crop inside a
  soft edge, then the story card fades in. Click elsewhere, ×, or Esc eases back out but stays where
  the viewer was looking; "Next discovery" and ← → step through.
- **Stories (8 candidates, from the user's 10):** Close Call Under the Bridge · The
  Ten-Thousand-Cash Tavern · A Song-Dynasty Delivery Runner? · A Sweet Stall by the Bridge · The Bird
  on the Pole · Five Men and a Rope · Eight Men, One Oar · Seeing a Friend Off. Dropped: *The
  Impatient Child* and *Street Shaving* (not locatable with confidence in this stretch of the Song
  original), *The One-Coin Alms* (likewise), *Cooking on the Boat* (the usual example lies further
  upstream than the stretch; could be added by extending it). Added from the stretch itself: the
  towpath, the sweep oar, the farewell.
- **Removed:** Three.js, the river sound, the diorama cards. GSAP stays for the transitions.

## Sixth review (2026-10-02): refinements

- Gallery labels back to Chinese-first (入画 / 清明上河图), English secondary.
- The row of dots at the bottom of the scroll: larger, each shows a glimpse of its moment on hover,
  click jumps there. No "found" colouring. Row moved lower.
- Leaving is a quiet fade back to the gallery; the entrance is not replayed backwards.
- Rights line under the image credits: "Design, code and texts © 2026 Christus Luo. All rights
  reserved. Not to be copied or reused."
- The four companion paintings carry a small lock and "Not yet open" on hover.
- Five stories added from the stretch (13 total, ordered left to right along the scroll): The
  Donkey-Drawn Barrow · Right of Way on the Bridge · The Rudder at the Stern · A Table Over the River
  · Life Aboard. "The Tavern Lamps" was dropped: the 栀子灯 could not be located with confidence in
  the Song original.
- Follow-up: locks now sit on the painting itself (paper disc, thin lock); locked paintings do not
  react to hover at all. "Malt Sugar on Rainbow Bridge?" uses the user's text and is re-aimed at the
  canopy stall at the crest of the left ramp (master 19080–19360 × 140–330); "The Bird on the Pole"
  is narrowed to the pole itself. All thirteen boxes were checked against their texts.
- Seventh pass (2026-10-03): all thirteen boxes re-aimed and re-checked against their texts; zoom cap
  raised to 1.7× so small moments are shown larger; picture may be pulled further when a moment is near
  the top or bottom edge. "The One-Wheeled Cart" (was "Donkey-Drawn Barrow": the animal is not clearly a
  donkey). "Right of Way" now on the horse + sedan + servants at the top of the left ramp
  (19050–19380 × 150–320); "Malt Sugar" on the parasol stall at the crest (19390–19580 × 40–180).
  "Dinner Above the River?" and "A Home on the River?" use the user's texts. The red progress dot now
  marks the one being looked at (no persistent "found"). Lock: a single light-grey glyph on the painting.
- Stretch extended left to master x 7500 (now 18,100 px wide; web strips 9,000 / 4,500) to take in the
  road outside the city gate. "The One-Wheeled Cart" replaced by the user's "A Song-Dynasty “Taxi”?"
  (veiled rider and loaded chuanche, 7960–9060 × 1050–1320). Pole story re-aimed to the whole pole.
- Texts from the user for "Who Gets to Cross First?" (rider + sedan chair on the left ramp,
  18630–18960 × 270–580), "Malt Sugar on Rainbow Bridge?" (the vendor at his table by the rail,
  19210–19400 × 150–310) and "A Giant Oar at the Stern?" (was "The Rudder at the Stern").
- (Stretch briefly extended to x 5700 for the wrong compound; reverted to x 7500.) The relay station
  is the fenced compound outside the gate, 11330–11980 × 300–720. "Malt Sugar on Rainbow Bridge?" removed; "Waiting for the Next
  Dispatch?" (relay station, 5880–6760 × 1230–1760) added. Spotlights may now be rotated and sized
  per story (`spot: { angle, rx, ry }`); "Who Gets to Cross First?" uses a diagonal one along the ramp
  from the sedan chair up to the rider (18620–19250 × 160–590, −31°).
