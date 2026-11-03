// Three pieces stream in the gallery. Exploration suspends background music
// while its scene foley remains available with an independent mute preference.
// Plain <audio>, as the Mercury
// playground does it: long tracks stream rather than decode in one piece.
const FADE_MS = 700;

export function createMusic(root, tracks, { toggle, onEnabledChange, onChange, controls = false, autoplay = true }) {
  const audio = new Audio();
  audio.preload = 'none';
  let i = 0;
  let on = autoplay;              // the direct gallery controls start paused
  let suspended = false;          // inside the painting
  let fade = 0;
  let level = 1;
  let blocked = false;
  let volume = 1;
  let request = 0;

  function reflect() {
    toggle?.classList.toggle('is-muted', !on || blocked || volume === 0);
    if (!controls) toggle?.setAttribute('aria-pressed', String(on));
    toggle?.setAttribute('aria-label', controls ? 'Music player' : on ? (blocked ? 'Play music' : 'Music on') : 'Music off');
    onChange?.();
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
    if (!on || suspended || !tracks.length) return false;
    const turn = ++request;
    if (!audio.src) load(i);
    // Request audible playback. Starting at zero can be treated as muted
    // autoplay and then paused by the browser when the fade becomes audible.
    if (audio.paused) audio.volume = Math.min(0.08, level * volume);
    try { await audio.play(); } catch { if (turn === request) { blocked = true; reflect(); } return false; }
    if (turn !== request) return false;
    // A pending play can resolve after the visitor muted or entered a painting.
    if (!on || suspended) { audio.pause(); return false; }
    blocked = false;
    reflect();
    ramp(level * volume);
    return true;
  }

  function stop() {
    ramp(0, () => audio.pause());
  }

  function select(n, { play = on } = {}) {
    if (!tracks.length || !Number.isInteger(n)) return;
    request++;
    clearInterval(fade);
    audio.pause();
    load(n);
    try { audio.currentTime = 0; } catch {}
    on = play;
    blocked = false;
    reflect();
    if (on && !suspended) start();
  }
  audio.addEventListener('ended', () => select(i + 1));

  function setEnabled(value) {
    if (on === value) return;
    on = value;
    reflect();
    if (on && !suspended) start();
    else if (!on) stop();
    onEnabledChange?.(on);
  }

  toggle?.addEventListener('click', (e) => {
    e.stopPropagation();
    if (controls) return; // the popup owns this button in the gallery UI
    // A refused autoplay request is not a visitor mute. The first speaker
    // click should play the music, rather than turn an inaudible track off.
    if (on && blocked) { start(); return; }
    setEnabled(!on);
  });

  // Autoplay permission is separate from the visitor's sound preference.
  // Retry after a gesture without changing the switch or storing a false mute.
  const unlock = (e) => {
    // Speakers own their click, so pointerdown cannot unlock and then have the
    // same click immediately mute again. Other gallery gestures unlock early.
    if (e.target?.closest?.('.sound-toggle, .music-player')) return;
    if (on && !suspended && audio.paused) start();
  };
  const gestures = root.ownerDocument ?? root;
  for (const name of ['pointerdown', 'click', 'touchend', 'keydown']) gestures.addEventListener(name, unlock, { capture: true });
  reflect();
  if (on) start();

  return {
    setEnabled,
    play() { if (!on) setEnabled(true); else start(); },
    pause() { setEnabled(false); },
    select,
    next() { select(i + 1); },
    previous() { select(i - 1); },
    setVolume(value) {
      if (!Number.isFinite(value)) return;
      volume = Math.max(0, Math.min(1, value));
      if (on && !suspended) ramp(level * volume);
      reflect();
    },
    setLevel(value) { level = Math.max(0, Math.min(1, value)); if (on && !suspended) start(); },
    suspend() { suspended = true; if (on) stop(); },
    resume() { suspended = false; if (on) start(); },
    get on() { return on; },
    // dev: what is sounding, and the element itself
    audio,
    state() { return { on, blocked, suspended, index: i, count: tracks.length, volumeLevel: volume, track: tracks[i]?.split('/').pop(), paused: audio.paused, volume: audio.volume, time: audio.currentTime }; },
  };
}
