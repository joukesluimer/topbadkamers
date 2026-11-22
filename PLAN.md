# Top Badkamers: projectplan

*Opgezet op 22 november 2026 als kopie van de code van Topschilder.nl (branch `ronde4`, gelijk aan live).*

## Het concept

Hetzelfde als Topschilder, maar dan voor badkamers:

- **Badkamermonteurs:** huiseigenaren vragen gratis offertes aan bij maximaal drie badkamerspecialisten uit de buurt. Topschilder doet hetzelfde voor schilders.
- **Badkamerspullen:** eerlijke kopersgidsen en richtprijzen voor sanitair en materialen, zoals inloopdouches, toiletten, wastafelmeubels, kranen en tegels. Zo weet iemand wat iets kost voordat hij een monteur of winkel kiest.
- **Gratis tools en content** die bezoekers en backlinks trekken, net als bij Topschilder.

## Stand van zaken

- [x] Projectmap `~/Projects/topbadkamers` met een eigen git-geschiedenis.
- [x] Code van Topschilder overgenomen: build, verify, componenten, tools, formulieren en de koppeling met Supabase.
- [ ] De foto's van Topschilder zijn bewust niet meegenomen (`fotos/` is leeg).
  - Die gaan over schilderwerk, en de licenties en vermeldingen horen bij die site.
  - De site bouwt daardoor nog niet volledig. Zie "Fase 1".
- [ ] Alle teksten gaan nog over schilderwerk. Er staan ongeveer 1.500 vermeldingen van "schilder" in de code.

## Hoe het concept vertaalt

| Topschilder | Top Badkamers |
|---|---|
| Diensten: binnen- en buitenschilderwerk, houtrot, spuitwerk, behangen, zakelijk | Badkamer renoveren (compleet), badkamer installeren of sanitair monteren, tegelwerk badkamer, inloopdouche plaatsen, toilet renoveren, badkamer onderhoud (kitten, voegen, lekkage) en zakelijk of VvE |
| Kostenpagina's (keuken spuiten, kozijnen, uurtarief) | Wat kost een nieuwe badkamer, een inloopdouche, toilet renoveren, een tegelzetter per m², badkamer slopen, vloerverwarming, kitwerk en voegen vernieuwen, en het uurtarief van een loodgieter of installateur |
| Huiscalculator | **Badkamercalculator:** m², tegels, sanitairniveau, sloopwerk, leidingwerk en elektra; je ziet het totaal per regio |
| Kleurenkiezer | **Badkamerstijl-kiezer:** een 3D-render van een badkamer, waarin je tegels, kraankleur, meubel en douche wisselt |
| Onderhoudscheck | **Badkamercheck:** is je badkamer aan vervanging toe? (leeftijd, voegen, schimmel, lekkage, kitranden) |
| Schilderweer | Vervalt. In de plaats: **renovatieplanner** (hoe lang duurt het en in welke volgorde gebeurt wat) |
| Offertechecker | **Badkamerofferte-checker:** dezelfde parser, met andere posten (sloop, tegelwerk per m², leidingwerk, elektra, stelposten voor sanitair) |
| Inspiratie | Badkamerstijlen: modern, landelijk, industrieel, Japandi, kleine badkamer en toilet |
| Kennisbank | Artikelen over waterdicht maken, tegels kiezen, inloopdouche zonder drempel, ventilatie, garanties en vergunning bij een VvE |
| Plaatspagina's met BAG/CBS-data | Hetzelfde. Het bouwjaar zegt veel over de leeftijd van badkamers en de staat van leidingen |
| Voor schilders | **Voor badkamerspecialisten:** aanmelden om leads te ontvangen |
| Social ads en actiepagina's | Hetzelfde, met badkamerhaakjes |

## Wat ik van je nodig heb

1. **Domeinnaam.**
   - Topbadkamers.nl is al geregistreerd door iemand anders. Die naam is niet beschikbaar, tenzij hij van jou is.
   - Vrij op 22 november: top-badkamers.nl, topbadkamermonteur.nl en topbadkamer.com.
2. **Hoe "spullen" werkt.** Kies een van deze vormen:
   - (a) alleen neutrale kopersgidsen en richtprijzen, zonder winkel;
   - (b) doorverwijzen naar webwinkels, eventueel met affiliatelinks;
   - (c) materiaal meenemen in de offerte van de monteur.
   - Als je een eigen winkel wilt koppelen, moet de site daar eerlijk over zijn.
3. **Werkgebied.** Hetzelfde als Topschilder (Flevoland, het Gooi, de Veluwe, Zwolle/Kampen, Amersfoort), of groter?
4. **Bedrijfsgegevens.** Hetzelfde KvK-nummer en e-mailadres als Topschilder, of nieuwe?
5. **Leads.** Een eigen Supabase-project, of een aparte tabel in het bestaande project?
6. **GitHub.** Mag ik een nieuwe repository voorbereiden? Jij maakt hem aan, en daarna richten we Pages en het domein in.

## Fases

1. **Basis:**
   - merk, kleuren en logo;
   - `data.py` herschrijven (SITE, DIENSTEN, prijzen);
   - de schilderspecifieke tools tijdelijk uitzetten;
   - de site bouwt en `verify.py` geeft ALLES OK.
2. **Content:**
   - dienstpagina's en kostenpagina's;
   - kennisbank;
   - de sectie badkamerspullen;
   - plaatspagina's met badkameradvies per bouwjaar.
3. **Tools:** badkamercalculator, stijlkiezer, badkamercheck, offertechecker en renovatieplanner.
4. **Beeld:**
   - 3D-renders van badkamers (three.js, zoals de tools-renders van Topschilder);
   - echte foto's alleen met een vrije licentie.
5. **Live zetten:** GitHub Pages, domein, Search Console, sitemap.
6. **Groei:** SEO-onderzoek met Semrush, vermeldingen en backlinks, social ads.

De regels van Topschilder gelden hier ook:
- geen valse claims (geen verzonnen reviews, sterren, aantallen monteurs of projecten);
- foto's alleen met licentie en vermelding;
- niets live en geen geld uitgeven zonder akkoord.
