# -*- coding: utf-8 -*-
"""Kostenpagina's ronde 5: verdieping van de vijf belangrijkste kostenpagina's en nieuwe pagina's.

Dit bestand exporteert:
- EXTRA: per slug extra velden voor een bestaande kostenpagina. badkamer_kosten.py voegt ze toe met
  k.update(...); "faqs_extra" wordt achter de bestaande FAQ gezet. Nieuwe velden (gerenderd door
  badkamer_kosten.extra_secties):
    opbouw_intro, opbouw   prijsopbouw per post (sloop, leidingwerk, tegelwerk, sanitair, afwerking),
                           elke rij met bron; een rij met een sleutel uit richtprijzen.py haalt bedrag,
                           eenheid en bron daaruit;
    voorbeeld_titel        kopje boven het bestaande rekenvoorbeeld;
    voorbeelden            extra rekenvoorbeelden [(titel, intro, rijen, slot)];
    spijt                  {"intro", "wel": [(kop, tekst)], "niet": [(kop, tekst)]};
    valkuilen              [(kop, tekst)], met een link naar /tools/offertechecker/.
- KOSTEN4: nieuwe pagina's in hetzelfde schema als badkamer_kosten.KOSTEN.
- B4: nieuwe bronnen.

Inbouwen gebeurt in badkamer_kosten.py (net als badkamer_kosten3); build.py hoeft niet te veranderen.

Zoekwoorden (Semrush, database nl, november 2026, volume per maand): wat kost een nieuwe badkamer 1.900,
badkamer renovatie kosten 1.600, nieuwe badkamer kosten 1.300, badkamer verbouwen kosten 1.300,
badkamer kosten 720, badkamer renoveren kosten 320, goedkope badkamer 320, tegelzetter kosten 260,
badkamer prijs 260, badkamer betegelen kosten 210, badkamer tegels over tegels 210, badkamer budget 140,
tegelzetter prijs per m2 110, beton cire badkamer kosten 110, kleine badkamer kosten 90,
badkamer opknappen kosten 90, vloertegels leggen prijs per m2 90, inloopdouche kosten 70,
badkamer verplaatsen kosten 70, badkamer verplaatsen 70, badkamer 5m2 kosten 40.

Alle bedragen zijn richtprijzen inclusief 21% btw (peildatum november 2026). Gedeelde posten komen uit
richtprijzen.py. Nieuwe bandbreedtes en hun bronnen:
- Microcement / beton ciré: Werkspot €100 – €150 per m²; Homedeal €120 – €180 per m², in de douche
  €150 – €200 per m²; Slimster €120 – €150 per m² (incl. materiaal, arbeid en btw). Dezelfde bedragen
  als /materialen/microcement/ (badkamer_materialen.py).
- Slimster, compleet nieuwe badkamer: leidingen verplaatsen in een hele badkamer vanaf ca. €5.000 en
  budgetbadkamer €3.000 – €7.000 (zie richtprijzen.py, slimster_badkamer).
- Homedeal, kleine badkamer verbouwen: 5 m² €4.500 – €8.000, basic €3.000 – €5.000 (zie badkamer_kosten3).
Eigen inschattingen (staan op de pagina als eigen inschatting):
- hechtprimer en egaliseren bij tegels over tegels €5 – €15 per m²;
- deur inkorten of dorpel aanpassen €75 – €200;
- afvoer van een verplaatste badkamer naar een andere verdieping: valstandaard of vuilwaterpomp,
  zie de pagina badkamer-verplaatsen.
"""

import datetime

from badkamer_kosten3 import rp, niv, som, rb, bt, TOTAAL, r100, uren, VOEGEN_M2, VOORRIJ_INCL
import richtprijzen as RP
from components import eur

JAAR = datetime.date.today().year


def mx(paar, n):
    """(laag, hoog) maal een aantal, op hele euro's."""
    return (int(round(paar[0] * n)), int(round(paar[1] * n)))


def tot(rijen):
    return som(*(w for _, w in rijen if isinstance(w, tuple)))


B4 = {
    "werkspot_microcement": ("Werkspot, microcement in de badkamer", "https://www.werkspot.nl/badkamer-sanitair/artikelen/microcement-in-de-badkamer"),
    "homedeal_microcement": ("Homedeal, microcement prijs", "https://www.homedeal.nl/stucwerk/microcement"),
    "slimster_microcement": ("Slimster, microbeton en microcement prijzen", "https://slimster.nl/stukadoors/microbeton-microcement-prijzen/"),
}

# Rijen die op meerdere pagina's terugkomen ---------------------------------------------------------
OPB_SLOOP = [
    ("Sloop: alleen slopen", "sloop", "Sanitair en tegels eruit, zonder afvoer en zonder dekvloer.", None),
    ("Sloop: tot op de ruwe vloer, met afvoer", "sloop_compleet", "Inclusief dekvloer en afvoer van al het afval.", None),
    ("Afvoer van het sloopafval", "afval", "Afvoer door het bedrijf of een container van 3 tot 6 m³ inclusief storten.", None),
]
OPB_LEIDING = [
    ("Leidingwerk op dezelfde plek", "leidingwerk", "Water- en afvoerleidingen vernieuwen, aansluitpunten blijven waar ze zitten.", None),
    ("Leidingwerk verplaatsen (extra)", "leidingwerk_verplaatsen", "Bovenop het leidingwerk als toilet, douche of afvoer naar een andere plek gaan.", None),
    ("Elektra", "elektra", "Aparte groep, stopcontacten, schakelaars en eenvoudige spots.", None),
]
OPB_TEGEL = [
    ("Tegels (materiaal)", "tegels", "Keramische tegels; natuursteen en grote formaten zijn duurder.", None),
    ("Legloon tegelzetter", "tegelwerk", "Alleen het zetten. Kleine ruimtes en grote formaten zitten aan de bovenkant.", None),
    ("Lijm, voegsel en kit", "tegelwerk_hulpmateriaal", "Hulpmateriaal bovenop het legloon.", None),
    ("Waterdicht maken", "waterdicht", "Waterdichte laag met kimband in de douche- of badhoek en afschot naar de afvoer.", None),
]
OPB_SANITAIR = [
    ("Sanitair (levering)", "sanitair", "Douche, toilet, wastafelmeubel en kranen samen, van basis tot luxe.", None),
    ("Montage douche", "montage_douche", "Douche, douchewand of cabine plaatsen en aansluiten.", None),
    ("Montage toilet", "montage_toilet", "Toilet plaatsen en aansluiten op dezelfde plek.", None),
    ("Montage wastafelmeubel", "montage_meubel", "Meubel ophangen, met sifon en kraan.", None),
]
OPB_AFWERKING = [
    ("Kitwerk hele badkamer", "kitwerk_badkamer", "Alle naden afkitten met sanitairkit.", None),
    ("Ventilator", "ventilator", "Badkamerventilator met montage, bij voorkeur met vochtsensor.", None),
    ("Elektrische vloerverwarming", "vloerverwarming_elektrisch", "Optioneel. Met thermostaat en aansluiting.", None),
]

SANI_MIDDEN = som(niv("sanitair_douche", "midden"), niv("sanitair_toilet", "midden"), niv("sanitair_meubel", "midden"))
SANI_BASIS = som(niv("sanitair_douche", "basis"), niv("sanitair_toilet", "basis"), niv("sanitair_meubel", "basis"))
MONTAGE_3 = som(rp("montage_douche"), rp("montage_toilet"), rp("montage_meubel"))

EIGEN5 = ("Eigen rekenvoorbeeld met de richtprijzen per post uit de bronnen op deze pagina (peildatum november "
          f"{JAAR}, inclusief 21% btw). Je eigen badkamer kan hoger of lager uitkomen.")

VALK_STELPOST = ("Een te lage stelpost voor sanitair",
                 f"Een stelpost is een bedrag dat je mag uitgeven. Staat er €1.500 voor al het sanitair, terwijl een middensegment-set "
                 f"(douche, hangtoilet en meubel) al {bt(SANI_MIDDEN)} kost, dan betaal je het verschil later bij. Vraag om een "
                 f"sanitairlijst met merk en type, of een realistische stelpost.")
VALK_PUIN = ("Sloop zonder afvoer",
             f"'Slopen' is iets anders dan 'slopen en afvoeren'. Afvoer van het sloopafval kost {rb('afval')}. Staat het er niet bij, vraag het dan na.")
VALK_WATERDICHT = ("Geen regel voor waterdicht maken",
                   f"Het waterdicht maken van de douchehoek met kimband kost {rb('waterdicht')}. Staat het niet op de offerte, vraag dan hoe en "
                   f"met welk systeem het gebeurt. Dit is het deel dat je later niet meer ziet en dat het vaakst misgaat.")
VALK_M2 = ("Tegelwerk zonder aantal m²",
           f"Een bedrag 'tegelwerk' zonder aantal vierkante meters kun je niet vergelijken. Vraag het aantal m² vloer en wand, het legloon per m² "
           f"(richtprijs {rb('tegelwerk')}) en of lijm, voegsel en kit erin zitten (zo'n {rb('tegelwerk_hulpmateriaal')} per m² extra).")
VALK_MEERWERK = ("Meerwerk zonder afspraken",
                 f"Rot in de vloer, oude loden leidingen of asbest kom je soms pas tegen bij de sloop. Spreek vooraf af welk uurtarief geldt voor meerwerk "
                 f"(een loodgieter rekent {rb('uurtarief')} per uur excl. btw) en dat meerwerk eerst schriftelijk wordt voorgelegd.")
VALK_BTW = ("Prijzen exclusief btw",
            "Bedrijven die vooral zakelijk werken, noemen prijzen soms zonder btw. Op badkamerwerk komt er 21% bij: €10.000 excl. btw is €12.100 incl. btw. "
            "Vergelijk altijd inclusief btw.")
VALK_BETALING = ("Een groot voorschot",
                 "Een aanbetaling voor het bestellen van sanitair en tegels is normaal. Betaal de rest in termijnen naar voortgang, en de laatste termijn pas "
                 "als alles af en goedgekeurd is.")


# ===================================================================================================
# EXTRA: verdieping van bestaande pagina's
# ===================================================================================================

# ---------------------------------------------------------------- nieuwe-badkamer
_NB_BUDGET = [
    ("Slopen van de oude badkamer (4 m²)", som(rp("sloop_vast"), rp("sloop_m2", 4))),
    ("Afvoer van het sloopafval", rp("afval")),
    ("Leidingwerk water en afvoer, op dezelfde plek", rp("leidingwerk")),
    ("Elektra: groep, stopcontact en lamp", rp("elektra")),
    (f"Tegels (basis), 14 m² × {bt(niv('tegels', 'basis'))}", mx(niv("tegels", "basis"), 14)),
    (f"Legloon, 14 m² × {rb('tegelwerk')}", rp("tegelwerk", 14)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 14)),
    ("Waterdicht maken van de douchehoek", rp("waterdicht")),
    ("Sanitair (basis): douche met wand, toilet, meubel", SANI_BASIS),
    ("Montage van douche, toilet en meubel", MONTAGE_3),
    ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
    ("Totaal, inclusief btw", TOTAAL),
]
_NB_LUXE = [
    ("Slopen tot op de ruwe vloer, met afvoer", rp("sloop_compleet")),
    ("Leidingwerk water en afvoer", rp("leidingwerk")),
    ("Extra: toilet en afvoer verplaatsen", rp("leidingwerk_verplaatsen")),
    ("Elektra en verlichting", rp("elektra")),
    (f"Tegels (luxe), 35 m² × {bt(niv('tegels', 'luxe'))}", mx(niv("tegels", "luxe"), 35)),
    (f"Legloon, 35 m² × {rb('tegelwerk')}", rp("tegelwerk", 35)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 35)),
    ("Waterdicht maken van douche en badhoek", rp("waterdicht")),
    ("Sanitair (luxe): inloopdouche, bad, hangtoilet, meubel",
     som(niv("sanitair_douche", "luxe"), niv("sanitair_bad", "luxe"), niv("sanitair_toilet", "luxe"), niv("sanitair_meubel", "luxe"))),
    ("Montage van douche, bad, toilet en meubel", som(MONTAGE_3, rp("montage_bad"))),
    ("Elektrische vloerverwarming", rp("vloerverwarming_elektrisch")),
    ("Ventilator met vochtsensor", rp("ventilator")),
    ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
    ("Totaal, inclusief btw", TOTAAL),
]

EXTRA = {}

EXTRA["nieuwe-badkamer"] = {
    "title": f"Kosten nieuwe badkamer {JAAR}: prijs per post",
    "description": (f"Een nieuwe badkamer kost in {JAAR} meestal €6.000 tot €18.000 incl. btw. Met prijs per post, "
                    "drie rekenvoorbeelden en de valkuilen in offertes."),
    "snel": ("Een nieuwe badkamer van 5 tot 9 m² kost meestal <strong>€6.000 tot €18.000</strong>, inclusief sloopwerk, leidingwerk, "
             "tegels, sanitair, montage en 21% btw. Dat geldt ook als je zoekt op 'badkamer renoveren' of 'badkamer verbouwen': het is "
             "hetzelfde werk. Een eenvoudige badkamer met basissanitair kan vanaf zo'n €3.500. Verplaats je het toilet, de douche of de "
             "afvoer, of kies je luxe sanitair en grote tegels, dan kom je al snel boven de €20.000. Hieronder zie je per post waar het "
             "geld heen gaat, met drie uitgerekende voorbeelden."),
    "opbouw_intro": ("Een badkamerofferte bestaat uit vijf blokken: sloop, leidingwerk (met elektra), tegelwerk, sanitair en afwerking. "
                     "Per post zie je hieronder de richtprijs en de bron. Zo kun je een offerte regel voor regel naast deze bedragen leggen."),
    "opbouw": OPB_SLOOP + OPB_LEIDING + OPB_TEGEL + OPB_SANITAIR + OPB_AFWERKING,
    "voorbeeld_titel": "Voorbeeld 1: gewone badkamer van 6 m² (midden)",
    "voorbeelden": [
        ("Voorbeeld 2: kleine badkamer van 4 m² (budget)",
         "Een badkamer van 2 bij 2 meter in een rijtjeshuis uit de jaren zeventig. Alles blijft op dezelfde plek. Basissanitair, "
         "tegels tot het plafond in de douchehoek en tot 1,20 m op de andere wanden: zo'n 14 m² tegelwerk.",
         _NB_BUDGET, EIGEN5),
        ("Voorbeeld 3: luxe badkamer van 9 m² met bad",
         "Een badkamer van 3 bij 3 meter. Het toilet gaat naar een andere wand. Inloopdouche met regendouche, vrijstaand bad, "
         "dubbel meubel, vloerverwarming en tegels in groot formaat tot het plafond: zo'n 35 m².",
         _NB_LUXE, EIGEN5 + " Meer over dit segment lees je bij <a href=\"/kosten/luxe-badkamer/\">kosten luxe badkamer</a>."),
    ],
    "spijt": {
        "intro": "Niet elke euro is even belangrijk. Op sommige posten kun je flink schrappen zonder dat je er later last van hebt. Op andere juist niet.",
        "wel": [
            ("Indeling houden.", f"Toilet, douche en wastafel op hun plek laten scheelt {rb('leidingwerk_verplaatsen')} aan extra leidingwerk."),
            ("Standaard tegelformaat.", f"Tegels van 30 × 60 of 60 × 60 cm uit het middensegment ({bt(niv('tegels', 'midden'))} per m²) zien er strak uit en zijn sneller gelegd dan mozaïek of platen van 120 cm."),
            ("Niet overal tot het plafond tegelen.", "Buiten de douche kan de wand boven 1,20 m ook vochtbestendig gestuct of geverfd worden. Dat scheelt tegels én legloon."),
            ("Opbouw in plaats van inbouw.", "Een opbouwthermostaat met regendouche geeft bijna hetzelfde gevoel als inbouw en is later makkelijk te vervangen."),
            ("Sanitair uit het middensegment.", f"Basis- en middensanitair verschillen vooral in uitstraling. Het verschil tussen een set midden ({bt(SANI_MIDDEN)}) en luxe kan duizenden euro's zijn."),
        ],
        "niet": [
            ("Waterdicht maken.", f"Kost {rb('waterdicht')}, maar een lekkende douchehoek kost later een nieuwe badkamer en soms het plafond van de buren."),
            ("Oude leidingen.", "Liggen er nog loden of oude stalen leidingen, vervang ze nu. Na het tegelen kom je er niet meer bij."),
            ("Ventilatie.", f"Een goede ventilator met vochtsensor ({rb('ventilator')}) voorkomt schimmel. Zonder ventilatie gaat ook een nieuwe badkamer snel achteruit."),
            ("Afschot en afvoer.", "Een douche die niet goed afloopt, merk je elke dag. Laat het afschot vóór het tegelen controleren."),
            ("Een vakman met garantie.", "Kies op prijs én op garantie en referenties. Lees <a href=\"/kennisbank/garantie-badkamerrenovatie/\">welke garantie je mag verwachten</a>."),
        ],
    },
    "valkuilen": [VALK_STELPOST, VALK_PUIN, VALK_WATERDICHT, VALK_M2,
                  ("Elektra 'in overleg'", f"Een aparte groep, stopcontacten en spots kosten samen {rb('elektra')}. Staat elektra er niet of als 'in overleg' op, dan komt het later als meerwerk."),
                  VALK_MEERWERK, VALK_BTW, VALK_BETALING],
    "faqs_extra": [
        ("Is badkamer renoveren duurder dan badkamer verbouwen?", "Nee, dat is hetzelfde werk: de oude badkamer eruit en een nieuwe erin. Pas als de badkamer naar een andere plek in huis gaat, wordt het duurder. Zie <a href=\"/kosten/badkamer-verplaatsen/\">kosten badkamer verplaatsen</a>."),
        ("Wat kost een badkamer van 5 m²?", "Een eenvoudige badkamer van 5 m² kost volgens Homedeal €4.500 tot €8.000. Met een inloopdouche, hangtoilet en tegels tot het plafond kom je eerder uit op €7.000 tot €12.000 (de variant midden hierboven)."),
        ("Hoeveel moet ik reserveren voor onvoorziene kosten?", "Houd 10 tot 15% van je budget achter de hand. Bij de sloop komen soms rotte vloerdelen, oude leidingen of asbest tevoorschijn. Spreek vooraf af hoe meerwerk wordt gemeld en afgerekend."),
        ("Wat is het duurste deel van een nieuwe badkamer?", f"Meestal het sanitair ({rb('sanitair')} voor alles samen) en daarna het leidingwerk ({rb('leidingwerk')}) en het tegelwerk. Hoe duur het tegelwerk is, hangt vooral af van het aantal m²."),
        ("Hoeveel offertes moet ik aanvragen?", "Drie is een goed aantal. Minder geeft weinig vergelijking, meer kost veel tijd. Vraag elk bedrijf om dezelfde posten apart te noemen, dan kun je ze naast elkaar leggen in de <a href=\"/tools/offertechecker/\">offertechecker</a>."),
        ("Moet ik het sanitair zelf kopen?", "Dat mag, maar overleg het eerst. Sommige bedrijven geven dan geen garantie op het product, of rekenen meer voor de montage. Koop je zelf, controleer dan of alles compleet is (inbouwdelen, sifons, afvoerset) voordat de monteur komt."),
        ("Wanneer kan ik de nieuwe badkamer gebruiken?", "Na de laatste kitnaad nog 24 uur wachten. De waterdichte laag, lijm en voegen moeten daarvoor al droog zijn. Reken voor een gewone badkamer op twee tot drie weken zonder douche: regel dus een alternatief."),
    ],
    "verwant": ["badkamer-slopen", "tegelzetter-per-m2", "inloopdouche", "kleine-badkamer", "luxe-badkamer"],
}


# ---------------------------------------------------------------- inloopdouche
# Eigen inschattingen, zelfde bedragen als het bestaande rekenvoorbeeld op de pagina:
DOUCHEHOEK_SLOPEN = (200, 400)   # oude douchebak en tegels in de douchehoek eruit
DOUCHEBAK_SLOPEN = (150, 300)    # alleen de douchebak eruit, tegels blijven grotendeels
GOOT = (400, 800)                # afvoer aanpassen en douchegoot plaatsen
GOOT_VERLEGGEN = (600, 1200)     # afvoer verleggen en goot plaatsen in een vloer die omlaag moet
VLOER_AFSCHOT = (40, 70)         # per m²: vloer uitfrezen of opnieuw op afschot leggen (vgl. infrezen €35 – €80 per m², Homedeal/Slimster)
INBOUW = (400, 1200)             # inbouwdeel en werk voor een inbouwthermostaat, zoals badkamer_kosten3 (eigen inschatting)

_ID_BUDGET = [
    ("Oude douchebak eruit", DOUCHEBAK_SLOPEN),
    ("Douche (basis): vlakke douchebak of vloerplaat, vaste glazen wand, opbouwthermostaat", niv("sanitair_douche", "basis")),
    ("Montage van bak, wand en kraan", rp("montage_douche")),
    (f"Onderste rij tegels bijwerken, 2 m² × ({rb('tegels')} + {rb('tegelwerk')})", som(rp("tegels", 2), rp("tegelwerk", 2))),
    (f"Kitwerk rond de douche, 8 m × {rb('kitwerk')}", rp("kitwerk", 8)),
    ("Totaal, inclusief btw", TOTAAL),
]
_ID_LUXE = [
    ("Oude douchehoek en vloertegels slopen", som(DOUCHEHOEK_SLOPEN, rp("sloop_m2", 3))),
    ("Afvoer verleggen en lange douchegoot plaatsen", GOOT_VERLEGGEN),
    (f"Vloer op afschot, 6 m² × {bt(VLOER_AFSCHOT)}", mx(VLOER_AFSCHOT, 6)),
    ("Waterdicht maken van vloer en douchewanden", rp("waterdicht")),
    (f"Tegels (midden), 14 m² × {bt(niv('tegels', 'midden'))}", mx(niv("tegels", "midden"), 14)),
    (f"Legloon, 14 m² × {rb('tegelwerk')}", rp("tegelwerk", 14)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 14)),
    ("Douche (luxe): goot, glazen wand 8 mm, regendouche", niv("sanitair_douche", "luxe")),
    ("Inbouwdeel en werk voor de inbouwthermostaat", INBOUW),
    ("Montage van wand en douche", rp("montage_douche")),
    ("Totaal, inclusief btw", TOTAAL),
]
T_ID_BUDGET, T_ID_LUXE = tot(_ID_BUDGET), tot(_ID_LUXE)

EXTRA["inloopdouche"] = {
    "description": ("Een inloopdouche met plaatsing kost meestal €1.500 tot €5.000 incl. btw. Met prijs per post, drie rekenvoorbeelden "
                    "en de valkuilen in offertes."),
    "snel": ("Een inloopdouche laten plaatsen kost meestal <strong>€1.500 tot €5.000</strong>, inclusief plaatsing en 21% btw. "
             f"Komt hij op de plek van de oude douchebak en blijven de tegels grotendeels, dan zit je rond {bt(r100(T_ID_BUDGET))}. "
             "Wordt de douchehoek opnieuw betegeld met een goot, dan is het €1.800 tot €4.100. Moet de vloer omlaag voor een douche "
             f"zonder drempel, met inbouwkraan en regendouche, dan kom je op {bt(r100(T_ID_LUXE))}. Het glas is zelden de grootste post: "
             "de vloer, het afschot en het tegelwerk kosten meer."),
    "opbouw_intro": ("Een inloopdouche bestaat uit vier blokken: slopen, de vloer met afvoer, het tegelwerk en de douche zelf. "
                     "Per post zie je de richtprijs en de bron."),
    "opbouw": [
        ("Douchehoek slopen", (DOUCHEHOEK_SLOPEN[0], DOUCHEHOEK_SLOPEN[1], "per douche"), "Oude bak of vloer en de tegels in de douchehoek eruit.", ["eigen"]),
        ("Afvoer aanpassen en douchegoot", (GOOT[0], GOOT[1], "per douche"), "Goot of putje op de bestaande afvoer. Verleggen kost meer.", ["eigen"]),
        ("Vloer op afschot of uitfrezen", (VLOER_AFSCHOT[0], VLOER_AFSCHOT[1], "per m²"), "Alleen nodig voor een drempelloze douche of als de vloer omlaag moet.", ["eigen", "homedeal_vv", "slimster_frezen"]),
        ("Waterdicht maken", "waterdicht", "Waterdichte laag met kimband in de hoeken en afschot naar de afvoer.", None),
        ("Tegels (materiaal)", "tegels", "Keramische tegels; grote formaten zijn duurder.", None),
        ("Legloon tegelzetter", "tegelwerk", "Een douchehoek heeft veel hoeken en snijwerk, en zit dus vaak aan de bovenkant.", None),
        ("Douche (product)", "sanitair_douche", f"Goot of putje, glazen wand en kraan. Basis {bt(niv('sanitair_douche', 'basis'))}, midden {bt(niv('sanitair_douche', 'midden'))}, luxe {bt(niv('sanitair_douche', 'luxe'))}.", None),
        ("Inbouwthermostaat (extra)", (INBOUW[0], INBOUW[1], "per douche"), "Inbouwdeel en werk in de muur, bovenop de kraan zelf.", ["eigen"]),
        ("Montage douche", "montage_douche", "Wand, goot en kraan plaatsen en aansluiten.", None),
        ("Kitwerk", "kitwerk", "Naden rond de douche en langs de vloer.", None),
    ],
    "voorbeeld_titel": "Voorbeeld 1: douchebak eruit, nieuwe douchehoek met goot",
    "voorbeelden": [
        ("Voorbeeld 2: budget, tegels blijven",
         "Een oude douchebak van 90 × 90 cm gaat eruit. Er komt een vlakke douchebak van dezelfde maat met een vaste glazen wand. "
         "De wandtegels blijven, alleen de onderste rij wordt bijgewerkt.",
         _ID_BUDGET, EIGEN5),
        ("Voorbeeld 3: drempelloos met inbouwkraan",
         "In een badkamer van 6 m² gaat de hele vloer op afschot naar een lange goot, zodat de douche zonder drempel in de vloer overloopt. "
         "De afvoer wordt verlegd, er komt een inbouwthermostaat met regendouche en de douchewanden en vloer worden opnieuw betegeld (zo'n 14 m²).",
         _ID_LUXE, EIGEN5 + " Dit valt boven de gewone bandbreedte, omdat de hele vloer meedoet. Dan is het eigenlijk al bijna een "
         "<a href=\"/kosten/nieuwe-badkamer/\">nieuwe badkamer</a>."),
    ],
    "spijt": {
        "intro": "Bij een inloopdouche zie je het glas en de kraan, maar zit het belangrijkste werk in de vloer.",
        "wel": [
            ("Op de oude plek.", f"De afvoer ligt er al. Verleggen kost {bt(GOOT_VERLEGGEN)} in plaats van {bt(GOOT)} (eigen inschatting)."),
            ("Vaste wand zonder deur.", "Een vaste glazen wand van 90 of 100 cm is de goedkoopste en makkelijkst schoon te houden."),
            ("Opbouwthermostaat.", f"Een opbouw-regendouche scheelt het inbouwdeel ({bt(INBOUW)}) en is later makkelijk te vervangen."),
            ("Een kleine drempel.", "Een paar centimeter hoogteverschil is vaak veel goedkoper dan een vloer die helemaal omlaag moet."),
        ],
        "niet": [
            ("Waterdicht maken met kimband.", f"Kost {rb('waterdicht')}. Bij een douche zonder bak is dit de enige bescherming tegen lekkage."),
            ("Voldoende afschot.", "Plassen water in de douche merk je elke dag. Vraag hoe het afschot wordt gemaakt en gecontroleerd."),
            ("Glas met anti-kalklaag.", "Kost iets meer, maar scheelt jarenlang schrobben."),
            ("Breedte.", "Onder de 90 × 120 cm spat er bij een inloopdouche zonder deur snel water buiten. Liever iets meer ruimte dan een duurder merk."),
        ],
    },
    "valkuilen": [
        ("Geen regel voor het afschot", "Staat er alleen 'inloopdouche plaatsen', vraag dan of de vloer op afschot wordt gelegd en hoe. Zonder afschot is het geen inloopdouche, maar een natte vloer."),
        VALK_WATERDICHT,
        ("Glas zonder maat of dikte", "Een 'glazen wand' kan 6 mm standaard of 8 mm op maat zijn. Vraag maat, dikte en coating, anders vergelijk je appels met peren."),
        ("Goot of putje niet benoemd", f"Een lange goot op een nieuwe plek kost meer dan een putje op de oude afvoer: {bt(GOOT_VERLEGGEN)} tegen {bt(GOOT)} (eigen inschatting)."),
        ("Tegelwerk zonder m²", f"Vraag hoeveel m² vloer en wand er opnieuw wordt betegeld, en tegen welk legloon (richtprijs {rb('tegelwerk')} per m²)."),
        VALK_MEERWERK, VALK_BTW,
    ],
    "faqs_extra": [
        ("Wat kost een inloopdouche zonder drempel?", f"Als de vloer omlaag moet of de hele vloer op afschot gaat, reken je op {bt(r100(T_ID_LUXE))} met inbouwkraan en regendouche (voorbeeld 3). Met een opbouwkraan en minder tegelwerk kan het lager."),
        ("Wat kost alleen het plaatsen van een inloopdouche?", f"De montage van wand, goot en kraan kost {rb('montage_douche')}. Daar komen het product, het waterdicht maken en het tegelwerk bij."),
        ("Wat kost een glazen douchewand?", f"In het basissegment zit de wand in de douchebudgetten van {bt(niv('sanitair_douche', 'basis'))} (met bak en kraan). Glas op maat, 8 mm dik of zwart profiel valt in het midden- of luxesegment."),
        ("Kan een inloopdouche op een houten vloer?", "Ja, maar de vloer moet stijf genoeg zijn en goed waterdicht worden gemaakt. Vaak komt er een douchevloerelement met ingebouwd afschot op. Laat een specialist kijken naar de balken."),
        ("Inloopdouche of douchecabine: wat is goedkoper?", "Een cabine op een bestaande bak is meestal goedkoper, omdat er geen tegelwerk aan de vloer nodig is. Zie <a href=\"/kosten/douchecabine-plaatsen/\">kosten douchecabine plaatsen</a>."),
        ("Hoe voorkom ik dat water buiten de douche loopt?", "Met genoeg breedte (minstens 90 × 120 cm), een goot aan de achterkant en een wand die ver genoeg doorloopt. Een kleine drempel of een tweede glazen paneel helpt ook."),
        ("Is een inloopdouche handig als je ouder wordt?", "Ja, zonder drempel kun je er ook met een rollator of douchestoel in. Lees meer over een <a href=\"/kennisbank/levensloopbestendige-badkamer/\">levensloopbestendige badkamer</a>."),
    ],
    "bronnen": ["werkspot_badkamer", "homedeal_douche", "trustoo_badkamer", "werkspot_tegel", "homedeal_vv", "slimster_frezen", "werkspot_kit", "btw"],
    "verwant": ["nieuwe-badkamer", "bad-vervangen-door-douche", "douchecabine-plaatsen", "douche-vervangen", "tegelzetter-per-m2"],
    "kennis": [("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel: kan dat bij jou?"),
               ("/kennisbank/badkamer-waterdicht-maken/", "Zo wordt een badkamer waterdicht gemaakt"),
               ("/kennisbank/regendouche/", "Waar let je op bij een regendouche?"),
               ("/materialen/douchewand-glas/", "Douchewand: welk glas kies je?")],
}


# ---------------------------------------------------------------- tegelzetter-per-m2
OUDE_TEGELS_M2 = (19, 40)    # Slimster: vloer verwijderen €19 – €40 per m²
EGALISEREN_M2 = (5, 15)      # eigen inschatting: hechtprimer en egaliseren per m²
GROOT_M2 = (40, 55)          # legloon grote formaten, zoals de varianten op deze pagina
PROFIELEN = (100, 250)       # tegelprofielen en kitwerk, zoals het bestaande rekenvoorbeeld
DAG = (8 * rp("tegelwerk")[0], 10 * rp("tegelwerk")[1])   # eigen rekensom: 8 – 10 m² per dag × legloon

_TZ_VLOER = [
    (f"Oude vloertegels verwijderen, 6 m² × {bt(OUDE_TEGELS_M2)}", mx(OUDE_TEGELS_M2, 6)),
    (f"Egaliseren en primer, 6 m² × {bt(EGALISEREN_M2)}", mx(EGALISEREN_M2, 6)),
    (f"Legloon groot formaat, 6 m² × {bt(GROOT_M2)}", mx(GROOT_M2, 6)),
    (f"Tegels 60 × 120 cm (luxe), 6,6 m² × {bt(niv('tegels', 'luxe'))}", mx(niv("tegels", "luxe"), 6.6)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 6)),
    ("Totaal, inclusief btw", TOTAAL),
]
_TZ_TOILET = [
    (f"Legloon wand en vloer, 9 m² × {rb('tegelwerk')}", rp("tegelwerk", 9)),
    (f"Tegels (midden), 10 m² × {bt(niv('tegels', 'midden'))}", mx(niv("tegels", "midden"), 10)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 9)),
    ("Tegelprofielen en kitwerk", PROFIELEN),
    ("Totaal, inclusief btw", TOTAAL),
]
T_TZ_VLOER, T_TZ_TOILET = tot(_TZ_VLOER), tot(_TZ_TOILET)
T_TZ_ALLIN = (rp("tegelwerk")[0] + rp("tegelwerk_hulpmateriaal")[0] + rp("tegels")[0],
              rp("tegelwerk")[1] + rp("tegelwerk_hulpmateriaal")[1] + rp("tegels")[1])

EXTRA["tegelzetter-per-m2"] = {
    "description": (f"Een tegelzetter rekent in de badkamer €{rp('tegelwerk')[0]} tot €{rp('tegelwerk')[1]} per m² legloon incl. btw. "
                    "Met prijs per post, drie rekenvoorbeelden, dagprijs en valkuilen."),
    "snel": (f"Een tegelzetter rekent in de badkamer meestal <strong>{eur(rp('tegelwerk')[0])} tot {eur(rp('tegelwerk')[1])} per m²</strong> "
             "aan legloon, inclusief 21% btw. Gewone wandtegels zitten aan de onderkant, grote formaten, mozaïek en kleine ruimtes aan de "
             f"bovenkant. Met lijm en voegsel ({eur(rp('tegelwerk_hulpmateriaal')[0])} per m²) en de tegels zelf ({rb('tegels')} per m²) "
             f"betaal je all-in zo'n <strong>{bt(T_TZ_ALLIN)} per m²</strong>. Een tegelzetter legt in een badkamer 8 tot 10 m² per dag. "
             f"Voor een badkamer van 6 m² met wanden tot het plafond (25 m²) zit je aan legloon op {rb('tegelwerk', 25)}."),
    "opbouw_intro": ("Een offerte voor tegelwerk bestaat uit het legloon, het materiaal en het voorwerk. Vraag altijd welke van deze posten "
                     "in de prijs per m² zitten: daar zitten de grootste verschillen tussen offertes."),
    "opbouw": [
        ("Legloon", "tegelwerk", "Alleen het zetten. Standaard wandtegels aan de onderkant, kleine ruimtes en grote formaten aan de bovenkant.", None),
        ("Legloon groot formaat", (GROOT_M2[0], GROOT_M2[1], "per m²"), "Tegels van 60 × 120 cm en groter: zwaar en een heel vlakke ondergrond nodig.", ["trustoo_tegel", "eigen"]),
        ("Lijm, voegsel en kit", "tegelwerk_hulpmateriaal", "Hulpmateriaal bovenop het legloon. Soms al in de m²-prijs; vraag het na.", None),
        ("Tegels (materiaal)", "tegels", f"Basis {bt(niv('tegels', 'basis'))}, midden {bt(niv('tegels', 'midden'))}, luxe {bt(niv('tegels', 'luxe'))} per m². Reken 10% extra voor snijverlies.", None),
        ("Oude tegels verwijderen", (OUDE_TEGELS_M2[0], OUDE_TEGELS_M2[1], "per m²"), "Vloertegels eruit. Wandtegels die vastzitten kosten vaak meer tijd.", ["slimster_slopen"]),
        ("Egaliseren en primer", (EGALISEREN_M2[0], EGALISEREN_M2[1], "per m²"), "Ondergrond vlak maken en een hechtlaag zetten, ook bij tegels over tegels.", ["eigen"]),
        ("Waterdicht maken", "waterdicht", "Douche- of badhoek met kimband. Sommige tegelzetters rekenen dit apart.", None),
        ("Kitwerk", "kitwerk", "Naden in hoeken en langs bad en douche.", None),
    ],
    "voorbeeld_titel": "Voorbeeld 1: hele badkamer van 6 m², wanden tot het plafond",
    "voorbeelden": [
        ("Voorbeeld 2: alleen een nieuwe vloer van 6 m² met grote tegels",
         "De oude vloertegels gaan eruit, de vloer wordt geëgaliseerd en er komen tegels van 60 × 120 cm in. De wanden blijven.",
         _TZ_VLOER, EIGEN5 + " Het verwijderen van oude tegels komt van Slimster; egaliseren is een eigen inschatting."),
        ("Voorbeeld 3: toiletruimte, 9 m² tegelwerk",
         "Een toilet van 0,9 × 1,5 meter, wanden betegeld tot 1,5 meter. Klein, maar veel hoeken en snijwerk: het legloon zit aan de bovenkant.",
         _TZ_TOILET, EIGEN5 + " Per m² is dit duurder dan in een grote badkamer. Zie ook <a href=\"/kosten/toilet-renoveren/\">kosten toilet renoveren</a>."),
    ],
    "spijt": {
        "intro": "Tegelwerk zie je elke dag. Bespaar op het materiaal en de keuzes, niet op het voorwerk.",
        "wel": [
            ("Standaard formaat.", "30 × 60 of 60 × 60 cm gaat het snelst. Mozaïek en visgraat kosten tot €80 per m² aan legloon."),
            ("Tegels uit het middensegment.", f"Voor {bt(niv('tegels', 'midden'))} per m² heb je mooie, goed te verwerken keramische tegels."),
            ("Niet overal tot het plafond.", "Buiten de douche kan de wand boven 1,20 m ook vochtbestendig gestuct worden."),
            ("Recht leggen.", "Halfsteens of recht is sneller dan diagonaal of visgraat, en geeft minder snijverlies."),
        ],
        "niet": [
            ("Een vlakke ondergrond.", "Bij grote tegels zie je elke oneffenheid. Egaliseren kost een paar euro per m² en voorkomt randen die uitsteken."),
            ("Waterdicht maken.", f"Kost {rb('waterdicht')}. Tegels en voegen zijn zelf niet waterdicht."),
            ("Goede voeg en kit.", "Een epoxyvoeg of goede cementvoeg in de douche blijft schoner en houdt langer."),
            ("Een tegelzetter met badkamerervaring.", "Afschot in de vloer en kimband in de hoeken vragen vakkennis. Vraag naar foto's van eerdere badkamers."),
        ],
    },
    "valkuilen": [
        ("Prijs per m² zonder wat erin zit", "Vraag of voorbereiden, egaliseren, lijm, voegen en kitten in de prijs per m² zitten. Een lage m²-prijs met alles apart is vaak duurder."),
        ("Geen aantal m²", "Laat het aantal m² vloer en wand apart noemen. Dan kun je offertes echt vergelijken en zie je of ramen en deuren zijn afgetrokken."),
        ("Snijverlies niet meegenomen", "Koop zo'n 10% extra tegels. Bij visgraat of diagonaal 15%. Te weinig betekent later een andere kleur uit een nieuwe partij."),
        ("Grote formaten tegen het standaardtarief", f"Tegels van 120 cm vragen twee mensen en een vlakke ondergrond. Een offerte die daar gewoon {eur(rp('tegelwerk')[0])} per m² voor rekent, slaat vaak het voorwerk over."),
        VALK_WATERDICHT, VALK_BTW,
    ],
    "faqs_extra": [
        ("Wat kost een tegelzetter per dag?", f"Reken het om: bij 8 tot 10 m² per dag en {rb('tegelwerk')} per m² komt een dag tegelwerk op zo'n {bt(DAG)} aan legloon (eigen rekensom). Sommige tegelzetters rekenen een vast dagtarief, vooral bij klein werk."),
        ("Wat kost tegelen per m² inclusief tegels?", f"All-in, met legloon, lijm en voegsel en tegels, zo'n {bt(T_TZ_ALLIN)} per m². Met luxe tegels of natuursteen meer."),
        ("Wat kost vloertegels leggen per m²?", "In de badkamer €25 tot €45 per m² aan legloon, inclusief het meenemen van afschot naar de afvoer. Grote formaten zitten hoger."),
        ("Is tegelwerk in een kleine badkamer duurder?", "Per m² wel, door de vele hoeken en randen. In totaal betaal je natuurlijk minder. Zie <a href=\"/kosten/kleine-badkamer/\">kosten kleine badkamer</a>."),
        ("Wat kost tegels over tegels zetten?", f"Je betaalt het legloon ({rb('tegelwerk')} per m²) en egaliseren of primer ({bt(EGALISEREN_M2)} per m², eigen inschatting), maar geen sloop. Zie <a href=\"/kosten/tegels-over-tegels/\">kosten tegels over tegels</a>."),
        ("Zit de btw in de prijs per m²?", "Op deze pagina wel. Tegelzetters noemen hun prijs soms zonder btw; dan komt er 21% bij. €40 excl. btw is €48,40 incl. btw."),
        ("Moet ik de tegels zelf kopen?", "Dat mag. Laat de tegelzetter dan wel vooraf meekijken of de tegels geschikt zijn voor de badkamer en voor het formaat dat je wilt, en bestel ruim genoeg uit dezelfde partij."),
    ],
    "bronnen": ["trustoo_tegel", "homedeal_tegel", "werkspot_tegel", "slimster_slopen", "werkspot_kit", "btw"],
    "verwant": ["nieuwe-badkamer", "tegels-over-tegels", "kitwerk-voegen", "inloopdouche", "kleine-badkamer"],
    "kennis": [("/kennisbank/tegels-kiezen/", "Welke tegels passen in de badkamer?"),
               ("/kennisbank/grote-tegels-badkamer/", "Grote tegels in de badkamer"),
               ("/materialen/keramische-tegels/", "Keramische tegels: soorten en prijzen"),
               ("/badkamerspullen/badkamertegels-kopen/", "Waar let je op bij het kopen van tegels?")],
}


# ---------------------------------------------------------------- kleine-badkamer
def _klein(m2_vloer, m2_tegel, tegelniveau, sani, sani_label, ventilator=False):
    rijen = [
        (f"Slopen van de oude badkamer ({m2_vloer} m²)", som(rp("sloop_vast"), rp("sloop_m2", m2_vloer))),
        ("Afvoer van het sloopafval", rp("afval")),
        ("Leidingwerk water en afvoer, op dezelfde plek", rp("leidingwerk")),
        ("Elektra: groep, stopcontact en spots", rp("elektra")),
        (f"Tegels ({tegelniveau}), {m2_tegel} m² × {bt(niv('tegels', tegelniveau))}", mx(niv("tegels", tegelniveau), m2_tegel)),
        (f"Legloon, {m2_tegel} m² × {rb('tegelwerk')}", rp("tegelwerk", m2_tegel)),
        ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", m2_tegel)),
        ("Waterdicht maken van de douchehoek", rp("waterdicht")),
        (sani_label, sani),
        ("Montage van douche, toilet en meubel", MONTAGE_3),
    ]
    if ventilator:
        rijen.append(("Ventilator met vochtsensor", rp("ventilator")))
    rijen += [("Kitwerk en afwerking", rp("kitwerk_badkamer")), ("Totaal, inclusief btw", TOTAAL)]
    return rijen


_KL_2 = _klein(2, 14, "basis", SANI_BASIS, "Sanitair (basis): douche met wand, toilet, fontein of smal meubel")
_KL_4 = _klein(4, 20, "midden", SANI_MIDDEN, "Sanitair (midden): inloopdouche, hangtoilet, wandmeubel", ventilator=True)
T_KL_2, T_KL_4 = tot(_KL_2), tot(_KL_4)

EXTRA["kleine-badkamer"] = {
    "description": ("Een kleine badkamer van 2 tot 4 m² kost meestal €4.500 tot €13.000 incl. btw. Met prijs per post, "
                    "rekenvoorbeelden voor 2, 3 en 4 m² en valkuilen."),
    "snel": ("Een complete kleine badkamer van 2 tot 4 m² kost meestal <strong>€4.500 tot €13.000</strong>, inclusief sloop, leidingwerk, "
             f"tegels, sanitair, montage en 21% btw. Een badkamer van 2 m² met basissanitair komt uit op {bt(r100(T_KL_2))}, een badkamer "
             f"van 4 m² met inloopdouche en hangtoilet op {bt(r100(T_KL_4))}. Per m² is een kleine badkamer duurder dan een grote: "
             "douche, toilet, wastafel, leidingwerk en elektra kosten bijna hetzelfde, of de ruimte nu 3 of 8 m² is. "
             "Besparen doe je vooral door alles op dezelfde plek te houden."),
    "opbouw_intro": ("Ook een kleine badkamer heeft dezelfde vijf blokken als een grote: sloop, leidingwerk en elektra, tegelwerk, sanitair "
                     "en afwerking. Alleen het tegelwerk schaalt mee met de vierkante meters; de rest zijn vooral vaste kosten."),
    "opbouw": OPB_SLOOP[:1] + OPB_SLOOP[2:] + OPB_LEIDING + OPB_TEGEL + OPB_SANITAIR + OPB_AFWERKING[:2],
    "voorbeeld_titel": "Voorbeeld 1: badkamer van 3 m² (basis)",
    "voorbeelden": [
        ("Voorbeeld 2: badkamer van 2 m² (basis)",
         "Een badkamertje van 1 bij 2 meter met douche, toilet en fontein. Alles blijft op zijn plek. Tegels tot het plafond in de douche, "
         "tot 1,20 m op de andere wanden: zo'n 14 m².",
         _KL_2, EIGEN5),
        ("Voorbeeld 3: badkamer van 4 m² (midden)",
         "Een badkamer van 2 bij 2 meter. Inloopdouche met goot, hangtoilet en een wandmeubel, tegels tot het plafond (zo'n 20 m²) en een "
         "ventilator met vochtsensor.",
         _KL_4, EIGEN5 + " De bovenkant valt boven de gewone bandbreedte: dan zitten alle posten tegelijk aan de bovenkant. Dat gebeurt zelden, "
         "maar het laat zien waarom een vaste prijs per post in de offerte belangrijk is."),
    ],
    "spijt": {
        "intro": "In een kleine badkamer telt elke centimeter én elke euro. Dit zijn de keuzes waar je later geen spijt van hebt.",
        "wel": [
            ("Indeling houden.", f"Verplaatsen kost {rb('leidingwerk_verplaatsen')} extra. In een kleine badkamer is dat al snel een kwart van het budget."),
            ("Eén tegel voor vloer en wand.", "Minder snijverlies, minder restanten en de ruimte oogt groter."),
            ("Basissanitair in standaardmaat.", f"Een basisset ({bt(SANI_BASIS)}) in smalle standaardmaten is er genoeg. Maatwerk kost meer en heeft levertijd."),
            ("Glazen wand in plaats van cabine.", "Zelfde prijs of minder, en de ruimte voelt groter."),
        ],
        "niet": [
            ("Ventilatie.", f"In een kleine ruimte wordt het snel vochtig. Een ventilator met vochtsensor ({rb('ventilator')}) voorkomt schimmel."),
            ("Waterdicht maken.", f"Kost {rb('waterdicht')}. In een kleine badkamer spat het water overal; de hele vloer moet goed zijn."),
            ("Hangtoilet en zwevend meubel.", "Iets duurder, maar je houdt vloer vrij en schoonmaken gaat makkelijker."),
            ("Goed licht.", "Een spiegel met verlichting en een paar spots maken een kleine badkamer groter dan duurdere tegels."),
        ],
    },
    "valkuilen": [
        ("Een prijs per m² voor de hele badkamer", "Een bedrijf dat een badkamer 'per m²' prijst, rekent een kleine badkamer vaak te laag. De vaste kosten (sanitair, leidingwerk, elektra) zijn hetzelfde. Vraag om een prijs per post."),
        VALK_STELPOST, VALK_PUIN, VALK_WATERDICHT, VALK_M2, VALK_MEERWERK, VALK_BTW,
    ],
    "faqs_extra": [
        ("Wat kost een badkamer van 2 m²?", f"Met basissanitair zo'n {bt(r100(T_KL_2))} (voorbeeld 2). Homedeal noemt €3.500 tot €5.000 voor een eenvoudige badkamer van 2 m²."),
        ("Wat kost een badkamer van 4 m²?", f"Met inloopdouche, hangtoilet en tegels tot het plafond zo'n {bt(r100(T_KL_4))} (voorbeeld 3). Homedeal noemt €4.500 tot €7.000 voor een eenvoudige badkamer van 4 m²."),
        ("Wat kost een badkamer van 5 m²?", "Homedeal noemt €4.500 tot €8.000 voor een eenvoudige badkamer van 5 m². Met middensanitair kom je eerder op de bedragen van een <a href=\"/kosten/nieuwe-badkamer/\">gewone nieuwe badkamer</a>."),
        ("Wat kost een kleine badkamer per m²?", "Al snel €1.500 tot €3.000 per m², tegen €1.000 tot €2.000 per m² bij een badkamer van 6 tot 9 m². Dat is onze eigen rekensom op basis van de voorbeelden."),
        ("Kan ik een bad kwijt in een kleine badkamer?", "Vanaf zo'n 170 × 70 cm past een bad. Een bad met douchescherm is in 3 tot 4 m² vaak de beste combinatie. Zie <a href=\"/kosten/bad-plaatsen/\">kosten bad plaatsen</a>."),
        ("Wat is goedkoper: een kleine badkamer opknappen of vernieuwen?", "Opknappen kost €750 tot €4.000 als de tegels en leidingen goed zijn. Zie <a href=\"/kosten/badkamer-opknappen/\">kosten badkamer opknappen</a>."),
    ],
    "verwant": ["nieuwe-badkamer", "inloopdouche", "badkamer-opknappen", "badkamermeubel-plaatsen", "tegelzetter-per-m2"],
}


# ===================================================================================================
# KOSTEN4: nieuwe pagina's
# ===================================================================================================
KOSTEN4 = []


def r1000(paar):
    """Afronden op duizendtallen (laag omlaag, hoog omhoog)."""
    return (paar[0] // 1000 * 1000, -(-paar[1] // 1000) * 1000)


# ---------------------------------------------------------------- badkamer-verplaatsen
# Eigen inschattingen (staan op de pagina als eigen inschatting):
OUDE_RUIMTE = (500, 1500)       # leidingen afdoppen, vloer en wanden van de oude badkamer dichtmaken en vlak maken
NIEUWE_AFVOER = (800, 2500)     # nieuwe afvoer met afschot naar de standleiding, inclusief vloer openmaken
GIPSWAND_M2 = (40, 50)          # Homedeal, zolder verbouwen: gipswand per m²
POMP = (600, 1500)              # vuilwaterpomp (vermaler) met montage, als afvoer onder afschot niet kan
KANAAL = (150, 400)             # ventilatiekanaal door gevel of dak, zoals badkamer_kosten3

_VERPL = [
    ("Oude badkamer slopen tot op de ruwe vloer, met afvoer", rp("sloop_compleet")),
    ("Oude ruimte dichtmaken: leidingen afdoppen, vloer en wanden herstellen", OUDE_RUIMTE),
    (f"Nieuwe scheidingswand, 10 m² × {bt(GIPSWAND_M2)}", mx(GIPSWAND_M2, 10)),
    ("Leidingwerk water en afvoer", rp("leidingwerk")),
    ("Extra: leidingen naar de nieuwe plek verleggen", rp("leidingwerk_verplaatsen")),
    ("Nieuwe afvoer met afschot naar de standleiding", NIEUWE_AFVOER),
    ("Elektra: nieuwe groep, stopcontacten en spots", rp("elektra")),
    ("Ventilator met vochtsensor", rp("ventilator")),
    ("Ventilatiekanaal naar buiten", KANAAL),
    (f"Tegels (midden), 25 m² × {bt(niv('tegels', 'midden'))}", mx(niv("tegels", "midden"), 25)),
    (f"Legloon, 25 m² × {rb('tegelwerk')}", rp("tegelwerk", 25)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 25)),
    ("Waterdicht maken van de douchehoek", rp("waterdicht")),
    ("Sanitair (midden): douche, hangtoilet, wastafelmeubel", SANI_MIDDEN),
    ("Montage van douche, toilet en meubel", MONTAGE_3),
    ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
    ("Totaal, inclusief btw", TOTAAL),
]
T_VERPL = tot(_VERPL)
# Alleen de extra kosten van het verplaatsen, bovenop een gewone nieuwe badkamer.
_VERPL_EXTRA = [
    ("Oude ruimte dichtmaken en herstellen", OUDE_RUIMTE),
    (f"Nieuwe scheidingswand, 10 m² × {bt(GIPSWAND_M2)}", mx(GIPSWAND_M2, 10)),
    ("Extra: leidingen naar de nieuwe plek verleggen", rp("leidingwerk_verplaatsen")),
    ("Nieuwe afvoer met afschot naar de standleiding", NIEUWE_AFVOER),
    ("Ventilatiekanaal naar buiten", KANAAL),
    ("Extra kosten door het verplaatsen", TOTAAL),
]
T_VERPL_EXTRA = tot(_VERPL_EXTRA)

KOSTEN4.append({
    "slug": "badkamer-verplaatsen",
    "kort": "Badkamer verplaatsen",
    "omschrijving": "Wat het kost om de badkamer naar een andere plek in huis te verhuizen.",
    "h1": f"Wat kost een badkamer verplaatsen in {JAAR}?",
    "title": f"Kosten badkamer verplaatsen {JAAR}: richtprijzen",
    "description": (f"Een badkamer verplaatsen kost meestal €{r1000(T_VERPL)[0] // 1000}.000 tot €{r1000(T_VERPL)[1] // 1000}.000 incl. btw. "
                    "Zie wat de afvoer, de oude ruimte en een nieuwe wand extra kosten, met rekenvoorbeeld."),
    "dienst": "badkamer-renoveren",
    "van": r1000(T_VERPL)[0], "tot": r1000(T_VERPL)[1], "eenheid": "per badkamer van zo'n 6 m² op dezelfde verdieping, inclusief btw",
    "snel": (f"Een badkamer naar een andere plek op dezelfde verdieping verplaatsen kost meestal <strong>{bt(r1000(T_VERPL))}</strong>, "
             f"inclusief sloop, nieuwe leidingen, tegels, sanitair en 21% btw. Dat is zo'n {bt(r100(T_VERPL_EXTRA))} meer dan een nieuwe "
             "badkamer op de oude plek. Het meeste extra geld gaat naar de afvoer: die moet met afschot naar de standleiding lopen. "
             "Gaat de badkamer naar een andere verdieping, zoals de zolder, dan reken je eerder op €20.000 tot €35.000."),
    "varianten": [
        ("Een paar meter verschuiven", 9000, 17000, "In dezelfde ruimte of naar de kamer ernaast, dicht bij de standleiding. De afvoer kan met gewoon afschot."),
        ("Naar een andere kamer, zelfde verdieping", r1000(T_VERPL)[0], r1000(T_VERPL)[1], "Nieuwe wand, nieuwe afvoer door de vloer, oude ruimte herstellen. Zie het rekenvoorbeeld."),
        ("Naar een andere verdieping", 20000, 35000, "Bijvoorbeeld naar de zolder: nieuwe leidingen door het huis, vaak constructiewerk en isolatie."),
    ],
    "varianten_eenheid": "Totaalprijs inclusief nieuwe badkamer, materiaal, arbeid en btw",
    "varianten_noot": ("De eerste twee rijen zijn een eigen inschatting op basis van de richtprijzen per post. De bovenste rij volgt "
                       "Homedeal (badkamer op zolder €20.000 – €35.000). Slimster noemt voor leidingen verplaatsen in een hele badkamer vanaf zo'n €5.000."),
    "factoren": [
        ("De afstand tot de standleiding", "De afvoer van een toilet moet met afschot (zo'n 1 cm per meter) naar de standleiding lopen. Hoe verder weg, hoe hoger de vloer moet of hoe dieper de leiding. Dat is meestal de grootste extra post."),
        ("Het soort vloer", "In een houten vloer kun je leidingen tussen de balken leggen. In een betonvloer moet er gefreesd of een verhoogde vloer gemaakt worden. Boren door een kanaalplaatvloer mag alleen na overleg met een constructeur."),
        ("Wat er met de oude ruimte gebeurt", "Leidingen afdoppen, de vloer dichtmaken en de wanden vlak maken kost geld. Wordt de oude badkamer een slaapkamer of berging, dan komt daar nog stucwerk of een nieuwe vloer bij."),
        ("Een nieuwe wand of deur", f"Moet er een badkamer uit een andere kamer worden gemaakt, dan heb je een scheidingswand nodig. Een gipswand kost volgens Homedeal {bt(GIPSWAND_M2)} per m²; een nieuwe deur komt erbij."),
        ("Ventilatie", "Een badkamer heeft afzuiging naar buiten nodig. Ligt de nieuwe plek niet bij een bestaand kanaal, dan moet er een kanaal door de gevel of het dak."),
        ("Appartement of VvE", "In een appartement liggen de standleidingen vast en zijn ze van de VvE. Verplaatsen kan vaak maar beperkt, en je hebt toestemming nodig. Lees <a href=\"/kennisbank/verbouwen-in-vve/\">verbouwen in een VvE</a>."),
    ],
    "voorbeeld_titel": "Voorbeeld: badkamer naar de slaapkamer ernaast",
    "voorbeeld": (
        "Stel: een kleine badkamer van 3 m² in een woning uit de jaren zeventig gaat naar een deel van de slaapkamer ernaast. "
        "Er komt een nieuwe wand, een badkamer van 6 m² met inloopdouche, hangtoilet en wastafelmeubel, en tegels tot het plafond (zo'n 25 m²). "
        "De oude badkamer wordt een inloopkast.",
        _VERPL,
        EIGEN5 + " De bedragen voor de oude ruimte, de nieuwe afvoer en het ventilatiekanaal zijn een eigen inschatting.",
    ),
    "voorbeelden": [
        ("Alleen de extra kosten van het verplaatsen",
         "Wat betaal je meer dan voor een nieuwe badkamer op de oude plek? Dat zijn deze posten. De rest (sloop, tegels, sanitair) betaal je in beide gevallen.",
         _VERPL_EXTRA,
         "Eigen inschatting. De extra leidingkosten komen uit richtprijzen.py (Homedeal en Slimster), de wand uit Homedeal."),
    ],
    "btw_extra": "Wordt de oude badkamer een slaapkamer en laat je die stukadoren of verven, dan kan dat arbeidsloon onder 9% vallen als de woning ouder is dan twee jaar.",
    "besparen": [
        "Kies een nieuwe plek dicht bij de standleiding. Een meter dichterbij scheelt afschot, hoogte en geld.",
        "Leg de natte ruimtes (badkamer, toilet, keuken) boven of naast elkaar. Dan delen ze een afvoer.",
        "Overweeg of een nieuwe badkamer op de oude plek met een slimmere indeling ook goed is. Probeer het eerst in de <a href=\"/tools/indelingsplanner/\">indelingsplanner</a>.",
        "Doe het verplaatsen samen met andere verbouwingen, zoals een nieuwe vloer. Dan hoeft de vloer maar één keer open.",
    ],
    "specialist": ("Een badkamer verplaatsen is werk voor een badkamerspecialist of aannemer die loodgieter, elektricien en tegelzetter aanstuurt. "
                   "Laat vooraf meten of de afvoer met voldoende afschot kan. Zaag of boor nooit zelf in een betonvloer of draagmuur: "
                   "vraag bij twijfel een constructeur en kijk in het <a href=\"https://omgevingswet.overheid.nl/\" rel=\"nofollow noopener\">Omgevingsloket</a> of je een vergunning nodig hebt."),
    "opbouw_intro": ("Bij het verplaatsen van een badkamer betaal je de posten van een nieuwe badkamer, plus een paar posten die alleen bij verplaatsen horen. "
                     "Hieronder staan de belangrijkste, met bron."),
    "opbouw": OPB_SLOOP[1:2] + [
        ("Oude ruimte dichtmaken", (OUDE_RUIMTE[0], OUDE_RUIMTE[1], "per badkamer"), "Leidingen afdoppen, vloer dichtmaken, wanden vlak maken.", ["eigen"]),
        ("Nieuwe scheidingswand", (GIPSWAND_M2[0], GIPSWAND_M2[1], "per m²"), "Gipswand, vochtbestendig aan de badkamerkant.", ["homedeal_zolder"]),
    ] + OPB_LEIDING + [
        ("Nieuwe afvoer naar de standleiding", (NIEUWE_AFVOER[0], NIEUWE_AFVOER[1], "per badkamer"), "Vloer openmaken en een afvoer met afschot leggen.", ["eigen"]),
        ("Vuilwaterpomp (als afschot niet kan)", (POMP[0], POMP[1], "per stuk"), "Een pomp die het afvalwater naar de standleiding pompt. Noodoplossing: maakt geluid en heeft stroom nodig.", ["eigen"]),
        ("Ventilatiekanaal naar buiten", (KANAAL[0], KANAAL[1], "per badkamer"), "Kanaal door gevel of dak, bovenop de ventilator.", ["eigen"]),
    ] + OPB_TEGEL + OPB_SANITAIR[:1],
    "spijt": {
        "intro": "Verplaatsen is duur. Bespaar op de juiste plekken.",
        "wel": [
            ("Korte afstand.", "Elke meter minder naar de standleiding scheelt werk aan de vloer."),
            ("Standaard sanitair.", f"Een set uit het middensegment ({bt(SANI_MIDDEN)}) is genoeg. Het geld gaat al naar het leidingwerk."),
            ("Oude ruimte simpel afwerken.", "Een inloopkast of berging hoeft niet meteen af. Stucwerk en een vloer kunnen later."),
        ],
        "niet": [
            ("Afschot van de afvoer.", "Te weinig afschot geeft verstoppingen. Een vuilwaterpomp is een noodoplossing, geen besparing."),
            ("Ventilatie naar buiten.", "Zonder goed kanaal krijg je vocht en schimmel in de nieuwe ruimte."),
            ("Waterdicht maken.", f"Een nieuwe ruimte is nog nooit nat geweest. Waterdicht maken kost {rb('waterdicht')}; lekkage kost veel meer."),
        ],
    },
    "valkuilen": [
        ("Geen meting van het afschot", "Vraag of de specialist heeft gemeten hoe de afvoer naar de standleiding loopt, en hoeveel de vloer omhoog moet. Zonder meting is de prijs een gok."),
        ("De oude ruimte vergeten", f"Leidingen afdoppen en de oude vloer en wanden herstellen staat soms niet op de offerte. Reken zelf op zo'n {bt(OUDE_RUIMTE)} (eigen inschatting)."),
        ("Constructie 'in overleg'", "Moet er door een betonvloer of draagmuur, vraag dan wie de constructeur betaalt en of er een vergunning nodig is."),
        VALK_STELPOST, VALK_MEERWERK, VALK_BTW,
    ],
    "faqs": [
        ("Wat kost het om alleen het toilet te verplaatsen?", f"Afvoer en waterleiding van één toilet verleggen kost {rb('leidingwerk_toilet_verplaatsen')}, zonder het tegelwerk. Zie <a href=\"/kosten/toilet-verplaatsen/\">kosten toilet verplaatsen</a>."),
        ("Kan een badkamer overal in huis?", "Bijna overal, als de afvoer met afschot naar de standleiding kan of als je een vuilwaterpomp accepteert. Ook ventilatie naar buiten en een stevige vloer zijn nodig."),
        ("Heb ik een vergunning nodig om de badkamer te verplaatsen?", "Binnen je eigen woning meestal niet. Grijp je in in de draagconstructie, of woon je in een monument of appartement, dan kan dat anders zijn. Check het Omgevingsloket en vraag de VvE om toestemming."),
        ("Wat is een vuilwaterpomp?", "Een pomp achter het toilet die het afvalwater vermaalt en door een dunne leiding wegpompt. Handig als afschot niet kan, maar hij maakt geluid, heeft stroom nodig en kan verstoppen. Zie het als laatste optie."),
        ("Hoe lang duurt het verplaatsen van een badkamer?", "Reken op drie tot vijf weken. Het leidingwerk en de nieuwe wand komen bovenop het werk van een gewone badkamer."),
        ("Is verplaatsen goedkoper dan een tweede badkamer?", "Niet per se. Bij een tweede badkamer blijft de eerste staan en heb je geen kosten voor de oude ruimte. Zie <a href=\"/kosten/tweede-badkamer/\">kosten tweede badkamer</a>."),
    ],
    "bronnen": ["homedeal_zolder", "slimster_badkamer", "homedeal_toilet", "trustoo_badkamer", "werkspot_tegel", "btw"],
    "verwant": ["nieuwe-badkamer", "toilet-verplaatsen", "badkamer-op-zolder", "tweede-badkamer"],
    "kennis": [("/kennisbank/volgorde-badkamerrenovatie/", "In welke volgorde gaat een badkamerrenovatie?"),
               ("/kennisbank/verbouwen-in-vve/", "Verbouwen in een VvE"),
               ("/tools/indelingsplanner/", "Probeer indelingen met de indelingsplanner")],
})


# ---------------------------------------------------------------- tegels-over-tegels
DEUR = (75, 200)            # eigen inschatting: deur inkorten of dorpel aanpassen
PUTJE = (50, 150)           # eigen inschatting: opzetstuk of verhoogd afvoerputje
SANI_LOS = uren(4, 8)       # sanitair los- en vastzetten: 4 tot 8 uur tegen het uurtarief, incl. btw


def _tot_rijen(m2_wand, m2_vloer, douche=True, sanitair=True):
    m2 = m2_wand + m2_vloer
    rijen = [
        (f"Schoonmaken, hechtprimer en egaliseren, {m2} m² × {bt(EGALISEREN_M2)}", mx(EGALISEREN_M2, m2)),
        (f"Tegels (midden), {round(m2 * 1.1)} m² met snijverlies × {bt(niv('tegels', 'midden'))}", mx(niv("tegels", "midden"), round(m2 * 1.1))),
        (f"Legloon, {m2} m² × {rb('tegelwerk')}", rp("tegelwerk", m2)),
        ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", m2)),
    ]
    if douche:
        rijen.append(("Douchehoek opnieuw waterdicht maken", rp("waterdicht")))
    if m2_vloer:
        rijen += [("Afvoerputje verhogen", PUTJE), ("Deur inkorten of dorpel aanpassen", DEUR)]
    if sanitair:
        rijen.append(("Sanitair los- en weer vastzetten (4 tot 8 uur)", SANI_LOS))
    rijen.append(("Kitwerk hele badkamer", rp("kitwerk_badkamer")))
    rijen.append(("Totaal, inclusief btw", TOTAAL))
    return rijen


_TOT_ALLES = _tot_rijen(19, 6)
_TOT_VLOER = _tot_rijen(0, 6, douche=False, sanitair=True)
_TOT_WAND = _tot_rijen(19, 0)
T_TOT_ALLES, T_TOT_VLOER, T_TOT_WAND = tot(_TOT_ALLES), tot(_TOT_VLOER), tot(_TOT_WAND)
# Wat je uitspaart ten opzichte van eerst slopen: sloop (6 m²) en afvoer van het afval.
_TOT_SPAAR = [
    ("Slopen van de oude tegels (6 m² vloer met wanden)", som(rp("sloop_vast"), rp("sloop_m2", 6))),
    ("Afvoer van het sloopafval", rp("afval")),
    ("Wat je niet betaalt bij tegels over tegels", TOTAAL),
]
T_TOT_SPAAR = tot(_TOT_SPAAR)

KOSTEN4.append({
    "slug": "tegels-over-tegels",
    "kort": "Tegels over tegels",
    "omschrijving": "Wat het kost om nieuwe tegels over de oude te laten zetten, en wanneer dat kan.",
    "h1": f"Wat kost tegels over tegels in de badkamer?",
    "title": f"Tegels over tegels kosten {JAAR}: badkamer zonder slopen",
    "description": (f"Nieuwe tegels over de oude zetten kost in een badkamer van 6 m² zo'n {bt(r100(T_TOT_ALLES))} incl. btw. "
                    "Zie wanneer het kan, wat je bespaart op sloop en waar je op let."),
    "dienst": "tegelwerk-badkamer",
    "van": r100(T_TOT_ALLES)[0], "tot": r100(T_TOT_ALLES)[1], "eenheid": "voor wand en vloer van een badkamer van 6 m², inclusief btw",
    "snel": (f"Nieuwe tegels over de oude zetten kost in een badkamer van 6 m² met wanden tot het plafond (25 m²) zo'n "
             f"<strong>{bt(r100(T_TOT_ALLES))}</strong>, inclusief tegels, legloon, voorbereiding en 21% btw. Je bespaart het slopen en "
             f"afvoeren van de oude tegels: {bt(T_TOT_SPAAR)}. Het kan alleen als de oude tegels vlak en vast zitten en er geen vocht achter zit. "
             "De vloer wordt zo'n 1 tot 2 cm hoger, dus de deur en het afvoerputje moeten mee."),
    "varianten": [
        ("Alleen de vloer (6 m²)", *r100(T_TOT_VLOER), "Vloertegels over de oude, met verhoogd putje en ingekorte deur. Sanitair los en weer vast."),
        ("Alleen de wanden (19 m²)", *r100(T_TOT_WAND), "Wandtegels over de oude, douchehoek opnieuw waterdicht. Vloer blijft."),
        ("Wand en vloer (25 m²)", *r100(T_TOT_ALLES), "De hele badkamer opnieuw betegeld, zonder sloop."),
    ],
    "varianten_eenheid": "Totaalprijs voor een badkamer van 6 m², inclusief tegels uit het middensegment, arbeid en btw",
    "varianten_noot": "Eigen rekenvoorbeelden met de richtprijzen per post (legloon en tegels: Trustoo, Homedeal, Werkspot). Voorbereiding, putje en deur zijn een eigen inschatting.",
    "factoren": [
        ("De staat van de oude tegels", "Tik op de tegels. Klinkt een tegel hol, dan zit hij los en moet hij eruit. Zit er vocht achter, zie je scheuren of zijn de voegen zwart en zacht, dan is slopen beter."),
        ("De hoogte", "Nieuwe tegels met lijm maken de vloer 1 tot 2 cm hoger. De deur, de dorpel en het afvoerputje moeten daarop worden aangepast. Een douchebak of toilet moet soms los en weer vast."),
        ("Het gewicht", "Een tweede laag tegels is zwaarder. Op een stenen muur of betonvloer is dat geen probleem. Op een houten vloer of een lichte wand moet je het laten controleren."),
        ("De douchehoek", "Ook over oude tegels moet de douchehoek waterdicht worden gemaakt, met kimband in de hoeken. Oude tegels zijn zelf niet waterdicht."),
        ("Het tegelformaat", "Grote tegels werken goed over oude tegels, omdat je de oude voegen niet terugziet. Ze vragen wel een vlakke ondergrond: soms moet er eerst geëgaliseerd worden."),
    ],
    "voorbeeld_titel": "Voorbeeld: wand en vloer van een badkamer van 6 m²",
    "voorbeeld": (
        "Stel: een badkamer van 2 bij 3 meter met tegels uit de jaren negentig die nog vast zitten. Wanden tot het plafond (19 m²) en vloer (6 m²) "
        "krijgen nieuwe tegels uit het middensegment. Toilet en meubel gaan los en weer vast.",
        _TOT_ALLES,
        EIGEN5 + " Voorbereiding, putje, deur en het los- en vastzetten van sanitair zijn een eigen inschatting.",
    ),
    "voorbeelden": [
        ("Wat bespaar je op sloop?",
         "Deze posten betaal je niet als je over de oude tegels heen tegelt.",
         _TOT_SPAAR, "Bedragen uit richtprijzen.py (Slimster, Werkspot). De tegels, het legloon en het waterdicht maken betaal je in beide gevallen."),
    ],
    "btw_extra": "",
    "besparen": [
        "Kies grote tegels voor de vloer. Dan heb je minder voegen en zie je oneffenheden van de oude vloer minder.",
        "Laat alleen de vloer of alleen de wanden doen als de rest nog goed is.",
        "Combineer het met nieuw sanitair. Het sanitair moet toch al los.",
        "Laat eerst een tegelzetter de oude tegels controleren. Een losse tegel die je over het hoofd ziet, geeft later scheuren in de nieuwe laag.",
    ],
    "specialist": ("Tegels over tegels lijkt eenvoudig, maar de voorbereiding is het werk. De oude tegels moeten vet- en kalkvrij zijn, er moet een hechtprimer op "
                   "en de douchehoek moet waterdicht. Laat het doen door een tegelzetter met badkamerervaring, zeker in de douche."),
    "opbouw_intro": "Bij tegels over tegels vervalt de sloop, maar komen er een paar kleine posten bij. Per post zie je de richtprijs en de bron.",
    "opbouw": [
        ("Hechtprimer en egaliseren", (EGALISEREN_M2[0], EGALISEREN_M2[1], "per m²"), "Oude tegels ontvetten, primer zetten, oneffenheden vlak maken.", ["eigen"]),
        ("Tegels (materiaal)", "tegels", "Reken 10% extra voor snijverlies.", None),
        ("Legloon tegelzetter", "tegelwerk", "Zelfde legloon als op een kale muur.", None),
        ("Lijm, voegsel en kit", "tegelwerk_hulpmateriaal", "Een flexibele lijm die op tegels hecht.", None),
        ("Waterdicht maken", "waterdicht", "Douchehoek met kimband, ook over oude tegels.", None),
        ("Afvoerputje verhogen", (PUTJE[0], PUTJE[1], "per stuk"), "Opzetstuk of nieuw putje op de nieuwe vloerhoogte.", ["eigen"]),
        ("Deur inkorten of dorpel aanpassen", (DEUR[0], DEUR[1], "per deur"), "Nodig omdat de vloer hoger wordt.", ["eigen"]),
        ("Uurtarief voor sanitair los en vast", "uurtarief", "Toilet, meubel en douchebak los en weer vast.", None),
    ],
    "spijt": {
        "intro": "Tegels over tegels is al een besparing. Doe het dan ook goed.",
        "wel": [
            ("Sloop en afvoer.", f"Scheelt {bt(T_TOT_SPAAR)} en een paar dagen stof."),
            ("Alleen wat nodig is.", "Is de vloer nog mooi? Laat dan alleen de wanden doen, of andersom."),
        ],
        "niet": [
            ("De controle van de oude tegels.", "Holle of losse tegels eerst eruit. Anders scheurt de nieuwe laag."),
            ("Waterdicht maken in de douche.", f"Kost {rb('waterdicht')}. Ook over oude tegels nodig."),
            ("Een goede lijm en primer.", "Gewone tegellijm hecht slecht op geglazuurde tegels."),
        ],
    },
    "valkuilen": [
        ("Geen controle van de ondergrond", "Vraag of de tegelzetter de oude tegels op holle plekken en vocht controleert, en wat er gebeurt als hij die vindt."),
        ("Deur en putje vergeten", f"De vloer wordt hoger. Een deur inkorten kost {bt(DEUR)}, een putje verhogen {bt(PUTJE)} (eigen inschatting). Staat het er niet op, dan komt het later."),
        VALK_WATERDICHT, VALK_M2, VALK_BTW,
    ],
    "faqs": [
        ("Kun je overal tegels over tegels zetten?", "Niet overal. De oude tegels moeten vast en vlak zitten, zonder vocht erachter. Op een houten vloer of lichte wand moet je het gewicht laten controleren."),
        ("Hoeveel hoger wordt de vloer?", "Zo'n 1 tot 2 cm, afhankelijk van de tegel en de lijm. Grote, dikke tegels maken het hoger."),
        ("Is tegels over tegels goedkoper dan slopen?", f"Ja, je spaart {bt(T_TOT_SPAAR)} aan sloop en afvoer. De tegels en het legloon betaal je in beide gevallen."),
        ("Kan het in de douche?", "Ja, als de douchehoek opnieuw waterdicht wordt gemaakt met kimband in de hoeken. Zit er al vocht achter de oude tegels, dan moeten ze eruit."),
        ("Hoe lang gaat tegels over tegels mee?", "Net zo lang als gewoon tegelwerk, als de voorbereiding goed is. Het zwakke punt is de hechting op de oude tegels: daarom zijn schoonmaken en primer belangrijk."),
        ("Wat is goedkoper: tegels over tegels of wandpanelen?", "Wandpanelen zijn vaak sneller geplaatst, maar per m² niet altijd goedkoper. Lees meer over <a href=\"/kennisbank/badkamer-zonder-tegels/\">een badkamer zonder tegels</a>."),
    ],
    "bronnen": ["trustoo_tegel", "homedeal_tegel", "werkspot_tegel", "slimster_slopen", "werkspot_puin", "werkspot_kit", "homedeal_lood", "btw"],
    "verwant": ["tegelzetter-per-m2", "badkamer-opknappen", "badkamer-slopen", "nieuwe-badkamer"],
    "kennis": [("/kennisbank/tegels-kiezen/", "Welke tegels passen in de badkamer?"),
               ("/kennisbank/badkamer-zonder-tegels/", "Een badkamer zonder tegels: kan dat?"),
               ("/kennisbank/badkamer-waterdicht-maken/", "Zo wordt een badkamer waterdicht gemaakt")],
})


# ---------------------------------------------------------------- badkamer-opknappen
# Staat onderaan, omdat het voorbeeld 'groot opknappen' de bedragen van tegels over tegels gebruikt.
KRAAN_OPBOUW = (50, 300)     # Werkspot, douchekraan vervangen: thermostaatkraan
DOUCHEWAND_BASIS = (250, 500)  # zoals badkamer_kosten3 (eigen inschatting)
TEGELVERF_M2 = (25, 50)      # eigen inschatting, zoals badkamer_kosten3

_OK_BUDGET = [
    ("Hele badkamer opnieuw afkitten", rp("kitwerk_badkamer")),
    (f"Voegen in de douche vernieuwen, 6 m² × {bt(VOEGEN_M2)}", mx(VOEGEN_M2, 6)),
    ("Thermostatische douchekraan met glijstang", KRAAN_OPBOUW),
    ("Kraan monteren (1 tot 2 uur)", uren(1, 2)),
    ("Ventilator met vochtsensor", rp("ventilator")),
    ("Voorrijkosten", VOORRIJ_INCL),
    ("Totaal, inclusief btw", TOTAAL),
]
_OK_GROOT = [
    ("Nieuwe wandtegels over de oude, 19 m² (zie tegels over tegels)", T_TOT_WAND),
    ("Wastafelmeubel (midden) met kraan en spiegel", niv("sanitair_meubel", "midden")),
    ("Meubel ophangen en aansluiten", rp("montage_meubel")),
    ("Hangtoilet of nieuw staand toilet (midden)", niv("sanitair_toilet", "midden")),
    ("Toilet plaatsen en aansluiten", rp("montage_toilet")),
    ("Totaal, inclusief btw", TOTAAL),
]
T_OK_BUDGET, T_OK_GROOT = tot(_OK_BUDGET), tot(_OK_GROOT)

EXTRA["badkamer-opknappen"] = {
    "description": ("Een badkamer opknappen zonder slopen kost meestal €750 tot €4.000 incl. btw. Met prijs per post, drie rekenvoorbeelden "
                    "en wanneer opknappen niet genoeg is."),
    "snel": ("Een badkamer opknappen zonder te slopen kost meestal <strong>€750 tot €4.000</strong>, inclusief 21% btw. Alleen opfrissen "
             f"met nieuwe kit, voegen in de douche, een nieuwe kraan en een ventilator kost {bt(r100(T_OK_BUDGET))}. Met een nieuw "
             "wastafelmeubel en een nieuwe douchewand erbij zit je rond €1.300 tot €3.500. Laat je ook nieuwe tegels over de oude zetten "
             f"en het toilet vervangen, dan kom je op {bt(r100(T_OK_GROOT))}. Opknappen werkt alleen als de tegels vastzitten, er geen "
             "vocht achter zit en de leidingen goed zijn."),
    "opbouw_intro": ("Bij opknappen betaal je per onderdeel. Kies wat je vervangt; elke post hieronder kan los. Kleine klussen samen "
                     "laten doen scheelt voorrijkosten en halve uren."),
    "opbouw": [
        ("Kitwerk per meter", "kitwerk", "Oude kit eruit, nieuwe sanitairkit erin.", None),
        ("Kitwerk hele badkamer", "kitwerk_badkamer", "Alle naden in één keer.", None),
        ("Voegen vernieuwen", (VOEGEN_M2[0], VOEGEN_M2[1], "per m²"), "Oude voeg uitslijpen en opnieuw voegen.", ["eigen"]),
        ("Douchekraan (product)", (KRAAN_OPBOUW[0], KRAAN_OPBOUW[1], "per stuk"), "Thermostatische opbouwkraan.", ["werkspot_douchekraan"]),
        ("Douchewand (basis)", (DOUCHEWAND_BASIS[0], DOUCHEWAND_BASIS[1], "per stuk"), "Vaste glazen wand in standaardmaat.", ["eigen"]),
        ("Wastafelmeubel (product)", "sanitair_meubel", f"Met wastafel, kraan en spiegel. Basis {bt(niv('sanitair_meubel', 'basis'))}, midden {bt(niv('sanitair_meubel', 'midden'))}.", None),
        ("Montage wastafelmeubel", "montage_meubel", "Ophangen en aansluiten, met sifon en kraan.", None),
        ("Toilet (product)", "sanitair_toilet", "Staand toilet of hangtoilet.", None),
        ("Montage toilet", "montage_toilet", "Op dezelfde plek.", None),
        ("Ventilator", "ventilator", "Bij voorkeur met vochtsensor.", None),
        ("Tegelverf door een vakman", (TEGELVERF_M2[0], TEGELVERF_M2[1], "per m²"), "Alleen buiten de douche; slijt in de douche snel.", ["eigen", "werkspot_tegelverf"]),
        ("Uurtarief loodgieter", "uurtarief", "Voor kleine klussen zonder vaste prijs.", None),
        ("Voorrijkosten", "voorrijkosten", "Per bezoek.", None),
    ],
    "voorbeeld_titel": "Voorbeeld 1: opknappen met nieuw meubel en douchewand",
    "voorbeelden": [
        ("Voorbeeld 2: alleen opfrissen",
         "Nieuwe kit in de hele badkamer, nieuwe voegen in de douche, een nieuwe thermostaatkraan en een ventilator met vochtsensor. "
         "Alles in één bezoek.",
         _OK_BUDGET, EIGEN5 + " Voegen vernieuwen is een eigen inschatting; de kraan komt van Werkspot."),
        ("Voorbeeld 3: groot opknappen met tegels over tegels",
         "De wanden krijgen nieuwe tegels over de oude (19 m²), er komt een nieuw wastafelmeubel en een nieuw toilet op dezelfde plek. "
         "Leidingen en vloer blijven.",
         _OK_GROOT, EIGEN5 + " Het tegelwerk is uitgewerkt op de pagina <a href=\"/kosten/tegels-over-tegels/\">tegels over tegels</a>."),
    ],
    "spijt": {
        "intro": "Opknappen is slim als de basis goed is. Investeer in wat je elke dag gebruikt, niet in wat er later toch uit moet.",
        "wel": [
            ("Schoonmaken en ontkalken eerst.", "Soms is dat al genoeg. Witte voegen en nieuwe kit maken een badkamer jaren jonger."),
            ("Meubel van dezelfde breedte.", "Dan passen de aansluitingen en hoef je geen gaten in de tegels te dichten."),
            ("Opbouwkraan.", "Een nieuwe thermostaatkraan op de oude aansluitingen is een klus van een uur of twee."),
            ("Klussen bundelen.", f"Eén bezoek scheelt voorrijkosten ({rb('voorrijkosten')} excl. btw per keer)."),
        ],
        "niet": [
            ("Vocht achter de tegels.", "Zie je zwarte voegen die niet schoon worden of klinkt een tegel hol? Dan is opknappen weggegooid geld. Laat het eerst onderzoeken."),
            ("Oude leidingen.", "Lekt er iets in de muur of zijn de leidingen van lood, kies dan voor een nieuwe badkamer."),
            ("Tegelverf in de douche.", "Slijt snel. In de douche liever nieuwe tegels over de oude of wandpanelen."),
            ("Ventilatie.", "Een badkamer die steeds beslaat en schimmelt, blijft dat doen na het opknappen. Los de oorzaak op."),
        ],
    },
    "valkuilen": [
        ("Uurtarief zonder maximum", f"Kleine klussen gaan vaak per uur ({rb('uurtarief')} excl. btw). Vraag een vaste prijs of een maximum aantal uren."),
        ("Voorrijkosten per klus", "Laat je drie dingen op drie dagen doen, dan betaal je drie keer voorrijkosten. Vraag alles in één bezoek."),
        ("Opknappen terwijl er vocht zit", "Een goed bedrijf controleert eerst de tegels en de voegen. Krijg je een offerte zonder dat iemand heeft gekeken, vraag dan wat er gebeurt als er vocht achter zit."),
        ("Voegen 'bijwerken' zonder m²", f"Vraag hoeveel m² voegwerk er vernieuwd wordt (eigen inschatting {bt(VOEGEN_M2)} per m²) en of de oude voeg eruit gaat."),
        VALK_BTW,
    ],
    "faqs_extra": [
        ("Wat kost een badkamer opfrissen?", f"Met nieuwe kit, nieuwe voegen in de douche, een nieuwe kraan en een ventilator zo'n {bt(r100(T_OK_BUDGET))} (voorbeeld 2)."),
        ("Wat kost een badkamer opknappen met nieuwe tegels?", f"Met nieuwe wandtegels over de oude, een nieuw meubel en toilet zo'n {bt(r100(T_OK_GROOT))} (voorbeeld 3). Dan zit je al dicht bij een <a href=\"/kosten/kleine-badkamer/\">kleine nieuwe badkamer</a>."),
        ("Wat kost een nieuw toilet in de badkamer?", f"Een toilet uit het middensegment kost {bt(niv('sanitair_toilet', 'midden'))}, de montage {rb('montage_toilet')}. Zie ook <a href=\"/kosten/toilet-renoveren/\">kosten toilet renoveren</a>."),
        ("Kan ik mijn badkamer opknappen in een huurhuis?", "Kleine dingen zoals kit en een nieuwe douchekop meestal wel. Voor tegels, kranen en meubels heb je toestemming van de verhuurder nodig. Lees <a href=\"/kennisbank/badkamer-huurwoning/\">badkamer in een huurwoning</a>."),
        ("Hoe lang duurt opknappen?", "Opfrissen met kit, voegen en een kraan is in één tot twee dagen klaar. Met tegels over tegels en nieuw sanitair reken je op een week."),
        ("Wat levert opknappen op bij verkoop van het huis?", "Een frisse badkamer verkoopt prettiger, maar wat het oplevert verschilt per huis. Doe het voor jezelf; een makelaar in je buurt kan zeggen of het bij verkoop verschil maakt."),
    ],
    "bronnen": ["werkspot_kit", "slimster_kit", "werkspot_sanitair", "werkspot_douchekraan", "werkspot_tegel", "werkspot_tegelverf", "trustoo_badkamer", "homedeal_lood", "trustoo_lood", "btw"],
    "verwant": ["kitwerk-voegen", "tegels-over-tegels", "douche-vervangen", "wastafel-vervangen", "kleine-badkamer"],
}


# ---------------------------------------------------------------- microcement-badkamer
MC_WAND = (100, 150)     # Werkspot €100 – €150, Slimster €120 – €150 per m²
MC_VLOER = (120, 180)    # Homedeal €120 – €180 per m² (vloer en wand)
MC_DOUCHE = (150, 200)   # Homedeal: inloopdouche €150 – €200 per m²

_MC = [
    (f"Schoonmaken, primer en egaliseren over de oude tegels, 25 m² × {bt(EGALISEREN_M2)}", mx(EGALISEREN_M2, 25)),
    (f"Microcement op de wanden buiten de douche, 13 m² × {bt(MC_WAND)}", mx(MC_WAND, 13)),
    (f"Microcement in de douche, 6 m² × {bt(MC_DOUCHE)}", mx(MC_DOUCHE, 6)),
    (f"Microcement op de vloer, 6 m² × {bt(MC_VLOER)}", mx(MC_VLOER, 6)),
    ("Waterdichte laag onder het microcement in de douche", rp("waterdicht")),
    ("Sanitair los- en weer vastzetten (4 tot 8 uur)", SANI_LOS),
    ("Kitwerk hele badkamer", rp("kitwerk_badkamer")),
    ("Totaal, inclusief btw", TOTAAL),
]
_MC_TEGEL = [
    (f"Tegels (midden), 27,5 m² met snijverlies × {bt(niv('tegels', 'midden'))}", mx(niv("tegels", "midden"), 27.5)),
    (f"Legloon, 25 m² × {rb('tegelwerk')}", rp("tegelwerk", 25)),
    ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 25)),
    ("Totaal tegelwerk (zonder voorbereiding en waterdicht maken)", TOTAAL),
]
_MC_ALLEEN = [
    (f"Microcement wand, 13 m² × {bt(MC_WAND)}", mx(MC_WAND, 13)),
    (f"Microcement douche, 6 m² × {bt(MC_DOUCHE)}", mx(MC_DOUCHE, 6)),
    (f"Microcement vloer, 6 m² × {bt(MC_VLOER)}", mx(MC_VLOER, 6)),
    ("Totaal microcement (zonder voorbereiding en waterdicht maken)", TOTAAL),
]
T_MC, T_MC_TEGEL, T_MC_ALLEEN = tot(_MC), tot(_MC_TEGEL), tot(_MC_ALLEEN)

KOSTEN4.append({
    "slug": "microcement-badkamer",
    "kort": "Microcement en beton ciré",
    "omschrijving": "Wat microcement of beton ciré in de badkamer kost per m², en hoe dat zich verhoudt tot tegels.",
    "h1": f"Wat kost microcement of beton ciré in de badkamer?",
    "title": f"Microcement badkamer kosten {JAAR}: prijs per m²",
    "description": (f"Microcement of beton ciré in de badkamer kost €{MC_WAND[0]} tot €{MC_DOUCHE[1]} per m² incl. btw. "
                    f"Een badkamer van 6 m² komt op {bt(r100(T_MC))}. Met vergelijking met tegels."),
    "dienst": "tegelwerk-badkamer",
    "van": MC_WAND[0], "tot": MC_DOUCHE[1], "eenheid": "per m², inclusief materiaal, arbeid en btw",
    "snel": (f"Microcement, ook wel beton ciré genoemd, kost in de badkamer meestal <strong>€{MC_WAND[0]} tot €{MC_DOUCHE[1]} per m²</strong>, "
             "inclusief materiaal, arbeid en 21% btw. Op een wand buiten de douche zit je aan de onderkant, in de douche aan de bovenkant. "
             f"Een badkamer van 6 m² met wanden tot het plafond en de vloer (25 m²) kost zo'n {bt(r100(T_MC))}, inclusief voorbereiding "
             f"en een waterdichte laag in de douche. Per m² is dat duurder dan gewone tegels ({bt(T_MC_TEGEL)} voor dezelfde 25 m² aan "
             "tegels, legloon en lijm). Je bespaart wel vaak de sloop, omdat microcement over vaste tegels kan."),
    "varianten": [
        ("Wand buiten de douche", *MC_WAND, "Werkspot en Slimster. Minder belasting, dus aan de onderkant."),
        ("Vloer", *MC_VLOER, "Homedeal. Een vloer vraagt meer lagen en een slijtvaste sealer."),
        ("Douche (wand en vloer)", *MC_DOUCHE, "Homedeal. Meer lagen en een extra afdichting; de waterdichte laag eronder komt erbij."),
    ],
    "varianten_eenheid": "Per m², inclusief materiaal, arbeid en btw",
    "varianten_noot": "Bedragen van Werkspot, Homedeal en Slimster, dezelfde als op de pagina over het materiaal microcement.",
    "factoren": [
        ("De ondergrond", "Microcement is maar 2 tot 3 mm dik. Elke oneffenheid zie je terug. Over oude tegels moeten de voegen eerst worden uitgevlakt en er komt een primer op."),
        ("Douche of droge wand", "In de douche zijn meer lagen en een betere sealer nodig, en eronder een waterdichte laag. Daarom kost de douche per m² het meest."),
        ("Het aantal lagen en de sealer", "Goedkoop microcement heeft minder lagen of een zwakkere sealer. Vraag hoeveel lagen er komen en welke sealer, en hoe vaak die later opnieuw moet."),
        ("De vakman", "Microcement is handwerk. Het verschil tussen een mooie, rustige wolk en vlekken zit in de ervaring van de verwerker. Ervaren verwerkers zijn duurder, maar het herstellen van slecht werk is nog duurder."),
        ("Nissen, randen en hoeken", "Een nis in de douche of een ingebouwd meubel kost extra werk, maar zonder tegelprofielen. Dat is juist een voordeel van microcement."),
    ],
    "voorbeeld_titel": "Voorbeeld: badkamer van 6 m² in microcement, over de oude tegels",
    "voorbeeld": (
        "Stel: een badkamer van 2 bij 3 meter met tegels die nog vast zitten. Wanden tot het plafond (19 m², waarvan 6 m² in de douche) en de vloer "
        "(6 m²) krijgen microcement. De douchehoek krijgt eerst een waterdichte laag. Toilet en meubel gaan los en weer vast.",
        _MC,
        EIGEN5 + " Voorbereiding en het los- en vastzetten van sanitair zijn een eigen inschatting.",
    ),
    "voorbeelden": [
        ("Vergelijking: dezelfde 25 m² in tegels",
         "Wat kost alleen de afwerking? Hieronder tegels uit het middensegment met legloon, tegenover dezelfde oppervlakte in microcement. "
         "Voorbereiding, waterdicht maken en sanitair los en vast heb je in beide gevallen.",
         _MC_TEGEL, f"Ter vergelijking: alleen het microcement op dezelfde 25 m² kost {bt(T_MC_ALLEEN)}. Eigen rekensom met de bedragen op deze pagina."),
    ],
    "btw_extra": "Wij rekenen op deze pagina met 21%. Valt een deel van het werk volgens het bedrijf onder het 9%-tarief, dan hoort dat apart op de offerte te staan. Vraag bij twijfel hoe zij de btw berekenen.",
    "besparen": [
        "Laat het over de oude tegels aanbrengen als die vast en vlak zitten. Dat scheelt sloop en afvoer.",
        "Combineer: microcement op de wanden buiten de douche en tegels in de douche. Je houdt het naadloze beeld met minder risico.",
        "Kies een standaardkleur uit de collectie. Een eigen kleur kost soms extra.",
        "Vraag naar het onderhoud: een goede sealer gaat langer mee en scheelt later kosten.",
    ],
    "specialist": ("Microcement is werk voor een gespecialiseerde verwerker, niet voor een gewone stukadoor of doe-het-zelver. Vraag naar foto's van "
                   "eerdere badkamers, het aantal lagen, de sealer en de garantie. In de douche moet er altijd een waterdichte laag onder."),
    "opbouw_intro": "Microcement wordt per m² geprijsd, maar er komen een paar posten bij. Per post zie je de richtprijs en de bron.",
    "opbouw": [
        ("Microcement wand", (MC_WAND[0], MC_WAND[1], "per m²"), "Buiten de douche, inclusief materiaal en sealer.", ["werkspot_microcement", "slimster_microcement"]),
        ("Microcement vloer", (MC_VLOER[0], MC_VLOER[1], "per m²"), "Meer lagen en een slijtvaste sealer.", ["homedeal_microcement"]),
        ("Microcement douche", (MC_DOUCHE[0], MC_DOUCHE[1], "per m²"), "Wand en vloer in de douche.", ["homedeal_microcement"]),
        ("Primer en egaliseren", (EGALISEREN_M2[0], EGALISEREN_M2[1], "per m²"), "Voegen uitvlakken en hechtlaag over oude tegels.", ["eigen"]),
        ("Waterdicht maken", "waterdicht", "Waterdichte laag met kimband onder het microcement in de douche.", None),
        ("Kitwerk", "kitwerk_badkamer", "Naden bij bad, douche en sanitair.", None),
    ],
    "spijt": {
        "intro": "Microcement is mooi, maar vergeeft weinig. Hier wel en niet op besparen.",
        "wel": [
            ("Sloop.", "Over vaste tegels heen scheelt sloop en afvoer."),
            ("Alleen de wanden.", "Een tegelvloer en microcement op de wanden is goedkoper en sterker."),
        ],
        "niet": [
            ("Waterdichte laag in de douche.", f"Kost {rb('waterdicht')}. Microcement zelf is niet waterdicht."),
            ("De verwerker.", "Kies op ervaring en eerder werk, niet op de laagste m²-prijs."),
            ("De sealer.", "Een goedkope sealer slijt snel en laat vlekken toe."),
        ],
    },
    "valkuilen": [
        ("Geen waterdichte laag in de douche", "Staat er alleen 'microcement douche', vraag dan wat eronder komt. Zonder afdichting kan water via haarscheurtjes in de muur komen."),
        ("Aantal lagen en sealer niet genoemd", "Vraag hoeveel lagen, welk merk en welke sealer. Anders vergelijk je ongelijke offertes."),
        ("Voorbereiding apart", f"Egaliseren en primer ({bt(EGALISEREN_M2)} per m², eigen inschatting) staat soms niet in de m²-prijs."),
        VALK_BTW,
    ],
    "faqs": [
        ("Wat is het verschil tussen microcement en beton ciré?", "In de praktijk niets: het zijn twee namen voor een dunne, naadloze cementlaag met kunsthars. Leveranciers gebruiken de namen door elkaar."),
        ("Is microcement duurder dan tegels?", f"Per m² meestal wel. Voor 25 m²: tegels met legloon {bt(T_MC_TEGEL)}, microcement {bt(T_MC_ALLEEN)}. Je bespaart wel sloop als het over de oude tegels kan."),
        ("Is microcement waterdicht?", "Niet vanzelf. De sealer maakt het waterafstotend. In de douche hoort er een waterdichte laag onder."),
        ("Kan microcement over tegels?", "Ja, als de tegels vast en vlak zitten. De voegen worden eerst uitgevlakt en er komt een primer op."),
        ("Hoe lang gaat microcement mee?", "Bij goed aanbrengen en onderhoud vele jaren. De sealer moet af en toe worden vernieuwd, vooral op de vloer en in de douche."),
        ("Hoe onderhoud je microcement?", "Met een milde zeep, zonder schuurmiddel of agressieve ontkalker. Lees meer op de pagina over <a href=\"/materialen/microcement/\">het materiaal microcement</a>."),
    ],
    "bronnen": ["werkspot_microcement", "homedeal_microcement", "slimster_microcement", "trustoo_tegel", "werkspot_tegel", "werkspot_kit", "btw"],
    "verwant": ["tegels-over-tegels", "tegelzetter-per-m2", "luxe-badkamer", "nieuwe-badkamer"],
    "kennis": [("/materialen/microcement/", "Microcement: eigenschappen en onderhoud"),
               ("/kennisbank/microcement-badkamer/", "Microcement in de badkamer"),
               ("/kennisbank/badkamer-zonder-tegels/", "Een badkamer zonder tegels: kan dat?")],
})


# ---------------------------------------------------------------- goedkope-badkamer
def _goedkoop(zelf_slopen):
    sloop = ([("Zelf slopen, container huren (niet bij asbest)", rp("container"))] if zelf_slopen else
             [("Slopen door het bedrijf (4 m²)", som(rp("sloop_vast"), rp("sloop_m2", 4))), ("Afvoer van het sloopafval", rp("afval"))])
    return sloop + [
        ("Leidingwerk water en afvoer, op dezelfde plek", rp("leidingwerk")),
        (f"Tegels (basis), 12 m² × {bt(niv('tegels', 'basis'))}: vloer en douchehoek", mx(niv("tegels", "basis"), 12)),
        (f"Legloon, 12 m² × {rb('tegelwerk')}", rp("tegelwerk", 12)),
        ("Lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 12)),
        ("Waterdicht maken van de douchehoek", rp("waterdicht")),
        ("Sanitair (basis): douche met wand, toilet, meubel", SANI_BASIS),
        ("Montage van douche, toilet en meubel", MONTAGE_3),
        ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
        ("Totaal, inclusief btw", TOTAAL),
    ]


_GK_ZELF, _GK_BEDRIJF = _goedkoop(True), _goedkoop(False)
T_GK_ZELF, T_GK_BEDRIJF = tot(_GK_ZELF), tot(_GK_BEDRIJF)

KOSTEN4.append({
    "slug": "goedkope-badkamer",
    "kort": "Goedkope badkamer",
    "omschrijving": "Wat een nieuwe badkamer met een klein budget kost, en waar je veilig op bespaart.",
    "h1": f"Wat kost een goedkope badkamer in {JAAR}?",
    "title": f"Goedkope badkamer {JAAR}: wat kost een budgetbadkamer?",
    "description": (f"Een goedkope nieuwe badkamer kost zo'n {bt(r100(T_GK_ZELF))} incl. btw. Lees waar je veilig op bespaart, "
                    "waar niet, en wanneer opknappen slimmer is."),
    "dienst": "badkamer-renoveren",
    "van": r100(T_GK_ZELF)[0], "tot": r100(T_GK_BEDRIJF)[1], "eenheid": "per kleine badkamer van zo'n 4 m² met basissanitair, inclusief btw",
    "snel": (f"Een nieuwe badkamer met een klein budget kost meestal <strong>{bt((r100(T_GK_ZELF)[0], r100(T_GK_BEDRIJF)[1]))}</strong>, "
             "inclusief 21% btw. Dat is een badkamer van zo'n 4 m² waarin alles op dezelfde plek blijft, met basissanitair en tegels alleen op "
             f"de vloer en in de douchehoek. Sloop je zelf, dan zit je rond {bt(r100(T_GK_ZELF))}. Slimster noemt voor een budgetbadkamer "
             "€3.000 tot €7.000. Zitten je tegels en leidingen nog goed, dan is <a href=\"/kosten/badkamer-opknappen/\">opknappen</a> "
             "voor €750 tot €4.000 vaak de goedkoopste weg."),
    "varianten": [
        ("Opknappen in plaats van vernieuwen", 750, 4000, "Kit, voegen, kraan, meubel en douchewand vervangen. Geen sloop."),
        ("Budgetbadkamer, zelf slopen", *r100(T_GK_ZELF), "Zelf slopen met een container, alles op dezelfde plek, basissanitair."),
        ("Budgetbadkamer, alles uitbesteed", *r100(T_GK_BEDRIJF), "Zelfde badkamer, maar het bedrijf sloopt en voert af."),
    ],
    "varianten_eenheid": "Totaalprijs per badkamer, inclusief materiaal, arbeid en btw",
    "varianten_noot": "De bovenste rij komt van de pagina badkamer opknappen. De andere twee zijn eigen rekenvoorbeelden met de richtprijzen per post; Slimster noemt voor een budgetbadkamer €3.000 – €7.000.",
    "factoren": [
        ("Alles op dezelfde plek", f"Verplaatsen kost {rb('leidingwerk_verplaatsen')} extra. Bij een klein budget is dat de eerste post om te schrappen."),
        ("Hoeveel je tegelt", "Tegels op de vloer en in de douchehoek, en de andere wanden vochtbestendig stucen of verven, scheelt de helft van het tegelwerk."),
        ("Basissanitair", f"Een basisset (douche met wand, toilet, meubel) kost {bt(SANI_BASIS)}, tegen {bt(SANI_MIDDEN)} in het middensegment."),
        ("Zelf doen", f"Zelf slopen scheelt {bt((T_GK_BEDRIJF[0] - T_GK_ZELF[0], T_GK_BEDRIJF[1] - T_GK_ZELF[1]))}. Overleg het vooraf met het bedrijf, en sloop nooit zelf als er asbest kan zitten."),
        ("De leidingen", "Zijn de leidingen nog goed, dan kan het leidingwerk beperkt blijven. Dat ziet een loodgieter bij een bezoek."),
    ],
    "voorbeeld_titel": "Voorbeeld: budgetbadkamer van 4 m², zelf slopen",
    "voorbeeld": (
        "Stel: een badkamer van 2 bij 2 meter. Je sloopt zelf en huurt een container. Alles blijft op dezelfde plek. Tegels alleen op de vloer en in "
        "de douchehoek (12 m²), de rest van de wanden verf je zelf met vochtbestendige verf. Basissanitair.",
        _GK_ZELF,
        EIGEN5 + " Zelf verven en eventueel elektra zijn niet meegerekend.",
    ),
    "voorbeelden": [
        ("Zelfde badkamer, alles uitbesteed",
         "Nu sloopt en voert het bedrijf af. De rest blijft gelijk.",
         _GK_BEDRIJF, EIGEN5),
    ],
    "btw_extra": "Laat je de wanden boven de tegels stukadoren of verven door een vakman in een woning ouder dan twee jaar, dan kan dat arbeidsloon onder 9% vallen.",
    "besparen": [
        "Houd toilet, douche en wastafel op hun plek.",
        "Tegel alleen de vloer en de douchehoek. Verf de rest met vochtbestendige verf.",
        "Kies basissanitair in standaardmaten en een vaste glazen wand.",
        "Sloop zelf, maar alleen na overleg en nooit bij mogelijk asbest (huizen van vóór 1994).",
        "Vraag drie offertes met dezelfde posten en vergelijk ze in de <a href=\"/tools/offertechecker/\">offertechecker</a>.",
    ],
    "specialist": ("Ook een goedkope badkamer moet waterdicht zijn. Het leidingwerk, het waterdicht maken en het tegelen in de douche laat je door een "
                   "vakman doen. Zelf slopen, verven en accessoires ophangen kan prima. Lees bij twijfel over asbest eerst de "
                   "<a href=\"/kennisbank/asbest-in-badkamer/\">uitleg over asbest in de badkamer</a>."),
    "opbouw_intro": "Bij een budgetbadkamer betaal je dezelfde posten als bij elke badkamer, maar je kiest bij elke post de goedkope kant. Per post zie je de richtprijs en de bron.",
    "opbouw": [
        ("Container (zelf slopen)", "container", "Alleen een container huren, als je zelf sloopt.", None),
    ] + OPB_SLOOP[:1] + OPB_SLOOP[2:] + OPB_LEIDING[:1] + OPB_TEGEL + [
        ("Sanitair basis: douche", (niv("sanitair_douche", "basis")[0], niv("sanitair_douche", "basis")[1], "per stuk"), "Bak of goot, wand en kraan.", ["trustoo_badkamer", "homedeal_douche"]),
        ("Sanitair basis: toilet", (niv("sanitair_toilet", "basis")[0], niv("sanitair_toilet", "basis")[1], "per stuk"), "Staand toilet.", ["trustoo_badkamer", "homedeal_toilet"]),
        ("Sanitair basis: meubel", (niv("sanitair_meubel", "basis")[0], niv("sanitair_meubel", "basis")[1], "per stuk"), "Meubel met wastafel, kraan en spiegel.", ["trustoo_badkamer"]),
    ] + OPB_SANITAIR[1:] + OPB_AFWERKING[:1],
    "spijt": {
        "intro": "Een goedkope badkamer hoeft geen spijtbadkamer te zijn. Het verschil zit in waar je bespaart.",
        "wel": [
            ("Indeling.", f"Alles op dezelfde plek scheelt {rb('leidingwerk_verplaatsen')}."),
            ("Tegels.", f"Basistegels ({bt(niv('tegels', 'basis'))} per m²) in een standaardformaat zien er strak uit."),
            ("Sanitair.", f"Basissanitair ({bt(SANI_BASIS)}) werkt net zo goed als duur sanitair."),
            ("Sloopwerk.", f"Zelf slopen scheelt {bt((T_GK_BEDRIJF[0] - T_GK_ZELF[0], T_GK_BEDRIJF[1] - T_GK_ZELF[1]))}, als er geen asbest is."),
        ],
        "niet": [
            ("Waterdicht maken.", f"Kost {rb('waterdicht')}. Lekkage maakt een goedkope badkamer heel duur."),
            ("Een vakman voor leidingen en douche.", "Fouten zie je pas later, als het water in de vloer of bij de buren zit."),
            ("Ventilatie.", f"Een ventilator ({rb('ventilator')}) voorkomt schimmel in een nieuwe badkamer."),
            ("De kraan.", "Een goedkope kraan die gaat lekken of druppelen kost je meer. Kies een bekend merk met onderdelen."),
        ],
    },
    "valkuilen": [
        ("Een 'complete badkamer' voor een vaste lage prijs", "Lees wat erin zit. Vaak zijn sloop, afvoer, leidingwerk of waterdicht maken niet inbegrepen, of is het sanitair een heel lage stelpost."),
        VALK_STELPOST, VALK_PUIN, VALK_WATERDICHT, VALK_MEERWERK, VALK_BTW, VALK_BETALING,
    ],
    "faqs": [
        ("Wat is de goedkoopste manier om een badkamer te vernieuwen?", "Alles op dezelfde plek, zelf slopen, tegels alleen op de vloer en in de douche, en basissanitair. Zijn tegels en leidingen nog goed, dan is opknappen goedkoper dan vernieuwen."),
        ("Kan een nieuwe badkamer voor €5.000?", f"Een kleine badkamer met basissanitair kan, vooral als je zelf sloopt: ons voorbeeld komt uit op {bt(r100(T_GK_ZELF))}. Met een grotere ruimte of extra wensen wordt het meer."),
        ("Is een badkamer van een webshop goedkoper?", "Het sanitair kan goedkoper zijn, maar de montage, het tegelwerk en het leidingwerk blijven. Overleg met het bedrijf of ze zelf gekocht sanitair willen plaatsen en of er dan garantie op zit."),
        ("Kan ik zelf tegelen om te besparen?", "Op een droge wand kan dat. De vloer en de douchehoek laat je beter een tegelzetter doen: afschot en waterdicht maken luisteren nauw."),
        ("Moet ik dan ook offertes vergelijken?", "Juist dan. Bij een klein budget telt elke post. Vraag drie offertes met dezelfde posten."),
        ("Is er subsidie voor een nieuwe badkamer?", "Voor een gewone badkamer niet. Voor aanpassingen vanwege een beperking kan de gemeente soms helpen via de Wmo. Vraag het bij je gemeente."),
    ],
    "bronnen": ["slimster_badkamer", "trustoo_badkamer", "homedeal_badkamer", "werkspot_puin", "slimster_slopen", "werkspot_tegel", "btw", "asbest"],
    "verwant": ["badkamer-opknappen", "kleine-badkamer", "nieuwe-badkamer", "badkamer-slopen"],
    "kennis": [("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer: waar let je op?"),
               ("/kennisbank/badkamer-zonder-tegels/", "Een badkamer zonder tegels: kan dat?"),
               ("/kennisbank/volgorde-badkamerrenovatie/", "In welke volgorde gaat een badkamerrenovatie?")],
})

# Nieuwe pagina's ook vanaf de vijf hoofdpagina's bereikbaar maken.
EXTRA["nieuwe-badkamer"]["verwant"] = ["badkamer-slopen", "tegelzetter-per-m2", "inloopdouche", "kleine-badkamer", "luxe-badkamer",
                                       "goedkope-badkamer", "badkamer-verplaatsen"]
