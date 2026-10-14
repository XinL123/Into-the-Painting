#!/usr/bin/env python3
"""Gallery assets: companion painting crops and dry-brush opening masks.

    .venv/bin/python scripts/prep-gallery.py

Companions are shown in the gallery only (not enterable). Each is cropped to the
painted area of its museum photograph (mount removed) and resized; nothing else
is changed. Sources: assets/paintings/<id>/SOURCE.md

Brush masks are generated here, not scanned: a simple bristle model (uneven start,
ink running out toward the end of the stroke, dry streaks). Deterministic by seed.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
PAINTINGS = ROOT / "assets/paintings"
BRUSH = ROOT / "assets/ui/brush"

# id: (master file, painted-area rectangle in master pixels, longest side for the web)
COMPANIONS = {
    "juran-retreat": ("1959.348_print.jpg", (150, 790, 820, 3010), 1500),
    "peach-birds": ("1985.367_print.jpg", (900, 620, 2500, 2240), 1400),
    "muqi-dragon": ("1958.427.1_print.jpg", (195, 1120, 970, 2850), 1400),
    "cloudy-mountains": ("1933.220_print.jpg", (760, 22, 3270, 585), 2510),
}


def companions():
    for pid, (fname, rect, longest) in COMPANIONS.items():
        im = Image.open(PAINTINGS / pid / "master" / fname).convert("RGB").crop(rect)
        s = min(1, longest / max(im.size))
        if s < 1:
            im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
        out = PAINTINGS / pid / "web"
        out.mkdir(exist_ok=True)
        im.save(out / f"{pid}.webp", "WEBP", quality=88, method=6)
        print(f"  {pid}: {im.size[0]} x {im.size[1]}")


# ---------- brush masks ----------

def smooth(rng, n, knots):
    """Smooth 1D noise in 0..1 with roughly `knots` bumps over n samples."""
    k = rng.random(knots + 3)
    x = np.linspace(0, knots, n)
    i = np.floor(x).astype(int)
    f = x - i
    f = f * f * (3 - 2 * f)
    return k[i] * (1 - f) + k[i + 1] * f


def stroke(w, h, seed, dry=0.6, round_=0.0, ss=2):
    """One left-to-right brush stroke as an alpha array (h, w) in 0..1."""
    rng = np.random.default_rng(seed)
    W, H = w * ss, h * ss
    x = np.arange(W)[None, :] / W
    y = np.arange(H)[:, None] / H

    # bristles: each row is a bristle with its own ink load; neighbours clump
    clump = smooth(rng, H, max(6, H // (26 * ss)))
    fine = rng.random(H)
    fine = np.convolve(fine, np.ones(3 * ss) / (3 * ss), mode="same")
    load = (0.55 * clump + 0.45 * fine)[:, None]            # 0 wet .. 1 dry

    # where each bristle touches down and lifts off
    start = (0.02 + 0.05 * smooth(rng, H, 9) + 0.02 * rng.random(H))[:, None]
    end = (0.99 - 0.05 * smooth(rng, H, 7) - 0.20 * dry * (load[:, 0] ** 1.5))[:, None]

    # the stroke's upper and lower edges wander
    top = (0.035 + 0.05 * smooth(rng, W, 7) + 0.012 * smooth(rng, W, 60))[None, :]
    bot = (0.965 - 0.05 * smooth(rng, W, 6) - 0.012 * smooth(rng, W, 50))[None, :]
    if round_:
        # press and release: the stroke swells in the middle
        swell = np.sqrt(np.clip(1 - ((x - 0.5) / 0.5) ** 2, 0, 1)) ** (1 / (1 + 2 * round_))
        mid = 0.5
        top = mid - (mid - top) * (1 - round_ + round_ * swell)
        bot = mid + (bot - mid) * (1 - round_ + round_ * swell)

    body = (x > start) & (x < end) & (y > top) & (y < bot)

    # ink runs out along the stroke: dry bristles start skipping, wetter ones later
    ink = 1.0 - dry * np.clip((x - 0.25) / 0.75, 0, 1) ** 1.3
    skip = rng.random((H // ss, W // (40 * ss) + 2))
    skip = np.asarray(Image.fromarray((skip * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), np.float32) / 255
    streak = (load * 0.75 + skip * 0.25) < (ink + 0.12)
    # edge bristles are always the driest
    edge = np.minimum(y - top, bot - y) / 0.08
    streak &= (load * 0.6 + skip * 0.4) < np.clip(edge, 0, 1) * 1.2 + 0.25

    a = (body & streak).astype(np.float32)
    im = Image.fromarray((a * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(ss * 0.9))
    im = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255
    return np.clip((a - 0.12) * 1.35, 0, 1)                 # ink bleeds a little, edges stay crisp-ish


def save_mask(name, a, vertical=False):
    im = Image.fromarray((a * 255).round().astype(np.uint8))
    if vertical:
        im = im.transpose(Image.ROTATE_270)                 # stroke runs top to bottom
    rgba = Image.merge("RGBA", (Image.new("L", im.size, 255),) * 3 + (im,))
    BRUSH.mkdir(parents=True, exist_ok=True)
    rgba.save(BRUSH / f"{name}.webp", "WEBP", quality=90, alpha_quality=92, method=6)
    print(f"  {name}: {im.size[0]} x {im.size[1]}")


def masks():
    # five upright strokes from the same hand: alike in size, each one different
    for name, seed, w, dry in (
        ("brush-dragon", 42, 380, 0.75),
        ("brush-juran", 5, 400, 0.6),
        ("brush-qingming", 11, 430, 0.5),
        ("brush-cloudy", 23, 390, 0.8),
        ("brush-birds", 8, 400, 0.65),
    ):
        save_mask(name, stroke(1500, w, seed=seed, dry=dry), vertical=True)


if __name__ == "__main__":
    print("companions")
    companions()
    print("brush masks")
    masks()
