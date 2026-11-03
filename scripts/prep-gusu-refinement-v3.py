#!/usr/bin/env python3
"""Third audition: festive wedding, dry rice, quiet guzheng, maximum eight seconds. CC0 source manifest in the dated review folder.
Writes new v2 files; preserves all earlier clips for comparison and rollback.
All performances and layers are contemporary editorial sound illustrations.
"""
import json, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'assets/sound/raw'; OUT=ROOT/'assets/sound'
REVIEW=ROOT/'research/gusu-audio-v3-2026-10-29'
NEW={s['key']:RAW/s['file'] for s in json.loads((ROOT/'research/gusu-audio-refinement-2026-10-29/new-sources.json').read_text())}
FRESH={s['key']:RAW/s['file'] for s in json.loads((REVIEW/'new-sources.json').read_text())}
PREVIOUS={s['key']:RAW/s['file'] for s in json.loads((ROOT/'research/gusu-all-scenes-audio-2026-10-28/new-sources.json').read_text())}
recipes=[]
def sox(*args): subprocess.run(['sox',*map(str,args)],check=True)
with tempfile.TemporaryDirectory() as td:
 temp=Path(td); serial=0
 def cut(label,source,start,duration,peak=-18,effects=(),attack=.008,release=.06):
  global serial
  serial+=1; path=temp/f'{serial}-{label}.wav'
  sox(source,'-r',44100,'-c',2,'-b',32,path,'trim',start,duration,'gain',-12,*effects,'gain','-n',peak)
  faded=temp/f'{serial}-{label}-f.wav'
  length=float(subprocess.check_output(['soxi','-D',str(path)],text=True))
  sox(path,faded,'fade','t',attack,f'{length:.7f}',release)
  return (label,faded)
 def render(scene,name,parts,duration,peak):
  layers=[]
  for i,((label,source),delay,gain) in enumerate(parts):
   layer=temp/f'{name}-{i}.wav'
   length=float(subprocess.check_output(['soxi','-D',str(source)],text=True))
   used=min(length,duration-delay)
   tail=max(0,duration-delay-used)
   sox(source,layer,'gain',gain,'trim',0,f'{used:.8f}','pad',delay,f'{tail:.8f}')
   layers.append(layer)
  mixed=temp/f'{name}-sum.wav'
  if len(layers)>1:sox('-m',*layers,mixed)
  else:sox(layers[0],mixed)
  final=temp/f'{name}.wav'
  sox(mixed,final,'gain','-n',peak,'fade','t',.2,duration,.9)
  sox(final,'-C',5,OUT/(name+'.ogg'))
  sox(final,'-r',22050,'-c',1,'-b',16,OUT/(name+'.wav'))
  recipes.append(dict(scene=scene,file=name,duration=duration,peak_dbfs=peak,layers=[dict(label=part[0][0],at=part[1],gain_db=part[2]) for part in parts]))
 def crowd(label,source,starts,duration,peak=-23):
  # Different passages overlap softly; no invented or transcribed dialogue.
  result=[]
  for i,start in enumerate(starts):
   result.append(cut(f'{label}-{i}',source,start,duration,peak,('highpass',230,'lowpass',1500,'pitch',[-35,50,-10][i%3]),.4,.7))
  return result
 # The wedding uses short, bright metal accents and a buoyant paired rhythm,
 # with no long low gong or temple bell tail.
 drum=cut('bright-wedding-drum',PREVIOUS['drum'],0,.6,-18,('highpass',120,'pitch',260,'lowpass',7500),.003,.13)
 rim=cut('wedding-rim',NEW['drum-rim'],0,.35,-19,('highpass',500,'lowpass',8500),.003,.1)
 gong=cut('short-bright-gong',PREVIOUS['gong'],0,.65,-18,('highpass',850,'pitch',450,'lowpass',9500),.003,.25)
 cymbal=cut('short-cymbal',NEW['cymbals'],10.95,.5,-19,('highpass',1000,'lowpass',10000),.003,.2)
 parts=[(gong,t,g) for t,g in [(.3,-3),(2.3,-5),(4.3,-3),(6.3,-5)]]
 parts += [(drum,t,g) for t,g in [(.3,0),(.8,-4),(1.3,-2),(1.55,-6),(1.8,-3),(2.3,0),(2.8,-4),(3.3,-2),(3.55,-6),(3.8,-3),(4.3,0),(4.8,-4),(5.3,-2),(5.55,-6),(5.8,-3),(6.3,0),(6.8,-4),(7.05,-3)]]
 parts += [(rim,t,-9) for t in [.55,1.05,2.55,3.05,4.55,5.05,6.55]]
 parts += [(cymbal,t,g) for t,g in [(.3,-8),(1.8,-10),(2.3,-8),(3.8,-10),(4.3,-8),(5.8,-10),(6.3,-8),(7.05,-11)]]
 render(6,'gusu-wedding-festive-v3',parts,7.8,-12)
 # Three dry, separated handling/pouring gestures; no continuous water-like bed.
 rice1=cut('dry-rice-first',FRESH['dry-rice'],.45,1.05,-18,('highpass',600,'lowpass',9500),.04,.12)
 rice2=cut('dry-rice-second',FRESH['dry-rice'],4.4,1.05,-18,('highpass',600,'lowpass',9500),.04,.12)
 rice3=cut('dry-rice-third',FRESH['dry-rice'],8.7,1.05,-18,('highpass',600,'lowpass',9500),.04,.12)
 grains=cut('falling-grains',PREVIOUS['grain'],.2,.8,-21,('highpass',600,'lowpass',9500),.015,.15)
 render(7,'gusu-granary-dry-rice-v3',[(rice1,.4,0),(grains,1.25,-3),(rice2,2.8,-1),(grains,3.65,-5),(rice3,5.15,-2),(grains,6,-4)],7.5,-12)
 garden=cut('garden-cups-and-guests',OUT/'gusu-garden-gathering-v2.wav',0,7.8,-20,(),.1,.4)
 note1=cut('quiet-guzheng-first',FRESH['guzheng'],0,3.0,-24,('highpass',180,'lowpass',7000,'reverb',10,35,25),.006,.3)
 note2=cut('quiet-guzheng-second',FRESH['guzheng'],7.25,3.0,-26,('highpass',180,'lowpass',7000,'reverb',10,35,25),.006,.3)
 render(8,'gusu-garden-guzheng-v3',[(garden,0,0),(note1,.55,0),(note2,4.15,0)],7.8,-17)
 # Condense the theatre phrase into 7.8s rather than cutting the final accent off.
 centre=cut('theatre-centre',PREVIOUS['drum'],0,1.4,-18,('highpass',80,'lowpass',6500),.003,.18)
 edge=cut('theatre-edge',NEW['drum-rim'],0,.6,-18,('highpass',180,'lowpass',8000),.003,.1)
 metal=cut('theatre-cymbal',NEW['cymbals'],10.95,1.05,-18,('highpass',700,'lowpass',9500),.005,.22)
 parts=[(centre,t,g) for t,g in [(.3,-1),(.95,-4),(1.6,-2),(2.1,-1),(2.8,0),(3.45,-3),(4.1,-1),(4.6,-3),(5.1,-4),(5.35,-6),(5.6,-3),(6.2,0),(6.85,-3)]]
 parts += [(edge,t,-8) for t in [.625,1.275,1.85,2.425,3.125,3.775,4.35,4.85,5.225,5.475,6.525]]
 parts += [(metal,t,g) for t,g in [(.3,-7),(2.1,-10),(4.1,-8),(6.2,-6),(6.85,-9)]]
 render(11,'gusu-theatre-short-v3',parts,7.8,-12)
 # Existing longer scenes retain native speed, trimmed with a natural ending.
 for scene,stem in [(5,'temple-courtyard'),(14,'wharf-crowd'),(19,'city-gate')]:
  source=OUT/f'gusu-{stem}-v2.wav';name=f'gusu-{stem}-v3'
  sox(source,OUT/(name+'.wav'),'trim',0,7.8,'fade','t',0,7.8,.65)
  sox(OUT/(name+'.wav'),'-C',5,OUT/(name+'.ogg'))
  recipes.append(dict(scene=scene,file=name,duration=7.8,treatment='native-speed trim with 650ms end fade'))
(REVIEW/'mix-recipes.json').write_text(json.dumps(recipes,indent=2))
print('Built seven v3 clips; every Gusu scene now fits within eight seconds.')
