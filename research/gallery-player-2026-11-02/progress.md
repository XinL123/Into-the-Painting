Completed locally.
- Existing three streaming tracks selectable by their supplied source labels: 琵琶语, 双面燕询, 苏州听雨. Previous/next wrap; paused skipping stays paused; selection starts the selected song; resume retains time.
- Volume preference survives track/project transitions. Autoplay refusal remains distinguishable from manual pause. Stale play rejections cannot mark the current track blocked.
- Paper popover closes on outside press/Escape and on project entry. Escape restores opener focus. Gallery music stays paused inside both paintings; independent project sound remains enabled unless explicitly muted.
-28 browser checks passed, including1280/390/320px fit, real audio, selection, volume, quick skipping, pause/continue, both paintings, and manual pause retention. Manual keyboard Tab/Left updated actual volume100 to99; Escape closed correctly. Desktop1280x720 and mobile390x844 screenshots inspected.
-21 Node audio, playlist, artwork/order/cache/framing and lifecycle checks passed. Build746ms;git diff --check clean. Artwork, stories, master coordinates and audio recordings untouched.
- Resolved during implementation: a placeholder paper texture path did not exist; replaced before browser testing with the existing page's exact SVG paper texture.
