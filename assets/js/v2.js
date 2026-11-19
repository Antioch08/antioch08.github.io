/* Layout test: floating image preview that follows the cursor over work rows. */
(() => {
  const pv = document.querySelector('.preview'); if (!pv) return;
  const im = pv.querySelector('img');
  if (!matchMedia('(hover: hover) and (min-width: 981px)').matches) return;
  document.querySelectorAll('[data-preview]').forEach(row => {
    row.addEventListener('mouseenter', () => { im.src = row.dataset.preview; pv.classList.add('on'); });
    row.addEventListener('mouseleave', () => pv.classList.remove('on'));
    row.addEventListener('mousemove', ev => { pv.style.left = ev.clientX + 'px'; pv.style.top = ev.clientY + 'px'; });
  });
})();
