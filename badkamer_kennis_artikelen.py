# -*- coding: utf-8 -*-
"""Inhoud van de kennisbank (/kennisbank/{slug}/). De opbouw staat in badkamer_kennis.py.

Per artikel: titels, intro, kort antwoord, secties (id, h2, html), stappen of checklist,
FAQ, bronnen en de links naar dienst, kosten en tool.

Feitencontrole (november 2026, met WebSearch):
- Asbest: gebruiksverbod sinds 1 juli 1993; gebouwen van voor 1994 gelden als asbestverdacht
  (Ondernemersplein, IPLO). Spelregels particuliere verwijdering: IPLO (max. 35 m², niet gelijmd).
- Ventilatie: Bbl art. 4.122 lid 5 (7 dm³/s toilet, 14 dm³/s badruimte, bepaald volgens NEN 1087)
  en art. 4.128 (afvoer rechtstreeks naar buiten). Bron: IPLO, ventilatie nieuwbouw.
- Wering van vocht bestaande bouw: Bbl art. 3.65 (wand tot 1 m en de hele vloer waterafstotend,
  wateropname bepaald volgens NEN 2778). Bron: IPLO.
- Combinatie bad- en toiletruimte nieuwbouw: Bbl art. 4.170 (2,2 m², breedte 0,9 m). Bron: IPLO.
- Normen die genoemd worden en bestaan: NEN 1010 (elektrische installaties), NEN 1006
  (leidingwaterinstallaties), NEN 3215 (gebouwriolering), NEN 1087 (ventilatie), NEN 2778
  (vochtwering), DIN 18534 (Duitse norm voor afdichting in binnenruimten).
- Garantie: BW 7:758 lid 4 (Wkb, overeenkomsten vanaf 1 januari 2024), BW 7:761 (verjaring
  twee jaar na protest), wettelijke garantie bij koop (Rijksoverheid, ACM). SWK en Woningborg
  dragen het Keurmerk GarantieWoning en zijn er voor nieuwbouw.
- VvE: BW Boek 5 titel 9 (appartementsrechten); splitsingsakte en huishoudelijk reglement
  bepalen wat privé en wat gemeenschappelijk is.
Prijzen staan bewust niet in de artikelen; daarvoor linken we naar de kostenpagina's.
"""

# Bronnen die in meerdere artikelen terugkomen
BBL = ("Besluit bouwwerken leefomgeving (Bbl), actuele tekst op wetten.overheid.nl",
       "https://wetten.overheid.nl/BWBR0041297/")
IPLO_VENTILATIE = ("IPLO, Ventilatie: regels bij nieuwbouw (Bbl artikel 4.122 en 4.128)",
                   "https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/ventilatie/")
IPLO_VOCHT = ("IPLO, Wering van vocht: regels bij bestaande bouw (Bbl artikel 3.65)",
              "https://iplo.nl/regelgeving/regels-voor-activiteiten/in-stand-houden-bestaand-bouwwerk/rijksregels/wering-vocht/")
IPLO_BADRUIMTE = ("IPLO, Bad- en toiletruimte: regels bij nieuwbouw (Bbl artikel 4.170)",
                  "https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/bad-toiletruimte/")
IPLO_ASBEST = ("IPLO, Spelregels particuliere verwijdering asbesthoudend materiaal",
               "https://iplo.nl/thema/asbest/praktische-informatie-verwijderen-asbest/spelregels-particuliere-verwijdering/")
IPLO_ASBEST_NL = ("IPLO, Toepassing van asbest in Nederland",
                  "https://iplo.nl/thema/asbest/wat-is-asbest/toepassing-in-nederland/")
RIJK_ASBEST = ("Rijksoverheid, Asbestbeleid",
               "https://www.rijksoverheid.nl/onderwerpen/asbest/asbestbeleid")
ONDERNEMERSPLEIN_ASBEST = ("Ondernemersplein (KVK), Werken met asbest",
                           "https://ondernemersplein.overheid.nl/werken-met-asbest")
BW7 = ("Burgerlijk Wetboek Boek 7, titel 12: aanneming van werk",
       "https://wetten.overheid.nl/BWBR0005290/")
BW5 = ("Burgerlijk Wetboek Boek 5, titel 9: appartementsrechten",
       "https://wetten.overheid.nl/BWBR0005288/")
IPLO_WKB = ("IPLO, Aansprakelijkheid onder de Wet kwaliteitsborging (artikel 7:758 lid 4 BW)",
            "https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/kwaliteitsborging/privaatrecht-wet-kwaliteitsborging/aansprakelijkheid-wet-kwaliteitsborging/")
RIJK_GARANTIE = ("Rijksoverheid, Welke garanties heb ik op een product?",
                 "https://www.rijksoverheid.nl/onderwerpen/bescherming-van-consumenten/vraag-en-antwoord/welke-garanties-heb-ik-op-een-product")
ACM_GARANTIE = ("ACM, Recht op een deugdelijk product (garantie en conformiteit)",
                "https://www.acm.nl/nl/onderwerpen/consumentenrecht/garantie-en-conformiteit/recht-op-een-deugdelijk-product/")
GARANTIEWONING = ("Stichting GarantieWoning, keurmerk voor garantie- en waarborgregelingen",
                  "https://www.garantiewoning.nl/")
SWK = ("SWK, Garantie- en waarborgregeling", "https://www.swk.nl/")
RIJK_VVE = ("Rijksoverheid, Wat houdt een vereniging van eigenaars (VvE) in?",
            "https://www.rijksoverheid.nl/documenten/vraag-en-antwoord/huis-kopen/wat-houdt-een-vereniging-van-eigenaars-vve-in")
UTRECHT_VVE = ("Gemeente Utrecht, Onderhoud en verbouwen voor VvE's",
               "https://www.utrecht.nl/wonen-en-leven/wonen/uw-koopwoning/hulp-voor-uw-vve/onderhoud-en-verbouwen")
RIJK_VENTILEREN = ("Rijksoverheid, Hoe kan ik mijn huis ventileren?",
                   "https://www.rijksoverheid.nl/themas/klimaat-milieu-en-natuur/duurzame-energie/vraag-en-antwoord/energie-thuis/hoe-kan-ik-mijn-huis-ventileren")
VHN_SCHIMMEL = ("Volkshuisvesting Nederland, Aanpak vocht en schimmel",
                "https://www.volkshuisvestingnederland.nl/onderwerpen/aanpak-vocht-en-schimmel")
NEN = ("NEN, normen voor de bouw en installaties (NEN 1006, NEN 1010, NEN 3215)",
       "https://www.nen.nl/")


ARTIKELEN = [
# ---------------------------------------------------------------------------
{
"slug": "badkamer-waterdicht-maken",
"groep": "Techniek en vocht",
"titel": "Badkamer waterdicht maken: zo voorkom je lekkage",
"seo_titel": "Badkamer waterdicht maken: zo doe je het goed",
"description": "Tegels en voegen zijn niet waterdicht. Lees waar de afdichting onder de tegels moet komen, welke systemen er zijn en waar je op let bij kimband en doorvoeren.",
"kort": "Waarom tegels niet waterdicht zijn, waar de afdichting moet komen en hoe je het werk controleert.",
"intro": "Veel mensen denken dat tegels een badkamer waterdicht maken. Dat klopt niet. Voegen en zelfs sommige tegels laten water door. De echte bescherming zit in een laag onder de tegels. Is die niet goed, dan merk je dat vaak pas na jaren: losse tegels, schimmel of een lekkage bij de buren. In dit artikel lees je waar die afdichting moet komen en hoe je controleert of het goed gebeurt.",
"kort_antwoord": "Een badkamer wordt waterdicht door een afdichtingslaag onder het tegelwerk, niet door de tegels zelf. Die laag komt op de hele vloer, op de wanden rond douche en bad, en wordt in hoeken en bij leidingen extra verstevigd met kimband en manchetten. Kitwerk is onderhoud en geen vervanging van die laag.",
"secties": [
("waarom", "Waarom tegels niet waterdicht zijn",
"""<p>Cementvoegen zijn poreus. Ze nemen water op, zeker in de douchehoek waar ze dagelijks nat worden. Dat water zakt naar de ondergrond. Is die ondergrond van gips, hout of gewone steen, dan kan die vocht opnemen en zwellen, schimmelen of zijn hechting verliezen. Ook kleine scheurtjes in voegen of kit laten water door.</p>
<p>De gevolgen zie je meestal niet meteen. Water kan maanden onder de tegels blijven staan. Pas als een tegel hol klinkt, de kit zwart wordt of er een vlek op het plafond eronder komt, wordt het zichtbaar. Dan is herstel vaak duur, omdat het tegelwerk eraf moet.</p>"""),
("regels", "Wat de regels zeggen",
"""<p>Het Besluit bouwwerken leefomgeving (Bbl), de opvolger van het Bouwbesluit, stelt een ondergrens. Voor een bestaande woning moeten in de badruimte de hele vloer en de wanden tot 1 meter hoogte waterafstotend zijn (artikel 3.65). De wateropname wordt bepaald met de norm NEN 2778. Voor nieuwbouw gelden aanvullende eisen.</p>
<p>Die wettelijke ondergrens is laag. Een douche spat veel hoger dan 1 meter. Vakmensen volgen daarom de voorschriften van de fabrikant van het afdichtingssysteem. In Duitsland is daar een aparte norm voor, DIN 18534, die ook Nederlandse vakmensen vaak als richtlijn gebruiken. Een Nederlandse norm specifiek voor afdichting onder tegels in woningen is er niet.</p>"""),
("zones", "Waar de afdichting moet komen",
"""<ul class="checklist">
<li><strong>De hele vloer</strong>, met een opstaande rand van een paar centimeter langs alle wanden. Zo blijft water op de vloer en loopt het niet onder de wand door.</li>
<li><strong>De douchehoek</strong>: vloer en wanden, minstens tot boven de douchekop. Bij een inloopdouche zonder bak is dit het belangrijkste deel.</li>
<li><strong>Rond en achter het bad</strong>, tot een flink stuk boven de rand, en de wand achter een badkraan.</li>
<li><strong>Elke doorvoer</strong>: kraanaansluitingen, een thermostaatkraan in de wand en de afvoer in de vloer.</li>
<li><strong>Hoeken en naden</strong> tussen vloer en wand en tussen twee wanden, want daar werkt het gebouw en ontstaan scheurtjes.</li>
</ul>"""),
("systemen", "Welke afdichtingssystemen er zijn",
"""<p>Er zijn grofweg drie manieren:</p>
<ul>
<li><strong>Vloeibare afdichting.</strong> Een pasta die je in twee lagen met een kwast of roller aanbrengt. Belangrijk is de laagdikte die de fabrikant voorschrijft. Te dun aangebracht werkt het niet.</li>
<li><strong>Afdichtingsfolie of -matten.</strong> Banen die in tegellijm worden gelegd, met overlap op de naden. Dit geeft een gelijkmatige laag en droogt niet, zodat je sneller verder kunt.</li>
<li><strong>Kant-en-klare onderdelen.</strong> Bijvoorbeeld een tegelbare douchevloer met afschot en afvoer, of een bouwplaat die zelf waterdicht is. De naden en aansluitingen moeten dan alsnog worden afgedicht.</li>
</ul>
<p>Welk systeem het beste is, hangt af van de ondergrond. Wat telt: alle onderdelen komen van hetzelfde systeem en worden verwerkt volgens het technische blad. Een vakman die onderdelen van verschillende merken mengt, kan bij problemen moeilijk aantonen dat het werk goed was.</p>"""),
("ondergrond", "De ondergrond telt mee",
"""<p>Gewone gipsplaat is geen goede ondergrond in de natte zone, ook niet met afdichting erop. Gebruik daar vochtbestendige of cementgebonden bouwplaat. Een houten vloer, zoals in veel oudere woningen op de verdieping, werkt mee met temperatuur en vocht. Die moet stijf genoeg zijn en vaak eerst een plaat of een egalisatielaag krijgen. Een scheur in de ondergrond wordt na verloop van tijd ook een scheur in de afdichting.</p>"""),
("kitwerk", "Kitwerk is onderhoud",
"""<p>Kit zit in de hoeken, rond het bad en langs de douchebak. Het voorkomt dat water in de naad loopt, maar het veroudert. Na een aantal jaren laat kit los of wordt hij zwart van schimmel. Vervang hem dan op tijd. Zie kitwerk als de buitenste verdediging en de afdichting onder de tegels als de echte bescherming. Wat kitwerk kost, lees je op de pagina over <a href="/kosten/kitwerk-voegen/">kitwerk en voegen</a>.</p>"""),
],
"stappen_kop": "Zo controleer je het werk",
"stappen": [
("Vraag welk systeem er komt", "Laat in de offerte zetten welk afdichtingssysteem wordt gebruikt en op welke delen van vloer en wanden."),
("Kijk voordat er getegeld wordt", "Spreek af dat je de afdichting ziet voordat de tegels erop gaan. Maak foto's van de hoeken, de afvoer en de doorvoeren."),
("Let op kimband en manchetten", "In elke hoek hoort een band, en rond elke leiding en de afvoer een manchet. Ontbreken die, vraag er dan naar."),
("Laat de droogtijd uitvoeren", "Vloeibare afdichting moet drogen tussen de lagen en voordat er getegeld wordt. Haast hierin is een veelgemaakte fout."),
("Bewaar de gegevens", "Vraag welk product is gebruikt en bewaar de foto's. Dat helpt bij een klacht of bij verkoop van de woning."),
],
"faq": [
("Is een badkamer met nieuwe tegels automatisch waterdicht?", "Nee. Tegels en vooral cementvoegen laten water door. De waterdichtheid komt van een afdichtingslaag onder het tegelwerk, die op de hele vloer en op de wanden rond douche en bad hoort te zitten."),
("Hoe hoog moet de wand waterdicht zijn bij een douche?", "Het Bbl vraagt voor een bestaande woning minimaal 1 meter, maar dat is laag. Fabrikanten van afdichtingssystemen adviseren in de douchehoek minstens tot boven de douchekop te gaan."),
("Kan ik de afdichting zelf aanbrengen?", "Dat kan, als je het technische blad van het systeem precies volgt, inclusief laagdikte, droogtijd, kimband en manchetten. Een fout merk je pas na jaren, dus twijfel je, laat het dan doen."),
("Is waterdichte tegellijm genoeg?", "Nee. Tegellijm is bedoeld om tegels te laten hechten en is geen afdichting. Gebruik een apart afdichtingssysteem onder de tegels."),
("Hoe vaak moet ik het kitwerk vervangen?", "Dat hangt af van het gebruik en het ventileren. Vervang kit zodra hij loslaat, scheurt of zwart wordt en niet meer schoon te krijgen is."),
],
"bronnen": [IPLO_VOCHT, BBL],
"dienst": "tegelwerk-badkamer",
"kosten": ["kitwerk-voegen", "tegelzetter-per-m2"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["inloopdouche-zonder-drempel", "badkamer-ventilatie", "garantie-badkamerrenovatie"],
},
# ---------------------------------------------------------------------------
{
"slug": "tegels-kiezen",
"groep": "Ontwerp en materialen",
"titel": "Tegels kiezen voor de badkamer: soort, formaat en antislip",
"seo_titel": "Badkamertegels kiezen: soort, formaat en antislip",
"description": "Welke tegels passen in een badkamer? Uitleg over keramiek en porselein, grote of kleine formaten, antislip voor de douchevloer, gerectificeerde tegels en voegen.",
"kort": "Keramiek of porselein, groot of klein formaat, antislip en voegen: zo kies je tegels die bij je badkamer passen.",
"intro": "Tegels bepalen voor een groot deel hoe je badkamer eruitziet. Maar ze moeten ook jaren tegen water, zeep en schoonmaakmiddel kunnen, en op de vloer mag je er niet op uitglijden. In dit artikel lees je waar je op let bij de soort tegel, het formaat, de antislip en de voegen, zodat je in de winkel weet welke vragen je stelt.",
"kort_antwoord": "Kies voor de vloer een porseleinen tegel met voldoende antislip, zeker in de douche. Op de wand kun je ook keramische wandtegels gebruiken. Grote tegels geven rust en minder voegen, maar vragen een vlakke ondergrond en een afschot dat bij het formaat past. Kleine tegels of mozaïek volgen een afschot makkelijker.",
"secties": [
("soorten", "Keramiek of porselein",
"""<p>De meeste badkamertegels zijn van gebakken klei. Het verschil zit in hoe dicht het materiaal is.</p>
<ul>
<li><strong>Keramische wandtegels</strong> zijn wat zachter en nemen meer water op. Op de wand zijn ze prima, omdat er weinig druk op komt. Ze zijn makkelijk te zagen.</li>
<li><strong>Porseleinen tegels</strong> (ook wel keramisch graniet of porcellanato) zijn heel dicht gebakken en nemen bijna geen water op. Ze zijn hard en slijtvast en daardoor geschikt voor vloer en wand.</li>
<li><strong>Natuursteen</strong>, zoals marmer of leisteen, is mooi maar vraagt meer onderhoud. Het moet vaak worden geïmpregneerd en kan vlekken door kalk, zeep of zure schoonmaakmiddelen.</li>
</ul>
<p>Twijfel je, vraag dan naar de waterabsorptie en de slijtvastheid in de productgegevens. Een tegel voor de vloer moet geschikt zijn voor belopen.</p>"""),
("formaat", "Groot of klein formaat",
"""<p>Grote tegels, zoals 60 bij 60 of 60 bij 120 centimeter, zijn populair. Ze geven een rustig beeld en je hebt minder voegen om schoon te houden. Maar er zijn nadelen:</p>
<ul>
<li>De ondergrond moet heel vlak zijn. Elke bobbel zie je terug als een rand tussen twee tegels.</li>
<li>Op een douchevloer met afschot naar een putje in het midden werken grote tegels slecht, omdat de vloer dan in vier richtingen helt. Met een douchegoot langs de wand helt de vloer maar één kant op, en dan kan het wel.</li>
<li>Grote tegels zijn zwaar en lastig te verwerken. Reken op meer werkuren per vierkante meter.</li>
</ul>
<p>Kleine tegels en mozaïek volgen een afschot makkelijk en geven door de vele voegen extra grip onder je voeten. Dat maakt ze geschikt voor de douchevloer, ook als de rest van de vloer grote tegels krijgt.</p>"""),
("antislip", "Antislip op de vloer",
"""<p>Een natte tegel kan glad zijn. Fabrikanten geven de stroefheid aan met een klasse. Veel gebruikt zijn de Duitse testmethoden DIN 51130, met de klassen R9 tot R13 voor schoeisel, en DIN 51097, met de klassen A, B en C voor blote voeten. Hoe hoger de letter of het getal, hoe stroever.</p>
<p>Voor een douchevloer waar je op blote voeten staat, is de blotevoetklasse het nuttigst. Vraag in de winkel naar die waarde. Een heel stroeve tegel is wel moeilijker schoon te houden. Een tussenweg is een stroeve tegel alleen in de douche en een gladdere op de rest van de vloer.</p>"""),
("gerectificeerd", "Gerectificeerde tegels en voegbreedte",
"""<p>Een gerectificeerde tegel is na het bakken op maat geslepen. Alle tegels zijn daardoor precies even groot en hebben strakke randen. Dat maakt een smalle voeg van een paar millimeter mogelijk. Niet-gerectificeerde tegels hebben iets afgeronde randen en kleine maatverschillen. Die vragen een bredere voeg.</p>
<p>Voor voegen kun je kiezen uit cementgebonden voegmiddel en epoxyvoeg. Epoxy neemt geen water op en verkleurt minder, maar is lastiger te verwerken en duurder. Een donkere voegkleur laat minder vuil zien dan wit.</p>"""),
("hoeveel", "Hoeveel tegels heb je nodig?",
"""<p>Meet vloer en wanden op en trek ramen en de deur af. Tel daar een deel bij op voor zaagverlies en breuk. Bij een recht legpatroon is dat minder dan bij een visgraat- of diagonaalpatroon. Koop alles uit één productiepartij, want de kleur kan per partij iets verschillen. Bewaar een paar reservetegels voor later herstel. De <a href="/tools/badkamercalculator/">badkamercalculator</a> helpt je met een eerste schatting.</p>"""),
],
"stappen_kop": "Checklist voor in de winkel",
"stappen": [
("Waar komt de tegel?", "Vraag of de tegel geschikt is voor vloer, wand of beide, en voor natte ruimten."),
("Wat is de antislipklasse?", "Vraag voor de douchevloer naar de klasse voor blote voeten (A, B of C)."),
("Is hij gerectificeerd?", "Dat bepaalt hoe smal de voeg kan zijn."),
("Past het formaat bij het afschot?", "Overleg met de tegelzetter welk formaat past bij de afvoer die je kiest."),
("Uit één partij en met reserve", "Bestel genoeg uit één partij en bewaar een paar tegels voor herstel."),
],
"faq": [
("Kan ik dezelfde tegel op vloer en wand gebruiken?", "Ja, met porseleinen tegels kan dat. Keramische wandtegels zijn niet geschikt voor de vloer, omdat ze minder sterk en slijtvast zijn."),
("Welke tegel is het minst glad in de douche?", "Een tegel met een hoge blotevoetklasse volgens DIN 51097, of kleine tegels en mozaïek met veel voegen. Vraag de klasse na in de productgegevens."),
("Zijn grote tegels geschikt voor een kleine badkamer?", "Vaak wel. Minder voegen geven rust en laten de ruimte groter lijken. Let op de douchevloer: met een putje in het midden zijn kleinere tegels beter, met een goot langs de wand kunnen grote tegels."),
("Wat betekent gerectificeerd?", "De tegel is na het bakken op exacte maat geslepen. Daardoor zijn de randen strak en kan de voeg smal zijn."),
("Hoeveel extra tegels moet ik bestellen?", "Dat hangt af van het legpatroon en het aantal hoeken en uitsparingen. Vraag de tegelzetter om een opgave, en bewaar altijd een paar reservetegels."),
],
"bronnen": [IPLO_VOCHT],
"dienst": "tegelwerk-badkamer",
"kosten": ["tegelzetter-per-m2", "nieuwe-badkamer"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Waar je op let bij het kopen van tegels.")],
"gerelateerd": ["badkamer-waterdicht-maken", "kleine-badkamer-indelen", "badkamerstijlen"],
},
# ---------------------------------------------------------------------------
{
"slug": "inloopdouche-zonder-drempel",
"groep": "Techniek en vocht",
"titel": "Inloopdouche zonder drempel: afschot, afvoer en ruimte",
"seo_titel": "Inloopdouche zonder drempel: zo werkt het",
"description": "Een inloopdouche zonder drempel vraagt om afschot, een goede afvoer en een waterdichte vloer. Lees wat er technisch nodig is en wanneer het lastig wordt.",
"kort": "Wat een drempelloze inloopdouche technisch vraagt: afschot, goot of putje, hoogte van de afvoer en afdichting.",
"intro": "Een inloopdouche zonder drempel ziet er strak uit en is makkelijk toegankelijk, ook als je ouder wordt of slecht ter been bent. Maar zonder bak of drempel moet de vloer zelf het water naar de afvoer leiden. Dat vraagt meer voorbereiding dan een gewone douchebak. Hier lees je wat er nodig is en waar het in een bestaande woning lastig kan worden.",
"kort_antwoord": "Voor een inloopdouche zonder drempel moet de douchevloer licht aflopen naar een goot of putje, met genoeg hoogte onder de vloer voor de afvoer en een volledig waterdichte laag onder de tegels. In een bestaande woning bepaalt vooral de hoogte en ligging van de bestaande afvoer of het kan. Soms moet de vloer omhoog of de afvoer worden verlegd.",
"secties": [
("afschot", "Afschot: de vloer loopt af",
"""<p>Zonder drempel moet het water vanzelf naar de afvoer stromen. Daarom krijgt de douchevloer afschot: een kleine helling. Vakmensen werken meestal met ongeveer 1 tot 2 centimeter per meter. Te weinig afschot geeft plassen, te veel voelt scheef aan onder je voeten.</p>
<p>Er zijn twee vormen:</p>
<ul>
<li><strong>Afschot naar een putje</strong> in het midden of in een hoek. De vloer helt dan in meerdere richtingen. Dat werkt het best met kleine tegels.</li>
<li><strong>Afschot naar een goot</strong> langs de wand. De vloer helt dan maar één kant op. Daardoor kun je ook grote tegels gebruiken.</li>
</ul>"""),
("afvoer", "De afvoer bepaalt wat kan",
"""<p>Een douchegoot of putje heeft een sifon nodig die water vasthoudt, zodat er geen rioollucht in de badkamer komt. Die sifon heeft hoogte nodig onder de vloer. Daarna moet de afvoerbuis nog met een klein verval naar de standleiding lopen. Hoe verder de douche van de standleiding af ligt, hoe meer hoogte je nodig hebt.</p>
<p>In een nieuwbouwwoning met een dekvloer is daar vaak ruimte voor. In een oudere woning met een houten vloer of een dunne dekvloer op beton soms niet. Oplossingen zijn dan:</p>
<ul>
<li>een extra platte goot of een putje met een lage sifon;</li>
<li>de hele badkamervloer een paar centimeter ophogen, zodat er toch geen drempel ontstaat ten opzichte van de douche (wel vaak bij de deur);</li>
<li>de afvoer verleggen of in een appartement afstemmen met de VvE, zie <a href="/kennisbank/verbouwen-in-vve/">verbouwen in een VvE</a>.</li>
</ul>
<p>Voor gebouwriolering bestaat de norm NEN 3215. Een loodgieter of installateur rekent daarmee of de afvoer voldoende capaciteit en verval heeft.</p>"""),
("ruimte", "Hoeveel ruimte heb je nodig?",
"""<p>Een inloopdouche heeft geen deur of maar één vaste glazen wand. Water spat dus verder dan bij een afgesloten cabine. Hoe groter de douchezone, hoe minder water buiten de douche komt. In een kleine badkamer kun je de douche laten doorlopen in de rest van de vloer: dan wordt de hele badkamer een natte ruimte, met afschot naar één afvoer. Lees meer in <a href="/kennisbank/kleine-badkamer-indelen/">een kleine badkamer indelen</a>.</p>
<p>Wil je de douche geschikt maken voor later, denk dan ook aan steunbeugels (de wand moet die kunnen dragen), een opklapbaar zitje en genoeg draairuimte.</p>"""),
("waterdicht", "Waterdicht maken is extra belangrijk",
"""<p>Bij een douchebak vangt de bak het water op. Bij een drempelloze inloopdouche doet de vloer dat. De afdichting onder de tegels moet daarom over de hele vloer doorlopen, met kimband in alle hoeken en een afdichtingsflens bij de goot of het putje. Fouten op deze plek leiden snel tot lekkage naar de ruimte eronder. Meer hierover in <a href="/kennisbank/badkamer-waterdicht-maken/">badkamer waterdicht maken</a>.</p>"""),
("onderhoud", "Onderhoud van goot en putje",
"""<p>Haren en zeepresten verzamelen zich in de sifon. Kies een goot of putje waarvan je het rooster en de sifon makkelijk los kunt halen. Maak die regelmatig schoon. Een goot met een tegelbaar rooster valt minder op, maar moet ook goed bereikbaar blijven.</p>"""),
],
"stappen_kop": "Stappen voor een drempelloze inloopdouche",
"stappen": [
("Laat de afvoer bekijken", "Een vakman meet de hoogte van de vloer en de afstand tot de standleiding."),
("Kies goot of putje", "Kies samen met het tegelformaat: een goot bij grote tegels, een putje bij kleine."),
("Bepaal het afschot", "Leg vast hoeveel afschot er komt en in welke richting."),
("Dicht de hele vloer af", "Afdichting over de hele douchezone, met kimband, manchetten en de flens van de afvoer."),
("Test voor het tegelen", "Laat water lopen en kijk of het goed wegloopt voordat de tegels erop gaan."),
],
"faq": [
("Kan een inloopdouche zonder drempel in elke badkamer?", "Niet altijd zonder aanpassingen. Het hangt af van de hoogte onder de vloer en de ligging van de afvoer. Soms moet de vloer omhoog of de afvoer worden verlegd."),
("Hoeveel afschot heeft een inloopdouche nodig?", "Vakmensen werken meestal met ongeveer 1 tot 2 centimeter per meter naar de goot of het putje. De precieze helling hangt af van het tegelformaat en de afvoer."),
("Wat is beter, een douchegoot of een putje?", "Een goot laat de vloer maar één kant op hellen, zodat grote tegels kunnen. Een putje is vaak lager en goedkoper, maar vraagt kleinere tegels door het afschot in meerdere richtingen."),
("Spat het water niet de badkamer in?", "Dat hangt af van de breedte van de douchezone en de glazen wand. Een ruimere douchezone of een iets langere wand helpt."),
("Is een inloopdouche geschikt als je ouder wordt?", "Ja, zonder drempel kun je er met een rollator of rolstoel in. Denk dan ook aan steunbeugels en een zitje."),
],
"bronnen": [NEN, IPLO_VOCHT],
"dienst": "inloopdouche-plaatsen",
"kosten": ["inloopdouche", "uurtarief-loodgieter"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/inloopdouche-kopen/", "Inloopdouche kopen", "Glazen wand, goot en douchekop kiezen.")],
"gerelateerd": ["badkamer-waterdicht-maken", "kleine-badkamer-indelen", "tegels-kiezen"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-ventilatie",
"groep": "Techniek en vocht",
"titel": "Badkamer ventileren: regels, systemen en schimmel voorkomen",
"seo_titel": "Badkamer ventileren: regels en schimmel voorkomen",
"description": "Hoeveel moet een badkamer ventileren? De eisen uit het Bbl, het verschil tussen een raam, mechanische afzuiging en WTW, en tips om schimmel te voorkomen.",
"kort": "De eisen uit het Bbl, welk systeem past en hoe je schimmel in de badkamer voorkomt.",
"intro": "Na een douchebeurt hangt er veel waterdamp in de badkamer. Als die niet snel weg kan, slaat hij neer op koude tegels, het plafond en de kitranden. Daar groeit dan schimmel. Goede ventilatie is daarom net zo belangrijk als goed tegelwerk. Bij een renovatie is het hét moment om de ventilatie op orde te brengen.",
"kort_antwoord": "Volgens het Besluit bouwwerken leefomgeving (Bbl) moet een badruimte bij nieuwbouw een ventilatiecapaciteit hebben van minimaal 14 dm³ per seconde, en de lucht moet rechtstreeks naar buiten worden afgevoerd. In de praktijk betekent dat een mechanische afzuiging of een goed werkend kanaal, plus een spleet onder de deur voor de toevoer van lucht.",
"secties": [
("regels", "Wat zegt de regelgeving?",
"""<p>Sinds 1 januari 2024 staan de bouwregels in het Besluit bouwwerken leefomgeving (Bbl), de opvolger van het Bouwbesluit. Voor ventilatie bij nieuwbouw geldt:</p>
<ul>
<li>een badruimte heeft een ventilatiecapaciteit van minimaal <strong>14 dm³/s</strong> (artikel 4.122, lid 5);</li>
<li>een toiletruimte minimaal <strong>7 dm³/s</strong>; zijn toilet en badkamer één ruimte, dan geldt de hoogste eis van 14 dm³/s;</li>
<li>de afvoer van lucht uit de badruimte moet <strong>rechtstreeks naar buiten</strong> (artikel 4.128). Een kanaal mag wel door een andere ruimte lopen.</li>
</ul>
<p>De capaciteit wordt bepaald volgens de norm NEN 1087. Voor bestaande woningen en verbouwingen gelden andere, meestal lagere eisen. Wie toch verbouwt, doet er goed aan de nieuwbouweis als doel te nemen. Twijfel je wat in jouw geval geldt, vraag het dan na bij de gemeente.</p>
<p>Ter vergelijking: 14 dm³/s is ongeveer 50 kubieke meter lucht per uur.</p>"""),
("systemen", "Welke manieren van ventileren zijn er?",
"""<ul>
<li><strong>Een raam.</strong> Een raam alleen voert damp vaak niet snel genoeg af, zeker als het buiten windstil of koud is. Het mag ook niet de enige oplossing zijn als het raam klein is of weinig open kan.</li>
<li><strong>Natuurlijke afvoer via een kanaal.</strong> In oudere woningen zit soms een rooster met een kanaal naar het dak. Dat werkt door trek en is afhankelijk van het weer.</li>
<li><strong>Mechanische afzuiging.</strong> Een centrale ventilatiebox zuigt lucht af uit keuken, toilet en badkamer. Of een losse ventilator in de badkamer met een kanaal naar buiten. Een vochtsensor of een nalooptimer zorgt dat hij lang genoeg doordraait.</li>
<li><strong>Balansventilatie met warmteterugwinning (WTW).</strong> Lucht wordt afgezogen en verse lucht wordt ingeblazen, waarbij de warmte van de afgevoerde lucht wordt hergebruikt. Dat zit vooral in nieuwe en goed geïsoleerde woningen.</li>
</ul>"""),
("toevoer", "Vergeet de toevoer niet",
"""<p>Afzuigen werkt alleen als er ook lucht binnen kan komen. Daarom heeft een badkamerdeur meestal een spleet van een paar centimeter onder de deur, of een rooster in de deur. Wordt de deur bij de renovatie vervangen of komt er een nieuwe, hogere vloer, let dan op dat die spleet blijft. Een nieuwe afzuiging met een dichte deur zonder spleet haalt veel minder lucht weg dan hij zou kunnen.</p>"""),
("renovatie", "Waar let je op bij een renovatie?",
"""<ul class="checklist">
<li>Laat meten of de afzuiging in de badkamer de 14 dm³/s haalt. Een installateur kan dit met een meter vaststellen.</li>
<li>Vervang een oud of vervuild afzuigventiel en maak het kanaal schoon.</li>
<li>Kies bij een losse ventilator een stil model met vochtsensor of nalooptimer.</li>
<li>Zorg dat het kanaal naar buiten gaat en niet eindigt in een zolder of spouw.</li>
<li>Een badkamer met een inloopdouche zonder deur heeft meer vocht in de lucht. Plaats de afzuiging bij voorkeur bij de douche en niet bij de deur.</li>
<li>In een appartement: de afvoerkanalen zijn vaak gemeenschappelijk. Overleg met de VvE voordat je iets aansluit.</li>
</ul>"""),
("schimmel", "Schimmel voorkomen in het dagelijks gebruik",
"""<p>Zet de mechanische ventilatie voor het douchen op de hoogste stand en laat hem daarna nog een tijd doordraaien. Houd de deur dicht tijdens en direct na het douchen, zodat de afzuiging de damp uit de badkamer haalt in plaats van uit de gang. Trek de wanden en de vloer van de douche droog met een wisser. Een raam dat urenlang open staat in de winter koelt de badkamer af en kan juist meer condens geven.</p>"""),
],
"stappen_kop": "Snelle check van je ventilatie",
"stappen": [
("De tissuetest", "Houd een velletje toiletpapier tegen het afzuigventiel. Wordt het niet aangezogen, dan werkt de afzuiging slecht."),
("Kijk na het douchen", "Blijft de spiegel lang beslagen of druppelt het plafond? Dan is de ventilatie te zwak."),
("Controleer de deur", "Is er een spleet of rooster? Zonder toevoer werkt afzuiging niet goed."),
("Let op zwarte kitranden", "Steeds terugkerende schimmel wijst op te weinig ventilatie of te veel vocht."),
("Laat meten", "Bij twijfel meet een installateur de werkelijke luchthoeveelheid."),
],
"faq": [
("Is een raam in de badkamer genoeg?", "Vaak niet. Een raam voert damp niet altijd snel genoeg af. De regels voor nieuwbouw vragen een capaciteit van 14 dm³/s met afvoer rechtstreeks naar buiten, wat meestal mechanische afzuiging betekent."),
("Hoeveel moet een badkamer ventileren?", "Bij nieuwbouw minimaal 14 dm³/s volgens het Bbl, artikel 4.122. Dat is ongeveer 50 kubieke meter per uur."),
("Hoe lang moet de ventilatie aan na het douchen?", "Laat hem op een hoge stand doordraaien tot de spiegel en wanden weer droog zijn. Een nalooptimer of vochtsensor regelt dit automatisch."),
("Mag ik een afzuigventilator aansluiten op de centrale ventilatie?", "Nee, een losse ventilator met eigen motor hoort niet op het kanaal van een centrale box. Overleg met een installateur, en in een appartement met de VvE."),
("Waarom komt de schimmel steeds terug?", "Meestal is de ventilatie te zwak, ontbreekt de toevoer onder de deur, of blijft er water staan op koude plekken. Schoonmaken helpt dan maar tijdelijk."),
],
"bronnen": [IPLO_VENTILATIE, BBL, RIJK_VENTILEREN, VHN_SCHIMMEL],
"dienst": "badkamer-renoveren",
"kosten": ["nieuwe-badkamer", "uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["badkamer-waterdicht-maken", "volgorde-badkamerrenovatie", "verbouwen-in-vve"],
},
# ---------------------------------------------------------------------------
{
"slug": "garantie-badkamerrenovatie",
"groep": "Plannen en regels",
"titel": "Garantie op een badkamerrenovatie: wat zijn je rechten?",
"seo_titel": "Garantie op een badkamerrenovatie: je rechten",
"description": "Welke garantie heb je op een nieuwe badkamer? Het verschil tussen de wettelijke garantie, de garantie van de vakman en SWK of Woningborg, en wat je vastlegt.",
"kort": "Wettelijke garantie, garantie van de vakman en SWK of Woningborg: wat geldt er bij een badkamerrenovatie?",
"intro": "Een nieuwe badkamer is een grote uitgave. Gaat er na een jaar iets mis, zoals een lekkage of losse tegels, dan wil je weten waar je aan toe bent. Er bestaan verschillende soorten garantie door elkaar: de wet, de belofte van de vakman, de fabrieksgarantie op producten en regelingen als SWK. In dit artikel zetten we ze op een rij.",
"kort_antwoord": "Je hebt altijd wettelijke rechten: het werk en de spullen moeten deugdelijk zijn. Een garantie van de vakman komt daar bovenop en kan je rechten niet beperken. SWK en Woningborg, met het keurmerk GarantieWoning, zijn regelingen voor nieuwbouw en gelden meestal niet voor een badkamerrenovatie in een bestaande woning. Leg afspraken over garantie altijd schriftelijk vast.",
"secties": [
("wettelijk", "De wettelijke garantie op het werk",
"""<p>Laat je een badkamer verbouwen, dan sluit je juridisch een overeenkomst van <strong>aanneming van werk</strong>. De regels staan in het Burgerlijk Wetboek, Boek 7, titel 12. De vakman moet goed en deugdelijk werk leveren.</p>
<p>Sinds 1 januari 2024 geldt door de Wet kwaliteitsborging voor het bouwen een belangrijke regel bij bouwwerken, ook bij een verbouwing: de aannemer is aansprakelijk voor gebreken die bij de oplevering niet zijn ontdekt, tenzij die niet aan hem zijn toe te rekenen (artikel 7:758 lid 4 BW). Dit geldt voor overeenkomsten die vanaf die datum zijn gesloten.</p>
<p>Ontdek je een gebrek, meld het dan zo snel mogelijk en schriftelijk. Na die melding heb je twee jaar om naar de rechter te stappen als het niet wordt opgelost (artikel 7:761 BW). Wacht dus niet te lang en bewaar alle correspondentie.</p>"""),
("producten", "Wettelijke garantie op de spullen",
"""<p>Koop je zelf een toilet, kraan of douchewand, dan heb je bij de verkoper wettelijke garantie. Een product moet doen wat je er redelijkerwijs van mag verwachten. Dat heet conformiteit. Er is geen vaste termijn: van een duur toilet mag je verwachten dat het veel langer meegaat dan een paar jaar. Je verhaalt een gebrek op de verkoper, niet op de fabrikant.</p>
<p>Levert de vakman de spullen, dan is hij ook voor die spullen je aanspreekpunt. Een fabrieksgarantie komt altijd bovenop de wettelijke garantie en vervangt die niet.</p>"""),
("vakman", "Wat betekent een garantie van de vakman?",
"""<p>Veel badkamerspecialisten geven een eigen garantie, bijvoorbeeld een aantal jaren op lekkage of op het tegelwerk. Zo'n garantie is een extra belofte. Let op:</p>
<ul>
<li>Een garantie van de vakman kan je wettelijke rechten <strong>niet</strong> beperken. Staat er bijvoorbeeld "één jaar garantie", dan kun je na dat jaar nog steeds een beroep doen op de wet als het werk ondeugdelijk was.</li>
<li>Lees de voorwaarden. Vaak geldt de garantie alleen bij normaal gebruik en onderhoud, zoals op tijd kitwerk vervangen.</li>
<li>Een garantie is zo sterk als het bedrijf dat hem geeft. Gaat het bedrijf failliet, dan vervalt de garantie meestal, tenzij die verzekerd is of via een brancheorganisatie loopt.</li>
</ul>"""),
("swk", "SWK, Woningborg en GarantieWoning",
"""<p>Het Keurmerk GarantieWoning is een kwaliteitsmerk voor garantie- en waarborgregelingen. De Stichting GarantieWoning is in 2010 opgericht door de bouwsector en Vereniging Eigen Huis. Instellingen als SWK en Woningborg werken met regelingen die dit keurmerk dragen.</p>
<p>Die regelingen zijn bedoeld voor <strong>nieuwbouwwoningen</strong>. Ze beschermen kopers als de bouwer failliet gaat of gebreken niet herstelt. Bij een badkamerrenovatie in een bestaande woning gelden ze meestal niet. Laat je een badkamer verbouwen in een nieuwbouwwoning die nog onder zo'n regeling valt, let dan op: werk dat je na de oplevering zelf laat uitvoeren valt er niet onder, en kan gevolgen hebben voor de garantie op de onderdelen die je laat aanpassen.</p>"""),
("vastleggen", "Wat leg je vast in de offerte?",
"""<ul class="checklist">
<li>Wat er precies gebeurt, inclusief het afdichtingssysteem en de merken en typen van sanitair.</li>
<li>De garantie van de vakman: hoe lang, waarop en onder welke voorwaarden.</li>
<li>Welke algemene voorwaarden gelden en bij welke geschillencommissie het bedrijf eventueel is aangesloten.</li>
<li>Hoe de oplevering gaat: samen langslopen en punten op papier zetten.</li>
<li>Een betaalschema dat past bij de voortgang, zonder dat je het hele bedrag vooraf betaalt.</li>
</ul>
<p>Twijfel je over een offerte, gebruik dan de <a href="/tools/offertechecker/">offertechecker</a>.</p>"""),
],
"stappen_kop": "Er gaat iets mis: wat doe je?",
"stappen": [
("Leg het vast", "Maak foto's en noteer wanneer je het gebrek ontdekte."),
("Meld het schriftelijk", "Stuur de vakman een e-mail of brief met een beschrijving en de foto's. Doe dit zo snel mogelijk."),
("Geef een redelijke termijn", "Vraag om herstel binnen een redelijke termijn, bijvoorbeeld twee tot vier weken."),
("Zoek hulp als het vastloopt", "Is het bedrijf aangesloten bij een geschillencommissie, dan kun je daar terecht. Een rechtsbijstandsverzekering kan ook helpen."),
("Let op de termijn", "Na je melding heb je twee jaar om een rechtszaak te beginnen als er niets gebeurt."),
],
"faq": [
("Hoe lang heb je garantie op een nieuwe badkamer?", "De wet noemt geen vast aantal jaren. Het werk moet deugdelijk zijn en zo lang meegaan als je redelijkerwijs mag verwachten. Een garantie van de vakman komt daar bovenop."),
("Geldt SWK-garantie voor een badkamerrenovatie?", "Meestal niet. SWK en Woningborg zijn regelingen voor nieuwbouwwoningen, niet voor een verbouwing van een bestaande woning."),
("Mag een vakman zijn garantie beperken tot één jaar?", "Hij mag een eigen garantie van één jaar geven, maar die kan je wettelijke rechten niet beperken. Na dat jaar kun je nog steeds een beroep doen op de wet."),
("Wat als het bedrijf failliet is?", "Dan vervalt de garantie van het bedrijf meestal. Rechten tegenover de fabrikant van producten kunnen blijven bestaan. Vraag vooraf of de garantie verzekerd is."),
("Moet ik een gebrek binnen een bepaalde tijd melden?", "Meld het zo snel mogelijk na ontdekking en schriftelijk. Na je melding heb je twee jaar om naar de rechter te gaan als het niet wordt opgelost."),
],
"bronnen": [BW7, IPLO_WKB, RIJK_GARANTIE, ACM_GARANTIE, GARANTIEWONING, SWK],
"dienst": "badkamer-renoveren",
"kosten": ["nieuwe-badkamer"],
"tool": "/tools/offertechecker/",
"extra": [],
"gerelateerd": ["badkamer-waterdicht-maken", "volgorde-badkamerrenovatie", "verbouwen-in-vve"],
},
]


ARTIKELEN += [
# ---------------------------------------------------------------------------
{
"slug": "verbouwen-in-vve",
"groep": "Plannen en regels",
"titel": "Badkamer verbouwen in een appartement met VvE",
"seo_titel": "Badkamer verbouwen in een VvE: regels en tips",
"description": "Woon je in een appartement? Lees wanneer je toestemming van de VvE nodig hebt voor een nieuwe badkamer, wat er in de splitsingsakte staat en hoe je overlast beperkt.",
"kort": "Splitsingsakte, huishoudelijk reglement en gemeenschappelijke leidingen: wat mag zonder en wat met toestemming?",
"intro": "In een appartement ben je eigenaar van je eigen woning, maar niet van alles wat erin zit. Leidingen, afvoeren en de vloer waarop je badkamer staat, kunnen van alle eigenaren samen zijn. Daarom gelden er bij een badkamerverbouwing in een VvE extra regels. Die verschillen per gebouw. In dit artikel lees je waar je ze vindt en welke onderwerpen bijna altijd spelen.",
"kort_antwoord": "Wat je mag doen, staat in de splitsingsakte, het reglement dat daarbij hoort en het huishoudelijk reglement van jouw VvE. In het algemeen mag je je privégedeelte verbouwen, maar heb je toestemming nodig als je gemeenschappelijke delen raakt, zoals standleidingen, ventilatiekanalen of de draagvloer. Vraag bij twijfel vooraf schriftelijk toestemming aan het bestuur.",
"secties": [
("documenten", "Waar staan de regels?",
"""<p>Een appartementsgebouw is juridisch gesplitst in appartementsrechten. De regels daarvoor staan in het Burgerlijk Wetboek, Boek 5, titel 9. Per gebouw zijn ze uitgewerkt in drie documenten:</p>
<ul>
<li><strong>De splitsingsakte</strong>, opgesteld door een notaris. Daarin staat welke delen privé zijn en welke gemeenschappelijk. Vaak hoort er een tekening bij.</li>
<li><strong>Het splitsingsreglement</strong>, meestal gebaseerd op een modelreglement uit het jaar van splitsing. Daarin staan de rechten en plichten van eigenaren.</li>
<li><strong>Het huishoudelijk reglement</strong>, met praktische afspraken, bijvoorbeeld over werktijden, geluid of het gebruik van de lift.</li>
</ul>
<p>Je kunt deze stukken opvragen bij het bestuur of de beheerder van de VvE. De splitsingsakte is ook op te vragen bij het Kadaster.</p>"""),
("prive", "Wat is privé en wat is gemeenschappelijk?",
"""<p>Dat verschilt per gebouw, maar dit zijn de onderwerpen die bij een badkamer bijna altijd spelen:</p>
<ul class="checklist">
<li><strong>Standleidingen</strong> voor afvoer en water lopen door alle verdiepingen en zijn meestal gemeenschappelijk. De aftakking naar jouw badkamer is vaak privé. Waar de grens ligt, staat in de akte of moet worden uitgezocht.</li>
<li><strong>Ventilatiekanalen</strong> zijn vaak gemeenschappelijk. Een eigen ventilator aansluiten op een gezamenlijk kanaal kan de afzuiging bij de buren verstoren.</li>
<li><strong>De constructievloer</strong> is vrijwel altijd gemeenschappelijk. Hakken of boren in de betonvloer voor een verdiepte douche of nieuwe afvoer mag meestal niet zonder toestemming.</li>
<li><strong>Dragende muren</strong> zijn gemeenschappelijk. Een badkamer vergroten door een muur weg te halen vraagt toestemming, en vaak ook een constructieve berekening.</li>
</ul>
<p>Niet altijd is duidelijk of een leiding privé of gemeenschappelijk is, zeker als de akte er niets over zegt. Bekijk dan alle stukken, inclusief de splitsingstekening, en vraag het na bij het bestuur.</p>"""),
("toestemming", "Hoe vraag je toestemming?",
"""<p>Doe een schriftelijk verzoek bij het bestuur. Beschrijf wat je wilt doen en welke gemeenschappelijke delen je raakt. Een tekening of de offerte van de vakman helpt. Afhankelijk van het reglement beslist het bestuur of de vergadering van eigenaars. Die kan voorwaarden stellen, bijvoorbeeld dat een erkend installateur het werk doet of dat je de kosten van herstel draagt als er iets misgaat.</p>
<p>Plan dit ruim vooruit. Een vergadering is er soms maar één of twee keer per jaar. Begin pas als je de toestemming op papier hebt. Werk zonder toestemming kan betekenen dat je het moet terugdraaien, en het kan problemen geven bij verkoop.</p>
<p>Ben je het niet eens met een besluit van de vergadering, dan kun je de kantonrechter vragen het te vernietigen of om vervangende toestemming. Dat is een laatste stap; overleg werkt bijna altijd sneller.</p>"""),
("geluid", "Geluid en harde vloeren",
"""<p>Badkamers liggen in appartementen vaak boven elkaar. Het geluid van een toilet dat doortrekt, een douche of een harde tegelvloer kan bij de buren hoorbaar zijn. Veel reglementen hebben regels over geluidsisolatie, bijvoorbeeld bij het vervangen van vloerbedekking door tegels. Vraag de vakman naar een geluidsisolerende ondervloer of ontkoppelde leidingbevestiging, en kijk wat het huishoudelijk reglement zegt.</p>"""),
("overlast", "Overlast voor de buren beperken",
"""<p>Een badkamerrenovatie betekent een paar dagen hakken en boren. Meld de planning vooraf aan je buren en de beheerder. Houd je aan de werktijden uit het huishoudelijk reglement. Spreek af waar puin en materiaal worden opgeslagen, en of de lift beschermd moet worden. Wordt het water van het gebouw tijdelijk afgesloten, dan moet dat ruim van tevoren worden aangekondigd.</p>
<p>Woon je in een gebouw van voor 1994? Laat dan vooraf onderzoeken of er asbest in de badkamer zit. Lees meer in <a href="/kennisbank/asbest-in-badkamer/">asbest in de badkamer</a>.</p>"""),
],
"stappen_kop": "Stappenplan voor een badkamer in een VvE",
"stappen": [
("Vraag de stukken op", "Splitsingsakte, reglement en huishoudelijk reglement bij het bestuur of de beheerder."),
("Bepaal wat je raakt", "Laat de vakman aangeven of er iets verandert aan standleidingen, kanalen, vloer of muren."),
("Dien een schriftelijk verzoek in", "Met tekening, offerte en een beschrijving van het werk."),
("Wacht op toestemming", "Begin pas als je een besluit op papier hebt, en houd je aan de voorwaarden."),
("Informeer de buren", "Deel de planning en houd je aan de werktijden."),
],
"faq": [
("Heb ik altijd toestemming van de VvE nodig voor een nieuwe badkamer?", "Niet altijd. Een badkamer vernieuwen binnen je privégedeelte mag vaak zonder. Raak je gemeenschappelijke delen, zoals standleidingen, kanalen of de betonvloer, dan heb je wel toestemming nodig. Kijk in de splitsingsakte en de reglementen van jouw gebouw."),
("Mag ik mijn badkamer verplaatsen in een appartement?", "Dat raakt bijna altijd de afvoer en vaak de vloer. Vraag vooraf toestemming, want de nieuwe afvoer moet aansluiten op een gemeenschappelijke standleiding."),
("Wie betaalt bij een lekkage naar de buren?", "Dat hangt af van de oorzaak en van wie het onderdeel is. Komt het door jouw privéleiding of je badkamer, dan ben jij meestal aansprakelijk. Controleer je verzekering."),
("Waar vind ik de splitsingsakte?", "Bij het bestuur of de beheerder van de VvE, of tegen betaling bij het Kadaster."),
("Wat als de VvE nee zegt?", "Vraag waarom en kijk of het plan kan worden aangepast. Kom je er niet uit, dan kun je de kantonrechter om een oordeel vragen."),
],
"bronnen": [BW5, RIJK_VVE, UTRECHT_VVE],
"dienst": "badkamer-renoveren",
"kosten": ["badkamer-slopen", "nieuwe-badkamer"],
"tool": "/tools/renovatieplanner/",
"extra": [],
"gerelateerd": ["volgorde-badkamerrenovatie", "asbest-in-badkamer", "badkamer-ventilatie"],
},
# ---------------------------------------------------------------------------
{
"slug": "volgorde-badkamerrenovatie",
"groep": "Plannen en regels",
"titel": "Volgorde van een badkamerrenovatie: van sloop tot oplevering",
"seo_titel": "Volgorde badkamerrenovatie: stap voor stap",
"description": "In welke volgorde verloopt een badkamerrenovatie? Van plan en sloop tot leidingwerk, afdichting, tegelwerk en montage, met de wachttijden en wat je zelf regelt.",
"kort": "De vaste volgorde van een renovatie, de droogtijden die je niet kunt overslaan en wat je vooraf regelt.",
"intro": "Een badkamerrenovatie bestaat uit veel losse klussen: slopen, leidingen, elektra, afdichten, tegelen en monteren. De volgorde ligt grotendeels vast. Wie een stap overslaat of te vroeg begint, krijgt later problemen. In dit artikel lees je hoe een renovatie verloopt, waar wachttijden zitten en wat je zelf vooraf kunt regelen.",
"kort_antwoord": "De volgorde is: plan maken en spullen bestellen, slopen, leidingwerk en elektra aanleggen, wanden en vloer opbouwen, afdichten, tegelen en voegen, sanitair monteren, kitten en opleveren. Tussen sommige stappen zitten droogtijden, bijvoorbeeld van een nieuwe dekvloer of de afdichting. Een complete badkamer duurt daardoor vaak twee tot vier weken.",
"secties": [
("voorbereiding", "1. Voorbereiding: plan en bestellen",
"""<p>De belangrijkste fase gebeurt voordat er iets gesloopt wordt. Maak een plattegrond met maten. Bepaal waar het toilet, de douche, de wastafel en eventueel een bad komen. Leg de afvoer vast, want die bepaalt veel. Kies daarna de spullen en bestel ze op tijd. Sommige tegels of douchewanden hebben weken levertijd. Het is vervelend als de badkamer gesloopt is en de tegels er nog niet zijn.</p>
<p>Vraag offertes op basis van hetzelfde plan, zodat je ze kunt vergelijken. Woon je in een appartement, regel dan nu de toestemming van de VvE. Is je woning van voor 1994, laat dan ook een asbestonderzoek doen. De <a href="/tools/renovatieplanner/">renovatieplanner</a> helpt je de stappen op een rij te zetten.</p>"""),
("sloop", "2. Slopen",
"""<p>Water en stroom gaan eraf, het oude sanitair en de tegels worden verwijderd. Vaak blijkt pas dan in welke staat de ondergrond en de leidingen zijn. Houd daarom een buffer aan in tijd en geld. Het puin moet worden afgevoerd. Lees wat dit kost op de pagina over <a href="/kosten/badkamer-slopen/">badkamer slopen</a>.</p>"""),
("leidingen", "3. Leidingwerk en elektra",
"""<p>Nu worden water, afvoer en elektra aangelegd of verlegd. Dit moet klaar zijn voordat de wanden dichtgaan. Voor elektra in een badkamer gelden de veiligheidsregels uit NEN 1010, met zones rond bad en douche waar je geen gewone stopcontacten mag plaatsen. Voor waterleidingen is NEN 1006 de norm, voor afvoer NEN 3215. Komt er vloerverwarming, dan wordt die nu gelegd. Spreek af dat de leidingen worden getest op lekdichtheid voordat ze worden weggewerkt.</p>"""),
("opbouw", "4. Wanden en vloer opbouwen",
"""<p>Voorzetwanden voor een hangtoilet of inbouwkraan worden geplaatst. Een nieuwe dekvloer of egalisatie wordt aangebracht, bij een inloopdouche met afschot. Een cementdekvloer moet drogen voordat erop getegeld kan worden. Hoe lang dat duurt, hangt af van de dikte en het soort vloer. Snelle dekvloeren verkorten die tijd. Vraag de vakman hoeveel droogtijd hij rekent en waarom.</p>"""),
("afdichten", "5. Afdichten en tegelen",
"""<p>Eerst komt de afdichting: op de vloer, de douchewanden en rond doorvoeren, met kimband in de hoeken. Die moet drogen volgens het technische blad. Daarna wordt getegeld, eerst de wanden en dan de vloer, of andersom, afhankelijk van de vakman en het soort aansluiting. Na het tegelen volgt het voegen. Kijk bij de afdichting even mee voordat de tegels erop gaan, zie <a href="/kennisbank/badkamer-waterdicht-maken/">badkamer waterdicht maken</a>.</p>"""),
("zelf", "Wat je tijdens de verbouwing zelf regelt",
"""<p>Ook als een vakman alles doet, heb je zelf een paar taken. Zorg dat de badkamer en de looproute leeg zijn en dat vloeren in de gang zijn beschermd. Spreek af waar materiaal kan staan en waar de container of puinzakken komen. Wees bereikbaar voor vragen: tijdens de sloop komen soms verrassingen boven, zoals een rotte balk of een oude leiding, en dan moet je snel kiezen. Leg zulke wijzigingen schriftelijk vast, met de prijs erbij, zodat er achteraf geen discussie is over meerwerk.</p>"""),
("montage", "6. Montage, kitten en oplevering",
"""<p>Als de voegen droog zijn, worden het toilet, het wastafelmeubel, de kranen, de douchewand en de verlichting gemonteerd. Als laatste komt het kitwerk. Daarna loop je samen de badkamer door. Test alle kranen, de afvoer en de verlichting. Noteer punten die nog niet goed zijn op papier, met een afspraak wanneer ze worden opgelost. Bewaar handleidingen en productgegevens.</p>"""),
],
"stappen_kop": "De volgorde in het kort",
"stappen": [
("Plan en bestel", "Plattegrond, keuzes, offertes, toestemming en levertijden."),
("Sloop", "Oude badkamer eruit, puin afvoeren, ondergrond beoordelen."),
("Leidingen en elektra", "Water, afvoer, elektra en eventueel vloerverwarming, getest voordat alles dichtgaat."),
("Opbouw en droogtijd", "Voorzetwanden, dekvloer en afschot; laten drogen."),
("Afdichten en tegelen", "Afdichting, tegelwerk en voegen."),
("Montage en oplevering", "Sanitair, kitwerk en samen controleren."),
],
"faq": [
("Hoe lang duurt een badkamerrenovatie?", "Een complete badkamer duurt vaak twee tot vier weken, inclusief droogtijden. Een kleinere ingreep, zoals alleen nieuw sanitair op bestaande aansluitingen, kan in een paar dagen."),
("Kan ik zonder badkamer in huis blijven wonen?", "Dat kan, maar regel een alternatief om te douchen. Vraag de vakman of het toilet tussendoor bruikbaar kan blijven."),
("Wat kan ik zelf doen om kosten te besparen?", "Sommige mensen slopen zelf. Overleg dat vooraf met de vakman, en doe het niet als er mogelijk asbest in zit."),
("Waarom moet ik op de dekvloer wachten?", "Een vloer die nog te vochtig is, kan de afdichting en het tegelwerk later laten loslaten. De droogtijd hangt af van de dikte en het soort vloer."),
("Wanneer bestel ik tegels en sanitair?", "Voordat de sloop begint. Sommige producten hebben weken levertijd."),
],
"bronnen": [NEN, IPLO_VOCHT, IPLO_ASBEST],
"dienst": "badkamer-renoveren",
"kosten": ["nieuwe-badkamer", "badkamer-slopen", "vloerverwarming-badkamer"],
"tool": "/tools/renovatieplanner/",
"extra": [],
"gerelateerd": ["badkamer-waterdicht-maken", "verbouwen-in-vve", "garantie-badkamerrenovatie"],
},
# ---------------------------------------------------------------------------
{
"slug": "kleine-badkamer-indelen",
"groep": "Ontwerp en materialen",
"titel": "Kleine badkamer indelen: slimme keuzes voor weinig ruimte",
"seo_titel": "Kleine badkamer indelen: tips voor weinig ruimte",
"description": "Een kleine badkamer slim indelen: waar komen douche, toilet en wastafel, welke maten heb je nodig en hoe laat je de ruimte groter lijken met tegels, licht en spiegels.",
"kort": "Indeling, maten en trucs met licht en tegels om een kleine badkamer ruimer te laten voelen.",
"intro": "Veel Nederlandse badkamers zijn klein, soms maar een paar vierkante meter. Toch kun je er een prettige ruimte van maken. Het draait om drie dingen: een indeling die past bij de afvoer, genoeg ruimte om je te bewegen en slimme keuzes in sanitair, licht en tegels. In dit artikel lees je hoe je dat aanpakt.",
"kort_antwoord": "Begin bij de afvoer: het toilet zit vast aan de standleiding, de rest kun je meestal makkelijker verplaatsen. Kies een inloopdouche zonder bak of een douche die doorloopt in de vloer, een hangtoilet en een smal of hangend wastafelmeubel. Grote lichte tegels, een grote spiegel en goed licht laten de ruimte groter lijken.",
"secties": [
("afvoer", "Begin bij de afvoer",
"""<p>Een toilet heeft een dikke afvoer nodig met genoeg verval. Daarom staat het meestal dicht bij de standleiding. Een douche en wastafel hebben dunnere afvoeren en zijn makkelijker te verplaatsen. Bepaal dus eerst waar het toilet kan, en deel de rest daaromheen in. In een appartement kun je de standleiding niet zomaar verplaatsen, zie <a href="/kennisbank/verbouwen-in-vve/">verbouwen in een VvE</a>.</p>"""),
("maten", "Hoeveel ruimte heb je nodig?",
"""<p>Bij nieuwbouw vraagt het Besluit bouwwerken leefomgeving voor een badkamer met toilet in één ruimte minimaal 2,2 m² vloeroppervlak met een breedte van minimaal 0,9 meter. Dat is een ondergrens. Voor gebruiksgemak gelden een paar vuistregels:</p>
<ul>
<li>Houd voor een toilet en een wastafel genoeg vrije ruimte ervoor om te staan en je te bukken.</li>
<li>Een douche van 80 bij 80 centimeter is krap. 90 bij 90 of groter is prettiger, en een inloopdouche zonder bak voelt ruimer door de doorlopende vloer.</li>
<li>Let op de draairichting van de deur. Een deur die naar buiten opent of een schuifdeur wint ruimte.</li>
</ul>"""),
("sanitair", "Sanitair dat ruimte bespaart",
"""<ul class="checklist">
<li><strong>Hangtoilet met inbouwreservoir.</strong> Het reservoir zit in een voorzetwand, en de vloer onder het toilet is vrij. Dat oogt rustiger en maakt schoonmaken makkelijker.</li>
<li><strong>Smal of hangend wastafelmeubel.</strong> Er zijn meubels met een geringe diepte. Een hangend meubel laat de vloer doorlopen.</li>
<li><strong>Inloopdouche met één glazen wand.</strong> Geen deur die ruimte nodig heeft om open te gaan. Een heldere wand zonder profiel houdt het zicht vrij.</li>
<li><strong>Nissen in de wand</strong> voor shampoo en zeep, in plaats van rekjes die uitsteken.</li>
<li><strong>Inbouwkranen</strong> in de voorzetwand, zodat er niets uitsteekt.</li>
</ul>"""),
("natte-cel", "De hele badkamer als natte ruimte",
"""<p>In een heel kleine badkamer kun je de douche laten doorlopen in de hele vloer. De vloer krijgt dan afschot naar één afvoer en is in zijn geheel waterdicht gemaakt. Er is geen douchebak of drempel. Het voelt groter, maar het toilet en de wastafel kunnen nat worden van spatwater. Een gordijn of een korte glazen wand helpt. Lees wat er technisch voor nodig is in <a href="/kennisbank/inloopdouche-zonder-drempel/">inloopdouche zonder drempel</a>.</p>"""),
("vocht", "Weinig ruimte, veel vocht",
"""<p>In een kleine badkamer is de lucht na het douchen sneller verzadigd met waterdamp dan in een grote. Goede afzuiging is daarom extra belangrijk. Plaats het afzuigventiel bij voorkeur bij de douche en zorg voor een spleet onder de deur. Een spiegel met verwarming blijft na het douchen helder. Meer uitleg vind je in <a href="/kennisbank/badkamer-ventilatie/">badkamer ventileren</a>.</p>"""),
("groter", "De ruimte groter laten lijken",
"""<ul>
<li><strong>Lichte kleuren</strong> op wanden en vloer weerkaatsen licht.</li>
<li><strong>Grote tegels</strong> geven minder voegen en daardoor minder onrust. Dezelfde tegel op vloer en wand laat de grenzen vervagen.</li>
<li><strong>Een grote spiegel</strong> over de hele breedte van de wastafel verdubbelt de ruimte optisch.</li>
<li><strong>Goed licht</strong>: een plafondlamp plus licht bij de spiegel. Let op de veiligheidszones uit NEN 1010 bij bad en douche.</li>
<li><strong>Weinig losse spullen</strong>: berging in een kast boven het toilet of in nissen.</li>
</ul>
<p>Zoek je een stijl die goed werkt in een kleine ruimte? Probeer de <a href="/tools/stijlkiezer/">stijlkiezer</a>.</p>"""),
],
"stappen_kop": "Zo pak je de indeling aan",
"stappen": [
("Meet alles op", "Lengte, breedte, hoogte, ramen, deur en de plek van de standleiding."),
("Plaats het toilet eerst", "Zo dicht mogelijk bij de afvoer."),
("Kies de douche", "Een inloopdouche of een doorlopende natte vloer bespaart ruimte."),
("Teken het op schaal", "Teken de vrije ruimte voor elk onderdeel erbij. Op ruitjespapier of met een eenvoudig tekenprogramma."),
("Laat het checken", "Vraag een vakman of de afvoer en het afschot passen bij je plan."),
],
"faq": [
("Wat is de minimale grootte van een badkamer?", "Voor nieuwbouw vraagt het Bbl voor een badkamer met toilet in één ruimte minimaal 2,2 m² bij een breedte van 0,9 meter. In bestaande woningen kom je ook kleinere badkamers tegen."),
("Past een bad in een kleine badkamer?", "Soms wel, bijvoorbeeld een kort bad of een bad met douchewand erboven. Je verliest dan wel de ruimte van een inloopdouche."),
("Is een hangtoilet beter voor een kleine badkamer?", "Het oogt rustiger en de vloer is makkelijker schoon te maken. Het inbouwreservoir zit in een voorzetwand van zo'n 15 tot 20 centimeter diep, dus het wint vooral ruimte onder het toilet."),
("Welke kleur tegels maakt een badkamer groter?", "Lichte kleuren en grote formaten met weinig voegen laten een ruimte groter lijken."),
("Kan ik het toilet verplaatsen?", "Dat kan, als de afvoer met genoeg verval naar de standleiding kan lopen. Laat een vakman dit beoordelen."),
],
"bronnen": [IPLO_BADRUIMTE, NEN],
"dienst": "badkamer-installeren",
"kosten": ["nieuwe-badkamer", "toilet-renoveren"],
"tool": "/tools/stijlkiezer/",
"extra": [("/badkamerspullen/wastafelmeubel-kiezen/", "Wastafelmeubel kiezen", "Maten en materialen voor een wastafelmeubel.")],
"gerelateerd": ["inloopdouche-zonder-drempel", "tegels-kiezen", "badkamerstijlen"],
},
# ---------------------------------------------------------------------------
{
"slug": "asbest-in-badkamer",
"groep": "Plannen en regels",
"titel": "Asbest in de badkamer: herkennen, laten onderzoeken en verwijderen",
"seo_titel": "Asbest in de badkamer: waar zit het en wat doe je?",
"description": "In woningen van voor 1994 kan asbest in de badkamer zitten, bijvoorbeeld in vloerzeil, kit of plaatmateriaal. Lees waar het zit, wat je zelf mag en wanneer een bedrijf moet.",
"kort": "Waar asbest in een oude badkamer kan zitten, wanneer je het laat onderzoeken en wat je zelf mag verwijderen.",
"intro": "Asbest werd tot begin jaren negentig veel gebruikt in de bouw. In een oude badkamer kan het op onverwachte plekken zitten. Zolang het heel blijft, is het meestal geen probleem. Maar bij slopen komen vezels vrij, en die zijn schadelijk als je ze inademt. Voordat je een oude badkamer sloopt, moet je dus weten of er asbest in zit.",
"kort_antwoord": "Sinds 1 juli 1993 is het gebruik van asbest in Nederland verboden. Woningen van voor 1994 gelden daarom als asbestverdacht. Laat bij een badkamer uit die tijd vóór de sloop onderzoeken of er asbest in zit. Een particulier mag maar heel beperkt zelf asbest verwijderen; vloerzeil met een asbesthoudende onderlaag of gelijmd materiaal laat je verwijderen door een gecertificeerd bedrijf.",
"secties": [
("waarom", "Waarom asbest een risico is",
"""<p>Asbest bestaat uit kleine vezels. Als asbesthoudend materiaal breekt, wordt geschuurd of geboord, komen die vezels vrij. Wie ze inademt, loopt kans op ernstige longziekten, soms tientallen jaren later. Daarom heeft de overheid strikte regels voor het verwijderen.</p>
<p>In Nederland geldt sinds 1 juli 1993 een verbod op het gebruik van asbest. Omdat materialen daarna nog werden verwerkt, worden gebouwen van voor 1994 als asbestverdacht gezien. Dat betekent niet dat er asbest in zit, wel dat je het moet uitsluiten voordat je sloopt.</p>"""),
("waar", "Waar kan asbest zitten in een badkamer?",
"""<ul class="checklist">
<li><strong>Vloerzeil (vinyl)</strong> met een onderlaag van asbestvilt. Die onderlaag is niet hechtgebonden en daardoor extra riskant.</li>
<li><strong>Vloertegels</strong> van vinyl of kunststof, en de lijm eronder.</li>
<li><strong>Plaatmateriaal</strong> achter tegels, rond een bad of in een verlaagd plafond.</li>
<li><strong>Ventilatiekanalen en rookgasafvoer</strong> van asbestcement, bijvoorbeeld van een oude geiser.</li>
<li><strong>Afvoerleidingen</strong> van asbestcement, vooral standleidingen in oudere gebouwen.</li>
<li><strong>Kit en vensterbanken</strong> in sommige gevallen.</li>
</ul>
<p>Aan het uiterlijk zie je niet of iets asbest bevat. Alleen onderzoek in een laboratorium geeft zekerheid.</p>"""),
("onderzoek", "Laten onderzoeken",
"""<p>Er zijn twee manieren:</p>
<ul>
<li><strong>Een monster laten onderzoeken.</strong> Bij twijfel over één materiaal kun je een stukje laten testen door een geaccrediteerd laboratorium.</li>
<li><strong>Een asbestinventarisatie.</strong> Een gecertificeerd bureau onderzoekt de hele ruimte en schrijft een rapport. Dat is nodig als er asbest gevonden wordt dat een bedrijf moet verwijderen, en de gemeente kan erom vragen bij de sloopmelding.</li>
</ul>
<p>Doe dit vóórdat de sloop begint. Komt de vakman tijdens het slopen verdacht materiaal tegen, dan moet het werk stoppen tot duidelijk is wat het is.</p>"""),
("zelf", "Wat mag je zelf verwijderen?",
"""<p>Particulieren mogen in bepaalde gevallen zelf asbest verwijderen uit hun eigen woning. Volgens de spelregels van de overheid gelden dan alle volgende voorwaarden:</p>
<ul>
<li>maximaal 35 m² asbesthoudend materiaal per gebouw, in totaal;</li>
<li>plaatmateriaal alleen als het geschroefd is, in zijn geheel los kan en niet kapot of verweerd is;</li>
<li>vloertegels en vloerbedekking alleen als ze <strong>niet gelijmd</strong> zijn, in zijn geheel los komen en hechtgebonden zijn;</li>
<li>je meldt de sloop vooraf bij de gemeente via het Omgevingsloket;</li>
<li>je verpakt het luchtdicht in stevig, doorzichtig plastic met het woord "Asbest" erop en brengt het naar de milieustraat.</li>
</ul>
<p>Niet zelf mag je onder meer: gelijmde tegels of vloerbedekking, de onderlaag van oud vloerzeil, gespijkerd of gelijmd plaatmateriaal en leidingen die vastzitten aan het gebouw, zoals een rioolpijp. Dat doet een gecertificeerd asbestverwijderingsbedrijf. In een badkamer betekent dat in de praktijk: de meeste asbestvondsten laat je door een bedrijf verwijderen.</p>"""),
("planning", "Wat betekent het voor je planning?",
"""<p>Een asbestinventarisatie, de melding bij de gemeente en de sanering kosten tijd. Reken op een paar weken extra voordat de gewone renovatie kan beginnen. Neem het asbestonderzoek daarom op in de eerste fase van je plan, zie <a href="/kennisbank/volgorde-badkamerrenovatie/">volgorde van een badkamerrenovatie</a>. Woon je in een appartement, overleg dan ook met de VvE: asbesthoudende standleidingen zijn meestal gemeenschappelijk.</p>"""),
],
"stappen_kop": "Stappen bij een oude badkamer",
"stappen": [
("Kijk naar het bouwjaar", "Is de woning, of de badkamer, van voor 1994? Dan geldt hij als asbestverdacht."),
("Laat onderzoeken", "Een monster of een volledige asbestinventarisatie door een gecertificeerd bureau."),
("Meld de sloop", "Bij asbest meld je de sloop vooraf bij de gemeente via het Omgevingsloket."),
("Laat het verwijderen", "Door een gecertificeerd bedrijf, of zelf als je aan alle voorwaarden voldoet."),
("Dan pas slopen", "De gewone renovatie begint als het asbest weg is."),
],
"faq": [
("Sinds wanneer is asbest verboden?", "Het gebruik van asbest is in Nederland verboden sinds 1 juli 1993. Gebouwen van voor 1994 gelden als asbestverdacht."),
("Kan ik zien of iets asbest is?", "Nee. Alleen onderzoek door een geaccrediteerd laboratorium geeft zekerheid."),
("Mag ik oud vloerzeil zelf verwijderen?", "Niet als er een asbesthoudende onderlaag onder zit of als het gelijmd is. Dat moet een gecertificeerd bedrijf doen."),
("Is asbest gevaarlijk als ik er niets mee doe?", "Hecht gebonden asbest dat heel is, geeft weinig vezels af. Het risico ontstaat bij breken, boren, schuren of slopen."),
("Moet ik asbest melden bij de gemeente?", "Als je het laat verwijderen of zelf verwijdert, moet je de sloop vooraf melden via het Omgevingsloket."),
],
"bronnen": [ONDERNEMERSPLEIN_ASBEST, IPLO_ASBEST_NL, IPLO_ASBEST, RIJK_ASBEST],
"dienst": "badkamer-renoveren",
"kosten": ["badkamer-slopen"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["volgorde-badkamerrenovatie", "verbouwen-in-vve", "garantie-badkamerrenovatie"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamerstijlen",
"groep": "Ontwerp en materialen",
"titel": "Badkamerstijlen: van modern en landelijk tot industrieel",
"seo_titel": "Badkamerstijlen: welke stijl past bij jou?",
"description": "Modern, landelijk, industrieel, Scandinavisch of klassiek: de kenmerken van populaire badkamerstijlen, welke materialen erbij passen en wat ze betekenen voor onderhoud.",
"kort": "De kenmerken van vijf badkamerstijlen, de materialen die erbij horen en wat ze vragen aan onderhoud.",
"intro": "Een stijl helpt je keuzes te maken. Wie weet wat hij mooi vindt, kiest sneller tegels, kranen en een wastafelmeubel die bij elkaar passen. In dit artikel bespreken we vijf veelgekozen stijlen. Per stijl lees je de kenmerken, de materialen en waar je op let bij onderhoud. De voorbeelden zijn beschrijvingen; er zijn geen merken aan gekoppeld.",
"kort_antwoord": "Een stijl wordt bepaald door kleur, materiaal en vormen. Modern is strak en rustig, landelijk warm met hout en natuurlijke tinten, industrieel stoer met beton en zwart metaal, Scandinavisch licht en eenvoudig, en klassiek met details en sierlijke vormen. Kies ook op onderhoud: matte en ruwe oppervlakken tonen kalk en vuil anders dan glanzende.",
"secties": [
("modern", "Modern en minimalistisch",
"""<p>Strakke lijnen, weinig details en een rustig kleurenpalet van wit, grijs, beige of zwart. Grote tegels met smalle voegen, een hangtoilet, een zwevend wastafelmeubel en een inloopdouche met een heldere glazen wand. Kranen zitten vaak in de wand.</p>
<p><strong>Onderhoud:</strong> weinig randen en voegen maken schoonmaken makkelijk. Glanzende zwarte oppervlakken laten wel snel kalkvlekken zien.</p>"""),
("landelijk", "Landelijk en warm",
"""<p>Natuurlijke tinten, houtlook en materialen met structuur. Denk aan tegels met een houtnerf of een handgemaakte uitstraling, een wastafelmeubel in eiken of een lichte houtkleur, en kranen in mat goud of brons. Soms met een vrijstaand bad als blikvanger.</p>
<p><strong>Onderhoud:</strong> echt hout in een natte ruimte vraagt bescherming en goede ventilatie. Houtlooktegels geven hetzelfde beeld zonder dat onderhoud.</p>"""),
("industrieel", "Industrieel en stoer",
"""<p>Betonlook, zwart metaal en ruwe materialen. Grote grijze tegels of een naadloze wand, een douchewand met zwarte profielen, zichtbare leidingen of opbouwkranen in mat zwart. Vaak gecombineerd met hout om het niet te koel te maken.</p>
<p><strong>Onderhoud:</strong> mat zwart laat kalk en vingerafdrukken zien. Bij hard water helpt het om de douchewand na gebruik droog te trekken. Een naadloze wandafwerking vraagt een systeem dat geschikt is voor natte ruimten.</p>"""),
("scandinavisch", "Scandinavisch en licht",
"""<p>Licht, eenvoudig en functioneel. Witte of lichtgrijze tegels, licht hout, accenten in zacht groen of blauw. Weinig spullen in beeld, veel daglicht en eenvoudige vormen. Werkt goed in kleine badkamers, omdat het de ruimte groter laat lijken.</p>
<p><strong>Onderhoud:</strong> witte voegen kunnen verkleuren. Een lichtgrijze voegkleur of epoxyvoeg blijft langer mooi.</p>"""),
("klassiek", "Klassiek en retro",
"""<p>Sierlijke vormen en details. Metrotegels in een halfsteensverband, een vloer met een patroontegel, een staande wastafel of een meubel met panelen, en kranen met kruisgrepen in chroom of messing. Een vrijstaand bad op pootjes past er goed bij.</p>
<p><strong>Onderhoud:</strong> veel voegen en details betekent meer schoonmaakwerk. Patroontegels van cementtegels moeten worden geïmpregneerd; keramische patroontegels zijn makkelijker.</p>"""),
("budget", "Stijl, budget en de rest van het huis",
"""<p>Een stijl zegt weinig over de prijs. Een moderne badkamer kan eenvoudig zijn, maar met inbouwkranen, grote tegels en een glazen wand zonder profiel loopt het werk wel op. Grote formaten vragen een vlakke ondergrond en meer werkuren per vierkante meter. Een klassieke badkamer met patroontegels vraagt veel snijwerk. Vraag de vakman daarom welke keuzes in jouw stijl het meeste werk geven, en waar je met een eenvoudiger alternatief hetzelfde beeld krijgt.</p>
<p>Kijk ook naar de rest van je huis. Een badkamer die aansluit bij de vloer, de deuren en de kleuren in de gang voelt als een geheel. Wil je over een paar jaar verhuizen, dan is een neutrale basis vaak verstandig: die spreekt meer kopers aan. Op de <a href="/kosten/nieuwe-badkamer/">kostenpagina over een nieuwe badkamer</a> lees je wat de prijs vooral bepaalt.</p>"""),
("combineren", "Hoe kies je?",
"""<p>Verzamel voorbeelden van badkamers die je mooi vindt en kijk wat ze gemeen hebben: kleur, materiaal of vorm. Kies daarna één basis en hooguit één of twee accenten. Te veel verschillende materialen geeft onrust, zeker in een kleine ruimte. Houd ook rekening met de rest van het huis en hoe lang je er wilt blijven wonen. Een rustige basis met wisselbare accenten, zoals handdoeken en accessoires, veroudert minder snel.</p>
<p>Twijfel je nog, doe dan de <a href="/tools/stijlkiezer/">stijlkiezer</a>. Die geeft op basis van een paar vragen een richting.</p>"""),
],
"stappen_kop": "Checklist voor je stijlkeuze",
"stappen": [
("Verzamel voorbeelden", "Bewaar beelden van badkamers die je aanspreken en zoek de overeenkomsten."),
("Kies een basis", "Eén kleurenpalet en één hoofdmateriaal voor vloer en wanden."),
("Kies accenten", "Hooguit één of twee, bijvoorbeeld de kleur van de kranen of een wand met een andere tegel."),
("Denk aan onderhoud", "Mat zwart, wit en natuursteen vragen meer aandacht bij hard water."),
("Check de ruimte", "Lichte stijlen werken het best in kleine badkamers."),
],
"faq": [
("Welke badkamerstijl blijft lang mooi?", "Een rustige basis in neutrale kleuren met wisselbare accenten veroudert het minst snel. Uitgesproken kleuren en materialen zijn meer modegevoelig."),
("Welke stijl past bij een kleine badkamer?", "Lichte stijlen, zoals Scandinavisch of modern in lichte tinten, laten een kleine ruimte groter lijken."),
("Zijn zwarte kranen lastig in onderhoud?", "Ze laten kalk en vingerafdrukken sneller zien dan chroom. Droog ze na gebruik af en gebruik geen schurende middelen."),
("Kan ik echt hout in de badkamer gebruiken?", "Dat kan buiten de natte zone, met goede bescherming en ventilatie. Houtlooktegels geven een vergelijkbaar beeld zonder onderhoud."),
("Kan ik stijlen combineren?", "Ja, bijvoorbeeld industrieel met warm hout. Houd één stijl als basis en gebruik de andere als accent."),
],
"bronnen": [RIJK_VENTILEREN],
"dienst": "badkamer-renoveren",
"kosten": ["nieuwe-badkamer", "tegelzetter-per-m2"],
"tool": "/tools/stijlkiezer/",
"extra": [("/badkamerspullen/kranen-kiezen/", "Kranen kiezen", "Soorten kranen en afwerkingen."),
          ("/badkamerspullen/bad-of-douche/", "Bad of douche?", "De voor- en nadelen naast elkaar.")],
"gerelateerd": ["tegels-kiezen", "kleine-badkamer-indelen", "volgorde-badkamerrenovatie"],
},
]
