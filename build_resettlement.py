#!/usr/bin/env python3
"""Generates the resettlement section pages. Run: python3 build_resettlement.py
Edit the content in PAGES below, then re-run to regenerate the HTML files."""
import os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, ROOT)
import site_shell as shell
import resettlement_hub as hub

REAL_HELP_URL = shell.REAL_HELP_URL  # official UNHCR help site, used instead of any private contact channel

# Local images (no remote hot-linking). Keys are used by the page definitions below.
IMG = {
    "a": "/images/gallery/unhcr-with-a-family-of-5.webp",
    "b": "/images/gallery/build-better-futures.webp",
    "c": "/images/gallery/about-unhcr-out-work.webp",
    "d": "/images/gallery/unhcr-with-a-family-of-4.webp",
    "e": "/images/gallery/unhcr-tent-with-a-family.webp",
}
def img(k, w=None): return IMG.get(k, k)

R = "/resettlement"
GROUPS = {
    "understanding": ("Understanding Resettlement", [
        ("What is resettlement?", f"{R}/what-is-resettlement.html"),
        ("Who may be considered?", f"{R}/who-may-be-considered.html"),
        ("How the process works", f"{R}/how-the-process-works.html"),
        ("Support after arrival", f"{R}/support-after-arrival.html"),
        ("Frequently asked questions", f"{R}/faq.html")]),
    "countries": ("Countries", [
        ("Canada", f"{R}/countries/canada.html"),
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

def header(url):
    return shell.header(url)

def footer():
    return shell.footer()

def page(p):
    url, group = p["url"], p.get("group")
    if "crumbs" in p:
        crumbs = list(p["crumbs"])
    else:
        crumbs = [("Home", "/index.html"), ("Resettlement", f"{R}/index.html")]
        if group: crumbs.append((GROUPS[group][0], None))
    bc = "".join(f'<li><a href="{u}">{e(t)}</a></li>' if u else f"<li>{e(t)}</li>" for t, u in crumbs)
    bc += f'<li aria-current="page">{e(p["crumb"])}</li>'
    actions = "".join(f'<a class="btn {c}" href="{u}">{e(t)}</a>' for t, u, c in p.get("actions", []))
    hero_bg = img(p["hero"])
    text = (f'<span class="hero-tag">{e(p["tag"])}</span><h1>{e(p["h1"])}</h1><p>{e(p["lead"])}</p>'
            + (f'<div class="actions">{actions}</div>' if actions else ""))
    if p.get("hero_img"):
        inner = (f'<div class="hero-split"><div>{text}</div><div class="hero-photo"><img src="{p["hero_img"]}" alt="{e(p.get("hero_alt", ""))}" width="405" height="675"></div></div>')
    else:
        inner = text
    hero = f"""<section class="hero{"" if p.get("big") else " sm"}" style="background-image:url('{hero_bg}')">
  <div class="container">{inner}</div></section>"""
    side = ""
    side_group = p.get("side") or (GROUPS[group] if group else None)
    if side_group:
        label, items = side_group
        side += f'<div class="panel"><h3>{e(label)}</h3><ul>' + "".join(
            f'<li><a href="{u}"' + (' aria-current="page"' if u == url else "") + f'>{e(t)}</a></li>' for t, u in items) + "</ul></div>"
    side += f"""<div class="panel"><h3>Looking for help?</h3><p style="font-size:.95rem">Read the <a href="{R}/faq.html">FAQ</a> or visit the <a href="/contact.html">contact page</a>. For real-world help, go to <a href="{REAL_HELP_URL}" rel="noopener">help.unhcr.org</a>.</p><p style="font-size:.85rem;color:var(--muted);margin-top:8px">UNHCR never asks for money to process resettlement.</p></div>"""
    if p.get("raw"):
        main_body = p["body"]
    else:
        inner_body = (f'<div class="layout"><div class="article">{p["body"]}</div><aside class="aside" aria-label="Related">{side}</aside></div>'
                      if p.get("layout", True) else p["body"])
        main_body = f'<section class="section"><div class="container">{inner_body}</div></section>'
    cta = p.get("cta", ("Questions about your situation?", "Read our frequently asked questions or visit the contact page.", "Contact us", "/contact.html"))
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p["title"])} | UNHCR (class project)</title>
<meta name="description" content="{e(p["lead"])}">
<meta name="theme-color" content="#18375f">
<link rel="icon" href="/images/logos/unhcr favicon.webp">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
{shell.HEAD_LINKS}
</head>
<body>
{header(url)}
<nav class="breadcrumb" aria-label="Breadcrumb"><div class="container"><ol>{bc}</ol></div></nav>
<main>
{hero}
{main_body}
{p.get("extra", "")}
<section class="section cta"><div class="container"><h2>{e(cta[0])}</h2><p>{e(cta[1])}</p><a class="btn btn-yellow" href="{cta[3]}">{e(cta[2])}</a></div></section>
</main>
{footer()}
{shell.BODY_SCRIPT}
</body>
</html>
"""

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

PAGES.append(dict(url=f"{R}/index.html", group=None, big=True, raw=True, crumb="Resettlement", title="Resettlement creates new beginnings", tag="UNHCR Resettlement",
    h1="Resettlement creates new beginnings", hero="b",
    hero_img="/images/resettlement/mother-and-child.webp", hero_alt="A mother and her smiling child embrace",
    lead="From crisis to safety. From displacement to opportunity.",
    actions=[("How the process works", f"{R}/how-the-process-works.html", "btn-yellow"), ("Resettlement countries", f"{R}/countries/canada.html", "btn-light")],
    body=hub.hub_body(FREE),
    cta=("Have a question?", "Read our frequently asked questions or visit the contact page.", "Read the FAQ", f"{R}/faq.html")))

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
    body=f'''{hub.steps6()}
<p class="tagline" style="margin-top:22px">Resettlement changes lives.</p>
<h2>The six stages in more detail</h2>
{steps([("1. Registration","You register with UNHCR or a partner organization and your details are recorded. If you are not already recognised as a refugee, your claim is assessed (refugee status determination)."),
("2. Assessment &amp; referral","UNHCR staff assess whether resettlement is the right solution and whether you meet the submission criteria. If suitable, your case is referred to a resettlement country."),
("3. Interviews &amp; screening","The country may interview you. Documents are verified and eligibility, medical and security checks are carried out."),
("4. Approval","The resettlement country makes the final decision on whether to accept you."),
("5. Pre-departure arrangements","Travel documents, health checks and cultural orientation are arranged, typically with IOM."),
("6. Arrival &amp; support","You are received and supported with housing, healthcare, education, employment and community integration.")])}
<h2>How long does it take?</h2>
<p>Timelines vary widely by country, case and security situation. Do not rely on anyone who promises a date.</p>
{FREE}
{call("<strong>Keep your details current.</strong> Tell UNHCR if your phone number, address or family situation changes so that you can be reached.")}''',
    cta=("Have a question about the process?", "Find answers to common questions on our FAQ page.", "Read the FAQ", f"{R}/faq.html")))

faqs = [
("Can I apply for resettlement directly?","No. UNHCR identifies and refers refugees. Individuals cannot apply to UNHCR for resettlement or choose a destination country."),
("Does it cost money?","No. Every step is free. Anyone asking for payment, including for “priority” or “guaranteed” places, is committing fraud. Report it."),
("How do I know if I am being considered?","UNHCR will contact you directly using your registered details. Keep them up to date."),
("Can I choose which country I go to?","No. The resettlement country decides, and UNHCR matches cases to countries’ criteria."),
("Can my family come with me?","Immediate family members usually travel together if they are part of the same case. Contact UNHCR about relatives in other places."),
("What if I am not selected?","Not being selected does not affect your refugee status or protection. Other pathways, such as family reunification, education or employment routes, may be possible."),
("How long does it take?","It varies from months to many years, depending on the country, security checks and available places."),
("What is the difference between resettlement and a complementary pathway?","Resettlement is led by UNHCR referral. Pathways such as study or work visas are separate routes you may apply to yourself or through partners."),
("Who can I trust for information?","Official UNHCR channels and government immigration websites only. See our <a href='/beware-of-fraud.html'>Beware of fraud</a> page for how to verify."),
("Where can I get help right now?",f"Visit our <a href='/contact.html'>contact page</a>. For real-world help, go to the official UNHCR help site at <a href='{REAL_HELP_URL}' rel='noopener'>help.unhcr.org</a>.")]
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
<h2>If your rights are not respected</h2><p>Contact UNHCR or a local legal aid organisation. For real-world help, go to <a href="{REAL_HELP_URL}" rel="noopener">help.unhcr.org</a>.</p>{FREE}'''))

PAGES.append(dict(url=CONTACT, group=None, crumb="Contact", title="Resettlement contact", tag="Get in touch", h1="Contact", hero="a",
    lead="Send a general question about this website. In this class project nothing is actually sent.", layout=False,
    body=f'''<div class="layout"><div class="article"><h2>Send a message</h2>{hub.contact_form()}</div>
<aside class="aside"><div class="panel"><h3>Official help</h3><p style="font-size:.95rem">People who need protection or information should use the official UNHCR help site: <a href="{REAL_HELP_URL}" rel="noopener">help.unhcr.org</a>.</p></div>
<div class="panel"><h3>Stay safe from fraud</h3><p style="font-size:.95rem">UNHCR services are always free. Read <a href="/beware-of-fraud.html">how to spot fraud</a>.</p></div></aside></div>
<div style="margin-top:28px">{FREE}</div>
<h2 style="margin-top:34px">Before you contact anyone</h2>{ul(["Have your registration number ready, if you have one.","Keep your own contact details up to date.","Never share passwords or bank details."])}
<p style="margin-top:14px">Common questions are answered in our <a href="{R}/faq.html">FAQ</a>.</p>''',
    cta=("Looking for general answers?", "Read our frequently asked questions.", "Read the FAQ", f"{R}/faq.html")))

PAGES.append(country("canada", "Canada", "a", "Canada resettles refugees through government-assisted and privately sponsored streams, and refugees arrive as permanent residents.",
    [("Main programme","Refugee and humanitarian resettlement"),("Referrals","UNHCR and other referral partners refer refugees for government-assisted resettlement"),("Community routes","Private sponsorship: groups and organisations in Canada sponsor refugees"),("Decision maker","Immigration, Refugees and Citizenship Canada (IRCC)")],
    f"<h2>How it works</h2>{ul(['UNHCR refers refugees who meet Canada’s priorities for government-assisted resettlement.','Privately sponsored refugees are supported by a group, organisation or community in Canada, usually for the first year.','Applicants complete interviews, medical and security screening.','Resettled refugees arrive as permanent residents and can access settlement services such as language classes and help finding housing and work.'])}",
    "https://www.canada.ca/en/immigration-refugees-citizenship.html", "Immigration, Refugees and Citizenship Canada"))

def _sup(title, ic, text):
    return f'<h2>{title}</h2><div class="support-item" style="flex-direction:row;text-align:left;margin-bottom:6px"><span class="ico">{hub.icon(ic)}</span><span style="font-weight:400;color:var(--text)">{text}</span></div>'
PAGES.append(dict(url=f"{R}/support-after-arrival.html", group="understanding", crumb="Support after arrival", title="Support after arrival", tag="Understanding Resettlement",
    h1="Support after arrival", hero="d",
    lead="Beyond resettlement, ongoing support helps families settle, learn, work and belong.",
    body=f'''<p class="lead">Refugees are not just survivors, they are future contributors.</p>
<p>Arriving in a new country is the start of a longer journey. What is offered depends on the country, the programme and the city or town, so always check the official source for the country concerned.</p>
{_sup("Housing","home","Reception and help finding safe, affordable housing. Many programmes arrange temporary accommodation on arrival.")}
{_sup("Healthcare","heart","Health screening, registration with health services and access to mental health and specialised care where it is available.")}
{_sup("Education","book","School places for children, and language classes, training and recognition of qualifications for adults.")}
{_sup("Employment support","briefcase","Help with CVs, job search, skills training and connecting with employers.")}
{_sup("Community integration","community","Orientation, mentors, sponsors and local groups that help newcomers build friendships and take part in community life.")}
{CHECK}''',
    cta=("See where refugees are resettled", "Explore how resettlement works in each country.", "Resettlement countries", f"{R}/countries/canada.html")))

def main():
    for p in PAGES:
        path = os.path.join(ROOT, p["url"].lstrip("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(page(p))
    print(f"Generated {len(PAGES)} pages")

if __name__ == "__main__":
    main()
