# -*- coding: utf-8 -*-
"""Technische vindbaarheid en snelheid van Top Badkamers (ronde 5).

Draait als laatste stap van build.py, op de kant-en-klare HTML in site/:

- nabewerken():   schema (Organization, ItemList, Service, HowTo), blok
                  "Gerelateerde pagina's", lazy-loading/decoding en een preload
                  van het hero-beeld;
- image_sitemap(): sitemap-afbeeldingen.xml voor de eigen renders.

Losse hulpmiddelen (na python3 build.py):

    python3 seo_extra.py meet    # grootte van CSS, JS en HTML
    python3 seo_extra.py audit   # titels, descriptions, H1, canonical, linkdiepte

Alles werkt op de HTML in site/, zodat de andere modules er niets voor hoeven te doen.
"""

import gzip
import json
import os
import re
import sys
from collections import Counter, defaultdict, deque

from data import SITE

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")


# ---------------------------------------------------------------------------
# Pagina's inlezen
# ---------------------------------------------------------------------------

def _pad_van(bestand):
    rel = os.path.relpath(bestand, OUT).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def paginas():
    """{pad: bestandsnaam} van alle HTML-pagina's in site/."""
    uit = {}
    for map_, _, bestanden in os.walk(OUT):
        if os.sep + "assets" in map_:
            continue
        for b in bestanden:
            if b.endswith(".html"):
                volledig = os.path.join(map_, b)
                uit[_pad_van(volledig)] = volledig
    return uit


def _lees(bestand):
    with open(bestand, encoding="utf-8") as f:
        return f.read()


def _schrijf(bestand, html):
    with open(bestand, "w", encoding="utf-8") as f:
        f.write(html)


def _tekst(fragment):
    t = re.sub(r"<[^>]+>", " ", fragment)
    t = (t.replace("&shy;", "").replace("&amp;", "&").replace("&nbsp;", " ")
          .replace("&#39;", "'").replace("&quot;", '"'))
    return re.sub(r"\s+", " ", t).strip()


def _meta(html, naam):
    m = re.search(rf'<meta name="{naam}" content="([^"]*)"', html)
    return m.group(1) if m else None


def _title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    return _tekst(m.group(1)) if m else ""


def _h1(html):
    return [_tekst(h) for h in re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.S)]


def _noindex(html):
    return 'name="robots" content="noindex' in html


def _jsonld(html):
    uit = []
    for blok in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            uit.append(json.loads(blok))
        except ValueError:
            pass
    return uit


def _types(html):
    t = []
    for b in _jsonld(html):
        for item in (b.get("@graph") or [b]) if isinstance(b, dict) else b:
            if isinstance(item, dict):
                tp = item.get("@type")
                t += tp if isinstance(tp, list) else [tp]
    return t


def _hoofdtekst(html):
    """Het deel tussen header en footer: zo tellen menu en footer niet mee."""
    a = html.find("</header>")
    b = html.rfind("<footer")
    return html[a if a > 0 else 0: b if b > 0 else len(html)]


def _links(html, alleen_hoofd=False):
    bron = _hoofdtekst(html) if alleen_hoofd else html
    uit = set()
    for href in re.findall(r'<a [^>]*href="(/[^"#?]*)', bron):
        if href.startswith("//") or href.startswith("/assets/"):
            continue
        uit.add(href if href.endswith("/") or "." in href.rsplit("/", 1)[-1] else href + "/")
    return uit


# ---------------------------------------------------------------------------
# Meten
# ---------------------------------------------------------------------------

def _gz(data):
    return len(gzip.compress(data.encode("utf-8") if isinstance(data, str) else data, 9))


def meet():
    """Grootte van CSS, JS en HTML (ruw en gzip). Geeft een dict terug en print een tabel."""
    res = {}
    for rel in ("css/style.css", "js/app.js", "js/config.js", "js/toestemming.js"):
        p = os.path.join(OUT, "assets", rel)
        if os.path.exists(p):
            d = open(p, "rb").read()
            res[rel] = (len(d), _gz(d))
    pag = paginas()
    tot = tot_gz = inline_css = inline_js = 0
    zonder_lazy = zonder_async = imgs = 0
    grootste = []
    for pad, b in pag.items():
        h = _lees(b)
        tot += len(h.encode())
        tot_gz += _gz(h)
        inline_css += sum(len(x) for x in re.findall(r"<style[^>]*>.*?</style>", h, re.S))
        inline_js += sum(len(x) for x in re.findall(r"<script(?![^>]*ld\+json)(?![^>]*src=)[^>]*>.*?</script>", h, re.S))
        for img in re.findall(r"<img\b[^>]*>", h):
            imgs += 1
            if "loading=" not in img:
                zonder_lazy += 1
            if "decoding=" not in img:
                zonder_async += 1
        grootste.append((len(h.encode()), pad))
    home = _lees(pag["/"]) if "/" in pag else ""
    res.update({
        "paginas": len(pag), "html_totaal": tot, "html_totaal_gz": tot_gz,
        "html_gem": tot // max(len(pag), 1), "html_gem_gz": tot_gz // max(len(pag), 1),
        "inline_css": inline_css, "inline_js": inline_js,
        "img": imgs, "img_zonder_loading": zonder_lazy, "img_zonder_decoding": zonder_async,
        "home": (len(home.encode()), _gz(home)),
        "grootste": sorted(grootste, reverse=True)[:5],
    })
    print(f"{'bestand':28} {'ruw':>9} {'gzip':>8}")
    for rel in ("css/style.css", "js/app.js", "js/config.js", "js/toestemming.js"):
        if rel in res:
            print(f"{rel:28} {res[rel][0]:>9,} {res[rel][1]:>8,}")
    print(f"{'homepage (HTML)':28} {res['home'][0]:>9,} {res['home'][1]:>8,}")
    print(f"{'HTML gemiddeld/pagina':28} {res['html_gem']:>9,} {res['html_gem_gz']:>8,}")
    print(f"{'HTML totaal':28} {tot:>9,} {tot_gz:>8,}")
    print(f"pagina's: {len(pag)}; inline CSS {inline_css:,} B, inline JS {inline_js:,} B (alle pagina's samen)")
    print(f"<img>: {imgs}, zonder loading= {zonder_lazy}, zonder decoding= {zonder_async}")
    print("grootste pagina's: " + ", ".join(f"{p} ({n // 1024} kB)" for n, p in res["grootste"]))
    return res


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

ONDERWERP = re.compile(r"badkamer|toilet|douche|\bbad\b|tegel|kraan|kranen|wastafel|sanitair|loodgieter|"
                       r"kit|voeg|lekkage|schimmel|spiegel|radiator|fontein|reservoir|vloerverwarming|"
                       r"microcement|terrazzo|natuursteen|marmer|offerte|specialist", re.I)


def audit(toon=True):
    """Loopt titels, descriptions, H1, canonical, breadcrumb en interne links na."""
    pag = paginas()
    info = {}
    for pad, b in pag.items():
        h = _lees(b)
        info[pad] = {
            "title": _title(h), "desc": _meta(h, "description") or "", "h1": _h1(h),
            "canonical": bool(re.search(r'<link rel="canonical" href="[^"]+"', h)),
            "crumb": "BreadcrumbList" in _types(h) or 'class="wrap crumbs"' in h,
            "noindex": _noindex(h), "links": _links(h), "hoofdlinks": _links(h, True),
        }
    idx = {p: i for p, i in info.items() if not i["noindex"]}
    problemen = defaultdict(list)
    for p, i in idx.items():
        t, d = i["title"], i["desc"]
        if len(t) > 62:
            problemen["title langer dan 62 (norm van verify.py)"].append(f"{p} ({len(t)})")
        if len(t) < 25:
            problemen["title korter dan 25"].append(f"{p} ({len(t)})")
        d = _tekst(d)
        if not 110 <= len(d) <= 175:
            problemen["description buiten 110-175 (norm van verify.py)"].append(f"{p} ({len(d)})")
        elif len(d) > 160:
            problemen["description 161-175: kan in Google worden afgekapt"].append(f"{p} ({len(d)})")
        if not ONDERWERP.search(t) and p != "/":
            problemen["geen onderwerpwoord (badkamer, toilet, douche ...) in de title"].append(p)
        if len(i["h1"]) != 1:
            problemen[f"aantal H1 is niet 1"].append(f"{p} ({len(i['h1'])})")
        if not i["canonical"]:
            problemen["geen canonical"].append(p)
        if not i["crumb"] and p != "/":
            problemen["geen breadcrumb"].append(p)
        if i["h1"] and t and i["h1"][0].lower() == t.split(" | ")[0].lower():
            problemen["H1 precies gelijk aan title (mag, maar is een gemiste kans)"].append(p)
    for veld in ("title", "desc"):
        c = Counter(i[veld] for i in idx.values())
        for waarde, n in c.items():
            if n > 1:
                problemen[f"dubbele {veld}"].append(f"{waarde[:60]} ({n}x)")

    # Linkdiepte vanaf de homepage (alle links, ook menu en footer) en inlinks
    # uit de hoofdtekst (zonder menu en footer: dat zijn de 'echte' contextlinks).
    diepte = {"/": 0}
    rij = deque(["/"])
    while rij:
        p = rij.popleft()
        for q in info.get(p, {}).get("links", ()):
            if q in info and q not in diepte:
                diepte[q] = diepte[p] + 1
                rij.append(q)
    inlinks = Counter()
    for p, i in info.items():
        for q in i["hoofdlinks"]:
            if q != p:
                inlinks[q] += 1
    diepteverdeling = Counter(diepte.get(p, -1) for p in idx)
    weinig = sorted((inlinks[p], p) for p in idx if p != "/")
    if toon:
        print(f"Indexeerbare pagina's: {len(idx)} (van {len(info)})")
        for soort, lijst in sorted(problemen.items()):
            print(f"\n--- {soort}: {len(lijst)}")
            for r in lijst[:12]:
                print("   ", r)
            if len(lijst) > 12:
                print(f"    ... en nog {len(lijst) - 12}")
        print("\n--- Linkdiepte vanaf de homepage (klikken: aantal pagina's)")
        for d, n in sorted(diepteverdeling.items()):
            print(f"    {'niet bereikbaar' if d < 0 else d}: {n}")
        print("\n--- Minste contextlinks (uit de hoofdtekst, zonder menu/footer)")
        verdeling = Counter(min(n, 5) for n, _ in weinig)
        print("    " + ", ".join(f"{k if k < 5 else '5+'} inlinks: {v}" for k, v in sorted(verdeling.items())))
        for n, p in weinig[:20]:
            print(f"    {n:>3}  {p}")
    return {"problemen": problemen, "diepte": diepteverdeling, "inlinks": inlinks, "info": info}


# ---------------------------------------------------------------------------
# Schema (JSON-LD). Geen review- of rating-schema: we hebben geen echte reviews.
# ---------------------------------------------------------------------------

def _ld_script(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"


def _abs(url):
    return SITE["url"] + url if url.startswith("/") else url


def _ld_bewerk(html, functie):
    """Roept functie(obj) aan voor elk JSON-LD-blok; geeft het obj terug of None (ongewijzigd)."""
    def vervang(m):
        try:
            obj = json.loads(m.group(1))
        except ValueError:
            return m.group(0)
        nieuw = functie(obj)
        return m.group(0) if nieuw is None else _ld_script(nieuw)
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', vervang, html, flags=re.S)


def _voeg_ld_toe(html, obj):
    return html.replace("</head>", _ld_script(obj) + "\n</head>", 1)


def _organization_logo(obj):
    if obj.get("@type") != "Organization" or "logo" in obj:
        return None
    obj["logo"] = {"@type": "ImageObject", "url": _abs("/assets/fotos/merk/apple-touch-icon.png"),
                   "width": 180, "height": 180}
    obj["image"] = _abs("/assets/fotos/merk/og-image.png")
    return obj


def _itemlist_absoluut(obj):
    """ItemList-urls moeten volledig zijn (https://...), niet /pad/."""
    tekst = json.dumps(obj, ensure_ascii=False)
    if '"url": "/' not in tekst:
        return None

    def loop(o):
        if isinstance(o, dict):
            return {k: (_abs(v) if k == "url" and isinstance(v, str) else loop(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [loop(x) for x in o]
        return o
    return loop(obj)


# Overzichtspagina's waarvan de kinderen niet direct onder het eigen pad staan.
KINDEREN_ELDERS = {"/werkgebied/": "/badkamerspecialist/"}


def _is_kind(ouder, pad):
    basis = KINDEREN_ELDERS.get(ouder, ouder)
    if not pad.startswith(basis) or pad == basis:
        return False
    return pad[len(basis):].strip("/").count("/") == 0


def _itemlist(pad, html, alle, h1s):
    """ItemList van de kindpagina's die in de hoofdtekst gelinkt staan, in volgorde van de pagina."""
    gezien, items = set(), []
    for href in re.findall(r'<a [^>]*href="(/[^"#?]*)"', _hoofdtekst(html)):
        if href in alle and href not in gezien and _is_kind(pad, href):
            gezien.add(href)
            items.append(href)
    if len(items) < 3:
        return None
    return {
        "@context": "https://schema.org", "@type": "ItemList",
        "name": h1s.get(pad) or _title(html),
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": _abs(u), "name": h1s.get(u, u)}
            for i, u in enumerate(items)],
    }


# HowTo alleen bij echte stappenplannen (iets wat de lezer zelf in een vaste volgorde doet),
# niet bij keuze-checklists. pad: (naam van de HowTo, kop boven het <ol class="stappen">-blok)
HOWTO = {
    "/kennisbank/badkamer-kitten/": ("Badkamer kitten in vijf stappen", "Checklist kitten"),
    "/kennisbank/volgorde-badkamerrenovatie/": ("De volgorde van een badkamerrenovatie", "De volgorde in het kort"),
    "/kennisbank/lekkage-badkamer/": ("Wat doe je bij lekkage in de badkamer?", "Stappenplan bij lekkage"),
    "/kennisbank/schimmel-in-badkamer/": ("Schimmel in de badkamer aanpakken", "Zo pak je het aan"),
    "/kennisbank/asbest-in-badkamer/": ("Een oude badkamer veilig slopen bij mogelijk asbest", "Stappen bij een oude badkamer"),
    "/kennisbank/inloopdouche-zonder-drempel/": ("Een drempelloze inloopdouche laten maken", "Stappen voor een drempelloze inloopdouche"),
    "/kennisbank/verbouwen-in-vve/": ("Je badkamer verbouwen in een VvE", "Stappenplan voor een badkamer in een VvE"),
    "/kennisbank/badkamer-schoonmaken/": ("Je badkamer snel schoonhouden", "Snelle routine"),
    "/kennisbank/badkamer-ventilatie/": ("De ventilatie van je badkamer checken", "Snelle check van je ventilatie"),
    "/kennisbank/kleine-badkamer-indelen/": ("Een kleine badkamer indelen", "Zo pak je de indeling aan"),
}


def _howto(pad, html):
    naam, kop = HOWTO[pad]
    m = re.search(r"<h[23][^>]*>\s*" + re.escape(kop) + r"\s*</h[23]>(.*?)</ol>", html, re.S)
    if not m or '<ol class="stappen">' not in m.group(1):
        return None
    lijst = m.group(1).split('<ol class="stappen">', 1)[1]
    stappen = re.findall(r"<li[^>]*>.*?<h[34]>(.*?)</h[34]>\s*<p>(.*?)</p>", lijst, re.S)
    if len(stappen) < 3:
        return None
    return {
        "@context": "https://schema.org", "@type": "HowTo", "name": naam, "inLanguage": "nl-NL",
        "url": _abs(pad),
        "step": [{"@type": "HowToStep", "position": i + 1, "name": _tekst(t), "text": _tekst(p)}
                 for i, (t, p) in enumerate(stappen)],
    }


def _service(pad, html, h1):
    """Service voor een dienstpagina die er (nog) geen heeft. Zonder prijzen of ratings."""
    return {
        "@context": "https://schema.org", "@type": "Service", "name": h1, "serviceType": h1,
        "url": _abs(pad), "provider": {"@id": SITE["url"] + "/#organization"},
        "areaServed": {"@type": "Country", "name": "Nederland"},
        "description": _meta(html, "description") or h1,
    }


def schema(alle):
    """Voegt ontbrekend schema toe aan de pagina's in site/. Geeft een telling terug."""
    teller = Counter()
    h1s = {}
    for pad, b in alle.items():
        h = _h1(_lees(b))
        if h:
            h1s[pad] = h[0]
    for pad, b in alle.items():
        html = oud = _lees(b)
        if _noindex(html):
            continue
        if pad == "/":
            html = _ld_bewerk(html, _organization_logo)
            if html != oud:
                teller["Organization-logo"] += 1
        voor = html
        html = _ld_bewerk(html, _itemlist_absoluut)
        if html != voor:
            teller["ItemList-urls absoluut"] += 1
        typen = _types(html)
        heeft_itemlist = '"ItemList"' in html
        if not heeft_itemlist and pad != "/" and any(_is_kind(pad, q) for q in alle):
            il = _itemlist(pad, html, alle, h1s)
            if il:
                html = _voeg_ld_toe(html, il)
                teller["ItemList"] += 1
        if pad.startswith("/diensten/") and pad.count("/") == 3 and "Service" not in typen and pad in h1s:
            html = _voeg_ld_toe(html, _service(pad, html, h1s[pad]))
            teller["Service"] += 1
        if pad in HOWTO and "HowTo" not in typen:
            ht = _howto(pad, html)
            if ht:
                html = _voeg_ld_toe(html, ht)
                teller["HowTo"] += 1
            else:
                print(f"  ! seo_extra: HowTo-stappen niet gevonden op {pad}")
        if html != oud:
            _schrijf(b, html)
    return teller


# ---------------------------------------------------------------------------
# Blok "Gerelateerde pagina's" onder contentpagina's
# ---------------------------------------------------------------------------

RUBRIEK = {
    "kennisbank": "Kennisbank", "kosten": "Wat kost het?", "badkamerspullen": "Kopersgids",
    "inspiratie": "Inspiratie", "materialen": "Materialen", "badkamer-voor": "Voor wie",
    "diensten": "Dienst", "tools": "Gratis tool",
}
# Pagina's die het blok krijgen; doelen mogen ook diensten en tools zijn.
HOST_RUBRIEKEN = {"kennisbank", "kosten", "badkamerspullen", "inspiratie", "materialen", "badkamer-voor"}
DOEL_RUBRIEKEN = HOST_RUBRIEKEN | {"diensten", "tools"}
STOP = set("""
voor door over naar maar want zijn wordt worden heeft hebben deze die dat wat hoe welk welke
waar wanneer meer veel kies kiezen kopen alles jouw jij je met van een het als ook niet nog
zo dit bij tot uit om op in te en of de per wel dan wij ons onze eigen echt goed beter grote klein
kost kosten prijs prijzen wat-kost gratis vergelijken offerte offertes tips stappen soorten top
plaatsen verplaatsen vervangen laten kiezen kopen nieuwe badkamers
""".split())
RELATED_CSS = (".gerel{padding-top:8px}.gerel h2{font-size:1.35rem;margin:0 0 14px}"
               ".gerel-grid{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(min(240px,100%),1fr))}"
               ".gerel-grid a{display:block;padding:14px 16px;border:1px solid var(--line);border-radius:var(--radius);"
               "background:#fff;text-decoration:none;color:inherit;transition:border-color .2s}"
               ".gerel-grid a:hover{border-color:currentColor}"
               ".gerel-grid small{display:block;font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;opacity:.7;margin-bottom:3px}"
               ".gerel-grid strong{display:block;font-size:.98rem;line-height:1.3}")


# Onderwerpen: een pagina die een van deze woorden (of een samenstelling ermee) noemt,
# krijgt het onderwerp erbij. Zo vindt 'kitten' ook 'kitwerk' en 'voegen'.
THEMA = {
    "vocht": "kit kitten kitwerk voeg waterdicht lekkage schimmel ventilatie kalk onderhoud schoonmaken vocht",
    "douche": "douche drempel",
    "toilet": "toilet reservoir fontein",
    "vloerwand": "tegel microcement natuursteen terrazzo marmer keramisch beton",
    "verbouwen": "renovatie renoveren slopen sloop volgorde verbouw asbest vve huur garantie planning opknappen",
    "warmte": "vloerverwarming radiator verwarming",
    "kraan": "kraan kranen water",
    "ruimte": "klein indelen indeling ontwerp zolder suite tweede levensloop ouderen appartement",
    "bad": "vrijstaand ligbad",
    "meubel": "wastafel meubel spiegel verlichting lamp licht",
    "stijl": "stijl modern landelijk industrieel japandi scandinavisch klassiek wellness luxe sfeer",
}
_THEMA_WOORD = [(w, t) for t, ws in THEMA.items() for w in ws.split()]


def _woorden(tekst):
    return [w for w in re.findall(r"[a-zà-ÿ0-9]+", tekst.lower()) if len(w) >= 3 and w not in STOP]


def _profielen(alle):
    """Per pagina: kort label, rubriek en een gewogen woordenset uit slug, title, H1 en H2's."""
    prof = {}
    for pad, b in alle.items():
        delen = pad.strip("/").split("/")
        if len(delen) != 2 or delen[0] not in DOEL_RUBRIEKEN:
            continue
        html = _lees(b)
        if _noindex(html):
            continue
        h1 = (_h1(html) or [_title(html)])[0]
        h2 = " ".join(_tekst(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", _hoofdtekst(html), re.S)[:12])
        gewicht = Counter()
        for w in _woorden(delen[1].replace("-", " ")):
            gewicht[w] += 3
        for w in _woorden(_title(html) + " " + h1):
            gewicht[w] += 2
        for w in _woorden(h2):
            gewicht[w] += 0.3
        for w, g in list(gewicht.items()):
            for kw, t in _THEMA_WOORD:
                if kw in w or (w.endswith("en") and w[:-2] == kw):
                    gewicht["#" + t] += g * 0.5
        label = re.split(r"[:?]| \| ", h1)[0].strip() or h1
        prof[pad] = {"rubriek": delen[0], "label": label, "w": gewicht, "links": _links(html, True)}
    # Samenstellingen: 'inloopdouche' telt ook als 'douche', 'badkamertegels' als 'tegels'.
    vocab = {w for p in prof.values() for w in p["w"]}
    for p in prof.values():
        extra = Counter()
        for w, g in p["w"].items():
            for v in vocab:
                if v != w and len(v) >= 4 and len(w) > len(v) and (w.endswith(v) or w.startswith(v)):
                    extra[v] += g * 0.6
        p["w"].update(extra)
    # Zeldzame woorden wegen zwaarder (idf); 'badkamer' staat bijna overal en telt weinig.
    df = Counter(w for p in prof.values() for w in p["w"])
    n = len(prof)
    import math
    for p in prof.values():
        p["v"] = {w: g * math.log((n + 1) / (df[w] + 0.5)) for w, g in p["w"].items()}
        p["norm"] = math.sqrt(sum(x * x for x in p["v"].values())) or 1
    return prof


def _gelijkenis(a, b):
    gedeeld = set(a["v"]) & set(b["v"])
    return sum(a["v"][w] * b["v"][w] for w in gedeeld) / (a["norm"] * b["norm"])


def gerelateerd(alle, aantal=6, inlinks=None):
    """{pad: [doelpaden]} voor alle contentpagina's. Voorkeur voor pagina's die nog niet in de
    tekst gelinkt staan en die weinig links krijgen; hooguit drie uit dezelfde rubriek."""
    prof = _profielen(alle)
    inlinks = inlinks or Counter()
    uit = {}
    for pad, p in prof.items():
        if p["rubriek"] not in HOST_RUBRIEKEN:
            continue
        scores = []
        for q, pq in prof.items():
            if q == pad:
                continue
            sim = _gelijkenis(p, pq)
            if sim <= 0:
                continue
            if q in p["links"]:
                sim *= 0.55          # staat al in de tekst: minder nodig
            sim *= 1 + 0.25 / (1 + inlinks.get(q, 0) / 4)   # zwak gelinkte pagina's krijgen een duwtje
            scores.append((sim, q))
        scores.sort(reverse=True)
        gekozen, per_rubriek = [], Counter()
        for sim, q in scores:
            r = prof[q]["rubriek"]
            if per_rubriek[r] >= 3:
                continue
            gekozen.append(q)
            per_rubriek[r] += 1
            if len(gekozen) == aantal:
                break
        # Te weinig gevonden: aanvullen met pagina's uit dezelfde rubriek.
        for q in sorted(prof):
            if len(gekozen) >= 4:
                break
            if q != pad and q not in gekozen and prof[q]["rubriek"] == p["rubriek"]:
                gekozen.append(q)
        if len(gekozen) >= 3:
            uit[pad] = gekozen
    return uit, prof


def _gerel_html(doelen, prof):
    kaarten = "".join(
        f'<a href="{q}"><small>{RUBRIEK[prof[q]["rubriek"]]}</small><strong>{prof[q]["label"]}</strong></a>'
        for q in doelen)
    return (f'<section class="section-sm gerel" aria-labelledby="gerel-kop"><div class="wrap">'
            f'<h2 id="gerel-kop">Gerelateerde pagina\'s</h2><div class="gerel-grid">{kaarten}</div>'
            f'</div></section>\n')


def blok_gerelateerd(alle):
    """Zet het blok op elke contentpagina, vóór de afsluitende CTA (of anders vóór de footer)."""
    inl = Counter()
    for pad, b in alle.items():
        for q in _links(_lees(b), True):
            if q != pad:
                inl[q] += 1
    keuze, prof = gerelateerd(alle, inlinks=inl)
    nieuw = 0
    for pad, doelen in keuze.items():
        b = alle[pad]
        html = _lees(b)
        if 'class="section-sm gerel"' in html:
            continue
        blok = _gerel_html(doelen, prof)
        voet = html.rfind("<footer")
        cta = html.rfind('<div class="cta">', 0, voet)
        sectie = html.rfind("<section", 0, cta) if cta > 0 else -1
        plek = sectie if sectie > 0 and html.rfind("</section>", sectie, cta) < 0 else voet
        if plek < 0:
            continue
        html = html[:plek] + blok + html[plek:]
        _schrijf(b, html)
        nieuw += sum(1 for q in doelen if q not in prof[pad]["links"])
    css = os.path.join(OUT, "assets", "css", "style.css")
    if keuze and os.path.exists(css) and ".gerel-grid" not in _lees(css):
        _schrijf(css, _lees(css) + RELATED_CSS)
    return len(keuze), nieuw


# ---------------------------------------------------------------------------
# Image-sitemap voor de eigen 3D-renders (fotos/renders/)
# ---------------------------------------------------------------------------

RENDER_IMG = re.compile(r'<img\b[^>]*\bsrc="/assets/fotos/renders/([a-z0-9-]+?)-(?:400|800|1600)\.webp"[^>]*>')


def image_sitemap(alle):
    """Schrijft site/sitemap-afbeeldingen.xml: per indexeerbare pagina de renders die erop staan,
    in de grootste versie. Zet de sitemap ook in robots.txt. Geeft (pagina's, beelden) terug."""
    renders = os.path.join(ROOT, "fotos", "renders")
    per_pagina = {}
    alle_beelden = set()
    for pad, b in sorted(alle.items()):
        html = _lees(b)
        if _noindex(html) or pad.endswith(".html"):
            continue
        namen = []
        for naam in RENDER_IMG.findall(html):
            if naam not in namen:
                namen.append(naam)
        if namen:
            per_pagina[pad] = namen
            alle_beelden.update(namen)

    def grootste(naam):
        for w in (1600, 800, 400):
            if os.path.exists(os.path.join(renders, f"{naam}-{w}.webp")):
                return f"{SITE['url']}/assets/fotos/renders/{naam}-{w}.webp"
        return None

    urls = []
    for pad, namen in per_pagina.items():
        beelden = "".join(f"<image:image><image:loc>{u}</image:loc></image:image>"
                          for u in (grootste(n) for n in namen) if u)
        if beelden:
            urls.append(f"<url><loc>{SITE['url']}{pad}</loc>{beelden}</url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">' + "".join(urls) + "</urlset>")
    _schrijf(os.path.join(OUT, "sitemap-afbeeldingen.xml"), xml)

    robots = os.path.join(OUT, "robots.txt")
    if os.path.exists(robots):
        r = _lees(robots)
        regel = f"Sitemap: {SITE['url']}/sitemap-afbeeldingen.xml"
        if regel not in r:
            _schrijf(robots, r.rstrip("\n") + "\n" + regel + "\n")
    ongebruikt = sorted({f.rsplit("-", 1)[0] for f in os.listdir(renders) if f.endswith(".webp")} - alle_beelden) \
        if os.path.isdir(renders) else []
    return len(urls), len(alle_beelden), ongebruikt


# ---------------------------------------------------------------------------
# Snelheid
# ---------------------------------------------------------------------------

def _attr(tag, naam):
    m = re.search(rf'\b{naam}="([^"]*)"', tag)
    return m.group(1) if m else None


def snelheid_html(html):
    """- elk <img> krijgt decoding="async";
    - <img> zonder loading= krijgt loading="lazy", behalve in de header en bij fetchpriority="high";
    - het eerste beeld met fetchpriority="high" (de hero, het LCP-beeld) krijgt een preload in de head;
    - config.js krijgt defer (wordt alleen door de andere, ook uitgestelde scripts gelezen)."""
    kop_eind = html.find("</header>")

    def img(m):
        tag = m.group(0)
        if "decoding=" not in tag:
            tag = tag[:-1].rstrip("/ ") + ' decoding="async">'
        if "loading=" not in tag and 'fetchpriority="high"' not in tag and m.start() > kop_eind:
            tag = tag[:-1] + ' loading="lazy">'
        return tag
    html = re.sub(r"<img\b[^>]*>", img, html)

    if 'rel="preload" as="image"' not in html:
        m = re.search(r'<img\b[^>]*fetchpriority="high"[^>]*>', html)
        if m:
            tag = m.group(0)
            src, srcset, sizes = _attr(tag, "src"), _attr(tag, "srcset"), _attr(tag, "sizes")
            if src:
                pre = f'<link rel="preload" as="image" href="{src}" fetchpriority="high"'
                if srcset:
                    pre += f' imagesrcset="{srcset}" imagesizes="{sizes or "100vw"}"'
                html = html.replace('<link rel="stylesheet"', pre + '>\n<link rel="stylesheet"', 1)

    html = html.replace('<script src="/assets/js/config.js"></script>',
                        '<script src="/assets/js/config.js" defer></script>')
    return html


def _css_regels(s):
    """Splitst CSS in (selector, inhoud); @media/@supports worden recursief verwerkt."""
    i, uit = 0, []
    while i < len(s):
        j = s.find("{", i)
        if j < 0:
            uit.append((None, s[i:]))
            break
        sel = s[i:j].strip()
        if sel.startswith("@") and not sel.startswith(("@font-face", "@page")):
            if sel.startswith(("@media", "@supports", "@layer", "@container")):
                d, k = 1, j + 1
                while d and k < len(s):
                    d += {"{": 1, "}": -1}.get(s[k], 0)
                    k += 1
                uit.append((sel, _css_regels(s[j + 1:k - 1])))
                i = k
                continue
            # @keyframes en dergelijke: in één stuk overnemen
            d, k = 1, j + 1
            while d and k < len(s):
                d += {"{": 1, "}": -1}.get(s[k], 0)
                k += 1
            uit.append((None, s[i:k]))
            i = k
            continue
        k = s.find("}", j)
        uit.append((sel, s[j + 1:k]))
        i = k + 1
    return uit


def css_opschonen(alle):
    """Haalt regels uit style.css waarvan elke selector een class noemt die op geen enkele pagina
    en in geen enkel script voorkomt (resten uit Topschilder en oude ontwerpen).
    Voorzichtig: een class die ergens als woord voorkomt, of die begint met een voorvoegsel dat
    een script aan elkaar plakt ('bl-dq-' + x), blijft staan. Geeft (oud, nieuw) in bytes terug."""
    css_pad = os.path.join(OUT, "assets", "css", "style.css")
    if not os.path.exists(css_pad):
        return 0, 0
    css = _lees(css_pad)
    corpus = [_lees(b) for b in alle.values()]
    js_map = os.path.join(OUT, "assets", "js")
    corpus += [_lees(os.path.join(js_map, f)) for f in os.listdir(js_map) if f.endswith(".js")]
    corpus = "\n".join(corpus)
    woorden = set(re.findall(r"[A-Za-z0-9_-]+", corpus))
    voorvoegsels = set(re.findall(r"""["'`\s]([a-z][a-z0-9-]*-)["'`]\s*\+""", corpus))
    voorvoegsels |= set(re.findall(r"""([a-z][a-z0-9-]*-)\$\{""", corpus))

    def gebruikt(cls):
        return cls in woorden or any(cls.startswith(v) for v in voorvoegsels)

    def weg(sel):
        for deel in sel.split(","):
            classes = re.findall(r"\.([A-Za-z_][A-Za-z0-9_-]*)", re.sub(r"\[[^\]]*\]|\([^)]*\)", "", deel))
            if not classes or all(gebruikt(c) for c in classes):
                return False
        return True

    def bouw(regels):
        out = []
        for sel, inhoud in regels:
            if sel is None:
                out.append(inhoud)
            elif isinstance(inhoud, list):
                binnen = bouw(inhoud)
                if binnen.strip():
                    out.append(f"{sel}{{{binnen}}}")
            elif not weg(sel):
                out.append(f"{sel}{{{inhoud}}}")
        return "".join(out)

    nieuw = bouw(_css_regels(css))
    _schrijf(css_pad, nieuw)
    return len(css.encode()), len(nieuw.encode())


def js_klein(tekst):
    """Lichte, veilige verkleining: commentaarregels, inspringing en lege regels eruit.
    Regels blijven regels (geen gedoe met automatische puntkomma's). Bestanden met
    template-strings (backticks) blijven ongemoeid, want daarin telt witruimte mee."""
    if "`" in tekst:
        return tekst
    tekst = re.sub(r"(?m)^[ \t]*/\*.*?\*/[ \t]*\n", "", tekst, flags=re.S)
    regels = []
    for r in tekst.split("\n"):
        r = r.strip()
        if r and not r.startswith("//"):
            regels.append(r)
    return "\n".join(regels) + "\n"


def js_verkleinen():
    """Verkleint de eigen scripts in site/assets/js/ (niet vendor/). Geeft (oud, nieuw) terug."""
    js_map = os.path.join(OUT, "assets", "js")
    oud = nieuw = 0
    if not os.path.isdir(js_map):
        return 0, 0
    for f in sorted(os.listdir(js_map)):
        if f.endswith(".js"):
            pad = os.path.join(js_map, f)
            t = _lees(pad)
            k = js_klein(t)
            oud += len(t.encode())
            nieuw += len(k.encode())
            _schrijf(pad, k)
    return oud, nieuw



def snelheid(alle):
    n = 0
    for pad, b in alle.items():
        html = _lees(b)
        nieuw = snelheid_html(html)
        if nieuw != html:
            _schrijf(b, nieuw)
            n += 1
    return n


# ---------------------------------------------------------------------------
# Alles na elkaar (aangeroepen vanuit build.py)
# ---------------------------------------------------------------------------

def nabewerken():
    alle = paginas()
    t = schema(alle)
    print("  seo_extra: schema " + ", ".join(f"{k} {v}" for k, v in sorted(t.items())))
    n_gerel, n_nieuw = blok_gerelateerd(alle)
    print(f"  seo_extra: blok 'Gerelateerde pagina's' op {n_gerel} pagina's, {n_nieuw} nieuwe contextlinks")
    n_snel = snelheid(alle)
    oud, nieuw = css_opschonen(alle)
    print(f"  seo_extra: snelheid bijgewerkt op {n_snel} pagina's; style.css {oud:,} -> {nieuw:,} bytes")
    oud, nieuw = js_verkleinen()
    print(f"  seo_extra: eigen scripts {oud:,} -> {nieuw:,} bytes")
    n_pag, n_img, ongebruikt = image_sitemap(alle)
    print(f"  seo_extra: sitemap-afbeeldingen.xml met {n_img} renders op {n_pag} pagina's"
          + (f" ({len(ongebruikt)} renders staan nog op geen enkele pagina)" if ongebruikt else ""))


if __name__ == "__main__":
    opdracht = sys.argv[1] if len(sys.argv) > 1 else "meet"
    if opdracht == "meet":
        meet()
    elif opdracht == "audit":
        audit()
    else:
        print(__doc__)
