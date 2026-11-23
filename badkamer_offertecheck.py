# -*- coding: utf-8 -*-
"""
Offertechecker voor badkamerofferte: /tools/offertechecker/

De bezoeker plakt de tekst van een offerte. De parser (offerte_parser_badkamer.js,
inline in de pagina) herkent de posten en legt ze naast richtprijzen. Daarna volgt
een checklist van wat vaak ontbreekt. Alles draait in de browser: er gaat niets
naar een server en er wordt niets opgeslagen.

Interface voor build.py: LINKS en build(write). CSS en JS staan in deze module.
"""

import json
import pathlib

from components import page, crumbs, faq_blok, cta_blok, title, eur
from data import DIENST_BY_SLUG
import richtprijzen as RP

PAD = "/tools/offertechecker/"

LINKS = [
    (PAD, "Offertechecker",
     "Plak je badkamerofferte en zie per post of de prijs binnen de richtprijs valt en wat er ontbreekt."),
]

# ---------------------------------------------------------------------------
# Richtprijzen per post. Bedragen inclusief 21% btw, tenzij excl_btw.
# Alle bedragen en bronnen komen uit richtprijzen.py (gedeeld met de calculator en de
# kostenpagina's). Hier staat alleen hoe de checker ze combineert:
# - sloop: van alleen slopen (laag) tot slopen met dekvloer en afvoer (hoog), omdat offertes
#   die twee vaak in één post zetten;
# - leidingwerk: van op dezelfde plek (laag) tot verplaatsen (leidingwerk hoog + verplaatsen hoog);
# - tegelwerk_incl: legloon plus tegels.
# Bewust ruime bandbreedtes; de parser geeft pas "hoog" of "laag" bij meer dan 10% buiten de band.
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


def _band_tekst(b):
    return f"{eur(b['van'])} – {eur(b['tot'])}"


def _richtprijs_tabel():
    rijen = ""
    for sleutel, naam, eenheid, uitleg, bronnen in RICHTPRIJS_RIJEN:
        b = BANDEN[sleutel]
        noten = "".join(f'<sup><a href="#boc-bron-{_BRON_NR[k]}">{_BRON_NR[k]}</a></sup>' for k in bronnen)
        rijen += (f'<tr><td><strong>{naam}</strong><br><small>{uitleg}</small></td>'
                  f'<td class="num">{_band_tekst(b)}{noten}<br><small>{eenheid}</small></td></tr>')
    return f'<div class="tablewrap"><table class="boc-tabel"><thead><tr><th>Post</th><th>Richtprijs</th></tr></thead><tbody>{rijen}</tbody></table></div>'


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Offertechecker", None)])
    data = {"banden": BANDEN}

    hero = f"""{cr}
<section class="section-sm tool-hero" data-boc>
<div class="wrap">
  <div class="boc-kop">
    <span class="badge">Gratis tool · alles blijft op je eigen toestel</span>
    <h1>Offertechecker voor je badkamer</h1>
    <p class="lead">Plak de tekst van je badkamerofferte hieronder. Je ziet per post of de prijs binnen de richtprijs valt, of de bedragen optellen, en wat er vaak ontbreekt.</p>
  </div>
  <div class="formcard boc-kaart">
    <div class="boc-privacy" role="note">
      <strong>Je offerte blijft bij jou.</strong> De check draait helemaal in je browser. De tekst gaat niet naar een server, wordt niet opgeslagen en niemand anders ziet hem. Haal je naam en adres er gerust uit.
    </div>
    <label for="boc-tekst" class="boc-label">Tekst van de offerte</label>
    <textarea id="boc-tekst" rows="12" spellcheck="false" placeholder="Open de offerte (pdf of e-mail), selecteer alles, kopieer en plak het hier.&#10;&#10;Bijvoorbeeld:&#10;Sloopwerk badkamer        € 850,00&#10;Tegelwerk 30 m2 à € 45,00  € 1.350,00&#10;Totaal excl. btw ..."></textarea>
    <div class="boc-rij">
      <label for="boc-basis" class="boc-label-klein">De bedragen op de offerte zijn</label>
      <select id="boc-basis">
        <option value="">automatisch bepalen</option>
        <option value="excl">exclusief btw</option>
        <option value="incl">inclusief btw</option>
      </select>
    </div>
    <div class="boc-knoppen">
      <button type="button" class="btn btn-primary btn-lg boc-check">Check de offerte</button>
      <button type="button" class="btn btn-ghost boc-wis">Wissen</button>
    </div>
    <p class="boc-fout" hidden></p>
    <noscript><p class="callout">Zet JavaScript aan om de offertechecker te gebruiken. De check draait in je browser.</p></noscript>
  </div>
  <div class="boc-uitslag" aria-live="polite" hidden>
    <h2>Zo ziet je offerte eruit</h2>
    <div class="boc-totalen"></div>
    <div class="boc-meldingen"></div>
    <h3>Per post</h3>
    <div class="boc-posten"></div>
    <p class="boc-klein">Richtprijzen inclusief 21% btw (het uurtarief exclusief btw). We noemen een post pas hoog of laag als hij meer dan 10% buiten de bandbreedte valt. Een post buiten de band is niet fout: het is een reden om door te vragen.</p>
    <div class="boc-g2">
      <div class="boc-blok"><h3>Wat vaak ontbreekt</h3><ul class="boc-lijst"></ul></div>
      <div class="boc-blok"><h3>Vragen voor de specialist</h3><ul class="boc-vragen"></ul></div>
    </div>
    <div class="boc-verder">
      <p><strong>Wil je een tweede of derde offerte om te vergelijken?</strong> Via ons formulier vraag je die gratis aan bij maximaal drie badkamerspecialisten uit je regio.</p>
      <a class="btn btn-primary" href="/offerte-aanvragen/">Vergelijk offertes</a>
    </div>
  </div>
</div>
</section>"""

    uitleg = f"""<section class="section soft" id="richtprijzen"><div class="wrap narrow prose">
  <h2>Met welke richtprijzen we vergelijken</h2>
  <p>Dit zijn de bandbreedtes die de checker gebruikt. Ze komen van openbare prijsoverzichten en zijn bewust ruim, want geen badkamer is hetzelfde. De grootte, de staat van de vloer en muren, het sanitair dat je kiest en de regio maken veel uit. Een complete badkamer van 5 tot 9 m² kost volgens onze <a href="/kosten/nieuwe-badkamer/">kostenpagina</a> meestal {eur(_ren['prijs_van'])} tot {eur(_ren['prijs_tot'])}.</p>
  {_richtprijs_tabel()}
  <p><small>Prijspeil 2026, inclusief 21% btw tenzij anders vermeld. Meer over de prijzen per onderdeel: <a href="/kosten/badkamer-slopen/">badkamer slopen</a>, <a href="/kosten/tegelzetter-per-m2/">tegelzetter per m²</a>, <a href="/kosten/kitwerk-voegen/">kitwerk en voegen</a> en <a href="/kosten/uurtarief-loodgieter/">uurtarief loodgieter</a>.</small></p>

  <h2>Wat hoort er in een goede badkamerofferte?</h2>
  <p>Een goede offerte laat per onderdeel zien wat er gebeurt en wat het kost. Let vooral op deze punten:</p>
  <ul>
    <li><strong>Waterdicht maken.</strong> Onder de tegels in de douchehoek en op de vloer hoort een waterdichte laag, met kimband in de hoeken. Staat het er niet in, vraag ernaar. Lees <a href="/kennisbank/badkamer-waterdicht-maken/">hoe een badkamer waterdicht wordt gemaakt</a>.</li>
    <li><strong>Kitwerk.</strong> Kit langs het bad, de douche, de wastafel en in de hoeken. Het lijkt een detail, maar slecht kitwerk geeft lekkage.</li>
    <li><strong>Afvoer van afval.</strong> Wie haalt het sloopafval weg, en zit de container in de prijs?</li>
    <li><strong>Stelposten met een eerlijk bedrag.</strong> Een stelpost is een voorlopig bedrag, bijvoorbeeld voor sanitair of tegels die je later kiest. Is dat bedrag laag, dan lijkt de offerte goedkoop en betaal je later bij.</li>
    <li><strong>Planning.</strong> Een startdatum en een doorlooptijd, liefst per fase. Zie ook de <a href="/tools/renovatieplanner/">renovatieplanner</a>.</li>
    <li><strong>Garantie.</strong> Hoe lang, en op wat: het werk, de waterdichting, het sanitair. Lees <a href="/kennisbank/garantie-badkamerrenovatie/">waar je op let bij garantie</a>.</li>
    <li><strong>Betaaltermijnen.</strong> Spreek af dat je het grootste deel betaalt na oplevering, niet vooraf.</li>
  </ul>
  <h3>Welk btw-tarief?</h3>
  <p>Op badkamerwerk, sanitair, tegelwerk en installatiewerk zit 21% btw. Het lage tarief van 9% geldt alleen voor bepaalde werkzaamheden aan een woning ouder dan twee jaar, zoals stukadoren en verven, en bij isoleren alleen voor het arbeidsloon (<a href="{BRONNEN['btw'][1]}" rel="noopener" target="_blank">Belastingdienst</a>). Staat er 9% op je hele offerte, vraag dan waarom.</p>

  <h3>Bronnen</h3>
  <ol class="boc-bronnen">{"".join(f'<li id="boc-bron-{_BRON_NR[k]}"><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for k, (t, u) in BRONNEN.items())}</ol>
</div></section>"""

    faqs = [
        ("Wordt mijn offerte ergens opgeslagen?",
         "Nee. De checker draait helemaal in je browser. De tekst die je plakt gaat niet naar een server en wordt niet bewaard. Sluit je de pagina, dan is hij weg."),
        ("Werkt het met elke offerte?",
         "Met de meeste. De checker leest regels met een omschrijving en een bedrag, en herkent aantallen zoals m², meters en uren. Bij een offerte met alleen een totaalprijs kan hij de posten niet beoordelen, maar wel de checklist invullen. Kijk de uitslag altijd zelf na."),
        ("Wat betekent hoog of laag?",
         "Dat de post meer dan 10% boven of onder de richtprijs ligt. Dat is geen oordeel over de vakman. Een hoge post kan kloppen, bijvoorbeeld bij grote tegels of verplaatste leidingen. Een lage post kan betekenen dat er iets ontbreekt. Vraag in beide gevallen wat erin zit."),
        ("Wat is een stelpost?",
         "Een voorlopig bedrag voor iets wat nog niet vastligt, zoals sanitair of tegels die je later uitzoekt. Na afloop wordt het verschil verrekend. Een stelpost die te laag is, maakt de offerte goedkoper dan hij in werkelijkheid is."),
        ("Welk btw-tarief hoort op een badkamerofferte?",
         "21%, op het werk en op de materialen. Alleen bepaalde onderdelen, zoals stukadoren of verven in een woning ouder dan twee jaar, mogen onder 9% vallen."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over de offertechecker")

    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Offertechecker badkamer",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsers",
        "inLanguage": "nl-NL",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Plak de tekst van een badkamerofferte en zie per post of de prijs binnen de richtprijs valt en wat er ontbreekt. Draait in de browser.",
    }

    data_tag = ('<script type="application/json" id="boc-data">'
                + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    parser_tag = "<script>\n" + PARSER_JS.replace("</script", "<\\/script") + "\n</script>"

    body = (hero + uitleg + faq_html
            + cta_blok("Nog maar één offerte?", "Vergelijken werkt het best met twee of drie offertes. Vraag ze gratis en vrijblijvend aan bij maximaal drie badkamerspecialisten uit je regio.", "Vraag offertes aan")
            + PAGE_CSS + data_tag + parser_tag + PAGE_JS)

    write(PAD, page(
        title("Offertechecker badkamer: klopt je offerte?"),
        "Plak je badkamerofferte en zie per post of de prijs klopt met de richtprijs, of de bedragen optellen en wat er ontbreekt. Alles blijft in je browser.",
        PAD, body, [cr_ld, faq_ld, app_ld]), prio=0.7)


# ---------------------------------------------------------------------------
# CSS (alleen deze pagina)
# ---------------------------------------------------------------------------

PAGE_CSS = """<style>
[data-boc] [hidden]{display:none!important}
.boc-kop{max-width:760px;margin:0 auto 18px;text-align:center}
.boc-kaart{max-width:820px;margin:0 auto;border-top:4px solid var(--accent)}
.boc-privacy{background:var(--bg-soft);border-left:4px solid var(--green);border-radius:10px;padding:12px 14px;font-size:.94rem;margin:0 0 16px}
.boc-label{display:block;font-weight:700;color:var(--ink);margin:0 0 6px}
.boc-label-klein{font-size:.92rem;color:var(--muted);margin:0}
#boc-tekst{display:block;width:100%;box-sizing:border-box;font:14px/1.45 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;padding:12px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink);resize:vertical;min-height:220px}
#boc-tekst:focus,#boc-basis:focus{outline:3px solid var(--accent-soft);border-color:var(--accent)}
.boc-rij{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center;margin:12px 0 0}
#boc-basis{font:inherit;padding:8px 10px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.boc-knoppen{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0 0}
.boc-fout{color:#a3361a;font-weight:600;margin:12px 0 0}
.boc-uitslag{max-width:980px;margin:32px auto 0}
.boc-uitslag h2{text-align:center}
.boc-uitslag h3{font-size:1.08rem;margin:22px 0 10px}
.boc-totalen{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:10px}
.boc-tot{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:12px 14px}
.boc-tot span{display:block;font-size:.84rem;color:var(--muted)}
.boc-tot b{font-size:1.25rem;color:var(--ink)}
.boc-melding{border-radius:10px;padding:10px 14px;margin:10px 0 0;font-size:.95rem}
.boc-m-ok{background:#e7f5ef;color:#0b5e41}.boc-m-let{background:#fff6e0;color:#6b4d00}.boc-m-fout{background:#fdecea;color:#8f2a1b}
.boc-post{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 14px;background:#fff;border:1px solid var(--line);border-left:5px solid var(--line);border-radius:var(--radius);padding:12px 14px;margin:0 0 8px}
.boc-post.o-binnen{border-left-color:var(--green)}.boc-post.o-hoog{border-left-color:#c0392b}.boc-post.o-laag{border-left-color:#e2a80c}
.boc-post.o-uit{opacity:.7}
.boc-soort{font-weight:700;color:var(--ink)}
.boc-oms{font-size:.9rem;color:var(--muted);overflow-wrap:anywhere}
.boc-bedrag{text-align:right;font-weight:700;color:var(--ink);white-space:nowrap}
.boc-oordeel{grid-column:1/-1;font-size:.9rem}
.boc-tag{display:inline-block;font-size:.78rem;font-weight:700;border-radius:99px;padding:2px 9px;margin-right:6px;vertical-align:1px}
.boc-t-binnen{background:#e7f5ef;color:#0b5e41}.boc-t-hoog{background:#fdecea;color:#8f2a1b}.boc-t-laag{background:#fff6e0;color:#6b4d00}.boc-t-geen{background:var(--bg-soft);color:var(--muted)}
.boc-vraag{display:block;margin-top:4px;color:var(--body)}
.boc-klein{font-size:.85rem;color:var(--muted);margin:10px 0 0}
.boc-g2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin-top:8px}
@media(max-width:760px){.boc-g2{grid-template-columns:minmax(0,1fr)}}
.boc-blok{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px}
.boc-blok h3{margin-top:0}
.boc-lijst,.boc-vragen{margin:0;padding:0;list-style:none}
.boc-lijst li,.boc-vragen li{margin:0 0 10px;padding-left:28px;position:relative;font-size:.95rem}
.boc-lijst li::before{position:absolute;left:0;top:0;width:20px;height:20px;border-radius:50%;display:grid;place-items:center;font-size:.75rem;font-weight:800;color:#fff}
.boc-lijst li.s-ok::before{content:"\\2713";background:var(--green)}
.boc-lijst li.s-mist::before{content:"!";background:#c0392b}
.boc-lijst li.s-let::before{content:"?";background:#e2a80c}
.boc-lijst li.s-neutraal::before{content:"\\2013";background:#8aa0a5}
.boc-vragen li::before{content:"\\203A";position:absolute;left:8px;top:-2px;font-weight:800;color:var(--accent);font-size:1.2rem}
.boc-verder{display:flex;flex-wrap:wrap;gap:12px 20px;align-items:center;justify-content:space-between;background:var(--accent-soft);border-radius:var(--radius);padding:16px 18px;margin-top:20px}
.boc-verder p{margin:0;flex:1 1 320px}
.boc-tabel td{vertical-align:top}
.boc-tabel td small{color:var(--muted)}
.boc-tabel sup a{text-decoration:none;margin-left:2px}
.boc-bronnen{font-size:.88rem}
.boc-bronnen li{margin:4px 0;overflow-wrap:anywhere}
@media(max-width:480px){.boc-kaart{padding:18px 14px}.boc-knoppen .btn{flex:1 1 100%}}
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
  var B = JSON.parse(document.getElementById("boc-data").textContent).banden;
  var veld = root.querySelector("#boc-tekst"), basisKeuze = root.querySelector("#boc-basis");
  var uitslag = root.querySelector(".boc-uitslag"), fout = root.querySelector(".boc-fout");

  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var euro = P.euro;
  var EENH = { m2: "m²", m: "meter", uur: "uur", post: "post" };

  function tot(label, waarde, noot) {
    return '<div class="boc-tot"><span>' + label + "</span><b>" + (waarde == null ? "–" : euro(waarde)) + "</b>" + (noot ? '<span>' + noot + "</span>" : "") + "</div>";
  }
  function melding(soort, tekst) { return '<p class="boc-melding boc-m-' + soort + '">' + tekst + "</p>"; }

  function postHtml(p, r) {
    var b = P.beoordeelPost(p, B, r.basis, (r.btwTarieven || [])[0]);
    var naam = (P.TYPES[p.type] || P.TYPES.overig).naam;
    var detail = "";
    if (p.aantal && p.eenheid) detail = p.aantal.toLocaleString("nl-NL") + " " + (P.EENHEDEN[p.eenheid] || p.eenheid) + (p.eenheidsprijs ? " à " + euro(p.eenheidsprijs) : "");
    var tags = [];
    if (p.stelpost) tags.push("stelpost");
    if (p.optie) tags.push("optie, telt niet mee");
    else if (p.naTotaal) tags.push("staat na het totaal, telt niet mee");
    var oordeel;
    if (b.oordeel) {
      var band = euro(b.van) + " – " + euro(b.tot) + (b.perEenheid ? " per " + EENH[b.perEenheid] : "") + (b.inclBtw ? " incl. btw" : " excl. btw");
      var vgl = euro(b.vergelijk) + (b.perEenheid ? " per " + EENH[b.perEenheid] : "") + (b.inclBtw ? " incl. btw" : " excl. btw");
      var woord = { binnen: "binnen de richtprijs", hoog: "boven de richtprijs", laag: "onder de richtprijs" }[b.oordeel];
      oordeel = '<span class="boc-tag boc-t-' + b.oordeel + '">' + woord + "</span>" + vgl + " · richtprijs " + band;
    } else {
      var reden = { "geen richtprijs": "geen richtprijs voor deze post", "geen aantal": "geen aantal gevonden, dus niet te vergelijken", "andere eenheid": "andere eenheid dan de richtprijs", "geen bedrag": "geen bedrag gevonden", korting: "korting" }[b.reden] || b.reden;
      oordeel = '<span class="boc-tag boc-t-geen">' + esc(reden) + "</span>";
    }
    var vraag = b.vragen.length ? '<span class="boc-vraag">' + esc(b.vragen[0]) + "</span>" : "";
    var bedrag = p.bedrag != null ? euro(p.bedrag) : (p.eenheidsprijs != null ? euro(p.eenheidsprijs) + (p.eenheid ? " per " + (P.EENHEDEN[p.eenheid] || p.eenheid) : "") : "–");
    return '<div class="boc-post o-' + (b.oordeel || "geen") + (p.meetellen ? "" : " o-uit") + '">' +
      '<div><div class="boc-soort">' + esc(naam) + (tags.length ? ' <span class="boc-tag boc-t-geen">' + esc(tags.join(", ")) + "</span>" : "") + "</div>" +
      '<div class="boc-oms">' + esc(p.omschrijving) + (detail ? " · " + esc(detail) : "") + "</div></div>" +
      '<div class="boc-bedrag">' + bedrag + "</div>" +
      '<div class="boc-oordeel">' + oordeel + vraag + "</div></div>";
  }

  function check() {
    var tekst = veld.value;
    fout.hidden = true;
    if (!/\d/.test(tekst) || tekst.trim().length < 20) {
      fout.textContent = "Plak eerst de tekst van je offerte, met de bedragen erbij.";
      fout.hidden = false; uitslag.hidden = true; return;
    }
    var r = P.leesOfferte(tekst);
    var keuze = basisKeuze.value;
    if (keuze && keuze !== r.basis) {
      r.basis = keuze;
      r.controle = P.controle(r.somPosten, keuze, r.totaal, r.subtotaal, 0);
    }
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
    if (!r.posten.length) m += melding("let", "We vonden geen losse posten met een bedrag. Staat er alleen een totaalprijs op de offerte? Vraag dan om een uitsplitsing per onderdeel." + (t.twijfel ? " We zagen wel een totaal van " + euro(t.twijfel) + ", maar niet of dat inclusief of exclusief btw is." : ""));
    else if (r.controle.klopt === true) m += melding("ok", "De posten tellen op tot het totaal (" + euro(r.controle.tegen) + " " + basisTekst + ").");
    else if (r.controle.klopt === false) m += melding("fout", "De posten tellen op tot " + euro(r.controle.som) + ", maar het totaal is " + euro(r.controle.tegen) + ". Verschil: " + euro(r.controle.verschil) + ". Controleer of we een regel gemist hebben, of vraag waar het verschil zit.");
    m += melding("let", "We lezen de bedragen als " + basisTekst + ". Klopt dat niet? Kies het hierboven en check opnieuw.");
    (r.meldingen || []).forEach(function (x) { m += melding("let", esc(x)); });
    root.querySelector(".boc-meldingen").innerHTML = m;

    root.querySelector(".boc-posten").innerHTML = r.posten.map(function (p) { return postHtml(p, r); }).join("") || '<p class="boc-klein">Geen posten gevonden.</p>';

    root.querySelector(".boc-lijst").innerHTML = P.checklist(r, B).map(function (c) {
      return '<li class="s-' + c.status + '"><strong>' + esc(c.titel) + ".</strong> " + esc(c.uitleg) + "</li>";
    }).join("");
    var vragen = P.algemeneVragen(r);
    r.posten.forEach(function (p) {
      var b = P.beoordeelPost(p, B, r.basis, (r.btwTarieven || [])[0]);
      if (b.oordeel === "hoog" || b.oordeel === "laag") vragen.push((P.TYPES[p.type] || P.TYPES.overig).naam + ": " + b.vragen[0]);
      else if (b.vragen[0] && vragen.length < 8 && p.meetellen && p.type !== "korting") vragen.push((P.TYPES[p.type] || P.TYPES.overig).naam + ": " + b.vragen[0]);
    });
    root.querySelector(".boc-vragen").innerHTML = vragen.slice(0, 10).map(function (v) { return "<li>" + esc(v) + "</li>"; }).join("") || "<li>Geen extra vragen gevonden. Loop de offerte toch nog even zelf na.</li>";

    uitslag.hidden = false;
    var top = uitslag.getBoundingClientRect().top + window.scrollY - 80;
    window.scrollTo({ top: top, behavior: "smooth" });
  }

  root.querySelector(".boc-check").addEventListener("click", check);
  root.querySelector(".boc-wis").addEventListener("click", function () {
    veld.value = ""; basisKeuze.value = ""; uitslag.hidden = true; fout.hidden = true; veld.focus();
  });
})();
</script>"""
