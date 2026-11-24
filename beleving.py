# -*- coding: utf-8 -*-
"""Beleving (ronde 3, agent A10): site-brede micro-interacties en extra homepagesecties.

Geen eigen pagina's. De hoofdsessie bouwt dit in (zie INTEGRATIE.md in de uitvoermap van A10):
- BELEVING_CSS  -> achter STYLE_CSS in assets.py   (STYLE_CSS += BELEVING_CSS)
- BELEVING_JS   -> achter APP_JS in assets.py      (APP_JS += BELEVING_JS)
- hero_visual(), sectie_stijlen(), sectie_droombadkamer(), sectie_ontdek(), sectie_cijfers()
  -> html-blokken voor build_home() in build.py.

Elke sectie is zelfstandig: eigen <style> (voorvoegsel .bl-) en waar nodig een eigen inline <script>.
Alle renders zijn eigen 3D-illustraties en staan er met "Illustratie (3D-render)" bij.

Prijzen in de droombadkamer-quiz: dezelfde bandbreedtes als /kosten/nieuwe-badkamer/ en /inspiratie/
(badkamer_inspiratie.NIVEAUS), geraadpleegd november 2026:
- Homedeal, badkamer renoveren (€3.500 – €15.000): https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/
- Trustoo, nieuwe badkamer (€8.500 – €15.000 voor 5 – 10 m²): https://trustoo.nl/kosten/badkamer-renovatie-kosten/
- Slimster (budget €3.000 – €7.000, midden €7.500 – €11.000, luxe €11.000 – €15.000):
  https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/
Alle bedragen inclusief 21% btw, voor een complete badkamer van 5 tot 9 m².
"""

import html as _h
import json
import os

from components import icon, eur
from render_data import RENDERS
from render_stijl_data import RENDERS_STIJL

_ROOT = os.path.dirname(os.path.abspath(__file__))
_RMAP = os.path.join(_ROOT, "fotos", "renders")

try:
    from badkamer_inspiratie import NIVEAUS as _NIVEAUS, BRONNEN_KOSTEN as _BRONNEN_KOSTEN
except Exception:  # zelfde waarden als op de kostenpagina
    _NIVEAUS = [("Basis", 3500, 7000), ("Midden", 7000, 12000), ("Luxe", 12000, 20000)]
    _BRONNEN_KOSTEN = [
        ("Homedeal, badkamer renoveren kosten", "https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/"),
        ("Trustoo, wat kost een nieuwe badkamer", "https://trustoo.nl/kosten/badkamer-renovatie-kosten/"),
        ("Slimster, compleet nieuwe badkamer kosten", "https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/"),
    ]

_MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus",
            "september", "oktober", "november", "december"]


def _esc(s):
    return _h.escape(str(s), quote=True)


def _bestaat(naam):
    return os.path.exists(os.path.join(_RMAP, f"{naam}-800.webp"))


def _img(naam, alt, sizes, w=1600, h=1067, lazy=True, klasse=""):
    """Render als <img> met srcset en vaste verhouding (geen layout shift)."""
    if not _bestaat(naam):
        return ""
    klein = f"/assets/fotos/renders/{naam}-400.webp 400w, " if os.path.exists(os.path.join(_RMAP, f"{naam}-400.webp")) else ""
    laden = 'loading="lazy"' if lazy else 'loading="eager" fetchpriority="high"'
    return (f'<img class="{klasse}" src="/assets/fotos/renders/{naam}-800.webp" '
            f'srcset="{klein}/assets/fotos/renders/{naam}-800.webp 800w, /assets/fotos/renders/{naam}-1600.webp 1600w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{_esc(alt)}" {laden} decoding="async">')


def _peildatum():
    try:
        from producten_badkamer import PRODUCTDATA
        j, m = PRODUCTDATA["peildatum"].split("-")[:2]
        return f"{_MAANDEN[int(m) - 1]} {j}"
    except Exception:
        return "november 2026"


# ===========================================================================
# 1. Site-brede micro-interacties
# ===========================================================================
# Wat al in assets.py zit (niet dubbel doen): .reveal/.rv-onthulling, .header.is-gescrold,
# kaartlift met spotlicht op a.card en .tool-kaart, fade bij het openen van .faq.
# Dit blok vult aan: onthulling voor wat daar buiten valt (eigen secties, renders, het
# voorbeeld van de offertecheck), hover-diepte op .bl-kaart en renders in links, een echte
# hoogte-animatie voor de FAQ en een header-schaduw die geleidelijk aanzwelt.

BELEVING_CSS = r"""
/* ---------- Beleving (A10): micro-interacties ---------- */
.header{box-shadow:0 1px 0 rgba(11,74,86,calc(var(--bl-s,0)*.04)),0 8px 24px rgba(11,74,86,calc(var(--bl-s,0)*.09))}
.header.is-gescrold{box-shadow:0 1px 0 rgba(11,74,86,calc(var(--bl-s,1)*.04)),0 8px 24px rgba(11,74,86,calc(var(--bl-s,1)*.09))}
.bl-js .bl-rv{opacity:0;transform:translateY(18px);transition:opacity .6s cubic-bezier(.2,.7,.2,1),transform .6s cubic-bezier(.2,.7,.2,1);transition-delay:calc(var(--bl-i,0)*80ms)}
.bl-js .bl-rv.bl-in{opacity:1;transform:none}
.bl-kaart{transition:transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s ease,border-color .2s}
.bl-kaart:hover,.bl-kaart:focus-visible{transform:translateY(-4px);box-shadow:0 2px 4px rgba(11,74,86,.06),0 22px 48px rgba(11,74,86,.15);text-decoration:none}
.bl-kaart:focus-visible{outline:3px solid #f0a37f;outline-offset:3px}
.bl-kaart img,a .foto.render img{transition:transform .6s cubic-bezier(.2,.7,.2,1)}
a .foto.render{overflow:hidden;border-radius:var(--radius)}
.bl-kaart:hover img,a:hover .foto.render img{transform:scale(1.04)}
.faq details .a{overflow:hidden}
@media (prefers-reduced-motion:reduce){
  .bl-js .bl-rv{opacity:1;transform:none;transition:none}
  .bl-kaart,.bl-kaart img,a .foto.render img{transition:none}
  .bl-kaart:hover,.bl-kaart:hover img,a:hover .foto.render img{transform:none}
}
"""

BELEVING_JS = r"""
/* ---------- Beleving (A10): onthulling, FAQ-accordeon, header-schaduw ---------- */
(function () {
  "use strict";
  var rust = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var h = document.querySelector(".header");
  if (h) {
    var w = false, z = function () { w = false; h.style.setProperty("--bl-s", Math.min(1, window.scrollY / 160).toFixed(2)); };
    window.addEventListener("scroll", function () { if (!w) { w = true; requestAnimationFrame(z); } }, { passive: true });
    z();
  }
  if (rust) return;
  /* FAQ: open en dicht met een hoogte-animatie */
  document.addEventListener("click", function (e) {
    var s = e.target.closest && e.target.closest(".faq summary");
    if (!s) return;
    var d = s.parentElement, a = d.querySelector(".a");
    if (!a || !a.animate) return;
    e.preventDefault();
    if (d.bl) return;
    d.bl = 1;
    var klaar = function () { d.bl = 0; };
    if (!d.open) {
      d.open = true;
      var cs = getComputedStyle(a);
      a.animate([{ height: "0px", paddingTop: "0px", paddingBottom: "0px", opacity: 0 },
                 { height: a.offsetHeight + "px", paddingTop: cs.paddingTop, paddingBottom: cs.paddingBottom, opacity: 1 }],
                { duration: 280, easing: "cubic-bezier(.2,.7,.2,1)" }).onfinish = klaar;
    } else {
      var an = a.animate([{ height: a.offsetHeight + "px", opacity: 1 }, { height: "0px", paddingTop: "0px", paddingBottom: "0px", opacity: 0 }],
                         { duration: 200, easing: "ease-in" });
      an.onfinish = function () { d.open = false; klaar(); };
    }
  });
  /* Onthulling: alleen wat bij het laden onder de vouw staat en nog niet door .reveal/.rv wordt gedaan */
  if (!("IntersectionObserver" in window)) return;
  var vouw = window.innerHeight;
  var el = [].slice.call(document.querySelectorAll("[data-bl-rv], [data-bl-groep] > *, .ov-voorbeeld, .section .foto.render, .faq"))
    .filter(function (x) { return !x.closest(".reveal, .rv, .bl-rv") && x.getBoundingClientRect().top > vouw; });
  if (!el.length) return;
  document.documentElement.classList.add("bl-js");
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("bl-in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -6% 0px", threshold: 0 });
  el.forEach(function (x) {
    var p = x.parentElement;
    if (p && p.hasAttribute("data-bl-groep")) x.style.setProperty("--bl-i", Math.min([].indexOf.call(p.children, x), 5));
    x.classList.add("bl-rv");
    io.observe(x);
  });
})();
"""


# ===========================================================================
# 2. Hero-visual: render bd-home met een zwevende voorbeelduitslag
# ===========================================================================

def hero_visual():
    """Gelaagde compositie: render bd-home op een tegelraster, met een zwevende voorbeelduitslag
    van de offertecheck (verzonnen offerte, echte prijsbanden). Responsief."""
    import richtprijzen as RP
    tg = RP.RICHTPRIJZEN["tegelwerk"]
    n_art, product = 0, None
    try:
        from producten_badkamer import PRODUCTDATA
        n_art = len(PRODUCTDATA["artikelen"])
        product = next((a for a in PRODUCTDATA["artikelen"] if "34558000" in a.get("codes", [])), None) \
            or next((a for a in PRODUCTDATA["artikelen"] if a.get("categorie") == "thermostaatkraan"), None)
    except Exception:
        pass
    r = RENDERS["home"]
    beeld = _img(r["naam"], r["alt"], "(max-width: 900px) 92vw, 560px")
    rij_p = ""
    if product:
        op_offerte = 200  # verzonnen offertebedrag incl. btw, alleen voor dit voorbeeld
        pct = round((op_offerte - product["tot"]) / product["tot"] * 100)
        tag = (f'<span class="bl-tag bl-boven">{pct}% boven</span>' if pct > 0
               else '<span class="bl-tag bl-binnen">binnen de band</span>')
        rij_p = (f'<li><span class="bl-soort">Product · thermostaatkraan</span><div class="bl-r"><strong>{eur(op_offerte)}</strong>{tag}</div>'
                 f'<small>Marktband {eur(product["van"])} – {eur(product["tot"])} incl. btw</small></li>')
    return f"""<style>
.bl-hv{{position:relative;padding:22px 0 0 22px;max-width:600px;margin:0 auto}}
.bl-hv::before{{content:"";position:absolute;left:0;top:0;right:42px;bottom:60px;border-radius:22px;z-index:0;
  background:linear-gradient(#e7f0f1 1px,transparent 1px) 0 0/28px 28px,linear-gradient(90deg,#e7f0f1 1px,#f6fafa 1px) 0 0/28px 28px}}
.bl-hv-frame{{position:relative;z-index:1;border-radius:18px;overflow:hidden;box-shadow:0 30px 60px -20px rgba(8,47,55,.35);aspect-ratio:3/2;background:#dfe9ea}}
.bl-hv-frame img{{width:100%;height:100%;object-fit:cover;display:block}}
.bl-hv-ill{{position:absolute;right:12px;bottom:12px;background:rgba(255,255,255,.9);color:#334;font-size:.72rem;padding:3px 9px;border-radius:99px}}
.bl-hv-kaart{{position:absolute;z-index:2;left:-18px;bottom:-84px;width:min(290px,62%);background:#fff;border-radius:16px;padding:14px 16px 12px;
  box-shadow:0 2px 4px rgba(11,74,86,.08),0 24px 50px rgba(11,74,86,.22);border:1px solid #e3ecee;font-size:.86rem;animation:bl-zweef 6s ease-in-out infinite}}
.bl-hv-kop{{display:flex;justify-content:space-between;align-items:center;font-weight:700;color:var(--navy);margin-bottom:6px}}
.bl-hv-label{{font-size:.68rem;text-transform:uppercase;letter-spacing:.06em;background:#eef3f4;color:#55696e;border-radius:99px;padding:3px 9px}}
.bl-hv-kaart ul{{list-style:none;margin:0;padding:0}}
.bl-hv-kaart li{{border-top:1px solid #edf2f3;padding:7px 0;margin:0}}
.bl-hv-kaart li:first-child{{border-top:0}}
.bl-soort{{display:block;font-size:.66rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#55696e}}
.bl-r{{display:flex;justify-content:space-between;gap:8px;align-items:center}}
.bl-r strong{{color:var(--ink);font-size:.92rem}}
.bl-hv-kaart small{{color:#55696e;font-size:.76rem}}
.bl-tag{{font-size:.72rem;font-weight:700;border-radius:99px;padding:2px 8px;white-space:nowrap}}
.bl-binnen{{background:#e3f4ea;color:#1d6b3e}}.bl-boven{{background:#fdecdf;color:#9a3d12}}.bl-vaag{{background:#fff4d6;color:#7a5800}}
.bl-hv-chip{{position:absolute;z-index:2;right:0;top:-4px;background:var(--navy);color:#fff;border-radius:12px;padding:8px 12px;font-size:.8rem;font-weight:600;
  box-shadow:0 12px 30px rgba(8,47,55,.3);display:flex;gap:8px;align-items:center;max-width:220px;line-height:1.3}}
.bl-hv-chip svg{{flex:0 0 auto;color:#f4c7b5}}
.bl-hv-noot{{margin:6px 0 0;font-size:.74rem;color:#55696e;border-top:1px solid #edf2f3;padding-top:7px}}
.bl-hv{{margin-bottom:96px}}
@keyframes bl-zweef{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-6px)}}}}
@media (max-width:600px){{
  .bl-hv{{padding:14px 0 0 14px}}
  .bl-hv::before{{right:24px;bottom:auto;height:70%}}
  .bl-hv-kaart{{position:relative;left:auto;bottom:auto;width:auto;margin:-36px 10px 0 14px;animation:none}}
  .bl-hv-chip{{top:-8px;right:4px;font-size:.74rem;padding:6px 10px}}
  .bl-hv-ill{{left:10px;top:10px;right:auto;bottom:auto}}
  .bl-hv{{margin-bottom:0}}
}}
@media (prefers-reduced-motion:reduce){{.bl-hv-kaart{{animation:none}}}}
</style>
<figure class="bl-hv" aria-label="Illustratie van een badkamer met een voorbeelduitslag van de offertecheck">
  <div class="bl-hv-frame">{beeld}<span class="bl-hv-ill">Illustratie (3D-render)</span></div>
  {f'<div class="bl-hv-chip">{icon("check", 16)}<span>{n_art} producten met een marktprijs</span></div>' if n_art else ''}
  <div class="bl-hv-kaart">
    <div class="bl-hv-kop"><span>Uitslag per regel</span><span class="bl-hv-label">Voorbeeld</span></div>
    <ul>
      {rij_p}
      <li><span class="bl-soort">Arbeid · tegelwerk 28 m²</span><div class="bl-r"><strong>€40 per m²</strong><span class="bl-tag bl-binnen">binnen de richtprijs</span></div>
        <small>Richtprijs {eur(tg['laag'])} – {eur(tg['hoog'])} per m² incl. btw</small></li>
      <li><span class="bl-soort">Materiaal</span><div class="bl-r"><strong>Sanitair compleet</strong><span class="bl-tag bl-vaag">te vaag</span></div></li>
    </ul>
    <p class="bl-hv-noot">Verzonnen offerte, echte prijsbanden ({_peildatum()}).</p>
  </div>
</figure>"""


# ===========================================================================
# 3. Stijlen-carrousel
# ===========================================================================

# Nieuwe stijlpagina's van A4. Ze komen alleen in de carrousel als hun render bestaat (bs-<slug>).
_EXTRA_STIJLEN = {
    "scandinavische-badkamer": ("Scandinavisch", "Licht hout, wit en zachte grijstinten."),
    "luxe-badkamer": ("Luxe", "Ruim, warm licht en materialen met diepte."),
    "marmer-badkamer": ("Marmer", "Natuursteen of marmerlook met een rustige ader."),
    "zwart-wit-badkamer": ("Zwart-wit", "Grafisch contrast met wit en mat zwart."),
    "terrazzo-badkamer": ("Terrazzo", "Speelse stukjes steen in vloer of wand."),
    "wellness-badkamer": ("Wellness", "Regendouche, warmte en rust, zoals in een spa."),
}


def _stijl_lijst():
    try:
        from badkamer_inspiratie import LINKS as IL
        beschr = {p.strip("/").split("/")[-1]: (t, d) for p, t, d in IL[1:]}
    except Exception:
        beschr = {}
    uit = []
    for slug, r in RENDERS_STIJL.items():
        t, d = beschr.get(slug, (slug.replace("-", " ").capitalize(), ""))
        kort = {"moderne-badkamer": "Modern", "landelijke-badkamer": "Landelijk", "industriele-badkamer": "Industrieel",
                "japandi-badkamer": "Japandi", "klassieke-badkamer": "Klassiek", "kleine-badkamer": "Kleine badkamer"}
        uit.append((slug, kort.get(slug, t), d, r["naam"], r["alt"]))
    try:  # renders van A4 (render_stijl_data2.py, b4-<slug>-1); alleen als het bestand bestaat
        from render_stijl_data2 import RENDERS_STIJL2 as R2
    except Exception:
        R2 = {}
    for slug, (t, d) in _EXTRA_STIJLEN.items():
        r = R2.get(slug)
        if r and _bestaat(r["naam"]):
            uit.append((slug, t, d, r["naam"], r["alt"]))
    return uit


def sectie_stijlen():
    """Horizontale, swipebare carrousel met de stijlrenders; elke kaart linkt naar /inspiratie/<stijl>/."""
    kaarten = "".join(
        f'<li class="bl-sc-item"><a class="bl-kaart bl-sc-kaart" href="/inspiratie/{slug}/">'
        f'<span class="bl-sc-beeld">{_img(naam, alt, "(max-width: 600px) 80vw, 380px")}<span class="bl-sc-ill">Illustratie (3D-render)</span></span>'
        f'<span class="bl-sc-tekst"><strong>{_esc(t)}</strong><span>{_esc(d)}</span><em>Bekijk deze stijl →</em></span></a></li>'
        for slug, t, d, naam, alt in _stijl_lijst())
    return f"""<section class="section bl-sc" aria-labelledby="bl-sc-kop">
<style>
.bl-sc{{overflow:hidden}}
.bl-sc-kop{{display:flex;justify-content:space-between;align-items:flex-end;gap:20px;margin-bottom:24px}}
.bl-sc-kop p{{margin:0;max-width:56ch}}
.bl-sc-knoppen{{display:flex;gap:8px;flex:0 0 auto}}
.bl-sc-knoppen button{{width:46px;height:46px;border-radius:50%;border:1px solid var(--line);background:#fff;color:var(--ink);font-size:1.2rem;cursor:pointer;
  transition:background .2s,border-color .2s,opacity .2s,transform .15s}}
.bl-sc-knoppen button:hover:not(:disabled){{border-color:var(--navy-500);background:var(--bg-soft)}}
.bl-sc-knoppen button:active:not(:disabled){{transform:scale(.94)}}
.bl-sc-knoppen button:disabled{{opacity:.35;cursor:default}}
.bl-sc-knoppen button:focus-visible{{outline:3px solid #f0a37f;outline-offset:2px}}
.bl-sc-rail{{list-style:none;margin:0;padding:6px 20px 26px;display:flex;gap:18px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 20px;
  scrollbar-width:none;-webkit-overflow-scrolling:touch;max-width:var(--max);margin:0 auto}}
.bl-sc-rail::-webkit-scrollbar{{display:none}}
.bl-sc-item{{flex:0 0 min(80vw,360px);scroll-snap-align:start;margin:0}}
.bl-sc-kaart{{text-decoration:none;display:block;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;color:var(--body);height:100%}}
.bl-sc-beeld{{display:block;position:relative;aspect-ratio:3/2;overflow:hidden;background:#e6eeef}}
.bl-sc-beeld img{{width:100%;height:100%;object-fit:cover;display:block}}
.bl-sc-ill{{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.9);color:#334;font-size:.7rem;padding:3px 8px;border-radius:99px}}
.bl-sc-tekst{{display:flex;flex-direction:column;gap:4px;padding:16px 18px 18px}}
.bl-sc-tekst strong{{color:var(--ink);font-size:1.12rem}}
.bl-sc-tekst span{{font-size:.93rem;line-height:1.5}}
.bl-sc-tekst em{{font-style:normal;color:var(--accent-dark);font-weight:700;font-size:.9rem;margin-top:6px}}
.bl-sc-voet{{display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
@media (max-width:600px){{.bl-sc-knoppen{{display:none}}.bl-sc-kop{{display:block}}}}
</style>
<div class="wrap">
  <div class="bl-sc-kop" data-bl-rv>
    <div><span class="badge">Inspiratie</span><h2 id="bl-sc-kop">Welke stijl past bij jou?</h2>
    <p class="lead">Swipe door de stijlen. Elke stijl heeft een eigen pagina met materialen, kleuren, kosten en valkuilen.</p></div>
    <div class="bl-sc-knoppen"><button type="button" data-bl-sc="-1" aria-label="Vorige stijlen">←</button><button type="button" data-bl-sc="1" aria-label="Volgende stijlen">→</button></div>
  </div>
</div>
<ul class="bl-sc-rail" data-bl-sc-rail aria-label="Badkamerstijlen" tabindex="0">{kaarten}</ul>
<div class="wrap bl-sc-voet"><a class="btn btn-ghost" href="/inspiratie/">Alle badkamerstijlen</a><a class="btn btn-ghost" href="/tools/stijlkiezer/">Doe de stijlkiezer</a><a class="btn btn-ghost" href="/inspiratie/voor-en-na/">Voor en na</a></div>
<script>
(function () {{
  var rail = document.querySelector("[data-bl-sc-rail]");
  if (!rail) return;
  var kn = document.querySelectorAll("[data-bl-sc]");
  var rust = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var stap = function () {{ var k = rail.querySelector(".bl-sc-item"); return k ? k.offsetWidth + 18 : 300; }};
  var zet = function () {{
    var max = rail.scrollWidth - rail.clientWidth - 4;
    kn[0].disabled = rail.scrollLeft <= 4;
    kn[1].disabled = rail.scrollLeft >= max;
  }};
  kn.forEach(function (b) {{
    b.addEventListener("click", function () {{
      rail.scrollBy({{ left: stap() * parseInt(b.getAttribute("data-bl-sc"), 10), behavior: rust ? "auto" : "smooth" }});
    }});
  }});
  rail.addEventListener("scroll", function () {{ requestAnimationFrame(zet); }}, {{ passive: true }});
  window.addEventListener("resize", zet);
  zet();
}})();
</script>
</section>"""


# ===========================================================================
# 4. Droombadkamer-quiz
# ===========================================================================

_QUIZ_STIJLEN = [
    # (waarde, label, stijlslug, materiaalslug, materiaalnaam)
    ("modern", "Strak en modern", "moderne-badkamer", "keramische-tegels", "keramische tegels"),
    ("landelijk", "Warm en landelijk", "landelijke-badkamer", "natuursteen", "natuursteen"),
    ("japandi", "Rustig en natuurlijk", "japandi-badkamer", "terrazzo", "terrazzo"),
    ("industrieel", "Stoer en industrieel", "industriele-badkamer", "microcement", "microcement"),
    ("klassiek", "Tijdloos en klassiek", "klassieke-badkamer", "kraanafwerkingen", "kraanafwerkingen"),
]
_QUIZ_RUIMTE = [
    ("klein", "Klein", "minder dan 5 m²",
     "Bij een kleine badkamer kom je vaak in de onderste helft uit: minder tegels en minder sloopwerk."),
    ("gemiddeld", "Gemiddeld", "5 tot 9 m²", "Deze bandbreedte geldt voor een badkamer van 5 tot 9 m²."),
    ("groot", "Groot", "meer dan 9 m²",
     "Boven de 9 m² kom je vaak in de bovenste helft uit, of erboven: meer tegels en vaak een bad erbij."),
]


def sectie_droombadkamer():
    """Mini-quiz (ruimte, stijl, budget) met direct een passende stijl, een prijsindicatie met bron en links."""
    niv = [(n.lower(), n, lo, hi) for n, lo, hi in _NIVEAUS]
    data = {
        "stijl": {w: {"t": RENDERS_STIJL.get(s, {}).get("naam") and l, "s": s, "m": m, "mn": mn,
                      "img": f"/assets/fotos/renders/{RENDERS_STIJL[s]['naam']}-800.webp" if s in RENDERS_STIJL else ""}
                  for w, l, s, m, mn in _QUIZ_STIJLEN},
        "niveau": {w: {"n": n, "p": f"{eur(lo)} – {eur(hi)}"} for w, n, lo, hi in niv},
        "ruimte": {w: z for w, _, _, z in _QUIZ_RUIMTE},
    }
    # namen van de stijlen voor in de uitslag
    for w, l, s, m, mn in _QUIZ_STIJLEN:
        data["stijl"][w]["t"] = {"moderne-badkamer": "Moderne badkamer", "landelijke-badkamer": "Landelijke badkamer",
                                 "japandi-badkamer": "Japandi-badkamer", "industriele-badkamer": "Industriële badkamer",
                                 "klassieke-badkamer": "Klassieke badkamer"}[s]

    def vraag(nr, naam, kop, opties):
        knoppen = "".join(
            f'<label class="bl-dq-optie"><input type="radio" name="bl-dq-{naam}" value="{w}"><span><strong>{_esc(l)}</strong>{f"<small>{_esc(sub)}</small>" if sub else ""}</span></label>'
            for w, l, sub in opties)
        return (f'<fieldset class="bl-dq-vraag"><legend><span class="bl-dq-nr">{nr}</span>{kop}</legend>'
                f'<div class="bl-dq-opties">{knoppen}</div></fieldset>')

    vragen = (vraag(1, "ruimte", "Hoe groot is je badkamer?", [(w, l, s) for w, l, s, _ in _QUIZ_RUIMTE])
              + vraag(2, "stijl", "Welke sfeer spreekt je aan?", [(w, l, "") for w, l, *_ in _QUIZ_STIJLEN])
              + vraag(3, "niveau", "Welk niveau past bij je budget?",
                      [(w, n, {"basis": "degelijk en eenvoudig", "midden": "meer keus en comfort", "luxe": "design en extra's"}.get(w, ""))
                       for w, n, _, _ in niv]))
    bronnen = ", ".join(f'<a href="{u}" rel="noopener" target="_blank">{_esc(n.split(",")[0])}</a>' for n, u in _BRONNEN_KOSTEN)
    return f"""<section class="section soft bl-dq" aria-labelledby="bl-dq-kop">
<style>
.bl-dq-grid{{display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:start}}
.bl-dq-vraag{{border:0;margin:0 0 22px;padding:0;min-width:0}}
.bl-dq-vraag legend{{display:flex;align-items:center;gap:10px;font-weight:700;color:var(--ink);font-size:1.05rem;margin-bottom:10px;padding:0}}
.bl-dq-nr{{width:28px;height:28px;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center;font-size:.85rem;flex:0 0 28px}}
.bl-dq-opties{{display:flex;flex-wrap:wrap;gap:8px}}
.bl-dq-optie{{position:relative;cursor:pointer}}
.bl-dq-optie input{{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}}
.bl-dq-optie span{{display:flex;flex-direction:column;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:9px 14px;line-height:1.3;
  transition:border-color .15s,box-shadow .15s,transform .15s,background .15s}}
.bl-dq-optie small{{color:var(--muted);font-size:.78rem}}
.bl-dq-optie strong{{color:var(--ink);font-size:.95rem}}
.bl-dq-optie:hover span{{border-color:#a9c4c9;transform:translateY(-1px)}}
.bl-dq-optie input:focus-visible + span{{outline:3px solid #f0a37f;outline-offset:2px}}
.bl-dq-optie input:checked + span{{border-color:var(--navy-500);background:#eaf4f5;box-shadow:inset 0 0 0 1px var(--navy-500)}}
.bl-dq-uit{{position:sticky;top:90px;background:#fff;border-radius:18px;box-shadow:var(--shadow-lg);overflow:hidden;min-height:420px;display:flex;flex-direction:column}}
.bl-dq-beeld{{aspect-ratio:3/2;background:linear-gradient(135deg,#e3eef0,#f6fafa);position:relative;overflow:hidden}}
.bl-dq-beeld img{{width:100%;height:100%;object-fit:cover;display:block;transition:opacity .35s ease}}
.bl-dq-beeld .bl-dq-ill{{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.9);color:#334;font-size:.7rem;padding:3px 8px;border-radius:99px}}
.bl-dq-wacht{{opacity:.28;filter:grayscale(.6) blur(1px)}}
.bl-dq-leeg{{position:absolute;inset:0;display:grid;place-items:center;text-align:center;color:var(--ink);padding:20px;font-weight:700;font-size:1.05rem}}
.bl-dq-leeg[hidden]{{display:none}}
.bl-dq-body{{padding:18px 20px 20px}}
.bl-dq-voortgang{{height:6px;background:#e8eff0;border-radius:99px;overflow:hidden;margin-bottom:14px}}
.bl-dq-voortgang i{{display:block;height:100%;width:0;background:var(--accent);border-radius:inherit;transition:width .35s cubic-bezier(.2,.7,.2,1)}}
.bl-dq-body h3{{margin:0 0 4px}}
.bl-dq-prijs{{font-size:1.5rem;font-weight:800;color:var(--ink);letter-spacing:-.02em;margin:6px 0 2px}}
.bl-dq-body p{{font-size:.92rem;margin:0 0 10px}}
.bl-dq-links{{display:flex;flex-wrap:wrap;gap:6px 14px;margin:0 0 14px;padding:0;list-style:none;font-size:.9rem}}
.bl-dq-links li{{margin:0}}
.bl-dq-cta{{display:flex;flex-wrap:wrap;gap:10px}}
.bl-dq-bron{{font-size:.78rem;color:var(--muted);margin:12px 0 0!important}}
@media (max-width:900px){{.bl-dq-grid{{grid-template-columns:1fr}}.bl-dq-uit{{position:static;min-height:0}}}}
@media (prefers-reduced-motion:reduce){{.bl-dq-optie span,.bl-dq-voortgang i,.bl-dq-beeld img{{transition:none}}}}
</style>
<div class="wrap">
  <div class="center" style="max-width:640px;margin:0 auto 34px" data-bl-rv>
    <span class="badge">In 3 vragen</span>
    <h2 id="bl-dq-kop">Hoe ziet jouw droombadkamer eruit?</h2>
    <p class="lead">Kies je ruimte, je sfeer en je budget. Je ziet meteen een stijl die past, wat zo'n badkamer ongeveer kost en waar je verder kunt kijken.</p>
  </div>
  <div class="bl-dq-grid" data-bl-dq>
    <form class="bl-dq-vragen" onsubmit="return false">{vragen}</form>
    <div class="bl-dq-uit" aria-live="polite">
      <div class="bl-dq-beeld"><img data-bl-dq-img class="bl-dq-wacht" src="/assets/fotos/renders/{RENDERS["home"]["naam"]}-800.webp" alt="" width="1600" height="1067" loading="lazy" decoding="async"><span class="bl-dq-ill">Illustratie (3D-render)</span>
        <div class="bl-dq-leeg" data-bl-dq-leeg>Beantwoord de drie vragen.<br>Je uitslag verschijnt hier.</div></div>
      <div class="bl-dq-body">
        <div class="bl-dq-voortgang" aria-hidden="true"><i data-bl-dq-bar></i></div>
        <div data-bl-dq-tekst>
          <h3>Jouw uitslag</h3>
          <p>Nog <span data-bl-dq-rest>3</span> vragen te gaan. Liever meteen een prijs op maat? Gebruik de <a href="/tools/badkamercalculator/">badkamercalculator</a>.</p>
        </div>
        <p class="bl-dq-bron">Prijsindicatie: complete badkamer, inclusief sloopwerk, tegels, sanitair, montage en 21% btw. Richtprijzen uit {bronnen} (geraadpleegd november 2026), dezelfde als op de <a href="/kosten/nieuwe-badkamer/">kostenpagina</a>. Een echte prijs hoor je pas na een bezoek van een specialist.</p>
      </div>
    </div>
  </div>
</div>
<script>
(function () {{
  var D = {json.dumps(data, ensure_ascii=False)};
  var box = document.querySelector("[data-bl-dq]");
  if (!box) return;
  var q = function (s) {{ return box.querySelector(s); }};
  var img = q("[data-bl-dq-img]"), ill = q(".bl-dq-ill"), leeg = q("[data-bl-dq-leeg]"), bar = q("[data-bl-dq-bar]"), tekst = q("[data-bl-dq-tekst]");
  var e = function (s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"}}[c]; }}); }};
  function keuze(n) {{ var i = box.querySelector('input[name="bl-dq-' + n + '"]:checked'); return i ? i.value : ""; }}
  function teken() {{
    var r = keuze("ruimte"), s = keuze("stijl"), n = keuze("niveau");
    var klaar = [r, s, n].filter(Boolean).length;
    bar.style.width = (klaar / 3 * 100) + "%";
    if (s && D.stijl[s].img) {{
      if (img.getAttribute("src") !== D.stijl[s].img) {{ img.src = D.stijl[s].img; img.alt = "Illustratie van een " + D.stijl[s].t.toLowerCase(); }}
      img.classList.remove("bl-dq-wacht"); leeg.hidden = true;
    }}
    if (klaar < 3) {{
      var rest = q("[data-bl-dq-rest]");
      if (rest) rest.textContent = 3 - klaar;
      return;
    }}
    var st = D.stijl[s], nv = D.niveau[n];
    /* hrefs voluit in de a-tag, zodat prefix.py er het voorvoegsel voor zet */
    var kosten = r === "klein" ? '<a href="/kosten/kleine-badkamer/">Kosten kleine badkamer</a>' : n === "luxe" ? '<a href="/kosten/luxe-badkamer/">Kosten luxe badkamer</a>' : '<a href="/kosten/nieuwe-badkamer/">Kosten nieuwe badkamer</a>';
    tekst.innerHTML = "<h3>Past bij jou: " + e(st.t) + "</h3>" +
      '<div class="bl-dq-prijs">' + e(nv.p) + "</div>" +
      "<p>Richtprijs voor niveau " + e(nv.n.toLowerCase()) + ". " + e(D.ruimte[r]) + "</p>" +
      '<ul class="bl-dq-links"><li><a href="/inspiratie/' + st.s + '/">Bekijk de ' + e(st.t.toLowerCase()) + "</a></li>" +
      '<li><a href="/materialen/' + st.m + '/">Over ' + e(st.mn) + "</a></li>" +
      "<li>" + kosten + "</li>" +
      (r === "klein" ? '<li><a href="/kennisbank/kleine-badkamer-indelen/">Kleine badkamer indelen</a></li>' : "") +
      '<li><a href="/tools/badkamercalculator/">Reken het precies uit</a></li></ul>' +
      '<div class="bl-dq-cta"><a class="btn btn-primary" href="/offerte-aanvragen/">Vraag 3 offertes aan</a><a class="btn btn-ghost" href="/tools/offertechecker/">Check je offerte</a></div>';
  }}
  box.addEventListener("change", teken);
  teken();
}})();
</script>
</section>"""


# ===========================================================================
# 5. Ontdek: alles wat de site biedt
# ===========================================================================

def _sublinks(sub):
    return "".join(f'<li><a href="{u}">{_esc(n)}</a></li>' for u, n in sub)


def sectie_ontdek():
    """Visueel overzicht van inspiratie, materialen, kosten, voor wie, tools en verloop (nieuwe URL's uit ronde 3)."""
    japandi = RENDERS_STIJL.get("japandi-badkamer")
    insp_beeld = (f'<span class="bl-on-foto">{_img(japandi["naam"], japandi["alt"], "(max-width: 600px) 90vw, 360px")}'
                  f'<span class="bl-on-ill">Illustratie (3D-render)</span></span>') if japandi else ""
    stalen = ('<span class="bl-on-stalen" aria-hidden="true"><i class="bl-st-tegel"></i><i class="bl-st-steen"></i>'
              '<i class="bl-st-micro"></i><i class="bl-st-terrazzo"></i><i class="bl-st-messing"></i></span>')
    balken = ('<span class="bl-on-balken" aria-hidden="true"><i style="--w:38%"></i><i style="--w:64%"></i>'
              '<i style="--w:82%"></i><i style="--w:52%"></i></span>')
    tijdlijn = ('<span class="bl-on-tijd" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>')
    tegels = [
        ("Inspiratie", "/inspiratie/", "Stijlen in beeld, van modern tot wellness, en voor en na.", insp_beeld, "groot",
         [("/inspiratie/japandi-badkamer/", "Japandi"), ("/inspiratie/wellness-badkamer/", "Wellness"), ("/inspiratie/voor-en-na/", "Voor en na")]),
        ("Materialen", "/materialen/", "Tegels, natuursteen, microcement en terrazzo: wat past waar?", stalen, "",
         [("/materialen/microcement/", "Microcement"), ("/materialen/voegen-en-kit/", "Voegen en kit")]),
        ("Kosten", "/kosten/", "Richtprijzen met bron, per klus en per onderdeel.", balken, "",
         [("/kosten/nieuwe-badkamer/", "Nieuwe badkamer"), ("/kosten/kleine-badkamer/", "Kleine badkamer")]),
        ("Voor wie", "/badkamer-voor/", "Wat telt voor gezinnen, ouderen, starters en verhuurders.",
         f'<span class="bl-on-ic">{icon("users", 30)}{icon("house", 30)}</span>', "",
         [("/badkamer-voor/gezinnen/", "Gezinnen"), ("/badkamer-voor/ouderen/", "Ouderen")]),
        ("Tools", "/tools/", "Calculator, indelingsplanner, stijlkiezer en offertechecker.",
         f'<span class="bl-on-ic">{icon("form", 30)}{icon("euro", 30)}</span>', "",
         [("/tools/indelingsplanner/", "Indelingsplanner"), ("/tools/offertechecker/", "Offertechecker")]),
        ("Zo verloopt het", "/zo-verloopt-je-verbouwing/", "Van eerste idee tot oplevering: elke stap en hoe lang die duurt.", tijdlijn, "breed",
         [("/kennisbank/volgorde-badkamerrenovatie/", "Volgorde van het werk"), ("/tools/renovatieplanner/", "Renovatieplanner")]),
    ]
    kaarten = "".join(
        f'<article class="bl-on-tegel bl-kaart {("bl-on-" + k) if k else ""}">'
        f'<a class="bl-on-hoofd" href="{href}"><span class="bl-on-vis">{vis}</span>'
        f'<span class="bl-on-t"><strong>{_esc(t)} <span aria-hidden="true">→</span></strong><span>{_esc(d)}</span></span></a>'
        f'<ul class="bl-on-sub">{_sublinks(sub)}</ul></article>'
        for t, href, d, vis, k, sub in tegels)
    return f"""<section class="section bl-on" aria-labelledby="bl-on-kop">
<style>
.bl-on-grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}}
.bl-on-tegel{{background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden;display:flex;flex-direction:column;position:relative}}
.bl-on-groot{{grid-row:span 2}}
.bl-on-breed{{grid-column:1/-1}}
.bl-on-breed .bl-on-hoofd{{flex-direction:row;align-items:center}}
.bl-on-breed .bl-on-vis{{flex:0 0 45%;align-self:stretch}}
.bl-on-breed .bl-on-t{{padding-bottom:56px;justify-content:center}}
.bl-on-breed .bl-on-sub{{position:absolute;left:45%;bottom:14px}}
.bl-on-hoofd{{text-decoration:none;display:flex;flex-direction:column;color:var(--body);flex:1}}
.bl-on-hoofd:hover{{text-decoration:none}}
.bl-on-hoofd::after{{content:"";position:absolute;inset:0;z-index:0}}
.bl-on-vis{{display:flex;align-items:center;justify-content:center;min-height:110px;background:linear-gradient(135deg,#eef5f6,#f9fbfb);padding:18px}}
.bl-on-groot .bl-on-vis{{padding:0;flex:1;min-height:220px;position:relative}}
.bl-on-foto{{position:absolute;inset:0;overflow:hidden}}
.bl-on-foto img{{width:100%;height:100%;object-fit:cover}}
.bl-on-ill{{position:absolute;left:10px;bottom:10px;background:rgba(255,255,255,.9);color:#334;font-size:.7rem;padding:3px 8px;border-radius:99px}}
.bl-on-t{{display:flex;flex-direction:column;gap:3px;padding:16px 18px 6px}}
.bl-on-t strong{{color:var(--ink);font-size:1.12rem}}
.bl-on-t strong span{{color:var(--accent-dark);display:inline-block;transition:transform .25s}}
.bl-on-tegel:hover .bl-on-t strong span{{transform:translateX(4px)}}
.bl-on-t > span{{font-size:.92rem;line-height:1.5}}
.bl-on-sub{{list-style:none;margin:0;padding:6px 18px 16px;display:flex;flex-wrap:wrap;gap:6px;position:relative;z-index:1}}
.bl-on-sub li{{margin:0}}
.bl-on-sub a{{display:inline-block;font-size:.82rem;font-weight:600;color:var(--navy);background:var(--bg-soft);border-radius:99px;padding:4px 11px;text-decoration:none}}
.bl-on-sub a:hover{{background:#e1eef0}}
.bl-on-stalen{{display:flex;gap:10px}}
.bl-on-stalen i{{width:44px;height:44px;border-radius:12px;box-shadow:0 4px 10px rgba(11,74,86,.15),inset 0 0 0 1px rgba(0,0,0,.05);transition:transform .3s cubic-bezier(.34,1.56,.64,1)}}
.bl-on-tegel:hover .bl-on-stalen i:nth-child(odd){{transform:translateY(-5px) rotate(-4deg)}}
.bl-on-tegel:hover .bl-on-stalen i:nth-child(even){{transform:translateY(-3px) rotate(4deg)}}
.bl-st-tegel{{background:linear-gradient(#fff 2px,transparent 2px) 0 0/50% 50%,linear-gradient(90deg,#fff 2px,#8fb8b0 2px) 0 0/50% 50%}}
.bl-st-steen{{background:linear-gradient(125deg,#f4f1ec 0 30%,#d9d3ca 31%,#f4f1ec 34% 62%,#cfc8bd 63%,#efebe5 66%)}}
.bl-st-micro{{background:radial-gradient(circle at 30% 30%,#b7b2aa,#8f8a83)}}
.bl-st-terrazzo{{background:radial-gradient(circle at 20% 30%,#c4511f 0 3px,transparent 4px),radial-gradient(circle at 70% 60%,#0b4a56 0 3px,transparent 4px),radial-gradient(circle at 45% 80%,#9a8f80 0 2px,transparent 3px),radial-gradient(circle at 80% 20%,#d9a88c 0 2px,transparent 3px),#efe9e1}}
.bl-st-messing{{background:linear-gradient(135deg,#e9c77b,#b08433 60%,#e2c07a)}}
.bl-on-balken{{display:flex;flex-direction:column;gap:7px;width:100%;max-width:220px}}
.bl-on-balken i{{display:block;height:10px;border-radius:99px;background:linear-gradient(90deg,var(--navy-500),#5f9aa4);width:var(--w);transition:width .5s cubic-bezier(.2,.7,.2,1)}}
.bl-on-balken i:nth-child(3){{background:linear-gradient(90deg,var(--accent),#e08a62)}}
.bl-on-tegel:hover .bl-on-balken i{{width:calc(var(--w) + 10%)}}
.bl-on-ic{{display:flex;gap:12px;color:var(--accent-dark)}}
.bl-on-ic svg{{background:#fff;border-radius:14px;padding:10px;width:54px;height:54px;box-shadow:0 4px 12px rgba(11,74,86,.1)}}
.bl-on-tijd{{display:flex;align-items:center;width:100%;max-width:420px;position:relative}}
.bl-on-tijd::before{{content:"";position:absolute;left:8px;right:8px;top:50%;height:3px;background:linear-gradient(90deg,var(--navy-500),var(--accent));border-radius:3px}}
.bl-on-tijd i{{position:relative;flex:1;display:flex;justify-content:center}}
.bl-on-tijd i::before{{content:"";width:16px;height:16px;border-radius:50%;background:#fff;border:3px solid var(--navy-500);transition:transform .3s}}
.bl-on-tijd i:last-child::before{{border-color:var(--accent);background:var(--accent)}}
.bl-on-tegel:hover .bl-on-tijd i::before{{transform:scale(1.2)}}
@media (max-width:900px){{.bl-on-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.bl-on-groot{{grid-row:auto;grid-column:span 2}}.bl-on-breed{{grid-column:span 2}}}}
@media (max-width:600px){{.bl-on-grid{{grid-template-columns:1fr}}.bl-on-groot,.bl-on-breed{{grid-column:auto}}.bl-on-groot .bl-on-vis{{min-height:0;aspect-ratio:3/2;flex:none}}}}
@media (max-width:600px){{
  .bl-on-tegel:not(.bl-on-groot) .bl-on-hoofd{{flex-direction:row;align-items:stretch}}
  .bl-on-tegel:not(.bl-on-groot) .bl-on-vis{{flex:0 0 92px;min-height:0;padding:10px;align-self:stretch}}
  .bl-on-tegel:not(.bl-on-groot) .bl-on-t{{padding:14px 14px 4px}}
  .bl-on-tegel:not(.bl-on-groot) .bl-on-sub{{padding:4px 14px 14px 106px}}
  .bl-on-breed .bl-on-t{{padding-bottom:4px}}.bl-on-breed .bl-on-sub{{position:relative;left:auto;bottom:auto}}
  .bl-on-stalen{{display:grid;grid-template-columns:repeat(2,26px);gap:6px}}
  .bl-on-stalen i{{width:26px;height:26px;border-radius:7px}}.bl-on-stalen i:nth-child(5){{display:none}}
  .bl-on-balken i{{height:7px}}
  .bl-on-ic{{flex-direction:column;gap:6px}}.bl-on-ic svg{{width:36px;height:36px;padding:7px;border-radius:10px}}
  .bl-on-tijd{{flex-direction:column;height:80px}}.bl-on-tijd::before{{left:50%;right:auto;top:6px;bottom:6px;width:3px;height:auto;transform:translateX(-50%)}}
  .bl-on-tijd i::before{{width:11px;height:11px;border-width:2px}}
}}
@media (prefers-reduced-motion:reduce){{.bl-on-tegel *{{transition:none!important}}}}
</style>
<div class="wrap">
  <div class="center" style="max-width:640px;margin:0 auto 34px" data-bl-rv>
    <span class="badge">Ontdek</span>
    <h2 id="bl-on-kop">Alles voor je nieuwe badkamer op één plek</h2>
    <p class="lead">Van een eerste idee tot een offerte die je begrijpt. Kies waar je wilt beginnen.</p>
  </div>
  <div class="bl-on-grid" data-bl-groep>{kaarten}</div>
</div>
</section>"""


# ===========================================================================
# 6. Cijfers: alleen controleerbare feiten met bron
# ===========================================================================

def sectie_cijfers(kosten_links=None):
    """Echte, natelbare feiten over de site zelf. Geen klant-, review- of monteuraantallen.

    kosten_links: optioneel de volledige lijst LINKS van alle kostenmodules (index meegeteld of niet:
    alles op /kosten/<slug>/ telt). Zonder argument telt hij badkamer_kosten.LINKS."""
    import richtprijzen as RP
    feiten = []
    try:
        from producten_badkamer import PRODUCTDATA as PD
        feiten.append((len(PD["artikelen"]), "producten met een marktprijs",
                       "Kranen, toiletten, douchegoten en meer in de offertechecker.",
                       ("/tools/offertechecker/", "Telling in de productdata van de offertechecker")))
        feiten.append((len(PD["categorieen"]), "soorten producten",
                       "Van thermostaatkraan tot inbouwreservoir.",
                       ("/tools/offertechecker/", "Telling in de productdata")))
    except Exception:
        pass
    n_post = len(RP.RICHTPRIJZEN)
    n_bron = len([b for b in RP.BRONNEN if b != "eigen"])
    feiten.append((n_post, "posten met een richtprijs", "Sloopwerk, tegelwerk, leidingwerk, montage, elektra en meer.",
                   ("/prijzen/", "Telling in de richtprijzen van de site")))
    feiten.append((n_bron, "openbare prijsbronnen", "Elke richtprijs heeft een bron die je zelf kunt nalezen.",
                   ("/kosten/", "De bronnen staan op elke kostenpagina")))
    if kosten_links is None:
        try:
            from badkamer_kosten import LINKS as kosten_links
        except Exception:
            kosten_links = []
    n_kost = len({p for p, *_ in kosten_links if p.startswith("/kosten/") and p != "/kosten/"})
    if n_kost:
        feiten.append((n_kost, "kostenpagina's", "Per klus: wat het kost, waar de prijs van afhangt en waar je op let.",
                       ("/kosten/", "Telling van de pagina's onder /kosten/")))
    blokken = "".join(
        f'<div class="bl-cf-feit"><span class="bl-cf-n">{n}</span><strong>{_esc(t)}</strong><p>{_esc(u)}</p>'
        f'<a href="{h}">{_esc(b)} →</a></div>' for n, t, u, (h, b) in feiten)
    peil = _peildatum()
    return f"""<section class="section dark bl-cf" aria-labelledby="bl-cf-kop">
<style>
.bl-cf{{position:relative;overflow:hidden}}
.bl-cf::before{{content:"";position:absolute;inset:0;opacity:.07;pointer-events:none;
  background:linear-gradient(#fff 1px,transparent 1px) 0 0/40px 40px,linear-gradient(90deg,#fff 1px,transparent 1px) 0 0/40px 40px}}
.bl-cf .wrap{{position:relative}}
.bl-cf-kop{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:30px}}
.bl-cf-kop p{{margin:0;max-width:52ch;color:#b8cadd}}
.bl-cf-peil{{display:inline-flex;gap:8px;align-items:center;border:1px solid rgba(255,255,255,.25);border-radius:99px;padding:6px 14px;color:#fff;font-weight:600;font-size:.9rem}}
.bl-cf-peil i{{width:8px;height:8px;border-radius:50%;background:#5fd39b;box-shadow:0 0 0 4px rgba(95,211,155,.2)}}
.bl-cf-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px}}
@media (max-width:600px){{.bl-cf-feit{{padding:16px 14px}}.bl-cf-feit p{{display:none}}}}
.bl-cf-feit{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:16px;padding:20px;transition:background .25s,transform .25s}}
.bl-cf-feit:hover{{background:rgba(255,255,255,.1);transform:translateY(-3px)}}
.bl-cf-n{{display:block;font-size:clamp(2.2rem,4vw,3rem);font-weight:800;line-height:1;color:#fff;letter-spacing:-.03em;margin-bottom:8px}}
.bl-cf-feit strong{{display:block;color:#fff;margin-bottom:4px}}
.bl-cf-feit p{{font-size:.88rem;margin:0 0 10px;color:#b8cadd}}
.bl-cf-feit a{{font-size:.8rem;color:#f4c7b5}}
@media (prefers-reduced-motion:reduce){{.bl-cf-feit{{transition:none}}.bl-cf-feit:hover{{transform:none}}}}
</style>
<div class="wrap">
  <div class="bl-cf-kop" data-bl-rv>
    <div><span class="badge badge-dark">Waar de cijfers vandaan komen</span>
    <h2 id="bl-cf-kop">Prijzen die je kunt nalezen</h2>
    <p>De offertechecker en de kostenpagina's rekenen met dezelfde data. Dit zit erin.</p></div>
    <span class="bl-cf-peil"><i aria-hidden="true"></i>Peildatum {peil}</span>
  </div>
  <div class="bl-cf-grid" data-bl-groep>{blokken}</div>
</div>
</section>"""


if __name__ == "__main__":
    for naam in ("hero_visual", "sectie_stijlen", "sectie_droombadkamer", "sectie_ontdek", "sectie_cijfers"):
        print(f"{naam:22} {len(globals()[naam]()):>6} tekens")
    print(f"BELEVING_CSS {len(BELEVING_CSS.encode())} bytes, BELEVING_JS {len(BELEVING_JS.encode())} bytes")
