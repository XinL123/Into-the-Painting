# Progress
Documents and code read. Museum catalog and scholarly article opened. No production edits.

Completed source and local browser review, all-strip inspection, targeted reference matching, 13-anchor register, two explicit reserve substitutions, map/contact-sheet visual QA, and future plans. Verified existing files against captured SHA256 baseline; see verification.json. No production build required because no production files changed.

Implementation authorized. Existing working source copied into implementation-baseline before edits; original proposal and approved coordinate register retained. Primary architecture issue: exactly one live reference plus eagerly created controller; will create only the selected controller and dispose it after leave. Gusu entrance will use a same-master segment rather than a 35k-wide DOM image.

Asset generation complete: 8 native horizontal tiles, 13 exact-master detail crops and tiny thumbnails, preview/entrance segment. First audio conversion required the macOS four-character AAC code (`aac `); fixed. Node standalone story check requires JSON import attribute; added standard attribute.

AAC codec is unavailable in this environment (afconvert lists no m4af encoder). Gusu ships Vorbis plus compact PCM WAV fallback instead; Qingming AAC/Vorbis bytes remain unchanged. New audio selector will choose a supported format that actually exists for each clip. All 13 final cards are 40–47 words.

First desktop live pass: all 13 titles/counts/order and camera side positions verified, no console warnings/errors. Edge framing checked mathematically at 1440x900, 805x745, 390x844, 320x568 and short landscape. Bounded cache tests cover concurrency, cancellation, failure/retry and disposal. Browser QA continues for mobile/entrance/audio/failed delivery.

Mobile live pass verified all 13 cards at 390x844; both edge scenes remain readable, and progress dots fit. Interaction fixture caught keyboard events targeting Window rather than Element; guarded closest() accordingly, then rerunning fixture. Synthetic touch pan/pinch and reduced-motion breathing checks already passed.

Interaction rerun passed touch/keyboard/13+13 cards/sound mute/ambient/first controller cleanup. QA state serialization exposed GSAP internal circular cache via object spread; restricted diagnostic transform to x/y/s. Keeping Qingming as the explicit default for old deep links. Gusu entry never waits for complete image assets, including cold entry.

Local delivery QA server initially hit sandbox bind restriction; successfully started with reviewed localhost-only permission. All interaction fixture checks now pass. Real production-build image failure pass: 13 controls/card remain usable, explicit Retry recovers; refining failure notice so failed offscreen prefetch does not warn about an otherwise readable scene.

Final: 46 real-app interaction checks and five core tests pass. Failure/retry and 1800ms-delayed production image delivery verified; selected cards and controls stay usable. Protected 87 Qingming source/assets unchanged; Juran original record preserved. Screenshots captured. See IMPLEMENTATION.md for exact evidence and physical-device/browser-engine limits. Temporary QA server stopped after testing; original servers untouched.

2026-10-27 cover adjustment: user identified the vertical green reproduction seam in the gallery. Inspected same-master vertical crops centered at 24500/25200/25500. Chose x24500 (350px left of the prior x24850), showing garden roofs, trees and a moon gate; native seam remains unedited. Only entry focus changed, preserving the continuous entrance. Hotspot coordinates/content unchanged.

2026-10-27: user chose the brighter apricot #E7B93E and approved uniform use. Applied to all thirteen Gusu markers, their breathing rings, and selected progress dots. Preserved 12px markers and ivory outlines. Qingming and card accents remain unchanged.
