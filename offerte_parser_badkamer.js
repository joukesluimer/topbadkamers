/* Offerteparser voor badkamerrenovatie (Top Badkamers).
   Gemaakt op basis van offerte_parser.js; dat bestand blijft ongewijzigd.
   Leest de geplakte tekst van een badkamerofferte uit: posten (sloopwerk, tegelwerk,
   leidingwerk, elektra, sanitair, stelposten, afvoer van afval, uren), totalen, btw
   en afspraken. Met productdata (opties.producten) herkent hij ook merk, serie,
   artikelnummer en EAN per regel en legt de prijs naast een marktprijsband. Draait in de browser (window.TBOfferte) en in Node (voor tests).
   Alles gebeurt lokaal; er wordt niets verstuurd. */
(function (root, maak) {
  var api = maak();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.TBOfferte = api;
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  /* ------------------------------------------------------------ soorten werk */
  // band: sleutel in de richtprijzen die de pagina meegeeft. eenheid: waarin die geldt.
  var TYPES = {
    sloop:           { naam: "Sloopwerk",                    band: "sloop",           eenheid: "post" },
    afval:           { naam: "Afvoer van afval",              band: "afval",           eenheid: "post" },
    tegelwerk:       { naam: "Tegelwerk (zetten)",            band: "tegelwerk",       eenheid: "m2" },
    tegels:          { naam: "Tegels (materiaal)",            band: "tegels",          eenheid: "m2" },
    waterdicht:      { naam: "Waterdicht maken" },
    vloer:           { naam: "Vloer, afschot en stucwerk" },
    leidingwerk:     { naam: "Leidingwerk",                   band: "leidingwerk",     eenheid: "post" },
    elektra:         { naam: "Elektra",                       band: "elektra",         eenheid: "post" },
    vloerverwarming: { naam: "Vloerverwarming",               band: "vloerverwarming", eenheid: "post" },
    ventilatie:      { naam: "Ventilatie" },
    sanitair:        { naam: "Sanitair (levering)",           band: "sanitair",        eenheid: "post" },
    montage:         { naam: "Montage van sanitair" },
    kitwerk:         { naam: "Kitwerk",                       band: "kitwerk",         eenheid: "m" },
    uren:            { naam: "Uren (regie)",                  band: "uur",             eenheid: "uur" },
    overig:          { naam: "Overig" },
    korting:         { naam: "Korting" }
  };
  var EENHEDEN = { m2: "m²", m: "meter", st: "stuks", uur: "uur", post: "post", dag: "dag" };

  /* ------------------------------------------------------------ getallen */
  // Nederlandse notatie: 1.250,50 · 1250,50 · € 1.250 · € 1250 · 1.250,- · 12,5
  function getal(t) {
    t = String(t == null ? "" : t).replace(/\s|€|euro|eur/gi, "");
    var neg = /^-/.test(t) || /^-\/-/.test(t);
    t = t.replace(/^-\/-|^-/, "").replace(/,-{1,2}$/, "");
    if (!t) return null;
    if (/,\d+$/.test(t)) t = t.replace(/\./g, "").replace(",", ".");
    else if (/^\d{1,3}(\.\d{3})+$/.test(t)) t = t.replace(/\./g, "");
    else if (!/^\d+\.\d{1,2}$/.test(t)) t = t.replace(/\./g, "");
    if (!/^\d+(\.\d+)?$/.test(t)) return null;
    var n = parseFloat(t);
    return isNaN(n) ? null : (neg ? -n : n);
  }
  function rond(n) { return Math.round(n * 100) / 100; }
  function gelijk(a, b, marge) {
    if (a == null || b == null) return false;
    return Math.abs(a - b) <= Math.max(marge == null ? 1 : marge, Math.abs(b) * 0.003);
  }

  var NUM_EURO = "\\d{1,3}(?:\\.\\d{3})+(?:,(?:\\d{1,2}|-{1,2}))?|\\d+(?:,(?:\\d{1,2}|-{1,2})|\\.\\d{2}(?!\\d))?";
  var NUM_DEC = "\\d{1,3}(?:\\.\\d{3})+,(?:\\d{2}|-{1,2})|\\d+,(?:\\d{2}|-{1,2})";
  var RE_BEDRAG = new RegExp("(-\\/-\\s*|-(?=\\s*€))?\\s*(?:(?:€|\\beur\\b|\\beuro\\b)\\s*(-\\s*)?(" + NUM_EURO + ")|(" + NUM_DEC + ")(?:\\s*(?:€|\\beuro\\b|\\beur\\b))?)", "gi");
  var RE_NA_EENHEID = /^\s*(m²|m2|m1|m\b|st\b|st\.|stuks?\b|uur\b|uren\b|meter|mtr|%|x\b|keer\b|punt|liter|ltr|l\b|mm\b|cm\b|dagen\b|dag\b)/i;
  var RE_PER_EENHEID = /^\s*(?:excl\.?\s*(?:btw)?\s*)?(?:per|\/|p\/|p\.)\s*(m²|m2|m1|m\b|meter|mtr|str|st\b|st\.|stuk|uur|u\b|punt|dag)/i;

  function zoekBedragen(regel) {
    var uit = [], m;
    RE_BEDRAG.lastIndex = 0;
    while ((m = RE_BEDRAG.exec(regel))) {
      var start = m.index + (m[0].length - m[0].replace(/^\s+/, "").length);
      var voor = regel.charAt(start - 1);
      var na = regel.slice(m.index + m[0].length);
      var euro = m[3] != null;
      if (/[\d.,a-z]/i.test(voor) && !euro) continue;
      if (/^\s*%/.test(na) || /^\d/.test(na)) continue;
      if (!euro && RE_NA_EENHEID.test(na)) continue;
      var w = getal(euro ? m[3] : m[4]);
      if (w == null) continue;
      if (m[1] || m[2]) w = -Math.abs(w);
      uit.push({
        waarde: w, start: start, eind: m.index + m[0].length, euro: euro,
        perEenheid: RE_PER_EENHEID.test(na) ? eenheidVan(RE_PER_EENHEID.exec(na)[1]) : null,
        a: /(?:^|\s)(?:à|á|a|@|x|per)\s*$/i.test(regel.slice(Math.max(0, start - 6), start))
      });
    }
    return uit;
  }

  /* ------------------------------------------------------------ aantallen */
  var RE_AANTAL = /(\d+(?:[.,]\d+)?)\s*(m²|m2|m\^2|vierkante\s+meters?|m1|str(?:\.|ekkende)?\s*m(?:eter|tr|1)?\.?|meters?|mtr\.?|m|stuks|stuk|st\.?|uren|uur|posten|post|punten|punt|dagen|dag)(?![a-zà-ÿ0-9²])/gi;
  var RE_AANTAL_X = /(\d+)\s*x\s+(?=toilet|wastafel|kraan|kranen|spot|stopcontact|douche|fontein|radiator|spiegel|punt|lamp)/gi;
  function eenheidVan(e) {
    e = String(e || "").toLowerCase();
    if (/^(m²|m2|m\^2|vierkant)/.test(e)) return "m2";
    if (/^(m1|str|meter|mtr|m)$|^(str|meter|mtr)/.test(e) || e === "m") return "m";
    if (/^(uur|uren|u)$/.test(e)) return "uur";
    if (/^post/.test(e)) return "post";
    if (/^dag/.test(e)) return "dag";
    return "st";
  }
  function zoekAantallen(regel, bedragen) {
    var uit = [], m;
    function inBedrag(i) { return bedragen.some(function (b) { return i >= b.start && i < b.eind; }); }
    RE_AANTAL.lastIndex = 0;
    while ((m = RE_AANTAL.exec(regel))) {
      if (inBedrag(m.index)) continue;
      var voor = regel.charAt(m.index - 1);
      if (/[\d.,\/a-z]/i.test(voor)) continue;
      uit.push({ aantal: getal(m[1]), eenheid: eenheidVan(m[2]), start: m.index, eind: m.index + m[0].length });
    }
    if (!uit.length) {
      RE_AANTAL_X.lastIndex = 0;
      while ((m = RE_AANTAL_X.exec(regel))) {
        if (!inBedrag(m.index)) uit.push({ aantal: getal(m[1]), eenheid: "st", start: m.index, eind: m.index + m[0].length });
      }
    }
    return uit;
  }

  /* ------------------------------------------------------------ soort herkennen */
  // Volgorde telt: de eerste regel die past wint. Een derde element sluit uit.
  var RE_SLOOP = /\bslo(op|pen)(werk(zaamheden)?)?\b|demonte(ren|ren van|ge)|uitbreken|verwijderen\s+(van\s+)?(de\s+)?(bestaande|oude)|strippen/;
  var REGELS_TYPE = [
    ["korting", /korting|reductie|vermindering|kortings/],
    ["afval", /container|\bpuin|afval|stortkosten|\bstorten\b|afvoeren\s+(van\s+)?(het\s+)?(sloop|puin|afval)/, RE_SLOOP],
    ["sloop", RE_SLOOP],
    ["waterdicht", /waterdicht|kimband|kimafdicht|afdichtingsfolie|tegelfolie|vochtwerend|vochtscherm|vloeibare\s+folie|afdichtingscoating/],
    ["vloerverwarming", /vloerverwarming|verwarmingsmat|verwarmingsfolie/],
    ["kitwerk", /\bkit(ten|werk|voeg|voegen)?\b|afkitten|siliconenkit/],
    ["tegelwerk", /tegelwerk|tegelzet|betegelen|tegels?\s+(zetten|leggen|plaatsen)|(zetten|leggen|plaatsen)\s+(van\s+)?(de\s+)?(wand|vloer)?tegels|legloon|wandtegelwerk|vloertegelwerk/],
    ["tegels", /\b(wand|vloer)?tegels?\b/],
    ["vloer", /egalis|stuc|uitvlakken|dekvloer|afschot|cementvloer|gipsplaat|voorzetwand|metal\s*stud/],
    ["elektra", /elektr|stopcontact|\bgroep|\bspots?\b|verlichting|bedrading|schakelaar|aarding|lichtpunt/],
    ["ventilatie", /ventilat|afzuig|mechanische\s+afzuiging|ventilator/],
    ["leidingwerk", /leiding|loodgiet|riolering|afvoer\s+(verleggen|aanpassen|aanleggen)|(water|afvoer)\s*aansluiting|aan-?\s*en\s+afvoer|installatiewerk|pex|\bkoper/],
    ["montage", /(montage|monteren|plaatsen|installeren|aansluiten)\b[^]*\b(sanitair|toilet|closet|wastafel|douche|kraan|kranen|bad|fontein|radiator|spiegel)|(sanitair|toilet|closet|wastafel|douche|kraan|kranen|ligbad|fontein|radiator|spiegel)\w*\b[^]*\b(montage|monteren|plaatsen|installeren|aansluiten)/, /levering|leveren|inclusief\s+sanitair|incl\.?\s+sanitair/],
    ["sanitair", /sanitair|toilet|\bwc\b|closet|wastafel|douche|kraan|kranen|thermostaat|\bbad\b|ligbad|fontein|radiator|spiegel|inbouwreservoir|reservoir/],
    ["uren", /\bregie|uurloon|uurtarief|\buren\b|manuren/]
  ];
  function bepaalType(tekst) {
    var t = tekst.toLowerCase();
    for (var i = 0; i < REGELS_TYPE.length; i++) {
      var r = REGELS_TYPE[i];
      if (!r[1].test(t)) continue;
      if (r[2] && r[2].test(t)) continue;
      return r[0];
    }
    return "overig";
  }

  /* ------------------------------------------------------------ regels voorbereiden */
  // Geplakte tabellen zetten soms meerdere rijen op één regel. Knip na een bedrag als er
  // daarna een nieuwe omschrijving (hoofdletter) én nog een bedrag volgt.
  function knipRegel(regel) {
    var b = zoekBedragen(regel);
    if (b.length < 2) return [regel];
    for (var i = 0; i < b.length - 1; i++) {
      var rest = regel.slice(b[i].eind);
      var m = /^\s*(?:\d{1,2}\s*%\s*)?(?=[A-ZÀ-Ý][a-zà-ÿ]{2,})/.exec(rest);
      if (!m) continue;
      var woord = /^\s*(?:\d{1,2}\s*%\s*)?([A-Za-zÀ-ÿ]+)/.exec(rest)[1].toLowerCase();
      if (/^(excl|incl|exclusief|inclusief|per|euro|eur)$/.test(woord)) continue;
      var heeftTekstVoor = /[a-zà-ÿ]{3,}/i.test(regel.slice(0, b[i].start));
      var restBedrag = zoekBedragen(rest).length > 0;
      if (heeftTekstVoor && restBedrag) {
        var knip = b[i].eind + m[0].length;
        return [regel.slice(0, knip)].concat(knipRegel(regel.slice(knip)));
      }
    }
    return [regel];
  }

  function letters(t) { return (t.match(/[a-zà-ÿ]/gi) || []).length; }
  function zonderBedragen(regel, bedragen) {
    var s = regel;
    for (var i = bedragen.length - 1; i >= 0; i--) s = s.slice(0, bedragen[i].start) + " " + s.slice(bedragen[i].eind);
    return s;
  }
  function schoon(t) {
    return t.replace(/^\s*\d{1,2}[.)]\s+/, "").replace(/\s*\|\s*/g, " – ").replace(/\s{2,}/g, " ").replace(/^[\s–\-:•*.]+|[\s–\-:•*=]+$/g, "").trim();
  }

  var RE_TOTAAL = /(sub\s*-?\s*totaal|totaal|eindbedrag|te\s+betalen|aanneemsom|offertebedrag|totale\s+prijs|prijs\s+totaal|totaalprijs|totaalbedrag)/i;
  var RE_BTW = /\bbtw\b|b\.t\.w|omzetbelasting/i;
  var RE_TERMIJN = /(termijn|aanbetaling|bij\s+(de\s+)?(start|aanvang|opdracht|akkoord|ondertekening|levering)|na\s+(de\s+)?(oplevering|afronding|voltooiing|gereedmelding)|bij\s+oplevering|halverwege|na\s+\d+\s*%|eindafrekening)/i;
  var RE_STELPOST = /stelpost|\bp\.?\s?m\.?\b|voorlopige?\s+(post|raming)|nacalculatie/i;
  var RE_OPTIE = /\boptie\b|optioneel|meerprijs|desgewenst|indien\s+gewenst|op\s+verzoek|alternatief|\bkeuze\b|niet\s+inbegrepen|meerwerk\s*:/i;
  var RE_UUR = /per\s+uur|\/\s*uur|uurloon|uurtarief|\bp\/u\b|regie(tarief)?|manuur/i;

  /* ------------------------------------------------------------ hoofdfunctie */
  function leesOfferte(tekst, opties) {
    var uit = leesOfferteBasis(tekst);
    voegProductenToe(uit, opties && opties.producten);
    return uit;
  }

  function leesOfferteBasis(tekst) {
    tekst = String(tekst || "").replace(/ /g, " ").replace(/\r/g, "");
    var ruw = tekst.split("\n");
    var regels = [];
    ruw.forEach(function (r) { knipRegel(r).forEach(function (k) { if (k.trim()) regels.push(k); }); });
    var laag = tekst.toLowerCase();

    var posten = [], totalen = [], btwRegels = [], termijnen = [], tarieven = [], losseBedragen = [];
    var sectie = null, variant = null, varianten = [], wachtTotaal = null, meldingen = [];

    regels.forEach(function (regel, i) {
      var r = regel.toLowerCase();
      var bedragen = zoekBedragen(regel);
      var kaal = zonderBedragen(regel, bedragen);
      var tekstLetters = letters(kaal.replace(/[€]|eur(o)?/gi, ""));

      // Regels zonder bedrag: kopjes en totaal-labels.
      if (!bedragen.length) {
        if (wachtTotaal && --wachtTotaal.ttl <= 0) wachtTotaal = null;
        var kop = r.trim();
        if (/^(betalingsschema|betaalschema|betalingsvoorwaarden|betalingstermijnen|termijnen|betaling)\b/.test(kop)) sectie = "betaling";
        else if (/^(opties|optioneel|meerprijzen|extra\s+opties|aanvullende\s+opties|optionele|niet\s+inbegrepen|meerwerk\b)/.test(kop)) sectie = "opties";
        else if (/^stelposten?\b/.test(kop)) sectie = "stelposten";
        else if (/^(variant|alternatief|offerte|prijsvariant)\s+([a-d1-4])\b/.test(kop) && kop.length < 70) {
          variant = kop.match(/^(variant|alternatief|offerte|prijsvariant)\s+([a-d1-4])/)[0];
          if (varianten.indexOf(variant) < 0) varianten.push(variant);
          sectie = null;
        } else if (/^(werkzaamheden|prijsopgave|specificatie|omschrijving)\b/.test(kop)) sectie = null;
        var tm = RE_TOTAAL.exec(regel);
        if (tm) {
          var soort = totaalSoort(regel.slice(tm.index));
          if (soort) {
            var los = losseBedragen.length && losseBedragen[losseBedragen.length - 1];
            if (los && i - los.regel <= 2 && !los.gebruikt) { los.gebruikt = true; voegTotaalToe(soort, los.waarde, i); }
            else wachtTotaal = { soort: soort, ttl: 6, regel: i };
          }
        }
        return;
      }

      // Alleen een bedrag op de regel: hoort bij een totaal-label erboven of eronder.
      if (tekstLetters < 3) {
        var w = bedragen[bedragen.length - 1].waarde;
        if (wachtTotaal) { voegTotaalToe(wachtTotaal.soort, w, i); wachtTotaal = null; }
        else losseBedragen.push({ waarde: w, regel: i });
        return;
      }
      wachtTotaal = null;
      var bedrag = bedragen[bedragen.length - 1].waarde;
      var procent = (/(\d{1,2}(?:[.,]\d+)?)\s*%/.exec(kaal) || [])[1];
      procent = procent != null ? getal(procent) : null;

      // Betalingstermijnen (een korting 'bij opdracht' is geen termijn)
      if (!/korting|reductie/.test(r) && (sectie === "betaling" || RE_TERMIJN.test(r)) && !RE_BTW.test(r.replace(/(incl|excl)\.?\s*btw/g, "")) && !RE_TOTAAL.test(r)) {
        termijnen.push({ omschrijving: schoon(kaal.replace(/\d{1,3}\s*%/, "")), procent: procent, bedrag: bedrag });
        return;
      }
      // Totalen
      var tm2 = RE_TOTAAL.exec(regel);
      if (tm2 && !(sectie === "opties" && /optie/i.test(r))) {
        var s2 = totaalSoort(regel.slice(tm2.index));
        if (s2) { voegTotaalToe(s2, bedrag, i); return; }
      }
      var aantallen = zoekAantallen(regel, bedragen);
      // Btw-regels
      if (RE_BTW.test(r) && !aantallen.length && !/korting/.test(r) && (procent != null || /^\s*(btw|b\.t\.w|omzetbelasting)/.test(r))) {
        var grond = bedragen.length > 1 ? Math.abs(bedragen[0].waarde) : null;
        var tarief = procent;
        if (tarief == null && grond) tarief = Math.round(bedrag / grond * 100);
        btwRegels.push({ tarief: tarief, grondslag: grond, bedrag: Math.abs(bedrag), regel: i });
        return;
      }

      var a = aantallen.length ? kiesAantal(aantallen, bedragen) : null;
      var oms = schoon(zonderAantallen(kaal, a ? [a] : []).replace(/\b\d{1,2}\s*%/g, "").replace(/\s(à|á|a|x|@|per\s+\S+)\s*$/i, ""));
      var type = bepaalType(oms + " " + kaal);
      if (a && a.eenheid === "uur" && type !== "korting") type = "uren";

      // Kortingen
      if (type === "korting" || /korting|reductie|-\/-|actieprijs/.test(r)) {
        posten.push(maakPost({ omschrijving: oms, type: "korting", bedrag: -Math.abs(bedrag), regel: i, btw: btwVan(kaal) }));
        return;
      }

      // Alleen een tarief, zonder aantal: uurloon of prijs per eenheid.
      var eenheidsprijs = null, berekend = false;
      var b0 = bedragen[0], bl = bedragen[bedragen.length - 1];
      if (bedragen.length === 1 && (b0.perEenheid || (b0.a && a))) {
        if (!a) {
          if (b0.perEenheid === "uur" || RE_UUR.test(r)) tarieven.push({ soort: "uurloon", bedrag: Math.abs(bedrag), omschrijving: oms });
          else tarieven.push({ soort: type, eenheid: b0.perEenheid, bedrag: Math.abs(bedrag), omschrijving: oms });
          if (type !== "overig" && type !== "uren" && b0.perEenheid !== "uur") {
            posten.push(maakPost({ omschrijving: oms, type: type, eenheid: b0.perEenheid, eenheidsprijs: Math.abs(bedrag), bedrag: null, regel: i, meetellen: false, alleenTarief: true }));
          }
          return;
        }
        eenheidsprijs = Math.abs(bedrag);
        bedrag = rond(a.aantal * eenheidsprijs);
        berekend = true;
      } else if (bedragen.length === 1 && RE_UUR.test(r) && !a) {
        tarieven.push({ soort: "uurloon", bedrag: Math.abs(bedrag), omschrijving: oms });
        return;
      } else if (bedragen.length >= 2) {
        var eerste = Math.abs(b0.waarde);
        if (a && gelijk(a.aantal * eerste, Math.abs(bl.waarde), 1.5)) eenheidsprijs = eerste;
        else if (b0.perEenheid || b0.a) eenheidsprijs = eerste;
      }

      var stel = RE_STELPOST.test(r) || sectie === "stelposten";
      var optie = sectie === "opties" || RE_OPTIE.test(r) || (variant && varianten.indexOf(variant) > 0);
      var naTotaal = totalen.some(function (t) { return t.soort !== "sub" && t.soort !== "groep"; }) && !variant;
      var p = maakPost({
        omschrijving: oms, type: type, aantal: a ? a.aantal : null, eenheid: a ? a.eenheid : null,
        eenheidsprijs: eenheidsprijs, bedrag: rond(bedrag), berekend: berekend, btw: btwVan(kaal),
        stelpost: stel, optie: !!optie, naTotaal: naTotaal && !optie, variant: variant, regel: i
      });
      if (p.type === "uren" && p.eenheid === "uur" && p.aantal && !p.eenheidsprijs) p.eenheidsprijs = rond(p.bedrag / p.aantal);
      posten.push(p);
    });

    function voegTotaalToe(soort, waarde, regel) {
      totalen.push({ soort: soort, waarde: Math.abs(waarde), regel: regel, variant: variant });
    }

    return verzoen({
      tekst: laag, regels: regels, posten: posten, totalen: totalen, btwRegels: btwRegels,
      termijnen: termijnen, tarieven: tarieven, varianten: varianten, meldingen: meldingen
    });
  }

  function zonderAantallen(s, aantallen) {
    // aantallen zijn gemeten op de oorspronkelijke regel; zonderBedragen behoudt de posities niet
    // exact, dus we verwijderen ze op tekst.
    aantallen.forEach(function (a) {
      s = s.replace(new RegExp("(^|[^\\d.,])" + String(a.aantal).replace(".", "[.,]") + "\\s*(m²|m2|m\\^2|vierkante\\s+meters?|m1|str\\S*\\s*m\\S*|meters?|mtr\\.?|m|stuks|stuk|st\\.?|uren|uur|rollen|rol|posten|post|dagen|dag)(?![a-zà-ÿ0-9²])", "i"), "$1 ");
    });
    return s;
  }
  function kiesAantal(aantallen, bedragen) {
    // Neem het aantal dat het dichtst vóór het eerste bedrag staat (de kolom 'aantal').
    var eerste = bedragen.length ? bedragen[0].start : Infinity;
    var voor = aantallen.filter(function (a) { return a.start < eerste; });
    return voor.length ? voor[voor.length - 1] : aantallen[0];
  }
  function btwVan(t) {
    var m = /(?:^|[^\d,.])(9|21|0)\s*%/.exec(t);
    return m ? parseInt(m[1], 10) : null;
  }
  function totaalSoort(t) {
    var l = t.toLowerCase();
    if (/^sub/.test(l)) return "sub";
    var incl = /incl|inclusief|inc\.\s*btw|met\s+btw/.test(l), excl = /excl|exclusief|ex\.?\s+btw|zonder\s+btw|exc\.\s*btw/.test(l);
    var rest = l.replace(/\(.*?\)/g, " ").replace(/totaal(prijs|bedrag)?|eindbedrag|te\s+betalen|aanneemsom|offertebedrag|totale\s+prijs|prijs|incl\w*|excl\w*|inc\.|ex\.|btw|b\.t\.w\.?|bedrag|generaal|offerte|alles|in|met|zonder|de|het|van|deze|voor|over|euro|eur|€|[\d.,%:=\-–]+/g, " ");
    if (letters(rest) >= 4) return incl ? "incl" : excl ? "excl" : "groep";
    return incl ? "incl" : excl ? "excl" : "onbekend";
  }
  function maakPost(p) {
    return {
      omschrijving: p.omschrijving || "", type: p.type || "overig",
      aantal: p.aantal != null ? p.aantal : null, eenheid: p.eenheid || null,
      eenheidsprijs: p.eenheidsprijs != null ? p.eenheidsprijs : null,
      bedrag: p.bedrag != null ? p.bedrag : null, berekend: !!p.berekend,
      btw: p.btw != null ? p.btw : null, stelpost: !!p.stelpost, optie: !!p.optie,
      naTotaal: !!p.naTotaal, alleenTarief: !!p.alleenTarief, variant: p.variant || null,
      meetellen: p.meetellen === false ? false : !(p.optie || p.naTotaal), regel: p.regel
    };
  }

  /* ------------------------------------------------------------ totalen kloppend maken */
  function verzoen(d) {
    var t = d.tekst, uit = {
      posten: d.posten, termijnen: d.termijnen, btwRegels: d.btwRegels.map(function (b) { return { tarief: b.tarief, grondslag: b.grondslag, bedrag: b.bedrag }; }),
      totaal: { excl: null, incl: null, btw: null, bron: {} }, subtotaal: null, varianten: [],
      basis: null, btwTarieven: [], meldingen: d.meldingen
    };
    var btwSom = d.btwRegels.length ? rond(d.btwRegels.reduce(function (s, b) { return s + b.bedrag; }, 0)) : null;
    var eersteBtw = d.btwRegels.length ? d.btwRegels[0].regel : null;
    var tarieven = [];
    d.btwRegels.forEach(function (b) { if (b.tarief != null && tarieven.indexOf(b.tarief) < 0) tarieven.push(b.tarief); });
    if (!tarieven.length) {
      var m = /(\d{1,2})\s*%\s*(btw|b\.t\.w|omzetbelasting)|(?:btw|b\.t\.w\.?)\s*(?:tarief|:)?\s*(?:van\s*)?(\d{1,2})\s*%/.exec(t);
      if (m) tarieven.push(parseInt(m[1] || m[3], 10));
      d.posten.forEach(function (p) { if (p.btw != null && p.btw > 0 && tarieven.indexOf(p.btw) < 0) tarieven.push(p.btw); });
    }

    // Varianten: per variant het eerste totaal; de eerste variant telt.
    var totalen = d.totalen;
    if (d.varianten.length > 1) {
      d.varianten.forEach(function (v) {
        var tv = totalen.filter(function (x) { return x.variant === v && x.soort !== "sub" && x.soort !== "groep"; });
        if (tv.length) uit.varianten.push({ naam: v.charAt(0).toUpperCase() + v.slice(1), totaal: tv[tv.length - 1].waarde, soort: tv[tv.length - 1].soort });
      });
      if (uit.varianten.length > 1) {
        totalen = totalen.filter(function (x) { return !x.variant || x.variant === d.varianten[0]; });
        uit.meldingen.push("De offerte heeft meerdere varianten. We rekenen met " + uit.varianten[0].naam.toLowerCase() + "; de andere posten tellen niet mee.");
      }
    }
    function laatste(soort) {
      var l = totalen.filter(function (x) { return x.soort === soort; });
      return l.length ? l[l.length - 1] : null;
    }
    var sub = laatste("sub"), ex = laatste("excl"), inc = laatste("incl");
    var onbekend = totalen.filter(function (x) { return x.soort === "onbekend"; });
    if (sub) uit.subtotaal = sub.waarde;
    var kortingNaSub = rond(d.posten.filter(function (p) { return p.type === "korting" && p.meetellen && sub && p.regel > sub.regel; })
      .reduce(function (s, p) { return s + p.bedrag; }, 0));

    var excl = ex ? ex.waarde : null, incl = inc ? inc.waarde : null;
    if (ex) uit.totaal.bron.excl = "offerte";
    if (inc) uit.totaal.bron.incl = "offerte";
    var basisHint = /(bedragen|prijzen|tarieven)\b[^\n.]{0,40}?(excl|exclusief)/.test(t) ? "excl"
      : /(bedragen|prijzen|tarieven)\b[^\n.]{0,40}?(incl|inclusief)/.test(t) ? "incl" : null;
    var RE_IN = /incl(\.|usief)?\s*(\d{1,2}\s*%\s*)?(btw|b\.t\.w)/, RE_EX = /excl(\.|usief)?\s*(\d{1,2}\s*%\s*)?(btw|b\.t\.w)/;

    // Totaal zonder incl/excl: bepaal wat het is.
    onbekend.forEach(function (o) {
      var soort = null;
      if (excl != null && btwSom != null && gelijk(o.waarde, excl + btwSom)) soort = "incl";
      else if (eersteBtw != null) soort = o.regel > eersteBtw ? "incl" : "excl";
      else if (excl != null && (gelijk(o.waarde, excl * 1.09) || gelijk(o.waarde, excl * 1.21))) soort = "incl";
      else if (incl != null && (gelijk(o.waarde * 1.09, incl) || gelijk(o.waarde * 1.21, incl))) soort = "excl";
      else if (basisHint) soort = basisHint;
      else if (RE_IN.test(t) && !RE_EX.test(t)) soort = "incl";
      else if (RE_EX.test(t) && !RE_IN.test(t)) soort = "excl";
      if (soort === "incl" && incl == null) { incl = o.waarde; uit.totaal.bron.incl = "offerte"; }
      else if (soort === "excl" && excl == null) { excl = o.waarde; uit.totaal.bron.excl = "offerte"; }
      else if (!soort && incl == null && excl == null) { o.twijfel = true; uit.totaal.twijfel = o.waarde; }
    });
    if (sub && basisHint === "incl") {
      if (incl == null) { incl = rond(sub.waarde + kortingNaSub); uit.totaal.bron.incl = kortingNaSub ? "berekend" : "offerte"; }
    } else if (excl == null && sub) { excl = rond(sub.waarde + kortingNaSub); uit.totaal.bron.excl = kortingNaSub ? "berekend" : "offerte"; }
    if (excl == null && incl != null && btwSom != null) { excl = rond(incl - btwSom); uit.totaal.bron.excl = "berekend"; }
    if (incl == null && excl != null && btwSom != null) { incl = rond(excl + btwSom); uit.totaal.bron.incl = "berekend"; }
    if (excl != null && incl != null && !tarieven.length) {
      var f = incl / excl;
      if (Math.abs(f - 1.09) < 0.003) tarieven.push(9); else if (Math.abs(f - 1.21) < 0.003) tarieven.push(21);
    }
    if (tarieven.length === 1) {
      var fac = 1 + tarieven[0] / 100;
      if (incl == null && excl != null) { incl = rond(excl * fac); uit.totaal.bron.incl = "berekend"; }
      if (excl == null && incl != null) { excl = rond(incl / fac); uit.totaal.bron.excl = "berekend"; }
    }
    // Termijnen bevestigen het totaal incl. btw.
    var termSom = rond(d.termijnen.reduce(function (s, x) { return s + x.bedrag; }, 0));
    if (incl == null && d.termijnen.length > 1 && termSom > 0 && /incl/.test(t)) { incl = termSom; uit.totaal.bron.incl = "betalingsschema"; }

    // Posten optellen en kijken op welke basis ze staan.
    var tellen = d.posten.filter(function (p) { return p.meetellen && p.bedrag != null; });
    var som = rond(tellen.reduce(function (s, p) { return s + p.bedrag; }, 0));
    var basis = basisHint;
    if (!basis) {
      if (gelijk(som, excl) || (sub && gelijk(som, sub.waarde + kortingNaSub))) basis = "excl";
      else if (gelijk(som, incl)) basis = "incl";
      else if (d.btwRegels.length || (excl != null && incl == null)) basis = "excl";
      else if (incl != null && excl == null) basis = "incl";
      else basis = "excl";
    }
    // Geen totaal op de offerte: gebruik de som van de posten.
    if (excl == null && incl == null && som > 0) {
      if (basis === "incl") { incl = som; uit.totaal.bron.incl = "posten"; } else { excl = som; uit.totaal.bron.excl = "posten"; }
      if (tarieven.length === 1) {
        var fc = 1 + tarieven[0] / 100;
        if (incl == null) { incl = rond(excl * fc); uit.totaal.bron.incl = "berekend"; }
        else { excl = rond(incl / fc); uit.totaal.bron.excl = "berekend"; }
      }
    }
    uit.totaal.excl = excl; uit.totaal.incl = incl;
    uit.totaal.btw = btwSom != null ? btwSom : (excl != null && incl != null ? rond(incl - excl) : null);
    uit.btwTarieven = tarieven.sort(function (a, b) { return a - b; });
    uit.basis = basis;
    uit.somPosten = som;
    uit.controle = controle(som, basis, uit.totaal, uit.subtotaal, kortingNaSub);
    if (d.termijnen.length > 1 && incl != null && !gelijk(termSom, incl, 2)) uit.meldingen.push("De betaaltermijnen tellen op tot " + euro(termSom) + ", het totaal is " + euro(incl) + ".");

    // Overige gegevens uit de hele tekst.
    var uurloon = d.tarieven.filter(function (x) { return x.soort === "uurloon"; })[0];
    var uurpost = d.posten.filter(function (p) { return p.type === "uren" && p.eenheidsprijs; })[0];
    uit.uurloon = uurloon ? uurloon.bedrag : uurpost ? uurpost.eenheidsprijs : null;
    uit.garantie = zoekGarantie(t);
    uit.geldigheid = zoekGeldigheid(t);
    uit.betaaltermijn = (/betaal(?:termijn|tijd)[^\n]{0,30}?(\d+)\s*dagen/.exec(t) || /binnen\s*(\d+)\s*dagen\s*na\s*factuur/.exec(t) || [])[1] || null;
    if (uit.betaaltermijn) uit.betaaltermijn += " dagen";
    var dl = /(doorlooptijd|duur\s+van\s+het\s+werk|uitvoeringsduur)[^\n]{0,30}?(\d+(?:\s*(?:tot|à|a|-|–)\s*\d+)?)\s*(werkdagen|dagen|weken)/.exec(t);
    uit.doorlooptijd = dl ? dl[2].replace(/\s*[-–à]\s*/, " tot ") + " " + dl[3] : null;
    uit.concept = /\bconcept\b|indicatie(f|ve)|geschatte\s+hoeveelheden|onder\s+voorbehoud/.test(t);
    uit.stelposten = d.posten.filter(function (p) { return p.stelpost; });
    uit.lijst = {
      waterdicht: /waterdicht|kimband|kimafdicht|afdichting|tegelfolie|vochtwerend|vochtscherm|vloeibare\s+folie/.test(t),
      kitwerk: /\bkit(ten|werk|voeg|voegen)?\b|afkitten|siliconen/.test(t),
      afval: /afval|container|\bpuin|stortkosten|afvoeren\s+van|slopen\s+en\s+afvoeren|incl\.?\s*afvoer\b|inclusief\s+afvoer\b/.test(t),
      planning: /planning|startdatum|start\s+(werk|werkzaamheden)|doorlooptijd|uitvoeringsduur|werkdagen|oplever|\bweek\s*\d/.test(t),
      garantie: !!uit.garantie && uit.garantie !== "geen",
      betaling: d.termijnen.length > 0 || !!uit.betaaltermijn || /betaling|betalen|termijn|factuur/.test(t),
      btw: tarieven.length > 0,
      geldigheid: !!uit.geldigheid
    };
    return uit;
  }

  function controle(som, basis, totaal, sub, kortingNaSub) {
    var tegen = basis === "incl" ? totaal.incl : totaal.excl;
    if (tegen == null || !som) return { klopt: null, som: som, tegen: tegen, basis: basis };
    var klopt = gelijk(som, tegen, 1.5) || (sub != null && gelijk(som, sub + kortingNaSub, 1.5));
    return { klopt: klopt, som: som, tegen: tegen, verschil: rond(tegen - som), basis: basis };
  }

  function zoekGarantie(t) {
    if (/geen\s+garantie/.test(t)) return "geen";
    var m = /(\d+)\s*(jaar|jaren|maanden|mnd)\.?\s*(?:volledige\s+|schriftelijke\s+)?garantie/.exec(t) ||
      /garantie(?:termijn)?[^\n.]{0,45}?(\d+)\s*(jaar|jaren|maanden|mnd)/.exec(t);
    if (!m) return /garantie/.test(t) ? "genoemd, zonder termijn" : null;
    return m[1] + " " + (m[2] === "mnd" ? "maanden" : m[2] === "jaren" ? "jaar" : m[2]);
  }
  function zoekGeldigheid(t) {
    var m = /geldig(?:heid)?[^\n]{0,20}?(t\/m|tot\s+en\s+met|tot|:)?\s*(\d{1,2}[-\/ .]\s?(?:\d{1,2}|[a-z]{3,9}\.?)[-\/ .]\s?\d{2,4})/.exec(t);
    if (m) return (m[1] && m[1] !== ":" ? m[1] + " " : "t/m ") + m[2];
    m = /geldig(?:heid)?[^\n]{0,25}?(\d+)\s*(dagen|weken|maanden)/.exec(t);
    return m ? m[1] + " " + m[2] : null;
  }
  function euro(n) {
    if (n == null || isNaN(n)) return "–";
    var r = Math.round(n * 100) / 100, heel = Math.abs(r) % 1 === 0;
    return (r < 0 ? "−" : "") + "€\u00a0" + Math.abs(r).toLocaleString("nl-NL", { minimumFractionDigits: heel ? 0 : 2, maximumFractionDigits: 2 });
  }

  /* ------------------------------------------------------------ beoordelen */
  var VRAGEN_TYPE = {
    sloop: "Valt het afvoeren van het sloopafval onder deze post, of staat dat apart?",
    afval: "Gaat het om een container of om afvoer met de bus, en zit het storten erbij?",
    tegelwerk: "Hoeveel m² wand en vloer is het, en zitten voegen, hoekprofielen en snijwerk in de prijs per m²?",
    tegels: "Welke tegel is gerekend, en mag je ook zelf tegels kiezen voor dit bedrag?",
    waterdicht: "Met welk systeem wordt de douchehoek waterdicht gemaakt, en hoe hoog op de wand?",
    vloer: "Wat valt er precies onder deze post: egaliseren, afschot maken of stucwerk?",
    leidingwerk: "Blijven de aansluitingen op dezelfde plek, of worden ze verlegd?",
    elektra: "Hoeveel stopcontacten, spots en schakelaars zitten erin, en wordt er een aparte groep aangelegd?",
    vloerverwarming: "Is het elektrische vloerverwarming of aangesloten op de cv, en zit de thermostaat erbij?",
    ventilatie: "Komt er een mechanische afzuiging, en op welk kanaal wordt die aangesloten?",
    sanitair: "Welke onderdelen zitten erin, en mag je zelf sanitair kiezen als het duurder wordt?",
    montage: "Welke onderdelen worden gemonteerd, en geldt de garantie ook voor sanitair dat je zelf koopt?",
    kitwerk: "Wordt de oude kit eerst helemaal verwijderd, en welke schimmelwerende kit wordt gebruikt?",
    uren: "Hoeveel uur is ingeschat, en wat gebeurt er als het meer wordt?"
  };

  // Geeft de prijs per eenheid of per post zoals die met de richtprijs vergeleken wordt.
  // banden: { sleutel: { van, tot, eenheid, excl_btw } }. Richtprijzen zijn incl. 21% btw,
  // behalve als excl_btw waar is. basis: staan de bedragen op de offerte incl. of excl. btw.
  function beoordeelPost(p, banden, basis, standaardBtw) {
    var type = TYPES[p.type] || TYPES.overig;
    var band = type.band && banden ? banden[type.band] : null;
    var uit = { oordeel: null, reden: null, van: null, tot: null, vergelijk: null, perEenheid: null, vragen: [] };
    if (VRAGEN_TYPE[p.type]) uit.vragen.push(VRAGEN_TYPE[p.type]);
    if (p.stelpost) uit.vragen.push("Dit is een stelpost. Wat gebeurt er als het meer of minder wordt, en krijg je het verschil terug?");
    if (p.btw === 9 && p.type !== "vloer") uit.vragen.push("Waarom staat hier 9% btw op? Voor badkamerwerk geldt meestal 21%.");
    if (p.type === "tegelwerk" && /tegels/.test(p.omschrijving.toLowerCase()) && /lever|incl/.test(p.omschrijving.toLowerCase())) band = banden && banden.tegelwerk_incl;
    // Een herkend product (bijv. een wastafelmeubel zonder merk) hoort nooit naast de band voor
    // complete sanitair; dat oordeel komt van beoordeelProduct.
    if (band && type.band === "sanitair" && p.soort === "product") { uit.reden = "product"; return uit; }
    if (!band) { uit.reden = p.type === "korting" ? "korting" : "geen richtprijs"; return uit; }
    var tarief = (p.btw != null ? p.btw : (standaardBtw || 21)) / 100;
    function naarVergelijk(bedrag) {
      if (band.excl_btw) return basis === "incl" ? bedrag / (1 + tarief) : bedrag;
      return basis === "incl" ? bedrag : bedrag * (1 + tarief);
    }
    var prijs = null;
    if (band.eenheid === "post") {
      if (p.alleenTarief || p.bedrag == null) { uit.reden = "geen bedrag"; return uit; }
      if (p.eenheid && p.eenheid !== "post" && p.eenheid !== "st" && p.aantal && p.aantal > 1) { uit.reden = "andere eenheid"; return uit; }
      prijs = p.bedrag;
    } else {
      if (p.eenheidsprijs != null && (p.eenheid === band.eenheid || (p.alleenTarief && !p.eenheid))) prijs = p.eenheidsprijs;
      else if (p.aantal && p.eenheid === band.eenheid && p.bedrag != null) prijs = p.bedrag / p.aantal;
      if (prijs == null) { uit.reden = p.aantal ? "andere eenheid" : "geen aantal"; return uit; }
      uit.perEenheid = band.eenheid;
    }
    var vgl = naarVergelijk(Math.abs(prijs));
    uit.van = band.van; uit.tot = band.tot; uit.vergelijk = rond(vgl); uit.inclBtw = !band.excl_btw;
    uit.oordeel = vgl < band.van * 0.9 ? "laag" : vgl > band.tot * 1.1 ? "hoog" : "binnen";
    if (uit.oordeel === "hoog") uit.vragen.unshift("Deze post ligt boven de richtprijs. Vraag wat er precies in zit; soms is het extra werk dat je wilt, soms niet.");
    if (uit.oordeel === "laag") uit.vragen.unshift(p.stelpost
      ? "Deze stelpost ligt onder de richtprijs. Een te laag bedrag maakt de offerte goedkoper dan hij is: reken op bijbetalen."
      : "Deze post ligt onder de richtprijs. Vraag of alles erin zit, zodat je achteraf niet bijbetaalt.");
    return uit;
  }

  // Wat vaak ontbreekt in een badkamerofferte. Geeft [{sleutel, titel, gevonden, uitleg}].
  function checklist(res, banden) {
    var l = res.lijst, uit = [];
    function item(sleutel, titel, gevonden, uitleg, status) {
      uit.push({ sleutel: sleutel, titel: titel, gevonden: gevonden, status: status || (gevonden ? "ok" : "mist"), uitleg: uitleg });
    }
    item("waterdicht", "Waterdicht maken", l.waterdicht, l.waterdicht ? "De offerte noemt het waterdicht maken." : "We zien niets over waterdicht maken (kimband, folie of coating). Vraag hoe de douchehoek en de vloer waterdicht worden.");
    item("kitwerk", "Kitwerk", l.kitwerk, l.kitwerk ? "Kitwerk staat erin." : "Kitwerk langs bad, douche en wastafel staat er niet in. Vraag of het in de prijs zit.");
    item("afval", "Afvoer van afval", l.afval, l.afval ? "Het afvoeren van afval of puin wordt genoemd." : "Er staat niet bij wie het sloopafval afvoert. Een container kost al snel een paar honderd euro.");
    var stel = res.stelposten || [], laag = stel.filter(function (p) { return beoordeelPost(p, banden, res.basis, (res.btwTarieven || [])[0]).oordeel === "laag"; });
    if (!stel.length) item("stelposten", "Stelposten met een eerlijk bedrag", true, "Er staan geen stelposten in. Kijk wel of sanitair en tegels erin zitten.", "neutraal");
    else item("stelposten", "Stelposten met een eerlijk bedrag", !laag.length,
      laag.length ? "Een of meer stelposten liggen onder de richtprijs. Dan valt de rekening later hoger uit." : "Er staan " + stel.length + " stelpost(en) in. Vraag wat er gebeurt bij meer of minder.",
      laag.length ? "mist" : "let");
    item("planning", "Planning", l.planning, l.planning ? "Er staat iets over de planning of doorlooptijd." : "We zien geen startdatum of doorlooptijd. Vraag om een planning per dag of week.");
    item("garantie", "Garantie", l.garantie, l.garantie ? "Garantie: " + res.garantie + "." : res.garantie === "geen" ? "De offerte zegt dat er geen garantie is. Vraag waarom." : "We zien geen garantie. Vraag hoe lang die geldt, en op werk én materiaal.");
    item("betaling", "Betaaltermijnen", l.betaling, l.betaling ? "Er staan afspraken over de betaling in." : "Er staat niet in wanneer je betaalt. Spreek termijnen af, met het grootste deel na oplevering.");
    return uit;
  }

  // Vragen over de offerte als geheel.
  function algemeneVragen(res) {
    var l = res.lijst, v = [];
    if (!l.btw) v.push("Zijn de bedragen inclusief of exclusief btw? Voor badkamerwerk geldt 21%.");
    if ((res.btwTarieven || []).indexOf(9) >= 0) v.push("Er staat 9% btw in de offerte. Voor badkamerwerk geldt 21%; 9% mag alleen voor stucwerk, verfwerk en isolatie aan een woning ouder dan twee jaar. Vraag welke posten 9% hebben.");
    if (!l.geldigheid) v.push("Hoe lang is deze offerte geldig?");
    var vooraf = (res.termijnen || []).filter(function (x) { return /start|aanvang|opdracht|akkoord|aanbetaling|ondertekening/i.test(x.omschrijving); })
      .reduce(function (s, x) { return s + (x.procent || 0); }, 0);
    if (vooraf >= 50) v.push("Je betaalt " + vooraf + "% voordat het werk klaar is. Vraag of een kleiner deel vooraf kan.");
    if (res.concept) v.push("De offerte noemt geschatte hoeveelheden of is onder voorbehoud. Vraag na de opname om een vaste prijs.");
    if (res.controle && res.controle.klopt === false) v.push("De losse posten tellen niet op tot het totaal. Vraag waar het verschil zit.");
    if (res.posten && !res.posten.some(function (p) { return p.type === "sanitair" || p.type === "montage"; })) v.push("We zien geen sanitair in de offerte. Lever je dat zelf, of zit het in een andere post?");
    return v;
  }

  /* ------------------------------------------------------------ producten herkennen */
  // Werkt met de productdata (PD) uit producten_badkamer.py: { peildatum, merken, categorieen,
  // artikelen, bronnen }. Herkenning in deze volgorde: 1) EAN of artikelnummer van de fabrikant,
  // 2) merk + serie, 3) categorie op trefwoorden. Prijsbanden zijn inclusief 21% btw, voor het
  // product zelf, zonder montage.
  var MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"];
  var VAAG_TEKST = "onvoldoende gespecificeerd: vraag merk en type per onderdeel";
  // Merknamen voor soortRegel zonder productdata (de PD-lijst is uitgebreider).
  var MERKEN_BASIS = ["grohe", "hansgrohe", "axor", "geberit", "villeroy", "duravit", "ideal standard", "sphinx", "laufen",
    "toto", "roca", "jacob delafon", "keuco", "dornbracht", "hansa", "hotbath", "clou", "wiesbaden", "plieger", "sealskin",
    "novellini", "huppe", "kermi", "radaway", "riho", "kaldewei", "bette", "xenz", "vasco", "zehnder", "easy drain", "viega",
    "tece", "wisa", "pressalit", "mosa", "damixa", "gessi", "lineabeta"];

  function plat(t) {
    t = String(t == null ? "" : t).toLowerCase();
    if (t.normalize) t = t.normalize("NFD").replace(/[̀-ͯ]/g, "");
    return t;
  }
  function normCode(c) { return String(c == null ? "" : c).replace(/[\s.\-\/]/g, "").toUpperCase(); }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function bevatWoord(t, w, eindGrens) {
    var re = new RegExp("(^|[^a-z0-9])" + esc(w) + (eindGrens === false ? "" : "(?=$|[^a-z0-9])"));
    var m = re.exec(t);
    return m ? m.index + m[1].length : -1;
  }
  function eanGeldig(e) {
    if (!/^\d{13}$/.test(e)) return false;
    var s = 0;
    for (var i = 0; i < 12; i++) s += (+e[i]) * (i % 2 ? 3 : 1);
    return (10 - s % 10) % 10 === +e[12];
  }
  function peildatumTekst(PD) {
    var m = /^(\d{4})-(\d{2})/.exec((PD && PD.peildatum) || "");
    return m ? MAANDEN[+m[2] - 1] + " " + m[1] : null;
  }

  var CACHE = typeof WeakMap !== "undefined" ? new WeakMap() : null;
  function index(PD) {
    if (CACHE && CACHE.has(PD)) return CACHE.get(PD);
    var idx = { codes: {}, ean: {}, merken: [], cats: [] };
    (PD.artikelen || []).forEach(function (a) {
      (a.codes || []).forEach(function (c) { var n = normCode(c); if (n.length >= 4 && !idx.codes[n]) idx.codes[n] = a; });
      (a.ean || []).forEach(function (e) { e = String(e).replace(/\D/g, ""); if (e.length === 13) idx.ean[e] = a; });
    });
    (PD.merken || []).forEach(function (m) {
      var al = (m.aliassen || []).concat([m.naam]).map(plat).filter(function (x, i, l) { return x && l.indexOf(x) === i; });
      al.sort(function (a, b) { return b.length - a.length; });
      var re = [];
      (m.code_regex || []).forEach(function (r) { try { re.push(new RegExp(r)); } catch (e) { /* ongeldige regex overslaan */ } });
      idx.merken.push({ naam: m.naam, aliassen: al, re: re });
    });
    var cats = PD.categorieen || {};
    Object.keys(cats).forEach(function (k) {
      idx.cats.push({ sleutel: k, trefwoorden: (cats[k].trefwoorden || []).map(plat) });
    });
    if (CACHE) CACHE.set(PD, idx);
    return idx;
  }

  // Woorden die samen een artikelnummer kunnen vormen ("34 558 000", "115.882.KJ.1", "Art.nr.:26533000").
  function codeVensters(tekst) {
    var tokens = String(tekst || "").split(/[\s:;,()\[\]#"']+/).map(function (t) { return t.replace(/^[.\-]+|[.\-]+$/g, ""); })
      .filter(Boolean);
    var uit = [];
    for (var i = 0; i < tokens.length; i++) {
      for (var n = 1; n <= 4 && i + n <= tokens.length; n++) {
        var ruw = tokens.slice(i, i + n).join(" "), norm = normCode(ruw);
        if (norm.length < 4 || norm.length > 16 || !/\d/.test(norm) || !/^[A-Z0-9]+$/.test(norm)) continue;
        if (n > 1 && !/\d/.test(tokens[i + n - 1])) continue; // laatste stuk moet een cijfer bevatten
        uit.push({ ruw: ruw, norm: norm });
      }
    }
    return uit;
  }

  // De regex moet het hele venster beslaan: "800 34558000" is geen code, "34558000" wel.
  function heelMatch(re, s) { var m = re.exec(s); return !!m && m[0] === s; }

  function zoekMerk(t, idx) {
    var beste = null;
    idx.merken.forEach(function (m) {
      for (var i = 0; i < m.aliassen.length; i++) {
        var pos = bevatWoord(t, m.aliassen[i]);
        if (pos < 0) continue;
        var len = m.aliassen[i].length;
        if (!beste || len > beste.len || (len === beste.len && pos < beste.pos)) beste = { naam: m.naam, len: len, pos: pos };
        break;
      }
    });
    return beste ? beste.naam : null;
  }

  // Categorie op trefwoorden: het langste trefwoord wint, bij gelijke lengte het eerste in de tekst.
  function zoekCategorie(t, idx, alle) {
    var lijst = [];
    idx.cats.forEach(function (c) {
      var best = null;
      c.trefwoorden.forEach(function (w) {
        var pos = bevatWoord(t, w, w.length >= 5 ? false : true);
        if (pos >= 0 && (!best || w.length > best.len)) best = { sleutel: c.sleutel, len: w.length, pos: pos };
      });
      if (best) lijst.push(best);
    });
    if (alle) {
      // Een trefwoord dat binnen een langer trefwoord valt telt niet apart ("wastafel" in "wastafelmeubel").
      return lijst.filter(function (x) {
        return !lijst.some(function (y) { return y !== x && y.len > x.len && x.pos >= y.pos && x.pos + x.len <= y.pos + y.len; });
      });
    }
    lijst.sort(function (a, b) { return b.len - a.len || a.pos - b.pos; });
    var k = lijst.length ? lijst[0].sleutel : null;
    // Een inbouwkraan of inbouwthermostaat is geen opbouwkraan.
    if (/\binbouw/.test(t) && (k === "thermostaatkraan" || k === "wastafelkraan" || k === "badkraan") &&
        idx.cats.some(function (c) { return c.sleutel === "inbouwkraan"; })) k = "inbouwkraan";
    // "thermostaat bad" of "kraan voor het bad" is een badkraan.
    else if (/(^|[^a-z])bad([^a-z]|$)/.test(t) && (k === "thermostaatkraan" || k === "wastafelkraan") &&
        idx.cats.some(function (c) { return c.sleutel === "badkraan"; })) k = "badkraan";
    return k;
  }

  function woorden(t) { return plat(t).split(/[^a-z0-9]+/).filter(Boolean); }
  function lev1(a, b) { // afstand hooguit 1 (een letter anders, erbij of eraf)
    if (a === b) return true;
    if (Math.abs(a.length - b.length) > 1) return false;
    var i = 0, j = 0, fout = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) { i++; j++; continue; }
      if (++fout > 1) return false;
      if (a.length > b.length) i++; else if (b.length > a.length) j++; else { i++; j++; }
    }
    return fout + (a.length - i) + (b.length - j) <= 1;
  }
  function serieScore(serie, set, lijst) {
    var sw = woorden(serie);
    if (!sw.length) return 0;
    for (var i = 0; i < sw.length; i++) {
      var w = sw[i];
      if (set[w]) continue;
      // Kleine tikfout mag (grotherm/grohtherm), maar niet in een typenummer (UP320 is geen UP720).
      if (w.length >= 5 && !/\d/.test(w) && lijst.some(function (x) { return x[0] === w[0] && !/\d/.test(x) && lev1(x, w); })) continue;
      return 0;
    }
    return sw.length;
  }

  // Zonder merknaam telt een serie alleen als die een eigen naam heeft (minstens 6 letters) en
  // geen gewoon woord is ("Comfort", "Douchedrain", "Kwartrond"), anders matcht elke regel.
  var GEWONE_WOORDEN = /^(comfort|compact|single|square|design|classic|smart|multi|connect|quadro|essence|essentials|focus|double|select|element|perfect|performance|cosmopolitan|infinity|hooked|fusion|douchedrain|showerdrain|tegeldrain|hoekinstap|kwartrond|inloop|standaard|premium|deluxe|modern|retro|basic|luxe|black|white|chrome|chroom)$/;
  function serieZonderMerk(serie) {
    var sw = woorden(serie);
    return sw.some(function (w) {
      return w.length >= 6 && /^[a-z]/.test(w) && !GEWONE_WOORDEN.test(w);
    });
  }

  function zoekAantalInTekst(t) {
    var m = /(?:^|\s)(\d{1,3})\s*(?:x|×|st\.?|stuks?)(?=\s|$)(?!\s*\d)/i.exec(t);
    return m ? parseInt(m[1], 10) : null;
  }

  // Geeft null of { merk, serie, code, ean, categorie, artikel, match, aantal }.
  function herkenProduct(omschrijving, PD) {
    if (!PD || !omschrijving) return null;
    var idx = index(PD), t = plat(omschrijving);
    var uit = { merk: null, serie: null, code: null, ean: null, categorie: null, artikel: null, match: null,
      aantal: zoekAantalInTekst(omschrijving) };
    var vensters = codeVensters(omschrijving);

    // 1. EAN of artikelnummer
    for (var i = 0; i < vensters.length; i++) {
      var v = vensters[i];
      if (/^\d{13}$/.test(v.norm)) {
        if (idx.ean[v.norm]) { uit.ean = v.norm; uit.artikel = idx.ean[v.norm]; break; }
        if (!uit.ean && eanGeldig(v.norm)) uit.ean = v.norm;
      }
      if (idx.codes[v.norm]) { uit.code = v.ruw; uit.artikel = idx.codes[v.norm]; break; }
    }
    var merkNaam = zoekMerk(t, idx);
    if (uit.artikel) {
      var a = uit.artikel;
      if (!uit.code && a.codes && a.codes.length) uit.code = a.codes[0];
      uit.merk = a.merk; uit.serie = a.serie; uit.categorie = a.categorie; uit.match = "exact";
      return uit;
    }
    // Code die past bij het nummerformaat van een merk (zonder artikel in de data).
    var codeMerken = [], codePer = {};
    vensters.forEach(function (v) {
      idx.merken.forEach(function (m) {
        if (!codePer[m.naam] && m.re.some(function (re) { return heelMatch(re, v.ruw) || heelMatch(re, v.norm); })) {
          codePer[m.naam] = v.ruw; codeMerken.push(m.naam);
        }
      });
    });
    if (merkNaam) { uit.merk = merkNaam; uit.code = codePer[merkNaam] || null; }
    else if (codeMerken.length === 1) { uit.merk = codeMerken[0]; uit.code = codePer[codeMerken[0]]; }
    else if (codeMerken.length > 1) uit.code = codePer[codeMerken[0]]; // formaat past bij meer merken: geen merk kiezen

    var cat = zoekCategorie(t, idx);
    uit.categorie = cat;

    // 2. merk + serie
    var tw = woorden(omschrijving), set = {};
    tw.forEach(function (w, i) { set[w] = true; if (tw[i + 1]) set[w + tw[i + 1]] = true; });
    var kandidaten = (PD.artikelen || []).filter(function (a) { return !uit.merk || a.merk === uit.merk; });
    var beste = null;
    kandidaten.forEach(function (a) {
      var s = serieScore(a.serie, set, tw);
      if (!s) return;
      if (!uit.merk && !serieZonderMerk(a.serie)) return;
      var catOk = !cat || a.categorie === cat;
      var overlap = woorden(a.oms).filter(function (w) { return w.length >= 3 && set[w]; }).length; // ook kleur: wit, mat
      var score = (catOk ? 1000 : 0) + s * 50 + overlap;
      if (!beste || score > beste.score) beste = { a: a, score: score, catOk: catOk, gelijk: [a] };
      else if (score === beste.score && a.serie === beste.a.serie && a.categorie === beste.a.categorie) beste.gelijk.push(a);
    });
    if (beste && (beste.catOk || uit.merk)) {
      uit.merk = beste.a.merk; uit.serie = beste.a.serie;
      if (beste.catOk) {
        uit.artikel = beste.a; uit.categorie = beste.a.categorie; uit.match = "serie";
        // Meer uitvoeringen van dezelfde serie (kleur, maat) die de tekst niet onderscheidt.
        if (beste.gelijk.length > 1) uit.varianten = beste.gelijk;
        return uit;
      }
    }
    // 3. categorie
    if (uit.categorie) { uit.match = "categorie"; return uit; }
    return uit.merk || uit.code || uit.ean ? uit : null;
  }

  // Geldt een productregel als 'onvoldoende gespecificeerd' (sanitair als één post zonder merk of type)?
  function bewijsProduct(t, oms, PD) {
    if (PD) {
      var idx = index(PD);
      if (zoekMerk(t, idx)) return true;
      var v = codeVensters(oms);
      if (v.some(function (x) { return idx.codes[x.norm] || idx.ean[x.norm] || (/^\d{13}$/.test(x.norm) && eanGeldig(x.norm)) ||
        idx.merken.some(function (m) { return m.re.some(function (re) { return heelMatch(re, x.ruw) || heelMatch(re, x.norm); }); }); })) return true;
      return false;
    }
    if (MERKEN_BASIS.some(function (m) { return bevatWoord(t, m) >= 0; })) return true;
    return codeVensters(oms).some(function (x) { return /^\d{8,13}$/.test(x.norm) || /^\d{3}\d{3}[A-Z0-9]{2}\d$/.test(x.norm); });
  }
  function onvoldoendeGespecificeerd(omschrijving, PD) {
    var t = plat(omschrijving);
    if (bewijsProduct(t, omschrijving, PD)) return false;
    if (/\bsanitair\b|sanitairpakket|sanitairset/.test(t)) return true;
    if (PD) {
      var c = zoekCategorie(t, index(PD), true);
      if (c.length >= 3) return true; // drie of meer soorten onderdelen in één bedrag
    }
    return false;
  }

  var RE_ARBEID_START = /^[\W\d]*(?:\d+\s*(?:x|st\.?|stuks?)\s+)?(montage|monteren|plaatsen|installeren|installatie|aansluiten|demonteren|demontage|slopen|sloop|verwijderen|leggen|zetten|tegelzetten|tegelwerk|betegelen|loodgieter\w*|leidingwerk|elektra|arbeid\w*|uren|regie|voorrijkosten|kitten|kitwerk|egaliseren|stucwerk|stuken|waterdicht|afvoeren|aanleggen|aanpassen|verplaatsen|verleggen|frezen|hakken|opruimen|schoonmaken|opleveren|wegwerken|inbouwen|ombouwen|afwerken|afkitten|maken|vervangen)\b/;
  var RE_ARBEID = /\b(montage|monteren|arbeid\w*|uurloon|uurtarief|loon|legloon|regie|manuren|uren|sloop\w*|slopen|tegelwerk|tegelzetten|leidingwerk|elektra|voorrijkosten|kitwerk|stucwerk|egaliseren|demontage|demonteren|installatiewerk|aansluiten|plaatsen|installeren|zetten|leggen|afvoeren|container|stortkosten|waterdicht\s+maken)\b/;
  var RE_INCL_MONTAGE = /\b(incl\.?|inclusief|met|en)\s+(de\s+)?(montage|plaatsing|installatie|aansluiten|monteren|plaatsen)\b/;
  var RE_MATERIAAL = /\b(tegellijm|lijm|voegmiddel|voegsel|voeg|kit|siliconen\w*|kimband|folie|tegelfolie|primer|voorstrijk\w*|egaliseermiddel|cement|zand|profielen|profiel|hoekprofiel\w*|afvoerbuis|buizen|buis|pvc|pex|klein\s*materiaal|bevestigingsmateriaal|hulpmaterialen|hulpmateriaal|materialen|materiaal|gipsplaat\w*|isolatie\w*|metal\s*stud|regelwerk|afdichting\w*|coating|sifon|afvoerset|stelpost\s+tegels)\b/;

  // "product" | "arbeid" | "materiaal" | "overig". PD is optioneel (betere merkherkenning).
  function soortRegel(omschrijving, PD) {
    var t = plat(omschrijving).trim();
    if (letters(t) < 3) return "overig";
    if (/korting|reductie|kortings/.test(t)) return "overig";
    var bewijs = bewijsProduct(t, omschrijving, PD);
    if (RE_ARBEID_START.test(t)) return "arbeid";
    if (bewijs) return "product";
    var cat = PD ? zoekCategorie(t, index(PD)) : null;
    if (onvoldoendeGespecificeerd(omschrijving, PD)) return "materiaal";
    if (cat && RE_INCL_MONTAGE.test(t)) return "product";
    if (RE_ARBEID.test(t)) return "arbeid";
    if (RE_MATERIAAL.test(t)) return "materiaal";
    if (cat) return "product";
    var type = bepaalType(omschrijving);
    if (type === "tegels") return "product";
    if (type === "sanitair") return PD ? "materiaal" : "product";
    if (/^(sloop|afval|tegelwerk|waterdicht|vloer|leidingwerk|elektra|vloerverwarming|ventilatie|montage|kitwerk|uren)$/.test(type)) return "arbeid";
    return "overig";
  }

  function pct(n) { return Math.abs(Math.round(n)) + "%"; }

  // Geeft { oordeel, band, verschilPct, toelichting, bron, bronnen, prijs, aantal }.
  // oordeel: "binnen" | "boven" (meer dan 25% boven de bovenkant) | "onder" (meer dan 20% onder de
  // onderkant) | "onbekend". prijs: per stuk (of per m² bij tegels), inclusief btw.
  function beoordeelProduct(post, herk, PD, basis) {
    var uit = { oordeel: "onbekend", band: null, verschilPct: null, toelichting: "", bron: [], bronnen: [], prijs: null, aantal: null };
    post = post || {};
    if (!herk || !PD) { uit.toelichting = "Dit product is niet herkend, daarom is er geen marktprijsband."; return uit; }
    var cats = PD.categorieen || {}, cat = herk.categorie ? cats[herk.categorie] : null, a = herk.artikel;
    var eenheid = (cat && cat.eenheid) || "st";
    if (a && a.van != null && a.tot != null && herk.varianten && herk.varianten.length > 1) {
      // Band van alle uitvoeringen samen: van de laagste 'van' tot de hoogste 'tot'.
      uit.band = { van: Math.min.apply(null, herk.varianten.map(function (x) { return x.van; })),
        tot: Math.max.apply(null, herk.varianten.map(function (x) { return x.tot; })), soort: "artikel", varianten: herk.varianten.length };
      uit.bron = herk.varianten.map(function (x) { return x.bron; }).filter(function (x, i, l) { return x && l.indexOf(x) === i; });
    } else if (a && a.van != null && a.tot != null) {
      uit.band = { van: a.van, tot: a.tot, soort: "artikel" };
      uit.bron = a.bron ? [a.bron] : [];
    } else if (cat && cat.van != null && cat.tot != null) {
      uit.band = { van: cat.van, tot: cat.tot, soort: "categorie" };
      uit.bron = (cat.bron || []).slice();
    } else {
      uit.toelichting = "Voor dit product hebben we geen marktprijsband.";
      return uit;
    }
    uit.band.eenheid = eenheid;
    uit.bronnen = uit.bron.map(function (k) { var b = (PD.bronnen || {})[k] || []; return { sleutel: k, oms: b[0] || k, url: b[1] || null }; });
    var peil = peildatumTekst(PD), bandTxt = euro(uit.band.van) + "–" + euro(uit.band.tot) + (eenheid === "m2" ? " per m²" : "");
    uit.match = herk.match;
    // Tekst volgt band.soort en match: exact = dit artikel, serie = deze serie, anders de categorie.
    var bandZin = (uit.band.soort === "artikel" && herk.match === "exact" ? "de marktprijsband van dit artikel" :
      uit.band.soort === "artikel" ? "de marktprijsband van deze serie" + (uit.band.varianten ? " (" + uit.band.varianten + " uitvoeringen)" : "") : "de marktprijsband voor " + (cat ? cat.naam.toLowerCase() : "deze categorie"))
      + " van " + bandTxt + (peil ? " (peildatum " + peil + ")" : "");
    var grof = uit.band.soort === "categorie" ? " Het precieze type is niet herkend, dus dit is een grove vergelijking." : "";

    if (post.bedrag == null && post.eenheidsprijs == null) { uit.toelichting = "Er staat geen bedrag bij deze regel. Ter vergelijking: " + bandZin + "."; return uit; }
    var prijs = null, n = 1;
    if (eenheid === "m2") {
      if (post.eenheidsprijs != null && (post.eenheid === "m2" || post.alleenTarief)) prijs = post.eenheidsprijs;
      else if (post.eenheid === "m2" && post.aantal && post.bedrag != null) prijs = post.bedrag / post.aantal;
      if (prijs == null) { uit.toelichting = "We kunnen de prijs niet per m² uitrekenen, omdat het aantal m² ontbreekt. Ter vergelijking: " + bandZin + "."; return uit; }
      n = post.aantal || null;
    } else {
      if (post.eenheid && !/^(st|post)$/.test(post.eenheid)) { uit.toelichting = "Deze regel staat in een andere eenheid (" + (EENHEDEN[post.eenheid] || post.eenheid) + "), daarom vergelijken we hem niet per stuk."; return uit; }
      n = (post.eenheid === "st" && post.aantal) || herk.aantal || 1;
      prijs = post.eenheidsprijs != null && post.eenheid === "st" ? post.eenheidsprijs : (post.bedrag != null ? post.bedrag / n : post.eenheidsprijs);
    }
    var tarief = post.btw != null && post.btw > 0 ? post.btw : 21;
    if (basis === "excl") prijs = prijs * (1 + tarief / 100);
    prijs = rond(Math.abs(prijs));
    uit.prijs = prijs; uit.aantal = n;
    var perStuk = eenheid === "st" && n > 1 ? " Gerekend per stuk: " + n + " × " + euro(prijs) + " inclusief btw." : "";
    if (eenheid === "st" && n === 1 && prijs > 0) perStuk = " Gerekend met " + euro(prijs) + " inclusief btw.";

    if (RE_INCL_MONTAGE.test(plat(post.omschrijving || ""))) {
      uit.toelichting = "Deze regel is inclusief montage. De marktprijsband geldt alleen voor het product, daarom geven we geen oordeel. Ter vergelijking: " + bandZin + ".";
      return uit;
    }
    var van = uit.band.van, tot = uit.band.tot;
    if (prijs > tot) uit.verschilPct = Math.round((prijs - tot) / tot * 100);
    else if (prijs < van) uit.verschilPct = -Math.round((van - prijs) / van * 100);
    else uit.verschilPct = 0;

    if (prijs > tot * 1.25) {
      uit.oordeel = "boven";
      uit.toelichting = "Deze regel ligt " + pct(uit.verschilPct) + " boven " + bandZin + "." + perStuk + grof +
        " Webwinkelprijzen zijn geen installateursprijzen: een installateur rekent vaak een opslag op materiaal, voor garantie, risico en levering. Vraag waaruit het verschil bestaat.";
    } else if (prijs < van * 0.8) {
      uit.oordeel = "onder";
      uit.toelichting = "Deze regel ligt " + pct(uit.verschilPct) + " onder " + bandZin + "." + perStuk + grof +
        " Check of het hetzelfde type en dezelfde maat is.";
    } else {
      uit.oordeel = "binnen";
      if (uit.verschilPct > 0) uit.toelichting = "Deze regel ligt " + pct(uit.verschilPct) + " boven de bovenkant van " + bandZin +
        ". Dat valt binnen een gebruikelijke opslag van een installateur op materiaal." + perStuk + grof;
      else if (uit.verschilPct < 0) uit.toelichting = "Deze regel ligt " + pct(uit.verschilPct) + " onder de onderkant van " + bandZin +
        ", maar nog binnen de marge." + perStuk + grof;
      else uit.toelichting = "Deze regel valt binnen " + bandZin + "." + perStuk + grof;
    }
    return uit;
  }

  function voegProductenToe(res, PD) {
    (res.posten || []).forEach(function (p) {
      p.soort = soortRegel(p.omschrijving, PD);
      if (p.soort === "materiaal" && onvoldoendeGespecificeerd(p.omschrijving, PD)) {
        p.vaag = true;
        p.vaagTekst = VAAG_TEKST;
      }
      if (PD && p.soort === "product") {
        p.product = herkenProduct(p.omschrijving, PD);
        p.productOordeel = beoordeelProduct(p, p.product, PD, res.basis);
      }
    });
    return res;
  }

  /* ------------------------------------------------------------ geanonimiseerde specificatie */
  // Platte tekst met alleen de posten (omschrijving, aantal, bedrag) en de totalen. Regels met
  // contact- of bedrijfsgegevens van de aanbieder of de klant vallen weg.
  var RE_PRIVE = [
    /[\w.+-]+@[\w-]+\.[\w.]+/,                                         // e-mail
    /https?:\/\/|\bwww\.|\b[\w-]+\.(nl|com|be|eu|net|org|info)\b/i,    // URL of website
    /(\+31|0031|\b0)[\s\-]?[1-9](?:[\s\-]?\d){7,8}\b/,                 // telefoonnummer
    /\b\d{4}\s?[A-Z]{2}\b/,                                            // postcode
    /\b[A-Z]{2}\d{2}\s?[A-Z]{4}(?:\s?\d){6,}/i,                        // IBAN
    /\bkvk\b|k\.v\.k|kamer\s+van\s+koophandel/i,                       // KvK
    /btw[\s\-]?(nr|nummer|id|identificatie)|\bNL\s?\d{9}\s?B\s?\d{2}\b/i, // btw-nummer
    /t\.a\.v|\btav\b|geachte|offerte\s*-?\s*(nummer|nr)|offertenr|klant\s*-?\s*(nummer|nr)|factuur\s*-?\s*(nummer|nr)|dossier\s*-?\s*(nummer|nr)|projectnummer/i,
    /\b(dhr|mevr|mw|fam|de\s+heer|mevrouw)\b\.?/i,
    /\bB\.V\.|\bBV\b|\bV\.O\.F\.|\bVOF\b/
  ];
  function prive(t) { return RE_PRIVE.some(function (re) { return re.test(t); }); }
  function kaalEuro(n) { return euro(n).replace(/ /g, " "); }

  function anoniemeSpecificatie(res) {
    res = res || {};
    var basis = res.basis === "incl" ? "incl." : "excl.";
    var r = ["Specificatie badkamerofferte (zonder naam-, adres- en contactgegevens)", "Bedragen per post " + basis + " btw.", "", "Posten:"];
    var weg = 0, n = 0;
    (res.posten || []).forEach(function (p) {
      var oms = String(p.omschrijving || "").replace(/\s+/g, " ").trim();
      if (!oms || prive(oms)) { weg++; return; }
      var delen = [oms];
      if (p.aantal != null) delen.push(String(p.aantal).replace(".", ",") + " " + (EENHEDEN[p.eenheid] || p.eenheid || "").trim());
      if (p.eenheidsprijs != null && p.alleenTarief) delen.push(kaalEuro(p.eenheidsprijs) + " per " + (EENHEDEN[p.eenheid] || "eenheid"));
      if (p.bedrag != null) delen.push(kaalEuro(p.bedrag));
      var noot = [];
      if (p.stelpost) noot.push("stelpost");
      if (p.optie) noot.push("optie, telt niet mee");
      else if (!p.meetellen) noot.push("telt niet mee");
      if (p.vaag) noot.push("merk en type niet genoemd");
      r.push("- " + delen.join(" | ") + (noot.length ? " (" + noot.join(", ") + ")" : ""));
      n++;
    });
    if (!n) r.push("- (geen posten gevonden)");
    var t = res.totaal || {};
    r.push("");
    if (t.excl != null) r.push("Totaal excl. btw: " + kaalEuro(t.excl));
    if (t.btw != null) r.push("Btw" + ((res.btwTarieven || []).length ? " (" + res.btwTarieven.join("% en ") + "%)" : "") + ": " + kaalEuro(t.btw));
    if (t.incl != null) r.push("Totaal incl. btw: " + kaalEuro(t.incl));
    if (weg) r.push("", "(" + weg + " regel" + (weg > 1 ? "s" : "") + " met persoons- of bedrijfsgegevens weggelaten)");
    return r.join("\n");
  }

  return {
    TYPES: TYPES, EENHEDEN: EENHEDEN, getal: getal, euro: euro, leesOfferte: leesOfferte,
    beoordeelPost: beoordeelPost, checklist: checklist, algemeneVragen: algemeneVragen,
    bepaalType: bepaalType, controle: controle,
    soortRegel: soortRegel, herkenProduct: herkenProduct, beoordeelProduct: beoordeelProduct,
    anoniemeSpecificatie: anoniemeSpecificatie, onvoldoendeGespecificeerd: onvoldoendeGespecificeerd,
    normCode: normCode, VAAG_TEKST: VAAG_TEKST
  };
});
