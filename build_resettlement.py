#!/usr/bin/env python3
"""Generates the resettlement section pages. Run: python3 build_resettlement.py
Edit the content in PAGES below, then re-run to regenerate the HTML files."""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
PHONE, PHONE_TEL = "+1 (343) 946-0343", "+13439460343"
SUPPORT = "support.unhcragencies.org"
SUPPORT_URL = "https://support.unhcragencies.org"
WA_NUMBER = "13439460343"  # change here if the WhatsApp number differs from the phone number
WA_URL = f"https://wa.me/{WA_NUMBER}?text=Hello%20UNHCR%2C%20I%20would%20like%20guidance%20on%20resettlement%20and%20legal%20pathways."
WA_ICON = '<svg class="wa-ico" viewBox="0 0 32 32" width="22" height="22" aria-hidden="true" fill="currentColor"><path d="M16.04 3C9.4 3 4 8.4 4 15.03c0 2.37.69 4.58 1.88 6.45L4 29l7.7-1.84a12 12 0 0 0 4.34.8C22.68 27.96 28 22.6 28 15.97 28 9.35 22.68 3 16.04 3Zm0 22.1c-1.4 0-2.77-.37-3.97-1.07l-.28-.17-4.57 1.09 1.2-4.45-.19-.3a9.9 9.9 0 0 1-1.52-5.27c0-5.5 4.5-9.97 10.03-9.97 5.52 0 10 4.47 10 9.97 0 5.5-4.48 9.97-10 9.97l-.7.2Zm5.5-7.46c-.3-.15-1.78-.88-2.05-.98-.28-.1-.48-.15-.68.15-.2.3-.78.98-.95 1.18-.18.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.78-1.67-2.08-.18-.3-.02-.46.13-.6.14-.13.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.68-1.64-.93-2.25-.25-.58-.5-.5-.68-.51h-.58c-.2 0-.53.08-.8.38-.28.3-1.05 1.02-1.05 2.5s1.08 2.9 1.23 3.1c.15.2 2.1 3.2 5.1 4.48.7.3 1.26.5 1.7.63.72.23 1.37.2 1.88.12.58-.09 1.78-.73 2.03-1.43.25-.7.25-1.3.18-1.43-.08-.13-.28-.2-.58-.35Z"/></svg>'
U = "https://images.unsplash.com/photo-"
IMG = {
    "a": U + "1593113598332-cd288d649433",
    "b": U + "1523803326055-1345a7c6a5c6",
    "c": U + "1469571486292-0ba58a3f068b",
    "d": U + "1488521787991-ed7bbaae773c",
    "e": U + "1509099836639-18ba1795216d",
}
def img(k, w): return f"{IMG[k]}?w={w}&q=80"

R = "/resettlement"
GROUPS = {
    "understanding": ("Understanding Resettlement", [
        ("What is resettlement?", f"{R}/what-is-resettlement.html"),
        ("Who may be considered?", f"{R}/who-may-be-considered.html"),
        ("How the process works", f"{R}/how-the-process-works.html"),
        ("Frequently asked questions", f"{R}/faq.html")]),
    "countries": ("Countries", [
        ("Australia", f"{R}/countries/australia.html"),
        ("Sweden", f"{R}/countries/sweden.html"),
        ("Germany", f"{R}/countries/germany.html"),
        ("United Kingdom", f"{R}/countries/united-kingdom.html")]),
    "pathways": ("Other Legal Pathways", [
        ("Family reunification", f"{R}/pathways/family-reunification.html"),
        ("Humanitarian pathways", f"{R}/pathways/humanitarian-pathways.html"),
        ("Education", f"{R}/pathways/education.html"),
        ("Employment", f"{R}/pathways/employment.html")]),
}
RIGHTS = f"{R}/refugee-rights-and-protection.html"
CONTACT = f"{R}/contact.html"

def e(s): return html.escape(s, quote=True)

def nav(current_url, group):
    out = []
    for key, (label, items) in GROUPS.items():
        act = " active" if key == group else ""
        links = "".join(
            f'<li><a href="{u}"{" aria-current=\"page\"" if u == current_url else ""}>{e(t)}</a></li>' for t, u in items)
        out.append(f'<li class="has-sub"><button class="sub-toggle{act}" aria-expanded="false">{e(label)}</button><ul class="sub">{links}</ul></li>')
    out.append(f'<li><a href="{RIGHTS}"{" class=\"active\" aria-current=\"page\"" if current_url == RIGHTS else ""}>Refugee Rights &amp; Protection</a></li>')
    out.append(f'<li><a href="{CONTACT}"{" class=\"active\" aria-current=\"page\"" if current_url == CONTACT else ""}>Contact</a></li>')
    return "".join(out)

def header(url, group):
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-top"><div class="container">
    <a class="change-site" href="/country-sites.html">Change site <span class="chev" aria-hidden="true"></span></a>
    <div class="ht-links">
      <a href="tel:{PHONE_TEL}">&#9742; {PHONE}</a>
      <a href="{SUPPORT_URL}" rel="noopener">{SUPPORT}</a>
    </div>
  </div></div>
  <div class="header-main"><div class="container">
    <a href="{R}/index.html" class="logo" aria-label="UNHCR Resettlement home">
      <img src="/images/logos/unhcr favicon.webp" alt="UNHCR" width="40" height="40">
      <div class="logo-text">UNHCR Resettlement<span>The UN Refugee Agency</span></div>
    </a>
    <div class="header-right">
      <div class="header-actions">
        <a href="{CONTACT}" class="btn btn-primary">Contact</a>
        <a href="/get-help.html" class="btn btn-dark">Get help</a>
      </div>
      <button class="nav-toggle" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu"><span class="bars" aria-hidden="true"></span></button>
    </div>
  </div></div>
  <nav class="main-nav" id="primary-nav" aria-label="Resettlement navigation"><div class="container"><ul class="nav-list">{nav(url, group)}<li class="nav-phone"><a href="tel:{PHONE_TEL}">&#9742; Call {PHONE}</a></li><li class="nav-phone nav-wa"><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp us</a></li></ul></div></nav>
</header>'''

def footer():
    def col(group):
        label, items = GROUPS[group]
        return f'<div><h3>{e(label)}</h3><ul>' + "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in items) + '</ul></div>'
    return f'''<footer class="site-footer"><div class="container">
  <div class="footer-grid">
    <div><h3>UNHCR Resettlement</h3><p>Information on resettlement and other safe, legal pathways for refugees.</p>
      <p style="margin-top:10px"><strong>UNHCR services are always free.</strong></p>
      <p style="margin-top:14px"><a class="btn btn-light btn-sm" href="{CONTACT}">Contact us</a></p></div>
    {col("understanding")}{col("pathways")}
    <div><h3>Contact</h3><ul>
      <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
      <li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp us</a></li>
      <li><a href="{SUPPORT_URL}" rel="noopener">{SUPPORT}</a></li>
      <li><a href="{RIGHTS}">Refugee Rights &amp; Protection</a></li>
      <li><a href="{CONTACT}">Contact page</a></li></ul></div>
  </div>
  <div class="footer-bottom">
    <img src="/images/logos/unhcr-footer-logo.webp" alt="UNHCR" height="36">
    <div><a href="/privacy.html">Privacy notice</a> &nbsp;·&nbsp; &copy; UNHCR 2001–2026</div>
  </div>
</div></footer>'''

def page(p):
    url, group = p["url"], p.get("group")
    crumbs = [("Home", "/index.html"), ("Resettlement", f"{R}/index.html")]
    if group: crumbs.append((GROUPS[group][0], None))
    bc = "".join(f'<li><a href="{u}">{e(t)}</a></li>' if u else f"<li>{e(t)}</li>" for t, u in crumbs)
    if url != f"{R}/index.html": bc += f'<li aria-current="page">{e(p["crumb"])}</li>'
    else: bc = '<li><a href="/index.html">Home</a></li><li aria-current="page">Resettlement</li>'
    actions = "".join(f'<a class="btn {c}" href="{u}">{e(t)}</a>' for t, u, c in p.get("actions", []))
    hero = f'''<section class="hero{"" if p.get("big") else " sm"}" style="background-image:url('{img(p["hero"], 1600)}')">
  <div class="container"><span class="hero-tag">{e(p["tag"])}</span><h1>{e(p["h1"])}</h1><p>{e(p["lead"])}</p>{f'<div class="actions">{actions}</div>' if actions else ""}</div></section>'''
    side = ""
    if group:
        label, items = GROUPS[group]
        side += f'<div class="panel"><h3>{e(label)}</h3><ul>' + "".join(
            f'<li><a href="{u}"{" aria-current=\"page\"" if u == url else ""}>{e(t)}</a></li>' for t, u in items) + "</ul></div>"
    side += f'''<div class="panel"><h3>Need to talk to someone?</h3><p style="font-size:.95rem">Call <a href="tel:{PHONE_TEL}">{PHONE}</a> or visit <a href="{SUPPORT_URL}" rel="noopener">{SUPPORT}</a>.</p><p style="font-size:.85rem;color:var(--muted);margin-top:8px">UNHCR never asks for money to process resettlement.</p></div>'''
    body = f'<div class="layout"><div class="article">{p["body"]}</div><aside class="aside" aria-label="Related">{side}</aside></div>' if p.get("layout", True) else p["body"]
    cta = p.get("cta", ("Questions about your situation?", "Our team can point you to the right information and services.", "Contact us", CONTACT))
    return f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p["title"])} | UNHCR</title>
<meta name="description" content="{e(p["lead"])}">
<meta name="theme-color" content="#1a2a3a">
<link rel="icon" href="/images/logos/unhcr favicon.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
</head>
<body>
{header(url, group)}
<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol>{bc}</ol></div></nav>
<main id="main">
{hero}
<section class="section"><div class="container">{body}</div></section>
{p.get("extra", "")}
<section class="section cta"><div class="container"><h2>{e(cta[0])}</h2><p>{e(cta[1])}</p><a class="btn btn-yellow" href="{cta[3]}">{e(cta[2])}</a></div></section>
</main>
{footer()}
<script src="/js/main.js" defer></script>
</body>
</html>
'''

def facts(rows):
    return '<div class="table-wrap"><table><tbody>' + "".join(f"<tr><th scope='row'>{a}</th><td>{b}</td></tr>" for a, b in rows) + "</tbody></table></div>"

def steps(items):
    return '<ol class="steps">' + "".join(f"<li><strong>{a}</strong>{b}</li>" for a, b in items) + "</ol>"

def ul(items): return '<ul class="list">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def call(t, warn=False): return f'<div class="callout{" warn" if warn else ""}">{t}</div>'

FREE = call("<strong>Resettlement is always free.</strong> UNHCR does not charge fees, sell places or accept applications through agents. If someone asks you for money, they are not acting for UNHCR.", True)
CHECK = call("Programmes, quotas and eligibility rules change often. Always confirm current details with the official government source linked on this page.")

def country(slug, name, hero, lead, rows, sections, official, official_name):
    return dict(url=f"{R}/countries/{slug}.html", group="countries", crumb=name, title=f"Resettlement to {name}", tag="Resettlement country",
        h1=name, lead=lead, hero=hero,
        body=f"<h2>At a glance</h2>{facts(rows)}{sections}{CHECK}<p>Official information: <a href='{official}' rel='noopener' target='_blank'>{official_name}</a></p>")

def pathway(slug, name, hero, lead, body):
    return dict(url=f"{R}/pathways/{slug}.html", group="pathways", crumb=name, title=name, tag="Other legal pathway", h1=name, lead=lead, hero=hero,
        body=body + call("<strong>Pathways are in addition to resettlement</strong>, not a replacement. Having a place on a pathway does not affect your refugee status, and UNHCR does not charge for any pathway."))

PAGES = []

PAGES.append(dict(url=f"{R}/index.html", group=None, big=True, crumb="Resettlement", title="Resettlement and safe pathways", tag="UNHCR Resettlement",
    h1="Safe, legal routes to a new future", hero="a",
    lead="Resettlement and other legal pathways help refugees who cannot return home or stay safely where they are to rebuild their lives in a new country.",
    actions=[("What is resettlement?", f"{R}/what-is-resettlement.html", "btn-yellow"), ("Contact us", CONTACT, "btn-light")],
    layout=False,
    body=f'''<div class="section-head"><h2>Explore this section</h2><p class="lead">Start with the basics, then find the route that fits your situation.</p></div>
<div class="grid cols-3">
<a class="card" href="{R}/what-is-resettlement.html"><img src="{img("b",700)}" alt="" loading="lazy"><div class="card-body"><h3>Understanding Resettlement</h3><p>What it is, who may be considered, how the process works and answers to common questions.</p><span class="more">Learn more &rarr;</span></div></a>
<a class="card" href="{R}/countries/australia.html"><img src="{img("c",700)}" alt="" loading="lazy"><div class="card-body"><h3>Countries</h3><p>How resettlement works in Australia, Sweden, Germany and the United Kingdom.</p><span class="more">See countries &rarr;</span></div></a>
<a class="card" href="{R}/pathways/family-reunification.html"><img src="{img("d",700)}" alt="" loading="lazy"><div class="card-body"><h3>Other Legal Pathways</h3><p>Family reunification, humanitarian pathways, education and employment routes.</p><span class="more">View pathways &rarr;</span></div></a>
<a class="card" href="{RIGHTS}"><img src="{img("e",700)}" alt="" loading="lazy"><div class="card-body"><h3>Refugee Rights &amp; Protection</h3><p>The rights every refugee has under international law, wherever they are.</p><span class="more">Know your rights &rarr;</span></div></a>
<a class="card" href="{CONTACT}"><img src="{img("a",700)}" alt="" loading="lazy"><div class="card-body"><h3>Contact</h3><p>Call {PHONE} or visit {SUPPORT}.</p><span class="more">Get in touch &rarr;</span></div></a>
</div><div style="margin-top:28px">{FREE}</div>''',
    cta=("Need help right now?", "Speak to our team by phone or visit our support site.", "Contact us", CONTACT)))

PAGES.append(dict(url=f"{R}/what-is-resettlement.html", group="understanding", crumb="What is resettlement?", title="What is resettlement?", tag="Understanding Resettlement",
    h1="What is resettlement?", hero="b",
    lead="Resettlement is the safe transfer of refugees from a country where they sought protection to another country that has agreed to admit them.",
    body=f'''<p class="lead">It is one of three lasting (“durable”) solutions for refugees, alongside voluntary return and local integration.</p>
<h2>A solution for those who need it most</h2>
<p>Resettled refugees are given legal protection, usually permanent residence, and the chance to eventually become citizens. Resettlement is for refugees whose lives, safety or health remain at risk, or who have no realistic prospect of another lasting solution.</p>
<h2>The key facts</h2>
{ul(["Only a small share of the world’s refugees are ever resettled; far more people need it than there are places offered.",
"Resettlement is voluntary for countries. Each government decides how many people to accept and on what terms.",
"UNHCR identifies and refers refugees in need. The resettlement country makes the final decision.",
"Refugees cannot apply directly to UNHCR to be resettled, and cannot choose the country."])}
<h2>Three lasting solutions</h2>
{facts([("Voluntary return","Going home in safety and dignity when conditions allow."),("Local integration","Building a permanent life in the country of asylum."),("Resettlement","Moving to a third country that offers lasting protection.")])}
{FREE}'''))

PAGES.append(dict(url=f"{R}/who-may-be-considered.html", group="understanding", crumb="Who may be considered?", title="Who may be considered for resettlement?", tag="Understanding Resettlement",
    h1="Who may be considered?", hero="c",
    lead="UNHCR submits refugees for resettlement based on vulnerability and protection needs, not on nationality, wealth or connections.",
    body=f'''<h2>You must first be a refugee</h2>
<p>Only people recognised as refugees, by a government or by UNHCR, can be considered. Being registered or recognised does not guarantee resettlement.</p>
<h2>Submission categories</h2>
<p>UNHCR looks at whether a person falls into one of these groups:</p>
{ul(["<strong>Legal and physical protection needs</strong>, including risk of being sent back to danger.","<strong>Survivors of violence and torture</strong> who need specialised care.","<strong>Medical needs</strong>, including life-threatening conditions where treatment is unavailable.","<strong>Women and girls at risk</strong> of harm because of their gender.","<strong>Children and adolescents at risk</strong>, including unaccompanied children.","<strong>Family reunification</strong> where separation causes serious hardship.","<strong>No foreseeable alternative</strong> lasting solution."])}
<h2>What also matters</h2>
<p>Countries set their own priorities and criteria, such as nationality groups or regions. UNHCR matches referrals to what each country accepts, so being eligible in principle does not mean being referred.</p>
{call("<strong>Important:</strong> UNHCR decides who it refers using its own assessment. You can keep your registration details up to date and tell staff about changes in your circumstances, but you cannot pay or apply to be selected.")}
{FREE}'''))

PAGES.append(dict(url=f"{R}/how-the-process-works.html", group="understanding", crumb="How the process works", title="How the resettlement process works", tag="Understanding Resettlement",
    h1="How the process works", hero="d",
    lead="From registration to arrival, resettlement can take months or years. Here are the main stages.",
    body=f'''{steps([("Registration","You register with UNHCR or the host government and your details are recorded."),
("Refugee status","Your claim is assessed (refugee status determination) if you are not already recognised."),
("Needs assessment","UNHCR staff assess whether resettlement is the right solution and whether you meet submission criteria."),
("Referral","If suitable, your case is referred to a resettlement country, which may also receive cases through its own selection missions."),
("Country decision","The country interviews you, runs security and medical checks, and decides whether to accept you."),
("Travel preparation","Cultural orientation, travel documents and health checks are arranged, typically with IOM."),
("Arrival and integration","You are received, housed and supported with language, schooling, health care and work.")])}
<h2>How long does it take?</h2>
<p>Timelines vary widely by country, case and security situation. Do not rely on anyone who promises a date.</p>
{FREE}
{call("<strong>Keep your details current.</strong> Tell UNHCR if your phone number, address or family situation changes so that you can be reached.")}''',
    cta=("Have a question about the process?", "Find answers to common questions or speak to our team.", "Read the FAQ", f"{R}/faq.html")))

faqs = [
("Can I apply for resettlement directly?","No. UNHCR identifies and refers refugees. Individuals cannot apply to UNHCR for resettlement or choose a destination country."),
("Does it cost money?","No. Every step is free. Anyone asking for payment, including for “priority” or “guaranteed” places, is committing fraud. Report it."),
("How do I know if I am being considered?","UNHCR will contact you directly using your registered details. Keep them up to date."),
("Can I choose which country I go to?","No. The resettlement country decides, and UNHCR matches cases to countries’ criteria."),
("Can my family come with me?","Immediate family members usually travel together if they are part of the same case. Contact UNHCR about relatives in other places."),
("What if I am not selected?","Not being selected does not affect your refugee status or protection. Other pathways, such as family reunification, education or employment routes, may be possible."),
("How long does it take?","It varies from months to many years, depending on the country, security checks and available places."),
("What is the difference between resettlement and a complementary pathway?","Resettlement is led by UNHCR referral. Pathways such as study or work visas are separate routes you may apply to yourself or through partners."),
("Who can I trust for information?","Official UNHCR channels and government immigration websites only. See our Contact page for how to verify."),
("Where can I get help right now?",f"Call <a href='tel:{PHONE_TEL}'>{PHONE}</a>, <a href='{WA_URL}' target='_blank' rel='noopener'>message us on WhatsApp</a> or visit <a href='{SUPPORT_URL}' rel='noopener'>{SUPPORT}</a>.")]
PAGES.append(dict(url=f"{R}/faq.html", group="understanding", crumb="Frequently asked questions", title="Frequently asked questions", tag="Understanding Resettlement",
    h1="Frequently asked questions", hero="e", lead="Short answers to common questions about resettlement and other pathways.",
    body="".join(f'<details{" open" if i == 0 else ""}><summary>{q}</summary><div class="answer"><p>{a}</p></div></details>' for i, (q, a) in enumerate(faqs)) + FREE))

# ---- Countries
PAGES.append(country("australia", "Australia", "c", "Australia accepts refugees through its Humanitarian Program, including referrals from UNHCR and community sponsorship.",
    [("Main programme","Offshore Humanitarian Program (Refugee and Special Humanitarian categories)"),("Referrals","UNHCR refers refugees for the Refugee category"),("Community routes","Community Support Program (CSP): sponsors support a new arrival"),("Decision maker","Department of Home Affairs")],
    f"<h2>How it works</h2>{ul(['UNHCR refers refugees who meet Australia’s priorities for the Refugee category.','The Special Humanitarian category usually needs a proposer in Australia.','The Community Support Program allows organisations to sponsor people and help them settle.','Applicants complete interviews, health and character checks.'])}",
    "https://www.homeaffairs.gov.au", "Australian Department of Home Affairs"))
PAGES.append(country("sweden", "Sweden", "b", "Sweden resettles refugees under an annual quota decided by the government, with selection by the Swedish Migration Agency.",
    [("Main programme","Quota refugee resettlement"),("Referrals","UNHCR submits cases; Sweden also runs selection missions"),("Quota","Set each year by the Government; it has changed over time"),("Decision maker","Swedish Migration Agency (Migrationsverket)")],
    f"<h2>How it works</h2>{ul(['The government sets the annual quota and priority groups.','UNHCR submits cases that match Sweden’s criteria.','Migration Agency staff review files and may interview refugees.','Those accepted receive residence permits and are placed in a municipality.'])}",
    "https://www.migrationsverket.se", "Swedish Migration Agency"))
PAGES.append(country("germany", "Germany", "e", "Germany admits refugees through federal humanitarian admission programmes and a private sponsorship scheme.",
    [("Main programme","Federal resettlement and humanitarian admission programmes"),("Community routes","NesT: a mentoring-based private sponsorship scheme"),("Referrals","UNHCR and partners identify candidates"),("Decision maker","Federal Office for Migration and Refugees (BAMF) and the Federal Ministry of the Interior")],
    f"<h2>How it works</h2>{ul(['Programmes are set by the federal government and may change.','Candidates are identified by UNHCR and checked by German authorities.','NesT mentors help newcomers with housing, language and daily life.','Admitted refugees receive a residence permit and integration support.'])}",
    "https://www.bamf.de/EN", "BAMF – Federal Office for Migration and Refugees"))
PAGES.append(country("united-kingdom", "United Kingdom", "a", "The UK resettles refugees through the UK Resettlement Scheme and supports community sponsorship.",
    [("Main programme","UK Resettlement Scheme (UKRS)"),("Community routes","Community Sponsorship: local groups welcome refugees"),("Referrals","UNHCR refers refugees to the Home Office"),("Decision maker","Home Office")],
    f"<h2>How it works</h2>{ul(['UNHCR refers refugees who meet the scheme’s criteria.','The Home Office reviews cases and carries out security and medical checks.','Local councils or community groups arrange housing and support on arrival.','Other schemes exist for specific nationalities; check GOV.UK for current rules.'])}",
    "https://www.gov.uk/government/collections/resettlement-scheme", "GOV.UK"))

# ---- Pathways
PAGES.append(pathway("family-reunification", "Family reunification", "d", "Refugee families separated by conflict may be able to join relatives who already have protection in another country.",
    f'''<h2>Who can it help?</h2><p>Family reunification lets close relatives, usually a spouse or partner and minor children, join a family member who has refugee status or similar protection.</p>
<h2>What to know</h2>{ul(['Rules differ by country, including who counts as family and time limits for applying.','Sponsors in the destination country often apply or provide evidence.','Documents such as marriage and birth certificates are usually needed.','Free legal advice from local refugee organisations can help.'])}'''))
PAGES.append(pathway("humanitarian-pathways", "Humanitarian pathways", "e", "Humanitarian corridors, admission programmes and private sponsorship offer organised, safe routes alongside resettlement.",
    f'''<h2>Types of humanitarian pathway</h2>{ul(['<strong>Humanitarian corridors:</strong> civil society groups and governments agree safe travel and visas for vulnerable people.','<strong>Humanitarian admission:</strong> governments admit groups under temporary programmes.','<strong>Private or community sponsorship:</strong> groups or individuals support refugees financially and socially.','<strong>Humanitarian visas:</strong> special visas for people at risk.'])}
<h2>How people are selected</h2><p>Selection is usually done by governments or partner organisations. Check each programme’s official page for current criteria.</p>'''))
PAGES.append(pathway("education", "Education", "b", "Scholarships and university programmes can offer refugees a legal route to study abroad.",
    f'''<h2>Study routes</h2>{ul(['Scholarship programmes run by universities, governments and charities.','University corridors that combine study places with visas and support.','Student sponsorship programmes that help refugees study and settle.'])}
<h2>Before you apply</h2>{ul(['Check language and academic requirements.','Keep certificates, transcripts and ID ready.','Apply only through official university or programme websites.'])}'''))
PAGES.append(pathway("employment", "Employment", "c", "Skilled refugees may find legal work-based routes to new countries.",
    f'''<h2>Work routes</h2>{ul(['Skilled migration visas adapted for refugees.','Employer-sponsored positions arranged through partner organisations.','Talent-matching platforms that connect refugees with employers.'])}
<h2>Tips</h2>{ul(['Prepare a CV and keep qualification records.','Use only verified programmes, and never pay a recruiter for a visa.','Ask whether you can keep refugee protection while you work abroad.'])}'''))

# ---- Rights & Contact
PAGES.append(dict(url=RIGHTS, group=None, crumb="Refugee Rights & Protection", title="Refugee rights and protection", tag="Know your rights",
    h1="Refugee rights and protection", hero="e",
    lead="Every refugee has rights under international law, whether or not they are resettled.",
    body=f'''<h2>Your core rights</h2>{ul(["<strong>Protection from return:</strong> you cannot be sent back to a place where your life or freedom is at risk (non-refoulement).","<strong>Access to asylum</strong> and fair procedures.","<strong>No penalty</strong> for entering irregularly to seek safety.","<strong>Safety and non-discrimination</strong> without distinction of race, religion or nationality.","<strong>Documentation</strong> such as identity and travel papers.","<strong>Basic services:</strong> education, health care and the right to work, in line with the host country’s laws.","<strong>Family unity</strong> wherever possible."])}
<h2>International law</h2><p>These rights come mainly from the 1951 Refugee Convention and its 1967 Protocol. UNHCR is mandated to protect refugees and help governments uphold the law.</p>
<h2>Your responsibilities</h2><p>Refugees are expected to respect the laws of the country where they live.</p>
<h2>If your rights are not respected</h2><p>Contact UNHCR or a local legal aid organisation. Call <a href="tel:{PHONE_TEL}">{PHONE}</a>.</p>{FREE}'''))

PAGES.append(dict(url=CONTACT, group=None, crumb="Contact", title="Contact", tag="Get in touch", h1="Contact", hero="a",
    lead="Reach our team by phone, on WhatsApp or through our support website.", layout=False,
    body=f'''<div class="contact-cards">
<div class="contact-card"><span class="label">Phone</span><a class="big" href="tel:{PHONE_TEL}">{PHONE}</a><p>Call to ask general questions about resettlement and legal pathways.</p><p style="margin-top:14px"><a class="btn btn-primary" href="tel:{PHONE_TEL}">Call now</a></p></div>
<div class="contact-card wa"><span class="label">WhatsApp</span><a class="big" href="{WA_URL}" target="_blank" rel="noopener">{PHONE}</a><p>Message us on WhatsApp to ask for guidance on resettlement and legal pathways.</p><p style="margin-top:14px"><a class="btn btn-wa" href="{WA_URL}" target="_blank" rel="noopener">{WA_ICON} Chat on WhatsApp</a></p><p class="wa-note">Never send passwords, bank details or payment. UNHCR services are always free.</p></div>
<div class="contact-card"><span class="label">Support website</span><a class="big" href="{SUPPORT_URL}" rel="noopener">{SUPPORT}</a><p>Visit our support site for help and updates.</p><p style="margin-top:14px"><a class="btn btn-outline" href="{SUPPORT_URL}" rel="noopener">Visit site</a></p></div></div>
<div style="margin-top:28px">{FREE}</div>
<h2 style="margin-top:34px">Before you contact us</h2>{ul(["Have your registration number ready, if you have one.","Keep your own contact details up to date.","Never share passwords or bank details."])}
<p style="margin-top:14px">Common questions are answered in our <a href="{R}/faq.html">FAQ</a>.</p>''',
    cta=("Looking for general answers?", "Read our frequently asked questions.", "Read the FAQ", f"{R}/faq.html")))

def main():
    for p in PAGES:
        path = os.path.join(ROOT, p["url"].lstrip("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(page(p))
    print(f"Generated {len(PAGES)} pages")

if __name__ == "__main__":
    main()
