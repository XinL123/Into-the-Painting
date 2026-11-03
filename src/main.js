import { reducedMotion } from './motion.js';
import { paintings, livePainting, music as musicTracks } from './paintings/index.js';
import { createGallery } from './gallery/gallery.js';
import { createExplore } from './explore/explore.js';
import { createTransition } from './transitions/enter.js';
import { createAbout } from './gallery/about.js';
import { createMusic } from './gallery/music.js';
import { createMusicPlayer } from './gallery/music-player.js';

const root = document.querySelector('.world');
root.classList.toggle('is-reduced-motion', reducedMotion);
let active = null;
let musicPlayer;
const music = createMusic(root, musicTracks, {
  controls: true, autoplay: false, onChange: () => musicPlayer?.refresh(),
});
musicPlayer = createMusicPlayer(root, music);
const about = createAbout(root);
const gallery = createGallery(root, paintings, { onEnter: (live) => activate(live)?.transition.enter() });

function activate(live) {
  if (active || root.classList.contains('is-leaving')) return null;
  const p = live.painting;
  root.dataset.painting = p.id;
  const view = root.querySelector('.explore');
  view.setAttribute('aria-label', `${p.title.en}, a stretch of the scroll`);
  const note = root.querySelector('.inside-note');
  const title = document.createElement('i'); title.textContent = p.title.en;
  note.replaceChildren(title, document.createTextNode(` · ${p.artist.en}, ${p.period.en} · ${p.collection.en}`));
  const explore = createExplore(root, p.scene, p.scene.stories, {
    // Gallery music and project foley have independent visitor preferences.
    // Only an explicit project-speaker mute carries into another project.
    entranceImage: live.img,
  });
  const transition = createTransition({
    root, live, stage: explore, onLayout: gallery.layoutLive,
    onEnter: () => music.suspend(),
    onLeaveDone: () => {
      explore.destroy(); transition.destroy(); active = null;
      delete root.dataset.painting;
      music.resume();
      live.opening.focus({ preventScroll: true });
    },
  });
  active = { painting: p, explore, transition };
  return active;
}

document.querySelector('.leave').addEventListener('click', () => active?.transition.leave());
addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (about.open) about.hide();
  else if (active?.explore.open) active.explore.hide();
  else active?.transition.leave();
});

// Dev-only direct views keep the selected painting explicit. Production entry
// remains the same gallery, with no new navigation or UI for test settings.
if (import.meta.env.DEV) {
  window.__painting = { get explore() { return active?.explore; }, get transition() { return active?.transition; }, get painting() { return active?.painting; }, about, music };
  const q = new URLSearchParams(location.search);
  if (q.has('shot')) root.classList.add('is-still');
  if (q.get('shot') === 'about') about.show();
  if (q.has('hover')) document.querySelectorAll('.opening')[Number(q.get('hover'))]?.classList.add('is-hover');
  if (q.get('shot') === 'inside') {
    const live = gallery.lives.get(q.get('painting') ?? livePainting.id) ?? gallery.lives.get(livePainting.id);
    const selected = activate(live);
    selected.explore.ready.then(() => {
      music.suspend(); selected.transition.adopt();
      root.classList.add('is-on', 'is-inside');
      selected.explore.start(); selected.explore.wake();
      if (q.has('story')) selected.explore.show(Number(q.get('story')));
      if (q.has('thumb')) document.querySelectorAll('.progress-dot')[Number(q.get('thumb'))]?.classList.add('is-hover');
    });
  }
}
