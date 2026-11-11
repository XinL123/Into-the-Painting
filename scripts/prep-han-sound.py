#!/usr/bin/env python3
"""Spring Dawn in the Han Palace: one short sound per discovery.

Real recordings only (Freesound player previews in assets/sound/raw), trimmed,
layered and balanced the way the Suzhou set is: about -24.5 LUFS at the 0.8
playback gain, nothing longer than 8 s, every clip played once.
Sources and licences: assets/sound/SOURCE.md.  Run from playground/painting:

    .venv/bin/python scripts/prep-han-sound.py
"""
import importlib.util, json, math, subprocess, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/sound'
RAW = OUT / 'raw'
spec = importlib.util.spec_from_file_location('meter', ROOT / 'scripts/audio-loudness.py')
meter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(meter)

TARGET, PLAY_GAIN = -24.5, 0.8


def raw(sound_id):
    return next(RAW.glob(f'{sound_id}_*-hq.*'))


def sox(*a):
    subprocess.run(['sox', *map(str, a)], check=True, stderr=subprocess.DEVNULL)


# A layer: (freesound id, start s, length s, peak dBFS, offset s in the mix, extra sox effects[, tempo])
# The first layer of each recipe is the subject; the others sit under it.
RECIPES = {
    # writing: a pen tip on paper, two short phrases
    'shelf-mark': (4.6, [(337087, 3.0, 1.5, -12, 0.3, ('highpass', 500)), (337087, 5.5, 1.4, -13, 2.6, ('highpass', 500))]),
    # the empty swing: rope creaking on its beam, sparrows at dawn
    'swing': (7.5, [(862995, 3.0, 7.5, -10, 0, ()), (628949, 2.0, 7.5, -24, 0, ())]),
    # wind moving through large trees, leaves rustling
    'rock': (7.5, [(858679, 116.0, 7.5, -12, 0, ('highpass', 120))]),
    # the gate standing ajar: one old wooden gate on its hinges
    'gate': (5.2, [(456763, 0.2, 5.0, -10, 0, ())]),
    # ducks on the pond, lapping water, a wren singing above
    'mandarin-duck': (7.0, [(263104, 40.0, 7.0, -13, 0, ('highpass', 150)), (318064, 31.0, 7.0, -23, 0, ()), (683402, 0.25, 6.0, -19, 0.6, ('highpass', 1500))]),
    # three peacock calls
    'peacocks': (6.2, [(810711, 1.0, 6.2, -10, 0, ())]),
    # the watering vessel emptying; a girl laughing softly, another's quiet chuckle
    'watering': (7.0, [(532890, 4.0, 7.0, -12, 0, ()), (402395, 0.0, 3.0, -19, 1.0, ('highpass', 200)), (377742, 0.5, 1.6, -20, 4.8, ('highpass', 200))]),
    # a branch broken off, one soft gust
    'flowers': (5.6, [(452109, 0.0, 2.8, -9, 0.9, ()), (181251, 8.0, 5.6, -20, 0, ('highpass', 100))]),
    # hair brushed out, ornaments picked up, a golden oriole whistling outside
    'toilette': (7.5, [(452534, 1.0, 7.0, -15, 0, ()), (349361, 2.6, 2.2, -19, 3.6, ()), (737205, 19.0, 7.5, -13, 0, ('highpass', 700))]),
    # a lively zheng passage, silk and bare feet under it
    'dance': (7.8, [(546978, 39.5, 7.8, -9, 0, ('highpass', 70)), (530105, 0.6, 7.8, -19, 0, ())]),
    # pipa and zheng playing together (the zheng raised 45 cents to the pipa's pitch)
    'ensemble': (7.8, [(546977, 37.0, 7.8, -9, 0, ('highpass', 90)), (546978, 5.6, 7.8, -14, 0, ('pitch', 45, 'highpass', 70))]),
    # a small meow, slow purring (the recording slowed to 82%), and the meow once more
    'cat': (7.4, [(463790, 6.5, 7.4, -13, 0, (), 0.82), (418160, 2.0, 2.2, -14, 0.3, ()), (418160, 2.0, 2.2, -15, 3.3, ())]),
    # the cloth cover drawn back, then the qin itself
    'qin': (7.6, [(161905, 18.0, 5.2, -10, 2.4, ('highpass', 100, 'lowpass', 6500)), (624477, 2.0, 3.0, -17, 0, ())]),
    # a game on the grass: three girls giggling, hands rustling through the grass
    'doucao': (7.5, [(342838, 0.5, 7.5, -12, 0, ('highpass', 200)), (636945, 10.0, 7.5, -17, 0, ('highpass', 300)), (594510, 0.5, 5.0, -18, 1.2, ('highpass', 300))]),
    # a page turned, a pause, another page; a quiet zheng in the background
    'reading': (7.8, [(365542, 1.1, 1.1, -12, 0.5, ()), (365542, 4.2, 1.0, -13, 3.5, ()), (365542, 5.5, 1.0, -13, 6.4, ()), (546978, 19.5, 7.8, -17, 0, ('highpass', 70))]),
    # the parrot on the railing
    'parrot': (5.5, [(187928, 0.25, 5.5, -13, 0, ())]),
    # three stones set down, unhurried; two short passages of young women murmuring
    # (only the higher-pitched passages of the recording; the lower voice is left out)
    'go': (7.8, [(588317, 0.0, 0.9, -8, 0.5, ()), (588317, 2.7, 0.8, -9, 3.3, ()), (588317, 5.95, 0.9, -8, 6.2, ()), (482822, 5.2, 3.2, -23, 0.2, ('highpass', 250, 'lowpass', 1800)), (482822, 42.2, 3.4, -23, 4.2, ('highpass', 250, 'lowpass', 1800))]),
    # a baby laughing
    'infants': (6.0, [(461789, 0.25, 6.0, -11, 0, ())]),
    # the needle through taut cloth, a girl laughing softly now and then
    'embroidery': (7.0, [(456772, 1.0, 7.0, -8, 0, ()), (218308, 0.0, 7.0, -20, 0, ('highpass', 200, 'lowpass', 6000))]),
    # coals in the pan, cloth shaken out
    'ironing': (6.5, [(471161, 0.0, 5.8, -12, 0, ()), (844390, 0.0, 6.4, -14, 0.1, ('highpass', 150, 'lowpass', 7000))]),
    # the harp, and the clappers keeping time
    'harp': (6.4, [(415476, 0.0, 5.5, -10, 0, ()), (222145, 0.0, 0.31, -17, 0.9, ()), (222145, 0.0, 0.31, -18, 2.4, ()), (222145, 0.0, 0.31, -17, 3.9, ())]),
    # two unhurried brush strokes; a room of girls talking
    'portrait': (7.5, [(729108, 4.5, 1.8, -12, 0.6, ()), (729108, 9.5, 1.8, -13, 4.4, ()), (675805, 20.0, 7.5, -14, 0, ('highpass', 200, 'lowpass', 5500))]),
    # a light wind in the leaves
    'fan-chase': (5.0, [(751473, 40.0, 5.0, -12, 0, ('highpass', 100))]),
}


def check_unique():
    seen = {}
    for name, (_, layers) in RECIPES.items():
        for sid, start, dur, *_ in layers:
            for other, o_start, o_dur in seen.get(sid, []):
                if other != name and not (sid == 546978 and (start >= o_start + o_dur or o_start >= start + dur)):
                    raise SystemExit(f'{sid} is used in both {other} and {name}')
            seen.setdefault(sid, []).append((name, start, dur))


def build():
    check_unique()
    report = []
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        for name, (length, layers) in RECIPES.items():
            stems = []
            for n, (sid, start, dur, peak, offset, fx, *slow) in enumerate(layers):
                p = t / f'{name}-{n}.wav'
                fade_out = min(0.6, dur / 3)
                # an optional seventh value slows the recording (0.82 = 82% speed, same pitch);
                # dur is the length after slowing
                tempo = slow[0] if slow else 1
                sox(raw(sid), '-r', 48000, '-c', 1, '-b', 32, p, 'trim', start, dur * tempo,
                    *(('tempo', tempo) if slow else ()), *fx,
                    'gain', '-n', peak, 'fade', 't', min(0.15, dur / 4), dur, fade_out,
                    'pad', offset, max(0, length - offset - dur))
                stems.append(p)
            work = t / f'{name}-mix.wav'
            if len(stems) == 1:
                sox(stems[0], work, 'trim', 0, length)
            else:
                # -m scales each input by 1/n; the loudness pass below restores the level
                sox('-m', *stems, work, 'trim', 0, length)
            asset_target = TARGET - 20 * math.log10(PLAY_GAIN)
            # tame isolated transients only when they stop the clip reaching the target level
            for attempt in range(8):
                m = meter.measure(work)
                if math.isnan(m['lufs']):          # too sparse for the gated meter: leave to the peak limit
                    break
                excess = m['peak'] + (asset_target - m['lufs']) + 3
                if excess <= .15:
                    break
                threshold = m['peak'] - max(8, excess * 1.6)
                squeezed = t / f'{name}-c{attempt}.wav'
                sox(work, squeezed, 'compand', '0,.09',
                    f'-100,-100,{threshold:.3f},{threshold:.3f},0,{threshold * .75:.3f}', '0', '-90', '.004')
                work = squeezed
            m = meter.measure(work)
            final = t / f'{name}-final.wav'
            gain = -3 - m['peak'] if math.isnan(m['lufs']) else min(asset_target - m['lufs'], -3 - m['peak'])
            sox(work, final, 'gain', gain, 'fade', 't', .05, length, .5)
            out = OUT / f'han-{name}'
            sox(final, '-C', 5, out.with_suffix('.ogg'))
            subprocess.run(['afconvert', '-f', 'm4af', '-d', 'aac', '-b', '96000', str(final), str(out.with_suffix('.m4a'))],
                           check=True, stderr=subprocess.DEVNULL)
            report.append(dict(id=name, file=out.name, gain=PLAY_GAIN, **meter.measure(out.with_suffix('.ogg'), PLAY_GAIN)))
    for r in report:
        print(r)
    return report


if __name__ == '__main__':
    qa = ROOT / 'research/han-palace-proposal/SOUND_LEVELS.json'
    qa.write_text(json.dumps(build(), indent=2))
