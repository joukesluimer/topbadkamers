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

from plaats_content import (cijfers, staafdiagram, woningen_intro, wijk_tabel, eigendom,
                            _geschiedenis, _pct_vanaf, bronnen as _bronnen)
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
    if voor94 >= 20:
        uit.append(("Asbest bij het slopen",
                    f"Ongeveer {voor94}% van de woningen in {naam} is gebouwd vóór 1994, het jaar waarin asbest in Nederland verboden werd. "
                    "In badkamers uit die tijd kan asbest zitten, bijvoorbeeld in oude vloerbedekking, plaatmateriaal achter tegels, kitnaden of "
                    "een rioolpijp. Twijfel je, laat dan vóór het slopen een asbestinventarisatie doen. Een goede badkamerspecialist vraagt daar zelf naar."))
    if voor60 >= 10:
        uit.append(("Oude leidingen",
                    f"Zo'n {voor60}% van de woningen is van vóór 1960. In huizen uit die periode kunnen nog loden waterleidingen zitten. "
                    "Bij een nieuwe badkamer is dat het moment om de leidingen te laten vervangen, nu de muren toch open gaan."))
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
    if not c:
        return ""
    gesch = _geschiedenis(p, c)
    adv = "".join(f"<h3>{k}</h3><p>{t}</p>" for k, t in advies_bouwjaren(p, c))
    eig = advies_eigendom(p, c)
    wijk = wijk_tabel(p, c)
    return f"""<section class="section" id="woningen-in-cijfers"><div class="wrap narrow prose">
  <h2>De woningen in {p['naam']} in cijfers</h2>
  <p>{woningen_intro(p, c)}{(' ' + gesch) if gesch else ''}</p>
  {staafdiagram(c, p['naam'])}
  <h3>Wat dat betekent voor je badkamer</h3>
  {adv or '<p>De woningen hier lopen sterk uiteen in leeftijd. Noem het bouwjaar van je huis in je aanvraag; dan weet de badkamerspecialist waar hij op moet letten.</p>'}
  {f'<h3>Koop, huur en appartementen</h3><p>{eig}</p>' if eig else ''}
  {wijk}
  {bronnen(c, met_wijken=bool(wijk))}
</div></section>"""


def dienst_blok(d, p):
    """Korte, dienstspecifieke alinea op basis van de bouwjaren. Leeg zonder cijfers."""
    c = cijfers(p)
    if not c:
        return ""
    voor75, j75_94, vanaf05, voor60, voor94 = _aandelen(c)
    s = d["slug"]
    naam = p["naam"]
    z = []
    if s in ("badkamer-renoveren", "toilet-renoveren", "tegelwerk-badkamer") and voor94 >= 20:
        z.append(f"{voor94}% van de woningen in {naam} is van vóór 1994. Laat bij twijfel eerst controleren of er asbest zit in wat er gesloopt wordt.")
    if s in ("badkamer-renoveren", "badkamer-installeren") and voor60 >= 10:
        z.append(f"{voor60}% is van vóór 1960; daar kunnen nog loden waterleidingen liggen. Vervang die als de muren toch open zijn.")
    if s == "inloopdouche-plaatsen":
        if voor75 >= 25:
            z.append(f"{voor75}% van de woningen is van vóór 1975. Daar ligt de afvoer vaak hoog of op een onhandige plek, en dat bepaalt of een drempelloze inloopdouche kan.")
        elif vanaf05 >= 25:
            z.append(f"{vanaf05}% is van 2005 of later. In die woningen is de vloer meestal goed genoeg om een inloopdouche met een goot te maken zonder veel breekwerk.")
    if s == "badkamer-onderhoud" and j75_94 >= 20:
        z.append(f"{j75_94}% van de woningen is van 1975 tot 1995. In die badkamers zijn kitranden en voegen vaak aan vervanging toe, en dat voorkomt lekkage.")
    if s == "zakelijk-badkamers":
        e, _ = eigendom(c)
        if e and e.get("meergezins_pct", 0) >= 30:
            z.append(f"{e['meergezins_pct']}% van de woningen is een appartement of ander meergezinshuis. VvE's en verhuurders vervangen badkamers daar vaak per complex.")
    if not z:
        return ""
    return f"<h3>Cijfers voor {naam}</h3><p>{' '.join(z)}</p>" + bronnen(c)
