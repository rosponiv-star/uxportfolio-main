// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.valeriorosponi.com',
  trailingSlash: 'ignore',
  integrations: [mdx(), sitemap()],
  devToolbar: { enabled: false },
  // The preview launcher may assign a free port through PORT; 4321 otherwise.
  server: { port: Number(process.env.PORT) || 4321 },
  prefetch: {
    prefetchAll: true,
    defaultStrategy: 'hover',
  },
});
