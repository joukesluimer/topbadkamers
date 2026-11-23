# -*- coding: utf-8 -*-
"""Badkamercalculator: wat kost jouw nieuwe badkamer ongeveer? (/tools/badkamercalculator/)

Losse module met de interface LINKS + build(write). Rekent in de browser met
de constante REKENWAARDEN hieronder; die gaat met json.dumps naar de JavaScript.
De bedragen zelf komen uit richtprijzen.py, zodat de calculator, de offertechecker
en de kostenpagina's dezelfde bandbreedtes gebruiken.

Alle bedragen zijn richtprijzen INCLUSIEF 21% btw, net als data.DIENSTEN. De
calculator laat het btw-deel apart zien (21/121 van het totaal).

Bronnen, geraadpleegd in november 2026 (de actuele waarden en bronnen staan in richtprijzen.py):
- Sloopwerk badkamer €265 – €685 (Werkspot) en €250 – €850 excl. afvoer (Slimster):
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kosten-badkamer-slopen
  https://slimster.nl/sloopwerk/sloopkosten/badkamer-slopen-kosten/
- Puin afvoeren: container 3 m³ €125 – €165, eenvoudige sloop met afvoer €200 – €400 (Werkspot):
  https://www.werkspot.nl/sloop-afvoeren/prijzen-kosten/puin-afvoeren
- Tegels €20 – €60 per m² (Werkspot), legloon €25 – €55 per m² (data.DIENSTEN, Trustoo/Homedeal):
  https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten
  https://trustoo.nl/kosten/tegelzetter-kosten/
- Sanitair: douche €500 – €2.000, toilet €450 – €900, ligbad €700 – €1.500, totaal sanitair
  €1.000 – €6.000 (Homedeal); douche plaatsen €600 – €1.900, bad plaatsen €850 – €2.800 (Werkspot):
  https://www.homedeal.nl/verbouwing/badkamer-verbouwen-kosten/
  https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/sanitair-plaatsen
- Leidingwerk op dezelfde plek €1.250 – €2.200 (Trustoo), €1.500 – €3.000 (Slimster):
  https://trustoo.nl/kosten/badkamer-renovatie-kosten/
  https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/
- Elektra €300 – €1.000 (Trustoo), €500 – €1.500 (Slimster); elektrische vloerverwarming
  per badkamer €600 – €1.100 (Trustoo), ook de ondergrens van de calculator.
- Elektrische vloerverwarming badkamer €40 – €110 per m² (Werkspot), €60 – €80 per m² (Slimster):
  https://www.werkspot.nl/verwarming/prijzen-kosten/vloerverwarming-badkamer
  https://slimster.nl/vloerverwarming/kosten/
- Stopcontact aanleggen €55 – €150 per stuk (Werkspot, Slimster); ventilator plus montage
  ruwweg €150 – €400 (indicatie op basis van Werkspot/Gamma, brede marge):
  https://www.werkspot.nl/stopcontact-plaatsen/prijzen-kosten
  https://slimster.nl/elektricien/wat-kost-een-stopcontact-aanleggen/
- Controle op het geheel: een middensegment-badkamer van 5 – 9 m² kost €6.000 – €18.000
  (data.DIENSTEN "badkamer-renoveren", Homedeal/Trustoo/Slimster). De standaardinvoer van de
  calculator (2 × 2,5 m, midden, douche + hangtoilet + meubel) valt daar binnen.
- Regiofactor: data.PRIJSINDEX per provincie (eigen schatting, zie data.py).
"""

import json

from data import PLAATSEN, PRIJSINDEX
import richtprijzen as RP
from components import page, crumbs, faq_blok, cta_blok, title, desc

PAD = "/tools/badkamercalculator/"

LINKS = [
    (PAD, "Badkamercalculator",
     "Reken uit wat je nieuwe badkamer ongeveer kost, per post en inclusief btw."),
]

# ---------------------------------------------------------------------------
# Rekenwaarden (euro, inclusief 21% btw). [laag, hoog]
# Alle bedragen komen uit richtprijzen.py; hier staat alleen hoe de calculator ze gebruikt.
# ---------------------------------------------------------------------------
REKENWAARDEN = {
    "btw": 0.21,
    "deur_m2": 1.6,             # aftrek voor de deur bij wandtegels
    "halfhoog_m": 1.2,          # hoogte van halfhoog wandtegelwerk
    # Sloopwerk: vast deel + per m² vloer (sluit aan op RP "sloop" €250 – €850)
    "sloop_vast": RP.lh("sloop_vast"),
    "sloop_m2": RP.lh("sloop_m2"),
    # Afval: met sloop door het bedrijf, of alleen een container als je zelf sloopt
    "afval_sloop": RP.lh("afval"),
    "afval_zelf": RP.lh("container"),
    # Tegels (materiaal) per m², per sanitairniveau
    "tegel_materiaal": RP.niveaus("tegels"),
    # Tegelzetten per m²: legloon plus lijm, voegsel en kit
    "tegel_arbeid": [RP.lh("tegelwerk")[0] + RP.lh("tegelwerk_hulpmateriaal")[0],
                     RP.lh("tegelwerk")[1] + RP.lh("tegelwerk_hulpmateriaal")[1]],
    # Waterdicht maken en afschot in de douchehoek (vast bedrag)
    "waterdicht": RP.lh("waterdicht"),
    # Sanitair (alleen het product), per niveau
    "sanitair": {k: RP.niveaus("sanitair_" + k) for k in ("douche", "bad", "toilet", "meubel")},
    # Montage door de installateur per onderdeel
    "montage": {k: RP.lh("montage_" + k) for k in ("douche", "bad", "toilet", "meubel")},
    # Leidingwerk vernieuwen op dezelfde plek (alleen bij een renovatie met sloopwerk)
    "leidingwerk_basis": RP.lh("leidingwerk"),
    # Leidingen en afvoer verplaatsen: extra bovenop het leidingwerk
    "leiding_verplaatsen": RP.lh("leidingwerk_verplaatsen"),
    # Elektra
    "vloerverwarming_m2": RP.lh("vloerverwarming_m2"),
    "vloerverwarming_min": RP.lh("vloerverwarming_elektrisch"),
    "ventilator": RP.lh("ventilator"),
    "elektra_extra": RP.lh("elektra"),   # stopcontacten, schakelaars en spots
}

POSTEN = [
    ("sloop", "Sloopwerk"),
    ("tegel_mat", "Tegels (materiaal)"),
    ("tegel_arb", "Tegelzetten en waterdicht maken"),
    ("sanitair", "Sanitair"),
    ("installatie", "Installatie en leidingwerk"),
    ("elektra", "Elektra en vloerverwarming"),
    ("afval", "Afvoer van afval"),
]

# Rekenfunctie: puur, zonder DOM, zodat hij los met node te testen is.
REKEN_JS = r"""/*REKEN-START*/
function berekenBadkamer(inv, R) {
  function r2(x) { return Math.round(x * 100) / 100; }
  var L = +inv.lengte || 0, B = +inv.breedte || 0, H = +inv.hoogte || 2.6;
  var vloer = inv.m2 ? +inv.m2 : L * B;
  if (!(vloer > 0)) { vloer = 0; }
  var omtrek = (L > 0 && B > 0) ? 2 * (L + B) : 4 * Math.sqrt(vloer);
  var wandH = inv.tegels === "plafond" ? H : (inv.tegels === "halfhoog" ? R.halfhoog_m : 0);
  var wand = Math.max(0, omtrek * wandH - (wandH > 0 ? R.deur_m2 * Math.min(1, wandH / 2.1) : 0));
  var tegelM2 = inv.tegels === "geen" ? 0 : vloer + wand;
  var niv = inv.niveau || "midden";
  var o = inv.onderdelen || {};
  var p = {};
  function zet(k, lo, hi) { p[k] = [ (p[k] ? p[k][0] : 0) + lo, (p[k] ? p[k][1] : 0) + hi ]; }
  function zetR(k, r, f) { f = f === undefined ? 1 : f; zet(k, r[0] * f, r[1] * f); }

  if (inv.sloop) { zetR("sloop", R.sloop_vast); zetR("sloop", R.sloop_m2, vloer); zetR("afval", R.afval_sloop); }
  else { zet("sloop", 0, 0); zetR("afval", R.afval_zelf); }

  zetR("tegel_mat", R.tegel_materiaal[niv], tegelM2);
  zetR("tegel_arb", R.tegel_arbeid, tegelM2);
  if (tegelM2 > 0 && (o.douche || o.bad)) { zetR("tegel_arb", R.waterdicht); }

  zet("sanitair", 0, 0); zet("installatie", 0, 0); zet("elektra", 0, 0);
  ["douche", "bad", "toilet", "meubel"].forEach(function (k) {
    if (o[k]) { zetR("sanitair", R.sanitair[k][niv]); zetR("installatie", R.montage[k]); }
  });
  if (inv.sloop) { zetR("installatie", R.leidingwerk_basis); }
  if (inv.verplaatsen) { zetR("installatie", R.leiding_verplaatsen); }
  if (o.vloerverwarming) {
    zet("elektra", Math.max(R.vloerverwarming_min[0], R.vloerverwarming_m2[0] * vloer),
                   Math.max(R.vloerverwarming_min[1], R.vloerverwarming_m2[1] * vloer));
  }
  if (o.ventilator) { zetR("elektra", R.ventilator); }
  if (o.elektra) { zetR("elektra", R.elektra_extra); }

  var f = +inv.regio || 1;
  var lo = 0, hi = 0, uit = {};
  Object.keys(p).forEach(function (k) {
    var a = Math.round(p[k][0] * f / 10) * 10, b = Math.round(p[k][1] * f / 10) * 10;
    uit[k] = [a, b]; lo += a; hi += b;
  });
  return {
    vloer: r2(vloer), wand: r2(wand), tegelM2: r2(tegelM2),
    posten: uit, laag: lo, hoog: hi,
    btwLaag: Math.round(lo * R.btw / (1 + R.btw)), btwHoog: Math.round(hi * R.btw / (1 + R.btw))
  };
}
/*REKEN-EIND*/"""


def _regio_opties():
    per_prov = {}
    for p in PLAATSEN:
        per_prov.setdefault(p["provincie"], []).append(p)
    out = '<option value="1">Weet ik niet / landelijk gemiddelde</option>'
    for prov, lijst in per_prov.items():
        f = PRIJSINDEX.get(prov, 1.0)
        out += f'<optgroup label="{prov}">'
        for p in sorted(lijst, key=lambda x: x["naam"]):
            out += f'<option value="{f}">{p["naam"]}</option>'
        out += "</optgroup>"
    return out


CSS = """<style>
.kc-tool{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:22px;display:grid;gap:26px}
@media(min-width:900px){.kc-tool{grid-template-columns:1fr 1fr;padding:32px;gap:36px}}
.kc-tool fieldset{border:0;margin:0 0 18px;padding:0}
.kc-tool legend{font-weight:700;color:var(--ink);margin-bottom:8px;font-size:1rem}
.kc-rij{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.kc-rij label,.kc-veld{display:flex;flex-direction:column;font-size:.88rem;color:var(--muted);gap:4px}
.kc-tool input[type=number],.kc-tool select{width:100%;padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;color:var(--ink);background:#fff;min-width:0}
.kc-keuze{display:flex;flex-wrap:wrap;gap:8px}
.kc-keuze label{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:7px 12px;cursor:pointer;font-size:.93rem;color:var(--ink);background:#fff}
.kc-keuze input{accent-color:var(--accent)}
.kc-keuze label:has(input:checked){border-color:var(--navy);background:var(--bg-soft)}
.kc-klein{font-size:.82rem;color:var(--muted);margin:6px 0 0}
.kc-uit{background:var(--bg-soft);border-radius:var(--radius);padding:20px}
.kc-totaal{font-size:1.7rem;font-weight:800;color:var(--ink);line-height:1.2;margin:2px 0 4px}
.kc-sub{color:var(--muted);font-size:.9rem;margin:0}
.kc-grafiek{display:flex;gap:18px;align-items:center;margin:18px 0}
.kc-grafiek svg{flex:0 0 130px;width:130px;height:130px}
.kc-posten{list-style:none;margin:0;padding:0;flex:1;font-size:.9rem}
.kc-posten li{display:flex;justify-content:space-between;gap:10px;padding:5px 0;border-bottom:1px solid var(--line)}
.kc-posten li span:first-child{display:flex;align-items:center;gap:7px}
.kc-stip{width:10px;height:10px;border-radius:3px;flex:0 0 10px}
.kc-posten b{white-space:nowrap;color:var(--ink);font-weight:600}
@media(max-width:520px){.kc-grafiek{flex-direction:column;align-items:stretch}.kc-grafiek svg{margin:0 auto}}
.kc-toel{font-size:.93rem;margin:14px 0}
.kc-tabel{width:100%;border-collapse:collapse;font-size:.92rem;margin:12px 0}
.kc-tabel th,.kc-tabel td{text-align:left;padding:8px;border-bottom:1px solid var(--line);vertical-align:top}
.kc-tabel th{color:var(--ink)}
.kc-scroll{overflow-x:auto}
</style>"""


def _tool_html():
    return f"""<div class="kc-tool" data-kc>
  <form class="kc-in" onsubmit="return false">
    <fieldset>
      <legend>1. Afmetingen van de badkamer</legend>
      <div class="kc-rij">
        <label>Lengte (m)<input type="number" id="kc-l" min="0.8" max="10" step="0.1" value="2.5" inputmode="decimal"></label>
        <label>Breedte (m)<input type="number" id="kc-b" min="0.8" max="10" step="0.1" value="2" inputmode="decimal"></label>
        <label>Hoogte (m)<input type="number" id="kc-h" min="2" max="4" step="0.1" value="2.6" inputmode="decimal"></label>
      </div>
      <label class="kc-veld" style="margin-top:10px">Of vul direct de vloeroppervlakte in (m²)
        <input type="number" id="kc-m2" min="1" max="60" step="0.5" placeholder="leeg laten = lengte × breedte" inputmode="decimal"></label>
    </fieldset>
    <fieldset>
      <legend>2. Tegelwerk</legend>
      <div class="kc-keuze">
        <label><input type="radio" name="kc-tegels" value="plafond" checked> Vloer + wand tot plafond</label>
        <label><input type="radio" name="kc-tegels" value="halfhoog"> Vloer + wand halfhoog</label>
        <label><input type="radio" name="kc-tegels" value="geen"> Geen tegelwerk</label>
      </div>
    </fieldset>
    <fieldset>
      <legend>3. Niveau van sanitair en tegels</legend>
      <div class="kc-keuze">
        <label><input type="radio" name="kc-niveau" value="basis"> Basis</label>
        <label><input type="radio" name="kc-niveau" value="midden" checked> Midden</label>
        <label><input type="radio" name="kc-niveau" value="luxe"> Luxe</label>
      </div>
    </fieldset>
    <fieldset>
      <legend>4. Wat komt erin?</legend>
      <div class="kc-keuze">
        <label><input type="checkbox" name="kc-o" value="douche" checked> Inloopdouche</label>
        <label><input type="checkbox" name="kc-o" value="bad"> Bad</label>
        <label><input type="checkbox" name="kc-o" value="toilet" checked> Hangtoilet</label>
        <label><input type="checkbox" name="kc-o" value="meubel" checked> Wastafelmeubel</label>
        <label><input type="checkbox" name="kc-o" value="vloerverwarming"> Vloerverwarming</label>
        <label><input type="checkbox" name="kc-o" value="ventilator" checked> Ventilator</label>
        <label><input type="checkbox" name="kc-o" value="elektra"> Extra stopcontacten en verlichting</label>
      </div>
    </fieldset>
    <fieldset>
      <legend>5. Sloopwerk en leidingen</legend>
      <div class="kc-keuze">
        <label><input type="radio" name="kc-sloop" value="1" checked> Laten slopen</label>
        <label><input type="radio" name="kc-sloop" value="0"> Niet nodig of zelf slopen</label>
      </div>
      <div class="kc-keuze" style="margin-top:8px">
        <label><input type="radio" name="kc-verpl" value="0" checked> Indeling blijft gelijk</label>
        <label><input type="radio" name="kc-verpl" value="1"> Leidingen of afvoer verplaatsen</label>
      </div>
    </fieldset>
    <fieldset>
      <legend>6. Waar woon je?</legend>
      <select id="kc-regio" aria-label="Plaats">{_regio_opties()}</select>
      <p class="kc-klein">De arbeidskosten verschillen per regio. We corrigeren met een schatting per provincie.</p>
    </fieldset>
  </form>
  <div class="kc-uit" aria-live="polite">
    <p class="kc-sub">Richtprijs voor jouw badkamer, inclusief 21% btw</p>
    <p class="kc-totaal" data-kc-totaal>–</p>
    <p class="kc-sub" data-kc-btw></p>
    <div class="kc-grafiek">
      <svg viewBox="0 0 42 42" role="img" aria-label="Verdeling van de kosten per post" data-kc-donut></svg>
      <ul class="kc-posten" data-kc-posten></ul>
    </div>
    <p class="kc-toel" data-kc-toel></p>
    <a class="btn btn-primary btn-lg" href="/offerte-aanvragen/" style="width:100%;text-align:center">Vergelijk offertes</a>
    <p class="kc-klein">Gratis en vrijblijvend: je ontvangt offertes van maximaal drie badkamerspecialisten uit je regio.</p>
  </div>
</div>"""


UI_JS = r"""
(function () {
  var R = __REKENWAARDEN__;
  var NAMEN = __POSTEN__;
  var KLEUR = ["#0b4a56", "#24606b", "#5f9aa3", "#c4511f", "#e08a5f", "#0f8a5f", "#9fb4b8"];
  var root = document.querySelector("[data-kc]");
  if (!root) { return; }
  function $(s) { return root.querySelector(s); }
  function waarde(naam) { var el = root.querySelector('input[name="' + naam + '"]:checked'); return el ? el.value : ""; }
  function eur(n) { return "€" + Math.round(n).toLocaleString("nl-NL"); }
  function getal(id) { var v = $(id).value.replace(",", "."); return v === "" ? 0 : parseFloat(v); }

  function lees() {
    var o = {};
    root.querySelectorAll('input[name="kc-o"]').forEach(function (c) { o[c.value] = c.checked; });
    return {
      lengte: getal("#kc-l"), breedte: getal("#kc-b"), hoogte: getal("#kc-h") || 2.6,
      m2: getal("#kc-m2"), tegels: waarde("kc-tegels"), niveau: waarde("kc-niveau"),
      onderdelen: o, sloop: waarde("kc-sloop") === "1", verplaatsen: waarde("kc-verpl") === "1",
      regio: parseFloat($("#kc-regio").value) || 1
    };
  }

  function donut(res) {
    var tot = 0, d = [];
    NAMEN.forEach(function (n, i) {
      var p = res.posten[n[0]] || [0, 0], m = (p[0] + p[1]) / 2;
      d.push([m, KLEUR[i]]); tot += m;
    });
    var svg = '<circle cx="21" cy="21" r="15.915" fill="none" stroke="#d9e5e7" stroke-width="7"></circle>';
    var start = 25;
    if (tot > 0) {
      d.forEach(function (x) {
        if (x[0] <= 0) { return; }
        var pct = x[0] / tot * 100;
        svg += '<circle cx="21" cy="21" r="15.915" fill="none" stroke="' + x[1] + '" stroke-width="7" stroke-dasharray="' +
          pct.toFixed(2) + ' ' + (100 - pct).toFixed(2) + '" stroke-dashoffset="' + start.toFixed(2) + '"></circle>';
        start = (start - pct + 100) % 100;
      });
    }
    return svg;
  }

  function toon() {
    var inv = lees();
    var res = berekenBadkamer(inv, R);
    if (res.vloer <= 0) {
      $("[data-kc-totaal]").textContent = "Vul de afmetingen in";
      $("[data-kc-btw]").textContent = ""; $("[data-kc-posten]").innerHTML = "";
      $("[data-kc-donut]").innerHTML = donut({ posten: {} }); $("[data-kc-toel]").textContent = "";
      return;
    }
    $("[data-kc-totaal]").textContent = eur(res.laag) + " – " + eur(res.hoog);
    $("[data-kc-btw]").textContent = "Waarvan btw: " + eur(res.btwLaag) + " – " + eur(res.btwHoog) +
      ". Excl. btw: " + eur(res.laag - res.btwLaag) + " – " + eur(res.hoog - res.btwHoog) + ".";
    var li = "";
    NAMEN.forEach(function (n, i) {
      var p = res.posten[n[0]] || [0, 0];
      li += '<li><span><i class="kc-stip" style="background:' + KLEUR[i] + '"></i>' + n[1] + '</span><b>' +
        (p[1] > 0 ? eur(p[0]) + " – " + eur(p[1]) : "–") + '</b></li>';
    });
    $("[data-kc-posten]").innerHTML = li;
    $("[data-kc-donut]").innerHTML = donut(res);
    var t = "Gerekend met " + res.vloer.toLocaleString("nl-NL") + " m² vloer";
    t += res.tegelM2 > 0 ? " en ongeveer " + Math.round(res.tegelM2) + " m² tegelwerk." : " en geen tegelwerk.";
    if (inv.verplaatsen) { t += " Het verplaatsen van leidingen is de onzekerste post: vraag de specialist om een vaste prijs."; }
    else { t += " De grootste besparing zit vaak in het gelijk laten van de indeling."; }
    if (!inv.sloop) { t += " Zelf slopen? Doe dat niet als er mogelijk asbest in zit."; }
    if (inv.regio !== 1) { t += " Prijzen zijn gecorrigeerd voor je regio (factor " + inv.regio.toLocaleString("nl-NL") + ")."; }
    $("[data-kc-toel]").textContent = t;
  }

  root.addEventListener("input", toon);
  root.addEventListener("change", toon);
  toon();
})();
"""


def _js():
    ui = (UI_JS.replace("__REKENWAARDEN__", json.dumps(REKENWAARDEN))
               .replace("__POSTEN__", json.dumps(POSTEN, ensure_ascii=False)))
    return "<script>\n" + REKEN_JS + "\n" + ui + "</script>"


def _eur(n):
    return f"€{n:,}".replace(",", ".")


def _r(r, eenheid=""):
    return f"{_eur(r[0])} – {_eur(r[1])}{eenheid}"


def _methode_html():
    R = REKENWAARDEN
    s = R["sanitair"]
    rijen = [
        ("Sloopwerk", f"{_r(R['sloop_vast'])} vast plus {_r(R['sloop_m2'], ' per m² vloer')}", "Werkspot, Slimster"),
        ("Tegels (materiaal)", f"basis {_r(R['tegel_materiaal']['basis'])}, midden {_r(R['tegel_materiaal']['midden'])}, luxe {_r(R['tegel_materiaal']['luxe'])} per m²", "Werkspot"),
        ("Tegelzetten", f"{_r(R['tegel_arbeid'], ' per m²')} inclusief lijm, voeg en kit; plus {_r(R['waterdicht'])} voor waterdicht maken bij een douche of bad", "Trustoo, Homedeal"),
        ("Sanitair (midden)", f"douche {_r(s['douche']['midden'])}, bad {_r(s['bad']['midden'])}, hangtoilet {_r(s['toilet']['midden'])}, wastafelmeubel {_r(s['meubel']['midden'])}", "Homedeal, Werkspot"),
        ("Installatie", f"montage per onderdeel {_eur(min(v[0] for v in R['montage'].values()))} – {_eur(max(v[1] for v in R['montage'].values()))}; leidingwerk vernieuwen {_r(R['leidingwerk_basis'])}; verplaatsen {_r(R['leiding_verplaatsen'])}", "Trustoo, Slimster, Homedeal, Werkspot"),
        ("Elektra", f"vloerverwarming {_r(R['vloerverwarming_m2'], ' per m²')} (minimaal {_eur(R['vloerverwarming_min'][0])}); ventilator {_r(R['ventilator'])}; stopcontacten en verlichting {_r(R['elektra_extra'])}", "Werkspot, Slimster, Trustoo"),
        ("Afvoer van afval", f"met sloop {_r(R['afval_sloop'])}; zelf een container huren {_r(R['afval_zelf'])}", "Werkspot, Slimster, Trustoo"),
    ]
    tr = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rijen)
    return f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Zo rekent de calculator</h2>
  <p>De calculator telt per post een lage en een hoge richtprijs op. Alle bedragen zijn inclusief 21% btw: dat is het tarief voor een nieuwe badkamer, voor zowel het werk als het materiaal.</p>
  <ul>
    <li><strong>Tegelwerk:</strong> vloer (lengte × breedte) plus wanden (omtrek × hoogte, min de deur). Bij halfhoog rekenen we met {str(R['halfhoog_m']).replace('.', ',')} meter wandhoogte.</li>
    <li><strong>Sanitair:</strong> per gekozen onderdeel de productprijs voor het gekozen niveau, plus de montage door de installateur.</li>
    <li><strong>Regio:</strong> het totaal wordt gecorrigeerd met een schatting per provincie, van 0,95 in Overijssel tot 1,13 in Noord-Holland.</li>
  </ul>
  <div class="kc-scroll"><table class="kc-tabel">
    <thead><tr><th>Post</th><th>Rekenwaarde (incl. btw)</th><th>Bron</th></tr></thead>
    <tbody>{tr}</tbody>
  </table></div>
  <h3>Wat er niet in zit</h3>
  <p>Een nieuw plafond, stucwerk, een nieuwe deur, asbestsanering, het herstellen van een rotte vloer of een nieuwe dekvloer. Die posten zie je pas na een opname of na het slopen. Houd daarom 10 tot 15 procent extra achter de hand. Wil je weten hoe een complete badkamer is opgebouwd, lees dan <a href="/kosten/nieuwe-badkamer/">wat een nieuwe badkamer kost</a>.</p>
  <p class="kc-klein">Bronnen (geraadpleegd november 2026):
    Werkspot (slopen),
    Slimster (slopen),
    Werkspot (puin afvoeren),
    Werkspot (betegelen),
    Trustoo (tegelzetter),
    Homedeal (badkamer verbouwen),
    Werkspot (sanitair plaatsen),
    Trustoo (nieuwe badkamer),
    Slimster (nieuwe badkamer),
    Werkspot (vloerverwarming),
    Werkspot (stopcontacten).
    Het zijn richtprijzen, geen offerte.</p>
</div></section>"""


FAQS = [
    ("Hoe nauwkeurig is de badkamercalculator?",
     "De uitkomst is een richtprijs met een bandbreedte. Hij laat zien in welke orde van grootte je moet denken. De echte prijs hangt af van wat er na het slopen tevoorschijn komt, de tegels en het sanitair die je precies kiest en de planning van de specialist. Een offerte na een opname is altijd nauwkeuriger."),
    ("Is de prijs inclusief btw?",
     "Ja. Alle bedragen zijn inclusief 21% btw. Dat tarief geldt voor een nieuwe badkamer, voor zowel het werk als het sanitair en de tegels. De calculator laat het btw-deel apart zien."),
    ("Waarom is het verplaatsen van leidingen zo duur?",
     "Een afvoer heeft afschot nodig en moet aansluiten op de standleiding. Vaak moet de vloer of een wand open, en soms moet de vloer omhoog. Dat kost uren van de loodgieter en extra materiaal. Laat je toilet en douche op hun plek, dan scheelt dat al snel duizend euro of meer."),
    ("Wat is het verschil tussen basis, midden en luxe?",
     "Bij basis gaat het om eenvoudige, degelijke producten en standaardtegels. Midden is bijvoorbeeld een thermostaatkraan, een hangtoilet met softclose en grotere tegels. Bij luxe horen inbouwkranen, een regendouche, groot formaat tegels of natuursteen. Het niveau bepaalt vooral de posten sanitair en tegels."),
    ("Kan ik besparen door zelf te slopen?",
     "Ja, sloopwerk scheelt een paar honderd euro. Overleg het wel eerst met de specialist en sloop niet als de badkamer van voor 1994 is en er mogelijk asbest in zit, bijvoorbeeld in kit, vloerzeil of plaatmateriaal. Laat dat eerst onderzoeken."),
]


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Badkamercalculator", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over de badkamercalculator")
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Badkamercalculator",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsers",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Bereken wat een nieuwe badkamer ongeveer kost, per post en inclusief 21% btw.",
    }
    body = f"""{cr}
{CSS}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:24px">
    <span class="badge">Gratis tool</span>
    <h1>Badkamercalculator: wat kost jouw nieuwe badkamer?</h1>
    <p class="lead">Vul de maten van je badkamer in en kies wat erin moet. Je ziet direct een richtprijs per post, van sloopwerk tot sanitair, met een lage en een hoge schatting inclusief 21% btw.</p>
  </div>
  {_tool_html()}
</div></section>
{_methode_html()}
{faq_html}
{cta_blok("Weet je nu ongeveer wat het kost?", "Een richtprijs is een startpunt. Een badkamerspecialist die bij je thuis komt kijken, kan een echte prijs geven. Vraag gratis offertes aan bij maximaal drie specialisten uit je regio.", "Vergelijk offertes")}
{_js()}"""
    write(PAD, page(
        title("Badkamercalculator: kosten nieuwe badkamer"),
        desc("Bereken gratis wat je nieuwe badkamer ongeveer kost.",
             "Per post een richtprijs voor sloop, tegels, sanitair en installatie, incl. 21% btw."),
        PAD, body, jsonld=[cr_ld, app_ld, faq_ld]), prio=0.7)
