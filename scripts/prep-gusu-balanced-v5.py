#!/usr/bin/env python3
"""Reversible loudness-balanced derivations; original recordings and mixes retained."""
import importlib.util,json,subprocess,tempfile,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/sound';RAW=OUT/'raw';QA=ROOT/'research/gusu-smooth-audio-2026-11-01'
spec=importlib.util.spec_from_file_location('meter',ROOT/'scripts/audio-loudness.py');meter=importlib.util.module_from_spec(spec);spec.loader.exec_module(meter)
before=json.loads((QA/'before-levels.json').read_text());report=[]
def sox(*a):subprocess.run(['sox',*map(str,a)],check=True,stderr=subprocess.DEVNULL)
with tempfile.TemporaryDirectory() as td:
 t=Path(td)
 def stem(name,src,start,length,peak,effects=()):
  p=t/(name+'.wav');sox(src,'-r',48000,'-c',1,'-b',32,p,'trim',start,length,*effects,'gain','-n',peak,'fade','t',.15,length,.5);return p
 study=stem('pages',OUT/'gusu-school-study-v2.wav',0,8,-23)
 guqin=stem('guqin',RAW/'161905_43-hq.mp3',18,7.8,-17,('highpass',100,'lowpass',6500))
 school=t/'school.wav';sox('-m',study,guqin,school,'pad',0,.2,'trim',0,8,'fade','t',.15,8,.7)
 # Quiet indistinct human activity, layered into the existing outdoor courtyard.
 crowd=stem('office-murmur',RAW/'545756_8031303-hq.mp3',66,7.8,-20,('highpass',220,'lowpass',1900))
 air=stem('courtyard',OUT/'gusu-official-courtyard-v4.wav',0,7.8,-22)
 admin=t/'administration.wav';sox('-m',air,crowd,admin,'fade','t',.25,7.8,.7)
 for row in before['g']:
  src={'school':school,'administration':admin}.get(row['id'],OUT/(row['file']+'.wav'))
  work=t/(row['id']+'-source.wav');sox(src,'-r',48000,'-c',1,'-b',32,work)
  target=-24.5;play_gain=.8;asset_target=target-20*math.log10(play_gain)
  # Compress only when isolated transients prevent a comfortable integrated level.
  # This avoids peak-normalising a tiny cloth click and leaving the actual fabric inaudible.
  for attempt in range(8):
   m=meter.measure(work);needed=asset_target-m['lufs'];excess=m['peak']+needed+3
   if excess<=.15:break
   threshold=m['peak']-max(8,excess*1.6)
   compressed=t/(row['id']+f'-compressed-{attempt}.wav')
   curve=f'-100,-100,{threshold:.3f},{threshold:.3f},0,{threshold*.75:.3f}'
   sox(work,compressed,'compand','0,.09',curve,'0','-90','.004')
   work=compressed
  m=meter.measure(work);gain=min(asset_target-m['lufs'],-3-m['peak'])
  final=t/(row['id']+'-final.wav');sox(work,final,'gain',gain)
  name='gusu-balanced-'+row['id']+'-v5'
  sox(final,'-C',5,OUT/(name+'.ogg'));sox(final,'-r',22050,'-c',1,'-b',16,OUT/(name+'.wav'))
  after=meter.measure(OUT/(name+'.ogg'),play_gain)
  wav=meter.measure(OUT/(name+'.wav'),play_gain)
  # Match the resampled fallback to Ogg rather than introducing a browser-volume jump.
  if abs(wav['lufs']-after['lufs'])>.15:
   matched=t/(row['id']+'-fallback.wav')
   sox(OUT/(name+'.wav'),matched,'gain',after['lufs']-wav['lufs'])
   sox(matched,OUT/(name+'.wav'))
  report.append(dict(id=row['id'],old_file=row['file'],file=name,gain=play_gain,before_lufs=row['lufs'],change_lu=round(after['lufs']-row['lufs'],2),**after))
(QA/'after-levels.json').write_text(json.dumps(report,indent=2))
print('\n'.join(str(r) for r in report))
