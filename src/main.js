import { paintings, livePainting } from './paintings/index.js';
import { createGallery } from './gallery/gallery.js';
import { createExplore } from './explore/explore.js';
import { createTransition } from './transitions/enter.js';

const root = document.querySelector('.world');
const explore = createExplore(root, livePainting.scene, livePainting.scene.stories);
let transition;
const gallery = createGallery(root, paintings, { onEnter: () => transition.enter() });
transition = createTransition({ root, live: gallery.live, stage: explore, onLayout: gallery.layoutLive });

document.querySelector('.leave').addEventListener('click', () => transition.leave());
addEventListener('keydown', (e) => {
  if (e.key !== 'Escape') return;
  if (explore.open) explore.hide();
  else transition.leave();
});

// dev only: a handle for the console, and ?shot=inside[&story=n] for screenshots
if (import.meta.env.DEV) {
  window.__painting = { explore, transition };
  const q = new URLSearchParams(location.search);
  if (q.has('shot')) root.classList.add('is-still');
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
