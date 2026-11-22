# -*- coding: utf-8 -*-
"""
Logo van Top Badkamers als SVG.

Een eenvoudig tekstlogo: een petrolkleurige tegel met een witte waterdruppel als
beeldmerk, met daarnaast "Top" in de accentkleur (terracotta) en "Badkamers" in
petrol. De witte variant is voor donkere vlakken, zoals de footer.

De tekst staat als <text> met een vaste textLength, zodat het logo op elk systeem
even breed is. Komt er een definitief logo, vervang dan deze twee strings.
"""

PETROL = "#0b4a56"
TERRACOTTA = "#c4511f"
TERRACOTTA_LICHT = "#f0a37f"

# Waterdruppel binnen de tegel van 64 x 64.
_DRUPPEL = "M32 12.5C32 12.5 18.5 28.2 18.5 37.6a13.5 13.5 0 0 0 27 0C45.5 28.2 32 12.5 32 12.5z"
_GLANS = "M25.6 38.4a6.6 6.6 0 0 0 6.4 6.6"


def _logo(tegel, druppel, glans, top, badkamers):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 64" role="img" aria-label="Top Badkamers">'
        f'<rect x="2" y="2" width="60" height="60" rx="15" fill="{tegel}"/>'
        f'<path d="{_DRUPPEL}" fill="{druppel}"/>'
        f'<path d="{_GLANS}" fill="none" stroke="{glans}" stroke-width="3.4" stroke-linecap="round"/>'
        '<text x="78" y="44.5" textLength="248" lengthAdjust="spacingAndGlyphs" '
        'font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,\'Helvetica Neue\',Arial,sans-serif" '
        'font-size="35" font-weight="800" letter-spacing="-0.5">'
        f'<tspan fill="{top}">Top</tspan> <tspan fill="{badkamers}">Badkamers</tspan></text>'
        '</svg>'
    )


LOGO_SVG = _logo(PETROL, "#ffffff", TERRACOTTA, TERRACOTTA, PETROL)
LOGO_WIT_SVG = _logo("#ffffff", PETROL, TERRACOTTA, TERRACOTTA_LICHT, "#ffffff")

# Breedte en hoogte van de viewBox, voor de width/height-attributen van <img>.
LOGO_B, LOGO_H = 330, 64

BESTANDEN = {
    "logo.svg": LOGO_SVG,
    "logo-wit.svg": LOGO_WIT_SVG,
}
