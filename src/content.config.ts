import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      order: z.number(),
      // One-line statement shown under the title.
      tagline: z.string(),
      year: z.string(),
      type: z.string(),
      // Work filters. Keep to the shared vocabulary in lib/projects.ts → CATEGORIES.
      categories: z.array(z.enum(['UX/UI', 'Service design', 'Product', 'XR', 'Research'])).min(1),
      platform: z.string(),
      role: z.string(),
      timeline: z.string(),
      team: z.string(),
      tools: z.array(z.string()),
      // Cover placeholder tone (muted, editorial) and whether text on it should be light.
      tone: z.string(),
      toneDark: z.boolean().default(false),
      cover: z
        .object({
          image: image().optional(),
          video: z.string().optional(),
          alt: z.string().default(''),
        })
        .optional(),
      // 30-second read for recruiters.
      glance: z.object({
        problem: z.string(),
        approach: z.string(),
        outcome: z.string(),
      }),
      // True while the case study still contains placeholder content.
      placeholder: z.boolean().default(false),
    }),
});

export const collections = { projects };
