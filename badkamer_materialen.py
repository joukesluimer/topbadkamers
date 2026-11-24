# -*- coding: utf-8 -*-
"""Materialen voor de badkamer: /materialen/ en acht materiaalpagina's (/materialen/<slug>/).

Elke pagina heeft getekende stalen (canvas, procedureel, geen foto's), een eerlijke vergelijking
van eigenschappen (onderhoud, slijtvastheid, antislip, waterdichtheid, prijs met bron), waar het
materiaal geschikt voor is, valkuilen, tips en een FAQ. Keramische tegels hebben een legpatroon-
kiezer, voegen en kit een voegkleurkiezer. Het overzicht heeft een vergelijkingstabel.

Het JavaScript (stalen en kiezers) staat onderaan in JS. Het tekent pas als een staal in beeld komt.

Prijzen: richtprijzen inclusief 21% btw. Waar het kan uit richtprijzen.py (RP), zodat de site overal
dezelfde bedragen noemt. Nieuwe prijzen staan hieronder met hun bron (geraadpleegd november 2026):
- Natuursteen: Werkspot, badkamer tegelen: hardsteen €30 – €130 per m², marmer €50 – €130 per m²
  (materiaal). https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten
  Slimster, kosten natuurstenen vloer (leggen en materiaal, ter controle):
  https://slimster.nl/tegelzetter/vloertegels-prijzen/kosten-natuursteen-vloertegels/
- Microcement: Werkspot €100 – €150 per m²; Homedeal €120 – €180 per m² (vloer en wand), inloopdouche
  €150 – €200 per m²; Slimster €120 – €150 per m², alles inclusief materiaal, arbeid en btw.
  https://www.werkspot.nl/badkamer-sanitair/artikelen/microcement-in-de-badkamer
  https://www.homedeal.nl/stucwerk/microcement
  https://slimster.nl/stukadoors/microbeton-microcement-prijzen/
- Gegoten terrazzo (granito): Slimster €120 – €280 per m² inclusief btw.
  https://slimster.nl/vloeren/kosten/granieten-vloer-prijzen/
- Opnieuw voegen: uitslijpen en hervoegen gemiddeld €43 – €66 per m² (indicatief, verzamelpagina).
  https://webwoordenboek.nl/kenniscentrum/wat-kost-badkamer-opnieuw-voegen
- Kranen en glazen douchewanden: eigen steekproef van winkelprijzen bij Nederlandse bouwmarkten en
  sanitairwebwinkels (november 2026). Wastafelkranen in mat zwart, gunmetal en goud: ongeveer
  €60 – €170 in het instapsegment; glazen inloopwanden (8 mm, 80 – 100 cm): ongeveer €200 – €750,
  ribbelglas aan de bovenkant. Winkels worden op de site niet genoemd.
"""

import datetime
import html as htmllib

from components import page, crumbs, title, faq_blok, cta_blok, cta_midden, offertecheck_blok, prijs_balken, eur
from data import SITE
import richtprijzen as RP

PAD = "/materialen/"
GEPUBLICEERD = "2026-11-23"

BRONNEN = dict(RP.BRONNEN)
BRONNEN.update({
    "slimster_natuursteen": ("Slimster, kosten natuurstenen vloer", "https://slimster.nl/tegelzetter/vloertegels-prijzen/kosten-natuursteen-vloertegels/"),
    "werkspot_micro": ("Werkspot, microcement in de badkamer", "https://www.werkspot.nl/badkamer-sanitair/artikelen/microcement-in-de-badkamer"),
    "homedeal_micro": ("Homedeal, microcement kosten", "https://www.homedeal.nl/stucwerk/microcement"),
    "slimster_micro": ("Slimster, microbeton en microcement prijzen", "https://slimster.nl/stukadoors/microbeton-microcement-prijzen/"),
    "slimster_granito": ("Slimster, granito vloer prijzen", "https://slimster.nl/vloeren/kosten/granieten-vloer-prijzen/"),
    "ww_voegen": ("Webwoordenboek kenniscentrum, badkamer opnieuw voegen (indicatief)", "https://webwoordenboek.nl/kenniscentrum/wat-kost-badkamer-opnieuw-voegen"),
    "steekproef": ("Eigen steekproef van winkelprijzen, november 2026", ""),
})


def _rp(sleutel):
    d = RP.RICHTPRIJZEN[sleutel]
    return d["laag"], d["hoog"]


def _niv(sleutel, niveau):
    return tuple(RP.RICHTPRIJZEN[sleutel]["niveaus"][niveau])


def _esc(t):
    return htmllib.escape(t, quote=True)


# ---------------------------------------------------------------------------
# Paletten voor de kiezers
# ---------------------------------------------------------------------------

TEGELKLEUREN = [("Wit", "#f3f1ec"), ("Zand", "#ddd2bf"), ("Betongrijs", "#a3a19b"), ("Antraciet", "#4a4c4f"),
                ("Saliegroen", "#a7b39c"), ("Terracotta", "#c07a58"), ("Diepblauw", "#2f4a63")]
VOEGKLEUREN = [("Wit", "#f6f5f1"), ("Zilvergrijs", "#c9c7c1"), ("Zand", "#cbbda3"), ("Cementgrijs", "#9a978f"),
               ("Antraciet", "#4f5153"), ("Zwart", "#1f1f21")]
FORMATEN = [("15x15", "15 × 15"), ("7.5x30", "7,5 × 30"), ("30x60", "30 × 60"), ("60x60", "60 × 60"), ("120x60", "120 × 60")]
PATRONEN = [("stapel", "Stapelverband"), ("halfsteens", "Halfsteens"), ("derde", "1/3 verband"), ("visgraat", "Visgraat")]


def staal(s, v="", w=600, h=400, label="", extra=""):
    """Canvas-staal. Zonder JS of voor het tekenen zie je de achtergrondkleur."""
    lab = f' role="img" aria-label="{_esc(label)}"' if label else ' aria-hidden="true"'
    vv = f' data-v="{v}"' if v else ""
    return f'<canvas class="mt-c" data-s="{s}"{vv} width="{w}" height="{h}"{extra}{lab}></canvas>'


def tegelstaal(f, p, k, g, vb=3, w=600, h=400, label="", gl=False, tex="", view=""):
    ex = f' data-f="{f}" data-p="{p}" data-k="{k}" data-g="{g}" data-vb="{vb}"'
    ex += ' data-gl="1"' if gl else ""
    ex += f' data-tex="{tex}"' if tex else ""
    ex += f' data-view="{view}"' if view else ""
    return staal("tegel", "", w, h, label, ex)


def _fig(canvas, naam, tekst):
    return f'<figure class="mt-staal">{canvas}<figcaption><strong>{naam}</strong>{tekst}</figcaption></figure>'


# ---------------------------------------------------------------------------
# Materialen
# ---------------------------------------------------------------------------
# geschikt: (plek, oordeel "ja" | "let" | "nee", uitleg)
# eig: onderhoud en slijt als score 1 – 5 (5 = weinig onderhoud / zeer slijtvast), plus tekst.
# prijzen: (label, laag, hoog) voor prijs_balken; eenheid en bronnen apart.

MATERIALEN = [
    dict(
        slug="keramische-tegels", naam="Keramische tegels", kort="Tegels",
        seo="Keramische tegels: formaten, legpatronen en prijs",
        h1="Keramische tegels: formaten, legpatronen en wat ze kosten",
        description="Keramische tegels in de badkamer: porselein of wandtegel, formaten tot 120 × 60, legpatronen zoals visgraat, antislip en prijzen per m². Met legpatroon-kiezer.",
        oms="De standaard voor vloer, wand en douche: sterk, waterafstotend en in elk formaat.",
        intro="Bijna elke badkamer heeft tegels. Dat is niet voor niets: een goede porseleinen tegel neemt bijna geen water op, slijt nauwelijks en is makkelijk schoon te houden. Toch maakt het veel uit welke tegel je kiest en hoe je hem legt. Het formaat, het legpatroon en de voegkleur bepalen of een badkamer rustig of druk oogt. Hieronder zie je getekende voorbeelden en kun je zelf combinaties proberen.",
        hero=[tegelstaal("120x60", "derde", "#d9d4ca", "#c4beb2", 2, tex="beton", label="Grote tegel 120 × 60 in 1/3 verband"),
              tegelstaal("7.5x30", "visgraat", "#f2f0ea", "#bdb8ae", 2, gl=True, label="Witte tegel 7,5 × 30 in visgraat"),
              tegelstaal("15x15", "stapel", "#a7b39c", "#efede6", 2, gl=True, label="Groene tegel 15 × 15 in stapelverband")],
        soorten_titel="Soorten keramische tegels",
        soorten=[
            (tegelstaal("60x60", "stapel", "#a3a19b", "#8f8c86", 2, tex="beton"), "Porseleinen tegel",
             "Gebakken op hoge temperatuur, heel dicht en hard. Neemt minder dan 0,5% water op. Geschikt voor vloer, wand en douche. Vaak doorgekleurd: een schilfer valt minder op."),
            (tegelstaal("7.5x30", "halfsteens", "#f4f2ed", "#dcd8d0", 2, gl=True, view="110"), "Geglazuurde wandtegel",
             "Een zachtere scherf met een glazuurlaag. Mooi glanzend en goedkoop, maar alleen voor de wand: op de vloer slijt en breekt hij."),
            (tegelstaal("120x60", "derde", "#ece9e3", "#d6d2ca", 2), "Groot formaat",
             "60 × 120 cm of groter. Weinig voegen, dus een rustig vlak dat makkelijk schoon blijft. Vraagt een heel vlakke ondergrond en een tegelzetter met ervaring."),
            (tegelstaal("5x5", "stapel", "#7d9aa6", "#e8e6e0", 2, gl=True, view="60"), "Mozaïek en kleine tegels",
             "Kleine tegels volgen het afschot in een douchevloer makkelijk. De vele voegen geven grip onder blote voeten, maar ook meer voegen om schoon te houden."),
            (tegelstaal("20x120", "visgraat", "#b98d5f", "#8d7258", 2, view="380"), "Houtlook in visgraat",
             "Lange smalle porseleinen tegels met een houtprint. Ziet eruit als parket, maar kan gewoon nat worden."),
        ],
        eig=dict(onderhoud=5, slijt=5,
                 onderhoud_t="Weinig: afnemen met een milde reiniger. De voegen vragen de meeste aandacht.",
                 slijt_t="Porselein is zeer slijtvast. Bij geglazuurde vloertegels geeft de PEI-klasse (1 tot 5) de slijtvastheid van het glazuur aan; neem in de badkamer klasse 3 of hoger.",
                 antislip="Badkamervloer: vaak R10 of klasse B (blote voeten). Douchevloer: R11 of klasse B tot C. De waarde staat op het productblad van de tegel.",
                 water="De tegel zelf is bijna waterdicht, de voegen niet. In de douche hoort er altijd een waterdichte laag onder de tegels."),
        prijs_eenheid="per m², inclusief 21% btw",
        prijzen=[("Tegels, basis", *_niv("tegels", "basis")), ("Tegels, midden", *_niv("tegels", "midden")),
                 ("Tegels, luxe of groot formaat", *_niv("tegels", "luxe")), ("Leggen (legloon)", *_rp("tegelwerk"))],
        prijs_tekst="De tegel zelf kost meestal €20 tot €60 per m². Grote formaten, bijzondere glazuren en handgemaakte tegels zitten hoger. Het leggen kost €25 tot €55 per m²; grote tegels, visgraat en kleine mozaïek zitten aan de bovenkant, omdat ze meer tijd en snijwerk vragen. Lijm, voegsel en kit komen daar nog bij, ongeveer €10 per m².",
        bronnen=["werkspot_tegel", "slimster_badkamer", "trustoo_tegel", "homedeal_tegel"],
        geschikt=[("Vloer", "ja", "Porseleinen tegels met R10 of klasse B. Geen glanzende tegel op de vloer."),
                  ("Wand", "ja", "Elke tegel. Geglazuurde wandtegels zijn hier een goedkope en mooie keuze."),
                  ("Douche", "ja", "Wand: alles. Vloer: kleine tegels op afschot, of grote tegels met een douchegoot en afschot in één richting.")],
        kiezer="tegel",
        valkuilen=[
            "Halfsteens leggen met lange tegels (60 cm en meer). Grote tegels zijn nooit helemaal vlak; bij halve verspringing komt het hoogste punt naast het laagste. Fabrikanten raden dan vaak hooguit 1/3 verspringing aan.",
            "Grote tegels in een douchevloer met een put in het midden. De vloer moet dan in vier richtingen aflopen, en dat lukt niet met een stijve grote tegel. Kies een douchegoot met afschot in één richting, of kleinere tegels.",
            "Een wandtegel op de vloer. Kijk of er op de doos of het productblad 'vloer' staat.",
            "Te weinig tegels bestellen. Een latere bestelling kan net anders van kleur zijn (een andere partij). Bestel alles in één keer, met 10% extra, en 15% bij visgraat of diagonaal.",
            "Een glanzende tegel op de vloer. Mooi in de showroom, maar glad met natte voeten.",
        ],
        tips=[
            "Leg dezelfde vloertegel door in de douche. Met een goot en afschot in één richting krijg je één rustig vlak zonder drempel.",
            "Bewaar een paar tegels uit dezelfde partij. Gaat er later een kapot, dan heb je een passende tegel.",
            "Gerectificeerde tegels (met rechte, geslepen randen) kunnen met een voeg van 2 mm. Niet-gerectificeerde tegels vragen 3 tot 5 mm.",
            "Bekijk tegels bij daglicht én bij de lampen die je in de badkamer wilt. Kleur en glans veranderen sterk met het licht.",
        ],
        faq=[
            ("Wat is het verschil tussen keramiek en porselein?", "Porselein is een soort keramiek die op hogere temperatuur wordt gebakken. Daardoor is het dichter en harder en neemt het bijna geen water op. Gewone keramische wandtegels zijn zachter en alleen geschikt voor de wand."),
            ("Welke antislipwaarde heb ik nodig in de badkamer?", "Voor de badkamervloer wordt vaak R10 of klasse B aangeraden; in de douche R11 of klasse B tot C. De R-waarde wordt met schoenen gemeten, de klasse A, B of C op blote voeten. Voor een badkamer zegt die laatste het meest."),
            ("Hoeveel tegels moet ik extra bestellen?", "Reken op 10% extra voor snijverlies bij stapelverband en halfsteens, en op 15% bij visgraat of diagonaal leggen. Bestel alles in één keer, zodat de kleur gelijk is."),
            ("Kan ik grote tegels in een kleine badkamer gebruiken?", "Ja. Grote tegels met weinig voegen laten een kleine ruimte vaak juist groter lijken. Let wel op het snijwerk rond de douche, het toilet en de afvoer, en op een vlakke ondergrond."),
            ("Wat betekent gerectificeerd?", "De randen van de tegel zijn na het bakken recht geslepen. Alle tegels zijn daardoor precies even groot en je kunt ze met een smalle voeg van ongeveer 2 mm leggen."),
        ],
        links=[("/kennisbank/tegels-kiezen/", "Kennisbank", "Tegels kiezen", "Formaat, materiaal, voegen en antislip."),
               ("/kennisbank/grote-tegels-badkamer/", "Kennisbank", "Grote tegels in de badkamer", "Wat je moet weten over 60 × 120 en groter."),
               ("/kosten/tegelzetter-per-m2/", "Kosten", "Tegelzetter per m²", "Legloon en materiaal met een rekenvoorbeeld."),
               ("/badkamerspullen/badkamertegels-kopen/", "Kopersgids", "Badkamertegels kopen", "Hoeveel je nodig hebt en waar je op let."),
               ("/inspiratie/zwart-wit-badkamer/", "Inspiratie", "Zwart-wit badkamer", "Contrast met tegels en voegen."),
               ("/diensten/tegelwerk-badkamer/", "Dienst", "Tegelwerk badkamer", "Offertes voor het tegelwerk vergelijken.")],
        tabel=dict(waar="Vloer, wand, douche", antislip="R10 tot R11 te kiezen", water="Tegel ja, voeg nee", prijs="€20 – €90 /m² + leggen"),
    ),
    dict(
        slug="natuursteen", naam="Natuursteen", kort="Natuursteen",
        seo="Natuursteen in de badkamer: marmer, hardsteen, travertin",
        h1="Natuursteen in de badkamer: marmer, hardsteen en travertin",
        description="Marmer, hardsteen of travertin in de badkamer? Eerlijke vergelijking van onderhoud, slijtvastheid, antislip en prijs per m², met getekende stalen en valkuilen.",
        oms="Marmer, hardsteen en travertin: elke tegel uniek, maar wel met onderhoud.",
        intro="Natuursteen geeft een badkamer iets dat geen print kan nadoen: elke tegel is anders. Marmer met zijn aders, het donkere blauwgrijs van hardsteen, de warme poriën van travertin. Maar natuursteen is een natuurproduct. Het is poreus, het reageert op zuren en het vraagt meer onderhoud dan een keramische tegel. Hieronder lees je per steen wat je kunt verwachten.",
        hero=[staal("marmer", "carrara", label="Wit marmer met grijze aders"), staal("hardsteen", "gezoet", label="Gezoet hardsteen, blauwgrijs met fossielen"),
              staal("travertin", "gevuld", label="Gevulde travertin met horizontale lagen")],
        soorten_titel="Drie bekende stenen, en hun varianten",
        soorten=[
            (staal("marmer", "carrara"), "Wit marmer (zoals Carrara)", "Wit tot lichtgrijs met fijne grijze aders. Klassiek en licht. Gevoelig voor zuur: citroen, azijn en ontkalker laten doffe plekken achter."),
            (staal("marmer", "calacatta"), "Marmer met brede aders", "Warmer wit met brede goudgrijze aders. Duurder, omdat zulke platen zeldzamer zijn. Op een wand of wastafelblad komt de tekening het best tot zijn recht."),
            (staal("marmer", "nero"), "Zwart marmer", "Diep zwart met witte aders. Heel sterk effect, maar kalk en zeepresten vallen erop op."),
            (staal("hardsteen", "gezoet"), "Hardsteen, gezoet", "Een harde blauwgrijze kalksteen met kleine witte fossielen. Gezoet betekent glad geschuurd, maar niet glanzend. Sterk en geschikt voor de vloer."),
            (staal("hardsteen", "gebouchardeerd"), "Hardsteen, gebouchardeerd", "Het oppervlak is opgeruwd met een hamer met punten. Lichter van kleur en stroever: meer grip, maar vuil hecht ook makkelijker."),
            (staal("travertin", "gevuld"), "Travertin, gevuld", "Een warme, beige kalksteen met gaatjes, die in de fabriek zijn gevuld. Rustig en zacht van uitstraling."),
            (staal("travertin", "ongevuld"), "Travertin, ongevuld", "Met open poriën. Mooi rustiek, maar in de douche verzamelen de gaatjes vuil en zeep. Kies daar de gevulde variant."),
        ],
        eig=dict(onderhoud=2, slijt=3,
                 onderhoud_t="Veel: impregneren na het leggen en daarna regelmatig opnieuw. Alleen pH-neutrale reinigers, geen azijn of ontkalker.",
                 slijt_t="Hardsteen is sterk. Marmer en travertin zijn zachter: ze krassen sneller en worden dof waar veel gelopen wordt.",
                 antislip="Gepolijste steen is glad als hij nat is. Kies op de vloer een gezoete, geschuurde of gezandstraalde afwerking.",
                 water="Poreus: neemt water, zeep en vuil op als hij niet goed geïmpregneerd is. Eronder hoort net als bij tegels een waterdichte laag."),
        prijs_eenheid="per m², inclusief btw; materiaal en leggen apart",
        prijzen=[("Hardsteen (materiaal)", 30, 130), ("Marmer (materiaal)", 50, 130), ("Leggen (legloon)", *_rp("tegelwerk"))],
        prijs_tekst="Volgens Werkspot kost hardsteen €30 tot €130 per m² en marmer €50 tot €130 per m², alleen voor de steen. Travertin valt meestal in dezelfde bandbreedte. Dikke platen, bijzondere aders en maatwerk zoals een wastafelblad zijn duurder. Voor het leggen geldt het gewone legloon van €25 tot €55 per m², maar reken bij natuursteen op de bovenkant: de tegels zijn zwaarder, vragen een geschikte lijm en moeten worden geïmpregneerd. Vraag het impregneren als aparte regel in de offerte.",
        bronnen=["werkspot_tegel", "slimster_natuursteen", "trustoo_tegel"],
        geschikt=[("Vloer", "ja", "Hardsteen en gezoete of geschuurde steen. Gepolijst marmer is op de vloer te glad."),
                  ("Wand", "ja", "Alle soorten. Op de wand slijt de steen nauwelijks en komt de tekening mooi uit."),
                  ("Douche", "let", "Kan, maar zeep, kalk en ontkalker tasten marmer en travertin aan. Goed impregneren en droogtrekken na het douchen.")],
        valkuilen=[
            "Zure schoonmaakmiddelen. Marmer, travertin en ook hardsteen zijn kalksteen: azijn, citroen, ontkalker en veel toiletreinigers etsen doffe plekken in het oppervlak.",
            "De verkeerde lijm. Lichte steen kan verkleuren door grijze lijm of vocht van onderen. Een tegelzetter met ervaring gebruikt een lijm die geschikt is voor natuursteen.",
            "Verwachten dat elke tegel gelijk is. Kleur en aders verschillen per plaat. Leg de tegels vooraf los uit en kies samen welke waar komt.",
            "Niet opnieuw impregneren. Na een paar jaar trekt water weer de steen in. Een simpele test: blijft een druppel water staan of trekt hij in?",
            "Ongevulde travertin in de douche. De open gaatjes vangen zeep en vuil.",
        ],
        tips=[
            "Twijfel je over het onderhoud? Kies natuursteen voor de wand of het wastafelblad en een keramische tegel voor de douchevloer.",
            "Natuursteenlook in porselein lijkt van een afstand sterk op echte steen en vraagt bijna geen onderhoud.",
            "Vraag naar de afwerking: gepolijst (glanzend), gezoet (glad en mat), geschuurd of gezandstraald (stroef).",
        ],
        faq=[
            ("Is marmer geschikt voor de badkamer?", "Ja, maar het vraagt zorg. Marmer is poreus en reageert op zuur. Laat het impregneren, gebruik alleen pH-neutrale reinigers en kies op de vloer een gezoete of geschuurde afwerking in plaats van gepolijst."),
            ("Hoe vaak moet je natuursteen impregneren?", "Na het leggen altijd, en daarna afhankelijk van het product en het gebruik. In de douche vaker dan op een wand buiten de natte zone. Een waterdruppel die in de steen trekt, betekent dat het weer tijd is."),
            ("Is hardsteen hetzelfde als graniet?", "Nee. Belgisch hardsteen is een kalksteen en dus gevoelig voor zuur. Graniet is een stollingsgesteente en veel minder gevoelig voor zuur."),
            ("Wat kost natuursteen in de badkamer?", "De steen kost ongeveer €30 tot €130 per m², afhankelijk van de soort en de dikte. Daar komen het leggen, lijm en impregneren bij. Vraag een offerte waarin dat apart staat."),
        ],
        links=[("/inspiratie/marmer-badkamer/", "Inspiratie", "Marmer badkamer", "Hoe marmer in een hele badkamer oogt."),
               ("/inspiratie/klassieke-badkamer/", "Inspiratie", "Klassieke badkamer", "Natuursteen, messing en paneeldeuren."),
               ("/kennisbank/tegels-kiezen/", "Kennisbank", "Tegels kiezen", "Keramiek, porselein of natuursteen."),
               ("/kennisbank/badkamer-schoonmaken/", "Kennisbank", "Badkamer schoonmaken", "Welke middelen je wel en niet gebruikt."),
               ("/kosten/luxe-badkamer/", "Kosten", "Luxe badkamer", "Wat bijzondere materialen doen met de prijs.")],
        tabel=dict(waar="Vloer, wand, douche met zorg", antislip="Alleen gezoet of geschuurd", water="Poreus, impregneren", prijs="€30 – €130 /m² + leggen"),
    ),
    dict(
        slug="microcement", naam="Microcement", kort="Microcement",
        seo="Microcement in de badkamer: eigenschappen en prijs",
        h1="Microcement in de badkamer: naadloos, maar niet vanzelf waterdicht",
        description="Microcement geeft een naadloze wand en vloer zonder voegen. Wat het kost per m², hoe waterdicht het is, hoeveel onderhoud het vraagt en welke valkuilen je vermijdt.",
        oms="Naadloos en wolkerig, zonder voegen. Mooi, maar alleen met een goede ondergrond.",
        intro="Microcement is een dunne laag van cement, kunsthars en pigment die in een paar lagen met de hand wordt aangebracht. Het resultaat is een naadloos oppervlak met een zachte, wolkerige tekening. Geen voegen, dus een rustig beeld. Maar de laag is maar 2 tot 3 millimeter dik. Alles wat eronder beweegt of scheurt, zie je terug. En waterdicht is het pas met de juiste lagen eronder en erop.",
        hero=[staal("micro", "kalkwit", label="Microcement in kalkwit"), staal("micro", "betongrijs", label="Microcement in betongrijs"),
              staal("micro", "terra", label="Microcement in een warme terratint")],
        soorten_titel="Kleuren en afwerking",
        soorten=[
            (staal("micro", "kalkwit"), "Kalkwit", "Licht en zacht. Laat de ruimte groter lijken, maar kalk en vlekken vallen minder op dan bij donker."),
            (staal("micro", "greige"), "Greige", "Een mengsel van grijs en beige. Warm en rustig, past bij hout en messing."),
            (staal("micro", "betongrijs"), "Betongrijs", "De klassieke betonlook. Stoer, en vergevingsgezind voor vlekken."),
            (staal("micro", "antraciet"), "Antraciet", "Donker en sterk. Witte kalkranden zijn hier het best zichtbaar."),
            (staal("micro", "salie"), "Saliegroen", "Een zachte groentint. Elke kleur kan, want het pigment wordt gemengd."),
            (staal("micro", "terra"), "Terra", "Een warme aardtint. Mooi bij veel daglicht en natuurlijke materialen."),
        ],
        eig=dict(onderhoud=3, slijt=3,
                 onderhoud_t="Gemiddeld: milde, pH-neutrale reiniger. De beschermende sealer heeft na een aantal jaren een nieuwe laag nodig, eerder op de vloer dan op de wand.",
                 slijt_t="Redelijk. Krassen en plekken waar veel gelopen wordt, slijten de sealer. Een plek herstellen zonder dat je het ziet, is lastig.",
                 antislip="Glad als het nat is. Vraag voor de vloer en de douche om een antislip-toplaag of korrel in de laatste laag.",
                 water="Niet vanzelf. De sealer maakt het waterafstotend. In de douche hoort er een afdichtingslaag onder het microcement."),
        prijs_eenheid="per m², inclusief materiaal, arbeid en btw",
        prijzen=[("Wand en vloer", 100, 180), ("Inloopdouche", 150, 200)],
        prijs_tekst="Werkspot noemt €100 tot €150 per m², Homedeal €120 tot €180 per m² voor vloer en wanden en €150 tot €200 per m² in een inloopdouche. Dat is inclusief materiaal, arbeid en btw. Bij een klein oppervlak rekenen veel verwerkers een starttarief. Moet de ondergrond eerst worden hersteld of moet er een afdichtingslaag onder, dan komt dat erbij.",
        bronnen=["werkspot_micro", "homedeal_micro", "slimster_micro"],
        geschikt=[("Wand", "ja", "Het mooiste resultaat, en de laag wordt hier het minst belast."),
                  ("Vloer", "let", "Kan, ook met vloerverwarming als het systeem dat toelaat. De sealer slijt sneller; reken op onderhoud."),
                  ("Douche", "let", "Alleen met een afdichtingslaag eronder en een verwerker met ervaring in natte ruimten.")],
        valkuilen=[
            "Een ondergrond die werkt. Op hout, losse tegels of naden in gipsplaat ontstaan haarscheurtjes. Laat de ondergrond eerst beoordelen.",
            "Denken dat microcement zelf waterdicht is. Zonder afdichting eronder kan water via kleine scheurtjes in de ondergrond komen.",
            "Een verwerker zonder ervaring. Microcement is handwerk; het verschil tussen een mooie wolk en vlekken zit in de hand van de vakman. Vraag naar eerder werk.",
            "Te snel in gebruik nemen. Er gaan meerdere lagen op, met droogtijd ertussen. Reken op een aantal dagen dat je de badkamer niet kunt gebruiken.",
            "Haarverf, zelfbruiner en schurende middelen. Die laten vlekken achter als de sealer beschadigd is.",
        ],
        tips=[
            "Microcement kan vaak over bestaande tegels heen, als ze vast en vlak zijn. Dat scheelt sloopwerk.",
            "Vraag welk systeem de verwerker gebruikt, en welke reinigers en welk onderhoud daarbij horen. Leg dat vast.",
            "Combineer: microcement op de wanden en een tegelvloer in de douche geeft het naadloze beeld met minder risico.",
        ],
        faq=[
            ("Is microcement waterdicht?", "Niet vanzelf. De sealer maakt het waterafstotend, maar in de douche hoort er een afdichtingslaag onder. Dan is de combinatie waterdicht, net als bij tegels."),
            ("Kan microcement over tegels heen?", "Vaak wel, als de tegels vast zitten en vlak liggen. De voegen worden eerst gevuld en er komt een hechtlaag op. Losse of holle tegels moeten eerst worden hersteld."),
            ("Hoe lang gaat microcement mee?", "Met goed onderhoud vele jaren. De sealer is het deel dat slijt; die krijgt na een aantal jaren een nieuwe laag. Vraag de verwerker hoe vaak dat bij zijn systeem nodig is."),
            ("Wat kost microcement per m²?", "Ongeveer €100 tot €180 per m², en €150 tot €200 per m² in een douche, inclusief materiaal, arbeid en btw. Bij een klein oppervlak komt er vaak een starttarief bij."),
        ],
        links=[("/kennisbank/microcement-badkamer/", "Kennisbank", "Microcement in de badkamer", "Hoe het werkt en wat eronder moet."),
               ("/kennisbank/badkamer-zonder-tegels/", "Kennisbank", "Badkamer zonder tegels", "Alternatieven voor tegels naast elkaar."),
               ("/kennisbank/badkamer-waterdicht-maken/", "Kennisbank", "Badkamer waterdicht maken", "Wat er onder de afwerking hoort."),
               ("/inspiratie/industriele-badkamer/", "Inspiratie", "Industriële badkamer", "Betonlook met zwart staal en hout."),
               ("/inspiratie/wellness-badkamer/", "Inspiratie", "Wellness badkamer", "Rust, warmte en zachte materialen.")],
        tabel=dict(waar="Wand; vloer en douche met zorg", antislip="Alleen met antislip-toplaag", water="Alleen met afdichting eronder", prijs="€100 – €200 /m² alles inbegrepen"),
    ),
    dict(
        slug="terrazzo", naam="Terrazzo", kort="Terrazzo",
        seo="Terrazzo in de badkamer: tegels, gegoten en prijs",
        h1="Terrazzo in de badkamer: van fijne spikkel tot grove korrel",
        description="Terrazzo in de badkamer: echte terrazzotegels, terrazzolook in porselein of een gegoten vloer. Getekende stalen per korrel, eigenschappen, prijs per m² en valkuilen.",
        oms="Spikkels van steen in een egale basis. Als tegel, als print of gegoten.",
        intro="Terrazzo is een mengsel van stukjes marmer, graniet of glas in cement of hars, dat na het uitharden glad wordt geslepen. Het resultaat is een vrolijk of juist rustig spikkelpatroon, afhankelijk van de korrel en de kleuren. Je kunt kiezen uit drie vormen: echte terrazzotegels, keramische tegels met een terrazzoprint, of een vloer die op locatie wordt gegoten. Ze lijken op elkaar, maar verschillen veel in onderhoud en prijs.",
        hero=[staal("terrazzo", "fijn", label="Terrazzo met fijne korrel"), staal("terrazzo", "middel", label="Terrazzo met middelgrote korrel"),
              staal("terrazzo", "grof", label="Terrazzo met grove korrel")],
        soorten_titel="Korrels en kleuren",
        soorten=[
            (staal("terrazzo", "fijn"), "Fijne korrel", "Kleine spikkels van een paar millimeter. Van dichtbij levendig, van een afstand bijna egaal. Rustig en tijdloos."),
            (staal("terrazzo", "middel"), "Middelgrote korrel", "De bekende terrazzo met duidelijke stukjes steen in verschillende kleuren."),
            (staal("terrazzo", "grof"), "Grove korrel", "Grote brokken steen. Een uitgesproken vloer of wand die de aandacht trekt."),
            (staal("terrazzo", "kleur"), "Kleurrijk", "Gekleurde stukjes in een lichte basis. Speels, mooi in een kleine badkamer of een toilet."),
            (staal("terrazzo", "donker"), "Donkere basis", "Lichte korrels in een antraciet basis. Stoer, en vlekken vallen minder op."),
        ],
        eig=dict(onderhoud=3, slijt=4,
                 onderhoud_t="Echte terrazzo: impregneren en geen zure middelen, want er zit marmer in. Terrazzolook in porselein: net zo makkelijk als een gewone tegel.",
                 slijt_t="Hard en slijtvast. Een gegoten vloer kan na jaren opnieuw worden geslepen.",
                 antislip="Gepolijst is glad. Kies op de vloer een gezoete of geschuurde afwerking, of een terrazzolook-tegel met R10.",
                 water="Echte terrazzo is licht poreus en moet worden geïmpregneerd. Porselein met terrazzoprint neemt bijna geen water op."),
        prijs_eenheid="per m², inclusief btw",
        prijzen=[("Terrazzolook-tegel (materiaal)", *_rp("tegels")), ("Leggen tegels (legloon)", *_rp("tegelwerk")), ("Gegoten terrazzovloer (alles)", 120, 280)],
        prijs_tekst="Terrazzotegels en porselein met een terrazzoprint vallen meestal in de gewone tegelprijs van €20 tot €60 per m², plus het legloon. Een gegoten terrazzovloer (ook wel granito) is maatwerk: volgens Slimster €120 tot €280 per m² inclusief btw. Bij een groter oppervlak daalt de prijs per m². Een gegoten vloer kost op locatie al gauw één tot twee weken werk.",
        bronnen=["werkspot_tegel", "slimster_badkamer", "trustoo_tegel", "slimster_granito"],
        geschikt=[("Vloer", "ja", "Tegels en gegoten vloeren, met een stroeve afwerking."),
                  ("Wand", "ja", "Tegels. Een terrazzowand achter de wastafel is een mooie blikvanger."),
                  ("Douche", "let", "Tegels gaan goed. Een gegoten vloer met afschot naar de afvoer vraagt een vakman met ervaring.")],
        valkuilen=[
            "Zure reinigers op echte terrazzo. De stukjes marmer worden dof en ruw.",
            "Een printtegel met weinig variatie. Als er maar een paar verschillende drukken zijn, zie je het patroon terugkomen. Vraag hoeveel verschillende tegelvlakken er in de serie zitten.",
            "Een gegoten vloer zonder voorbereiding. De vloer moet stevig, vlak en droog zijn. Anders ontstaan er scheuren.",
            "Te druk combineren. Een grove kleurrijke terrazzo naast een uitgesproken wandtegel is snel te veel. Kies één blikvanger.",
        ],
        tips=[
            "Kies de voegkleur in de basiskleur van de terrazzo. Dan lopen de tegels rustig in elkaar over.",
            "Fijne korrel en een lichte basis passen in bijna elke stijl. Grove korrel en veel kleur zijn persoonlijker.",
            "Neem een stuk terrazzo mee naar huis en leg het naast je meubel, kranen en wandkleur.",
        ],
        faq=[
            ("Is terrazzo geschikt voor de badkamer?", "Ja. Terrazzotegels en terrazzolook in porselein zijn prima voor vloer en wand. Kies op de vloer een stroeve afwerking en laat echte terrazzo impregneren."),
            ("Wat is het verschil tussen terrazzo en granito?", "Granito is een andere naam voor terrazzo, vooral voor vloeren die op locatie worden gegoten en geslepen."),
            ("Hoe maak je terrazzo schoon?", "Met een pH-neutrale reiniger en een zachte doek of mop. Geen azijn, ontkalker of schuurmiddel. Terrazzolook in porselein maak je schoon als een gewone tegel."),
            ("Wat kost een terrazzovloer?", "Terrazzotegels kosten ongeveer €20 tot €60 per m² plus het leggen. Een gegoten vloer kost €120 tot €280 per m² inclusief btw."),
        ],
        links=[("/inspiratie/terrazzo-badkamer/", "Inspiratie", "Terrazzo badkamer", "Zo oogt terrazzo in een hele badkamer."),
               ("/inspiratie/scandinavische-badkamer/", "Inspiratie", "Scandinavische badkamer", "Licht, hout en een speelse vloer."),
               ("/kennisbank/tegels-kiezen/", "Kennisbank", "Tegels kiezen", "Formaat, materiaal en antislip."),
               ("/kosten/tegelzetter-per-m2/", "Kosten", "Tegelzetter per m²", "Wat het leggen kost.")],
        tabel=dict(waar="Vloer, wand; douche met tegels", antislip="Gezoet of R10-tegel", water="Echt: impregneren", prijs="€20 – €60 /m² tegel; gegoten €120 – €280"),
    ),
    dict(
        slug="kraanafwerkingen", naam="Kraanafwerkingen", kort="Kranen",
        seo="Kraanafwerkingen: chroom, mat zwart, goud en gunmetal",
        h1="Kraanafwerkingen: chroom, mat zwart, RVS, goud en gunmetal",
        description="Chroom, mat zwart, geborsteld RVS, geborsteld goud of gunmetal? Vergelijk kraanafwerkingen op kalk, krassen, onderhoud en prijs, met getekende metalen stalen.",
        oms="Chroom, mat zwart, geborsteld RVS, geborsteld goud en gunmetal naast elkaar.",
        intro="Kranen bepalen voor een groot deel de sfeer van een badkamer. Chroom is klassiek en makkelijk, mat zwart grafisch, geborsteld goud warm en gunmetal stoer. Maar elke afwerking gedraagt zich anders met kalk, vingers en schoonmaakmiddelen. Hieronder zie je ze getekend naast elkaar en lees je waar je op let.",
        hero=[staal("metaal", "chroom", label="Kraan in chroom"), staal("metaal", "zwart", label="Kraan in mat zwart"),
              staal("metaal", "goud", label="Kraan in geborsteld goud")],
        soorten_titel="Vijf afwerkingen",
        soorten=[
            (staal("metaal", "chroom"), "Chroom", "Een glanzende laag over messing. Hard, goedkoop en makkelijk schoon te poetsen. Kalkvlekken en vingers zie je wel, maar ze zijn er ook snel af."),
            (staal("metaal", "zwart"), "Mat zwart", "Grafisch en strak. Gemaakt met een coating of met PVD. Kalk laat witte randen achter; droog de kraan na gebruik."),
            (staal("metaal", "rvs"), "RVS geborsteld", "Een matte metaalkleur met fijne krasjes in één richting. Verbergt vingers en kalk goed. Massief RVS of een RVS-kleurige PVD-laag op messing."),
            (staal("metaal", "goud"), "Goud geborsteld", "Warm en luxe, bijna altijd met PVD. De tint verschilt per merk: van licht champagne tot diep messing."),
            (staal("metaal", "gunmetal"), "Gunmetal", "Een donker metaalgrijs, tussen zwart en RVS in. Stoer, en minder gevoelig voor kalkranden dan mat zwart."),
        ],
        afwerkingen=[("Chroom", "Zeer goed", "Zichtbaar, makkelijk weg", "Laagste"),
                     ("Mat zwart", "Coating: matig; PVD: goed", "Goed zichtbaar", "Iets hoger"),
                     ("RVS geborsteld", "Goed", "Weinig zichtbaar", "Iets hoger"),
                     ("Goud geborsteld", "Goed (PVD)", "Weinig zichtbaar", "Hoger"),
                     ("Gunmetal", "Goed (PVD)", "Redelijk zichtbaar", "Hoger")],
        eig=dict(onderhoud=4, slijt=4,
                 onderhoud_t="Afnemen met een zachte doek en een milde reiniger, en na gebruik droogmaken. Geen schuurspons of agressieve ontkalker.",
                 slijt_t="Chroom en PVD zijn hard en krasvast. Een gewone poedercoating (vaak bij goedkoop mat zwart) kan beschadigen bij krassen.",
                 antislip="Niet van toepassing.",
                 water="Niet van toepassing. Wel belangrijk: hoe zichtbaar is kalk? Op glanzend en donker het meest."),
        prijs_eenheid="per wastafelkraan, inclusief btw",
        prijzen=[("Wastafelkraan, instap (alle kleuren)", 60, 170), ("Wastafelkraan, middensegment", 150, 450), ("Kraan laten plaatsen (uurtarief, excl. btw)", *_rp("uurtarief"))],
        prijs_tekst="In onze steekproef van winkelprijzen (november 2026) kost een eenvoudige wastafelkraan in mat zwart, gunmetal of goud ongeveer €60 tot €170. Kranen uit het middensegment en inbouwkranen kosten al snel €150 tot €450 (eigen inschatting). Binnen dezelfde serie is een gekleurde PVD-afwerking meestal iets duurder dan chroom. Voor het plaatsen rekent een installateur zijn uurtarief van €45 tot €85 exclusief btw, plus voorrijkosten.",
        bronnen=["steekproef", "homedeal_lood", "knab_lood"],
        geschikt=[("Wastafel", "ja", "Alle afwerkingen. Hier pak je de kraan het vaakst vast; geborsteld verbergt vingers het best."),
                  ("Douche", "ja", "Geborsteld RVS en gunmetal verbergen kalk het best. Mat zwart vraagt droogtrekken."),
                  ("Hard water", "let", "In gebieden met hard water valt kalk op mat zwart en glanzend chroom het meest op. Chroom is wel het makkelijkst schoon te maken.")],
        valkuilen=[
            "Afwerkingen van verschillende merken combineren. 'Goud' of 'gunmetal' is bij elk merk een andere tint. Kies kranen, douche en accessoires uit één serie, of leg ze vooraf naast elkaar.",
            "Schuurmiddelen en sterke ontkalkers. Die maken een coating dof of laten hem loskomen. Volg de schoonmaakadviezen van de fabrikant, anders kan de garantie vervallen.",
            "Denken dat 'RVS-look' massief RVS is. Vaak is het een kleurlaag op messing. Dat is prima, maar gedraagt zich anders bij een diepe kras.",
            "Mat zwart in een badkamer met hard water en zonder droogtrekken. Witte kalkranden zijn binnen een week zichtbaar.",
        ],
        tips=[
            "Twijfel je? Geborsteld RVS of gunmetal is het meest vergevingsgezind voor kalk en vingers.",
            "Vraag naar PVD. Dat is een heel dunne, harde laag die veel krasvaster is dan gewone lak of poedercoating.",
            "Laat de kleur van de kranen terugkomen in de afvoer, de bedieningsplaat van het toilet en de douchegoot. Dan oogt het als één geheel.",
        ],
        faq=[
            ("Welke kraanafwerking is het makkelijkst schoon te houden?", "Geborsteld RVS en gunmetal verbergen kalk en vingers het best. Chroom laat meer zien, maar is wel het snelst schoon te poetsen."),
            ("Wat is PVD?", "PVD staat voor physical vapour deposition. Daarbij wordt een heel dunne, harde metaallaag op de kraan aangebracht. Die is krasvaster dan lak of poedercoating en wordt veel gebruikt voor goud, gunmetal en geborsteld RVS."),
            ("Worden mat zwarte kranen grijs?", "Een goede mat zwarte kraan blijft zwart. Wat grijs lijkt, is meestal kalk. Droog de kraan na gebruik af en gebruik geen schuurmiddel."),
            ("Kan ik verschillende kraankleuren combineren?", "Dat kan, bijvoorbeeld zwart in de douche en goud bij de wastafel. Houd het bij twee afwerkingen en laat elke kleur op meer plekken terugkomen."),
        ],
        links=[("/badkamerspullen/kranen-kiezen/", "Kopersgids", "Kranen kiezen", "Soorten kranen en waar je op let."),
               ("/kennisbank/inbouwkranen/", "Kennisbank", "Inbouwkranen", "Strak in de wand: wat erbij komt kijken."),
               ("/kennisbank/kalk-en-waterhardheid/", "Kennisbank", "Kalk en waterhardheid", "Waarom kalk op sommige kranen meer opvalt."),
               ("/kosten/kraan-vervangen/", "Kosten", "Kraan vervangen", "Wat een nieuwe kraan met montage kost."),
               ("/inspiratie/zwart-wit-badkamer/", "Inspiratie", "Zwart-wit badkamer", "Mat zwart als rode draad.")],
        tabel=dict(waar="Wastafel, douche, bad", antislip="n.v.t.", water="n.v.t.; kalk zichtbaar op zwart en chroom", prijs="€60 – €450 per kraan"),
    ),
    dict(
        slug="douchewand-glas", naam="Glas voor de douchewand", kort="Glas",
        seo="Douchewand glas: helder, getint, geribbeld of mat",
        h1="Glas voor je douchewand: helder, getint, geribbeld of mat",
        description="Helder, extra helder, rookglas, brons, geribbeld of mat glas voor de douchewand. Wat je ziet, hoeveel kalk opvalt, hoe dik het moet zijn en wat het ongeveer kost.",
        oms="Helder, getint, geribbeld of mat: wat je ziet en hoeveel kalk opvalt.",
        intro="Een douchewand van glas houdt het water binnen zonder de ruimte dicht te maken. Maar glas is niet gewoon glas. Helder glas laat alles zien, ook kalk. Rookglas geeft sfeer en wat privacy. Geribbeld glas vervormt het beeld erachter en is weer helemaal in. Mat glas geeft de meeste privacy. In de getekende stalen hieronder zie je hetzelfde achtergrondbeeld door elk soort glas.",
        hero=[staal("glas", "helder", label="Helder glas met een tegelwand erachter"), staal("glas", "ribbel", label="Geribbeld glas dat het beeld erachter vervormt"),
              staal("glas", "rook", label="Getint rookglas")],
        soorten_titel="Zes soorten glas",
        soorten=[
            (staal("glas", "helder"), "Helder glas", "De standaard. Licht groen aan de rand, doordat er wat ijzer in zit. Laat de ruimte doorlopen."),
            (staal("glas", "extra"), "Extra helder glas", "Glas met minder ijzer, dus zonder groene zweem. Vooral mooi bij brede panelen en witte tegels."),
            (staal("glas", "rook"), "Rookglas (getint grijs)", "Geeft sfeer en een beetje privacy. Kalk en zeepresten vallen op als witte vlekken."),
            (staal("glas", "brons"), "Bronsglas", "Een warme tint. Past bij geborsteld goud, messing en hout."),
            (staal("glas", "ribbel"), "Geribbeld glas", "Verticale ribbels vervormen het beeld erachter. Privacy met licht. In de ribbels blijft wel sneller kalk zitten."),
            (staal("glas", "mat"), "Mat glas", "Gezandstraald of geëtst. De meeste privacy. Vingers en vet zijn soms zichtbaar als vlekken."),
        ],
        eig=dict(onderhoud=3, slijt=4,
                 onderhoud_t="Na elke douchebeurt aftrekken met een wisser houdt kalk weg. Een anti-kalkcoating helpt, maar vervangt dat niet.",
                 slijt_t="Gehard veiligheidsglas is sterk en krast niet snel. Schuurmiddel kan een coating wel beschadigen.",
                 antislip="Niet van toepassing.",
                 water="Glas zelf is waterdicht. Spatwater langs een open wand is het punt: een inloopwand van minder dan 90 cm laat vaak water door."),
        prijs_eenheid="inclusief btw",
        prijzen=[("Glazen inloopwand (paneel)", 200, 750), ("Plaatsen douche of douchewand", *_rp("montage_douche")),
                 ("Complete douche, midden", *_niv("sanitair_douche", "midden"))],
        prijs_tekst="In onze steekproef van winkelprijzen (november 2026) kost een glazen inloopwand van 8 mm dik en 80 tot 100 cm breed ongeveer €200 tot €750. Rookglas, bronsglas en vooral ribbelglas zitten meestal hoger dan helder glas van dezelfde maat, net als een zwart of geborsteld profiel. Het plaatsen kost €400 tot €800. Een complete douche met goot, wand en kraan in het middensegment kost €1.000 tot €2.200.",
        bronnen=["steekproef", "werkspot_sanitair", "homedeal_douche"],
        geschikt=[("Inloopdouche", "ja", "Alle soorten glas. Kies 8 mm veiligheidsglas en minstens 90 cm breed."),
                  ("Douchecabine of deur", "ja", "Helder of getint glas met een deur die naar buiten draait."),
                  ("Badwand", "ja", "Een vast of draaibaar paneel. Getint of ribbelglas geeft het bad wat beschutting.")],
        valkuilen=[
            "Denken dat een anti-kalkcoating onderhoud overbodig maakt. Ook daarop blijft kalk achter als je niet aftrekt.",
            "Ribbelglas in een gebied met hard water. In de groefjes blijft kalk zitten; schoonmaken kost meer tijd.",
            "Een te smalle inloopwand. Met minder dan 90 cm, of een regendouche dicht bij de opening, staat de badkamer na elke douchebeurt nat.",
            "Glas bestellen voordat de tegels er liggen. Wanden en vloer zijn zelden precies haaks; meet na het tegelen.",
        ],
        tips=[
            "Hang een wisser in de douche en trek het glas na elke beurt af. Dat is de beste bescherming tegen kalk.",
            "Laat het profiel dezelfde kleur hebben als de kranen.",
            "Extra helder glas is het waard bij een brede wand van 120 cm of meer en lichte tegels.",
        ],
        faq=[
            ("Hoe dik moet glas voor een douchewand zijn?", "Voor een vrijstaande inloopwand is 8 mm gehard veiligheidsglas gebruikelijk. Bij brede panelen of zonder stabilisatiestang kiezen fabrikanten vaak 10 mm. Deuren en cabines zijn soms 6 mm."),
            ("Welk glas laat de minste kalk zien?", "Helder glas en mat glas laten kalk het minst opvallen. Op rookglas zie je witte vlekken, en in ribbelglas blijft kalk in de groefjes zitten."),
            ("Is geribbeld glas lastig schoon te houden?", "Iets lastiger dan vlak glas, omdat kalk in de groefjes blijft. Met een wisser en een zachte borstel gaat het goed. Bij hard water is het meer werk."),
            ("Wat kost een glazen douchewand?", "Een glazen inloopwand kost ongeveer €200 tot €750, afhankelijk van maat, glas en profiel. Plaatsen kost €400 tot €800."),
        ],
        links=[("/badkamerspullen/douchewand-kiezen/", "Kopersgids", "Douchewand kiezen", "Maten, profielen en deuren."),
               ("/badkamerspullen/inloopdouche-kopen/", "Kopersgids", "Inloopdouche kopen", "Glas, afvoer en maten."),
               ("/kosten/inloopdouche/", "Kosten", "Kosten inloopdouche", "Wat een inloopdouche compleet kost."),
               ("/kennisbank/kalk-en-waterhardheid/", "Kennisbank", "Kalk en waterhardheid", "Minder kalk op glas en kranen."),
               ("/inspiratie/luxe-badkamer/", "Inspiratie", "Luxe badkamer", "Brede glazen wanden en warme tinten.")],
        tabel=dict(waar="Douche, bad", antislip="n.v.t.", water="Glas ja; let op spatwater", prijs="€200 – €750 per wand + plaatsen"),
    ),
    dict(
        slug="meubelmaterialen", naam="Meubelmaterialen", kort="Meubel",
        seo="Badkamermeubel materialen: hout, lak, HPL en keramiek",
        h1="Materialen voor het badkamermeubel: hout, lak, HPL en keramiek",
        description="Eiken fineer, notenhout, gelakt MDF, HPL of een keramisch blad? Vergelijk badkamermeubel materialen op vocht, krassen en onderhoud, met richtprijzen en getekende stalen.",
        oms="Fineer, lak, HPL, massief hout en keramiek: wat kan tegen vocht?",
        intro="Een badkamermeubel staat elke dag in de damp en krijgt spatwater over zich heen. Het materiaal van de kast en het blad bepaalt of hij er na tien jaar nog netjes uitziet. Het grootste risico zit niet in het oppervlak, maar in de randen: daar komt water bij de kern. Hieronder zie je de bekendste materialen.",
        hero=[staal("hout", "eiken", label="Eiken fineer met een rustige nerf"), staal("hout", "lakgroen", label="Mat gelakt front in groen"),
              staal("hout", "keramisch", label="Keramisch blad in marmerlook")],
        soorten_titel="Materialen voor kast en blad",
        soorten=[
            (staal("hout", "eiken"), "Eiken fineer", "Een dun laagje echt eiken op een plaat. Warm en natuurlijk, met een goede lak beschermd. Veel gebruikt en betaalbaar."),
            (staal("hout", "noten"), "Notenhout (fineer)", "Donker en chique. Net als eiken een laag echt hout op een plaat."),
            (staal("hout", "massief"), "Massief hout", "Mooi en te herstellen door te schuren. Werkt wel: het zet uit en krimpt met vocht. Alleen met goede ventilatie en olie of lak."),
            (staal("hout", "lakwit"), "Gelakt MDF, wit", "Strak en naadloos, in elke kleur. Hoogglans laat krassen zien, mat laat vingers zien."),
            (staal("hout", "lakgroen"), "Gelakt MDF, in kleur", "Een kleur geeft karakter. Vochtbestendig MDF (vaak met een groene kern) is hier de basis."),
            (staal("hout", "hpl"), "HPL en compact", "Een harde kunststof toplaag, vaak in beton- of houtlook. Compact is massief HPL: tegen water bestand, ook aan de randen."),
            (staal("hout", "keramisch"), "Keramisch of composiet blad", "Een blad van porselein, keramiek of een mineraal composiet. Waterdicht, hittebestendig en krasvast."),
        ],
        eig=dict(onderhoud=3, slijt=3,
                 onderhoud_t="Spatwater direct afnemen, vooral op de randen en rond de kraan. Geen natte doekjes laten liggen.",
                 slijt_t="HPL, compact en keramiek zijn het meest krasvast. Hoogglans lak en zacht hout krassen het snelst.",
                 antislip="Niet van toepassing.",
                 water="Spaanplaat en gewoon MDF zwellen als water bij de randen komt. Let op afgewerkte randen en een kitnaad tussen blad en wand."),
        prijs_eenheid="per wastafelmeubel met wastafel, kraan en spiegel, inclusief btw",
        prijzen=[("Basis (vaak melamine of folie)", *_niv("sanitair_meubel", "basis")), ("Midden (lak of fineer)", *_niv("sanitair_meubel", "midden")),
                 ("Luxe (massief, keramisch blad)", *_niv("sanitair_meubel", "luxe")), ("Ophangen en aansluiten", *_rp("montage_meubel"))],
        prijs_tekst="Een wastafelmeubel met wastafel, kraan en spiegel kost volgens onze richtprijzen €250 tot €2.500. Grofweg vind je melamine en folie in de basis, lak en fineer in het midden en massief hout, compact en keramische of composiet bladen in de luxe klasse. Ophangen en aansluiten kost €200 tot €600.",
        bronnen=["werkspot_sanitair", "eigen"],
        geschikt=[("Naast de douche", "let", "Kies HPL, compact of een goed afgewerkt gelakt front. Fineer en massief hout alleen buiten het spatwater."),
                  ("Bij de wastafel", "ja", "Alle materialen, als de randen dicht zijn en er een kitnaad langs de wand zit."),
                  ("Badkamer zonder raam", "let", "Veel damp vraagt een vochtbestendige kern en goede ventilatie. Massief hout kan hier gaan werken.")],
        valkuilen=[
            "Open randen en boorgaten. Een niet-afgewerkte rand of het gat voor de afvoer laat vocht in de plaat; die zwelt dan op.",
            "Gewoon MDF of spaanplaat in plaats van een vochtbestendige soort. Vraag naar de kern, niet alleen naar het front.",
            "Massief hout in een slecht geventileerde badkamer. Het hout trekt krom en kan scheuren.",
            "Hoogglans in een drukke gezinsbadkamer. Elke kras en elk vingerspoor valt op.",
        ],
        tips=[
            "Een zwevend meubel houdt de vloer vrij van spatwater en maakt dweilen makkelijk.",
            "Kies RVS-scharnieren en ladegeleiders. Gewoon staal kan in de badkamer gaan roesten.",
            "Een keramisch blad met geïntegreerde wastafel heeft geen naad waar water in kan.",
        ],
        faq=[
            ("Welk materiaal is het beste voor een badkamermeubel?", "Voor de kast werken vochtbestendig MDF met lak, fineer met een goede lak en HPL allemaal goed, mits de randen dicht zijn. Voor het blad zijn keramiek, composiet en compact het sterkst tegen water."),
            ("Kan een houten meubel in de badkamer?", "Ja, als het goed is gelakt of geolied en de badkamer goed wordt geventileerd. Houd het buiten het directe spatwater van de douche."),
            ("Waarom zwelt een badkamermeubel op?", "Omdat er water in de kern komt, meestal via een open rand, een boorgat of een kapotte kitnaad. Spaanplaat en gewoon MDF zwellen dan op en dat herstelt niet."),
            ("Wat is het verschil tussen HPL en compact?", "HPL is een dunne harde toplaag op een plaat. Compact is helemaal van HPL-materiaal. Compact is daardoor ook aan de randen tegen water bestand."),
        ],
        links=[("/badkamerspullen/wastafelmeubel-kiezen/", "Kopersgids", "Wastafelmeubel kiezen", "Maten, soorten wasbakken en materialen."),
               ("/kosten/badkamermeubel-plaatsen/", "Kosten", "Badkamermeubel plaatsen", "Wat ophangen en aansluiten kost."),
               ("/badkamerspullen/spiegelkast-kiezen/", "Kopersgids", "Spiegelkast kiezen", "Opbergen boven de wastafel."),
               ("/kennisbank/badkamer-ventilatie/", "Kennisbank", "Badkamer ventileren", "Minder vocht, langer mooi meubel."),
               ("/inspiratie/japandi-badkamer/", "Inspiratie", "Japandi badkamer", "Licht hout en rust.")],
        tabel=dict(waar="Kast en blad", antislip="n.v.t.", water="Randen zijn het zwakke punt", prijs="€250 – €2.500 per meubel"),
    ),
    dict(
        slug="voegen-en-kit", naam="Voegen en kit", kort="Voegen",
        seo="Voegen en kit in de badkamer: kleur, soorten en prijs",
        h1="Voegen en kit: kleur, soorten en waarom het verschil maakt",
        description="Cementvoeg of epoxy, welke voegkleur en waar hoort kit in plaats van voeg? Met voegkleurkiezer, eigenschappen, richtprijzen voor voegen en kitwerk, en de valkuilen.",
        oms="Cementvoeg, epoxyvoeg en sanitairkit, met een voegkleurkiezer.",
        intro="Voegen zijn klein, maar je ziet ze overal. Ze bepalen of een tegelwand rustig of druk oogt, en ze zijn de plek waar vuil, kalk en schimmel het eerst zichtbaar worden. Kit is iets anders: dat is de elastische naad in hoeken en langs het bad, waar materialen bewegen. Hieronder kies je zelf een tegel en een voegkleur en zie je meteen het resultaat.",
        hero=[tegelstaal("7.5x15", "halfsteens", "#f3f1ec", "#1f1f21", 2, gl=True, view="70", label="Witte metrotegels met een zwarte voeg"),
              tegelstaal("30x60", "derde", "#a3a19b", "#9a978f", 2, tex="beton", label="Grijze tegel met een voeg in dezelfde kleur"),
              tegelstaal("15x15", "stapel", "#c07a58", "#cbbda3", 3, view="80", label="Terracotta tegels met een zandkleurige voeg")],
        soorten_titel="Soorten voeg en kit",
        soorten=[
            (tegelstaal("15x15", "stapel", "#f3f1ec", "#c9c7c1", 3, view="80"), "Cementgebonden voeg", "De standaard. Flexibel en betaalbaar, maar licht poreus: de voeg neemt vuil op en is niet waterdicht. Een voegimpregneermiddel helpt."),
            (tegelstaal("15x15", "stapel", "#f3f1ec", "#ecebe6", 3, view="80"), "Epoxyvoeg", "Een voeg op basis van kunsthars. Waterdicht, vlekbestendig en sterk tegen schoonmaakmiddelen. Duurder en lastiger te verwerken."),
            (tegelstaal("60x60", "stapel", "#ddd2bf", "#cbbda3", 2, view="150"), "Voeg in tegelkleur", "Een voeg in dezelfde tint als de tegel laat de voegen bijna verdwijnen. Rustig, vooral bij grote tegels."),
            (tegelstaal("7.5x30", "visgraat", "#f3f1ec", "#4f5153", 2, gl=True, view="110"), "Contrasterende voeg", "Een donkere voeg bij een lichte tegel maakt het patroon zichtbaar. Mooi bij metrotegels en visgraat."),
        ],
        eig=dict(onderhoud=3, slijt=3,
                 onderhoud_t="Cementvoeg: regelmatig schoonmaken en eventueel impregneren. Epoxy: bijna onderhoudsvrij. Kit: vervangen zodra hij loslaat of schimmel heeft.",
                 slijt_t="Epoxy is het sterkst. Cementvoeg slijt en verkleurt in de loop van de jaren. Kit wordt na een aantal jaren hard en laat los.",
                 antislip="Meer voegen geeft meer grip. Daarom werken kleine tegels goed in een douchevloer.",
                 water="Een cementvoeg is niet waterdicht, een epoxyvoeg wel. De echte waterdichting zit in de laag onder de tegels."),
        prijs_eenheid="inclusief btw",
        prijzen=[("Kitwerk (per meter)", *_rp("kitwerk")), ("Hele badkamer opnieuw kitten", *_rp("kitwerk_badkamer")), ("Uitslijpen en opnieuw voegen (per m²)", 43, 66)],
        prijs_tekst="Oude kit verwijderen en opnieuw kitten kost €6 tot €11 per meter, en een hele badkamer opnieuw afkitten €95 tot €325. Bestaande voegen uitslijpen en opnieuw voegen kost gemiddeld €43 tot €66 per m² (indicatief). Bij nieuw tegelwerk zit het voegen in de prijs van de tegelzetter, met ongeveer €10 per m² voor lijm, voegsel en kit. Een epoxyvoeg is duurder in materiaal en kost meer tijd; vraag hem als aparte regel in de offerte.",
        bronnen=["werkspot_kit", "slimster_kit", "ww_voegen", "trustoo_badkamer"],
        geschikt=[("Wand", "ja", "Cementvoeg is prima. Kies een tint die bij de tegel past."),
                  ("Douche", "ja", "Epoxy is hier de sterkste keuze: geen vlekken, geen schimmel in de voeg."),
                  ("Hoeken en aansluitingen", "nee", "Nooit voegen, altijd kit. Hier bewegen de materialen en scheurt een voeg.")],
        kiezer="voeg",
        valkuilen=[
            "Kit over oude kit. Het hecht slecht en de schimmel eronder komt terug. Oude kit moet er helemaal uit.",
            "Voeg in de hoeken. Wand en vloer bewegen een beetje; een harde voeg scheurt. In elke inwendige hoek en langs bad en douchebak hoort kit.",
            "Te vroeg douchen. Kit heeft meestal minimaal 24 uur nodig om uit te harden, een voeg vaak nog langer. Volg het advies op de verpakking.",
            "Een witte voeg op de douchevloer. Die ziet er na een paar maanden grijs uit.",
            "Agressieve reinigers. Chloor en zure middelen tasten cementvoegen en kit aan.",
        ],
        tips=[
            "Kies een voeg die iets donkerder is dan de tegel. Dan valt vuil minder op en blijft het beeld rustig.",
            "Laat de kit dezelfde kleur hebben als de voeg. Dan zie je de overgang niet.",
            "Trek na het douchen de wanden af. Dat scheelt kalk op de tegels én schimmel in de voegen.",
        ],
        faq=[
            ("Welke voegkleur is het makkelijkst in onderhoud?", "Een middentint, zoals lichtgrijs, zand of cementgrijs. Wit laat vuil zien, heel donker kan een witte kalkwaas laten zien."),
            ("Is een epoxyvoeg de moeite waard?", "In de douche vaak wel. Epoxy is waterdicht, neemt geen vuil op en schimmelt niet in de voeg. Het is wel duurder en lastiger te verwerken, dus kies een tegelzetter met ervaring."),
            ("Wanneer gebruik je kit en wanneer voeg?", "Voeg tussen tegels in een vlak. Kit in hoeken en waar verschillende materialen samenkomen, zoals langs het bad, de douchebak of het aanrecht, omdat die een beetje bewegen."),
            ("Hoe vaak moet kit vervangen worden?", "Zodra hij loslaat, scheurt of schimmel heeft die je er niet meer af krijgt. Dat is vaak na een aantal jaren. Wacht niet te lang, want via losse kit komt water achter de tegels."),
        ],
        links=[("/kosten/kitwerk-voegen/", "Kosten", "Kitwerk en voegen", "Wat opnieuw kitten of voegen kost."),
               ("/kennisbank/schimmel-in-badkamer/", "Kennisbank", "Schimmel in de badkamer", "Oorzaak, aanpak en voorkomen."),
               ("/kennisbank/badkamer-schoonmaken/", "Kennisbank", "Badkamer schoonmaken", "Voegen en kit schoon houden."),
               ("/diensten/badkamer-onderhoud/", "Dienst", "Badkamer onderhoud", "Kitwerk en voegen laten vernieuwen."),
               ("/kosten/badkamer-opknappen/", "Kosten", "Badkamer opknappen", "Opfrissen zonder te verbouwen.")],
        tabel=dict(waar="Vloer, wand, douche; kit in hoeken", antislip="Meer voegen = meer grip", water="Cement nee, epoxy ja", prijs="Kit €6 – €11 /m; hervoegen €43 – €66 /m²"),
    ),
]

LINKS = [(PAD, "Badkamermaterialen", "Acht materialen naast elkaar: tegels, natuursteen, microcement, terrazzo, kranen, glas, meubels en voegen.")] + [
    (f"{PAD}{m['slug']}/", m["naam"], m["oms"]) for m in MATERIALEN]


# ---------------------------------------------------------------------------
# CSS
# ---------------------------------------------------------------------------

CSS = """<style>
.mt-c{display:block;width:100%;height:auto;background:#e6e1d8}
.mt-hero{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:20px 0 6px}
.mt-hero .mt-c{border-radius:10px}
.mt-noot{font-size:.8rem;color:var(--muted,#5b6470);margin:6px 0 0}
.mt-stalen{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px;margin:18px 0}
.mt-staal{margin:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden}
.mt-staal figcaption{padding:11px 13px 13px;font-size:.88rem;line-height:1.45}
.mt-staal strong{display:block;font-size:.97rem;color:var(--ink);margin-bottom:3px}
.mt-eig{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:16px 0}
.mt-eig>div{background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px}
.mt-eig h3{font-size:.98rem;margin:0 0 6px;display:flex;justify-content:space-between;gap:10px;align-items:center}
.mt-eig p{font-size:.9rem;margin:0;line-height:1.5}
.mt-meter{display:inline-flex;gap:3px;flex:none}
.mt-meter i{width:14px;height:8px;border-radius:2px;background:var(--line,#e3e0da)}
.mt-meter i.on{background:var(--accent,#c4572a)}
.mt-waar{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0}
.mt-waar>div{border-radius:var(--radius);padding:14px 16px;border:1px solid var(--line);background:#fff}
.mt-waar h3{font-size:1rem;margin:0 0 6px;display:flex;align-items:center;gap:8px}
.mt-waar p{font-size:.88rem;margin:0;line-height:1.45}
.mt-oor{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;font-size:.85rem;font-weight:800;color:#fff;flex:none}
.mt-ja .mt-oor{background:#2f7d55}.mt-let .mt-oor{background:#c08a1e}.mt-nee .mt-oor{background:#b23b2e}
.mt-ja{box-shadow:inset 0 3px 0 #2f7d55}.mt-let{box-shadow:inset 0 3px 0 #c08a1e}.mt-nee{box-shadow:inset 0 3px 0 #b23b2e}
.mt-kz{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:22px;background:var(--bg-soft,#f6f4f0);border:1px solid var(--line);border-radius:var(--radius);padding:18px;margin:18px 0 26px}
.mt-kz .mt-c{border-radius:10px;box-shadow:0 2px 10px rgba(20,30,40,.08)}
.mt-kz-titel{font-weight:700;margin:10px 0 0;font-size:.95rem}
.mt-fs{border:0;padding:0;margin:0 0 14px;min-width:0}
.mt-fs legend{font-weight:700;font-size:.9rem;margin-bottom:7px;padding:0}
.mt-chips{display:flex;flex-wrap:wrap;gap:7px}
.mt-chip{position:relative;cursor:pointer}
.mt-chip input,.mt-kl input{position:absolute;opacity:0;width:1px;height:1px}
.mt-chip span{display:inline-block;padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:#fff;font-size:.86rem;line-height:1.2}
.mt-chip input:checked+span{border-color:var(--ink,#1f2a33);background:var(--ink,#1f2a33);color:#fff}
.mt-chip input:disabled+span{opacity:.4;text-decoration:line-through;cursor:not-allowed}
.mt-chip input:focus-visible+span,.mt-kl input:focus-visible+span{outline:3px solid var(--accent,#c4572a);outline-offset:2px}
.mt-kl{position:relative;cursor:pointer;display:inline-flex;flex-direction:column;align-items:center;width:58px;font-size:.72rem;text-align:center;line-height:1.2}
.mt-kl span{width:34px;height:34px;border-radius:50%;border:1px solid rgba(0,0,0,.18);box-shadow:inset 0 -4px 8px rgba(0,0,0,.08);margin-bottom:4px}
.mt-kl input:checked+span{box-shadow:0 0 0 3px #fff,0 0 0 5px var(--ink,#1f2a33)}
.mt-check{display:flex;gap:8px;align-items:center;font-size:.9rem;cursor:pointer}
.mt-adv{margin:6px 0 0;padding-left:18px;font-size:.88rem;line-height:1.5}
.mt-adv li{margin-bottom:5px}
.mt-afw{margin:12px 0 20px}
.mt-tabel td,.mt-tabel th{font-size:.88rem;vertical-align:top}
.mt-tabel td:first-child{font-weight:700;white-space:nowrap}
.mt-tabel a{color:inherit}
.mt-tabel .mt-meter i{width:10px;height:7px}
.mt-kaarten{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px;margin:22px 0}
.mt-kaart{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit}
.mt-kaart:hover,.mt-kaart:focus-visible{border-color:var(--accent)}
.mt-kaart-t{padding:14px 16px 16px}
.mt-kaart h2{font-size:1.08rem;margin:0 0 5px}
.mt-kaart p{font-size:.92rem;margin:0 0 8px}
.mt-go{font-weight:700;color:var(--accent-dark,#9a3d14);font-size:.9rem}
.mt-verder{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0}
.mt-verder a{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px;text-decoration:none;color:inherit}
.mt-verder a:hover,.mt-verder a:focus-visible{border-color:var(--accent)}
.mt-soort{display:block;font-size:.74rem;text-transform:uppercase;letter-spacing:.04em;color:var(--accent-dark,#9a3d14);font-weight:700}
.mt-naam{display:block;font-weight:700;margin:3px 0}
.mt-oms{display:block;font-size:.88rem;color:var(--muted,#5b6470)}
.mt-twee{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.mt-andere{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,1fr));gap:12px;margin:14px 0}
.mt-andere a{text-decoration:none;color:inherit;font-weight:700;font-size:.88rem}
.mt-andere .mt-c{border-radius:8px;margin-bottom:5px}
.mt-bron{font-size:.86rem}
.mt-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media (prefers-reduced-motion:no-preference){.mt-kaart,.mt-verder a{transition:border-color .15s}.mt-chip span{transition:background .12s,color .12s}}
@media (max-width:760px){.mt-kz{grid-template-columns:1fr;padding:14px}.mt-twee{grid-template-columns:1fr}.mt-waar{grid-template-columns:1fr}}
@media (max-width:520px){.mt-hero{grid-template-columns:1fr 1fr}.mt-hero .mt-c:nth-child(3){display:none}.mt-stalen{grid-template-columns:1fr 1fr;gap:10px}.mt-staal figcaption{font-size:.82rem;padding:9px 10px 11px}}
</style>"""


# ---------------------------------------------------------------------------
# Bouwstenen
# ---------------------------------------------------------------------------

def _meter(n):
    return ('<span class="mt-meter" aria-hidden="true">' + "".join(
        f'<i class="{"on" if i < n else ""}"></i>' for i in range(5)) + "</span>")


def _woord(n):
    return {1: "zeer veel", 2: "veel", 3: "gemiddeld", 4: "weinig", 5: "zeer weinig"}[n]


def _slijt(n):
    return {1: "laag", 2: "matig", 3: "redelijk", 4: "hoog", 5: "zeer hoog"}[n]


def _bronnen(keys):
    out = []
    for k in keys:
        lab, url = BRONNEN[k]
        out.append(f'<li><a href="{_esc(url)}" rel="noopener">{_esc(lab)}</a></li>' if url else f"<li>{_esc(lab)}</li>")
    return "".join(out)


def _kaart(href, soort, naam, oms):
    return (f'<a href="{href}"><span class="mt-soort">{soort}</span><span class="mt-naam">{naam}</span>'
            f'<span class="mt-oms">{oms}</span></a>')


def _radio(groep, waarde, label, checked=False):
    c = " checked" if checked else ""
    return f'<label class="mt-chip"><input type="radio" name="{groep}" value="{waarde}"{c}><span>{label}</span></label>'


def _kleur(groep, naam, hx, checked=False):
    c = " checked" if checked else ""
    return (f'<label class="mt-kl"><input type="radio" name="{groep}" value="{hx}"{c} aria-label="{naam}">'
            f'<span style="background:{hx}"></span>{naam}</label>')


def _tegelkiezer():
    i = "tk"
    fm = "".join(_radio(f"{i}-f", v, l, v == "120x60") for v, l in FORMATEN)
    pt = "".join(_radio(f"{i}-p", v, l, v == "derde") for v, l in PATRONEN)
    tk = "".join(_kleur(f"{i}-k", n, h, n == "Wit") for n, h in TEGELKLEUREN)
    vk = "".join(_kleur(f"{i}-g", n, h, n == "Cementgrijs") for n, h in VOEGKLEUREN)
    return f"""<div class="mt-kz" id="{i}" data-kz="tegel">
  <div>
    {tegelstaal("120x60", "derde", "#f3f1ec", "#9a978f", 2, w=640, h=480, label="Getekend voorbeeld van het gekozen legpatroon")}
    <p class="mt-kz-titel" aria-live="polite">120 × 60 cm in 1/3 verband</p>
    <p class="mt-noot">Getekend voorbeeld, geen foto. Ongeveer op schaal; kleuren zijn een benadering.</p>
  </div>
  <div>
    <fieldset class="mt-fs"><legend>Tegelformaat (cm)</legend><div class="mt-chips">{fm}</div></fieldset>
    <fieldset class="mt-fs"><legend>Legpatroon</legend><div class="mt-chips">{pt}</div></fieldset>
    <fieldset class="mt-fs"><legend>Tegelkleur</legend><div class="mt-chips">{tk}</div></fieldset>
    <fieldset class="mt-fs"><legend>Voegkleur</legend><div class="mt-chips">{vk}</div></fieldset>
    <ul class="mt-adv" aria-live="polite"><li>Kies een formaat, patroon en kleuren. Het voorbeeld verandert direct.</li></ul>
  </div>
</div>"""


def _voegkiezer():
    i = "vk"
    tk = "".join(_kleur(f"{i}-k", n, h, n == "Wit") for n, h in TEGELKLEUREN)
    vk = "".join(_kleur(f"{i}-g", n, h, n == "Cementgrijs") for n, h in VOEGKLEUREN)
    fm = "".join(_radio(f"{i}-f", v, l, n == 0) for n, (v, l) in enumerate(
        [("7.5x15|halfsteens", "Metro 7,5 × 15"), ("15x15|stapel", "15 × 15"), ("30x60|derde", "30 × 60"), ("60x60|stapel", "60 × 60")]))
    br = "".join(_radio(f"{i}-b", v, l, v == "3") for v, l in [("2", "2 mm"), ("3", "3 mm"), ("5", "5 mm")])
    return f"""<div class="mt-kz" id="{i}" data-kz="voeg">
  <div>
    {tegelstaal("7.5x15", "halfsteens", "#f3f1ec", "#9a978f", 3, w=640, h=480, label="Getekend voorbeeld van de gekozen voegkleur")}
    <p class="mt-kz-titel">Jouw tegel met de gekozen voeg</p>
    <p class="mt-noot">Getekend voorbeeld, geen foto. Kleuren op een scherm zijn een benadering; vraag altijd een voegstaal.</p>
  </div>
  <div>
    <fieldset class="mt-fs"><legend>Tegel</legend><div class="mt-chips">{fm}</div></fieldset>
    <fieldset class="mt-fs"><legend>Tegelkleur</legend><div class="mt-chips">{tk}</div></fieldset>
    <fieldset class="mt-fs"><legend>Voegkleur</legend><div class="mt-chips">{vk}</div></fieldset>
    <fieldset class="mt-fs"><legend>Voegbreedte</legend><div class="mt-chips">{br}</div></fieldset>
    <label class="mt-check"><input type="checkbox" name="{i}-o"> Laat zien hoe een cementvoeg na een paar jaar kan ogen</label>
    <ul class="mt-adv" aria-live="polite"><li>Kies een tegel en een voegkleur. Het voorbeeld verandert direct.</li></ul>
  </div>
</div>"""


def _eigenschappen(m):
    e = m["eig"]
    return f"""<div class="mt-eig">
  <div><h3>Onderhoud {_meter(e['onderhoud'])}</h3><p><strong>{_woord(e['onderhoud']).capitalize()} onderhoud.</strong> {e['onderhoud_t']}</p></div>
  <div><h3>Slijtvastheid {_meter(e['slijt'])}</h3><p><strong>{_slijt(e['slijt']).capitalize()}.</strong> {e['slijt_t']}</p></div>
  <div><h3>Antislip</h3><p>{e['antislip']}</p></div>
  <div><h3>Waterdichtheid</h3><p>{e['water']}</p></div>
</div>
<p class="mt-noot">Meters: vijf blokjes betekent weinig onderhoud of zeer slijtvast. Het is onze inschatting ten opzichte van de andere materialen op deze site.</p>"""


def _geschikt(m):
    teken = {"ja": "✓", "let": "!", "nee": "✕"}
    woord = {"ja": "geschikt", "let": "let op", "nee": "niet doen"}
    return '<div class="mt-waar">' + "".join(
        f'<div class="mt-{o}"><h3><span class="mt-oor" aria-hidden="true">{teken[o]}</span>{p}'
        f'<span class="mt-sr"> ({woord[o]})</span></h3><p>{t}</p></div>' for p, o, t in m["geschikt"]) + "</div>"


def _art_ld(m, url, today):
    return {
        "@context": "https://schema.org", "@type": "Article",
        "headline": m["h1"], "description": m["description"], "inLanguage": "nl-NL",
        "datePublished": GEPUBLICEERD, "dateModified": today,
        "author": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "publisher": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "mainEntityOfPage": SITE["url"] + url,
        "isPartOf": {"@type": "CollectionPage", "@id": SITE["url"] + PAD},
        "citation": [BRONNEN[k][1] for k in m["bronnen"] if BRONNEN[k][1]],
    }


# ---------------------------------------------------------------------------
# Materiaalpagina
# ---------------------------------------------------------------------------

def _materiaalpagina(m, write, today):
    url = f"{PAD}{m['slug']}/"
    cr, cr_ld = crumbs([("Home", "/"), ("Materialen", PAD), (m["naam"], None)])
    stalen = "".join(_fig(c, n, t) for c, n, t in m["soorten"])
    kiezer = ""
    if m.get("kiezer") == "tegel":
        kiezer = ('<h2 id="kiezer">Probeer het zelf: formaat, legpatroon en voeg</h2>'
                  '<p>Kies een tegelformaat, een legpatroon, een tegelkleur en een voegkleur. Je ziet direct hoe het eruitziet, met advies over voegbreedte, snijverlies en wat een tegelzetter je zou afraden.</p>'
                  + _tegelkiezer())
    elif m.get("kiezer") == "voeg":
        kiezer = ('<h2 id="kiezer">Kies je voegkleur</h2>'
                  '<p>Dezelfde tegel kan er met een andere voeg heel anders uitzien. Probeer het hieronder, en kijk ook hoe een lichte voeg na een paar jaar kan ogen.</p>'
                  + _voegkiezer())
    afw = ""
    if m.get("afwerkingen"):
        rijen = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in m["afwerkingen"])
        afw = (f'<h3>De afwerkingen naast elkaar</h3><div class="tablewrap mt-afw"><table class="mt-tabel"><thead><tr>'
               f'<th>Afwerking</th><th>Krasvast</th><th>Kalk en vingers</th><th>Prijs</th></tr></thead><tbody>{rijen}</tbody></table></div>')
    balken = prijs_balken(m["prijzen"], m["prijs_eenheid"], "Richtprijzen, inclusief 21% btw tenzij anders vermeld. Bronnen staan hieronder.")
    valk = "".join(f"<li>{v}</li>" for v in m["valkuilen"])
    tips = "".join(f"<li>{t}</li>" for t in m["tips"])
    verder = "".join(_kaart(*l) for l in m["links"])
    andere = "".join(
        f'<a href="{PAD}{o["slug"]}/">{_mini(o)}{o["naam"]}</a>' for o in MATERIALEN if o["slug"] != m["slug"])
    faq_html, faq_ld = faq_blok(m["faq"], f"Veelgestelde vragen over {m['naam'].lower()}")
    klus = {"keramische-tegels": "tegelwerk", "natuursteen": "natuursteen", "microcement": "microcement",
            "terrazzo": "een terrazzovloer", "kraanafwerkingen": "nieuwe kranen", "douchewand-glas": "een douchewand",
            "meubelmaterialen": "een badkamermeubel", "voegen-en-kit": "kitwerk of voegen"}[m["slug"]]

    body = f"""{CSS}{cr}
<article class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Materialen</span>
  <h1>{m['h1']}</h1>
  <p class="lead">{m['intro']}</p>
  <div class="mt-hero">{"".join(m['hero'])}</div>
  <p class="mt-noot">Getekende stalen, geen foto's. Kleur en structuur zijn een benadering; bekijk materialen altijd in het echt.</p>

  <h2 id="soorten">{m['soorten_titel']}</h2>
  <div class="mt-stalen">{stalen}</div>
  {kiezer}

  <h2 id="eigenschappen">Eigenschappen: een eerlijke vergelijking</h2>
  {_eigenschappen(m)}
  {afw}

  <h2 id="geschikt">Waar is het geschikt voor?</h2>
  {_geschikt(m)}

  {cta_midden(f"Advies over {m['naam'].lower()} in jouw badkamer?", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Zij kijken ook naar je ondergrond en wat daar past.")}

  <h2 id="prijs">Wat kost het?</h2>
  {balken}
  <p>{m['prijs_tekst']}</p>
  <p class="mt-bron"><strong>Bronnen</strong> (geraadpleegd november 2026):</p>
  <ul class="mt-bron">{_bronnen(m['bronnen'])}</ul>
  {offertecheck_blok(klus)}

  <div class="mt-twee">
    <div><h2 id="valkuilen">Valkuilen</h2><ul>{valk}</ul></div>
    <div><h2 id="tips">Tips</h2><ul class="checklist">{tips}</ul></div>
  </div>

  <h2 id="verder">Verder lezen</h2>
  <div class="mt-verder">{verder}</div>

  <h2 id="andere">Andere materialen</h2>
  <div class="mt-andere">{andere}</div>
  <p><a href="{PAD}">Alle materialen in één vergelijkingstabel</a></p>
</div></article>
{faq_html}
{cta_blok("Klaar om te kiezen?", "Beschrijf je wensen in een minuut en ontvang gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio.")}
{JS}"""
    write(url, page(title(m["seo"]), m["description"], url, body, [cr_ld, _art_ld(m, url, today), faq_ld]), prio=0.7)


MINI = {"keramische-tegels": lambda: tegelstaal("30x60", "halfsteens", "#ddd2bf", "#c9c7c1", 2, w=300, h=200, view="160"),
        "natuursteen": lambda: staal("marmer", "carrara", 300, 200),
        "microcement": lambda: staal("micro", "greige", 300, 200),
        "terrazzo": lambda: staal("terrazzo", "middel", 300, 200),
        "kraanafwerkingen": lambda: staal("metaal", "gunmetal", 300, 200),
        "douchewand-glas": lambda: staal("glas", "ribbel", 300, 200),
        "meubelmaterialen": lambda: staal("hout", "eiken", 300, 200),
        "voegen-en-kit": lambda: tegelstaal("7.5x15", "halfsteens", "#f3f1ec", "#4f5153", 2, w=300, h=200, gl=True, view="60")}


def _mini(m):
    return MINI[m["slug"]]()


# ---------------------------------------------------------------------------
# Overzicht
# ---------------------------------------------------------------------------

def _overzicht(write, today):
    cr, cr_ld = crumbs([("Home", "/"), ("Materialen", None)])
    kaarten = "".join(
        f'<a class="mt-kaart" href="{PAD}{m["slug"]}/">{_mini(m)}'
        f'<div class="mt-kaart-t"><h2>{m["naam"]}</h2><p>{m["oms"]}</p><span class="mt-go">Bekijk de stalen →</span></div></a>'
        for m in MATERIALEN)
    rijen = "".join(
        f'<tr><td><a href="{PAD}{m["slug"]}/">{m["naam"]}</a></td><td>{m["tabel"]["waar"]}</td>'
        f'<td>{_meter(m["eig"]["onderhoud"])}<br>{_woord(m["eig"]["onderhoud"])}</td>'
        f'<td>{_meter(m["eig"]["slijt"])}<br>{_slijt(m["eig"]["slijt"])}</td>'
        f'<td>{m["tabel"]["antislip"]}</td><td>{m["tabel"]["water"]}</td><td>{m["tabel"]["prijs"]}</td></tr>'
        for m in MATERIALEN)
    alle_bronnen = []
    for m in MATERIALEN:
        for k in m["bronnen"]:
            if k not in alle_bronnen:
                alle_bronnen.append(k)
    faqs = [
        ("Zijn de stalen op deze pagina's foto's?", "Nee. Het zijn stalen die je browser tekent op basis van kleur en structuur. Ze geven een indruk, maar echte materialen verschillen per partij en per licht. Bekijk ze altijd in het echt."),
        ("Welk materiaal vraagt het minste onderhoud?", "Porseleinen tegels met een voeg in een middentint, of met een epoxyvoeg in de douche. Natuursteen en echte terrazzo vragen het meeste onderhoud, omdat ze poreus zijn en niet tegen zuur kunnen."),
        ("Welk materiaal is het beste voor een douchevloer?", "Kleine porseleinen tegels of grote tegels met een douchegoot, met een antislipwaarde van R11 of klasse B tot C. Natuursteen en microcement kunnen ook, maar vragen meer zorg en een vakman met ervaring."),
        ("Waarom zijn de prijzen zo breed?", "Omdat de prijs sterk afhangt van de kwaliteit, het formaat, de ondergrond en de regio. Wij geven richtprijzen met bronnen. Een offerte van een specialist die je badkamer heeft gezien, is altijd preciezer."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over badkamermaterialen")
    body = f"""{CSS}{cr}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose">
    <span class="badge">Materialen</span>
    <h1>Badkamermaterialen vergelijken: stalen, eigenschappen en prijzen</h1>
    <p class="lead">Tegels of microcement? Marmer of terrazzo? Mat zwart of geborsteld goud? Per materiaal zie je getekende stalen en lees je eerlijk hoe het zit met onderhoud, slijtvastheid, antislip, waterdichtheid en prijs. Met valkuilen die je pas ziet als het te laat is.</p>
    <p>De stalen tekent je browser zelf; het zijn geen foto's. Wij voeren zelf geen werk uit, maar brengen je in contact met maximaal drie badkamerspecialisten uit je regio.</p>
  </div>
  <div class="mt-kaarten">{kaarten}</div>
  <div class="narrow prose">
    <h2 id="vergelijk">Alle materialen in één tabel</h2>
    <p>Onderhoud en slijtvastheid zijn onze inschatting ten opzichte van elkaar: vijf blokjes is weinig onderhoud of zeer slijtvast. De prijzen zijn richtprijzen inclusief btw; op elke materiaalpagina staat de uitleg met bronnen.</p>
  </div>
  <div class="tablewrap" style="max-width:1100px;margin:16px auto 0"><table class="mt-tabel">
    <thead><tr><th>Materiaal</th><th>Waar</th><th>Onderhoud</th><th>Slijtvast</th><th>Antislip</th><th>Water</th><th>Richtprijs</th></tr></thead>
    <tbody>{rijen}</tbody></table></div>
  <div class="narrow prose" style="margin-top:34px">
    <h2>Zo kies je het juiste materiaal</h2>
    <ul class="checklist">
      <li><strong>Begin bij de douche.</strong> Daar wordt alles het zwaarst belast. Kies daar een materiaal dat tegen water, zeep en kalk kan, en volg met de rest van de badkamer.</li>
      <li><strong>Denk aan je water.</strong> Bij hard water vallen kalkvlekken op donker glas, mat zwarte kranen en donkere voegen het meest op. Lees meer over <a href="/kennisbank/kalk-en-waterhardheid/">kalk en waterhardheid</a>.</li>
      <li><strong>Wees eerlijk over onderhoud.</strong> Natuursteen en microcement zijn prachtig, maar vragen aandacht. Wil je zo min mogelijk werk, kies dan porselein met een goede voeg.</li>
      <li><strong>Laat de ondergrond meewegen.</strong> Grote tegels en microcement vragen een vlakke, stevige ondergrond. Dat kan extra werk geven; vraag het na in de offerte.</li>
      <li><strong>Houd het bij één blikvanger.</strong> Een terrazzovloer, een marmeren wand of gouden kranen: kies er één, en houd de rest rustig.</li>
    </ul>
    <p>Wil je zien hoe materialen samen uitpakken? Probeer de <a href="/tools/stijlkiezer/">stijlkiezer</a> of zet je indeling neer in de <a href="/tools/indelingsplanner/">indelingsplanner</a>. Voor inspiratie zie je stijlen in beeld bij <a href="/inspiratie/">badkamer inspiratie</a> en <a href="/inspiratie/voor-en-na/">voor en na</a>. Wat een nieuwe badkamer in totaal kost, lees je op <a href="/kosten/nieuwe-badkamer/">de kostenpagina</a>, en hoe een verbouwing verloopt op <a href="/zo-verloopt-je-verbouwing/">zo verloopt je verbouwing</a>.</p>
    {offertecheck_blok()}
    <p class="mt-bron"><strong>Bronnen voor de richtprijzen</strong> (geraadpleegd november 2026):</p>
    <ul class="mt-bron">{_bronnen(alle_bronnen)}</ul>
  </div>
</div></section>
{faq_html}
{cta_blok("Weet je wat je wilt?", "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit jouw regio en vergelijk ze naast elkaar.")}
{JS}"""
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE["url"] + f"{PAD}{m['slug']}/", "name": m["naam"]}
             for i, m in enumerate(MATERIALEN)]
    lijst_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE["url"] + PAD,
                "name": "Badkamermaterialen vergelijken", "inLanguage": "nl-NL", "dateModified": today,
                "mainEntity": {"@type": "ItemList", "itemListElement": items}}
    write(PAD, page(title("Badkamermaterialen vergelijken"),
                    "Vergelijk badkamermaterialen: tegels, natuursteen, microcement, terrazzo, kranen, glas, meubels en voegen. Met getekende stalen, eigenschappen en richtprijzen.",
                    PAD, body, [cr_ld, lijst_ld, faq_ld]), prio=0.8)


def build(write):
    today = datetime.date.today().isoformat()
    for m in MATERIALEN:
        _materiaalpagina(m, write, today)
    _overzicht(write, today)


# ---------------------------------------------------------------------------
# JavaScript: procedurele stalen in canvas en de twee kiezers
# ---------------------------------------------------------------------------
# Tekent pas als een staal in beeld komt (IntersectionObserver). Geen animatie, dus niets dat
# prefers-reduced-motion hoeft uit te zetten; hover-overgangen staan in de CSS achter no-preference.

JS = r"""<script>
(function(){
"use strict";
var DPR=Math.min(window.devicePixelRatio||1,2);
function rng(seed){var s=(seed>>>0)||7;return function(){s^=s<<13;s>>>=0;s^=s>>>17;s^=s<<5;s>>>=0;return s/4294967296;};}
function hsh(t){var h=2166136261;for(var i=0;i<t.length;i++){h^=t.charCodeAt(i);h=Math.imul(h,16777619);}return h>>>0;}
function hex(c){c=String(c).replace('#','');if(c.length===3)c=c.replace(/./g,'$&$&');var n=parseInt(c,16);return[n>>16&255,n>>8&255,n&255];}
function rgba(c,a){var r=hex(c);return'rgba('+r[0]+','+r[1]+','+r[2]+','+a+')';}
function mix(a,b,t){var x=hex(a),y=hex(b),o='#';for(var i=0;i<3;i++){o+=('0'+Math.round(x[i]+(y[i]-x[i])*t).toString(16)).slice(-2);}return o;}
function shade(c,t){return t>0?mix(c,'#ffffff',t):mix(c,'#000000',-t);}
function lum(c){var r=hex(c);return(0.2126*r[0]+0.7152*r[1]+0.0722*r[2])/255;}
function rr(x,a,b,c,d,r){r=Math.min(r,c/2,d/2);x.beginPath();x.moveTo(a+r,b);x.lineTo(a+c-r,b);x.quadraticCurveTo(a+c,b,a+c,b+r);x.lineTo(a+c,b+d-r);x.quadraticCurveTo(a+c,b+d,a+c-r,b+d);x.lineTo(a+r,b+d);x.quadraticCurveTo(a,b+d,a,b+d-r);x.lineTo(a,b+r);x.quadraticCurveTo(a,b,a+r,b);x.closePath();}
function ruis(x,w,h,R,st){var d=x.getImageData(0,0,w,h),p=d.data;for(var i=0;i<p.length;i+=4){var n=(R()-.5)*st;p[i]+=n;p[i+1]+=n;p[i+2]+=n;}x.putImageData(d,0,0);}
function wolken(x,w,h,R,kl,n,a){for(var i=0;i<n;i++){var cx=R()*w,cy=R()*h,r=(.15+R()*.45)*Math.max(w,h);var g=x.createRadialGradient(cx,cy,0,cx,cy,r);var c=kl[i%kl.length];g.addColorStop(0,rgba(c,a*(.5+R())));g.addColorStop(1,rgba(c,0));x.fillStyle=g;x.fillRect(0,0,w,h);}}

/* ---------------- varianten ---------------- */
var V={
 marmer:{carrara:{b:'#efede9',a:['#8e9095','#b4b4b6'],n:7,d:1,w:['#dcdad6','#f8f7f4']},
  calacatta:{b:'#f5f1e9',a:['#9c8259','#77736e'],n:4,d:1.8,w:['#ece4d4','#fbf9f4']},
  nero:{b:'#1d1d20',a:['#ece8e0','#b9b4aa'],n:5,d:1.1,w:['#2a2a2e','#141416']},
  verde:{b:'#25443a',a:['#d9e3dc','#8fb3a0'],n:9,d:.8,w:['#1a3229','#35594b']},
  blad:{b:'#f3f2ef',a:['#8c8c90','#b1b0ad'],n:4,d:1.1,w:['#e6e5e1','#fbfbf9']}},
 hardsteen:{gezoet:{b:'#4e5558',sp:.8,f:9},gebouchardeerd:{b:'#7d8486',sp:2.2,f:3},verouderd:{b:'#5d6467',sp:1.4,f:6}},
 travertin:{gevuld:{b:'#dcc9a8',g:1},ongevuld:{b:'#d6c1a0',g:0},zilver:{b:'#bdb8ad',g:1}},
 terrazzo:{fijn:{b:'#ece7de',k:3,c:['#b9b2a6','#8b8479','#d8cfc0','#6d6a66'],dn:.55},
  middel:{b:'#e9e4dc',k:7,c:['#a9a197','#c96f4a','#5f6f66','#d9cfbf','#3e3d3b'],dn:.42},
  grof:{b:'#efebe4',k:15,c:['#b7aea2','#7c8a80','#d7a184','#2f2f31','#e3dccf'],dn:.36},
  kleur:{b:'#f3ece6',k:9,c:['#e07a5f','#3d5a80','#f2cc8f','#81b29a','#2b2d42'],dn:.4},
  donker:{b:'#3a3b3d',k:7,c:['#e8e3da','#a59c90','#c9a27a','#6e7470'],dn:.45}},
 micro:{kalkwit:{b:'#ece8e1'},greige:{b:'#c9beb0'},betongrijs:{b:'#9d9b96'},antraciet:{b:'#4b4d4f'},terra:{b:'#b9876b'},salie:{b:'#a3ac98'}},
 metaal:{chroom:{s:['#5b6066','#f6f8fa','#8e959c','#ffffff','#666b71','#d4d9de','#7d838a'],br:0},
  zwart:{s:['#111','#2b2b2b','#1a1a1a','#363636','#141414','#262626','#101010'],br:0,mat:1},
  rvs:{s:['#7f8488','#d2d5d8','#9ea3a7','#e2e4e6','#878b8f','#c3c6c9','#80858a'],br:1},
  goud:{s:['#8f6a2e','#e8c983','#b28a42','#f4dda5','#9b7535','#d8b56e','#8d6a30'],br:1},
  gunmetal:{s:['#2f3235','#727679','#43474b','#868a8e','#383b3e','#62666a','#2d3033'],br:1}},
 glas:{helder:{},extra:{},rook:{},brons:{},ribbel:{},mat:{}},
 hout:{eiken:{b:'#c99c66',l:'#a97c4a',t:'nerf'},noten:{b:'#6e4b33',l:'#4f3322',t:'nerf'},massief:{b:'#b88553',l:'#8f6236',t:'nerf',vl:1},
  lakwit:{b:'#f1efea',t:'lak'},lakgroen:{b:'#7d8b78',t:'lak'},hpl:{b:'#8f8e8a',t:'hpl'},keramisch:{b:'#f3f2ef',t:'keramisch'}}
};

/* ---------------- tekenaars ---------------- */
function ader(x,R,px,py,ang,len,s,col,dik,diep){
 var pts=[[px,py]],dr=0;for(var i=0;i<len;i++){dr+=(R()-.5)*.06;dr*=.92;ang+=dr+(R()-.5)*.12;px+=Math.cos(ang)*6*s;py+=Math.sin(ang)*6*s;pts.push([px,py]);
  if(diep<2&&R()<.012){ader(x,R,px,py,ang+(R()-.5)*1.6,Math.floor(len*.35),s,col,dik*.55,diep+1);}}
 var lagen=[[16,.05],[5,.13],[1.6,.55]];
 for(var l=0;l<3;l++){x.beginPath();x.moveTo(pts[0][0],pts[0][1]);for(var j=1;j<pts.length;j++){x.lineTo(pts[j][0],pts[j][1]);}
  x.strokeStyle=rgba(col,lagen[l][1]);x.lineWidth=lagen[l][0]*s*dik;x.lineJoin='round';x.lineCap='round';x.stroke();}
}
function marmer(x,w,h,R,o){
 var s=w/600;x.fillStyle=o.b;x.fillRect(0,0,w,h);wolken(x,w,h,R,o.w,16,.35);
 for(var i=0;i<o.n;i++){var lr=R()<.5;ader(x,R,lr?-20:R()*w,lr?R()*h:-20,Math.PI*(.12+R()*.3),Math.ceil((w+h)/(6*s)),s,o.a[i%o.a.length],o.d*(.5+R()*.9),0);}
 ruis(x,w,h,R,8);
}
function hardsteen(x,w,h,R,o){
 var s=w/600;x.fillStyle=o.b;x.fillRect(0,0,w,h);wolken(x,w,h,R,[shade(o.b,.08),shade(o.b,-.1)],12,.35);
 var n=Math.floor(w*h/(70*s*s));for(var i=0;i<n;i++){var l=R()<.55;x.fillStyle=rgba(l?'#ffffff':'#000000',(.04+R()*.1)*o.sp);var z=(.6+R()*1.6)*s;x.fillRect(R()*w,R()*h,z,z);}
 for(var f=0;f<o.f;f++){var cx=R()*w,cy=R()*h,r=(3+R()*7)*s;x.strokeStyle='rgba(235,238,240,'+(.18+R()*.2)+')';x.lineWidth=1.2*s;x.beginPath();x.ellipse(cx,cy,r,r*(.5+R()*.5),R()*3,0,Math.PI*2);x.stroke();x.fillStyle='rgba(235,238,240,.25)';x.beginPath();x.arc(cx,cy,r*.25,0,7);x.fill();}
 ruis(x,w,h,R,o.sp*12);
}
function travertin(x,w,h,R,o){
 var s=w/600;x.fillStyle=o.b;x.fillRect(0,0,w,h);
 for(var y=0;y<h;){var bh=(3+R()*18)*s;x.fillStyle=rgba(shade(o.b,(R()-.5)*.16),.55);x.fillRect(0,y,w,bh);y+=bh;}
 var n=Math.floor(w*h/(1100*s*s));for(var i=0;i<n;i++){var cx=R()*w,cy=R()*h,rx=(3+R()*16)*s,ry=(1+R()*3)*s;
  x.fillStyle=o.g?rgba(shade(o.b,-.16),.75):rgba(shade(o.b,-.45),.8);x.beginPath();x.ellipse(cx,cy,rx,ry,(R()-.5)*.12,0,7);x.fill();
  if(!o.g){x.strokeStyle=rgba(shade(o.b,.25),.5);x.lineWidth=.8*s;x.beginPath();x.ellipse(cx,cy+ry*.4,rx,ry,0,.2,Math.PI-.2);x.stroke();}}
 ruis(x,w,h,R,14);
}
function terrazzo(x,w,h,R,o){
 var s=w/600;x.fillStyle=o.b;x.fillRect(0,0,w,h);wolken(x,w,h,R,[shade(o.b,-.05),shade(o.b,.05)],8,.3);
 var k=o.k*s,n=Math.floor(o.dn*w*h/(k*k*2.2));
 for(var i=0;i<n;i++){var cx=R()*w,cy=R()*h,r=k*(.35+R()*.95),v=5+Math.floor(R()*3),a0=R()*6.3;x.beginPath();
  for(var j=0;j<v;j++){var a=a0+j/v*6.283+(R()-.5)*.6,rr2=r*(.55+R()*.6);var px=cx+Math.cos(a)*rr2,py=cy+Math.sin(a)*rr2*(.7+R()*.4);j?x.lineTo(px,py):x.moveTo(px,py);}
  x.closePath();var c=o.c[Math.floor(R()*o.c.length)];x.fillStyle=shade(c,(R()-.5)*.14);x.fill();}
 var m=Math.floor(w*h/(40*s*s));for(var q=0;q<m;q++){x.fillStyle=rgba(o.c[q%o.c.length],.5);var z=(.6+R()*1.4)*s;x.fillRect(R()*w,R()*h,z,z);}
 ruis(x,w,h,R,9);
}
function micro(x,w,h,R,o){
 var s=w/600;x.fillStyle=o.b;x.fillRect(0,0,w,h);wolken(x,w,h,R,[shade(o.b,.09),shade(o.b,-.09),shade(o.b,.04)],46,.22);
 for(var i=0;i<30;i++){x.beginPath();x.ellipse(R()*w,R()*h,(60+R()*160)*s,(20+R()*70)*s,R()*3,R()*3,R()*3+1.5+R()*2);
  x.strokeStyle=rgba(R()<.5?shade(o.b,.14):shade(o.b,-.12),.05+R()*.06);x.lineWidth=(12+R()*40)*s;x.lineCap='round';x.stroke();}
 ruis(x,w,h,R,10);
}
function tegel(x,w,h,R,o){
 var f=(o.f||'60x60').split('x').map(Number),tb=f[0],th=f[1],L=Math.max(tb,th),W=Math.min(tb,th);
 var view=o.view?+o.view:Math.max(90,Math.min(420,L*3.4));var sc=w/view;var gp=Math.max(1,(+o.vb||3)/10*sc);
 var k=o.k||'#e9e6e0',g=o.g||'#bdb8ae',gl=o.gl==='1';
 x.fillStyle=g;x.fillRect(0,0,w,h);
 function tg(a,b,c,d){a+=gp/2;b+=gp/2;c-=gp;d-=gp;if(c<=0||d<=0)return;x.fillStyle=shade(k,(R()-.5)*.07);x.fillRect(a,b,c,d);
  var gr=x.createLinearGradient(a,b,a+c,b+d);gr.addColorStop(0,'rgba(255,255,255,'+(gl?.26:.07)+')');gr.addColorStop(.6,'rgba(255,255,255,0)');gr.addColorStop(1,'rgba(0,0,0,'+(gl?.07:.05)+')');x.fillStyle=gr;x.fillRect(a,b,c,d);
  if(o.tex==='beton'){for(var i=0;i<c*d/900;i++){x.fillStyle=rgba(R()<.5?'#ffffff':'#000000',.06+R()*.06);x.fillRect(a+R()*c,b+R()*d,1.5,1.5);}}}
 var p=o.p||'stapel';if(p==='visgraat'&&L===W)p='stapel';
 if(p==='visgraat'){var Lp=L*sc,Wp=W*sc,dg=Math.hypot(w,h);x.save();x.translate(w/2,h/2);x.rotate(-Math.PI/4);
  var nk=Math.ceil(dg/Wp)+2,nj=Math.ceil(dg/Lp)+2;
  for(var j=-nj;j<=nj;j++){for(var q=-nk;q<=nk;q++){var px=q*Wp+j*Lp,py=q*Wp-j*Lp;if(Math.abs(px)>dg||Math.abs(py)>dg)continue;tg(px,py,Lp,Wp);tg(px,py+Wp,Wp,Lp);}}
  x.restore();return;}
 var tw=tb*sc,tH=th*sc,ofs=p==='halfsteens'?.5:p==='derde'?1/3:0;
 for(var r=0,y=-tH*.3;y<h;r++,y+=tH){var o2=((r*ofs)%1)*tw;for(var xx=-tw+o2;xx<w;xx+=tw){tg(xx,y,tw,tH);}}
}
function metaal(x,w,h,R,o){
 var s=w/600;var bg=x.createLinearGradient(0,0,0,h);bg.addColorStop(0,'#f1efeb');bg.addColorStop(1,'#dedad3');x.fillStyle=bg;x.fillRect(0,0,w,h);
 x.strokeStyle='rgba(0,0,0,.05)';x.lineWidth=1;for(var gx=w*.1;gx<w;gx+=w*.3){x.beginPath();x.moveTo(gx,0);x.lineTo(gx,h);x.stroke();}
 x.beginPath();x.moveTo(0,h*.55);x.lineTo(w,h*.55);x.stroke();
 function vul(a,b,c,d,hor,rad){var g=hor?x.createLinearGradient(a,0,a+c,0):x.createLinearGradient(0,b,0,b+d);
  for(var i=0;i<o.s.length;i++)g.addColorStop(i/(o.s.length-1),o.s[i]);x.save();rr(x,a,b,c,d,rad);x.fillStyle=g;x.fill();x.clip();
  if(o.br){for(var k=0;k<(hor?d:c)/(1.2*s);k++){x.strokeStyle=rgba(R()<.5?'#ffffff':'#000000',.04+R()*.08);x.lineWidth=.7*s;x.beginPath();
   if(hor){var yy=b+R()*d;x.moveTo(a,yy);x.lineTo(a+c,yy);}else{var xx=a+R()*c;x.moveTo(xx,b);x.lineTo(xx,b+d);}x.stroke();}}
  if(o.mat){x.fillStyle='rgba(255,255,255,.04)';x.fillRect(a,b,c,d);}x.restore();}
 var cx=w*.6,bw=w*.13,top=h*.34,base=h*.86,sw=bw*.56;
 x.fillStyle='rgba(0,0,0,.13)';x.beginPath();x.ellipse(cx+8*s,base+6*s,bw*1.25,9*s,0,0,7);x.fill();
 vul(cx-bw*.9,base-9*s,bw*1.8,13*s,true,6*s);
 vul(cx-bw/2,top,bw,base-top,true,bw*.28);
 vul(cx-w*.38,top+5*s,w*.38,sw,false,sw/2);
 vul(cx-w*.38,top+5*s,sw*1.05,sw*1.7,true,sw*.3);
 x.save();x.translate(cx,top+3*s);x.rotate(-.42);vul(-5*s,-bw*1.15,bw*.24,bw*1.2,true,6*s);x.restore();
}
function glasAchter(x,w,h,R){
 x.fillStyle='#e9e3d8';x.fillRect(0,0,w,h);var tw=w/5,tH=tw*2;x.strokeStyle='rgba(120,110,95,.35)';x.lineWidth=Math.max(1,w/400);
 for(var r=0,y=0;y<h;r++,y+=tH/2){x.beginPath();x.moveTo(0,y);x.lineTo(w,y);x.stroke();for(var xx=(r%2)*tw/2;xx<w;xx+=tw){x.beginPath();x.moveTo(xx,y);x.lineTo(xx,y+tH/2);x.stroke();}}
 x.fillStyle='#c46f4c';x.fillRect(w*.58,h*.12,w*.14,h*.9);x.fillStyle='#d98d6c';x.fillRect(w*.58,h*.12,w*.14,h*.06);
 x.fillStyle='#5f7f66';x.beginPath();x.ellipse(w*.3,h*.62,w*.09,h*.2,0,0,7);x.fill();x.fillStyle='#466352';x.beginPath();x.ellipse(w*.34,h*.7,w*.06,h*.15,.4,0,7);x.fill();
 x.fillStyle='#8a8d91';x.fillRect(w*.83,h*.08,w*.025,h*.4);x.beginPath();x.arc(w*.8425,h*.08,w*.05,0,Math.PI);x.fill();
}
function glas(x,w,h,R,o,v){
 var s=w/600;glasAchter(x,w,h,R);var gx=w*.16,gw=w*.8;
 if(v==='ribbel'||v==='mat'){var off=document.createElement('canvas');off.width=w;off.height=h;glasAchter(off.getContext('2d'),w,h,R);
  if(v==='ribbel'){var rb=11*s;for(var a=gx;a<gx+gw;a+=rb){var mid=a+rb/2;x.drawImage(off,Math.max(0,mid-rb*1.4),0,rb*2.8,h,a,0,rb,h);
   var g=x.createLinearGradient(a,0,a+rb,0);g.addColorStop(0,'rgba(0,0,0,.14)');g.addColorStop(.45,'rgba(255,255,255,.22)');g.addColorStop(1,'rgba(0,0,0,.1)');x.fillStyle=g;x.fillRect(a,0,rb,h);}
   x.fillStyle='rgba(225,238,234,.12)';x.fillRect(gx,0,gw,h);}
  else{var sm=document.createElement('canvas');sm.width=Math.max(4,Math.round(w/16));sm.height=Math.max(4,Math.round(h/16));sm.getContext('2d').drawImage(off,0,0,sm.width,sm.height);
   x.save();x.beginPath();x.rect(gx,0,gw,h);x.clip();x.imageSmoothingEnabled=true;x.drawImage(sm,0,0,w,h);x.restore();x.fillStyle='rgba(248,249,248,.55)';x.fillRect(gx,0,gw,h);}}
 else{var t={helder:'rgba(185,222,208,.13)',extra:'rgba(225,240,236,.06)',rook:'rgba(38,42,46,.52)',brons:'rgba(112,80,48,.45)'}[v];x.fillStyle=t;x.fillRect(gx,0,gw,h);}
 var rf=x.createLinearGradient(gx,0,gx+gw,h);rf.addColorStop(0,'rgba(255,255,255,0)');rf.addColorStop(.38,'rgba(255,255,255,0)');rf.addColorStop(.46,'rgba(255,255,255,.32)');rf.addColorStop(.52,'rgba(255,255,255,0)');rf.addColorStop(.6,'rgba(255,255,255,.14)');rf.addColorStop(.64,'rgba(255,255,255,0)');
 x.fillStyle=rf;x.fillRect(gx,0,gw,h);
 x.fillStyle=v==='extra'?'rgba(215,235,230,.7)':'rgba(120,170,150,.65)';x.fillRect(gx,0,3*s,h);x.fillRect(gx+gw-3*s,0,3*s,h);
 var pg=x.createLinearGradient(gx-7*s,0,gx,0);pg.addColorStop(0,'#6b7075');pg.addColorStop(.5,'#e6e8ea');pg.addColorStop(1,'#80868b');x.fillStyle=pg;x.fillRect(gx-7*s,0,7*s,h);
}
function hout(x,w,h,R,o){
 var s=w/600;x.fillStyle=o.b;x.fillRect(0,0,w,h);
 if(o.t==='nerf'){var n=Math.floor(h/(2.4*s));for(var i=0;i<n;i++){var y0=i*2.4*s+R()*2*s,A=(4+R()*9)*s,f=(.004+R()*.006)/s,ph=R()*6;x.beginPath();
   for(var xx=0;xx<=w;xx+=6*s){var y=y0+A*Math.sin(xx*f+ph)+Math.sin(xx*f*3.1+ph*2)*A*.25;xx?x.lineTo(xx,y):x.moveTo(xx,y);}
   x.strokeStyle=rgba(o.l,.16+R()*.38);x.lineWidth=(.6+R()*1.6)*s;x.stroke();}
  var nv=o.vl?3:2;for(var v=0;v<nv;v++){var cx=R()*w,cy=h*(.3+R()*.5);for(var r=1;r<9;r++){x.beginPath();x.ellipse(cx,cy,(30+r*26)*s,(5+r*6)*s,0,Math.PI*1.05,Math.PI*1.95);x.strokeStyle=rgba(o.l,.4);x.lineWidth=1.8*s;x.stroke();}}
  for(var p=0;p<w*h/(300*s*s);p++){x.fillStyle=rgba(o.l,.18);x.fillRect(R()*w,R()*h,(2+R()*5)*s,.8*s);}
  wolken(x,w,h,R,[shade(o.b,.12),shade(o.b,-.12)],6,.15);ruis(x,w,h,R,8);}
 else if(o.t==='lak'){var g=x.createLinearGradient(0,0,w,h);g.addColorStop(0,'rgba(255,255,255,.18)');g.addColorStop(.5,'rgba(255,255,255,0)');g.addColorStop(1,'rgba(0,0,0,.08)');x.fillStyle=g;x.fillRect(0,0,w,h);
  x.fillStyle=rgba(shade(o.b,-.35),.6);x.fillRect(0,h*.36,w,3*s);x.fillStyle=rgba('#ffffff',.5);x.fillRect(0,h*.36+3*s,w,1.2*s);x.fillStyle=rgba(shade(o.b,-.25),.5);x.fillRect(w*.5-1*s,h*.36,2*s,h*.64);ruis(x,w,h,R,4);}
 else if(o.t==='hpl'){wolken(x,w,h,R,[shade(o.b,.1),shade(o.b,-.1)],16,.3);for(var q=0;q<w*h/(80*s*s);q++){x.fillStyle=rgba(R()<.5?'#ffffff':'#000000',.05+R()*.08);x.fillRect(R()*w,R()*h,1.4*s,1.4*s);}
  x.fillStyle='#2b2b2b';x.fillRect(0,h*.82,w,h*.18);x.fillStyle='rgba(255,255,255,.08)';for(var z=0;z<6;z++)x.fillRect(0,h*.82+z*h*.03,w,1);ruis(x,w,h,R,10);}
 else{marmer(x,w,h,R,V.marmer.blad);}
}
var TEK={marmer:marmer,hardsteen:hardsteen,travertin:travertin,terrazzo:terrazzo,micro:micro,tegel:tegel,metaal:metaal,glas:glas,hout:hout};

function teken(c){
 var r=c.getBoundingClientRect();if(!r.width)return;var ratio=(+c.getAttribute('height')||400)/(+c.getAttribute('width')||600);
 var w=Math.round(r.width*DPR),h=Math.round(r.width*ratio*DPR);c.width=w;c.height=h;c._w=r.width;
 var x=c.getContext('2d');if(!x)return;var s=c.getAttribute('data-s'),v=c.getAttribute('data-v')||'';
 var R=rng(hsh(s+v+(c.getAttribute('data-f')||'')+(c.getAttribute('data-p')||'')+(c.getAttribute('data-seed')||'')));
 var o=s==='tegel'?{f:c.dataset.f,p:c.dataset.p,k:c.dataset.k,g:c.dataset.g,vb:c.dataset.vb,gl:c.dataset.gl,tex:c.dataset.tex,view:c.dataset.view}:(V[s]&&V[s][v])||{};
 try{TEK[s](x,w,h,R,o,v);}catch(e){}
 c.setAttribute('data-klaar','1');
}

/* ---------------- adviezen (los te testen) ---------------- */
function adviesTegel(f,p,k,g){
 var d=String(f).split('x').map(Number),L=Math.max(d[0],d[1]),W=Math.min(d[0],d[1]),uit=[],pp=p;
 if(p==='visgraat'&&L===W){pp='stapel';uit.push('Visgraat kan alleen met rechthoekige tegels. Je ziet nu stapelverband.');}
 if(pp==='halfsteens'&&L>=60){uit.push('Let op: bij tegels van 60 cm en langer raden fabrikanten vaak hooguit 1/3 verspringing aan. Halfsteens geeft snel hoogteverschil in het midden van de tegel (overtand).');}
 var vb=L>=60?2:(L<=10?2:3);uit.push('Voegbreedte: ongeveer '+vb+' mm'+(L>=60?' (gerectificeerde tegel).':'.'));
 uit.push('Snijverlies: reken op '+(pp==='visgraat'?'15':'10')+'% extra tegels.');
 var dl=Math.abs(lum(k)-lum(g));
 if(dl>.42)uit.push('Veel contrast tussen tegel en voeg: elke voeg valt op en het patroon wordt zichtbaar. Mooi bij kleine en smalle tegels, onrustig bij grote tegels of scheve wanden.');
 else if(dl<.1)uit.push('Voeg in de kleur van de tegel: de voegen vallen bijna weg en het vlak oogt rustig.');
 else uit.push('Rustig contrast: je ziet het patroon, maar het wordt niet druk.');
 return {p:pp,vb:vb,tekst:uit};
}
function adviesVoeg(k,g,oud){
 var lg=lum(g),uit=[],dl=Math.abs(lum(k)-lg);
 if(lg>.8)uit.push('Een witte of heel lichte voeg laat vuil, zeepresten en schimmel het eerst zien. In de douche is lichtgrijs of een epoxyvoeg vaak verstandiger.');
 else if(lg<.25)uit.push('Een donkere voeg verbergt vuil, maar kan een witte waas van kalk of cement laten zien. Vraag de tegelzetter de cementsluier goed af te wassen.');
 else uit.push('Een middentint, zoals lichtgrijs of zand, is het meest vergevingsgezind: vuil en kalk vallen minder op.');
 if(dl>.42)uit.push('Groot contrast met de tegel: het voegpatroon wordt een deel van het ontwerp.');
 else if(dl<.1)uit.push('Bijna dezelfde kleur als de tegel: de wand oogt als één vlak.');
 if(oud)uit.push('Indicatie: zo kan een cementvoeg er na een paar jaar uitzien zonder goed onderhoud. Lichte voegen verkleuren het meest.');
 return {g:oud?mix(g,'#857b69',lg>.6?.38:.14):g,tekst:uit};
}
window.MTstaal={adviesTegel:adviesTegel,adviesVoeg:adviesVoeg,mix:mix,lum:lum};

/* ---------------- kiezers ---------------- */
function waarde(box,n){var i=box.querySelector('input[name="'+n+'"]:checked');return i?i.value:'';}
function lijst(el,t){el.innerHTML='';for(var i=0;i<t.length;i++){var li=document.createElement('li');li.textContent=t[i];el.appendChild(li);}}
var kz=document.querySelectorAll('.mt-kz');
for(var z=0;z<kz.length;z++)(function(box){
 var c=box.querySelector('canvas'),adv=box.querySelector('.mt-adv'),soort=box.getAttribute('data-kz'),id=box.id;
 function bij(){
  if(soort==='tegel'){var f=waarde(box,id+'-f'),p=waarde(box,id+'-p'),k=waarde(box,id+'-k'),g=waarde(box,id+'-g');var a=adviesTegel(f,p,k,g);
   var vis=box.querySelector('input[value="visgraat"]'),d=f.split('x');if(vis){vis.disabled=(d[0]===d[1]);}
   c.dataset.f=f;c.dataset.p=a.p;c.dataset.k=k;c.dataset.g=g;c.dataset.vb=a.vb;lijst(adv,a.tekst);
   var lbl=box.querySelector('.mt-kz-titel');if(lbl){var pn={stapel:'stapelverband',halfsteens:'halfsteens verband',derde:'1/3 verband',visgraat:'visgraat'}[a.p];lbl.textContent=f.replace('x',' × ').replace('.',',')+' cm in '+pn;}}
  else{var k2=waarde(box,id+'-k'),g2=waarde(box,id+'-g'),f2=waarde(box,id+'-f').split('|'),vb2=waarde(box,id+'-b'),oud=box.querySelector('input[name="'+id+'-o"]');
   var b=adviesVoeg(k2,g2,oud&&oud.checked);c.dataset.f=f2[0];c.dataset.p=f2[1];c.dataset.k=k2;c.dataset.g=b.g;c.dataset.vb=vb2;lijst(adv,b.tekst);}
  c.setAttribute('aria-label','Getekend voorbeeld: '+(box.querySelector('.mt-kz-titel')||{}).textContent);
  teken(c);
 }
 box.addEventListener('change',bij);box._bij=bij;
})(kz[z]);

/* ---------------- lui tekenen ---------------- */
var alle=document.querySelectorAll('canvas.mt-c');
function start(c){var b=c.closest('.mt-kz');if(b&&b._bij){b._bij();}else{teken(c);}}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){io.unobserve(e.target);start(e.target);}});},{rootMargin:'250px 0px'});
 for(var i=0;i<alle.length;i++)io.observe(alle[i]);}
else{for(var j=0;j<alle.length;j++)start(alle[j]);}
var tm;window.addEventListener('resize',function(){clearTimeout(tm);tm=setTimeout(function(){for(var i=0;i<alle.length;i++){var c=alle[i];if(c.getAttribute('data-klaar')&&Math.abs(c.getBoundingClientRect().width-c._w)>2)teken(c);}},200);});
})();
</script>"""
