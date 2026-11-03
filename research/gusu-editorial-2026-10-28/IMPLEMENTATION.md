# Gusu editorial and UX refinement · 2026-10-28

Applied03–22 from supplied review;04/05/07/08/09/15/18/21 use the pasted text verbatim. Removed06’s unknown-couple ending in accordance with the request to avoid unknowable-detail disclaimers.01–02 unchanged (serialized pre-change data comparison).

-18: corrected to more than200 signs across the whole scroll, with People’s Daily Overseas Edition2026-08-28 citation. About Sources updated too. No260 recent museum recount claim remains in runtime copy.
-16: retained museum-supplied close-up attribution; added Huangshan government source forSongluo green tea.
-13 camera focus narrowed to[16340,0,16840,330];15 to[12900,600,13670,1010]. Existing native1.25zoom cap kept. Original22scene boxes/marker anchors unchanged; no image processing or asset changes.
-Floating navigation thumbnails hidden while Gusu story cards are open; keyboard preview becomes visible again after closing a card.
-22 button saysRestart the Journey and retains actual wrap-to01 behavior. Other cards and Qingming retainNext discovery.
-New cards reset scrollTop so previous reading position cannot hide the next title.

## Validation

5core tests passed, including exact latest copy,01–02 preservation,22anchor fidelity,7viewport safe framing, bounded image requests/failure retry, and audio cancellation.

58 live iframe interaction checks passed, including22Gusu cards,13Qingming cards,final restart,reading thumbnail suppression,card scroll reset,Next/arrow wrap,touch pan/pinch,mute/audio cleanup,About and reduced motion.

All20 revised cards captured and checked at1440×900 and390×844 (40cases);06 was recaptured after trimming its ending. Card/navigation bounds fit and focused markers did not intersect cards.07 was scrolled with native input andNext reached08. At320×568,07/09/16/22 retained visible navigation and scrollable in-bounds cards. Desktop and phone13/15 screenshots visually confirm improved subject visibility. No preview browser console errors.

170protected artwork/audio/source files andQingming data unchanged by SHA-256. All22original scene boxes/marker anchors preserved. Build andgit diff --check passed. Screenshots use reduced motion for repeatability; actual motion code/timing retained.

Local only; no commit,push or deployment. Native master still limits fine lettering and tiny figures. Physical device testing was not performed.

Evidence:qa/interaction-results.json,qa/visual-checks.json,qa/narrow-checks.json,qa/screenshots/.
