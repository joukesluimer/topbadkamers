"""Kostenpagina's voor badkamerwerk: /kosten/ en een pagina per klus.

Elke pagina heeft een snel antwoord, een prijstabel per variant, wat de prijs
bepaalt, een rekenvoorbeeld, btw-uitleg, besparingstips, wanneer je een
specialist nodig hebt, een FAQ, een CTA en de bronnen.

Alle bedragen zijn richtprijzen inclusief materiaal en 21% btw, tenzij er
"excl. btw" of "alleen arbeid" bij staat. Ze sluiten aan op data.DIENSTEN
(prijs_van, prijs_tot); waar een pagina afwijkt, staat dat in de tekst en
hieronder bij de bron. Bronnen geraadpleegd in november 2026:

- Homedeal, badkamer renoveren (€3.500 – €15.000, vaak €5.000 – €8.000):
  https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/
- Trustoo, nieuwe badkamer 2026 (€8.500 – €15.000 voor 5 – 10 m²; sloop en afvoer €1.200 – €1.800):
  https://trustoo.nl/kosten/badkamer-renovatie-kosten/
- Slimster, compleet nieuwe badkamer (budget €3.000 – €7.000, midden €7.500 – €11.000, luxe €11.000 – €15.000):
  https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/
- Werkspot, badkamer plaatsen en inloopdouche (inloopdouche €1.500 – €5.000):
  https://www.werkspot.nl/badkamer-plaatsen/prijzen-kosten
- Homedeal en Werkspot, toilet verbouwen (basis €2.500 – €4.000, compleet €4.000 – €6.500, toilet vervangen €300 – €700):
  https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/
  https://www.werkspot.nl/toiletruimte-verbouwen/prijzen-kosten
- Trustoo en Homedeal, tegelzetter (legloon €25 – €40 per m², 8 – 10 m² per dag):
  https://trustoo.nl/kosten/tegelzetter-kosten/
  https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter
- Werkspot, badkamer betegelen (tegels €20 – €60 per m², totaal €25 – €100 per m², voegmiddel €10 – €20 per zak):
  https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten
- Slimster, badkamer slopen (gemiddeld €550, €250 – €850; vloer verwijderen €19 – €40 per m²; €30 – €60 per uur):
  https://slimster.nl/sloopwerk/sloopkosten/badkamer-slopen-kosten/
- Werkspot, badkamer slopen (klein €265 – €400, standaard €400 – €550, groot €550 – €685):
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kosten-badkamer-slopen
- Werkspot, vloerverwarming badkamer (elektrisch €60 – €100 per m², water €50 – €65 per m²,
  verdeler en aansluiting €800 – €2.000, infrezen €40 – €70 per m²):
  https://www.werkspot.nl/verwarming/prijzen-kosten/vloerverwarming-badkamer
- Homedeal, vloerverwarming badkamer (kleine badkamer bijverwarming €850 – €1.600; infrezen €35 – €80 per m²):
  https://www.homedeal.nl/vloerverwarming/vloerverwarming-badkamer-kosten/
- Slimster, vloerverwarming en infrezen (infrezen €35 – €50 per m²):
  https://slimster.nl/vloerverwarming/kosten/
  https://slimster.nl/vloerverwarming/vloerverwarming-infrezen-kosten/
- Werkspot en Slimster, kitwerk badkamer (€6 – €11 per meter, starttarief €100 – €200, hele badkamer €95 – €325):
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kitwerk
  https://slimster.nl/kitwerk/kosten-kitter/badkamer-kitten/
- Homedeal, loodgieter (uurtarief €45 – €85 excl. btw):
  https://www.homedeal.nl/loodgieter/loodgieter-kosten/
- Trustoo, loodgieter (voorrijkosten gemiddeld €20 – €40):
  https://trustoo.nl/kosten/loodgieter-kosten/
- Knab, uurtarief loodgieter zzp 2026 (gemiddeld €57 per uur excl. btw):
  https://bieb.knab.nl/ondernemen/wat-verdient-een-loodgieter-zzp-bekijk-uurtarief-en-winst
- Belastingdienst, 9% btw alleen voor bepaalde werkzaamheden aan woningen ouder dan twee jaar:
  https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/tarieven_en_vrijstellingen/diensten_9_btw/werkzaamheden_aan_woningen/werkzaamheden_aan_woningen
- Rijksoverheid, asbest (verwijderen door gecertificeerd bedrijf, regels voor particulieren):
  https://www.rijksoverheid.nl/onderwerpen/asbest

Ronde 2 (zes extra pagina's), bronnen geraadpleegd in november 2026:
- Werkspot, bad plaatsen (ligbad €850 – €2.800, bad €750 – €3.000; aansluiten en plaatsen €300 – €1.000,
  afwerking €200 – €500): https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/bad-plaatsen
- Homedeal, bad plaatsen 2026 (gemiddeld €2.750, €800 – €10.000; plaatstaal vanaf €850, acryl vanaf €1.000,
  gietijzer vanaf €1.500 – €2.000, incl. montage en btw): https://www.homedeal.nl/badkamerspecialist/bad-plaatsen-kosten/
- Werkspot, sanitair plaatsen (meubel vrijstaand €200 – €500, hangend €250 – €600, dubbel €350 – €800,
  spiegelkast €150 – €300; uurtarief €45 – €80): https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/sanitair-plaatsen
- Slimster, badkamermeubel (vanaf €150 / €750 / €1.500 incl. btw, excl. montage):
  https://slimster.nl/badkamer/badkamermeubel-plaatsen-kosten/
- Homedeal, nieuwe douche 2026 (douchecabine gemiddeld €1.800, €430 – €5.200; inloopdouche €430 – €4.000;
  douchebak €85 – €740; incl. montage en btw): https://www.homedeal.nl/badkamerspecialist/nieuwe-douche-kosten/
- Slimster, douche (cabine vanaf €300 / €800 / €1.500, douchebak vanaf €75 / €200 / €500, excl. montage):
  https://slimster.nl/badkamer/douche-plaatsen-kosten/
- Trustoo, nieuwe badkamer 2026 (douchecabine plaatsen €275 – €435, verlaagde douchebak €300 – €550,
  bak of cabine demonteren vanaf €125; leidingwerk €1.250 – €2.200; elektra €300 – €1.000;
  elektrische vloerverwarming €600 – €1.100): https://trustoo.nl/kosten/badkamer-renovatie-kosten/
- Homedeal, zolder verbouwen (badkamer op zolder €20.000 – €35.000 incl. constructie, leidingen, ventilatie
  en sanitair; dakisolatie binnen €20 – €50 per m²; gipswand €40 – €50 per m²; elektra €500 – €2.000;
  dakkapel €7.000 – €9.800): https://www.homedeal.nl/verbouwing/zolder-verbouwen-kosten/
- Slimster, zolder verbouwen tot badkamer (€2.000 – €18.000): https://slimster.nl/zolder/voorbeelden/badkamer/
- Werkspot, zolder verbouwen (tussenwand €600 – €1.000, isolatie €2.000 – €5.000, dakraam €1.000 – €3.000):
  https://www.werkspot.nl/uitbouw-renovatie/prijzen-kosten/zolder-verbouwen
- Homedeal en Werkspot, toilet verbouwen (leidingen of toilet verplaatsen €700 – €1.500 extra; kleine
  leidingaanpassing €300 – €600): zie de toilet-bronnen hierboven.

Gedeelde posten (sloop, afvoer, leidingwerk, elektra, tegels, legloon, waterdicht maken, kitwerk,
montage en sanitair per onderdeel, vloerverwarming, uurtarief) komen uit richtprijzen.py. Daar staan
ook hun bronnen. Zo rekenen de kostenpagina's, de calculator en de offertechecker met dezelfde bedragen.

Voegen vernieuwen per m² (€20 – €40) en de bedragen per post in de
rekenvoorbeelden zijn een eigen inschatting, afgeleid van het legloon en de
uurtarieven hierboven. Dat staat er op de pagina ook bij.
"""

import datetime

from components import (page, title, desc, crumbs, faq_blok, cta_blok, cta_midden, offertecheck_blok,
                        prijs_balken, icon, eur, dienst_icoon)
from data import DIENST_BY_SLUG
import richtprijzen as RP

JAAR = datetime.date.today().year
MAAND = datetime.date.today().strftime("%m/%Y")

BTW_BRON = ("https://www.belastingdienst.nl/wps/wcm/connect/bldcontentnl/belastingdienst/zakelijk/btw/"
            "tarieven_en_vrijstellingen/diensten_9_btw/werkzaamheden_aan_woningen/werkzaamheden_aan_woningen")

# Bronnen met korte naam, zodat elke pagina dezelfde schrijfwijze gebruikt.
B = {
    "homedeal_badkamer": ("Homedeal, badkamer renoveren kosten", "https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/"),
    "trustoo_badkamer": ("Trustoo, wat kost een nieuwe badkamer", "https://trustoo.nl/kosten/badkamer-renovatie-kosten/"),
    "slimster_badkamer": ("Slimster, compleet nieuwe badkamer kosten", "https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/"),
    "werkspot_badkamer": ("Werkspot, badkamer plaatsen prijzen", "https://www.werkspot.nl/badkamer-plaatsen/prijzen-kosten"),
    "homedeal_toilet": ("Homedeal, toilet verbouwen kosten", "https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/"),
    "werkspot_toilet": ("Werkspot, toiletruimte verbouwen prijzen", "https://www.werkspot.nl/toiletruimte-verbouwen/prijzen-kosten"),
    "trustoo_tegel": ("Trustoo, kosten tegelzetter", "https://trustoo.nl/kosten/tegelzetter-kosten/"),
    "homedeal_tegel": ("Homedeal, kosten tegelzetter", "https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter"),
    "werkspot_tegel": ("Werkspot, badkamer betegelen prijzen", "https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten"),
    "slimster_slopen": ("Slimster, badkamer slopen kosten", "https://slimster.nl/sloopwerk/sloopkosten/badkamer-slopen-kosten/"),
    "werkspot_slopen": ("Werkspot, kosten badkamer slopen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kosten-badkamer-slopen"),
    "werkspot_vv": ("Werkspot, vloerverwarming badkamer prijzen", "https://www.werkspot.nl/verwarming/prijzen-kosten/vloerverwarming-badkamer"),
    "homedeal_vv": ("Homedeal, vloerverwarming badkamer kosten", "https://www.homedeal.nl/vloerverwarming/vloerverwarming-badkamer-kosten/"),
    "slimster_vv": ("Slimster, vloerverwarming kosten", "https://slimster.nl/vloerverwarming/kosten/"),
    "slimster_frezen": ("Slimster, vloerverwarming infrezen kosten", "https://slimster.nl/vloerverwarming/vloerverwarming-infrezen-kosten/"),
    "werkspot_kit": ("Werkspot, kitwerk badkamer prijzen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kitwerk"),
    "slimster_kit": ("Slimster, badkamer kitten kosten", "https://slimster.nl/kitwerk/kosten-kitter/badkamer-kitten/"),
    "homedeal_lood": ("Homedeal, loodgieter kosten", "https://www.homedeal.nl/loodgieter/loodgieter-kosten/"),
    "trustoo_lood": ("Trustoo, uurtarief loodgieter", "https://trustoo.nl/kosten/loodgieter-kosten/"),
    "knab_lood": ("Knab, uurtarief loodgieter zzp 2026", "https://bieb.knab.nl/ondernemen/wat-verdient-een-loodgieter-zzp-bekijk-uurtarief-en-winst"),
    "btw": ("Belastingdienst, 9% btw op werkzaamheden aan woningen", BTW_BRON),
    "asbest": ("Rijksoverheid, asbest", "https://www.rijksoverheid.nl/onderwerpen/asbest"),
    "slimster_meubel": ("Slimster, badkamermeubel plaatsen", "https://slimster.nl/badkamer/badkamermeubel-plaatsen-kosten/"),
    "slimster_douche": ("Slimster, kosten douche", "https://slimster.nl/badkamer/douche-plaatsen-kosten/"),
    "homedeal_zolder": ("Homedeal, zolder verbouwen kosten", "https://www.homedeal.nl/verbouwing/zolder-verbouwen-kosten/"),
    "slimster_zolder": ("Slimster, zolder verbouwen tot badkamer", "https://slimster.nl/zolder/voorbeelden/badkamer/"),
    "werkspot_zolder": ("Werkspot, zolder verbouwen kosten", "https://www.werkspot.nl/uitbouw-renovatie/prijzen-kosten/zolder-verbouwen"),
}
# Bronnen uit richtprijzen.py aanvullen (sleutels die hier nog niet staan).
for _k, _v in RP.BRONNEN.items():
    if _v[1]:
        B.setdefault(_k, _v)


def rp(sleutel, factor=1):
    """(laag, hoog) uit richtprijzen.py, eventueel maal een aantal, afgerond op hele euro's."""
    lo, hi = RP.lh(sleutel, factor)
    return (int(round(lo)), int(round(hi)))


def rp_niveau(sleutel, niveau):
    lo, hi = RP.RICHTPRIJZEN[sleutel]["niveaus"][niveau]
    return (lo, hi)


def som(*paren):
    """Telt (laag, hoog)-paren op."""
    return (sum(p[0] for p in paren), sum(p[1] for p in paren))


def rb(sleutel, factor=1):
    """Bandbreedte als tekst, bv. '€25 – €55'."""
    lo, hi = rp(sleutel, factor)
    return f"{eur(lo)} – {eur(hi)}"


def bedrag(van, tot, eenheid=""):
    """Bedrag van–tot; kleine bedragen (zoals per meter) zonder afronding."""
    if van == tot:
        return eur(van)
    return f"{eur(van)} – {eur(tot)}"


TOTAAL = None  # markeert in een rekenvoorbeeld de totaalregel, die wordt opgeteld

CALC = "/tools/badkamercalculator/"

# Standaard btw-uitleg; per pagina kan er een zin achter.
BTW_BASIS = (f"Over badkamerwerk betaal je <strong>21% btw</strong>: over het arbeidsloon én over het sanitair, de tegels "
             f"en de andere materialen. Het lage tarief van 9% geldt alleen voor een paar werkzaamheden aan woningen die ouder "
             f"zijn dan twee jaar, zoals stukadoren, verfwerk en het arbeidsloon bij isoleren "
             f"(<a href=\"{BTW_BRON}\" rel=\"nofollow noopener\">Belastingdienst</a>). Tegelwerk, loodgieterswerk en het plaatsen "
             f"van sanitair vallen daar niet onder.")


def tabel(koppen, rijen):
    """Eenvoudige tabel in de huisstijl. Bedragen in een kolom met 'num'."""
    th = "".join(f"<th>{k}</th>" for k in koppen)
    tr = ""
    for r in rijen:
        cellen = ""
        for i, c in enumerate(r):
            klasse = ' class="num"' if (i == 1 and ("€" in str(c) or "%" in str(c))) else ""
            cellen += f"<td{klasse}>{c}</td>"
        tr += f"<tr>{cellen}</tr>"
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# ---------------------------------------------------------------------------
# De acht kostenpagina's
# ---------------------------------------------------------------------------
# Velden:
#   slug, kort (kaarttitel), h1, title, description, dienst (slug in data.DIENSTEN),
#   van, tot, eenheid, snel (snel antwoord), varianten [(label, van, tot, uitleg)],
#   varianten_eenheid, varianten_noot, factoren [(kop, tekst)], voorbeeld (intro, rijen, slot),
#   btw_extra, besparen [..], specialist (html), faqs [(v, a)], bronnen [sleutels uit B],
#   verwant [slugs van andere kostenpagina's], kennis [(pad, tekst)]

KOSTEN = [
    # ------------------------------------------------------------------
    {
        "slug": "nieuwe-badkamer",
        "kort": "Nieuwe badkamer",
        "omschrijving": "Wat een complete badkamerrenovatie kost, van basis tot luxe.",
        "h1": f"Wat kost een nieuwe badkamer in {JAAR}?",
        "title": f"Kosten nieuwe badkamer {JAAR}: richtprijzen",
        "description": "Een nieuwe badkamer kost meestal €6.000 tot €18.000, inclusief sloop, tegels, sanitair en 21% btw. Met prijzen voor basis, midden en luxe en een rekenvoorbeeld.",
        "dienst": "badkamer-renoveren",
        "van": 6000, "tot": 18000, "eenheid": "per complete badkamer van 5 tot 9 m², inclusief btw",
        "snel": "De meeste complete badkamers van 5 tot 9 m² kosten <strong>€6.000 tot €18.000</strong>, inclusief sloopwerk, leidingwerk, tegels, sanitair, montage en 21% btw. Een eenvoudige badkamer met basissanitair kan vanaf zo'n €3.500. Verplaats je het toilet, de douche of de afvoer, of kies je luxe sanitair en grote tegels, dan kom je al snel boven de €20.000.",
        "varianten": [
            ("Basis", 3500, 7000, "Kleine badkamer, alles op dezelfde plek, standaard tegels en eenvoudig sanitair."),
            ("Midden", 7000, 12000, "Gewone badkamer met inloopdouche, wastafelmeubel, hangtoilet en tegels uit het middensegment."),
            ("Luxe", 12000, 20000, "Grote tegels, inbouwkranen, regendouche, bad of vloerverwarming, vaak met verplaatste leidingen."),
        ],
        "varianten_eenheid": "Totaalprijs per badkamer, inclusief materiaal en btw",
        "varianten_noot": "Deze indeling volgt Slimster en Homedeal; de bovengrens van luxe is open. Onze algemene richtprijs van €6.000 – €18.000 is het middensegment.",
        "factoren": [
            ("De grootte van de badkamer", "Meer vierkante meters betekent meer tegels, meer legloon en meer kitwerk. Een kleine badkamer is per m² wel duurder, omdat sloop, leidingwerk en sanitair grotendeels vaste kosten zijn."),
            ("Of de indeling verandert", "Blijven toilet, douche en wastafel op hun plek, dan kan het leidingwerk grotendeels blijven. Verplaats je de afvoer van het toilet, dan moet de vloer vaak open en loopt de prijs snel op."),
            ("Het sanitair", f"Een wastafelmeubel, toilet, douche en kranen kunnen samen {eur(rp('sanitair')[0])} kosten, maar ook {eur(rp('sanitair')[1])}. Inbouwkranen en een hangtoilet vragen ook meer werk in de muur."),
            ("De tegels", f"Tegels kosten grofweg {rb('tegels')} per m², en meer voor natuursteen. Grote formaten en mozaïek kosten ook meer legloon."),
            ("De staat van de bestaande badkamer", "Oude leidingen, een slechte vloer of een muur die niet recht is, kosten extra werk. Bij huizen van vóór 1994 kan er asbest zitten, bijvoorbeeld in oude kit, vloerzeil of een plaat achter de tegels."),
            ("Extra's", "Vloerverwarming, een designradiator, extra stopcontacten, verlichting en mechanische ventilatie tellen allemaal op."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 2 bij 3 meter (6 m²) in een tussenwoning. Alles blijft op dezelfde plek. Er komt een inloopdouche, een hangtoilet en een wastafelmeubel. Wanden tot het plafond betegeld: samen met de vloer zo'n 25 m² tegelwerk.",
            [
                ("Slopen van de oude badkamer (6 m²)", som(rp("sloop_vast"), rp("sloop_m2", 6))),
                ("Afvoer van het sloopafval", rp("afval")),
                ("Leidingwerk water en afvoer, op dezelfde plek", rp("leidingwerk")),
                ("Elektra: stopcontacten, schakelaars en spots", rp("elektra")),
                (f"Tegels, 25 m² × {rb('tegels')}", rp("tegels", 25)),
                (f"Legloon tegelwerk, 25 m² × {rb('tegelwerk')}", rp("tegelwerk", 25)),
                ("Waterdicht maken van de douchehoek", rp("waterdicht")),
                ("Sanitair (midden): douche, hangtoilet, wastafelmeubel", som(*(rp_niveau("sanitair_" + x, "midden") for x in ("douche", "toilet", "meubel")))),
                ("Montage van douche, toilet en meubel", som(rp("montage_douche"), rp("montage_toilet"), rp("montage_meubel"))),
                ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld op basis van de bronnen hieronder, met dezelfde richtprijzen als de badkamercalculator. Het laat zien waar het geld heen gaat. Je eigen badkamer kan hoger of lager uitkomen.",
        ),
        "btw_extra": "Laat je in dezelfde verbouwing ook het plafond stukadoren of verven, dan kan dat deel onder 9% vallen als de woning ouder is dan twee jaar. Het bedrijf hoort die posten dan apart op de offerte te zetten.",
        "besparen": [
            "Laat toilet, douche en wastafel op hun plek staan. Dat scheelt het meeste geld.",
            "Kies standaardmaten voor tegels, zoals 30 × 60 cm. Grote formaten en mozaïek kosten meer legloon.",
            "Tegel niet alle wanden tot het plafond. Boven de douche wel, op andere wanden kan de bovenkant ook vochtbestendig gestuct of geverfd worden.",
            "Sloop zelf, maar alleen na overleg met het bedrijf en niet als er mogelijk asbest zit.",
            "Vergelijk minimaal drie offertes, en kijk wat er wel en niet in zit. Een stelpost voor sanitair kan een lage prijs mooier laten lijken dan hij is.",
        ],
        "specialist": "Een complete badkamer is werk voor een badkamerspecialist of een aannemer die tegelzetter, loodgieter en elektricien aanstuurt. Doe het zelf alleen als je ervaring hebt met waterdicht maken en leidingwerk: een lekkage door een slecht afgedichte douche ontdek je vaak pas na maanden, als de schade bij de buren of in het plafond zit.",
        "faqs": [
            ("Hoe lang duurt een badkamerrenovatie?", "Voor een gewone badkamer meestal twee tot drie weken, inclusief droogtijd van de vloer en de lijm. Moet er veel verplaatst worden of komt er een nieuwe dekvloer, dan duurt het langer."),
            ("Wat kost een nieuwe badkamer per m²?", "Reken grofweg op €1.000 tot €2.000 per m² voor een complete badkamer. Dat is onze eigen rekensom: €6.000 tot €18.000 gedeeld door 6 tot 9 m². Kleine badkamers zitten per m² aan de bovenkant, omdat het sanitair en het leidingwerk ongeveer hetzelfde kosten als in een grote badkamer."),
            ("Zit het sanitair in de prijs?", "In de richtprijs van €6.000 tot €18.000 wel. In offertes staat het sanitair soms als stelpost: een vast bedrag dat je mag uitgeven. Kies je duurder, dan betaal je het verschil bij."),
            ("Kan ik een badkamer in delen laten doen?", "Dat kan, maar het is meestal duurder. Tegels, leidingen en afvoer hangen met elkaar samen. Wie eerst de tegels laat doen en later de douche verplaatst, betaalt twee keer voor sloop en tegelwerk."),
            ("Is een nieuwe badkamer aftrekbaar of te financieren?", "Een badkamer is niet aftrekbaar van de belasting. Je kunt hem wel meefinancieren bij een hypotheek of verbouwing; vraag daarvoor je hypotheekadviseur."),
        ],
        "bronnen": ["homedeal_badkamer", "trustoo_badkamer", "slimster_badkamer", "werkspot_badkamer", "werkspot_tegel", "slimster_slopen", "werkspot_puin", "btw"],
        "verwant": ["badkamer-slopen", "tegelzetter-per-m2", "inloopdouche"],
        "kennis": [("/kennisbank/volgorde-badkamerrenovatie/", "In welke volgorde gaat een badkamerrenovatie?"),
                   ("/kennisbank/garantie-badkamerrenovatie/", "Welke garantie mag je verwachten?")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "inloopdouche",
        "kort": "Inloopdouche",
        "omschrijving": "Wat een inloopdouche met plaatsing kost, met of zonder drempel.",
        "h1": "Wat kost een inloopdouche met plaatsing?",
        "title": f"Inloopdouche kosten {JAAR}: prijs met plaatsing",
        "description": "Een inloopdouche laten plaatsen kost €1.500 tot €5.000, inclusief btw. Lees wat het verschil maakt: de vloer, de afvoer, de douchewand en het tegelwerk.",
        "dienst": "inloopdouche-plaatsen",
        "van": 1500, "tot": 5000, "eenheid": "per inloopdouche, inclusief plaatsing en btw",
        "snel": "Een inloopdouche laten plaatsen kost meestal <strong>€1.500 tot €5.000</strong>, inclusief plaatsing en 21% btw. Komt hij op de plek van de oude douchebak, dan zit je aan de onderkant. Moet de hele vloer op afschot en opnieuw betegeld worden voor een douche zonder drempel, dan zit je aan de bovenkant of erboven.",
        "varianten": [
            ("Douchebak vervangen door glazen wand", 1500, 2500, "Op de bestaande plek, met een lage douchebak of vloerplaat en een vaste glazen wand."),
            ("Nieuwe tegelvloer met douchegoot", 2500, 4000, "De douchevloer wordt op afschot gelegd en betegeld, met een goot langs de wand."),
            ("Drempelloos, afvoer verplaatst", 3500, 5000, "De vloer moet omlaag of de afvoer wordt verlegd. Vaak samen met nieuw tegelwerk op meer wanden."),
        ],
        "varianten_eenheid": "Per inloopdouche, inclusief materiaal, plaatsing en btw",
        "varianten_noot": "De indeling in drie varianten is een eigen inschatting binnen de bandbreedte van Werkspot (€1.500 – €5.000). Bij luxe glas of een regendouche met thermostaat in de muur kan het hoger uitkomen.",
        "factoren": [
            ("De vloer en het afschot", "Water moet naar de afvoer lopen. Ligt de afvoer niet op de goede plek of moet de vloer omlaag voor een douche zonder drempel, dan is dat het grootste deel van het werk."),
            ("Douchegoot of putje", "Een goot langs de wand maakt het afschot makkelijker en ziet er strak uit, maar kost meer dan een gewoon putje."),
            ("De douchewand", "Een vaste glazen wand van 90 cm is het goedkoopst. Breder glas, een draaideur, zwart profiel of mat glas kosten meer."),
            ("Kraan en douchekop", "Een opbouwthermostaat is eenvoudig. Een inbouwthermostaat met regendouche moet in de muur worden weggewerkt."),
            ("Tegelwerk en waterdicht maken", "Rond de douche moet de vloer en de wand waterdicht worden gemaakt, met een kimband in de hoeken. Dat is niet het duurste deel, maar wel het belangrijkste."),
        ],
        "voorbeeld": (
            "Stel: je vervangt een oude douchebak van 90 × 90 cm door een inloopdouche van 120 × 90 cm met een douchegoot. De douchevloer en de wanden in de douchehoek worden opnieuw betegeld (zo'n 8 m²).",
            [
                ("Oude douchebak en tegels in de douchehoek slopen", (200, 400)),
                ("Afvoer aanpassen en douchegoot plaatsen", (400, 800)),
                ("Douchevloer op afschot en waterdicht maken", rp("waterdicht")),
                ("Tegels en legloon, 8 m²", som(rp("tegels", 8), rp("tegelwerk", 8))),
                ("Glazen wand 120 cm met montage", (400, 900)),
                ("Opbouwthermostaat met handdouche", (150, 400)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld. Het komt mooi binnen de bandbreedte, maar laat zien dat de vloer en het tegelwerk meer kosten dan de glazen wand.",
        ),
        "btw_extra": "",
        "besparen": [
            "Houd de douche op de plek van de oude douchebak. De afvoer ligt daar al.",
            "Kies een douchegoot of putje van een standaardmaat en een vaste glazen wand zonder deur.",
            "Een opbouwthermostaat is goedkoper dan inbouw en makkelijker te vervangen.",
            "Een kleine drempel van een paar centimeter is vaak veel goedkoper dan een vloer die helemaal omlaag moet.",
        ],
        "specialist": "Een inloopdouche op een bestaande douchebakplek lukt een handige doe-het-zelver soms, maar het waterdicht maken en het afschot luisteren nauw. Bel een badkamerspecialist als de vloer omlaag moet, als de afvoer verlegd wordt of als je in een appartement woont: dan kan lekkage de buren raken.",
        "faqs": [
            ("Kan een inloopdouche zonder drempel overal?", "Niet altijd. Er moet genoeg hoogte zijn voor het afschot en de afvoer. Op een betonvloer moet er soms gefreesd worden, op een houten vloer kan het lastiger zijn. Een specialist kan dat ter plekke beoordelen."),
            ("Hoe groot moet een inloopdouche zijn?", "Minimaal 90 × 120 cm is een prettige maat zonder deur. Bij een kleinere ruimte spat er sneller water buiten de douche."),
            ("Hoe lang duurt het plaatsen?", "Een inloopdouche op de plek van een douchebak is vaak in twee tot vier dagen klaar, inclusief droogtijd. Met een nieuwe vloer duurt het langer."),
            ("Is een douchegoot beter dan een putje?", "Niet beter, wel anders. Met een goot hoeft de vloer maar één kant op af te lopen, zodat je grote tegels kunt gebruiken. Een putje is goedkoper."),
        ],
        "bronnen": ["werkspot_badkamer", "homedeal_badkamer", "werkspot_tegel", "btw"],
        "verwant": ["nieuwe-badkamer", "tegelzetter-per-m2", "kitwerk-voegen"],
        "kennis": [("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel: kan dat bij jou?"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Zo wordt een badkamer waterdicht gemaakt")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "toilet-renoveren",
        "kort": "Toilet renoveren",
        "omschrijving": "Wat een nieuwe toiletruimte kost, of alleen een nieuw toilet.",
        "h1": "Wat kost een toilet renoveren?",
        "title": f"Toilet renoveren kosten {JAAR}: richtprijzen",
        "description": "Een complete toiletruimte renoveren kost €2.500 tot €6.500, inclusief btw. Alleen een nieuw toilet laten plaatsen kost €300 tot €700 aan werk. Met rekenvoorbeeld.",
        "dienst": "toilet-renoveren",
        "van": 2500, "tot": 6500, "eenheid": "per toiletruimte, inclusief btw",
        "snel": "Een complete toiletruimte met nieuwe tegels, toilet en fontein kost meestal <strong>€2.500 tot €6.500</strong>, inclusief 21% btw. Wil je alleen een nieuw staand toilet, dan kost de montage zo'n €300 tot €700, het toilet zelf niet meegerekend.",
        "varianten": [
            ("Alleen toilet vervangen (montage)", *rp("montage_toilet"), "Staand toilet op dezelfde plek, zonder ander werk. Het toilet zelf komt erbij."),
            ("Basis renovatie", 2500, 4000, "Nieuwe tegels, staand of hangend toilet en een eenvoudige fontein."),
            ("Compleet met voorzetwand", 4000, 6500, "Hangtoilet met inbouwreservoir, voorzetwand, nieuwe fontein en tegels tot het plafond."),
        ],
        "varianten_eenheid": "Inclusief materiaal en btw, tenzij anders vermeld",
        "varianten_noot": "Volgens Homedeal en Werkspot. De bovenste rij is alleen het werk.",
        "factoren": [
            ("Staand of hangend toilet", "Een hangtoilet heeft een inbouwreservoir en een voorzetwand nodig. Dat is meer werk, maar het toilet is wel makkelijker schoon te houden."),
            ("Tegels", "Een toiletruimte is klein, maar heeft veel hoeken en randen. Per m² is tegelwerk hier daarom duurder dan in een grote badkamer."),
            ("De fontein", "Een fontein met koudwaterkraan is eenvoudig. Warm water vraagt een extra leiding of een close-in boiler."),
            ("Leidingen en afvoer", "Komt het toilet op een andere plek of moet de afvoer omlaag, dan kost dat extra."),
            ("Elektra en ventilatie", "Een nieuwe lamp of een ventilator op een schakelaar tellen ook mee."),
        ],
        "voorbeeld": (
            "Stel: een toiletruimte van 0,9 × 1,5 meter. Het staande toilet wordt een hangtoilet met voorzetwand, er komt een nieuwe fontein en de wanden worden tot 1,5 meter betegeld (zo'n 9 m² met de vloer).",
            [
                ("Slopen en afvoeren", "€200 – €400"),
                ("Inbouwreservoir, voorzetwand en leidingwerk", "€700 – €1.300"),
                ("Hangtoilet met zitting", "€250 – €800"),
                ("Fontein met kraan", "€150 – €450"),
                ("Tegels en legloon, 9 m²", "€650 – €1.300"),
                ("Montage, kitwerk en afwerking", "€400 – €800"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€2.350 – €5.050</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld op basis van de bronnen hieronder.",
        ),
        "btw_extra": "Laat je het plafond of de wanden boven de tegels stukadoren of verven in een woning die ouder is dan twee jaar, dan kan alleen dat deel onder 9% vallen.",
        "besparen": [
            "Laat het toilet op dezelfde plek. Dan blijft de afvoer gewoon liggen.",
            "Tegel tot halverwege de wand en laat de rest stucen of verven.",
            "Kies een fontein met alleen koud water.",
            "Combineer de toiletruimte met de badkamer als je die ook laat doen. Je betaalt dan één keer voorrijden en opstarten.",
        ],
        "specialist": "Een staand toilet vervangen op dezelfde plek kan een handige doe-het-zelver. Voor een hangtoilet met inbouwreservoir, nieuwe leidingen of nieuw tegelwerk heb je een loodgieter of badkamerspecialist nodig. Een slecht aangesloten reservoir lekt vaak in de muur, waar je het pas laat ziet.",
        "faqs": [
            ("Hoe lang duurt een toiletrenovatie?", "Meestal drie tot vijf werkdagen. Je hebt in die tijd een paar dagen geen toilet; vraag of er een tijdelijke oplossing kan komen als je geen tweede toilet hebt."),
            ("Is een hangtoilet duurder dan een staand toilet?", "Ja, vooral door het inbouwreservoir en de voorzetwand. Reken op een paar honderd tot ruim duizend euro meer dan een staand toilet."),
            ("Kan een hangtoilet aan elke muur?", "Het inbouwframe staat op de vloer en wordt aan de muur vastgezet. Bij een lichte scheidingswand kan het, maar de wand moet stevig genoeg zijn. Een specialist ziet dat snel."),
            ("Wat kost alleen een nieuw toilet plaatsen?", "Het werk kost zo'n €300 tot €700. Daar komt het toilet zelf bij, dat er al is vanaf een paar honderd euro."),
        ],
        "bronnen": ["homedeal_toilet", "werkspot_toilet", "werkspot_tegel", "btw"],
        "verwant": ["uurtarief-loodgieter", "tegelzetter-per-m2", "nieuwe-badkamer"],
        "kennis": [("/badkamerspullen/toilet-kiezen/", "Welk toilet past bij jou?")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "tegelzetter-per-m2",
        "kort": "Tegelzetter per m²",
        "omschrijving": "Wat een tegelzetter per m² rekent voor wand- en vloertegels.",
        "h1": "Wat kost een tegelzetter per m²?",
        "title": f"Tegelzetter kosten per m² {JAAR}: legloon badkamer",
        "description": "Een tegelzetter rekent in de badkamer meestal €25 tot €55 per m² legloon, exclusief tegels. Lees wat het verschil maakt en wat een badkamer betegelen in totaal kost.",
        "dienst": "tegelwerk-badkamer",
        "van": rp("tegelwerk")[0], "tot": rp("tegelwerk")[1], "eenheid": "per m² legloon, inclusief btw, zonder tegels",
        "snel": f"Een tegelzetter rekent in de badkamer meestal <strong>{eur(rp('tegelwerk')[0])} tot {eur(rp('tegelwerk')[1])} per m²</strong> aan legloon. De tegels zelf kosten daarnaast grofweg {eur(rp('tegels')[0])} tot {eur(rp('tegels')[1])} per m². Een tegelzetter legt in een badkamer zo'n 8 tot 10 m² per dag. Voor een badkamer van 6 m² met wanden tot het plafond (zo'n 25 m²) zit je aan legloon op ongeveer {eur(rp('tegelwerk', 25)[0])} tot {eur(rp('tegelwerk', 25)[1])}.",
        "varianten": [
            ("Wandtegels, standaard formaat", 25, 40, "Bijvoorbeeld 30 × 60 cm, recht gelegd op een vlakke wand."),
            ("Vloertegels", 25, 45, "Inclusief het meenemen van afschot naar de afvoer."),
            ("Grote formaten (60 × 120 cm en groter)", 40, 55, "Zwaar en lastig te verwerken; de ondergrond moet heel vlak zijn."),
            ("Mozaïek en patroon (visgraat, diagonaal)", 45, 80, "Veel snijwerk en veel voegen. Dit valt boven onze algemene richtprijs."),
        ],
        "varianten_eenheid": "Legloon per m², inclusief btw, zonder tegels",
        "varianten_noot": "Trustoo en Homedeal noemen gemiddeld €25 – €40 per m². Onze bovengrens van €55 is voor kleine badkamers en grote formaten. Mozaïek en patronen gaan daar soms overheen; dat is een eigen inschatting.",
        "factoren": [
            ("Het formaat van de tegel", "Standaardformaten gaan het snelst. Heel kleine tegels (mozaïek) en heel grote tegels kosten meer tijd."),
            ("Het legpatroon", "Recht leggen is het goedkoopst. Halfsteens, visgraat of diagonaal geven meer snijwerk en meer afval."),
            ("De ondergrond", "Een wand die niet recht is moet eerst worden uitgevlakt of voorzien van platen. Oude tegels eraf halen kost ook tijd."),
            ("Het aantal hoeken en randen", "Een kleine badkamer met een nis, een voorzetwand en een vensterbank kost per m² meer dan een grote, rechte ruimte."),
            ("Waterdicht maken", "Rond de douche hoort een waterdichte laag met kimband. Sommige tegelzetters rekenen dat apart."),
            ("Afwerking", "Tegelprofielen op de hoeken, een nis in de douche en het voegen tellen mee. Vraag of het voegen in de prijs per m² zit."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 2 × 3 meter (6 m² vloer). De wanden worden tot 2,4 meter betegeld. Na aftrek van de deur en het raam is dat zo'n 19 m² wand. Samen met de vloer is het 25 m² tegelwerk, met tegels van 30 × 60 cm.",
            [
                (f"Legloon wand en vloer, 25 m² × {rb('tegelwerk')}", rp("tegelwerk", 25)),
                (f"Tegels, 25 m² + 10% snijverlies × {rb('tegels')}", rp("tegels", 27.5)),
                (f"Lijm en voegsel, 25 m² × {eur(rp('tegelwerk_hulpmateriaal')[0])}", rp("tegelwerk_hulpmateriaal", 25)),
                ("Waterdicht maken van de douchehoek, met kimband en afschot", rp("waterdicht")),
                ("Tegelprofielen en kitwerk", (100, 250)),
                ("Totaal tegelwerk, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld. Een tegelzetter is met 25 m² zo'n drie werkdagen bezig, plus droogtijd.",
        ),
        "btw_extra": "Een tegelzetter rekent dus altijd 21%, ook als de woning ouder is dan twee jaar. Let erop dat een prijs per m² soms exclusief btw wordt genoemd.",
        "besparen": [
            "Kies een standaardformaat en leg recht of halfsteens.",
            "Haal zelf de oude tegels van de muur, als de ondergrond daarna nog goed is. Overleg dat eerst.",
            "Koop 10% extra tegels, niet meer. Te veel tegels kun je vaak niet terugbrengen.",
            "Laat de tegelzetter de tegels adviseren of zelf inkopen: dan is hij ook verantwoordelijk als ze niet goed te verwerken zijn.",
        ],
        "specialist": "Een stukje wand betegelen kun je zelf, maar in de badkamer luistert het nauw. Een tegelvloer moet op afschot liggen en de douchehoek moet waterdicht zijn. Een fout zie je pas als het water de verkeerde kant op loopt of er vocht achter de tegels komt. Laat de douche en de vloer daarom door een tegelzetter doen.",
        "faqs": [
            ("Hoeveel m² legt een tegelzetter per dag?", "In een badkamer zo'n 8 tot 10 m². Bij grote, rechte vlakken meer, bij mozaïek of veel snijwerk minder."),
            ("Rekent een tegelzetter per m² of per uur?", "De meeste tegelzetters rekenen per m². Klein werk of reparaties gaan vaak per uur. Vraag altijd wat er in de prijs per m² zit: voorbereiden, voegen en kitten zijn niet altijd inbegrepen."),
            ("Kun je over oude tegels heen tegelen?", "Soms wel, als de oude tegels vast zitten en de vloer of wand daarna niet te hoog of te zwaar wordt. Het scheelt sloopwerk, maar de deur en de afvoer moeten wel passen."),
            ("Waarom is tegelwerk in een kleine badkamer duurder per m²?", "Omdat er per m² meer hoeken, randen en snijwerk zijn. De opstartkosten zijn ook hetzelfde."),
        ],
        "bronnen": ["trustoo_tegel", "homedeal_tegel", "werkspot_tegel", "btw"],
        "verwant": ["nieuwe-badkamer", "kitwerk-voegen", "inloopdouche"],
        "kennis": [("/kennisbank/tegels-kiezen/", "Welke tegels passen in de badkamer?"),
                   ("/badkamerspullen/badkamertegels-kopen/", "Waar let je op bij het kopen van tegels?")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "badkamer-slopen",
        "kort": "Badkamer slopen",
        "omschrijving": "Wat het slopen en afvoeren van een oude badkamer kost.",
        "h1": "Wat kost een badkamer slopen?",
        "title": f"Badkamer slopen kosten {JAAR}: prijs en afvoer",
        "description": "Een badkamer laten slopen kost meestal €250 tot €850, inclusief btw. Afvoer van puin en asbest kosten soms extra. Lees wat het verschil maakt en wanneer je zelf kunt slopen.",
        "dienst": "badkamer-renoveren",
        "van": rp("sloop")[0], "tot": rp("sloop")[1], "eenheid": "per badkamer, inclusief btw",
        "snel": f"Een badkamer laten slopen kost meestal <strong>{eur(rp('sloop')[0])} tot {eur(rp('sloop')[1])}</strong>, inclusief 21% btw. Gemiddeld is het zo'n €550. Het afvoeren van het afval kost daarnaast zo'n {rb('afval')}. Komt ook het verwijderen van een dekvloer erbij, dan kan het oplopen tot {eur(rp('sloop_compleet')[0])} à {eur(rp('sloop_compleet')[1])}. Zit er asbest in, dan moet een gecertificeerd bedrijf dat eerst weghalen.",
        "varianten": [
            ("Kleine badkamer (tot ca. 4 m²)", 265, 400, "Douche, toilet, wastafel en tegels eruit."),
            ("Standaard badkamer (5 – 8 m²)", 400, 550, "Ook bad of douchebak en meer tegelwerk."),
            ("Grote badkamer (vanaf 9 m²)", 550, 685, "Meer tegels en vaak een bad en een tweede wastafel."),
            ("Inclusief afvoer en dekvloer", *rp("sloop_compleet"), "Als de vloer tot op het beton open moet en alles wordt afgevoerd."),
        ],
        "varianten_eenheid": "Per badkamer, inclusief btw",
        "varianten_noot": "De eerste drie rijen volgen Werkspot. De onderste rij volgt Trustoo, dat een ruimere opdracht meeneemt. Daardoor lopen de bronnen zo ver uiteen.",
        "factoren": [
            ("Hoeveel er weg moet", "Alleen sanitair eruit is snel gebeurd. Tegels van de muur hakken, een tegelvloer en een dekvloer verwijderen kost veel meer tijd. Slimster noemt voor de vloer €19 tot €40 per m²."),
            ("Afvoer van puin", "Een badkamer levert al snel een paar kuub puin op. Een container of afvoer naar de milieustraat kost extra, als het niet in de prijs zit."),
            ("Bereikbaarheid", "Een badkamer op de derde verdieping zonder lift betekent alles naar beneden sjouwen."),
            ("Asbest", "In woningen van vóór 1994 kan asbest zitten in oude kit, lijm, vloerzeil, een plaat achter de tegels of een afvoer. Dat moet eerst onderzocht en door een gecertificeerd bedrijf verwijderd worden."),
            ("Leidingen afdoppen", "Water, afvoer en stroom moeten veilig worden afgesloten. Dat doet meestal de loodgieter die daarna ook de nieuwe leidingen legt."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 6 m² op de eerste verdieping. Douchebak, toilet, wastafel en alle wand- en vloertegels gaan eruit. De dekvloer blijft liggen.",
            [
                ("Sanitair demonteren en leidingen afdoppen", rp("sloop_vast")),
                ("Wandtegels verwijderen (ca. 19 m²)", (150, 300)),
                ("Vloertegels verwijderen, 6 m² × €19 – €40", (115, 240)),
                ("Puin afvoeren", rp("afval")),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld. De sloper rekent €30 tot €60 per uur; een badkamer van deze maat is meestal in één tot twee dagen leeg.",
        ),
        "btw_extra": "Sloopwerk dat bij een badkamerrenovatie hoort, valt onder 21% btw.",
        "besparen": [
            "Laat het slopen meenemen in de offerte van de badkamerspecialist. Dan is ook duidelijk wie verantwoordelijk is voor de leidingen.",
            "Sloop zelf het sanitair en de tegels, als het bedrijf dat goed vindt en er zeker geen asbest is.",
            "Laat de dekvloer liggen als die nog goed en vlak is.",
            "Vraag of je puin zelf mag wegbrengen naar de milieustraat. Bij veel gemeenten kan dat in beperkte hoeveelheden.",
        ],
        "specialist": "Zelf slopen kan, maar sluit eerst het water af en laat de leidingen door een loodgieter afdoppen. Twijfel je over asbest, stop dan en laat het onderzoeken. Asbest mag je als particulier maar in beperkte gevallen zelf verwijderen; de regels staan bij de <a href=\"https://www.rijksoverheid.nl/onderwerpen/asbest\" rel=\"nofollow noopener\">Rijksoverheid</a>. Meer uitleg vind je in <a href=\"/kennisbank/asbest-in-badkamer/\">asbest in de badkamer</a>.",
        "faqs": [
            ("Hoe lang duurt het slopen van een badkamer?", "Een gewone badkamer is meestal in één tot twee dagen leeg. Moet de dekvloer eruit, dan duurt het langer."),
            ("Mag ik zelf mijn badkamer slopen?", "Ja, maar overleg het met het bedrijf dat de nieuwe badkamer maakt. Sommige bedrijven geven minder garantie als ze niet zelf hebben gesloopt, omdat ze niet weten wat er onder de tegels zat."),
            ("Hoe weet ik of er asbest in mijn badkamer zit?", "Zeker weten doe je het alleen met een onderzoek door een gecertificeerd bedrijf. Bij woningen van vóór 1994 is de kans groter. Twijfel je, laat het dan eerst onderzoeken voordat je gaat slopen."),
            ("Zit het afvoeren van puin in de prijs?", "Niet altijd. Vraag het na. Een offerte zonder afvoer lijkt goedkoper, maar dan blijf je met een paar kuub puin zitten."),
        ],
        "bronnen": ["slimster_slopen", "werkspot_slopen", "trustoo_badkamer", "werkspot_puin", "slimster_afval", "asbest", "btw"],
        "verwant": ["nieuwe-badkamer", "uurtarief-loodgieter", "tegelzetter-per-m2"],
        "kennis": [("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer: wat nu?"),
                   ("/kennisbank/volgorde-badkamerrenovatie/", "De volgorde van een badkamerrenovatie")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "vloerverwarming-badkamer",
        "kort": "Vloerverwarming badkamer",
        "omschrijving": "Wat elektrische of watergedragen vloerverwarming in de badkamer kost.",
        "h1": "Wat kost vloerverwarming in de badkamer?",
        "title": f"Vloerverwarming badkamer kosten {JAAR}: per m²",
        "description": "Vloerverwarming in de badkamer kost €50 tot €120 per m², inclusief installatie en btw. Lees het verschil tussen elektrisch en watergedragen, en wat het stroomverbruik is.",
        "dienst": "badkamer-renoveren",
        "van": 50, "tot": 120, "eenheid": "per m², inclusief installatie en btw",
        "snel": "Vloerverwarming in de badkamer kost meestal <strong>€50 tot €120 per m²</strong>, inclusief installatie en 21% btw. Voor een kleine badkamer met elektrische matten als bijverwarming zit je op zo'n €850 tot €1.600. Watergedragen vloerverwarming is per m² niet duurder, maar daar komt de aansluiting op de cv-ketel of warmtepomp bij: €800 tot €2.000.",
        "varianten": [
            ("Elektrische matten", *rp("vloerverwarming_m2"), "Dunne matten onder de tegels. Snel aan te leggen, wel stroomverbruik."),
            ("Watergedragen, nieuwe vloer", 50, 65, "Leidingen in de dekvloer, aangesloten op de cv of warmtepomp."),
            ("Watergedragen, infrezen in bestaande vloer", 35, 80, "Sleuven in de bestaande dekvloer. Daarna komen er nieuwe tegels op."),
        ],
        "varianten_eenheid": "Per m², inclusief installatie en btw",
        "varianten_noot": f"Elektrisch volgens Werkspot, Slimster en Homedeal; watergedragen volgens Werkspot; infrezen volgens Homedeal en Slimster. Bij watergedragen komt de verdeler en de aansluiting erbij, €800 – €2.000 volgens Werkspot. Trustoo noemt voor elektrische vloerverwarming in een hele badkamer {rb('vloerverwarming_elektrisch')}.",
        "factoren": [
            ("Elektrisch of watergedragen", "Elektrisch is goedkoop aan te leggen, maar verbruikt stroom. Watergedragen is zuiniger in gebruik, maar de aansluiting op de verwarming kost meer."),
            ("Bijverwarming of hoofdverwarming", "Wil je alleen warme voeten, dan is een kleinere mat genoeg. Moet de vloer de hele badkamer verwarmen, dan heb je meer vermogen of meer leidingen nodig, en vaak nog een radiator voor de handdoeken."),
            ("De bestaande vloer", "Bij een nieuwe dekvloer kunnen de leidingen erin. In een bestaande vloer moet er gefreesd worden, of komt er een dunne mat op."),
            ("Isolatie", "Ligt de badkamer boven een koude ruimte, dan gaat er warmte naar beneden. Een isolatielaag kost extra, maar scheelt in het verbruik."),
            ("Thermostaat", "Een eigen thermostaat met klok voor de badkamer zorgt dat de vloer alleen warm is als je hem gebruikt."),
        ],
        "voorbeeld": (
            "Stel: een badkamer van 6 m², waarvan 4 m² vrije vloer (onder de douche, het toilet en het meubel komt geen verwarming). Je kiest elektrische matten als bijverwarming bij een nieuwe tegelvloer.",
            [
                (f"Elektrische mat, 4 m² × {rb('vloerverwarming_m2')} met installatie", rp("vloerverwarming_m2", 4)),
                ("Thermostaat met klok en vloervoeler", (100, 250)),
                ("Aansluiting door elektricien, eigen groep", (150, 400)),
                ("Isolatieplaten onder de mat", (60, 150)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld. <strong>Stroomverbruik:</strong> een mat van 4 m² heeft zo'n 400 tot 600 watt. Staat hij gemiddeld twee uur per dag aan, dan is dat 290 tot 440 kWh per jaar. Bij €0,25 tot €0,35 per kWh is dat ongeveer €75 tot €155 per jaar. Met een klokthermostaat kun je dat beperken.",
        ),
        "btw_extra": "Vloerverwarming valt niet onder isolatie, dus ook het arbeidsloon kent 21% btw.",
        "besparen": [
            "Leg verwarming alleen in de vrije vloer, niet onder de douche, het bad of het meubel.",
            "Kies een klokthermostaat, zodat de vloer alleen warm is als je de badkamer gebruikt.",
            "Leg vloerverwarming aan tijdens een badkamerrenovatie. Achteraf moeten de tegels er weer uit.",
            "Heb je een warmtepomp of lage-temperatuurverwarming, vraag dan of watergedragen vloerverwarming kan. Dat is zuiniger dan elektrisch.",
        ],
        "specialist": "Elektrische vloerverwarming hoort op een eigen groep met aardlekschakelaar. Laat de aansluiting door een erkende elektricien doen. Watergedragen vloerverwarming laat je door een installateur aanleggen, omdat die op je cv-ketel of warmtepomp wordt aangesloten en ingeregeld.",
        "faqs": [
            ("Is elektrische vloerverwarming duur in gebruik?", "Als bijverwarming in een kleine badkamer valt het mee: zo'n €75 tot €155 per jaar bij twee uur per dag, volgens onze rekensom. Gebruik je hem als hoofdverwarming en staat hij veel aan, dan loopt het op."),
            ("Kan vloerverwarming onder elke tegel?", "Onder keramische tegels en natuursteen werkt het goed, want die geven warmte goed door. Vraag bij de tegelwinkel of de tegel en de lijm geschikt zijn."),
            ("Is vloerverwarming genoeg als enige verwarming in de badkamer?", "In een goed geïsoleerd huis soms wel. Vaak wordt er nog een handdoekradiator bij geplaatst, voor droge handdoeken en extra warmte."),
            ("Hoe lang duurt het aanleggen?", "Elektrische matten liggen vaak in een halve dag. Daarna moeten de tegels erop. Watergedragen vloerverwarming in een nieuwe dekvloer vraagt weken droogtijd voordat er getegeld kan worden."),
        ],
        "bronnen": ["werkspot_vv", "homedeal_vv", "slimster_vv", "slimster_frezen", "trustoo_badkamer", "btw"],
        "verwant": ["nieuwe-badkamer", "tegelzetter-per-m2", "uurtarief-loodgieter"],
        "kennis": [("/kennisbank/badkamer-ventilatie/", "Ventilatie in de badkamer")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "kitwerk-voegen",
        "kort": "Kitwerk en voegen",
        "omschrijving": "Wat nieuwe kit en vernieuwde voegen in de badkamer kosten.",
        "h1": "Wat kost kitwerk en voegen vernieuwen in de badkamer?",
        "title": f"Kitwerk en voegen badkamer kosten {JAAR}",
        "description": "Nieuwe kit in de badkamer kost €6 tot €11 per meter, plus vaak een starttarief. Een hele badkamer opnieuw afkitten kost €95 tot €325. Ook de prijs van voegen vernieuwen.",
        "dienst": "badkamer-onderhoud",
        "van": rp("kitwerk")[0], "tot": rp("kitwerk")[1], "eenheid": "per meter kitwerk, inclusief btw",
        "snel": f"Oude kit verwijderen en nieuwe kit aanbrengen kost <strong>{eur(rp('kitwerk')[0])} tot {eur(rp('kitwerk')[1])} per meter</strong>, inclusief 21% btw. Veel vakmensen rekenen daarnaast een starttarief van €100 tot €200. Een hele badkamer opnieuw afkitten kost daarom meestal <strong>{eur(rp('kitwerk_badkamer')[0])} tot {eur(rp('kitwerk_badkamer')[1])}</strong>. Voegen vernieuwen kost grofweg €20 tot €40 per m².",
        "varianten": [
            ("Kitwerk per meter", *rp("kitwerk"), "Oude kit eruit, schoonmaken en nieuwe sanitairkit erin."),
            ("Hele badkamer afkitten", *rp("kitwerk_badkamer"), "Douche, bad, wastafel, toilet en vloerranden samen."),
            ("Starttarief (los)", 100, 200, "Voor voorrijden en opstarten, bij kleine klussen."),
            ("Voegen vernieuwen per m²", 20, 40, "Oude voeg eruit frezen en nieuwe voeg aanbrengen. Eigen inschatting."),
        ],
        "balken": False,
        "varianten_eenheid": "Inclusief materiaal en btw",
        "varianten_noot": "Kitwerk volgens Werkspot en Slimster. Voegen vernieuwen is een eigen inschatting op basis van het legloon van tegelzetters (€20 – €40 per m² volgens Werkspot).",
        "factoren": [
            ("Hoeveel meter kit", "Een douchehoek heeft zo'n 5 tot 8 meter kit, een hele badkamer al snel 15 tot 30 meter."),
            ("De oude kit", "Schimmelige of harde kit moet helemaal weg en de rand moet schoon en droog zijn. Dat kost meer tijd dan de nieuwe kit erin spuiten."),
            ("Schimmel en vocht", "Zit er vocht achter de kit of de tegels, dan is nieuwe kit maar een pleister. Dan moet eerst de oorzaak worden gevonden."),
            ("Voegen of kit", "Voegen zitten tussen de tegels, kit zit in de hoeken en langs het sanitair. Voegen vernieuwen is veel meer werk dan kitten."),
            ("Starttarief", "Bij een kleine klus is het starttarief vaak het grootste deel van de rekening. Combineer het daarom met ander klein werk."),
        ],
        "voorbeeld": (
            "Stel: de kit in je badkamer is zwart van de schimmel. Er moet nieuwe kit in de douchehoek, langs het bad, rond de wastafel en het toilet en langs de vloer: samen zo'n 20 meter.",
            [
                (f"Oude kit verwijderen en nieuwe aanbrengen, 20 m × {rb('kitwerk')}", rp("kitwerk", 20)),
                ("Starttarief (als de vakman het rekent)", (0, 200)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld. Komen er ook nieuwe voegen in de douche, reken dan op €20 tot €40 per m² extra. Voor 6 m² douchewand is dat €120 tot €240.",
        ),
        "btw_extra": "",
        "besparen": [
            "Vervang kit op tijd. Een losse of gescheurde kitrand laat water door, en vochtschade is veel duurder dan nieuwe kit.",
            "Laat alle kit in één keer doen, zodat je het starttarief maar één keer betaalt.",
            "Droog de douche na het douchen met een trekker. Dan blijft kit veel langer schoon.",
            "Is alleen de bovenkant van de voeg vies, probeer dan eerst een voegenreiniger. Vernieuwen is pas nodig als de voeg zacht of kapot is.",
        ],
        "specialist": "Kitten kun je zelf leren, maar een strakke, waterdichte kitrand is lastiger dan het lijkt. Bel een vakman als de kit steeds weer loslaat, als er zwarte plekken achter de kit blijven of als je vocht ziet in de muur of het plafond eronder. Dan is er vaak meer aan de hand dan alleen oude kit.",
        "faqs": [
            ("Hoe vaak moet kit in de badkamer vervangen worden?", "Gemiddeld om de vijf tot tien jaar, of eerder als er schimmel in zit die niet meer weggaat, of als de kit loslaat of scheurt."),
            ("Kan ik nieuwe kit over oude kit spuiten?", "Nee. Nieuwe kit hecht slecht op oude kit, en schimmel groeit gewoon door. De oude kit moet er helemaal uit."),
            ("Hoe lang moet nieuwe kit drogen?", "Meestal 24 uur voordat je weer kunt douchen. Kijk op de koker; sommige kit heeft langer nodig."),
            ("Wat is het verschil tussen voegen en kit?", "Voegen zijn hard en zitten tussen de tegels. Kit is flexibel en zit in de hoeken en langs het sanitair, waar dingen een beetje kunnen bewegen."),
        ],
        "bronnen": ["werkspot_kit", "slimster_kit", "werkspot_tegel", "btw"],
        "verwant": ["tegelzetter-per-m2", "inloopdouche", "uurtarief-loodgieter"],
        "kennis": [("/kennisbank/badkamer-waterdicht-maken/", "Een badkamer waterdicht maken"),
                   ("/kennisbank/badkamer-ventilatie/", "Goede ventilatie tegen schimmel")],
    },
    # ------------------------------------------------------------------
    {
        "slug": "uurtarief-loodgieter",
        "kort": "Uurtarief loodgieter",
        "omschrijving": "Wat een loodgieter per uur rekent, met voorrijkosten en spoedtoeslag.",
        "h1": f"Wat is het uurtarief van een loodgieter in {JAAR}?",
        "title": f"Uurtarief loodgieter {JAAR}: prijs per uur",
        "description": "Een loodgieter rekent meestal €45 tot €85 per uur excl. btw, plus voorrijkosten van €20 tot €50. Lees wat spoed, avond en weekend kosten en wat kleine klussen kosten.",
        "dienst": "badkamer-installeren",
        "van": rp("uurtarief")[0], "tot": rp("uurtarief")[1], "eenheid": "per uur, exclusief btw",
        "snel": f"Een loodgieter rekent meestal <strong>{eur(rp('uurtarief')[0])} tot {eur(rp('uurtarief')[1])} per uur, exclusief btw</strong>. Met 21% btw is dat {eur(round(rp('uurtarief')[0] * 1.21))} tot {eur(round(rp('uurtarief')[1] * 1.21))} per uur. Daar komen vaak voorrijkosten van {rb('voorrijkosten')} bij. Voor spoed, 's avonds of in het weekend betaal je meer: vaak 50 tot 100% toeslag op het uurtarief.",
        "varianten": [
            ("Uurtarief, werkdag", *rp("uurtarief"), "Gewoon werk overdag, op afspraak."),
            ("Voorrijkosten", *rp("voorrijkosten"), "Per bezoek. Soms vervalt dit bij een grotere klus."),
            ("Uurtarief, avond en weekend", 70, 170, "Met 50 tot 100% toeslag. Eigen inschatting op basis van het gewone uurtarief."),
            ("Spoed voorrijden", 50, 150, "Bij spoed, buiten werktijd, komt er een hoger voorrijtarief."),
        ],
        "balken": False,
        "varianten_eenheid": "Exclusief btw",
        "varianten_noot": "Uurtarief volgens Homedeal (€45 – €85); het Knab Uurtarievenboekje noemt een gemiddelde van €57 voor zzp-loodgieters. Voorrijkosten volgens Trustoo en Homedeal. De toeslagen verschillen sterk per bedrijf.",
        "factoren": [
            ("Wanneer je belt", "Overdag op afspraak is het goedkoopst. Spoed, avond, nacht en weekend kosten een flinke toeslag."),
            ("Waar je woont", "In de Randstad liggen de tarieven vaak hoger dan in de rest van het land. Woont de loodgieter verder weg, dan zijn de voorrijkosten hoger."),
            ("Zzp'er of bedrijf", "Een zelfstandige is vaak goedkoper per uur dan een groter installatiebedrijf met personeel en een bus vol voorraad."),
            ("Vaste prijs of uurtarief", "Kleine klussen, zoals een toilet vervangen, gaan vaak voor een vaste prijs. Bij lekkage zoeken weet niemand vooraf hoe lang het duurt; dat gaat per uur."),
            ("Materiaal", "Kranen, sifons, leidingen en koppelingen komen bovenop het uurtarief. Vraag vooraf of de loodgieter dat bij zich heeft."),
        ],
        "voorbeeld": (
            "Stel: je wilt een nieuwe wastafelkraan en een nieuwe sifon laten plaatsen. De loodgieter komt op een doordeweekse dag en is anderhalf uur bezig. Je kraan heb je zelf gekocht.",
            [
                ("Arbeid, 1,5 uur × €45 – €85", "€67,50 – €127,50"),
                ("Voorrijkosten", "€20 – €50"),
                ("Sifon en koppelingen", "€15 – €40"),
                ("Subtotaal exclusief btw", "€102,50 – €217,50"),
                ("21% btw", "€21,53 – €45,68"),
                ("<strong>Totaal, inclusief btw</strong>", "<strong>€124,03 – €263,18</strong>"),
            ],
            "Dit is een eigen rekenvoorbeeld. Veel loodgieters rekenen per half uur of hebben een minimumtarief van een uur.",
        ),
        "btw_extra": "Let op: veel loodgieters noemen hun uurtarief exclusief btw. Vergelijk daarom altijd prijzen met of zonder btw, en niet door elkaar.",
        "besparen": [
            "Bel niet met spoed als het kan wachten. Sluit bij een lekkage eerst de hoofdkraan af, dan kan de loodgieter vaak de volgende werkdag komen.",
            "Bundel klussen: laat de lekkende kraan, het toilet en de sifon in één bezoek doen.",
            "Vraag bij grotere klussen om een vaste prijs in plaats van een uurtarief.",
            "Vraag vooraf naar voorrijkosten, minimumtarief en of het uurtarief met of zonder btw is.",
        ],
        "specialist": "Een sifon of een douchekop vervangen kun je vaak zelf. Bel een loodgieter bij lekkages in de muur of de vloer, bij werk aan de waterleiding of de afvoer, en als er iets aan de cv-ketel of warmwatervoorziening moet. Werk aan gasleidingen mag je nooit zelf doen.",
        "faqs": [
            ("Is het uurtarief van een loodgieter inclusief btw?", "Meestal niet. De meeste loodgieters noemen hun tarief exclusief btw. Met 21% btw wordt €60 per uur dus €72,60."),
            ("Wat zijn normale voorrijkosten?", "Zo'n €20 tot €50 per bezoek. Sommige loodgieters rekenen geen voorrijkosten als de klus boven een bepaald bedrag uitkomt."),
            ("Wat kost een spoedloodgieter?", "Bij spoed buiten werktijd betaal je vaak 50 tot 100% meer per uur en een hoger voorrijtarief. Vraag altijd aan de telefoon wat het gaat kosten."),
            ("Rekent een loodgieter per uur of per klus?", "Allebei komt voor. Kleine, voorspelbare klussen gaan vaak voor een vaste prijs, zoeken naar lekkage en onvoorspelbaar werk per uur."),
        ],
        "bronnen": ["homedeal_lood", "trustoo_lood", "knab_lood", "btw"],
        "verwant": ["toilet-renoveren", "kitwerk-voegen", "badkamer-slopen"],
        "kennis": [("/badkamerspullen/kranen-kiezen/", "Waar let je op bij een nieuwe kraan?")],
    },
    # ==================================================================
    # Ronde 2: zes extra pagina's
    # ==================================================================
    {
        # Bronnen: Werkspot bad plaatsen (ligbad €850 – €2.800; aansluiten €300 – €1.000, afwerking €200 – €500),
        # Homedeal bad plaatsen (gemiddeld €2.750, €800 – €10.000; plaatstaal vanaf €850, acryl vanaf €1.000).
        "slug": "bad-plaatsen",
        "kort": "Bad plaatsen",
        "omschrijving": "Wat een nieuw ligbad met plaatsing kost, van inbouwbad tot vrijstaand bad.",
        "h1": "Wat kost een bad laten plaatsen?",
        "title": f"Bad laten plaatsen kosten {JAAR}: prijs met montage",
        "description": "Een nieuw ligbad laten plaatsen kost meestal €850 tot €3.000, inclusief bad, montage en btw. Lees wat een vrijstaand bad kost en wat de prijs bepaalt.",
        "dienst": "badkamer-installeren",
        "van": 850, "tot": 3000, "eenheid": "per ligbad, inclusief montage en btw",
        "snel": f"Een nieuw ligbad laten plaatsen kost meestal <strong>€850 tot €3.000</strong>, inclusief het bad, de montage en 21% btw. Homedeal noemt een gemiddelde van zo'n €2.750. Heb je het bad al, dan kost alleen het plaatsen en aansluiten {rb('montage_bad')}. Een vrijstaand bad met een vloer- of wandkraan is duurder: reken op €2.500 tot €6.000, en soms meer.",
        "varianten": [
            ("Inbouwbad op dezelfde plek", 850, 2000, "Plaatstaal of acryl, op de plek van het oude bad, met de bestaande ombouw of een badpaneel."),
            ("Inbouwbad met nieuwe ombouw en tegels", 1500, 3500, "Het oude bad en de ombouw gaan eruit. Er komt een nieuwe ombouw die wordt betegeld."),
            ("Vrijstaand bad", 2500, 6000, "Bad met een vloer- of wandkraan. De afvoer en de waterleiding moeten vaak naar een nieuwe plek."),
            ("Alleen plaatsen en aansluiten", *rp("montage_bad"), "Je hebt het bad al. Zonder ombouw, tegelwerk en afvoer van het oude bad."),
        ],
        "varianten_eenheid": "Per bad, inclusief btw",
        "varianten_noot": "De eerste rij volgt Homedeal (plaatstaal vanaf €850, acryl vanaf €1.000) en Werkspot (ligbad €850 – €2.800). De rijen met ombouw en vrijstaand bad zijn een eigen inschatting; Homedeal noemt als bovengrens €10.000. Alleen plaatsen volgt Werkspot.",
        "factoren": [
            ("Het soort bad", "Plaatstaal is het goedkoopst en stevig. Acryl is licht en warm aan je huid. Gietijzer en solid surface zijn zwaar en duur. Een bad met bubbels of verlichting kost honderden euro's meer."),
            ("Inbouw of vrijstaand", "Een inbouwbad staat in een ombouw tegen de muur. Een vrijstaand bad staat los in de ruimte. Dan moeten de afvoer en vaak ook de waterleiding naar het midden van de vloer, en heb je een vloerkraan of wandkraan nodig."),
            ("De ombouw en het tegelwerk", "Een nieuwe ombouw van gasbeton of een badpaneel moet worden betegeld of afgewerkt. Vaak gaan er dan ook tegels op de wand rond het bad mee."),
            ("De afvoer en de kraan", "Staat het nieuwe bad op de plek van het oude, dan kan de afvoer vaak blijven. Een inbouwkraan of thermostaat in de muur betekent hakken en weer dichtmaken."),
            ("De vloer", "Een gevuld bad weegt al snel enkele honderden kilo's, met een zwaar bad of een vrijstaand bad meer. Op een houten vloer moet iemand kijken of die dat aankan."),
            ("Het oude bad", "Een oud gietijzeren bad is zwaar om weg te halen. Vraag of het slopen en afvoeren in de prijs zit."),
        ],
        "voorbeeld": (
            "Stel: je vervangt een oud inbouwbad van 170 × 75 cm door een nieuw acryl bad van dezelfde maat. Het komt op dezelfde plek, met een nieuwe ombouw die wordt betegeld (zo'n 2 m²).",
            [
                ("Oud bad en ombouw slopen", (150, 350)),
                ("Afvoer van het oude bad en het puin", (75, 200)),
                ("Acryl bad met badkraan (midden)", rp_niveau("sanitair_bad", "midden")),
                ("Bad plaatsen en aansluiten", rp("montage_bad")),
                ("Nieuwe ombouw maken", (150, 300)),
                ("Tegels en legloon ombouw, 2 m²", som(rp("tegels", 2), rp("tegelwerk", 2))),
                ("Kitwerk rond het bad, 4 meter", rp("kitwerk", 4)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld op basis van de bronnen hieronder en dezelfde richtprijzen als de badkamercalculator. Kies je een vrijstaand bad of moet de wand rond het bad ook opnieuw betegeld worden, dan kom je hoger uit.",
        ),
        "btw_extra": "Ook als je alleen het plaatsen laat doen, betaal je 21% over het arbeidsloon.",
        "besparen": [
            "Zet het nieuwe bad op de plek van het oude. Dan kunnen de afvoer en de waterleiding blijven.",
            "Kies een standaardmaat, zoals 170 × 75 of 180 × 80 cm. Dan past het in de bestaande ombouw.",
            "Een badpaneel is sneller geplaatst dan een betegelde ombouw.",
            "Kies een opbouwkraan op de rand of de muur in plaats van een inbouwkraan.",
            "Laat het bad meenemen in een grotere klus, zoals nieuwe tegels. Dan betaal je één keer voorrijden en opstarten.",
        ],
        "specialist": "Een bad aansluiten op de afvoer en de waterleiding kan een handige doe-het-zelver, maar het kitwerk en de waterdichte aansluiting op de muur luisteren nauw. Lekt het langs de rand van het bad, dan zie je dat vaak pas als het plafond eronder vlekken krijgt. Laat een vrijstaand bad, een bad op een houten vloer of een bad met een inbouwkraan door een badkamerspecialist of loodgieter plaatsen.",
        "faqs": [
            ("Hoe lang duurt het plaatsen van een bad?", "Een bad op dezelfde plek is vaak in één tot twee dagen geplaatst. Met een nieuwe ombouw en tegelwerk duurt het langer, omdat de lijm en de voegen moeten drogen."),
            ("Kan een bad op een houten vloer?", "Vaak wel, maar een gevuld bad is zwaar. Laat iemand kijken naar de balken en de vloer. Soms moet de vloer worden verstevigd, vooral bij een gietijzeren of vrijstaand bad."),
            ("Wat is goedkoper: een bad of een douche?", "Een eenvoudig inbouwbad is niet veel duurder dan een douche met glazen wand. Een vrijstaand bad of een inloopdouche zonder drempel is wel duurder. Lees ook <a href=\"/badkamerspullen/bad-of-douche/\">bad of douche</a>."),
            ("Kan ik mijn bad vervangen zonder de tegels te slopen?", "Soms. Als het nieuwe bad precies dezelfde maat heeft, kan het oude eruit zonder dat de wandtegels sneuvelen. Vaak gaat er toch een rij tegels kapot. Houd daarom een paar reservetegels achter de hand."),
        ],
        "bronnen": ["werkspot_bad", "homedeal_bad", "trustoo_badkamer", "werkspot_tegel", "btw"],
        "verwant": ["bad-vervangen-door-douche", "nieuwe-badkamer", "tegelzetter-per-m2"],
        "kennis": [("/badkamerspullen/bad-of-douche/", "Bad of douche: wat past bij jou?"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Zo wordt een badkamer waterdicht gemaakt")],
    },
    # ------------------------------------------------------------------
    {
        # Bronnen: Homedeal nieuwe douche (inloopdouche €430 – €4.000 incl. montage en btw), Werkspot
        # inloopdouche €1.500 – €5.000, Trustoo (verlaagde douchebak €300 – €550, demonteren vanaf €125).
        # De bandbreedte €2.000 – €6.000 is een eigen inschatting op basis van die bronnen.
        "slug": "bad-vervangen-door-douche",
        "kort": "Bad vervangen door douche",
        "omschrijving": "Wat het kost om een bad eruit te halen en er een douche voor in de plaats te zetten.",
        "h1": "Wat kost het om een bad te vervangen door een douche?",
        "title": f"Bad vervangen door douche: kosten {JAAR}",
        "description": "Een bad vervangen door een douche kost meestal €2.000 tot €6.000, inclusief sloop, tegelwerk en btw. Met prijzen per variant, een rekenvoorbeeld en tips.",
        "dienst": "inloopdouche-plaatsen",
        "van": 2000, "tot": 6000, "eenheid": "per douche op de plek van het bad, inclusief btw",
        "snel": "Een bad eruit en een douche erin kost meestal <strong>€2.000 tot €6.000</strong>, inclusief slopen, afvoer aanpassen, tegelwerk, de douche zelf en 21% btw. Een douchebak met een glazen wand op de plek van het bad zit aan de onderkant. Een inloopdouche met een betegelde vloer en nieuwe wandtegels zit aan de bovenkant. Moet de hele badkamer anders worden ingedeeld, dan kom je hoger uit.",
        "varianten": [
            ("Douchebak met wand op de plek van het bad", 1500, 3000, "Een lage douchebak en een glazen wand. Alleen de tegels rond het bad worden aangepast."),
            ("Inloopdouche met tegelvloer", 2500, 5000, "Douchevloer op afschot met een goot, waterdicht gemaakt en opnieuw betegeld."),
            ("Met nieuwe indeling of verplaatste afvoer", 4000, 8000, "De douche komt op een andere plek of de vloer moet omlaag. Vaak samen met meer tegelwerk."),
        ],
        "varianten_eenheid": "Per douche, inclusief materiaal, plaatsing en btw",
        "varianten_noot": "Eigen inschatting op basis van Homedeal (inloopdouche €430 – €4.000), Werkspot (inloopdouche €1.500 – €5.000) en Trustoo (losse posten). De bovenste rij kan lager uitvallen als de wandtegels kunnen blijven.",
        "factoren": [
            ("Wat er met de tegels gebeurt", "Onder en achter een bad zitten vaak geen tegels. Haal je het bad weg, dan moeten de vloer en de muur daar opnieuw worden betegeld. Zijn de oude tegels niet meer te krijgen, dan worden het al snel alle wanden."),
            ("Douchebak of inloopdouche", "Een douchebak is snel geplaatst. Een inloopdouche met een tegelvloer vraagt afschot, een goot en waterdicht maken, en kost dus meer."),
            ("De afvoer", "Een bad heeft een afvoer laag bij de vloer. Een douche heeft vaak meer afschot nodig. Ligt de afvoer niet goed, dan moet de vloer open of omhoog."),
            ("De kraan", "De badkraan zit vaak lager dan een douchekraan. De leidingen moeten dan omhoog in de muur, en die moet daarna weer dicht en betegeld."),
            ("De maat", "Een bad is meestal 170 of 180 cm lang. Daar past een ruime douche van 120 tot 160 cm met ruimte voor een plank of een nis."),
        ],
        "voorbeeld": (
            "Stel: je vervangt een inbouwbad van 170 × 75 cm door een inloopdouche van 160 × 80 cm met een douchegoot en een glazen wand. De douchevloer en de twee wanden in de douchehoek worden opnieuw betegeld (zo'n 7 m²).",
            [
                ("Bad, ombouw en tegels rond het bad slopen", (300, 600)),
                ("Afvoer van het bad en het puin", (100, 250)),
                ("Afvoer aanpassen en douchegoot plaatsen", (400, 800)),
                ("Kraanleidingen omhoog in de muur", (150, 400)),
                ("Douchevloer op afschot en waterdicht maken", rp("waterdicht")),
                ("Tegels en legloon, 7 m²", som(rp("tegels", 7), rp("tegelwerk", 7))),
                ("Glazen wand met montage", (400, 900)),
                ("Opbouwthermostaat met handdouche", (150, 400)),
                ("Kitwerk, 6 meter", rp("kitwerk", 6)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld. Het tegelwerk en de afvoer zijn samen het grootste deel. Kunnen de bestaande wandtegels blijven en kies je een lage douchebak, dan kom je lager uit.",
        ),
        "btw_extra": "",
        "besparen": [
            "Zet de douche op de plek van het bad. De afvoer ligt daar al, ook al moet hij soms iets worden aangepast.",
            "Kies een lage douchebak in plaats van een betegelde douchevloer.",
            "Vraag of de wandtegels kunnen blijven. Dan hoeft alleen de plek van het bad te worden betegeld.",
            "Een vaste glazen wand zonder deur is goedkoper en makkelijker schoon te houden.",
            "Heb je de douche nodig vanwege een beperking? Vraag dan vóór de start bij je gemeente of je in aanmerking komt voor steun via de Wmo.",
        ],
        "specialist": "Een bad weghalen kan een handige doe-het-zelver, maar een douche op die plek vraagt waterdicht werk. Onder een bad is de vloer vaak niet waterdicht gemaakt, terwijl dat onder een douche wel moet. Laat het afschot, de goot en het waterdicht maken door een badkamerspecialist doen. Woon je in een appartement, overleg dan ook met de VvE.",
        "faqs": [
            ("Is het slim om je bad weg te halen?", "Gebruik je het bad bijna nooit, dan geeft een ruime douche vaak meer gemak, zeker als je ouder wordt. Heb je jonge kinderen, dan is een bad juist handig. Lees ook <a href=\"/badkamerspullen/bad-of-douche/\">bad of douche</a>."),
            ("Hoe lang duurt het?", "Meestal drie tot vijf werkdagen, inclusief droogtijd van de vloer, de lijm en de voegen. Je kunt die dagen niet douchen in die badkamer."),
            ("Kan de douche precies op de plek van het bad?", "Meestal wel. Een bad van 170 cm is lang genoeg voor een ruime inloopdouche. Soms past er zelfs een nis of een plank bij."),
            ("Is een huis zonder bad minder waard?", "Daar is geen eenduidig antwoord op. Voor veel kopers is een goede douche belangrijker. Heb je een tweede badkamer of genoeg ruimte, dan kan een bad een plus zijn."),
        ],
        "bronnen": ["homedeal_douche", "werkspot_badkamer", "trustoo_badkamer", "werkspot_tegel", "btw"],
        "verwant": ["inloopdouche", "bad-plaatsen", "douchecabine-plaatsen"],
        "kennis": [("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel: kan dat bij jou?"),
                   ("/badkamerspullen/bad-of-douche/", "Bad of douche: wat past bij jou?")],
    },
    # ------------------------------------------------------------------
    {
        # Bronnen: Werkspot sanitair plaatsen (vrijstaand €200 – €500, hangend €250 – €600, dubbel €350 – €800,
        # spiegelkast €150 – €300), Slimster badkamermeubel (vanaf €150 / €750 / €1.500, excl. montage).
        "slug": "badkamermeubel-plaatsen",
        "kort": "Badkamermeubel plaatsen",
        "omschrijving": "Wat het ophangen en aansluiten van een wastafelmeubel kost, met of zonder meubel.",
        "h1": "Wat kost een badkamermeubel laten plaatsen?",
        "title": f"Badkamermeubel plaatsen kosten {JAAR}",
        "description": "Een badkamermeubel laten plaatsen kost €200 tot €600 aan montage, inclusief btw. Met prijzen voor een hangend, staand of dubbel meubel en een rekenvoorbeeld.",
        "dienst": "badkamer-installeren",
        "van": rp("montage_meubel")[0], "tot": rp("montage_meubel")[1], "eenheid": "per meubel, alleen montage, inclusief btw",
        "snel": f"Een wastafelmeubel laten ophangen en aansluiten kost meestal <strong>{eur(rp('montage_meubel')[0])} tot {eur(rp('montage_meubel')[1])}</strong> aan werk, inclusief 21% btw. Het meubel zelf komt erbij: van zo'n {eur(rp_niveau('sanitair_meubel', 'basis')[0])} voor een eenvoudig meubel tot {eur(rp_niveau('sanitair_meubel', 'luxe')[1])} of meer voor een groot of luxe meubel. Een dubbel meubel of een meubel op een nieuwe plek kost meer werk.",
        "varianten": [
            ("Staand meubel", 200, 500, "Meubel op pootjes of op de vloer, op de plek van het oude."),
            ("Hangend meubel", 250, 600, "Aan de muur, met stevige bevestiging. De muur moet het gewicht kunnen dragen."),
            ("Dubbel meubel", 350, 800, "Twee wastafels: meer aansluitingen en vaak een extra afvoer."),
            ("Spiegelkast ophangen", 150, 300, "Met aansluiten van de verlichting, als er al een aansluitpunt is."),
        ],
        "varianten_eenheid": "Alleen montage, inclusief btw",
        "varianten_noot": "Volgens Werkspot. Het meubel, de kraan en de spiegel komen erbij. Moeten de aansluitingen naar een andere plek, dan rekent de vakman ook het leidingwerk.",
        "factoren": [
            ("Het meubel zelf", f"Een eenvoudig meubel met wastafel kost {bedrag(*rp_niveau('sanitair_meubel', 'basis'))}, een gewoon meubel {bedrag(*rp_niveau('sanitair_meubel', 'midden'))} en een luxe of groot meubel {bedrag(*rp_niveau('sanitair_meubel', 'luxe'))}. Slimster noemt vanafprijzen van €150, €750 en €1.500."),
            ("Hangend of staand", "Een hangend meubel moet stevig in de muur. In een lichte wand zijn soms extra plaatjes of een frame nodig."),
            ("De aansluitingen", "Passen de afvoer en de kranen bij het nieuwe meubel, dan is het vooral ophangen en aansluiten. Zit de afvoer te hoog, te laag of te ver opzij, dan moet de muur open."),
            ("De breedte", "Een breed meubel of een dubbele wastafel vraagt meer werk en soms een tweede afvoer."),
            ("Spiegel en verlichting", "Een spiegel met verlichting of een spiegelkast heeft stroom nodig. Is er geen aansluitpunt, dan komt er een elektricien bij."),
            ("Het oude meubel", "Het oude meubel losmaken en afvoeren kost ook tijd. Vraag of dat in de prijs zit."),
        ],
        "voorbeeld": (
            "Stel: je vervangt een oud wastafelmeubel van 60 cm door een hangend meubel van 80 cm met een nieuwe kraan en een spiegel met verlichting. De afvoer en de kranen blijven op dezelfde plek.",
            [
                ("Oud meubel losmaken en afvoeren", (50, 150)),
                ("Wastafelmeubel 80 cm met kraan en spiegel (midden)", rp_niveau("sanitair_meubel", "midden")),
                ("Meubel ophangen en aansluiten", rp("montage_meubel")),
                ("Spiegelverlichting aansluiten", (75, 200)),
                ("Kitwerk langs de wastafel, 2 meter", rp("kitwerk", 2)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld, met dezelfde richtprijzen als de badkamercalculator. Zijn er tegels kapot gegaan achter het oude meubel, of moet de afvoer worden verlegd, dan komt dat erbij.",
        ),
        "btw_extra": "",
        "besparen": [
            "Kies een meubel dat past bij de afvoer en de kranen die er al zitten. Meet de hoogte van de afvoer voordat je koopt.",
            "Neem een meubel dat even breed of breder is dan het oude. Dan zie je geen gaten in het tegelwerk.",
            "Laat het meubel plaatsen samen met ander klein werk, zoals een nieuwe kraan of nieuwe kit.",
            "Haal het oude meubel zelf weg, als je weet hoe je het water afsluit.",
        ],
        "specialist": "Een staand meubel op dezelfde plek kan een handige doe-het-zelver plaatsen. Bij een hangend meubel moet je zeker weten dat de muur sterk genoeg is en dat je geen leidingen raakt bij het boren. Laat het doen door een loodgieter of badkamerspecialist als de afvoer moet worden verlegd, als het een dubbel meubel is of als er stroom voor de spiegel moet komen.",
        "faqs": [
            ("Hoe lang duurt het plaatsen van een badkamermeubel?", "Een meubel op dezelfde plek is vaak in twee tot vier uur geplaatst. Moet de afvoer worden verlegd of komt er een stopcontact bij, dan duurt het langer."),
            ("Kan een hangend meubel aan elke muur?", "Niet altijd. Aan een stenen muur gaat het meestal goed. Aan een lichte wand van gips of hout is extra versteviging nodig."),
            ("Moet de kraan apart worden betaald?", "Vaak wel. Bij veel meubels zit de kraan er niet bij. Vraag het na, en ook of de sifon en de afvoerplug erbij zitten."),
            ("Wat kost een badkamermeubel inclusief plaatsen?", f"Voor een gewoon meubel ben je samen zo'n {bedrag(*som(rp_niveau('sanitair_meubel', 'midden'), rp('montage_meubel')))} kwijt, volgens onze rekensom. Een eenvoudig meubel kan voor minder, een luxe of dubbel meubel kost meer."),
        ],
        "bronnen": ["werkspot_sanitair", "slimster_meubel", "trustoo_badkamer", "btw"],
        "verwant": ["uurtarief-loodgieter", "kitwerk-voegen", "nieuwe-badkamer"],
        "kennis": [("/badkamerspullen/wastafelmeubel-kiezen/", "Waar let je op bij een wastafelmeubel?"),
                   ("/badkamerspullen/kranen-kiezen/", "Waar let je op bij een nieuwe kraan?")],
    },
    # ------------------------------------------------------------------
    {
        # Bronnen: Homedeal nieuwe douche (douchecabine gemiddeld €1.800, €430 – €5.200 incl. montage en btw),
        # Slimster douche (cabine vanaf €300 / €800 / €1.500 excl. montage), Trustoo (cabine plaatsen
        # €275 – €435, verlaagde douchebak €300 – €550, bak of cabine demonteren vanaf €125).
        "slug": "douchecabine-plaatsen",
        "kort": "Douchecabine plaatsen",
        "omschrijving": "Wat een douchecabine met plaatsing kost, en wat alleen de montage kost.",
        "h1": "Wat kost een douchecabine laten plaatsen?",
        "title": f"Douchecabine plaatsen kosten {JAAR}: prijs en montage",
        "description": "Een douchecabine met plaatsing kost meestal €700 tot €2.500, inclusief btw. Alleen de montage kost €275 tot €450. Lees wat de prijs bepaalt en wat je kunt besparen.",
        "dienst": "inloopdouche-plaatsen",
        "van": 700, "tot": 2500, "eenheid": "per douchecabine met plaatsing, inclusief btw",
        "snel": "Een douchecabine laten plaatsen kost meestal <strong>€700 tot €2.500</strong>, inclusief de cabine, de montage en 21% btw. Homedeal noemt een gemiddelde van €1.800 en een spreiding van €430 tot €5.200. Heb je de cabine al en is de douchebak goed, dan kost alleen het monteren zo'n €275 tot €450.",
        "varianten": [
            ("Alleen cabine monteren", 275, 450, "Op een bestaande douchebak, met afkitten. De cabine heb je zelf gekocht."),
            ("Eenvoudige cabine met plaatsing", 700, 1300, "Standaardmaat 80 of 90 cm, op de bestaande bak of met een nieuwe lage bak."),
            ("Cabine met nieuwe lage douchebak", 1200, 2500, "Oude bak eruit, een verlaagde bak erin en een nieuwe cabine."),
            ("Luxe of maatwerk", 2500, 5200, "Dik glas, maatwerk of een cabine met extra functies."),
        ],
        "varianten_eenheid": "Inclusief btw",
        "varianten_noot": "Alleen monteren volgens Trustoo (€275 – €435). De bovengrens van €5.200 is van Homedeal. De rijen daartussen zijn een eigen inschatting op basis van Slimster (cabine vanaf €300, €800 of €1.500) en Trustoo.",
        "factoren": [
            ("De cabine", "Een eenvoudige kwartronde cabine van 80 of 90 cm is het goedkoopst. Dikker glas, een zwart profiel, een rechthoekige maat of maatwerk kost meer."),
            ("De douchebak", "Kan de oude bak blijven, dan gaat het snel. Een nieuwe verlaagde bak moet vaak in de vloer worden ingehakt en op de afvoer worden aangesloten."),
            ("Het tegelwerk", "De cabine komt tegen de tegels aan. Zijn de wanden niet recht of moeten er nieuwe tegels komen, dan moet dat eerst klaar zijn."),
            ("De kraan", "Een cabine met een kraan in het paneel is snel aangesloten. Een thermostaat in de muur vraagt meer werk."),
            ("Het oude werk", "De oude cabine en bak demonteren en afvoeren kost apart geld. Trustoo noemt vanaf €125."),
        ],
        "voorbeeld": (
            "Stel: je vervangt een oude douchecabine van 90 × 90 cm met een hoge bak door een nieuwe kwartronde cabine met een lage douchebak. De wandtegels blijven.",
            [
                ("Oude cabine en douchebak demonteren en afvoeren", (125, 250)),
                ("Nieuwe lage douchebak inhakken en aansluiten", (300, 550)),
                ("Douchebak 90 × 90 cm", (100, 400)),
                ("Kwartronde douchecabine 90 × 90 cm", (300, 800)),
                ("Cabine monteren", (275, 435)),
                ("Kitwerk, 6 meter", rp("kitwerk", 6)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld op basis van Trustoo, Slimster en Homedeal. Moeten er nieuwe tegels komen of verandert de kraan, dan komt dat erbij.",
        ),
        "btw_extra": "",
        "besparen": [
            "Laat de bestaande douchebak liggen als die nog goed is en de afvoer niet lekt.",
            "Kies een standaardmaat. Maatwerk glas is veel duurder.",
            "Haal de oude cabine zelf weg, als je het water hebt afgesloten.",
            "Vergelijk ook met een vaste glazen wand op een lage bak of een tegelvloer. Zie de kosten van een <a href=\"/kosten/inloopdouche/\">inloopdouche</a>.",
        ],
        "specialist": "Een cabine op een bestaande bak monteren kan een handige doe-het-zelver met de handleiding erbij. Het afkitten moet wel goed gebeuren, anders loopt er water achter de bak. Laat een nieuwe douchebak, een verlaagde bak of een aanpassing aan de afvoer door een loodgieter of badkamerspecialist doen. Zorg dat het tegelwerk klaar is voordat de cabine komt.",
        "faqs": [
            ("Is een douchecabine goedkoper dan een inloopdouche?", "Vaak wel, als de bestaande bak en tegels kunnen blijven. Een inloopdouche met een tegelvloer en een goot is meer werk. Een luxe cabine kan wel net zo duur zijn als een eenvoudige inloopdouche."),
            ("Hoe lang duurt het plaatsen van een douchecabine?", "Alleen een cabine monteren duurt een paar uur. Met een nieuwe douchebak ben je één tot twee dagen bezig, plus een dag om de kit te laten drogen."),
            ("Moet het tegelwerk eerst klaar zijn?", "Ja. De cabine wordt tegen de tegels gemonteerd en afgekit. Komen er nog nieuwe tegels, dan moeten die eerst gezet en gevoegd zijn."),
            ("Hoe houd ik een douchecabine schoon?", "Trek het glas na het douchen droog met een trekker. Dan blijft er minder kalk achter. Lees ook over <a href=\"/badkamerspullen/douchesysteem-kiezen/\">douchesystemen kiezen</a>."),
        ],
        "bronnen": ["homedeal_douche", "slimster_douche", "trustoo_badkamer", "btw"],
        "verwant": ["inloopdouche", "bad-vervangen-door-douche", "kitwerk-voegen"],
        "kennis": [("/badkamerspullen/inloopdouche-kopen/", "Waar let je op bij het kopen van een douche?"),
                   ("/badkamerspullen/douchesysteem-kiezen/", "Welk douchesysteem past bij jou?")],
    },
    # ------------------------------------------------------------------
    {
        # Bronnen: Homedeal zolder verbouwen (badkamer op zolder €20.000 – €35.000; dakisolatie binnen
        # €20 – €50 per m²; elektra €500 – €2.000; dakkapel €7.000 – €9.800), Slimster (€2.000 – €18.000),
        # Werkspot zolder verbouwen (tussenwand €600 – €1.000). Varianten zijn een eigen inschatting.
        "slug": "badkamer-op-zolder",
        "kort": "Badkamer op zolder",
        "omschrijving": "Wat een nieuwe badkamer op zolder kost, met leidingen, isolatie en ventilatie.",
        "h1": "Wat kost een badkamer op zolder?",
        "title": f"Badkamer op zolder kosten {JAAR}: richtprijzen",
        "description": "Een badkamer op zolder kost meestal €8.000 tot €35.000, inclusief btw. Lees wat leidingen, isolatie, ventilatie en een dakkapel kosten, met een rekenvoorbeeld.",
        "dienst": "badkamer-renoveren",
        "van": 8000, "tot": 35000, "eenheid": "per badkamer op zolder, inclusief btw",
        "snel": "Een badkamer op zolder kost meestal <strong>€8.000 tot €35.000</strong>, inclusief 21% btw. Homedeal noemt gemiddeld €20.000 tot €35.000, inclusief constructie, leidingen, ventilatie en sanitair. Liggen de leidingen dichtbij en hoeft er weinig verbouwd te worden, dan kan het voor minder. Komt er een dakkapel bij, dan kost die volgens Homedeal nog eens €7.000 tot €9.800.",
        "varianten": [
            ("Eenvoudig: leidingen dichtbij", 8000, 15000, "Douche, toilet en meubel in een deel van de zolder dat al stahoogte heeft. Weinig bouwkundig werk."),
            ("Gemiddeld: nieuwe wand, isolatie en ventilatie", 15000, 25000, "Een aparte ruimte met een tussenwand, extra isolatie, nieuwe leidingen en mechanische ventilatie."),
            ("Compleet, met constructief werk", 20000, 35000, "Inclusief vloer verstevigen, dakraam of andere aanpassingen aan het dak. Een dakkapel komt er nog bij."),
        ],
        "varianten_eenheid": "Per badkamer, inclusief btw",
        "varianten_noot": "De onderste rij volgt Homedeal (€20.000 – €35.000). De andere rijen zijn een eigen inschatting op basis van het rekenvoorbeeld hieronder; Slimster noemt een bandbreedte van €2.000 tot €18.000.",
        "factoren": [
            ("De afvoer", "Water en afvoer moeten van de zolder naar de standleiding. De afvoer heeft afschot nodig. Ligt de standleiding ver weg, dan moet de vloer omhoog of de leiding door een kast of een lagere verdieping. Een toiletpomp (vermaler) is soms een uitweg, maar maakt geluid en vraagt onderhoud."),
            ("Warm water", "Hoe verder de zolder van de cv-ketel of warmtepomp, hoe langer je op warm water wacht. Soms is een eigen boiler of een extra leiding nodig."),
            ("De vloer", "Een zoldervloer is vaak van hout. Een tegelvloer en zeker een bad zijn zwaar. Laat de draagkracht beoordelen; soms moet de vloer worden verstevigd."),
            ("Stahoogte en het schuine dak", "Onder een schuin dak is weinig plek om te staan. De douche hoort op de hoogste plek. Een dakraam of dakkapel geeft meer ruimte en licht, maar kost veel."),
            ("Isolatie en ventilatie", "Een warme, natte ruimte onder het dak moet goed geïsoleerd en geventileerd zijn. Anders krijg je condens en schimmel. Mechanische ventilatie met een afvoer naar buiten is eigenlijk altijd nodig."),
            ("Vergunning", "Een badkamer binnen de bestaande zolder heeft meestal geen vergunning nodig. Een dakkapel aan de voorkant of een nokverhoging meestal wel. Vraag het na bij je gemeente."),
        ],
        "voorbeeld": (
            "Stel: je maakt op de zolder van een tussenwoning een badkamer van 2,5 × 2,5 meter tegen de achtergevel, met een douche, een hangtoilet en een wastafelmeubel. Er komt een tussenwand met deur. De standleiding ligt een paar meter verderop.",
            [
                ("Tussenwand met deur", (600, 1000)),
                ("Extra dakisolatie, 10 m² × €20 – €50", (200, 500)),
                ("Vloer vlak en geschikt maken voor tegels", (500, 1500)),
                ("Leidingwerk in de badkamer", rp("leidingwerk")),
                ("Nieuwe aanvoer en afvoer naar de zolder", rp("leidingwerk_verplaatsen")),
                ("Elektra: groep, stopcontacten en spots", rp("elektra")),
                ("Ventilator met afvoer door het dak", (300, 800)),
                ("Tegels en legloon, 20 m²", som(rp("tegels", 20), rp("tegelwerk", 20))),
                ("Waterdicht maken van de douchehoek", rp("waterdicht")),
                ("Sanitair (midden): douche, hangtoilet, wastafelmeubel", som(*(rp_niveau("sanitair_" + x, "midden") for x in ("douche", "toilet", "meubel")))),
                ("Montage van douche, toilet en meubel", som(rp("montage_douche"), rp("montage_toilet"), rp("montage_meubel"))),
                ("Kitwerk en afwerking", rp("kitwerk_badkamer")),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld zonder dakraam, dakkapel, verwarming of stucwerk. De posten voor leidingwerk, tegels en sanitair zijn dezelfde richtprijzen als in de badkamercalculator. Moet de vloer worden verstevigd of komt er een dakkapel bij, dan zit je eerder in de bandbreedte van Homedeal.",
        ),
        "btw_extra": "Op een zolder kan een deel van het werk wel onder 9% vallen als de woning ouder is dan twee jaar: het arbeidsloon voor isolatie en het stukadoren of verven van wanden en plafond. Het bedrijf hoort die posten dan apart op de offerte te zetten.",
        "besparen": [
            "Zet de badkamer zo dicht mogelijk boven de bestaande badkamer of de standleiding. Dat scheelt veel leidingwerk.",
            "Plaats de douche op de hoogste plek en het toilet of de wastafel onder het schuine dak.",
            "Kies een douche in plaats van een bad. Dat scheelt gewicht, ruimte en vaak het verstevigen van de vloer.",
            "Laat isolatie en ventilatie in één keer goed doen. Vochtschade achteraf is veel duurder.",
            "Vraag offertes waarin elke post apart staat, zodat je ziet wat de verbouwing kost en wat de badkamer.",
        ],
        "specialist": "Een badkamer op zolder is werk voor een badkamerspecialist of aannemer die ook het bouwkundige deel kan doen of aansturen. Er komen veel vakken bij elkaar: loodgieter, elektricien, tegelzetter en soms een timmerman of constructeur. Laat vooraf de vloer, de afvoer en de ventilatie beoordelen. Woon je in een appartement, overleg dan met de VvE.",
        "faqs": [
            ("Heb ik een vergunning nodig voor een badkamer op zolder?", "Meestal niet, zolang je binnen de bestaande zolder blijft en niets aan de constructie of het dak verandert. Een dakkapel aan de voorkant of een nokverhoging heeft meestal wel een vergunning nodig. Check het bij je gemeente."),
            ("Kan een badkamer op elke zolder?", "Niet altijd. Er moet genoeg stahoogte zijn, de vloer moet sterk genoeg zijn en de afvoer moet naar de standleiding kunnen. Een specialist kan dat bij een bezoek beoordelen."),
            ("Hoe lang duurt het?", "Reken op twee tot vier weken voor de badkamer zelf. Met isolatie, een tussenwand of een dakraam erbij duurt het langer."),
            ("Wat als de afvoer niet onder afschot kan?", "Dan kan de vloer omhoog, kan de leiding een andere route krijgen of kan een toiletpomp een oplossing zijn. Een pomp maakt geluid en heeft onderhoud nodig. Bespreek de mogelijkheden met de specialist."),
        ],
        "bronnen": ["homedeal_zolder", "slimster_zolder", "werkspot_zolder", "trustoo_badkamer", "slimster_badkamer", "btw"],
        "verwant": ["nieuwe-badkamer", "toilet-verplaatsen", "vloerverwarming-badkamer"],
        "kennis": [("/kennisbank/badkamer-op-zolder/", "Een badkamer op zolder: waar let je op?"),
                   ("/kennisbank/badkamer-ventilatie/", "Ventilatie in de badkamer")],
    },
    # ------------------------------------------------------------------
    {
        # Bronnen: Homedeal toilet verbouwen (leidingen verplaatsen gemiddeld €700 – €1.500 extra; hangtoilet
        # met inbouwreservoir €400 – €1.200 excl. montage), Werkspot toiletruimte verbouwen (toilet of afvoer
        # verplaatsen €700 – €1.500, kleine leidingaanpassing €300 – €600).
        "slug": "toilet-verplaatsen",
        "kort": "Toilet verplaatsen",
        "omschrijving": "Wat het verleggen van de afvoer en de waterleiding voor een toilet kost.",
        "h1": "Wat kost een toilet verplaatsen?",
        "title": f"Toilet verplaatsen kosten {JAAR}: afvoer verleggen",
        "description": "Een toilet verplaatsen kost meestal €700 tot €1.500 extra aan leidingwerk, inclusief btw. Lees wat het verschil maakt en wat het in totaal kost met nieuw tegelwerk.",
        "dienst": "toilet-renoveren",
        "van": rp("leidingwerk_toilet_verplaatsen")[0], "tot": rp("leidingwerk_toilet_verplaatsen")[1], "eenheid": "extra aan leidingwerk, inclusief btw",
        "snel": f"Een toilet naar een andere plek verplaatsen kost meestal <strong>{eur(rp('leidingwerk_toilet_verplaatsen')[0])} tot {eur(rp('leidingwerk_toilet_verplaatsen')[1])} extra</strong> aan leidingwerk, inclusief 21% btw. Daar komen het toilet, de montage en het herstellen van de vloer en de tegels bij. Een kleine verschuiving op dezelfde wand kost zo'n €300 tot €600. Moet de afvoer door een andere ruimte of de vloer helemaal open, dan wordt het duurder.",
        "varianten": [
            ("Kleine verschuiving", 300, 600, "Een stukje opzij op dezelfde wand. De afvoer hoeft nauwelijks om."),
            ("Toilet verplaatsen in dezelfde ruimte", *rp("leidingwerk_toilet_verplaatsen"), "Afvoer en waterleiding naar een andere wand, vloer of muur open."),
            ("Naar een andere ruimte", 1500, 3500, "Een nieuwe route naar de standleiding, vaak door vloer of muur. Eigen inschatting."),
        ],
        "varianten_eenheid": "Alleen het leidingwerk, inclusief btw",
        "varianten_noot": "De eerste twee rijen volgen Werkspot en Homedeal. De onderste rij is een eigen inschatting. Het toilet, de montage en het tegelwerk komen er nog bij.",
        "factoren": [
            ("De afstand tot de standleiding", "Een toiletafvoer is dik en moet onder afschot naar de standleiding lopen. Hoe verder weg, hoe meer hoogte je nodig hebt en hoe meer de vloer open moet."),
            ("De vloer", "In een houten vloer kan de leiding vaak tussen de balken. In een betonvloer moet er worden gehakt of gefreesd, of moet de vloer omhoog."),
            ("Staand of hangend toilet", "Bij een hangtoilet komt de afvoer uit de muur. Met een voorzetwand kun je de leidingen daarachter wegwerken. Dat maakt verplaatsen soms makkelijker."),
            ("Tegels en afwerking", "Waar de leiding komt, moeten de vloer en de muur weer dicht en opnieuw worden betegeld. Zijn de oude tegels niet meer te krijgen, dan wordt het meer tegelwerk."),
            ("Appartement of eengezinswoning", "In een appartement ligt de standleiding vast en loopt die door het gebouw. Verplaatsen kan dan beperkt zijn en de VvE moet soms toestemming geven."),
        ],
        "voorbeeld": (
            "Stel: in je badkamer gaat een staand toilet een meter opzij naar de andere wand, en het wordt een hangtoilet met een voorzetwand. De vloer gaat daarvoor deels open en wordt daarna opnieuw betegeld (zo'n 4 m²).",
            [
                ("Vloer openmaken en afvoer en waterleiding verleggen", rp("leidingwerk_toilet_verplaatsen")),
                ("Inbouwreservoir met frame en voorzetwand", (400, 900)),
                ("Hangtoilet met zitting (midden)", rp_niveau("sanitair_toilet", "midden")),
                ("Toilet plaatsen en aansluiten", rp("montage_toilet")),
                ("Tegels en legloon vloer en voorzetwand, 4 m²", som(rp("tegels", 4), rp("tegelwerk", 4))),
                ("Kitwerk, 3 meter", rp("kitwerk", 3)),
                ("Totaal, inclusief btw", TOTAAL),
            ],
            "Dit is een eigen rekenvoorbeeld met dezelfde richtprijzen als de badkamercalculator. Gaat het toilet naar een andere ruimte of moet de hele vloer opnieuw betegeld worden, dan kom je hoger uit.",
        ),
        "btw_extra": "",
        "besparen": [
            "Laat het toilet staan als het kan. Verplaatsen is vooral leidingwerk en tegelwerk, en dat zie je niet terug.",
            "Een kleine verschuiving op dezelfde wand is veel goedkoper dan naar een andere wand.",
            "Combineer het verplaatsen met een complete renovatie. Dan gaan de tegels toch al opnieuw.",
            "Vraag of een voorzetwand de leidingen kan verbergen, zodat de vloer minder open hoeft.",
        ],
        "specialist": "Een toilet verplaatsen is werk voor een loodgieter of badkamerspecialist. De afvoer moet goed onder afschot liggen en luchtdicht aansluiten, anders krijg je verstoppingen of stank. Woon je in een appartement, overleg dan eerst met de VvE over de standleiding.",
        "faqs": [
            ("Kan een toilet overal worden geplaatst?", "Niet overal. De afvoer moet onder afschot naar de standleiding kunnen. Is dat niet mogelijk, dan kan een toiletpomp een uitweg zijn, maar die maakt geluid en heeft onderhoud nodig."),
            ("Hoe lang duurt het verplaatsen van een toilet?", "Het leidingwerk is vaak in één tot twee dagen klaar. Met een voorzetwand, nieuwe tegels en droogtijd ben je meestal drie tot vijf werkdagen bezig."),
            ("Is een hangtoilet makkelijker te verplaatsen?", "Soms. Met een voorzetwand kunnen de leidingen erachter lopen. De afvoer moet wel nog steeds op de goede hoogte uitkomen."),
            ("Mag ik in een appartement mijn toilet verplaatsen?", "Dat hangt af van de regels van de VvE en van waar de standleiding loopt. Vraag het eerst na. Lees ook <a href=\"/kennisbank/verbouwen-in-vve/\">verbouwen in een VvE</a>."),
        ],
        "bronnen": ["homedeal_toilet", "werkspot_toilet", "werkspot_tegel", "btw"],
        "verwant": ["toilet-renoveren", "uurtarief-loodgieter", "badkamer-op-zolder"],
        "kennis": [("/badkamerspullen/toilet-kiezen/", "Welk toilet past bij jou?"),
                   ("/kennisbank/verbouwen-in-vve/", "Verbouwen in een VvE: waar let je op?")],
    },
]

from badkamer_kosten3 import KOSTEN3, B3
B.update(B3)
KOSTEN += KOSTEN3

# Ronde 5: verdieping van de vijf belangrijkste kostenpagina's (EXTRA) en nieuwe pagina's (KOSTEN4).
from badkamer_kosten4 import KOSTEN4, B4, EXTRA
B.update(B4)
for _k in KOSTEN:
    _x = EXTRA.get(_k["slug"])
    if _x:
        _x = dict(_x)
        _k["faqs"] = list(_k["faqs"]) + list(_x.pop("faqs_extra", []))
        _k.update(_x)
KOSTEN += KOSTEN4

KOSTEN_BY_SLUG = {k["slug"]: k for k in KOSTEN}

LINKS = [("/kosten/", "Kosten badkamerwerk", "Richtprijzen voor een nieuwe badkamer, inloopdouche, bad, tegelwerk en meer.")] + [
    (f"/kosten/{k['slug']}/", k["kort"], k["omschrijving"]) for k in KOSTEN
]


# ---------------------------------------------------------------------------
# Opmaak
# ---------------------------------------------------------------------------

STYLE = """<style>
.kc-snel{display:flex;gap:16px;align-items:flex-start;background:var(--bg-soft);border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:var(--radius);padding:18px 20px;margin:18px 0 8px}
.kc-snel .kc-ico{flex:0 0 auto;color:var(--navy);margin-top:2px}
.kc-snel p{margin:0}
.kc-snel .kc-kop{font-size:.78rem;font-weight:750;letter-spacing:.04em;text-transform:uppercase;color:var(--accent-dark);margin-bottom:4px}
.kc-snel .kc-bedrag{font-size:1.5rem;font-weight:800;color:var(--ink);line-height:1.2;margin-bottom:6px}
.kc-snel .kc-bedrag span{font-size:.95rem;font-weight:600;color:var(--muted)}
.kc-factoren{list-style:none;padding:0;margin:0}
.kc-factoren li{padding:12px 0;border-bottom:1px solid var(--line)}
.kc-factoren li:last-child{border-bottom:0}
.kc-factoren strong{display:block;color:var(--ink)}
.kc-tips{list-style:none;padding:0}
.kc-tips li{position:relative;padding-left:30px}
.kc-tips li svg{position:absolute;left:0;top:2px;color:var(--green)}
.kc-links{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));margin:14px 0}
.kc-links a{display:block;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;background:#fff;font-weight:650}
.kc-links a small{display:block;font-weight:400;color:var(--muted);margin-top:2px}
.kc-bronnen{font-size:.88rem;color:var(--muted)}
.kc-bronnen li{margin-bottom:.3em}
.kc-grid .card h3{display:flex;gap:10px;align-items:center}
.kc-grid .card .price{margin-top:4px}
@media (max-width:600px){.kc-snel{flex-direction:column;gap:8px}.kc-snel .kc-bedrag{font-size:1.3rem}}
@media (max-width:600px){.kc-opb table{min-width:0}.kc-opb thead{display:none}.kc-opb table,.kc-opb tbody,.kc-opb tr,.kc-opb td{display:block;width:auto}.kc-opb tr{padding:10px 0;border-bottom:1px solid var(--line)}.kc-opb tr:last-child{border-bottom:0}.kc-opb td{padding:2px 14px;border:0;text-align:left}}
</style>"""


def voorbeeld_rijen(rijen):
    """Rijen van een rekenvoorbeeld. Een waarde (laag, hoog) wordt opgemaakt en opgeteld;
    een rij met waarde TOTAAL krijgt de som. Tekst blijft tekst."""
    uit, lo, hi = [], 0, 0
    for label, waarde in rijen:
        if waarde is TOTAAL:
            uit.append((f"<strong>{label}</strong>", f"<strong>{bedrag(lo, hi)}</strong>"))
        elif isinstance(waarde, tuple):
            lo += waarde[0]
            hi += waarde[1]
            uit.append((label, bedrag(*waarde)))
        else:
            uit.append((label, waarde))
    return uit


def bronnen_html(sleutels):
    li = "".join(f'<li><a href="{B[s][1]}" rel="nofollow noopener">{B[s][0]}</a></li>' for s in sleutels)
    return (f'<h2>Bronnen</h2><p class="kc-bronnen">De richtprijzen op deze pagina zijn gebaseerd op deze bronnen, '
            f'geraadpleegd in november {JAAR}. Rekenvoorbeelden en bedragen die we zelf hebben afgeleid, staan als eigen '
            f'inschatting aangegeven.</p><ul class="kc-bronnen">{li}</ul>')


def bron_kort(sleutel):
    """Link naar een bron uit B of richtprijzen.BRONNEN."""
    naam, url = B.get(sleutel) or RP.BRONNEN[sleutel]
    if not url:
        return naam.lower()
    return f'<a href="{url}" rel="nofollow noopener">{naam.split(",")[0]}</a>'


def opbouw_html(rijen):
    """Prijsopbouw per post. Rij: (post, waarde, toelichting, bronnen).
    waarde is een sleutel uit richtprijzen.py (bedrag, eenheid en bronnen komen dan daaruit)
    of een tuple (laag, hoog, eenheidstekst); bronnen is dan een lijst sleutels."""
    uit = []
    for post, waarde, uitleg, bronnen in rijen:
        if isinstance(waarde, str):
            p = RP.RICHTPRIJZEN[waarde]
            bedr = f"{bedrag(*rp(waarde))} {RP.EENHEID_TEKST[p['eenheid']]}" + (" excl. btw" if p["btw"] == "excl" else "")
            bronnen = bronnen or p["bron"]
        else:
            bedr = f"{bedrag(waarde[0], waarde[1])} {waarde[2]}".strip()
        gezien, delen = set(), []
        for b in bronnen:
            naam = (B.get(b) or RP.BRONNEN[b])[0].split(",")[0]
            if b != "eigen" and naam not in gezien:
                gezien.add(naam)
                delen.append(bron_kort(b))
        links = ", ".join(delen)
        if "eigen" in bronnen:
            links = (links + ", " if links else "") + "eigen inschatting"
        uit.append((f"<strong>{post}</strong>", bedr, f"{uitleg} <small>Bron: {links}.</small>"))
    return f'<div class="kc-opb">{tabel(["Post", "Richtprijs", "Wat zit erin"], uit)}</div>'


def extra_secties(k):
    """De verdiepende blokken van ronde 5. Geeft (opbouw, voorbeelden, spijt, valkuilen) als HTML."""
    opb = ""
    if k.get("opbouw"):
        intro = k.get("opbouw_intro", "")
        opb = (f'<h2>Prijsopbouw per post</h2><p>{intro}</p>{opbouw_html(k["opbouw"])}'
               f'<p><small>Bedragen per post komen uit dezelfde richtprijzen als de <a href="{CALC}">badkamercalculator</a> '
               f'en de <a href="/tools/offertechecker/">offertechecker</a>, inclusief 21% btw tenzij anders vermeld. Peildatum november {JAAR}.</small></p>')
    vb = ""
    for titel, intro, rijen, slot in k.get("voorbeelden", []):
        vb += f"<h3>{titel}</h3><p>{intro}</p>{tabel(['Post', 'Richtprijs'], voorbeeld_rijen(rijen))}<p><small>{slot}</small></p>"
    spijt = ""
    if k.get("spijt"):
        wel = "".join(f"<li>{icon('check', 20)}<strong>{a}</strong> {b}</li>" for a, b in k["spijt"]["wel"])
        niet = "".join(f"<li><strong>{a}</strong> {b}</li>" for a, b in k["spijt"]["niet"])
        spijt = (f"<h2>Besparen zonder spijt</h2><p>{k['spijt'].get('intro', '')}</p>"
                 f"<h3>Hier kun je veilig op besparen</h3><ul class=\"kc-tips\">{wel}</ul>"
                 f"<h3>Hier bespaar je beter niet op</h3><ul class=\"kc-factoren\">{niet}</ul>")
    val = ""
    if k.get("valkuilen"):
        li = "".join(f"<li><strong>{a}</strong>{b}</li>" for a, b in k["valkuilen"])
        val = (f"<h2>Valkuilen in offertes</h2><p>Een lage totaalprijs zegt weinig als er posten ontbreken. Let bij "
               f"{k['kort'].lower()} vooral hierop:</p><ul class=\"kc-factoren\">{li}</ul>"
               f"<p>Heb je een offerte? Zet hem in de <a href=\"/tools/offertechecker/\">offertechecker</a>: die legt elke regel "
               f"naast deze richtprijzen en laat zien wat ontbreekt of vaag is.</p>")
    return opb, vb, spijt, val


def kosten_body(k):
    d = DIENST_BY_SLUG[k["dienst"]]
    cr, cr_ld = crumbs([("Home", "/"), ("Kosten", "/kosten/"), (k["kort"], None)])

    # Balken alleen als alle varianten dezelfde eenheid hebben; anders alleen de tabel met een noot.
    if k.get("balken", True):
        varianten = prijs_balken([(lbl, v, t) for lbl, v, t, _ in k["varianten"]], k["varianten_eenheid"], k["varianten_noot"])
    else:
        varianten = f'<p><small>{k["varianten_eenheid"]}. {k["varianten_noot"]}</small></p>'
    var_tabel = '<div class="kc-opb">' + tabel(["Variant", "Richtprijs", "Wat je krijgt"],
                      [(f"<strong>{lbl}</strong>", bedrag(v, t), uitleg) for lbl, v, t, uitleg in k["varianten"]]) + '</div>'
    factoren = "".join(f"<li><strong>{kop}</strong>{tekst}</li>" for kop, tekst in k["factoren"])
    intro, rijen, slot = k["voorbeeld"]
    voorbeeld = tabel(["Post", "Richtprijs"], voorbeeld_rijen(rijen))
    tips = "".join(f"<li>{icon('check', 20)}{t}</li>" for t in k["besparen"])
    verwant = "".join(
        f'<a href="/kosten/{s}/">{KOSTEN_BY_SLUG[s]["kort"]}<small>{KOSTEN_BY_SLUG[s]["omschrijving"]}</small></a>'
        for s in k["verwant"])
    kennis = "".join(f'<li><a href="{p}">{t}</a></li>' for p, t in k["kennis"])
    faq_html, faq_ld = faq_blok(k["faqs"], f"Veelgestelde vragen over {k['kort'].lower()}")
    x_opbouw, x_voorbeelden, x_spijt, x_valkuilen = extra_secties(k)
    vb_kop = "Rekenvoorbeelden" if x_voorbeelden else "Rekenvoorbeeld"
    tips_kop = "Meer tips om te besparen" if x_spijt else "Tips om te besparen"

    eenheid_kort = k["eenheid"]
    body = f"""{STYLE}{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Richtprijzen bijgewerkt {MAAND}</span>
  <h1>{k['h1']}</h1>
  <div class="kc-snel" role="note" aria-label="Snel antwoord">
    <span class="kc-ico">{dienst_icoon(k['dienst'], 40)}</span>
    <div>
      <p class="kc-kop">Snel antwoord</p>
      <p class="kc-bedrag">{bedrag(k['van'], k['tot'])} <span>{eenheid_kort}</span></p>
      <p>{k['snel']}</p>
    </div>
  </div>
  <p><small>Alle bedragen zijn richtprijzen. Je echte prijs hangt af van jouw badkamer en hoor je pas na een bezoek van een specialist.</small></p>

  <h2>Prijzen per variant</h2>
  {varianten}
  {var_tabel}
  {x_opbouw}

  <h2>Wat bepaalt de prijs?</h2>
  <ul class="kc-factoren">{factoren}</ul>

  <h2>{vb_kop}</h2>
  {"<h3>" + k["voorbeeld_titel"] + "</h3>" if k.get("voorbeeld_titel") else ""}
  <p>{intro}</p>
  {voorbeeld}
  <p>{slot}</p>
  {x_voorbeelden}
  <p>Wil je een schatting voor je eigen badkamer? Gebruik de <a href="{CALC}">badkamercalculator</a>.</p>

  {cta_midden("Weet wat het bij jou kost", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit jouw regio en vergelijk ze rustig.")}
  {offertecheck_blok(k['kort'].lower())}

  <h2>Welke btw betaal je?</h2>
  <p>{BTW_BASIS} {k['btw_extra']}</p>

  {x_valkuilen}
  {x_spijt}
  <h2>{tips_kop}</h2>
  <ul class="kc-tips">{tips}</ul>

  <h2>Wanneer heb je een specialist nodig?</h2>
  <p>{k['specialist']}</p>
  <p>Meer over dit werk lees je op de pagina <a href="/diensten/{d['slug']}/">{d['naam'].lower()}</a>. Heb je al een offerte? Leg hem naast de <a href="/tools/offertechecker/">offertechecker</a>.</p>

  <h2>Verder lezen</h2>
  <ul>{kennis}<li><a href="/prijzen/">Alle badkamerprijzen op een rij</a></li></ul>
  <div class="kc-links">{verwant}</div>

  {bronnen_html(k['bronnen'])}
</div></section>
{faq_html}
{cta_blok(f"Offertes voor {k['kort'].lower()} vergelijken?", "Vul in een minuut het formulier in. Je krijgt vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio. Je kiest zelf of je met een van hen verder gaat.")}"""
    return body, [cr_ld, faq_ld]


def overzicht_body():
    cr, cr_ld = crumbs([("Home", "/"), ("Kosten", None)])
    kaarten = "".join(
        f'<a class="card reveal" href="/kosten/{k["slug"]}/">'
        f'<h3>{dienst_icoon(k["dienst"], 28)}{k["kort"]}</h3>'
        f'<p>{k["omschrijving"]}</p>'
        f'<div class="price">{bedrag(k["van"], k["tot"])} {k["eenheid"]}</div>'
        f'<p style="margin:10px 0 0"><span class="go">Bekijk de kosten →</span></p></a>'
        for k in KOSTEN)
    rijen = [(f'<a href="/kosten/{k["slug"]}/">{k["kort"]}</a>', bedrag(k["van"], k["tot"]), k["eenheid"]) for k in KOSTEN]
    faqs = [
        ("Waar komen deze prijzen vandaan?", "Uit openbare prijsoverzichten van onder meer Homedeal, Werkspot, Trustoo en Slimster, geraadpleegd in november " + str(JAAR) + ". Op elke pagina staan de bronnen. Rekenvoorbeelden zijn een eigen inschatting op basis van die bronnen."),
        ("Zijn de prijzen inclusief btw?", "Ja, tenzij er 'excl. btw' bij staat. Dat doen we bij het uurtarief van een loodgieter, omdat loodgieters hun tarief bijna altijd zonder btw noemen. Over badkamerwerk betaal je 21% btw."),
        ("Waarom zijn de bandbreedtes zo breed?", "Omdat geen badkamer hetzelfde is. De grootte, de staat van de oude badkamer, of de indeling verandert en welk sanitair je kiest, maken samen duizenden euro's verschil."),
        ("Hoe kom ik aan een echte prijs?", "Door een specialist naar je badkamer te laten kijken. Via Top Badkamers vraag je gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Wij voeren het werk zelf niet uit."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over badkamerkosten")
    body = f"""{STYLE}{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Richtprijzen {JAAR}</span>
  <h1>Kosten van badkamerwerk</h1>
  <p class="lead">Wat kost een nieuwe badkamer, een inloopdouche, een nieuw bad of een tegelzetter? Per klus vind je hier de richtprijs, een rekenvoorbeeld, de btw en tips om te besparen. Zo zie je snel of een offerte in de buurt zit.</p>
  <p>Alle bedragen zijn richtprijzen inclusief materiaal en 21% btw, tenzij er iets anders bij staat. Ze komen uit openbare prijsoverzichten; de bronnen staan op elke pagina. De kostenpagina's, de <a href="{CALC}">badkamercalculator</a> en de <a href="/tools/offertechecker/">offertechecker</a> rekenen met dezelfde richtprijzen per post, zoals sloopwerk, leidingwerk en tegelwerk.</p>
</div></section>
<section class="section-sm"><div class="wrap">
  <h2>Kies een klus</h2>
  <div class="grid g3 kc-grid">{kaarten}</div>
</div></section>
<section class="section-sm"><div class="wrap narrow prose">
  <h2>Alle bandbreedtes op een rij</h2>
  {tabel(["Klus", "Richtprijs", "Eenheid"], rijen)}
  <p><small>Richtprijzen, geen offerte. Je echte prijs hangt af van jouw situatie. Een overzicht per dienst vind je op <a href="/prijzen/">badkamerprijzen</a>.</small></p>

  <h2>Hoe gebruik je deze richtprijzen?</h2>
  <p>Een richtprijs gaat uit van een gewone klus. Je betaalt meer als er leidingen verplaatst moeten worden, als de vloer omlaag of omhoog moet, als er asbest zit of als je kiest voor luxe sanitair en grote tegels. Gebruik de bedragen dus om te zien of een offerte in de buurt zit, niet als vaste prijs.</p>
  <p>Leg offertes naast elkaar en kijk per offerte wat er in zit: sloopwerk, afvoer van puin, leidingwerk, elektra, waterdicht maken, sanitair (of een stelpost), btw en garantie. Ontbreekt er iets, dan is dat geen detail maar een latere meerprijs. De <a href="/tools/offertechecker/">offertechecker</a> helpt je daarbij.</p>
</div></section>
{faq_html}
{cta_blok("Benieuwd wat jouw badkamer kost?", "Richtprijzen zijn een begin. Een echte prijs krijg je als een specialist naar jouw badkamer kijkt. Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio.")}"""
    return body, [cr_ld, faq_ld]


def build(write):
    body, ld = overzicht_body()
    write("/kosten/", page(
        title(f"Kosten badkamerwerk {JAAR}: alle richtprijzen"),
        desc(f"Wat kost een nieuwe badkamer, inloopdouche, toilet of tegelzetter in {JAAR}?",
             "Richtprijzen per klus met rekenvoorbeeld, btw-uitleg en tips om te besparen.",
             limit=175),
        "/kosten/", body, ld), prio=0.8, freq="monthly")
    for k in KOSTEN:
        body, ld = kosten_body(k)
        write(f"/kosten/{k['slug']}/", page(title(k["title"]), k["description"],
                                             f"/kosten/{k['slug']}/", body, ld), prio=0.7, freq="monthly")
