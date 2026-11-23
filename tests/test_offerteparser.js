#!/usr/bin/env node
/* Tests voor de offerteparsers.
   Deel 1: badkamerparser (offerte_parser_badkamer.js): producten herkennen, beoordelen en de
           geanonimiseerde specificatie, met een eigen kleine productdata-fixture (PD), zodat de
           test niet afhangt van producten_data_kranen.py / producten_data_sanitair.py.
   Deel 2: de oorspronkelijke parser (offerte_parser.js) met de voorbeeldoffertes in tests/offertes/.
           Die map staat in Topschilder; ontbreekt hij hier, dan wordt deel 2 overgeslagen.
           Andere map:  OFFERTES_MAP=/pad/naar/offertes node tests/test_offerteparser.js
   Draai:  node tests/test_offerteparser.js
   Met een echte pdf erbij (wordt niet in de repo gezet):
           OFFERTE_PDF=/pad/naar/offerte.pdf node tests/test_offerteparser.js
   Voor de pdf moeten de totalen gelijk zijn aan die van 00-echte-offerte-geanonimiseerd.txt. */
"use strict";
var fs = require("fs"), path = require("path");
var P = require("../offerte_parser.js");
var MAP = process.env.OFFERTES_MAP || path.join(__dirname, "offertes");

// Per testgeval: wat er minimaal uit moet komen. posten = types van de posten die meetellen.
var VERWACHT = {
  "00-echte-offerte-geanonimiseerd.txt": {
    excl: 6608, incl: 7283.36, btw: 675.36, tarieven: [9, 21], basis: "excl", klopt: true,
    posten: ["voorbereiding", "voorbereiding", "voorbereiding", "wanden", "plafonds", "wanden", "wanden", "plafonds",
             "deur", "binnenkozijn", "plinten", "voorbereiding", "behang", "materiaal"],
    details: [
      { i: 3, aantal: 62, eenheid: "m2", eenheidsprijs: 12, bedrag: 744 },
      { i: 10, aantal: 24, eenheid: "m", bedrag: 216 },
      { i: 13, aantal: 8, eenheid: "rol", btw: 21, bedrag: 672 }
    ],
    termijnen: [2185.01, 5098.35], garantie: "12 maanden", geldigheid: "t/m 22 dec. 2026",
    lagen: 2, merken: ["Sikkens"], doorlooptijd: "8 tot 10 werkdagen", concept: true
  },
  "01-subtotaal-btw-totaal.txt": {
    excl: 2881, incl: 3140.29, btw: 259.29, tarieven: [9], basis: "excl", klopt: true,
    posten: ["buitenkozijn", "buitendeur", "boeidelen", "steiger", "houtrot"],
    details: [
      { i: 0, aantal: 8, eenheid: "st", eenheidsprijs: 150, bedrag: 1200 },
      { i: 2, aantal: 18, eenheid: "m", bedrag: 396 },
      { i: 4, aantal: 3, eenheid: "st", bedrag: 285 }
    ],
    garantie: "2 jaar", merken: ["Sikkens"], lagen: 2, buiten: true
  },
  "02-tabel-op-een-regel.txt": {
    excl: 1930, incl: 2103.7, btw: 173.7, tarieven: [9], basis: "excl", klopt: true,
    posten: ["buitenkozijn", "buitenkozijn", "buitendeur", "glaslatten"],
    details: [{ i: 1, aantal: 5, eenheidsprijs: 135, bedrag: 675 }, { i: 3, aantal: 14, eenheid: "m", bedrag: 175 }]
  },
  "03-korting-incl-btw.txt": {
    incl: 2800, excl: 2568.81, tarieven: [9], basis: "incl", klopt: true, subtotaal: 2936,
    posten: ["wanden", "plafonds", "trap", "deur", "korting"],
    details: [{ i: 1, aantal: 36, eenheid: "m2", bedrag: 648 }, { i: 3, aantal: 5, eenheid: "st" }, { i: 4, bedrag: -136 }]
  },
  "04-stelpost-uurloon.txt": {
    excl: 3456, incl: 4181.76, tarieven: [21], basis: "excl", klopt: true, uurloon: 52.5,
    posten: ["buitenkozijn", "dakkapel", "houtrot", "kitwerk", "boeidelen"],
    details: [
      { i: 0, aantal: 9, eenheid: "st", omschrijvingBegint: "Kozijnen" },
      { i: 2, stelpost: true, bedrag: 400 },
      { i: 3, aantal: 32, eenheid: "m" },
      { i: 4, aantal: 22, eenheid: "m" }
    ],
    vraagBevat: "21% btw"
  },
  "05-varianten.txt": {
    excl: 2890, incl: 3150.1, tarieven: [9], klopt: true, varianten: [2890, 3900],
    posten: ["buitenkozijn", "boeidelen", "steiger"],
    nietMeetellen: 3, garantie: "5 jaar"
  },
  "06-opties-na-totaal.txt": {
    excl: 2430, incl: 2648.7, btw: 218.7, tarieven: [9], basis: "excl", klopt: true,
    posten: ["wanden", "plafonds", "wanden", "binnenkozijn", "voorbereiding"],
    nietMeetellen: 2, geldigheid: "30 dagen"
  },
  "07-eenheidsprijs-zonder-totaal.txt": {
    incl: 1772, excl: null, basis: "incl",
    posten: ["keukenfront", "uren", "plafonds", "materiaal"],
    details: [
      { i: 0, aantal: 16, eenheid: "st", eenheidsprijs: 70, bedrag: 1120, berekend: true },
      { i: 1, aantal: 6, eenheid: "uur", bedrag: 297 },
      { i: 2, aantal: 14, eenheid: "m2", bedrag: 210 }
    ],
    uurloon: 49.5
  },
  "08-alleen-totaal.txt": {
    excl: null, incl: null, twijfel: 2450, posten: [], lagen: 2, buiten: true
  },
  "09-termijnen-en-21-procent.txt": {
    excl: 3117, incl: 3771.57, btw: 654.57, tarieven: [21], basis: "excl", klopt: true,
    posten: ["wanden", "binnenkozijn", "uren"], termijnen: [1885.79, 1885.78], uurloon: 55,
    geldigheid: "tot 31-12-2026", vraagBevat: "50%"
  }
};

var fouten = 0, getest = 0;
function check(naam, wat, kreeg, wilde) {
  getest++;
  var ok = JSON.stringify(kreeg) === JSON.stringify(wilde) ||
    (typeof wilde === "number" && typeof kreeg === "number" && Math.abs(kreeg - wilde) < 0.011);
  if (!ok) { fouten++; console.log("  FOUT " + naam + " · " + wat + ": kreeg " + JSON.stringify(kreeg) + ", verwacht " + JSON.stringify(wilde)); }
}

function test(naam, tekst, v) {
  var r = P.leesOfferte(tekst);
  var tellen = r.posten.filter(function (p) { return p.meetellen; });
  if ("excl" in v) check(naam, "totaal excl", r.totaal.excl, v.excl);
  if ("incl" in v) check(naam, "totaal incl", r.totaal.incl, v.incl);
  if ("btw" in v) check(naam, "btw-bedrag", r.totaal.btw, v.btw);
  if (v.tarieven) check(naam, "btw-tarieven", r.btwTarieven, v.tarieven);
  if (v.basis) check(naam, "basis", r.basis, v.basis);
  if ("klopt" in v) check(naam, "posten tellen op tot totaal", r.controle.klopt, v.klopt);
  if ("subtotaal" in v) check(naam, "subtotaal", r.subtotaal, v.subtotaal);
  if (v.posten) check(naam, "post-types", tellen.map(function (p) { return p.type; }), v.posten);
  if ("nietMeetellen" in v) check(naam, "posten die niet meetellen", r.posten.length - tellen.length, v.nietMeetellen);
  (v.details || []).forEach(function (d) {
    var p = tellen[d.i] || {};
    Object.keys(d).forEach(function (k) {
      if (k === "i") return;
      if (k === "omschrijvingBegint") check(naam, "post " + d.i + " omschrijving", (p.omschrijving || "").indexOf(d[k]) === 0, true);
      else check(naam, "post " + d.i + " " + k, p[k], d[k]);
    });
  });
  if (v.termijnen) check(naam, "termijnen", r.termijnen.map(function (t) { return t.bedrag; }), v.termijnen);
  if (v.varianten) check(naam, "varianten", r.varianten.map(function (x) { return x.totaal; }), v.varianten);
  if ("twijfel" in v) check(naam, "totaal zonder btw-aanduiding", r.totaal.twijfel, v.twijfel);
  ["garantie", "geldigheid", "uurloon", "doorlooptijd", "concept", "buiten"].forEach(function (k) {
    if (k in v) check(naam, k, r[k], v[k]);
  });
  if ("lagen" in v) check(naam, "aantal lagen", r.lagen.aantal, v.lagen);
  if (v.merken) check(naam, "verfmerk", r.merken, v.merken);
  if (v.vraagBevat) {
    var vragen = P.algemeneVragen(r).concat.apply(P.algemeneVragen(r), r.posten.map(function (p) {
      return P.beoordeelPost(p, {}, 1, r.basis, r.btwTarieven[0]).vragen;
    }));
    check(naam, "vraag met '" + v.vraagBevat + "'", vragen.some(function (q) { return q.indexOf(v.vraagBevat) >= 0; }), true);
  }
  return r;
}

/* ======================================================================= Deel 1: badkamerparser */
console.log("Deel 1: offerte_parser_badkamer.js");
var TB = require("../offerte_parser_badkamer.js");

// Kleine eigen productdata in het formaat van producten_badkamer.als_json(). Prijzen zijn
// testwaarden, geen marktgegevens.
var PD = {
  peildatum: "2026-11",
  merken: [
    { naam: "Grohe", aliassen: ["grohe"], code_regex: ["\\b\\d{5}(?:000|001|002|DC0|GL0|GN0|DA0|DL0|AL0|A00|BE0|EN0)\\b"] },
    { naam: "Hansgrohe", aliassen: ["hansgrohe", "hans grohe"], code_regex: ["\\b\\d{5}(?:000|670|700|990|140|250|340|800)\\b"] },
    { naam: "Geberit", aliassen: ["geberit"], code_regex: ["\\b\\d{3}\\.\\d{3}\\.\\w{2}\\.\\d\\b"] },
    { naam: "Villeroy & Boch", aliassen: ["villeroy & boch", "villeroy", "v&b"] },
    { naam: "Sphinx", aliassen: ["sphinx"] },
    { naam: "Easy Drain", aliassen: ["easy drain", "easydrain"] }
  ],
  categorieen: {
    thermostaatkraan: { naam: "Thermostaatkraan douche (opbouw)", trefwoorden: ["thermostaatkraan", "thermostaat", "thermostatisch", "douchekraan", "grohtherm"], van: 50, tot: 400, bron: ["werkspot_kraan"] },
    douchesysteem: { naam: "Douchesysteem of regendoucheset", trefwoorden: ["douchesysteem", "regendoucheset", "regendouche", "hoofddouche"], van: 100, tot: 1500, bron: ["aanbod"] },
    handdouche_set: { naam: "Glijstangset of handdouche", trefwoorden: ["glijstangset", "glijstang", "handdouche"], van: 25, tot: 250, bron: ["aanbod"] },
    wastafelkraan: { naam: "Wastafelkraan", trefwoorden: ["wastafelkraan", "wastafelmengkraan", "fonteinkraan", "kraan"], van: 40, tot: 600, bron: ["aanbod"] },
    inbouwkraan: { naam: "Inbouwkraan of inbouwthermostaat (incl. inbouwdeel)", trefwoorden: ["inbouwthermostaat", "inbouwkraan", "inbouwdeel", "smartbox", "rapido"], van: 100, tot: 900, bron: ["aanbod"] },
    douchegoot: { naam: "Douchegoot of doucheput", trefwoorden: ["douchegoot", "doucheput", "goot"], van: 50, tot: 700, bron: ["werkspot_goot"] },
    hangtoilet: { naam: "Hangtoilet (pot)", trefwoorden: ["hangtoilet", "wandcloset", "toilet", "closet", "wc"], van: 100, tot: 900, bron: ["bobex_toilet"] },
    inbouwreservoir: { naam: "Inbouwreservoir (frame)", trefwoorden: ["inbouwreservoir", "duofix", "up320", "reservoir"], van: 100, tot: 400, bron: ["homedeal_toilet"] },
    bedieningsplaat: { naam: "Bedieningsplaat toilet", trefwoorden: ["bedieningsplaat", "drukplaat", "sigma01", "sigma20"], van: 40, tot: 450, bron: ["aanbod"] },
    toiletzitting: { naam: "Toiletzitting", trefwoorden: ["toiletzitting", "toiletbril", "zitting met deksel"], van: 25, tot: 200, bron: ["aanbod"] },
    wastafelmeubel: { naam: "Wastafelmeubel (kast met wastafel)", trefwoorden: ["wastafelmeubel", "badmeubel", "badkamermeubel"], van: 100, tot: 2500, bron: ["slimster_meubel"] },
    wastafel: { naam: "Wastafel (los)", trefwoorden: ["wastafel"], van: 50, tot: 700, bron: ["aanbod"] },
    douchewand: { naam: "Douchewand of inloopwand", trefwoorden: ["douchewand", "inloopwand", "inloopdouche"], van: 150, tot: 2000, bron: ["slimster_inloop"] },
    spiegel_kast: { naam: "Spiegel of spiegelkast", trefwoorden: ["spiegelkast", "spiegel"], van: 40, tot: 900, bron: ["aanbod"] },
    tegels: { naam: "Tegels (per m²)", eenheid: "m2", trefwoorden: ["wandtegels", "vloertegels", "tegels"], van: 10, tot: 160, bron: ["slimster_tegels"] }
  },
  artikelen: [
    { merk: "Grohe", serie: "Grohtherm 800", oms: "Thermostatische douchekraan opbouw, chroom", categorie: "thermostaatkraan", codes: ["34558000"], ean: ["4005176934261"], van: 129, tot: 189, bron: "test" },
    { merk: "Grohe", serie: "Eurosmart", oms: "Wastafelmengkraan S-size, chroom", categorie: "wastafelkraan", codes: ["32467002"], ean: [], van: 55, tot: 95, bron: "test" },
    { merk: "Grohe", serie: "Rapido SmartBox", oms: "Universeel inbouwdeel", categorie: "inbouwkraan", codes: ["35600000"], ean: [], van: 95, tot: 140, bron: "test" },
    { merk: "Hansgrohe", serie: "Croma Select S", oms: "Glijstangset 65 cm, wit/chroom", categorie: "handdouche_set", codes: ["26566400"], ean: [], van: 55, tot: 90, bron: "test" },
    { merk: "Geberit", serie: "Sigma01", oms: "Bedieningsplaat, glans chroom", categorie: "bedieningsplaat", codes: ["115.770.21.5"], ean: [], van: 52, tot: 75, bron: "test" },
    { merk: "Geberit", serie: "Duofix UP320", oms: "Inbouwreservoir Duofix met Sigma UP320", categorie: "inbouwreservoir", codes: ["111.300.00.5"], ean: [], van: 230, tot: 330, bron: "test" },
    { merk: "Villeroy & Boch", serie: "Subway 2.0", oms: "Hangtoilet DirectFlush, wit", categorie: "hangtoilet", codes: ["5614R001"], ean: [], van: 250, tot: 380, bron: "test" },
    { merk: "Villeroy & Boch", serie: "Subway 2.0", oms: "Toiletzitting met deksel, softclose", categorie: "toiletzitting", codes: ["9M68S101"], ean: [], van: 75, tot: 130, bron: "test" }
  ],
  bronnen: {
    test: ["Testbron (fixture)", null], aanbod: ["Eigen vergelijking van het aanbod", null],
    werkspot_kraan: ["Werkspot: douchekraan vervangen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/douchekraan-vervangen"],
    werkspot_goot: ["Werkspot: douchegoot plaatsen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/douchegoot-plaatsen"],
    bobex_toilet: ["Bobex: toilet", "https://www.bobex.be/nl-be/badkamerrenovatie/toilet/"],
    homedeal_toilet: ["Homedeal: toilet renoveren", "https://www.homedeal.nl/verbouwing/toilet-renovatie"],
    slimster_meubel: ["Slimster: badkamermeubel", "https://slimster.nl/badkamer/prijzen/badkamermeubel"],
    slimster_inloop: ["Slimster: inloopdouche", "https://slimster.nl/badkamer/douche-plaatsen-kosten/inloopdouche/"],
    slimster_tegels: ["Slimster: vloertegels", "https://slimster.nl/tegelzetter/vloertegels-prijzen/kosten-keramische-vloertegels/"]
  }
};

function zoekPost(r, begin) {
  return r.posten.filter(function (p) { return p.omschrijving.toLowerCase().indexOf(begin.toLowerCase()) >= 0; })[0] || {};
}
function verwachtPost(naam, r, begin, v) {
  var p = zoekPost(r, begin), h = p.product || {}, o = p.productOordeel || {};
  if (!p.omschrijving) { check(naam, "post '" + begin + "' gevonden", false, true); return; }
  var w = { soort: p.soort, merk: h.merk, serie: h.serie, code: h.code, ean: h.ean, categorie: h.categorie, match: h.match,
    oordeel: o.oordeel, band: o.band && o.band.soort, verschilPct: o.verschilPct, prijs: o.prijs, aantal: o.aantal, vaag: p.vaag };
  Object.keys(v).forEach(function (k) { check(naam, "'" + begin + "' " + k, w[k], v[k]); });
}
function geval(naam, tekst, verwacht, extra) {
  var voor = fouten;
  var r = TB.leesOfferte(tekst, { producten: PD });
  Object.keys(verwacht).forEach(function (b) { verwachtPost(naam, r, b, verwacht[b]); });
  if (extra) extra(r, naam);
  console.log((fouten === voor ? "ok   " : "FOUT ") + naam);
  return r;
}

// 1. Nette offerte, bedragen excl. 21% btw, met artikelnummers en EAN.
var OFF1 = [
  "Offerte badkamerrenovatie",
  "Alle bedragen zijn exclusief 21% btw.",
  "Omschrijving                                                     Aantal   Prijs      Totaal",
  "Slopen bestaande badkamer incl. afvoer puin                      1 post             € 850,00",
  "Grohe Grohtherm 800 douchethermostaat 34558000                   1 st     € 165,00  € 165,00",
  "Grohe Rapido SmartBox inbouwdeel art. 35600000                   1 st     € 110,00  € 110,00",
  "Hansgrohe Croma Select S glijstangset 26566400                   1 st     € 95,00   € 95,00",
  "Geberit Duofix UP320 inbouwreservoir 111.300.00.5                1 st     € 245,00  € 245,00",
  "Geberit Sigma01 bedieningsplaat glans chroom 115.770.21.5        1 st     € 89,00   € 89,00",
  "Villeroy & Boch Subway 2.0 hangtoilet DirectFlush 5614R001       1 st     € 325,00  € 325,00",
  "Wandtegels 30x60 mat wit                                         18 m2    € 32,00   € 576,00",
  "Tegelwerk wanden en vloer zetten                                 24 m2    € 55,00   € 1.320,00",
  "Montage sanitair                                                 1 post             € 650,00",
  "Tegellijm, voegmiddel en kimband                                 1 post             € 185,00",
  "Subtotaal excl. btw                                                                 € 4.610,00",
  "Btw 21%                                                                             € 968,10",
  "Totaal incl. btw                                                                    € 5.578,10"
].join("\n");
geval("1 nette offerte met artikelnummers", OFF1, {
  // 165 excl = 199,65 incl; band 129–189 → 6% boven de bovenkant, binnen de marge van 25%.
  "Grohtherm 800": { soort: "product", merk: "Grohe", serie: "Grohtherm 800", match: "exact", categorie: "thermostaatkraan", oordeel: "binnen", band: "artikel", verschilPct: 6, prijs: 199.65 },
  "Rapido": { soort: "product", match: "exact", categorie: "inbouwkraan", oordeel: "binnen" },
  "Croma Select": { soort: "product", merk: "Hansgrohe", match: "exact", categorie: "handdouche_set", verschilPct: 28, oordeel: "boven" },
  "Duofix": { match: "exact", code: "111.300.00.5", oordeel: "binnen" },
  // 89 excl = 107,69 incl; band 52–75 → 44% boven.
  "Sigma01": { match: "exact", categorie: "bedieningsplaat", oordeel: "boven", verschilPct: 44 },
  "Subway 2.0": { merk: "Villeroy & Boch", match: "exact", categorie: "hangtoilet", oordeel: "binnen" },
  // 32 excl = 38,72 per m² incl; categorieband 10–160 per m².
  "Wandtegels": { soort: "product", categorie: "tegels", match: "categorie", oordeel: "binnen", band: "categorie", prijs: 38.72 },
  "Tegelwerk": { soort: "arbeid" },
  "Slopen": { soort: "arbeid" },
  "Montage sanitair": { soort: "arbeid", vaag: undefined },
  "Tegellijm": { soort: "materiaal" }
}, function (r, naam) {
  check(naam, "totaal excl", r.totaal.excl, 4610);
  check(naam, "totaal incl", r.totaal.incl, 5578.1);
  check(naam, "basis", r.basis, "excl");
  check(naam, "posten tellen op", r.controle.klopt, true);
  var o = zoekPost(r, "Sigma01").productOordeel;
  check(naam, "toelichting boven noemt band en peildatum", /44% boven de marktprijsband van dit artikel van € 52–€ 75 \(peildatum november 2026\)/.test(o.toelichting.replace(/ /g, " ")), true);
  check(naam, "toelichting boven legt opslag uit", /opslag op materiaal/.test(o.toelichting), true);
  check(naam, "geen oordeelwoorden", /te duur|afzet|duur/i.test(r.posten.map(function (p) { return (p.productOordeel || {}).toelichting || ""; }).join(" ")), false);
  check(naam, "bron van artikel", o.bron, ["test"]);
});

// 2. Rommelige pdf-tekst: kolommen door elkaar, codes met spaties en punten, EAN zonder merk,
//    aantallen als "2x", bedragen incl. btw.
var OFF2 = [
  "BADKAMERS & ZO      pagina 1/2",
  "Pos  Omschrijving    Aantal    Bedrag",
  "1.   Art.nr.: 34 558 000  Grohe   douchethermostaat   chroom      € 239,00",
  "2.   2x  Eurosmart wastafelmengkraan  grohe 32467002   à € 79,00   € 158,00",
  "3.   EAN 4005176934261 thermostaat opbouw                         € 175,00",
  "4.   Sphinx 300 toilet randloos  wandcloset                       € 189,00",
  "5.   douchegoot rvs 80cm  Easy Drain                               € 129,00",
  "6.   Inloopdouche  glaswand 100 cm 8 mm antikalk                  € 899,00",
  "7.   Spiegel met LED-verlichting 80x70                            €   20,00",
  "Alle prijzen inclusief 21% BTW",
  "Totaal                                                         € 1.809,00"
].join("\n");
geval("2 rommelige pdf-tekst", OFF2, {
  "34 558 000": { soort: "product", merk: "Grohe", code: "34 558 000", match: "exact", categorie: "thermostaatkraan", verschilPct: 26, oordeel: "boven" },
  "Eurosmart": { soort: "product", match: "exact", aantal: 2, prijs: 79, oordeel: "binnen" },
  "EAN 4005176934261": { match: "exact", ean: "4005176934261", merk: "Grohe", serie: "Grohtherm 800", oordeel: "binnen" },
  // Merk zonder artikel in de data: categorieband.
  "Sphinx 300": { soort: "product", merk: "Sphinx", match: "categorie", categorie: "hangtoilet", band: "categorie", oordeel: "binnen" },
  "douchegoot": { merk: "Easy Drain", categorie: "douchegoot", match: "categorie", oordeel: "binnen" },
  "Inloopdouche": { soort: "product", categorie: "douchewand", oordeel: "binnen" },
  // 20 incl, band 40–900 → 50% onder: check type en maat.
  "Spiegel": { categorie: "spiegel_kast", oordeel: "onder", verschilPct: -50 }
}, function (r, naam) {
  check(naam, "basis", r.basis, "incl");
  check(naam, "totaal incl", r.totaal.incl, 1809);
  var o = zoekPost(r, "Spiegel").productOordeel;
  check(naam, "onder: check type en maat", /Check of het hetzelfde type en dezelfde maat is/.test(o.toelichting), true);
  check(naam, "categorieband zegt dat het grof is", /grove vergelijking/.test(o.toelichting), true);
});

// 3. Offerte met NAW-gegevens, IBAN, KvK en een stelpost sanitair zonder merk.
var OFF3 = [
  "Loodgietersbedrijf De Waterlijn B.V.",
  "Kerkstraat 12, 1234 AB Ergens",
  "Tel. 06-12345678 | info@dewaterlijn.nl | www.dewaterlijn.nl",
  "KvK 12345678 | Btw-nr NL123456789B01 | IBAN NL91 ABNA 0417 1643 00",
  "",
  "T.a.v. dhr. J. Jansen, Dorpsweg 5, 4321 CD Ergens",
  "Offertenummer 2026-117",
  "Geachte heer Jansen,",
  "",
  "Hierbij onze prijsopgave voor uw badkamer. Bedragen exclusief btw.",
  "Sloopwerk badkamer                          € 750,00",
  "Stelpost sanitair compleet                  € 2.500,00",
  "Sanitair: toilet, wastafelmeubel en douche  € 1.800,00",
  "Grohe Grohtherm 800 thermostaatkraan incl. montage   € 295,00",
  "Leidingwerk aanpassen                       € 900,00",
  "Elektra: 2 stopcontacten en spots           € 450,00",
  "Totaal excl. btw                            € 6.695,00",
  "21% btw                                     € 1.405,95",
  "Totaal incl. btw                            € 8.100,95",
  "Betaling: 30% bij opdracht, 70% na oplevering. IBAN NL91ABNA0417164300 o.v.v. offertenummer."
].join("\n");
var r3 = geval("3 offerte met NAW en IBAN", OFF3, {
  "Stelpost sanitair": { soort: "materiaal", vaag: true },
  "Sanitair: toilet": { soort: "materiaal", vaag: true },
  "Grohtherm 800": { soort: "product", match: "serie", oordeel: "onbekend" },
  "Sloopwerk": { soort: "arbeid" },
  "Leidingwerk": { soort: "arbeid" }
}, function (r, naam) {
  check(naam, "vaag-tekst", zoekPost(r, "Stelpost sanitair").vaagTekst, "onvoldoende gespecificeerd: vraag merk en type per onderdeel");
  check(naam, "stelpost blijft type sanitair", zoekPost(r, "Stelpost sanitair").type, "sanitair");
  check(naam, "incl. montage: geen oordeel", /inclusief montage/.test(zoekPost(r, "Grohtherm").productOordeel.toelichting), true);
  var spec = TB.anoniemeSpecificatie(r);
  ["Waterlijn", "Kerkstraat", "1234 AB", "06-12345678", "@", "www.", "12345678", "NL123456789B01", "NL91", "ABNA",
   "Jansen", "Dorpsweg", "Offertenummer", "2026-117", "Geachte", "B.V."].forEach(function (s) {
    check(naam, "specificatie zonder '" + s + "'", spec.indexOf(s) >= 0, false);
  });
  ["Sloopwerk badkamer", "Stelpost sanitair compleet", "Leidingwerk aanpassen", "Totaal excl. btw: € 6.695", "Totaal incl. btw: € 8.100,95",
   "merk en type niet genoemd"].forEach(function (s) {
    check(naam, "specificatie met '" + s + "'", spec.indexOf(s) >= 0, true);
  });
});

// 4. Aantallen (2x kraan), excl/incl btw per regel, een product onder de band en een
//    regel zonder bedrag.
var OFF4 = [
  "Prijsopgave sanitair (prijzen excl. btw)",
  "2 x Grohe Eurosmart wastafelkraan 32467002   à € 45,00    € 90,00",
  "Villeroy & Boch Subway 2.0 toiletzitting 9M68S101          € 49,00",
  "Badmeubel 80 cm eiken met wastafel                         € 790,00",
  "Grohe Grohtherm 1000 douchethermostaat                     € 199,00",
  "Totaal excl. btw                                           € 1.128,00"
].join("\n");
geval("4 aantallen en btw", OFF4, {
  // 45 excl = 54,45 incl per stuk; band 55–95 → net onder, binnen de marge.
  "Eurosmart": { soort: "product", match: "exact", aantal: 2, prijs: 54.45, oordeel: "binnen", verschilPct: -1 },
  // 49 excl = 59,29 incl; band 75–130 → 21% onder.
  "toiletzitting": { match: "exact", categorie: "toiletzitting", oordeel: "onder", verschilPct: -21 },
  "Badmeubel": { soort: "product", categorie: "wastafelmeubel", match: "categorie", oordeel: "binnen" },
  // Grohtherm 1000 staat niet in de fixture: serie "Grohtherm 800" mag niet matchen.
  "Grohtherm 1000": { merk: "Grohe", match: "categorie", categorie: "thermostaatkraan", band: "categorie" }
});

// 4b. Bevindingen browsertest: wastafelmeubel met kraan zonder merk, en de bandtekst bij een serie.
geval("4b wastafelmeubel met kraan", "Bedragen incl. btw\nWastafelmeubel 80 cm met kraan  € 1.150,00\nTotaal incl. btw € 1.150,00", {
  "Wastafelmeubel": { soort: "product", categorie: "wastafelmeubel", match: "categorie", band: "categorie", oordeel: "binnen", vaag: undefined }
}, function (r, naam) {
  var p = zoekPost(r, "Wastafelmeubel");
  var b = TB.beoordeelPost(p, { sanitair: { van: 1500, tot: 9500, eenheid: "post" } }, r.basis, 21);
  check(naam, "nooit tegen de band voor complete sanitair", b.oordeel, null);
  check(naam, "reden", b.reden, "product");
  check(naam, "toelichting noemt categorie", /marktprijsband voor wastafelmeubel/.test(p.productOordeel.toelichting), true);
});
var hs = TB.herkenProduct("Villeroy & Boch Subway 2.0 toiletpot", PD);
var os = TB.beoordeelProduct({ omschrijving: "", bedrag: 300 }, hs, PD, "incl");
check("bandtekst", "serie-match zegt 'van deze serie'", [hs.match, /van deze serie/.test(os.toelichting), /van dit artikel/.test(os.toelichting)], ["serie", true, false]);
var oe = TB.beoordeelProduct({ omschrijving: "", bedrag: 150 }, TB.herkenProduct("Grohe 34558000", PD), PD, "incl");
check("bandtekst", "exacte match zegt 'van dit artikel'", /van dit artikel/.test(oe.toelichting), true);
check("bandtekst", "match staat in het oordeel", oe.match, "exact");

// 5. Losse functies.
[["Montage Geberit inbouwreservoir", "arbeid"], ["Geberit Sigma20 bedieningsplaat", "product"], ["Tegellijm flexibel 25 kg", "materiaal"],
 ["Sanitair volgens showroombezoek", "materiaal"], ["Korting bij opdracht", "overig"], ["Plaatsen douchewand", "arbeid"],
 ["Douchegoot RVS 80 cm", "product"], ["Uren regie", "arbeid"], ["Diversen", "overig"]]
  .forEach(function (x) { check("soortRegel", x[0], TB.soortRegel(x[0], PD), x[1]); });
check("soortRegel zonder PD", "Grohe kraan", TB.soortRegel("Grohe Eurosmart kraan"), "product");
check("herkenProduct", "geen PD", TB.herkenProduct("Grohe 34558000", null), null);
check("herkenProduct", "onbekende tekst", TB.herkenProduct("Diversen en kleinigheden", PD), null);
var hg = TB.herkenProduct("thermostaat 34558999", PD);
check("herkenProduct", "code past bij Grohe én Hansgrohe? nee, alleen formaat Grohe → geen artikel", hg && hg.match, "categorie");
var amb = TB.herkenProduct("douchekraan 12345000", PD);
check("herkenProduct", "code past bij twee merken: geen merk", amb && amb.merk, null);
check("herkenProduct", "Geberit-code zonder artikel geeft merk", (TB.herkenProduct("bedieningsplaat 115.882.KJ.1", PD) || {}).merk, "Geberit");
check("herkenProduct", "Hansgrohe niet als Grohe", (TB.herkenProduct("Hansgrohe Raindance glijstangset", PD) || {}).merk, "Hansgrohe");
check("herkenProduct", "inbouw wint van thermostaat", (TB.herkenProduct("Thermostaat inbouw met afdekplaat", PD) || {}).categorie, "inbouwkraan");
var bo = TB.beoordeelProduct({ omschrijving: "x", bedrag: 100, aantal: 3, eenheid: "m" }, TB.herkenProduct("Grohe 34558000", PD), PD, "incl");
check("beoordeelProduct", "andere eenheid → onbekend", bo.oordeel, "onbekend");
check("beoordeelProduct", "zonder herkenning", TB.beoordeelProduct({ bedrag: 10 }, null, PD, "incl").oordeel, "onbekend");
// Precies op de drempels: 25% boven de bovenkant is nog binnen, daarboven boven.
var hk = TB.herkenProduct("Grohe 34558000", PD);
check("drempel", "189 × 1,25 = 236,25 → binnen", TB.beoordeelProduct({ omschrijving: "", bedrag: 236.25 }, hk, PD, "incl").oordeel, "binnen");
check("drempel", "236,50 → boven", TB.beoordeelProduct({ omschrijving: "", bedrag: 236.5 }, hk, PD, "incl").oordeel, "boven");
check("drempel", "129 × 0,8 = 103,20 → binnen", TB.beoordeelProduct({ omschrijving: "", bedrag: 103.2 }, hk, PD, "incl").oordeel, "binnen");
check("drempel", "103 → onder", TB.beoordeelProduct({ omschrijving: "", bedrag: 103 }, hk, PD, "incl").oordeel, "onder");
check("btw", "9% op de regel telt mee", TB.beoordeelProduct({ omschrijving: "", bedrag: 100, btw: 9 }, hk, PD, "excl").prijs, 109);
// Zonder opties werkt leesOfferte als vroeger (wel met soort).
var r0 = TB.leesOfferte(OFF1);
check("zonder producten", "geen product-veld", r0.posten.some(function (p) { return "product" in p; }), false);
check("zonder producten", "totaal gelijk", r0.totaal.incl, 5578.1);

// 6. Optioneel: de echte productdata uit producten_badkamer.py (als python3 er is).
try {
  var json = require("child_process").execFileSync("python3", ["-c",
    "import json,sys; sys.path.insert(0,'.'); import producten_badkamer as p; print(json.dumps(p.als_json(), ensure_ascii=False))"],
    { cwd: path.join(__dirname, ".."), encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] });
  var ECHT = JSON.parse(json), voor6 = fouten;
  check("echte PD", "24 categorieën", Object.keys(ECHT.categorieen).length, 24);
  Object.keys(ECHT.categorieen).forEach(function (k) {
    var c = ECHT.categorieen[k];
    check("echte PD", k + " heeft band en bronnen", c.van > 0 && c.tot > c.van && c.bron.every(function (b) { return b in ECHT.bronnen; }), true);
  });
  ECHT.artikelen.forEach(function (a) {
    var code = (a.codes || [])[0] || (a.ean || [])[0];
    if (!code) return;
    var h = TB.herkenProduct(a.merk + " " + a.serie + " " + code, ECHT);
    check("echte PD", "artikel " + code + " exact herkend", h && h.match === "exact" && h.artikel === a, true);
  });
  [["Grohe Grohtherm 800 douchethermostaat", "thermostaatkraan"], ["Geberit Sigma20 bedieningsplaat", "bedieningsplaat"],
   ["Villeroy & Boch Subway toiletzitting softclose", "toiletzitting"], ["Badmeubel 100 cm met wastafel", "wastafelmeubel"],
   ["Wastafelkraan chroom", "wastafelkraan"], ["Vrijstaand bad 170 cm", "vrijstaand_bad"], ["Ligbad acryl 170x75", "bad"],
   ["Designradiator 180x60 antraciet", "badkamerradiator"], ["Regendoucheset met thermostaat", "douchesysteem"],
   ["Inbouwreservoir Geberit Duofix", "inbouwreservoir"], ["Fonteinset compleet", "fontein"], ["Toiletrolhouder chroom", "accessoires"],
   ["Douchebak 90x90", "douchebak"], ["Douchecabine kwartrond 90x90", "douchecabine"], ["Vloertegels 60x60", "tegels"],
   ["Hansgrohe Ecostat thermostaat bad", "badkraan"], ["Staand toilet duoblok", "staand_toilet"], ["Douchegoot 80 cm", "douchegoot"]]
    .forEach(function (x) { check("echte PD", "categorie '" + x[0] + "'", (TB.herkenProduct(x[0], ECHT) || {}).categorie, x[1]); });
  // Realistische regels (bevindingen pagina-agent). Alleen als het artikel in de data staat.
  function heeft(merk, serie) { return ECHT.artikelen.some(function (a) { return a.merk === merk && a.serie === serie; }); }
  [["Grohe Grohtherm 800 34558000", "Grohe", "Grohtherm 800", "thermostaatkraan", "exact"],
   ["Geberit Sigma20 bedieningsplaat wit/chroom", "Geberit", "Sigma20", "bedieningsplaat", "serie"],
   ["Villeroy & Boch Subway 2.0 hangtoilet DirectFlush", "Villeroy & Boch", "Subway 2.0", "hangtoilet", "serie"],
   ["Hansgrohe Croma Select S 180 showerpipe", "Hansgrohe", "Croma Select S", "douchesysteem", "serie"]].forEach(function (x) {
    if (!heeft(x[1], x[2])) return;
    var h = TB.herkenProduct(x[0], ECHT) || {};
    check("echte PD", "'" + x[0] + "'", [h.merk, h.serie, h.categorie, h.match], [x[1], x[2], x[3], x[4]]);
  });
  check("echte PD", "code los van getal ervoor", (TB.herkenProduct("Grohe thermostaat 800 34559000", ECHT) || {}).code, "34559000");
  check("echte PD", "Geberit-code los van typenummer", (TB.herkenProduct("Geberit Duofix UP320 111.300.00.5", ECHT) || {}).code, "111.300.00.5");
  var s20 = TB.herkenProduct("Geberit Sigma20 bedieningsplaat wit/chroom", ECHT);
  if (s20 && s20.artikel) check("echte PD", "Sigma20 wit/chroom kiest de witte uitvoering", /wit/.test(s20.artikel.oms), true);
  var s20b = TB.beoordeelProduct({ omschrijving: "", bedrag: 100 }, TB.herkenProduct("Geberit Sigma20 bedieningsplaat", ECHT), ECHT, "incl");
  if (heeft("Geberit", "Sigma20")) check("echte PD", "Sigma20 zonder kleur: band over alle uitvoeringen", s20b.band.varianten > 1, true);
  console.log((fouten === voor6 ? "ok   " : "FOUT ") + "echte productdata (" + ECHT.artikelen.length + " artikelen)");
} catch (e) {
  console.log("     echte productdata overgeslagen (" + String(e.message).split("\n")[0] + ")");
}

if (fs.existsSync(MAP)) {
  console.log("\nDeel 2: offerte_parser.js");
  Object.keys(VERWACHT).forEach(function (naam) {
    var voor = fouten;
    test(naam, fs.readFileSync(path.join(MAP, naam), "utf8"), VERWACHT[naam]);
    console.log((fouten === voor ? "ok   " : "FOUT ") + naam);
  });
} else {
  console.log("\nDeel 2 overgeslagen: map " + MAP + " ontbreekt (staat in Topschilder).");
}

// Losse controles op getallen en soorten.
[["1.234,50", 1234.5], ["€ 1234", 1234], ["1.250", 1250], ["12,5", 12.5], ["1.250,-", 1250], ["-150", -150], ["€ 6.608,00", 6608]]
  .forEach(function (x) { check("getal", x[0], P.getal(x[0]), x[1]); });
[["Boeiboorden en windveren schilderen", "boeidelen"], ["Glaslatten kitten", "glaslatten"], ["Trapgat wanden sausen", "wanden"],
 ["Vloeren en keuken afdekken", "voorbereiding"], ["Behang verwijderen op geselecteerde wanden", "voorbereiding"], ["Hal en trap nieuw behang", "behang"], ["Voordeur lakken", "buitendeur"]]
  .forEach(function (x) { check("soort", x[0], P.bepaalType(x[0], "binnen"), x[1]); });

// Richtprijs-oordeel: 4 binnendeuren à € 125 excl. 9% btw = € 545 incl., band € 65–185 per deur.
var b = P.beoordeelPost({ type: "deur", aantal: 4, eenheid: "st", bedrag: 500, btw: 9 },
  { deur: { van: 65, tot: 185 } }, 1, "excl", 9);
check("oordeel", "binnendeuren", b.oordeel, "binnen");

function klaar() {
  console.log("\n" + (getest - fouten) + " van " + getest + " controles goed.");
  process.exit(fouten ? 1 : 0);
}

// Optioneel: de echte pdf via pdf.js uitlezen, op dezelfde manier als de site.
if (process.env.OFFERTE_PDF) {
  var lib = require("../vendor/pdfjs/pdf.min.js");
  lib.GlobalWorkerOptions.workerSrc = path.join(__dirname, "../vendor/pdfjs/pdf.worker.min.js");
  lib.getDocument({ data: new Uint8Array(fs.readFileSync(process.env.OFFERTE_PDF)), verbosity: 0 }).promise.then(function (doc) {
    var p = [];
    for (var i = 1; i <= doc.numPages; i++) p.push(doc.getPage(i).then(function (pg) { return pg.getTextContent(); }));
    return Promise.all(p);
  }).then(function (inh) {
    var tekst = inh.map(function (c) { return P.regelsUitItems(c.items); }).join("\n");
    var v = VERWACHT["00-echte-offerte-geanonimiseerd.txt"];
    var voor = fouten;
    test("echte pdf", tekst, { excl: v.excl, incl: v.incl, btw: v.btw, tarieven: v.tarieven, klopt: true, posten: v.posten });
    console.log((fouten === voor ? "ok   " : "FOUT ") + "echte pdf (" + path.basename(process.env.OFFERTE_PDF).replace(/./g, "*").slice(0, 8) + ")");
    klaar();
  }).catch(function (e) { console.log("pdf niet te lezen: " + e.message); fouten++; klaar(); });
} else {
  klaar();
}
