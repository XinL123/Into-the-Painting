from pathlib import Path
from PIL import Image,ImageChops
import json,hashlib,math
P=Path(__file__).resolve().parent;r=json.loads((P/'final-hotspots.json').read_text());im=Image.open(r['master']).convert('RGB')
assert im.size==(35311,1010) and hashlib.sha256(Path(r['master']).read_bytes()).hexdigest()==r['master_sha256']
assert len(r['new_candidates'])==9 and len(r['route'])==22
assert {d['id'] for d in r['new_candidates']}==set(['A','B','C','D','F','G','E2','H','J'])
for d in r['new_candidates']:
 assert 30<=len(d['text'].split())<=55
 for key in ['context','detail']:
  b=d[key];a=im.crop(b);c=Image.open(P/'crops'/f"{d['id']}-{key}.png").convert('RGB');assert a.size==c.size and ImageChops.difference(a,c).getbbox() is None
  assert 0<=b[0]<b[2]<=35311 and 0<=b[1]<b[3]<=1010
 x,y=d['anchor'];b=d['box'];assert b[0]<=x<=b[2] and b[1]<=y<=b[3]
for i,a in enumerate(r['new_candidates']):
 for b in r['new_candidates'][i+1:]+r['existing_13_unchanged']:
  aa=a['box'];bb=b['box'];assert not(min(aa[2],bb[2])>max(aa[0],bb[0]) and min(aa[3],bb[3])>max(aa[1],bb[1])),(a['id'],b['id'])
live=json.loads(Path('playground/painting/src/paintings/gusu/anchors.json').read_text());assert [d['box'] for d in live]==[d['box'] for d in r['existing_13_unchanged']]
base=json.loads((P/'application-baseline.json').read_text());assert all(hashlib.sha256(Path(f).read_bytes()).hexdigest()==h for f,h in base.items())
res=dict(native_crops_pixel_identical=18,master_unchanged=True,application_files_unchanged=len(base),existing_anchor_boxes_unchanged=13,new_candidates=9,total_route=22,scene_box_collisions=0,word_counts={d['id']:d['word_count'] for d in r['new_candidates']},runtime_integration_performed=False)
(P/'verification.json').write_text(json.dumps(res,indent=2));print(json.dumps(res,indent=2))
