# -*- coding: utf-8 -*-
"""Kennisbank ronde 3: tien extra artikelen voor /kennisbank/{slug}/.

Zelfde opbouw als badkamer_kennis_artikelen.py en badkamer_kennis_artikelen2.py;
badkamer_kennis.py voegt de lijsten samen (ARTIKELEN + ARTIKELEN2 + ARTIKELEN3).

Feitencontrole (november 2026, met WebSearch en WebFetch):
- Elektra in de badkamer: NEN 1010 deel 7-701. Gangbare uitleg: zone 0 is de binnenkant van bad of
  douchebak (alleen zeer lage veiligheidsspanning, IPX7); zone 1 ligt boven bad of douchebak tot
  2,25 m boven de vloer (IPX4, IPX5 als er met een waterstraal wordt schoongemaakt); zone 2 is een
  strook van 0,60 m rond zone 1, ook tot 2,25 m (IPX4). Bij een douche zonder bak loopt zone 1 tot
  1,20 m vanaf het vaste douchepunt. Eindgroepen in de badkamer achter een aardlekschakelaar van 30 mA.
  Bronnen: NEN (nen.nl) en uitleg van bouwmarkten en vakfora; daarom op de pagina als "gangbare uitleg"
  en met het advies een erkend installateur te laten beslissen.
- Lichtsterkte: algemeen licht rond 150 tot 300 lux, koeler licht (3500 tot 5000 K) bij de spiegel,
  warm licht (2700 tot 3000 K) voor de avond. Geen norm; richtwaarden uit lichtadvies.
- Watergebruik: CBS, Watergebruik thuis 2021: gemiddeld 7,4 minuten douchen, 7,7 l/min,
  56,9 liter per beurt, 46,2 liter per persoon per dag; regendouche gemiddeld 10,3 l/min,
  waterbesparende kop 6,3 l/min, massagedouche 13,6 l/min; 24% van de mensen heeft een regendouche.
  Milieu Centraal: 129 liter drinkwater per persoon per dag (2021), toilet 24%; waterbesparende kop
  maximaal 7,2 l/min; van 7,4 naar 5 minuten douchen bespaart ca. €36 per persoon per jaar (gasprijs
  €1,37); kleine spoelknop bespaart 12 liter per persoon per dag; bad ca. 140 liter.
  Milieu Centraal, Nieuwe badkamer: douche-wtw bespaart 40 tot 50% energie voor het douchen;
  wachttijd voor warm water maximaal 30 seconden met korte leidingen.
- Schoonmaken: Milieu Centraal, Sanitairreinigers en Schimmels in huis: schoonmaakazijn of
  sanitairreiniger tegen kalk, chloor maakt niet schoon en ontkalkt niet, niet overdoseren.
- Hangtoilet: Homedeal, Toilet verbouwen kosten: inbouwreservoir €150 tot €300; hangtoilet met
  inbouwreservoir inclusief montage gemiddeld €600 tot €1.400.
- Wandpanelen: Werkspot, Wandpanelen in de badkamer: €50 tot €100 per m², tegels €30 tot €80 per m².
- Grote tegels: Homedeal, Kosten tegelzetter: legloon gemiddeld €25 tot €40 per m², hoger bij grote
  formaten. richtprijzen.py "tegelwerk" (€25 tot €55, bovengrens voor kleine badkamers en grote formaten).
- Inbouwkranen: Werkspot, Inbouw of opbouw douchekraan: installatie complexer, meer leidingwerk,
  hogere arbeidskosten. Geen los tarief gevonden; daarom uurtarief en montage uit richtprijzen.py.
- Minimummaten nieuwbouw: Bbl artikel 4.170 (badruimte 1,6 m² en 0,8 m breed; met toilet 2,2 m² en
  0,9 m breed), via IPLO.
Overige prijzen komen uit richtprijzen.py (incl. 21% btw, tenzij anders vermeld).
"""

import richtprijzen as RP
from components import eur
from badkamer_kennis_artikelen import BBL, IPLO_VOCHT, IPLO_BADRUIMTE, IPLO_VENTILATIE, NEN
from badkamer_kennis_artikelen2 import MC_SCHIMMEL, MC_VENTILEREN, WERKSPOT_MICROCEMENT


def _bereik(sleutel, factor=1):
    lo, hi = RP.lh(sleutel, factor)
    return f"{eur(int(lo))} tot {eur(int(hi))}"


def _niveau(sleutel, niveau):
    lo, hi = RP.niveaus(sleutel)[niveau]
    return f"{eur(lo)} tot {eur(hi)}"


# Richtprijzen uit richtprijzen.py (incl. btw, behalve uurtarief en voorrijkosten)
P_ELEKTRA = _bereik("elektra")
P_UUR = _bereik("uurtarief")                     # excl. btw
P_TEGELWERK = _bereik("tegelwerk")               # legloon per m²
P_TEGELS = _bereik("tegels")                     # materiaal per m²
P_WATERDICHT = _bereik("waterdicht")
P_LEIDING = _bereik("leidingwerk")
P_LEIDING_VERPL = _bereik("leidingwerk_verplaatsen")
P_TOILET_VERPL = _bereik("leidingwerk_toilet_verplaatsen")
P_MONTAGE_TOILET = _bereik("montage_toilet")
P_MONTAGE_DOUCHE = _bereik("montage_douche")
P_KIT = _bereik("kitwerk_badkamer")
P_VENTILATOR = _bereik("ventilator")
P_TOILET_BASIS = _niveau("sanitair_toilet", "basis")
P_TOILET_MIDDEN = _niveau("sanitair_toilet", "midden")
P_TOILET_LUXE = _niveau("sanitair_toilet", "luxe")
P_DOUCHE_MIDDEN = _niveau("sanitair_douche", "midden")
P_DOUCHE_LUXE = _niveau("sanitair_douche", "luxe")

# Nieuwe prijzen in deze module (incl. btw), met bron:
# Homedeal, toilet verbouwen kosten: hangtoilet met inbouwreservoir incl. montage €600 – €1.400.
P_HANGTOILET_TOTAAL = f"{eur(600)} tot {eur(1400)}"
# Homedeal, toilet verbouwen kosten: inbouwreservoir los €150 – €300.
P_INBOUWRESERVOIR = f"{eur(150)} tot {eur(300)}"
# Werkspot, wandpanelen in de badkamer: €50 – €100 per m².
P_PANELEN = f"{eur(50)} tot {eur(100)}"
# Milieu Centraal: van 7,4 naar 5 minuten douchen ≈ €36 per persoon per jaar (gasprijs €1,37).
P_KORTER_DOUCHEN = eur(36)

# Bronnen
MC_DOUCHE = ("Milieu Centraal, Besparen onder de douche en in bad",
             "https://www.milieucentraal.nl/energie-besparen/duurzaam-warm-water/besparen-onder-de-douche/")
MC_DRINKWATER = ("Milieu Centraal, Zo bespaar je drinkwater",
                 "https://www.milieucentraal.nl/huis-en-tuin/water-besparen/drinkwater-besparen/")
MC_NIEUWE_BADKAMER = ("Milieu Centraal, Nieuwe badkamer: duurzaam verbouwen",
                      "https://www.milieucentraal.nl/in-en-om-het-huis/verbouwen/nieuwe-badkamer/")
MC_KLUSWIJZER = ("Milieu Centraal, Kluswijzer waterbesparende douchekop (pdf)",
                 "https://www.milieucentraal.nl/media/q1bb4qtr/kluswijzer-waterbesparende-douchekop.pdf")
MC_SANITAIR = ("Milieu Centraal, Sanitairreinigers", "https://www.milieucentraal.nl/huis-en-tuin/schoonmaken/sanitairreinigers/")
MC_SCHOONMAKEN = ("Milieu Centraal, Milieuvriendelijk schoonmaken", "https://www.milieucentraal.nl/huis-en-tuin/schoonmaken/")
CBS_DOUCHE = ("CBS, Watergebruik thuis 2021: de douche",
              "https://www.cbs.nl/nl-nl/longread/aanvullende-statistische-diensten/2022/watergebruik-thuis--wgt---2021/6-de-douche")
CBS_TOTAAL = ("CBS, Watergebruik thuis 2021: totaal watergebruik",
              "https://www.cbs.nl/nl-nl/longread/aanvullende-statistische-diensten/2022/watergebruik-thuis--wgt---2021/4-totaal-watergebruik")
HOMEDEAL_TOILET = ("Homedeal, Toilet verbouwen: kosten", "https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/")
HOMEDEAL_TEGEL = ("Homedeal, Kosten tegelzetter", "https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter")
WERKSPOT_PANELEN = ("Werkspot, Wandpanelen in de badkamer: voor- en nadelen",
                    "https://www.werkspot.nl/badkamer-sanitair/artikelen/wandpanelen-in-de-badkamer-voordelen-nadelen")
WERKSPOT_INBOUW = ("Werkspot, Inbouw of opbouw douchekraan",
                   "https://www.werkspot.nl/badkamer-sanitair/artikelen/tips-voor-kiezen-tussen-inbouw-of-opbouw-douchekranen")
WERKSPOT_SANITAIR = ("Werkspot, Sanitair plaatsen: installatiekosten",
                     "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/sanitair-plaatsen")
SLIMSTER_BADKAMER = RP.BRONNEN["slimster_badkamer"]
TRUSTOO_BADKAMER = RP.BRONNEN["trustoo_badkamer"]
NEN_1010 = ("NEN, NEN 1010: veiligheidsbepalingen voor laagspanningsinstallaties", "https://www.nen.nl/")

# Eenvoudige opmaak voor de maattekeningen (inline, geen extra CSS nodig)
_FIG = 'style="margin:22px 0;padding:16px;background:#fff;border:1px solid var(--line);border-radius:var(--radius)"'
_CAP = 'style="font-size:.88rem;margin-top:8px;color:var(--muted)"'


_SVG_ZONES = """<figure """ + _FIG + """>
<svg viewBox="0 0 640 300" width="100%" role="img" aria-labelledby="ka3-zt ka3-zd" style="max-width:640px;display:block;margin:0 auto">
<title id="ka3-zt">Zones rond een bad of douchebak volgens NEN 1010</title>
<desc id="ka3-zd">Zijaanzicht. Zone 0 is de binnenkant van het bad. Zone 1 ligt erboven tot 2,25 meter. Zone 2 is een strook van 60 centimeter naast zone 1. Daarbuiten gelden geen extra zone-eisen.</desc>
<rect x="60" y="35" width="200" height="180" style="fill:var(--accent);opacity:.32"/>
<rect x="260" y="35" width="60" height="225" style="fill:var(--accent);opacity:.14"/>
<rect x="60" y="215" width="200" height="45" style="fill:var(--navy);opacity:.85"/>
<rect x="30" y="20" width="12" height="245" style="fill:var(--line)"/>
<line x1="20" y1="262" x2="620" y2="262" style="stroke:var(--ink);stroke-width:3"/>
<path d="M60 215 v45 h200 v-45" style="fill:none;stroke:var(--ink);stroke-width:3"/>
<line x1="60" y1="35" x2="320" y2="35" style="stroke:var(--ink);stroke-dasharray:6 5"/>
<text x="160" y="244" text-anchor="middle" style="fill:#fff;font-size:15px;font-weight:700">zone 0 · IPX7</text>
<text x="160" y="120" text-anchor="middle" style="fill:var(--ink);font-size:17px;font-weight:700">zone 1</text>
<text x="160" y="142" text-anchor="middle" style="fill:var(--ink);font-size:14px">IPX4 (IPX5 bij waterstraal)</text>
<text x="290" y="130" text-anchor="middle" style="fill:var(--ink);font-size:15px;font-weight:700" transform="rotate(-90 290 130)">zone 2 · IPX4</text>
<text x="470" y="120" text-anchor="middle" style="fill:var(--muted);font-size:15px">buiten de zones</text>
<text x="470" y="142" text-anchor="middle" style="fill:var(--muted);font-size:13px">IP44 blijft verstandig</text>
<line x1="345" y1="38" x2="345" y2="258" style="stroke:var(--ink)"/>
<path d="M340 46 l5 -10 l5 10 M340 250 l5 10 l5 -10" style="fill:none;stroke:var(--ink)"/>
<text x="352" y="152" style="fill:var(--ink);font-size:14px">2,25 m</text>
<text x="290" y="285" text-anchor="middle" style="fill:var(--ink);font-size:13px">60 cm</text>
<text x="160" y="285" text-anchor="middle" style="fill:var(--ink);font-size:13px">bad of douchebak</text>
<circle cx="470" cy="45" r="9" style="fill:#f6c453"/><circle cx="160" cy="45" r="9" style="fill:#f6c453"/>
</svg>
<figcaption """ + _CAP + """>Maattekening (illustratie) van de zones in de gangbare uitleg van NEN 1010. Bij een douche zonder bak loopt zone 1 tot 1,20 m vanaf het vaste douchepunt. Je installateur bepaalt de zones in jouw badkamer.</figcaption>
</figure>"""

ARTIKELEN3 = [
# ---------------------------------------------------------------------------
{
"slug": "badkamerverlichting",
"groep": "Techniek en vocht",
"titel": "Badkamerverlichting: IP-zones, lux en lichtkleur",
"seo_titel": "Badkamerverlichting: IP-zones, lux en lichtkleur",
"description": "Welke lampen mogen waar in de badkamer? Lees hoe de zones uit NEN 1010 werken, welke IP-waarde je nodig hebt, hoeveel licht je nodig hebt en wat verlichting kost.",
"kort": "Zones, IP-waarden, lux en lichtkleur: zo krijg je veilig en prettig licht in de badkamer.",
"intro": "Licht in de badkamer moet twee dingen doen. Het moet veilig zijn in een ruimte vol water en damp, en het moet goed werken: helder bij de spiegel, rustig in bad en zacht als je 's nachts naar het toilet gaat. In dit artikel lees je hoe de zones uit de norm NEN 1010 werken, welke IP-waarde een lamp nodig heeft en hoe je met drie soorten licht een badkamer maakt die er elke dag goed uitziet.",
"kort_antwoord": "De badkamer is verdeeld in zones. In het bad of de douchebak (zone 0) mag alleen zeer lage spanning met IPX7. Boven het bad of de douche tot 2,25 m (zone 1) en in een strook van 60 cm ernaast (zone 2) moet een lamp minstens IPX4 zijn. Combineer algemeen licht, licht bij de spiegel en sfeerlicht, en laat een erkend installateur het aansluiten.",
"secties": [
("zones", "De zones uit NEN 1010",
"""<p>Voor elektra in een badkamer gelden extra regels. Ze staan in de norm NEN 1010, in het deel over ruimten met een bad of douche. De ruimte wordt verdeeld in zones. Hoe dichter bij het water, hoe strenger de eisen.</p>
<ul class="checklist">
<li><strong>Zone 0</strong> is de binnenkant van het bad of de douchebak. Hier mag alleen een toestel op zeer lage veiligheidsspanning (12 volt), dat waterdicht is tot onderdompeling: IPX7.</li>
<li><strong>Zone 1</strong> ligt recht boven het bad of de douchebak, tot 2,25 m boven de vloer. Een lamp moet hier minstens IPX4 zijn, en IPX5 als de ruimte met een waterstraal wordt schoongemaakt. Alleen vaste toestellen die voor deze zone gemaakt zijn, het liefst op 12 volt.</li>
<li><strong>Zone 2</strong> is een strook van 60 cm rond zone 1, ook tot 2,25 m hoog. Ook hier minstens IPX4. Een stopcontact hoort hier niet; alleen een speciaal scheerstopcontact met scheidingstransformator.</li>
<li><strong>Buiten de zones</strong> gelden geen extra zone-eisen. Toch is een lamp met IP44 in de hele badkamer verstandig, omdat er overal damp is.</li>
</ul>
""" + _SVG_ZONES + """
<p>Bij een inloopdouche zonder bak is de uitleg anders: zone 1 loopt dan tot 1,20 m vanaf het vaste punt waar het water uit de muur of het plafond komt. Een regendouche aan het plafond maakt zone 1 dus groter dan je denkt. Daarnaast moet elke groep in de badkamer beveiligd zijn met een aardlekschakelaar van 30 mA. Twijfel je, laat de zones dan bepalen door een erkend installateur.</p>"""),
("ip", "Wat betekent de IP-waarde?",
"""<p>IP staat voor <em>ingress protection</em>: bescherming tegen binnendringen. Het eerste cijfer gaat over stof en aanraking (0 tot 6), het tweede over water (0 tot 8). Een X betekent dat dat cijfer niet getest is.</p>
<div class="tablewrap"><table>
<thead><tr><th>Code</th><th>Water</th><th>Waar in de badkamer</th></tr></thead>
<tbody>
<tr><td>IPX4 / IP44</td><td>Spatwater van alle kanten</td><td>Zone 1 en 2, en als basis in de hele badkamer</td></tr>
<tr><td>IPX5 / IP65</td><td>Waterstraal</td><td>Zone 1 als er met een straal wordt schoongemaakt, en in een inloopdouche</td></tr>
<tr><td>IPX7 / IP67</td><td>Tijdelijk onder water</td><td>Zone 0, bijvoorbeeld een ledstrip in een badnis</td></tr>
</tbody></table></div>
<p>Let op de hele lamp, niet alleen de lichtbron. Een inbouwspot met een losse ring is soms alleen aan de voorkant IP44. Kijk ook naar de transformator of driver: die moet buiten de natte zones zitten, bijvoorbeeld boven het plafond buiten de douche, en daar goed bereikbaar zijn.</p>"""),
("lagen", "Drie soorten licht",
"""<p>Een badkamer met alleen één plafondlamp oogt vlak. Bij de spiegel geeft die lamp bovendien schaduw op je gezicht. Werk daarom met drie lagen.</p>
<ol>
<li><strong>Algemeen licht.</strong> Inbouwspots of een plafondlamp die de hele ruimte verlicht. Als richtwaarde wordt vaak 150 tot 300 lux genoemd. In een badkamer van 6 m² zijn vier tot zes spots meestal genoeg; plaats ze niet allemaal in een rij boven het midden, maar ook boven de douche en het toilet.</li>
<li><strong>Licht bij de spiegel.</strong> Licht van voren of van opzij, op gezichtshoogte, geeft een gezicht zonder schaduw. Denk aan een spiegel met verlichting aan beide kanten, of twee wandlampen naast de spiegel. Een spot recht boven je hoofd geeft juist donkere kringen onder de ogen.</li>
<li><strong>Sfeerlicht.</strong> Een ledstrip in een nis, onder een zwevend meubel of achter een spiegel. Gedimd geeft dat rust bij het baden en genoeg licht als je 's nachts naar het toilet gaat.</li>
</ol>"""),
("kleur", "Lichtkleur en kleurweergave",
"""<p>De lichtkleur staat in kelvin (K). Warm wit is ongeveer 2700 tot 3000 K, neutraal wit rond 4000 K. Bij de spiegel kiezen veel mensen iets koeler licht, rond 3500 tot 4000 K, omdat je kleuren dan beter ziet. Voor de avond en de nacht is warm licht prettiger.</p>
<p>Kijk ook naar de kleurweergave, de CRI of Ra. Hoe hoger, hoe natuurlijker huid en make-up eruitzien. Kies bij de spiegel minstens Ra 90. Wil je beide, kies dan lampen waarvan je de lichtkleur kunt instellen, of zet de spiegel en de spots op aparte schakelaars.</p>"""),
("schakelen", "Schakelaars, dimmers en sensoren",
"""<p>Een schakelaar hoort niet in zone 1 of 2. De meeste mensen plaatsen hem naast de deur, buiten de badkamer of direct binnen bij de deur. Handig zijn:</p>
<ul class="checklist">
<li>aparte schakelaars voor algemeen licht, spiegel en sfeerlicht;</li>
<li>een dimmer voor de spots (controleer of de lampen dimbaar zijn);</li>
<li>een bewegingssensor voor een laag nachtlicht, zodat je niet in fel licht stapt;</li>
<li>de ventilator gekoppeld aan het licht met een nalooptijd, of met een vochtsensor. Meer daarover lees je in het artikel over <a href="/kennisbank/badkamer-ventilatie/">badkamer ventilatie</a>.</li>
</ul>"""),
("kosten", "Wat kost badkamerverlichting?",
f"""<p>Elektra aanpassen in een badkamer kost volgens de richtprijzen op deze site ongeveer {P_ELEKTRA} inclusief btw. Daarin zitten stopcontacten, schakelaars, een aparte groep en eenvoudige spots. Uitgebreide verlichting met meerdere circuits, dimmers en ledstrips komt erbovenop. Een installateur rekent daarnaast een uurtarief van ongeveer {P_UUR} exclusief btw.</p>
<p>Het voordeligst is om de verlichting mee te nemen bij een complete renovatie. Leidingen en dozen gaan dan in de muur en het plafond voordat er getegeld wordt. Achteraf een spot verplaatsen betekent hakken in nieuw tegelwerk. Kijk voor lampen en spiegels ook bij <a href="/badkamerspullen/badkamerlampen-kiezen/">badkamerlampen kiezen</a>.</p>"""),
],
"stappen_kop": "Checklist voor je lichtplan",
"stappen": [
("Teken de zones", "Zet bad, douche en douchepunt op een plattegrond en teken zone 1 en 2 erbij."),
("Kies drie lagen licht", "Algemeen licht, spiegellicht van voren of opzij en sfeerlicht dat je kunt dimmen."),
("Controleer de IP-waarde", "Minstens IPX4 in zone 1 en 2, IPX7 in zone 0, en IP44 als basis voor de rest."),
("Plan de schakelaars", "Aparte schakelaars of een dimmer, buiten de zones, en de ventilator met nalooptijd."),
("Laat het aansluiten", "Een erkend installateur sluit alles aan op een groep met een aardlekschakelaar van 30 mA."),
],
"faq": [
("Mag een gewone lamp in de badkamer?", "Buiten de zones mag dat volgens de norm, maar door de damp is een lamp met IP44 verstandiger. In zone 1 en 2 moet een lamp minstens IPX4 zijn."),
("Mag er een spot boven de douche?", "Ja, als de spot geschikt is voor zone 1: minstens IPX4, en IPX5 als er met een waterstraal wordt schoongemaakt. Een spot op 12 volt met de transformator buiten de zones is de veiligste keus."),
("Hoeveel spots heb ik nodig?", "In een badkamer van ongeveer 6 m² zijn vier tot zes spots meestal genoeg voor algemeen licht. Spiegellicht komt daar los bij."),
("Welke lichtkleur is het beste voor de spiegel?", "Neutraal wit, ongeveer 3500 tot 4000 K, met een hoge kleurweergave (Ra 90 of hoger). Voor de avond is warm wit rond 2700 K prettiger."),
("Mag ik zelf lampen aansluiten in de badkamer?", "Een lamp vervangen kan, maar nieuwe groepen, dozen en lampen in de zones laat je aanleggen door een erkend installateur. Dat is veiliger en voorkomt problemen met je verzekering."),
],
"bronnen": [NEN_1010, MC_VENTILEREN, SLIMSTER_BADKAMER, TRUSTOO_BADKAMER],
"dienst": "badkamer-installeren",
"kosten": ["nieuwe-badkamer", "uurtarief-loodgieter"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/badkamerlampen-kiezen/", "Badkamerlampen kiezen", "Spots, spiegellampen en ledstrips naast elkaar.")],
"gerelateerd": ["badkamer-ventilatie", "regendouche", "badkamer-ontwerpen"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-ontwerpen",
"groep": "Ontwerp en materialen",
"titel": "Badkamer ontwerpen: in zes stappen van idee naar tekening",
"seo_titel": "Badkamer ontwerpen in zes stappen",
"description": "Zelf je badkamer ontwerpen? Lees hoe je meet, een indeling kiest, rekening houdt met afvoer en loopruimte, materialen combineert en een tekening maakt voor de offerte.",
"kort": "Meten, indelen, loopruimte en materialen: zo maak je een ontwerp waar een specialist mee verder kan.",
"intro": "Een goed ontwerp voorkomt dure verrassingen. Als je vooraf weet waar de douche komt, hoe de deur draait en waar de afvoer ligt, kun je offertes beter vergelijken en kies je bewust. Je hoeft geen ontwerper te zijn. Met een rolmaat, ruitjespapier en de stappen in dit artikel maak je een tekening waar een badkamerspecialist mee verder kan.",
"kort_antwoord": "Begin met nauwkeurig meten: vloer, hoogte, ramen, deur en de plek van afvoer en leidingen. Kies daarna een indeling waarin elk toestel genoeg loopruimte heeft, meestal 60 tot 80 cm ervoor. Houd de afvoer van het toilet zo veel mogelijk op dezelfde plek, want verplaatsen kost geld. Kies pas daarna materialen en kleuren, en zet alles op een tekening met maten.",
"secties": [
("meten", "Stap 1: meet alles op",
"""<p>Meet de badkamer op in centimeters en teken de plattegrond op schaal, bijvoorbeeld 1 hokje is 10 cm. Meet niet alleen lengte en breedte, maar ook:</p>
<ul class="checklist">
<li>de hoogte van het plafond, en een schuin dak of een balk;</li>
<li>de plek en de draairichting van de deur;</li>
<li>de ramen: breedte, hoogte en de hoogte van de vensterbank;</li>
<li>de afvoer van het toilet, de douche en de wastafel, en de standleiding;</li>
<li>de radiator, de ventilatie en de meterkast als die vlakbij is.</li>
</ul>
<p>Meet op twee of drie plekken. Muren zijn zelden helemaal haaks; een verschil van een paar centimeter bepaalt of een douchewand van 90 cm past.</p>"""),
("ruimte", "Stap 2: ken de loopruimte",
"""<p>Elk toestel heeft vrije ruimte ervoor nodig. Dit zijn gangbare richtmaten:</p>
<div class="tablewrap"><table>
<thead><tr><th>Toestel</th><th>Breedte toestel</th><th>Vrije ruimte ervoor</th></tr></thead>
<tbody>
<tr><td>Toilet</td><td>ca. 36 tot 40 cm, plus 20 cm aan elke kant</td><td>60 tot 80 cm</td></tr>
<tr><td>Wastafel</td><td>50 tot 120 cm</td><td>70 tot 90 cm</td></tr>
<tr><td>Douche</td><td>minimaal 80 × 80 cm, prettig 90 × 120 cm</td><td>70 cm om in en uit te stappen</td></tr>
<tr><td>Bad</td><td>70 tot 80 cm breed, 170 tot 180 cm lang</td><td>70 cm langs de lange kant</td></tr>
</tbody></table></div>
<p>Voor nieuwbouw geeft het Besluit bouwwerken leefomgeving minimummaten: een badruimte van 1,6 m² en 0,8 m breed, of 2,2 m² en 0,9 m breed als het toilet erin staat (artikel 4.170). Voor een bestaande woning gelden die maten niet, maar ze laten zien wat het minimum is. Wil je later zonder drempels kunnen wonen, reken dan op een draaicirkel van 150 cm; lees meer in het artikel over <a href="/kennisbank/levensloopbestendige-badkamer/">een levensloopbestendige badkamer</a>.</p>"""),
("indeling", "Stap 3: kies een indeling",
"""<p>De meeste badkamers passen in een paar vaste vormen. In een smalle badkamer staan alle toestellen aan één lange wand, met de douche achterin. In een vierkante badkamer komt de douche in een hoek, met wastafel en toilet tegenover elkaar. In een grotere ruimte kun je zones maken: een droog deel bij de deur en een nat deel achterin.</p>
<p>Een paar vuistregels:</p>
<ul class="checklist">
<li>Zet het toilet niet recht tegenover de deur als je dat kunt vermijden.</li>
<li>Houd de wastafel bij de deur en de douche verder weg; dan blijft het natte deel achterin.</li>
<li>Een deur die naar buiten draait, of een schuifdeur, wint vaak 60 cm ruimte.</li>
<li>Een raam boven het bad of in de douche kan, maar vraag naar kozijn en afdichting.</li>
</ul>
<p>Proberen kan met de <a href="/tools/indelingsplanner/">indelingsplanner</a>. Voor kleine ruimtes staan meer ideeën in <a href="/kennisbank/kleine-badkamer-indelen/">een kleine badkamer indelen</a>.</p>"""),
("techniek", "Stap 4: let op afvoer en techniek",
f"""<p>Het toilet heeft een afvoer van 90 tot 110 mm nodig met genoeg afschot. Die verplaatsen is de duurste wijziging in een ontwerp. Volgens de richtprijzen op deze site kost het verleggen van de afvoer van één toilet ongeveer {P_TOILET_VERPL}, nog zonder tegelwerk. Een douche of wastafel verplaatsen is meestal makkelijker, omdat de afvoer dunner is. In een appartement of bij een houten vloer is er vaak weinig ruimte voor afschot.</p>
<p>Denk in deze stap ook aan een voorzetwand voor het toilet en de kranen, de plek van de ventilatie, de vloerverwarming of radiator en het licht. Wie de zones voor elektra kent, kiest makkelijker de plek van spots en stopcontacten; zie <a href="/kennisbank/badkamerverlichting/">badkamerverlichting</a>.</p>"""),
("materialen", "Stap 5: materialen en sfeer",
"""<p>Kies pas materialen als de indeling vastligt. Begin met de grote vlakken: vloer en wanden. Twee of drie materialen is genoeg; meer wordt al snel onrustig. Grote tegels geven rust, kleine tegels geven grip op de douchevloer. Een warme houtkleur bij het meubel maakt een witte badkamer zachter. Kijk voor eigenschappen en onderhoud bij <a href="/materialen/">materialen</a> en voor sfeer bij <a href="/kennisbank/badkamerstijlen/">badkamerstijlen</a> of de <a href="/tools/stijlkiezer/">stijlkiezer</a>.</p>"""),
("tekening", "Stap 6: maak een tekening voor de offerte",
"""<p>Een goede tekening heeft een plattegrond met maten, de plek van elk toestel en de wanden die je wilt betegelen tot het plafond. Schrijf erbij wat je wilt: bijvoorbeeld een inloopdouche van 90 × 140 cm, een hangtoilet en een wastafel van 80 cm. Zo krijg je offertes die je naast elkaar kunt leggen. Veel badkamerspecialisten maken daarna zelf een uitgewerkte tekening of 3D-tekening. Vraag of die in de prijs zit, en wie de maten controleert voordat er besteld wordt.</p>
<p>Wil je weten hoe de rest van het traject loopt, van eerste gesprek tot oplevering? Lees <a href="/zo-verloopt-je-verbouwing/">zo verloopt je verbouwing</a> en <a href="/kennisbank/volgorde-badkamerrenovatie/">de volgorde van een badkamerrenovatie</a>.</p>"""),
],
"stappen_kop": "Checklist voor je ontwerp",
"stappen": [
("Plattegrond op schaal", "Alle maten in centimeters, met deur, ramen, afvoer en leidingen."),
("Loopruimte gecontroleerd", "60 tot 80 cm vrij voor toilet, wastafel en douche."),
("Afvoer toilet bekeken", "Blijft hij op zijn plek, of heb je budget om hem te verplaatsen?"),
("Techniek ingetekend", "Ventilatie, verwarming, licht en stopcontacten buiten de natte zones."),
("Wensen op papier", "Maten van douche, meubel en toilet, en welke wanden je betegelt."),
],
"faq": [
("Heb ik een ontwerper nodig?", "Niet altijd. Met een goede plattegrond en duidelijke wensen kun je zelf veel. Veel badkamerspecialisten werken je ontwerp daarna uit. Bij een lastige ruimte of een complete verbouwing kan een ontwerper wel helpen."),
("Hoeveel ruimte moet er voor een toilet zijn?", "Reken op 60 tot 80 cm vrije ruimte voor de pot en ongeveer 20 cm naast de pot aan elke kant."),
("Kan ik het toilet verplaatsen?", "Meestal wel, maar het kost extra. Het hangt af van de afvoer, het afschot en de vloer. Vraag het na voordat je het ontwerp vastlegt."),
("Wat is de kleinste maat voor een douche?", "80 × 80 cm is het minimum. 90 × 120 cm of groter voelt een stuk ruimer."),
("Hoe lang duurt het ontwerpen?", "Reken op een paar weken: meten, ideeën verzamelen, offertes aanvragen en de tekening aanpassen. Neem er de tijd voor; wijzigen tijdens de verbouwing kost meer."),
],
"bronnen": [IPLO_BADRUIMTE, BBL, TRUSTOO_BADKAMER, HOMEDEAL_TOILET],
"dienst": "badkamer-renoveren",
"kosten": ["nieuwe-badkamer", "badkamer-slopen"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/wastafelmeubel-kiezen/", "Wastafelmeubel kiezen", "Maten, materialen en ophanghoogte.")],
"gerelateerd": ["kleine-badkamer-indelen", "volgorde-badkamerrenovatie", "badkamerstijlen"],
},
# ---------------------------------------------------------------------------
{
"slug": "grote-tegels-badkamer",
"groep": "Ontwerp en materialen",
"titel": "Grote tegels in de badkamer: wat je moet weten",
"seo_titel": "Grote tegels in de badkamer: voordelen en valkuilen",
"description": "Tegels van 60 × 120 cm of groter geven rust, maar vragen een vlakke ondergrond, de juiste lijm en een ervaren tegelzetter. Lees de voordelen, valkuilen en wat het extra kost.",
"kort": "60 × 60, 60 × 120 of nog groter: wat grote tegels vragen van de ondergrond, het afschot en de tegelzetter.",
"intro": "Grote tegels zijn populair. Minder voegen geeft een rustig beeld, en een kleine badkamer lijkt er groter door. Maar hoe groter de tegel, hoe meer er bij het zetten kan misgaan. Een ondergrond die een paar millimeter scheef is, zie je bij een tegel van 120 cm meteen. In dit artikel lees je wat er anders is aan grote tegels, waar je op let in de douche en wat het zetten extra kost.",
"kort_antwoord": "Grote tegels geven minder voegen en een rustig beeld. Ze vragen wel een heel vlakke ondergrond, volle verlijming met de juiste lijm, een tegelzetter met ervaring en vaak een levelsysteem. In een inloopdouche met afschot werken grote tegels het best met een douchegoot langs de wand, zodat de vloer maar naar één kant hoeft te hellen. Reken op een hoger legloon dan voor standaardtegels.",
"secties": [
("wat", "Wat is een grote tegel?",
"""<p>Er is geen vaste grens, maar in de praktijk heet alles vanaf 60 × 60 cm een groot formaat. Veel gebruikte maten zijn 60 × 60, 60 × 120, 80 × 80, 90 × 90 en 120 × 120 cm. Daarboven zijn er keramische platen van 120 × 260 cm of meer, die vooral op wanden worden gebruikt. Bijna alle grote tegels zijn van keramiek of porselein en zijn gerectificeerd: de randen zijn na het bakken recht geslepen. Daardoor kan de voeg smal blijven, vaak 2 tot 3 mm. Lees meer over het materiaal bij <a href="/materialen/keramische-tegels/">keramische tegels</a>.</p>"""),
("voordelen", "Voordelen en nadelen",
"""<div class="tablewrap"><table>
<thead><tr><th>Voordelen</th><th>Nadelen</th></tr></thead>
<tbody>
<tr><td>Minder voegen, dus minder vuil en schimmel in de voeg</td><td>De ondergrond moet heel vlak zijn; dat kost voorbereiding</td></tr>
<tr><td>Rustig beeld; een kleine ruimte oogt groter</td><td>Zwaar en lastig te hanteren, vaak met twee mensen</td></tr>
<tr><td>Doorlopende vloer van badkamer naar douche</td><td>Afschot in de douche is lastiger (zie hieronder)</td></tr>
<tr><td>Strak bij moderne en minimalistische stijlen</td><td>Meer snijverlies in een kleine badkamer met veel hoeken</td></tr>
</tbody></table></div>
<p>Een grote tegel is op de vloer van een kleine badkamer niet altijd mooier. In een ruimte van 1,5 × 2 meter hou je met 60 × 120 cm veel smalle stroken over. Laat de tegelzetter een legplan maken, zodat je vooraf ziet waar de snijranden komen.</p>"""),
("ondergrond", "De ondergrond: vlak, stevig en droog",
"""<p>Bij een kleine tegel vang je een oneffenheid op met wat extra lijm. Bij een grote tegel lukt dat niet. Een bolle vloer laat een tegel wippen, een holle plek onder een tegel geeft later een scheur. Daarom:</p>
<ul class="checklist">
<li>moet de vloer of wand vooraf vlak zijn, soms met een egalisatielaag of nieuwe wandplaten;</li>
<li>gebruikt de tegelzetter flexibele tegellijm die geschikt is voor grote formaten, en lijm op de vloer én op de achterkant van de tegel (dubbele verlijming), zodat er geen holle plekken zijn;</li>
<li>helpt een levelsysteem met clips en wiggen om hoogteverschil tussen tegels (overtand) te voorkomen;</li>
<li>moet een nieuwe dekvloer eerst droog genoeg zijn. Vraag de tegelzetter of hij het vocht meet.</li>
</ul>
<p>Op een houten vloer of een zwevende vloer is extra voorzichtigheid nodig: die werkt, en een grote tegel scheurt dan eerder. Een ontkoppelingsmat of extra versteviging kan nodig zijn.</p>"""),
("douche", "Grote tegels in de douche",
"""<p>Een douchevloer heeft afschot nodig naar de afvoer. Bij een putje in het midden loopt de vloer van vier kanten schuin naar het midden. Een grote tegel kan die vorm niet volgen zonder te knikken; de tegelzetter moet dan in vier driehoeken snijden (enveloppe-snit). Dat kan mooi zijn, maar het vraagt vakmanschap.</p>
<p>Makkelijker is een douchegoot langs de wand. Dan helt de vloer maar naar één kant, en kan een tegel van 60 × 120 cm in één stuk blijven. Zorg ook dat de tegel stroef genoeg is voor een natte vloer: vraag naar de antislipklasse, en kies in de douche een matte of gestructureerde tegel. Lees meer over goten bij <a href="/badkamerspullen/douchegoot-kiezen/">een douchegoot kiezen</a> en over afschot bij <a href="/kennisbank/inloopdouche-zonder-drempel/">een inloopdouche zonder drempel</a>. Onder de tegels hoort in de natte zone altijd een afdichting; zie <a href="/kennisbank/badkamer-waterdicht-maken/">badkamer waterdicht maken</a>.</p>"""),
("kosten", "Wat kost tegelen met grote tegels?",
f"""<p>Het legloon voor badkamertegels ligt volgens de richtprijzen op deze site tussen {P_TEGELWERK} per m² inclusief btw. Grote formaten zitten aan de bovenkant van die bandbreedte of erboven, omdat ze zwaarder zijn, meer voorbereiding vragen en vaak met twee mensen worden gezet. Homedeal noemt ook dat de prijs stijgt met het formaat. Reken daarnaast op:</p>
<ul>
<li>tegels zelf: gemiddeld {P_TEGELS} per m², grote formaten en natuursteenlook vaak meer;</li>
<li>egaliseren van de vloer of nieuwe wandplaten, als de ondergrond niet vlak genoeg is;</li>
<li>meer snijverlies: bestel 10 tot 15% extra in plaats van de gebruikelijke 5 tot 10%.</li>
</ul>
<p>Vergelijk offertes per m² en kijk of egaliseren, lijm en levelsysteem erin zitten. Meer rekenvoorbeelden staan bij <a href="/kosten/tegelzetter-per-m2/">tegelzetter per m²</a>.</p>"""),
("voeg", "Voegen en kitten",
"""<p>Bij gerectificeerde tegels is een voeg van 2 tot 3 mm gebruikelijk. Smaller dan 2 mm raden tegelzetters af, omdat de tegel moet kunnen werken. Kies een voegkleur die dicht bij de tegel ligt voor een rustig beeld. In hoeken en bij de aansluiting met bad of douchebak komt geen voeg maar kit. Meer over voegen en kit lees je bij <a href="/materialen/voegen-en-kit/">voegen en kit</a>.</p>"""),
],
"stappen_kop": "Checklist voor grote tegels",
"stappen": [
("Vraag een legplan", "Zo zie je vooraf waar snijranden en smalle stroken komen."),
("Laat de ondergrond meten", "Vlakheid en vocht van vloer en wand, en of egaliseren nodig is."),
("Vraag naar lijm en levelsysteem", "Flexibele lijm voor grote formaten, dubbele verlijming en clips tegen overtand."),
("Kies de goot bij de tegel", "Een douchegoot langs de wand maakt afschot met grote tegels eenvoudiger."),
("Check de antislip", "Een matte of gestructureerde tegel in de douche, met een antislipklasse."),
],
"faq": [
("Maken grote tegels een kleine badkamer groter?", "Ze geven minder voegen en dus een rustiger beeld, waardoor een ruimte groter kan lijken. In een heel kleine ruimte met veel hoeken kunnen veel smalle stroken het effect juist verpesten. Een legplan laat zien wat het wordt."),
("Kan ik grote tegels in de douche gebruiken?", "Ja, het makkelijkst met een douchegoot langs de wand, zodat de vloer naar één kant afloopt. Kies een stroeve tegel."),
("Kun je grote tegels over oude tegels zetten?", "Soms, als de oude tegels vast, vlak en schoon zijn en de hoogte het toelaat. Vaak is verwijderen en egaliseren de betere keus."),
("Zijn grote tegels duurder om te laten zetten?", "Meestal wel. Het legloon ligt hoger door het gewicht, de voorbereiding en het extra werk. Vergelijk offertes per m²."),
("Hoe breed is de voeg bij grote tegels?", "Meestal 2 tot 3 mm bij gerectificeerde tegels."),
],
"bronnen": [HOMEDEAL_TEGEL, RP.BRONNEN["trustoo_tegel"], RP.BRONNEN["werkspot_tegel"], IPLO_VOCHT],
"dienst": "tegelwerk-badkamer",
"kosten": ["tegelzetter-per-m2", "nieuwe-badkamer"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Formaat, kwaliteit en hoeveel je bestelt."),
          ("/badkamerspullen/douchegoot-kiezen/", "Douchegoot kiezen", "Goot of putje, lengte en plaats in de douche.")],
"gerelateerd": ["tegels-kiezen", "badkamer-waterdicht-maken", "badkamer-zonder-tegels"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-zonder-tegels",
"groep": "Ontwerp en materialen",
"titel": "Badkamer zonder tegels: vijf alternatieven vergeleken",
"seo_titel": "Badkamer zonder tegels: vijf alternatieven",
"description": "Microcement, wandpanelen, kalkstuc, glas of waterbestendige verf? Vergelijk vijf alternatieven voor tegels op prijs, onderhoud en waterdichtheid, en lees waar je op let.",
"kort": "Microcement, wandpanelen, kalkstuc, glas en verf naast elkaar: wat kan waar, en wat vraagt het?",
"intro": "Steeds meer mensen willen een badkamer zonder voegen. Er zijn genoeg alternatieven voor tegels, van naadloos microcement tot wandpanelen die je in een dag plaatst. Maar niet elk materiaal kan overal. Op de wand naast de wastafel kan bijna alles, in de douche maar een paar. In dit artikel zetten we vijf alternatieven naast elkaar, met hun voor- en nadelen en een richtprijs.",
"kort_antwoord": "Voor de douche zijn microcement met een afdichting eronder en waterdichte wandpanelen de bekendste alternatieven voor tegels. Kalkstuc (tadelakt) kan ook, maar vraagt een specialist en onderhoud. Glas is goed voor een achterwand. Verf is alleen geschikt buiten de natte zone. Wat je ook kiest: in de douche hoort een waterdichte opbouw, en de naden en hoeken bepalen of het lang goed blijft.",
"secties": [
("waarom", "Waarom zonder tegels?",
"""<p>De redenen zijn bijna altijd dezelfde: geen voegen die vuil worden, een rustig en modern beeld, en minder sloopwerk. Sommige alternatieven kunnen over bestaande tegels heen. Dat scheelt puin, stof en tijd. Daar staat tegenover dat tegels sterk, betaalbaar en makkelijk te herstellen zijn. Een kapotte tegel vervang je; een beschadiging in een naadloze wand is lastiger.</p>"""),
("vergelijking", "Vijf alternatieven op een rij",
f"""<div class="tablewrap"><table>
<thead><tr><th>Materiaal</th><th>In de douche?</th><th>Onderhoud</th><th>Richtprijs per m²</th></tr></thead>
<tbody>
<tr><td>Microcement</td><td>Ja, met afdichting eronder</td><td>Mild reinigen, sealer na een aantal jaren vernieuwen</td><td>Duurder dan tegels: veel handwerk</td></tr>
<tr><td>Wandpanelen (kunststof, SPC of composiet)</td><td>Ja, als het systeem daarvoor gemaakt is</td><td>Laag; kitnaden controleren</td><td>{P_PANELEN} inclusief plaatsing</td></tr>
<tr><td>Kalkstuc of tadelakt</td><td>Ja, door een specialist</td><td>Regelmatig met zeep of was behandelen</td><td>Hoog; specialistisch werk</td></tr>
<tr><td>Glas (achterwand)</td><td>Op de wand, niet op de vloer</td><td>Laag; kalkvlekken zichtbaar</td><td>Maatwerk, per project</td></tr>
<tr><td>Waterbestendige verf</td><td>Nee, alleen buiten de natte zone</td><td>Na een aantal jaren opnieuw</td><td>Laag</td></tr>
</tbody></table></div>
<p>Ter vergelijking: tegels kosten volgens de richtprijzen op deze site {P_TEGELS} per m² aan materiaal en {P_TEGELWERK} per m² aan legloon, inclusief btw. Werkspot noemt voor wandpanelen {P_PANELEN} per m². Voor microcement, kalkstuc en glas hangt de prijs sterk af van het oppervlak en de verwerker; vraag een offerte per m² met de voorbereiding erin.</p>"""),
("microcement", "Microcement",
"""<p>Microcement is een dunne laag van cement en kunsthars, in een paar lagen opgezet en afgewerkt met een sealer. Het geeft een naadloze wand en vloer. Het kan vaak over bestaande tegels, mits die vast zitten. In de douche is microcement niet vanzelf waterdicht: er hoort een afdichting onder. Het resultaat hangt sterk af van de verwerker. Alles over dit materiaal lees je in <a href="/kennisbank/microcement-badkamer/">microcement in de badkamer</a> en bij <a href="/materialen/microcement/">materialen: microcement</a>.</p>"""),
("panelen", "Wandpanelen",
"""<p>Wandpanelen zijn grote platen van kunststof, SPC of een composiet met een toplaag. Er zijn uitvoeringen in steen-, beton- en tegellook. Ze worden verlijmd of met een profiel bevestigd, vaak over bestaande tegels. Een badkamer is er soms in een of twee dagen mee klaar.</p>
<p>Let op drie dingen. Ten eerste moet het systeem geschikt zijn voor de douche; niet elk paneel is dat. Ten tweede bepalen de naden, hoeken en aansluitingen of er water achter komt. Gebruik de profielen en kit van het systeem. Ten derde voelt een paneel anders aan dan steen; klop er eens op in een showroom. Voor de vloer zijn panelen meestal niet bedoeld.</p>"""),
("kalkstuc", "Kalkstuc en tadelakt",
"""<p>Tadelakt is een Marokkaanse kalkpleister die met een steen glad wordt gewreven en met zachte zeep waterafstotend wordt gemaakt. Het geeft een zachte, levendige wand. Het is handwerk voor een specialist en vraagt onderhoud: de wand wordt regelmatig met zeep of was behandeld. Agressieve schoonmaakmiddelen en ontkalkers tasten de kalk aan. Voor wie het mooi vindt, is het een bijzondere keus; voor wie weinig onderhoud wil, minder.</p>"""),
("glas-verf", "Glas en verf",
"""<p>Een glazen achterwand, in kleur gelakt, is strak en makkelijk schoon te houden. Hij wordt op maat gemaakt en is vooral geschikt achter een wastafel of als douchewand. Verf is het goedkoopst, maar alleen geschikt buiten de natte zone. Milieu Centraal raadt latex af in de badkamer, omdat die schimmelgevoelig is, en noemt minerale muurverf als alternatief.</p>"""),
("valkuilen", "Valkuilen",
"""<ul class="checklist">
<li><strong>Geen afdichting in de douche.</strong> Bij microcement en kalkstuc hoort in de natte zone een waterdichte laag eronder.</li>
<li><strong>Losse ondergrond.</strong> Over tegels heen werken kan alleen als die vast zitten. Holle tegels gaan eerst weg.</li>
<li><strong>Naden en hoeken.</strong> Bij panelen komt water vooral binnen bij slordige naden en kitranden.</li>
<li><strong>Gladde vloer.</strong> Vraag naar de antislip van het hele systeem, inclusief sealer.</li>
<li><strong>De wettelijke ondergrens.</strong> In een bestaande woning moeten de vloer en de wanden tot 1 meter in de badruimte waterafstotend zijn (Bbl artikel 3.65). Rond de douche is meer nodig.</li>
</ul>"""),
],
"stappen_kop": "Zo kies je",
"stappen": [
("Bepaal per zone", "Wat komt in de douche, wat op de droge wanden en wat op de vloer?"),
("Check de ondergrond", "Vast, vlak en droog? Dan kan er soms iets over de oude tegels heen."),
("Vraag naar de waterdichte opbouw", "Laat in de offerte zetten welke afdichting onder de natte zone komt."),
("Bekijk een proefstuk", "Zie en voel het materiaal, en vraag naar eerder werk dat al een paar jaar oud is."),
("Spreek onderhoud af", "Welke middelen mag je gebruiken en wanneer is er nieuwe sealer of was nodig?"),
],
"faq": [
("Wat is het goedkoopste alternatief voor tegels?", "Voor de droge wanden is verf het goedkoopst. Voor de douche zijn wandpanelen meestal voordeliger dan microcement of kalkstuc, ook omdat het plaatsen snel gaat."),
("Kunnen wandpanelen over oude tegels?", "Vaak wel, als de tegels vast zitten en de wand vlak is. Volg de voorschriften van het systeem."),
("Is een badkamer zonder tegels waterdicht?", "Alleen met de juiste opbouw. In de douche hoort onder microcement of kalkstuc een afdichting, en bij panelen moeten de naden en hoeken goed afgewerkt zijn."),
("Kan de vloer ook zonder tegels?", "Ja, met microcement of een gietvloer die geschikt is voor natte ruimtes. Wandpanelen zijn meestal niet bedoeld voor de vloer."),
("Is het makkelijker schoon te houden?", "Zonder voegen wel. Maar microcement en kalkstuc vragen milde middelen; schuurmiddel en sterke ontkalker tasten ze aan."),
],
"bronnen": [WERKSPOT_PANELEN, WERKSPOT_MICROCEMENT, MC_NIEUWE_BADKAMER, IPLO_VOCHT],
"dienst": "badkamer-renoveren",
"kosten": ["tegelzetter-per-m2", "nieuwe-badkamer"],
"tool": "/tools/stijlkiezer/",
"extra": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Toch tegels? Waar je op let bij het kopen.")],
"gerelateerd": ["microcement-badkamer", "grote-tegels-badkamer", "badkamer-waterdicht-maken"],
},
# ---------------------------------------------------------------------------
{
"slug": "hangtoilet-of-staand-toilet",
"groep": "Techniek en vocht",
"titel": "Hangtoilet of staand toilet: verschillen, maten en kosten",
"seo_titel": "Hangtoilet of staand toilet: verschillen en maten",
"description": "Een hangtoilet is makkelijk schoon te houden en de zithoogte kies je zelf, maar het vraagt een inbouwreservoir en een voorzetwand. Vergelijk maten, techniek en richtprijzen.",
"kort": "Inbouwreservoir, zithoogte, voorzetwand en richtprijzen: de verschillen tussen een hangend en een staand toilet.",
"intro": "Bij een nieuwe badkamer of toiletruimte kiezen de meeste mensen voor een hangtoilet. Het oogt strak en je kunt eronder dweilen. Toch is een staand toilet niet ouderwets: het is goedkoper, sneller vervangen en past ook waar geen ruimte is voor een voorzetwand. In dit artikel lees je de verschillen, de belangrijkste maten en wat elk type ongeveer kost.",
"kort_antwoord": "Een hangtoilet hangt aan een stalen frame met een inbouwreservoir achter een voorzetwand. Het is makkelijk schoon te houden en de zithoogte bepaal je bij de montage. Het kost meer, de voorzetwand neemt 15 tot 25 cm diepte in en het reservoir zit achter tegels. Een staand toilet is goedkoper en eenvoudiger te vervangen, maar lastiger schoon te maken rond de voet.",
"secties": [
("verschil", "Het verschil in het kort",
"""<div class="tablewrap"><table>
<thead><tr><th></th><th>Hangtoilet</th><th>Staand toilet</th></tr></thead>
<tbody>
<tr><td>Montage</td><td>Aan een frame met inbouwreservoir, achter een voorzetwand</td><td>Op de vloer, met een los of duoblok-reservoir</td></tr>
<tr><td>Schoonmaken</td><td>Vloer eronder vrij; makkelijk dweilen</td><td>Rond de voet en achter de pot lastiger</td></tr>
<tr><td>Zithoogte</td><td>Zelf te kiezen bij de montage</td><td>Vast; hoger alleen met een verhoogde pot</td></tr>
<tr><td>Ruimte</td><td>Voorzetwand van 15 tot 25 cm diep</td><td>Reservoir staat tegen de muur, geen voorzetwand nodig</td></tr>
<tr><td>Geluid</td><td>Reservoir in de wand, meestal stiller</td><td>Vullen van het reservoir hoorbaar</td></tr>
<tr><td>Onderhoud</td><td>Via de bedieningsplaat; reservoir zit achter tegels</td><td>Alles direct bereikbaar</td></tr>
<tr><td>Prijs</td><td>Hoger, vooral door frame en montage</td><td>Lager</td></tr>
</tbody></table></div>"""),
("maten", "De belangrijkste maten",
"""<figure """ + _FIG + """>
<svg viewBox="0 0 420 300" width="100%" role="img" aria-labelledby="ka3-ht ka3-hd" style="max-width:520px;display:block;margin:0 auto">
<title id="ka3-ht">Maten van een hangtoilet in zijaanzicht</title>
<desc id="ka3-hd">Frame tot ongeveer 112 centimeter hoog achter een voorzetwand. Bedieningsplaat rond 100 centimeter. Bovenkant pot op 40 tot 42 centimeter, comforthoogte 46 tot 48 centimeter. Diepte pot 48 tot 56 centimeter, met 60 tot 80 centimeter vrije ruimte ervoor.</desc>
<rect x="20" y="20" width="16" height="252" style="fill:var(--line)"/>
<rect x="36" y="46" width="50" height="226" style="fill:var(--accent);opacity:.18"/>
<rect x="44" y="52" width="26" height="140" rx="4" style="fill:none;stroke:var(--accent-dark);stroke-width:2;stroke-dasharray:5 4"/>
<rect x="82" y="64" width="6" height="26" rx="2" style="fill:var(--ink)"/>
<path d="M88 186 h96 q10 0 6 12 q-14 32 -56 34 h-22 q-12 0 -12 -8 v-38 z" style="fill:#fff;stroke:var(--ink);stroke-width:3"/>
<line x1="8" y1="272" x2="410" y2="272" style="stroke:var(--ink);stroke-width:3"/>
<line x1="88" y1="174" x2="200" y2="174" style="stroke:var(--accent-dark);stroke-dasharray:5 4"/>
<line x1="230" y1="186" x2="230" y2="270" style="stroke:var(--ink)"/>
<path d="M226 194 l4 -8 l4 8 M226 262 l4 8 l4 -8" style="fill:none;stroke:var(--ink)"/>
<text x="238" y="226" style="fill:var(--ink);font-size:13px;font-weight:700">40 tot 42 cm</text>
<text x="238" y="242" style="fill:var(--muted);font-size:12px">bovenkant pot</text>
<text x="206" y="170" style="fill:var(--accent-dark);font-size:12px">comfort 46 tot 48 cm</text>
<text x="96" y="80" style="fill:var(--ink);font-size:12px">bedieningsplaat ca. 100 cm</text>
<text x="96" y="42" style="fill:var(--ink);font-size:12px">frame ca. 112 cm, voorzetwand 15 tot 25 cm</text>
<line x1="88" y1="286" x2="190" y2="286" style="stroke:var(--ink)"/>
<text x="139" y="298" text-anchor="middle" style="fill:var(--ink);font-size:12px">pot 48 tot 56 cm</text>
<line x1="192" y1="286" x2="330" y2="286" style="stroke:var(--accent-dark);stroke-dasharray:4 3"/>
<text x="300" y="298" text-anchor="middle" style="fill:var(--accent-dark);font-size:12px">60 tot 80 cm vrij</text>
</svg>
<figcaption """ + _CAP + """>Maattekening (illustratie) met gangbare maten. De precieze maten staan in de montagehandleiding van het frame en de pot.</figcaption>
</figure>
<p>De bovenkant van de pot zit bij een standaardmontage op 40 tot 42 cm. Voor lange mensen of wie moeilijker opstaat, is 46 tot 48 cm prettiger; dat heet een comforthoogte. Bij een hangtoilet regel je dat met de hoogte van het frame, zonder dat je een andere pot nodig hebt. De bedieningsplaat zit meestal rond 1 meter hoogte.</p>
<p>Een hangpot is ongeveer 48 tot 56 cm diep; compacte potten zijn korter. Reken op 60 tot 80 cm vrije ruimte voor de pot en ongeveer 20 cm aan weerszijden. Voor nieuwbouw is de minimale toiletruimte 0,9 bij 1,2 meter; in een bestaand huis is die vaak krapper. Wie later zonder hulp wil kunnen wonen, leest meer in <a href="/kennisbank/levensloopbestendige-badkamer/">een levensloopbestendige badkamer</a>.</p>"""),
("techniek", "Inbouwreservoir en voorzetwand",
"""<p>Een hangtoilet hangt aan een stalen frame dat aan de vloer en de muur vastzit. In dat frame zit het inbouwreservoir. Het frame wordt weggewerkt achter een voorzetwand van waterbestendige platen, die daarna betegeld wordt. Het frame moet het gewicht dragen, dus aan een lichte scheidingswand alleen hangen is niet genoeg.</p>
<p>Het reservoir zit achter de tegels, maar is niet onbereikbaar. De vulkraan en de spoelklep vervang je via de opening achter de bedieningsplaat. Bewaar het merk en het type van het reservoir, zodat een loodgieter later de juiste onderdelen heeft. Een frame met een standaardmaat maakt vervangen in de toekomst eenvoudiger. Meer over het kiezen staat bij <a href="/badkamerspullen/inbouwreservoir-kiezen/">een inbouwreservoir kiezen</a>.</p>"""),
("water", "Spoelen en water besparen",
"""<p>Moderne toiletten hebben een grote en een kleine spoelknop. Volgens Milieu Centraal is het toilet goed voor ongeveer een kwart van ons drinkwatergebruik, en bespaar je 12 liter per persoon per dag door bij een kleine boodschap de kleine knop te gebruiken. Heb je nog een oud toilet met een grote stortbak, dan scheelt een nieuw toilet direct water. Randloze potten zijn makkelijker schoon te houden, omdat er geen rand is waaronder vuil zit. Meer tips staan in <a href="/kennisbank/water-besparen-badkamer/">water besparen in de badkamer</a>.</p>"""),
("kosten", "Wat kost het?",
f"""<p>Volgens Homedeal kost een hangtoilet met inbouwreservoir inclusief montage gemiddeld {P_HANGTOILET_TOTAAL}. Het inbouwreservoir alleen kost {P_INBOUWRESERVOIR}. De richtprijzen op deze site, inclusief btw:</p>
<ul>
<li>staand toilet (product): {P_TOILET_BASIS};</li>
<li>hangtoilet met inbouwreservoir (product): {P_TOILET_MIDDEN}, in een luxere uitvoering {P_TOILET_LUXE};</li>
<li>toilet plaatsen op dezelfde plek: {P_MONTAGE_TOILET};</li>
<li>afvoer en waterleiding verleggen: {P_TOILET_VERPL} extra, zonder tegelwerk.</li>
</ul>
<p>Ga je van een staand naar een hangend toilet, dan komt er meestal tegelwerk bij: de voorzetwand moet betegeld worden, en vaak ook de vloer waar de oude voet stond. Meer rekenvoorbeelden staan op <a href="/kosten/toilet-renoveren/">wat kost een toilet renoveren</a> en <a href="/kosten/toilet-verplaatsen/">toilet verplaatsen</a>.</p>"""),
("keus", "Wanneer kies je wat?",
"""<p>Kies een <strong>hangtoilet</strong> als je toch verbouwt, er ruimte is voor een voorzetwand en je schoonmaakgemak belangrijk vindt. Kies een <strong>staand toilet</strong> als je alleen de pot wilt vervangen zonder tegelwerk, als het budget krap is, of in een huurwoning waar je weinig mag aanpassen. Er zijn ook staande potten die tegen de wand aansluiten (back-to-wall); die combineren een staand toilet met een strakke uitstraling.</p>"""),
],
"stappen_kop": "Checklist voordat je kiest",
"stappen": [
("Meet de ruimte", "Is er 15 tot 25 cm voor een voorzetwand en 60 tot 80 cm vrij voor de pot?"),
("Kies de zithoogte", "Standaard 40 tot 42 cm, comfort 46 tot 48 cm. Probeer het in een showroom."),
("Check de wand", "Kan het frame aan een stevige muur en de vloer worden vastgezet?"),
("Vraag naar onderdelen", "Noteer merk en type van het reservoir voor later onderhoud."),
("Vergelijk de offerte", "Staan frame, voorzetwand, tegelwerk en afvoer er apart in?"),
],
"faq": [
("Is een hangtoilet sterk genoeg?", "Ja. Het frame is gemaakt om een flink gewicht te dragen, mits het goed aan de vloer en een stevige muur is vastgezet."),
("Wat als het inbouwreservoir lekt?", "De vulkraan en de spoelklep zijn bereikbaar via de opening achter de bedieningsplaat. Je hoeft dus meestal geen tegels te breken."),
("Hoe hoog hangt een hangtoilet?", "De bovenkant van de pot zit meestal op 40 tot 42 cm. Een comforthoogte van 46 tot 48 cm kan ook, zonder een andere pot."),
("Kan ik een staand toilet vervangen door een hangtoilet?", "Ja, maar er komt een frame en een voorzetwand bij, vaak ook tegelwerk en een aanpassing van de afvoer."),
("Wat kost een hangtoilet inclusief plaatsen?", f"Homedeal noemt gemiddeld {P_HANGTOILET_TOTAAL} inclusief montage. Tegelwerk en het verleggen van de afvoer komen daar soms bij."),
],
"bronnen": [HOMEDEAL_TOILET, RP.BRONNEN["werkspot_toilet"], MC_DRINKWATER, IPLO_BADRUIMTE],
"dienst": "toilet-renoveren",
"kosten": ["toilet-renoveren", "uurtarief-loodgieter"],
"tool": "/tools/offertechecker/",
"extra": [("/badkamerspullen/toilet-kiezen/", "Toilet kiezen", "Randloos, zithoogte en spoelsysteem."),
          ("/badkamerspullen/inbouwreservoir-kiezen/", "Inbouwreservoir kiezen", "Frame, bedieningsplaat en onderhoud.")],
"gerelateerd": ["kleine-badkamer-indelen", "levensloopbestendige-badkamer", "water-besparen-badkamer"],
},
# ---------------------------------------------------------------------------
{
"slug": "regendouche",
"groep": "Techniek en vocht",
"titel": "Regendouche: waterdruk, verbruik en inbouw",
"seo_titel": "Regendouche: waterdruk, verbruik en inbouw",
"description": "Een regendouche voelt luxe, maar vraagt genoeg waterdruk en warm water. Lees hoeveel water een regendouche gebruikt, op welke hoogte hij komt en wat inbouw of opbouw betekent.",
"kort": "Waterdruk, liters per minuut, hoogte en inbouw: wat je moet weten voordat je een regendouche kiest.",
"intro": "Een regendouche geeft een brede, zachte straal van boven. Het voelt als een warme regenbui. Maar een grote douchekop vraagt meer water, en daarmee ook meer warm water. Of het goed werkt, hangt af van je waterdruk, je cv-ketel of warmtepomp en de leidingen. In dit artikel lees je wat je vooraf controleert, hoeveel water een regendouche gebruikt en wat de keuze tussen opbouw en inbouw betekent.",
"kort_antwoord": "Een regendouche gebruikt volgens het CBS gemiddeld 10,3 liter per minuut, tegen 7,8 liter voor een gewone douchekop. Controleer vooraf of je cv-ketel of boiler genoeg warm water levert en of de waterdruk voldoende is. Kies bij voorkeur een regendouche met een begrenzer of een zuinige stand, en een handdouche erbij. Inbouw oogt strak, maar vraagt meer werk en planning.",
"secties": [
("verbruik", "Hoeveel water gebruikt een regendouche?",
"""<p>Het CBS heeft gemeten hoeveel water Nederlanders gebruiken onder de douche. Een gemiddelde douchebeurt duurt 7,4 minuten en kost bijna 57 liter. Per type douchekop:</p>
<div class="tablewrap"><table>
<thead><tr><th>Type douchekop</th><th>Gemiddeld per minuut</th><th>Bij 7,4 minuten</th></tr></thead>
<tbody>
<tr><td>Waterbesparende douchekop</td><td>6,3 liter</td><td>ca. 47 liter</td></tr>
<tr><td>Gewone douchekop</td><td>7,8 liter</td><td>ca. 58 liter</td></tr>
<tr><td>Regendouche</td><td>10,3 liter</td><td>ca. 76 liter</td></tr>
<tr><td>Massagedouche</td><td>13,6 liter</td><td>ca. 101 liter</td></tr>
</tbody></table></div>
<p>Bron: CBS, Watergebruik thuis 2021; de laatste kolom is eigen rekenwerk. Grote regendouches zonder begrenzer kunnen veel meer gebruiken, soms 15 tot 20 liter per minuut. Bijna een kwart van de mensen heeft volgens het CBS een regendouche. Het meeste geld zit niet in het water, maar in het opwarmen ervan.</p>"""),
("druk", "Waterdruk en warm water",
"""<p>Een regendouche werkt alleen goed met genoeg druk en genoeg warm water. Controleer daarom:</p>
<ul class="checklist">
<li><strong>De waterdruk.</strong> De meeste regendouches werken vanaf ongeveer 1,5 tot 2 bar. Op een hoge verdieping of aan het einde van een lange leiding kan de druk lager zijn. Een installateur meet het met een drukmeter op de kraan.</li>
<li><strong>De cv-ketel of boiler.</strong> Kijk naar de CW-klasse van je ketel. Een lage CW-klasse levert minder warm water per minuut. Een regendouche én een handdouche tegelijk is voor veel ketels te veel. Met een warmtepomp heb je een boilervat: reken uit of dat genoeg is voor jullie gezin.</li>
<li><strong>De leidingen.</strong> Dunne of lange leidingen geven minder doorstroming en een langere wachttijd voor warm water.</li>
</ul>"""),
("hoogte", "Op welke hoogte en welk formaat?",
"""<p>Een regendouche aan de wand of het plafond hangt meestal zo dat de kop ongeveer 2,10 tot 2,25 meter boven de vloer zit, of 20 tot 30 cm boven het hoofd van de langste gebruiker. Hangt hij te laag, dan stoot je je hoofd; te hoog, dan koelt de straal af en spat het meer. Het formaat ligt meestal tussen 20 en 40 cm. Een grotere kop geeft een bredere straal, maar vraagt meer water. In een douche van 80 × 80 cm is 20 tot 25 cm genoeg; in een inloopdouche van 90 × 140 cm past 30 cm of meer.</p>
<p>Let ook op de elektra: een plafondkop maakt zone 1 groter. Lees hierover in <a href="/kennisbank/badkamerverlichting/">badkamerverlichting</a>.</p>"""),
("opbouw", "Opbouw of inbouw?",
f"""<p>Bij een <strong>opbouwset</strong> zitten de thermostaatkraan, de stang en de regendouche op de muur. Hij past op de bestaande aansluitingen en is snel geplaatst. Bij <strong>inbouw</strong> zit de kraan in de muur en komt de arm uit de wand of het plafond. Dat oogt strak, maar het inbouwdeel moet geplaatst worden voordat er getegeld wordt, en het moet goed waterdicht worden aangesloten. Alles over deze keuze lees je in <a href="/kennisbank/inbouwkranen/">inbouwkranen</a>.</p>
<p>Een douche plaatsen en aansluiten kost volgens de richtprijzen op deze site {P_MONTAGE_DOUCHE}, inclusief btw. Een douche als product (bak of goot, wand en kraan) ligt in het middensegment op {P_DOUCHE_MIDDEN} en in een luxere uitvoering op {P_DOUCHE_LUXE}. Inbouw kost meer arbeid; er komt leidingwerk in de muur bij.</p>"""),
("zuinig", "Een regendouche die zuiniger is",
f"""<ul class="checklist">
<li>Kies een regendouche met een ingebouwde begrenzer of een zuinige stand.</li>
<li>Kies een thermostaatkraan, zodat je niet steeds bijstelt en water verspilt.</li>
<li>Combineer met een handdouche voor kort afspoelen en het schoonmaken.</li>
<li>Overweeg een douche-wtw: volgens Milieu Centraal bespaart die 40 tot 50% van de energie voor het douchen.</li>
<li>Douche korter. Van 7,4 naar 5 minuten bespaart volgens Milieu Centraal ongeveer {P_KORTER_DOUCHEN} per persoon per jaar.</li>
</ul>
<p>Meer tips staan in <a href="/kennisbank/water-besparen-badkamer/">water besparen in de badkamer</a>.</p>"""),
("kalk", "Onderhoud en kalk",
"""<p>Een regendouche heeft veel kleine gaatjes. Bij hard water slibben die dicht met kalk. Kies een kop met rubberen noppen, die je met je vingers schoonwrijft. Ontkalk de kop af en toe met schoonmaakazijn. Meer daarover in <a href="/kennisbank/kalk-en-waterhardheid/">kalk en waterhardheid</a> en <a href="/kennisbank/badkamer-schoonmaken/">badkamer schoonmaken</a>.</p>"""),
],
"stappen_kop": "Checklist voor een regendouche",
"stappen": [
("Laat de waterdruk meten", "Meestal is 1,5 tot 2 bar nodig; vraag het na voor de kop die je wilt."),
("Check je warm water", "Kan je ketel, boiler of warmtepomp genoeg leveren voor een grote kop?"),
("Kies de hoogte", "Ongeveer 2,10 tot 2,25 m, of 20 tot 30 cm boven de langste gebruiker."),
("Kies opbouw of inbouw", "Inbouw moet geplaatst zijn voordat er getegeld wordt."),
("Denk aan zuinig", "Begrenzer, thermostaatkraan, handdouche en eventueel een douche-wtw."),
],
"faq": [
("Gebruikt een regendouche veel meer water?", "Gemiddeld 10,3 liter per minuut volgens het CBS, tegen 7,8 liter voor een gewone kop. Zonder begrenzer kan het nog meer zijn."),
("Werkt een regendouche met een warmtepomp?", "Ja, als het boilervat groot genoeg is voor jullie gebruik. Vraag de installateur om het uit te rekenen."),
("Welke waterdruk heb ik nodig?", "De meeste regendouches werken goed vanaf ongeveer 1,5 tot 2 bar. Kijk in de specificaties van de kop."),
("Hoe hoog hangt een regendouche?", "Meestal op 2,10 tot 2,25 meter, of 20 tot 30 cm boven het hoofd van de langste gebruiker."),
("Kan ik mijn bestaande douche vervangen door een regendouche?", "Met een opbouwset vaak wel, op de bestaande aansluitingen. Voor inbouw moet de muur open."),
],
"bronnen": [CBS_DOUCHE, MC_DOUCHE, MC_NIEUWE_BADKAMER, WERKSPOT_INBOUW, NEN_1010],
"dienst": "inloopdouche-plaatsen",
"kosten": ["inloopdouche", "uurtarief-loodgieter"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/douchesysteem-kiezen/", "Douchesysteem kiezen", "Opbouw, inbouw en thermostaat naast elkaar."),
          ("/badkamerspullen/douchewand-kiezen/", "Douchewand kiezen", "Glas, maten en profielen.")],
"gerelateerd": ["inbouwkranen", "water-besparen-badkamer", "inloopdouche-zonder-drempel"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-schoonmaken",
"groep": "Techniek en vocht",
"titel": "Badkamer schoonmaken: per materiaal en zonder schade",
"seo_titel": "Badkamer schoonmaken: per materiaal en zonder schade",
"description": "Hoe maak je tegels, voegen, glas, kranen, natuursteen en microcement schoon zonder schade? Een schema per week en per maand, de juiste middelen en wat je beter niet gebruikt.",
"kort": "Een schema per week en per maand, en per materiaal welk middel wel en niet kan.",
"intro": "Een badkamer die je goed schoonhoudt, blijft langer mooi. Kalk, zeepresten en schimmel krijgen minder kans, en kit en voegen gaan langer mee. Maar niet elk middel past bij elk materiaal. Een ontkalker die prima is voor tegels, kan natuursteen of een gekleurde kraan beschadigen. In dit artikel lees je een eenvoudig schema en per materiaal wat je gebruikt en wat je laat staan.",
"kort_antwoord": "Spoel en droog na het douchen de wand en het glas af met een trekker; dat voorkomt de meeste kalk. Maak wekelijks schoon met een milde reiniger of sanitairreiniger, en ontkalk tegels en glas met schoonmaakazijn. Gebruik geen azijn of zuur op natuursteen, microcement of gekleurde kranen. Chloor maakt volgens Milieu Centraal niet schoon en ontkalkt niet. Meer middel is niet schoner.",
"secties": [
("schema", "Een schema dat werkt",
"""<div class="tablewrap"><table>
<thead><tr><th>Wanneer</th><th>Wat</th></tr></thead>
<tbody>
<tr><td>Na elke douchebeurt</td><td>Glas en wanden aftrekken met een trekker, deur of raam even open of de ventilator laten lopen</td></tr>
<tr><td>Elke week</td><td>Wastafel, toilet, kranen en douchevloer met een milde reiniger; spiegel en glas afnemen; putje of goot leegmaken</td></tr>
<tr><td>Elke maand</td><td>Kalk op tegels en glas met schoonmaakazijn of sanitairreiniger; douchekop ontkalken; voegen nakijken</td></tr>
<tr><td>Elk halfjaar</td><td>Ventilatieventiel en ventilator stofvrij maken; kitranden controleren op losse plekken of zwarte plekjes</td></tr>
<tr><td>Elk jaar</td><td>Sifons en afvoer doorspoelen; bij natuursteen of microcement de beschermlaag laten nakijken</td></tr>
</tbody></table></div>
<p>Het belangrijkste is het dagelijkse aftrekken. Water dat opdroogt laat kalk achter. Twintig seconden met een trekker scheelt elke maand veel schrobben.</p>"""),
("middelen", "Welke middelen heb je nodig?",
"""<p>Milieu Centraal adviseert om het simpel te houden. Met water, een sopje van een allesreiniger en een doek of borstel kom je volgens hen al een heel eind. Voor kalk werkt schoonmaakazijn of een sanitairreiniger, die een ontkalker en een ontvetter bevat. Chloor maakt niet schoon en haalt geen kalk weg. En meer middel gebruiken maakt het niet schoner. Kijk bij het kopen naar een milieukeurmerk zoals het Europese Ecolabel.</p>
<ul class="checklist">
<li>een trekker voor glas en wanden;</li>
<li>een microvezeldoek voor kranen en spiegel;</li>
<li>een zachte borstel voor voegen;</li>
<li>een milde allesreiniger of pH-neutrale reiniger;</li>
<li>schoonmaakazijn of een sanitairreiniger, alleen voor materialen die tegen zuur kunnen.</li>
</ul>"""),
("materialen", "Per materiaal: wel en niet",
"""<div class="tablewrap"><table>
<thead><tr><th>Materiaal</th><th>Wel</th><th>Niet</th></tr></thead>
<tbody>
<tr><td>Keramische tegels</td><td>Allesreiniger; azijn tegen kalk</td><td>Schuurspons op glanzende tegels</td></tr>
<tr><td>Cementvoegen</td><td>Zachte borstel en sop; kort azijn, daarna goed naspoelen</td><td>Lang inwerkend zuur: dat tast de voeg aan</td></tr>
<tr><td>Natuursteen (marmer, hardsteen)</td><td>pH-neutrale steenreiniger</td><td>Azijn, citroenzuur, ontkalker en schuurmiddel</td></tr>
<tr><td>Microcement en tadelakt</td><td>Milde, pH-neutrale reiniger</td><td>Schuurmiddel en sterke ontkalker: die tasten de sealer of kalk aan</td></tr>
<tr><td>Glas</td><td>Trekker; azijn of glasreiniger tegen kalk</td><td>Schuursponsen die krassen geven</td></tr>
<tr><td>Chroom</td><td>Microvezel, mild middel, af en toe azijn</td><td>Schuurmiddel</td></tr>
<tr><td>Zwart, goud of geborsteld staal</td><td>Alleen water, zachte zeep en een zachte doek</td><td>Azijn, ontkalker en schuurmiddel; kijk naar het advies van de fabrikant</td></tr>
<tr><td>Kit</td><td>Sop en een zachte borstel; droog houden</td><td>Bleek of chloor; schimmel in kit komt terug, vervang de kit</td></tr>
</tbody></table></div>
<p>Weet je niet zeker van welk materiaal iets is, probeer een middel dan eerst op een plek die je niet ziet. Meer over materialen en hun onderhoud staat bij <a href="/materialen/">materialen</a>, over kranen bij <a href="/materialen/kraanafwerkingen/">kraanafwerkingen</a>.</p>"""),
("schimmel", "Schimmel in voegen en kit",
"""<p>Zwarte plekjes in de kit of de voegen zijn meestal schimmel. Milieu Centraal adviseert alleen middelen te gebruiken die een toelating van het Ctgb hebben, en geen zelfgemaakte mengsels met soda, bleek of chloor. Schimmel die diep in de kit zit, komt na schoonmaken vaak terug; dan is nieuwe kit de oplossing. Komt schimmel steeds terug, dan is er meestal te weinig ventilatie of een vochtprobleem. Lees verder in <a href="/kennisbank/schimmel-in-badkamer/">schimmel in de badkamer</a> en <a href="/kennisbank/badkamer-ventilatie/">badkamer ventilatie</a>.</p>"""),
("afvoer", "Afvoer, putje en goot",
"""<p>Haren en zeepresten verstoppen het putje. Maak het rooster en de sifon eens per week of twee weken schoon. Een haarzeefje helpt. Gebruik geen agressieve ontstopper als routine; die kan rubberen ringen aantasten. Een verstopping die niet weggaat met een ontstopper of door de sifon schoon te maken, laat je oplossen door een loodgieter. Een lekkende of stinkende afvoer kan op een ander probleem wijzen: lees <a href="/kennisbank/lekkage-badkamer/">lekkage in de badkamer</a>.</p>"""),
("ontwerp", "Makkelijk schoon te houden: kies het bij de verbouwing",
f"""<p>Wie gaat verbouwen, kan veel schoonmaakwerk voorkomen:</p>
<ul class="checklist">
<li>een hangtoilet, zodat je de vloer eronder kunt dweilen (zie <a href="/kennisbank/hangtoilet-of-staand-toilet/">hangtoilet of staand toilet</a>);</li>
<li>grote tegels of een naadloze wand, met minder voegen (zie <a href="/kennisbank/grote-tegels-badkamer/">grote tegels</a>);</li>
<li>een glazen wand met een coating die water afstoot;</li>
<li>een inbouwkraan, met minder hoekjes waar kalk in komt (zie <a href="/kennisbank/inbouwkranen/">inbouwkranen</a>);</li>
<li>een goede ventilator met nalooptijd of vochtsensor, zodat de badkamer snel droog is. Een ventilator kost volgens de richtprijzen op deze site {P_VENTILATOR}, inclusief montage.</li>
</ul>
<p>Is de kit al zwart of los? De hele badkamer opnieuw laten kitten kost volgens de richtprijzen op deze site {P_KIT}. Zie ook <a href="/kosten/kitwerk-voegen/">kitwerk en voegen vernieuwen</a>.</p>"""),
],
"stappen_kop": "Snelle routine",
"stappen": [
("Trek af na het douchen", "Glas en wanden, en zet de ventilator aan of het raam open."),
("Wekelijks een sopje", "Milde reiniger voor wastafel, toilet, kranen en douchevloer."),
("Maandelijks ontkalken", "Azijn of sanitairreiniger op tegels en glas, niet op natuursteen of gekleurde kranen."),
("Kijk naar kit en voegen", "Zwarte plekjes of losse randen? Vervang de kit op tijd."),
("Maak afvoer en ventilator schoon", "Putje, sifon en ventiel regelmatig stofvrij en vrij van haren."),
],
"faq": [
("Mag ik azijn gebruiken in de badkamer?", "Op keramische tegels, glas en chroom wel. Niet op natuursteen, microcement, tadelakt of gekleurde kranen; zuur tast die aan."),
("Helpt chloor tegen vuil en kalk?", "Nee. Volgens Milieu Centraal maakt chloor niet schoon en haalt het geen kalk weg."),
("Hoe krijg ik kalkvlekken van de douchewand?", "Met schoonmaakazijn of een sanitairreiniger, en daarna voorkom je nieuwe vlekken door na elke douchebeurt af te trekken."),
("Hoe maak ik een zwarte kraan schoon?", "Met water, een beetje zachte zeep en een zachte doek. Geen azijn, ontkalker of schuurmiddel. Volg het advies van de fabrikant."),
("Wat doe ik tegen schimmel in de kit?", "Oppervlakkige schimmel kun je schoonmaken met een toegelaten middel. Zit het diep in de kit, dan is nieuwe kit beter. Zorg daarna voor betere ventilatie."),
],
"bronnen": [MC_SANITAIR, MC_SCHOONMAKEN, MC_SCHIMMEL, MC_VENTILEREN],
"dienst": "badkamer-onderhoud",
"kosten": ["kitwerk-voegen", "uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [("/badkamerspullen/kranen-kiezen/", "Kranen kiezen", "Afwerkingen en wat ze vragen aan onderhoud.")],
"gerelateerd": ["schimmel-in-badkamer", "kalk-en-waterhardheid", "badkamer-ventilatie"],
},
# ---------------------------------------------------------------------------
{
"slug": "water-besparen-badkamer",
"groep": "Techniek en vocht",
"titel": "Water besparen in de badkamer: wat levert het op?",
"seo_titel": "Water besparen in de badkamer: wat levert het op?",
"description": "Waterbesparende douchekop, korter douchen, douche-wtw, thermostaatkraan en zuinig toilet: per maatregel wat het oplevert en wat je meeneemt bij een verbouwing.",
"kort": "Douchekop, korter douchen, douche-wtw en een zuinig toilet: per maatregel wat het oplevert.",
"intro": "De badkamer is de grootste waterverbruiker in huis. Volgens Milieu Centraal gaat ruim 40 procent van ons drinkwater naar douchen en baden, en een kwart naar het toilet. En warm water kost energie: bijna een kwart van het gasverbruik gaat naar warm water. Je kunt dus veel besparen, soms met een kleine aankoop, soms door het slim mee te nemen bij een verbouwing. In dit artikel staan de maatregelen op een rij, met wat ze ongeveer opleveren.",
"kort_antwoord": "De meeste winst zit in warm water. Een waterbesparende douchekop (maximaal 7,2 liter per minuut) en korter douchen leveren het snelst iets op: van 7,4 naar 5 minuten scheelt volgens Milieu Centraal ongeveer €36 per persoon per jaar. Bij een verbouwing zijn een douche-wtw (40 tot 50% minder energie voor het douchen), korte leidingen, een thermostaatkraan en een toilet met kleine spoelknop de beste keuzes.",
"secties": [
("cijfers", "Waar gaat het water naartoe?",
"""<p>In 2021 gebruikte een Nederlander gemiddeld 129 liter drinkwater per dag. Daarvan ging ruim 40 procent naar douchen en baden en 24 procent naar het toilet (Milieu Centraal, op basis van het CBS). Een gemiddelde douchebeurt duurt 7,4 minuten en kost ongeveer 55 tot 57 liter. Een bad kost met ongeveer 140 liter bijna vier keer zoveel water en energie als een douche van vijf minuten.</p>
<p>Water uit de kraan is in Nederland niet duur. Het opwarmen is de grote kostenpost. Daarom levert besparen op warm water het meeste op, zowel in euro's als voor het klimaat.</p>"""),
("tabel", "Maatregelen op een rij",
f"""<div class="tablewrap"><table>
<thead><tr><th>Maatregel</th><th>Wat het oplevert</th><th>Moment</th></tr></thead>
<tbody>
<tr><td>Korter douchen (7,4 naar 5 minuten)</td><td>Ongeveer {P_KORTER_DOUCHEN} per persoon per jaar (Milieu Centraal, gasprijs €1,37)</td><td>Vandaag</td></tr>
<tr><td>Waterbesparende douchekop</td><td>Ongeveer 20% minder warm water bij het douchen; Milieu Centraal rekende eerder met zo'n €50 tot €60 per huishouden per jaar</td><td>Vandaag; een kop vervang je zelf</td></tr>
<tr><td>Kleine spoelknop gebruiken</td><td>12 liter drinkwater per persoon per dag</td><td>Vandaag</td></tr>
<tr><td>Thermostaatkraan</td><td>Minder water weg tijdens het afstellen</td><td>Bij vervangen van de kraan</td></tr>
<tr><td>Douche-wtw</td><td>40 tot 50% minder energie voor het douchen</td><td>Bij de verbouwing</td></tr>
<tr><td>Korte warmwaterleidingen</td><td>Warm water binnen 30 seconden, minder koud water weggespoeld</td><td>Bij de verbouwing</td></tr>
<tr><td>Zuinig toilet met twee knoppen</td><td>Minder liters per spoelbeurt dan een oude grote stortbak</td><td>Bij vervangen van het toilet</td></tr>
</tbody></table></div>
<p>De bedragen hangen af van de energieprijs, de grootte van het huishouden en hoe lang je doucht. Zie ze als orde van grootte.</p>"""),
("douchekop", "De waterbesparende douchekop",
"""<p>Een waterbesparende douchekop laat volgens Milieu Centraal maximaal 7,2 liter water per minuut door, en voelt toch vol aan. Test je huidige douche met de emmertest uit de kluswijzer van Milieu Centraal: zet de douche op je normale temperatuur, vang één minuut water op in een emmer, en meet. Zit er meer dan 7 liter in, dan loont een zuinige kop. Op de verpakking staat soms een klasse: klasse Z (ongeveer 4,3 tot 6,9 liter) is het zuinigst. Heb je een regendouche, kies dan een model met een begrenzer; zie <a href="/kennisbank/regendouche/">regendouche</a>.</p>"""),
("wtw", "Douche-wtw: warmte terugwinnen",
"""<p>Een douche-wtw (warmteterugwinning) haalt warmte uit het weglopende douchewater en geeft die aan het koude water dat naar de douche of de ketel gaat. Volgens Milieu Centraal bespaar je daarmee 40 tot 50 procent van de energie voor het douchen. Er zijn verticale systemen (een pijp in de afvoer naar beneden, vaak in een verdieping eronder) en horizontale systemen in een douchegoot of onder de douchebak. Bij een nieuwe badkamer is het inbouwen volgens Milieu Centraal weinig extra werk. Vraag je badkamerspecialist of het in jouw situatie past en wat het extra kost.</p>"""),
("leidingen", "Leidingen en kranen bij een verbouwing",
"""<p>Hoe verder de douche van de ketel, hoe langer je wacht op warm water, en hoe meer koud water er weg stroomt. Milieu Centraal noemt een wachttijd van maximaal 30 seconden als doel met korte leidingen. Plan de badkamer daarom zo dicht mogelijk bij de ketel of boiler, of laat de leidingen isoleren.</p>
<p>Een thermostaatkraan houdt de temperatuur constant. Je verliest minder water met afstellen. Een kraan met een koude middenstand voorkomt dat je onbewust de ketel aanzet als je even je handen wast. Een perlator op de wastafelkraan mengt lucht door het water en vermindert de straal. Meer over kranen lees je in <a href="/kennisbank/inbouwkranen/">inbouwkranen</a>.</p>"""),
("toilet", "Het toilet en het bad",
"""<p>Heb je nog een oud toilet met een grote stortbak, dan scheelt een nieuw toilet met twee spoelknoppen veel water. Milieu Centraal raadt aan om bij een verbouwing direct voor een waterbesparende toiletpot te kiezen, en anders de stortbak te verkleinen. Gebruik de kleine knop bij een kleine boodschap: dat scheelt 12 liter per persoon per dag. Wil je een bad, kies dan een model dat niet groter is dan nodig, en houd baden voor af en toe. Lees ook <a href="/kennisbank/hangtoilet-of-staand-toilet/">hangtoilet of staand toilet</a> en <a href="/badkamerspullen/bad-of-douche/">bad of douche</a>.</p>"""),
],
"stappen_kop": "Zo begin je",
"stappen": [
("Doe de emmertest", "Meer dan 7 liter in één minuut? Vervang de douchekop."),
("Douche korter", "Zet een timer of kies een liedje van vier minuten."),
("Gebruik de kleine spoelknop", "Bij een kleine boodschap; dat scheelt 12 liter per persoon per dag."),
("Plan bij de verbouwing", "Vraag naar een douche-wtw, korte leidingen en een thermostaatkraan."),
("Kies zuinig sanitair", "Een toilet met twee knoppen en een douchekop of regendouche met begrenzer."),
],
"faq": [
("Wat levert een waterbesparende douchekop op?", "Ongeveer 20% minder warm water bij het douchen. Milieu Centraal rekende eerder met zo'n €50 tot €60 per huishouden per jaar; het bedrag hangt af van de energieprijs."),
("Is een douche-wtw de moeite waard?", "Bij een nieuwe badkamer vaak wel. Volgens Milieu Centraal bespaar je 40 tot 50% van de energie voor het douchen, en het inbouwen is dan weinig extra werk."),
("Bespaart een thermostaatkraan water?", "Ja, je verliest minder water met het afstellen van de temperatuur, en de temperatuur blijft constant."),
("Hoeveel water gebruikt een bad?", "Ongeveer 140 liter: bijna vier keer zoveel water en energie als een douche van vijf minuten."),
("Hoeveel water gebruik ik per dag?", "Gemiddeld 129 liter per persoon per dag (2021). Ruim 40% daarvan gaat naar douchen en baden."),
],
"bronnen": [MC_DOUCHE, MC_DRINKWATER, MC_NIEUWE_BADKAMER, MC_KLUSWIJZER, CBS_DOUCHE, CBS_TOTAAL],
"dienst": "badkamer-installeren",
"kosten": ["nieuwe-badkamer", "uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [("/badkamerspullen/douchesysteem-kiezen/", "Douchesysteem kiezen", "Thermostaat, regendouche en zuinige standen.")],
"gerelateerd": ["regendouche", "hangtoilet-of-staand-toilet", "vloerverwarming-of-radiator"],
},
# ---------------------------------------------------------------------------
{
"slug": "inbouwkranen",
"groep": "Techniek en vocht",
"titel": "Inbouwkranen: voordelen, nadelen en waar je op let",
"seo_titel": "Inbouwkranen in de badkamer: voor- en nadelen",
"description": "Een inbouwkraan oogt strak, maar het inbouwdeel zit voorgoed in de muur. Lees hoe inbouw werkt, welke maten en hoogtes gangbaar zijn, wat er mis kan gaan en wat het kost.",
"kort": "Inbouwdeel, hoogtes, waterdichte aansluiting en onderhoud: wat een inbouwkraan vraagt.",
"intro": "Een inbouwkraan laat alleen de knoppen en de uitloop zien. De rest zit in de muur. Dat geeft een rustige, strakke badkamer, met minder hoekjes waar kalk en vuil in komen. Maar het inbouwdeel zit voorgoed achter de tegels. Wie het verkeerd plant, krijgt een kraan op de verkeerde hoogte of een lek achter de wand. In dit artikel lees je hoe inbouw werkt, welke maten gangbaar zijn en wat je in de offerte controleert.",
"kort_antwoord": "Een inbouwkraan bestaat uit een inbouwdeel in de muur en een afbouwdeel met knoppen en uitloop. Het inbouwdeel wordt geplaatst voordat er getegeld wordt, op de juiste diepte en waterdicht aangesloten op de afdichting van de wand. Kies een bekend systeem waarvan onderdelen lang leverbaar zijn, en laat de hoogte en diepte vooraf vastleggen. Inbouw kost meer werk dan een opbouwkraan.",
"secties": [
("werking", "Hoe werkt een inbouwkraan?",
"""<p>Een inbouwkraan bestaat uit twee delen. Het <strong>inbouwdeel</strong> (ook wel inbouwbox of basisunit) zit in de muur of in een voorzetwand. Daarin zitten de aansluitingen voor warm en koud water, en vaak de thermostaat en de omstelling. Het <strong>afbouwdeel</strong> is wat je ziet: de rozet, de knoppen en de uitloop of douchearm.</p>
<p>Het inbouwdeel wordt in een vroege fase geplaatst, samen met de leidingen. Daarna komt de wand dicht, de afdichting erop en het tegelwerk. Het afbouwdeel komt pas helemaal aan het einde. Bij veel systemen past één inbouwdeel bij verschillende afbouwdelen. Dan kun je later de knoppen of de afwerking vervangen zonder de muur open te maken.</p>"""),
("voordelen", "Voor- en nadelen",
"""<div class="tablewrap"><table>
<thead><tr><th>Voordelen</th><th>Nadelen</th></tr></thead>
<tbody>
<tr><td>Strak en rustig: alleen knoppen en uitloop in zicht</td><td>Het inbouwdeel moet geplaatst worden voor het tegelwerk</td></tr>
<tr><td>Makkelijk schoon te houden, minder hoekjes voor kalk</td><td>Meer arbeid en leidingwerk dan een opbouwkraan</td></tr>
<tr><td>Meer ruimte op de wastafel of in de douche</td><td>Bij een lek of defect zit het inbouwdeel achter de tegels</td></tr>
<tr><td>Vrij te kiezen hoogte van knoppen en uitloop</td><td>Een fout in hoogte of diepte is lastig te herstellen</td></tr>
</tbody></table></div>
<p>Werkspot noemt ook dat de installatie complexer is en daardoor meer arbeid kost, omdat het leidingwerk in de muur moet en de kraan wordt weggewerkt.</p>"""),
("maten", "Gangbare hoogtes en maten",
"""<p>Er is geen norm voor de hoogte van kranen. Dit zijn gangbare maten, gemeten vanaf de afgewerkte vloer:</p>
<div class="tablewrap"><table>
<thead><tr><th>Onderdeel</th><th>Gangbare hoogte</th><th>Let op</th></tr></thead>
<tbody>
<tr><td>Thermostaat in de douche</td><td>100 tot 120 cm</td><td>Zo dat je hem kunt bedienen zonder onder de straal te staan</td></tr>
<tr><td>Douchearm uit de wand</td><td>210 tot 225 cm</td><td>20 tot 30 cm boven de langste gebruiker; zie <a href="/kennisbank/regendouche/">regendouche</a></td></tr>
<tr><td>Wandkraan boven wastafel</td><td>10 tot 20 cm boven de rand van de wastafel</td><td>De uitloop moet ver genoeg reiken: meestal tot ongeveer het midden van de kom</td></tr>
<tr><td>Badkraan in de wand</td><td>15 tot 25 cm boven de badrand</td><td>Uitloop zo dat het water niet op de rand spat</td></tr>
</tbody></table></div>
<p>Belangrijk is ook de inbouwdiepte. Elk inbouwdeel heeft een minimale en maximale diepte, gemeten tot de afgewerkte wand, dus inclusief afdichting, tegellijm en tegel. Te diep en het afbouwdeel past niet, te ondiep en de rozet sluit niet aan. Leg die maten vast voordat de wand dicht gaat.</p>"""),
("waterdicht", "Waterdicht aansluiten",
"""<p>Een inbouwdeel maakt een gat in de waterdichte wand. Daar moet de afdichting goed op aansluiten. Veel systemen hebben een manchet of een flens voor het afdichten; die hoort bij de afdichtingslaag van de douchewand. Vraag welke manchet gebruikt wordt en laat hem op een foto vastleggen voordat er getegeld wordt.</p>
<p>Laat ook de leidingen onder druk testen voordat de wand dicht gaat. Een lek in een koppeling ontdek je liever nu dan na een jaar door een vlek op het plafond van de kamer eronder. Lees meer in <a href="/kennisbank/badkamer-waterdicht-maken/">badkamer waterdicht maken</a> en <a href="/kennisbank/lekkage-badkamer/">lekkage in de badkamer</a>.</p>"""),
("onderhoud", "Onderhoud en vervangen",
"""<p>De thermostaatpatroon en de stopkranen in een inbouwdeel zijn meestal vanaf de voorkant te vervangen, na het verwijderen van de knoppen en de rozet. Dat is alleen makkelijk als de onderdelen nog leverbaar zijn. Kies daarom een systeem van een fabrikant die lang onderdelen levert, en bewaar het typenummer, de handleiding en de garantiekaart. Bij hard water slibt een thermostaat sneller dicht; spoel en ontkalk de uitloop af en toe. Over afwerkingen en wat ze vragen aan onderhoud lees je bij <a href="/materialen/kraanafwerkingen/">kraanafwerkingen</a>.</p>"""),
("kosten", "Wat kost een inbouwkraan?",
f"""<p>Een los tarief voor alleen een inbouwkraan plaatsen is moeilijk te geven, omdat het werk samenhangt met het leidingwerk en het tegelwerk. Richtprijzen op deze site, inclusief btw:</p>
<ul>
<li>douche plaatsen en aansluiten: {P_MONTAGE_DOUCHE};</li>
<li>douche als product (bak of goot, wand en kraan): {P_DOUCHE_MIDDEN} in het middensegment, {P_DOUCHE_LUXE} luxe;</li>
<li>leidingwerk vernieuwen in een badkamer: {P_LEIDING};</li>
<li>uurtarief installateur: {P_UUR}, exclusief btw.</li>
</ul>
<p>Een inbouwkraan is vooral logisch bij een complete renovatie, als de wanden toch open gaan. Alleen een opbouwkraan vervangen door inbouw betekent hakken in het bestaande tegelwerk. Meer over de kosten van een nieuwe kraan lees je op <a href="/kosten/kraan-vervangen/">kraan vervangen</a> en over het kiezen bij <a href="/badkamerspullen/kranen-kiezen/">kranen kiezen</a>.</p>"""),
],
"stappen_kop": "Checklist voor de offerte",
"stappen": [
("Merk en type inbouwdeel", "Staat in de offerte welk inbouwdeel het is, en zijn onderdelen lang leverbaar?"),
("Hoogtes vastgelegd", "Thermostaat, douchearm en uitloop gemeten vanaf de afgewerkte vloer."),
("Inbouwdiepte gecontroleerd", "Past de diepte bij de opbouw van de wand, inclusief afdichting en tegel?"),
("Manchet en afdichting", "Welke manchet sluit het inbouwdeel aan op de waterdichte laag?"),
("Druktest en foto's", "Leidingen onder druk getest en alles gefotografeerd voordat de wand dicht gaat."),
],
"faq": [
("Is een inbouwkraan duurder dan een opbouwkraan?", "Meestal wel, vooral door het extra werk: leidingwerk in de muur en het plaatsen van het inbouwdeel voor het tegelwerk."),
("Wat als een inbouwkraan kapot gaat?", "Thermostaatpatroon en stopkranen zijn meestal vanaf de voorkant te vervangen. Dat lukt het makkelijkst als de onderdelen nog leverbaar zijn."),
("Kan ik een opbouwkraan vervangen door een inbouwkraan?", "Ja, maar de muur moet open en er komt tegelwerk bij. Dat is vooral logisch als je toch renoveert."),
("Op welke hoogte komt de thermostaat in de douche?", "Meestal op 100 tot 120 cm, zodat je hem bedient zonder onder de straal te staan."),
("Kan een inbouwkraan in een gewone muur?", "Ja, als de muur dik genoeg is voor de inbouwdiepte. Anders komt het inbouwdeel in een voorzetwand."),
],
"bronnen": [WERKSPOT_INBOUW, WERKSPOT_SANITAIR, IPLO_VOCHT, NEN],
"dienst": "badkamer-installeren",
"kosten": ["uurtarief-loodgieter", "inloopdouche"],
"tool": "/tools/offertechecker/",
"extra": [("/badkamerspullen/kranen-kiezen/", "Kranen kiezen", "Inbouw, opbouw, thermostaat en afwerking."),
          ("/badkamerspullen/douchesysteem-kiezen/", "Douchesysteem kiezen", "Regendouche, handdouche en thermostaat.")],
"gerelateerd": ["regendouche", "badkamer-waterdicht-maken", "badkamer-schoonmaken"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-en-suite",
"groep": "Wonen en situatie",
"titel": "Badkamer en suite: een badkamer bij de slaapkamer",
"seo_titel": "Badkamer en suite: ruimte, techniek en kosten",
"description": "Een badkamer en suite bij de slaapkamer vraagt goede afvoer, ventilatie en geluidwering. Lees hoeveel ruimte je nodig hebt, welke indeling werkt en waar de kosten zitten.",
"kort": "Ruimte, afvoer, ventilatie en privacy: waar je op let bij een badkamer direct aan de slaapkamer.",
"intro": "Een badkamer en suite ligt direct aan de slaapkamer, soms zonder deur ertussen. Het voelt als een hotel en scheelt 's ochtends wachten op de gezinsbadkamer. Maar een badkamer naast het bed brengt ook vocht, geluid en geurtjes mee. En de afvoer moet ergens heen. In dit artikel lees je hoeveel ruimte je nodig hebt, welke indelingen werken, wat er technisch nodig is en waar de kosten zitten.",
"kort_antwoord": "Voor een badkamer en suite met douche, wastafel en eventueel toilet heb je minimaal ongeveer 2 tot 3 m² nodig. De grootste vragen zijn de afvoer (kan die met genoeg afschot naar de standleiding?), de ventilatie (mechanisch, rechtstreeks naar buiten) en de scheiding met de slaapkamer: vocht, geluid en privacy. Zet het toilet bij voorkeur in een eigen hokje of achter een deur.",
"secties": [
("wat", "Wat is een badkamer en suite?",
"""<p>En suite komt uit het Frans en betekent zoiets als 'in het verlengde van'. Een badkamer en suite is alleen bereikbaar vanuit de slaapkamer. Dat kan een aparte ruimte met een deur zijn, maar ook een open badkamer waarbij alleen een glazen wand of een halfhoge muur het slaapdeel scheidt. Het past vaak in een grote slaapkamer, een zolder of een uitbouw. Gaat het om een tweede badkamer in huis, lees dan ook <a href="/badkamer-voor/tweede-badkamer/">een tweede badkamer in huis</a> en de kosten op <a href="/kosten/tweede-badkamer/">tweede badkamer</a>.</p>"""),
("ruimte", "Hoeveel ruimte heb je nodig?",
"""<div class="tablewrap"><table>
<thead><tr><th>Indeling</th><th>Ruimte (richtmaat)</th><th>Wat er in past</th></tr></thead>
<tbody>
<tr><td>Compact</td><td>ca. 2 tot 3 m²</td><td>Douche 90 × 90 cm, kleine wastafel, eventueel toilet</td></tr>
<tr><td>Gemiddeld</td><td>ca. 3 tot 5 m²</td><td>Inloopdouche, wastafelmeubel, toilet</td></tr>
<tr><td>Ruim</td><td>vanaf ca. 6 m²</td><td>Inloopdouche, dubbele wastafel, apart toilet, eventueel bad</td></tr>
</tbody></table></div>
<p>Ter vergelijking: voor nieuwbouw is een badruimte minimaal 1,6 m² en 0,8 m breed, of 2,2 m² en 0,9 m breed met toilet erin (Bbl artikel 4.170). Dat is echt het minimum; prettig is iets meer. Een slaapkamer moet daarna nog bruikbaar zijn: houd rekening met de plek van het bed, de kast en de deur. Speel met de ruimte in de <a href="/tools/indelingsplanner/">indelingsplanner</a>.</p>"""),
("afvoer", "Afvoer en leidingen: de grootste vraag",
f"""<p>Een badkamer en suite ligt vaak niet boven de keuken of de bestaande badkamer. De afvoer moet dan een eind lopen tot de standleiding, met genoeg afschot. Een toilet heeft een afvoer van 90 tot 110 mm nodig. Dat past niet altijd in de vloer. Oplossingen zijn een verhoogde vloer of een voorzetwand, en als het echt niet anders kan een vermaler-pomp (een toilet met pomp), die ook geluid maakt.</p>
<p>Volgens de richtprijzen op deze site kost nieuw leidingwerk {P_LEIDING}, en komen leidingen naar een andere plek brengen daar {P_LEIDING_VERPL} bovenop. Bij een badkamer op een nieuwe plek horen ook warm water (hoe ver is de ketel?) en een eigen groep voor de elektra. Laat dit als eerste beoordelen, voordat je verder ontwerpt.</p>"""),
("vocht", "Ventilatie en vocht",
"""<p>Douchedamp die de slaapkamer in trekt, geeft vocht en schimmel op koude plekken. Een badkamer en suite heeft daarom een eigen mechanische afzuiging nodig, die rechtstreeks naar buiten afvoert. Voor nieuwbouw geldt in het Bbl een afvoercapaciteit van 14 dm³/s voor een badruimte en 7 dm³/s voor een toiletruimte (artikel 4.122). Een ventilator met nalooptijd of vochtsensor houdt het droog zonder dat je eraan denkt. Bij een open badkamer zonder deur is dit nog belangrijker. Meer in <a href="/kennisbank/badkamer-ventilatie/">badkamer ventilatie</a> en de kosten op <a href="/kosten/badkamer-ventilatie/">badkamer ventilatie</a>.</p>"""),
("privacy", "Geluid, geur en privacy",
"""<ul class="checklist">
<li><strong>Toilet apart.</strong> Een toilet in een eigen hokje of achter een deur is voor de meeste stellen prettiger dan een toilet in het zicht van het bed.</li>
<li><strong>Stille techniek.</strong> Kies een stil inbouwreservoir en een ventilator met laag geluid. Isoleer de afvoerleidingen in de wand.</li>
<li><strong>Licht.</strong> Een gedimd nachtlicht of een bewegingssensor voorkomt dat je partner wakker wordt van fel licht; zie <a href="/kennisbank/badkamerverlichting/">badkamerverlichting</a>.</li>
<li><strong>Deur.</strong> Een schuifdeur of een deur die naar de slaapkamer opendraait wint ruimte. Matglas geeft licht met privacy.</li>
</ul>"""),
("regels", "VvE, vergunning en zolder",
"""<p>Een badkamer binnen de bestaande woning bouwen is meestal vergunningvrij, zolang je niets aan de draagconstructie of de gevel verandert. Een nieuwe dakkapel of een doorbraak in een dragende muur vraagt wel om aandacht. In een appartement beslist de VvE mee over afvoer en ventilatie, en vaak over geluidsisolatie in de vloer. Lees <a href="/kennisbank/verbouwen-in-vve/">verbouwen in een VvE</a> en, als de badkamer op zolder komt, <a href="/kennisbank/badkamer-op-zolder/">een badkamer op zolder</a>.</p>"""),
],
"stappen_kop": "Stappenplan",
"stappen": [
("Laat de afvoer beoordelen", "Kan een toilet en douche met genoeg afschot naar de standleiding?"),
("Kies de indeling", "Open of met een deur, en het toilet bij voorkeur apart."),
("Plan ventilatie", "Een eigen afzuiging rechtstreeks naar buiten, met nalooptijd of vochtsensor."),
("Denk aan geluid en licht", "Stil reservoir, geïsoleerde afvoer en een nachtlicht."),
("Vraag offertes met tekening", "Met de plek van afvoer, ventilatie en elektra erop."),
],
"faq": [
("Hoeveel ruimte heb ik nodig voor een badkamer en suite?", "Een compacte versie met douche en wastafel past in ongeveer 2 tot 3 m². Met een toilet en wat meer bewegingsruimte is 3 tot 5 m² prettiger."),
("Kan een badkamer en suite zonder deur?", "Ja, maar dan zijn ventilatie en vochtwering extra belangrijk. Zet het toilet in dat geval apart achter een deur."),
("Wat als de afvoer niet ver genoeg kan?", "Soms helpt een verhoogde vloer of een voorzetwand. Een vermaler-pomp kan ook, maar maakt geluid en vraagt onderhoud."),
("Heb ik een vergunning nodig?", "Meestal niet als je binnen de woning bouwt zonder de draagconstructie of de gevel te veranderen. Twijfel je, check het bij je gemeente."),
("Wat kost een badkamer en suite?", "Dat hangt vooral af van de afvoer, de grootte en het sanitair. Reken op de kosten van een complete badkamer, plus extra leidingwerk als het een nieuwe plek is."),
],
"bronnen": [IPLO_BADRUIMTE, IPLO_VENTILATIE, BBL, TRUSTOO_BADKAMER, SLIMSTER_BADKAMER],
"dienst": "badkamer-installeren",
"kosten": ["nieuwe-badkamer", "badkamer-op-zolder"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/inloopdouche-kopen/", "Inloopdouche kopen", "Wand, goot en douchekop kiezen.")],
"gerelateerd": ["badkamer-op-zolder", "badkamer-ventilatie", "badkamer-ontwerpen"],
},
]
