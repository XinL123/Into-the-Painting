# Implementation and verification — 2026-10-27

Completed locally after the user's approval of all thirteen anchors and both reserve replacements. No commit, push, deployment or publication.

## Delivered

- Prosperous Suzhou occupies the approved left-adjacent frame. Its actual same-master gallery image expands continuously into the shared exploration canvas. Juran's original metadata, brush, image, object positioning and frame configuration remain intact in `archivedPaintings`; original assets were not removed.
- Both paintings use the same layout, markers, card typography, Next/progress navigation, sound controls and entrance/exit animation. Only the selected painting creates an exploration controller; leaving destroys its input listeners, image requests, cache references, tweens and AudioContext. Existing Qingming deep links still default to Qingming.
- Thirteen exact approved anchors in right-to-left order. Native boxes are unchanged; camera composition adapts to viewport, card area and scan edges. Tea room and pagoda remain within the image's available pixels. Phone/tablet widths up to 800px use the same card below the scene; long cards scroll internally.
- English copy is 40–47 words per story. School and textile identification are research-based; wedding and garden identity are explicitly qualified. No exact sign transcription is required from unreadable scan letters. Historical and image references remain in STORY_RESEARCH.md / FINAL_COPY.md and About Sources.
- Eight overlapping native-resolution horizontal tiles (maximum width 4,532px), a small overview, one same-master entrance segment, lazy detail crops and tiny hover thumbnails. Up to four native tile images and three detail images are retained by the controller; at most two requests per cache. Offscreen/stale requests are cancelled. Only one adjacent native segment is prefetched, after visible segments arrive. Gusu's full 35k master never becomes a browser image/texture.
- Gusu native-pixel zoom capped at 1.25×; all production derivatives only crop/downsample/encode. Original scan seams remain. No sharpening/repainting/reconstruction.
- Subtle bird and water ambience from existing CC0 recordings; no invented period dialogue or music. Vorbis with compact PCM WAV fallback, because the OS AAC encoder is unavailable. Existing Qingming AAC/Vorbis files are unchanged.
- Image failures preserve available fallback/detail pixels and navigation; Retry reattempts failed assets. An offscreen prefetch failure does not show an irrelevant warning.

## Verification

- Build: `npm run build --prefix playground/painting` passes. `git diff --check` passes.
- `qa/core.test.mjs`: five tests pass: exact anchors/order/copy length; scene containment and zoom limit across seven viewports; bounded asynchronous cache; cancellation/failure/retry/disposal; pending sound cancellation.
- `qa/interaction-results.json`: 46 checks pass in the real local app. Covers both galleries entering/leaving, thirteen cards for each painting, Next wrap, arrow navigation, Escape, mute persistence, ambient playback, controller/audio teardown, no duplicate markers, About content and reduced-motion branch.
- Touch pan/pinch exercised with synthetic PointerEvents in the actual 390px-wide app iframe, including controller state checks. Mouse/keyboard/progress navigation also exercised through the browser. This is not physical-phone hardware verification.
- Live card/framing inspection: all thirteen Gusu cards on desktop (1440×900) and phone (390×844). Geometric safety tests also cover 805×745, 768×1024, 640×480, 320×568 and 844×390. Native sharpness and the two edge scenes inspected visually.
- Local production-build delivery server: intentional initial HTTP 503 overview/tile failures; cards remained usable, Retry recovered, selected story persisted. Delayed overview/native responses by 1,800ms; normal entrance completed in approximately 2,570ms, with thirteen navigation points and sound control available before all native segments arrived. The server logs show only relevant Gusu segments and the gallery's medium Qingming preview, not both paintings' complete high-resolution assets.
- `qa/preservation-and-assets.json`: all 87 protected original Qingming image/audio/story files retain their research-baseline SHA256. Original Juran record is preserved verbatim.
- Console on ordinary desktop/mobile/delayed-delivery passes: no runtime errors. Deliberate failed-image responses are expected during failure QA. Browser background animation/locator timing required a settled-state recheck; final rendered cards were verified.

## Evidence

- `qa/screenshots/gallery-desktop.jpg`
- `qa/screenshots/gusu-garden-desktop.jpg`
- `qa/screenshots/gusu-pagoda-desktop.jpg`
- `qa/screenshots/gusu-tea-mobile.jpg`
- `qa/screenshots/gusu-pagoda-mobile.jpg`
- `qa/screenshots/qingming-regression-desktop.jpg`
- `qa/desktop-cards.json`, `qa/mobile-cards.json`, `qa/failure-retry.json`, `qa/slow-delivery.json`

## Remaining limits

The master is only 1,010px tall. Small inscriptions cannot become clearer through zoom; separate detail reproductions were research references and were never substituted. Continuous full-scroll travel is longer than the Qingming cropped scene; the existing discovery dots provide direct access. Physical iOS/Android hardware and a separate Safari engine were not available in this run. All edits stay in this checkout, served by the existing localhost servers.
