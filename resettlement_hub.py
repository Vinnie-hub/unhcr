"""Content blocks for the resettlement section, taken from the campaign image
(six-step process, third-country map, photo tiles, ongoing-support grid, hope band).
Imported by build_resettlement.py and build_site.py."""

R = "/resettlement"
IMGS = "/images/resettlement"

_P = {
    "people": '<circle cx="9" cy="8" r="3"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17" cy="9" r="2.5"/><path d="M16 14.2c2.8.3 5 2.6 5 5.8"/>',
    "search": '<circle cx="11" cy="11" r="6"/><path d="m20 20-4.2-4.2"/>',
    "docs": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4"/><path d="m9 14 2 2 4-4"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16 9.5"/>',
    "plane": '<path d="m21 4-6 16-4-6-6-4z"/><path d="M21 4 11 14"/>',
    "home": '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>',
    "heart": '<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
    "book": '<path d="M3 5h6a3 3 0 0 1 3 3v12a2 2 0 0 0-2-2H3z"/><path d="M21 5h-6a3 3 0 0 0-3 3v12a2 2 0 0 1 2-2h7z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2"/><path d="M3 13h18"/>',
    "community": '<circle cx="12" cy="7" r="3"/><circle cx="5" cy="10" r="2.2"/><circle cx="19" cy="10" r="2.2"/><path d="M6.5 20c0-3 2.5-5.5 5.5-5.5s5.5 2.5 5.5 5.5"/><path d="M1.5 18c0-2.3 1.6-4 3.5-4"/><path d="M22.5 18c0-2.3-1.6-4-3.5-4"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{_P[name]}</svg>')


# The six steps shown in the campaign image
STEPS = [
    ("Registration", "people", "with UNHCR or a partner organization."),
    ("Assessment &amp; Referral", "search", "for resettlement to a host country."),
    ("Interviews &amp; Screening", "docs", "including document verification, eligibility and security checks."),
    ("Approval", "check", "by the resettlement country."),
    ("Pre-departure Arrangements", "plane", "travel preparations and orientation."),
    ("Arrival &amp; Support", "home", "housing, healthcare, education, employment and community integration."),
]


def steps6():
    return '<ol class="steps6">' + "".join(
        f'<li class="step6"><span class="ico">{icon(i)}</span><h3>{t}</h3><p>{d[0].upper() + d[1:]}</p></li>'
        for t, i, d in STEPS) + "</ol>"


SUPPORT = [
    ("Housing", "home", "A safe place to live"),
    ("Healthcare", "heart", "Access to medical care"),
    ("Education", "book", "Schools, language and training"),
    ("Employment support", "briefcase", "Help to find work"),
    ("Community integration", "community", "Belonging and connection"),
]


def support_grid():
    return '<div class="support-grid">' + "".join(
        f'<div class="support-item"><span class="ico">{icon(i)}</span><span class="t">{t}</span><small>{s}</small></div>'
        for t, i, s in SUPPORT) + "</div>"


COUNTRIES = [  # slug, name, flag, (x, y) on the route map
    ("canada", "Canada", "🇨🇦", (92, 64)),
    ("united-kingdom", "UK", "🇬🇧", (232, 54)),
    ("sweden", "Sweden", "🇸🇪", (352, 40)),
    ("germany", "Germany", "🇩🇪", (292, 124)),
    ("australia", "Australia", "🇦🇺", (440, 242)),
]


def routes_svg():
    ox, oy = 205, 205
    arcs, pins = [], []
    for slug, name, flag, (x, y) in COUNTRIES:
        cx, cy = (ox + x) / 2, min(oy, y) - 38
        arcs.append(f'<path d="M{ox} {oy} Q{cx:.0f} {cy:.0f} {x} {y}" fill="none" stroke="#fff" stroke-width="1.6" stroke-dasharray="4 5" opacity=".75"/>')
        w = 26 + 8 * len(name)
        pins.append(
            f'<a href="{R}/countries/{slug}.html" aria-label="Resettlement to {name}"><g class="pin">'
            f'<rect x="{x - w / 2:.0f}" y="{y - 14}" width="{w}" height="28" rx="14" fill="#fff"/>'
            f'<text x="{x - w / 2 + 12:.0f}" y="{y + 5}" font-size="14">{flag}</text>'
            f'<text x="{x - w / 2 + 32:.0f}" y="{y + 5}" font-size="12" font-weight="700" fill="#18375f" font-family="Inter,Arial,sans-serif">{name}</text></g></a>')
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="1.6"/>' for x in range(20, 520, 20) for y in range(20, 290, 20))
    return (f'<svg class="routes" viewBox="0 0 520 290" role="img" aria-label="Refugees are resettled from first countries of asylum to Canada, the UK, Sweden, Germany and Australia">'
            f'<g fill="#fff" opacity=".18">{dots}</g>{"".join(arcs)}'
            f'<circle cx="{ox}" cy="{oy}" r="16" fill="#faeb00" opacity=".25"/><circle cx="{ox}" cy="{oy}" r="7" fill="#faeb00"/>'
            f'{"".join(pins)}</svg>')


def chips():
    return '<div class="chips">' + "".join(
        f'<a class="chip" href="{R}/countries/{s}.html"><span class="flag" aria-hidden="true">{f}</span>{ {"UK": "United Kingdom"}.get(n, n)}</a>'
        for s, n, f, _ in COUNTRIES) + "</div>"


def hub_body(free_callout):
    """Whole resettlement landing page (raw sections, full width)."""
    return f'''
<section class="section"><div class="container">
  <div class="split">
    <img src="{IMGS}/unhcr-guidance.webp" alt="A UNHCR staff member in a blue vest talks with a refugee family at a desk" width="909" height="381" loading="lazy">
    <div>
      <span class="eyebrow">Guidance. Information. Support.</span>
      <h2>UNHCR helps refugees find durable solutions</h2>
      <p class="lead">Durable solutions include resettlement to safer countries, alongside voluntary return and local integration.</p>
      <p>Resettlement is for refugees whose lives, safety or health are still at risk where they are. UNHCR identifies who is most in need and refers them to countries that have agreed to admit them.</p>
      <div class="links-inline"><a class="btn btn-primary" href="{R}/what-is-resettlement.html">What is resettlement?</a><a class="btn btn-outline" href="{R}/who-may-be-considered.html">Who may be considered?</a></div>
    </div>
  </div>
</div></section>

<section class="section alt" id="process"><div class="container">
  <div class="section-head" style="text-align:center;margin-inline:auto"><span class="eyebrow">The resettlement process</span><h2>A safer future, step by step</h2>
  <p class="lead">Six stages take a refugee from registration to a new home. Timelines vary from months to years.</p></div>
  {steps6()}
  <p class="tagline">Resettlement changes lives.</p>
  <p style="text-align:center;margin-top:18px"><a class="btn btn-primary" href="{R}/how-the-process-works.html">See the process in detail</a></p>
</div></section>

<section class="section band" id="third-countries"><div class="container"><div class="dest-grid">
  <div>
    <span class="eyebrow" style="color:#faeb00">Resettlement to third countries</span>
    <h2>A chance for a new life</h2>
    <p class="lead" style="color:#e6eef7">UNHCR works with countries like Canada, Australia, Sweden, Germany and the United Kingdom to offer refugees a chance for a new life.</p>
    {chips()}
  </div>
  {routes_svg()}
</div></div></section>

<section class="section"><div class="container">
  <div class="section-head"><h2>More than a journey</h2><p class="lead">Resettlement is a chance to rebuild lives, reunite families and create a future in safety.</p></div>
  <div class="trio">
    <article class="tile"><img src="{IMGS}/departing-family.webp" alt="A family with suitcases walks towards an aircraft" loading="lazy"><div><h3>New country. New opportunities.</h3><p>A brighter future begins the day a family boards the plane.</p></div></article>
    <article class="tile"><img src="{IMGS}/passport.webp" alt="A hand holding a passport beside an aircraft window" loading="lazy"><div><h3>Resettlement is more than a journey</h3><p>It&rsquo;s a chance to rebuild lives, reunite families and create a future in safety.</p></div></article>
    <article class="tile"><img src="{IMGS}/family-reunited.webp" alt="A family reunited at an arrivals hall, holding a small flag" loading="lazy"><div><h3>Families reunited. Lives reconstructed.</h3><p>Many families are welcomed together, or find their way back to each other.</p></div></article>
  </div>
</div></section>

<section class="section alt" id="beyond"><div class="container">
  <div class="section-head" style="text-align:center;margin-inline:auto"><span class="eyebrow">After arrival</span><h2>Beyond resettlement, ongoing support includes</h2></div>
  {support_grid()}
  <p class="note-band">Refugees are not just survivors, they are future contributors.</p>
  <p style="text-align:center;margin-top:14px"><a class="btn btn-primary" href="{R}/support-after-arrival.html">Read about support after arrival</a></p>
</div></section>

<section class="section quote-band"><img src="{IMGS}/hope-has-no-borders.webp" alt="" loading="lazy">
  <div class="container"><blockquote>Hope has no borders</blockquote><p>Every year, refugees who cannot return home or stay safely where they are begin again in a new country.</p>
  <div class="links-inline"><a class="btn btn-yellow" href="{R}/countries/canada.html">Explore resettlement countries</a><a class="btn btn-light" href="{R}/pathways/family-reunification.html">Other legal pathways</a></div></div></section>

<section class="section"><div class="container"><div class="section-head"><h2>Explore this section</h2><p class="lead">Start with the basics, then find the route that fits your situation.</p></div>
<div class="grid cols-3">
<a class="card" href="{R}/what-is-resettlement.html"><img src="/images/gallery/build-better-futures.webp" alt="" loading="lazy"><div class="card-body"><h3>Understanding Resettlement</h3><p>What it is, who may be considered, how the process works and answers to common questions.</p><span class="more">Learn more &rarr;</span></div></a>
<a class="card" href="{R}/countries/canada.html"><img src="/images/gallery/unhcr-works-in-122-countries.webp" alt="" loading="lazy"><div class="card-body"><h3>Resettlement countries</h3><p>How resettlement works in Canada, Australia, Sweden, Germany and the United Kingdom.</p><span class="more">See countries &rarr;</span></div></a>
<a class="card" href="{R}/pathways/family-reunification.html"><img src="/images/gallery/unhcr-familie-gathering.webp" alt="" loading="lazy"><div class="card-body"><h3>Other Legal Pathways</h3><p>Family reunification, humanitarian pathways, education and employment routes.</p><span class="more">View pathways &rarr;</span></div></a>
<a class="card" href="{R}/support-after-arrival.html"><img src="/images/gallery/unhcr-housing-resetttling.webp" alt="" loading="lazy"><div class="card-body"><h3>Support after arrival</h3><p>Housing, healthcare, education, employment support and community integration.</p><span class="more">Find out more &rarr;</span></div></a>
<a class="card" href="{R}/refugee-rights-and-protection.html"><img src="/images/gallery/protect-human-rights.webp" alt="" loading="lazy"><div class="card-body"><h3>Refugee Rights &amp; Protection</h3><p>The rights every refugee has under international law, wherever they are.</p><span class="more">Know your rights &rarr;</span></div></a>
<a class="card" href="{R}/faq.html"><img src="/images/gallery/opportunity-for-displaced-people.webp" alt="" loading="lazy"><div class="card-body"><h3>Frequently asked questions</h3><p>Short answers to the most common questions about resettlement and pathways.</p><span class="more">Read the FAQ &rarr;</span></div></a>
</div><div style="margin-top:28px">{free_callout}</div></div></section>
'''


def contact_form(topics=("General question", "Resettlement information", "Media enquiry", "Feedback on this website")):
    opts = "".join(f"<option>{t}</option>" for t in topics)
    return f'''<form class="form" data-demo>
  <p class="callout warn" style="margin:0">This is a class project demo. Nothing you type is sent or stored. Please do not enter real personal details.</p>
  <label>Full name<input name="name" autocomplete="name" required></label>
  <label>Email address<input name="email" type="email" autocomplete="email" required></label>
  <label>Topic<select name="topic">{opts}</select></label>
  <label>Message<textarea name="message" required></textarea></label>
  <button class="btn btn-primary" type="submit">Send message</button>
  <p class="demo-result" role="status" hidden></p>
</form>'''
