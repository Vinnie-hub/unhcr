/* Shared site behaviour: header menu (hover on desktop, accordion on mobile), demo forms. */
(function () {
  'use strict';
  var header = document.getElementById('siteHeader');
  if (!header) return;
  var burger = header.querySelector('.sh-burger');
  var nav = document.getElementById('sh-nav');
  var items = Array.prototype.slice.call(header.querySelectorAll('.sh-item'));
  var desktop = window.matchMedia('(min-width: 992px)');
  var timers = new WeakMap();

  function setOpen(item, open) {
    item.classList.toggle('open', open);
    var caret = item.querySelector('.sh-caret');
    if (caret) caret.setAttribute('aria-expanded', String(open));
  }
  function closeAll(except) {
    items.forEach(function (it) { if (it !== except) setOpen(it, false); });
  }
  function setNav(open) {
    if (!nav || !burger) return;
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    if (!open) closeAll();
  }
  if (burger) burger.addEventListener('click', function () { setNav(!nav.classList.contains('open')); });

  items.forEach(function (item) {
    var caret = item.querySelector('.sh-caret');
    caret.addEventListener('click', function (ev) {
      ev.stopPropagation();
      var open = !item.classList.contains('open');
      closeAll(item);
      setOpen(item, open);
    });
    item.addEventListener('mouseenter', function () {
      if (!desktop.matches) return;
      clearTimeout(timers.get(item));
      closeAll(item);
      setOpen(item, true);
    });
    item.addEventListener('mouseleave', function () {
      if (!desktop.matches) return;
      timers.set(item, setTimeout(function () { setOpen(item, false); }, 140));
    });
    item.querySelector('.sh-link').addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowDown') {
        ev.preventDefault();
        closeAll(item);
        setOpen(item, true);
        var first = item.querySelector('.sh-panel a');
        if (first) first.focus();
      }
    });
    item.addEventListener('focusout', function (ev) {
      if (!item.contains(ev.relatedTarget)) setOpen(item, false);
    });
  });

  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    var openItem = items.filter(function (i) { return i.classList.contains('open'); })[0];
    closeAll();
    if (openItem && desktop.matches) openItem.querySelector('.sh-link').focus();
    else if (nav && nav.classList.contains('open')) { setNav(false); if (burger) burger.focus(); }
  });
  document.addEventListener('click', function (ev) {
    if (!ev.target.closest('.sh-header')) { closeAll(); if (!desktop.matches) setNav(false); }
  });
  desktop.addEventListener('change', function () { setNav(false); closeAll(); });

  function syncHeight() {
    document.documentElement.style.setProperty('--site-header-height', header.offsetHeight + 'px');
  }
  syncHeight();
  window.addEventListener('resize', syncHeight);
  window.addEventListener('load', syncHeight);

  /* demo forms: nothing is ever sent anywhere */
  Array.prototype.forEach.call(document.querySelectorAll('form[data-demo]'), function (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var note = form.querySelector('.demo-result');
      if (note) { note.hidden = false; note.textContent = 'Thank you. This is a class project demo, so nothing was sent or stored.'; }
      form.reset();
    });
  });
})();
