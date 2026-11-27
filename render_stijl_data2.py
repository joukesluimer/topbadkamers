# -*- coding: utf-8 -*-
"""Metadata van de stijlrenders uit ronde 3 (renders/b4-*.html, uitvoer in fotos/renders/).

Zelfde schema als render_stijl_data.py. Elke stijl heeft twee renders:
- "<slug>": het overzicht (b4-<slug>-1);
- "<slug>-2": een detail of andere hoek (b4-<slug>-2).
Elke render is een eigen 3D-illustratie: "Illustratie (3D-render, Top Badkamers)".
`naam` is de bestandsnaam zonder -400/-800/-1600.webp.
"""

_BIJ = "Illustratie (3D-render, Top Badkamers)"


def _r(naam, alt, bijschrift):
    return {"naam": naam, "alt": alt, "w": 1600, "h": 1067, "bijschrift": f"{_BIJ}: {bijschrift}"}


RENDERS_STIJL2 = {
    "scandinavische-badkamer": _r(
        "b4-scandinavische-badkamer-1",
        "Illustratie van een lichte Scandinavische badkamer met staande witte tegels, een vloer in licht eiken "
        "houtlook, een inloopdouche met helder glas, een eiken meubel met ronde kom en een eiken ladderrek",
        "Scandinavische badkamer met witte staande tegels, licht eiken en veel daglicht."),
    "scandinavische-badkamer-2": _r(
        "b4-scandinavische-badkamer-2",
        "Detail van een Scandinavisch wastafelmeubel in licht eiken met een witte ronde opzetkom, een kraan in "
        "geborsteld rvs en een ronde spiegel met eiken rand tegen witte staande tegels",
        "detail van het eiken meubel met opzetkom en de ronde spiegel met houten rand."),
    "luxe-badkamer": _r(
        "b4-luxe-badkamer-1",
        "Illustratie van een ruime luxe badkamer met een wand van warm geaderd marmer, een dubbel wastafelmeubel "
        "in donker eiken met twee kommen, een vrijstaand bad onder het raam en een ruime inloopdouche met goudkleurig profiel",
        "luxe badkamer met een marmeren wand, een dubbel meubel, een vrijstaand bad en goudkleurige kranen."),
    "luxe-badkamer-2": _r(
        "b4-luxe-badkamer-2",
        "Detail van het dubbele wastafelmeubel in donker eiken met twee witte opzetkommen, goudkleurige wandkranen, "
        "twee boogspiegels en wandlampjes tegen een wand van warm geaderd marmer",
        "detail van het dubbele meubel met twee kommen, boogspiegels en de marmeren wand."),
    "marmer-badkamer": _r(
        "b4-marmer-badkamer-1",
        "Illustratie van een marmeren badkamer met grote platen wit marmer met grijze en goudachtige aders op wanden en vloer, "
        "een vrijstaand bad, een inloopdouche en een zwevend walnoten meubel met goudkleurige kranen",
        "marmeren badkamer met grote platen op wand en vloer, een vrijstaand bad en walnoot."),
    "marmer-badkamer-2": _r(
        "b4-marmer-badkamer-2",
        "Detail van een zwevend walnoten wastafelmeubel met marmeren blad en een ronde witte opzetkom, een "
        "goudkleurige wandkraan, een ronde spiegel en wandlampjes tegen een wand van geaderd marmer",
        "detail van het walnoten meubel met marmeren blad tegen de geaderde marmerwand."),
    "zwart-wit-badkamer": _r(
        "b4-zwart-wit-badkamer-1",
        "Illustratie van een zwart-wit badkamer met witte metrotegels en zwarte voeg, een zwart-wit dambordvloer, "
        "een douchewand met zwart profiel en roeden, een mat zwart meubel en een boogspiegel",
        "zwart-wit badkamer met metrotegels, een dambordvloer en zwart staal."),
    "zwart-wit-badkamer-2": _r(
        "b4-zwart-wit-badkamer-2",
        "Detail van de zwart-wit badkamer: de dambordvloer, het mat zwarte meubel op pootjes en de douchewand "
        "met zwarte roeden tegen witte metrotegels met donkere voeg",
        "detail van de dambordvloer, het zwarte meubel en de douchewand met roeden."),
    "terrazzo-badkamer": _r(
        "b4-terrazzo-badkamer-1",
        "Illustratie van een terrazzo badkamer met een vloer en douchewand in warme terrazzo met terracotta en "
        "grijze korrels, zachte terracotta verf, een eiken meubel met terracotta kom en messing kranen",
        "terrazzo badkamer met warme korrels, terracotta accenten en messing."),
    "terrazzo-badkamer-2": _r(
        "b4-terrazzo-badkamer-2",
        "Detail van een eiken wastafelmeubel met een blad van terrazzo, een ronde terracotta opzetkom, een "
        "messing wandkraan en een ronde spiegel tegen terrazzo en terracotta verf",
        "detail van het terrazzo blad met terracotta kom en messing kraan."),
    "wellness-badkamer": _r(
        "b4-wellness-badkamer-1",
        "Illustratie van een wellness badkamer met donkere tegels in steenlook, een wand met eiken lamellen, een "
        "inloopdouche met betegelde zitbank en een lange nis met warm ledlicht, en een zwevend meubel met ronde spiegel",
        "wellness badkamer met donkere steenlook, eiken lamellen, een zitbank in de douche en warm licht."),
    "wellness-badkamer-2": _r(
        "b4-wellness-badkamer-2",
        "Detail van een inloopdouche met een betegelde zitbank, opgevouwen handdoeken, een vierkante regendouche "
        "aan het plafond en een lange nis met warm ledlicht in donkere tegels",
        "detail van de zitbank in de douche en de verlichte nis."),
}
