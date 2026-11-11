"""Builds the Han Palace review package from the untouched master. Research only: touches nothing in src/ or assets/ except reading the master.
Usage: .venv/bin/python research/han-palace-proposal/build_review.py [--rgb-cache path.png]
"""
import sys, os, json, csv, hashlib
from PIL import Image, ImageCms, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
MASTER = os.path.join(ROOT, 'assets/paintings/han-palace/master/Spring_Morning_in_the_Han_Palace.jpg')
SHA256 = '556575e5ec4326bdd03efa6c7cb1545845c6511ff2333826605c5c475f33c07a'
sys.path.insert(0, HERE)
from candidates import CANDIDATES

def load_rgb():
    cache = sys.argv[sys.argv.index('--rgb-cache') + 1] if '--rgb-cache' in sys.argv else None
    if cache and os.path.exists(cache):
        return Image.open(cache)
    h = hashlib.sha256(open(MASTER, 'rb').read()).hexdigest()
    assert h == SHA256, 'master checksum mismatch'
    im = Image.open(MASTER)  # CMYK JPEG without an embedded profile
    cmyk = ImageCms.ImageCmsProfile('/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc')
    return ImageCms.profileToProfile(im, cmyk, ImageCms.createProfile('sRGB'), outputMode='RGB')

def font(size):
    for p in ['/System/Library/Fonts/Helvetica.ttc', '/System/Library/Fonts/Supplemental/Arial.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

im = load_rgb(); W, H = im.size
RED, AMBER, GREY = (200, 30, 30), (215, 130, 0), (110, 110, 110)
COL = {'accepted': RED, 'optional': AMBER, 'rejected': GREY}

located = [c for c in CANDIDATES if c['box']]
route = sorted([c for c in located if c['status'] == 'accepted'], key=lambda c: -c['marker'][0])
for i, c in enumerate(route, 1): c['order'] = i
for j, c in enumerate(sorted([c for c in located if c['status'] == 'optional'], key=lambda c: -c['marker'][0])): c['order'] = 'O' + str(j + 1)
for j, c in enumerate([c for c in CANDIDATES if c['status'] == 'rejected']): c['order'] = 'R' + str(j + 1)

# ---- contact sheets: context crop with outline (left) + untouched native detail crop (right) ----
os.makedirs(os.path.join(HERE, 'CANDIDATE_CONTACT_SHEETS'), exist_ok=True)
for c in located:
    x0, y0, x1, y1 = c['box']; bw, bh = x1 - x0, y1 - y0
    cx0 = max(0, x0 - max(900, bw)); cx1 = min(W, x1 + max(900, bw))
    ctx = im.crop((cx0, 0, cx1, H)).copy()
    d = ImageDraw.Draw(ctx)
    for k in range(8): d.rectangle((x0 - cx0 - k, y0 - k, x1 - cx0 + k, y1 + k), outline=COL[c['status']])
    s = 1100 / ctx.height; ctx = ctx.resize((int(ctx.width * s), 1100), Image.LANCZOS)
    det = im.crop((x0, y0, x1, y1))              # evidence crop: pixels untouched
    ds = min(1.0, 1100 / det.height, 1500 / det.width)
    det_show = det if ds == 1.0 else det.resize((int(det.width * ds), int(det.height * ds)), Image.LANCZOS)
    pad, cap = 24, 120
    sheet = Image.new('RGB', (ctx.width + det_show.width + pad * 3, 1100 + cap + pad * 2), (247, 244, 236))
    sheet.paste(ctx, (pad, pad)); sheet.paste(det_show, (ctx.width + pad * 2, pad))
    d = ImageDraw.Draw(sheet); f = font(24); fs = font(19)
    d.text((pad, 1100 + pad + 12), f"{c['order']}  {c['title']}   [{c['status']}]   rubric {c['rubric']}", fill=(20, 20, 20), font=f)
    d.text((pad, 1100 + pad + 48), f"left: context x {cx0}-{cx1}, full height, outline = detail box   |   right: detail crop [{x0},{y0},{x1},{y1}] ({bw}x{bh} px) shown at {ds:.2f}x, unaltered", fill=(70, 70, 70), font=fs)
    d.text((pad, 1100 + pad + 76), f"marker centre ({c['marker'][0]},{c['marker'][1]})   master {W}x{H}   sha256 {SHA256[:16]}...", fill=(70, 70, 70), font=fs)
    sheet.save(os.path.join(HERE, 'CANDIDATE_CONTACT_SHEETS', f"{str(c['order']).zfill(2)}_{c['id']}.jpg"), quality=88)
    det.save(os.path.join(HERE, 'CANDIDATE_CONTACT_SHEETS', f"{str(c['order']).zfill(2)}_{c['id']}_detail_native.jpg"), quality=93)

# ---- full-scroll location map: 8 bands, right to left ----
NB, BWID = 8, 2600
bw = W / NB; sc = BWID / bw; bh = int(H * sc); gap = 58
mp = Image.new('RGB', (BWID + 40, NB * (bh + gap) + 70), (247, 244, 236)); d = ImageDraw.Draw(mp); f = font(26); fb = font(30)
d.text((20, 14), 'Spring Dawn in the Han Palace (NPM Guhua 001038) - proposed hotspots, read RIGHT to LEFT, band 1 at top.  red = accepted (route order), amber = optional, grey = rejected', fill=(20, 20, 20), font=font(24))
for b in range(NB):
    X1 = W - b * bw; X0 = X1 - bw; oy = 60 + b * (bh + gap)
    band = im.crop((int(X0), 0, int(X1), H)).resize((BWID, bh), Image.LANCZOS); mp.paste(band, (20, oy + 30))
    d.text((20, oy), f'band {b + 1}:  x {int(X0)} - {int(X1)}   (reading direction: right to left)', fill=(60, 60, 60), font=font(22))
    for c in located:
        mx, my = c['marker']
        if X0 <= mx < X1:
            px, py = 20 + (mx - X0) * sc, oy + 30 + my * sc; r = 22
            d.ellipse((px - r, py - r, px + r, py + r), fill=COL[c['status']], outline='white', width=3)
            t = str(c['order']); tw = d.textlength(t, font=f); d.text((px - tw / 2, py - 15), t, fill='white', font=f)
mp.save(os.path.join(HERE, 'FULL_SCROLL_LOCATION_MAP.jpg'), quality=86)

# ---- register (csv + json) ----
def norm(b): return [round(b[0] / W, 5), round(b[1] / H, 5), round((b[2] - b[0]) / W, 5), round((b[3] - b[1]) / H, 5)]
rows = []
for c in route + [c for c in CANDIDATES if c['status'] != 'accepted']:
    b = c['box']
    fit = lambda vh: round((b[2] - b[0]) * vh / H) if b else None   # subject box width in CSS px when the scroll fills a viewport of height vh
    rows.append(dict(route_order=c['order'], id=c['id'], title=c['title'], status=c['status'], rubric_ref=c['rubric'],
        bbox_px=b, bbox_norm=norm(b) if b else None, marker_px=c['marker'],
        marker_norm=[round(c['marker'][0] / W, 5), round(c['marker'][1] / H, 5)] if b else None,
        box_width_at_fit_h900=fit(900), box_width_at_fit_h390=fit(390),
        evidence_level=c['level'], confidence_image=c['conf_image'], confidence_history=c['conf_history'],
        score_total=sum(c['score']), score_parts=c['score'], sources=c['evidence'], reason=c['reason'],
        story_en=c['story'], words=len(c['story'].split()), fact_zh=c['zh'], visible=c['visible'], guardrail=c['guardrail'], open_issues=c['issues']))
meta = dict(master='assets/paintings/han-palace/master/Spring_Morning_in_the_Han_Palace.jpg', sha256=SHA256, width=W, height=H,
            source='https://commons.wikimedia.org/wiki/File:Spring_Morning_in_the_Han_Palace.jpg', licence='Public domain (Commons)',
            coordinate_note='origin top-left, x increases left to right; route order is right to left (descending x)')
json.dump(dict(meta=meta, hotspots=rows), open(os.path.join(HERE, 'HOTSPOT_REGISTER.json'), 'w'), ensure_ascii=False, indent=1)
with open(os.path.join(HERE, 'HOTSPOT_REGISTER.csv'), 'w', newline='', encoding='utf-8-sig') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader()
    for r in rows: w.writerow({k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in r.items()})

# ---- STORY_REVIEW.md ----
out = ['# Story review: Spring Dawn in the Han Palace', '', 'Drafts for review. Nothing here is in the app. Order is the proposed route, right to left. Word counts are for the English card (target 30-55).', '']
def block(c):
    r = next(r for r in rows if r['id'] == c['id'])
    o = [f"## {c['order']}. {c['title']}", '', f"**Status:** {c['status']} · **Score:** {sum(c['score'])}/100 · **Rubric:** {c['rubric']} · **Words:** {len(c['story'].split())}", '']
    if c['story']: o += [f"> {c['story']}", '']
    o += [f"- **事实说明:** {c['zh']}", f"- **Visible in the crop:** {c['visible']}"]
    if c['box']: o += [f"- **Location:** box `{c['box']}`, marker `{c['marker']}`; sheet `CANDIDATE_CONTACT_SHEETS/{str(c['order']).zfill(2)}_{c['id']}.jpg`; box is {r['box_width_at_fit_h900']} px wide when the scroll fills a 900 px tall window"]
    o += [f"- **Evidence ({c['level']}):** " + ('; '.join(c['evidence']) if c['evidence'] else 'none found'),
          f"- **Confidence:** image {c['conf_image']}; history {c['conf_history']}"]
    if c['guardrail']: o.append(f"- **Guardrail:** {c['guardrail']}")
    if c['issues']: o.append(f"- **Open issue:** {c['issues']}")
    o += [f"- **Why this status:** {c['reason']}", '']
    return o
out += ['# Accepted', '']
for c in route: out += block(c)
out += ['# Optional (your call)', '']
for c in CANDIDATES:
    if c['status'] == 'optional': out += block(c)
out += ['# Rejected', '']
for c in CANDIDATES:
    if c['status'] == 'rejected': out += block(c)
open(os.path.join(HERE, 'STORY_REVIEW.md'), 'w').write('\n'.join(out))

# ---- numbers for the gap review ----
xs = [c['marker'][0] for c in route]
print('accepted', len(route), 'optional', sum(c['status'] == 'optional' for c in CANDIDATES), 'rejected', sum(c['status'] == 'rejected' for c in CANDIDATES))
for c in CANDIDATES:
    if c['story']: 
        n = len(c['story'].split()); print(f"{str(c['order']):>3} {c['id']:14} words {n} {'OK' if 30 <= n <= 55 else 'OUT'} score {sum(c['score'])}")
print('gaps (px between consecutive accepted markers, right to left):')
print([xs[i] - xs[i + 1] for i in range(len(xs) - 1)])
print('route:', [(c['order'], c['id'], c['marker'][0]) for c in route])
