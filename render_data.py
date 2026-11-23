"""3D-renders (three.js) voor de homepage en de dienstpagina's.

Bestanden: fotos/renders/<naam>-400.webp, -800.webp en -1600.webp (3:2).
Bronscènes: renders/bd-<sleutel>.html met renders/bd-common.js.
Altijd tonen met het bijschrift: het zijn illustraties, geen foto's van uitgevoerd werk.
"""

BIJSCHRIFT = "Illustratie (3D-render, Top Badkamers)"

RENDERS = {
    "home": {
        "naam": "bd-home",
        "alt": "Lichte, moderne badkamer met inloopdouche met zwart profiel, groene wandtegels, zwevend eiken badmeubel en hangtoilet",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "badkamer-renoveren": {
        "naam": "bd-badkamer-renoveren",
        "alt": "Gerenoveerde badkamer in warme tinten met vrijstaand bad, dubbel notenhouten badmeubel met waskommen en een gouden regendouche",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "badkamer-installeren": {
        "naam": "bd-badkamer-installeren",
        "alt": "Open badmeubel met waskom, kraan, sifon, hoekstopkranen en flexibele aansluitslangen",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "tegelwerk-badkamer": {
        "naam": "bd-tegelwerk-badkamer",
        "alt": "Half betegelde badkamerwand met tegelkruisjes in de voegen, gekamde tegellijm, een lijmkam op de emmer en een stapel tegels",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "inloopdouche-plaatsen": {
        "naam": "bd-inloopdouche-plaatsen",
        "alt": "Inloopdouche met glazen wand, douchegoot langs de wand, regendouche en marmerlook wandtegels",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "toilet-renoveren": {
        "naam": "bd-toilet-renoveren",
        "alt": "Apart toilet met hangtoilet in een betegelde voorzetwand, zwarte bedieningsplaat, fonteintje en rond spiegeltje",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "badkamer-onderhoud": {
        "naam": "bd-badkamer-onderhoud",
        "alt": "Close-up van een douchehoek met strakke kitranden en schone voegen tussen wand- en vloertegels",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
    "zakelijk-badkamers": {
        "naam": "bd-zakelijk-badkamers",
        "alt": "Functionele hotel- of appartementsbadkamer met inloopdouche, zwevend badmeubel voor een donkere accentwand en hangtoilet",
        "w": 1600,
        "h": 1067,
        "bijschrift": BIJSCHRIFT,
    },
}
