# -*- coding: utf-8 -*-
"""Kennisbank ronde 2: acht extra artikelen voor /kennisbank/{slug}/.

Zelfde opbouw als badkamer_kennis_artikelen.py; badkamer_kennis.py voegt beide lijsten samen.

Feitencontrole (november 2026, met WebSearch en WebFetch):
- Huurwoning: Rijksoverheid, "Mag ik mijn huurwoning verbouwen of renoveren?": voor een aanpassing
  van de badkamer altijd toestemming van de verhuurder; kleine aanpassingen die je zonder veel
  kosten terugdraait niet; verhuurder reageert binnen 8 weken; weigeren mag als de woning slechter
  verhuurbaar wordt of in waarde daalt; daarna kan de huurder naar de rechter (BW 7:215).
  Rijksoverheid, "Hoe krijg ik tijdelijke huurverlaging bij ernstige onderhoudsgebreken?": schriftelijk
  melden, 6 weken hersteltermijn, daarna Huurcommissie; die kan herstel niet afdwingen (dat kunnen de
  gemeente en de rechter); lekkage, vocht en schimmel zijn voorbeelden van gebreken.
  Rijksoverheid, "Mag ik een traplift of verhoogd toilet laten plaatsen?": bij Wmo/Wlz-vergoeding
  hoeft de aanpassing bij verhuizing niet terug.
- Wmo: Rijksoverheid, "Vergoeding voor woningaanpassing": via het Wmo-loket of sociaal wijkteam
  van de gemeente; soms een eigen bijdrage (rekenhulp van het CAK); Wlz-indicatie kan ook; sommige
  gemeenten geven een verhuisvergoeding. Bewust geen bedragen: die verschillen per gemeente en jaar.
- Levensloopbestendig: een draaicirkel van 150 cm en een vrije doorgang van 85 tot 90 cm worden in
  gemeentelijke verordeningen en praktijkgidsen vaak als richtmaat genoemd; er is geen bindende norm
  voor bestaande woningen gevonden. Daarom als richtmaat beschreven.
- Waterhardheid: Waternet 7,8 °dH (1,40 mmol/l), landelijk gemiddelde ongeveer 8 °dH, "hard" pas vanaf
  12 °dH (waternet.nl); PWN gemiddeld 7,9 °dH (pwn.nl); Dunea ongeveer 1,42 mmol/l, circa 7,9 °dH,
  wettelijk minimum 1 mmol/l, na een ontharder in de binneninstallatie niet lager dan 5,6 °dH
  (dunea.nl); Brabant Water gemiddeld 5,0 tot 11,2 °dH per plaats, Helmond 10,81 °dH (brabantwater.nl);
  Vitens: rond 8 °dH, Consumentenbond vindt een ontharder niet nodig, risico's en keurmerk (vitens.nl).
- Lekkage opsporen met de watermeter: werkwijze van Dunea, Evides, Brabant Water en Waternet.
- Verzekering: opstal dekt het huis (vloeren, wanden, leidingen), inboedel de spullen; dekking hangt af
  van oorzaak en voorwaarden (Consumentenbond, waterschade). Geschillen: Kifid.
- Schimmel: Milieu Centraal, "Schimmels in huis": alleen middelen met Ctgb-toelating, geen
  zelfgemaakte mengsels van soda, bleek en chloor, niet over schimmel heen verven, terugkerende
  schimmel heeft vaak een bouwkundige oorzaak. RIVM, GGD-richtlijn schimmel.
- Vloerverwarming: Milieu Centraal: werkt meestal rond 40 °C, soms 30 °C; badkamervloer maximaal
  33 °C; traag, dus geen nachtverlaging; tegels ideaal; elektrische vloerverwarming is niet zuinig,
  kies voor warm water. Lagetemperatuurverwarming: radiatoren met twee of drie platen en lamellen zijn
  meestal geschikt; Verwarmingstest op 50 °C.
- Zolder: Rijksoverheid en IPLO, vergunningvrij bouwen (Bbl artikel 2.29) en dakkapel; wijzigingen aan
  de draagconstructie altijd laten beoordelen. Woonvloeren worden volgens NEN-EN 1991-1-1 meestal
  ontworpen op een opgelegde belasting van 1,75 kN/m² (klasse A); zoldervloeren soms lager.
- Microcement: geen overheidsbron; Werkspot (vakartikel) en technische bladen: dunne lagen van
  ongeveer 1 tot 3 mm, sealer nodig, onder natte zones een afdichting. Wettelijke ondergrens voor
  vochtwering: Bbl artikel 3.65 (IPLO).
Prijzen staan bewust niet in de artikelen; daarvoor linken we naar de kostenpagina's.
"""

from badkamer_kennis_artikelen import BBL, IPLO_VENTILATIE, IPLO_VOCHT, RIJK_VENTILEREN, VHN_SCHIMMEL, NEN

RIJK_HUUR_VERBOUWEN = ("Rijksoverheid, Mag ik mijn huurwoning verbouwen of renoveren?",
                       "https://www.rijksoverheid.nl/onderwerpen/woning-huren/vraag-en-antwoord/mag-ik-mijn-huurwoning-verbouwen-of-renoveren")
RIJK_HUUR_GEBREKEN = ("Rijksoverheid, Hoe krijg ik tijdelijke huurverlaging bij ernstige onderhoudsgebreken?",
                      "https://www.rijksoverheid.nl/onderwerpen/woning-huren/vraag-en-antwoord/hoe-krijg-ik-tijdelijke-huurverlaging-bij-ernstige-onderhoudsgebreken")
RIJK_HUUR_KOSTEN = ("Rijksoverheid, Welke kosten zijn voor de huurder en welke voor de verhuurder?",
                    "https://www.rijksoverheid.nl/onderwerpen/woning-huren/vraag-en-antwoord/welke-kosten-zijn-voor-de-huurder-en-welke-voor-de-verhuurder")
RIJK_TRAPLIFT = ("Rijksoverheid, Mag ik een traplift of verhoogd toilet laten plaatsen?",
                 "https://www.rijksoverheid.nl/onderwerpen/woning-huren/vraag-en-antwoord/mag-ik-een-traplift-of-verhoogd-toilet-laten-plaatsen")
RIJK_WMO = ("Rijksoverheid, Vergoeding voor woningaanpassing (Wmo en Wlz)",
            "https://www.rijksoverheid.nl/onderwerpen/zorg-en-ondersteuning-thuis/vraag-en-antwoord/vergoeding-voor-woningaanpassing")
RIJK_WMO_BIJDRAGE = ("Rijksoverheid, Eigen bijdrage Wmo 2015",
                     "https://www.rijksoverheid.nl/onderwerpen/zorg-en-ondersteuning-thuis/vraag-en-antwoord/eigen-bijdrage-wmo-2015")
HUURCOMMISSIE = ("Huurcommissie, informatie over gebreken en huurprijs", "https://www.huurcommissie.nl/")
JURIDISCH_LOKET = ("Het Juridisch Loket, gratis juridisch advies", "https://www.juridischloket.nl/")
MC_SCHIMMEL = ("Milieu Centraal, Schimmels in huis", "https://www.milieucentraal.nl/huis-en-tuin/schoonmaken/schimmels-in-huis/")
MC_VENTILEREN = ("Milieu Centraal, Woning ventileren", "https://www.milieucentraal.nl/energie-besparen/ventilatie/woning-ventileren/")
RIVM_SCHIMMEL = ("RIVM, GGD-richtlijn medische milieukunde: schimmel", "https://www.rivm.nl/bibliotheek/rapporten/609300022.pdf")
MC_VLOERVERWARMING = ("Milieu Centraal, Vloerverwarming: zuinig verwarmen op lage temperatuur",
                      "https://www.milieucentraal.nl/energie-besparen/duurzaam-verwarmen-en-koelen/vloerverwarming/")
MC_LTV = ("Milieu Centraal, Lagetemperatuurverwarming (ltv)",
          "https://www.milieucentraal.nl/energie-besparen/energiezuinig-huis/energiezuinig-verwarmen-en-warm-water/lage-temperatuur-verwarming-ltv/")
WATERNET_HARDHEID = ("Waternet, Hardheid van het drinkwater",
                     "https://www.waternet.nl/en/service-and-contact/tap-water/tap-water-hardness/")
PWN_HARDHEID = ("PWN, Wat is de hardheid van het water?", "https://www.pwn.nl/veelgestelde-vragen/wat-de-hardheid-van-het-water")
DUNEA_HARDHEID = ("Dunea, Waterhardheid", "https://www.dunea.nl/drinkwater/waterhardheid")
BRABANTWATER_HARDHEID = ("Brabant Water, Waterkwaliteit opvragen (voorbeeld Helmond)",
                         "https://www.brabantwater.nl/drinkwater/waterkwaliteit/waterkwaliteit-opvragen/helmond")
VITENS_ONTHARDERS = ("Vitens, Waterontharders", "https://www.vitens.nl/service/waterkwaliteit/waterhardheid/waterontharders")
DUNEA_LEK = ("Dunea, Check op lek", "https://www.dunea.nl/checkoplek")
EVIDES_LEK = ("Evides, Lekkage opsporen", "https://www.evides.nl/storing-onderhoud/lekkage-opsporen")
WATERNET_LEK = ("Waternet, Wat doe ik bij lekkage?", "https://www.waternet.nl/service-en-contact/problemen-met-water/lekkage/")
CB_WATERSCHADE = ("Consumentenbond, Waterschade en je woonverzekering", "https://www.consumentenbond.nl/woonverzekering/waterschade")
KIFID = ("Kifid, Klachteninstituut Financiële Dienstverlening", "https://www.kifid.nl/")
RIJK_VERGUNNINGVRIJ = ("Rijksoverheid, Vergunningvrij bouwen en verbouwen",
                       "https://www.rijksoverheid.nl/onderwerpen/bouwregelgeving/checken-of-vergunning-nodig-is-voor-ver-bouwen/vergunningvrij-bouwen-en-verbouwen")
IPLO_WONING = ("IPLO, Bouwregels voor woningen (vergunningvrij bouwen, Bbl artikel 2.29)",
               "https://iplo.nl/thema/praktijksituaties/woning/bouwregels/")
IPLO_DAKKAPEL = ("IPLO, Dakkapel: vergunning of melding", "https://iplo.nl/thema/bouw/bouwen-vergunning-melding/dakkapel/")
WERKSPOT_MICROCEMENT = ("Werkspot, Microcement in de badkamer: voor- en nadelen",
                        "https://www.werkspot.nl/badkamer-sanitair/artikelen/microcement-in-de-badkamer")


ARTIKELEN2 = [
# ---------------------------------------------------------------------------
{
"slug": "microcement-badkamer",
"groep": "Ontwerp en materialen",
"titel": "Microcement in de badkamer: voor- en nadelen",
"seo_titel": "Microcement in de badkamer: voor- en nadelen",
"description": "Microcement geeft een badkamer zonder voegen. Lees hoe het wordt aangebracht, waarom er een afdichting onder moet, wat het onderhoud vraagt en wanneer tegels beter passen.",
"kort": "Een naadloze wand en vloer: hoe microcement werkt, wat eronder moet en wanneer tegels de betere keus zijn.",
"intro": "Microcement is populair in badkamers. Het geeft een strak, naadloos oppervlak zonder voegen, in een betonlook of een rustige kleur. Het kan vaak over bestaande tegels heen, wat sloopwerk scheelt. Maar het is geen wondermiddel. De laag is dun en gevoelig voor een slechte ondergrond, en zonder goede afdichting en sealer is ook microcement niet waterdicht. In dit artikel lees je hoe het werkt en waar je op let.",
"kort_antwoord": "Microcement is een dunne laag van cement, kunsthars en fijne vulstof, in een paar lagen aangebracht en afgewerkt met een sealer. Het is mooi en naadloos, maar niet vanzelf waterdicht: in de douche hoort er een afdichting onder. Het vraagt een stevige, droge ondergrond, een ervaren verwerker en af en toe een nieuwe sealerlaag.",
"secties": [
("wat", "Wat is microcement?",
"""<p>Microcement is een mengsel van cement, kunsthars (polymeren) en zeer fijne vulstoffen. Het wordt met een spaan in dunne lagen opgezet, meestal samen niet meer dan een paar millimeter. Na het schuren en afwerken komt er een transparante sealer op. Die sealer maakt het oppervlak minder gevoelig voor water, vlekken en zeep.</p>
<p>Je hoort ook de namen microbeton en beton ciré. Dat zijn vergelijkbare producten met een iets andere samenstelling of korrel. Welke naam een vakman ook gebruikt: vraag welk systeem het is en vraag naar het technische blad. Daarin staat uit welke lagen het bestaat en hoe dik elke laag moet zijn.</p>"""),
("voordelen", "De voordelen",
"""<ul class="checklist">
<li><strong>Geen voegen.</strong> Er is geen voeg die vuil wordt of zwart kleurt. Dat oogt rustig, ook in een kleine badkamer.</li>
<li><strong>Over bestaande tegels.</strong> Liggen de oude tegels nog vast en vlak, dan kan microcement er vaak overheen. Dat scheelt sloopwerk, puin en tijd.</li>
<li><strong>Dun.</strong> De laag is zo dun dat deuren en drempels meestal niet aangepast hoeven te worden.</li>
<li><strong>Doorlopend.</strong> Vloer, wanden en zelfs een wastafelblad of nis kunnen in één materiaal worden afgewerkt.</li>
</ul>"""),
("nadelen", "De nadelen",
"""<p>Microcement is handwerk. Het resultaat hangt sterk af van de verwerker: wolken, spaanslagen en kleurverschil horen bij het materiaal, maar een onervaren verwerker maakt er vlekken of scheuren van. Bekijk daarom werk dat iemand eerder deed.</p>
<p>Het materiaal kan krassen en scheuren als de ondergrond werkt. Een houten vloer die doorbuigt of een naad tussen twee bouwplaten zie je na verloop van tijd terug. Ook is een glad afgewerkte vloer nat soms glad. Vraag welke antislipwaarde het complete systeem heeft, inclusief sealer, en kies voor de douchevloer een stroevere afwerking.</p>
<p>Tot slot is herstel lastig. Een beschadigde tegel vervang je; een plek in microcement bijwerken zonder dat je het ziet, is moeilijk.</p>"""),
("waterdicht", "Is microcement waterdicht?",
"""<p>Niet vanzelf. Fabrikanten noemen het waterbestendig dankzij de sealer, maar in de douche staat het oppervlak dagelijks onder water. Kleine haarscheurtjes of een versleten sealer laten dan water door naar de ondergrond. Daarom hoort er in de natte zone een afdichtingslaag onder het microcement, net als onder tegels. Lees meer in ons artikel over <a href="/kennisbank/badkamer-waterdicht-maken/">een badkamer waterdicht maken</a>.</p>
<p>De wettelijke ondergrens uit het Besluit bouwwerken leefomgeving geldt ook hier: in een bestaande woning moeten de vloer en de wanden tot 1 meter hoogte in de badruimte waterafstotend zijn (artikel 3.65). Rond de douche is meer nodig dan dat minimum.</p>"""),
("ondergrond", "De ondergrond en de voorbereiding",
"""<p>De ondergrond moet stevig, droog, vlak en schoon zijn. Losse of holle tegels gaan eerst weg. Over tegels komt meestal een hechtprimer en vaak een wapeningsgaas in de eerste laag, zodat de voegen niet doortekenen. Ook leidingen, afvoer en eventuele vloerverwarming moeten klaar zijn voordat het werk begint. Daarna volgen meerdere lagen met droogtijd ertussen, dus reken op een badkamer die een aantal dagen niet te gebruiken is.</p>"""),
("onderhoud", "Onderhoud",
"""<p>Maak microcement schoon met een milde, pH-neutrale reiniger. Schurende middelen en agressieve ontkalkers tasten de sealer aan. Droog de douchewand na gebruik af, zeker bij hard water, want kalkvlekken vallen op een egaal oppervlak eerder op. Afhankelijk van het gebruik heeft de sealer na een aantal jaren een nieuwe laag nodig. Vraag de verwerker hoe vaak dat bij zijn systeem nodig is en welke middelen je wel en niet gebruikt. Meer over kalk lees je in het artikel over <a href="/kennisbank/kalk-en-waterhardheid/">kalk en waterhardheid</a>.</p>"""),
],
"stappen_kop": "Checklist voordat je kiest",
"stappen": [
("Vraag het technische blad", "Laat zien uit welke lagen het systeem bestaat, hoe dik elke laag is en welke sealer erop komt."),
("Vraag naar de afdichting", "Laat in de offerte zetten welke afdichting onder de douchezone komt."),
("Laat de ondergrond beoordelen", "Losse tegels, een werkende houten vloer of vocht in de muur moeten eerst opgelost zijn."),
("Bekijk eerder werk", "Vraag foto's of een adres van eerder werk, het liefst een badkamer die al een paar jaar in gebruik is."),
("Spreek onderhoud af", "Vraag welke schoonmaakmiddelen geschikt zijn en wanneer de sealer vernieuwd moet worden."),
],
"faq": [
("Kan microcement over oude tegels?", "Vaak wel, als de tegels vast en vlak liggen. Er komt eerst een hechtprimer op en meestal een wapening, zodat de voegen niet doortekenen."),
("Is microcement geschikt voor een inloopdouche?", "Ja, met een afdichting onder de laag, een goede sealer en een stroeve afwerking op de vloer. De vloer moet ook het juiste afschot naar de afvoer hebben."),
("Gaat microcement scheuren?", "Dat kan als de ondergrond werkt, bijvoorbeeld bij een houten vloer of naden tussen platen. Een stevige ondergrond en een wapeningsgaas verkleinen die kans."),
("Is microcement goedkoper dan tegels?", "Niet per se. Het materiaal is dun, maar het werk kost veel uren. Vergelijk offertes voor dezelfde oppervlakte en let op wat er aan voorbereiding in zit."),
("Hoe maak ik microcement schoon?", "Met een milde, pH-neutrale reiniger en een zachte doek. Gebruik geen schuurmiddel of sterke ontkalker, want die tasten de sealer aan."),
],
"bronnen": [IPLO_VOCHT, BBL, WERKSPOT_MICROCEMENT],
"dienst": "badkamer-renoveren",
"kosten": ["tegelzetter-per-m2", "nieuwe-badkamer"],
"tool": "/tools/stijlkiezer/",
"extra": [("/badkamerspullen/badkamertegels-kopen/", "Badkamertegels kopen", "Liever toch tegels? Waar je op let bij het kopen.")],
"gerelateerd": ["badkamer-waterdicht-maken", "tegels-kiezen", "badkamerstijlen"],
},
# ---------------------------------------------------------------------------
{
"slug": "levensloopbestendige-badkamer",
"groep": "Wonen en situatie",
"titel": "Levensloopbestendige badkamer: veilig en makkelijk, ook later",
"seo_titel": "Levensloopbestendige badkamer: tips en Wmo",
"description": "Een badkamer die meegaat als je ouder wordt of minder mobiel bent. Lees welke maten en voorzieningen helpen en hoe je via de Wmo bij je gemeente een aanpassing aanvraagt.",
"kort": "Drempelvrij, genoeg ruimte en steun waar je die nodig hebt. Plus: hoe een Wmo-aanvraag bij de gemeente werkt.",
"intro": "Een levensloopbestendige badkamer kun je blijven gebruiken als je ouder wordt, een blessure hebt of minder goed ter been bent. Dat hoeft er niet uit te zien als een ziekenhuisbadkamer. Veel keuzes zijn ook gewoon prettig en mooi: een inloopdouche zonder drempel, een wat hoger toilet of een brede deur. Ga je toch verbouwen, dan kost het weinig extra om dit meteen mee te nemen. In dit artikel lees je waar je op let en hoe de Wmo werkt.",
"kort_antwoord": "Kies een douche zonder drempel, een antislipvloer, voldoende vrije ruimte, een toilet op een prettige hoogte en stevige wanden waar later beugels aan kunnen. Heb je een beperking, vraag dan vóór de verbouwing bij het Wmo-loket van je gemeente of je een vergoeding kunt krijgen. De regels en de eigen bijdrage verschillen per gemeente.",
"secties": [
("wat", "Wat maakt een badkamer levensloopbestendig?",
"""<p>Het gaat om drie dingen: je kunt er veilig in bewegen, je kunt alles bereiken zonder te bukken of te reiken, en de badkamer is later makkelijk aan te passen. Denk aan iemand met een rollator, iemand die na een operatie tijdelijk slecht loopt, of een mantelzorger die moet kunnen helpen. Wat voor hen werkt, is voor iedereen comfortabel.</p>"""),
("douche", "Douche en vloer",
"""<ul class="checklist">
<li><strong>Geen drempel.</strong> Een inloopdouche met de vloer op één hoogte voorkomt struikelen en maakt een douchestoel of rolstoel mogelijk. Hoe dat technisch werkt, lees je in <a href="/kennisbank/inloopdouche-zonder-drempel/">inloopdouche zonder drempel</a>.</li>
<li><strong>Antislip.</strong> Kies vloertegels met een goede antislipwaarde, of kleinere tegels met veel voegen in de douche.</li>
<li><strong>Thermostaatkraan.</strong> Die houdt de temperatuur stabiel en voorkomt verbranding. Een kraan met een hendel is makkelijker dan een draaiknop.</li>
<li><strong>Een glijstang</strong> voor de handdouche, zodat zittend douchen ook kan.</li>
</ul>"""),
("ruimte", "Ruimte en maten",
"""<p>Voor iemand met een rolstoel wordt vaak een vrije draaicirkel van 150 centimeter aangehouden, en een vrije doorgang bij de deur van 85 tot 90 centimeter. Voor een rollator is iets minder genoeg. Dit zijn richtmaten uit praktijkgidsen en gemeentelijke regels, geen wettelijke eis voor een bestaande woning. Een ergotherapeut kan precies zeggen wat in jouw situatie nodig is.</p>
<p>Een schuifdeur of een deur die naar buiten opendraait, helpt ook. Valt iemand achter een naar binnen draaiende deur, dan kan niemand erbij.</p>"""),
("toilet", "Toilet, wastafel en steun",
"""<p>Een hangend toilet kun je op een hoogte laten monteren die past, vaak iets hoger dan standaard. Een wastafel zonder kast eronder maakt zittend wassen mogelijk. Laat de spiegel laag genoeg beginnen.</p>
<p>Beugels plaats je vaak pas als ze nodig zijn. Laat daarom nu al versterking in de wand aanbrengen naast het toilet en in de douche, bijvoorbeeld een houten regel of een plaat achter de tegels. Dan kun je later zonder breekwerk een beugel ophangen. Zet in de offerte waar die versterking komt en maak er foto's van.</p>"""),
("wmo", "Vergoeding via de Wmo",
"""<p>Heb je door een beperking, ziekte of ouderdom een aanpassing nodig, dan kun je een beroep doen op de Wet maatschappelijke ondersteuning (Wmo). Die regeling voert je gemeente uit. Zo werkt het meestal:</p>
<ul>
<li>Je meldt je bij het Wmo-loket of het sociaal wijkteam van je gemeente.</li>
<li>De gemeente onderzoekt in een gesprek wat je nodig hebt en wat je zelf kunt regelen.</li>
<li>Daarna besluit de gemeente of en hoe je ondersteuning krijgt. Dat kan een aanpassing zijn, een geldbedrag of een persoonsgebonden budget. Sommige gemeenten bieden een verhuisvergoeding als verhuizen beter past dan verbouwen.</li>
<li>Vaak betaal je een eigen bijdrage. De hoogte en de regels hangen af van je gemeente en veranderen soms per jaar. Het CAK heeft een rekenhulp.</li>
</ul>
<p>Heb je een Wlz-indicatie en woon je thuis, dan kan een woningaanpassing ook via de Wet langdurige zorg; ook daarvoor ga je naar de gemeente. Belangrijk: start de verbouwing pas als je weet wat de gemeente vergoedt. Vraag na hoe jouw gemeente omgaat met werk dat al begonnen is.</p>"""),
("huur", "Huur je de woning?",
"""<p>Voor een aanpassing in een huurwoning heb je meestal schriftelijke toestemming van de verhuurder nodig. Volgens de Rijksoverheid hoef je een aanpassing die via de Wmo of de Wlz is vergoed, bij verhuizing niet terug te draaien. Lees meer in ons artikel over <a href="/kennisbank/badkamer-huurwoning/">een badkamer in een huurwoning</a>.</p>"""),
],
"stappen_kop": "Stappenplan",
"stappen": [
("Bepaal wat nodig is", "Nu en over tien jaar. Laat je bij een beperking adviseren door een ergotherapeut."),
("Meld je bij de gemeente", "Heb je een beperking, vraag dan eerst bij het Wmo-loket wat mogelijk is, voordat je iets bestelt of laat slopen."),
("Vraag toestemming bij huur", "Leg de toestemming van de verhuurder schriftelijk vast."),
("Laat het meenemen in de offerte", "Drempelvrije douche, antislip, wandversterking en de maten van de deur. Laat de offertes vergelijken op dezelfde punten."),
("Controleer de oplevering", "Zit de versterking waar afgesproken, is de vloer stroef en loopt het water goed weg?"),
],
"faq": [
("Wat is een levensloopbestendige badkamer?", "Een badkamer die je veilig kunt blijven gebruiken als je ouder wordt of minder mobiel bent: drempelvrij, met genoeg ruimte, antislip en de mogelijkheid om later steun aan te brengen."),
("Betaalt de gemeente mijn nieuwe badkamer?", "Niet zomaar. Via de Wmo kun je ondersteuning krijgen als je door een beperking een aanpassing nodig hebt. De gemeente onderzoekt wat nodig is; regels en eigen bijdrage verschillen per gemeente."),
("Moet ik eerst naar de gemeente of eerst offertes vragen?", "Eerst naar de gemeente als je een vergoeding wilt. Start de verbouwing pas als je weet wat de gemeente besluit."),
("Hoe breed moet de deur zijn?", "Voor een rolstoel wordt vaak een vrije doorgang van 85 tot 90 centimeter aangehouden. Dit is een richtmaat; een ergotherapeut kan zeggen wat in jouw situatie nodig is."),
("Moet ik beugels meteen ophangen?", "Dat hoeft niet. Laat wel nu versterking in de wand aanbrengen, dan kun je beugels later zonder breekwerk plaatsen."),
],
"bronnen": [RIJK_WMO, RIJK_WMO_BIJDRAGE, RIJK_TRAPLIFT],
"dienst": "inloopdouche-plaatsen",
"kosten": ["inloopdouche", "toilet-renoveren"],
"tool": "/tools/badkamercheck/",
"extra": [("/badkamerspullen/inloopdouche-kopen/", "Inloopdouche kopen", "Glazen wand, goot en douchekop kiezen."),
          ("/badkamerspullen/toilet-kiezen/", "Toilet kiezen", "Hangend of staand, en op welke hoogte.")],
"gerelateerd": ["inloopdouche-zonder-drempel", "badkamer-huurwoning", "kleine-badkamer-indelen"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-op-zolder",
"groep": "Wonen en situatie",
"titel": "Badkamer op zolder: afvoer, vloer, vergunning en ventilatie",
"seo_titel": "Badkamer op zolder: waar je op let",
"description": "Een badkamer op zolder vraagt meer dan tegels. Lees waar je op let bij de afvoer, de draagkracht van de vloer, een eventuele vergunning, ventilatie en warm water.",
"kort": "Afvoer, draagkracht van de vloer, vergunning en ventilatie: de vier punten die een zolderbadkamer laten slagen.",
"intro": "Een tweede badkamer op zolder is handig voor een groeiend gezin, logés of een slaapkamer met eigen badkamer. Maar een zolder is vaak niet gebouwd om nat te worden of zwaar belast. De afvoer moet ver naar beneden, de vloer moet een gevuld bad kunnen dragen en vocht moet weg onder een schuin dak. In dit artikel lees je welke vragen je vooraf beantwoordt.",
"kort_antwoord": "Een badkamer op zolder kan bijna altijd, als vier dingen kloppen: een afvoer met genoeg afschot naar een standleiding, een vloer die het gewicht kan dragen, mechanische afzuiging naar buiten en warm water dat snel genoeg boven is. Binnen verbouwen is meestal vergunningvrij, maar een dakkapel, een dakraam aan de voorkant of een wijziging aan de constructie vraagt soms een vergunning.",
"secties": [
("afvoer", "De afvoer: het belangrijkste punt",
"""<p>Water en vooral de afvoer van een toilet hebben afschot nodig om goed weg te lopen. Hoe verder de badkamer van de bestaande standleiding ligt, hoe meer hoogte de leiding nodig heeft. Die leiding loopt in de vloer, in een verhoogde vloer of in een koof. Ligt de standleiding ver weg, dan kan de vloer van de badkamer een stuk hoger moeten worden.</p>
<p>Kan het niet onder vrij verval, dan is een vuilwaterpomp of een toilet met vermaler een uitweg. Die maken wel geluid, hebben stroom nodig en vragen onderhoud. Zie het als oplossing voor het toilet of een wastafel als het echt niet anders kan, niet als eerste keus. De regels voor binnenriolering staan in de norm NEN 3215; een installateur weet hoe die in jouw situatie uitpakt.</p>"""),
("vloer", "Kan de vloer het dragen?",
"""<p>Een badkamer is zwaar. Tegels, lijm, een dekvloer en vooral een gevuld bad tellen op: een bad met 200 liter water weegt met een persoon erin al snel 300 kilo of meer, op een kleine oppervlakte. Woonvloeren worden meestal berekend op een gebruiksbelasting van 1,75 kN/m², ongeveer 175 kilo per vierkante meter. Een oude zoldervloer is soms lichter uitgevoerd, omdat de zolder als bergruimte bedoeld was.</p>
<p>Laat bij een houten vloer, een vrijstaand bad of een dikke dekvloer een constructeur rekenen. Die bepaalt of de balklaag sterk en stijf genoeg is, en zo niet, hoe je hem versterkt. Een vloer die te veel doorbuigt geeft ook scheuren in tegels en afdichting. Kies op een lichte vloer liever een douche dan een bad.</p>"""),
("vergunning", "Heb je een vergunning nodig?",
"""<p>Een badkamer binnen de bestaande zolder bouwen is meestal vergunningvrij. Dat geldt niet altijd voor wat erbij komt kijken:</p>
<ul class="checklist">
<li><strong>Een dakkapel</strong> aan de achterkant is onder voorwaarden vergunningvrij. Aan de voorkant of zijkant die naar de straat kijkt, is vaak wel een vergunning nodig.</li>
<li><strong>Een wijziging aan de draagconstructie</strong>, zoals een balk verplaatsen of een dragende wand weghalen, laat je altijd beoordelen. Vraag bij de gemeente of een melding of vergunning nodig is.</li>
<li><strong>Een monument of beschermd stads- of dorpsgezicht</strong> heeft vaak strengere regels, ook voor dakramen.</li>
<li><strong>In een appartement</strong> beslist ook de VvE mee, zeker als je aan leidingen of het dak komt.</li>
</ul>
<p>Doe de vergunningcheck in het Omgevingsloket of vraag het na bij je gemeente voordat je bestelt.</p>"""),
("ventilatie", "Ventilatie onder een schuin dak",
"""<p>Een zolder is vaak kleiner en koeler dan een badkamer op de verdieping. Stoom slaat dan snel neer op koude plekken, zoals bij een dakraam of slecht geïsoleerde delen van het dak. Een mechanische afzuiging die rechtstreeks naar buiten afvoert, is daarom bijna altijd nodig. Voor nieuwbouw noemt het Bbl voor een badruimte 14 dm³ per seconde afzuiging; voor een verbouwing is dat een goede richtwaarde. Isoleer het dak rond de badkamer goed en laat een dampremmende laag aanbrengen aan de warme kant. Meer hierover in het artikel over <a href="/kennisbank/badkamer-ventilatie/">ventilatie in de badkamer</a>.</p>"""),
("water", "Warm water en waterdruk",
"""<p>Hoe verder de badkamer van de cv-ketel of warmtepomp, hoe langer je wacht op warm water. Dat kost water en energie. Vraag de installateur naar de lengte van de leiding en of een dunnere leiding of een andere route helpt. Kijk ook of je toestel genoeg warm water levert voor twee badkamers tegelijk. Op de hoogste verdieping is de waterdruk iets lager; meestal is dat geen probleem, maar laat het bij een regendouche controleren.</p>"""),
("indeling", "Indeling onder een schuin dak",
"""<p>Gebruik de lage delen voor wat je zittend of liggend gebruikt: een bad, het toilet of kastjes. Zet de douche en de wastafel waar je rechtop staat. Een dakraam boven de douche geeft licht, maar is ook een koude plek; kies dan goed isolerend glas. Lees meer over slim indelen in <a href="/kennisbank/kleine-badkamer-indelen/">een kleine badkamer indelen</a>.</p>"""),
],
"stappen_kop": "Stappenplan voor een zolderbadkamer",
"stappen": [
("Zoek de standleiding", "Kijk waar de bestaande afvoer loopt en hoe ver de nieuwe badkamer daarvan ligt."),
("Laat de vloer beoordelen", "Zeker bij een houten vloer of een bad: laat een constructeur rekenen."),
("Doe de vergunningcheck", "Voor een dakkapel, dakraam of wijziging aan de constructie, via het Omgevingsloket of de gemeente."),
("Plan ventilatie en isolatie", "Een afzuiging naar buiten en een goed geïsoleerd dak rond de badkamer."),
("Vraag offertes op dezelfde basis", "Laat afvoer, vloerversterking, ventilatie en leidingwerk apart in de offerte zetten."),
],
"faq": [
("Kan overal op zolder een badkamer komen?", "Bijna altijd, maar de afvoer bepaalt het meest. Hoe verder van de standleiding, hoe meer hoogte de leiding nodig heeft of hoe eerder een pomp nodig is."),
("Heb ik een vergunning nodig voor een badkamer op zolder?", "Binnen verbouwen is meestal vergunningvrij. Een dakkapel aan de voorkant, een wijziging aan de constructie of een monument kan wel een vergunning vragen. Check het bij je gemeente."),
("Kan er een bad op een houten zoldervloer?", "Soms. Een gevuld bad is zwaar. Laat een constructeur rekenen of de balken het dragen, of kies voor een douche."),
("Is een toilet met vermaler een goed idee?", "Alleen als vrij verval echt niet kan. Het werkt, maar maakt geluid, heeft stroom nodig en vraagt onderhoud."),
("Wat kost een badkamer op zolder?", "Dat hangt sterk af van de afvoer, de vloer en de ventilatie. Bekijk de richtprijzen op de kostenpagina en vraag offertes met deze posten apart."),
],
"bronnen": [RIJK_VERGUNNINGVRIJ, IPLO_WONING, IPLO_DAKKAPEL, IPLO_VENTILATIE, NEN],
"dienst": "badkamer-installeren",
"kosten": ["badkamer-op-zolder", "uurtarief-loodgieter"],
"tool": "/tools/badkamercalculator/",
"extra": [("/badkamerspullen/bad-of-douche/", "Bad of douche?", "De voor- en nadelen naast elkaar.")],
"gerelateerd": ["badkamer-ventilatie", "vloerverwarming-of-radiator", "volgorde-badkamerrenovatie"],
},
# ---------------------------------------------------------------------------
{
"slug": "schimmel-in-badkamer",
"groep": "Techniek en vocht",
"titel": "Schimmel in de badkamer: oorzaak, verwijderen en voorkomen",
"seo_titel": "Schimmel in de badkamer verwijderen en voorkomen",
"description": "Zwarte plekken in de voegen of op het plafond? Lees waar schimmel in de badkamer vandaan komt, hoe je het veilig verwijdert en wat je doet als het steeds terugkomt.",
"kort": "Waar schimmel vandaan komt, hoe je het veilig weghaalt en wanneer er een bouwkundig probleem achter zit.",
"intro": "Bijna iedereen heeft er weleens last van: zwarte puntjes in de kit, grijze voegen of een vlek op het plafond boven de douche. Schimmel in de badkamer is meer dan een schoonheidsfout. Het wijst op te veel vocht, en wie het alleen wegpoetst, ziet het snel terug. In dit artikel lees je hoe je de oorzaak vindt, hoe je schimmel veilig verwijdert en wanneer je een vakman nodig hebt.",
"kort_antwoord": "Schimmel groeit waar het lang vochtig blijft. Meestal is de oorzaak te weinig ventilatie, soms een lekkage of een koude plek. Verwijder schimmel met een middel dat door het Ctgb is toegelaten en volg het etiket. Komt het steeds terug of zit het op meerdere plekken, laat dan de oorzaak onderzoeken.",
"secties": [
("oorzaken", "Waar komt schimmel vandaan?",
"""<p>Na een douchebeurt zit de lucht vol waterdamp. Die damp slaat neer op de koudste plekken: het plafond, de hoeken, de buitenmuur en het raam. Blijven die plekken lang vochtig, dan krijgen schimmelsporen, die altijd in de lucht zitten, de kans om te groeien. Zeepresten, kalk en vuil in voegen en kit maken het oppervlak extra aantrekkelijk.</p>
<p>De belangrijkste oorzaken zijn:</p>
<ul class="checklist">
<li><strong>Te weinig afzuiging</strong>, of een ventilator die te kort draait of vervuild is.</li>
<li><strong>Geen toevoer van lucht.</strong> Een afzuiging werkt alleen als er lucht kan binnenkomen, bijvoorbeeld via een spleet onder de deur of een rooster.</li>
<li><strong>Koude plekken</strong>, zoals een slecht geïsoleerde buitenmuur of een koudebrug bij een balk of raam.</li>
<li><strong>Lekkage</strong>, bijvoorbeeld via losse kit of een lekkende leiding in de wand.</li>
</ul>"""),
("gezondheid", "Is schimmel ongezond?",
"""<p>Een beetje schimmel in een kitrand is vooral vervelend. Veel schimmel in huis hangt volgens de GGD-richtlijn van het RIVM wel samen met luchtwegklachten, zoals hoesten en astma, vooral bij kinderen en mensen met een longziekte. Neem schimmel dus serieus, zeker als het op meerdere plekken in huis zit.</p>"""),
("verwijderen", "Schimmel veilig verwijderen",
"""<p>Milieu Centraal adviseert alleen schimmelmiddelen te gebruiken met een toelating van het Ctgb, het College voor de toelating van gewasbeschermingsmiddelen en biociden. Het toelatingsnummer staat op het etiket. Let verder op het volgende:</p>
<ul>
<li>Volg de gebruiksaanwijzing precies, ook voor dosering en inwerktijd. Zorg voor frisse lucht tijdens het werk.</li>
<li>Maak geen eigen mengsels. Soda, bleek en chloor door elkaar gebruiken is gevaarlijk voor je gezondheid.</li>
<li>Verf nooit over schimmel heen. Behandel de plek eerst, laat hem drogen en gebruik daarna eventueel schimmelbestendige muurverf.</li>
<li>Kit die zwart is van binnenuit, krijg je niet meer schoon. Haal die eruit en laat nieuwe kit aanbrengen. Wat dat kost, lees je bij <a href="/kosten/kitwerk-voegen/">kitwerk en voegen</a>.</li>
<li>Lever restanten van schimmelmiddel in als klein chemisch afval.</li>
</ul>"""),
("voorkomen", "Schimmel voorkomen",
"""<p>Laat de mechanische afzuiging tijdens het douchen op de hoogste stand draaien en daarna nog een tijd na, bij voorkeur met een nalooptimer of vochtsensor. Houd de deur dicht tijdens het douchen, zodat de damp niet door het huis trekt, maar zorg voor een spleet of rooster voor de luchttoevoer. Trek na het douchen de wanden en de vloer droog met een trekker. Een raam open zetten in de winter kan averechts werken: de ruimte koelt af en de damp slaat juist neer op de koude muren.</p>
<p>Maak de voegen en kit regelmatig schoon en houd de ventilatieroosters stofvrij. Ontvochtigers en vochtvreters vangen tijdelijk wat vocht op, maar lossen de oorzaak niet op. Meer over afzuiging en luchttoevoer lees je in <a href="/kennisbank/badkamer-ventilatie/">ventilatie in de badkamer</a>.</p>"""),
("structureel", "Komt het steeds terug?",
"""<p>Komt schimmel snel terug, zit het op plekken die niet nat worden of op meerdere plekken in huis, dan is er vaak een bouwkundige oorzaak: lekkage, doorslaand of optrekkend vocht, of een koudebrug. Dan helpt schoonmaken niet meer. Laat een vakman of een onderzoeksbureau de oorzaak zoeken, bijvoorbeeld met een vochtmeting. Bij een verbouwing lossen betere isolatie, een goede afdichting onder de tegels en een sterkere afzuiging het meestal op. Lees ook <a href="/kennisbank/lekkage-badkamer/">lekkage in de badkamer</a>.</p>"""),
("huur", "Huur je de woning?",
"""<p>Huurders melden ernstige schimmel bij de verhuurder. Is de oorzaak een gebrek aan de woning, zoals lekkage of slechte ventilatie, dan moet de verhuurder dat herstellen. Hoe dat werkt en wat de Huurcommissie kan doen, lees je in <a href="/kennisbank/badkamer-huurwoning/">een badkamer in een huurwoning</a>.</p>"""),
],
"stappen_kop": "Zo pak je het aan",
"stappen": [
("Zoek de oorzaak", "Waar zit de schimmel, en is die plek koud, nat of slecht geventileerd?"),
("Controleer de ventilatie", "Draait de afzuiging, is het rooster schoon en kan er lucht binnenkomen?"),
("Verwijder de schimmel", "Met een Ctgb-toegelaten middel, volgens het etiket. Vervang zwarte kit."),
("Houd het droog", "Afzuiging laten nadraaien, wanden droogtrekken, voegen schoonhouden."),
("Schakel hulp in", "Komt het terug of zit het op meerdere plekken, laat dan een vakman de oorzaak onderzoeken."),
],
"faq": [
("Hoe krijg ik schimmel uit de kit?", "Oppervlakkige schimmel verwijder je met een Ctgb-toegelaten middel. Is de kit van binnenuit zwart, dan helpt dat niet meer en moet de kit vervangen worden."),
("Mag ik bleek en soda mengen tegen schimmel?", "Nee. Milieu Centraal raadt zelfgemaakte mengsels af; ze zijn gevaarlijk en niet toegelaten. Gebruik een middel met een Ctgb-toelating."),
("Moet het raam open na het douchen?", "In de winter liever niet. De ruimte koelt dan af en damp slaat neer op koude muren. Laat de mechanische afzuiging het werk doen en zorg voor luchttoevoer."),
("Helpt schimmelwerende verf?", "Schimmelbestendige verf helpt nieuwe groei te remmen, maar verf nooit over bestaande schimmel. Behandel de plek eerst."),
("Wanneer is schimmel een bouwkundig probleem?", "Als het snel terugkomt, op droge plekken zit of op meerdere plekken in huis. Dan is er vaak lekkage, doorslaand vocht of een koudebrug."),
],
"bronnen": [MC_SCHIMMEL, MC_VENTILEREN, RIVM_SCHIMMEL, VHN_SCHIMMEL, RIJK_VENTILEREN],
"dienst": "badkamer-onderhoud",
"kosten": ["kitwerk-voegen", "uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["badkamer-ventilatie", "lekkage-badkamer", "badkamer-waterdicht-maken"],
},
# ---------------------------------------------------------------------------
{
"slug": "lekkage-badkamer",
"groep": "Techniek en vocht",
"titel": "Lekkage in de badkamer: opsporen, herstellen en verzekering",
"seo_titel": "Lekkage in de badkamer opsporen en oplossen",
"description": "Een vlek op het plafond of een lopende watermeter? Lees hoe je een lekkage in de badkamer opspoort, wie je belt, wat je zelf doet en hoe het zit met je verzekering.",
"kort": "Zo vind je de bron van een lekkage, wat je meteen doet en waar je op let bij je woonverzekering.",
"intro": "Een lekkage in de badkamer merk je vaak pas laat. Een vlek op het plafond eronder, een tegel die loskomt of een watermeter die blijft draaien. Hoe sneller je de bron vindt, hoe kleiner de schade. In dit artikel lees je hoe je een lekkage opspoort, wat je zelf kunt doen en waar je op let als je de schade bij je verzekering meldt.",
"kort_antwoord": "Stop eerst de schade: draai bij een leidinglek de hoofdkraan dicht. Kijk daarna met de watermeter of het een lek in de waterleiding is of een lek bij gebruik, zoals via kit, de afvoer of de afdichting. Maak foto's en meld de schade snel bij je verzekeraar. Of je verzekering betaalt, hangt af van de oorzaak en je polisvoorwaarden.",
"secties": [
("eerst", "Wat je meteen doet",
"""<ul class="checklist">
<li><strong>Draai de hoofdkraan dicht</strong> als je een lekkende leiding vermoedt of water ziet stromen.</li>
<li><strong>Zet de stroom uit</strong> in de groep waar water bij elektra kan komen, bijvoorbeeld bij een lamp in het plafond.</li>
<li><strong>Beperk de schade</strong>: zet een emmer neer, haal spullen weg en dep water op.</li>
<li><strong>Maak foto's</strong> van de plek, de schade en eventueel de watermeter, met datum.</li>
<li><strong>Waarschuw de buren</strong> als je in een appartement woont; water zoekt zijn weg naar beneden.</li>
</ul>"""),
("opsporen", "Lekkage opsporen met de watermeter",
"""<p>De drinkwaterbedrijven geven allemaal ongeveer dezelfde test. Draai alle kranen dicht en zet apparaten die water gebruiken uit, zoals de wasmachine, de vaatwasser en eventueel de cv-ketel. Laat de hoofdkraan open en kijk een minuut naar het rode wieltje of driehoekje op de watermeter.</p>
<ul>
<li><strong>Staat de meter stil?</strong> Dan lekt de waterleiding niet. De lekkage ontstaat dan waarschijnlijk alleen bij gebruik: via de afvoer, de kit of de afdichting onder de tegels.</li>
<li><strong>Draait de meter?</strong> Dan zit er een lek in de waterleiding achter de meter, in je eigen installatie. Bel een loodgieter of installateur. Huurders bellen de verhuurder.</li>
<li><strong>Lekt het bij of vóór de meter?</strong> Neem dan contact op met je drinkwaterbedrijf.</li>
</ul>
<p>Kijk ook of het toilet nog doorloopt. Een stil doorlopend toilet laat de meter draaien zonder dat er iets nat wordt.</p>"""),
("bronnen", "De meest voorkomende bronnen",
"""<p>In de badkamer zijn dit de bekende boosdoeners:</p>
<ul>
<li><strong>Kitvoegen</strong> rond het bad, de douchebak of langs de vloer die loslaten of scheuren.</li>
<li><strong>De afvoer</strong>: een losse sifon, een lekkende aansluiting van de doucheput of een afvoergoot die niet goed in de afdichting is opgenomen.</li>
<li><strong>De afdichting onder de tegels</strong>, die ontbreekt, is gescheurd of slecht aansluit op de afvoer. Water loopt dan door de voegen naar beneden.</li>
<li><strong>Kranen en inbouwdelen</strong>, zoals een inbouwthermostaat of het inbouwreservoir van het toilet.</li>
<li><strong>Leidingen in de vloer of wand</strong>, bijvoorbeeld door een slechte koppeling of een boorgat.</li>
</ul>
<p>Lekt het alleen tijdens het douchen, test dan stap voor stap: laat alleen het bad of de douchebak vol lopen zonder te spatten, en daarna alleen water tegen de wand. Zo zie je of het lek bij de afvoer, de bak of de wand zit.</p>"""),
("vakman", "Wanneer een lekdetectiebedrijf?",
"""<p>Zie je geen duidelijke bron, dan kan een lekdetectiebedrijf zoeken zonder alles open te breken, bijvoorbeeld met een warmtecamera, een vochtmeter of een gas- of geluidsmeting op de leiding. Dat kost geld, maar kan veel onnodig breekwerk voorkomen. Vraag je verzekeraar vooraf of zij de kosten van het opsporen vergoeden en of ze een eigen bedrijf inschakelen.</p>"""),
("verzekering", "Hoe zit het met de verzekering?",
"""<p>Grofweg zo: de opstalverzekering dekt schade aan het huis zelf, zoals vloeren, wanden, plafonds en leidingen. De inboedelverzekering dekt je spullen. Veel opstalpolissen vergoeden het breek- en herstelwerk om bij een plotseling gesprongen of lekkende leiding te komen. De reparatie van de oorzaak zelf, zoals een versleten kitvoeg of een lekkende kraan, valt meestal onder onderhoud en is voor eigen rekening.</p>
<p>Verzekeraars kijken vooral of de lekkage plotseling en onvoorzien was. Schade die langzaam is ontstaan door slecht onderhoud of een fout bij de aanleg wordt vaak niet vergoed. De precieze dekking verschilt per polis, dus lees je voorwaarden. Ben je het niet eens met je verzekeraar, dan kun je na de klachtenprocedure terecht bij het Kifid.</p>"""),
("anderen", "Huur, VvE en buren",
"""<p>Huurders melden een lekkage direct bij de verhuurder; leidingen en afdichting zijn van de eigenaar. In een appartement kan de schade bij de buren terechtkomen. Dan kijkt jouw aansprakelijkheids- of opstalverzekering, of die van de VvE, naar de schade. In ons artikel over <a href="/kennisbank/verbouwen-in-vve/">verbouwen in een VvE</a> lees je wat privé is en wat gemeenschappelijk. Na een herstel wil je dat het niet terugkomt: lees hoe je <a href="/kennisbank/badkamer-waterdicht-maken/">een badkamer goed waterdicht maakt</a>.</p>"""),
],
"stappen_kop": "Stappenplan bij lekkage",
"stappen": [
("Stop de schade", "Hoofdkraan dicht, stroom uit waar nodig, water opvangen."),
("Doe de watermetertest", "Alle kranen dicht, een minuut kijken. Draait de meter, dan lekt de leiding."),
("Leg alles vast", "Foto's van de schade en de oorzaak, met datum."),
("Meld het snel", "Bij je verzekeraar, en bij huur bij de verhuurder."),
("Laat het goed herstellen", "Niet alleen de vlek, maar de oorzaak: leiding, afvoer, kit of afdichting."),
],
"faq": [
("Hoe weet ik of mijn waterleiding lekt?", "Draai alle kranen dicht, zet apparaten uit en kijk een minuut naar de watermeter. Draait het wieltje, dan lekt er water in je installatie."),
("Betaalt mijn verzekering een lekkage in de badkamer?", "Dat hangt af van de oorzaak en je polis. Plotselinge schade aan het huis valt vaak onder de opstalverzekering; versleten kit of slecht onderhoud meestal niet."),
("Wie betaalt de lekkage in een huurwoning?", "Leidingen, afvoer en afdichting zijn van de eigenaar. Meld de lekkage direct bij de verhuurder, schriftelijk."),
("Lekt het via de voegen?", "Voegen laten altijd wat water door. Lekt het daardoor naar beneden, dan werkt de afdichting onder de tegels niet goed."),
("Is opnieuw kitten genoeg?", "Alleen als de kit de oorzaak is. Zit het lek in de afdichting, de afvoer of een leiding, dan lost kit het niet op."),
],
"bronnen": [DUNEA_LEK, EVIDES_LEK, WATERNET_LEK, CB_WATERSCHADE, KIFID, RIJK_HUUR_GEBREKEN],
"dienst": "badkamer-onderhoud",
"kosten": ["uurtarief-loodgieter", "kitwerk-voegen"],
"tool": "/tools/badkamercheck/",
"extra": [],
"gerelateerd": ["badkamer-waterdicht-maken", "schimmel-in-badkamer", "verbouwen-in-vve"],
},
# ---------------------------------------------------------------------------
{
"slug": "badkamer-huurwoning",
"groep": "Wonen en situatie",
"titel": "Badkamer in een huurwoning: wat mag je en wat moet de verhuurder?",
"seo_titel": "Badkamer in een huurwoning: rechten en regels",
"description": "Mag je de badkamer in je huurwoning verbouwen? Lees wanneer je toestemming nodig hebt, hoe het zit met zelf aangebrachte voorzieningen en wat de verhuurder moet herstellen.",
"kort": "Toestemming, zelf aangebrachte voorzieningen en onderhoud: wat je als huurder mag en wat de verhuurder moet.",
"intro": "Een verouderde badkamer in een huurwoning is een veelgehoorde klacht. Mag je die zelf vernieuwen? Moet de verhuurder dat doen? En wat gebeurt er met je nieuwe badkamer als je verhuist? In dit artikel lees je hoe het huurrecht in grote lijnen werkt, wat zelf aangebrachte voorzieningen zijn en wat je kunt doen als de verhuurder gebreken niet herstelt.",
"kort_antwoord": "Voor een nieuwe of aangepaste badkamer heb je altijd schriftelijke toestemming van de verhuurder nodig. De verhuurder moet binnen 8 weken reageren en mag alleen weigeren als de woning slechter verhuurbaar wordt of in waarde daalt. Gebreken, zoals lekkage of schimmel door een bouwkundige oorzaak, moet de verhuurder herstellen. Bij sociale huur kun je anders naar de Huurcommissie.",
"secties": [
("toestemming", "Toestemming van de verhuurder",
"""<p>Als huurder mag je kleine aanpassingen doen die je bij vertrek zonder veel kosten terugdraait, zoals een spiegel of planchet ophangen. Voor een renovatie van de badkamer heb je volgens de Rijksoverheid altijd toestemming van de verhuurder nodig. Dat staat in artikel 7:215 van het Burgerlijk Wetboek.</p>
<ul class="checklist">
<li>Vraag de toestemming schriftelijk en beschrijf precies wat je wilt: tekening, materialen en wie het werk doet.</li>
<li>De verhuurder moet binnen 8 weken reageren.</li>
<li>Weigeren mag alleen als de woning daardoor slechter te verhuren is of in waarde daalt.</li>
<li>Weigert de verhuurder, dan kun je de rechter vragen of de verandering redelijk is.</li>
<li>Bespreek meteen wie wat betaalt en wat er bij vertrek gebeurt. Leg dat vast.</li>
</ul>"""),
("zav", "Zelf aangebrachte voorzieningen (ZAV)",
"""<p>Een badkamer die je met toestemming zelf laat aanleggen, heet een zelf aangebrachte voorziening, afgekort ZAV. Veel woningcorporaties hebben een eigen ZAV-beleid. Daarin staat welke aanpassingen mogen, aan welke eisen ze moeten voldoen en wat er bij vertrek gebeurt. Soms mag de badkamer blijven en krijg je een vergoeding die afneemt met de jaren. Soms moet je hem bij vertrek terugbrengen in de oude staat.</p>
<p>Vraag het ZAV-beleid op voordat je begint. Vraag ook of het onderhoud van jouw nieuwe badkamer daarna voor jou of voor de verhuurder is, en of de huur verandert. Een particuliere verhuurder heeft meestal geen vast beleid; maak dan zelf duidelijke afspraken op papier.</p>"""),
("onderhoud", "Wat moet de verhuurder onderhouden?",
"""<p>De verhuurder moet de woning onderhouden en gebreken herstellen. Een lekkende afvoer, een kapotte leiding, losse tegels door een slechte ondergrond of schimmel door slechte ventilatie zijn gebreken. Klein onderhoud is voor de huurder, zoals een leertje in de kraan vervangen of ontkalken. Welke kosten bij wie horen, staat in het Besluit kleine herstellingen; de Rijksoverheid heeft daar een overzicht van. Groot onderhoud en vernieuwing zijn voor de verhuurder.</p>
<p>Een badkamer die gewoon oud of ouderwets is, is geen gebrek. De verhuurder hoeft hem dan niet te vernieuwen. Wel telt het sanitair mee in het woningwaarderingsstelsel: de puntentelling die bij gereguleerde huur de maximale huurprijs bepaalt.</p>"""),
("gebreken", "Als de verhuurder niet herstelt",
"""<p>De Rijksoverheid beschrijft de route zo:</p>
<ul>
<li>Meld het gebrek per mail of brief aan de verhuurder. Noem elk gebrek en vraag om herstel binnen 6 weken. Bewaar een kopie en maak foto's.</li>
<li>Is het na 6 weken niet opgelost, dan kun je bij sociale huur de Huurcommissie vragen om tijdelijke huurverlaging. Lekkage, vocht en schimmel zijn voorbeelden van gebreken die daarvoor kunnen tellen, als ze ernstig genoeg zijn. Op de site van de Huurcommissie staat een gebrekencheck.</li>
<li>De Huurcommissie kan de verhuurder niet dwingen te repareren. Dat kunnen de rechter of de gemeente wel.</li>
</ul>
<p>Huur je in de vrije sector, dan zijn de mogelijkheden bij de Huurcommissie beperkter. Het Juridisch Loket geeft gratis advies over jouw situatie.</p>"""),
("renovatie", "Als de verhuurder renoveert",
"""<p>Wil de verhuurder de badkamer vernieuwen, dan moet hij een redelijk voorstel doen. Na een woningverbetering mag de huur soms omhoog, bijvoorbeeld bij sociale huur. Vraag vooraf hoe lang het werk duurt, of je tijdelijk ergens anders kunt douchen en of er een vergoeding is voor overlast of verhuizing. Bij grote renovaties van een complex gelden vaak afspraken met de huurdersvereniging.</p>"""),
("wmo", "Aanpassing om medische redenen",
"""<p>Heb je door een beperking een aanpassing nodig, zoals een douche zonder drempel of een verhoogd toilet, dan kun je via de Wmo bij je gemeente een vergoeding aanvragen. Volgens de Rijksoverheid hoef je zo'n aanpassing bij verhuizing niet terug te draaien. Lees meer in <a href="/kennisbank/levensloopbestendige-badkamer/">de levensloopbestendige badkamer</a>.</p>"""),
],
"stappen_kop": "Stappenplan voor huurders",
"stappen": [
("Lees je huurcontract", "Kijk wat er staat over veranderingen en vraag het ZAV-beleid op."),
("Vraag schriftelijk toestemming", "Met een beschrijving, tekening en wie het werk doet."),
("Maak afspraken over geld", "Wie betaalt wat, verandert de huur en wat gebeurt er bij vertrek?"),
("Laat het netjes uitvoeren", "Bewaar offertes, facturen en foto's van het werk, ook van de afdichting."),
("Meld gebreken schriftelijk", "Met een hersteltermijn van 6 weken. Kom je er niet uit, vraag dan advies bij het Juridisch Loket of de Huurcommissie."),
],
"faq": [
("Mag ik de badkamer in mijn huurhuis zelf vernieuwen?", "Alleen met toestemming van de verhuurder. Vraag die schriftelijk aan; de verhuurder moet binnen 8 weken reageren."),
("Moet de verhuurder een oude badkamer vervangen?", "Nee, ouderdom alleen is geen gebrek. Wel moet de verhuurder gebreken herstellen, zoals lekkage of kapotte leidingen."),
("Wat gebeurt er met mijn badkamer als ik verhuis?", "Dat hangt af van de afspraken en het ZAV-beleid. Soms mag hij blijven, soms met een vergoeding, soms moet je hem terugbrengen in de oude staat."),
("Wie betaalt een lekkende kraan in een huurwoning?", "Een leertje vervangen is klein onderhoud voor de huurder. Een kapotte leiding of afvoer herstelt de verhuurder."),
("Kan ik huurverlaging krijgen bij schimmel in de badkamer?", "Bij sociale huur kun je de Huurcommissie om tijdelijke huurverlaging vragen als de verhuurder een ernstig gebrek niet binnen 6 weken herstelt."),
],
"bronnen": [RIJK_HUUR_VERBOUWEN, RIJK_HUUR_GEBREKEN, RIJK_HUUR_KOSTEN, RIJK_TRAPLIFT, HUURCOMMISSIE, JURIDISCH_LOKET],
"dienst": "badkamer-renoveren",
"kosten": ["nieuwe-badkamer", "kitwerk-voegen"],
"tool": "/tools/offertechecker/",
"extra": [],
"gerelateerd": ["levensloopbestendige-badkamer", "schimmel-in-badkamer", "lekkage-badkamer"],
},
# ---------------------------------------------------------------------------
{
"slug": "kalk-en-waterhardheid",
"groep": "Techniek en vocht",
"titel": "Kalk en waterhardheid: hoe hard is jouw water?",
"seo_titel": "Kalk in de badkamer en waterhardheid in Nederland",
"description": "Hoe hard is het kraanwater in Nederland en hoe voorkom je kalk op glas, kranen en tegels? Met cijfers van drinkwaterbedrijven en uitleg over waterontharders.",
"kort": "Wat waterhardheid is, hoe hard het water bij jou is en hoe je kalk op douchewand en kranen voorkomt.",
"intro": "Witte vlekken op de douchewand, een verstopte douchekop en kranen die dof worden: dat is kalk. Hoeveel last je ervan hebt, hangt af van de hardheid van je kraanwater en van wat je na het douchen doet. In dit artikel lees je hoe hard het water in Nederland is, waar je dat voor jouw adres opzoekt, hoe je kalk voorkomt en of een waterontharder zin heeft.",
"kort_antwoord": "Nederlands kraanwater is gemiddeld zacht tot gemiddeld hard, rond 8 graden Duitse hardheid (°dH). Per drinkwaterbedrijf en per plaats verschilt het. Kalk voorkom je vooral door glas en kranen na het douchen droog te maken. Een waterontharder is volgens drinkwaterbedrijven en de Consumentenbond meestal niet nodig.",
"secties": [
("wat", "Wat is waterhardheid?",
"""<p>De hardheid van water zegt hoeveel calcium en magnesium erin zit. In Nederland wordt dat meestal uitgedrukt in Duitse graden (°dH) of in millimol per liter (mmol/l). Eén mmol/l is ongeveer 5,6 °dH. Hoe harder het water, hoe meer kalk achterblijft als het opdroogt of wordt verwarmd. Hard water is niet ongezond; het is vooral een kwestie van schoonmaken en van slijtage aan apparaten.</p>
<p>Let op: bedrijven gebruiken niet allemaal dezelfde indeling. Waternet noemt water pas hard vanaf 12 °dH. Dunea noemt 4 tot 8 °dH zacht. Brabant Water gebruikt een schaal met grenzen bij 4, 8, 12 en 18 °dH. Verkopers van ontharders noemen water soms al hard vanaf 4 °dH; Waternet noemt dat onjuist.</p>"""),
("nederland", "Hoe hard is het water in Nederland?",
"""<p>Drinkwaterbedrijven ontharden het water centraal, zodat het in de meeste regio's zacht tot gemiddeld hard uit de kraan komt. Een paar voorbeelden van wat de bedrijven zelf opgeven:</p>
<ul>
<li><strong>Waternet</strong> (Amsterdam en omgeving): 7,8 °dH. Waternet noemt het landelijk gemiddelde ongeveer 8 °dH.</li>
<li><strong>PWN</strong> (Noord-Holland): gemiddeld 7,9 °dH.</li>
<li><strong>Dunea</strong> (Zuid-Holland, regio Den Haag en Leiden): ongeveer 1,42 mmol/l, ruim 7,9 °dH.</li>
<li><strong>Brabant Water</strong>: per plaats verschillend, gemiddeld tussen 5,0 en 11,2 °dH. Helmond zit bijvoorbeeld op 10,8 °dH.</li>
<li><strong>Vitens</strong> (onder meer Gelderland, Overijssel, Utrecht, Friesland en Flevoland): noemt een hardheid rond 8 °dH en laat je per postcode zoeken.</li>
</ul>
<p>De wet vraagt een minimale hardheid van 1 mmol/l. Weet je niet welk drinkwaterbedrijf je hebt, kijk dan op je waterrekening. Op de site van je bedrijf zoek je de hardheid voor jouw postcode of plaats op. Deze cijfers kunnen veranderen als een bedrijf zijn zuivering aanpast.</p>"""),
("badkamer", "Waar zie je kalk in de badkamer?",
"""<ul class="checklist">
<li><strong>Glazen douchewand</strong>: witte vlekken en een doffe waas.</li>
<li><strong>Douchekop</strong>: verstopte gaatjes en een scheve straal.</li>
<li><strong>Kranen</strong>: vooral mat zwart, goud en geborsteld metaal laten kalkvlekken goed zien.</li>
<li><strong>Tegels en voegen</strong>: een grijze laag waar schimmel zich makkelijk aan hecht.</li>
<li><strong>Toilet</strong>: kalkaanslag onder de rand en in het reservoir.</li>
</ul>"""),
("voorkomen", "Kalk voorkomen en verwijderen",
"""<p>Waternet geeft drie eenvoudige tips: spoel de douche na met koud water, droog de douchewand af met een trekker of handdoek, en leg een verkalkte douchekop een nacht in schoonmaakazijn. Volg bij apparaten altijd de instructies van de fabrikant. Wat ook helpt:</p>
<ul>
<li>Kies glas met een coating die water laat afparelen, en een douchekop met rubberen nopjes die je met je vingers schoonwrijft.</li>
<li>Gebruik op kranen en microcement geen sterke ontkalker of schuurmiddel; die beschadigen de afwerking. Vraag de leverancier welke middelen geschikt zijn.</li>
<li>Kalk en zeepresten trekken schimmel aan. Wie kalk bijhoudt, heeft minder <a href="/kennisbank/schimmel-in-badkamer/">schimmel in de badkamer</a>.</li>
</ul>
<p>Dunea wijst erop dat een lagere temperatuur van de boiler minder kalk geeft, maar dat warm water minstens 60 °C moet blijven tegen bacteriën.</p>"""),
("ontharder", "Is een waterontharder nodig?",
"""<p>Vitens schrijft dat de Consumentenbond een waterontharder niet nodig vindt bij Nederlands kraanwater. Wil je er toch een, let dan op het volgende, zoals Vitens en Dunea het beschrijven:</p>
<ul>
<li>Laat hem plaatsen door een erkende installateur, met de juiste terugstroombeveiliging.</li>
<li>Kies een toestel met een Kiwa-keurmerk of een vergelijkbare erkende kwaliteitsverklaring.</li>
<li>Na de ontharder mag het water in je installatie niet zachter worden dan 5,6 °dH.</li>
<li>Onderhoud is nodig; anders kunnen bacteriën groeien en krijgt het water een luchtje of smaak.</li>
<li>Een ontharder verlaagt de waterdruk, volgens beide bedrijven met ongeveer 0,7 bar.</li>
</ul>"""),
("keuzes", "Keuzes bij een nieuwe badkamer",
"""<p>Woon je in een gebied met harder water of wil je weinig poetsen? Kies dan een glazen wand met coating of een wand met minder glas, chroom of geborsteld staal in plaats van mat zwart, en tegels met een glad, niet te donker oppervlak. Meer over afwerkingen lees je bij <a href="/badkamerspullen/kranen-kiezen/">kranen kiezen</a>.</p>"""),
],
"stappen_kop": "Checklist tegen kalk",
"stappen": [
("Zoek je waterhardheid op", "Op de site van je drinkwaterbedrijf, met je postcode of plaats."),
("Droog na het douchen", "Trek glas, kranen en tegels droog. Dat scheelt het meeste werk."),
("Ontkalk op tijd", "Douchekop in schoonmaakazijn; volg bij kranen en apparaten de instructies van de fabrikant."),
("Kies slimme materialen", "Coating op glas, chroom of geborsteld staal, lichte tegels."),
("Twijfel je over een ontharder?", "Lees eerst het advies van je drinkwaterbedrijf en laat hem alleen door een erkende installateur plaatsen."),
],
"faq": [
("Hoe hard is het kraanwater in Nederland?", "Gemiddeld rond 8 °dH, zacht tot gemiddeld hard. Per bedrijf en plaats verschilt het; Brabant Water geeft bijvoorbeeld 5,0 tot 11,2 °dH op."),
("Is hard water ongezond?", "Nee. Hard water geeft meer kalk, maar is niet schadelijk voor de gezondheid."),
("Hoe krijg ik kalk van de douchewand?", "Droog de wand na elke douchebeurt. Bestaande kalk verwijder je met een geschikte kalkreiniger of schoonmaakazijn, volgens de instructies van de leverancier van het glas."),
("Heb ik een waterontharder nodig?", "Meestal niet, volgens drinkwaterbedrijven en de Consumentenbond. Wil je er toch een, laat hem dan door een erkende installateur plaatsen en onderhoud hem goed."),
("Waarom heeft mijn buurman ander water?", "Dat kan als je net op de grens van twee leveringsgebieden woont. De hardheid hangt af van het winpunt en de zuivering."),
],
"bronnen": [WATERNET_HARDHEID, PWN_HARDHEID, DUNEA_HARDHEID, BRABANTWATER_HARDHEID, VITENS_ONTHARDERS],
"dienst": "badkamer-onderhoud",
"kosten": ["uurtarief-loodgieter"],
"tool": "/tools/badkamercheck/",
"extra": [("/badkamerspullen/kranen-kiezen/", "Kranen kiezen", "Afwerkingen die wel en niet tegen kalk kunnen."),
          ("/badkamerspullen/douchesysteem-kiezen/", "Douchesysteem kiezen", "Douchekoppen en thermostaten vergelijken.")],
"gerelateerd": ["schimmel-in-badkamer", "microcement-badkamer", "tegels-kiezen"],
},
# ---------------------------------------------------------------------------
{
"slug": "vloerverwarming-of-radiator",
"groep": "Techniek en vocht",
"titel": "Vloerverwarming of radiator in de badkamer?",
"seo_titel": "Vloerverwarming of radiator in de badkamer?",
"description": "Vloerverwarming, een handdoekradiator of allebei? Lees de voor- en nadelen voor de badkamer, wat past bij een warmtepomp en waarom elektrische vloerverwarming niet zuinig is.",
"kort": "Warme voeten of snel warm? De voor- en nadelen van vloerverwarming en radiatoren in de badkamer.",
"intro": "Een badkamer moet snel warm zijn als je eruit stapt, en je handdoek wil je droog. Kies je voor vloerverwarming, een handdoekradiator of een combinatie? Het antwoord hangt af van je verwarmingssysteem, de grootte van de badkamer en of je over een tijd een warmtepomp wilt. In dit artikel zetten we de keuzes naast elkaar.",
"kort_antwoord": "Vloerverwarming op warm water geeft gelijkmatige warmte en werkt goed op lage temperatuur, dus ook met een warmtepomp. Het reageert traag. Een radiator warmt sneller op en droogt handdoeken. In veel badkamers werkt een combinatie het best: vloerverwarming als basis en een handdoekradiator erbij. Elektrische vloerverwarming is volgens Milieu Centraal niet zuinig.",
"secties": [
("vloer", "Vloerverwarming in de badkamer",
"""<p>Bij vloerverwarming lopen buizen met warm water door de dekvloer onder de tegels. Tegels geleiden de warmte goed, dus een badkamer is daar heel geschikt voor. Volgens Milieu Centraal werkt vloerverwarming meestal met water rond 40 °C, en vaak lager. De vloer van een badkamer mag maximaal 33 °C worden.</p>
<ul class="checklist">
<li><strong>Voordelen</strong>: warme voeten, gelijkmatige warmte, geen radiator aan de wand, en een vloer die sneller droogt na het douchen.</li>
<li><strong>Nadelen</strong>: traag. Het duurt lang voordat de ruimte warm is. Milieu Centraal raadt daarom af om 's nachts de temperatuur te verlagen.</li>
<li><strong>Aandachtspunt</strong>: de vloer wordt een paar centimeter hoger door de buizen en de dekvloer, en de dekvloer moet drogen voordat er getegeld wordt.</li>
</ul>"""),
("radiator", "Radiator of handdoekradiator",
"""<p>Een radiator geeft snel warmte. Een handdoekradiator, de bekende ladder aan de wand, droogt bovendien je handdoeken. Maar een handdoekradiator vol met handdoeken geeft minder warmte af aan de ruimte. In een grotere badkamer of een badkamer met een koude buitenmuur is een handdoekradiator alleen soms te weinig.</p>
<p>Een handdoekradiator kan op de cv aangesloten worden, elektrisch zijn of allebei. Een elektrisch element is handig in de zomer, als de verwarming uit staat, maar draait op stroom; zet het op een timer.</p>"""),
("combinatie", "De combinatie: vaak de beste keus",
"""<p>In veel nieuwe badkamers komt vloerverwarming als basis, met een handdoekradiator voor droge handdoeken en snelle extra warmte. Zo heb je warme voeten en een ruimte die snel op temperatuur is. Let op als alles op één circuit zit: de radiator heeft vaak een hogere watertemperatuur nodig dan de vloer. Een installateur lost dat op met een aparte groep of een regeling die de temperatuur van de vloer begrenst.</p>"""),
("warmtepomp", "Wil je later een warmtepomp?",
"""<p>Een warmtepomp werkt het zuinigst met water van lage temperatuur. Vloerverwarming past daar goed bij. Radiatoren kunnen ook, mits ze groot genoeg zijn. Milieu Centraal noemt radiatoren met twee of drie platen en lamellen meestal geschikt; er zijn ook radiatoren speciaal voor lage temperatuur. Met de Verwarmingstest van Milieu Centraal zet je de cv-ketel een tijd op 50 °C en kijk je of het huis warm genoeg blijft. Ga je toch verbouwen, neem dan vloerverwarming of een radiator die op lage temperatuur genoeg warmte geeft meteen mee.</p>"""),
("elektrisch", "Elektrische vloerverwarming",
"""<p>Elektrische vloerverwarming bestaat uit dunne matten met verwarmingsdraden onder de tegels. Het is makkelijk aan te leggen en de vloer wordt nauwelijks hoger. Daarom wordt het vaak verkocht als oplossing voor een kleine badkamer. Milieu Centraal is duidelijk: elektrische vloerverwarming is niet zuinig en het advies is te kiezen voor verwarming met warm water. Wil je toch elektrisch, gebruik het dan alleen als extra voor warme voeten, met een thermostaat en een timer, en niet als enige verwarming.</p>"""),
("kosten", "Wat kost het?",
"""<p>Vloerverwarming kost meer bij de aanleg dan een radiator, omdat er een dekvloer en een verdeler nodig zijn. In een badkamer die je toch helemaal vernieuwt, valt het extra werk mee. Richtprijzen en rekenvoorbeelden vind je op de pagina over <a href="/kosten/vloerverwarming-badkamer/">vloerverwarming in de badkamer</a>.</p>"""),
],
"stappen_kop": "Zo kies je",
"stappen": [
("Kijk naar je verwarming", "Cv-ketel, warmtepomp of stadswarmte? En wil je over een paar jaar overstappen?"),
("Bepaal wat je belangrijk vindt", "Warme voeten, snel warm, droge handdoeken of ruimte aan de wand."),
("Check de vloer", "Is er hoogte voor buizen en een dekvloer, en is de vloer geïsoleerd?"),
("Vraag een warmteberekening", "Laat de installateur uitrekenen hoeveel warmte de badkamer nodig heeft."),
("Plan het op tijd", "Vloerverwarming komt vroeg in de verbouwing en de dekvloer moet drogen voordat er getegeld wordt."),
],
"faq": [
("Is vloerverwarming in de badkamer genoeg?", "In een kleine, goed geïsoleerde badkamer vaak wel. In een grotere badkamer of bij een koude buitenmuur is een radiator erbij prettig."),
("Werkt vloerverwarming met een warmtepomp?", "Ja, heel goed. Vloerverwarming werkt op lage watertemperatuur, en daar is een warmtepomp het zuinigst mee."),
("Is elektrische vloerverwarming zuinig?", "Nee. Milieu Centraal raadt aan om te kiezen voor verwarming met warm water. Gebruik elektrisch hooguit als extra, met een timer."),
("Hoe warm mag een badkamervloer worden?", "Volgens Milieu Centraal maximaal 33 °C."),
("Geeft een handdoekradiator genoeg warmte?", "Soms niet, zeker als er handdoeken over hangen. Laat de installateur uitrekenen wat de badkamer nodig heeft."),
],
"bronnen": [MC_VLOERVERWARMING, MC_LTV],
"dienst": "badkamer-installeren",
"kosten": ["vloerverwarming-badkamer", "nieuwe-badkamer"],
"tool": "/tools/badkamercalculator/",
"extra": [],
"gerelateerd": ["badkamer-op-zolder", "volgorde-badkamerrenovatie", "badkamer-ventilatie"],
},
]
