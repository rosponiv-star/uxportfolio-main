import { getCollection, type CollectionEntry } from 'astro:content';

export type Project = CollectionEntry<'projects'>;

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

/** Chapter titles in order, read from the `<Chapter title="…">` tags in the MDX source. */
export const chaptersOf = (p: Project) =>
  Array.from((p.body ?? '').matchAll(/<Chapter\s+title=["']([^"']+)["']/g), (m) => ({
    title: m[1],
    id: chapterId(m[1]),
  }));

export async function getProjects() {
  const all = await getCollection('projects');
  return all.sort((a, b) => a.data.order - b.data.order);
}
