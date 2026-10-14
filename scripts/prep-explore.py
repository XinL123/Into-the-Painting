#!/usr/bin/env python3
"""Derive the exploration assets for 清明上河图 from the untouched master.

    npm run assets          (= .venv/bin/python scripts/prep-explore.py && ... prep-gallery.py)

Reads   assets/paintings/qingming/master/Alongtheriver_QingMing.jpg
        src/paintings/qingming/stories.js        (hotspot boxes, master pixels)
Writes  assets/paintings/qingming/stretch/web/qingming-stretch-{7000,3500}.webp
        assets/paintings/qingming/stretch/details/<story>.webp   full-resolution crops
        assets/paintings/qingming/stretch/stretch.json

Crop and resample only. No colour, contrast or sharpening changes.
"""
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent.parent
QM = ROOT / "assets/paintings/qingming"
MASTER = QM / "master/Alongtheriver_QingMing.jpg"
MASTER_SHA256 = "ad9ccd836874141c985c8db89589d7f6960719eda8281966646eb41a6ed02950"
OUT = QM / "stretch"

# The stretch the viewer explores: from the road just outside the city gate, past
# the shops, the tavern and the Rainbow Bridge, to the moored grain boats upstream. The bridge
# sits a little right of centre. Master pixels (left, top, right, bottom); top and
# bottom sit just inside the mount border.
RECT = (7500, 24, 25600, 1772)
WIDTHS = (9000, 4500)
MARGIN = 0.35          # a detail crop extends this far beyond its box on each side


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_stories():
    src = (ROOT / "src/paintings/qingming/stories.js").read_text()
    out = []
    for m in re.finditer(r"id:\s*'([^']+)'.*?box:\s*\[([^\]]+)\]", src, re.S):
        out.append((m.group(1), [int(v) for v in m.group(2).split(",")]))
    return out


def main():
    digest = sha256(MASTER)
    if digest != MASTER_SHA256:
        raise SystemExit(f"master checksum mismatch: {digest}\nsee SOURCE.md")
    master = Image.open(MASTER).convert("RGB")
    mw, mh = master.size
    (OUT / "web").mkdir(parents=True, exist_ok=True)
    (OUT / "details").mkdir(parents=True, exist_ok=True)
    for old in list((OUT / "web").glob("*.webp")) + list((OUT / "details").glob("*.webp")):
        old.unlink()

    l, t, r, b = RECT
    stretch = master.crop(RECT)
    W, H = stretch.size
    web = []
    for w in WIDTHS:
        h = round(H * w / W)
        name = f"qingming-stretch-{w}.webp"
        stretch.resize((w, h), Image.LANCZOS).save(OUT / "web" / name, "WEBP", quality=88, method=6)
        web.append({"file": f"web/{name}", "width": w, "height": h})

    details = {}
    for sid, (x0, y0, x1, y1) in read_stories():
        mx, my = (x1 - x0) * MARGIN, (y1 - y0) * MARGIN
        cx0, cy0 = max(l, int(x0 - mx)), max(t, int(y0 - my))
        cx1, cy1 = min(r, int(x1 + mx)), min(b, int(y1 + my))
        name = f"{sid}.webp"
        master.crop((cx0, cy0, cx1, cy1)).save(OUT / "details" / name, "WEBP", quality=92, method=6)
        details[sid] = {"file": f"details/{name}", "rect": [cx0, cy0, cx1, cy1]}

    manifest = {
        "master": {"file": "master/" + MASTER.name, "width": mw, "height": mh, "sha256": digest},
        "rect": {"left": l, "top": t, "right": r, "bottom": b},
        "width": W, "height": H,
        "web": web,
        "details": details,
    }
    (OUT / "stretch.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"stretch {W} x {H}  rect {RECT}")
    for p in sorted((OUT / "web").iterdir()):
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size / 1024:.0f} KB")
    print(f"  {len(details)} detail crops, {sum(p.stat().st_size for p in (OUT / 'details').iterdir()) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
