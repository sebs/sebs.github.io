// Carbon UI Shell — mobile side nav.
//
// Carbon's React SideNav is stateful; this is the same behaviour in ~30 lines
// of vanilla JS, driving the classes Carbon's CSS already ships:
// `cds--side-nav--expanded` on the panel and `cds--side-nav__overlay-active`
// on the scrim. Progressive enhancement — without JS the nav simply stays
// closed and the header menu bar still works from `lg` up.
(function () {
  var toggle = document.querySelector('[data-nav-toggle]');
  var nav = document.getElementById('site-side-nav');
  var overlay = document.querySelector('[data-nav-overlay]');
  if (!toggle || !nav) return;

  var openIcon = toggle.querySelector('[data-nav-icon="open"]');
  var closeIcon = toggle.querySelector('[data-nav-icon="close"]');

  function setOpen(open) {
    nav.classList.toggle('cds--side-nav--expanded', open);
    nav.setAttribute('aria-hidden', String(!open));
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    toggle.classList.toggle('cds--header__action--active', open);
    if (openIcon) openIcon.hidden = open;
    if (closeIcon) closeIcon.hidden = !open;
    if (overlay) overlay.classList.toggle('cds--side-nav__overlay-active', open);
  }

  toggle.addEventListener('click', function () {
    setOpen(!nav.classList.contains('cds--side-nav--expanded'));
  });

  if (overlay) overlay.addEventListener('click', function () { setOpen(false); });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') setOpen(false);
  });

  // Following a link inside the panel navigates away; close it either way so
  // in-page anchors (#projects, #writing) don't leave the nav covering them.
  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) setOpen(false);
  });
})();
