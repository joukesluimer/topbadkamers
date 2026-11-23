# -*- coding: utf-8 -*-
"""
Badkamerstijl-kiezer (/tools/stijlkiezer/).

Alles van deze tool staat in dit ene bestand: de keuzes, de getekende badkamer
(inline SVG, vooraanzicht), de pagina, de CSS en de JavaScript. build.py roept
alleen build(write) aan.

Hoe het werkt: elke wand- en vloertegel is een SVG-<pattern>, elke kraankleur een
<linearGradient> en elk meubel een <pattern>. De JavaScript zet alleen het
fill-attribuut van een paar vlakken om naar een ander patroon. Het type douche is
een groep die wordt getoond of verborgen. Er staan geen prijzen op deze pagina,
dus er zijn ook geen prijsbronnen nodig.
"""

import json

from components import page, crumbs, faq_blok, cta_blok, title, desc
from data import SITE

PAD = "/tools/stijlkiezer/"

LINKS = [
    (PAD, "Badkamerstijl-kiezer",
     "Wissel live tegels, kraankleur, meubel, douche en licht in een getekende badkamer."),
]

# ---------------------------------------------------------------------------
# Keuzes: (id, naam, korte uitleg, css-staal voor de knop)
# ---------------------------------------------------------------------------

WANDEN = [
    ("wit", "Wit glans", "Witte tegel van 20 × 20 cm met glans. Licht, makkelijk schoon te houden en tijdloos.",
     "linear-gradient(135deg,#fff 0 45%,#e9eef1 46% 54%,#fff 55%)"),
    ("beton", "Beton-look", "Grote grijze tegel die op beton lijkt. Weinig voegen en een rustig, strak vlak.",
     "radial-gradient(circle at 30% 40%,#c5c4be 0 8%,transparent 9%),#b4b3ad"),
    ("zellige", "Groen zellige", "Kleine handgemaakte tegel met kleurverschil per stuk. Levendig en ambachtelijk.",
     "conic-gradient(#2f6b55 0 25%,#47866b 0 50%,#2a604c 0 75%,#3b7a61 0)"),
    ("terrazzo", "Terrazzo", "Lichte tegel met steenslag in verschillende kleuren. Speels en vergeeflijk voor vlekken.",
     "radial-gradient(circle at 30% 30%,#c9774f 0 9%,transparent 10%),radial-gradient(circle at 70% 65%,#5b5f63 0 8%,transparent 9%),#ece6dc"),
    ("metro", "Metrotegel halfsteens", "Langwerpige tegel in halfsteens verband, zoals in een metrostation. Klassiek en rustig.",
     "repeating-linear-gradient(0deg,#cfc9be 0 2px,#f4f2ed 2px 12px)"),
    ("visgraat", "Metrotegel visgraat", "Dezelfde langwerpige tegel, maar schuin in visgraat gelegd. Geeft beweging aan de wand.",
     "repeating-linear-gradient(45deg,#cfc9be 0 2px,#f4f2ed 2px 10px),#f4f2ed"),
]

VLOEREN = [
    ("antraciet", "Antraciet 60 × 60", "Donkere grote tegel. Strak, en vuil valt er weinig op.",
     "#4a4d50"),
    ("betonvloer", "Beton-look lichtgrijs", "Lichtgrijze tegel van 60 × 120 cm. Weinig voegen, dus de ruimte oogt groter.",
     "#bdbcb6"),
    ("hout", "Houtlook visgraat", "Keramische tegel met een houtprint, in visgraat gelegd. De warmte van hout, maar waterbestendig.",
     "repeating-linear-gradient(45deg,#a87a4c 0 6px,#c39461 6px 12px)"),
    ("marmer", "Marmerlook wit", "Witte tegel met grijze aders. Chique, vooral met goud- of messingkleurige kranen.",
     "linear-gradient(120deg,#f4f3f1 0 40%,#cfcfcf 41% 43%,#f4f3f1 44%)"),
    ("cement", "Cementtegel-look", "Tegel met een zwart-wit patroon in de stijl van oude cementtegels. Een blikvanger.",
     "conic-gradient(#2d3135 0 25%,#ecebe6 0 50%,#2d3135 0 75%,#ecebe6 0)"),
    ("terrazzovloer", "Terrazzo", "Dezelfde terrazzo als op de wand, nu op de vloer. Mooi bij een effen wand.",
     "radial-gradient(circle at 30% 30%,#c9774f 0 9%,transparent 10%),radial-gradient(circle at 70% 65%,#5b5f63 0 8%,transparent 9%),#ece6dc"),
]

KRANEN = [
    ("chroom", "Chroom", "Glanzend en het meest verkocht. Past bij bijna elke stijl; kalk en vingers zie je wel snel.",
     "linear-gradient(135deg,#f5f7f9,#9aa3ab 50%,#e9edf0)"),
    ("zwart", "Mat zwart", "Strak contrast tegen lichte tegels. Kalkvlekken vallen op, dus droog na gebruik even af.",
     "linear-gradient(135deg,#3a3a3a,#111 50%,#2a2a2a)"),
    ("goud", "Goud of messing", "Warm en opvallend. Mooi bij groen, terrazzo en marmerlook.",
     "linear-gradient(135deg,#f3d58a,#b88a35 50%,#e7c46f)"),
    ("rvs", "Rvs-look", "Geborsteld staal: minder glans dan chroom, dus vingerafdrukken vallen minder op.",
     "linear-gradient(135deg,#d9dbdc,#a7abae 50%,#cfd2d4)"),
]

MEUBELS = [
    ("eiken", "Eiken", "Licht hout met een rustige nerf. Warm en past bij bijna elke tegel.",
     "repeating-linear-gradient(90deg,#c79a63 0 5px,#b8894f 5px 6px,#cfa46f 6px 11px)"),
    ("wit", "Wit hoogglans", "Licht en strak. In een kleine badkamer valt het meubel zo weg tegen de wand.",
     "linear-gradient(135deg,#fff,#e8ecee)"),
    ("antraciet", "Antraciet mat", "Donker en stoer. Mooi contrast met lichte tegels.",
     "#3a3d40"),
    ("noten", "Notenhout", "Donker, warm hout. Oogt luxe en past bij messing en groen.",
     "repeating-linear-gradient(90deg,#6b4630 0 5px,#5a3a27 5px 6px,#77503a 6px 11px)"),
]

DOUCHES = [
    ("inloop", "Inloopdouche met glazen wand", "Geen deur en geen drempel. Ruim en makkelijk schoon te maken."),
    ("cabine", "Douchebak met deuren", "Een vlakke douchebak met schuif- of draaideuren. Het water blijft goed binnen."),
    ("bad", "Bad met douche", "Een bad met een glazen badwand en een douche erboven. Handig met kleine kinderen."),
]

LICHT = [
    ("warm", "Warm licht", "Ongeveer 2700 tot 3000 kelvin. Gezellig en ontspannen, vooral 's avonds."),
    ("koel", "Koel licht", "Ongeveer 4000 kelvin. Helder en zakelijk, handig bij scheren en opmaken voor de spiegel."),
]

# Voorinstellingen: (id, naam, wand, vloer, kraan, meubel, douche, licht, kenmerken, tips)
STIJLEN = [
    dict(id="modern", naam="Modern", wand="wit", vloer="antraciet", kraan="zwart", meubel="eiken",
         douche="inloop", licht="warm",
         kenmerken="Strakke lijnen, grote tegels, weinig voegen en contrast tussen licht en donker. "
                   "Mat zwarte kranen en een zwevend meubel zijn kenmerkend.",
         tips=["Kies grote tegels (60 × 60 cm of groter): minder voegen geeft een rustig vlak.",
               "Een zwevend meubel en een hangtoilet laten de vloer doorlopen. Dat oogt ruimer en maakt dweilen makkelijker.",
               "Houd het bij twee of drie kleuren, bijvoorbeeld wit, antraciet en hout."]),
    dict(id="landelijk", naam="Landelijk", wand="zellige", vloer="cement", kraan="goud", meubel="eiken",
         douche="bad", licht="warm",
         kenmerken="Warme materialen, handgemaakte tegels en een tegel met patroon op de vloer. "
                   "Messing of goudkleurige kranen en een bad maken het af.",
         tips=["Combineer één tegel met patroon met effen tegels. Twee drukke tegels naast elkaar vechten om aandacht.",
               "Zellige verschilt per tegel in kleur en dikte. Dat hoort zo; vraag de tegelzetter of hij er ervaring mee heeft.",
               "Een staande kraan op het bad of een ouderwetse douchekop past hier goed bij."]),
    dict(id="industrieel", naam="Industrieel", wand="beton", vloer="betonvloer", kraan="zwart", meubel="antraciet",
         douche="inloop", licht="koel",
         kenmerken="Beton-look, zwart metaal en stoere, donkere kleuren. Een inloopdouche met een zwart "
                   "profiel rond het glas hoort er vaak bij.",
         tips=["Beton-look in tegels is waterdicht en makkelijker te onderhouden dan echt beton of betonstuc.",
               "Breng warmte terug met hout, een plant of warm licht, anders oogt het al snel koud.",
               "Een glazen wand met een zwart profiel is een typisch industrieel detail."]),
    dict(id="japandi", naam="Japandi", wand="visgraat", vloer="terrazzovloer", kraan="zwart", meubel="eiken",
         douche="inloop", licht="warm",
         kenmerken="Een mix van Japans en Scandinavisch: licht hout, gedempte natuurtinten, weinig spullen "
                   "en hier en daar een zwart accent.",
         tips=["Kies gedempte tinten: zand, gebroken wit, salie en licht hout.",
               "Weinig spullen in zicht. Een nis in de douche en lades in het meubel helpen daarbij.",
               "Gebruik zwart alleen als accent, bijvoorbeeld bij de kraan of de spiegelrand."]),
    dict(id="klassiek", naam="Klassiek", wand="metro", vloer="marmer", kraan="goud", meubel="wit",
         douche="bad", licht="warm",
         kenmerken="Tijdloze metrotegels, marmerlook op de vloer en een wit meubel. Goud- of "
                   "messingkleurige kranen geven een chique uitstraling.",
         tips=["Metrotegels in halfsteens verband zijn tijdloos; een lichtgrijze voeg is minder gevoelig voor vuil dan een witte.",
               "Marmerlook-tegels zijn makkelijker te onderhouden dan echt marmer, dat zuur en kalk slecht verdraagt.",
               "Kies alle metalen in dezelfde kleur: kraan, spiegelrand, handdoekrek en bedieningsplaat."]),
    dict(id="klein", naam="Kleine badkamer", wand="wit", vloer="betonvloer", kraan="chroom", meubel="wit",
         douche="inloop", licht="koel",
         kenmerken="Lichte kleuren, grote tegels, een zwevend meubel en een inloopdouche met helder glas. "
                   "Zo oogt een kleine ruimte zo groot mogelijk.",
         tips=["Kies een inloopdouche met helder glas in plaats van een cabine met deuren: het glas onderbreekt de ruimte niet.",
               "Leg dezelfde tegel op de vloer en in de douche, dan loopt de vloer visueel door.",
               "Een grote spiegel en goed licht boven de wastafel maken de ruimte groter. Lees ook onze tips voor het indelen van een kleine badkamer."]),
]

STANDAARD = STIJLEN[0]

GROEPEN = [
    ("wand", "Wandtegel", WANDEN),
    ("vloer", "Vloertegel", VLOEREN),
    ("kraan", "Kraankleur", KRANEN),
    ("meubel", "Meubel", MEUBELS),
]


# ---------------------------------------------------------------------------
# SVG: patronen
# ---------------------------------------------------------------------------

def _visgraat(pid, u, tegel, voeg, transform="", tinten=None):
    """Visgraatpatroon van tegels 2u × 1u. Rooster (1,1) en (4,0): periode 4u × 4u."""
    tinten = tinten or [tegel]
    rects = []
    n = 0
    for k in range(-6, 8):
        for m in range(-3, 3):
            ox, oy = k + 4 * m, k
            for (x, y, w, h) in [(ox, oy, 2, 1), (ox, oy + 1, 1, 2)]:
                if x + w <= 0 or x >= 4 or y + h <= 0 or y >= 4:
                    continue
                kleur = tinten[n % len(tinten)]
                n += 1
                rects.append(f'<rect x="{x * u + .6:g}" y="{y * u + .6:g}" width="{w * u - 1.2:g}" '
                             f'height="{h * u - 1.2:g}" fill="{kleur}"/>')
    tf = f' patternTransform="{transform}"' if transform else ""
    return (f'<pattern id="{pid}" width="{4 * u}" height="{4 * u}" patternUnits="userSpaceOnUse"{tf}>'
            f'<rect width="{4 * u}" height="{4 * u}" fill="{voeg}"/>{"".join(rects)}</pattern>')


def _terrazzo(pid, achter):
    stukjes = [(14, 18, 5, "#c9774f"), (48, 10, 3, "#5b5f63"), (80, 26, 4, "#8d9c8a"), (104, 12, 3, "#d8b8a0"),
               (30, 50, 3, "#8d9c8a"), (62, 46, 6, "#d8b8a0"), (96, 60, 4, "#c9774f"), (12, 82, 4, "#5b5f63"),
               (44, 92, 5, "#c9774f"), (76, 86, 3, "#5b5f63"), (108, 98, 5, "#8d9c8a"), (26, 110, 3, "#d8b8a0"),
               (60, 112, 2.5, "#5b5f63"), (88, 40, 2, "#5b5f63"), (36, 30, 2, "#c9774f"), (70, 70, 2, "#8d9c8a")]
    s = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .7:g}" fill="{c}" '
                f'transform="rotate({(x * 7) % 90} {x} {y})"/>' for x, y, r, c in stukjes)
    return (f'<pattern id="{pid}" width="120" height="120" patternUnits="userSpaceOnUse">'
            f'<rect width="120" height="120" fill="#d6cfc3"/><rect x=".8" y=".8" width="118.4" height="118.4" fill="{achter}"/>'
            f'{s}</pattern>')


def _defs():
    p = []
    # Wanden
    p.append('<pattern id="sk-w-wit" width="40" height="40" patternUnits="userSpaceOnUse">'
             '<rect width="40" height="40" fill="#dfe4e7"/><rect x=".7" y=".7" width="38.6" height="38.6" fill="#fbfcfd"/>'
             '<path d="M3 3h14L3 17z" fill="#fff" opacity=".9"/></pattern>')
    p.append('<pattern id="sk-w-beton" width="160" height="80" patternUnits="userSpaceOnUse">'
             '<rect width="160" height="80" fill="#9d9c97"/><rect x=".8" y=".8" width="158.4" height="78.4" fill="#b7b6b0"/>'
             '<circle cx="30" cy="20" r="1.6" fill="#a5a49e"/><circle cx="90" cy="52" r="2" fill="#c4c3bd"/>'
             '<circle cx="128" cy="18" r="1.2" fill="#a2a19b"/><circle cx="62" cy="66" r="1.4" fill="#a8a7a1"/>'
             '<path d="M10 40c30-6 50 6 80-2s50 4 64-1" stroke="#c0bfb9" stroke-width="5" fill="none" opacity=".6"/></pattern>')
    p.append('<pattern id="sk-w-zellige" width="48" height="48" patternUnits="userSpaceOnUse">'
             '<rect width="48" height="48" fill="#cfd8cf"/>'
             '<rect x=".8" y=".8" width="22.4" height="22.4" rx="1.5" fill="#2f6b55"/>'
             '<rect x="24.8" y=".8" width="22.4" height="22.4" rx="1.5" fill="#47866b"/>'
             '<rect x=".8" y="24.8" width="22.4" height="22.4" rx="1.5" fill="#3b7a61"/>'
             '<rect x="24.8" y="24.8" width="22.4" height="22.4" rx="1.5" fill="#2a604c"/>'
             '<ellipse cx="7" cy="7" rx="4" ry="2.5" fill="#fff" opacity=".22"/><ellipse cx="33" cy="9" rx="3" ry="2" fill="#fff" opacity=".18"/>'
             '<ellipse cx="9" cy="32" rx="3" ry="2" fill="#fff" opacity=".2"/><ellipse cx="31" cy="31" rx="4" ry="2.4" fill="#fff" opacity=".15"/>'
             '</pattern>')
    p.append(_terrazzo("sk-w-terrazzo", "#ece6dc"))
    p.append('<pattern id="sk-w-metro" width="60" height="30" patternUnits="userSpaceOnUse">'
             '<rect width="60" height="30" fill="#cfc9be"/>'
             '<rect x=".7" y=".7" width="58.6" height="13.6" rx="1" fill="#f4f2ed"/>'
             '<rect x="-29.3" y="15.7" width="58.6" height="13.6" rx="1" fill="#f4f2ed"/>'
             '<rect x="30.7" y="15.7" width="58.6" height="13.6" rx="1" fill="#f4f2ed"/>'
             '<rect x="3" y="2.5" width="30" height="2" fill="#fff" opacity=".8"/></pattern>')
    p.append(_visgraat("sk-w-visgraat", 14, "#f4f2ed", "#cfc9be", "rotate(45)"))
    # Vloeren (worden in de tekening platgedrukt voor het perspectief)
    p.append('<pattern id="sk-v-antraciet" width="120" height="120" patternUnits="userSpaceOnUse">'
             '<rect width="120" height="120" fill="#33363a"/><rect x="1.2" y="1.2" width="117.6" height="117.6" fill="#4a4d50"/>'
             '<circle cx="40" cy="30" r="2" fill="#55585c"/><circle cx="90" cy="80" r="2.5" fill="#43464a"/></pattern>')
    p.append('<pattern id="sk-v-betonvloer" width="240" height="120" patternUnits="userSpaceOnUse">'
             '<rect width="240" height="120" fill="#a3a29c"/><rect x="1.2" y="1.2" width="237.6" height="117.6" fill="#bdbcb6"/>'
             '<circle cx="50" cy="40" r="2" fill="#b0afa9"/><circle cx="170" cy="90" r="2.5" fill="#c8c7c1"/></pattern>')
    p.append(_visgraat("sk-v-hout", 22, "#b8875a", "#7d5a3a", "rotate(45)",
                       ["#b8875a", "#c69766", "#a87a4c", "#bf8e5e", "#ad7f51"]))
    p.append('<pattern id="sk-v-marmer" width="160" height="160" patternUnits="userSpaceOnUse">'
             '<rect width="160" height="160" fill="#d9d9d6"/><rect x="1" y="1" width="158" height="158" fill="#f4f3f1"/>'
             '<path d="M0 40c30 10 40 40 80 44s50 30 80 36" stroke="#b9b9b9" stroke-width="1.6" fill="none"/>'
             '<path d="M20 160c10-30 40-40 50-70s30-50 60-60" stroke="#cfcfcf" stroke-width="1.1" fill="none"/></pattern>')
    p.append('<pattern id="sk-v-cement" width="80" height="80" patternUnits="userSpaceOnUse">'
             '<rect width="80" height="80" fill="#ecebe6"/>'
             '<path d="M40 4 76 40 40 76 4 40z" fill="#2d3135"/><path d="M40 18 62 40 40 62 18 40z" fill="#ecebe6"/>'
             '<circle cx="40" cy="40" r="7" fill="#2d3135"/>'
             '<path d="M0 0h14L0 14zM80 0H66L80 14zM0 80h14L0 66zM80 80H66L80 66z" fill="#2d3135"/>'
             '<rect width="80" height="80" fill="none" stroke="#c9c7c0" stroke-width="1.2"/></pattern>')
    p.append(_terrazzo("sk-v-terrazzovloer", "#e6dfd3"))
    # Meubels
    p.append('<pattern id="sk-m-eiken" width="60" height="120" patternUnits="userSpaceOnUse">'
             '<rect width="60" height="120" fill="#c79a63"/>'
             '<path d="M8 0c3 40-3 80 2 120M24 0c-4 30 4 70-1 120M41 0c3 50-2 70 3 120M53 0c-2 40 2 80-1 120" '
             'stroke="#b3854f" stroke-width="1.2" fill="none"/>'
             '<ellipse cx="33" cy="60" rx="3" ry="9" fill="none" stroke="#a97c48" stroke-width="1"/></pattern>')
    p.append('<linearGradient id="sk-m-wit" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/>'
             '<stop offset=".55" stop-color="#f1f4f5"/><stop offset="1" stop-color="#dfe5e8"/></linearGradient>')
    p.append('<linearGradient id="sk-m-antraciet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#43474b"/>'
             '<stop offset="1" stop-color="#33363a"/></linearGradient>')
    p.append('<pattern id="sk-m-noten" width="60" height="120" patternUnits="userSpaceOnUse">'
             '<rect width="60" height="120" fill="#6b4630"/>'
             '<path d="M7 0c4 40-3 80 2 120M22 0c-4 30 4 70-1 120M40 0c3 50-2 70 3 120M52 0c-2 40 2 80-1 120" '
             'stroke="#55372a" stroke-width="1.3" fill="none"/>'
             '<ellipse cx="30" cy="70" rx="3" ry="10" fill="none" stroke="#4f3324" stroke-width="1"/></pattern>')
    # Kraankleuren
    for kid, a, b, c in [("chroom", "#f7f9fb", "#8f99a2", "#e4e9ec"), ("zwart", "#4a4a4a", "#0f0f0f", "#2c2c2c"),
                         ("goud", "#f6dc96", "#b0822f", "#e9c770"), ("rvs", "#dfe1e2", "#a2a6a9", "#c9ccce")]:
        p.append(f'<linearGradient id="sk-k-{kid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/>'
                 f'<stop offset=".5" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>')
    # Overig
    p.append('<linearGradient id="sk-spiegel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#eef4f7"/>'
             '<stop offset=".5" stop-color="#cfdde4"/><stop offset="1" stop-color="#e3ecf0"/></linearGradient>')
    p.append('<linearGradient id="sk-glas" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8f4f8" stop-opacity=".55"/>'
             '<stop offset=".5" stop-color="#cfe6ee" stop-opacity=".22"/><stop offset="1" stop-color="#e8f4f8" stop-opacity=".45"/></linearGradient>')
    p.append('<linearGradient id="sk-porselein" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/>'
             '<stop offset="1" stop-color="#e6ebee"/></linearGradient>')
    p.append('<linearGradient id="sk-schaduw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".28"/>'
             '<stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>')
    p.append('<linearGradient id="sk-kegel" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--sk-licht)" stop-opacity=".55"/>'
             '<stop offset="1" style="stop-color:var(--sk-licht)" stop-opacity="0"/></linearGradient>')
    p.append('<radialGradient id="sk-gloed" cx=".5" cy="0" r="1"><stop offset="0" style="stop-color:var(--sk-licht)" stop-opacity=".5"/>'
             '<stop offset="1" style="stop-color:var(--sk-licht)" stop-opacity="0"/></radialGradient>')
    return "<defs>" + "".join(p) + "</defs>"


def _k(extra):
    """Een element in de kraankleur."""
    return f'class="sk-kraan" fill="url(#sk-k-{STANDAARD["kraan"]})" {extra}'


def svg_badkamer():
    s = STANDAARD
    douche_inloop = f"""<g class="sk-douche" data-douche="inloop">
  <rect x="490" y="436" width="300" height="5" fill="#000" opacity=".12"/>
  <rect x="620" y="430" width="120" height="4" rx="2" {_k('')}/>
  <rect x="690" y="200" width="70" height="44" rx="3" fill="#000" opacity=".18"/>
  <rect x="694" y="204" width="62" height="38" rx="2" fill="url(#sk-w-{s['wand']})" data-vlak="wand"/>
  <rect x="694" y="204" width="62" height="38" rx="2" fill="#000" opacity=".12"/>
  <rect x="742" y="140" width="6" height="210" {_k('')}/>
  <rect x="680" y="132" width="68" height="6" rx="3" {_k('')}/>
  <ellipse cx="672" cy="140" rx="34" ry="7" {_k('')}/>
  <rect x="728" y="300" width="34" height="22" rx="6" {_k('')}/>
  <path d="M652 150v30M664 150v40M676 150v36M688 150v28" stroke="#cfe6ee" stroke-width="1.4" opacity=".7" stroke-dasharray="4 7"/>
  <rect x="500" y="96" width="140" height="344" fill="url(#sk-glas)" stroke="#d8e9ef" stroke-width="1.5"/>
  <path d="M520 120l40-20M520 160l80-40" stroke="#fff" stroke-width="3" opacity=".45"/>
  <rect x="497" y="92" width="6" height="350" {_k('')}/>
  <rect x="503" y="92" width="287" height="5" {_k('')}/>
</g>"""
    douche_cabine = f"""<g class="sk-douche" data-douche="cabine" display="none">
  <rect x="490" y="418" width="300" height="22" rx="2" fill="url(#sk-porselein)" stroke="#d3dade"/>
  <ellipse cx="640" cy="424" rx="10" ry="2.5" {_k('')}/>
  <rect x="742" y="150" width="6" height="200" {_k('')}/>
  <ellipse cx="745" cy="150" rx="18" ry="5" {_k('')}/>
  <rect x="728" y="300" width="34" height="22" rx="6" {_k('')}/>
  <rect x="496" y="100" width="146" height="318" fill="url(#sk-glas)" stroke="#d8e9ef" stroke-width="1.5"/>
  <rect x="636" y="104" width="150" height="314" fill="url(#sk-glas)" stroke="#d8e9ef" stroke-width="1.5"/>
  <path d="M512 130l40-20M650 140l50-25" stroke="#fff" stroke-width="3" opacity=".45"/>
  <rect x="490" y="94" width="300" height="7" {_k('')}/>
  <rect x="490" y="94" width="6" height="326" {_k('')}/>
  <rect x="784" y="94" width="6" height="326" {_k('')}/>
  <rect x="628" y="230" width="5" height="70" rx="2.5" {_k('')}/>
  <rect x="644" y="230" width="5" height="70" rx="2.5" {_k('')}/>
</g>"""
    douche_bad = f"""<g class="sk-douche" data-douche="bad" display="none">
  <path d="M478 352h318v6c0 44-24 74-60 76H538c-36-2-60-32-60-76z" fill="url(#sk-porselein)" stroke="#d3dade"/>
  <rect x="474" y="346" width="326" height="10" rx="5" fill="#fff" stroke="#d3dade"/>
  <rect x="540" y="434" width="12" height="7" {_k('')}/><rect x="722" y="434" width="12" height="7" {_k('')}/>
  <rect x="740" y="150" width="6" height="140" {_k('')}/>
  <ellipse cx="743" cy="150" rx="18" ry="5" {_k('')}/>
  <rect x="712" y="292" width="58" height="16" rx="6" {_k('')}/>
  <path d="M712 300h-22v20" stroke="url(#sk-k-{s['kraan']})" class="sk-kraan-lijn" stroke-width="7" fill="none" stroke-linecap="round"/>
  <rect x="500" y="140" width="110" height="206" fill="url(#sk-glas)" stroke="#d8e9ef" stroke-width="1.5"/>
  <path d="M514 170l40-20M514 210l70-36" stroke="#fff" stroke-width="3" opacity=".45"/>
  <rect x="496" y="140" width="5" height="206" {_k('')}/>
</g>"""

    return f"""<svg id="sk-svg" class="sk-svg" viewBox="0 0 800 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Illustratie van een badkamer" style="--sk-licht:#ffd59a">
{_defs()}
<rect width="800" height="442" fill="url(#sk-w-{s['wand']})" data-vlak="wand"/>
<g transform="translate(0 442) scale(1 .45)"><rect width="800" height="262" fill="url(#sk-v-{s['vloer']})" data-vlak="vloer"/></g>
<rect y="442" width="800" height="26" fill="url(#sk-schaduw)" opacity=".5"/>
<rect y="440" width="800" height="3" fill="#000" opacity=".12"/>
<!-- spiegel met lichtlijn -->
<rect x="96" y="70" width="200" height="190" rx="14" {_k('')}/>
<rect x="101" y="75" width="190" height="180" rx="11" fill="url(#sk-spiegel)"/>
<path d="M130 100l50-22M130 140l100-50" stroke="#fff" stroke-width="5" opacity=".55"/>
<rect x="110" y="56" width="172" height="5" rx="2.5" style="fill:var(--sk-licht)" class="sk-lamp"/>
<rect x="110" y="61" width="172" height="80" fill="url(#sk-gloed)"/>
<!-- wastafelmeubel -->
<rect x="74" y="312" width="244" height="12" rx="2" fill="#000" opacity=".12" transform="translate(0 70)"/>
<rect x="74" y="300" width="244" height="80" rx="3" fill="url(#sk-m-{s['meubel']})" data-vlak="meubel" stroke="#000" stroke-opacity=".12"/>
<path d="M76 340h240" stroke="#000" stroke-opacity=".16" stroke-width="1.5"/>
<rect x="166" y="318" width="60" height="4" rx="2" {_k('')}/><rect x="166" y="356" width="60" height="4" rx="2" {_k('')}/>
<rect x="70" y="286" width="252" height="16" rx="3" fill="url(#sk-porselein)" stroke="#d3dade"/>
<path d="M150 288h92" stroke="#c9d3d8" stroke-width="3" stroke-linecap="round"/>
<path d="M196 288v-30h-20" class="sk-kraan-lijn" stroke="url(#sk-k-{s['kraan']})" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<rect x="190" y="282" width="12" height="7" rx="2" {_k('')}/>
<rect x="198" y="262" width="12" height="4" rx="2" {_k('')}/>
<!-- handdoekhaak -->
<rect x="340" y="210" width="24" height="5" rx="2.5" {_k('')}/>
<path d="M334 214h36v62c0 6-4 10-10 10h-16c-6 0-10-4-10-10z" fill="#f2efe9" stroke="#dcd6cc"/>
<path d="M334 250h36M334 256h36" stroke="#dcd6cc"/>
<!-- hangtoilet -->
<rect x="388" y="240" width="54" height="74" rx="4" {_k('')}/>
<rect x="394" y="246" width="20" height="62" rx="3" fill="#000" opacity=".08"/><rect x="416" y="246" width="20" height="62" rx="3" fill="#000" opacity=".08"/>
<path d="M380 340h76v8c0 26-16 42-36 42h-10c-18 0-30-14-30-34z" fill="url(#sk-porselein)" stroke="#d3dade"/>
<rect x="378" y="334" width="80" height="9" rx="4" fill="#fff" stroke="#d3dade"/>
<!-- plafondspots met lichtkegels -->
<polygon points="196,0 216,0 300,300 112,300" fill="url(#sk-kegel)" opacity=".5" class="sk-kegel"/>
<polygon points="410,0 430,0 500,240 340,240" fill="url(#sk-kegel)" opacity=".35" class="sk-kegel"/>
<polygon points="630,0 650,0 740,320 540,320" fill="url(#sk-kegel)" opacity=".45" class="sk-kegel"/>
<rect x="194" y="0" width="24" height="5" rx="2" style="fill:var(--sk-licht)" class="sk-lamp"/>
<rect x="408" y="0" width="24" height="5" rx="2" style="fill:var(--sk-licht)" class="sk-lamp"/>
<rect x="628" y="0" width="24" height="5" rx="2" style="fill:var(--sk-licht)" class="sk-lamp"/>
{douche_inloop}
{douche_cabine}
{douche_bad}
<!-- lichtkleur over het geheel -->
<rect width="800" height="560" style="fill:var(--sk-licht);mix-blend-mode:multiply" opacity=".1" class="sk-sfeer"/>
<g class="sk-label"><rect x="12" y="520" width="94" height="26" rx="13" fill="#fff" opacity=".88"/>
<text x="59" y="538" text-anchor="middle" font-size="13" font-family="Arial,sans-serif" font-weight="700" fill="#33474c">Illustratie</text></g>
</svg>"""


# ---------------------------------------------------------------------------
# Paneel
# ---------------------------------------------------------------------------

def _knoppen(groep, opties, gekozen):
    return "".join(
        f'<button type="button" class="sk-optie{" on" if oid == gekozen else ""}" data-groep="{groep}" '
        f'data-waarde="{oid}" aria-pressed="{"true" if oid == gekozen else "false"}" title="{uitleg}">'
        f'<i style="background:{staal}"></i><span>{naam}</span></button>'
        for oid, naam, uitleg, staal in opties)


def _tekstknoppen(groep, opties, gekozen):
    return "".join(
        f'<button type="button" class="sk-optie sk-tekst{" on" if oid == gekozen else ""}" data-groep="{groep}" '
        f'data-waarde="{oid}" aria-pressed="{"true" if oid == gekozen else "false"}" title="{uitleg}">'
        f'<span>{naam}</span></button>'
        for oid, naam, uitleg in opties)


def _overzicht_html(s):
    """Tekstoverzicht van een combinatie. De JavaScript bouwt hetzelfde na elke klik."""
    def naam(lijst, oid):
        return next(x[1] for x in lijst if x[0] == oid)
    rijen = [("Wandtegel", naam(WANDEN, s["wand"])), ("Vloertegel", naam(VLOEREN, s["vloer"])),
             ("Kraankleur", naam(KRANEN, s["kraan"])), ("Meubel", naam(MEUBELS, s["meubel"])),
             ("Douche", naam(DOUCHES, s["douche"])), ("Verlichting", naam(LICHT, s["licht"]))]
    return "".join(f"<li><span>{k}</span><strong>{v}</strong></li>" for k, v in rijen)


def _tool_html():
    s = STANDAARD
    stijlknoppen = "".join(
        f'<button type="button" class="sk-stijl{" on" if st["id"] == s["id"] else ""}" data-stijl="{st["id"]}" '
        f'aria-pressed="{"true" if st["id"] == s["id"] else "false"}">{st["naam"]}</button>' for st in STIJLEN)
    groepen = "".join(
        f'<h3 class="sk-kop">{lab}</h3><div class="sk-opties" role="group" aria-label="{lab}">'
        f'{_knoppen(g, opties, s[g])}</div>' for g, lab, opties in GROEPEN)
    return f"""<div class="sk-tool" id="stijlkiezer">
  <div class="sk-voorbeeld">
    <div class="sk-plaat">{svg_badkamer()}</div>
    <p class="sk-hint">Dit is een illustratie, geen foto. Kleuren op een scherm wijken af van echte tegels en kranen: bekijk altijd een staal in het echt.</p>
  </div>
  <div class="sk-paneel">
    <h2 class="sk-kop sk-kop1">Begin met een stijl</h2>
    <div class="sk-stijlen" role="group" aria-label="Stijlen">{stijlknoppen}</div>
    <p class="sk-kenmerken" data-kenmerken><strong>{s['naam']}:</strong> {s['kenmerken']}</p>
    <h2 class="sk-kop sk-kop1">Pas zelf aan</h2>
    {groepen}
    <h3 class="sk-kop">Douche</h3>
    <div class="sk-opties sk-opties-tekst" role="group" aria-label="Douche">{_tekstknoppen("douche", DOUCHES, s["douche"])}</div>
    <h3 class="sk-kop">Verlichting</h3>
    <div class="sk-opties sk-opties-tekst" role="group" aria-label="Verlichting">{_tekstknoppen("licht", LICHT, s["licht"])}</div>
    <p class="sk-uitleg" data-uitleg aria-live="polite">Tip: tik op een keuze om hem in de tekening te zien.</p>
  </div>
</div>
<div class="sk-overzicht" id="overzicht">
  <div>
    <h2>Jouw combinatie</h2>
    <ul class="sk-lijst" data-overzicht>{_overzicht_html(s)}</ul>
    <p class="sk-zin" data-zin></p>
  </div>
  <div class="sk-acties">
    <a class="btn btn-primary" href="/offerte-aanvragen/">Offertes voor deze badkamer</a>
    <button type="button" class="btn btn-ghost" data-kopieer>Kopieer als tekst</button>
    <button type="button" class="btn btn-ghost" data-deel>Kopieer link naar dit ontwerp</button>
    <p class="sk-melding" role="status" aria-live="polite"></p>
  </div>
</div>"""


# ---------------------------------------------------------------------------
# Inhoud onder de tool
# ---------------------------------------------------------------------------

FAQS = [
    ("Hoe kies ik een stijl voor mijn badkamer?",
     "Begin bij wat je mooi vindt en wat bij de rest van je huis past. Kies daarna één ding dat de toon zet, "
     "bijvoorbeeld de wandtegel of de kraankleur, en stem de rest daarop af. Houd het bij twee of drie kleuren "
     "en materialen. Met deze stijlkiezer zie je snel welke combinaties werken."),
    ("Klopt de kleur in de tekening met de echte tegel?",
     "Nee, niet precies. De tekening is een illustratie en elk scherm toont kleuren anders. Gebruik de tool om "
     "combinaties te vergelijken, en bekijk daarna echte stalen in een showroom of thuis bij daglicht en bij de "
     "lamp die je in de badkamer gebruikt."),
    ("Welke kraankleur is het makkelijkst schoon te houden?",
     "Geborsteld rvs en geborsteld messing laten het minst zien van kalk en vingerafdrukken. Glanzend chroom en "
     "mat zwart tonen kalkvlekken sneller, vooral bij hard water. Even droogwrijven na het douchen helpt bij elke kleur."),
    ("Kan ik verschillende metaalkleuren combineren?",
     "Dat kan, maar het oogt rustiger als kraan, douche, spiegelrand, handdoekrek en bedieningsplaat van het toilet "
     "dezelfde kleur hebben. Wil je toch mengen, kies dan één hoofdkleur en gebruik de tweede alleen als klein accent."),
    ("Welke stijl werkt het best in een kleine badkamer?",
     "Lichte kleuren, grote tegels, een zwevend meubel en een inloopdouche met helder glas laten een kleine ruimte "
     "groter lijken. Een donkere vloer kan ook, zolang de wanden licht blijven. Kies in de tool de voorinstelling "
     "Kleine badkamer om te zien hoe dat uitpakt."),
    ("Wat is het verschil tussen warm en koel licht?",
     "Warm licht (ongeveer 2700 tot 3000 kelvin) is geler en gezelliger. Koel licht (rond 4000 kelvin) is witter en "
     "helderder. Veel mensen kiezen warm licht voor de algemene verlichting en een heldere lamp bij de spiegel. "
     "Lampen die je kunt dimmen of in kleur kunt instellen geven je allebei."),
    ("Bewaart de stijlkiezer mijn keuzes?",
     "Je keuze staat in het adres van de pagina. Kopieer de link en je kunt het ontwerp later weer openen of "
     "doorsturen. Er wordt niets naar ons verstuurd en er is geen account nodig."),
]


def _stijlen_html():
    kaarten = []
    for st in STIJLEN:
        tips = "".join(f"<li>{t}</li>" for t in st["tips"])
        kaarten.append(f"""<article class="sk-kaart" id="stijl-{st['id']}">
  <h3>{st['naam']}</h3>
  <p>{st['kenmerken']}</p>
  <ul class="checklist">{tips}</ul>
  <button type="button" class="sk-probeer" data-stijl="{st['id']}">Bekijk {st['naam'].lower()} in de tekening</button>
</article>""")
    return "".join(kaarten)


CSS = r"""<style>
.sk-sectie{padding:8px 0 40px}
.sk-tool{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:28px;align-items:start}
.sk-voorbeeld{position:sticky;top:86px;background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);padding:12px;box-shadow:var(--shadow)}
.sk-plaat{border-radius:var(--radius);overflow:hidden;background:#eef1f2}
.sk-svg{display:block;width:100%;height:auto}
.sk-svg [data-vlak],.sk-svg .sk-kraan{transition:fill .2s}
.sk-hint{font-size:.82rem;color:var(--muted);margin:10px 2px 0}
.sk-paneel{min-width:0;background:#fff;border:1px solid var(--line);border-top:4px solid var(--accent);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:20px 20px 22px}
.sk-kop{font-size:.8rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:16px 0 8px;font-weight:700}
.sk-kop1{font-size:1.08rem;text-transform:none;letter-spacing:0;color:var(--ink);margin:0 0 10px}
.sk-kop1:not(:first-child){margin-top:20px;padding-top:16px;border-top:1px solid var(--line)}
.sk-stijlen{display:flex;flex-wrap:wrap;gap:7px}
.sk-stijl{border:1px solid var(--line);background:var(--bg-soft);border-radius:99px;padding:7px 13px;font:inherit;font-size:.88rem;font-weight:650;color:var(--ink);cursor:pointer;transition:border-color .15s,background .15s}
.sk-stijl:hover{border-color:var(--navy-500)}
.sk-stijl.on{border-color:var(--accent);background:var(--accent-soft);box-shadow:0 0 0 3px rgba(196,81,31,.13)}
.sk-kenmerken{font-size:.88rem;line-height:1.5;margin:12px 0 0;background:var(--bg-soft);border-radius:var(--radius);padding:10px 12px}
.sk-opties{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px}
.sk-optie{display:flex;align-items:center;gap:8px;text-align:left;border:1.5px solid var(--line);background:#fff;border-radius:10px;padding:6px 8px;font:inherit;font-size:.8rem;line-height:1.2;font-weight:600;color:var(--ink);cursor:pointer;min-width:0;transition:border-color .15s,background .15s}
.sk-optie i{flex:0 0 24px;height:24px;border-radius:6px;box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
.sk-optie span{min-width:0;overflow-wrap:break-word;hyphens:auto}
.sk-optie:hover{border-color:var(--navy-500)}
.sk-optie.on{border-color:var(--accent);background:var(--accent-soft)}
.sk-optie:focus-visible,.sk-stijl:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.sk-opties-tekst{grid-template-columns:repeat(3,minmax(0,1fr))}
.sk-opties-tekst .sk-tekst{justify-content:center;text-align:center;padding:8px}
.sk-uitleg{font-size:.86rem;color:var(--muted);margin:14px 0 0;min-height:2.6em}
.sk-overzicht{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(0,1fr);gap:28px;margin-top:28px;background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);padding:22px;box-shadow:var(--shadow)}
.sk-overzicht h2{font-size:1.25rem;margin:0 0 10px}
.sk-lijst{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px 18px}
.sk-lijst li{display:flex;justify-content:space-between;gap:10px;border-bottom:1px dashed var(--line);padding:6px 0;font-size:.92rem}
.sk-lijst span{color:var(--muted)}
.sk-lijst strong{color:var(--ink);text-align:right}
.sk-zin{font-size:.92rem;margin:12px 0 0}
.sk-acties{display:flex;flex-direction:column;gap:10px;justify-content:center}
.sk-melding{min-height:1.4em;font-size:.88rem;color:var(--green);font-weight:600;margin:0}
.sk-kaarten{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:10px}
.sk-kaart{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);padding:20px;box-shadow:var(--shadow);display:flex;flex-direction:column}
.sk-kaart h3{margin:0 0 6px}
.sk-kaart p{font-size:.93rem}
.sk-kaart .checklist{font-size:.9rem;margin:4px 0 12px}
.sk-probeer{margin-top:auto;align-self:flex-start;border:0;background:none;padding:0;font:inherit;font-weight:700;color:var(--accent);cursor:pointer;text-decoration:underline;text-underline-offset:3px}
.sk-links{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:10px}
.sk-links a{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:16px;text-decoration:none;color:var(--ink);box-shadow:var(--shadow)}
.sk-links a:hover{border-color:var(--navy-500)}
.sk-links strong{display:block;margin-bottom:4px}
.sk-links span{font-size:.88rem;color:var(--muted)}
@media(max-width:900px){
  .sk-tool,.sk-overzicht{grid-template-columns:minmax(0,1fr);gap:16px}
  .sk-voorbeeld{top:64px;z-index:5;padding:6px}
  .sk-hint{font-size:.74rem;margin-top:6px}
  .sticky-cta{display:none}body{padding-bottom:0}
}
@media(max-width:900px) and (max-height:760px){.sk-svg{max-height:32vh;width:auto;max-width:100%;margin:0 auto}}
@media(max-width:480px){
  .sk-paneel{padding:16px 14px}
  .sk-opties{grid-template-columns:repeat(2,minmax(0,1fr))}
  .sk-opties-tekst{grid-template-columns:minmax(0,1fr)}
  .sk-lijst{grid-template-columns:minmax(0,1fr)}
  .sk-overzicht{padding:16px}
  .sk-kaarten{grid-template-columns:minmax(0,1fr)}
}
</style>"""


def _js_data():
    data = {
        "wand": {o[0]: [o[1], o[2]] for o in WANDEN},
        "vloer": {o[0]: [o[1], o[2]] for o in VLOEREN},
        "kraan": {o[0]: [o[1], o[2]] for o in KRANEN},
        "meubel": {o[0]: [o[1], o[2]] for o in MEUBELS},
        "douche": {o[0]: [o[1], o[2]] for o in DOUCHES},
        "licht": {o[0]: [o[1], o[2]] for o in LICHT},
        "stijlen": {st["id"]: {k: st[k] for k in ("naam", "wand", "vloer", "kraan", "meubel", "douche", "licht", "kenmerken")}
                    for st in STIJLEN},
        "standaard": STANDAARD["id"],
    }
    return json.dumps(data, ensure_ascii=False)


JS = r"""
(function () {
  "use strict";
  var D = window.SK_DATA;
  var tool = document.getElementById("stijlkiezer");
  if (!D || !tool) return;
  var svg = document.getElementById("sk-svg");
  var GROEPEN = ["wand", "vloer", "kraan", "meubel", "douche", "licht"];
  var LABEL = {wand: "Wandtegel", vloer: "Vloertegel", kraan: "Kraankleur", meubel: "Meubel", douche: "Douche", licht: "Verlichting"};
  var LICHTKLEUR = {warm: "#ffd59a", koel: "#dcecff"};
  var st = {};
  var stijl = D.standaard;
  var basis = D.stijlen[D.standaard];
  GROEPEN.forEach(function (g) { st[g] = basis[g]; });

  function zetFill(sel, waarde) {
    var els = svg.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++) els[i].setAttribute("fill", waarde);
  }

  function teken() {
    zetFill('[data-vlak="wand"]', "url(#sk-w-" + st.wand + ")");
    zetFill('[data-vlak="vloer"]', "url(#sk-v-" + st.vloer + ")");
    zetFill('[data-vlak="meubel"]', "url(#sk-m-" + st.meubel + ")");
    zetFill(".sk-kraan", "url(#sk-k-" + st.kraan + ")");
    var lijnen = svg.querySelectorAll(".sk-kraan-lijn");
    for (var i = 0; i < lijnen.length; i++) lijnen[i].setAttribute("stroke", "url(#sk-k-" + st.kraan + ")");
    var douches = svg.querySelectorAll(".sk-douche");
    for (var j = 0; j < douches.length; j++) {
      if (douches[j].getAttribute("data-douche") === st.douche) douches[j].removeAttribute("display");
      else douches[j].setAttribute("display", "none");
    }
    svg.style.setProperty("--sk-licht", LICHTKLEUR[st.licht] || LICHTKLEUR.warm);
    svg.setAttribute("aria-label", "Illustratie van een badkamer: " + omschrijving());
    var knoppen = tool.querySelectorAll(".sk-optie");
    for (var k = 0; k < knoppen.length; k++) {
      var on = st[knoppen[k].getAttribute("data-groep")] === knoppen[k].getAttribute("data-waarde");
      knoppen[k].classList.toggle("on", on);
      knoppen[k].setAttribute("aria-pressed", on ? "true" : "false");
    }
    var sk = tool.querySelectorAll(".sk-stijl");
    for (var m = 0; m < sk.length; m++) {
      var aan = sk[m].getAttribute("data-stijl") === stijl;
      sk[m].classList.toggle("on", aan);
      sk[m].setAttribute("aria-pressed", aan ? "true" : "false");
    }
    var ken = tool.querySelector("[data-kenmerken]");
    if (stijl && D.stijlen[stijl]) {
      ken.innerHTML = "<strong>" + D.stijlen[stijl].naam + ":</strong> " + D.stijlen[stijl].kenmerken;
    } else {
      ken.innerHTML = "<strong>Eigen combinatie.</strong> Je hebt een stijl aangepast. Kies een stijl om opnieuw te beginnen.";
    }
    overzicht();
  }

  function naam(g) { return D[g][st[g]][0]; }

  function omschrijving() {
    return GROEPEN.map(function (g) { return LABEL[g].toLowerCase() + " " + naam(g).toLowerCase(); }).join(", ");
  }

  function overzicht() {
    var ul = document.querySelector("[data-overzicht]");
    if (ul) {
      ul.innerHTML = GROEPEN.map(function (g) {
        return "<li><span>" + LABEL[g] + "</span><strong>" + naam(g) + "</strong></li>";
      }).join("");
    }
    var zin = document.querySelector("[data-zin]");
    if (zin) {
      var basisTekst = stijl && D.stijlen[stijl] ? "Stijl: " + D.stijlen[stijl].naam + ". " : "Eigen combinatie. ";
      zin.textContent = basisTekst + "Neem dit overzicht mee naar de showroom of de badkamerspecialist, dan weten jullie meteen waar je heen wilt.";
    }
  }

  function alsTekst() {
    var regels = ["Mijn badkamer (" + (stijl && D.stijlen[stijl] ? D.stijlen[stijl].naam : "eigen combinatie") + ")"];
    GROEPEN.forEach(function (g) { regels.push("- " + LABEL[g] + ": " + naam(g)); });
    return regels.join("\n");
  }

  function naarHash() {
    var h = "#" + GROEPEN.map(function (g) { return g + "=" + st[g]; }).join("&") + (stijl ? "&stijl=" + stijl : "");
    try { history.replaceState(null, "", h); } catch (e) {}
  }

  function uitHash() {
    var h = (location.hash || "").replace(/^#/, "");
    if (!h) return false;
    var gevonden = false;
    var nieuw = {};
    var nieuwStijl = null;
    h.split("&").forEach(function (deel) {
      var kv = deel.split("=");
      if (kv.length !== 2) return;
      if (kv[0] === "stijl" && D.stijlen[kv[1]]) { nieuwStijl = kv[1]; return; }
      if (GROEPEN.indexOf(kv[0]) > -1 && D[kv[0]][kv[1]]) { nieuw[kv[0]] = kv[1]; gevonden = true; }
    });
    if (!gevonden) return false;
    for (var g in nieuw) st[g] = nieuw[g];
    stijl = nieuwStijl;
    if (stijl) {
      GROEPEN.forEach(function (gr) { if (D.stijlen[stijl][gr] !== st[gr]) stijl = null; });
    }
    return true;
  }

  function kiesStijl(id) {
    var s = D.stijlen[id];
    if (!s) return;
    stijl = id;
    GROEPEN.forEach(function (g) { st[g] = s[g]; });
    tool.querySelector("[data-uitleg]").textContent = "Stijl " + s.naam + " staat in de tekening.";
    teken();
    naarHash();
  }

  tool.addEventListener("click", function (e) {
    var knop = e.target.closest ? e.target.closest("button") : null;
    if (!knop) return;
    if (knop.hasAttribute("data-stijl")) { kiesStijl(knop.getAttribute("data-stijl")); return; }
    var g = knop.getAttribute("data-groep");
    var w = knop.getAttribute("data-waarde");
    if (!g || !D[g] || !D[g][w]) return;
    st[g] = w;
    if (stijl && D.stijlen[stijl][g] !== w) stijl = null;
    tool.querySelector("[data-uitleg]").textContent = D[g][w][0] + ": " + D[g][w][1];
    teken();
    naarHash();
  });

  var probeer = document.querySelectorAll(".sk-probeer");
  for (var p = 0; p < probeer.length; p++) {
    probeer[p].addEventListener("click", function () {
      kiesStijl(this.getAttribute("data-stijl"));
      tool.scrollIntoView({behavior: "smooth", block: "start"});
    });
  }

  function kopieer(tekst, melding) {
    var m = document.querySelector(".sk-melding");
    function klaar(ok) { if (m) m.textContent = ok ? melding : "Kopiëren lukte niet. Selecteer de tekst en kopieer hem zelf."; }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(tekst).then(function () { klaar(true); }, function () { klaar(false); });
    } else {
      klaar(false);
    }
  }
  var kb = document.querySelector("[data-kopieer]");
  if (kb) kb.addEventListener("click", function () { kopieer(alsTekst(), "Het overzicht staat op je klembord."); });
  var db = document.querySelector("[data-deel]");
  if (db) db.addEventListener("click", function () { naarHash(); kopieer(location.href, "De link naar dit ontwerp staat op je klembord."); });

  uitHash();
  teken();
  window.SK_TEST = {st: st, alsTekst: alsTekst, uitHash: uitHash, kiesStijl: kiesStijl};
})();
"""


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Badkamerstijl-kiezer", None)])
    faq_html, faq_ld = faq_blok(FAQS)
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Badkamerstijl-kiezer",
        "url": SITE["url"] + PAD,
        "applicationCategory": "DesignApplication",
        "operatingSystem": "Alle",
        "isAccessibleForFree": True,
        "inLanguage": "nl-NL",
        "description": "Probeer in een getekende badkamer verschillende tegels, kraankleuren, meubels, douches en verlichting uit.",
    }

    links = [
        ("/inspiratie/", "Inspiratie: zes stijlen in beeld", "3D-illustraties van zes badkamerstijlen, met materialen en kleuren."),
        ("/kennisbank/badkamerstijlen/", "Badkamerstijlen uitgelegd", "Meer over elke stijl, met voorbeelden en valkuilen."),
        ("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Formaat, antislip, glazuur en hoeveel tegels je nodig hebt."),
        ("/badkamerspullen/kranen-kiezen/", "Kranen kiezen", "Thermostaat of mengkraan, inbouw of opbouw, en welke afwerking."),
        ("/kennisbank/kleine-badkamer-indelen/", "Kleine badkamer indelen", "Slimme keuzes voor een badkamer met weinig ruimte."),
        ("/offerte-aanvragen/", "Offertes aanvragen", "Ontvang gratis offertes van maximaal drie badkamerspecialisten."),
    ]
    links_html = "".join(f'<a href="{u}"><strong>{t}</strong><span>{o}</span></a>' for u, t, o in links)

    body = f"""{CSS}
{cr}
<section class="section-sm tool-hero">
  <div class="wrap">
    <span class="badge">Gratis tool · stijlkiezer</span>
    <h1>Badkamerstijl kiezen: probeer het uit in een tekening</h1>
    <p class="lead">Kies een stijl, of wissel zelf de wandtegel, de vloertegel, de kraankleur, het meubel, de douche en het licht. Je ziet het meteen in de getekende badkamer. Handig om te ontdekken wat je mooi vindt, voordat je naar de showroom of een badkamerspecialist gaat.</p>
  </div>
</section>
<section class="sk-sectie">
  <div class="wrap">{_tool_html()}</div>
</section>

<section class="section soft"><div class="wrap">
  <div class="prose" style="max-width:760px">
    <h2>Zes stijlen en wat erbij hoort</h2>
    <p>Elke stijl heeft een paar vaste kenmerken. Je hoeft ze niet allemaal over te nemen: kies wat bij jou en je huis past. Klik bij een stijl op de link om hem in de tekening te zien.</p>
  </div>
  <div class="sk-kaarten">{_stijlen_html()}</div>
</div></section>

<section class="section"><div class="wrap narrow prose">
  <h2>Zo maak je een combinatie die klopt</h2>
  <ul class="checklist">
    <li><strong>Kies één blikvanger.</strong> Een tegel met patroon, een gekleurde zellige of een opvallende kraan. Houd de rest daaromheen rustig.</li>
    <li><strong>Houd het bij twee of drie kleuren en materialen.</strong> Bijvoorbeeld wit, hout en zwart. Meer wordt al snel onrustig, zeker in een kleine ruimte.</li>
    <li><strong>Eén metaalkleur.</strong> Kraan, douche, spiegelrand, handdoekrek en bedieningsplaat in dezelfde afwerking ogen als één geheel.</li>
    <li><strong>Denk aan onderhoud.</strong> Kleine tegels betekenen meer voegen om schoon te houden. Mat zwart en glanzend chroom tonen kalk sneller dan geborsteld metaal.</li>
    <li><strong>Kijk naar het licht.</strong> Een tegel ziet er bij warm licht anders uit dan bij koel licht of daglicht. Bekijk stalen daarom in de ruimte zelf.</li>
    <li><strong>Antislip op de vloer.</strong> Kies voor de douchevloer een tegel die geschikt is voor natte ruimtes. Vraag ernaar bij de tegelwinkel of de specialist.</li>
  </ul>
  <p>Weet je wat je wilt? Neem het overzicht van je combinatie mee als je <a href="/offerte-aanvragen/">offertes aanvraagt</a>. Een badkamerspecialist kan dan meteen inschatten wat er nodig is.</p>
</div></section>

<section class="section soft"><div class="wrap">
  <h2>Verder lezen</h2>
  <div class="sk-links">{links_html}</div>
</div></section>

{faq_html}
{cta_blok("Je stijl gekozen? Vergelijk offertes", "Beschrijf je wensen in een minuut en ontvang gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio.")}
<script>window.SK_DATA = {_js_data()};</script>
<script>{JS}</script>
"""
    html = page(
        title("Badkamerstijl kiezen: probeer tegels en kranen"),
        desc("Wissel in een getekende badkamer live van tegels, kraankleur, meubel, douche en licht.",
             "Met zes stijlen, tips per stijl en een overzicht om mee te nemen."),
        PAD, body, jsonld=[cr_ld, faq_ld, app_ld])
    write(PAD, html, prio=0.6)
