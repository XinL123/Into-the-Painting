from pathlib import Path
from PIL import Image,ImageChops
import hashlib,json,zipfile
p=Path(__file__).resolve().parent
r=json.loads((p/'proposed-hotspots.json').read_text());im=Image.open(r['master']).convert('RGB')
assert im.size==(35311,1010)
assert hashlib.sha256(Path(r['master']).read_bytes()).hexdigest()==r['master_sha256']
assert len(r['new_candidates'])==9 and len(r['route'])==22
for d in r['new_candidates']:
 assert 30<=len(d['text'].split())<=55
 for k in ['context','detail']:
  a=im.crop(d[k]);b=Image.open(p/'crops'/f"{d['id']}-{k}.png").convert('RGB')
  assert a.size==b.size and ImageChops.difference(a,b).getbbox() is None
 x,y=d['anchor'];a,b,c,e=d['box'];assert a<=x<=c and b<=y<=e
for d in r['rejected']:
 assert d['anchor'] is None
for i,a in enumerate(r['new_candidates']):
 for b in r['existing_13_unchanged']+r['new_candidates'][i+1:]:
  aa=a['box'];bb=b['box'];assert not(min(aa[2],bb[2])>max(aa[0],bb[0]) and min(aa[3],bb[3])>max(aa[1],bb[1]))
base=json.loads(Path('/tmp/gusu-expansion-app-hashes.json').read_text())
changed=[f for f,h in base.items() if not Path(f).exists() or hashlib.sha256(Path(f).read_bytes()).hexdigest()!=h]
assert not changed,changed
frames=json.loads((p/'framing-estimates.json').read_text());assert all(f['fully_inside_image_area'] for f in frames)
result={'native_crops_pixel_identical':18,'new_candidates':9,'existing_preserved':13,'route_count':22,'word_counts':{d['id']:d['word_count'] for d in r['new_candidates']},'new_scene_box_overlaps':0,'framing_geometry_estimates':len(frames),'app_files_unchanged':len(base),'runtime_integration_tested':False}
(p/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
