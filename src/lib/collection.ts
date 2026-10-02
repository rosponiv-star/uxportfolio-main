// Shared helpers for filterable collections (Work, Playground).

export const categoryId = (c: string) => c.toLowerCase().replace(/[^a-z0-9]+/g, '-');

/** Grid rhythm: full, half, half, full… A half left without a partner becomes full. */
export function gridSizes(n: number): ('full' | 'half')[] {
  const out = Array.from({ length: n }, (_, i) => (i % 3 === 0 ? 'full' : 'half') as 'full' | 'half');
  if (n % 3 === 2) out[n - 1] = 'full';
  return out;
}

export function yearSpan(years: (string | number)[]) {
  const ys = years.map(Number).filter(Number.isFinite);
  if (!ys.length) return '';
  const lo = Math.min(...ys);
  const hi = Math.max(...ys);
  return lo === hi ? `${lo}` : `${lo} to ${hi}`;
}
