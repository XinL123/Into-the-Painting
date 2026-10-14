// Entering and leaving the painting, as one continuous move.
//
//   enter:  the brushed opening spreads until it is the whole view, carrying the
//           same image from its gallery frame to the scroll's resting frame; the
//           gallery fades; the exploration canvas takes over underneath, showing
//           the very same picture; then its marks appear.
//   leave:  the same, backwards.
import gsap from 'gsap';

const lerp = (a, b, t) => a + (b - a) * t;
const lerpRect = (a, b, t) => ({
  left: lerp(a.left, b.left, t),
  top: lerp(a.top, b.top, t),
  width: lerp(a.width, b.width, t),
  height: lerp(a.height, b.height, t),
});
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const T = reducedMotion ? 0.35 : 1;

export function createTransition({ root, live, stage, onLayout, onEnter, onLeave }) {
  const { opening, ink, img } = live;
  let from = null;          // gallery geometry captured at the moment of entering
  let timeline = null;
  let inside = false;
  const travel = { p: 0 };

  function place() {
    const p = travel.p;
    // The opening grows past the view so its brushed edge leaves the screen still
    // looking brushed; it never outgrows the picture it shows.
    const big = {
      left: -0.34 * innerWidth, top: -0.3 * innerHeight,
      width: 1.75 * innerWidth, height: 1.6 * innerHeight,
    };
    const pic = lerpRect(from.img, stage.restRect(), p);
    const want = lerpRect(from.box, big, p);
    const left = Math.max(want.left, pic.left);
    const top = Math.max(want.top, pic.top);
    const box = {
      left, top,
      width: Math.min(want.left + want.width, pic.left + pic.width) - left,
      height: Math.min(want.top + want.height, pic.top + pic.height) - top,
    };
    Object.assign(opening.style, {
      left: `${box.left}px`, top: `${box.top}px`, width: `${box.width}px`, height: `${box.height}px`,
    });
    Object.assign(img.style, {
      left: `${pic.left - box.left}px`, top: `${pic.top - box.top}px`,
      width: `${pic.width}px`, height: `${pic.height}px`,
    });
    // in the last stretch the stroke itself swells, taking its ragged ends off screen
    const t = Math.min(1, Math.max(0, (p - 0.86) / 0.14));
    const size = 100 + 90 * t * t * (3 - 2 * t);
    ink.style.maskSize = ink.style.webkitMaskSize = `${size}% ${size}%`;
    ink.style.maskPosition = ink.style.webkitMaskPosition = '44% 50%';
  }

  function enter() {
    if (inside || timeline?.isActive()) return;
    inside = true;
    const b = opening.getBoundingClientRect();
    const i = img.getBoundingClientRect();
    from = {
      box: { left: b.left, top: b.top, width: b.width, height: b.height },
      img: { left: i.left, top: i.top, width: i.width, height: i.height },
    };
    root.classList.add('is-entering');
    opening.classList.add('is-travelling');
    stage.measure();
    travel.p = 0;
    place();
    onEnter?.();

    timeline = gsap.timeline()
      .to(travel, { p: 1, duration: 1.7 * T, ease: 'power2.inOut', onUpdate: place })
      // wait for the layers if they are still loading; the flat image simply stays
      .add(() => {
        timeline.pause();
        stage.ready.then(() => {
          stage.measure();
          place();
          root.classList.add('is-on');
          stage.start();
          timeline.resume();
        });
      })
      .to(opening, { opacity: 0, duration: 0.7 * T, ease: 'power1.inOut' }, '+=0.05')
      .add(() => {
        root.classList.remove('is-entering');
        root.classList.add('is-inside');
      })
      // a beat of looking at the painting itself, then the marks come up
      .add(() => stage.wake(), '+=0.9');
  }

  // Leaving is a quiet return, not the entrance played backwards: the scroll
  // settles and fades, the gallery is simply there again.
  function leave() {
    if (!inside) return;
    inside = false;
    timeline?.kill();
    onLeave?.();
    root.classList.remove('is-inside', 'is-entering');
    root.classList.add('is-leaving');
    // put the opening straight back in its place, hidden, ready to fade in with the rest
    opening.classList.remove('is-travelling');
    for (const k of ['left', 'top', 'width', 'height']) opening.style[k] = '';
    const { x, y, w, h } = live.painting.place;
    Object.assign(opening.style, { left: `${x}%`, top: `${y}%`, width: `${w}%`, height: `${h}%`, opacity: 1 });
    ink.style.maskSize = ink.style.webkitMaskSize = '';
    ink.style.maskPosition = ink.style.webkitMaskPosition = '';
    onLayout();
    stage.sleep(0.9 * T);
    timeline = gsap.timeline()
      .to(root.querySelector('.explore'), { opacity: 0, duration: 0.9 * T, ease: 'power1.inOut' })
      .add(() => {
        stage.stop();
        root.classList.remove('is-on', 'is-leaving');
        gsap.set(root.querySelector('.explore'), { clearProps: 'opacity' });
      });
  }

  addEventListener('resize', () => {
    if (inside && travel.p === 1) place();
  });

  // dev: freeze the travel at p (0 gallery .. 1 full view)
  function pose(p) {
    const b = opening.getBoundingClientRect();
    const i = img.getBoundingClientRect();
    from = {
      box: { left: b.left, top: b.top, width: b.width, height: b.height },
      img: { left: i.left, top: i.top, width: i.width, height: i.height },
    };
    root.classList.add('is-entering');
    opening.classList.add('is-travelling');
    stage.measure();
    travel.p = p;
    place();
  }

  return { enter, leave, pose, get inside() { return inside; } };
}
