# -*- coding: utf-8 -*-
"""Indelingsplanner badkamer (/tools/indelingsplanner/).

Losse module met de interface LINKS + build(write). De bezoeker tekent zijn badkamer op schaal
na, sleept elementen op een raster van 5 cm en ziet live of er genoeg vrije ruimte is.
Alles gebeurt in de browser: er wordt niets verstuurd of op een server opgeslagen.
De JavaScript staat in badkamer_indeling_js.py (LOGIC_JS is los te testen met node).

"Neem deze indeling mee in je aanvraag" zet een korte tekst in sessionStorage onder de sleutel
"tb_indeling" en linkt naar /offerte-aanvragen/?via=indeling. De prefill van het formulier
hoort in assets.py (hoofdsessie).

Richtmaten en bronnen (geraadpleegd november 2026):
- Bbl artikel 4.170 lid 2 (nieuwbouw): een badruimte met toilet heeft minstens 2,2 m² vloer
  en is minstens 0,9 m breed. https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/bad-toiletruimte/
- RVO, Bijlage 2 "Eisen rollatorgeschikte wooneenheid" (2025): aansluitend op de closetpot een
  obstakelvrije ruimte van 1,1 x 1,1 m; in de doucheruimte ook 1,1 x 1,1 m (mag 0,3 m onder
  de wastafel doorlopen). Dat gebruiken we voor de stand "ruim".
  https://www.rvo.nl/sites/default/files/2025-04/Bijlage-2-Eisen-rollatorgeschikte-wooneenheid.pdf
- Voor bestaande woningen is er geen wettelijke maat voor de vrije ruimte bij toilet en
  wastafel. 60 cm vrij voor het toilet, 70 cm voor de wastafel en 20 cm naast het toilet zijn
  gangbare vuistregels uit de badkamerpraktijk (adviezen van installateurs en badkamerontwerpers
  noemen 60 tot 70 cm). Op de pagina staat dat zo eerlijk vermeld.
- NEN 1814 (toegankelijkheid van gebouwen) gaat over toegankelijke sanitaire ruimten; die
  noemen we alleen als verwijzing, niet als bron van de maten.
- Prijzen: richtprijzen.py (RP), incl. 21% btw, met de bronnen daaruit.
"""

import json

import richtprijzen as RP
from components import (page, crumbs, faq_blok, cta_blok, cta_midden, offertecheck_blok,
                        title, desc, render_beeld, icon)
from badkamer_indeling_js import LOGIC_JS, UI_JS

PAD = "/tools/indelingsplanner/"

LINKS = [
    (PAD, "Indelingsplanner",
     "Teken je badkamer op schaal en probeer indelingen uit, met een live check op vrije ruimte."),
]

# Elementen: w = breedte langs de muur, d = diepte van de muur af (cm).
# Maten zijn gangbare handelsmaten, afgerond op 5 cm (hangtoilet ca. 36 x 54 cm -> 40 x 55).
TYPES = {
    "inloop90":  {"naam": "Inloopdouche 90×90", "kort": "douche", "w": 90, "d": 90, "cat": "douche", "vorm": "inloop"},
    "inloop120": {"naam": "Inloopdouche 120×90", "kort": "douche", "w": 120, "d": 90, "cat": "douche", "vorm": "inloop"},
    "inloop200": {"naam": "Inloopdouche 200×100", "kort": "inloopdouche", "w": 200, "d": 100, "cat": "douche", "vorm": "inloop"},
    "douchebak": {"naam": "Douchebak 90×90", "kort": "douche", "w": 90, "d": 90, "cat": "douche", "vorm": "douchebak"},
    "bad170":    {"naam": "Bad 170×75", "kort": "bad", "w": 170, "d": 75, "cat": "bad", "vorm": "bad"},
    "bad180":    {"naam": "Bad 180×80", "kort": "bad", "w": 180, "d": 80, "cat": "bad", "vorm": "bad"},
    "vrijstaand": {"naam": "Vrijstaand bad 170×80", "kort": "vrijstaand bad", "w": 170, "d": 80, "cat": "bad", "vorm": "vrijstaand"},
    "toilet":    {"naam": "Hangtoilet", "kort": "wc", "w": 40, "d": 55, "cat": "toilet", "vorm": "toilet"},
    "was60":     {"naam": "Wastafelmeubel 60", "kort": "wastafel", "w": 60, "d": 45, "cat": "wastafel", "vorm": "wastafel"},
    "was80":     {"naam": "Wastafelmeubel 80", "kort": "wastafel", "w": 80, "d": 45, "cat": "wastafel", "vorm": "wastafel"},
    "was120":    {"naam": "Wastafelmeubel 120", "kort": "wastafel", "w": 120, "d": 45, "cat": "wastafel", "vorm": "wastafel"},
    "dubbel":    {"naam": "Dubbele wastafel 140", "kort": "dubbele wastafel", "w": 140, "d": 45, "cat": "wastafel", "vorm": "wastafel", "bakken": 2},
    "radiator":  {"naam": "Radiator 60", "kort": "radiator", "w": 60, "d": 10, "cat": "radiator", "vorm": "radiator"},
    "wasmachine": {"naam": "Wasmachine", "kort": "was", "w": 60, "d": 60, "cat": "wasmachine", "vorm": "wasmachine"},
}

# Volgorde en groepen van de knoppen
KNOPPEN = [
    ("Douche", ["inloop90", "inloop120", "inloop200", "douchebak"]),
    ("Bad", ["bad170", "bad180", "vrijstaand"]),
    ("Toilet en wastafel", ["toilet", "was60", "was80", "was120", "dubbel"]),
    ("Overig", ["radiator", "wasmachine"]),
]


def _deur(wand, pos, b=80, draai="in-a"):
    return {"wand": wand, "pos": pos, "b": b, "draai": draai}


def _raam(aan=False, wand="boven", pos=40, b=60):
    return {"aan": aan, "wand": wand, "pos": pos, "b": b}


# Voorbeeldindelingen. Getest met node (zie tests in de uitvoermap): geen knelpunten.
PRESETS = {
    "klein": {
        "naam": "Klein", "maat": "170 × 220 cm", "uitleg": "Inloopdouche in de hoek, hangtoilet en een smal wastafelmeubel tegenover elkaar.",
        "kamer": {"b": 170, "d": 220, "deur": _deur("onder", 45), "raam": _raam(False, "rechts", 20, 60)},
        "elementen": [
            {"type": "inloop90", "x": 0, "y": 0, "rot": 0},
            {"type": "radiator", "x": 100, "y": 0, "rot": 0},
            {"type": "toilet", "x": 115, "y": 110, "rot": 90},
            {"type": "was60", "x": 0, "y": 110, "rot": 270},
        ],
    },
    "middel": {
        "naam": "Middel", "maat": "220 × 260 cm", "uitleg": "Bad langs de korte wand, wastafel en toilet in het looppad, deur naar binnen.",
        "kamer": {"b": 220, "d": 260, "deur": _deur("onder", 100), "raam": _raam(True, "boven", 40, 80)},
        "elementen": [
            {"type": "bad170", "x": 0, "y": 0, "rot": 0},
            {"type": "radiator", "x": 210, "y": 70, "rot": 90},
            {"type": "was80", "x": 0, "y": 110, "rot": 270},
            {"type": "toilet", "x": 165, "y": 150, "rot": 90},
        ],
    },
    "groot": {
        "naam": "Groot", "maat": "300 × 360 cm", "uitleg": "Royale inloopdouche, vrijstaand bad, dubbele wastafel en een apart hoekje voor het toilet.",
        "kamer": {"b": 300, "d": 360, "deur": _deur("onder", 30), "raam": _raam(True, "rechts", 210, 100)},
        "elementen": [
            {"type": "inloop200", "x": 0, "y": 0, "rot": 270},
            {"type": "dubbel", "x": 120, "y": 0, "rot": 0},
            {"type": "toilet", "x": 245, "y": 120, "rot": 90},
            {"type": "vrijstaand", "x": 120, "y": 200, "rot": 0},
            {"type": "radiator", "x": 0, "y": 220, "rot": 270},
        ],
    },
}


def _som(*sleutels):
    return [sum(RP.RICHTPRIJZEN[s]["laag"] for s in sleutels), sum(RP.RICHTPRIJZEN[s]["hoog"] for s in sleutels)]


def _kosten():
    """Richtprijzen voor de JS (incl. 21% btw), allemaal uit richtprijzen.py."""
    tegel = _som("tegelwerk", "tegelwerk_hulpmateriaal", "tegels")
    el = {
        "douche": ("Douche", _som("sanitair_douche", "montage_douche")),
        "bad": ("Bad", _som("sanitair_bad", "montage_bad")),
        "toilet": ("Toilet", _som("sanitair_toilet", "montage_toilet")),
        "wastafel": ("Wastafelmeubel", _som("sanitair_meubel", "montage_meubel")),
    }
    vast = [
        ("Slopen en afvoeren van de oude badkamer", "sloop_compleet", False),
        ("Leidingwerk water en afvoer", "leidingwerk", False),
        ("Waterdicht maken van de natte zone", "waterdicht", True),
        ("Elektra en ventilator", None, False),
    ]
    v = []
    for naam, s, nat in vast:
        lh = _som("elektra", "ventilator") if s is None else _som(s)
        v.append({"naam": naam, "l": lh[0], "h": lh[1], "alleenNat": nat})
    return {"tegel_m2": tegel,
            "element": {k: {"naam": n, "l": lh[0], "h": lh[1]} for k, (n, lh) in el.items()},
            "vast": v}


KOSTEN_SLEUTELS = ["tegelwerk", "tegelwerk_hulpmateriaal", "tegels", "sanitair_douche", "montage_douche",
                   "sanitair_bad", "montage_bad", "sanitair_toilet", "montage_toilet", "sanitair_meubel",
                   "montage_meubel", "sloop_compleet", "leidingwerk", "waterdicht", "elektra", "ventilator"]


def _prijsbronnen():
    gezien, uit = set(), []
    for s in KOSTEN_SLEUTELS:
        for naam, url in RP.bron_links(s):
            if url not in gezien:
                gezien.add(url)
                uit.append(f'<a href="{url}" rel="noopener" target="_blank">{naam}</a>')
    return ", ".join(uit)


CSS = """<style>
.ip-tool{max-width:100%;min-width:0;background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:16px}
@media(min-width:900px){.ip-tool{padding:28px}}
.ip-presets{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}
.ip-presets button{flex:1 1 140px;text-align:left;border:1px solid var(--line);background:#fff;border-radius:var(--radius);padding:10px 12px;cursor:pointer;font:inherit;color:var(--ink)}
.ip-presets button small{display:block;color:var(--muted);font-size:.8rem}
.ip-presets button[aria-pressed=true]{border-color:var(--navy);background:var(--bg-soft);box-shadow:inset 0 0 0 1px var(--navy)}
.ip-grid{display:grid;gap:18px}
.ip-grid>div{min-width:0}
.ip-tool [hidden]{display:none!important}
@media(min-width:980px){.ip-grid{grid-template-columns:minmax(0,1fr) 340px;align-items:start}}
.ip-plan{position:relative;background:var(--bg-soft);border-radius:var(--radius);padding:6px}
.ip-plan svg{display:block;width:100%;height:auto;max-height:72vh;touch-action:pan-y pinch-zoom;user-select:none;-webkit-user-select:none}
.ip-plan svg:focus{outline:none}
.ip-el{cursor:grab;touch-action:none;outline:none}
.ip-el:focus-visible{outline:none}
.ip-el:focus-visible>g{filter:drop-shadow(0 0 3px #e8792b)}
.ip-sel{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:10px 0 0;font-size:.9rem;color:var(--ink)}
.ip-sel span{flex:1 1 100%}
.ip-btn{border:1px solid var(--line);background:#fff;border-radius:999px;padding:8px 14px;font:inherit;font-size:.9rem;cursor:pointer;color:var(--ink);min-height:40px}
.ip-btn:hover{border-color:var(--navy)}
.ip-hulp{font-size:.82rem;color:var(--muted);margin:8px 0 0}
.ip-palet h3{font-size:.95rem;margin:14px 0 6px}
.ip-palet div{display:flex;flex-wrap:wrap;gap:6px}
.ip-palet button{border:1px dashed #9fb0c0;background:#fff;border-radius:8px;padding:7px 10px;font:inherit;font-size:.86rem;cursor:pointer;color:var(--ink);min-height:38px}
.ip-palet button:hover{border-style:solid;border-color:var(--navy)}
.ip-form{display:grid;gap:12px}
.ip-form fieldset{border:1px solid var(--line);border-radius:var(--radius);padding:10px 12px;margin:0;min-width:0}
.ip-form legend{font-weight:700;color:var(--ink);font-size:.95rem;padding:0 4px}
.ip-rij{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px}
.ip-form label{display:block;font-size:.84rem;color:var(--muted)}
.ip-form input[type=number],.ip-form select{width:100%;padding:8px;border:1px solid var(--line);border-radius:8px;font:inherit;color:var(--ink);background:#fff;margin-top:2px}
.ip-form .ip-check{display:flex;gap:8px;align-items:center;color:var(--ink);font-size:.9rem;margin:2px 0 6px}
.ip-status{font-weight:700;border-radius:var(--radius);padding:10px 12px;margin:0 0 8px}
.ip-st-ok{background:#e6f4ea;color:#1d5c32}
.ip-st-advies{background:#fff4dc;color:#7a5200}
.ip-st-fout{background:#fde8e8;color:#9b1c1c}
.ip-meld{list-style:none;margin:0 0 14px;padding:0;font-size:.88rem}
.ip-meld li{padding:4px 0 4px 18px;position:relative}
.ip-meld li:before{content:"";position:absolute;left:2px;top:.75em;width:8px;height:8px;border-radius:50%;background:#9fb0c0}
.ip-meld .ip-m-fout:before{background:#c82828}
.ip-meld .ip-m-advies:before{background:#d48a00}
.ip-res{margin-top:22px;border-top:1px solid var(--line);padding-top:18px}
.ip-sam{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:0 0 12px}
.ip-sam div{background:var(--bg-soft);border-radius:var(--radius);padding:12px}
.ip-sam small{display:block;color:var(--muted);font-size:.8rem}
.ip-sam b{font-size:1.12rem;color:var(--ink)}
.ip-posten{list-style:none;margin:8px 0;padding:0;font-size:.88rem}
.ip-posten li{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px solid var(--line)}
.ip-posten b{white-space:nowrap;font-weight:600;color:var(--ink)}
.ip-klein{font-size:.82rem;color:var(--muted)}
.ip-acties{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
.ip-leg{display:flex;flex-wrap:wrap;gap:12px;font-size:.8rem;color:var(--muted);margin:8px 0 0}
.ip-leg i{display:inline-block;width:14px;height:10px;border:1px dashed;vertical-align:-1px;margin-right:4px}
.ip-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.ip-tabel{width:100%;border-collapse:collapse;font-size:.92rem}
.ip-tabel th,.ip-tabel td{padding:8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.ip-maten{display:grid;gap:14px}
@media(min-width:800px){.ip-maten{grid-template-columns:repeat(3,1fr)}}
.ip-maat{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);padding:18px}
.ip-maat h3{margin-top:0}
.ip-maat .ip-tag{display:inline-block;background:var(--accent-soft);border-radius:999px;padding:2px 10px;font-size:.8rem;font-weight:600;margin-bottom:6px}
.ip-maat ul{padding-left:18px;margin:0}
.ip-maat li{margin:4px 0}
.ip-beeld{display:grid;gap:22px;align-items:center}
@media(min-width:900px){.ip-beeld{grid-template-columns:1.1fr 1fr}}
@media(prefers-reduced-motion:reduce){.ip-tool *{transition:none!important;animation:none!important}}
</style>"""


def _opties(paren, gekozen=None):
    return "".join(f'<option value="{v}"{" selected" if v == gekozen else ""}>{n}</option>' for v, n in paren)


WANDEN = [("boven", "Bovenwand"), ("rechts", "Rechterwand"), ("onder", "Onderwand"), ("links", "Linkerwand")]


def _tool_html():
    presets = "".join(
        f'<button type="button" data-ip-preset="{k}" aria-pressed="false"><strong>{p["naam"]}</strong> · {p["maat"]}<small>{p["uitleg"]}</small></button>'
        for k, p in PRESETS.items())
    palet = "".join(
        f'<h3>{groep}</h3><div>' + "".join(
            f'<button type="button" data-ip-add="{t}">+ {TYPES[t]["naam"]}</button>' for t in ids) + "</div>"
        for groep, ids in KNOPPEN)
    return f"""<div class="ip-tool" data-ip>
  <p class="ip-klein" style="margin:0 0 6px"><strong>Begin met een voorbeeld</strong> of vul hieronder je eigen maten in.</p>
  <div class="ip-presets" role="group" aria-label="Voorbeeldindelingen">{presets}</div>
  <div class="ip-grid">
    <div>
      <div class="ip-plan">
        <svg data-ip-svg xmlns="http://www.w3.org/2000/svg" viewBox="-34 -34 238 288" role="application" tabindex="-1" aria-roledescription="plattegrond"></svg>
      </div>
      <p class="ip-leg"><span><i style="border-color:#3f7f89;background:rgba(63,127,137,.1)"></i>vrije ruimte (gekozen element)</span><span><i style="border-color:#c82828;background:rgba(200,40,40,.16)"></i>te weinig ruimte</span><span><i style="border-color:#3a4a5c"></i>draaicirkel deur</span></p>
      <div class="ip-sel" data-ip-sel hidden>
        <span data-ip-selnaam></span>
        <button type="button" class="ip-btn" data-ip-draai>Draai een kwartslag</button>
        <button type="button" class="ip-btn" data-ip-weg>Verwijder</button>
      </div>
      <p class="ip-hulp">Sleep een element met je muis of vinger. Het raster is 10 cm, met een dikkere lijn om de 50 cm; elementen springen per 5 cm. Met het toetsenbord: Tab naar een element, pijltjes verplaatsen 5 cm (met Shift 25 cm), R draait en Delete verwijdert.</p>
      <div class="ip-palet" aria-label="Elementen toevoegen">{palet}
        <div style="margin-top:10px"><button type="button" data-ip-leeg>Alles weghalen</button></div>
      </div>
    </div>
    <div>
      <form class="ip-form" data-ip-form>
        <fieldset><legend>Ruimte (binnenmaat)</legend>
          <div class="ip-rij">
            <label for="ip-b">Breedte (cm)<input type="number" id="ip-b" min="100" max="600" step="5" inputmode="numeric"></label>
            <label for="ip-d">Diepte (cm)<input type="number" id="ip-d" min="100" max="600" step="5" inputmode="numeric"></label>
          </div>
        </fieldset>
        <fieldset><legend>Deur</legend>
          <div class="ip-rij">
            <label for="ip-dw">In de<select id="ip-dw">{_opties(WANDEN)}</select></label>
            <label for="ip-dp">Afstand tot de hoek (cm)<input type="number" id="ip-dp" min="0" max="600" step="5" inputmode="numeric"></label>
            <label for="ip-db">Breedte<select id="ip-db">{_opties([("70", "70 cm"), ("80", "80 cm"), ("90", "90 cm")])}</select></label>
            <label for="ip-dd">Draairichting<select id="ip-dd">{_opties([("in-a", "Naar binnen, scharnier links/boven"), ("in-b", "Naar binnen, scharnier rechts/onder"), ("uit", "Naar buiten")])}</select></label>
          </div>
        </fieldset>
        <fieldset><legend>Raam (optioneel)</legend>
          <label class="ip-check"><input type="checkbox" id="ip-ra"> Er zit een raam in de badkamer</label>
          <div class="ip-rij" data-ip-raam>
            <label for="ip-rw">In de<select id="ip-rw">{_opties(WANDEN)}</select></label>
            <label for="ip-rp">Afstand tot de hoek (cm)<input type="number" id="ip-rp" min="0" max="600" step="5" inputmode="numeric"></label>
            <label for="ip-rb">Breedte (cm)<input type="number" id="ip-rb" min="30" max="400" step="5" inputmode="numeric"></label>
          </div>
        </fieldset>
        <fieldset><legend>Instellingen</legend>
          <div class="ip-rij">
            <label for="ip-modus">Richtmaten<select id="ip-modus">{_opties([("gangbaar", "Gangbaar (60–70 cm)"), ("ruim", "Ruim, rollator (110 cm)")])}</select></label>
            <label for="ip-h">Wandtegels tot<select id="ip-h">{_opties([("210", "2,10 m"), ("240", "2,40 m (plafond)"), ("260", "2,60 m (plafond)")])}</select></label>
          </div>
        </fieldset>
        <button type="submit" class="ip-sr">Bijwerken</button>
      </form>
      <div aria-live="polite" style="margin-top:14px">
        <p class="ip-status" data-ip-status>–</p>
        <ul class="ip-meld" data-ip-meld></ul>
        <p class="ip-sr" data-ip-live></p>
      </div>
    </div>
  </div>
  <div class="ip-res">
    <h2 style="font-size:1.25rem;margin:0 0 10px">Jouw indeling in cijfers</h2>
    <div class="ip-sam">
      <div><small>Afmetingen</small><b data-ip-maat>–</b></div>
      <div><small>Vloeroppervlak</small><b data-ip-vloer>–</b></div>
      <div><small>Tegeloppervlak (indicatie)</small><b data-ip-tegel>–</b></div>
      <div><small>Grove kostenindicatie</small><b data-ip-kosten>–</b></div>
    </div>
    <p class="ip-klein" data-ip-tegeluitleg></p>
    <details><summary style="cursor:pointer;font-weight:600">Zo is de kostenindicatie opgebouwd</summary>
      <ul class="ip-posten" data-ip-posten></ul>
      <p class="ip-klein" data-ip-nietmee hidden>Radiator en wasmachine zijn niet meegerekend.</p>
      <p class="ip-klein">Richtprijzen inclusief 21% btw, van basis tot luxe. Het is een grove indicatie voor een complete renovatie, geen offerte. Vloerverwarming, verlichting en bijzondere tegels zitten er niet in. Bronnen: {_prijsbronnen()}.</p>
    </details>
    <div class="ip-acties">
      <a class="btn btn-primary" href="/offerte-aanvragen/?via=indeling" data-ip-mee>Neem deze indeling mee in je aanvraag</a>
      <button type="button" class="btn btn-ghost" data-ip-png>Opslaan als afbeelding</button>
    </div>
    <p class="ip-klein" style="margin-top:10px">Je tekening blijft in je browser. Er wordt niets verstuurd of opgeslagen. Kies je voor meenemen, dan zetten we alleen een korte beschrijving klaar in het aanvraagformulier, die je zelf nog kunt aanpassen.</p>
  </div>
</div>"""


def _js():
    ui = (UI_JS.replace("__TYPES__", json.dumps(TYPES, ensure_ascii=False))
               .replace("__PRESETS__", json.dumps(PRESETS, ensure_ascii=False))
               .replace("__KOSTEN__", json.dumps(_kosten(), ensure_ascii=False)))
    return "<script>\n" + LOGIC_JS + "\n" + ui + "</script>"


def _uitleg_html():
    from render_stijl_data import RENDERS_STIJL
    beeld = render_beeld(RENDERS_STIJL["kleine-badkamer"], "(min-width: 900px) 520px, 100vw")
    bbl = "https://iplo.nl/regelgeving/regels-voor-activiteiten/technische-bouwactiviteit/nieuwbouw/rijksregels/bad-toiletruimte/"
    rvo = "https://www.rvo.nl/sites/default/files/2025-04/Bijlage-2-Eisen-rollatorgeschikte-wooneenheid.pdf"
    return f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Zo werkt de indelingsplanner</h2>
  <ol>
    <li><strong>Meet de binnenmaat</strong> van je badkamer: van muur tot muur, op vloerhoogte. Meet ook waar de deur zit en hoe breed hij is.</li>
    <li><strong>Vul de maten in</strong> of begin met een voorbeeld dat er het meest op lijkt. Kies de wand van de deur en de draairichting.</li>
    <li><strong>Sleep de elementen</strong> naar hun plek en draai ze waar nodig. De tool kijkt meteen of alles past.</li>
    <li><strong>Lees de controle.</strong> Rood is een knelpunt: iets overlapt, de deur slaat ergens tegen of er is te weinig vrije ruimte. Oranje is een aandachtspunt.</li>
    <li><strong>Bewaar of neem mee.</strong> Sla de tekening op als afbeelding, of neem een korte beschrijving mee in je offerteaanvraag. Dan weet de specialist meteen waar het over gaat.</li>
  </ol>
  <h2>Welke maten de tool controleert</h2>
  <p>Voor een bestaande woning staat er in de wet geen maat voor de vrije ruimte bij een toilet of wastafel. Badkamerontwerpers en installateurs werken met vuistregels. Die gebruikt de tool in de stand <em>gangbaar</em>:</p>
  <div style="overflow-x:auto"><table class="ip-tabel">
    <thead><tr><th>Regel</th><th>Gangbaar</th><th>Ruim (rollator)</th></tr></thead>
    <tbody>
      <tr><td>Vrije ruimte vóór het toilet</td><td>60 cm diep, 70 cm breed</td><td>110 × 110 cm</td></tr>
      <tr><td>Ruimte naast het toilet (tot muur of element)</td><td>20 cm aan beide kanten</td><td>20 cm aan beide kanten</td></tr>
      <tr><td>Vrije ruimte vóór de wastafel</td><td>70 cm diep</td><td>110 cm diep</td></tr>
      <tr><td>Deur</td><td colspan="2">mag niet tegen een element draaien; bij een deur naar buiten blijft 60 cm doorgang vrij</td></tr>
      <tr><td>Overlap</td><td colspan="2">niet toegestaan, ook niet een paar centimeter</td></tr>
      <tr><td>Wasmachine (aandachtspunt)</td><td colspan="2">60 cm vrij voor het deurtje</td></tr>
    </tbody></table></div>
  <p>De vrije ruimte van verschillende elementen mag samenvallen. Je staat immers niet tegelijk voor het toilet en voor de wastafel. Ook de draaicirkel van de deur mag over vrije ruimte gaan.</p>
  <p class="ip-klein">Bronnen: de 60 tot 70 cm en de 20 cm naast het toilet zijn gangbare vuistregels uit de badkamerpraktijk, geen wettelijke eis. De stand <em>ruim</em> volgt de eis van een obstakelvrije ruimte van 1,1 bij 1,1 meter bij de closetpot uit <a href="{rvo}" rel="noopener" target="_blank">RVO, Eisen rollatorgeschikte wooneenheid (2025)</a>. Voor nieuwbouw geldt volgens het Besluit bouwwerken leefomgeving (Bbl, artikel 4.170) dat een badruimte met toilet minstens 2,2 m² groot en 0,9 meter breed is, zie <a href="{bbl}" rel="noopener" target="_blank">IPLO, bad- en toiletruimte</a>. Voor volledig toegankelijke sanitaire ruimten is er de norm NEN 1814; die gaat verder dan deze tool.</p>
</div></section>
<section class="section"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:22px">
    <h2>Tips per badkamermaat</h2>
    <p>Hoe kleiner de ruimte, hoe meer elke tien centimeter telt. Deze keuzes maken het verschil.</p>
  </div>
  <div class="ip-maten">
    <div class="ip-maat"><span class="ip-tag">tot ca. 4 m²</span><h3>Kleine badkamer</h3><ul>
      <li>Kies een inloopdouche van 90 × 90 of 80 × 100 cm zonder deur. Een open kant scheelt draairuimte.</li>
      <li>Een hangtoilet laat de vloer vrij en is een paar centimeter minder diep dan een staand toilet.</li>
      <li>Een wastafelmeubel van 60 cm of een fonteintje houdt het looppad open.</li>
      <li>Laat de deur naar buiten draaien als hij binnen tegen het toilet slaat. Of kies een schuifdeur.</li>
      <li>Meer ideeën: <a href="/kennisbank/kleine-badkamer-indelen/">een kleine badkamer indelen</a>.</li></ul></div>
    <div class="ip-maat"><span class="ip-tag">ca. 4 tot 7 m²</span><h3>Middelgrote badkamer</h3><ul>
      <li>Twijfel je tussen bad en douche? Een bad van 170 × 75 cm met een glazen wand doet allebei.</li>
      <li>Zet de natte zone (douche of bad) aan de kant van de afvoer. Dat scheelt leidingwerk.</li>
      <li>Een wastafelmeubel van 80 cm geeft al genoeg aflegruimte voor twee.</li>
      <li>Houd het toilet uit het zicht van de deur, bijvoorbeeld achter een halfhoge wand.</li></ul></div>
    <div class="ip-maat"><span class="ip-tag">vanaf ca. 7 m²</span><h3>Grote badkamer</h3><ul>
      <li>Een vrijstaand bad heeft rondom zo'n 15 tot 20 cm nodig om schoon te kunnen maken.</li>
      <li>Een inloopdouche van 100 × 200 cm kan zonder glazen deur, met alleen een vaste wand.</li>
      <li>Een dubbele wastafel van 120 tot 140 cm voorkomt ochtendfiles.</li>
      <li>Denk aan een apart hoekje of nis voor het toilet, en aan een plek voor een wasmachine.</li></ul></div>
  </div>
</div></section>
<section class="section soft"><div class="wrap">
  <div class="ip-beeld">
    {beeld}
    <div class="prose">
      <h2>Van tekening naar badkamer</h2>
      <p>Een plattegrond is een goed begin, maar een specialist kijkt ook naar wat je niet ziet: waar de afvoer en de standleiding lopen, hoe dik de muren zijn en of er genoeg afschot naar de douche kan komen. Een toilet verplaatsen kost al snel honderden euro's extra aan leidingwerk. Kijk dus eerst of een indeling werkt met de aansluitingen op dezelfde plek.</p>
      <p>Op zoek naar sfeer en kleuren voor een kleine ruimte? Bekijk de <a href="/inspiratie/kleine-badkamer/">inspiratie voor een kleine badkamer</a>.</p>
      <p><a class="btn btn-ghost" href="/kennisbank/kleine-badkamer-indelen/">Lees: een kleine badkamer indelen</a></p>
    </div>
  </div>
</div></section>"""


FAQS = [
    ("Hoeveel ruimte heb je nodig voor een toilet?",
     "Reken op een nis van minstens 80 cm breed: het toilet zelf is ongeveer 36 tot 40 cm breed en daarnaast wil je aan beide kanten zo'n 20 cm. Vóór het toilet houd je 60 tot 70 cm vrij. Voor iemand met een rollator is 1,1 bij 1,1 meter vrije ruimte bij het toilet nodig."),
    ("Wat is de kleinste badkamer met douche, toilet en wastafel?",
     "Met een inloopdouche van 90 × 90 cm, een hangtoilet en een klein wastafelmeubel lukt het vaak vanaf ongeveer 170 × 200 cm. Voor nieuwbouw is 2,2 m² en 0,9 meter breed het wettelijke minimum voor een badruimte met toilet. Probeer het voorbeeld 'klein' in de planner en pas de maten aan jouw ruimte aan."),
    ("Mag een badkamerdeur naar binnen draaien?",
     "Ja, dat mag. In een kleine badkamer is een deur die naar buiten draait of een schuifdeur vaak handiger. Dan slaat de deur niet tegen het toilet en kun je iemand die onwel wordt altijd bereiken. De planner laat zien of je deur ergens tegenaan draait."),
    ("Hoe nauwkeurig is de tegelberekening?",
     "Het is een indicatie: vloer plus de wanden tot de hoogte die je kiest, min de deur. Ramen, nissen en een bad met ombouw tellen we niet apart. Bestel 10 tot 15 procent extra voor snijverlies en breuk, bij grote tegels of een visgraatpatroon meer."),
    ("Wordt mijn tekening ergens opgeslagen?",
     "Nee. Alles gebeurt in je eigen browser. Sla je de tekening op als afbeelding, dan komt het bestand alleen op je eigen apparaat. Neem je de indeling mee in je aanvraag, dan zetten we een korte beschrijving klaar in het formulier. Die wordt pas verstuurd als je het formulier zelf verzendt."),
    ("Kan ik het toilet of de douche zomaar verplaatsen?",
     "Dat kan vaak, maar het kost extra leidingwerk. Een toilet heeft een afvoer van 90 tot 110 mm nodig met genoeg afschot naar de standleiding. Vraag de specialist of de nieuwe plek haalbaar is voordat je de indeling vastlegt."),
]


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Indelingsplanner", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over je badkamer indelen")
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Indelingsplanner badkamer",
        "applicationCategory": "DesignApplication",
        "operatingSystem": "Alle browsers",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Teken je badkamer op schaal, sleep douche, bad, toilet en wastafel op hun plek en zie live of er genoeg vrije ruimte is.",
    }
    body = f"""{cr}
{CSS}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:22px">
    <span class="badge">Gratis tool</span>
    <h1>Indelingsplanner: teken je badkamer op schaal</h1>
    <p class="lead">Vul de maten van je badkamer in, zet de deur op zijn plek en sleep douche, bad, toilet en wastafel waar je ze wilt hebben. Je ziet meteen of alles past, hoeveel tegels je ongeveer nodig hebt en wat het grofweg kost.</p>
  </div>
  {_tool_html()}
</div></section>
<section class="section-sm"><div class="wrap narrow">
  {cta_midden("Past je indeling? Laat hem doorrekenen", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Neem je tekening mee, dan rekenen ze met jouw indeling.", "Offertes aanvragen met mijn indeling", "/offerte-aanvragen/?via=indeling")}
</div></section>
{_uitleg_html()}
<section class="section-sm"><div class="wrap narrow">{offertecheck_blok("je nieuwe badkamer")}</div></section>
{faq_html}
{cta_blok("Van plattegrond naar offerte", "Vergelijk gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten. Zij kijken ook naar de afvoer, de leidingen en het afschot.", "Gratis offertes aanvragen")}
{_js()}"""
    write(PAD, page(
        title("Indelingsplanner badkamer: teken je badkamer"),
        desc("Teken je badkamer gratis op schaal en probeer indelingen uit.",
             "Sleep douche, bad, toilet en wastafel en zie live of alles past, met tegels en kosten."),
        PAD, body, jsonld=[cr_ld, app_ld, faq_ld]), prio=0.7)
