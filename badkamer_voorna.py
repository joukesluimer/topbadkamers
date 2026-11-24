# -*- coding: utf-8 -*-
"""Voor en na: /inspiratie/voor-en-na/ met vier interactieve voor-en-na-sliders.

Elke slider toont dezelfde ruimte twee keer, vanuit dezelfde camerahoek: eerst gedateerd (jaren 80/90),
daarna gerenoveerd. De beelden zijn eigen 3D-illustraties (renders/b5-*.html, metadata en richtprijzen
in render_voorna_data.py). Per paar: wat er veranderd is, een richtprijs met bron en een link naar de
passende kosten- of dienstpagina.

Herbruikbaar (bijvoorbeeld op de homepage):
    from badkamer_voorna import voorna_slider, VOORNA_CSS, VOORNA_JS
    from render_voorna_data import PAAR_BY_SLUG
    html = VOORNA_CSS + voorna_slider(PAAR_BY_SLUG["kleine-badkamer"], "(max-width: 860px) 100vw, 820px") + VOORNA_JS
VOORNA_CSS en VOORNA_JS zijn complete <style>- en <script>-blokken; zet ze één keer per pagina neer.
Het script werkt voor alle sliders op de pagina en doet niets zonder sliders.
"""

import datetime
import html as htmllib

from components import page, crumbs, title, faq_blok, cta_blok, cta_midden, offertecheck_blok
from data import SITE
from render_voorna_data import PAREN

PAD = "/inspiratie/voor-en-na/"
GEPUBLICEERD = "2026-11-23"

LINKS = [
    (PAD, "Badkamer voor en na", "Vier badkamers uit de jaren 80 en 90 vóór en na de renovatie, met een schuifbalk, wat er veranderd is en een richtprijs."),
]


def _esc(s):
    return htmllib.escape(str(s), quote=True)


def _eur(n):
    return f"€{int(n):,}".replace(",", ".")


# ---------------------------------------------------------------------------
# Herbruikbare slider
# ---------------------------------------------------------------------------

VOORNA_CSS = """<style>
.vno{position:relative;margin:0;aspect-ratio:3/2;width:100%;overflow:hidden;border-radius:var(--radius,14px);background:#d8d6d0;
  touch-action:pan-y;user-select:none;-webkit-user-select:none;--p:50%}
.vno img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;pointer-events:none}
.vno-voor{clip-path:inset(0 calc(100% - var(--p)) 0 0)}
.vno-lijn{position:absolute;top:0;bottom:0;left:var(--p);width:3px;margin-left:-1.5px;background:#fff;box-shadow:0 0 6px rgba(0,0,0,.35);pointer-events:none}
.vno-knop{position:absolute;top:50%;left:var(--p);width:46px;height:46px;margin:-23px 0 0 -23px;border-radius:50%;background:#fff;
  box-shadow:0 2px 10px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;pointer-events:none;color:#1d3b53}
.vno-knop svg{width:26px;height:26px}
.vno-label{position:absolute;top:12px;padding:4px 11px;border-radius:999px;font-size:.8rem;font-weight:700;letter-spacing:.02em;pointer-events:none;
  background:rgba(20,28,36,.72);color:#fff}
.vno-label-voor{left:12px}
.vno-label-na{right:12px;background:rgba(255,255,255,.92);color:#1d3b53}
.vno-range{position:absolute;inset:0;width:100%;height:100%;margin:0;opacity:0;cursor:ew-resize;touch-action:pan-y;-webkit-appearance:none;appearance:none}
.vno-range:focus-visible~.vno-knop{outline:3px solid #f2b705;outline-offset:3px}
.vno-cap{margin:8px 0 0;font-size:.8rem;color:#5b6670;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.vno-hint{color:#5b6670}
@media (prefers-reduced-motion:no-preference){.vno.vno-glij .vno-voor,.vno.vno-glij .vno-lijn,.vno.vno-glij .vno-knop{transition:clip-path .45s ease,left .45s ease}}
</style>"""

_PIJLEN = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true"><path d="M9 6l-6 6 6 6"/><path d="M15 6l6 6-6 6"/></svg>')


def _srcset(naam):
    b = f"/assets/fotos/renders/{naam}"
    return f"{b}-400.webp 400w, {b}-800.webp 800w, {b}-1600.webp 1600w"


def voorna_slider(paar, sizes, boven_vouw=False):
    """HTML van één voor-en-na-slider voor een paar uit render_voorna_data.PAREN.

    sizes: het sizes-attribuut van de afbeeldingen, bijvoorbeeld "(max-width: 860px) 100vw, 820px".
    De verhouding ligt vast op 3:2 (aspect-ratio), dus geen layout shift. Zonder JavaScript staat de
    scheiding op de helft en zie je beide helften.
    """
    v, n = paar["voor"], paar["na"]
    laden = 'loading="eager" fetchpriority="high"' if boven_vouw else 'loading="lazy"'
    sid = f"vno-{paar['slug']}"
    return f"""<figure class="vno-wrap" style="margin:0">
<div class="vno" id="{sid}" data-vno>
  <img class="vno-na" src="/assets/fotos/renders/{n['naam']}-800.webp" srcset="{_srcset(n['naam'])}" sizes="{_esc(sizes)}" width="{n['w']}" height="{n['h']}" alt="{_esc(n['alt'])}" {laden} decoding="async">
  <img class="vno-voor" src="/assets/fotos/renders/{v['naam']}-800.webp" srcset="{_srcset(v['naam'])}" sizes="{_esc(sizes)}" width="{v['w']}" height="{v['h']}" alt="{_esc(v['alt'])}" {laden} decoding="async">
  <span class="vno-label vno-label-voor" aria-hidden="true">Voor</span>
  <span class="vno-label vno-label-na" aria-hidden="true">Na</span>
  <input class="vno-range" type="range" min="0" max="100" step="1" value="50" aria-label="Vergelijk voor en na: {_esc(paar['kort'].lower())}. Naar links zie je meer van na, naar rechts meer van voor." aria-valuetext="50 procent voor, 50 procent na">
  <span class="vno-lijn" aria-hidden="true"></span>
  <span class="vno-knop" aria-hidden="true">{_PIJLEN}</span>
</div>
<figcaption class="vno-cap"><span>Illustratie (3D-render), geen echt project</span><span class="vno-hint">Sleep de schuif of gebruik de pijltjestoetsen</span></figcaption>
</figure>"""


VOORNA_JS = """<script>
(function(){
  var sliders = document.querySelectorAll('[data-vno]');
  if (!sliders.length) return;
  var stil = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  sliders.forEach(function(el){
    var r = el.querySelector('.vno-range');
    if (!r) return;
    function zet(p){
      p = Math.max(0, Math.min(100, Math.round(p)));
      el.style.setProperty('--p', p + '%');
      r.value = p;
      r.setAttribute('aria-valuetext', p + ' procent voor, ' + (100 - p) + ' procent na');
    }
    function vanX(x){
      var b = el.getBoundingClientRect();
      if (b.width > 0) zet((x - b.left) / b.width * 100);
    }
    r.addEventListener('input', function(){ el.classList.remove('vno-glij'); zet(+r.value); });
    var sleep = false;
    el.addEventListener('pointerdown', function(e){
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      sleep = true; el.classList.remove('vno-glij');
      if (el.setPointerCapture) { try { el.setPointerCapture(e.pointerId); } catch (_) {} }
      vanX(e.clientX); r.focus({preventScroll: true});
      if (e.pointerType === 'mouse') e.preventDefault();
    });
    el.addEventListener('pointermove', function(e){ if (sleep) vanX(e.clientX); });
    function los(){ sleep = false; }
    el.addEventListener('pointerup', los);
    el.addEventListener('pointercancel', los);
    el.addEventListener('lostpointercapture', los);
    // Home/End en PageUp/PageDown doet het range-element zelf; dit zijn grotere stappen met Shift
    r.addEventListener('keydown', function(e){
      if (e.shiftKey && (e.key === 'ArrowLeft' || e.key === 'ArrowRight')) {
        e.preventDefault(); zet(+r.value + (e.key === 'ArrowRight' ? 10 : -10));
      }
    });
    // korte hint als de slider in beeld komt: even heen en weer, alleen zonder 'beperk beweging'
    if (!stil && 'IntersectionObserver' in window) {
      var io = new IntersectionObserver(function(items){
        items.forEach(function(it){
          if (!it.isIntersecting) return;
          io.disconnect();
          if (sleep || +r.value !== 50) return;
          el.classList.add('vno-glij'); zet(62);
          setTimeout(function(){ if (el.classList.contains('vno-glij')) zet(50); }, 520);
          setTimeout(function(){ el.classList.remove('vno-glij'); }, 1100);
        });
      }, {threshold: 0.6});
      io.observe(el);
    }
    zet(+r.value || 50);
  });
})();
</script>"""


# ---------------------------------------------------------------------------
# Pagina
# ---------------------------------------------------------------------------

CSS = """<style>
.vnp-paar{margin:44px 0 0;padding-top:8px;scroll-margin-top:90px}
.vnp-paar h2{margin-bottom:6px}
.vnp-maat{color:#5b6670;font-size:.9rem;margin:0 0 14px}
.vnp-info{display:grid;grid-template-columns:1fr;gap:18px;margin-top:18px}
@media (min-width:760px){.vnp-info{grid-template-columns:1.35fr 1fr}}
.vnp-info h3{margin-top:0;font-size:1.05rem}
.vnp-info ul{margin:0;padding-left:1.15em}
.vnp-info li{margin:0 0 6px}
.vnp-prijs{background:#f4f7f9;border:1px solid #dfe6eb;border-radius:var(--radius,14px);padding:16px 18px}
.vnp-bedrag{font-size:1.45rem;font-weight:800;color:#1d3b53;margin:4px 0 2px;line-height:1.2}
.vnp-wat{font-size:.92rem;margin:0 0 10px}
.vnp-prijs p{font-size:.92rem}
.vnp-bron{font-size:.8rem;color:#5b6670;margin:8px 0 0}
.vnp-bron a{color:inherit}
.vnp-links{margin:12px 0 0;padding:0;list-style:none}
.vnp-links li{margin:0 0 6px}
.vnp-links a{font-weight:600}
.vnp-inhoud{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 0;padding:0;list-style:none}
.vnp-inhoud a{display:inline-block;padding:6px 12px;border:1px solid #cfd8de;border-radius:999px;font-size:.88rem;text-decoration:none}
.vnp-inhoud a:hover{background:#f4f7f9}
.vnp-kenmerken{display:grid;grid-template-columns:1fr;gap:12px;margin:14px 0 0;padding:0;list-style:none}
@media (min-width:640px){.vnp-kenmerken{grid-template-columns:1fr 1fr}}
.vnp-kenmerken li{border:1px solid #e3e8ec;border-radius:12px;padding:12px 14px;margin:0}
.vnp-kenmerken strong{display:block;margin-bottom:2px}
</style>"""


def _paar_sectie(p, i):
    pr = p["prijs"]
    veranderd = "".join(f"<li>{_esc(t)}</li>" for t in p["veranderd"])
    bronnen = ", ".join(f'<a href="{_esc(u)}" rel="noopener">{_esc(lab)}</a>' for lab, u in pr["bron"])
    href, label = p["link"]
    links = f'<li><a href="{href}">{_esc(label)} →</a></li>' + "".join(
        f'<li><a href="{h}">{_esc(t)}</a></li>' for h, t in p["links"])
    return f"""<section class="vnp-paar" id="{p['slug']}" aria-labelledby="h-{p['slug']}">
  <h2 id="h-{p['slug']}">{i}. {_esc(p['titel'])}</h2>
  <p class="vnp-maat">Afmeting in de illustratie: {_esc(p['maat'])}</p>
  <p>{_esc(p['intro'])}</p>
  {voorna_slider(p, "(max-width: 860px) calc(100vw - 32px), 820px", boven_vouw=(i == 1))}
  <div class="vnp-info">
    <div>
      <h3>Wat er veranderd is</h3>
      <ul>{veranderd}</ul>
    </div>
    <div class="vnp-prijs">
      <h3>Richtprijs voor deze ingreep</h3>
      <p class="vnp-bedrag">{_eur(pr['laag'])} – {_eur(pr['hoog'])}</p>
      <p class="vnp-wat">{_esc(pr['wat'])}, inclusief materiaal, arbeid en 21% btw.</p>
      <p>{_esc(pr['extra'])}</p>
      <p class="vnp-bron">Bron: {bronnen} (geraadpleegd november 2026). Richtprijs, je eigen offerte kan afwijken.</p>
      <ul class="vnp-links">{links}</ul>
    </div>
  </div>
</section>"""


FAQ = [
    ("Zijn dit foto's van echte badkamers?",
     "Nee. Het zijn 3D-illustraties die wij zelf hebben gemaakt. Per paar is het dezelfde ruimte met dezelfde maten en "
     "dezelfde camerahoek, zodat je goed ziet wat een renovatie verandert. Het zijn geen projecten van een bepaalde specialist."),
    ("Kan een bad zomaar plaatsmaken voor een inloopdouche?",
     "Meestal wel, omdat de afvoer van het bad al op die plek zit. Wel moet de vloer op afschot naar de afvoer of een goot, "
     "en moet de douchehoek opnieuw waterdicht worden gemaakt. Ligt de afvoer te hoog voor een vloer zonder drempel, "
     "dan kan een lage douchebak een oplossing zijn."),
    ("Moet ik alles slopen of kan ik ook alleen het sanitair vervangen?",
     "Dat kan allebei. Alleen een toilet of wastafel vervangen kan zonder sloopwerk. Zitten de oude tegels vast en is de "
     "kit nog goed, dan kun je ook overtegelen of de wanden afwerken met een tegelverf of panelen. Bij een bad naar een "
     "douche, of een hangtoilet in plaats van een staand toilet, moet er wel een deel uit."),
    ("Kan er asbest in een oude badkamer zitten?",
     "In woningen die vóór 1994 zijn gebouwd of verbouwd kan asbest zitten, bijvoorbeeld in oude vloerbedekking, "
     "plaatmateriaal achter tegels of rond leidingen. Twijfel je, laat het dan eerst onderzoeken voordat er gesloopt wordt."),
    ("Hoe lang duurt een badkamerrenovatie zoals in deze voorbeelden?",
     "Een toiletruimte duurt meestal enkele dagen. Een complete badkamer duurt vaak twee tot drie weken, omdat tegelwerk, "
     "waterdicht maken en drogen tijd kosten. Een zolderbadkamer met nieuw dak of isolatie kan langer duren."),
    ("Wat kost het om een badkamer uit de jaren 80 te renoveren?",
     "Een complete badkamer van 5 tot 9 m² kost meestal €6.000 tot €18.000, inclusief 21% btw. Een toiletruimte kost "
     "€2.500 tot €6.500. Bij elk voorbeeld op deze pagina staat een richtprijs voor precies die ingreep, met de bron."),
]


def _pagina(write):
    today = datetime.date.today().isoformat()
    cr, cr_ld = crumbs([("Home", "/"), ("Inspiratie", "/inspiratie/"), ("Voor en na", None)])
    inhoud = "".join(f'<li><a href="#{p["slug"]}">{_esc(p["kort"])}</a></li>' for p in PAREN)
    secties = "".join(_paar_sectie(p, i + 1) for i, p in enumerate(PAREN))
    faq_html, faq_ld = faq_blok(FAQ, "Veelgestelde vragen over voor en na")

    body = f"""{VOORNA_CSS}{CSS}{cr}
<article class="section-sm"><div class="wrap narrow prose">
  <span class="badge">Inspiratie · voor en na</span>
  <h1>Badkamer voor en na: vier renovaties in beeld</h1>
  <p class="lead">Beige tegels met een bloemetjesrand, een bad met douchegordijn en een tl-buis boven de spiegel. Veel badkamers zien er nog zo uit. Hier zie je vier van die ruimtes vóór en na een renovatie, steeds vanuit precies dezelfde hoek.</p>
  <p>Schuif over het beeld om te vergelijken. Bij elk voorbeeld lees je wat er veranderd is, wat zo'n ingreep ongeveer kost en waar je meer leest. De beelden zijn 3D-illustraties die wij zelf hebben gemaakt, geen foto's van echte projecten. Wij voeren zelf geen werk uit, maar brengen je in contact met maximaal drie badkamerspecialisten uit je regio.</p>
  <ul class="vnp-inhoud" aria-label="Naar een voorbeeld">{inhoud}</ul>

  {secties}

  {cta_midden("Je eigen badkamer ook aanpakken?", "Beschrijf wat je wilt veranderen en ontvang gratis offertes van maximaal drie badkamerspecialisten uit je regio.")}

  <h2 id="herkennen">Zo herken je een badkamer uit de jaren 80 en 90</h2>
  <p>De meeste kenmerken zijn vooral een kwestie van smaak. Een paar zeggen ook iets over de staat van de badkamer.</p>
  <ul class="vnp-kenmerken">
    <li><strong>Gekleurd sanitair</strong>Beige, pergamon of bahama: toen heel gewoon. Werkt het nog goed, dan is vervangen vooral een keuze voor de uitstraling.</li>
    <li><strong>Kleine tegels met veel voegen</strong>Tegels van 15 × 15 cm met een sierstrook. Veel voegen betekent meer schoonmaken, en oude voegen kunnen water doorlaten.</li>
    <li><strong>Bad met douchegordijn</strong>Douchen in het bad is een stap omhoog en een natte vloer. Een douche op vloerniveau is veiliger en makkelijker.</li>
    <li><strong>Staand toilet met reservoir</strong>Zichtbare leidingen en een voet om omheen te dweilen. Een hangtoilet maakt de vloer vrij.</li>
    <li><strong>Tl-buis en bollamp</strong>Koel, vlak licht. Spots en licht bij de spiegel geven een veel prettiger beeld.</li>
    <li><strong>Schrootjes en kunststof panelen</strong>Vooral op zolder. Achter schrootjes zit vaak weinig isolatie, wat condens en schimmel geeft.</li>
  </ul>

  <h2 id="aanpak">Waar let je op bij het renoveren van een oude badkamer?</h2>
  <ul class="checklist">
    <li><strong>Leidingen en afvoer.</strong> Oude leidingen kunnen beter meteen mee, nu de wanden toch open zijn. Bekijk ook of de afvoer laag genoeg ligt voor een douche zonder drempel.</li>
    <li><strong>Waterdicht maken.</strong> Tegels zelf zijn niet waterdicht. Onder de tegels in de douchehoek hoort een waterdichte laag. Lees meer in <a href="/kennisbank/badkamer-waterdicht-maken/">badkamer waterdicht maken</a>.</li>
    <li><strong>Ventilatie.</strong> Een oude badkamer heeft vaak alleen een klein raam of rooster. Een goede afzuiging voorkomt schimmel. Zie <a href="/kennisbank/badkamer-ventilatie/">ventilatie in de badkamer</a>.</li>
    <li><strong>Asbest.</strong> Is je woning gebouwd of verbouwd vóór 1994, laat dan eerst controleren of er asbest zit. Lees <a href="/kennisbank/asbest-in-badkamer/">asbest in de badkamer</a>.</li>
    <li><strong>Volgorde.</strong> Slopen, leidingwerk, elektra, waterdicht maken, tegelen en pas dan het sanitair. Zie <a href="/kennisbank/volgorde-badkamerrenovatie/">de volgorde van een badkamerrenovatie</a>.</li>
  </ul>
  <p>Wil je weten wat jouw badkamer ongeveer kost? Reken het uit met de <a href="/tools/badkamercalculator/">badkamercalculator</a> of bekijk de <a href="/kosten/">kostenpagina's</a>. Meer stijlen zie je bij <a href="/inspiratie/">badkamer inspiratie</a>.</p>

  {offertecheck_blok("een badkamerrenovatie")}
</div></article>
{faq_html}
{cta_blok("Klaar om je oude badkamer aan te pakken?", "Vertel in een minuut wat je wilt veranderen en ontvang gratis en vrijblijvend offertes van maximaal drie badkamerspecialisten uit jouw regio.")}
{VOORNA_JS}"""

    beelden = []
    for p in PAREN:
        for k in ("voor", "na"):
            r = p[k]
            beelden.append({"@type": "ImageObject", "url": f"{SITE['url']}/assets/fotos/renders/{r['naam']}-1600.webp",
                            "width": r["w"], "height": r["h"], "caption": r["bijschrift"]})
    art_ld = {
        "@context": "https://schema.org", "@type": "Article",
        "headline": "Badkamer voor en na: vier renovaties in beeld",
        "description": DESCRIPTION, "inLanguage": "nl-NL",
        "datePublished": GEPUBLICEERD, "dateModified": today,
        "image": beelden,
        "author": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "publisher": {"@type": "Organization", "@id": SITE["url"] + "/#organization", "name": SITE["naam"]},
        "mainEntityOfPage": SITE["url"] + PAD,
        "citation": sorted({u for p in PAREN for _, u in p["prijs"]["bron"]}),
    }
    write(PAD, page(title("Badkamer voor en na: vier renovaties in beeld"), DESCRIPTION, PAD, body,
                    [cr_ld, art_ld, faq_ld]), prio=0.7)


DESCRIPTION = ("Badkamer voor en na: vier badkamers uit de jaren 80 en 90 vóór en na de renovatie. "
               "Schuif over het beeld en lees wat er veranderd is en wat het ongeveer kost.")


def build(write):
    _pagina(write)
