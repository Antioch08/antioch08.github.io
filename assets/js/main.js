/* Daniel J Lewis · Portfolio interactions (no dependencies) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* nav: solid on scroll + mobile toggle */
  const nav = $('[data-nav]');
  const onScroll = () => nav && nav.classList.toggle('is-solid', scrollY > 30);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const tog = $('[data-nav-toggle]'), links = $('#nav-links');
  if (tog) {
    tog.addEventListener('click', () => {
      const open = tog.getAttribute('aria-expanded') !== 'true';
      tog.setAttribute('aria-expanded', open); links.classList.toggle('is-open', open);
    });
    $$('a', links).forEach(a => a.addEventListener('click', () => { tog.setAttribute('aria-expanded', 'false'); links.classList.remove('is-open'); }));
  }

  /* hero reel */
  const reel = $('[data-reel]');
  if (reel) {
    const slides = $$('[data-reel-slide]', reel), dots = $$('[data-reel-dot]'), now = $('[data-reel-now]');
    let i = 0, timer;
    const show = n => {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => s.classList.toggle('is-on', k === i));
      dots.forEach((d, k) => d.classList.toggle('is-on', k === i));
      if (now) { now.href = slides[i].dataset.href; now.querySelector('strong').textContent = slides[i].dataset.title; }
    };
    const play = () => { clearInterval(timer); if (!reduce) timer = setInterval(() => show(i + 1), 5500); };
    dots.forEach((d, k) => d.addEventListener('click', () => { show(k); play(); }));
    document.addEventListener('visibilitychange', () => document.hidden ? clearInterval(timer) : play());
    play();
  }

  /* carousels */
  $$('[data-carousel]').forEach(c => {
    const track = $('[data-car-track]', c), slides = $$('.car__slide', c), count = $('[data-car-count]', c);
    const step = dir => {
      const w = slides[0].getBoundingClientRect().width + 16;
      track.scrollBy({ left: dir * w, behavior: reduce ? 'auto' : 'smooth' });
    };
    $('[data-car-prev]', c).addEventListener('click', () => step(-1));
    $('[data-car-next]', c).addEventListener('click', () => step(1));
    let raf;
    track.addEventListener('scroll', () => {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(() => {
        const w = slides[0].getBoundingClientRect().width + 16;
        let idx = Math.round(track.scrollLeft / w);
        if (track.scrollLeft + track.clientWidth >= track.scrollWidth - 4) idx = slides.length - 1;
        count.textContent = `${Math.min(idx + 1, slides.length)} / ${slides.length}`;
      });
    }, { passive: true });
  });

  /* lightbox */
  const lb = $('[data-lightbox]');
  if (lb) {
    const im = $('[data-lb-img]', lb), cap = $('[data-lb-count]', lb);
    let set = [], at = 0, last;
    const show = n => { at = (n + set.length) % set.length; im.src = set[at]; cap.textContent = `${at + 1} / ${set.length}`; };
    const open = (list, n) => { set = list; last = document.activeElement; lb.hidden = false; document.body.style.overflow = 'hidden'; show(n); $('[data-lb-close]', lb).focus(); };
    const close = () => { lb.hidden = true; document.body.style.overflow = ''; im.removeAttribute('src'); last && last.focus(); };
    $$('[data-carousel]').forEach(c => {
      const btns = $$('[data-lb-src]', c), list = btns.map(b => b.dataset.lbSrc);
      btns.forEach((b, k) => b.addEventListener('click', () => open(list, k)));
    });
    $('[data-lb-close]', lb).addEventListener('click', close);
    $('[data-lb-prev]', lb).addEventListener('click', () => show(at - 1));
    $('[data-lb-next]', lb).addEventListener('click', () => show(at + 1));
    lb.addEventListener('click', e => { if (e.target === lb) close(); });
    addEventListener('keydown', e => {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(at - 1);
      if (e.key === 'ArrowRight') show(at + 1);
    });
    let x0 = null;
    lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) show(at + (dx < 0 ? 1 : -1)); x0 = null; });
  }

  /* lite YouTube: load the player only when clicked */
  /* YouTube refuses to play embeds on pages opened from disk (file://, no referrer: error 153),
     so locally we open the video on YouTube instead; on the live site it plays inline. */
  $$('[data-yt]').forEach(el => el.querySelector('.yt__play').addEventListener('click', () => {
    if (location.protocol === 'file:') { window.open(`https://www.youtube.com/watch?v=${el.dataset.yt}`, '_blank', 'noopener'); return; }
    const f = document.createElement('iframe');
    f.src = `https://www.youtube.com/embed/${el.dataset.yt}?autoplay=1&rel=0&origin=${encodeURIComponent(location.origin)}`;
    f.referrerPolicy = 'strict-origin-when-cross-origin';
    f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen; web-share';
    f.allowFullscreen = true; f.title = 'YouTube video';
    el.innerHTML = ''; el.appendChild(f);
  }));

  /* reveal on scroll */
  const rev = $$('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
    rev.forEach(r => io.observe(r));
  } else rev.forEach(r => r.classList.add('is-in'));
})();

/* game list under the intro drives the hero background */
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
