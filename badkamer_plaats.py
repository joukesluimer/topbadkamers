# -*- coding: utf-8 -*-
"""Plaatscontent voor Top Badkamers op basis van open data (plaats_cijfers.py).

Hergebruikt de rekenhulpen uit plaats_content.py (BAG-bouwjaren, CBS-eigendom),
maar het advies gaat over badkamers in plaats van schilderwerk.

Regels:
- Alleen cijfers uit plaats_cijfers.py, met bron en peildatum op de pagina.
- Advies volgt uit bouwjaren en eigendom en uit algemeen bekende feiten
  (asbest tot 1994, loden leidingen vóór 1960). Geen claims over monteurs,
  reviews of projecten.
"""

from plaats_content import (cijfers, staafdiagram, woningen_intro, wijk_tabel, eigendom, rangorde,
                            _geschiedenis, _pct_vanaf, bronnen as _bronnen)
from components import feiten_blok
import plaats_lokaal as PL
from plaats_lokaal import lokale_faq, lokale_dienst_faq  # noqa: F401  (gebruikt door build.py)
from plaats_cijfers import META

JAAR = int(META["opgehaald"][:4])


def bronnen(c, met_wijken=False):
    return _bronnen(c, met_wijken).replace("Bewerking en telling: Topschilder", "Bewerking en telling: Top Badkamers")


def _aandelen(c):
    b = c["bag"]
    voor75 = b.get("voor_1975_pct", 0)
    j75_94 = b.get("jaren_1975_1994_pct", 0)
    vanaf05 = b.get("vanaf_2005_pct", 0)
    voor60 = max(0, 100 - _pct_vanaf(c, 1960)) if b["woningen"] else 0
    voor94 = max(0, 100 - _pct_vanaf(c, 1994)) if b["woningen"] else 0
    return voor75, j75_94, vanaf05, voor60, voor94


def advies_bouwjaren(p, c):
    """Lijst van (kop, tekst) met badkameradvies dat uit de bouwjaren volgt."""
    voor75, j75_94, vanaf05, voor60, voor94 = _aandelen(c)
    naam = p["naam"]
    uit = []
    if voor75 >= 25:
        uit.append(("Kleine badkamers in oudere woningen",
                    f"{voor75}% van de woningen in {naam} is van vóór 1975. Badkamers in die woningen zijn vaak klein, met een bad of douchebak "
                    "en een aparte wc. Met een inloopdouche, een hangtoilet en een smal wastafelmeubel haal je er vaak meer ruimte uit dan je denkt."))
    if j75_94 >= 25:
        uit.append(("Badkamers uit de jaren 75 tot 95",
                    f"{j75_94}% van de woningen is gebouwd tussen 1975 en 1995. Een badkamer gaat gemiddeld twintig tot vijfentwintig jaar mee, "
                    "dus in veel van deze huizen is de eerste badkamer al vervangen of is hij daar nu aan toe. Let op voegen, kitranden en de "
                    "afvoer: lekkage achter de tegels zie je vaak pas als het plafond eronder vlekken krijgt."))
    if vanaf05 >= 25:
        uit.append(("Jongere woningen",
                    f"{vanaf05}% van de woningen is van 2005 of later. Daar is de badkamer meestal nog goed. Vaak gaat het dan om een "
                    "upgrade: een inloopdouche in plaats van een bad, een extra toilet, of de badkamer afmaken die als casco werd opgeleverd."))
    return uit[:3]


def advies_eigendom(p, c):
    e, oms = eigendom(c)
    if not e or e.get("koop_pct") is None:
        return ""
    t = f"In {oms} is {e['koop_pct']}% van de woningen een koopwoning en {e.get('huur_pct', 0)}% een huurwoning. "
    if e.get("meergezins_pct", 0) >= 40:
        t += ("Woon je in een appartement, overleg dan vooraf met de VvE: leidingen en afvoeren lopen door het gebouw, en voor "
              "een verbouwing gelden vaak regels over geluid, werktijden en de vloeropbouw. ")
    if e.get("corporatie_pct", 0) >= 30:
        t += ("Huur je van een corporatie, dan is de badkamer in principe haar zaak. Zelf verbouwen mag meestal alleen met "
              "schriftelijke toestemming.")
    return t


def plaats_sectie(p):
    """Sectie 'woningen in cijfers' voor /badkamerspecialist/{plaats}/. Leeg zonder cijfers."""
    c = cijfers(p)
    k = PL.kerncijfers(p)
    if not c or not k:
        return ""
    gesch = _geschiedenis(p, c)
    adv = "".join(f"<h3>{kop}</h3><p>{t}</p>" for kop, t in advies_bouwjaren(p, c))
    wijk = PL.wijk_badkamer_tabel(p, k) or wijk_tabel(p, c)
    onderwerpen = [("Asbest en oude leidingen", PL.tekst_asbest(p, k)),
                   ("Hoe hard is het water?", PL.tekst_water(p, k)),
                   ("Appartementen en VvE", PL.tekst_vve(p, k)),
                   ("Monumenten en vergunning", PL.tekst_monument(p, k))]
    lokaal = "".join(f"<h3>{kop}</h3><p>{t}</p>" for kop, t in onderwerpen if t)
    return f"""<section class="section" id="woningen-in-cijfers"><div class="wrap narrow prose">
  <h2>Badkamers in {p['naam']}: wat de cijfers zeggen</h2>
  <p>{woningen_intro(p, c)} {rangorde(p)}{(' ' + gesch) if gesch else ''}</p>
  {PL.lokaal_tekst(p)}
  {feiten_blok(PL.feiten(p, k))}
  {staafdiagram(c, p['naam'])}
  {lokaal}
  <h3>De typische badkamer in {p['naam']}</h3>
  <p>{PL.periode_tekst(p, k)} {PL.vergelijk_tekst(p, k)}</p>
  {('<h3>Wat de bouwjaren betekenen voor je badkamer</h3>' + adv) if adv else ''}
  {wijk}
  {PL.bronregel(k)}
</div></section>"""


def dienst_blok(d, p):
    """Dienstspecifieke lokale alinea's op basis van bouwjaren, appartementen, monumenten en water."""
    c = cijfers(p)
    k = PL.kerncijfers(p)
    if not c or not k:
        return ""
    s = d["slug"]
    naam = p["naam"]
    voor75 = c["bag"].get("voor_1975_pct", 0)
    z = []
    w = k["water"]
    wdh = PL.dh_tekst(w) if w else ""
    oud = [g for g in k["gebieden"] if g["mediaan_bouwjaar"] < 1994][:2]
    oud_t = (" Vooral in " + PL._lijst([g["naam"] for g in oud]) + " staan veel oudere woningen.") if oud else ""

    if s == "badkamer-renoveren":
        if k["voor94"] >= 3:
            z.append(f"{k['voor94']}% van de woningen in {naam} is van vóór 1994. Plan bij die woningen een asbestcheck in vóór de sloopdag, "
                     f"anders kan het werk dagen stil komen te liggen.{oud_t}")
        if k["voor60"] >= 5:
            z.append(f"{k['voor60']}% is van vóór 1960, waar nog loden waterleidingen kunnen liggen. Neem het vervangen mee in de offerte.")
        if k["vanaf05"] >= 25:
            z.append(f"{k['vanaf05']}% is van 2005 of later. Daar gaat het vaker om een upgrade dan om een complete sloop, wat de prijs flink drukt.")
        if k["monumenten"] >= 10:
            z.append(f"Met {PL._nl(k['monumenten'])} rijksmonumenten in {naam} is het goed om te weten dat verbouwen in een rijksmonument, ook binnen, vaak een vergunning vraagt.")
    elif s == "badkamer-installeren":
        if k["voor60"] >= 5:
            z.append(f"{k['voor60']}% van de woningen in {naam} is van vóór 1960. Ziet de installateur loden leidingen, vervang die dan meteen.")
        if w:
            z.append(f"Het water in {naam} is {wdh} ({PL.klasse(w[1])}). " + ("Kies kranen en een thermostaatkraan met een goed te reinigen perlator, want kalk zet zich daar het eerst af." if w[1] >= 8 else "Kalk in kranen en de thermostaatkraan is hier weinig een probleem."))
        if k["app"] is not None and k["app"] >= 25:
            z.append(f"{k['app']}% van de woningen is een appartement. Daar zit de standleiding van de afvoer vaak op een vaste plek, wat bepaalt waar een nieuw toilet kan komen.")
    elif s == "tegelwerk-badkamer":
        if k["voor94"] >= 3:
            z.append(f"{k['voor94']}% van de woningen in {naam} is van vóór 1994. Laat bij oude vloerbedekking of plaatmateriaal onder de tegels eerst checken op asbest.")
        if k["app"] is not None and k["app"] >= 25:
            z.append(f"{k['app']}% is een appartement. Hakken en boren maakt veel geluid; in een VvE gelden vaak vaste werktijden en soms eisen aan de geluidsisolatie van de vloer.")
        if voor75 >= 25:
            z.append(f"{voor75}% van de woningen is van vóór 1975. Wanden daar zijn vaak niet vlak genoeg voor grote tegels zonder uitvlakken vooraf.")
    elif s == "inloopdouche-plaatsen":
        if voor75 >= 25:
            z.append(f"{voor75}% van de woningen is van vóór 1975. Daar ligt de afvoer vaak hoog of op een onhandige plek, en dat bepaalt of een drempelloze inloopdouche kan.")
        elif k["vanaf05"] >= 25:
            z.append(f"{k['vanaf05']}% is van 2005 of later. In die woningen is de vloer meestal goed genoeg om een inloopdouche met een goot te maken zonder veel breekwerk.")
        if w:
            z.append(f"Het water in {naam} is {wdh}. " + ("Dat geeft kalk op een glazen wand; een coating en een trekker na het douchen schelen veel poetswerk." if w[1] >= 8 else "Bij dit zachte water heb je weinig kalk op de glazen wand."))
        if k["app"] is not None and k["app"] >= 25:
            z.append(f"{k['app']}% is een appartement met meestal een betonvloer. Drempelloos is daar alleen mogelijk als er hoogte is voor afschot.")
    elif s == "toilet-renoveren":
        if k["voor94"] >= 3:
            z.append(f"{k['voor94']}% van de woningen in {naam} is van vóór 1994. In oude toiletten kan asbest zitten in de kit of de vloerbedekking.")
        if k["j75_94"] >= 25:
            z.append(f"{k['j75_94']}% is van 1975 tot 1995. Het toilet in die woningen is vaak nog het eerste of tweede; het reservoir en de afvoer zijn dan ook aan vervanging toe.")
        if k["app"] is not None and k["app"] >= 25:
            z.append(f"{k['app']}% is een appartement, waar de afvoer van het toilet direct op de standleiding van het gebouw zit.")
    elif s == "badkamer-onderhoud":
        if k["j75_94"] >= 20:
            z.append(f"{k['j75_94']}% van de woningen in {naam} is van 1975 tot 1995. In die badkamers zijn kitranden en voegen vaak aan vervanging toe, en dat voorkomt lekkage.")
        if w:
            z.append(f"Het water in {naam} is {wdh} ({PL.klasse(w[1])}). " + ("Kalk en zeepresten op kit en voegen geven schimmel een kans; maak ze regelmatig schoon met azijn of een kalkoplosser die geschikt is voor kit." if w[1] >= 8 else "Kalk is hier minder een probleem; schimmel komt vooral door te weinig ventilatie."))
    elif s == "zakelijk-badkamers":
        if k["app"] is not None:
            z.append(f"In {k['waar']} is {k['app']}% van de woningen een appartement of meergezinswoning en {k['corp'] or 0}% een corporatiewoning. "
                     "VvE's en verhuurders vervangen badkamers daar vaak per complex.")
        if k["voor94"] >= 20:
            z.append(f"{k['voor94']}% van de woningen is van vóór 1994. Neem bij projecten een asbestinventarisatie mee in de planning.")
    wz = PL.wijk_zin(d, p, k)
    if wz:
        z.append(wz)
    if not z:
        return ""
    extra = PL.lokaal_tekst(p) + PL.wijk_badkamer_tabel(p, k)
    return f"<h3>Cijfers voor {naam}</h3><p>{' '.join(z)}</p>" + extra + PL.bronregel(k)
