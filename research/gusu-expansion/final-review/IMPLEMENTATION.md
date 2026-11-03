# Approved expansion — local implementation

User approved the final review. Gusu now has22 discoveries: all original13 plus A,B,C,D,F,G,E2,H,J. E and I are excluded.

- Approved English preserved verbatim, split at the first sentence into the existing lead/body layout. Original13 copy stays keyed by stable IDs, preserving its wording when route order expands.
- Exact approved scene boxes drive the existing camera; independently approved anchor coordinates position the nine new markers. Original markers retain box-center behavior.
- Same-master detail crops/thumbs added; existing8 tiles, preview, entrance and original13 detail crops unchanged. Existing tile/detail cache limits and lazy loading retained.
- Same apricot #E7B93E marker treatment. At<=1000px22 navigation dots form two11-dot rows. Mobile cards sit above that row, and camera framing accounts for its height. Qingming retains its13-dot navigation and original styling.
- Existing modern CC0 water/bird clips reused for suitable new scenes; no historical sound claim. Silent stories still stop previous clips. About adds evidence sources without rewriting Why or Rights.

## Verification

-5 core tests passed: approval-to-data fidelity, safe frames across7 viewport geometries, bounded async image cache, failure/retry/cancellation, stale audio cancellation.
-55 live-app checks passed in the real local app iframe:22 Gusu cards,13 Qingming cards,Next/arrow wrap,touch pan/pinch,wheel zoom,mute persistence,audio and request cleanup,About and reduced motion.
-9 new scenes captured at1440×900 and390×844; markers and cards do not intersect; all22 navigation controls stay within viewport. Additional320×568,844×390,805×745 and768×1024 checks confirmed navigation/card bounds and scrolling of long cards.
- Browser preview reported no console errors. Normal-motion entry/card transition checked separately in the user's original local tab. Preview screenshots use reduced motion for repeatable framing.
- 57 existing Qingming/Gusu image-source files verified byte-identical against the start-of-implementation baseline. Exact source master unchanged. No original anchor box moved.
- Production build and diff whitespace check passed.

## Limits

Native master remains1010px tall. Ruiguang tower and subtle Stone Lake banks remain small on phones; no reconstruction or artificial enlargement. Synthetic touch events and browser viewport overrides do not replace physical-device testing. Browser failure/slow-network simulation was not repeated for this data expansion; bounded loading/failure handling passed core tests and existing recovery behavior is retained.

Local only. No commit, push, deployment or publication.

Screenshots: `qa/screenshots/`; runtime evidence: `qa/interaction-results.json`, `visual-checks.json`, `narrow-checks.json`.
