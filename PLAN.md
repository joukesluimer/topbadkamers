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
- [x] Eigen Supabase-project **TopBadkamers** (ref `zedqxocehypoioskzsfc`, EU-West, gratis plan). Het schema staat erin, met de tabel `monteurs` in plaats van `schilders`. Lezen met de publieke sleutel wordt geweigerd. `supabase_leadbeheer.sql` is nog niet uitgevoerd, want de leadprijzen daarin gaan nog over schilderwerk.
- [x] GitHub-repo `joukesluimer/topbadkamers` (publiek), met alle code behalve `.github/workflows`. Die komt erbij zodra de site bouwt, zodat er geen mislukte deploys komen.
- [x] De Make-webhook van Topschilder is losgekoppeld (`WEBHOOK_URL` is leeg).
- [x] Fase 1 af en live op https://joukesluimer.github.io/topbadkamers/ (22 november 2026).
- [x] Fase 2 en 3 af (23 november 2026), gemaakt met zes agents tegelijk. Elke module heeft `LINKS` en `build(write)`; `build.py` roept ze aan via `CONTENT_MODULES` en `TOOL_MODULES`.
  - `badkamer_kosten.py`: `/kosten/` en 8 kostenpagina's.
  - `badkamer_kennis.py` en `badkamer_kennis_artikelen.py`: `/kennisbank/` en 10 artikelen.
  - `badkamer_spullen.py`: `/badkamerspullen/` en 7 kopersgidsen. Het is vorm (a): neutraal, zonder winkel en zonder affiliatelinks.
  - Tools, met het overzicht `/tools/` in build.py:
    - `badkamer_calculator.py`;
    - `badkamer_planner.py`;
    - `badkamer_check.py`;
    - `badkamer_offertecheck.py`, met de parser `offerte_parser_badkamer.js` inline;
    - `badkamer_stijl.py`.
  - Het menu heeft nu Diensten, Wat kost het? (/kosten/), Tools, Kennisbank en Voor badkamerspecialisten. De dienstpagina's linken naar de passende kosten, artikelen, gidsen en tools ("Meer weten?").
  - De oude Topschilder-modules (`kosten_data.py`, `kennisbank.py`, `huiscalculator.py` enz.) staan nog in de map maar worden niet gebouwd. Ze kunnen weg.
  - Nog te doen: de richtprijzen jaarlijks nalopen, en de richtprijzen van offertechecker, calculator en kostenpagina's naast elkaar leggen zodat ze gelijk lopen.

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

1. **Domeinnaam: top-badkamers.nl, later.** Jouke koopt het domein later. Tot die tijd draait de site op het gratis GitHub-adres `https://joukesluimer.github.io/topbadkamers/` (`SITE["domein"]` is leeg, dus er komt geen CNAME).
   - **Let op voor fase 1:** de site staat dan in een submap (`/topbadkamers/`), maar de code gebruikt links vanaf de root (`/assets/...`, `/kosten/...`). Bij het bouwen moeten die een voorvoegsel krijgen, of die links breken op het GitHub-adres.
   - Bij de overstap naar het domein: `domein` en `url` in `data.py` invullen, het voorvoegsel weer leeg maken en DNS bij de registrar op GitHub Pages zetten.
2. **Hoe "spullen" werkt.** Voorlopig gekozen: (a). Wil je het anders, kies dan een van deze vormen:
   - (a) alleen neutrale kopersgidsen en richtprijzen, zonder winkel;
   - (b) doorverwijzen naar webwinkels, eventueel met affiliatelinks;
   - (c) materiaal meenemen in de offerte van de monteur.
   - Als je een eigen winkel wilt koppelen, moet de site daar eerlijk over zijn.
3. **Werkgebied.** Hetzelfde als Topschilder (Flevoland, het Gooi, de Veluwe, Zwolle/Kampen, Amersfoort), of groter?
4. **Bedrijfsgegevens.** Hetzelfde KvK-nummer en e-mailadres als Topschilder, of nieuwe?

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
