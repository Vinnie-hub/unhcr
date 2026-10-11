#!/usr/bin/env python3
"""Shared header / footer / navigation for every page of the site.

Edit NAV or the footer here, then re-run:
    python3 build_site.py          # re-applies the shell to all pages + builds new pages
    python3 build_resettlement.py  # rebuilds the resettlement section

CLASS PROJECT NOTE: this site is a student recreation. The DEMO_* constants drive the
notice shown at the top of every page and in the footer. Do not remove them.
"""
import html

LOGO = "/images/logos/unhcr-logo.svg"
FOOTER_LOGO = "/images/logos/unhcr-footer-logo.webp"
DEMO_SHORT = "Class project demo: not affiliated with UNHCR."
DEMO_LONG = ("This website is a class project that recreates the look of the UNHCR website for learning purposes. "
             "It is not operated, endorsed or approved by UNHCR, and it cannot process any request. "
             "The UNHCR name and logo belong to UNHCR.")
REAL_HELP_URL = "https://help.unhcr.org"
REAL_SITE_URL = "https://www.unhcr.org"


def e(s):
    return html.escape(s, quote=True)


# --------------------------------------------------------------------------- navigation
# (label, href, [(group title, [(link label, href), ...]), ...], promo=(image, title, text, href))
NAV = [
    ("About UNHCR", "/about.html", [
        ("Who we are", [
            ("Overview", "/about.html"),
            ("The High Commissioner", "/about/high-commissioner.html"),
            ("Mandate and governing charters", "/about.html#mandate"),
            ("Governance and oversight", "/about/governance-and-oversight.html"),
        ]),
        ("What we stand for", [
            ("Who we protect", "/about/who-we-protect.html"),
            ("Planning, funding and results", "/about/planning-funding-and-results.html"),
            ("Our partners", "/about/our-partners.html"),
            ("The 1951 Refugee Convention", "/about/refugee-convention.html"),
            ("Statelessness", "/about/statelessness.html"),
        ]),
    ], ("/images/gallery/the-high-level-event-commemorating-75-years-of-the-1951-refugee-convention.webp",
        "75 years of the Refugee Convention", "How the 1951 Convention still protects people forced to flee.",
        "/about/refugee-convention.html")),

    ("What we do", "/what-we-do.html", [
        ("Our work", [
            ("Respond to emergencies", "/what-we-do.html#respond-to-emergencies"),
            ("Protect human rights", "/what-we-do.html#protect-human-rights"),
            ("Build better futures", "/what-we-do.html#build-better-futures"),
        ]),
        ("Data and support", [
            ("Data and publications", "/what-we-do/data-and-publications.html"),
            ("Resettlement and safe pathways", "/resettlement/index.html"),
            ("Get help", "/get-help.html"),
        ]),
    ], ("/images/gallery/respond-to-emergencies.webp", "Responding to emergencies",
        "Life-saving shelter, food, water and protection when people are forced to flee.",
        "/what-we-do.html#respond-to-emergencies")),

    ("Where we work", "/where-we-work.html", [
        ("Regions", [
            ("Eastern and Southern Africa", "/regions/eastern-and-southern-africa.html"),
            ("West and Central Africa", "/regions/west-and-central-africa.html"),
            ("Middle East and North Africa", "/regions/middle-east-and-north-africa.html"),
            ("Asia and Pacific", "/regions/asia-and-pacific.html"),
            ("Europe", "/regions/europe.html"),
            ("Americas", "/regions/americas.html"),
        ]),
        ("Country sites", [
            ("Kenya", "/countries/kenya.html"),
            ("Uganda", "/countries/uganda.html"),
            ("Rwanda", "/countries/rwanda.html"),
            ("Nigeria", "/countries/nigeria.html"),
            ("Egypt", "/countries/egypt.html"),
            ("Canada", "/countries/canada.html"),
            ("United States", "/countries/united-states.html"),
            ("All country sites", "/country-sites.html"),
        ]),
    ], ("/images/gallery/unhcr-works-in-122-countries.webp", "Working in 122 countries",
        "Browse every country and regional site in one place.", "/country-sites.html")),

    ("News and stories", "/news-and-stories.html", [
        ("Read", [
            ("Latest news and stories", "/news-and-stories.html"),
            ("Press releases", "/news-and-stories/press-releases.html"),
            ("Media centre", "/news-and-stories/media-centre.html"),
        ]),
        ("Stay in touch", [
            ("Sign up for updates", "/get-involved/sign-and-stay-informed.html"),
            ("Contact UNHCR", "/contact.html"),
        ]),
    ], ("/images/gallery/stories-hero.webp", "Stories from the field",
        "The people and the moments behind the numbers.", "/news-and-stories.html")),

    ("Resettlement", "/resettlement/index.html", [
        ("Understanding resettlement", [
            ("What is resettlement?", "/resettlement/what-is-resettlement.html"),
            ("Who may be considered?", "/resettlement/who-may-be-considered.html"),
            ("How the process works", "/resettlement/how-the-process-works.html"),
            ("Support after arrival", "/resettlement/support-after-arrival.html"),
            ("Frequently asked questions", "/resettlement/faq.html"),
        ]),
        ("Resettlement countries", [
            ("Canada", "/resettlement/countries/canada.html"),
            ("Australia", "/resettlement/countries/australia.html"),
            ("Sweden", "/resettlement/countries/sweden.html"),
            ("Germany", "/resettlement/countries/germany.html"),
            ("United Kingdom", "/resettlement/countries/united-kingdom.html"),
        ]),
        ("Other legal pathways", [
            ("Family reunification", "/resettlement/pathways/family-reunification.html"),
            ("Humanitarian pathways", "/resettlement/pathways/humanitarian-pathways.html"),
            ("Education", "/resettlement/pathways/education.html"),
            ("Employment", "/resettlement/pathways/employment.html"),
            ("Refugee rights and protection", "/resettlement/refugee-rights-and-protection.html"),
        ]),
    ], ("/images/resettlement/family-reunited.webp", "Resettlement changes lives",
        "From crisis to safety. From displacement to opportunity.", "/resettlement/index.html")),

    ("Get involved", "/get-involved.html", [
        ("Ways to help", [
            ("Ways to give", "/get-involved.html#ways-to-give"),
            ("Partner with us", "/get-involved/partner-with-us.html"),
            ("Volunteer and advocate", "/get-involved.html#take-action"),
        ]),
        ("Stay informed", [
            ("Stay informed", "/get-involved.html#stay-informed"),
            ("Sign up for updates", "/get-involved/sign-and-stay-informed.html"),
            ("Beware of fraud", "/beware-of-fraud.html"),
        ]),
    ], ("/images/gallery/build-better-futures.webp", "Build better futures",
        "Every action helps someone forced to flee rebuild their life.", "/get-involved.html")),
]

SOCIAL = [
    ("X", "https://x.com/refugees"), ("Facebook", "https://www.facebook.com/UNHCR"),
    ("Instagram", "https://www.instagram.com/refugees/"), ("YouTube", "https://www.youtube.com/c/unhcr"),
    ("TikTok", "https://www.tiktok.com/@refugees"), ("LinkedIn", "https://www.linkedin.com/company/unhcr/"),
]


def active_index(path):
    """Which top-level nav item a page belongs to."""
    p = "/" + path.lstrip("/")
    rules = [("/about", 0), ("/what-we-do", 1), ("/where-we-work", 2), ("/countries", 2), ("/regions", 2),
             ("/country-sites", 2), ("/news-and-stories", 3), ("/resettlement", 4), ("/get-involved", 5)]
    for prefix, i in rules:
        if p.startswith(prefix):
            return i
    return None


def _nav_items(path):
    act = active_index(path)
    cur = "/" + path.lstrip("/")
    out = []
    for i, (label, href, groups, promo) in enumerate(NAV):
        is_act = i == act
        cols = []
        for gt, links in groups:
            li = "".join(
                f'<li><a href="{u}"{" aria-current=\"page\"" if u == cur else ""}>{e(t)}</a></li>' for t, u in links)
            cols.append(f'<div class="sh-group"><h3 class="sh-gt">{e(gt)}</h3><ul>{li}</ul></div>')
        img, pt, ptxt, purl = promo
        promo_html = (f'<a class="sh-promo" href="{purl}"><img src="{img}" alt="" loading="lazy">'
                      f'<span><strong>{e(pt)}</strong><span>{e(ptxt)}</span></span></a>')
        out.append(
            f'<li class="sh-item{" is-active" if is_act else ""}">'
            f'<a class="sh-link" href="{href}"{" aria-current=\"true\"" if is_act else ""}>{e(label)}</a>'
            f'<button class="sh-caret" type="button" aria-expanded="false" aria-label="Show {e(label)} menu"></button>'
            f'<div class="sh-panel"><div class="sh-wrap sh-panel-grid" style="--cols:{len(cols)}">'
            f'{"".join(cols)}{promo_html}</div></div></li>')
    return "".join(out)


def header(path="/index.html", home=False):
    """Full site header. `home=True` makes Change site a button that opens the index.html overlay."""
    if home:
        change = ('<button type="button" class="sh-change" id="sitesToggler" aria-expanded="false" '
                  'aria-controls="sitesOverlay">Change site <span class="sh-arrow" aria-hidden="true"></span></button>')
    else:
        change = ('<a class="sh-change" href="/country-sites.html" id="sitesToggler">Change site '
                  '<span class="sh-arrow" aria-hidden="true"></span></a>')
    return f'''<a class="sh-skip" href="#main">Skip to content</a>
<header class="sh-header" id="siteHeader">
  <div class="sh-top"><div class="sh-wrap sh-top-in">
    <p class="sh-demo"><span class="sh-chip">Demo</span> <span class="sh-demo-text">{e(DEMO_SHORT)} For real help, visit <a href="{REAL_HELP_URL}" rel="noopener">help.unhcr.org</a>.</span></p>
    <div class="sh-top-right"><span class="sh-site">UNHCR global website: {change}</span>
      <span class="sh-langs" aria-label="Languages (demo)"><span class="on">English</span><span>Français</span><span>Español</span><span>عربي</span></span></div>
  </div></div>
  <div class="sh-bar"><div class="sh-wrap sh-bar-in">
    <a class="sh-logo" href="/index.html" aria-label="UNHCR home"><img src="{LOGO}" alt="UNHCR" width="120" height="44"><span class="sh-logo-text">UNHCR<small>The UN Refugee Agency</small></span></a>
    <div class="sh-actions"><a class="sh-btn sh-btn-blue" href="/contact.html">Contact</a><a class="sh-btn sh-btn-navy" href="/get-help.html">Get help</a>
      <button class="sh-burger" type="button" aria-expanded="false" aria-controls="sh-nav" aria-label="Menu"><span class="sh-bars" aria-hidden="true"></span></button></div>
  </div></div>
  <nav class="sh-nav" id="sh-nav" aria-label="Main navigation"><div class="sh-wrap"><ul class="sh-list">{_nav_items(path)}</ul></div></nav>
</header>
<div id="main" tabindex="-1"></div>'''


def footer():
    def col(title, links):
        return (f'<div class="sh-fcol"><h3>{e(title)}</h3><ul>' +
                "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in links) + '</ul></div>')

    about = [("About UNHCR", "/about.html"), ("What we do", "/what-we-do.html"), ("Where we work", "/where-we-work.html"),
             ("News and stories", "/news-and-stories.html"), ("Data and publications", "/what-we-do/data-and-publications.html"),
             ("All country sites", "/country-sites.html")]
    resett = [("What is resettlement?", "/resettlement/what-is-resettlement.html"),
              ("How the process works", "/resettlement/how-the-process-works.html"),
              ("Resettlement countries", "/resettlement/countries/canada.html"),
              ("Other legal pathways", "/resettlement/pathways/family-reunification.html"),
              ("Support after arrival", "/resettlement/support-after-arrival.html"),
              ("Frequently asked questions", "/resettlement/faq.html")]
    help_ = [("Get help", "/get-help.html"), ("Get involved", "/get-involved.html"),
             ("Sign up for updates", "/get-involved/sign-and-stay-informed.html"), ("Contact UNHCR", "/contact.html"),
             ("Media centre", "/news-and-stories/media-centre.html"), ("Beware of fraud", "/beware-of-fraud.html"),
             ("Report misconduct or abuse", "/contact.html#report-misconduct"), ("Become a supplier", "/contact.html#suppliers")]
    social = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t, u in SOCIAL)
    return f'''<footer class="sh-footer">
  <div class="sh-demo-foot"><div class="sh-wrap"><strong>Class project demo.</strong> {e(DEMO_LONG)} Need real help? Visit <a href="{REAL_HELP_URL}" rel="noopener">help.unhcr.org</a>.</div></div>
  <div class="sh-wrap">
    <div class="sh-fgrid">
      <div class="sh-fcol sh-fbrand"><img src="{FOOTER_LOGO}" alt="UNHCR" height="40"><p>UNHCR, the UN Refugee Agency, leads international action to protect people forced to flee conflict and persecution.</p>
        <p><a class="sh-btn sh-btn-outline" href="/get-involved/sign-and-stay-informed.html">Stay informed</a></p></div>
      {col("About and work", about)}{col("Resettlement", resett)}{col("Help and contact", help_)}
      <div class="sh-fcol"><h3>Stay connected</h3><ul>{social}</ul></div>
    </div>
    <div class="sh-fbottom">
      <div class="sh-flinks"><a href="/privacy.html">Privacy notice</a><a href="/terms.html">Terms and conditions of use</a><a href="/privacy.html#cookie-notice">Cookies</a><a href="/terms.html#copyright">Copyright</a><a href="/sitemap.html">Sitemap</a></div>
      <div class="sh-copy">&copy; 2026 Class project. UNHCR name and logo are the property of UNHCR.</div>
    </div>
  </div>
</footer>'''


HEAD_LINKS = '<link rel="stylesheet" href="/css/site.css">'
BODY_SCRIPT = '<script src="/js/main.js" defer></script>'
