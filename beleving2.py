# -*- coding: utf-8 -*-
"""Beleving 2 (ronde 4, agent H): nieuwe bovenkant van de homepage.

Geen eigen pagina's. Drie html-blokken voor build_home() in build.py, elk met eigen inline
<style> (voorvoegsel .h2-) en waar nodig een klein inline <script>:

- hero()          -> grote hero in de volle breedte met de beste render, Ken Burns-beweging,
                     kop, twee knoppen, drie USP's en een voorbeelduitslag (alleen desktop).
- zo_werkt_het()  -> strook "Zo werkt het" in 3 stappen, elk met een kleine geanimeerde illustratie.
- inspiratie()    -> mozaïekgalerij "Laat je inspireren" met links naar de stijlpagina's.

Alle bewegingen staan uit bij prefers-reduced-motion. Zonder JavaScript staat alles in de eindstand.
Alle renders zijn eigen 3D-illustraties en staan er met "Illustratie (3D-render)" bij.
"""

import html as _h
import os

from components import icon, eur

_ROOT = os.path.dirname(os.path.abspath(__file__))
_RMAP = os.path.join(_ROOT, "fotos", "renders")

# Hero-beeld: eerste die bestaat. De wellness-render heeft een donkere linkerkant (goed leesbare tekst)
# en een warm verlichte houten wand rechts.
HERO_KANDIDATEN = [
    ("b4-wellness-badkamer-1",
     "Illustratie van een wellness-badkamer met grote donkere tegels, een inloopdouche met glazen wand en zitbank, "
     "een warm verlichte wand van houten lamellen, een zwevend meubel met opzetkom en een ronde spiegel met licht"),
    ("bd-badkamer-renoveren",
     "Illustratie van een gerenoveerde badkamer in warme tinten met vrijstaand bad, dubbel notenhouten badmeubel en een gouden regendouche"),
    ("bd-home",
     "Illustratie van een lichte, moderne badkamer met inloopdouche, groene wandtegels, zwevend eiken badmeubel en hangtoilet"),
]


def _esc(s):
    return _h.escape(str(s), quote=True)


def _bestaat(naam):
    return os.path.exists(os.path.join(_RMAP, f"{naam}-800.webp")) and \
        os.path.exists(os.path.join(_RMAP, f"{naam}-1600.webp"))


def _srcset(naam, met_400=False):
    delen = []
    if met_400 and os.path.exists(os.path.join(_RMAP, f"{naam}-400.webp")):
        delen.append(f"/assets/fotos/renders/{naam}-400.webp 400w")
    delen += [f"/assets/fotos/renders/{naam}-800.webp 800w", f"/assets/fotos/renders/{naam}-1600.webp 1600w"]
    return ", ".join(delen)


def _peildatum():
    try:
        import beleving
        return beleving._peildatum()
    except Exception:
        return "november 2026"


# ===========================================================================
# 1. Hero
# ===========================================================================

_HERO_CSS = """<style>
.h2-hero{position:relative;overflow:hidden;background:#071f25;color:#d5e3e6;isolation:isolate}
.h2-beeld{position:absolute;inset:0;z-index:-2;margin:0;overflow:hidden;background:#2b2a28}
.h2-beeld img{width:100%;height:100%;object-fit:cover;object-position:68% 50%;display:block;
  transform-origin:72% 45%;animation:h2-kb 30s ease-in-out infinite alternate;will-change:transform}
@keyframes h2-kb{from{transform:scale(1)}to{transform:scale(1.09) translate(-1.2%,-.8%)}}
.h2-hero::before{content:"";position:absolute;inset:0;z-index:-1;pointer-events:none;
  background:linear-gradient(90deg,rgba(5,27,32,.94) 0%,rgba(5,27,32,.86) 30%,rgba(5,27,32,.45) 55%,rgba(5,27,32,.05) 78%),
             linear-gradient(0deg,rgba(5,27,32,.55) 0%,rgba(5,27,32,0) 35%)}
.h2-in{position:relative;display:grid;grid-template-columns:minmax(0,600px) 1fr;align-items:center;gap:40px;
  min-height:clamp(560px,calc(100vh - 140px),700px);padding-top:64px;padding-bottom:84px}
.h2-oog{display:inline-flex;align-items:center;gap:10px;font-size:.8rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#f3b89b;margin:0 0 18px}
.h2-oog::before{content:"";width:28px;height:2px;background:#c4511f;border-radius:2px}
.h2-hero h1{color:#fff;font-size:clamp(2.1rem,1.2rem + 3.4vw,3.7rem);line-height:1.06;letter-spacing:-.025em;margin:0 0 20px;font-weight:800;text-wrap:balance}
.h2-hero h1 em{font-style:normal;color:#f3b89b;background:linear-gradient(transparent 82%,rgba(196,81,31,.55) 82%,rgba(196,81,31,.55) 94%,transparent 94%)}
.h2-lead{font-size:clamp(1.05rem,1rem + .3vw,1.2rem);line-height:1.6;color:#d5e3e6;margin:0 0 30px;max-width:54ch}
.h2-knoppen{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 34px}
.h2-knop{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:54px;padding:14px 28px;border-radius:999px;
  font-weight:700;font-size:1.04rem;text-decoration:none;line-height:1.2;transition:transform .18s cubic-bezier(.2,.7,.2,1),box-shadow .18s,background .18s}
.h2-knop svg{flex:0 0 auto}
.h2-knop-1{background:linear-gradient(180deg,#d05a26,#b8481a);color:#fff;box-shadow:0 14px 30px -10px rgba(196,81,31,.65)}
.h2-knop-1:hover{background:#d25b26;transform:translateY(-2px);color:#fff}
.h2-knop-2{background:rgba(255,255,255,.08);color:#fff;border:1.5px solid rgba(255,255,255,.55);backdrop-filter:blur(6px)}
.h2-knop-2:hover{background:#fff;color:#082f37;transform:translateY(-2px)}
.h2-knop:focus-visible{outline:3px solid #f3b89b;outline-offset:3px}
.h2-knop .h2-pijl{transition:transform .18s}
.h2-knop:hover .h2-pijl{transform:translateX(3px)}
.h2-usps{list-style:none;margin:0;padding:22px 0 0;border-top:1px solid rgba(255,255,255,.16);display:grid;grid-template-columns:repeat(3,auto);gap:12px 26px;justify-content:start}
.h2-usps li{display:flex;align-items:center;gap:9px;margin:0;font-size:.93rem;color:#e7f0f1;font-weight:600;line-height:1.3}
.h2-usps i{flex:0 0 auto;width:26px;height:26px;border-radius:50%;display:grid;place-items:center;background:rgba(15,138,95,.22);color:#7fe0b4;font-style:normal}
.h2-ill{position:absolute;right:14px;bottom:12px;z-index:2;background:rgba(255,255,255,.88);color:#334;font-size:.72rem;padding:3px 9px;border-radius:99px;margin:0}
/* voorbeelduitslag (alleen brede schermen) */
.h2-kaart{justify-self:end;align-self:end;width:300px;margin-bottom:6px;background:rgba(255,255,255,.95);color:#3f5459;border-radius:16px;padding:14px 16px 10px;
  box-shadow:0 2px 6px rgba(0,0,0,.12),0 30px 60px -10px rgba(0,0,0,.45);font-size:.84rem;backdrop-filter:blur(10px);animation:h2-zweef 7s ease-in-out infinite}
.h2-kaart-kop{display:flex;justify-content:space-between;align-items:center;font-weight:800;color:#0b4a56;margin-bottom:4px}
.h2-kaart-kop span+span{font-size:.64rem;text-transform:uppercase;letter-spacing:.07em;background:#eef3f4;color:#55696e;border-radius:99px;padding:3px 9px;font-weight:700}
.h2-kaart ul{list-style:none;margin:0;padding:0}
.h2-kaart li{border-top:1px solid #edf2f3;padding:7px 0;margin:0}
.h2-kaart li:first-child{border-top:0}
.h2-soort{display:block;font-size:.64rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:#6a7d81}
.h2-r{display:flex;justify-content:space-between;gap:8px;align-items:center}
.h2-r strong{color:#082f37;font-size:.9rem}
.h2-kaart small{color:#55696e;font-size:.74rem}
.h2-tag{font-size:.7rem;font-weight:700;border-radius:99px;padding:2px 8px;white-space:nowrap}
.h2-binnen{background:#e3f4ea;color:#1d6b3e}.h2-boven{background:#fdecdf;color:#9a3d12}.h2-vaag{background:#fff4d6;color:#7a5800}
.h2-kaart-noot{margin:4px 0 0;font-size:.7rem;color:#6a7d81;border-top:1px solid #edf2f3;padding-top:6px}
@keyframes h2-zweef{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
@media (max-width:1080px){.h2-in{grid-template-columns:1fr}.h2-kaart{display:none}}
@media (max-width:900px){.h2-usps{grid-template-columns:1fr;gap:10px}}
/* mobiel: beeld boven, tekst eronder op petrol */
@media (max-width:760px){
  .h2-hero{background:#071f25}
  .h2-hero::before{display:none}
  .h2-beeld{position:relative;inset:auto;z-index:0;aspect-ratio:4/3}
  .h2-beeld::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,#071f25 0%,rgba(7,31,37,0) 38%)}
  .h2-beeld img{object-position:62% 50%}
  .h2-ill{top:10px;left:10px;right:auto;bottom:auto}
  .h2-in{min-height:0;padding-top:0;padding-bottom:44px;margin-top:-34px}
  .h2-hero h1{font-size:clamp(1.95rem,7.6vw,2.4rem)}
  .h2-lead{margin-bottom:24px}
  .h2-knoppen{flex-direction:column}
  .h2-knop{width:100%}
}
@media (prefers-reduced-motion:reduce){
  .h2-beeld img,.h2-kaart{animation:none}
  .h2-knop,.h2-knop .h2-pijl{transition:none}
}
</style>"""


def _voorbeeldkaart():
    """Kleine voorbeelduitslag: verzonnen offerte, echte prijsbanden uit de data."""
    try:
        import richtprijzen as RP
        tg = RP.RICHTPRIJZEN["tegelwerk"]
    except Exception:
        return ""
    rij_p = ""
    try:
        from producten_badkamer import PRODUCTDATA
        product = next((a for a in PRODUCTDATA["artikelen"] if "34558000" in a.get("codes", [])), None) \
            or next((a for a in PRODUCTDATA["artikelen"] if a.get("categorie") == "thermostaatkraan"), None)
    except Exception:
        product = None
    if product:
        op_offerte = 200  # verzonnen offertebedrag incl. btw, alleen voor dit voorbeeld
        pct = round((op_offerte - product["tot"]) / product["tot"] * 100)
        tag = (f'<span class="h2-tag h2-boven">{pct}% boven</span>' if pct > 0
               else '<span class="h2-tag h2-binnen">binnen de band</span>')
        rij_p = (f'<li><span class="h2-soort">Product · thermostaatkraan</span><div class="h2-r"><strong>{eur(op_offerte)}</strong>{tag}</div>'
                 f'<small>Marktband {eur(product["van"])} – {eur(product["tot"])} incl. btw</small></li>')
    return f"""<aside class="h2-kaart" aria-label="Voorbeeld van een uitslag per regel">
      <div class="h2-kaart-kop"><span>Uitslag per regel</span><span>Voorbeeld</span></div>
      <ul>
        {rij_p}
        <li><span class="h2-soort">Arbeid · tegelwerk 28 m²</span><div class="h2-r"><strong>€ 40 per m²</strong><span class="h2-tag h2-binnen">binnen de richtprijs</span></div>
          <small>Richtprijs {eur(tg['laag'])} – {eur(tg['hoog'])} per m² incl. btw</small></li>
        <li><span class="h2-soort">Materiaal</span><div class="h2-r"><strong>Sanitair compleet</strong><span class="h2-tag h2-vaag">te vaag</span></div></li>
      </ul>
      <p class="h2-kaart-noot">Verzonnen offerte, echte prijsbanden ({_peildatum()}).</p>
    </aside>"""


def hero():
    """Hero in de volle breedte. Het beeld is het LCP-element: eager, fetchpriority=high,
    srcset 800/1600 en vaste afmetingen (1600x1067). Desktop: beeld als achtergrond met verloop;
    mobiel: beeld (4:3) boven de tekst."""
    naam, alt = next(((n, a) for n, a in HERO_KANDIDATEN if _bestaat(n)), (None, None))
    beeld = ""
    if naam:
        beeld = (f'<figure class="h2-beeld"><img src="/assets/fotos/renders/{naam}-800.webp" '
                 f'srcset="{_srcset(naam)}" sizes="100vw" width="1600" height="1067" alt="{_esc(alt)}" '
                 f'loading="eager" fetchpriority="high" decoding="async">'
                 f'<figcaption class="h2-ill">Illustratie (3D-render)</figcaption></figure>')
    return f"""{_HERO_CSS}<section class="h2-hero" aria-labelledby="h2-kop">
  {beeld}
  <div class="wrap h2-in">
    <div class="h2-tekst">
      <p class="h2-oog">Badkamerofferte checken en vergelijken</p>
      <h1 id="h2-kop">Weet of je badkamer&shy;offerte <em>klopt</em></h1>
      <p class="h2-lead">Check je offerte gratis per regel: per product, per m² en per uur zie je hoe je prijs zich verhoudt tot de markt. Nog geen offerte? Vraag er gratis tot 3 aan bij badkamerspecialisten uit je regio.</p>
      <div class="h2-knoppen">
        <a class="h2-knop h2-knop-1" href="/tools/offertechecker/">{icon('form', 20)}<span>Check je offerte</span><span class="h2-pijl" aria-hidden="true">→</span></a>
        <a class="h2-knop h2-knop-2" href="/offerte-aanvragen/">{icon('users', 20)}<span>Offertes aanvragen</span></a>
      </div>
      <ul class="h2-usps">
        <li><i>{icon('euro', 14)}</i>Gratis voor jou</li>
        <li><i>{icon('shield', 14)}</i>Je offerte blijft in je browser</li>
        <li><i>{icon('users', 14)}</i>Tot 3 offertes van specialisten uit je regio</li>
      </ul>
    </div>
    {_voorbeeldkaart()}
  </div>
</section>"""


# ===========================================================================
# 2. Zo werkt het (3 stappen met kleine animaties)
# ===========================================================================

_STAP_CSS = """<style>
.h2-stappen{padding:76px 0 80px;background:#f2f8f8;position:relative}
.h2-stappen-kop{text-align:center;max-width:640px;margin:0 auto 46px}
.h2-stappen-kop .h2-oog2{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#c4511f;margin:0 0 10px}
.h2-stappen-kop h2{margin:0 0 12px}
.h2-stappen-kop p{margin:0;color:#55696e;font-size:1.08rem}
.h2-rij{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);gap:26px;counter-reset:h2s;position:relative}
.h2-rij::before{content:"";position:absolute;top:96px;left:16%;right:16%;border-top:2px dashed #b9d0d4;z-index:0}
.h2-stap{position:relative;z-index:1;margin:0;background:#fff;border:1px solid #d9e5e7;border-radius:18px;padding:22px 22px 24px;
  box-shadow:0 1px 2px rgba(11,74,86,.05),0 14px 34px -14px rgba(11,74,86,.18);counter-increment:h2s;transition:transform .2s,box-shadow .2s}
.h2-stap:hover{transform:translateY(-3px);box-shadow:0 2px 4px rgba(11,74,86,.06),0 22px 44px -14px rgba(11,74,86,.25)}
.h2-ill2{display:block;width:100%;height:auto;aspect-ratio:220/140;border-radius:12px;background:linear-gradient(160deg,#eaf3f4,#f8fbfb);margin-bottom:18px}
.h2-stap h3{display:flex;gap:10px;align-items:baseline;font-size:1.14rem;margin:0 0 8px;color:#082f37}
.h2-stap h3::before{content:counter(h2s);flex:0 0 auto;display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;
  background:#0b4a56;color:#fff;font-size:.86rem;font-weight:800;transform:translateY(-2px)}
.h2-stap p{margin:0;color:#3f5459;font-size:.97rem;line-height:1.55}
.h2-stappen-cta{text-align:center;margin:38px 0 0}
.h2-stappen-cta a{display:inline-flex;align-items:center;gap:8px;font-weight:700;color:#0b4a56;text-decoration:none;border-bottom:2px solid #c4511f;padding-bottom:2px}
.h2-stappen-cta a:hover{color:#c4511f}
/* animaties: alleen als .h2-aan gezet is (JS + in beeld). Zonder JS: eindstand. */
.h2-aan .h2-doc{animation:h2-doc 4.2s cubic-bezier(.2,.7,.2,1) infinite}
.h2-aan .h2-vink{animation:h2-vink 4.2s ease-out infinite}
.h2-aan .h2-scan{animation:h2-scan 4.2s ease-in-out infinite}
.h2-aan .h2-dot1{animation:h2-dot1 4.5s cubic-bezier(.2,.7,.2,1) infinite}
.h2-aan .h2-dot2{animation:h2-dot2 4.5s cubic-bezier(.2,.7,.2,1) infinite}
.h2-aan .h2-dot3{animation:h2-dot3 4.5s cubic-bezier(.2,.7,.2,1) infinite}
.h2-aan .h2-knopje{animation:h2-knopje 4.8s cubic-bezier(.34,1.56,.64,1) infinite}
.h2-aan .h2-baan{animation:h2-baan 4.8s ease infinite}
.h2-aan .h2-sp1{animation:h2-sp 4.8s ease infinite}
.h2-aan .h2-sp2{animation:h2-sp 4.8s ease infinite .15s}
.h2-aan .h2-sp3{animation:h2-sp 4.8s ease infinite .3s}
@keyframes h2-doc{0%{transform:translateY(-34px);opacity:0}18%{opacity:1}34%,100%{transform:translateY(0);opacity:1}}
@keyframes h2-vink{0%,38%{transform:scale(0);opacity:0}48%{transform:scale(1.15);opacity:1}56%,100%{transform:scale(1);opacity:1}}
@keyframes h2-scan{0%,40%{transform:translateY(0);opacity:0}45%{opacity:.85}80%{transform:translateY(58px);opacity:.85}88%,100%{transform:translateY(58px);opacity:0}}
@keyframes h2-dot1{0%,8%{transform:translateX(-60px)}38%,100%{transform:translateX(0)}}
@keyframes h2-dot2{0%,20%{transform:translateX(-48px)}50%,100%{transform:translateX(0)}}
@keyframes h2-dot3{0%,32%{transform:translateX(-34px)}62%,100%{transform:translateX(0)}}
@keyframes h2-knopje{0%,25%{transform:translateX(-22px)}40%,100%{transform:translateX(0)}}
@keyframes h2-baan{0%,25%{fill:#c9d6d9}40%,100%{fill:#0f8a5f}}
@keyframes h2-sp{0%,42%{opacity:.25;transform:translateY(6px)}56%,100%{opacity:1;transform:translateY(0)}}
.h2-doc,.h2-vink,.h2-scan,.h2-dot1,.h2-dot2,.h2-dot3,.h2-knopje,.h2-sp1,.h2-sp2,.h2-sp3{transform-box:fill-box;transform-origin:center}
@media (max-width:860px){.h2-rij{grid-template-columns:1fr;gap:18px;max-width:460px;margin:0 auto}.h2-rij::before{display:none}
  .h2-stappen{padding:56px 0 60px}}
@media (prefers-reduced-motion:reduce){
  .h2-aan .h2-doc,.h2-aan .h2-vink,.h2-aan .h2-scan,.h2-aan .h2-dot1,.h2-aan .h2-dot2,.h2-aan .h2-dot3,
  .h2-aan .h2-knopje,.h2-aan .h2-baan,.h2-aan .h2-sp1,.h2-aan .h2-sp2,.h2-aan .h2-sp3{animation:none}
  .h2-stap{transition:none}
}
</style>"""

# Stap 1: een offerte valt in een browservenster en wordt daar gelezen (geen wolk/server).
_SVG_UPLOAD = """<svg class="h2-ill2" viewBox="0 0 220 140" role="img" aria-label="Een offerte wordt in je browser gelezen">
  <rect x="34" y="18" width="152" height="108" rx="10" fill="#fff" stroke="#b9d0d4" stroke-width="1.5"/>
  <path d="M34 28a10 10 0 0 1 10-10h132a10 10 0 0 1 10 10v8H34z" fill="#dbe8ea"/>
  <circle cx="46" cy="27" r="2.6" fill="#c4511f"/><circle cx="55" cy="27" r="2.6" fill="#e7b04a"/><circle cx="64" cy="27" r="2.6" fill="#0f8a5f"/>
  <rect x="76" y="23" width="90" height="8" rx="4" fill="#fff"/>
  <g class="h2-doc">
    <rect x="82" y="44" width="56" height="72" rx="5" fill="#fff" stroke="#0b4a56" stroke-width="1.6"/>
    <path d="M124 44v12h14" fill="#eef3f4" stroke="#0b4a56" stroke-width="1.6" stroke-linejoin="round"/>
    <rect x="90" y="60" width="26" height="4" rx="2" fill="#0b4a56"/>
    <rect x="90" y="72" width="40" height="3" rx="1.5" fill="#b9d0d4"/><rect x="90" y="80" width="34" height="3" rx="1.5" fill="#b9d0d4"/>
    <rect x="90" y="88" width="40" height="3" rx="1.5" fill="#b9d0d4"/><rect x="90" y="96" width="28" height="3" rx="1.5" fill="#b9d0d4"/>
    <rect x="90" y="105" width="18" height="4" rx="2" fill="#c4511f"/>
  </g>
  <rect class="h2-scan" x="78" y="52" width="64" height="3" rx="1.5" fill="#c4511f" opacity="0"/>
  <g class="h2-vink"><circle cx="146" cy="104" r="13" fill="#0f8a5f"/><path d="M140 104l4.5 4.5 8-9" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>
</svg>"""

# Stap 2: per regel een marktband met een stip die op zijn plek schuift.
_SVG_REGELS = """<svg class="h2-ill2" viewBox="0 0 220 140" role="img" aria-label="Per regel zie je waar je prijs staat ten opzichte van de marktband">
  <g font-family="system-ui,-apple-system,sans-serif" font-size="9" font-weight="700" fill="#55696e">
    <text x="22" y="34">Kraan</text><text x="22" y="72">Tegelwerk</text><text x="22" y="110">Sanitair</text>
  </g>
  <rect x="82" y="26" width="116" height="10" rx="5" fill="#e3ecee"/><rect x="104" y="26" width="46" height="10" rx="5" fill="#bfe5d0"/>
  <rect x="82" y="64" width="116" height="10" rx="5" fill="#e3ecee"/><rect x="112" y="64" width="54" height="10" rx="5" fill="#bfe5d0"/>
  <rect x="82" y="102" width="116" height="10" rx="5" fill="#e3ecee"/><rect x="100" y="102" width="50" height="10" rx="5" fill="#bfe5d0" opacity=".45"/>
  <g class="h2-dot1"><circle cx="176" cy="31" r="7" fill="#c4511f" stroke="#fff" stroke-width="2"/></g>
  <g class="h2-dot2"><circle cx="138" cy="69" r="7" fill="#0f8a5f" stroke="#fff" stroke-width="2"/></g>
  <g class="h2-dot3"><circle cx="126" cy="107" r="7" fill="#e7b04a" stroke="#fff" stroke-width="2"/><text x="123.2" y="110.4" font-family="system-ui,sans-serif" font-size="9" font-weight="800" fill="#fff">?</text></g>
  <g font-family="system-ui,-apple-system,sans-serif" font-size="7.5" font-weight="700">
    <text x="160" y="50" fill="#9a3d12">boven</text><text x="126" y="88" fill="#1d6b3e">binnen</text><text x="114" y="126" fill="#7a5800">te vaag</text>
  </g>
</svg>"""

# Stap 3: een schakelaar "Tegenoffertes" gaat aan, daarna lichten maximaal 3 specialisten op.
_SVG_KIES = """<svg class="h2-ill2" viewBox="0 0 220 140" role="img" aria-label="Je kiest zelf of je tegenoffertes wilt van maximaal drie specialisten">
  <rect x="40" y="20" width="140" height="36" rx="10" fill="#fff" stroke="#b9d0d4" stroke-width="1.5"/>
  <text x="54" y="42" font-family="system-ui,-apple-system,sans-serif" font-size="10" font-weight="700" fill="#082f37">Tegenoffertes?</text>
  <rect class="h2-baan" x="134" y="29" width="36" height="18" rx="9" fill="#0f8a5f"/>
  <circle class="h2-knopje" cx="161" cy="38" r="7" fill="#fff"/>
  <g class="h2-sp1"><circle cx="70" cy="96" r="20" fill="#fff" stroke="#0b4a56" stroke-width="1.6"/><circle cx="70" cy="90" r="6" fill="#0b4a56"/><path d="M59 106c2-7 7-9 11-9s9 2 11 9" fill="#0b4a56"/></g>
  <g class="h2-sp2"><circle cx="110" cy="96" r="20" fill="#fff" stroke="#0b4a56" stroke-width="1.6"/><circle cx="110" cy="90" r="6" fill="#0b4a56"/><path d="M99 106c2-7 7-9 11-9s9 2 11 9" fill="#0b4a56"/></g>
  <g class="h2-sp3"><circle cx="150" cy="96" r="20" fill="#fff" stroke="#0b4a56" stroke-width="1.6"/><circle cx="150" cy="90" r="6" fill="#0b4a56"/><path d="M139 106c2-7 7-9 11-9s9 2 11 9" fill="#0b4a56"/></g>
  <text x="110" y="132" text-anchor="middle" font-family="system-ui,-apple-system,sans-serif" font-size="8.5" font-weight="700" fill="#55696e">maximaal 3 specialisten</text>
</svg>"""

_STAP_JS = """<script>
(function(){
  var r=document.querySelector('.h2-rij');
  if(!r||!('IntersectionObserver' in window))return;
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  new IntersectionObserver(function(es){es.forEach(function(e){r.classList.toggle('h2-aan',e.isIntersecting);});},{threshold:.25}).observe(r);
})();
</script>"""


def zo_werkt_het():
    return f"""{_STAP_CSS}<section class="h2-stappen" aria-labelledby="h2-stappen-kop">
<div class="wrap">
  <div class="h2-stappen-kop">
    <span class="h2-oog2">Zo werkt het</span>
    <h2 id="h2-stappen-kop">In drie stappen weet je waar je staat</h2>
    <p>Geen account nodig. Je offerte wordt gelezen op je eigen computer of telefoon.</p>
  </div>
  <ol class="h2-rij">
    <li class="h2-stap">{_SVG_UPLOAD}
      <h3>Upload je offerte</h3>
      <p>Kies de pdf of plak de tekst uit je mail. Hij wordt in je browser gelezen; er gaat niets naar een server.</p></li>
    <li class="h2-stap">{_SVG_REGELS}
      <h3>Zie per regel waar je staat</h3>
      <p>Elk product, elke m² en elk uur naast de marktprijs of een richtprijs met bron. Je ziet ook wat ontbreekt of te vaag is.</p></li>
    <li class="h2-stap">{_SVG_KIES}
      <h3>Kies zelf of je tegenoffertes wilt</h3>
      <p>Wil je vergelijken? Vraag gratis tot 3 offertes aan bij specialisten uit je regio. Je naam en die van je aanbieder gaan niet mee.</p></li>
  </ol>
  <p class="h2-stappen-cta"><a href="/tools/offertechecker/">Start de offertecheck <span aria-hidden="true">→</span></a></p>
</div>
</section>{_STAP_JS}"""


# ===========================================================================
# 3. Laat je inspireren (mozaïek)
# ===========================================================================

_GAL_CSS = """<style>
.h2-gal{padding:76px 0 80px}
.h2-gal-kop{display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-bottom:28px}
.h2-gal-kop h2{margin:0 0 6px}
.h2-gal-kop p{margin:0;color:#55696e;max-width:54ch}
.h2-gal-kop .h2-oog2{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:#c4511f;margin:0 0 10px}
.h2-gal-alle{font-weight:700;color:#0b4a56;text-decoration:none;border-bottom:2px solid #c4511f;padding-bottom:2px;white-space:nowrap}
.h2-gal-alle:hover{color:#c4511f}
.h2-mozaiek{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:200px;gap:14px}
.h2-mozaiek li{margin:0;position:relative}
.h2-mozaiek .h2-groot{grid-column:span 2;grid-row:span 2}
.h2-mozaiek .h2-breed{grid-column:span 2}
.h2-tegel{display:block;position:relative;height:100%;border-radius:16px;overflow:hidden;background:#dfe9ea;text-decoration:none;color:#fff;isolation:isolate}
.h2-tegel img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s cubic-bezier(.2,.7,.2,1)}
.h2-tegel::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(5,27,32,.72) 0%,rgba(5,27,32,0) 48%);z-index:1}
.h2-tegel:hover img,.h2-tegel:focus-visible img{transform:scale(1.05)}
.h2-tegel:focus-visible{outline:3px solid #c4511f;outline-offset:3px}
.h2-naam{position:absolute;left:16px;bottom:14px;right:16px;z-index:2;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:1.08rem;text-shadow:0 1px 8px rgba(0,0,0,.35)}
.h2-naam span:last-child{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,.18);backdrop-filter:blur(6px);display:grid;place-items:center;transition:background .2s,transform .2s;text-shadow:none}
.h2-tegel:hover .h2-naam span:last-child{background:#c4511f;transform:translateX(2px)}
.h2-tegel small{position:absolute;top:10px;right:10px;z-index:2;background:rgba(255,255,255,.88);color:#334;font-size:.68rem;padding:2px 8px;border-radius:99px;font-weight:500}
@media (max-width:860px){.h2-mozaiek{grid-template-columns:repeat(2,1fr);grid-auto-rows:150px;gap:10px}
  .h2-gal{padding:56px 0 60px}}
@media (max-width:480px){.h2-mozaiek{grid-auto-rows:130px}.h2-naam{font-size:.95rem;left:12px;bottom:10px;right:10px}.h2-naam span:last-child{width:26px;height:26px}}
@media (prefers-reduced-motion:reduce){.h2-tegel img,.h2-naam span:last-child{transition:none}.h2-tegel:hover img{transform:none}}
</style>"""

# (slug van de stijlpagina, naam, vorm)
_GAL_KEUZE = [
    ("luxe-badkamer", "Luxe", "h2-groot"),
    ("marmer-badkamer", "Marmer", ""),
    ("terrazzo-badkamer", "Terrazzo", ""),
    ("landelijke-badkamer", "Landelijk", "h2-breed"),
    ("zwart-wit-badkamer", "Zwart-wit", ""),
    ("japandi-badkamer", "Japandi", ""),
    ("scandinavische-badkamer", "Scandinavisch", "h2-breed"),
]


def inspiratie():
    alle = {}
    try:
        from render_stijl_data import RENDERS_STIJL
        alle.update(RENDERS_STIJL)
    except Exception:
        pass
    try:
        from render_stijl_data2 import RENDERS_STIJL2
        alle.update(RENDERS_STIJL2)
    except Exception:
        pass
    tegels = []
    for slug, naam, vorm in _GAL_KEUZE:
        r = alle.get(slug)
        if not r or not _bestaat(r["naam"]):
            continue
        sizes = "(max-width: 860px) 100vw, 580px" if vorm == "h2-groot" else \
                "(max-width: 860px) 50vw, 290px" if not vorm else "(max-width: 860px) 100vw, 580px"
        tegels.append(
            f'<li class="{vorm}"><a class="h2-tegel" href="/inspiratie/{slug}/">'
            f'<img src="/assets/fotos/renders/{r["naam"]}-800.webp" srcset="{_srcset(r["naam"], True)}" sizes="{sizes}" '
            f'width="1600" height="1067" alt="{_esc(r["alt"])}" loading="lazy" decoding="async">'
            f'<small>Illustratie (3D-render)</small>'
            f'<span class="h2-naam"><span>{_esc(naam)}</span><span aria-hidden="true">→</span></span></a></li>')
    if len(tegels) < 3:
        return ""
    return f"""{_GAL_CSS}<section class="h2-gal" aria-labelledby="h2-gal-kop">
<div class="wrap">
  <div class="h2-gal-kop">
    <div><span class="h2-oog2">Inspiratie</span>
      <h2 id="h2-gal-kop">Laat je inspireren</h2>
      <p>Van warm marmer tot speels terrazzo. Kies een stijl en zie welke tegels, kranen en meubels erbij passen.</p></div>
    <a class="h2-gal-alle" href="/inspiratie/">Alle badkamerstijlen →</a>
  </div>
  <ul class="h2-mozaiek">{"".join(tegels)}</ul>
</div>
</section>"""
