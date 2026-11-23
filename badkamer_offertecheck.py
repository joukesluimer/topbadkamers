# -*- coding: utf-8 -*-
"""
Offertevergelijker voor badkamerofferte: /tools/offertechecker/

De bezoeker uploadt een pdf (gelezen met pdf.js, lokaal in de browser) of plakt de
tekst van een offerte. De parser (offerte_parser_badkamer.js, inline in de pagina)
deelt elke regel in als product, arbeid, materiaal of overig. Producten (merk, serie,
artikelnummer) gaan naast een marktprijsband uit producten_badkamer.py; arbeid en
materiaal naast de richtprijzen uit richtprijzen.py.

Laag 1 (de check) verstuurt niets. Laag 2 (tegenofferte) staat in een apart blok onder
de uitslag: pas na een eigen klik zie je de geanonimiseerde specificatie, en pas na een
tweede klik gaat die (via sessionStorage) naar het aanvraagformulier. Versturen gebeurt
alleen in dat formulier.

Interface voor build.py: LINKS en build(write). CSS en JS staan in deze module.
"""

import json
import pathlib

from components import page, crumbs, faq_blok, cta_blok, title, eur
from data import DIENST_BY_SLUG
import richtprijzen as RP

# Productdata wordt tegelijk door een andere module gemaakt. Ontbreekt die, dan werkt de
# pagina zonder productniveau (alleen arbeid en materiaal).
try:
    import producten_badkamer as PB
    PRODUCTEN = PB.als_json()
    _PD = getattr(PB, "PRODUCTDATA", {}) or {}
except Exception:  # pragma: no cover - module ontbreekt of is nog in aanbouw
    PRODUCTEN = {}
    _PD = {}

PAD = "/tools/offertechecker/"

LINKS = [
    (PAD, "Offerte vergelijken",
     "Upload of plak je badkamerofferte en zie per regel hoe product, arbeid en materiaal zich verhouden tot de markt."),
]

# Drempels (gelijk aan de parser): arbeid en materiaal pas "boven" of "onder" bij meer dan
# 10% buiten de richtprijs; producten pas "boven" bij meer dan 25% boven de bovenkant van de band.
DREMPEL_ARBEID = 10
DREMPEL_PRODUCT = 25

# ---------------------------------------------------------------------------
# Richtprijzen per post. Bedragen inclusief 21% btw, tenzij excl_btw.
# Alle bedragen en bronnen komen uit richtprijzen.py (gedeeld met de calculator en de
# kostenpagina's). Hier staat alleen hoe de checker ze combineert:
# - sloop: van alleen slopen (laag) tot slopen met dekvloer en afvoer (hoog), omdat offertes
#   die twee vaak in één post zetten;
# - leidingwerk: van op dezelfde plek (laag) tot verplaatsen (leidingwerk hoog + verplaatsen hoog);
# - tegelwerk_incl: legloon plus tegels.
# ---------------------------------------------------------------------------

def _band(van, tot, eenheid, excl_btw=False):
    b = {"van": van, "tot": tot, "eenheid": eenheid}
    if excl_btw:
        b["excl_btw"] = True
    return b


_RP = RP.RICHTPRIJZEN

BANDEN = {
    "sloop":           _band(_RP["sloop"]["laag"], _RP["sloop_compleet"]["hoog"], "post"),
    "afval":           _band(_RP["afval"]["laag"], _RP["afval"]["hoog"], "post"),
    "tegelwerk":       _band(_RP["tegelwerk"]["laag"], _RP["tegelwerk"]["hoog"], "m2"),
    "tegelwerk_incl":  _band(_RP["tegelwerk"]["laag"] + _RP["tegels"]["laag"], _RP["tegelwerk"]["hoog"] + _RP["tegels"]["hoog"], "m2"),
    "tegels":          _band(_RP["tegels"]["laag"], _RP["tegels"]["hoog"], "m2"),
    "leidingwerk":     _band(_RP["leidingwerk"]["laag"], _RP["leidingwerk"]["hoog"] + _RP["leidingwerk_verplaatsen"]["hoog"], "post"),
    "elektra":         _band(_RP["elektra"]["laag"], _RP["elektra"]["hoog"], "post"),
    "vloerverwarming": _band(_RP["vloerverwarming"]["laag"], _RP["vloerverwarming"]["hoog"], "post"),
    "sanitair":        _band(_RP["sanitair"]["laag"], _RP["sanitair"]["hoog"], "post"),
    "kitwerk":         _band(_RP["kitwerk"]["laag"], _RP["kitwerk"]["hoog"], "m"),
    "uur":             _band(_RP["uurtarief"]["laag"], _RP["uurtarief"]["hoog"], "uur", _RP["uurtarief"]["btw"] == "excl"),
}

# Uitleg per band voor de tabel op de pagina: (naam, eenheid-tekst, toelichting, bron-sleutels uit richtprijzen.BRONNEN)
RICHTPRIJS_RIJEN = [
    ("sloop", "Sloopwerk", "per badkamer", "Alleen slopen kan vanaf zo'n €250; met afvoer van het afval en de dekvloer erbij zit je eerder aan de bovenkant.", ["slimster_slopen", "werkspot_slopen", "trustoo_badkamer"]),
    ("afval", "Afvoer van afval", "per badkamer", "Afvoer door het bedrijf, of een container van 3 tot 6 m³ inclusief storten.", ["werkspot_puin", "slimster_afval", "trustoo_badkamer"]),
    ("tegelwerk", "Tegelwerk (zetten)", "per m²", "Alleen het zetten (legloon). In kleine badkamers is de prijs per m² hoger.", ["trustoo_tegel", "homedeal_tegel"]),
    ("tegelwerk_incl", "Tegelwerk inclusief tegels", "per m²", "Legloon plus tegels.", ["trustoo_tegel", "werkspot_tegel"]),
    ("tegels", "Tegels (materiaal)", "per m²", "Ook de maat voor een eerlijke stelpost tegels.", ["werkspot_tegel"]),
    ("leidingwerk", "Leidingwerk", "per badkamer", "Op dezelfde plek aan de onderkant; aansluitingen verplaatsen aan de bovenkant.", ["trustoo_badkamer", "slimster_badkamer", "homedeal_toilet"]),
    ("elektra", "Elektra", "per badkamer", "Stopcontacten, schakelaars, een aparte groep en spots. Uitgebreide verlichting kan er nog bij komen.", ["trustoo_badkamer", "slimster_badkamer"]),
    ("vloerverwarming", "Vloerverwarming", "per badkamer", "Elektrisch of aangesloten op de cv.", ["slimster_badkamer", "trustoo_badkamer"]),
    ("sanitair", "Sanitair (levering)", "per badkamer", "Van een basisset tot luxe sanitair. Ook de maat voor een stelpost sanitair.", ["trustoo_badkamer", "homedeal_badkamer"]),
    ("kitwerk", "Kitwerk", "per meter", "Oude kit verwijderen en nieuwe aanbrengen.", ["werkspot_kit", "slimster_kit"]),
    ("uur", "Uurtarief vakman", "per uur, excl. btw", "Voor regiewerk en meerwerk.", ["homedeal_lood", "knab_lood"]),
]

_ren = DIENST_BY_SLUG["badkamer-renoveren"]

# Bronnen in volgorde van eerste gebruik, plus de Belastingdienst voor het btw-tarief.
BRONNEN = {}
for _r in RICHTPRIJS_RIJEN:
    for _k in _r[4]:
        BRONNEN.setdefault(_k, RP.BRONNEN[_k])
BRONNEN["btw"] = ("Belastingdienst, Diensten met 9% btw", "https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/tarieven_en_vrijstellingen/diensten_9_btw")
_BRON_NR = {k: i + 1 for i, k in enumerate(BRONNEN)}

PARSER_JS = (pathlib.Path(__file__).parent / "offerte_parser_badkamer.js").read_text(encoding="utf-8")

_MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
            "september", "oktober", "november", "december"]


def _peildatum():
    """'2026-11' -> 'november 2026'. Valt terug op november 2026 (de peildatum van richtprijzen.py)."""
    p = str(_PD.get("peildatum") or PRODUCTEN.get("peildatum") or "2026-11")
    try:
        jaar, maand = p.split("-")[:2]
        return f"{_MAANDEN[int(maand) - 1]} {jaar}"
    except Exception:
        return p


def _band_tekst(b):
    return f"{eur(b['van'])} – {eur(b['tot'])}"


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def _richtprijs_tabel():
    rijen = ""
    for sleutel, naam, eenheid, uitleg, bronnen in RICHTPRIJS_RIJEN:
        b = BANDEN[sleutel]
        noten = "".join(f'<sup><a href="#boc-bron-{_BRON_NR[k]}">{_BRON_NR[k]}</a></sup>' for k in bronnen)
        rijen += (f'<tr><td><strong>{naam}</strong><br><small>{uitleg}</small></td>'
                  f'<td class="num">{_band_tekst(b)}{noten}<br><small>{eenheid}</small></td></tr>')
    return f'<div class="tablewrap"><table class="boc-tabel"><thead><tr><th>Post</th><th>Richtprijs</th></tr></thead><tbody>{rijen}</tbody></table></div>'


def _product_bronnen():
    """Bronnen van de productbanden (prijsvergelijkers en overzichtspagina's) uit producten_badkamer."""
    bronnen = _PD.get("bronnen") or PRODUCTEN.get("bronnen") or {}
    items = []
    for _k, v in bronnen.items():
        try:
            oms, url = v[0], v[1]
        except Exception:
            continue
        if url and str(url).startswith("http"):
            items.append(f'<li><a href="{_esc(url)}" rel="noopener" target="_blank">{_esc(oms)}</a></li>')
        else:
            items.append(f'<li>{_esc(oms)}</li>')
    return items


def _product_dekking():
    """Korte zin over hoeveel artikelen en categorieën de productdata dekt (alleen als die er is)."""
    art = _PD.get("artikelen") or PRODUCTEN.get("artikelen") or []
    cat = _PD.get("categorieen") or PRODUCTEN.get("categorieen") or {}
    if not art and not cat:
        return ("De productdata wordt nog aangevuld. Tot die tijd vergelijken we producten met de "
                "richtprijs voor sanitair als geheel.")
    return (f"Op dit moment kennen we {len(art)} veelgebruikte artikelen en {len(cat)} productcategorieën. "
            "Herkennen we het artikel niet, dan vergelijken we met de band van de categorie, zoals "
            "‘thermostaatkraan’ of ‘hangtoilet’.")


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Offerte vergelijken", None)])
    data = {"banden": BANDEN, "producten": PRODUCTEN}
    peil = _peildatum()

    hero = f"""{cr}
<section class="section-sm tool-hero" data-boc>
<div class="wrap">
  <div class="boc-kop">
    <span class="badge">Gratis tool · je offerte blijft op je eigen toestel</span>
    <h1>Badkamerofferte vergelijken: check je offerte per regel</h1>
    <p class="lead">Upload je offerte als pdf of plak de tekst. Je ziet per regel wat het is (product, arbeid of materiaal), hoe de prijs zich verhoudt tot de markt, wat ontbreekt en wat te vaag is.</p>
  </div>
  <div class="formcard boc-kaart">
    <div class="boc-privacy" role="note">
      <strong>Je offerte wordt in je browser gelezen.</strong> Er gaat niets naar een server, tot je zelf kiest voor een tegenofferte.
    </div>
    <div class="boc-drop" tabindex="-1">
      <input type="file" id="boc-pdf" accept="application/pdf,.pdf" class="boc-bestand">
      <label for="boc-pdf" class="boc-drop-in">
        <span class="boc-drop-ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M12 18v-6"/><path d="m9 15 3-3 3 3"/></svg></span>
        <span><strong>Kies je offerte (pdf)</strong><br><span class="boc-drop-sub">of sleep het bestand hierheen</span></span>
      </label>
      <p class="boc-pdf-status" aria-live="polite" hidden></p>
    </div>
    <p class="boc-of"><span>of plak de tekst</span></p>
    <label for="boc-tekst" class="boc-label">Tekst van de offerte</label>
    <textarea id="boc-tekst" rows="10" spellcheck="false" placeholder="Open de offerte (pdf of e-mail), selecteer alles, kopieer en plak het hier.&#10;&#10;Bijvoorbeeld:&#10;Sloopwerk badkamer        € 850,00&#10;Thermostaatkraan Grohtherm 800 34558000   € 245,00&#10;Tegelwerk 30 m2 à € 45,00  € 1.350,00&#10;Totaal excl. btw ..."></textarea>
    <div class="boc-rij">
      <label for="boc-basis" class="boc-label-klein">De bedragen op de offerte zijn</label>
      <select id="boc-basis">
        <option value="">automatisch bepalen</option>
        <option value="excl">exclusief btw</option>
        <option value="incl">inclusief btw</option>
      </select>
    </div>
    <div class="boc-knoppen">
      <button type="button" class="btn btn-primary btn-lg boc-check">Vergelijk de offerte</button>
      <button type="button" class="btn btn-ghost boc-wis">Wissen</button>
    </div>
    <p class="boc-fout" hidden></p>
    <noscript><p class="callout">Zet JavaScript aan om de offertevergelijker te gebruiken. De check draait in je browser.</p></noscript>
  </div>

  <div class="boc-uitslag" aria-live="polite" hidden>
    <h2>Zo ziet je offerte eruit</h2>
    <div class="boc-totalen"></div>
    <div class="boc-meldingen"></div>
    <h3>Per regel</h3>
    <p class="boc-uitleg-vast"><strong>Goed om te weten:</strong> Webwinkelprijzen zijn geen installateursprijzen; een opslag op materiaal is normaal en dekt garantie, risico en levering. Een regel boven de band is daarom geen fout, maar een reden om te vragen wat erin zit.</p>
    <div class="boc-posten"></div>
    <p class="boc-klein">Productbanden zijn inclusief 21% btw, zonder montage (peildatum {peil}). We noemen een product pas ‘boven de band’ bij meer dan {DREMPEL_PRODUCT}% boven de bovenkant. Arbeid en materiaal vergelijken we met richtprijzen inclusief 21% btw (het uurtarief exclusief btw); daar tonen we ‘boven’ of ‘onder’ bij meer dan {DREMPEL_ARBEID}% buiten de band. <a href="#hoe-we-vergelijken">Hoe we vergelijken</a></p>
    <div class="boc-g2">
      <div class="boc-blok boc-b-goed"><h3>Waar de offerte goed geprijsd is</h3><ul class="boc-lijst boc-goed"></ul></div>
      <div class="boc-blok"><h3>Wat ontbreekt</h3><ul class="boc-lijst boc-mist"></ul></div>
      <div class="boc-blok"><h3>Wat te vaag is</h3><ul class="boc-lijst boc-vaag"></ul></div>
      <div class="boc-blok"><h3>Vragen voor je aanbieder</h3><ul class="boc-vragen"></ul>
        <button type="button" class="btn btn-ghost boc-kopieer">Kopieer vragen voor je aanbieder</button>
        <p class="boc-kopieer-ok boc-klein" aria-live="polite" hidden></p>
        <details class="boc-mail"><summary>Bekijk de mail</summary><textarea class="boc-mailtekst" rows="12" readonly aria-label="Mail met vragen voor je aanbieder"></textarea></details>
      </div>
    </div>
  </div>

  <aside class="boc-laag2" aria-labelledby="boc-l2-kop" hidden>
    <h2 id="boc-l2-kop">Wil je een tegenofferte? Gratis voor jou</h2>
    <p>Wij kunnen de posten uit je offerte, zonder je gegevens, voorleggen aan maximaal drie badkamerspecialisten uit je regio. Zij maken dan zelf een tegenofferte. Dat is gratis voor jou: wij krijgen een vergoeding van de specialist als je via ons een offerte aanvraagt. <a href="/hoe-verdienen-wij-geld/">Hoe verdienen wij geld?</a></p>
    <p class="boc-klein">De check hierboven ziet er hetzelfde uit, of je dit blok gebruikt of niet. Er gaat niets automatisch weg.</p>
    <div class="boc-knoppen">
      <button type="button" class="btn btn-ghost boc-l2-toon" aria-expanded="false" aria-controls="boc-l2-spec">Bekijk wat we zouden doorsturen</button>
    </div>
    <div id="boc-l2-spec" class="boc-l2-spec" hidden>
      <p>Dit is de specificatie zonder je naam, adres, telefoonnummer en e-mail, en zonder de naam van je huidige aanbieder. Kijk hem na: je kunt hem hier zelf aanpassen of inkorten (maximaal 3.000 tekens).</p>
      <label for="boc-l2-tekst" class="boc-label">Specificatie voor een tegenofferte</label>
      <textarea id="boc-l2-tekst" rows="12" maxlength="3000" spellcheck="false"></textarea>
      <p class="boc-klein boc-l2-teller"></p>
      <div class="boc-knoppen">
        <button type="button" class="btn btn-primary boc-l2-gebruik">Gebruik dit voor mijn aanvraag</button>
      </div>
      <p class="boc-klein">Je gaat naar het aanvraagformulier. Daar staat deze tekst in het veld ‘omschrijving’ en vul je zelf je contactgegevens in. Pas als je daar op verzenden drukt, gaat je aanvraag naar maximaal drie specialisten.</p>
    </div>
  </aside>
</div>
</section>"""

    prod_bronnen = _product_bronnen()
    prod_bronnen_html = (f'<details class="boc-bronlijst"><summary>Bronnen van de productbanden ({len(prod_bronnen)} prijsvergelijkers en overzichtspagina’s)</summary><ul class="boc-bronnen">{"".join(prod_bronnen)}</ul></details>'
                         if prod_bronnen else "")

    hoe = f"""<section class="section" id="hoe-we-vergelijken"><div class="wrap narrow prose">
  <h2>Hoe we vergelijken</h2>
  <p>De vergelijker leest je offerte regel voor regel en deelt elke regel in:</p>
  <ul>
    <li><strong>Product:</strong> een kraan, toilet, douchewand, wastafelmeubel of ander onderdeel. We zoeken naar het merk, de serie, het artikelnummer en de EAN-code. Vinden we het artikelnummer, dan vergelijken we met de prijsband van dat artikel. Anders gebruiken we de band van de serie of van de productcategorie.</li>
    <li><strong>Arbeid:</strong> sloopwerk, tegelwerk, leidingwerk, elektra, montage en uren. Die leggen we naast de richtprijzen in de tabel hieronder.</li>
    <li><strong>Materiaal:</strong> tegels, lijm, kit en ander materiaal, ook naast de richtprijzen.</li>
    <li><strong>Overig:</strong> regels die we niet kunnen indelen, zoals ‘diversen’. Die noemen we bij ‘wat te vaag is’.</li>
  </ul>
  <h3>Waar de marktbanden vandaan komen</h3>
  <p>Een productband is de laagste tot de hoogste prijs die we bij minstens drie aanbieders vonden, inclusief 21% btw en zonder montage. We halen die van openbare prijsvergelijkers en overzichtspagina’s. Peildatum: {peil}. {_product_dekking()}</p>
  {prod_bronnen_html}
  <p>Webwinkelprijzen zijn geen installateursprijzen. Een installateur rekent vaak een opslag op materiaal, en die dekt garantie, risico en levering. Daarom noemen we een product pas ‘boven de band’ als het meer dan {DREMPEL_PRODUCT}% boven de bovenkant ligt. Bij arbeid en materiaal is die drempel {DREMPEL_ARBEID}%, omdat de richtprijzen daar al ruim zijn.</p>
  <h3>Wat we niet doen</h3>
  <ul>
    <li>We zijn geen winkel en verkopen niets. Er staan geen winkellinks of aanbiedingen in de uitslag.</li>
    <li>We geven geen oordeel over je aanbieder. We zeggen alleen hoe een regel zich verhoudt tot de band, bijvoorbeeld ‘ligt 30% boven de marktband’.</li>
    <li>Niemand betaalt voor een plek of een gunstiger uitslag in de check.</li>
    <li>We lezen nog geen scans of foto’s. Is je pdf een scan, kopieer dan de tekst uit de e-mail of typ de belangrijkste regels over.</li>
  </ul>
</div></section>"""

    uitleg = f"""<section class="section soft" id="richtprijzen"><div class="wrap narrow prose">
  <h2>Met welke richtprijzen we arbeid en materiaal vergelijken</h2>
  <p>Dit zijn de bandbreedtes voor arbeid en materiaal. Ze komen van openbare prijsoverzichten en zijn bewust ruim, want geen badkamer is hetzelfde. De grootte, de staat van de vloer en muren, het sanitair dat je kiest en de regio maken veel uit. Een complete badkamer van 5 tot 9 m² kost volgens onze <a href="/kosten/nieuwe-badkamer/">kostenpagina</a> meestal {eur(_ren['prijs_van'])} tot {eur(_ren['prijs_tot'])}.</p>
  {_richtprijs_tabel()}
  <p><small>Prijspeil 2026, inclusief 21% btw tenzij anders vermeld. Meer over de prijzen per onderdeel: <a href="/kosten/badkamer-slopen/">badkamer slopen</a>, <a href="/kosten/tegelzetter-per-m2/">tegelzetter per m²</a>, <a href="/kosten/kitwerk-voegen/">kitwerk en voegen</a> en <a href="/kosten/uurtarief-loodgieter/">uurtarief loodgieter</a>.</small></p>

  <h2>Wat hoort er in een goede badkamerofferte?</h2>
  <p>Een goede offerte laat per onderdeel zien wat er gebeurt en wat het kost. Let vooral op deze punten:</p>
  <ul>
    <li><strong>Merk, serie en artikelnummer.</strong> ‘Thermostaatkraan’ zegt weinig; ‘Grohe Grohtherm 800, 34558000’ is te vergelijken. Lees ook <a href="/badkamerspullen/kranen-kiezen/">hoe je een kraan kiest</a>.</li>
    <li><strong>Waterdicht maken.</strong> Onder de tegels in de douchehoek en op de vloer hoort een waterdichte laag, met kimband in de hoeken. Lees <a href="/kennisbank/badkamer-waterdicht-maken/">hoe een badkamer waterdicht wordt gemaakt</a>.</li>
    <li><strong>Kitwerk.</strong> Kit langs het bad, de douche, de wastafel en in de hoeken. Slecht kitwerk geeft lekkage.</li>
    <li><strong>Afvoer van afval.</strong> Wie haalt het sloopafval weg, en zit de container in de prijs?</li>
    <li><strong>Stelposten met een eerlijk bedrag.</strong> Een stelpost is een voorlopig bedrag, bijvoorbeeld voor sanitair of tegels die je later kiest. Is dat bedrag laag, dan lijkt de offerte goedkoop en betaal je later bij.</li>
    <li><strong>Planning.</strong> Een startdatum en een doorlooptijd, liefst per fase. Zie ook de <a href="/tools/renovatieplanner/">renovatieplanner</a>.</li>
    <li><strong>Garantie.</strong> Hoe lang, en op wat: het werk, de waterdichting, het sanitair. Lees <a href="/kennisbank/garantie-badkamerrenovatie/">waar je op let bij garantie</a>.</li>
    <li><strong>Betaaltermijnen.</strong> Spreek af dat je het grootste deel betaalt na oplevering, niet vooraf.</li>
  </ul>
  <h3>Welk btw-tarief?</h3>
  <p>Op badkamerwerk, sanitair, tegelwerk en installatiewerk zit 21% btw. Het lage tarief van 9% geldt alleen voor bepaalde werkzaamheden aan een woning ouder dan twee jaar, zoals stukadoren en verven, en bij isoleren alleen voor het arbeidsloon (<a href="{BRONNEN['btw'][1]}" rel="noopener" target="_blank">Belastingdienst</a>). Staat er 9% op je hele offerte, vraag dan waarom.</p>

  <h3>Bronnen richtprijzen</h3>
  <ol class="boc-bronnen">{"".join(f'<li id="boc-bron-{_BRON_NR[k]}"><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for k, (t, u) in BRONNEN.items())}</ol>
</div></section>"""

    faqs = [
        ("Wordt mijn offerte ergens opgeslagen of verstuurd?",
         "Nee. De pdf of tekst wordt in je browser gelezen en vergeleken. Er gaat niets naar een server. Pas als je zelf kiest voor een tegenofferte en het aanvraagformulier verstuurt, gaan de posten (zonder je naam en adres) en je contactgegevens naar maximaal drie specialisten."),
        ("Mijn pdf wordt niet gelezen. Hoe kan dat?",
         "Waarschijnlijk is het een scan of foto van papier. Die bevat geen tekst, alleen een afbeelding, en die kan deze versie nog niet lezen. Kopieer de tekst uit de e-mail van je aanbieder, of typ de regels met een bedrag over in het tekstvak."),
        ("Waarom is een prijs boven de marktband niet meteen te duur?",
         "Webwinkelprijzen zijn geen installateursprijzen. Een installateur rekent vaak een opslag op materiaal, en die dekt garantie, risico en levering. Daarom tonen we ‘boven de band’ pas vanaf meer dan 25% boven de bovenkant. Ook dan is het een reden om te vragen wat erin zit, geen oordeel over je aanbieder."),
        ("Wat betekent ‘onvoldoende gespecificeerd’?",
         "Dat een regel te weinig zegt om hem te vergelijken. Bijvoorbeeld ‘sanitair compleet’ zonder merk en type, of ‘tegelwerk’ zonder aantal m². Vraag je aanbieder om merk, serie en artikelnummer, of om het aantal en de prijs per eenheid."),
        ("Wat kost een tegenofferte?",
         "Niets. Wij krijgen een vaste vergoeding van de specialist als je via ons een offerte aanvraagt. Je zit nergens aan vast. Lees meer op de pagina over hoe wij geld verdienen."),
        ("Welk btw-tarief hoort op een badkamerofferte?",
         "21%, op het werk en op de materialen. Alleen bepaalde onderdelen, zoals stukadoren of verven in een woning ouder dan twee jaar, mogen onder 9% vallen."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over offertes vergelijken")

    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Badkamerofferte vergelijken",
        "url": None,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsers",
        "inLanguage": "nl-NL",
        "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Upload of plak een badkamerofferte en zie per regel hoe producten, arbeid en materiaal zich verhouden tot marktbanden en richtprijzen. Draait in de browser.",
    }
    del app_ld["url"]

    data_tag = ('<script type="application/json" id="boc-data">'
                + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    parser_tag = "<script>\n" + PARSER_JS.replace("</script", "<\\/script") + "\n</script>"

    body = (hero + hoe + uitleg + faq_html
            + cta_blok("Nog maar één offerte?", "Vergelijken werkt het best met twee of drie offertes. Vraag ze gratis en vrijblijvend aan bij maximaal drie badkamerspecialisten uit je regio.", "Vraag offertes aan")
            + PAGE_CSS + data_tag + parser_tag + PAGE_JS)

    write(PAD, page(
        title("Badkamerofferte vergelijken: check je offerte per regel"),
        "Upload of plak je badkamerofferte en zie per regel hoe product, arbeid en materiaal zich verhouden tot de markt. Gratis, en je offerte blijft in je browser.",
        PAD, body, [cr_ld, faq_ld, app_ld]), prio=0.7)


# ---------------------------------------------------------------------------
# CSS (alleen deze pagina)
# ---------------------------------------------------------------------------

PAGE_CSS = """<style>
[data-boc] [hidden]{display:none!important}
.boc-kop{max-width:760px;margin:0 auto 18px;text-align:center}
.boc-kaart{max-width:820px;margin:0 auto;border-top:4px solid var(--accent)}
.boc-privacy{background:var(--bg-soft);border-left:4px solid var(--green);border-radius:10px;padding:12px 14px;font-size:.94rem;margin:0 0 16px}
.boc-drop{position:relative;border:2px dashed var(--line);border-radius:12px;background:#fff;transition:border-color .15s,background .15s}
.boc-drop.is-over{border-color:var(--accent);background:var(--accent-soft)}
.boc-bestand{position:absolute;width:1px;height:1px;opacity:0;overflow:hidden}
.boc-drop-in{display:flex;gap:14px;align-items:center;justify-content:center;padding:20px 16px;cursor:pointer;text-align:left;color:var(--ink)}
.boc-bestand:focus-visible+.boc-drop-in{outline:3px solid var(--accent-soft);outline-offset:2px;border-radius:10px}
.boc-drop-ico{color:var(--accent);flex:none}
.boc-drop-sub{font-size:.9rem;color:var(--muted)}
.boc-pdf-status{margin:0;padding:0 16px 14px;font-size:.92rem;text-align:center}
.boc-pdf-status.is-fout{color:#8f2a1b}
.boc-of{display:flex;align-items:center;gap:10px;color:var(--muted);font-size:.88rem;margin:16px 0 10px}
.boc-of::before,.boc-of::after{content:"";flex:1;height:1px;background:var(--line)}
.boc-label{display:block;font-weight:700;color:var(--ink);margin:0 0 6px}
.boc-label-klein{font-size:.92rem;color:var(--muted);margin:0}
#boc-tekst,#boc-l2-tekst,.boc-mailtekst{display:block;width:100%;box-sizing:border-box;font:14px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;padding:12px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);resize:vertical}
#boc-tekst{min-height:200px}
#boc-tekst:focus,#boc-basis:focus,#boc-l2-tekst:focus{outline:3px solid var(--accent-soft);border-color:var(--accent)}
.boc-rij{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin:12px 0 0}
#boc-basis{font:inherit;padding:8px 10px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);max-width:100%}
.boc-knoppen{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 0}
.boc-fout{color:#a3361a;font-weight:600;margin:12px 0 0}
.boc-uitslag{max-width:980px;margin:32px auto 0}
.boc-uitslag h2{text-align:center}
.boc-uitslag h3{font-size:1.08rem;margin:22px 0 10px}
.boc-totalen{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.boc-tot{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px}
.boc-tot span{display:block;font-size:.84rem;color:var(--muted)}
.boc-tot b{font-size:1.2rem;color:var(--ink)}
.boc-melding{border-radius:10px;padding:10px 14px;margin:10px 0 0;font-size:.95rem}
.boc-m-ok{background:#e7f5ef;color:#0b5e41}.boc-m-let{background:#fff6e0;color:#6b4d00}.boc-m-fout{background:#fdecea;color:#8f2a1b}
.boc-uitleg-vast{background:var(--bg-soft);border-radius:10px;padding:10px 14px;font-size:.93rem;margin:0 0 12px}
.boc-post{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:6px 14px;background:#fff;border:1px solid var(--line);border-left:5px solid var(--line);border-radius:var(--radius);padding:12px 14px;margin:0 0 8px}
.boc-post.o-binnen,.boc-post.o-onder-p{border-left-color:var(--green)}.boc-post.o-hoog,.boc-post.o-boven{border-left-color:#c0392b}.boc-post.o-laag{border-left-color:#e2a80c}
.boc-post.o-uit{opacity:.7}
.boc-soort{font-weight:700;color:var(--ink)}
.boc-oms{font-size:.9rem;color:var(--muted);overflow-wrap:anywhere}
.boc-herkend{font-size:.88rem;color:var(--body);margin-top:2px;overflow-wrap:anywhere}
.boc-bedrag{text-align:right;font-weight:700;color:var(--ink);white-space:nowrap}
.boc-bedrag small{display:block;font-weight:400;font-size:.78rem;color:var(--muted)}
.boc-oordeel{grid-column:1/-1;font-size:.9rem;border-top:1px dashed var(--line);padding-top:6px}
.boc-oordeel dl{display:grid;grid-template-columns:auto minmax(0,1fr);gap:2px 10px;margin:4px 0 0}
.boc-oordeel dt{color:var(--muted)}
.boc-oordeel dd{margin:0;overflow-wrap:anywhere}
.boc-tag{display:inline-block;font-size:.76rem;font-weight:700;border-radius:99px;padding:2px 9px;margin:0 6px 2px 0;vertical-align:1px}
.boc-s-product{background:#e8f0fb;color:#1f4f8f}.boc-s-arbeid{background:#efe9f8;color:#4d2f80}.boc-s-materiaal{background:#eef4e6;color:#3f5e1b}.boc-s-overig{background:var(--bg-soft);color:var(--muted)}
.boc-t-binnen{background:#e7f5ef;color:#0b5e41}.boc-t-hoog,.boc-t-boven{background:#fdecea;color:#8f2a1b}.boc-t-laag{background:#fff6e0;color:#6b4d00}.boc-t-onder{background:#e7f5ef;color:#0b5e41}.boc-t-geen,.boc-t-onbekend{background:var(--bg-soft);color:var(--muted)}
.boc-vraag{display:block;margin-top:4px;color:var(--body)}
.boc-klein{font-size:.85rem;color:var(--muted);margin:10px 0 0}
.boc-g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:16px}
@media(max-width:760px){.boc-g2{grid-template-columns:minmax(0,1fr)}}
.boc-blok{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;min-width:0}
.boc-blok h3{margin-top:0}
.boc-lijst,.boc-vragen{margin:0;padding:0;list-style:none}
.boc-lijst li,.boc-vragen li{margin:0 0 10px;padding-left:28px;position:relative;font-size:.95rem;overflow-wrap:anywhere}
.boc-lijst li::before{position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font-size:.75rem;font-weight:800;color:#fff}
.boc-lijst li.s-ok::before{content:"\\2713";background:var(--green)}
.boc-lijst li.s-mist::before{content:"!";background:#c0392b}
.boc-lijst li.s-let::before{content:"?";background:#e2a80c}
.boc-lijst li.s-neutraal::before{content:"\\2013";background:#8aa0a5}
.boc-vragen li::before{content:"\\203A";position:absolute;left:8px;top:-2px;font-weight:800;color:var(--accent);font-size:1.2rem}
.boc-kopieer{margin-top:6px}
.boc-mail{margin-top:10px;font-size:.92rem}
.boc-mail summary{cursor:pointer;color:var(--accent);font-weight:600}
.boc-mailtekst{margin-top:8px;font-size:13px}
.boc-laag2{max-width:980px;margin:36px auto 0;background:#fffaf0;border:2px solid #e9c46a;border-radius:var(--radius);padding:20px 22px}
.boc-laag2 h2{margin-top:0;font-size:1.3rem}
.boc-laag2 p{margin:8px 0 0}
.boc-l2-spec{margin-top:14px}
.boc-tabel td{vertical-align:top}
.boc-tabel td small{color:var(--muted)}
.boc-tabel sup a{text-decoration:none;margin-left:2px}
.boc-bronnen{font-size:.88rem}
.boc-bronlijst{margin:12px 0}.boc-bronlijst summary{cursor:pointer;font-weight:600;color:var(--accent)}
.boc-bronnen li{margin:4px 0;overflow-wrap:anywhere}
@media(max-width:480px){.boc-kaart{padding:18px 14px}.boc-knoppen .btn{flex:1 1 100%}.boc-laag2{padding:16px 14px}.boc-post{grid-template-columns:minmax(0,1fr)}.boc-bedrag{text-align:left}}
</style>"""


# ---------------------------------------------------------------------------
# JavaScript (alleen deze pagina, draait volledig in de browser)
# ---------------------------------------------------------------------------

PAGE_JS = r"""<script>
(function () {
  "use strict";
  var root = document.querySelector("[data-boc]");
  if (!root || !window.TBOfferte) return;
  var P = window.TBOfferte;
  var DATA = JSON.parse(document.getElementById("boc-data").textContent);
  var B = DATA.banden;
  var PD = DATA.producten && DATA.producten.categorieen ? DATA.producten : null;
  var veld = root.querySelector("#boc-tekst"), basisKeuze = root.querySelector("#boc-basis");
  var uitslag = root.querySelector(".boc-uitslag"), fout = root.querySelector(".boc-fout");
  var laag2 = root.querySelector(".boc-laag2");
  var laatste = null;

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var euro = P.euro;
  var EENH = { m2: "m²", m: "meter", uur: "uur", post: "post" };
  var SOORT_NAAM = { product: "Product", arbeid: "Arbeid", materiaal: "Materiaal", overig: "Overig" };

  function tot(label, waarde, noot) {
    return '<div class="boc-tot"><span>' + label + "</span><b>" + (waarde == null ? "–" : euro(waarde)) + "</b>" + (noot ? '<span>' + noot + "</span>" : "") + "</div>";
  }
  function melding(soort, tekst) { return '<p class="boc-melding boc-m-' + soort + '">' + tekst + "</p>"; }

  /* ---------------------------------------------------- indeling per regel */
  // Terugval als de parser (nog) geen soort geeft.
  var SOORT_TYPE = { tegels: "materiaal", sanitair: "product", korting: "overig", overig: "overig" };
  function soortVan(p) {
    if (p.soort) return p.soort;
    if (P.soortRegel) return P.soortRegel(p.omschrijving || "", PD || undefined);
    return SOORT_TYPE[p.type] || "arbeid";
  }
  function productOordeel(p, r) {
    if (!p.product || !PD) return p.productOordeel || null;
    // Koos de bezoeker een andere btw-basis, reken dan opnieuw.
    if (P.beoordeelProduct && (!p.productOordeel || p._basis !== r.basis)) {
      try { p.productOordeel = P.beoordeelProduct(p, p.product, PD, r.basis); p._basis = r.basis; } catch (e) {}
    }
    return p.productOordeel || null;
  }
  function catNaam(k) { return PD && PD.categorieen && PD.categorieen[k] ? PD.categorieen[k].naam : (k || ""); }
  function bronNaam(k) {
    var b = PD && PD.bronnen && PD.bronnen[k];
    if (!b) return "";
    return Array.isArray(b) ? b[0] : (b.naam || b.oms || "");
  }
  // po.bron kan een sleutel of een lijst sleutels zijn; po.bronnen een lijst {oms, url}.
  function bronnenTekst(po) {
    if (po.bronnen && po.bronnen.length) return po.bronnen.map(function (b) { return b.oms; }).join("; ");
    var k = po.bron;
    if (!k) return "";
    return (Array.isArray(k) ? k : [k]).map(bronNaam).filter(Boolean).join("; ");
  }
  function pct(n) { return Math.round(Math.abs(n)) + "%"; }
  var CODE_RE = /\b\d[\d.\-]{5,}\d\b/;
  function merkGenoemd(t) {
    if (!PD || !PD.merken) return false;
    var l = " " + t.toLowerCase() + " ";
    return PD.merken.some(function (m) { return [m.naam].concat(m.aliassen || []).some(function (a) { return a && l.indexOf(String(a).toLowerCase()) >= 0; }); });
  }
  var VAAG_RE = /\b(divers(en|e)?|klein\s*materiaal|bijkomende?\s+kosten|overige?\s+(kosten|werkzaamheden)|aanneemsom|totaalprijs|compleet|complete|pakket|all[\s-]?in)\b/i;

  // Beoordeelt één regel. Geeft {soort, html, goed, vaag, vraag}.
  function regel(p, r) {
    var soort = soortVan(p);
    var bedrag = p.bedrag != null ? euro(p.bedrag) : (p.eenheidsprijs != null ? euro(p.eenheidsprijs) + (p.eenheid ? " per " + (P.EENHEDEN[p.eenheid] || p.eenheid) : "") : "–");
    var detail = "";
    if (p.aantal && p.eenheid) detail = p.aantal.toLocaleString("nl-NL") + " " + (P.EENHEDEN[p.eenheid] || p.eenheid) + (p.eenheidsprijs ? " à " + euro(p.eenheidsprijs) : "");
    var tags = [];
    if (p.stelpost) tags.push("stelpost");
    if (p.optie) tags.push("optie, telt niet mee");
    else if (p.naTotaal) tags.push("staat na het totaal, telt niet mee");
    var oms = p.omschrijving || "";
    var kort = oms.length > 60 ? oms.slice(0, 57) + "…" : oms;
    var uit = { soort: soort, goed: null, vaag: null, vraag: null, klasse: "geen" };
    var herkend = "", oordeel = "";

    var h = soort === "product" ? p.product : null;
    var po = soort === "product" ? productOordeel(p, r) : null;
    if (h) {
      var delen = [];
      if (h.merk) delen.push(h.merk);
      if (h.serie) delen.push(h.serie);
      if (h.code) delen.push("art.nr. " + h.code);
      if (h.ean) delen.push("EAN " + h.ean);
      var hoe = { exact: "artikel herkend", serie: "serie herkend", categorie: (h.merk || h.code) ? "artikel niet in onze lijst, vergeleken met de categorie" : "alleen soort product herkend" }[h.match] || "herkend";
      herkend = '<div class="boc-herkend"><strong>' + esc(hoe) + ":</strong> " + esc(delen.join(" · ") || catNaam(h.categorie)) + (h.categorie && delen.length ? " (" + esc(catNaam(h.categorie)) + ")" : "") + "</div>";
    }

    if (po && po.band && po.oordeel && po.oordeel !== "onbekend") {
      var bandSoort = po.band.soort === "artikel" ? (h && h.match === "serie" ? "marktband van deze serie" : "marktband van dit artikel") : "marktband " + (h && h.categorie ? catNaam(h.categorie).toLowerCase() : "categorie");
      var woord = { binnen: "binnen de marktband", boven: "boven de marktband", onder: "onder de marktband" }[po.oordeel] || po.oordeel;
      var verschil = "";
      if (po.verschilPct != null && po.oordeel === "boven") verschil = pct(po.verschilPct) + " boven de bovenkant";
      else if (po.verschilPct != null && po.oordeel === "onder") verschil = pct(po.verschilPct) + " onder de onderkant";
      else if (po.oordeel === "binnen") verschil = "valt binnen de band";
      uit.klasse = po.oordeel === "onder" ? "onder-p" : po.oordeel;
      oordeel = '<span class="boc-tag boc-t-' + esc(po.oordeel) + '">' + esc(woord) + "</span>" +
        "<dl><dt>Band</dt><dd>" + euro(po.band.van) + " – " + euro(po.band.tot) + " incl. btw (" + esc(bandSoort) + ")</dd>" +
        (verschil ? "<dt>Verschil</dt><dd>" + esc(verschil) + "</dd>" : "") +
        (po.toelichting ? "<dt>Toelichting</dt><dd>" + esc(po.toelichting) + "</dd>" : "") +
        (bronnenTekst(po) ? "<dt>Bron</dt><dd>" + esc(bronnenTekst(po)) + "</dd>" : "") + "</dl>";
      if (po.oordeel === "binnen") uit.goed = kort + ": binnen de " + bandSoort + (po.band.soort === "artikel" ? "." : " (grove vergelijking, het precieze type is niet bekend).");
      if (po.oordeel === "onder") uit.goed = kort + ": onder de " + bandSoort + ". Controleer wel of het hetzelfde type en dezelfde maat is.";
      if (po.oordeel === "boven") uit.vraag = "‘" + kort + "’ (" + bedrag + "): kun je toelichten wat deze prijs omvat, zoals levering, garantie en montage? De " + bandSoort + " is " + euro(po.band.van) + " – " + euro(po.band.tot) + " incl. btw.";
      if (h && h.match === "categorie" && !h.merk && !h.code && !CODE_RE.test(oms)) { uit.vaag = kort + ": we herkennen alleen de soort product. Vraag om merk, serie en artikelnummer, dan is het precies te vergelijken."; uit.vaagVraag = "‘" + kort + "’: welk merk, welke serie en welk artikelnummer is gerekend?"; }
    } else if (soort === "product") {
      var reden = po && po.toelichting ? po.toelichting : (PD ? "geen marktband voor deze regel" : "productvergelijking nog niet beschikbaar");
      oordeel = '<span class="boc-tag boc-t-onbekend">' + esc(reden) + "</span>";
      // Eén product naast de sanitair-richtprijs voor een hele badkamer leggen zegt niets; dat doen we dus niet.
      if (h ? (h.match === "categorie" || !h.merk) : !(merkGenoemd(oms) || CODE_RE.test(oms))) { uit.vaag = kort + ": onvoldoende gespecificeerd. Vraag om merk, serie en artikelnummer."; uit.vaagVraag = "‘" + kort + "’: welk merk, welke serie en welk artikelnummer is gerekend?"; }
    } else {
      var b = P.beoordeelPost(p, B, r.basis, (r.btwTarieven || [])[0]);
      if (b.oordeel) {
        oordeel = richtprijsTekst(b);
        uit.klasse = b.oordeel;
        if (b.oordeel === "binnen") uit.goed = kort + ": binnen de richtprijs.";
        if (b.oordeel === "hoog") uit.vraag = "‘" + kort + "’ (" + bedrag + "): kun je toelichten wat er in deze post zit?";
        if (b.oordeel === "laag") uit.vraag = "‘" + kort + "’ (" + bedrag + "): zit hier alles in, of kan er later nog iets bij komen?";
      } else {
        var rd = { "geen richtprijs": "geen richtprijs voor deze regel", "geen aantal": "geen aantal gevonden, dus niet te vergelijken", "andere eenheid": "andere eenheid dan de richtprijs", "geen bedrag": "geen bedrag gevonden", korting: "korting" }[b.reden] || b.reden;
        oordeel = '<span class="boc-tag boc-t-geen">' + esc(rd) + "</span>";
        if (b.reden === "geen aantal") { uit.vaag = kort + ": er staat geen aantal bij (m², meter of uren). Vraag om het aantal en de prijs per eenheid."; uit.vaagVraag = "‘" + kort + "’: om hoeveel m², meter of uren gaat het, en wat is de prijs per eenheid?"; }
      }
      if (!uit.vraag && b.vragen[0] && p.meetellen && p.type !== "korting") uit.vraagZacht = "‘" + kort + "’: " + b.vragen[0];
    }
    if (!uit.vaag && p.vaag) { uit.vaag = kort + ": " + String(p.vaagTekst || "onvoldoende gespecificeerd").replace(/:\s*vraag/, ". Vraag").replace(/\.?$/, "."); uit.vaagVraag = "‘" + kort + "’ (" + bedrag + "): welke producten zitten hierin, met merk, serie en artikelnummer?"; }
    if (!uit.vaag && VAAG_RE.test(oms) && p.bedrag != null) { uit.vaag = kort + ": deze regel zegt niet precies wat erin zit. Vraag om een uitsplitsing."; uit.vaagVraag = "‘" + kort + "’ (" + bedrag + "): wat zit er precies in deze regel?"; }
    if (!uit.vaag && p.bedrag == null && !p.alleenTarief && p.type !== "korting") { uit.vaag = kort + ": er staat geen bedrag bij."; uit.vaagVraag = "‘" + kort + "’: wat kost dit onderdeel?"; }

    uit.html = '<div class="boc-post o-' + uit.klasse + (p.meetellen ? "" : " o-uit") + '">' +
      '<div><div class="boc-soort"><span class="boc-tag boc-s-' + esc(soort) + '">' + esc(SOORT_NAAM[soort] || soort) + "</span>" +
      (p.type && p.type !== "overig" && soort !== "product" ? esc((P.TYPES[p.type] || P.TYPES.overig).naam) : "") +
      (tags.length ? ' <span class="boc-tag boc-t-geen">' + esc(tags.join(", ")) + "</span>" : "") + "</div>" +
      '<div class="boc-oms">' + esc(oms) + (detail ? " · " + esc(detail) : "") + "</div>" + herkend + "</div>" +
      '<div class="boc-bedrag">' + bedrag + "<small>op de offerte, " + (r.basis === "incl" ? "incl." : "excl.") + " btw</small></div>" +
      '<div class="boc-oordeel">' + oordeel + "</div></div>";
    return uit;
  }

  function richtprijsTekst(b) {
    var band = euro(b.van) + " – " + euro(b.tot) + (b.perEenheid ? " per " + EENH[b.perEenheid] : "") + (b.inclBtw ? " incl. btw" : " excl. btw");
    var vgl = euro(b.vergelijk) + (b.perEenheid ? " per " + EENH[b.perEenheid] : "") + (b.inclBtw ? " incl. btw" : " excl. btw");
    var woord = { binnen: "binnen de richtprijs", hoog: "boven de richtprijs", laag: "onder de richtprijs" }[b.oordeel];
    var verschil = "";
    if (b.oordeel === "hoog") verschil = pct((b.vergelijk / b.tot - 1) * 100) + " boven de bovenkant";
    if (b.oordeel === "laag") verschil = pct((1 - b.vergelijk / b.van) * 100) + " onder de onderkant";
    return '<span class="boc-tag boc-t-' + b.oordeel + '">' + woord + "</span>" +
      "<dl><dt>Richtprijs</dt><dd>" + band + "</dd><dt>Deze regel</dt><dd>" + vgl + (verschil ? " (" + verschil + ")" : "") + "</dd>" +
      (b.vragen[0] ? "<dt>Toelichting</dt><dd>" + esc(b.vragen[0]) + "</dd>" : "") + "</dl>";
  }

  /* ---------------------------------------------------- mailsjabloon */
  // Wat ontbreekt, als vraag aan de aanbieder.
  var MIST_VRAAG = {
    waterdicht: "Hoe worden de douchehoek en de vloer waterdicht gemaakt (kimband, folie of coating)?",
    kitwerk: "Zit het kitwerk langs bad, douche en wastafel in de prijs?",
    afval: "Wie voert het sloopafval af, en zit dat in de prijs?",
    stelposten: "Wat gebeurt er als een stelpost hoger of lager uitvalt?",
    planning: "Wat zijn de startdatum en de doorlooptijd?",
    garantie: "Hoe lang is de garantie, en geldt die op het werk én op het materiaal?",
    betaling: "Wanneer betaal ik welk deel? Ik betaal het grootste deel graag na oplevering."
  };
  function mailTekst(vragen) {
    return "Beste,\n\nBedankt voor de offerte voor mijn badkamer. Voordat ik een keuze maak, heb ik nog een paar vragen:\n\n" +
      vragen.map(function (v, i) { return (i + 1) + ". " + v; }).join("\n") +
      "\n\nKun je de offerte waar nodig aanvullen met merk, serie en artikelnummer van de producten, en het aantal en de prijs per eenheid bij het werk?\n\nAlvast bedankt.\n\nMet vriendelijke groet,\n";
  }
  function kopieer(tekst, klaar) {
    function terug() {
      var t = document.createElement("textarea");
      t.value = tekst; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
      document.body.appendChild(t); t.select();
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(t); klaar(ok);
    }
    if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(tekst).then(function () { klaar(true); }, terug);
    else terug();
  }

  /* ---------------------------------------------------- anonieme specificatie (laag 2) */
  var NAW_RE = /@|https?:\/\/|www\.|\b\d{4}\s?[a-z]{2}\b|(\+31|0031|\b0)[\s-]?\d[\d\s-]{7,}|\bNL\d{2}[A-Z]{4}\d{6,}|\bkvk\b|\bbtw[\s-]?(nr|nummer|id)|t\.a\.v\.|geachte|offertenummer|offerte\s*nr|klantnummer|\biban\b/i;
  function specificatie(r) {
    if (P.anoniemeSpecificatie) { try { return P.anoniemeSpecificatie(r); } catch (e) {} }
    // Terugval: alleen de posten en de totalen, regels met NAW-kenmerken eruit.
    var regels = ["Specificatie badkamerofferte (zonder namen en adressen)", ""];
    r.posten.forEach(function (p) {
      if (NAW_RE.test(p.omschrijving || "")) return;
      var a = p.aantal && p.eenheid ? " – " + p.aantal.toLocaleString("nl-NL") + " " + (P.EENHEDEN[p.eenheid] || p.eenheid) : "";
      regels.push("- " + p.omschrijving + a + (p.bedrag != null ? ": " + euro(p.bedrag) : "") + (p.stelpost ? " (stelpost)" : "") + (p.optie ? " (optie)" : ""));
    });
    var t = r.totaal || {};
    regels.push("");
    if (t.excl != null) regels.push("Totaal excl. btw: " + euro(t.excl));
    if (t.incl != null) regels.push("Totaal incl. btw: " + euro(t.incl));
    return regels.join("\n");
  }

  /* ---------------------------------------------------- de check */
  function check() {
    var tekst = veld.value;
    fout.hidden = true;
    if (!/\d/.test(tekst) || tekst.trim().length < 20) {
      fout.textContent = "Upload eerst je offerte of plak de tekst, met de bedragen erbij.";
      fout.hidden = false; uitslag.hidden = true; laag2.hidden = true; return;
    }
    var r = null;
    // Valt de productherkenning om wat voor reden ook om, lees dan zonder productniveau.
    if (PD) { try { r = P.leesOfferte(tekst, { producten: PD }); } catch (e) { r = null; } }
    if (!r) r = P.leesOfferte(tekst);
    var keuze = basisKeuze.value, orig = r.basis;
    r.posten.forEach(function (p) { if (p.productOordeel) p._basis = orig; });
    if (keuze && keuze !== r.basis) {
      r.basis = keuze;
      r.controle = P.controle(r.somPosten, keuze, r.totaal, r.subtotaal, 0);
    }
    laatste = r;
    var basisTekst = r.basis === "incl" ? "inclusief btw" : "exclusief btw";

    var t = r.totaal, html = "";
    html += tot("Totaal excl. btw", t.excl, t.bron.excl === "berekend" ? "berekend" : t.bron.excl === "posten" ? "som van de posten" : "");
    html += tot("Btw" + (r.btwTarieven.length ? " (" + r.btwTarieven.join("% en ") + "%)" : ""), t.btw);
    html += tot("Totaal incl. btw", t.incl, t.bron.incl === "berekend" ? "berekend" : t.bron.incl === "posten" ? "som van de posten" : "");
    if (r.uurloon) {
      var ub = P.beoordeelPost({ type: "uren", alleenTarief: true, eenheidsprijs: r.uurloon, eenheid: "uur", omschrijving: "" }, B, r.basis, 21);
      html += tot("Uurtarief", r.uurloon, ub.oordeel ? { binnen: "binnen", hoog: "boven", laag: "onder" }[ub.oordeel] + " de richtprijs van " + euro(B.uur.van) + " – " + euro(B.uur.tot) + " excl. btw" : "");
    }
    root.querySelector(".boc-totalen").innerHTML = html;

    var m = "";
    if (!r.posten.length) m += melding("let", "We vonden geen losse regels met een bedrag. Staat er alleen een totaalprijs op de offerte? Vraag dan om een uitsplitsing per onderdeel." + (t.twijfel ? " We zagen wel een totaal van " + euro(t.twijfel) + ", maar niet of dat inclusief of exclusief btw is." : ""));
    else if (r.controle.klopt === true) m += melding("ok", "De regels tellen op tot het totaal (" + euro(r.controle.tegen) + " " + basisTekst + ").");
    else if (r.controle.klopt === false) m += melding("fout", "De regels tellen op tot " + euro(r.controle.som) + ", maar het totaal is " + euro(r.controle.tegen) + ". Verschil: " + euro(r.controle.verschil) + ". Controleer of we een regel gemist hebben, of vraag waar het verschil zit.");
    m += melding("let", "We lezen de bedragen als " + basisTekst + ". Klopt dat niet? Kies het hierboven en vergelijk opnieuw.");
    (r.meldingen || []).forEach(function (x) { m += melding("let", esc(x)); });
    root.querySelector(".boc-meldingen").innerHTML = m;

    var regels = r.posten.map(function (p) { return regel(p, r); });
    root.querySelector(".boc-posten").innerHTML = regels.map(function (x) { return x.html; }).join("") || '<p class="boc-klein">Geen regels gevonden.</p>';

    // Goed geprijsd
    var goed = regels.filter(function (x) { return x.goed; }).map(function (x) { return x.goed; });
    root.querySelector(".boc-goed").innerHTML = goed.length
      ? goed.slice(0, 10).map(function (g) { return '<li class="s-ok">' + esc(g) + "</li>"; }).join("")
      : '<li class="s-neutraal">We vonden geen regels die we binnen een band konden plaatsen.</li>';

    // Wat ontbreekt
    var lijst = P.checklist(r, B);
    var mist = lijst.filter(function (c) { return c.status === "mist" || c.status === "let"; });
    var okLijst = lijst.filter(function (c) { return c.status === "ok"; });
    root.querySelector(".boc-mist").innerHTML = (mist.length ? mist : []).map(function (c) {
      return '<li class="s-' + c.status + '"><strong>' + esc(c.titel) + ".</strong> " + esc(c.uitleg) + "</li>";
    }).join("") + (okLijst.length ? '<li class="s-ok"><strong>Wel genoemd:</strong> ' + esc(okLijst.map(function (c) { return c.titel.toLowerCase(); }).join(", ")) + ".</li>" : "");

    // Te vaag
    var vaag = regels.filter(function (x) { return x.vaag; }).map(function (x) { return x.vaag; });
    root.querySelector(".boc-vaag").innerHTML = vaag.length
      ? vaag.slice(0, 10).map(function (v) { return '<li class="s-let">' + esc(v) + "</li>"; }).join("")
      : '<li class="s-ok">Geen regels die we te vaag vonden.</li>';

    // Vragen + mail
    var vragen = P.algemeneVragen(r).slice();
    regels.forEach(function (x) { if (x.vraag) vragen.push(x.vraag); });
    regels.forEach(function (x) { if (x.vaagVraag) vragen.push(x.vaagVraag); });
    regels.forEach(function (x) { if (x.vraagZacht && vragen.length < 8) vragen.push(x.vraagZacht); });
    mist.forEach(function (c) { if (c.status === "mist" && MIST_VRAAG[c.sleutel]) vragen.push(MIST_VRAAG[c.sleutel]); });
    vragen = vragen.filter(function (v, i) { return vragen.indexOf(v) === i; }).slice(0, 14);
    root.querySelector(".boc-vragen").innerHTML = vragen.map(function (v) { return "<li>" + esc(v) + "</li>"; }).join("") || "<li>Geen extra vragen gevonden. Loop de offerte toch nog even zelf na.</li>";
    root.querySelector(".boc-mailtekst").value = mailTekst(vragen.length ? vragen : ["Kun je per onderdeel aangeven wat er in de prijs zit?"]);
    root.querySelector(".boc-kopieer-ok").hidden = true;

    // Laag 2 klaarzetten (dicht), maar nog niets tonen of opslaan.
    laag2.hidden = !r.posten.length;
    var spec = root.querySelector("#boc-l2-spec");
    spec.hidden = true;
    root.querySelector(".boc-l2-toon").setAttribute("aria-expanded", "false");
    root.querySelector("#boc-l2-tekst").value = "";

    uitslag.hidden = false;
    var top = uitslag.getBoundingClientRect().top + window.scrollY - 80;
    window.scrollTo({ top: top, behavior: "smooth" });
  }

  /* ---------------------------------------------------- pdf lezen (lokaal, pdf.js) */
  var pdfjs = null;
  function laadPdfjs() {
    if (pdfjs) return pdfjs;
    pdfjs = new Promise(function (ok, nee) {
      if (window.pdfjsLib) { window.pdfjsLib.GlobalWorkerOptions.workerSrc = "/assets/vendor/pdfjs/pdf.worker.min.js"; ok(window.pdfjsLib); return; }
      var s = document.createElement("script");
      s.src = "/assets/vendor/pdfjs/pdf.min.js";
      s.onload = function () {
        if (!window.pdfjsLib) { nee(new Error("geen pdfjsLib")); return; }
        window.pdfjsLib.GlobalWorkerOptions.workerSrc = "/assets/vendor/pdfjs/pdf.worker.min.js";
        ok(window.pdfjsLib);
      };
      s.onerror = function () { pdfjs = null; nee(new Error("laden mislukt")); };
      document.head.appendChild(s);
    });
    return pdfjs;
  }
  // Zet de losse tekststukjes van een pdf-pagina terug in regels (op hoogte, dan van links naar rechts).
  function regelsUitItems(items) {
    if (P.regelsUitItems) return P.regelsUitItems(items);
    var lijst = items.filter(function (it) { return it.str && it.str.trim(); }).map(function (it) {
      var h = Math.abs(it.height || it.transform[3] || 10);
      return { s: it.str, x: it.transform[4], y: it.transform[5], w: it.width || 0, h: h };
    }).sort(function (a, b) { return b.y - a.y || a.x - b.x; });
    var rg = [];
    lijst.forEach(function (it) {
      var r = rg.length && rg[rg.length - 1];
      if (r && Math.abs(r.y - it.y) <= Math.max(2, Math.min(r.h, it.h) * 0.45)) r.items.push(it);
      else rg.push({ y: it.y, h: it.h, items: [it] });
    });
    return rg.map(function (r) {
      r.items.sort(function (a, b) { return a.x - b.x; });
      var s = "", eind = null;
      r.items.forEach(function (it) {
        if (eind != null) {
          var gat = it.x - eind;
          s += gat > it.h * 1.5 ? "   " : (gat > it.h * 0.15 && !/\s$/.test(s) && !/^\s/.test(it.s) ? " " : "");
        }
        s += it.s;
        eind = it.x + it.w;
      });
      return s.replace(/\s+$/, "");
    }).join("\n");
  }
  function pdfNaarTekst(bestand) {
    return Promise.all([laadPdfjs(), bestand.arrayBuffer()]).then(function (x) {
      return x[0].getDocument({ data: x[1] }).promise;
    }).then(function (doc) {
      var paginas = [];
      for (var i = 1; i <= Math.min(doc.numPages, 15); i++) paginas.push(doc.getPage(i).then(function (pg) { return pg.getTextContent(); }));
      return Promise.all(paginas);
    }).then(function (inh) {
      return inh.map(function (c) { return regelsUitItems(c.items); }).join("\n");
    });
  }
  var pdfStatus = root.querySelector(".boc-pdf-status"), invoer = root.querySelector("#boc-pdf"), drop = root.querySelector(".boc-drop");
  function status(tekst, isFout) { pdfStatus.textContent = tekst; pdfStatus.hidden = !tekst; pdfStatus.classList.toggle("is-fout", !!isFout); }
  function leesBestand(bestand) {
    if (!bestand) return;
    if (bestand.type !== "application/pdf" && !/\.pdf$/i.test(bestand.name)) { status("Dit is geen pdf. Plak de tekst van je offerte hieronder.", true); return; }
    if (bestand.size > 25 * 1024 * 1024) { status("Deze pdf is groter dan 25 MB. Plak de tekst hieronder.", true); return; }
    status("Bezig met lezen van " + bestand.name + "…");
    pdfNaarTekst(bestand).then(function (t) {
      if (t.replace(/\s/g, "").length < 40 || !/\d/.test(t)) {
        status("In deze pdf staat geen leesbare tekst. Het is waarschijnlijk een scan of foto, en die kan versie 1 nog niet lezen. Tip: kopieer de tekst uit de e-mail van je aanbieder, of typ de regels met een bedrag over in het vak hieronder.", true);
        return;
      }
      veld.value = t;
      status("Gelezen: " + bestand.name + ". De tekst staat hieronder; je kunt hem nog aanpassen.");
      check();
    }).catch(function () {
      status("Deze pdf konden we niet openen. Is hij beveiligd met een wachtwoord? Kopieer dan de tekst en plak hem hieronder.", true);
    });
  }
  invoer.addEventListener("change", function () { leesBestand(invoer.files[0]); invoer.value = ""; });
  ["dragenter", "dragover"].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add("is-over"); }); });
  ["dragleave", "drop"].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.remove("is-over"); }); });
  drop.addEventListener("drop", function (e) { var f = e.dataTransfer && e.dataTransfer.files; if (f && f[0]) leesBestand(f[0]); });

  /* ---------------------------------------------------- knoppen */
  root.querySelector(".boc-check").addEventListener("click", check);
  root.querySelector(".boc-wis").addEventListener("click", function () {
    veld.value = ""; basisKeuze.value = ""; uitslag.hidden = true; laag2.hidden = true; fout.hidden = true; status(""); laatste = null; veld.focus();
  });
  root.querySelector(".boc-kopieer").addEventListener("click", function () {
    var t = root.querySelector(".boc-mailtekst").value, ok = root.querySelector(".boc-kopieer-ok");
    kopieer(t, function (gelukt) {
      ok.textContent = gelukt ? "Gekopieerd. Plak de vragen in een mail aan je aanbieder." : "Kopiëren lukte niet. Open ‘Bekijk de mail’ en kopieer de tekst zelf.";
      ok.hidden = false;
      if (!gelukt) root.querySelector(".boc-mail").open = true;
    });
  });

  var l2tekst = root.querySelector("#boc-l2-tekst"), teller = root.querySelector(".boc-l2-teller");
  function tel() { teller.textContent = l2tekst.value.length.toLocaleString("nl-NL") + " van 3.000 tekens"; }
  l2tekst.addEventListener("input", tel);
  root.querySelector(".boc-l2-toon").addEventListener("click", function () {
    if (!laatste) return;
    var spec = root.querySelector("#boc-l2-spec");
    if (!l2tekst.value) l2tekst.value = String(specificatie(laatste) || "").slice(0, 3000);
    spec.hidden = false; this.setAttribute("aria-expanded", "true"); tel(); l2tekst.focus();
  });
  root.querySelector(".boc-l2-gebruik").addEventListener("click", function () {
    var t = l2tekst.value.trim().slice(0, 3000);
    if (!t) { l2tekst.focus(); return; }
    try { sessionStorage.setItem("tb_offertespec", t); } catch (e) {}
    window.location.href = "/offerte-aanvragen/?via=offertecheck";
  });
})();
</script>"""
