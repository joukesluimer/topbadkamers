# -*- coding: utf-8 -*-
"""
Badkamercheck: "Is je badkamer aan vervanging toe?" op /tools/badkamercheck/

Elf korte vragen, één per stap. De uitkomst is een score van 0 tot 100 en een van
drie adviezen: onderhoud is genoeg, een gedeeltelijke renovatie of een complete
renovatie. Daaronder staan aandachtspunten per antwoord. Alle teksten en links
staan in de HTML; het script zet alleen de juiste blokken aan. Er wordt niets
opgeslagen en niets verstuurd.

Aanpak naar het voorbeeld van onderhoudscheck.py (Topschilder).
Interface voor build.py: LINKS en build(write). CSS en JS staan in deze module.
"""

import json

from components import page, crumbs, faq_blok, cta_blok, title

PAD = "/tools/badkamercheck/"

LINKS = [
    (PAD, "Badkamercheck",
     "Elf korte vragen: is onderhoud genoeg, of is je badkamer toe aan een gedeeltelijke of complete renovatie?"),
]

# Bronnen (geraadpleegd in november 2026)
BRONNEN = {
    "asbest": ("Informatiepunt Leefomgeving (IPLO), Asbest binnen in huis", "https://iplo.nl/thema/asbest/asbestwegwijzer/binnen-huis/"),
    "asbestregels": ("Rijksoverheid, Asbestregels", "https://www.rijksoverheid.nl/onderwerpen/asbest/asbestregels"),
    "lood": ("Rijksoverheid, Hoe kan ik loden leidingen in mijn huis opsporen en laten vervangen?", "https://www.rijksoverheid.nl/onderwerpen/gezond-en-veilig-wonen/vraag-en-antwoord/hoe-kan-ik-loden-leidingen-in-mijn-huis-opsporen-en-laten-vervangen"),
    "schimmel": ("Volkshuisvesting Nederland, Aanpak vocht en schimmel", "https://www.volkshuisvestingnederland.nl/onderwerpen/aanpak-vocht-en-schimmel"),
    "rivm": ("RIVM, Schimmel en vocht in woningen (factsheet)", "https://rivm.nl/sites/default/files/2018-11/84305-008013_Schimmel%20en%20vocht%20TG2.pdf"),
}


def _bl(k, kort):
    return f'<a href="{BRONNEN[k][1]}" rel="noopener" target="_blank">{kort}</a>'


# ---------------------------------------------------------------------------
# De vragen: (sleutel, vraag, hint, [(waarde, label, toelichting, toon, punten, vlag)])
# toon: g (goed), o (let op), r (slecht), n (neutraal). vlag stuurt het advies (zie LOGICA_JS).
# ---------------------------------------------------------------------------

VRAGEN = [
    ("leeftijd", "Hoe oud is je badkamer?", "Gerekend vanaf de laatste keer dat hij helemaal vernieuwd is. Een schatting is goed genoeg.",
     [("0-10", "Jonger dan 10 jaar", "Nog vrij nieuw", "g", 0, ""),
      ("10-20", "10 tot 20 jaar", "Middelbare leeftijd", "o", 1, ""),
      ("20-30", "20 tot 30 jaar", "Op leeftijd", "r", 2.5, "oud"),
      ("30+", "Ouder dan 30 jaar", "Of nooit vernieuwd", "r", 3.5, "oud"),
      ("onbekend", "Weet ik niet", "Bijvoorbeeld net verhuisd", "n", 1.5, "")]),
    ("uiterlijk", "Hoe tevreden ben je over hoe de badkamer eruitziet?", "Denk aan de tegels, het sanitair en de indeling.",
     [("tevreden", "Tevreden", "Hij mag zo blijven", "g", 0, ""),
      ("gedateerd", "Wat gedateerd", "Het kan frisser", "o", 1.5, ""),
      ("niet", "Helemaal niet", "Ik wil iets anders", "r", 2.5, "")]),
    ("voegen", "Hoe zien de voegen en kitranden eruit?", "Kijk langs het bad, de douche, de wastafel en in de hoeken.",
     [("goed", "Schoon en heel", "De kit is soepel", "g", 0, ""),
      ("verkleurd", "Verkleurd of zwart", "Maar nog heel", "o", 1, ""),
      ("kapot", "Gescheurd of los", "Of er ontbreken stukken", "r", 2, "")]),
    ("schimmel", "Zie je schimmel?", "Zwarte puntjes of plekken op de voegen, de kit, het plafond of de muur.",
     [("nee", "Nee", "Alles is schoon", "g", 0, ""),
      ("plekjes", "Een paar plekjes", "Gaat weg met schoonmaken", "o", 1, ""),
      ("terug", "Komt steeds terug", "Ook op plafond of muur", "r", 2.5, "")]),
    ("lekkage", "Zie je vlekken op het plafond onder de badkamer, of is er lekkage?", "Kijk in de ruimte onder de badkamer. Bij een appartement kun je het ook aan de onderburen vragen.",
     [("nee", "Nee, nooit gehad", "Plafond is schoon", "g", 0, ""),
      ("vroeger", "Ooit gehad, opgelost", "Nu droog", "o", 1, ""),
      ("nu", "Ja, nu", "Vlekken, een kring of druppels", "r", 4, "lek")]),
    ("tegels", "Zitten de tegels nog vast?", "Tik met een knokkel op de wand- en vloertegels. Klinkt het hol of beweegt een tegel?",
     [("vast", "Alles zit vast", "Geen barsten", "g", 0, ""),
      ("enkele", "Een paar hol of gebarsten", "Hier en daar", "o", 1.5, ""),
      ("meerdere", "Meerdere los of hol", "Vooral bij de douche", "r", 3, "tegels")]),
    ("afvoer", "Hoe werkt de afvoer?", "Van de douche, het bad en de wastafel.",
     [("goed", "Loopt goed weg", "Geen geur", "g", 0, ""),
      ("traag", "Soms traag", "Na ontstoppen weer goed", "o", 0.5, ""),
      ("stank", "Traag of stank", "Steeds weer", "r", 2, "")]),
    ("kraan", "Hoe zijn de kranen en de douche?", "Let op kalk, druppelen en de temperatuur.",
     [("goed", "Werken prima", "Geen druppels", "g", 0, ""),
      ("kalk", "Kalkaanslag of een druppel", "Verder in orde", "o", 0.5, ""),
      ("slecht", "Kraan lekt of temperatuur wisselt", "De thermostaat doet het slecht", "r", 1.5, "")]),
    ("ventilatie", "Hoe ventileert je badkamer?", "Een raam alleen is vaak niet genoeg: de badkamer koelt dan snel af en het vocht slaat neer.",
     [("goed", "Afzuiging die goed werkt", "Spiegel is snel weer helder", "g", 0, ""),
      ("matig", "Alleen een raam of zwakke afzuiging", "Het blijft lang vochtig", "o", 1, ""),
      ("geen", "Geen raam en geen afzuiging", "Of de afzuiging doet het niet", "r", 2, "")]),
    ("bouwjaar", "Wanneer is je woning gebouwd?", "Ongeveer is goed. Het zegt iets over asbest en oude leidingen.",
     [("voor1960", "Voor 1960", "Vooroorlogs of wederopbouw", "n", 1, ""),
      ("1960-1993", "1960 tot 1994", "Jaren 60, 70, 80 en begin 90", "n", 0.5, ""),
      ("1994+", "1994 of later", "Nieuwere woning", "n", 0, "")]),
    ("wensen", "Wat wil je anders?", "Kies wat het beste past.",
     [("niets", "Niets, het moet vooral weer goed zijn", "Zelfde indeling", "n", 0, ""),
      ("inloop", "Een inloopdouche", "In plaats van een bad of douchebak", "n", 2, "wens_deel"),
      ("toegankelijk", "Toegankelijk en veilig", "Drempelvrij, beugels, een hoger toilet", "n", 2.5, "wens_deel"),
      ("indeling", "Een andere indeling", "Douche, toilet of bad op een andere plek", "n", 4, "wens_compleet")]),
]

MAX_PUNTEN = sum(max(o[4] for o in opties) for _, _, _, opties in VRAGEN)
PUNTEN = {k: {o[0]: [o[4], o[5]] for o in opties} for k, _, _, opties in VRAGEN}

# ---------------------------------------------------------------------------
# Aandachtspunten per antwoord (vraag, waarde) -> html. Staan verborgen in de pagina.
# ---------------------------------------------------------------------------

PUNTEN_TEKST = [
    (("leeftijd", "20-30"), "<strong>Leeftijd.</strong> Na 20 jaar zijn leidingen, afvoer en de waterdichte laag onder de tegels vaak aan het eind. Laat bij een opknapbeurt ook naar de leidingen kijken."),
    (("leeftijd", "30+"), "<strong>Leeftijd.</strong> Een badkamer van meer dan 30 jaar heeft vaak nog geen goede waterdichte laag onder de tegels. Bij nieuwe tegels hoort die er wel in. Lees <a href=\"/kennisbank/badkamer-waterdicht-maken/\">hoe je een badkamer waterdicht maakt</a>."),
    (("uiterlijk", "gedateerd"), "<strong>Uiterlijk.</strong> Is alleen het uiterlijk het probleem? Nieuwe kranen, een wastafelmeubel en nieuw kitwerk maken al veel verschil, zonder te slopen. Zie <a href=\"/badkamerspullen/wastafelmeubel-kiezen/\">een wastafelmeubel kiezen</a>."),
    (("uiterlijk", "niet"), "<strong>Uiterlijk.</strong> Wil je echt iets anders, dan kom je al snel bij nieuwe tegels. Dat is meestal het moment om de hele badkamer aan te pakken. Inspiratie vind je bij de <a href=\"/tools/stijlkiezer/\">stijlkiezer</a>."),
    (("voegen", "verkleurd"), "<strong>Voegen en kit.</strong> Verkleurde kit kun je laten vervangen. Dat is goedkoop onderhoud: zie <a href=\"/kosten/kitwerk-voegen/\">wat kitwerk en voegen kosten</a>."),
    (("voegen", "kapot"), "<strong>Voegen en kit.</strong> Door gescheurde of losse kit loopt water achter de tegels. Laat het snel vervangen, dan voorkom je lekkage. Zie <a href=\"/kosten/kitwerk-voegen/\">wat kitwerk en voegen kosten</a>."),
    (("schimmel", "plekjes"), "<strong>Schimmel.</strong> Een paar plekjes is meestal een kwestie van ventileren en schoonmaken. Zet de afzuiging na het douchen een tijd hoog en trek de wanden droog (" + _bl("schimmel", "Volkshuisvesting Nederland") + ")."),
    (("schimmel", "terug"), "<strong>Schimmel.</strong> Schimmel die steeds terugkomt wijst op te veel vocht: slechte ventilatie, of vocht in de muur. Schimmel is ook slecht voor je gezondheid (" + _bl("rivm", "RIVM") + "). Lees meer over <a href=\"/kennisbank/badkamer-ventilatie/\">ventilatie in de badkamer</a>."),
    (("lekkage", "vroeger"), "<strong>Lekkage.</strong> Is de oorzaak echt gevonden? Kijk het plafond eronder af en toe na. Komt er een nieuwe vlek, laat dan meteen kijken."),
    (("lekkage", "nu"), "<strong>Lekkage.</strong> Een vlek op het plafond eronder betekent dat er water door de vloer gaat. Wacht niet: laat een specialist de oorzaak zoeken. Zit het in de douchevloer of de waterdichting, dan is opnieuw tegelen vaak de enige echte oplossing."),
    (("tegels", "enkele"), "<strong>Tegels.</strong> Een paar losse of gebarsten tegels kan een tegelzetter vaak vervangen, als er nog reservetegels zijn. Zie <a href=\"/kosten/tegelzetter-per-m2/\">wat een tegelzetter kost</a>."),
    (("tegels", "meerdere"), "<strong>Tegels.</strong> Meerdere holle tegels, vooral bij de douche, kunnen betekenen dat er al water achter zit. Dan helpt alleen opnieuw tegelen, met een waterdichte laag eronder."),
    (("afvoer", "traag"), "<strong>Afvoer.</strong> Haal regelmatig haren uit het putje en maak de sifon schoon. Helpt dat niet meer, laat dan een loodgieter kijken."),
    (("afvoer", "stank"), "<strong>Afvoer.</strong> Steeds stank of een trage afvoer kan liggen aan een verkeerd afschot, een verzakte leiding of een slechte ontluchting. Dat los je vaak pas op als de vloer open gaat. Zie het <a href=\"/kosten/uurtarief-loodgieter/\">uurtarief van een loodgieter</a>."),
    (("kraan", "kalk"), "<strong>Kalk.</strong> Ontkalk de douchekop en de straalbrekers met azijn of citroenzuur. Een druppelende kraan heeft vaak alleen een nieuw binnenwerk nodig."),
    (("kraan", "slecht"), "<strong>Kranen.</strong> Een lekkende kraan of een thermostaat die niet meer goed regelt, vervang je los. Zie <a href=\"/badkamerspullen/kranen-kiezen/\">kranen kiezen</a> en <a href=\"/badkamerspullen/douchesysteem-kiezen/\">een douchesysteem kiezen</a>."),
    (("ventilatie", "matig"), "<strong>Ventilatie.</strong> Met alleen een raam koelt de badkamer snel af en blijft het vocht hangen. Een mechanische afzuiging werkt beter. Lees meer over <a href=\"/kennisbank/badkamer-ventilatie/\">ventilatie in de badkamer</a>."),
    (("ventilatie", "geen"), "<strong>Ventilatie.</strong> Zonder ventilatie krijg je vrijwel zeker vocht en schimmel, ook in een nieuwe badkamer. Laat bij elke renovatie een afzuiging meenemen. Zie <a href=\"/kennisbank/badkamer-ventilatie/\">ventilatie in de badkamer</a>."),
    (("bouwjaar", "voor1960"), "<strong>Oude woning.</strong> In woningen van voor 1960 kunnen nog loden waterleidingen liggen; de overheid raadt aan die te laten vervangen (" + _bl("lood", "Rijksoverheid") + "). In woningen van voor 1994 kan ook asbest zitten, bijvoorbeeld in kit, plaatmateriaal of vloerzeil (" + _bl("asbest", "IPLO") + "). Lees <a href=\"/kennisbank/asbest-in-badkamer/\">asbest in de badkamer</a>."),
    (("bouwjaar", "1960-1993"), "<strong>Asbest.</strong> In woningen van voor 1994 kan asbest zitten, bijvoorbeeld in kit, plaatmateriaal of vloerzeil (" + _bl("asbest", "IPLO") + "). Voor je gaat slopen, laat je dat eerst uitzoeken (" + _bl("asbestregels", "Rijksoverheid") + "). Lees <a href=\"/kennisbank/asbest-in-badkamer/\">asbest in de badkamer</a>."),
    (("wensen", "inloop"), "<strong>Inloopdouche.</strong> Vaak kan een inloopdouche op de plek van het bad of de douchebak, zonder de hele badkamer te slopen. Zie <a href=\"/kosten/inloopdouche/\">wat een inloopdouche kost</a> en <a href=\"/kennisbank/inloopdouche-zonder-drempel/\">een inloopdouche zonder drempel</a>."),
    (("wensen", "toegankelijk"), "<strong>Toegankelijk.</strong> Een drempelvrije douche, beugels en een hoger toilet maken de badkamer veiliger. Vraag bij je gemeente of je hulp of een vergoeding kunt krijgen via de Wmo. Lees <a href=\"/kennisbank/inloopdouche-zonder-drempel/\">een inloopdouche zonder drempel</a>."),
    (("wensen", "indeling"), "<strong>Andere indeling.</strong> Gaan douche, toilet of bad naar een andere plek, dan moeten leidingen en afvoer mee. Dat is bijna altijd een complete renovatie. Gebruik de <a href=\"/tools/renovatieplanner/\">renovatieplanner</a> om de stappen te zien."),
]

ADVIEZEN = {
    "onderhoud": ("Onderhoud is genoeg",
                  "Je badkamer is in redelijke staat. Met goed onderhoud gaat hij nog jaren mee: nieuwe kit, voegen bijwerken en een kraan vervangen waar nodig.",
                  '<a class="btn btn-primary" href="/diensten/badkamer-onderhoud/">Badkamer onderhoud</a> '
                  '<a class="btn btn-ghost" href="/kosten/kitwerk-voegen/">Kosten kitwerk en voegen</a>'),
    "deel": ("Een gedeeltelijke renovatie",
             "Een paar onderdelen zijn aan vervanging toe, maar je hoeft niet alles te slopen. Denk aan een inloopdouche op de plek van het bad, nieuwe kranen, of de douchehoek opnieuw tegelen.",
             '<a class="btn btn-primary" href="/offerte-aanvragen/">Vraag offertes aan</a> '
             '<a class="btn btn-ghost" href="/kosten/inloopdouche/">Kosten inloopdouche</a> '
             '<a class="btn btn-ghost" href="/diensten/tegelwerk-badkamer/">Tegelwerk badkamer</a>'),
    "compleet": ("Een complete renovatie",
                 "Er spelen meerdere dingen tegelijk, of dingen die je alleen oplost als de vloer en de wanden open gaan. Dan is een complete renovatie meestal de beste keuze: alles in één keer goed, met nieuwe leidingen en een waterdichte laag.",
                 '<a class="btn btn-primary" href="/tools/badkamercalculator/">Reken het uit</a> '
                 '<a class="btn btn-ghost" href="/kosten/nieuwe-badkamer/">Kosten nieuwe badkamer</a>'),
}

# ---------------------------------------------------------------------------
# De rekenlogica, los zodat hij in node te testen is. ans = {vraag: waarde}.
# ---------------------------------------------------------------------------

LOGICA_JS = r"""function bkcAdvies(ans, punten, max) {
  var s = 0, vlag = {};
  Object.keys(punten).forEach(function (k) {
    var p = punten[k][ans[k]];
    if (!p) return;
    s += p[0];
    if (p[1]) vlag[p[1]] = true;
  });
  var score = Math.round(s / max * 100);
  var advies;
  if (score >= 45 || vlag.wens_compleet || (vlag.lek && vlag.oud) || (vlag.tegels && vlag.oud) || (vlag.lek && vlag.tegels)) advies = "compleet";
  else if (score >= 20 || vlag.lek || vlag.tegels || vlag.wens_deel) advies = "deel";
  else advies = "onderhoud";
  // positie van de pijl op de meter: altijd in het vak van het advies
  var positie = advies === "compleet" ? Math.max(score, 48) : advies === "deel" ? Math.min(Math.max(score, 23), 44) : Math.min(score, 18);
  return { score: score, advies: advies, positie: positie, vlaggen: vlag };
}"""


def _vraag_html(i, sleutel, vraag, hint, opties):
    knoppen = "".join(
        f'<button type="button" class="bkc-opt bkc-t-{toon}" data-v="{v}" aria-pressed="false">'
        f'<span class="bkc-lbl">{lbl}</span><span class="bkc-sub">{sub}</span></button>'
        for v, lbl, sub, toon, _p, _f in opties)
    return (f'<fieldset class="bkc-q" data-key="{sleutel}"{"" if i == 0 else " hidden"}>'
            f'<legend class="bkc-vraag">{vraag}</legend><p class="bkc-hint">{hint}</p>'
            f'<div class="bkc-opts">{knoppen}</div></fieldset>')


def build(write):
    cr, cr_ld = crumbs([("Home", "/"), ("Tools", "/tools/"), ("Badkamercheck", None)])
    vragen = "".join(_vraag_html(i, *v) for i, v in enumerate(VRAGEN))
    punten_html = "".join(f'<li data-punt="{k}={v}" hidden>{t}</li>' for (k, v), t in PUNTEN_TEKST)
    adviezen_html = "".join(
        f'<div class="bkc-advies" data-advies="{k}" hidden><h2 class="bkc-titel">{t}</h2><p>{tekst}</p><p class="bkc-knoppen">{knoppen}</p></div>'
        for k, (t, tekst, knoppen) in ADVIEZEN.items())
    n = len(VRAGEN)

    hero = f"""{cr}
<section class="section-sm tool-hero" data-bkc>
<div class="wrap">
  <div class="bkc-grid">
    <div class="bkc-intro">
      <span class="badge">Gratis tool · 2 minuten · niets opgeslagen</span>
      <h1>Is je badkamer aan vervanging toe?</h1>
      <p class="lead">Beantwoord {n} korte vragen over je badkamer. Je krijgt een score en een advies: is onderhoud genoeg, of is een gedeeltelijke of complete renovatie verstandig? Met aandachtspunten per antwoord.</p>
      <ul class="checklist">
        <li>Direct een uitslag, zonder e-mailadres</li>
        <li>Concrete tips per onderdeel</li>
        <li>Je antwoorden blijven op je eigen toestel</li>
      </ul>
    </div>
    <div class="formcard bkc-kaart" aria-live="polite">
      <div class="bkc-quiz">
        <div class="bkc-top">
          <span class="bkc-teller">Vraag <b>1</b> van {n}</span>
          <button type="button" class="btn-link bkc-terug" hidden>← Terug</button>
        </div>
        <div class="bkc-balk"><i style="width:{100 / n:.1f}%"></i></div>
        {vragen}
        <noscript><p class="callout">Zet JavaScript aan om de badkamercheck te doen. Je kunt ook meteen <a href="/offerte-aanvragen/">offertes aanvragen</a>.</p></noscript>
      </div>
      <div class="bkc-uitslag" hidden>
        <p class="bkc-kicker">Jouw uitslag</p>
        <div class="bkc-score"><span class="bkc-getal">0</span><span class="bkc-van">/100</span></div>
        <div class="bkc-meter" aria-hidden="true"><i class="bkc-z1"></i><i class="bkc-z2"></i><i class="bkc-z3"></i><b class="bkc-pijl"></b></div>
        <div class="bkc-meter-lbl"><span>Onderhoud</span><span>Gedeeltelijk</span><span>Compleet</span></div>
        <p class="bkc-klein bkc-uitleg-score">Hoe hoger de score, hoe meer er aan je badkamer speelt. Ook je wensen tellen mee in het advies.</p>
        {adviezen_html}
        <div class="bkc-punten-blok">
          <h3>Aandachtspunten bij jouw antwoorden</h3>
          <ul class="bkc-punten">{punten_html}</ul>
          <p class="bkc-geen" hidden>Bij jouw antwoorden zien we geen bijzondere aandachtspunten. Loop de kit en de voegen wel elk jaar even na.</p>
        </div>
        <p class="bkc-klein">De score is een eerste indruk op basis van jouw antwoorden. Een badkamerspecialist kan ter plekke zien wat er achter de tegels zit. Er wordt niets opgeslagen of verstuurd.</p>
        <p class="bkc-opnieuw"><button type="button" class="btn-link bkc-reset">Opnieuw doen</button></p>
      </div>
    </div>
  </div>
</div>
</section>"""

    uitleg = f"""<section class="section soft"><div class="wrap narrow prose">
  <h2>Onderhoud, gedeeltelijk of compleet: zo kies je</h2>
  <p>Niet elke oude badkamer hoeft eruit. De vraag is vooral of de problemen aan de oppervlakte zitten, of eronder.</p>
  <h3>Onderhoud is genoeg als</h3>
  <ul>
    <li>de tegels vastzitten en er geen lekkage is;</li>
    <li>het vooral gaat om verkleurde kit, wat kalk of een druppelende kraan;</li>
    <li>je tevreden bent over hoe de badkamer eruitziet.</li>
  </ul>
  <p>Nieuwe kit, voegen bijwerken en een kraan vervangen kosten weinig. Zie <a href="/diensten/badkamer-onderhoud/">badkamer onderhoud</a> en <a href="/kosten/kitwerk-voegen/">wat kitwerk en voegen kosten</a>.</p>
  <h3>Een gedeeltelijke renovatie past als</h3>
  <ul>
    <li>één deel aan vervanging toe is, bijvoorbeeld de douchehoek of het bad;</li>
    <li>je een inloopdouche wilt, of de badkamer toegankelijker wilt maken;</li>
    <li>de leidingen en de afvoer op hun plek kunnen blijven.</li>
  </ul>
  <h3>Een complete renovatie is verstandig als</h3>
  <ul>
    <li>er lekkage is naar de verdieping eronder, of veel tegels hol klinken;</li>
    <li>de badkamer ouder is dan zo'n 20 tot 30 jaar en er meerdere dingen tegelijk spelen;</li>
    <li>je de indeling wilt veranderen, zodat leidingen en afvoer mee moeten.</li>
  </ul>
  <p>Wat een complete badkamer kost, lees je bij <a href="/kosten/nieuwe-badkamer/">kosten nieuwe badkamer</a>. Of reken het meteen uit met de <a href="/tools/badkamercalculator/">badkamercalculator</a>.</p>
  <h3>Let op bij oudere woningen</h3>
  <p>In woningen die voor 1994 zijn gebouwd kan asbest zitten, bijvoorbeeld in oude kit, plaatmateriaal achter de tegels of vloerzeil ({_bl("asbest", "IPLO")}). Laat dat uitzoeken voordat er gesloopt wordt ({_bl("asbestregels", "Rijksoverheid")}). In woningen van voor 1960 kunnen nog loden waterleidingen liggen ({_bl("lood", "Rijksoverheid")}). Bij een renovatie is dat een goed moment om ze te laten vervangen. Lees meer over <a href="/kennisbank/asbest-in-badkamer/">asbest in de badkamer</a>.</p>
  <h3>Bronnen</h3>
  <ol class="bkc-bronnen">{"".join(f'<li><a href="{u}" rel="noopener" target="_blank">{t}</a></li>' for t, u in BRONNEN.values())}</ol>
</div></section>"""

    faqs = [
        ("Hoe lang gaat een badkamer mee?",
         "Dat verschilt sterk. Het hangt af van de kwaliteit van het werk, de waterdichting onder de tegels, de ventilatie en het onderhoud. Kijk daarom niet alleen naar de leeftijd, maar vooral naar signalen zoals holle tegels, lekkage en schimmel die terugkomt."),
        ("Is schimmel in de badkamer een reden om te renoveren?",
         "Niet altijd. Vaak is schimmel op te lossen met betere ventilatie en nieuwe kit. Komt de schimmel steeds terug op het plafond of de muren, dan zit er waarschijnlijk te veel vocht. Laat dan eerst de ventilatie nakijken."),
        ("Wat doe ik bij een vlek op het plafond onder de badkamer?",
         "Laat zo snel mogelijk de oorzaak zoeken. Het kan een lekkende leiding zijn, maar ook water dat door de voegen of kit van de douchevloer gaat. Hoe langer het lekt, hoe groter de schade aan de vloer en het plafond."),
        ("Kan ik een inloopdouche laten maken zonder de hele badkamer te slopen?",
         "Vaak wel, op de plek van het oude bad of de douchebak. Of dat kan, hangt af van de hoogte van de vloer en de plek van de afvoer. Een specialist kan dat bij de opname zien."),
        ("Worden mijn antwoorden opgeslagen?",
         "Nee. De check werkt helemaal in je browser. Er gaat niets naar een server, en er wordt niets bewaard."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Veelgestelde vragen over de badkamercheck")

    app_ld = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Badkamercheck",
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "Alle browsers",
        "inLanguage": "nl-NL",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
        "description": "Elf korte vragen over je badkamer, met een score en het advies onderhoud, gedeeltelijke of complete renovatie.",
    }

    data = {"punten": PUNTEN, "max": MAX_PUNTEN}
    data_tag = ('<script type="application/json" id="bkc-data">'
                + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + "</script>")

    body = (hero + uitleg + faq_html
            + cta_blok("Wil je weten wat het bij jou kost?", "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit je regio. Zij kijken ter plekke naar je badkamer.", "Vraag offertes aan")
            + PAGE_CSS + data_tag + "<script>\n" + LOGICA_JS + PAGE_JS)

    write(PAD, page(
        title("Badkamercheck: is je badkamer aan vervanging toe?"),
        "Doe de gratis badkamercheck: elf korte vragen en je ziet of onderhoud genoeg is, of een gedeeltelijke of complete renovatie. Met tips per onderdeel.",
        PAD, body, [cr_ld, faq_ld, app_ld]), prio=0.7)


PAGE_CSS = """<style>
[data-bkc] [hidden]{display:none!important}
.bkc-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,540px);gap:48px;align-items:start}
[data-bkc].klaar .bkc-grid{grid-template-columns:minmax(0,1fr);max-width:760px;margin:0 auto}
[data-bkc].klaar .bkc-intro{display:none}
@media(max-width:980px){.bkc-grid{grid-template-columns:minmax(0,1fr);gap:20px}.bkc-intro .checklist{display:none}}
.bkc-kaart{min-width:0;border-top:4px solid var(--accent)}
.bkc-top{display:flex;justify-content:space-between;align-items:center;min-height:28px;font-size:.9rem;color:var(--muted)}
.bkc-teller b{color:var(--ink)}
.bkc-balk{height:5px;border-radius:99px;background:var(--line);margin:8px 0 20px;overflow:hidden}
.bkc-balk i{display:block;height:100%;background:var(--accent);border-radius:99px;transition:width .3s ease}
.bkc-q{border:0;margin:0;padding:0;min-width:0}
.bkc-vraag{font-size:1.25rem;font-weight:750;color:var(--ink);line-height:1.25;padding:0;margin:0 0 6px}
.bkc-hint{font-size:.93rem;color:var(--muted);margin:0 0 16px}
.bkc-opts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
@media(max-width:480px){.bkc-opts{grid-template-columns:minmax(0,1fr)}}
.bkc-opt{display:flex;flex-direction:column;justify-content:center;text-align:left;font:inherit;color:var(--ink);background:#fff;border:1.5px solid var(--line);border-left-width:5px;border-radius:var(--radius);padding:12px 14px;cursor:pointer;min-height:64px;transition:border-color .15s,background .15s}
.bkc-opt:hover{border-color:var(--navy);background:var(--bg-soft)}
.bkc-opt:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.bkc-opt.gekozen{border-color:var(--accent);background:var(--accent-soft)}
.bkc-t-g{border-left-color:#0f8a5f}.bkc-t-o{border-left-color:#e2a80c}.bkc-t-r{border-left-color:#c0392b}.bkc-t-n{border-left-color:var(--line)}
.bkc-lbl{font-weight:700;line-height:1.25}
.bkc-sub{font-size:.84rem;color:var(--muted);line-height:1.3;margin-top:2px}
.bkc-kicker{text-transform:uppercase;letter-spacing:.06em;font-size:.78rem;font-weight:750;color:var(--muted);margin:0;text-align:center}
.bkc-score{text-align:center;color:var(--ink);margin:2px 0 8px}
.bkc-getal{font-size:3rem;font-weight:800;line-height:1}
.bkc-van{font-size:1.1rem;color:var(--muted);margin-left:2px}
.bkc-meter{position:relative;display:grid;grid-template-columns:20fr 25fr 55fr;gap:3px;height:12px;max-width:440px;margin:0 auto}
.bkc-meter i{display:block;border-radius:99px}
.bkc-z1{background:#0f8a5f}.bkc-z2{background:#e2a80c}.bkc-z3{background:#c0392b}
.bkc-pijl{position:absolute;top:-6px;left:0;width:4px;height:24px;margin-left:-2px;border-radius:2px;background:var(--ink);transition:left .9s ease}
.bkc-meter-lbl{display:grid;grid-template-columns:20fr 25fr 55fr;max-width:440px;margin:6px auto 18px;font-size:.78rem;color:var(--muted)}
.bkc-meter-lbl span:nth-child(2){text-align:center}.bkc-meter-lbl span:nth-child(3){text-align:right}
.bkc-uitleg-score{text-align:center;margin:-8px 0 14px}
.bkc-advies{text-align:center}
.bkc-titel{margin:0 0 6px;font-size:clamp(1.4rem,3vw,1.9rem)}
.bkc-advies[data-advies=onderhoud] .bkc-titel{color:#0b6e4b}.bkc-advies[data-advies=deel] .bkc-titel{color:#8a6400}.bkc-advies[data-advies=compleet] .bkc-titel{color:#a3301f}
.bkc-advies p{max-width:56ch;margin:0 auto 12px}
.bkc-knoppen{display:flex;flex-wrap:wrap;gap:8px;justify-content:center}
.bkc-punten-blok{border-top:1px solid var(--line);margin-top:18px;padding-top:14px}
.bkc-punten-blok h3{font-size:1.05rem;margin:0 0 10px}
.bkc-punten{margin:0;padding-left:20px}
.bkc-punten li{margin:0 0 10px;font-size:.95rem}
.bkc-klein{font-size:.84rem;color:var(--muted);margin:12px 0 0}
.bkc-opnieuw{text-align:center;margin:14px 0 0}
.bkc-bronnen{font-size:.88rem}
.bkc-bronnen li{margin:4px 0;overflow-wrap:anywhere}
@media(max-width:480px){.bkc-kaart{padding:20px 16px}.bkc-vraag{font-size:1.12rem}.bkc-knoppen .btn{flex:1 1 100%}}
@media(prefers-reduced-motion:reduce){.bkc-pijl,.bkc-balk i{transition:none}}
</style>"""

PAGE_JS = r"""
(function () {
  "use strict";
  var root = document.querySelector("[data-bkc]");
  if (!root) return;
  var DATA = JSON.parse(document.getElementById("bkc-data").textContent);
  var vragen = [].slice.call(root.querySelectorAll(".bkc-q"));
  var quiz = root.querySelector(".bkc-quiz"), uitslag = root.querySelector(".bkc-uitslag");
  var teller = root.querySelector(".bkc-teller b"), balk = root.querySelector(".bkc-balk i");
  var terug = root.querySelector(".bkc-terug"), kaart = root.querySelector(".bkc-kaart");
  var ans = {}, idx = 0;

  function toon(i) {
    idx = i;
    vragen.forEach(function (q, n) { q.hidden = n !== i; });
    teller.textContent = i + 1;
    balk.style.width = ((i + 1) / vragen.length * 100) + "%";
    terug.hidden = i === 0;
    var k = vragen[i].dataset.key;
    [].forEach.call(vragen[i].querySelectorAll(".bkc-opt"), function (b) {
      var aan = ans[k] === b.dataset.v;
      b.classList.toggle("gekozen", aan);
      b.setAttribute("aria-pressed", aan ? "true" : "false");
    });
  }
  function naarBoven(el) {
    var top = el.getBoundingClientRect().top + window.scrollY - 90;
    if (Math.abs(window.scrollY - top) > 60) window.scrollTo({ top: top, behavior: "smooth" });
  }

  vragen.forEach(function (q, n) {
    q.addEventListener("click", function (e) {
      var b = e.target.closest(".bkc-opt");
      if (!b) return;
      ans[q.dataset.key] = b.dataset.v;
      [].forEach.call(q.querySelectorAll(".bkc-opt"), function (x) { x.classList.toggle("gekozen", x === b); });
      setTimeout(function () {
        if (n < vragen.length - 1) {
          toon(n + 1);
          var f = vragen[n + 1].querySelector(".bkc-opt");
          if (f && document.activeElement && document.activeElement.classList.contains("bkc-opt")) f.focus({ preventScroll: true });
        } else {
          toonUitslag();
        }
      }, 160);
    });
  });
  terug.addEventListener("click", function () { if (idx > 0) toon(idx - 1); });

  function toonUitslag() {
    var r = bkcAdvies(ans, DATA.punten, DATA.max);
    root.querySelector(".bkc-getal").textContent = r.score;
    [].forEach.call(root.querySelectorAll(".bkc-advies"), function (a) { a.hidden = a.dataset.advies !== r.advies; });
    var zichtbaar = 0;
    [].forEach.call(root.querySelectorAll("[data-punt]"), function (li) {
      var d = li.dataset.punt.split("=");
      li.hidden = ans[d[0]] !== d[1];
      if (!li.hidden) zichtbaar++;
    });
    root.querySelector(".bkc-geen").hidden = zichtbaar > 0;
    quiz.hidden = true;
    uitslag.hidden = false;
    root.classList.add("klaar");
    var pijl = root.querySelector(".bkc-pijl");
    pijl.style.left = "0%";
    setTimeout(function () { pijl.style.left = Math.max(1, Math.min(99, r.positie)) + "%"; }, 200);
    naarBoven(kaart);
    var titel = root.querySelector('.bkc-advies[data-advies="' + r.advies + '"] .bkc-titel');
    titel.setAttribute("tabindex", "-1");
    titel.focus({ preventScroll: true });
  }

  root.querySelector(".bkc-reset").addEventListener("click", function () {
    ans = {};
    uitslag.hidden = true; quiz.hidden = false; root.classList.remove("klaar");
    toon(0);
    naarBoven(kaart);
  });

  toon(0);
})();
</script>"""
