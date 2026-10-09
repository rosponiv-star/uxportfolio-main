import { getCollection, type CollectionEntry } from 'astro:content';

export type Project = CollectionEntry<'projects'>;

/** Filter vocabulary, in display order. Must match the enum in content.config.ts. */
export const CATEGORIES = ['Mobile', 'XR', 'Product', 'Multi-screen'] as const;

export { categoryId } from './collection';

/** URL slug: file id without its numeric ordering prefix ("01-justcook" → "justcook"). */
export const slugOf = (p: Project) => p.id.replace(/^\d+-/, '');

export const hrefOf = (p: Project) => `/work/${slugOf(p)}`;

export const numOf = (p: Project) => String(p.data.order).padStart(2, '0');

export const chapterId = (title: string) =>
  title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');

/** Chapters in order, read from the `<Chapter title="…" summary="…">` tags in the MDX source.
 *  `summary` (optional, a few words) is shown under the step in the Process index. */
export const chaptersOf = (p: Project) =>
  Array.from((p.body ?? '').matchAll(/<Chapter\b([^>]*)>/g), (m) => {
    const attr = (name: string) => m[1].match(new RegExp(`${name}=["']([^"']+)["']`))?.[1];
    const title = attr('title') ?? '';
    return { title, id: chapterId(title), summary: attr('summary') };
  }).filter((c) => c.title);

export async function getProjects() {
  const all = await getCollection('projects');
  return all.sort((a, b) => a.data.order - b.data.order);
}
