# Asset plan

No artwork has been added to the project. This document lists the source options for your approval
and the minimum set of assets the MVP needs.

## 1. Source research — 清明上河图

There are several historical paintings with this title. They are different artworks. The pilot uses
**only the Northern Song original by Zhang Zeduan**; nothing from another version is ever combined
with it.

### Option 1 — Song original, Wikimedia Commons full scroll (recommended for the pilot)

| | |
|---|---|
| Artwork / version | 清明上河图, the Song original |
| Artist | Zhang Zeduan 张择端 |
| Date | Northern Song, early 12th century |
| Collection | Palace Museum, Beijing (24.8 × 528 cm, ink and light colour on silk) |
| File | `Alongtheriver QingMing.jpg`, **38,414 × 1,800 px**, 18.9 MB |
| URL | https://commons.wikimedia.org/wiki/File:Alongtheriver_QingMing.jpg |
| Licence | Public domain (faithful reproduction of a 2D public-domain work, PD-Art). The same image cut into four 7,683 × 1,800 sections is tagged CC0. |
| Provenance | Uploaded 2014; credited to Baidu Tieba, **not** directly to the museum. Aspect ratio (21.3 : 1) matches the Song scroll's dimensions, and the content matches the Palace Museum's description. |
| Quality for a scene crop | The scene crop would be about 4,000 × 1,800 px. Sharp enough for a full-screen scene on a 1080p–1440p display with a slight zoom; at 4K the silk weave and JPEG softness become visible. **Sufficient for the pilot.** |

Caveat: the painting itself is unquestionably public domain, but this file's chain of custody is not
museum-backed. I would check its colour and detail against the Palace Museum's own viewer before use.

### Option 2 — Palace Museum, Beijing, official digital images (most authoritative; needs permission)

| | |
|---|---|
| Artwork / version | Same Song original |
| Pages | Collection page: https://www.dpm.org.cn/collection/paint/228226.html · deep-zoom viewers: 故宫名画记 https://minghuaji.dpm.org.cn and 数字文物库 https://digicol.dpm.org.cn |
| Resolution | Deep-zoom, far higher than Option 1 (exact pixel size not published; not verified by me for this specific scroll) |
| Licence | "版权所有：故宫博物院". The site states that downloading or using high-resolution images requires contacting the museum; there is an image-licensing application (影像授权). No open licence, no IIIF. |
| Quality | Best available anywhere |

Use: as the visual reference for checking Option 1, and as the route to a properly licensed master
if the project later becomes public-facing or commercial. I will not scrape the viewer tiles.

### Option 3 — `清明上河图卷.png` on Commons (reject: wrong painting)

21,844 × 1,109 px, sourced from 故宫名画记. Its source page describes an **anonymous Ming-dynasty**
清明上河图卷 (35.5 × 658.7 cm), not Zhang Zeduan's scroll. It is listed here because its file name
makes it easy to mistake for the original. This is exactly the version mix-up to avoid.

### Option 4 — Qing Court version, National Palace Museum, Taipei (different painting, cleanest licence)

| | |
|---|---|
| Artwork / version | 清院本清明上河圖 |
| Artists | Chen Mei, Sun Hu, Jin Kun, Dai Hong, Cheng Zhidao (Qing court painters) |
| Date | Completed 1736–37 |
| Collection | National Palace Museum, Taipei (35.6 × 1,152.8 cm, colour on silk) |
| Sources | NPM Open Data https://digitalarchive.npm.gov.tw/opendata (about 6 MP images under CC BY 4.0, about 1 MP under CC0) · Commons stitch `Along the River During the Qingming Festival (Qing Court Version).jpg`, 56,531 × 1,700 px, 102 MB, public domain |
| Quality | Good; brightly coloured and crisp |

Museum-backed and openly licensed, but it is an 18th-century reinterpretation with a different
composition, palette and mood. Choose it only if you would rather have an impeccable licence than
the Song original. It would be a different project visually.

### Recommendation

Use **Option 1** as the pilot master, verified by eye against **Option 2**. Credit line in the
experience: "张择端《清明上河图》, 北宋, 故宫博物院藏 / Zhang Zeduan, Northern Song, Palace Museum, Beijing.
Image: Wikimedia Commons, public domain." If the piece goes on your public portfolio and you want
zero ambiguity, apply for the Palace Museum image licence in parallel.

## 2. Assets the MVP needs

Ordered from source to screen. "Made by" says who produces it; almost nothing requires manual work
from you.

| # | Asset | What it is | Made by |
|---|---|---|---|
| 1 | **Master** | The approved full-scroll file, untouched | Downloaded once after approval |
| 2 | **Overview strip** | Whole scroll downscaled (about 8,000 px wide, plus a small one for mobile) for the overview screen | Script |
| 3 | **Scene crop** | The chosen section at full source resolution, about 4,000 × 1,800 px, no retouching | Script (crop rectangle recorded in the manifest) |
| 4 | **Layer masks** (5) | Greyscale mask per broad layer: far bank, river+boat, bridge+street, rooftops, willow | First pass by me (assisted segmentation plus hand-drawn polygons), you review the edges; refine in an image editor only where needed |
| 5 | **Layer images** (5) | Scene crop × mask, with the hidden area behind each front layer filled | Script, with fills as described below |
| 6 | **Depth gradients** | One simple hand-authored greyscale gradient per layer that needs to tilt (mainly the bridge and the river plane) | Me, hand-authored; not an AI depth estimate |
| 7 | **Motion masks** (2–3) | Where water shimmer applies; which willow twigs sway and how much; the boat cut-out | Derived from the layer masks |
| 8 | **Paper texture** | Tileable warm paper/silk grain for page backgrounds | Generated procedurally or taken from the scroll's own blank margins |
| 9 | **Brush masks** | 5–6 dry-brush silhouettes for the gallery, as SVG or greyscale PNG | Drawn by me in code/SVG; replace with your own brushed scans later if you want a more hand-made edge |
| 10 | **Fonts** | One Chinese serif, one Latin serif (open licences) | Web fonts |

### Things deliberately not needed

- No per-person or per-object cut-outs (the crowd stays baked into the bridge layer).
- No 3D models, no normal maps.
- No AI-generated depth map as the basis for depth. Monocular depth models are trained on photographs
  with real perspective; on a scroll with shifting oblique projection they give unreliable results.
  Depth here is simple and legible: lower in the frame is nearer. A hand-drawn gradient says that
  better.
- No upscaling or "enhancement" of the artwork.

### Filling what parallax reveals

When a front layer shifts, a sliver of the layer behind it is exposed. Policy, in order:

1. Keep parallax small enough that slivers are a few pixels wide.
2. Fill hidden areas by extending the surrounding silk/water tone (edge dilation and blur), which is
   honest because those areas are plain ground in the painting anyway.
3. Only if a larger area must be filled (behind the bridge arch), clone nearby water texture by hand.
4. Generative inpainting is **not** used unless you approve it. It would be inventing painting.

## 3. Folder layout (after approval)

Master, processed crop and derived assets stay separate, as requested.

```
assets/
  paintings/
    qingming/
      master/            original file, never edited      (large; see decision on git below)
      SOURCE.md          version, artist, museum, URL, licence, download date, checksum
      overview/          downscaled strips
      scene-hongqiao/
        crop/            scene crop, unretouched, lossless
        web/             browser derivatives of the crop
        scene.json       crop rectangle, sizes, master checksum
        masks/           layer masks + motion masks
        layers/          derived layer images (web formats)
        depth/           per-layer depth gradients
  ui/
    paper/               paper texture
    brush/               gallery brush masks
scripts/                 asset-prep scripts (crop, downscale, cut layers, export)
```

Every derived file can be regenerated from `master/` plus `masks/` by script, so only masks are
"hand-made" assets.

## 4. Preparation workflow

```
 master ──crop──▶ scene crop ──masks──▶ layer cut-outs ──fill hidden edges──▶ layer images
                       │                                                          │
                       └──▶ overview strip                    depth gradients ────┤
                                                              motion masks ───────┴──▶ scene manifest
```

Web delivery: layers as WebP/AVIF with alpha, each at most 4,096 px wide (the safe GPU texture limit
on phones), plus half-size versions for small screens. Estimated total scene payload: 3–6 MB.

## 5. What I need from you

1. Approval of the image source (Option 1, or another).
2. Approval of the scene (see [SCENE_SELECTION.md](SCENE_SELECTION.md)).
3. A yes/no on assisted segmentation for the *first pass* of masks (it only finds edges; it does not
   alter the artwork).
4. Later, a review pass on mask edges and on motion strength. No asset preparation is required from
   you unless you want to hand-brush the gallery masks yourself.
