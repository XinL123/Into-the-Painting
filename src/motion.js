// Respect the system setting. A development-only query makes the same path
// reviewable on localhost without changing the user's operating-system settings.
export const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches ||
  (import.meta.env.DEV && new URLSearchParams(location.search).get('motion') === 'reduce');
