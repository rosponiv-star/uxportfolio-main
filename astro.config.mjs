// @ts-check
import { readdirSync, readFileSync } from 'node:fs';
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

// Pages that are built but not linked yet stay out of the sitemap: case studies still marked
// `placeholder: true` in their frontmatter, and the Playground (shown as "Coming soon" in the nav).
const projectsDir = new URL('./src/content/projects/', import.meta.url);
const hidden = [
  '/playground',
  ...readdirSync(projectsDir)
    .filter((f) => f.endsWith('.mdx') && /^placeholder:\s*true/m.test(readFileSync(new URL(f, projectsDir), 'utf8')))
    .map((f) => `/work/${f.replace(/^\d+-/, '').replace(/\.mdx$/, '')}`),
];

export default defineConfig({
  site: 'https://www.valeriorosponi.com',
  trailingSlash: 'ignore',
  integrations: [
    mdx(),
    sitemap({ filter: (page) => !hidden.some((path) => new URL(page).pathname.replace(/\/$/, '') === path) }),
  ],
  devToolbar: { enabled: false },
  // The preview launcher may assign a free port through PORT; 4321 otherwise.
  server: { port: Number(process.env.PORT) || 4321 },
  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'hover',
  },
});
