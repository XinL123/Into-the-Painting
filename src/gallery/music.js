// Music for the gallery, and only the gallery: three pieces played in order,
// round and round, behind the paintings. The speaker in the top right turns it
// on and off (the user's choice is remembered); entering the painting fades it
// out, leaving brings it back if it was on. Plain <audio>, as the Mercury
// playground does it: long tracks stream rather than decode in one piece.
const KEY = 'painting.music';
const FADE_MS = 700;

export function createMusic(root, tracks, { toggle }) {
  const audio = new Audio();
  audio.preload = 'none';
  let i = 0;
  let on = false;                 // the user wants music
  let suspended = false;          // inside the painting
  let fade = 0;
  try { on = localStorage.getItem(KEY) === 'on'; } catch {}

  function reflect() {
    toggle.classList.toggle('is-muted', !on);
    toggle.setAttribute('aria-pressed', String(on));
    toggle.setAttribute('aria-label', on ? 'Music on' : 'Music off');
  }

  function ramp(to, done) {
    clearInterval(fade);
    const from = audio.volume;
    const t0 = performance.now();
    fade = setInterval(() => {
      const t = Math.min(1, (performance.now() - t0) / FADE_MS);
      audio.volume = from + (to - from) * t;
      if (t === 1) { clearInterval(fade); done?.(); }
    }, 40);
  }

  function load(n) {
    i = (n + tracks.length) % tracks.length;
    audio.src = tracks[i];
  }

  // start (or continue) the current track; false if the browser refused
  async function start() {
    if (!audio.src) load(i);
    audio.volume = 0;
    try { await audio.play(); } catch { return false; }
    ramp(1);
    return true;
  }

  function stop() {
    ramp(0, () => audio.pause());
  }

  audio.addEventListener('ended', () => { load(i + 1); if (on && !suspended) start(); });

  toggle.addEventListener('click', async (e) => {
    e.stopPropagation();
    on = !on;
    if (on && !suspended) on = await start();
    else if (!on) stop();
    try { localStorage.setItem(KEY, on ? 'on' : 'off'); } catch {}
    reflect();
  });

  // a remembered "on" can only sound after a gesture; try, and show the truth
  reflect();
  if (on) start().then((ok) => { if (!ok) { on = false; reflect(); } });

  return {
    suspend() { suspended = true; if (on) stop(); },
    resume() { suspended = false; if (on) start(); },
    get on() { return on; },
    // dev: what is sounding, and the element itself
    audio,
    state() { return { on, suspended, track: tracks[i]?.split('/').pop(), paused: audio.paused, volume: audio.volume, time: audio.currentTime }; },
  };
}
