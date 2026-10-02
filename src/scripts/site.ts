// Global, progressively enhanced behaviours. Everything here is optional:
// the site is fully readable without JavaScript.

const root = document.documentElement;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* -------------------------------------------------------------------------- */
/* Scroll reveals                                                             */
/* -------------------------------------------------------------------------- */
function initReveals() {
  const items = document.querySelectorAll<HTMLElement>('[data-reveal]');
  if (!('IntersectionObserver' in window) || reducedMotion) {
    items.forEach((el) => el.classList.add('is-in'));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      }
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.05 },
  );
  items.forEach((el) => io.observe(el));
}

/* -------------------------------------------------------------------------- */
/* Header: border after scroll, hide on scroll down, show on scroll up        */
/* -------------------------------------------------------------------------- */
function initHeader() {
  let lastY = window.scrollY;
  let ticking = false;

  const update = () => {
    const y = window.scrollY;
    root.toggleAttribute('data-scrolled', y > 8);
    const goingDown = y > lastY;
    root.toggleAttribute('data-header-hidden', goingDown && y > 240);
    lastY = y;
    ticking = false;
  };

  window.addEventListener(
    'scroll',
    () => {
      if (!ticking) {
        requestAnimationFrame(update);
        ticking = true;
      }
    },
    { passive: true },
  );
  update();

  // Keyboard users always get the header back.
  document.querySelector('[data-header]')?.addEventListener('focusin', () => {
    root.removeAttribute('data-header-hidden');
  });
}

/* -------------------------------------------------------------------------- */
/* Local clock (Europe/Rome)                                                  */
/* -------------------------------------------------------------------------- */
function initClock() {
  const clocks = document.querySelectorAll<HTMLElement>('[data-clock]');
  if (!clocks.length) return;
  const fmt = new Intl.DateTimeFormat('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'Europe/Rome',
    timeZoneName: 'short',
  });
  const tick = () => {
    const text = fmt.format(new Date());
    clocks.forEach((c) => (c.textContent = text));
  };
  tick();
  setInterval(tick, 15_000);
}

/* -------------------------------------------------------------------------- */
/* Cursor label on project covers                                             */
/* -------------------------------------------------------------------------- */
function initCursorLabel() {
  const targets = document.querySelectorAll<HTMLElement>('[data-cursor]');
  if (!targets.length || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

  const label = document.createElement('div');
  label.className = 'cursor-label';
  label.setAttribute('aria-hidden', 'true');
  document.body.appendChild(label);

  let x = 0;
  let y = 0;
  let cx = 0;
  let cy = 0;
  let raf = 0;
  let active = false;

  const loop = () => {
    cx += (x - cx) * (reducedMotion ? 1 : 0.22);
    cy += (y - cy) * (reducedMotion ? 1 : 0.22);
    label.style.transform = `translate3d(${cx}px, ${cy}px, 0)`;
    if (active || Math.abs(x - cx) > 0.5 || Math.abs(y - cy) > 0.5) {
      raf = requestAnimationFrame(loop);
    } else {
      raf = 0;
    }
  };

  targets.forEach((el) => {
    el.addEventListener('pointerenter', (e) => {
      label.textContent = el.dataset.cursor || 'View';
      x = cx = e.clientX;
      y = cy = e.clientY;
      active = true;
      label.classList.add('is-visible');
      if (!raf) raf = requestAnimationFrame(loop);
    });
    el.addEventListener('pointermove', (e) => {
      x = e.clientX;
      y = e.clientY;
    });
    el.addEventListener('pointerleave', () => {
      active = false;
      label.classList.remove('is-visible');
    });
  });
}

/* -------------------------------------------------------------------------- */
/* Scroll spy: highlights the current item in an index / table of contents.   */
/* Markup: [data-spy] container with links [data-spy-link="id"].              */
/* -------------------------------------------------------------------------- */
function initScrollSpy() {
  document.querySelectorAll<HTMLElement>('[data-spy]').forEach((container) => {
    const links = Array.from(container.querySelectorAll<HTMLAnchorElement>('[data-spy-link]'));
    const sections = links
      .map((l) => document.getElementById(l.dataset.spyLink!))
      .filter((s): s is HTMLElement => Boolean(s));
    if (!sections.length) return;

    const setActive = (id: string) => {
      links.forEach((l) => l.classList.toggle('is-active', l.dataset.spyLink === id));
    };

    const onScroll = () => {
      const line = window.innerHeight * 0.4;
      let current = sections[0].id;
      for (const s of sections) {
        if (s.getBoundingClientRect().top <= line) current = s.id;
      }
      setActive(current);
    };

    let ticking = false;
    window.addEventListener(
      'scroll',
      () => {
        if (!ticking) {
          requestAnimationFrame(() => {
            onScroll();
            ticking = false;
          });
          ticking = true;
        }
      },
      { passive: true },
    );
    onScroll();
  });
}

/* -------------------------------------------------------------------------- */
/* Reading progress bar                                                       */
/* -------------------------------------------------------------------------- */
function initProgress() {
  const bar = document.querySelector<HTMLElement>('[data-progress]');
  const article = document.querySelector<HTMLElement>('[data-progress-target]');
  if (!bar || !article) return;
  const update = () => {
    const rect = article.getBoundingClientRect();
    const total = rect.height - window.innerHeight;
    const p = total > 0 ? Math.min(1, Math.max(0, -rect.top / total)) : 0;
    bar.style.transform = `scaleX(${p})`;
  };
  window.addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  window.addEventListener('resize', update);
  update();
}

/* -------------------------------------------------------------------------- */
/* Videos: only play while visible                                            */
/* -------------------------------------------------------------------------- */
function initVideos() {
  const videos = document.querySelectorAll<HTMLVideoElement>('video[data-autoplay]');
  if (!videos.length) return;
  if (reducedMotion) return;
  const io = new IntersectionObserver(
    (entries) => {
      for (const { target, isIntersecting } of entries) {
        const v = target as HTMLVideoElement;
        if (isIntersecting) v.play().catch(() => {});
        else v.pause();
      }
    },
    { threshold: 0.15 },
  );
  videos.forEach((v) => io.observe(v));
}

initReveals();
initHeader();
initClock();
initCursorLabel();
initScrollSpy();
initProgress();
initVideos();
