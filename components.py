# -*- coding: utf-8 -*-
"""Herbruikbare HTML-componenten voor Top Badkamers"""

import json
from data import SITE, DIENSTEN
from illustraties import illustratie, voor_na
from foto_data import FOTOS
from data import PLAATSEN
from kaart_data import BREEDTE, HOOGTE, PADEN, PUNTEN
from merk_data import LOGO_B, LOGO_H
import html as _html

# Zet op True zodra je ECHTE reviews hebt verzameld. Verzonnen reviews op een
# live site zijn in Nederland een misleidende handelspraktijk (ACM) en Google
# straft nep-reviewmarkup af. Laat dit dus op False tot je echte klanten hebt.
SHOW_REVIEWS = False

ICONS = {
    "roller": '<path d="M4 5h11v5H4z"/><path d="M15 7.5h3.5a1.5 1.5 0 0 1 1.5 1.5v2a1.5 1.5 0 0 1-1.5 1.5H12v3"/><rect x="10" y="14" width="4" height="7" rx="1"/>',
    "house": '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/><path d="M10 21v-6h4v6"/>',
    "wood": '<path d="M3 7h18v10H3z"/><path d="M7 7v10M12 7v10M17 7v10"/>',
    "spray": '<path d="M9 8h6v13H9z"/><path d="M11 8V4h2v4"/><circle cx="18" cy="4" r="1"/><circle cx="20" cy="7" r="1"/><circle cx="18" cy="10" r="1"/>',
    "wall": '<path d="M3 5h18v14H3z"/><path d="M3 10h18M3 15h18M9 5v5M15 10v5M9 15v4"/>',
    "office": '<path d="M4 21V4h10v17"/><path d="M14 10h6v11"/><path d="M7 8h1M11 8h1M7 12h1M11 12h1M7 16h1M11 16h1M17 14h1M17 18h1"/>',
    "check": '<path d="m5 12 5 5 9-10"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "euro": '<path d="M17 6.5A6.5 6.5 0 0 0 7.2 10M17 17.5A6.5 6.5 0 0 1 7.2 14"/><path d="M4 10h8M4 14h8"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16.5 5.5a3.2 3.2 0 0 1 0 5.6M17 14.6A6 6 0 0 1 21 20"/>',
    "form": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v2h6V3"/><path d="M9 11h6M9 15h4"/>',
    "match": '<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/><path d="m8.5 11 1.8 1.8 3.4-3.6"/>',
    # Badkamer-iconen in dezelfde lijnstijl
    "druppel": '<path d="M12 3s-6.5 7.4-6.5 11.7a6.5 6.5 0 0 0 13 0C18.5 10.4 12 3 12 3z"/><path d="M9 15a3 3 0 0 0 3 3"/>',
    "douche": '<path d="M5 21V8a4.5 4.5 0 0 1 9 0v1"/><path d="M10 13a4 4 0 0 1 8 0z"/><path d="M11.5 16.5v1.5M14 16.5v3M16.5 16.5v1.5"/>',
    "toilet": '<rect x="5" y="3" width="6" height="8" rx="1.2"/><path d="M3.5 11h16a6 6 0 0 1-6 6h-4a6 6 0 0 1-6-6z"/><path d="M9 17l-.5 4h6l-.5-4"/>',
    "tegels": '<rect x="3.5" y="3.5" width="17" height="17" rx="1.6"/><path d="M12 3.5v17M3.5 12h17"/>',
    "kraan": '<path d="M3 7v6"/><path d="M3 10h9a4 4 0 0 1 4 4v1.5"/><path d="M9 10V6.5M6.5 6.5h5"/><path d="M16 18.5s-1.4 1.6-1.4 2.4a1.4 1.4 0 0 0 2.8 0c0-.8-1.4-2.4-1.4-2.4z"/>',
    "bad": '<path d="M3 12h18v2.5a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M6 12V5.5a2.5 2.5 0 0 1 5 0"/><path d="M7 19.5 6 21M17 19.5l1 1.5"/>',
}


def _klein(n):
    """Kleine 400px-variant in de srcset, als die bestaat (scheelt veel op mobiel)."""
    import os
    pad = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos", f"{n}-400.webp")
    return f"/assets/fotos/{n}-400.webp 400w, " if os.path.exists(pad) else ""


def foto(f, sizes, boven_vouw=False):
    """Responsieve <img> voor een foto uit foto_data.py."""
    n = f["naam"]
    laden = 'loading="eager" fetchpriority="high"' if boven_vouw else 'loading="lazy"'
    alt = f["alt"].replace("&", "&amp;").replace('"', "&quot;")
    return (f'<figure class="foto"><img src="/assets/fotos/{n}-800.webp" '
            f'srcset="{_klein(n)}/assets/fotos/{n}-800.webp 800w, /assets/fotos/{n}-1600.webp 1600w" '
            f'sizes="{sizes}" width="{f["w"]}" height="{f["h"]}" alt="{alt}" {laden} decoding="async"></figure>')


def icon(name, size=23):
    p = ICONS.get(name, ICONS["check"])
    return (
        f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
        f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>'
    )


def eur(n):
    return f"€{n:,}".replace(",", ".")


# ---------------------------------------------------------------------------
# Head / header / footer
# ---------------------------------------------------------------------------

def head(title, description, canonical, jsonld=None, depth_ok=True, noindex=False):
    ld = ""
    if jsonld:
        blocks = jsonld if isinstance(jsonld, list) else [jsonld]
        for b in blocks:
            ld += '<script type="application/ld+json">' + json.dumps(b, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{SITE['url']}{canonical}">
{robots}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE['naam']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{SITE['url']}{canonical}">
<meta property="og:locale" content="nl_NL">
<meta name="theme-color" content="#0b4a56">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml"><meta property="og:image" content="https://joukesluimer.github.io/topbadkamers/assets/merk/logo.svg">
<link rel="stylesheet" href="/assets/css/style.css">
{ld}
</head>"""


def header():
    diensten_nav = ""
    return f"""<header class="header">
<div class="wrap header-in">
  <a class="logo" href="/" aria-label="Top Badkamers, naar de homepage">
    <img src="/assets/merk/logo.svg" alt="Top Badkamers" width="{LOGO_B}" height="{LOGO_H}">
  </a>
  <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="hoofdmenu"><span></span><span></span><span></span></button>
  <nav class="nav" id="hoofdmenu" aria-label="Hoofdmenu">
    <a href="/diensten/"><span class="nav-ic">{icon('druppel', 20)}</span>Diensten</a>
    <a href="/kosten/"><span class="nav-ic">{icon('euro', 20)}</span>Wat kost het?</a>
    <a href="/tools/"><span class="nav-ic">{icon('form', 20)}</span>Tools</a>
    <a href="/kennisbank/"><span class="nav-ic">{icon('check', 20)}</span>Kennisbank</a>
    <a href="/voor-badkamerspecialisten/"><span class="nav-ic">{icon('users', 20)}</span>Voor badkamerspecialisten</a>
    <a class="btn btn-primary" href="/offerte-aanvragen/">Offertes aanvragen</a>
    <p class="nav-noot">Gratis en vrijblijvend · maximaal 3 specialisten</p>
  </nav>
</div>
</header>{diensten_nav}"""


def footer():
    dl = "".join(f'<li><a href="/diensten/{d["slug"]}/"><span class="f-ic">{dienst_icoon(d["slug"], 18)}</span>{d["naam"]}</a></li>' for d in DIENSTEN)
    pl = "".join(f'<li><a href="/badkamerspecialist/{p["slug"]}/">{p["naam"]}</a></li>'
                 for p in sorted((p for p in PLAATSEN if p["prio"] == 1), key=lambda x: x["naam"]))
    return f"""<footer class="footer">
<div class="footer-golf" aria-hidden="true"></div>
<div class="wrap">
  <div class="footer-cta">
    <div>
      <p class="footer-cta-titel">Eén aanvraag, maximaal drie offertes</p>
      <p>Gratis en vrijblijvend. Je kiest zelf of je met een van de specialisten verder gaat.</p>
    </div>
    <a class="btn btn-primary" href="/offerte-aanvragen/">Offertes aanvragen</a>
  </div>
  <div class="footer-grid">
    <div>
      <a class="logo" href="/" aria-label="Top Badkamers, naar de homepage"><img src="/assets/merk/logo-wit.svg" alt="Top Badkamers" width="{LOGO_B}" height="{LOGO_H}" loading="lazy"></a>
      <p style="margin-top:14px;max-width:34ch">Vergelijk vrijblijvend offertes van badkamerspecialisten bij jou in de buurt. Gratis, zonder verplichtingen en met maximaal drie bedrijven die contact opnemen.</p>
    </div>
    <div>
      <h2 class="fh">Diensten</h2>
      <ul class="footer-diensten">{dl}</ul>
    </div>
    <div>
      <h2 class="fh">Handig</h2>
      <ul>
        <li><a href="/prijzen/">Prijzen &amp; tarieven</a></li>
        <li><a href="/kosten/">Kosten per klus</a></li>
        <li><a href="/badkamerspullen/">Badkamerspullen kiezen</a></li>
        <li><a href="/kennisbank/">Kennisbank</a></li>
        <li><a href="/tools/badkamercalculator/">Badkamercalculator</a></li>
        <li><a href="/tools/">Alle gratis tools</a></li>
        <li><a href="/werkgebied/">Alle plaatsen</a></li>
        <li><a href="/over-ons/">Over Top Badkamers</a></li>
        <li><a href="/contact/">Contact</a></li>
      </ul>
      <h2 class="fh" style="margin-top:22px">Badkamerspecialisten</h2>
      <ul>
        <li><a href="/voor-badkamerspecialisten/">Voor badkamerspecialisten</a></li>
        <li><a href="/voor-badkamerspecialisten/#aanmelden">Aanmelden als specialist</a></li>
      </ul>
    </div>
    <div>
      <h2 class="fh">Werkgebied</h2>
      <ul class="footer-plaatsen">{pl}</ul>
      <p style="margin-top:10px"><a href="/werkgebied/" class="footer-meer">Alle {len(PLAATSEN)} plaatsen →</a></p>
    </div>
  </div>
  <div class="footer-bot">
    <div>© {SITE['oprichting']}–2026 {SITE['naam']} · KvK {SITE['kvk']}</div>
    <div><a href="/privacy/">Privacy</a> · <a href="/voorwaarden/">Algemene voorwaarden</a> · <a href="/cookies/">Cookies</a> · <button type="button" class="cookie-instellingen">Cookie-instellingen</button> · <a href="/fotoverantwoording/">Fotoverantwoording</a></div>
  </div>
</div>
</footer>"""


def sticky_cta(label="Gratis offertes aanvragen"):
    return f'<div class="sticky-cta"><a class="btn btn-primary btn-block" href="/offerte-aanvragen/">{label}<span class="pijl" aria-hidden="true">→</span></a></div>'


def scripts():
    return ('<script src="/assets/js/config.js"></script><script src="/assets/js/toestemming.js" defer></script>'
            '<script src="/assets/js/app.js" defer></script>')


HONEYPOT = (
    '<div aria-hidden="true" style="position:absolute;left:-9999px;top:-9999px">'
    '<label>Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label>'
    '</div>'
)


def page(title, description, canonical, body, jsonld=None, body_attrs="", noindex=False):
    # Honeypot in elk formulier: bots vullen dit veld, echte bezoekers zien het niet.
    body = body.replace(" novalidate>", " novalidate>" + HONEYPOT)
    return (
        head(title, description, canonical, jsonld, noindex=noindex)
        + f"<body{(' ' + body_attrs) if body_attrs else ''}>"
        + header() + body + footer() + sticky_cta() + scripts()
        + "</body></html>"
    )


# ---------------------------------------------------------------------------
# Kruimelpad
# ---------------------------------------------------------------------------

def title(base, brand=" | Top Badkamers", limit=60):
    """Houdt de <title> onder de 60 zichtbare tekens; laat de merknaam vallen als het niet past."""
    vis = len(base.replace("&amp;", "&").replace("&#39;", "'"))
    return base + brand if vis + len(brand) <= limit else base


def desc(*zinnen, limit=158):
    """Bouwt een meta description uit losse zinnen en laat achterste zinnen vallen
    zodra het geheel boven de limiet komt. Zo blijft elke description compleet."""
    zinnen = [z.strip() for z in zinnen if z and z.strip()]
    out = []
    for z in zinnen:
        kandidaat = " ".join(out + [z])
        if len(kandidaat) <= limit:
            out.append(z)
    return " ".join(out) if out else zinnen[0][:limit]


def crumbs(items):
    """items = [(label, url|None), ...] — laatste item is de huidige pagina."""
    parts = [f'<a href="{url}">{label}</a>' if url else label for label, url in items]
    html = '<div class="wrap crumbs">' + '<span>›</span>'.join(parts) + "</div>"
    ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": lbl,
             **({"item": SITE["url"] + url} if url else {})}
            for i, (lbl, url) in enumerate(items)
        ],
    }
    return html, ld


# ---------------------------------------------------------------------------
# Offerteformulier (multi-step)
# ---------------------------------------------------------------------------

def offerte_form(title="Ontvang gratis 3 offertes", sub="Gratis · vrijblijvend · maximaal 3 badkamerspecialisten"):
    dienstkeuze = "".join(
        f'<label><input type="radio" name="dienst" value="{d["naam"]}" data-required><span>{d["naam"]}</span></label>'
        for d in DIENSTEN
    )
    return f"""
<div class="formcard" id="offerte">
  <h2>{title}</h2>
  <p class="sub">{sub}</p>
  <div class="steps"><div class="on"></div><div></div><div></div><div></div></div>

  <form data-wizard data-table="leads" novalidate>

    <div class="step active" data-autoadvance="1">
      <div class="field">
        <label>Wat wil je laten doen?</label>
        <div class="choice">{dienstkeuze}</div>
      </div>
      <div class="err"></div>
      <div class="formnav"><button type="button" class="btn btn-primary" data-next>Volgende</button></div>
    </div>

    <div class="step">
      <div class="row2">
        <div class="field">
          <label for="f-postcode">Postcode</label>
          <input type="text" id="f-postcode" name="postcode" placeholder="3892 AA" required autocomplete="postal-code">
        </div>
        <div class="field">
          <label for="f-plaats">Plaats</label>
          <input type="text" id="f-plaats" name="plaats" placeholder="Zeewolde" required autocomplete="address-level2">
        </div>
      </div>
      <div class="field">
        <label>Om wat voor pand gaat het?</label>
        <div class="choice">
          <label><input type="radio" name="pandtype" value="Koopwoning" data-required><span>Koopwoning</span></label>
          <label><input type="radio" name="pandtype" value="Huurwoning" data-required><span>Huurwoning</span></label>
          <label><input type="radio" name="pandtype" value="Appartement / VvE" data-required><span>Appartement / VvE</span></label>
          <label><input type="radio" name="pandtype" value="Bedrijfspand" data-required><span>Bedrijfspand</span></label>
        </div>
      </div>
      <div class="err"></div>
      <div class="formnav">
        <button type="button" class="btn btn-ghost" data-prev>Terug</button>
        <button type="button" class="btn btn-primary" data-next>Volgende</button>
      </div>
    </div>

    <div class="step">
      <div class="field">
        <label>Hoe groot is de klus ongeveer?</label>
        <div class="choice">
          <label><input type="radio" name="omvang" value="Klein (één onderdeel, zoals toilet, kraan of kitwerk)" data-required><span>Klein</span></label>
          <label><input type="radio" name="omvang" value="Gemiddeld (badkamer tot ongeveer 6 m²)" data-required><span>Gemiddeld</span></label>
          <label><input type="radio" name="omvang" value="Groot (grote badkamer of meerdere ruimtes)" data-required><span>Groot</span></label>
          <label><input type="radio" name="omvang" value="Weet ik niet, graag advies" data-required><span>Weet ik nog niet</span></label>
        </div>
      </div>
      <div class="field">
        <label>Wanneer wil je het laten uitvoeren?</label>
        <div class="choice">
          <label><input type="radio" name="planning" value="Zo snel mogelijk" data-required><span>Zo snel mogelijk</span></label>
          <label><input type="radio" name="planning" value="Binnen 1-3 maanden" data-required><span>Binnen 1–3 maanden</span></label>
          <label><input type="radio" name="planning" value="Over 3-6 maanden" data-required><span>Over 3–6 maanden</span></label>
          <label><input type="radio" name="planning" value="Nog aan het oriënteren" data-required><span>Ik oriënteer me</span></label>
        </div>
      </div>
      <div class="field">
        <label for="f-oms">Korte omschrijving <span class="hint">— optioneel, maar het levert je scherpere offertes op</span></label>
        <textarea id="f-oms" name="omschrijving" placeholder="Bijvoorbeeld: badkamer van 2 bij 2,5 meter uit 1995. Het bad mag eruit, er komt een inloopdouche en een nieuw hangtoilet."></textarea>
      </div>
      <div class="err"></div>
      <div class="formnav">
        <button type="button" class="btn btn-ghost" data-prev>Terug</button>
        <button type="button" class="btn btn-primary" data-next>Volgende</button>
      </div>
    </div>

    <div class="step">
      <div class="field">
        <label for="f-naam">Naam</label>
        <input type="text" id="f-naam" name="naam" required autocomplete="name" placeholder="Voor- en achternaam">
      </div>
      <div class="row2">
        <div class="field">
          <label for="f-mail">E-mailadres</label>
          <input type="email" id="f-mail" name="email" required autocomplete="email" placeholder="naam@email.nl">
        </div>
        <div class="field">
          <label for="f-tel">Telefoonnummer</label>
          <input type="tel" id="f-tel" name="telefoon" required autocomplete="tel" placeholder="06 12345678">
        </div>
      </div>
      <div class="err"></div>
      <div class="formnav">
        <button type="button" class="btn btn-ghost" data-prev>Terug</button>
        <button type="submit" class="btn btn-primary" data-submit>Verstuur aanvraag</button>
      </div>
      <p class="formfoot">Door te versturen ga je akkoord met onze <a href="/voorwaarden/">voorwaarden</a> en <a href="/privacy/">privacyverklaring</a>. Je gegevens gaan naar maximaal 3 badkamerspecialisten uit jouw regio, die ons betalen om je aanvraag te ontvangen. Andere partijen krijgen ze niet.</p>
    </div>
  </form>

  <div class="success">
    <div class="big">{icon('check', 26)}</div>
    <h2>Aanvraag ontvangen</h2>
    <p>We zoeken nu badkamerspecialisten in jouw regio die bij deze klus passen. Je krijgt meteen een bevestiging per mail. De specialisten nemen daarna zelf contact met je op. Houd ook je spambox even in de gaten.</p>
    <p><a class="btn btn-ghost" href="/prijzen/">Bekijk alvast wat een badkamer kost</a></p>
  </div>
</div>"""


# ---------------------------------------------------------------------------
# Blokken
# ---------------------------------------------------------------------------

def hoe_werkt_het(plaats=None):
    waar = f" in {plaats}" if plaats else ""
    return f"""<section class="section soft">
<div class="wrap">
  <div class="center" style="max-width:640px;margin:0 auto 44px">
    <span class="badge">In 3 stappen</span>
    <h2>Zo {streep("werkt")} het</h2>
    <p class="lead">Eén aanvraag, meerdere prijzen. Je hoeft niet zelf bedrijf voor bedrijf af te bellen.</p>
  </div>
  <ol class="steps3">
    <li class="reveal">
      <span class="step-ic">{icon('form', 26)}</span>
      <h3>Vertel wat je nodig hebt</h3>
      <p>Vier korte vragen over de klus, het pand en de planning. Klaar in ongeveer een minuut.</p>
    </li>
    <li class="reveal reveal-d1">
      <span class="step-ic">{icon('match', 26)}</span>
      <h3>Wij zoeken de match</h3>
      <p>We koppelen je aanvraag aan maximaal drie badkamerspecialisten{waar} die dit soort werk doen.</p>
    </li>
    <li class="reveal reveal-d2">
      <span class="step-ic">{icon('check', 26)}</span>
      <h3>Vergelijk en kies zelf</h3>
      <p>Je ontvangt de offertes rechtstreeks van de specialisten. Bevalt het niet? Dan zeg je gewoon nee. Je zit nergens aan vast.</p>
    </li>
  </ol>
</div>
</section>"""


def waarom_blok():
    items = [
        ("shield", "Gecontroleerde bedrijven",
         "We werken alleen met badkamerbedrijven met een geldige KvK-inschrijving en een aansprakelijkheidsverzekering. Bij klachten stoppen we de samenwerking."),
        ("euro", "Prijzen lopen uiteen",
         "Voor dezelfde badkamer kunnen offertes flink verschillen, en uit één offerte zie je dat niet. Met meerdere offertes zie je wat een redelijke prijs is."),
        ("clock", "Geen belrondes",
         "Je vult één keer in wat je wilt. Wij sturen je aanvraag door naar specialisten in jouw regio, zodat je niet zelf bedrijf voor bedrijf hoeft te bellen."),
        ("users", "Maximaal 3 specialisten",
         "Genoeg om echt te kunnen vergelijken, weinig genoeg om niet plat gebeld te worden. Je nummer gaat nooit naar meer partijen dan dat."),
    ]
    cards = "".join(
        f'<div class="card reveal reveal-d{n%4}"><div class="ic">{icon(i)}</div><h3>{t}</h3><p>{p}</p></div>'
        for n, (i, t, p) in enumerate(items)
    )
    return f"""<section class="section">
<div class="wrap">
  <div class="center" style="max-width:620px;margin:0 auto 40px">
    <span class="badge">Waarom wij</span>
    <h2>Waarom via {streep("Top Badkamers")}</h2>
    <p class="lead">Omdat je aan één offerte niet ziet of je een goede prijs betaalt.</p>
  </div>
  <div class="grid g4">{cards}</div>
  {feiten_blok([
      ("€0", "betaal je voor een aanvraag; de specialisten betalen ons"),
      ("3", "specialisten maximaal krijgen je aanvraag"),
      ("4", "korte vragen, en je aanvraag staat"),
      (str(len(PLAATSEN)), "plaatsen in ons werkgebied"),
  ])}
</div>
</section>"""


def dienst_cards(plaats_slug=None, plaats_naam=None, exclude=None):
    out = []
    for d in DIENSTEN:
        if exclude and d["slug"] == exclude:
            continue
        url = f"/badkamerspecialist/{plaats_slug}/{d['slug']}/" if plaats_slug else f"/diensten/{d['slug']}/"
        titel = f"{d.get('naam_lang', d['naam'])}{' in ' + plaats_naam if plaats_naam else ''}"
        chip = f'<span class="card-chip">{dienst_icoon(d["slug"], 27)}</span></figure>'
        beeld = (foto(FOTOS[d["slug"]]["hero"], "(max-width:600px) 92px, (max-width:900px) 45vw, 340px").replace("</figure>", chip)
                 if d["slug"] in FOTOS else illustratie(d["slug"]))
        out.append(
            f'<a class="card card-dienst reveal" href="{url}">'
            f'{beeld}'
            f"<h3>{titel}</h3><p>{d['kort']}</p>"
            f'<div class="price">Vanaf {eur(d["prijs_van"])} {d["prijs_eenheid"]}</div>'
            f'<p style="margin:10px 0 0"><span class="go">Bekijk &amp; vraag offertes aan →</span></p></a>'
        )
    return '<div class="grid g3">' + "".join(out) + "</div>"


def faq_blok(faqs, titel="Veelgestelde vragen"):
    items = "".join(
        f"<details><summary>{q}</summary><div class=\"a\"><p>{a}</p></div></details>"
        for q, a in faqs
    )
    html = f"""<section class="section">
<div class="wrap narrow">
  <h2>{titel}</h2>
  <div class="faq">{items}</div>
</div>
</section>"""
    ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }
    return html, ld


def cta_blok(titel="Klaar om te vergelijken?", tekst=None, knop="Gratis offertes aanvragen"):
    tekst = tekst or "Vul in een minuut het formulier in en ontvang vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio."
    return f"""<section class="section">
<div class="wrap">
  <div class="cta">
    <h2>{titel}</h2>
    <p>{tekst}</p>
    <a class="btn btn-primary btn-lg" href="/offerte-aanvragen/">{knop}</a>
  </div>
</div>
</section>"""


# Uitleg onder de schuif per dienst. Ontbreekt een dienst, dan blijft de uitleg leeg.
CALC_UITLEG = {
    "badkamer-renoveren": "Sloop, leidingwerk, tegelwerk en sanitair samen. De grootte van de badkamer en het sanitair dat je kiest maken het grootste verschil.",
    "badkamer-installeren": "Bijvoorbeeld een wastafelmeubel, kranen, een douche of een bad plaatsen op bestaande aansluitingen.",
    "tegelwerk-badkamer": "Tel wanden en vloer samen: een badkamer van 2 bij 2,5 meter heeft al snel 25 tot 30 m² tegelwerk.",
    "inloopdouche-plaatsen": "De afvoer, het tegelwerk en het type douchewand bepalen grotendeels de prijs.",
    "toilet-renoveren": "Een hangtoilet met inbouwreservoir kost meer dan een staand toilet, maar is makkelijker schoon te houden.",
    "badkamer-onderhoud": "Bij kitwerk en voegen telt vooral het aantal meters en de staat van de ondergrond.",
    "zakelijk-badkamers": "Bij grotere projecten, zoals meerdere badkamers in een VvE, werkt een specialist meestal met een vaste aanneemsom.",
}


def _calc_omvang(d):
    """(min, max, start, eenheid) voor de schuif, afgeleid uit de prijseenheid in data.py.

    Bij een vaste prijs (per badkamer, per toilet, per klus) is min gelijk aan max;
    de JavaScript verbergt de schuif dan en toont alleen de prijsrange."""
    e = d.get("prijs_eenheid", "").lower()
    if "m²" in e or "m2" in e:
        return (2, 60, 25, "m²") if "tegel" in d["slug"] else (2, 20, 6, "m²")
    if "uur" in e:
        return (4, 80, 16, "uren")
    if "meter" in e or " m " in e + " ":
        return (2, 40, 10, "meter")
    return (1, 1, 1, "")


def calculator():
    """Prijsindicator. Rekent met dezelfde richtprijzen als de rest van de site."""
    opties = ""
    for d in DIENSTEN:
        mn, mx, start, eenheid = _calc_omvang(d)
        uitleg = _html.escape(CALC_UITLEG.get(d["slug"], ""), quote=True)
        opties += (f'<option value="{d["slug"]}" data-van="{d["prijs_van"]}" data-tot="{d["prijs_tot"]}" '
                   f'data-min="{mn}" data-max="{mx}" data-start="{start}" data-eenheid="{eenheid}" '
                   f'data-uitleg="{uitleg}">{d["naam"]}</option>')
    eerste = _calc_omvang(DIENSTEN[0])
    return f"""<div class="calc" data-calc>
  <h3>Wat kost mijn klus ongeveer?</h3>
  <div class="rij">
    <label for="calc-dienst">Klus</label>
    <select id="calc-dienst">{opties}</select>
  </div>
  <div class="rij">
    <label for="calc-omvang">Omvang</label>
    <input type="range" id="calc-omvang" min="{eerste[0]}" max="{eerste[1]}" value="{eerste[2]}" step="1">
    <span class="waarde" data-aantal></span>
  </div>
  <div class="calc-uit">
    <div class="bedrag" data-bedrag></div>
    <div class="sub" data-sub></div>
  </div>
  <p style="margin:18px 0 0;font-size:.88rem;color:var(--muted)">
    Indicatie inclusief materiaal en btw. De echte prijs hangt af van de staat
    van de bestaande badkamer, het leidingwerk en het sanitair dat je kiest. <a href="/offerte-aanvragen/">Vraag gratis drie offertes aan</a>
    voor een prijs die op jouw situatie klopt, of <a data-cta href="/diensten/{DIENSTEN[0]['slug']}/">lees waar de prijs door bepaald wordt</a>.
  </p>
</div>"""


def prijstabel(diensten=None, plaats=None):
    """Zonder plaats: landelijke richtprijzen. Met plaats: gecorrigeerd voor de regio."""
    from data import lokale_prijs
    diensten = diensten or DIENSTEN
    rows = ""
    for d in diensten:
        van, tot = lokale_prijs(d, plaats) if plaats else (d["prijs_van"], d["prijs_tot"])
        url = f"/badkamerspecialist/{plaats['slug']}/{d['slug']}/" if plaats else f"/diensten/{d['slug']}/"
        rows += (f'<tr><td><a href="{url}">{d["naam"]}</a></td>'
                 f'<td class="num">{eur(van)} – {eur(tot)}</td>'
                 f'<td>{d["prijs_eenheid"]}</td></tr>')
    return f"""<div class="tablewrap">
<table>
<thead><tr><th>Dienst</th><th>Richtprijs</th><th>Eenheid</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p><small>Indicatieve prijzen inclusief materiaal en btw, tenzij er excl. btw staat. De werkelijke prijs hangt af van de staat van de bestaande badkamer, het leidingwerk, het sanitair en de tegels die je kiest. Vraag altijd meerdere offertes aan.</small></p>"""


# ---------------------------------------------------------------------------
# Werkgebiedkaart
# ---------------------------------------------------------------------------

def werkgebied_kaart():
    """Eigen SVG-kaart: elke plaats is een gewone link, dus zonder JavaScript werkt hij ook."""
    e = _html.escape
    links_van = {"naarden", "weesp", "bussum", "hilversum", "ermelo", "nijkerk", "amersfoort", "almere", "urk", "espel", "creil", "nagele"}
    boven = {"emmeloord"}
    provs = sorted({p["provincie"] for p in PLAATSEN})
    land = "".join(f'<path class="kl{" ka" if n in provs else ""}" d="{d}"/>' for n, d in PADEN.items())
    pts = ""
    for p in sorted(PLAATSEN, key=lambda x: x["prio"], reverse=True):
        x, y = PUNTEN[p["slug"]]
        lk = p["slug"] in links_van
        kant = "b" if p["slug"] == "kraggenburg" else "t" if p["slug"] in boven else ("l" if lk else "r")
        pts += (f'<a class="kp{" kg" if p["prio"] == 1 else ""}" href="/badkamerspecialist/{p["slug"]}/" aria-label="Badkamerspecialist {e(p["naam"])}, {e(p["provincie"])}" '
                f'data-naam="{e(p["naam"])}" data-prov="{e(p["provincie"])}" data-hook="{e(p["hook"])}" data-x="{x}" data-y="{y}" data-l="{kant}">'
                f'<circle class="kh" cx="{x}" cy="{y}" r="20"/><circle class="kd" cx="{x}" cy="{y}" r="9"/>'
                f'<text x="{x + (-16 if lk else 16)}" y="{y + 6}" text-anchor="{"middle" if kant in "tb" else "end" if lk else "start"}" font-size="24">{e(p["naam"])}</text></a>')
    knoppen = '<button type="button" class="chip-k" data-prov="" aria-pressed="true">Alle plaatsen</button>' + "".join(
        f'<button type="button" class="chip-k" data-prov="{e(n)}" aria-pressed="false">{e(n)}</button>' for n in provs)
    return f"""<div class="kaart" data-kaart data-b="{BREEDTE}" data-h="{HOOGTE}">
  <div class="kaart-knoppen" role="group" aria-label="Kaart inzoomen op provincie">{knoppen}</div>
  <div class="kaart-grid">
    <svg viewBox="0 0 {BREEDTE} {HOOGTE}" role="group" aria-label="Kaart met de {len(PLAATSEN)} plaatsen in ons werkgebied. Elke plaats is een link." preserveAspectRatio="xMidYMid slice">
      <rect class="kw" x="-500" y="-500" width="{BREEDTE + 1000}" height="{HOOGTE + 1000}"/>{land}{pts}
    </svg>
    <aside class="kaart-info" aria-live="polite">
      <p class="kaart-prov">Werkgebied</p>
      <h2 class="kaart-naam">Kies een plaats</h2>
      <p class="kaart-hook">Beweeg over de kaart of ga er met de Tab-toets doorheen. Klik op een plaats voor lokale richtprijzen en badkamerspecialisten in de buurt.</p>
      <a class="btn btn-primary kaart-link" href="/offerte-aanvragen/">Offertes aanvragen</a>
    </aside>
  </div>
  <p class="kaart-bron">Kaart: provinciegrenzen en woonplaatsen van <a href="https://www.pdok.nl/" rel="nofollow noopener">PDOK</a> (CBS en Kadaster), <a href="https://creativecommons.org/licenses/by/4.0/deed.nl" rel="nofollow noopener license">CC BY 4.0</a>, vereenvoudigd. Liever een lijst? Alle plaatsen staan hieronder.</p>
</div>"""


# ---------------------------------------------------------------------------
# Prijskaart en CTA halverwege (kosten-, plaats- en plaats-dienstpagina's)
# ---------------------------------------------------------------------------

def prijskaart(van, tot, eenheid, noot, beeld="", knop="Vergelijk offertes", extra=""):
    """Opvallende kaart met de richtprijs, optioneel met foto bovenaan."""
    return f"""<aside class="prijskaart" aria-label="Richtprijs">
  {beeld}
  <div class="prijskaart-in">
    <p class="prijskaart-kop">Richtprijs</p>
    <p class="prijskaart-bedrag">{eur(van)} <span>–</span> {eur(tot)}</p>
    <p class="prijskaart-eenheid">{eenheid}</p>
    <p class="prijskaart-noot">{noot}</p>
    <a class="btn btn-primary btn-block" href="/offerte-aanvragen/">{knop}</a>
    {extra}
  </div>
</aside>"""


def cta_midden(titel, tekst, knop="Gratis offertes aanvragen", href="/offerte-aanvragen/"):
    """Compacte oproep halverwege een lange pagina."""
    return f"""<div class="cta-midden reveal">
  <div class="cta-midden-tekst"><p class="cta-midden-titel">{titel}</p><p>{tekst}</p></div>
  <a class="btn btn-primary" href="{href}">{knop}</a>
</div>"""


# ===========================================================================
# Visuele bouwstenen (ronde 3) — herbruikbaar voor alle pagina's
# ===========================================================================
#
# Alles hieronder is pure HTML + CSS uit style.css (blok "Ronde 3" in assets.py),
# zonder extra bestanden of bibliotheken. Kort overzicht:
#
#   dienst_icoon(slug, size=28)      Eigen tweekleurig SVG-icoon per dienst.
#   streep(tekst)                    Accentstreep onder een woord in een kop:
#                                    f"<h2>Zo {streep('werkt')} het</h2>"
#   feiten_blok(feiten, bron=None)   Rij met cijfers. ALLEEN controleerbare feiten
#                                    (eigen werkwijze, wetgeving, eigen richtprijzen).
#                                    feiten = [("9%", "btw op ...", "https://bron" of None), ...]
#   stappen_blok(stappen)            Genummerde tijdlijn, voor werkwijzen en gidsen.
#                                    stappen = [("Titel", "Uitleg"), ...]
#   foto_kader(f, sizes, bijschrift) Foto uit foto_data.py met bijschrift en
#                                    makersvermelding (licentie staat op /fotoverantwoording/).
#   prijs_balken(rijen, eenheid)     Visuele prijsvergelijking uit eigen richtprijzen.
#                                    rijen = [("Label", van, tot), ...]
#
# Scrollanimaties: zet class "reveal" (en eventueel "reveal-d1".."reveal-d3") op
# een element; zonder JS of met prefers-reduced-motion staat alles gewoon stil in beeld.

DIENST_ICONEN = {
    # Elk icoon: lijnen in currentColor, vlakken met class "ia" in de accentkleur.
    # Badkamer renoveren: bad met kraan
    "badkamer-renoveren": '<path class="ia" d="M3 12h18v2.5a5 5 0 0 1-5 5H8a5 5 0 0 1-5-5z"/><path d="M2.5 12h19"/><path d="M3 12v2.5a5 5 0 0 0 5 5h8a5 5 0 0 0 5-5V12"/><path d="M6 12V5.6a2.6 2.6 0 0 1 5.2 0v.6"/><path d="M9.6 6.2h3.2"/><path d="M7 19.5 6 21M17 19.5l1 1.5"/>',
    # Badkamer installeren: kraan met druppel
    "badkamer-installeren": '<path d="M3 7.5v6"/><path d="M3 10.5h9a4 4 0 0 1 4 4V16"/><path d="M8.5 10.5V7M6 7h5"/><path class="ia" d="M16 18.2s-1.6 1.8-1.6 2.8a1.6 1.6 0 0 0 3.2 0c0-1-1.6-2.8-1.6-2.8z"/><path d="M16 18.2s-1.6 1.8-1.6 2.8a1.6 1.6 0 0 0 3.2 0c0-1-1.6-2.8-1.6-2.8z"/>',
    # Tegelwerk: tegelraster met één accenttegel
    "tegelwerk-badkamer": '<rect class="ia" x="12" y="3.5" width="8.5" height="8.5" rx="1"/><rect x="3.5" y="3.5" width="17" height="17" rx="1.6"/><path d="M12 3.5v17M3.5 12h17"/>',
    # Inloopdouche: regendouche met stralen
    "inloopdouche-plaatsen": '<path d="M4.5 21V7.5A4.5 4.5 0 0 1 9 3a4.5 4.5 0 0 1 4.5 4.5V9"/><path class="ia" d="M9.5 12.5a4 4 0 0 1 8 0z"/><path d="M9.5 12.5a4 4 0 0 1 8 0z"/><path d="M11 15.5v1.5M13.5 15.5v3M16 15.5v1.5"/>',
    # Toilet: reservoir en pot, zijaanzicht
    "toilet-renoveren": '<rect class="ia" x="4.5" y="3" width="6" height="8" rx="1.2"/><rect x="4.5" y="3" width="6" height="8" rx="1.2"/><path d="M3.5 11h16.5a6.5 6.5 0 0 1-6.5 6.5H9.5a6 6 0 0 1-6-6z"/><path d="M8.5 17.5 8 21h6l-.5-3.5"/>',
    # Onderhoud: druppel met vinkje (kitwerk, voegen, lekkage)
    "badkamer-onderhoud": '<path class="ia" d="M12 3s-6.5 7.3-6.5 11.6a6.5 6.5 0 0 0 13 0C18.5 10.3 12 3 12 3z"/><path d="M12 3s-6.5 7.3-6.5 11.6a6.5 6.5 0 0 0 13 0C18.5 10.3 12 3 12 3z"/><path d="m9.2 14.8 2 2 3.8-4"/>',
    # Zakelijk en VvE: gebouw met accentdeur
    "zakelijk-badkamers": '<path d="M4 21V4.5h10V21"/><path d="M14 10h6v11"/><path d="M7 8h1M10.5 8h1M7 11.5h1M10.5 11.5h1M17 13.5h.5M17 17h.5"/><rect class="ia" x="7.3" y="15.2" width="3.6" height="5.8" rx=".6"/><path d="M2.5 21h19"/>',
}


def dienst_icoon(slug, size=28):
    """Tweekleurig dienst-icoon; valt terug op het gewone icoon uit ICONS."""
    p = DIENST_ICONEN.get(slug)
    if not p:
        d = next((x for x in DIENSTEN if x["slug"] == slug), None)
        return icon(d["icon"] if d else "check", size)
    return (f'<svg class="dicon" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{p}</svg>')


def streep(tekst):
    """Accentstreep onder een woord of kort zinsdeel in een kop."""
    return f'<span class="streep">{tekst}</span>'


def feiten_blok(feiten, bron=None, donker=False):
    """Cijferblok. Gebruik alleen feiten die je kunt onderbouwen; geef bij wetgeving een bronlink."""
    items = ""
    for n, f in enumerate(feiten):
        waarde, label = f[0], f[1]
        url = f[2] if len(f) > 2 else None
        lbl = f'{label} <a href="{url}" rel="noopener">bron</a>' if url else label
        items += (f'<div class="feit reveal reveal-d{n % 4}"><p class="feit-getal">{waarde}</p>'
                  f'<p class="feit-label">{lbl}</p></div>')
    noot = f'<p class="feiten-noot">{bron}</p>' if bron else ""
    return f'<div class="feiten{" feiten-donker" if donker else ""}">{items}</div>{noot}'


def stappen_blok(stappen, kop_tag="h3"):
    """Visuele tijdlijn met genummerde stappen."""
    li = "".join(
        f'<li class="reveal"><span class="stap-nr" aria-hidden="true">{i + 1}</span>'
        f'<div><{kop_tag}>{t}</{kop_tag}><p>{p}</p></div></li>'
        for i, (t, p) in enumerate(stappen))
    return f'<ol class="stappen">{li}</ol>'


def foto_kader(f, sizes, bijschrift=None):
    """Foto met bijschrift en makersvermelding; de volledige licentie staat op /fotoverantwoording/."""
    img = foto(f, sizes).replace('<figure class="foto">', '').replace("</figure>", "")
    tekst = bijschrift or f["alt"]
    maker = _html.escape(f.get("maker", ""))
    credit = (f' <span class="foto-credit">Foto: <a href="/fotoverantwoording/">{maker}</a>'
              f'{", " + f["licentie"] if f.get("licentie") else ""}</span>') if maker else ""
    return f'<figure class="foto foto-kader reveal">{img}<figcaption>{tekst}{credit}</figcaption></figure>'


def prijs_balken(rijen, eenheid="", noot=None):
    """Horizontale balken van/tot, geschaald op de hoogste prijs. Alleen eigen richtprijzen gebruiken."""
    hoogste = max(t for _, _, t in rijen) or 1
    out = ""
    for label, van, tot in rijen:
        l = round(van / hoogste * 100, 1)
        b = max(round((tot - van) / hoogste * 100, 1), 2)
        out += (f'<li><span class="pb-label">{label}</span>'
                f'<span class="pb-baan" aria-hidden="true"><span class="pb-balk" style="margin-left:{l}%;width:{b}%"></span></span>'
                f'<span class="pb-bedrag">{eur(van)} – {eur(tot)}</span></li>')
    kop = f'<p class="pb-eenheid">{eenheid}</p>' if eenheid else ""
    voet = f'<p class="pb-noot">{noot}</p>' if noot else ""
    return f'<div class="prijs-balken reveal">{kop}<ul>{out}</ul>{voet}</div>'
