(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (!toggle || !nav) return;
  var subs = nav.querySelectorAll('.has-sub');

  function closeSubs(except) {
    subs.forEach(function (li) {
      if (li !== except) {
        li.classList.remove('open');
        li.querySelector('.sub-toggle').setAttribute('aria-expanded', 'false');
      }
    });
  }
  function setNav(open) {
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    if (!open) closeSubs();
  }

  toggle.addEventListener('click', function () {
    setNav(!nav.classList.contains('open'));
  });

  subs.forEach(function (li) {
    var btn = li.querySelector('.sub-toggle');
    btn.addEventListener('click', function () {
      var open = !li.classList.contains('open');
      closeSubs(li);
      li.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', String(open));
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { setNav(false); closeSubs(); toggle.focus(); }
  });
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.site-header')) { setNav(false); closeSubs(); }
  });
  window.matchMedia('(min-width: 992px)').addEventListener('change', function () {
    setNav(false);
  });
})();
