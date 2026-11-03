# Default-on sound — corrected refresh semantics
Both localhost:4173 and127.0.0.1:4173 processes serve /Users/Xin.L/Desktop/portfolio (verified process cwd).
Gallery music and scene effects ignore legacy localStorage mute records. Every full page load starts enabled. Explicit mute is held only in memory during the current page visit; scene-controller changes preserve it, full refresh clears it. Browser autoplay rejection preserves enabled intent and retries on a gesture.

Four regression tests passed: autoplay retry, stale persisted-off ignored after refresh, pending play cannot escape mute/suspension, scene mute retained during this visit but reset after fresh module load. Build and git diff --check passed.

Direct browser verification at http://localhost:4173/playground/painting/: Music on initially; manual click produced Music off; full reload produced Music on. Entered Gusu and confirmed Sound on. Screenshot /tmp/painting-sound-refresh-on.jpg. No art, text, hotspot or audio asset edits. Local only, not published.
