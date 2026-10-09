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
      categories: z.array(z.enum(['Mobile', 'XR', 'Product', 'Multi-screen'])).min(1),
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
      // The result, shown right after the Overview: what was made (screens and boards, placeholders
      // until `image` is set), what it does in one or two sentences, and the key numbers.
      result: z
        .object({
          text: z.string(),
          media: z
            .array(
              z.object({
                label: z.string(),
                image: image().optional(),
                alt: z.string().default(''),
                // 'screen' = one track, phone ratio; 'wide' = the whole body lane.
                kind: z.enum(['screen', 'wide']).default('screen'),
              }),
            )
            .default([]),
          // Interface presentation (replaces `media` when present): labelled groups of device shots.
          // layout: 'trio' = tracks A/B/C beside the label; 'pair' / 'quad' = the full 12 columns.
          // crop: share of the device height shown from the top (e.g. 0.45 for Dynamic Island / widgets).
          // stagger: trio shots step down one after the other.
          showcase: z
            .array(
              z.object({
                label: z.string(),
                layout: z.enum(['trio', 'pair', 'quad']),
                crop: z.number().min(0.2).max(1).optional(),
                stagger: z.boolean().default(false),
                items: z.array(z.object({ image: image(), alt: z.string() })),
              }),
            )
            .optional(),
          metricsLabel: z.string().optional(),
          metrics: z.array(z.object({ value: z.string(), label: z.string() })).default([]),
        })
        .optional(),
      // True while the case study still contains placeholder content.
      placeholder: z.boolean().default(false),
    }),
});

export const collections = { projects };
