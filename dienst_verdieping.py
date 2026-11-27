# -*- coding: utf-8 -*-
"""Verdieping voor de 7 dienstpagina's /diensten/<slug>/.

Per dienst:
- intentie: wat iemand die hierop zoekt meestal wil weten, bovenaan beantwoord;
- stappen: het werk stap voor stap, met een indicatie van de duur (sluit aan op de
  renovatieplanner, badkamer_planner.FASEN);
- posten: kostenposten uit richtprijzen.py (één bron voor alle bedragen);
- keuzes: de keuzes die de prijs en het resultaat het meest bepalen;
- specialist: waar je op let bij het kiezen van een bedrijf;
- faq: extra vragen bovenop data.DIENSTEN[...]["faq"];
- links: interne links die nog niet in build.MEER_WETEN staan.

Regels: geen verzonnen cijfers. Bedragen komen uit richtprijzen.py, duur is een
vuistregel en staat er ook zo.
"""
import html as _html

from components import eur
from richtprijzen import RICHTPRIJZEN, BRONNEN, EENHEID_TEKST

V = {}

V["badkamer-renoveren"] = dict(
    intentie=[
        ("Wat kost het?", f"Een complete badkamer van 5 tot 9 m² in het middensegment kost meestal €6.000 tot €18.000, inclusief sloop, tegels, sanitair, montage en btw."),
        ("Hoe lang duurt het?", "Reken op twee tot vier weken werk in huis. De voorbereiding (ontwerp, bestellen, levertijd) duurt vaak nog eens drie tot zes weken."),
        ("Wie heb je nodig?", "Eén badkamerspecialist die sloop, leidingwerk, tegelwerk en sanitair regelt. Dan heb je één aanspreekpunt en één garantie."),
    ],
    stappen=[
        ("Ontwerp en bestellen", "3 tot 6 weken vooraf", "Indeling en materialen vastleggen. Laat sanitair en tegels leveren vóór de sloopdag, anders staat de klus later stil."),
        ("Slopen en afvoeren", "1 tot 2 dagen", "Tegels, sanitair en vaak de dekvloer eruit. Bij een huis van vóór 1994 eerst laten checken op asbest."),
        ("Leidingwerk en elektra", "2 tot 3 dagen", "Nieuwe water- en afvoerleidingen, aansluitpunten op de juiste hoogte en de elektra voor licht, ventilatie en eventueel vloerverwarming."),
        ("Dekvloer en drogen", "1 dag storten, daarna 3 dagen tot 5 weken drogen", "Een sneldrogende vloer kan na een paar dagen betegeld worden. Zandcement droogt ongeveer een week per centimeter."),
        ("Waterdicht maken", "1 tot 2 dagen", "Afdichting op vloer en wanden in de natte zone, met band in de hoeken en rond doorvoeren."),
        ("Tegelen, voegen en kitten", "5 tot 8 dagen", "Een tegelzetter haalt ongeveer 8 tot 10 m² per dag. Grote tegels en natuursteen gaan langzamer."),
        ("Sanitair en oplevering", "2 tot 4 dagen", "Douche, toilet, meubel en kranen monteren, een lektest doen en samen een opleverlijst maken."),
    ],
    posten=[("sloop", "Slopen"), ("afval", "Puin en afval afvoeren"), ("leidingwerk", "Leidingwerk (water en afvoer)"),
            ("elektra", "Elektra"), ("waterdicht", "Waterdicht maken"), ("tegelwerk", "Tegelwerk (arbeid)"),
            ("tegels", "Tegels (materiaal)"), ("sanitair", "Sanitair (compleet pakket)"), ("ventilator", "Mechanische ventilator"),
            ("vloerverwarming", "Vloerverwarming")],
    keuzes=[
        ("Indeling", "Alles op dezelfde plek laten", "Toilet, douche of afvoer verplaatsen kost al snel €1.000 tot €2.500 extra aan leidingwerk."),
        ("Bad of douche", "Alleen een douche", "Een bad kost ruimte en geld voor bad, montage en extra tegelwerk. In een kleine badkamer geeft een inloopdouche vaak meer ruimte."),
        ("Toilet", "Staand toilet", "Een hangtoilet vraagt een inbouwreservoir en een voorzetwand. Strak en makkelijk schoon te maken, maar duurder."),
        ("Tegels", "Middenformaat, keramisch", "Grote formaten en natuursteen kosten meer per m² én meer werk. Ze vragen ook een vlakkere ondergrond."),
        ("Verwarming", "Radiator", "Vloerverwarming is comfortabel, maar kost €500 tot €2.500 extra. Een handdoekradiator blijft vaak nodig."),
    ],
    specialist=[
        "Doet het bedrijf de hele klus zelf, of werkt het met vaste onderaannemers voor tegelwerk en leidingwerk? Vraag wie er op welke dag komt.",
        "Vraag welk systeem ze gebruiken om waterdicht te maken, en of de garantie daar ook op geldt.",
        "Laat een tekening of ontwerp maken met de plek van alle aansluitpunten, voordat er gesloopt wordt.",
        "Vraag een planning per dag, met de dagen waarop je geen douche of toilet hebt.",
        "Check de inschrijving bij de KvK en vraag of er een aansprakelijkheidsverzekering is.",
        "Vraag hoe meerwerk wordt afgesproken: vooraf, schriftelijk en met een prijs.",
    ],
    faq=[
        ("Wat zit er bijna nooit in een lage offerte?", "Vaak ontbreken afvoer van puin, het verleggen van leidingen, elektra en een realistische stelpost voor sanitair. Vraag om een prijs per onderdeel, dan zie je direct wat er mist."),
        ("Moet de dekvloer er altijd uit?", "Nee. Als de vloer vlak en droog is en het afschot goed kan worden gemaakt, kan de oude vloer blijven. Bij een inloopdouche zonder drempel of nieuwe afvoeren moet hij er vaak wel uit."),
        ("Hoe vaak moet een badkamer vernieuwd worden?", "Een badkamer gaat meestal twintig tot vijfentwintig jaar mee. Lekkende voegen, losse tegels of een afvoer die steeds verstopt zijn signalen dat het tijd wordt."),
        ("Kan ik een deel zelf doen om te besparen?", "Slopen of schilderen kan vaak, maar spreek het vooraf af. Werk aan leidingen, afdichting en elektra laat je beter aan de specialist, ook vanwege de garantie."),
        ("Wanneer moet ik de VvE inlichten?", "Woon je in een appartement, overleg dan vóór je offertes vraagt. Leidingen, afvoeren en de vloer zijn vaak gemeenschappelijk, en de VvE kan regels hebben over geluid en werktijden."),
    ],
    links=[("/tools/renovatieplanner/", "Renovatieplanner: hoe lang duurt jouw verbouwing?"),
           ("/tools/indelingsplanner/", "Indelingsplanner"),
           ("/kosten/badkamer-slopen/", "Wat kost badkamer slopen?"),
           ("/kosten/vloerverwarming-badkamer/", "Wat kost vloerverwarming in de badkamer?"),
           ("/kennisbank/badkamer-waterdicht-maken/", "Een badkamer waterdicht maken")],
)

V["badkamer-installeren"] = dict(
    intentie=[
        ("Wat kost het?", "Een installateur rekent meestal €45 tot €85 per uur exclusief btw, plus voorrijkosten. Veel kleine klussen gaan voor een vaste prijs."),
        ("Hoe lang duurt het?", "Een kraan of wastafel is vaak binnen een paar uur klaar. Een staand toilet in een halve dag, een hangtoilet met voorzetwand in één tot drie dagen."),
        ("Wie heb je nodig?", "Een loodgieter of installateur. Moet er ook tegelwerk open en dicht, vraag dan of hij dat zelf doet of een tegelzetter meeneemt."),
    ],
    stappen=[
        ("Foto's en opname", "15 minuten tot een uur", "Bij kleine klussen zijn foto's van de aansluitingen vaak genoeg. Bij een hangtoilet of een nieuwe douche komt de installateur kijken."),
        ("Water afsluiten en demonteren", "1 tot 2 uur", "Het oude sanitair eruit. De installateur kijkt meteen naar de staat van stopkranen, leidingen en afvoer."),
        ("Aansluitingen aanpassen", "0 tot 1 dag", "Alleen nodig als het nieuwe sanitair andere aansluitpunten heeft. Bij een hangtoilet komt hier een inbouwreservoir en een voorzetwand bij."),
        ("Plaatsen en aansluiten", "1 uur tot een halve dag per onderdeel", "Waterpas zetten, aansluiten op water en afvoer en vastzetten."),
        ("Testen en afkitten", "1 tot 2 uur", "Water erop, alles nalopen op lekkage en de kitnaden zetten. Kit moet ongeveer een dag uitharden."),
    ],
    posten=[("uurtarief", "Uurtarief loodgieter of installateur"), ("voorrijkosten", "Voorrijkosten"),
            ("montage_toilet", "Toilet plaatsen (werk)"), ("montage_meubel", "Wastafelmeubel plaatsen (werk)"),
            ("montage_douche", "Douche plaatsen (werk)"), ("montage_bad", "Bad plaatsen (werk)"),
            ("sanitair_toilet", "Toilet (materiaal)"), ("sanitair_meubel", "Wastafelmeubel (materiaal)")],
    keuzes=[
        ("Prijsafspraak", "Vaste prijs per klus", "Bij een uurtarief draag jij het risico als het tegenvalt. Vraag dan altijd een schatting van het aantal uren."),
        ("Wie levert", "De installateur levert", "Zelf kopen kan goedkoper lijken, maar dan is er soms geen garantie op het onderdeel en loop je risico met verkeerde maten."),
        ("Toilet", "Staand op dezelfde plek", "Een hangtoilet of een andere plek betekent breekwerk en nieuw tegelwerk op die wand."),
        ("Kraan", "Opbouwkraan", "Een inbouwkraan vraagt een inbouwdeel in de muur en dus hak- en tegelwerk."),
        ("Klussen bundelen", "Alles in één bezoek", "Een toilet, kraan en sifon tegelijk scheelt voorrijkosten en een tweede afspraak."),
    ],
    specialist=[
        "Vraag of de prijs per klus is of per uur, en of voorrijkosten en klein materiaal erbij zitten.",
        "Stuur foto's van de aansluitingen mee. Dan kan de installateur zien of er iets verlegd moet worden.",
        "Vraag of hij tegelwerk zelf herstelt of dat je daarvoor iemand anders nodig hebt.",
        "Vraag wat de garantie is op het werk en op het sanitair, ook als jij het sanitair koopt.",
        "Laat de installateur na afloop een lektest doen terwijl jij erbij bent.",
    ],
    faq=[
        ("Wat is het verschil tussen een loodgieter en een installateur?", "In de praktijk doen ze vaak hetzelfde werk aan water en afvoer. Een installateur doet daarnaast vaak ook cv en ventilatie. Voor sanitair plaatsen zijn ze allebei geschikt."),
        ("Kan een kraan vervangen in een uur?", "Een gewone opbouwkraan vaak wel, als de aansluitingen passen. Een thermostaatkraan met andere hartafstand of een inbouwkraan kost meer tijd."),
        ("Hoe weet ik of mijn toilet op de oude plek past?", "Meet de afstand van de muur tot het midden van de afvoer en kijk of de afvoer in de vloer of in de muur zit. Geef die maten door, dan weet de installateur welk toilet past."),
        ("Moet de waterleiding eraf bij een nieuwe kraan?", "Meestal is het genoeg om de stopkraantjes onder de wastafel dicht te draaien. Zijn die er niet of zitten ze vast, dan gaat de hoofdkraan dicht."),
    ],
    links=[("/kosten/kraan-vervangen/", "Wat kost een kraan vervangen?"),
           ("/kosten/wastafel-vervangen/", "Wat kost een wastafel vervangen?"),
           ("/kosten/badkamermeubel-plaatsen/", "Wat kost een badkamermeubel plaatsen?"),
           ("/badkamerspullen/inbouwreservoir-kiezen/", "Een inbouwreservoir kiezen"),
           ("/kennisbank/hangtoilet-of-staand-toilet/", "Hangtoilet of staand toilet?")],
)

V["tegelwerk-badkamer"] = dict(
    intentie=[
        ("Wat kost het?", "Een tegelzetter rekent meestal €25 tot €55 per m² voor het zetten. Tegels kosten daarnaast €20 tot €60 per m², en lijm en voegmiddel ongeveer €10 per m²."),
        ("Hoe lang duurt het?", "Een tegelzetter haalt ongeveer 8 tot 10 m² per dag. Een gemiddelde badkamer met zo'n 25 m² wand en vloer kost dus drie tot vijf dagen, plus voegen."),
        ("Wie heb je nodig?", "Een tegelzetter, en als het om een douchezone gaat ook iemand die de ondergrond waterdicht maakt. Vaak is dat dezelfde vakman."),
    ],
    stappen=[
        ("Oude tegels eruit", "1 tot 2 dagen", "Hakken en afvoeren. Soms kan er over oude tegels heen getegeld worden, maar alleen als die goed vastzitten en de hoogte het toelaat."),
        ("Ondergrond vlak maken", "1 tot 2 dagen", "Wanden uitvlakken of voorzien van plaatmateriaal. Grote tegels vragen een heel vlakke ondergrond."),
        ("Waterdicht maken", "1 dag, plus droogtijd", "In de douchezone een afdichting op vloer en wanden, met band in de hoeken."),
        ("Tegels zetten", "3 tot 5 dagen", "Eerst het legplan afspreken: waar beginnen de tegels en waar komen de snijranden."),
        ("Voegen en kitten", "1 tot 2 dagen", "Voegen als de lijm droog is. Kit komt in de hoeken en langs het sanitair, niet in gewone voegen."),
    ],
    posten=[("tegelwerk", "Tegelwerk (arbeid)"), ("tegels", "Tegels (materiaal)"),
            ("tegelwerk_hulpmateriaal", "Lijm, voegmiddel en hulpmateriaal"), ("sloop_m2", "Oude tegels verwijderen"),
            ("waterdicht", "Waterdicht maken")],
    keuzes=[
        ("Tegelformaat", "30x60 of 60x60 cm", "Formaten van 120 cm en meer kosten meer arbeid en vragen een vlakkere ondergrond. Heel kleine mozaïek kost juist veel voegwerk."),
        ("Materiaal", "Keramisch", "Natuursteen is mooier maar duurder, zwaarder en vraagt meer onderhoud."),
        ("Hoogte", "Wanden tot het plafond", "Halfhoog tegelen is goedkoper, maar dan moet de rest vochtbestendig worden afgewerkt."),
        ("Legpatroon", "Recht", "Halfsteens, visgraat of diagonaal kost meer tijd en meer snijverlies."),
        ("Voeg", "Cementvoeg", "Een epoxyvoeg is vuil- en waterafstotend, maar duurder en lastiger te verwerken."),
    ],
    specialist=[
        "Vraag naar foto's van eerder werk met hetzelfde tegelformaat dat jij wilt.",
        "Spreek het legplan vooraf af: waar begint de eerste tegel en waar komen de snijranden.",
        "Vraag of de prijs per m² ook het voorbereiden van de ondergrond en het waterdicht maken omvat.",
        "Vraag hoeveel extra tegels je moet bestellen voor snijverlies. Bij een recht patroon is dat vaak rond de 10%.",
        "Check of de tegelzetter ook kitwerk doet, of dat dat apart moet.",
    ],
    faq=[
        ("Kan ik over oude tegels heen tegelen?", "Soms wel, als de oude tegels vlak zijn en goed vastzitten. Maar de vloer wordt hoger en de deur en de afvoer moeten daar wel op passen. In de douche raden de meeste vakmensen het af."),
        ("Hoeveel tegels moet ik bestellen?", "Reken de m² van wanden en vloer uit en tel daar ongeveer 10% bij op voor snijverlies. Bij visgraat of diagonaal is dat meer. Bestel alles uit één productiepartij, dan is de kleur gelijk."),
        ("Hoe lang moet ik wachten met douchen na het tegelen?", "Voegen en kit moeten uitharden. Houd minstens 24 uur aan, en volg de tijd die op het voegmiddel staat."),
        ("Waarom kost een vloer per m² soms meer dan een wand?", "Op de vloer moet afschot naar de afvoer komen, en rond een douchegoot of putje is veel snijwerk. Dat kost tijd."),
    ],
    links=[("/kennisbank/grote-tegels-badkamer/", "Grote tegels in de badkamer"),
           ("/kennisbank/badkamer-kitten/", "Een badkamer kitten"),
           ("/kennisbank/badkamer-zonder-tegels/", "Een badkamer zonder tegels"),
           ("/kennisbank/microcement-badkamer/", "Microcement in de badkamer"),
           ("/tools/badkamercalculator/", "Badkamercalculator")],
)

V["inloopdouche-plaatsen"] = dict(
    intentie=[
        ("Wat kost het?", "Een inloopdouche met plaatsing kost meestal €1.500 tot €5.000. Komt er een douchegoot of moet de afvoer worden verlegd, dan zit je eerder aan de bovenkant."),
        ("Hoe lang duurt het?", "Als het bad of de douchebak eruit gaat en de afvoer blijft, reken op drie tot zes werkdagen. Met een nieuwe vloer en droogtijd duurt het langer."),
        ("Wie heb je nodig?", "Een badkamerspecialist die leidingwerk, afdichting en tegelwerk combineert. Een inloopdouche zonder drempel valt of staat met het afschot en de afdichting."),
    ],
    stappen=[
        ("Afvoer en vloer bekijken", "Bij de opname", "Waar zit de afvoer en hoe hoog is de vloer? Dat bepaalt of een drempelloze douche kan en of er een goot of een putje komt."),
        ("Slopen", "1 dag", "Douchebak of bad eruit, tegels in de douchezone eraf."),
        ("Afvoer en leidingen", "1 tot 2 dagen", "Afvoer verleggen of een douchegoot plaatsen, en de leidingen voor een inbouw- of opbouwkraan."),
        ("Afschot en waterdicht maken", "1 tot 2 dagen, plus droogtijd", "De vloer krijgt een helling naar de afvoer. Daarna komt een afdichting op vloer en wanden."),
        ("Tegelen", "2 tot 3 dagen", "Vloer en wanden van de douchezone. Rond de goot is precies snijwerk nodig."),
        ("Glaswand en kraan", "Halve tot hele dag", "De glazen wand plaatsen, de douchekraan monteren en alles testen."),
    ],
    posten=[("sanitair_douche", "Douche, wand en kraan (materiaal)"), ("montage_douche", "Douche plaatsen (werk)"),
            ("waterdicht", "Waterdicht maken"), ("tegelwerk", "Tegelwerk (arbeid)"),
            ("leidingwerk_verplaatsen", "Afvoer en leidingen verplaatsen")],
    keuzes=[
        ("Afvoer", "Douchegoot langs de wand", "Een goot geeft afschot in één richting, zodat je grote tegels kunt gebruiken. Een putje in het midden is goedkoper maar vraagt afschot in vier richtingen."),
        ("Drempel", "Drempelloos", "Kan alleen als er genoeg hoogte is voor afschot. Anders komt er een lage opstaande rand of een verhoogde vloer."),
        ("Glaswand", "Vaste wand van 8 mm", "Een tweede wand of een draaideur houdt water beter binnen, maar kost meer."),
        ("Kraan", "Opbouw-thermostaatkraan", "Een inbouwkraan met regendouche oogt strakker, maar vraagt hak- en tegelwerk in de muur."),
        ("Vloer", "Tegels", "Een kant-en-klare douchevloer of microcement kan ook. Vraag naar de garantie en het onderhoud."),
    ],
    specialist=[
        "Vraag hoe het afschot wordt gemaakt en hoeveel hoogte daarvoor nodig is.",
        "Vraag welk afdichtsysteem wordt gebruikt en of de goot of het putje daarbij past.",
        "Vraag of de vloer buiten de douche ook nieuw moet, zodat alles op één hoogte ligt.",
        "Laat de plek van de kraan en de glaswand op tekening zetten, zodat het water in de douche blijft.",
        "Vraag of er een drempelloze oplossing mogelijk is bij jouw vloer, en wat het kost als dat niet kan.",
    ],
    faq=[
        ("Hoe groot moet een inloopdouche zijn?", "Ga uit van minimaal 90 bij 120 cm, dan blijft het water redelijk binnen. Met een open zijde zonder deur is meer ruimte prettig, bijvoorbeeld 100 bij 140 cm."),
        ("Kan een inloopdouche in een appartement?", "Vaak wel, maar de vloer is daar meestal beton en de afvoer loopt door het gebouw. Drempelloos is dan soms lastig. Overleg ook met de VvE."),
        ("Spat het water niet de badkamer in?", "Bij een te kleine douche of een korte wand wel. Een langere wand, een tweede wand of een draaibaar zijpaneel helpt. Ook de plek van de douchekop maakt verschil."),
        ("Wat is beter: goot of putje?", "Een goot laat je grote tegels leggen en is makkelijk schoon te houden. Een putje is goedkoper en werkt ook goed in een kleine douche."),
    ],
    links=[("/kosten/bad-vervangen-door-douche/", "Wat kost een bad vervangen door een douche?"),
           ("/kosten/douche-vervangen/", "Wat kost een douche vervangen?"),
           ("/badkamerspullen/douchegoot-kiezen/", "Een douchegoot kiezen"),
           ("/badkamerspullen/douchewand-kiezen/", "Een douchewand kiezen"),
           ("/kennisbank/regendouche/", "Een regendouche")],
)

V["toilet-renoveren"] = dict(
    intentie=[
        ("Wat kost het?", "Een complete toiletrenovatie kost meestal €2.500 tot €6.500. Alleen een toilet vervangen kan voor €300 tot €700 aan werk, het toilet zelf niet meegerekend."),
        ("Hoe lang duurt het?", "Een complete toiletruimte duurt vaak vijf tot tien werkdagen. Heb je één toilet in huis, vraag dan hoeveel dagen het buiten gebruik is."),
        ("Wie heb je nodig?", "Een badkamerspecialist of installateur die ook tegelt. Voor alleen een nieuwe pot is een loodgieter genoeg."),
    ],
    stappen=[
        ("Opname en keuzes", "1 tot 3 weken vooraf", "Staand of hangend toilet, een fontein, tegels en verlichting kiezen en bestellen."),
        ("Slopen", "Halve tot hele dag", "Toilet, fontein en tegels eruit. Let bij oudere woningen op asbest in kit of vloerbedekking."),
        ("Leidingwerk en inbouwreservoir", "1 dag", "Afvoer en water op de goede plek, bij een hangtoilet ook het inbouwreservoir in een voorzetwand."),
        ("Tegelen en voegen", "2 tot 3 dagen", "Vloer en wanden, vaak tot halverwege of tot het plafond."),
        ("Toilet en fontein monteren", "Halve tot hele dag", "Pot, fontein en kraan monteren, testen op lekkage en afkitten."),
    ],
    posten=[("montage_toilet", "Toilet plaatsen (werk)"), ("sanitair_toilet", "Toilet (materiaal)"),
            ("leidingwerk_toilet_verplaatsen", "Toilet verplaatsen"), ("tegelwerk", "Tegelwerk (arbeid)"),
            ("ventilator", "Mechanische ventilator")],
    keuzes=[
        ("Toilet", "Staand toilet", "Een hangtoilet is makkelijker schoon te houden, maar vraagt een inbouwreservoir en een voorzetwand."),
        ("Fontein", "Klein fonteintje", "Een fontein met kast of een groter wasbakje kost meer, maar geeft opbergruimte."),
        ("Plek", "Toilet op dezelfde plek", "Verplaatsen kost al snel €700 tot €1.500 extra voor afvoer en leidingen."),
        ("Tegels", "Tot halverwege de wand", "Tot het plafond tegelen kost meer m², maar je hebt geen schilderwerk meer."),
        ("Ventilatie", "Bestaande afzuiging", "Is er geen ventilatie, neem een ventilator mee in de offerte. Dat voorkomt vocht en geur."),
    ],
    specialist=[
        "Vraag hoe lang je zonder toilet zit en of er een tijdelijke oplossing is.",
        "Vraag welk inbouwreservoir wordt gebruikt en of onderdelen daarvan later nog te krijgen zijn.",
        "Vraag of de afvoer wordt vernieuwd of alleen aangesloten.",
        "Laat de plek van het fonteintje en de kraan op tekening zetten.",
        "Vraag of tegelwerk, kitwerk en afwerking van het plafond in de prijs zitten.",
    ],
    faq=[
        ("Is een hangtoilet beter dan een staand toilet?", "Een hangtoilet is makkelijk schoon te maken, omdat de vloer eronder vrij is. Een staand toilet is goedkoper en sneller te vervangen. Allebei werken ze goed."),
        ("Kan het toilet naar een andere plek?", "Dat kan, maar de afvoer moet dan mee. Met een gewone afvoer moet er genoeg afschot zijn. Kan dat niet, dan is soms een vermaler nodig."),
        ("Hoe lang gaat een inbouwreservoir mee?", "Een goed inbouwreservoir gaat lang mee. De onderdelen die slijten, zoals de vlotter en de spoelklep, zijn bij de bekende merken meestal los te vervangen via het bedieningspaneel."),
        ("Heb ik een raam of een ventilator nodig?", "Een toilet moet geventileerd worden. Is er geen raam, dan is mechanische afzuiging het meest gebruikelijk."),
    ],
    links=[("/kosten/toilet-verplaatsen/", "Wat kost een toilet verplaatsen?"),
           ("/badkamerspullen/fontein-kiezen/", "Een fontein kiezen"),
           ("/badkamerspullen/inbouwreservoir-kiezen/", "Een inbouwreservoir kiezen"),
           ("/kennisbank/hangtoilet-of-staand-toilet/", "Hangtoilet of staand toilet?"),
           ("/inspiratie/", "Inspiratie voor badkamer en toilet")],
)

V["badkamer-onderhoud"] = dict(
    intentie=[
        ("Wat kost het?", "Kit vervangen kost meestal €6 tot €11 per meter, vaak met een starttarief. Een hele badkamer opnieuw afkitten kost zo'n €95 tot €325."),
        ("Hoe lang duurt het?", "Opnieuw kitten is meestal binnen een paar uur klaar. Daarna moet de kit ongeveer 24 uur uitharden voordat je weer doucht."),
        ("Wie heb je nodig?", "Een kitter of badkamerspecialist. Bij lekkage achter de tegels eerst iemand die de oorzaak zoekt, anders blijf je kitten."),
    ],
    stappen=[
        ("Oorzaak zoeken", "15 minuten tot een uur", "Is het alleen de kit, of lekt er iets achter de tegels? Vlekken op het plafond eronder wijzen vaak op een lek."),
        ("Oude kit verwijderen", "1 tot 2 uur", "Alle oude kit moet eruit, ook de resten. Nieuwe kit op oude kit hecht slecht."),
        ("Schoonmaken en ontvetten", "Half uur", "Schimmel en zeepresten verwijderen. De naad moet helemaal droog zijn."),
        ("Nieuwe kit zetten", "1 tot 2 uur", "Sanitairkit met schimmelwerend middel, strak afgewerkt."),
        ("Uitharden", "Ongeveer 24 uur", "Niet douchen tot de kit uitgehard is. Lees de tijd op de koker."),
    ],
    posten=[("kitwerk", "Kitwerk per meter"), ("kitwerk_badkamer", "Hele badkamer afkitten"),
            ("uurtarief", "Uurtarief bij lekkage of herstel"), ("voorrijkosten", "Voorrijkosten"), ("ventilator", "Ventilator vervangen")],
    keuzes=[
        ("Kit of voegen", "Alleen kit vervangen", "Zijn de voegen zelf poreus of zitten er scheuren in, dan helpt alleen kitten niet. Voegen vernieuwen kost meer tijd."),
        ("Doe-het-zelf of vakman", "Vakman bij de douche", "Zelf kitten kan, maar oude kit goed verwijderen is het meeste werk. In de douche loont een strakke, goed hechtende naad."),
        ("Schimmel", "Kit vervangen", "Schimmel in kit gaat er niet meer uit. Zonder betere ventilatie komt hij wel terug."),
        ("Kitsoort", "Sanitairkit (siliconen)", "Gebruik geen acrylaatkit in natte zones. Die is niet geschikt voor water."),
    ],
    specialist=[
        "Vraag of alle oude kit eruit gaat, en niet alleen de zichtbare laag.",
        "Vraag welke kit wordt gebruikt en of die schimmelwerend is.",
        "Laat bij vlekken op het plafond eerst de oorzaak zoeken voordat er gekit wordt.",
        "Vraag of voegen worden gecontroleerd op scheuren en losse tegels.",
        "Vraag een vaste prijs, inclusief starttarief en voorrijkosten.",
    ],
    faq=[
        ("Hoe vaak moet kit vervangen worden?", "Dat hangt af van gebruik en ventilatie. Als de kit loslaat, scheurt of zwart wordt van schimmel, is het tijd. Wacht niet tot er water achter loopt."),
        ("Waarom komt schimmel steeds terug?", "Meestal is het te vochtig. Laat de ventilator lang genoeg draaien, zet na het douchen een raam open en trek de wanden droog."),
        ("Is een lek altijd de kit?", "Nee. Ook een lekkende afvoer, een slechte afdichting onder de tegels of een kapotte leiding kan de oorzaak zijn. Daarom eerst zoeken, dan herstellen."),
        ("Kan ik voegen opnieuw laten doen zonder nieuwe tegels?", "Ja. De oude voeg wordt eruit gefreesd en er komt nieuwe voeg in. Dat is een goede optie als de tegels nog goed vastzitten."),
    ],
    links=[("/kennisbank/badkamer-kitten/", "Een badkamer kitten"),
           ("/kennisbank/badkamer-schoonmaken/", "Een badkamer schoonmaken"),
           ("/kosten/badkamer-ventilatie/", "Wat kost ventilatie in de badkamer?"),
           ("/kosten/badkamer-opknappen/", "Wat kost een badkamer opknappen?")],
)

V["zakelijk-badkamers"] = dict(
    intentie=[
        ("Wat kost het?", "Zakelijk werk wordt meestal per project geprijsd. Als richtlijn: €45 tot €85 per uur exclusief btw, en per badkamer de bedragen van een gewone renovatie, met korting bij herhaling."),
        ("Hoe lang duurt het?", "Per badkamer vaak één tot drie weken. Bij een complex wordt in series gewerkt, zodat bewoners zo kort mogelijk zonder douche zitten."),
        ("Wie heb je nodig?", "Een badkamerbedrijf dat projecten aankan: genoeg mensen, een vaste planning en heldere afspraken met bewoners en beheerder."),
    ],
    stappen=[
        ("Inventarisatie", "1 tot 4 weken", "Alle badkamers in kaart brengen: maat, staat, leidingen en of er asbest kan zitten."),
        ("Proefbadkamer", "1 tot 3 weken", "Eén badkamer als voorbeeld uitvoeren. Zo zie je de echte tijd, de kosten en de kwaliteit."),
        ("Planning en bewoners", "2 tot 6 weken vooraf", "Een planning per woning, met een brief aan de bewoners over overlast en dagen zonder douche."),
        ("Uitvoering in series", "Afhankelijk van het aantal woningen", "Ploegen werken achter elkaar: slopen, leidingwerk, tegelen, sanitair."),
        ("Oplevering per woning", "Halve dag per woning", "Samen met beheerder of bewoner nalopen en een opleverlijst maken."),
    ],
    posten=[("uurtarief", "Uurtarief installateur"), ("sanitair", "Sanitair per badkamer"),
            ("tegelwerk", "Tegelwerk (arbeid)"), ("leidingwerk", "Leidingwerk per badkamer"),
            ("kitwerk_badkamer", "Afkitten per badkamer (onderhoud)")],
    keuzes=[
        ("Aanpak", "Per complex in één keer", "Losse badkamers bij mutatie vervangen spreidt de kosten, maar kost per stuk meer."),
        ("Sanitair", "Eén standaardpakket", "Eén type sanitair voor alle woningen maakt onderhoud en reserveonderdelen eenvoudiger."),
        ("Proef", "Eerst een proefbadkamer", "Kost een paar weken, maar voorkomt fouten die je anders tientallen keren maakt."),
        ("Bewoners", "Keuze uit twee of drie tegelkleuren", "Meer keuze is fijn voor bewoners, maar maakt de planning en inkoop lastiger."),
    ],
    specialist=[
        "Vraag naar ervaring met projecten van vergelijkbare omvang, en of je een referentie mag bellen.",
        "Vraag hoeveel badkamers per week ze aankunnen, en met hoeveel eigen mensen.",
        "Vraag hoe ze met bewoners communiceren en wie het aanspreekpunt is tijdens de uitvoering.",
        "Laat een vaste prijs per badkamer afspreken, met een duidelijke regeling voor meerwerk.",
        "Vraag hoe ze omgaan met asbest in woningen van vóór 1994.",
        "Check KvK-inschrijving en een aansprakelijkheidsverzekering die past bij projectwerk.",
    ],
    faq=[
        ("Wie beslist bij een VvE over nieuwe badkamers?", "De badkamer in een appartement is meestal van de eigenaar zelf. Leidingen en afvoeren die door het gebouw lopen, vallen vaak onder de VvE. Kijk in de splitsingsakte wat van wie is."),
        ("Kan een verhuurder de badkamer vervangen terwijl de huurder er woont?", "Ja, maar het is een renovatie waarover de verhuurder vooraf afspraken maakt met de huurder, over overlast en de planning. Een redelijk voorstel en goede communicatie zijn belangrijk."),
        ("Is een vaste prijs per badkamer mogelijk?", "Ja, zeker na een proefbadkamer. Spreek dan ook af wat er gebeurt als er bij het slopen iets onverwachts gevonden wordt."),
        ("Welk btw-tarief geldt zakelijk?", "Voor badkamerwerk geldt 21% btw. Een ondernemer of verhuurder kan de btw soms terugvragen; dat hangt af van de eigen btw-positie."),
    ],
    links=[("/voor-badkamerspecialisten/", "Voor badkamerspecialisten"),
           ("/kennisbank/badkamer-huurwoning/", "De badkamer in een huurwoning"),
           ("/kennisbank/asbest-in-badkamer/", "Asbest in de badkamer"),
           ("/tools/renovatieplanner/", "Renovatieplanner")],
)


def _post_rij(sleutel, label):
    p = RICHTPRIJZEN[sleutel]
    eenheid = EENHEID_TEKST[p["eenheid"]]
    if sleutel == "sanitair" and p["eenheid"] == "post":
        eenheid = "per badkamer"
    btw = "incl. btw" if p["btw"] == "incl" else "excl. btw"
    bronnen = [BRONNEN[b] for b in p["bron"] if b != "eigen" and BRONNEN[b][1]]
    bron = ", ".join(f'<a href="{u}" rel="nofollow noopener">{_html.escape(n.split(",")[0])}</a>' for n, u in bronnen[:2]) or "eigen inschatting"
    return (f'<tr><td>{label}<br><small>{_html.escape(p["toelichting"])}</small></td>'
            f'<td class="num">{eur(p["laag"])} – {eur(p["hoog"])}</td><td>{eenheid}, {btw}</td><td><small>{bron}</small></td></tr>')


def intentie_blok(d):
    """Antwoord-eerst-blok voor bovenaan de dienstpagina."""
    v = V.get(d["slug"])
    if not v:
        return ""
    li = "".join(f"<li><strong>{k}</strong> {t}</li>" for k, t in v["intentie"])
    return f'<div class="callout"><p><strong>In het kort</strong></p><ul>{li}</ul></div>'


def stappen_met_duur(d):
    """Stappen met duur als tijdlijn; valt terug op data.DIENSTEN[...]['werkwijze']."""
    from components import stappen_blok
    v = V.get(d["slug"])
    if not v:
        return stappen_blok(d["werkwijze"])
    st = [(f'{t} <small style="font-weight:400">· {duur}</small>', tekst) for t, duur, tekst in v["stappen"]]
    return (stappen_blok(st)
            + '<p><small>De duur is een vuistregel voor een gemiddelde klus. Droogtijden en levertijden kunnen het langer maken. '
              'Maak je eigen planning met de <a href="/tools/renovatieplanner/">renovatieplanner</a>.</small></p>')


def verdieping(d):
    """Extra sectie: kosten per post, keuzes, de specialist kiezen en verder lezen."""
    v = V.get(d["slug"])
    if not v:
        return ""
    rijen = "".join(_post_rij(k, l) for k, l in v["posten"] if k in RICHTPRIJZEN)
    keuzes = "".join(f"<tr><td><strong>{k}</strong></td><td>{a}</td><td>{e}</td></tr>" for k, a, e in v["keuzes"])
    spec = "".join(f"<li>{x}</li>" for x in v["specialist"])
    links = "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in v["links"])
    naam = d["naam"].lower()
    return f"""<section class="section"><div class="wrap narrow prose reveal">
  <h2>Wat kost {naam} per onderdeel?</h2>
  <p>De totaalprijs bovenaan is een bandbreedte. Hieronder zie je de losse posten die in een offerte voor {naam} kunnen staan, met de bron van elk bedrag. Zo kun je een offerte regel voor regel naast deze bedragen leggen.</p>
  <div class="tablewrap"><table>
  <thead><tr><th>Post</th><th>Richtprijs</th><th>Eenheid</th><th>Bron</th></tr></thead>
  <tbody>{rijen}</tbody></table></div>
  <p><small>Bedragen uit onze richtprijzen, gecontroleerd in november 2026. Niet elke post komt in elke klus voor.</small></p>

  <h2>De keuzes die het verschil maken</h2>
  <p>De meeste prijsverschillen ontstaan door een paar keuzes. Per keuze zie je de voordeligste optie en wat het betekent als je iets anders kiest.</p>
  <div class="tablewrap"><table>
  <thead><tr><th>Keuze</th><th>Voordeligste optie</th><th>Wat het verschil maakt</th></tr></thead>
  <tbody>{keuzes}</tbody></table></div>

  <h2>Waar let je op bij een specialist?</h2>
  <ul class="checklist">{spec}</ul>

  <h2>Verder lezen</h2>
  <ul>{links}</ul>
</div></section>"""


def extra_faq(d):
    v = V.get(d["slug"])
    return list(v["faq"]) if v else []
