# -*- coding: utf-8 -*-
"""Kostenpagina's ronde 3: acht extra pagina's onder /kosten/<slug>/.

Dit bestand exporteert:
- KOSTEN3: lijst met acht dicts in precies hetzelfde schema als badkamer_kosten.KOSTEN;
- B3: nieuwe bronnen (sleutel -> (naam, url)) die nog niet in badkamer_kosten.B staan.

Inbouwen in badkamer_kosten.py (door de hoofdsessie), direct ná de lijst KOSTEN en vóór KOSTEN_BY_SLUG:

    from badkamer_kosten3 import KOSTEN3, B3
    B.update(B3)
    KOSTEN += KOSTEN3

Dit bestand importeert NIET uit badkamer_kosten (dat zou circulair zijn). De kleine helpers
(rp, som, rb, TOTAAL) staan daarom hieronder nog een keer, met dezelfde werking.

Opbouw per pagina (binnen het bestaande schema):
- "varianten" zijn de drie voorbeeldscenario's budget, midden en luxe;
- "voorbeeld" is de kostenopbouw, in drie blokken: materiaal, arbeid en extra's, elk met een subtotaal.

Alle bedragen zijn richtprijzen inclusief 21% btw, tenzij er iets anders bij staat. Gedeelde posten
(sloop, afvoer, leidingwerk, elektra, tegels, legloon, waterdicht, kitwerk, montage, sanitair per niveau,
vloerverwarming, ventilator, uurtarief) komen uit richtprijzen.py; hun bronnen staan daar.

Nieuwe bandbreedtes en hun bronnen, geraadpleegd in november 2026:
- Homedeal, kleine badkamer verbouwen: 2 m² €3.500 – €5.000, 3 m² €4.000 – €6.500, 4 m² €4.500 – €7.000,
  5 m² €4.500 – €8.000; basic €3.000 – €5.000, midden €5.000 – €10.000, luxe vanaf €10.000.
  https://www.homedeal.nl/badkamerspecialist/kleine-badkamer-verbouwen/
- Trustoo, nieuwe badkamer 2026: compacte badkamer 3 – 4 m² €8.250 – €12.000 inclusief basismateriaal.
  https://trustoo.nl/kosten/badkamer-renovatie-kosten/
- Homedeal, badkamer aanleggen: gemiddeld €7.500 (€3.500 – €15.000), €550 – €1.100 per m²; basic €5.000 – €7.500,
  gemiddeld €7.500 – €10.000, luxe €10.000 – €15.000; voorbeeld luxe badkamer 12 m² €20.000 – €30.000;
  stoomdouche €1.600 – €4.300; whirlpool €2.700 – €6.700 (incl. materiaal, montage en btw).
  https://www.homedeal.nl/badkamerspecialist/badkamer-aanleggen-kosten/
- Slimster, compleet nieuwe badkamer: luxe €11.000 – €15.000 inclusief installatie (zie richtprijzen.py).
- Slimster, vrijstaand bad: luxe vrijstaand bad zonder plaatsing rond €2.000.
  https://slimster.nl/badkamer/bad-plaatsen-kosten/vrijstaand-bad/
- Werkspot, wastafel: plaatsen of vervangen €150 – €800; vrijstaande wastafel €200 – €550, inbouwwastafel
  €150 – €400, dubbele wastafel €300 – €800; 2 – 3 uur werk plus 0,5 – 1 uur testen en afwerken.
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/wastafel
- Slimster, wastafel plaatsen: gemiddeld €550 (€100 – €1.000), exclusief kraan en montage.
  https://slimster.nl/badkamer/wastafel-plaatsen-kosten/
- Werkspot, douchekraan vervangen: eenhendelmengkraan €50 – €150, thermostaatkraan €50 – €300, designkraan
  €200 – €450; uurtarief €45 – €75; oude kraan verwijderen en afvoeren €10 – €30.
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/douchekraan-vervangen
- Werkspot, sanitair plaatsen: kraan €150 – €450 (zie richtprijzen.py, werkspot_sanitair).
- Homedeal, nieuwe douche 2026: douchecabine gemiddeld €1.800 (€430 – €5.200), inloopdouche €430 – €4.000,
  incl. montage en btw (zie richtprijzen.py, homedeal_douche).
- Homedeal, ventilatie badkamer (incl. montage): basisventilator €150 – €250, met timer €200 – €300, met
  vochtsensor €250 – €500, aansluiten op een bestaand centraal systeem €250 – €450, nieuwe mechanische
  ventilatie-unit voor de hele woning €1.700 – €7.000. De pagina zegt niet of dit incl. btw is; wij
  rekenen ermee als bedrag inclusief btw en houden een ruime marge.
  https://www.homedeal.nl/ventilatie/ventilatie-badkamer/
- Milieu Centraal, ventilatie met mechanische afvoer: tijdens het douchen op de hoogste stand en laten nadraaien;
  ventielen jaarlijks schoonmaken, box eens per 2 jaar laten onderhouden, kanalen eens per 8 jaar reinigen;
  gelijkstroommotor (DC) gebruikt veel minder stroom; ISDE-subsidie €400 voor een energiezuinig
  ventilatiesysteem vanaf 2026, alleen samen met minstens één isolatiemaatregel en niet bij zelf installeren.
  https://www.milieucentraal.nl/energie-besparen/ventilatie/ventilatie-met-mechanische-afvoer/
- Homedeal, zolder verbouwen: badkamer op zolder €20.000 – €35.000; gipswand €40 – €50 per m²
  (zie badkamer_kosten.py, homedeal_zolder).
- Werkspot, tegels verven: alleen als achtergrond; tegelverf is een goedkope, minder duurzame oplossing.
  https://www.werkspot.nl/tegels-verven/prijzen-kosten

Eigen inschattingen (staan op de pagina als eigen inschatting):
- inbouwkraan vervangen inclusief hak- en tegelwerk €600 – €1.500;
- ventilatiekanaal door de gevel of het dak €150 – €400 extra;
- tegelverf door een vakman €25 – €50 per m²; voegen vernieuwen €20 – €40 per m² (zoals badkamer_kosten.py);
- extra voor inbouwkranen en inbouwdelen in een luxe badkamer €400 – €1.200.
"""

import datetime

from components import eur
import richtprijzen as RP

JAAR = datetime.date.today().year

TOTAAL = None  # zelfde markering als in badkamer_kosten: de totaalregel van een rekenvoorbeeld

# Nieuwe bronnen. De hoofdsessie voegt ze toe met B.update(B3).
B3 = {
    "homedeal_klein": ("Homedeal, kleine badkamer verbouwen", "https://www.homedeal.nl/badkamerspecialist/kleine-badkamer-verbouwen/"),
    "homedeal_aanleggen": ("Homedeal, badkamer aanleggen kosten", "https://www.homedeal.nl/badkamerspecialist/badkamer-aanleggen-kosten/"),
    "slimster_vrijstaand": ("Slimster, vrijstaand bad plaatsen", "https://slimster.nl/badkamer/bad-plaatsen-kosten/vrijstaand-bad/"),
    "werkspot_wastafel": ("Werkspot, wastafel plaatsen prijzen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/wastafel"),
    "slimster_wastafel": ("Slimster, wastafel plaatsen kosten", "https://slimster.nl/badkamer/wastafel-plaatsen-kosten/"),
    "werkspot_douchekraan": ("Werkspot, douchekraan vervangen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/douchekraan-vervangen"),
    "homedeal_ventilatie": ("Homedeal, ventilatie in de badkamer", "https://www.homedeal.nl/ventilatie/ventilatie-badkamer/"),
    "mc_ventilatie": ("Milieu Centraal, ventilatie met mechanische afvoer", "https://www.milieucentraal.nl/energie-besparen/ventilatie/ventilatie-met-mechanische-afvoer/"),
    "werkspot_tegelverf": ("Werkspot, tegels verven prijzen", "https://www.werkspot.nl/tegels-verven/prijzen-kosten"),
}

# Bronnen die in badkamer_kosten.B (of via richtprijzen.BRONNEN) al bestaan en die we hier ook gebruiken:
# homedeal_badkamer, trustoo_badkamer, slimster_badkamer, werkspot_tegel, werkspot_sanitair, homedeal_douche,
# slimster_douche, homedeal_lood, trustoo_lood, werkspot_kit, homedeal_zolder, werkspot_zolder, btw, asbest.


# ---------------------------------------------------------------------------
# Helpers (zelfde werking als in badkamer_kosten.py)
# ---------------------------------------------------------------------------

def rp(sleutel, factor=1):
    """(laag, hoog) uit richtprijzen.py, eventueel maal een aantal, afgerond op hele euro's."""
    lo, hi = RP.lh(sleutel, factor)
    return (int(round(lo)), int(round(hi)))


def niv(sleutel, niveau):
    lo, hi = RP.RICHTPRIJZEN[sleutel]["niveaus"][niveau]
    return (lo, hi)


def som(*paren):
    return (sum(p[0] for p in paren), sum(p[1] for p in paren))


def rb(sleutel, factor=1):
    lo, hi = rp(sleutel, factor)
    return f"{eur(lo)} – {eur(hi)}"


def bt(paar):
    """Bandbreedte als tekst."""
    return f"{eur(paar[0])} – {eur(paar[1])}"


def incl(paar):
    """Bedrag exclusief btw omrekenen naar inclusief 21% btw, afgerond op hele euro's."""
    return (int(round(paar[0] * 1.21)), int(round(paar[1] * 1.21)))


def uren(aantal_laag, aantal_hoog):
    """Arbeid in uren tegen het uurtarief uit richtprijzen.py, omgerekend naar inclusief btw."""
    lo, hi = rp("uurtarief")
    return incl((lo * aantal_laag, hi * aantal_hoog))


def opbouw(materiaal, arbeid, extra, totaal_label="Totaal, inclusief 21% btw"):
    """Kostenopbouw in drie blokken (materiaal, arbeid, extra's) met per blok een subtotaal.
    Geeft rijen in het formaat van badkamer_kosten.voorbeeld_rijen: (label, (laag, hoog)) wordt opgeteld,
    (label, tekst) blijft tekst, (label, TOTAAL) wordt de som van alle bedragen."""
    rijen = []
    for kop, posten in (("Materiaal", materiaal), ("Arbeid", arbeid), ("Extra's", extra)):
        if not posten:
            continue
        rijen.append((f"<strong>{kop}</strong>", ""))
        rijen += posten
        sub = som(*(w for _, w in posten))
        rijen.append((f"<em>Subtotaal {kop.lower()}</em>", f"<em>{bt(sub)}</em>"))
    rijen.append((totaal_label, TOTAAL))
    return rijen


def totaal(rijen):
    return som(*(w for _, w in rijen if isinstance(w, tuple)))


def r100(paar):
    """Afronden op honderdtallen (laag omlaag, hoog omhoog), voor teksten bij een rekenvoorbeeld."""
    return (paar[0] // 100 * 100, -(-paar[1] // 100) * 100)


# Vaste, gedeelde stukjes
UUR_INCL = incl(rp("uurtarief"))          # uurtarief loodgieter inclusief btw
VOORRIJ_INCL = incl(rp("voorrijkosten"))  # voorrijkosten inclusief btw
OUDE_KRAAN = (10, 30)                     # Werkspot: oude kraan verwijderen en afvoeren
KRAAN_WERKSPOT = (150, 450)               # Werkspot, sanitair plaatsen: kraan
VOEGEN_M2 = (20, 40)                      # eigen inschatting, zoals badkamer_kosten.py
TEGELVERF_M2 = (25, 50)                   # eigen inschatting, door een vakman
GIPSWAND_M2 = (40, 50)                    # Homedeal, zolder verbouwen
KANAAL = (150, 400)                       # eigen inschatting, kanaal door gevel of dak
INBOUW_EXTRA = (400, 1200)                # eigen inschatting, inbouwkranen en inbouwdelen

EIGEN = ("Dit is een eigen rekenvoorbeeld op basis van de bronnen hieronder, met dezelfde richtprijzen per post "
         "als de badkamercalculator. Het laat zien hoe de prijs is opgebouwd uit materiaal, arbeid en extra's. "
         "Je eigen badkamer kan hoger of lager uitkomen.")


# ---------------------------------------------------------------------------
# Rekenvoorbeelden (kostenopbouw)
# ---------------------------------------------------------------------------

# 1. Kleine badkamer: 1,5 × 2 m (3 m²), alles op dezelfde plek, wanden tot het plafond: ~18 m² tegelwerk.
_KLEIN = opbouw(
    materiaal=[
        (f"Tegels, 18 m² × {rb('tegels')}", rp("tegels", 18)),
        ("Hulpmateriaal: lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 18)),
        ("Sanitair (basis): douche met glazen wand, toilet, fonteintje of smal meubel",
         som(niv("sanitair_douche", "basis"), niv("sanitair_toilet", "basis"), niv("sanitair_meubel", "basis"))),
    ],
    arbeid=[
        ("Slopen van de oude badkamer (3 m²)", som(rp("sloop_vast"), rp("sloop_m2", 3))),
        ("Leidingwerk water en afvoer, op dezelfde plek", rp("leidingwerk")),
        (f"Legloon tegelwerk, 18 m² × {rb('tegelwerk')}", rp("tegelwerk", 18)),
        ("Waterdicht maken van de douchehoek", rp("waterdicht")),
        ("Montage van douche, toilet en meubel", som(rp("montage_douche"), rp("montage_toilet"), rp("montage_meubel"))),
    ],
    extra=[
        ("Afvoer van het sloopafval", rp("afval")),
        ("Elektra: groep, stopcontact en spots", rp("elektra")),
        ("Ventilator met vochtsensor", rp("ventilator")),
        ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
    ],
)

# 2. Luxe badkamer: 3 × 3 m (9 m²), toilet verplaatst, ~35 m² tegelwerk in groot formaat, vrijstaand bad,
#    inloopdouche met regendouche, dubbel meubel, vloerverwarming.
_LUXE = opbouw(
    materiaal=[
        (f"Tegels (luxe), 35 m² × {bt(niv('tegels', 'luxe'))}", (niv("tegels", "luxe")[0] * 35, niv("tegels", "luxe")[1] * 35)),
        ("Hulpmateriaal: lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 35)),
        ("Inloopdouche met regendouche en inbouwkraan (luxe)", niv("sanitair_douche", "luxe")),
        ("Vrijstaand bad met kraan (luxe)", niv("sanitair_bad", "luxe")),
        ("Hangtoilet met inbouwreservoir (luxe)", niv("sanitair_toilet", "luxe")),
        ("Dubbel wastafelmeubel met spiegel (luxe)", niv("sanitair_meubel", "luxe")),
    ],
    arbeid=[
        ("Slopen tot op de ruwe vloer, met afvoer", rp("sloop_compleet")),
        ("Leidingwerk water en afvoer", rp("leidingwerk")),
        ("Extra: toilet en afvoer verplaatsen", rp("leidingwerk_verplaatsen")),
        (f"Legloon tegelwerk, 35 m² × {rb('tegelwerk')}", rp("tegelwerk", 35)),
        ("Waterdicht maken van douche en badhoek", rp("waterdicht")),
        ("Montage van douche, bad, toilet en meubel",
         som(rp("montage_douche"), rp("montage_bad"), rp("montage_toilet"), rp("montage_meubel"))),
    ],
    extra=[
        ("Inbouwkranen en inbouwdelen (eigen inschatting)", INBOUW_EXTRA),
        ("Elektrische vloerverwarming", rp("vloerverwarming_elektrisch")),
        ("Elektra en verlichting", rp("elektra")),
        ("Ventilator met vochtsensor", rp("ventilator")),
        ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
    ],
)

# 3. Badkamer opknappen: 5 m², tegels blijven, alles op dezelfde plek.
_OPKNAP = opbouw(
    materiaal=[
        ("Nieuw wastafelmeubel met kraan en spiegel (basis)", niv("sanitair_meubel", "basis")),
        ("Thermostatische douchekraan met glijstang", (50, 300)),
        ("Nieuwe douchewand (basis)", (250, 500)),
    ],
    arbeid=[
        (f"Voegen vernieuwen, 8 m² × {bt(VOEGEN_M2)}", (VOEGEN_M2[0] * 8, VOEGEN_M2[1] * 8)),
        ("Hele badkamer opnieuw afkitten", rp("kitwerk_badkamer")),
        ("Wastafelmeubel ophangen en aansluiten", rp("montage_meubel")),
        ("Douchekraan en douchewand monteren (2 tot 4 uur)", uren(2, 4)),
    ],
    extra=[
        ("Voorrijkosten", VOORRIJ_INCL),
        ("Ventilator met vochtsensor", rp("ventilator")),
        ("Oude onderdelen afvoeren", OUDE_KRAAN),
    ],
)

# 4. Douche vervangen: douchebak met wand eruit, douchehoek 0,9 × 1,2 m opnieuw betegelen, inloopwand.
_DOUCHE = opbouw(
    materiaal=[
        ("Douche (midden): goot of vlakke bak, glazen wand en thermostaatkraan", niv("sanitair_douche", "midden")),
        (f"Tegels douchehoek, 8 m² × {rb('tegels')}", rp("tegels", 8)),
        ("Hulpmateriaal: lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 8)),
    ],
    arbeid=[
        ("Oude douche en tegels in de douchehoek verwijderen (3 tot 6 uur)", uren(3, 6)),
        ("Afvoer en kraanpunten aanpassen (2 tot 5 uur)", uren(2, 5)),
        ("Waterdicht maken met kimband en afschot", rp("waterdicht")),
        (f"Legloon tegelwerk, 8 m² × {rb('tegelwerk')}", rp("tegelwerk", 8)),
        ("Douche, wand en kraan plaatsen en aansluiten", rp("montage_douche")),
    ],
    extra=[
        ("Afvoer van het sloopafval (klein)", (50, 150)),
        ("Kitwerk rond douche en wand", (VOEGEN_M2[0] * 3, VOEGEN_M2[1] * 3)),
    ],
)

# 5. Wastafel vervangen: oud meubel eruit, nieuw hangend meubel met kraan op dezelfde plek.
_WASTAFEL = opbouw(
    materiaal=[
        ("Wastafelmeubel met wastafel en spiegel (midden)", niv("sanitair_meubel", "midden")),
        ("Wastafelkraan", (50, 300)),
        ("Sifon, stopkranen en flexibele slangen", (30, 80)),
    ],
    arbeid=[
        ("Oud meubel demonteren en afvoeren", uren(0.5, 1)),
        ("Nieuw meubel ophangen en aansluiten", rp("montage_meubel")),
    ],
    extra=[
        ("Voorrijkosten", VOORRIJ_INCL),
        ("Gaten in de tegels dichtmaken of nieuwe pluggen", (0, 100)),
        ("Stopcontact bij de spiegel (als er nog geen is)", (0, 250)),
    ],
)

# 6. Kraan vervangen: thermostatische douchekraan (opbouw) op dezelfde plek.
_KRAAN = opbouw(
    materiaal=[
        ("Thermostatische douchekraan (opbouw)", (50, 300)),
        ("Nieuwe koppelingen, S-koppelingen en rozetten", (15, 40)),
    ],
    arbeid=[
        ("Oude kraan eraf, nieuwe kraan monteren en testen (1 tot 2 uur)", uren(1, 2)),
    ],
    extra=[
        ("Voorrijkosten", VOORRIJ_INCL),
        ("Oude kraan verwijderen en afvoeren", OUDE_KRAAN),
    ],
)

# 7. Badkamerventilatie: losse ventilator met vochtsensor, nieuw kanaal door de gevel, aparte schakeling.
_VENT = opbouw(
    materiaal=[
        ("Ventilator met vochtsensor en terugslagklep", (100, 300)),
        ("Kanaal, muurdoorvoer en buitenrooster", (40, 120)),
    ],
    arbeid=[
        ("Gat boren door de gevel en kanaal leggen (eigen inschatting)", KANAAL),
        ("Ventilator monteren en elektrisch aansluiten (1 tot 2 uur)", uren(1, 2)),
    ],
    extra=[
        ("Voorrijkosten", VOORRIJ_INCL),
        ("Wand bijwerken rond de doorvoer", (0, 150)),
    ],
)

# 8. Tweede badkamer: 2 × 2 m (4 m²) in een hoek van een slaapkamer op de verdieping, met douche, toilet en
#    wastafel. Nieuwe wanden, nieuwe aansluitingen op de bestaande standleiding.
_TWEEDE = opbouw(
    materiaal=[
        (f"Tegels, 22 m² × {rb('tegels')}", rp("tegels", 22)),
        ("Hulpmateriaal: lijm, voegsel en kit", rp("tegelwerk_hulpmateriaal", 22)),
        ("Sanitair (midden): douche, hangtoilet en wastafelmeubel",
         som(niv("sanitair_douche", "midden"), niv("sanitair_toilet", "midden"), niv("sanitair_meubel", "midden"))),
    ],
    arbeid=[
        (f"Twee nieuwe wanden, 12 m² gipswand × {bt(GIPSWAND_M2)}", (GIPSWAND_M2[0] * 12, GIPSWAND_M2[1] * 12)),
        ("Nieuw leidingwerk water en afvoer", rp("leidingwerk")),
        ("Extra: nieuwe afvoer naar de standleiding", rp("leidingwerk_verplaatsen")),
        ("Waterdichte vloer en douchehoek", rp("waterdicht")),
        (f"Legloon tegelwerk, 22 m² × {rb('tegelwerk')}", rp("tegelwerk", 22)),
        ("Montage van douche, toilet en meubel", som(rp("montage_douche"), rp("montage_toilet"), rp("montage_meubel"))),
    ],
    extra=[
        ("Elektra: nieuwe groep, stopcontact en verlichting", rp("elektra")),
        ("Ventilator met kanaal naar buiten", som(rp("ventilator"), KANAAL)),
        ("Elektrische vloerverwarming", rp("vloerverwarming_elektrisch")),
        ("Deur met kozijn", (300, 800)),
        ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
    ],
)

T_KLEIN, T_LUXE, T_OPKNAP, T_DOUCHE = totaal(_KLEIN), totaal(_LUXE), totaal(_OPKNAP), totaal(_DOUCHE)
T_WASTAFEL, T_KRAAN, T_VENT, T_TWEEDE = totaal(_WASTAFEL), totaal(_KRAAN), totaal(_VENT), totaal(_TWEEDE)


# ---------------------------------------------------------------------------
# De acht pagina's
# ---------------------------------------------------------------------------

KOSTEN3 = [
    # ------------------------------------------------------------------ 1
    {
        "slug": "kleine-badkamer",
        "kort": "Kleine badkamer",
        "omschrijving": "Wat een kleine badkamer van 2 tot 4 m² kost, en waarom die per m² duurder is.",
        "h1": f"Wat kost een kleine badkamer in {JAAR}?",
        "title": f"Kosten kleine badkamer {JAAR}: 2 tot 4 m²",
        "description": "Een kleine badkamer van 2 tot 4 m² kost meestal €4.500 tot €13.000, inclusief 21% btw. Met kostenopbouw, drie voorbeelden en tips om ruimte en geld te sparen.",
        "dienst": "badkamer-renoveren",
        "van": 4500, "tot": 13000, "eenheid": "per kleine badkamer van 2 tot 4 m², inclusief btw",
        "snel": "Een complete kleine badkamer van 2 tot 4 m² kost meestal <strong>€4.500 tot €13.000</strong>, inclusief sloop, leidingwerk, tegels, sanitair, montage en 21% btw. Per m² is dat duurder dan een grote badkamer: een douche, toilet en wastafel kosten hetzelfde, of je nu 3 of 8 m² hebt. Wie alles op dezelfde plek laat en basissanitair kiest, blijft aan de onderkant.",
        "varianten": [
            ("Budget", 4500, 7000, "Alles op dezelfde plek, standaard tegels 30 × 60 cm, douche met glazen wand, staand of eenvoudig hangtoilet, fonteintje of smal meubel."),
            ("Midden", 7000, 10000, "Inloopdouche met goot, hangtoilet, wandmeubel op maat van de ruimte, tegels tot het plafond en een ventilator met vochtsensor."),
            ("Luxe", 10000, 14000, "Grote tegels of microcement, inbouwkranen, nis in de douchewand, spiegelkast met licht en vloerverwarming. Soms een verplaatste afvoer."),
        ],
        "varianten_eenheid": "Totaalprijs per kleine badkamer van 2 tot 4 m², inclusief materiaal, arbeid en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Homedeal (3 m² €4.000 – €6.500, 4 m² €4.500 – €7.000) en Trustoo (compacte badkamer 3 – 4 m² €8.250 – €12.000). De grens tussen de scenario's is een eigen inschatting.",
        "factoren": [
            ("Vaste kosten wegen zwaar", "Sloop, leidingwerk, elektra en sanitair kosten in een kleine badkamer bijna hetzelfde als in een grote. Daarom kost een kleine badkamer al snel €1.500 tot €3.000 per m². Homedeal noemt voor 2 m² al €3.500 tot €5.000."),
            ("Of de indeling verandert", "In een kleine ruimte wil je soms de deur of het toilet verplaatsen om plek te maken. Dat kost extra leidingwerk: "
             f"{rb('leidingwerk_verplaatsen')}. Teken eerst wat er kan met de <a href=\"/tools/indelingsplanner/\">indelingsplanner</a>."),
            ("Maatwerk of standaard", "Een wastafel van 40 cm diep of een douchewand op maat kost meer dan standaardmaten. Kijk eerst of er een standaardmaat past; die zijn er ook in smalle uitvoeringen."),
            ("Hoe ver je tegelt", "In een kleine badkamer zijn de wanden al snel groter dan de vloer. Tegels tot het plafond: zo'n 15 tot 20 m² tegelwerk. Tegel je alleen tot 1,20 m buiten de douche, dan scheelt dat flink."),
            ("Bereikbaarheid", "Een kleine badkamer op de verdieping, zonder plek voor een container, kost meer tijd voor sloop en afvoer. Ook werken twee vakmensen niet goed tegelijk in 3 m², dus de doorlooptijd is niet veel korter dan bij een grotere badkamer."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 1,5 bij 2 meter (3 m²) op de verdieping. Douche, toilet en wastafel blijven op hun plek. De wanden worden tot het plafond betegeld: samen met de vloer zo'n 18 m². Het sanitair is basis.",
            _KLEIN,
            EIGEN + f" Met sanitair uit het middensegment komt dezelfde badkamer zo'n {bt(r100((T_KLEIN[0] + 1000, T_KLEIN[1] + 2300)))} uit.",
        ),
        "btw_extra": "Een kleine badkamer valt voor de btw niet anders dan een grote: tegelwerk, loodgieterswerk en sanitair zijn altijd 21%.",
        "besparen": [
            "Laat toilet, douche en wastafel op hun plek. In een kleine badkamer is het leidingwerk een groot deel van de prijs.",
            "Kies een glazen douchewand in plaats van een cabine of gordijn: hetzelfde budget, maar de ruimte voelt groter.",
            "Een hangtoilet en een zwevend meubel kosten iets meer, maar je houdt vloer vrij en schoonmaken gaat makkelijker. Spaar liever op tegels dan op die twee.",
            "Gebruik één tegel voor vloer en wand. Je hebt minder snijverlies en minder restanten.",
            "Vraag om een vaste prijs voor het hele werk. Bij een kleine badkamer zijn de uren moeilijk te schatten, en een uurtarief loopt snel op.",
        ],
        "specialist": "Ook een kleine badkamer is werk voor een badkamerspecialist. Er zit net zoveel leidingwerk, waterdicht maken en elektra in als in een grote badkamer, maar je hebt minder speling. Een douche die niet goed afloopt of een kimband die lekt, merk je in een kleine ruimte meteen aan de muren ernaast. Wil je eerst ideeën opdoen, lees dan <a href=\"/kennisbank/kleine-badkamer-indelen/\">een kleine badkamer indelen</a>.",
        "faqs": [
            ("Wat kost een badkamer van 3 m²?", "Reken op €4.000 tot €10.000, inclusief btw. Homedeal noemt €4.000 tot €6.500 voor een eenvoudige badkamer van 3 m². Trustoo noemt voor een compacte badkamer van 3 tot 4 m² €8.250 tot €12.000, inclusief basismateriaal. Het verschil zit vooral in het sanitair en of er iets verplaatst wordt."),
            ("Waarom is een kleine badkamer per m² zo duur?", "Omdat de duurste posten vaste kosten zijn: een douche, toilet, wastafel, leidingwerk en elektra heb je in elke badkamer. In een kleine badkamer deel je die door minder vierkante meters."),
            ("Past er een inloopdouche in een kleine badkamer?", "Vaak wel. Met 80 × 80 cm kun je douchen, 90 × 120 cm is comfortabel. Een inloopdouche zonder drempel loopt over in de vloer, waardoor de ruimte groter lijkt. Lees meer over <a href=\"/kosten/inloopdouche/\">de kosten van een inloopdouche</a>."),
            ("Hoe lang duurt een kleine badkamer?", "Meestal een tot twee weken. Het werk is minder, maar droogtijden van de vloer, de waterdichte laag en de lijm blijven hetzelfde."),
            ("Kan een toilet in de badkamer als er weinig ruimte is?", "Ja. Je hebt voor een toilet zo'n 80 cm breedte nodig en 60 cm vrije ruimte ervoor. Een hangtoilet met inbouwreservoir is 10 tot 15 cm minder diep dan een staand toilet met duoblok."),
        ],
        "bronnen": ["homedeal_klein", "trustoo_badkamer", "homedeal_badkamer", "werkspot_tegel", "slimster_slopen", "werkspot_puin", "btw"],
        "verwant": ["nieuwe-badkamer", "inloopdouche", "badkamermeubel-plaatsen"],
        "kennis": [("/kennisbank/kleine-badkamer-indelen/", "Een kleine badkamer slim indelen"),
                   ("/tools/indelingsplanner/", "Probeer indelingen met de indelingsplanner"),
                   ("/kennisbank/grote-tegels-badkamer/", "Grote tegels in een kleine badkamer: werkt dat?")],
    },
    # ------------------------------------------------------------------ 2
    {
        "slug": "luxe-badkamer",
        "kort": "Luxe badkamer",
        "omschrijving": "Wat een luxe badkamer kost met vrijstaand bad, inbouwkranen en grote tegels.",
        "h1": f"Wat kost een luxe badkamer in {JAAR}?",
        "title": f"Kosten luxe badkamer {JAAR}: richtprijzen",
        "description": "Een luxe badkamer kost meestal €15.000 tot €30.000, inclusief 21% btw. Zie wat een vrijstaand bad, inbouwkranen, grote tegels en vloerverwarming toevoegen.",
        "dienst": "badkamer-renoveren",
        "van": 15000, "tot": 30000, "eenheid": "per luxe badkamer van 8 tot 12 m², inclusief btw",
        "snel": "Een luxe badkamer van 8 tot 12 m² kost meestal <strong>€15.000 tot €30.000</strong>, inclusief sloop, leidingwerk, tegels, sanitair, montage en 21% btw. Homedeal noemt voor een luxe badkamer van 12 m² €20.000 tot €30.000. Het verschil met een gewone badkamer zit niet in één ding, maar in veel extra's samen: grote tegels, inbouwkranen, een vrijstaand bad, vloerverwarming en verlichting.",
        "varianten": [
            ("Budget (luxe instap)", 12000, 18000, "Inloopdouche met regendouche, hangtoilet, wastafelmeubel uit het hogere segment, tegels 60 × 120 cm en vloerverwarming. Indeling blijft gelijk."),
            ("Midden", 18000, 25000, "Daarbij een vrijstaand bad, inbouwkranen, een dubbel meubel, een nis met verlichting en een verplaatst toilet of verplaatste afvoer."),
            ("Luxe", 25000, 35000, "Natuursteen of grote keramische platen, maatwerkmeubel, stoomdouche of whirlpool, slimme verlichting en een badkamer van 10 m² of meer."),
        ],
        "varianten_eenheid": "Totaalprijs per badkamer van 8 tot 12 m², inclusief materiaal, arbeid en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Homedeal (luxe €10.000 – €15.000, voorbeeld luxe 12 m² €20.000 – €30.000) en Slimster (luxe €11.000 – €15.000 inclusief installatie). De bovengrens is open; die is een eigen inschatting.",
        "factoren": [
            ("Groot formaat tegels en natuursteen", f"Luxe tegels kosten zo'n {bt(niv('tegels', 'luxe'))} per m², natuursteen vaak meer. Platen van 120 cm of groter vragen een heel vlakke ondergrond en twee mensen om te leggen. Dat kost meer legloon dan een tegel van 30 × 60 cm."),
            ("Inbouwkranen", "Een inbouwkraan zit in de muur. Het inbouwdeel moet vóór het tegelwerk precies goed zitten, en is later lastig te vervangen. Reken op €400 tot €1.200 extra aan inbouwdelen en werk (eigen inschatting), bovenop de kranen zelf."),
            ("Vrijstaand bad", f"Een vrijstaand bad kost {bt(niv('sanitair_bad', 'luxe'))} in het luxe segment; Slimster noemt rond €2.000 voor alleen het bad. De afvoer en de kraan komen uit de vloer, dus de vloer moet open. Controleer ook of de vloer het gewicht met water kan dragen: 250 tot 400 kg."),
            ("Leidingen verplaatsen", f"Een luxe indeling betekent vaak dat toilet, douche of bad op een andere plek komen. Dat kost {rb('leidingwerk_verplaatsen')} extra, en meer als de vloer van beton is."),
            ("Wellness-extra's", "Homedeal noemt voor een stoomdouche €1.600 tot €4.300 en voor een whirlpool €2.700 tot €6.700, inclusief montage en btw. Ook een designradiator, een spiegel met verwarming en dimbare verlichting tellen op."),
            ("Ontwerp en regie", "Bij een luxe badkamer werken vaak meer vakmensen na elkaar: loodgieter, elektricien, tegelzetter, soms een meubelmaker. Een goede planning en één aanspreekpunt zijn dan het geld waard."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 3 bij 3 meter (9 m²). Het toilet gaat naar een andere wand. Er komt een inloopdouche met regendouche en inbouwkraan, een vrijstaand bad, een dubbel meubel en vloerverwarming. Wanden tot het plafond in groot formaat: zo'n 35 m² tegelwerk.",
            _LUXE,
            EIGEN + " Met natuursteen, een maatwerkmeubel of een stoomdouche kom je hoger uit.",
        ),
        "btw_extra": "Voor luxe sanitair en wellness-extra's geldt ook 21%. Een stoomdouche of whirlpool is geen medisch hulpmiddel en valt niet onder een lager tarief.",
        "besparen": [
            "Kies één blikvanger, zoals het bad of de douche, en houd de rest rustig. Twee dure tegels naast elkaar ziet niemand.",
            "Gebruik grote tegels op de vloer en de douchewand, en een eenvoudiger tegel of vochtbestendig stucwerk op de andere wanden.",
            "Laat de afvoer van het bad op de plek van de oude afvoer uitkomen. Een vrijstaand bad hoeft niet midden in de ruimte te staan.",
            "Een opbouw-regendouche met thermostaat geeft bijna hetzelfde gevoel als een inbouwset, voor minder geld en met makkelijker onderhoud.",
            "Vraag offertes met de sanitairlijst erbij, niet met een stelpost. Bij luxe sanitair kan een stelpost duizenden euro's te laag zijn.",
        ],
        "specialist": "Een luxe badkamer is werk voor een badkamerspecialist met ervaring in inbouwkranen, grote tegels en vloerverwarming. Vraag naar foto's van eerder werk met dezelfde tegels en vraag hoe ze de ondergrond vlak maken. Bij een vrijstaand bad of veel natuursteen op een houten vloer laat je de draagkracht controleren door een constructeur. Inspiratie vind je bij <a href=\"/inspiratie/luxe-badkamer/\">luxe badkamers</a>.",
        "faqs": [
            ("Vanaf wanneer is een badkamer luxe?", "Daar is geen vaste grens voor. Homedeal rekent luxe vanaf zo'n €10.000. In de praktijk spreek je van luxe als er inbouwkranen, een regendouche, grote tegels of natuursteen, vloerverwarming en vaak een vrijstaand bad in komen."),
            ("Wat kost een vrijstaand bad met plaatsing?", f"Het bad zelf kost in het luxe segment {bt(niv('sanitair_bad', 'luxe'))}. Plaatsen en aansluiten kost {rb('montage_bad')}. Omdat de afvoer en vaak de kraan uit de vloer komen, komt daar werk aan de vloer bij. Zie ook <a href=\"/kosten/bad-plaatsen/\">de kosten van een bad plaatsen</a>."),
            ("Zijn inbouwkranen het geld waard?", "Ze zijn mooi en makkelijk schoon te houden, want er zit niets op de muur. Maar ze kosten meer, en een defect inbouwdeel betekent soms tegels eruit. Kies een bekend systeem waarvan onderdelen lang te krijgen zijn. Lees meer in <a href=\"/kennisbank/inbouwkranen/\">inbouwkranen: voor- en nadelen</a>."),
            ("Hoe lang duurt een luxe badkamer?", "Reken op drie tot vijf weken. Grote tegels, vloerverwarming en een nieuwe dekvloer hebben langer droogtijd nodig, en maatwerk heeft een levertijd."),
            ("Kan een luxe badkamer in een appartement?", "Ja, maar vraag eerst wat de VvE toestaat. Vooral de afvoer, het gewicht van een bad en geluid naar de buren zijn punten. Lees <a href=\"/kennisbank/verbouwen-in-vve/\">verbouwen in een VvE</a>."),
        ],
        "bronnen": ["homedeal_aanleggen", "homedeal_badkamer", "slimster_badkamer", "slimster_vrijstaand", "trustoo_badkamer", "werkspot_tegel", "werkspot_vv", "btw"],
        "verwant": ["nieuwe-badkamer", "bad-plaatsen", "vloerverwarming-badkamer"],
        "kennis": [("/inspiratie/luxe-badkamer/", "Inspiratie voor een luxe badkamer"),
                   ("/kennisbank/inbouwkranen/", "Inbouwkranen: voor- en nadelen"),
                   ("/kennisbank/regendouche/", "Waar let je op bij een regendouche?"),
                   ("/badkamerspullen/vrijstaand-bad-kopen/", "Een vrijstaand bad kopen")],
    },
    # ------------------------------------------------------------------ 3
    {
        "slug": "badkamer-opknappen",
        "kort": "Badkamer opknappen",
        "omschrijving": "Wat het kost om je badkamer op te frissen zonder alles te slopen.",
        "h1": f"Wat kost een badkamer opknappen in {JAAR}?",
        "title": f"Kosten badkamer opknappen {JAAR}: zonder slopen",
        "description": "Een badkamer opknappen zonder slopen kost meestal €750 tot €4.000, inclusief 21% btw. Met kostenopbouw, drie voorbeelden en wanneer opknappen niet meer genoeg is.",
        "dienst": "badkamer-onderhoud",
        "van": 750, "tot": 4000, "eenheid": "per badkamer, zonder sloop, inclusief btw",
        "snel": "Een badkamer opknappen zonder te slopen kost meestal <strong>€750 tot €4.000</strong>, inclusief 21% btw. Daarvoor krijg je bijvoorbeeld nieuwe kit en voegen, een nieuwe douchekraan en douchewand, en een nieuw wastafelmeubel. De tegels en de leidingen blijven. Leg je ook nieuwe tegels over de oude, dan kom je op €4.000 tot €7.000.",
        "varianten": [
            ("Budget: opfrissen", 500, 1500, "Kit en voegen vernieuwen, nieuwe douchekraan en glijstang, nieuwe accessoires en een ventilator. Alles op de bestaande plek."),
            ("Midden: opknappen", 1500, 4000, "Daarbij een nieuw wastafelmeubel met spiegel, een nieuwe douchewand en eventueel een nieuwe toiletpot of zitting."),
            ("Luxe: groot opknappen", 4000, 7000, "Nieuwe tegels over de oude heen of wandpanelen, nieuwe vloertegels, nieuw sanitair op dezelfde plek. Leidingen en afvoer blijven."),
        ],
        "varianten_eenheid": "Totaalprijs per badkamer van zo'n 5 m², inclusief materiaal, arbeid en btw",
        "varianten_noot": "Eigen voorbeeldscenario's, opgebouwd uit de richtprijzen per post: kitwerk (Werkspot en Slimster), montage en sanitair (Werkspot, Trustoo), uurtarief (Homedeal).",
        "factoren": [
            ("De staat van de tegels en de ondergrond", "Opknappen werkt alleen als de tegels vast zitten en er geen vocht achter zit. Klinkt een tegel hol als je erop tikt, of zie je zwarte voegen die niet schoon worden, dan zit er mogelijk vocht achter. Dan is opknappen zonde van het geld."),
            ("Hoeveel je vervangt", f"Alleen kit en voegen kost een paar honderd euro: hele badkamer afkitten {rb('kitwerk_badkamer')}, voegen vernieuwen €20 – €40 per m² (eigen inschatting). Een nieuw meubel, nieuwe kranen of een nieuwe douchewand tellen er per stuk bij op."),
            ("Tegels over tegels", f"Nieuwe tegels over de oude kan als de ondergrond vlak en vast is. Je betaalt dan de tegels ({rb('tegels')} per m²) en het legloon ({rb('tegelwerk')} per m²), maar geen sloop. Let op: de vloer wordt hoger, en de deur en de afvoer moeten daarbij passen."),
            ("Tegelverf of wandpanelen", "Tegelverf is het goedkoopst, maar in de douche slijt het snel. Een vakman rekent zo'n €25 tot €50 per m² (eigen inschatting). Waterdichte wandpanelen zijn duurder, maar gaan langer mee."),
            ("Kleine klussen samen", f"Een loodgieter rekent {rb('uurtarief')} per uur exclusief btw, plus voorrijkosten. Laat meerdere klussen op één dag doen. Dan betaal je één keer voorrijkosten en geen halve uren."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 5 m² met tegels uit 2005 die nog vast zitten. Je laat de kit en de voegen in de douche vernieuwen, een nieuw wastafelmeubel ophangen, en de douchekraan en douchewand vervangen.",
            _OPKNAP,
            EIGEN,
        ),
        "btw_extra": "Laat je bij het opknappen ook het plafond of de wanden boven de tegels verven of stukadoren, dan kan dat arbeidsloon onder 9% vallen als de woning ouder is dan twee jaar. Kitwerk, voegen, tegelwerk en loodgieterswerk blijven 21%.",
        "besparen": [
            "Begin met schoonmaken en ontkalken. Een badkamer met witte voegen en nieuwe kit ziet er vaak jaren jonger uit.",
            "Vervang onderdelen die je elke dag ziet en gebruikt: kraan, douchewand, spiegel en verlichting. Daar zit het meeste effect voor het minste geld.",
            "Kies een meubel met dezelfde breedte als het oude. Dan passen de aansluitingen en hoef je geen gaten in de tegels te dichten.",
            "Bundel klussen op één dag, zodat je één keer voorrijkosten betaalt.",
            "Houd 10 tot 15% van je budget achter de hand. Onder een oud meubel of achter een oude douchebak kom je soms een verrassing tegen.",
        ],
        "specialist": "Kit, accessoires en een nieuwe spiegel kun je vaak zelf. Een nieuwe kraan of meubel ook, als je weet hoe je de water afsluit en lekvrij aansluit. Voegen vernieuwen in de douche, tegels over tegels en een nieuwe douchewand laat je beter aan een vakman over. Zie je vocht achter de tegels of schimmel die terugkomt, laat dan eerst kijken of opknappen nog zin heeft. Lees ook <a href=\"/kennisbank/badkamer-zonder-tegels/\">een badkamer zonder tegels</a>.",
        "faqs": [
            ("Wanneer is opknappen niet meer genoeg?", "Als er vocht achter de tegels zit, als de douche niet goed afloopt, als de leidingen oud zijn of als je de indeling wilt veranderen. Dan betaal je bij opknappen twee keer. Kijk dan naar <a href=\"/kosten/nieuwe-badkamer/\">de kosten van een nieuwe badkamer</a>."),
            ("Kan ik tegels over oude tegels laten zetten?", "Ja, als de oude tegels vlak en vast liggen. De tegelzetter maakt ze eerst ruw of zet een hechtlaag. Let op de hoogte bij de deur en de douche, en op de afvoer in de vloer."),
            ("Hoe lang gaat tegelverf mee in de badkamer?", "Op de wand buiten de douche een paar jaar, als de voorbereiding goed is: ontvetten, licht schuren en een primer. In de douche zelf slijt het snel. Zie het als tijdelijke oplossing."),
            ("Wat kost nieuwe kit en nieuwe voegen?", f"Hele badkamer opnieuw afkitten kost {rb('kitwerk_badkamer')}. Voegen vernieuwen kost zo'n €20 tot €40 per m² (eigen inschatting). Lees meer bij <a href=\"/kosten/kitwerk-voegen/\">kosten kitwerk en voegen</a>."),
            ("Kan ik alleen de douche vervangen?", "Ja. Een nieuwe douchewand en kraan is een kleine klus. Moet ook de bak eruit en de douchehoek opnieuw betegeld, dan is het meer werk. Zie <a href=\"/kosten/douche-vervangen/\">de kosten van een douche vervangen</a>."),
        ],
        "bronnen": ["werkspot_kit", "slimster_kit", "werkspot_sanitair", "werkspot_douchekraan", "werkspot_tegel", "werkspot_tegelverf", "homedeal_lood", "btw"],
        "verwant": ["kitwerk-voegen", "douche-vervangen", "wastafel-vervangen"],
        "kennis": [("/kennisbank/badkamer-schoonmaken/", "De badkamer goed schoonmaken"),
                   ("/kennisbank/badkamer-zonder-tegels/", "Een badkamer zonder tegels: kan dat?"),
                   ("/materialen/voegen-en-kit/", "Voegen en kit: welke kies je?")],
    },
    # ------------------------------------------------------------------ 4
    {
        "slug": "douche-vervangen",
        "kort": "Douche vervangen",
        "omschrijving": "Wat het kost om je douche te vervangen: alleen wand en kraan, of de hele douchehoek.",
        "h1": f"Wat kost een douche vervangen in {JAAR}?",
        "title": f"Kosten douche vervangen {JAAR}: richtprijzen",
        "description": "Een douche vervangen kost €600 tot €6.000, inclusief 21% btw: van alleen een nieuwe wand en kraan tot een vernieuwde douchehoek met tegels. Met kostenopbouw en tips.",
        "dienst": "inloopdouche-plaatsen",
        "van": 600, "tot": 6000, "eenheid": "per douche, inclusief plaatsing en btw",
        "snel": "Een douche vervangen kost <strong>€600 tot €6.000</strong>, inclusief plaatsing en 21% btw. Alleen een nieuwe douchewand en kraan op dezelfde plek kost zo'n €600 tot €1.500. Moeten de douchebak en de tegels in de douchehoek eruit, dan betaal je meestal €3.000 tot €6.000, omdat de hoek opnieuw waterdicht en betegeld moet worden.",
        "varianten": [
            ("Budget: wand en kraan", 600, 1500, "Nieuwe glazen douchewand, thermostaatkraan en douchekop. Douchebak of vloer en tegels blijven."),
            ("Midden: nieuwe douchebak", 1500, 3000, "Oude bak eruit, nieuwe vlakke douchebak of cabine, nieuwe wand en kraan. Tegels rond de bak bijwerken."),
            ("Luxe: hele douchehoek", 3000, 6000, "Douchehoek tot op de muur strippen, waterdicht maken, nieuwe tegels, inloopdouche met goot en regendouche."),
        ],
        "varianten_eenheid": "Totaalprijs per douche, inclusief materiaal, montage en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Homedeal (douchecabine €430 – €5.200, inloopdouche €430 – €4.000, incl. montage en btw), Trustoo (cabine plaatsen €275 – €435) en de richtprijzen voor tegelwerk en waterdicht maken.",
        "factoren": [
            ("Blijven de tegels?", "Het grootste verschil zit in de vraag of de douchehoek open moet. Een nieuwe wand en kraan zijn een middag werk. Moeten de tegels eruit, dan komt er sloop, waterdicht maken, tegelwerk en droogtijd bij."),
            ("Douchebak of inloopdouche", "Een nieuwe douchebak van dezelfde maat is snel geplaatst. Een inloopdouche zonder drempel vraagt afschot in de vloer en vaak een goot. Lees ook <a href=\"/kennisbank/inloopdouche-zonder-drempel/\">een inloopdouche zonder drempel</a>."),
            ("De afvoer", "Een goot of een afvoer op een andere plek betekent dat de vloer open moet. In een betonvloer is dat meer werk dan in een houten vloer. Een nieuwe afvoer op de oude plek is het goedkoopst."),
            ("De kraan", "Een opbouw-thermostaatkraan kost €50 tot €300 (Werkspot). Een inbouwkraan of regendouche kost meer, en het inbouwdeel moet in de muur. Dat kan alleen als de tegels eraf gaan."),
            ("Glas en maatwerk", "Een standaard douchewand van 90 of 100 cm is goedkoper dan glas op maat of een wand met deur. Dikker glas (8 mm) en een anti-kalklaag kosten meer, maar zijn makkelijker schoon te houden."),
        ],
        "voorbeeld": (
            "Stel: een oude douchebak van 90 × 90 cm met glazen deuren. Je wilt een douche van 90 × 120 cm met een vlakke vloer en een glazen wand. De douchehoek wordt tot op de muur gestript en opnieuw betegeld: zo'n 8 m² wand en vloer.",
            _DOUCHE,
            EIGEN,
        ),
        "btw_extra": "Ook als je alleen de douche laat vervangen, betaal je 21% over het werk en de materialen.",
        "besparen": [
            "Zitten de tegels goed? Vervang dan alleen de wand, de kraan en de douchekop. Dat is vaak de helft van het werk voor een groot deel van het effect.",
            "Kies een douchewand in standaardmaat. Glas op maat kost meer en heeft een langere levertijd.",
            "Laat de afvoer op de oude plek. Een putje in de hoek met afschot is goedkoper dan een goot op een nieuwe plek.",
            "Vervang een oude douchekop door een zuinige. Dat kost weinig en scheelt warm water. Lees meer over <a href=\"/kennisbank/water-besparen-badkamer/\">water besparen in de badkamer</a>.",
            "Gaat de douchehoek toch open? Laat dan meteen de kraanaansluitingen controleren. Later is dat duurder.",
        ],
        "specialist": "Een nieuwe douchekop of glijstang kun je zelf. Een douchewand en een opbouwkraan ook, als je ervaring hebt met boren in tegels en lekvrij aansluiten. Moet de douchehoek open, dan is het werk voor een badkamerspecialist: de waterdichte laag en de kimband in de hoeken bepalen of je douche over tien jaar nog droog is. Een lek onder een douche zie je vaak pas als er schade aan het plafond is.",
        "faqs": [
            ("Hoe lang duurt het vervangen van een douche?", "Een nieuwe wand en kraan zijn in een dag klaar. Een hele douchehoek met nieuwe tegels duurt drie tot vijf werkdagen, door de droogtijd van de waterdichte laag, de lijm en de voegen."),
            ("Kan ik een douchebak vervangen zonder nieuwe tegels?", "Soms. Als de nieuwe bak precies dezelfde maat heeft, kun je de onderste rij tegels bijwerken. Vaak beschadigt de onderste rij bij het uitbreken. Bewaar daarom reservetegels, of kies een andere tegel voor de onderkant."),
            ("Wat kost een nieuwe douchekraan?", f"Een thermostatische opbouwkraan kost €50 tot €300, plus een tot twee uur werk. Met voorrijkosten kom je op zo'n {bt(r100(T_KRAAN))}. Zie <a href=\"/kosten/kraan-vervangen/\">de kosten van een kraan vervangen</a>."),
            ("Wat kost een bad vervangen door een douche?", "Dat is meer werk dan een douche vervangen, omdat het bad eruit moet en de afvoer anders wordt. Zie <a href=\"/kosten/bad-vervangen-door-douche/\">de kosten van een bad vervangen door een douche</a>."),
            ("Douchecabine of inloopdouche?", "Een cabine is goedkoper en snel geplaatst, en houdt het water goed binnen. Een inloopdouche oogt ruimer en is makkelijker schoon te houden. Lees meer bij <a href=\"/kosten/douchecabine-plaatsen/\">de kosten van een douchecabine</a> en <a href=\"/kosten/inloopdouche/\">een inloopdouche</a>."),
        ],
        "bronnen": ["homedeal_douche", "slimster_douche", "trustoo_badkamer", "werkspot_douchekraan", "werkspot_tegel", "homedeal_lood", "btw"],
        "verwant": ["inloopdouche", "douchecabine-plaatsen", "kraan-vervangen"],
        "kennis": [("/badkamerspullen/douchewand-kiezen/", "Een douchewand kiezen"),
                   ("/badkamerspullen/douchesysteem-kiezen/", "Een douchesysteem kiezen"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Je badkamer waterdicht maken")],
    },
    # ------------------------------------------------------------------ 5
    {
        "slug": "wastafel-vervangen",
        "kort": "Wastafel vervangen",
        "omschrijving": "Wat een nieuwe wastafel of wastafelmeubel kost, inclusief kraan en montage.",
        "h1": f"Wat kost een wastafel vervangen in {JAAR}?",
        "title": f"Kosten wastafel vervangen {JAAR}: richtprijzen",
        "description": "Een wastafel vervangen kost €300 tot €2.500, inclusief kraan, montage en 21% btw. Met kostenopbouw, voorbeelden van eenvoudig tot dubbel meubel en tips.",
        "dienst": "badkamer-installeren",
        "van": 300, "tot": 2500, "eenheid": "per wastafel of meubel, inclusief montage en btw",
        "snel": "Een wastafel vervangen kost meestal <strong>€300 tot €2.500</strong>, inclusief kraan, montage en 21% btw. Werkspot noemt €150 tot €800 voor het plaatsen of vervangen van een eenvoudige wastafel. Kies je een wastafelmeubel met spiegel, dan kom je vaker op €700 tot €2.500. Een dubbel of luxe meubel kost meer.",
        "varianten": [
            ("Budget: losse wastafel", 300, 800, "Eenvoudige wastafel of fontein met kraan en sifon, op dezelfde plek als de oude."),
            ("Midden: wastafelmeubel", 700, 2500, "Hangend meubel met lades, wastafel, kraan en spiegel. Aansluitingen blijven op hun plek."),
            ("Luxe: dubbel meubel", 2500, 4500, "Dubbel meubel of maatwerk met twee kranen, spiegelkast met licht en soms een extra afvoer."),
        ],
        "varianten_eenheid": "Totaalprijs per wastafel of meubel, inclusief kraan, montage en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Werkspot (plaatsen of vervangen €150 – €800; wastafel €150 – €800; meubel plaatsen €200 – €600, dubbel €350 – €800), Slimster (wastafel gemiddeld €550) en de sanitairniveaus uit de calculator.",
        "factoren": [
            ("Losse wastafel of meubel", f"Werkspot noemt voor een vrijstaande wastafel €200 tot €550, een inbouwwastafel €150 tot €400 en een dubbele €300 tot €800. Een meubel met wastafel en spiegel kost in het middensegment {bt(niv('sanitair_meubel', 'midden'))}."),
            ("Blijven de aansluitingen op hun plek?", "Komt de nieuwe wastafel op dezelfde hoogte en plek, dan is het een klus van twee tot vier uur. Moeten de waterleiding of de afvoer verhuizen, bijvoorbeeld voor een dubbel meubel, dan moet de muur open en komt er tegelwerk bij."),
            ("De muur", "Een hangend meubel moet stevig vast. In een gipswand of een oude, zachte muur zijn extra versterkingen of speciale pluggen nodig. Dat is een kleine meerprijs, maar wel belangrijk."),
            ("De kraan", f"Een wastafelkraan kost €50 tot €300 voor een gewone mengkraan, meer voor design of inbouw. Werkspot noemt voor een kraan €150 tot €450."),
            ("Gaten en tegels", "Is het nieuwe meubel smaller of hoger dan het oude, dan zie je oude boorgaten of een rand zonder tegels. Houd daar rekening mee, of kies een meubel dat het oude formaat bedekt."),
        ],
        "voorbeeld": (
            "Stel: een oud staand meubel van 80 cm moet weg. Er komt een hangend meubel van 80 cm met lades, een mengkraan en een spiegel. Water en afvoer blijven op dezelfde plek.",
            _WASTAFEL,
            EIGEN,
        ),
        "btw_extra": "Over de wastafel, de kraan en de montage betaal je 21% btw.",
        "besparen": [
            "Kies een meubel met dezelfde breedte en hoogte als het oude. Dan passen de aansluitingen en blijven de tegels heel.",
            "Een staand meubel is iets goedkoper te plaatsen dan een hangend, omdat er geen versterking in de muur nodig is.",
            "Koop een complete set van meubel, wastafel en spiegel. Losse onderdelen bij elkaar zoeken is vaak duurder.",
            "Laat andere kleine klussen, zoals nieuwe kit of een nieuwe kraan in de douche, op dezelfde dag doen.",
            "Zuinige kranen met een perlator sparen water. Dat kost bij aanschaf vrijwel niets extra.",
        ],
        "specialist": "Een wastafel op dezelfde plek vervangen kun je zelf, als je de water kunt afsluiten en de sifon en kranen lekvrij aansluit. Een hangend meubel moet stevig vast; twijfel je over de muur, laat het dan doen. Verhuizen de aansluitingen of komt er een stopcontact bij de spiegel, dan heb je een loodgieter en een elektricien nodig. Lees ook <a href=\"/badkamerspullen/wastafelmeubel-kiezen/\">een wastafelmeubel kiezen</a>.",
        "faqs": [
            ("Hoe lang duurt het vervangen van een wastafel?", "Op dezelfde plek twee tot vier uur, volgens Werkspot inclusief testen en afwerken. Moeten de aansluitingen verplaatsen, dan een tot twee dagen, door het tegelwerk."),
            ("Wat kost alleen het plaatsen van een meubel?", f"Werkspot noemt voor een hangend meubel {rb('montage_meubel')} voor de montage, zonder het meubel zelf. Zie <a href=\"/kosten/badkamermeubel-plaatsen/\">de kosten van een badkamermeubel plaatsen</a>."),
            ("Kan een dubbele wastafel op één afvoer?", "Vaak wel, met een verdeelstuk onder het meubel. Dat is goedkoper dan een tweede afvoer in de muur. Vraag de vakman of de afvoer groot genoeg is."),
            ("Moet er een stopcontact bij de wastafel?", "Niet verplicht, maar handig voor een spiegel met licht of een tandenborstel. In de badkamer gelden regels voor afstand tot water. Laat een elektricien dat aanleggen."),
            ("Wat is beter: hangend of staand?", "Hangend oogt ruimer en is makkelijk schoon te maken onder het meubel. Staand is iets goedkoper en makkelijker te plaatsen. In een kleine badkamer kiezen de meeste mensen voor hangend."),
        ],
        "bronnen": ["werkspot_wastafel", "slimster_wastafel", "werkspot_sanitair", "slimster_meubel", "trustoo_badkamer", "homedeal_lood", "trustoo_lood", "btw"],
        "verwant": ["badkamermeubel-plaatsen", "kraan-vervangen", "badkamer-opknappen"],
        "kennis": [("/badkamerspullen/wastafelmeubel-kiezen/", "Een wastafelmeubel kiezen"),
                   ("/badkamerspullen/spiegelkast-kiezen/", "Een spiegelkast kiezen"),
                   ("/materialen/meubelmaterialen/", "Welk materiaal voor je badkamermeubel?")],
    },
    # ------------------------------------------------------------------ 6
    {
        "slug": "kraan-vervangen",
        "kort": "Kraan vervangen",
        "omschrijving": "Wat het kost om een wastafel-, douche- of badkraan te laten vervangen.",
        "h1": f"Wat kost een kraan vervangen in {JAAR}?",
        "title": f"Kosten kraan vervangen {JAAR}: badkamer",
        "description": "Een badkamerkraan laten vervangen kost meestal €150 tot €600, inclusief kraan, voorrijkosten en 21% btw. Een inbouwkraan kost meer. Met kostenopbouw en tips.",
        "dienst": "badkamer-installeren",
        "van": 150, "tot": 600, "eenheid": "per opbouwkraan, inclusief montage en btw",
        "snel": "Een opbouwkraan in de badkamer laten vervangen kost meestal <strong>€150 tot €600</strong>, inclusief de kraan, een tot twee uur werk, voorrijkosten en 21% btw. De kraan zelf kost €50 tot €450, afhankelijk van het type. Een inbouwkraan vervangen is veel meer werk: reken op €600 tot €1.500 (eigen inschatting), omdat er vaak tegels uit moeten.",
        "varianten": [
            ("Budget: wastafelkraan", 150, 400, "Eenvoudige eenhendelmengkraan op de wastafel, op dezelfde plek."),
            ("Midden: douche- of badkraan", 200, 600, "Thermostatische opbouwkraan voor douche of bad, eventueel met nieuwe glijstang of handdouche."),
            ("Luxe: inbouwkraan", 600, 1500, "Inbouwkraan of regendoucheset vervangen. Vaak moet het inbouwdeel ook nieuw, en moeten er tegels uit en terug."),
        ],
        "varianten_eenheid": "Totaalprijs per kraan, inclusief kraan, montage, voorrijkosten en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Werkspot (eenhendelkraan €50 – €150, thermostaatkraan €50 – €300, designkraan €200 – €450, uurtarief €45 – €75) en Homedeal (uurtarief €45 – €85 excl. btw). Het bedrag voor een inbouwkraan is een eigen inschatting.",
        "factoren": [
            ("Het type kraan", "Werkspot noemt een eenhendelmengkraan €50 tot €150, een thermostaatkraan €50 tot €300 en een designkraan €200 tot €450. Zwarte, gouden of geborstelde kranen zitten vaak aan de bovenkant. Lees meer over <a href=\"/materialen/kraanafwerkingen/\">kraanafwerkingen</a>."),
            ("Opbouw of inbouw", "Een opbouwkraan draai je los en vervang je binnen een uur. Bij een inbouwkraan zit het werk in de muur. Past een nieuw bedieningsdeel op het oude inbouwdeel, dan valt het mee. Anders moeten er tegels uit."),
            ("Het uurtarief en de voorrijkosten", f"Een loodgieter rekent {rb('uurtarief')} per uur exclusief btw, plus {rb('voorrijkosten')} voorrijkosten. Bij een kleine klus zijn de voorrijkosten een groot deel van de rekening."),
            ("Oude aansluitingen", "Zitten de S-koppelingen of stopkranen vast door kalk, of is de hart-op-hart-maat anders, dan kost het meer tijd en onderdelen. Bij een wastafelkraan worden de flexibele slangen vaak meteen vervangen."),
            ("Spoed", "Een lekkende kraan in het weekend of 's avonds laten maken is duurder: loodgieters rekenen dan een hoger uurtarief. Sluit de stopkraan en plan het op een werkdag als dat kan."),
        ],
        "voorbeeld": (
            "Stel: de thermostatische douchekraan lekt en de temperatuur schommelt. Er komt een nieuwe opbouwkraan van dezelfde maat (hart-op-hart 15 cm) op dezelfde plek.",
            _KRAAN,
            EIGEN + " Het uurtarief is hier omgerekend naar een bedrag inclusief btw.",
        ),
        "btw_extra": "Let op: loodgieters noemen hun uurtarief bijna altijd zonder btw. Op de rekening komt er 21% bij.",
        "besparen": [
            "Lekt de kraan alleen? Vaak is een nieuw binnenwerk of een nieuw thermostaatelement genoeg. Dat kost minder dan een nieuwe kraan.",
            "Koop een kraan met dezelfde maat en aansluiting als de oude. Dan blijft het werk beperkt tot een uur.",
            "Laat meerdere kranen tegelijk vervangen. Je betaalt één keer voorrijkosten.",
            "Kies een kraan van een bekend merk waarvan onderdelen lang leverbaar zijn. Goedkope kranen kun je vaak niet repareren.",
            "Een thermostaatkraan met eco-knop en een zuinige douchekop sparen warm water. Dat verdien je in een paar jaar terug.",
        ],
        "specialist": "Een opbouwkraan op de wastafel of in de douche kun je zelf vervangen, als je de water kunt afsluiten en de koppelingen lekvrij monteert. Twijfel je, of zitten de stopkranen vast, laat het dan doen. Een inbouwkraan vervang je niet zelf: als het inbouwdeel niet waterdicht aansluit, lekt het in de muur. Lees ook <a href=\"/badkamerspullen/kranen-kiezen/\">kranen kiezen</a>.",
        "faqs": [
            ("Hoe lang duurt een kraan vervangen?", "Een opbouwkraan meestal een half uur tot een uur, inclusief testen. Bij vastzittende koppelingen of nieuwe stopkranen een tot twee uur."),
            ("Kan ik een inbouwkraan vervangen door een opbouwkraan?", "Ja, maar dan moet het inbouwdeel worden afgedopt en de muur worden dichtgemaakt, en de leidingen moeten op de juiste plek uitkomen. Er gaan dus tegels uit. Vaak is een nieuw bedieningsdeel op het oude inbouwdeel goedkoper."),
            ("Wat kost een loodgieter voor een kraan?", f"Reken op een tot twee uur à {rb('uurtarief')} per uur exclusief btw, plus voorrijkosten. Inclusief btw is dat voor het werk zo'n {bt(uren(1, 2))}, zonder de kraan. Zie ook <a href=\"/kosten/uurtarief-loodgieter/\">het uurtarief van een loodgieter</a>."),
            ("Waarom wordt mijn douche niet meer warm?", "Vaak is het thermostaatelement verkalkt of versleten. Dat kun je soms los vervangen. Wordt ook de wastafel niet warm, dan ligt het eerder aan de ketel of de warmtepomp."),
            ("Wat is een hart-op-hart-maat?", "De afstand tussen de twee aansluitingen in de muur. Bij douche- en badkranen is dat meestal 15 cm. Met S-koppelingen kun je een paar millimeter verschil opvangen."),
        ],
        "bronnen": ["werkspot_douchekraan", "werkspot_sanitair", "homedeal_lood", "trustoo_lood", "knab_lood", "btw"],
        "verwant": ["uurtarief-loodgieter", "douche-vervangen", "wastafel-vervangen"],
        "kennis": [("/badkamerspullen/kranen-kiezen/", "Welke kraan past bij jou?"),
                   ("/kennisbank/inbouwkranen/", "Inbouwkranen: voor- en nadelen"),
                   ("/materialen/kraanafwerkingen/", "Kraanafwerkingen: chroom, zwart, goud of rvs")],
    },
    # ------------------------------------------------------------------ 7
    {
        "slug": "badkamer-ventilatie",
        "kort": "Badkamerventilatie",
        "omschrijving": "Wat een badkamerventilator of aansluiting op mechanische ventilatie kost.",
        "h1": f"Wat kost ventilatie in de badkamer in {JAAR}?",
        "title": f"Kosten badkamerventilatie {JAAR}: richtprijzen",
        "description": "Een badkamerventilator met montage kost meestal €150 tot €500, inclusief 21% btw. Met kostenopbouw, drie voorbeelden, onderhoud en de €400 subsidie van 2026.",
        "dienst": "badkamer-installeren",
        "van": 150, "tot": 500, "eenheid": "per ventilator, inclusief montage en btw",
        "snel": "Een badkamerventilator met montage kost meestal <strong>€150 tot €500</strong>, inclusief 21% btw. Homedeal noemt €150 tot €250 voor een basisventilator, €200 tot €300 met timer en €250 tot €500 met vochtsensor. Moet er een nieuw kanaal door de gevel of het dak, dan komt daar zo'n €150 tot €400 bij (eigen inschatting). Een nieuwe mechanische ventilatie-unit voor het hele huis kost €1.700 tot €7.000.",
        "varianten": [
            ("Budget: basisventilator", 150, 300, "Losse ventilator op een bestaand kanaal, die meedraait met het licht of een nalooptimer heeft."),
            ("Midden: met vochtsensor", 250, 500, "Ventilator die zelf aanslaat bij hoge luchtvochtigheid. Of aansluiten op een bestaand centraal systeem (€250 – €450)."),
            ("Luxe: nieuw kanaal of nieuwe unit", 500, 2000, "Ventilator met nieuw kanaal naar buiten, of een nieuwe zuinige ventilatiebox voor het huis met een vochtsensor in de badkamer. Een complete nieuwe unit kan tot €7.000 kosten."),
        ],
        "varianten_eenheid": "Totaalprijs inclusief montage en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Homedeal (basis €150 – €250, timer €200 – €300, vochtsensor €250 – €500, aansluiten op centraal systeem €250 – €450, nieuwe unit €1.700 – €7.000). Homedeal noemt niet of dit inclusief btw is; wij gaan daarvan uit. Het luxe scenario is een eigen inschatting.",
        "factoren": [
            ("Is er al een kanaal?", "Zit er al een afvoer naar buiten of een ventiel van de mechanische ventilatie, dan is het een klus van een tot twee uur. Moet er een gat door de gevel of het dak, dan kost het meer: boren, kanaal leggen en afwerken."),
            ("Losse ventilator of centraal systeem", "Veel huizen hebben mechanische afvoer met ronde ventielen in keuken, badkamer en toilet. Dan plaats je geen losse ventilator, maar zet je het systeem op de hoogste stand tijdens het douchen. Een losse ventilator op een centraal kanaal werkt niet goed samen."),
            ("Bediening", "Een basisventilator draait mee met het licht. Een timer laat hem nadraaien. Een vochtsensor schakelt zelf aan en uit, ook als je vergeet. In een badkamer zonder raam is een vochtsensor of timer de beste keuze."),
            ("Zuinigheid en geluid", "Een ventilatiebox met gelijkstroommotor (DC) gebruikt volgens Milieu Centraal veel minder stroom dan een oude met wisselstroom (AC). Boxen van vóór 2010 zijn meestal nog AC. Let ook op het geluid: een stille ventilator laat je eerder aan staan."),
            ("Subsidie", "Voor een nieuw, energiezuinig ventilatiesysteem kun je vanaf 2026 €400 ISDE-subsidie krijgen. Volgens Milieu Centraal alleen samen met minstens één isolatiemaatregel en als een installateur het plaatst. Voor een losse badkamerventilator geldt dit niet."),
        ],
        "voorbeeld": (
            "Stel: een badkamer zonder raam en zonder ventilatiekanaal, aan een buitenmuur. Er komt een ventilator met vochtsensor en een nieuw kanaal door de gevel.",
            _VENT,
            EIGEN + " Met een bestaand kanaal vallen het boren en het kanaal weg en kom je op zo'n €150 tot €500.",
        ),
        "btw_extra": "Ook ventilatie in de badkamer valt onder 21% btw. Het 9%-tarief voor isolatie geldt niet voor een ventilator.",
        "besparen": [
            "Heb je al mechanische ventilatie? Gebruik dan de hoogste stand tijdens en na het douchen, en laat de ventielen schoonmaken. Dat is vaak genoeg.",
            "Kies een ventilator met vochtsensor of timer, zodat hij niet de hele dag draait en niet te vroeg stopt.",
            "Plaats de ventilator tegenover de deur, zo hoog mogelijk en uit de buurt van de douche. Laat onder de deur een spleet van 1 à 2 cm voor aanvoer van lucht.",
            "Maak roosters en ventielen een keer per jaar schoon. Milieu Centraal adviseert de box eens in de twee jaar te laten onderhouden en de kanalen eens in de acht jaar te laten reinigen.",
            "Combineer een nieuwe ventilatiebox met isolatie als je die toch plant. Dan kom je mogelijk in aanmerking voor €400 subsidie.",
        ],
        "specialist": "Een ventilator op een bestaand kanaal en een bestaande aansluiting kun je zelf vervangen, als je weet hoe je veilig met elektra werkt. Een nieuw kanaal door de gevel, een nieuwe groep of een nieuwe ventilatiebox laat je aan een installateur over. In een appartement mag je vaak niet zomaar een gat in de gevel maken; vraag dat eerst na bij de VvE. Lees meer in <a href=\"/kennisbank/badkamer-ventilatie/\">ventilatie in de badkamer</a>.",
        "faqs": [
            ("Is een raam genoeg om de badkamer te ventileren?", "Niet altijd. Milieu Centraal raadt aan om het raam niet als vaste oplossing open te zetten: in de winter koelt de badkamer af en ontstaat juist condens. Wil je luchten, doe dat dan kort, maximaal tien minuten direct na het douchen."),
            ("Hoe lang moet een ventilator nadraaien?", "Milieu Centraal adviseert de ventilatie tijdens het douchen op de hoogste stand te zetten en daarna te laten nadraaien. In de praktijk is 15 tot 30 minuten gebruikelijk, of tot de vochtsensor afslaat."),
            ("Mag een losse ventilator op mijn mechanische ventilatie?", "Nee, dat werkt niet goed. Een losse ventilator blaast lucht in het kanaal van het centrale systeem, en die kan dan via een ander ventiel terugkomen. Vraag een installateur om de afzuiging in de badkamer beter in te regelen."),
            ("Wat kost een nieuwe mechanische ventilatiebox?", "Homedeal noemt €1.700 tot €7.000 voor een nieuwe mechanische ventilatie-unit voor het hele huis. Een vervangende box op een bestaand systeem zit aan de onderkant, een nieuw systeem met kanalen aan de bovenkant."),
            ("Waarom komt de schimmel terug?", "Meestal omdat het vocht niet snel genoeg weg kan: te weinig afzuiging, geen spleet onder de deur of een ventilator die te vroeg stopt. Kit met schimmel kun je vervangen, maar zonder betere ventilatie komt het terug."),
        ],
        "bronnen": ["homedeal_ventilatie", "mc_ventilatie", "werkspot_stopcontact", "homedeal_lood", "btw"],
        "verwant": ["badkamer-opknappen", "nieuwe-badkamer", "uurtarief-loodgieter"],
        "kennis": [("/kennisbank/badkamer-ventilatie/", "Ventilatie in de badkamer: zo doe je het goed"),
                   ("/kennisbank/badkamer-schoonmaken/", "Schimmel voorkomen en de badkamer schoonmaken"),
                   ("/kennisbank/badkamerverlichting/", "Verlichting en elektra in de badkamer")],
    },
    # ------------------------------------------------------------------ 8
    {
        "slug": "tweede-badkamer",
        "kort": "Tweede badkamer",
        "omschrijving": "Wat een extra badkamer kost op een plek waar nog geen water en afvoer is.",
        "h1": f"Wat kost een tweede badkamer in {JAAR}?",
        "title": f"Kosten tweede badkamer {JAAR}: richtprijzen",
        "description": "Een tweede badkamer kost meestal €8.000 tot €25.000, inclusief 21% btw. Zie wat nieuwe wanden, afvoer en ventilatie kosten, en wanneer zolder duurder uitvalt.",
        "dienst": "badkamer-renoveren",
        "van": 8000, "tot": 25000, "eenheid": "per extra badkamer van 3 tot 6 m², inclusief btw",
        "snel": "Een tweede badkamer kost meestal <strong>€8.000 tot €25.000</strong>, inclusief 21% btw. Dat is meer dan het vervangen van een bestaande badkamer, omdat er nog geen water, afvoer, ventilatie en vaak ook geen wanden zijn. De afstand tot de standleiding bepaalt veel. Op zolder, met isolatie en een dakraam of dakkapel, kom je volgens Homedeal op €20.000 tot €35.000.",
        "varianten": [
            ("Budget: douche en wastafel", 8000, 13000, "Kleine douche met wastafel in een bestaande kamer, vlak bij de standleiding. Geen toilet, eenvoudig sanitair."),
            ("Midden: volwaardige badkamer", 13000, 22000, "Badkamer van 4 tot 6 m² met douche, hangtoilet, meubel en vloerverwarming. Nieuwe wanden, afvoer en ventilatie."),
            ("Luxe: op zolder of en-suite", 20000, 35000, "Badkamer op zolder met isolatie, dakraam of dakkapel, of een luxe en-suite bij de slaapkamer met grote tegels."),
        ],
        "varianten_eenheid": "Totaalprijs per extra badkamer, inclusief materiaal, arbeid en btw",
        "varianten_noot": "Voorbeeldscenario's op basis van Homedeal (badkamer aanleggen €550 – €1.100 per m², €3.500 – €15.000; badkamer op zolder €20.000 – €35.000) en de richtprijzen voor leidingwerk en verplaatsen. De grenzen zijn een eigen inschatting.",
        "factoren": [
            ("Afstand tot de standleiding", f"Een toilet heeft een afvoer met voldoende afschot nodig. Hoe verder de nieuwe badkamer van de bestaande standleiding ligt, hoe meer werk. Reken bovenop het gewone leidingwerk ({rb('leidingwerk')}) op {rb('leidingwerk_verplaatsen')} voor een nieuwe afvoer. Is het te ver, dan kan een vuilwaterpomp, maar die is een noodoplossing."),
            ("Nieuwe wanden en een deur", "Maak je de badkamer in een deel van een slaapkamer, dan komen er wanden bij. Homedeal noemt voor een gipswand €40 tot €50 per m². Gebruik in de badkamer vochtbestendige platen. Een deur met kozijn komt er ook bij."),
            ("Warm water", "Een tweede douche vraagt meer van je ketel of warmtepomp. Kan die geen twee douches tegelijk aan, dan kan een grotere boiler of een tweede toestel nodig zijn. Vraag dat na voordat je begint."),
            ("Ventilatie", "Een nieuwe badkamer moet een afvoer van lucht naar buiten hebben. Is er geen kanaal, dan komt er een ventilator met kanaal door de gevel of het dak bij. Zie <a href=\"/kosten/badkamer-ventilatie/\">de kosten van badkamerventilatie</a>."),
            ("De vloer", "Een houten verdiepingsvloer moet waterdicht en stijf genoeg zijn voor tegels. Soms is een nieuwe ondervloer of een verhoogde vloer nodig voor het afschot naar de afvoer."),
        ],
        "voorbeeld": (
            "Stel: in een hoek van een slaapkamer op de eerste verdieping komt een badkamer van 2 bij 2 meter (4 m²), met douche, hangtoilet en wastafelmeubel. De standleiding zit aan de andere kant van de muur. Er komen twee nieuwe wanden en een deur. Wanden tot het plafond betegeld: zo'n 22 m² tegelwerk.",
            _TWEEDE,
            EIGEN + " Ligt de standleiding verder weg of komt de badkamer op zolder, dan kom je hoger uit.",
        ),
        "btw_extra": "Laat je de nieuwe gipswanden stukadoren of verven, dan kan dat arbeidsloon onder 9% vallen als de woning ouder is dan twee jaar. Het bedrijf moet dat apart op de offerte zetten. Het badkamerwerk zelf is 21%.",
        "besparen": [
            "Kies een plek recht boven of naast de bestaande badkamer of de standleiding. Dat scheelt het meeste geld.",
            "Begin klein: een douche en wastafel zonder toilet is een stuk goedkoper, omdat de dikke toiletafvoer de lastigste leiding is.",
            "Laat de tweede badkamer meteen meenemen als je toch de eerste badkamer of de zolder verbouwt. Eén keer sloop, één keer leidingwerk.",
            "Kies standaard sanitair en standaard tegels. Een tweede badkamer wordt vaak minder gebruikt; luxe heeft daar minder zin.",
            "Laat eerst controleren of je ketel of warmtepomp genoeg warm water kan leveren. Een nieuw toestel achteraf is een dure verrassing.",
        ],
        "specialist": "Een tweede badkamer is werk voor een badkamerspecialist of aannemer, met een loodgieter voor de nieuwe afvoer en een elektricien voor een nieuwe groep. Bij een badkamer op zolder of een draagmuur die weg moet, heb je soms een constructeur nodig. In een appartement heb je toestemming van de VvE nodig voor nieuwe aansluitingen op de standleiding. Lees meer bij <a href=\"/badkamer-voor/tweede-badkamer/\">een tweede badkamer</a>.",
        "faqs": [
            ("Levert een tweede badkamer meer op bij verkoop?", "Een tweede badkamer maakt een huis voor gezinnen aantrekkelijker. Hoeveel het oplevert, verschilt per huis en regio. Vraag een makelaar in je buurt als dat de reden is om te verbouwen."),
            ("Heb ik een vergunning nodig voor een tweede badkamer?", "Binnen in het huis meestal niet. Wel als je een dakkapel plaatst aan de voorkant, of iets aan de constructie verandert. Bij een appartement heb je vaak toestemming van de VvE nodig. Check het bij je gemeente via het Omgevingsloket."),
            ("Kan ik een badkamer maken zonder standleiding in de buurt?", "Ja, met een vuilwaterpomp die het afvalwater door een dunne leiding wegpompt. Dat is een oplossing als er echt geen andere weg is. Een pomp maakt geluid en heeft onderhoud nodig."),
            ("Wat kost een badkamer op zolder?", "Homedeal noemt €20.000 tot €35.000, inclusief constructie, leidingen, ventilatie en sanitair. Zie <a href=\"/kosten/badkamer-op-zolder/\">de kosten van een badkamer op zolder</a>."),
            ("Hoe lang duurt het maken van een tweede badkamer?", "Reken op drie tot vijf weken, langer bij een zolder met dakkapel. Er komen meer vakmensen na elkaar dan bij een gewone badkamerrenovatie."),
        ],
        "bronnen": ["homedeal_aanleggen", "homedeal_zolder", "werkspot_zolder", "trustoo_badkamer", "slimster_badkamer", "homedeal_ventilatie", "btw"],
        "verwant": ["badkamer-op-zolder", "toilet-verplaatsen", "kleine-badkamer"],
        "kennis": [("/badkamer-voor/tweede-badkamer/", "Een tweede badkamer: waar begin je?"),
                   ("/kennisbank/badkamer-en-suite/", "Een badkamer en-suite bij de slaapkamer"),
                   ("/kennisbank/verbouwen-in-vve/", "Verbouwen in een VvE: waar let je op?")],
    },
]


if __name__ == "__main__":
    for naam, rijen in (("kleine", _KLEIN), ("luxe", _LUXE), ("opknap", _OPKNAP), ("douche", _DOUCHE),
                        ("wastafel", _WASTAFEL), ("kraan", _KRAAN), ("vent", _VENT), ("tweede", _TWEEDE)):
        print(f"{naam:10} {totaal(rijen)}")
