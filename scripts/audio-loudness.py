# Mono BS.1770 K-weighted, 400ms/100ms gated estimate; not a stereo programme meter.
import subprocess,json,numpy as np,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'research/gusu-smooth-audio-2026-11-01'
def read(path,k=False):
 cmd=['sox',str(path),'-r','48000','-c','1','-t','f32','-']
 if k:cmd+=['biquad','1.53512485958697','-2.69169618940638','1.19839281085285','1','-1.69065929318241','.73248077421585','biquad','1','-2','1','1','-1.99004745483398','.99007225036621']
 return np.frombuffer(subprocess.check_output(cmd,stderr=subprocess.DEVNULL),dtype='<f4').astype(float)
def measure(path,gain=1):
 raw=read(path)*gain;y=read(path,True)*gain
 win=19200;hop=4800
 energy=np.array([np.mean(y[i:i+win]**2) for i in range(0,len(y)-win+1,hop)])
 loud=-.691+10*np.log10(np.maximum(energy,1e-20));sel=energy[loud>-70]
 abs_l=-.691+10*np.log10(np.mean(sel));rel=energy[(loud>-70)&(loud>abs_l-10)]
 return dict(lufs=round(float(-.691+10*np.log10(np.mean(rel))),2),peak=round(float(20*np.log10(max(abs(raw)))),2),rms=round(float(20*np.log10(np.sqrt(np.mean(raw**2)))),2),duration=round(len(raw)/48000,3))
if __name__=='__main__':
 import sys
 print(json.dumps(measure(Path(sys.argv[1]),float(sys.argv[2]) if len(sys.argv)>2 else 1),indent=2))
