# -*- coding: utf-8 -*-
"""Metadata van de voor-en-na-renders (renders/b5-*.html, uitvoer in fotos/renders/).

Per paar twee 3D-illustraties van dezelfde ruimte, vanuit exact dezelfde camerahoek en met dezelfde
afmetingen: eerst gedateerd (jaren 80/90), daarna gerenoveerd. Bestandsnamen: b5-<scene>-voor en
b5-<scene>-na, elk op 400, 800 en 1600 px breed (3:2). Op de site staat er altijd bij dat het een
illustratie is en geen echt project.

Richtprijzen (incl. 21% btw), dezelfde bandbreedtes als op de kostenpagina's van de site, geraadpleegd
november 2026:
- Bad vervangen door een inloopdouche met tegelvloer: €2.500 – €5.000 (zoals /kosten/bad-vervangen-door-douche/;
  eigen inschatting op basis van Homedeal, nieuwe douche kosten, en Trustoo, losse posten badkamerrenovatie).
- Toiletruimte compleet met voorzetwand: €4.000 – €6.500; hele range €2.500 – €6.500 (zoals /kosten/toilet-renoveren/;
  Homedeal, toilet verbouwen kosten, en Werkspot, toiletruimte verbouwen).
- Zolderbadkamer vernieuwen waar de leidingen al liggen: €8.000 – €15.000 (zoals /kosten/badkamer-op-zolder/,
  variant "eenvoudig"; Homedeal en Trustoo, badkamer renoveren).
- Gezinsbadkamer compleet, midden tot luxe: €7.000 – €20.000 (zoals /kosten/nieuwe-badkamer/, niveaus midden en luxe;
  Slimster en Homedeal). Dubbel wastafelmeubel: sanitair_meubel (midden – luxe €500 – €2.500) en montage_meubel
  (€200 – €600) uit richtprijzen.py.
"""

import richtprijzen as RP

_BIJ = "Illustratie (3D-render), geen echt project"
_W, _H = 1600, 1067


def _eur(n):
    return f"€{int(n):,}".replace(",", ".")


def _bron(sleutel):
    return RP.BRONNEN[sleutel]


def _r(naam, alt, bijschrift):
    return {"naam": naam, "alt": alt, "w": _W, "h": _H, "bijschrift": f"{_BIJ}: {bijschrift}"}


_meubel = RP.RICHTPRIJZEN["sanitair_meubel"]["niveaus"]
_montage_meubel = RP.lh("montage_meubel")

PAREN = [
    {
        "slug": "kleine-badkamer",
        "titel": "Kleine badkamer: van bad naar inloopdouche",
        "kort": "Kleine badkamer",
        "maat": "1,8 × 2,3 meter",
        "intro": "Een smalle badkamer met een ingebouwd bad over de hele breedte. Het bad wordt bijna nooit gebruikt, "
                 "het douchegordijn plakt en de tegels zijn van rond 1985. Op dezelfde plek komt een inloopdouche.",
        "voor": _r("b5-kleine-badkamer-voor",
                   "Illustratie van een gedateerde kleine badkamer: beige gevlekte tegels met een bruine sierstrook met bloemen, "
                   "een ingebouwd beige bad met een gestreept douchegordijn, bruine vloertegels, een wastafel op een zuil "
                   "en een tl-buis boven de spiegel",
                   "kleine badkamer vóór de renovatie, met bad en douchegordijn."),
        "na": _r("b5-kleine-badkamer-na",
                 "Illustratie van dezelfde kleine badkamer na de renovatie: een inloopdouche met glazen wand op de plek van het bad, "
                 "smalle groene wandtegels met een nis, grote lichte tegels, een zwevend eiken meubel met spiegel, "
                 "mat zwarte kranen en een handdoekradiator",
                 "dezelfde kleine badkamer met een inloopdouche op de plek van het bad."),
        "veranderd": [
            "Het bad is eruit. Op dezelfde plek ligt een inloopdouche met een goot langs de achterwand en een glazen wand.",
            "De douchevloer loopt op afschot naar de goot en is eerst waterdicht gemaakt. Er is geen drempel meer.",
            "Een nis in de achterwand vervangt het rekje met flessen op de badrand.",
            "Grote tegels (30 × 60 en 60 × 60 cm) geven minder voegen dan de oude tegels van 15 × 15 cm.",
            "De wastafel op een zuil is een zwevend meubel met lades. De vloer eronder blijft vrij, dat maakt schoonmaken makkelijker.",
            "Spots in het plafond in plaats van een tl-buis en een bollamp, en een handdoekradiator.",
        ],
        "prijs": {"laag": 2500, "hoog": 5000,
                  "wat": "Bad eruit, inloopdouche met tegelvloer op dezelfde plek",
                  "extra": "Komt er ook nieuw tegelwerk op alle wanden en een nieuw meubel bij, zoals in de illustratie, "
                           "dan ben je eerder bezig met een complete kleine badkamer. Reken dan op €3.500 tot €12.000.",
                  "bron": [_bron("homedeal_douche"), _bron("trustoo_badkamer")]},
        "link": ("/kosten/bad-vervangen-door-douche/", "Wat kost een bad vervangen door een douche?"),
        "links": [("/diensten/inloopdouche-plaatsen/", "Inloopdouche laten plaatsen"),
                  ("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel")],
    },
    {
        "slug": "toiletruimte",
        "titel": "Toiletruimte met fonteintje",
        "kort": "Toiletruimte",
        "maat": "1,0 × 1,6 meter",
        "intro": "Een klein toilet met bruine tegels tot borsthoogte, geel behang erboven en een staand toilet met een "
                 "reservoir erop. In de nieuwe versie hangt het toilet aan een voorzetwand en is er een echte fontein.",
        "voor": _r("b5-toiletruimte-voor",
                   "Illustratie van een gedateerde toiletruimte: bruine tegels tot 1,5 meter met een strook ruitjestegels, "
                   "geel gestreept behang, een houten afwerklat, een staand beige toilet met reservoir en een zichtbare leiding",
                   "toiletruimte vóór de renovatie, met staand toilet en bruine tegels."),
        "na": _r("b5-toiletruimte-na",
                 "Illustratie van dezelfde toiletruimte na de renovatie: donkergroene staande tegels op de achterwand, "
                 "een hangtoilet in een voorzetwand met een eiken plank, een zwarte bedieningsplaat, een fontein op een eiken plank, "
                 "een ronde spiegel en een lichte terrazzovloer",
                 "dezelfde toiletruimte met hangtoilet, voorzetwand en fontein."),
        "veranderd": [
            "Het staande toilet met reservoir is vervangen door een hangtoilet. Het reservoir zit nu in een voorzetwand.",
            "Op de voorzetwand ligt een eiken plank. Daar is plek voor een plant of een extra rol.",
            "Leidingen zitten weggewerkt in de wand. Geen losse buizen meer langs het toilet.",
            "De oude fonteinkom met één kraan is een strakke fontein op een plank, met een kraan uit de wand.",
            "Eén donkere tegelwand als accent, de andere wanden licht gestuct. Zo voelt de ruimte niet kleiner.",
            "Een lichte vloer zonder brede voegen. Onder een hangtoilet kun je de vloer in één keer dweilen.",
        ],
        "prijs": {"laag": 4000, "hoog": 6500,
                  "wat": "Complete toiletruimte met voorzetwand en hangtoilet",
                  "extra": "Een eenvoudigere renovatie, met nieuwe tegels en een staand toilet op dezelfde plek, kost meestal "
                           "€2.500 tot €4.000. Alleen het toilet vervangen kost €300 tot €700 aan werk.",
                  "bron": [_bron("homedeal_toilet"), _bron("werkspot_toilet")]},
        "link": ("/kosten/toilet-renoveren/", "Wat kost een toilet renoveren?"),
        "links": [("/diensten/toilet-renoveren/", "Toilet laten renoveren"),
                  ("/badkamerspullen/toilet-kiezen/", "Toilet kiezen: hangend of staand")],
    },
    {
        "slug": "zolderbadkamer",
        "titel": "Zolderbadkamer onder een schuin dak",
        "kort": "Zolderbadkamer",
        "maat": "2,8 × 2,4 meter, knieschot 1 meter",
        "intro": "Een badkamer op zolder uit de jaren 80: grenen schrootjes tegen het dak, een douchecabine met kunststof "
                 "panelen en een bad onder de schuinte. Bij de renovatie blijft de indeling grotendeels gelijk.",
        "voor": _r("b5-zolderbadkamer-voor",
                   "Illustratie van een gedateerde zolderbadkamer: grenen schrootjes op het schuine dak, een douchecabine met "
                   "beige kunststof panelen in een aluminium profiel, een ingebouwd beige bad onder de schuinte, "
                   "een wastafel op een zuil met spiegelkastje en tl-buis",
                   "zolderbadkamer vóór de renovatie, met schrootjes en een douchecabine."),
        "na": _r("b5-zolderbadkamer-na",
                 "Illustratie van dezelfde zolderbadkamer na de renovatie: een wit gestuct schuin dak met dakraam, "
                 "een inloopdouche met glaswand in zwart profiel en lichte handgemaakte tegels, een vrijstaand bad onder "
                 "het dakraam, een zwevend eiken meubel met ronde kom, messing kranen en een vloer in houtlook",
                 "dezelfde zolderbadkamer met inloopdouche, vrijstaand bad en een gestuct dak."),
        "veranderd": [
            "De douchecabine met verhoogde bak is een inloopdouche op vloerniveau, met een glazen wand.",
            "Het ingebouwde bad is een vrijstaand bad. Onder de schuinte staat het op de plek waar je toch niet rechtop staat.",
            "De schrootjes zijn weg. Het dak is geïsoleerd, afgewerkt met gipsplaat en gestuct.",
            "Lichte tegels in de douchehoek en verf op de andere wanden: de ruimte lijkt groter en lichter.",
            "Een zwevend meubel met opzetkom, een ronde spiegel en wandlampjes in plaats van een tl-buis.",
            "Een vloer in houtlook (keramisch), die goed tegen water kan.",
        ],
        "prijs": {"laag": 8000, "hoog": 15000,
                  "wat": "Zolderbadkamer vernieuwen waar water en afvoer al liggen",
                  "extra": "Moet er constructief werk gebeuren, of komen de leidingen nieuw naar boven, dan kan het oplopen "
                           "tot €20.000 à €35.000. Een dakraam of dakkapel komt daar nog bij.",
                  "bron": [_bron("homedeal_badkamer"), _bron("trustoo_badkamer")]},
        "link": ("/kosten/badkamer-op-zolder/", "Wat kost een badkamer op zolder?"),
        "links": [("/kennisbank/badkamer-op-zolder/", "Badkamer op zolder: waar let je op?"),
                  ("/kennisbank/badkamer-ventilatie/", "Ventilatie in de badkamer")],
    },
    {
        "slug": "gezinsbadkamer",
        "titel": "Gezinsbadkamer met dubbele wastafel",
        "kort": "Gezinsbadkamer",
        "maat": "3,0 × 2,7 meter",
        "intro": "Een badkamer voor een gezin met één wastafel, een bad met douchegordijn en een staand toilet. Elke ochtend "
                 "staat er een rij. Bij de renovatie komt er een dubbel meubel en wordt het bad ook een fijne douche.",
        "voor": _r("b5-gezinsbadkamer-voor",
                   "Illustratie van een gedateerde gezinsbadkamer: crème tegels met een bruine strook, roodbruine vloertegels, "
                   "een ingebouwd beige bad met douchegordijn, een staand toilet met reservoir, één wastafel op een zuil "
                   "met spiegelkast en tl-buis, en een raam met bruin kozijn",
                   "gezinsbadkamer vóór de renovatie, met één wastafel en een bad met gordijn."),
        "na": _r("b5-gezinsbadkamer-na",
                 "Illustratie van dezelfde gezinsbadkamer na de renovatie: grote tegels in marmerlook op de achterwand, "
                 "een bad met glazen badwand en regendouche, een hangtoilet in een voorzetwand met plank, "
                 "een dubbel eiken wastafelmeubel van 140 cm met twee kommen en een lange spiegel",
                 "dezelfde gezinsbadkamer met een dubbel wastafelmeubel en een bad met regendouche."),
        "veranderd": [
            "Eén wastafel is een dubbel meubel van 140 cm geworden, met twee kommen, twee kranen en lades.",
            "Een lange spiegel over de hele breedte vervangt het spiegelkastje met tl-buis.",
            "Het bad blijft, maar met een glazen badwand en een regendouche. Zo is het bad ook een volwaardige douche.",
            "Het staande toilet is een hangtoilet in een voorzetwand, met een plank erboven.",
            "De achterwand heeft grote tegels in marmerlook, de andere wanden lichte tegels van 30 × 60 cm.",
            "Een handdoekradiator naast het raam en spots in het plafond.",
        ],
        "prijs": {"laag": 7000, "hoog": 20000,
                  "wat": "Complete badkamer van deze grootte, midden tot luxe",
                  "extra": f"Alleen het dubbele meubel kost {_eur(_meubel['midden'][0])} tot {_eur(_meubel['luxe'][1])}, "
                           f"plus {_eur(_montage_meubel[0])} tot {_eur(_montage_meubel[1])} voor het ophangen en aansluiten. "
                           "Voor een tweede kraan moet er wel een extra wateraansluiting en afvoer komen.",
                  "bron": [_bron("slimster_badkamer"), _bron("homedeal_badkamer"), _bron("trustoo_badkamer")]},
        "link": ("/kosten/nieuwe-badkamer/", "Wat kost een nieuwe badkamer?"),
        "links": [("/diensten/badkamer-renoveren/", "Badkamer laten renoveren"),
                  ("/badkamerspullen/wastafelmeubel-kiezen/", "Wastafelmeubel kiezen")],
    },
]

PAAR_BY_SLUG = {p["slug"]: p for p in PAREN}
