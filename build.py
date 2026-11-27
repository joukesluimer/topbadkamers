# -*- coding: utf-8 -*-
"""
Top Badkamers: statische site generator.

Gebruik:   python3 build.py
Resultaat: alles in ./site/, met links vanaf de root (/assets/..., /diensten/...).
           Voor GitHub Pages in een submap zet prefix.py daarna het voorvoegsel ervoor.

Fase 1 (november 2026): home, diensten, werkgebied, plaatsen, plaats×dienst,
offertes aanvragen, voor badkamerspecialisten, prijzen en de vaste pagina's.
De schildertools van Topschilder (kosten, gidsen, kennisbank, kleurenkiezer,
inspiratie, onderhoudscheck, schilderweer, offertechecker, actiepagina's) staan
nog in de map, maar worden niet gebouwd. Zie PLAN.md, fase 2 en 3.
"""

import os
import shutil
import datetime

from data import (SITE, DIENSTEN, PLAATSEN, buurplaatsen,
                  PRIJSINDEX, INDEX_TOELICHTING, lokale_prijs)
from wijk_data import WIJKEN  # noqa: F401  (wijkteksten zijn nog schilderspecifiek; fase 2)
from badkamer_plaats import plaats_sectie, dienst_blok, lokale_faq, lokale_dienst_faq
import dienst_verdieping as DV
from plaats_content import bouwperiode_zin
from components import (
    page, crumbs, offerte_form, hoe_werkt_het, waarom_blok, dienst_cards,
    faq_blok, cta_blok, prijstabel, icon, eur, title, desc, werkgebied_kaart,
    feiten_blok, stappen_blok, dienst_icoon, cta_midden, offertecheck_blok,
)
import lastmod
from components import render_beeld
from render_data import RENDERS
from render_stijl_data import RENDERS_STIJL

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
TODAY = datetime.date.today().isoformat()

URLS = []  # (pad, prioriteit, changefreq)

BTW_BRON = ("https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/"
            "tarieven_en_vrijstellingen/diensten_9_btw/werkzaamheden_aan_woningen/werkzaamheden_aan_woningen")

# Plaatsen onder deze grens krijgen geen indexeerbare plaats×dienst-pagina's:
# daar is te weinig lokaal te vertellen, en de plaatspagina dekt de zoekvraag al.
DORP_GRENS = 5000


def write(path, html, prio=0.6, freq="monthly", index=True):
    full = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    if index:
        URLS.append((path, prio, freq))
        lastmod.onthoud(path, html)


def dienst(slug):
    """Dienst op slug, of None als data.py hem (nog) niet heeft."""
    return next((d for d in DIENSTEN if d["slug"] == slug), None)


def dlink(slug, tekst=None):
    d = dienst(slug)
    if not d:
        return tekst or slug
    return f'<a href="/diensten/{d["slug"]}/">{tekst or d["naam"]}</a>'


def incl(d):
    return "" if "excl" in d["prijs_eenheid"] else ", inclusief materiaal en btw"


# ===========================================================================
# HOME
# ===========================================================================

import beleving
import beleving2
from badkamer_voorna import voorna_slider, VOORNA_CSS, VOORNA_JS
from render_voorna_data import PAAR_BY_SLUG


def build_home():
    kern = [p for p in PLAATSEN if p["prio"] == 1]
    chips = "".join(f'<li><a href="/badkamerspecialist/{p["slug"]}/">Badkamer {p["naam"]}</a></li>' for p in kern)

    # Voorbeelduitslag van de offertevergelijker (verzonnen offerte, echte banden uit de data)
    try:
        from producten_badkamer import PRODUCTDATA as _PD
        n_art = len(_PD["artikelen"])
        _gt = next((a for a in _PD["artikelen"] if "34558000" in a.get("codes", [])), None)
    except Exception:
        n_art, _gt = 0, None
    from richtprijzen import RICHTPRIJZEN as _RP
    _tg = _RP["tegelwerk"]
    rij_product = ""
    if _gt:
        _prijs_incl = 165 * 1.21
        _pct = round((_prijs_incl - _gt["tot"]) / _gt["tot"] * 100)
        rij_product = f"""<div class="ov-rij"><span class="ov-soort">Product</span>
      <div class="ov-rij-top"><strong>{_gt['merk']} {_gt['serie']} {_gt['codes'][0]}</strong><span class="ov-tag ov-tag-boven">{_pct}% boven de band</span></div>
      <p>Op de offerte € 165 excl. btw. Marktband van dit artikel: {eur(_gt['van'])} – {eur(_gt['tot'])} incl. btw. Een opslag op materiaal is normaal; vraag wat erin zit.</p></div>"""
    voorbeeld = f"""<div class="ov-voorbeeld" aria-label="Voorbeeld van een uitslag">
    <div class="ov-voorbeeld-kop"><span>Uitslag per regel</span><span class="ov-label">Voorbeeld</span></div>
    {rij_product}
    <div class="ov-rij"><span class="ov-soort">Arbeid</span>
      <div class="ov-rij-top"><strong>Tegelwerk wand en vloer, 28 m²</strong><span class="ov-tag ov-tag-binnen">binnen de richtprijs</span></div>
      <p>€ 40 per m² excl. btw. Richtprijs voor het zetten: {eur(_tg['laag'])} – {eur(_tg['hoog'])} per m² incl. btw.</p></div>
    <div class="ov-rij"><span class="ov-soort">Materiaal</span>
      <div class="ov-rij-top"><strong>Sanitair compleet</strong><span class="ov-tag ov-tag-vaag">te vaag</span></div>
      <p>Onvoldoende gespecificeerd: vraag merk en type per onderdeel.</p></div>
    <p class="ov-noot">Verzonnen offerte, echte prijsbanden (november 2026).</p>
  </div>"""

    hero = beleving2.hero()

    check_sec = f"""<section class="section">
<div class="wrap">
  <div class="grid g2" style="gap:48px;align-items:center">
    <div>
      <span class="badge">Offertevergelijker</span>
      <h2>Zo check je een badkamerofferte per regel</h2>
      <p class="lead">Een offerte van één bedrag zegt weinig. De offertevergelijker splitst je offerte op en legt elke regel naast een prijsband met bron.</p>
      <ol class="ov-stappen">
        <li><strong>Upload of plak je offerte.</strong> Een pdf met tekst of de tekst uit je mail. Hij wordt in je browser gelezen.</li>
        <li><strong>Zie per regel waar je staat.</strong> Producten zoals kranen, toiletten en douchegoten naast de marktprijs van dat artikel of die serie. Werk en materiaal naast richtprijzen per m², meter of uur.</li>
        <li><strong>Stel de juiste vragen.</strong> Je krijgt een lijst met wat ontbreekt en wat te vaag is, en een mailtje voor je aanbieder.</li>
        <li><strong>Wil je een tegenofferte?</strong> Kies zelf of je de specificatie, zonder je naam en die van je aanbieder, meeneemt in een aanvraag bij maximaal drie specialisten.</li>
      </ol>
      <p><a class="btn btn-primary btn-lg" href="/tools/offertechecker/">Check je offerte</a> <a class="btn btn-ghost" href="/hoe-verdienen-wij-geld/">Hoe verdienen wij geld?</a></p>
      <p style="font-size:.9rem;color:#5b6d71">Wij verkopen geen sanitair en verwijzen niet naar winkels. De check is gratis; een specialist betaalt ons alleen als je via ons een offerte aanvraagt.</p>
    </div>
    <div>{beleving.hero_visual()}</div>
  </div>
</div>
</section>"""

    stijlen = [("moderne-badkamer", "Modern"), ("landelijke-badkamer", "Landelijk"), ("japandi-badkamer", "Japandi")]
    stijl_kaarten = "".join(
        f'<a href="/inspiratie/{sl}/" style="display:block;text-decoration:none">'
        f'{render_beeld(RENDERS_STIJL[sl], "(max-width: 900px) 100vw, 360px")}'
        f'<span style="display:block;margin-top:8px;font-weight:600">{naam} →</span></a>'
        for sl, naam in stijlen if sl in RENDERS_STIJL)
    beeld_sec = f"""<section class="section">
<div class="wrap">
  <div class="grid g2" style="gap:44px;align-items:center">
    <div>{render_beeld(RENDERS["home"], "(max-width: 900px) 100vw, 600px")}</div>
    <div>
      <span class="badge">Inspiratie</span>
      <h2>Hoe ziet jouw nieuwe badkamer eruit?</h2>
      <p class="lead">Een inloopdouche met een glazen wand, een zwevend meubel en een hangtoilet: zo ziet een moderne badkamer er vaak uit. Maar er is meer. Bekijk zes stijlen in beeld, of stel er zelf een samen.</p>
      <p><a class="btn btn-ghost" href="/inspiratie/">Bekijk de badkamerstijlen</a> <a class="btn btn-ghost" href="/tools/stijlkiezer/">Probeer de stijlkiezer</a></p>
    </div>
  </div>
  <div class="grid g3" style="margin-top:36px">{stijl_kaarten}</div>
</div>
</section>"""

    diensten_sec = f"""<section class="section soft">
<div class="wrap">
  <div class="center" style="max-width:620px;margin:0 auto 40px">
    <span class="badge">Diensten</span>
    <h2>Waar heb je een badkamerspecialist voor nodig?</h2>
    <p class="lead">Per klus zie je wat het ongeveer kost, waar de prijs door bepaald wordt en waar je op let in een offerte.</p>
  </div>
  {dienst_cards()}
</div>
</section>"""

    reno = dienst("badkamer-renoveren")
    reno_zin = (f"Een complete nieuwe badkamer kost meestal tussen {eur(reno['prijs_van'])} en {eur(reno['prijs_tot'])}{incl(reno)}. "
                if reno else "")
    prijs_sec = f"""<section class="section">
<div class="wrap narrow">
  <span class="badge">Richtprijzen {TODAY[:4]}</span>
  <h2>Wat kost een nieuwe badkamer?</h2>
  <p class="lead">{reno_zin}Waar je in die bandbreedte uitkomt, hangt vooral af van de grootte, hoeveel er gesloopt en verlegd moet worden, en welk sanitair en welke tegels je kiest.</p>
  {prijstabel()}
  <p style="margin-top:22px"><a class="btn btn-ghost" href="/prijzen/">Volledig prijzenoverzicht bekijken</a></p>
</div>
</section>"""

    tips_sec = """<section class="section soft">
<div class="wrap">
  <div class="grid g2" style="align-items:center;gap:44px">
    <div>
      <span class="badge">Offertes vergelijken</span>
      <h2>Zo leg je badkameroffertes eerlijk naast elkaar</h2>
      <p>Twee offertes voor dezelfde badkamer kunnen duizenden euro's uit elkaar liggen. Dat zit zelden in de marge, en bijna altijd in wat er wel en niet in de prijs zit. Let vooral op deze punten.</p>
      <ul class="checklist">
        <li>Sloopwerk en afvoer van puin apart benoemd</li>
        <li>Sanitair als vast bedrag of als stelpost</li>
        <li>Leidingwerk, afvoer en elektra meegenomen</li>
      </ul>
      <p><a class="btn btn-primary" href="/tools/offertechecker/">Laat de offertevergelijker meekijken</a></p>
    </div>
    <div>
      <div class="card" style="box-shadow:var(--shadow-lg);border:0">
        <h3 style="margin-bottom:16px">Waar het vaak misgaat</h3>
        <div class="faq">
          <details><summary>Stelpost voor sanitair te laag</summary><div class="a"><p>Een stelpost van een paar honderd euro voor kranen en sanitair klinkt mooi, maar wie daarna in de showroom kiest, betaalt het verschil bij. Vraag welk merk en type er in de stelpost zit.</p></div></details>
          <details><summary>Waterdicht maken niet genoemd</summary><div class="a"><p>Onder de tegels van een douche hoort een waterdichte laag (tanking of een folie). Staat dat niet in de offerte, vraag dan hoe de vloer en wanden waterdicht worden.</p></div></details>
          <details><summary>Tegels per m² zonder snijverlies</summary><div class="a"><p>Reken op zo'n tien procent extra tegels voor snijverlies en breuk. Grote tegels en visgraat vragen meer.</p></div></details>
          <details><summary>Btw-tarief</summary><div class="a"><p>Voor een nieuwe badkamer betaal je in principe 21% btw. Het lage tarief van 9% geldt alleen voor een paar soorten werk aan een woning ouder dan twee jaar, zoals schilderen, stukadoren en isoleren.</p></div></details>
        </div>
      </div>
    </div>
  </div>
</div>
</section>"""

    regio_sec = f"""<section class="section">
<div class="wrap">
  <h2>Badkamerspecialisten per plaats</h2>
  <p class="lead" style="max-width:60ch">We beginnen in Flevoland, het Gooi, de Veluwe en rond Zwolle en Amersfoort. Staat jouw plaats er niet bij? Vraag alsnog offertes aan. Badkamerbedrijven werken vaak in een ruime regio.</p>
  <ul class="chips" style="margin:26px 0">{chips}</ul>
  <p><a href="/werkgebied/">Bekijk alle {len(PLAATSEN)} plaatsen →</a></p>
</div>
</section>"""

    vakmensen_sec = """<section class="section dark">
<div class="wrap center" style="max-width:680px">
  <span class="badge badge-dark">Voor badkamerspecialisten</span>
  <h2>Zoek je zelf klussen in plaats van een monteur?</h2>
  <p class="lead" style="color:#b8cadd">We koppelen aanvragen aan badkamerbedrijven, installateurs en tegelzetters in de regio. Je betaalt per aanvraag, niet per maand, en je bepaalt zelf je werkgebied.</p>
  <p style="margin-top:24px"><a class="btn btn-primary btn-lg" href="/voor-badkamerspecialisten/">Bekijk hoe het werkt</a></p>
</div>
</section>"""

    faqs = [
        ("Kan ik een badkamerofferte die ik al heb laten checken?",
         "Ja. Upload de pdf of plak de tekst in de offertevergelijker. Je ziet per regel of het om een product, werk of materiaal gaat en hoe de prijs zich verhoudt tot marktprijzen en richtprijzen met bron. De offerte wordt in je browser gelezen: er gaat niets naar ons of naar anderen, tot je zelf kiest voor een tegenofferte."),
        ("Wat is een tegenofferte via Top Badkamers?",
         "Na de check kun je de specificatie van je offerte gebruiken voor een aanvraag bij maximaal drie badkamerspecialisten. Je naam, adres en de naam van je huidige aanbieder gaan niet mee, en je ziet en bewerkt de tekst voordat je iets verstuurt. De specialisten maken een eigen offerte op dezelfde specificatie. Voor jou is dat gratis; de specialist betaalt ons een vergoeding per aanvraag."),
        ("Wat kost het om via Top Badkamers offertes aan te vragen?",
         "Niets. Aanvragen is gratis en vrijblijvend. Wij worden betaald door de bedrijven die je aanvraag ontvangen."),
        ("Hoeveel bedrijven nemen er contact met mij op?",
         "Maximaal drie. Dat is genoeg om echt te vergelijken, en weinig genoeg om niet dagenlang gebeld te worden. Je gegevens gaan nooit naar meer partijen."),
        ("Ben ik verplicht een offerte te accepteren?",
         "Nee. Je vergelijkt de offertes, kiest wat je wilt en kunt ze alle drie afwijzen zonder opgaaf van reden."),
        ("Kan ik ook alleen een toilet, kraan of inloopdouche laten plaatsen?",
         "Ja. Kies bij de eerste vraag het soort klus. Kleine klussen gaan naar bedrijven die die klussen ook echt doen."),
        ("Hoe worden de bedrijven geselecteerd?",
         "We controleren KvK-inschrijving en aansprakelijkheidsverzekering, en we kijken of het bedrijf het gevraagde werk doet. Bij herhaalde klachten stoppen we de samenwerking."),
        ("Wat gebeurt er met mijn gegevens?",
         "Je gegevens gaan alleen naar maximaal 3 bedrijven uit jouw regio. Andere partijen krijgen ze niet en we gebruiken ze niet voor ongevraagde reclame. Zie onze privacyverklaring."),
    ]
    faq_html, faq_ld = faq_blok(faqs)

    org_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": SITE["url"] + "/#organization",
        "name": SITE["naam"],
        "url": SITE["url"],
        "email": SITE["email"],
        "areaServed": [{"@type": "AdministrativeArea", "name": x}
                       for x in ["Flevoland", "Gelderland", "Overijssel", "Utrecht", "Noord-Holland"]],
        "description": "Top Badkamers laat je een badkamerofferte gratis per regel checken en koppelt je aan maximaal drie badkamerspecialisten in je regio voor vergelijkbare offertes.",
    }
    web_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": SITE["url"] + "/#website",
        "name": SITE["naam"],
        "url": SITE["url"],
        "inLanguage": "nl-NL",
        "publisher": {"@id": SITE["url"] + "/#organization"},
    }

    voorna_sec = f"""{VOORNA_CSS}<section class="section soft"><div class="wrap narrow">
  <span class="badge">Voor en na</span>
  <h2>Van jaren 80 naar nu: sleep en zie het verschil</h2>
  <p>Dezelfde kleine badkamer, vanuit dezelfde hoek: eerst met bad en douchegordijn, daarna met een inloopdouche. Sleep de schuif om te vergelijken.</p>
  {voorna_slider(PAAR_BY_SLUG["kleine-badkamer"], "(max-width: 860px) 100vw, 820px")}
  <p style="margin-top:14px"><a class="link" href="/inspiratie/voor-en-na/">Bekijk alle vier de voor-en-na-voorbeelden →</a></p>
</div></section>{VOORNA_JS}"""

    body = (hero + beleving2.zo_werkt_het() + check_sec + beleving2.inspiratie() + voorna_sec + beleving.sectie_droombadkamer()
            + beleving.sectie_ontdek() + waarom_blok() + diensten_sec + prijs_sec + beleving.sectie_cijfers()
            + tips_sec + regio_sec + faq_html + vakmensen_sec + cta_blok())

    write("/", page(
        "Badkamerofferte vergelijken en checken | Top Badkamers",
        "Check je badkamerofferte gratis per regel tegen marktprijzen, of vraag vrijblijvend offertes aan bij maximaal 3 badkamerspecialisten. Je offerte blijft in je browser.",
        "/", body, [org_ld, web_ld, faq_ld]), prio=1.0, freq="weekly")


# ===========================================================================
# DIENSTEN
# ===========================================================================

def build_diensten_index():
    cr, cr_ld = crumbs([("Home", "/"), ("Diensten", None)])
    rijen = [
        ("De hele badkamer moet anders: nieuwe indeling, nieuwe tegels, nieuw sanitair", "badkamer-renoveren"),
        ("Je wilt alleen een toilet, wastafel, kraan of douche laten vervangen", "badkamer-installeren"),
        ("De tegels zijn gedateerd of gebarsten, of je wilt nieuwe wand- en vloertegels", "tegelwerk-badkamer"),
        ("Je wilt een douche zonder drempel of instap, in plaats van een bad of douchebak", "inloopdouche-plaatsen"),
        ("Het toilet of de toiletruimte is aan vervanging toe", "toilet-renoveren"),
        ("Kitranden zijn zwart, voegen brokkelen of er lekt iets", "badkamer-onderhoud"),
        ("Het gaat om een VvE, verhuurwoningen of een bedrijfspand", "zakelijk-badkamers"),
    ]
    tabel = "".join(f"<tr><td>{w}</td><td>{dlink(s)}</td></tr>" for w, s in rijen if dienst(s))
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow">
  <h1>Badkamer laten doen: alle diensten en wat ze kosten</h1>
  <p class="lead">Van een nieuwe kraan tot een complete badkamer met inloopdouche. Kies hieronder je klus en zie meteen de richtprijzen, waar de prijs door bepaald wordt en waar je in een offerte op let.</p>
</div></section>
<section class="section-sm"><div class="wrap">{dienst_cards()}</div></section>
<section class="section soft"><div class="wrap narrow prose">
  <h2>Welke dienst past bij jouw klus?</h2>
  <p>Niet elke klus heeft een duidelijke naam. Herken je je situatie hieronder, dan weet je waar je moet zijn.</p>
  <div class="tablewrap"><table>
    <thead><tr><th>Wat je ziet of wilt</th><th>Kijk bij</th></tr></thead>
    <tbody>{tabel}</tbody>
  </table></div>
  <h2>Renoveren of alleen vervangen?</h2>
  <p>Werkt de afvoer goed, zitten de tegels nog vast en is er geen lekkage, dan kun je vaak volstaan met nieuw sanitair en nieuwe kitranden. Zit er vocht achter de tegels, wil je een andere indeling of is de badkamer ouder dan twintig jaar, dan is een complete renovatie meestal verstandiger. Beschrijf in je aanvraag wat je ziet; de badkamerspecialist kan het dan ter plekke beoordelen.</p>
  <h2>Klussen combineren</h2>
  <p>Moeten de badkamer en het toilet allebei worden aangepakt, noem dat dan meteen. Eén planning scheelt opstartkosten, en jij ziet in één offerte wat alles samen kost. Vraag wel om een aparte regel per onderdeel, zodat je kunt vergelijken en eventueel iets kunt schrappen.</p>
</div></section>
{hoe_werkt_het()}
{cta_blok()}"""
    write("/diensten/", page(
        title("Badkamer laten doen: diensten en richtprijzen"),
        "Alle badkamerklussen die je via Top Badkamers kunt aanvragen: complete badkamer, sanitair, tegelwerk, inloopdouche, toilet en onderhoud. Met richtprijzen.",
        "/diensten/", body, [cr_ld]), prio=0.8)


# Verwijzingen per dienst naar kosten, kennisbank, kopersgidsen en tools (fase 2 en 3).
MEER_WETEN = {
    "badkamer-renoveren": [("/kosten/nieuwe-badkamer/", "Wat kost een nieuwe badkamer?"),
                           ("/kennisbank/volgorde-badkamerrenovatie/", "De volgorde van een badkamerrenovatie"),
                           ("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer"),
                           ("/badkamerspullen/bad-of-douche/", "Bad of douche?"),
                           ("/tools/badkamercalculator/", "Badkamercalculator")],
    "badkamer-installeren": [("/kosten/uurtarief-loodgieter/", "Uurtarief van een loodgieter"),
                             ("/badkamerspullen/kranen-kiezen/", "Kranen kiezen"),
                             ("/badkamerspullen/wastafelmeubel-kiezen/", "Een wastafelmeubel kiezen"),
                             ("/kennisbank/kleine-badkamer-indelen/", "Een kleine badkamer indelen"),
                             ("/kennisbank/badkamer-op-zolder/", "Een badkamer op zolder"),
                             ("/kennisbank/vloerverwarming-of-radiator/", "Vloerverwarming of radiator?")],
    "tegelwerk-badkamer": [("/kosten/tegelzetter-per-m2/", "Wat kost een tegelzetter per m²?"),
                           ("/kennisbank/badkamer-waterdicht-maken/", "Een badkamer waterdicht maken"),
                           ("/kennisbank/tegels-kiezen/", "Tegels kiezen"),
                           ("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen"),
                           ("/tools/stijlkiezer/", "Stijlkiezer")],
    "inloopdouche-plaatsen": [("/kosten/inloopdouche/", "Wat kost een inloopdouche?"),
                              ("/kennisbank/inloopdouche-zonder-drempel/", "Een inloopdouche zonder drempel"),
                              ("/badkamerspullen/inloopdouche-kopen/", "Een inloopdouche kopen"),
                              ("/badkamerspullen/douchesysteem-kiezen/", "Een douchesysteem kiezen"),
                              ("/kennisbank/levensloopbestendige-badkamer/", "Een levensloopbestendige badkamer")],
    "toilet-renoveren": [("/kosten/toilet-renoveren/", "Wat kost een toilet renoveren?"),
                         ("/badkamerspullen/toilet-kiezen/", "Een toilet kiezen"),
                         ("/kennisbank/badkamer-ventilatie/", "Ventilatie in badkamer en toilet")],
    "badkamer-onderhoud": [("/kosten/kitwerk-voegen/", "Wat kost kitwerk en voegen?"),
                           ("/tools/badkamercheck/", "Badkamercheck: is je badkamer aan vervanging toe?"),
                           ("/kennisbank/badkamer-ventilatie/", "Ventilatie tegen schimmel"),
                           ("/kennisbank/schimmel-in-badkamer/", "Schimmel in de badkamer"),
                           ("/kennisbank/lekkage-badkamer/", "Lekkage in de badkamer"),
                           ("/kennisbank/kalk-en-waterhardheid/", "Kalk en waterhardheid")],
    "zakelijk-badkamers": [("/kennisbank/verbouwen-in-vve/", "Verbouwen in een VvE"),
                           ("/kennisbank/garantie-badkamerrenovatie/", "Garantie bij een badkamerrenovatie"),
                           ("/tools/offertechecker/", "Offertechecker")],
}


def meer_weten(slug):
    items = MEER_WETEN.get(slug)
    if not items:
        return ""
    li = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in items)
    return f"<h2>Meer weten?</h2><ul>{li}</ul>"


def dienst_body(d, plaats=None):
    """Inhoud voor zowel /diensten/{dienst}/ als /badkamerspecialist/{plaats}/{dienst}/."""
    pn = plaats["naam"] if plaats else None
    inplaats = f" in {pn}" if pn else ""
    p_van, p_tot = lokale_prijs(d, plaats) if plaats else (d["prijs_van"], d["prijs_tot"])
    prijsnoot = ""
    if plaats:
        i = PRIJSINDEX.get(plaats["provincie"], 1)
        rel = "iets onder" if i < 0.99 else "rond" if i < 1.03 else "boven"
        prijsnoot = f" Dat is de richtprijs voor {plaats['provincie']}, {rel} het landelijk gemiddelde."

    if plaats:
        cr, cr_ld = crumbs([("Home", "/"), ("Werkgebied", "/werkgebied/"),
                            (pn, f"/badkamerspecialist/{plaats['slug']}/"), (d["naam"], None)])
        h1 = f"{d['naam']} {pn}"
        intro_extra = f"<p>{plaats['hook']}</p>"
    else:
        cr, cr_ld = crumbs([("Home", "/"), ("Diensten", "/diensten/"), (d["naam"], None)])
        h1 = f"{d.get('naam_lang', d['naam'])}: kosten, werkwijze en offertes"
        intro_extra = DV.intentie_blok(d)

    feiten = feiten_blok([
        (f"{eur(p_van)}–{eur(p_tot)}", f"richtprijs {d['prijs_eenheid']}{inplaats}"),
        ("21%", "btw op een nieuwe badkamer en sanitair (9% alleen voor bijvoorbeeld schilder- en stucwerk)", BTW_BRON),
        ("3", "offertes maximaal, gratis en vrijblijvend"),
    ])

    hero = f"""<section class="section-sm">
<div class="wrap">
  <div class="grid g2" style="gap:48px;align-items:start">
    <div>
      <span class="badge badge-ic">{dienst_icoon(d['slug'], 18)}{d['naam_kort']}</span>
      <h1>{h1}</h1>
      <p class="lead">{d['intro']}</p>
      {intro_extra}
      <div class="callout callout-prijs">
        <p><strong>Richtprijs{inplaats}:</strong> {eur(p_van)} – {eur(p_tot)} {d['prijs_eenheid']}{incl(d)}.{prijsnoot}</p>
        <p style="font-size:.93rem;margin-top:8px">{d['prijs_extra']}</p>
      </div>
    </div>
    <div>{offerte_form(f"Offertes voor {d['naam_kort'].lower()}{inplaats}", "Vier korte vragen · gratis en vrijblijvend")}</div>
  </div>
</div>
</section>"""

    if plaats:
        wat_kort = "; ".join(x.split(" (")[0].split(":")[0].rstrip(".").lower() for x in d["wat"][:3])
        content = f"""<section class="section soft"><div class="wrap narrow prose reveal">
  <h2>Wat valt er onder {d['naam'].lower()}?</h2>
  <p>Onder andere {wat_kort}. De volledige lijst, hoe een badkamerspecialist te werk gaat, wat de prijs bepaalt en waar je op let in de offerte, lees je op onze pagina over <a href="/diensten/{d['slug']}/">{d['naam'].lower()}</a>. Hieronder staat wat specifiek voor {pn} geldt.</p>
  {feiten}
  {offertecheck_blok(d['naam'].lower())}
</div></section>"""
        return cr, cr_ld, hero + content

    wat = "".join(f"<li>{x}</li>" for x in d["wat"])
    fact = "".join(f"<li>{x}</li>" for x in d["prijsfactoren"])
    tips = "".join(f"<li>{x}</li>" for x in d["tips"])
    beeld = render_beeld(RENDERS[d["slug"]], "(max-width: 900px) 100vw, 760px") if d["slug"] in RENDERS else ""
    content = f"""<section class="section soft"><div class="wrap narrow prose reveal">
  {f'<div style="margin-bottom:28px">{beeld}</div>' if beeld else ''}
  <h2>Wat valt er onder {d['naam'].lower()}?</h2>
  <ul class="checklist">{wat}</ul>
  {feiten}

  <h2>Zo gaat een badkamerspecialist te werk</h2>
  {DV.stappen_met_duur(d)}

  <h2>Waar hangt de prijs vanaf?</h2>
  <p>Twee offertes voor ogenschijnlijk dezelfde klus kunnen ver uit elkaar liggen. Dat komt zelden door de winstmarge en bijna altijd door deze factoren:</p>
  <ul>{fact}</ul>

  <h2>Tips die je geld schelen</h2>
  <ul class="checklist">{tips}</ul>

  <h2>Let hierop in de offerte</h2>
  <p>Een goede offerte voor {d['naam'].lower()} is meer dan een bedrag onderaan een A4'tje. Controleer of het volgende erin staat:</p>
  <ul>
    <li>Wat er gesloopt wordt, en of afvoer van puin en eventueel asbest in de prijs zit</li>
    <li>Welk sanitair en welke tegels: merk en type, of een stelpost met een duidelijk bedrag</li>
    <li>Leidingwerk, afvoer, elektra en ventilatie: wat wordt er verlegd of vernieuwd?</li>
    <li>Hoe de douchevloer en wanden waterdicht worden gemaakt</li>
    <li>Het btw-tarief per post. Voor een badkamer is dat in principe 21%; alleen bijvoorbeeld schilder- en stucwerk aan een woning ouder dan twee jaar kan onder 9% vallen (<a href="{BTW_BRON}" rel="nofollow noopener">Belastingdienst</a>)</li>
    <li>Een concrete start- en opleverdatum, en hoe lang je zonder badkamer of toilet zit</li>
    <li>De garantietermijn en wat daar wel en niet onder valt</li>
  </ul>
  {offertecheck_blok(d['naam'].lower())}
  {meer_weten(d['slug'])}
</div></section>"""
    return cr, cr_ld, hero + content


def build_dienst_pages():
    for d in DIENSTEN:
        cr, cr_ld, body_top = dienst_body(d)
        faq_html, faq_ld = faq_blok(d["faq"] + DV.extra_faq(d), f"Veelgestelde vragen over {d['naam'].lower()}")

        andere = f"""<section class="section"><div class="wrap">
  <h2>Andere badkamerklussen</h2>
  {dienst_cards(exclude=d['slug'])}
</div></section>"""

        plaats_chips = "".join(
            f'<li><a href="/badkamerspecialist/{p["slug"]}/{d["slug"]}/">{d["naam_kort"]} {p["naam"]}</a></li>'
            for p in PLAATSEN if p["prio"] <= 2 and p["inwoners"] >= DORP_GRENS
        )
        regio = f"""<section class="section soft"><div class="wrap">
  <h2>{d['naam']} per plaats</h2>
  <p class="lead" style="max-width:60ch">Bekijk wat {d['naam'].lower()} kost in jouw gemeente en vraag direct offertes aan bij bedrijven uit de buurt.</p>
  <ul class="chips" style="margin-top:22px">{plaats_chips}</ul>
  <p style="margin-top:20px"><a href="/werkgebied/">Alle plaatsen bekijken →</a></p>
</div></section>"""

        svc_ld = {
            "@context": "https://schema.org",
            "@type": "Service",
            "serviceType": d["naam"],
            "name": f"{d['naam']}: offertes vergelijken",
            "provider": {"@id": SITE["url"] + "/#organization"},
            "areaServed": {"@type": "Country", "name": "Nederland"},
            "description": d["kort"],
            "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR",
                       "lowPrice": d["prijs_van"], "highPrice": d["prijs_tot"]},
        }

        body = body_top + DV.verdieping(d) + faq_html + regio + andere + cta_blok(
            f"Offertes voor {d['naam'].lower()} vergelijken?",
            "Vertel in een minuut wat je nodig hebt. Wij zoeken maximaal drie bedrijven die dit werk doen en beschikbaar zijn.")

        write(f"/diensten/{d['slug']}/", page(
            title(d.get("seo_titel") or f"{d['naam']}: kosten en offertes"),
            desc(f"Wat kost {d.get('naam_lang', d['naam']).lower()}?",
                 f"Richtprijs {eur(d['prijs_van'])}–{eur(d['prijs_tot'])} {d['prijs_eenheid']}, werkwijze en prijsfactoren.",
                 "Plus waar je op let in een offerte.",
                 "Vergelijk gratis 3 bedrijven bij jou in de buurt."),
            f"/diensten/{d['slug']}/", body, [cr_ld, faq_ld, svc_ld]), prio=0.9)


# ===========================================================================
# PLAATSEN
# ===========================================================================

REGIO_TEKST = {
    "Flevoland": "De steden en dorpen hier zijn gebouwd nadat de polders waren drooggelegd. Daardoor zijn hele wijken even oud, en zijn ook de badkamers in een buurt vaak rond dezelfde tijd aan vervanging toe.",
    "Gelderland": "Langs de randmeren en de Veluwe staan historische kernen zoals Elburg en Harderwijk naast naoorlogse wijken en nieuwbouw. Een badkamer in een oud pand vraagt een andere aanpak dan een in een rijtjeshuis uit de jaren tachtig.",
    "Noord-Holland": "In het Gooi en rond Weesp vind je veel oudere woningen, vaak met kleine of onhandig ingedeelde badkamers, en vestingsteden als Naarden en Weesp.",
    "Overijssel": "Kampen en Zwolle hebben historische binnensteden naast grote nieuwbouwwijken. Woon je in een monument, vraag dan bij je gemeente na of je voor ingrijpende verbouwingen een vergunning nodig hebt.",
    "Utrecht": "In Amersfoort en Bunschoten-Spakenburg staan oude stadskernen en dorpsgezichten naast grote uitbreidingswijken, waar badkamers vaak per straat in dezelfde periode zijn geplaatst.",
}


def build_werkgebied():
    per_prov = {}
    for p in sorted(PLAATSEN, key=lambda x: x["naam"]):
        per_prov.setdefault(p["provincie"], []).append(p)

    secs = ""
    for prov in sorted(per_prov):
        lis = "".join(f'<li><a href="/badkamerspecialist/{p["slug"]}/">Badkamer {p["naam"]}</a></li>' for p in per_prov[prov])
        secs += f"<h2>{prov}</h2><p style='max-width:68ch'>{REGIO_TEKST.get(prov, '')}</p><ul class='places' style='margin-bottom:34px'>{lis}</ul>"

    cr, cr_ld = crumbs([("Home", "/"), ("Werkgebied", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow">
  <h1>Ons werkgebied</h1>
  <p class="lead">Top Badkamers begint in Flevoland, de randmeren, de Veluwe, de IJsseldelta, Amersfoort en het Gooi. Kies je plaats voor lokale richtprijzen en informatie over de woningen in jouw buurt.</p>
  <p>Staat jouw plaats er niet tussen? Vraag toch offertes aan. Badkamerbedrijven werken vaak in een straal van dertig kilometer of meer, zeker bij een complete renovatie.</p>
</div></section>
<section class="section-sm" id="kaart"><div class="wrap">{werkgebied_kaart()}</div></section>
<section class="section-sm"><div class="wrap">
  <h2 style="margin-bottom:6px">Alle plaatsen per provincie</h2>
  <p style="margin-bottom:30px">Elke plaats heeft een eigen pagina met lokale richtprijzen en de klussen die je daar kunt aanvragen.</p>
  {secs}
</div></section>
<section class="section soft"><div class="wrap narrow prose">
  <h2>Hoe we bepalen wie er bij jou langskomt</h2>
  <p>Je vult je plaats en de klus in. Wij zoeken daarna maximaal drie bedrijven die in jouw regio werken en dit type werk doen. Staat jouw plaats niet op de kaart, dan kun je alsnog een aanvraag doen. We laten je weten of er een bedrijf beschikbaar is.</p>
</div></section>
{cta_blok()}"""
    write("/werkgebied/", page(
        title(f"Werkgebied: badkamerspecialisten in {len(PLAATSEN)} plaatsen"),
        desc("Bekijk in welke plaatsen Top Badkamers badkamerspecialisten koppelt.",
             "Van Almere en Lelystad tot Zwolle, Amersfoort en Hilversum.",
             "Vergelijk gratis offertes in jouw gemeente."),
        "/werkgebied/", body, [cr_ld]), prio=0.8)


def build_plaats_pages():
    reno = dienst("badkamer-renoveren") or DIENSTEN[0]
    for p in PLAATSEN:
        buren = buurplaatsen(p, 8)
        buren_li = "".join(f'<li><a href="/badkamerspecialist/{b["slug"]}/">Badkamer {b["naam"]}</a></li>' for b in buren)
        cr, cr_ld = crumbs([("Home", "/"), ("Werkgebied", "/werkgebied/"), (p["naam"], None)])
        r_van, r_tot = lokale_prijs(reno, p)

        hero = f"""<section class="section-sm">
<div class="wrap">
  <div class="grid g2" style="gap:48px;align-items:start">
    <div>
      <span class="badge">{p['gemeente']} · {p['provincie']}</span>
      <h1>Nieuwe badkamer in {p['naam']}?</h1>
      <p class="lead">Vergelijk vrijblijvend offertes van badkamerspecialisten die in {p['naam']} werken. Eén aanvraag, tot drie prijzen, en je zit nergens aan vast.</p>
      <p>{p['hook']}</p>
      <ul class="checklist">
        <li>Bedrijven die {p['naam']} en omgeving als werkgebied hebben</li>
        <li>Gecontroleerd op KvK-inschrijving en aansprakelijkheidsverzekering</li>
        <li>Gratis vergelijken, geen abonnement, geen verplichtingen</li>
      </ul>
      <div class="callout callout-prijs"><p><strong>Richtprijs complete badkamer in {p['naam']}:</strong> {eur(r_van)} – {eur(r_tot)} {reno['prijs_eenheid']}{incl(reno)}. De prijzen per klus zie je <a href="#prijzen">hieronder</a>.</p></div>
    </div>
    <div>{offerte_form(f"Offertes van badkamerspecialisten in {p['naam']}", "Vier korte vragen · gratis en vrijblijvend")}</div>
  </div>
</div>
</section>"""

        diensten_sec = f"""<section class="section soft"><div class="wrap">
  <div class="center" style="max-width:640px;margin:0 auto 40px">
    <h2>Welke badkamerklus heb je in {p['naam']}?</h2>
    <p class="lead">Klik door voor de richtprijzen per klus en vraag direct offertes aan bij lokale bedrijven.</p>
  </div>
  {dienst_cards(p['slug'], p['naam'])}
</div></section>"""

        v = PLAATSEN.index(p) % 3
        if v == 0:
            blok = f"""<h3>Waarom je in {p['naam']} meerdere offertes wilt</h3>
  <p>Badkamerbedrijven verschillen sterk. Het ene bedrijf doet alles zelf, van sloop tot tegelwerk; het andere werkt met een vaste tegelzetter en een installateur, of levert ook het sanitair uit een eigen showroom. Dat zie je terug in de prijs en in de planning. Met één offerte weet je nooit in welke categorie je terecht bent gekomen.</p>"""
        elif v == 1:
            blok = f"""<h3>Lokaal of van verderop?</h3>
  <p>Veel mensen zoeken bewust een bedrijf uit {p['naam']} zelf. Begrijpelijk, maar niet altijd de scherpste keuze. Een badkamerrenovatie duurt al snel één tot drie weken, en dan wegen voorrijkosten nauwelijks mee. Kijk dus naar {p['gemeente']} én de gemeenten eromheen.</p>"""
        else:
            blok = f"""<h3>Wat een badkamerspecialist van je nodig heeft</h3>
  <p>Hoe concreter je vraag, hoe scherper de offerte. Noem de afmetingen van de badkamer, of het toilet erin zit of apart, wat er weg moet (bad, douchebak, tegels) en wat je ervoor terug wilt. Vertel ook het bouwjaar van je huis. Een paar foto's na het eerste contact scheelt een hoop onzekerheid, en onzekerheid rekent een bedrijf altijd mee in de prijs.</p>"""

        prijs_sec = f"""<section class="section" id="prijzen"><div class="wrap narrow prose">
  <h2>Wat kost een badkamerspecialist in {p['naam']}?</h2>
  <p>{INDEX_TOELICHTING.get(p['provincie'], '')} De meeste bedrijven werken met een vaste prijs voor de hele klus, zodat je vooraf weet waar je aan toe bent.</p>
  {prijstabel(plaats=p)}

  {cta_midden(f"Prijzen in {p['naam']} vergelijken?", "Eén aanvraag, maximaal drie offertes van bedrijven die in " + p['naam'] + " werken.")}

  <h3>De woningen in {p['naam']}</h3>
  <p>{bouwperiode_zin(p)} Het gaat overwegend om {p['woningmix']}. Dat is relevant voor je offerte: het bouwjaar zegt iets over de leidingen, de afvoer en hoeveel ruimte er in de badkamer is.</p>

  {blok}
</div></section>"""

        buren_sec = f"""<section class="section soft"><div class="wrap">
  <h2>Ook actief rond {p['naam']}</h2>
  <p class="lead" style="max-width:60ch">Zoek je in een buurgemeente?</p>
  <ul class="places" style="margin-top:22px">{buren_li}</ul>
</div></section>"""

        faqs = [
            (f"Hoeveel bedrijven in {p['naam']} nemen contact met mij op?",
             "Maximaal drie. Zo kun je goed vergelijken zonder dat je de hele week wordt gebeld. Reageren er minder, dan zijn er op dat moment niet meer bedrijven met ruimte in de agenda."),
            (f"Werken deze bedrijven ook echt in {p['naam']}?",
             f"We koppelen alleen bedrijven die {p['naam']} en omgeving in hun werkgebied hebben. Zo voorkom je hoge voorrijkosten van een bedrijf dat drie provincies verderop zit."),
            ("Hoe lang duurt een badkamerrenovatie?",
             "Reken voor een complete badkamer op één tot drie weken, afhankelijk van de grootte en hoeveel er verlegd moet worden. Een toilet vervangen of een kraan plaatsen is meestal binnen een dag klaar."),
            ("Welk btw-tarief betaal ik voor een nieuwe badkamer?",
             "In principe 21%, over het werk en het sanitair. Het lage tarief van 9% geldt alleen voor een paar soorten werk aan een woning ouder dan twee jaar, zoals schilderen, stukadoren en isoleren."),
            ("Kan ik ook zakelijk aanvragen, bijvoorbeeld voor een VvE?",
             f"Ja. VvE's, verhuurders en bedrijven in {p['naam']} volgen dezelfde route. Kies bij de eerste vraag voor zakelijk, dan komt je aanvraag bij bedrijven terecht die zulke projecten aankunnen."),
        ] + lokale_faq(p)
        faq_html, faq_ld = faq_blok(faqs, f"Veelgestelde vragen over badkamers in {p['naam']}")

        svc_ld = {
            "@context": "https://schema.org",
            "@type": "Service",
            "serviceType": "Badkamerrenovatie",
            "name": f"Badkamerspecialist vinden in {p['naam']}",
            "provider": {"@id": SITE["url"] + "/#organization"},
            "areaServed": {"@type": "City", "name": p["naam"],
                           "containedInPlace": {"@type": "AdministrativeArea", "name": p["provincie"]}},
            "description": f"Vergelijk gratis offertes van badkamerspecialisten in {p['naam']} ({p['provincie']}).",
        }

        body = (cr + hero + diensten_sec + hoe_werkt_het(p["naam"]) + prijs_sec + plaats_sectie(p)
                + faq_html + buren_sec
                + cta_blok(f"Badkamerspecialist zoeken in {p['naam']}?",
                           f"Vul het formulier in en ontvang vrijblijvend offertes van maximaal drie bedrijven die in {p['naam']} werken."))

        write(f"/badkamerspecialist/{p['slug']}/", page(
            title(f"Badkamer {p['naam']}: vergelijk gratis 3 offertes"),
            desc(f"Nieuwe badkamer in {p['naam']}?",
                 f"Vergelijk vrijblijvend offertes van badkamerspecialisten uit {p['gemeente']}.",
                 "Complete badkamer, inloopdouche, toilet en tegelwerk.",
                 "Gratis en zonder verplichtingen."),
            f"/badkamerspecialist/{p['slug']}/", body, [cr_ld, faq_ld, svc_ld]),
            prio=0.9 if p["prio"] == 1 else 0.7)


def build_plaats_dienst_pages():
    for p in PLAATSEN:
        dun = p["inwoners"] < DORP_GRENS  # kleine dorpen: wel bereikbaar, niet in Google
        buren = [b for b in buurplaatsen(p, 8) if b["inwoners"] >= DORP_GRENS][:5]
        for d in DIENSTEN:
            cr, cr_ld, body_top = dienst_body(d, p)
            p_van, p_tot = lokale_prijs(d, p)

            voorbeeld = ""
            if "m²" in d["prijs_eenheid"]:
                voorbeeld = (f"<h3>Rekenvoorbeeld</h3><p>Een gemiddelde badkamer heeft zo'n 25 m² aan wand- en vloertegels. "
                             f"Met de richtprijs voor {p['provincie']} kom je dan uit op <strong>{eur(25 * p_van)} tot {eur(25 * p_tot)}</strong>"
                             f"{incl(d)}. Sloopwerk, waterdicht maken en tegels uit het hogere segment komen daar nog bij.</p>")

            buren_links = ", ".join(f'<a href="/badkamerspecialist/{b["slug"]}/{d["slug"]}/">{b["naam"]}</a>' for b in buren)
            lokaal = f"""<section class="section"><div class="wrap narrow prose">
  <h2>{d['naam']} in {p['naam']}: wat je moet weten</h2>
  <p>{bouwperiode_zin(p)} Je vindt er vooral {p['woningmix']}. {p['hook']}</p>

  <h3>Richtprijs in {p['provincie']}</h3>
  <p>Voor {d['naam'].lower()} in {p['naam']} zie je prijzen tussen <strong>{eur(p_van)} en {eur(p_tot)}</strong> {d['prijs_eenheid']}. {INDEX_TOELICHTING.get(p['provincie'], '')}</p>
  <p>Ligt een offerte daar duidelijk boven, vraag dan om een specificatie per onderdeel. Ligt hij er ver onder, kijk dan juist goed: het verschil zit meestal in wat er niet in de prijs zit, zoals sloopwerk, leidingwerk of een te lage stelpost voor sanitair.</p>

  {voorbeeld}

  {cta_midden(f"Offertes voor {d['naam'].lower()} in {p['naam']}?", "Vraag gratis prijzen aan bij maximaal drie bedrijven uit de buurt. Je zit nergens aan vast.")}
  {dienst_blok(d, p)}

  <h3>Ook in de buurt</h3>
  <p>Zoek je {d['naam'].lower()} net over de gemeentegrens? Bekijk dan {buren_links or '<a href="/werkgebied/">het hele werkgebied</a>'}.</p>
</div></section>"""

            faqs = list(d["faq"][:2]) + [
                (f"Wat kost {d['naam'].lower()} in {p['naam']}?",
                 f"Reken in {p['naam']} op {eur(p_van)} tot {eur(p_tot)} {d['prijs_eenheid']}{incl(d)}."),
                (f"Werken jullie bedrijven ook in {p['naam']}?",
                 f"Ja. We koppelen je aan bedrijven die {p['naam']} in hun werkgebied hebben staan, zodat je geen onnodige voorrijkosten betaalt."),
            ] + lokale_dienst_faq(d, p)
            faq_html, faq_ld = faq_blok(faqs, f"Vragen over {d['naam'].lower()} in {p['naam']}")

            andere = f"""<section class="section soft"><div class="wrap">
  <h2>Andere badkamerklussen in {p['naam']}</h2>
  {dienst_cards(p['slug'], p['naam'], exclude=d['slug'])}
  <p style="margin-top:22px"><a href="/badkamerspecialist/{p['slug']}/">Alles over badkamers in {p['naam']} →</a></p>
</div></section>"""

            svc_ld = {
                "@context": "https://schema.org",
                "@type": "Service",
                "serviceType": d["naam"],
                "name": f"{d['naam']} in {p['naam']}",
                "provider": {"@id": SITE["url"] + "/#organization"},
                "areaServed": {"@type": "City", "name": p["naam"]},
                "description": f"{d['kort']} in {p['naam']}. Vergelijk gratis offertes van lokale bedrijven.",
                "offers": {"@type": "AggregateOffer", "priceCurrency": "EUR", "lowPrice": p_van, "highPrice": p_tot},
            }

            body = (cr + body_top + lokaal + faq_html + andere
                    + cta_blok(f"{d['naam']} in {p['naam']} laten doen?",
                               "Eén formulier, maximaal drie offertes van bedrijven uit de buurt. Gratis en vrijblijvend."))

            t = f"{d['naam']} {p['naam']}: kosten &amp; 3 offertes"
            if len(t.replace("&amp;", "&")) > 60:
                t = f"{d['naam_kort']} {p['naam']}: kosten &amp; offertes"
            write(f"/badkamerspecialist/{p['slug']}/{d['slug']}/", page(
                title(t),
                desc(f"{d['naam']} in {p['naam']}?",
                     f"Richtprijs {eur(p_van)}–{eur(p_tot)} {d['prijs_eenheid']}.",
                     "Vergelijk gratis en vrijblijvend offertes van maximaal 3 lokale bedrijven.",
                     f"Actief in heel {p['gemeente']}.", "Geen verplichtingen."),
                f"/badkamerspecialist/{p['slug']}/{d['slug']}/", body, [cr_ld, faq_ld, svc_ld], noindex=dun),
                prio=0.7 if p["prio"] == 1 else 0.5, index=not dun)


# ===========================================================================
# CONVERSIEPAGINA'S
# ===========================================================================

def build_offerte_aanvragen():
    cr, cr_ld = crumbs([("Home", "/"), ("Offertes aanvragen", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap">
  <div class="grid g2" style="gap:48px;align-items:start">
    <div>
      <span class="badge">Gratis &amp; vrijblijvend</span>
      <h1>Vraag gratis 3 offertes aan</h1>
      <p class="lead">Vier korte vragen en je bent klaar. Wij zoeken badkamerspecialisten in jouw regio die dit werk doen en op dit moment ruimte hebben.</p>
      <ul class="checklist">
        <li><strong>Kost je niets.</strong> Aanvragen en vergelijken is gratis. Wij worden betaald door de bedrijven.</li>
        <li><strong>Maximaal drie bedrijven.</strong> Je nummer gaat nooit naar meer partijen.</li>
        <li><strong>Geen verplichting.</strong> Alle drie afwijzen mag, zonder uitleg.</li>
      </ul>
      <div class="callout">
        <p><strong>Tip:</strong> hoe concreter je omschrijving, hoe scherper de offertes. Noem de afmetingen van de badkamer, wat er weg moet en wat je ervoor terug wilt, en het bouwjaar van je huis. Foto's kun je na het eerste contact altijd nog sturen.</p>
      </div>
      <p style="margin-top:18px">Heb je al een offerte? <a href="/tools/offertechecker/">Check hem eerst per regel</a>. Daarna kun je de specificatie, zonder je gegevens, meenemen in deze aanvraag.</p>
    </div>
    <div>{offerte_form("Start je aanvraag", "Klaar in ongeveer een minuut")}</div>
  </div>
</div></section>
{hoe_werkt_het()}
{cta_blok("Liever eerst weten wat het kost?", "Bekijk het prijzenoverzicht met richtprijzen per badkamerklus.", "Naar het prijzenoverzicht")}"""
    write("/offerte-aanvragen/", page(
        title("Gratis 3 badkameroffertes aanvragen"),
        desc("Vraag in een minuut gratis offertes aan bij maximaal 3 badkamerspecialisten uit jouw regio.",
             "Vrijblijvend en zonder kosten voor jou."),
        "/offerte-aanvragen/", body, [cr_ld]), prio=0.9, freq="weekly")


def build_voor_vakmensen():
    cr, cr_ld = crumbs([("Home", "/"), ("Voor badkamerspecialisten", None)])
    dienstopties = "".join(
        f'<label><input type="checkbox" name="diensten" value="{d["naam"]}"><span>{d["naam"]}</span></label>'
        for d in DIENSTEN)
    faqs = [
        ("Zit ik vast aan een contract?",
         "Nee. Je betaalt per aanvraag, niet per maand. Zit je agenda vol, dan laat je het ons weten en pauzeren we tot je weer ruimte hebt."),
        ("Wat als een aanvraag niet deugt?",
         "Verkeerd nummer, dubbele aanvraag of iemand die duidelijk buiten je werkgebied zit: meld het binnen vijf werkdagen en je krijgt de aanvraag gecrediteerd."),
        ("Hoeveel bedrijven krijgen dezelfde aanvraag?",
         "Maximaal drie, inclusief jij."),
        ("Kan ik mijn werkgebied en het soort klussen begrenzen?",
         "Ja. Je geeft door in welke plaatsen je werkt, welke klussen je doet (bijvoorbeeld alleen complete badkamers, of juist ook kleine klussen) en hoeveel aanvragen je per maand maximaal wilt."),
        ("Wat kost een aanvraag?",
         "Dat hangt af van het soort klus: een complete badkamer is meer waard dan een kraan vervangen. We bespreken de tarieven bij je aanmelding, voordat je iets ontvangt."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Vragen van badkamerspecialisten")

    body = f"""{cr}
<section class="section-sm"><div class="wrap">
  <div class="grid g2" style="gap:48px;align-items:start">
    <div>
      <span class="badge">Voor badkamerspecialisten</span>
      <h1>Badkameraanvragen uit jouw regio, betaal per aanvraag</h1>
      <p class="lead">Voor badkamerbedrijven, installateurs en tegelzetters. Geen maandabonnement en geen opstartkosten: je betaalt alleen voor de aanvragen die je ontvangt, en je bepaalt zelf je werkgebied en je maximum per maand.</p>
      <ul class="checklist">
        <li>Aanvragen uit jouw eigen plaats en omliggende gemeenten</li>
        <li>Maximaal drie bedrijven per aanvraag</li>
        <li>Elke aanvraag eerst gecontroleerd, daarna per e-mail naar jou</li>
        <li>Ongeldige aanvragen worden gecrediteerd</li>
        <li>Opzeggen of pauzeren kan per direct</li>
      </ul>
      <p><a class="btn btn-primary btn-lg" href="#aanmelden">Vrijblijvend aanmelden</a></p>
    </div>
    <div id="aanmelden">
      <div class="formcard">
        <h2>Meld je bedrijf aan</h2>
        <p class="sub">We nemen contact op om je werkgebied door te nemen</p>
        <div class="steps"><div class="on"></div><div></div></div>
        <form data-wizard data-table="monteurs" novalidate>
          <div class="step active">
            <div class="field">
              <label for="s-bedrijf">Bedrijfsnaam</label>
              <input type="text" id="s-bedrijf" name="bedrijfsnaam" required autocomplete="organization">
            </div>
            <div class="row2">
              <div class="field">
                <label for="s-contact">Contactpersoon</label>
                <input type="text" id="s-contact" name="contactpersoon" required autocomplete="name">
              </div>
              <div class="field">
                <label for="s-kvk">KvK-nummer</label>
                <input type="text" id="s-kvk" name="kvk" required inputmode="numeric">
              </div>
            </div>
            <div class="row2">
              <div class="field">
                <label for="s-mail">E-mailadres</label>
                <input type="email" id="s-mail" name="email" required autocomplete="email">
              </div>
              <div class="field">
                <label for="s-tel">Telefoonnummer</label>
                <input type="tel" id="s-tel" name="telefoon" required autocomplete="tel">
              </div>
            </div>
            <div class="err"></div>
            <div class="formnav"><button type="button" class="btn btn-primary" data-next>Volgende</button></div>
          </div>
          <div class="step">
            <div class="field">
              <label for="s-gebied">In welke plaatsen werk je?</label>
              <input type="text" id="s-gebied" name="werkgebied" required placeholder="Zeewolde, Almere, Harderwijk">
            </div>
            <div class="field">
              <label>Welk werk doe je? <span class="hint">(meerdere mogelijk)</span></label>
              <div class="choice">{dienstopties}</div>
            </div>
            <div class="field">
              <label>Hoeveel aanvragen wil je maximaal per maand?</label>
              <div class="choice">
                <label><input type="radio" name="leads_per_maand" value="1-5" data-required><span>1 – 5</span></label>
                <label><input type="radio" name="leads_per_maand" value="6-15" data-required><span>6 – 15</span></label>
                <label><input type="radio" name="leads_per_maand" value="16-30" data-required><span>16 – 30</span></label>
                <label><input type="radio" name="leads_per_maand" value="Zoveel mogelijk" data-required><span>Zoveel mogelijk</span></label>
              </div>
            </div>
            <div class="err"></div>
            <div class="formnav">
              <button type="button" class="btn btn-ghost" data-prev>Terug</button>
              <button type="submit" class="btn btn-primary" data-submit>Aanmelden</button>
            </div>
            <p class="formfoot">Aanmelden is vrijblijvend. Je zit nergens aan vast tot je de eerste aanvraag accepteert.</p>
          </div>
        </form>
        <div class="success">
          <div class="big">{icon('check',26)}</div>
          <h2>Aanmelding ontvangen</h2>
          <p>We nemen contact met je op om je werkgebied en de tarieven door te nemen.</p>
        </div>
      </div>
    </div>
  </div>
</div></section>

<section class="section"><div class="wrap narrow prose">
  <h2>Zo werkt het als je je aanmeldt</h2>
  <ol>
    <li><strong>Je meldt je aan</strong> met je bedrijfsgegevens, je werkgebied en het werk dat je doet.</li>
    <li><strong>We nemen contact op</strong> om je werkgebied, de soorten klussen, je maximum en de tarieven door te nemen.</li>
    <li><strong>Je ontvangt aanvragen</strong> uit jouw gebied, met de omschrijving en de contactgegevens van de aanvrager.</li>
    <li><strong>Jij neemt contact op</strong> en maakt je eigen offerte. De opdracht sluit je rechtstreeks met de klant.</li>
  </ol>

  <h2>Hoe wij aanvragen binnenhalen</h2>
  <p>Via Google. Mensen die zoeken op bijvoorbeeld &quot;badkamer renoveren Almere&quot; of &quot;wat kost een inloopdouche&quot; komen op onze pagina's terecht en vragen daar offertes aan. Iemand die actief zoekt, heeft al een klus in gedachten.</p>

  <h2>Wat we van jou verwachten</h2>
  <ul class="checklist">
    <li>Bel of mail binnen één werkdag. Aanvragers vergelijken, en wie als eerste belt heeft een voorsprong.</li>
    <li>Geef een nette, gespecificeerde offerte, met sanitair en tegels per post of als duidelijke stelpost.</li>
    <li>Meld het als een aanvraag niet deugt, dan crediteren we hem.</li>
    <li>Geldige KvK-inschrijving en een aansprakelijkheidsverzekering.</li>
  </ul>
</div></section>
{faq_html}
<section class="section"><div class="wrap">
  <div class="cta">
    <h2>Klaar om aanvragen te ontvangen?</h2>
    <p>Meld je vrijblijvend aan. We nemen contact op voordat je iets ontvangt.</p>
    <a class="btn btn-primary btn-lg" href="#aanmelden">Aanmelden als badkamerspecialist</a>
  </div>
</div></section>"""
    write("/voor-badkamerspecialisten/", page(
        title("Aanvragen voor badkamerspecialisten"),
        desc("Ontvang aanvragen voor badkamers, inloopdouches, toiletten en tegelwerk uit jouw regio.",
             "Geen abonnement: je betaalt per aanvraag, met maximaal 3 bedrijven per aanvraag.",
             "Werkgebied en maximum bepaal je zelf."),
        "/voor-badkamerspecialisten/", body, [cr_ld, faq_ld]), prio=0.8)


def build_prijzen():
    cr, cr_ld = crumbs([("Home", "/"), ("Prijzen", None)])
    blokken = ""
    for d in DIENSTEN:
        fact = "".join(f"<li>{x}</li>" for x in d["prijsfactoren"][:3])
        blokken += f"""<h3 id="{d['slug']}">{d['naam']}: {eur(d['prijs_van'])} – {eur(d['prijs_tot'])} {d['prijs_eenheid']}</h3>
<p>{d['prijs_extra']}</p>
<p><strong>Grootste prijsbepalers:</strong></p><ul>{fact}</ul>
<p><a href="/diensten/{d['slug']}/">Alles over {d['naam'].lower()} →</a></p>"""

    faqs = [
        ("Waarom lopen badkameroffertes zo ver uiteen?",
         "Meestal door wat er wel en niet in zit: sloopwerk, afvoer van puin, leidingwerk, elektra, waterdicht maken en de stelpost voor sanitair en tegels. Een offerte die duizenden euro's lager is, is vaak niet goedkoper maar minder compleet."),
        ("Welk btw-tarief geldt voor een nieuwe badkamer?",
         "In principe 21%, over het werk en de materialen. Het lage tarief van 9% geldt alleen voor bepaalde werkzaamheden aan een woning ouder dan twee jaar, zoals schilderen, stukadoren en isoleren."),
        ("Is het goedkoper om zelf sanitair te kopen?",
         "Soms, maar let op: een bedrijf geeft meestal geen garantie op wat het niet zelf levert, en als een onderdeel niet past of ontbreekt, loopt de planning uit. Spreek het vooraf af en laat het in de offerte zetten."),
        ("Wat is een stelpost?",
         "Een bedrag in de offerte voor iets wat nog niet precies vastligt, zoals sanitair of tegels die je later uitkiest. Kies je duurder, dan betaal je het verschil bij. Vraag dus wat er voor dat bedrag in zit."),
        ("Kan ik besparen zonder in te leveren op kwaliteit?",
         "Ja. Laat de leidingen en de afvoer op hun plek als dat kan, kies standaardmaten voor tegels en sanitair, en sloop eventueel zelf (na overleg, en niet als er mogelijk asbest zit)."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over badkamerprijzen")

    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Bijgewerkt {TODAY[:7].replace('-', '/')}</span>
  <h1>Badkamerprijzen {TODAY[:4]}: richtprijzen per klus</h1>
  <p class="lead">Het eerlijke antwoord: dat hangt ervan af. Maar met de richtprijzen hieronder weet je snel of een offerte in de goede orde van grootte zit, en welke vragen je moet stellen als dat niet zo is.</p>

  <h2>Richtprijzen per badkamerklus</h2>
  {prijstabel()}

  <p>Wil je per klus de details, met rekenvoorbeelden? Kijk bij <a href="/kosten/">alle kostenpagina's</a> of reken het zelf uit met de <a href="/tools/badkamercalculator/">badkamercalculator</a>.</p>

  <h2>Per klus toegelicht</h2>
  {blokken}

  <h2>Welke btw betaal je?</h2>
  <p>Voor een nieuwe badkamer betaal je in principe <strong>21% btw</strong>, over het werk en over het sanitair, de tegels en de andere materialen. Het lage tarief van 9% geldt alleen voor een beperkt aantal werkzaamheden aan een woning die ouder is dan twee jaar, zoals schilderen, stukadoren en het aanbrengen van isolatie (<a href="{BTW_BRON}" rel="nofollow noopener">Belastingdienst</a>). Combineert een offerte die werkzaamheden met het badkamerwerk, dan hoort het bedrijf de posten te splitsen.</p>

  <h2>Wat een richtprijs niet vertelt</h2>
  <p>Een richtprijs gaat uit van een gewone klus. Je prijs komt hoger uit als er veel verlegd moet worden, als de vloer moet worden opgehoogd of de afvoer niet op de goede plek ligt, als er asbest gesaneerd moet worden of als je duur sanitair en grote tegels kiest. Gebruik een richtprijs dus om te zien of een offerte in de buurt zit, niet als bedrag dat je mag verwachten.</p>

  <h2>Hoe je offertes eerlijk vergelijkt</h2>
  <p>Leg ze naast elkaar en check per offerte: wat er gesloopt en afgevoerd wordt, welk sanitair en welke tegels (of hoe hoog de stelposten zijn), het leidingwerk en de elektra, hoe de douche waterdicht wordt gemaakt, de btw, de garantie en de planning. Ontbreekt er iets, dan is dat geen detail maar een toekomstige meerprijs.</p>
  {offertecheck_blok()}
</div></section>
{faq_html}
{cta_blok("Benieuwd wat het bij jou kost?", "Richtprijzen zijn een startpunt. Een echte prijs krijg je pas als een badkamerspecialist naar jouw situatie kijkt. Vraag gratis drie offertes aan.")}"""
    write("/prijzen/", page(
        title(f"Wat kost een nieuwe badkamer in {TODAY[:4]}? Prijzen"),
        desc(f"Badkamerprijzen {TODAY[:4]}: wat kost een complete badkamer, een inloopdouche, een toilet of tegelwerk?",
             "Met btw-regels en tips om offertes te vergelijken."),
        "/prijzen/", body, [cr_ld, faq_ld]), prio=0.9, freq="weekly")


# ===========================================================================
# STATISCHE PAGINA'S
# ===========================================================================

def build_static_pages():
    naam = SITE["naam"]

    # --- Over ons ---
    cr, cr_ld = crumbs([("Home", "/"), ("Over ons", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Over {naam}</h1>
  <p class="lead">{naam} is opgezet omdat een goede badkamerspecialist vinden onnodig lastig is. Je belt een paar bedrijven, de helft belt niet terug, en de offertes die je krijgt zijn zo verschillend opgebouwd dat je ze niet kunt vergelijken.</p>

  <h2>Wat we doen</h2>
  <p>Wij verzamelen jouw aanvraag en zetten die door naar maximaal drie bedrijven die in jouw regio werken en het gevraagde werk doen. Zij nemen rechtstreeks contact met je op. Wij zitten daar verder niet tussen: je onderhandelt zelf, je kiest zelf, en de opdracht sluit je rechtstreeks met het bedrijf.</p>

  <h2>Hoe we geld verdienen</h2>
  <p>Bedrijven betalen ons per aanvraag die ze ontvangen. Voor jou als aanvrager is de dienst gratis en er zit geen opslag op de offertes. Wij hebben er belang bij dat je een goed bedrijf vindt, want een bedrijf dat slecht werk levert of niet terugbelt, kost ons uiteindelijk aanvragers.</p>

  <h2>Welke bedrijven we toelaten</h2>
  <ul class="checklist">
    <li>Geldige inschrijving bij de Kamer van Koophandel</li>
    <li>Aansprakelijkheidsverzekering voor bedrijven</li>
    <li>Ervaring met het type werk waarvoor ze aanvragen ontvangen</li>
    <li>Reactie binnen één werkdag op een doorgestuurde aanvraag</li>
  </ul>
  <p>Bij herhaalde klachten stoppen we de samenwerking.</p>

  <h2>Waar we werken</h2>
  <p>We beginnen in Flevoland, de randmeren, de Veluwe, de IJsseldelta, Amersfoort en het Gooi. <a href="/werkgebied/">Bekijk alle plaatsen</a>.</p>

  <h2>Contact</h2>
  <p>Vragen, klachten of een suggestie? Mail naar <a href="mailto:{SITE['email']}">{SITE['email']}</a> of ga naar de <a href="/contact/">contactpagina</a>.</p>
</div></section>
{cta_blok()}"""
    write("/over-ons/", page(
        title(f"Over {naam}: zo werken we", brand=""),
        f"{naam} koppelt aanvragers aan badkamerspecialisten in hun regio. Lees hoe we werken, welke bedrijven we toelaten en waarom het voor jou gratis is.",
        "/over-ons/", body, [cr_ld]), prio=0.5)

    # --- Contact ---
    btwregel = f"<br>Btw {SITE['btw']}" if SITE.get("btw") else ""
    cr, cr_ld = crumbs([("Home", "/"), ("Contact", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap">
  <div class="grid g2" style="gap:48px;align-items:start">
    <div class="prose">
      <h1>Contact</h1>
      <p class="lead">Een vraag over je aanvraag, een klacht over een bedrijf of interesse om je bedrijf aan te melden? Laat het weten.</p>
      <h3>E-mail</h3>
      <p><a href="mailto:{SITE['email']}">{SITE['email']}</a></p>
      <h3>Ik zoek een badkamerspecialist</h3>
      <p>Dat gaat het snelst via het <a href="/offerte-aanvragen/">aanvraagformulier</a>. Je aanvraag komt dan direct bij de juiste bedrijven terecht.</p>
      <h3>Ik ben badkamerspecialist</h3>
      <p>Kijk op <a href="/voor-badkamerspecialisten/">voor badkamerspecialisten</a> en meld je daar vrijblijvend aan.</p>
      <h3>Klacht over een bedrijf</h3>
      <p>Mail ons met een korte omschrijving. We nemen elke klacht op in het dossier van het betreffende bedrijf en stoppen de samenwerking bij herhaling.</p>
      <h3>Bedrijfsgegevens</h3>
      <p>{naam}<br>{SITE['adres']}<br>KvK {SITE['kvk']}{btwregel}</p>
    </div>
    <div>
      <div class="formcard">
        <h2>Stuur een bericht</h2>
        <p class="sub">We reageren zo snel mogelijk</p>
        <div class="steps"><div class="on"></div></div>
        <form data-wizard data-table="berichten" novalidate>
          <div class="step active">
            <div class="field">
              <label for="k-naam">Naam</label>
              <input type="text" id="k-naam" name="naam" required autocomplete="name">
            </div>
            <div class="field">
              <label for="k-mail">E-mailadres</label>
              <input type="email" id="k-mail" name="email" required autocomplete="email">
            </div>
            <div class="field">
              <label for="k-ber">Bericht</label>
              <textarea id="k-ber" name="bericht" required></textarea>
            </div>
            <div class="err"></div>
            <div class="formnav"><button type="submit" class="btn btn-primary btn-block" data-submit>Versturen</button></div>
          </div>
        </form>
        <div class="success">
          <div class="big">{icon('check',26)}</div>
          <h2>Bericht verstuurd</h2>
          <p>Bedankt. We reageren zo snel mogelijk.</p>
        </div>
      </div>
    </div>
  </div>
</div></section>"""
    write("/contact/", page(
        f"Contact met {naam}: vragen, klachten en aanmelden",
        desc(f"Neem contact op met {naam}: vragen over je offerteaanvraag, een klacht over een bedrijf",
             "of je bedrijf aanmelden als badkamerspecialist."),
        "/contact/", body, [cr_ld]), prio=0.4)

    # --- Privacy ---
    adres = SITE['domein'] or SITE['url'].split('//')[1]
    cr, cr_ld = crumbs([("Home", "/"), ("Privacy", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Privacyverklaring</h1>
  <p><small>Laatst bijgewerkt: {TODAY}</small></p>

  <h2>Wie zijn wij</h2>
  <p>{naam}, gevestigd te {SITE['adres']}, KvK {SITE['kvk']}, is verwerkingsverantwoordelijke voor de gegevens die via {adres} worden verzameld. Contact: <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>

  <h2>Welke gegevens verzamelen we</h2>
  <ul>
    <li><strong>Aanvraaggegevens:</strong> naam, e-mailadres, telefoonnummer, postcode, plaats, type woning en de omschrijving van je klus.</li>
    <li><strong>Technische gegevens:</strong> de pagina waarop je de aanvraag deed, de verwijzende website en eventuele campagneparameters (utm-tags, gclid of fbclid).</li>
    <li><strong>Advertentiemeting (alleen met toestemming):</strong> via de Meta-pixel, als die is ingesteld. Zie hieronder bij Meta.</li>
    <li><strong>Gegevens van bedrijven:</strong> bedrijfsnaam, KvK-nummer, contactpersoon, e-mail, telefoon en werkgebied.</li>
  </ul>

  <h2>Waarom en op welke grondslag</h2>
  <p>We verwerken je gegevens om je aanvraag door te sturen naar maximaal drie bedrijven. De grondslag is de uitvoering van de overeenkomst die ontstaat op het moment dat je het formulier verstuurt. Voor advertentiemeting is de grondslag je toestemming, die je altijd kunt intrekken.</p>

  <h2>Met wie delen we gegevens</h2>
  <p>Je aanvraaggegevens gaan naar maximaal drie bedrijven die in jouw regio werken. Deze bedrijven betalen ons een vergoeding om je aanvraag te ontvangen. Zij zijn zelfstandig verwerkingsverantwoordelijke voor wat zij daarna met je gegevens doen. <strong>Je contactgegevens en de omschrijving van je klus geven of verkopen we niet aan andere partijen</strong>, en we gebruiken ze niet voor ongevraagde reclame van derden.</p>
  <p>Daarnaast maken we gebruik van verwerkers voor hosting en dataopslag.</p>

  <h2>Meta (Facebook en Instagram)</h2>
  <p>Als we adverteren via Meta, meten we met de Meta-pixel welke advertenties bezoekers en aanvragen opleveren. Die pixel laadt alleen als je in de cookiebanner op Accepteren klikt. Meta ontvangt dan dat je een pagina bekijkt en of er een aanvraag is gedaan, plus technische gegevens zoals je IP-adres. Je naam, e-mailadres, telefoonnummer en de omschrijving van je klus sturen we niet naar Meta. Intrekken kan via Cookie-instellingen onderaan elke pagina. Zie ook de <a href="/cookies/">cookieverklaring</a>.</p>

  <h2>Hoelang bewaren we gegevens</h2>
  <p>Aanvraaggegevens bewaren we maximaal 24 maanden na je aanvraag, tenzij een langere bewaartermijn wettelijk verplicht is. Gegevens van bedrijven bewaren we zolang de samenwerking loopt en daarna zeven jaar in verband met de fiscale bewaarplicht.</p>

  <h2>Jouw rechten</h2>
  <p>Je hebt recht op inzage, correctie, verwijdering, beperking, bezwaar en dataportabiliteit. Stuur een mail naar <a href="mailto:{SITE['email']}">{SITE['email']}</a> en we reageren binnen vier weken. Ben je het oneens met onze reactie, dan kun je een klacht indienen bij de Autoriteit Persoonsgegevens.</p>

  <h2>Beveiliging</h2>
  <p>De website werkt uitsluitend over een beveiligde verbinding (https). Aanvraaggegevens worden opgeslagen in een database met toegangsbeperking.</p>
</div></section>"""
    write("/privacy/", page(f"Privacyverklaring | {naam}",
                            desc(f"Hoe {naam} omgaat met je persoonsgegevens:",
                                 "wat we verzamelen, met wie we het delen, hoelang we het bewaren en welke rechten je hebt."),
                            "/privacy/", body, [cr_ld]), prio=0.3)

    # --- Voorwaarden ---
    cr, cr_ld = crumbs([("Home", "/"), ("Algemene voorwaarden", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Algemene voorwaarden</h1>
  <p><small>Laatst bijgewerkt: {TODAY}</small></p>

  <h2>1. Definities</h2>
  <p><strong>{naam}:</strong> {naam}, KvK {SITE['kvk']}. <strong>Aanvrager:</strong> de particulier of onderneming die via de website een aanvraag indient. <strong>Vakbedrijf:</strong> het bedrijf dat via {naam} aanvragen ontvangt.</p>

  <h2>2. Rol van {naam}</h2>
  <p>{naam} is uitsluitend een bemiddelend platform. Wij brengen aanvragers en vakbedrijven met elkaar in contact. Wij zijn geen partij bij de overeenkomst die daarna tussen aanvrager en vakbedrijf tot stand komt, voeren zelf geen werk uit en zijn niet aansprakelijk voor de uitvoering, kwaliteit, planning of prijs van dat werk.</p>

  <h2>3. Voor aanvragers</h2>
  <p>Het indienen van een aanvraag is gratis en vrijblijvend. Je bent niet verplicht een offerte te accepteren. Door een aanvraag in te dienen ga je ermee akkoord dat maximaal drie vakbedrijven contact met je opnemen via de door jou opgegeven gegevens. Je verklaart dat de opgegeven gegevens juist zijn en dat je bevoegd bent de aanvraag te doen voor het betreffende pand.</p>

  <h2>4. Voor vakbedrijven</h2>
  <p>Het vakbedrijf betaalt per ontvangen aanvraag volgens de tarieven die bij aanmelding schriftelijk zijn afgesproken. Een aanvraag wordt aan maximaal drie vakbedrijven verstrekt. Facturatie gebeurt maandelijks achteraf met een betaaltermijn van veertien dagen.</p>
  <p>Het vakbedrijf kan een aanvraag binnen vijf werkdagen ter creditering aanbieden als het opgegeven telefoonnummer of e-mailadres aantoonbaar onjuist is, de aanvraag een duplicaat is, of de aanvraag buiten het afgesproken werkgebied valt. Het enkele feit dat de aanvrager niet reageert of de opdracht aan een ander gunt, geeft geen recht op creditering.</p>
  <p>Het vakbedrijf moet beschikken over een geldige KvK-inschrijving en een bedrijfsaansprakelijkheidsverzekering, en reageert binnen één werkdag op een ontvangen aanvraag. {naam} kan de samenwerking met onmiddellijke ingang beëindigen bij herhaalde klachten of het niet nakomen van deze verplichtingen.</p>

  <h2>5. Aansprakelijkheid</h2>
  <p>{naam} spant zich in om aanvragen te koppelen aan geschikte vakbedrijven, maar geeft geen garantie op het aantal reacties, de kwaliteit van de offertes of de uitvoering van het werk. Aansprakelijkheid van {naam} is in alle gevallen beperkt tot het bedrag dat de betreffende partij in de drie maanden voorafgaand aan het schadeveroorzakende feit aan {naam} heeft betaald, en bij aanvragers tot nihil aangezien de dienst kosteloos is.</p>

  <h2>6. Klachten</h2>
  <p>Klachten kunnen worden gemeld via <a href="mailto:{SITE['email']}">{SITE['email']}</a>. Wij reageren binnen tien werkdagen.</p>

  <h2>7. Toepasselijk recht</h2>
  <p>Op deze voorwaarden is Nederlands recht van toepassing. Geschillen worden voorgelegd aan de bevoegde rechter in het arrondissement waarin {naam} is gevestigd, onverminderd het recht van consumenten om zich tot de wettelijk bevoegde rechter te wenden.</p>
</div></section>"""
    write("/voorwaarden/", page(f"Algemene voorwaarden | {naam}",
                                desc(f"De algemene voorwaarden van {naam} voor aanvragers en aangesloten vakbedrijven:",
                                     "onze rol, tarieven, creditering en aansprakelijkheid."),
                                "/voorwaarden/", body, [cr_ld]), prio=0.3)

    # --- Cookies ---
    cr, cr_ld = crumbs([("Home", "/"), ("Cookies", None)])
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Cookieverklaring</h1>
  <p><small>Laatst bijgewerkt: {TODAY}</small></p>
  <p>Hier staat welke cookies en welke lokale opslag {naam} gebruikt, waarvoor en hoelang. Cookies van Meta plaatsen we alleen als er een Meta-pixel is ingesteld en je daar toestemming voor geeft.</p>

  <h2>Overzicht</h2>
  <h3>ts_toestemming <small style="font-weight:400">(lokale opslag)</small></h3>
  <ul>
    <li><strong>Van:</strong> {naam}</li>
    <li><strong>Waarvoor:</strong> Onthoudt of je advertentiecookies hebt geaccepteerd of geweigerd.</li>
    <li><strong>Hoelang:</strong> 12 maanden, daarna vragen we het opnieuw</li>
  </ul>
  <h3>ts_attr <small style="font-weight:400">(lokale opslag)</small></h3>
  <ul>
    <li><strong>Van:</strong> {naam}</li>
    <li><strong>Waarvoor:</strong> Bewaart de campagneparameters waarmee je op de site kwam (zoals utm-tags of een gclid). Bij een aanvraag sturen we die mee, zodat we zien via welke campagne de aanvraag binnenkwam.</li>
    <li><strong>Hoelang:</strong> We gebruiken ze tot 90 dagen na je bezoek</li>
  </ul>
  <h3>_fbp en _fbc <small style="font-weight:400">(cookies)</small></h3>
  <ul>
    <li><strong>Van:</strong> Meta</li>
    <li><strong>Waarvoor:</strong> Meten welke advertenties tot bezoeken en aanvragen leiden. Alleen na toestemming.</li>
    <li><strong>Hoelang:</strong> 90 dagen</li>
  </ul>

  <h2>Je keuze wijzigen of intrekken</h2>
  <p>Wil je je keuze later wijzigen, klik dan onderaan elke pagina op <button type="button" class="cookie-instellingen" style="text-decoration:underline">Cookie-instellingen</button>. Je kunt cookies en lokale opslag ook zelf wissen in de instellingen van je browser. Weigeren heeft geen invloed op de werking van de site of de formulieren.</p>

  <h2>Vragen</h2>
  <p>Mail naar <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
</div></section>"""
    write("/cookies/", page(f"Cookieverklaring | {naam}",
                            desc(f"Welke cookies en lokale opslag {naam} gebruikt,",
                                 "waarvoor we campagneparameters bewaren en hoe je cookies in je browser weigert of verwijdert."),
                            "/cookies/", body, [cr_ld]), prio=0.2)

    # --- Fotoverantwoording: nog geen foto's van derden, wel eigen renders ---
    cr, cr_ld = crumbs([("Home", "/"), ("Fotoverantwoording", None)])
    render_lijst = "".join(f"<li>{r['alt']}</li>" for r in list(RENDERS.values()) + list(RENDERS_STIJL.values()))
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Fotoverantwoording</h1>
  <p class="lead">Op deze site staan nog geen foto's van derden. Komen die er, dan staat hier per foto wie hem maakte, onder welke licentie en wat wij eraan veranderden.</p>
  <h2>Eigen 3D-renders</h2>
  <p>De badkamerbeelden op deze site zijn geen foto's maar illustraties: 3D-renders die Top Badkamers zelf maakte met de opensource-software three.js. Er staan geen bestaande badkamers, producten of merken in. Op de site staat bij elke render "Illustratie (3D-render)".</p>
  <ul>{render_lijst}</ul>
</div></section>"""
    write("/fotoverantwoording/", page(f"Fotoverantwoording | {naam}",
                                       desc(f"Per foto op {naam}: de maker, de licentie en de bron.",
                                            "Zelfgemaakte illustraties en renders noemen we ook als zodanig."),
                                       "/fotoverantwoording/", body, [cr_ld]), prio=0.2)

    # --- Bedankt (niet indexeren) ---
    body = f"""<section class="section"><div class="wrap narrow center">
  <div class="big" style="width:64px;height:64px;border-radius:50%;background:#e7f7ef;color:var(--green);display:grid;place-items:center;font-size:1.7rem;margin:0 auto 20px">{icon('check',28)}</div>
  <h1>Bedankt voor je aanvraag</h1>
  <p class="lead">We zoeken nu badkamerspecialisten in jouw regio die bij deze klus passen.</p>
  <p><a class="btn btn-primary" href="/prijzen/">Bekijk alvast de richtprijzen</a></p>
</div></section>"""
    write("/bedankt/", page(f"Bedankt voor je aanvraag | {naam}",
                            "Je aanvraag is ontvangen.", "/bedankt/", body, noindex=True), index=False)

    # --- 404 ---
    html404 = page(f"Pagina niet gevonden | {naam}",
                   "Deze pagina bestaat niet (meer).", "/404/",
                   """<section class="section"><div class="wrap narrow center">
  <h1>Deze pagina bestaat niet</h1>
  <p class="lead">Mogelijk is de link verouderd. Probeer het via een van deze routes:</p>
  <p style="margin-top:26px">
    <a class="btn btn-primary" href="/offerte-aanvragen/">Offertes aanvragen</a>
    <a class="btn btn-ghost" href="/werkgebied/">Alle plaatsen</a>
    <a class="btn btn-ghost" href="/prijzen/">Prijzen</a>
  </p>
</div></section>""", noindex=True)
    with open(os.path.join(OUT, "404.html"), "w", encoding="utf-8") as f:
        f.write(html404)


# ===========================================================================
# ASSETS, SITEMAP, ROBOTS
# ===========================================================================

def build_assets():
    """Schrijft CSS, JS, logo en favicon vanuit assets.py en merk_data.py naar site/assets/."""
    from assets import STYLE_CSS, APP_JS, CONFIG_JS, FAVICON_SVG, TOESTEMMING_JS, css_klein

    bestanden = {
        "css/style.css": css_klein(STYLE_CSS),
        "js/app.js": APP_JS,
        "js/config.js": CONFIG_JS,
        "js/toestemming.js": TOESTEMMING_JS,
        "img/favicon.svg": FAVICON_SVG,
    }
    for pad, inhoud in bestanden.items():
        full = os.path.join(OUT, "assets", pad)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as f:
            f.write(inhoud)

    # pdf.js voor de offertevergelijker (pdf wordt in de browser gelezen)
    pdfjs = os.path.join(ROOT, "vendor", "pdfjs")
    if os.path.isdir(pdfjs):
        shutil.copytree(pdfjs, os.path.join(OUT, "assets", "vendor", "pdfjs"))
    # three.js voor de 3D-badkamer (pas geladen na een klik op "Start 3D")
    three = os.path.join(ROOT, "vendor", "three")
    if os.path.isdir(three):
        shutil.copytree(three, os.path.join(OUT, "assets", "vendor", "three"))

    fotos = os.path.join(ROOT, "fotos")
    if os.path.isdir(fotos) and os.listdir(fotos):
        shutil.copytree(fotos, os.path.join(OUT, "assets", "fotos"))

    from merk_data import BESTANDEN as MERK
    merkmap = os.path.join(OUT, "assets", "merk")
    os.makedirs(merkmap, exist_ok=True)
    for bestandsnaam, inhoud in MERK.items():
        with open(os.path.join(merkmap, bestandsnaam), "w", encoding="utf-8") as f:
            f.write(inhoud)


def build_sitemap():
    lm = lastmod.datums(TODAY)
    urls = "".join(
        f"<url><loc>{SITE['url']}{p}</loc><lastmod>{lm.get(p, TODAY)}</lastmod>"
        f"<changefreq>{freq}</changefreq><priority>{prio}</priority></url>"
        for p, prio, freq in sorted(set(URLS))
    )
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>")
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)

    robots = f"""User-agent: *
Allow: /
Disallow: /bedankt/

Sitemap: {SITE['url']}/sitemap.xml
"""
    with open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    # GitHub Pages: CNAME alleen als er een eigen domein is. .nojekyll voorkomt
    # dat GitHub de site door Jekyll haalt.
    if SITE["domein"]:
        with open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8") as f:
            f.write(SITE["domein"] + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").close()


# ===========================================================================
# FASE 2 EN 3: CONTENT- EN TOOLMODULES
# ===========================================================================
# Elke module heeft LINKS = [(pad, titel, omschrijving), ...] en build(write).

import importlib

CONTENT_MODULES = ["badkamer_kosten", "badkamer_kennis", "badkamer_spullen", "badkamer_spullen2", "badkamer_inspiratie", "badkamer_inspiratie2", "badkamer_verdienmodel", "badkamer_verloop", "badkamer_materialen", "badkamer_doelgroep", "badkamer_voorna"]
TOOL_MODULES = ["badkamer_offertecheck", "badkamer_calculator", "badkamer_check",
                "badkamer_stijl", "badkamer_planner", "badkamer_indeling",
                "badkamer_tegelpatroon", "badkamer_waterverbruik", "badkamer_3d"]


def _laad(namen):
    uit = []
    for naam in namen:
        try:
            uit.append(importlib.import_module(naam))
        except ModuleNotFoundError as e:
            if e.name != naam:
                raise
            print(f"  ! module {naam} ontbreekt, overgeslagen")
    return uit


def build_modules():
    for m in _laad(CONTENT_MODULES) + _laad(TOOL_MODULES):
        m.build(write)


def build_tools_index():
    tools = [l for m in _laad(TOOL_MODULES) for l in m.LINKS]
    if not tools:
        return
    cr, cr_ld = crumbs([("Home", "/"), ("Gratis tools", None)])
    kaarten = "".join(
        f'<a class="card" href="{pad}"><h2 style="font-size:1.15rem;margin:0 0 6px">{t}</h2><p>{o}</p>'
        f'<span class="link">Open de tool →</span></a>' for pad, t, o in tools)
    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Gratis badkamertools</h1>
  <p class="lead">Reken uit wat je badkamer ongeveer kost, plan de verbouwing, check een offerte of probeer een stijl uit. Alles werkt in je browser: je hoeft niets in te vullen over jezelf en er wordt niets opgeslagen.</p>
</div></section>
<section class="section-sm"><div class="wrap"><div class="grid g3">{kaarten}</div></div></section>
{cta_blok("Liever meteen echte prijzen?", "Een tool geeft een indruk. Een badkamerspecialist die bij je langskomt, geeft een echte prijs. Vraag gratis tot drie offertes aan.")}"""
    write("/tools/", page(
        title("Gratis badkamertools: calculator, planner en meer"),
        desc("Gratis badkamertools: bereken de kosten van een nieuwe badkamer, plan je renovatie, check je offerte en probeer stijlen uit.",
             "Werkt in je browser, zonder gegevens."),
        "/tools/", body, [cr_ld]), prio=0.8)


# ===========================================================================

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT, exist_ok=True)

    build_home()
    build_diensten_index()
    build_dienst_pages()
    build_werkgebied()
    build_plaats_pages()
    build_plaats_dienst_pages()
    build_offerte_aanvragen()
    build_voor_vakmensen()
    build_prijzen()
    build_static_pages()
    build_modules()
    build_tools_index()
    build_assets()
    build_sitemap()
    import seo_extra  # seo-ronde 5: schema, gerelateerde pagina's, snelheid
    seo_extra.nabewerken()

    print(f"✓ {len(URLS)} indexeerbare pagina's gegenereerd in {OUT}")
    print(f"  {len(PLAATSEN)} plaatsen, {len(DIENSTEN)} diensten")


if __name__ == "__main__":
    main()
