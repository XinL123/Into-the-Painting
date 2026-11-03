#!/usr/bin/env python3
"""Nine requested scene remixes. CC0 source manifest in the dated review folder.
Writes new v2 files; preserves all earlier clips for comparison and rollback.
All performances and layers are contemporary editorial sound illustrations.
"""
import json, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'assets/sound/raw'; OUT=ROOT/'assets/sound'
REVIEW=ROOT/'research/gusu-audio-refinement-2026-10-29'
NEW={s['key']:RAW/s['file'] for s in json.loads((REVIEW/'new-sources.json').read_text())}
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
 page=cut('soft-page',PREVIOUS['paper'],0,.34,-18,('lowpass',3200,'tempo',.8,'reverb',8,35,20))
 air=cut('study-air',RAW/'109485_1213320-hq.ogg',105,8,-35,('highpass',250,'lowpass',1800),.6,.8)
 render(1,'gusu-school-study-v2',[(air,0,0),(page,.8,0),(page,3.65,-6),(page,6.1,-3)],8,-19)
 fish=cut('wooden-fish',NEW['wooden-fish'],0,.85,-18,('highpass',180,'lowpass',6500,'reverb',22,40,45),.004,.12)
 bell=cut('distant-temple-bell',PREVIOUS['bell'],0,8,-30,('highpass',150,'lowpass',3500,'reverb',30,50,50),.025,.8)
 temple_air=cut('temple-air',RAW/'109485_1213320-hq.ogg',64,8,-37,('highpass',250,'lowpass',2200),.5,.8)
 render(5,'gusu-temple-courtyard-v2',[(temple_air,0,0),(bell,.2,0)]+[(fish,t,g) for t,g in [(1.1,-1),(2.55,-3),(4,-2),(5.5,0),(6.95,-3)]],8.5,-15)
 gong=cut('celebration-gong',PREVIOUS['gong'],0,5,-18,('highpass',130,'lowpass',8500),.004,.5)
 drum=cut('round-drum',PREVIOUS['drum'],0,2.2,-18,('highpass',80,'lowpass',6500),.003,.15)
 cymbal=cut('small-cymbal',NEW['cymbals'],10.95,1.1,-18,('highpass',700,'lowpass',9500),.005,.2)
 wedding=[(gong,t,g) for t,g in [(.4,0),(2.7,-3),(5.1,-1),(7.35,-4)]]
 wedding += [(drum,t,g) for t,g in [(.4,-8),(1.05,-12),(1.55,-10),(2.7,-9),(3.35,-13),(3.85,-10),(5.1,-8),(5.75,-12),(6.25,-10),(7.35,-9),(8,-13),(8.5,-11)]]
 wedding += [(cymbal,2.7,-11),(cymbal,7.35,-14)]
 render(6,'gusu-wedding-procession-v2',wedding,10,-12)
 grain=cut('continuous-rice-pour',NEW['bulk-grain'],15,9,-18,('highpass',130,'lowpass',9000),.2,.6)
 render(7,'gusu-granary-pour-v2',[(grain,0,0)],9,-11)
 cup=cut('gentle-teacup',NEW['cup'],0,.52,-18,('highpass',180,'lowpass',7000,'reverb',7,30,18),.003,.1)
 saucer=cut('cup-and-saucer',NEW['saucer'],0,1.5,-18,('highpass',180,'lowpass',6500,'reverb',7,30,18),.003,.2)
 guests=crowd('garden-guests',RAW/'539811_2396346-hq.ogg',[7,22],8,-33)
 render(8,'gusu-garden-gathering-v2',[(guests[0],0,0),(guests[1],0,-3),(saucer,1.15,-2),(cup,4.4,-6),(saucer,6.15,-5)],8.5,-17)
 stone=cut('stone-footsteps',PREVIOUS['stone'],.1,6,-18,('highpass',100,'lowpass',6500),.03,.2)
 bridge_water=cut('water-under-bridge',RAW/'318064_4457609-hq.ogg',21,8,-25,('highpass',180,'lowpass',5500),.5,.7)
 render(15,'gusu-bridge-water-v2',[(bridge_water,0,0),(stone,.6,0)],8,-12)
 dock_crowd=crowd('quayside-crowd',NEW['dock-crowd'],[13,42,71],9,-24)
 hull=cut('boat-touching-dock',RAW/'506688_10949426-hq.ogg',1,7,-18,('highpass',90,'lowpass',6000),.06,.5)
 dock_water=cut('dock-lapping',RAW/'260263_509379-hq.ogg',3,9,-30,('highpass',150,'lowpass',4500),.4,.7)
 dock_parts=[(p,0,g) for p,g in zip(dock_crowd,[0,-2,-4])]+[(hull,1,0),(dock_water,0,0)]
 render(14,'gusu-wharf-crowd-v2',dock_parts,9,-12)
 gate_crowd=crowd('gate-crowd',NEW['gate-crowd'],[14,49,91],9,-22)
 hooves=cut('passing-horse',RAW/'159498_1177772-hq.ogg',1,8,-18,('highpass',100,'lowpass',6500),.1,.4)
 snort=cut('horse-snort',RAW/'397236_4889106-hq.ogg',0,1.5,-21,('highpass',130),.01,.2)
 render(19,'gusu-city-gate-v2',[(p,0,g) for p,g in zip(gate_crowd,[0,-2,-4])]+[(hooves,.35,0),(snort,4.3,0)],9,-12)
 rim=cut('drum-rim',NEW['drum-rim'],0,.65,-18,('highpass',180,'lowpass',8000),.003,.09)
 # Two brisk phrases, increasingly close strokes, with contrasting rim and cymbal accents.
 theatre=[(drum,t,g) for t,g in [(.4,-1),(1.15,-4),(1.9,-2),(2.4,-1),(3.4,0),(4.15,-3),(4.9,-1),(5.4,-3),(6.1,-4),(6.4,-6),(6.7,-3),(7.3,0),(8.05,-3),(8.8,-1)]]
 theatre += [(rim,t,g) for t,g in [(.775,-7),(1.525,-9),(2.15,-7),(2.775,-8),(3.025,-10),(3.775,-7),(4.525,-9),(5.15,-7),(5.775,-8),(6.25,-10),(6.55,-8),(7.675,-7),(8.425,-9)]]
 theatre += [(cymbal,t,g) for t,g in [(.4,-7),(2.4,-10),(4.9,-8),(7.3,-6),(8.8,-8)]]
 render(11,'gusu-theatre-ensemble-v2',theatre,10,-12)
(REVIEW/'mix-recipes.json').write_text(json.dumps(recipes,indent=2))
print('Rendered',len(recipes),'scene remixes; original clips preserved.')
