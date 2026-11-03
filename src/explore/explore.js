import { reducedMotion } from '../motion.js';
// The exploration canvas: a long stretch of the original scroll, unrolled by
// dragging, with a few quiet marks. Choosing a mark draws the view in toward one
// small moment: the rest of the scroll falls back into shadow, the moment comes
// forward at full resolution, and a short story appears beside it.
//
// The picture is drawn onto a viewport-sized canvas, only the part in view, so
// the browser never has to hold a 16,000-pixel-wide layer.
import gsap from 'gsap';
import { createSound } from './sound.js';
import { createImageCache, loadImage } from './images.js';
import { sceneFrame } from './framing.js';

const BAND = 0.86;            // the scroll's height as a share of the window at rest
const START_AT = 0.6;         // the bridge sits this far across the window at rest
const MAX_ZOOM = 1.7;         // 1 = one master pixel per CSS pixel; small moments may be shown larger
const VEIL = 'rgb(42, 35, 25)';


const el = (tag, cls, text) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
};
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));


export function createExplore(root, scene, stories, { onStoryChange, onMuteChange, muted, entranceImage } = {}) {
  const { width: W, height: H, rect, focus } = scene;     // picture units = master px
  const view = root.querySelector('.explore');
  const canvas = root.querySelector('.explore-canvas');
  const ctx = canvas.getContext('2d');
  const marksRoot = root.querySelector('.explore-marks');
  const card = root.querySelector('.story');
  const progress = root.querySelector('.progress');
  root.querySelector('.explore-hint span:last-child').textContent =
    root.dataset.painting === 'gusu' ? 'Look for the small golden marks' : 'Look for the small red marks';
  const soundToggles = [root.querySelector('.explore .sound-toggle')];   // independent from gallery music

  const t = { x: 0, y: 0, s: 1 };          // picture -> screen: sx = x + px * s
  let rest = { x: 0, y: 0, s: 1 };
  let vw = 1, vh = 1, dpr = 1;
  let active = false, disposed = false, generation = 0;
  const events = new AbortController();
  const requests = new AbortController();
  const listen = (node, name, fn, options = {}) => node.addEventListener(name, fn, { ...options, signal: events.signal });
  const maxZoom = scene.maxZoom ?? MAX_ZOOM;
  const status = el('div', 'image-status');
  status.hidden = true; status.setAttribute('role', 'status');
  const statusText = el('span', null, 'Some image detail could not load.');
  const retry = el('button', null, 'Retry'); retry.type = 'button';
  status.append(statusText, retry); view.append(status);
  const detailCache = createImageCache({ limit: 3, onChange: schedule });
  const tileCache = createImageCache({ limit: 4, onChange: schedule });
  let open = null;                         // index of the story being looked at
  // A few small, explicitly framed details permit a modest extra enlargement.
  // Ordinary Gusu navigation and all Qingming zoom limits remain unchanged.
  const zoomLimit = (i = open) => scene.edgeAware && stories[i]?.maxZoom
    ? Math.min(1.5, Math.max(maxZoom, stories[i].maxZoom)) : maxZoom;
  let drag = null;
  let tween = null;
  let picture = null, baseFailed = false;

  // the spotlight: where it is (picture px) and how far it has come up
  const look = { amt: 0, detail: 0, cx: 0, cy: 0, rx: 1, ry: 1, angle: 0, inner: 0.45, id: null };
  let raf = 0;

  // ---- sound ----
  const sound = createSound(scene.sounds ?? {}, {
    onMuteChange(muted) {
      for (const t of soundToggles) {
        t.classList.toggle('is-muted', muted);
        t.setAttribute('aria-pressed', String(!muted));
        t.setAttribute('aria-label', muted ? 'Sound off' : 'Sound on');
      }
      onMuteChange?.(muted);
    },
  });
  sound.setMuted(muted ?? sound.muted);      // reflect the shared sound preference
  for (const t of soundToggles) listen(t, 'click', (e) => { e.stopPropagation(); sound.toggle(); });

  const toPic = (v) => v - rect.left;      // master x -> picture x
  const toPicY = (v) => v - rect.top;

  // ---- marks and progress ----
  const marks = stories.map((story, i) => {
    const [x0, y0, x1, y1] = story.box;
    const label = root.dataset.painting === 'gusu' ? `${String(i + 1).padStart(2, '0')} · ${story.title}` : story.title;
    const m = el('button', 'mark');
    m.dataset.storyId = story.id;
    m.dataset.storyIndex = i;
    m.type = 'button';
    m.style.setProperty('--i', i);
    m.setAttribute('aria-label', label);
    m.append(el('span', 'mark-dot'), el('span', 'mark-label', label));
    listen(m, 'click', (e) => { e.stopPropagation(); show(i); });
    marksRoot.append(m);
    // the same moment in the row at the bottom, with a glimpse of it on hover
    const dot = el('button', 'progress-dot');
    dot.type = 'button';
    dot.dataset.storyId = story.id;
    dot.dataset.storyIndex = i;
    dot.setAttribute('aria-label', label);
    const thumb = el('span', 'progress-thumb');
    const img = el('img');
    img.alt = '';
    img.draggable = false;
    img.loading = 'lazy';
    const d = scene.details[story.id];
    if (d) {
      const loadThumb = () => { if (!img.getAttribute('src')) img.src = d.thumb ?? d.url; };
      listen(dot, 'pointerenter', loadThumb); listen(dot, 'focus', loadThumb);
      // centre the glimpse on the story's box within its detail crop
      const [dx0, dy0, dx1, dy1] = d.rect;
      const [fx0, fy0, fx1, fy1] = story.frameBox ?? story.box;
      // Authored thumbnails already contain the exact camera crop. In particular,
      // a relocated scene must not be positioned using its archival research box.
      img.style.objectPosition = d.thumb ? '50% 50%' : `${((fx0 + fx1) / 2 - dx0) / (dx1 - dx0) * 100}% ${((fy0 + fy1) / 2 - dy0) / (dy1 - dy0) * 100}%`;
    }
    thumb.append(img, el('span', null, label));
    dot.append(thumb);
    listen(dot, 'click', (e) => { e.stopPropagation(); show(i); });
    progress.append(dot);
    const [ax, ay] = story.anchor ?? [(x0 + x1) / 2, (y0 + y1) / 2];
    return { el: m, dot, story, px: toPic(ax), py: toPicY(ay) };
  });

  // Gusu story data, marker numbering and navigation share the same left-to-right order.
  // Stable story IDs keep artwork, sound and copy attached to the same scene.
  const spatialMarks = root.dataset.painting === 'gusu'
    ? [...marks].sort((a, b) => a.px - b.px || a.py - b.py)
    : marks;
  progress.replaceChildren(...spatialMarks.map((m) => m.dot));

  // ---- drawing ----
  function schedule() {
    if (!disposed && !raf) raf = requestAnimationFrame(() => { raf = 0; draw(); });
  }
  function draw() {
    if (disposed) return;
    let imageFailed = baseFailed || (open != null && detailCache.get(look.id) === null);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, vw, vh);
    if (!picture && entranceImage?.naturalWidth && scene.entrance) {
      const [a,b,c,d] = scene.entrance.rect;
      ctx.drawImage(entranceImage, t.x + a*t.s, t.y + b*t.s, (c-a)*t.s, (d-b)*t.s);
    }
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
    if (scene.tiles && active) {
      const left = clamp(-t.x / t.s, 0, W), right = clamp((vw - t.x) / t.s, 0, W);
      const visible = scene.tiles.filter(({ rect: [a,,b] }) => b >= left && a <= right);
      const wanted = new Set(visible.map((tile) => tile.file));
      const first = scene.tiles.indexOf(visible[0]), last = scene.tiles.indexOf(visible.at(-1));
      // A single adjacent segment, following the current direction of travel.
      const neighbor = scene.tiles[last + 1] ?? scene.tiles[first - 1];
      const prefetch = neighbor && visible.every((tile) => tileCache.get(tile.file));
      if (prefetch) wanted.add(neighbor.file);
      tileCache.retain(wanted);
      for (const tile of [...visible, ...(prefetch ? [neighbor] : [])]) {
        tileCache.request(tile.file, tile.url);
        const img = tileCache.get(tile.file);
        if (visible.includes(tile) && img === null) imageFailed = true;
        if (!img || !visible.includes(tile)) continue;
        const [a,b,c,d] = tile.rect;
        const x0 = Math.max(a, left), x1 = Math.min(c, right);
        const y0 = clamp(-t.y/t.s, b, d), y1 = clamp((vh-t.y)/t.s, b, d);
        if (x1>x0 && y1>y0) ctx.drawImage(img, x0-a, y0-b, x1-x0, y1-y0,
          t.x+x0*t.s, t.y+y0*t.s, (x1-x0)*t.s, (y1-y0)*t.s);
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
      const g = ctx.createRadialGradient(0, 0, rx * look.inner, 0, 0, rx);
      g.addColorStop(0, 'rgba(42,35,25,0)');
      g.addColorStop(1, `rgba(42,35,25,${0.6 * look.amt})`);
      ctx.fillStyle = g;
      const big = (vw + vh) * 2;
      ctx.fillRect(-big, -big * rx / ry, big * 2, big * 2 * rx / ry);
      ctx.restore();
      // the moment itself, at full resolution, within a soft edge
      const metadata = scene.details[look.id];
      if (metadata) detailCache.request(look.id, metadata.url, { priority: true });
      const detailImage = detailCache.get(look.id);
      const d = metadata && detailImage ? { ...metadata, img: detailImage } : null;
      if (d && look.detail > 0.001) {
        const [dx0, dy0, dx1, dy1] = d.rect;
        const sx = t.x + toPic(dx0) * t.s, sy = t.y + toPicY(dy0) * t.s;
        const sw = (dx1 - dx0) * t.s, sh = (dy1 - dy0) * t.s;
        const off = offscreen(Math.ceil(sw * dpr), Math.ceil(sh * dpr));
        const o = off.getContext('2d');
        o.setTransform(dpr, 0, 0, dpr, 0, 0);
        o.clearRect(0, 0, sw, sh);
        o.imageSmoothingQuality = 'high';
        o.filter = scene.detailFilter ?? 'brightness(1.05) saturate(1.08)';
        o.drawImage(d.img, 0, 0, sw, sh);
        o.filter = 'none';
        o.globalCompositeOperation = 'destination-in';
        o.save();
        o.translate(cx - sx, cy - sy);
        o.rotate(look.angle);
        o.scale(1, ry / rx);
        const m = o.createRadialGradient(0, 0, rx * Math.max(0.5, look.inner), 0, 0, rx * 0.9);
        m.addColorStop(0, `rgba(0,0,0,${look.detail})`);
        m.addColorStop(1, 'rgba(0,0,0,0)');
        o.fillStyle = m;
        o.fillRect(-sw * 2, -sh * 2 * rx / ry, sw * 5, sh * 5 * rx / ry);
        o.restore();
        o.globalCompositeOperation = 'source-over';
        ctx.drawImage(off, 0, 0, off.width, off.height, sx, sy, sw, sh);
      }
    }
    status.hidden = !imageFailed;
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
    const s = scene.edgeAware ? Math.min(1.25, (vh * BAND) / H) : (vh * BAND) / H;
    rest = clampT({ s, x: vw * START_AT - focus.x * W * s, y: (vh - H * s) / 2 });
    if (!active || open == null) Object.assign(t, rest);
    else {
      const i = open, turn = generation;
      frame(i, 0).then(() => { if (!disposed && generation === turn && open === i) card.classList.add('is-shown'); });
    }
    draw();
  }
  const restRect = () => {
    const r = scene.entrance?.rect ?? [0, 0, W, H];
    return { left: rest.x + r[0] * rest.s, top: rest.y + r[1] * rest.s, width: (r[2]-r[0])*rest.s, height: (r[3]-r[1])*rest.s };
  };

  // ---- looking closer ----
  function frame(i, duration = 1.4) {
    if (scene.edgeAware) {
      if (vw <= 800) card.dataset.side='bottom';
      const { side, x, y, s } = sceneFrame({ box: stories[i].frameBox ?? stories[i].box, width: W, height: H, vw, vh, rest, cardHeight: card.offsetHeight, cardBottom: stories.length > 13 ? 88 : 64, maxZoom: zoomLimit(i) });
      card.dataset.side = side;
      tween?.kill();
      tween = gsap.to(t, { x, y, s, duration: reducedMotion ? 0.01 : duration, ease: 'power2.inOut', onUpdate: schedule });
      return tween;
    }
    const [x0, y0, x1, y1] = stories[i].box;
    const bw = x1 - x0, bh = y1 - y0;
    // a tall, thin moment (the pole) may fill more of the window's height
    const share = bh > 2.5 * bw ? 0.8 : 0.6;
    // close enough to see the moment, and at least close enough that the picture
    // fills the window's height, so no paper shows above or below it
    const fill = vh / H;
    const s = clamp(Math.min((vh * share) / bh, (vw * 0.46) / bw), Math.max(rest.s * 1.5, fill), maxZoom);
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
    if (disposed || !active || !stories[i]) return;
    const turn = ++generation;
    const story = stories[i];
    const d = scene.details[story.id];
    detailCache.retain([story.id]);
    if (d) detailCache.request(story.id, d.url, { priority: true });
    const [x0, y0, x1, y1] = story.frameBox ?? story.box;
    open = i;
    view.classList.add('is-looking');
    marks.forEach((m, k) => {
      m.el.classList.toggle('is-open', k === i);
      m.dot.classList.toggle('is-open', k === i);
    });

    look.id = story.id;
    look.cx = toPic(story.spot?.center?.[0] ?? (x0 + x1) / 2);
    look.cy = toPicY(story.spot?.center?.[1] ?? (y0 + y1) / 2);
    look.rx = story.spot?.rx ?? Math.max((x1 - x0) * 0.8, (y1 - y0) * 0.22);
    look.ry = story.spot?.ry ?? Math.max((y1 - y0) * 0.8, (x1 - x0) * 0.22);
    look.angle = ((story.spot?.angle ?? 0) * Math.PI) / 180;
    look.inner = story.spot?.inner ?? 0.45;
    gsap.killTweensOf(look);
    gsap.to(look, { amt: 1, duration: reducedMotion ? 0.01 : 1.2, ease: 'power1.inOut', onUpdate: schedule });
    look.detail = 0;
    gsap.to(look, { detail: 1, duration: reducedMotion ? 0.01 : 0.9, delay: 0.5, ease: 'power1.inOut', onUpdate: schedule });
    // the moment's sound arrives with its detail; a story without one quiets the last
    sound.play(story.sound, 0.5);

    card.querySelector('.story-title').textContent = story.title;
    card.querySelector('.story-body').replaceChildren(...story.text.map((text) => {
      const paragraph = el('p');
      // The authored copy uses *emphasis*; keep every other character as text.
      text.split(/\*([^*]+)\*/g).forEach((part, i) => {
        paragraph.append(i % 2 ? el('em', null, part) : document.createTextNode(part));
      });
      return paragraph;
    }));
    card.scrollTop = 0;
    card.querySelector('.story-count').textContent = `${i + 1} of ${stories.length}`;
    const next = card.querySelector('.story-next');
    const arrow = el('span', null, '→');
    arrow.setAttribute('aria-hidden', 'true');
    next.replaceChildren(document.createTextNode(`${story.nextLabel ?? 'Next discovery'} `), arrow);
    card.classList.remove('is-shown');
    frame(i).then(() => { if (!disposed && generation === turn && open === i) card.classList.add('is-shown'); });
    onStoryChange?.(story);
  }

  function hide(duration = 1.2) {
    if (open == null) return null;
    open = null;
    generation++;
    view.classList.remove('is-looking');
    card.classList.remove('is-shown');
    marks.forEach((m) => { m.el.classList.remove('is-open'); m.dot.classList.remove('is-open'); });
    sound.stop();
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
  const pointers = new Map();
  let pinch = null;
  function onPointerDown(e) {
    if (!active || (e.button !== 0 && e.pointerType !== 'touch') || e.target.closest('.mark, .story, .progress, .sound-toggle, .image-status')) return;
    pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.size === 2) {
      const [a,b] = [...pointers.values()];
      pinch = { distance: Math.hypot(a.x-b.x,a.y-b.y), cx:(a.x+b.x)/2, cy:(a.y+b.y)/2, x:t.x, y:t.y, s:t.s };
      drag = null; view.setPointerCapture(e.pointerId); return;
    }
    drag = { x: e.clientX, y: e.clientY, tx: t.x, ty: t.y, moved: false };
    view.setPointerCapture(e.pointerId);
    tween?.kill();
  }
  function onPointerMove(e) {
    if (pointers.has(e.pointerId)) pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pinch && pointers.size === 2) {
      const [a,b] = [...pointers.values()];
      const cx=(a.x+b.x)/2, cy=(a.y+b.y)/2;
      const s=clamp(pinch.s*Math.hypot(a.x-b.x,a.y-b.y)/Math.max(1,pinch.distance),rest.s,Math.max(rest.s,zoomLimit()));
      const k=s/pinch.s; Object.assign(t,clampT({s,x:cx-(pinch.cx-pinch.x)*k,y:cy-(pinch.cy-pinch.y)*k})); schedule(); return;
    }
    if (!drag) return;
    const dx = e.clientX - drag.x, dy = e.clientY - drag.y;
    if (Math.abs(dx) + Math.abs(dy) > 4) drag.moved = true;
    Object.assign(t, clampT({ s: t.s, x: drag.tx + dx, y: drag.ty + dy }));
    view.classList.add('is-dragging');
    schedule();
  }
  function onPointerUp(e) {
    pointers.delete(e.pointerId);
    if (pinch) {
      pinch=null; const remaining=[...pointers.values()][0];
      drag=remaining ? {x:remaining.x,y:remaining.y,tx:t.x,ty:t.y,moved:true} : null; return;
    }
    if (!drag) return;
    const moved = drag.moved;
    drag = null;
    view.classList.remove('is-dragging');
    if (!moved && open != null && !e.target.closest('.story, .mark, .progress, .sound-toggle')) hide();
  }
  function onWheel(e) {
    if (!active || e.target.closest('.story, .progress, .image-status')) return;
    e.preventDefault();
    tween?.kill();
    if (e.ctrlKey || e.metaKey) {
      // pinch / ctrl-wheel: closer, around the pointer
      const s = clamp(t.s * Math.exp(-e.deltaY * 0.0025), rest.s, Math.max(rest.s, zoomLimit()));
      const k = s / t.s;
      Object.assign(t, clampT({ s, x: e.clientX - (e.clientX - t.x) * k, y: e.clientY - (e.clientY - t.y) * k }));
    } else {
      const d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      Object.assign(t, clampT({ s: t.s, x: t.x - d * 1.1, y: t.y }));
    }
    schedule();
  }
  function onKey(e) {
    if (!active || e.target.closest?.('button, a, input') && !['ArrowLeft','ArrowRight'].includes(e.key)) return;
    if (['ArrowLeft','ArrowRight'].includes(e.key)) e.preventDefault();
    if (open != null && ['ArrowLeft', 'ArrowRight'].includes(e.key)) {
      const at = spatialMarks.indexOf(marks[open]);
      const direction = e.key === 'ArrowLeft' ? -1 : 1;
      const target = spatialMarks[(at + direction + spatialMarks.length) % spatialMarks.length];
      show(marks.indexOf(target));
    }
    else if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
      tween?.kill();
      const target = clampT({ ...t, x: t.x + (e.key === 'ArrowLeft' ? 1 : -1) * vw * 0.5 });
      tween = gsap.to(t, { ...target, duration: reducedMotion ? 0.01 : 0.9, ease: 'power2.out', onUpdate: schedule });
    }
  }

  listen(view, 'pointerdown', onPointerDown);
  listen(view, 'pointermove', onPointerMove);
  listen(view, 'pointerup', onPointerUp);
  listen(view, 'pointercancel', onPointerUp);
  listen(view, 'wheel', onWheel, { passive: false });
  listen(window, 'keydown', onKey);
  listen(window, 'resize', measure);
  listen(card.querySelector('.story-close'), 'click', () => hide());
  listen(card.querySelector('.story-next'), 'click', () => step(1));

  // Only the active painting loads a base image. The gallery segment can carry
  // entry immediately, even while a slow overview request is still in flight.
  const need = W * ((innerHeight * BAND) / H) * Math.min(devicePixelRatio || 1, 2);
  const file = [...scene.flat].sort((a,b) => a.width-b.width).find((f) => f.width>=need) ?? scene.flat.at(-1);
  let loadingBase = null;
  function loadBase() {
    if (loadingBase || disposed) return loadingBase;
    loadingBase = loadImage(file.url, requests.signal).then((img) => {
      if (!disposed) { picture=img; baseFailed=false; measure(); }
    }).catch((error) => {
      if (!disposed) { console.warn('Painting base image unavailable', error); baseFailed=true; schedule(); }
    }).finally(() => { loadingBase=null; });
    return loadingBase;
  }
  listen(retry, 'click', () => { baseFailed=false; status.hidden=true; tileCache.retry(); detailCache.retry(); loadBase(); schedule(); });
  const base = loadBase();
  const ready = scene.tiles || entranceImage?.naturalWidth ? Promise.resolve() : base;

  measure();

  return {
    ready, measure, restRect,
    get open() { return open != null; },
    start() { active = true; schedule(); },
    wake() { view.classList.add('is-awake'); },
    // back to rest before leaving; resolves when the view is flat again
    sleep(duration = 1.2) {
      active = false;
      pointers.clear(); pinch = drag = null;
      hide(0.01);
      sound.stop(0.1);
      view.classList.remove('is-awake');
      tween?.kill();
      tween = gsap.to(t, { ...rest, duration: reducedMotion ? 0.01 : duration, ease: 'power2.inOut', onUpdate: schedule });
      return tween;
    },
    stop() { active = false; Object.assign(t, rest); draw(); },
    destroy() {
      disposed=true; active=false; generation++;
      events.abort(); requests.abort(); tileCache.destroy(); detailCache.destroy(); sound.destroy();
      tween?.kill(); gsap.killTweensOf([t,look]); cancelAnimationFrame(raf);
      marksRoot.replaceChildren(); progress.replaceChildren(); status.remove();
      card.classList.remove('is-shown'); view.classList.remove('is-awake','is-looking','is-dragging');
      picture=null; entranceImage=null; offCanvas=null;
      ctx.clearRect(0,0,canvas.width,canvas.height);
    },
    show, hide, sound,
    state() { return { active, disposed, open, transform: { x:t.x, y:t.y, s:t.s }, spotlight: { ...look }, tiles: tileCache.state(), details: detailCache.state(), imageReady: Boolean(picture), statusVisible: !status.hidden }; },
    // dev: jump every tween to its end and paint now (for screenshots in a hidden pane)
    settle() { gsap.getTweensOf([t, look]).forEach((tw) => tw.progress(1)); draw(); },
  };
}
