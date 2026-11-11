# Spring Dawn in the Han Palace: Qiu Ying, Ming dynasty

National Palace Museum, Taipei, 故畫001038. Handscroll, ink and colour on silk, 30.6 × 574.1 cm.
Catalogue: https://digitalarchive.npm.gov.tw/Collection/Detail?dep=P&id=3672

Master: `master/Spring_Morning_in_the_Han_Palace.jpg` (git-ignored; re-download from the URL below)
https://upload.wikimedia.org/wikipedia/commons/c/c3/Spring_Morning_in_the_Han_Palace.jpg
52,680 × 2,683 px, 280,723,350 bytes. SHA-256 `556575e5ec4326bdd03efa6c7cb1545845c6511ff2333826605c5c475f33c07a`.
Commons marks it public domain (credit "scanned by Krause, Johansen"); it is not a museum download.

`.venv/bin/python scripts/prep-han.py` verifies the master and derives everything in `web/`, `tiles/`, `details/`, `thumbs/` and `scene.json`.
The master is a profile-less CMYK scan of a print, so the script converts it to sRGB and applies one global colour
correction fitted to the museum's own preview photographs (`color-fit.json`). Otherwise: cropping, downsampling and WebP only.

Hotspots, evidence and texts: `research/han-palace-proposal/` (start with `REVIEW_SUMMARY.md`).
Story anchors: `src/paintings/han-palace/anchors.json`. Replaces Cloudy Mountains in the gallery; that record is kept in `archivedPaintings`.
