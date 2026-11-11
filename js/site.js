/* Lead-article rotation: switches every data-ms; tabs switch on click; pauses on hover/focus and via the button;
   no auto-rotation when the visitor prefers reduced motion. */
(function () {
  var root = document.querySelector('.tl'); if (!root) return;
  var slides = root.querySelectorAll('.tl-slide'), tabs = root.querySelectorAll('.tl-tab'), btn = root.querySelector('.tl-pause');
  var ms = +root.dataset.ms || 7000, i = 0, timer = null, held = false, user = false;
  var L = document.documentElement.lang === 'en' ? { play: 'Start rotation', pause: 'Pause rotation' }
    : { play: 'Automatisches Wechseln starten', pause: 'Automatisches Wechseln anhalten' };
  var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.classList.add('js'); root.style.setProperty('--ms', ms + 'ms');
  function show(n) {
    i = (n + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.classList.toggle('is-on', k === i); s.hidden = k !== i; });
    tabs.forEach(function (t, k) { t.classList.toggle('is-on', k === i); t.setAttribute('aria-selected', k === i); });
    restart();
  }
  function restart() {
    clearTimeout(timer); root.classList.remove('run'); void root.offsetWidth;
    if (still || held || user) return;
    root.classList.add('run'); timer = setTimeout(function () { show(i + 1); }, ms);
  }
  tabs.forEach(function (t, k) { t.addEventListener('click', function () { show(k); }); });
  btn.addEventListener('click', function () {
    user = !user; btn.textContent = user ? '▶' : '❚❚';
    btn.setAttribute('aria-label', user ? L.play : L.pause); restart();
  });
  root.addEventListener('mouseenter', function () { held = true; restart(); });
  root.addEventListener('mouseleave', function () { held = false; restart(); });
  root.addEventListener('focusin', function () { held = true; restart(); });
  root.addEventListener('focusout', function () { held = false; restart(); });
  if (still) { user = true; btn.textContent = '▶'; }
  show(0);
})();
