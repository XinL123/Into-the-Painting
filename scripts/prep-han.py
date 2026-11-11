"""Han Palace derivatives. The master stays untouched and offline (git-ignored).
Run: .venv/bin/python scripts/prep-han.py [--cache /path/corrected.png]

Steps, all non-destructive and repeatable:
  1. verify the master's SHA-256;
  2. CMYK -> sRGB with the macOS Generic CMYK profile (the JPEG carries no profile);
  3. one global colour correction (quadratic in Lab) fitted against the National Palace
     Museum's own preview photographs of 故畫001038: assets/paintings/han-palace/color-fit.json;
  4. crop, downsample and encode. No sharpening, repainting or enlargement.
"""
import argparse, hashlib, json, math
from pathlib import Path
import numpy as np, cv2
from PIL import Image, ImageCms
Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/paintings/han-palace'
MASTER = OUT / 'master/Spring_Morning_in_the_Han_Palace.jpg'
EXPECTED = '556575e5ec4326bdd03efa6c7cb1545845c6511ff2333826605c5c475f33c07a'
TILE_SCALE = 0.7          # the print screen of the scan disappears below about 0.8
parser = argparse.ArgumentParser(); parser.add_argument('--cache', type=Path); args = parser.parse_args()

def corrected():
    if args.cache and args.cache.exists(): return Image.open(args.cache)
    assert hashlib.sha256(MASTER.read_bytes()).hexdigest() == EXPECTED, 'Unexpected master; coordinates must be reverified'
    cmyk = ImageCms.ImageCmsProfile('/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc')
    rgb = np.array(ImageCms.profileToProfile(Image.open(MASTER), cmyk, ImageCms.createProfile('sRGB'), outputMode='RGB'))
    M = np.array(json.loads((OUT / 'color-fit.json').read_text())['M'], np.float32)
    for y in range(0, rgb.shape[0], 48):
        L = cv2.cvtColor(rgb[y:y+48].astype(np.float32) / 255, cv2.COLOR_RGB2LAB); sh = L.shape; L = L.reshape(-1, 3)
        l, a, b = L[:, 0] / 100, L[:, 1] / 100, L[:, 2] / 100
        B = (np.stack([np.ones_like(l), l, a, b, l*l, a*a, b*b, l*a, l*b, a*b], 1) @ M).astype(np.float32)
        B[:, 0] = np.clip(B[:, 0], 0, 100)
        rgb[y:y+48] = np.clip(cv2.cvtColor(B.reshape(sh), cv2.COLOR_LAB2RGB) * 255 + 0.5, 0, 255).astype(np.uint8)
    im = Image.fromarray(rgb)
    if args.cache: im.save(args.cache, compress_level=1)
    return im

im = corrected(); W, H = im.size
assert (W, H) == (52680, 2683)
for d in ['web', 'tiles', 'details', 'thumbs']:
    (OUT / d).mkdir(parents=True, exist_ok=True)
    for old in (OUT / d).glob('*.webp'): old.unlink()
def save(crop, name, width=None, quality=88):
    if width and width < crop.width: crop = crop.resize((width, round(crop.height * width / crop.width)), Image.Resampling.LANCZOS)
    crop.save(OUT / name, 'WEBP', quality=quality, method=6)
    return {'file': name, 'width': crop.width, 'height': crop.height}
preview = save(im, 'web/han-palace-preview.webp', 6000, 80)
# gallery opening and first view: the musicians' hall (pipa, zheng and the sleeper on the stool)
# Wide enough to fill the resting view on a ~2:1 window (the scroll is tall, so
# 4000 px, as used for Suzhou, left the left third of the window empty on entry).
entrance_rect = [19650, 0, 25800, H]
entrance = save(im.crop(tuple(entrance_rect)), 'web/han-palace-entrance.webp', 2600, 86); entrance['rect'] = entrance_rect
tiles = []
for left in range(0, W, 4500):
    right = min(W, left + 4500 + 32)
    c = im.crop((left, 0, right, H))
    a = save(c, f'tiles/{left:05d}.webp', round(c.width * TILE_SCALE), 86); a['rect'] = [left, 0, right, H]; tiles.append(a)
anchors = json.loads((ROOT / 'src/paintings/han-palace/anchors.json').read_text())
details = {}
for a in anchors:
    x0, y0, x1, y1 = a.get('frameBox', a['box']); mx = max(90, (x1 - x0) * .45); my = max(90, (y1 - y0) * .45)
    r = [max(0, math.floor(x0 - mx)), max(0, math.floor(y0 - my)), min(W, math.ceil(x1 + mx)), min(H, math.ceil(y1 + my))]
    d = save(im.crop(tuple(r)), f"details/{a['id']}.webp", a.get('detailWidth', 2400), 90); d['rect'] = r
    d['thumb'] = save(im.crop((x0, y0, x1, y1)), f"thumbs/{a['id']}.webp", 224, 85)['file']; details[a['id']] = d
manifest = {'width': W, 'height': H, 'rect': {'left': 0, 'top': 0, 'right': W, 'bottom': H}, 'master_sha256': EXPECTED,
            'preview': preview, 'entrance': entrance, 'tiles': tiles, 'details': details}
(OUT / 'scene.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'{len(tiles)} tiles at {TILE_SCALE}x; {len(details)} detail crops')
for d in ['web', 'tiles', 'details', 'thumbs']: print(d, round(sum(p.stat().st_size for p in (OUT / d).glob('*.webp')) / 1024), 'KiB')
