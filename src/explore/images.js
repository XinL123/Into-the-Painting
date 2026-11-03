// Bounded, cancellable image cache. Only the active painting creates one.
// The tiny overview is a fallback; native pixels arrive as viewport-sized segments.
export function loadImage(url, signal) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) { reject(new DOMException('Aborted', 'AbortError')); return; }
    const img = new Image();
    img.decoding = 'async';
    let timer;
    const cleanup = () => { clearTimeout(timer); signal?.removeEventListener('abort', abort); img.onload = img.onerror = null; };
    const abort = () => { cleanup(); img.src = ''; reject(new DOMException('Aborted', 'AbortError')); };
    img.onload = () => { cleanup(); resolve(img); };
    img.onerror = () => { cleanup(); reject(new Error(`Image unavailable: ${url}`)); };
    signal?.addEventListener('abort', abort, { once: true });
    // Never strand entry behind a hung request. Late retries are explicit.
    timer = setTimeout(() => { cleanup(); img.src = ''; reject(new Error('Image timed out')); }, 12000);
    img.src = url;
  });
}

export function createImageCache({ limit = 6, concurrency = 2, load = loadImage, onChange = () => {}, onError = () => {} } = {}) {
  const entries = new Map();
  const pending = new Map();
  let queue = [], disposed = false;
  function trim() {
    while (entries.size > limit) entries.delete(entries.keys().next().value);
  }
  function pump() {
    if (disposed) return;
    while (pending.size < concurrency && queue.length) {
      const { key, url } = queue.shift();
      if (entries.has(key) || pending.has(key)) continue;
      const controller = new AbortController();
      pending.set(key, controller);
      load(url, controller.signal).then((img) => {
        if (disposed || controller.signal.aborted) return;
        entries.set(key, img); trim(); onChange();
      }).catch((error) => {
        // Keep fallback pixels; retry only when the viewer explicitly asks.
        if (!disposed && !controller.signal.aborted) { console.warn('Painting detail unavailable', key, error); entries.set(key, null); onError(key); }
        trim();
      }).finally(() => { pending.delete(key); pump(); if (!disposed) onChange(); });
    }
  }
  return {
    get(key) {
      if (!entries.has(key)) return undefined;
      const value = entries.get(key); entries.delete(key); entries.set(key, value); return value;
    },
    request(key, url, { priority = false } = {}) {
      if (disposed || entries.has(key) || pending.has(key)) return;
      queue = queue.filter((q) => q.key !== key);
      if (priority) queue.unshift({ key, url }); else queue.push({ key, url });
      pump();
    },
    retain(keys) {
      const wanted = new Set(keys);
      queue = queue.filter((q) => wanted.has(q.key));
      for (const [key, controller] of pending) if (!wanted.has(key)) controller.abort();
    },
    retry() { for (const [key, img] of entries) if (!img) entries.delete(key); },
    destroy() { disposed = true; queue = []; for (const c of pending.values()) c.abort(); pending.clear(); entries.clear(); },
    state() { return { cached: entries.size, pending: pending.size, queued: queue.length, disposed }; },
  };
}
