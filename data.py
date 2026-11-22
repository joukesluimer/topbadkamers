# -*- coding: utf-8 -*-
"""
Contentmodel voor Top-badkamers.nl
Alles wat je aanpast in dit bestand rolt automatisch door de hele site.
"""

SITE = {
    "naam": "Top Badkamers",
    # Tijdelijk op het gratis GitHub-adres. Het domein top-badkamers.nl komt later:
    # vul het dan hier in ("domein" leeg = geen CNAME) en zet "url" erop.
    "domein": "",
    "url": "https://joukesluimer.github.io/topbadkamers",
    "tagline": "Vergelijk badkamerspecialisten bij jou in de buurt",
    "email": "joukesluimer@hotmail.com",
    "telefoon": "085 - 000 00 00",
    "kvk": "97150975",
    "btw": "",  # <- vul hier je btw-id in zodra je die hebt; blijft verborgen zolang het leeg is
    "adres": "Zeewolde",
    "provincie_hq": "Flevoland",
    "oprichting": "2026",
}

# ---------------------------------------------------------------------------
# DIENSTEN
#
# Richtprijzen zijn inclusief 21% btw, tenzij er "excl. btw" bij staat. Het zijn
# bewust ruime bandbreedtes: de bronnen hieronder lopen onderling flink uiteen
# en geen enkele badkamer is hetzelfde. Bijstellen zodra er echte offertedata
# uit de eigen leads is. Bronnen, geraadpleegd in november 2026:
#
# - Homedeal, badkamer renoveren kosten (€3.500 – €15.000 voor ca. 9 m², vaak €5.000 – €8.000):
#   https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/
# - Trustoo, wat kost een nieuwe badkamer in 2026 (€8.500 – €15.000 voor 5 – 10 m²):
#   https://trustoo.nl/kosten/badkamer-renovatie-kosten/
# - Slimster, compleet nieuwe badkamer (budget €3.000 – €7.000, midden €7.500 – €11.000, luxe €11.000 – €15.000):
#   https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/
# - Werkspot, kosten badkamer verbouwen en inloopdouche (inloopdouche €1.500 – €5.000):
#   https://www.werkspot.nl/badkamer-plaatsen/prijzen-kosten
# - Bobex, inloopdouche (gemiddeld ca. €3.500 incl. plaatsing; Belgische bron, alleen ter controle):
#   https://www.bobex.be/nl-be/badkamerrenovatie/inloopdouche/
# - Trustoo en Homedeal, tegelzetter (legloon gemiddeld €25 – €40 per m², 8 – 10 m² per dag):
#   https://trustoo.nl/kosten/tegelzetter-kosten/ en https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter
# - Werkspot, badkamer betegelen (tegels €20 – €60 per m², totaal €25 – €100 per m²):
#   https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten
# - Homedeal en Werkspot, toilet verbouwen (basis €2.500 – €4.000, compleet €4.000 – €6.500;
#   alleen toilet vervangen incl. montage €300 – €700):
#   https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/ en https://www.werkspot.nl/toiletruimte-verbouwen/prijzen-kosten
# - Homedeal, loodgieter kosten (uurtarief €45 – €85 excl. btw, spoed hoger):
#   https://www.homedeal.nl/loodgieter/loodgieter-kosten/
# - Werkspot en Slimster, kitwerk badkamer (verwijderen + nieuw €6 – €11 per meter, starttarief €100 – €200,
#   hele badkamer afkitten €95 – €325): https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kitwerk
#   en https://slimster.nl/kitwerk/kosten-kitter/badkamer-kitten/
# - Btw: badkamerrenovatie, sanitair, tegelwerk en installatiewerk vallen onder 21%. Het 9%-tarief geldt
#   alleen voor specifieke werkzaamheden aan woningen ouder dan twee jaar: stukadoren, verfwerk en
#   behangen (werk en hulpmaterialen, niet het behang zelf), en bij isoleren alleen het arbeidsloon.
#   Sinds 1 juli 2025 alleen nog voor het woongedeelte van een gemengd pand.
#   https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/tarieven_en_vrijstellingen/diensten_9_btw
#   https://www.jongbloed-fiscaaljuristen.nl/databank/omzetbelasting/btw_werkzaamheden_woning/
#   https://www.taxlive.nl/nl/documenten/nieuws/handreiking-btw-tarief-werkzaamheden-aan-gemengde-panden-per-1-juli-2025/
# ---------------------------------------------------------------------------

DIENSTEN = [
    {
        "slug": "badkamer-renoveren",
        "seo_titel": "Badkamer renoveren: kosten en werkwijze",
        "naam": "Badkamer renoveren",
        "naam_kort": "Renoveren",
        "naam_lang": "Complete badkamerrenovatie",
        "kort": "Slopen, leidingwerk, tegelwerk en sanitair in één opdracht",
        "icon": "bad",
        "prijs_van": 6000,
        "prijs_tot": 18000,
        "prijs_eenheid": "per complete badkamer",
        "prijs_extra": "Dat is een middensegment-badkamer van 5 tot 9 m², inclusief sloopwerk, tegels, sanitair, montage en 21% btw. Een eenvoudige badkamer met basissanitair kan vanaf zo'n €3.500. Verplaats je de douche, het toilet of de afvoer, of kies je voor luxe sanitair en grote tegels, dan zit je al snel boven de €20.000.",
        "meta_title": "Badkamer renoveren: kosten & specialist vinden | {plaats}",
        "intro": (
            "Een complete badkamerrenovatie is een van de grotere klussen in huis. De badkamer "
            "wordt gesloopt tot op de ruwe vloer en muren, daarna komen er nieuwe leidingen, een "
            "waterdichte ondergrond, tegels en sanitair in. Het verschil tussen een badkamer die "
            "twintig jaar meegaat en een die na vijf jaar gaat lekken, zit vooral in wat je straks "
            "niet meer ziet: afschot, kimband, afdichting en leidingwerk."
        ),
        "wat": [
            "De oude badkamer slopen en het puin afvoeren",
            "Water- en afvoerleidingen vernieuwen of verleggen",
            "Elektra aanpassen: verlichting, stopcontacten, ventilatie en eventueel vloerverwarming",
            "Vloer en wanden waterdicht maken en op afschot brengen",
            "Wand- en vloertegels zetten",
            "Sanitair monteren: douche, bad, toilet, wastafelmeubel en kranen",
            "Kitwerk en afwerking, zoals een plafond of stucwerk",
        ],
        "werkwijze": [
            ("Opname en ontwerp", "De specialist meet de ruimte op, kijkt waar leidingen en afvoer lopen en bespreekt indeling, stijl en budget. Vaak hoort daar een tekening of 3D-ontwerp bij."),
            ("Slopen", "Tegels, sanitair en vaak ook de dekvloer gaan eruit. Pas dan zie je in welke staat leidingen en ondergrond zijn."),
            ("Leidingwerk en elektra", "Nieuwe water- en afvoerleidingen, aansluitingen op de juiste plek en de elektra voor verlichting, ventilatie en eventueel vloerverwarming."),
            ("Waterdicht maken en tegelen", "De vloer krijgt afschot naar de afvoer, naden en hoeken worden afgedicht en daarna volgt het tegelwerk."),
            ("Sanitair en oplevering", "Douche, toilet, meubel en kranen worden gemonteerd en aangesloten. Samen lopen jullie alles na, inclusief een lektest."),
        ],
        "prijsfactoren": [
            "De grootte van de badkamer en het aantal vierkante meters tegelwerk",
            "Of de indeling hetzelfde blijft of dat leidingen en afvoer verplaatst moeten worden",
            "Het niveau van het sanitair: een basisset of design-kranen, een hangtoilet en een inbouwdouche",
            "Het soort tegels: grote formaten en natuursteen kosten meer materiaal én meer arbeid",
            "Extra's zoals vloerverwarming, een inloopdouche zonder drempel of een vrijstaand bad",
            "Wat er bij het slopen tevoorschijn komt, zoals een rotte vloer of oude leidingen",
        ],
        "tips": [
            "Houd de indeling zo veel mogelijk gelijk. Toilet en afvoer op dezelfde plek laten scheelt al snel duizenden euro's.",
            "Vraag of het sanitair in de offerte zit of als stelpost is opgenomen. Een lage stelpost maakt een offerte goedkoper op papier, maar niet in werkelijkheid.",
            "Vraag hoe de vloer en wanden waterdicht worden gemaakt en welke garantie je daarop krijgt. Dat is het deel dat je later niet meer kunt controleren.",
        ],
        "faq": [
            ("Hoelang duurt een badkamerrenovatie?", "Voor een gemiddelde badkamer moet je rekenen op twee tot vier weken, afhankelijk van de grootte, droogtijden van de vloer en de levertijd van het sanitair. Vraag de specialist om een planning per dag."),
            ("Kan ik thuis blijven wonen tijdens de verbouwing?", "Meestal wel, maar je hebt een paar weken geen eigen douche. Heb je maar één toilet in huis, vraag dan of dat zo kort mogelijk buiten gebruik is."),
            ("Moet ik zelf het sanitair kopen?", "Dat mag, maar overleg het vooraf. Niet elke specialist geeft garantie op de montage van sanitair dat hij niet zelf levert, en met een verkeerd onderdeel loopt de planning uit."),
            ("Welk btw-tarief geldt voor een nieuwe badkamer?", "In principe 21%, voor zowel het werk als het materiaal. Alleen specifieke onderdelen zoals stukadoren of verven van het plafond in een woning ouder dan twee jaar kunnen onder 9% vallen. Een nette offerte benoemt die onderdelen apart."),
        ],
    },
    {
        "slug": "badkamer-installeren",
        "seo_titel": "Sanitair laten installeren: kosten en werkwijze",
        "naam": "Sanitair installeren",
        "naam_kort": "Installeren",
        "naam_lang": "Sanitair laten installeren",
        "kort": "Toilet, wastafel, kraan of douche laten plaatsen en aansluiten",
        "icon": "kraan",
        "prijs_van": 45,
        "prijs_tot": 85,
        "prijs_eenheid": "per uur excl. btw",
        "prijs_extra": "Kleine klussen gaan vaak voor een vaste prijs per klus. Een staand toilet vervangen kost inclusief montage zo'n €300 tot €700 aan werk, het toilet zelf niet meegerekend. Voorrijkosten en spoedtoeslagen komen er soms bij.",
        "meta_title": "Sanitair laten installeren: kosten & installateur | {plaats}",
        "intro": (
            "Niet elke badkamer hoeft helemaal opnieuw. Soms wil je alleen een nieuw toilet, een "
            "wastafelmeubel, een thermostaatkraan of een andere douche. Dan heb je een installateur "
            "nodig die het sanitair netjes plaatst en waterdicht aansluit, zonder dat de rest van "
            "de badkamer eruit hoeft."
        ),
        "wat": [
            "Een staand toilet of hangtoilet met inbouwreservoir plaatsen",
            "Wastafel of wastafelmeubel monteren en aansluiten",
            "Kranen vervangen, zoals een thermostaatkraan of regendouche",
            "Een douchebak, douchewand of douchecabine plaatsen",
            "Een bad plaatsen of vervangen",
            "Afvoer en wateraansluitingen aanpassen of vernieuwen",
        ],
        "werkwijze": [
            ("Opname", "De installateur kijkt naar de bestaande aansluitingen en of het nieuwe sanitair daarop past. Bij kleine klussen kan dat vaak met foto's."),
            ("Water afsluiten en demonteren", "Het oude sanitair gaat eraf, waarbij de installateur let op de staat van de leidingen en de afvoer."),
            ("Aansluiten", "Het nieuwe sanitair wordt geplaatst, waterpas gezet en aangesloten op water en afvoer."),
            ("Testen", "Water erop, alles nalopen op lekkage en de afvoer controleren."),
            ("Afwerken", "Kitnaden aanbrengen en het oude sanitair afvoeren, als dat is afgesproken."),
        ],
        "prijsfactoren": [
            "Het soort klus: een kraan vervangen is iets anders dan een hangtoilet met inbouwreservoir",
            "Of de aansluitingen op de goede plek zitten of verlegd moeten worden",
            "Of er tegelwerk open moet en weer dicht",
            "Wie het sanitair levert: de installateur of jij",
            "Voorrijkosten, en of je een vaste prijs of een uurtarief afspreekt",
        ],
        "tips": [
            "Combineer kleine klussen. Een toilet, een kraan en een nieuwe sifon in één bezoek scheelt voorrijkosten.",
            "Stuur foto's van de bestaande aansluitingen mee met je aanvraag. Dan krijg je een prijs die beter klopt.",
            "Vraag bij een uurtarief om een schatting van het aantal uren, zodat je niet voor verrassingen komt te staan.",
        ],
        "faq": [
            ("Kan een hangtoilet overal geplaatst worden?", "Vaak wel, maar er moet ruimte zijn voor een inbouwreservoir en een voorzetwand. Dat betekent meestal ook nieuw tegelwerk op die wand, waardoor het duurder is dan een staand toilet vervangen."),
            ("Moet ik zelf sanitair kopen?", "Dat kan, maar overleg het vooraf. Sommige installateurs geven geen garantie op onderdelen die ze niet zelf hebben geleverd."),
            ("Wat kost een installateur per uur?", "Gangbaar is ongeveer €45 tot €85 per uur exclusief btw. Bij spoed, 's avonds of in het weekend ligt het tarief hoger."),
            ("Welk btw-tarief geldt?", "Voor het installeren van sanitair geldt 21% btw, op het werk en op de materialen."),
        ],
    },
    {
        "slug": "tegelwerk-badkamer",
        "seo_titel": "Tegelwerk badkamer: kosten per m² en werkwijze",
        "naam": "Tegelwerk badkamer",
        "naam_kort": "Tegelwerk",
        "kort": "Wand- en vloertegels zetten, waterdicht en strak gevoegd",
        "icon": "tegels",
        "prijs_van": 25,
        "prijs_tot": 55,
        "prijs_eenheid": "per m² legloon",
        "prijs_extra": "Dat is alleen het zetten. Tegels kosten daarnaast grofweg €20 tot €60 per m² of meer. Kleine badkamers zijn per m² duurder dan grote, omdat er meer hoeken, randen en snijwerk zijn. Een tegelzetter legt in een badkamer gemiddeld 8 tot 10 m² per dag.",
        "meta_title": "Tegelzetter badkamer: kosten per m² | {plaats}",
        "intro": (
            "Tegelwerk bepaalt voor een groot deel hoe je badkamer eruitziet, maar ook of hij "
            "waterdicht blijft. Een goede tegelzetter begint niet met tegels, maar met de "
            "ondergrond: vlak, droog en op afschot. Daarna zie je het vakmanschap terug in rechte "
            "voegen, netjes gesneden hoeken en een douchevloer waar het water vanzelf wegloopt."
        ),
        "wat": [
            "Wandtegels zetten in de badkamer of toiletruimte",
            "Vloertegels leggen, met afschot naar de afvoer of douchegoot",
            "Oude tegels verwijderen en de ondergrond vlak maken",
            "Een waterdichte laag en kimband aanbrengen in de natte zone",
            "Grote formaten en natuursteen verwerken",
            "Voegen en kitwerk afwerken",
        ],
        "werkwijze": [
            ("Opmeten en tegels kiezen", "De tegelzetter meet de vierkante meters op, kijkt naar de ondergrond en adviseert over formaat en legpatroon."),
            ("Ondergrond voorbereiden", "Oude tegels eruit, wanden en vloer vlak maken en in de natte zone een waterdichte laag aanbrengen."),
            ("Indelen", "De tegels worden uitgezet, zodat je aan de zichtkant geen smalle reepjes krijgt."),
            ("Zetten en voegen", "Tegel voor tegel lijmen, na het uitharden voegen en de tegels schoonmaken."),
            ("Kitten", "Naden bij hoeken, bad, douchebak en vloer afkitten met sanitairkit."),
        ],
        "prijsfactoren": [
            "Het aantal vierkante meters en hoeveel snijwerk de ruimte vraagt",
            "Het formaat: grote tegels en heel kleine mozaïektegels kosten meer arbeid",
            "De staat van de ondergrond en of oude tegels eerst moeten worden verwijderd",
            "Of de vloer op afschot moet voor een inloopdouche of douchegoot",
            "Het materiaal: keramisch, natuursteen of terrazzo",
        ],
        "tips": [
            "Bestel ongeveer 10% extra tegels voor snijverlies en breuk, en bewaar een paar stuks voor later herstel.",
            "Vraag of de offerte alleen het legloon is of ook tegels, lijm, voegsel en kitwerk. Anders vergelijk je offertes die niet vergelijkbaar zijn.",
            "Kies bij een kleine badkamer niet automatisch kleine tegels. Grotere tegels geven minder voegen en een rustiger beeld.",
        ],
        "faq": [
            ("Kan er over bestaande tegels heen getegeld worden?", "Soms, als de oude tegels vast zitten en de ruimte niet te klein wordt. Vaak is verwijderen toch beter, omdat je dan ook de waterdichting onder de tegels kunt vernieuwen."),
            ("Hoelang duurt het tegelen van een badkamer?", "Een tegelzetter legt gemiddeld 8 tot 10 m² per dag. Voor een gemiddelde badkamer, met wanden en vloer, moet je rekenen op een paar dagen, plus droogtijd."),
            ("Wat kost een tegelzetter per uur?", "Gangbaar is ongeveer €30 tot €50 per uur, maar voor badkamers rekenen de meeste tegelzetters per m²."),
            ("Welk btw-tarief geldt voor tegelwerk?", "Voor tegelwerk geldt 21% btw, op het werk en op de tegels."),
        ],
    },
    {
        "slug": "inloopdouche-plaatsen",
        "seo_titel": "Inloopdouche laten plaatsen: kosten en werkwijze",
        "naam": "Inloopdouche plaatsen",
        "naam_kort": "Inloopdouche",
        "kort": "Een douche zonder drempel, met glazen wand en douchegoot",
        "icon": "douche",
        "prijs_van": 1500,
        "prijs_tot": 5000,
        "prijs_eenheid": "per inloopdouche",
        "prijs_extra": "Dat is inclusief plaatsing. Het grootste verschil zit in de vloer: een inloopdouche op een bestaande douchebakplek is goedkoper dan een drempelloze douche waarvoor de hele vloer op afschot moet en opnieuw betegeld wordt.",
        "meta_title": "Inloopdouche laten plaatsen: kosten | {plaats}",
        "intro": (
            "Een inloopdouche is een douche zonder deur en meestal zonder drempel, met alleen een "
            "glazen wand. Hij is ruim, makkelijk schoon te houden en ook op latere leeftijd prettig "
            "in gebruik. Het lastige zit in de vloer: het water moet de goede kant op lopen, en "
            "dat vraagt het juiste afschot en een goede afvoer."
        ),
        "wat": [
            "Een inloopdouche plaatsen op de plek van een oude douchebak of bad",
            "Een douchegoot of putje inbouwen met afschot in de vloer",
            "Een glazen douchewand plaatsen",
            "Een inbouwkraan of regendouche aansluiten",
            "De natte zone waterdicht maken en betegelen",
            "Een drempelloze douche voor gebruik op latere leeftijd",
        ],
        "werkwijze": [
            ("Opname", "De specialist kijkt waar de afvoer zit, hoeveel afschot mogelijk is en of de vloer daarvoor open moet."),
            ("Slopen", "De oude douchebak of het bad gaat eruit, net als de tegels in de douchehoek."),
            ("Afvoer en afschot", "De douchegoot of het putje wordt ingebouwd en de vloer krijgt afschot."),
            ("Waterdicht maken en tegelen", "De natte zone krijgt een waterdichte laag, daarna volgt het tegelwerk."),
            ("Wand en kraan", "De glazen wand wordt geplaatst en de kraan aangesloten. Daarna volgt een test op lekkage en afvoer."),
        ],
        "prijsfactoren": [
            "Of er een drempel mag blijven of dat de douche helemaal vlak moet",
            "Hoeveel van de vloer en wanden opnieuw betegeld moet worden",
            "Het type afvoer: een douchegoot is duurder dan een putje",
            "De douchewand: de dikte en het formaat van het glas",
            "De kraan: een opbouwkraan is goedkoper dan een inbouwkraan met regendouche",
        ],
        "tips": [
            "Vraag naar de hoogte van de vloer en de plek van de afvoer. Die bepalen of een volledig drempelloze douche haalbaar is.",
            "Kies een glazen wand die breed genoeg is om spatwater binnen te houden. Een te smalle wand betekent een natte badkamervloer.",
            "Een douchegoot langs de wand is makkelijker schoon te houden dan een putje in het midden.",
        ],
        "faq": [
            ("Kan een inloopdouche in een kleine badkamer?", "Vaak wel. Een inloopdouche zonder deur neemt juist minder ruimte in dan een cabine. Houd wel rekening met spatwater buiten de douchezone."),
            ("Hoelang duurt het plaatsen van een inloopdouche?", "Als alleen de douchehoek wordt aangepast, vaak een paar dagen inclusief tegelwerk en droogtijd. Moet de hele vloer opnieuw, dan duurt het langer."),
            ("Is een inloopdouche zonder drempel altijd mogelijk?", "Niet altijd. Het hangt af van de vloeropbouw en de hoogte van de afvoer. Een specialist kan dat bij de opname vertellen."),
            ("Welk btw-tarief geldt?", "Voor het plaatsen van een inloopdouche geldt 21% btw, op het werk en op de materialen."),
        ],
    },
    {
        "slug": "toilet-renoveren",
        "seo_titel": "Toilet renoveren: kosten en werkwijze",
        "naam": "Toilet renoveren",
        "naam_kort": "Toilet",
        "naam_lang": "Toiletruimte renoveren",
        "kort": "Nieuw toilet, fontein, tegels en verlichting in de toiletruimte",
        "icon": "toilet",
        "prijs_van": 2500,
        "prijs_tot": 6500,
        "prijs_eenheid": "per toiletruimte",
        "prijs_extra": "Dat is een complete renovatie met nieuwe tegels, toilet en fontein. Wil je alleen een nieuw staand toilet, dan kost dat inclusief montage zo'n €300 tot €700 aan werk. Een hangtoilet met inbouwreservoir en voorzetwand, of luxe tegels, zit aan de bovenkant van de bandbreedte.",
        "meta_title": "Toilet renoveren: kosten & specialist vinden | {plaats}",
        "intro": (
            "De toiletruimte is klein, maar elke bezoeker ziet hem. Een toiletrenovatie is daarom "
            "een overzichtelijke klus met veel effect. Omdat de ruimte zo klein is, telt elke "
            "centimeter: een hangtoilet, een smalle fontein en goed licht maken de ruimte groter "
            "en makkelijker schoon te houden."
        ),
        "wat": [
            "Het oude toilet en de tegels verwijderen",
            "Een staand toilet of hangtoilet met inbouwreservoir plaatsen",
            "Een fontein met kraan plaatsen en aansluiten",
            "Wand- en vloertegels zetten",
            "Verlichting en ventilatie aanpassen",
            "Het plafond en de wanden boven het tegelwerk afwerken",
        ],
        "werkwijze": [
            ("Opname", "De specialist kijkt naar de plek van de afvoer en wateraansluitingen en bespreekt de keuze voor toilet, fontein en tegels."),
            ("Slopen", "Toilet, fontein en tegels gaan eruit. Dan wordt ook de staat van de afvoer zichtbaar."),
            ("Leidingwerk", "Aansluitingen worden aangepast en bij een hangtoilet wordt het inbouwreservoir met voorzetwand geplaatst."),
            ("Tegelen", "Wanden en vloer worden betegeld en gevoegd."),
            ("Sanitair en afwerken", "Toilet en fontein worden gemonteerd, de naden gekit en de verlichting aangesloten."),
        ],
        "prijsfactoren": [
            "Staand toilet of hangtoilet met inbouwreservoir",
            "Hoeveel wand er betegeld wordt: tot halverwege of tot het plafond",
            "Of de afvoer en aansluitingen op dezelfde plek blijven",
            "Het niveau van toilet, fontein en kraan",
            "Extra's zoals een spiegel, inbouwspots of een nieuw plafond",
        ],
        "tips": [
            "Een hangtoilet maakt schoonmaken veel makkelijker, maar vraagt een voorzetwand. Neem dat mee in de beslissing.",
            "Vraag of de ventilatie meegenomen wordt. Een toilet zonder goede afzuiging blijft vochtig.",
            "Plan de renovatie zo dat je een tweede toilet in huis kunt gebruiken. Heb je dat niet, vraag dan hoelang het toilet buiten gebruik is.",
        ],
        "faq": [
            ("Hoelang duurt een toiletrenovatie?", "Meestal enkele werkdagen, inclusief tegelwerk en droogtijd. Bij een hangtoilet met voorzetwand of nieuwe leidingen duurt het iets langer."),
            ("Is een hangtoilet duurder dan een staand toilet?", "Ja, vooral door het inbouwreservoir en de voorzetwand. Daar staat tegenover dat de vloer eronder makkelijker schoon te houden is."),
            ("Kan ik het oude tegelwerk laten zitten?", "Als alleen het toilet wordt vervangen wel. Bij een hangtoilet moet de wand achter het toilet meestal opnieuw betegeld worden."),
            ("Welk btw-tarief geldt?", "Voor een toiletrenovatie geldt 21% btw. Alleen stukadoren of verfwerk in een woning ouder dan twee jaar kan onder 9% vallen, als het apart op de offerte staat."),
        ],
    },
    {
        "slug": "badkamer-onderhoud",
        "seo_titel": "Badkamer onderhoud: kitwerk, voegen en lekkage",
        "naam": "Badkamer onderhoud",
        "naam_kort": "Onderhoud",
        "kort": "Kitwerk vernieuwen, voegen herstellen en lekkages oplossen",
        "icon": "druppel",
        "prijs_van": 6,
        "prijs_tot": 11,
        "prijs_eenheid": "per meter kitwerk",
        "prijs_extra": "Dat is voor oude kit verwijderen en nieuwe aanbrengen. Veel vakmensen rekenen daarnaast een starttarief van €100 tot €200. Een hele badkamer opnieuw afkitten kost zo'n €95 tot €325. Voegen vernieuwen en lekkage zoeken gaan meestal per uur of per klus.",
        "meta_title": "Badkamer onderhoud: kitwerk & voegen | {plaats}",
        "intro": (
            "Een badkamer gaat niet in één keer kapot. Het begint met een zwarte kitrand, een "
            "voeg die loslaat of een vochtplek op het plafond eronder. Wie daar op tijd bij is, "
            "voorkomt dat water achter de tegels kruipt en de schade veel groter wordt. Goed "
            "onderhoud kan een badkamer jaren langer laten meegaan."
        ),
        "wat": [
            "Oude of beschimmelde kitranden verwijderen en vernieuwen",
            "Voegen uitslijpen en opnieuw invoegen",
            "Losse of gebarsten tegels vervangen",
            "Lekkage opsporen bij douche, bad of afvoer",
            "Lekkende kranen en sifons vervangen",
            "Advies over ventilatie tegen schimmel",
        ],
        "werkwijze": [
            ("Inspectie", "De vakman bekijkt de kitranden, voegen en tegels en zoekt bij lekkage naar de oorzaak."),
            ("Verwijderen", "Oude kit wordt volledig weggesneden en de naad schoongemaakt. Nieuwe kit over oude kit hecht niet goed."),
            ("Herstellen", "Voegen uitslijpen en opnieuw voegen, losse tegels vervangen of een lekkende aansluiting repareren."),
            ("Nieuw kitwerk", "Nieuwe sanitairkit aanbrengen, glad afwerken en laten uitharden."),
            ("Advies", "Tips om de nieuwe kit en voegen schoon en droog te houden."),
        ],
        "prijsfactoren": [
            "Het aantal meters kitwerk en hoeveel oude kit er weg moet",
            "Of het alleen om kitwerk gaat of ook om voegen en tegels",
            "Hoe moeilijk een lekkage te vinden is",
            "Of er schade achter de tegels zit",
            "Het starttarief en de voorrijkosten",
        ],
        "tips": [
            "Laat na het douchen de badkamer goed ventileren en trek de tegels af. Dat houdt kit en voegen veel langer schoon.",
            "Combineer kitwerk met andere klusjes in de badkamer, zodat je maar één keer starttarief betaalt.",
            "Zie je een vochtplek op het plafond onder de badkamer, wacht dan niet. Hoe langer water lekt, hoe duurder het herstel.",
        ],
        "faq": [
            ("Hoe vaak moet kitwerk vernieuwd worden?", "Dat hangt af van gebruik en ventilatie. Wordt kit zwart, laat hij los of zie je scheurtjes, dan is het tijd om hem te vernieuwen."),
            ("Kan nieuwe kit over oude kit heen?", "Nee, dat hecht slecht en schimmel blijft eronder zitten. Oude kit moet er helemaal af."),
            ("Hoe weet ik of mijn badkamer lekt?", "Let op vochtplekken op het plafond eronder, loszittende tegels, een muffe geur of voegen die steeds donker blijven. Een vakman kan de oorzaak opsporen."),
            ("Dekt mijn verzekering lekkage?", "Dat hangt af van je polis. Plotselinge waterschade wordt vaak gedekt, slijtage en achterstallig onderhoud zoals versleten kitwerk meestal niet. Kijk in je polisvoorwaarden."),
        ],
    },
    {
        "slug": "zakelijk-badkamers",
        "seo_titel": "Zakelijk: badkamers voor VvE, verhuur en projecten",
        "naam": "Zakelijk en VvE",
        "naam_kort": "Zakelijk",
        "naam_lang": "Badkamers voor VvE, verhuur en projecten",
        "kort": "VvE's, verhuurders, vakantieparken en projectmatige renovatie",
        "icon": "office",
        "prijs_van": 45,
        "prijs_tot": 85,
        "prijs_eenheid": "per uur excl. btw",
        "prijs_extra": "Bij meerdere badkamers werken specialisten vrijwel altijd met een vaste prijs per badkamer of een aanneemsom voor het hele project. Hoe meer badkamers van hetzelfde type, hoe scherper die prijs meestal is.",
        "meta_title": "Badkamers voor VvE, verhuur en projecten | {plaats}",
        "intro": (
            "Bij zakelijke badkamerprojecten gaat het niet om één badkamer, maar om tien of "
            "honderd. Denk aan een verhuurder die tussen twee huurders door renoveert, een VvE "
            "die gemeenschappelijke leidingen aanpakt of een vakantiepark dat alle chalets "
            "vernieuwt. Planning, vaste prijzen en een vaste contactpersoon wegen dan zwaarder "
            "dan de prijs per m²."
        ),
        "wat": [
            "Badkamers in huurwoningen renoveren tussen twee huurders door",
            "Projecten voor VvE's, zoals leidingwerk en standleidingen",
            "Badkamers in vakantiewoningen, chalets en hotels",
            "Sanitair in kantoren, kantines en bedrijfspanden",
            "Seriematige renovatie van meerdere gelijke badkamers",
            "Onderhoudscontracten voor kitwerk en kleine reparaties",
        ],
        "werkwijze": [
            ("Intake", "Een adviseur bekijkt een of meer badkamers, inventariseert het werk en bespreekt de planning."),
            ("Offerte", "Een vaste prijs per badkamer of een aanneemsom, met een duidelijke afbakening van meer- en minderwerk."),
            ("Planning", "Per woning of per verdieping, afgestemd op huurders, gasten of bewoners."),
            ("Uitvoering", "Een vaste contactpersoon en afspraken over oplevering per badkamer."),
            ("Nazorg", "Oplevering met een restpuntenlijst en garantie op papier."),
        ],
        "prijsfactoren": [
            "Het aantal badkamers en of ze van hetzelfde type zijn",
            "De planning: werken in bewoonde woningen of leegstand",
            "Of leidingwerk in gemeenschappelijke delen meegenomen moet worden",
            "Het niveau van sanitair en tegels",
            "Contractvorm: eenmalig project of meerjarig onderhoud",
        ],
        "tips": [
            "Kies bij meerdere badkamers voor één standaard sanitairpakket. Dat maakt inkoop, planning en onderhoud eenvoudiger.",
            "Leg vast hoeveel dagen een woning zonder badkamer zit en wat er gebeurt als dat uitloopt.",
            "Vraag om een kopie van de aansprakelijkheidsverzekering en leg vast wie verantwoordelijk is bij waterschade bij de buren.",
        ],
        "faq": [
            ("Hoe werkt een badkamerproject voor een VvE?", "Meestal via het meerjarenonderhoudsplan. Werk aan gemeenschappelijke leidingen valt onder de VvE, de badkamer in een appartement meestal onder de eigenaar. Laat dat vooraf goed uitzoeken."),
            ("Kan er buiten werktijden gewerkt worden?", "Vaak wel, bijvoorbeeld in hotels of bedrijfspanden. Reken dan op een toeslag op het uurtarief."),
            ("Welk btw-tarief geldt zakelijk?", "Voor badkamerwerk geldt 21% btw. Het 9%-tarief voor bijvoorbeeld stukadoren of verfwerk geldt alleen voor woningen ouder dan twee jaar, en bij een gemengd pand alleen voor het woongedeelte."),
            ("Wat is een aanneemsom?", "Een vaste totaalprijs voor het hele werk, in plaats van afrekenen per uur. Bij grotere projecten geeft dat zekerheid over het budget."),
        ],
    },
]

DIENST_BY_SLUG = {d["slug"]: d for d in DIENSTEN}

# ---------------------------------------------------------------------------
# PLAATSEN — Flevoland als thuisbasis, daarna de grensregio
# De hooks gaan over de leeftijd van de woningvoorraad, en dus over de badkamer
# die je er meestal aantreft. Bewust voorzichtig geformuleerd: het zegt iets
# over de gemiddelde woning, niet over elk huis.
# ---------------------------------------------------------------------------

PLAATSEN = [
    # --- Flevoland (kernmarkt) ---
    dict(slug="zeewolde", naam="Zeewolde", provincie="Flevoland", gemeente="Zeewolde",
         inwoners=23000, prio=1,
         hook="Zeewolde is gebouwd vanaf 1984. In de oudste wijken zit nog regelmatig de eerste of tweede badkamer, en die is inmiddels toe aan een grondige vernieuwing."),
    dict(slug="almere", naam="Almere", provincie="Flevoland", gemeente="Almere",
         inwoners=225000, prio=1,
         hook="Almere heeft veel woningen uit de jaren tachtig en negentig én veel recente nieuwbouw. In Almere Haven en Stad gaat het vaak om een complete badkamerrenovatie, in Poort en Duin eerder om upgrades zoals een inloopdouche of een hangtoilet."),
    dict(slug="lelystad", naam="Lelystad", provincie="Flevoland", gemeente="Lelystad",
         inwoners=82000, prio=1,
         hook="Veel woningen in Lelystad stammen uit de jaren zeventig en tachtig. Badkamers uit die tijd zijn vaak al eens vervangen, maar lang niet altijd: soms zitten de oorspronkelijke tegels en leidingen er nog."),
    dict(slug="dronten", naam="Dronten", provincie="Flevoland", gemeente="Dronten",
         inwoners=28000, prio=1,
         hook="Dronten combineert woningen uit de jaren zestig en zeventig met nieuwe wijken. In de oudere woningen is de badkamer vaak al eens vernieuwd; bij een volgende renovatie is het slim om ook de leidingen te laten bekijken."),
    dict(slug="biddinghuizen", naam="Biddinghuizen", provincie="Flevoland", gemeente="Dronten",
         inwoners=6500, prio=2,
         hook="In Biddinghuizen staan relatief veel vrijstaande woningen en voormalige boerderijen. Daar is vaak meer ruimte voor een tweede badkamer of een grotere inloopdouche."),
    dict(slug="swifterbant", naam="Swifterbant", provincie="Flevoland", gemeente="Dronten",
         inwoners=6800, prio=2,
         hook="Swifterbant is grotendeels gebouwd in de jaren zeventig. Badkamers uit die periode zijn vaak klein en zijn inmiddels meestal al een keer, soms twee keer, vernieuwd."),
    dict(slug="emmeloord", naam="Emmeloord", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=26000, prio=1,
         hook="Als hoofdplaats van de Noordoostpolder heeft Emmeloord een gevarieerde woningvoorraad. In de naoorlogse woningen is de badkamer vaak klein, in de nieuwbouw aan de randen gaat het eerder om upgrades."),
    dict(slug="urk", naam="Urk", provincie="Flevoland", gemeente="Urk",
         inwoners=21500, prio=2,
         hook="Op Urk staan compacte woningen in de oude kern naast ruimere nieuwbouw. In de kern is de badkamer vaak klein, waardoor slimme oplossingen zoals een inloopdouche en een hangtoilet veel winst geven."),
    dict(slug="marknesse", naam="Marknesse", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=4200, prio=3,
         hook="Marknesse bestaat vooral uit polderwoningen uit de jaren vijftig en zestig. De oorspronkelijke badkamers waren klein en zijn vaak al eens vervangen; bij een nieuwe renovatie is het slim om ook de indeling opnieuw te bekijken."),
    dict(slug="nagele", naam="Nagele", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=1900, prio=3,
         hook="Nagele is als modernistisch dorp ontworpen in de jaren vijftig. De woningen zijn compact, wat bij een badkamerrenovatie om een goed doordachte indeling vraagt."),
    dict(slug="ens", naam="Ens", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=3200, prio=3,
         hook="Ens ligt centraal in de Noordoostpolder, waardoor badkamerspecialisten uit Emmeloord en Kampen hier allebei zonder veel voorrijkosten kunnen komen."),
    dict(slug="kraggenburg", naam="Kraggenburg", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=1500, prio=3,
         hook="Kraggenburg is klein, waardoor specialisten hier het liefst meerdere klussen in dezelfde periode plannen. Flexibel zijn in de startdatum kan je dus geld schelen."),
    dict(slug="luttelgeest", naam="Luttelgeest", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=1900, prio=3,
         hook="In Luttelgeest staan naast woningen ook veel bedrijfsgebouwen, waardoor lokale installateurs vaak zowel particuliere badkamers als zakelijk sanitair doen."),
    dict(slug="tollebeek", naam="Tollebeek", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=2100, prio=3,
         hook="Tollebeek bestaat vooral uit compacte polderwoningen uit de jaren vijftig en zestig. Kleine badkamers hebben daar veel baat bij een inloopdouche in plaats van een bad."),
    dict(slug="bant", naam="Bant", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=1400, prio=3,
         hook="Bant is een compact polderdorp waar de meeste woningen uit dezelfde bouwperiode stammen. Buren hebben er dus vaak een vergelijkbare badkamer, met dezelfde aandachtspunten."),
    dict(slug="creil", naam="Creil", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=1400, prio=3,
         hook="Creil ligt aan de noordrand van de polder. Specialisten combineren werk hier graag met opdrachten in Rutten en Espel."),
    dict(slug="rutten", naam="Rutten", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=800, prio=3,
         hook="Rutten is een van de kleinste polderdorpen. Vraag bij offertes gericht naar voorrijkosten, die kunnen hier het verschil maken."),
    dict(slug="espel", naam="Espel", provincie="Flevoland", gemeente="Noordoostpolder",
         inwoners=800, prio=3,
         hook="In Espel staan veel woningen uit de jaren vijftig, vaak met agrarische bijgebouwen. Wie verbouwt, heeft er soms ruimte om de badkamer te vergroten of een tweede toilet toe te voegen."),

    # --- Randmeren / Veluwe ---
    dict(slug="harderwijk", naam="Harderwijk", provincie="Gelderland", gemeente="Harderwijk",
         inwoners=49000, prio=1,
         hook="In de binnenstad van Harderwijk staan veel oude en monumentale panden, waar de badkamer vaak klein is en leidingen niet altijd logisch lopen. Daarbuiten gaat het vooral om naoorlogse rijwoningen."),
    dict(slug="ermelo", naam="Ermelo", provincie="Gelderland", gemeente="Ermelo",
         inwoners=27000, prio=2,
         hook="Ermelo heeft veel vrijstaande woningen en twee-onder-een-kappers uit de jaren zestig tot tachtig. In veel van die huizen is de badkamer al een of twee keer vernieuwd en is de volgende ronde in zicht."),
    dict(slug="putten", naam="Putten", provincie="Gelderland", gemeente="Putten",
         inwoners=25000, prio=2,
         hook="Putten heeft relatief veel vrijstaande woningen uit de jaren zeventig. Badkamers uit die tijd zijn vaak al eens vervangen; wie nu renoveert, kiest vaak voor een inloopdouche in plaats van het bad."),
    dict(slug="nijkerk", naam="Nijkerk", provincie="Gelderland", gemeente="Nijkerk",
         inwoners=45000, prio=2,
         hook="Nijkerk groeide de laatste jaren hard met nieuwbouw in Doornsteeg, waar badkamers nog nieuw zijn. In de oude kern gaat het juist vaker om een complete renovatie."),
    dict(slug="nunspeet", naam="Nunspeet", provincie="Gelderland", gemeente="Nunspeet",
         inwoners=28000, prio=3,
         hook="Nunspeet heeft veel ruime woningen uit de jaren zestig en zeventig. Daar is vaak genoeg ruimte voor een grotere badkamer, en soms voor een tweede badkamer op de verdieping."),
    dict(slug="elburg", naam="Elburg", provincie="Gelderland", gemeente="Elburg",
         inwoners=23000, prio=3,
         hook="Binnen de vesting van Elburg staan monumenten, waar een badkamerrenovatie soms aan regels gebonden is. Laat bij een monument vooraf bij de gemeente checken wat er mag."),

    # --- Overijssel / IJsseldelta ---
    dict(slug="kampen", naam="Kampen", provincie="Overijssel", gemeente="Kampen",
         inwoners=54000, prio=2,
         hook="Kampen heeft een historische binnenstad naast de nieuwbouw van Het Onderdijks. In oude panden is de badkamer vaak klein en lastig in te delen, in de nieuwbouw gaat het eerder om upgrades."),
    dict(slug="zwolle", naam="Zwolle", provincie="Overijssel", gemeente="Zwolle",
         inwoners=132000, prio=1,
         hook="Zwolle is groot genoeg voor gespecialiseerde badkamerbedrijven: van kleine badkamers in oude binnenstadspanden tot projecten voor VvE's in de nieuwere wijken."),
    dict(slug="genemuiden", naam="Genemuiden", provincie="Overijssel", gemeente="Zwartewaterland",
         inwoners=10500, prio=3,
         hook="Genemuiden heeft veel eengezinswoningen uit de jaren zestig tot tachtig. Veel badkamers in die woningen zijn al eens vernieuwd, maar niet allemaal recent."),

    # --- Utrecht / Gooi ---
    dict(slug="bunschoten-spakenburg", naam="Bunschoten-Spakenburg", provincie="Utrecht", gemeente="Bunschoten",
         inwoners=22000, prio=3,
         hook="In de oude kern van Spakenburg zijn woningen vaak smal en de badkamers klein. In de naoorlogse wijken daarbuiten gaat het vooral om rijwoningen met een standaard badkamer."),
    dict(slug="amersfoort", naam="Amersfoort", provincie="Utrecht", gemeente="Amersfoort",
         inwoners=161000, prio=1,
         hook="Amersfoort loopt van middeleeuwse binnenstad tot de nieuwbouw van Vathorst. Prijzen liggen hier merkbaar hoger dan in Flevoland, dus vergelijken loont extra."),
    dict(slug="huizen", naam="Huizen", provincie="Noord-Holland", gemeente="Huizen",
         inwoners=42000, prio=2,
         hook="Huizen heeft veel woningen uit de jaren zestig tot tachtig. Bij die bouwperiode is het slim om bij een nieuwe badkamer ook de leidingen en afvoer te laten beoordelen."),
    dict(slug="blaricum", naam="Blaricum", provincie="Noord-Holland", gemeente="Blaricum",
         inwoners=12000, prio=3,
         hook="In Blaricum staan veel karakteristieke villa's, waar badkamers vaak ruimer zijn en afwerking en materiaalkeuze zwaarder wegen dan de laagste prijs."),
    dict(slug="naarden", naam="Naarden", provincie="Noord-Holland", gemeente="Gooise Meren",
         inwoners=17500, prio=3,
         hook="Binnen de vesting van Naarden staan monumenten, waar een badkamerrenovatie soms aan regels gebonden is. Buiten de vesting gaat het vooral om gewone woningen."),
    dict(slug="bussum", naam="Bussum", provincie="Noord-Holland", gemeente="Gooise Meren",
         inwoners=33000, prio=2,
         hook="Bussum heeft veel jaren-dertig woningen. Die hebben vaak een kleine badkamer, waar elke centimeter telt en een goed ontwerp veel verschil maakt."),
    dict(slug="hilversum", naam="Hilversum", provincie="Noord-Holland", gemeente="Hilversum",
         inwoners=93000, prio=1,
         hook="Hilversum staat vol jaren-twintig en jaren-dertig woningen. De badkamer is daar vaak klein of later toegevoegd, en oude leidingen zijn een aandachtspunt bij een renovatie."),
    dict(slug="weesp", naam="Weesp", provincie="Noord-Holland", gemeente="Amsterdam",
         inwoners=19500, prio=3,
         hook="Weesp combineert een historische kern met nieuwbouw in Weespersluis. In oude panden is de badkamer vaak klein, in de nieuwbouw gaat het eerder om upgrades."),
]

PLAATS_BY_SLUG = {p["slug"]: p for p in PLAATSEN}


def buurplaatsen(plaats, n=6):
    """Simpele nabijheid: zelfde gemeente eerst, dan zelfde provincie, dan de rest."""
    others = [p for p in PLAATSEN if p["slug"] != plaats["slug"]]

    def score(p):
        s = 0
        if p["gemeente"] == plaats["gemeente"]:
            s -= 100
        if p["provincie"] == plaats["provincie"]:
            s -= 40
        s -= p["inwoners"] / 50000.0
        return s

    others.sort(key=score)
    return others[:n]


# ---------------------------------------------------------------------------
# PRIJSINDEX PER PROVINCIE
# Arbeidskosten van badkamerspecialisten en installateurs verschillen per regio.
# Deze index maakt de richtprijzen op elke plaatspagina kloppend én uniek.
# Het is een schatting: bijstellen zodra je echte offertedata uit je eigen
# leads hebt.
# ---------------------------------------------------------------------------

PRIJSINDEX = {
    "Flevoland": 0.96,
    "Overijssel": 0.95,
    "Gelderland": 1.00,
    "Utrecht": 1.09,
    "Noord-Holland": 1.13,
}

INDEX_TOELICHTING = {
    "Flevoland": "Flevoland zit naar verwachting iets onder het landelijk gemiddelde. Ruime bouw, goede bereikbaarheid en weinig binnensteden met parkeergedoe houden de arbeidskosten van badkamerspecialisten hier lager.",
    "Overijssel": "Overijssel hoort bij de goedkopere regio's. Er zijn relatief veel kleinere installatiebedrijven en zelfstandige tegelzetters actief, wat de prijzen drukt.",
    "Gelderland": "Gelderland zit vrijwel op het landelijk gemiddelde. Alleen in de historische kernen loopt het op, door lastiger bereikbaarheid en oudere panden.",
    "Utrecht": "In Utrecht liggen de tarieven ongeveer een tiende boven het landelijk gemiddelde. Hogere bedrijfskosten en volle agenda's bij installateurs spelen daarin mee.",
    "Noord-Holland": "Noord-Holland is de duurste regio van dit werkgebied. Reken op ruim tien procent boven het landelijk gemiddelde, vooral door hogere loon- en huisvestingskosten van badkamerbedrijven.",
}


def lokale_prijs(dienst, plaats):
    """Richtprijs van een dienst, gecorrigeerd voor de regio."""
    i = PRIJSINDEX.get(plaats["provincie"], 1.0)
    van = int(round(dienst["prijs_van"] * i))
    tot = int(round(dienst["prijs_tot"] * i))
    return van, tot


# ---------------------------------------------------------------------------
# WONINGVOORRAAD PER PLAATS
# bouwperiode = wanneer het gros van de woningen is neergezet
# woningmix   = het overheersende woningtype
# ligging     = de woonomgeving (neutraal; over water of kalk zeggen we niets
#               zonder bron per drinkwaterbedrijf)
# ---------------------------------------------------------------------------

WONINGEN = {
    "zeewolde":      ("vanaf 1984", "ruime eengezinswoningen met veel eigen grond", "een ruim opgezet dorp in het open polderlandschap"),
    "almere":        ("jaren tachtig en negentig, plus recente nieuwbouw", "een mix van rijwoningen, twee-onder-een-kappers en appartementen", "een jonge stad met per stadsdeel een heel andere bouwperiode"),
    "lelystad":      ("jaren zeventig en tachtig", "eengezinswoningen met flinke raampartijen", "ruim opgezette woonwijken aan het IJsselmeer"),
    "dronten":       ("jaren zestig en zeventig, met nieuwbouw aan de randen", "ruime woningen met grote raampartijen", "een polderdorp met een oudere kern en nieuwe wijken aan de randen"),
    "biddinghuizen": ("jaren zestig en zeventig", "veel vrijstaande woningen en voormalige boerderijen", "een dorp in open agrarisch gebied"),
    "swifterbant":   ("jaren zeventig", "eengezinswoningen met houten geveldelen", "een compact dorp in vlak polderland"),
    "emmeloord":     ("naoorlogse polderbouw tot recente nieuwbouw", "een brede mix van rij-, hoek- en vrijstaande woningen", "de centrale plaats van de Noordoostpolder"),
    "urk":           ("gemengd, van historische kern tot nieuwbouwwijken", "compacte woningen in de kern en ruimere woningen aan de rand", "een dichtbebouwde oude kern met ruimere wijken eromheen"),
    "marknesse":     ("jaren vijftig en zestig", "ruime polderwoningen met grote tuinen", "een rustig polderdorp"),
    "nagele":        ("jaren vijftig, modernistisch ontworpen", "woningen met platte daken en houten geveldelen", "een modernistisch ontworpen dorp met veel groen"),
    "ens":           ("jaren vijftig en zestig", "polderwoningen met eenvoudige gevels", "een dorp midden in de Noordoostpolder"),
    "kraggenburg":   ("jaren vijftig", "kleinschalige polderwoningen", "een klein, landelijk dorp"),
    "luttelgeest":   ("jaren vijftig en zestig", "woningen naast veel agrarische bebouwing", "een dorp tussen agrarische bedrijven en kassen"),
    "tollebeek":     ("jaren vijftig en zestig", "compacte polderwoningen", "een klein dorp vlak bij het IJsselmeer"),
    "bant":          ("jaren vijftig", "woningen uit één bouwstroom", "een compact polderdorp"),
    "creil":         ("jaren vijftig", "polderwoningen aan de noordrand", "een klein dorp aan de noordrand van de polder"),
    "rutten":        ("jaren vijftig", "kleinschalige woningen", "een van de kleinste dorpen van de polder"),
    "espel":         ("jaren vijftig", "woningen met vaak agrarische bijgebouwen", "een klein dorp in de open polder"),
    "harderwijk":    ("historische kern plus naoorlogse uitbreidingen", "monumentale panden in het centrum en rijwoningen daarbuiten", "een oude binnenstad met naoorlogse wijken eromheen"),
    "ermelo":        ("jaren zestig tot tachtig", "veel vrijstaande woningen en twee-onder-een-kappers", "een groen dorp tegen de bossen van de Veluwe"),
    "putten":        ("gemengd, veel uit de jaren zeventig", "vrijstaande woningen, deels met riet en houten geveldelen", "een dorp op de rand van de Veluwe"),
    "nijkerk":       ("oude kern plus recente nieuwbouw in Doornsteeg", "historische panden naast moderne rijwoningen", "een oude kern met grote nieuwbouwwijken"),
    "nunspeet":      ("jaren zestig en zeventig", "ruime woningen met veel houtwerk", "een ruim opgezet dorp tussen bos en heide"),
    "elburg":        ("vestingstad met naoorlogse uitbreidingen", "monumenten binnen de vesting, gewone woningen erbuiten", "een historische vestingstad aan het Drontermeer"),
    "kampen":        ("historische binnenstad plus nieuwbouw in Het Onderdijks", "monumentale panden naast moderne eengezinswoningen", "een historische stad aan de IJssel"),
    "zwolle":        ("van middeleeuwse binnenstad tot Stadshagen", "alle woningtypes, van grachtenpand tot nieuwbouwappartement", "een grote stad met wijken uit elke bouwperiode"),
    "genemuiden":    ("jaren zestig tot tachtig", "eengezinswoningen dicht op elkaar", "een compact stadje aan het Zwarte Water"),
    "bunschoten-spakenburg": ("historische kern plus naoorlogse wijken", "karakteristieke panden in de kern, rijwoningen daarbuiten", "een oude vissersplaats aan het Eemmeer"),
    "amersfoort":    ("middeleeuwse binnenstad tot de nieuwbouw van Vathorst", "van monumenten tot recente gezinswoningen", "een grote stad met een historische kern en veel nieuwbouw"),
    "huizen":        ("jaren zestig tot tachtig", "eengezinswoningen en appartementen", "een gemeente aan het Gooimeer met veel naoorlogse wijken"),
    "blaricum":      ("gemengd, met veel vooroorlogse villabouw", "karakteristieke villa's met riet en houten gevels", "een groen dorp tussen bos en heide"),
    "naarden":       ("vesting plus naoorlogse uitbreidingen", "monumenten binnen de vesting, gewone woningen erbuiten", "een historische vesting met nieuwere wijken erbuiten"),
    "bussum":        ("vooral jaren dertig", "woningen met roedeverdeling en veel raamdetail", "een groene woonplaats met veel vooroorlogse bouw"),
    "hilversum":     ("jaren twintig tot veertig, veel Dudok", "jaren-dertig woningen, deels met stalen kozijnen", "een groene stad met veel vooroorlogse woonwijken"),
    "weesp":         ("historische kern plus nieuwbouw in Weespersluis", "grachtenpanden naast moderne gezinswoningen", "een historisch stadje aan de Vecht"),
}

for _p in PLAATSEN:
    _b, _w, _l = WONINGEN.get(_p["slug"], ("gemengd", "een mix van woningtypes", "een gemengde woonomgeving"))
    _p["bouwperiode"], _p["woningmix"], _p["ligging"] = _b, _w, _l
