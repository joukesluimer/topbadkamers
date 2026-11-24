# -*- coding: utf-8 -*-
"""JavaScript voor de indelingsplanner (/tools/indelingsplanner/), gebruikt door badkamer_indeling.py.

LOGIC_JS bevat alleen rekenwerk (botsingen, vrije ruimte, oppervlakken, kosten, tekst) en is los
te testen met node (zie de module.exports onderaan LOGIC_JS). UI_JS tekent de SVG en regelt
slepen, toetsenbord, opslaan als afbeelding en het meenemen naar de aanvraag.

Afspraken over coördinaten: alles in centimeters. (0,0) is de linkerbovenhoek van de ruimte
zoals op de tekening; x loopt naar rechts (breedte), y naar beneden (diepte).
Een element heeft een eigen breedte w (langs de muur) en diepte d (van de muur af).
rot 0: rug tegen de bovenwand, voorkant naar beneden; rot 90: rug tegen de rechterwand;
rot 180: rug tegen de onderwand; rot 270: rug tegen de linkerwand.
"""

LOGIC_JS = r"""/*IP-LOGICA*/
var IP = (function () {
  var EPS = 0.001;
  function rect(x, y, w, h) { return { x: x, y: y, w: w, h: h }; }
  function overlap(a, b) {
    return a.x < b.x + b.w - EPS && b.x < a.x + a.w - EPS && a.y < b.y + b.h - EPS && b.y < a.y + a.h - EPS;
  }
  function binnen(r, k) {
    return r.x >= -EPS && r.y >= -EPS && r.x + r.w <= k.b + EPS && r.y + r.h <= k.d + EPS;
  }
  function maat(el, T) {
    var t = T[el.type], staand = el.rot === 90 || el.rot === 270;
    return { w: staand ? t.d : t.w, h: staand ? t.w : t.d };
  }
  function voetafdruk(el, T) { var m = maat(el, T); return rect(el.x, el.y, m.w, m.h); }
  /* Zone voor de voorkant: diepte F, breedte Z, gecentreerd op het element. */
  function voorZone(el, T, F, Z) {
    var r = voetafdruk(el, T), cx = r.x + r.w / 2, cy = r.y + r.h / 2;
    if (el.rot === 0) { return rect(cx - Z / 2, r.y + r.h, Z, F); }
    if (el.rot === 180) { return rect(cx - Z / 2, r.y - F, Z, F); }
    if (el.rot === 90) { return rect(r.x - F, cy - Z / 2, F, Z); }
    return rect(r.x + r.w, cy - Z / 2, F, Z);
  }
  function zijZones(el, T, S) {
    var r = voetafdruk(el, T);
    if (el.rot === 0 || el.rot === 180) { return [rect(r.x - S, r.y, S, r.h), rect(r.x + r.w, r.y, S, r.h)]; }
    return [rect(r.x, r.y - S, r.w, S), rect(r.x, r.y + r.h, r.w, S)];
  }
  /* Richtmaten. modus "gangbaar" of "ruim" (rollatorgeschikt, 1,1 x 1,1 m). */
  function richtmaten(modus) {
    return modus === "ruim"
      ? { toiletVoor: 110, toiletBreed: 110, toiletZij: 20, wasVoor: 110, wasMin: 110, wasmachineVoor: 60 }
      : { toiletVoor: 60, toiletBreed: 70, toiletZij: 20, wasVoor: 70, wasMin: 60, wasmachineVoor: 60 };
  }
  /* Alle vrije-ruimtezones van een element: [{r, soort, ernst, tekst}] */
  function zones(el, T, modus) {
    var t = T[el.type], R = richtmaten(modus), uit = [];
    if (t.cat === "toilet") {
      uit.push({ r: voorZone(el, T, R.toiletVoor, R.toiletBreed), soort: "voor", ernst: "fout",
                 tekst: "Voor het toilet is minder dan " + R.toiletVoor + " cm vrij" + (modus === "ruim" ? " (over 110 cm breed)" : "") + "." });
      zijZones(el, T, R.toiletZij).forEach(function (z) {
        uit.push({ r: z, soort: "zij", ernst: "fout", tekst: "Naast het toilet is minder dan " + R.toiletZij + " cm vrij tot de muur of een ander element." });
      });
    } else if (t.cat === "wastafel") {
      uit.push({ r: voorZone(el, T, R.wasVoor, Math.max(t.w, R.wasMin)), soort: "voor", ernst: "fout",
                 tekst: "Voor de wastafel is minder dan " + R.wasVoor + " cm vrij." });
    } else if (t.cat === "wasmachine") {
      uit.push({ r: voorZone(el, T, R.wasmachineVoor, t.w), soort: "voor", ernst: "advies",
                 tekst: "Voor de wasmachine is minder dan " + R.wasmachineVoor + " cm vrij om het deurtje te openen." });
    }
    return uit;
  }
  /* Deur: wand boven|rechts|onder|links, pos = begin van de opening (cm vanaf links of boven),
     b = breedte, draai "in-a" (scharnier aan het begin), "in-b" (scharnier aan het eind) of "uit". */
  function deurGeometrie(k) {
    var D = k.deur, b = D.b, p = D.pos, in_ = D.draai !== "uit", diep = in_ ? b : 60, sq, scharnier;
    var eind = D.draai === "in-b";
    if (D.wand === "boven") { sq = rect(p, 0, b, diep); scharnier = { x: eind ? p + b : p, y: 0 }; }
    else if (D.wand === "onder") { sq = rect(p, k.d - diep, b, diep); scharnier = { x: eind ? p + b : p, y: k.d }; }
    else if (D.wand === "links") { sq = rect(0, p, diep, b); scharnier = { x: 0, y: eind ? p + b : p }; }
    else { sq = rect(k.b - diep, p, diep, b); scharnier = { x: k.b, y: eind ? p + b : p }; }
    return { naarBinnen: in_, zone: sq, scharnier: scharnier, r: b };
  }
  function doorsnede(a, b) {
    var x1 = Math.max(a.x, b.x), y1 = Math.max(a.y, b.y), x2 = Math.min(a.x + a.w, b.x + b.w), y2 = Math.min(a.y + a.h, b.y + b.h);
    if (x2 - x1 <= EPS || y2 - y1 <= EPS) { return null; }
    return rect(x1, y1, x2 - x1, y2 - y1);
  }
  /* Raakt rechthoek r de draaicirkel (kwart cirkel) van de deur? */
  function deurRaakt(r, g) {
    var s = doorsnede(r, g.zone);
    if (!s) { return false; }
    if (!g.naarBinnen) { return true; }
    var px = Math.min(Math.max(g.scharnier.x, s.x), s.x + s.w), py = Math.min(Math.max(g.scharnier.y, s.y), s.y + s.h);
    var dx = px - g.scharnier.x, dy = py - g.scharnier.y;
    return Math.sqrt(dx * dx + dy * dy) < g.r - EPS;
  }
  function deurPast(k) {
    var D = k.deur, lengte = (D.wand === "boven" || D.wand === "onder") ? k.b : k.d;
    return D.pos >= 0 && D.pos + D.b <= lengte;
  }
  /* Controle: geeft {meldingen:[{ernst, tekst, ids}], perEl:{id: "fout"|"advies"}, zones:[{id, r, ok, ernst}]} */
  function controleer(st, T) {
    var k = st.kamer, els = st.elementen, meld = [], perEl = {}, zl = [];
    function zet(id, e) { if (perEl[id] !== "fout") { perEl[id] = e; } }
    function naam(el) { return T[el.type].naam; }
    if (!deurPast(k)) { meld.push({ ernst: "fout", tekst: "De deur past niet in deze wand. Kies een andere plek of maat.", ids: [] }); }
    var g = deurGeometrie(k);
    els.forEach(function (el, i) {
      var r = voetafdruk(el, T);
      if (!binnen(r, k)) { meld.push({ ernst: "fout", tekst: naam(el) + " steekt door de muur.", ids: [el.id] }); zet(el.id, "fout"); }
      for (var j = i + 1; j < els.length; j++) {
        if (overlap(r, voetafdruk(els[j], T))) {
          meld.push({ ernst: "fout", tekst: naam(el) + " en " + naam(els[j]).toLowerCase() + " overlappen.", ids: [el.id, els[j].id] });
          zet(el.id, "fout"); zet(els[j].id, "fout");
        }
      }
      if (deurRaakt(r, g)) {
        meld.push({ ernst: "fout", tekst: g.naarBinnen ? "De deur draait tegen " + naam(el).toLowerCase() + "." : naam(el) + " staat in de doorgang bij de deur.", ids: [el.id] });
        zet(el.id, "fout");
      }
    });
    els.forEach(function (el) {
      zones(el, T, st.modus).forEach(function (z) {
        var ok = binnen(z.r, k), in_ = [];
        els.forEach(function (ander) {
          if (ander.id !== el.id && overlap(z.r, voetafdruk(ander, T))) { ok = false; in_.push(ander.id); }
        });
        zl.push({ id: el.id, r: z.r, ok: ok, ernst: z.ernst, soort: z.soort });
        if (!ok) {
          var dubbel = meld.some(function (m) { return m.tekst === z.tekst && m.ids[0] === el.id; });
          if (!dubbel) { meld.push({ ernst: z.ernst, tekst: z.tekst, ids: [el.id].concat(in_) }); }
          zet(el.id, z.ernst);
        }
      });
    });
    return { meldingen: meld, perEl: perEl, zones: zl, deur: g };
  }
  function klem(el, T, k) {
    var m = maat(el, T);
    el.x = Math.max(0, Math.min(k.b - m.w, el.x));
    el.y = Math.max(0, Math.min(k.d - m.h, el.y));
    el.x = Math.round(el.x / 5) * 5; el.y = Math.round(el.y / 5) * 5;
    if (el.x + m.w > k.b) { el.x -= 5; }
    if (el.y + m.h > k.d) { el.y -= 5; }
    return el;
  }
  /* Draai een kwartslag rond het midden en houd het element in de ruimte. */
  function draai(el, T, k) {
    var m = maat(el, T), cx = el.x + m.w / 2, cy = el.y + m.h / 2;
    el.rot = (el.rot + 90) % 360;
    var n = maat(el, T);
    el.x = cx - n.w / 2; el.y = cy - n.h / 2;
    return klem(el, T, k);
  }
  /* Zoek een vrije plek voor een nieuw element (eerst langs de wanden). */
  function vrijePlek(type, st, T) {
    var k = st.kamer, g = deurGeometrie(k), best = null;
    var rots = [0, 90, 180, 270];
    for (var ri = 0; ri < rots.length && !best; ri++) {
      var el = { id: "_", type: type, x: 0, y: 0, rot: rots[ri] }, m = maat(el, T);
      for (var y = 0; y + m.h <= k.d && !best; y += 5) {
        for (var x = 0; x + m.w <= k.b; x += 5) {
          el.x = x; el.y = y;
          var r = voetafdruk(el, T), vrij = !deurRaakt(r, g);
          for (var i = 0; vrij && i < st.elementen.length; i++) { if (overlap(r, voetafdruk(st.elementen[i], T))) { vrij = false; } }
          if (vrij) { best = { x: x, y: y, rot: rots[ri] }; break; }
        }
      }
    }
    return best;
  }
  function oppervlak(st, T) {
    var k = st.kamer, vloer = k.b * k.d / 10000, h = st.tegelHoogte / 100;
    var omtrek = 2 * (k.b + k.d) / 100, deur = (k.deur.b / 100) * Math.min(h, 2.1);
    var wand = Math.max(0, omtrek * h - deur);
    return { vloer: vloer, wand: wand, tegels: vloer + wand, omtrek: omtrek, h: h };
  }
  /* Grove kosten met richtprijzen (KOSTEN uit richtprijzen.py). */
  function kosten(st, T, K) {
    var o = oppervlak(st, T), posten = [], tel = {};
    st.elementen.forEach(function (el) { var c = T[el.type].cat; tel[c] = (tel[c] || 0) + 1; });
    var m2 = Math.round(o.tegels * 10) / 10;
    posten.push({ naam: "Tegelwerk vloer en wand, " + String(m2).replace(".", ",") + " m² (tegels, lijm en legloon)", l: K.tegel_m2[0] * m2, h: K.tegel_m2[1] * m2 });
    var volg = ["douche", "bad", "toilet", "wastafel"];
    volg.forEach(function (c) {
      if (!tel[c]) { return; }
      var p = K.element[c];
      posten.push({ naam: p.naam + (tel[c] > 1 ? " (" + tel[c] + "×)" : "") + ", levering en montage", l: p.l * tel[c], h: p.h * tel[c] });
    });
    K.vast.forEach(function (p) {
      if (p.alleenNat && !tel.douche && !tel.bad) { return; }
      posten.push({ naam: p.naam, l: p.l, h: p.h });
    });
    var l = 0, h = 0;
    posten.forEach(function (p) { l += p.l; h += p.h; });
    return { posten: posten, laag: Math.round(l / 100) * 100, hoog: Math.round(h / 100) * 100,
             nietMee: (tel.radiator ? 1 : 0) + (tel.wasmachine ? 1 : 0) };
  }
  function getal(n, dec) { return n.toFixed(dec).replace(".", ","); }
  function duizend(n) { return String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, "."); }
  function vanaf(w) { return (w === "boven" || w === "onder") ? " cm vanaf links" : " cm vanaf boven"; }
  var WANDNAAM = { boven: "bovenwand", rechts: "rechterwand", onder: "onderwand", links: "linkerwand" };
  function beschrijving(st, T, K) {
    var k = st.kamer, o = oppervlak(st, T), c = controleer(st, T), r = [];
    r.push("Indeling uit de indelingsplanner:");
    r.push("Ruimte: " + k.b + " x " + k.d + " cm (" + getal(o.vloer, 2) + " m² vloer)");
    var dr = k.deur.draai === "uit" ? "draait naar buiten" : "draait naar binnen";
    r.push("Deur: " + WANDNAAM[k.deur.wand] + ", " + k.deur.pos + vanaf(k.deur.wand) + ", " + k.deur.b + " cm breed, " + dr);
    if (k.raam && k.raam.aan) { r.push("Raam: " + WANDNAAM[k.raam.wand] + ", " + k.raam.pos + vanaf(k.raam.wand) + ", " + k.raam.b + " cm breed"); }
    if (st.elementen.length) {
      r.push("Elementen:");
      st.elementen.forEach(function (el) {
        var t = T[el.type];
        r.push("- " + t.naam + (/\d/.test(t.naam) ? "" : " (" + t.w + " x " + t.d + " cm)") + ", op " + el.x + " cm van links en " + el.y + " cm van boven");
      });
    } else { r.push("Elementen: nog niets ingetekend"); }
    r.push("Tegelwerk (indicatie): " + getal(o.vloer, 1) + " m² vloer + " + getal(o.wand, 1) + " m² wand (tot " + getal(o.h, 2) + " m)");
    var fout = c.meldingen.filter(function (m) { return m.ernst === "fout"; });
    r.push(fout.length ? "Let op, nog " + fout.length + " knelpunt(en): " + fout.map(function (m) { return m.tekst; }).join(" ") : "Controle vrije ruimte: geen knelpunten gevonden.");
    if (K) { var ko = kosten(st, T, K); r.push("Grove kostenindicatie: € " + duizend(ko.laag) + " – € " + duizend(ko.hoog) + " incl. btw"); }
    return r.join("\n").slice(0, 1800);
  }
  return { overlap: overlap, binnen: binnen, voetafdruk: voetafdruk, maat: maat, zones: zones, richtmaten: richtmaten,
           deurGeometrie: deurGeometrie, deurRaakt: deurRaakt, controleer: controleer, klem: klem, draai: draai,
           vrijePlek: vrijePlek, oppervlak: oppervlak, kosten: kosten, beschrijving: beschrijving };
})();
if (typeof module !== "undefined" && module.exports) { module.exports = IP; }
/*IP-LOGICA-EINDE*/
"""

UI_JS = r"""(function () {
  var root = document.querySelector("[data-ip]");
  if (!root) { return; }
  var T = __TYPES__, PRESETS = __PRESETS__, K = __KOSTEN__;
  var NS = "http://www.w3.org/2000/svg";
  var svg = root.querySelector("[data-ip-svg]"), $ = function (s) { return root.querySelector(s); };
  var st = null, gekozen = null, sleep = null, teller = 1;
  function kopie(o) { return JSON.parse(JSON.stringify(o)); }
  function laadPreset(n) {
    var p = kopie(PRESETS[n]);
    st = { kamer: p.kamer, elementen: p.elementen.map(function (e) { e.id = "e" + (teller++); return e; }),
           modus: st ? st.modus : "gangbaar", tegelHoogte: st ? st.tegelHoogte : 210 };
    gekozen = null; naarFormulier(); teken();
  }
  function num(id, min, max, def) {
    var v = parseInt($(id).value, 10);
    if (isNaN(v)) { return def; }
    return Math.max(min, Math.min(max, Math.round(v / 5) * 5));
  }
  function naarFormulier() {
    var k = st.kamer;
    $("#ip-b").value = k.b; $("#ip-d").value = k.d;
    $("#ip-dw").value = k.deur.wand; $("#ip-dp").value = k.deur.pos; $("#ip-db").value = k.deur.b; $("#ip-dd").value = k.deur.draai;
    $("#ip-ra").checked = !!k.raam.aan; $("#ip-rw").value = k.raam.wand; $("#ip-rp").value = k.raam.pos; $("#ip-rb").value = k.raam.b;
    $("#ip-modus").value = st.modus; $("#ip-h").value = st.tegelHoogte;
    $("[data-ip-raam]").hidden = !k.raam.aan;
  }
  function uitFormulier() {
    var k = st.kamer;
    k.b = num("#ip-b", 100, 600, k.b); k.d = num("#ip-d", 100, 600, k.d);
    k.deur.wand = $("#ip-dw").value; k.deur.b = parseInt($("#ip-db").value, 10); k.deur.draai = $("#ip-dd").value;
    k.deur.pos = num("#ip-dp", 0, 600, k.deur.pos);
    k.raam.aan = $("#ip-ra").checked; k.raam.wand = $("#ip-rw").value; k.raam.b = num("#ip-rb", 30, 400, k.raam.b); k.raam.pos = num("#ip-rp", 0, 600, k.raam.pos);
    st.modus = $("#ip-modus").value; st.tegelHoogte = parseInt($("#ip-h").value, 10) || 210;
    $("[data-ip-raam]").hidden = !k.raam.aan;
    st.elementen.forEach(function (el) { IP.klem(el, T, k); });
    teken();
  }
  function el(tag, at, ouder) {
    var e = document.createElementNS(NS, tag);
    for (var a in at) { e.setAttribute(a, at[a]); }
    if (ouder) { ouder.appendChild(e); }
    return e;
  }
  var KLEUR = { douche: ["#e4f2f5", "#3f7f89"], bad: ["#e4f2f5", "#3f7f89"], toilet: ["#ffffff", "#3a4a5c"],
                wastafel: ["#f3ece2", "#7a5a3a"], radiator: ["#eef0f3", "#55606e"], wasmachine: ["#ffffff", "#55606e"] };
  /* Tekening in lokale coördinaten: breedte w, diepte d, rug op y=0. */
  function vorm(g, t) {
    var w = t.w, d = t.d, k = KLEUR[t.cat], f = k[0], s = k[1];
    var basis = { fill: f, stroke: s, "stroke-width": 1.5 };
    if (t.vorm === "inloop") {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d }, basis), g);
      el("line", { x1: 0, y1: d, x2: w * 0.7, y2: d, stroke: s, "stroke-width": 3 }, g);
      el("rect", { x: w / 2 - 15, y: d / 2 - 2, width: 30, height: 4, fill: s }, g);
    } else if (t.vorm === "douchebak") {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d }, basis), g);
      el("rect", { x: 6, y: 6, width: w - 12, height: d - 12, rx: 6, fill: "none", stroke: s, "stroke-width": 1 }, g);
      el("circle", { cx: w / 2, cy: d / 2, r: 4, fill: "none", stroke: s, "stroke-width": 1.2 }, g);
    } else if (t.vorm === "bad") {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d }, basis), g);
      el("rect", { x: 7, y: 7, width: w - 14, height: d - 14, rx: d / 3, fill: "#ffffff", stroke: s, "stroke-width": 1 }, g);
      el("circle", { cx: 20, cy: d / 2, r: 3.5, fill: s }, g);
    } else if (t.vorm === "vrijstaand") {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d, rx: d / 2 }, basis), g);
      el("rect", { x: 8, y: 8, width: w - 16, height: d - 16, rx: (d - 16) / 2, fill: "#ffffff", stroke: s, "stroke-width": 1 }, g);
    } else if (t.vorm === "toilet") {
      el("rect", { x: 2, y: 0, width: w - 4, height: 10, fill: "#dfe4ea", stroke: s, "stroke-width": 1.2 }, g);
      el("ellipse", Object.assign({ cx: w / 2, cy: 10 + (d - 10) / 2, rx: w / 2 - 1, ry: (d - 10) / 2 }, basis), g);
      el("ellipse", { cx: w / 2, cy: 12 + (d - 12) / 2, rx: w / 2 - 7, ry: (d - 12) / 2 - 7, fill: "none", stroke: s, "stroke-width": 1 }, g);
    } else if (t.vorm === "wastafel") {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d, rx: 2 }, basis), g);
      var n = t.bakken || 1;
      for (var i = 0; i < n; i++) {
        var cx = w / (2 * n) * (2 * i + 1);
        el("ellipse", { cx: cx, cy: d / 2 + 3, rx: Math.min(22, w / (2 * n) - 6), ry: d / 2 - 9, fill: "#ffffff", stroke: s, "stroke-width": 1 }, g);
        el("circle", { cx: cx, cy: 6, r: 2.5, fill: s }, g);
      }
    } else if (t.vorm === "radiator") {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d }, basis), g);
      for (var x = 8; x < w; x += 8) { el("line", { x1: x, y1: 1, x2: x, y2: d - 1, stroke: s, "stroke-width": 0.8 }, g); }
    } else {
      el("rect", Object.assign({ x: 0, y: 0, width: w, height: d, rx: 3 }, basis), g);
      el("circle", { cx: w / 2, cy: d / 2, r: Math.min(w, d) / 2 - 10, fill: "#eef3f6", stroke: s, "stroke-width": 1.5 }, g);
    }
  }
  function transform(e) {
    var t = T[e.type];
    if (e.rot === 0) { return "translate(" + e.x + " " + e.y + ")"; }
    if (e.rot === 90) { return "translate(" + (e.x + t.d) + " " + e.y + ") rotate(90)"; }
    if (e.rot === 180) { return "translate(" + (e.x + t.w) + " " + (e.y + t.d) + ") rotate(180)"; }
    return "translate(" + e.x + " " + (e.y + t.w) + ") rotate(270)";
  }
  var WANDNAAM = { boven: "boven", rechts: "rechts", onder: "onder", links: "links" };
  function teken() {
    var k = st.kamer, c = IP.controleer(st, T), M = 34, fs = Math.max(9, (Math.max(k.b, k.d) + 2 * M) / 32);
    var actief = document.activeElement && document.activeElement.getAttribute && document.activeElement.getAttribute("data-id");
    svg.setAttribute("viewBox", (-M) + " " + (-M) + " " + (k.b + 2 * M) + " " + (k.d + 2 * M));
    svg.setAttribute("aria-label", "Plattegrond van de badkamer, " + k.b + " bij " + k.d + " centimeter, met " + st.elementen.length + " elementen");
    while (svg.firstChild) { svg.removeChild(svg.firstChild); }
    el("rect", { x: -M, y: -M, width: k.b + 2 * M, height: k.d + 2 * M, fill: "#ffffff" }, svg);
    var defs = el("defs", {}, svg), pat = el("pattern", { id: "ip-raster", width: 10, height: 10, patternUnits: "userSpaceOnUse" }, defs);
    el("path", { d: "M10 0H0V10", fill: "none", stroke: "#e3e8ee", "stroke-width": 0.6 }, pat);
    el("rect", { x: -10, y: -10, width: k.b + 20, height: k.d + 20, fill: "#3a4a5c" }, svg);
    el("rect", { x: 0, y: 0, width: k.b, height: k.d, fill: "#fbfcfd" }, svg);
    el("rect", { x: 0, y: 0, width: k.b, height: k.d, fill: "url(#ip-raster)" }, svg);
    for (var x = 50; x < k.b; x += 50) { el("line", { x1: x, y1: 0, x2: x, y2: k.d, stroke: "#d3dbe3", "stroke-width": 0.8 }, svg); }
    for (var y = 50; y < k.d; y += 50) { el("line", { x1: 0, y1: y, x2: k.b, y2: y, stroke: "#d3dbe3", "stroke-width": 0.8 }, svg); }
    /* maatvoering */
    var tx = { "font-family": "system-ui,-apple-system,Segoe UI,Arial,sans-serif", "font-size": fs, fill: "#3a4a5c", "text-anchor": "middle" };
    var t1 = el("text", Object.assign({ x: k.b / 2, y: -M + fs * 1.1 }, tx), svg); t1.textContent = k.b + " cm";
    var t2 = el("text", Object.assign({ x: -M + fs * 1.1, y: k.d / 2, transform: "rotate(-90 " + (-M + fs * 1.1) + " " + (k.d / 2) + ")" }, tx), svg); t2.textContent = k.d + " cm";
    /* raam */
    var R = k.raam;
    if (R.aan) {
      var rr = wandRect(k, R.wand, R.pos, R.b);
      el("rect", Object.assign(rr, { fill: "#cfe8f3", stroke: "#3f7f89", "stroke-width": 1 }), svg);
    }
    /* vrije-ruimtezones */
    c.zones.forEach(function (z) {
      var sel = z.id === gekozen;
      if (!z.ok || sel) {
        el("rect", { x: z.r.x, y: z.r.y, width: z.r.w, height: z.r.h,
          fill: z.ok ? "rgba(63,127,137,.10)" : (z.ernst === "fout" ? "rgba(200,40,40,.16)" : "rgba(230,150,20,.18)"),
          stroke: z.ok ? "#3f7f89" : (z.ernst === "fout" ? "#c82828" : "#d48a00"), "stroke-width": 1, "stroke-dasharray": "4 3" }, svg);
      }
    });
    /* deur */
    var g = c.deur, D = k.deur, open = wandRect(k, D.wand, D.pos, D.b);
    el("rect", Object.assign(open, { fill: "#fbfcfd" }), svg);
    var deurFout = c.meldingen.some(function (m) { return /De deur|bij de deur/.test(m.tekst); });
    var dk = deurFout ? "#c82828" : "#3a4a5c";
    if (g.naarBinnen) {
      var h = g.scharnier, r = g.r, a, b;
      if (D.wand === "boven" || D.wand === "onder") {
        var dir = D.wand === "boven" ? 1 : -1, ander = (D.draai === "in-b") ? h.x - r : h.x + r;
        a = { x: h.x, y: h.y + dir * r }; b = { x: ander, y: h.y };
      } else {
        var dx = D.wand === "links" ? 1 : -1, ander2 = (D.draai === "in-b") ? h.y - r : h.y + r;
        a = { x: h.x + dx * r, y: h.y }; b = { x: h.x, y: ander2 };
      }
      el("path", { d: "M" + h.x + " " + h.y + "L" + a.x + " " + a.y + "L" + a.x + " " + a.y + "A" + r + " " + r + " 0 0 " + boogRichting(D) + " " + b.x + " " + b.y,
        fill: "none", stroke: dk, "stroke-width": 1, "stroke-dasharray": "3 3" }, svg);
      el("line", { x1: h.x, y1: h.y, x2: a.x, y2: a.y, stroke: dk, "stroke-width": 3 }, svg);
    } else {
      el("rect", { x: g.zone.x, y: g.zone.y, width: g.zone.w, height: g.zone.h, fill: "none", stroke: dk, "stroke-width": 1, "stroke-dasharray": "3 3" }, svg);
    }
    var dl = wandMidden(k, D.wand, D.pos + D.b / 2, M, fs);
    var t3 = el("text", Object.assign({ x: dl.x, y: dl.y }, tx, { "font-size": fs * 0.85 }), svg); t3.textContent = "deur";
    /* elementen */
    st.elementen.forEach(function (e) {
      var t = T[e.type], fp = IP.voetafdruk(e, T), ernst = c.perEl[e.id];
      var grp = el("g", { "data-id": e.id, tabindex: 0, role: "button", class: "ip-el",
        "aria-label": t.naam + ", " + e.x + " cm van links, " + e.y + " cm van boven" + (ernst === "fout" ? ", probleem" : "") + ". Pijltjes verplaatsen, R draait, Delete verwijdert." }, svg);
      var binnen = el("g", { transform: transform(e) }, grp);
      vorm(binnen, t);
      if (ernst || e.id === gekozen) {
        el("rect", { x: fp.x - 1.5, y: fp.y - 1.5, width: fp.w + 3, height: fp.h + 3, fill: "none",
          stroke: ernst === "fout" ? "#c82828" : (ernst === "advies" ? "#d48a00" : "#e8792b"), "stroke-width": e.id === gekozen ? 3 : 2 }, grp);
      }
      if (Math.min(fp.w, fp.h) >= 30) {
        var lt = el("text", Object.assign({ x: fp.x + fp.w / 2, y: fp.y + fp.h / 2 + fs * 0.35 }, tx, { "font-size": fs * 0.8, "pointer-events": "none", fill: "#1f2b38" }), grp);
        lt.textContent = t.kort;
      }
    });
    if (actief) { var terug = svg.querySelector('[data-id="' + actief + '"]'); if (terug) { terug.focus({ preventScroll: true }); } }
    paneel(); resultaat(c);
  }
  function boogRichting(D) {
    var mapv = { "boven-in-a": 0, "boven-in-b": 1, "onder-in-a": 1, "onder-in-b": 0, "links-in-a": 1, "links-in-b": 0, "rechts-in-a": 0, "rechts-in-b": 1 };
    return mapv[D.wand + "-" + D.draai];
  }
  function wandRect(k, wand, pos, b) {
    if (wand === "boven") { return { x: pos, y: -10, width: b, height: 10 }; }
    if (wand === "onder") { return { x: pos, y: k.d, width: b, height: 10 }; }
    if (wand === "links") { return { x: -10, y: pos, width: 10, height: b }; }
    return { x: k.b, y: pos, width: 10, height: b };
  }
  function wandMidden(k, wand, m, M, fs) {
    if (wand === "boven") { return { x: m, y: -14 }; }
    if (wand === "onder") { return { x: m, y: k.d + 14 + fs * 0.7 }; }
    if (wand === "links") { return { x: -M + fs * 2.6, y: m }; }
    return { x: k.b + 22, y: m };
  }
  function eur(n) { return "€ " + Math.round(n).toLocaleString("nl-NL"); }
  function paneel() {
    var p = $("[data-ip-sel]"), e = st.elementen.filter(function (x) { return x.id === gekozen; })[0];
    if (!e) { p.hidden = true; return; }
    p.hidden = false;
    $("[data-ip-selnaam]").textContent = T[e.type].naam + " · " + e.x + " cm van links, " + e.y + " cm van boven";
  }
  function resultaat(c) {
    var o = IP.oppervlak(st, T), ko = IP.kosten(st, T, K), k = st.kamer;
    $("[data-ip-maat]").textContent = k.b + " × " + k.d + " cm";
    $("[data-ip-vloer]").textContent = o.vloer.toFixed(2).replace(".", ",") + " m²";
    $("[data-ip-tegel]").textContent = o.tegels.toFixed(1).replace(".", ",") + " m²";
    $("[data-ip-tegeluitleg]").textContent = o.vloer.toFixed(1).replace(".", ",") + " m² vloer + " + o.wand.toFixed(1).replace(".", ",") +
      " m² wand tot " + o.h.toFixed(2).replace(".", ",") + " m (deur eraf, raam niet). Bestel 10 tot 15% extra voor snijverlies.";
    $("[data-ip-kosten]").textContent = eur(ko.laag) + " – " + eur(ko.hoog);
    var ul = $("[data-ip-posten]"); ul.innerHTML = "";
    ko.posten.forEach(function (p) {
      var li = document.createElement("li");
      li.innerHTML = "<span></span><b></b>";
      li.firstChild.textContent = p.naam; li.lastChild.textContent = eur(Math.round(p.l / 10) * 10) + " – " + eur(Math.round(p.h / 10) * 10);
      ul.appendChild(li);
    });
    $("[data-ip-nietmee]").hidden = !ko.nietMee;
    var m = $("[data-ip-meld]"); m.innerHTML = "";
    var fouten = c.meldingen.filter(function (x) { return x.ernst === "fout"; }).length;
    var kop = $("[data-ip-status]");
    kop.className = "ip-status " + (fouten ? "ip-st-fout" : (c.meldingen.length ? "ip-st-advies" : "ip-st-ok"));
    kop.textContent = fouten ? fouten + (fouten === 1 ? " knelpunt" : " knelpunten") + " in deze indeling"
      : (c.meldingen.length ? "Past, met een aandachtspunt" : "Alles past volgens de richtmaten");
    c.meldingen.forEach(function (x) {
      var li = document.createElement("li"); li.className = x.ernst === "fout" ? "ip-m-fout" : "ip-m-advies"; li.textContent = x.tekst; m.appendChild(li);
    });
    if (!st.elementen.length) { var li2 = document.createElement("li"); li2.textContent = "Voeg elementen toe met de knoppen hieronder, of kies een voorbeeld."; m.appendChild(li2); }
  }
  function punt(ev) {
    var p = svg.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY;
    return p.matrixTransform(svg.getScreenCTM().inverse());
  }
  svg.addEventListener("pointerdown", function (ev) {
    var g = ev.target.closest && ev.target.closest(".ip-el");
    if (!g) { if (gekozen) { gekozen = null; teken(); } return; }
    var e = st.elementen.filter(function (x) { return x.id === g.getAttribute("data-id"); })[0];
    var p = punt(ev);
    sleep = { e: e, dx: p.x - e.x, dy: p.y - e.y, id: ev.pointerId };
    gekozen = e.id;
    try { svg.setPointerCapture(ev.pointerId); } catch (x) {}
    ev.preventDefault(); teken();
    var nieuw = svg.querySelector('[data-id="' + e.id + '"]'); if (nieuw) { nieuw.focus({ preventScroll: true }); }
  });
  svg.addEventListener("pointermove", function (ev) {
    if (!sleep || ev.pointerId !== sleep.id) { return; }
    var p = punt(ev), e = sleep.e, ox = e.x, oy = e.y;
    e.x = Math.round((p.x - sleep.dx) / 5) * 5; e.y = Math.round((p.y - sleep.dy) / 5) * 5;
    IP.klem(e, T, st.kamer);
    if (e.x !== ox || e.y !== oy) { teken(); }
  });
  function stop(ev) { if (sleep && ev.pointerId === sleep.id) { sleep = null; } }
  svg.addEventListener("pointerup", stop); svg.addEventListener("pointercancel", stop);
  svg.addEventListener("keydown", function (ev) {
    var g = ev.target.closest && ev.target.closest(".ip-el"); if (!g) { return; }
    var e = st.elementen.filter(function (x) { return x.id === g.getAttribute("data-id"); })[0], s = ev.shiftKey ? 25 : 5, ok = true;
    if (ev.key === "ArrowLeft") { e.x -= s; } else if (ev.key === "ArrowRight") { e.x += s; }
    else if (ev.key === "ArrowUp") { e.y -= s; } else if (ev.key === "ArrowDown") { e.y += s; }
    else if (ev.key === "r" || ev.key === "R") { IP.draai(e, T, st.kamer); }
    else if (ev.key === "Delete" || ev.key === "Backspace") { verwijder(e.id); ev.preventDefault(); return; }
    else if (ev.key === "Enter" || ev.key === " ") { gekozen = e.id; }
    else { ok = false; }
    if (ok) { ev.preventDefault(); IP.klem(e, T, st.kamer); gekozen = e.id; teken(); }
  });
  svg.addEventListener("focusin", function (ev) {
    var g = ev.target.closest && ev.target.closest(".ip-el");
    if (g && gekozen !== g.getAttribute("data-id")) { gekozen = g.getAttribute("data-id"); teken(); }
  });
  function verwijder(id) {
    st.elementen = st.elementen.filter(function (x) { return x.id !== id; }); gekozen = null; teken();
    svg.focus({ preventScroll: true });
  }
  root.querySelectorAll("[data-ip-add]").forEach(function (b) {
    b.addEventListener("click", function () {
      var type = b.getAttribute("data-ip-add"), plek = IP.vrijePlek(type, st, T);
      var e = { id: "e" + (teller++), type: type, x: 0, y: 0, rot: 0 };
      if (plek) { e.x = plek.x; e.y = plek.y; e.rot = plek.rot; } else { e.x = st.kamer.b / 2; e.y = st.kamer.d / 2; }
      IP.klem(e, T, st.kamer);
      st.elementen.push(e); gekozen = e.id; teken();
      $("[data-ip-live]").textContent = T[type].naam + " toegevoegd" + (plek ? "." : ", maar er is geen vrije plek: schuif hem zelf op zijn plaats.");
    });
  });
  $("[data-ip-draai]").addEventListener("click", function () {
    var e = st.elementen.filter(function (x) { return x.id === gekozen; })[0]; if (e) { IP.draai(e, T, st.kamer); teken(); }
  });
  $("[data-ip-weg]").addEventListener("click", function () { if (gekozen) { verwijder(gekozen); } });
  $("[data-ip-leeg]").addEventListener("click", function () { st.elementen = []; gekozen = null; teken(); });
  root.querySelectorAll("[data-ip-preset]").forEach(function (b) {
    b.addEventListener("click", function () {
      laadPreset(b.getAttribute("data-ip-preset"));
      root.querySelectorAll("[data-ip-preset]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
    });
  });
  root.querySelector("[data-ip-form]").addEventListener("change", uitFormulier);
  root.querySelector("[data-ip-form]").addEventListener("submit", function (ev) { ev.preventDefault(); uitFormulier(); });
  /* Opslaan als afbeelding: SVG naar png via canvas, alles in de browser. */
  $("[data-ip-png]").addEventListener("click", function () {
    var vb = svg.viewBox.baseVal, schaal = Math.min(4, 1600 / Math.max(vb.width, vb.height));
    var kloon = svg.cloneNode(true);
    kloon.setAttribute("xmlns", NS); kloon.setAttribute("width", Math.round(vb.width * schaal)); kloon.setAttribute("height", Math.round(vb.height * schaal));
    var data = new XMLSerializer().serializeToString(kloon);
    var img = new Image();
    img.onload = function () {
      var cv = document.createElement("canvas"); cv.width = Math.round(vb.width * schaal); cv.height = Math.round(vb.height * schaal);
      var cx = cv.getContext("2d"); cx.fillStyle = "#fff"; cx.fillRect(0, 0, cv.width, cv.height); cx.drawImage(img, 0, 0, cv.width, cv.height);
      var a = document.createElement("a"); a.download = "badkamerindeling-" + st.kamer.b + "x" + st.kamer.d + ".png";
      try { a.href = cv.toDataURL("image/png"); document.body.appendChild(a); a.click(); a.remove(); }
      catch (x) { $("[data-ip-live]").textContent = "Opslaan lukt niet in deze browser. Maak anders een schermafbeelding."; }
    };
    img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(data);
  });
  /* Meenemen in de aanvraag: korte tekst in sessionStorage tb_indeling. */
  document.querySelectorAll('a[href*="via=indeling"]').forEach(function (a) {
    a.addEventListener("click", function () {
      try { sessionStorage.setItem("tb_indeling", IP.beschrijving(st, T, K)); } catch (x) {}
    });
  });
  laadPreset("klein");
  root.querySelector('[data-ip-preset="klein"]').setAttribute("aria-pressed", "true");
})();
"""
