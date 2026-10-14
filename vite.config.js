import { defineConfig } from 'vite';

export default defineConfig({
  // relative base so the build can sit under the portfolio's /playground/ later
  base: './',
  // assets/ is the preparation pipeline (master, crops, masks). Only files that
  // src/ imports reach the build; nothing is copied wholesale.
  publicDir: false,
  server: { port: 4180 },
});
