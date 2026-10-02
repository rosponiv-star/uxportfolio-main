// Shared helpers for filterable collections (Work, Playground).

export const categoryId = (c: string) => c.toLowerCase().replace(/[^a-z0-9]+/g, '-');

/** Grid: two columns, every item half width. */
export function gridSizes(n: number): ('full' | 'half')[] {
  return Array.from({ length: n }, () => 'half' as const);
}

export function yearSpan(years: (string | number)[]) {
  const ys = years.map(Number).filter(Number.isFinite);
  if (!ys.length) return '';
  const lo = Math.min(...ys);
  const hi = Math.max(...ys);
  return lo === hi ? `${lo}` : `${lo} to ${hi}`;
}
