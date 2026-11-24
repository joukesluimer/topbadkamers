# -*- coding: utf-8 -*-
"""Badkamer voor ...: /badkamer-voor/ (kiezer) en zes doelgroeppagina's (/badkamer-voor/<slug>/).

Elke pagina spreekt de situatie van één groep aan (gezinnen, ouderen, starters, tweede badkamer,
appartementen, verhuurders), met:
- de keuzes die voor die groep echt anders zijn;
- een bestaande 3D-render (render_data.py of render_stijl_data.py) als illustratie;
- een kleine rekenhulp of checklist die bij de groep past (inline JS, voorvoegsel .bv-);
- drie budgetscenario's die per post zijn opgeteld uit richtprijzen.py, zodat de bedragen
  aansluiten op de rest van de site;
- links naar kennis-, kosten-, spullen- en inspiratiepagina's, een offertecheck-blok, FAQ en CTA.

Bronnen (geraadpleegd november 2026):
- Rijksoverheid, vergoeding voor woningaanpassing (Wmo, eigen bijdrage, Wlz):
  https://www.rijksoverheid.nl/vraag-en-antwoord/zorg-en-ondersteuning-thuis/vergoeding-voor-woningaanpassing
- Rijksoverheid, ondersteuning gemeente Wmo 2015 ("in een onderzoek, meestal een gesprek"):
  https://www.rijksoverheid.nl/vraag-en-antwoord/zorg-en-ondersteuning-thuis/ondersteuning-gemeente-wmo-2015
- Staatsblad 2024, 194 (Besluit betaalbare huur), bijlage I onder A, rubriek 6 Sanitair:
  toilet 3 (apart) / 2 (in badkamer), hangend toilet 3,75 / 2,75, wastafel 1 (max 1 per vertrek
  m.u.v. de badkamer), meerpersoonswastafel 1,5, douche 4, bad 6, bad/douche 7; voorzieningen
  (tot maximaal het aantal punten van douche, bad of bad/douche): bubbelfunctie 1,5, volledige
  afscheiding douche 1,25, handdoekenradiator 0,75, ingebouwd kastje met wastafel 1, kastruimte 0,75,
  stopcontact 0,25 (max 0,5 per wastafel), eenhandsmengkraan 0,25, thermostatische mengkraan 0,5.
  Rubriek 7: 1 punt per € 332 aan woonvoorzieningen voor gehandicapten. Grens middenhuur: 186 punten.
  https://zoek.officielebekendmakingen.nl/stb-2024-194.html
- Milieu Centraal, besparen onder de douche (waterbesparende douchekop max 7,2 l/min, gemiddeld
  ruim 7 minuten douchen, regendouche bij voorkeur onder 15 l/min):
  https://www.milieucentraal.nl/energie-besparen/duurzaam-warm-water/besparen-onder-de-douche/
- Milieu Centraal, nieuwe badkamer: duurzaam verbouwen:
  https://www.milieucentraal.nl/huis-en-tuin/verbouwen/nieuwe-badkamer/
- Prijzen: richtprijzen.py (Homedeal, Trustoo, Werkspot, Slimster), allemaal incl. 21% btw.
"""

import datetime
import json

import richtprijzen as RP
from components import (page, crumbs, title, faq_blok, cta_blok, cta_midden, offertecheck_blok,
                        prijs_balken, render_beeld, eur)
from data import SITE
from render_data import RENDERS
from render_stijl_data import RENDERS_STIJL

PAD = "/badkamer-voor/"
GEPUBLICEERD = "2026-11-23"

B_WMO = ("Rijksoverheid, vergoeding voor woningaanpassing",
         "https://www.rijksoverheid.nl/vraag-en-antwoord/zorg-en-ondersteuning-thuis/vergoeding-voor-woningaanpassing")
B_WMO2 = ("Rijksoverheid, ondersteuning van de gemeente (Wmo 2015)",
          "https://www.rijksoverheid.nl/vraag-en-antwoord/zorg-en-ondersteuning-thuis/ondersteuning-gemeente-wmo-2015")
B_WWS = ("Staatsblad 2024, 194: Besluit betaalbare huur (puntentelling sanitair)",
         "https://zoek.officielebekendmakingen.nl/stb-2024-194.html")
B_HC = ("Huurcommissie (huurprijscheck en beleidsboeken)", "https://www.huurcommissie.nl/")
B_MC_DOUCHE = ("Milieu Centraal, besparen onder de douche",
               "https://www.milieucentraal.nl/energie-besparen/duurzaam-warm-water/besparen-onder-de-douche/")
B_MC_BADKAMER = ("Milieu Centraal, nieuwe badkamer: duurzaam verbouwen",
                 "https://www.milieucentraal.nl/huis-en-tuin/verbouwen/nieuwe-badkamer/")

# ---------------------------------------------------------------------------
# Linkkaarten (alle paden komen uit de brief: bestaande pagina's en de nieuwe URL's van ronde 3)
# ---------------------------------------------------------------------------

K = {
    # kennisbank
    "/kennisbank/inloopdouche-zonder-drempel/": ("Kennisbank", "Inloopdouche zonder drempel", "Afschot, goot en waterkering."),
    "/kennisbank/badkamer-ventilatie/": ("Kennisbank", "Badkamer ventileren", "Vocht en schimmel voorkomen."),
    "/kennisbank/verbouwen-in-vve/": ("Kennisbank", "Verbouwen in een VvE", "Toestemming, geluid en leidingen."),
    "/kennisbank/kleine-badkamer-indelen/": ("Kennisbank", "Kleine badkamer indelen", "Slimme indelingen voor weinig ruimte."),
    "/kennisbank/volgorde-badkamerrenovatie/": ("Kennisbank", "Volgorde van de renovatie", "Wat eerst, wat daarna."),
    "/kennisbank/badkamer-waterdicht-maken/": ("Kennisbank", "Badkamer waterdicht maken", "Zo blijft de douchehoek droog."),
    "/kennisbank/garantie-badkamerrenovatie/": ("Kennisbank", "Garantie op je badkamer", "Wat je vastlegt in de offerte."),
    "/kennisbank/asbest-in-badkamer/": ("Kennisbank", "Asbest in de badkamer", "Wanneer je moet laten testen."),
    "/kennisbank/hangtoilet-of-staand-toilet/": ("Kennisbank", "Hangtoilet of staand toilet", "Voor- en nadelen naast elkaar."),
    "/kennisbank/badkamer-schoonmaken/": ("Kennisbank", "Badkamer schoonmaken", "Materialen die weinig onderhoud vragen."),
    "/kennisbank/water-besparen-badkamer/": ("Kennisbank", "Water besparen", "Douchekop, kraan en toilet."),
    "/kennisbank/badkamer-en-suite/": ("Kennisbank", "Badkamer en suite", "Een badkamer bij de slaapkamer."),
    "/kennisbank/badkamerverlichting/": ("Kennisbank", "Badkamerverlichting", "Licht dat veilig en prettig is."),
    "/kennisbank/grote-tegels-badkamer/": ("Kennisbank", "Grote tegels", "Minder voegen, minder schoonmaken."),
    "/kennisbank/badkamer-zonder-tegels/": ("Kennisbank", "Badkamer zonder tegels", "Microcement, panelen en meer."),
    # kosten
    "/kosten/nieuwe-badkamer/": ("Kosten", "Wat kost een nieuwe badkamer?", "Richtprijzen met rekenvoorbeeld."),
    "/kosten/inloopdouche/": ("Kosten", "Kosten inloopdouche", "Goot, glas en tegelwerk."),
    "/kosten/kleine-badkamer/": ("Kosten", "Kosten kleine badkamer", "Wat een compacte badkamer kost."),
    "/kosten/badkamer-opknappen/": ("Kosten", "Badkamer opknappen", "Opfrissen zonder te slopen."),
    "/kosten/tweede-badkamer/": ("Kosten", "Kosten tweede badkamer", "Afvoer, ventilatie en inbouw."),
    "/kosten/badkamer-ventilatie/": ("Kosten", "Kosten ventilatie", "Ventilator en afvoerkanaal."),
    "/kosten/douche-vervangen/": ("Kosten", "Douche vervangen", "Wat het kost en wat erbij komt."),
    "/kosten/wastafel-vervangen/": ("Kosten", "Wastafel vervangen", "Meubel, kraan en aansluiting."),
    "/kosten/kraan-vervangen/": ("Kosten", "Kraan vervangen", "Thermostaatkraan en mengkraan."),
    "/kosten/vloerverwarming-badkamer/": ("Kosten", "Vloerverwarming", "Elektrisch of watergedragen."),
    "/kosten/kitwerk-voegen/": ("Kosten", "Kitwerk en voegen", "Onderhoud per meter."),
    "/kosten/uurtarief-loodgieter/": ("Kosten", "Uurtarief loodgieter", "Voor kleine reparaties."),
    # spullen
    "/badkamerspullen/wastafelmeubel-kiezen/": ("Kopersgids", "Wastafelmeubel kiezen", "Enkel of dubbel, maten en materiaal."),
    "/badkamerspullen/kranen-kiezen/": ("Kopersgids", "Kranen kiezen", "Thermostaat, mengkraan en afwerking."),
    "/badkamerspullen/douchesysteem-kiezen/": ("Kopersgids", "Douchesysteem kiezen", "Thermostaat, opbouw of inbouw."),
    "/badkamerspullen/bad-of-douche/": ("Kopersgids", "Bad of douche?", "De voor- en nadelen naast elkaar."),
    "/badkamerspullen/toilet-kiezen/": ("Kopersgids", "Toilet kiezen", "Hangend of staand, hoogte en spoeling."),
    "/badkamerspullen/inloopdouche-kopen/": ("Kopersgids", "Inloopdouche kopen", "Glas, afvoer en maten."),
    "/badkamerspullen/douchegoot-kiezen/": ("Kopersgids", "Douchegoot kiezen", "Lengte, rooster en afvoer."),
    "/badkamerspullen/douchewand-kiezen/": ("Kopersgids", "Douchewand kiezen", "Glas, coating en profiel."),
    "/badkamerspullen/badkamerradiator-kiezen/": ("Kopersgids", "Badkamerradiator kiezen", "Vermogen en handdoekbeugels."),
    "/badkamerspullen/spiegelkast-kiezen/": ("Kopersgids", "Spiegelkast kiezen", "Bergruimte boven de wastafel."),
    "/badkamerspullen/inbouwreservoir-kiezen/": ("Kopersgids", "Inbouwreservoir kiezen", "Voorzetwand en bedieningsplaat."),
    "/badkamerspullen/fontein-kiezen/": ("Kopersgids", "Fontein kiezen", "Voor een extra toilet."),
    "/badkamerspullen/badkamertegels-kopen/": ("Kopersgids", "Badkamertegels kopen", "Formaat, materiaal en antislip."),
    "/badkamerspullen/vrijstaand-bad-kopen/": ("Kopersgids", "Vrijstaand bad kopen", "Maat, gewicht en kraan."),
    # inspiratie, materialen en tools
    "/inspiratie/kleine-badkamer/": ("Inspiratie", "Kleine badkamer", "Een compacte badkamer in beeld."),
    "/inspiratie/moderne-badkamer/": ("Inspiratie", "Moderne badkamer", "Strak, rustig en makkelijk schoon."),
    "/inspiratie/scandinavische-badkamer/": ("Inspiratie", "Scandinavische badkamer", "Licht, hout en rustige kleuren."),
    "/inspiratie/japandi-badkamer/": ("Inspiratie", "Japandi-badkamer", "Rust, hout en natuurlijke tinten."),
    "/inspiratie/landelijke-badkamer/": ("Inspiratie", "Landelijke badkamer", "Warm en ambachtelijk."),
    "/inspiratie/industriele-badkamer/": ("Inspiratie", "Industriële badkamer", "Betonlook en zwart staal."),
    "/inspiratie/voor-en-na/": ("Inspiratie", "Voor en na", "Zie wat een renovatie verandert."),
    "/materialen/keramische-tegels/": ("Materialen", "Keramische tegels", "Sterk, betaalbaar, weinig onderhoud."),
    "/materialen/voegen-en-kit/": ("Materialen", "Voegen en kit", "Wat lang mooi blijft."),
    "/materialen/kraanafwerkingen/": ("Materialen", "Kraanafwerkingen", "Chroom, zwart en messing."),
    "/materialen/meubelmaterialen/": ("Materialen", "Meubelmaterialen", "Wat tegen vocht en stoten kan."),
    "/tools/indelingsplanner/": ("Tool", "Indelingsplanner", "Schuif douche, toilet en meubel op maat."),
    "/tools/badkamercalculator/": ("Tool", "Badkamercalculator", "Reken je eigen badkamer door."),
    "/tools/renovatieplanner/": ("Tool", "Renovatieplanner", "Je planning week voor week."),
    "/zo-verloopt-je-verbouwing/": ("Uitleg", "Zo verloopt je verbouwing", "Van eerste gesprek tot oplevering."),
}


def _kaart(pad):
    soort, naam, oms = K[pad]
    return (f'<a href="{pad}"><span class="bv-soort">{soort}</span><span class="bv-naam">{naam}</span>'
            f'<span class="bv-oms">{oms}</span></a>')


# ---------------------------------------------------------------------------
# Budgetscenario's: optellen uit richtprijzen.py
# ---------------------------------------------------------------------------

def _post(sleutel, n=1, niveau=None):
    p = RP.RICHTPRIJZEN[sleutel]
    if niveau:
        l, h = p["niveaus"][niveau]
    else:
        l, h = p["laag"], p["hoog"]
    return l * n, h * n


def _scenario(regels):
    """regels = [(label, sleutel, aantal, niveau)] -> (laag, hoog, html-regels, sleutels)."""
    tl = th = 0
    rijen = ""
    for label, sleutel, n, niveau in regels:
        l, h = _post(sleutel, n, niveau)
        tl += l
        th += h
        rijen += f"<tr><td>{label}</td><td>{eur(round(l))} – {eur(round(h))}</td></tr>"
    laag = int(tl // 100 * 100)
    hoog = int(-(-th // 100) * 100)
    return laag, hoog, rijen, [r[1] for r in regels]


def _tegels(m2, niveau):
    return [(f"Tegels zetten, {m2} m² (legloon)", "tegelwerk", m2, None),
            (f"Lijm, voeg en kit, {m2} m²", "tegelwerk_hulpmateriaal", m2, None),
            (f"Tegels, {m2} m² ({niveau})", "tegels", m2, niveau)]


def _basis_renovatie():
    return [("Slopen", "sloop", 1, None), ("Afval afvoeren", "afval", 1, None),
            ("Leidingwerk op dezelfde plek", "leidingwerk", 1, None),
            ("Waterdicht maken douchehoek", "waterdicht", 1, None)]


def _scenarios_html(scenarios, eenheid_noot):
    """scenarios = [(naam, wat, regels)]."""
    kaarten = ""
    balken = []
    sleutels = set()
    for i, (naam, wat, regels) in enumerate(scenarios):
        laag, hoog, rijen, sl = _scenario(regels)
        sleutels.update(sl)
        balken.append((naam, laag, hoog))
        kaarten += (f'<div class="bv-scen{" bv-scen-mid" if i == 1 else ""}">'
                    f'<p class="bv-scen-nr">Scenario {i + 1}</p><h3>{naam}</h3>'
                    f'<p class="bv-scen-prijs">{eur(laag)} – {eur(hoog)}</p><p>{wat}</p>'
                    f'<details><summary>Zo is het opgeteld</summary><table class="bv-tabel">{rijen}</table></details></div>')
    bronnen = []
    for s in sorted(sleutels):
        for b in RP.bron_links(s):
            if b not in bronnen:
                bronnen.append(b)
    bron_html = ", ".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in bronnen)
    html = (f'<div class="bv-scens">{kaarten}</div>'
            + prijs_balken(balken, "Richtprijs per scenario, inclusief materiaal, arbeid en 21% btw", eenheid_noot)
            + f'<p class="bv-klein">Opgeteld per post uit dezelfde richtprijzen als op onze kostenpagina\'s. '
              f'Een offerte kan hoger of lager uitkomen, bijvoorbeeld door de staat van de '
              f'ondergrond, de bereikbaarheid of je regio.</p>'
              f'<details class="bv-klein"><summary>Bronnen van de richtprijzen</summary><p>{bron_html}.</p></details>')
    return html, balken


# ---------------------------------------------------------------------------
# Iconen (eigen inline SVG, lijnstijl)
# ---------------------------------------------------------------------------

def _svg(paden, size=44):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" stroke="currentColor" '
            f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paden}</svg>')


ICONEN = {
    "gezinnen": '<circle cx="15" cy="12" r="5"/><circle cx="33" cy="12" r="5"/><circle cx="24" cy="25" r="3.5"/>'
                '<path d="M6 40v-8a9 9 0 0 1 18 0"/><path d="M24 32a9 9 0 0 1 18 0v8"/><path d="M19 42v-4a5 5 0 0 1 10 0v4"/>',
    "ouderen": '<circle cx="20" cy="9" r="4.5"/><path d="M20 15v13l-6 13"/><path d="M20 28l6 13"/><path d="M14 20l12 3"/>'
               '<path d="M34 18v24"/><path d="M34 18c0-3 4-3 4 0"/>',
    "starters": '<path d="M6 22L24 8l18 14"/><path d="M11 19v21h26V19"/><rect x="20" y="28" width="8" height="12"/>'
                '<path d="M34 6v8"/><path d="M30 10h8"/>',
    "tweede-badkamer": '<rect x="5" y="9" width="17" height="30" rx="2"/><rect x="26" y="9" width="17" height="30" rx="2"/>'
                       '<path d="M10 17h7"/><path d="M31 17h7"/><path d="M34.5 24v8"/><path d="M30.5 28h8"/>',
    "appartementen": '<rect x="9" y="5" width="30" height="38" rx="2"/><path d="M15 12h5M28 12h5M15 20h5M28 20h5M15 28h5M28 28h5"/>'
                     '<path d="M21 43v-7h6v7"/>',
    "verhuurders": '<circle cx="15" cy="24" r="8"/><path d="M23 24h20"/><path d="M37 24v6"/><path d="M42 24v5"/>'
                   '<circle cx="15" cy="24" r="2.5"/>',
}

# ---------------------------------------------------------------------------
# CSS (voorvoegsel .bv-)
# ---------------------------------------------------------------------------

CSS = """<style>
.bv-kort{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 4px;padding:0;list-style:none}
.prose .bv-kort li{margin:0;padding:6px 12px 6px 30px;background:var(--bg-soft,#f6f4f0);border:1px solid var(--line);border-radius:999px;font-size:.88rem;position:relative}
.prose .bv-kort li::before{content:"";position:absolute;left:11px;top:50%;width:9px;height:9px;margin-top:-5px;border-radius:50%;background:var(--accent,#c4572a);border:0}
.bv-keuzes{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:18px 0}
.bv-keuze{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px 18px;border-top:4px solid var(--accent,#c4572a)}
.bv-keuze h3{font-size:1.02rem;margin:0 0 6px}
.bv-keuze p{font-size:.93rem;margin:0;line-height:1.5}
.bv-maat{display:inline-block;margin-top:8px;font-size:.8rem;font-weight:700;color:var(--accent-dark,#9a3d14);background:var(--accent-soft,#f6e4da);padding:2px 9px;border-radius:999px}
.bv-zo{display:grid;grid-template-columns:1.25fr 1fr;gap:22px;align-items:center;background:var(--bg-soft,#f6f4f0);border:1px solid var(--line);border-radius:var(--radius-lg,16px);padding:18px;margin:26px 0}
.bv-zo h2{margin-top:0}
.bv-zo ul{margin:0}
.bv-zo .render img{transition:transform .5s ease}
.bv-zo:hover .render img{transform:scale(1.02)}
.bv-tool{background:#fff;border:2px solid var(--accent-soft,#f6e4da);border-radius:var(--radius-lg,16px);padding:20px;margin:26px 0;box-shadow:var(--shadow,0 4px 18px rgba(20,30,40,.06))}
.bv-tool h2{margin-top:0}
.bv-tool-lbl{display:inline-block;font-size:.74rem;font-weight:800;text-transform:uppercase;letter-spacing:.05em;color:var(--accent-dark,#9a3d14);margin-bottom:4px}
.bv-veld{margin:0 0 14px}
.bv-veld label,.bv-veld .bv-vlabel{display:flex;flex-wrap:wrap;justify-content:space-between;gap:2px 10px;font-weight:700;font-size:.95rem;margin-bottom:6px}
.bv-veld output{font-variant-numeric:tabular-nums;color:var(--accent-dark,#9a3d14);margin-left:auto;text-align:right}
.bv-veld input[type=range]{width:100%;accent-color:var(--accent,#c4572a);height:28px}
.bv-veld select{width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:#fff}
.bv-velden{display:grid;grid-template-columns:1fr 1fr;gap:4px 22px}
.bv-keus{display:flex;flex-wrap:wrap;gap:8px}
.bv-keus label{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:7px 13px;font-weight:600;font-size:.9rem;cursor:pointer;background:#fff}
.bv-keus input{accent-color:var(--accent,#c4572a)}
.bv-keus label:has(input:checked){border-color:var(--accent,#c4572a);background:var(--accent-soft,#f6e4da)}
.bv-uit{background:var(--bg-soft,#f6f4f0);border-radius:var(--radius);padding:16px 18px;margin-top:8px;min-height:120px}
.bv-uit h3{font-size:1.02rem;margin:0 0 8px}
.bv-uit-rij{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-top:1px solid var(--line)}
.bv-uit-rij:first-of-type{border-top:0}
.bv-uit-rij p{margin:0;font-size:.94rem}
.bv-stip{flex:0 0 14px;height:14px;border-radius:50%;margin-top:4px;background:#8fbf9a}
.bv-stip.oranje{background:#e7a54a}.bv-stip.rood{background:#d0573a}
.bv-meter{height:12px;background:#e6e2da;border-radius:999px;overflow:hidden;margin:8px 0 4px}
.bv-meter span{display:block;height:100%;width:0;background:var(--accent,#c4572a);border-radius:999px;transition:width .35s ease}
.bv-check{display:grid;grid-template-columns:1fr 1fr;gap:6px 18px;margin:0 0 12px;padding:0;list-style:none}
.prose .bv-check li{margin:0;padding:0}
.prose .bv-check li::before{display:none}
.bv-check label{display:flex;gap:10px;align-items:flex-start;padding:9px 10px;border:1px solid var(--line);border-radius:10px;cursor:pointer;font-size:.93rem;line-height:1.4;background:#fff}
.bv-check input{margin-top:3px;accent-color:var(--accent,#c4572a);flex:0 0 auto;width:18px;height:18px}
.bv-check label:has(input:checked){background:#eef6f0;border-color:#9cc8a6}
.bv-check small{display:block;color:var(--muted,#5b6470);font-size:.82rem}
.bv-groep{font-weight:800;font-size:.86rem;text-transform:uppercase;letter-spacing:.04em;margin:12px 0 6px;color:var(--muted,#5b6470)}
.bv-scens{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0}
.bv-scen{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px}
.bv-scen-mid{border-color:var(--accent,#c4572a);box-shadow:0 6px 22px rgba(20,30,40,.07)}
.bv-scen h3{font-size:1.02rem;margin:0 0 4px}
.bv-scen p{font-size:.92rem;margin:0 0 8px}
.bv-scen-nr{font-size:.74rem!important;text-transform:uppercase;letter-spacing:.05em;color:var(--muted,#5b6470);font-weight:700;margin:0 0 2px!important}
.bv-scen-prijs{font-size:1.25rem!important;font-weight:800;color:var(--ink,#1d2733);font-variant-numeric:tabular-nums}
.bv-scen summary{cursor:pointer;font-size:.86rem;font-weight:700;color:var(--accent-dark,#9a3d14)}
.bv-tabel{width:100%;border-collapse:collapse;font-size:.8rem;margin-top:8px}
.bv-tabel td{padding:4px 0;border-top:1px solid var(--line);vertical-align:top}
.bv-tabel td:last-child{text-align:right;white-space:nowrap;padding-left:8px;font-variant-numeric:tabular-nums}
.bv-klein{font-size:.86rem;color:var(--muted,#5b6470)}
.bv-kader{background:#f3f7fb;border:1px solid #cfdceb;border-left:5px solid #3d6f9e;border-radius:var(--radius);padding:16px 18px;margin:22px 0}
.bv-kader h2,.bv-kader h3{margin-top:0}
.bv-verder{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0 8px}
.bv-verder a{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;text-decoration:none;color:inherit;transition:border-color .15s,transform .15s}
.bv-verder a:hover,.bv-verder a:focus-visible{border-color:var(--accent);transform:translateY(-2px)}
.bv-soort{display:block;font-size:.72rem;text-transform:uppercase;letter-spacing:.04em;color:var(--accent-dark,#9a3d14);font-weight:700}
.bv-naam{display:block;font-weight:700;margin:3px 0}
.bv-oms{display:block;font-size:.88rem;color:var(--muted,#5b6470)}
.bv-andere{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0}
.bv-andere a{display:inline-flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:999px;padding:6px 14px 6px 8px;text-decoration:none;color:inherit;font-weight:600;font-size:.9rem;background:#fff}
.bv-andere a:hover{border-color:var(--accent)}
.bv-andere svg{width:24px;height:24px;color:var(--accent,#c4572a)}
.bv-bronnen{font-size:.86rem}
/* kiezer */
.bv-kiezer{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px}
.bv-kies{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg,16px);overflow:hidden;text-decoration:none;color:inherit;transition:border-color .2s,box-shadow .2s,transform .2s}
.bv-kies:hover,.bv-kies:focus-visible{border-color:var(--accent);box-shadow:0 10px 30px rgba(20,30,40,.1);transform:translateY(-3px)}
.bv-kies-beeld{position:relative;aspect-ratio:3/2;background:#e9e6e0;overflow:hidden}
.bv-kies-beeld img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s ease}
.bv-kies:hover .bv-kies-beeld img{transform:scale(1.04)}
.bv-kies-beeld figcaption{position:absolute;left:8px;bottom:8px;background:rgba(255,255,255,.9);color:#334;font-size:.7rem;padding:2px 8px;border-radius:999px}
.bv-kies-ic{position:absolute;right:12px;bottom:-26px;width:58px;height:58px;border-radius:50%;background:#fff;color:var(--accent,#c4572a);display:flex;align-items:center;justify-content:center;box-shadow:0 4px 14px rgba(20,30,40,.15)}
.bv-kies-beeld{overflow:visible}
.bv-kies-beeld img{border-radius:0}
.bv-kies-tekst{padding:18px 18px 18px}
.bv-kies h2{font-size:1.15rem;margin:0 0 6px;padding-right:56px}
.bv-kies p{font-size:.93rem;margin:0 0 10px}
.bv-kies ul{list-style:none;padding:0;margin:0 0 12px;display:flex;flex-wrap:wrap;gap:6px}
.bv-kies li{font-size:.78rem;background:var(--bg-soft,#f6f4f0);border-radius:999px;padding:3px 10px;margin:0}
.bv-kies li::before{display:none}
.bv-go{font-weight:700;color:var(--accent-dark,#9a3d14);font-size:.92rem;margin-top:auto}
@media (max-width:900px){.bv-kiezer{grid-template-columns:1fr 1fr}.bv-scens{grid-template-columns:1fr}}
@media (max-width:700px){.bv-zo,.bv-velden,.bv-check{grid-template-columns:1fr}.bv-kiezer{grid-template-columns:1fr}.bv-tool{padding:16px 14px}.bv-verder{grid-template-columns:1fr 1fr;gap:8px}.bv-verder a{padding:11px 12px}.bv-naam{font-size:.92rem;line-height:1.3}.bv-oms{display:none}}
@media (prefers-reduced-motion:reduce){.bv-zo .render img,.bv-kies,.bv-kies img,.bv-verder a,.bv-meter span{transition:none!important;transform:none!important}}
</style>"""

# ---------------------------------------------------------------------------
# Rekenhulpen (HTML + JS per groep)
# ---------------------------------------------------------------------------

TOOL_GEZIN = """<div class="bv-tool" id="spitsuur">
<span class="bv-tool-lbl">Rekenhulp</span>
<h2>Spitsuur-check: hoeveel badkamer heeft jouw gezin nodig?</h2>
<p>Vul in hoe jullie ochtend eruitziet. Je ziet of één wastafel, één douche en één toilet genoeg zijn, en hoeveel warm water er in die tijd doorheen gaat.</p>
<div class="bv-velden">
 <div class="bv-veld"><label for="bv-pers">Gezinsleden <output id="bv-pers-o">4</output></label><input type="range" id="bv-pers" min="1" max="8" value="4"></div>
 <div class="bv-veld"><label for="bv-douch">Douchen 's ochtends <output id="bv-douch-o">3</output></label><input type="range" id="bv-douch" min="0" max="8" value="3"></div>
 <div class="bv-veld"><label for="bv-tijd">Ochtendvenster <output id="bv-tijd-o">45 min</output></label><input type="range" id="bv-tijd" min="20" max="120" step="5" value="45"></div>
 <div class="bv-veld"><label for="bv-dmin">Douchetijd per persoon <output id="bv-dmin-o">7 min</output></label><input type="range" id="bv-dmin" min="3" max="15" value="7"></div>
 <div class="bv-veld"><label for="bv-kop">Douchekop</label><select id="bv-kop"><option value="7">Waterbesparend (tot 7,2 liter per minuut)</option><option value="9" selected>Gewone douchekop (ongeveer 9 liter)</option><option value="12">Regendouche (ongeveer 12 liter)</option></select></div>
 <div class="bv-veld"><span class="bv-vlabel">Toiletten in huis</span><div class="bv-keus"><label><input type="radio" name="bv-wc" value="1" checked> 1, in de badkamer</label><label><input type="radio" name="bv-wc" value="2"> 1, apart</label><label><input type="radio" name="bv-wc" value="3"> 2 of meer</label></div></div>
</div>
<div class="bv-uit" id="bv-gezin-uit" aria-live="polite"></div>
<p class="bv-klein">Dit is een vuistregel, geen berekening van een installateur. We rekenen met ongeveer 5 minuten wastafeltijd en 4 minuten toilettijd per persoon in de ochtend, en met het douchedebiet dat je kiest. Hoeveel warm water je cv-ketel of boiler echt kan leveren, hangt af van het toestel; laat dat nakijken voordat je een tweede douche laat aanleggen.</p>
</div>"""

JS_GEZIN = r"""(function(){
var $=function(i){return document.getElementById(i)};
if(!$('bv-pers'))return;
function rij(kl,t){return '<div class="bv-uit-rij"><span class="bv-stip '+kl+'"></span><p>'+t+'</p></div>'}
function reken(){
 var p=+$('bv-pers').value,d=+$('bv-douch').value,v=+$('bv-tijd').value,m=+$('bv-dmin').value,k=+$('bv-kop').value;
 if(d>p){d=p;$('bv-douch').value=p}
 var wc=+document.querySelector('input[name=bv-wc]:checked').value;
 $('bv-pers-o').textContent=p;$('bv-douch-o').textContent=d;$('bv-tijd-o').textContent=v+' min';$('bv-dmin-o').textContent=m+' min';
 var dBez=d*m,wBez=p*5,tBez=p*4,uit='<h3>Advies voor jullie ochtend</h3>';
 var rD=dBez/v;
 if(rD<=0.5)uit+=rij('','<strong>Douche: één is genoeg.</strong> De douche is '+dBez+' van de '+v+' minuten bezet.');
 else if(rD<=0.8)uit+=rij('oranje','<strong>Douche: krap.</strong> De douche is '+dBez+' van de '+v+' minuten bezet. Een vaste volgorde of een paar mensen \'s avonds laten douchen lost veel op.');
 else uit+=rij('rood','<strong>Douche: te weinig.</strong> '+dBez+' minuten douchen past niet goed in '+v+' minuten. Denk aan een tweede douche, bijvoorbeeld in een tweede badkamer, of spreid het douchen over de dag.');
 var rW=wBez/v;
 if(p>=4&&rW>0.35)uit+=rij('oranje','<strong>Wastafel: kies een dubbele.</strong> Met '+p+' personen staan jullie samen ongeveer '+wBez+' minuten aan de wastafel. Twee wasbakken halveren de wachtrij; daarvoor heb je een meubel van zo\'n 120 cm nodig.');
 else if(p>=3)uit+=rij('','<strong>Wastafel: één kan, twee is prettig.</strong> Ongeveer '+wBez+' minuten wastafeltijd. Een brede wasbak met twee kranen is een tussenvorm.');
 else uit+=rij('','<strong>Wastafel: één is genoeg.</strong>');
 if(wc===1&&p>=3)uit+=rij('rood','<strong>Toilet: zet er een apart toilet bij.</strong> Het enige toilet in de badkamer blokkeert de badkamer als iemand doucht. Een apart toilet met fontein is in de ochtend de grootste winst.');
 else if(wc<3&&p>=5&&tBez/v>0.4)uit+=rij('oranje','<strong>Toilet: een tweede toilet helpt.</strong> Met '+p+' personen is één toilet in de ochtendspits krap.');
 else uit+=rij('','<strong>Toilet: dit is genoeg.</strong>');
 var l=d*m*k,lz=d*m*7;
 var tw='<strong>Warm water: ongeveer '+l+' liter douchewater</strong> van rond de 40 °C in het ochtendvenster.';
 if(l>200)uit+=rij('rood',tw+' Dat is veel. Laat een installateur kijken of je toestel dit aankan, zeker als twee mensen tegelijk douchen. Een grotere boiler of een toestel met voorraadvat kan nodig zijn.');
 else if(l>120)uit+=rij('oranje',tw+' Na elkaar douchen gaat met een goede combiketel meestal prima. Tegelijk douchen in twee badkamers vraagt meer: laat de warmwaterklasse van je ketel of de inhoud van je boiler checken.');
 else uit+=rij('',tw+' Dat is voor de meeste toestellen geen probleem.');
 if(k>7&&d>0)uit+=rij('','<strong>Besparen:</strong> met een waterbesparende douchekop is het ongeveer '+lz+' liter, '+(l-lz)+' liter minder per ochtend.');
 $('bv-gezin-uit').innerHTML=uit;
}
['bv-pers','bv-douch','bv-tijd','bv-dmin','bv-kop'].forEach(function(i){$(i).addEventListener('input',reken)});
document.querySelectorAll('input[name=bv-wc]').forEach(function(e){e.addEventListener('change',reken)});
reken();
})();"""

CHECK_OUDEREN = [
    ("Toegang", [
        ("drempel", "Geen drempel bij de badkamerdeur", "Ook geen opstaande rand bij de douche.", "nu"),
        ("deur", "Deur van minstens 85 cm breed", "Of een schuifdeur, of een deur die naar buiten draait.", "nu"),
        ("ruimte", "Draairuimte van ongeveer 1,50 m", "Richtmaat als je ooit met rollator of rolstoel wilt draaien.", "voor"),
    ]),
    ("Douche", [
        ("inloop", "Inloopdouche zonder instap", "Vloer loopt door, water loopt weg via een goot.", "nu"),
        ("antislip", "Stroeve vloertegels", "Vraag naar tegels die ook nat stroef zijn.", "nu"),
        ("thermo", "Thermostaatkraan", "Houdt de temperatuur gelijk en voorkomt verbranden.", "nu"),
        ("zitje", "Douchezitje of klapstoel", "Aan de wand, opklapbaar als je hem niet nodig hebt.", "voor"),
        ("beugel_d", "Beugel bij de douche", "Om je aan vast te houden bij het in- en uitstappen.", "voor"),
    ]),
    ("Toilet en wastafel", [
        ("wc_hoog", "Toilet op een hogere zithoogte", "Een hangtoilet kun je op de gewenste hoogte laten plaatsen.", "nu"),
        ("beugel_t", "Beugel of steun bij het toilet", "Opklapbaar, zodat hij niet in de weg zit.", "voor"),
        ("wastafel", "Wastafel die je zittend kunt gebruiken", "Ruimte eronder, kraan met een lange hendel.", "voor"),
    ]),
    ("Voorbereiden", [
        ("wand", "Verstevigde wanden", "Laat nu achterhout of plaatmateriaal in de wanden zetten: dan kun je later overal beugels monteren.", "nu"),
        ("licht", "Goed licht en een nachtlampje", "Licht met bewegingsmelder helpt 's nachts.", "voor"),
        ("stopc", "Stopcontact op een makkelijke hoogte", "Ook handig voor een elektrische tandenborstel of föhn.", "voor"),
    ]),
]


def _tool_ouderen():
    groepen = ""
    for groep, items in CHECK_OUDEREN:
        li = "".join(f'<li><label><input type="checkbox" value="{k}" data-wat="{t}" data-wanneer="{w}">'
                     f'<span>{t}<small>{u}</small></span></label></li>' for k, t, u, w in items)
        groepen += f'<p class="bv-groep">{groep}</p><ul class="bv-check">{li}</ul>'
    n = sum(len(i) for _, i in CHECK_OUDEREN)
    return f"""<div class="bv-tool" id="checklist">
<span class="bv-tool-lbl">Checklist</span>
<h2>Is je badkamer levensloopbestendig?</h2>
<p>Vink aan wat je badkamer nu al heeft. Je ziet direct wat nog ontbreekt, en wat je het beste meteen bij de verbouwing regelt en wat je alleen hoeft voor te bereiden.</p>
{groepen}
<div class="bv-uit" id="bv-oud-uit" aria-live="polite" data-n="{n}"></div>
<p class="bv-klein">De maten zijn richtmaten. Heb je een beperking of een indicatie, laat de gemeente (Wmo) of een ergotherapeut dan meekijken: die adviseren wat in jouw situatie nodig is.</p>
</div>"""


JS_OUDEREN = r"""(function(){
var uit=document.getElementById('bv-oud-uit');if(!uit)return;
var boxen=[].slice.call(document.querySelectorAll('#checklist input[type=checkbox]'));
function reken(){
 var n=boxen.length,ja=0,nu=[],voor=[];
 boxen.forEach(function(b){if(b.checked)ja++;else(b.dataset.wanneer==='nu'?nu:voor).push(b.dataset.wat)});
 var pct=Math.round(ja/n*100),h='<h3>'+ja+' van de '+n+' punten in orde</h3><div class="bv-meter" aria-hidden="true"><span style="width:'+pct+'%"></span></div>';
 if(!nu.length&&!voor.length)h+='<p>Je badkamer is goed voorbereid op later. Mooi.</p>';
 if(nu.length)h+='<div class="bv-uit-rij"><span class="bv-stip rood"></span><p><strong>Regel dit bij de verbouwing</strong> (later aanpassen kost veel meer breekwerk): '+nu.join(', ').toLowerCase()+'.</p></div>';
 if(voor.length)h+='<div class="bv-uit-rij"><span class="bv-stip oranje"></span><p><strong>Kan later, als je het voorbereidt:</strong> '+voor.join(', ').toLowerCase()+'.</p></div>';
 uit.innerHTML=h;
}
boxen.forEach(function(b){b.addEventListener('change',reken)});
reken();
})();"""


def _starter_posten():
    """Posten voor de budgetverdeler: [naam, [ (optie, laag, hoog), ... ], standaardindex]."""
    def som(regels):
        l = h = 0
        for s, n, niv in regels:
            a, b = _post(s, n, niv)
            l += a
            h += b
        return round(l), round(h)
    t = lambda m2, niv: [("tegelwerk", m2, None), ("tegelwerk_hulpmateriaal", m2, None), ("tegels", m2, niv)]
    posten = [
        ["Sloop, afvoer en waterdicht maken", [("Nodig bij elke renovatie", *som([("sloop", 1, None), ("afval", 1, None), ("waterdicht", 1, None)]))], 0],
        ["Leidingwerk", [("Alles op dezelfde plek", *som([("leidingwerk", 1, None)])),
                         ("Eén onderdeel verplaatsen", *som([("leidingwerk", 1, None), ("leidingwerk_verplaatsen", 1, None)]))], 0],
        ["Tegels en tegelwerk", [("Alleen vloer en douchewand (12 m²), basis", *som(t(12, "basis"))),
                                 ("Wanden en vloer (25 m²), basis", *som(t(25, "basis"))),
                                 ("Wanden en vloer (25 m²), midden", *som(t(25, "midden"))),
                                 ("Wanden en vloer (25 m²), luxe", *som(t(25, "luxe")))], 1],
        ["Douche", [("Basis, met thermostaatkraan", *som([("sanitair_douche", 1, "basis"), ("montage_douche", 1, None)])),
                    ("Midden, inloopdouche met glazen wand", *som([("sanitair_douche", 1, "midden"), ("montage_douche", 1, None)])),
                    ("Luxe, met regendouche of inbouw", *som([("sanitair_douche", 1, "luxe"), ("montage_douche", 1, None)]))], 0],
        ["Toilet", [("Bestaand toilet houden", 0, 0),
                    ("Basis", *som([("sanitair_toilet", 1, "basis"), ("montage_toilet", 1, None)])),
                    ("Midden, hangtoilet", *som([("sanitair_toilet", 1, "midden"), ("montage_toilet", 1, None)]))], 1],
        ["Wastafelmeubel", [("Basis", *som([("sanitair_meubel", 1, "basis"), ("montage_meubel", 1, None)])),
                            ("Midden", *som([("sanitair_meubel", 1, "midden"), ("montage_meubel", 1, None)])),
                            ("Luxe", *som([("sanitair_meubel", 1, "luxe"), ("montage_meubel", 1, None)]))], 0],
        ["Elektra en ventilatie", [("Ventilator vervangen", *som([("ventilator", 1, None)])),
                                   ("Ventilator en extra stopcontacten en licht", *som([("ventilator", 1, None), ("elektra", 1, None)]))], 0],
        ["Vloerverwarming", [("Later of niet", 0, 0),
                             ("Elektrische vloerverwarming", *som([("vloerverwarming_elektrisch", 1, None)]))], 0],
    ]
    return posten


def _tool_starters():
    posten = _starter_posten()
    velden = ""
    for i, (naam, opties, std) in enumerate(posten):
        if len(opties) == 1:
            velden += (f'<div class="bv-veld"><span class="bv-vlabel">{naam} <output>{opties[0][0]}</output></span>'
                       f'<p class="bv-klein" style="margin:0">Vaste post: {eur(opties[0][1])} – {eur(opties[0][2])}</p></div>')
        else:
            velden += (f'<div class="bv-veld"><label for="bv-p{i}">{naam} <output id="bv-p{i}-o"></output></label>'
                       f'<input type="range" id="bv-p{i}" data-i="{i}" min="0" max="{len(opties) - 1}" value="{std}" step="1"></div>')
    data = json.dumps([{"n": naam, "o": opties} for naam, opties, _ in posten], ensure_ascii=False)
    return f"""<div class="bv-tool" id="budgetverdeler">
<span class="bv-tool-lbl">Rekenhulp</span>
<h2>Budgetverdeler: wat past er nu in je budget?</h2>
<p>Stel je budget in en schuif per onderdeel naar het niveau dat je wilt. Je ziet meteen of het past, en wat je kunt uitstellen.</p>
<div class="bv-veld"><label for="bv-budget">Jouw budget <output id="bv-budget-o"></output></label><input type="range" id="bv-budget" min="4000" max="20000" step="500" value="9000"></div>
<div class="bv-velden">{velden}</div>
<div class="bv-uit" id="bv-start-uit" aria-live="polite"></div>
<p class="bv-klein">Gerekend met de richtprijzen van deze site voor een badkamer van ongeveer 5 m², inclusief 21% btw. We vergelijken je budget met het midden van de bandbreedte. Een offerte kan afwijken, onder meer door de staat van de ondergrond en de bereikbaarheid.</p>
<script type="application/json" id="bv-start-data">{data}</script>
</div>"""


JS_STARTERS = r"""(function(){
var d=document.getElementById('bv-start-data');if(!d)return;
var P=JSON.parse(d.textContent),$=function(i){return document.getElementById(i)};
function e(n){return '€ '+(Math.round(n/100)*100).toLocaleString('nl-NL')}
var sl=[].slice.call(document.querySelectorAll('#budgetverdeler input[data-i]'));
function reken(){
 var b=+$('bv-budget').value,l=0,h=0,later=[];
 $('bv-budget-o').textContent=e(b);
 P.forEach(function(post,i){
  var opties=post.o,s=$('bv-p'+i),o=opties[s?+s.value:0];
  if(s)$('bv-p'+i+'-o').textContent=o[0];
  l+=o[1];h+=o[2];
  if(s&&+s.value>0&&opties[0][2]===0)later.push(post.n.toLowerCase());
 });
 var m=(l+h)/2,pct=Math.min(100,Math.round(m/b*100)),kl,t;
 if(m<=b*0.9){kl='';t='Dit past, met ongeveer '+e(b-m)+' over voor onverwachte kosten. Houd 10 procent achter de hand.';}
 else if(m<=b){kl='oranje';t='Dit past net. Je hebt weinig ruimte voor tegenvallers; zet iets een niveau lager of stel een onderdeel uit.';}
 else{kl='rood';t='Dit gaat ongeveer '+e(m-b)+' over je budget. Schuif tegels of sanitair een niveau lager, houd het toilet of laat de vloerverwarming voor later.';}
 var h2='<h3>Geschat totaal: '+e(l)+' – '+e(h)+'</h3><div class="bv-meter" aria-hidden="true"><span style="width:'+pct+'%;background:'+(kl==='rood'?'#d0573a':kl==='oranje'?'#e7a54a':'#5f9e6e')+'"></span></div>';
 h2+='<div class="bv-uit-rij"><span class="bv-stip '+kl+'"></span><p>'+t+'</p></div>';
 if(later.length)h2+='<div class="bv-uit-rij"><span class="bv-stip"></span><p><strong>Kan ook later:</strong> '+later.join(', ')+'. Laat wel nu de leidingen of kabels voorbereiden als je dat wilt.</p></div>';
 $('bv-start-uit').innerHTML=h2;
}
sl.concat([$('bv-budget')]).forEach(function(s){s.addEventListener('input',reken)});
reken();
})();"""


def _tool_tweede():
    plekken = [("zolder", "Zolder"), ("slaapkamer", "Bij de slaapkamer (en suite)"), ("beneden", "Begane grond of bijkeuken")]
    afstand = [("kort", "Minder dan 1 m"), ("midden", "1 tot 3 m"), ("ver", "Meer dan 3 m of onbekend")]
    soort = [("compact", "Douche en wastafel"), ("toilet", "Douche, wastafel en toilet"), ("bad", "Met bad")]
    def keus(naam, opties):
        return '<div class="bv-keus">' + "".join(
            f'<label><input type="radio" name="{naam}" value="{v}"{" checked" if i == 0 else ""}> {t}</label>'
            for i, (v, t) in enumerate(opties)) + "</div>"
    # kostenbanden per soort (opgeteld uit richtprijzen, zie _tweede_banden)
    data = json.dumps(_tweede_banden(), ensure_ascii=False)
    return f"""<div class="bv-tool" id="plekkiezer">
<span class="bv-tool-lbl">Plek-check</span>
<h2>Waar komt je tweede badkamer?</h2>
<p>Kies de plek, de afstand tot de afvoer (de dikke standleiding waar ook je toilet op zit) en wat erin moet. Je ziet waar je op moet letten en een eerste kostenband.</p>
<div class="bv-veld"><span class="bv-vlabel">Plek</span>{keus("bv-plek", plekken)}</div>
<div class="bv-veld"><span class="bv-vlabel">Afstand tot de standleiding</span>{keus("bv-afst", afstand)}</div>
<div class="bv-veld"><span class="bv-vlabel">Wat moet erin?</span>{keus("bv-soort", soort)}</div>
<div class="bv-uit" id="bv-tweede-uit" aria-live="polite"></div>
<p class="bv-klein">Een eerste indicatie, opgeteld uit de richtprijzen van deze site (inclusief 21% btw). Een specialist kan pas na een bezoek zeggen hoe de afvoer precies loopt.</p>
<script type="application/json" id="bv-tweede-data">{data}</script>
</div>"""


def _tweede_banden():
    def som(regels):
        l = h = 0
        for s, n, niv in regels:
            a, b = _post(s, n, niv)
            l += a
            h += b
        return [round(l), round(h)]
    basis = [("leidingwerk", 1, None), ("waterdicht", 1, None), ("tegelwerk", 18, None),
             ("tegelwerk_hulpmateriaal", 18, None), ("tegels", 18, "basis"), ("elektra", 1, None),
             ("ventilator", 1, None), ("sanitair_douche", 1, "basis"), ("montage_douche", 1, None),
             ("sanitair_meubel", 1, "basis"), ("montage_meubel", 1, None)]
    toilet = [("sanitair_toilet", 1, "basis"), ("montage_toilet", 1, None), ("leidingwerk_toilet_verplaatsen", 1, None)]
    bad = [("sanitair_bad", 1, "basis"), ("montage_bad", 1, None)]
    return {"compact": som(basis), "toilet": som(basis + toilet), "bad": som(basis + toilet + bad),
            "extra_ver": som([("leidingwerk_verplaatsen", 1, None)])}


JS_TWEEDE = r"""(function(){
var d=document.getElementById('bv-tweede-data');if(!d)return;
var B=JSON.parse(d.textContent);
function e(n){return '€ '+(Math.round(n/100)*100).toLocaleString('nl-NL')}
function v(n){return document.querySelector('input[name='+n+']:checked').value}
function rij(kl,t){return '<div class="bv-uit-rij"><span class="bv-stip '+kl+'"></span><p>'+t+'</p></div>'}
var tekst={
 zolder:['Let op de stahoogte: bij de douche wil je minstens zo\'n 2 meter vrije hoogte. Een dakkapel of de hoge kant van het dak lost dat vaak op.','Ventilatie: een mechanische afzuiging via het dak of aansluiten op de bestaande ventilatie. Zonder goede afvoer krijg je vocht en schimmel onder het dak.','Een houten zoldervloer vraagt een waterdichte, stijve ondergrond. Vraag of de vloer versterkt moet worden, zeker bij een bad.'],
 slaapkamer:['Een badkamer bij de slaapkamer kost slaapkamerruimte; een open opzet met alleen een glazen wand bij de douche bespaart vierkante meters.','Geluid: kies een stil toilet of zet het toilet achter een eigen deur. Laat afvoerleidingen in de wand isoleren.','Ventilatie: een badkamer die direct aan de slaapkamer grenst, moet goed afzuigen, anders trekt het vocht de slaapkamer in.'],
 beneden:['Op de begane grond ligt de afvoer vaak onder de vloer. In een kruipruimte is aansluiten meestal eenvoudig; op een betonvloer zonder kruipruimte moet er soms gehakt worden.','Een bijkeuken of washok is vaak al nat en heeft een afvoer: dat scheelt leidingwerk.','Handig voor later: een douche op de begane grond maakt het makkelijker om op hoge leeftijd in huis te blijven wonen.']
};
function reken(){
 var p=v('bv-plek'),a=v('bv-afst'),s=v('bv-soort'),b=B[s].slice(),h='<h3>Aandachtspunten</h3>';
 tekst[p].forEach(function(t){h+=rij('',t)});
 if(a==='kort')h+=rij('','<strong>Afvoer dichtbij:</strong> mooi, het toilet en de douche kunnen met voldoende afschot aansluiten.');
 else if(a==='midden')h+=rij('oranje','<strong>Afvoer op 1 tot 3 meter:</strong> meestal goed te doen, maar je hebt afschot nodig. Een toilet heeft een dikke afvoer nodig; houd het toilet het dichtst bij de standleiding.');
 else{h+=rij('rood','<strong>Afvoer ver weg:</strong> dan wordt het lastiger. Soms moet er een nieuwe afvoer door de vloer, of is een vuilwaterpomp nodig. Dat maakt het duurder; vraag hier altijd een specialist naar.');b[0]+=B.extra_ver[0];b[1]+=B.extra_ver[1];}
 h+='<h3 style="margin-top:12px">Eerste kostenband: '+e(b[0])+' – '+e(b[1])+'</h3><p class="bv-klein" style="margin:0">Inclusief leidingwerk, tegelwerk (ongeveer 18 m²), elektra, ventilator en basis-sanitair. Zonder bouwkundig werk zoals een dakkapel of nieuwe wanden.</p>';
 document.getElementById('bv-tweede-uit').innerHTML=h;
}
document.querySelectorAll('#plekkiezer input').forEach(function(i){i.addEventListener('change',reken)});
reken();
})();"""


def _tool_appartement():
    werk = [
        ("leiding", "Leidingen of afvoer verplaatsen", "VvE"),
        ("vloer", "Vloer of dekvloer eruit halen", "VvE"),
        ("vvwater", "Vloerverwarming aansluiten op de cv", "VvE"),
        ("vent", "Ventilator op een gezamenlijk kanaal", "VvE"),
        ("harde", "Harde vloer of grote tegels (geluid)", "geluid"),
        ("bad", "Een (vrijstaand) bad plaatsen", "gewicht"),
        ("wand", "Een wand weghalen of verplaatsen", "VvE"),
        ("asbest", "Gebouw van vóór 1994", "asbest"),
    ]
    li = "".join(f'<li><label><input type="checkbox" value="{k}" data-soort="{s}"><span>{t}</span></label></li>'
                 for k, t, s in werk)
    return f"""<div class="bv-tool" id="vve-check">
<span class="bv-tool-lbl">Check</span>
<h2>VvE-check: wat moet je regelen?</h2>
<p>Vink aan wat je van plan bent. Je ziet wat je bij de VvE moet aanvragen en waar je op let.</p>
<ul class="bv-check">{li}</ul>
<div class="bv-veld"><label for="bv-badl">Inhoud van het bad (alleen bij een bad) <output id="bv-badl-o">180 liter</output></label><input type="range" id="bv-badl" min="100" max="400" step="10" value="180"></div>
<div class="bv-uit" id="bv-app-uit" aria-live="polite"></div>
<p class="bv-klein">Wat precies mag, staat in de splitsingsakte en het huishoudelijk reglement van jouw VvE. Deze check is een hulp, geen juridisch advies.</p>
</div>"""


JS_APPARTEMENT = r"""(function(){
var uit=document.getElementById('bv-app-uit');if(!uit)return;
var boxen=[].slice.call(document.querySelectorAll('#vve-check input[type=checkbox]')),$=function(i){return document.getElementById(i)};
function rij(kl,t){return '<div class="bv-uit-rij"><span class="bv-stip '+kl+'"></span><p>'+t+'</p></div>'}
function reken(){
 var s={};boxen.forEach(function(b){if(b.checked)s[b.value]=1});
 var l=+$('bv-badl').value;$('bv-badl-o').textContent=l+' liter';
 var h='',vve=[];
 if(s.leiding)vve.push('leidingen of afvoer verplaatsen');
 if(s.vloer)vve.push('de vloer openmaken');
 if(s.vvwater)vve.push('vloerverwarming op de cv');
 if(s.vent)vve.push('aansluiten op het ventilatiekanaal');
 if(s.wand)vve.push('een wand weghalen');
 if(vve.length)h+=rij('rood','<strong>Vraag vooraf schriftelijk toestemming aan de VvE</strong> voor: '+vve.join(', ')+'. Standleidingen, vloeren en ventilatiekanalen zijn vaak gemeenschappelijk. Plan het verzoek ruim voor de vergadering.');
 if(s.harde||s.vloer)h+=rij('oranje','<strong>Geluid:</strong> een harde vloer zonder goede ondervloer geeft contactgeluid bij de buren. Vraag welke geluidseisen je VvE stelt en laat de specialist een ontkoppelde (zwevende) opbouw voorstellen.');
 if(s.bad){var kg=l+60+80;h+=rij('oranje','<strong>Gewicht:</strong> een gevuld bad van '+l+' liter weegt met bad en persoon al snel zo\'n '+kg+' kilo, op minder dan een vierkante meter. Bij een houten vloer, een oud gebouw of een vrijstaand bad op pootjes: laat een constructeur kijken.');}
 if(s.asbest)h+=rij('rood','<strong>Asbest:</strong> in gebouwen van vóór 1994 kan asbest zitten, bijvoorbeeld in oude kitten, vloerlijm of leidingkokers. Laat dat eerst onderzoeken voordat er gesloopt wordt.');
 if(!h)h=rij('','Vink aan wat je van plan bent. Alleen sanitair op dezelfde plek vervangen kan vaak zonder toestemming, maar check altijd het huishoudelijk reglement.');
 else h='<h3>Dit regel je vooraf</h3>'+h;
 uit.innerHTML=h;
}
boxen.forEach(function(b){b.addEventListener('change',reken)});
$('bv-badl').addEventListener('input',reken);
reken();
})();"""


def _tool_verhuur():
    return """<div class="bv-tool" id="wws-sanitair">
<span class="bv-tool-lbl">Rekenhulp</span>
<h2>Puntenteller sanitair (WWS)</h2>
<p>Tel de punten van het sanitair in een zelfstandige huurwoning, volgens de tabel die sinds 1 juli 2024 geldt. Voor de volledige puntentelling van de woning gebruik je de huurprijscheck van de Huurcommissie.</p>
<div class="bv-velden">
 <div class="bv-veld"><label for="bv-wc1">Toilet 1</label><select id="bv-wc1"><option value="0">Geen</option><option value="3">Staand, aparte toiletruimte (3)</option><option value="2">Staand, in de badkamer (2)</option><option value="3.75" selected>Hangend, aparte toiletruimte (3,75)</option><option value="2.75">Hangend, in de badkamer (2,75)</option></select></div>
 <div class="bv-veld"><label for="bv-wc2">Toilet 2</label><select id="bv-wc2"><option value="0" selected>Geen</option><option value="3">Staand, aparte toiletruimte (3)</option><option value="2">Staand, in de badkamer (2)</option><option value="3.75">Hangend, aparte toiletruimte (3,75)</option><option value="2.75">Hangend, in de badkamer (2,75)</option></select></div>
 <div class="bv-veld"><label for="bv-was">Wastafels in de badkamer <output id="bv-was-o">1</output></label><input type="range" id="bv-was" min="0" max="3" value="1"></div>
 <div class="bv-veld"><label for="bv-mp">Waarvan meerpersoonswastafel <output id="bv-mp-o">0</output></label><input type="range" id="bv-mp" min="0" max="2" value="0"></div>
 <div class="bv-veld"><label for="bv-dou">Douche en bad</label><select id="bv-dou"><option value="0">Geen</option><option value="4" selected>Douche (4)</option><option value="6">Bad (6)</option><option value="7">Bad/douche of bad en douche (7)</option></select></div>
</div>
<p class="bv-groep">Voorzieningen in de badkamer</p>
<ul class="bv-check">
 <li><label><input type="checkbox" data-p="1.25" checked><span>Volledige, gemonteerde douche-afscheiding<small>1,25 punt</small></span></label></li>
 <li><label><input type="checkbox" data-p="0.75"><span>Handdoekenradiator<small>0,75 punt</small></span></label></li>
 <li><label><input type="checkbox" data-p="0.5" checked><span>Thermostatische mengkraan<small>0,5 punt</small></span></label></li>
 <li><label><input type="checkbox" data-p="0.25"><span>Eenhandsmengkraan (bij de wastafel)<small>0,25 punt</small></span></label></li>
 <li><label><input type="checkbox" data-p="1"><span>Ingebouwd kastje met wastafel (wastafelmeubel)<small>1 punt</small></span></label></li>
 <li><label><input type="checkbox" data-p="0.75"><span>Kastruimte van minstens 40 × 40 cm<small>0,75 punt</small></span></label></li>
 <li><label><input type="checkbox" data-p="0.5"><span>Twee stopcontacten bij de wastafel<small>0,5 punt (0,25 per stuk)</small></span></label></li>
 <li><label><input type="checkbox" data-p="1.5"><span>Bubbelfunctie van het bad<small>1,5 punt</small></span></label></li>
</ul>
<div class="bv-uit" id="bv-wws-uit" aria-live="polite"></div>
<p class="bv-klein">Bron: Besluit betaalbare huur, Staatsblad 2024, 194, rubriek 6 Sanitair. Voorzieningen tellen mee tot maximaal het aantal punten dat de douche, het bad of de bad/douche al krijgt. Een wastafel buiten de badkamer telt maximaal 1 punt per ruimte; die zit niet in deze teller. Controleer de uitkomst altijd met de huurprijscheck van de Huurcommissie.</p>
</div>"""


JS_VERHUUR = r"""(function(){
var $=function(i){return document.getElementById(i)};if(!$('bv-wws-uit'))return;
var boxen=[].slice.call(document.querySelectorAll('#wws-sanitair input[type=checkbox]'));
function f(n){return (Math.round(n*100)/100).toString().replace('.',',')}
function reken(){
 var w=+$('bv-was').value,m=+$('bv-mp').value;if(m>w){m=w;$('bv-mp').value=w}
 $('bv-was-o').textContent=w;$('bv-mp-o').textContent=m;
 var wc=+$('bv-wc1').value+ +$('bv-wc2').value,was=(w-m)*1+m*1.5,dou=+$('bv-dou').value,vz=0;
 boxen.forEach(function(b){if(b.checked)vz+=+b.dataset.p});
 var vzt=Math.min(vz,dou),tot=wc+was+dou+vzt;
 var h='<h3>Sanitair: '+f(tot)+' punten</h3><table class="bv-tabel"><tr><td>Toilet(ten)</td><td>'+f(wc)+'</td></tr><tr><td>Wastafel(s)</td><td>'+f(was)+'</td></tr><tr><td>Douche / bad</td><td>'+f(dou)+'</td></tr><tr><td>Voorzieningen'+(vz>dou?' (afgetopt op '+f(dou)+')':'')+'</td><td>'+f(vzt)+'</td></tr></table>';
 if(vz>dou)h+='<div class="bv-uit-rij"><span class="bv-stip oranje"></span><p>Je hebt meer voorzieningen dan er mogen meetellen. Extra luxe levert hier geen punten meer op.</p></div>';
 else if(dou>0&&vz<dou)h+='<div class="bv-uit-rij"><span class="bv-stip"></span><p>Er is nog ruimte voor '+f(dou-vz)+' punt aan voorzieningen, bijvoorbeeld een handdoekenradiator of een wastafelmeubel.</p></div>';
 if(+$('bv-wc1').value===2||+$('bv-wc1').value===2.75)h+='<div class="bv-uit-rij"><span class="bv-stip"></span><p>Een toilet in een aparte toiletruimte telt 1 punt meer dan een toilet in de badkamer.</p></div>';
 $('bv-wws-uit').innerHTML=h;
}
['bv-wc1','bv-wc2','bv-was','bv-mp','bv-dou'].forEach(function(i){$(i).addEventListener('input',reken);$(i).addEventListener('change',reken)});
boxen.forEach(function(b){b.addEventListener('change',reken)});
reken();
})();"""

# ---------------------------------------------------------------------------
# Doelgroepen
# ---------------------------------------------------------------------------

def _wmo_kader():
    return f"""<div class="bv-kader">
<h2 id="wmo">Vergoeding via de gemeente (Wmo)</h2>
<p>Heb je door ouderdom of een beperking een aangepaste badkamer nodig? Dan kun je volgens de Rijksoverheid ook voor een woningaanpassing een beroep doen op de Wmo, de Wet maatschappelijke ondersteuning. Die regeling voert je eigen gemeente uit.</p>
<ul>
<li><strong>Waar vraag je het aan?</strong> Bij het Wmo-loket of het sociaal wijkteam van je gemeente. In een onderzoek, meestal een gesprek, stelt de gemeente met jou vast wat je nodig hebt.</li>
<li><strong>Eigen bijdrage.</strong> Voor sommige voorzieningen betaal je een eigen bijdrage. Het CAK heeft een rekenhulp die een indicatie geeft.</li>
<li><strong>Verhuizen in plaats van verbouwen.</strong> Sommige gemeenten geven in plaats van een vergoeding voor de aanpassing een verhuisvergoeding, bijvoorbeeld als een aanpassing heel duur is.</li>
<li><strong>Wlz-indicatie?</strong> Heb je een indicatie voor de Wet langdurige zorg en krijg je zorg thuis, dan loopt de vergoeding voor een woningaanpassing via die regeling. Ook daarvoor kun je bij de gemeente terecht.</li>
</ul>
<p><strong>Tip:</strong> de regels verschillen per gemeente. Neem contact op voordat je een opdracht geeft of begint met slopen. Wat al gedaan is, kan de gemeente vaak niet meer beoordelen.</p>
<p class="bv-klein">Bronnen: <a href="{B_WMO[1]}" rel="noopener">{B_WMO[0]}</a>, <a href="{B_WMO2[1]}" rel="noopener">{B_WMO2[0]}</a>.</p>
</div>"""


def _wws_kader():
    return f"""<div class="bv-kader">
<h2 id="wws">Huurrecht: wat het sanitair doet met de huurprijs</h2>
<p>De maximale huur van een huurwoning hangt af van het aantal punten in het woningwaarderingsstelsel (WWS). Sinds de Wet betaalbare huur (1 juli 2024) geldt dat stelsel ook voor middenhuur: woningen tot en met 186 punten. Het sanitair is één van de rubrieken.</p>
<ul>
<li><strong>Douche 4 punten, bad 6, bad/douche 7.</strong> Een toilet telt 3 punten in een aparte toiletruimte en 2 in de badkamer; een hangend toilet 3,75 en 2,75. Een wastafel telt 1 punt, een meerpersoonswastafel (minstens 70 cm breed, twee kranen) 1,5.</li>
<li><strong>Voorzieningen geven extra punten</strong>, zoals een volledige douche-afscheiding (1,25), een handdoekenradiator (0,75) en een thermostaatkraan (0,5). Ze tellen mee tot maximaal het aantal punten van de douche of het bad.</li>
<li><strong>Aanpassingen voor gehandicapten</strong> leveren 1 punt op per € 332 die de verhuurder eraan heeft besteed.</li>
</ul>
<p>De punten voor sanitair zijn maar een deel van het totaal: ook oppervlakte, energielabel en WOZ-waarde tellen mee. Een betere badkamer verhoogt de maximale huur dus beperkt. Wil je de huur na een renovatie verhogen, kijk dan ook naar de regels voor huurverhoging na woningverbetering en maak er afspraken over met je huurder.</p>
<p class="bv-klein">Bronnen: <a href="{B_WWS[1]}" rel="noopener">{B_WWS[0]}</a>, <a href="{B_HC[1]}" rel="noopener">{B_HC[0]}</a>.</p>
</div>"""


def _vve_kader():
    return """<div class="bv-kader">
<h2 id="vve">Eerst de VvE, dan de aannemer</h2>
<p>In een appartement ben je eigenaar van je eigen deel, maar zijn de constructie, de standleidingen en vaak de ventilatiekanalen van iedereen samen. In de splitsingsakte en het huishoudelijk reglement staat wat je zelf mag en waarvoor je toestemming nodig hebt.</p>
<ul>
<li><strong>Toestemming</strong> heb je meestal nodig als je aan gemeenschappelijke delen komt: leidingen in de vloer of de schacht, de dekvloer, het ventilatiekanaal of een dragende wand.</li>
<li><strong>Geluid</strong> is de bekendste bron van burenruzie. Een tegelvloer direct op beton geeft meer contactgeluid dan de oude vloer. Een goede ondervloer of een zwevende opbouw helpt.</li>
<li><strong>Afvoer</strong>: je zit vast aan de plek van de standleiding. Het toilet moet daar dichtbij blijven; een douche kun je met een goot en voldoende afschot iets verder weg zetten.</li>
<li><strong>Gewicht</strong>: tegels, een nieuwe dekvloer en een bad zijn samen zwaar. Bij een houten vloer of een oud gebouw laat je een constructeur rekenen.</li>
</ul>
<p>Lees meer in <a href="/kennisbank/verbouwen-in-vve/">verbouwen in een VvE</a>.</p>
</div>"""


GROEPEN = [
    dict(
        slug="gezinnen", naam="Gezinnen", kort="gezin",
        h1="Badkamer voor een gezin: ruim, robuust en veilig",
        seo="Gezinsbadkamer: dubbele wastafel, veilig en robuust",
        description="Een badkamer voor een gezin moet het ochtendspitsuur aankunnen. Dubbele wastafel, thermostaatkraan, robuuste materialen en drie budgetscenario's met richtprijzen.",
        kaart="Spitsuur in de ochtend, kinderen in bad en materialen die tegen een stootje kunnen.",
        chips=["Dubbele wastafel", "Kindveilige kraan", "Robuust"],
        lead="Om kwart over zeven wil iedereen tegelijk naar binnen. Een gezinsbadkamer moet vooral het spitsuur aankunnen, veilig zijn voor kinderen en jarenlang tegen water, speelgoed en haast kunnen. Dat vraagt andere keuzes dan een badkamer voor twee.",
        kort_feiten=["Spitsuur aankunnen", "Veilig voor kinderen", "Makkelijk schoon"],
        keuzes=[
            ("Dubbele wastafel", "Twee wasbakken halveren de wachtrij bij het tandenpoetsen. Je hebt een meubel van zo'n 120 cm breed nodig. Past dat niet, dan is één brede wasbak met twee kranen een tussenvorm.", "Meubel vanaf ca. 120 cm"),
            ("Thermostaatkraan", "Een thermostaatkraan houdt de temperatuur gelijk, ook als iemand anders een kraan opendraait. Kies er een met een temperatuurstop: die moet je bewust indrukken om boven ongeveer 38 °C te komen. Zo verbrandt een kind zich niet.", "Stop bij ca. 38 °C"),
            ("Apart toilet", "Zit het enige toilet in de badkamer, dan is de badkamer bezet als er iemand moet. Een apart toilet met fontein is in een gezin de grootste winst in de ochtend.", "Fontein in de toiletruimte"),
            ("Bad of grote douche", "Met kleine kinderen is een bad handig. Weinig ruimte? Een bad met douchewand combineert beide. Of kies een ruime inloopdouche en een los kinderbadje voor de eerste jaren.", "Bad 170 × 75 cm of douche 90 × 120 cm"),
            ("Robuuste materialen", "Keramische tegels in een middentint met een iets donkerdere voeg zien er na jaren nog goed uit. Grote tegels betekenen minder voegen om te poetsen. Een meubel met een gelakt of HPL-front kan beter tegen spatwater dan onbehandeld hout.", "Tegel 60 × 60 cm of groter"),
            ("Bergruimte en veiligheid", "Lades met een kindvergrendeling of een spiegelkast hoog aan de wand houden medicijnen en schoonmaakmiddel buiten bereik. Kies een stroeve vloertegel, ook buiten de douche.", "Spiegelkast op volwassen hoogte"),
        ],
        render=("d", "badkamer-renoveren"),
        render_tekst=["Een dubbel badmeubel met twee waskommen: geen wachtrij bij het tandenpoetsen.", "Een vrijstaand bad voor de kinderen en een aparte douche voor de ochtend.", "Warme tinten en hout, met tegels die vuil niet meteen laten zien."],
        tool="gezin",
        scenarios=lambda: [
            ("Slim opfrissen", "Indeling blijft. Een dubbel wastafelmeubel, een nieuwe douche met thermostaatkraan en nieuwe kit.",
             [("Wastafelmeubel dubbel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
              ("Douche met thermostaatkraan (basis)", "sanitair_douche", 1, "basis"), ("Douche plaatsen", "montage_douche", 1, None),
              ("Hele badkamer opnieuw kitten", "kitwerk_badkamer", 1, None), ("Nieuwe ventilator", "ventilator", 1, None)]),
            ("Nieuwe gezinsbadkamer", "Alles nieuw op dezelfde plek: douche, bad, dubbel meubel en hangtoilet, met 30 m² tegelwerk.",
             _basis_renovatie() + _tegels(30, "midden") + [
                 ("Douche (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Bad (basis)", "sanitair_bad", 1, "basis"), ("Bad plaatsen", "montage_bad", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Dubbel wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektra en ventilator", "elektra", 1, None)]),
            ("Ruim en anders ingedeeld", "Nieuwe indeling met bad en inloopdouche, dubbel meubel en vloerverwarming op 8 m².",
             _basis_renovatie() + [("Leidingen verplaatsen", "leidingwerk_verplaatsen", 1, None)] + _tegels(35, "midden") + [
                 ("Inloopdouche (luxe)", "sanitair_douche", 1, "luxe"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Bad (midden)", "sanitair_bad", 1, "midden"), ("Bad plaatsen", "montage_bad", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Dubbel wastafelmeubel (luxe)", "sanitair_meubel", 1, "luxe"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Vloerverwarming, 8 m²", "vloerverwarming_m2", 8, None), ("Elektra en ventilator", "elektra", 1, None)]),
        ],
        valkuilen=[
            "Een regendouche ziet er mooi uit, maar gebruikt veel meer warm water. Met vier douchers op een rij kan je boiler leeg raken.",
            "Glanzende zwarte tegels en mat zwarte kranen laten elke druppel en vingerafdruk zien.",
            "Een vrijstaand bad midden in de ruimte is lastig schoon te houden en neemt veel plek in. In een gezin is een inbouwbad met een brede rand vaak praktischer.",
            "Een te kleine ventilator: met meerdere douches achter elkaar wordt het vochtig. Laat de afzuiging op de drukte afstemmen.",
        ],
        extra="",
        links=["/badkamerspullen/wastafelmeubel-kiezen/", "/badkamerspullen/kranen-kiezen/", "/badkamerspullen/bad-of-douche/",
               "/badkamerspullen/fontein-kiezen/", "/kennisbank/water-besparen-badkamer/", "/kennisbank/grote-tegels-badkamer/",
               "/kennisbank/badkamer-schoonmaken/", "/kosten/nieuwe-badkamer/", "/kosten/tweede-badkamer/",
               "/materialen/keramische-tegels/", "/tools/indelingsplanner/", "/inspiratie/scandinavische-badkamer/"],
        bronnen=[B_MC_DOUCHE, B_MC_BADKAMER],
        faq=[
            ("Hoe breed moet een dubbel wastafelmeubel zijn?", "Reken op ongeveer 120 cm, zodat twee mensen naast elkaar kunnen staan. Vanaf 100 cm kan een brede wasbak met twee kranen. Smaller dan dat werkt een dubbele wastafel niet goed."),
            ("Wat is een kindveilige thermostaatkraan?", "Een thermostaatkraan houdt de watertemperatuur gelijk. Met een temperatuurstop gaat hij niet zomaar heter dan ongeveer 38 °C: daarvoor moet je bewust een knop indrukken. Zo verbranden kinderen zich niet."),
            ("Bad of douche voor een gezin met jonge kinderen?", "Een bad is handig voor jonge kinderen. Heb je maar ruimte voor één van de twee, dan combineert een bad met douchewand beide. Voor tieners en volwassenen is een ruime douche vaak belangrijker."),
            ("Wanneer is een tweede badkamer of toilet nodig?", "Met vier of meer mensen die in hetzelfde uur weg moeten, wordt één badkamer met het toilet erin snel krap. Een apart toilet is meestal de eerste en goedkoopste stap. Vul de spitsuur-check op deze pagina in voor een eerste idee."),
            ("Welke tegels zijn het meest praktisch in een gezinsbadkamer?", "Keramische tegels in een middentint met een iets donkerdere voeg. Grote tegels geven minder voegen om te poetsen. Kies op de vloer een stroeve tegel."),
        ],
    ),
    dict(
        slug="ouderen", naam="Ouderen", kort="levensloopbestendig",
        h1="Badkamer voor ouderen: drempelvrij en levensloopbestendig",
        seo="Badkamer voor ouderen: drempelvrij en Wmo-hulp",
        description="Een levensloopbestendige badkamer is drempelvrij, met beugels, een douchezitje en een thermostaatkraan. Met checklist, kosten en wat de Wmo van je gemeente kan betekenen.",
        kaart="Langer zelfstandig thuis: drempelvrij, beugels, zitje en hulp via de Wmo.",
        chips=["Drempelvrij", "Beugels", "Wmo"],
        lead="Wie zijn badkamer verbouwt na zijn vijftigste, verbouwt vaak voor de laatste keer. Dan loont het om nu al rekening te houden met later: geen drempels, ruimte om te draaien, steun waar je die nodig hebt. Een levensloopbestendige badkamer hoeft er niet uit te zien als een zorgbadkamer.",
        kort_feiten=["Geen drempels", "Steun en zitje", "Hulp via de gemeente"],
        keuzes=[
            ("Inloopdouche zonder drempel", "De vloer loopt door in de douche en het water loopt weg via een goot langs de wand. Geen opstap, dus geen struikelrand. Ook met een rollator of douchestoel kom je erin.", "Drempelloos, met afschot"),
            ("Beugels en verstevigde wanden", "Beugels bij de douche en het toilet geven houvast. Heb je ze nu nog niet nodig, laat dan wel de wanden verstevigen. Dan kun je later beugels monteren zonder te breken.", "Achterhout in de wand"),
            ("Douchezitje", "Een opklapbaar zitje aan de wand neemt geen ruimte in als je het niet gebruikt. Zet de douchekraan en de handdouche binnen bereik vanaf het zitje.", "Kraan bereikbaar vanuit zit"),
            ("Toilet op de juiste hoogte", "Een hangtoilet kun je op de hoogte laten plaatsen die voor jou prettig is. Gaan zitten en opstaan wordt makkelijker als het toilet iets hoger hangt dan standaard.", "Hoogte op maat"),
            ("Ruimte om te draaien", "Wil je er ooit met een rollator of rolstoel kunnen draaien, dan is een vrije ruimte van ongeveer 1,50 meter doorsnee een veelgebruikte richtmaat. Een schuifdeur of een deur die naar buiten draait helpt ook.", "Richtmaat 1,50 m"),
            ("Thermostaatkraan en goed licht", "Een thermostaatkraan voorkomt schrikken en verbranden. Goed, egaal licht en een nachtlampje of lamp met bewegingsmelder voorkomen vallen.", "Licht zonder schaduw"),
        ],
        render=("d", "inloopdouche-plaatsen"),
        render_tekst=["Een inloopdouche zonder drempel: de vloer loopt door tot in de douche.", "Een douchegoot langs de wand voert het water af, ook bij een douchestoel.", "Een glazen wand zonder deur: niets om omheen te manoeuvreren."],
        tool="ouderen",
        scenarios=lambda: [
            ("Kleine aanpassingen", "Bad of douchebak blijft. Beugels, een thermostaatkraan en een nieuw, hoger toilet.",
             [("Hangtoilet op hoogte (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
              ("Thermostaatkraan en handdouche (basis)", "sanitair_douche", 1, "basis"), ("Douchekraan plaatsen", "montage_douche", 1, None),
              ("Beugels, zitje en montage (uren loodgieter)", "uurtarief", 4, None)]),
            ("Bad eruit, inloopdouche erin", "Het bad maakt plaats voor een drempelloze inloopdouche met goot, zitje en beugels.",
             [("Slopen", "sloop", 1, None), ("Afval afvoeren", "afval", 1, None), ("Leidingwerk aanpassen", "leidingwerk", 1, None),
              ("Waterdicht maken", "waterdicht", 1, None)] + _tegels(15, "midden") + [
                 ("Inloopdouche met goot (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Beugels en zitje monteren (uren)", "uurtarief", 4, None)]),
            ("Volledig levensloopbestendig", "Nieuwe badkamer met draairuimte, inloopdouche, hoger hangtoilet, onderrijdbare wastafel en vloerverwarming.",
             _basis_renovatie() + [("Leidingen verplaatsen", "leidingwerk_verplaatsen", 1, None)] + _tegels(28, "midden") + [
                 ("Inloopdouche met goot (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafel (midden)", "sanitair_meubel", 1, "midden"), ("Wastafel plaatsen", "montage_meubel", 1, None),
                 ("Vloerverwarming, 6 m²", "vloerverwarming_m2", 6, None), ("Elektra, licht en ventilator", "elektra", 1, None)]),
        ],
        valkuilen=[
            "Gladde, glanzende vloertegels. Kies een tegel die ook nat stroef is en vraag ernaar bij de specialist.",
            "Een douchedeur die naar binnen draait. Valt er iemand in de douche, dan krijg je de deur niet meer open.",
            "Eerst verbouwen en dan pas de gemeente bellen. Vraag een Wmo-vergoeding aan voordat je een opdracht geeft.",
            "Een zitje of beugel aan een gipsplaatwand zonder versteviging. Die houdt een volwassene niet.",
        ],
        extra="wmo",
        links=["/kennisbank/inloopdouche-zonder-drempel/", "/badkamerspullen/inloopdouche-kopen/", "/badkamerspullen/douchegoot-kiezen/",
               "/badkamerspullen/toilet-kiezen/", "/kennisbank/hangtoilet-of-staand-toilet/", "/kennisbank/badkamerverlichting/",
               "/kosten/inloopdouche/", "/kosten/douche-vervangen/", "/kosten/kraan-vervangen/",
               "/inspiratie/voor-en-na/", "/tools/indelingsplanner/", "/zo-verloopt-je-verbouwing/"],
        bronnen=[B_WMO, B_WMO2],
        faq=[
            ("Wat is een levensloopbestendige badkamer?", "Een badkamer die je ook kunt blijven gebruiken als je minder mobiel wordt: zonder drempels, met een inloopdouche, ruimte om te draaien, steun bij douche en toilet en goede verlichting."),
            ("Betaalt de gemeente mee aan een aangepaste badkamer?", "Dat kan via de Wmo als je de aanpassing nodig hebt door ouderdom of een beperking. Je vraagt het aan bij het Wmo-loket of het sociaal wijkteam. De gemeente bekijkt in een gesprek wat je nodig hebt; soms betaal je een eigen bijdrage. De regels verschillen per gemeente."),
            ("Moet ik eerst de gemeente bellen of eerst offertes vragen?", "Bel eerst de gemeente als je een vergoeding wilt. Offertes vergelijken kan daarna, of tegelijk, maar geef nog geen opdracht voordat de gemeente heeft besloten."),
            ("Hoeveel ruimte heb je nodig voor een rolstoel?", "Een vrije draaicirkel van ongeveer 1,50 meter doorsnee is een veelgebruikte richtmaat. In een kleine badkamer kan het ook helpen om de douche open te laten, zodat die ruimte meetelt."),
            ("Kan ik beugels later nog plaatsen?", "Ja, als de wand sterk genoeg is. Laat bij de verbouwing achterhout of stevig plaatmateriaal in de wanden zetten op de plekken waar later beugels kunnen komen."),
        ],
    ),
    dict(
        slug="starters", naam="Starters", kort="starter",
        h1="Badkamer voor starters: slim kiezen met een krap budget",
        seo="Badkamer voor starters: slim kiezen met weinig budget",
        description="Net een huis gekocht en weinig budget over? Zo prioriteer je je badkamer: wat moet nu, wat kan later. Met budgetverdeler, drie scenario's en richtprijzen.",
        kaart="Eerste huis, krap budget: wat moet nu en wat kan later?",
        chips=["Budget", "Prioriteren", "Later uitbreiden"],
        lead="Na de aankoop van je eerste huis is het budget vaak op. De badkamer is gedateerd, maar alles tegelijk kan niet. Het goede nieuws: met de juiste volgorde krijg je nu een badkamer die werkt, en verspil je later geen geld aan dubbel werk.",
        kort_feiten=["Eerst wat je niet ziet", "Leidingen laten liggen", "Later upgraden"],
        keuzes=[
            ("Eerst wat je later niet meer kunt", "Leidingen, afvoer, waterdichting en ventilatie zitten straks achter de tegels. Daar bezuinigen kost later veel meer. Sanitair en accessoires kun je altijd nog vervangen.", "Waterdicht en ventilatie eerst"),
            ("Laat aansluitingen op hun plek", "Leidingwerk verplaatsen kost al snel duizend euro of meer. Houd de douche, het toilet en de wastafel op dezelfde plek; dat is de grootste besparing.", "Bespaart vaak € 1.000+"),
            ("Opknappen in plaats van slopen", "Zijn de tegels heel en is de badkamer droog? Dan kan opknappen genoeg zijn: nieuw kitwerk, een nieuw meubel en een nieuwe douchekraan. Lees meer over badkamer opknappen.", "Vanaf een paar honderd euro"),
            ("Middenklasse sanitair, basistegels", "Een goede douchekraan en een toilet dat goed spoelt gebruik je elke dag. Bij tegels geeft een eenvoudige witte of lichtgrijze tegel een rustig beeld voor weinig geld.", "Tegels vanaf ca. € 20 per m²"),
            ("Voorbereiden op later", "Wil je later vloerverwarming of een extra stopcontact? Laat nu een loze leiding of kabel aanleggen. Dat kost weinig en scheelt later breekwerk.", "Loze leiding nu, apparaat later"),
            ("Zelf doen wat kan", "Sloopwerk zelf doen en een container huren kan schelen. Laat leidingwerk, elektra en waterdichting over aan een vakman: fouten daarin zie je pas als het te laat is.", "Container vanaf ca. € 125"),
        ],
        render=("d", "badkamer-installeren"),
        render_tekst=["Een nieuw wastafelmeubel op de bestaande aansluitingen: snel resultaat voor weinig geld.", "Hoekstopkranen en sifon blijven op hun plek; alleen het meubel en de kraan zijn nieuw.", "Zo pak je de badkamer in stappen aan, zonder alles te slopen."],
        tool="starters",
        scenarios=lambda: [
            ("Opfrissen", "Tegels blijven. Nieuw wastafelmeubel, nieuwe douchekraan, kitwerk en ventilator.",
             [("Wastafelmeubel (basis)", "sanitair_meubel", 1, "basis"), ("Meubel plaatsen", "montage_meubel", 1, None),
              ("Douchekraan en glazen wand (basis)", "sanitair_douche", 1, "basis"), ("Douche plaatsen", "montage_douche", 1, None),
              ("Hele badkamer opnieuw kitten", "kitwerk_badkamer", 1, None), ("Nieuwe ventilator", "ventilator", 1, None)]),
            ("Nieuw op dezelfde plek", "Alles eruit en nieuw, maar de aansluitingen blijven waar ze zitten. Basis-sanitair.",
             _basis_renovatie() + _tegels(22, "basis") + [
                 ("Douche (basis)", "sanitair_douche", 1, "basis"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Toilet (basis)", "sanitair_toilet", 1, "basis"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (basis)", "sanitair_meubel", 1, "basis"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Ventilator", "ventilator", 1, None)]),
            ("Nieuw, met een paar upgrades", "Zelfde plek, midden-sanitair, hangtoilet en elektrische vloerverwarming.",
             _basis_renovatie() + _tegels(22, "midden") + [
                 ("Inloopdouche (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektrische vloerverwarming", "vloerverwarming_elektrisch", 1, None), ("Elektra en ventilator", "elektra", 1, None)]),
        ],
        valkuilen=[
            "Bezuinigen op waterdichting. Een lekkende douchehoek merk je pas als de buren of het plafond eronder nat worden.",
            "Goedkoop sanitair dat na een paar jaar lekt of slecht spoelt. Kies bij kranen en het toilet liever een middenklasse.",
            "Geen buffer. Bij oude badkamers kom je achter de tegels vaak iets tegen. Houd 10 procent van je budget achter de hand.",
            "Een offerte zonder specificatie. Vraag per post wat erin zit, zodat je ziet waar je kunt schuiven.",
        ],
        extra="",
        links=["/kosten/badkamer-opknappen/", "/kosten/kleine-badkamer/", "/kosten/wastafel-vervangen/", "/kosten/kitwerk-voegen/",
               "/kennisbank/volgorde-badkamerrenovatie/", "/kennisbank/badkamer-waterdicht-maken/", "/kennisbank/badkamer-zonder-tegels/",
               "/badkamerspullen/wastafelmeubel-kiezen/", "/badkamerspullen/badkamertegels-kopen/", "/inspiratie/kleine-badkamer/",
               "/inspiratie/voor-en-na/", "/tools/badkamercalculator/"],
        bronnen=[B_MC_BADKAMER],
        faq=[
            ("Wat kost een simpele nieuwe badkamer?", "Een badkamer van ongeveer 5 m² met basis-sanitair op dezelfde plek kost volgens onze richtprijzen een paar duizend euro tot ruim tien duizend euro, inclusief 21% btw. Op deze pagina zie je drie scenario's met de berekening erbij."),
            ("Waar kan ik het beste op besparen?", "Op het verplaatsen van leidingen, op de tegels en op luxe extra's. Niet op waterdichting, ventilatie en het vakmanschap van leidingwerk en elektra."),
            ("Kan ik de badkamer in fases aanpakken?", "Ja. Begin met wat achter de tegels zit en wat je dagelijks gebruikt. Vloerverwarming, een nieuw toilet of luxe kranen kunnen later, mits je de leidingen of kabels nu voorbereidt."),
            ("Is opknappen genoeg?", "Als de tegels heel zijn, de douchehoek droog blijft en er geen schimmel achter de kit zit, dan vaak wel. Bij lekkage, losse tegels of een muffe geur is een renovatie verstandiger."),
            ("Mag ik zelf slopen?", "Ja, dat kan in je eigen huis. Laat bij een huis van vóór 1994 eerst controleren of er asbest in kit, lijm of platen zit. Spreek met de specialist af wat jij doet en wat hij doet."),
        ],
    ),
    dict(
        slug="tweede-badkamer", naam="Tweede badkamer", kort="tweede badkamer",
        h1="Tweede badkamer: waar plaats je hem en wat kost het?",
        seo="Tweede badkamer: plek, afvoer, ventilatie en kosten",
        description="Een tweede badkamer op zolder, bij de slaapkamer of beneden? Lees wat afvoer, ventilatie en stahoogte betekenen, check je plek en bekijk drie kostenscenario's.",
        kaart="Op zolder, bij de slaapkamer of beneden: afvoer, ventilatie en kosten.",
        chips=["Plek", "Afvoer", "Ventilatie"],
        lead="Een tweede badkamer lost het ochtendspitsuur op, geeft logés of tieners een eigen plek en maakt je huis vaak aantrekkelijker bij verkoop. Of het makkelijk wordt, hangt vooral af van één ding: hoe ver de nieuwe badkamer van de afvoer ligt.",
        kort_feiten=["Afvoer bepaalt de plek", "Ventilatie is verplicht", "Warm water genoeg?"],
        keuzes=[
            ("De afvoer bepaalt de plek", "Een toilet heeft een dikke afvoer nodig en moet dicht bij de standleiding (de verticale afvoerbuis) zitten. Een douche of wastafel kan met voldoende afschot verder weg. Ligt de plek ver weg, dan is soms een vuilwaterpomp nodig.", "Toilet dicht bij de standleiding"),
            ("Ventilatie", "Elke badkamer moet vocht kwijt kunnen. Op zolder betekent dat vaak een afvoer door het dak of aansluiten op de bestaande mechanische ventilatie. Een raam alleen is meestal niet genoeg.", "Mechanische afzuiging"),
            ("Stahoogte op zolder", "Onder een schuin dak wil je bij de douche en de wastafel rechtop kunnen staan. Zet het toilet of bad onder de lage kant. Een dakkapel kan de bruikbare ruimte flink vergroten.", "Ca. 2 m bij de douche"),
            ("Warm water", "Twee mensen tegelijk douchen vraagt meer van je cv-ketel of boiler. Laat de installateur checken of je toestel dat aankan, of dat een grotere boiler nodig is.", "Check tapwaterklasse"),
            ("Compact kan prima", "Een tweede badkamer hoeft niet groot. Een douche, een kleine wastafel en eventueel een toilet passen al op 2 tot 3 m². Een fontein in plaats van een wastafel scheelt ruimte.", "Vanaf ca. 2 m²"),
            ("Geluid en vloer", "Afvoer en toilet boven een slaap- of woonkamer hoor je. Laat leidingen isoleren. Op een houten vloer is een stijve, waterdichte ondergrond nodig, zeker onder een bad.", "Leidingen geïsoleerd"),
        ],
        render=("s", "kleine-badkamer"),
        render_tekst=["Een compacte badkamer van ongeveer 1,8 bij 2,2 meter: genoeg voor een tweede badkamer.", "Inloopdouche met helder glas, wastafel en hangtoilet op een kleine ruimte.", "Lichte tegels laten de ruimte groter lijken."],
        tool="tweede",
        scenarios=lambda: [
            ("Douche en wastafel", "Compacte doucheruimte dicht bij de bestaande afvoer, bijvoorbeeld bij een slaapkamer.",
             [("Leidingwerk", "leidingwerk", 1, None), ("Waterdicht maken", "waterdicht", 1, None)] + _tegels(16, "basis") + [
                 ("Douche (basis)", "sanitair_douche", 1, "basis"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Wastafelmeubel (basis)", "sanitair_meubel", 1, "basis"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektra", "elektra", 1, None), ("Ventilator", "ventilator", 1, None)]),
            ("Complete tweede badkamer", "Douche, wastafel en hangtoilet, met een nieuwe afvoer naar de standleiding.",
             [("Leidingwerk", "leidingwerk", 1, None), ("Nieuwe afvoer en aanvoer", "leidingwerk_verplaatsen", 1, None),
              ("Waterdicht maken", "waterdicht", 1, None)] + _tegels(20, "midden") + [
                 ("Inloopdouche (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektra", "elektra", 1, None), ("Ventilator", "ventilator", 1, None)]),
            ("Ruime zolderbadkamer", "Met bad, inloopdouche, toilet en vloerverwarming. Zonder dakkapel of nieuwe wanden.",
             [("Leidingwerk", "leidingwerk", 1, None), ("Nieuwe afvoer en aanvoer", "leidingwerk_verplaatsen", 1, None),
              ("Waterdicht maken", "waterdicht", 1, None)] + _tegels(30, "midden") + [
                 ("Inloopdouche (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Bad (midden)", "sanitair_bad", 1, "midden"), ("Bad plaatsen", "montage_bad", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Vloerverwarming, 7 m²", "vloerverwarming_m2", 7, None), ("Elektra", "elektra", 1, None), ("Ventilator", "ventilator", 1, None)]),
        ],
        valkuilen=[
            "Geen rekening houden met bouwkundig werk. Wanden, een nieuwe vloer of een dakkapel komen bovenop de kosten van de badkamer zelf.",
            "Te weinig afschot naar de afvoer. Dan blijft water staan of gaat de afvoer ruiken.",
            "Een badkamer onder het dak zonder goede afzuiging. Het vocht slaat neer in het dakbeschot.",
            "Vergeten te checken of de cv-ketel of boiler twee douches tegelijk aankan.",
        ],
        extra="",
        links=["/kosten/tweede-badkamer/", "/kosten/badkamer-ventilatie/", "/kosten/kleine-badkamer/", "/kosten/uurtarief-loodgieter/",
               "/kennisbank/badkamer-en-suite/", "/kennisbank/badkamer-ventilatie/", "/kennisbank/kleine-badkamer-indelen/",
               "/badkamerspullen/fontein-kiezen/", "/badkamerspullen/inbouwreservoir-kiezen/", "/badkamerspullen/douchewand-kiezen/",
               "/inspiratie/kleine-badkamer/", "/tools/indelingsplanner/"],
        bronnen=[B_MC_BADKAMER],
        faq=[
            ("Waar plaats je een tweede badkamer het beste?", "Zo dicht mogelijk bij de bestaande afvoer, bijvoorbeeld boven of naast de huidige badkamer of keuken. Dat scheelt leidingwerk. Op zolder let je ook op de stahoogte en de ventilatie."),
            ("Wat kost een tweede badkamer?", "Van een paar duizend euro voor een eenvoudige doucheruimte tot ruim twintigduizend euro voor een complete zolderbadkamer met bad, inclusief 21% btw en zonder bouwkundig werk. Op deze pagina staan drie scenario's met de berekening."),
            ("Kan een toilet ver van de afvoer?", "Een toilet moet met een dikke buis en voldoende afschot op de standleiding aansluiten. Lukt dat niet, dan kan een vuilwaterpomp (een fecaliënpomp) een oplossing zijn. Die maakt geluid en vraagt onderhoud."),
            ("Heb ik een vergunning nodig voor een badkamer op zolder?", "Voor een badkamer binnen je huis meestal niet. Voor een dakkapel soms wel; dat hangt af van de plek en je gemeente. Woon je in een appartement, dan heb je vaak toestemming van de VvE nodig."),
            ("Is een tweede badkamer zijn geld waard?", "Dat hangt af van je gezin en je huis. Vooral in grotere gezinnen en bij huizen met meerdere slaapkamers op verschillende verdiepingen is het een gewilde voorziening. Een apart toilet is een goedkopere eerste stap."),
        ],
    ),
    dict(
        slug="appartementen", naam="Appartementen", kort="appartement",
        h1="Badkamer in een appartement: VvE, geluid, afvoer en gewicht",
        seo="Badkamer in een appartement: VvE, geluid en afvoer",
        description="Een badkamer verbouwen in een appartement? Denk aan toestemming van de VvE, geluid naar de buren, de vaste afvoer en het gewicht. Met VvE-check en drie kostenscenario's.",
        kaart="Toestemming van de VvE, geluid naar de buren, vaste afvoer en gewicht.",
        chips=["VvE", "Geluid", "Afvoer"],
        lead="In een appartement deel je muren, vloeren en leidingen met je buren. Dat maakt een badkamerverbouwing net wat anders: je hebt vaak toestemming van de VvE nodig, je zit vast aan de standleiding en wat jij in je badkamer doet, hoort de buurman onder je.",
        kort_feiten=["Toestemming VvE", "Geluid naar beneden", "Vaste standleiding"],
        keuzes=[
            ("Toestemming van de VvE", "Kom je aan leidingen, de dekvloer, ventilatie of een wand, dan heb je meestal schriftelijk toestemming nodig. Vraag het ruim op tijd aan; sommige VvE's beslissen alleen in de jaarvergadering.", "Splitsingsakte en reglement"),
            ("Geluid", "Een tegelvloer direct op beton geeft meer contactgeluid. Een akoestische ondervloer of een zwevende dekvloer beperkt dat. Laat ook afvoerleidingen in schachten en wanden isoleren.", "Ontkoppelde opbouw"),
            ("Vaste afvoer", "De standleiding zit waar hij zit. Het toilet blijft daar dichtbij. Een inloopdouche met goot kan iets verder weg, maar vraagt afschot, en dat kost vloerhoogte.", "Toilet bij de standleiding"),
            ("Vloerhoogte en drempel", "Voor een drempelloze douche heb je ruimte nodig voor afschot en goot. In een betonvloer kun je niet zomaar dieper. Een verhoogde vloer of een dunne goot kan een oplossing zijn.", "Afschot ca. 1 tot 2%"),
            ("Gewicht", "Een gevuld bad weegt honderden kilo's. Een nieuwe dekvloer en natuursteen tellen ook mee. In een oud gebouw of op een houten vloer laat je een constructeur rekenen.", "Gevuld bad: 300+ kg"),
            ("Ventilatie op het gezamenlijke kanaal", "Veel appartementen hebben centrale mechanische afzuiging. Daar mag je meestal geen eigen motor op aansluiten, want dat verstoort de ventilatie bij je buren.", "Ventielen, geen eigen motor"),
        ],
        render=("d", "zakelijk-badkamers"),
        render_tekst=["Een functionele appartementsbadkamer: inloopdouche, zwevend meubel en hangtoilet.", "Alles op de muur: de vloer blijft vrij en is makkelijk schoon te houden.", "Een donkere accentwand geeft sfeer zonder extra vloerhoogte of gewicht."],
        tool="appartement",
        scenarios=lambda: [
            ("Vervangen op dezelfde plek", "Geen werk aan de vloer of leidingen in de schacht. Nieuw sanitair en kitwerk.",
             [("Douche (basis)", "sanitair_douche", 1, "basis"), ("Douche plaatsen", "montage_douche", 1, None),
              ("Wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
              ("Toilet (basis)", "sanitair_toilet", 1, "basis"), ("Toilet plaatsen", "montage_toilet", 1, None),
              ("Hele badkamer opnieuw kitten", "kitwerk_badkamer", 1, None)]),
            ("Nieuwe badkamer, zelfde indeling", "Alles nieuw, aansluitingen blijven bij de standleiding. Met akoestische opbouw en 20 m² tegels.",
             _basis_renovatie() + _tegels(20, "midden") + [
                 ("Inloopdouche (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektra", "elektra", 1, None)]),
            ("Nieuwe indeling", "Douche verplaatst, nieuwe dekvloer met elektrische vloerverwarming, midden- tot luxe-sanitair.",
             _basis_renovatie() + [("Leidingen verplaatsen", "leidingwerk_verplaatsen", 1, None)] + _tegels(22, "luxe") + [
                 ("Inloopdouche (luxe)", "sanitair_douche", 1, "luxe"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Hangtoilet (midden)", "sanitair_toilet", 1, "midden"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (luxe)", "sanitair_meubel", 1, "luxe"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektrische vloerverwarming", "vloerverwarming_elektrisch", 1, None), ("Elektra", "elektra", 1, None)]),
        ],
        valkuilen=[
            "Beginnen zonder toestemming. De VvE kan je laten terugbrengen wat je zonder akkoord hebt veranderd.",
            "Een eigen afzuigmotor op het gezamenlijke ventilatiekanaal. Dat kan de afzuiging bij je buren verstoren.",
            "Geen rekening houden met werktijden en de lift. Veel VvE's hebben regels voor lawaai en het afvoeren van puin.",
            "Vergeten de buren in te lichten. Een briefje vooraf voorkomt veel ergernis tijdens het breekwerk.",
        ],
        extra="vve",
        links=["/kennisbank/verbouwen-in-vve/", "/kennisbank/badkamer-ventilatie/", "/kennisbank/asbest-in-badkamer/",
               "/kennisbank/inloopdouche-zonder-drempel/", "/badkamerspullen/douchegoot-kiezen/", "/badkamerspullen/inbouwreservoir-kiezen/",
               "/badkamerspullen/vrijstaand-bad-kopen/", "/kosten/nieuwe-badkamer/", "/kosten/vloerverwarming-badkamer/",
               "/kosten/badkamer-ventilatie/", "/inspiratie/moderne-badkamer/", "/tools/renovatieplanner/"],
        bronnen=[B_MC_BADKAMER],
        faq=[
            ("Heb ik toestemming van de VvE nodig voor een nieuwe badkamer?", "Vaak wel als je aan gemeenschappelijke delen komt, zoals leidingen in de schacht, de dekvloer of het ventilatiekanaal. Alleen sanitair op dezelfde plek vervangen kan meestal zonder. Wat precies geldt, staat in de splitsingsakte en het huishoudelijk reglement."),
            ("Hoe voorkom ik geluidsoverlast voor de buren?", "Met een akoestische ondervloer of een zwevende dekvloer, geïsoleerde afvoerleidingen en een toilet dat aan een goed bevestigde voorzetwand hangt. Vraag welke eisen jouw VvE stelt."),
            ("Kan ik mijn toilet verplaatsen in een appartement?", "Alleen een klein stukje. Het toilet moet met een dikke afvoer en afschot op de standleiding aansluiten, en in een betonvloer is weinig ruimte voor een lange leiding."),
            ("Mag een vrijstaand bad in een appartement?", "Dat kan, maar een gevuld bad weegt al snel 300 kilo of meer op een kleine oppervlakte. Laat in een oud gebouw of bij een houten vloer een constructeur rekenen, en vraag de VvE om toestemming."),
            ("Mag ik een badkamerventilator op het kanaal aansluiten?", "In appartementen met centrale afzuiging meestal niet met een eigen motor. Je krijgt dan een ventiel op het kanaal. Vraag het na bij je VvE."),
        ],
    ),
    dict(
        slug="verhuurders", naam="Verhuurders", kort="verhuur",
        h1="Badkamer voor een huurwoning: duurzaam en onderhoudsarm",
        seo="Badkamer voor verhuur: onderhoudsarm en WWS-punten",
        description="Een badkamer in een huurwoning moet lang meegaan, weinig onderhoud vragen en past in het woningwaarderingsstelsel. Met WWS-puntenteller voor sanitair, kosten en bronnen.",
        kaart="Lang meegaan, weinig onderhoud en wat het sanitair doet met de WWS-punten.",
        chips=["Onderhoudsarm", "WWS-punten", "Duurzaam"],
        lead="Als verhuurder kijk je anders naar een badkamer dan een bewoner. Hij moet tien tot vijftien jaar mee, weinig klachten opleveren, makkelijk te repareren zijn en passen bij de huur die je mag vragen. Het woningwaarderingsstelsel bepaalt wat het sanitair aan punten oplevert.",
        kort_feiten=["Lang meegaan", "Weinig klachten", "Punten in het WWS"],
        keuzes=[
            ("Standaard onderdelen", "Kies sanitair en kranen met onderdelen die je over tien jaar nog kunt krijgen. Een standaard douchekraan en een gangbaar inbouwreservoir zijn makkelijker te repareren dan een designer-model.", "Gangbare maten"),
            ("Weinig voegen, weinig kit", "Grote keramische tegels en een iets donkere voeg verkleinen de kans op vieze voegen en klachten over schimmel. Kit is onderhoud: hoe minder meters, hoe beter.", "Tegel 60 × 60 cm of groter"),
            ("Ventilatie die niemand uitzet", "Schimmel is de meest gehoorde klacht. Een ventilator met vochtsensor of nalooptijd blijft werken, ook als de huurder vergeet hem aan te zetten.", "Vochtsensor of nalooptijd"),
            ("Zuinig met water", "Een waterbesparende douchekop (tot 7,2 liter per minuut) en een toilet met spaarspoeling verlagen de kosten voor de huurder. Dat maakt de woning aantrekkelijker.", "Douchekop tot 7,2 l/min"),
            ("Punten waar het kan", "Een volledige douche-afscheiding, een thermostaatkraan, een handdoekenradiator en een wastafelmeubel leveren punten op in het WWS. Ze tellen mee tot het aantal punten van de douche of het bad.", "Max. = punten douche/bad"),
            ("Robuust boven luxe", "Een vrijstaand bad of regendouche levert weinig extra punten op en meer onderhoud. Een goede inloopdouche met glazen wand is voor de meeste huurders genoeg.", "Douche: 4 punten"),
        ],
        render=("d", "badkamer-onderhoud"),
        render_tekst=["Strakke kitranden en schone voegen: zo blijft een huurbadkamer jaren netjes.", "Grote tegels betekenen minder voegen om te onderhouden.", "Goede kit en een droge douchehoek voorkomen de meeste klachten."],
        tool="verhuur",
        scenarios=lambda: [
            ("Opknappen tussen twee huurders", "Kitwerk, nieuwe ventilator met vochtsensor, nieuwe douchekraan en wastafelmeubel.",
             [("Hele badkamer opnieuw kitten", "kitwerk_badkamer", 1, None), ("Ventilator", "ventilator", 1, None),
              ("Douchekraan en wand (basis)", "sanitair_douche", 1, "basis"), ("Douche plaatsen", "montage_douche", 1, None),
              ("Wastafelmeubel (basis)", "sanitair_meubel", 1, "basis"), ("Meubel plaatsen", "montage_meubel", 1, None)]),
            ("Onderhoudsarme renovatie", "Alles nieuw op dezelfde plek, basis- tot middenklasse, grote tegels en een hangtoilet.",
             _basis_renovatie() + _tegels(22, "basis") + [
                 ("Douche met glazen wand (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Hangtoilet (basis)", "sanitair_toilet", 1, "basis"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (basis)", "sanitair_meubel", 1, "basis"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektra en ventilator", "elektra", 1, None)]),
            ("Renovatie met extra punten", "Als scenario 2, met bad/douche-combinatie en vloerverwarming, voor een grotere woning.",
             _basis_renovatie() + _tegels(26, "midden") + [
                 ("Douche met glazen wand (midden)", "sanitair_douche", 1, "midden"), ("Douche plaatsen", "montage_douche", 1, None),
                 ("Bad (basis)", "sanitair_bad", 1, "basis"), ("Bad plaatsen", "montage_bad", 1, None),
                 ("Hangtoilet (basis)", "sanitair_toilet", 1, "basis"), ("Toilet plaatsen", "montage_toilet", 1, None),
                 ("Wastafelmeubel (midden)", "sanitair_meubel", 1, "midden"), ("Meubel plaatsen", "montage_meubel", 1, None),
                 ("Elektrische vloerverwarming", "vloerverwarming_elektrisch", 1, None), ("Elektra en ventilator", "elektra", 1, None)]),
        ],
        valkuilen=[
            "Verwachten dat een dure badkamer veel meer huur oplevert. De punten voor sanitair zijn beperkt en de voorzieningen zijn afgetopt.",
            "Renoveren met de huurder er nog in zonder afspraken. Spreek vooraf af hoe lang het duurt, waar de huurder kan douchen en wat er met de huur gebeurt.",
            "Kitwerk niet in het onderhoudsplan. Kit gaat ongeveer vijf tot tien jaar mee; daarna begint de schimmel.",
            "Exotische materialen zoals natuursteen of microcement in een huurwoning: mooi, maar gevoelig voor verkeerde schoonmaakmiddelen.",
        ],
        extra="wws",
        links=["/kennisbank/badkamer-schoonmaken/", "/kennisbank/garantie-badkamerrenovatie/", "/kennisbank/badkamer-ventilatie/",
               "/kennisbank/water-besparen-badkamer/", "/badkamerspullen/douchewand-kiezen/", "/badkamerspullen/badkamerradiator-kiezen/",
               "/badkamerspullen/kranen-kiezen/", "/kosten/kitwerk-voegen/", "/kosten/badkamer-opknappen/",
               "/materialen/voegen-en-kit/", "/materialen/meubelmaterialen/", "/inspiratie/industriele-badkamer/"],
        bronnen=[B_WWS, B_HC, B_MC_DOUCHE],
        faq=[
            ("Hoeveel WWS-punten levert een badkamer op?", "Een douche telt 4 punten, een bad 6 en een bad/douche 7. Een toilet telt 3 punten in een aparte toiletruimte en 2 in de badkamer (hangend 3,75 en 2,75), een wastafel 1 punt. Voorzieningen zoals een douche-afscheiding, handdoekenradiator en thermostaatkraan geven extra punten, tot maximaal het aantal punten van de douche of het bad. Bron: Staatsblad 2024, 194."),
            ("Geldt het puntenstelsel ook voor middenhuur?", "Ja. Sinds de Wet betaalbare huur (1 juli 2024) geldt het woningwaarderingsstelsel ook voor woningen tot en met 186 punten. Daarboven is het een vrije-sectorwoning."),
            ("Welke materialen zijn het meest onderhoudsarm?", "Grote keramische tegels met een iets donkere voeg, een hangtoilet, een glazen douchewand met een coating en een meubel met een kunststof of gelakt front. Een ventilator met vochtsensor voorkomt de meeste schimmelklachten."),
            ("Mag ik de huur verhogen na een nieuwe badkamer?", "Door extra voorzieningen kan het puntenaantal en dus de maximale huur stijgen. Of en hoe je de huur verhoogt, hangt af van je huurcontract en de regels voor huurverhoging na woningverbetering. Maak er vooraf afspraken over met je huurder."),
            ("Hoe lang gaat een badkamer in een huurwoning mee?", "Een goed aangelegde badkamer gaat vaak vijftien jaar of langer mee. Kitwerk en de ventilator hebben eerder onderhoud nodig. Neem die op in je onderhoudsplan."),
        ],
    ),
]

TOOLS = {
    "gezin": (lambda: TOOL_GEZIN, JS_GEZIN),
    "ouderen": (_tool_ouderen, JS_OUDEREN),
    "starters": (_tool_starters, JS_STARTERS),
    "tweede": (_tool_tweede, JS_TWEEDE),
    "appartement": (_tool_appartement, JS_APPARTEMENT),
    "verhuur": (_tool_verhuur, JS_VERHUUR),
}
EXTRA = {"": lambda: "", "wmo": _wmo_kader, "wws": _wws_kader, "vve": _vve_kader}

LINKS = [(PAD, "Badkamer voor wie?", "Kies je situatie: gezin, ouderen, starters, tweede badkamer, appartement of verhuur.")] + [
    (f"{PAD}{g['slug']}/", f"Badkamer voor {g['naam'].lower()}" if g["slug"] != "tweede-badkamer" else "Tweede badkamer",
     g["kaart"]) for g in GROEPEN]


def _render(g):
    soort, sleutel = g["render"]
    return RENDERS[sleutel] if soort == "d" else RENDERS_STIJL[sleutel]


def _groep_pagina(g, write, today):
    url = f"{PAD}{g['slug']}/"
    cr, cr_ld = crumbs([("Home", "/"), ("Badkamer voor wie?", PAD), (g["naam"], None)])
    r = _render(g)
    keuzes = "".join(f'<div class="bv-keuze"><h3>{t}</h3><p>{p}</p><span class="bv-maat">{m}</span></div>'
                     for t, p, m in g["keuzes"])
    kort = "".join(f"<li>{x}</li>" for x in g["kort_feiten"])
    zo = "".join(f"<li>{x}</li>" for x in g["render_tekst"])
    tool_html_f, tool_js = TOOLS[g["tool"]]
    scen_html, _ = _scenarios_html(g["scenarios"](), "Bedragen afgerond op honderden euro's.")
    valk = "".join(f"<li>{v}</li>" for v in g["valkuilen"])
    verder = "".join(_kaart(p) for p in g["links"])
    andere = "".join(f'<a href="{PAD}{o["slug"]}/">{_svg(ICONEN[o["slug"]], 24)}{o["naam"]}</a>'
                     for o in GROEPEN if o["slug"] != g["slug"])
    bronnen = "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in g["bronnen"])
    faq_html, faq_ld = faq_blok(g["faq"], f"Veelgestelde vragen: badkamer voor {g['naam'].lower()}"
                                if g["slug"] != "tweede-badkamer" else "Veelgestelde vragen over een tweede badkamer")
    klus = {"gezinnen": "je gezinsbadkamer", "ouderen": "een aangepaste badkamer", "starters": "je badkamer",
            "tweede-badkamer": "een tweede badkamer", "appartementen": "je appartementsbadkamer",
            "verhuurders": "een huurbadkamer"}[g["slug"]]

    body = f"""{CSS}{cr}
<article class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Badkamer voor wie? · {g['naam']}</span>
  <h1>{g['h1']}</h1>
  <p class="lead">{g['lead']}</p>
  <ul class="bv-kort">{kort}</ul>

  <h2 id="keuzes">Waar het voor jou om draait</h2>
  <div class="bv-keuzes">{keuzes}</div>

  <div class="bv-zo">
    {render_beeld(r, "(max-width: 700px) 100vw, 460px")}
    <div><h2>Zo ziet het eruit</h2><ul class="checklist">{zo}</ul>
    <p class="bv-klein">Illustratie (3D-render), geen foto van een bestaande badkamer.</p></div>
  </div>

  {tool_html_f()}

  {EXTRA[g['extra']]()}

  <h2 id="budget">Drie budgetscenario's</h2>
  <p>Wat het kost, hangt af van hoeveel je verandert. Deze drie scenario's laten de bandbreedte zien. Klik op "Zo is het opgeteld" om per post te zien wat erin zit.</p>
  {scen_html}

  {offertecheck_blok(klus)}

  <h2 id="valkuilen">Valkuilen</h2>
  <ul>{valk}</ul>

  {cta_midden("Offertes vergelijken voor " + klus + "?", "Beschrijf je situatie en ontvang gratis offertes van maximaal drie badkamerspecialisten uit je regio. Jij kiest, wij krijgen een vergoeding van de specialist.")}

  <h2 id="verder">Verder lezen</h2>
  <div class="bv-verder">{verder}</div>

  <h2 id="bronnen">Bronnen</h2>
  <p class="bv-bronnen">Geraadpleegd in november 2026. De bedragen zijn richtprijzen inclusief 21% btw; de bronnen per prijs staan onder de scenario's.</p>
  <ul class="bv-bronnen">{bronnen}</ul>

  <h2 id="andere">Badkamer voor een andere situatie</h2>
  <div class="bv-andere">{andere}</div>
</div></article>
{faq_html}
{cta_blok("Klaar voor de volgende stap?", "Vul in een minuut het formulier in en ontvang vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio. De aanvraag is gratis.")}
<script>{tool_js}</script>"""

    art_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": g["h1"], "description": g["description"], "inLanguage": "nl-NL",
        "datePublished": GEPUBLICEERD, "dateModified": today,
        "image": {"@type": "ImageObject", "url": f"{SITE['url']}/assets/fotos/renders/{r['naam']}-1600.webp",
                  "width": r["w"], "height": r["h"], "caption": "Illustratie (3D-render)"},
        "author": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "publisher": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "mainEntityOfPage": SITE["url"] + url,
        "isPartOf": {"@type": "CollectionPage", "@id": SITE["url"] + PAD},
        "citation": [u for _, u in g["bronnen"]],
    }
    write(url, page(title(g["seo"]), g["description"], url, body, [cr_ld, art_ld, faq_ld]), prio=0.7)


def _kiezer(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Badkamer voor wie?", None)])
    kaarten = ""
    for i, g in enumerate(GROEPEN):
        r = _render(g)
        n = r["naam"]
        laden = 'loading="eager"' if i < 2 else 'loading="lazy"'
        chips = "".join(f"<li>{c}</li>" for c in g["chips"])
        titel = f"Voor {g['naam'].lower()}" if g["slug"] != "tweede-badkamer" else "Een tweede badkamer"
        kaarten += (f'<a class="bv-kies" href="{PAD}{g["slug"]}/">'
                    f'<figure class="bv-kies-beeld" style="margin:0"><img src="/assets/fotos/renders/{n}-400.webp" '
                    f'srcset="/assets/fotos/renders/{n}-400.webp 400w, /assets/fotos/renders/{n}-800.webp 800w" '
                    f'sizes="(max-width: 700px) 100vw, (max-width: 900px) 50vw, 360px" width="{r["w"]}" height="{r["h"]}" '
                    f'alt="" {laden} decoding="async"><figcaption>Illustratie (3D-render)</figcaption>'
                    f'<span class="bv-kies-ic">{_svg(ICONEN[g["slug"]], 34)}</span></figure>'
                    f'<div class="bv-kies-tekst"><h2>{titel}</h2><p>{g["kaart"]}</p><ul>{chips}</ul>'
                    f'<span class="bv-go">Bekijk advies en kosten →</span></div></a>')
    faqs = [
        ("Waarom verschilt een badkamer per situatie?", "Een gezin heeft vooral last van het ochtendspitsuur, iemand van 70 wil drempelvrij, een starter heeft weinig budget en in een appartement beslist de VvE mee. Daarom krijg je per situatie andere keuzes, andere valkuilen en andere budgetscenario's."),
        ("Passen meerdere situaties bij mij?", "Dat kan, bijvoorbeeld als je met je gezin in een appartement woont of als je als verhuurder een levensloopbestendige woning wilt. Lees dan beide pagina's; de VvE-regels en de Wmo gelden naast elkaar."),
        ("Kloppen de prijzen op deze pagina's?", "Het zijn richtprijzen inclusief 21% btw, opgeteld per post uit dezelfde bronnen als onze kostenpagina's (Homedeal, Trustoo, Werkspot en Slimster). Je eigen offerte kan hoger of lager uitkomen."),
        ("Voeren jullie het werk zelf uit?", "Nee. Wij brengen je gratis in contact met maximaal drie badkamerspecialisten uit je regio. Zij maken een offerte; wij krijgen een vergoeding van de specialist."),
    ]
    faq_html, faq_ld = faq_blok(faqs)
    body = f"""{CSS}{cr}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose">
    <span class="badge">Badkamer voor wie?</span>
    <h1>Voor wie is je badkamer?</h1>
    <p class="lead">Een badkamer voor een druk gezin vraagt andere keuzes dan een badkamer voor later, een eerste huis of een huurwoning. Kies je situatie en zie wat voor jou telt, met een rekenhulp, drie budgetscenario's en de valkuilen.</p>
  </div>
  <div class="bv-kiezer">{kaarten}</div>
  <div class="narrow prose" style="margin-top:42px">
    <h2>Niet zeker waar je begint?</h2>
    <p>Begin bij wat je badkamer moet kunnen, niet bij hoe hij eruitziet. Hoeveel mensen gebruiken hem, en wanneer? Moet je er over twintig jaar nog in kunnen douchen? Wat is je budget, en wat mag later? Met die antwoorden kies je makkelijker tegels en sanitair.</p>
    <p>Zoek je eerst ideeën, kijk dan bij de <a href="/inspiratie/">badkamerstijlen</a>. Wil je weten wat een badkamer kost, lees <a href="/kosten/nieuwe-badkamer/">wat een nieuwe badkamer kost</a> of reken je eigen badkamer door met de <a href="/tools/badkamercalculator/">badkamercalculator</a>. Hoe een verbouwing stap voor stap gaat, lees je in <a href="/zo-verloopt-je-verbouwing/">zo verloopt je verbouwing</a>.</p>
  </div>
</div></section>
{faq_html}
{cta_blok("Offertes vergelijken?", "Beschrijf je situatie in een minuut en ontvang gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio.")}"""
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE["url"] + f"{PAD}{g['slug']}/", "name": g["h1"]}
             for i, g in enumerate(GROEPEN)]
    lijst_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE["url"] + PAD,
                "name": "Voor wie is je badkamer?", "inLanguage": "nl-NL",
                "mainEntity": {"@type": "ItemList", "itemListElement": items}}
    write(PAD, page(title("Badkamer voor wie? Advies per situatie"),
                    "Badkamer voor een gezin, ouderen, starters, een tweede badkamer, een appartement of verhuur. Per situatie de keuzes, een rekenhulp en drie budgetscenario's.",
                    PAD, body, [cr_ld, lijst_ld, faq_ld]), prio=0.8)


def build(write):
    today = datetime.date.today().isoformat()
    for g in GROEPEN:
        _groep_pagina(g, write, today)
    _kiezer(write)
