# Tasks

Small, incremental, each ending in something that can be looked at. Work stops for review at the end
of each milestone. Build order follows the approved priorities in
[PROJECT_PLAN.md](PROJECT_PLAN.md#approved-decisions-and-adjustments-2026-10-02): source and crop →
composition → flat-to-depth transition → parallax → subtle motion → polish.

## Phase 0 — Understanding and research (done)

- [x] Inspect the project folder (empty)
- [x] Research image sources and licensing for 清明上河图; separate the versions
- [x] Inspect the Song scroll section by section; shortlist scenes
- [x] Write README, PROJECT_PLAN, ASSET_PLAN, VISUAL_DIRECTION, SCENE_SELECTION, TASKS
- [x] **Approved:** image source, scene, stack, mask approach, gallery scope, folder rename

## Phase 1 — Structure and static viewer = Milestone 1 (done, awaiting review)

- [x] Rename folder `3D painting` → `painting`
- [x] Download the approved master into `assets/paintings/qingming/master/`; write `SOURCE.md`
- [x] Compare against the Palace Museum reference image (version, completeness, colour, detail)
- [x] Project skeleton (Vite, vanilla JS) and asset folder layout
- [x] `scripts/prep-qingming.py`: scene crop at full resolution, web derivatives, `scene.json`
- [x] Overview strips (8,000 and 4,000 px wide) derived, not yet shown
- [x] Static page: scene crop on a paper ground, flat, with caption and credit
- [x] Review aid: whole / scene-height / 1:1 views with a pixel readout
- [ ] **Review with you:** framing of the crop (bridge to willow), sharpness on your display

## Core experience (replaces the old Phases 2–4 after the Milestone 1 review) — done, awaiting review

- [x] Reframe the crop: bridge as subject, slightly right of centre (3,100 × 1,748)
- [x] Source four companion paintings (Cleveland Museum of Art, CC0) with source records
- [x] Generated dry-brush masks; gallery sheet with five brushed openings; hover caption
- [x] Click the painting itself: the opening expands with its brushed edge, the gallery fades
- [x] Hand-traced outlines → three layers (base, bridge, foreground) with mirrored-edge fill
- [x] Layered scene in Three.js; flat-to-depth "awaken"; pointer lean, slight wheel zoom, slow idle sway
- [x] Leave (Esc or 出画) reverses the whole move
- [x] Removed the review page and its whole / scene-height / 1:1 controls
- [ ] **Review with you:** gallery feel, the entering move, framing, strength of depth

Known gaps, left on purpose until the above feels right:

- [ ] Phone / portrait layout of the gallery (the sheet simply scales down for now)
- [ ] Brush masks are generated; hand-brushed scans would look more made-by-hand
- [ ] The boat in the river is part of the base layer (no separate depth)
- [ ] Web fonts (system Songti / serif for now)

## Diorama rounds (2026-10-02) — built, then set aside after review

- [x] Rounds 2–4: cut-out cards, snapped silhouettes, travelling camera, fills, water, sound
- [x] Review: did not feel like being in the painting; direction changed (pipeline archived)

## Discovery experience (2026-10-02) — built, awaiting review

- [x] English-language rewrite of gallery, labels, captions, controls
- [x] 14,000 px stretch of the Song original as the exploration canvas (drag / wheel / keys / zoom)
- [x] Canvas renderer drawing only the visible region (GPU-safe at full zoom)
- [x] Eight stories located in the Song original, with full-resolution detail crops
- [x] Marks, spotlight veil, detail reveal, story card, found-dots, next / previous
- [x] Enter from the gallery by clicking the painting; leave returns the view to rest first
- [x] Sixth-review refinements: Chinese-first gallery, thumbnail dots, quiet exit, rights line, locks, +5 stories (13)
- [x] Seventh–ninth passes: boxes verified one by one, user-supplied texts, relay/taxi/cross-first/poles re-aimed, lock glyph, red = current dot
- [ ] **Review with you:** the 13 stories, the spotlight feel, the English copy

Known gaps, left on purpose until the above feels right:

- [ ] Phone / portrait layout (gallery scales; the scroll works but the card is desktop-shaped)
- [ ] Story texts are first drafts; sources should be checked and cited in a STORIES.md
- [ ] No ambient sound (removed with the diorama; can return if wanted)
- [ ] Brush masks are generated; hand-brushed scans would look more made-by-hand

## Phase 6 — Polish and review

- [ ] Loading: low-res first, then full textures; no layout jump
- [ ] Reduced-motion mode; keyboard access; focus states
- [ ] Touch: drag and pinch; half-size textures on small screens
- [ ] Performance pass: render on demand, texture sizes, memory
- [ ] Credits and source line; licence note
- [ ] Cross-browser check (Safari, Chrome, Firefox)
- [ ] Notes for painting two: what the pipeline needed, what should be shared
- [ ] **Final review with you**

## Later (not in the pilot)

- Second painting of a contrasting type
- Licensed museum-grade master for 清明上河图
- Sound, captions/annotations, gyroscope on mobile
- Linking from the portfolio playground
