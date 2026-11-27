# -*- coding: utf-8 -*-
"""Kennisbank ronde 5: acht nieuwe artikelen (ARTIKELEN4) en verdieping van zes bestaande (VERDIEPING).

Zelfde opbouw als badkamer_kennis_artikelen3.py. badkamer_kennis.py voegt de lijsten samen
(ARTIKELEN + ARTIKELEN2 + ARTIKELEN3 + ARTIKELEN4) en past VERDIEPING toe op de bestaande artikelen:
    VERDIEPING[slug] = {
        "vervang": {sectie_id: (kop, html)},   # bestaande sectie vervangen (optioneel)
        "secties": [(id, kop, html), ...],      # achteraan toegevoegd
        "faq": [(vraag, antwoord), ...],        # achter de bestaande FAQ
        "bronnen": [(label, url), ...],
        "gerelateerd": [slug, ...],             # extra "Lees ook"
        "extra": [(href, naam, omschrijving)],  # extra kaartjes
    }

Zoekwoorden (Semrush, database nl, november 2026, volume per maand):
    kit verwijderen 2400, badkamer kitten 1300, kitten badkamer 720, douche kitten 210;
    afvoer ontstoppen 5400, afvoer verstopt 2400, wastafel verstopt 320, douche afvoer verstopt 260;
    rioollucht badkamer 590, badkamer stinkt 30;
    badkamer plafond 1600, badkamerplafond 480;
    pvc vloer badkamer 1300, badkamer vloer 880, badkamervloer 320;
    badkamer tegelen 390, zelf badkamer tegelen 170, tegels over tegels 320, tegels zetten badkamer 70;
    badkamer schilderen 390, tegels schilderen badkamer 210;
    badkamer zonder raam 260.

Feitencontrole (november 2026, WebSearch):
- Kit: sanitairkit ongeveer 24 uur laten drogen voor je doucht, helemaal uitgehard na ongeveer een week
  (Slimster, Hoe lang moet kit drogen; GAMMA klusadvies badkamer kitten). Altijd de koker volgen.
- Ontstoppen: Slimster gemiddeld €90 (€40 tot €150); Homedeal afvoer in douche of wastafel €100 tot €180,
  riool €150 tot €300, camera-inspectie €150 tot €250, toeslag buiten kantoortijd 25 tot 100%.
  Radar (AVROTROS): chemische ontstoppers afgeraden (natriumhydroxide of zwavelzuur), eerst heet
  (niet kokend) water en een plopper.
- Rioollucht: droge of leeggezogen sifon, vuil in de sifon, lekke afvoer na de sifon, ontbrekende
  beluchting (Werkspot, Stinkend doucheputje; gemeente Geldrop-Mierlo, Veel voorkomende rioolproblemen).
- Plafond: spanplafond in de badkamer €80 tot €150 per m², pvc-spanplafond €70 tot €90 per m²
  inclusief plaatsing (Werkspot, Kosten spanplafond plaatsen).
- Vloer: pvc-vloer €35 tot €75 per m² inclusief leggen (Werkspot); gietvloer €50 tot €100 per m²
  (Werkspot), €60 tot €150 per m² (Slimster).
- Tegels verven: €15 tot €38 per m² inclusief arbeid en materiaal (Werkspot, Tegels verven);
  tweecomponentenlak of epoxy voor de natte zone.
- Badkamer zonder raam: Bbl art. 4.122 lid 5 (14 dm³/s afvoer badruimte, nieuwbouw) en art. 4.128
  (afvoer rechtstreeks naar buiten), via IPLO. Daglichteis geldt voor verblijfsruimten, niet voor de
  badruimte.
Overige prijzen komen uit richtprijzen.py (incl. 21% btw, behalve uurtarief en voorrijkosten).
"""

import richtprijzen as RP
from components import eur
from badkamer_kennis_artikelen import BBL, IPLO_VOCHT, IPLO_BADRUIMTE, IPLO_VENTILATIE, NEN, IPLO_ASBEST, \
    IPLO_ASBEST_NL, RIJK_VVE
from badkamer_kennis_artikelen2 import MC_SCHIMMEL, MC_VENTILEREN, MC_VLOERVERWARMING, MC_LTV


def _bereik(sleutel, factor=1):
    lo, hi = RP.lh(sleutel, factor)
    return f"{eur(int(lo))} tot {eur(int(hi))}"


def _niveau(sleutel, niveau):
    lo, hi = RP.niveaus(sleutel)[niveau]
    return f"{eur(lo)} tot {eur(hi)}"


# Richtprijzen uit richtprijzen.py (incl. btw, behalve uurtarief en voorrijkosten)
P_UUR = _bereik("uurtarief")                     # excl. btw
P_VOORRIJ = _bereik("voorrijkosten")             # excl. btw
P_KIT_M = _bereik("kitwerk")                     # per meter
P_KIT = _bereik("kitwerk_badkamer")
P_TEGELWERK = _bereik("tegelwerk")               # legloon per m²
P_TEGELS = _bereik("tegels")
P_TEGELS_BASIS = _niveau("tegels", "basis")
P_TEGELS_LUXE = _niveau("tegels", "luxe")
P_HULP = eur(RP.RICHTPRIJZEN["tegelwerk_hulpmateriaal"]["laag"])
P_WATERDICHT = _bereik("waterdicht")
P_VENTILATOR = _bereik("ventilator")
P_ELEKTRA = _bereik("elektra")
P_SLOOP = _bereik("sloop")
P_SLOOP_COMPLEET = _bereik("sloop_compleet")
P_AFVAL = _bereik("afval")
P_CONTAINER = _bereik("container")
P_LEIDING = _bereik("leidingwerk")
P_LEIDING_VERPL = _bereik("leidingwerk_verplaatsen")
P_TOILET_VERPL = _bereik("leidingwerk_toilet_verplaatsen")
P_MONTAGE_DOUCHE = _bereik("montage_douche")
P_MONTAGE_TOILET = _bereik("montage_toilet")
P_MONTAGE_MEUBEL = _bereik("montage_meubel")
P_DOUCHE_BASIS = _niveau("sanitair_douche", "basis")
P_DOUCHE_MIDDEN = _niveau("sanitair_douche", "midden")
P_DOUCHE_LUXE = _niveau("sanitair_douche", "luxe")
P_TOILET_MIDDEN = _niveau("sanitair_toilet", "midden")
P_MEUBEL_BASIS = _niveau("sanitair_meubel", "basis")
P_MEUBEL_MIDDEN = _niveau("sanitair_meubel", "midden")
P_VV_M2 = _bereik("vloerverwarming_m2")
P_VV_ELEKTRISCH = _bereik("vloerverwarming_elektrisch")
P_VV = _bereik("vloerverwarming")

# Nieuwe prijzen in deze module, met bron (prijzen zoals de bron ze voor particulieren noemt):
P_ONTSTOPPEN = f"{eur(100)} tot {eur(180)}"       # Homedeal: afvoer douche of wastafel
P_ONTSTOPPEN_GEM = eur(90)                         # Slimster: gemiddeld, €40 – €150
P_RIOOL = f"{eur(150)} tot {eur(300)}"            # Homedeal: riool ontstoppen
P_CAMERA = f"{eur(150)} tot {eur(250)}"           # Homedeal: camera-inspectie
P_SPANPLAFOND = f"{eur(80)} tot {eur(150)}"       # Werkspot: spanplafond badkamer per m²
P_PVC_SPAN = f"{eur(70)} tot {eur(90)}"           # Werkspot: pvc-spanplafond per m² incl. plaatsing
P_PVC_VLOER = f"{eur(35)} tot {eur(75)}"          # Werkspot: pvc-vloer per m² incl. leggen
P_GIETVLOER = f"{eur(50)} tot {eur(100)}"         # Werkspot: gietvloer per m²
P_TEGELVERF = f"{eur(15)} tot {eur(38)}"          # Werkspot: tegels verven per m², incl. arbeid

# Bronnen
SLIMSTER_KIT_DROGEN = ("Slimster, Hoe lang moet kit drogen?", "https://slimster.nl/blog/hoe-lang-moet-kit-drogen/")
GAMMA_KITTEN = ("GAMMA klusadvies, Badkamer kitten", "https://www.gamma.nl/klusadvies/a/badkamer-kitten")
WERKSPOT_KIT = RP.BRONNEN["werkspot_kit"]
SLIMSTER_KIT = RP.BRONNEN["slimster_kit"]
SLIMSTER_ONTSTOPPEN = ("Slimster, Wat kost een afvoer ontstoppen?", "https://slimster.nl/loodgieter/kosten-afvoer-ontstoppen/")
HOMEDEAL_VERSTOPPING = ("Homedeal, Verstopping verhelpen: kosten", "https://www.homedeal.nl/prijsgidsen/verstopping-verhelpen-kosten/")
RADAR_ONTSTOPPEN = ("Radar (AVROTROS), Afvoer ontstoppen van je wc, douche, gootsteen of wastafel",
                    "https://radar.avrotros.nl/hulp-tips/hulpartikelen/item/afvoer-ontstoppen-van-je-wc-douche-gootsteen-of-wastafel-zo-doe-je-het/")
RADAR_VLOEIBAAR = ("Radar (AVROTROS), Waarom je beter geen vloeibare ontstoppers kunt gebruiken",
                   "https://radar.avrotros.nl/artikel/dit-is-waarom-je-beter-geen-vloeibare-ontstoppers-kunt-gebruiken-38263")
WERKSPOT_PUTJE = ("Werkspot, Stinkend doucheputje? Dit is er aan de hand",
                  "https://www.werkspot.nl/loodgieterswerk/artikelen/wat-te-doen-bij-een-stinkend-doucheputje")
GELDROP_RIOOL = ("Gemeente Geldrop-Mierlo, Veel voorkomende rioolproblemen (pdf)",
                 "https://www.geldrop-mierlo.nl/_flysystem/media/1548944814Veel_voorkomende_rioolproblemen.pdf")
WERKSPOT_SPANPLAFOND = ("Werkspot, Kosten spanplafond plaatsen", "https://www.werkspot.nl/stucen/prijzen-kosten/kosten-spanplafond-plaatsen")
WERKSPOT_PLAFOND_VERLAGEN = ("Werkspot, Kosten verlaagd plafond", "https://www.werkspot.nl/stucen/prijzen-kosten/plafonds-plaatsen-verlagen")
WERKSPOT_PVC = ("Werkspot, Pvc-vloer laten leggen: kosten", "https://www.werkspot.nl/vinyl-linoleum-pvc-vloer-leggen/prijzen-kosten")
WERKSPOT_GIETVLOER = ("Werkspot, Gietvloer aanbrengen: kosten", "https://www.werkspot.nl/vloeren-tegels/prijzen-kosten/gietvloer-aanbrengen")
SLIMSTER_GIETVLOER = ("Slimster, Wat kost een gietvloer?", "https://slimster.nl/vloeren/kosten/gietvloer-prijzen")
WERKSPOT_TEGELVERF = ("Werkspot, Tegels verven: wat zijn de gemiddelde kosten?", "https://www.werkspot.nl/tegels-verven/prijzen-kosten")
WERKSPOT_TEGELVERF_TIPS = ("Werkspot, Badkamertegels verven: waar let je op?",
                           "https://www.werkspot.nl/schilderen/artikelen/badkamertegels-verven-waar-let-je-op")
SLIMSTER_SCHILDEREN = ("Slimster, Wat kost een badkamer schilderen?",
                       "https://slimster.nl/schilder/schilderwerk-prijzen/kosten-badkamer-schilderen/")
GAMMA_TEGELVERF = ("GAMMA klusadvies, Tegels verven: stappenplan", "https://www.gamma.nl/klusadvies/verven/stappenplan/tegels-verven")
WERKSPOT_TEGEL = RP.BRONNEN["werkspot_tegel"]
HOMEDEAL_TEGEL = RP.BRONNEN["homedeal_tegel"]
TRUSTOO_TEGEL = RP.BRONNEN["trustoo_tegel"]
TRUSTOO_BADKAMER = RP.BRONNEN["trustoo_badkamer"]
SLIMSTER_BADKAMER = RP.BRONNEN["slimster_badkamer"]
SLIMSTER_SLOPEN = RP.BRONNEN["slimster_slopen"]
WERKSPOT_VV = RP.BRONNEN["werkspot_vv"]
HOMEDEAL_DOUCHE = RP.BRONNEN["homedeal_douche"]
HOMEDEAL_TOILET = RP.BRONNEN["homedeal_toilet"]
RIJK_ASBEST_PART = ("Rijksoverheid, Mag ik zelf asbest verwijderen?",
                    "https://www.rijksoverheid.nl/onderwerpen/asbest/vraag-en-antwoord/mag-ik-zelf-asbest-verwijderen")
OMGEVINGSLOKET = ("Omgevingsloket, sloopmelding doen", "https://omgevingswet.overheid.nl/")
GEBERIT_HOOGTE = ("Geberit, The perfect installation height for washbasins, WCs and more",
                  "https://www.geberit.co.uk/inspiration/stories/the-perfect-installation-height")
HORNBACH_WC = ("HORNBACH, Soorten wc's en de juiste hoogte", "https://www.hornbach.nl/projecten/wc-inrichten/")
WERKSPOT_ASBEST_INV = ("Werkspot, Kosten asbestinventarisatie",
                      "https://www.werkspot.nl/sloop-afvoeren/prijzen-kosten/kosten-asbestinventarisatie")
WERKSPOT_ASBEST = ("Werkspot, Asbest verwijderen: kosten", "https://www.werkspot.nl/sloop-afvoeren/prijzen-kosten/asbest-verwijderen")
HOMEDEAL_ASBEST_INV = ("Homedeal, Asbestinventarisatie: kosten",
                       "https://www.homedeal.nl/asbest-verwijderen/asbestinventarisatie-kosten/")
SLIMSTER_ASBEST_INV = ("Slimster, Wat kost een asbestinventarisatie?",
                       "https://slimster.nl/asbest/asbestinventarisatie/kosten-inventarisatie/")
TRUSTOO_ASBEST = ("Trustoo, Asbest verwijderen kosten", "https://trustoo.nl/kosten/asbest-kosten/")
BOBEX_TOILET = ("Bobex, Afmetingen toilet: de juiste hoogte vinden", "https://www.bobex.be/nl-be/badkamerrenovatie/toilet/hoogte/")

# Eenvoudige opmaak, gelijk aan badkamer_kennis_artikelen3.py
_FIG = 'style="margin:22px 0;padding:16px;background:#fff;border:1px solid var(--line);border-radius:var(--radius)"'
_CAP = 'style="font-size:.88rem;margin-top:8px;color:var(--muted)"'


def _vakman(vragen):
    """Blok 'Wat vraag je aan de vakman?' als genummerde lijst."""
    return "<ol>" + "".join(f"<li>{v}</li>" for v in vragen) + "</ol>"


ARTIKELEN4 = [
# ---------------------------------------------------------------------------
{
"slug": "badkamer-kitten",
"groep": "Techniek en vocht",
"titel": "Badkamer kitten: oude kit verwijderen en strak opnieuw kitten",
"seo_titel": "Badkamer kitten: kit verwijderen en opnieuw kitten",
"description": "Zelf de badkamer kitten? Lees hoe je oude kit verwijdert, welke kit je kiest, hoe je een strakke kitrand maakt, hoe lang kit moet drogen en wat een kitter kost.",
"kort": "Oude kit eruit, ondergrond schoon en droog, nieuwe sanitairkit erin: zo krijg je een strakke en schimmelvrije kitrand.",
"intro": "Je kitrand opnieuw doen is een van de klussen die je in de badkamer het vaakst tegenkomt. Kit wordt na een paar jaar zwart van schimmel, laat los of scheurt. Dan kan er water achter je tegels of je douchebak komen. In dit artikel lees je hoe je oude kit verwijdert, welke kit je kiest, hoe je in vijf stappen een strakke kitrand maakt en wanneer je het beter laat doen.",
"kort_antwoord": "Snijd de oude kit los met een scherp mesje, haal de resten weg met een kitverwijderaar en maak de naad vet- en stofvrij. Laat de naad helemaal droog worden. Breng daarna sanitairkit met schimmelwerend middel aan, strijk die in één keer glad en wacht ongeveer 24 uur voordat je doucht. Een vakman doet een hele badkamer voor ongeveer " + P_KIT + ".",
"secties": [
("wanneer", "Wanneer moet de kit eruit?",
"""<p>Kit is onderhoud, geen bouwmateriaal voor de eeuwigheid. In een badkamer die elke dag gebruikt wordt, gaat een kitrand vaak vijf tot tien jaar mee. Vervang de kit als je een van deze dingen ziet:</p>
<ul class="checklist">
<li><strong>Zwarte puntjes die niet weg te poetsen zijn.</strong> Dan zit de schimmel in de kit zelf. Schoonmaken helpt niet meer.</li>
<li><strong>Losse randen of kieren.</strong> Steek er voorzichtig een nagel achter. Laat de kit los, dan kan er water achter lopen.</li>
<li><strong>Scheuren of gaten,</strong> vaak in de hoek van de douchebak of langs het bad, waar het meeste beweegt.</li>
<li><strong>Verkleurde of harde kit</strong> die niet meer veert als je erop drukt.</li>
</ul>
<p>Twijfel je of er al water achter de kit zit? Kijk dan in het artikel over <a href="/kennisbank/lekkage-badkamer/">lekkage in de badkamer</a>. Een donkere rand op het plafond eronder, losse tegels of een muffe geur zijn signalen dat er meer aan de hand is dan alleen een oude kitrand.</p>"""),
("soorten", "Welke kit kies je?",
"""<p>In de badkamer gebruik je bijna altijd <strong>sanitairkit</strong>: siliconenkit met een schimmelwerend middel. Die blijft elastisch, kan tegen water en zeep en hecht op tegels, glas, emaille en acryl. Andere soorten kit hebben elk hun eigen plek.</p>
<div class="tablewrap"><table>
<thead><tr><th>Soort kit</th><th>Geschikt voor</th><th>Niet voor</th></tr></thead>
<tbody>
<tr><td>Sanitairkit (siliconen, schimmelwerend)</td><td>Naden rond douchebak, bad, wastafel, toilet en in binnenhoeken van tegelwerk</td><td>Overschilderen; natuursteen (kan randen verkleuren)</td></tr>
<tr><td>Natuursteenkit</td><td>Marmer, hardsteen en andere natuursteen</td><td>Algemeen gebruik; is duurder</td></tr>
<tr><td>Acrylaatkit</td><td>Droge naden die je wilt schilderen, zoals bij plafond en kozijn</td><td>Natte zones: wordt niet waterdicht genoeg</td></tr>
<tr><td>Hybride of MS-polymeerkit</td><td>Lijmen en kitten in één, bijvoorbeeld een spiegel of plint</td><td>Douchehoek, tenzij de fabrikant het uitdrukkelijk toestaat</td></tr>
</tbody></table></div>
<p>Kies een kleur die bij je voeg past. Wit en transparant zijn het meest gebruikt; grijze of antraciete kit valt minder op bij donkere voegen. Lees meer over voeg en kit als materiaal bij <a href="/materialen/voegen-en-kit/">voegen en kit</a>.</p>"""),
("verwijderen", "Oude kit verwijderen",
"""<p>Nieuwe kit hecht niet op oude kit. Ook resten van siliconen zorgen ervoor dat de nieuwe kitrand snel loslaat. Neem daarom de tijd voor deze stap.</p>
<ol>
<li><strong>Snijd de kit los</strong> met een scherp afbreekmes of een speciaal kitmes. Snijd langs de tegel en langs de douchebak, en trek de kitrups er dan in één stuk uit.</li>
<li><strong>Schraap de resten weg</strong> met een kunststof kitschraper of een verfkrabber. Wees voorzichtig met emaille, acryl en glas: een metalen mes geeft snel krassen.</li>
<li><strong>Gebruik een kitverwijderaar</strong> voor de laatste dunne laag. Laat die inwerken volgens de verpakking en schraap daarna opnieuw. Soms is twee keer nodig.</li>
<li><strong>Behandel schimmel</strong> in de voeg naast de kit met een schimmelreiniger en spoel goed na. Kijk voor aanpak en oorzaak in <a href="/kennisbank/schimmel-in-badkamer/">schimmel in de badkamer</a>.</li>
<li><strong>Ontvet</strong> de naad met spiritus of een ontvetter en laat alles goed drogen. Zet een raam open of de ventilator aan. Kit op een vochtige naad hecht slecht.</li>
</ol>"""),
("aanbrengen", "In vijf stappen strak kitten",
"""<p>Een strakke kitrand is vooral een kwestie van voorbereiden. De meeste klussers zetten de kit goed, maar maken de rand rommelig bij het gladstrijken.</p>
<ol>
<li><strong>Vul het bad.</strong> Een bad zakt een paar millimeter als het vol is. Kit je het bad leeg, dan scheurt de kit bij het eerste bad. Laat het water staan tot de kit droog is. Bij een douchebak waar je op staat geldt hetzelfde idee: kit niet als de bak onder spanning staat.</li>
<li><strong>Plak af</strong> met schilderstape aan weerszijden van de naad, op 2 tot 4 mm van de hoek. Zo krijg je een rechte lijn.</li>
<li><strong>Snijd de spuitmond schuin af</strong>, iets kleiner dan de breedte van de naad. Spuit in één rustige beweging een rups die de naad helemaal vult. Is de naad dieper dan 1 cm, druk er dan eerst een rondschuim (rugvulling) in.</li>
<li><strong>Strijk glad</strong> met een kitspaan of een vinger die je nat maakt met water en een druppel afwasmiddel. Werk in één beweging van hoek naar hoek. Haal overtollige kit weg met een doek.</li>
<li><strong>Trek de tape eraf</strong> zolang de kit nog nat is, schuin van de kitrand af. Raak de kitrand daarna niet meer aan.</li>
</ol>
<p>Werk per naad en niet de hele badkamer tegelijk: sanitairkit vormt na een paar minuten een vel en dan kun je hem niet meer mooi gladstrijken.</p>"""),
("drogen", "Hoe lang moet kit drogen?",
"""<p>Sanitairkit is na ongeveer een kwartier tot een half uur huiddroog. Douchen kan meestal na ongeveer 24 uur. Helemaal uitgehard is de kit pas na ongeveer een week, afhankelijk van de dikte van de rups, de temperatuur en de luchtvochtigheid. Kijk altijd op de koker: daar staat de droogtijd van dat merk. Er zijn ook snel drogende sanitairkitten waarbij je eerder kunt douchen.</p>
<p>Na het drogen houd je de kit het langst mooi door na het douchen de kitrand droog te trekken en goed te ventileren. Lees in <a href="/kennisbank/badkamer-ventilatie/">badkamer ventilatie</a> hoe lang de ventilator moet nadraaien, en in <a href="/kennisbank/badkamer-schoonmaken/">badkamer schoonmaken</a> welke middelen kit niet aantasten.</p>"""),
("kosten", "Wat kost kitten laten doen?",
f"""<p>Volgens de richtprijzen op deze site kost opnieuw kitten ongeveer {P_KIT_M} per strekkende meter, inclusief het verwijderen van de oude kit en inclusief btw. Een hele badkamer opnieuw afkitten kost ongeveer {P_KIT}. Een kitter of klusbedrijf rekent soms een minimumbedrag of voorrijkosten, dus een paar meter laten doen is relatief duur. Combineer het daarom met ander klein onderhoud, zoals voegen bijwerken of een kraan vervangen.</p>
<div class="tablewrap"><table>
<thead><tr><th>Zelf doen</th><th>Laten doen</th></tr></thead>
<tbody>
<tr><td>Koker sanitairkit, kitpistool, kitverwijderaar, schraper en tape: samen meestal enkele tientjes</td><td>{P_KIT} voor een hele badkamer, of {P_KIT_M} per meter</td></tr>
<tr><td>Een middag werk plus een dag droogtijd</td><td>Vaak binnen een paar uur klaar, met een strakke rand</td></tr>
<tr><td>Risico: kit hecht slecht als de naad niet schoon en droog is</td><td>Vraag of er garantie op hechting zit</td></tr>
</tbody></table></div>
<p>Meer rekenvoorbeelden vind je op <a href="/kosten/kitwerk-voegen/">kosten kitwerk en voegen</a>.</p>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Haalt u alle oude kit en kitresten weg, of kit u eroverheen? (Eroverheen kitten is geen goed werk.)",
"Welke kit gebruikt u in de douche, en bij natuursteen?",
"Is de naad droog genoeg, en hoe controleert u dat?",
"Zit er onder de kit nog een afdichting met kimband, of is de kit de enige bescherming?",
"Hoe lang moet ik wachten met douchen, en wat is de garantie op hechting?",
"Ziet u tekenen van lekkage achter de kit, zoals losse tegels of vocht in de wand?",
])),
],
"stappen_kop": "Checklist kitten",
"stappen": [
("Oude kit eruit", "Snijden, schrapen en de laatste resten weg met kitverwijderaar."),
("Schoon en droog", "Schimmel weg, ontvetten en de naad een paar uur laten drogen."),
("Afplakken", "Tape aan beide kanten, en het bad vullen met water."),
("Kitten en gladstrijken", "Eén rups per naad, in één beweging gladstrijken, tape eraf terwijl de kit nat is."),
("Laten drogen", "Ongeveer 24 uur niet douchen, en daarna goed ventileren."),
],
"faq": [
("Kan ik nieuwe kit over oude kit spuiten?", "Nee. Nieuwe kit hecht slecht op oude kit en sluit vuil en schimmel in. Haal de oude kit altijd helemaal weg."),
("Hoe lang moet sanitairkit drogen voor ik kan douchen?", "Meestal ongeveer 24 uur. Helemaal uitgehard is kit na ongeveer een week. De koker vermeldt de precieze tijd van dat merk."),
("Waarom wordt mijn kit steeds zwart?", "Schimmel groeit op kit die vaak nat blijft. Ventileer na het douchen, trek de kitrand droog en kies sanitairkit met een schimmelwerend middel. Komt het snel terug, kijk dan ook naar de ventilatie."),
("Moet het bad vol zitten als ik kit?", "Ja. Een vol bad zakt een paar millimeter. Kit je het bad leeg, dan scheurt of laat de kit los zodra je in bad gaat."),
("Welke kit gebruik ik bij natuursteen?", "Gebruik speciale natuursteenkit. Gewone sanitairkit kan bij natuursteen vlekken langs de rand geven."),
("Hoe vaak moet je de badkamer opnieuw kitten?", "Gemiddeld na vijf tot tien jaar, of eerder als de kit loslaat, scheurt of zwart is van schimmel die niet meer weg gaat."),
("Is kit genoeg om de douche waterdicht te maken?", "Nee. Kit beschermt de naden, maar de echte afdichting zit onder de tegels. Lees daarover meer in het artikel over waterdicht maken."),
],
"bronnen": [SLIMSTER_KIT_DROGEN, GAMMA_KITTEN, WERKSPOT_KIT, SLIMSTER_KIT, MC_SCHIMMEL],
"dienst": "badkamer-onderhoud",
"kosten": ["kitwerk-voegen"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["schimmel-in-badkamer", "lekkage-badkamer", "badkamer-waterdicht-maken", "badkamer-schoonmaken"],
},
# ---------------------------------------------------------------------------
{
"slug": "afvoer-ontstoppen",
"groep": "Techniek en vocht",
"titel": "Afvoer ontstoppen: douche, wastafel en bad weer vrij zonder chemie",
"seo_titel": "Afvoer ontstoppen in de badkamer: zo doe je het",
"description": "Douche of wastafel verstopt? Zo ontstop je de afvoer zelf met heet water, een plopper of ontstopveer, zonder chemie. Plus wat een loodgieter kost.",
"kort": "Heet water, een plopper, de sifon schoonmaken of een ontstopveer: zo krijg je de meeste verstoppingen zelf weg.",
"intro": "Een afvoer die traag leegloopt of helemaal vastzit, is een van de vaakste problemen in de badkamer. Meestal zit er een prop van haar, zeep en kalk vlak onder het putje of in de sifon. Die krijg je vaak zelf weg, zonder bijtende middelen. In dit artikel lees je hoe je stap voor stap ontstopt, wat je beter niet doet, wanneer je een loodgieter belt en hoe je nieuwe verstoppingen voorkomt.",
"kort_antwoord": "Begin met heet (niet kokend) water en een plopper. Helpt dat niet, maak dan het putje of de sifon schoon, en gebruik daarna een ontstopveer. Chemische ontstopper wordt afgeraden: het is bijtend en lost een haarprop vaak niet op. Zit de verstopping dieper of lopen meerdere afvoeren slecht weg, bel dan een loodgieter. Die rekent voor een afvoer in douche of wastafel vaak " + P_ONTSTOPPEN + ".",
"secties": [
("oorzaak", "Waar zit de verstopping meestal?",
"""<p>In de badkamer is een verstopping bijna altijd een mengsel van haar, zeepresten, huidvet en kalk. Dat blijft hangen op plekken waar het water een bocht maakt of langzaam stroomt.</p>
<div class="tablewrap"><table>
<thead><tr><th>Plek</th><th>Typische oorzaak</th><th>Wat je merkt</th></tr></thead>
<tbody>
<tr><td>Douchegoot of doucheputje</td><td>Haar en zeep in het rooster en de stankafsluiter</td><td>Water blijft rond je voeten staan</td></tr>
<tr><td>Wastafelsifon</td><td>Tandpasta, scheerhaar, zeep en kalk</td><td>Wastafel loopt langzaam leeg, soms een geur</td></tr>
<tr><td>Afvoer van het bad</td><td>Haar en badolie rond de plug en overloop</td><td>Bad loopt traag leeg</td></tr>
<tr><td>Standleiding of riool</td><td>Vochtige doekjes, vet of een verzakte leiding</td><td>Meerdere afvoeren tegelijk traag, geborrel in de wc</td></tr>
</tbody></table></div>
<p>Die laatste rij is belangrijk. Lopen de douche, de wastafel en het toilet allemaal slecht weg, dan zit het probleem niet in één putje maar verderop in de leiding. Dan helpt zelf ploppen weinig en is een loodgieter of ontstoppingsbedrijf nodig.</p>"""),
("zelf", "Zelf ontstoppen in vijf stappen",
"""<p>Werk van licht naar zwaar. Stop zodra het water weer vrij wegloopt.</p>
<ol>
<li><strong>Haal het rooster eruit</strong> en trek met een haakje of een ontstopstrip (een kunststof strip met weerhaakjes) het haar uit het putje. Bij een douchegoot zit er vaak een bakje of stankafsluiter onder het rooster dat je eruit kunt tillen.</li>
<li><strong>Giet heet water</strong> in de afvoer, bijvoorbeeld een paar liter uit de waterkoker die even heeft afgekoeld. Gebruik geen kokend water: dat kan kunststof leidingen en de kitrand beschadigen.</li>
<li><strong>Gebruik een plopper.</strong> Zet de rubberen kop over het putje, zorg dat er een laagje water staat en duw een paar keer krachtig op en neer. Dek bij een wastafel of bad de overloop af met een natte doek, anders ontsnapt de druk.</li>
<li><strong>Maak de sifon schoon.</strong> Zet een emmer onder de wastafel, draai de sifon met de hand los en spoel hem om. Zet hem daarna terug met de rubberen ringen goed op hun plek, en controleer of hij niet lekt.</li>
<li><strong>Gebruik een ontstopveer.</strong> Draai de veer voorzichtig de afvoer in tot je weerstand voelt, draai dan door om de prop te pakken of te breken, en trek hem terug. Spoel na met heet water.</li>
</ol>
<p>Een hogedrukontstopper of een natte stofzuiger kan ook werken. Wees voorzichtig met de hogedrukvariant bij oude of gelijmde leidingen.</p>"""),
("chemie", "Waarom geen chemische ontstopper?",
"""<p>In de winkel liggen veel vloeibare ontstoppers en korrels. Consumentenprogramma Radar raadt die af. Ze bevatten vaak natriumhydroxide of zwavelzuur. Dat is bijtend voor je huid en ogen, kan dampen geven en is slecht voor het milieu. Een haarprop lost er vaak niet goed door op. Blijft het middel staan in een leiding die vastzit, dan sta je bij het ploppen of losdraaien van de sifon met een bijtende vloeistof te werken.</p>
<p>Heb je toch een middel gebruikt en zit de afvoer nog dicht? Zeg dat dan tegen de loodgieter, zodat die zich kan beschermen. Gebruik nooit twee verschillende middelen na elkaar: die kunnen met elkaar reageren.</p>
<p>Huismiddeltjes zoals soda met azijn zijn milder, maar werken vooral bij een lichte aanslag. Een echte prop haar haal je er niet mee weg.</p>"""),
("loodgieter", "Wanneer bel je een loodgieter?",
f"""<p>Bel een vakman als:</p>
<ul class="checklist">
<li>de vijf stappen hierboven niet helpen;</li>
<li>meerdere afvoeren tegelijk slecht weglopen of het toilet borrelt als je doucht;</li>
<li>er water omhoog komt in de douche als je ergens anders in huis water laat lopen;</li>
<li>de verstopping steeds terugkomt, want dan kan er iets mis zijn met het afschot of de leiding zelf;</li>
<li>je in een appartement woont en de verstopping in de gezamenlijke standleiding lijkt te zitten. Meld dat bij de VvE of verhuurder.</li>
</ul>
<p>Een loodgieter of ontstoppingsbedrijf heeft een elektrische veer, een hogedrukreiniger en vaak een camera. Met een camera-inspectie zie je of een leiding verzakt, gebroken of vol aanslag zit. Huur je? Dan is ontstoppen van een eigen putje meestal voor de huurder, maar een verstopte standleiding of riool vaak voor de verhuurder. Lees meer in <a href="/kennisbank/badkamer-huurwoning/">badkamer in een huurwoning</a>.</p>"""),
("kosten", "Wat kost ontstoppen?",
f"""<p>Prijzen voor ontstoppen zijn sterk afhankelijk van de plek, het moment en het bedrijf. Deze bedragen noemen prijsvergelijkers voor particulieren:</p>
<div class="tablewrap"><table>
<thead><tr><th>Klus</th><th>Richtprijs</th><th>Bron</th></tr></thead>
<tbody>
<tr><td>Afvoer van douche of wastafel ontstoppen</td><td>{P_ONTSTOPPEN}</td><td>Homedeal</td></tr>
<tr><td>Gemiddelde ontstopping</td><td>ongeveer {P_ONTSTOPPEN_GEM} (meestal {eur(40)} tot {eur(150)})</td><td>Slimster</td></tr>
<tr><td>Riool ontstoppen</td><td>{P_RIOOL}</td><td>Homedeal</td></tr>
<tr><td>Camera-inspectie</td><td>{P_CAMERA}</td><td>Homedeal</td></tr>
<tr><td>Uurtarief loodgieter (excl. btw)</td><td>{P_UUR}</td><td>richtprijzen op deze site</td></tr>
</tbody></table></div>
<p>Buiten kantoortijd, 's nachts of in het weekend rekenen veel bedrijven een toeslag van 25 tot 100 procent. Vraag altijd vooraf naar een vaste prijs of een maximum. Let op bedrijven die aan de telefoon een laag bedrag noemen en ter plekke een veel hogere rekening maken. Check vooraf de naam, het adres en de KvK-inschrijving. Zie ook <a href="/kosten/uurtarief-loodgieter/">kosten loodgieter per uur</a>.</p>"""),
("voorkomen", "Verstopping voorkomen",
"""<ul class="checklist">
<li><strong>Leg een haarvanger</strong> in het doucheputje of gebruik een goot met een uitneembaar haarzeefje. Maak die elke week leeg.</li>
<li><strong>Spoel de afvoer maandelijks door</strong> met heet water, en haal de stankafsluiter van de douchegoot er een paar keer per jaar uit om hem schoon te maken.</li>
<li><strong>Gooi geen doekjes, wattenstaafjes of haar</strong> in toilet of wastafel. Ook "doorspoelbare" vochtige doekjes lossen slecht op.</li>
<li><strong>Kies bij een renovatie</strong> een goot of putje dat je makkelijk schoon kunt maken, en laat de leiding met voldoende afschot leggen. Lees meer in <a href="/kennisbank/inloopdouche-zonder-drempel/">inloopdouche zonder drempel</a> en bij <a href="/badkamerspullen/douchegoot-kiezen/">douchegoot kiezen</a>.</li>
<li><strong>Ontkalk regelmatig</strong> in een gebied met hard water. Zie <a href="/kennisbank/kalk-en-waterhardheid/">kalk en waterhardheid</a>.</li>
</ul>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Wat kost het voorrijden, het eerste uur en elk volgend kwartier? Is er een toeslag buiten kantoortijd?",
"Kunt u een vaste prijs of een maximumbedrag noemen voordat u begint?",
"Waar zat de verstopping, en wat was de oorzaak?",
"Is een camera-inspectie zinvol, of is de leiding nu helemaal vrij?",
"Is het afschot van de leiding goed, of komt de verstopping waarschijnlijk terug?",
"Krijg ik een factuur met btw, KvK-nummer en een omschrijving van het werk?",
])),
],
"stappen_kop": "Stappenplan bij een verstopte afvoer",
"stappen": [
("Rooster eruit", "Haal zichtbaar haar en vuil weg met een haakje of ontstopstrip."),
("Heet water", "Een paar liter heet, niet kokend, water in de afvoer."),
("Ploppen", "Overloop afdekken en een paar keer krachtig ploppen."),
("Sifon of goot schoonmaken", "Losdraaien, omspoelen en lekvrij terugzetten."),
("Ontstopveer", "Door tot de prop, draaien en terugtrekken. Helpt dit niet: bel een loodgieter."),
],
"faq": [
("Wat is het beste middel om een afvoer te ontstoppen?", "Begin met heet water en een plopper, en maak daarna de sifon of het putje schoon. Een ontstopveer helpt bij een prop die dieper zit. Chemische ontstoppers worden afgeraden omdat ze bijtend zijn."),
("Mag ik kokend water in de afvoer gieten?", "Liever niet. Kokend water kan kunststof leidingen en kitranden beschadigen. Heet water dat even heeft afgekoeld werkt bijna net zo goed."),
("Wat kost een loodgieter voor een verstopte douche?", "Vaak " + P_ONTSTOPPEN + " voor een afvoer in de douche of wastafel. Buiten kantoortijd komt er een toeslag bij. Vraag vooraf een vaste prijs."),
("Waarom borrelt mijn toilet als ik doucht?", "Dat wijst vaak op een verstopping verderop in de leiding of op een probleem met de beluchting. Dan is een loodgieter nodig."),
("Wie betaalt ontstoppen in een huurhuis?", "Een eigen putje of sifon is meestal voor de huurder. Een verstopte standleiding of riool is vaak voor de verhuurder. Kijk in je huurcontract of vraag het na."),
("Helpt soda met azijn tegen een verstopping?", "Alleen bij lichte aanslag. Een prop haar of zeep krijg je er meestal niet mee weg. Gebruik dan een plopper of ontstopveer."),
("Hoe voorkom ik dat de douche steeds verstopt raakt?", "Gebruik een haarvanger, maak het putje elke week schoon en spoel de afvoer regelmatig door met heet water."),
],
"bronnen": [RADAR_ONTSTOPPEN, RADAR_VLOEIBAAR, SLIMSTER_ONTSTOPPEN, HOMEDEAL_VERSTOPPING, RP.BRONNEN["homedeal_lood"]],
"dienst": "badkamer-onderhoud",
"kosten": ["uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [("/badkamerspullen/douchegoot-kiezen/", "Douchegoot kiezen", "Goot of putje: welke is makkelijk schoon te houden?")],
"gerelateerd": ["rioollucht-badkamer", "kalk-en-waterhardheid", "inloopdouche-zonder-drempel", "badkamer-schoonmaken"],
},
# ---------------------------------------------------------------------------
{
"slug": "rioollucht-badkamer",
"groep": "Techniek en vocht",
"titel": "Rioollucht in de badkamer: oorzaken en oplossingen",
"seo_titel": "Rioollucht in de badkamer? Oorzaken en oplossingen",
"description": "Stinkt je badkamer naar riool? Lees de oorzaken, van een droge sifon tot een lekke afvoer of ontbrekende beluchting, en wat je zelf controleert.",
"kort": "Een droge of vuile sifon, een lekke afvoer of een leiding zonder beluchting: zo spoor je de rioollucht op.",
"intro": "Een rioollucht in de badkamer is vervelend, en soms een teken van een technisch probleem. Gelukkig is de oorzaak vaak simpel: een stankafsluiter die droog staat of vol vuil zit. In dit artikel lees je hoe een stankafsluiter werkt, welke oorzaken het meest voorkomen, wat je zelf in een kwartier controleert en wanneer je een vakman nodig hebt.",
"kort_antwoord": "Elke afvoer heeft een stankafsluiter: een bocht of bakje met water dat de rioollucht tegenhoudt. Staat die droog, is hij vuil of wordt hij leeggezogen, dan ruik je het riool. Laat eerst water lopen in alle afvoeren en maak putje en sifon schoon. Blijft de lucht hangen, dan kan er een lek in de afvoer zitten of ontbreekt beluchting. Laat dat door een loodgieter onderzoeken.",
"secties": [
("werking", "Hoe houdt een afvoer de stank tegen?",
"""<p>Onder elke wastafel, douche, bad en toilet zit een <strong>stankafsluiter</strong>, ook wel sifon of waterslot. Dat is een bocht of bakje waarin altijd een laagje water blijft staan. Dat water sluit de leiding af, zodat de lucht uit het riool niet je badkamer in komt.</p>
<p>Zo'n waterslot werkt alleen als er genoeg water in staat, als het schoon is en als de druk in de leiding goed blijft. Daarvoor heeft het rioolstelsel van je huis een <strong>ontluchting</strong>: een buis die via het dak naar buiten gaat, of een beluchter die lucht binnenlaat als dat nodig is. Ontbreekt die, dan kan het water uit de sifon worden gezogen als ergens anders in huis veel water wegloopt, bijvoorbeeld bij het doortrekken van het toilet.</p>"""),
("oorzaken", "De zes meest voorkomende oorzaken",
"""<div class="tablewrap"><table>
<thead><tr><th>Oorzaak</th><th>Hoe herken je het?</th><th>Oplossing</th></tr></thead>
<tbody>
<tr><td>Droge stankafsluiter</td><td>Stank uit een afvoer die je weinig gebruikt, zoals een tweede wastafel of logeerbadkamer</td><td>Een emmer water erin. Bij weinig gebruik elke paar weken herhalen</td></tr>
<tr><td>Vuil in sifon of putje</td><td>Stank vlak boven het putje, vaak met trage afvoer</td><td>Putje, goot en sifon schoonmaken</td></tr>
<tr><td>Stankafsluiter verkeerd teruggeplaatst</td><td>Stank na het schoonmaken van de douchegoot</td><td>Het bakje of de dompelbocht goed terugzetten</td></tr>
<tr><td>Leeggezogen waterslot</td><td>Geborrel als het toilet doorspoelt, daarna stank</td><td>Beluchting laten controleren of plaatsen</td></tr>
<tr><td>Lekke afvoer of losse verbinding</td><td>Stank ook als alle sifons vol staan, soms met vochtplekken</td><td>Loodgieter laat de leiding nakijken</td></tr>
<tr><td>Probleem in het riool</td><td>Stank in meerdere ruimtes, of bij buren</td><td>Gemeente (openbaar riool) of loodgieter (eigen leiding)</td></tr>
</tbody></table></div>
<p>Uit informatie van gemeenten en loodgieters blijkt dat de eerste twee oorzaken verreweg het vaakst voorkomen. Begin daarom altijd daar.</p>"""),
("zelf", "Wat controleer je zelf?",
"""<ol>
<li><strong>Laat in elke afvoer water lopen,</strong> ook in de afvoer van de wasmachine en een vloerputje in de bijkeuken. Een droog waterslot ergens anders kan je badkamer laten stinken.</li>
<li><strong>Maak het doucheputje of de goot schoon.</strong> Haal het rooster en de stankafsluiter eruit, maak alles schoon met een borstel en zet de stankafsluiter goed terug. Een goot zonder het bakje stinkt altijd.</li>
<li><strong>Maak de wastafelsifon schoon</strong> en kijk of de rubberen ringen er goed in zitten. Een sifon die niet goed aansluit op de muur laat lucht door.</li>
<li><strong>Ruik waar het het sterkst is.</strong> Komt de lucht uit de muur, uit de kitrand of van onder het bad? Dan is een lekke verbinding waarschijnlijker dan een sifon.</li>
<li><strong>Let op geborrel</strong> als je het toilet doortrekt. Borrelt de douche of wastafel, dan wordt het waterslot leeggezogen.</li>
</ol>
<p>Een verstopte afvoer en rioollucht gaan vaak samen. Lees ook <a href="/kennisbank/afvoer-ontstoppen/">afvoer ontstoppen</a>.</p>"""),
("renovatie", "Na een renovatie: let op bij de oplevering",
"""<p>Ruik je kort na een nieuwe badkamer een rioollucht, dan zit de oorzaak vaak in het werk zelf. Denk aan een afvoer zonder beluchting, een goot die niet goed op de leiding is aangesloten of een leiding met te weinig afschot, waardoor er water en vuil blijft staan. Meld het dan zo snel mogelijk schriftelijk bij het bedrijf dat de badkamer heeft gemaakt, met foto's en een omschrijving van wanneer je het ruikt. Dit valt onder de garantie. Lees in <a href="/kennisbank/garantie-badkamerrenovatie/">garantie op je badkamerrenovatie</a> hoe je dat aanpakt.</p>
<p>Ventileren helpt tegen de geur, maar lost de oorzaak niet op. Een goede afzuiging is wel belangrijk voor vocht en schimmel: zie <a href="/kennisbank/badkamer-ventilatie/">badkamer ventilatie</a>.</p>"""),
("kosten", "Wat kost het laten oplossen?",
f"""<p>Een loodgieter rekent meestal per uur plus voorrijkosten. Op deze site rekenen we met een uurtarief van {P_UUR} en voorrijkosten van {P_VOORRIJ} (beide excl. btw). Een sifon vervangen of een beluchter plaatsen is vaak binnen een uur klaar. Moet de loodgieter zoeken met een camera, dan kost een inspectie volgens Homedeal ongeveer {P_CAMERA}. Moet er een leiding achter de tegels worden vervangen, dan komen daar breek- en tegelwerk bij. Vraag in dat geval een offerte met een aparte post voor het herstel van tegels en kit.</p>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Is er een ontluchting of beluchter op de afvoer van de badkamer? Waar zit die?",
"Wordt het waterslot leeggezogen als het toilet doorspoelt?",
"Zijn alle verbindingen achter de wand en onder het bad dicht?",
"Heeft de leiding genoeg afschot, of blijft er water staan?",
"Is een camera-inspectie zinvol? Wat kost die?",
"Valt dit onder de garantie van de renovatie? (Bij een nieuwe badkamer.)",
])),
],
"stappen_kop": "Stappenplan bij rioollucht",
"stappen": [
("Alle afvoeren vullen", "Water in elke afvoer, ook die je weinig gebruikt."),
("Putje en goot schoon", "Rooster en stankafsluiter eruit, schoonmaken, goed terugzetten."),
("Sifon controleren", "Schoonmaken en kijken of de ringen en de aansluiting dicht zijn."),
("Opletten bij doortrekken", "Borrelt een afvoer? Dan ontbreekt waarschijnlijk beluchting."),
("Vakman inschakelen", "Blijft de lucht, laat dan de leiding en verbindingen controleren."),
],
"faq": [
("Waarom stinkt mijn doucheputje naar riool?", "Meestal staat de stankafsluiter droog, zit hij vol vuil of is hij na het schoonmaken niet goed teruggeplaatst. Maak het putje schoon en zet het bakje goed terug."),
("Waarom ruik ik riool als het toilet doorspoelt?", "Dan wordt het water uit een sifon gezogen doordat de leiding niet goed belucht is. Een loodgieter kan een beluchter plaatsen of de ontluchting controleren."),
("Is rioollucht gevaarlijk?", "Een lichte geur is vooral vervelend. Blijft een sterke lucht hangen, laat dan de oorzaak snel opsporen en ventileer goed tot het is opgelost."),
("Helpt een geurblokker of luchtverfrisser?", "Dat maskeert de geur alleen. Los de oorzaak op: een droge of vuile sifon, een lek of een probleem met de beluchting."),
("Wat kost een loodgieter voor rioollucht?", "Meestal een uurtarief van " + P_UUR + " plus voorrijkosten (excl. btw). Een camera-inspectie kost ongeveer " + P_CAMERA + "."),
("Mijn nieuwe badkamer stinkt naar riool. Wat nu?", "Meld het schriftelijk en met foto's bij het bedrijf dat de badkamer heeft gemaakt. Een fout in de afvoer of beluchting valt onder de garantie."),
],
"bronnen": [WERKSPOT_PUTJE, GELDROP_RIOOL, HOMEDEAL_VERSTOPPING, RP.BRONNEN["homedeal_lood"]],
"dienst": "badkamer-onderhoud",
"kosten": ["uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["afvoer-ontstoppen", "badkamer-ventilatie", "garantie-badkamerrenovatie", "lekkage-badkamer"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-plafond",
"groep": "Ontwerp en materialen",
"titel": "Badkamerplafond: welk plafond kies je en wat kost het?",
"seo_titel": "Badkamerplafond kiezen: soorten, vocht en kosten",
"description": "Welk plafond past in de badkamer? Vergelijk stucwerk, kunststof panelen, een spanplafond en een verlaagd plafond op vocht, onderhoud en kosten.",
"kort": "Stucwerk, kunststof panelen, spanplafond of verlaagd plafond: de voor- en nadelen in een vochtige ruimte.",
"intro": "Het plafond is de plek in de badkamer waar warme, vochtige lucht als eerste tegenaan komt. Daarom zie je daar vaak als eerste schimmel en bladderende verf. Bij een renovatie is het een goed moment om het plafond aan te pakken. In dit artikel vergelijken we de vier meest gekozen plafonds, lees je waar je op let met vocht en verlichting, en wat het ongeveer kost.",
"kort_antwoord": "Voor de meeste badkamers werkt een glad gestuct plafond met vochtwerende of schimmelwerende verf goed, als er ook goed geventileerd wordt. Kunststof panelen en een spanplafond zijn vochtbestendig en snel geplaatst. Een spanplafond kost volgens Werkspot ongeveer " + P_SPANPLAFOND + " per m². Een verlaagd plafond van vochtwerende gipsplaat is handig om leidingen, een ventilatiekanaal of inbouwspots weg te werken.",
"secties": [
("vocht", "Waarom het plafond extra aandacht vraagt",
"""<p>Bij het douchen stijgt warme lucht vol waterdamp op. Die damp slaat neer op het koelste vlak dat hij tegenkomt. Vaak is dat het plafond, zeker bij een buitenmuur of een plafond onder een koud dak. Blijft het plafond lang vochtig, dan krijgt schimmel een kans en gaat gewone muurverf bladderen.</p>
<p>Het plafond oplossen zonder iets aan de ventilatie te doen helpt daarom maar half. Zorg voor een afzuiging die genoeg lucht afvoert en na het douchen nog een tijd blijft draaien. Lees hoe dat werkt in <a href="/kennisbank/badkamer-ventilatie/">badkamer ventilatie</a>, en wat je doet als de schimmel er al zit in <a href="/kennisbank/schimmel-in-badkamer/">schimmel in de badkamer</a>.</p>"""),
("soorten", "Vier plafonds vergeleken",
f"""<div class="tablewrap"><table>
<thead><tr><th></th><th>Stucwerk + vochtwerende verf</th><th>Kunststof panelen</th><th>Spanplafond</th><th>Verlaagd plafond (gipsplaat)</th></tr></thead>
<tbody>
<tr><td>Uitstraling</td><td>Strak en naadloos</td><td>Lijnen of naden zichtbaar</td><td>Strak, mat of glanzend</td><td>Strak na stucen of sauzen</td></tr>
<tr><td>Vochtbestendig</td><td>Goed, met de juiste verf</td><td>Zeer goed</td><td>Zeer goed</td><td>Goed, met vochtwerende plaat</td></tr>
<tr><td>Leidingen wegwerken</td><td>Nee</td><td>Ja, met een regelwerk</td><td>Ja, ruimte erboven</td><td>Ja</td></tr>
<tr><td>Inbouwspots</td><td>Alleen als er ruimte is</td><td>Ja</td><td>Ja, met speciale ringen</td><td>Ja</td></tr>
<tr><td>Zelf te doen?</td><td>Verven wel, stucen lastig</td><td>Ja, voor handige klussers</td><td>Nee, vakwerk</td><td>Deels</td></tr>
<tr><td>Kosten</td><td>Laag tot middel</td><td>Laag tot middel</td><td>{P_SPANPLAFOND} per m² (Werkspot)</td><td>Middel, plus afwerking</td></tr>
</tbody></table></div>
<p>Houten schroten zie je soms in oudere badkamers. In een vochtige badkamer is dat geen goede keus: hout zet uit, kan gaan schimmelen en vraagt veel onderhoud.</p>"""),
("stucwerk", "Stucwerk met vochtwerende verf",
"""<p>Een gestuct plafond geeft het rustigste beeld. Gebruik geen gewone muurverf maar een verf die geschikt is voor vochtige ruimtes, met schimmelwerende toevoegingen. Breng eerst een voorstrijkmiddel aan op nieuw stucwerk, en laat het stucwerk helemaal drogen voor je verft. Op een plafond dat al geschimmeld is, maak je eerst de schimmel schoon en laat je het goed drogen.</p>
<p>Zit het stucwerk los of zit er veel scheurvorming in? Dan is een nieuw plafond eronder vaak handiger dan alles herstellen. Wil je ook de muren verven in plaats van tegelen? Lees dan <a href="/kennisbank/badkamer-schilderen/">badkamer schilderen en tegels verven</a>.</p>"""),
("panelen", "Kunststof plafondpanelen",
"""<p>Kunststof (pvc) panelen worden op een houten of metalen regelwerk geschroefd of geklikt. Ze zijn waterdicht, makkelijk schoon te maken en je kunt er leidingen en spots achter wegwerken. Er zijn panelen met een brede of smalle lijn, en panelen die eruitzien als een glad vlak met nauwelijks naden.</p>
<p>Let op: zorg voor een afwerklijst langs de wanden en laat een kleine ruimte voor uitzetten, zoals de fabrikant voorschrijft. Kies panelen die geschikt zijn voor de badkamer en laat ruimte over het plafond voor de ventilatieleiding.</p>"""),
("spanplafond", "Spanplafond",
f"""<p>Een spanplafond is een folie die onder het bestaande plafond wordt gespannen, op een profiel langs de wanden. De folie is waterdicht en schimmelt niet snel. Het plaatsen gaat vaak in één dag en er komt weinig stof of rommel bij kijken. Volgens Werkspot kost een spanplafond in de badkamer ongeveer {P_SPANPLAFOND} per m², en een eenvoudig pvc-spanplafond ongeveer {P_PVC_SPAN} per m² inclusief plaatsing.</p>
<p>Nadelen: de folie kan scheuren als je er met iets scherps tegenaan komt, en je verliest een paar centimeter hoogte. Spots en de ventilatie-opening moeten van tevoren worden gepland, met speciale ringen in de folie.</p>"""),
("verlaagd", "Verlaagd plafond van gipsplaat",
"""<p>Een verlaagd plafond maak je met een metalen of houten frame en gipsplaten. In de badkamer gebruik je <strong>vochtwerende gipsplaat</strong> (vaak groen van kleur). Daarna wordt het plafond afgewerkt met stuc of saus en vochtwerende verf.</p>
<p>Een verlaagd plafond is vooral handig als je iets wilt wegwerken: een ventilatiekanaal naar de buitenmuur, waterleidingen, of de ruimte voor inbouwspots. In een hoge badkamer, bijvoorbeeld in een oud huis, voelt de ruimte er ook gezelliger door. Houd minstens 2,1 tot 2,3 meter vrije hoogte aan, zeker boven de douche. Laat de dampdichte laag en de ventilatie goed aansluiten, anders kan er vocht boven het plafond komen.</p>"""),
("verlichting", "Verlichting en elektra in het plafond",
f"""<p>Voor lampen in de badkamer gelden zones uit de norm NEN 1010. Boven en direct rond de douche en het bad zijn armaturen nodig met een hogere spatwaterbescherming (IP-waarde) en soms extra veiligheidseisen. Laat de elektra altijd door een installateur aanleggen. Inbouwspots hebben ruimte boven het plafond nodig: plan die voordat het plafond dicht gaat. Een elektrapunt kost volgens de richtprijzen op deze site ongeveer {P_ELEKTRA}. Lees meer in <a href="/kennisbank/badkamerverlichting/">badkamerverlichting</a>.</p>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Welk plafond raadt u aan bij mijn ventilatie en de hoogte van de ruimte?",
"Gebruikt u vochtwerende gipsplaat of panelen die geschikt zijn voor de badkamer?",
"Waar komen de ventilatie-opening en de spots, en welke IP-waarde krijgen de lampen boven de douche?",
"Is de oorzaak van schimmel op het oude plafond opgelost, of verplaatsen we het probleem?",
"Wat is de vrije hoogte na het plaatsen?",
"Wat kost het per m², en is het afwerken (stucen, verven, lijsten) inbegrepen?",
])),
],
"stappen_kop": "Stappenplan nieuw badkamerplafond",
"stappen": [
("Oorzaak van vocht oplossen", "Controleer de afzuiging en pak schimmel eerst aan."),
("Kiezen", "Stucwerk, panelen, spanplafond of verlaagd plafond, afhankelijk van hoogte en leidingen."),
("Elektra en ventilatie plannen", "Spots, ventilatie-opening en kabels vastleggen voor het plafond dicht gaat."),
("Plaatsen", "Met vochtwerende materialen en ruimte voor uitzetten."),
("Afwerken", "Vochtwerende verf of afwerklijsten, en kitten langs de wand waar nodig."),
],
"faq": [
("Welk plafond is het beste voor de badkamer?", "Dat hangt af van je wensen. Een gestuct plafond met vochtwerende verf geeft het rustigste beeld. Kunststof panelen en een spanplafond zijn het meest vochtbestendig. Goede ventilatie is bij elk plafond nodig."),
("Wat kost een spanplafond in de badkamer?", "Volgens Werkspot ongeveer " + P_SPANPLAFOND + " per m². Een eenvoudig pvc-spanplafond kost ongeveer " + P_PVC_SPAN + " per m² inclusief plaatsing."),
("Kan ik gewone muurverf op het badkamerplafond gebruiken?", "Liever niet. Kies verf die geschikt is voor vochtige ruimtes, met schimmelwerende toevoegingen. Gewone muurverf gaat in een badkamer sneller bladderen of schimmelen."),
("Waarom komt er steeds schimmel op mijn badkamerplafond?", "Meestal omdat er te weinig wordt geventileerd en het plafond koud is. Laat de afzuiging na het douchen langer draaien en controleer of die genoeg lucht afvoert."),
("Mag ik spots boven de douche in het plafond?", "Ja, als de lampen de juiste spatwaterbescherming hebben voor die zone volgens NEN 1010. Laat dit door een installateur aanleggen."),
("Is een verlaagd plafond in de badkamer handig?", "Ja, als je leidingen, een ventilatiekanaal of inbouwspots wilt wegwerken. Gebruik vochtwerende gipsplaat en houd genoeg vrije hoogte over."),
],
"bronnen": [WERKSPOT_SPANPLAFOND, WERKSPOT_PLAFOND_VERLAGEN, MC_SCHIMMEL, MC_VENTILEREN, IPLO_VENTILATIE, NEN],
"dienst": "badkamer-renoveren",
"kosten": ["badkamer-opknappen", "badkamer-ventilatie"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/badkamerlampen-kiezen/", "Badkamerlampen kiezen", "IP-waarde, zones en licht dat werkt bij de spiegel.")],
"gerelateerd": ["badkamer-ventilatie", "schimmel-in-badkamer", "badkamerverlichting", "badkamer-zonder-tegels"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-schilderen",
"groep": "Ontwerp en materialen",
"titel": "Badkamer schilderen en tegels verven: zo houdt het",
"seo_titel": "Badkamer schilderen en tegels verven: stappenplan",
"description": "Badkamer opknappen met verf? Lees welke verf je gebruikt voor muren, plafond en tegels, hoe je tegels verft in zes stappen en wat het kost.",
"kort": "Met de juiste verf en een goede voorbereiding geef je muren en tegels voor weinig geld een nieuw uiterlijk.",
"intro": "Een nieuwe badkamer kost al snel duizenden euro's. Zijn je tegels nog heel maar vind je ze lelijk of gedateerd? Dan kan verf een betaalbare tussenstap zijn. Ook muren en plafonds zonder tegels kun je opfrissen. Maar verf in een badkamer moet tegen vocht, warmte en schoonmaakmiddelen kunnen. In dit artikel lees je welke verf je waar gebruikt, hoe je tegels verft en waar je beter iets anders kiest.",
"kort_antwoord": "Gebruik op muren en plafond verf voor vochtige ruimtes met schimmelwerende toevoegingen. Tegels verf je na grondig ontvetten en licht schuren met een hechtprimer en een tweecomponentenlak of speciale tegelverf. In de douche zelf is verf minder duurzaam dan tegels. Tegels laten verven kost volgens Werkspot ongeveer " + P_TEGELVERF + " per m² inclusief arbeid en materiaal.",
"secties": [
("waar", "Waar werkt verf wel, en waar niet?",
"""<div class="tablewrap"><table>
<thead><tr><th>Plek</th><th>Verf geschikt?</th><th>Toelichting</th></tr></thead>
<tbody>
<tr><td>Plafond</td><td>Ja</td><td>Met vochtwerende verf en goede ventilatie</td></tr>
<tr><td>Muur buiten de douche</td><td>Ja</td><td>Kies een afwasbare, vochtbestendige verf</td></tr>
<tr><td>Wandtegels buiten de douche</td><td>Ja</td><td>Met hechtprimer en tegellak; houdt meestal jaren</td></tr>
<tr><td>Wandtegels in de douche</td><td>Beperkt</td><td>Alleen met tweecomponentenlak of epoxy; gaat minder lang mee dan tegels</td></tr>
<tr><td>Vloertegels</td><td>Beperkt</td><td>Alleen met speciale vloercoating; slijt waar je loopt</td></tr>
<tr><td>Douchebak, bad, kit</td><td>Nee</td><td>Verf hecht niet goed op kit en slijt snel in de bak</td></tr>
</tbody></table></div>
<p>Verf is dus vooral geschikt om een badkamer op te frissen die technisch nog in orde is. Laten tegels los, zit er vocht achter of lekt de douche? Dan los je met verf niets op. Kijk dan eerst naar <a href="/kennisbank/lekkage-badkamer/">lekkage in de badkamer</a>.</p>"""),
("verf", "Welke verf gebruik je?",
"""<ul>
<li><strong>Muren en plafond:</strong> een muurverf voor vochtige ruimtes (badkamer- of keukenverf). Die is afwasbaar en heeft vaak schimmelwerende toevoegingen. Een zijdeglans of satijnen afwerking is makkelijker schoon te houden dan mat.</li>
<li><strong>Tegels buiten de natte zone:</strong> een hechtprimer voor gladde ondergronden, daarna een tegelverf of een lak op waterbasis die geschikt is voor tegels.</li>
<li><strong>Tegels in de douche:</strong> een tweecomponentenlak of epoxyverf. Die wordt harder en beter bestand tegen water en schoonmaakmiddel. Werk met goede ventilatie en volg de veiligheidsinstructies op de verpakking.</li>
<li><strong>Houten deur of kozijn:</strong> een lak die tegen vocht kan. Verf de bovenkant en onderkant van de deur ook, zodat het hout geen vocht opneemt.</li>
</ul>
<p>Werkspot noemt tweecomponentenlak of epoxy de beste keus voor tegels die nat worden. Kijk altijd op het blik of de verf geschikt is voor de plek waar je hem gebruikt.</p>"""),
("stappen", "Tegels verven in zes stappen",
"""<ol>
<li><strong>Repareer eerst.</strong> Haal oude kit weg, vervang kapotte voegen en zet losse tegels vast. Verf maakt kapotte delen niet heel.</li>
<li><strong>Ontvet grondig.</strong> Gebruik een sterke ontvetter of een middel speciaal voor tegels. Zeep, kalk en huidvet zorgen ervoor dat verf loslaat. Spoel goed na met schoon water.</li>
<li><strong>Schuur licht</strong> met fijn schuurpapier of een schuurspons, zodat de glans eraf gaat. Maak het stof daarna weg met een vochtige doek.</li>
<li><strong>Plak af</strong> wat niet geverfd moet worden: kranen, douchebak, plinten en randen.</li>
<li><strong>Breng een hechtprimer aan</strong> en laat die drogen volgens de verpakking.</li>
<li><strong>Verf twee lagen</strong> met een kleine roller voor de tegels en een kwast voor de voegen. Laat tussen de lagen goed drogen. Wacht met douchen tot de verf volledig is uitgehard; dat kan een paar dagen tot een week duren.</li>
</ol>
<p>Kit daarna opnieuw af met sanitairkit. Hoe dat strak lukt, lees je in <a href="/kennisbank/badkamer-kitten/">badkamer kitten</a>.</p>"""),
("alternatief", "Verf, tegelstickers, panelen of nieuwe tegels?",
f"""<div class="tablewrap"><table>
<thead><tr><th>Optie</th><th>Richtprijs</th><th>Hoe lang mooi?</th><th>Geschikt in douche?</th></tr></thead>
<tbody>
<tr><td>Tegels verven (laten doen)</td><td>{P_TEGELVERF} per m² (Werkspot)</td><td>Enkele jaren, langer buiten de douche</td><td>Beperkt</td></tr>
<tr><td>Wandpanelen over de tegels</td><td>Afhankelijk van paneel en montage</td><td>Lang, als de naden goed zijn afgekit</td><td>Ja, met panelen voor natte ruimtes</td></tr>
<tr><td>Nieuwe tegels (legloon)</td><td>{P_TEGELWERK} per m² plus tegels</td><td>Tientallen jaren</td><td>Ja</td></tr>
</tbody></table></div>
<p>Wil je tegels helemaal vermijden? In <a href="/kennisbank/badkamer-zonder-tegels/">badkamer zonder tegels</a> vergelijken we microcement, wandpanelen, kalkstuc en glas. Wil je nieuwe tegels over de oude heen leggen? Lees dan <a href="/kennisbank/badkamer-tegelen/">badkamer tegelen</a>.</p>"""),
("kosten", "Wat kost een badkamer schilderen?",
f"""<p>Zelf verven kost vooral materiaal: ontvetter, primer, verf, rollers, tape en schuurpapier. Laat je het doen, dan noemt Werkspot voor tegels verven ongeveer {P_TEGELVERF} per m², inclusief arbeid en materiaal. Voor een gemiddelde badkamer met 20 tot 25 m² wand ben je dan enkele honderden euro's kwijt. Dat is fors minder dan nieuwe tegels, waarvoor je alleen al aan legloon {P_TEGELWERK} per m² betaalt, plus de tegels en het slopen.</p>
<p>Muren en plafond schilderen zonder tegels gaat sneller. Een schilder rekent vaak per m² of per dag. Slimster geeft richtprijzen voor het schilderen van een complete badkamer. Wil je een paar kleine dingen tegelijk opknappen, zoals kit, kranen en verf? Bekijk dan <a href="/kosten/badkamer-opknappen/">kosten badkamer opknappen</a>.</p>"""),
("vakman", "Wat vraag je aan de schilder?",
_vakman([
"Welke primer en welke verf gebruikt u op tegels, en in de douche?",
"Hoe ontvet en schuurt u de tegels? Is dat inbegrepen in de prijs?",
"Vernieuwt u ook de kit, en wanneer: voor of na het verven?",
"Hoe lang moet de verf uitharden voor ik weer kan douchen?",
"Welke garantie geeft u op hechting, en geldt die ook in de douche?",
"Is de prijs per m² of voor de hele badkamer, en zit het afplakken en opruimen erin?",
])),
],
"stappen_kop": "Checklist badkamer verven",
"stappen": [
("Technisch in orde?", "Geen lekkage, losse tegels of vocht achter de wand."),
("Repareren en kit weg", "Voegen en tegels herstellen, oude kit verwijderen."),
("Ontvetten en schuren", "Grondig ontvetten, licht opschuren, stofvrij maken."),
("Primer en twee lagen verf", "Hechtprimer, daarna twee lagen tegellak of 2K-lak."),
("Uitharden en kitten", "Een paar dagen tot een week niet douchen, daarna opnieuw kitten."),
],
"faq": [
("Kun je badkamertegels verven?", "Ja. Ontvet de tegels grondig, schuur ze licht op en gebruik een hechtprimer met tegelverf of een tweecomponentenlak. Buiten de douche houdt dat meestal jaren."),
("Kun je tegels in de douche verven?", "Het kan met een tweecomponentenlak of epoxy, maar het gaat minder lang mee dan tegels. Water, warmte en schoonmaakmiddel slijten de laag."),
("Wat kost tegels verven laten doen?", "Volgens Werkspot ongeveer " + P_TEGELVERF + " per m², inclusief arbeid en materiaal."),
("Welke verf gebruik ik op een badkamerplafond?", "Een muurverf voor vochtige ruimtes met schimmelwerende toevoegingen. Zorg daarnaast voor goede ventilatie."),
("Kan ik over kit heen verven?", "Nee. Verf hecht niet op siliconenkit. Haal de oude kit weg, verf de tegels en kit daarna opnieuw."),
("Hoe lang moet tegelverf drogen voor ik kan douchen?", "Dat verschilt per merk. Vaak is de verf na een dag droog, maar pas na enkele dagen tot een week helemaal uitgehard. Volg de verpakking."),
],
"bronnen": [WERKSPOT_TEGELVERF, WERKSPOT_TEGELVERF_TIPS, GAMMA_TEGELVERF, SLIMSTER_SCHILDEREN, MC_SCHIMMEL, WERKSPOT_TEGEL],
"dienst": "badkamer-onderhoud",
"kosten": ["badkamer-opknappen", "tegelzetter-per-m2"],
"tool": "/tools/stijlkiezer/",
"extra": [],
"gerelateerd": ["badkamer-zonder-tegels", "badkamer-kitten", "badkamer-plafond", "tegels-kiezen"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-tegelen",
"groep": "Ontwerp en materialen",
"titel": "Badkamer tegelen: zelf doen, laten doen of tegels over tegels",
"seo_titel": "Badkamer tegelen: stappen, tegels over tegels en kosten",
"description": "Badkamer tegelen? Lees hoe het werkt, wanneer tegels over tegels kan, welke fouten je voorkomt en wat een tegelzetter per m² kost.",
"kort": "Van ondergrond en waterdichte laag tot voegen: zo pak je het tegelwerk in de badkamer aan, en wanneer tegels over tegels kan.",
"intro": "Tegelwerk bepaalt voor een groot deel hoe je badkamer eruitziet, en hoe goed hij water tegenhoudt. Veel handige klussers tegelen zelf een toilet of een wand. Een complete badkamer met een douche is lastiger, omdat de waterdichte laag en het afschot precies goed moeten zijn. In dit artikel lees je hoe tegelen in de badkamer werkt, wanneer je nieuwe tegels over de oude mag leggen, welke fouten je voorkomt en wat het kost.",
"kort_antwoord": "Tegelen in de badkamer begint met een vlakke, stevige en droge ondergrond. In de douche komt daar eerst een waterdichte laag met kimband op. Daarna lijm je de tegels, laat je ze drogen en voeg je ze. Tegels over tegels kan als de oude tegels vast zitten en de vloer of wand het extra gewicht en de hoogte aankan. Een tegelzetter rekent volgens de richtprijzen op deze site " + P_TEGELWERK + " per m² legloon, plus de tegels.",
"secties": [
("ondergrond", "De ondergrond bepaalt het resultaat",
"""<p>Een tegel is zo goed als de laag eronder. De ondergrond moet aan drie dingen voldoen:</p>
<ul class="checklist">
<li><strong>Vlak:</strong> oneffenheden zie je terug als scheve voegen of tegels die uitsteken. Zeker bij grote tegels moet de wand of vloer heel vlak zijn. Lees meer in <a href="/kennisbank/grote-tegels-badkamer/">grote tegels in de badkamer</a>.</li>
<li><strong>Stevig:</strong> een vloer die doorbuigt, zoals een houten vloer op zolder, laat voegen en tegels scheuren. Die vloer moet eerst verstijfd worden met extra platen of een ontkoppelingsmat.</li>
<li><strong>Droog en schoon:</strong> nieuwe dekvloer of stucwerk moet uitgedroogd zijn. Stof en vet zorgen dat de lijm slecht hecht. Breng een voorstrijkmiddel aan dat past bij de ondergrond.</li>
</ul>
<p>In de douche en rond het bad komt daar een <strong>waterdichte laag</strong> bij, met kimband in de hoeken en manchetten rond leidingen. Tegels en voegen zelf zijn niet waterdicht. Hoe dat werkt, lees je in <a href="/kennisbank/badkamer-waterdicht-maken/">badkamer waterdicht maken</a>.</p>"""),
("stappen", "Tegelen in zeven stappen",
"""<ol>
<li><strong>Plan het tegelpatroon.</strong> Leg de tegels droog uit of teken ze op de wand. Begin in het midden van de wand of bij het meest zichtbare punt, zodat je aan beide kanten even grote snijstukken hebt. Voorkom smalle reepjes van een paar centimeter.</li>
<li><strong>Zet een hulplat of laser uit.</strong> Begin op de wand niet op de vloer, maar op een rechte lat op de hoogte van de tweede rij. De vloer is bijna nooit helemaal waterpas.</li>
<li><strong>Breng tegellijm aan</strong> met een lijmkam met de juiste tandgrootte. Bij grote tegels smeer je ook de achterkant in (dubbel verlijmen), zodat er geen holle plekken overblijven.</li>
<li><strong>Zet de tegels</strong> met kruisjes of een levelsysteem voor gelijke voegen. Controleer elke rij met een waterpas.</li>
<li><strong>Laat de lijm drogen,</strong> vaak een dag. Kijk op de zak voor de droogtijd.</li>
<li><strong>Voeg</strong> met een rubberen voegspaan en was na met een vochtige spons. Kies in de douche een voeg die geschikt is voor natte ruimtes.</li>
<li><strong>Kit</strong> alle binnenhoeken en aansluitingen met sanitair. Daar wordt geen voeg gebruikt, omdat die gaat scheuren. Zie <a href="/kennisbank/badkamer-kitten/">badkamer kitten</a>.</li>
</ol>
<p>Op de vloer van een inloopdouche moet de vloer onder de tegels afschot hebben naar de afvoer. Dat afschot maak je in de dekvloer of met een afschotplaat, niet met extra lijm. Zie <a href="/kennisbank/inloopdouche-zonder-drempel/">inloopdouche zonder drempel</a>.</p>"""),
("over", "Tegels over tegels: wanneer kan het?",
"""<p>Nieuwe tegels op de oude leggen bespaart sloopwerk, stof en tijd. Het kan als:</p>
<ul class="checklist">
<li>alle oude tegels vast zitten. Tik ze af met een houten steel: een hol geluid betekent dat de tegel los zit;</li>
<li>er geen vocht of lekkage achter de tegels zit;</li>
<li>de wand of vloer het extra gewicht en de extra dikte aankan. Een vloer wordt minimaal 1 tot 1,5 cm hoger;</li>
<li>deuren, de douchebak, kranen en het toilet nog passen. Leidingen en inbouwdelen komen soms te diep te liggen.</li>
</ul>
<p>Ontvet de oude tegels grondig, schuur ze op en gebruik een speciale hechtprimer voor gladde ondergronden. In de douche heb je nog steeds een waterdichte laag nodig. Twijfel je of de oude tegels goed genoeg zijn, laat dan een tegelzetter kijken. Bij losse tegels, vocht of een oude douche zonder waterdichte laag is slopen meestal de betere keus.</p>"""),
("vergelijk", "Zelf tegelen of laten doen?",
f"""<div class="tablewrap"><table>
<thead><tr><th></th><th>Zelf tegelen</th><th>Tegelzetter</th></tr></thead>
<tbody>
<tr><td>Kosten</td><td>Tegels, lijm, voeg en gereedschap (tegelsnijder, lijmkam, waterpas)</td><td>{P_TEGELWERK} per m² legloon, plus tegels en hulpmateriaal</td></tr>
<tr><td>Tijd</td><td>Vaak twee tot drie keer zo lang als een vakman</td><td>Kleine badkamer meestal in enkele dagen</td></tr>
<tr><td>Geschikt voor</td><td>Een wand of toilet zonder douche, standaard formaten</td><td>Inloopdouche, grote tegels, natuursteen, visgraat</td></tr>
<tr><td>Risico</td><td>Lekkage door een slechte waterdichte laag; scheve voegen</td><td>Klein, als er garantie op het werk zit</td></tr>
</tbody></table></div>
<p>Een tussenweg is de douchehoek en de vloer laten doen en zelf een wand of het toilet tegelen.</p>"""),
("kosten", "Wat kost een badkamer tegelen?",
f"""<p>Volgens de richtprijzen op deze site (bronnen: Trustoo, Homedeal en Werkspot, inclusief btw):</p>
<ul>
<li>legloon tegelzetter: {P_TEGELWERK} per m²;</li>
<li>tegels: {P_TEGELS} per m² (basis {P_TEGELS_BASIS}, luxe {P_TEGELS_LUXE});</li>
<li>lijm, voeg en kit: ongeveer {P_HULP} per m²;</li>
<li>waterdicht maken van de douchehoek: {P_WATERDICHT}.</li>
</ul>
<p><strong>Rekenvoorbeeld:</strong> een badkamer met 5 m² vloer en 20 m² wandtegels is samen 25 m². Dan kost het legloon ongeveer {_bereik("tegelwerk", 25)}, de tegels {_bereik("tegels", 25)} en het hulpmateriaal ongeveer {eur(RP.RICHTPRIJZEN["tegelwerk_hulpmateriaal"]["laag"] * 25)}. Voor de douchehoek komt er {P_WATERDICHT} bij. Moeten de oude tegels eruit, reken dan ook sloop en afvoer mee: zie <a href="/kosten/badkamer-slopen/">kosten badkamer slopen</a>. Meer voorbeelden staan op <a href="/kosten/tegelzetter-per-m2/">kosten tegelzetter per m²</a>.</p>"""),
("fouten", "Vijf veelgemaakte fouten",
"""<ul>
<li><strong>Geen waterdichte laag in de douche,</strong> of kimband die niet doorloopt in de hoeken.</li>
<li><strong>Te weinig lijm onder grote tegels,</strong> waardoor er holle plekken ontstaan die later breken.</li>
<li><strong>Voegen in de binnenhoeken</strong> in plaats van kit. Die scheuren altijd.</li>
<li><strong>Te snel voegen of douchen,</strong> voordat lijm en voeg droog zijn.</li>
<li><strong>Geen reservetegels bewaren.</strong> Houd een paar tegels over voor reparaties. Dezelfde kleur en partij is later vaak niet meer te krijgen.</li>
</ul>
<p>Hulp bij het kiezen van tegels vind je in <a href="/kennisbank/tegels-kiezen/">tegels kiezen</a>.</p>"""),
("vakman", "Wat vraag je aan de tegelzetter?",
_vakman([
"Is de prijs per m² inclusief lijm, voeg, voorstrijk en kit, of komt dat erbij?",
"Welk waterdicht systeem gebruikt u in de douche, en zit kimband in alle hoeken?",
"Kunnen de nieuwe tegels over de oude, of raadt u slopen aan? Waarom?",
"Hoe maakt u het afschot naar de afvoer?",
"Rekent u een toeslag voor grote tegels, natuursteen of een bijzonder patroon zoals visgraat?",
"Hoeveel snijverlies moet ik bestellen, en wie bestelt de tegels?",
"Welke garantie geeft u op het tegelwerk en de waterdichtheid?",
])),
],
"stappen_kop": "Stappenplan tegelen",
"stappen": [
("Ondergrond controleren", "Vlak, stevig, droog en schoon, en voorstrijken."),
("Waterdicht maken", "Kimband en waterdichte laag in de douche en rond het bad."),
("Indeling bepalen", "Patroon uitleggen en een rechte startlat zetten."),
("Tegels lijmen", "Juiste lijmkam, grote tegels dubbel verlijmen."),
("Voegen en kitten", "Na het drogen voegen, binnenhoeken kitten."),
],
"faq": [
("Kan ik zelf mijn badkamer tegelen?", "Een wand of toilet lukt handige klussers vaak goed. Een douche met afschot en waterdichte laag is lastiger. Laat dat bij twijfel doen, want een fout leidt tot lekkage."),
("Kun je tegels over tegels leggen?", "Ja, als de oude tegels vast zitten, er geen vocht achter zit en de extra dikte en het gewicht geen probleem zijn. Gebruik een hechtprimer en in de douche een nieuwe waterdichte laag."),
("Wat kost een tegelzetter per m²?", "Volgens de richtprijzen op deze site " + P_TEGELWERK + " per m² legloon, inclusief btw. Tegels en hulpmateriaal komen erbij."),
("Hoe lang duurt het tegelen van een badkamer?", "Een tegelzetter doet een kleine badkamer vaak in enkele dagen. Reken met droogtijd voor de lijm en de voeg, en eerder voor het waterdicht maken."),
("Moet ik eerst de wand of de vloer tegelen?", "Vaak worden eerst de wanden gedaan, behalve de onderste rij. Daarna de vloer, en dan de onderste rij van de wand, zodat de wandtegels over de vloertegels vallen. Vakmensen hebben soms een eigen volgorde."),
("Hoeveel tegels moet ik extra bestellen?", "Reken met ongeveer 10 procent extra voor snijverlies en breuk, en meer bij een diagonaal of visgraatpatroon of grote tegels."),
],
"bronnen": [WERKSPOT_TEGEL, TRUSTOO_TEGEL, HOMEDEAL_TEGEL, SLIMSTER_BADKAMER, IPLO_VOCHT],
"dienst": "tegelwerk-badkamer",
"kosten": ["tegelzetter-per-m2", "badkamer-slopen"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Waar let je op bij formaat, antislip en partij?")],
"gerelateerd": ["tegels-kiezen", "badkamer-waterdicht-maken", "grote-tegels-badkamer", "badkamer-kitten"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamervloer",
"groep": "Ontwerp en materialen",
"titel": "Badkamervloer kiezen: tegels, pvc, gietvloer of microcement",
"seo_titel": "Badkamervloer kiezen: tegels, pvc, gietvloer en kosten",
"description": "Welke vloer leg je in de badkamer? Vergelijk tegels, pvc, gietvloer, microcement en natuursteen op water, antislip, vloerverwarming en kosten.",
"kort": "Tegels, pvc, gietvloer, microcement of natuursteen: welke vloer kan tegen water, is veilig en past bij je budget?",
"intro": "Een badkamervloer krijgt het zwaar: water, zeep, natte voeten en schoonmaakmiddel, en vaak ook vloerverwarming eronder. Tegels zijn de bekendste keus, maar pvc, een gietvloer en microcement worden steeds populairder. In dit artikel vergelijken we vijf vloeren, lees je waar je op let met antislip en waterdichtheid, en wat elke vloer ongeveer kost.",
"kort_antwoord": "Keramische tegels zijn de meest gekozen en meest duurzame badkamervloer, ook in de douche. Pvc is warm en betaalbaar (volgens Werkspot " + P_PVC_VLOER + " per m² inclusief leggen), maar alleen geschikt buiten de douche en als de naden waterdicht zijn. Een gietvloer of microcement geeft een naadloze vloer; een gietvloer kost volgens Werkspot " + P_GIETVLOER + " per m². Kies in de natte zone altijd een vloer met voldoende antislip.",
"secties": [
("eisen", "Waar moet een badkamervloer tegen kunnen?",
"""<ul class="checklist">
<li><strong>Water:</strong> de vloer zelf moet tegen water kunnen, en de laag eronder moet waterdicht zijn. Bij een inloopdouche loopt de natte zone door tot in de rest van de badkamer.</li>
<li><strong>Uitglijden:</strong> een natte, gladde vloer is gevaarlijk. Let op de antislipwaarde, zeker in de douche. Bij tegels zie je vaak een R-waarde (bijvoorbeeld R10 of R11) of een klasse voor blote voeten (A, B of C).</li>
<li><strong>Warmte:</strong> past de vloer op vloerverwarming? Tegels en natuursteen geleiden warmte goed. Pvc en houtachtige vloeren hebben een maximale temperatuur.</li>
<li><strong>Onderhoud:</strong> voegen, naden en poreuze materialen vragen meer schoonmaakwerk.</li>
<li><strong>Afschot:</strong> bij een inloopdouche moet de vloer naar de afvoer aflopen. Niet elk materiaal is daarvoor geschikt.</li>
</ul>"""),
("vergelijk", "Vijf badkamervloeren vergeleken",
f"""<div class="tablewrap"><table>
<thead><tr><th>Vloer</th><th>In de douche?</th><th>Vloerverwarming</th><th>Onderhoud</th><th>Richtprijs per m²</th></tr></thead>
<tbody>
<tr><td>Keramische tegels</td><td>Ja</td><td>Zeer goed</td><td>Laag; voegen schoonhouden</td><td>{P_TEGELS} tegels + {P_TEGELWERK} leggen</td></tr>
<tr><td>Pvc (vinyl)</td><td>Nee, alleen buiten de douche</td><td>Ja, tot de maximale temperatuur van het product</td><td>Laag</td><td>{P_PVC_VLOER} incl. leggen (Werkspot)</td></tr>
<tr><td>Gietvloer</td><td>Ja, met geschikt systeem en afschot</td><td>Goed</td><td>Laag; wel krasgevoelig</td><td>{P_GIETVLOER} (Werkspot)</td></tr>
<tr><td>Microcement</td><td>Ja, met waterdichte afwerking</td><td>Goed</td><td>Middel; toplaag soms opnieuw sealen</td><td>Meestal hoger dan tegels</td></tr>
<tr><td>Natuursteen</td><td>Ja, met juiste afwerking</td><td>Zeer goed</td><td>Hoger; impregneren en mild schoonmaken</td><td>Vaak hoger dan keramiek</td></tr>
</tbody></table></div>
<p>De prijzen zijn richtprijzen inclusief btw. Bij elke vloer komen eventueel sloopwerk, egaliseren en de waterdichte laag in de douche erbij.</p>"""),
("tegels", "Keramische tegels",
"""<p>Keramische tegels, vaak porcelanato (doorgekleurd en hard gebakken), zijn de standaard in de Nederlandse badkamer. Ze zijn hard, slijtvast, kunnen tegen water en geleiden de warmte van vloerverwarming goed. Kleine tegels of mozaïek in de douche geven meer grip door de vele voegen en volgen het afschot makkelijker. Grote tegels geven een rustige vloer met weinig voegen, maar vragen een heel vlakke ondergrond. Lees meer in <a href="/kennisbank/tegels-kiezen/">tegels kiezen</a> en <a href="/kennisbank/grote-tegels-badkamer/">grote tegels in de badkamer</a>.</p>"""),
("pvc", "Pvc in de badkamer",
f"""<p>Pvc voelt warmer en zachter aan dan tegels, is stil en betaalbaar. Volgens Werkspot kost een pvc-vloer {P_PVC_VLOER} per m² inclusief leggen. Er zijn twee soorten:</p>
<ul>
<li><strong>Plak-pvc (dryback):</strong> wordt op een egale ondergrond verlijmd. Dat is in de badkamer de betere keus, omdat er geen water onder de planken kan komen.</li>
<li><strong>Klik-pvc:</strong> sneller te leggen, maar water kan via de naden en randen onder de vloer komen. Gebruik het alleen als de fabrikant het uitdrukkelijk voor de badkamer goedkeurt.</li>
</ul>
<p>In de douchehoek zelf is pvc niet geschikt: daar staat te lang water en is afschot nodig. Combineer daarom een betegelde douche of een douchebak met pvc op de rest van de vloer. Kit de randen langs de wanden en rond het toilet af.</p>"""),
("naadloos", "Gietvloer en microcement",
f"""<p>Een <strong>gietvloer</strong> (meestal epoxy of polyurethaan) wordt vloeibaar aangebracht en hardt uit tot één naadloos vlak. Er zijn geen voegen waarin vuil blijft zitten. Volgens Werkspot kost een gietvloer {P_GIETVLOER} per m²; Slimster noemt {eur(60)} tot {eur(150)} per m², afhankelijk van het systeem en de voorbereiding. In de douche moet er een systeem worden gebruikt dat daarvoor geschikt is, met afschot in de ondervloer en een antisliplaag.</p>
<p><strong>Microcement</strong> is een dunne laag van cement en kunststof die op vloer en wand kan. Het geeft een warme, stenen uitstraling zonder naden. Microcement vraagt een goede waterdichte laag en sealer, en een vakman die het systeem kent. Lees meer in <a href="/kennisbank/microcement-badkamer/">microcement in de badkamer</a>.</p>"""),
("vloerverwarming", "Vloerverwarming en de vloer",
f"""<p>Vloerverwarming maakt een badkamer comfortabel. Tegels en natuursteen geven de warmte het beste door. Bij pvc mag de vloer aan de oppervlakte meestal niet te warm worden; kijk naar de maximale temperatuur van het product. Bij een renovatie is elektrische vloerverwarming onder de tegels vaak het eenvoudigst. Die kost volgens de richtprijzen op deze site {P_VV_ELEKTRISCH} voor een badkamer. Lees meer in <a href="/kennisbank/vloerverwarming-of-radiator/">vloerverwarming of radiator</a>.</p>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Is deze vloer geschikt in de douche, en wat is de antislipwaarde?",
"Moet de ondervloer worden geëgaliseerd of verstevigd, en zit dat in de prijs?",
"Hoe wordt de vloer onder de douche waterdicht gemaakt?",
"Past de vloer op mijn vloerverwarming? Wat is de maximale temperatuur?",
"Hoe sluit de vloer aan op de wanden, de deur en het toilet?",
"Hoe onderhoud ik de vloer, en welke schoonmaakmiddelen mag ik gebruiken?",
])),
],
"stappen_kop": "Stappenplan nieuwe badkamervloer",
"stappen": [
("Eisen bepalen", "Inloopdouche of douchebak? Vloerverwarming? Wie gebruikt de badkamer?"),
("Materiaal kiezen", "Vergelijk waterdichtheid, antislip, onderhoud en prijs."),
("Ondergrond voorbereiden", "Oude vloer weg, egaliseren of verstevigen, afschot in de douche."),
("Waterdichte laag", "In de natte zone onder elke vloer een waterdicht systeem."),
("Leggen en afkitten", "Vloer leggen of gieten, randen en aansluitingen afkitten."),
],
"faq": [
("Wat is de beste vloer voor de badkamer?", "Keramische tegels zijn de meest gekozen en meest duurzame vloer, ook in de douche. Pvc, een gietvloer en microcement zijn goede alternatieven, elk met eigen voorwaarden."),
("Kan pvc in de badkamer?", "Ja, buiten de douche. Kies bij voorkeur plak-pvc en kit de randen goed af. In de douchehoek zelf is pvc niet geschikt."),
("Wat kost een pvc-vloer in de badkamer?", "Volgens Werkspot " + P_PVC_VLOER + " per m², inclusief leggen."),
("Wat kost een gietvloer in de badkamer?", "Volgens Werkspot " + P_GIETVLOER + " per m². Slimster noemt " + eur(60) + " tot " + eur(150) + " per m², afhankelijk van systeem en voorbereiding."),
("Welke antislipwaarde heb ik nodig in de douche?", "In de douche kies je een vloer die ook nat stroef is. Bij tegels wordt vaak R10 of R11 of klasse B of C voor blote voeten aangeraden. Vraag het de leverancier."),
("Kan ik over mijn oude badkamertegels een nieuwe vloer leggen?", "Soms. Bij pvc, een gietvloer of nieuwe tegels moet de oude vloer vast, vlak en droog zijn. Let op de extra hoogte bij de deur en de douche."),
],
"bronnen": [WERKSPOT_PVC, WERKSPOT_GIETVLOER, SLIMSTER_GIETVLOER, WERKSPOT_TEGEL, WERKSPOT_VV, MC_VLOERVERWARMING],
"dienst": "tegelwerk-badkamer",
"kosten": ["tegelzetter-per-m2", "vloerverwarming-badkamer"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Formaat, antislip en partij: waar let je op?")],
"gerelateerd": ["tegels-kiezen", "microcement-badkamer", "vloerverwarming-of-radiator", "badkamer-tegelen"],
},
# ---------------------------------------------------------------------------
{
"slug": "maten-badkamer",
"groep": "Ontwerp en materialen",
"titel": "Maten in de badkamer: hoogte van wastafel, toilet, douche en spiegel",
"seo_titel": "Wastafel en toilet hoogte: alle maten in de badkamer",
"description": "Op welke hoogte hang je wastafel, toilet, douchekraan en spiegel? Gangbare maten en vrije ruimte in de badkamer, met tips voor elke lengte.",
"kort": "Wastafel op 85 tot 90 cm, toilet op 40 tot 46 cm en genoeg vrije ruimte ervoor: de maten die je badkamer prettig maken.",
"intro": "Een badkamer kan er mooi uitzien maar toch onhandig zijn: een wastafel waarbij je moet bukken, een toilet dat te laag is of een douche waarin je met je ellebogen tegen de wand stoot. De meeste maten in de badkamer liggen niet vast in de wet. Er zijn wel gangbare hoogtes en vuistregels. In dit artikel zetten we ze op een rij, en lees je hoe je ze aanpast aan je eigen lengte en situatie.",
"kort_antwoord": "Een wastafel hangt meestal met de bovenkant op 85 tot 90 centimeter van de vloer, bij lange mensen hoger. Een staand toilet heeft een pothoogte van ongeveer 40 tot 43 centimeter; een comforttoilet of hangtoilet kan op 45 tot 48 centimeter. Een douche van 90 bij 90 centimeter is prettiger dan 80 bij 80. Houd voor toilet en wastafel genoeg vrije ruimte om te staan en te bukken. Controleer altijd de montagemaat van het product dat je kiest.",
"secties": [
("tabel", "De belangrijkste maten op een rij",
"""<div class="tablewrap"><table>
<thead><tr><th>Onderdeel</th><th>Gangbare maat</th><th>Toelichting</th></tr></thead>
<tbody>
<tr><td>Wastafel (bovenkant)</td><td>85 tot 90 cm</td><td>Geberit noemt 85 tot 95 cm; hoger bij lange gebruikers</td></tr>
<tr><td>Meubel met opzetkom</td><td>Meubel lager, kom bovenop</td><td>Reken met de bovenkant van de kom, niet van het meubel</td></tr>
<tr><td>Staand toilet (pot zonder bril)</td><td>40 tot 43 cm</td><td>De bril komt er nog ongeveer 1,5 cm bovenop</td></tr>
<tr><td>Comfort- of seniorentoilet</td><td>45 tot 48 cm</td><td>Makkelijker opstaan</td></tr>
<tr><td>Hangtoilet</td><td>Naar keuze, vaak 40 tot 46 cm</td><td>Hoogte stel je in bij het inbouwreservoir</td></tr>
<tr><td>Douche</td><td>90 x 90 cm of groter</td><td>80 x 80 cm kan, maar is krap</td></tr>
<tr><td>Spiegel (onderkant)</td><td>Ongeveer 10 tot 20 cm boven de wastafel</td><td>Midden van de spiegel ongeveer op ooghoogte</td></tr>
</tbody></table></div>
<p>Dit zijn gangbare maten en vuistregels uit montagehandleidingen en van fabrikanten, geen wettelijke eisen. Fabrikanten geven per product een montagemaat. Die gaat altijd voor.</p>"""),
("wastafel", "Hoogte van de wastafel",
"""<p>De standaardhoogte van een wastafel ligt met de bovenkant op ongeveer 85 tot 90 centimeter. Voor de meeste volwassenen werkt dat goed. Ben je lang, of is het een badkamer voor twee lange mensen, dan is 90 tot 95 centimeter prettiger. Je hoeft dan minder te bukken bij het tanden poetsen.</p>
<ul>
<li><strong>Kinderen:</strong> hang de wastafel niet lager, maar gebruik een opstapje. Kinderen groeien, de wastafel niet.</li>
<li><strong>Zittend wassen:</strong> voor iemand in een rolstoel of op een douchestoel is een lagere wastafel zonder kast eronder nodig. Lees meer in <a href="/kennisbank/levensloopbestendige-badkamer/">levensloopbestendige badkamer</a>.</li>
<li><strong>Afvoer en kraan:</strong> laat de afvoer en wateraansluiting op de juiste hoogte zetten voordat de wand wordt betegeld. Kies dus eerst je meubel en kraan.</li>
<li><strong>Fontein in het toilet:</strong> die hangt vaak iets hoger of lager, afhankelijk van het model.</li>
</ul>"""),
("toilet", "Hoogte van het toilet",
"""<p>Een staand toilet heeft meestal een pothoogte van 40 tot 43 centimeter zonder bril. Met bril kom je ongeveer 1,5 centimeter hoger uit. Voor ouderen of mensen met knie- of heupklachten zijn er comforttoiletten met een hoogte van 45 tot 48 centimeter.</p>
<p>Bij een <strong>hangtoilet</strong> kies je de hoogte zelf. Het inbouwreservoir heeft een verstelbaar frame; de installateur zet het toilet op de hoogte die jij wilt. Vraag daar dus naar voordat de wand dicht gaat. Een iets hoger hangtoilet, rond 46 centimeter, wordt door veel mensen prettig gevonden. Lees de verschillen in <a href="/kennisbank/hangtoilet-of-staand-toilet/">hangtoilet of staand toilet</a>.</p>
<p>Houd voor het toilet genoeg vrije ruimte: als vuistregel ongeveer 60 tot 70 centimeter vrije ruimte voor de pot en aan elke kant een paar decimeter vanaf de wand. Zo kun je er makkelijk gaan zitten en opstaan.</p>"""),
("douche", "Douche, kraan en douchekop",
"""<ul>
<li><strong>Douchegrootte:</strong> 80 bij 80 centimeter is het minimum dat je vaak tegenkomt, maar krap. Met 90 bij 90 of 90 bij 120 centimeter heb je ruimte om te bewegen. Een inloopdouche zonder bak voelt ruimer door de doorlopende vloer.</li>
<li><strong>Douchekraan:</strong> de thermostaatkraan hangt vaak op ongeveer 100 tot 120 centimeter. Zo kun je erbij zonder te bukken, ook als je zit.</li>
<li><strong>Douchekop en glijstang:</strong> een glijstang laat iedereen de handdouche op eigen hoogte zetten. Een vaste regendouche hangt meestal op ruim 2 meter. Lees meer in <a href="/kennisbank/regendouche/">regendouche</a>.</li>
<li><strong>Nisje:</strong> een nis voor shampoo zit vaak tussen heup- en schouderhoogte, buiten de directe straal van de douchekop.</li>
</ul>
<p>De vloer van een inloopdouche moet afschot hebben naar de afvoer. Hoe dat werkt, lees je in <a href="/kennisbank/inloopdouche-zonder-drempel/">inloopdouche zonder drempel</a>.</p>"""),
("regels", "Wat zegt de wet over maten?",
"""<p>Voor nieuwbouw staan in het Besluit bouwwerken leefomgeving (Bbl) minimumeisen voor de badruimte en de toiletruimte, zoals een minimale vloeroppervlakte en breedte. Het IPLO legt die regels uit. Bij een verbouwing van een bestaande badkamer gelden die eisen niet altijd. Voor de hoogte van een wastafel of toilet staat niets in de wet.</p>
<p>Voor elektra in de badkamer gelden wel regels: de norm NEN 1010 deelt de badkamer in zones in. Daaruit volgt hoe dicht bij de douche of het bad een stopcontact of lamp mag zitten en welke spatwaterbescherming nodig is. Laat dat door een installateur bepalen. Lees meer in <a href="/kennisbank/badkamerverlichting/">badkamerverlichting</a>.</p>"""),
("klein", "Weinig ruimte? Zo kies je",
"""<p>In een kleine badkamer wil je elke centimeter benutten. Kies een smaller of minder diep wastafelmeubel, een hangtoilet (dat steekt minder ver uit) en een draaideur of schuifdeur die geen ruimte in de badkamer kost. Teken de badkamer op schaal of plak de maten met tape op de vloer, zodat je ziet of je er makkelijk langs kunt. Meer tips staan in <a href="/kennisbank/kleine-badkamer-indelen/">kleine badkamer indelen</a> en <a href="/kennisbank/badkamer-ontwerpen/">badkamer ontwerpen</a>.</p>"""),
("vakman", "Wat vraag je aan de installateur?",
_vakman([
"Op welke hoogte zet u de afvoer en de wateraansluiting van de wastafel, en past die bij mijn meubel?",
"Op welke hoogte komt het hangtoilet? Kan het hoger dan standaard?",
"Op welke hoogte komt de douchekraan, en komt er een glijstang?",
"Blijft er genoeg vrije ruimte voor het toilet en de wastafel?",
"Komt er versterking in de wand voor beugels, nu of later?",
"Waar mogen stopcontacten en lampen komen volgens de zones van NEN 1010?",
])),
],
"stappen_kop": "Stappenplan maten bepalen",
"stappen": [
("Gebruikers in beeld", "Hoe lang zijn de gebruikers, en wil je de badkamer later ook nog kunnen gebruiken als je ouder bent?"),
("Sanitair kiezen", "Montagematen van wastafel, toilet en kraan opzoeken."),
("Op schaal tekenen", "Badkamer tekenen of met tape uitzetten, met vrije ruimte."),
("Hoogtes vastleggen", "Hoogtes voor afvoeren, kranen en het inbouwreservoir in de offerte."),
("Controleren voor de wand dicht gaat", "Meten voordat er wordt betegeld."),
],
"faq": [
("Wat is de standaard hoogte van een wastafel?", "Meestal ligt de bovenkant op 85 tot 90 centimeter van de vloer. Voor lange mensen is 90 tot 95 centimeter prettiger."),
("Wat is de standaard hoogte van een toilet?", "Een staand toilet heeft meestal een pothoogte van 40 tot 43 centimeter zonder bril. Een comforttoilet zit op 45 tot 48 centimeter."),
("Op welke hoogte hang je een hangtoilet?", "Dat kies je zelf. Veel mensen kiezen 40 tot 46 centimeter tot de bovenkant van de pot. Spreek het af met de installateur voordat de wand dicht gaat."),
("Hoe groot moet een douche minimaal zijn?", "80 bij 80 centimeter is het minimum dat je vaak tegenkomt, maar 90 bij 90 centimeter of groter is veel prettiger."),
("Op welke hoogte hang je de douchekraan?", "Vaak op ongeveer 100 tot 120 centimeter, zodat je er staand en zittend makkelijk bij kunt."),
("Staan de hoogtes van sanitair in de wet?", "Nee. Het Bbl heeft voor nieuwbouw wel minimummaten voor de badruimte, en NEN 1010 regelt waar elektra mag zitten. Hoogtes van wastafel en toilet zijn een kwestie van comfort."),
],
"bronnen": [GEBERIT_HOOGTE, HORNBACH_WC, BOBEX_TOILET, IPLO_BADRUIMTE, NEN],
"dienst": "badkamer-installeren",
"kosten": ["nieuwe-badkamer", "kleine-badkamer"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/wastafelmeubel-kiezen/", "Wastafelmeubel kiezen", "Breedte, diepte en hoogte van je meubel."),
          ("/badkamerspullen/toilet-kiezen/", "Toilet kiezen", "Staand, hangend en comforthoogte.")],
"gerelateerd": ["kleine-badkamer-indelen", "levensloopbestendige-badkamer", "hangtoilet-of-staand-toilet", "badkamer-ontwerpen"],
},
# EINDE ARTIKELEN4
]


VERDIEPING = {
# ---------------------------------------------------------------------------
"asbest-in-badkamer": {
"secties": [
("regels", "De regels op een rij",
"""<div class="tablewrap"><table>
<thead><tr><th>Regel</th><th>Wat het betekent</th><th>Bron</th></tr></thead>
<tbody>
<tr><td>Verbod sinds 1 juli 1993</td><td>Woningen gebouwd of verbouwd voor 1994 zijn asbestverdacht</td><td>IPLO, Rijksoverheid</td></tr>
<tr><td>Zelf verwijderen: max. 35 m²</td><td>Alleen hechtgebonden, niet gelijmd en heel te verwijderen materiaal, in je eigen woning</td><td>IPLO, spelregels particuliere verwijdering</td></tr>
<tr><td>Sloopmelding</td><td>Vooraf melden bij de gemeente via het Omgevingsloket, ook als je zelf verwijdert</td><td>IPLO, Rijksoverheid</td></tr>
<tr><td>Asbestinventarisatie</td><td>Door een gecertificeerd bureau als een bedrijf het asbest moet verwijderen</td><td>Ondernemersplein</td></tr>
<tr><td>Sanering</td><td>Door een gecertificeerd asbestverwijderingsbedrijf, met een vrijgavemeting na afloop</td><td>Ondernemersplein</td></tr>
</tbody></table></div>
<p>De regels voor zelf verwijderen staan in de spelregels van het IPLO en op de site van de Rijksoverheid. Een gemeente kan extra eisen stellen in de omgevingsregels. Kijk daarom altijd op het Omgevingsloket wat er voor jouw adres geldt.</p>"""),
("zelf-stappen", "Zelf verwijderen: zo doe je het veilig",
"""<p>Mag je volgens de voorwaarden het asbest zelf weghalen, bijvoorbeeld een geschroefde plaat achter het bad? Werk dan zo:</p>
<ol>
<li><strong>Meld de sloop</strong> op tijd vooraf via het Omgevingsloket. Daar zie je ook hoeveel dagen of weken je van tevoren moet melden, en of je gemeente extra eisen stelt.</li>
<li><strong>Bescherm jezelf</strong> met een wegwerpoverall met capuchon, wegwerphandschoenen en een stofmasker met P3-filter.</li>
<li><strong>Maak het materiaal nat</strong> met een plantenspuit, zodat er minder vezels vrijkomen. Niet breken, zagen, boren of schuren.</li>
<li><strong>Schroef de plaat in zijn geheel los</strong> en leg hem direct in dik, doorzichtig plastic.</li>
<li><strong>Verpak luchtdicht</strong> met tape, plak er "Asbest" op en breng het naar de milieustraat. Vraag vooraf of die asbest aanneemt.</li>
<li><strong>Maak de ruimte schoon</strong> met natte doeken. Gebruik geen gewone stofzuiger. Gooi overall, doeken en handschoenen weg bij het asbest.</li>
</ol>
<p>Breekt de plaat toch, of blijkt hij gelijmd? Stop dan en schakel een gecertificeerd bedrijf in.</p>"""),
("kosten", "Wat kost asbestonderzoek en verwijderen?",
f"""<div class="tablewrap"><table>
<thead><tr><th>Onderdeel</th><th>Richtprijs</th><th>Bron</th></tr></thead>
<tbody>
<tr><td>Monster laten testen</td><td>{eur(25)} tot {eur(55)} per extra monster</td><td>Slimster</td></tr>
<tr><td>Asbestinventarisatie van één ruimte, zoals een badkamer</td><td>ongeveer {eur(225)}</td><td>Slimster</td></tr>
<tr><td>Inventarisatie bij een badkamer- of keukenrenovatie</td><td>{eur(350)} tot {eur(500)}</td><td>Homedeal</td></tr>
<tr><td>Complete inventarisatie van een woning</td><td>{eur(200)} tot {eur(700)}</td><td>Werkspot</td></tr>
<tr><td>Verwijderen door een bedrijf</td><td>{eur(20)} tot {eur(30)} per m² (Werkspot); {eur(50)} tot {eur(80)} per m² (Trustoo)</td><td>Werkspot, Trustoo</td></tr>
</tbody></table></div>
<p>Voor een kleine klus zoals een badkamer werken saneerders vaak met een vaste prijs per project, omdat er altijd kosten zijn voor voorbereiding, afscherming en de vrijgavemeting. Vraag daarom een totaalprijs. Daarna volgt het gewone sloopwerk: dat kost volgens de richtprijzen op deze site {P_SLOOP_COMPLEET} voor een complete badkamer tot op de ruwe vloer. Zie <a href="/kosten/badkamer-slopen/">kosten badkamer slopen</a>.</p>"""),
("vakman", "Wat vraag je aan het asbestbedrijf en de aannemer?",
_vakman([
"Bent u gecertificeerd voor asbestinventarisatie of asbestverwijdering? Mag ik het certificaat zien?",
"Is het onderzoek niet-destructief, of moet er worden gebroken om achter tegels en in de vloer te kijken?",
"Is de prijs een totaalprijs, inclusief afvoer en de vrijgavemeting?",
"Wie doet de sloopmelding bij de gemeente: u of ik?",
"Wat gebeurt er als de aannemer tijdens de sloop toch verdacht materiaal vindt? Wat kost meerwerk?",
"Krijg ik het inventarisatierapport en het vrijgavebewijs op papier?",
])),
],
"faq": [
("Wat kost een asbestinventarisatie voor een badkamer?", "Slimster noemt ongeveer " + eur(225) + " voor één ruimte, Homedeal " + eur(350) + " tot " + eur(500) + " bij een badkamer- of keukenrenovatie. Een hele woning kost volgens Werkspot " + eur(200) + " tot " + eur(700) + "."),
("Hoeveel asbest mag ik zelf verwijderen?", "Maximaal 35 m² per woning, en alleen hechtgebonden materiaal dat niet gelijmd is en in zijn geheel los kan. Je meldt het vooraf bij de gemeente."),
("Zitten er asbest in oude badkamertegels?", "In keramische wandtegels zelf zit meestal geen asbest. Wel soms in de lijm of in vinyl vloertegels, vloerzeil, kit of plaatmateriaal achter de tegels. Alleen onderzoek geeft zekerheid."),
("Hoe lang duurt het voordat asbest is verwijderd?", "Reken op enkele weken: inventarisatie, de melding bij de gemeente en de planning van de saneerder. Het verwijderen zelf duurt in een badkamer vaak een of twee dagen."),
],
"bronnen": [RIJK_ASBEST_PART, WERKSPOT_ASBEST_INV, SLIMSTER_ASBEST_INV, HOMEDEAL_ASBEST_INV, WERKSPOT_ASBEST, TRUSTOO_ASBEST, OMGEVINGSLOKET],
"gerelateerd": ["badkamer-huurwoning", "badkamer-tegelen", "badkamervloer"],
},
# ---------------------------------------------------------------------------
"vloerverwarming-of-radiator": {
"vervang": {
"kosten": ("Wat kost het?",
f"""<p>Volgens de richtprijzen op deze site (inclusief btw, bronnen: Werkspot, Slimster en Homedeal):</p>
<div class="tablewrap"><table>
<thead><tr><th>Verwarming</th><th>Richtprijs</th><th>Wat zit erin</th></tr></thead>
<tbody>
<tr><td>Vloerverwarming in de hele badkamer</td><td>{P_VV}</td><td>Elektrisch of aangesloten op cv of warmtepomp, afhankelijk van de situatie</td></tr>
<tr><td>Elektrische vloerverwarming (post)</td><td>{P_VV_ELEKTRISCH}</td><td>Matten onder de tegels, thermostaat en aansluiting</td></tr>
<tr><td>Elektrische vloerverwarming per m²</td><td>{P_VV_M2}</td><td>Inclusief installatie</td></tr>
<tr><td>Elektrapunt of aparte groep</td><td>{P_ELEKTRA}</td><td>Nodig voor elektrische vloerverwarming of een elektrische radiator</td></tr>
</tbody></table></div>
<p><strong>Rekenvoorbeeld:</strong> een badkamer van 5 m² vloer met elektrische matten kost met {P_VV_M2} per m² ongeveer {_bereik("vloerverwarming_m2", 5)} voor de vloerverwarming zelf. Bij warmwatervloerverwarming komen de dekvloer en de aansluiting op de verdeler erbij, maar die is zuiniger in gebruik. Een handdoekradiator kost aanschaf en montage; de prijs hangt sterk af van het model. Meer voorbeelden staan op <a href="/kosten/vloerverwarming-badkamer/">kosten vloerverwarming in de badkamer</a>.</p>"""),
},
"secties": [
("vergelijk", "Vloerverwarming en radiator naast elkaar",
"""<div class="tablewrap"><table>
<thead><tr><th></th><th>Vloerverwarming (water)</th><th>Elektrische vloerverwarming</th><th>Handdoekradiator</th></tr></thead>
<tbody>
<tr><td>Snel warm</td><td>Nee, traag</td><td>Redelijk</td><td>Ja</td></tr>
<tr><td>Warme voeten</td><td>Ja</td><td>Ja</td><td>Nee</td></tr>
<tr><td>Zuinig</td><td>Ja, zeker met een warmtepomp</td><td>Nee, volgens Milieu Centraal</td><td>Op cv: redelijk; elektrisch: minder</td></tr>
<tr><td>Vloer hoger</td><td>Een paar centimeter (dekvloer)</td><td>Nauwelijks</td><td>Nee</td></tr>
<tr><td>Handdoeken drogen</td><td>Nee</td><td>Nee</td><td>Ja</td></tr>
<tr><td>Geschikt bij renovatie</td><td>Ja, als de vloer toch open gaat</td><td>Ja, ook in een kleine badkamer</td><td>Ja, altijd</td></tr>
</tbody></table></div>"""),
("normen", "Temperaturen en vermogen",
"""<ul>
<li><strong>Vloertemperatuur:</strong> een badkamervloer mag volgens Milieu Centraal maximaal 33 °C worden. Warmer is niet prettig voor je voeten en niet goed voor de vloer.</li>
<li><strong>Watertemperatuur:</strong> vloerverwarming werkt meestal met water van rond 40 °C of lager. Daardoor past het goed bij lagetemperatuurverwarming en een warmtepomp.</li>
<li><strong>Kamertemperatuur:</strong> in een badkamer wordt vaak met 22 tot 24 °C gerekend, warmer dan in de woonkamer. Vraag de installateur met welke temperatuur hij rekent.</li>
<li><strong>Warmteberekening:</strong> laat uitrekenen hoeveel vermogen de badkamer nodig heeft. Bij een koude buitenmuur, een raam of een badkamer op zolder is vloerverwarming alleen soms niet genoeg.</li>
<li><strong>Elektra:</strong> voor elektrische vloerverwarming en een elektrische radiator gelden de zones uit NEN 1010. Laat een installateur aansluiten, vaak op een aparte groep met aardlekschakelaar.</li>
</ul>
<p>Bij een vloerverwarmde badkamer past een vloer die warmte goed doorlaat. Lees meer in <a href="/kennisbank/badkamervloer/">badkamervloer kiezen</a>.</p>"""),
("vakman", "Wat vraag je aan de installateur?",
_vakman([
"Maakt u een warmteberekening? Met welke kamertemperatuur rekent u?",
"Is vloerverwarming alleen genoeg, of raadt u een handdoekradiator erbij aan?",
"Kunnen vloer en radiator op dezelfde groep, of is een aparte regeling nodig?",
"Hoeveel hoger wordt de vloer, en hoe lang moet de dekvloer drogen?",
"Is de verwarming geschikt als ik later een warmtepomp neem?",
"Komt er een thermostaat per ruimte, en een timer voor de elektrische delen?",
])),
],
"faq": [
("Wat kost vloerverwarming in de badkamer?", "Volgens de richtprijzen op deze site " + P_VV + " voor de hele badkamer. Elektrische vloerverwarming kost ongeveer " + P_VV_M2 + " per m²."),
("Hoe warm moet een badkamer zijn?", "Vaak wordt met 22 tot 24 °C gerekend. De vloer zelf mag niet warmer worden dan 33 °C."),
("Kan ik een handdoekradiator op de vloerverwarming aansluiten?", "Dat kan, maar de radiator heeft vaak warmer water nodig dan de vloer. Een installateur lost dat op met een aparte groep of een regeling."),
],
"bronnen": [WERKSPOT_VV, RP.BRONNEN["slimster_vv"], RP.BRONNEN["homedeal_vv"], NEN],
"gerelateerd": ["badkamervloer", "badkamer-tegelen", "water-besparen-badkamer"],
},
# ---------------------------------------------------------------------------
"kleine-badkamer-indelen": {
"secties": [
("indelingen", "Drie indelingen vergeleken",
"""<div class="tablewrap"><table>
<thead><tr><th>Indeling</th><th>Geschikt voor</th><th>Voordeel</th><th>Let op</th></tr></thead>
<tbody>
<tr><td>Alles aan één wand</td><td>Smalle, lange badkamer</td><td>Eén leidingwand, goedkoopste aanleg</td><td>Genoeg loopruimte voor het sanitair houden</td></tr>
<tr><td>Douche aan de korte kant, toilet en wastafel tegenover elkaar</td><td>Bijna vierkante badkamer</td><td>Ruime douche, goed bereikbaar</td><td>Leidingen aan twee wanden</td></tr>
<tr><td>Natte cel (hele vloer is douche)</td><td>Heel kleine badkamer</td><td>Voelt groter, geen drempel</td><td>Spatwater op toilet en wastafel; afschot over de hele vloer</td></tr>
</tbody></table></div>
<p>Teken alle drie op schaal voordat je kiest. Op ruitjespapier of met een gratis planner zie je snel waar de deur, de radiator en het raam in de weg zitten.</p>"""),
("maten-tabel", "Maten die je nodig hebt",
"""<ul>
<li><strong>Toilet:</strong> ongeveer 60 tot 70 cm vrije ruimte voor de pot, en aan elke kant ruimte vanaf de wand.</li>
<li><strong>Wastafel:</strong> bovenkant op 85 tot 90 cm; er zijn meubels van 40 cm breed en 25 tot 35 cm diep voor kleine ruimtes.</li>
<li><strong>Douche:</strong> 80 x 80 cm is het minimum; 90 x 90 cm of 90 x 120 cm is prettiger.</li>
<li><strong>Deur:</strong> een draaideur die naar binnen opent kost ruimte. Laat hem naar buiten draaien of kies een schuifdeur.</li>
</ul>
<p>Dit zijn vuistregels, geen wettelijke eisen. Het Bbl stelt voor nieuwbouw wel minimummaten aan een badruimte (zie de IPLO-pagina in de bronnen). Alle hoogtes en maten staan uitgebreider in <a href="/kennisbank/maten-badkamer/">maten in de badkamer</a>.</p>"""),
("kosten", "Wat kost een kleine badkamer?",
f"""<p>Een kleine badkamer is niet veel goedkoper per m² dan een grote: de dure onderdelen, zoals leidingwerk, de douche en het waterdicht maken, heb je toch nodig. Volgens de richtprijzen op deze site (inclusief btw):</p>
<div class="tablewrap"><table>
<thead><tr><th>Onderdeel</th><th>Richtprijs</th></tr></thead>
<tbody>
<tr><td>Slopen tot op de ruwe vloer, incl. afvoer</td><td>{P_SLOOP_COMPLEET}</td></tr>
<tr><td>Leidingwerk op dezelfde plek</td><td>{P_LEIDING}</td></tr>
<tr><td>Tegelwerk, legloon per m²</td><td>{P_TEGELWERK}</td></tr>
<tr><td>Waterdicht maken van de douchehoek</td><td>{P_WATERDICHT}</td></tr>
<tr><td>Douche, basis tot midden</td><td>{P_DOUCHE_BASIS.split(' tot ')[0]} tot {P_DOUCHE_MIDDEN.split(' tot ')[1]}</td></tr>
<tr><td>Wastafelmeubel, basis</td><td>{P_MEUBEL_BASIS}</td></tr>
<tr><td>Toilet verplaatsen (als het moet)</td><td>{P_TOILET_VERPL}</td></tr>
</tbody></table></div>
<p>Laat je het toilet op zijn plek, dan bespaar je het meest. Een compleet rekenvoorbeeld staat op <a href="/kosten/kleine-badkamer/">kosten kleine badkamer</a>, en met de <a href="/tools/badkamercalculator/">badkamercalculator</a> reken je je eigen situatie door.</p>"""),
("vakman", "Wat vraag je aan de badkamerspecialist?",
_vakman([
"Kan het toilet blijven staan, of is verplaatsen nodig voor een betere indeling? Wat kost dat?",
"Is een natte cel zonder douchebak mogelijk boven mijn vloer, met genoeg afschot?",
"Welk wastafelmeubel en welke douchewand passen zonder dat de deur klemt?",
"Waar komt het afzuigventiel, en draait de ventilator na?",
"Kan er een nis of een voorzetwand met bergruimte komen?",
"Kunt u een tekening op schaal maken voordat we beginnen?",
])),
],
"faq": [
("Wat is de kleinste maat voor een douche?", "80 bij 80 centimeter is het minimum dat je vaak tegenkomt. 90 bij 90 centimeter of groter is veel prettiger."),
("Hoeveel ruimte heb je nodig voor een toilet?", "Als vuistregel ongeveer 60 tot 70 centimeter vrije ruimte voor de pot, en aan elke kant ruimte vanaf de wand."),
("Is een kleine badkamer goedkoper?", "Iets goedkoper door minder tegels, maar leidingwerk, douche en waterdicht maken kosten bijna hetzelfde. Per m² is een kleine badkamer vaak duurder."),
],
"bronnen": [RP.BRONNEN["trustoo_badkamer"], RP.BRONNEN["slimster_badkamer"], GEBERIT_HOOGTE, BBL],
"gerelateerd": ["maten-badkamer", "hangtoilet-of-staand-toilet", "badkamer-ontwerpen"],
},
# ---------------------------------------------------------------------------
"inloopdouche-zonder-drempel": {
"secties": [
("normen", "Maten en eisen voor een drempelloze douche",
"""<div class="tablewrap"><table>
<thead><tr><th>Onderdeel</th><th>Gangbare maat of eis</th><th>Waarom</th></tr></thead>
<tbody>
<tr><td>Afschot douchevloer</td><td>Ongeveer 1 tot 2 cm per meter</td><td>Water loopt vanzelf weg zonder dat de vloer scheef voelt</td></tr>
<tr><td>Douchezone</td><td>Minimaal 90 x 90 cm, liever 90 x 120 cm of groter</td><td>Minder spatwater buiten de douche</td></tr>
<tr><td>Inbouwhoogte goot of putje</td><td>Verschilt per product, vaak enkele centimeters onder de afgewerkte vloer</td><td>Ruimte voor de sifon en het verval naar de standleiding</td></tr>
<tr><td>Waterdichte laag</td><td>Over de hele natte zone, met kimband in de hoeken</td><td>Bbl artikel 3.65: een badruimte moet waterdicht zijn</td></tr>
<tr><td>Afvoerleiding</td><td>Volgens NEN 3215, met voldoende verval</td><td>Geen water dat blijft staan, geen rioollucht</td></tr>
</tbody></table></div>
<p>De wettelijke eis uit het Bbl gaat over het resultaat: vloer en wanden in de douchezone moeten waterdicht zijn. Hoe je dat bereikt, staat in de verwerkingsvoorschriften van het afdichtingssysteem en de goot. Vraag de vakman welk systeem hij gebruikt.</p>"""),
("goot-putje", "Douchegoot of putje?",
"""<div class="tablewrap"><table>
<thead><tr><th></th><th>Douchegoot langs de wand</th><th>Putje in het midden</th><th>Putje in de hoek</th></tr></thead>
<tbody>
<tr><td>Afschot</td><td>Eén richting: grote tegels mogelijk</td><td>Vier richtingen: kleinere tegels of insnijden</td><td>Twee richtingen</td></tr>
<tr><td>Uitstraling</td><td>Strak, rooster valt weg langs de wand</td><td>Klassiek</td><td>Onopvallend</td></tr>
<tr><td>Schoonmaken</td><td>Langer rooster; kies een uitneembaar haarzeefje</td><td>Klein en makkelijk</td><td>Klein en makkelijk</td></tr>
<tr><td>Prijs</td><td>Meestal hoger</td><td>Meestal lager</td><td>Meestal lager</td></tr>
</tbody></table></div>
<p>Bij elke afvoer verzamelen zich haar en zeep. Lees hoe je dat oplost in <a href="/kennisbank/afvoer-ontstoppen/">afvoer ontstoppen</a>, en wat je doet als de douche gaat stinken in <a href="/kennisbank/rioollucht-badkamer/">rioollucht in de badkamer</a>. Hulp bij het kiezen vind je bij <a href="/badkamerspullen/douchegoot-kiezen/">douchegoot kiezen</a>.</p>"""),
("kosten", "Wat kost een inloopdouche zonder drempel?",
f"""<p>Volgens de richtprijzen op deze site (inclusief btw):</p>
<div class="tablewrap"><table>
<thead><tr><th>Onderdeel</th><th>Richtprijs</th></tr></thead>
<tbody>
<tr><td>Douche, glazen wand en goot (basis / midden / luxe)</td><td>{P_DOUCHE_BASIS} / {P_DOUCHE_MIDDEN} / {P_DOUCHE_LUXE}</td></tr>
<tr><td>Douche plaatsen en aansluiten</td><td>{P_MONTAGE_DOUCHE}</td></tr>
<tr><td>Waterdicht maken met afschot</td><td>{P_WATERDICHT}</td></tr>
<tr><td>Tegelwerk, legloon per m²</td><td>{P_TEGELWERK}</td></tr>
<tr><td>Afvoer of leidingen verplaatsen</td><td>{P_LEIDING_VERPL}</td></tr>
</tbody></table></div>
<p>Of de afvoer verplaatst moet worden en of de vloer verlaagd of opgehoogd moet worden, bepaalt vaak het verschil tussen een betaalbare en een dure inloopdouche. Meer rekenvoorbeelden staan op <a href="/kosten/inloopdouche/">kosten inloopdouche</a>.</p>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Is er onder mijn vloer genoeg hoogte voor een goot met sifon en verval naar de standleiding?",
"Hoeveel afschot maakt u, en in welke richting?",
"Welk afdichtingssysteem gebruikt u, en hoe sluit het aan op de goot of het putje?",
"Mag ik de waterdichte laag zien voordat de tegels erop gaan?",
"Hoe ver spat het water bij de glazen wand die ik kies? Is een tweede wand of een draaibaar deel nodig?",
"Kan ik het rooster en de stankafsluiter zelf makkelijk schoonmaken?",
])),
],
"faq": [
("Wat kost een inloopdouche zonder drempel?", "Reken volgens de richtprijzen op deze site op " + P_DOUCHE_BASIS + " voor een eenvoudige douche, plus " + P_MONTAGE_DOUCHE + " montage en " + P_WATERDICHT + " voor waterdicht maken en afschot. Tegelwerk en eventueel leidingwerk komen erbij."),
("Hoe diep moet een douchegoot liggen?", "Dat verschilt per goot. Er zijn lage goten voor vloeren met weinig ruimte. Kijk naar de inbouwhoogte van het product en laat de vakman controleren of er genoeg verval naar de standleiding is."),
("Moet de hele badkamervloer waterdicht bij een inloopdouche?", "In ieder geval de hele douchezone. Bij een natte cel, waarbij de douche doorloopt in de rest van de vloer, wordt de hele vloer waterdicht gemaakt."),
],
"bronnen": [IPLO_VOCHT, BBL, RP.BRONNEN["homedeal_douche"], WERKSPOT_TEGEL],
"gerelateerd": ["afvoer-ontstoppen", "rioollucht-badkamer", "maten-badkamer", "badkamer-tegelen"],
},
# ---------------------------------------------------------------------------
"badkamerstijlen": {
"secties": [
("tabel", "De stijlen op een rij",
f"""<div class="tablewrap"><table>
<thead><tr><th>Stijl</th><th>Tegels en wand</th><th>Kranen</th><th>Onderhoud</th><th>Prijsdrijvers</th></tr></thead>
<tbody>
<tr><td>Modern</td><td>Grote tegels, smalle voeg</td><td>Chroom of mat zwart, vaak inbouw</td><td>Laag; zwart toont kalk</td><td>Inbouwkranen, grote formaten, glas zonder profiel</td></tr>
<tr><td>Landelijk</td><td>Houtlook, handgemaakte look</td><td>Mat goud, brons</td><td>Laag met houtlooktegels</td><td>Echt hout, vrijstaand bad</td></tr>
<tr><td>Industrieel</td><td>Betonlook of naadloze wand</td><td>Mat zwart, opbouw</td><td>Middel; kalk zichtbaar</td><td>Microcement, zwarte profielen</td></tr>
<tr><td>Scandinavisch</td><td>Wit of lichtgrijs, licht hout</td><td>Chroom of wit</td><td>Laag; witte voeg verkleurt</td><td>Weinig; een betaalbare stijl</td></tr>
<tr><td>Klassiek</td><td>Metrotegels, patroonvloer</td><td>Kruisgrepen, messing</td><td>Hoger; veel voegen</td><td>Snijwerk, cementtegels, pootjesbad</td></tr>
</tbody></table></div>
<p>Tegels kosten volgens de richtprijzen op deze site {P_TEGELS} per m² (basis {P_TEGELS_BASIS}, luxe {P_TEGELS_LUXE}), en een tegelzetter {P_TEGELWERK} per m² legloon. Een stijl met grote formaten, een patroon of veel snijwerk zit aan de bovenkant van dat legloon.</p>"""),
("praktisch", "Stijl en techniek: waar je op let",
"""<ul>
<li><strong>Antislip:</strong> een matte, stroeve vloertegel past in elke stijl. Kies in de douche een tegel die nat stroef blijft, ook als je een glanzende look wilt. Zie <a href="/kennisbank/badkamervloer/">badkamervloer kiezen</a>.</li>
<li><strong>Kalk:</strong> donkere en matte oppervlakken laten kalk zien. In een gebied met hard water is dat dagelijks werk. Lees <a href="/kennisbank/kalk-en-waterhardheid/">kalk en waterhardheid</a>.</li>
<li><strong>Verlichting:</strong> lampen die bij een stijl passen moeten wel de juiste spatwaterbescherming hebben voor de zone volgens NEN 1010. Zie <a href="/kennisbank/badkamerverlichting/">badkamerverlichting</a>.</li>
<li><strong>Plafond en verf:</strong> een gekleurde muur of plafond kan ook met vochtwerende verf, zie <a href="/kennisbank/badkamer-schilderen/">badkamer schilderen</a> en <a href="/kennisbank/badkamer-plafond/">badkamerplafond</a>.</li>
<li><strong>Ventilatie:</strong> hout, kalkstuc en natuursteen hebben goede ventilatie nodig om mooi te blijven.</li>
</ul>"""),
("vakman", "Wat vraag je aan de vakman?",
_vakman([
"Welke keuzes in deze stijl kosten het meeste werk: tegelformaat, patroon, inbouwkranen of glas zonder profiel?",
"Is mijn wand en vloer vlak genoeg voor grote tegels, of moet er eerst worden geëgaliseerd?",
"Welke voegkleur raadt u aan, en blijft die mooi in de douche?",
"Hoe onderhoud ik mat zwart, messing of natuursteen zonder het te beschadigen?",
"Kunt u voorbeelden laten zien van badkamers in deze stijl die u eerder heeft gemaakt?",
])),
],
"faq": [
("Welke badkamerstijl is het goedkoopst?", "Een eenvoudige Scandinavische of moderne stijl met standaard tegels en opbouwkranen is meestal het goedkoopst. Grote formaten, patronen en inbouwkranen maken het duurder."),
("Welke stijl is het makkelijkst schoon te houden?", "Een stijl met grote tegels, weinig voegen en lichte, glanzende oppervlakken. Mat zwart en donkere tegels laten kalk sneller zien."),
("Hoe vind ik mijn badkamerstijl?", "Verzamel voorbeelden en kijk wat ze gemeen hebben. De stijlkiezer op deze site helpt je met een paar vragen op weg."),
],
"bronnen": [WERKSPOT_TEGEL, SLIMSTER_BADKAMER, NEN, MC_SCHIMMEL],
"gerelateerd": ["badkamervloer", "badkamer-plafond", "badkamer-schilderen", "badkamer-ontwerpen"],
},
# ---------------------------------------------------------------------------
"volgorde-badkamerrenovatie": {
"secties": [
("planning", "Hoe lang duurt elke fase?",
"""<div class="tablewrap"><table>
<thead><tr><th>Fase</th><th>Indicatie</th><th>Wat bepaalt de duur</th></tr></thead>
<tbody>
<tr><td>Voorbereiding en offertes</td><td>Enkele weken tot maanden</td><td>Keuzes, levertijden, asbestonderzoek, VvE-toestemming</td></tr>
<tr><td>Slopen</td><td>1 tot 2 dagen</td><td>Dekvloer eruit of niet, hoeveel tegels</td></tr>
<tr><td>Leidingwerk en elektra</td><td>1 tot 3 dagen</td><td>Verplaatsen of op dezelfde plek</td></tr>
<tr><td>Dekvloer en wanden</td><td>1 tot 2 dagen werk, daarna droogtijd</td><td>Soort dekvloer: snelle dekvloer of cementdekvloer</td></tr>
<tr><td>Waterdicht maken en tegelen</td><td>3 tot 6 dagen</td><td>m² tegels, formaat, patroon, droogtijd van de afdichting</td></tr>
<tr><td>Montage en kitten</td><td>1 tot 3 dagen</td><td>Hoeveel sanitair, inbouwkranen, glazen wand op maat</td></tr>
</tbody></table></div>
<p>Dit zijn indicaties voor een gemiddelde badkamer zonder verrassingen. Een complete badkamer duurt in de praktijk vaak twee tot vier weken. Met de <a href="/tools/renovatieplanner/">renovatieplanner</a> zet je de stappen voor jouw situatie op een rij.</p>"""),
("kosten", "Wat kost elke fase?",
f"""<p>Volgens de richtprijzen op deze site (inclusief btw):</p>
<div class="tablewrap"><table>
<thead><tr><th>Fase</th><th>Richtprijs</th></tr></thead>
<tbody>
<tr><td>Slopen tot op de ruwe vloer, incl. afvoer</td><td>{P_SLOOP_COMPLEET}</td></tr>
<tr><td>Leidingwerk op dezelfde plek</td><td>{P_LEIDING}</td></tr>
<tr><td>Elektra</td><td>{P_ELEKTRA}</td></tr>
<tr><td>Waterdicht maken douchehoek</td><td>{P_WATERDICHT}</td></tr>
<tr><td>Tegelwerk, legloon per m²</td><td>{P_TEGELWERK}</td></tr>
<tr><td>Montage douche / toilet / meubel</td><td>{P_MONTAGE_DOUCHE} / {P_MONTAGE_TOILET} / {P_MONTAGE_MEUBEL}</td></tr>
<tr><td>Kitwerk hele badkamer</td><td>{P_KIT}</td></tr>
</tbody></table></div>
<p>Houd naast deze posten een buffer van ongeveer 10 procent aan voor verrassingen tijdens de sloop. Het totaal voor een complete badkamer vind je op <a href="/kosten/nieuwe-badkamer/">kosten nieuwe badkamer</a>.</p>"""),
("controle", "Momenten om zelf te controleren",
"""<ul class="checklist">
<li><strong>Na het slopen:</strong> is de ondergrond gezond, zijn er rotte balken of oude leidingen? Leg meerwerk schriftelijk vast.</li>
<li><strong>Na het leidingwerk:</strong> maak foto's met een meetlint erbij, zodat je later weet waar leidingen lopen. Vraag of de leidingen zijn afgeperst (op druk getest).</li>
<li><strong>Na het waterdicht maken:</strong> kijk of de kimband in alle hoeken en rond de goot zit, voordat er getegeld wordt.</li>
<li><strong>Voor het voegen:</strong> controleer of het tegelpatroon klopt en of de tegels vlak liggen.</li>
<li><strong>Bij de oplevering:</strong> test alle kranen, de afvoer en de verlichting, en kijk of het water goed wegloopt. Bewaar facturen en garantiebewijzen.</li>
</ul>
<p>Lees ook <a href="/kennisbank/badkamer-tegelen/">badkamer tegelen</a> en <a href="/kennisbank/badkamer-kitten/">badkamer kitten</a>.</p>"""),
("vakman", "Wat vraag je aan de aannemer?",
_vakman([
"Kunt u een planning per dag of per fase geven, met de droogtijden erin?",
"Wie coördineert de loodgieter, elektricien en tegelzetter?",
"Wanneer moeten tegels en sanitair binnen zijn, en wie bestelt ze?",
"Hoe gaat u om met meerwerk? Krijg ik eerst een prijs voordat u het doet?",
"Mag ik de leidingen en de waterdichte laag zien voordat ze dicht gaan?",
"Welke garantie geeft u, en wat staat er in het opleveringsrapport?",
])),
],
"faq": [
("Wat kost een badkamerrenovatie per fase?", "Volgens de richtprijzen op deze site kost slopen " + P_SLOOP_COMPLEET + ", leidingwerk " + P_LEIDING + " en tegelwerk " + P_TEGELWERK + " per m² legloon. Sanitair en montage komen erbij."),
("Wat is de juiste volgorde: eerst tegelen of eerst sanitair?", "Eerst leidingen, dan waterdicht maken en tegelen, en als laatste het sanitair monteren en kitten."),
("Moet ik asbest laten onderzoeken voor de sloop?", "Bij een woning van voor 1994 is dat verstandig, en soms verplicht. Doe het in de voorbereidingsfase, want het kan weken duren."),
],
"bronnen": [RP.BRONNEN["trustoo_badkamer"], SLIMSTER_SLOPEN, WERKSPOT_TEGEL, NEN, IPLO_VOCHT],
"gerelateerd": ["asbest-in-badkamer", "badkamer-tegelen", "badkamer-kitten"],
},
# EINDE VERDIEPING
}
