"""Kostenpagina's voor badkamerwerk: /kosten/ en acht pagina's per klus.

Elke pagina heeft een snel antwoord, een prijstabel per variant, wat de prijs
bepaalt, een rekenvoorbeeld, btw-uitleg, besparingstips, wanneer je een
specialist nodig hebt, een FAQ, een CTA en de bronnen.

Alle bedragen zijn richtprijzen inclusief materiaal en 21% btw, tenzij er
"excl. btw" of "alleen arbeid" bij staat. Ze sluiten aan op data.DIENSTEN
(prijs_van, prijs_tot); waar een pagina afwijkt, staat dat in de tekst en
hieronder bij de bron. Bronnen geraadpleegd in november 2026:

- Homedeal, badkamer renoveren (€3.500 – €15.000, vaak €5.000 – €8.000):
  https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/
- Trustoo, nieuwe badkamer 2026 (€8.500 – €15.000 voor 5 – 10 m²; sloop en afvoer €1.200 – €1.800):
  https://trustoo.nl/kosten/badkamer-renovatie-kosten/
- Slimster, compleet nieuwe badkamer (budget €3.000 – €7.000, midden €7.500 – €11.000, luxe €11.000 – €15.000):
  https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/
- Werkspot, badkamer plaatsen en inloopdouche (inloopdouche €1.500 – €5.000):
  https://www.werkspot.nl/badkamer-plaatsen/prijzen-kosten
- Homedeal en Werkspot, toilet verbouwen (basis €2.500 – €4.000, compleet €4.000 – €6.500, toilet vervangen €300 – €700):
  https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/
  https://www.werkspot.nl/toiletruimte-verbouwen/prijzen-kosten
- Trustoo en Homedeal, tegelzetter (legloon €25 – €40 per m², 8 – 10 m² per dag):
  https://trustoo.nl/kosten/tegelzetter-kosten/
  https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter
- Werkspot, badkamer betegelen (tegels €20 – €60 per m², totaal €25 – €100 per m², voegmiddel €10 – €20 per zak):
  https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten
- Slimster, badkamer slopen (gemiddeld €550, €250 – €850; vloer verwijderen €19 – €40 per m²; €30 – €60 per uur):
  https://slimster.nl/sloopwerk/sloopkosten/badkamer-slopen-kosten/
- Werkspot, badkamer slopen (klein €265 – €400, standaard €400 – €550, groot €550 – €685):
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kosten-badkamer-slopen
- Werkspot, vloerverwarming badkamer (elektrisch €60 – €100 per m², water €50 – €65 per m²,
  verdeler en aansluiting €800 – €2.000, infrezen €40 – €70 per m²):
  https://www.werkspot.nl/verwarming/prijzen-kosten/vloerverwarming-badkamer
- Homedeal, vloerverwarming badkamer (kleine badkamer bijverwarming €850 – €1.600; infrezen €35 – €80 per m²):
  https://www.homedeal.nl/vloerverwarming/vloerverwarming-badkamer-kosten/
- Slimster, vloerverwarming en infrezen (infrezen €35 – €50 per m²):
  https://slimster.nl/vloerverwarming/kosten/
  https://slimster.nl/vloerverwarming/vloerverwarming-infrezen-kosten/
- Werkspot en Slimster, kitwerk badkamer (€6 – €11 per meter, starttarief €100 – €200, hele badkamer €95 – €325):
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kitwerk
  https://slimster.nl/kitwerk/kosten-kitter/badkamer-kitten/
- Homedeal, loodgieter (uurtarief €45 – €85 excl. btw):
  https://www.homedeal.nl/loodgieter/loodgieter-kosten/
- Trustoo, loodgieter (voorrijkosten gemiddeld €20 – €40):
  https://trustoo.nl/kosten/loodgieter-kosten/
- Knab, uurtarief loodgieter zzp 2026 (gemiddeld €57 per uur excl. btw):
  https://bieb.knab.nl/ondernemen/wat-verdient-een-loodgieter-zzp-bekijk-uurtarief-en-winst
- Belastingdienst, 9% btw alleen voor bepaalde werkzaamheden aan woningen ouder dan twee jaar:
  https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/tarieven_en_vrijstellingen/diensten_9_btw/werkzaamheden_aan_woningen/werkzaamheden_aan_woningen
- Rijksoverheid, asbest (verwijderen door gecertificeerd bedrijf, regels voor particulieren):
  https://www.rijksoverheid.nl/onderwerpen/asbest

Voegen vernieuwen per m² (€20 – €40) en de bedragen per post in de
rekenvoorbeelden zijn een eigen inschatting, afgeleid van het legloon en de
uurtarieven hierboven. Dat staat er op de pagina ook bij.
"""

import datetime

from components import (page, title, desc, crumbs, faq_blok, cta_blok, cta_midden,
                        prijs_balken, icon, eur, dienst_icoon)
from data import DIENST_BY_SLUG

JAAR = datetime.date.today().year
MAAND = datetime.date.today().strftime("%m/%Y")

BTW_BRON = ("https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/"
            "tarieven_en_vrijstellingen/diensten_9_btw/werkzaamheden_aan_woningen/werkzaamheden_aan_woningen")

# Bronnen met korte naam, zodat elke pagina dezelfde schrijfwijze gebruikt.
B = {
    "homedeal_badkamer": ("Homedeal, badkamer renoveren kosten", "https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/"),
    "trustoo_badkamer": ("Trustoo, wat kost een nieuwe badkamer", "https://trustoo.nl/kosten/badkamer-renovatie-kosten/"),
    "slimster_badkamer": ("Slimster, compleet nieuwe badkamer kosten", "https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/"),
    "werkspot_badkamer": ("Werkspot, badkamer plaatsen prijzen", "https://www.werkspot.nl/badkamer-plaatsen/prijzen-kosten"),
    "homedeal_toilet": ("Homedeal, toilet verbouwen kosten", "https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/"),
    "werkspot_toilet": ("Werkspot, toiletruimte verbouwen prijzen", "https://www.werkspot.nl/toiletruimte-verbouwen/prijzen-kosten"),
    "trustoo_tegel": ("Trustoo, kosten tegelzetter", "https://trustoo.nl/kosten/tegelzetter-kosten/"),
    "homedeal_tegel": ("Homedeal, kosten tegelzetter", "https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter"),
    "werkspot_tegel": ("Werkspot, badkamer betegelen prijzen", "https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten"),
    "slimster_slopen": ("Slimster, badkamer slopen kosten", "https://slimster.nl/sloopwerk/sloopkosten/badkamer-slopen-kosten/"),
    "werkspot_slopen": ("Werkspot, kosten badkamer slopen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kosten-badkamer-slopen"),
    "werkspot_vv": ("Werkspot, vloerverwarming badkamer prijzen", "https://www.werkspot.nl/verwarming/prijzen-kosten/vloerverwarming-badkamer"),
    "homedeal_vv": ("Homedeal, vloerverwarming badkamer kosten", "https://www.homedeal.nl/vloerverwarming/vloerverwarming-badkamer-kosten/"),
    "slimster_vv": ("Slimster, vloerverwarming kosten", "https://slimster.nl/vloerverwarming/kosten/"),
    "slimster_frezen": ("Slimster, vloerverwarming infrezen kosten", "https://slimster.nl/vloerverwarming/vloerverwarming-infrezen-kosten/"),
    "werkspot_kit": ("Werkspot, kitwerk badkamer prijzen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kitwerk"),
    "slimster_kit": ("Slimster, badkamer kitten kosten", "https://slimster.nl/kitwerk/kosten-kitter/badkamer-kitten/"),
    "homedeal_lood": ("Homedeal, loodgieter kosten", "https://www.homedeal.nl/loodgieter/loodgieter-kosten/"),
    "trustoo_lood": ("Trustoo, uurtarief loodgieter", "https://trustoo.nl/kosten/loodgieter-kosten/"),
    "knab_lood": ("Knab, uurtarief loodgieter zzp 2026", "https://bieb.knab.nl/ondernemen/wat-verdient-een-loodgieter-zzp-bekijk-uurtarief-en-winst"),
    "btw": ("Belastingdienst, 9% btw op werkzaamheden aan woningen", BTW_BRON),
    "asbest": ("Rijksoverheid, asbest", "https://www.rijksoverheid.nl/onderwerpen/asbest"),
}

CALC = "/tools/badkamercalculator/"

# Standaard btw-uitleg; per pagina kan er een zin achter.
BTW_BASIS = (f"Over badkamerwerk betaal je <strong>21% btw</strong>: over het arbeidsloon én over het sanitair, de tegels "
             f"en de andere materialen. Het lage tarief van 9% geldt alleen voor een paar werkzaamheden aan woningen die ouder "
             f"zijn dan twee jaar, zoals stukadoren, verfwerk en het arbeidsloon bij isoleren "
             f"(<a href=\"{BTW_BRON}\" rel=\"nofollow noopener\">Belastingdienst</a>). Tegelwerk, loodgieterswerk en het plaatsen "
             f"van sanitair vallen daar niet onder.")


def tabel(koppen, rijen):
    """Eenvoudige tabel in de huisstijl. Bedragen in een kolom met 'num'."""
    th = "".join(f"<th>{k}</th>" for k in koppen)
    tr = ""
    for r in rijen:
        cellen = ""
        for i, c in enumerate(r):
            klasse = ' class="num"' if (i == 1 and ("€" in str(c) or "%" in str(c))) else ""
            cellen += f"<td{klasse}>{c}</td>"
        tr += f"<tr>{cellen}</tr>"
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ---------------------------------------------------------------------------
# De acht kostenpagina's
# ---------------------------------------------------------------------------
# Velden:
#   slug, kort (kaarttitel), h1, title, description, dienst (slug in data.DIENSTEN),
#   van, tot, eenheid, snel (snel antwoord), varianten [(label, van, tot, uitleg)],
#   varianten_eenheid, varianten_noot, factoren [(kop, tekst)], voorbeeld (intro, rijen, slot),
#   btw_extra, besparen [..], specialist (html), faqs [(v, a)], bronnen [sleutels uit B],
#   verwant [slugs van andere kostenpagina's], kennis [(pad, tekst)]

KOSTEN = [
    # ------------------------------------------------------------------
    {
        "slug": "nieuwe-badkamer",
        "kort": "Nieuwe badkamer",
        "omschrijving": "Wat een complete badkamerrenovatie kost, van basis tot luxe.",
        "h1": f"Wat kost een nieuwe badkamer in {JAAR}?",
        "title": f"Kosten nieuwe badkamer {JAAR}: richtprijzen",
        "description": "Een nieuwe badkamer kost meestal €6.000 tot €18.000, inclusief sloop, tegels, sanitair en 21% btw. Met prijzen voor basis, midden en luxe en een rekenvoorbeeld.",
        "dienst": "badkamer-renoveren",
        "van": 6000, "tot": 18000, "eenheid": "per complete badkamer van 5 tot 9 m², inclusief btw",
        "snel": "De meeste complete badkamers van 5 tot 9 m² kosten <strong>€6.000 tot €18.000</strong>, inclusief sloopwerk, leidingwerk, tegels, sanitair, montage en 21% btw. Een eenvoudige badkamer met basissanitair kan vanaf zo'n €3.500. Verplaats je het toilet, de douche of de afvoer, of kies je luxe sanitair en grote tegels, dan kom je al snel boven de €20.000.",
        "varianten": [
            ("Basis", 3500, 7000, "Kleine badkamer, alles op dezelfde plek, standaard tegels en eenvoudig sanitair."),
            ("Midden", 7000, 12000, "Gewone badkamer met inloopdouche, wastafelmeubel, hangtoilet en tegels uit het middensegment."),
            ("Luxe", 12000, 20000, "Grote tegels, inbouwkranen, regendouche, bad of vloerverwarming, vaak met verplaatste leidingen."),
        ],
        "varianten_eenheid": "Totaalprijs per badkamer, inclusief materiaal en btw",
        "varianten_noot": "Deze indeling volgt Slimster en Homedeal; de bovengrens van luxe is open. Onze algemene richtprijs van €6.000 – €18.000 is het middensegment.",
        "factoren": [
            ("De grootte van de badkamer", "Meer vierkante meters betekent meer tegels, meer legloon en meer kitwerk. Een kleine badkamer is per m² wel duurder, omdat sloop, leidingwerk en sanitair grotendeels vaste kosten zijn."),
            ("Of de indeling verandert", "Blijven toilet, douche en wastafel op hun plek, dan kan het leidingwerk grotendeels blijven. Verplaats je de afvoer van het toilet, dan moet de vloer vaak open en loopt de prijs snel op."),
            ("Het sanitair", "Een wastafelmeubel, toilet, douchewand en kranen kunnen samen €1.500 kosten, maar ook €8.000. Inbouwkranen en een hangtoilet vragen ook meer werk in de muur."),
            ("De tegels", "Tegels kosten grofweg €20 tot €60 per m², en meer voor natuursteen. Grote formaten en mozaïek kosten ook meer legloon."),
            ("De staat van de bestaande badkamer", "Oude leidingen, een slechte vloer of een muur die niet recht is, kosten extra werk. Bij huizen van vóór 1994 kan er asbest zitten, bijvoorbeeld in oude kit, vloerzeil of een plaat achter de tegels."),
            ("Extra's", "Vloerverwarming, een designradiator, extra stopcontacten, verlichting en mechanische ventilatie tellen allemaal op."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 2 bij 3 meter (6 m²) in een tussenwoning. Alles blijft op dezelfde plek. Er komt een inloopdouche, een hangtoilet en een wastafelmeubel. Wanden tot het plafond betegeld: samen met de vloer zo'n 25 m² tegelwerk.",
            [
                ("Slopen en afvoeren van de oude badkamer", "€400 – €700"),
                ("Leidingwerk, afvoer en elektra aanpassen", "€1.000 – €2.500"),
                ("Tegels, 25 m² × €20 – €60", "€500 – €1.500"),
                ("Legloon tegelwerk, 25 m² × €25 – €55", "€625 – €1.375"),
                ("Sanitair: douche, toilet, wastafelmeubel, kranen", "€2.000 – €5.000"),
                ("Montage sanitair", "€800 – €1.500"),
                ("Waterdicht maken, kitwerk en afwerking", "€300 – €600"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€5.625 – €13.175</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld op basis van de bronnen hieronder. Het laat zien waar het geld heen gaat. Je eigen badkamer kan hoger of lager uitkomen.",
        ),
        "btw_extra": "Laat je in dezelfde verbouwing ook het plafond stukadoren of verven, dan kan dat deel onder 9% vallen als de woning ouder is dan twee jaar. Het bedrijf hoort die posten dan apart op de offerte te zetten.",
        "besparen": [
            "Laat toilet, douche en wastafel op hun plek staan. Dat scheelt het meeste geld.",
            "Kies standaardmaten voor tegels, zoals 30 × 60 cm. Grote formaten en mozaïek kosten meer legloon.",
            "Tegel niet alle wanden tot het plafond. Boven de douche wel, op andere wanden kan de bovenkant ook vochtbestendig gestuct of geverfd worden.",
            "Sloop zelf, maar alleen na overleg met het bedrijf en niet als er mogelijk asbest zit.",
            "Vergelijk minimaal drie offertes, en kijk wat er wel en niet in zit. Een stelpost voor sanitair kan een lage prijs mooier laten lijken dan hij is.",
        ],
        "specialist": "Een complete badkamer is werk voor een badkamerspecialist of een aannemer die tegelzetter, loodgieter en elektricien aanstuurt. Doe het zelf alleen als je ervaring hebt met waterdicht maken en leidingwerk: een lekkage door een slecht afgedichte douche ontdek je vaak pas na maanden, als de schade bij de buren of in het plafond zit.",
        "faqs": [
            ("Hoe lang duurt een badkamerrenovatie?", "Voor een gewone badkamer meestal twee tot drie weken, inclusief droogtijd van de vloer en de lijm. Moet er veel verplaatst worden of komt er een nieuwe dekvloer, dan duurt het langer."),
            ("Wat kost een nieuwe badkamer per m²?", "Reken grofweg op €1.000 tot €2.000 per m² voor een complete badkamer. Dat is onze eigen rekensom: €6.000 tot €18.000 gedeeld door 6 tot 9 m². Kleine badkamers zitten per m² aan de bovenkant, omdat het sanitair en het leidingwerk ongeveer hetzelfde kosten als in een grote badkamer."),
            ("Zit het sanitair in de prijs?", "In de richtprijs van €6.000 tot €18.000 wel. In offertes staat het sanitair soms als stelpost: een vast bedrag dat je mag uitgeven. Kies je duurder, dan betaal je het verschil bij."),
            ("Kan ik een badkamer in delen laten doen?", "Dat kan, maar het is meestal duurder. Tegels, leidingen en afvoer hangen met elkaar samen. Wie eerst de tegels laat doen en later de douche verplaatst, betaalt twee keer voor sloop en tegelwerk."),
            ("Is een nieuwe badkamer aftrekbaar of te financieren?", "Een badkamer is niet aftrekbaar van de belasting. Je kunt hem wel meefinancieren bij een hypotheek of verbouwing; vraag daarvoor je hypotheekadviseur."),
        ],
        "bronnen": ["homedeal_badkamer", "trustoo_badkamer", "slimster_badkamer", "werkspot_badkamer", "werkspot_tegel", "btw"],
        "verwant": ["badkamer-slopen", "tegelzetter-per-m2", "inloopdouche"],
        "kennis": [("/kennisbank/volgorde-badkamerrenovatie/", "In welke volgorde gaat een badkamerrenovatie?"),
                   ("/kennisbank/garantie-badkamerrenovatie/", "Welke garantie mag je verwachten?")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "inloopdouche",
        "kort": "Inloopdouche",
        "omschrijving": "Wat een inloopdouche met plaatsing kost, met of zonder drempel.",
        "h1": "Wat kost een inloopdouche met plaatsing?",
        "title": f"Inloopdouche kosten {JAAR}: prijs met plaatsing",
        "description": "Een inloopdouche laten plaatsen kost €1.500 tot €5.000, inclusief btw. Lees wat het verschil maakt: de vloer, de afvoer, de douchewand en het tegelwerk.",
        "dienst": "inloopdouche-plaatsen",
        "van": 1500, "tot": 5000, "eenheid": "per inloopdouche, inclusief plaatsing en btw",
        "snel": "Een inloopdouche laten plaatsen kost meestal <strong>€1.500 tot €5.000</strong>, inclusief plaatsing en 21% btw. Komt hij op de plek van de oude douchebak, dan zit je aan de onderkant. Moet de hele vloer op afschot en opnieuw betegeld worden voor een douche zonder drempel, dan zit je aan de bovenkant of erboven.",
        "varianten": [
            ("Douchebak vervangen door glazen wand", 1500, 2500, "Op de bestaande plek, met een lage douchebak of vloerplaat en een vaste glazen wand."),
            ("Nieuwe tegelvloer met douchegoot", 2500, 4000, "De douchevloer wordt op afschot gelegd en betegeld, met een goot langs de wand."),
            ("Drempelloos, afvoer verplaatst", 3500, 5000, "De vloer moet omlaag of de afvoer wordt verlegd. Vaak samen met nieuw tegelwerk op meer wanden."),
        ],
        "varianten_eenheid": "Per inloopdouche, inclusief materiaal, plaatsing en btw",
        "varianten_noot": "De indeling in drie varianten is een eigen inschatting binnen de bandbreedte van Werkspot (€1.500 – €5.000). Bij luxe glas of een regendouche met thermostaat in de muur kan het hoger uitkomen.",
        "factoren": [
            ("De vloer en het afschot", "Water moet naar de afvoer lopen. Ligt de afvoer niet op de goede plek of moet de vloer omlaag voor een douche zonder drempel, dan is dat het grootste deel van het werk."),
            ("Douchegoot of putje", "Een goot langs de wand maakt het afschot makkelijker en ziet er strak uit, maar kost meer dan een gewoon putje."),
            ("De douchewand", "Een vaste glazen wand van 90 cm is het goedkoopst. Breder glas, een draaideur, zwart profiel of mat glas kosten meer."),
            ("Kraan en douchekop", "Een opbouwthermostaat is eenvoudig. Een inbouwthermostaat met regendouche moet in de muur worden weggewerkt."),
            ("Tegelwerk en waterdicht maken", "Rond de douche moet de vloer en de wand waterdicht worden gemaakt, met een kimband in de hoeken. Dat is niet het duurste deel, maar wel het belangrijkste."),
        ],
        "voorbeeld": (
            "Stel: je vervangt een oude douchebak van 90 × 90 cm door een inloopdouche van 120 × 90 cm met een douchegoot. De douchevloer en de wanden in de douchehoek worden opnieuw betegeld (zo'n 8 m²).",
            [
                ("Oude douchebak en tegels in de douchehoek slopen", "€200 – €400"),
                ("Afvoer aanpassen en douchegoot plaatsen", "€400 – €800"),
                ("Douchevloer op afschot en waterdicht maken", "€300 – €600"),
                ("Tegels en legloon, 8 m²", "€400 – €900"),
                ("Glazen wand 120 cm met montage", "€400 – €900"),
                ("Opbouwthermostaat met handdouche", "€150 – €400"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€1.850 – €4.000</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. Het komt mooi binnen de bandbreedte, maar laat zien dat de vloer en het tegelwerk meer kosten dan de glazen wand.",
        ),
        "btw_extra": "",
        "besparen": [
            "Houd de douche op de plek van de oude douchebak. De afvoer ligt daar al.",
            "Kies een douchegoot of putje van een standaardmaat en een vaste glazen wand zonder deur.",
            "Een opbouwthermostaat is goedkoper dan inbouw en makkelijker te vervangen.",
            "Een kleine drempel van een paar centimeter is vaak veel goedkoper dan een vloer die helemaal omlaag moet.",
        ],
        "specialist": "Een inloopdouche op een bestaande douchebakplek lukt een handige doe-het-zelver soms, maar het waterdicht maken en het afschot luisteren nauw. Bel een badkamerspecialist als de vloer omlaag moet, als de afvoer verlegd wordt of als je in een appartement woont: dan kan lekkage de buren raken.",
        "faqs": [
            ("Kan een inloopdouche zonder drempel overal?", "Niet altijd. Er moet genoeg hoogte zijn voor het afschot en de afvoer. Op een betonvloer moet er soms gefreesd worden, op een houten vloer kan het lastiger zijn. Een specialist kan dat ter plekke beoordelen."),
            ("Hoe groot moet een inloopdouche zijn?", "Minimaal 90 × 120 cm is een prettige maat zonder deur. Bij een kleinere ruimte spat er sneller water buiten de douche."),
            ("Hoe lang duurt het plaatsen?", "Een inloopdouche op de plek van een douchebak is vaak in twee tot vier dagen klaar, inclusief droogtijd. Met een nieuwe vloer duurt het langer."),
            ("Is een douchegoot beter dan een putje?", "Niet beter, wel anders. Met een goot hoeft de vloer maar één kant op af te lopen, zodat je grote tegels kunt gebruiken. Een putje is goedkoper."),
        ],
        "bronnen": ["werkspot_badkamer", "homedeal_badkamer", "werkspot_tegel", "btw"],
        "verwant": ["nieuwe-badkamer", "tegelzetter-per-m2", "kitwerk-voegen"],
        "kennis": [("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel: kan dat bij jou?"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Zo wordt een badkamer waterdicht gemaakt")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "toilet-renoveren",
        "kort": "Toilet renoveren",
        "omschrijving": "Wat een nieuwe toiletruimte kost, of alleen een nieuw toilet.",
        "h1": "Wat kost een toilet renoveren?",
        "title": f"Toilet renoveren kosten {JAAR}: richtprijzen",
        "description": "Een complete toiletruimte renoveren kost €2.500 tot €6.500, inclusief btw. Alleen een nieuw toilet laten plaatsen kost €300 tot €700 aan werk. Met rekenvoorbeeld.",
        "dienst": "toilet-renoveren",
        "van": 2500, "tot": 6500, "eenheid": "per toiletruimte, inclusief btw",
        "snel": "Een complete toiletruimte met nieuwe tegels, toilet en fontein kost meestal <strong>€2.500 tot €6.500</strong>, inclusief 21% btw. Wil je alleen een nieuw staand toilet, dan kost de montage zo'n €300 tot €700, het toilet zelf niet meegerekend.",
        "varianten": [
            ("Alleen toilet vervangen (montage)", 300, 700, "Staand toilet op dezelfde plek, zonder ander werk. Het toilet zelf komt erbij."),
            ("Basis renovatie", 2500, 4000, "Nieuwe tegels, staand of hangend toilet en een eenvoudige fontein."),
            ("Compleet met voorzetwand", 4000, 6500, "Hangtoilet met inbouwreservoir, voorzetwand, nieuwe fontein en tegels tot het plafond."),
        ],
        "varianten_eenheid": "Inclusief materiaal en btw, tenzij anders vermeld",
        "varianten_noot": "Volgens Homedeal en Werkspot. De bovenste rij is alleen het werk.",
        "factoren": [
            ("Staand of hangend toilet", "Een hangtoilet heeft een inbouwreservoir en een voorzetwand nodig. Dat is meer werk, maar het toilet is wel makkelijker schoon te houden."),
            ("Tegels", "Een toiletruimte is klein, maar heeft veel hoeken en randen. Per m² is tegelwerk hier daarom duurder dan in een grote badkamer."),
            ("De fontein", "Een fontein met koudwaterkraan is eenvoudig. Warm water vraagt een extra leiding of een close-in boiler."),
            ("Leidingen en afvoer", "Komt het toilet op een andere plek of moet de afvoer omlaag, dan kost dat extra."),
            ("Elektra en ventilatie", "Een nieuwe lamp of een ventilator op een schakelaar tellen ook mee."),
        ],
        "voorbeeld": (
            "Stel: een toiletruimte van 0,9 × 1,5 meter. Het staande toilet wordt een hangtoilet met voorzetwand, er komt een nieuwe fontein en de wanden worden tot 1,5 meter betegeld (zo'n 9 m² met de vloer).",
            [
                ("Slopen en afvoeren", "€200 – €400"),
                ("Inbouwreservoir, voorzetwand en leidingwerk", "€700 – €1.300"),
                ("Hangtoilet met zitting", "€250 – €800"),
                ("Fontein met kraan", "€150 – €450"),
                ("Tegels en legloon, 9 m²", "€650 – €1.300"),
                ("Montage, kitwerk en afwerking", "€400 – €800"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€2.350 – €5.050</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld op basis van de bronnen hieronder.",
        ),
        "btw_extra": "Laat je het plafond of de wanden boven de tegels stukadoren of verven in een woning die ouder is dan twee jaar, dan kan alleen dat deel onder 9% vallen.",
        "besparen": [
            "Laat het toilet op dezelfde plek. Dan blijft de afvoer gewoon liggen.",
            "Tegel tot halverwege de wand en laat de rest stucen of verven.",
            "Kies een fontein met alleen koud water.",
            "Combineer de toiletruimte met de badkamer als je die ook laat doen. Je betaalt dan één keer voorrijden en opstarten.",
        ],
        "specialist": "Een staand toilet vervangen op dezelfde plek kan een handige doe-het-zelver. Voor een hangtoilet met inbouwreservoir, nieuwe leidingen of nieuw tegelwerk heb je een loodgieter of badkamerspecialist nodig. Een slecht aangesloten reservoir lekt vaak in de muur, waar je het pas laat ziet.",
        "faqs": [
            ("Hoe lang duurt een toiletrenovatie?", "Meestal drie tot vijf werkdagen. Je hebt in die tijd een paar dagen geen toilet; vraag of er een tijdelijke oplossing kan komen als je geen tweede toilet hebt."),
            ("Is een hangtoilet duurder dan een staand toilet?", "Ja, vooral door het inbouwreservoir en de voorzetwand. Reken op een paar honderd tot ruim duizend euro meer dan een staand toilet."),
            ("Kan een hangtoilet aan elke muur?", "Het inbouwframe staat op de vloer en wordt aan de muur vastgezet. Bij een lichte scheidingswand kan het, maar de wand moet stevig genoeg zijn. Een specialist ziet dat snel."),
            ("Wat kost alleen een nieuw toilet plaatsen?", "Het werk kost zo'n €300 tot €700. Daar komt het toilet zelf bij, dat er al is vanaf een paar honderd euro."),
        ],
        "bronnen": ["homedeal_toilet", "werkspot_toilet", "werkspot_tegel", "btw"],
        "verwant": ["uurtarief-loodgieter", "tegelzetter-per-m2", "nieuwe-badkamer"],
        "kennis": [("/badkamerspullen/toilet-kiezen/", "Welk toilet past bij jou?")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "tegelzetter-per-m2",
        "kort": "Tegelzetter per m²",
        "omschrijving": "Wat een tegelzetter per m² rekent voor wand- en vloertegels.",
        "h1": "Wat kost een tegelzetter per m²?",
        "title": f"Tegelzetter kosten per m² {JAAR}: legloon badkamer",
        "description": "Een tegelzetter rekent in de badkamer meestal €25 tot €55 per m² legloon, exclusief tegels. Lees wat het verschil maakt en wat een badkamer betegelen in totaal kost.",
        "dienst": "tegelwerk-badkamer",
        "van": 25, "tot": 55, "eenheid": "per m² legloon, inclusief btw, zonder tegels",
        "snel": "Een tegelzetter rekent in de badkamer meestal <strong>€25 tot €55 per m²</strong> aan legloon. De tegels zelf kosten daarnaast grofweg €20 tot €60 per m². Een tegelzetter legt in een badkamer zo'n 8 tot 10 m² per dag. Voor een badkamer van 6 m² met wanden tot het plafond (zo'n 25 m²) zit je aan legloon op ongeveer €625 tot €1.375.",
        "varianten": [
            ("Wandtegels, standaard formaat", 25, 40, "Bijvoorbeeld 30 × 60 cm, recht gelegd op een vlakke wand."),
            ("Vloertegels", 25, 45, "Inclusief het meenemen van afschot naar de afvoer."),
            ("Grote formaten (60 × 120 cm en groter)", 40, 55, "Zwaar en lastig te verwerken; de ondergrond moet heel vlak zijn."),
            ("Mozaïek en patroon (visgraat, diagonaal)", 45, 80, "Veel snijwerk en veel voegen. Dit valt boven onze algemene richtprijs."),
        ],
        "varianten_eenheid": "Legloon per m², inclusief btw, zonder tegels",
        "varianten_noot": "Trustoo en Homedeal noemen gemiddeld €25 – €40 per m². Onze bovengrens van €55 is voor kleine badkamers en grote formaten. Mozaïek en patronen gaan daar soms overheen; dat is een eigen inschatting.",
        "factoren": [
            ("Het formaat van de tegel", "Standaardformaten gaan het snelst. Heel kleine tegels (mozaïek) en heel grote tegels kosten meer tijd."),
            ("Het legpatroon", "Recht leggen is het goedkoopst. Halfsteens, visgraat of diagonaal geven meer snijwerk en meer afval."),
            ("De ondergrond", "Een wand die niet recht is moet eerst worden uitgevlakt of voorzien van platen. Oude tegels eraf halen kost ook tijd."),
            ("Het aantal hoeken en randen", "Een kleine badkamer met een nis, een voorzetwand en een vensterbank kost per m² meer dan een grote, rechte ruimte."),
            ("Waterdicht maken", "Rond de douche hoort een waterdichte laag met kimband. Sommige tegelzetters rekenen dat apart."),
            ("Afwerking", "Tegelprofielen op de hoeken, een nis in de douche en het voegen tellen mee. Vraag of het voegen in de prijs per m² zit."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 2 × 3 meter (6 m² vloer). De wanden worden tot 2,4 meter betegeld. Na aftrek van de deur en het raam is dat zo'n 19 m² wand. Samen met de vloer is het 25 m² tegelwerk, met tegels van 30 × 60 cm.",
            [
                ("Legloon wand en vloer, 25 m² × €25 – €55", "€625 – €1.375"),
                ("Tegels, 25 m² + 10% snijverlies × €20 – €60", "€550 – €1.650"),
                ("Lijm, voegsel en kimband", "€150 – €350"),
                ("Waterdicht maken van de douchehoek", "€150 – €350"),
                ("Tegelprofielen en kitwerk", "€100 – €250"),
                ("<strong>Totaal tegelwerk, inclusief btw</strong>", "<strong>€1.575 – €3.975</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. Een tegelzetter is met 25 m² zo'n drie werkdagen bezig, plus droogtijd.",
        ),
        "btw_extra": "Een tegelzetter rekent dus altijd 21%, ook als de woning ouder is dan twee jaar. Let erop dat een prijs per m² soms exclusief btw wordt genoemd.",
        "besparen": [
            "Kies een standaardformaat en leg recht of halfsteens.",
            "Haal zelf de oude tegels van de muur, als de ondergrond daarna nog goed is. Overleg dat eerst.",
            "Koop 10% extra tegels, niet meer. Te veel tegels kun je vaak niet terugbrengen.",
            "Laat de tegelzetter de tegels adviseren of zelf inkopen: dan is hij ook verantwoordelijk als ze niet goed te verwerken zijn.",
        ],
        "specialist": "Een stukje wand betegelen kun je zelf, maar in de badkamer luistert het nauw. Een tegelvloer moet op afschot liggen en de douchehoek moet waterdicht zijn. Een fout zie je pas als het water de verkeerde kant op loopt of er vocht achter de tegels komt. Laat de douche en de vloer daarom door een tegelzetter doen.",
        "faqs": [
            ("Hoeveel m² legt een tegelzetter per dag?", "In een badkamer zo'n 8 tot 10 m². Bij grote, rechte vlakken meer, bij mozaïek of veel snijwerk minder."),
            ("Rekent een tegelzetter per m² of per uur?", "De meeste tegelzetters rekenen per m². Klein werk of reparaties gaan vaak per uur. Vraag altijd wat er in de prijs per m² zit: voorbereiden, voegen en kitten zijn niet altijd inbegrepen."),
            ("Kun je over oude tegels heen tegelen?", "Soms wel, als de oude tegels vast zitten en de vloer of wand daarna niet te hoog of te zwaar wordt. Het scheelt sloopwerk, maar de deur en de afvoer moeten wel passen."),
            ("Waarom is tegelwerk in een kleine badkamer duurder per m²?", "Omdat er per m² meer hoeken, randen en snijwerk zijn. De opstartkosten zijn ook hetzelfde."),
        ],
        "bronnen": ["trustoo_tegel", "homedeal_tegel", "werkspot_tegel", "btw"],
        "verwant": ["nieuwe-badkamer", "kitwerk-voegen", "inloopdouche"],
        "kennis": [("/kennisbank/tegels-kiezen/", "Welke tegels passen in de badkamer?"),
                   ("/badkamerspullen/badkamertegels-kopen/", "Waar let je op bij het kopen van tegels?")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "badkamer-slopen",
        "kort": "Badkamer slopen",
        "omschrijving": "Wat het slopen en afvoeren van een oude badkamer kost.",
        "h1": "Wat kost een badkamer slopen?",
        "title": f"Badkamer slopen kosten {JAAR}: prijs en afvoer",
        "description": "Een badkamer laten slopen kost meestal €250 tot €850, inclusief btw. Afvoer van puin en asbest kosten soms extra. Lees wat het verschil maakt en wanneer je zelf kunt slopen.",
        "dienst": "badkamer-renoveren",
        "van": 250, "tot": 850, "eenheid": "per badkamer, inclusief btw",
        "snel": "Een badkamer laten slopen kost meestal <strong>€250 tot €850</strong>, inclusief 21% btw. Gemiddeld is het zo'n €550. Komen het afvoeren van puin, een container en het verwijderen van een dekvloer erbij, dan kan het oplopen tot €1.200 à €1.800. Zit er asbest in, dan moet een gecertificeerd bedrijf dat eerst weghalen.",
        "varianten": [
            ("Kleine badkamer (tot ca. 4 m²)", 265, 400, "Douche, toilet, wastafel en tegels eruit."),
            ("Standaard badkamer (5 – 8 m²)", 400, 550, "Ook bad of douchebak en meer tegelwerk."),
            ("Grote badkamer (vanaf 9 m²)", 550, 685, "Meer tegels en vaak een bad en een tweede wastafel."),
            ("Inclusief afvoer en dekvloer", 1200, 1800, "Als de vloer tot op het beton open moet en alles wordt afgevoerd."),
        ],
        "varianten_eenheid": "Per badkamer, inclusief btw",
        "varianten_noot": "De eerste drie rijen volgen Werkspot. De onderste rij volgt Trustoo, dat een ruimere opdracht meeneemt. Daardoor lopen de bronnen zo ver uiteen.",
        "factoren": [
            ("Hoeveel er weg moet", "Alleen sanitair eruit is snel gebeurd. Tegels van de muur hakken, een tegelvloer en een dekvloer verwijderen kost veel meer tijd. Slimster noemt voor de vloer €19 tot €40 per m²."),
            ("Afvoer van puin", "Een badkamer levert al snel een paar kuub puin op. Een container of afvoer naar de milieustraat kost extra, als het niet in de prijs zit."),
            ("Bereikbaarheid", "Een badkamer op de derde verdieping zonder lift betekent alles naar beneden sjouwen."),
            ("Asbest", "In woningen van vóór 1994 kan asbest zitten in oude kit, lijm, vloerzeil, een plaat achter de tegels of een afvoer. Dat moet eerst onderzocht en door een gecertificeerd bedrijf verwijderd worden."),
            ("Leidingen afdoppen", "Water, afvoer en stroom moeten veilig worden afgesloten. Dat doet meestal de loodgieter die daarna ook de nieuwe leidingen legt."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 6 m² op de eerste verdieping. Douchebak, toilet, wastafel en alle wand- en vloertegels gaan eruit. De dekvloer blijft liggen.",
            [
                ("Sanitair demonteren en leidingen afdoppen", "€100 – €200"),
                ("Wandtegels verwijderen (ca. 19 m²)", "€150 – €300"),
                ("Vloertegels verwijderen, 6 m² × €19 – €40", "€115 – €240"),
                ("Puin afvoeren", "€100 – €300"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€465 – €1.040</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. De sloper rekent €30 tot €60 per uur; een badkamer van deze maat is meestal in één tot twee dagen leeg.",
        ),
        "btw_extra": "Sloopwerk dat bij een badkamerrenovatie hoort, valt onder 21% btw.",
        "besparen": [
            "Laat het slopen meenemen in de offerte van de badkamerspecialist. Dan is ook duidelijk wie verantwoordelijk is voor de leidingen.",
            "Sloop zelf het sanitair en de tegels, als het bedrijf dat goed vindt en er zeker geen asbest is.",
            "Laat de dekvloer liggen als die nog goed en vlak is.",
            "Vraag of je puin zelf mag wegbrengen naar de milieustraat. Bij veel gemeenten kan dat in beperkte hoeveelheden.",
        ],
        "specialist": "Zelf slopen kan, maar sluit eerst het water af en laat de leidingen door een loodgieter afdoppen. Twijfel je over asbest, stop dan en laat het onderzoeken. Asbest mag je als particulier maar in beperkte gevallen zelf verwijderen; de regels staan bij de <a href=\"https://www.rijksoverheid.nl/onderwerpen/asbest\" rel=\"nofollow noopener\">Rijksoverheid</a>. Meer uitleg vind je in <a href=\"/kennisbank/asbest-in-badkamer/\">asbest in de badkamer</a>.",
        "faqs": [
            ("Hoe lang duurt het slopen van een badkamer?", "Een gewone badkamer is meestal in één tot twee dagen leeg. Moet de dekvloer eruit, dan duurt het langer."),
            ("Mag ik zelf mijn badkamer slopen?", "Ja, maar overleg het met het bedrijf dat de nieuwe badkamer maakt. Sommige bedrijven geven minder garantie als ze niet zelf hebben gesloopt, omdat ze niet weten wat er onder de tegels zat."),
            ("Hoe weet ik of er asbest in mijn badkamer zit?", "Zeker weten doe je het alleen met een onderzoek door een gecertificeerd bedrijf. Bij woningen van vóór 1994 is de kans groter. Twijfel je, laat het dan eerst onderzoeken voordat je gaat slopen."),
            ("Zit het afvoeren van puin in de prijs?", "Niet altijd. Vraag het na. Een offerte zonder afvoer lijkt goedkoper, maar dan blijf je met een paar kuub puin zitten."),
        ],
        "bronnen": ["slimster_slopen", "werkspot_slopen", "trustoo_badkamer", "asbest", "btw"],
        "verwant": ["nieuwe-badkamer", "uurtarief-loodgieter", "tegelzetter-per-m2"],
        "kennis": [("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer: wat nu?"),
                   ("/kennisbank/volgorde-badkamerrenovatie/", "De volgorde van een badkamerrenovatie")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "vloerverwarming-badkamer",
        "kort": "Vloerverwarming badkamer",
        "omschrijving": "Wat elektrische of watergedragen vloerverwarming in de badkamer kost.",
        "h1": "Wat kost vloerverwarming in de badkamer?",
        "title": f"Vloerverwarming badkamer kosten {JAAR}: per m²",
        "description": "Vloerverwarming in de badkamer kost €50 tot €120 per m², inclusief installatie en btw. Lees het verschil tussen elektrisch en watergedragen, en wat het stroomverbruik is.",
        "dienst": "badkamer-renoveren",
        "van": 50, "tot": 120, "eenheid": "per m², inclusief installatie en btw",
        "snel": "Vloerverwarming in de badkamer kost meestal <strong>€50 tot €120 per m²</strong>, inclusief installatie en 21% btw. Voor een kleine badkamer met elektrische matten als bijverwarming zit je op zo'n €850 tot €1.600. Watergedragen vloerverwarming is per m² niet duurder, maar daar komt de aansluiting op de cv-ketel of warmtepomp bij: €800 tot €2.000.",
        "varianten": [
            ("Elektrische matten", 60, 100, "Dunne matten onder de tegels. Snel aan te leggen, wel stroomverbruik."),
            ("Watergedragen, nieuwe vloer", 50, 65, "Leidingen in de dekvloer, aangesloten op de cv of warmtepomp."),
            ("Watergedragen, infrezen in bestaande vloer", 35, 80, "Sleuven in de bestaande dekvloer. Daarna komen er nieuwe tegels op."),
        ],
        "varianten_eenheid": "Per m², inclusief installatie en btw",
        "varianten_noot": "Volgens Werkspot (elektrisch en watergedragen) en Homedeal en Slimster (infrezen). Bij watergedragen komt de verdeler en de aansluiting erbij, €800 – €2.000 volgens Werkspot.",
        "factoren": [
            ("Elektrisch of watergedragen", "Elektrisch is goedkoop aan te leggen, maar verbruikt stroom. Watergedragen is zuiniger in gebruik, maar de aansluiting op de verwarming kost meer."),
            ("Bijverwarming of hoofdverwarming", "Wil je alleen warme voeten, dan is een kleinere mat genoeg. Moet de vloer de hele badkamer verwarmen, dan heb je meer vermogen of meer leidingen nodig, en vaak nog een radiator voor de handdoeken."),
            ("De bestaande vloer", "Bij een nieuwe dekvloer kunnen de leidingen erin. In een bestaande vloer moet er gefreesd worden, of komt er een dunne mat op."),
            ("Isolatie", "Ligt de badkamer boven een koude ruimte, dan gaat er warmte naar beneden. Een isolatielaag kost extra, maar scheelt in het verbruik."),
            ("Thermostaat", "Een eigen thermostaat met klok voor de badkamer zorgt dat de vloer alleen warm is als je hem gebruikt."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 6 m², waarvan 4 m² vrije vloer (onder de douche, het toilet en het meubel komt geen verwarming). Je kiest elektrische matten als bijverwarming bij een nieuwe tegelvloer.",
            [
                ("Elektrische mat, 4 m² × €60 – €100 met installatie", "€240 – €400"),
                ("Thermostaat met klok en vloervoeler", "€100 – €250"),
                ("Aansluiting door elektricien, eigen groep", "€150 – €400"),
                ("Isolatieplaten onder de mat", "€60 – €150"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€550 – €1.200</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. <strong>Stroomverbruik:</strong> een mat van 4 m² heeft zo'n 400 tot 600 watt. Staat hij gemiddeld twee uur per dag aan, dan is dat 290 tot 440 kWh per jaar. Bij €0,25 tot €0,35 per kWh is dat ongeveer €75 tot €155 per jaar. Met een klokthermostaat kun je dat beperken.",
        ),
        "btw_extra": "Vloerverwarming valt niet onder isolatie, dus ook het arbeidsloon kent 21% btw.",
        "besparen": [
            "Leg verwarming alleen in de vrije vloer, niet onder de douche, het bad of het meubel.",
            "Kies een klokthermostaat, zodat de vloer alleen warm is als je de badkamer gebruikt.",
            "Leg vloerverwarming aan tijdens een badkamerrenovatie. Achteraf moeten de tegels er weer uit.",
            "Heb je een warmtepomp of lage-temperatuurverwarming, vraag dan of watergedragen vloerverwarming kan. Dat is zuiniger dan elektrisch.",
        ],
        "specialist": "Elektrische vloerverwarming hoort op een eigen groep met aardlekschakelaar. Laat de aansluiting door een erkende elektricien doen. Watergedragen vloerverwarming laat je door een installateur aanleggen, omdat die op je cv-ketel of warmtepomp wordt aangesloten en ingeregeld.",
        "faqs": [
            ("Is elektrische vloerverwarming duur in gebruik?", "Als bijverwarming in een kleine badkamer valt het mee: zo'n €75 tot €155 per jaar bij twee uur per dag, volgens onze rekensom. Gebruik je hem als hoofdverwarming en staat hij veel aan, dan loopt het op."),
            ("Kan vloerverwarming onder elke tegel?", "Onder keramische tegels en natuursteen werkt het goed, want die geven warmte goed door. Vraag bij de tegelwinkel of de tegel en de lijm geschikt zijn."),
            ("Is vloerverwarming genoeg als enige verwarming in de badkamer?", "In een goed geïsoleerd huis soms wel. Vaak wordt er nog een handdoekradiator bij geplaatst, voor droge handdoeken en extra warmte."),
            ("Hoe lang duurt het aanleggen?", "Elektrische matten liggen vaak in een halve dag. Daarna moeten de tegels erop. Watergedragen vloerverwarming in een nieuwe dekvloer vraagt weken droogtijd voordat er getegeld kan worden."),
        ],
        "bronnen": ["werkspot_vv", "homedeal_vv", "slimster_vv", "slimster_frezen", "btw"],
        "verwant": ["nieuwe-badkamer", "tegelzetter-per-m2", "uurtarief-loodgieter"],
        "kennis": [("/kennisbank/badkamer-ventilatie/", "Ventilatie in de badkamer")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "kitwerk-voegen",
        "kort": "Kitwerk en voegen",
        "omschrijving": "Wat nieuwe kit en vernieuwde voegen in de badkamer kosten.",
        "h1": "Wat kost kitwerk en voegen vernieuwen in de badkamer?",
        "title": f"Kitwerk en voegen badkamer kosten {JAAR}",
        "description": "Nieuwe kit in de badkamer kost €6 tot €11 per meter, plus vaak een starttarief. Een hele badkamer opnieuw afkitten kost €95 tot €325. Ook de prijs van voegen vernieuwen.",
        "dienst": "badkamer-onderhoud",
        "van": 6, "tot": 11, "eenheid": "per meter kitwerk, inclusief btw",
        "snel": "Oude kit verwijderen en nieuwe kit aanbrengen kost <strong>€6 tot €11 per meter</strong>, inclusief 21% btw. Veel vakmensen rekenen daarnaast een starttarief van €100 tot €200. Een hele badkamer opnieuw afkitten kost daarom meestal <strong>€95 tot €325</strong>. Voegen vernieuwen kost grofweg €20 tot €40 per m².",
        "varianten": [
            ("Kitwerk per meter", 6, 11, "Oude kit eruit, schoonmaken en nieuwe sanitairkit erin."),
            ("Hele badkamer afkitten", 95, 325, "Douche, bad, wastafel, toilet en vloerranden samen."),
            ("Starttarief (los)", 100, 200, "Voor voorrijden en opstarten, bij kleine klussen."),
            ("Voegen vernieuwen per m²", 20, 40, "Oude voeg eruit frezen en nieuwe voeg aanbrengen. Eigen inschatting."),
        ],
        "balken": False,
        "varianten_eenheid": "Inclusief materiaal en btw",
        "varianten_noot": "Kitwerk volgens Werkspot en Slimster. Voegen vernieuwen is een eigen inschatting op basis van het legloon van tegelzetters (€20 – €40 per m² volgens Werkspot).",
        "factoren": [
            ("Hoeveel meter kit", "Een douchehoek heeft zo'n 5 tot 8 meter kit, een hele badkamer al snel 15 tot 30 meter."),
            ("De oude kit", "Schimmelige of harde kit moet helemaal weg en de rand moet schoon en droog zijn. Dat kost meer tijd dan de nieuwe kit erin spuiten."),
            ("Schimmel en vocht", "Zit er vocht achter de kit of de tegels, dan is nieuwe kit maar een pleister. Dan moet eerst de oorzaak worden gevonden."),
            ("Voegen of kit", "Voegen zitten tussen de tegels, kit zit in de hoeken en langs het sanitair. Voegen vernieuwen is veel meer werk dan kitten."),
            ("Starttarief", "Bij een kleine klus is het starttarief vaak het grootste deel van de rekening. Combineer het daarom met ander klein werk."),
        ],
        "voorbeeld": (
            "Stel: de kit in je badkamer is zwart van de schimmel. Er moet nieuwe kit in de douchehoek, langs het bad, rond de wastafel en het toilet en langs de vloer: samen zo'n 20 meter.",
            [
                ("Oude kit verwijderen en nieuwe aanbrengen, 20 m × €6 – €11", "€120 – €220"),
                ("Starttarief (als de vakman het rekent)", "€0 – €200"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€120 – €420</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. Komen er ook nieuwe voegen in de douche, reken dan op €20 tot €40 per m² extra. Voor 6 m² douchewand is dat €120 tot €240.",
        ),
        "btw_extra": "",
        "besparen": [
            "Vervang kit op tijd. Een losse of gescheurde kitrand laat water door, en vochtschade is veel duurder dan nieuwe kit.",
            "Laat alle kit in één keer doen, zodat je het starttarief maar één keer betaalt.",
            "Droog de douche na het douchen met een trekker. Dan blijft kit veel langer schoon.",
            "Is alleen de bovenkant van de voeg vies, probeer dan eerst een voegenreiniger. Vernieuwen is pas nodig als de voeg zacht of kapot is.",
        ],
        "specialist": "Kitten kun je zelf leren, maar een strakke, waterdichte kitrand is lastiger dan het lijkt. Bel een vakman als de kit steeds weer loslaat, als er zwarte plekken achter de kit blijven of als je vocht ziet in de muur of het plafond eronder. Dan is er vaak meer aan de hand dan alleen oude kit.",
        "faqs": [
            ("Hoe vaak moet kit in de badkamer vervangen worden?", "Gemiddeld om de vijf tot tien jaar, of eerder als er schimmel in zit die niet meer weggaat, of als de kit loslaat of scheurt."),
            ("Kan ik nieuwe kit over oude kit spuiten?", "Nee. Nieuwe kit hecht slecht op oude kit, en schimmel groeit gewoon door. De oude kit moet er helemaal uit."),
            ("Hoe lang moet nieuwe kit drogen?", "Meestal 24 uur voordat je weer kunt douchen. Kijk op de koker; sommige kit heeft langer nodig."),
            ("Wat is het verschil tussen voegen en kit?", "Voegen zijn hard en zitten tussen de tegels. Kit is flexibel en zit in de hoeken en langs het sanitair, waar dingen een beetje kunnen bewegen."),
        ],
        "bronnen": ["werkspot_kit", "slimster_kit", "werkspot_tegel", "btw"],
        "verwant": ["tegelzetter-per-m2", "inloopdouche", "uurtarief-loodgieter"],
        "kennis": [("/kennisbank/badkamer-waterdicht-maken/", "Een badkamer waterdicht maken"),
                   ("/kennisbank/badkamer-ventilatie/", "Goede ventilatie tegen schimmel")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "uurtarief-loodgieter",
        "kort": "Uurtarief loodgieter",
        "omschrijving": "Wat een loodgieter per uur rekent, met voorrijkosten en spoedtoeslag.",
        "h1": f"Wat is het uurtarief van een loodgieter in {JAAR}?",
        "title": f"Uurtarief loodgieter {JAAR}: prijs per uur",
        "description": "Een loodgieter rekent meestal €45 tot €85 per uur excl. btw, plus voorrijkosten van €20 tot €50. Lees wat spoed, avond en weekend kosten en wat kleine klussen kosten.",
        "dienst": "badkamer-installeren",
        "van": 45, "tot": 85, "eenheid": "per uur, exclusief btw",
        "snel": "Een loodgieter rekent meestal <strong>€45 tot €85 per uur, exclusief btw</strong>. Met 21% btw is dat €54 tot €103 per uur. Daar komen vaak voorrijkosten van €20 tot €50 bij. Voor spoed, 's avonds of in het weekend betaal je meer: vaak 50 tot 100% toeslag op het uurtarief.",
        "varianten": [
            ("Uurtarief, werkdag", 45, 85, "Gewoon werk overdag, op afspraak."),
            ("Voorrijkosten", 20, 50, "Per bezoek. Soms vervalt dit bij een grotere klus."),
            ("Uurtarief, avond en weekend", 70, 170, "Met 50 tot 100% toeslag. Eigen inschatting op basis van het gewone uurtarief."),
            ("Spoed voorrijden", 50, 150, "Bij spoed, buiten werktijd, komt er een hoger voorrijtarief."),
        ],
        "balken": False,
        "varianten_eenheid": "Exclusief btw",
        "varianten_noot": "Uurtarief volgens Homedeal (€45 – €85); het Knab Uurtarievenboekje noemt een gemiddelde van €57 voor zzp-loodgieters. Voorrijkosten volgens Trustoo en Homedeal. De toeslagen verschillen sterk per bedrijf.",
        "factoren": [
            ("Wanneer je belt", "Overdag op afspraak is het goedkoopst. Spoed, avond, nacht en weekend kosten een flinke toeslag."),
            ("Waar je woont", "In de Randstad liggen de tarieven vaak hoger dan in de rest van het land. Woont de loodgieter verder weg, dan zijn de voorrijkosten hoger."),
            ("Zzp'er of bedrijf", "Een zelfstandige is vaak goedkoper per uur dan een groter installatiebedrijf met personeel en een bus vol voorraad."),
            ("Vaste prijs of uurtarief", "Kleine klussen, zoals een toilet vervangen, gaan vaak voor een vaste prijs. Bij lekkage zoeken weet niemand vooraf hoe lang het duurt; dat gaat per uur."),
            ("Materiaal", "Kranen, sifons, leidingen en koppelingen komen bovenop het uurtarief. Vraag vooraf of de loodgieter dat bij zich heeft."),
        ],
        "voorbeeld": (
            "Stel: je wilt een nieuwe wastafelkraan en een nieuwe sifon laten plaatsen. De loodgieter komt op een doordeweekse dag en is anderhalf uur bezig. Je kraan heb je zelf gekocht.",
            [
                ("Arbeid, 1,5 uur × €45 – €85", "€67,50 – €127,50"),
                ("Voorrijkosten", "€20 – €50"),
                ("Sifon en koppelingen", "€15 – €40"),
                ("Subtotaal exclusief btw", "€102,50 – €217,50"),
                ("21% btw", "€21,53 – €45,68"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€124,03 – €263,18</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. Veel loodgieters rekenen per half uur of hebben een minimumtarief van een uur.",
        ),
        "btw_extra": "Let op: veel loodgieters noemen hun uurtarief exclusief btw. Vergelijk daarom altijd prijzen met of zonder btw, en niet door elkaar.",
        "besparen": [
            "Bel niet met spoed als het kan wachten. Sluit bij een lekkage eerst de hoofdkraan af, dan kan de loodgieter vaak de volgende werkdag komen.",
            "Bundel klussen: laat de lekkende kraan, het toilet en de sifon in één bezoek doen.",
            "Vraag bij grotere klussen om een vaste prijs in plaats van een uurtarief.",
            "Vraag vooraf naar voorrijkosten, minimumtarief en of het uurtarief met of zonder btw is.",
        ],
        "specialist": "Een sifon of een douchekop vervangen kun je vaak zelf. Bel een loodgieter bij lekkages in de muur of de vloer, bij werk aan de waterleiding of de afvoer, en als er iets aan de cv-ketel of warmwatervoorziening moet. Werk aan gasleidingen mag je nooit zelf doen.",
        "faqs": [
            ("Is het uurtarief van een loodgieter inclusief btw?", "Meestal niet. De meeste loodgieters noemen hun tarief exclusief btw. Met 21% btw wordt €60 per uur dus €72,60."),
            ("Wat zijn normale voorrijkosten?", "Zo'n €20 tot €50 per bezoek. Sommige loodgieters rekenen geen voorrijkosten als de klus boven een bepaald bedrag uitkomt."),
            ("Wat kost een spoedloodgieter?", "Bij spoed buiten werktijd betaal je vaak 50 tot 100% meer per uur en een hoger voorrijtarief. Vraag altijd aan de telefoon wat het gaat kosten."),
            ("Rekent een loodgieter per uur of per klus?", "Allebei komt voor. Kleine, voorspelbare klussen gaan vaak voor een vaste prijs, zoeken naar lekkage en onvoorspelbaar werk per uur."),
        ],
        "bronnen": ["homedeal_lood", "trustoo_lood", "knab_lood", "btw"],
        "verwant": ["toilet-renoveren", "kitwerk-voegen", "badkamer-slopen"],
        "kennis": [("/badkamerspullen/kranen-kiezen/", "Waar let je op bij een nieuwe kraan?")],
    },
]

KOSTEN_BY_SLUG = {k["slug"]: k for k in KOSTEN}

LINKS = [("/kosten/", "Kosten badkamerwerk", "Richtprijzen voor een nieuwe badkamer, inloopdouche, tegelwerk en meer.")] + [
    (f"/kosten/{k['slug']}/", k["kort"], k["omschrijving"]) for k in KOSTEN
]


# ---------------------------------------------------------------------------
# Opmaak
# ---------------------------------------------------------------------------

STYLE = """<style>
.kc-snel{display:flex;gap:16px;align-items:flex-start;background:var(--bg-soft);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:var(--radius);padding:18px 20px;margin:18px 0 8px}
.kc-snel .kc-ico{flex:0 0 auto;color:var(--navy);margin-top:2px}
.kc-snel p{margin:0}
.kc-snel .kc-kop{font-size:.78rem;font-weight:750;letter-spacing:.04em;text-transform:uppercase;color:var(--accent-dark);margin-bottom:4px}
.kc-snel .kc-bedrag{font-size:1.5rem;font-weight:800;color:var(--ink);line-height:1.2;margin-bottom:6px}
.kc-snel .kc-bedrag span{font-size:.95rem;font-weight:600;color:var(--muted)}
.kc-factoren{list-style:none;padding:0;margin:0}
.kc-factoren li{padding:12px 0;border-bottom:1px solid var(--line)}
.kc-factoren li:last-child{border-bottom:0}
.kc-factoren strong{display:block;color:var(--ink)}
.kc-tips{list-style:none;padding:0}
.kc-tips li{position:relative;padding-left:30px}
.kc-tips li svg{position:absolute;left:0;top:2px;color:var(--green)}
.kc-links{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin:14px 0}
.kc-links a{display:block;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;background:#fff;font-weight:650}
.kc-links a small{display:block;font-weight:400;color:var(--muted);margin-top:2px}
.kc-bronnen{font-size:.88rem;color:var(--muted)}
.kc-bronnen li{margin-bottom:.3em}
.kc-grid .card h3{display:flex;gap:10px;align-items:center}
.kc-grid .card .price{margin-top:4px}
@media (max-width:600px){.kc-snel{flex-direction:column;gap:8px}.kc-snel .kc-bedrag{font-size:1.3rem}}
</style>"""


def bedrag(van, tot, eenheid=""):
    """Bedrag van–tot; kleine bedragen (zoals per meter) zonder afronding."""
    return f"{eur(van)} – {eur(tot)}"


def bronnen_html(sleutels):
    li = "".join(f'<li><a href="{B[s][1]}" rel="nofollow noopener">{B[s][0]}</a></li>' for s in sleutels)
    return (f'<h2>Bronnen</h2><p class="kc-bronnen">De richtprijzen op deze pagina zijn gebaseerd op deze bronnen, '
            f'geraadpleegd in november {JAAR}. Rekenvoorbeelden en bedragen die we zelf hebben afgeleid, staan als eigen '
            f'inschatting aangegeven.</p><ul class="kc-bronnen">{li}</ul>')


def kosten_body(k):
    d = DIENST_BY_SLUG[k["dienst"]]
    cr, cr_ld = crumbs([("Home", "/"), ("Kosten", "/kosten/"), (k["kort"], None)])

    # Balken alleen als alle varianten dezelfde eenheid hebben; anders alleen de tabel met een noot.
    if k.get("balken", True):
        varianten = prijs_balken([(lbl, v, t) for lbl, v, t, _ in k["varianten"]], k["varianten_eenheid"], k["varianten_noot"])
    else:
        varianten = f'<p><small>{k["varianten_eenheid"]}. {k["varianten_noot"]}</small></p>'
    var_tabel = tabel(["Variant", "Richtprijs", "Wat je krijgt"],
                      [(f"<strong>{lbl}</strong>", bedrag(v, t), uitleg) for lbl, v, t, uitleg in k["varianten"]])
    factoren = "".join(f"<li><strong>{kop}</strong>{tekst}</li>" for kop, tekst in k["factoren"])
    intro, rijen, slot = k["voorbeeld"]
    voorbeeld = tabel(["Post", "Richtprijs"], rijen)
    tips = "".join(f"<li>{icon('check', 20)}{t}</li>" for t in k["besparen"])
    verwant = "".join(
        f'<a href="/kosten/{s}/">{KOSTEN_BY_SLUG[s]["kort"]}<small>{KOSTEN_BY_SLUG[s]["omschrijving"]}</small></a>'
        for s in k["verwant"])
    kennis = "".join(f'<li><a href="{p}">{t}</a></li>' for p, t in k["kennis"])
    faq_html, faq_ld = faq_blok(k["faqs"], f"Veelgestelde vragen over {k['kort'].lower()}")

    eenheid_kort = k["eenheid"]
    body = f"""{STYLE}{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Richtprijzen bijgewerkt {MAAND}</span>
  <h1>{k['h1']}</h1>
  <div class="kc-snel" role="note" aria-label="Snel antwoord">
    <span class="kc-ico">{dienst_icoon(k['dienst'], 40)}</span>
    <div>
      <p class="kc-kop">Snel antwoord</p>
      <p class="kc-bedrag">{bedrag(k['van'], k['tot'])} <span>{eenheid_kort}</span></p>
      <p>{k['snel']}</p>
    </div>
  </div>
  <p><small>Alle bedragen zijn richtprijzen. Je echte prijs hangt af van jouw badkamer en hoor je pas na een bezoek van een specialist.</small></p>

  <h2>Prijzen per variant</h2>
  {varianten}
  {var_tabel}

  <h2>Wat bepaalt de prijs?</h2>
  <ul class="kc-factoren">{factoren}</ul>

  <h2>Rekenvoorbeeld</h2>
  <p>{intro}</p>
  {voorbeeld}
  <p>{slot}</p>
  <p>Wil je een schatting voor je eigen badkamer? Gebruik de <a href="{CALC}">badkamercalculator</a>.</p>

  {cta_midden("Weet wat het bij jou kost", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit jouw regio en vergelijk ze rustig.")}

  <h2>Welke btw betaal je?</h2>
  <p>{BTW_BASIS} {k['btw_extra']}</p>

  <h2>Tips om te besparen</h2>
  <ul class="kc-tips">{tips}</ul>

  <h2>Wanneer heb je een specialist nodig?</h2>
  <p>{k['specialist']}</p>
  <p>Meer over dit werk lees je op de pagina <a href="/diensten/{d['slug']}/">{d['naam'].lower()}</a>. Heb je al een offerte? Leg hem naast de <a href="/tools/offertechecker/">offertechecker</a>.</p>

  <h2>Verder lezen</h2>
  <ul>{kennis}<li><a href="/prijzen/">Alle badkamerprijzen op een rij</a></li></ul>
  <div class="kc-links">{verwant}</div>

  {bronnen_html(k['bronnen'])}
</div></section>
{faq_html}
{cta_blok(f"Offertes voor {k['kort'].lower()} vergelijken?", "Vul in een minuut het formulier in. Je krijgt vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio. Je kiest zelf of je met een van hen verder gaat.")}"""
    return body, [cr_ld, faq_ld]


def overzicht_body():
    cr, cr_ld = crumbs([("Home", "/"), ("Kosten", None)])
    kaarten = "".join(
        f'<a class="card reveal" href="/kosten/{k["slug"]}/">'
        f'<h3>{dienst_icoon(k["dienst"], 28)}{k["kort"]}</h3>'
        f'<p>{k["omschrijving"]}</p>'
        f'<div class="price">{bedrag(k["van"], k["tot"])} {k["eenheid"]}</div>'
        f'<p style="margin:10px 0 0"><span class="go">Bekijk de kosten →</span></p></a>'
        for k in KOSTEN)
    rijen = [(f'<a href="/kosten/{k["slug"]}/">{k["kort"]}</a>', bedrag(k["van"], k["tot"]), k["eenheid"]) for k in KOSTEN]
    faqs = [
        ("Waar komen deze prijzen vandaan?", "Uit openbare prijsoverzichten van onder meer Homedeal, Werkspot, Trustoo en Slimster, geraadpleegd in november " + str(JAAR) + ". Op elke pagina staan de bronnen. Rekenvoorbeelden zijn een eigen inschatting op basis van die bronnen."),
        ("Zijn de prijzen inclusief btw?", "Ja, tenzij er 'excl. btw' bij staat. Dat doen we bij het uurtarief van een loodgieter, omdat loodgieters hun tarief bijna altijd zonder btw noemen. Over badkamerwerk betaal je 21% btw."),
        ("Waarom zijn de bandbreedtes zo breed?", "Omdat geen badkamer hetzelfde is. De grootte, de staat van de oude badkamer, of de indeling verandert en welk sanitair je kiest, maken samen duizenden euro's verschil."),
        ("Hoe kom ik aan een echte prijs?", "Door een specialist naar je badkamer te laten kijken. Via Top Badkamers vraag je gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Wij voeren het werk zelf niet uit."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over badkamerkosten")
    body = f"""{STYLE}{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Richtprijzen {JAAR}</span>
  <h1>Kosten van badkamerwerk</h1>
  <p class="lead">Wat kost een nieuwe badkamer, een inloopdouche of een tegelzetter? Per klus vind je hier de richtprijs, een rekenvoorbeeld, de btw en tips om te besparen. Zo zie je snel of een offerte in de buurt zit.</p>
  <p>Alle bedragen zijn richtprijzen inclusief materiaal en 21% btw, tenzij er iets anders bij staat. Ze komen uit openbare prijsoverzichten; de bronnen staan op elke pagina. Wil je een schatting voor je eigen badkamer, gebruik dan de <a href="{CALC}">badkamercalculator</a>.</p>
</div></section>
<section class="section-sm"><div class="wrap">
  <h2>Kies een klus</h2>
  <div class="grid g3 kc-grid">{kaarten}</div>
</div></section>
<section class="section-sm"><div class="wrap narrow prose">
  <h2>Alle bandbreedtes op een rij</h2>
  {tabel(["Klus", "Richtprijs", "Eenheid"], rijen)}
  <p><small>Richtprijzen, geen offerte. Je echte prijs hangt af van jouw situatie. Een overzicht per dienst vind je op <a href="/prijzen/">badkamerprijzen</a>.</small></p>

  <h2>Hoe gebruik je deze richtprijzen?</h2>
  <p>Een richtprijs gaat uit van een gewone klus. Je betaalt meer als er leidingen verplaatst moeten worden, als de vloer omlaag of omhoog moet, als er asbest zit of als je kiest voor luxe sanitair en grote tegels. Gebruik de bedragen dus om te zien of een offerte in de buurt zit, niet als vaste prijs.</p>
  <p>Leg offertes naast elkaar en kijk per offerte wat er in zit: sloopwerk, afvoer van puin, leidingwerk, elektra, waterdicht maken, sanitair (of een stelpost), btw en garantie. Ontbreekt er iets, dan is dat geen detail maar een latere meerprijs. De <a href="/tools/offertechecker/">offertechecker</a> helpt je daarbij.</p>
</div></section>
{faq_html}
{cta_blok("Benieuwd wat jouw badkamer kost?", "Richtprijzen zijn een begin. Een echte prijs krijg je als een specialist naar jouw badkamer kijkt. Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio.")}"""
    return body, [cr_ld, faq_ld]


def build(write):
    body, ld = overzicht_body()
    write("/kosten/", page(
        title(f"Kosten badkamerwerk {JAAR}: alle richtprijzen"),
        desc(f"Wat kost een nieuwe badkamer, inloopdouche, toilet of tegelzetter in {JAAR}?",
             "Richtprijzen per klus met rekenvoorbeeld, btw-uitleg en tips om te besparen.",
             limit=175),
        "/kosten/", body, ld), prio=0.8, freq="monthly")
    for k in KOSTEN:
        body, ld = kosten_body(k)
        write(f"/kosten/{k['slug']}/", page(title(k["title"]), k["description"],
                                             f"/kosten/{k['slug']}/", body, ld), prio=0.7, freq="monthly")
