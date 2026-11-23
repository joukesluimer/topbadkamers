# -*- coding: utf-8 -*-
"""Metadata van de stijlrenders (renders/bs-*.html, uitvoer in fotos/renders/).

Elke render is een eigen 3D-illustratie: "Illustratie (3D-render, Top Badkamers)".
Op de site staat er altijd bij dat het een illustratie is. De sleutel is de slug van
de stijlpagina op /inspiratie/<slug>/; `naam` is de bestandsnaam zonder -400/-800/-1600.webp.
"""

_BIJ = "Illustratie (3D-render, Top Badkamers)"

RENDERS_STIJL = {
    "moderne-badkamer": {
        "naam": "bs-moderne-badkamer",
        "alt": "Illustratie van een moderne badkamer met grote witte wandtegels, een antraciet tegelvloer, "
               "een inloopdouche met helder glas, een zwevend eiken wastafelmeubel, mat zwarte kranen en een hangtoilet",
        "w": 1600, "h": 1067,
        "bijschrift": f"{_BIJ}: moderne badkamer met grote tegels, een zwevend eiken meubel en mat zwarte kranen.",
    },
    "landelijke-badkamer": {
        "naam": "bs-landelijke-badkamer",
        "alt": "Illustratie van een landelijke badkamer met groene handgemaakte tegels tot halverwege de wand, "
               "kalkverf, een vloer met cementtegelpatroon, een vrijstaand bad, een eiken meubel en messing kranen",
        "w": 1600, "h": 1067,
        "bijschrift": f"{_BIJ}: landelijke badkamer met groene tegels, een vrijstaand bad en messing kranen.",
    },
    "industriele-badkamer": {
        "naam": "bs-industriele-badkamer",
        "alt": "Illustratie van een industriële badkamer met grote tegels in betonlook, een douchewand met zwart "
               "stalen profiel, een opbouwregendouche in mat zwart en een antraciet meubel met eiken blad",
        "w": 1600, "h": 1067,
        "bijschrift": f"{_BIJ}: industriële badkamer met betonlook, zwart staal en warm hout.",
    },
    "japandi-badkamer": {
        "naam": "bs-japandi-badkamer",
        "alt": "Illustratie van een japandi-badkamer met gebroken witte tegels in visgraat, zandkleurige kalkverf, "
               "een terrazzovloer, een eiken meubel met opzetkom, een ronde spiegel en zwarte accenten",
        "w": 1600, "h": 1067,
        "bijschrift": f"{_BIJ}: japandi-badkamer met visgraattegels, terrazzo, licht eiken en zwarte accenten.",
    },
    "klassieke-badkamer": {
        "naam": "bs-klassieke-badkamer",
        "alt": "Illustratie van een klassieke badkamer met witte metrotegels in halfsteens verband, grijsgroene "
               "wanden, een marmerlook vloer, een bad op gouden pootjes en een wit meubel met kruiskraan",
        "w": 1600, "h": 1067,
        "bijschrift": f"{_BIJ}: klassieke badkamer met metrotegels, een bad op pootjes en goudkleurige kranen.",
    },
    "kleine-badkamer": {
        "naam": "bs-kleine-badkamer",
        "alt": "Illustratie van een kleine badkamer van ongeveer 1,8 bij 2,2 meter met een inloopdouche met helder "
               "glas in de hoek, een hangtoilet ernaast en een smal zwevend meubel met grote spiegel aan de zijwand",
        "w": 1600, "h": 1067,
        "bijschrift": f"{_BIJ}: kleine badkamer van ongeveer 1,8 × 2,2 m met inloopdouche, hangtoilet en smal meubel.",
    },
}
