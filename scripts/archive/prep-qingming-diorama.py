#!/usr/bin/env python3
"""Derive the Qingming pilot assets from the untouched master.

    npm run assets            (= .venv/bin/python scripts/prep-qingming.py)

Reads   assets/paintings/qingming/master/Alongtheriver_QingMing.jpg
        assets/paintings/qingming/scene-hongqiao/masks/hongqiao-shapes.json  (rough hand outlines)
Writes  assets/paintings/qingming/scene-hongqiao/crop/    the scene crop, lossless, unretouched
        assets/paintings/qingming/scene-hongqiao/web/     flat crop for the browser
        assets/paintings/qingming/scene-hongqiao/layers/  the diorama's cards
        assets/paintings/qingming/scene-hongqiao/depth/   per-card depth maps, water mask
        assets/paintings/qingming/scene-hongqiao/masks/   card masks (PNG, for inspection)
        assets/paintings/qingming/scene-hongqiao/scene.json

The scene is a painting diorama. The crop is cut into cards that stand at different
distances:

  ground      far bank, river, street: one surface running away from the bottom edge
  things      everything standing on that ground (figures, stalls, parasols, small
              boats, far houses, willows), found automatically from where the ink is
              and stood upright on its own base
  barge, bridge, boat, nearbank, gate, foreground
              large pieces cut by hand outline, snapped to the painted silhouette

What is and is not done to the artwork
  * the flat crop is crop + resample only
  * every card is the painting's own pixels; stacked at rest they are the crop again
    (the script prints the difference)
  * what lies behind a card is filled in, since the viewer can now look a little
    way round it: mirrored source pixels behind the large cards, diffusion from the
    surrounding silk behind figures and twigs. This filling is the only invented
    picture, and it only shows when cards part.
"""
import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None  # the master is 38,414 x 1,800

ROOT = Path(__file__).resolve().parent.parent
QM = ROOT / "assets/paintings/qingming"
SCENE = QM / "scene-hongqiao"
MASTER = QM / "master/Alongtheriver_QingMing.jpg"
MASTER_SHA256 = "ad9ccd836874141c985c8db89589d7f6960719eda8281966646eb41a6ed02950"

# A long stretch of the scroll with the Rainbow Bridge near its middle: from the
# decorated gate (彩楼欢门) on the left bank to the great willow downstream. The
# viewer travels along it. Rectangle in master pixels (left, top, right, bottom);
# top/bottom sit just inside the mount border.
SCENE_RECT = (16545, 24, 22545, 1772)

SCALES = (1, 0.5)          # full and half-size sets for the browser
EDGE_FEATHER = 1.6         # px, softness of cut-out edges
FILL_BAND = 220            # px, how far behind a large card's edge the fill reaches
DEPTH_SCALE = 0.25         # depth maps are stored at quarter size
FIGURE_H = 130             # px, about the tallest single thing standing in a crowd


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ellipse(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def poly_mask(shape, points):
    m = np.zeros(shape, np.uint8)
    cv2.fillPoly(m, [np.array(points, np.int32)], 255)
    return m


def soft(mask):
    """Hard 0/255 mask -> float alpha with a feathered edge."""
    return cv2.GaussianBlur(mask.astype(np.float32) / 255, (0, 0), EDGE_FEATHER)


def ink_darkness(img):
    """How much darker each pixel is than the bare silk around it."""
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    silk = cv2.GaussianBlur(
        cv2.morphologyEx(cv2.medianBlur(img, 5), cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8)), (0, 0), 8)
    return np.clip(cv2.cvtColor(silk, cv2.COLOR_BGR2GRAY).astype(np.float32) - lum, 0, None), lum


def snap(feat, hard, reach=40, scale=0.5):
    """Snap a rough outline to the painted silhouette (GrabCut within `reach` px of it)."""
    H, W = hard.shape
    sure = cv2.erode(hard, ellipse(reach))
    maybe = cv2.dilate(hard, ellipse(reach))
    ys, xs = np.nonzero(maybe)
    y0, y1 = max(ys.min() - 20, 0), min(ys.max() + 20, H)
    x0, x1 = max(xs.min() - 20, 0), min(xs.max() + 20, W)
    sub = cv2.resize(feat[y0:y1, x0:x1], None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    rs = lambda m: cv2.resize(m[y0:y1, x0:x1], (sub.shape[1], sub.shape[0]), interpolation=cv2.INTER_NEAREST)
    m = np.full(sub.shape[:2], cv2.GC_BGD, np.uint8)
    m[rs(maybe) > 0] = cv2.GC_PR_BGD
    m[rs(hard) > 0] = cv2.GC_PR_FGD
    m[rs(sure) > 0] = cv2.GC_FGD
    cv2.setRNGSeed(7)
    cv2.grabCut(sub, m, None, np.zeros((1, 65)), np.zeros((1, 65)), 4, cv2.GC_INIT_WITH_MASK)
    r = ((m == cv2.GC_FGD) | (m == cv2.GC_PR_FGD)).astype(np.uint8) * 255
    r = cv2.morphologyEx(r, cv2.MORPH_CLOSE, ellipse(6))
    r = cv2.morphologyEx(r, cv2.MORPH_OPEN, ellipse(3))
    full = np.zeros((H, W), np.uint8)
    full[y0:y1, x0:x1] = cv2.resize(r, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
    full = (cv2.GaussianBlur(full, (0, 0), 3) > 127).astype(np.uint8) * 255
    # a card has no holes: whatever shows through one would be torn when it moves
    contours, _ = cv2.findContours(full, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    full = np.zeros_like(full)
    cv2.drawContours(full, contours, -1, 255, cv2.FILLED)
    # the picture's own edges are not silhouettes
    edge = np.zeros_like(hard)
    edge[:, :3] = edge[:, -3:] = edge[:3] = edge[-3:] = 255
    grow = cv2.dilate(cv2.bitwise_and(hard, edge), ellipse(reach))
    return np.where(grow > 0, hard, full)


def fill_behind(img, hard_mask):
    """Fill a band just inside the mask edge with the picture mirrored across that edge.

    Every filled pixel is a copy of a real source pixel from just outside the cut-out,
    so the silk's weave and tone carry on unbroken.
    """
    grow = cv2.dilate(hard_mask, ellipse(6))
    dist, labels = cv2.distanceTransformWithLabels(grow, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    oy, ox = np.nonzero(grow == 0)
    lut_y = np.zeros(labels.max() + 1, np.int32)
    lut_x = np.zeros(labels.max() + 1, np.int32)
    lut_y[labels[oy, ox]] = oy
    lut_x[labels[oy, ox]] = ox
    py, px = np.nonzero((hard_mask > 0) & (dist <= FILL_BAND))   # only under the card itself
    ny, nx = lut_y[labels[py, px]], lut_x[labels[py, px]]
    h, w = grow.shape
    sy = np.clip(2 * ny - py, 0, h - 1)
    sx = np.clip(2 * nx - px, 0, w - 1)
    inside = grow[sy, sx] > 0            # the mirror image fell inside another cut-out
    sy[inside], sx[inside] = ny[inside], nx[inside]
    out = img.copy()
    out[py, px] = img[sy, sx]
    lost = np.zeros(grow.shape, np.uint8)  # those spots are handed back to the caller
    lost[py[inside], px[inside]] = 255
    return out, cv2.dilate(lost, ellipse(2))


def solve_colour(orig, under, alpha):
    """Colour for a card so that  alpha*colour + (1-alpha)*under == orig."""
    a = np.maximum(alpha, 1e-3)[..., None]
    c = (orig.astype(np.float32) - (1 - a) * under.astype(np.float32)) / a
    c = np.where(alpha[..., None] < 0.6, orig, c)    # in the thin feathered rim the picture itself is the best colour
    return np.clip(c, 0, 255)


def run_bottom(mask):
    """For every pixel of a mask, the y of the bottom of the vertical run it sits in."""
    H, W = mask.shape
    out = np.zeros((H, W), np.int32)
    below = np.full(W, H - 1, np.int32)
    for y in range(H - 1, -1, -1):
        on = mask[y] > 0
        nxt = mask[y + 1] > 0 if y + 1 < H else np.zeros(W, bool)
        below = np.where(on & nxt, below, y)
        out[y] = below
    return out


def save_rgba(path, bgr, alpha, scale):
    rgba = np.dstack([bgr[..., ::-1], alpha * 255]).round().astype(np.uint8)
    im = Image.fromarray(rgba)
    if scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    im.save(path, "WEBP", quality=92, alpha_quality=100, method=6)


def save_rgb(path, bgr, scale, quality=92):
    im = Image.fromarray(np.clip(bgr[..., ::-1], 0, 255).round().astype(np.uint8))
    if scale != 1:
        im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6)


def main():
    digest = sha256(MASTER)
    if digest != MASTER_SHA256:
        raise SystemExit(f"master checksum mismatch: {digest}\nsee SOURCE.md")

    master = Image.open(MASTER).convert("RGB")
    mw, mh = master.size
    for d in ("crop", "web", "masks", "layers", "depth"):
        (SCENE / d).mkdir(parents=True, exist_ok=True)
        for old in (SCENE / d).glob("hongqiao-*"):
            if old.suffix in (".png", ".webp"):
                old.unlink()

    crop = master.crop(SCENE_RECT)
    W, H = crop.size
    crop.save(SCENE / "crop/hongqiao-crop.png", optimize=True)
    orig = cv2.cvtColor(np.asarray(crop), cv2.COLOR_RGB2BGR)
    shapes = json.loads((SCENE / "masks/hongqiao-shapes.json").read_text())
    P = lambda name: poly_mask((H, W), shapes[name])

    dark, lum = ink_darkness(orig)
    feat = np.dstack([np.clip(cv2.GaussianBlur(dark, (0, 0), 5) * 6, 0, 255),
                      np.clip(cv2.GaussianBlur(dark, (0, 0), 16) * 8, 0, 255), lum]).astype(np.uint8)
    cut_out = lambda name: snap(feat, P(name))

    # ---- the large cards, by hand outline ----
    bridge_hard = cut_out("bridge")
    boat_hard = cut_out("boat") & ~bridge_hard
    barge_hard = cut_out("barge") & ~(bridge_hard | boat_hard)      # passing beneath the arch
    fg_hard = cut_out("foreground")                                   # rooftops along the bottom edge
    gate_hard = cut_out("gate") & ~fg_hard                            # the decorated gate and its roof
    pole_hard = P("pole")                                             # the wind-vane pole: too thin to snap
    # the near bank behind the roofs; its outline runs on underneath them
    bank_hard = (cut_out("nearBank") | (P("nearBank") & fg_hard) | pole_hard)
    cut = bridge_hard | boat_hard | barge_hard | bank_hard | fg_hard | gate_hard

    # ---- things: whatever stands on the ground, found from where the ink is ----
    density = cv2.GaussianBlur(dark, (0, 0), 3)
    obj = ((density > 22) | (cv2.GaussianBlur(dark, (0, 0), 9) > 16)).astype(np.uint8) * 255
    obj = cv2.morphologyEx(cv2.dilate(obj, ellipse(3)), cv2.MORPH_CLOSE, ellipse(4))
    obj[cv2.dilate(cut, ellipse(3)) > 0] = 0
    tree_zone = np.zeros((H, W), np.uint8)
    for tree in shapes["uprights"]:
        tree_zone |= poly_mask((H, W), tree["outline"])
    obj[tree_zone > 0] = 0
    n, labels, stats, _ = cv2.connectedComponentsWithStats(obj, connectivity=8)
    keep = stats[:, cv2.CC_STAT_AREA] >= 260
    # the far bank stays on the ground: whatever stands wholly above that line
    keep &= (stats[:, cv2.CC_STAT_TOP] + stats[:, cv2.CC_STAT_HEIGHT]) > shapes["farBankBelow"]
    keep[0] = False
    obj = keep[labels].astype(np.uint8) * 255

    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    at = lambda y: np.asarray(y, np.float32) / (H - 1)
    ground = at(ys)

    # Each thing is as near as the ground under its own feet. A single figure or stall
    # stands as one upright piece; in a crowd, where things overlap up the picture,
    # each part stands on the ground a figure's height below it.
    base_y = np.minimum(run_bottom(obj), ys + FIGURE_H)
    bottoms = (stats[:, cv2.CC_STAT_TOP] + stats[:, cv2.CC_STAT_HEIGHT] - 1).astype(np.float32)
    small = stats[:, cv2.CC_STAT_HEIGHT] <= int(FIGURE_H * 1.3)
    base_y = np.where(small[labels], bottoms[labels], cv2.blur(base_y.astype(np.float32), (31, 1)))
    things_depth = at(base_y)
    life = (small[labels] & (obj > 0)).astype(np.float32)             # single figures may stir a little
    # trees: one upright piece each, standing on its trunk's foot. Only their ink is
    # lifted (twigs are too fine to cut round); the silk between the twigs stays behind.
    tree_ink = np.zeros((H, W), np.uint8)
    tree_alpha = np.zeros((H, W), np.float32)
    for tree in shapes["uprights"]:
        zone = poly_mask((H, W), tree["outline"]) > 0
        ink = cv2.GaussianBlur(dark, (0, 0), 1.2)
        a = np.clip((ink - 8) / 22, 0, 1) * cv2.GaussianBlur(zone.astype(np.float32), (0, 0), 10)
        tree_alpha = np.maximum(tree_alpha, a)
        tree_ink[(a > 0.3) & (cut == 0)] = 255
        things_depth[zone] = at(tree["standsAt"])
        life[zone] = 0
    things_depth[(obj == 0) & (tree_ink == 0)] = 0
    # between things, each bit of (invisible) card takes after the nearest thing
    stood = obj | tree_ink
    _, near = cv2.distanceTransformWithLabels(255 - stood, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
    oy, ox = np.nonzero(stood)
    lut = np.zeros(near.max() + 1, np.float32)
    lut[near[oy, ox]] = things_depth[oy, ox]
    things_depth = lut[near]
    phase = ((labels * 0.61803398875) % 1.0).astype(np.float32)
    things_a = np.maximum(soft(obj), tree_alpha)

    # ---- ground: the whole picture with everything standing on it taken off ----
    base, lost = fill_behind(orig, cut)
    pole_zone = cv2.dilate(pole_hard, np.ones((11, 11), np.uint8)) & ~(cut & ~pole_hard)
    w_pole = cv2.GaussianBlur(pole_zone.astype(np.float32) / 255, (0, 0), 2)[..., None]
    base = (base * (1 - w_pole) + np.roll(orig, -110, axis=1) * w_pole).astype(np.uint8)
    # under each thing: the bare silk's local tone (from the silk around it) with the
    # picture's own weave laid over it
    bare = ((obj == 0) & (cut == 0) & (cv2.GaussianBlur(dark, (0, 0), 6) < 7)).astype(np.float32)
    # inside a tree, the silk showing between the twigs is the tone to continue
    for tree in shapes["uprights"]:
        gaps = (poly_mask((H, W), tree["outline"]) > 0) & (cv2.GaussianBlur(dark, (0, 0), 2) < 10) & (cut == 0)
        bare[gaps] = 1
    src = orig.astype(np.float32)
    tone = np.broadcast_to(src[bare > 0].mean(axis=0), src.shape).copy()   # last resort: the silk's mean
    for sigma in (400, 140, 50):                     # nearer bare silk wins where there is some
        wsum = cv2.GaussianBlur(bare, (0, 0), sigma)
        local = cv2.GaussianBlur(src * bare[..., None], (0, 0), sigma) / np.maximum(wsum, 1e-4)[..., None]
        trust = np.clip(wsum / 0.08, 0, 1)[..., None]
        tone = local * trust + tone * (1 - trust)
    # the weave laid over the fill comes from a patch of open water, tiled, so no ink
    # from what was lifted shows through it
    grain = orig.astype(np.float32) - cv2.GaussianBlur(orig, (0, 0), 2.5).astype(np.float32)
    gx0, gy0, gx1, gy1 = shapes["bareSilkPatch"]
    patch = grain[gy0:gy1, gx0:gx1]
    reps = (H // patch.shape[0] + 2, W // patch.shape[1] + 2, 1)
    quiet = np.tile(patch, reps)[:H, :W] * 0.6
    hole = cv2.dilate(obj, ellipse(1)) | cv2.dilate(tree_ink, ellipse(2)) | lost   # also where the mirror had nothing to mirror
    w_obj = cv2.GaussianBlur(hole.astype(np.float32) / 255, (0, 0), 1)[..., None]
    base = np.clip(base * (1 - w_obj) + (tone + quiet) * w_obj, 0, 255).astype(np.float32)

    # ---- large cards run on a little under the cards in front, and take their colour ----
    def under(card, front, grow=90):
        return cv2.dilate(card, ellipse(grow)) & front
    barge_under = under(barge_hard, bridge_hard | boat_hard)
    bridge_under = under(bridge_hard, boat_hard)
    bank_under = bank_hard & fg_hard

    comp = base.copy()
    def card(alpha, hidden=None, front=None):
        nonlocal comp
        rgb = solve_colour(orig, comp, alpha)
        if hidden is not None:
            grown = cv2.dilate(hidden, np.ones((13, 13), np.uint8))
            rgb = np.where(grown[..., None] > 0, fill_behind(orig, front)[0].astype(np.float32), rgb)
        a = alpha[..., None]
        comp = rgb * a + comp * (1 - a)
        return rgb
    things_rgb = card(things_a)
    barge_a = soft(barge_hard | barge_under); barge_rgb = card(barge_a, barge_under, bridge_hard | boat_hard)
    bridge_a = soft(bridge_hard | bridge_under); bridge_rgb = card(bridge_a, bridge_under, boat_hard)
    boat_a = soft(boat_hard); boat_rgb = card(boat_a)
    bank_a = soft(bank_hard); bank_rgb = card(bank_a, bank_under, fg_hard)
    gate_a = soft(gate_hard); gate_rgb = card(gate_a)
    fg_a = soft(fg_hard); fg_rgb = card(fg_a)

    # ---- depth of the large cards: 0 = farthest, 1 = nearest ----
    (x0, y0), (x1, y1) = shapes["bridgeFeet"]         # the bridge stands over the line between its feet
    foot_y = y0 + (np.clip(xs, x0, x1) - x0) * (y1 - y0) / (x1 - x0)
    blend_l, blend_r = shapes["bridgeBlend"]          # where the deck meets each bank
    w = np.clip((xs - blend_l[0]) / (blend_l[1] - blend_l[0]), 0, 1) * \
        np.clip((blend_r[1] - xs) / (blend_r[1] - blend_r[0]), 0, 1)
    w = w * w * (3 - 2 * w)
    bridge_depth = np.maximum(ground, ground + (at(foot_y) - ground) * w)
    (bx0, by0), (bx1, by1) = shapes["boatWaterline"]  # the boat stands along its waterline
    boat_depth = at(by0 + (np.clip(xs, bx0, bx1) - bx0) * (by1 - by0) / (bx1 - bx0))
    flat = lambda key: np.full_like(ground, at(shapes[key]))
    fg_depth = np.maximum(ground, at(shapes["foregroundStandsAt"]))

    # ---- where the river is (for its slow movement) ----
    water = P("water").astype(np.float32) / 255
    water *= 1 - np.clip(cv2.GaussianBlur((cut | obj | tree_zone).astype(np.float32) / 255, (0, 0), 6) * 2, 0, 1)
    water = cv2.GaussianBlur(water, (0, 0), 14)

    layers = [  # drawn in this order
        {"id": "ground", "rgb": base, "alpha": None, "depth": ground, "note": "far bank, river, street"},
        {"id": "barge", "rgb": barge_rgb, "alpha": barge_a, "depth": flat("bargeStandsAt"), "note": "the barge beneath the arch"},
        {"id": "bridge", "rgb": bridge_rgb, "alpha": bridge_a, "depth": bridge_depth, "note": "the Rainbow Bridge and its crowd"},
        {"id": "boat", "rgb": boat_rgb, "alpha": boat_a, "depth": boat_depth, "note": "the boat fighting the current"},
        {"id": "nearbank", "rgb": bank_rgb, "alpha": bank_a, "depth": flat("nearBankStandsAt"), "note": "pavilion, parasols, moored boat, pole"},
        {"id": "things", "rgb": things_rgb, "alpha": things_a, "depth": things_depth, "phase": phase, "life": life,
         "note": "figures, stalls, small boats, far houses, willows: each upright on its own base"},
        {"id": "gate", "rgb": gate_rgb, "alpha": gate_a, "depth": flat("gateStandsAt"), "note": "the decorated gate"},
        {"id": "foreground", "rgb": fg_rgb, "alpha": fg_a, "depth": fg_depth, "note": "rooftops along the bottom edge"},
    ]

    small_size = (round(W * DEPTH_SCALE), round(H * DEPTH_SCALE))
    shrink = lambda a, how=cv2.INTER_AREA: cv2.resize(a, small_size, interpolation=how)
    manifest_layers = []
    for L in layers:
        files = {}
        for s in SCALES:
            w_px = round(W * s)
            name = f"hongqiao-{L['id']}-{w_px}.webp"
            if L["alpha"] is None:
                save_rgb(SCENE / "layers" / name, L["rgb"], s)
            else:
                save_rgba(SCENE / "layers" / name, L["rgb"], L["alpha"], s)
            files[str(w_px)] = f"layers/{name}"
        dname = f"hongqiao-{L['id']}-depth.png"
        stepped = "phase" in L                       # upright pieces: no blending between neighbours
        how = cv2.INTER_NEAREST if stepped else cv2.INTER_AREA
        chans = [shrink(L["depth"], how), shrink(L.get("phase", np.zeros_like(ground)), cv2.INTER_NEAREST),
                 shrink(L.get("life", np.zeros_like(ground)), cv2.INTER_NEAREST)]
        Image.fromarray((np.clip(np.dstack(chans), 0, 1) * 255).round().astype(np.uint8)).save(SCENE / "depth" / dname)
        if L["alpha"] is not None:
            Image.fromarray((L["alpha"] * 255).round().astype(np.uint8)).save(
                SCENE / "masks" / f"hongqiao-{L['id']}-mask.png", optimize=True)
        manifest_layers.append({"id": L["id"], "note": L["note"], "files": files,
                                "depth": f"depth/{dname}", "stepped": stepped})
    Image.fromarray((np.clip(shrink(water), 0, 1) * 255).round().astype(np.uint8)).save(SCENE / "depth/hongqiao-water.png")

    web = {}
    for s in SCALES:
        w_px, h_px = round(W * s), round(H * s)
        name = f"hongqiao-{w_px}.webp"
        save_rgb(SCENE / "web" / name, orig, s)
        web[str(w_px)] = {"file": f"web/{name}", "width": w_px, "height": h_px}

    # ---- check: the cards stacked at rest vs the crop ----
    comp = None
    for m in manifest_layers:
        im = np.asarray(Image.open(SCENE / m["files"][str(W)]).convert("RGBA")).astype(np.float32)
        rgb, a = im[..., :3], im[..., 3:] / 255
        comp = rgb if comp is None else rgb * a + comp * (1 - a)
    rms = float(np.sqrt(((comp - np.asarray(crop).astype(np.float32)) ** 2).mean()))
    psnr = 20 * np.log10(255 / rms)

    l, t_, r, b = SCENE_RECT
    scene = {
        "id": "hongqiao",
        "master": {"file": "master/" + MASTER.name, "width": mw, "height": mh, "sha256": digest},
        "rect": {"left": l, "top": t_, "right": r, "bottom": b},
        "crop": {"file": "crop/hongqiao-crop.png", "width": W, "height": H},
        "web": web,
        "layers": manifest_layers,
        "water": "depth/hongqiao-water.png",
        "boatPivot": [(bx0 + bx1) / 2 / W, (by0 + by1) / 2 / H],
        "restCheck": {"rms": round(rms, 2), "psnr": round(float(psnr), 1)},
    }
    (SCENE / "scene.json").write_text(json.dumps(scene, indent=2) + "\n")

    print(f"crop     {W} x {H}  ({W / H:.3f}:1)  rect {SCENE_RECT}")
    print(f"things   {int(keep.sum())} pieces, {int(small[keep].sum())} of them single upright ones")
    print(f"cards stacked at rest vs crop: rms {rms:.2f}, PSNR {psnr:.1f} dB")
    total = sum(p.stat().st_size for p in (SCENE / "layers").glob(f"*-{W}.webp"))
    print(f"full-size cards: {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
