# -*- coding: utf-8 -*-
"""Lokale badkamerfeiten per plaats, met bron. Gebruikt door badkamer_plaats.py.

Bronnen:
- bouwjaren, wijken en buurten: BAG en CBS (plaats_cijfers.py, opgehaald door plaatsdata_ophalen.py);
- koop, huur en appartementen: CBS Kerncijfers wijken en buurten 2024;
- rijksmonumenten en beschermde gezichten: RCE (plaats_cijfers.py);
- waterhardheid: het drinkwaterbedrijf, zie WATER hieronder (alleen plaatsen met een gevonden bron).

Algemene feiten (met bron in REGELS): asbestverbod sinds 1 juli 1993, loden leidingen in
woningen van vóór 1960, vergunningplicht bij het wijzigen van een rijksmonument.

Regel: niets verzinnen. Ontbreekt een getal, dan blijft dat stukje weg.
"""
import re

from plaats_cijfers import CIJFERS, META
from plaats_content import eigendom, _pct_vanaf, _nl, _datum, monumenten_telling

# Zoekvolume Semrush (database nl, november 2026): som van "badkamer <plaats>",
# "badkamer renovatie <plaats>" en "badkamerspecialist <plaats>". De tien grootste
# krijgen het uitgebreide lokale blok met wijken en waterhardheid.
ZOEKVOLUME = {
    "almere": 1050, "amersfoort": 910, "zwolle": 860, "nijkerk": 480, "hilversum": 450,
    "harderwijk": 390, "nunspeet": 350, "kampen": 280, "zeewolde": 230, "lelystad": 230,
    "putten": 180, "dronten": 160, "ermelo": 140, "urk": 140, "emmeloord": 140,
    "bussum": 110, "elburg": 70, "huizen": 70, "naarden": 70, "weesp": 40,
    "bunschoten-spakenburg": 30, "genemuiden": 20, "blaricum": 10,
}
TOP10 = sorted(ZOEKVOLUME, key=lambda s: -ZOEKVOLUME[s])[:10]

# Algemene regels met bron.
REGELS = {
    "asbest": ("IPLO, toepassing van asbest in Nederland",
               "https://iplo.nl/thema/asbest/wat-is-asbest/toepassing-in-nederland/"),
    "lood": ("Rijksoverheid, loden leidingen opsporen en vervangen",
             "https://www.rijksoverheid.nl/onderwerpen/gezond-en-veilig-wonen/vraag-en-antwoord/hoe-kan-ik-loden-leidingen-in-mijn-huis-opsporen-en-laten-vervangen"),
    "monument": ("IPLO, rijksregels rijksmonumentenactiviteit",
                 "https://iplo.nl/regelgeving/regels-voor-activiteiten/rijksmonumentenactiviteit/rijksregels/"),
    "gezicht": ("RCE, pand in een beschermd stads- of dorpsgezicht",
                "https://www.cultureelerfgoed.nl/onderwerpen/b/beschermde-stads-en-dorpsgezichten/pand-in-een-beschermd-dorps--en-stadsgezicht"),
    "ontharder": ("Vitens, wat is hard water", "https://www.vitens.nl/over-water/wat-is-hard-water"),
}

# Waterhardheid volgens het drinkwaterbedrijf. Vorm per plaats:
#   (bedrijf, dH_laag, dH_hoog, toelichting of "", bronnaam, url, peiljaar)
# Wordt gevuld vanuit het bronnenonderzoek van november 2026; plaatsen zonder bron ontbreken.
_VT = "Vitens, waterhardheid per postcode"
_VU = "https://www.vitens.nl/over-water/waterhardheid"
_VJ = "geraadpleegd november 2026"
WATER = {
    "almere":     ("Vitens", 4.4, 5.2, "gemeten op postcodes 1325, 1335, 1351 en 1361", _VT, _VU, _VJ),
    "amersfoort": ("Vitens", 5.3, 6.1, "gemeten op postcodes 3815, 3824 en 3828", _VT, _VU, _VJ),
    "zwolle":     ("Vitens", 7.5, 7.5, "gemeten op postcode 8011", _VT, _VU, _VJ),
    "nijkerk":    ("Vitens", 6.1, 6.1, "gemeten op postcode 3861", _VT, _VU, _VJ),
    "hilversum":  ("Vitens", 6.9, 7.0, "gemeten op postcodes 1211 en 1222", _VT, _VU, _VJ),
    "harderwijk": ("Vitens", 5.5, 5.6, "gemeten op postcodes 3841 en 3843", _VT, _VU, _VJ),
    "nunspeet":   ("Vitens", 3.9, 3.9, "gemeten op postcode 8071", _VT, _VU, _VJ),
    "kampen":     ("Vitens", 6.2, 6.3, "gemeten op postcodes 8261 en 8266", _VT, _VU, _VJ),
    "zeewolde":   ("Vitens", 4.4, 4.4, "gemeten op postcode 3891", _VT, _VU, _VJ),
    "lelystad":   ("Vitens", 4.9, 5.0, "gemeten op postcodes 8232 en 8243", _VT, _VU, _VJ),
}

# Indeling die Vitens zelf gebruikt in de postcodetool.
HARDHEID_KLASSEN = [(0, 4, "zeer zacht"), (4, 8, "zacht"), (8, 12, "gemiddeld"), (12, 18, "vrij hard"), (18, 99, "hard")]


def dh_tekst(w, tot=" tot "):
    lo, hi = w[1], w[2]
    t = f"{lo:g}" + (f"{tot}{hi:g}" if hi and hi != lo else "")
    return t.replace(".", ",") + " °dH"


def klasse(dh):
    for lo, hi, naam in HARDHEID_KLASSEN:
        if lo <= dh < hi:
            return naam
    return ""


def _schoon(naam):
    return re.sub(r"^(Wijk|Buurt) \d+\s*", "", naam).strip() or naam


def gebieden(c):
    """Wijken (of buurten als er geen drie wijken zijn) met een naam, van oud naar jong."""
    g = c.get("wijken") or []
    if len(g) < 3:
        g = c.get("buurten") or []
    g = [dict(w, naam=_schoon(w["naam"])) for w in g if w.get("woningen", 0) >= 200]
    return sorted(g, key=lambda w: w["mediaan_bouwjaar"]) if len(g) >= 3 else []


def kerncijfers(p):
    """Alle getallen die de teksten gebruiken, op één plek. None zonder cijfers."""
    c = CIJFERS.get(p["slug"])
    if not c or not c["bag"]["woningen"]:
        return None
    b = c["bag"]
    e, waar = eigendom(c)
    n_mon, _ = monumenten_telling(c)
    return dict(
        c=c, woningen=b["woningen"], mediaan=b["mediaan_bouwjaar"],
        voor94=max(0, 100 - _pct_vanaf(c, 1994)), voor60=max(0, 100 - _pct_vanaf(c, 1960)),
        voor45=round(100 * sum(n for lab, n, _ in b["klassen"] if lab == "vóór 1945") / b["woningen"]),
        j75_94=b.get("jaren_1975_1994_pct", 0), vanaf05=b.get("vanaf_2005_pct", 0),
        app=e.get("meergezins_pct"), koop=e.get("koop_pct"), corp=e.get("corporatie_pct"), waar=waar,
        monumenten=n_mon, gezichten=c.get("beschermde_gezichten") or [], gebieden=gebieden(c),
        water=WATER.get(p["slug"]), top=p["slug"] in TOP10,
    )


def _lijst(items):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " en " + items[-1]


def _bron(sleutel):
    n, u = REGELS[sleutel]
    return f'<a href="{u}" rel="nofollow noopener">{n}</a>'


# ------------------------------------------------------------------ onderwerpen
def tekst_asbest(p, k):
    naam = p["naam"]
    if k["voor94"] < 3:
        return (f"Vrijwel alle woningen in {naam} zijn van 1994 of later. Asbest is in Nederland sinds 1 juli 1993 verboden, "
                "dus in een badkamer uit de bouwtijd van je huis verwacht je het niet. Is er later iets aangepast met oud materiaal, "
                "dan is een check bij twijfel nog steeds verstandig.")
    t = (f"{k['voor94']}% van de woningen in {naam} is gebouwd vóór 1994. Asbest is sinds 1 juli 1993 verboden, dus in badkamers "
         "uit die tijd kan het nog zitten: in oude vloerbedekking, kit, plaatmateriaal achter de tegels of een rioolpijp "
         f"({_bron('asbest')}). Laat bij twijfel vóór het slopen een asbestinventarisatie doen. ")
    if k["voor60"] >= 5:
        t += (f"{k['voor60']}% is zelfs van vóór 1960. In die woningen kunnen nog loden waterleidingen liggen ({_bron('lood')}). "
              "Als de muren bij een nieuwe badkamer toch opengaan, is dat het moment om ze te vervangen. ")
    g = k["gebieden"]
    if k["top"] and g:
        oud = [w for w in g if w["mediaan_bouwjaar"] < 1994][:3]
        if oud:
            delen = [f"{w['naam']} (mediaan bouwjaar {w['mediaan_bouwjaar']})" for w in oud]
            t += f"De oudste woningen staan in {_lijst(delen)}. Daar is de kans het grootst dat je dit tegenkomt."
    return t.strip()


def tekst_water(p, k):
    w = k["water"]
    if not w:
        return ""
    bedrijf, lo, hi, toel, bnaam, url, jaar = w
    dh = f"{lo:g}".replace(".", ",") + (f" tot {hi:g}".replace(".", ",") if hi and hi != lo else "")
    kl = klasse((lo + (hi or lo)) / 2)
    t = (f"Het drinkwater in {p['naam']} komt van {bedrijf}. De hardheid is {dh} °dH, dat is {kl}"
         f"{' (' + toel + ')' if toel else ''}. ")
    if (hi or lo) >= 8:
        t += ("Bij dit water zie je kalk op een glazen douchewand en in de perlator van de kraan. Kies een wand met een "
              "anti-kalkcoating, een douchekop met rubberen nopjes en droog de wand na het douchen even af. ")
    else:
        t += ("Bij zacht water heb je weinig last van kalk op de douchewand en in de kranen. Een waterontharder is dan zinloos: "
              f"volgens Vitens loont zelf ontharden pas boven ongeveer 20 °dH ({_bron('ontharder')}). ")
    t += f'<small>Bron: <a href="{url}" rel="nofollow noopener">{bnaam}</a>, {jaar}.</small>'
    return t


def tekst_vve(p, k):
    if k["app"] is None:
        return ""
    naam = p["naam"]
    t = f"In {k['waar']} is {k['app']}% van de woningen een appartement of ander meergezinshuis, en {k['koop']}% een koopwoning. "
    if k["app"] >= 25:
        t += ("Bij een koopappartement ben je lid van de VvE. Leidingen en afvoeren in de muren en vloeren zijn vaak "
              "gemeenschappelijk, en in het huishoudelijk reglement staan soms regels over werktijden, geluid en de vloer. "
              "Vraag dus vóór je offertes aanvraagt bij de VvE wat er mag. ")
    else:
        t += ("Het grootste deel is een eengezinswoning, waar je als eigenaar zelf over de badkamer beslist. "
              "Woon je wel in een appartement, overleg dan vooraf met de VvE. ")
    g = k["gebieden"]
    if k["top"] and g:
        app = sorted([w for w in g if w.get("eengezins_pct") is not None and w["eengezins_pct"] <= 60],
                     key=lambda w: w["eengezins_pct"])[:3]
        if app:
            delen = [f"{w['naam']} ({100 - w['eengezins_pct']}%)" for w in app]
            t += f"Het hoogste aandeel appartementen staat in {_lijst(delen)}. "
    if k["corp"] and k["corp"] >= 25:
        t += f"{k['corp']}% is een huurwoning van een corporatie. Daar regelt de verhuurder de badkamer, en zelf verbouwen mag alleen met toestemming."
    t += ' Meer lees je in <a href="/kennisbank/verbouwen-in-vve/">verbouwen in een VvE</a>.'
    return t.strip()


def tekst_monument(p, k):
    n, gez = k["monumenten"], k["gezichten"]
    if not n and not gez:
        return ""
    naam = p["naam"]
    delen = []
    if n:
        delen.append(f"In {naam} staan {_nl(n)} gebouwde rijksmonumenten" if n > 1 else f"In {naam} staat één gebouwd rijksmonument")
    if gez:
        soort = "een rijksbeschermd stads- of dorpsgezicht" if len(gez) == 1 else f"{len(gez)} rijksbeschermde gezichten"
        delen.append(("en " if n else f"{naam} heeft ") + f"{soort} ({_lijst(gez)})")
    t = " ".join(delen) + ". "
    t += ("Bij een rijksmonument is het hele gebouw beschermd, ook binnen. Zonder vergunning mag alleen gewoon onderhoud, en een "
          "verandering binnen aan onderdelen zonder monumentale waarde. Moet er gehakt of gebroken worden in muren of vloeren, "
          "bijvoorbeeld voor nieuwe leidingen, dan heb je meestal een omgevingsvergunning nodig "
          f"({_bron('monument')}). De gemeente {p['gemeente']} beslist daarover. ")
    if gez:
        t += ("Staat je huis in een beschermd gezicht maar is het zelf geen monument, dan is verbouwen binnen vergunningvrij. "
              "Een nieuwe ventilatiekap of afvoer door het dak of de gevel kan wel vergunningplichtig zijn "
              f"({_bron('gezicht')}). Voor een gemeentelijk monument gelden de regels uit het omgevingsplan van de gemeente. ")
    if n >= 50:
        t += "Kies dan een bedrijf dat ervaring heeft met oude panden: vloeren zijn daar vaak van hout en niet vlak, en dat vraagt een andere opbouw onder de tegels."
    return t.strip()


def bronregel(k):
    datum = _datum(META["opgehaald"])
    delen = [f"bouwjaren: BAG (Kadaster) via PDOK, stand {datum}",
             "koop, huur en appartementen: CBS, Kerncijfers wijken en buurten 2024"]
    if k["monumenten"] or k["gezichten"]:
        delen.append("rijksmonumenten en beschermde gezichten: Rijksdienst voor het Cultureel Erfgoed")
    if k["water"]:
        delen.append(f"waterhardheid: {k['water'][4]}")
    return f'<p class="pc-bron"><small>Bronnen: {"; ".join(delen)}. Bewerking: Top Badkamers.</small></p>'


def feiten(p, k):
    """Vier kerngetallen voor een feitenblok: (waarde, label)."""
    f = [(f"{k['voor94']}%", "van de woningen is van vóór 1994 (asbestrisico)")]
    if k["water"]:
        lo, hi = k["water"][1], k["water"][2]
        f.append((f"{lo:g}".replace(".", ",") + (f"–{hi:g}".replace(".", ",") if hi and hi != lo else "") + " °dH",
                  f"waterhardheid ({k['water'][0]})"))
    else:
        f.append((f"{k['voor60']}%", "van de woningen is van vóór 1960 (kans op loden leidingen)"))
    if k["app"] is not None:
        f.append((f"{k['app']}%", "appartementen en andere meergezinswoningen"))
    if k["monumenten"]:
        f.append((_nl(k["monumenten"]), "gebouwde rijksmonumenten" if k["monumenten"] > 1 else "gebouwd rijksmonument"))
    return f


# ------------------------------------------------------------------ FAQ
def lokale_faq(p):
    k = kerncijfers(p)
    if not k:
        return []
    naam = p["naam"]
    uit = []
    if k["voor94"] >= 3:
        uit.append((f"Kan er asbest in mijn badkamer in {naam} zitten?",
                    f"Dat kan als je huis van vóór 1994 is. Dat geldt voor {k['voor94']}% van de woningen in {naam}. "
                    "Asbest zat onder meer in kit, vloerbedekking en plaatmateriaal. Laat het vóór het slopen onderzoeken als je twijfelt."))
    if k["water"]:
        w = k["water"]
        dh = f"{w[1]:g}".replace(".", ",") + (f" tot {w[2]:g}".replace(".", ",") if w[2] and w[2] != w[1] else "")
        uit.append((f"Hoe hard is het water in {naam}?",
                    f"Volgens {w[0]} is het water in {naam} {dh} °dH, dat is {klasse((w[1] + (w[2] or w[1])) / 2)}. "
                    "Dat bepaalt hoe snel je kalk ziet op glas en kranen."))
    if k["app"] is not None and k["app"] >= 25:
        uit.append((f"Heb ik in een appartement in {naam} toestemming van de VvE nodig?",
                    f"Voor de badkamer zelf meestal niet, maar wel als je aan gemeenschappelijke leidingen, de afvoer of de vloer komt. "
                    f"{k['app']}% van de woningen in {k['waar']} is een appartement of meergezinswoning. Kijk in de splitsingsakte en het reglement, en meld de verbouwing vooraf."))
    if k["monumenten"] >= 10 or k["gezichten"]:
        uit.append((f"Heb ik een vergunning nodig voor een nieuwe badkamer in een monument in {naam}?",
                    "Bij een rijksmonument vaak wel, als je iets aan het gebouw verandert, ook binnen. Alleen vervangen wat er al is mag meestal zonder. "
                    f"In {naam} staan {_nl(k['monumenten'])} gebouwde rijksmonumenten. Vraag het vooraf na bij de gemeente {p['gemeente']}."))
    return uit


def lokale_dienst_faq(d, p):
    k = kerncijfers(p)
    if not k:
        return []
    s, naam = d["slug"], p["naam"]
    if s in ("inloopdouche-plaatsen", "badkamer-onderhoud", "badkamer-installeren") and k["water"]:
        w = k["water"]
        return [(f"Heb ik in {naam} last van kalk?",
                 f"Het water in {naam} is {klasse((w[1] + (w[2] or w[1])) / 2)} ({w[1]:g}".replace(".", ",") + " °dH volgens " + w[0] + "). "
                 + ("Reken op kalk op glas en kranen; een anti-kalkcoating en afdrogen helpen." if (w[2] or w[1]) >= 8
                    else "Kalk is hier weinig een probleem."))]
    if s in ("badkamer-renoveren", "tegelwerk-badkamer", "toilet-renoveren") and k["voor94"] >= 3:
        return [(f"Moet ik in {naam} op asbest letten bij het slopen?",
                 f"Bij {k['voor94']}% van de woningen in {naam} wel, want die zijn van vóór 1994. Een asbestinventarisatie vooraf voorkomt dat het werk stil komt te liggen.")]
    if s == "zakelijk-badkamers" and k["app"] is not None:
        return [(f"Hoeveel appartementen staan er in {naam}?",
                 f"In {k['waar']} is {k['app']}% van de woningen een appartement of andere meergezinswoning (CBS 2024). "
                 + (f"{k['corp']}% is een huurwoning van een corporatie." if k["corp"] else ""))]
    if s == "badkamer-installeren" and k["voor60"] >= 5:
        return [(f"Kunnen er in {naam} nog loden leidingen liggen?",
                 f"In woningen van vóór 1960 wel. Dat is {k['voor60']}% van de woningen in {naam}. Vraag de installateur ernaar als hij toch bij de leidingen moet.")]
    return []


# ------------------------------------------------------------------ per wijk
def _aandachtspunt(w):
    med = w["mediaan_bouwjaar"]
    app = 100 - w["eengezins_pct"] if w.get("eengezins_pct") is not None else None
    delen = []
    if med < 1960:
        delen.append("kans op loden leidingen en asbest")
    elif med < 1994:
        delen.append("asbestcheck vóór het slopen")
    elif med >= 2005:
        delen.append("badkamer vaak nog jong: upgrade in plaats van sloop")
    else:
        delen.append("eerste badkamer nu twintig tot dertig jaar oud")
    if w.get("voor_1945_pct", 0) >= 40:
        delen.append("veel vooroorlogse panden met houten vloeren")
    if app is not None and app >= 50:
        delen.append("vooral appartementen: VvE-regels")
    return "; ".join(delen)


def wijk_badkamer_tabel(p, k):
    """Tabel per wijk of buurt met bouwjaar, aandeel appartementen en het aandachtspunt dat daaruit volgt."""
    g = k["gebieden"]
    if not g:
        return ""
    soort = "wijk" if len(k["c"].get("wijken") or []) >= 3 else "buurt"
    rijen = "".join(
        f"<tr><td>{w['naam']}</td><td class=\"num\">{_nl(w['woningen'])}</td><td class=\"num\">{w['mediaan_bouwjaar']}</td>"
        f"<td class=\"num\">{(str(100 - w['eengezins_pct']) + '%') if w.get('eengezins_pct') is not None else '–'}</td>"
        f"<td>{_aandachtspunt(w)}</td></tr>" for w in g)
    oud, jong = g[0], g[-1]
    return f"""<h3>Per {soort}: waar let je op?</h3>
  <p>Binnen {p['naam']} verschilt het flink. In {oud['naam']} is de helft van de woningen van vóór {oud['mediaan_bouwjaar']}, in {jong['naam']} van na {jong['mediaan_bouwjaar']}. Zoek je eigen {soort} op: het aandachtspunt volgt uit het mediane bouwjaar en het aandeel appartementen.</p>
  <div class="tablewrap"><table class="pc-wijken"><thead><tr><th scope="col">{soort.capitalize()} (CBS)</th><th scope="col" class="num">Woningen</th><th scope="col" class="num">Mediaan bouwjaar</th><th scope="col" class="num">Appartementen</th><th scope="col">Aandachtspunt badkamer</th></tr></thead><tbody>{rijen}</tbody></table></div>"""


def wijk_zin(d, p, k):
    """Eén zin die per dienst de wijken of buurten noemt waar het het meest speelt."""
    g = k["gebieden"]
    if not g:
        return ""
    s = d["slug"]
    met_app = [w for w in g if w.get("eengezins_pct") is not None]
    if s in ("badkamer-renoveren", "tegelwerk-badkamer"):
        sel = [w for w in g if w["mediaan_bouwjaar"] < 1994][:3]
        t = "de oudste woningen staan, en dus de meeste badkamers die compleet aan vervanging toe zijn"
    elif s == "inloopdouche-plaatsen":
        sel = [w for w in reversed(g) if 1995 <= w["mediaan_bouwjaar"] < 2015][:3]
        t = "de woningen relatief jong zijn; daar is de vloer vaak geschikt voor een inloopdouche met goot zonder veel breekwerk"
    elif s in ("toilet-renoveren", "badkamer-onderhoud"):
        sel = [w for w in g if 1975 <= w["mediaan_bouwjaar"] < 1995][:3]
        t = "veel woningen uit 1975 tot 1995 staan, met toiletten, kit en voegen die nu vaak aan vervanging toe zijn"
    else:
        sel = sorted([w for w in met_app if w["eengezins_pct"] <= 60], key=lambda w: w["eengezins_pct"])[:3]
        t = "het aandeel appartementen het hoogst is, en je dus vaker met een VvE te maken hebt"
    if not sel:
        return ""
    namen = _lijst([f"{w['naam']} ({w['mediaan_bouwjaar']})" if s != "zakelijk-badkamers" and s != "badkamer-installeren"
                    else f"{w['naam']} ({100 - w['eengezins_pct']}% appartementen)" for w in sel])
    return f"In {p['naam']} gaat het dan vooral om {namen}, waar {t}."


# ------------------------------------------------------------------ top 10: eigen tekst
# Handgeschreven per plaats, alleen met getallen uit plaats_cijfers.py (BAG, CBS 2024, RCE).
# "Mediaan bouwjaar" = de helft van de woningen is ouder, de helft jonger.
LOKAAL_TEKST = {
    "almere": (
        "Almere is een jonge stad. De oudste woningen in de BAG zijn van 1976, en de helft van alle woningen is gebouwd na 1997. "
        "Toch zijn er grote verschillen. In de eerste wijken van Almere Haven, zoals De Werven en De Hoven, is de helft van de woningen "
        "van vóór 1978. Is de badkamer daar nooit vervangen, dan is hij nu bijna vijftig jaar oud. In Almere Stad komen de badkamers in "
        "Stedenwijk, Waterwijk en de Muziekwijk vooral uit de jaren tachtig en begin jaren negentig. In het Homeruskwartier, Duin, "
        "Nobelhorst en Oosterwold is de helft van de woningen van 2013 of later, en gaat het meestal om een upgrade. De centra van Haven, "
        "Stad en Buiten bestaan voor 87 tot 100% uit appartementen: daar regel je een nieuwe badkamer samen met de VvE."),
    "amersfoort": (
        "Amersfoort heeft een van de oudste woningvoorraden in ons werkgebied. 16% van de woningen is van vóór 1945, en de stad telt "
        "435 gebouwde rijksmonumenten en twee rijksbeschermde gezichten: de binnenstad en het Bergkwartier. In het Vermeerkwartier, "
        "De Berg-Zuid en het Leusderkwartier is de helft van de woningen van vóór 1943. Badkamers zijn daar vaak later toegevoegd, "
        "op een houten vloer, en oude leidingen zijn een aandachtspunt. In Liendert, Randenbroek en Schuilenburg, gebouwd rond 1966 tot "
        "1970, is bijna twee derde een appartement. In Nieuwland en Vathorst ligt het mediane bouwjaar tussen 1998 en 2012; daar "
        "zit vaak nog de eerste badkamer, die nu aan een opknapbeurt toe kan zijn."),
    "zwolle": (
        "Zwolle heeft 487 gebouwde rijksmonumenten en een rijksbeschermd stadsgezicht. In Assendorp is 55% van de woningen van vóór "
        "1945, in de Binnenstad 50% en in de Wipstrik 41%. Badkamers in die panden zijn vaak klein en later ingebouwd, en de kans op "
        "loden leidingen is daar het grootst. In de Binnenstad is 84% van de woningen een appartement, in Diezerpoort en Holtenbroek "
        "ongeveer twee derde. Stadshagen is met ruim 11.500 woningen de grootste wijk; de helft is gebouwd na 2006. Daar gaat het "
        "eerder om een inloopdouche of een tweede toilet dan om een complete sloop. In Aa-landen, Ittersum en Schelle, met vooral "
        "woningen uit 1975 tot 1990, is de eerste badkamer vaak aan vervanging toe."),
    "nijkerk": (
        "In Nijkerk staan volgens de BAG ruim 13.100 woningen, gelijkmatig verdeeld over de bouwperiodes. 9% is van vóór 1945 en "
        "16% uit 1965 tot 1975, de grootste groep. Daarnaast is 15% gebouwd in 2015 of later. Nijkerk telt 105 gebouwde rijksmonumenten. "
        "Volgens het CBS is 79% van de woningen een eengezinswoning en 67% een koopwoning. Als eigenaar beslis je dus meestal zelf over "
        "je badkamer. In de woningen uit de jaren zestig en zeventig is de badkamer vaak al eens vernieuwd, maar het leidingwerk niet "
        "altijd: laat dat meenemen bij de opname."),
    "hilversum": (
        "Hilversum heeft de oudste woningen van alle grote plaatsen in ons werkgebied: de helft is van vóór 1955. 28% is gebouwd tussen "
        "1920 en 1940, en de stad telt 230 gebouwde rijksmonumenten en drie rijksbeschermde gezichten: het Noordwestelijk Villagebied, "
        "Plan Oost en Hilversum-Zuid. In Oost en Zuid is meer dan de helft van de woningen van vóór 1945. Badkamers zijn daar vaak "
        "klein, soms later in een slaapkamer gebouwd, met leidingen die niet logisch lopen. In het Centrum is 68% een appartement. "
        "Alleen de Hilversumse Meent is duidelijk jonger, met een mediaan bouwjaar van 1975 en vooral eengezinswoningen."),
    "harderwijk": (
        "Harderwijk heeft een historische binnenstad met een rijksbeschermd stadsgezicht en telt 97 gebouwde rijksmonumenten. In de "
        "Binnenstad is 41% van de woningen van vóór 1945 en 58% een appartement. Tweelingstad en Stadsdennen, gebouwd rond 1960 tot "
        "1970, vormen samen een grote groep naoorlogse woningen; badkamers daar zijn vaak al eens vernieuwd, maar asbest en oude "
        "leidingen spelen nog. Stadsweiden, de Zeebuurt en Frankrijk komen uit de jaren tachtig en rond 1990. In Drielanden, met ruim 4.100 "
        "woningen, is de helft van na 2005, en het Waterfront is van na 2020."),
    "nunspeet": (
        "In Nunspeet is de helft van de woningen gebouwd vóór 1977. De grootste groep komt uit 1965 tot 1975: 24% van alle woningen. "
        "In de buurt Nunspeet-Oost is zelfs 69% van vóór 1975, in Nunspeet-West ligt het mediane bouwjaar op 1986. 81% van de woningen "
        "is een eengezinswoning. Badkamers uit de jaren zestig en zeventig zijn vaak klein, met een bad en een aparte wc; een "
        "inloopdouche en een hangtoilet geven daar veel ruimte terug. Nunspeet telt 20 gebouwde rijksmonumenten."),
    "kampen": (
        "Kampen heeft met 517 gebouwde rijksmonumenten de meeste monumenten van alle plaatsen in ons werkgebied, en een rijksbeschermd "
        "stadsgezicht. In oude panden zit de badkamer vaak op een verdieping met een houten vloer. Dat vraagt een andere opbouw "
        "onder de tegels, en verbouwen in een rijksmonument vraagt meestal een vergunning. Tegelijk is ruim "
        "een kwart van de woningen na 1995 gebouwd. 72% is een eengezinswoning en 58% een koopwoning."),
    "zeewolde": (
        "Zeewolde is gebouwd vanaf 1984, dus vrijwel geen woning is ouder dan veertig jaar. In de Eerste woonwijk ligt het mediane "
        "bouwjaar op 1986, in de Tweede woonwijk op 1991. Daar zit vaak nog de eerste of tweede badkamer, die nu aan vervanging toe is. "
        "45% van alle woningen is gebouwd tussen 1975 en 1995. In het Centrum is 65% een appartement, in de woonwijken nog geen 20%. "
        "In de Derde woonwijk en Buurt 4, met een mediaan bouwjaar van 1998 en 2018, gaat het meestal om een upgrade."),
    "lelystad": (
        "Lelystad groeide vooral in de jaren zeventig en tachtig: 53% van de woningen is gebouwd tussen 1975 en 1995. De Zuiderzeewijk "
        "en de Atolwijk zijn het oudst, met een mediaan bouwjaar van 1972 en 1974. Daar is asbest in een oude badkamer een reëel "
        "aandachtspunt. In de Zuiderzeewijk is 41% van de woningen een appartement, in het Stadshart 93%. De Kustwijk, de Boswijk en "
        "Havendiep komen uit de jaren tachtig. Warande is de jongste wijk, met een mediaan bouwjaar van 2021."),
}


def lokaal_tekst(p):
    t = LOKAAL_TEKST.get(p["slug"])
    return f"<p>{t}</p>" if t else ""


# ------------------------------------------------------------------ alle plaatsen: data-gestuurde variatie
# Wat je in een badkamer uit de grootste bouwperiode meestal aantreft. Algemene kennis,
# geen claim over een specifiek huis.
PERIODE_BADKAMER = {
    "vóór 1945": "Badkamers in vooroorlogse woningen zijn vaak later ingebouwd, soms in een kleine slaapkamer, op een houten balklaag. "
                 "Een houten vloer moet stijf genoeg zijn voor tegels en een volle douche; reken op extra werk aan de vloeropbouw.",
    "1945–1964": "In naoorlogse woningen is de badkamer meestal klein, met een douche of zitbad en een aparte wc. "
                 "Leidingen liepen vaak in het zicht of in de vloer, en lood kan nog voorkomen.",
    "1965–1974": "Woningen uit 1965 tot 1975 hebben vaak een badkamer met ligbad, kleine tegels en een betonvloer. "
                 "Bij sloop is asbest in kit, vloerzeil of plaatmateriaal een bekend aandachtspunt.",
    "1975–1984": "Badkamers uit 1975 tot 1985 zijn vaak al één keer vervangen. Waar dat niet zo is, zijn voegen, kit en afvoer "
                 "nu op leeftijd, en kan er nog asbest zitten.",
    "1985–1994": "De eerste badkamer uit 1985 tot 1995 is nu dertig tot veertig jaar oud. Vaak is de indeling goed, "
                 "maar zijn sanitair, tegels en kitwerk aan vervanging toe.",
    "1995–2004": "Badkamers uit 1995 tot 2005 zijn twintig tot dertig jaar oud. Dat is precies de leeftijd waarop veel "
                 "mensen de badkamer vernieuwen, vaak met een inloopdouche in plaats van een bad.",
    "2005–2014": "In woningen uit 2005 tot 2015 is de badkamer meestal nog in orde. Het gaat dan eerder om onderhoud van kit en "
                 "voegen, of om een upgrade zoals een regendouche of een hangtoilet.",
    "2015 en later": "Bij nieuwbouw na 2015 werd de badkamer soms casco opgeleverd of met een basispakket. "
                     "Veel bewoners maken de badkamer dan zelf af of vervangen het basissanitair.",
}


def periode_tekst(p, k):
    dom = k["c"]["bag"]["dominant"]
    t = PERIODE_BADKAMER.get(dom)
    if not t:
        return ""
    pct = next((pc for lab, _, pc in k["c"]["bag"]["klassen"] if lab == dom), 0)
    return f"De grootste groep woningen in {p['naam']} komt uit de periode {dom} ({pct}%). {t}"


def vergelijk_tekst(p, k):
    """Vergelijking met de twee dichtstbijzijnde plaatsen (volgens data.buurplaatsen) met cijfers."""
    from data import buurplaatsen
    zinnen = []
    for b in buurplaatsen(p, 6):
        kb = kerncijfers(b)
        if not kb or b["slug"] == p["slug"]:
            continue
        verschil = k["mediaan"] - kb["mediaan"]
        if abs(verschil) <= 2:
            leeftijd = f"even oud als in {b['naam']} (mediaan bouwjaar {k['mediaan']} tegen {kb['mediaan']})"
        elif verschil < 0:
            leeftijd = f"ouder dan in {b['naam']} (mediaan bouwjaar {k['mediaan']} tegen {kb['mediaan']})"
        else:
            leeftijd = f"jonger dan in {b['naam']} (mediaan bouwjaar {k['mediaan']} tegen {kb['mediaan']})"
        zin = f"De woningen in {p['naam']} zijn {leeftijd}"
        if k["app"] is not None and kb["app"] is not None and abs(k["app"] - kb["app"]) >= 5:
            zin += f", en er staan {'meer' if k['app'] > kb['app'] else 'minder'} appartementen ({k['app']}% tegen {kb['app']}%)"
        zinnen.append(zin + ".")
        if len(zinnen) == 2:
            break
    if not zinnen:
        return ""
    return " ".join(zinnen) + " Noem daarom het bouwjaar van je eigen huis in je aanvraag; dat zegt de specialist meer dan het gemiddelde van de plaats."
