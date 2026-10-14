# Source record — 清明上河图 (Song original)

## Artwork

| | |
|---|---|
| Title | 清明上河图 / *Along the River During the Qingming Festival* |
| Version | The Northern Song original. Not the Ming copies, not the Qing Court version (Taipei). |
| Artist | Zhang Zeduan 张择端 |
| Date | Northern Song, early 12th century |
| Medium | Handscroll, ink and light colour on silk, 24.8 × 528 cm |
| Collection | Palace Museum, Beijing (故宫博物院) |
| Museum record | https://www.dpm.org.cn/collection/paint/228226.html |

## Master file

| | |
|---|---|
| File | `master/Alongtheriver_QingMing.jpg` (kept out of git; re-download from the URL below) |
| Size | 38,414 × 1,800 px, 19,320,386 bytes |
| SHA-256 | `ad9ccd836874141c985c8db89589d7f6960719eda8281966646eb41a6ed02950` |
| File page | https://commons.wikimedia.org/wiki/File:Alongtheriver_QingMing.jpg |
| Direct URL | https://upload.wikimedia.org/wikipedia/commons/8/86/Alongtheriver_QingMing.jpg |
| Downloaded | 2026-10-02 |
| Licence | Public domain (Commons tag PD-Art: faithful reproduction of a two-dimensional public-domain work) |
| State | Untouched. Never edited; everything else is derived from it by `scripts/prep-qingming.py`. |

## Provenance and its limits

- The Commons file was uploaded in 2014 and credits **Baidu Tieba** as its source. It was not issued
  by the Palace Museum, and who made the photograph/stitch is not recorded.
- The painting is public domain. The Palace Museum's own high-resolution images are
  "版权所有：故宫博物院" and require permission; they are **not** used in this project. No licence
  application is being pursued for the prototype.
- Do not confuse with `File:清明上河图卷.png` on Commons, which is an anonymous **Ming** copy.

## Verification against the Palace Museum reference (2026-10-02)

Reference: the detail image published on the museum's record page for this scroll
(`img.dpm.org.cn/Uploads/Picture/2017/05/12/s591529137db2e.jpg`, 1,258 × 500 px), viewed in the
browser only, not saved. By coincidence it shows almost exactly our scene: bridge, boat, rooftops,
great willow.

| Check | Result |
|---|---|
| Same painting / version | Yes. Wooden arch bridge, boat with mast being lowered, wind-vane pole at the bridge foot, parasols, figure standing on the boat roof below the bridge, great willow: all match in position and drawing. |
| Completeness | The master is the full height of the painted silk, with the mount border visible at top (about 22 px) and bottom (about 24 px). The museum detail is trimmed tighter top and bottom. |
| Aspect ratio | Master 21.3 : 1 matches the scroll's 528 / 24.8 = 21.3. |
| Geometry | No visible stitch seams, duplicated or missing passages within the scene area. |
| Colour | Close but not identical. Mean RGB of the museum detail is (127, 99, 71); the same area of the master is (131, 106, 78). The master is slightly lighter and a little less warm/saturated. |
| Detail | Master resolves individual brush lines, faces and the silk weave at 1:1. Light JPEG softness, no blocking visible at normal viewing size. |

Decision: the master is used **without colour correction**. The difference from the museum image is
small, and which of the two is closer to the object is unknown, so matching one photograph to the
other would be an unfounded alteration. Revisit only if a museum-issued master is ever obtained.

## Derived files

Produced by `npm run assets` (`scripts/prep-explore.py`). Crop and resample only; no colour,
contrast or sharpening changes.

| File | What |
|---|---|
| `stretch/web/qingming-stretch-9000.webp`, `-4500.webp` | The exploration stretch, master x 7500–25600, y 24–1772 (18,100 × 1,748), downscaled |
| `stretch/details/<story>.webp` | Full-resolution crops around each story's box, with a 35 % margin |
| `stretch/stretch.json` | Rectangle, sizes, detail rectangles, master checksum |

Story boxes (master pixels) live in `src/paintings/qingming/stories.js`.

## Credit line

张择端《清明上河图》，北宋，故宫博物院藏 · Zhang Zeduan, *Along the River During the Qingming Festival*,
Northern Song, Palace Museum, Beijing. Image: Wikimedia Commons, public domain.
