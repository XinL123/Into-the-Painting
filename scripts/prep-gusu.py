"""Faithful derivatives only. No recoloring, reconstruction, sharpening or upsampling.
Run: python3 scripts/prep-gusu.py [--master /path/to/master.jpg]
The supplied master remains offline; only the manifest's derivatives enter Vite.
"""
import argparse, hashlib, json, math
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
EXPECTED = '1e56d64df733839ed8f05cb7d067ced84be6ee5b2a489d0440f6c26ef8546a80'
parser = argparse.ArgumentParser()
parser.add_argument('--master', type=Path, default=ROOT/'research/gusu-proposal/master-research.jpg')
args = parser.parse_args()
assert hashlib.sha256(args.master.read_bytes()).hexdigest() == EXPECTED, 'Unexpected master; coordinates must be reverified'
im = Image.open(args.master).convert('RGB'); W,H = im.size
assert (W,H) == (35311,1010)
OUT = ROOT/'assets/paintings/gusu'
for d in ['web','tiles','details','thumbs']:(OUT/d).mkdir(parents=True,exist_ok=True)
def save(crop,name,width=None,quality=90):
 if width and width<crop.width: crop=crop.resize((width,round(crop.height*width/crop.width)),Image.Resampling.LANCZOS)
 crop.save(OUT/name,'WEBP',quality=quality,method=6)
 return {'file':name,'width':crop.width,'height':crop.height}
preview=save(im,'web/gusu-preview.webp',6000,80)
entrance_rect=[27100,0,31100,H]
entrance=save(im.crop(tuple(entrance_rect)),'web/gusu-entrance-temple.webp',1800,90)
entrance['rect']=entrance_rect
native=[]
for left in range(0,W,4500):
 right=min(W,left+4500+32)
 a=save(im.crop((left,0,right,H)),f'tiles/{left:05d}.webp',quality=90)
 a['rect']=[left,0,right,H];native.append(a)
anchors=json.loads((ROOT/'src/paintings/gusu/anchors.json').read_text())
focus=json.loads((ROOT/'src/paintings/gusu/focus.json').read_text())
details={}
for a in anchors:
 a={**a,**focus.get(a['id'],{})}
 x0,y0,x1,y1=a.get('frameBox',a['box']);mx=max(65,(x1-x0)*.45);my=max(65,(y1-y0)*.45)
 r=[max(0,math.floor(x0-mx)),max(0,math.floor(y0-my)),min(W,math.ceil(x1+mx)),min(H,math.ceil(y1+my))]
 version=3 if a['id'] in {'canal','signs','tea','wedding','wannian','granary'} else 2
 suffix=f'-focus-v{version}' if a['id'] in focus else ''
 d=save(im.crop(tuple(r)),f"details/{a['id']}{suffix}.webp",quality=93);d['rect']=r
 thumb=save(im.crop(tuple(a.get('frameBox',a['box']))),f"thumbs/{a['id']}{suffix}.webp",224,85)
 d['thumb']=thumb['file'];details[a['id']]=d
manifest={'width':W,'height':H,'rect':{'left':0,'top':0,'right':W,'bottom':H},'master_sha256':EXPECTED,'preview':preview,'entrance':entrance,'tiles':native,'details':details}
(OUT/'scene.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'{len(native)} native tiles; {len(details)} exact-master detail crops')
for d in ['web','tiles','details','thumbs']:print(d,round(sum(p.stat().st_size for p in (OUT/d).glob('*.webp'))/1024),'KiB')
