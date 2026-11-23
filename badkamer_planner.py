# -*- coding: utf-8 -*-
"""Renovatieplanner: hoelang duurt je badkamerrenovatie? (/tools/renovatieplanner/)

Losse module met de interface LINKS + build(write). De planning wordt in de
browser gemaakt uit de constante FASEN hieronder (json.dumps naar de JavaScript).

Duur per fase in werkdagen (ma – vr, zonder vaste feestdagen). Alleen de
droogtijd van de dekvloer telt in kalenderdagen, want een vloer droogt ook in
het weekend.

Bronnen en onderbouwing, geraadpleegd in november 2026:
- Droogtijd zandcementdekvloer: vuistregel ongeveer 1 week per centimeter dikte
  (Gamma klusadvies; Hornbach: 6 cm is circa 6 weken). Beloopbaar na 2 – 3 dagen.
  https://www.gamma.nl/klusadvies/a/zandcement-dekvloer-maken
  https://www.werkspot.nl/vloeren-tegels/artikelen/tips-voor-een-cement-dekvloer-storten
- Sneldrogende cementgebonden dekvloeren zijn volgens de productbladen van fabrikanten
  meestal na 1 tot 3 dagen betegelbaar; we rekenen 1 dag storten + 3 kalenderdagen drogen.
- Totale duur complete badkamer: twee tot vier weken werk in huis (data.DIENSTEN,
  "badkamer-renoveren", FAQ). Tegelzetter 8 – 10 m² per dag (Trustoo/Homedeal, zie data.py).
- Levertijd sanitair en tegels: drie tot zes weken is gebruikelijk; we rekenen met
  vier weken voor een complete badkamer (eigen schatting, brede marge, staat als tip in de tool).
"""

import json

from components import page, crumbs, faq_blok, cta_blok, title, desc

PAD = "/tools/renovatieplanner/"

LINKS = [
    (PAD, "Renovatieplanner",
     "Zie in welke volgorde je badkamer wordt verbouwd en wanneer hij klaar is."),
]

# Typen klus
KLUSSEN = [
    ("compleet", "Complete renovatie"),
    ("douche", "Alleen de douche"),
    ("toilet", "Toiletruimte"),
    ("tegels", "Alleen tegelwerk"),
]

# Fasen in vaste volgorde. dagen = werkdagen per type klus (0 = fase vervalt).
# 'wie': specialist, leverancier of droogtijd.
FASEN = [
    {"id": "voorbereiding", "naam": "Voorbereiding, bestellen en levertijd", "wie": "leverancier",
     "dagen": {"compleet": 20, "douche": 15, "toilet": 10, "tegels": 10},
     "tip": "Kies sanitair en tegels voordat de sloop begint en laat alles leveren vóór de eerste werkdag. Een onderdeel dat later komt, legt de hele planning stil."},
    {"id": "slopen", "naam": "Slopen en afvoeren", "wie": "specialist",
     "dagen": {"compleet": 2, "douche": 1, "toilet": 1, "tegels": 2},
     "tip": "Is je badkamer van voor 1994? Laat dan eerst onderzoeken of er asbest in zit, bijvoorbeeld in kit, vloerzeil of plaatmateriaal."},
    {"id": "leidingwerk", "naam": "Leidingwerk en elektra", "wie": "specialist",
     "dagen": {"compleet": 3, "douche": 2, "toilet": 1, "tegels": 0},
     "tip": "Maak foto's met een duimstok erbij van alle leidingen voordat ze worden weggewerkt. Dan weet je later waar je niet moet boren."},
    {"id": "dekvloer", "naam": "Dekvloer en droogtijd", "wie": "droogtijd",
     "dagen": {"compleet": 1, "douche": 1, "toilet": 0, "tegels": 0},
     "tip": "De droogtijd telt door in het weekend. Tegel nooit op een vloer die nog te nat is: dan kunnen tegels later loslaten of gaan de voegen scheuren."},
    {"id": "waterdicht", "naam": "Waterdicht maken", "wie": "specialist",
     "dagen": {"compleet": 2, "douche": 1, "toilet": 0, "tegels": 1},
     "tip": "Vraag welk systeem de specialist gebruikt en of de hoeken en doorvoeren met band worden afgedicht. Dit zie je straks niet meer."},
    {"id": "tegelen", "naam": "Tegelen", "wie": "specialist",
     "dagen": {"compleet": 5, "douche": 3, "toilet": 2, "tegels": 4},
     "tip": "Controleer op de eerste tegeldag of de tegels en het legpatroon kloppen. Groot formaat tegels kost meer tijd per vierkante meter."},
    {"id": "voegen", "naam": "Voegen en kitten", "wie": "specialist",
     "dagen": {"compleet": 2, "douche": 1, "toilet": 1, "tegels": 1},
     "tip": "Kit komt pas als de voegen droog zijn. Douche daarna minstens 24 uur niet, zodat de kit kan uitharden."},
    {"id": "sanitair", "naam": "Sanitair monteren", "wie": "specialist",
     "dagen": {"compleet": 2, "douche": 1, "toilet": 1, "tegels": 1},
     "tip": "Laat bij de montage een lektest doen van alle aansluitingen en van de afvoer, en kijk zelf mee."},
    {"id": "afwerking", "naam": "Afwerking en oplevering", "wie": "specialist",
     "dagen": {"compleet": 2, "douche": 1, "toilet": 1, "tegels": 1},
     "tip": "Loop bij de oplevering alles samen na en zet kleine punten op een lijst. Spreek af wanneer die worden opgelost en vraag de garantie op papier."},
]

DEKVLOER = {
    # kalenderdagen droogtijd na het storten
    "snel": {"naam": "Sneldrogende dekvloer", "droog": 3},
    "zandcement": {"naam": "Zandcement, ca. 5 cm (1 week per cm)", "droog": 35},
    "geen": {"naam": "Geen nieuwe dekvloer", "droog": 0},
}

PLAN_JS = r"""/*PLAN-START*/
function pasen(j) {
  var a = j % 19, b = Math.floor(j / 100), c = j % 100, d = Math.floor(b / 4), e = b % 4,
      f = Math.floor((b + 8) / 25), g = Math.floor((b - f + 1) / 3), h = (19 * a + b - d - g + 15) % 30,
      i = Math.floor(c / 4), k = c % 4, l = (32 + 2 * e + 2 * i - h - k) % 7, m = Math.floor((a + 11 * h + 22 * l) / 451),
      maand = Math.floor((h + l - 7 * m + 114) / 31), dag = ((h + l - 7 * m + 114) % 31) + 1;
  return new Date(j, maand - 1, dag);
}
function sleutel(d) { return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(); }
var _fd = {};
function feestdagen(j) {
  if (_fd[j]) { return _fd[j]; }
  var p = pasen(j), s = {};
  function plus(n) { var x = new Date(p); x.setDate(x.getDate() + n); s[sleutel(x)] = 1; }
  plus(1); plus(39); plus(50);
  s[j + "-1-1"] = 1; s[j + "-12-25"] = 1; s[j + "-12-26"] = 1;
  var kd = new Date(j, 3, 27); if (kd.getDay() === 0) { kd.setDate(26); }
  s[sleutel(kd)] = 1;
  if (j % 5 === 0) { s[j + "-5-5"] = 1; }
  _fd[j] = s; return s;
}
function isWerkdag(d) { var w = d.getDay(); return w !== 0 && w !== 6 && !feestdagen(d.getFullYear())[sleutel(d)]; }
function volgendeWerkdag(d) { var x = new Date(d); while (!isWerkdag(x)) { x.setDate(x.getDate() + 1); } return x; }
function plusWerkdagen(d, n) {
  var x = volgendeWerkdag(d), t = 1;
  while (t < n) { x.setDate(x.getDate() + 1); if (isWerkdag(x)) { t++; } }
  return x;
}
function maakPlanning(inv, FASEN, DEKVLOER) {
  var cur = new Date(inv.start), uit = [], werk = 0, slopenStart = null, sanitairEind = null;
  FASEN.forEach(function (f) {
    var n = f.dagen[inv.klus] || 0;
    if (f.id === "dekvloer" && inv.dekvloer === "geen") { n = 0; }
    if (n <= 0) { return; }
    var zelf = (f.id === "slopen" && inv.zelfSlopen);
    if (zelf) { n = n + 1; }
    var begin = volgendeWerkdag(cur), eind = plusWerkdagen(begin, n), droog = 0;
    if (f.id === "dekvloer") {
      droog = DEKVLOER[inv.dekvloer].droog;
      eind = new Date(eind); eind.setDate(eind.getDate() + droog);
    }
    if (f.id !== "voorbereiding") { werk += n; }
    if (f.id === "slopen") { slopenStart = begin; }
    if (f.id === "sanitair") { sanitairEind = eind; }
    uit.push({ id: f.id, naam: f.naam, wie: zelf ? "zelf" : f.wie, begin: begin, eind: eind, werkdagen: n, droog: droog, tip: f.tip });
    cur = new Date(eind); cur.setDate(cur.getDate() + 1);
  });
  var start = uit.length ? uit[0].begin : new Date(inv.start), einde = uit.length ? uit[uit.length - 1].eind : start;
  var zonder = (slopenStart && sanitairEind) ? Math.round((sanitairEind - slopenStart) / 864e5) + 1 : 0;
  return { fasen: uit, start: start, einde: einde, werkdagenInHuis: werk,
           kalenderdagen: Math.round((einde - start) / 864e5) + 1, dagenZonder: zonder,
           eersteDagInHuis: slopenStart };
}
/*PLAN-EIND*/"""

UI_JS = r"""
(function () {
  var FASEN = __FASEN__, DEKVLOER = __DEKVLOER__;
  var root = document.querySelector("[data-rp]");
  if (!root) { return; }
  function $(s) { return root.querySelector(s); }
  function keuze(n) { var e = root.querySelector('input[name="' + n + '"]:checked'); return e ? e.value : ""; }
  var MND = ["jan", "feb", "mrt", "apr", "mei", "jun", "jul", "aug", "sep", "okt", "nov", "dec"];
  var DAG = ["zo", "ma", "di", "wo", "do", "vr", "za"];
  function dt(d) { return DAG[d.getDay()] + " " + d.getDate() + " " + MND[d.getMonth()]; }
  function dtl(d) { return d.getDate() + " " + MND[d.getMonth()] + " " + d.getFullYear(); }
  var nu = new Date(); nu.setDate(nu.getDate() + 7);
  var inp = $("#rp-start");
  inp.value = nu.getFullYear() + "-" + String(nu.getMonth() + 1).padStart(2, "0") + "-" + String(nu.getDate()).padStart(2, "0");
  var WIE = { leverancier: "Bestellen", specialist: "Specialist", droogtijd: "Droogtijd", zelf: "Zelf" };

  function toon() {
    var klus = keuze("rp-klus");
    var dekBlok = $("[data-rp-dek]");
    dekBlok.hidden = (klus === "toilet" || klus === "tegels");
    var w = inp.value.split("-");
    if (w.length !== 3) { return; }
    var inv = { klus: klus, start: new Date(+w[0], +w[1] - 1, +w[2]), zelfSlopen: keuze("rp-zelf") === "1",
                tweede: keuze("rp-tweede") === "1", dekvloer: dekBlok.hidden ? "geen" : keuze("rp-dek") };
    var p = maakPlanning(inv, FASEN, DEKVLOER);
    var totaal = p.kalenderdagen, html = "";
    p.fasen.forEach(function (f) {
      var off = Math.round((f.begin - p.start) / 864e5), len = Math.round((f.eind - f.begin) / 864e5) + 1;
      var l = off / totaal * 100, b = Math.max(len / totaal * 100, 1.5);
      var duur = f.werkdagen + (f.werkdagen === 1 ? " werkdag" : " werkdagen") + (f.droog ? " + " + f.droog + " dagen drogen" : "");
      html += '<li class="rp-fase rp-' + f.wie + '"><div class="rp-kop"><strong>' + f.naam + '</strong><span>' + dt(f.begin) +
        (len > 1 ? " – " + dt(f.eind) : "") + " · " + duur + ' · <em>' + WIE[f.wie] + '</em></span></div>' +
        '<div class="rp-baan" aria-hidden="true"><span style="margin-left:' + l.toFixed(2) + '%;width:' + b.toFixed(2) + '%"></span></div>' +
        '<p class="rp-tip">' + f.tip + '</p></li>';
    });
    $("[data-rp-lijst]").innerHTML = html;
    $("[data-rp-eind]").textContent = dtl(p.einde);
    $("[data-rp-werk]").textContent = p.werkdagenInHuis + " werkdagen";
    $("[data-rp-dag1]").textContent = p.eersteDagInHuis ? dtl(p.eersteDagInHuis) : "–";
    var mis = klus === "toilet" ? "toilet" : (klus === "compleet" ? "badkamer" : "douche");
    var t;
    if (inv.tweede) {
      t = "Je hebt nog een tweede " + (klus === "toilet" ? "toilet" : "douche") + " in huis. Dan kun je tijdens de verbouwing gewoon thuis blijven wonen.";
    } else {
      t = "Let op: je zit ongeveer " + p.dagenZonder + " dagen zonder " + mis + ". ";
      t += klus === "toilet" ? "Vraag of de specialist het toilet aan het eind van elke werkdag tijdelijk kan aansluiten."
         : "Regel een plek om te douchen, bijvoorbeeld bij familie of de sportschool, of vraag naar een tijdelijke douche.";
    }
    if (inv.zelfSlopen) { t += " Je sloopt zelf: zorg dat het klaar is vóór de eerste dag van de specialist."; }
    if (inv.dekvloer === "zandcement") { t += " Een gewone zandcementvloer droogt ongeveer een week per centimeter. Vraag of een sneldrogende vloer kan."; }
    $("[data-rp-let]").textContent = t;
  }
  root.addEventListener("input", toon);
  root.addEventListener("change", toon);
  toon();
})();
"""

CSS = """<style>
.rp-tool{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:22px}
@media(min-width:900px){.rp-tool{padding:32px}}
.rp-in{display:grid;gap:18px;margin-bottom:26px}
@media(min-width:900px){.rp-in{grid-template-columns:1fr 1fr}}
.rp-tool fieldset{border:0;margin:0;padding:0}
.rp-tool legend{font-weight:700;color:var(--ink);margin-bottom:8px}
.rp-keuze{display:flex;flex-wrap:wrap;gap:8px}
.rp-keuze label{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:7px 12px;cursor:pointer;font-size:.93rem;color:var(--ink)}
.rp-keuze input{accent-color:var(--accent)}
.rp-keuze label:has(input:checked){border-color:var(--navy);background:var(--bg-soft)}
.rp-tool input[type=date]{padding:10px;border:1px solid var(--line);border-radius:8px;font:inherit;color:var(--ink);max-width:100%}
.rp-sam{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:14px}
.rp-sam div{background:var(--bg-soft);border-radius:var(--radius);padding:14px}
.rp-sam small{display:block;color:var(--muted);font-size:.82rem}
.rp-sam b{font-size:1.15rem;color:var(--ink)}
.rp-let{background:var(--accent-soft);border-radius:var(--radius);padding:12px 14px;font-size:.93rem;margin:0 0 18px}
.rp-lijst{list-style:none;margin:0;padding:0}
.rp-fase{padding:12px 0;border-bottom:1px solid var(--line)}
.rp-kop{display:flex;flex-wrap:wrap;justify-content:space-between;gap:4px 12px}
.rp-kop strong{color:var(--ink)}
.rp-kop span{font-size:.86rem;color:var(--muted)}
.rp-kop em{font-style:normal;font-weight:600}
.rp-baan{position:relative;height:12px;background:var(--bg-soft);border-radius:6px;margin:8px 0;overflow:hidden}
.rp-baan span{display:block;height:100%;border-radius:6px;background:var(--navy)}
.rp-leverancier .rp-baan span{background:#9fb4b8}
.rp-droogtijd .rp-baan span{background:repeating-linear-gradient(45deg,#5f9aa3 0 6px,#8fbcc2 6px 12px)}
.rp-zelf .rp-baan span{background:var(--accent)}
.rp-tip{font-size:.88rem;margin:0;color:var(--body)}
.rp-leg{display:flex;flex-wrap:wrap;gap:14px;font-size:.82rem;color:var(--muted);margin:0 0 6px}
.rp-leg i{display:inline-block;width:12px;height:12px;border-radius:3px;vertical-align:-2px;margin-right:5px}
</style>"""


def _tool_html():
    klussen = "".join(
        f'<label><input type="radio" name="rp-klus" value="{k}"{" checked" if i == 0 else ""}> {n}</label>'
        for i, (k, n) in enumerate(KLUSSEN))
    dek = "".join(
        f'<label><input type="radio" name="rp-dek" value="{k}"{" checked" if k == "snel" else ""}> {v["naam"]}</label>'
        for k, v in DEKVLOER.items())
    return f"""<div class="rp-tool" data-rp>
  <form class="rp-in" onsubmit="return false">
    <fieldset><legend>1. Wat ga je verbouwen?</legend><div class="rp-keuze">{klussen}</div></fieldset>
    <fieldset><legend>2. Wanneer begin je?</legend>
      <label style="font-size:.88rem;color:var(--muted)">Startdatum: de dag dat je de opdracht geeft en gaat bestellen<br>
      <input type="date" id="rp-start"></label></fieldset>
    <fieldset><legend>3. Sloop je zelf?</legend><div class="rp-keuze">
      <label><input type="radio" name="rp-zelf" value="0" checked> Nee, de specialist sloopt</label>
      <label><input type="radio" name="rp-zelf" value="1"> Ja, ik sloop zelf</label></div></fieldset>
    <fieldset><legend>4. Is er een tweede toilet of douche in huis?</legend><div class="rp-keuze">
      <label><input type="radio" name="rp-tweede" value="1"> Ja</label>
      <label><input type="radio" name="rp-tweede" value="0" checked> Nee</label></div></fieldset>
    <fieldset data-rp-dek><legend>5. Soort dekvloer</legend><div class="rp-keuze">{dek}</div></fieldset>
  </form>
  <div aria-live="polite">
    <div class="rp-sam">
      <div><small>Eerste werkdag in huis</small><b data-rp-dag1>–</b></div>
      <div><small>Werkdagen in huis</small><b data-rp-werk>–</b></div>
      <div><small>Verwachte einddatum</small><b data-rp-eind>–</b></div>
    </div>
    <p class="rp-let" data-rp-let></p>
    <p class="rp-leg"><span><i style="background:#9fb4b8"></i>Bestellen en levertijd</span><span><i style="background:var(--navy)"></i>Specialist aan het werk</span><span><i style="background:#5f9aa3"></i>Droogtijd</span><span><i style="background:var(--accent)"></i>Zelf slopen</span></p>
    <ol class="rp-lijst" data-rp-lijst></ol>
    <p style="margin:18px 0 0;font-size:.85rem;color:var(--muted)">Werkdagen zijn maandag tot en met vrijdag, zonder de vaste feestdagen. Bouwvak, vakanties en de agenda van de specialist zijn niet meegerekend.</p>
    <a class="btn btn-primary btn-lg" href="/offerte-aanvragen/" style="margin-top:16px">Vraag offertes en een planning aan</a>
  </div>
</div>"""


def _js():
    ui = (UI_JS.replace("__FASEN__", json.dumps(FASEN, ensure_ascii=False))
               .replace("__DEKVLOER__", json.dumps(DEKVLOER, ensure_ascii=False)))
    return "<script>\n" + PLAN_JS + "\n" + ui + "</script>"


def _uitleg_html():
    rijen = "".join(
        f"<tr><td>{f['naam']}</td>"
        + "".join(f"<td>{f['dagen'][k] or '–'}</td>" for k, _ in KLUSSEN) + "</tr>"
        for f in FASEN)
    kop = "".join(f"<th>{n}</th>" for _, n in KLUSSEN)
    return f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Waarom deze volgorde?</h2>
  <p>Een badkamer wordt van grof naar fijn gebouwd. Eerst gaat alles eruit, dan komen de leidingen die later in de muur en de vloer verdwijnen. Daarna volgt de dekvloer met afschot naar de afvoer, die moet drogen voordat de vloer waterdicht kan worden gemaakt. Pas dan wordt er getegeld, gevoegd en gekit, en als laatste komt het sanitair. Wie die volgorde omdraait, moet later dingen weer openbreken. Meer uitleg per stap lees je in <a href="/kennisbank/volgorde-badkamerrenovatie/">de volgorde van een badkamerrenovatie</a>.</p>
  <h3>De droogtijd van de dekvloer</h3>
  <p>Een gewone zandcementdekvloer droogt volgens de gangbare vuistregel ongeveer <strong>een week per centimeter dikte</strong>. Een badkamervloer met afschot is al snel 5 centimeter, dus dan wacht je zo'n vijf weken. Daarom kiezen veel specialisten in de badkamer voor een sneldrogende dekvloer, die volgens de fabrikanten vaak na één tot drie dagen betegelbaar is. Vraag welke vloer de specialist gebruikt en hoe hij het vochtgehalte meet voordat hij gaat tegelen.</p>
  <h3>Rekenwaarden per fase (werkdagen)</h3>
  <div style="overflow-x:auto"><table class="kc-tabel" style="width:100%;border-collapse:collapse;font-size:.9rem">
    <thead><tr><th style="text-align:left">Fase</th>{kop}</tr></thead><tbody>{rijen}</tbody></table></div>
  <p style="font-size:.85rem;color:var(--muted)">Bij de dekvloer komt de droogtijd er in kalenderdagen bij. Zelf slopen rekenen we als één dag extra. Bronnen: Gamma en Werkspot (droogtijd zandcementdekvloer, november 2026), productbladen van sneldrogende dekvloeren, en de gangbare duur van twee tot vier weken werk voor een complete badkamer. Het is een richtplanning, geen toezegging.</p>
</div></section>
<style>.kc-tabel th,.kc-tabel td{{padding:7px;border-bottom:1px solid var(--line);text-align:left}}</style>"""


FAQS = [
    ("Hoelang duurt een complete badkamerrenovatie?",
     "Reken op twee tot vier weken werk in huis. Daarvoor zitten meestal nog een paar weken voor het kiezen en bestellen van sanitair en tegels. Een gewone zandcementdekvloer kan er nog een paar weken droogtijd bij doen."),
    ("Kan ik thuis blijven wonen tijdens de verbouwing?",
     "Meestal wel. Het lastigste is dat je een tijd geen douche of toilet hebt. Heb je geen tweede toilet, vraag dan of de specialist het oude toilet zo lang mogelijk laat staan of het aan het eind van de dag tijdelijk aansluit."),
    ("Waarom duurt de levertijd zo lang?",
     "Tegels en sanitair liggen niet altijd op voorraad, zeker niet bij bijzondere maten of kleuren. Drie tot zes weken is normaal. Bestel daarom alles voordat de sloop begint."),
    ("Waarom moet de dekvloer zo lang drogen?",
     "Er zit veel water in een verse zandcementvloer. Tegel je te vroeg, dan kan dat vocht niet weg. Dan laten tegels los of scheuren de voegen. De vuistregel is ongeveer een week droogtijd per centimeter dikte. Een sneldrogende vloer is sneller klaar."),
    ("Wat als de planning uitloopt?",
     "Spreek vooraf een planning per dag af en leg vast wat er gebeurt als het uitloopt. Vaak komt vertraging door een onderdeel dat niet op tijd is, of door iets wat pas bij het slopen zichtbaar wordt, zoals een rotte vloer of oude leidingen."),
]


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Renovatieplanner", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over de planning")
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Renovatieplanner badkamer",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsers",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Maak een planning voor je badkamerrenovatie met de fasen, de werkdagen en de verwachte einddatum.",
    }
    body = f"""{cr}
{CSS}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:24px">
    <span class="badge">Gratis tool</span>
    <h1>Renovatieplanner: hoelang duurt je badkamerrenovatie?</h1>
    <p class="lead">Kies wat je gaat verbouwen en wanneer je begint. Je ziet de fasen in de juiste volgorde, hoeveel werkdagen de specialist in huis is en wanneer je badkamer naar verwachting klaar is.</p>
  </div>
  {_tool_html()}
</div></section>
{_uitleg_html()}
{faq_html}
{cta_blok("Wil je een planning die op jouw badkamer klopt?", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Vraag ze er meteen een planning per dag bij.", "Gratis offertes aanvragen")}
{_js()}"""
    write(PAD, page(
        title("Renovatieplanner badkamer: planning en duur"),
        desc("Maak gratis een planning voor je badkamerrenovatie.",
             "Zie de fasen in de juiste volgorde, de droogtijd van de dekvloer, de werkdagen en de verwachte einddatum."),
        PAD, body, jsonld=[cr_ld, app_ld, faq_ld]), prio=0.7)
