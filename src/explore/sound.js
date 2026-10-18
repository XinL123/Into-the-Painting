// A sound for a moment. When a story comes forward its clip fades in a beat
// after the spotlight; leaving the story, or choosing the next one, fades it
// out. One clip at a time, through a single gain that the mute control holds.
//
// Web Audio rather than <audio>: fades are sample-accurate and loops are
// gapless. The context is made on the first play, which always follows a
// click, so the browser's autoplay rule is satisfied.
const FADE_IN = 0.4;
const FADE_OUT = 0.6;
const MUTE_KEY = 'painting.sound';

// the first format this browser plays; files ship as m4a (Safari) and ogg
const probe = document.createElement('audio');
const FORMAT = ['m4a', 'ogg'].find((f) =>
  probe.canPlayType(f === 'm4a' ? 'audio/mp4; codecs="mp4a.40.2"' : 'audio/ogg; codecs="vorbis"') !== '') ?? 'ogg';

export function createSound(files, { onMuteChange } = {}) {
  let ctx = null, master = null;
  let current = null;                       // { id, source, gain }
  const buffers = {};                       // id -> AudioBuffer (decoded on first use)
  const bytes = {};                         // id -> Promise<ArrayBuffer> (fetched early)
  let muted = false;
  try { muted = localStorage.getItem(MUTE_KEY) === 'off'; } catch {}

  function context() {
    if (ctx) return ctx;
    ctx = new (window.AudioContext || window.webkitAudioContext)();
    master = ctx.createGain();
    master.gain.value = muted ? 0 : 1;
    master.connect(ctx.destination);
    return ctx;
  }

  // start fetching the bytes in the background; decoding waits for the context
  function preload(id) {
    const url = files[id]?.[FORMAT];
    if (!url || bytes[id]) return;
    bytes[id] = fetch(url).then((r) => r.arrayBuffer()).catch(() => null);
  }
  async function buffer(id) {
    if (buffers[id]) return buffers[id];
    preload(id);
    const data = await bytes[id];
    if (!data) return null;
    buffers[id] = await context().decodeAudioData(data.slice(0));
    return buffers[id];
  }

  function stop(fade = FADE_OUT) {
    if (!current) return;
    const { source, gain } = current;
    current = null;
    const now = ctx.currentTime;
    gain.gain.cancelScheduledValues(now);
    gain.gain.setValueAtTime(gain.gain.value, now);
    gain.gain.linearRampToValueAtTime(0, now + fade);
    try { source.stop(now + fade + 0.05); } catch {}
  }

  // play a story's sound: { file, mode: 'once' | 'loop', gain? }
  async function play(sound, delay = 0) {
    stop();
    if (!sound || !files[sound.file]) return;
    const token = { id: sound.file };
    current = token;
    const ac = context();
    if (ac.state === 'suspended') ac.resume();
    const buf = await buffer(sound.file);
    if (current !== token || !buf) return;        // another story came, or the file failed
    const source = ac.createBufferSource();
    source.buffer = buf;
    source.loop = sound.mode === 'loop';
    const gain = ac.createGain();
    const at = ac.currentTime + delay;
    gain.gain.setValueAtTime(0, at);
    gain.gain.linearRampToValueAtTime(sound.gain ?? 1, at + FADE_IN);
    source.connect(gain).connect(master);
    source.start(at);
    source.onended = () => { if (current === token) current = null; };
    Object.assign(token, { source, gain });
  }

  function setMuted(v) {
    muted = v;
    try { localStorage.setItem(MUTE_KEY, v ? 'off' : 'on'); } catch {}
    if (master) {
      const now = ctx.currentTime;
      master.gain.cancelScheduledValues(now);
      master.gain.setValueAtTime(master.gain.value, now);
      master.gain.linearRampToValueAtTime(v ? 0 : 1, now + 0.25);
    }
    onMuteChange?.(v);
  }

  // quiet while the tab is away
  document.addEventListener('visibilitychange', () => {
    if (!ctx) return;
    if (document.hidden) ctx.suspend(); else if (current) ctx.resume();
  });

  return {
    play, stop, preload,
    get muted() { return muted; },
    setMuted,
    toggle() { setMuted(!muted); },
    // dev: what is sounding right now
    state() { return { playing: current?.id ?? null, context: ctx?.state ?? 'none', master: master?.gain.value ?? null, format: FORMAT }; },
  };
}
