# -*- coding: utf-8 -*-
"""Tegelpatroon-visualizer (/tools/tegelpatroon/).

Losse module met de interface LINKS + build(write). De tekening gebeurt in de
browser op een <canvas>; alle rekenwaarden gaan via json.dumps naar de JavaScript.

Rekenwaarden en bronnen:
- Legloon per m² en hulpmateriaal: richtprijzen.py, posten "tegelwerk" (alleen
  het zetten) en "tegelwerk_hulpmateriaal" (lijm, voegsel, kit). Incl. 21% btw.
- Tegels zelf: richtprijzen.py, post "tegels" (materiaal per m²), alleen als indicatie.
- Snijverlies per patroon: gangbare vuistregels van tegelzetters en bouwmarkten
  (recht 5 tot 10%, halfsteens iets meer, visgraat en Hongaarse punt 15 tot 20%).
  We rekenen met één waarde per patroon; dat is een eigen inschatting en staat zo
  op de pagina.
- Toeslag op het legloon voor visgraat, Hongaarse punt en blokverband: eigen
  inschatting. Tegelzetters rekenen voor deze patronen vaak meer, omdat er meer
  gezaagd en uitgelijnd wordt; er is geen vaste bron voor de hoogte.
"""

import json

import richtprijzen as RP
from components import page, crumbs, faq_blok, cta_blok, title, desc, eur

PAD = "/tools/tegelpatroon/"

LINKS = [
    (PAD, "Tegelpatroon bekijken",
     "Kies legpatroon, tegelmaat, kleur en voeg en zie meteen hoeveel tegels je nodig hebt."),
]

# id, naam, snijverlies (fractie), toeslag legloon (fractie), korte uitleg
PATRONEN = [
    {"id": "recht", "naam": "Recht", "verlies": 0.07, "toeslag": 0.0,
     "uitleg": "Tegels recht onder en naast elkaar, met doorlopende voegen. Rustig en het minste snijverlies."},
    {"id": "halfsteens", "naam": "Halfsteens", "verlies": 0.10, "toeslag": 0.0,
     "uitleg": "Elke rij schuift een halve tegel op, zoals metselwerk. Past goed bij langwerpige tegels."},
    {"id": "verticaal", "naam": "Verticaal", "verlies": 0.07, "toeslag": 0.0,
     "uitleg": "Langwerpige tegels staand en recht boven elkaar. Maakt een lage wand optisch hoger."},
    {"id": "blokverband", "naam": "Blokverband", "verlies": 0.10, "toeslag": 0.10,
     "uitleg": "Blokjes van liggende en staande tegels om en om, ook wel mandverband. Speels en wat retro."},
    {"id": "visgraat", "naam": "Visgraat", "verlies": 0.15, "toeslag": 0.25,
     "uitleg": "Tegels haaks tegen elkaar in een zigzag, hier onder 45 graden. Meer snijwerk langs de randen."},
    {"id": "hongaars", "naam": "Hongaarse punt", "verlies": 0.18, "toeslag": 0.30,
     "uitleg": "Tegels met schuin afgezaagde kopse kanten vormen punten. De tegels zijn vaak al schuin gemaakt."},
]

# Tegelmaten in cm: (lang, breed). De eerste waarde is de lange kant.
MATEN = [
    ("60x60", 60, 60), ("30x60", 60, 30), ("60x120", 120, 60), ("20x120", 120, 20),
    ("30x30", 30, 30), ("20x20", 20, 20), ("15x15", 15, 15), ("10x10", 10, 10),
    ("7,5x30", 30, 7.5), ("6x24", 24, 6), ("10x40", 40, 10),
]

# Tegelkleur of materiaal: basiskleur en een eventuele textuur
MATERIALEN = [
    {"id": "wit", "naam": "Wit glans", "kleur": "#f4f3ef", "var": 0.015, "tex": ""},
    {"id": "gebroken", "naam": "Gebroken wit", "kleur": "#e9e2d4", "var": 0.03, "tex": ""},
    {"id": "beton", "naam": "Betonlook grijs", "kleur": "#a9a7a1", "var": 0.06, "tex": "vlek"},
    {"id": "antraciet", "naam": "Antraciet", "kleur": "#3f4144", "var": 0.04, "tex": "vlek"},
    {"id": "zand", "naam": "Zandkleur", "kleur": "#d6c4a3", "var": 0.04, "tex": "vlek"},
    {"id": "terracotta", "naam": "Terracotta", "kleur": "#c0704c", "var": 0.08, "tex": ""},
    {"id": "salie", "naam": "Saliegroen", "kleur": "#9fae96", "var": 0.04, "tex": ""},
    {"id": "blauw", "naam": "Diepblauw", "kleur": "#2f4e6e", "var": 0.05, "tex": ""},
    {"id": "marmer", "naam": "Marmerlook wit", "kleur": "#eeece8", "var": 0.02, "tex": "marmer"},
    {"id": "hout", "naam": "Houtlook eiken", "kleur": "#b48a5e", "var": 0.09, "tex": "hout"},
    {"id": "zwart", "naam": "Zwart mat", "kleur": "#232426", "var": 0.03, "tex": ""},
]

VOEGKLEUREN = [
    ("Wit", "#f7f7f5"), ("Lichtgrijs", "#c9c9c5"), ("Cementgrijs", "#8f8e8a"),
    ("Antraciet", "#4a4b4d"), ("Zwart", "#1d1d1f"), ("Zand", "#cbb994"),
]

PRIJS = {
    "leg": RP.lh("tegelwerk"),
    "hulp": RP.lh("tegelwerk_hulpmateriaal"),
    "tegels": RP.lh("tegels"),
}

JS = r"""
(function () {
  var D = __DATA__;
  var root = document.querySelector("[data-tp]");
  if (!root) { return; }
  function $(s) { return root.querySelector(s); }
  var cv = $("#tp-canvas"), ctx = cv.getContext("2d");
  var P = {}; D.patronen.forEach(function (p) { P[p.id] = p; });
  var M = {}; D.materialen.forEach(function (m) { M[m.id] = m; });

  function nl(n, d) { return n.toLocaleString("nl-NL", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 }); }
  function eur(n) { return "€" + nl(Math.round(n / 5) * 5); }
  function getal(id, min, max, std) {
    var v = parseFloat(String($(id).value).replace(",", "."));
    if (!isFinite(v)) { return std; }
    return Math.min(max, Math.max(min, v));
  }
  function keuze(n) { var e = root.querySelector('input[name="' + n + '"]:checked'); return e ? e.value : ""; }

  // Kleine voorspelbare random, zodat dezelfde instellingen hetzelfde beeld geven
  function rnd(a, b) { var x = Math.sin(a * 127.1 + b * 311.7) * 43758.5453; return x - Math.floor(x); }
  function hex(h) { return [parseInt(h.substr(1, 2), 16), parseInt(h.substr(3, 2), 16), parseInt(h.substr(5, 2), 16)]; }
  function tint(rgb, f) {
    return "rgb(" + rgb.map(function (c) { return Math.max(0, Math.min(255, Math.round(c * (1 + f)))); }).join(",") + ")";
  }

  function leesInvoer() {
    var mt = $("#tp-maat").value, lang, breed;
    if (mt === "eigen") {
      lang = getal("#tp-lang", 2, 200, 60); breed = getal("#tp-breed", 2, 200, 30);
      if (breed > lang) { var t = lang; lang = breed; breed = t; }
    } else {
      var o = $("#tp-maat").selectedOptions[0];
      lang = +o.dataset.l; breed = +o.dataset.b;
    }
    return {
      patroon: keuze("tp-patroon"), lang: lang, breed: breed, maat: mt,
      mat: $("#tp-mat").value, voeg: keuze("tp-voeg"), voegmm: getal("#tp-voegmm", 1, 10, 3),
      w: getal("#tp-w", 0.3, 12, 2.4), h: getal("#tp-h", 0.3, 12, 2.6), soort: keuze("tp-soort")
    };
  }

  // ---------- tekenen ----------
  function tegel(pts, i, j, mat, s, rgb) {
    var f = (rnd(i, j) - 0.5) * 2 * mat.var;
    ctx.beginPath();
    ctx.moveTo(pts[0][0], pts[0][1]);
    for (var k = 1; k < pts.length; k++) { ctx.lineTo(pts[k][0], pts[k][1]); }
    ctx.closePath();
    ctx.fillStyle = tint(rgb, f);
    ctx.fill();
    if (!mat.tex) { return; }
    ctx.save(); ctx.clip();
    var minx = Infinity, miny = Infinity, maxx = -Infinity, maxy = -Infinity;
    pts.forEach(function (p) { minx = Math.min(minx, p[0]); maxx = Math.max(maxx, p[0]); miny = Math.min(miny, p[1]); maxy = Math.max(maxy, p[1]); });
    var bw = maxx - minx, bh = maxy - miny, n, q;
    if (mat.tex === "marmer") {
      // een of twee zachte aders die schuin door de tegel lopen
      ctx.lineCap = "round";
      for (n = 0; n < 2; n++) {
        if (n === 1 && rnd(i, j + 9) < 0.5) { break; }
        ctx.strokeStyle = "rgba(125,125,132," + (n ? 0.18 : 0.3) + ")";
        ctx.lineWidth = Math.max(0.6, s * (n ? 0.08 : 0.16));
        var ya = miny + rnd(i + n, j) * bh, yb = miny + rnd(i, j + n + 3) * bh;
        ctx.beginPath();
        ctx.moveTo(minx - 2, ya);
        ctx.bezierCurveTo(minx + bw * 0.35, ya + (rnd(i * 2, j) - 0.5) * bh, minx + bw * 0.65, yb + (rnd(i, j * 2 + 1) - 0.5) * bh, maxx + 2, yb);
        ctx.stroke();
      }
    } else if (mat.tex === "hout") {
      var lang = bw >= bh, len = lang ? bh : bw;
      ctx.strokeStyle = "rgba(70,45,20,.18)"; ctx.lineWidth = Math.max(0.5, s * 0.08);
      for (n = 1; n < 6; n++) {
        ctx.beginPath();
        var off = len * (n / 6 + (rnd(i, j + n) - 0.5) * 0.08);
        if (lang) { ctx.moveTo(minx, miny + off); ctx.bezierCurveTo(minx + bw * .3, miny + off - len * .05, minx + bw * .7, miny + off + len * .05, maxx, miny + off); }
        else { ctx.moveTo(minx + off, miny); ctx.bezierCurveTo(minx + off - len * .05, miny + bh * .3, minx + off + len * .05, miny + bh * .7, minx + off, maxy); }
        ctx.stroke();
      }
    } else if (mat.tex === "vlek") {
      for (n = 0; n < 4; n++) {
        ctx.fillStyle = "rgba(255,255,255," + (0.04 + rnd(i + n, j) * 0.05) + ")";
        ctx.beginPath();
        ctx.arc(minx + rnd(i, j + n * 7) * bw, miny + rnd(i + n * 5, j) * bh, Math.max(bw, bh) * (0.08 + rnd(n, i) * 0.15), 0, 6.283);
        ctx.fill();
      }
    }
    ctx.restore();
  }

  function rect(x, y, w, h, g) {
    return [[x + g, y + g], [x + w - g, y + g], [x + w - g, y + h - g], [x + g, y + h - g]];
  }

  // Tekent het patroon in een gebied van W x H pixels; s = pixels per cm
  function teken(c, inv, W, H, s) {
    var mat = M[inv.mat], rgb = hex(mat.kleur);
    var L = inv.lang * s, B = inv.breed * s, g = Math.max(0.35, inv.voegmm / 10 * s / 2);
    c.fillStyle = inv.voegkleur; c.fillRect(0, 0, W, H);
    var i, j, x, y;
    if (inv.patroon === "recht" || inv.patroon === "verticaal" || inv.patroon === "halfsteens") {
      var tw = inv.patroon === "verticaal" ? B : L, th = inv.patroon === "verticaal" ? L : B;
      for (j = 0; j * th < H + th; j++) {
        var sh = (inv.patroon === "halfsteens" && j % 2) ? -tw / 2 : 0;
        for (i = -1; i * tw + sh < W + tw; i++) {
          x = i * tw + sh; y = H - (j + 1) * th;   // van onder naar boven, zoals een tegelzetter begint
          tegel(rect(x, y, tw, th, g), i, j, mat, s, rgb);
        }
      }
    } else if (inv.patroon === "blokverband") {
      var n = Math.max(1, Math.round(L / B)), bl = L, tb = bl / n;
      for (j = 0; j * bl < H + bl; j++) {
        for (i = 0; i * bl < W + bl; i++) {
          var bx = i * bl, by = H - (j + 1) * bl, lig = (i + j) % 2 === 0;
          for (var k = 0; k < n; k++) {
            tegel(lig ? rect(bx, by + k * tb, bl, tb, g) : rect(bx + k * tb, by, tb, bl, g), i * 10 + k, j, mat, s, rgb);
          }
        }
      }
    } else if (inv.patroon === "visgraat") {
      c.save();
      c.translate(W / 2, H / 2); c.rotate(Math.PI / 4);
      var R = Math.sqrt(W * W + H * H) / 2 + L + B;
      var kmax = Math.ceil((2 * R) / (2 * B)) + 2, smax = Math.ceil((2 * R) / (2 * L)) + 2;
      for (var st = -smax; st <= smax; st++) {
        for (var kk = -kmax; kk <= kmax; kk++) {
          var ox = st * L + kk * B, oy = -st * L + kk * B;
          if (Math.abs(ox) > R + L || Math.abs(oy) > R + L) { continue; }
          tegel(rect(ox, oy, L, B, g), st * 2, kk, mat, s, rgb);
          tegel(rect(ox, oy + B, B, L, g), st * 2 + 1, kk, mat, s, rgb);
        }
      }
      c.restore();
    } else if (inv.patroon === "hongaars") {
      var cw = L / Math.SQRT2, hh = B * Math.SQRT2;
      for (i = 0; i * cw < W + cw; i++) {
        var op = i % 2 === 0, y0 = op ? 0 : -cw;
        for (j = -2; y0 + j * hh < H + cw + hh; j++) {
          y = y0 + j * hh; x = i * cw;
          var pts = op ? [[x, y + cw], [x + cw, y], [x + cw, y + hh], [x, y + cw + hh]]
                       : [[x, y], [x + cw, y + cw], [x + cw, y + cw + hh], [x, y + hh]];
          // voeg: krimp het parallellogram een fractie naar het midden
          var mx = x + cw / 2, my = 0; pts.forEach(function (p) { my += p[1] / 4; });
          var fx = (cw / 2 - g) / (cw / 2), fy = (hh / 2 - g) / (hh / 2);
          pts = pts.map(function (p) { return [mx + (p[0] - mx) * fx, my + (p[1] - my) * fy]; });
          tegel(pts, i, j, mat, s, rgb);
        }
      }
    }
  }

  // ---------- rekenen ----------
  function reken(inv) {
    var p = P[inv.patroon];
    var m2 = inv.w * inv.h;
    var tm2 = inv.lang * inv.breed / 10000;
    var netto = Math.ceil(m2 / tm2);
    var bruto = Math.ceil(m2 * (1 + p.verlies) / tm2);
    var groot = inv.lang >= 90 || inv.breed >= 90 ? 0.15 : 0; // groot formaat: zwaarder werk
    var klein = Math.max(inv.lang, inv.breed) <= 10 ? 0.15 : 0; // mozaïekachtig klein: meer voegen
    var fac = 1 + p.toeslag + groot + klein;
    var leg = [D.prijs.leg[0] * fac * m2 + D.prijs.hulp[0] * m2, D.prijs.leg[1] * fac * m2 + D.prijs.hulp[1] * m2];
    var mat = [D.prijs.tegels[0] * m2 * (1 + p.verlies), D.prijs.tegels[1] * m2 * (1 + p.verlies)];
    return { m2: m2, netto: netto, bruto: bruto, verlies: p.verlies, fac: fac, leg: leg, mat: mat, bestelm2: m2 * (1 + p.verlies) };
  }

  var laatste = null;
  function maatTekst(inv) { return nl(inv.breed, inv.breed % 1 ? 1 : 0) + " x " + nl(inv.lang, inv.lang % 1 ? 1 : 0) + " cm"; }

  function toon() {
    var inv = leesInvoer();
    inv.voegkleur = inv.voeg;
    $("[data-tp-eigen]").hidden = inv.maat !== "eigen";
    $("[data-tp-mmw]").textContent = nl(inv.voegmm) + " mm";
    // canvas passend in de kolom
    var box = $(".tp-doek"), bw = box.clientWidth || 600;
    var maxH = Math.min(560, Math.max(260, window.innerHeight * 0.6));
    var sc = Math.min(bw / inv.w, maxH / inv.h); // pixels per meter
    var cw = Math.round(inv.w * sc), ch = Math.round(inv.h * sc), dpr = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = cw * dpr; cv.height = ch * dpr; cv.style.width = cw + "px"; cv.style.height = ch + "px";
    ctx = cv.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    teken(ctx, inv, cw, ch, sc / 100);
    var r = reken(inv), p = P[inv.patroon];
    $("[data-tp-m2]").textContent = nl(r.m2, 2) + " m²";
    $("[data-tp-aantal]").textContent = nl(r.bruto) + " tegels";
    $("[data-tp-netto]").textContent = "Zonder snijverlies " + nl(r.netto) + ", met " + Math.round(r.verlies * 100) + "% snijverlies " + nl(r.bruto) + ". Bestel ongeveer " + nl(r.bestelm2, 1) + " m².";
    $("[data-tp-leg]").textContent = eur(r.leg[0]) + " – " + eur(r.leg[1]);
    $("[data-tp-legnoot]").textContent = "Legloon plus lijm, voeg en kit voor " + nl(r.m2, 1) + " m²" + (r.fac > 1 ? ", met " + Math.round((r.fac - 1) * 100) + "% toeslag voor dit patroon of formaat" : "") + ".";
    $("[data-tp-mat]").textContent = eur(r.mat[0]) + " – " + eur(r.mat[1]);
    $("[data-tp-uitleg]").textContent = p.uitleg;
    $("[data-tp-sub]").textContent = p.naam + " · " + maatTekst(inv) + " · " + M[inv.mat].naam + " · voeg " + nl(inv.voegmm) + " mm · " + (inv.soort === "vloer" ? "vloer " : "wand ") + nl(inv.w, 2) + " x " + nl(inv.h, 2) + " m";
    laatste = { inv: inv, r: r };
    bewaarInLink(inv);
  }

  // ---------- deelbare link ----------
  var VELDEN = ["patroon", "maat", "lang", "breed", "mat", "voegmm", "w", "h", "soort"];
  function bewaarInLink(inv) {
    var d = {}; VELDEN.forEach(function (k) { d[k] = inv[k]; });
    d.voeg = inv.voeg.replace("#", "");
    var q = Object.keys(d).map(function (k) { return k + "=" + encodeURIComponent(d[k]); }).join("&");
    try { history.replaceState(null, "", "#" + q); } catch (e) { /* niet erg */ }
  }
  function laadUitLink() {
    if (location.hash.length < 3) { return; }
    var d = {};
    location.hash.substr(1).split("&").forEach(function (kv) { var a = kv.split("="); if (a.length === 2) { d[a[0]] = decodeURIComponent(a[1]); } });
    function zet(naam, w) { var e = root.querySelector('input[name="' + naam + '"][value="' + w + '"]'); if (e) { e.checked = true; } }
    if (d.patroon) { zet("tp-patroon", d.patroon); }
    if (d.soort) { zet("tp-soort", d.soort); }
    if (d.voeg && /^[0-9a-f]{6}$/i.test(d.voeg)) { zet("tp-voeg", "#" + d.voeg.toLowerCase()); }
    if (d.maat && $('#tp-maat option[value="' + d.maat + '"]')) { $("#tp-maat").value = d.maat; }
    if (d.mat && M[d.mat]) { $("#tp-mat").value = d.mat; }
    ["lang", "breed", "voegmm", "w", "h"].forEach(function (k) { if (d[k] && isFinite(+d[k])) { $("#tp-" + k).value = d[k]; } });
  }

  // ---------- PNG ----------
  function maakPng(klaar) {
    if (!laatste) { return; }
    var inv = laatste.inv, r = laatste.r;
    var W = 1200, sc = Math.min(W / inv.w, 900 / inv.h), cw = Math.round(inv.w * sc), ch = Math.round(inv.h * sc);
    var balk = 150, pad = 40, out = document.createElement("canvas");
    out.width = Math.max(cw, 800) + pad * 2; out.height = ch + balk + pad * 2;
    var c = out.getContext("2d");
    c.fillStyle = "#ffffff"; c.fillRect(0, 0, out.width, out.height);
    c.save(); c.translate(pad + (out.width - pad * 2 - cw) / 2, pad);
    c.beginPath(); c.rect(0, 0, cw, ch); c.clip();
    var oud = ctx; ctx = c; teken(c, inv, cw, ch, sc / 100); ctx = oud;
    c.restore();
    c.fillStyle = "#16303a"; c.font = "bold 30px system-ui, sans-serif";
    c.fillText(P[inv.patroon].naam + " · " + maatTekst(inv) + " · " + M[inv.mat].naam, pad, pad + ch + 52);
    c.fillStyle = "#4d5a5f"; c.font = "22px system-ui, sans-serif";
    c.fillText(nl(r.m2, 2) + " m² · ongeveer " + nl(r.bruto) + " tegels incl. " + Math.round(r.verlies * 100) + "% snijverlies · voeg " + nl(inv.voegmm) + " mm", pad, pad + ch + 90);
    c.fillStyle = "#8a9599"; c.font = "18px system-ui, sans-serif";
    c.fillText("Illustratie gemaakt met de tegelpatroon-tool van Top Badkamers", pad, pad + ch + 124);
    out.toBlob(klaar, "image/png");
  }
  $("[data-tp-png]").addEventListener("click", function () {
    var knop = this;
    maakPng(function (blob) {
      if (!blob) { return; }
      var url = URL.createObjectURL(blob), a = document.createElement("a");
      a.href = url; a.download = "tegelpatroon-" + laatste.inv.patroon + ".png";
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      knop.blur();
    });
  });
  $("[data-tp-link]").addEventListener("click", function () {
    var meld = $("[data-tp-meld]");
    var klaar = function () { meld.textContent = "Link gekopieerd. Plak hem in een bericht of mail."; };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(location.href).then(klaar, function () { meld.textContent = "Kopieer de link uit de adresbalk."; });
    } else { meld.textContent = "Kopieer de link uit de adresbalk."; }
  });

  laadUitLink();
  var wacht = null;
  function later() { if (wacht) { cancelAnimationFrame(wacht); } wacht = requestAnimationFrame(toon); }
  root.addEventListener("input", later);
  root.addEventListener("change", later);
  window.addEventListener("resize", later);
  toon();
})();
"""

CSS = """<style>
.tp-tool{background:#fff;border:1px solid var(--line);border-radius:var(--radius-lg);box-shadow:var(--shadow);padding:18px}
@media(min-width:900px){.tp-tool{padding:28px;display:grid;grid-template-columns:340px 1fr;gap:28px;align-items:start}}
.tp-in{display:grid;gap:16px}
.tp-tool fieldset{border:0;margin:0;padding:0;min-width:0}
.tp-tool legend,.tp-lbl{font-weight:700;color:var(--ink);margin-bottom:8px;display:block}
.tp-keuze{display:flex;flex-wrap:wrap;gap:6px}
.tp-keuze label{display:flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;padding:6px 11px;cursor:pointer;font-size:.9rem;color:var(--ink)}
.tp-keuze input{accent-color:var(--accent)}
.tp-keuze label:has(input:checked){border-color:var(--navy);background:var(--bg-soft)}
.tp-voegen label{padding:5px 10px 5px 6px}
.tp-voegen i{display:inline-block;width:16px;height:16px;border-radius:50%;border:1px solid rgba(0,0,0,.2)}
.tp-tool select,.tp-tool input[type=number]{width:100%;padding:9px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;color:var(--ink);background:#fff}
.tp-twee{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.tp-twee[hidden]{display:none}
.tp-twee label{font-size:.85rem;color:var(--muted)}
.tp-tool input[type=range]{width:100%;accent-color:var(--accent)}
.tp-doek{background:var(--bg-soft);border-radius:var(--radius);padding:10px;display:flex;justify-content:center;min-height:260px;align-items:center;overflow:hidden}
.tp-doek canvas{display:block;max-width:100%;border-radius:4px;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.tp-sub{font-size:.85rem;color:var(--muted);margin:8px 0 14px}
.tp-sam{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin-bottom:10px}
.tp-sam div{background:var(--bg-soft);border-radius:var(--radius);padding:12px}
.tp-sam small{display:block;color:var(--muted);font-size:.8rem}
.tp-sam b{font-size:1.1rem;color:var(--ink)}
.tp-noot{font-size:.86rem;color:var(--body);margin:4px 0}
.tp-uitleg{background:var(--accent-soft);border-radius:var(--radius);padding:10px 12px;font-size:.9rem;margin:12px 0}
.tp-knoppen{display:flex;flex-wrap:wrap;gap:10px;margin-top:14px}
.tp-meld{font-size:.85rem;color:var(--muted);min-height:1.2em;margin:6px 0 0}
@media(prefers-reduced-motion:no-preference){.tp-keuze label{transition:background-color .15s,border-color .15s}}
</style>"""


def _tool_html():
    pat = "".join(
        f'<label><input type="radio" name="tp-patroon" value="{p["id"]}"{" checked" if i == 0 else ""}> {p["naam"]}</label>'
        for i, p in enumerate(PATRONEN))
    maten = "".join(
        f'<option value="{n}" data-l="{l}" data-b="{b}"{" selected" if n == "30x60" else ""}>{n} cm</option>'
        for n, l, b in MATEN) + '<option value="eigen">Eigen maat…</option>'
    mats = "".join(f'<option value="{m["id"]}">{m["naam"]}</option>' for m in MATERIALEN)
    voegen = "".join(
        f'<label title="{n}"><input type="radio" name="tp-voeg" value="{k}"{" checked" if n == "Lichtgrijs" else ""}>'
        f'<i style="background:{k}"></i> {n}</label>'
        for n, k in VOEGKLEUREN)
    return f"""<div class="tp-tool" data-tp>
  <form class="tp-in" onsubmit="return false">
    <fieldset><legend>1. Legpatroon</legend><div class="tp-keuze">{pat}</div></fieldset>
    <div><label class="tp-lbl" for="tp-maat">2. Tegelmaat</label>
      <select id="tp-maat">{maten}</select>
      <div class="tp-twee" data-tp-eigen hidden style="margin-top:8px">
        <label>Lengte in cm<input type="number" id="tp-lang" value="60" min="2" max="200" step="0.5" inputmode="decimal"></label>
        <label>Breedte in cm<input type="number" id="tp-breed" value="30" min="2" max="200" step="0.5" inputmode="decimal"></label>
      </div></div>
    <div><label class="tp-lbl" for="tp-mat">3. Tegelkleur of materiaal</label><select id="tp-mat">{mats}</select></div>
    <fieldset><legend>4. Voegkleur</legend><div class="tp-keuze tp-voegen">{voegen}</div></fieldset>
    <div><label class="tp-lbl" for="tp-voegmm">5. Voegbreedte: <span data-tp-mmw>3 mm</span></label>
      <input type="range" id="tp-voegmm" min="1" max="10" step="1" value="3"></div>
    <fieldset><legend>6. Wand of vloer en afmetingen</legend>
      <div class="tp-keuze" style="margin-bottom:8px">
        <label><input type="radio" name="tp-soort" value="wand" checked> Wand</label>
        <label><input type="radio" name="tp-soort" value="vloer"> Vloer</label></div>
      <div class="tp-twee">
        <label>Breedte (m)<input type="number" id="tp-w" value="2.4" min="0.3" max="12" step="0.05" inputmode="decimal"></label>
        <label>Hoogte of lengte (m)<input type="number" id="tp-h" value="2.6" min="0.3" max="12" step="0.05" inputmode="decimal"></label>
      </div></fieldset>
  </form>
  <div>
    <div class="tp-doek"><canvas id="tp-canvas" role="img" aria-label="Voorbeeld van het gekozen tegelpatroon"></canvas></div>
    <p class="tp-sub" data-tp-sub></p>
    <div aria-live="polite">
      <div class="tp-sam">
        <div><small>Oppervlak</small><b data-tp-m2>–</b></div>
        <div><small>Aantal tegels</small><b data-tp-aantal>–</b></div>
        <div><small>Leggen (incl. btw)</small><b data-tp-leg>–</b></div>
      </div>
      <p class="tp-noot" data-tp-netto></p>
      <p class="tp-noot" data-tp-legnoot></p>
      <p class="tp-noot">Tegels zelf, als indicatie: <strong data-tp-mat>–</strong> (gewone tot middenklasse tegels, inclusief snijverlies).</p>
      <p class="tp-uitleg" data-tp-uitleg></p>
    </div>
    <div class="tp-knoppen">
      <button type="button" class="btn btn-primary" data-tp-png>Download als PNG</button>
      <button type="button" class="btn btn-ghost" data-tp-link>Kopieer deelbare link</button>
      <a class="btn btn-ghost" href="/kosten/tegelzetter-per-m2/">Wat kost een tegelzetter per m²?</a>
    </div>
    <p class="tp-meld" data-tp-meld aria-live="polite"></p>
    <p style="font-size:.82rem;color:var(--muted);margin:6px 0 0">Het beeld is een illustratie. Echte tegels verschillen per partij in kleur en structuur, en een tegelzetter verdeelt de snijtegels meestal gelijk over beide kanten.</p>
  </div>
</div>"""


def _js():
    data = {
        "patronen": PATRONEN,
        "materialen": MATERIALEN,
        "prijs": PRIJS,
    }
    return "<script>\n" + JS.replace("__DATA__", json.dumps(data, ensure_ascii=False)) + "</script>"


def _uitleg_html():
    rijen = "".join(
        f"<tr><td>{p['naam']}</td><td>{round(p['verlies'] * 100)}%</td>"
        f"<td>{'geen' if not p['toeslag'] else '+' + str(round(p['toeslag'] * 100)) + '%'}</td></tr>"
        for p in PATRONEN)
    leg_lo, leg_hi = PRIJS["leg"]
    hulp = PRIJS["hulp"][0]
    t_lo, t_hi = PRIJS["tegels"]
    bronnen = "; ".join(f'<a href="{u}" rel="nofollow noopener" target="_blank">{n}</a>'
                        for n, u in RP.bron_links("tegelwerk"))
    return f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Zo kies je een legpatroon</h2>
  <p>Het legpatroon bepaalt hoe een badkamer aanvoelt. <strong>Recht</strong> en <strong>verticaal</strong> zijn rustig en strak. <strong>Halfsteens</strong> geeft beweging en verbergt kleine maatverschillen tussen tegels. <strong>Visgraat</strong>, <strong>Hongaarse punt</strong> en <strong>blokverband</strong> zijn opvallend en passen goed op één wand of op de vloer, terwijl de rest van de badkamer rustig blijft.</p>
  <p>Let bij halfsteens op langwerpige tegels van 60 cm of langer. Die zijn vaak een klein beetje bol. Veel fabrikanten raden dan aan om maximaal een derde op te schuiven in plaats van de helft. Vraag dit na bij je tegelzetter.</p>
  <h3>Voegkleur en voegbreedte</h3>
  <p>Een voeg in de kleur van de tegel maakt het vlak rustig en de tegels lijken groter. Een voeg die afsteekt, laat het patroon juist zien. Kleine wandtegels krijgen meestal een voeg van 2 tot 3 mm, grote vloertegels vaak 3 tot 5 mm. Gerectificeerde tegels (met strak afgezaagde randen) kunnen een smallere voeg hebben.</p>
  <h3>Snijverlies en toeslag per patroon</h3>
  <div class="tablewrap"><table>
    <thead><tr><th>Patroon</th><th>Snijverlies</th><th>Toeslag legloon</th></tr></thead><tbody>{rijen}</tbody></table></div>
  <p>Het snijverlies is een vuistregel. Bij veel hoeken, nissen of een kleine ruimte heb je meer nodig. Neem altijd een paar tegels extra uit dezelfde partij, voor als er later een tegel kapot gaat. Bij tegels van 90 cm of groter en bij heel kleine tegels (10 cm of kleiner) rekent de tool 15% extra legloon, omdat dat werk zwaarder of preciezer is. De toeslagen zijn een eigen inschatting.</p>
  <h3>Hoe rekent de tool de kosten?</h3>
  <p>Het legloon is {eur(leg_lo)} tot {eur(leg_hi)} per m², met daarbij ongeveer {eur(hulp)} per m² voor lijm, voeg en kit. Dat zijn de richtprijzen die we op de hele site gebruiken, inclusief 21% btw. Tegels zelf kosten meestal {eur(t_lo)} tot {eur(t_hi)} per m². Natuursteen en groot formaat kunnen duurder zijn. Egaliseren, waterdicht maken en slopen zitten er niet in. Meer rekenvoorbeelden vind je bij <a href="/kosten/tegelzetter-per-m2/">wat een tegelzetter per m² kost</a>.</p>
  <p style="font-size:.85rem;color:var(--muted)">Bronnen legloon (november 2026): {bronnen}. Snijverlies: gangbare vuistregels van tegelzetters en bouwmarkten.</p>
</div></section>"""


FAQS = [
    ("Hoeveel snijverlies moet ik rekenen bij visgraat?",
     "Reken bij visgraat op ongeveer 15% extra tegels, en bij een Hongaarse punt op ongeveer 18%. Bij een recht patroon is 5 tot 10% meestal genoeg. In een kleine ruimte met veel hoeken heb je meer nodig."),
    ("Is visgraat leggen duurder?",
     "Meestal wel. Een tegelzetter moet meer zagen en uitlijnen, dus hij doet minder vierkante meter per dag. Vraag in de offerte of er een toeslag voor het patroon in zit en hoe hoog die is."),
    ("Welke voegkleur past bij mijn tegels?",
     "Kies een voeg in de kleur van de tegel als je een rustig vlak wilt. Kies een lichtere of donkerdere voeg als je het patroon wilt laten zien. Een lichtgrijze voeg is in de douche praktischer dan wit, omdat vuil minder opvalt."),
    ("Kan ik halfsteens leggen met grote tegels?",
     "Dat kan, maar langwerpige tegels van 60 cm of langer zijn vaak licht bol. Schuif dan bij voorkeur een derde op in plaats van de helft, anders zie je hoogteverschil tussen de tegels. Kijk wat de fabrikant van je tegel adviseert."),
    ("Klopt het beeld precies met het echte resultaat?",
     "Nee, het is een illustratie. Echte tegels verschillen per partij in kleur en structuur. Een tegelzetter begint ook vaak in het midden van de wand, zodat de snijtegels aan beide kanten even breed zijn."),
]


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Tegelpatroon", None)])
    faq_html, faq_ld = faq_blok(FAQS, "Veelgestelde vragen over tegelpatronen")
    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Tegelpatroon-visualizer",
        "applicationCategory": "DesignApplication",
        "operatingSystem": "Alle browsers",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Bekijk tegelpatronen zoals visgraat, halfsteens en Hongaarse punt en reken het aantal tegels, het snijverlies en de legkosten uit.",
    }
    body = f"""{cr}
{CSS}
<section class="section-sm"><div class="wrap">
  <div class="narrow prose" style="margin-bottom:22px">
    <span class="badge">Gratis tool</span>
    <h1>Tegelpatroon bekijken en tegels uitrekenen</h1>
    <p class="lead">Kies een legpatroon, de tegelmaat, de kleur en de voeg. Je ziet direct hoe je wand of vloer eruitziet, hoeveel tegels je nodig hebt en wat het leggen ongeveer kost.</p>
  </div>
  {_tool_html()}
</div></section>
{_uitleg_html()}
{faq_html}
{cta_blok("Weet je welk patroon je wilt?", "Vraag gratis offertes aan bij maximaal drie badkamerspecialisten uit je regio. Noem het patroon en de tegelmaat, dan kunnen ze een prijs per m² geven die klopt.", "Gratis offertes aanvragen")}
{_js()}"""
    write(PAD, page(
        title("Tegelpatroon bekijken: visgraat, halfsteens en meer"),
        desc("Bekijk gratis tegelpatronen als visgraat, halfsteens en Hongaarse punt.",
             "Kies maat, kleur en voeg en zie het aantal tegels, het snijverlies en de legkosten."),
        PAD, body, jsonld=[cr_ld, app_ld, faq_ld]), prio=0.7)
