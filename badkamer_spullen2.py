"""Badkamerspullen, deel 2: acht kopersgidsen op /badkamerspullen/<slug>/.

Zelfde soort pagina's als badkamer_spullen.py (zelfde CSS, tabellen en bronnenstijl), met per
gids extra onderdelen:
- een eenvoudige inline SVG met maten (goot, radiator, bad, frame, zones, wanden, fonteinen);
- een prijsklasse per soort, binnen de marktband van de offertevergelijker;
- uitleg hoe je het product op een offerte herkent (merk, serie, artikelnummer) met een
  voorbeeld van een goede en een vage offerteregel.

Prijzen: de banden komen uit producten_badkamer.PRODUCTDATA["categorieen"] (van, tot, bron),
dezelfde marktbanden die de offertevergelijker gebruikt. Peildatum november 2026. De prijzen
per soort zijn een verdeling binnen die band; de herkomst staat per gids als commentaar.
Alleen voor badkamerlampen is er geen categorie: die band staat hieronder met bron.

Wij verkopen niets en noemen geen winkels. Merknamen staan er niet in; op de offerte gaat het
om merk, serie en artikelnummer, wat dat ook is.

Interface: LINKS + build(write). De overzichtspagina /badkamerspullen/ wordt gebouwd door
badkamer_spullen.py; index_kaarten() levert de kaarten voor die pagina.
"""

import datetime

from components import page, title, crumbs, faq_blok, cta_blok, cta_midden, offertecheck_blok, prijs_balken, eur, icon
from producten_badkamer import PRODUCTDATA
import badkamer_spullen as BS

JAAR = datetime.date.today().year
BASIS = "/badkamerspullen/"
PEIL = "november 2026"
CAT = PRODUCTDATA["categorieen"]
PBRON = PRODUCTDATA["bronnen"]

# Eigen bronnen, aanvullend op PRODUCTDATA["bronnen"].
B2 = {
    # Badkamerlampen: geen categorie in de offertevergelijker. Band per armatuur uit het aanbod van
    # meerdere bouwmarkten en verlichtingswinkels (november 2026): IP44-plafonnières vanaf ongeveer
    # €16 tot €180, losse IP44-spots ongeveer €15 tot €80, spiegel- en wandlampen tot ongeveer €250.
    "aanbod_licht": ("Eigen vergelijking van het aanbod badkamerverlichting (IP44 en hoger) bij meerdere bouwmarkten en verlichtingswinkels, november 2026 (geen links)", None),
    "nen1010": ("NEN 1010: veiligheidsbepalingen voor elektrische installaties, deel over ruimten met bad of douche (zones 0, 1 en 2)", None),
    "mc_douchekop": ("Milieu Centraal: kluswijzer waterbesparende douchekop",
                     "https://www.milieucentraal.nl/media/q1bb4qtr/kluswijzer-waterbesparende-douchekop.pdf"),
    "mc_checklist": ("Milieu Centraal: verbouwingschecklist badkamer",
                     "https://www.milieucentraal.nl/media/dvaafvgn/verbouwingschecklist_badkamer_milieu-centraal.pdf"),
}


def _bron(k):
    if k in B2:
        return B2[k]
    v = PBRON[k]
    return v[0], v[1]


def band(sleutel):
    c = CAT[sleutel]
    return c["van"], c["tot"]


# ---------------------------------------------------------------------------
# Illustraties met maten (inline SVG, lijnen in currentColor)
# ---------------------------------------------------------------------------
_OPEN = ('<svg class="bs-svg b2-svg" viewBox="0 0 320 200" role="img" aria-label="{label}" fill="none" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">')
_T = 'stroke="none" fill="currentColor" font-size="11" font-family="inherit"'


def _t(x, y, s, anchor="middle", size=11):
    return f'<text x="{x}" y="{y}" {_T.replace("11", str(size))} text-anchor="{anchor}">{s}</text>'


def _maat(x1, x2, y, s):
    """Horizontale maatlijn met pijlpunten en tekst erboven."""
    return (f'<path class="b2-maat" d="M{x1} {y}H{x2}M{x1} {y-4}v8M{x2} {y-4}v8"/>'
            + _t((x1 + x2) / 2, y - 6, s, size=10))


def _vmaat(x, y1, y2, s, links=True):
    tx = x - 6 if links else x + 6
    return (f'<path class="b2-maat" d="M{x} {y1}V{y2}M{x-4} {y1}h8M{x-4} {y2}h8"/>'
            + _t(tx, (y1 + y2) / 2 + 4, s, "end" if links else "start", 10))


ILL2 = {
    # Douchegoot: bovenaanzicht van een douchevloer met goot langs de wand, plus doorsnede afschot
    "douchegoot-kiezen": (
        "Illustratie van een douchevloer met goot langs de wand en het afschot in doorsnede",
        '<rect x="20" y="24" width="150" height="120" rx="3"/>'
        '<rect class="bs-vlak" x="30" y="30" width="130" height="10" rx="2"/>'
        '<path class="bs-dun" d="M40 35h110"/>'
        '<path class="bs-dun" d="M60 120v-60M95 120v-60M130 120v-60"/><path class="bs-dun" d="M54 68l6-8 6 8M89 68l6-8 6 8M124 68l6-8 6 8"/>'
        + _maat(30, 160, 160, "goot 70 – 120 cm")
        + _t(95, 185, "Bovenaanzicht", size=10)
        + '<path d="M196 70h110"/><path class="bs-vlak" d="M200 70l96 -10v10z"/>'
        '<rect x="196" y="56" width="10" height="20" rx="1"/>'
        + _t(250, 50, "afschot ± 1 – 1,5 %", size=10)
        + '<path class="bs-dun" d="M196 76v44h110"/>'
        + _t(250, 100, "inbouwhoogte", size=10) + _t(250, 113, "6 – 11 cm", size=10)
        + _t(250, 150, "Doorsnede", size=10)),
    # Radiator: drie handdoekradiatoren in verschillende hoogtes naast een persoon-maat
    "badkamerradiator-kiezen": (
        "Illustratie van drie handdoekradiatoren van 80, 120 en 180 cm hoog",
        '<path d="M14 182h292"/>'
        + "".join(
            f'<rect x="{x}" y="{182-h}" width="44" height="{h}" rx="4"/>'
            + "".join(f'<path class="bs-dun" d="M{x+4} {y}h36"/>' for y in range(182 - h + 10, 182, 10))
            + _t(x + 22, 182 - h - 8, lab, size=10)
            for x, h, lab in ((40, 64, "80 cm"), (130, 96, "120 cm"), (220, 144, "180 cm")))
        + _t(62, 196, "toilet, klein", size=9) + _t(152, 196, "gemiddeld", size=9) + _t(242, 196, "hoofdverwarming", size=9)),
    # Spiegelkast: wastafelmeubel met spiegelkast erboven, breedtes en diepte
    "spiegelkast-kiezen": (
        "Illustratie van een spiegelkast boven een wastafelmeubel met breedte en diepte",
        '<path d="M10 190h200"/>'
        '<rect class="bs-glas" x="40" y="20" width="140" height="70" rx="3"/><path d="M110 20v70"/>'
        '<path class="bs-vlak" d="M44 92h132v4H44z"/>'
        '<rect x="34" y="120" width="152" height="12" rx="2"/><rect x="38" y="132" width="144" height="40" rx="3"/>'
        '<path d="M110 120v-10h12"/>'
        + _maat(40, 180, 16, "60 – 120 cm")
        + _vmaat(196, 90, 120, "20–30 cm", links=False)
        + '<rect x="262" y="20" width="16" height="70" rx="2"/><path d="M256 20v70" stroke-dasharray="4 4"/>'
        + _maat(262, 278, 106, "12–17 cm") + _t(268, 140, "opbouw", size=10)
        + '<rect x="290" y="20" width="10" height="70" rx="2" class="bs-vlak"/><path d="M300 20v70"/>'
        + _t(295, 160, "inbouw", size=10) + _t(295, 173, "± 10 cm", size=9) + _t(295, 185, "in de wand", size=9)),
    # Vrijstaand bad: bovenaanzicht met lengte, breedte en vrije ruimte rondom
    "vrijstaand-bad-kopen": (
        "Illustratie van een vrijstaand bad van bovenaf met lengte, breedte en vrije ruimte",
        '<path d="M20 20h280"/><path class="bs-dun" d="M20 14h280" stroke-dasharray="3 5"/>'
        '<rect x="40" y="50" width="200" height="90" rx="44"/><rect class="bs-vlak" x="52" y="60" width="176" height="70" rx="34"/>'
        '<circle cx="70" cy="95" r="4"/><rect x="22" y="88" width="10" height="14" rx="2"/>'
        + _maat(40, 240, 166, "lengte 150 – 190 cm")
        + _vmaat(252, 50, 140, "70–90 cm", links=False)
        + _vmaat(140, 20, 50, "≥ 15 cm", links=False)
        + _t(160, 192, "Wand boven; staande kraan of wandkraan bij het afvoereind", size=10)),
    # Inbouwreservoir: zijaanzicht voorzetwand met frame, bedieningsplaat en pot
    "inbouwreservoir-kiezen": (
        "Illustratie van een inbouwreservoir in een voorzetwand met de belangrijkste hoogtes",
        '<path d="M20 186h280"/><path d="M60 20v166"/>'
        '<rect class="bs-stippel" x="64" y="40" width="40" height="146" rx="2"/>'
        '<rect class="bs-vlak" x="70" y="52" width="28" height="44" rx="3"/>'
        '<path d="M108 40v146"/><rect x="108" y="78" width="6" height="22" rx="1"/>'
        '<path d="M108 120h80a24 24 0 0 1-24 24h-40"/><path d="M108 144h18l-4 16"/><path d="M108 120h86"/>'
        + _vmaat(48, 40, 186, "")
        + _t(230, 52, "frame ± 112 cm", "start", 10) + _t(230, 65, "(laag: ± 82 cm)", "start", 10)
        + _vmaat(210, 120, 186, "zit 40 – 48 cm", links=False)
        + _maat(60, 108, 30, "voorzetwand 15 – 25 cm")
        + _t(230, 90, "bedieningsplaat", "start", 10) + '<path class="bs-dun" d="M226 87h-108"/>'),
    # Badkamerlampen: zones rond een douche (zijaanzicht)
    "badkamerlampen-kiezen": (
        "Illustratie van de veiligheidszones 0, 1 en 2 rond een douche, gezien van opzij",
        '<path d="M20 180h280"/><path d="M20 20v160"/>'
        '<rect class="b2-zone1" x="20" y="38" width="110" height="138"/>'
        '<rect class="b2-zone2" x="130" y="38" width="60" height="138"/>'
        '<rect class="bs-vlak" x="20" y="172" width="110" height="8"/>'
        '<path d="M40 38v-10h30"/><path class="bs-dun" d="M74 44v14M84 44v18M94 44v14"/>'
        + _t(75, 120, "zone 1", size=12) + _t(160, 120, "zone 2", size=12) + _t(75, 168, "zone 0", size=9)
        + _vmaat(210, 38, 180, "225 cm", links=False)
        + _maat(130, 190, 198, "60 cm")
        + '<circle cx="250" cy="34" r="8" class="bs-vlak"/><path class="bs-dun" d="M250 44v10M242 50l-4 6M258 50l4 6"/>'
        + _t(266, 28, "buiten", "start", 9) + _t(266, 40, "de zones", "start", 9)),
    # Douchewand: vier opstellingen van bovenaf
    "douchewand-kiezen": (
        "Illustratie van vier douchewanden van bovenaf: vaste wand, nisdeur, hoekinstap en kwartrond",
        "".join(
            f'<g transform="translate({x} 24)"><path d="M0 0h60M0 0v60" stroke-width="3"/>{inh}</g>'
            + _t(x + 30, 112, lab, size=10) + _t(x + 30, 126, sub, size=9)
            for x, inh, lab, sub in (
                (10, '<path class="b2-glas-l" d="M40 0v46"/>', "vaste wand", "inloop"),
                (88, '<path d="M60 0v60" stroke-width="3"/><path class="b2-glas-l" d="M0 60h28"/><path class="b2-glas-l" d="M30 62h30" stroke-dasharray="5 3"/>', "nisdeur", "tussen 2 muren"),
                (166, '<path class="b2-glas-l" d="M60 0v34"/><path class="b2-glas-l" d="M0 60h34"/><path class="bs-dun" d="M60 34l-18 18M34 60l18-18"/>', "hoekinstap", "2 deuren"),
                (244, '<path class="b2-glas-l" d="M60 0a60 60 0 0 1-60 60"/>', "kwartrond", "cabine"),
            ))
        + _t(160, 160, "Dikke lijn: muur · blauwe lijn: glas", size=10)
        + _t(160, 180, "Gangbare hoogte 195 – 200 cm, glas 6 – 10 mm", size=10)),
    # Fontein: drie fonteinen van bovenaf in een toiletruimte van 90 cm breed
    "fontein-kiezen": (
        "Illustratie van drie fonteinformaten in een toiletruimte van 90 cm breed",
        '<path d="M20 30h280" stroke-width="3"/>'
        '<rect x="30" y="30" width="72" height="44" rx="6"/><ellipse class="bs-vlak" cx="66" cy="54" rx="24" ry="12"/>'
        + _maat(30, 102, 96, "± 36 × 25 cm") + _t(66, 116, "standaard", size=10)
        + '<rect x="126" y="30" width="80" height="34" rx="4"/><rect class="bs-vlak" x="136" y="38" width="60" height="18" rx="4"/>'
        + _maat(126, 206, 86, "± 40 × 18 cm") + _t(166, 116, "smal", size=10)
        + '<path d="M230 30h60v4a56 56 0 0 1-56 56h-4z" transform="translate(0 0)"/><path d="M290 30v60" stroke-width="3"/>'
        + _t(258, 116, "hoekfontein", size=10)
        + _maat(20, 300, 150, "toiletruimte vaak 80 – 90 cm breed")
        + _t(160, 180, "Hoe dieper de fontein, hoe minder beenruimte voor de pot", size=10)),
}


def illustratie2(slug, klein=False):
    label, inhoud = ILL2[slug]
    svg = _OPEN.format(label=label) + inhoud + "</svg>"
    if klein:
        return f'<div class="bs-ill bs-ill-klein" aria-hidden="true">{svg}</div>'
    return (f'<figure class="bs-ill">{svg}<figcaption>Illustratie: {label[len("Illustratie van "):]}. '
            'Maten zijn gangbare waarden, geen vaste norm.</figcaption></figure>')


# ---------------------------------------------------------------------------
# De gidsen
# ---------------------------------------------------------------------------
# Velden: slug, kort, kaart, h1, title, desc, lead, cat (sleutels in PRODUCTDATA["categorieen"]),
# soorten [(naam, goed, minder, van, tot)], maten [(kop, tekst)], letop [(kop, tekst)],
# valkuilen [..], offerte {"goed", "vaag", "let"}, faqs, bronnen, verder [(href, tekst)].

GIDSEN2 = [
    # Band douchegoot €50 – €700 (Werkspot: RVS-goot vaak vanaf €300; aanbod).
    {
        "slug": "douchegoot-kiezen",
        "kort": "Douchegoot kiezen",
        "kaart": "Goot of put, tegelgoot of wandgoot: welke lengte, hoeveel inbouwhoogte en wat kost hij?",
        "h1": "Douchegoot kiezen: soorten, maten en richtprijzen",
        "title": "Douchegoot kiezen: soorten, maten en prijzen",
        "desc": "Een douchegoot kiezen? Vergelijk doucheput, RVS-goot, tegelgoot en wandgoot. Met lengtes, inbouwhoogte, afvoercapaciteit en richtprijzen per soort (peil november 2026).",
        "lead": "Een douchegoot voert het water af langs één kant van de douche. Daardoor kan de vloer in één richting aflopen en kun je grote tegels gebruiken. De goot zelf is niet duur, maar een verkeerde keuze merk je jaren: een lekkende aansluiting of een goot die het water niet aankan.",
        "cat": ["douchegoot"],
        "soorten": [
            ("Doucheput (vierkant)", "Goedkoop, past in bijna elke vloer", "Afschot naar vier kanten, dus kleinere tegels", 50, 150),
            ("RVS-goot met rooster", "Makkelijk schoon, veel lengtes, standaard leverbaar", "Het rooster blijft zichtbaar", 150, 400),
            ("Tegelgoot (rooster in te tegelen)", "Bijna onzichtbaar, de vloer loopt door", "Zorgvuldig tegelwerk nodig, iets duurder", 200, 550),
            ("Wandgoot of goot in de wand", "Strak, geen rooster in de vloer", "Wand moet ervoor gebouwd worden, meer werk", 300, 700),
        ],
        "maten": [
            ("Lengte", "Gangbaar zijn 60, 70, 80, 90, 100 en 120 cm. Kies een goot die bijna de hele breedte van de douche beslaat, zodat het water niet om de goot heen loopt. Bij een douche van 90 cm breed past meestal een goot van 70 tot 80 cm."),
            ("Inbouwhoogte", "Dit is de ruimte die je onder de afgewerkte vloer nodig hebt voor goot en sifon. Standaardgoten vragen vaak 9 tot 11 cm, lage varianten ongeveer 6 tot 7 cm. In een appartement of op een houten verdiepingsvloer is die ruimte er niet altijd."),
            ("Afvoercapaciteit", "Fabrikanten noemen hoeveel liter per minuut de goot aankan. Een gewone douchekop geeft ongeveer 6 tot 12 liter per minuut, een grote regendouche al snel meer. Kies een goot die ruim boven je douche zit."),
            ("Afschot", "De vloer loopt naar de goot af, vaak ongeveer 1 tot 1,5 procent. Bij een douche van 1 meter diep is dat 1 tot 1,5 cm hoogteverschil."),
        ],
        "letop": [
            ("Afdichtflens of manchet", "De goot moet een brede rand hebben waarop de waterdichte laag aansluit. Hier ontstaan de meeste lekkages. Vraag welke afdichting er bij de goot hoort."),
            ("Uitneembaar sifon", "Haren en zeep komen in de goot terecht. Een sifon die je er zonder gereedschap uit haalt, maakt schoonmaken makkelijk."),
            ("Stankafsluiter", "Een goot zonder water in de sifon gaat ruiken. Sommige goten hebben een droge stankafsluiter. Handig bij een douche die je weinig gebruikt."),
            ("Rooster en afwerking", "Geborsteld RVS laat minder kalk zien dan glanzend. Zwarte of goudkleurige roosters kosten meer. Let op of het rooster los te koop is als het later beschadigt."),
        ],
        "valkuilen": [
            "Een goot kopen voordat bekend is hoeveel inbouwhoogte er is.",
            "Een korte goot in een brede douche: het water loopt dan langs de zijkant.",
            "Een regendouche combineren met een goot die het water niet aankan.",
            "Geen afspraak over de afdichting rond de goot in de offerte.",
        ],
        "offerte": {
            "goed": "Douchegoot RVS 80 cm, lage inbouw (70 mm), met tegelrooster en afdichtingsmanchet · merk · serie · art.nr.",
            "vaag": "Douchegoot leveren en plaatsen",
            "let": "Staan lengte, inbouwhoogte en het type rooster erbij? En staat de afdichting rond de goot als aparte regel of in de omschrijving van het tegelwerk?",
        },
        "faqs": [
            ("Is een douchegoot beter dan een doucheput?", "Niet per se. Een goot laat de vloer in één richting aflopen, zodat je grote tegels kunt leggen. Een put is goedkoper en werkt goed met kleinere tegels. De keuze hangt vooral af van je tegels en de ruimte onder de vloer."),
            ("Hoe lang moet een douchegoot zijn?", "Meestal net iets korter dan de breedte van de douche. Bij een douche van 90 cm past vaak een goot van 70 of 80 cm. Wil je dat de goot van muur tot muur loopt, dan heb je maatwerk of een goot op maat nodig."),
            ("Wat kost een douchegoot?", f"De goot zelf kost ongeveer {eur(50)} tot {eur(700)}, inclusief btw, zonder montage. Een eenvoudige doucheput zit onderaan, een wandgoot of maatwerk bovenaan. Inbouwen, afschot maken en waterdicht maken komen erbij."),
            ("Kan ik een douchegoot zelf plaatsen?", "Dat raden we alleen aan als je ervaring hebt met afschot en waterdicht maken. De aansluiting van de goot op de waterdichte laag is de plek waar het het vaakst misgaat."),
        ],
        "bronnen": ["werkspot_goot", "aanbod", "mc_douchekop"],
        "verder": [("/badkamerspullen/inloopdouche-kopen/", "Inloopdouche kopen"),
                   ("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Een badkamer waterdicht maken"),
                   ("/kosten/inloopdouche/", "Kosten van een inloopdouche")],
    },
    # Band badkamerradiator €50 – €1.200 (Slimster €50 – €800, gemiddeld €425; Werkspot €150 – €1.200).
    {
        "slug": "badkamerradiator-kiezen",
        "kort": "Badkamerradiator kiezen",
        "kaart": "Handdoekradiator, designradiator of elektrisch: hoeveel vermogen heb je nodig en wat kost het?",
        "h1": "Badkamerradiator kiezen: vermogen, maten en richtprijzen",
        "title": "Badkamerradiator kiezen: vermogen en prijzen",
        "desc": "Een badkamerradiator kiezen? Lees hoeveel vermogen je nodig hebt, welke hoogtes er zijn, wat werkt met een warmtepomp en wat een handdoek- of designradiator kost.",
        "lead": "In de badkamer wil je het warmer dan in de rest van het huis, vaak 22 tot 24 graden. Een badkamerradiator moet dus genoeg vermogen hebben, ook als er handdoeken over hangen. Hieronder lees je hoe je dat uitrekent en wat de soorten kosten.",
        "cat": ["badkamerradiator"],
        "soorten": [
            ("Elektrische handdoekradiator", "Geen cv-leidingen nodig, werkt ook in de zomer", "Stroomverbruik, eigen stopcontact of aansluiting nodig", 50, 600),
            ("Handdoekradiator op de cv", "Goedkoop in gebruik, veel maten", "Alleen warm als de cv aan staat", 100, 500),
            ("Gemengd (cv met verwarmingselement)", "Ook zonder cv warm voor droge handdoeken", "Duurder, extra aansluiting", 200, 800),
            ("Designradiator (plat, verticaal, kleur)", "Strak, ook als blikvanger", "Vaak minder vermogen per euro", 300, 1200),
        ],
        "maten": [
            ("Hoogte", "Gangbaar zijn ongeveer 80, 120, 160 en 180 cm. Een lage radiator past onder een raam of in een toiletruimte. Moet de radiator de badkamer alleen verwarmen, dan kom je vaak uit op 160 cm of hoger."),
            ("Breedte", "Meestal 50 of 60 cm. Een bredere radiator geeft meer vermogen bij dezelfde hoogte en meer ruimte voor handdoeken."),
            ("Vermogen", "Als vuistregel heb je in een badkamer 100 tot 150 watt per m² vloer nodig: de lage kant bij een goed geïsoleerd huis, de hoge kant bij een ouder huis. Een badkamer van 6 m² vraagt dan 600 tot 900 watt."),
            ("Watertemperatuur", "Het vermogen op de doos geldt vaak bij een watertemperatuur van 75 of 70 graden. Een warmtepomp werkt met 35 tot 55 graden. Dan geeft dezelfde radiator soms nog maar de helft of minder. Vraag naar het vermogen bij jouw temperatuur."),
        ],
        "letop": [
            ("Handdoeken dekken af", "Een handdoek over de radiator houdt een deel van de warmte tegen. Wil je de radiator als handdoekdroger gebruiken, reken dan wat ruimer, of kies vloerverwarming plus een kleine radiator."),
            ("Aansluiting", "Kijk waar de leidingen nu uit de muur of vloer komen. Een middenaansluiting met hart-op-hartmaat van vaak 50 mm is gangbaar. Een radiator met een andere aansluiting kan betekenen dat leidingen verlegd moeten worden."),
            ("Elektrisch in de badkamer", "Een elektrische radiator moet geschikt zijn voor de zone waar hij hangt (spatwaterdicht, IP-waarde). Er hoort een geaard stopcontact of vaste aansluiting buiten de natte zone bij. Laat dat door een installateur doen."),
            ("Kleur en afwerking", "Wit is het goedkoopst. Zwart, antraciet, RVS of goud kost vaak 20 tot 50 procent meer voor dezelfde maat."),
        ],
        "valkuilen": [
            "Kiezen op uiterlijk en pas daarna kijken naar het vermogen.",
            "Het vermogen bij 75 graden aanhouden terwijl je een warmtepomp hebt.",
            "Een elektrische radiator laten draaien als hoofdverwarming: dat kost veel stroom.",
            "Vergeten dat de oude aansluiting niet past bij de nieuwe radiator.",
        ],
        "offerte": {
            "goed": "Handdoekradiator 180 × 60 cm, middenaansluiting, 850 W bij 55/45/20 °C, wit · merk · serie · art.nr.",
            "vaag": "Designradiator badkamer, incl. montage",
            "let": "Staat het vermogen erbij, en bij welke watertemperatuur? Zit het aanpassen van de leidingen in de prijs, of komt dat er later bij?",
        },
        "faqs": [
            ("Hoeveel watt moet een badkamerradiator hebben?", "Reken als vuistregel 100 tot 150 watt per m² vloer. Bij een badkamer van 6 m² is dat 600 tot 900 watt. Kijk wel bij welke watertemperatuur dat vermogen geldt."),
            ("Werkt een badkamerradiator met een warmtepomp?", "Ja, maar hij geeft minder warmte omdat het water minder heet is. Kies een grotere radiator of combineer met vloerverwarming. Vraag het vermogen bij 45 of 55 graden op."),
            ("Wat kost een badkamerradiator?", f"De radiator zelf kost ongeveer {eur(50)} tot {eur(1200)}, inclusief btw, zonder montage. Een eenvoudige elektrische of witte cv-radiator zit onderaan, een designradiator in kleur bovenaan."),
            ("Is een elektrische handdoekradiator duur in gebruik?", "Dat hangt af van het vermogen en hoe lang hij aan staat. Een radiator van 500 watt die drie uur per dag aan staat, gebruikt ongeveer 1,5 kWh per dag. Een timer of thermostaat helpt."),
        ],
        "bronnen": ["slimster_radiator", "werkspot_radiator", "mc_checklist"],
        "verder": [("/kosten/vloerverwarming-badkamer/", "Kosten van vloerverwarming in de badkamer"),
                   ("/kennisbank/badkamer-ventilatie/", "Badkamer ventileren"),
                   ("/diensten/badkamer-installeren/", "Badkamer installeren")],
    },
    # Band spiegel_kast €40 – €900 (aanbod).
    {
        "slug": "spiegelkast-kiezen",
        "kort": "Spiegelkast kiezen",
        "kaart": "Spiegel, LED-spiegel of spiegelkast, opbouw of inbouw: maten, licht en richtprijzen.",
        "h1": "Spiegelkast kiezen: opbouw of inbouw, maten en richtprijzen",
        "title": "Spiegelkast kiezen: maten, licht en prijzen",
        "desc": "Spiegel of spiegelkast boven de wastafel? Vergelijk opbouw en inbouw, LED-verlichting en verwarming tegen beslaan. Met maten, valkuilen en richtprijzen per soort.",
        "lead": "Boven de wastafel hangt meestal een spiegel, een spiegel met licht of een spiegelkast met opbergruimte. De keuze hangt af van hoeveel spullen je kwijt wilt, hoe diep de kast mag zijn en of je een stopcontact nodig hebt.",
        "cat": ["spiegel_kast"],
        "soorten": [
            ("Spiegel zonder licht", "Goedkoop, dun, elke maat", "Geen opbergruimte, licht apart regelen", 40, 150),
            ("LED-spiegel", "Licht op gezichtshoogte, vaak met anti-beslag", "Elektra nodig, lamp niet altijd te vervangen", 80, 400),
            ("Spiegelkast opbouw", "Veel opbergruimte, makkelijk te plaatsen", "Steekt 12 tot 17 cm uit de muur", 100, 500),
            ("Spiegelkast inbouw of met verlichting en stopcontact", "Vlak in de wand, strak", "Wand moet dik genoeg zijn of erbij gebouwd worden", 300, 900),
        ],
        "maten": [
            ("Breedte", "Kies de spiegel even breed als het wastafelmeubel of iets smaller: gangbaar zijn 60, 80, 100 en 120 cm. Bij een dubbele wastafel zijn twee kleinere spiegels ook een optie."),
            ("Diepte", "Een opbouwkast is meestal 12 tot 17 cm diep. Bij een kleine badkamer stoot je daar sneller je hoofd aan. Een inbouwkast zit grotendeels in de wand en vraagt ongeveer 10 cm wanddiepte."),
            ("Hoogte", "Het midden van de spiegel hangt op ooghoogte, vaak rond 160 tot 170 cm vanaf de vloer. Tussen kraan en onderkant spiegel houd je 20 tot 30 cm vrij."),
            ("Licht", "Licht van voren of van de zijkanten geeft de minste schaduw op je gezicht. Een kleurtemperatuur van ongeveer 3000 tot 4000 kelvin is prettig voor scheren en make-up."),
        ],
        "letop": [
            ("Stroom en zone", "Een spiegel met licht of een stopcontact heeft een aansluiting nodig. Die moet geschikt zijn voor de plek ten opzichte van douche en bad. Laat de installateur bepalen waar de aansluiting komt, voordat er getegeld wordt."),
            ("Anti-beslag", "Een verwarmingsfolie achter de spiegel houdt hem helder na het douchen. Handig in een kleine badkamer met weinig ventilatie."),
            ("Kastdeuren", "Spiegeldeuren aan beide kanten (binnen en buiten) zijn handig om je achterhoofd te zien. Let op softclose-scharnieren en verstelbare planken."),
            ("Inbouw plannen", "Inbouw kan alleen als er een voorzetwand of holle wand is van voldoende dikte. Dat moet je vóór het tegelwerk regelen."),
        ],
        "valkuilen": [
            "Een spiegelkast die breder is dan het meubel: dat ziet er scheef uit.",
            "Pas na het tegelen bedenken dat er stroom nodig is.",
            "Een diepe opbouwkast boven een smalle wastafel waar je je hoofd aan stoot.",
            "Ledverlichting die niet te vervangen is: als die stuk gaat, moet de hele spiegel eruit.",
        ],
        "offerte": {
            "goed": "Spiegelkast opbouw 80 × 70 × 15 cm, 2 deuren, LED-verlichting en stopcontact · merk · serie · art.nr.",
            "vaag": "Spiegel(kast) passend bij meubel",
            "let": "Staat erbij of het opbouw of inbouw is, en of de aansluiting van de verlichting in de prijs zit? Een inbouwkast vraagt ook werk aan de wand.",
        },
        "faqs": [
            ("Hoe hoog hang je een spiegelkast?", "Het midden van de spiegel hangt meestal op ooghoogte, rond 160 tot 170 cm. Houd tussen kraan en onderkant 20 tot 30 cm vrij, zodat je de kraan goed kunt gebruiken."),
            ("Wat is beter, opbouw of inbouw?", "Opbouw is goedkoper en makkelijk te plaatsen. Inbouw is strakker en steekt niet uit, maar kan alleen als de wand dik genoeg is. Meestal wordt daarvoor een voorzetwand gebouwd."),
            ("Wat kost een spiegelkast?", f"Spiegels en spiegelkasten kosten ongeveer {eur(40)} tot {eur(900)}, inclusief btw, zonder montage. Een gewone spiegel zit onderaan, een inbouwkast met verlichting en stopcontact bovenaan."),
            ("Mag een stopcontact in een spiegelkast?", "Dat kan, als de kast daarvoor gemaakt is en buiten de zones rond douche en bad hangt. Een installateur controleert dit volgens de regels voor elektra in badkamers."),
        ],
        "bronnen": ["aanbod", "nen1010"],
        "verder": [("/badkamerspullen/wastafelmeubel-kiezen/", "Wastafelmeubel kiezen"),
                   ("/badkamerspullen/badkamerlampen-kiezen/", "Badkamerlampen kiezen"),
                   ("/kennisbank/badkamerverlichting/", "Badkamerverlichting")],
    },
    # Band vrijstaand_bad €300 – €3.000 (Slimster €300 / €900 / €2.000; Homedeal gietijzer gemiddeld €1.850).
    {
        "slug": "vrijstaand-bad-kopen",
        "kort": "Vrijstaand bad kopen",
        "kaart": "Acryl, staal, solid surface of gietijzer: maten, gewicht, kraan en richtprijzen.",
        "h1": "Vrijstaand bad kopen: materialen, maten en richtprijzen",
        "title": "Vrijstaand bad kopen: materialen en prijzen",
        "desc": "Een vrijstaand bad kopen? Vergelijk acryl, staal-emaille, solid surface en gietijzer. Met maten, ruimte rondom, gewicht op de vloer, de kraan en richtprijzen per materiaal.",
        "lead": "Een vrijstaand bad staat los in de ruimte en is vaak het middelpunt van de badkamer. Het materiaal bepaalt de prijs, het gewicht en hoe lang het water warm blijft. Daarnaast heb je ruimte rondom nodig en een plan voor de kraan.",
        "cat": ["vrijstaand_bad"],
        "soorten": [
            ("Acryl", "Licht, warm aanvoelend, betaalbaar", "Krast sneller, kan iets meegeven", 300, 1200),
            ("Staal-emaille", "Hard en krasvast oppervlak", "Koeler aanvoelend, minder vormen", 700, 2000),
            ("Solid surface (mineraal composiet)", "Mat, strak, houdt warmte goed vast, herstelbaar", "Zwaar en duurder", 900, 3000),
            ("Gietijzer", "Klassiek, zeer stevig, blijft lang warm", "Erg zwaar, vloer moet het dragen", 1500, 3000),
        ],
        "maten": [
            ("Lengte en breedte", "Gangbaar zijn 150 tot 190 cm lang en 70 tot 90 cm breed. Ben je lang, kies dan minstens 170 cm en ga er even in liggen in de showroom."),
            ("Ruimte rondom", "Houd minstens 15 cm tussen bad en muur om schoon te kunnen maken. Wil je er echt omheen kunnen lopen, reken dan op 50 tot 70 cm aan de looprand."),
            ("Inhoud", "Een vrijstaand bad bevat vaak 180 tot 300 liter water. Kijk of je warmwatertoestel of cv-ketel dat in één keer aankan."),
            ("Gewicht", "Een acryl bad weegt leeg ongeveer 30 tot 60 kg, gietijzer of solid surface al snel 100 tot 200 kg. Met water en een persoon erin kom je ruim boven de 400 kg. Op een houten verdiepingsvloer moet een constructeur of specialist dat controleren."),
        ],
        "letop": [
            ("De kraan", "Een staande kraan naast het bad heeft leidingen in de vloer nodig. Een wandkraan kan alleen als het bad dicht bij de muur staat. Beide moeten vóór de vloer klaar is gepland."),
            ("De afvoer", "De afvoer zit onder het bad. Bij een vloer die je niet open kunt breken, moet het bad op de plek van de afvoer komen of verhoogd worden."),
            ("Warm water", "Een combiketel geeft vaak 8 tot 15 liter per minuut. Een bad van 250 liter vullen duurt dan al snel 20 minuten of langer. Bij een kleine boiler is het water op voordat het bad vol is."),
            ("Overloop en plug", "Let op of het bad een overloop heeft en hoe de plug werkt (klik-klak of draaiknop). Dat bepaalt ook welke badafvoer je nodig hebt."),
        ],
        "valkuilen": [
            "Een zwaar bad kiezen zonder te checken of de vloer het draagt.",
            "Het bad plannen waar geen afvoer of waterleiding kan komen.",
            "Te weinig ruimte tussen bad en muur: je komt er niet bij om schoon te maken.",
            "Vergeten dat de kraan apart wordt geprijsd en soms meer kost dan een acryl bad.",
        ],
        "offerte": {
            "goed": "Vrijstaand bad solid surface 170 × 80 cm, mat wit, incl. klik-wasteset met overloop · merk · serie · art.nr. + vrijstaande badkraan (aparte regel)",
            "vaag": "Vrijstaand bad incl. kraan",
            "let": "Staan materiaal, maat en badafvoer erbij? En staat de kraan als eigen regel, met het leidingwerk in de vloer?",
        },
        "faqs": [
            ("Hoeveel ruimte heb je nodig voor een vrijstaand bad?", "Voor het bad zelf 150 tot 190 cm bij 70 tot 90 cm. Houd daarnaast minstens 15 cm tot de muur om schoon te maken en meer aan de kant waar je instapt."),
            ("Kan mijn vloer een vrijstaand bad dragen?", "Een betonvloer meestal wel. Een houten verdiepingsvloer niet altijd, zeker bij een zwaar bad van gietijzer of solid surface. Laat dat controleren voordat je koopt."),
            ("Wat kost een vrijstaand bad?", f"Het bad zelf kost ongeveer {eur(300)} tot {eur(3000)}, inclusief btw, zonder montage en zonder kraan. Acryl zit onderaan, solid surface en gietijzer bovenaan."),
            ("Welk materiaal houdt het water het langst warm?", "Solid surface en gietijzer houden de warmte het langst vast. Acryl isoleert ook redelijk. Staal-emaille koelt sneller af."),
        ],
        "bronnen": ["slimster_vrijstaand", "homedeal_bad", "aanbod"],
        "verder": [("/badkamerspullen/bad-of-douche/", "Bad of douche?"),
                   ("/kennisbank/badkamer-en-suite/", "Badkamer en suite"),
                   ("/inspiratie/wellness-badkamer/", "Inspiratie: wellnessbadkamer")],
    },
    # Banden inbouwreservoir €100 – €400 (Homedeal €150 – €300, verruimd) en bedieningsplaat €40 – €450 (Geberit-brochure, aanbod).
    {
        "slug": "inbouwreservoir-kiezen",
        "kort": "Inbouwreservoir kiezen",
        "kaart": "Frame, hoogte, voorzetwand en bedieningsplaat: zo kies je het deel dat achter de tegels verdwijnt.",
        "h1": "Inbouwreservoir kiezen: frame, hoogte en bedieningsplaat",
        "title": "Inbouwreservoir kiezen: frame, hoogte en plaat",
        "desc": "Een inbouwreservoir kiezen voor een hangtoilet? Lees welke frames er zijn, hoe hoog en diep ze zijn, welke bedieningsplaat past en wat frame en plaat kosten.",
        "lead": "Bij een hangtoilet zit het reservoir in de muur, op een stalen frame. Na het tegelen zie je alleen nog de bedieningsplaat. Juist daarom is dit deel belangrijk: als het later lekt, kom je er alleen via de opening achter de plaat bij.",
        "cat": ["inbouwreservoir", "bedieningsplaat"],
        "soorten": [
            ("Standaard frame (± 112 cm hoog)", "Het meest gangbaar, onderdelen goed te krijgen", "Vraagt een voorzetwand van een vaste hoogte", 100, 250),
            ("Laag frame (± 82 cm, onder een raam)", "Past onder een raam of schuin dak", "Kleinere keuze in bedieningsplaten", 150, 350),
            ("Frame met extra functies", "Bijvoorbeeld een aansluiting voor geurafzuiging of een douchewc", "Duurder, alleen nodig als je die functie wilt", 200, 400),
            ("Bedieningsplaat kunststof", "Goedkoop, veel kleuren", "Minder luxe uitstraling", 40, 120),
            ("Bedieningsplaat metaal, glas of aanraakloos", "Strak en duurzaam", "Duurder, aanraakloos heeft stroom nodig", 120, 450),
        ],
        "maten": [
            ("Hoogte van het frame", "Een standaard frame is ongeveer 112 cm hoog. Lage frames van ongeveer 82 cm passen onder een raam. De bedieningsplaat zit bij een standaard frame op ongeveer 1 meter hoogte."),
            ("Voorzetwand", "Frame en wand samen steken meestal 15 tot 25 cm uit de achterwand. Daar kun je bovenop een plankje of een nis voor spullen maken."),
            ("Zithoogte", "De hoogte van de pot stel je in op het frame, vaak tussen 40 en 48 cm. Voor ouderen of lange mensen is een hogere zitting prettig."),
            ("Boutafstand", "De meeste hangpotten hebben bevestigingsbouten op 18 cm afstand, sommige op 23 cm. Het frame moet daarbij passen."),
        ],
        "letop": [
            ("Plaat past bij het reservoir", "Een bedieningsplaat past alleen op reservoirs van hetzelfde merk en vaak dezelfde serie. Kies frame en plaat dus samen."),
            ("Onderdelen later", "Vulventiel en spoelventiel slijten. Je bereikt ze via de opening achter de bedieningsplaat. Kies een frame waarvan de onderdelen nog jaren te krijgen zijn."),
            ("Waterbesparing", "Een tweeknops-plaat spoelt bijvoorbeeld 3 of 6 liter. Veel reservoirs zijn ook af te stellen op een kleinere spoeling."),
            ("Geluid", "Een frame met geluidsisolatie en een goed gevulde voorzetwand voorkomt dat je het doorspoelen in de hele woning hoort."),
        ],
        "valkuilen": [
            "Een goedkoop onbekend frame kopen waarvan later geen onderdelen te krijgen zijn.",
            "Een bedieningsplaat kiezen die niet op het reservoir past.",
            "De pot pas na het tegelen kiezen, terwijl de boutafstand niet klopt.",
            "Geen stroomaansluiting achter de wand terwijl je later een douchewc of aanraakloze plaat wilt.",
        ],
        "offerte": {
            "goed": "Inbouwreservoir frame 112 cm, met bevestigingsset, voor voorzetwand · merk · serie · art.nr. + bedieningsplaat 2-knops, mat zwart · art.nr.",
            "vaag": "Toilet compleet (hangend)",
            "let": "Staan frame, pot, zitting en bedieningsplaat als losse regels met artikelnummer? Dan kun je per onderdeel zien wat het kost en of de plaat bij het reservoir past.",
        },
        "faqs": [
            ("Hoe lang gaat een inbouwreservoir mee?", "Het frame en het reservoir zelf gaan tientallen jaren mee. Het vulventiel en het spoelventiel slijten eerder en worden via de opening achter de bedieningsplaat vervangen."),
            ("Past elke bedieningsplaat op elk reservoir?", "Nee. Een plaat past meestal alleen op een reservoir van hetzelfde merk, en soms alleen op bepaalde series. Kies ze daarom samen."),
            ("Wat kost een inbouwreservoir?", f"Het frame met reservoir kost ongeveer {eur(100)} tot {eur(400)}, de bedieningsplaat {eur(40)} tot {eur(450)}, inclusief btw en zonder montage. De pot en de zitting komen erbij."),
            ("Kan een inbouwreservoir onder een raam?", "Ja, met een laag frame van ongeveer 82 cm hoog. De keuze in bedieningsplaten is dan wat kleiner, omdat de plaat soms bovenop zit."),
        ],
        "bronnen": ["homedeal_toilet", "geberit_platen", "aanbod"],
        "verder": [("/badkamerspullen/toilet-kiezen/", "Toilet kiezen"),
                   ("/kennisbank/hangtoilet-of-staand-toilet/", "Hangtoilet of staand toilet"),
                   ("/kosten/toilet-renoveren/", "Kosten toilet renoveren")],
    },
    # Geen categorie in de offertevergelijker: band per armatuur uit het aanbod (zie B2['aanbod_licht']).
    {
        "slug": "badkamerlampen-kiezen",
        "kort": "Badkamerlampen kiezen",
        "kaart": "Plafondlamp, spots, spiegellicht en ledstrip: IP-waarde per zone, lichtkleur en richtprijzen.",
        "h1": "Badkamerlampen kiezen: zones, IP-waarde en richtprijzen",
        "title": "Badkamerlampen kiezen: zones, IP en prijzen",
        "desc": "Badkamerlampen kiezen? Lees welke IP-waarde je nodig hebt in zone 0, 1 en 2, hoeveel licht prettig is bij de spiegel en wat plafondlampen, spots en spiegelverlichting kosten.",
        "lead": "In een badkamer komen water en stroom dicht bij elkaar. Daarom gelden er regels voor waar welke lamp mag hangen. Goed licht is daarnaast meer dan één lamp aan het plafond: licht bij de spiegel maakt het verschil.",
        "cat": [],
        "band": (15, 400),
        "soorten": [
            ("Inbouwspot (per stuk)", "Strak, licht gelijkmatig verdeeld", "Plafond moet er ruimte voor hebben", 15, 80),
            ("Plafondlamp of plafonnière", "Eén aansluiting, betaalbaar", "Geeft schaduw bij de spiegel", 20, 180),
            ("Spiegel- of wandlamp", "Licht op je gezicht, minder schaduw", "Extra aansluiting bij de wastafel", 30, 250),
            ("Ledstrip in nis of onder meubel (per set)", "Sfeerlicht, ook als nachtlicht", "Moet waterdicht zijn en een driver hebben", 30, 150),
            ("Spot of armatuur geschikt voor zone 0 of 1", "Kan boven of in de douche", "Hoge IP-waarde, vaak laagspanning", 60, 400),
        ],
        "maten": [
            ("Zone 0", "De binnenkant van het bad of de douchebak. Hier mag alleen materiaal dat onder water kan (minstens IPX7) en dat op veilige laagspanning werkt."),
            ("Zone 1", "Boven bad of douche, tot 225 cm hoogte. Lampen moeten hier minstens spatwaterdicht zijn (IPX4 of hoger)."),
            ("Zone 2", "Een strook van 60 cm rond zone 1. Ook hier minstens IPX4. Daarbuiten mag in principe een gewone lamp, maar IP44 is in de hele badkamer verstandig."),
            ("Hoeveel licht", "Voor algemeen licht is ongeveer 200 tot 300 lux genoeg, bij de spiegel 400 tot 500 lux. Kies een kleurtemperatuur van 2700 tot 4000 kelvin en een kleurweergave (CRI of Ra) van 90 of hoger bij de spiegel."),
        ],
        "letop": [
            ("IP-waarde lezen", "Het eerste cijfer gaat over stof, het tweede over water. IP44 betekent beschermd tegen spatwater van alle kanten. IP65 is ook bestand tegen een waterstraal."),
            ("Dimbaar", "Een dimbare lamp geeft 's avonds rustig licht. Lamp, dimmer en driver moeten bij elkaar passen, anders gaat het licht flikkeren of zoemen."),
            ("Vervangbare lichtbron", "Bij veel ledlampen zit de led vast. Gaat die stuk, dan vervang je de hele lamp. Een armatuur met vervangbare lamp gaat langer mee."),
            ("Laat het aansluiten", "Werk aan elektra in de badkamer hoort bij een erkend installateur. Die weet welke regels voor jouw situatie gelden en sluit alles aan op een groep met aardlekschakelaar."),
        ],
        "valkuilen": [
            "Alleen een plafondlamp: je gezicht staat dan in de schaduw bij de spiegel.",
            "Een gewone lamp zonder IP-waarde boven de douche.",
            "Koud wit licht (boven 5000 kelvin) dat de badkamer kil maakt.",
            "Lampen kopen voordat de plek van de aansluitingen vastligt.",
        ],
        "offerte": {
            "goed": "6× inbouwspot LED IP65, 2700 K, dimbaar, incl. driver · merk · serie · art.nr. + aansluiten op bestaande groep",
            "vaag": "Verlichting badkamer",
            "let": "Staan het aantal lampen, de IP-waarde en de lichtkleur erbij? En is duidelijk of het aansluiten en een eventuele nieuwe groep in de prijs zitten?",
        },
        "faqs": [
            ("Welke IP-waarde heb ik nodig in de badkamer?", "Boven de douche of het bad en in een strook van 60 cm eromheen minstens IPX4, zoals IP44. In het bad of de douchebak zelf alleen materiaal dat onder water kan, op laagspanning. Een installateur weet precies wat in jouw situatie geldt."),
            ("Hoeveel spots heb ik nodig in de badkamer?", "Dat hangt af van de lichtsterkte per spot. Als vuistregel kom je in een badkamer van 6 m² vaak uit op 4 tot 6 spots, plus apart licht bij de spiegel."),
            ("Wat kosten badkamerlampen?", f"Per armatuur ongeveer {eur(15)} tot {eur(400)}, inclusief btw en zonder montage. Een losse spot zit onderaan, een armatuur die geschikt is voor zone 0 of 1 bovenaan. Aansluiten komt erbij."),
            ("Welke lichtkleur is het best voor de badkamer?", "Warm wit (2700 tot 3000 kelvin) voor sfeer en neutraal wit (3500 tot 4000 kelvin) bij de spiegel. Met twee schakelaars of een dimmer kun je allebei."),
        ],
        "bronnen": ["aanbod_licht", "nen1010"],
        "verder": [("/kennisbank/badkamerverlichting/", "Badkamerverlichting"),
                   ("/badkamerspullen/spiegelkast-kiezen/", "Spiegelkast kiezen"),
                   ("/kennisbank/badkamer-ontwerpen/", "Badkamer ontwerpen")],
    },
    # Banden douchewand €150 – €2.000 (Slimster, Bobex), douchecabine €300 – €2.000 (Slimster).
    {
        "slug": "douchewand-kiezen",
        "kort": "Douchewand kiezen",
        "kaart": "Vaste wand, nisdeur, hoekinstap of cabine: welke opstelling past, welk glas en wat kost het?",
        "h1": "Douchewand kiezen: opstellingen, glas en richtprijzen",
        "title": "Douchewand kiezen: opstelling, glas en prijs",
        "desc": "Welke douchewand past bij jouw douche? Vergelijk vaste wand, nisdeur, hoekinstap, kwartronde cabine en badwand. Met glasdikte, maten, onderhoud en richtprijzen per opstelling.",
        "lead": "Welke douchewand past, hangt vooral af van waar je douche staat: tegen één muur, tussen twee muren of in een hoek. Daarna kies je glas, profiel en coating. Op deze pagina zie je alle opstellingen naast elkaar.",
        "cat": ["douchewand", "douchecabine"],
        "soorten": [
            ("Vaste wand (inloop)", "Open, geen deur, makkelijk schoon", "Meer spatwater, ruimte nodig", 150, 900),
            ("Nisdeur (schuif- of draaideur)", "Sluit de douche goed af tussen twee muren", "Rails en scharnieren schoonhouden", 250, 1200),
            ("Hoekinstap (twee deuren of deur + zijwand)", "Compact in een hoek, houdt water binnen", "Meer profielen en naden", 300, 1500),
            ("Kwartronde cabine", "Weinig vloerruimte, compleet pakket", "Gebogen glas is duurder te vervangen", 300, 2000),
            ("Badwand (op de badrand)", "Douchen in bad zonder gordijn", "Smal, vaak toch wat spatwater", 150, 600),
        ],
        "maten": [
            ("Breedte", "Vaste wanden zijn er van ongeveer 70 tot 140 cm. Nisdeuren hebben een verstelbereik van een paar centimeter, bijvoorbeeld 96 tot 101 cm. Meet de nis op drie hoogtes, want muren staan zelden helemaal recht."),
            ("Hoogte", "Gangbaar is 195 tot 200 cm. Bij een regendouche aan het plafond of een stoomfunctie kan een hogere wand nodig zijn."),
            ("Glasdikte", "6 mm voor deuren en cabines, 8 mm voor vaste wanden, 10 mm voor brede of hoge wanden. Altijd gehard veiligheidsglas."),
            ("Instapbreedte", "Een deuropening van minstens 60 tot 70 cm stapt prettig. Bij een vaste wand heb je in totaal minstens 90 bij 120 cm douchezone nodig."),
        ],
        "letop": [
            ("Profiel of profielloos", "Een wand met dun profiel of alleen klemmen ziet er strak uit. Een volledig profiel vangt scheve muren beter op."),
            ("Coating", "Een antikalkcoating laat water makkelijker aflopen. Na het douchen even met een wisser erover blijft het beste tegen kalk."),
            ("Draairichting", "Een draaideur moet naar buiten open kunnen zonder tegen het toilet, de radiator of het meubel te slaan."),
            ("CE-markering", "Douchewanden vallen onder de Europese norm EN 14428. Een CE-markering met prestatieverklaring laat zien dat de wand daarop getest is."),
        ],
        "valkuilen": [
            "Alleen de breedte meten en niet controleren of de muren recht staan.",
            "Een vaste wand in een te kleine douche: het water spat de badkamer in.",
            "Een draaideur die tegen het toilet of de radiator slaat.",
            "Glas zonder coating in een gebied met hard water.",
        ],
        "offerte": {
            "goed": "Nisdeur schuifdeur 120 cm (verstelbaar 116 – 121), 8 mm helder glas met coating, profiel mat zwart, hoogte 200 cm · merk · serie · art.nr.",
            "vaag": "Douchewand glas",
            "let": "Staan breedte, glasdikte, coating en profielkleur erbij? En is de wand op maat ingemeten of standaard? Maatwerk heeft een langere levertijd.",
        },
        "faqs": [
            ("Welke douchewand past in een nis?", "Een nisdeur: een schuifdeur, draaideur of pendeldeur die tussen twee muren past. Meet de nis op drie hoogtes en kijk of het verstelbereik van de deur daarbinnen valt."),
            ("Hoe dik moet het glas van een douchewand zijn?", "Voor deuren en cabines is 6 mm gangbaar, voor vaste wanden 8 mm. Bij brede of hoge wanden kiezen fabrikanten vaak 10 mm. Het glas moet altijd gehard veiligheidsglas zijn."),
            ("Wat kost een douchewand?", f"Een douchewand kost ongeveer {eur(150)} tot {eur(2000)}, inclusief btw, zonder montage. Een vaste wand in standaardmaat zit onderaan, maatwerk en kwartronde cabines bovenaan."),
            ("Wat is het verschil met een inloopdouche?", "Een inloopdouche is een douche met een open instap, meestal met een vaste wand. De douchewand is het glas zelf. Lees ook onze gids over een inloopdouche kopen."),
        ],
        "bronnen": ["slimster_inloop", "bobex_wand", "slimster_douche"],
        "verder": [("/badkamerspullen/inloopdouche-kopen/", "Inloopdouche kopen"),
                   ("/materialen/douchewand-glas/", "Materialen: douchewand en glas"),
                   ("/kosten/douche-vervangen/", "Kosten douche vervangen")],
    },
    # Banden fontein €40 – €450 (Slimster toilet en fontein samen €250 – €900; aanbod) en wastafelkraan €40 – €600.
    {
        "slug": "fontein-kiezen",
        "kort": "Fontein kiezen",
        "kaart": "Standaard, smal of hoekfontein, kraangat links of rechts, koud of warm water: maten en prijzen.",
        "h1": "Fontein kiezen voor het toilet: maten, kraan en richtprijzen",
        "title": "Fontein kiezen: maten, kraan en richtprijzen",
        "desc": "Een fontein kiezen voor de toiletruimte? Vergelijk standaard, smalle en hoekfonteinen en fonteinmeubels. Met maten, kraangat, warm water, sifon en richtprijzen per soort.",
        "lead": "Een fontein is een kleine wastafel in de toiletruimte. Omdat die ruimte vaak maar 80 tot 90 cm breed is, telt elke centimeter. De diepte van de fontein, de plek van het kraangat en de afvoer bepalen of alles past.",
        "cat": ["fontein", "wastafelkraan"],
        "soorten": [
            ("Standaard keramische fontein", "Goedkoop, veel maten", "Steekt 25 cm of meer uit", 40, 150),
            ("Smalle of hoekfontein", "Weinig diepte, past in kleine ruimtes", "Klein bakje, meer spatwater", 60, 250),
            ("Fonteinset met kraan en sifon", "Alles past bij elkaar", "Minder keuze in kraan en kleur", 100, 300),
            ("Fontein met meubeltje of van solid surface of natuursteen", "Opbergruimte of mooi materiaal", "Duurder, natuursteen vraagt onderhoud", 200, 450),
            ("Fonteinkraan (los)", "Vrije keuze in vorm en kleur", "Moet passen bij het kraangat", 40, 250),
        ],
        "maten": [
            ("Breedte en diepte", "Een standaard fontein is ongeveer 36 tot 40 cm breed en 25 cm diep. Smalle modellen zijn 18 tot 22 cm diep. Hoe minder diep, hoe meer ruimte voor je knieën voor de pot."),
            ("Hoogte", "De rand van een fontein hangt meestal op 80 tot 90 cm boven de vloer."),
            ("Kraangat", "Links, rechts of in het midden. Kies de kant die het verst van de deur zit of die het makkelijkst bereikbaar is vanaf het toilet. Een kraan op de muur kan ook, dan heeft de fontein geen kraangat."),
            ("Toiletruimte", "Veel toiletruimtes zijn 80 tot 90 cm breed en 120 tot 150 cm diep. Houd voor de pot ongeveer 60 tot 70 cm beenruimte vrij."),
        ],
        "letop": [
            ("Koud of ook warm water", "De meeste fonteinen hebben alleen koud water. Wil je warm water, dan is er een extra leiding of een klein boilertje onder de fontein nodig. Dat kost extra en vraagt een stopcontact."),
            ("Sifon in het zicht", "Onder een fontein zie je de sifon. Een verchroomde designsifon of een fontein met meubeltje werkt het netjes weg."),
            ("Overloop", "Een fontein zonder overloop ziet er strakker uit, maar loopt over als de afvoer dicht zit. Gebruik dan een plug die niet dicht kan."),
            ("Bevestiging", "Een fontein hangt aan twee bouten. In een holle wand of voorzetwand moet er vooraf een plaat of drager in om op te bevestigen."),
        ],
        "valkuilen": [
            "Een diepe fontein in een smalle toiletruimte: je stoot je knieën.",
            "Een kraangat aan de verkeerde kant ten opzichte van de deur.",
            "Pas na het tegelen bedenken dat je warm water wilt.",
            "Geen drager in de voorzetwand: de fontein zit dan los.",
        ],
        "offerte": {
            "goed": "Fontein keramiek 40 × 22 cm, kraangat rechts, zonder overloop · merk · serie · art.nr. + fonteinkraan koud water, chroom · art.nr. + designsifon",
            "vaag": "Fonteinset compleet",
            "let": "Staan maat, kraangat en kraan als aparte regels? En staat erbij of het alleen koud water is, of dat er een warmwateraansluiting bij komt?",
        },
        "faqs": [
            ("Welke maat fontein past in een kleine toiletruimte?", "Kies een smalle of hoekfontein van 18 tot 22 cm diep. Dan houd je genoeg beenruimte voor de pot. In een ruimte van 80 cm breed past een standaard fontein van 36 cm meestal ook, als hij niet te diep is."),
            ("Kan een fontein ook warm water hebben?", "Ja, met een extra warmwaterleiding of een klein boilertje onder de fontein. Het boilertje heeft een stopcontact nodig. Bespreek dit voordat de wand dicht gaat."),
            ("Wat kost een fontein?", f"Een fontein kost ongeveer {eur(40)} tot {eur(450)}, inclusief btw, zonder montage. Een fonteinkraan kost daarnaast ongeveer {eur(40)} tot {eur(250)}. Een eenvoudige keramische fontein zit onderaan, natuursteen of een fonteinmeubel bovenaan."),
            ("Kraangat links of rechts?", "Kies de kant die je het makkelijkst bereikt vanaf het toilet en die niet in de weg zit bij het openen van de deur."),
        ],
        "bronnen": ["slimster_toilet", "aanbod"],
        "verder": [("/badkamerspullen/toilet-kiezen/", "Toilet kiezen"),
                   ("/badkamerspullen/kranen-kiezen/", "Kranen kiezen"),
                   ("/kosten/toilet-renoveren/", "Kosten toilet renoveren")],
    },
]

# Tekst voor 'Heb je al een offerte voor ...?'
KLUS = {"douchegoot-kiezen": "een douche met goot", "badkamerradiator-kiezen": "een badkamerradiator",
        "spiegelkast-kiezen": "een badkamermeubel met spiegelkast", "vrijstaand-bad-kopen": "een vrijstaand bad",
        "inbouwreservoir-kiezen": "een hangtoilet", "badkamerlampen-kiezen": "badkamerverlichting",
        "douchewand-kiezen": "een douchewand", "fontein-kiezen": "een toilet met fontein"}

LINKS = [(f"{BASIS}{g['slug']}/", g["kort"], g["kaart"]) for g in GIDSEN2]


def _band_gids(g):
    """Laagste en hoogste prijs van de soorten (valt binnen de categorieband)."""
    return min(s[3] for s in g["soorten"]), max(s[4] for s in g["soorten"])


def _controleer():
    """Elke soortprijs moet binnen een van de marktbanden van de offertevergelijker vallen."""
    for g in GIDSEN2:
        banden = [band(c) for c in g["cat"]] or [g["band"]]
        lo, hi = min(b[0] for b in banden), max(b[1] for b in banden)
        for s in g["soorten"]:
            assert lo <= s[3] < s[4] <= hi, (g["slug"], s[0])


_controleer()

# ---------------------------------------------------------------------------
# Eigen CSS (voorvoegsel .b2-), aanvullend op badkamer_spullen.CSS (.bs-)
# ---------------------------------------------------------------------------
CSS2 = """<style>
.b2-svg{max-width:460px}
.b2-svg text{font-weight:600}
.b2-svg .b2-maat{stroke:var(--accent);stroke-width:1.3}
.b2-svg .b2-zone1{fill:rgba(36,96,107,.16);stroke:none}
.b2-svg .b2-zone2{fill:rgba(36,96,107,.07);stroke:none}
.b2-svg .b2-glas-l{stroke:#3a8fa0;stroke-width:3}
.b2-soorten{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px;margin-top:18px}
.b2-soort{display:flex;flex-direction:column;gap:6px}
.b2-soort h3{font-size:1.05rem;margin:0}
.b2-soort p{margin:0;font-size:.94rem}
.b2-soort .b2-plus::before{content:"+ ";font-weight:800;color:var(--accent)}
.b2-soort .b2-min::before{content:"– ";font-weight:800;color:var(--muted)}
.b2-soort .b2-prijs{margin-top:auto;padding-top:8px;border-top:1px solid var(--line);font-weight:700;color:var(--ink)}
.b2-maten{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:18px 0 0}
.b2-maten dt{font-weight:700;color:var(--ink);font-size:1.05rem}
.b2-maten dd{margin:6px 0 0}
.b2-valk{list-style:none;padding:0;margin:14px 0 0}
.b2-valk li{position:relative;padding-left:30px;margin-bottom:.6em}
.b2-valk li::before{content:"!";position:absolute;left:0;top:1px;width:20px;height:20px;border-radius:50%;background:var(--accent-soft);color:#9c4019;font-weight:800;font-size:.8rem;text-align:center;line-height:20px}
.b2-regels{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:16px 0}
.b2-regel{border:1px solid var(--line);border-radius:var(--radius);background:#fff;padding:14px 16px}
.b2-regel .b2-lbl{font-size:.78rem;font-weight:750;text-transform:uppercase;letter-spacing:.03em;margin:0 0 6px}
.b2-regel code{display:block;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.86rem;white-space:normal;overflow-wrap:anywhere;color:var(--ink)}
.b2-goed{border-left:4px solid #2f8a5b}.b2-goed .b2-lbl{color:#2f7a52}
.b2-vaag{border-left:4px solid #c2562a}.b2-vaag .b2-lbl{color:#9c4019}
.b2-woorden{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 0;padding:0;list-style:none}
.b2-woorden li{background:var(--bg-soft);border:1px solid var(--line);border-radius:99px;padding:3px 10px;font-size:.85rem}
@media(max-width:760px){.b2-maten,.b2-regels{grid-template-columns:1fr}}
</style>"""


def _bronnen_html(sleutels):
    items = ""
    for k in sleutels:
        naam, url = _bron(k)
        items += f'<li><a href="{url}" rel="noopener nofollow">{naam}</a></li>' if url else f"<li>{naam}</li>"
    return f'<ol class="bs-bronnen">{items}</ol>'


def _soorten_html(g):
    kaarten = "".join(
        f'<div class="card b2-soort reveal"><h3>{n}</h3><p class="b2-plus">{goed}</p><p class="b2-min">{min_}</p>'
        f'<p class="b2-prijs">{eur(v)} – {eur(t)}</p></div>'
        for n, goed, min_, v, t in g["soorten"])
    return f'<div class="b2-soorten">{kaarten}</div>'


def _trefwoorden(g):
    woorden = []
    for c in g["cat"]:
        for w in CAT[c]["trefwoorden"]:
            if w not in woorden and len(woorden) < 10:
                woorden.append(w)
    return woorden


def _andere_gidsen(huidig):
    eigen = "".join(
        f'<a class="card bs-kaart reveal" href="{BASIS}{x["slug"]}/">{illustratie2(x["slug"], klein=True)}'
        f'<h3>{x["kort"]}</h3><span class="go">Lees de gids →</span></a>'
        for x in GIDSEN2 if x["slug"] != huidig)
    oud = "".join(f'<li><a href="{BASIS}{x["slug"]}/">{x["kort"]}</a></li>' for x in BS.GIDSEN)
    return (f'<div class="grid g3">{eigen}</div>'
            f'<div class="prose" style="margin-top:22px"><h3>Meer kopersgidsen</h3><ul>{oud}'
            f'<li><a href="{BASIS}">Alle badkamerspullen</a></li></ul></div>')


def gids_body(g):
    cr, cr_ld = crumbs([("Home", "/"), ("Badkamerspullen", BASIS), (g["kort"], None)])
    laag, hoog = _band_gids(g)
    if g["cat"]:
        markt = "; ".join(f'{CAT[c]["naam"].lower()} {eur(CAT[c]["van"])} – {eur(CAT[c]["tot"])}' for c in g["cat"])
        markt_zin = (f"De marktband die onze offertevergelijker gebruikt: {markt} (peildatum {PEIL}).")
    else:
        markt_zin = (f"Voor lampen heeft de offertevergelijker geen eigen band; deze bedragen komen uit ons eigen "
                     f"vergelijk van het aanbod (peildatum {PEIL}).")

    hero = f"""<section class="section-sm"><div class="wrap">
  <div class="grid g2" style="gap:44px;align-items:center">
    <div>
      <span class="badge">Kopersgids · richtprijzen {PEIL}</span>
      <h1>{g['h1']}</h1>
      <p class="lead">{g['lead']}</p>
      <div class="callout callout-prijs">
        <p><strong>Richtprijs voor het product:</strong> {eur(laag)} – {eur(hoog)}, inclusief 21% btw, los van de montage.</p>
        <p style="font-size:.93rem;margin-top:8px">Wij verkopen niets en verwijzen niet naar winkels. Deze gids noemt geen merken.</p>
      </div>
    </div>
    <div>{illustratie2(g['slug'])}</div>
  </div>
</div></section>"""

    soorten = f"""<section class="section soft"><div class="wrap">
  <div class="narrow prose" style="margin:0 auto"><h2>Welke soorten zijn er, en wat kosten ze?</h2>
  <p>Per soort zie je waar hij goed in is, waar hij minder sterk is en een richtprijs voor het product zelf. {markt_zin}</p></div>
  {_soorten_html(g)}
</div></section>"""

    maten_dl = "".join(f'<div class="card reveal"><dt>{k}</dt><dd>{t}</dd></div>' for k, t in g["maten"])
    maten = f"""<section class="section"><div class="wrap">
  <div class="narrow prose" style="margin:0 auto"><h2>Maten die je moet weten</h2>
  <p>De maten in de illustratie bovenaan, uitgelegd. Het zijn gangbare waarden; de maatvoering van het product dat je kiest gaat altijd voor.</p></div>
  <dl class="b2-maten">{maten_dl}</dl>
</div></section>"""

    prijzen = f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Richtprijzen naast elkaar</h2>
  {prijs_balken([(s[0], s[3], s[4]) for s in g['soorten']], "Richtprijs product, inclusief 21% btw, zonder montage")}
  <p class="bs-noot">Peildatum {PEIL}. Prijzen wisselen per winkel en per actie. Gebruik ze om te zien of een prijs in de buurt zit, niet als offerte. Montage, leidingwerk en afwerking komen erbij.</p>
  {cta_midden("Wil je weten wat het geplaatst kost?", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit jouw regio. Dan zie je de prijs inclusief montage.")}
</div></section>"""

    letop_k = "".join(f'<div class="card"><h3>{k}</h3><p>{t}</p></div>' for k, t in g["letop"])
    valk = "".join(f"<li>{v}</li>" for v in g["valkuilen"])
    letop = f"""<section class="section"><div class="wrap">
  <div class="narrow prose" style="margin:0 auto"><h2>Waar let je op?</h2></div>
  <div class="bs-letop">{letop_k}</div>
  <div class="narrow prose" style="margin:30px auto 0"><h3>Veelgemaakte fouten</h3><ul class="b2-valk">{valk}</ul></div>
</div></section>"""

    o = g["offerte"]
    woorden = "".join(f"<li>{w}</li>" for w in _trefwoorden(g))
    woorden_html = (f"<p>De offertevergelijker herkent dit product onder meer aan woorden als:</p><ul class=\"b2-woorden\">{woorden}</ul>"
                    if woorden else "")
    offerte = f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Zo herken je het op een offerte</h2>
  <p>Een goede offerte noemt per product het <strong>merk</strong>, de <strong>serie</strong> (de productlijn) en het <strong>artikelnummer</strong> van de fabrikant. Met die drie gegevens kun je het product opzoeken, de maat controleren en de prijs vergelijken. Staat er alleen een algemene omschrijving, vraag dan om de artikelnummers.</p>
  <div class="b2-regels">
    <div class="b2-regel b2-goed"><p class="b2-lbl">{icon('check', 16)} Duidelijke regel</p><code>{o['goed']}</code></div>
    <div class="b2-regel b2-vaag"><p class="b2-lbl">Vage regel</p><code>{o['vaag']}</code></div>
  </div>
  <p><strong>Let op:</strong> {o['let']}</p>
  {woorden_html}
  {offertecheck_blok(KLUS[g['slug']])}
</div></section>"""

    faq_html, faq_ld = faq_blok(g["faqs"], f"Veelgestelde vragen: {g['kort'].lower()}")

    verder = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in g.get("verder", []))
    bronnen = f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Bronnen</h2>
  <p>De richtprijzen zijn bandbreedtes uit kostenartikelen, vergelijkers en het aanbod van meerdere winkels samen, gecontroleerd in {PEIL}. Het zijn geen offertes en geen prijzen van één winkel. Maten zijn gangbare waarden; de maten van het product dat je kiest gaan altijd voor.</p>
  {_bronnen_html(g['bronnen'])}
  <h3>Verder lezen</h3><ul>{verder}</ul>
</div></section>"""

    andere = f"""<section class="section"><div class="wrap">
  <h2>Andere kopersgidsen</h2>
  {_andere_gidsen(g['slug'])}
</div></section>"""

    body = (BS.CSS + CSS2 + cr + hero + soorten + maten + prijzen + letop + offerte + faq_html + bronnen + andere
            + cta_blok("Liever meteen een prijs inclusief montage?",
                       "Vul in een minuut het formulier in en ontvang vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio."))
    return body, [cr_ld, faq_ld]


def index_kaarten():
    """Kaarten voor de overzichtspagina /badkamerspullen/ (in te voegen door badkamer_spullen.index_body).

    Gebruikt de klassen .bs-kaart en .bs-ill uit badkamer_spullen.CSS plus CSS2 hieronder.
    """
    kaarten = "".join(
        f'<a class="card bs-kaart reveal" href="{BASIS}{g["slug"]}/">{illustratie2(g["slug"], klein=True)}'
        f'<h3>{g["kort"]}</h3><p>{g["kaart"]}</p>'
        f'<p class="price">Richtprijs {eur(_band_gids(g)[0])} – {eur(_band_gids(g)[1])}</p>'
        f'<span class="go">Lees de gids →</span></a>'
        for g in GIDSEN2)
    return CSS2 + f'<div class="grid g3">{kaarten}</div>'


def build(write):
    for g in GIDSEN2:
        body, ld = gids_body(g)
        url = f"{BASIS}{g['slug']}/"
        write(url, page(title(g["title"], limit=62), g["desc"], url, body, ld), prio=0.6)
