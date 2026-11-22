# -*- coding: utf-8 -*-
"""
Sfeerbeelden in SVG.

Waarom SVG en geen foto's: dit zijn vectorbeelden van een paar kilobyte die
oneindig scherp blijven, in de huisstijlkleuren staan en geen enkel
licentierisico geven. Ze worden rechtstreeks in de HTML gezet, dus ze kosten
geen extra laadverzoek. Het zijn getekende illustraties, geen foto's van echte
klussen: presenteer ze ook zo.

Wil je later echte foto's? Zie FOTO_SLOTS onderaan: dan is het één regel per
plek om een illustratie te vervangen door een <img>.
"""

# huisstijl, gelijk aan STYLE_CSS in assets.py
PETROL      = "#0b4a56"
PETROL_ZACHT= "#24606b"
ACCENT      = "#c4511f"
ACCENT_D    = "#a8431a"
ACCENT_L    = "#f0a37f"
CREME       = "#f2f8f8"
LICHT       = "#dde9eb"
VOEG        = "#c6d8db"
WIT         = "#ffffff"
GLAS        = "#cfe6ea"
GLAS_D      = "#a9cdd4"
HOUT        = "#d9b48f"


def _wrap(inner, vb="0 0 640 420", extra=""):
    return (f'<svg class="illu" viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-hidden="true" preserveAspectRatio="xMidYMid slice"{extra}>{inner}</svg>')


def _tegels(x, y, b, h, maat, kleur=VOEG, dikte=2):
    """Voegenraster over een vlak: één <path> met horizontale en verticale lijnen."""
    d = "".join(f"M{x} {yy}h{b}" for yy in range(y + maat, y + h, maat))
    d += "".join(f"M{xx} {y}v{h}" for xx in range(x + maat, x + b, maat))
    return f'<path d="{d}" stroke="{kleur}" stroke-width="{dikte}" fill="none"/>'


def _ruimte(vloer_y=340):
    """Achterwand met tegels en een vloer: de basis van elke badkamerscène."""
    return (f'<rect width="640" height="420" fill="{CREME}"/>'
            f'<rect x="0" y="0" width="640" height="{vloer_y}" fill="{WIT}"/>'
            + _tegels(0, 0, 640, vloer_y, 40) +
            f'<path d="M0 {vloer_y}h640v{420 - vloer_y}H0z" fill="{LICHT}"/>'
            + _tegels(0, vloer_y, 640, 420 - vloer_y, 40, kleur="#c9dbde") +
            f'<path d="M0 {vloer_y}h640" stroke="{PETROL}" stroke-width="5"/>')


# ---------------------------------------------------------------------------
# Hero en per dienst
# ---------------------------------------------------------------------------

def badkamer_renoveren():
    """Complete badkamer: bad met kraan, wastafelmeubel met spiegel, handdoek."""
    return _wrap(_ruimte() + f'''
<!-- spiegel -->
<rect x="404" y="70" width="150" height="112" rx="14" fill="{GLAS}" stroke="{PETROL}" stroke-width="6"/>
<path d="M430 150 470 98M452 162 500 100" stroke="{WIT}" stroke-width="7" stroke-linecap="round" opacity=".8"/>
<!-- wastafelmeubel -->
<rect x="390" y="208" width="178" height="18" rx="5" fill="{WIT}" stroke="{PETROL}" stroke-width="6"/>
<rect x="398" y="226" width="162" height="78" rx="6" fill="{HOUT}" stroke="{PETROL}" stroke-width="6"/>
<path d="M479 226v78" stroke="{PETROL}" stroke-width="5"/>
<path d="M458 262h12M488 262h12" stroke="{PETROL}" stroke-width="5" stroke-linecap="round"/>
<path d="M479 208v-22h18" fill="none" stroke="{PETROL}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
<!-- bad -->
<path d="M38 236h300v34a54 54 0 0 1-54 54H92a54 54 0 0 1-54-54z" fill="{WIT}" stroke="{PETROL}" stroke-width="6" stroke-linejoin="round"/>
<path d="M30 236h316" stroke="{PETROL}" stroke-width="9" stroke-linecap="round"/>
<path d="M84 324l-10 16M292 324l10 16" stroke="{PETROL}" stroke-width="7" stroke-linecap="round"/>
<path d="M72 236v-92a24 24 0 0 1 48 0v10" fill="none" stroke="{PETROL}" stroke-width="7" stroke-linecap="round"/>
<path d="M106 162h28" stroke="{PETROL}" stroke-width="7" stroke-linecap="round"/>
<!-- handdoek -->
<path d="M590 120v120" stroke="{PETROL}" stroke-width="6" stroke-linecap="round"/>
<rect x="566" y="128" width="48" height="96" rx="6" fill="{ACCENT}"/>
<path d="M566 206h48" stroke="{ACCENT_D}" stroke-width="5"/>
''')


def badkamer_installeren():
    """Sanitair monteren: wastafel met kraan en zichtbare afvoer, met een steeksleutel."""
    return _wrap(_ruimte() + f'''
<!-- wastafel -->
<path d="M180 168h280v20a50 50 0 0 1-50 50H230a50 50 0 0 1-50-50z" fill="{WIT}" stroke="{PETROL}" stroke-width="6" stroke-linejoin="round"/>
<path d="M170 168h300" stroke="{PETROL}" stroke-width="9" stroke-linecap="round"/>
<!-- kraan -->
<path d="M320 168v-50h36v18" fill="none" stroke="{PETROL}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M304 118h32" stroke="{ACCENT}" stroke-width="10" stroke-linecap="round"/>
<path d="M356 146c0 0-7 9-7 14a7 7 0 0 0 14 0c0-5-7-14-7-14z" fill="{GLAS_D}"/>
<!-- afvoer en sifon -->
<path d="M320 238v34a22 22 0 0 0 44 0v-6h70v74" fill="none" stroke="{PETROL_ZACHT}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
<!-- leidingen naar de muur -->
<path d="M262 238v40h-62v62M378 238v26" fill="none" stroke="{ACCENT}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
<!-- steeksleutel -->
<g transform="rotate(-32 520 300)">
  <rect x="470" y="292" width="104" height="16" rx="8" fill="{PETROL}"/>
  <path d="M598 287a17 17 0 1 0 0 26" fill="none" stroke="{PETROL}" stroke-width="13" stroke-linecap="round"/>
</g>
''')


def tegelwerk_badkamer():
    """Tegelzetten: een wand die half betegeld is, een lijmkam en een stapel tegels."""
    return _wrap(f'''
<rect width="640" height="420" fill="{CREME}"/>
<path d="M0 340h640v80H0z" fill="{LICHT}"/>
<!-- kale wand -->
<rect x="60" y="40" width="380" height="300" fill="#e9eeee"/>
<!-- lijmbed met kamstrepen -->
<rect x="250" y="40" width="80" height="300" fill="#d7e0e1"/>
<path d="M258 50v280M270 50v280M282 50v280M294 50v280M306 50v280M318 50v280" stroke="#c3cfd1" stroke-width="3"/>
<!-- gezette tegels -->
<rect x="60" y="40" width="190" height="300" fill="{WIT}"/>
{_tegels(60, 40, 190, 300, 60, kleur=PETROL_ZACHT, dikte=3)}
<rect x="190" y="160" width="60" height="60" fill="{ACCENT}" opacity=".85"/>
<path d="M60 40h380v300" fill="none" stroke="{PETROL}" stroke-width="5"/>
<path d="M60 40v300" stroke="{PETROL}" stroke-width="5"/>
<!-- tegel die geplaatst wordt -->
<g transform="rotate(-8 300 120)">
  <rect x="268" y="88" width="60" height="60" rx="2" fill="{WIT}" stroke="{PETROL}" stroke-width="4"/>
</g>
<!-- lijmkam -->
<g transform="rotate(18 520 190)">
  <rect x="466" y="170" width="110" height="46" rx="4" fill="#9fb5b9"/>
  <path d="M466 216l6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10 6 10 6-10" fill="none" stroke="#9fb5b9" stroke-width="4"/>
  <rect x="500" y="144" width="40" height="26" rx="8" fill="{ACCENT}"/>
</g>
<!-- stapel tegels -->
<g stroke="{PETROL}" stroke-width="4">
  <rect x="470" y="306" width="120" height="16" rx="2" fill="{WIT}"/>
  <rect x="476" y="290" width="120" height="16" rx="2" fill="{WIT}"/>
  <rect x="466" y="322" width="120" height="18" rx="2" fill="{WIT}"/>
</g>
''')


def inloopdouche_plaatsen():
    """Inloopdouche: regendouche, glazen wand en een douchegoot in de vloer."""
    return _wrap(_ruimte() + f'''
<!-- douchestang en regendouche -->
<path d="M150 340V112a20 20 0 0 1 20-20h96v28" fill="none" stroke="{PETROL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M226 132h80a0 0 0 0 1 0 0 40 12 0 0 1-40 12 40 12 0 0 1-40-12z" fill="{PETROL}"/>
<rect x="222" y="122" width="88" height="12" rx="6" fill="{PETROL}"/>
<g stroke="{GLAS_D}" stroke-width="5" stroke-linecap="round">
  <path d="M236 160v26M256 168v38M276 160v30M296 168v22M246 222v26M286 214v30M266 236v24"/>
</g>
<!-- thermostaatkraan -->
<rect x="138" y="214" width="24" height="44" rx="8" fill="{WIT}" stroke="{PETROL}" stroke-width="5"/>
<circle cx="150" cy="236" r="7" fill="{ACCENT}"/>
<!-- glazen wand -->
<rect x="380" y="70" width="150" height="270" rx="4" fill="{GLAS}" opacity=".55" stroke="{PETROL}" stroke-width="5"/>
<path d="M404 300 470 100M432 318 508 92" stroke="{WIT}" stroke-width="7" stroke-linecap="round" opacity=".8"/>
<path d="M455 40v30" stroke="{PETROL}" stroke-width="6" stroke-linecap="round"/>
<!-- douchegoot -->
<rect x="150" y="364" width="220" height="14" rx="5" fill="{WIT}" stroke="{PETROL}" stroke-width="4"/>
<path d="M166 371h188" stroke="{ACCENT}" stroke-width="4" stroke-dasharray="10 8"/>
''')


def toilet_renoveren():
    """Hangtoilet voor een ingebouwd reservoir, met bedieningsplaat en rolhouder."""
    return _wrap(_ruimte() + f'''
<!-- voorzetwand -->
<rect x="170" y="110" width="300" height="230" fill="{WIT}" stroke="{PETROL}" stroke-width="5"/>
{_tegels(170, 110, 300, 230, 50, kleur=VOEG)}
<!-- bedieningsplaat -->
<rect x="282" y="140" width="76" height="50" rx="8" fill="{WIT}" stroke="{PETROL}" stroke-width="5"/>
<rect x="292" y="150" width="34" height="30" rx="5" fill="{ACCENT}"/>
<rect x="326" y="150" width="22" height="30" rx="5" fill="{ACCENT_L}"/>
<!-- hangtoilet, zijaanzicht -->
<path d="M240 240h170a0 0 0 0 1 0 0v10a56 56 0 0 1-56 56h-68a46 46 0 0 1-46-46z" fill="{WIT}" stroke="{PETROL}" stroke-width="6" stroke-linejoin="round"/>
<path d="M232 236h186" stroke="{PETROL}" stroke-width="9" stroke-linecap="round"/>
<!-- rolhouder -->
<path d="M520 200h34v14" fill="none" stroke="{PETROL}" stroke-width="6" stroke-linecap="round"/>
<circle cx="548" cy="236" r="24" fill="{WIT}" stroke="{PETROL}" stroke-width="5"/>
<circle cx="548" cy="236" r="8" fill="{LICHT}" stroke="{PETROL}" stroke-width="4"/>
<path d="M524 240v40h24" fill="{WIT}" stroke="{PETROL}" stroke-width="5" stroke-linejoin="round"/>
''')


def badkamer_onderhoud():
    """Onderhoud: een nieuwe kitrand langs het bad en een kitspuit."""
    return _wrap(_ruimte(vloer_y=350) + f'''
<!-- bad, vooraanzicht -->
<rect x="40" y="210" width="380" height="140" rx="6" fill="{WIT}" stroke="{PETROL}" stroke-width="6"/>
<path d="M32 210h396" stroke="{PETROL}" stroke-width="9" stroke-linecap="round"/>
<!-- verse kitrand (accent) en oude, vergeelde kit -->
<path d="M36 200h250" stroke="{ACCENT}" stroke-width="9" stroke-linecap="round"/>
<path d="M300 200h124" stroke="#c9c19a" stroke-width="9" stroke-linecap="round" stroke-dasharray="18 10"/>
<circle cx="350" cy="186" r="10" fill="#9fb0a2" opacity=".55"/>
<circle cx="378" cy="180" r="6" fill="#9fb0a2" opacity=".5"/>
<!-- kitspuit -->
<g transform="rotate(-20 420 160)">
  <rect x="300" y="146" width="150" height="34" rx="6" fill="{WIT}" stroke="{PETROL}" stroke-width="5"/>
  <path d="M300 163h-34l-10 0" stroke="{PETROL}" stroke-width="8" stroke-linecap="round"/>
  <path d="M256 158l-22 5 22 5z" fill="{ACCENT}"/>
  <rect x="450" y="152" width="70" height="22" rx="4" fill="{PETROL}"/>
  <path d="M470 174l-6 54h22l4-54" fill="{PETROL}"/>
  <path d="M520 163h40" stroke="{PETROL}" stroke-width="7" stroke-linecap="round"/>
</g>
<!-- druppel -->
<path d="M560 236c0 0-22 26-22 40a22 22 0 0 0 44 0c0-14-22-40-22-40z" fill="{GLAS_D}" stroke="{PETROL}" stroke-width="4"/>
''')


def zakelijk_badkamers():
    """Zakelijk en VvE: een appartementengebouw waarin één badkamer oplicht."""
    ramen = "".join(
        f'<rect x="{x}" y="{y}" width="62" height="46" rx="3"/>'
        for y in (78, 150, 222) for x in (124, 210, 296)
        if not (x == 210 and y == 150))
    return _wrap(f'''
<rect width="640" height="420" fill="{CREME}"/>
<path d="M0 356h640v64H0z" fill="{LICHT}"/>
<!-- appartementengebouw -->
<rect x="100" y="52" width="282" height="304" fill="{WIT}" stroke="{PETROL}" stroke-width="6"/>
<g fill="{GLAS}" stroke="{PETROL_ZACHT}" stroke-width="4">{ramen}</g>
<!-- het raam met de nieuwe badkamer -->
<rect x="210" y="150" width="62" height="46" rx="3" fill="{ACCENT}" stroke="{PETROL}" stroke-width="4"/>
<path d="M228 164h26a0 0 0 0 1 0 0 13 5 0 0 1-13 5 13 5 0 0 1-13-5z" fill="{WIT}"/>
<path d="M234 176v8M241 176v12M248 176v8" stroke="{WIT}" stroke-width="3" stroke-linecap="round"/>
<rect x="210" y="294" width="62" height="62" rx="3" fill="{PETROL_ZACHT}"/>
<!-- tweede pand -->
<rect x="400" y="132" width="168" height="224" fill="{WIT}" stroke="{PETROL}" stroke-width="6"/>
<g fill="{GLAS_D}">
  <rect x="424" y="160" width="52" height="40" rx="3"/><rect x="494" y="160" width="52" height="40" rx="3"/>
  <rect x="424" y="222" width="52" height="40" rx="3"/><rect x="494" y="222" width="52" height="40" rx="3"/>
</g>
<rect x="458" y="296" width="52" height="60" rx="3" fill="{PETROL_ZACHT}"/>
''')


ILLUSTRATIES = {
    "hero": badkamer_renoveren,
    "badkamer-renoveren": badkamer_renoveren,
    "badkamer-installeren": badkamer_installeren,
    "tegelwerk-badkamer": tegelwerk_badkamer,
    "inloopdouche-plaatsen": inloopdouche_plaatsen,
    "toilet-renoveren": toilet_renoveren,
    "badkamer-onderhoud": badkamer_onderhoud,
    "zakelijk-badkamers": zakelijk_badkamers,
}


def hero():
    """Bewaard voor oude aanroepen: de hero is nu de complete badkamer."""
    return badkamer_renoveren()


def illustratie(sleutel):
    fn = ILLUSTRATIES.get(sleutel)
    return fn() if fn else ""


# ---------------------------------------------------------------------------
# Voor/na: een verouderde badkamerwand tegenover een vernieuwde
# ---------------------------------------------------------------------------

def _wand(nieuw):
    tegel = WIT if nieuw else "#e8e4d4"
    voeg = VOEG if nieuw else "#a9a58e"
    kit = ACCENT if nieuw else "#c9c19a"
    vlek = "" if nieuw else '''
      <circle cx="96" cy="250" r="22" fill="#8f9f92" opacity=".45"/>
      <circle cx="126" cy="268" r="12" fill="#8f9f92" opacity=".4"/>
      <circle cx="520" cy="120" r="16" fill="#8f9f92" opacity=".35"/>
      <path d="M300 60l10 40-6 30" fill="none" stroke="#a9a58e" stroke-width="3"/>'''
    kraan = (f'<path d="M320 210v-34h28v12" fill="none" stroke="{PETROL}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
             if nieuw else
             '<path d="M300 210v-26h-14M340 210v-26h14" fill="none" stroke="#8c8a7a" stroke-width="8" stroke-linecap="round"/>'
             '<path d="M300 196h40" stroke="#8c8a7a" stroke-width="8"/>')
    return f'''
<rect width="640" height="360" fill="{CREME}"/>
<rect x="40" y="30" width="560" height="270" fill="{tegel}" stroke="{PETROL}" stroke-width="5"/>
{_tegels(40, 30, 560, 270, 45, kleur=voeg, dikte=3)}
<path d="M40 300h560v60H40z" fill="{LICHT}"/>
<path d="M150 210h340v26a40 40 0 0 1-40 40H190a40 40 0 0 1-40-40z" fill="{WIT}" stroke="{PETROL}" stroke-width="5"/>
<path d="M142 210h356" stroke="{PETROL}" stroke-width="8" stroke-linecap="round"/>
<path d="M144 203h352" stroke="{kit}" stroke-width="6" stroke-linecap="round"/>
{kraan}{vlek}'''


def voor_na():
    """Interactieve schuif: sleep om het verschil te zien. Getekend, dus gelabeld als illustratie:
    gebruik voor echte voor/na-foto's alleen paren waarvan de licentie vastligt."""
    return f'''<div class="vn" data-vn>
  <svg viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Badkamerwand voor de renovatie">{_wand(False)}</svg>
  <div class="vn-na"><svg viewBox="0 0 640 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Badkamerwand na de renovatie">{_wand(True)}</svg></div>
  <span class="vn-label l">Voor</span>
  <span class="vn-label r">Na</span>
  <span class="vn-soort">Illustratie</span>
  <div class="vn-greep" role="slider" tabindex="0" aria-label="Sleep om voor en na te vergelijken" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50"></div>
</div>'''


# ---------------------------------------------------------------------------
# Later echte foto's gebruiken?
# ---------------------------------------------------------------------------

FOTO_SLOTS = """
Elke illustratie is te vervangen door een foto. Zet het bestand in
fotos/ (zie foto_data.py) en vervang in build.py de aanroep, bijvoorbeeld:

    illustratie("inloopdouche-plaatsen")
->  '<img class="illu" src="/assets/fotos/inloopdouche-800.webp" width="640" height="420"
     alt="Inloopdouche met glazen wand en douchegoot" loading="lazy">'

Waar foto's het meest opleveren, in volgorde:
  1. Hero op de homepage         - een echte badkamer zegt meer dan een illustratie
  2. De zeven dienstpagina's     - renovatie, installatie, tegelwerk, inloopdouche,
                                   toilet, onderhoud en zakelijk
  3. Voor/na                     - twee foto's van dezelfde badkamer, zelfde standpunt

Vraag ze op bij de badkamerspecialisten die zich aansluiten: zij hebben vaak
opleveringsfoto's. Leg wel vast dat je ze mag gebruiken, en vermeld ze op
/fotoverantwoording/.
"""
