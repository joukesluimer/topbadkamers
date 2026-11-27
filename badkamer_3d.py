# -*- coding: utf-8 -*-
"""3D-badkamer (/tools/badkamer-3d/).

Losse module met de interface LINKS + build(write). De bezoeker kijkt rond in een 3D-badkamer
(three.js) en kiest zelf wandtegels, vloertegels, kraankleur, badmeubel en douche of bad.
Er loopt een prijsindicatie mee op basis van richtprijzen.py.

- three.js 0.160.0 staat lokaal in vendor/three/ (MIT, zie vendor/three/LICENSE) en wordt pas
  geladen na een klik op "Start 3D". Daarvoor staat een poster (fotos/renders/badkamer-3d-*.webp),
  gemaakt met dezelfde scène.
- Zonder WebGL blijft de poster staan; kiezen en de prijs werken dan gewoon.
- "Vraag offertes aan met deze keuzes" zet een korte tekst in sessionStorage onder "tb_3d" en
  linkt naar /offerte-aanvragen/?via=3d. De prefill staat in assets.py.
- De JavaScript staat in badkamer_3d_js.py.
"""

import json
import os

import richtprijzen as RP
from components import page, crumbs, faq_blok, cta_blok, cta_midden, offertecheck_blok, title, desc
from badkamer_3d_js import JS

PAD = "/tools/badkamer-3d/"

LINKS = [
    (PAD, "3D-badkamer",
     "Kijk rond in een 3D-badkamer en kies zelf tegels, kraankleur, meubel en douche of bad, met een prijsindicatie."),
]

# Rekenvoorbeeld: de badkamer in de scène (binnenmaat in meters).
KAMER = {"b": 2.6, "d": 2.4, "h": 2.5}
VLOER_M2 = round(KAMER["b"] * KAMER["d"], 1)                                   # 6,2 m²
WAND_M2 = round(2 * (KAMER["b"] + KAMER["d"]) * KAMER["h"] - 0.8 * 2.1)        # 23 m², min de deur
SNIJVERLIES = 1.1

# Tegels. "tex" beschrijft hoe de JavaScript de tegel tekent (maten in meters).
# Het niveau (basis, midden, luxe) koppelt de tegel aan de m²-prijs in richtprijzen.py.
TEGELS_WAND = {
    "zellige": {"naam": "Groene zellige-look", "formaat": "10 × 10 cm", "niveau": "midden",
                "swatch": "#5d8b76",
                "tex": {"p": "zellige", "tw": 0.1, "th": 0.1, "kleur": "#5b8a75", "var": 0.17,
                        "voeg": "#e6e1d6", "vb": 4, "rough": 0.22}},
    "wit": {"naam": "Wit glans", "formaat": "30 × 60 cm", "niveau": "basis",
            "swatch": "#f3f2ee",
            "tex": {"p": "rechthoek", "tw": 0.6, "th": 0.3, "kleur": "#f3f2ee", "var": 0.015,
                    "voeg": "#d6d2ca", "vb": 3, "rough": 0.12}},
    "metro": {"naam": "Metrotegel wit, halfsteens", "formaat": "7,5 × 15 cm", "niveau": "basis",
              "swatch": "#f1f0eb",
              "tex": {"p": "metro", "tw": 0.15, "th": 0.075, "offset": 0.5, "kleur": "#f1f0eb", "var": 0.025,
                      "voeg": "#c9c4b9", "vb": 4, "rough": 0.1}},
    "marmer": {"naam": "Marmerlook wit", "formaat": "60 × 120 cm", "niveau": "luxe",
               "swatch": "#ebeae6",
               "tex": {"p": "marmer", "tw": 0.6, "th": 1.2, "kleur": "#ecebe7", "ader": "#8f8f8c",
                       "voeg": "#dad8d2", "vb": 3, "rough": 0.14}},
}
TEGELS_VLOER = {
    "beton": {"naam": "Betonlook grijs", "formaat": "60 × 60 cm", "niveau": "basis",
              "swatch": "#8c8a85",
              "tex": {"p": "beton", "tw": 0.6, "th": 0.6, "kleur": "#8e8c87", "var": 0.04,
                      "voeg": "#75726d", "vb": 3, "rough": 0.7}},
    "hout": {"naam": "Houtlook eiken", "formaat": "20 × 120 cm", "niveau": "midden",
             "swatch": "#b48a5c",
             "tex": {"p": "hout", "tw": 1.2, "th": 0.2, "offset": 0.5, "kleur": "#b58b5d", "var": 0.09,
                     "voeg": "#6f5640", "vb": 2, "rough": 0.6}},
    "cement": {"naam": "Cementlook zwart-wit", "formaat": "20 × 20 cm", "niveau": "midden",
               "swatch": "#2b2d2f",
               "tex": {"p": "cement", "tw": 0.2, "th": 0.2, "kleur": "#eeeae1", "kleur2": "#2b2d30",
                       "voeg": "#d4cfc4", "vb": 2, "rough": 0.5}},
    "terrazzo": {"naam": "Terrazzo licht", "formaat": "60 × 60 cm", "niveau": "luxe",
                 "swatch": "#e4ded4",
                 "tex": {"p": "terrazzo", "tw": 0.6, "th": 0.6, "kleur": "#e5dfd5",
                         "chips": ["#9c9389", "#c9b8a3", "#6f7b77", "#d8cfc2", "#a65f3f", "#4f5654"],
                         "voeg": "#d2cabd", "vb": 2, "rough": 0.35}},
}
KRANEN = {
    "chroom": {"naam": "Chroom", "kleur": "#dfe3e6", "metal": 1.0, "rough": 0.08,
               "swatch": "linear-gradient(135deg,#fbfcfc,#9ba4a9 55%,#eef0f1)"},
    "zwart": {"naam": "Mat zwart", "kleur": "#1d1d1f", "metal": 0.35, "rough": 0.55,
              "swatch": "#1d1d1f"},
    "goud": {"naam": "Geborsteld goud", "kleur": "#c99a4b", "metal": 1.0, "rough": 0.3,
             "swatch": "linear-gradient(135deg,#f0d49a,#b8873c 55%,#e6c27e)"},
}
MEUBELS = {
    "hout": {"naam": "Hout (eikenfineer)", "niveau": "midden", "swatch": "linear-gradient(90deg,#b7895a,#c99d6c 40%,#a87b4e)"},
    "wit": {"naam": "Wit mat gelakt", "niveau": "basis", "swatch": "#f6f5f2"},
}
INDELING = {
    "douche": {"naam": "Inloopdouche", "sanitair": "sanitair_douche", "montage": "montage_douche"},
    "bad": {"naam": "Ligbad", "sanitair": "sanitair_bad", "montage": "montage_bad"},
}
START = {"wand": "zellige", "vloer": "beton", "kraan": "zwart", "meubel": "hout", "indeling": "douche"}

NIVEAU_TEKST = {"basis": "basisniveau", "midden": "middenniveau", "luxe": "luxe niveau"}


def _r(lh):
    return [int(round(lh[0])), int(round(lh[1]))]


def _plus(*paren):
    return [sum(p[0] for p in paren), sum(p[1] for p in paren)]


def _niv(sleutel, niveau):
    return RP.RICHTPRIJZEN[sleutel]["niveaus"][niveau]


def _post(sleutel):
    return [RP.RICHTPRIJZEN[sleutel]["laag"], RP.RICHTPRIJZEN[sleutel]["hoog"]]


def prijzen():
    """Alle bedragen voor de JavaScript, incl. 21% btw, uit richtprijzen.py."""
    tegel = _niv
    wand = {k: _r([v * WAND_M2 * SNIJVERLIES for v in tegel("tegels", t["niveau"])]) for k, t in TEGELS_WAND.items()}
    vloer = {k: _r([v * VLOER_M2 * SNIJVERLIES for v in tegel("tegels", t["niveau"])]) for k, t in TEGELS_VLOER.items()}
    zetten = _r([v * (WAND_M2 + VLOER_M2) for v in _plus(_post("tegelwerk"), _post("tegelwerk_hulpmateriaal"))])
    indeling = {k: _r(_plus(_niv(i["sanitair"], "midden"), _post(i["montage"]))) for k, i in INDELING.items()}
    meubel = {k: _r(_plus(_niv("sanitair_meubel", m["niveau"]), _post("montage_meubel"))) for k, m in MEUBELS.items()}
    toilet = _r(_plus(_niv("sanitair_toilet", "midden"), _post("montage_toilet")))
    vast = [
        {"naam": "Slopen en afvoeren van de oude badkamer", "lh": _post("sloop_compleet")},
        {"naam": "Leidingwerk water en afvoer", "lh": _post("leidingwerk")},
        {"naam": "Waterdicht maken van de douche- of badhoek", "lh": _post("waterdicht")},
        {"naam": "Elektra en ventilator", "lh": _plus(_post("elektra"), _post("ventilator"))},
    ]
    return {"wand": wand, "vloer": vloer, "zetten": zetten, "indeling": indeling, "meubel": meubel,
            "toilet": toilet, "vast": vast}


KOSTEN_SLEUTELS = ["tegels", "tegelwerk", "tegelwerk_hulpmateriaal", "sanitair_douche", "montage_douche",
                   "sanitair_bad", "montage_bad", "sanitair_meubel", "montage_meubel", "sanitair_toilet",
                   "montage_toilet", "sloop_compleet", "leidingwerk", "waterdicht", "elektra", "ventilator"]


def _prijsbronnen():
    gezien, uit = set(), []
    for s in KOSTEN_SLEUTELS:
        for naam, url in RP.bron_links(s):
            if url not in gezien:
                gezien.add(url)
                uit.append(f'<a href="{url}" rel="noopener" target="_blank">{naam}</a>')
    return ", ".join(uit)


def _data():
    def kaal(d, velden):
        return {k: {f: v[f] for f in velden if f in v} for k, v in d.items()}
    return {
        "kamer": KAMER,
        "wand": kaal(TEGELS_WAND, ["naam", "formaat", "niveau", "tex"]),
        "vloer": kaal(TEGELS_VLOER, ["naam", "formaat", "niveau", "tex"]),
        "kraan": kaal(KRANEN, ["naam", "kleur", "metal", "rough"]),
        "meubel": kaal(MEUBELS, ["naam", "niveau"]),
        "indeling": kaal(INDELING, ["naam"]),
        "start": START,
        "prijs": prijzen(),
        "m2": {"wand": WAND_M2, "vloer": VLOER_M2},
    }


# ---------------------------------------------------------------------------- HTML

POSTER = "badkamer-3d"
POSTER_ALT = ("3D-badkamer met groene zellige-look wandtegels, betonlook vloer, inloopdouche met glazen wand, "
              "zwevend houten badmeubel met ronde spiegel en hangtoilet")


def _poster_html():
    map_ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fotos", "renders")
    if not os.path.exists(os.path.join(map_, f"{POSTER}-800.webp")):
        return '<div class="b3-poster b3-poster-leeg" aria-hidden="true"></div>'
    return (f'<img class="b3-poster" src="/assets/fotos/renders/{POSTER}-800.webp" '
            f'srcset="/assets/fotos/renders/{POSTER}-800.webp 800w, /assets/fotos/renders/{POSTER}-1600.webp 1600w" '
            f'sizes="(min-width: 1000px) 720px, 100vw" width="1600" height="1200" alt="{POSTER_ALT}" '
            f'loading="eager" fetchpriority="high" decoding="async">')


def _keuzes(naam, legend, opties, gekozen, extra=lambda k, o: ""):
    knoppen = "".join(
        f'<label class="b3-optie"><input type="radio" name="b3-{naam}" value="{k}"{" checked" if k == gekozen else ""}>'
        f'<span class="b3-swatch" style="background:{o["swatch"]}" data-b3-sw="{naam}-{k}"></span>'
        f'<span class="b3-label">{o["naam"]}{extra(k, o)}</span></label>'
        for k, o in opties.items())
    return f'<fieldset class="b3-set"><legend>{legend}</legend><div class="b3-opties">{knoppen}</div></fieldset>'


def _formaat(k, o):
    return f'<small>{o["formaat"]}</small>'


INDELING_SWATCH = {
    "douche": {"naam": "Inloopdouche", "swatch": "linear-gradient(90deg,rgba(190,220,225,.9) 0 46%,#2b2d30 46% 50%,#e9e6df 50%)"},
    "bad": {"naam": "Ligbad", "swatch": "radial-gradient(ellipse 60% 40% at 50% 55%,#cfe3e6 0 60%,#fff 62%)"},
}


def _tool_html():
    return f"""<div class="b3-tool" data-b3>
  <div class="b3-grid">
    <div class="b3-kijk">
      <div class="b3-stage" data-b3-stage>
        {_poster_html()}
        <div class="b3-start" data-b3-startblok>
          <button type="button" class="btn btn-primary b3-startknop" data-b3-start>{_icoon_3d()} Start 3D</button>
          <p>Laadt ongeveer 0,7 MB. Werkt ook op je telefoon.</p>
        </div>
        <p class="b3-melding" data-b3-melding role="status" hidden></p>
        <div class="b3-knoppen" data-b3-knoppen hidden>
          <button type="button" data-b3-cam="links" aria-label="Draai naar links">&#8630;</button>
          <button type="button" data-b3-cam="rechts" aria-label="Draai naar rechts">&#8631;</button>
          <button type="button" data-b3-cam="in" aria-label="Zoom in">+</button>
          <button type="button" data-b3-cam="uit" aria-label="Zoom uit">&minus;</button>
          <button type="button" data-b3-cam="terug" aria-label="Terug naar het beginbeeld">&#8962;</button>
        </div>
        <span class="b3-bijschrift">Illustratie (3D)</span>
      </div>
      <p class="b3-hulp" data-b3-hulp>Klik op <strong>Start 3D</strong>. Daarna sleep je met je muis of vinger om rond te kijken. Zoomen doe je met het scrollwiel of door te knijpen. De knoppen rechtsonder werken ook.</p>
    </div>
    <div class="b3-paneel">
      <form data-b3-form onsubmit="return false">
        {_keuzes("wand", "Wandtegels", TEGELS_WAND, START["wand"], _formaat)}
        {_keuzes("vloer", "Vloertegels", TEGELS_VLOER, START["vloer"], _formaat)}
        {_keuzes("kraan", "Kranen en details", KRANEN, START["kraan"])}
        {_keuzes("meubel", "Badmeubel", MEUBELS, START["meubel"])}
        {_keuzes("indeling", "Douche of bad", INDELING_SWATCH, START["indeling"])}
      </form>
      <div class="b3-prijs" aria-live="polite">
        <small>Prijsindicatie voor deze badkamer</small>
        <b data-b3-totaal>–</b>
        <span class="b3-klein">Complete renovatie, inclusief 21% btw. Rekenvoorbeeld van {str(KAMER["b"]).replace(".", ",")} × {str(KAMER["d"]).replace(".", ",")} meter.</span>
        <p class="b3-klein" data-b3-kraannoot></p>
        <details><summary>Zo is de prijs opgebouwd</summary>
          <ul class="b3-posten" data-b3-posten></ul>
        </details>
      </div>
      <a class="btn btn-primary b3-mee" href="/offerte-aanvragen/?via=3d" data-b3-mee>Vraag offertes aan met deze keuzes</a>
      <p class="b3-klein" style="margin:8px 0 0">Je keuzes blijven in je browser. Kies je voor offertes, dan zetten we alleen een korte beschrijving klaar in het formulier. Die kun je zelf nog aanpassen.</p>
    </div>
  </div>
</div>"""


def _icoon_3d():
    return ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            'stroke-linejoin="round" aria-hidden="true" style="vertical-align:-4px"><path d="M12 2 3 7v10l9 5 9-5V7z"/>'
            '<path d="m3 7 9 5 9-5M12 12v10"/></svg>')


CSS = """<style>
.b3-tool{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:12px;min-width:0}
@media(min-width:900px){.b3-tool{padding:22px}}
.b3-tool [hidden]{display:none!important}
.b3-grid{display:grid;gap:18px}
.b3-grid>div{min-width:0}
@media(min-width:1000px){.b3-grid{grid-template-columns:minmax(0,1fr) 340px;align-items:start}.b3-kijk{position:sticky;top:90px}}
.b3-stage{position:relative;aspect-ratio:4/3;border-radius:var(--radius);overflow:hidden;background:linear-gradient(180deg,#eef4f4,#dfe8e8)}
.b3-poster{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.b3-poster-leeg{background:linear-gradient(160deg,#5b8a75 0 38%,#e9e6df 38% 40%,#5b8a75 40% 70%,#8e8c87 70%)}
.b3-stage canvas{position:absolute;inset:0;width:100%!important;height:100%!important;display:block;touch-action:none;outline:none}
.b3-start{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;background:linear-gradient(180deg,rgba(8,47,55,0) 40%,rgba(8,47,55,.55));padding:16px;text-align:center}
.b3-start p{margin:0;color:#fff;font-size:.82rem;text-shadow:0 1px 3px rgba(0,0,0,.5)}
.b3-startknop{font-size:1.05rem;padding:14px 26px;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.b3-melding{position:absolute;left:12px;right:12px;top:12px;margin:0;background:rgba(255,255,255,.94);border-radius:10px;padding:10px 12px;font-size:.88rem;color:var(--ink);box-shadow:var(--shadow)}
.b3-knoppen{position:absolute;right:8px;bottom:8px;display:flex;gap:6px}
.b3-knoppen button{width:40px;height:40px;border-radius:50%;border:1px solid rgba(8,47,55,.15);background:rgba(255,255,255,.92);color:var(--ink);font-size:1.15rem;line-height:1;cursor:pointer;box-shadow:0 2px 6px rgba(0,0,0,.12)}
.b3-knoppen button:hover{background:#fff;border-color:var(--navy)}
.b3-knoppen button:focus-visible{outline:3px solid var(--accent);outline-offset:1px}
.b3-bijschrift{position:absolute;left:8px;top:8px;background:rgba(255,255,255,.88);color:#334;font-size:.72rem;padding:3px 8px;border-radius:999px;pointer-events:none}
.b3-hulp{font-size:.84rem;color:var(--muted);margin:8px 2px 0}
.b3-set{border:0;padding:0;margin:0 0 14px;min-width:0}
.b3-set legend{font-weight:700;color:var(--ink);font-size:.95rem;padding:0;margin:0 0 6px}
.b3-opties{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}
.b3-optie{position:relative;display:flex;align-items:center;gap:8px;border:1px solid var(--line);border-radius:10px;padding:7px 8px;cursor:pointer;font-size:.86rem;line-height:1.25;color:var(--ink);background:#fff;min-height:48px}
.b3-optie:hover{border-color:var(--navy-500)}
.b3-optie input{position:absolute;opacity:0;width:1px;height:1px}
.b3-optie:has(input:checked){border-color:var(--navy);box-shadow:inset 0 0 0 1px var(--navy);background:var(--bg-soft)}
.b3-optie:has(input:focus-visible){outline:3px solid var(--accent);outline-offset:1px}
.b3-swatch{flex:0 0 30px;height:30px;border-radius:7px;border:1px solid rgba(0,0,0,.12);background-size:cover}
.b3-label small{display:block;color:var(--muted);font-size:.76rem}
.b3-prijs{background:var(--bg-soft);border-radius:var(--radius);padding:14px;margin:4px 0 14px}
.b3-prijs>small{display:block;color:var(--muted);font-size:.82rem}
.b3-prijs>b{display:block;font-size:1.5rem;color:var(--ink);margin:2px 0 4px}
.b3-klein{font-size:.8rem;color:var(--muted);display:block}
.b3-prijs p.b3-klein{margin:6px 0 0}
.b3-prijs summary{cursor:pointer;font-weight:600;font-size:.88rem;margin-top:8px;color:var(--ink)}
.b3-posten{list-style:none;margin:8px 0 0;padding:0;font-size:.84rem}
.b3-posten li{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-bottom:1px solid var(--line)}
.b3-posten b{white-space:nowrap;font-weight:600;color:var(--ink)}
.b3-mee{display:block;text-align:center;width:100%}
.b3-tabel{width:100%;border-collapse:collapse;font-size:.92rem}
.b3-tabel th,.b3-tabel td{padding:8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
@media(prefers-reduced-motion:reduce){.b3-tool *{transition:none!important;animation:none!important}}
</style>"""


def _js():
    return "<script>\n" + JS.replace("__DATA__", json.dumps(_data(), ensure_ascii=False)) + "\n</script>"


def _euro(n):
    return "€ " + f"{int(n):,}".replace(",", ".")


def _uitleg_html():
    p = prijzen()
    niv = RP.niveaus("tegels")
    rij = lambda n: f"{_euro(niv[n][0])} – {_euro(niv[n][1])}"
    return f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Zo werkt de 3D-badkamer</h2>
  <ol>
    <li><strong>Start de 3D-weergave.</strong> Pas dan laadt de 3D-techniek. Zo blijft de pagina snel.</li>
    <li><strong>Kijk rond.</strong> Sleep om de badkamer te draaien en zoom in op details, zoals de kraan of de voegen.</li>
    <li><strong>Kies je materialen.</strong> Wissel wandtegels, vloertegels, de kleur van de kranen, het badmeubel en douche of bad. De badkamer verandert meteen mee.</li>
    <li><strong>Bekijk de prijs.</strong> Onder je keuzes staat wat zo'n badkamer ongeveer kost, met de opbouw per post.</li>
    <li><strong>Vraag offertes aan.</strong> Met één klik gaan je keuzes als korte tekst mee naar het aanvraagformulier.</li>
  </ol>
  <p>De 3D-badkamer is een illustratie. Kleuren op een scherm wijken af van echte tegels. Bekijk tegels daarom altijd in het echt, het liefst bij daglicht en naast elkaar.</p>

  <h2>Zo rekenen we de prijsindicatie</h2>
  <p>We rekenen met een badkamer van {str(KAMER["b"]).replace(".", ",")} bij {str(KAMER["d"]).replace(".", ",")} meter. De wanden zijn betegeld tot het plafond. Dat is ongeveer {str(VLOER_M2).replace(".", ",")} m² vloer en {WAND_M2} m² wand. Voor snijverlies tellen we 10% extra tegels.</p>
  <div style="overflow-x:auto"><table class="b3-tabel">
    <thead><tr><th>Tegelniveau</th><th>Prijs per m² (alleen de tegel)</th><th>Tegels in de tool</th></tr></thead>
    <tbody>
      <tr><td>Basis</td><td>{rij("basis")}</td><td>wit glans, metrotegel, betonlook</td></tr>
      <tr><td>Midden</td><td>{rij("midden")}</td><td>zellige-look, houtlook, cementlook</td></tr>
      <tr><td>Luxe</td><td>{rij("luxe")}</td><td>marmerlook groot formaat, terrazzo</td></tr>
    </tbody></table></div>
  <ul>
    <li><strong>Tegels zetten</strong> met lijm en voeg: {_euro(p["zetten"][0])} tot {_euro(p["zetten"][1])} voor de hele badkamer. Kleine tegels zoals zellige en metro kosten vaak meer werk dan grote. Reken dan eerder op de bovenkant.</li>
    <li><strong>Inloopdouche of bad</strong> op middenniveau, met plaatsen en aansluiten. Een inloopdouche: {_euro(p["indeling"]["douche"][0])} tot {_euro(p["indeling"]["douche"][1])}. Een ligbad: {_euro(p["indeling"]["bad"][0])} tot {_euro(p["indeling"]["bad"][1])}.</li>
    <li><strong>Badmeubel</strong> met wastafel, kraan en spiegel. Een wit gelakt meubel rekenen we als basis, een houten meubel als midden.</li>
    <li><strong>Kranen</strong> zitten in de prijs van de douche, het bad en het meubel. Mat zwart en goud zijn vaak iets duurder dan chroom, maar dat verschilt sterk per merk. We tellen het daarom niet apart.</li>
    <li><strong>Vaste posten:</strong> slopen en afvoeren, leidingwerk, waterdicht maken, elektra en een ventilator, en een hangtoilet op middenniveau.</li>
  </ul>
  <p>Vloerverwarming, een radiator, verlichting en extra's zoals een nis zitten er niet in. Wil je dat erbij? Reken het uit met de <a href="/tools/badkamercalculator/">badkamercalculator</a>.</p>
  <p class="b3-klein">Richtprijzen inclusief 21% btw, geraadpleegd in november 2026. Het is een indicatie, geen offerte. Bronnen: {_prijsbronnen()}.</p>
</div></section>
<section class="section"><div class="wrap narrow prose">
  <h2>Tips voor een badkamer die klopt</h2>
  <ul>
    <li><strong>Eén blikvanger is genoeg.</strong> Kies je een drukke vloer, zoals cementlook of terrazzo, dan werkt een rustige wand vaak beter. Andersom kan ook: groene zellige op de wand met een egale vloer.</li>
    <li><strong>Laat de kranen terugkomen.</strong> Neem dezelfde kleur voor de kranen, de douchestang, het profiel van de glazen wand en de spoelknop. Dat ziet er rustig uit.</li>
    <li><strong>Mat zwart en goud</strong> laten minder kalkvlekken zien dan je denkt, maar je ziet wel waterdruppels. Chroom is het makkelijkst schoon te houden.</li>
    <li><strong>Hout in de badkamer</strong> kan prima, als het goed gelakt of gefineerd is. Een zwevend meubel maakt de vloer vrij en de ruimte lijkt groter.</li>
    <li><strong>Twijfel je over de indeling?</strong> Teken je badkamer eerst op schaal in de <a href="/tools/indelingsplanner/">indelingsplanner</a>. Een snelle stijl uitproberen kan ook in de <a href="/tools/stijlkiezer/">stijlkiezer</a>.</li>
  </ul>
</div></section>"""


FAQS = [
    ("Is de 3D-badkamer een echte badkamer?",
     "Nee. Het is een illustratie die we zelf in 3D hebben gemaakt. De tegels, kranen en het meubel zijn voorbeelden, geen producten van een bepaald merk. Zo krijg je een indruk van hoe kleuren en materialen samen werken."),
    ("Waarom staat er een prijs bij mijn keuzes?",
     "Zodat je ziet wat je keuzes ongeveer betekenen voor je budget. We rekenen met richtprijzen van sites als Werkspot, Trustoo en Homedeal, voor een badkamer van ongeveer 6 m². Een echte prijs hangt af van jouw badkamer. Die krijg je pas als een specialist komt kijken."),
    ("Werkt de 3D-badkamer op mijn telefoon?",
     "Ja. Je draait met één vinger en zoomt door te knijpen. Werkt 3D niet in je browser, dan zie je een vaste afbeelding. Je kunt dan nog steeds kiezen en de prijs bekijken."),
    ("Wat gebeurt er met mijn keuzes?",
     "Niets, zolang je niet zelf iets verstuurt. Alles blijft in je browser. Klik je op de knop om offertes aan te vragen, dan zetten we een korte beschrijving van je keuzes in het formulier. Die gaat pas mee als je het formulier zelf verstuurt."),
    ("Zijn mat zwarte of gouden kranen duurder?",
     "Vaak wel een beetje, omdat de afwerking meer werk is. Het verschil hangt sterk af van het merk en de serie. Bij goedkope en dure series kan het verschil klein of juist groot zijn. Vraag de specialist om de kraan in de offerte met merk en typenummer te noemen."),
]


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("3D-badkamer", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over de 3D-badkamer")
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "3D-badkamer",
        "applicationCategory": "DesignApplication",
        "operatingSystem": "Alle browsers met WebGL",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Kijk rond in een 3D-badkamer en kies tegels, kraankleur, badmeubel en douche of bad, met een prijsindicatie.",
    }
    body = f"""{cr}
{CSS}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:20px">
    <span class="badge">Gratis tool</span>
    <h1>3D-badkamer: kijk rond en kies zelf</h1>
    <p class="lead">Draai rond in een badkamer en kies je tegels voor de wand en de vloer, de kleur van de kranen, het meubel en een inloopdouche of een bad. Je ziet meteen hoe het eruitziet en wat het ongeveer kost.</p>
  </div>
  {_tool_html()}
</div></section>
<section class="section-sm"><div class="wrap narrow">
  {cta_midden("Blij met je keuzes? Laat er een echte prijs voor maken", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Je keuzes gaan als korte tekst mee.", "Offertes aanvragen met mijn keuzes", "/offerte-aanvragen/?via=3d")}
</div></section>
{_uitleg_html()}
<section class="section-sm"><div class="wrap narrow">{offertecheck_blok("je nieuwe badkamer")}</div></section>
{faq_html}
{cta_blok("Van 3D naar je eigen badkamer", "Vergelijk gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten. Zij kijken ook naar de leidingen, de afvoer en wat er in jouw ruimte kan.", "Gratis offertes aanvragen")}
{_js()}"""
    write(PAD, page(
        title("3D-badkamer: kijk rond en kies je tegels"),
        desc("Kijk gratis rond in een 3D-badkamer en kies je wandtegels, vloertegels, kraankleur, meubel en douche of bad.",
             "Met een prijsindicatie die meteen meeloopt."),
        PAD, body, jsonld=[cr_ld, app_ld, faq_ld]), prio=0.7)
