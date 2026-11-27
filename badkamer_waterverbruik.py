# -*- coding: utf-8 -*-
"""Water- en energieverbruik van douche en bad (/tools/waterverbruik/).

Losse module met de interface LINKS + build(write). De berekening gebeurt in de
browser met de constanten hieronder (json.dumps naar de JavaScript).

Bronnen, geraadpleegd in november 2026 (peildatum tarieven: november 2026):
- CBS, Watergebruik thuis 2021, hoofdstuk De douche: gemiddeld 7,4 minuten per
  beurt, gemiddeld 7,7 liter per minuut over alle douches, waterbesparende kop
  gemeten 6,3 l/min, regendouche 10,3 l/min, massagedouche 13,6 l/min,
  46,2 liter per persoon per dag bij 56,9 liter per beurt (= ongeveer 5,7 beurten
  per persoon per week).
- Milieu Centraal, Besparen onder de douche en in bad (laatst gewijzigd augustus
  2026): gasprijs € 1,37 per m³ (verwachte gemiddelde prijs 2026-2040);
  elektrische boiler ruim 1.700 kWh voor € 360 (daaruit volgt ongeveer € 0,21 per
  kWh; eigen afleiding); waterbesparende kop maximaal 7,2 l/min; bad 140 liter;
  thermostaatkraan bespaart gemiddeld 650 liter water per jaar; van 7,4 naar
  5 minuten douchen bespaart ca. € 36 per persoon per jaar.
- Milieu Centraal, Nieuwe badkamer: douche-wtw bespaart 40 tot 50% van de
  energie voor het douchen.
- Vitens, Tarieven 2026 consument: € 1,34 per m³ incl. 9% btw, plus belasting op
  leidingwater € 0,477 per m³. Wij rekenen met ongeveer € 1,80 per m³; het tarief
  verschilt per waterbedrijf.

Rekenmodel (eigen aannames, staan ook op de pagina):
- Douchewater gemengd op 38 °C, bad op 40 °C, koud leidingwater 10 °C.
  Warmte per liter = 4,186 kJ/(kg·K) x temperatuurverschil.
- Cv-ketel: 1 m³ aardgas = 9,77 kWh (bovenwaarde), rendement voor warm water 85%.
- Elektrische boiler: rendement 85% inclusief stilstandsverlies.
- Warmtepomp(boiler): gemiddeld 2,5 kWh warmte per kWh stroom.
Controle: met 7,7 l/min en € 1,37 per m³ geeft 7,4 naar 5 minuten douchen
ongeveer € 36 per persoon per jaar, gelijk aan Milieu Centraal.
"""

import json

from components import page, crumbs, faq_blok, cta_blok, title, desc

PAD = "/tools/waterverbruik/"
KENNIS = "/kennisbank/water-besparen-badkamer/"

LINKS = [
    (PAD, "Waterverbruik douche en bad",
     "Reken uit hoeveel water, gas of stroom je douche en bad kosten, en wat je kunt besparen."),
]

KOPPEN = [
    {"id": "zuinig", "naam": "Waterbesparende kop", "lpm": 6.3, "noot": "gemeten gemiddelde, CBS"},
    {"id": "gewoon", "naam": "Gewone douchekop", "lpm": 7.7, "noot": "gemiddelde van alle douches, CBS"},
    {"id": "regen", "naam": "Regendouche", "lpm": 10.3, "noot": "CBS"},
    {"id": "massage", "naam": "Massagedouche", "lpm": 13.6, "noot": "CBS"},
]

VERWARMING = [
    {"id": "gas", "naam": "Cv-ketel op gas"},
    {"id": "boiler", "naam": "Elektrische boiler"},
    {"id": "wp", "naam": "Warmtepomp"},
]

MODEL = {
    "koud": 10, "douche_temp": 38, "bad_temp": 40, "bad_liter": 140,
    "kwh_per_m3_gas": 9.77, "rend_gas": 0.85, "rend_boiler": 0.85, "cop_wp": 2.5,
    "zuinig_lpm": 6.3, "thermo_liter": 650, "wtw_laag": 0.40, "wtw_hoog": 0.50,
}

TARIEVEN = {"gas": 1.37, "stroom": 0.21, "water": 1.80}

JS = r"""
(function () {
  var D = __DATA__, K = {}, MD = D.model;
  D.koppen.forEach(function (k) { K[k.id] = k; });
  var root = document.querySelector("[data-wv]");
  if (!root) { return; }
  function $(s) { return root.querySelector(s); }
  function keuze(n) { var e = root.querySelector('input[name="' + n + '"]:checked'); return e ? e.value : ""; }
  function num(id, min, max, std) {
    var v = parseFloat(String($(id).value).replace(",", "."));
    return isFinite(v) ? Math.min(max, Math.max(min, v)) : std;
  }
  function nl(n, d) { return n.toLocaleString("nl-NL", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function eur(n) { return "€" + nl(Math.round(n)); }
  var stil = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // kWh warmte per liter bij een bepaalde temperatuur
  function warmte(temp) { return 4.186 * (temp - MD.koud) / 3600; }
  // energie (eenheid van de verwarming) per kWh warmte
  function energie(kwh, verw) {
    if (verw === "gas") { return kwh / (MD.kwh_per_m3_gas * MD.rend_gas); }
    if (verw === "boiler") { return kwh / MD.rend_boiler; }
    return kwh / MD.cop_wp;
  }

  function lees() {
    return {
      pers: num("#wv-pers", 1, 10, 2), min: num("#wv-min", 1, 30, 8), keer: num("#wv-keer", 0, 21, 6),
      kop: keuze("wv-kop"), wat: keuze("wv-wat"), baden: num("#wv-baden", 0, 14, 1), verw: keuze("wv-verw"),
      gas: num("#wv-tgas", 0.2, 5, D.tarief.gas), stroom: num("#wv-tstroom", 0.02, 2, D.tarief.stroom),
      water: num("#wv-twater", 0.2, 6, D.tarief.water)
    };
  }

  // Jaarcijfers voor douchen en baden apart
  function jaar(i, lpm, minuten) {
    var douche = i.wat === "bad" ? 0 : i.pers * i.keer * 52 * minuten * lpm;
    var bad = i.wat === "douche" ? 0 : i.baden * 52 * MD.bad_liter;
    var eD = energie(douche * warmte(MD.douche_temp), i.verw), eB = energie(bad * warmte(MD.bad_temp), i.verw);
    var prijsE = i.verw === "gas" ? i.gas : i.stroom;
    return { lD: douche, lB: bad, eD: eD, eB: eB,
             kE: (eD + eB) * prijsE, kW: (douche + bad) / 1000 * i.water, prijsE: prijsE };
  }

  function telOp(el, doel, fmt) {
    var van = parseFloat(el.dataset.v);
    el.dataset.v = doel;
    if (stil || !isFinite(van) || Math.abs(doel - van) < 1) { el.textContent = fmt(doel); return; }
    var t0 = null;
    function stap(t) {
      if (!t0) { t0 = t; }
      var p = Math.min(1, (t - t0) / 350), x = van + (doel - van) * (1 - Math.pow(1 - p, 3));
      el.textContent = fmt(x);
      if (p < 1) { requestAnimationFrame(stap); }
    }
    requestAnimationFrame(stap);
  }

  function toon() {
    var i = lees();
    $("[data-wv-douche]").hidden = i.wat === "bad";
    $("[data-wv-bad]").hidden = i.wat === "douche";
    $("[data-wv-minw]").textContent = nl(i.min) + " min";
    var lpm = K[i.kop].lpm, j = jaar(i, lpm, i.min);
    var liters = j.lD + j.lB, en = j.eD + j.eB, totaal = j.kE + j.kW;
    var eenh = i.verw === "gas" ? " m³ gas" : " kWh stroom";
    telOp($("[data-wv-liter]"), liters, function (x) { return nl(Math.round(x / 100) * 100) + " liter"; });
    telOp($("[data-wv-energie]"), en, function (x) { return nl(Math.round(x)) + eenh; });
    telOp($("[data-wv-kosten]"), totaal, function (x) { return eur(x); });
    $("[data-wv-dag]").textContent = "Dat is ongeveer " + nl(Math.round(liters / 365)) + " liter per dag, of " + nl(Math.round(liters / 140)) + " volle badkuipen per jaar.";
    $("[data-wv-split]").textContent = "Energie " + eur(j.kE) + " en water " + eur(j.kW) + " per jaar. Je betaalt dus vooral voor het verwarmen.";
    var pE = totaal > 0 ? j.kE / totaal * 100 : 0;
    $("[data-wv-bar-e]").style.width = pE.toFixed(1) + "%";
    $("[data-wv-bar-w]").style.width = (100 - pE).toFixed(1) + "%";

    // ---- besparingen ----
    var rij = [], prijsE = j.prijsE;
    function regel(titel, euro, tekst, liter) {
      rij.push({ t: titel, e: Math.max(0, euro), x: tekst, l: liter || 0 });
    }
    if (i.wat !== "bad") {
      if (lpm > MD.zuinig_lpm) {
        var z = jaar(i, MD.zuinig_lpm, i.min);
        regel("Waterbesparende douchekop", (j.kE + j.kW) - (z.kE + z.kW),
          "Van " + nl(lpm, 1) + " naar " + nl(MD.zuinig_lpm, 1) + " liter per minuut. Een kop kost weinig en vervang je zelf.", liters - (z.lD + z.lB));
      } else {
        regel("Waterbesparende douchekop", 0, "Die heb je al. Goed bezig.", 0);
      }
      var tl = MD.thermo_liter, tE = energie(tl * warmte(MD.douche_temp), i.verw);
      regel("Thermostaatkraan", tl / 1000 * i.water + tE * prijsE,
        "Minder water weg tijdens het afstellen van de temperatuur. Milieu Centraal noemt gemiddeld " + nl(tl) + " liter per jaar; wij rekenen dat per huishouden.", tl);
      var wl = j.eD * MD.wtw_laag * prijsE, wh = j.eD * MD.wtw_hoog * prijsE;
      rij.push({ t: "Douche-wtw (warmteterugwinning)", e: (wl + wh) / 2, bereik: eur(wl) + " – " + eur(wh),
                 x: "40 tot 50% minder energie voor het douchen. Neem dit mee bij een verbouwing.", l: 0 });
      if (i.min > 1) {
        var k = jaar(i, lpm, i.min - 1);
        regel("Elke beurt 1 minuut korter", (j.kE + j.kW) - (k.kE + k.kW),
          "Met " + nl(i.pers) + (i.pers === 1 ? " persoon" : " personen") + " en " + nl(i.keer) + " keer per week.", liters - (k.lD + k.lB));
      }
    }
    if (i.wat !== "douche" && i.baden > 0) {
      var b1 = 52 * MD.bad_liter, b1E = energie(b1 * warmte(MD.bad_temp), i.verw);
      var d1 = 52 * Math.min(i.min, 10) * Math.max(lpm, 6.3), d1E = energie(d1 * warmte(MD.douche_temp), i.verw);
      regel("Eén bad per week vervangen door een douche", (b1 - d1) / 1000 * i.water + (b1E - d1E) * prijsE,
        "Een bad kost " + nl(MD.bad_liter) + " liter. Een douche van " + nl(Math.min(i.min, 10)) + " minuten kost minder.", b1 - d1);
    }
    var max = rij.reduce(function (m, r) { return Math.max(m, r.e); }, 1), html = "";
    rij.forEach(function (r) {
      html += '<li><div class="wv-bk"><strong>' + r.t + '</strong><b>' + (r.e < 0.5 ? "–" : (r.bereik || eur(r.e)) + " per jaar") + '</b></div>' +
        '<div class="wv-bb" aria-hidden="true"><span style="width:' + (r.e / max * 100).toFixed(1) + '%"></span></div>' +
        '<p>' + r.x + (r.l > 50 ? " Scheelt ongeveer " + nl(Math.round(r.l / 100) * 100) + " liter per jaar." : "") + '</p></li>';
    });
    $("[data-wv-bespaar]").innerHTML = html;
    $("[data-wv-tarief]").textContent = "Gerekend met " + (i.verw === "gas" ? "gas €" + nl(i.gas, 2) + " per m³" : "stroom €" + nl(i.stroom, 2) + " per kWh") + " en water €" + nl(i.water, 2) + " per m³.";
  }
  root.addEventListener("input", toon);
  root.addEventListener("change", toon);
  toon();
})();
"""

CSS = """<style>
.wv-tool{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:18px}
@media(min-width:900px){.wv-tool{padding:28px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:30px;align-items:start}}
.wv-in{display:grid;gap:16px}
.wv-tool fieldset{border:0;margin:0;padding:0;min-width:0}
.wv-tool legend,.wv-lbl{font-weight:700;color:var(--ink);margin-bottom:8px;display:block}
.wv-keuze{display:flex;flex-wrap:wrap;gap:6px}
.wv-keuze label{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:6px 11px;cursor:pointer;font-size:.9rem;color:var(--ink)}
.wv-keuze input{accent-color:var(--accent)}
.wv-keuze label:has(input:checked){border-color:var(--navy);background:var(--bg-soft)}
.wv-keuze small{color:var(--muted)}
.wv-tool input[type=number]{width:100%;padding:9px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;color:var(--ink);background:#fff}
.wv-tool input[type=range]{width:100%;accent-color:var(--accent)}
.wv-drie{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.wv-drie label{font-size:.85rem;color:var(--muted)}
.wv-twee{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.wv-twee label{font-size:.85rem;color:var(--muted)}
.wv-in [hidden]{display:none}
.wv-tool details{border:1px solid var(--line);border-radius:var(--radius);padding:10px 12px}
.wv-tool summary{cursor:pointer;font-weight:600;color:var(--ink)}
.wv-sam{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px}
.wv-sam div{background:var(--bg-soft);border-radius:var(--radius);padding:12px}
.wv-sam small{display:block;color:var(--muted);font-size:.8rem}
.wv-sam b{font-size:1.15rem;color:var(--ink);font-variant-numeric:tabular-nums}
.wv-noot{font-size:.88rem;margin:8px 0}
.wv-split{display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--bg-soft);margin:6px 0 2px}
.wv-split span:first-child{background:var(--accent)}
.wv-split span:last-child{background:#5f9aa3}
.wv-leg{display:flex;gap:14px;font-size:.8rem;color:var(--muted);margin:0 0 14px}
.wv-leg i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:-1px}
.wv-tool h2{font-size:1.15rem;margin:18px 0 8px}
.wv-lijst{list-style:none;margin:0;padding:0}
.wv-lijst li{padding:10px 0;border-bottom:1px solid var(--line)}
.wv-bk{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.wv-bk strong{color:var(--ink)}
.wv-bk b{color:var(--navy);font-variant-numeric:tabular-nums}
.wv-bb{height:8px;border-radius:4px;background:var(--bg-soft);margin:6px 0;overflow:hidden}
.wv-bb span{display:block;height:100%;background:#5f9aa3;border-radius:4px}
.wv-lijst p{font-size:.86rem;margin:0}
@media(prefers-reduced-motion:no-preference){.wv-bb span,.wv-split span{transition:width .35s ease}}
</style>"""


def _tool_html():
    koppen = "".join(
        f'<label><input type="radio" name="wv-kop" value="{k["id"]}"{" checked" if k["id"] == "gewoon" else ""}> '
        f'{k["naam"]} <small>{str(k["lpm"]).replace(".", ",")} l/min</small></label>'
        for k in KOPPEN)
    verw = "".join(
        f'<label><input type="radio" name="wv-verw" value="{v["id"]}"{" checked" if v["id"] == "gas" else ""}> {v["naam"]}</label>'
        for v in VERWARMING)
    t = TARIEVEN
    return f"""<div class="wv-tool" data-wv>
  <form class="wv-in" onsubmit="return false">
    <fieldset><legend>1. Douche of bad?</legend><div class="wv-keuze">
      <label><input type="radio" name="wv-wat" value="douche" checked> Alleen douche</label>
      <label><input type="radio" name="wv-wat" value="allebei"> Douche en soms bad</label>
      <label><input type="radio" name="wv-wat" value="bad"> Alleen bad</label></div></fieldset>
    <div class="wv-twee">
      <label><span class="wv-lbl">2. Personen</span><input type="number" id="wv-pers" value="2" min="1" max="10" step="1" inputmode="numeric"></label>
      <label data-wv-bad hidden><span class="wv-lbl">Baden per week</span><input type="number" id="wv-baden" value="1" min="0" max="14" step="1" inputmode="numeric"></label>
    </div>
    <div data-wv-douche>
      <label class="wv-lbl" for="wv-min">3. Douchetijd per beurt: <span data-wv-minw>8 min</span></label>
      <input type="range" id="wv-min" min="2" max="20" step="1" value="8">
      <label style="font-size:.85rem;color:var(--muted);display:block;margin-top:10px">Douchebeurten per persoon per week (gemiddeld bijna 6)
        <input type="number" id="wv-keer" value="6" min="0" max="21" step="1" inputmode="numeric"></label>
    </div>
    <fieldset data-wv-douche><legend>4. Soort douchekop</legend><div class="wv-keuze">{koppen}</div></fieldset>
    <fieldset><legend>5. Hoe wordt je water warm?</legend><div class="wv-keuze">{verw}</div></fieldset>
    <details><summary>Tarieven aanpassen</summary>
      <p style="font-size:.85rem;color:var(--muted);margin:8px 0">Peildatum november 2026. Vul gerust je eigen tarieven in; die staan op je jaarafrekening.</p>
      <div class="wv-drie">
        <label>Gas per m³ (€)<input type="number" id="wv-tgas" value="{t['gas']}" min="0.2" max="5" step="0.01" inputmode="decimal"></label>
        <label>Stroom per kWh (€)<input type="number" id="wv-tstroom" value="{t['stroom']}" min="0.02" max="2" step="0.01" inputmode="decimal"></label>
        <label>Water per m³ (€)<input type="number" id="wv-twater" value="{t['water']:.2f}" min="0.2" max="6" step="0.01" inputmode="decimal"></label>
      </div></details>
  </form>
  <div aria-live="polite">
    <div class="wv-sam">
      <div><small>Water per jaar</small><b data-wv-liter>–</b></div>
      <div><small>Energie per jaar</small><b data-wv-energie>–</b></div>
      <div><small>Kosten per jaar</small><b data-wv-kosten>–</b></div>
    </div>
    <p class="wv-noot" data-wv-dag></p>
    <div class="wv-split" aria-hidden="true"><span data-wv-bar-e></span><span data-wv-bar-w></span></div>
    <p class="wv-leg"><span><i style="background:var(--accent)"></i>Energie</span><span><i style="background:#5f9aa3"></i>Water</span></p>
    <p class="wv-noot" data-wv-split></p>
    <h2>Zoveel kun je besparen</h2>
    <ul class="wv-lijst" data-wv-bespaar></ul>
    <p style="font-size:.82rem;color:var(--muted);margin:10px 0 0"><span data-wv-tarief></span> Het is een schatting: je echte verbruik hangt af van je ketel, de lengte van de leidingen en hoe warm je doucht.</p>
    <p style="margin:14px 0 0"><a href="{KENNIS}">Meer tips: water besparen in de badkamer →</a></p>
  </div>
</div>"""


def _js():
    data = {"koppen": KOPPEN, "model": MODEL, "tarief": TARIEVEN}
    return "<script>\n" + JS.replace("__DATA__", json.dumps(data, ensure_ascii=False)) + "</script>"


def _uitleg_html():
    return f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Waar betaal je voor bij het douchen?</h2>
  <p>Water uit de kraan is in Nederland niet duur. Het opwarmen kost het meeste geld. Daarom levert minder <strong>warm</strong> water het meeste op. Een gemiddelde douchebeurt duurt volgens het CBS 7,4 minuten. Met een gewone douchekop stroomt er dan ongeveer 57 liter door. Een bad kost met zo'n 140 liter veel meer water en energie dan een douche.</p>
  <h3>Drie maatregelen die veel opleveren</h3>
  <ul>
    <li><strong>Waterbesparende douchekop.</strong> Zo'n kop laat volgens Milieu Centraal maximaal 7,2 liter per minuut door en voelt toch vol aan. Test je douche met de emmertest: vang een minuut water op. Zit er meer dan 7 liter in, dan loont een zuinige kop.</li>
    <li><strong>Thermostaatkraan.</strong> Je hebt meteen de goede temperatuur. Zo loopt er minder water weg terwijl je de kraan afstelt.</li>
    <li><strong>Douche-wtw.</strong> Een warmteterugwinsysteem haalt warmte uit het weglopende douchewater. Volgens Milieu Centraal bespaar je zo 40 tot 50 procent van de energie voor het douchen. Inbouwen kan het best tijdens een verbouwing.</li>
  </ul>
  <p>Wil je meer weten? Lees dan <a href="{KENNIS}">water besparen in de badkamer</a>. Daar staan ook tips over het toilet en de leidingen.</p>
  <h3>Hoe rekent de tool?</h3>
  <p>We rekenen met de liters per minuut die het CBS heeft gemeten per soort douche: waterbesparend 6,3, gemiddeld 7,7, regendouche 10,3 en massagedouche 13,6 liter per minuut. Douchewater warmt de tool op van 10 naar 38 graden, een bad tot 40 graden. Een cv-ketel haalt daarbij 85 procent rendement. Een elektrische boiler rekenen we ook met 85 procent, omdat hij warmte verliest terwijl hij stilstaat. Een warmtepomp maakt gemiddeld 2,5 kWh warmte van 1 kWh stroom. Dit zijn eigen aannames; de echte waarden verschillen per toestel.</p>
  <p>Controle: van 7,4 naar 5 minuten douchen met een gemiddelde douche levert in de tool ongeveer €36 per persoon per jaar op. Dat is hetzelfde bedrag dat Milieu Centraal noemt.</p>
  <h3>Tarieven en bronnen (peildatum november 2026)</h3>
  <ul style="font-size:.92rem">
    <li>Gas €1,37 per m³: de prijs waarmee Milieu Centraal rekent, de verwachte gemiddelde prijs voor 2026 tot 2040 (<a href="https://www.milieucentraal.nl/energie-besparen/duurzaam-warm-water/besparen-onder-de-douche/" rel="nofollow noopener" target="_blank">Milieu Centraal, besparen onder de douche</a>).</li>
    <li>Stroom €0,21 per kWh: afgeleid uit hetzelfde artikel van Milieu Centraal (ruim 1.700 kWh voor een elektrische boiler kost daar €360). Je eigen stroomprijs kan hoger zijn. Pas hem dan aan bij de tarieven.</li>
    <li>Water €1,80 per m³: ongeveer het tarief van Vitens voor 2026 inclusief btw (€1,34) plus de belasting op leidingwater (€0,477). Elk waterbedrijf heeft een eigen tarief (<a href="https://www.vitens.nl/-/media/Project/Vitens/VitensNl/Tarieven/Documenten-tarieven-2026/050004-31_Vitens-Tarieven-2026-Consument.pdf" rel="nofollow noopener" target="_blank">Vitens, tarieven 2026</a>).</li>
    <li>Liters per minuut en douchetijd: <a href="https://www.cbs.nl/nl-nl/longread/aanvullende-statistische-diensten/2022/watergebruik-thuis--wgt---2021/6-de-douche" rel="nofollow noopener" target="_blank">CBS, Watergebruik thuis 2021</a>.</li>
    <li>Douche-wtw 40 tot 50%: <a href="https://www.milieucentraal.nl/in-en-om-het-huis/verbouwen/nieuwe-badkamer/" rel="nofollow noopener" target="_blank">Milieu Centraal, nieuwe badkamer</a>.</li>
  </ul>
</div></section>"""


FAQS = [
    ("Hoeveel water gebruikt een douche per minuut?",
     "Volgens metingen van het CBS gemiddeld 7,7 liter per minuut. Een waterbesparende kop zit rond de 6,3 liter, een regendouche rond de 10,3 liter en een massagedouche rond de 13,6 liter per minuut."),
    ("Wat kost een douchebeurt?",
     "Een douche van 8 minuten met een gewone kop en een cv-ketel kost met de tarieven in deze tool ongeveer 45 cent: zo'n 35 cent voor het gas en 10 cent voor het water. Met een regendouche is het ongeveer een derde meer."),
    ("Is een bad duurder dan douchen?",
     "Meestal wel. Een gemiddeld bad kost ongeveer 140 liter warm water. Dat is net zoveel als ruim twee douchebeurten van 8 minuten met een gewone douchekop."),
    ("Wat levert een douche-wtw op?",
     "Volgens Milieu Centraal 40 tot 50 procent van de energie voor het douchen. Hoeveel euro dat is, hangt af van hoe vaak en hoe lang er in je huis wordt gedoucht. Bij een groot gezin verdien je hem sneller terug. Inbouwen kan het best tijdens een verbouwing."),
    ("Kloppen de bedragen voor mijn huis?",
     "Het is een schatting. Je echte verbruik hangt af van je ketel of warmtepomp, de lengte van de leidingen en hoe warm je doucht. Vul je eigen tarieven in voor een betere schatting. Die staan op je jaarafrekening."),
]


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Waterverbruik", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over water en energie")
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Calculator waterverbruik douche en bad",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsers",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Reken uit hoeveel water, gas of stroom je douche en bad per jaar kosten en wat een zuinige douchekop, thermostaatkraan of douche-wtw bespaart.",
    }
    body = f"""{cr}
{CSS}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:22px">
    <span class="badge">Gratis tool</span>
    <h1>Wat kost douchen en baden per jaar?</h1>
    <p class="lead">Vul in met hoeveel mensen je bent, hoe lang je doucht en welke douchekop je hebt. Je ziet hoeveel water en energie dat per jaar kost, en wat je bespaart met een zuinige kop, een thermostaatkraan of een douche-wtw.</p>
  </div>
  {_tool_html()}
</div></section>
{_uitleg_html()}
{faq_html}
{cta_blok("Een zuinige badkamer bij je verbouwing?", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Vraag ze meteen naar een douche-wtw en een thermostaatkraan.", "Gratis offertes aanvragen")}
{_js()}"""
    write(PAD, page(
        title("Waterverbruik douche en bad: kosten per jaar"),
        desc("Reken gratis uit wat douchen en baden per jaar kosten aan water, gas of stroom.",
             "Zie wat een zuinige douchekop, thermostaatkraan of douche-wtw bespaart."),
        PAD, body, jsonld=[cr_ld, app_ld, faq_ld]), prio=0.7)
