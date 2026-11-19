/* Hybrid test: the game list under the intro drives the hero background. */
(() => {
  const slides = [...document.querySelectorAll('[data-slide]')];
  const tiles = [...document.querySelectorAll('[data-tile]')];
  if (!slides.length) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let i = 0, timer, held = false;
  const show = (n, hold) => {
    i = (n + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('is-on', k === i));
    tiles.forEach((t, k) => {
      t.classList.remove('is-on', 'is-held');
      if (k === i) { void t.offsetWidth; t.classList.add('is-on'); if (hold) t.classList.add('is-held'); }
    });
  };
  const play = () => { clearInterval(timer); if (!reduce && !held) timer = setInterval(() => show(i + 1), 6000); };
  tiles.forEach((t, k) => {
    t.addEventListener('mouseenter', () => { held = true; clearInterval(timer); show(k, true); });
    t.addEventListener('focus', () => { held = true; clearInterval(timer); show(k, true); });
  });
  const games = document.querySelector('.games');
  games && games.addEventListener('mouseleave', () => { held = false; show(i); play(); });
  document.addEventListener('visibilitychange', () => document.hidden ? clearInterval(timer) : play());
  show(0); play();
})();
