# -*- coding: utf-8 -*-
"""Beleving-pagina /zo-verloopt-je-verbouwing/ (agent A8, ronde 3).

Het hele traject van een badkamerrenovatie als verhaal dat meebeweegt met scrollen:
- een sticky inline SVG van één badkamer die per fase verandert (kaal, leidingen, tegels, sanitair);
- een voortgangsbalk "dag X van ±15";
- per fase: wat er gebeurt, richtduur, wat jij regelt, richtprijs (uit richtprijzen.py) en valkuilen;
- op mobiel (en zonder JavaScript) een eigen beeld per fase in plaats van de sticky illustratie;
- onderaan een checklist met vinkjes (voortgang in localStorage) en een printknop.

Interface: LINKS + build(write).

Bronnen (geraadpleegd november 2026):
- Doorlooptijd: Homedeal, badkamer renovatie: "kleine renovatie 3 tot 7 dagen, gemiddelde renovatie
  1 tot 2 weken, complete verbouwing 2 tot 3+ weken". https://www.homedeal.nl/badkamerspecialist/badkamer-renovatie/
  De verdeling over de fases (±15 werkdagen) is een eigen inschatting binnen die bandbreedte en sluit aan op
  /kennisbank/volgorde-badkamerrenovatie/ ("vaak twee tot vier weken, inclusief droogtijden").
- Oplevering: Consumentenbond, oplevering door aannemer: proces-verbaal van oplevering; bij ontevredenheid
  een deel (bijvoorbeeld 5 of 10%) van de betaling inhouden.
  https://www.consumentenbond.nl/juridisch-advies/wonen/problemen-aannemer/oplevering-aannemer-te-laat
- Waterbesparende douchekop: Milieu Centraal, kluswijzer waterbesparende douchekop (4,0 tot 7,2 liter per
  minuut, doorstroomklasse ZZ). https://www.milieucentraal.nl/media/q1bb4qtr/kluswijzer-waterbesparende-douchekop.pdf
- Garantie: Burgerlijk Wetboek art. 7:758 lid 4 en 7:761 (zoals uitgelegd op /kennisbank/garantie-badkamerrenovatie/).
- Alle bedragen komen uit richtprijzen.py (Homedeal, Werkspot, Trustoo, Slimster), incl. 21% btw.
"""
import json
import re
from datetime import date

import richtprijzen as RP
from components import (page, crumbs, title, faq_blok, cta_blok, cta_midden, offertecheck_blok,
                        render_beeld, feiten_blok, eur)
from data import SITE, DIENST_BY_SLUG

try:
    from render_data import RENDERS
except Exception:  # render_data ontbreekt: dan geen renders
    RENDERS = {}

PAD = "/zo-verloopt-je-verbouwing/"
GEPUBLICEERD = "2026-11-23"
TOTAAL_DAGEN = 15

LINKS = [
    (PAD, "Zo verloopt je verbouwing",
     "Het hele traject van een badkamerrenovatie in tien fases, met duur, kosten en wat jij regelt."),
]

BRON_HOMEDEAL = ("Homedeal, badkamer renovatie: doorlooptijd per soort renovatie",
                 "https://www.homedeal.nl/badkamerspecialist/badkamer-renovatie/")
BRON_CB = ("Consumentenbond, oplevering door de aannemer",
           "https://www.consumentenbond.nl/juridisch-advies/wonen/problemen-aannemer/oplevering-aannemer-te-laat")
BRON_MC = ("Milieu Centraal, kluswijzer waterbesparende douchekop",
           "https://www.milieucentraal.nl/media/q1bb4qtr/kluswijzer-waterbesparende-douchekop.pdf")


def _p(sleutel):
    """'€250 – €850' uit richtprijzen.py."""
    r = RP.RICHTPRIJZEN[sleutel]
    return f"{eur(r['laag'])} – {eur(r['hoog'])}"


_TOT = DIENST_BY_SLUG["badkamer-renoveren"]
TOTAAL = f"{eur(_TOT['prijs_van'])} – {eur(_TOT['prijs_tot'])}"

# ---------------------------------------------------------------------------
# De tien fases
# ---------------------------------------------------------------------------
# dag: (van, tot) binnen de ±15 werkdagen; None = voorbereiding of nazorg.
FASES = [
    {
        "id": "orienteren", "titel": "Oriënteren en budget", "kort": "Wat wil je, en wat mag het kosten?",
        "dag": None, "balk": "Voorbereiding, vóór dag 1",
        "duur": "1 tot 3 weken", "duur_noot": "eigen inschatting; jij bepaalt het tempo",
        "gebeurt": "<p>Je kijkt wat er mis is met je huidige badkamer en wat je wilt veranderen. Meet de ruimte op: lengte, breedte, hoogte, en waar de deur, het raam en de afvoer zitten. Maak een simpele schets. Bepaal of de indeling gelijk blijft of verandert, want leidingen verplaatsen kost veel meer. Zet daarna een budget op papier, met een buffer voor verrassingen achter de tegels.</p>",
        "jij": ["Maak een schets met maten en foto's van de huidige badkamer.",
                "Schrijf op wat moet en wat leuk is (bijv. inloopdouche moet, vloerverwarming mag).",
                "Is je huis van vóór 1994? Houd rekening met een asbestonderzoek.",
                "Woon je in een appartement? Vraag de regels van de VvE op."],
        "kost": f"Een complete badkamer van 5 tot 9 m² kost meestal <strong>{TOTAAL}</strong>, inclusief sloop, leidingwerk, tegels, sanitair, montage en 21% btw. Houd zelf ongeveer 10% extra achter de hand.",
        "mis": ["Een budget zonder buffer: achter oude tegels zit vaak meer werk dan je denkt.",
                "De indeling omgooien zonder te weten waar de afvoer kan liggen.",
                "Alleen naar plaatjes kijken en niet naar de maten van je eigen ruimte."],
        "links": [("/tools/badkamercalculator/", "Reken je budget uit met de badkamercalculator"),
                  ("/kosten/nieuwe-badkamer/", "Wat kost een nieuwe badkamer?")],
    },
    {
        "id": "offertes", "titel": "Offertes vergelijken", "kort": "Maximaal drie specialisten, één plan.",
        "dag": None, "balk": "Voorbereiding, vóór dag 1",
        "duur": "2 tot 4 weken", "duur_noot": "eigen inschatting: bezoek, uitwerking en vergelijken",
        "gebeurt": "<p>Je vraagt offertes aan op basis van hetzelfde plan, zodat je ze echt kunt vergelijken. De specialisten komen meestal langs om te meten en te kijken naar de leidingen en de ondergrond. Daarna maken ze een offerte. Vergelijk niet alleen de eindprijs. Kijk ook naar wat er wél en níet in staat: sloop, afvoer van puin, afdichting, kitwerk, stelposten en de planning.</p>",
        "jij": ["Geef elke specialist dezelfde schets en wensenlijst.",
                "Vraag naar het afdichtingssysteem, de garantie en een betaalschema.",
                "Leg de offertes naast elkaar en check ze per regel.",
                "Vraag na wat een stelpost precies dekt."],
        "kost": "Offertes aanvragen via Top Badkamers is <strong>gratis en vrijblijvend</strong>. Je krijgt offertes van maximaal drie badkamerspecialisten uit je regio. De offertevergelijker is ook gratis.",
        "mis": ["Offertes op basis van verschillende wensen: dan vergelijk je appels met peren.",
                "Een lage prijs met hoge stelposten, die later alsnog oplopen.",
                "Sloop, puin afvoeren of kitwerk staan er niet in, maar komen wel op de rekening."],
        "links": [("/tools/offertechecker/", "Check je offerte per regel"),
                  ("/offerte-aanvragen/", "Vraag gratis maximaal 3 offertes aan")],
        "extra": "offertes",
    },
    {
        "id": "showroom", "titel": "Keuzes maken in de showroom", "kort": "Tegels, sanitair, kranen en kleuren.",
        "dag": None, "balk": "Voorbereiding, vóór dag 1",
        "duur": "1 tot 2 weken kiezen, plus levertijd", "duur_noot": "levertijden verschillen per product, soms enkele weken",
        "gebeurt": "<p>Nu kies je wat er echt in komt: tegels voor wand en vloer, het toilet, het wastafelmeubel, de douche, kranen en verlichting. Bekijk tegels bij daglicht en bij het licht dat in je badkamer komt. Let op maten: past de deur nog open met een groter meubel, en is er genoeg ruimte voor de toiletpot? Kies je een regendouche, kijk dan naar het verbruik. Een waterbesparende douchekop gebruikt volgens Milieu Centraal 4,0 tot 7,2 liter per minuut.</p>",
        "jij": ["Neem je schets en maten mee naar de showroom.",
                "Vraag naar de levertijd van elk product en zet die op papier.",
                "Spreek af wie wat bestelt: jij of de specialist.",
                "Bestel ongeveer 10% extra tegels voor zaagwerk en latere reparaties."],
        "kost": f"Sanitair kost samen ongeveer <strong>{_p('sanitair')}</strong>, afhankelijk van wat je kiest. Tegels kosten ongeveer <strong>{_p('tegels')} per m²</strong>.",
        "mis": ["Tegels of een douchewand met weken levertijd, terwijl de sloop al gepland staat.",
                "Grote tegels kiezen voor een vloer met afschot: dat vraagt extra zaagwerk of een andere goot.",
                "Een inbouwkraan kiezen nadat de wanden al dicht zijn."],
        "links": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen: waar let je op?"),
                  ("/kennisbank/tegels-kiezen/", "Tegels kiezen voor je badkamer")],
    },
    {
        "id": "planning", "titel": "Planning maken", "kort": "Startdatum, dagplanning en een tijdelijke douche.",
        "dag": None, "balk": "Voorbereiding, vóór dag 1",
        "duur": "1 tot 2 weken vóór de start", "duur_noot": "eigen inschatting",
        "gebeurt": "<p>Je kiest de specialist en spreekt een startdatum af. Vraag om een planning per dag op papier: wanneer wordt er gesloopt, wanneer komt de loodgieter, hoeveel droogtijd zit erin en wanneer is de oplevering. Leg ook vast wat er gebeurt als het uitloopt. Regel nu waar jij en je gezin douchen terwijl de badkamer er niet is.</p>",
        "jij": ["Regel een tijdelijke douche: bij familie, de sportschool of een buurman.",
                "Vraag of het toilet tussendoor bruikbaar blijft.",
                "Vraag een vergunning of melding aan als de gemeente of VvE dat vraagt.",
                "Plan geen vakantie of feest in de weken van de verbouwing."],
        "kost": "Plannen kost niets. Spreek wel een <strong>betaalschema</strong> af dat past bij de voortgang, zodat je nooit het hele bedrag vooraf betaalt.",
        "mis": ["Geen dagplanning: dan weet niemand wie wanneer moet komen.",
                "Geen afspraak over uitloop en meerwerk.",
                "Vergeten dat de buren of de VvE vooraf moeten weten dat er geluid komt."],
        "links": [("/tools/renovatieplanner/", "Maak je eigen planning met de renovatieplanner"),
                  ("/kennisbank/verbouwen-in-vve/", "Verbouwen in een VvE")],
    },
    {
        "id": "slopen", "titel": "Slopen", "kort": "De oude badkamer gaat eruit.",
        "dag": (1, 2), "balk": None,
        "duur": "1 tot 2 dagen", "duur_noot": "eigen inschatting voor 5 tot 9 m²; met asbest of een dekvloer eruit langer",
        "gebeurt": "<p>Water en stroom gaan eraf. Het oude sanitair, de tegels en vaak ook de oude dekvloer worden verwijderd. Het puin gaat in zakken of een container. Pas nu zie je in welke staat de ondergrond, de balken en de leidingen zijn. Soms komt er iets tevoorschijn, zoals een rotte balk of een oude loden leiding. Dan moet er snel een keuze worden gemaakt.</p>",
        "jij": ["Maak de badkamer en de looproute leeg.",
                "Bescherm vloeren in de gang en op de trap.",
                "Spreek af waar de container of de puinzakken staan.",
                "Wees bereikbaar: bij een verrassing moet je snel beslissen."],
        "kost": f"Alleen slopen kost ongeveer <strong>{_p('sloop')}</strong>. Het puin afvoeren kost daarbovenop ongeveer <strong>{_p('afval')}</strong>.",
        "mis": ["Zelf slopen terwijl er asbest in kan zitten: laat dat eerst onderzoeken.",
                "Meerwerk mondeling afspreken: leg het altijd op papier, met de prijs.",
                "Geen stofschot of afdekking, waardoor het stof door het hele huis gaat."],
        "links": [("/kosten/badkamer-slopen/", "Wat kost een badkamer slopen?"),
                  ("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer")],
    },
    {
        "id": "leidingen", "titel": "Leidingwerk en elektra", "kort": "Water, afvoer, stroom en ventilatie.",
        "dag": (3, 5), "balk": None,
        "duur": "2 tot 3 dagen", "duur_noot": "eigen inschatting; plus droogtijd als er een nieuwe dekvloer komt",
        "gebeurt": "<p>De loodgieter legt de waterleidingen en de afvoer aan of verlegt ze. De elektricien trekt nieuwe leidingen voor verlichting, een stopcontact bij de spiegel en eventueel vloerverwarming en een ventilator. Voorzetwanden voor een hangtoilet of inbouwkraan worden nu geplaatst. Komt er een nieuwe dekvloer of een vloer met afschot voor een inloopdouche, dan moet die eerst drogen. Dat kan dagen tot weken extra kosten, afhankelijk van de dikte en het soort vloer.</p>",
        "jij": ["Maak foto's van alle leidingen voordat de wanden dichtgaan.",
                "Check of stopcontacten, schakelaars en lampen op de goede plek komen.",
                "Vraag of de leidingen onder druk getest zijn voordat er getegeld wordt.",
                "Vraag hoeveel droogtijd de vloer krijgt en waarom."],
        "kost": f"Leidingwerk kost ongeveer <strong>{_p('leidingwerk')}</strong>; verplaats je de afvoer of het toilet, dan ligt het hoger. Elektra kost ongeveer <strong>{_p('elektra')}</strong>. Elektrische vloerverwarming kost ongeveer <strong>{_p('vloerverwarming_elektrisch')}</strong>, een ventilator <strong>{_p('ventilator')}</strong>.",
        "mis": ["Leidingen niet testen voordat de wanden dichtgaan.",
                "Een stopcontact te dicht bij de douche: in een badkamer gelden vaste zones (NEN 1010).",
                "Te snel tegelen op een vloer die nog nat is: dan kan de afdichting later loslaten."],
        "links": [("/kosten/uurtarief-loodgieter/", "Uurtarief van een loodgieter"),
                  ("/kosten/vloerverwarming-badkamer/", "Wat kost vloerverwarming in de badkamer?")],
    },
    {
        "id": "tegelen", "titel": "Waterdicht maken en tegelen", "kort": "Eerst de afdichting, dan pas tegels.",
        "dag": (6, 11), "balk": None,
        "duur": "5 tot 6 dagen", "duur_noot": "eigen inschatting, inclusief droogtijd van afdichting en voegen",
        "gebeurt": "<p>Eerst komt de afdichting: een waterdichte laag op de vloer en de douchewanden, met kimband in de hoeken en manchetten rond leidingen. Die moet drogen volgens het technische blad van de fabrikant. Daarna begint de tegelzetter, meestal met de wanden en dan de vloer. Na het tegelen volgt het voegen. Dit is de langste fase. Het is ook de fase waarin later de meeste lekkages ontstaan als het niet goed gebeurt.</p>",
        "jij": ["Kijk mee voordat de tegels op de afdichting gaan, en maak foto's.",
                "Vraag welk afdichtingssysteem gebruikt wordt.",
                "Leg de tegels die je wilt bewaren apart.",
                "Check de voegkleur op een proefstukje."],
        "kost": f"Afdichten kost ongeveer <strong>{_p('waterdicht')}</strong> per badkamer. Tegelzetten kost ongeveer <strong>{_p('tegelwerk')} per m²</strong> arbeid, plus de tegels zelf. Een badkamer van 2 bij 2,5 meter heeft al snel 25 tot 30 m² tegelwerk.",
        "mis": ["Geen afdichting, of alleen in de douchehoek terwijl de hele vloer nat wordt.",
                "Tegelen voordat de afdichting droog is.",
                "Geen afschot naar de goot of put, waardoor er water blijft staan."],
        "links": [("/kennisbank/badkamer-waterdicht-maken/", "Badkamer waterdicht maken"),
                  ("/kosten/tegelzetter-per-m2/", "Wat kost een tegelzetter per m²?")],
        "render": "tegelwerk-badkamer",
    },
    {
        "id": "sanitair", "titel": "Sanitair monteren", "kort": "Toilet, meubel, douche en kranen erin.",
        "dag": (12, 13), "balk": None,
        "duur": "1 tot 2 dagen", "duur_noot": "eigen inschatting",
        "gebeurt": "<p>Als de voegen droog zijn, monteert de installateur het toilet, het wastafelmeubel, de kranen, de douchewand en de douchekop. De radiator, spiegel en verlichting komen er ook in. Daarna gaan water en stroom weer aan en wordt alles getest op lekkage.</p>",
        "jij": ["Controleer bij levering of alles compleet en heel is.",
                "Zet de verpakkingen niet meteen buiten: soms zit er een onderdeel in.",
                "Bewaar handleidingen en garantiebewijzen in één map."],
        "kost": f"Montage kost per onderdeel ongeveer: toilet <strong>{_p('montage_toilet')}</strong>, wastafelmeubel <strong>{_p('montage_meubel')}</strong>, douche <strong>{_p('montage_douche')}</strong>, bad <strong>{_p('montage_bad')}</strong>.",
        "mis": ["Beschadigd sanitair pas na montage ontdekken.",
                "Een kraan of douchewand die niet past bij de inbouwdelen in de wand.",
                "Het toilet niet goed afstellen, waardoor het reservoir blijft doorlopen."],
        "links": [("/badkamerspullen/toilet-kiezen/", "Een toilet kiezen"),
                  ("/badkamerspullen/wastafelmeubel-kiezen/", "Een wastafelmeubel kiezen")],
        "render": "badkamer-installeren",
    },
    {
        "id": "opleveren", "titel": "Kitten en opleveren", "kort": "De laatste naden, en samen controleren.",
        "dag": (14, 15), "balk": None,
        "duur": "1 tot 2 dagen", "duur_noot": "eigen inschatting; kit moet daarna nog uitharden",
        "gebeurt": "<p>Als laatste worden de naden gekit: tussen wand en vloer, rond de douchebak of goot, langs het bad en rond het meubel. Kit moet uitharden voordat je weer gaat douchen; vraag hoe lang. Daarna loop je samen met de specialist de badkamer door. Je test alle kranen, de afvoer, de spoeling, de verlichting en de ventilator. Wat nog niet goed is, zet je op papier, met een datum waarop het klaar is.</p>",
        "jij": ["Loop alles na met een lijst (gebruik de checklist hieronder).",
                "Laat de douche flink lopen en kijk of het water goed wegloopt.",
                "Zet opleverpunten op papier en laat beide partijen tekenen.",
                "Spreek af dat je een klein deel pas betaalt als alle punten klaar zijn."],
        "kost": f"Kitwerk voor een hele badkamer kost ongeveer <strong>{_p('kitwerk_badkamer')}</strong>, als het apart wordt gerekend. De Consumentenbond adviseert: ben je bij de oplevering niet tevreden, houd dan een deel van de betaling in, bijvoorbeeld 5 of 10%.",
        "mis": ["Douchen voordat de kit is uitgehard.",
                "Opleverpunten alleen mondeling afspreken.",
                "Het laatste bedrag betalen terwijl er nog punten openstaan."],
        "links": [("/kosten/kitwerk-voegen/", "Wat kost kitwerk en voegen?")],
    },
    {
        "id": "nazorg", "titel": "Nazorg en garantie", "kort": "Ventileren, onderhoud en je rechten.",
        "dag": None, "balk": "Na dag 15: nazorg",
        "duur": "jaren", "duur_noot": "onderhoud blijft; meld gebreken zo snel mogelijk",
        "gebeurt": "<p>Je badkamer is klaar, maar je bent er nog niet helemaal vanaf. Ventileer goed, zeker in de eerste weken als alles nog droogt. Houd de kitranden en de goot schoon. Zie je na een tijdje een gebrek, zoals een losse tegel of vocht onder de vloer, meld het dan meteen schriftelijk. Sinds 2024 is een aannemer bij een verbouwing ook aansprakelijk voor gebreken die bij de oplevering niet te zien waren, tenzij die niet aan hem te wijten zijn (artikel 7:758 lid 4 BW).</p>",
        "jij": ["Bewaar de offerte, de factuur, het opleverformulier en foto's van de leidingen.",
                "Laat de ventilator lopen en zet na het douchen een raam of rooster open.",
                "Controleer elk jaar de kitranden en vervang kit die loslaat of zwart wordt.",
                "Meld een gebrek per e-mail, met foto's en de datum waarop je het zag."],
        "kost": f"Onderhoud kost weinig. Moet de kit na een aantal jaar opnieuw, dan kost dat ongeveer <strong>{_p('kitwerk')} per meter</strong>.",
        "mis": ["Te lang wachten met het melden van een gebrek.",
                "Garantie van de vakman verwarren met je wettelijke rechten: die gaan altijd door.",
                "Niet ventileren, waardoor schimmel op de voegen en kit ontstaat."],
        "links": [("/kennisbank/garantie-badkamerrenovatie/", "Garantie op een badkamerrenovatie"),
                  ("/kennisbank/badkamer-ventilatie/", "Badkamer ventileren")],
    },
]

# ---------------------------------------------------------------------------
# De badkamer-illustratie (inline SVG): lagen met een fase-bereik (van, tot)
# ---------------------------------------------------------------------------
# Geen <pattern> of id's: dezelfde tekening staat meerdere keren op de pagina.

def _raster(x0, y0, x1, y1, dx, dy, kleur, breedte=1):
    d = ""
    x = x0 + dx
    while x < x1 - 0.5:
        d += f"M{x:g} {y0}V{y1}"
        x += dx
    y = y0 + dy
    while y < y1 - 0.5:
        d += f"M{x0} {y:g}H{x1}"
        y += dy
    return f'<path d="{d}" stroke="{kleur}" stroke-width="{breedte}" fill="none"/>'


def _badge(inhoud):
    return (f'<g transform="translate(372 30)"><rect width="78" height="78" rx="16" fill="#fff" '
            f'stroke="#0b4a56" stroke-width="2"/>{inhoud}</g>')


LAGEN = [
    # Oude badkamer (fase 1–4)
    ((1, 4), '<rect x="20" y="20" width="440" height="260" fill="#efe4c9"/>'
             '<rect x="20" y="130" width="440" height="150" fill="#e6d6ae"/>'
             + _raster(20, 130, 460, 280, 20, 20, "#cdb98a")
             + '<rect x="0" y="280" width="480" height="80" fill="#a77c55"/>'
             + _raster(0, 280, 480, 360, 40, 26, "#8d6644")
             # bad met pootjes
             + '<rect x="36" y="200" width="170" height="56" rx="18" fill="#fbfaf6" stroke="#b9ad92" stroke-width="2"/>'
             '<path d="M52 256v14M190 256v14" stroke="#9a8f78" stroke-width="5" stroke-linecap="round"/>'
             '<path d="M70 200v-36h22" stroke="#9aa4a6" stroke-width="5" fill="none" stroke-linecap="round"/>'
             # staand toilet
             '<rect x="282" y="176" width="44" height="50" rx="6" fill="#fbfaf6" stroke="#b9ad92" stroke-width="2"/>'
             '<path d="M270 226h68a30 26 0 0 1-30 30h-10a28 26 0 0 1-28-30z" fill="#fbfaf6" stroke="#b9ad92" stroke-width="2"/>'
             '<rect x="290" y="256" width="28" height="24" fill="#fbfaf6" stroke="#b9ad92" stroke-width="2"/>'
             # wastafel op zuil
             '<path d="M362 196h80l-8 22h-64z" fill="#fbfaf6" stroke="#b9ad92" stroke-width="2"/>'
             '<rect x="394" y="218" width="16" height="62" fill="#fbfaf6" stroke="#b9ad92" stroke-width="2"/>'
             '<rect x="372" y="120" width="60" height="58" rx="4" fill="#d9e6ea" stroke="#9a8f78" stroke-width="3"/>'),
    ((1, 1), _badge('<rect x="20" y="14" width="38" height="50" rx="4" fill="#fdefe8" stroke="#c4511f" stroke-width="2.5"/>'
                    '<path d="M28 30h22M28 40h22M28 50h12" stroke="#c4511f" stroke-width="2.5" stroke-linecap="round"/>'
                    '<text x="47" y="58" font-size="16" font-weight="800" fill="#0b4a56" font-family="sans-serif">€</text>')),
    ((2, 2), _badge('<rect x="14" y="20" width="30" height="40" rx="3" fill="#fff" stroke="#0b4a56" stroke-width="2"/>'
                    '<rect x="24" y="15" width="30" height="40" rx="3" fill="#fff" stroke="#0b4a56" stroke-width="2"/>'
                    '<rect x="34" y="10" width="30" height="40" rx="3" fill="#fdefe8" stroke="#c4511f" stroke-width="2.5"/>'
                    '<path d="m41 31 6 6 10-12" stroke="#0f8a5f" stroke-width="3" fill="none" stroke-linecap="round"/>')),
    ((3, 3), _badge('<rect x="12" y="14" width="24" height="24" rx="3" fill="#d9dfd8"/><rect x="42" y="14" width="24" height="24" rx="3" fill="#6f7a7c"/>'
                    '<rect x="12" y="42" width="24" height="24" rx="3" fill="#c9a77c"/><rect x="42" y="42" width="24" height="24" rx="3" fill="#2f5d62"/>')),
    ((4, 4), _badge('<rect x="13" y="18" width="52" height="46" rx="5" fill="#fff" stroke="#0b4a56" stroke-width="2.5"/>'
                    '<path d="M13 30h52M26 12v10M52 12v10" stroke="#0b4a56" stroke-width="2.5" stroke-linecap="round"/>'
                    '<rect x="22" y="37" width="9" height="8" fill="#c4511f"/><rect x="35" y="37" width="9" height="8" fill="#c4511f"/>'
                    '<rect x="48" y="37" width="9" height="8" fill="#e8b49b"/><rect x="22" y="50" width="9" height="8" fill="#e8b49b"/>')),
    # Kaal (vanaf fase 5)
    ((5, 10), '<rect x="20" y="20" width="440" height="260" fill="#d3d6d5"/>'
              '<path d="M60 60l14 8M150 90l-9 12M330 70l12 6M240 200l-10 9M410 230l8 10" stroke="#b8bdbb" stroke-width="2"/>'
              '<rect x="0" y="280" width="480" height="80" fill="#b9bebd"/>'),
    # Puin en sloopgereedschap (alleen fase 5)
    ((5, 5), '<path d="M60 280l18-16 14 8 12-12 20 20z" fill="#9aa09e"/><path d="M300 280l10-10 12 6 10-8 16 12z" fill="#a9aeac"/>'
             '<path d="M380 280c-6-40 4-62 26-66l26 2c16 10 20 32 12 64z" fill="#f2f2ee" stroke="#9aa09e" stroke-width="2"/>'
             '<path d="M392 222c10-6 30-6 42 2" stroke="#9aa09e" stroke-width="2" fill="none"/>'
             '<path d="M160 270l60-36" stroke="#6b4b2e" stroke-width="7" stroke-linecap="round"/>'
             '<rect x="210" y="222" width="26" height="16" rx="3" transform="rotate(-31 223 230)" fill="#55696e"/>'),
    # Leidingen, elektra en voorzetwand (vanaf fase 6, later achter de tegels)
    ((6, 10), '<path d="M104 280V176h0" stroke="#2e7dd7" stroke-width="6" fill="none"/>'
              '<path d="M118 280V176" stroke="#d64b3a" stroke-width="6" fill="none"/>'
              '<path d="M111 176V80h20" stroke="#2e7dd7" stroke-width="5" fill="none"/>'
              '<rect x="96" y="166" width="30" height="16" rx="4" fill="#8f9a9c"/>'
              '<rect x="270" y="130" width="80" height="150" fill="none" stroke="#e39a52" stroke-width="5"/>'
              '<path d="M270 170h80M270 220h80" stroke="#e39a52" stroke-width="3"/>'
              '<path d="M310 280v-30" stroke="#7c8587" stroke-width="12"/>'
              '<path d="M396 280v-66M412 280v-66" stroke="#2e7dd7" stroke-width="5"/><path d="M412 280v-66" stroke="#d64b3a" stroke-width="5"/>'
              '<path d="M404 280v-48" stroke="#7c8587" stroke-width="9"/>'
              '<path d="M240 20v20h160v60M300 40v-20" stroke="#e8b923" stroke-width="3" stroke-dasharray="7 5" fill="none"/>'
              '<circle cx="400" cy="104" r="7" fill="#fff" stroke="#e8b923" stroke-width="3"/>'
              '<circle cx="300" cy="34" r="7" fill="#fff" stroke="#e8b923" stroke-width="3"/>'
              '<rect x="232" y="34" width="34" height="24" rx="4" fill="#fff" stroke="#8f9a9c" stroke-width="3"/>'),
    # Afdichting in de douchezone (vanaf fase 7; alleen zichtbaar zolang er nog niet getegeld is)
    ((7, 10), '<rect x="20" y="60" width="180" height="220" fill="#5fa3b5" opacity=".85"/>'
              '<rect x="0" y="280" width="480" height="80" fill="#5fa3b5" opacity=".7"/>'
              '<path d="M20 60V280M200 60V280M0 282H480" stroke="#e8f1f3" stroke-width="5" opacity=".9"/>'),
    # Tegels rechts van de douche en op de vloer (vanaf fase 7)
    ((7, 10), '<rect x="200" y="20" width="260" height="260" fill="#eceee9"/>'
              + _raster(200, 20, 460, 280, 52, 32, "#d3d7d1")
              + '<rect x="0" y="280" width="480" height="80" fill="#6f7a7c"/>'
              + _raster(0, 280, 480, 360, 60, 40, "#5d6769")),
    # Douchewand half betegeld (alleen fase 7) met tegelstapel
    ((7, 7), '<rect x="20" y="184" width="180" height="96" fill="#eceee9"/>'
             + _raster(20, 184, 200, 280, 45, 32, "#d3d7d1")
             + '<rect x="214" y="250" width="56" height="30" fill="#d9dcd6" stroke="#b5bab3" stroke-width="2"/>'
             '<path d="M214 260h56M214 270h56" stroke="#b5bab3" stroke-width="2"/>'),
    # Douchewand volledig betegeld (vanaf fase 8)
    ((8, 10), '<rect x="20" y="20" width="180" height="260" fill="#e3e6e0"/>'
              + _raster(20, 20, 200, 280, 45, 32, "#cdd2cb")),
    # Sanitair (vanaf fase 8)
    ((8, 10), '<path d="M120 52v18h-6" stroke="#2a2f30" stroke-width="5" fill="none" stroke-linecap="round"/>'
              '<rect x="72" y="66" width="56" height="9" rx="4" fill="#2a2f30"/>'
              '<rect x="104" y="160" width="14" height="26" rx="4" fill="#2a2f30"/>'
              '<rect x="196" y="56" width="6" height="224" fill="#2a2f30"/>'
              '<rect x="140" y="56" width="58" height="224" fill="#bfe0e8" opacity=".35"/>'
              '<rect x="50" y="272" width="110" height="6" rx="3" fill="#2a2f30"/>'
              # radiator
              '<rect x="218" y="110" width="36" height="120" rx="5" fill="none" stroke="#2a2f30" stroke-width="4"/>'
              '<path d="M218 140h36M218 170h36M218 200h36" stroke="#2a2f30" stroke-width="4"/>'
              # hangtoilet met bedieningsplaat
              '<rect x="296" y="140" width="28" height="18" rx="3" fill="#fff" stroke="#9aa1a3" stroke-width="2"/>'
              '<path d="M278 200h66v6a30 26 0 0 1-30 26h-16a20 20 0 0 1-20-20z" fill="#fff" stroke="#9aa1a3" stroke-width="2"/>'
              # wastafelmeubel en spiegel
              '<rect x="362" y="196" width="88" height="40" rx="3" fill="#b88a5a"/>'
              '<rect x="358" y="188" width="96" height="10" rx="3" fill="#fff" stroke="#c9ccc8" stroke-width="2"/>'
              '<path d="M406 188v-14h10" stroke="#2a2f30" stroke-width="4" fill="none" stroke-linecap="round"/>'
              '<rect x="370" y="78" width="72" height="88" rx="10" fill="#dcebef" stroke="#2a2f30" stroke-width="3"/>'
              '<path d="M384 96l18-12M384 112l30-20" stroke="#fff" stroke-width="3" stroke-linecap="round"/>'),
    # Kitwerk gemarkeerd (alleen fase 9)
    ((9, 9), '<path d="M20 279H460M200 56V280M362 237H450M278 233h66" stroke="#c4511f" stroke-width="4" '
             'stroke-dasharray="10 6" stroke-linecap="round"/>'
             + _badge('<path d="m22 40 12 12 22-26" stroke="#0f8a5f" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')),
    # Lampen aan (vanaf fase 9)
    ((9, 10), '<circle cx="300" cy="24" r="22" fill="#ffe9a8" opacity=".7"/><rect x="286" y="20" width="28" height="7" rx="3" fill="#fff" stroke="#c9ccc8"/>'
              '<circle cx="406" cy="72" r="14" fill="#ffe9a8" opacity=".8"/>'),
    # Nazorg: handdoeken, plant en schild (fase 10)
    ((10, 10), '<rect x="222" y="118" width="28" height="56" rx="4" fill="#c4511f" opacity=".9"/>'
               '<rect x="226" y="176" width="24" height="40" rx="4" fill="#f0a37f"/>'
               '<rect x="372" y="168" width="18" height="20" rx="3" fill="#d9c7a8"/>'
               '<path d="M381 168c-10-14-6-26 0-30 6 4 10 16 0 30zM381 168c6-14 18-18 22-14-2 8-12 14-22 14z" fill="#3f8a5f"/>'
               + _badge('<path d="M39 14l20 8v16c0 13-9 22-20 26-11-4-20-13-20-26V22z" fill="#e7f7ef" stroke="#0f8a5f" stroke-width="3"/>'
                        '<path d="m30 38 7 7 12-14" stroke="#0f8a5f" stroke-width="4" fill="none" stroke-linecap="round"/>')),
]

KADER = '<rect x="20" y="20" width="440" height="260" fill="none" stroke="#0b4a56" stroke-width="3"/>' \
        '<path d="M0 280H480" stroke="#0b4a56" stroke-width="3"/>'


def _svg(fase=None, klasse="vl-svg"):
    """fase=None: alle lagen met data-van/data-tot (sticky versie). Anders alleen de lagen van die fase."""
    delen = []
    for (van, tot), inhoud in LAGEN:
        if fase is None:
            uit = "" if van <= 1 <= tot else " vl-uit"
            delen.append(f'<g class="vl-g{uit}" data-van="{van}" data-tot="{tot}">{inhoud}</g>')
        elif van <= fase <= tot:
            delen.append(f"<g>{inhoud}</g>")
    label = ("Getekende badkamer die per fase verandert: van oude badkamer via kale muren, leidingen "
             "en afdichting naar tegels en nieuw sanitair") if fase is None else \
        f"Tekening van de badkamer in fase {fase}: {FASES[fase - 1]['titel'].lower()}"
    return (f'<svg class="{klasse}" viewBox="0 0 480 360" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(delen)}{KADER}</svg>')


# ---------------------------------------------------------------------------
# Checklist
# ---------------------------------------------------------------------------
CHECKLIST = [
    ("Voorbereiding", [
        "Badkamer opgemeten en schets gemaakt",
        "Budget bepaald, met ongeveer 10% buffer",
        "Asbest en VvE-regels nagevraagd (indien van toepassing)",
        "Offertes van maximaal drie specialisten op basis van hetzelfde plan",
        "Offertes per regel vergeleken (sloop, afvoer, afdichting, kitwerk, stelposten)",
        "Tegels en sanitair gekozen, levertijden op papier",
        "Dagplanning en betaalschema schriftelijk vastgelegd",
        "Tijdelijke douche en toilet geregeld",
    ]),
    ("Tijdens de verbouwing", [
        "Badkamer en looproute leeg, vloeren beschermd",
        "Meerwerk alleen schriftelijk en met prijs afgesproken",
        "Foto's gemaakt van alle leidingen voordat de wanden dichtgaan",
        "Afdichting gezien en gefotografeerd voordat er getegeld werd",
        "Sanitair bij levering gecontroleerd op schade",
    ]),
    ("Oplevering", [
        "Kranen, afvoer, spoeling, licht en ventilator getest",
        "Opleverpunten op papier, door beide partijen getekend",
        "Laatste deel pas betaald toen alle punten klaar waren",
    ]),
    ("Nazorg", [
        "Offerte, factuur, opleverformulier en handleidingen in één map",
        "Herinnering gezet om elk jaar de kitranden te controleren",
    ]),
]


def _checklist_html():
    n = 0
    groepen = ""
    for kop, items in CHECKLIST:
        li = ""
        for t in items:
            n += 1
            li += (f'<li><label><input type="checkbox" data-k="c{n}"><span class="vl-vink" aria-hidden="true"></span>'
                   f'<span>{t}</span></label></li>')
        groepen += f'<div class="vl-cgroep"><h3>{kop}</h3><ul>{li}</ul></div>'
    return n, groepen


# ---------------------------------------------------------------------------
# HTML per fase
# ---------------------------------------------------------------------------

def _dag_label(f):
    if f["dag"]:
        a, b = f["dag"]
        return f"Dag {a}–{b} van ±{TOTAAL_DAGEN}" if a != b else f"Dag {a} van ±{TOTAAL_DAGEN}"
    return f["balk"]


def _render(sleutel, sizes):
    r = RENDERS.get(sleutel)
    return render_beeld(r, sizes) if r else ""


def _fase_html(i, f):
    nr = i + 1
    jij = "".join(f"<li>{t}</li>" for t in f["jij"])
    mis = "".join(f"<li>{t}</li>" for t in f["mis"])
    links = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in f["links"])
    extra = ""
    if f.get("extra") == "offertes":
        extra = (offertecheck_blok("je badkamer")
                 + cta_midden("Nog geen offertes?",
                              "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit je regio.",
                              "Gratis 3 offertes aanvragen"))
    render = ""
    if f.get("render"):
        render = f'<div class="vl-render">{_render(f["render"], "(max-width: 960px) 100vw, 560px")}</div>'
    eind = (f["dag"][1] if f["dag"] else (0 if nr < 5 else TOTAAL_DAGEN))
    return f"""<article class="vl-fase" id="fase-{f['id']}" data-fase="{nr}" data-eind="{eind}" data-label="{_dag_label(f)}">
  <figure class="vl-mob">{_svg(nr, "vl-svg-mob")}<figcaption>Illustratie: fase {nr}</figcaption></figure>
  <header class="vl-kop">
    <span class="vl-nr" aria-hidden="true">{nr}</span>
    <div><p class="vl-boven">Fase {nr} van 10 · {_dag_label(f)}</p>
    <h2>{f['titel']}</h2><p class="vl-kort">{f['kort']}</p></div>
  </header>
  <p class="vl-duur"><strong>Richtduur:</strong> {f['duur']} <span>({f['duur_noot']})</span></p>
  <h3 class="vl-h">Wat er gebeurt</h3>
  {f['gebeurt']}
  {render}
  <div class="vl-blokken">
    <div class="vl-blok vl-jij"><h3>Wat jij doet of regelt</h3><ul class="checklist">{jij}</ul></div>
    <div class="vl-blok vl-kost"><h3>Wat het ongeveer kost</h3><p>{f['kost']}</p></div>
    <div class="vl-blok vl-mis"><h3>Waar het vaak misgaat</h3><ul>{mis}</ul></div>
  </div>
  {extra}
  <ul class="vl-links">{links}</ul>
</article>"""


# ---------------------------------------------------------------------------
# CSS en JS
# ---------------------------------------------------------------------------
CSS = """<style>
.vl-hero{display:grid;gap:28px;align-items:center}
@media(min-width:900px){.vl-hero{grid-template-columns:1.05fr .95fr}}
.vl-hero .lead{max-width:56ch}
.vl-inhoud{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0;margin:18px 0 0}
.vl-inhoud a{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:99px;padding:6px 12px;font-size:.88rem;font-weight:650;color:var(--ink);background:#fff}
.vl-inhoud a:hover{border-color:var(--accent);text-decoration:none}
.vl-inhoud b{display:inline-grid;place-items:center;width:20px;height:20px;border-radius:50%;background:var(--accent-soft);color:#9c4019;font-size:.72rem}
.vl-grid{display:block}
.vl-zij{display:none}
.vl-mob{margin:0 0 16px;background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius);padding:10px;position:relative}
.vl-mob figcaption{position:absolute;left:18px;bottom:16px;background:rgba(255,255,255,.9);color:#334;font-size:.72rem;padding:2px 8px;border-radius:99px}
.vl-svg,.vl-svg-mob{display:block;width:100%;height:auto;aspect-ratio:4/3}
.vl-g{transition:opacity .55s ease}
.vl-uit{opacity:0}
/* Voortgangsbalk */
.vl-voortgang{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:10px 14px;box-shadow:0 6px 20px rgba(8,47,55,.08)}
.vl-vt-tekst{display:flex;justify-content:space-between;gap:10px;font-size:.86rem;color:var(--ink);font-weight:700;margin:0 0 6px}
.vl-vt-tekst span:last-child{color:var(--muted);font-weight:600;text-align:right}
.vl-vt-baan{height:8px;border-radius:8px;background:var(--bg-soft);overflow:hidden;box-shadow:inset 0 0 0 1px var(--line)}
.vl-vt-balk{display:block;height:100%;width:0;background:linear-gradient(90deg,var(--accent),#f0a37f);border-radius:8px;transition:width .5s ease}
.vl-stippen{display:flex;gap:4px;margin:8px 0 0;padding:0;list-style:none}
.vl-stippen a{display:block;flex:1;height:6px;border-radius:6px;background:var(--line)}
.vl-stippen a.af{background:#f0a37f}.vl-stippen a.nu{background:var(--accent)}
.vl-mobbalk{position:sticky;top:var(--vl-top,64px);z-index:20;margin:0 0 18px}
/* Fases */
.vl-fase{padding:30px 0 36px;border-bottom:1px solid var(--line);scroll-margin-top:140px}
.vl-fase:last-child{border-bottom:0}
.vl-kop{display:flex;gap:14px;align-items:flex-start}
.vl-nr{flex:0 0 44px;height:44px;border-radius:50%;display:grid;place-items:center;background:var(--ink);color:#fff;font-weight:800;font-size:1.1rem;transition:background .3s}
.vl-fase.actief .vl-nr{background:var(--accent)}
.vl-boven{margin:0 0 2px;font-size:.78rem;font-weight:750;text-transform:uppercase;letter-spacing:.04em;color:var(--accent-dark)}
.vl-kop h2{margin:0 0 4px;font-size:1.55rem}
.vl-kort{margin:0;color:var(--muted)}
.vl-duur{margin:14px 0 8px;font-size:.95rem;background:var(--bg-soft);border-radius:10px;padding:8px 12px}
.vl-duur span{color:var(--muted);font-size:.86rem}
.vl-h{font-size:1.08rem;margin:16px 0 6px}
.vl-blokken{display:grid;gap:12px;margin:16px 0}
@media(min-width:640px){.vl-blokken{grid-template-columns:1fr 1fr}.vl-jij{grid-row:span 2}}
.vl-blok{border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;background:#fff}
.vl-blok h3{font-size:.98rem;margin:0 0 8px}
.vl-blok ul{margin:0;padding-left:18px;font-size:.94rem}
.vl-blok .checklist{padding-left:0}
.vl-blok p{margin:0;font-size:.94rem}
.vl-kost{background:#fffaf6;border-color:#f3d6c6}
.vl-mis{background:#fff6f4;border-color:#f1d0c8}
.vl-mis li::marker{color:var(--accent)}
.vl-render{margin:16px 0}
.vl-links{list-style:none;padding:0;margin:12px 0 0;display:flex;flex-wrap:wrap;gap:8px 18px;font-size:.93rem}
.vl-links a{font-weight:650}
.vl-links a::after{content:" →"}
.vl-fase .ocb,.vl-fase .cta-midden{margin:18px 0}
/* Desktop: sticky tekening naast de tekst (alleen met JS) */
@media(min-width:960px){
  .vl-js .vl-grid{display:grid;grid-template-columns:minmax(0,1fr) 430px;gap:48px;align-items:start}
  .vl-js .vl-zij{display:block;position:sticky;top:calc(var(--vl-top,64px) + 16px)}
  .vl-js .vl-mob,.vl-js .vl-mobbalk{display:none}
  .vl-tekening{background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius-lg);padding:14px;margin:12px 0 0;position:relative}
  .vl-tekening figcaption{font-size:.78rem;color:var(--muted);margin:8px 2px 0}
  .vl-zij-titel{font-weight:800;color:var(--ink);margin:12px 2px 0;font-size:1.05rem}
}
/* Checklist */
.vl-check{border:1px solid var(--line);border-radius:var(--radius-lg);padding:20px;background:#fff}
.vl-check-kop{display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;margin-bottom:12px}
.vl-check-kop p{margin:0;font-weight:700;color:var(--ink)}
.vl-cgroepen{display:grid;gap:8px 28px}
@media(min-width:760px){.vl-cgroepen{grid-template-columns:1fr 1fr}}
.vl-cgroep h3{font-size:1rem;margin:12px 0 6px}
.vl-cgroep ul{list-style:none;padding:0;margin:0}
.vl-cgroep li{margin:0 0 6px}
.vl-cgroep label{font-weight:500;display:flex;gap:10px;align-items:flex-start;cursor:pointer;font-size:.95rem;line-height:1.45;padding:4px 0}
.vl-cgroep input{position:absolute;opacity:0;width:1px;height:1px}
.vl-vink{flex:0 0 22px;height:22px;border:2px solid #9fb3b7;border-radius:6px;display:grid;place-items:center;background:#fff;transition:background .2s,border-color .2s}
.vl-cgroep input:checked+.vl-vink{background:var(--green);border-color:var(--green)}
.vl-cgroep input:checked+.vl-vink::after{content:"";width:6px;height:11px;border:solid #fff;border-width:0 3px 3px 0;transform:rotate(45deg) translate(-1px,-1px)}
.vl-cgroep input:checked~span:last-child{color:var(--muted);text-decoration:line-through}
.vl-cgroep input:focus-visible+.vl-vink{outline:3px solid var(--accent);outline-offset:2px}
.vl-knoppen{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.vl-bronnen{font-size:.88rem}
.vl-bronnen li{margin-bottom:4px}
@media(prefers-reduced-motion:reduce){.vl-g,.vl-vt-balk,.vl-nr,.vl-vink{transition:none}}
@media print{
  .header,.footer,.sticky-cta,.crumbs,.vl-zij,.vl-mob,.vl-mobbalk,.vl-knoppen,.cta,.cta-midden,.ocb,.faq,.vl-hero figure,.vl-render,.vl-inhoud,.vl-geenprint,.vl-links{display:none!important}
  body{font-size:11pt;color:#000}
  .section,.section-sm{padding:8px 0}
  .vl-grid{display:block!important}
  .vl-fase{padding:10px 0;break-inside:avoid}
  .vl-blok{border:1px solid #999;break-inside:avoid}
  .vl-check{border:0;padding:0;break-before:page}
  .vl-cgroep input:checked~span:last-child{text-decoration:none;color:#000}
  .vl-vink{border:1.5px solid #000}
  .reveal{opacity:1!important;transform:none!important}
  a{color:#000;text-decoration:none}
}
</style>"""

JS = """<script>
(function(){
  var root=document.getElementById('vl');
  if(!root)return;
  root.classList.add('vl-js');
  var TOT=%d;
  var hdr=document.querySelector('.header');
  function zetTop(){var h=hdr?hdr.offsetHeight:64;document.documentElement.style.setProperty('--vl-top',h+'px');}
  zetTop();window.addEventListener('resize',zetTop);
  var fases=[].slice.call(root.querySelectorAll('.vl-fase'));
  var lagen=[].slice.call(root.querySelectorAll('.vl-zij .vl-g'));
  var balken=[].slice.call(root.querySelectorAll('.vl-vt-balk'));
  var teksten=[].slice.call(root.querySelectorAll('[data-vt-tekst]'));
  var fasetekst=[].slice.call(root.querySelectorAll('[data-vt-fase]'));
  var stippen=[].slice.call(root.querySelectorAll('.vl-stippen'));
  var titel=root.querySelector('.vl-zij-titel');
  var huidig=0;
  function toon(n){
    if(n===huidig)return;huidig=n;
    var el=fases[n-1];if(!el)return;
    lagen.forEach(function(g){var v=+g.getAttribute('data-van'),t=+g.getAttribute('data-tot');g.classList.toggle('vl-uit',!(n>=v&&n<=t));});
    var pct=Math.min(100,Math.round(+el.getAttribute('data-eind')/TOT*100));
    balken.forEach(function(b){b.style.width=pct+'%%';});
    teksten.forEach(function(t){t.textContent=el.getAttribute('data-label');});
    var naam=el.querySelector('h2').textContent;
    fasetekst.forEach(function(t){t.textContent='Fase '+n+': '+naam;});
    if(titel)titel.textContent=naam;
    stippen.forEach(function(s){[].slice.call(s.children).forEach(function(li,i){var a=li.firstChild;a.classList.toggle('af',i<n-1);a.classList.toggle('nu',i===n-1);});});
    fases.forEach(function(f,i){f.classList.toggle('actief',i===n-1);});
  }
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(items){
      items.forEach(function(it){if(it.isIntersecting)toon(+it.target.getAttribute('data-fase'));});
    },{rootMargin:'-40%% 0px -55%% 0px',threshold:0});
    fases.forEach(function(f){io.observe(f);});
  }
  toon(1);
  /* Checklist met voortgang in localStorage */
  var KEY='tb-verloop-checklist-v1';
  var vakjes=[].slice.call(document.querySelectorAll('.vl-check input[type=checkbox]'));
  var teller=document.getElementById('vl-teller');
  var cbalk=document.getElementById('vl-cbalk');
  var staat={};
  try{staat=JSON.parse(localStorage.getItem(KEY)||'{}')||{};}catch(e){staat={};}
  function telOp(){
    var n=vakjes.filter(function(v){return v.checked;}).length;
    if(teller)teller.textContent=n+' van '+vakjes.length+' afgevinkt';
    if(cbalk)cbalk.style.width=Math.round(n/vakjes.length*100)+'%%';
  }
  vakjes.forEach(function(v){
    v.checked=!!staat[v.getAttribute('data-k')];
    v.addEventListener('change',function(){
      staat[v.getAttribute('data-k')]=v.checked;
      try{localStorage.setItem(KEY,JSON.stringify(staat));}catch(e){}
      telOp();
    });
  });
  telOp();
  var wis=document.getElementById('vl-wis');
  if(wis)wis.addEventListener('click',function(){
    staat={};vakjes.forEach(function(v){v.checked=false;});
    try{localStorage.removeItem(KEY);}catch(e){}
    telOp();
  });
  var pr=document.getElementById('vl-print');
  if(pr)pr.addEventListener('click',function(){window.print();});
})();
</script>""" % TOTAAL_DAGEN


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------
FAQS = [
    ("Hoe lang duurt een complete badkamerrenovatie?",
     "Reken voor een complete badkamer op ongeveer drie weken werk, ofwel zo'n 15 werkdagen. Homedeal noemt voor een complete verbouwing twee tot drie weken of langer. Een nieuwe dekvloer, asbest of meerwerk kan het langer maken. De voorbereiding, van oriënteren tot planning, kost daarnaast vaak enkele weken."),
    ("Kan ik thuis blijven wonen tijdens de verbouwing?",
     "Ja, dat doen de meeste mensen. Regel wel een andere plek om te douchen, bijvoorbeeld bij familie of de sportschool. Vraag de specialist of het toilet tussendoor bruikbaar blijft, zeker als er geen tweede toilet in huis is."),
    ("Wat is de langste fase van een badkamerrenovatie?",
     "Meestal het waterdicht maken en tegelen. De afdichting moet drogen voordat de tegels erop gaan, en na het tegelen moeten de voegen nog drogen. Komt er een nieuwe dekvloer, dan kan de droogtijd van die vloer nog langer duren."),
    ("Wanneer moet ik tegels en sanitair bestellen?",
     "Voordat de sloop begint. Sommige tegels, douchewanden en kranen hebben weken levertijd. Vraag de levertijd van elk product en zet die naast de planning."),
    ("Hoeveel offertes moet ik aanvragen?",
     "Twee of drie offertes op basis van hetzelfde plan zijn genoeg om goed te vergelijken. Via Top Badkamers vraag je gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Met de offertevergelijker check je daarna per regel wat er in staat."),
    ("Wat doe ik als er na de oplevering iets mis is?",
     "Maak foto's, noteer de datum en meld het gebrek zo snel mogelijk per e-mail of brief aan de specialist. Een garantie van de vakman komt bovenop je wettelijke rechten en kan die niet beperken. Lees meer op de pagina over garantie op een badkamerrenovatie."),
]


# ---------------------------------------------------------------------------
# Pagina
# ---------------------------------------------------------------------------

def _bronnen():
    lijst = [BRON_HOMEDEAL, BRON_CB, BRON_MC]
    gezien = {u for _, u in lijst}
    for k in ["sloop", "afval", "leidingwerk", "elektra", "waterdicht", "tegelwerk", "tegels",
              "sanitair", "montage_toilet", "montage_douche", "kitwerk_badkamer", "kitwerk",
              "vloerverwarming_elektrisch", "ventilator"]:
        for naam, url in RP.bron_links(k):
            if url and url not in gezien:
                gezien.add(url)
                lijst.append((naam, url))
    return lijst


def _platte_tekst(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def build(write):
    today = date.today().isoformat()
    cr, cr_ld = crumbs([("Home", "/"), ("Zo verloopt je verbouwing", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over het verloop")
    aantal, checklist = _checklist_html()
    bronnen = _bronnen()
    bron_li = "".join(f'<li><a href="{u}" rel="noopener">{n}</a></li>' for n, u in bronnen)

    inhoud = "".join(f'<li><a href="#fase-{f["id"]}"><b>{i + 1}</b>{f["titel"]}</a></li>' for i, f in enumerate(FASES))
    stippen = "".join(f'<li style="flex:1"><a href="#fase-{f["id"]}" aria-label="Naar fase {i + 1}: {f["titel"]}"></a></li>'
                      for i, f in enumerate(FASES))
    stippen = f'<ul class="vl-stippen">{stippen}</ul>'.replace('<a href', '<a class="" href')

    def voortgang():
        return (f'<div class="vl-voortgang" aria-live="polite"><p class="vl-vt-tekst"><span data-vt-fase>Fase 1: {FASES[0]["titel"]}</span>'
                f'<span data-vt-tekst>{FASES[0]["balk"]}</span></p>'
                f'<div class="vl-vt-baan" role="presentation"><span class="vl-vt-balk"></span></div>{stippen}</div>')

    fases_html = "".join(_fase_html(i, f) for i, f in enumerate(FASES))
    hero_render = _render("badkamer-renoveren", "(max-width: 900px) 100vw, 520px")
    if hero_render:
        hero_render = hero_render.replace('loading="lazy"', 'loading="eager" fetchpriority="high"')

    feiten = feiten_blok([
        ("10", "fases, van eerste idee tot nazorg"),
        (f"±{TOTAAL_DAGEN}", "werkdagen voor een complete badkamer"),
        (TOTAAL.replace(" – ", "–"), "richtprijs complete badkamer, incl. btw"),
        ("max. 3", "gratis offertes van specialisten"),
    ], bron="Werkdagen: eigen verdeling binnen de 2 tot 3+ weken die Homedeal noemt voor een complete verbouwing. Richtprijs: zie de bronnen onderaan.")

    body = f"""{CSS}{cr}
<section class="section-sm"><div class="wrap">
  <div class="vl-hero">
    <div>
      <span class="badge">Stap voor stap</span>
      <h1>Zo verloopt je badkamerverbouwing, van plan tot nazorg</h1>
      <p class="lead">Een nieuwe badkamer is geen klus van één dag. Het is een reeks stappen die op elkaar wachten: eerst plannen en kiezen, dan slopen, leidingen, afdichten, tegelen en monteren. Scroll mee en zie de badkamer fase voor fase veranderen. Per fase lees je wat er gebeurt, hoe lang het duurt, wat het ongeveer kost, wat jij regelt en waar het vaak misgaat.</p>
      <ul class="vl-inhoud">{inhoud}</ul>
    </div>
    {hero_render}
  </div>
  <div style="margin-top:28px">{feiten}</div>
</div></section>

<section class="section-sm" style="padding-top:0"><div class="wrap">
  <div id="vl">
    <div class="vl-grid">
      <div class="vl-tekst">
        <div class="vl-mobbalk">{voortgang()}</div>
        {fases_html}
      </div>
      <aside class="vl-zij" aria-label="Voortgang en tekening">
        {voortgang()}
        <figure class="vl-tekening">{_svg()}<figcaption>Illustratie: dezelfde badkamer in elke fase. Scroll om te zien wat er verandert.</figcaption></figure>
        <p class="vl-zij-titel">{FASES[0]['titel']}</p>
      </aside>
    </div>
  </div>
</div></section>

<section class="section soft" id="checklist"><div class="wrap narrow">
  <h2>Checklist voor je verbouwing</h2>
  <p>Vink af wat je geregeld hebt. Je voortgang wordt alleen in deze browser bewaard. Je kunt de lijst ook printen en op de deur van de badkamer hangen.</p>
  <div class="vl-check">
    <div class="vl-check-kop"><p id="vl-teller">0 van {aantal} afgevinkt</p>
      <div class="vl-vt-baan" style="flex:1;min-width:140px;max-width:260px"><span class="vl-vt-balk" id="vl-cbalk"></span></div></div>
    <div class="vl-cgroepen">{checklist}</div>
    <div class="vl-knoppen">
      <button type="button" class="btn btn-primary" id="vl-print">Print de checklist</button>
      <button type="button" class="btn btn-ghost" id="vl-wis">Alles uitvinken</button>
    </div>
  </div>
  <p style="margin-top:18px">Wil je een planning met je eigen data? Gebruik de <a href="/tools/renovatieplanner/">renovatieplanner</a>. De vaste volgorde en de droogtijden lees je in <a href="/kennisbank/volgorde-badkamerrenovatie/">de volgorde van een badkamerrenovatie</a>.</p>
</div></section>

<section class="section-sm vl-geenprint"><div class="wrap narrow">
  <h2>Kosten op een rij</h2>
  <p>Alle bedragen op deze pagina zijn richtprijzen, inclusief 21% btw. Je eigen badkamer kan hoger of lager uitkomen. Meer uitleg en rekenvoorbeelden vind je hier:</p>
  <ul>
    <li><a href="/kosten/nieuwe-badkamer/">Wat kost een nieuwe badkamer?</a></li>
    <li><a href="/kosten/badkamer-slopen/">Wat kost een badkamer slopen?</a></li>
    <li><a href="/kosten/tegelzetter-per-m2/">Wat kost een tegelzetter per m²?</a></li>
    <li><a href="/kosten/kitwerk-voegen/">Wat kost kitwerk en voegen?</a></li>
    <li><a href="/prijzen/">Alle prijzen</a></li>
  </ul>
  <h3>Bronnen</h3>
  <p class="vl-bronnen">Geraadpleegd in november 2026. De verdeling over werkdagen is een eigen inschatting binnen de doorlooptijd die Homedeal noemt.</p>
  <ul class="vl-bronnen">{bron_li}</ul>
</div></section>
{faq_html}
{cta_blok("Klaar voor fase 2?", "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit jouw regio. Zo vergelijk je op basis van hetzelfde plan.")}
{JS}"""

    howto = {
        "@context": "https://schema.org", "@type": "HowTo",
        "name": "Zo verloopt een badkamerrenovatie",
        "description": "Het traject van een badkamerrenovatie in tien fases, van oriënteren en budget tot nazorg en garantie.",
        "inLanguage": "nl-NL",
        "totalTime": "P3W",
        "estimatedCost": {"@type": "MonetaryAmount", "currency": "EUR",
                          "minValue": _TOT["prijs_van"], "maxValue": _TOT["prijs_tot"]},
        "step": [
            {"@type": "HowToStep", "position": i + 1, "name": f["titel"],
             "text": _platte_tekst(f["gebeurt"]), "url": f"{SITE['url']}{PAD}#fase-{f['id']}"}
            for i, f in enumerate(FASES)
        ],
        "datePublished": GEPUBLICEERD, "dateModified": today,
    }
    titel = title("Zo verloopt je badkamerverbouwing, fase voor fase")
    beschrijving = ("Van oriënteren en offertes tot slopen, tegelen, opleveren en nazorg: zo verloopt een "
                    "badkamerrenovatie in tien fases, met duur, kosten en een checklist.")
    write(PAD, page(titel, beschrijving, PAD, body, [cr_ld, howto, faq_ld]), prio=0.7)
