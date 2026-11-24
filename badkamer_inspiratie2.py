# -*- coding: utf-8 -*-
"""Badkamerinspiratie, ronde 3: zes extra stijlpagina's op /inspiratie/<slug>/.

Stijlen: scandinavisch, luxe, marmer, zwart-wit, terrazzo en wellness. Elke stijl heeft twee eigen
3D-illustraties (renders/b4-*.html, metadata in render_stijl_data2.py): een overzicht en een detail.
Opbouw zoals badkamer_inspiratie.py: sfeer, kenmerken, materialen als stalen, kleurpalet, kosten met
bronnen, tips, valkuilen, FAQ en CTA. De CSS (klassen .bi-) komt uit badkamer_inspiratie.py; eigen
aanvullingen hebben het voorvoegsel .bi2-.

Prijzen: alleen uit richtprijzen.py (RP), zodat de bedragen gelijk zijn aan de kostenpagina's en de
calculator. Er staan hier geen nieuwe bedragen in. De totaalprijs per badkamer (basis / midden / luxe)
komt uit badkamer_inspiratie.NIVEAUS, met dezelfde bronnen (Homedeal, Trustoo, Slimster, november 2026).
Alle bedragen zijn richtprijzen inclusief 21% btw.
"""

import datetime
import html as htmllib

import richtprijzen as RP
from components import page, crumbs, title, faq_blok, cta_blok, cta_midden, prijs_balken, offertecheck_blok
from data import SITE
from render_stijl_data2 import RENDERS_STIJL2
from badkamer_inspiratie import CSS as BI_CSS, BRONNEN_KOSTEN, NIVEAUS, GIDSEN, KENNIS

PAD = "/inspiratie/"
GEPUBLICEERD = "2026-11-23"


def _rp(sleutel, niveau=None):
    """Tekst 'van € x tot € y per ...' uit richtprijzen.py."""
    p = RP.RICHTPRIJZEN[sleutel]
    lo, hi = (p["niveaus"][niveau] if niveau else (p["laag"], p["hoog"]))
    eenh = RP.EENHEID_TEKST.get(p["eenheid"], "")
    f = lambda v: f"€{v:,.0f}".replace(",", ".")
    return f"{f(lo)} – {f(hi)} {eenh}".strip()


# ---------------------------------------------------------------------------
# Stijlen. kosten_posten: (onderdeel, RP-sleutel, niveau of None, waarom bij deze stijl)
# materialen: (naam, uitleg, css-achtergrond van het staal). kleuren: (naam, hex, waar)
# ---------------------------------------------------------------------------

STIJLEN = [
    dict(
        slug="scandinavische-badkamer", naam="Scandinavische badkamer", kort="Scandinavisch",
        h1="Scandinavische badkamer: licht, eenvoudig en warm",
        seo="Scandinavische badkamer: kenmerken, kleuren en tips",
        description="Een Scandinavische badkamer is licht en eenvoudig: wit, licht hout en zachte grijsblauwe tinten. Met materialen, kleuren, kosten en tips voor een rustige badkamer.",
        intro="Een Scandinavische badkamer voelt licht en opgeruimd, maar niet kil. Wit en licht hout vormen de basis, met zachte grijsblauwe en lichtgrijze tinten. In de illustratie zie je staande witte tegels tot halverwege de wand, een vloer in licht eiken houtlook en een eiken meubel met een ronde kom.",
        sfeer="De stijl komt uit landen met lange, donkere winters. Daar wil je zoveel mogelijk licht binnen houden. Daarom zie je veel wit, matte oppervlakken die het licht zacht verspreiden en hout dat warmte geeft. Alles heeft een functie: een ladderrek voor de handdoeken, een nis in de douche en één lade in het meubel. Het resultaat is een badkamer waar je 's ochtends rustig wakker wordt.",
        kenmerken=[
            "Een lichte basis: wit of gebroken wit op de wanden, vaak met een zachte grijsblauwe verf erboven.",
            "Licht hout, zoals eiken of essen, voor het meubel, een rek of een krukje.",
            "Staande of liggende smalle tegels (bijvoorbeeld 7,5 × 30 cm) die de wand wat ritme geven.",
            "Een houten vloer of een keramische tegel in houtlook, ook in de douche.",
            "Eenvoudige vormen: een ronde spiegel, een ronde opzetkom en een kraan in geborsteld staal of mat wit.",
            "Textiel en planten in rustige kleuren: lichtgrijs, grijsblauw en salie.",
        ],
        materialen=[
            ("Witte staande tegel 7,5 × 30", "Smalle tegel in warm wit, rechtop gelegd. Het ritme van de voegen maakt een witte wand minder vlak.",
             "repeating-linear-gradient(90deg,#f5f4f0 0 10px,#e2e0db 10px 11px)"),
            ("Houtlook vloertegel", "Keramische tegel van 20 × 120 cm met een eikennerf. Waterdicht en geschikt voor vloerverwarming.",
             "repeating-linear-gradient(0deg,#d4b48c 0 14px,#c6a47b 14px 15px,#dcbe98 15px 29px,#a88d70 29px 30px)"),
            ("Licht eiken", "Fineer of massief eiken met een matte lak. Voor het meubel, de spiegelrand en een ladderrek.",
             "repeating-linear-gradient(90deg,#d9b88f 0 5px,#c9a57a 5px 6px,#e0c29b 6px 11px)"),
            ("Grijsblauwe verf", "Vochtbestendige muurverf boven de tegels. Koel genoeg om fris te blijven, zacht genoeg om niet kil te zijn.",
             "radial-gradient(circle at 30% 30%,#e3e8eb 0 30%,transparent 60%),#d9e0e3"),
            ("Geborsteld rvs", "Kranen en douche in geborsteld staal laten minder vlekken zien dan glanzend chroom.",
             "linear-gradient(135deg,#e4e6e8,#b9bcbf 50%,#d7d9db)"),
        ],
        kleuren=[("Warm wit", "#f5f4f0", "wandtegels"), ("Grijsblauw", "#d9e0e3", "wand boven de tegels"),
                 ("Licht eiken", "#d4b48c", "vloer en meubel"), ("Rvs", "#c9cccf", "kranen"),
                 ("Duifblauw", "#9fb1bd", "textiel")],
        kosten_posten=[
            ("Wandtegels in de middenklasse", "tegels", "midden", "Witte keramische tegels zijn betaalbaar. Smalle tegels geven wel meer voegwerk."),
            ("Tegels zetten", "tegelwerk", None, "Smalle staande tegels vragen meer tijd per m² dan grote tegels."),
            ("Wastafelmeubel", "sanitair_meubel", "midden", "Een eiken meubel met opzetkom en kraan."),
            ("Elektrische vloerverwarming", "vloerverwarming_elektrisch", None, "Een houtlook-vloer voelt pas echt warm met vloerverwarming eronder."),
        ],
        kosten="Een Scandinavische badkamer hoeft niet duur te zijn. Witte tegels en een eenvoudig meubel vallen meestal in het basis- of middensegment. Wat het duurder maakt: smalle tegels (meer voegwerk), echt hout in plaats van houtlook, en vloerverwarming onder de houtlook-vloer.",
        tips=[
            "Kies gebroken wit in plaats van helder wit. Dat oogt zachter, vooral bij noorderlicht.",
            "Houd het hout overal in dezelfde tint: vloer, meubel en rek. Drie soorten hout naast elkaar is onrustig.",
            "Een ladderrek of haakjes aan de wand zijn praktisch en passen bij de stijl. Dan heb je minder kasten nodig.",
            "Gebruik licht van 2700 tot 3000 kelvin. Dan blijft het wit warm in plaats van blauw.",
        ],
        valkuilen=[
            "Alleen wit en grijs wordt snel kil. Voeg hout, textiel en een plant toe.",
            "Echt hout in de douche vraagt veel onderhoud. Kies daar een tegel in houtlook.",
            "Lichte voegen worden in de douche snel grauw. Kies een voeg die een tint donkerder is dan de tegel.",
        ],
        faq=[
            ("Wat is typisch voor een Scandinavische badkamer?", "Een lichte basis in wit en grijs, licht hout, eenvoudige vormen en weinig spullen in zicht. Textiel in zachte tinten en een plant maken het af."),
            ("Kan ik een houten vloer in de badkamer leggen?", "Echt hout kan, maar het vraagt een geschikte houtsoort, een goede afwerking en ventilatie. Een keramische tegel in houtlook geeft bijna hetzelfde beeld en kan ook in de douche."),
            ("Welke kraan past bij een Scandinavische badkamer?", "Een eenvoudige kraan in geborsteld rvs, chroom of mat wit. Mat zwart kan ook, als accent bij veel wit en hout."),
            ("Is een Scandinavische badkamer geschikt voor een kleine ruimte?", "Ja. Lichte kleuren en een zwevend meubel laten een kleine badkamer groter lijken."),
        ],
        gidsen=["wastafelmeubel-kiezen", "badkamertegels-kopen", "kranen-kiezen"],
        kennis=["tegels-kiezen", "kleine-badkamer-indelen", "badkamerstijlen"],
    ),
    dict(
        slug="luxe-badkamer", naam="Luxe badkamer", kort="Luxe",
        h1="Luxe badkamer: ruimte, natuursteen en warm licht",
        seo="Luxe badkamer: inspiratie, materialen en kosten",
        description="Een luxe badkamer draait om ruimte, mooie materialen en goed licht: een marmeren wand, een vrijstaand bad, een dubbel meubel. Met kosten, tips en valkuilen.",
        intro="Een luxe badkamer voelt als een hotelkamer waar je niet weg wilt. Het zit niet in goud alleen, maar in ruimte, goede materialen en licht dat klopt. In de illustratie zie je een badkamer van 4 bij 4,2 meter met een wand van warm geaderd marmer, een dubbel meubel, een vrijstaand bad en een ruime inloopdouche.",
        sfeer="Luxe is vooral rust en comfort. Een dubbel meubel betekent 's ochtends geen wachtrij. Een ruime inloopdouche zonder drempel en met een grote regendouche voelt als een spa. Een vrijstaand bad onder het raam is de plek om op zondag te ontspannen. Wandlampjes naast de spiegels geven zacht licht op je gezicht, en spots aan het plafond zijn dimbaar. Eén bijzonder materiaal, zoals een wand van marmer, maakt het af.",
        kenmerken=[
            "Ruimte: een dubbel meubel, een inloopdouche van minstens 120 cm breed en vrije loopruimte.",
            "Eén bijzonder materiaal als blikvanger, bijvoorbeeld een wand van marmer of grote keramische platen in marmerlook.",
            "Een vrijstaand bad, als de vloer het gewicht kan dragen en de afvoer op de juiste plek kan komen.",
            "Licht in lagen: dimbare spots, wandlampjes bij de spiegel en ledlicht onder het meubel.",
            "Kranen en details in één warme kleur, zoals goud, messing of brons.",
            "Comfort dat je niet ziet: vloerverwarming, een handdoekradiator en goede ventilatie.",
        ],
        materialen=[
            ("Marmer of marmerlook met warme aders", "Grote platen met goudbruine aders (calacatta-look). Als keramische plaat is het waterdicht en makkelijk te onderhouden.",
             "linear-gradient(115deg,transparent 0 40%,rgba(150,120,85,.55) 41%,transparent 43%),linear-gradient(70deg,transparent 0 62%,rgba(150,120,85,.35) 63%,transparent 64%),#f3f0ea"),
            ("Grote lichte vloertegel 120 × 120", "Weinig voegen, dus de vloer oogt als één vlak. Vraagt een zeer vlakke ondergrond.",
             "linear-gradient(90deg,#dcd6cc 0 49%,#c9c2b6 49% 51%,#dcd6cc 51%)"),
            ("Donker eiken", "Een dubbel meubel in gerookt of donker gebeitst eiken geeft diepte naast het lichte marmer.",
             "repeating-linear-gradient(90deg,#5e4433 0 5px,#4e3829 5px 6px,#6a4d3a 6px 11px)"),
            ("Goud geborsteld", "Kranen, douche, spiegelranden en wandlampjes in één kleur.",
             "linear-gradient(135deg,#f0d491,#b8913f 50%,#e3c27a)"),
            ("Warme greige verf", "Rustige vochtbestendige verf op de wanden zonder marmer, zodat de blikvanger niet gaat vechten.",
             "radial-gradient(circle at 30% 30%,#e3dbd0 0 30%,transparent 60%),#d9d0c4"),
        ],
        kleuren=[("Calacatta-wit", "#f3f0ea", "marmeren wand"), ("Goudbruin", "#96785a", "aders"),
                 ("Greige", "#d9d0c4", "wanden en vloer"), ("Donker eiken", "#5e4433", "meubel"),
                 ("Goud", "#d9b26a", "kranen en lampen")],
        kosten_posten=[
            ("Tegels in het luxe segment", "tegels", "luxe", "Grote platen in marmerlook. Echt marmer ligt meestal hoger."),
            ("Vrijstaand bad met kraan", "sanitair_bad", "luxe", "Een vrijstaand bad met een staande badkraan."),
            ("Inloopdouche met regendouche", "sanitair_douche", "luxe", "Douchegoot, grote glazen wand en thermostaat met regendouche."),
            ("Wastafelmeubel (per meubel)", "sanitair_meubel", "luxe", "Een dubbel meubel met twee kommen kost meer dan één meubel."),
            ("Elektra en verlichting", "elektra", None, "Wandlampjes, dimbare spots en ledlicht vragen extra leidingen en schakelaars."),
            ("Vloerverwarming", "vloerverwarming", None, "In een grote badkamer vaak aangesloten op de cv of warmtepomp."),
        ],
        kosten="Een luxe badkamer zit bijna altijd in het hoogste segment van de indeling hierboven, en bij een grote ruimte kan het meer worden. De grootste posten zijn het tegelwerk met grote platen, het sanitair (vrijstaand bad, dubbel meubel, regendouche) en het extra leidingwerk als je de indeling verandert. Vraag altijd een offerte met de posten apart, dan zie je waar het geld heen gaat.",
        tips=[
            "Kies één blikvanger, zoals een marmeren wand of een vrijstaand bad, en houd de rest rustig.",
            "Plan het licht vroeg: leidingen voor wandlampjes en een dimmer moeten erin voordat er getegeld wordt.",
            "Check bij een vrijstaand bad of de vloer het gewicht draagt. Gevuld weegt een bad al snel 300 kilo of meer.",
            "Kies grote keramische platen in plaats van echt marmer als je weinig onderhoud wilt.",
        ],
        valkuilen=[
            "Goud, marmer, donker hout en een patroon tegelijk wordt druk. Luxe is juist rust.",
            "Een vrijstaand bad in een te kleine ruimte voelt krap. Houd rondom minstens 15 tot 20 cm vrij om schoon te maken.",
            "Een ruime inloopdouche zonder goede afvoer en afschot geeft natte vloeren. Laat dit door een specialist uitwerken.",
        ],
        faq=[
            ("Wat maakt een badkamer luxe?", "Ruimte, goede materialen, licht in lagen en comfort zoals vloerverwarming. Een vrijstaand bad, een dubbel meubel en een ruime inloopdouche horen er vaak bij."),
            ("Hoeveel ruimte heb ik nodig voor een vrijstaand bad?", "Een vrijstaand bad is vaak 160 tot 180 cm lang en 75 tot 80 cm breed. Reken daarbij rondom wat vrije ruimte om schoon te maken en in en uit te stappen."),
            ("Is echt marmer beter dan marmerlook?", "Echt marmer is uniek, maar zacht en gevoelig voor zuren en vlekken. Het moet geïmpregneerd worden. Keramische platen in marmerlook zijn sterker en makkelijker te onderhouden."),
            ("Welke kraankleur past bij een luxe badkamer?", "Warme kleuren zoals goud, messing of brons zijn populair. Chroom en mat zwart kunnen ook, zolang je overal dezelfde kleur gebruikt."),
        ],
        gidsen=["bad-of-douche", "douchesysteem-kiezen", "wastafelmeubel-kiezen", "kranen-kiezen"],
        kennis=["badkamer-waterdicht-maken", "inloopdouche-zonder-drempel", "tegels-kiezen"],
    ),
    dict(
        slug="marmer-badkamer", naam="Marmer badkamer", kort="Marmer",
        h1="Marmer badkamer: echt marmer of marmerlook?",
        seo="Marmer badkamer: echt marmer of marmerlook?",
        description="Een marmer badkamer is tijdloos: witte platen met grijze aders, op wand en vloer. Lees het verschil tussen echt marmer en marmerlook, met kosten, onderhoud en tips.",
        intro="Marmer geeft een badkamer meteen een rustige, tijdloze uitstraling. Wit met zachte grijze aders past bij hout, goud, chroom en zwart. In de illustratie zie je grote platen in marmerlook op wanden en vloer, een vrijstaand bad, een inloopdouche en een zwevend walnoten meubel.",
        sfeer="Een marmeren badkamer voelt koel en fris, maar door warm licht en hout wordt het juist zacht. Grote platen met doorlopende aders geven een rustig beeld, omdat je bijna geen voegen ziet. Kleinere tegels geven meer een klassieke sfeer. De vraag die je vroeg moet beantwoorden: kies je voor echt natuursteen of voor keramiek dat erop lijkt? Dat bepaalt het onderhoud voor de komende twintig jaar.",
        kenmerken=[
            "Witte of lichtgrijze steen met aders, op de wand, de vloer of allebei.",
            "Grote platen (bijvoorbeeld 120 × 270 cm) met weinig voegen, of tegels van 60 × 60 of 80 × 80 cm.",
            "Een warm contrast, zoals walnoot of eiken, zodat het niet kil wordt.",
            "Kranen in goud, messing, chroom of mat zwart.",
            "Een blad of wasbak van hetzelfde marmer voor een doorlopend beeld.",
        ],
        materialen=[
            ("Marmerlook plaat (keramisch)", "Wit met grijze aders, in grote platen. Waterdicht, krasvast en ongevoelig voor zure schoonmaakmiddelen.",
             "linear-gradient(115deg,transparent 0 38%,rgba(96,98,104,.45) 39%,transparent 41%),linear-gradient(60deg,transparent 0 66%,rgba(96,98,104,.3) 67%,transparent 68%),#f2f1ee"),
            ("Echt marmer", "Natuursteen met diepte in de aders. Elke plaat is anders. Zacht, poreus en gevoelig voor zuur, dus impregneren is nodig.",
             "radial-gradient(circle at 70% 30%,rgba(200,200,205,.6) 0 20%,transparent 50%),linear-gradient(120deg,transparent 0 45%,rgba(110,112,118,.5) 46%,transparent 48%),#efeeea"),
            ("Walnoot", "Donker hout met een levendige nerf. Een mooi warm contrast met wit marmer.",
             "repeating-linear-gradient(90deg,#6e4b33 0 5px,#5b3d29 5px 6px,#7a553b 6px 11px)"),
            ("Goud geborsteld", "Warm metaal voor kranen, spiegel en douche. Chroom geeft een koelere, klassieke uitstraling.",
             "linear-gradient(135deg,#f0d491,#b8913f 50%,#e3c27a)"),
        ],
        kleuren=[("Marmerwit", "#f2f1ee", "wanden en vloer"), ("Adergrijs", "#606268", "aders"),
                 ("Walnoot", "#6e4b33", "meubel en kruk"), ("Goud", "#d9b26a", "kranen"),
                 ("Linnen", "#e8e1d6", "textiel")],
        kosten_posten=[
            ("Marmerlook tegels", "tegels", "luxe", "Grote keramische platen vallen meestal in het luxe segment."),
            ("Tegels zetten", "tegelwerk", None, "Grote platen vragen een vlakke wand, twee mensen en speciaal gereedschap. Reken op de bovenkant."),
            ("Lijm, voeg en kit", "tegelwerk_hulpmateriaal", None, "Bij natuursteen kies je lijm en voeg die geschikt zijn voor marmer."),
            ("Vrijstaand bad", "sanitair_bad", "midden", "Het bad uit de illustratie, met staande kraan."),
        ],
        kosten="Echt marmer kost meestal meer dan de tegelprijzen hierboven, en het leggen vraagt een specialist in natuursteen. Daarna komen impregneren en onderhoud. Marmerlook in keramiek valt meestal in het luxe tegelsegment en heeft weinig onderhoud nodig. Grote platen besparen voegen, maar het zetten is zwaarder werk en duurder per m².",
        tips=[
            "Twijfel je tussen echt en look? Leg een staal van allebei een week in je badkamer en kijk hoe het voelt en hoe het reageert op water en zeep.",
            "Laat bij grote platen de aders doorlopen van plaat naar plaat. Vraag de tegelzetter om de platen eerst op de grond uit te leggen.",
            "Kies bij echt marmer een gezoete (matte) afwerking op de vloer. Gepolijst marmer is glad als het nat is.",
            "Combineer marmer met warm hout of warm licht, anders voelt het snel koel.",
        ],
        valkuilen=[
            "Echt marmer kan vlekken en dof worden door zure middelen, zoals azijn en kalkreiniger. Gebruik pH-neutrale schoonmaakmiddelen.",
            "Gepolijst marmer op de vloer is glad bij natte voeten. Kies een matte afwerking of marmerlook met antislip.",
            "Marmer op de vloer én de wand én het blad kan vlak worden. Wissel af met een effen vlak of hout.",
        ],
        faq=[
            ("Is marmer geschikt voor een badkamer?", "Ja, maar echt marmer vraagt onderhoud: impregneren, pH-neutraal schoonmaken en water snel afnemen. Marmerlook in keramiek geeft hetzelfde beeld met weinig onderhoud."),
            ("Wat is het verschil tussen marmer en marmerlook?", "Echt marmer is natuursteen met diepte en is per plaat uniek. Marmerlook is keramiek met een print van marmer. Dat is harder, minder poreus en makkelijker schoon te houden."),
            ("Hoe maak ik een marmeren badkamer schoon?", "Gebruik een zachte doek en een pH-neutraal middel. Geen azijn, citroen of kalkreiniger op echt marmer. Droog de douche na gebruik af met een trekker."),
            ("Welke kleur kraan past bij wit marmer?", "Goud en messing geven warmte, chroom oogt klassiek en fris, mat zwart geeft contrast. Kies één kleur voor alle kranen en accessoires."),
        ],
        gidsen=["badkamertegels-kopen", "kranen-kiezen", "bad-of-douche"],
        kennis=["tegels-kiezen", "badkamer-waterdicht-maken", "badkamerstijlen"],
    ),
    dict(
        slug="zwart-wit-badkamer", naam="Zwart-wit badkamer", kort="Zwart-wit",
        h1="Zwart-wit badkamer: tijdloos contrast",
        seo="Zwart-wit badkamer: ideeën, tegels en tips",
        description="Een zwart-wit badkamer is tijdloos en grafisch: witte metrotegels, een dambordvloer en zwart staal. Bekijk de kenmerken, materialen, kosten, tips en valkuilen.",
        intro="Zwart en wit gaan nooit uit de mode. Het contrast is grafisch en duidelijk, en past zowel in een jaren-dertigwoning als in nieuwbouw. In de illustratie zie je witte metrotegels met een donkere voeg, een zwart-wit dambordvloer, een douchewand met zwarte roeden en een mat zwart meubel op pootjes.",
        sfeer="Een zwart-wit badkamer heeft karakter. De dambordvloer en de metrotegels verwijzen naar oude stadsbadkamers en hotels, het zwarte staal geeft een moderne rand. Omdat er bijna geen kleur in zit, valt vorm extra op: de boog van de spiegel, de roeden in het glas, de lijn boven de tegels. Een beetje hout en een plant maken het vriendelijk.",
        kenmerken=[
            "Witte wandtegels, vaak metrotegels in halfsteens verband, met een grijze of zwarte voeg.",
            "Een vloer met contrast: dambord, een tegel met patroon of zwarte zeshoekjes.",
            "Zwarte accenten: kranen, douchewand, spiegelrand en een bies boven de tegels.",
            "Een zwart of wit meubel, staand op pootjes of zwevend.",
            "Wit sanitair en witte verf boven de tegels, zodat de ruimte licht blijft.",
        ],
        materialen=[
            ("Witte metrotegel met donkere voeg", "Tegel van 10 × 20 cm in halfsteens verband. De donkere voeg tekent elke tegel en verbergt vuil.",
             "linear-gradient(0deg,#3a3a3a 0 2px,transparent 2px),linear-gradient(90deg,#3a3a3a 0 2px,transparent 2px) 0 0/27px 14px,#f6f5f1"),
            ("Dambordvloer 30 × 30", "Zwarte en witte tegels om en om. Diagonaal gelegd lijkt de ruimte breder, recht gelegd oogt het rustiger.",
             "conic-gradient(#1f1f20 0 25%,#f1f0ec 0 50%,#1f1f20 0 75%,#f1f0ec 0) 0 0/27px 27px"),
            ("Mat zwart metaal", "Kranen, douchewand met roeden, spiegelrand en wandlampjes.",
             "linear-gradient(135deg,#3a3a3a,#111 50%,#2a2a2a)"),
            ("Zwart mat meubel", "Een meubel op pootjes met lades. Met een wit keramisch blad blijft het licht.",
             "linear-gradient(180deg,#1c1c1d 0 48%,#0f0f10 48% 52%,#1c1c1d 52%)"),
            ("Licht eiken", "Eén houten accent, zoals een krukje, maakt het contrast zachter.",
             "repeating-linear-gradient(90deg,#b58c62 0 5px,#a47c54 5px 6px,#c0976b 6px 11px)"),
        ],
        kleuren=[("Wit", "#f6f5f1", "wandtegels en sanitair"), ("Zwart", "#1f1f20", "vloer en accenten"),
                 ("Donkergrijs", "#3a3a3a", "voeg"), ("Gebroken wit", "#f2f1ee", "verf"),
                 ("Eiken", "#b58c62", "accent")],
        kosten_posten=[
            ("Tegels in de middenklasse", "tegels", "midden", "Metrotegels en effen vloertegels zijn niet duur."),
            ("Tegels zetten", "tegelwerk", None, "Kleine metrotegels en een dambord vragen meer tijd per m². Reken eerder op de bovenkant."),
            ("Douche met wand", "sanitair_douche", "midden", "Een douchewand met roeden kost meestal meer dan helder glas zonder profiel."),
            ("Wastafelmeubel", "sanitair_meubel", "midden", "Een zwart meubel op pootjes met keramisch blad."),
        ],
        kosten="De materialen zijn meestal niet duur, maar het legwerk wel. Kleine metrotegels en een dambordvloer betekenen veel voegen en precies uitlijnen: een scheve rij zie je meteen bij zoveel contrast. Een douchewand met zwarte roeden is duurder dan een simpele glazen wand. Met standaard sanitair blijf je vaak in het middensegment.",
        tips=[
            "Kies een voeg die bij het effect past: zwarte voeg voor grafisch, lichtgrijze voeg voor rustiger.",
            "Leg het dambord diagonaal in een smalle badkamer. Dat laat de ruimte breder lijken.",
            "Houd de bovenkant van de wand wit, dan blijft de ruimte licht.",
            "Voeg één warm materiaal toe, zoals hout of messing, als het te streng voelt.",
        ],
        valkuilen=[
            "Mat zwarte kranen en een zwarte vloer laten kalk en zeepresten goed zien. Bij hard water droog maken na gebruik.",
            "Een dambord dat niet in het midden begint, eindigt met halve tegels langs de muur. Laat de tegelzetter eerst een legplan maken.",
            "Te veel zwart maakt een kleine badkamer donker. Houd zwart voor de vloer en de accenten.",
        ],
        faq=[
            ("Is een zwart-wit badkamer niet te streng?", "Dat hangt af van de verhouding. Veel wit met zwarte accenten is fris en licht. Hout, een plant en warm licht maken het vriendelijker."),
            ("Welke voegkleur kies ik bij witte metrotegels?", "Een donkere voeg tekent het patroon en verbergt vuil. Een lichte voeg oogt rustiger, maar wordt sneller grauw in de douche."),
            ("Is een zwarte vloer lastig schoon te houden?", "Stof, kalk en zeepresten zie je sneller op zwart. Een dambord met wit verbergt dat beter dan een helemaal zwarte vloer."),
            ("Past een zwart-wit badkamer in een oud huis?", "Ja, juist. Metrotegels en een dambordvloer horen bij huizen uit begin twintigste eeuw."),
        ],
        gidsen=["badkamertegels-kopen", "inloopdouche-kopen", "kranen-kiezen"],
        kennis=["tegels-kiezen", "badkamerstijlen", "kleine-badkamer-indelen"],
    ),
    dict(
        slug="terrazzo-badkamer", naam="Terrazzo badkamer", kort="Terrazzo",
        h1="Terrazzo badkamer: speels, warm en sterk",
        seo="Terrazzo badkamer: tegels, kleuren en tips",
        description="Een terrazzo badkamer is speels en warm: een vloer met gekleurde korrels, terracotta tinten en messing. Met materialen, kleuren, kosten, onderhoud en valkuilen.",
        intro="Terrazzo is steenslag in een bindmiddel, geslepen tot een glad vlak vol gekleurde korrels. Het geeft een badkamer meteen een vrolijke, warme uitstraling. In de illustratie zie je terrazzotegels met terracotta en grijze korrels op de vloer en in de douche, zachte terracotta verf en een eiken meubel met een terracotta kom.",
        sfeer="Terrazzo komt uit Italië en lag vroeger in trappenhuizen en hallen. Nu is het terug in kleuren van zand, roze, terracotta en groen. Het werkt het mooist als je de korrels terug laat komen in de rest van de badkamer: een kom in terracotta, verf in een zachte aardetint en messing kranen. Zo wordt het een geheel in plaats van een losse tegel.",
        kenmerken=[
            "Een vloer of wand in terrazzo met korrels in twee tot vijf kleuren.",
            "Kleuren uit de korrels terug in verf, textiel of een kom.",
            "Warme materialen erbij: licht eiken, messing of mat goud.",
            "Ronde vormen: een ronde spiegel en een ronde opzetkom.",
            "Een rustige achtergrond, zodat de terrazzo de blikvanger blijft.",
        ],
        materialen=[
            ("Terrazzotegel 60 × 60", "Tegels van terrazzo of keramiek met terrazzoprint. Echte terrazzo is sterk, maar moet bij gebruik in de badkamer geïmpregneerd worden.",
             "radial-gradient(circle at 20% 30%,#c4704f 0 3px,transparent 4px),radial-gradient(circle at 70% 60%,#5f5a55 0 4px,transparent 5px),radial-gradient(circle at 45% 80%,#d99a7c 0 3px,transparent 4px),radial-gradient(circle at 80% 20%,#9a948c 0 2px,transparent 3px),#ebe2d7"),
            ("Terrazzo blad", "Een blad in hetzelfde materiaal laat de vloer doorlopen in het meubel.",
             "radial-gradient(circle at 30% 60%,#b5543a 0 3px,transparent 4px),radial-gradient(circle at 60% 30%,#e8c4b0 0 4px,transparent 5px),#ebe2d7"),
            ("Terracotta kalkverf", "Een zachte aardetint boven de tegels. Kies een soort die geschikt is voor natte ruimtes.",
             "radial-gradient(circle at 30% 30%,#ecd0bd 0 30%,transparent 60%),#e3bfa8"),
            ("Licht eiken", "Een eiken meubel en krukje voor warmte.",
             "repeating-linear-gradient(90deg,#c9a074 0 5px,#b88f64 5px 6px,#d3aa7e 6px 11px)"),
            ("Messing", "Kranen, douche en spiegelrand in warm metaal.",
             "linear-gradient(135deg,#f3d58a,#b88a35 50%,#e7c46f)"),
        ],
        kleuren=[("Zandbasis", "#ebe2d7", "terrazzo"), ("Terracotta", "#c4704f", "korrels en kom"),
                 ("Poederroze", "#e3bfa8", "verf"), ("Steengrijs", "#9a948c", "korrels"),
                 ("Messing", "#c9a35c", "kranen")],
        kosten_posten=[
            ("Tegels in het luxe segment", "tegels", "luxe", "Echte terrazzotegels zijn duurder dan keramische tegels met terrazzoprint (die vallen eerder in het middensegment)."),
            ("Tegels zetten", "tegelwerk", None, "Terrazzo is zwaar en dik. Echte terrazzo wordt na het leggen soms nog geslepen."),
            ("Lijm, voeg en kit", "tegelwerk_hulpmateriaal", None, "Gebruik lijm en voeg die geschikt zijn voor natuursteen en terrazzo."),
            ("Wastafelmeubel", "sanitair_meubel", "midden", "Een eiken meubel met een blad van terrazzo en een opzetkom."),
        ],
        kosten="Keramische tegels met een terrazzoprint zijn de betaalbare keuze en vragen geen extra onderhoud. Echte terrazzotegels kosten meer, zijn zwaarder om te leggen en moeten geïmpregneerd worden. Een gegoten naadloze terrazzovloer is weer een ander, duurder vak; vraag daarvoor een gespecialiseerd bedrijf.",
        tips=[
            "Kies een terrazzo met kleine korrels voor een kleine badkamer. Grote korrels zijn druk op een klein vlak.",
            "Pak één kleur uit de korrels en gebruik die voor verf of textiel. Dan hoort alles bij elkaar.",
            "Wil je echte terrazzo in de douche? Vraag naar impregneren en de juiste schoonmaakmiddelen.",
            "Een terrazzo blad of vensterbank is een kleinere stap als je niet de hele vloer wilt doen.",
        ],
        valkuilen=[
            "Echte terrazzo bevat marmer en kalk en is gevoelig voor zure middelen. Gebruik pH-neutraal.",
            "Terrazzo op vloer én wand én blad kan te veel worden. Houd één vlak rustig.",
            "Goedkope print kan van dichtbij nep ogen. Bekijk een staal in het echt, niet alleen op een foto.",
        ],
        faq=[
            ("Wat is terrazzo?", "Steenslag van marmer, graniet of glas in een bindmiddel van cement of hars, geslepen tot een glad oppervlak. Je kunt het kopen als tegel of laten gieten als naadloze vloer."),
            ("Is terrazzo geschikt voor een douche?", "Ja, als het goed is geïmpregneerd en je pH-neutraal schoonmaakt. Keramische tegels met terrazzoprint kunnen zonder extra onderhoud in de douche."),
            ("Is terrazzo glad?", "Gepolijste terrazzo kan glad zijn als hij nat is. Kies voor de douche een matte of geschuurde afwerking, of een tegel met antislip."),
            ("Welke kleuren passen bij terrazzo?", "Haal een kleur uit de korrels terug, bijvoorbeeld terracotta, roze, groen of grijs. Hout en messing passen bijna altijd."),
        ],
        gidsen=["badkamertegels-kopen", "wastafelmeubel-kiezen", "kranen-kiezen"],
        kennis=["tegels-kiezen", "badkamerstijlen", "badkamer-waterdicht-maken"],
    ),
    dict(
        slug="wellness-badkamer", naam="Wellness badkamer", kort="Wellness",
        h1="Wellness badkamer: een spa in je eigen huis",
        seo="Wellness badkamer: ideeën, kosten en tips",
        description="Een wellness badkamer voelt als een spa: donkere steen, warm hout, een zitbank in de douche en gedimd licht. Met materialen, kleuren, kosten, tips en valkuilen.",
        intro="Een wellness badkamer is gemaakt om te ontspannen. Donkere, natuurlijke materialen, warm hout en zacht licht maken er een plek van waar je langer blijft. In de illustratie zie je donkere tegels in steenlook, een wand van eiken lamellen, een ruime inloopdouche met een betegelde zitbank en een lange nis met warm ledlicht.",
        sfeer="Een wellness badkamer draait om je zintuigen. Je voelt de warmte van de vloer, je hoort alleen het water en het licht is laag en warm, zoals in een sauna of een hotelspa. Donkere tinten maken de ruimte intiem, hout geeft geur en warmte. Een zitbank in de douche is fijn om even te zitten, je benen te scheren of je kind te wassen. Planten maken het af.",
        kenmerken=[
            "Donkere, natuurlijke tinten: tegels in steenlook of leisteen, met warm hout.",
            "Een ruime inloopdouche met een grote regendouche, eventueel aan het plafond.",
            "Een zitbank in de douche, betegeld of van massief steen.",
            "Indirect, dimbaar licht: ledstrips in nissen en onder het meubel, en een spiegel met lichtrand.",
            "Warmte: vloerverwarming en een handdoekradiator.",
            "Rust: weinig spullen, gesloten kasten en planten.",
        ],
        materialen=[
            ("Donkere steenlook tegel 60 × 120", "Grote tegel in warm donkergrijs met een lichte steenstructuur. Mat, dus minder glad en minder vlekken.",
             "radial-gradient(circle at 30% 40%,#625e58 0 10%,transparent 11%),radial-gradient(circle at 70% 70%,#4a4743 0 8%,transparent 9%),#57534e"),
            ("Eiken lamellen", "Houten latten op een donkere achtergrond, achter het meubel buiten de natte zone. Ze dempen ook het geluid.",
             "repeating-linear-gradient(90deg,#b88758 0 8px,#1c1a18 8px 11px)"),
            ("Zandkleurige kalkverf", "Een warme wand tegenover de donkere tegels houdt de ruimte prettig licht.",
             "radial-gradient(circle at 30% 30%,#d8ccbc 0 30%,transparent 60%),#cdbfae"),
            ("Mat zwart", "Kranen, regendouche en profiel van de glazen wand.",
             "linear-gradient(135deg,#3a3a3a,#111 50%,#2a2a2a)"),
            ("Warm ledlicht", "Ledstrips van 2700 kelvin of lager in de nis en onder het meubel. Geschikt voor natte ruimtes (IP65 of hoger in de douche).",
             "linear-gradient(180deg,#57534e 0 40%,#ffc98f 46%,#fff1dc 50%,#ffc98f 54%,#57534e 60%)"),
        ],
        kleuren=[("Steengrijs", "#57534e", "wanden en vloer"), ("Eiken", "#b88758", "lamellen"),
                 ("Zand", "#cdbfae", "verf"), ("Mat zwart", "#1b1b1c", "kranen"),
                 ("Warm licht", "#ffc98f", "ledlicht")],
        kosten_posten=[
            ("Inloopdouche met regendouche", "sanitair_douche", "luxe", "Grote regendouche, thermostaat, goot en een brede glazen wand."),
            ("Waterdicht maken van de douche", "waterdicht", None, "Een zitbank en een lange nis maken het waterdicht maken en tegelen bewerkelijker."),
            ("Elektra en verlichting", "elektra", None, "Ledstrips, een spiegel met licht en dimmers vragen extra leidingen."),
            ("Vloerverwarming", "vloerverwarming", None, "Een warme vloer hoort bij een wellness badkamer."),
            ("Badkamerventilator", "ventilator", None, "Een regendouche maakt veel damp. Een goede afzuiging voorkomt schimmel."),
        ],
        kosten="Een wellness badkamer valt meestal in het midden- of luxesegment. De extra kosten zitten in de douche (grote regendouche, zitbank, lange nis), in het licht (ledstrips, dimmers, extra groepen) en in comfort zoals vloerverwarming. Lamellen en planten zijn juist relatief goedkoop en geven veel sfeer.",
        tips=[
            "Plan de zitbank en de nis voordat de wanden dicht gaan. Ze moeten in het waterdichte pakket worden meegenomen.",
            "Kies ledlicht van 2700 kelvin of lager, met een dimmer. Wit licht van 4000 kelvin past niet bij een spa.",
            "Houd hout buiten de natte zone, of kies een houtsoort en afwerking die geschikt zijn voor vocht.",
            "Een regendouche aan het plafond vraagt een goede waterdruk en vaak een grotere warmwatervoorziening. Laat dat vooraf checken.",
        ],
        valkuilen=[
            "Donkere tegels laten kalkaanslag zien. Een matte afwerking en een trekker na het douchen helpen.",
            "Te weinig licht: een sfeervolle badkamer heeft ook goed licht bij de spiegel nodig om je te scheren of op te maken.",
            "Een grote regendouche met een kleine boiler: na vijf minuten is het warme water op. Laat de capaciteit berekenen.",
        ],
        faq=[
            ("Wat heb je nodig voor een wellness badkamer?", "Een ruime inloopdouche met regendouche, warme materialen, dimbaar indirect licht en comfort zoals vloerverwarming. Een zitbank, een stoomdouche of een bad zijn extra's."),
            ("Kan ik een sauna in mijn badkamer zetten?", "Dat kan als er genoeg ruimte is en de elektra het aankan. Een sauna vraagt meestal een eigen groep en goede ventilatie. Laat dat door een specialist bekijken."),
            ("Is een donkere badkamer niet te somber?", "Niet als je zorgt voor genoeg licht in lagen en een warm contrast, zoals hout en een lichte wand. Donker maakt een ruimte intiem."),
            ("Welke regendouche past bij een wellness badkamer?", "Een grote vierkante of ronde hoofddouche van 30 cm of meer, met een thermostaat en een losse handdouche. Lees meer in de gids over douchesystemen."),
        ],
        gidsen=["douchesysteem-kiezen", "inloopdouche-kopen", "wastafelmeubel-kiezen"],
        kennis=["badkamer-ventilatie", "badkamer-waterdicht-maken", "inloopdouche-zonder-drempel"],
    ),
]

LINKS = [(f"{PAD}{s['slug']}/", s["naam"], s["description"].split(".")[0] + ".") for s in STIJLEN]


def _esc(t):
    return htmllib.escape(t, quote=True)


def _render_img(sleutel, sizes, boven_vouw=False):
    """Responsieve <img> voor een render: srcset 400/800/1600 en vaste width/height."""
    r = RENDERS_STIJL2[sleutel]
    n = r["naam"]
    laden = 'loading="eager" fetchpriority="high"' if boven_vouw else 'loading="lazy"'
    return (f'<img src="/assets/fotos/renders/{n}-800.webp" '
            f'srcset="/assets/fotos/renders/{n}-400.webp 400w, /assets/fotos/renders/{n}-800.webp 800w, '
            f'/assets/fotos/renders/{n}-1600.webp 1600w" sizes="{sizes}" width="{r["w"]}" height="{r["h"]}" '
            f'alt="{_esc(r["alt"])}" {laden} decoding="async">')


def _figuur(sleutel, sizes, boven_vouw=False):
    return (f'<figure class="bi-fig">{_render_img(sleutel, sizes, boven_vouw)}'
            f'<figcaption class="bi-label">Illustratie (3D-render)</figcaption></figure>'
            f'<p class="bi-bij">{_esc(RENDERS_STIJL2[sleutel]["bijschrift"])}</p>')


def _kaart(href, soort, naam, oms):
    return (f'<a href="{href}"><span class="bi-soort">{soort}</span><span class="bi-naam">{naam}</span>'
            f'<span class="bi-oms">{oms}</span></a>')


CSS2 = """<style>
.bi2-sfeer{background:var(--bg-soft,#f6f4f0);border-left:4px solid var(--accent,#c4622d);border-radius:var(--radius);padding:16px 20px;margin:22px 0}
.bi2-sfeer p{margin:0}
.bi2-tabel{width:100%;border-collapse:collapse;margin:14px 0 6px;font-size:.93rem}
.bi2-tabel th,.bi2-tabel td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
.bi2-tabel th{font-size:.8rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted,#5b6470)}
.bi2-tabel td:nth-child(2){white-space:nowrap;font-weight:700}
.bi2-detail{margin:26px 0 8px}
.bi2-palet{display:flex;height:46px;border-radius:var(--radius);overflow:hidden;border:1px solid rgba(0,0,0,.08);margin:6px 0 10px}
.bi2-palet span{flex:1}
@media (max-width:560px){.bi2-tabel thead{display:none}.bi2-tabel tr{display:block;border-bottom:1px solid var(--line);padding:8px 0}
.bi2-tabel td{display:block;border:0;padding:2px 0}.bi2-tabel td:nth-child(2){white-space:normal}}
</style>"""


def _kosten_tabel(s):
    rijen = "".join(
        f"<tr><td>{naam}</td><td>{_rp(k, niv)}</td><td>{waarom}</td></tr>" for naam, k, niv, waarom in s["kosten_posten"])
    return (f'<table class="bi2-tabel"><thead><tr><th>Onderdeel</th><th>Richtprijs</th><th>Waarom bij deze stijl</th></tr></thead>'
            f'<tbody>{rijen}</tbody></table>'
            f'<p style="font-size:.86rem">Richtprijzen inclusief 21% btw, voor alleen dat onderdeel. Bij een niveau (basis, midden, luxe) '
            f'staat de bandbreedte van dat niveau. Dezelfde bedragen gebruiken we in de badkamercalculator.</p>')


def _bronnen(s):
    gezien, items = set(), []
    for lab, u in BRONNEN_KOSTEN:
        gezien.add(u); items.append((lab, u))
    for _, k, _, _ in s["kosten_posten"]:
        for lab, u in RP.bron_links(k):
            if u and u not in gezien:
                gezien.add(u); items.append((lab, u))
    return items


def _stijlpagina(s, write, today):
    url = f"{PAD}{s['slug']}/"
    cr, cr_ld = crumbs([("Home", "/"), ("Inspiratie", PAD), (s["naam"], None)])
    kenmerken = "".join(f"<li>{k}</li>" for k in s["kenmerken"])
    stalen = "".join(
        f'<div class="bi-staal"><span class="bi-staal-vlak" style="background:{bg}" aria-hidden="true"></span>'
        f'<div><h3>{n}</h3><p>{t}</p></div></div>' for n, t, bg in s["materialen"])
    kleuren = "".join(
        f'<li><span class="bi-dot" style="background:{hx}" aria-hidden="true"></span><strong>{n}</strong>{waar}</li>'
        for n, hx, waar in s["kleuren"])
    palet = "".join(f'<span style="background:{hx}"></span>' for _, hx, _ in s["kleuren"])
    tips = "".join(f"<li>{t}</li>" for t in s["tips"])
    valkuilen = "".join(f"<li>{t}</li>" for t in s["valkuilen"])
    bronnen = _bronnen(s)
    eigen = ('<p class="bi-bronnen">Een deel van de bedragen in de tabel is een eigen inschatting op basis van deze bronnen.</p>'
             if any("eigen" in RP.RICHTPRIJZEN[k]["bron"] for _, k, _, _ in s["kosten_posten"]) else "")
    bronnen_html = "".join(f'<li><a href="{_esc(u)}" rel="noopener">{_esc(lab)}</a></li>' for lab, u in bronnen)

    kaarten = [_kaart("/tools/stijlkiezer/", "Tool", "Probeer combinaties in de stijlkiezer",
                      "Wissel zelf tegels, kranen en meubels in een getekende badkamer.")]
    kaarten += [_kaart(f"/badkamerspullen/{g}/", "Kopersgids", *GIDSEN[g]) for g in s["gidsen"]]
    kaarten += [_kaart(f"/kennisbank/{k}/", "Kennisbank", *KENNIS[k]) for k in s["kennis"]]
    kaarten.append(_kaart("/kosten/nieuwe-badkamer/", "Kosten", "Wat kost een nieuwe badkamer?",
                          "Richtprijzen met een rekenvoorbeeld en bronnen."))

    andere = "".join(
        f'<a href="{PAD}{o["slug"]}/"><figure class="bi-fig">{_render_img(o["slug"], "(max-width: 700px) 45vw, 200px")}'
        f'<figcaption class="bi-label">Illustratie</figcaption></figure>{o["naam"]}</a>'
        for o in STIJLEN if o["slug"] != s["slug"])

    balken = prijs_balken(NIVEAUS, "Totaalprijs per badkamer, inclusief materiaal en 21% btw",
                          "Indeling zoals op onze kostenpagina, op basis van Homedeal, Trustoo en Slimster.")
    faq_html, faq_ld = faq_blok(s["faq"], f"Veelgestelde vragen over een {s['naam'].lower()}")
    naam_l = s["naam"].lower()

    body = f"""{BI_CSS}{CSS2}{cr}
<article class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Inspiratie · badkamerstijl</span>
  <h1>{s['h1']}</h1>
  <p class="lead">{s['intro']}</p>
  <div class="bi-hero">{_figuur(s['slug'], "(max-width: 860px) 100vw, 820px", boven_vouw=True)}</div>

  <h2 id="sfeer">De sfeer</h2>
  <div class="bi2-sfeer"><p>{s['sfeer']}</p></div>

  <h2 id="kenmerken">Kenmerken van een {naam_l}</h2>
  <ul class="checklist">{kenmerken}</ul>

  <h2 id="materialen">Materialen en kleuren</h2>
  <p>Dit zijn de materialen uit de illustraties. Je hoeft ze niet allemaal over te nemen: kies een basis en hooguit één of twee accenten.</p>
  <div class="bi-stalen">{stalen}</div>
  <div class="bi2-detail">{_figuur(s['slug'] + '-2', "(max-width: 860px) 100vw, 820px")}</div>
  <h3>Kleurenpalet</h3>
  <div class="bi2-palet" aria-hidden="true">{palet}</div>
  <ul class="bi-kleuren">{kleuren}</ul>
  <p style="font-size:.88rem">De kleurstalen zijn een benadering op een scherm. Bekijk tegels en verf altijd in het echt, bij daglicht en bij het licht in je badkamer.</p>

  <h2 id="kosten">Wat kost een {naam_l}?</h2>
  <p>De meeste complete badkamers van 5 tot 9 m² kosten <strong>€6.000 tot €18.000</strong>, inclusief sloopwerk, leidingwerk, tegels, sanitair, montage en 21% btw. De stijl zelf bepaalt de prijs niet; de keuzes erbinnen wel.</p>
  {balken}
  <h3>Onderdelen die bij deze stijl horen</h3>
  {_kosten_tabel(s)}
  <p>{s['kosten']}</p>
  <p>Een uitgebreide uitleg met een rekenvoorbeeld staat op <a href="/kosten/nieuwe-badkamer/">wat kost een nieuwe badkamer</a>. Je eigen badkamer doorrekenen kan met de <a href="/tools/badkamercalculator/">badkamercalculator</a>.</p>
  <p class="bi-bronnen"><strong>Bronnen voor de richtprijzen</strong> (geraadpleegd november 2026):</p>
  <ul class="bi-bronnen">{bronnen_html}</ul>
  {eigen}

  {offertecheck_blok(f"een {naam_l}")}

  <div class="bi-twee">
    <div>
      <h2 id="tips">Tips</h2>
      <ul class="checklist">{tips}</ul>
    </div>
    <div>
      <h2 id="valkuilen">Valkuilen</h2>
      <ul>{valkuilen}</ul>
    </div>
  </div>

  {cta_midden(f"Een {naam_l} laten maken?", "Vergelijk gratis offertes van maximaal drie badkamerspecialisten uit je regio.")}

  <h2 id="verder">Verder met je plan</h2>
  <p>Kopersgidsen, uitleg en richtprijzen die bij deze stijl passen:</p>
  <div class="bi-verder">{"".join(kaarten)}</div>

  <h2 id="andere">Meer stijlen</h2>
  <div class="bi-andere">{andere}</div>
  <p style="margin-top:14px"><a href="{PAD}">Alle badkamerstijlen op een rij</a></p>
</div></article>
{faq_html}
{cta_blok("Klaar voor je nieuwe badkamer?", "Beschrijf je wensen in een minuut en ontvang gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio.")}"""

    beelden = []
    for k in (s["slug"], s["slug"] + "-2"):
        r = RENDERS_STIJL2[k]
        beelden.append({"@type": "ImageObject", "url": f"{SITE['url']}/assets/fotos/renders/{r['naam']}-1600.webp",
                        "width": r["w"], "height": r["h"], "caption": r["bijschrift"]})
    art_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": s["h1"], "description": s["description"], "inLanguage": "nl-NL",
        "datePublished": GEPUBLICEERD, "dateModified": today, "image": beelden,
        "author": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "publisher": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "mainEntityOfPage": SITE["url"] + url,
        "isPartOf": {"@type": "CollectionPage", "@id": SITE["url"] + PAD},
        "citation": [u for _, u in bronnen],
    }
    write(url, page(title(s["seo"]), s["description"], url, body, [cr_ld, art_ld, faq_ld]), prio=0.7)


def build(write):
    today = datetime.date.today().isoformat()
    for s in STIJLEN:
        _stijlpagina(s, write, today)
