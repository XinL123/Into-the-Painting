#!/usr/bin/env python3
"""Crops *search areas*, not verified new hotspots, from the locally stored full master.
Usage: python3 crop_from_master.py --master /path/to/master-research.jpg
Requires Pillow (PIL). NEVER rescales or repaints original artwork in raw crops.
"""
import argparse
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ZONES=[
 ('01_Mudu_AB',27200,31300),
 ('02_Granary_C',22000,24800),
 ('03_StoneLake_D',19100,22000),
 ('04_City_EFG',11650,17900),
 ('05_ProvincialOffice_H',7800,11300),
 ('06_Shantang_IJ',1600,5000),
]
p=argparse.ArgumentParser()
p.add_argument('--master',required=True)
p.add_argument('--out',default='gusu_candidate_native_crops')
args=p.parse_args()
Image.MAX_IMAGE_PIXELS=None
im=Image.open(args.master).convert('RGB')
if im.size!=(35311,1010):raise SystemExit(f'Expected master 35311x1010, got {im.size}; DO NOT copy coordinates to a different source.')
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
for name,x0,x1 in ZONES:
 crop=im.crop((x0,0,x1,im.height))
 crop.save(out/(name+'_RAW.png'),optimize=True)
 # An optional coordinate guide for matching native x/y, separate from the unaltered artwork.
 guided=crop.copy();d=ImageDraw.Draw(guided,'RGBA')
 for x in range(((x0+499)//500)*500,x1,500):
  at=x-x0
  d.line((at,0,at,im.height),fill=(0,120,155,110),width=2)
  d.rectangle((at+3,2,at+76,24),fill=(245,244,231,230))
  d.text((at+6,4),str(x),fill=(10,50,65,255))
 for y in range(0,im.height,250):
  d.line((0,y,x1-x0,y),fill=(0,120,155,100),width=2)
 guided.save(out/(name+'_GUIDE.png'),optimize=True)
 print(name, f'x={x0}..{x1}',crop.size)
print('Search areas saved. Next: identify actual objects, annotate exact tight boxes, and verify historical identities.')
