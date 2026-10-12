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
})();


/* ---- Contact / get-help form: sends to the form's action (Formspree) ---- */
(function () {
  'use strict';
  var form = document.getElementById('contact-form');
  if (!form) return;
  var button = form.querySelector('button[type="submit"]');
  var success = document.getElementById('contact-success');
  var error = document.getElementById('contact-error');
  if (!button) return;
  if (!error) {
    error = document.createElement('div');
    error.id = 'contact-error';
    error.className = 'form-error';
    error.setAttribute('role', 'alert');
    error.hidden = true;
    form.parentNode.insertBefore(error, form);
  }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function hide(el) { if (el) { el.hidden = true; el.classList.remove('visible', 'show'); } }
  function reveal(el, msg) {
    if (!el) return;
    if (msg) el.textContent = msg;
    el.hidden = false;
    el.classList.add('visible');
    el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    try { el.focus({ preventScroll: true }); } catch (e) {}
  }
  function clearInvalid() {
    Array.prototype.forEach.call(form.elements, function (el) {
      el.classList.remove('is-invalid');
      el.removeAttribute('aria-invalid');
    });
  }
  Array.prototype.forEach.call(form.elements, function (el) {
    el.addEventListener('input', function () {
      el.classList.remove('is-invalid');
      el.removeAttribute('aria-invalid');
    });
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (button.disabled) return;
    hide(success); hide(error); clearInvalid();

    var bad = Array.prototype.filter.call(form.elements, function (el) {
      return el.willValidate && !el.checkValidity();
    });
    if (bad.length) {
      bad.forEach(function (el) { el.classList.add('is-invalid'); el.setAttribute('aria-invalid', 'true'); });
      reveal(error, 'Please check the highlighted fields and try again.');
      bad[0].focus();
      return;
    }
    if (/YOUR_FORM_ID/.test(form.action)) {
      if (window.console) console.warn('Contact form: replace YOUR_FORM_ID in the form action with your Formspree form ID.');
      reveal(error, 'This form is not connected yet. Please email support@unhcr.org instead.');
      return;
    }

    var label = button.textContent;
    button.disabled = true;
    button.setAttribute('aria-busy', 'true');
    button.textContent = 'Sending\u2026';

    fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      headers: { Accept: 'application/json' }
    }).then(function (res) {
      if (res.ok) {
        form.reset();
        reveal(success);
        return;
      }
      return res.json().catch(function () { return {}; }).then(function (data) {
        var msg = data && data.errors && data.errors.map(function (x) { return x.message; }).join(', ');
        reveal(error, msg || 'Something went wrong. Please try again.');
      });
    }).catch(function () {
      reveal(error, 'Network error. Please check your connection and try again.');
    }).then(function () {
      button.disabled = false;
      button.removeAttribute('aria-busy');
      button.textContent = label;
    });
  });
})();

  (function () {
    const form = document.getElementById('newsletter-form');
    const success = document.getElementById('newsletter-success');
    const error = document.getElementById('newsletter-error');
    const button = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', async function (e) {
      e.preventDefault();

      success.hidden = true;
      error.hidden = true;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      const originalText = button.textContent;
      button.disabled = true;
      button.textContent = 'Subscribing…';

      try {
        const response = await fetch(form.action, {
          method: 'POST',
          body: new FormData(form),
          headers: { Accept: 'application/json' }
        });

        if (response.ok) {
          form.reset();
          success.hidden = false;
          success.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
          const data = await response.json().catch(() => ({}));
          error.textContent =
            data?.errors?.map(err => err.message).join(', ') ||
            'Something went wrong. Please try again.';
          error.hidden = false;
        }
      } catch (err) {
        error.textContent = 'Network error. Please check your connection and try again.';
        error.hidden = false;
      } finally {
        button.disabled = false;
        button.textContent = originalText;
      }
    });
  })();

/* ---- Floating WhatsApp button: dismiss for the session ---- */
(function () {
  'use strict';
  var wrap = document.getElementById('wa-float-wrap');
  var dismiss = document.getElementById('wa-dismiss');
  if (!wrap || !dismiss) return;
  var KEY = 'wa-dismissed';
  function dismissed() { try { return sessionStorage.getItem(KEY) === '1'; } catch (e) { return false; } }
  if (dismissed()) { wrap.classList.add('is-hidden'); return; }
  dismiss.addEventListener('click', function (e) {
    e.preventDefault();
    e.stopPropagation();
    wrap.classList.add('is-hidden');
    try { sessionStorage.setItem(KEY, '1'); } catch (err) {}
  });
})();
