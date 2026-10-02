// Single source of truth for personal info used across the site.
export const site = {
  name: 'Valerio Rosponi',
  url: 'https://www.valeriorosponi.com',
  email: 'rosponiv@gmail.com',
  // TODO: replace with the full LinkedIn profile URL.
  linkedin: 'https://www.linkedin.com/in/',
  cv: '/cv/Valerio-Rosponi-CV.pdf',
  roles: ['UX Designer', 'Digital Product Designer', 'Visual Designer'],
  location: 'Trentino, Italy',
  timezone: 'Europe/Rome',
  description:
    'Valerio Rosponi — UX, digital product and visual designer. Case studies, process and the thinking behind the work.',
};

export const nav = [
  { href: '/', label: 'Work', match: (p: string) => p === '/' || p.startsWith('/work') },
  { href: '/playground', label: 'Playground', match: (p: string) => p.startsWith('/playground') },
  { href: '/about', label: 'About', match: (p: string) => p.startsWith('/about') },
];
