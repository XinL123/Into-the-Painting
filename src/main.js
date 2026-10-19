import { paintings, livePainting, music as musicTracks } from './paintings/index.js';
import { createGallery } from './gallery/gallery.js';
import { createExplore } from './explore/explore.js';
import { createTransition } from './transitions/enter.js';
import { createAbout } from './gallery/about.js';
import { createMusic } from './gallery/music.js';

const root = document.querySelector('.world');
const explore = createExplore(root, livePainting.scene, livePainting.scene.stories);
let transition;
const gallery = createGallery(root, paintings, { onEnter: () => transition.enter() });
const music = createMusic(root, musicTracks, { toggle: root.querySelector('.sound-toggle--gallery') });
transition = createTransition({
  root, live: gallery.live, stage: explore, onLayout: gallery.layoutLive,
  onEnter: () => music.suspend(),
  onLeave: () => music.resume(),
});
const about = createAbout(root);

document.querySelector('.leave').addEventListener('click', () => transition.leave());
addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (about.open) about.hide();
  else if (explore.open) explore.hide();
  else transition.leave();
});

// dev only: a handle for the console, and ?shot=inside[&story=n] for screenshots
if (import.meta.env.DEV) {
  window.__painting = { explore, transition, about, music };
  const q = new URLSearchParams(location.search);
  if (q.has('shot')) root.classList.add('is-still');
  if (q.get('shot') === 'about') about.show();
  if (q.has('hover')) document.querySelectorAll('.opening')[Number(q.get('hover'))]?.classList.add('is-hover');
  if (q.get('shot') === 'inside') {
    explore.ready.then(() => {
      root.classList.add('is-on', 'is-inside');
      explore.start();
      explore.wake();
      if (q.has('story')) explore.show(Number(q.get('story')));
      if (q.has('thumb')) document.querySelectorAll('.progress-dot')[Number(q.get('thumb'))]?.classList.add('is-hover');
    });
  }
}
