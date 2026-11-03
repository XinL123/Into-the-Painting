#!/usr/bin/env python3
"""Build the fourteen extra CC0 scene illustrations, preserving the first eight.

Run from any directory. Sources: assets/sound/SOURCE.md and
research/gusu-all-scenes-audio-2026-10-28/new-sources.json. No historical
performance, depicted speaker, species or exact machine is reconstructed.
"""
import json, subprocess, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'assets/sound/raw'
OUT=ROOT/'assets/sound'
NEW={s['key']:RAW/s['file'] for s in json.loads((ROOT/'research/gusu-all-scenes-audio-2026-10-28/new-sources.json').read_text())}

def sox(*args):
 subprocess.run(['sox',*map(str,args)],check=True)

with tempfile.TemporaryDirectory() as td:
 temp=Path(td)
 def segment(name,source,start,duration,peak=-10,effects=()):
  path=temp/(name+'.wav')
  sox(source,'-r',44100,'-c',2,path,'trim',start,duration,'gain',-9,*effects,'gain','-n',peak,'fade','t',.025,duration,.12)
  return path
 def mix(name,parts,duration=6,peak=-10):
  # parts = (input, delay, gain). Avoid automatic mix attenuation; normalize once.
  layers=[]
  for i,(source,delay,level) in enumerate(parts):
   f=temp/f'{name}-{i}.wav'
   length=float(subprocess.check_output(['soxi','-D',str(source)],text=True))
   tail=max(0,duration-delay-length)
   sox(source,f,'gain',level,'pad',delay,f'{tail:.8f}','trim',0,duration)
   layers.append(f)
  mixed=temp/f'{name}-mixed.wav'
  if len(layers)>1: sox('-m',*layers,mixed)
  else: sox(layers[0],mixed)
  final=temp/(name+'.wav')
  sox(mixed,final,'gain','-n',peak,'fade','t',.15,duration,.7)
  sox(final,'-C',5,OUT/(name+'.ogg'))
  sox(final,'-r',22050,'-c',1,'-b',16,OUT/(name+'.wav'))

 page=segment('page',NEW['paper'],0,.34,-8,('highpass',180))
 mix('gusu-school-pages',[(page,.55,0),(page,2.8,-4)],5,-10)
 loom=segment('loom',NEW['loom'],3,6,-10,('highpass',100,'lowpass',6500))
 mix('gusu-cloth-loom',[(loom,0,0)],6,-11)
 gong=segment('gong',NEW['gong'],0,6,-10,('highpass',120))
 mix('gusu-wedding-gong',[(gong,0,0)],6,-13)
 grain=segment('grain',NEW['grain'],.2,6,-10,('highpass',180,'lowpass',8500))
 mix('gusu-granary-grain',[(grain,0,0)],6,-10)
 lid=segment('lid',RAW/'732158_15889796-hq.ogg',2,1.4,-14,('highpass',180))
 cup=segment('cup',RAW/'209009_140737-hq.ogg',0,.7,-12,('highpass',180))
 mix('gusu-garden-ceramics',[(lid,.55,-3),(cup,2.6,-5),(cup,4,-8)],6,-12)
 frogs=segment('frogs',NEW['frogs'],5,6,-12,('highpass',400,'lowpass',7000))
 mix('gusu-pond-frogs',[(frogs,0,0)],6,-14)
 drum=segment('drum',NEW['drum'],0,2.8,-10,('highpass',65,'lowpass',8000))
 mix('gusu-theatre-drum',[(drum,.35,-2),(drum,1.55,-5),(drum,2.15,-3),(drum,3.65,0)],7,-12)
 fabric=segment('fabric',NEW['fabric'],2,6,-12,('highpass',180,'lowpass',7000))
 mix('gusu-dye-fabric',[(fabric,0,0)],6,-11)
 bell=segment('bell',NEW['bell'],0,7,-12,('highpass',100))
 mix('gusu-ruiguang-bell',[(bell,0,0)],7,-14)
 steps=segment('stone',NEW['stone'],.1,6,-10,('highpass',100,'lowpass',7000))
 mix('gusu-wannian-steps',[(steps,0,0)],6,-11)
 flag=segment('flag',RAW/'386797_7236624-hq.ogg',0,4.9,-10,('highpass',180,'lowpass',6000))
 mix('gusu-official-flags',[(flag,.4,0)],6,-12)
 # Overlap distant room recordings to create an indistinct crowd, with no script.
 crowd1=segment('crowd1',RAW/'539811_2396346-hq.ogg',2,6,-12,('pitch',-90,'lowpass',1200,'reverb',25,40,30))
 crowd2=segment('crowd2',RAW/'539811_2396346-hq.ogg',16,6,-12,('pitch',110,'lowpass',1200,'reverb',25,40,30))
 mix('gusu-signs-market',[(crowd1,0,0),(crowd2,0,-2)],6,-14)
 hooves=segment('hooves',RAW/'159498_1177772-hq.ogg',1,6,-10,('highpass',100,'lowpass',6500))
 snort=segment('snort',RAW/'397236_4889106-hq.ogg',0,1.5,-12,('highpass',100))
 mix('gusu-gate-hooves',[(hooves,0,0),(snort,2.4,-5)],6,-12)
 rope=segment('rope',RAW/'231438_2016452-hq.ogg',100,6,-12,('highpass',150,'lowpass',6000))
 mix('gusu-shantang-rope',[(rope,0,0)],6,-12)
