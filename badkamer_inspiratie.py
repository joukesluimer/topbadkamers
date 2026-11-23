# -*- coding: utf-8 -*-
"""Badkamerinspiratie: /inspiratie/ en zes stijlpagina's (/inspiratie/<stijl>/).

Elke stijl heeft een eigen 3D-illustratie (renders/bs-*.html, metadata in
render_stijl_data.py), kenmerken, materialen en kleuren met stalen in CSS,
een globale kostenindicatie met bron, tips, valkuilen, een FAQ en links naar de
stijlkiezer, de kopersgidsen en het offerteformulier.

De kenmerken volgen de stijlkiezer (/tools/stijlkiezer/, badkamer_stijl.py) en het
artikel over badkamerstijlen (/kennisbank/badkamerstijlen/), zodat de site overal
hetzelfde vertelt.

Kosten (geraadpleegd november 2026, dezelfde bronnen en bedragen als /kosten/nieuwe-badkamer/):
- Homedeal, badkamer renoveren (€3.500 – €15.000, vaak €5.000 – €8.000):
  https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/
- Trustoo, nieuwe badkamer (€8.500 – €15.000 voor 5 – 10 m²):
  https://trustoo.nl/kosten/badkamer-renovatie-kosten/
- Slimster, compleet nieuwe badkamer (budget €3.000 – €7.000, midden €7.500 – €11.000, luxe €11.000 – €15.000):
  https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/
Onze richtprijs: meestal €6.000 – €18.000 voor een complete badkamer van 5 tot 9 m², inclusief 21% btw;
indeling basis €3.500 – €7.000, midden €7.000 – €12.000, luxe €12.000 – €20.000 (zoals op de kostenpagina).
"""

import datetime
import html as htmllib

from components import page, crumbs, title, faq_blok, cta_blok, cta_midden, prijs_balken
from data import SITE
from render_stijl_data import RENDERS_STIJL

try:  # de hash van de stijlkiezer volgt de groepen en stijlen uit badkamer_stijl.py
    from badkamer_stijl import STIJLEN as _SK_STIJLEN
except Exception:  # zonder stijlkiezer gewoon een link zonder hash
    _SK_STIJLEN = []

PAD = "/inspiratie/"
GEPUBLICEERD = "2026-11-23"

BRONNEN_KOSTEN = [
    ("Homedeal, badkamer renoveren kosten", "https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/"),
    ("Trustoo, wat kost een nieuwe badkamer", "https://trustoo.nl/kosten/badkamer-renovatie-kosten/"),
    ("Slimster, compleet nieuwe badkamer kosten", "https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/"),
]
NIVEAUS = [("Basis", 3500, 7000), ("Midden", 7000, 12000), ("Luxe", 12000, 20000)]

GIDSEN = {
    "inloopdouche-kopen": ("Inloopdouche kopen", "Glas, afvoer en maten van een inloopdouche."),
    "toilet-kiezen": ("Toilet kiezen", "Hangend of staand, en waar je op let."),
    "wastafelmeubel-kiezen": ("Wastafelmeubel kiezen", "Maten, materialen en soorten wasbakken."),
    "kranen-kiezen": ("Kranen kiezen", "Soorten kranen en afwerkingen zoals chroom en mat zwart."),
    "badkamertegels-kopen": ("Badkamertegels kopen", "Formaten, materialen en hoeveel je nodig hebt."),
    "douchesysteem-kiezen": ("Douchesysteem kiezen", "Regendouche, thermostaat, opbouw of inbouw."),
    "bad-of-douche": ("Bad of douche?", "De voor- en nadelen naast elkaar."),
}

KENNIS = {
    "badkamerstijlen": ("Badkamerstijlen uitgelegd", "Vijf stijlen met materialen en onderhoud."),
    "tegels-kiezen": ("Tegels kiezen", "Formaat, materiaal, voegen en antislip."),
    "kleine-badkamer-indelen": ("Kleine badkamer indelen", "Slimme indelingen voor weinig ruimte."),
    "badkamer-waterdicht-maken": ("Badkamer waterdicht maken", "Zo blijft de douchehoek droog."),
    "inloopdouche-zonder-drempel": ("Inloopdouche zonder drempel", "Afschot, goot en waterkering."),
    "badkamer-ventilatie": ("Badkamer ventileren", "Vocht en schimmel voorkomen."),
}

# ---------------------------------------------------------------------------
# Stijlen. Kleurstalen: (naam, hex, waar). Materialen: (naam, uitleg, css-achtergrond voor het staal).
# ---------------------------------------------------------------------------

STIJLEN = [
    dict(
        slug="moderne-badkamer", naam="Moderne badkamer", kort="Modern", stijl="modern",
        h1="Moderne badkamer: kenmerken, materialen en tips",
        seo="Moderne badkamer: kenmerken, kleuren en tips",
        description="Een moderne badkamer is strak en rustig: grote tegels, een zwevend meubel en mat zwarte kranen. Met materialen, kleuren, kosten, tips en valkuilen.",
        galerij="Strak en rustig: grote tegels, weinig voegen, een zwevend meubel en contrast tussen licht en donker.",
        intro="Een moderne badkamer draait om rust. Strakke lijnen, grote tegels met weinig voegen en een beperkt kleurenpalet van wit, grijs, beige en zwart. In de illustratie zie je een inloopdouche met helder glas, een zwevend eiken meubel en mat zwarte kranen in de wand.",
        kenmerken=[
            "Grote tegels (60 × 60 cm of groter) met smalle voegen, zodat wand en vloer rustig ogen.",
            "Contrast tussen licht en donker, bijvoorbeeld witte wanden en een antraciet vloer.",
            "Een zwevend wastafelmeubel en een hangtoilet: de vloer loopt eronder door.",
            "Een inloopdouche met een heldere glazen wand, vaak met een smal profiel.",
            "Kranen in de wand of strakke opbouwkranen, vaak in mat zwart.",
            "Weinig spullen in zicht: een nis in de douche en lades in het meubel.",
        ],
        materialen=[
            ("Grote witte wandtegels", "Tegels van 60 × 120 cm in warm wit met een zachte glans. Weinig voegen, dus makkelijk schoon te houden.",
             "linear-gradient(90deg,#f1efea 0 49%,#d9d6cf 49% 51%,#f1efea 51%)"),
            ("Antraciet vloer 60 × 60", "Donkere tegel met een lichte betonstructuur. Doorgelegd in de douche voor één rustig vlak.",
             "linear-gradient(90deg,#4a4c4f 0 48%,#3b3c3e 48% 52%,#4d5053 52%)"),
            ("Eiken fineer", "Een zwevend meubel in licht eiken brengt warmte in het strakke beeld.",
             "repeating-linear-gradient(90deg,#c79a63 0 5px,#b8894f 5px 6px,#cfa46f 6px 11px)"),
            ("Mat zwart metaal", "Kranen, regendouche, bedieningsplaat en spiegelrand in dezelfde kleur.",
             "linear-gradient(135deg,#3a3a3a,#111 50%,#2a2a2a)"),
            ("Helder glas", "Een glazen wand zonder deur, met een smal profiel aan de muur.",
             "linear-gradient(135deg,rgba(210,232,224,.55),rgba(255,255,255,.9) 45%,rgba(200,225,215,.5))"),
        ],
        kleuren=[("Warm wit", "#f1efea", "wanden"), ("Antraciet", "#4a4c4f", "vloer en douche"),
                 ("Licht eiken", "#c09468", "meubel"), ("Mat zwart", "#1b1b1c", "kranen en accenten"),
                 ("Zand", "#d9d2c6", "textiel")],
        kosten="Een moderne badkamer kan eenvoudig zijn, maar een paar typische keuzes maken het werk duurder: inbouwkranen in de wand, grote tegels die een heel vlakke ondergrond vragen, een glazen wand zonder profiel en een hangtoilet met inbouwreservoir. Met grote tegels, inbouwkranen en een regendouche zit je volgens de indeling op onze kostenpagina eerder in het midden- of luxesegment.",
        tips=[
            "Kies grote tegels (60 × 60 cm of groter): minder voegen geeft een rustig vlak.",
            "Een zwevend meubel en een hangtoilet laten de vloer doorlopen. Dat oogt ruimer en maakt dweilen makkelijker.",
            "Houd het bij twee of drie kleuren, bijvoorbeeld wit, antraciet en hout.",
            "Leg dezelfde vloertegel in de douche, met een douchegoot. Dan loopt de vloer zonder drempel door.",
        ],
        valkuilen=[
            "Mat zwarte kranen laten kalk en vingerafdrukken zien. Bij hard water helpt het om ze na gebruik droog te maken.",
            "Grote tegels op een scheve wand of vloer geven randen die net niet gelijk liggen. Laat de ondergrond eerst vlak maken.",
            "Alles strak en wit kan kil worden. Breng warmte terug met hout, textiel en warm licht.",
        ],
        faq=[
            ("Wat maakt een badkamer modern?", "Strakke lijnen, grote tegels met weinig voegen, een rustig kleurenpalet en weinig spullen in zicht. Een zwevend meubel, een hangtoilet en een inloopdouche met helder glas horen er vaak bij."),
            ("Welke kleuren passen in een moderne badkamer?", "Wit, grijs, beige en zwart vormen de basis. Contrast tussen een lichte wand en een donkere vloer is typisch. Hout geeft warmte."),
            ("Zijn zwarte kranen lastig in onderhoud?", "Ze laten kalk en vingerafdrukken sneller zien dan chroom. Droog ze na gebruik af en gebruik geen schurende middelen."),
            ("Kan een moderne badkamer ook in een klein huis?", "Ja. Lichte grote tegels, een zwevend meubel en helder glas laten een kleine ruimte juist groter lijken."),
        ],
        gidsen=["inloopdouche-kopen", "wastafelmeubel-kiezen", "kranen-kiezen", "badkamertegels-kopen"],
        kennis=["badkamerstijlen", "tegels-kiezen", "inloopdouche-zonder-drempel"],
    ),
    dict(
        slug="landelijke-badkamer", naam="Landelijke badkamer", kort="Landelijk", stijl="landelijk",
        h1="Landelijke badkamer: warm, ambachtelijk en sfeervol",
        seo="Landelijke badkamer: materialen, kleuren en tips",
        description="Een landelijke badkamer is warm, met handgemaakte tegels, hout, een tegel met patroon en messing kranen. Lees de kenmerken, materialen, kosten en valkuilen.",
        galerij="Warm en ambachtelijk: handgemaakte tegels, een patroon op de vloer, eiken en messing kranen.",
        intro="Een landelijke badkamer voelt warm en een beetje ambachtelijk. Natuurlijke tinten, materialen met structuur en een tegel met patroon op de vloer. In de illustratie zie je groene handgemaakte tegels tot halverwege de wand, kalkverf erboven, een vrijstaand bad en messing kranen.",
        kenmerken=[
            "Natuurlijke tinten en materialen met structuur, zoals handgemaakte tegels en hout.",
            "Tegels tot halverwege de wand, met kalkverf of vochtbestendige verf erboven.",
            "Eén tegel met patroon, vaak op de vloer, gecombineerd met effen tegels.",
            "Een wastafelmeubel in eiken of een lichte houtkleur, soms op pootjes.",
            "Kranen in messing, mat goud of brons.",
            "Een vrijstaand bad als blikvanger, als de ruimte het toelaat.",
        ],
        materialen=[
            ("Groene handgemaakte tegel", "Kleine tegel van 10 × 10 cm in zellige-stijl. Elke tegel verschilt iets in kleur en glans.",
             "conic-gradient(#2f6b55 0 25%,#47866b 0 50%,#2a604c 0 75%,#3b7a61 0)"),
            ("Kalkverf", "Een zachte, wolkerige verf in gebroken wit boven de tegels. Kies een soort die geschikt is voor natte ruimten.",
             "radial-gradient(circle at 30% 30%,#f3eee4 0 30%,transparent 60%),#e6dfd2"),
            ("Cementtegel-look", "Keramische vloertegel met een patroon in de stijl van oude cementtegels.",
             "radial-gradient(circle at 0 0,#6d7d74 0 30%,transparent 31%),radial-gradient(circle at 100% 100%,#6d7d74 0 30%,transparent 31%),radial-gradient(circle,#6d7d74 0 18%,#ebe5d8 19%)"),
            ("Eiken", "Een meubel in eiken met een zichtbare nerf. Houtlook-tegels geven hetzelfde beeld waar het nat wordt.",
             "repeating-linear-gradient(90deg,#b88c5c 0 5px,#a67b4c 5px 6px,#c29766 6px 11px)"),
            ("Messing", "Warm en opvallend metaal voor kranen, spiegelrand en handdoekrek.",
             "linear-gradient(135deg,#f3d58a,#b88a35 50%,#e7c46f)"),
        ],
        kleuren=[("Flessengroen", "#3f7a62", "wandtegels"), ("Gebroken wit", "#ece6da", "wand boven de tegels"),
                 ("Grijsgroen", "#6d7d74", "patroon op de vloer"), ("Eiken", "#b88c5c", "meubel"),
                 ("Messing", "#c9a35c", "kranen")],
        kosten="Handgemaakte tegels en een patroonvloer zijn arbeidsintensief. Kleine tegels betekenen meer voegen en meer legwerk per vierkante meter, en bij een patroon moet de tegelzetter de tegels goed uitlijnen. Een vrijstaand bad vraagt een afvoer op de juiste plek in de vloer. Met een bad en bijzondere tegels kom je volgens de indeling op onze kostenpagina eerder in het midden- of luxesegment.",
        tips=[
            "Combineer één tegel met patroon met effen tegels. Twee drukke tegels naast elkaar vechten om aandacht.",
            "Zellige verschilt per tegel in kleur en dikte. Dat hoort zo; vraag de tegelzetter of hij er ervaring mee heeft.",
            "Een staande kraan bij het bad of een ouderwetse douchekop past goed bij deze stijl.",
            "Tegel tot halverwege de wand en maak de rest af met vochtbestendige verf. Dat scheelt tegels en oogt zacht.",
        ],
        valkuilen=[
            "Echt hout in een natte ruimte vraagt bescherming en goede ventilatie. Houtlook-tegels geven hetzelfde beeld zonder dat onderhoud.",
            "Echte cementtegels moeten worden geïmpregneerd. Keramische tegels met een cementtegelpatroon zijn makkelijker.",
            "Te veel verschillende materialen geeft onrust. Houd het bij één basis en hooguit twee accenten.",
        ],
        faq=[
            ("Wat hoort er in een landelijke badkamer?", "Natuurlijke tinten, hout of houtlook, tegels met een handgemaakte uitstraling, een patroon op de vloer en kranen in messing, mat goud of brons. Een vrijstaand bad is een mooie blikvanger."),
            ("Kan ik echt hout gebruiken in een landelijke badkamer?", "Dat kan buiten de natte zone, met goede bescherming en ventilatie. In de douche zijn houtlook-tegels een betere keuze."),
            ("Past een landelijke badkamer in een nieuwbouwhuis?", "Ja. Begin met een rustige basis en kies een paar landelijke accenten, zoals een eiken meubel, messing kranen of een vloer met patroon."),
            ("Wat is zellige?", "Een kleine, handgemaakte geglazuurde tegel. Elke tegel verschilt in kleur, glans en dikte. Dat geeft een levendige wand, maar vraagt een tegelzetter met ervaring."),
        ],
        gidsen=["bad-of-douche", "kranen-kiezen", "wastafelmeubel-kiezen", "badkamertegels-kopen"],
        kennis=["badkamerstijlen", "tegels-kiezen", "badkamer-ventilatie"],
    ),
    dict(
        slug="industriele-badkamer", naam="Industriële badkamer", kort="Industrieel", stijl="industrieel",
        h1="Industriële badkamer: beton, zwart staal en hout",
        seo="Industriële badkamer: betonlook, zwart en tips",
        description="Een industriële badkamer is stoer: betonlook, zwart staal en warm hout. Bekijk de kenmerken, materialen en kleuren, wat het ongeveer kost en de valkuilen.",
        galerij="Stoer: grote tegels in betonlook, een douchewand met zwart profiel en hout voor de warmte.",
        intro="Een industriële badkamer is stoer en een beetje rauw. Betonlook, zwart metaal en donkere kleuren, met hout om het niet te koel te maken. In de illustratie zie je grote tegels in betonlook, een douchewand met zwart stalen profiel en een opbouwregendouche in mat zwart.",
        kenmerken=[
            "Grote grijze tegels in betonlook op wand en vloer, of een naadloze wand.",
            "Een glazen douchewand met zwarte profielen, soms met roeden zoals een fabrieksraam.",
            "Opbouwkranen en een opbouwregendouche in mat zwart, met zichtbare leidingen.",
            "Een donker meubel, vaak gecombineerd met een blad van hout.",
            "Koel licht en zwarte lampen; hout, planten en textiel brengen warmte.",
        ],
        materialen=[
            ("Betonlook-tegel 60 × 120", "Grote grijze tegel die op beton lijkt. Waterdicht en makkelijker te onderhouden dan echt beton of betonstuc.",
             "radial-gradient(circle at 30% 40%,#a8a6a0 0 8%,transparent 9%),radial-gradient(circle at 70% 70%,#8f8d87 0 6%,transparent 7%),#9c9a94"),
            ("Lichtgrijze vloer", "Dezelfde betonlook, iets lichter, in halfsteens verband. Weinig voegen, dus de ruimte oogt groot.",
             "linear-gradient(90deg,#a6a49e 0 66%,#94928c 66% 67%,#a6a49e 67%)"),
            ("Zwart staal", "Profielen rond het glas met horizontale en verticale roeden.",
             "linear-gradient(90deg,transparent 0 46%,#1b1b1c 46% 54%,transparent 54%),linear-gradient(0deg,transparent 0 46%,#1b1b1c 46% 54%,transparent 54%),#dfe8e4"),
            ("Antraciet mat", "Donker meubel dat contrast geeft met de grijze tegels.",
             "#36393c"),
            ("Eiken blad", "Een houten blad op het meubel en een plankje in de douche voor warmte.",
             "repeating-linear-gradient(90deg,#a87a4e 0 5px,#966b42 5px 6px,#b48656 6px 11px)"),
        ],
        kleuren=[("Betongrijs", "#9c9a94", "wanden"), ("Lichtgrijs", "#a6a49e", "vloer"),
                 ("Antraciet", "#36393c", "meubel"), ("Mat zwart", "#1b1b1c", "staal en kranen"),
                 ("Eiken", "#a87a4e", "blad en accenten")],
        kosten="Grote betonlook-tegels vragen een vlakke ondergrond en kosten meer legloon per vierkante meter dan standaardformaten. Een douchewand met stalen profielen en roeden is duurder dan een eenvoudige glazen wand. Kies je in plaats van tegels voor een naadloze wand, dan heb je een systeem nodig dat geschikt is voor natte ruimten. Opbouwkranen zijn juist vaak minder werk dan inbouwkranen, omdat de muur niet open hoeft.",
        tips=[
            "Beton-look in tegels is waterdicht en makkelijker te onderhouden dan echt beton of betonstuc.",
            "Breng warmte terug met hout, een plant of warm licht, anders oogt het al snel koud.",
            "Een glazen wand met een zwart profiel is een typisch industrieel detail.",
            "Kies opbouwkranen als je de leidingen niet in de muur wilt wegwerken. Dat past bij de stijl en scheelt breekwerk.",
        ],
        valkuilen=[
            "Mat zwart laat kalk en vingerafdrukken zien. Trek de douchewand bij hard water na gebruik droog.",
            "Een naadloze wandafwerking vraagt een systeem dat geschikt is voor natte ruimten. Vraag de vakman welk systeem hij gebruikt.",
            "Alles grijs en zwart in een kleine badkamer zonder raam kan somber worden. Zorg voor genoeg licht.",
        ],
        faq=[
            ("Is een betonlook-tegel beter dan echt beton?", "Voor de meeste badkamers wel. Een keramische tegel in betonlook is waterdicht, slijtvast en makkelijk schoon te houden. Echt beton of betonstuc vraagt een goede afwerking en meer onderhoud."),
            ("Hoe maak ik een industriële badkamer minder koud?", "Combineer het grijs en zwart met hout, planten, textiel en warm licht. Een eiken blad op het meubel is al genoeg om het beeld warmer te maken."),
            ("Wat is een douchewand met roeden?", "Een glazen wand met zwarte stalen of aluminium profielen die het glas in vakken verdelen, zoals bij een oud fabrieksraam."),
            ("Passen chromen kranen in een industriële badkamer?", "Dat kan, maar mat zwart of een geborstelde rvs-look past beter bij het stoere beeld."),
        ],
        gidsen=["inloopdouche-kopen", "douchesysteem-kiezen", "kranen-kiezen", "badkamertegels-kopen"],
        kennis=["badkamerstijlen", "tegels-kiezen", "badkamer-waterdicht-maken"],
    ),
    dict(
        slug="japandi-badkamer", naam="Japandi-badkamer", kort="Japandi", stijl="japandi",
        h1="Japandi-badkamer: rust, natuurtinten en licht hout",
        seo="Japandi-badkamer: kenmerken, kleuren en tips",
        description="Japandi mengt Japans en Scandinavisch: licht hout, gedempte natuurtinten, weinig spullen en zwarte accenten. Met materialen, kleuren, kosten, tips en een FAQ.",
        galerij="Japans en Scandinavisch: licht hout, gedempte natuurtinten, weinig spullen en zwarte accenten.",
        intro="Japandi is een mix van Japans en Scandinavisch. Licht hout, gedempte natuurtinten, eenvoudige vormen en weinig spullen in zicht, met hier en daar een zwart accent. In de illustratie zie je gebroken witte tegels in visgraat, zandkleurige kalkverf, een terrazzovloer en een eiken meubel.",
        kenmerken=[
            "Gedempte tinten: zand, gebroken wit, salie en licht hout.",
            "Langwerpige tegels in visgraat of een rustige tegel met kleine structuur, zoals terrazzo.",
            "Een eenvoudig meubel in licht eiken, vaak met een opzetkom.",
            "Zwart alleen als accent: kraan, spiegelrand, douchegoot.",
            "Weinig spullen in zicht, met een nis in de douche en lades in het meubel.",
            "Natuurlijke details zoals een houten krukje, linnen handdoeken en een plant.",
        ],
        materialen=[
            ("Visgraattegel gebroken wit", "Langwerpige tegel van 7,5 × 30 cm, schuin in visgraat gelegd. Geeft beweging aan de wand.",
             "repeating-linear-gradient(45deg,#d6cfc2 0 2px,#ece6db 2px 10px),#ece6db"),
            ("Zandkleurige kalkverf", "Een zachte, warme wand boven de tegels. Kies een soort die geschikt is voor natte ruimten.",
             "radial-gradient(circle at 30% 30%,#e2d8c8 0 30%,transparent 60%),#d9cdbb"),
            ("Warme terrazzo", "Lichte tegel met steenslag in zand, grijs en roest. Op de vloer en in de douche.",
             "radial-gradient(circle at 30% 30%,#b58c6a 0 9%,transparent 10%),radial-gradient(circle at 70% 65%,#8f8a82 0 8%,transparent 9%),radial-gradient(circle at 55% 25%,#6f6a63 0 5%,transparent 6%),#e6dfd3"),
            ("Licht eiken", "Rustige nerf in een lichte tint, voor het meubel en een krukje.",
             "repeating-linear-gradient(90deg,#cfab80 0 5px,#c09c72 5px 6px,#d6b48a 6px 11px)"),
            ("Mat zwart", "Alleen voor accenten: de kraan, de regendouche en de rand van de spiegel.",
             "linear-gradient(135deg,#3a3a3a,#111 50%,#2a2a2a)"),
        ],
        kleuren=[("Gebroken wit", "#ece6db", "visgraattegel"), ("Zand", "#d9cdbb", "wanden"),
                 ("Terrazzo", "#e6dfd3", "vloer"), ("Licht eiken", "#cfab80", "meubel"),
                 ("Salie", "#a4ae95", "textiel"), ("Mat zwart", "#1b1b1c", "accenten")],
        kosten="Visgraat vraagt veel snijwerk en meer legtijd dan tegels in een recht verband. Een nis in de douche moet al in de planning zitten, omdat de wand daarvoor wordt voorbereid. Daar staat tegenover dat Japandi weinig spullen en eenvoudige vormen gebruikt: met een gewoon eiken meubel en een standaard inloopdouche blijf je volgens de indeling op onze kostenpagina vaak in het middensegment.",
        tips=[
            "Kies gedempte tinten: zand, gebroken wit, salie en licht hout.",
            "Weinig spullen in zicht. Een nis in de douche en lades in het meubel helpen daarbij.",
            "Gebruik zwart alleen als accent, bijvoorbeeld bij de kraan of de spiegelrand.",
            "Leg visgraat alleen op één wand, bijvoorbeeld achter het meubel. Dat geeft rust en scheelt snijwerk.",
        ],
        valkuilen=[
            "Witte voegen kunnen verkleuren. Een lichtgrijze of zandkleurige voeg blijft langer mooi.",
            "Een opzetkom vraagt een hoge kraan of een wandkraan met de juiste uitloop. Controleer de maten voor je koopt.",
            "Te veel decoratie past niet bij de stijl. Kies een paar dingen en laat de rest weg.",
        ],
        faq=[
            ("Wat is japandi?", "Een mix van Japanse en Scandinavische inrichting. Licht hout, gedempte natuurtinten, eenvoudige vormen en weinig spullen, met hier en daar een zwart accent."),
            ("Welke tegels passen bij een japandi-badkamer?", "Rustige tegels in natuurtinten: langwerpige tegels in visgraat, terrazzo met fijne steenslag of een effen tegel in zand of gebroken wit."),
            ("Is japandi hetzelfde als Scandinavisch?", "Niet helemaal. Scandinavisch is vaak lichter en witter. Japandi heeft meer aardse tinten, donkerdere accenten en nog minder spullen."),
            ("Kan japandi in een kleine badkamer?", "Ja. De lichte tinten en het kleine aantal spullen werken goed in een kleine ruimte. Houd de visgraat dan bij één wand."),
        ],
        gidsen=["wastafelmeubel-kiezen", "inloopdouche-kopen", "badkamertegels-kopen", "kranen-kiezen"],
        kennis=["badkamerstijlen", "tegels-kiezen", "inloopdouche-zonder-drempel"],
    ),
    dict(
        slug="klassieke-badkamer", naam="Klassieke badkamer", kort="Klassiek", stijl="klassiek",
        h1="Klassieke badkamer: tijdloos, met details",
        seo="Klassieke badkamer: metrotegels, marmer en tips",
        description="Een klassieke badkamer is tijdloos: metrotegels, marmerlook, een bad op pootjes en goud- of messingkleurige kranen. Met materialen, kosten, tips en valkuilen.",
        galerij="Tijdloos: metrotegels in halfsteens verband, marmerlook, een bad op pootjes en kruisgrepen.",
        intro="Een klassieke badkamer is tijdloos en heeft oog voor details. Metrotegels in halfsteens verband, marmerlook op de vloer, een wit meubel met kaders en kranen met kruisgrepen. In de illustratie zie je een bad op gouden pootjes, een spiegel met boog en goudkleurige kranen.",
        kenmerken=[
            "Witte metrotegels in halfsteens verband, vaak tot ongeveer 1,5 meter hoog.",
            "Een vloer in marmerlook of met een patroontegel.",
            "Een wit meubel met kaders en knopjes, of een staande wastafel.",
            "Kranen met kruisgrepen in chroom, goud of messing.",
            "Een vrijstaand bad op pootjes, als er ruimte is.",
            "Alle metalen in dezelfde kleur: kraan, spiegelrand, handdoekrek en wandlampen.",
        ],
        materialen=[
            ("Metrotegel 7,5 × 15", "Witte geglazuurde tegel met afgeschuinde rand, in halfsteens verband met een lichtgrijze voeg.",
             "repeating-linear-gradient(0deg,#bdbab3 0 2px,#f4f2ec 2px 12px)"),
            ("Marmerlook", "Witte tegel met grijze aders. Makkelijker te onderhouden dan echt marmer.",
             "linear-gradient(120deg,#f1f0ec 0 40%,#bfc0c4 41% 42.5%,#f1f0ec 43.5% 70%,#d4d5d8 71% 71.8%,#f1f0ec 72.5%)"),
            ("Grijsgroene verf", "Zachte kleur boven de tegels. Kies een verf die geschikt is voor natte ruimten.",
             "#c9d0c8"),
            ("Witte lak", "Een meubel met kaders in wit, op pootjes, met een blad in marmerlook.",
             "linear-gradient(135deg,#fff,#ece9e2)"),
            ("Goud", "Warm metaal voor kranen met kruisgrepen, de pootjes van het bad en de spiegelrand.",
             "linear-gradient(135deg,#f3d58a,#b88a35 50%,#e7c46f)"),
        ],
        kleuren=[("Wit", "#f4f2ec", "metrotegels"), ("Lichtgrijs", "#bdbab3", "voegen"),
                 ("Grijsgroen", "#c9d0c8", "wand boven de tegels"), ("Marmerwit", "#f1f0ec", "vloer"),
                 ("Goud", "#d9b26a", "kranen en details")],
        kosten="Kleine tegels zoals metrotegels vragen meer legwerk per vierkante meter dan een standaardtegel, en een patroontegel op de vloer vraagt veel snijwerk. Een bad op pootjes met een staande badkraan heeft een afvoer en wateraansluitingen in de vloer nodig. Met een bad en veel details kom je volgens de indeling op onze kostenpagina eerder in het midden- of luxesegment.",
        tips=[
            "Metrotegels in halfsteens verband zijn tijdloos; een lichtgrijze voeg is minder gevoelig voor vuil dan een witte.",
            "Marmerlook-tegels zijn makkelijker te onderhouden dan echt marmer, dat zuur en kalk slecht verdraagt.",
            "Kies alle metalen in dezelfde kleur: kraan, spiegelrand, handdoekrek en bedieningsplaat.",
            "Maak de tegels af met een bies of tegellijst. Dat geeft een nette rand tussen tegels en verf.",
        ],
        valkuilen=[
            "Veel voegen en details betekent meer schoonmaakwerk.",
            "Echt marmer is gevoelig voor zure schoonmaakmiddelen en kalkvlekken.",
            "Patroontegels van echt cement moeten worden geïmpregneerd; keramische patroontegels zijn makkelijker.",
        ],
        faq=[
            ("Wat hoort er in een klassieke badkamer?", "Metrotegels, marmer of marmerlook, een wit meubel met kaders, kranen met kruisgrepen en eventueel een bad op pootjes. Details zoals een tegellijst en wandlampen maken het af."),
            ("Welke voegkleur past bij witte metrotegels?", "Een lichtgrijze voeg is minder gevoelig voor vuil dan een witte en laat het tegelpatroon mooi zien."),
            ("Is echt marmer geschikt voor een badkamer?", "Het kan, maar echt marmer verdraagt zuur en kalk slecht en vraagt onderhoud. Marmerlook-tegels geven hetzelfde beeld met minder zorgen."),
            ("Goud of chroom in een klassieke badkamer?", "Beide passen. Chroom is fris en tijdloos, goud of messing is warmer en chiquer. Kies één kleur voor alle metalen."),
        ],
        gidsen=["bad-of-douche", "kranen-kiezen", "wastafelmeubel-kiezen", "badkamertegels-kopen"],
        kennis=["badkamerstijlen", "tegels-kiezen", "badkamer-ventilatie"],
    ),
    dict(
        slug="kleine-badkamer", naam="Kleine badkamer", kort="Kleine badkamer", stijl="klein",
        h1="Kleine badkamer inrichten: licht, slim en ruimtelijk",
        seo="Kleine badkamer: indeling, kleuren en tips",
        description="Zo oogt een kleine badkamer groter: lichte grote tegels, een inloopdouche met helder glas en een zwevend meubel. Met een indeling van 1,8 × 2,2 m, kosten en tips.",
        galerij="Een badkamer van 1,8 × 2,2 m: lichte grote tegels, helder glas en een smal zwevend meubel.",
        intro="In een kleine badkamer telt elke centimeter. Lichte kleuren, grote tegels, helder glas en meubels die zweven laten de ruimte groter lijken. De illustratie toont een badkamer van ongeveer 1,8 bij 2,2 meter met een inloopdouche van 90 × 90 cm in de hoek, een hangtoilet ernaast en een smal meubel met een grote spiegel aan de zijwand.",
        kenmerken=[
            "Lichte kleuren en grote tegels, zodat de wanden rustig en ver weg lijken.",
            "Een inloopdouche met helder glas in plaats van een cabine met deuren.",
            "Dezelfde vloertegel in de douche en daarbuiten, met een douchegoot.",
            "Een smal zwevend meubel en een hangtoilet: de vloer blijft zichtbaar.",
            "Een grote spiegel en goed licht boven de wastafel.",
            "Een nis in de douchewand in plaats van rekjes.",
        ],
        indeling=[
            ("Inloopdouche in de hoek", "90 × 90 cm, met één heldere glazen wand en een goot langs de achterwand."),
            ("Hangtoilet naast de douche", "Tegen dezelfde wand als de douche, zodat de afvoer kort blijft."),
            ("Smal meubel aan de zijwand", "60 × 40 cm, met een grote spiegel erboven. De deur blijft vrij."),
        ],
        materialen=[
            ("Witte wandtegel 30 × 60", "Lichte tegel met een zachte glans. Staand gelegd, zodat het plafond hoger lijkt.",
             "linear-gradient(90deg,#f3f2ef 0 48%,#dcdad5 48% 52%,#f3f2ef 52%)"),
            ("Lichtgrijze vloer 60 × 60", "Grote tegel met weinig voegen, ook in de douche. De vloer loopt zo zonder onderbreking door.",
             "linear-gradient(90deg,#a8a6a0 0 48%,#96948e 48% 52%,#aaa8a2 52%)"),
            ("Wit hoogglans", "Een wit meubel valt weg tegen de wand en weerkaatst licht.",
             "linear-gradient(135deg,#fff,#e8ecee)"),
            ("Chroom", "Glanzend metaal dat licht weerkaatst. Past bij bijna elke stijl.",
             "linear-gradient(135deg,#f5f7f9,#9aa3ab 50%,#e9edf0)"),
            ("Helder glas", "Een glazen wand zonder deur onderbreekt de ruimte niet.",
             "linear-gradient(135deg,rgba(210,232,224,.55),rgba(255,255,255,.9) 45%,rgba(200,225,215,.5))"),
        ],
        kleuren=[("Wit", "#f3f2ef", "wanden"), ("Lichtgrijs", "#a8a6a0", "vloer en douche"),
                 ("Wit hoogglans", "#f5f5f3", "meubel"), ("Chroom", "#c9cfd4", "kranen"),
                 ("IJsblauw", "#c9d6dc", "textiel")],
        kosten="Een kleine badkamer is in totaal goedkoper dan een grote, maar per vierkante meter juist duurder. Sloopwerk, leidingwerk en sanitair zijn grotendeels vaste kosten. Een eenvoudige kleine badkamer met basissanitair kan volgens de bronnen vanaf ongeveer €3.500. Blijven douche, toilet en wastafel op hun plek, dan scheelt dat het meeste geld.",
        tips=[
            "Kies een inloopdouche met helder glas in plaats van een cabine met deuren: het glas onderbreekt de ruimte niet.",
            "Leg dezelfde tegel op de vloer en in de douche, dan loopt de vloer visueel door.",
            "Een grote spiegel en goed licht boven de wastafel maken de ruimte groter.",
            "Kies een smal meubel (bijvoorbeeld 40 cm diep) en een kraan die niet ver uitsteekt.",
        ],
        valkuilen=[
            "Een kleine badkamer wordt snel vochtig. Zorg voor goede ventilatie, zeker als er geen raam is.",
            "Een draaideur van de douche of de badkamer zelf kan botsen met het toilet of meubel. Meet de draairichting na.",
            "Donkere tegels en veel verschillende materialen maken een kleine ruimte kleiner.",
        ],
        faq=[
            ("Hoe laat ik een kleine badkamer groter lijken?", "Met lichte kleuren, grote tegels, helder glas, een zwevend meubel, een hangtoilet en een grote spiegel. Leg dezelfde vloertegel in de douche, zodat de vloer doorloopt."),
            ("Past een inloopdouche in een badkamer van 1,8 × 2,2 meter?", "Ja. Een inloopdouche van 90 × 90 cm in de hoek, met een hangtoilet ernaast en een smal meubel aan de zijwand, past goed. Laat een vakman wel controleren of de afvoer er kan komen."),
            ("Welke tegels passen in een kleine badkamer?", "Lichte, grote tegels met weinig voegen. Een staande wandtegel laat het plafond hoger lijken."),
            ("Wat kost een kleine badkamer?", "Een eenvoudige kleine badkamer kan vanaf ongeveer €3.500, inclusief btw. Per vierkante meter is een kleine badkamer duurder dan een grote, omdat sloop, leidingwerk en sanitair grotendeels vaste kosten zijn."),
        ],
        gidsen=["inloopdouche-kopen", "toilet-kiezen", "wastafelmeubel-kiezen", "badkamertegels-kopen"],
        kennis=["kleine-badkamer-indelen", "badkamer-ventilatie", "inloopdouche-zonder-drempel"],
    ),
]

# ---------------------------------------------------------------------------
# Hulpjes
# ---------------------------------------------------------------------------

LINKS = [(PAD, "Badkamer inspiratie", "Zes badkamerstijlen in beeld, met kenmerken, materialen en kleuren.")] + [
    (f"{PAD}{s['slug']}/", s["naam"], s["galerij"]) for s in STIJLEN]


def _esc(t):
    return htmllib.escape(t, quote=True)


def _render_img(slug, sizes, boven_vouw=False):
    """Responsieve <img> voor een stijlrender: srcset 400/800/1600 en vaste width/height."""
    r = RENDERS_STIJL[slug]
    n = r["naam"]
    laden = 'loading="eager" fetchpriority="high"' if boven_vouw else 'loading="lazy"'
    return (f'<img src="/assets/fotos/renders/{n}-800.webp" '
            f'srcset="/assets/fotos/renders/{n}-400.webp 400w, /assets/fotos/renders/{n}-800.webp 800w, '
            f'/assets/fotos/renders/{n}-1600.webp 1600w" sizes="{sizes}" width="{r["w"]}" height="{r["h"]}" '
            f'alt="{_esc(r["alt"])}" {laden} decoding="async">')


def _sk_hash(stijl_id):
    """Hash voor de stijlkiezer, in de vorm die badkamer_stijl.py leest (#wand=..&vloer=..&stijl=..)."""
    st = next((s for s in _SK_STIJLEN if s.get("id") == stijl_id), None)
    if not st:
        return ""
    # dezelfde zes groepen als GROEPEN in het script van de stijlkiezer
    delen = [f"{g}={st[g]}" for g in ("wand", "vloer", "kraan", "meubel", "douche", "licht") if g in st]
    return "#" + "&".join(delen + [f"stijl={stijl_id}"])


def _kaart(href, soort, naam, oms):
    return (f'<a href="{href}"><span class="bi-soort">{soort}</span><span class="bi-naam">{naam}</span>'
            f'<span class="bi-oms">{oms}</span></a>')


CSS = """<style>
.bi-hero{margin:18px 0 0}
.bi-fig{position:relative;margin:0;border-radius:var(--radius);overflow:hidden;background:#e9e6e0;aspect-ratio:3/2}
.bi-fig img{display:block;width:100%;height:auto}
.bi-label{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.9);color:#334;font-size:.74rem;padding:3px 9px;border-radius:999px}
.bi-bij{font-size:.86rem;color:var(--muted,#5b6470);margin:8px 0 0}
.bi-galerij{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:22px;margin-top:22px}
.bi-kaart{display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:var(--radius);overflow:hidden;text-decoration:none;color:inherit;transition:border-color .15s,box-shadow .15s}
.bi-kaart:hover,.bi-kaart:focus-visible{border-color:var(--accent);box-shadow:0 6px 22px rgba(20,30,40,.08)}
.bi-kaart .bi-fig{border-radius:0}
.bi-kaart-tekst{padding:16px 18px 18px}
.bi-kaart h2,.bi-kaart h3{font-size:1.12rem;margin:0 0 6px}
.bi-kaart p{margin:0 0 10px;font-size:.95rem}
.bi-go{font-weight:700;color:var(--accent-dark,#9a3d14);font-size:.92rem}
.bi-stalen{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin:18px 0}
.bi-staal{display:flex;gap:12px;align-items:flex-start;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:12px}
.bi-staal-vlak{flex:0 0 54px;height:54px;border-radius:8px;border:1px solid rgba(0,0,0,.08);background-size:cover}
.bi-staal h3{font-size:.98rem;margin:0 0 3px}
.bi-staal p{font-size:.88rem;margin:0;line-height:1.45}
.bi-kleuren{display:flex;flex-wrap:wrap;gap:14px;list-style:none;padding:0;margin:14px 0 22px}
.bi-kleuren li{display:flex;flex-direction:column;align-items:center;width:92px;text-align:center;font-size:.8rem;line-height:1.3;margin:0}
.bi-kleuren li::before{display:none}
.bi-dot{width:56px;height:56px;border-radius:50%;border:1px solid rgba(0,0,0,.12);box-shadow:inset 0 -6px 12px rgba(0,0,0,.08);margin-bottom:6px}
.bi-kleuren strong{display:block;font-size:.84rem}
.bi-verder{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:18px 0 8px}
.bi-verder a{display:block;background:#fff;border:1px solid var(--line);border-radius:var(--radius);padding:15px 17px;text-decoration:none;color:inherit}
.bi-verder a:hover,.bi-verder a:focus-visible{border-color:var(--accent)}
.bi-soort{display:block;font-size:.76rem;text-transform:uppercase;letter-spacing:.04em;color:var(--accent-dark,#9a3d14);font-weight:700}
.bi-naam{display:block;font-weight:700;margin:4px 0}
.bi-oms{display:block;font-size:.9rem;color:var(--muted,#5b6470)}
.bi-twee{display:grid;grid-template-columns:1fr 1fr;gap:26px}
.bi-indeling{counter-reset:bi;list-style:none;padding:0}
.bi-indeling li{counter-increment:bi;position:relative;padding-left:40px;margin:0 0 12px}
.bi-indeling li::before{content:counter(bi);position:absolute;left:0;top:0;width:28px;height:28px;border-radius:50%;background:var(--accent-soft,#f6e4da);color:var(--accent-dark,#9a3d14);font-weight:800;display:flex;align-items:center;justify-content:center;font-size:.9rem}
.bi-bronnen{font-size:.88rem}
.bi-andere{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin-top:16px}
.bi-andere a{display:block;text-decoration:none;color:inherit;font-weight:700;font-size:.92rem}
.bi-andere .bi-fig{margin-bottom:6px}
.bi-probeer{background:var(--bg-soft,#f6f4f0);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px;margin:22px 0}
.bi-probeer p{margin:0 0 10px}
@media (max-width:700px){.bi-twee{grid-template-columns:1fr}.bi-galerij{grid-template-columns:1fr}}
</style>"""


def _figuur(slug, sizes, boven_vouw=False, bijschrift=True):
    img = _render_img(slug, sizes, boven_vouw)
    bij = f'<p class="bi-bij">{_esc(RENDERS_STIJL[slug]["bijschrift"])}</p>' if bijschrift else ""
    return (f'<figure class="bi-fig">{img}<figcaption class="bi-label">Illustratie (3D-render)</figcaption></figure>{bij}')


def _bronnen_html():
    return "".join(f'<li><a href="{_esc(u)}" rel="noopener">{_esc(lab)}</a></li>' for lab, u in BRONNEN_KOSTEN)


# ---------------------------------------------------------------------------
# Stijlpagina
# ---------------------------------------------------------------------------

def _stijlpagina(s, write, today):
    url = f"{PAD}{s['slug']}/"
    cr, cr_ld = crumbs([("Home", "/"), ("Inspiratie", PAD), (s["naam"], None)])
    sk = f"/tools/stijlkiezer/{_sk_hash(s['stijl'])}".replace("&", "&amp;")

    kenmerken = "".join(f"<li>{k}</li>" for k in s["kenmerken"])
    stalen = "".join(
        f'<div class="bi-staal"><span class="bi-staal-vlak" style="background:{bg}" aria-hidden="true"></span>'
        f'<div><h3>{n}</h3><p>{t}</p></div></div>' for n, t, bg in s["materialen"])
    kleuren = "".join(
        f'<li><span class="bi-dot" style="background:{hx}" aria-hidden="true"></span><strong>{n}</strong>{waar}</li>'
        for n, hx, waar in s["kleuren"])
    tips = "".join(f"<li>{t}</li>" for t in s["tips"])
    valkuilen = "".join(f"<li>{t}</li>" for t in s["valkuilen"])

    indeling = ""
    if s.get("indeling"):
        li = "".join(f"<li><strong>{t}.</strong> {x}</li>" for t, x in s["indeling"])
        indeling = (f'<h2 id="indeling">De indeling in de illustratie</h2>'
                    f'<p>Zo past alles in ongeveer 1,8 × 2,2 meter, met de deur in de korte wand tegenover de douche:</p>'
                    f'<ol class="bi-indeling">{li}</ol>'
                    f'<p>Meer indelingen, ook met een bad of een toilet apart, lees je in '
                    f'<a href="/kennisbank/kleine-badkamer-indelen/">kleine badkamer indelen</a>.</p>')

    kaarten = [_kaart(sk, "Tool", "Probeer het in de stijlkiezer",
                      f"Zie {s['kort'].lower()} in een getekende badkamer en wissel zelf tegels en kranen.")]
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

    body = f"""{CSS}{cr}
<article class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Inspiratie · badkamerstijl</span>
  <h1>{s['h1']}</h1>
  <p class="lead">{s['intro']}</p>
  <div class="bi-hero">{_figuur(s['slug'], "(max-width: 860px) 100vw, 820px", boven_vouw=True)}</div>

  <h2 id="kenmerken">Kenmerken van een {s['naam'].lower()}</h2>
  <ul class="checklist">{kenmerken}</ul>
  {indeling}

  <h2 id="materialen">Materialen en kleuren</h2>
  <p>Dit zijn de materialen uit de illustratie. Je hoeft ze niet allemaal over te nemen: kies een basis en hooguit één of twee accenten.</p>
  <div class="bi-stalen">{stalen}</div>
  <h3>Kleurenpalet</h3>
  <ul class="bi-kleuren">{kleuren}</ul>
  <p style="font-size:.88rem">De kleurstalen zijn een benadering op een scherm. Bekijk tegels en verf altijd in het echt, bij daglicht en bij het licht in je badkamer.</p>

  <h2 id="kosten">Wat kost een {s['naam'].lower()}?</h2>
  <p>Een stijl zegt weinig over de prijs. De meeste complete badkamers van 5 tot 9 m² kosten <strong>€6.000 tot €18.000</strong>, inclusief sloopwerk, leidingwerk, tegels, sanitair, montage en 21% btw. Je eigen badkamer kan hoger of lager uitkomen; de grootte, het sanitair en of de indeling verandert maken het grootste verschil.</p>
  {balken}
  <p>{s['kosten']}</p>
  <p>Een uitgebreide uitleg met een rekenvoorbeeld staat op de pagina <a href="/kosten/nieuwe-badkamer/">wat kost een nieuwe badkamer</a>. Wil je je eigen badkamer doorrekenen, gebruik dan de <a href="/tools/badkamercalculator/">badkamercalculator</a>.</p>
  <p class="bi-bronnen"><strong>Bronnen voor de richtprijzen</strong> (geraadpleegd november 2026):</p>
  <ul class="bi-bronnen">{_bronnen_html()}</ul>

  {cta_midden(f"Een {s['naam'].lower()} laten maken?", "Vergelijk gratis offertes van maximaal drie badkamerspecialisten uit je regio.")}

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

  <div class="bi-probeer">
    <p><strong>Zelf proberen?</strong> In de stijlkiezer staat {s['kort'].lower()} al klaar. Wissel de wandtegel, de vloer, de kraankleur, het meubel en de douche en zie meteen wat er verandert.</p>
    <a class="btn btn-primary" href="{sk}">Open de stijlkiezer</a>
  </div>

  <h2 id="verder">Verder met je plan</h2>
  <p>Kopersgidsen, uitleg en richtprijzen die bij deze stijl passen:</p>
  <div class="bi-verder">{"".join(kaarten)}</div>

  <h2 id="andere">Andere stijlen</h2>
  <div class="bi-andere">{andere}</div>
  <p style="margin-top:14px"><a href="{PAD}">Alle stijlen naast elkaar</a></p>
</div></article>
{faq_html}
{cta_blok("Klaar voor je nieuwe badkamer?", "Beschrijf je wensen in een minuut en ontvang gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio.")}"""

    img_url = f"{SITE['url']}/assets/fotos/renders/{RENDERS_STIJL[s['slug']]['naam']}-1600.webp"
    art_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": s["h1"], "description": s["description"], "inLanguage": "nl-NL",
        "datePublished": GEPUBLICEERD, "dateModified": today,
        "image": {"@type": "ImageObject", "url": img_url, "width": 1600, "height": 1067,
                  "caption": RENDERS_STIJL[s["slug"]]["bijschrift"]},
        "author": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "publisher": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "mainEntityOfPage": SITE["url"] + url,
        "isPartOf": {"@type": "CollectionPage", "@id": SITE["url"] + PAD},
        "citation": [u for _, u in BRONNEN_KOSTEN],
    }
    write(url, page(title(s["seo"]), s["description"], url, body, [cr_ld, art_ld, faq_ld]), prio=0.7)


# ---------------------------------------------------------------------------
# Overzicht
# ---------------------------------------------------------------------------

def _overzicht(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Inspiratie", None)])
    kaarten = "".join(
        f'<a class="bi-kaart" href="{PAD}{s["slug"]}/">'
        f'<figure class="bi-fig">{_render_img(s["slug"], "(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 380px", boven_vouw=(i < 2))}'
        f'<figcaption class="bi-label">Illustratie (3D-render)</figcaption></figure>'
        f'<div class="bi-kaart-tekst"><h2>{s["naam"]}</h2><p>{s["galerij"]}</p><span class="bi-go">Bekijk de stijl →</span></div></a>'
        for i, s in enumerate(STIJLEN))
    faqs = [
        ("Zijn dit foto's van echte badkamers?", "Nee. Het zijn 3D-illustraties die wij zelf hebben gemaakt om de stijlen te laten zien. Echte badkamers verschillen in maat, licht en details."),
        ("Welke badkamerstijl blijft lang mooi?", "Een rustige basis in neutrale kleuren met wisselbare accenten veroudert het minst snel. Uitgesproken kleuren en materialen zijn meer modegevoelig."),
        ("Kan ik stijlen combineren?", "Ja, bijvoorbeeld industrieel met warm hout of modern met een landelijk accent. Houd één stijl als basis en gebruik de andere als accent."),
        ("Bepaalt de stijl wat mijn badkamer kost?", "Niet zozeer de stijl, wel de keuzes erbinnen: de grootte, het sanitair, de tegelmaat en of de indeling verandert. Op elke stijlpagina lees je welke keuzes het werk duurder maken."),
    ]
    faq_html, faq_ld = faq_blok(faqs)
    body = f"""{CSS}{cr}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose">
    <span class="badge">Inspiratie</span>
    <h1>Badkamer inspiratie: zes stijlen in beeld</h1>
    <p class="lead">Modern, landelijk, industrieel, japandi, klassiek of juist een slimme kleine badkamer. Per stijl zie je een illustratie en lees je de kenmerken, de materialen en kleuren, wat het ongeveer kost en waar je op let.</p>
    <p>De beelden zijn 3D-illustraties die wij zelf hebben gemaakt, geen foto's van echte badkamers. Wij voeren zelf geen werk uit, maar brengen je in contact met maximaal drie badkamerspecialisten uit je regio.</p>
  </div>
  <div class="bi-galerij">{kaarten}</div>
  <div class="narrow prose" style="margin-top:42px">
    <h2>Hoe kies je een stijl?</h2>
    <p>Verzamel voorbeelden van badkamers die je mooi vindt en kijk wat ze gemeen hebben: kleur, materiaal of vorm. Kies daarna één basis en hooguit één of twee accenten. Houd ook rekening met de rest van je huis, met onderhoud en met hoe lang je er wilt blijven wonen.</p>
    <p>Twijfel je nog? Probeer combinaties uit in de <a href="/tools/stijlkiezer/">stijlkiezer</a>, of lees meer over materialen en onderhoud per stijl in <a href="/kennisbank/badkamerstijlen/">badkamerstijlen uitgelegd</a>. Wat een nieuwe badkamer kost, lees je op <a href="/kosten/nieuwe-badkamer/">de kostenpagina</a>.</p>
  </div>
</div></section>
{faq_html}
{cta_blok("Je stijl gevonden?", "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit jouw regio en vergelijk ze naast elkaar.")}"""
    items = [{"@type": "ListItem", "position": i + 1, "url": SITE["url"] + f"{PAD}{s['slug']}/", "name": s["naam"]}
             for i, s in enumerate(STIJLEN)]
    lijst_ld = {"@context": "https://schema.org", "@type": "CollectionPage", "@id": SITE["url"] + PAD,
                "name": "Badkamer inspiratie: zes stijlen in beeld", "inLanguage": "nl-NL",
                "mainEntity": {"@type": "ItemList", "itemListElement": items}}
    write(PAD, page(title("Badkamer inspiratie: zes stijlen in beeld"),
                    "Inspiratie voor je badkamer: modern, landelijk, industrieel, japandi, klassiek en klein. Met illustraties, kenmerken, materialen, kleuren en kosten per stijl.",
                    PAD, body, [cr_ld, lijst_ld, faq_ld]), prio=0.8)


def build(write):
    today = datetime.date.today().isoformat()
    for s in STIJLEN:
        _stijlpagina(s, write, today)
    _overzicht(write)
