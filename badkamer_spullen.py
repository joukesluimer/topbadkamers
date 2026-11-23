"""Badkamerspullen: neutrale kopersgidsen voor sanitair en materialen.

Een overzicht op /badkamerspullen/ en zeven gidsen op /badkamerspullen/<slug>/.
Wij verkopen niets, krijgen geen commissie en noemen geen merken of winkels.
Alle prijzen zijn richtprijzen voor het product zelf (inclusief 21% btw),
los van de montage. Elke gids noemt zijn bronnen op de pagina.

Prijsonderzoek: november 2026, via WebSearch. Gebruikt zijn bandbreedtes uit
kostenartikelen en vergelijkers (Slimster, Werkspot, Homedeal, Bobex) en, waar
die ontbraken, het gecombineerde aanbod van meerdere bouwmarkten en
sanitairwinkels. Nooit de prijs van één winkel.
"""

import datetime

from components import page, title, crumbs, faq_blok, cta_blok, cta_midden, prijs_balken, eur, icon

JAAR = datetime.date.today().year
BASIS = "/badkamerspullen/"

# ---------------------------------------------------------------------------
# Bronnen (op de pagina's getoond onder "Bronnen")
# ---------------------------------------------------------------------------
B = {
    "slimster_inloop": ("Slimster: kosten inloopdouche (gemiddeld €825 zonder montage, spreiding €250 tot €1.400)",
                        "https://slimster.nl/badkamer/douche-plaatsen-kosten/inloopdouche/"),
    "bobex_wand": ("Bobex: welk materiaal voor een douchewand (eenvoudig €100 tot €200, luxe tot ruim €2.000)",
                   "https://www.bobex.be/nl-be/badkamerrenovatie/douchewand/"),
    "homedeal_inloop": ("Homedeal: kosten inloopdouche, inclusief plaatsing",
                        "https://www.homedeal.nl/badkamerspecialist/inloopdouche/"),
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
    "kiwa_kranen": ("Kiwa: certificering en testen van sanitaire kranen (onder meer BRL-K652)",
                    "https://www.kiwa.com/nl/nl/diensten/testen/kiwa-watermark-certificering-en-testen-voor-sanitaire-kranen/"),
    "kiwa_keramiek": ("Kiwa: certificering en testen van keramiek, zoals toiletpotten en reservoirs",
                      "https://www.kiwa.com/nl/nl/diensten/testen/kiwa-watermark-certificering-en-testen-voor-keramiek-en-accessoires/"),
    "mc_douchekop": ("Milieu Centraal: kluswijzer waterbesparende douchekop (4,0 tot 7,2 liter per minuut)",
                     "https://www.milieucentraal.nl/media/q1bb4qtr/kluswijzer-waterbesparende-douchekop.pdf"),
    "mc_checklist": ("Milieu Centraal: verbouwingschecklist badkamer",
                     "https://www.milieucentraal.nl/media/dvaafvgn/verbouwingschecklist_badkamer_milieu-centraal.pdf"),
    "cbs_douche": ("CBS: Watergebruik thuis 2021, hoofdstuk De douche",
                   "https://www.cbs.nl/nl-nl/longread/aanvullende-statistische-diensten/2022/watergebruik-thuis--wgt---2021/6-de-douche"),
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
    "bobex_bad": ("Bobex: de verschillende soorten baden", "https://www.bobex.be/nl-be/badkamerrenovatie/bad/"),
    "aanbod": ("Eigen vergelijking van het aanbod bij meerdere bouwmarkten en sanitairwinkels, november 2026 (geen links, wij verwijzen niet naar winkels)", None),
}

# ---------------------------------------------------------------------------
# Illustraties (eenvoudige inline SVG, lijnen in currentColor)
# ---------------------------------------------------------------------------
_SVG_OPEN = ('<svg class="bs-svg" viewBox="0 0 240 160" role="img" aria-label="{label}" fill="none" '
             'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">')

ILL = {
    # Inloopdouche: vaste glaswand met stang, douchekop aan de wand en een goot in de vloer
    "inloopdouche-kopen": (
        "Illustratie van een inloopdouche met vaste glaswand",
        '<path d="M20 140h200"/><path d="M40 140V20"/>'
        '<rect class="bs-glas" x="120" y="30" width="56" height="110" rx="2"/>'
        '<path d="M176 40h0M120 40H40"/><path d="M58 30v42"/><path d="M58 30h22"/>'
        '<path class="bs-vlak" d="M70 30h22a2 2 0 0 1 2 2v3H68v-3a2 2 0 0 1 2-2z"/>'
        '<path class="bs-dun" d="M74 42v10M81 42v14M88 42v10"/>'
        '<rect x="54" y="84" width="14" height="10" rx="2"/>'
        '<rect class="bs-vlak" x="60" y="136" width="44" height="5" rx="1"/>'
        '<path class="bs-dun" d="M132 40l12 30M146 40l12 30"/>'),
    # Toilet: hangtoilet met inbouwreservoir in een voorzetwand (gestippeld) en een bedieningsplaat
    "toilet-kiezen": (
        "Illustratie van een hangtoilet met inbouwreservoir achter de wand",
        '<path d="M20 140h200"/><path d="M110 20v120"/>'
        '<rect class="bs-stippel" x="70" y="40" width="36" height="96" rx="3"/>'
        '<rect class="bs-vlak" x="78" y="50" width="20" height="30" rx="3"/>'
        '<rect x="114" y="58" width="16" height="12" rx="2"/>'
        '<path d="M110 92h70a20 20 0 0 1-20 20h-30"/><path d="M110 112h20l-4 14"/>'
        '<path d="M110 92h74"/>'),
    # Wastafelmeubel: zwevend meubel met twee lades, wastafel, kraan en spiegel
    "wastafelmeubel-kiezen": (
        "Illustratie van een zwevend wastafelmeubel met twee lades en spiegel",
        '<path d="M20 145h200"/>'
        '<rect x="80" y="14" width="80" height="44" rx="4"/>'
        '<path d="M60 82h120"/><rect class="bs-vlak" x="60" y="76" width="120" height="8" rx="2"/>'
        '<rect x="62" y="84" width="116" height="48" rx="3"/><path d="M62 108h116"/>'
        '<path d="M108 96h24M108 120h24"/><path d="M120 76v-10h12"/>'),
    # Kranen: eenhendel mengkraan op een waskom
    "kranen-kiezen": (
        "Illustratie van een eenhendel mengkraan op een wastafel",
        '<path d="M40 120h160"/><path d="M50 120q0 22 70 22t70-22"/>'
        '<rect x="104" y="58" width="18" height="62" rx="3"/>'
        '<path d="M113 70h34a8 8 0 0 1 8 8v6"/><path class="bs-dun" d="M155 92v14"/>'
        '<path d="M112 58l-14-18"/><rect class="bs-vlak" x="92" y="30" width="14" height="10" rx="3" transform="rotate(-50 99 35)"/>'),
    # Tegels: drie formaten naast elkaar
    "badkamertegels-kopen": (
        "Illustratie van drie tegelformaten: groot vierkant, langwerpig en mozaïek",
        '<rect x="18" y="30" width="64" height="64" rx="2"/><rect class="bs-vlak" x="22" y="34" width="56" height="56" rx="1"/>'
        '<rect x="96" y="30" width="56" height="28" rx="2"/><rect x="96" y="66" width="56" height="28" rx="2"/>'
        '<rect x="166" y="30" width="56" height="64" rx="2"/>'
        '<path class="bs-dun" d="M180 30v64M194 30v64M208 30v64M166 46h56M166 62h56M166 78h56"/>'
        '<path class="bs-dun" d="M18 116h64M96 116h56M166 116h56"/>'),
    # Douchesysteem: opbouwthermostaat, stang, regendouche en handdouche
    "douchesysteem-kiezen": (
        "Illustratie van een douchesysteem met thermostaat, stang, regendouche en handdouche",
        '<path d="M20 145h200"/>'
        '<rect class="bs-vlak" x="92" y="104" width="56" height="12" rx="6"/>'
        '<circle cx="96" cy="110" r="7"/><circle cx="144" cy="110" r="7"/>'
        '<path d="M120 104V30h36"/>'
        '<path class="bs-vlak" d="M146 30h36a2 2 0 0 1 2 2v4h-40v-4a2 2 0 0 1 2-2z"/>'
        '<path class="bs-dun" d="M152 44v12M164 44v16M176 44v12"/>'
        '<path d="M114 64h12"/><path d="M120 64l-14 18"/><path d="M110 116q-16 10-6 24"/>'),
    # Bad of douche: links een bad, rechts een douche
    "bad-of-douche": (
        "Illustratie van een ligbad naast een douche",
        '<path d="M14 140h212"/><path d="M120 30v110"/>'
        '<path class="bs-vlak" d="M22 92h88v10a26 26 0 0 1-26 26H48a26 26 0 0 1-26-26z"/>'
        '<path d="M18 92h96"/><path d="M36 128l-4 10M96 128l4 10"/><path d="M34 92V70a10 10 0 0 1 20 0"/>'
        '<path d="M150 40h0"/><path d="M146 140V44h28"/>'
        '<path class="bs-vlak" d="M166 44h24a2 2 0 0 1 2 2v3h-28v-3a2 2 0 0 1 2-2z"/>'
        '<path class="bs-dun" d="M170 56v12M178 56v16M186 56v12"/>'
        '<rect class="bs-glas" x="198" y="50" width="22" height="90" rx="2"/>'),
}


def illustratie(slug, klein=False):
    label, inhoud = ILL[slug]
    svg = _SVG_OPEN.format(label=label) + inhoud + "</svg>"
    if klein:
        return f'<div class="bs-ill bs-ill-klein" aria-hidden="true">{svg}</div>'
    return f'<figure class="bs-ill">{svg}<figcaption>Illustratie: {label[len("Illustratie van "):]}</figcaption></figure>'


# ---------------------------------------------------------------------------
# De gidsen
# ---------------------------------------------------------------------------
# Velden per gids:
#   slug, kort (kaarttitel), h1, title, desc, lead, intro (alinea's)
#   soorten: [(soort, voordelen, nadelen, past bij)]
#   prijs_wat: wat de prijs omvat; prijzen: [(klasse, van, tot, wat je krijgt)]
#   prijs_noot, prijs_extra (optioneel, html)
#   letop: [(kop, tekst)]
#   zelf: [..], specialist: [..], dienst: (slug, naam), kosten: (slug, naam)
#   faqs: [(vraag, antwoord)], bronnen: [sleutels uit B], verder: [(href, tekst)]

GIDSEN = [
    {
        "slug": "inloopdouche-kopen",
        "kort": "Inloopdouche kopen",
        "kaart": "Vaste glaswand, nis met deur of cabine: wat past bij jouw badkamer en wat kost de wand zelf?",
        "h1": "Inloopdouche kopen: soorten, richtprijzen en waar je op let",
        "title": "Inloopdouche kopen: soorten en richtprijzen",
        "desc": "Een inloopdouche kopen? Vergelijk vaste glaswanden, nissen met deur en cabines. Met richtprijzen voor de wand zelf, maten, glasdikte en wanneer je een specialist nodig hebt.",
        "lead": "Een inloopdouche is een douche zonder deur of bak, vaak met één vaste glazen wand. Hieronder lees je welke soorten er zijn, wat de wand zelf ongeveer kost en waar je op let voordat je koopt.",
        "soorten": [
            ("Vaste glaswand (walk-in)", "Open en licht, geen deur die vuil wordt, makkelijk schoon te houden", "Meer spatwater en soms tocht; je hebt een ruime douchezone nodig", "Badkamers met genoeg ruimte, vanaf ongeveer 90 bij 120 cm"),
            ("Vaste wand met draaibaar zijpaneel", "Minder spatwater dan alleen een vaste wand, toch open", "Extra scharnieren om schoon te houden, iets duurder", "Douchezones die net wat kort zijn"),
            ("Nis met schuif- of draaideur", "Houdt het water goed binnen, warm douchen", "Deur en rails vragen onderhoud; minder open gevoel", "Een douche tussen twee muren"),
            ("Douchecabine of kwartronde hoekinstap", "Compleet pakket, goedkoop, makkelijk te plaatsen", "Minder strak, vaak met douchebak en drempel", "Kleine badkamers en een beperkt budget"),
            ("Betegelde vloer met goot (de vloer, niet de wand)", "Drempelloos, één doorlopende vloer", "Afschot en waterdicht maken vragen vakwerk", "Wie gelijkvloers wil douchen"),
        ],
        "prijs_wat": "de douchewand zelf, inclusief profiel en eventuele stabilisatiestang",
        "prijzen": [
            ("Instap", 150, 400, "Vaste wand in standaardmaat, 6 of 8 mm glas, chromen of aluminium profiel."),
            ("Midden", 400, 900, "8 mm gehard glas met antikalkcoating, stabilisatiestang, ook met draaibaar paneel of deur."),
            ("Hoog", 900, 2000, "Maatwerk, 10 mm glas, gekleurd of zwart profiel, getint of gezandstraald glas."),
        ],
        "prijs_noot": "Richtprijs voor de wand zelf, inclusief 21% btw, zonder douchegoot, afvoer, tegels en montage. Slimster noemt gemiddeld €825 met een spreiding van €250 tot €1.400, Bobex €100 tot €200 voor een eenvoudige wand en tot ruim €2.000 voor luxe.",
        "letop": [
            ("Maat van de douchezone", "Meet de ruimte waar je onder staat, niet alleen de muur. Als vuistregel heb je met één vaste wand minstens 90 bij 120 cm nodig om niet alles nat te spetteren. Hoe korter de wand, hoe meer water er langs komt."),
            ("Glas", "Kies gehard veiligheidsglas. 8 mm is gebruikelijk; 6 mm is lichter maar gaat sneller trillen bij een brede wand. Bij een wand breder dan ongeveer 90 cm hoort een stabilisatiestang naar de muur of het plafond."),
            ("Coating en onderhoud", "Een antikalkcoating zorgt dat water beter afloopt. Het scheelt poetsen, maar een wisser na het douchen blijft nodig in gebieden met hard water."),
            ("CE-markering", "Douchewanden vallen onder de Europese norm EN 14428. Een CE-markering met prestatieverklaring laat zien dat de wand daarop is getest. Er is geen apart Nederlands keurmerk voor douchewanden."),
            ("Goot of put", "Een douchegoot langs de muur geeft afschot in één richting; dat maakt grote tegels mogelijk. Een put in het midden vraagt afschot naar vier kanten en meestal kleinere tegels."),
            ("Drempel of niet", "Wil je gelijkvloers douchen, dan moet de vloer vaak verlaagd of de rest van de badkamer verhoogd worden. Dat bepaalt de kosten meer dan de wand zelf."),
        ],
        "zelf": ["Je een complete cabine of een wand op een bestaande, goed aflopende douchevloer plaatst.",
                 "De wand recht en stevig kan worden vastgezet in steen of een versterkte wand.",
                 "Je ervaring hebt met boren in tegels en kitten."],
        "specialist": ["De vloer opnieuw op afschot moet, of je een goot wilt laten inbouwen.",
                       "De douchezone waterdicht gemaakt moet worden (kimband, folie of coating onder de tegels).",
                       "De afvoer verplaatst moet worden of je drempelloos wilt douchen.",
                       "Het om maatwerkglas gaat: daar hoort inmeten bij."],
        "dienst": ("inloopdouche-plaatsen", "inloopdouche plaatsen"),
        "kosten": ("inloopdouche", "kosten van een inloopdouche"),
        "faqs": [
            ("Wat is het verschil tussen een inloopdouche en een douchecabine?",
             "Een inloopdouche heeft geen deur en meestal geen douchebak: je loopt er via een opening in. Een douchecabine is een gesloten geheel met deuren, vaak op een bak. Een cabine is goedkoper en sneller geplaatst; een inloopdouche is opener en makkelijker schoon te houden."),
            ("Hoe breed moet de glaswand van een inloopdouche zijn?",
             "Dat hangt af van de lengte van de douchezone. Gangbaar is een wand van 90 tot 120 cm. Hoe dichter de douchekop bij de opening zit, hoe langer de wand moet zijn om spatwater binnen te houden."),
            ("Is een inloopdouche koud?",
             "Een open douche kan iets frisser aanvoelen dan een cabine, omdat de warme lucht ontsnapt. Een draaibaar zijpaneel, vloerverwarming of een goede plek van de douchekop helpt."),
            ("Kan ik een inloopdouche maken in een kleine badkamer?",
             "Ja, vaak met een korte vaste wand en een draaibaar paneel, of met een nis met deur. Lees ook onze tips over het indelen van een kleine badkamer."),
            ("Wat kost een inloopdouche inclusief plaatsing?",
             "Dat is veel meer dan de wand alleen, omdat de vloer, de afvoer, het waterdicht maken en het tegelwerk meetellen. Homedeal noemt €1.500 tot €5.000. Op onze kostenpagina staat een uitgebreide opbouw."),
        ],
        "bronnen": ["slimster_inloop", "bobex_wand", "homedeal_inloop", "mc_checklist"],
        "verder": [("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Badkamer waterdicht maken"),
                   ("/kennisbank/kleine-badkamer-indelen/", "Kleine badkamer indelen")],
    },
    {
        "slug": "toilet-kiezen",
        "kort": "Toilet kiezen",
        "kaart": "Staand of hangend, randloos of met douchefunctie: de soorten, de zithoogte en de richtprijzen.",
        "h1": "Toilet kiezen: staand, hangend of randloos?",
        "title": "Toilet kiezen: soorten, maten en richtprijzen",
        "desc": "Welk toilet past bij jou? Vergelijk staande toiletten, hangtoiletten met inbouwreservoir, randloze potten en douche-wc's. Met richtprijzen, maten en tips voor zuinig spoelen.",
        "lead": "Een toilet koop je voor twintig jaar of langer. Het belangrijkste verschil zit tussen staand en hangend, en dat bepaalt ook hoeveel werk de montage is. Hieronder zie je de soorten, de richtprijzen en waar je op let.",
        "soorten": [
            ("Staand toilet (duoblok)", "Goedkoop, makkelijk te vervangen, reservoir bereikbaar", "Lastiger schoon te maken rond de voet, neemt meer plek in", "Vervangen op dezelfde plek, beperkt budget"),
            ("Hangtoilet met inbouwreservoir", "Vloer eronder makkelijk schoon, rustig beeld, hoogte instelbaar bij montage", "Duurder, er is een voorzetwand of frame nodig", "Een nieuwe badkamer of een complete toiletrenovatie"),
            ("Randloos toilet (staand of hangend)", "Geen spoelrand waar vuil zich verzamelt, sneller schoon", "Spoelt soms iets harder, net iets duurder", "Iedereen die minder wil poetsen"),
            ("Verkort toilet", "Steekt minder ver uit de muur, scheelt ruimte", "Iets minder zitcomfort voor sommige mensen", "Kleine toiletruimtes"),
            ("Verhoogd toilet (comforthoogte)", "Makkelijker gaan zitten en opstaan", "Voor kinderen minder handig", "Ouderen en mensen met knie- of heupklachten"),
            ("Douche-wc", "Reinigt met water, minder papier", "Duur, heeft een stopcontact en wateraansluiting nodig", "Wie extra comfort of hygiëne zoekt"),
        ],
        "prijs_wat": "de toiletpot met zitting, en bij een hangtoilet ook het inbouwreservoir en de bedieningsplaat",
        "prijzen": [
            ("Instap", 100, 250, "Staand duoblok met reservoir, soms zonder zitting; let daarop bij het vergelijken."),
            ("Midden", 250, 600, "Hangtoilet met inbouwreservoir en bedieningsplaat als set, of een randloos staand toilet met softclose-zitting."),
            ("Hoog", 600, 1500, "Design- of randloze hangsets met extra functies; douche-wc's zitten vaak boven de €1.000."),
        ],
        "prijs_noot": "Richtprijs voor het product, inclusief 21% btw, zonder montage en leidingwerk. Bobex noemt €200 tot €500 voor een staand toilet en €200 tot €600 voor een hangtoilet met inbouwreservoir; Homedeal €150 tot €300 voor alleen het inbouwreservoir.",
        "letop": [
            ("Aansluiting van een staand toilet", "Kijk of je oude toilet een afvoer in de vloer heeft (AO, onderuitgang) of in de muur (PK, achteruitgang). Een nieuw staand toilet moet daarop passen, anders moet de afvoer worden aangepast."),
            ("Inbouwreservoir en bedieningsplaat", "Een bedieningsplaat past meestal alleen op een reservoir van hetzelfde merk. Koop ze dus samen, of vraag na welke platen passen. Een verlaagd reservoir bestaat voor onder een raam of schuin dak."),
            ("Zithoogte en diepte", "Een gewone pot zit rond 40 tot 42 cm hoog, een verhoogde rond 46 tot 48 cm. Een hangtoilet kun je zelf op hoogte laten monteren. Verkorte potten steken minder ver uit, handig in een smal toilet."),
            ("Zuinig spoelen", "Kies een reservoir met een grote en kleine spoeltoets. De kleine knop gebruikt ongeveer de helft van het water. Milieu Centraal raadt bij een verbouwing waterbesparend sanitair aan."),
            ("Keurmerk", "Kiwa test en certificeert toiletpotten, reservoirs en vlotterkranen op werking en veiligheid voor het drinkwater. Vraag of het product dat keur heeft."),
            ("Zitting", "Een softclose-zitting valt niet dicht met een klap. Een quick-release zitting klik je los om de pot goed schoon te maken."),
        ],
        "zelf": ["Je een staand toilet vervangt door een nieuw exemplaar met dezelfde aansluiting.",
                 "Je alleen een nieuwe zitting of bedieningsplaat plaatst.",
                 "Je ervaring hebt met afkitten en het aansluiten van een vlotterkraan."],
        "specialist": ["Je van staand naar hangend overstapt: er komt een frame en een voorzetwand.",
                       "Het toilet op een andere plek moet komen of de afvoer niet past.",
                       "Er een stopcontact moet komen voor een douche-wc.",
                       "Er in een oud toilet mogelijk asbest zit, bijvoorbeeld in een oud reservoir of in vloerzeil."],
        "dienst": ("toilet-renoveren", "toilet renoveren"),
        "kosten": ("toilet-renoveren", "kosten van een toiletrenovatie"),
        "faqs": [
            ("Is een hangtoilet beter dan een staand toilet?",
             "Niet beter, wel anders. Een hangtoilet is makkelijker schoon te houden en ziet er rustiger uit. Een staand toilet is goedkoper en eenvoudiger te vervangen. Bij een complete renovatie kiezen veel mensen voor hangend, bij alleen vervangen vaak voor staand."),
            ("Hoeveel gewicht kan een hangtoilet dragen?",
             "Een goed gemonteerd frame is gemaakt voor gewoon gebruik door volwassenen. Het hangt sterk af van de montage en de wand. Vraag de specialist naar de opgegeven belasting van het frame dat hij gebruikt."),
            ("Wat is het verschil tussen AO en PK?",
             "AO betekent dat de afvoer recht naar beneden in de vloer gaat, PK dat hij naar achteren in de muur gaat. Een staand toilet moet passen bij wat er in je huis zit."),
            ("Kan ik een inbouwreservoir later nog onderhouden?",
             "Ja. Achter de bedieningsplaat zit een opening waardoor je de vlotter en de spoelklep kunt bereiken. Daarom is het slim om een reservoir te kiezen waarvan de onderdelen nog lang te koop zijn."),
            ("Is een randloos toilet echt schoner?",
             "Er is geen holle rand meer waar vuil en kalk zich ophopen, dus je kunt alles zien en bereiken met de borstel. Dat maakt schoonmaken makkelijker."),
        ],
        "bronnen": ["bobex_toilet", "homedeal_toilet", "kiwa_keramiek", "mc_checklist", "aanbod"],
        "verder": [("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer"),
                   ("/kennisbank/kleine-badkamer-indelen/", "Kleine badkamer indelen")],
    },
    {
        "slug": "wastafelmeubel-kiezen",
        "kort": "Wastafelmeubel kiezen",
        "kaart": "Breedte, diepte, materiaal van kast en wastafel: zo kies je een meubel dat jaren meegaat.",
        "h1": "Wastafelmeubel kiezen: maten, materialen en richtprijzen",
        "title": "Wastafelmeubel kiezen: maten en materialen",
        "desc": "Een wastafelmeubel kiezen: welke breedte en diepte passen, welk materiaal kan tegen vocht en wat kost een meubel? Richtprijzen voor de consument, los van de montage.",
        "lead": "Een wastafelmeubel bestaat uit een kast, een wastafel en vaak een spiegel. Juist de kast krijgt het zwaar door vocht en spatwater. Hieronder lees je welke materialen en maten er zijn en wat je ongeveer betaalt.",
        "soorten": [
            ("Zwevend meubel met lades", "Vloer eronder vrij, makkelijk schoonmaken, veel opbergruimte", "Heeft een stevige wand nodig", "De meeste badkamers"),
            ("Staand meubel op pootjes of plint", "Geen zware wandbevestiging nodig", "Lastiger schoonmaken onder en rond het meubel", "Lichte of holle wanden"),
            ("Kast van spaanplaat met melamine", "Goedkoop, veel kleuren en houtdecors", "Zwelt op als water in de randen trekt", "Instap en een tweede badkamer"),
            ("Kast van gelakt MDF", "Strak, naadloos gelakt, goed tegen vocht als de lak heel is", "Beschadigingen in de lak laten vocht door", "Middenklasse"),
            ("Kast van massief hout of fineer", "Warme uitstraling, lang mee bij goed onderhoud", "Duurder, vraagt goede ventilatie", "Wie een natuurlijke look wil"),
            ("Keramische wastafel", "Hard, krasvast, makkelijk schoon", "Breekbaar bij een klap, beperkte vormen", "Dagelijks intensief gebruik"),
            ("Wastafel van mineraalgietsteen of solid surface", "Naadloos, strakke vormen, kleine krassen weg te schuren", "Gevoeliger voor hitte en sterke middelen", "Strakke, moderne badkamers"),
        ],
        "prijs_wat": "kast en wastafel samen, zonder kraan, sifon en spiegel",
        "prijzen": [
            ("Instap", 100, 400, "Meubel van 60 tot 80 cm, spaanplaat met melamine, keramische of kunststof wastafel."),
            ("Midden", 400, 1000, "80 tot 120 cm, gelakt MDF of beter plaatmateriaal, lades met volledige uittrek en zachte sluiting."),
            ("Hoog", 1000, 2500, "Dubbel meubel, massief hout of fineer, solid surface wastafel, maatwerk."),
        ],
        "prijs_noot": "Richtprijs voor het meubel met wastafel, inclusief 21% btw, zonder montage. Slimster noemt vanafprijzen van €150 (basis), €750 (comfort) en €1.500 (luxe); eenvoudige meubels zijn in de bouwmarkt al vanaf ongeveer €100 te koop.",
        "letop": [
            ("Breedte en diepte", "Gangbaar zijn 60, 80, 100 en 120 cm breed. Een gewone diepte is 45 tot 50 cm; voor een kleine badkamer zijn er compacte meubels van 35 tot 40 cm diep. Houd minstens 70 tot 80 cm vrij voor het meubel om je te kunnen bewegen."),
            ("Hoogte", "De bovenkant van de wastafel komt meestal op 85 tot 90 cm. Bij een zwevend meubel kies je die hoogte zelf bij de montage."),
            ("Afvoer en lades", "Een gewone sifon zit in de weg van de bovenste la. Vraag of de lades een uitsparing hebben, of kies een ruimtebesparende sifon."),
            ("Vochtbestendigheid", "Let op de randen: zijn ze rondom afgewerkt met een kantenband of lak? Daar trekt water het eerst in. Goede ventilatie in de badkamer verlengt de levensduur."),
            ("Kraangat en overloop", "Kijk of de wastafel een voorgeboord kraangat heeft, of dat de kraan uit de muur komt. Een wastafel zonder overloop vraagt een afvoerplug die altijd open kan."),
            ("Spiegel en verlichting", "Een spiegelkast met verlichting of een stopcontact vraagt elektra. Laat die aanleggen volgens de NEN 1010; in een badkamer gelden extra regels voor de zones rond douche en bad."),
        ],
        "zelf": ["Het nieuwe meubel op dezelfde plek komt en de aansluitingen passen.",
                 "De wand van steen is, of al versterkt is voor een zwevend meubel.",
                 "Je de kraan en de sifon zelf kunt aansluiten en lekvrij kunt afkitten."],
        "specialist": ["De wateraansluiting of de afvoer moet worden verplaatst.",
                       "Het meubel aan een holle wand komt die eerst versterkt moet worden.",
                       "Er elektra bij komt voor verlichting of een stopcontact.",
                       "Het om een dubbel meubel of maatwerk gaat."],
        "dienst": ("badkamer-installeren", "badkamer installeren"),
        "kosten": ("nieuwe-badkamer", "kosten van een nieuwe badkamer"),
        "faqs": [
            ("Welke breedte wastafelmeubel heb ik nodig?",
             "Voor één persoon is 60 tot 80 cm genoeg. Wil je met twee mensen tegelijk kunnen poetsen, dan heb je minimaal 120 cm met twee kommen nodig."),
            ("Kan een wastafelmeubel tegen vocht?",
             "Een meubel voor de badkamer is erop gemaakt, maar niet waterdicht. Veeg spatwater weg, sluit de randen goed af en zorg voor ventilatie. Beschadigde lak of randen laten vocht door."),
            ("Hoe hoog hang ik een wastafelmeubel?",
             "Meestal komt de bovenkant van de wastafel op 85 tot 90 cm. Lange mensen kiezen soms iets hoger. Kijk ook naar de hoogte van de afvoer in de muur."),
            ("Wat is beter: keramiek of solid surface?",
             "Keramiek is harder en krasvaster. Solid surface en mineraalgietsteen zijn warmer om aan te raken en naadloos, en kleine krassen kun je wegschuren. Beide zijn goed; het is vooral een kwestie van smaak en onderhoud."),
            ("Zit de kraan bij een wastafelmeubel inbegrepen?",
             "Meestal niet. Ook de sifon, de afvoerplug en de spiegel koop je vaak los. Tel die erbij als je prijzen vergelijkt. In onze gids over kranen lees je waar je bij een kraan op let."),
        ],
        "bronnen": ["slimster_meubel", "werkspot_wastafel", "mc_checklist", "aanbod"],
        "verder": [("/kennisbank/badkamer-ventilatie/", "Badkamer ventilatie"),
                   ("/kennisbank/kleine-badkamer-indelen/", "Kleine badkamer indelen")],
    },
    {
        "slug": "kranen-kiezen",
        "kort": "Kranen kiezen",
        "kaart": "Mengkraan, thermostaat of inbouw: verschillen, richtprijzen en het Kiwa-keur uitgelegd.",
        "h1": "Badkamerkranen kiezen: mengkraan, thermostaat of inbouw?",
        "title": "Badkamerkraan kiezen: soorten en richtprijzen",
        "desc": "Welke kraan kies je voor wastafel, douche of bad? Lees de verschillen tussen mengkraan, thermostaatkraan en inbouwkraan, met richtprijzen, Kiwa-keur en tips om zuinig te zijn.",
        "lead": "Een kraan gebruik je elke dag. Een goede kraan loopt soepel, lekt niet en geeft meteen de goede temperatuur. Hieronder zie je welke soorten er zijn, wat ze ongeveer kosten en hoe je een degelijke kraan herkent.",
        "soorten": [
            ("Eenhendel mengkraan", "Temperatuur en hoeveelheid met één hendel, makkelijk te bedienen", "Temperatuur verschuift als elders in huis water wordt getapt", "Wastafel en fontein"),
            ("Tweegreeps kraan", "Klassieke uitstraling", "Lastiger op de goede temperatuur te krijgen, verspilt water", "Klassieke badkamers"),
            ("Thermostaatkraan", "Vaste temperatuur, veilig tegen verbranden dankzij de 38-gradenknop", "Duurder dan een mengkraan", "Douche en bad, zeker met kinderen"),
            ("Inbouwkraan (uit de muur)", "Strak, ruimte op de wastafel of in de douche blijft vrij", "Duurder, het inbouwdeel zit in de muur", "Nieuwe badkamers"),
            ("Kraan met koude middenstand", "In de middenstand komt koud water, zodat de ketel niet onnodig aanslaat", "Even wennen", "Wie energie wil besparen"),
            ("Sensorkraan", "Hygiënisch, gaat vanzelf uit", "Heeft stroom of batterij nodig, duurder", "Gastentoilet of fontein"),
        ],
        "prijs_wat": "een wastafelmengkraan; voor een thermostatische douchekraan staan de prijzen in de tabel eronder",
        "prijzen": [
            ("Instap", 40, 100, "Eenvoudige mengkraan, verchroomd, standaard binnenwerk."),
            ("Midden", 100, 250, "Degelijke mengkraan met keramische binnenwerk, koude middenstand of watersparende perlator, keuze in afwerking."),
            ("Hoog", 250, 600, "Inbouwkraan uit de muur of een designkraan in een bijzondere afwerking."),
        ],
        "prijs_noot": "Richtprijs voor de kraan zelf, inclusief 21% btw, zonder montage. Wastafelkranen op basis van het aanbod bij meerdere bouwmarkten en sanitairwinkels.",
        "prijs_extra": [
            ("Opbouwthermostaat voor de douche", 50, 300, "Werkspot noemt €50 tot €300 voor een thermostaatkraan."),
            ("Inbouwthermostaat (inbouwdeel en afdekset)", 250, 700, "Brede bandbreedte op basis van het aanbod; het inbouwdeel koop je soms los."),
        ],
        "letop": [
            ("Hartafstand", "Een opbouwthermostaat voor douche of bad sluit je aan op twee koppelingen in de muur, meestal 15 cm uit elkaar. Meet dit voordat je koopt. Met S-koppelingen is een paar centimeter verschil op te vangen."),
            ("Uitloop en hoogte", "De straal moet ongeveer in het midden van de wastafel komen. Een hoge kraan op een ondiepe kom spat. Kijk naar de lengte van de uitloop en de hoogte onder de straal."),
            ("Kiwa-keur", "Kiwa certificeert kranen, mengkranen en thermostaatkranen voor de Nederlandse drinkwatereisen (onder meer de beoordelingsrichtlijn BRL-K652). Een kraan met dat keur is getest op materialen die in contact komen met drinkwater."),
            ("Binnenwerk en onderdelen", "Een keramische binnenwerk (cartouche) gaat lang mee. Vraag of losse onderdelen nog jaren leverbaar zijn; dan hoef je bij een lek niet de hele kraan te vervangen."),
            ("Water besparen", "Een perlator of doorstroombegrenzer mengt lucht in de straal en verlaagt het verbruik. Een koude middenstand voorkomt dat de ketel aanslaat voor een korte handwas."),
            ("Afwerking", "Chroom is slijtvast en makkelijk schoon. Mat zwart, goud of geborsteld staal vragen een milder schoonmaakmiddel; kalkaanslag valt er meer op."),
        ],
        "zelf": ["Je een wastafelkraan vervangt op dezelfde wastafel.",
                 "Je een opbouwthermostaat vervangt op bestaande koppelingen met dezelfde hartafstand.",
                 "Je de hoofdkraan kunt dichtdraaien en weet hoe je koppelingen lekvrij afdicht."],
        "specialist": ["Je een inbouwkraan wilt: er moeten sleuven in de muur en het inbouwdeel moet waterdicht worden ingewerkt.",
                       "De leidingen moeten worden verlegd of de hartafstand klopt niet.",
                       "Je twijfelt of de waterdruk en de warmwatervoorziening passen bij de nieuwe kraan."],
        "dienst": ("badkamer-installeren", "badkamer installeren"),
        "kosten": ("uurtarief-loodgieter", "uurtarief van een loodgieter"),
        "faqs": [
            ("Wat is beter: mengkraan of thermostaatkraan?",
             "Voor de wastafel is een mengkraan prima. Voor douche en bad is een thermostaatkraan prettiger en veiliger: hij houdt de temperatuur vast, ook als iemand anders in huis water tapt."),
            ("Waarom moet ik op de hartafstand letten?",
             "Een opbouwthermostaat past alleen op de koppelingen in de muur als de afstand tussen de twee aansluitingen klopt. In Nederland is dat meestal 15 cm."),
            ("Wat betekent het Kiwa-keur op een kraan?",
             "Dat de kraan is getest volgens de Nederlandse eisen voor producten die in contact komen met drinkwater, zoals de beoordelingsrichtlijn BRL-K652. Het zegt iets over materialen en werking, niet over de vormgeving."),
            ("Hoeveel water bespaart een perlator?",
             "Dat hangt af van je huidige kraan. Een perlator of doorstroombegrenzer mengt lucht door het water, waardoor er minder water door de kraan gaat terwijl de straal vol aanvoelt."),
            ("Hoe lang gaat een kraan mee?",
             "Een degelijke kraan gaat vele jaren mee. Lekt hij, dan is vaak alleen het binnenwerk of een rubbertje aan vervanging toe. Dat lukt alleen als die onderdelen nog te koop zijn."),
        ],
        "bronnen": ["werkspot_kraan", "kiwa_kranen", "mc_checklist", "aanbod"],
        "verder": [("/kennisbank/volgorde-badkamerrenovatie/", "Volgorde van een badkamerrenovatie")],
    },
    {
        "slug": "badkamertegels-kopen",
        "kort": "Badkamertegels kopen",
        "kaart": "Keramiek, porcellanato of natuursteen: prijs per m², antislip, formaat en hoeveel je moet bestellen.",
        "h1": "Badkamertegels kopen: soorten, prijs per m² en antislip",
        "title": "Badkamertegels kopen: soorten en prijs per m²",
        "desc": "Badkamertegels kopen? Vergelijk wandtegels, porcellanato, natuursteen en mozaïek. Met richtprijzen per m² voor de tegels zelf, antislipklassen en hoeveel extra je bestelt.",
        "lead": "Tegels bepalen voor een groot deel hoe je badkamer eruitziet, en hoe veilig de vloer is als hij nat is. Hieronder lees je welke soorten er zijn, wat ze per vierkante meter kosten en hoe je de goede hoeveelheid bestelt.",
        "soorten": [
            ("Keramische wandtegel (faience)", "Goedkoop, licht, veel kleuren, makkelijk te snijden", "Alleen voor de wand; zachter en poreuzer", "Wanden buiten en binnen de douche"),
            ("Geglazuurde keramische vloertegel", "Betaalbaar, veel dessins", "Beschadigt de glazuur, dan zie je de andere kleur eronder", "Vloeren met normaal gebruik"),
            ("Porcellanato (gres porcellanato)", "Zeer hard, neemt bijna geen water op, voor wand en vloer", "Zwaarder en lastiger te snijden, vraagt een goede lijm", "Douchevloeren en grote formaten"),
            ("Natuursteen", "Uniek per tegel, lang mee", "Duur, moet geïmpregneerd worden, gevoelig voor zure middelen", "Wie een natuurlijke look wil en onderhoud niet erg vindt"),
            ("Cementtegels", "Bijzondere patronen", "Poreus, vraagt behandeling en onderhoud", "Accentvlakken"),
            ("Mozaïek", "Volgt afschot goed, veel voegen geven grip", "Veel voegen om schoon te houden", "Douchevloer met een put in het midden"),
            ("Grootformaat (60 bij 120 cm en groter)", "Weinig voegen, rustig beeld", "Vraagt een vlakke ondergrond en vakwerk", "Wanden en vloeren met een goot"),
        ],
        "prijs_wat": "de tegels zelf, per vierkante meter",
        "prijs_eenheid": "per m²",
        "prijzen": [
            ("Instap", 10, 25, "Keramische wandtegels en eenvoudige vloertegels in standaardformaten."),
            ("Midden", 25, 60, "Porcellanato in gangbare formaten, ook beton- en houtlook, gerectificeerde randen."),
            ("Hoog", 60, 160, "Grootformaat, natuursteen, cementtegels en bijzondere series."),
        ],
        "prijs_noot": "Richtprijs voor de tegels per m², inclusief 21% btw, zonder lijm, voegmiddel en leggen. Slimster noemt €15 tot €65 per m² voor porcellanato en €9 tot €40 voor faience, Werkspot meestal €20 tot €60 en Homedeal €15 tot €160 per m².",
        "letop": [
            ("Antislip op de douchevloer", "Voor blote voeten bestaat een aparte klasse (A, B of C volgens DIN 51097). Voor een douchevloer is minimaal B gebruikelijk. De bekende R-waarde (R9 tot R13) gaat over lopen met schoenen."),
            ("Waterabsorptie", "Porcellanato neemt minder dan 0,5% water op en kan overal in de badkamer. Faience neemt veel meer op en hoort alleen op de wand. De tegel zelf maakt de badkamer niet waterdicht; dat doet de laag eronder."),
            ("Formaat en afschot", "Een douchevloer loopt af naar de afvoer. Met een goot langs de muur kun je grote tegels gebruiken. Met een put in het midden zijn kleine tegels of mozaïek makkelijker, omdat de vloer naar vier kanten afloopt."),
            ("Hoeveel bestellen", "Bestel 10 tot 15% extra voor snijverlies en breuk, bij visgraat of diagonaal leggen meer. Bewaar een paar tegels voor later herstel."),
            ("Eén partij", "Tegels verschillen per productiepartij in kleur en maat. Kijk op de dozen of partijnummer en kaliber hetzelfde zijn, en bestel alles in één keer."),
            ("Gerectificeerd", "Gerectificeerde tegels zijn na het bakken recht geslepen. Dan kan de voeg smaller, maar de vloer moet wel vlakker zijn. Let bij vloerverwarming op een tegel en lijm die daarvoor geschikt zijn."),
        ],
        "zelf": ["Het om een klein wandvlak buiten de douche gaat.",
                 "Je ervaring hebt met tegels zetten, recht uitzetten en voegen.",
                 "De ondergrond al vlak en droog is."],
        "specialist": ["De douchevloer op afschot moet worden betegeld.",
                       "De douchezone eerst waterdicht moet worden gemaakt.",
                       "Je kiest voor grootformaat, natuursteen of een patroon zoals visgraat.",
                       "De wanden of vloer eerst vlak gemaakt moeten worden."],
        "dienst": ("tegelwerk-badkamer", "tegelwerk in de badkamer"),
        "kosten": ("tegelzetter-per-m2", "kosten van een tegelzetter per m²"),
        "faqs": [
            ("Welke tegels zijn het beste voor een badkamervloer?",
             "Porcellanato is het meest gekozen: hard, slijtvast en het neemt bijna geen water op. Kies voor de douchevloer een tegel met een antislipklasse voor blote voeten, minimaal B."),
            ("Hoeveel tegels moet ik extra bestellen?",
             "Reken op 10 tot 15% extra voor snijverlies en breuk. Leg je in een visgraat of diagonaal, dan heb je meer nodig."),
            ("Mag ik wandtegels op de vloer leggen?",
             "Nee, gewone wandtegels zijn daar niet sterk genoeg voor. Vloertegels mogen vaak wel op de wand, als de lijm en de wand het gewicht aankunnen."),
            ("Zijn grote tegels geschikt voor een kleine badkamer?",
             "Ja, minder voegen geven juist een rustig en ruim beeld. Op een douchevloer met een put in het midden zijn grote tegels wel lastig, omdat de vloer naar vier kanten afloopt."),
            ("Wat kost het leggen van tegels?",
             "Dat staat los van de tegelprijs. Het hangt af van formaat, patroon en de staat van de ondergrond. Op onze kostenpagina over de tegelzetter per m² lees je de richtprijzen."),
        ],
        "bronnen": ["slimster_tegels", "werkspot_tegels", "homedeal_tegels", "mc_checklist"],
        "verder": [("/kennisbank/tegels-kiezen/", "Tegels kiezen"),
                   ("/kennisbank/badkamer-waterdicht-maken/", "Badkamer waterdicht maken"),
                   ("/kennisbank/badkamerstijlen/", "Badkamerstijlen")],
    },
    {
        "slug": "douchesysteem-kiezen",
        "kort": "Douchesysteem kiezen",
        "kaart": "Glijstang, regendouche of inbouw: wat kost het, hoeveel water gebruikt het en past het bij je ketel?",
        "h1": "Douchesysteem kiezen: glijstang, regendouche of inbouw?",
        "title": "Douchesysteem kiezen: soorten en richtprijzen",
        "desc": "Een douchesysteem kiezen: vergelijk glijstangsets, opbouw regendouches en inbouwsystemen. Met richtprijzen, waterverbruik per minuut en waarom je cv-ketel er ook toe doet.",
        "lead": "Een douchesysteem is het geheel van kraan, douchekop en handdouche. De keuze bepaalt je comfort, maar ook hoeveel water en energie je elke dag gebruikt. Hieronder lees je de soorten, de richtprijzen en waar je op let.",
        "soorten": [
            ("Glijstangset met handdouche", "Goedkoop, eenvoudig, handdouche in hoogte verstelbaar", "Minder het gevoel van een regendouche", "Kleine douches en een beperkt budget"),
            ("Opbouw regendoucheset", "Regendouche en handdouche in één, op bestaande koppelingen", "Stang en kraan blijven zichtbaar", "Vervangen zonder hak- en breekwerk"),
            ("Inbouw douchesysteem", "Strak, alleen bedieningsknoppen en douchekop in zicht", "Duurder, het inbouwdeel zit in de muur", "Nieuwe badkamers en inloopdouches"),
            ("Plafonddouche", "Water valt recht naar beneden, ruimtelijk", "Leidingen in het plafond, meer werk", "Ruime douches"),
            ("Douchepaneel of douchezuil", "Alles in één paneel, vaak met extra stralen", "Gebruikt soms veel water, lastig te repareren", "Wie extra functies wil"),
        ],
        "prijs_wat": "het douchesysteem zelf: kraan, stang of inbouwdeel, hoofddouche en handdouche",
        "prijzen": [
            ("Instap", 100, 250, "Glijstangset met thermostaat, of een eenvoudige opbouw regendoucheset met één straalsoort."),
            ("Midden", 250, 500, "Thermostatische opbouw regendoucheset met meerdere straalsoorten en een grotere hoofddouche."),
            ("Hoog", 500, 1500, "Inbouwsysteem met inbouwdeel, thermostaat, wand- of plafondarm en handdouche."),
        ],
        "prijs_noot": "Richtprijs voor het product, inclusief 21% btw, zonder montage. Thermostatische opbouw regendouchesets lagen in november 2026 bij meerdere bouwmarkten tussen ongeveer €200 en €400; Werkspot noemt €50 tot €300 voor alleen een thermostaatkraan. Inbouwsystemen: brede bandbreedte.",
        "letop": [
            ("Waterverbruik", "Milieu Centraal noemt een douchekop waterbesparend bij 4,0 tot 7,2 liter per minuut. Grote regendouches gebruiken vaak meer. Test thuis: houd een emmer een minuut onder de douche. Komt er meer dan ongeveer 7 liter in, dan bespaart een zuinigere kop water en energie."),
            ("Past het bij je cv-ketel?", "Een grote regendouche vraagt veel warm water per minuut. Kijk naar het CW-label van je combiketel: een hoger CW-getal levert meer warm water. Twijfel je, vraag het dan aan je installateur."),
            ("Hartafstand en hoogte", "Een opbouwset sluit je aan op koppelingen met meestal 15 cm hartafstand. Meet ook de hoogte tot het plafond: een stang moet passen en de regendouche moet boven je hoofd komen."),
            ("Inbouwdiepte", "Een inbouwdeel heeft een minimale diepte in de muur. Bij een dunne of holle wand kan dat een voorzetwand vragen."),
            ("Kiwa-keur", "Kiwa test hoofddouches, handdouches en doucheslangen apart (onder meer BRL-K658 voor douches). Kraan en douche met keur zijn getest op werking en drinkwaterveiligheid."),
            ("Kalk", "Kies een douchekop met rubberen nopjes; daar wrijf je kalk eenvoudig af. Dat houdt de straal gelijkmatig."),
        ],
        "zelf": ["Je een opbouwset of glijstangset vervangt op bestaande koppelingen.",
                 "De hartafstand en de hoogte kloppen en je in tegels kunt boren.",
                 "Je alleen een douchekop of slang vervangt."],
        "specialist": ["Je een inbouwsysteem of plafonddouche wilt.",
                       "Er nieuwe leidingen in muur of plafond moeten komen.",
                       "Het inbouwdeel waterdicht moet worden ingewerkt in de douchewand.",
                       "Je twijfelt of de warmwatervoorziening het systeem aankan."],
        "dienst": ("badkamer-installeren", "badkamer installeren"),
        "kosten": ("uurtarief-loodgieter", "uurtarief van een loodgieter"),
        "faqs": [
            ("Gebruikt een regendouche meer water?",
             "Vaak wel, omdat de kop groter is. Er zijn ook zuinige regendouches. Kijk naar het aantal liters per minuut; Milieu Centraal noemt tot 7,2 liter per minuut waterbesparend."),
            ("Wat is beter: opbouw of inbouw?",
             "Opbouw is goedkoper en kun je vaak zelf vervangen. Inbouw is strakker en makkelijker schoon te houden, maar het inbouwdeel zit in de muur en de montage is vakwerk. Bij een complete renovatie kiezen veel mensen inbouw."),
            ("Welke maat regendouche moet ik nemen?",
             "Een hoofddouche van 20 tot 30 cm is gangbaar. Hoe groter, hoe meer water er nodig is voor een volle straal. In een kleine douche is 20 tot 25 cm vaak genoeg."),
            ("Kan mijn cv-ketel een regendouche aan?",
             "Dat hangt af van de warmwatercapaciteit, te zien aan het CW-label van een combiketel. Met een lage klasse wordt een grote regendouche snel lauw. Vraag het na bij je installateur."),
            ("Wat is een douche-wtw?",
             "Een warmteterugwinsysteem dat de warmte uit het afvoerwater gebruikt om het koude water voor te verwarmen. Het past het best bij een verbouwing, omdat de afvoer ervoor aangepast moet worden. Milieu Centraal noemt het in de verbouwingschecklist voor de badkamer."),
        ],
        "bronnen": ["mc_douchekop", "mc_checklist", "werkspot_kraan", "kiwa_kranen", "cbs_douche", "aanbod"],
        "verder": [("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel")],
    },
    {
        "slug": "bad-of-douche",
        "kort": "Bad of douche?",
        "kaart": "Ruimte, gebruik, water en budget naast elkaar, met richtprijzen voor inbouwbaden en vrijstaande baden.",
        "h1": "Bad of douche? Zo maak je de keuze",
        "title": "Bad of douche? Ruimte, kosten en waterverbruik",
        "desc": "Bad of douche, of allebei? Vergelijk ruimte, gebruik, waterverbruik en kosten. Met richtprijzen voor een inbouwbad en een vrijstaand bad, en wat er bij de montage komt kijken.",
        "lead": "Een bad neemt veel ruimte in en wordt in veel huizen weinig gebruikt. Toch is het voor sommige gezinnen onmisbaar. Hieronder zetten we de opties naast elkaar, met de ruimte die je nodig hebt, het waterverbruik en de richtprijzen.",
        "soorten": [
            ("Alleen een inloopdouche", "Ruim, gelijkvloers mogelijk, zuinig", "Geen bad voor kinderen of om te ontspannen", "Kleine badkamers, ouder worden in huis"),
            ("Inbouwbad met douchescherm", "Bad en douche op één plek, ruimtebesparend", "Over de rand stappen om te douchen", "Badkamers van rond 2 bij 2 meter met kinderen"),
            ("Apart bad en aparte douche", "Het comfort van allebei", "Vraagt veel ruimte en is duurder", "Grote badkamers"),
            ("Vrijstaand bad", "Opvallend middelpunt, ruim gevoel", "Duur, leidingen in de vloer, ruimte rondom nodig", "Grote badkamers en een ruim budget"),
            ("Kort of compact bad", "Past in een kleinere ruimte", "Minder ver kunnen liggen", "Kleine badkamers met kinderen"),
        ],
        "prijs_wat": "het bad zelf, zonder kraan, afvoer, ombouw en plaatsing",
        "prijzen": [
            ("Instap", 150, 400, "Acryl inbouwbad in een standaardmaat, bijvoorbeeld 170 bij 75 cm."),
            ("Midden", 400, 1000, "Groter acryl duobad, staal-emaille inbouwbad of een eenvoudig vrijstaand bad."),
            ("Hoog", 1000, 3000, "Vrijstaand bad van solid surface of gietijzer, of een bad met bubbelsysteem."),
        ],
        "prijs_noot": "Richtprijs voor het bad, inclusief 21% btw, zonder plaatsing. Slimster noemt voor een vrijstaand bad vanafprijzen van €300 (basis), €900 (comfort) en €2.000 (luxe); Homedeal noemt gemiddeld €1.850 voor een gietijzeren bad. Inbouwbaden: brede bandbreedte op basis van dezelfde bronnen en het aanbod.",
        "letop": [
            ("Ruimte", "Een standaard inbouwbad is 170 bij 75 cm, maar 160 tot 180 cm lang en 70 tot 80 cm breed komt veel voor. Een vrijstaand bad heeft daarnaast ruimte rondom nodig om schoon te maken. Een douche kan vanaf 80 bij 80 cm; 90 bij 120 cm is ruim."),
            ("Water en energie", "Een gevuld bad bevat al snel 120 liter. Een douchebeurt van vijf minuten met een waterbesparende douchekop (tot 7,2 liter per minuut) kost zo'n 36 liter. Het opwarmen van het water is de grootste kostenpost."),
            ("Draagkracht van de vloer", "Een groot gevuld bad weegt al snel een paar honderd kilo, een gietijzeren bad nog meer. Laat bij een houten vloer de draagkracht controleren."),
            ("Warm water", "Een groot bad vul je alleen snel als de ketel of boiler genoeg warm water levert. Kijk naar het CW-label of de inhoud van de boiler."),
            ("Materiaal", "Acryl is licht, warm en goedkoop, maar krast sneller. Staal-emaille is krasvast maar koeler. Gietijzer houdt de warmte goed vast, maar is zwaar en duur."),
            ("Later in huis", "Wil je lang in je huis blijven wonen, dan is een drempelloze douche makkelijker dan over een badrand stappen."),
        ],
        "zelf": ["Bijna nooit: een bad vraagt afvoer, ombouw, waterdicht afwerken en kitten.",
                 "Alleen een kraan op een bestaand bad vervangen kan een handige klusser zelf."],
        "specialist": ["Je een bad plaatst of vervangt; ook als de aansluitingen al op de goede plek zitten.",
                       "Er een vrijstaand bad komt met leidingen en afvoer in de vloer.",
                       "Je het bad vervangt door een inloopdouche: de vloer, afvoer en waterdichting veranderen.",
                       "De vloer versterkt moet worden voor een zwaar bad."],
        "dienst": ("badkamer-renoveren", "badkamer renoveren"),
        "kosten": ("nieuwe-badkamer", "kosten van een nieuwe badkamer"),
        "faqs": [
            ("Is douchen goedkoper dan in bad gaan?",
             "Meestal wel. Een bad bevat al snel 120 liter. Een douchebeurt van vijf minuten met een waterbesparende kop kost zo'n 36 liter. Pas bij heel lang douchen kom je in de buurt van een bad."),
            ("Hoeveel ruimte heb je nodig voor een bad?",
             "Een standaard inbouwbad is 170 bij 75 cm. Daarnaast heb je ruimte nodig om erin en eruit te stappen. Een vrijstaand bad vraagt aan alle kanten wat ruimte om bij te kunnen."),
            ("Is een bad goed voor de verkoop van mijn huis?",
             "Dat verschilt per koper. Gezinnen met jonge kinderen zoeken soms een bad, anderen kiezen liever een ruime douche. Harde cijfers over meer of minder waarde zijn er niet. Kies vooral wat bij je eigen gebruik past."),
            ("Kan ik een bad vervangen door een inloopdouche?",
             "Ja, dat gebeurt veel. Er komt meer bij kijken dan het bad weghalen: de afvoer, de vloer, de waterdichting en het tegelwerk veranderen."),
            ("Wat kost een vrijstaand bad met plaatsing?",
             "De plaatsing is duurder dan bij een inbouwbad, omdat de leidingen en afvoer in de vloer moeten. Op onze kostenpagina voor een nieuwe badkamer zie je hoe de kosten zijn opgebouwd."),
        ],
        "bronnen": ["slimster_vrijstaand", "slimster_bad", "homedeal_bad", "bobex_bad", "mc_douchekop", "cbs_douche"],
        "verder": [("/kennisbank/kleine-badkamer-indelen/", "Kleine badkamer indelen"),
                   ("/kennisbank/inloopdouche-zonder-drempel/", "Inloopdouche zonder drempel")],
    },
]

LINKS = [(BASIS, "Badkamerspullen", "Neutrale kopersgidsen met richtprijzen voor sanitair en materialen.")] + [
    (f"{BASIS}{g['slug']}/", g["kort"], g["kaart"]) for g in GIDSEN
]

# ---------------------------------------------------------------------------
# Eigen CSS (voorvoegsel .bs-)
# ---------------------------------------------------------------------------
CSS = """<style>
.bs-ill{margin:0;background:var(--bg-soft);border:1px solid var(--line);border-radius:var(--radius-lg);padding:22px;color:var(--navy);text-align:center}
.bs-ill figcaption{font-size:.85rem;color:var(--muted);margin-top:10px}
.bs-svg{width:100%;max-width:380px;height:auto;display:block;margin:0 auto}
.bs-svg .bs-vlak{fill:var(--accent-soft);stroke:var(--accent)}
.bs-svg .bs-glas{fill:rgba(36,96,107,.08)}
.bs-svg .bs-dun{stroke-width:1.4;opacity:.7}
.bs-svg .bs-stippel{stroke-dasharray:4 4;opacity:.7}
.bs-ill-klein{padding:12px;margin-bottom:14px;border-radius:var(--radius)}
.bs-ill-klein .bs-svg{max-width:200px}
.bs-kaart{display:flex;flex-direction:column}
.bs-kaart .go{margin-top:auto}
.bs-noot{font-size:.9rem;color:var(--muted)}
.bs-tabel td:first-child{font-weight:650;color:var(--ink);min-width:150px}
.bs-tabel td{vertical-align:top}
.bs-montage{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:18px 0}
.bs-montage .card h3{display:flex;gap:10px;align-items:center}
.bs-montage ul{margin:0;padding-left:20px}
.bs-montage li{margin-bottom:.5em;font-size:.95rem}
.bs-bronnen{font-size:.9rem}
.bs-bronnen li{margin-bottom:.4em}
.bs-letop{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:18px}
.bs-letop .card h3{font-size:1.05rem}
.bs-uitleg{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:22px 0}
.bs-uitleg .card p{margin:0}
@media(max-width:760px){.bs-montage,.bs-letop,.bs-uitleg{grid-template-columns:1fr}}
@media(max-width:640px){.bs-stapel thead{display:none}.bs-stapel tr{display:block;border-bottom:1px solid var(--line);padding:12px 0}
.bs-stapel td{display:block;border:0;padding:4px 14px}.bs-stapel td:first-child{font-size:1.02rem;padding-bottom:6px}
.bs-stapel td[data-kop]::before{content:attr(data-kop) ": ";font-weight:700;color:var(--ink)}}
</style>"""

# ---------------------------------------------------------------------------
# Opbouw van de pagina's
# ---------------------------------------------------------------------------


def _bronnen_html(sleutels):
    items = ""
    for k in sleutels:
        naam, url = B[k]
        items += f'<li><a href="{url}" rel="noopener nofollow">{naam}</a></li>' if url else f"<li>{naam}</li>"
    return f'<ol class="bs-bronnen">{items}</ol>'


def _soorten_tabel(rijen, kop1="Soort"):
    body = "".join(f'<tr><td>{a}</td><td data-kop="Voordelen">{b}</td><td data-kop="Nadelen">{c}</td>'
                   f'<td data-kop="Past bij">{d}</td></tr>' for a, b, c, d in rijen)
    return (f'<div class="tablewrap"><table class="bs-tabel bs-stapel"><thead><tr><th>{kop1}</th><th>Voordelen</th>'
            f'<th>Nadelen</th><th>Past bij</th></tr></thead><tbody>{body}</tbody></table></div>')


def _prijs_tabel(rijen, eenheid, kop="Prijsklasse"):
    body = "".join(f'<tr><td>{k}</td><td class="num">{eur(v)} – {eur(t)}{(" " + eenheid) if eenheid else ""}</td><td>{w}</td></tr>'
                   for k, v, t, w in rijen)
    return (f'<div class="tablewrap"><table class="bs-tabel"><thead><tr><th>{kop}</th><th>Richtprijs</th>'
            f'<th>Wat je krijgt</th></tr></thead><tbody>{body}</tbody></table></div>')


def _andere_gidsen(huidig):
    kaarten = "".join(
        f'<a class="card bs-kaart reveal" href="{BASIS}{g["slug"]}/">{illustratie(g["slug"], klein=True)}'
        f'<h3>{g["kort"]}</h3><span class="go">Lees de gids →</span></a>'
        for g in GIDSEN if g["slug"] != huidig)
    return f'<div class="grid g3">{kaarten}</div>'


def gids_body(g):
    cr, cr_ld = crumbs([("Home", "/"), ("Badkamerspullen", BASIS), (g["kort"], None)])
    eenheid = g.get("prijs_eenheid", "")
    laag, hoog = g["prijzen"][0][1], g["prijzen"][-1][2]
    d_slug, d_naam = g["dienst"]
    k_slug, k_naam = g["kosten"]

    hero = f"""<section class="section-sm"><div class="wrap">
  <div class="grid g2" style="gap:44px;align-items:center">
    <div>
      <span class="badge">Kopersgids · richtprijzen {JAAR}</span>
      <h1>{g['h1']}</h1>
      <p class="lead">{g['lead']}</p>
      <div class="callout callout-prijs">
        <p><strong>Richtprijs voor het product:</strong> {eur(laag)} – {eur(hoog)}{(' ' + eenheid) if eenheid else ''}, voor {g['prijs_wat']}. Inclusief btw, los van de montage.</p>
        <p style="font-size:.93rem;margin-top:8px">Wij verkopen niets en krijgen geen commissie. Deze gids noemt geen merken of winkels.</p>
      </div>
    </div>
    <div>{illustratie(g['slug'])}</div>
  </div>
</div></section>"""

    soorten = f"""<section class="section soft"><div class="wrap">
  <div class="narrow prose" style="margin:0 auto 18px"><h2>Welke soorten zijn er?</h2>
  <p>De belangrijkste soorten en varianten naast elkaar, met wat ze goed doen en waar ze minder sterk in zijn.</p></div>
  {_soorten_tabel(g['soorten'], "Soort of variant")}
</div></section>"""

    extra = ""
    if g.get("prijs_extra"):
        extra = ("<h3>Thermostaatkranen voor douche en bad</h3>"
                 + _prijs_tabel(g["prijs_extra"], "", "Soort"))
    midden = cta_midden("Wil je weten wat het geplaatst kost?",
                        f'Lees de opbouw op onze pagina over de <a href="/kosten/{k_slug}/">{k_naam}</a>, '
                        "of vraag offertes aan bij maximaal drie badkamerspecialisten.")
    prijzen = f"""<section class="section"><div class="wrap narrow prose">
  <h2>Wat kost het? Richtprijzen per prijsklasse</h2>
  <p>De bedragen hieronder gaan over {g['prijs_wat']}. Montage, leidingwerk en bijkomende materialen komen erbij.</p>
  {prijs_balken([(k, v, t) for k, v, t, _ in g['prijzen']], f"Richtprijs product{(' ' + eenheid) if eenheid else ''}, inclusief btw")}
  {_prijs_tabel(g['prijzen'], eenheid)}
  {extra}
  <p class="bs-noot">{g['prijs_noot']} Prijzen wisselen per winkel en per actie; gebruik ze om te zien of een prijs in de buurt zit.</p>
  {midden}
</div></section>"""

    letop_kaarten = "".join(f'<div class="card"><h3>{k}</h3><p>{t}</p></div>' for k, t in g["letop"])
    letop = f"""<section class="section soft"><div class="wrap">
  <div class="narrow prose" style="margin:0 auto"><h2>Waar let je op bij het kopen?</h2>
  <p>Maten, materialen en keurmerken die het verschil maken tussen een aankoop waar je jaren plezier van hebt en een die snel tegenvalt.</p></div>
  <div class="bs-letop">{letop_kaarten}</div>
</div></section>"""

    zelf = "".join(f"<li>{x}</li>" for x in g["zelf"])
    spec = "".join(f"<li>{x}</li>" for x in g["specialist"])
    montage = f"""<section class="section"><div class="wrap narrow prose">
  <h2>Montage: zelf doen of een specialist?</h2>
  <p>De prijs van het product is maar een deel van het verhaal. Hoeveel werk de montage is, hangt vooral af van wat er aan leidingen, afvoer en ondergrond moet veranderen.</p>
  <div class="bs-montage">
    <div class="card"><h3>{icon('check', 20)} Zelf doen kan als</h3><ul>{zelf}</ul></div>
    <div class="card"><h3>{icon('check', 20)} Een specialist is verstandig als</h3><ul>{spec}</ul></div>
  </div>
  <p>Meer over het werk lees je op onze pagina over <a href="/diensten/{d_slug}/">{d_naam}</a>. Wat de montage kost, staat bij de <a href="/kosten/{k_slug}/">{k_naam}</a>. Laat je het product door het bedrijf leveren, dan geldt de garantie meestal voor product en montage samen; koop je zelf, spreek dat dan vooraf af.</p>
</div></section>"""

    faq_html, faq_ld = faq_blok(g["faqs"], f"Veelgestelde vragen: {g['kort'].lower().rstrip('?')}")

    verder = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in g.get("verder", []))
    verder_html = f"<h3>Verder lezen</h3><ul>{verder}</ul>" if verder else ""
    bronnen = f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Bronnen</h2>
  <p>De richtprijzen zijn bandbreedtes uit kostenartikelen en vergelijkers, gecontroleerd in november 2026. Het zijn geen offertes en geen prijzen van één winkel.</p>
  {_bronnen_html(g['bronnen'])}
  {verder_html}
</div></section>"""

    andere = f"""<section class="section"><div class="wrap">
  <h2>Andere kopersgidsen</h2>
  {_andere_gidsen(g['slug'])}
</div></section>"""

    body = (CSS + cr + hero + soorten + prijzen + letop + montage + faq_html + bronnen + andere
            + cta_blok("Liever meteen een prijs inclusief montage?",
                       "Vul in een minuut het formulier in en ontvang vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio."))
    return body, [cr_ld, faq_ld]


def index_body():
    cr, cr_ld = crumbs([("Home", "/"), ("Badkamerspullen", None)])
    kaarten = "".join(
        f'<a class="card bs-kaart reveal" href="{BASIS}{g["slug"]}/">{illustratie(g["slug"], klein=True)}'
        f'<h3>{g["kort"]}</h3><p>{g["kaart"]}</p>'
        f'<p class="price">Richtprijs {eur(g["prijzen"][0][1])} – {eur(g["prijzen"][-1][2])}{(" " + g["prijs_eenheid"]) if g.get("prijs_eenheid") else ""}</p>'
        f'<span class="go">Lees de gids →</span></a>'
        for g in GIDSEN)
    item_ld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Kopersgidsen badkamerspullen",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": g["kort"], "url": f"{BASIS}{g['slug']}/"}
            for i, g in enumerate(GIDSEN)
        ],
    }
    body = f"""{CSS}{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Kopersgidsen · richtprijzen {JAAR}</span>
  <h1>Badkamerspullen kiezen: neutrale kopersgidsen</h1>
  <p class="lead">Een nieuwe douche, toilet, kraan of tegels uitzoeken? In deze gidsen lees je welke soorten er zijn, wat ze ongeveer kosten en waar je op let. Zonder merken aan te prijzen.</p>
</div>
<div class="wrap">
  <div class="bs-uitleg">
    <div class="card"><h3>Wij verkopen niets</h3><p>Top Badkamers is geen winkel. We krijgen geen commissie en plaatsen geen links naar webwinkels.</p></div>
    <div class="card"><h3>Richtprijzen</h3><p>De prijzen zijn richtprijzen voor de consument, inclusief btw, voor het product zelf en los van de montage.</p></div>
    <div class="card"><h3>Met bronnen</h3><p>Elke gids noemt zijn bronnen, zoals kostenartikelen, Milieu Centraal en Kiwa.</p></div>
  </div>
</div></section>
<section class="section soft"><div class="wrap">
  <h2>De gidsen</h2>
  <div class="grid g3">{kaarten}</div>
</div></section>
<section class="section"><div class="wrap narrow prose">
  <h2>Hoe komen de richtprijzen tot stand?</h2>
  <p>We gebruiken bandbreedtes uit kostenartikelen en prijsvergelijkers, en waar die ontbreken het aanbod van meerdere winkels samen. Nooit de prijs van één winkel. Per gids verdelen we die bandbreedte in drie klassen: instap, midden en hoog. Acties en prijzen wisselen, dus zie de bedragen als richting en niet als offerte.</p>
  <h2>Product en montage zijn twee dingen</h2>
  <p>Een douchewand van een paar honderd euro kan geplaatst een veelvoud kosten, omdat de vloer, de afvoer, het waterdicht maken en het tegelwerk meetellen. Wat het werk kost, lees je bij <a href="/prijzen/">onze prijzen</a> en per klus op <a href="/kosten/">de kostenpagina's</a>. Wil je weten wat het in jouw badkamer kost, <a href="/offerte-aanvragen/">vraag dan offertes aan</a> bij maximaal drie badkamerspecialisten.</p>
</div></section>
{cta_blok("Een prijs voor jouw badkamer?", "Vergelijk gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio, inclusief montage.")}"""
    return body, [cr_ld, item_ld]


def build(write):
    body, ld = index_body()
    write(BASIS, page(
        title("Badkamerspullen kiezen: kopersgidsen en richtprijzen", limit=62),
        "Neutrale kopersgidsen voor douche, toilet, wastafelmeubel, kranen, tegels en bad. Met richtprijzen voor de consument, zonder merken en zonder commissie.",
        BASIS, body, ld), prio=0.7)
    for g in GIDSEN:
        body, ld = gids_body(g)
        write(f"{BASIS}{g['slug']}/", page(title(g["title"], limit=62), g["desc"], f"{BASIS}{g['slug']}/", body, ld), prio=0.6)
