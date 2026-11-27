# SEO-ronde 5: technische vindbaarheid en snelheid

*27 november 2026, branch `claude/tb-seo-5c12e0`.*

Alle nieuwe logica staat in `seo_extra.py`. Dat bestand bewerkt de kant-en-klare HTML in `site/` als laatste stap van `build.py`. De andere modules hoeven er niets voor te doen.

Gewijzigde gedeelde bestanden:

- `build.py`: twee regels in `main()`, die `seo_extra.nabewerken()` aanroepen.
- `prefix.py`: de regex `SRCSET` pakt nu ook `imagesrcset`, voor de preload.

`assets.py` en `components.py` zijn niet aangeraakt.

## Hulpmiddelen

```bash
python3 seo_extra.py meet    # grootte van CSS, JS en HTML (ruw en gzip)
python3 seo_extra.py audit   # titels, descriptions, H1, canonical, breadcrumb, linkdiepte, inlinks
```

## 1. Audit (337 indexeerbare pagina's)

- **Titels:** allemaal binnen de 62 tekens van verify.py, en elke titel noemt het onderwerp. Er zijn geen dubbele titels.
- **Descriptions:**
  - geen dubbele;
  - 1 pagina buiten de norm van 110–175 tekens: `/kosten/nieuwe-badkamer/` (180). Die is al opgelost in tb-kosten (commit f34c65c);
  - 61 pagina's zitten tussen 161 en 175 tekens. Dat mag volgens verify.py, maar Google kan ze afkappen. Vooral kopersgidsen, kennisbank en materialen. Inkorten hoort bij de contentsessies.
- **H1, canonical, breadcrumb:** elke indexeerbare pagina heeft precies één H1 en een canonical. Elke pagina behalve de homepage heeft een breadcrumb.
- **Linkdiepte vanaf de homepage:**
  - 1 klik: 58 pagina's;
  - 2 klikken: 229;
  - 3 klikken: 49;
  - geen enkele pagina is onbereikbaar of dieper dan 3 klikken.
- **Weinig contextlinks** (links uit de lopende tekst, dus zonder menu en footer):
  - vóór deze ronde hadden 20 contentpagina's er 4 of minder, zoals `/kennisbank/badkamer-kitten/`, `/kosten/bad-plaatsen/` en `/kosten/douchecabine-plaatsen/`;
  - na het blok "Gerelateerde pagina's" heeft elke contentpagina er minstens 5;
  - alleen servicepagina's zitten nog onder de 5: over ons, contact, cookies en fotoverantwoording. Die staan in het menu of de footer.
- **Bekende melding van verify.py:** de kapotte link naar `/kosten/badkamer-verplaatsen/` komt uit het onaffe kosten4-werk in de basiscommit. Ook die is opgelost in tb-kosten (f34c65c). Met die commit erbij geeft verify.py "ALLES OK". Dat is getest, maar de commit is niet overgenomen.

## 2. Schema

- **Organization (homepage):** krijgt `logo` (`/assets/fotos/merk/apple-touch-icon.png`, 180×180) en `image` (de og-png).
- **ItemList:** toegevoegd op `/diensten/`, `/kosten/`, `/tools/` en `/werkgebied/`, en op de 35 plaatspagina's (een lijst van diensten in die plaats).
  - De kennisbank, inspiratie, materialen, badkamer-voor en de kopersgidsen hadden al een ItemList.
  - De lijst van de kopersgidsen had relatieve urls; die zijn nu volledig.
- **Service:** alle dienstpagina's en plaats×dienst-pagina's hadden er al een. `seo_extra` vult hem aan als hij ooit ontbreekt.
- **HowTo:** op 10 kennisbankartikelen met een echt stappenplan:
  - kitten;
  - volgorde van een renovatie;
  - lekkage;
  - schimmel;
  - asbest;
  - een drempelloze douche;
  - verbouwen in een VvE;
  - schoonmaken;
  - ventilatie checken;
  - een kleine badkamer indelen.

  Keuze-checklists krijgen geen HowTo. De lijst staat in `HOWTO` in `seo_extra.py`.
- **Geen review- of rating-schema.**

## 3. Image-sitemap

`site/sitemap-afbeeldingen.xml` bevat 34 renders op 31 pagina's, telkens in de grootste versie. De sitemap staat ook in `robots.txt`.

## 4. Gerelateerde pagina's

Onder 93 contentpagina's staat nu een blok met zes verwante pagina's. Het gaat om kennisbank, kosten, kopersgidsen, inspiratie, materialen en "voor wie".

- **Hoe de pagina's gekozen worden:**
  - op onderwerp: woorden uit slug, title, H1 en H2's, samenstellingen ("inloopdouche" telt ook als "douche") en vaste onderwerpgroepen (`THEMA`);
  - zeldzame woorden tellen zwaarder;
  - pagina's die nog niet in de tekst gelinkt staan en weinig links krijgen, gaan voor;
  - hooguit drie pagina's uit dezelfde rubriek.
- **Resultaat:** 429 nieuwe contextlinks.
- **Plek:** vóór de afsluitende CTA.
- **Vormgeving:** de CSS (`.gerel`) wordt achter style.css gezet. Gecontroleerd op 375 en 1280 px.

## 5. Snelheid

| | vóór | na |
|---|---:|---:|
| style.css | 80.063 B (gzip 17.891) | 64.432 B (gzip 14.756) |
| app.js | 33.168 B (gzip 10.228) | 26.698 B (gzip 8.530) |
| config.js | 1.906 B (gzip 1.042), render-blokkerend | 401 B (gzip 297), `defer` |
| toestemming.js | 3.908 B (gzip 1.755) | 3.185 B (gzip 1.507) |
| CSS + JS samen, gzip | 30.916 B | 25.090 B (−19%) |
| `<img>` zonder `decoding` | 818 van 952 | 0 |
| `<img>` zonder `loading` | 409 | 409: alleen het logo in de header, bewust zonder lazy |
| preload hero-beeld | nee | ja, met `imagesrcset` en `fetchpriority=high` |
| render-blokkerende scripts | 1 (config.js) | 0 |

Wat er precies veranderd is:

- **CSS:** 202 regels met classes die op geen enkele pagina en in geen enkel script voorkomen, gaan eruit. Dat zijn resten uit Topschilder (`oc-*`, `hero-*`, `stars` en dergelijke).
  - Het werkt voorzichtig: een class die ergens als woord voorkomt, of die een script aan elkaar plakt (`'bl-dq-' + x`), blijft staan.
  - Het draait bij elke build opnieuw, dus nieuwe pagina's houden hun CSS.
  - 20 pagina's zijn op 500 en 1280 px vergeleken, met en zonder opschoning. Er is geen zichtbaar verschil.
- **JS:** commentaarregels, inspringing en lege regels eruit. Regels blijven regels, dus er is geen risico met automatische puntkomma's. `node --check` is in orde.
- **Fonts:** alleen systeemfonts (`--font` en `--serif`). Er zijn geen webfonts en er is geen Google Fonts.
- **HTML:** per pagina gemiddeld 42,5 → 42,9 kB (gzip 10,3 kB). Dat komt door het nieuwe blok en het schema.
- **Niet gedaan:**
  - herhaalde inline `<style>`-blokken (in totaal 349 kB over alle pagina's, het meest `.bv-kort`, `.mt-*` en `.bi-*`) naar style.css verhuizen. Die zitten in modules van andere sessies;
  - de offertechecker (291 kB HTML met de parser inline) opsplitsen.
