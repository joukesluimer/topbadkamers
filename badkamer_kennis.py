# -*- coding: utf-8 -*-
"""Kennisbank badkamers: overzicht op /kennisbank/ en artikelen op /kennisbank/{slug}/.

De tekst van de artikelen staat in badkamer_kennis_artikelen.py. Deze module bouwt de pagina's.
Interface voor build.py:
    LINKS = [(pad, korte titel, omschrijving), ...]   # overzicht eerst
    build(write)                                      # schrijft alle pagina's
Eigen CSS staat in een <style> in de body, met het voorvoegsel .kk-.
"""

import datetime
import html as htmllib

from data import SITE, DIENSTEN
from components import page, crumbs, faq_blok, cta_blok, cta_midden, stappen_blok, title, icon
from badkamer_kennis_artikelen import ARTIKELEN as _ARTIKELEN1
from badkamer_kennis_artikelen2 import ARTIKELEN2
from badkamer_kennis_artikelen3 import ARTIKELEN3

ARTIKELEN = _ARTIKELEN1 + ARTIKELEN2 + ARTIKELEN3

GEPUBLICEERD = "2026-11-23"

# Thema's in de volgorde van het overzicht, met een icoon uit components.ICONS
THEMAS = [
    ("Plannen en regels", "form", "Wat je regelt voordat de sloop begint: volgorde, VvE, asbest en garantie."),
    ("Wonen en situatie", "house", "Je woonsituatie telt mee: huren, ouder worden in je huis of een badkamer op zolder."),
    ("Techniek en vocht", "druppel", "Waterdicht maken, ventileren, schimmel, lekkage, kalk en verwarming."),
    ("Ontwerp en materialen", "tegels", "Tegels, microcement, indeling en stijl: keuzes die je elke dag ziet."),
]

# Titels van de kostenpagina's (module badkamer_kosten.py van een andere agent; alleen de URL's)
KOSTEN_TITELS = {
    "nieuwe-badkamer": "Wat kost een nieuwe badkamer?",
    "inloopdouche": "Wat kost een inloopdouche?",
    "toilet-renoveren": "Wat kost een toilet renoveren?",
    "tegelzetter-per-m2": "Wat kost een tegelzetter per m²?",
    "badkamer-slopen": "Wat kost een badkamer slopen?",
    "vloerverwarming-badkamer": "Wat kost vloerverwarming in de badkamer?",
    "kitwerk-voegen": "Wat kost kitwerk en voegen vernieuwen?",
    "uurtarief-loodgieter": "Wat kost een loodgieter per uur?",
}

# Kostenpagina's uit ronde 2 (module van agent kosten-2). Alleen in de kaartjes van een artikel,
# niet in de lijst op het overzicht.
KOSTEN_TITELS_EXTRA = {
    "badkamer-op-zolder": "Wat kost een badkamer op zolder?",
}

TOOLS = {
    "/tools/badkamercalculator/": ("Badkamercalculator", "Maak een eerste schatting van de kosten en het aantal m² tegels."),
    "/tools/renovatieplanner/": ("Renovatieplanner", "Zet de stappen en wachttijden van je renovatie op een rij."),
    "/tools/badkamercheck/": ("Badkamercheck", "Controleer in een paar vragen in welke staat je badkamer is."),
    "/tools/offertechecker/": ("Offertechecker", "Kijk of je offerte compleet is en wat er nog ontbreekt."),
    "/tools/stijlkiezer/": ("Stijlkiezer", "Ontdek met een paar vragen welke badkamerstijl bij je past."),
}

_PER_SLUG = {a["slug"]: a for a in ARTIKELEN}
_DIENST = {d["slug"]: d for d in DIENSTEN}

LINKS = [("/kennisbank/", "Kennisbank", "Praktische uitleg over badkamerrenovatie, regels, techniek en ontwerp.")] + [
    (f"/kennisbank/{a['slug']}/", a["titel"].split(":")[0], a["kort"]) for a in ARTIKELEN
]

CSS = """<style>
.kk-toc{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:18px 22px;margin:26px 0}
.kk-toc p{margin:0 0 8px;font-weight:700}
.kk-toc ol{margin:0;padding-left:1.3em;columns:2;column-gap:28px}
.kk-toc li{margin-bottom:5px;break-inside:avoid}
@media(max-width:600px){.kk-toc ol{columns:1}}
.kk-verder{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:18px 0 8px}
.kk-verder a{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;text-decoration:none;color:inherit}
.kk-verder a:hover,.kk-verder a:focus-visible{border-color:var(--accent)}
.kk-soort{display:block;font-size:.78rem;text-transform:uppercase;letter-spacing:.04em;color:var(--accent-dark);font-weight:700}
.kk-naam{display:block;font-weight:700;margin:4px 0}
.kk-oms{display:block;font-size:.9rem}
.kk-bronnen{font-size:.9rem}
.kk-thema{display:flex;align-items:center;gap:10px;margin-top:42px}
.kk-thema svg{color:var(--accent)}
.kk-thema-oms{margin:6px 0 0}
.kk-meta{font-size:.88rem}
</style>"""


def _url(slug):
    return f"/kennisbank/{slug}/"


def _kort_titel(a):
    return a["titel"].split(":")[0]


def _verder_blok(a):
    """Kaartjes naar de passende dienst-, kosten- en toolpagina."""
    kaarten = []
    d = _DIENST.get(a["dienst"])
    if d:
        kaarten.append((f"/diensten/{d['slug']}/", "Dienst", d["naam"],
                        "Wat een specialist doet, de werkwijze en een richtprijs."))
    for ks in a["kosten"]:
        naam_k = KOSTEN_TITELS.get(ks) or KOSTEN_TITELS_EXTRA[ks]
        kaarten.append((f"/kosten/{ks}/", "Kosten", naam_k, "Richtprijzen met rekenvoorbeelden en bronnen."))
    naam, oms = TOOLS[a["tool"]]
    kaarten.append((a["tool"], "Tool", naam, oms))
    for href, naam_, oms_ in a.get("extra", []):
        kaarten.append((href, "Badkamerspullen", naam_, oms_))
    return '<div class="kk-verder">' + "".join(
        f'<a href="{h}"><span class="kk-soort">{s}</span><span class="kk-naam">{n}</span><span class="kk-oms">{o}</span></a>'
        for h, s, n, o in kaarten) + "</div>"


def _woorden(*delen):
    import re
    tekst = re.sub(r"<[^>]+>", " ", " ".join(delen))
    return len(tekst.split())


def _artikel(a, write, today):
    url = _url(a["slug"])
    cr, cr_ld = crumbs([("Home", "/"), ("Kennisbank", "/kennisbank/"), (_kort_titel(a), None)])

    toc_items = [(sid, kop) for sid, kop, _ in a["secties"]]
    toc_items += [("stappen", a["stappen_kop"]), ("verder", "Verder met je plan"),
                  ("bronnen", "Bronnen"), ("faq", "Veelgestelde vragen")]
    toc = "".join(f'<li><a href="#{sid}">{kop}</a></li>' for sid, kop in toc_items)

    secties = ""
    for i, (sid, kop, h) in enumerate(a["secties"]):
        secties += f'<h2 id="{sid}">{kop}</h2>{h}'
        if i == 2:
            secties += cta_midden("Plannen voor een nieuwe badkamer?",
                                  "Vergelijk gratis offertes van maximaal drie badkamerspecialisten uit je regio.")

    bronnen = "".join(f'<li><a href="{htmllib.escape(u)}" rel="noopener">{htmllib.escape(lab)}</a></li>'
                      for lab, u in a["bronnen"])
    lees_ook = "".join(f'<li><a href="{_url(s)}">{_kort_titel(_PER_SLUG[s])}</a></li>' for s in a["gerelateerd"])
    faq_html, faq_ld = faq_blok(a["faq"], "Veelgestelde vragen")
    datum = f"{today[8:10]}-{today[5:7]}-{today[:4]}"

    body = f"""{CSS}{cr}
<article class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Kennisbank · {a['groep']}</span>
  <h1>{a['titel']}</h1>
  <p class="lead">{a['intro']}</p>
  <p class="kk-meta">Bijgewerkt op {datum} · door de redactie van {SITE['naam']}</p>
  <div class="callout"><p><strong>Kort antwoord:</strong> {a['kort_antwoord']}</p></div>
  <nav class="kk-toc" aria-label="Inhoud van dit artikel"><p>Inhoud</p><ol>{toc}</ol></nav>
  {secties}
  <h2 id="stappen">{a['stappen_kop']}</h2>
  {stappen_blok(a['stappen'])}
  <h2 id="verder">Verder met je plan</h2>
  <p>Wil je weten wat het kost, of het laten doen? Deze pagina's sluiten aan op dit artikel.</p>
  {_verder_blok(a)}
  <h2 id="bronnen">Bronnen</h2>
  <ul class="kk-bronnen">{bronnen}</ul>
  <p class="kk-meta">Regels en normen veranderen. Controleer bij twijfel de actuele tekst bij de bron, of vraag het na bij je gemeente of een vakman. Dit artikel is algemene uitleg en geen juridisch advies.</p>
  <h2>Lees ook</h2>
  <ul>{lees_ook}</ul>
</div></article>
<div id="faq">{faq_html}</div>
{cta_blok("Liever een vakman?", "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit jouw regio en vergelijk ze naast elkaar.")}"""

    art_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": a["titel"], "description": a["description"],
        "inLanguage": "nl-NL", "datePublished": GEPUBLICEERD, "dateModified": today,
        "wordCount": _woorden(a["intro"], a["kort_antwoord"], *[h for _, _, h in a["secties"]],
                              *[t + " " + p for t, p in a["stappen"]], *[q + " " + x for q, x in a["faq"]]),
        "author": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "publisher": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "mainEntityOfPage": SITE["url"] + url,
        "isPartOf": {"@type": "CollectionPage", "@id": SITE["url"] + "/kennisbank/"},
        "articleSection": a["groep"],
        "citation": [u for _, u in a["bronnen"]],
    }
    write(url, page(title(a["seo_titel"]), a["description"], url, body, [cr_ld, art_ld, faq_ld]), prio=0.7)


def _kaart(a):
    href = _url(a["slug"])
    return (f'<a class="card" href="{href}"><h3 style="font-size:1.08rem">{a["titel"]}</h3>'
            f'<p>{a["kort"]}</p><span class="go">Lees meer →</span></a>')


def _overzicht(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Kennisbank", None)])
    blokken = ""
    for thema, ic, oms in THEMAS:
        kaarten = "".join(_kaart(a) for a in ARTIKELEN if a["groep"] == thema)
        blokken += (f'<h2 class="kk-thema">{icon(ic, 26)}{thema}</h2><p class="kk-thema-oms">{oms}</p>'
                    f'<div class="grid g3" style="margin-top:16px">{kaarten}</div>')
    kosten = "".join(f'<li><a href="/kosten/{s}/">{t}</a></li>' for s, t in KOSTEN_TITELS.items())
    tools = "".join(f'<li><a href="{h}">{n}</a>: {o}</li>' for h, (n, o) in TOOLS.items())
    body = f"""{CSS}{cr}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose">
    <span class="badge">Kennisbank</span>
    <h1>Kennisbank badkamers</h1>
    <p class="lead">Praktische uitleg over je badkamer: van de volgorde van een renovatie en de regels in een VvE of huurwoning tot waterdicht tegelen, schimmel, lekkage, kalk en het kiezen van tegels en een stijl. Elk artikel heeft een stappenplan, veelgestelde vragen en bronnen.</p>
    <p>Wij zijn een vergelijkingsplatform. We voeren zelf geen werk uit, maar brengen je in contact met maximaal drie badkamerspecialisten uit je regio. Deze artikelen helpen je om goede vragen te stellen en offertes te beoordelen.</p>
  </div>
  {blokken}
  <div class="narrow prose" style="margin-top:42px">
    <h2>Wat kost het?</h2>
    <p>Richtprijzen per klus, met rekenvoorbeelden en bronnen:</p>
    <ul>{kosten}</ul>
    <p>Alle prijzen op één pagina vind je bij <a href="/prijzen/">prijzen</a>.</p>
    <h2>Rekenen en plannen</h2>
    <ul>{tools}</ul>
  </div>
</div></section>
{cta_blok()}"""
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE["url"] + _url(a["slug"]), "name": a["titel"]}
             for i, a in enumerate(ARTIKELEN)]
    lijst_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE["url"] + "/kennisbank/",
                "name": "Kennisbank badkamers", "inLanguage": "nl-NL",
                "mainEntity": {"@type": "ItemList", "itemListElement": items}}
    write("/kennisbank/", page(title("Kennisbank badkamers: renovatie, regels en ontwerp"),
          "Praktische uitleg over je badkamer: renovatie, VvE, huur en asbest, waterdicht maken, schimmel, lekkage, kalk, verwarming, tegels, microcement en badkamerstijlen.",
          "/kennisbank/", body, [cr_ld, lijst_ld]), prio=0.8)


def build(write):
    today = datetime.date.today().isoformat()
    for a in ARTIKELEN:
        _artikel(a, write, today)
    _overzicht(write)
