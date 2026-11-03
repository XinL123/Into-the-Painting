#!/usr/bin/env python3
"""Fourth audition: recognizable ensemble, independent guqin, courtyard, clearer paddle and gentle bridge ambience. CC0 source manifest in the dated review folder.
Writes new v2 files; preserves all earlier clips for comparison and rollback.
All performances and layers are contemporary editorial sound illustrations.
"""
import json, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'assets/sound/raw'; OUT=ROOT/'assets/sound'
REVIEW=ROOT/'research/gusu-audio-v4-2026-10-29'
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
 # A continuous real performance excerpt: no chopped cymbal/metal-noise pattern.
 ensemble=cut('natural-suona-percussion',FRESH['ensemble'],.3,7.8,-15,('highpass',65),.12,.55)
 render(6,'gusu-wedding-ensemble-v4',[(ensemble,0,0)],7.8,-13)
 study=cut('soft-pages-and-air',OUT/'gusu-school-study-v2.wav',0,8,-21,(),.1,.45)
 guqin=cut('independent-guqin-phrase',FRESH['guqin'],18,7.8,-28,('highpass',100,'lowpass',6500),.25,.6)
 render(1,'gusu-school-guqin-v4',[(study,0,0),(guqin,.1,0)],8,-19)
 # Outdoor air replaces the close, stiff slap of the previous flag recording.
 air=cut('courtyard-breeze',RAW/'109485_1213320-hq.ogg',34,7.8,-23,('highpass',180,'lowpass',5000),.5,.65)
 steps=cut('distant-courtyard-steps',PREVIOUS['stone'],2,3,-33,('highpass',180,'lowpass',2000),.2,.4)
 render(17,'gusu-official-courtyard-v4',[(air,0,0),(steps,3.3,0)],7.8,-20)
 # Keep actual paddle texture with restrained compression, rather than generic water.
 paddle=cut('clear-paddle-strokes',RAW/'249707_300738-hq.ogg',10,7.8,-18,('highpass',90,'lowpass',10000,'compand','.02,.2','-60,-60,-30,-25,-12,-10,-3,-3'),.1,.5)
 render(20,'gusu-canal-clear-paddle-v4',[(paddle,0,0)],7.8,-8)
 rope=cut('boat-rope',OUT/'gusu-shantang-rope.wav',0,6,-18,(),.1,.3)
 water=cut('quiet-water-under-arch',RAW/'318064_4457609-hq.ogg',31,7.8,-27,('highpass',150,'lowpass',5500),.4,.65)
 # These different passages stay low and distant, beneath rope and water.
 bridge_guests=crowd('distant-bridge-passers',NEW['gate-crowd'],[111,140],7.8,-34)
 render(21,'gusu-bridge-boats-ambience-v4',[(rope,.25,0),(water,0,0),(bridge_guests[0],0,0),(bridge_guests[1],0,-3)],7.8,-12)
(REVIEW/'mix-recipes.json').write_text(json.dumps(recipes,indent=2))
print('Built five v4 clips; old assets preserved.')
