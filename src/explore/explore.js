// The exploration canvas: a long stretch of the original scroll, unrolled by
// dragging, with a few quiet marks. Choosing a mark draws the view in toward one
// small moment: the rest of the scroll falls back into shadow, the moment comes
// forward at full resolution, and a short story appears beside it.
//
// The picture is drawn onto a viewport-sized canvas, only the part in view, so
// the browser never has to hold a 16,000-pixel-wide layer.
import gsap from 'gsap';

const BAND = 0.86;            // the scroll's height as a share of the window at rest
const START_AT = 0.6;         // the bridge sits this far across the window at rest
const MAX_ZOOM = 1.7;         // 1 = one master pixel per CSS pixel; small moments may be shown larger
const VEIL = 'rgb(42, 35, 25)';
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const loadImage = (url) => new Promise((resolve, reject) => {
  const img = new Image();
  img.decoding = 'async';
  img.onload = () => resolve(img);
  img.onerror = reject;
  img.src = url;
});

export function createExplore(root, scene, stories, { onStoryChange } = {}) {
  const { width: W, height: H, rect, focus } = scene;     // picture units = master px
  const view = root.querySelector('.explore');
  const canvas = root.querySelector('.explore-canvas');
  const ctx = canvas.getContext('2d');
  const marksRoot = root.querySelector('.explore-marks');
  const card = root.querySelector('.story');
  const progress = root.querySelector('.progress');

  const t = { x: 0, y: 0, s: 1 };          // picture -> screen: sx = x + px * s
  let rest = { x: 0, y: 0, s: 1 };
  let vw = 1, vh = 1, dpr = 1;
  let active = false;
  let open = null;                         // index of the story being looked at
  let drag = null;
  let tween = null;
  let picture = null;
  const details = {};
  // the spotlight: where it is (picture px) and how far it has come up
  const look = { amt: 0, detail: 0, cx: 0, cy: 0, rx: 1, ry: 1, angle: 0, id: null };
  let raf = 0;

  const toPic = (v) => v - rect.left;      // master x -> picture x
  const toPicY = (v) => v - rect.top;

  // ---- marks and progress ----
  const marks = stories.map((story, i) => {
    const [x0, y0, x1, y1] = story.box;
    const m = el('button', 'mark');
    m.type = 'button';
    m.style.setProperty('--i', i);
    m.setAttribute('aria-label', story.title);
    m.append(el('span', 'mark-dot'), el('span', 'mark-label', story.title));
    m.addEventListener('click', (e) => { e.stopPropagation(); show(i); });
    marksRoot.append(m);
    // the same moment in the row at the bottom, with a glimpse of it on hover
    const dot = el('button', 'progress-dot');
    dot.type = 'button';
    dot.setAttribute('aria-label', story.title);
    const thumb = el('span', 'progress-thumb');
    const img = el('img');
    img.alt = '';
    img.draggable = false;
    img.loading = 'lazy';
    const d = scene.details[story.id];
    if (d) {
      img.src = d.url;
      // centre the glimpse on the story's box within its detail crop
      const [dx0, dy0, dx1, dy1] = d.rect;
      img.style.objectPosition = `${((x0 + x1) / 2 - dx0) / (dx1 - dx0) * 100}% ${((y0 + y1) / 2 - dy0) / (dy1 - dy0) * 100}%`;
    }
    thumb.append(img, el('span', null, story.title));
    dot.append(thumb);
    dot.addEventListener('click', (e) => { e.stopPropagation(); show(i); });
    progress.append(dot);
    return { el: m, dot, story, px: toPic((x0 + x1) / 2), py: toPicY((y0 + y1) / 2) };
  });

  // ---- drawing ----
  function schedule() {
    if (!raf) raf = requestAnimationFrame(() => { raf = 0; draw(); });
  }
  function draw() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, vw, vh);
    if (picture) {
      // only the part of the picture that is in view
      const k = picture.naturalWidth / W;
      const px0 = clamp(-t.x / t.s, 0, W), px1 = clamp((vw - t.x) / t.s, 0, W);
      const py0 = clamp(-t.y / t.s, 0, H), py1 = clamp((vh - t.y) / t.s, 0, H);
      if (px1 > px0 && py1 > py0) {
        ctx.imageSmoothingQuality = 'high';
        ctx.drawImage(picture, px0 * k, py0 * k, (px1 - px0) * k, (py1 - py0) * k,
          t.x + px0 * t.s, t.y + py0 * t.s, (px1 - px0) * t.s, (py1 - py0) * t.s);
      }
    }
    if (look.amt > 0.001) {
      // the rest of the scroll falls back
      const cx = t.x + look.cx * t.s, cy = t.y + look.cy * t.s;
      const rx = look.rx * t.s, ry = look.ry * t.s;
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(look.angle);
      ctx.scale(1, ry / rx);
      const g = ctx.createRadialGradient(0, 0, rx * 0.45, 0, 0, rx);
      g.addColorStop(0, 'rgba(42,35,25,0)');
      g.addColorStop(1, `rgba(42,35,25,${0.6 * look.amt})`);
      ctx.fillStyle = g;
      const big = (vw + vh) * 2;
      ctx.fillRect(-big, -big * rx / ry, big * 2, big * 2 * rx / ry);
      ctx.restore();
      // the moment itself, at full resolution, within a soft edge
      const d = details[look.id];
      if (d && look.detail > 0.001) {
        const [dx0, dy0, dx1, dy1] = d.rect;
        const sx = t.x + toPic(dx0) * t.s, sy = t.y + toPicY(dy0) * t.s;
        const sw = (dx1 - dx0) * t.s, sh = (dy1 - dy0) * t.s;
        const off = offscreen(Math.ceil(sw * dpr), Math.ceil(sh * dpr));
        const o = off.getContext('2d');
        o.setTransform(dpr, 0, 0, dpr, 0, 0);
        o.clearRect(0, 0, sw, sh);
        o.imageSmoothingQuality = 'high';
        o.filter = 'brightness(1.05) saturate(1.08)';
        o.drawImage(d.img, 0, 0, sw, sh);
        o.filter = 'none';
        o.globalCompositeOperation = 'destination-in';
        o.save();
        o.translate(cx - sx, cy - sy);
        o.rotate(look.angle);
        o.scale(1, ry / rx);
        const m = o.createRadialGradient(0, 0, rx * 0.5, 0, 0, rx * 0.9);
        m.addColorStop(0, `rgba(0,0,0,${look.detail})`);
        m.addColorStop(1, 'rgba(0,0,0,0)');
        o.fillStyle = m;
        o.fillRect(-sw * 2, -sh * 2 * rx / ry, sw * 5, sh * 5 * rx / ry);
        o.restore();
        o.globalCompositeOperation = 'source-over';
        ctx.drawImage(off, 0, 0, off.width, off.height, sx, sy, sw, sh);
      }
    }
    // marks follow the picture
    for (const m of marks) {
      m.el.style.transform = `translate(${t.x + m.px * t.s}px, ${t.y + m.py * t.s}px)`;
    }
  }
  let offCanvas = null;
  function offscreen(w, h) {
    if (!offCanvas) offCanvas = document.createElement('canvas');
    if (offCanvas.width !== w || offCanvas.height !== h) { offCanvas.width = w; offCanvas.height = h; }
    return offCanvas;
  }

  // ---- transform ----
  function limits(s) {
    const w = W * s, h = H * s;
    // the paper beyond the picture's top and bottom edges never shows: a moment
    // near an edge sits off-centre instead
    return {
      xmin: Math.min(0, vw - w), xmax: Math.max(0, vw - w),
      ymin: Math.min((vh - h) / 2, vh - h), ymax: Math.max((vh - h) / 2, 0),
    };
  }
  function clampT(o) {
    const L = limits(o.s);
    o.x = clamp(o.x, L.xmin, L.xmax);
    o.y = clamp(o.y, L.ymin, L.ymax);
    return o;
  }
  function measure() {
    vw = innerWidth; vh = innerHeight;
    dpr = Math.min(devicePixelRatio || 1, 2);
    canvas.width = Math.round(vw * dpr);
    canvas.height = Math.round(vh * dpr);
    const s = (vh * BAND) / H;
    rest = clampT({ s, x: vw * START_AT - focus.x * W * s, y: (vh - H * s) / 2 });
    if (!active || open == null) Object.assign(t, rest);
    else frame(open, 0);
    draw();
  }
  const restRect = () => ({ left: rest.x, top: rest.y, width: W * rest.s, height: H * rest.s });

  // ---- looking closer ----
  function frame(i, duration = 1.4) {
    const [x0, y0, x1, y1] = stories[i].box;
    const bw = x1 - x0, bh = y1 - y0;
    // a tall, thin moment (the pole) may fill more of the window's height
    const share = bh > 2.5 * bw ? 0.8 : 0.6;
    // close enough to see the moment, and at least close enough that the picture
    // fills the window's height, so no paper shows above or below it
    const fill = vh / H;
    const s = clamp(Math.min((vh * share) / bh, (vw * 0.46) / bw), Math.max(rest.s * 1.5, fill), MAX_ZOOM);
    const cx = toPic((x0 + x1) / 2), cy = toPicY((y0 + y1) / 2);
    // the story card takes the side of the window the moment is not on
    const side = cx * rest.s + rest.x > vw / 2 ? 'left' : 'right';
    const px = side === 'right' ? vw * 0.36 : vw * 0.64;
    // aim for the window's centre; the clamp keeps the picture's edges off screen,
    // so a moment at the bottom of the scroll sits lower in the window instead
    const target = clampT({ s, x: px - cx * s, y: vh * 0.5 - cy * s });
    card.dataset.side = side;
    tween?.kill();
    tween = gsap.to(t, { ...target, duration: reducedMotion ? 0.01 : duration, ease: 'power2.inOut', onUpdate: schedule });
    return tween;
  }

  function show(i) {
    const story = stories[i];
    const [x0, y0, x1, y1] = story.box;
    open = i;
    view.classList.add('is-looking');
    marks.forEach((m, k) => {
      m.el.classList.toggle('is-open', k === i);
      m.dot.classList.toggle('is-open', k === i);
    });

    look.id = story.id;
    look.cx = toPic((x0 + x1) / 2); look.cy = toPicY((y0 + y1) / 2);
    look.rx = story.spot?.rx ?? Math.max((x1 - x0) * 0.8, (y1 - y0) * 0.22);
    look.ry = story.spot?.ry ?? Math.max((y1 - y0) * 0.8, (x1 - x0) * 0.22);
    look.angle = ((story.spot?.angle ?? 0) * Math.PI) / 180;
    gsap.killTweensOf(look);
    gsap.to(look, { amt: 1, duration: reducedMotion ? 0.01 : 1.2, ease: 'power1.inOut', onUpdate: schedule });
    look.detail = 0;
    gsap.to(look, { detail: 1, duration: reducedMotion ? 0.01 : 0.9, delay: 0.5, ease: 'power1.inOut', onUpdate: schedule });

    card.querySelector('.story-title').textContent = story.title;
    card.querySelector('.story-body').replaceChildren(...story.text.map((p) => el('p', null, p)));
    card.querySelector('.story-count').textContent = `${i + 1} of ${stories.length}`;
    card.classList.remove('is-shown');
    frame(i).then(() => { if (open === i) card.classList.add('is-shown'); });
    onStoryChange?.(story);
  }

  function hide(duration = 1.2) {
    if (open == null) return null;
    open = null;
    view.classList.remove('is-looking');
    card.classList.remove('is-shown');
    marks.forEach((m) => { m.el.classList.remove('is-open'); m.dot.classList.remove('is-open'); });
    gsap.killTweensOf(look);
    gsap.to(look, { amt: 0, detail: 0, duration: reducedMotion ? 0.01 : 0.8, ease: 'power1.inOut', onUpdate: schedule });
    tween?.kill();
    // ease back out, but not all the way: stay where the viewer was looking
    const s = Math.max(rest.s, t.s * 0.72);
    const cx = (vw / 2 - t.x) / t.s, cy = (vh / 2 - t.y) / t.s;
    const target = clampT({ s, x: vw / 2 - cx * s, y: vh / 2 - cy * s });
    tween = gsap.to(t, { ...target, duration: reducedMotion ? 0.01 : duration, ease: 'power2.inOut', onUpdate: schedule });
    onStoryChange?.(null);
    return tween;
  }
  const step = (d) => show((((open ?? -1) + d) % stories.length + stories.length) % stories.length);

  // ---- unrolling ----
  function onPointerDown(e) {
    if (!active || e.button !== 0 || e.target.closest('.mark, .story, .progress')) return;
    drag = { x: e.clientX, y: e.clientY, tx: t.x, ty: t.y, moved: false };
    view.setPointerCapture(e.pointerId);
    tween?.kill();
  }
  function onPointerMove(e) {
    if (!drag) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
    Object.assign(t, clampT({ s: t.s, x: drag.tx + dx, y: drag.ty + dy }));
    view.classList.add('is-dragging');
    schedule();
  }
  function onPointerUp(e) {
    if (!drag) return;
    const moved = drag.moved;
    drag = null;
    view.classList.remove('is-dragging');
    if (!moved && open != null && !e.target.closest('.story, .mark, .progress')) hide();
  }
  function onWheel(e) {
    if (!active) return;
    e.preventDefault();
    tween?.kill();
    if (e.ctrlKey || e.metaKey) {
      // pinch / ctrl-wheel: closer, around the pointer
      const s = clamp(t.s * Math.exp(-e.deltaY * 0.0025), rest.s, MAX_ZOOM);
      const k = s / t.s;
      Object.assign(t, clampT({ s, x: e.clientX - (e.clientX - t.x) * k, y: e.clientY - (e.clientY - t.y) * k }));
    } else {
      const d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      Object.assign(t, clampT({ s: t.s, x: t.x - d * 1.1, y: t.y }));
    }
    schedule();
  }
  function onKey(e) {
    if (!active) return;
    if (e.key === 'ArrowRight' && open != null) step(1);
    else if (e.key === 'ArrowLeft' && open != null) step(-1);
    else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      tween?.kill();
      const target = clampT({ ...t, x: t.x + (e.key === 'ArrowLeft' ? 1 : -1) * vw * 0.5 });
      tween = gsap.to(t, { ...target, duration: reducedMotion ? 0.01 : 0.9, ease: 'power2.out', onUpdate: schedule });
    }
  }

  view.addEventListener('pointerdown', onPointerDown);
  view.addEventListener('pointermove', onPointerMove);
  view.addEventListener('pointerup', onPointerUp);
  view.addEventListener('pointercancel', onPointerUp);
  view.addEventListener('wheel', onWheel, { passive: false });
  addEventListener('keydown', onKey);
  addEventListener('resize', measure);
  card.querySelector('.story-close').addEventListener('click', () => hide());
  card.querySelector('.story-next').addEventListener('click', () => step(1));

  // the picture at the resolution this window needs, then the details in the background
  const need = W * ((innerHeight * BAND) / H) * Math.min(devicePixelRatio || 1, 2);
  const file = [...scene.flat].sort((a, b) => a.width - b.width).find((f) => f.width >= need) ?? scene.flat.at(-1);
  const ready = loadImage(file.url).then((img) => { picture = img; measure(); });
  ready.then(() => Promise.all(Object.entries(scene.details).map(([id, d]) =>
    loadImage(d.url).then((img) => { details[id] = { img, rect: d.rect }; if (look.id === id) schedule(); }))));

  measure();

  return {
    ready, measure, restRect,
    get open() { return open != null; },
    start() { active = true; },
    wake() { view.classList.add('is-awake'); },
    // back to rest before leaving; resolves when the view is flat again
    sleep(duration = 1.2) {
      active = false;
      hide(0.01);
      view.classList.remove('is-awake');
      tween?.kill();
      tween = gsap.to(t, { ...rest, duration: reducedMotion ? 0.01 : duration, ease: 'power2.inOut', onUpdate: schedule });
      return tween;
    },
    stop() { active = false; Object.assign(t, rest); draw(); },
    show, hide,
    // dev: jump every tween to its end and paint now (for screenshots in a hidden pane)
    settle() { gsap.getTweensOf([t, look]).forEach((tw) => tw.progress(1)); draw(); },
  };
}
