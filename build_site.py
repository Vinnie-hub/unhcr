#!/usr/bin/env python3
"""Applies the shared header/footer to every page, fixes broken links and images,
and generates the pages that were missing.

    python3 build_site.py            # run from the project root; safe to re-run (idempotent)

Order: python3 build_resettlement.py  then  python3 build_site.py
"""
import glob
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
import site_shell as shell                      # noqa: E402
import resettlement_hub as hub                  # noqa: E402
import build_resettlement as rb                 # noqa: E402

e = shell.e
HELP = shell.REAL_HELP_URL

# ----------------------------------------------------------------------------- helpers
def read(path):
    with open(path, encoding="utf-8", newline="") as f:
        return f.read().replace("\r\n", "\n")

def write(path, text):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

# ----------------------------------------------------------------------------- country data
def parse_countries():
    """Regions and their countries, read from country-sites.html (the single source of truth)."""
    s = read("country-sites.html")
    regions = []
    for block in re.split(r'<div class="region">', s)[1:]:
        rm = re.search(r'href="/regions/([^"]+?)(?:\.html)?"[^>]*>\s*(.*?)\s*</a>', block, re.S)
        slug, name = rm.group(1), re.sub(r"\s+", " ", rm.group(2)).replace("&amp;", "&")
        cs = re.findall(r'<a href="/countries/([^"]+?)(?:\.html)?"><span class="flag">(.*?)</span>\s*(.*?)</a>', block, re.S)
        regions.append((slug, name, [(c[0], c[1], c[2].strip().replace("&amp;", "&")) for c in cs]))
    return regions

REGIONS = parse_countries()
# normalise the one slug that was spelled two ways
ALIAS = {"united-state": "united-states", "turkey": "turkiye"}
COUNTRY_REGION = {c[0]: (r[0], r[1]) for r in REGIONS for c in r[2]}
ASYLUM = {"canada", "united-states", "united-kingdom", "germany", "france", "italy", "greece", "poland"}
REGION_BLURB = {
    "eastern-and-southern-africa": "From the Horn of Africa to Southern Africa, the region hosts many refugees and asylum-seekers, most living in settlements and communities alongside their hosts.",
    "west-and-central-africa": "Conflict, insecurity and climate pressure in the Sahel, Lake Chad basin and Central Africa have displaced many people within and across borders.",
    "middle-east-and-north-africa": "The region has long hosted people displaced by conflict, and many countries here are also stages on onward journeys.",
    "asia-and-pacific": "The region is home to some of the world’s longest-running displacement situations as well as people displaced by conflict, disasters and statelessness.",
    "europe": "Countries across Europe receive people seeking asylum and run resettlement and complementary pathway programmes. UNHCR supports fair and efficient asylum systems.",
    "americas": "Displacement in Latin America and the Caribbean, along with asylum in North America, makes this one of the most dynamic regions for protection.",
}
REGION_IMG = {
    "eastern-and-southern-africa": "/images/gallery/unhcr-tent-with-a-family.webp",
    "west-and-central-africa": "/images/gallery/unhcr-with-a-family-of-4.webp",
    "middle-east-and-north-africa": "/images/gallery/unhcr-single-mom-with-3-children.webp",
    "asia-and-pacific": "/images/gallery/unhcr-responds-to-rising-displacement.webp",
    "europe": "/images/gallery/build-better-futures.webp",
    "americas": "/images/gallery/opportunity-for-displaced-people.webp",
}

# ----------------------------------------------------------------------------- legacy pages
# the country pages that existed before; every other country page is generated below
ORIGINAL_COUNTRIES = ["canada", "egypt", "kenya", "nigeria", "rwanda", "uganda", "united-states"]
LEGACY = ["index.html", "unhcr.html", "about.html", "what-we-do.html", "where-we-work.html", "get-help.html",
          "get-involved.html", "news-and-stories.html", "privacy.html", "country-sites.html",
          "what-we-do/data-and-publications.html", "news-and-stories/press-releases.html"] + \
         [f"countries/{c}.html" for c in ORIGINAL_COUNTRIES]

# anchor text -> real target for the old href="#" placeholders
PLACEHOLDER_TEXT = [
    (r"who we protect", "/about/who-we-protect.html"),
    (r"planning, funding", "/about/planning-funding-and-results.html"),
    (r"our partners", "/about/our-partners.html"),
    (r"governance and oversight", "/about/governance-and-oversight.html"),
    (r"high commissioner", "/about/high-commissioner.html"),
    (r"1951", "/about/refugee-convention.html"),
    (r"statelessness|stateless", "/about/statelessness.html"),
    (r"emergenc", "/what-we-do.html#respond-to-emergencies"),
    (r"human rights|protect", "/what-we-do.html#protect-human-rights"),
    (r"better futures|solutions", "/what-we-do.html#build-better-futures"),
    (r"data|statistic|publication|report|refworld|global trends|global appeal|global report", "/what-we-do/data-and-publications.html"),
    (r"press release|media", "/news-and-stories/press-releases.html"),
    (r"newsletter|subscribe|sign up|stay informed|updates", "/get-involved/sign-and-stay-informed.html"),
    (r"donat|give|appeal|support|fundrais|made51|bracelet", "/get-involved.html#ways-to-give"),
    (r"partner", "/get-involved/partner-with-us.html"),
    (r"volunteer|intern|work with us|career|job|classroom", "/get-involved.html#take-action"),
    (r"resettle|resettlement", "/resettlement/index.html"),
    (r"help|asylum|refugee status|register", "/get-help.html"),
    (r"contact|question|faq", "/contact.html"),
    (r"fraud|scam", "/beware-of-fraud.html"),
    (r"supplier", "/contact.html#suppliers"),
    (r"misconduct|abuse", "/contact.html#report-misconduct"),
    (r"privacy", "/privacy.html"),
    (r"terms|copyright", "/terms.html"),
    (r"cookie", "/privacy.html#cookie-notice"),
    (r"country|where we work|operation|region", "/where-we-work.html"),
    (r"news|story|stories|read more|latest|more", "/news-and-stories.html"),
    (r"about", "/about.html"),
]
EXACT = [
    (r"newsletter", "/get-involved/sign-and-stay-informed.html"),
    (r"data protection", "/privacy.html"),
    (r"database", "/what-we-do/data-and-publications.html"),
    (r"statute of the office", "/about.html#mandate"),
    (r"seeking help from unhcr", "/contact.html"),
    (r"resettlement information", "/resettlement/index.html"),
    (r"asylum and refugee status|rights and duties", "/resettlement/refugee-rights-and-protection.html"),
    (r"registration how to register", "/resettlement/how-the-process-works.html"),
    (r"reporting fraud", "/beware-of-fraud.html"),
    (r"statelessness help", "/about/statelessness.html"),
    (r"^home$", "/index.html"),
    (r"how can i get involved", "/get-involved.html"),
    (r"who do we serve", "/about/who-we-protect.html"),
    (r"events and committees|governance", "/about/governance-and-oversight.html"),
    (r"strategic directions|beyond borders", "/about/planning-funding-and-results.html"),
    (r"^(all countries|view all \d+ countries)", "/country-sites.html"),
    (r"family reunification", "/resettlement/pathways/family-reunification.html"),
    (r"education access|^.{0,3}education", "/resettlement/pathways/education.html"),
    (r"work and income|livelihoods", "/resettlement/pathways/employment.html"),
    (r"sponsorship", "/resettlement/pathways/humanitarian-pathways.html"),
    (r"travel documents", "/get-help.html"),
    (r"vacanc", "/get-involved.html#take-action"),
    (r"signing up to email|email lists", "/get-involved/sign-and-stay-informed.html"),
    (r"please use this form", "/contact.html"),
    (r"global public api|forced displacement survey|handbooks|registration and identity|clifdew|sociosat|uprooted in their own|covid-19", "/what-we-do/data-and-publications.html"),
]
COUNTRY_NAMES = {}   # filled in main(): lower-case name -> slug
LEFTOVERS = []
MAPPED = set()

def fix_placeholders(s, rel):
    def repl(m):
        before, after, inner = m.group(1), m.group(2), m.group(3)
        text = re.sub(r"<[^>]+>", " ", inner)
        text = re.sub(r"\s+", " ", text).strip().lower()
        target = None
        if text in ("français", "español", "عربي", "english"):
            target = "/" + rel
        if not target:
            for pat, t in EXACT:
                if re.search(pat, text):
                    target = t
                    break
        if not target:
            for nm, slug in COUNTRY_NAMES.items():
                if re.fullmatch(r"(?:visit the website for )?" + re.escape(nm) + r"(?: →)?", text):
                    target = f"/countries/{slug}.html"
                    break
        if not target and len(text) > 48:      # a news / story headline
            target = "/news-and-stories.html"
        if not target:
            for pat, t in PLACEHOLDER_TEXT:
                if re.search(pat, text):
                    target = t
                    break
        if target:
            MAPPED.add((text[:50], target))
            return f'<a{before} href="{target}"{after}>{inner}</a>'
        LEFTOVERS.append((rel, text[:60]))
        return f'<a{before} href="/news-and-stories.html"{after}>{inner}</a>'
    return re.sub(r'<a((?:\s[^>]*?)?)\shref="#"([^>]*)>(.*?)</a>', repl, s, flags=re.S)

IMG_FIX = {
    "/images/gallery/gallery-1.svg": "/images/gallery/the-un-refugee-agency.webp",
    "/images/gallery/unhcr-with-different-families.webp": "/images/gallery/unchr-with-different-families.webp",
}
NEWS_POOL = ["/images/gallery/emergencies-respond.webp", "/images/gallery/unhcr-responding-to-new-emergencies.webp",
             "/images/gallery/stories-hero.webp", "/images/gallery/the-un-refugee-agency.webp"]
DATA_POOL = ["/images/gallery/unhcr-works-in-122-countries.webp", "/images/gallery/the-high-level-event-commemorating-75-years-of-the-1951-refugee-convention.webp",
             "/images/gallery/statement-by-the-united-nations-high-commissioner.webp", "/images/gallery/unhcr-responds-to-rising-displacement.webp",
             "/images/gallery/protect-human-rights.webp", "/images/gallery/opportunity-for-displaced-people.webp"]

def fix_images(s):
    for a, b in IMG_FIX.items():
        s = s.replace(a, b)
    counter = {"n": 0}
    def pool(pool_list):
        def r(m):
            counter["n"] += 1
            return f'src="{pool_list[counter["n"] % len(pool_list)]}"'
        return r
    s = re.sub(r'src="(?:/news-and-stories/)?images/news/[^"]+"', pool(NEWS_POOL), s)
    s = re.sub(r'src="(?:/what-we-do/)?images/data/[^"]+"', pool(DATA_POOL), s)
    return s

def transform_legacy(rel):
    s = read(rel)
    path = "/" + rel
    home = "id=\"sitesOverlay\"" in s
    # old shell assets
    s = re.sub(r'\s*<link rel="stylesheet" href="/css/(?:header-mobile|whatsapp-float)\.css"\s*/?>', "", s)
    s = re.sub(r'\s*<!--[^>]*WHATSAPP[^>]*-->\s*<a class="wa-float".*?</a>', "", s, flags=re.S)
    # header
    s = re.sub(r'<a class="sh-skip"[^>]*>.*?</a>\s*', "", s, flags=re.S)
    s = re.sub(r'<div id="main" tabindex="-1"></div>\s*', "", s)
    hdr = shell.header(path, home=home)
    if re.search(r"<header\b", s):
        s = re.sub(r'(?:\s*<!--[^>]*HEADER[^>]*-->)?\s*<header\b.*?</header>', "\n" + hdr, s, count=1, flags=re.S)
    else:
        s = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + hdr + "\n", s, count=1)
    # footer
    ftr = shell.footer()
    if re.search(r"<footer\b", s):
        s = re.sub(r'<footer\b.*?</footer>', lambda m: ftr, s, count=1, flags=re.S)
    else:
        s = s.replace("</body>", ftr + "\n</body>", 1)
    # head / body hooks (idempotent)
    if "/css/site.css" not in s:
        s = s.replace("</head>", "  " + shell.HEAD_LINKS + "\n</head>", 1)
    if "/js/main.js" not in s:
        s = s.replace("</body>", shell.BODY_SCRIPT + "\n</body>", 1)
    # links + images
    s = fix_images(s)
    s = fix_placeholders(s, rel)
    # country / region links: use real files so they also work without Vercel "clean URLs"
    s = re.sub(r'href="/countries/([a-z-]+)"', lambda m: f'href="/countries/{ALIAS.get(m.group(1), m.group(1))}.html"', s)
    s = re.sub(r'href="/regions/([a-z-]+)"', r'href="/regions/\1.html"', s)
    s = re.sub(r'href="/countries/([a-z-]+)\.html"', lambda m: f'href="/countries/{ALIAS.get(m.group(1), m.group(1))}.html"', s)
    s = s.replace('href="/about-unhcr.html"', 'href="/about.html"').replace('href="/countries.html"', 'href="/country-sites.html"')
    s = s.replace('href="/data-and-publications.html"', 'href="/what-we-do/data-and-publications.html"').replace('href="/help.html"', 'href="/get-help.html"')
    s = s.replace('href="privacy.html"', 'href="/privacy.html"')
    # anchors the nav menus point to
    s = s.replace("<h2>Respond to emergencies", '<h2 id="respond-to-emergencies">Respond to emergencies', 1) if rel == "what-we-do.html" else s
    if rel == "what-we-do.html":
        s = s.replace("<h2>Protect human rights", '<h2 id="protect-human-rights">Protect human rights', 1)
        s = s.replace("<h2>Build better futures", '<h2 id="build-better-futures">Build better futures', 1)
    if rel == "about.html":
        s = s.replace("<h2>UNHCR mandate and governing charters", '<h2 id="mandate">UNHCR mandate and governing charters', 1)
    if rel == "get-involved.html" and 'id="take-action"' not in s:
        h = s.find("Explore opportunities in detail")
        k = s.rfind("<section", 0, h)
        if h != -1 and k != -1:
            s = s[:k] + '<section id="take-action"' + s[k + len("<section"):]
        s = s.replace('href="#work-with-us"', 'href="#take-action"')
    if rel == "get-help.html":
        s = re.sub(r'<div class="contact-details">.*?</div>', (
            '<div class="contact-details"><h3>Official help</h3>'
            '<p>For real help, visit the official UNHCR help site: <a href="%s" rel="noopener">help.unhcr.org</a>.</p>'
            '<p>This class project does not provide any contact service, and nothing entered in the form is sent.</p></div>') % HELP, s, count=1, flags=re.S)
        s = s.replace("We aim to respond within two business days.", "Class project demo: nothing you enter is sent or stored.")
    write(rel, s)

# ----------------------------------------------------------------------------- new pages
def crumbs(*items):
    return [("Home", "/index.html")] + list(items)

def emit(p):
    write(p["url"].lstrip("/"), rb.page(p))

ABOUT_SIDE = ("About UNHCR", [
    ("Overview", "/about.html"), ("Who we protect", "/about/who-we-protect.html"),
    ("Planning, funding and results", "/about/planning-funding-and-results.html"), ("Our partners", "/about/our-partners.html"),
    ("Governance and oversight", "/about/governance-and-oversight.html"), ("The High Commissioner", "/about/high-commissioner.html"),
    ("The 1951 Refugee Convention", "/about/refugee-convention.html"), ("Statelessness", "/about/statelessness.html")])

def about_page(slug, title, tag, lead, hero, body, cta=None):
    p = dict(url=f"/about/{slug}.html", group=None, crumbs=crumbs(("About UNHCR", "/about.html")), side=ABOUT_SIDE, crumb=title,
             title=title, tag=tag, h1=title, lead=lead, hero=hero, body=body)
    if cta: p["cta"] = cta
    emit(p)

def build_about():
    ul, call, facts = rb.ul, rb.call, rb.facts
    about_page("who-we-protect", "Who we protect", "About UNHCR",
        "UNHCR protects and assists people who have been forced to flee, and people who have no nationality.", "/images/gallery/about-unhcr-out-work.webp",
        f"""<p class="lead">Our mandate covers several groups, each with different needs and legal protections.</p>
{facts([("Refugees", "People who have fled their country because of persecution, conflict or violence and cannot return safely. They are protected by international law, mainly the 1951 Refugee Convention."),
("Asylum-seekers", "People who have left their country and are asking for protection but whose claim has not yet been decided."),
("Internally displaced people", "People forced to flee their homes but who remain inside their own country. UNHCR works with partners to protect and assist them."),
("Stateless people", "People who are not considered a national by any country. Without a nationality they can be denied rights such as education, health care and work."),
("Returnees", "Former refugees who have gone back to their country and need support to reintegrate safely.")])}
<h2>Protection comes first</h2>
<p>Everything UNHCR does starts from protection: making sure people can reach safety, are not sent back to danger, and can enjoy their rights. See <a href="/about/refugee-convention.html">the 1951 Refugee Convention</a> and <a href="/about/statelessness.html">statelessness</a> for the legal framework.</p>
{call("Are you a refugee, asylum-seeker or stateless person? Visit our <a href='/get-help.html'>Get help</a> page.")}""")
    about_page("planning-funding-and-results", "Planning, funding and results", "About UNHCR",
        "How UNHCR plans its work, how it is funded and how it measures results.", "/images/gallery/the-un-refugee-agency.webp",
        f"""<h2>Planning</h2><p>UNHCR plans in multi-year strategies and sets out yearly needs in its Global Appeal. Country operations build their plans together with refugees, host communities, governments and partners.</p>
<h2>Funding</h2><p>UNHCR is funded overwhelmingly by voluntary contributions from governments, the European Union, private donors, companies and individuals. A small subsidy from the United Nations regular budget covers part of administrative costs.</p>
{ul(["Contributions can be flexible, which lets UNHCR respond where needs are greatest, or earmarked for a specific operation.","Private-sector and individual giving is a growing part of income.","Funding needs usually exceed what is received, so priorities have to be set."])}
<h2>Results</h2><p>UNHCR reports on its results each year, including in the Global Report. Data and publications are collected on the <a href="/what-we-do/data-and-publications.html">data and publications</a> page.</p>""",
        cta=("Support UNHCR’s work", "See the ways you can help people forced to flee.", "Ways to give", "/get-involved.html#ways-to-give"))
    about_page("our-partners", "Our partners", "About UNHCR",
        "No organization can respond to displacement alone. UNHCR works with a wide range of partners.", "/images/gallery/the-high-level-event-commemorating-75-years-of-the-1951-refugee-convention.webp",
        f"""{facts([("Governments", "Host countries, resettlement countries and donors. Governments have the primary responsibility to protect refugees on their territory."),
("United Nations agencies", "Agencies such as WFP, UNICEF, WHO and IOM, with whom UNHCR shares responsibilities in emergencies and long-term responses."),
("Non-governmental organizations", "Local and international NGOs deliver much of the assistance on the ground."),
("Refugee-led organizations", "Groups led by people who have themselves been displaced, who understand needs first-hand."),
("Private sector and foundations", "Companies and foundations contribute funding, expertise, jobs and technology."),
("Development actors and academia", "Development banks, researchers and universities help build long-term solutions and evidence.")])}
<p style="margin-top:16px">Interested in working with us? Read about <a href="/get-involved/partner-with-us.html">partnering with UNHCR</a>.</p>""")
    about_page("governance-and-oversight", "Governance and oversight", "About UNHCR",
        "UNHCR is accountable to the United Nations General Assembly and to its member states.", "/images/gallery/statement-by-the-united-nations-high-commissioner.webp",
        f"""<h2>Governance</h2>{ul(["The <strong>General Assembly</strong> of the United Nations created UNHCR and sets its mandate. The High Commissioner reports to it through the Economic and Social Council.","The <strong>Executive Committee (ExCom)</strong> of the High Commissioner’s Programme approves programmes and budgets and advises on protection.","The <strong>High Commissioner</strong> is elected by the General Assembly and leads the organization."])}
<h2>Oversight and accountability</h2>{ul(["An <strong>Inspector General’s Office</strong> investigates allegations of misconduct.","An <strong>Independent Audit and Oversight Committee</strong> advises on risk, audit and internal control.","An <strong>Evaluation Service</strong> assesses the results of UNHCR operations.","External audit is carried out by the United Nations Board of Auditors."])}
<p>To raise a concern about misconduct or abuse, see our <a href="/contact.html#report-misconduct">contact page</a>.</p>""")
    about_page("high-commissioner", "The High Commissioner", "About UNHCR",
        "The High Commissioner for Refugees leads UNHCR and speaks for the world’s refugees.", "/images/gallery/the-high-commissioner.webp",
        f"""<p class="lead">The High Commissioner is elected by the United Nations General Assembly, on the nomination of the Secretary-General, for a fixed term.</p>
<h2>Role</h2>{ul(["Leads UNHCR’s operations in around 120 countries.","Advocates with governments for the rights and protection of refugees, displaced and stateless people.","Reports to the General Assembly and to the Executive Committee.","Works with partners to mobilize the funding and political support needed for solutions."])}
<img src="/images/gallery/statement-by-the-united-nations-high-commissioner.webp" alt="The High Commissioner speaking at a United Nations meeting" loading="lazy" style="border-radius:8px;margin-top:8px">
<p>Read recent statements in <a href="/news-and-stories.html">News and stories</a> and <a href="/news-and-stories/press-releases.html">press releases</a>.</p>""")
    about_page("refugee-convention", "The 1951 Refugee Convention", "About UNHCR",
        "Seventy-five years on, the Convention remains the foundation of refugee protection.", "/images/gallery/the-1951-refugee-convention.webp",
        f"""<p class="lead">Adopted in 1951 in the aftermath of the Second World War, the Convention relating to the Status of Refugees defines who is a refugee and sets out their rights.</p>
<h2>Key principles</h2>{ul(["<strong>Definition:</strong> a refugee is someone outside their country with a well-founded fear of persecution for reasons of race, religion, nationality, membership of a particular social group or political opinion.","<strong>Non-refoulement:</strong> refugees must not be returned to a place where their life or freedom would be at risk.","<strong>No penalty</strong> for entering or staying irregularly in order to seek safety.","<strong>Rights:</strong> including access to courts, education, work and documentation, with obligations to respect the laws of the host country."])}
<h2>The 1967 Protocol</h2><p>The 1967 Protocol removed the original time and geographic limits, so the Convention applies to refugees everywhere.</p>
<img src="/images/gallery/the-high-level-event-commemorating-75-years-of-the-1951-refugee-convention.webp" alt="A high-level event commemorating 75 years of the 1951 Refugee Convention" loading="lazy" style="border-radius:8px;margin-top:8px">
<p>See also <a href="/resettlement/refugee-rights-and-protection.html">refugee rights and protection</a>.</p>""")
    about_page("statelessness", "Statelessness", "About UNHCR",
        "Stateless people are not recognized as citizens by any country. UNHCR works to prevent and end statelessness.", "/images/gallery/un-conventions-on-statelessness-passport.webp",
        f"""<p class="lead">Without a nationality, a person may be unable to go to school, see a doctor, get a job, open a bank account or even get married.</p>
<h2>The conventions</h2>{ul(["The <strong>1954 Convention relating to the Status of Stateless Persons</strong> sets minimum standards of treatment.","The <strong>1961 Convention on the Reduction of Statelessness</strong> helps states prevent children from being born stateless."])}
<h2>What UNHCR does</h2>{ul(["Identifies and protects stateless people.","Helps states change laws that cause statelessness.","Encourages states to join the conventions and to grant nationality to children born on their territory who would otherwise be stateless."])}
{call("Everyone has the right to a nationality. Information for stateless people is on our <a href='/get-help.html'>Get help</a> page.")}""")

def build_regions_and_countries():
    all_countries = {c[0]: (c[1], c[2], r[0], r[1]) for r in REGIONS for c in r[2]}
    for slug, name, countries in REGIONS:
        cards = "".join(f'<a class="country-link" href="/countries/{c[0]}.html"><span class="flag" aria-hidden="true">{c[1]}</span>{e(c[2])}</a>' for c in countries)
        emit(dict(url=f"/regions/{slug}.html", group=None, crumbs=crumbs(("Where we work", "/where-we-work.html")), crumb=name,
                  side=("Regions", [(r[1], f"/regions/{r[0]}.html") for r in REGIONS]),
                  title=f"{name} regional site", tag="Where we work", h1=name, lead=REGION_BLURB[slug], hero=REGION_IMG[slug],
                  body=f"""<h2>Country sites in this region</h2><div class="country-grid">{cards}</div>
<div style="margin-top:28px">{rb.call("Each country page gives an overview of UNHCR’s role there. For the full list across the world, see <a href='/country-sites.html'>all country sites</a>.")}</div>""",
                  cta=("Need help?", "Information for refugees, asylum-seekers, stateless and displaced people.", "Get help", "/get-help.html")))
    existing = set(ORIGINAL_COUNTRIES)
    for cslug, (cname, flag, rslug, rname) in all_countries.items():
        if cslug in existing:
            continue
        dest = cslug in ASYLUM
        siblings = [(c[2], f"/countries/{c[0]}.html") for c in next(r for r in REGIONS if r[0] == rslug)[2]]
        if dest:
            lead = f"{cname} is a country where people seek safety. UNHCR works with the authorities and partners so that asylum systems are fair and efficient and refugees can rebuild their lives."
            work = rb.ul(["<strong>Asylum.</strong> Supporting fair, efficient procedures and access to territory for people seeking protection.",
                          "<strong>Rights.</strong> Advising on laws and policies, and monitoring that people are treated with dignity.",
                          "<strong>Integration.</strong> Working with cities, civil society and communities to help refugees learn, work and belong.",
                          "<strong>Pathways.</strong> Encouraging resettlement and other safe, legal routes."])
        else:
            lead = f"UNHCR works in {cname} together with the government, UN agencies, local and international partners and communities to protect and assist people forced to flee."
            work = rb.ul(["<strong>Protection.</strong> Registering people, documenting them and helping them access asylum and legal protection.",
                          "<strong>Assistance.</strong> Shelter, water, health care, education and cash or relief items for families in need.",
                          "<strong>Inclusion.</strong> Helping refugees, displaced people and host communities access services and livelihoods together.",
                          "<strong>Solutions.</strong> Supporting voluntary return when it is safe, local integration, and resettlement for those most at risk."])
        extra = ""
        if cslug in ("germany", "united-kingdom"):
            extra = f"<p>Read how <a href='/resettlement/countries/{cslug}.html'>resettlement to {cname}</a> works.</p>"
        emit(dict(url=f"/countries/{cslug}.html", group=None,
                  crumbs=crumbs(("Where we work", "/where-we-work.html"), (rname, f"/regions/{rslug}.html")), crumb=cname,
                  side=(rname, siblings), title=f"UNHCR in {cname}", tag=rname, h1=f"UNHCR in {cname}", lead=lead, hero=REGION_IMG[rslug],
                  body=f"""<span class="flag-xl" aria-hidden="true">{flag}</span>
<h2>What UNHCR does</h2>{work}{extra}
<h2>Find help</h2><p>Information and services for refugees, asylum-seekers, stateless and displaced people are on our <a href="/get-help.html">Get help</a> page. For official, up-to-date country information, visit <a href="{HELP}" rel="noopener">help.unhcr.org</a>.</p>
{rb.call("<strong>Class project note:</strong> this page gives general information only. Figures, local news and contact details are not included.")}
<p style="margin-top:14px"><a href="/regions/{rslug}.html">&larr; Back to {e(rname)}</a></p>""",
                  cta=("Looking for another country?", "Browse every UNHCR country site.", "All country sites", "/country-sites.html")))

def build_misc():
    call, ul = rb.call, rb.ul
    # news
    emit(dict(url="/news-and-stories/media-centre.html", group=None, crumbs=crumbs(("News and stories", "/news-and-stories.html")), crumb="Media centre",
              side=("News and stories", [("Latest news and stories", "/news-and-stories.html"), ("Press releases", "/news-and-stories/press-releases.html"), ("Media centre", "/news-and-stories/media-centre.html")]),
              title="Media centre", tag="News and stories", h1="Media centre", hero="/images/gallery/stories-hero.webp",
              lead="Resources for journalists and editors covering displacement and statelessness.",
              body=f"""<h2>What you will find here</h2>{ul(["<a href='/news-and-stories/press-releases.html'>Press releases</a> and statements.","<a href='/what-we-do/data-and-publications.html'>Data and publications</a> for facts and figures.","Background on <a href='/about/who-we-protect.html'>who UNHCR protects</a> and the <a href='/about/refugee-convention.html'>1951 Refugee Convention</a>."])}
<h2>Media enquiries</h2><p>Send your question using our <a href="/contact.html">contact form</a>. In this class project the form does not deliver messages.</p>
{call("Reporting on refugees? Please protect the identity and safety of the people you interview, especially children and survivors of violence.")}"""))
    # get involved
    emit(dict(url="/get-involved/sign-and-stay-informed.html", group=None, crumbs=crumbs(("Get involved", "/get-involved.html")), crumb="Sign up for updates",
              side=("Get involved", [("Ways to give", "/get-involved.html#ways-to-give"), ("Partner with us", "/get-involved/partner-with-us.html"), ("Sign up for updates", "/get-involved/sign-and-stay-informed.html")]),
              title="Sign up and stay informed", tag="Get involved", h1="Sign up and stay informed", hero="/images/gallery/stories-hero.webp",
              lead="Learn more about people forced to flee and how you can support them.",
              body=f"""<form class="form" data-demo>
  <p class="callout warn" style="margin:0">This is a class project demo. Nothing you enter is sent or stored. Please do not enter real details.</p>
  <label>Email address<input type="email" name="email" autocomplete="email" required></label>
  <fieldset style="border:0;padding:0;display:grid;gap:8px"><legend style="font-weight:600;color:var(--navy);margin-bottom:6px">I am interested in</legend>
    <label class="check"><input type="checkbox" checked> Latest news and stories</label>
    <label class="check"><input type="checkbox"> Emergency updates</label>
    <label class="check"><input type="checkbox"> Resettlement and pathways</label>
    <label class="check"><input type="checkbox"> Ways to help</label></fieldset>
  <button class="btn btn-primary" type="submit">Subscribe</button>
  <p class="demo-result" role="status" hidden></p>
</form>
<p style="margin-top:18px">We would only ever use real sign-ups as described in the <a href="/privacy.html">privacy notice</a>.</p>"""))
    emit(dict(url="/get-involved/partner-with-us.html", group=None, crumbs=crumbs(("Get involved", "/get-involved.html")), crumb="Partner with us",
              side=("Get involved", [("Ways to give", "/get-involved.html#ways-to-give"), ("Partner with us", "/get-involved/partner-with-us.html"), ("Sign up for updates", "/get-involved/sign-and-stay-informed.html")]),
              title="Partner with us", tag="Get involved", h1="Partner with us", hero="/images/gallery/build-better-futures.webp",
              lead="Governments, companies, foundations and communities all have a part to play.",
              body=f"""{rb.facts([("Companies", "Funding, employee engagement, jobs for refugees, products and technology."),("Foundations and philanthropists", "Multi-year support for protection, education and solutions."),("Governments", "Contributions, asylum and resettlement places, and policy partnership."),("Civil society and faith groups", "Community sponsorship, advocacy and local support."),("Universities and researchers", "Evidence, scholarships and education pathways.")])}
<h2>How to start</h2><p>Tell us a little about your organization through the <a href="/contact.html">contact form</a>. See also <a href="/about/our-partners.html">our partners</a>.</p>"""))
    # contact
    emit(dict(url="/contact.html", group=None, crumbs=crumbs(), crumb="Contact", side=("Contact UNHCR", [("General enquiries", "/contact.html"), ("Media centre", "/news-and-stories/media-centre.html"), ("Beware of fraud", "/beware-of-fraud.html"), ("Get help", "/get-help.html")]),
              title="Contact UNHCR", tag="Get in touch", h1="Contact UNHCR", hero="/images/gallery/opportunity-for-displaced-people.webp",
              lead="Questions about this website, media enquiries, feedback and reports.",
              body=f"""<h2>General enquiries</h2>{hub.contact_form()}
<h2 id="report-misconduct" style="margin-top:34px">Report misconduct or abuse</h2><p>UNHCR takes allegations of misconduct, including sexual exploitation and abuse, fraud and corruption, very seriously. This class project cannot receive reports. To report a real concern, use the official channels on <a href="{shell.REAL_SITE_URL}" rel="noopener">unhcr.org</a>.</p>
<h2 id="suppliers" style="margin-top:34px">Become a supplier</h2><p>Companies that wish to supply goods or services to UNHCR should register through the official procurement pages on <a href="{shell.REAL_SITE_URL}" rel="noopener">unhcr.org</a>.</p>
<h2 style="margin-top:34px">Report a fraudulent site or email</h2><p>Read <a href="/beware-of-fraud.html">how to recognize fraud</a>.</p>
<h2 style="margin-top:34px">Need help yourself?</h2><p>Go to <a href="/get-help.html">Get help</a>, or visit the official <a href="{HELP}" rel="noopener">help.unhcr.org</a>.</p>"""))
    emit(dict(url="/beware-of-fraud.html", group=None, crumbs=crumbs(), crumb="Beware of fraud", side=("Contact UNHCR", [("General enquiries", "/contact.html"), ("Beware of fraud", "/beware-of-fraud.html"), ("Get help", "/get-help.html")]),
              title="Beware of fraud", tag="Stay safe", h1="Beware of fraud", hero="/images/gallery/protect-human-rights.webp",
              lead="UNHCR never charges for its services. Anyone who asks you for money is not acting for UNHCR.",
              body=f"""{rb.FREE}
<h2>Warning signs</h2>{ul(["Someone asks for a fee, a “deposit” or a gift to register you, process your case, speed it up or guarantee resettlement.","You are asked to pay or share personal details through a messaging app or a personal bank or mobile-money account.","A website or email uses UNHCR’s name and logo but does not end in <strong>unhcr.org</strong>.","You are promised a place, a visa or a date.","You are pressured to act immediately or to keep it secret."])}
<h2>What to do</h2>{ul(["Do not pay and do not send passport copies, passwords or financial details.","Check the address: official UNHCR websites are on <strong>unhcr.org</strong> and its sub-domains.","Report fraud to the local police and through the official channels on <a href='{shell.REAL_SITE_URL}' rel='noopener'>unhcr.org</a>.","If you need real help, go to <a href='{HELP}' rel='noopener'>help.unhcr.org</a>."])}
{call("<strong>This website is a class project.</strong> It is not an official UNHCR website. Do not use it to contact UNHCR or to ask about your case.", True)}"""))
    # terms
    emit(dict(url="/terms.html", group=None, crumbs=crumbs(), crumb="Terms and conditions", title="Terms and conditions of use", tag="Legal", h1="Terms and conditions of use",
              hero="/images/gallery/the-unhcr-statute.webp", lead="How this class project may be used.", layout=False,
              body=f"""<div class="article" style="max-width:800px"><h2>Purpose of this website</h2><p>{e(shell.DEMO_LONG)}</p>
<h2>No official services</h2><p>Nothing on this website is an application, a request for assistance or legal advice. Forms do not send or store any information.</p>
<h2 id="copyright">Copyright and trademarks</h2><p>The UNHCR name, emblem and logo are the property of UNHCR and are shown here only to illustrate a design exercise. They must be removed or replaced before this project is published for any other purpose. Photographs and text on this site are used for demonstration and remain the property of their respective owners.</p>
<h2>Links to other websites</h2><p>Links to unhcr.org and other external sites are provided for information. We are not responsible for their content.</p>
<h2>Contact</h2><p>Use the <a href="/contact.html">contact page</a> for questions about this class project.</p></div>"""))
    # sitemap
    sec = []
    for label, href, groups, _ in shell.NAV:
        li = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for g, links in groups for t, u in links)
        sec.append(f'<div><h2><a href="{href}">{e(label)}</a></h2><ul class="list">{li}</ul></div>')
    other = "".join(f'<li><a href="{u}">{e(t)}</a></li>' for t, u in [("Home", "/index.html"), ("Get help", "/get-help.html"), ("Contact", "/contact.html"), ("Beware of fraud", "/beware-of-fraud.html"), ("All country sites", "/country-sites.html"), ("Privacy notice", "/privacy.html"), ("Terms and conditions", "/terms.html")])
    sec.append(f'<div><h2>More</h2><ul class="list">{other}</ul></div>')
    emit(dict(url="/sitemap.html", group=None, crumbs=crumbs(), crumb="Sitemap", title="Sitemap", tag="Find your way", h1="Sitemap", hero="/images/gallery/unhcr-works-in-122-countries.webp",
              lead="Every main section of this website in one place.", layout=False, body=f'<div class="grid cols-3">{"".join(sec)}</div>'))
    # 404
    emit(dict(url="/404.html", group=None, crumbs=crumbs(), crumb="Page not found", title="Page not found", tag="Error 404", h1="We can’t find that page",
              hero="/images/gallery/the-un-refugee-agency.webp", lead="The page may have moved. Try one of the links below.", layout=False,
              body='<div class="links-inline"><a class="btn btn-primary" href="/index.html">Go to the home page</a><a class="btn btn-outline" href="/sitemap.html">Open the sitemap</a><a class="btn btn-outline" href="/get-help.html">Get help</a></div>',
              cta=("Looking for a country?", "Browse every country site.", "All country sites", "/country-sites.html")))

# ----------------------------------------------------------------------------- cleanup & config
def cleanup():
    # rename the misspelt country page
    if os.path.exists("countries/united-state.html"):
        os.replace("countries/united-state.html", "countries/united-states.html")
    for f in ("css/header-mobile.css", "css/whatsapp-float.css"):
        if os.path.exists(f):
            os.remove(f)
    # vercel.json: drop the redirect to the unrelated domain and the unrelated /earn, /bonus rewrites
    write("vercel.json", '''{
  "$schema": "https://openapi.vercel.sh/vercel.json",
  "trailingSlash": false,
  "cleanUrls": true,
  "redirects": [
    { "source": "/countries/united-state", "destination": "/countries/united-states", "permanent": true }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    },
    {
      "source": "/(css|js)/(.*)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=0, must-revalidate" }]
    },
    {
      "source": "/(.*)\\\\.(png|jpg|jpeg|gif|svg|webp|ico)",
      "headers": [{ "key": "Cache-Control", "value": "public, max-age=2592000, immutable" }]
    }
  ]
}
''')

def main():
    cleanup()
    for r in REGIONS:
        for c in r[2]:
            COUNTRY_NAMES[c[2].lower()] = c[0]
    COUNTRY_NAMES["syrian arab republic"] = "syria"
    for rel in LEGACY:
        transform_legacy(rel)
    build_about()
    build_regions_and_countries()
    build_misc()
    if os.environ.get("SHOW_MAP"):
        for t, g in sorted(MAPPED):
            print("MAP", t, "->", g)
    if LEFTOVERS:
        print("placeholders sent to the news page by default:")
        for r, t in LEFTOVERS:
            print("  ", r, "|", t)
    print("done")

if __name__ == "__main__":
    main()
