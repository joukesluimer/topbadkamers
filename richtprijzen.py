# -*- coding: utf-8 -*-
"""Richtprijzen voor badkamerwerk: één bron voor de calculator, de offertechecker en de kostenpagina's.

Elke post heeft:
- laag, hoog: de bandbreedte in euro;
- eenheid: "post" (per badkamer of per klus), "m2", "m" (strekkende meter), "uur", "stuk" of "bezoek";
- btw: "incl" (inclusief 21% btw) of "excl" (exclusief btw);
- bron: sleutels uit BRONNEN hieronder; "eigen" betekent een eigen inschatting op basis van de andere bronnen;
- toelichting: wat er wel en niet in zit.
Sommige posten hebben ook "niveaus" (basis, midden, luxe) voor de calculator.

Gebruik:
- badkamer_calculator.REKENWAARDEN wordt hieruit opgebouwd;
- badkamer_offertecheck.BANDEN wordt hieruit opgebouwd (de JavaScript-parser krijgt die banden mee);
- badkamer_kosten haalt de gedeelde bedragen (headlines, varianten, rekenvoorbeelden) hieruit.

data.DIENSTEN (prijs_van, prijs_tot) is de referentie voor de dienstpagina's. Deze module wijzigt
data.py niet; met verschillen_met_diensten() zie je of de twee nog gelijk lopen.

Bronnen geraadpleegd in november 2026. Btw op badkamerwerk is 21%; het 9%-tarief geldt niet
voor tegelwerk, loodgieterswerk of het plaatsen van sanitair.
"""

BRONNEN = {
    "homedeal_lood": ("Homedeal, loodgieter kosten", "https://www.homedeal.nl/loodgieter/loodgieter-kosten/"),
    "trustoo_lood": ("Trustoo, uurtarief loodgieter", "https://trustoo.nl/kosten/loodgieter-kosten/"),
    "knab_lood": ("Knab, uurtarief loodgieter zzp 2026", "https://bieb.knab.nl/ondernemen/wat-verdient-een-loodgieter-zzp-bekijk-uurtarief-en-winst"),
    "trustoo_badkamer": ("Trustoo, wat kost een nieuwe badkamer", "https://trustoo.nl/kosten/badkamer-renovatie-kosten/"),
    "slimster_badkamer": ("Slimster, compleet nieuwe badkamer kosten", "https://slimster.nl/badkamer/compleet-nieuwe-badkamer-kosten/"),
    "homedeal_badkamer": ("Homedeal, badkamer renoveren kosten", "https://www.homedeal.nl/badkamerspecialist/badkamer-renoveren-kosten/"),
    "werkspot_tegel": ("Werkspot, badkamer betegelen prijzen", "https://www.werkspot.nl/badkamer-betegelen/prijzen-kosten"),
    "trustoo_tegel": ("Trustoo, kosten tegelzetter", "https://trustoo.nl/kosten/tegelzetter-kosten/"),
    "homedeal_tegel": ("Homedeal, kosten tegelzetter", "https://www.homedeal.nl/tegels-zetten/kosten-tegelzetter"),
    "werkspot_kit": ("Werkspot, kitwerk badkamer prijzen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kitwerk"),
    "slimster_kit": ("Slimster, badkamer kitten kosten", "https://slimster.nl/kitwerk/kosten-kitter/badkamer-kitten/"),
    "slimster_slopen": ("Slimster, badkamer slopen kosten", "https://slimster.nl/sloopwerk/sloopkosten/badkamer-slopen-kosten/"),
    "werkspot_slopen": ("Werkspot, kosten badkamer slopen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/kosten-badkamer-slopen"),
    "werkspot_puin": ("Werkspot, puin afvoeren prijzen", "https://www.werkspot.nl/puin-afvoeren/prijzen-kosten"),
    "slimster_afval": ("Slimster, bouwafval afvoeren", "https://slimster.nl/blog/bouwafval-afvoeren/"),
    "werkspot_vv": ("Werkspot, vloerverwarming badkamer prijzen", "https://www.werkspot.nl/verwarming/prijzen-kosten/vloerverwarming-badkamer"),
    "slimster_vv": ("Slimster, vloerverwarming kosten", "https://slimster.nl/vloerverwarming/kosten/"),
    "homedeal_vv": ("Homedeal, vloerverwarming badkamer kosten", "https://www.homedeal.nl/vloerverwarming/vloerverwarming-badkamer-kosten/"),
    "werkspot_sanitair": ("Werkspot, sanitair plaatsen prijzen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/sanitair-plaatsen"),
    "werkspot_bad": ("Werkspot, bad plaatsen prijzen", "https://www.werkspot.nl/badkamer-sanitair/prijzen-kosten/bad-plaatsen"),
    "homedeal_bad": ("Homedeal, bad plaatsen kosten", "https://www.homedeal.nl/badkamerspecialist/bad-plaatsen-kosten/"),
    "homedeal_douche": ("Homedeal, nieuwe douche kosten", "https://www.homedeal.nl/badkamerspecialist/nieuwe-douche-kosten/"),
    "homedeal_toilet": ("Homedeal, toilet verbouwen kosten", "https://www.homedeal.nl/verbouwing/toilet-verbouwen-kosten/"),
    "werkspot_toilet": ("Werkspot, toiletruimte verbouwen prijzen", "https://www.werkspot.nl/toiletruimte-verbouwen/prijzen-kosten"),
    "werkspot_stopcontact": ("Werkspot, stopcontact plaatsen prijzen", "https://www.werkspot.nl/stopcontact-plaatsen/prijzen-kosten"),
    "eigen": ("Eigen inschatting op basis van de andere bronnen", ""),
}

RICHTPRIJZEN = {
    # ------------------------------------------------------------------ uurtarief
    "uurtarief": {
        # Homedeal €45 – €85 excl. btw; Werkspot €45 – €80; Knab gemiddeld €57 (zzp, excl. btw).
        "laag": 45, "hoog": 85, "eenheid": "uur", "btw": "excl",
        "bron": ["homedeal_lood", "knab_lood"],
        "toelichting": "Uurtarief van een loodgieter of installateur op een werkdag, zonder voorrijkosten.",
    },
    "voorrijkosten": {
        # Trustoo gemiddeld €20 – €40; Homedeal tot ca. €50.
        "laag": 20, "hoog": 50, "eenheid": "bezoek", "btw": "excl",
        "bron": ["trustoo_lood", "homedeal_lood"],
        "toelichting": "Per bezoek. Vervalt soms bij een grotere klus.",
    },
    # ------------------------------------------------------------------ sloop en afval
    "sloop": {
        # Slimster gemiddeld €550, €250 – €850; Werkspot €265 – €685 (klein tot groot).
        "laag": 250, "hoog": 850, "eenheid": "post", "btw": "incl",
        "bron": ["slimster_slopen", "werkspot_slopen"],
        "toelichting": "Alleen slopen: sanitair en tegels eruit, zonder afvoer van het afval en zonder dekvloer.",
    },
    "sloop_vast": {
        # Rekenmodel van de calculator: vast deel + per m² vloer. 5 – 8 m² komt uit op €300 – €1.000,
        # dat sluit aan op "sloop" hierboven.
        "laag": 100, "hoog": 200, "eenheid": "post", "btw": "incl",
        "bron": ["eigen", "slimster_slopen", "werkspot_slopen"],
        "toelichting": "Vast deel van het sloopwerk: sanitair demonteren en leidingen afdoppen.",
    },
    "sloop_m2": {
        # Slimster: vloer verwijderen €19 – €40 per m²; hier inclusief het deel wandtegels per m² vloer.
        "laag": 40, "hoog": 100, "eenheid": "m2", "btw": "incl",
        "bron": ["eigen", "slimster_slopen"],
        "toelichting": "Sloopwerk per m² vloer, inclusief de wandtegels die daarbij horen.",
    },
    "sloop_compleet": {
        # Trustoo: sloopwerk en afvoer €1.200 – €1.800.
        "laag": 1200, "hoog": 1800, "eenheid": "post", "btw": "incl",
        "bron": ["trustoo_badkamer"],
        "toelichting": "Slopen tot op de ruwe vloer, inclusief dekvloer en afvoer van al het afval.",
    },
    "afval": {
        # Werkspot: container 3 m³ €125 – €165, 6 m³ €180 – €220; Slimster: 6 m³ bouwafval ca. €350 all-in;
        # Trustoo: afvoer bouw- en sloopafval €35 – €400.
        "laag": 150, "hoog": 450, "eenheid": "post", "btw": "incl",
        "bron": ["werkspot_puin", "slimster_afval", "trustoo_badkamer"],
        "toelichting": "Afvoer van het sloopafval door het bedrijf, of een container van 3 tot 6 m³ inclusief storten.",
    },
    "container": {
        # Werkspot: container 3 – 6 m³ €125 – €220.
        "laag": 125, "hoog": 220, "eenheid": "post", "btw": "incl",
        "bron": ["werkspot_puin"],
        "toelichting": "Alleen een container huren, als je zelf sloopt.",
    },
    # ------------------------------------------------------------------ tegelwerk
    "tegelwerk": {
        # Trustoo en Homedeal: legloon gemiddeld €25 – €40 per m²; bovengrens €55 voor kleine badkamers en
        # grote formaten. Gelijk aan data.DIENSTEN "tegelwerk-badkamer". (Trustoo noemt in 2026 ook
        # €50 – €70 per m² inclusief lijm, voeg en voorstrijk; zie tegelwerk_hulpmateriaal.)
        "laag": 25, "hoog": 55, "eenheid": "m2", "btw": "incl",
        "bron": ["trustoo_tegel", "homedeal_tegel", "trustoo_badkamer"],
        "toelichting": "Alleen het zetten (legloon), zonder tegels.",
    },
    "tegelwerk_hulpmateriaal": {
        # Lijm, voegsel, voorstrijk en kit per m². Eigen inschatting; met het legloon komt dat op €35 – €65,
        # wat aansluit op Trustoo (€50 – €70 per m² inclusief lijm en voeg).
        "laag": 10, "hoog": 10, "eenheid": "m2", "btw": "incl",
        "bron": ["eigen", "trustoo_badkamer"],
        "toelichting": "Lijm, voegsel en kit bovenop het legloon.",
    },
    "tegels": {
        # Werkspot: tegels €20 – €60 per m². Slimster: budget €20 – €40, midden €40 – €70, luxe €70 – €150.
        "laag": 20, "hoog": 60, "eenheid": "m2", "btw": "incl",
        "bron": ["werkspot_tegel", "slimster_badkamer"],
        "toelichting": "De tegels zelf (materiaal). Natuursteen en groot formaat kunnen duurder zijn.",
        "niveaus": {"basis": [20, 30], "midden": [30, 50], "luxe": [50, 90]},
    },
    "waterdicht": {
        # Eigen inschatting: waterdichte laag met kimband in de douche- of badhoek plus het afschot.
        "laag": 300, "hoog": 700, "eenheid": "post", "btw": "incl",
        "bron": ["eigen", "werkspot_tegel"],
        "toelichting": "Waterdicht maken van de douche- of badhoek, met kimband en afschot naar de afvoer.",
    },
    "kitwerk": {
        # Werkspot en Slimster: €6 – €11 per meter. Gelijk aan data.DIENSTEN "badkamer-onderhoud".
        "laag": 6, "hoog": 11, "eenheid": "m", "btw": "incl",
        "bron": ["werkspot_kit", "slimster_kit"],
        "toelichting": "Oude kit verwijderen en nieuwe sanitairkit aanbrengen.",
    },
    "kitwerk_badkamer": {
        # Werkspot en Slimster: hele badkamer afkitten €95 – €325.
        "laag": 95, "hoog": 325, "eenheid": "post", "btw": "incl",
        "bron": ["werkspot_kit", "slimster_kit"],
        "toelichting": "Hele badkamer opnieuw afkitten.",
    },
    # ------------------------------------------------------------------ installatie
    "leidingwerk": {
        # Trustoo: leidingwerk water en afvoer €1.250 – €2.200; Slimster: op dezelfde plek €1.500 – €3.000.
        "laag": 1250, "hoog": 3000, "eenheid": "post", "btw": "incl",
        "bron": ["trustoo_badkamer", "slimster_badkamer"],
        "toelichting": "Water- en afvoerleidingen vernieuwen, met de aansluitpunten op dezelfde plek.",
    },
    "leidingwerk_verplaatsen": {
        # Homedeal: leidingen verplaatsen gemiddeld €700 – €1.500 extra (per toilet of toestel);
        # Slimster: verplaatsen in een hele badkamer vanaf ca. €5.000 in totaal. Eigen inschatting.
        "laag": 1000, "hoog": 2500, "eenheid": "post", "btw": "incl",
        "bron": ["eigen", "homedeal_toilet", "slimster_badkamer"],
        "toelichting": "Extra bovenop het leidingwerk als toilet, douche of afvoer naar een andere plek gaan.",
    },
    "leidingwerk_toilet_verplaatsen": {
        # Homedeal en Werkspot: toilet of afvoer verplaatsen €700 – €1.500 extra.
        "laag": 700, "hoog": 1500, "eenheid": "post", "btw": "incl",
        "bron": ["homedeal_toilet", "werkspot_toilet"],
        "toelichting": "Afvoer en waterleiding van één toilet verleggen, zonder het tegelwerk.",
    },
    "montage_douche": {
        # Trustoo: douchecabine plaatsen €275 – €435, verlaagde douchebak €300 – €550; Werkspot: douche
        # plaatsen €600 – €1.900 inclusief product.
        "laag": 400, "hoog": 800, "eenheid": "stuk", "btw": "incl",
        "bron": ["trustoo_badkamer", "werkspot_sanitair"],
        "toelichting": "Douche, douchewand of cabine plaatsen en aansluiten.",
    },
    "montage_bad": {
        # Werkspot: bad aansluiten en plaatsen €300 – €1.000 (plus afwerking €200 – €500).
        "laag": 300, "hoog": 1000, "eenheid": "stuk", "btw": "incl",
        "bron": ["werkspot_bad"],
        "toelichting": "Bad plaatsen en aansluiten, zonder ombouw en tegelwerk.",
    },
    "montage_toilet": {
        # Homedeal en Werkspot: toilet vervangen €300 – €700 aan werk; Homedeal: loodgieter €150 – €250 voor
        # een eenvoudig staand toilet.
        "laag": 300, "hoog": 700, "eenheid": "stuk", "btw": "incl",
        "bron": ["homedeal_toilet", "werkspot_toilet"],
        "toelichting": "Toilet plaatsen en aansluiten op dezelfde plek.",
    },
    "montage_meubel": {
        # Werkspot: vrijstaand meubel €200 – €500, hangend €250 – €600 plaatsen.
        "laag": 200, "hoog": 600, "eenheid": "stuk", "btw": "incl",
        "bron": ["werkspot_sanitair"],
        "toelichting": "Wastafelmeubel ophangen en aansluiten, met sifon en kraan.",
    },
    "sanitair": {
        # Homedeal: totaal sanitair €1.000 – €6.000; Trustoo per onderdeel: toilet €150 – €1.500,
        # douche €400 – €6.000, wastafelmeubel €200 – €3.000, kranen €50 – €900.
        "laag": 1500, "hoog": 9500, "eenheid": "post", "btw": "incl",
        "bron": ["trustoo_badkamer", "homedeal_badkamer"],
        "toelichting": "Levering van douche, toilet, wastafelmeubel en kranen, van basis tot luxe.",
    },
    # Sanitair per onderdeel (alleen het product), per niveau. Trustoo (budget – luxe) en Homedeal/Slimster.
    "sanitair_douche": {"laag": 500, "hoog": 4000, "eenheid": "stuk", "btw": "incl", "bron": ["trustoo_badkamer", "homedeal_douche"],
                        "toelichting": "Douche: bak of goot, wand en kraan.",
                        "niveaus": {"basis": [500, 900], "midden": [1000, 2200], "luxe": [2200, 4000]}},
    "sanitair_bad": {"laag": 300, "hoog": 3000, "eenheid": "stuk", "btw": "incl", "bron": ["trustoo_badkamer", "homedeal_bad"],
                     "toelichting": "Ligbad met badkraan.",
                     "niveaus": {"basis": [300, 600], "midden": [600, 1300], "luxe": [1300, 3000]}},
    "sanitair_toilet": {"laag": 300, "hoog": 1800, "eenheid": "stuk", "btw": "incl", "bron": ["trustoo_badkamer", "homedeal_toilet"],
                        "toelichting": "Toilet, bij midden en luxe een hangtoilet met inbouwreservoir.",
                        "niveaus": {"basis": [300, 500], "midden": [500, 900], "luxe": [900, 1800]}},
    "sanitair_meubel": {"laag": 250, "hoog": 2500, "eenheid": "stuk", "btw": "incl", "bron": ["trustoo_badkamer"],
                        "toelichting": "Wastafelmeubel met wastafel, kraan en spiegel.",
                        "niveaus": {"basis": [250, 500], "midden": [500, 1100], "luxe": [1100, 2500]}},
    # ------------------------------------------------------------------ elektra en verwarming
    "elektra": {
        # Trustoo: elektra aanpassen €300 – €1.000; Slimster: stopcontacten en schakelaars €500 – €1.500.
        # (Slimster noemt uitgebreide verlichting apart: €300 – €1.500.)
        "laag": 300, "hoog": 1500, "eenheid": "post", "btw": "incl",
        "bron": ["trustoo_badkamer", "slimster_badkamer", "werkspot_stopcontact"],
        "toelichting": "Stopcontacten, schakelaars, een aparte groep en eenvoudige spots. Uitgebreide verlichting kan erbij komen.",
    },
    "ventilator": {
        # Indicatie op basis van Werkspot en bouwmarktprijzen, brede marge.
        "laag": 150, "hoog": 400, "eenheid": "stuk", "btw": "incl",
        "bron": ["eigen", "werkspot_stopcontact"],
        "toelichting": "Badkamerventilator met montage en aansluiting.",
    },
    "vloerverwarming_m2": {
        # Werkspot: €40 – €110 per m²; Slimster: elektrische matten €60 – €80 per m² incl. montage;
        # Homedeal: €75 – €85 per m².
        "laag": 60, "hoog": 110, "eenheid": "m2", "btw": "incl",
        "bron": ["werkspot_vv", "slimster_vv", "homedeal_vv"],
        "toelichting": "Elektrische vloerverwarming per m², inclusief installatie.",
    },
    "vloerverwarming_elektrisch": {
        # Trustoo: elektrische vloerverwarming €600 – €1.100 per badkamer; Werkspot: €600 – €1.000 voor 6 – 10 m².
        "laag": 600, "hoog": 1100, "eenheid": "post", "btw": "incl",
        "bron": ["trustoo_badkamer", "werkspot_vv"],
        "toelichting": "Elektrische vloerverwarming in een gewone badkamer, met thermostaat en aansluiting.",
    },
    "vloerverwarming": {
        # Slimster: vloerverwarming €500 – €2.500 (elektrisch of aangesloten op de cv).
        "laag": 500, "hoog": 2500, "eenheid": "post", "btw": "incl",
        "bron": ["slimster_badkamer", "trustoo_badkamer"],
        "toelichting": "Vloerverwarming in de hele badkamer, elektrisch of aangesloten op de cv of warmtepomp.",
    },
}

EENHEID_TEKST = {"post": "per badkamer", "m2": "per m²", "m": "per meter", "uur": "per uur",
                 "stuk": "per stuk", "bezoek": "per bezoek"}


def lh(sleutel, factor=1):
    """[laag, hoog] van een post, eventueel maal een aantal (m², meters)."""
    p = RICHTPRIJZEN[sleutel]
    return [round(p["laag"] * factor, 2), round(p["hoog"] * factor, 2)]


def niveaus(sleutel):
    """Kopie van de niveaus (basis, midden, luxe) van een post."""
    return {k: list(v) for k, v in RICHTPRIJZEN[sleutel]["niveaus"].items()}


def bron_links(sleutel):
    """Lijst (naam, url) van de bronnen van een post, zonder de eigen inschatting."""
    return [BRONNEN[b] for b in RICHTPRIJZEN[sleutel]["bron"] if b != "eigen"]


def verschillen_met_diensten():
    """Vergelijkt de gedeelde posten met data.DIENSTEN en geeft de verschillen terug (leeg = gelijk)."""
    from data import DIENST_BY_SLUG
    paren = {"tegelwerk": "tegelwerk-badkamer", "kitwerk": "badkamer-onderhoud", "uurtarief": "badkamer-installeren"}
    uit = []
    for post, slug in paren.items():
        d = DIENST_BY_SLUG[slug]
        if (d["prijs_van"], d["prijs_tot"]) != (RICHTPRIJZEN[post]["laag"], RICHTPRIJZEN[post]["hoog"]):
            uit.append((post, slug, (d["prijs_van"], d["prijs_tot"]), (RICHTPRIJZEN[post]["laag"], RICHTPRIJZEN[post]["hoog"])))
    return uit


if __name__ == "__main__":
    for k, p in RICHTPRIJZEN.items():
        print(f"{k:32} {p['laag']:>6} – {p['hoog']:<6} {EENHEID_TEKST[p['eenheid']]:13} {p['btw']}")
    print("verschillen met data.DIENSTEN:", verschillen_met_diensten() or "geen")
