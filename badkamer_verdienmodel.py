# -*- coding: utf-8 -*-
"""
Pagina "Hoe verdienen wij geld": /hoe-verdienen-wij-geld/

Korte, eerlijke uitleg van het verdienmodel. Spreekt de privacyverklaring (/privacy/)
en de algemene voorwaarden (/voorwaarden/) in build.py niet tegen:
- aanvragen gaan naar maximaal drie bedrijven, die per aanvraag een vergoeding betalen
  volgens schriftelijk afgesproken tarieven;
- de aanvrager betaalt niets;
- contactgegevens en omschrijving gaan niet naar andere partijen.
Bewust geen bedragen voor de vergoeding: die zijn per bedrijf afgesproken.

Interface voor build.py: LINKS en build(write).
"""

from components import page, crumbs, faq_blok, cta_blok, title
from data import SITE

PAD = "/hoe-verdienen-wij-geld/"

LINKS = [
    (PAD, "Hoe verdienen wij geld?",
     "Gratis voor jou: badkamerspecialisten betalen ons een vaste vergoeding per aanvraag. Geen winkel, geen affiliatelinks."),
]


def build(write):
    naam = SITE["naam"]
    cr, cr_ld = crumbs([("Home", "/"), ("Hoe verdienen wij geld?", None)])

    body = f"""{cr}
<section class="section-sm"><div class="wrap narrow prose">
  <h1>Hoe verdienen wij geld?</h1>
  <p class="lead">{naam} is gratis voor jou. Ons geld komt van de badkamerspecialisten die via ons een aanvraag krijgen. Hieronder staat precies hoe dat werkt.</p>

  <h2>Wat wij doen</h2>
  <p>Wij brengen je in contact met maximaal drie badkamerspecialisten uit je regio. Je vult één keer een aanvraag in, en zij nemen contact met je op voor een offerte. Wij voeren zelf geen werk uit en zijn geen partij bij de afspraak die je daarna met een specialist maakt (zie onze <a href="/voorwaarden/">algemene voorwaarden</a>).</p>

  <h2>Wie betaalt</h2>
  <ul>
    <li><strong>Jij betaalt niets.</strong> Een aanvraag is gratis en vrijblijvend. Je hoeft geen offerte aan te nemen.</li>
    <li><strong>De specialist betaalt.</strong> Een badkamerspecialist die je aanvraag krijgt, betaalt ons een vaste vergoeding per aanvraag. Die vergoeding hangt niet af van welke offerte je kiest, en ook niet van de prijs.</li>
  </ul>

  <h2>Wat wij niet doen</h2>
  <ul>
    <li>Wij zijn geen winkel en verkopen geen badkamerspullen.</li>
    <li>Wij gebruiken geen affiliatelinks. Op onze pagina’s staan geen links waar wij aan verdienen als je iets koopt.</li>
    <li>Niemand kan betalen voor een plek of een betere uitslag in de <a href="/tools/offertechecker/">offertevergelijker</a>.</li>
    <li>Wij verkopen je gegevens niet. Je aanvraag gaat alleen naar de maximaal drie specialisten die hem ontvangen, en niet naar andere partijen. Lees hoe we met je gegevens omgaan in de <a href="/privacy/">privacyverklaring</a>.</li>
  </ul>

  <h2>Hoe de offertevergelijker werkt</h2>
  <p>De <a href="/tools/offertechecker/">offertevergelijker</a> leest je offerte in je eigen browser. Er gaat niets naar een server en wij zien je offerte niet. De uitslag is voor iedereen hetzelfde, of je daarna een aanvraag doet of niet.</p>
  <p>Onder de uitslag staat een apart blok voor een tegenofferte. Kies je daarvoor, dan zie je eerst welke posten we zouden doorsturen, zonder je naam, adres, telefoonnummer en de naam van je huidige aanbieder. Die tekst kun je zelf aanpassen. Pas als je het aanvraagformulier verstuurt, gaat je aanvraag naar maximaal drie specialisten. Voor die aanvraag krijgen wij dan een vergoeding van de specialist.</p>

  <h2>Wie zijn wij</h2>
  <p>{naam} is gevestigd in {SITE['adres']} en ingeschreven bij de KvK onder nummer {SITE['kvk']}. Vragen over hoe wij werken? Mail naar <a href="mailto:{SITE['email']}">{SITE['email']}</a>. Ben je zelf badkamerspecialist? Lees dan <a href="/voor-badkamerspecialisten/">hoe aansluiten werkt</a>.</p>
</div></section>"""

    faqs = [
        ("Kost een aanvraag mij echt niets?",
         "Nee. Je betaalt niets aan ons, ook niet als je een offerte aanneemt. De specialist betaalt ons een vaste vergoeding per aanvraag."),
        ("Beïnvloedt de vergoeding de offertevergelijker?",
         "Nee. De vergelijker legt je offerte naast marktbanden en richtprijzen. Wie er betaalt, speelt daarin geen rol, en niemand kan een plek of een betere uitslag kopen."),
        ("Aan wie gaan mijn gegevens?",
         "Alleen aan de maximaal drie badkamerspecialisten die je aanvraag ontvangen. We verkopen je gegevens niet aan anderen en gebruiken ze niet voor ongevraagde reclame."),
        ("Krijgen jullie geld van winkels of merken?",
         "Nee. We hebben geen winkel, geen affiliatelinks en geen betaalde samenwerkingen met merken."),
    ]
    faq_html, faq_ld = faq_blok(faqs, "Vragen over ons verdienmodel")

    body += faq_html + cta_blok(
        "Offertes vergelijken?",
        "Vraag gratis en vrijblijvend offertes aan bij maximaal drie badkamerspecialisten uit je regio.",
        "Vraag offertes aan")

    write(PAD, page(
        title("Hoe verdienen wij geld?"),
        f"{naam} is gratis voor jou. Badkamerspecialisten betalen een vaste vergoeding per aanvraag. Geen winkel, geen affiliatelinks en geen verkoop van je gegevens.",
        PAD, body, [cr_ld, faq_ld]), prio=0.4)
