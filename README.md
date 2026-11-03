# Into the Painting

> "Look closely — there is a whole life happening inside this painting."

**Current release:** two enterable paintings: *Along the River During the Qingming Festival*
(13 discoveries) and *Prosperous Suzhou / 姑苏繁华图* (22 discoveries).

[Open the live experience](https://xinl123.github.io/Into-the-Painting/).
Gallery music starts paused and has direct previous/play-pause/next controls. Scene sound is independent;
background music pauses inside a painting. Sources and recording licences are in About and the asset source notes.

```bash
npm install
npm run dev        # http://localhost:4180
```

Re-deriving assets from the masters (only needed after changing the stretch or a story box):

```bash
python3 -m venv .venv && .venv/bin/pip install pillow numpy opencv-python-headless
npm run assets
```

## What this is

An English-language interactive discovery experience about the small, surprising stories hidden in
traditional Chinese paintings. The pilot is *Along the River During the Qingming Festival* (清明上河图,
Zhang Zeduan, Northern Song, Palace Museum, Beijing).

```
 gallery of five paintings  →  click the painting  →  a broad stretch of the scroll unrolls
      →  a few quiet red marks  →  choose one  →  the scroll falls back, one moment comes forward
      →  a short "Did you know?" story  →  next discovery, or back to the scroll
```

## Core principles

1. **The painting is the centre.** At rest the viewer is looking at the original scroll, nothing else.
2. **Specific, not general.** Each story is one person, one shop, one object or one action; never
   "Song commerce".
3. **Spotlight, not tooltip.** Choosing a mark is a cinematic move: the rest recedes, the moment is
   shown at full resolution, the text arrives last.
4. **Short and careful.** A title, a hook, two to four sentences; disputed readings are phrased as
   readings.
5. **Interface made of the same stuff as the art.** Paper, ink, brushed openings, negative space.

## What was tried and set aside

Three earlier rounds built a 2.5D / diorama version of the bridge (cut-out cards at real depths with a
moving camera). It worked technically but never felt like being inside the painting, and it fought the
scroll's bird's-eye projection. The pipeline is kept in `scripts/archive/` for reference; see
PROJECT_PLAN.md for the history.

## Companion paintings

Three companion works appear in the gallery (not yet enterable), all from the Cleveland Museum of Art's
open-access collection (CC0). Each has a `SOURCE.md` under `assets/paintings/<id>/`.

## Documents

| File | Purpose |
|---|---|
| [PROJECT_PLAN.md](PROJECT_PLAN.md) | MVP scope, journey, interaction, transitions, architecture, tech comparison, risks, phases |
| [SCENE_SELECTION.md](SCENE_SELECTION.md) | Candidate scenes from the scroll and the recommendation |
| [ASSET_PLAN.md](ASSET_PLAN.md) | Image source research, licensing, what assets are needed and how they are made |
| [VISUAL_DIRECTION.md](VISUAL_DIRECTION.md) | Gallery/homepage look, reading of the reference, typography, brush and paper language |
| [TASKS.md](TASKS.md) | Phased task list |
| [assets/paintings/qingming/SOURCE.md](assets/paintings/qingming/SOURCE.md) | Source record, provenance, verification against the museum reference |
