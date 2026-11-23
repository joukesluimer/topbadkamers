# Concept: badkamerofferte vergelijken (november 2026)

Status: voorstel, nog niets gebouwd. **Besluit 23-11-2026: geen laag 3, alleen leads.** Laag 3 hieronder blijft alleen staan als vastlegging van wat we bewust niet doen. Dit gaat in de plaats van keuze 2 ("hoe spullen werkt") in PLAN.md zodra er een besluit is.

## Waar het vandaan komt
- **Abedini.nl** is geen productvergelijker maar een tegenofferte-dienst:
  - je uploadt je offerte en krijgt een voorstel van een leverancier uit hun eigen netwerk terug;
  - je betaalt €399 vast, of een vergoeding volgens no cure no pay;
  - het verdienmodel en de banden met leveranciers staan alleen in de voorwaarden.
- **Andere sites** doen het in drie soorten, en allemaal zonder heldere scheiding tussen advies en verkoop:
  - tegenoffertes van winkels: Voordelig Design Sanitair, Bad en Vloer;
  - leadplatforms: Homedeal, Werkspot, Bobex, Slimster, Renocheck;
  - prijsvergelijkers per product: Klarna, Vergelijk.nl, Beslist.
- **Het gat in de markt:** niemand leest de offerte die je al hebt regel voor regel en geeft daar een neutraal oordeel over. Niemand kijkt per regel naar product (merk, serie, artikelnummer), arbeid, materiaal en ontbrekende posten, en zegt eerlijk waar de prijs goed is en waar hij niet klopt.

## Uitgangspunt (Jouke, 23-11-2026)
- **De consument betaalt niets.** Abedini laat de eindklant betalen (€399 of no cure no pay); dat doen wij niet.
- **Wij zijn de tussenpersoon en doen zelf weinig in het proces.** Ons geld komt van de aanbodkant:
  - een leadvergoeding van badkamerspecialisten;
  - eventueel commissie van winkels.
- **Gevolg:** alles wat wij doen moet automatisch gaan, dus de check, het doorsturen en het productaanbod. Er komt geen handmatige beoordeling per offerte.

## Het idee in één zin
Bij Top Badkamers leg je je badkamerofferte neer. Je krijgt per regel te zien hoe die zich verhoudt tot de markt. Pas daarna, en alleen als je dat zelf wilt, kies je voor een tweede offerte of voor een productaanbod.

## Drie lagen, strikt gescheiden

| | Laag 1: Offertecheck | Laag 2: Tweede offerte | Laag 3: Productaanbod (optioneel) |
|---|---|---|---|
| Wat | Elke regel naast richtprijs en marktband. Plus ontbrekende posten, regels die te vaag zijn ("onvoldoende gespecificeerd") en een mailsjabloon om een betere offerte te vragen | De "tegenofferte zonder kosten": de specificatie uit je offerte, zonder NAW, gaat naar maximaal 3 specialisten. Zij sturen zelf een tegenofferte. Dit is de Abedini-gedachte, maar de specialist betaalt in plaats van de klant | Bij herkende producten: het aanbod van een winkel |
| Geld | Niets | Leadvergoeding van specialisten | Commissie of eigen marge |
| Gegevens | Blijven in de browser, er wordt niets verstuurd | Alleen na een eigen klik en een aparte toestemming | Alleen na een eigen klik, en NAW gaat niet mee |
| Uiterlijk | Neutrale huisstijl | Eigen blok met de vermelding "Wij krijgen een vergoeding van de specialist" | Eigen blok in een andere kleur, met "Aanbod van [winkel]: [relatie]" bij elk product |

**Regels voor de afscheiding** (volgen uit ACM, EU-principes voor vergelijkers en vergelijkende reclame):
1. Laag 1 ziet er precies hetzelfde uit, of laag 2 en 3 nu bestaan of niet. Het oordeel en de volgorde houden nooit rekening met wie betaalt.
2. Laag 3 staat nooit tussen de marktprijzen. Hij heeft een eigen blok onder de check, met een label bij elk product en "Hoe we vergelijken" ernaast. De marktband blijft altijd zichtbaar, ook als de winkel duurder is.
3. Er komt een pagina "Hoe verdienen wij geld", die vanaf de footer en vanaf de uitslag bereikbaar is. Daarop staan de eigenaar, de leadvergoeding, de relatie met de winkel en de dekking van de productdata.
4. Geen "onafhankelijk" zolang er laag 2 of 3 is. Wel: "De check is gratis en verstuurt niets. Kies je voor een tweede offerte, dan krijgen wij een vergoeding van de specialist."
5. Geen oordeel over de aanbieder ("te duur", "afzetterij"), maar een feitelijke vergelijking: "Deze post ligt 35% boven de richtprijs van €X–€Y (bron, peildatum)". We vergelijken alleen een gelijk product, of noemen het expliciet "vergelijkbaar" en geven de verschillen.
6. Geen betaalde check zoals Abedini. Dat haalt het herroepingsrecht, de bestelknop en de no-cure-no-pay-voorwaarden binnen, en het maakt de neutraliteit ongeloofwaardig.

## Technische fasering
- **Versie 1, statisch, kan nu** (± 800–1.000 regels code, plus productdata):
  - **Pdf-upload:** de pdf wordt in de browser gelezen. `vendor/pdfjs` staat er al, maar is nog niet gekoppeld.
  - **Regels splitsen:** de parser splitst elke regel in product, arbeid of materiaal en bepaalt de productcategorie.
  - **Producten herkennen:** merk, serie, EAN en artikelnummer.
  - **`producten_badkamer.py`:** ~150–300 veelgebruikte artikelen met prijsband en peildatum. Is een product onbekend, dan valt hij terug op de band van zijn categorie uit de spullengidsen.
  - **Uitslag per regel**, met een mailsjabloon voor een betere offerte.
- **Versie 2:** scans en foto's lezen via de bestaande Supabase Edge Function. Die moet eerst van schilderwerk naar badkamers. NAW-gegevens worden al in de browser verwijderd. Hiervoor zijn nodig: een API-sleutel, een maandlimiet, een verwerkersovereenkomst en een aangepaste privacyverklaring. **Dit kost geld, dus eerst jouw akkoord.**
- ~~Versie 3: laag 3 met een productfeed~~ (vervalt, besluit 23-11-2026).

## Keuzes voor Jouke
1. **Laag 3: BESLOTEN, (a) geen laag 3, alleen leads.**
   - (a) geen laag 3; Top Badkamers blijft puur check en leads;
   - (b) meerdere winkels via een affiliatefeed (Daisycon of Tradetracker);
   - (c) één winkel, bijvoorbeeld Tegeldepot of Badkamerdepot. Dan moet de band ("zusterbedrijf" of "partner") bij elk product en op de pagina "Hoe verdienen wij geld" staan. Omdat je daar werkt, regel je dit eerst intern.
2. **Bron voor de productdata in versie 1:** handmatig verzamelde marktprijzen (meerdere winkels, elk kwartaal), of een export of feed waarvan de herkomst op de pagina staat.
3. **Naam en plek:**
   - de huidige `/tools/offertechecker/` uitbreiden (behoudt de bestaande links), of
   - een eigen hoofdmenu-item "Offerte vergelijken" met de tool als kern.

**Naar de shop:** vervalt, want er komt geen winkel aan de site. Wel mag de check geanonimiseerde tellingen bijhouden van welke posten vaak voorkomen en tegen welke prijs. Dat mag alleen als de verwerking op een server plaatsvindt en de privacyverklaring het noemt. In versie 1 blijft alles in de browser, dus dan niet.
