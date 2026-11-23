"""Productdata voor de offertevergelijker (Top Badkamers).

Levert PRODUCTDATA en als_json() voor de pagina /tools/offertechecker/. De parser
(offerte_parser_badkamer.js) gebruikt deze data om producten op een offerte te herkennen
(merk, serie, artikelnummer, EAN) en de prijs naast een marktprijsband te leggen.

Opbouw:
- merken: gangbare sanitairmerken in Nederland met aliassen. Een code_regex staat er alleen
  bij als het nummerformaat van de fabrikant zeker is (gecontroleerd in november 2026).
- categorieen: vaste sleutels met trefwoorden en een prijsband van/tot, inclusief 21% btw,
  voor het product zelf, zonder montage. Waar het kan komen de banden uit de spullengidsen
  (badkamer_spullen.py, prijsklassen en bronnen B). Ontbrekende categorieen zijn met
  WebSearch aangevuld; die banden zijn bewust ruim.
- artikelen: samengevoegd uit producten_data_kranen.py en producten_data_sanitair.py
  (andere agents). Die worden veilig geladen: ontbreken ze, dan blijft de lijst leeg en valt
  de parser terug op de categorieband.
- bronnen: {sleutel: [omschrijving, url]}. Geen winkelnamen en geen links naar winkels.

Peildatum: november 2026. Prijzen zijn richtprijzen, geen offerte.
"""
import json
import re
import sys

PEILDATUM = "2026-11"

# ---------------------------------------------------------------------------
# Bronnen
# ---------------------------------------------------------------------------
# Bronnen uit de spullengidsen (badkamer_spullen.B). Veilig geladen; bij een fout gebruiken we
# de kopie hieronder (zelfde teksten en URL's).
try:
    from badkamer_spullen import B as _SPULLEN_B
except Exception:  # pragma: no cover - alleen als badkamer_spullen niet te importeren is
    _SPULLEN_B = {}

_BRONNEN_SPULLEN_KOPIE = {
    "slimster_inloop": ("Slimster: kosten inloopdouche (gemiddeld €825 zonder montage, spreiding €250 tot €1.400)",
                        "https://slimster.nl/badkamer/douche-plaatsen-kosten/inloopdouche/"),
    "bobex_wand": ("Bobex: welk materiaal voor een douchewand (eenvoudig €100 tot €200, luxe tot ruim €2.000)",
                   "https://www.bobex.be/nl-be/badkamerrenovatie/douchewand/"),
    "bobex_toilet": ("Bobex: wat kost een nieuw toilet (staand €200 tot €500, hangtoilet met inbouwreservoir €200 tot €600)",
                     "https://www.bobex.be/nl-be/badkamerrenovatie/toilet/"),
    "homedeal_toilet": ("Homedeal: toilet renoveren (inbouwreservoir €150 tot €300)",
                        "https://www.homedeal.nl/verbouwing/toilet-renovatie"),
    "slimster_meubel": ("Slimster: prijs badkamermeubel (vanaf €150 basis, €750 comfort, €1.500 luxe, zonder montage)",
                        "https://slimster.nl/badkamer/prijzen/badkamermeubel"),
    "werkspot_wastafel": ("Werkspot: kosten wastafel plaatsen",
                          "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/wastafel"),
    "werkspot_kraan": ("Werkspot: douchekraan vervangen (thermostaatkraan €50 tot €300)",
                       "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/douchekraan-vervangen"),
    "slimster_tegels": ("Slimster: kosten keramische vloertegels (porcellanato €15 tot €65 per m², faience €9 tot €40 per m²)",
                        "https://slimster.nl/tegelzetter/vloertegels-prijzen/kosten-keramische-vloertegels/"),
    "homedeal_tegels": ("Homedeal: badkamer betegelen (tegels €15 tot €160 per m²)",
                        "https://www.homedeal.nl/tegels-zetten/badkamer-betegelen-kosten/"),
    "werkspot_tegels": ("Werkspot: badkamer betegelen (tegels meestal €20 tot €60 per m²)",
                        "https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten"),
    "slimster_vrijstaand": ("Slimster: vrijstaand bad (vanaf €300 basis, €900 comfort, €2.000 luxe, zonder plaatsing)",
                            "https://slimster.nl/badkamer/prijzen/bad/vrijstaand"),
    "slimster_bad": ("Slimster: wat kost een bad plaatsen", "https://slimster.nl/badkamer/prijzen/bad"),
    "homedeal_bad": ("Homedeal: bad plaatsen (gietijzeren bad gemiddeld €1.850)",
                     "https://www.homedeal.nl/badkamerspecialist/bad-plaatsen-kosten/"),
    "aanbod": ("Eigen vergelijking van het aanbod bij meerdere bouwmarkten en sanitairwinkels, november 2026 (geen links, wij verwijzen niet naar winkels)", None),
}

# Nieuwe bronnen voor categorieen die niet in de spullengidsen staan (WebSearch, november 2026).
_BRONNEN_EIGEN = {
    # Douchebak €75 / €200 / €500 en douchecabine €300 / €800 / €1.500 (basis, comfort, luxe), vanafprijzen incl. btw, zonder montage.
    "slimster_douche": ("Slimster: kosten douche (douchebak vanaf €75, €200, €500; douchecabine vanaf €300, €800, €1.500; zonder montage)",
                        "https://slimster.nl/badkamer/douche-plaatsen-kosten/"),
    # RVS-douchegoot 'vaak vanaf €300'; eenvoudige goten liggen lager (aanbod).
    "werkspot_goot": ("Werkspot: douchegoot plaatsen (RVS-goten vaak vanaf €300)",
                      "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/douchegoot-plaatsen"),
    # Designradiator gemiddeld €425, spreiding €50 tot €800, zonder montage.
    "slimster_radiator": ("Slimster: designradiator badkamer (gemiddeld €425, spreiding €50 tot €800, zonder montage)",
                          "https://slimster.nl/badkamer/badkamer-verwarming-kosten/designradiator/"),
    # Radiator zelf ongeveer €150 tot €1.200.
    "werkspot_radiator": ("Werkspot: designradiator badkamer (radiator zelf ongeveer €150 tot €1.200)",
                          "https://www.werkspot.nl/verwarming/prijzen-kosten/designradiator-badkamer"),
    # Sanitair voor toilet en fontein samen €250 tot €900.
    "slimster_toilet": ("Slimster: wat kost een toiletrenovatie (sanitair voor toilet en fontein €250 tot €900)",
                        "https://slimster.nl/toilet/toilet-renovatie-kosten/"),
    # Brochure met de series bedieningsplaten (Sigma01 tot Sigma70) en het nummerformaat 115.xxx.xx.x.
    "geberit_platen": ("Geberit: brochure bedieningsplaten (series en artikelnummers)",
                       "https://www.geberit.nl/_assets/local-media/downloadcenter/brochure/b2c/brochure-bedieningsplaten.pdf"),
}


def _bron(k):
    v = _SPULLEN_B.get(k) or _BRONNEN_SPULLEN_KOPIE.get(k) or _BRONNEN_EIGEN.get(k)
    return [v[0], v[1]] if v else None


# ---------------------------------------------------------------------------
# Merken
# ---------------------------------------------------------------------------
# code_regex alleen waar het formaat zeker is:
# - Grohe: 5 cijfers model + 3 tekens afwerking (000 = chroom; DC0 supersteel, GL0 cool sunrise,
#   GN0 geborsteld cool sunrise, DA0 warm sunset, DL0 geborsteld warm sunset, AL0 geborsteld hard
#   graphite, A00 hard graphite, BE0 nikkel, EN0 geborsteld nikkel; soms 001/002). Bron: Grohe-
#   brochures en prijslijst 2025 (cdn.cloud.grohe.com). Spaties ("34 558 000") normaliseert de parser.
# - Hansgrohe: 8 cijfers, laatste 3 = afwerking (000 chroom, 670 mat zwart, 700 mat wit,
#   990 polished gold, 140 brushed bronze, 250 brushed gold, 340 brushed black chrome, 800 rvs-look).
#   Overlapt met Grohe op ...000: bij alleen een code zonder merknaam kiest de parser geen merk.
# - Geberit: 115.882.KJ.1 (3 cijfers . 3 cijfers . 2 tekens . 1 cijfer). Bron: Geberit-catalogus.
# - Ideal Standard: letter + 4 cijfers + 2 letters (bijv. B1312AA).
# - TECE: 9.240.xxx voor bedieningsplaten (TECEloop/TECEsquare).
MERKEN = [
    {"naam": "Grohe", "aliassen": ["grohe"],
     "code_regex": [r"\b\d{5}(?:000|001|002|DC0|GL0|GN0|DA0|DL0|AL0|A00|BE0|EN0|KS0|LS0)\b"]},
    {"naam": "Hansgrohe", "aliassen": ["hansgrohe", "hans grohe"],
     "code_regex": [r"\b\d{5}(?:000|670|700|990|140|250|340|800)\b"]},
    {"naam": "Axor", "aliassen": ["axor"]},
    {"naam": "Geberit", "aliassen": ["geberit"], "code_regex": [r"\b\d{3}\.\d{3}\.\w{2}\.\d\b"]},
    {"naam": "Villeroy & Boch", "aliassen": ["villeroy & boch", "villeroy en boch", "villeroy&boch", "villeroy", "v&b"]},
    {"naam": "Duravit", "aliassen": ["duravit"]},
    {"naam": "Ideal Standard", "aliassen": ["ideal standard", "ideal-standard"],
     "code_regex": [r"\b[A-Z]\d{4}[A-Z]{2}\b"]},
    {"naam": "Sphinx", "aliassen": ["sphinx"]},
    {"naam": "Laufen", "aliassen": ["laufen"]},
    {"naam": "Toto", "aliassen": ["toto"]},
    {"naam": "Roca", "aliassen": ["roca"]},
    {"naam": "Jacob Delafon", "aliassen": ["jacob delafon", "delafon"]},
    {"naam": "Keuco", "aliassen": ["keuco"]},
    {"naam": "Dornbracht", "aliassen": ["dornbracht"]},
    {"naam": "Hansa", "aliassen": ["hansa"]},
    {"naam": "Tres", "aliassen": ["tres griferia", "tres"]},
    {"naam": "Gessi", "aliassen": ["gessi"]},
    {"naam": "Damixa", "aliassen": ["damixa"]},
    {"naam": "Hotbath", "aliassen": ["hotbath", "hot bath"]},
    {"naam": "Clou", "aliassen": ["clou"]},
    {"naam": "Wiesbaden", "aliassen": ["wiesbaden"]},
    {"naam": "Plieger", "aliassen": ["plieger"]},
    {"naam": "Sealskin", "aliassen": ["sealskin"]},
    {"naam": "Novellini", "aliassen": ["novellini"]},
    {"naam": "Hüppe", "aliassen": ["hüppe", "huppe", "hueppe"]},
    {"naam": "Kermi", "aliassen": ["kermi"]},
    {"naam": "Radaway", "aliassen": ["radaway"]},
    {"naam": "Riho", "aliassen": ["riho"]},
    {"naam": "Kaldewei", "aliassen": ["kaldewei"]},
    {"naam": "Bette", "aliassen": ["bette"]},
    {"naam": "Xenz", "aliassen": ["xenz"]},
    {"naam": "Vasco", "aliassen": ["vasco"]},
    {"naam": "Zehnder", "aliassen": ["zehnder"]},
    {"naam": "Easy Drain", "aliassen": ["easy drain", "easydrain", "ess easy drain"]},
    {"naam": "Viega", "aliassen": ["viega"]},
    {"naam": "TECE", "aliassen": ["tece", "teceloop", "tecesquare"], "code_regex": [r"\b9\.240\.\d{3}\b"]},
    {"naam": "Wisa", "aliassen": ["wisa"]},
    {"naam": "Pressalit", "aliassen": ["pressalit"]},
    {"naam": "Mosa", "aliassen": ["mosa"]},
    {"naam": "Lineabeta", "aliassen": ["lineabeta", "linea beta"]},
]

# ---------------------------------------------------------------------------
# Categorieen: trefwoorden en prijsband (incl. 21% btw, product zonder montage)
# ---------------------------------------------------------------------------
# eenheid: "st" (per stuk) of "m2" (tegels). De parser rekent naar die eenheid.
# Herkomst per band staat erachter als commentaar.
CATEGORIEEN = {
    # Spullengids kranen-kiezen, prijs_extra 'Opbouwthermostaat' €50–300 (Werkspot). Bovenkant
    # verruimd naar €400 omdat merkthermostaten met douchegarnituur er vaak net boven zitten.
    "thermostaatkraan": {"naam": "Thermostaatkraan douche (opbouw)",
                         "trefwoorden": ["thermostaatkraan", "douchethermostaat", "thermostatische douchekraan",
                                         "thermostatische kraan", "thermostaat", "thermostatisch", "douchekraan",
                                         "douchemengkraan", "grohtherm", "ecostat"],
                         "van": 50, "tot": 400, "bron": ["werkspot_kraan", "aanbod"]},
    # Spullengids douchesysteem-kiezen: instap €100 tot hoog €1.500 (aanbod bij meerdere winkels).
    "douchesysteem": {"naam": "Douchesysteem of regendoucheset",
                      "trefwoorden": ["douchesysteem", "regendoucheset", "regendouche", "doucheset met thermostaat",
                                      "showerpipe", "douchezuil", "hoofddouche", "douchekop", "plafonddouche",
                                      "euphoria system", "rainshower system"],
                      "van": 100, "tot": 1500, "bron": ["aanbod"]},
    # Glijstangset of handdouche: aanbod, ruime band.
    "handdouche_set": {"naam": "Glijstangset of handdouche",
                       "trefwoorden": ["glijstangset", "glijstang", "handdouche", "doucheslang", "douchestang",
                                       "wandhouder", "handdoucheset"],
                       "van": 25, "tot": 250, "bron": ["aanbod"]},
    # Spullengids kranen-kiezen: instap €40 tot hoog €600.
    "wastafelkraan": {"naam": "Wastafelkraan",
                      "trefwoorden": ["wastafelkraan", "wastafelmengkraan", "fonteinkraan", "toiletkraan",
                                      "mengkraan wastafel", "eengreepsmengkraan", "fonteinkraantje", "kraan"],
                      "van": 40, "tot": 600, "bron": ["aanbod"]},
    # Badkraan / badthermostaat: aanbod, band als wastafelkraan met hogere bovenkant.
    "badkraan": {"naam": "Badkraan of badthermostaat",
                 "trefwoorden": ["badkraan", "badmengkraan", "badthermostaat", "badvulcombinatie", "badvuller",
                                 "bad/douche thermostaat", "badrandkraan"],
                 "van": 60, "tot": 600, "bron": ["werkspot_kraan", "aanbod"]},
    # Spullengids kranen-kiezen, prijs_extra 'Inbouwthermostaat' €250–700. Onderkant verlaagd naar
    # €100 omdat een inbouwdeel ook los op de offerte staat.
    "inbouwkraan": {"naam": "Inbouwkraan of inbouwthermostaat (incl. inbouwdeel)",
                    "trefwoorden": ["inbouwthermostaat", "inbouwkraan", "inbouwdeel", "inbouwbox", "inbouw thermostaat",
                                    "inbouwmengkraan", "smartbox", "ibox", "rapido", "afbouwdeel", "afdekset",
                                    "smartcontrol"],
                    "van": 100, "tot": 900, "bron": ["aanbod"]},
    # Werkspot: RVS-douchegoot vaak vanaf €300; eenvoudige goten vanaf ongeveer €50 (aanbod).
    "douchegoot": {"naam": "Douchegoot of doucheput",
                   "trefwoorden": ["douchegoot", "douchedrain", "doucheput", "drain", "goot", "tegelrooster", "showerdrain"],
                   "van": 50, "tot": 700, "bron": ["werkspot_goot", "aanbod"]},
    # Spullengids inloopdouche-kopen: €150 tot €2.000 (Slimster, Bobex).
    "douchewand": {"naam": "Douchewand of inloopwand",
                   "trefwoorden": ["douchewand", "inloopwand", "inloopdouche", "walk-in", "walk in", "glaswand",
                                   "zijwand", "douchedeur", "draaideur", "schuifdeur", "nisdeur", "glasplaat douche"],
                   "van": 150, "tot": 2000, "bron": ["slimster_inloop", "bobex_wand"]},
    # Slimster: douchecabine vanaf €300 / €800 / €1.500. Bovenkant verruimd naar €2.000.
    "douchecabine": {"naam": "Douchecabine",
                     "trefwoorden": ["douchecabine", "complete douche", "kwartronde", "kwart rond", "douchehoek"],
                     "van": 300, "tot": 2000, "bron": ["slimster_douche"]},
    # Slimster: douchebak vanaf €75 / €200 / €500. Bovenkant verruimd naar €700 (stone-look, maatwerk).
    "douchebak": {"naam": "Douchebak",
                  "trefwoorden": ["douchebak", "douchevloer", "douchetray", "receveur"],
                  "van": 75, "tot": 700, "bron": ["slimster_douche"]},
    # Bobex: hangtoilet met inbouwreservoir €200–600; spullengids toilet-kiezen tot €1.500 (design).
    # Alleen de pot: van €100.
    "hangtoilet": {"naam": "Hangtoilet (pot)",
                   "trefwoorden": ["hangtoilet", "wandcloset", "hangcloset", "wandtoilet", "hangend toilet",
                                   "toiletpot hangend", "randloos hangtoilet", "rimless", "rimfree", "directflush",
                                   "wand-wc", "hang-wc", "toiletpot", "closetpot", "toilet", "closet", "wc"],
                   "van": 100, "tot": 900, "bron": ["bobex_toilet", "aanbod"]},
    # Bobex: staand toilet €200–500; spullengids instap vanaf €100.
    "staand_toilet": {"naam": "Staand toilet",
                      "trefwoorden": ["staand toilet", "staande closet", "duoblok", "staande wc", "pk-afvoer",
                                      "ao-afvoer", "staand closet", "closetcombinatie"],
                      "van": 100, "tot": 600, "bron": ["bobex_toilet", "aanbod"]},
    # Homedeal: inbouwreservoir €150–300. Verruimd naar €100–400.
    "inbouwreservoir": {"naam": "Inbouwreservoir (frame)",
                        "trefwoorden": ["inbouwreservoir", "inbouwframe", "toiletframe", "wc-element", "duofix",
                                        "up320", "up100", "sigma reservoir", "inbouwelement", "reservoir"],
                        "van": 100, "tot": 400, "bron": ["homedeal_toilet", "aanbod"]},
    # Aanbod: eenvoudige kunststof platen vanaf ongeveer €40, glazen design-platen tot ruim €400.
    "bedieningsplaat": {"naam": "Bedieningsplaat toilet",
                        "trefwoorden": ["bedieningsplaat", "bedieningspaneel", "drukplaat", "duwplaat", "spoelknop",
                                        "sigma01", "sigma 01", "sigma20", "sigma 20", "sigma30", "sigma 30", "sigma50",
                                        "sigma 50", "sigma60", "sigma 60", "sigma70", "teceloop", "tecesquare"],
                        "van": 40, "tot": 450, "bron": ["geberit_platen", "aanbod"]},
    # Aanbod: toiletzitting met deksel, ook softclose.
    "toiletzitting": {"naam": "Toiletzitting",
                      "trefwoorden": ["toiletzitting", "toiletbril", "closetzitting", "wc-bril", "wc bril",
                                      "zitting met deksel", "softclose zitting", "closetbril"],
                      "van": 25, "tot": 200, "bron": ["aanbod"]},
    # Slimster: sanitair voor toilet en fontein samen €250–900; fontein alleen: aanbod.
    "fontein": {"naam": "Fontein (toiletruimte)",
                "trefwoorden": ["fontein", "fonteintje", "fonteinset", "handenwasser", "fonteinbak"],
                "van": 40, "tot": 450, "bron": ["slimster_toilet", "aanbod"]},
    # Losse wastafel (zonder meubel): aanbod; Werkspot over wastafel plaatsen.
    "wastafel": {"naam": "Wastafel (los)",
                 "trefwoorden": ["wastafel", "waskom", "opzetkom", "waskommen", "meubelwastafel", "dubbele wastafel",
                                 "fontein wastafel"],
                 "van": 50, "tot": 700, "bron": ["werkspot_wastafel", "aanbod"]},
    # Spullengids wastafelmeubel-kiezen: €100 tot €2.500 (Slimster).
    "wastafelmeubel": {"naam": "Wastafelmeubel (kast met wastafel)",
                       "trefwoorden": ["wastafelmeubel", "badmeubel", "badkamermeubel", "onderkast", "meubelset",
                                       "wastafelonderkast", "badmeubelset"],
                       "van": 100, "tot": 2500, "bron": ["slimster_meubel", "aanbod"]},
    # Spiegel of spiegelkast: aanbod, ruime band.
    "spiegel_kast": {"naam": "Spiegel of spiegelkast",
                     "trefwoorden": ["spiegelkast", "spiegel", "led-spiegel", "ledspiegel", "spiegel met verlichting",
                                     "kolomkast", "hoge kast", "zijkast"],
                     "van": 40, "tot": 900, "bron": ["aanbod"]},
    # Spullengids bad-of-douche: inbouwbad instap €150 tot midden €1.000; met bubbelsysteem hoger.
    "bad": {"naam": "Inbouwbad of ligbad",
            "trefwoorden": ["inbouwbad", "ligbad", "acrylbad", "duobad", "hoekbad", "whirlpool", "bubbelbad",
                        "staal-emaille bad", "bad"],
            "van": 150, "tot": 1500, "bron": ["slimster_bad", "homedeal_bad", "aanbod"]},
    # Slimster: vrijstaand bad vanaf €300 / €900 / €2.000; Homedeal gietijzer gemiddeld €1.850.
    "vrijstaand_bad": {"naam": "Vrijstaand bad",
                       "trefwoorden": ["vrijstaand bad", "vrijstaande badkuip", "vrijstaand ligbad", "freestanding",
                                       "solid surface bad", "gietijzeren bad"],
                       "van": 300, "tot": 3000, "bron": ["slimster_vrijstaand", "homedeal_bad"]},
    # Slimster designradiator €50–800, Werkspot €150–1.200.
    "badkamerradiator": {"naam": "Badkamerradiator of designradiator",
                         "trefwoorden": ["badkamerradiator", "designradiator", "handdoekradiator", "handdoekverwarmer",
                                         "radiator", "sierradiator"],
                         "van": 50, "tot": 1200, "bron": ["slimster_radiator", "werkspot_radiator"]},
    # Spullengids badkamertegels-kopen: €10 tot €160 per m² (Slimster, Werkspot, Homedeal).
    "tegels": {"naam": "Tegels (per m²)", "eenheid": "m2",
               "trefwoorden": ["wandtegels", "vloertegels", "tegels", "tegel", "porcellanato", "keramische tegel",
                               "mozaiek", "mozaïek", "natuursteen"],
               "van": 10, "tot": 160, "bron": ["slimster_tegels", "werkspot_tegels", "homedeal_tegels"]},
    # Accessoires per stuk (handdoekhouder, toiletrolhouder, zeepdispenser): aanbod.
    "accessoires": {"naam": "Badkameraccessoire (per stuk)",
                    "trefwoorden": ["toiletrolhouder", "closetrolhouder", "handdoekhouder", "handdoekrek", "handdoekhaak",
                                    "zeepdispenser", "zeephouder", "toiletborstel", "borstelgarnituur", "planchet",
                                    "badgreep", "douchemand", "haakje", "accessoireset", "accessoires"],
                    "van": 10, "tot": 200, "bron": ["aanbod"]},
}

VASTE_CATEGORIEEN = [
    "thermostaatkraan", "douchesysteem", "handdouche_set", "wastafelkraan", "badkraan", "inbouwkraan",
    "douchegoot", "douchewand", "douchecabine", "douchebak", "hangtoilet", "staand_toilet", "inbouwreservoir",
    "bedieningsplaat", "toiletzitting", "fontein", "wastafel", "wastafelmeubel", "spiegel_kast", "bad",
    "vrijstaand_bad", "badkamerradiator", "tegels", "accessoires",
]
assert sorted(VASTE_CATEGORIEEN) == sorted(CATEGORIEEN), "categoriesleutels wijken af van de brief"

# ---------------------------------------------------------------------------
# Artikelen laden (veilig) en valideren
# ---------------------------------------------------------------------------
WAARSCHUWINGEN = []


def _waarschuw(tekst):
    WAARSCHUWINGEN.append(tekst)
    print("producten_badkamer: " + tekst, file=sys.stderr)


def _laad(modulenaam):
    try:
        mod = __import__(modulenaam)
    except ImportError:
        return [], {}
    except Exception as e:  # syntaxfout of iets anders in een bestand van een andere agent
        _waarschuw(f"{modulenaam} niet te laden ({type(e).__name__}: {e})")
        return [], {}
    art = getattr(mod, "ARTIKELEN", []) or []
    bron = getattr(mod, "BRONNEN", {}) or {}
    if not isinstance(art, list) or not isinstance(bron, dict):
        _waarschuw(f"{modulenaam}: ARTIKELEN moet een lijst zijn en BRONNEN een dict")
        return [], {}
    return art, bron


def _norm_code(c):
    return re.sub(r"[\s.\-/]", "", str(c)).upper()


def _geldig(a, bronnen):
    """Geeft een foutmelding (str) of None als het artikel klopt."""
    if not isinstance(a, dict):
        return "geen dict"
    for k in ("merk", "oms", "categorie", "bron"):
        if not isinstance(a.get(k), str) or not a.get(k).strip():
            return f"veld '{k}' ontbreekt of is leeg"
    if not isinstance(a.get("serie", ""), str):
        return "veld 'serie' moet tekst zijn"
    if a["categorie"] not in CATEGORIEEN:
        return f"onbekende categorie '{a['categorie']}'"
    codes, ean = a.get("codes", []), a.get("ean", [])
    if not isinstance(codes, list) or not all(isinstance(c, str) and len(_norm_code(c)) >= 4 for c in codes):
        return "codes moet een lijst met artikelnummers zijn"
    if not isinstance(ean, list) or not all(isinstance(e, str) and re.fullmatch(r"\d{13}", e.replace(" ", "")) for e in ean):
        return "ean moet een lijst met 13-cijferige codes zijn"
    if not codes and not ean and not (a.get("serie") or "").strip():
        return "geen artikelnummer, geen EAN en geen serie: niet te herkennen"
    van, tot = a.get("van"), a.get("tot")
    if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (van, tot)) or van <= 0 or van > tot:
        return f"prijsband klopt niet (van {van}, tot {tot})"
    if tot > van * 6:
        return f"prijsband te breed voor één artikel (van {van}, tot {tot})"
    if a["bron"] not in bronnen:
        return f"bron '{a['bron']}' staat niet in BRONNEN"
    return None


def _artikelen():
    alle, bronnen = [], {}
    for naam in ("producten_data_kranen", "producten_data_sanitair"):
        art, br = _laad(naam)
        for k, v in br.items():
            if isinstance(v, (list, tuple)) and len(v) >= 1:
                bronnen[k] = [str(v[0]), (v[1] if len(v) > 1 else None)]
        alle.extend(art)
    uit, gezien = [], set()
    for a in alle:
        fout = _geldig(a, bronnen)
        label = f"{a.get('merk', '?')} {a.get('serie', '?')} {a.get('codes', '')}" if isinstance(a, dict) else repr(a)[:60]
        if fout:
            _waarschuw(f"artikel overgeslagen ({label}): {fout}")
            continue
        sleutels = {_norm_code(c) for c in a["codes"]} | {e.replace(" ", "") for e in a["ean"]}
        if not sleutels:  # zonder code of EAN: ontdubbelen op merk + serie + omschrijving
            sleutels = {"|".join(x.strip().lower() for x in (a["merk"], a.get("serie", ""), a["oms"]))}
        dubbel = sleutels & gezien
        if dubbel:
            _waarschuw(f"artikel overgeslagen ({label}): code {sorted(dubbel)[0]} komt al voor")
            continue
        gezien |= sleutels
        uit.append({
            "merk": a["merk"].strip(), "serie": (a.get("serie") or "").strip(), "oms": a["oms"].strip(),
            "categorie": a["categorie"], "codes": [c.strip() for c in a["codes"]],
            "ean": [e.replace(" ", "") for e in a["ean"]],
            "van": round(float(a["van"]), 2) if a["van"] % 1 else int(a["van"]),
            "tot": round(float(a["tot"]), 2) if a["tot"] % 1 else int(a["tot"]),
            "bron": a["bron"],
        })
    return uit, bronnen


_ARTIKELEN, _ARTIKEL_BRONNEN = _artikelen()


def _merken():
    """Merkenlijst plus merken die alleen in de artikelen voorkomen."""
    merken = [dict(m) for m in MERKEN]
    bekend = {m["naam"].lower() for m in merken} | {a for m in merken for a in m["aliassen"]}
    for a in _ARTIKELEN:
        if a["merk"].lower() not in bekend:
            merken.append({"naam": a["merk"], "aliassen": [a["merk"].lower()]})
            bekend.add(a["merk"].lower())
    return merken


def _bronnen():
    uit = {}
    for c in CATEGORIEEN.values():
        for k in c["bron"]:
            b = _bron(k)
            if b is None:
                raise KeyError(f"bron '{k}' onbekend")
            uit[k] = b
    for a in _ARTIKELEN:
        uit[a["bron"]] = _ARTIKEL_BRONNEN[a["bron"]]
    return uit


PRODUCTDATA = {
    "peildatum": PEILDATUM,
    "merken": _merken(),
    "categorieen": CATEGORIEEN,
    "artikelen": _ARTIKELEN,
    "bronnen": _bronnen(),
}


MAX_JSON = 118 * 1024


def als_json():
    """Compacte dict voor in de pagina (JSON onder de sleutel 'producten').

    Zelfde sleutels als PRODUCTDATA en hetzelfde artikel-schema. Compact: alleen de bronnen die
    gebruikt worden, 'code_regex' alleen waar die er is; categorieen zonder 'eenheid' zijn per stuk.
    Dump met separators=(",", ":") voor de kleinste JSON."""
    d = PRODUCTDATA
    merken = []
    for m in d["merken"]:
        x = {"naam": m["naam"], "aliassen": m["aliassen"]}
        if m.get("code_regex"):
            x["code_regex"] = m["code_regex"]
        merken.append(x)
    artikelen = []
    for a in d["artikelen"]:
        artikelen.append({k: a[k] for k in ("merk", "serie", "oms", "categorie", "codes", "ean", "van", "tot", "bron")})
    uit = {
        "peildatum": d["peildatum"],
        "merken": merken,
        "categorieen": d["categorieen"],
        "artikelen": artikelen,
        "bronnen": d["bronnen"],
    }
    # Houd de JSON onder ~120 KB: worden het er te veel, dan korten we de omschrijving van de
    # bronnen van artikelen in (de URL blijft staan).
    if len(json.dumps(uit)) > MAX_JSON:
        art_bronnen = {a["bron"] for a in artikelen}
        uit["bronnen"] = {k: ([v[0][:70].rstrip() + "…", v[1]] if k in art_bronnen and len(v[0]) > 72 else v)
                          for k, v in d["bronnen"].items()}
    return uit


if __name__ == "__main__":
    j = als_json()
    tekst = json.dumps(j, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(j['artikelen'])} artikelen, {len(j['merken'])} merken, {len(j['categorieen'])} categorieen, "
          f"{len(tekst.encode('utf-8')) // 1024} KB, {len(WAARSCHUWINGEN)} waarschuwingen")
