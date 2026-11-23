"""Productdata kranen en douche voor de offertevergelijker (Top Badkamers).

Categorieen: thermostaatkraan, douchesysteem, handdouche_set, wastafelkraan, badkraan,
inbouwkraan, douchegoot, douchewand, douchecabine, douchebak.

Methode
-------
* Peildatum: november 2026 (opgehaald op 23-11-2026).
* Bron: de prijsvergelijker Beslist.nl. Per artikel is de vergelijkingspagina gelezen
  (URL bevat de EAN). `van` is de laagste en `tot` de hoogste actuele productprijs
  van alle aanbieders op die pagina, inclusief 21% btw en exclusief verzendkosten.
  Alleen artikelen met minstens 3 aanbieders zijn opgenomen. Bedragen zijn afgerond:
  `van` naar beneden en `tot` naar boven op hele euro's.
* Ruwe uitschieters (een marktplaats die ver boven de rest zit) zijn NIET weggelaten.
  De band is daardoor soms breed. Dat is bewust ruim: de pagina meldt "boven de band"
  pas vanaf meer dan 25% boven `tot`.
* EAN: alleen zoals letterlijk op de vergelijkingspagina (en in de URL) vermeld.
  Artikelnummers (`codes`) staan er alleen in als ze letterlijk in de producttitel of
  specificaties stonden. Beslist toont bij de meeste artikelen geen fabrikantnummer;
  daar is `codes` dus leeg. Niets is aangevuld uit het geheugen.
* Serie-artikelen (lege `ean`, meestal lege `codes`) komen uit een overzichtspagina
  met meerdere aanbieders. De band is dan de spreiding van de getoonde prijzen over
  de maten/uitvoeringen van die serie. Gebruik ze als "serie"-match, niet als exact.
* Webwinkelprijzen zijn geen installateursprijzen; zie de toelichting op de pagina.

Niet gevonden met minstens 3 aanbieders (dus niet opgenomen): Radaway, Hansgrohe
iBox-afbouwdelen per stuk, de meeste losse Easy Drain- en I-Drain-maten (2 aanbieders).
"""

ARTIKELEN = [
    # ---- thermostaatkraan ----
    # Beslist 10 aanbieders, EUR 126.74-251.23
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Thermostaatkraan, douchemengkraan chroom",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176612022"],
     "van": 126, "tot": 252, "bron": "bsl_4005176612022"},
    # Beslist 10 aanbieders, EUR 112.70-227.76
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Thermostaatkraan, douchekraan EcoButton",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176310096"],
     "van": 112, "tot": 228, "bron": "bsl_4005176310096"},
    # Beslist 8 aanbieders, EUR 118.41-164.90
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Thermostaatkraan, douchekraan EcoJoy volumegreep",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176310089"],
     "van": 118, "tot": 165, "bron": "bsl_4005176310089"},
    # Beslist 5 aanbieders, EUR 113.80-207.95
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Thermostaatkraan, douchekraan 34767000",
     "categorie": "thermostaatkraan", "codes": ["34767000"], "ean": ["4005176612046"],
     "van": 113, "tot": 208, "bron": "bsl_4005176612046"},
    # Beslist 6 aanbieders, EUR 143.95-271.61
    {"merk": "Grohe", "serie": "Grohtherm 1000", "oms": "Thermostaatkraan, douchethermostaat CoolTouch",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176695728"],
     "van": 143, "tot": 272, "bron": "bsl_4005176695728"},
    # Beslist 5 aanbieders, EUR 160.00-204.84
    {"merk": "Grohe", "serie": "Grohtherm 1000 Performance", "oms": "Thermostaatkraan, douchekraan",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176698651"],
     "van": 160, "tot": 205, "bron": "bsl_4005176698651"},
    # Beslist 5 aanbieders, EUR 172.59-343.99
    {"merk": "Grohe", "serie": "Grohtherm 1000", "oms": "Thermostaatkraan, douchekraan thermostatisch",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176309618"],
     "van": 172, "tot": 344, "bron": "bsl_4005176309618"},
    # Beslist 6 aanbieders, EUR 305.03-413.99
    {"merk": "Grohe", "serie": "Grohtherm 1000 Cosmopolitan", "oms": "Thermostaatkraan, douchekraan supersteel",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4005176374432"],
     "van": 305, "tot": 414, "bron": "bsl_4005176374432"},
    # Beslist 10 aanbieders, EUR 101.80-147.00
    {"merk": "Hansgrohe", "serie": "Ecostat", "oms": "Thermostaatkraan, douchethermostaat opbouw",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4011097799582"],
     "van": 101, "tot": 147, "bron": "bsl_4011097799582"},
    # Beslist 9 aanbieders, EUR 149.72-206.83
    {"merk": "Hansgrohe", "serie": "Ecostat Comfort", "oms": "Thermostaatkraan, douchethermostaat opbouw",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4011097678856"],
     "van": 149, "tot": 207, "bron": "bsl_4011097678856"},
    # Beslist 8 aanbieders, EUR 135.87-215.07
    {"merk": "Hansgrohe", "serie": "Ecostat Element", "oms": "Thermostaatkraan, douchethermostaat",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["4059625522400"],
     "van": 135, "tot": 216, "bron": "bsl_4059625522400"},
    # Beslist 4 aanbieders, EUR 499.00-603.94
    {"merk": "Hotbath", "serie": "Cobber X", "oms": "Thermostaatkraan, thermostatische douchemengkraan opbouw verouderd messing",
     "categorie": "thermostaatkraan", "codes": [], "ean": ["8720847724892"],
     "van": 499, "tot": 604, "bron": "bsl_8720847724892"},
    # Serie: artikelnummer 34558000 letterlijk op Kieskeurig (EUR 114) en in zoekresultaten van twee bouwmarktpagina's (ca. EUR 114 en EUR 149); EAN niet gezien
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Thermostatische douchekraan opbouw, chroom (artikel 34558000)",
     "categorie": "thermostaatkraan", "codes": ["34558000"], "ean": [],
     "van": 114, "tot": 149, "bron": "vgl_kieskeurig_34558000"},
    # ---- douchesysteem ----
    # Beslist 10 aanbieders, EUR 679.00-1021.60
    {"merk": "Grohe", "serie": "Euphoria SmartControl", "oms": "Douchesysteem/regendoucheset opbouw, douchesysteem Duo 310 thermostaat chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4005176457586"],
     "van": 679, "tot": 1022, "bron": "bsl_4005176457586"},
    # Beslist 10 aanbieders, EUR 609.99-815.90
    {"merk": "Grohe", "serie": "Euphoria SmartControl", "oms": "Douchesysteem/regendoucheset opbouw, douchesysteem 260 thermostaat chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4005176457623"],
     "van": 609, "tot": 816, "bron": "bsl_4005176457623"},
    # Beslist 10 aanbieders, EUR 672.10-1010.50
    {"merk": "Grohe", "serie": "Euphoria SmartControl", "oms": "Douchesysteem/regendoucheset opbouw, douchesysteem 310 Cube thermostaat chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4005176457593"],
     "van": 672, "tot": 1011, "bron": "bsl_4005176457593"},
    # Beslist 9 aanbieders, EUR 297.61-365.00
    {"merk": "Hansgrohe", "serie": "Crometta S", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 240 1jet EcoSmart thermostaat",
     "categorie": "douchesysteem", "codes": [], "ean": ["4011097775937"],
     "van": 297, "tot": 365, "bron": "bsl_4011097775937"},
    # Beslist 6 aanbieders, EUR 294.61-395.00
    {"merk": "Hansgrohe", "serie": "Crometta E", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 240 EcoSmart thermostaat",
     "categorie": "douchesysteem", "codes": [], "ean": ["4011097775890"],
     "van": 294, "tot": 395, "bron": "bsl_4011097775890"},
    # Beslist 6 aanbieders, EUR 656.16-750.27
    {"merk": "Hansgrohe", "serie": "Croma Select S", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe EcoSmart thermostaat",
     "categorie": "douchesysteem", "codes": [], "ean": ["4011097806297"],
     "van": 656, "tot": 751, "bron": "bsl_4011097806297"},
    # Beslist 4 aanbieders, EUR 589.54-688.01
    {"merk": "Hansgrohe", "serie": "Croma Select S", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 280 thermostaat",
     "categorie": "douchesysteem", "codes": [], "ean": ["4011097806280"],
     "van": 589, "tot": 689, "bron": "bsl_4011097806280"},
    # Beslist 5 aanbieders, EUR 760.19-1135.25
    {"merk": "Hansgrohe", "serie": "Raindance Alive", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 300 Ecostat Element",
     "categorie": "douchesysteem", "codes": [], "ean": ["4059625568613"],
     "van": 760, "tot": 1136, "bron": "bsl_4059625568613"},
    # Beslist 10 aanbieders, EUR 365.00-671.42
    {"merk": "Hansgrohe", "serie": "Vernis Blend", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 200 thermostaat mat zwart",
     "categorie": "douchesysteem", "codes": [], "ean": ["4059625338667"],
     "van": 365, "tot": 672, "bron": "bsl_4059625338667"},
    # Beslist 7 aanbieders, EUR 260.82-392.40
    {"merk": "Hansgrohe", "serie": "Vernis Blend", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 1jet chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4059625328934"],
     "van": 260, "tot": 393, "bron": "bsl_4059625328934"},
    # Beslist 5 aanbieders, EUR 286.30-389.00
    {"merk": "Hansgrohe", "serie": "Activera S", "oms": "Douchesysteem/regendoucheset opbouw, Showerpipe 1jet EcoSmart chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4059625605141"],
     "van": 286, "tot": 389, "bron": "bsl_4059625605141"},
    # Beslist 4 aanbieders, EUR 319.23-428.11
    {"merk": "Grohe", "serie": "Tempesta Cosmopolitan 210", "oms": "Douchesysteem/regendoucheset opbouw, douchesysteem met thermostaat chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4005176985348"],
     "van": 319, "tot": 429, "bron": "bsl_4005176985348"},
    # Beslist 8 aanbieders, EUR 525.67-819.55
    {"merk": "Hansgrohe", "serie": "Pulsify S", "oms": "Douchesysteem/regendoucheset opbouw, Puro douchesysteem thermostaat chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4059625539125"],
     "van": 525, "tot": 820, "bron": "bsl_4059625539125"},
    # Beslist 8 aanbieders, EUR 261.80-390.28
    {"merk": "Grohe", "serie": "Tempesta Cosmopolitan", "oms": "Douchesysteem/regendoucheset opbouw, douchesysteem chroom",
     "categorie": "douchesysteem", "codes": [], "ean": ["4005176923364"],
     "van": 261, "tot": 391, "bron": "bsl_4005176923364"},
    # Beslist 3 aanbieders, EUR 280.89-519.00
    {"merk": "Ideal Standard", "serie": "Ceratherm T25", "oms": "Douchesysteem/regendoucheset opbouw, Ceratherm T25+ douchesysteem met thermostaat",
     "categorie": "douchesysteem", "codes": ["A7212AA"], "ean": ["4015413356732"],
     "van": 280, "tot": 519, "bron": "bsl_4015413356732"},
    # ---- handdouche_set ----
    # Beslist 4 aanbieders, EUR 182.34-195.67
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Handdouche/glijstangset, doucheset thermostaat+glijstang",
     "categorie": "handdouche_set", "codes": [], "ean": ["4005176766459"],
     "van": 182, "tot": 196, "bron": "bsl_4005176766459"},
    # Beslist 3 aanbieders, EUR 190.00-304.99
    {"merk": "Grohe", "serie": "Grohtherm 1000 Performance", "oms": "Handdouche/glijstangset, doucheset thermostaat+glijstang",
     "categorie": "handdouche_set", "codes": [], "ean": ["4005176766381"],
     "van": 190, "tot": 305, "bron": "bsl_4005176766381"},
    # Beslist 8 aanbieders, EUR 152.21-195.00
    {"merk": "Hansgrohe", "serie": "Crometta", "oms": "Handdouche/glijstangset, Crometta Vario renovatieset met Ecostat 1001 CL",
     "categorie": "handdouche_set", "codes": [], "ean": ["4011097803265"],
     "van": 152, "tot": 195, "bron": "bsl_4011097803265"},
    # Beslist 5 aanbieders, EUR 231.76-343.96
    {"merk": "Hansgrohe", "serie": "Pulsify Select S", "oms": "Handdouche/glijstangset, doucheset 105 glijstang 65 cm met thermostaat",
     "categorie": "handdouche_set", "codes": [], "ean": ["4059625534496"],
     "van": 231, "tot": 344, "bron": "bsl_4059625534496"},
    # Beslist 3 aanbieders, EUR 57.16-81.66
    {"merk": "Grohe", "serie": "Tempesta 110", "oms": "Handdouche/glijstangset, glijstangset 60 cm chroom",
     "categorie": "handdouche_set", "codes": [], "ean": ["4005176680632"],
     "van": 57, "tot": 82, "bron": "bsl_4005176680632"},
    # Beslist 3 aanbieders, EUR 84.54-109.00
    {"merk": "Hansgrohe", "serie": "Croma 100", "oms": "Handdouche/glijstangset, Croma 100 Vario glijstangset 90 cm chroom",
     "categorie": "handdouche_set", "codes": [], "ean": ["4011097537290"],
     "van": 84, "tot": 109, "bron": "bsl_4011097537290"},
    # Beslist 5 aanbieders, EUR 97.44-139.00
    {"merk": "Hansgrohe", "serie": "Croma Select S", "oms": "Handdouche/glijstangset, Croma Select S Vario glijstangset 90 cm wit/chroom",
     "categorie": "handdouche_set", "codes": [], "ean": ["4011097736402"],
     "van": 97, "tot": 139, "bron": "bsl_4011097736402"},
    # Beslist 7 aanbieders, EUR 91.09-147.68
    {"merk": "Hansgrohe", "serie": "Pulsify Select", "oms": "Handdouche/glijstangset, glijstangset 3jet Relaxation 90 cm chroom",
     "categorie": "handdouche_set", "codes": [], "ean": ["4059625348024"],
     "van": 91, "tot": 148, "bron": "bsl_4059625348024"},
    # Beslist 7 aanbieders, EUR 299.57-444.65
    {"merk": "Hansgrohe", "serie": "Pulsify Select S", "oms": "Handdouche/glijstangset, thermostaat met glijstangset 65 cm mat zwart",
     "categorie": "handdouche_set", "codes": [], "ean": ["4059625534489"],
     "van": 299, "tot": 445, "bron": "bsl_4059625534489"},
    # Beslist 8 aanbieders, EUR 62.74-114.19
    {"merk": "Hansgrohe", "serie": "Raindance Select S", "oms": "Handdouche/glijstangset, handdouche 120 wit/chroom",
     "categorie": "handdouche_set", "codes": [], "ean": ["4011097726663"],
     "van": 62, "tot": 115, "bron": "bsl_4011097726663"},
    # ---- wastafelkraan ----
    # Beslist 6 aanbieders, EUR 113.92-194.95
    {"merk": "Grohe", "serie": "Eurosmart Cosmopolitan", "oms": "Wastafelkraan, wastafelkraan chroom waterbesparend",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4005176584039"],
     "van": 113, "tot": 195, "bron": "bsl_4005176584039"},
    # Beslist 8 aanbieders, EUR 110.33-187.95
    {"merk": "Grohe", "serie": "Eurosmart Cosmopolitan", "oms": "Wastafelkraan, wastafelkraan hoge draaibare uitloop chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4005176472749"],
     "van": 110, "tot": 188, "bron": "bsl_4005176472749"},
    # Beslist 5 aanbieders, EUR 40.69-78.99
    {"merk": "Grohe", "serie": "BauEdge", "oms": "Wastafelkraan, wastafelmengkraan chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4005176934278"],
     "van": 40, "tot": 79, "bron": "bsl_4005176934278"},
    # Beslist 9 aanbieders, EUR 78.00-125.95
    {"merk": "Hansgrohe", "serie": "Logis", "oms": "Wastafelkraan, Logis 100 wastafelmengkraan chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097738550"],
     "van": 78, "tot": 126, "bron": "bsl_4011097738550"},
    # Beslist 7 aanbieders, EUR 59.00-112.90
    {"merk": "Hansgrohe", "serie": "Logis", "oms": "Wastafelkraan, Logis 70 wastafelmengkraan chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097738680"],
     "van": 59, "tot": 113, "bron": "bsl_4011097738680"},
    # Beslist 7 aanbieders, EUR 83.74-111.87
    {"merk": "Hansgrohe", "serie": "Logis E", "oms": "Wastafelkraan, wastafelmengkraan draaibare uitloop chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097738413"],
     "van": 83, "tot": 112, "bron": "bsl_4011097738413"},
    # Beslist 7 aanbieders, EUR 79.00-139.87
    {"merk": "Hansgrohe", "serie": "Logis", "oms": "Wastafelkraan, wastafelkraan mat zwart",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4059625460597"],
     "van": 79, "tot": 140, "bron": "bsl_4059625460597"},
    # Beslist 9 aanbieders, EUR 147.74-284.64
    {"merk": "Hansgrohe", "serie": "Talis E", "oms": "Wastafelkraan, wastafelmengkraan brushed black chrome",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4059625147054"],
     "van": 147, "tot": 285, "bron": "bsl_4059625147054"},
    # Beslist 6 aanbieders, EUR 109.31-164.17
    {"merk": "Hansgrohe", "serie": "Talis E", "oms": "Wastafelkraan, Talis E 110 wastafelmengkraan chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097770741"],
     "van": 109, "tot": 165, "bron": "bsl_4011097770741"},
    # Beslist 8 aanbieders, EUR 93.45-138.95
    {"merk": "Hansgrohe", "serie": "Talis E", "oms": "Wastafelkraan, Talis E wastafelmengkraan CoolStart chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097770727"],
     "van": 93, "tot": 139, "bron": "bsl_4011097770727"},
    # Beslist 7 aanbieders, EUR 154.43-221.66
    {"merk": "Hansgrohe", "serie": "Talis Select E", "oms": "Wastafelkraan, Talis Select E 110 wastafelkraan chroom",
     "categorie": "wastafelkraan", "codes": ["71751000"], "ean": ["4011097775791"],
     "van": 154, "tot": 222, "bron": "bsl_4011097775791"},
    # Beslist 7 aanbieders, EUR 72.31-118.25
    {"merk": "Hansgrohe", "serie": "Focus", "oms": "Wastafelkraan, wastafelmengkraan chroom zonder afvoer",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097679402"],
     "van": 72, "tot": 119, "bron": "bsl_4011097679402"},
    # Beslist 7 aanbieders, EUR 87.44-173.56
    {"merk": "Hansgrohe", "serie": "Talis S", "oms": "Wastafelkraan, wastafelmengkraan chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097770116"],
     "van": 87, "tot": 174, "bron": "bsl_4011097770116"},
    # Beslist 8 aanbieders, EUR 109.87-190.82
    {"merk": "Grohe", "serie": "Essence", "oms": "Wastafelkraan, Essence wastafelkraan chroom S-size",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4005176339189"],
     "van": 109, "tot": 191, "bron": "bsl_4005176339189"},
    # Beslist 7 aanbieders, EUR 129.75-195.91
    {"merk": "Grohe", "serie": "Essence", "oms": "Wastafelkraan, Essence wastafelkraan hoge draaibare uitloop chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4005176306907"],
     "van": 129, "tot": 196, "bron": "bsl_4005176306907"},
    # Beslist 6 aanbieders, EUR 183.60-204.00
    {"merk": "Hotbath", "serie": "Cobber", "oms": "Wastafelkraan, wastafelmengkraan gebogen chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["8718924072264"],
     "van": 183, "tot": 204, "bron": "bsl_8718924072264"},
    # Beslist 6 aanbieders, EUR 119.15-143.62
    {"merk": "Hansgrohe", "serie": "Talis E", "oms": "Wastafelkraan, Talis E 110 wastafelmengkraan ComfortZone chroom",
     "categorie": "wastafelkraan", "codes": [], "ean": ["4011097770765"],
     "van": 119, "tot": 144, "bron": "bsl_4011097770765"},
    # Serie: 9 Cobber-inbouwkranen in het overzicht (diverse kleuren)
    {"merk": "Hotbath", "serie": "Cobber", "oms": "Inbouw wastafelkraan Cobber, uitloop 18-25 cm, PVD (serie)",
     "categorie": "wastafelkraan", "codes": [], "ean": [],
     "van": 408, "tot": 497, "bron": "bsl_ovz_hotbath_wastafelkraan"},
    # ---- badkraan ----
    # Beslist 10 aanbieders, EUR 152.15-208.91
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Badkraan opbouw, badkraan thermostatisch chroom",
     "categorie": "badkraan", "codes": [], "ean": ["4005176310157"],
     "van": 152, "tot": 209, "bron": "bsl_4005176310157"},
    # Beslist 9 aanbieders, EUR 165.14-249.03
    {"merk": "Grohe", "serie": "Grohtherm 800", "oms": "Badkraan opbouw, badkraan waterbesparend",
     "categorie": "badkraan", "codes": [], "ean": ["4005176612039"],
     "van": 165, "tot": 250, "bron": "bsl_4005176612039"},
    # Beslist 5 aanbieders, EUR 238.00-360.48
    {"merk": "Grohe", "serie": "Grohtherm 1000", "oms": "Badkraan opbouw, badmengkraan thermostatisch",
     "categorie": "badkraan", "codes": [], "ean": ["4005176695742"],
     "van": 238, "tot": 361, "bron": "bsl_4005176695742"},
    # Beslist 10 aanbieders, EUR 115.15-237.21
    {"merk": "Hansgrohe", "serie": "Ecostat 1001 CL", "oms": "Badkraan opbouw, badthermostaat",
     "categorie": "badkraan", "codes": [], "ean": ["4011097799599"],
     "van": 115, "tot": 238, "bron": "bsl_4011097799599"},
    # Beslist 8 aanbieders, EUR 97.00-120.79
    {"merk": "Hansgrohe", "serie": "Logis", "oms": "Badkraan opbouw, badmengkraan opbouw eengreeps chroom",
     "categorie": "badkraan", "codes": [], "ean": ["4011097738260"],
     "van": 97, "tot": 121, "bron": "bsl_4011097738260"},
    # Beslist 6 aanbieders, EUR 77.95-158.95
    {"merk": "Grohe", "serie": "Costa L", "oms": "Badkraan opbouw, badkraan chroom hoh 15 cm",
     "categorie": "badkraan", "codes": [], "ean": ["4005176843082"],
     "van": 77, "tot": 159, "bron": "bsl_4005176843082"},
    # Beslist 4 aanbieders, EUR 203.00-328.99
    {"merk": "Grohe", "serie": "Grohtherm", "oms": "Badkraan opbouw, thermostatische badkraan wandmontage chroom",
     "categorie": "badkraan", "codes": [], "ean": ["4005176698682"],
     "van": 203, "tot": 329, "bron": "bsl_4005176698682"},
    # Beslist 4 aanbieders, EUR 256.91-472.99
    {"merk": "Ideal Standard", "serie": "Ceratherm S200", "oms": "Badkraan opbouw, badthermostaat chroom",
     "categorie": "badkraan", "codes": [], "ean": ["4015413350808"],
     "van": 256, "tot": 473, "bron": "bsl_4015413350808"},
    # Beslist 3 aanbieders, EUR 109.22-129.14
    {"merk": "Grohe", "serie": "Cubeo", "oms": "Badkraan opbouw, badmengkraan opbouw chroom",
     "categorie": "badkraan", "codes": [], "ean": ["4067393011590"],
     "van": 109, "tot": 130, "bron": "bsl_4067393011590"},
    # ---- inbouwkraan ----
    # Beslist 7 aanbieders, EUR 968.11-1294.90
    {"merk": "Grohe", "serie": "Grohtherm SmartControl", "oms": "Inbouwkraan/inbouwset, inbouw doucheset thermostaat met hoofddouche 31 vierkant",
     "categorie": "inbouwkraan", "codes": [], "ean": ["4005176413810"],
     "van": 968, "tot": 1295, "bron": "bsl_4005176413810"},
    # Beslist 4 aanbieders, EUR 1490.53-1766.44
    {"merk": "Hotbath", "serie": "Cobber IBS23", "oms": "Inbouwkraan/inbouwset, inbouw doucheset chroom 30cm hoofddouche",
     "categorie": "inbouwkraan", "codes": ["IBS23"], "ean": ["8720143177422"],
     "van": 1490, "tot": 1767, "bron": "bsl_8720143177422"},
    # Beslist 5 aanbieders, EUR 288.65-474.54
    {"merk": "Grohe", "serie": "Grohtherm", "oms": "Inbouwkraan/inbouwset, inbouw douchethermostaat (afbouwdeel) chroom",
     "categorie": "inbouwkraan", "codes": [], "ean": ["4005176466007"],
     "van": 288, "tot": 475, "bron": "bsl_4005176466007"},
    # Beslist 4 aanbieders, EUR 385.61-534.99
    {"merk": "Grohe", "serie": "Grohtherm SmartControl", "oms": "Inbouwkraan/inbouwset, inbouw douchethermostaat rond chroom (afbouwdeel)",
     "categorie": "inbouwkraan", "codes": [], "ean": ["4005176412240"],
     "van": 385, "tot": 535, "bron": "bsl_4005176412240"},
    # Beslist 3 aanbieders, EUR 735.01-920.00
    {"merk": "Grohe", "serie": "Grohtherm Perfect", "oms": "Inbouwkraan/inbouwset, inbouw doucheset met regendouche chroom",
     "categorie": "inbouwkraan", "codes": [], "ean": ["4005176466403"],
     "van": 735, "tot": 920, "bron": "bsl_4005176466403"},
    # Beslist 9 aanbieders, EUR 300.48-402.90
    {"merk": "Grohe", "serie": "Grohtherm", "oms": "Inbouwkraan/inbouwset, inbouw douchethermostaat (afbouwdeel) chroom, variant 2",
     "categorie": "inbouwkraan", "codes": [], "ean": ["4005176465994"],
     "van": 300, "tot": 403, "bron": "bsl_4005176465994"},
    # Beslist 3 aanbieders, EUR 179.69-260.15
    {"merk": "Grohe", "serie": "Essence", "oms": "Inbouwkraan/inbouwset, inbouw badkraan met omstel chroom (afbouwdeel)",
     "categorie": "inbouwkraan", "codes": [], "ean": ["4005176698422"],
     "van": 179, "tot": 261, "bron": "bsl_4005176698422"},
    # Serie: 10 Giulini-inbouwsets in het overzicht
    {"merk": "Sanimex", "serie": "Giulini", "oms": "Inbouw regendoucheset thermostatisch, met inbouwdeel (serie)",
     "categorie": "inbouwkraan", "codes": [], "ean": [],
     "van": 1044, "tot": 1562, "bron": "bsl_ovz_sanimex"},
    # ---- douchegoot ----
    # Beslist 4 aanbieders, EUR 233.81-309.00
    {"merk": "Geberit", "serie": "CleanLine30", "oms": "Douchegoot, douchegoot 30-90 cm rvs",
     "categorie": "douchegoot", "codes": [], "ean": ["4064746028748"],
     "van": 233, "tot": 309, "bron": "bsl_4064746028748"},
    # Beslist 4 aanbieders, EUR 280.95-365.38
    {"merk": "Geberit", "serie": "CleanLine20", "oms": "Douchegoot, douchegoot 30-110 cm rvs",
     "categorie": "douchegoot", "codes": [], "ean": ["4064746058028"],
     "van": 280, "tot": 366, "bron": "bsl_4064746058028"},
    # Beslist 6 aanbieders, EUR 288.66-404.24
    {"merk": "Geberit", "serie": "CleanLine60", "oms": "Douchegoot, douchegoot rvs",
     "categorie": "douchegoot", "codes": [], "ean": ["4025416383147"],
     "van": 288, "tot": 405, "bron": "bsl_4025416383147"},
    # Beslist 3 aanbieders, EUR 531.37-772.27
    {"merk": "Geberit", "serie": "CleanLine80", "oms": "Douchegoot, douchegoot 30-130 cm",
     "categorie": "douchegoot", "codes": ["154.441.KS.1"], "ean": ["4025410736468"],
     "van": 531, "tot": 773, "bron": "bsl_4025410736468"},
    # Beslist 4 aanbieders, EUR 75.00-269.00
    {"merk": "Wiesbaden", "serie": "Drain", "oms": "Douchegoot, douchegoot met flens 90 cm mat zwart",
     "categorie": "douchegoot", "codes": [], "ean": ["8719323039117"],
     "van": 75, "tot": 269, "bron": "bsl_8719323039117"},
    # Beslist 3 aanbieders, EUR 212.99-228.69
    {"merk": "Aco", "serie": "ShowerDrain C", "oms": "Douchegoot, douchegoot rvs",
     "categorie": "douchegoot", "codes": [], "ean": ["4002626880574"],
     "van": 212, "tot": 229, "bron": "bsl_4002626880574"},
    # Beslist 3 aanbieders, EUR 431.99-448.49
    {"merk": "I-Drain", "serie": "Pro Linear 54", "oms": "Douchegoot, douchegoot rvs 600 mm",
     "categorie": "douchegoot", "codes": [], "ean": ["5420056905596"],
     "van": 431, "tot": 449, "bron": "bsl_5420056905596"},
    # Beslist 3 aanbieders, EUR 469.99-487.87
    {"merk": "I-Drain", "serie": "Pro Linear 54", "oms": "Douchegoot, douchegoot zonder rooster 800 mm",
     "categorie": "douchegoot", "codes": [], "ean": ["5420056905619"],
     "van": 469, "tot": 488, "bron": "bsl_5420056905619"},
    # Serie: laagste prijzen van 9 Compact-uitvoeringen 60-80 cm in het overzicht
    {"merk": "Easy Drain", "serie": "Compact", "oms": "Douchegoot Compact / Compact Clean 60-100 cm, rvs (serie)",
     "categorie": "douchegoot", "codes": [], "ean": [],
     "van": 246, "tot": 389, "bron": "bsl_ovz_easy_drain"},
    # Serie: 5 Multi-inbouwdelen in het overzicht
    {"merk": "Easy Drain", "serie": "Multi", "oms": "Douchegoot Multi inbouwdeel zonder rooster 70-100 cm (serie)",
     "categorie": "douchegoot", "codes": [], "ean": [],
     "van": 171, "tot": 190, "bron": "bsl_ovz_easy_drain"},
    # Serie: 2 Tegeldrain-uitvoeringen in het overzicht; smalle band, alleen indicatief
    {"merk": "Easy Drain", "serie": "Tegeldrain", "oms": "Douchegoot Tegeldrain rvs, betegelbaar (serie)",
     "categorie": "douchegoot", "codes": [], "ean": [],
     "van": 269, "tot": 304, "bron": "bsl_ovz_easy_drain"},
    # Serie: rvs-uitvoeringen; zwarte 'Colours'-uitvoeringen (EUR 488-588) vallen erbuiten
    {"merk": "Aco", "serie": "ShowerDrain C", "oms": "Douchegoot ShowerDrain C rvs, 48-89 cm (serie)",
     "categorie": "douchegoot", "codes": [], "ean": [],
     "van": 146, "tot": 215, "bron": "bsl_ovz_aco_showerdrain"},
    # Serie: 15 douchedrains met flens in het overzicht
    {"merk": "Wiesbaden", "serie": "Douchedrain", "oms": "Douchegoot met flens 50-110 cm, rvs (Elbe, Eufraat, Tiber, Tigris, Theems)",
     "categorie": "douchegoot", "codes": [], "ean": [],
     "van": 139, "tot": 230, "bron": "bsl_ovz_wiesbaden_douchegoot"},
    # ---- douchewand ----
    # Beslist 4 aanbieders, EUR 299.00-329.99
    {"merk": "Wiesbaden", "serie": "Less", "oms": "Douchewand/inloopdouche, inloopdouche 120x200 cm 8 mm helder glas chroom",
     "categorie": "douchewand", "codes": [], "ean": ["8720847408723"],
     "van": 299, "tot": 330, "bron": "bsl_8720847408723"},
    # Beslist 6 aanbieders, EUR 218.05-245.00
    {"merk": "Wiesbaden", "serie": "Slim", "oms": "Douchewand/inloopdouche, inloopdouche 90x200 cm brons rookglas 8 mm",
     "categorie": "douchewand", "codes": [], "ean": ["8720847404985"],
     "van": 218, "tot": 245, "bron": "bsl_8720847404985"},
    # Beslist 5 aanbieders, EUR 186.15-359.00
    {"merk": "Wiesbaden", "serie": "Comfort", "oms": "Douchewand/inloopdouche, inloopdouche 130x200 cm helder glas chroom",
     "categorie": "douchewand", "codes": [], "ean": ["8718053679051"],
     "van": 186, "tot": 359, "bron": "bsl_8718053679051"},
    # Beslist 3 aanbieders, EUR 445.00-500.00
    {"merk": "Sealskin", "serie": "I AM", "oms": "Douchewand/inloopdouche, zijwand 90x200 cm chroom",
     "categorie": "douchewand", "codes": [], "ean": ["8717821384852"],
     "van": 445, "tot": 500, "bron": "bsl_8717821384852"},
    # Serie: 13 Slim-uitvoeringen (helder glas en rookglas) in het overzicht
    {"merk": "Wiesbaden", "serie": "Slim", "oms": "Inloopdouche Slim 60-100 x 200 cm, 8 mm glas (serie)",
     "categorie": "douchewand", "codes": [], "ean": [],
     "van": 207, "tot": 347, "bron": "bsl_ovz_wiesbaden_inloopdouche"},
    # ---- douchecabine ----
    # Beslist 5 aanbieders, EUR 385.00-579.00
    {"merk": "Wiesbaden", "serie": "Hoekinstap", "oms": "Douchecabine, douchecabine hoekinstap 90x90x200 8 mm mat zwart",
     "categorie": "douchecabine", "codes": [], "ean": ["8719956087356"],
     "van": 385, "tot": 579, "bron": "bsl_8719956087356"},
    # Beslist 8 aanbieders, EUR 517.76-599.00
    {"merk": "Wiesbaden", "serie": "Sydney", "oms": "Douchecabine, kwartronde douchecabine 90x200 2 deuren",
     "categorie": "douchecabine", "codes": [], "ean": ["8718858072057"],
     "van": 517, "tot": 599, "bron": "bsl_8718858072057"},
    # Beslist 9 aanbieders, EUR 492.80-579.00
    {"merk": "Wiesbaden", "serie": "Single", "oms": "Douchecabine, douchecabine draaideur 90x90 chroom",
     "categorie": "douchecabine", "codes": [], "ean": ["8718503678351"],
     "van": 492, "tot": 579, "bron": "bsl_8718503678351"},
    # Beslist 6 aanbieders, EUR 289.00-329.00
    {"merk": "Wiesbaden", "serie": "Kwartrond", "oms": "Douchecabine, douchecabine kwartrond 90x90x190 helder glas",
     "categorie": "douchecabine", "codes": [], "ean": ["8719323030978"],
     "van": 289, "tot": 329, "bron": "bsl_8719323030978"},
    # Beslist 7 aanbieders, EUR 531.09-699.00
    {"merk": "Wiesbaden", "serie": "Uni", "oms": "Douchecabine, douchecabine 90x90 mat zwart swingdeur",
     "categorie": "douchecabine", "codes": [], "ean": ["8720195543619"],
     "van": 531, "tot": 699, "bron": "bsl_8720195543619"},
    # Beslist 4 aanbieders, EUR 516.00-697.00
    {"merk": "Sealskin", "serie": "Hooked", "oms": "Douchecabine, douchecabine kwartrond 90x90 schuifdeuren chroom",
     "categorie": "douchecabine", "codes": [], "ean": ["8720314711479"],
     "van": 516, "tot": 697, "bron": "bsl_8720314711479"},
    # Serie: 18 Pure-cabines in het overzicht (zilver, zwart, gunmetal, goud)
    {"merk": "Sealskin", "serie": "Pure", "oms": "Douchecabine Pure 90x90 t/m 100x120 cm, anti-kalk (serie)",
     "categorie": "douchecabine", "codes": [], "ean": [],
     "van": 705, "tot": 905, "bron": "bsl_ovz_sealskin"},
    # ---- douchebak ----
    # Beslist 3 aanbieders, EUR 148.57-209.95
    {"merk": "Sealskin", "serie": "Fusion", "oms": "Douchebak, douchebak vierkant 90x90 inbouw wit",
     "categorie": "douchebak", "codes": [], "ean": ["8717821437183"],
     "van": 148, "tot": 210, "bron": "bsl_8717821437183"},
    # Beslist 3 aanbieders, EUR 211.61-291.32
    {"merk": "Ideal Standard", "serie": "Ultra Flat S", "oms": "Douchebak, i.life douchebak 90x90x3 carrara wit",
     "categorie": "douchebak", "codes": [], "ean": ["8014140492672"],
     "van": 211, "tot": 292, "bron": "bsl_8014140492672"},
    # Beslist 3 aanbieders, EUR 236.84-329.95
    {"merk": "Sealskin", "serie": "Fusion", "oms": "Douchebak, douchebak opbouw kwartrond 90x90 wit",
     "categorie": "douchebak", "codes": [], "ean": ["8717821437152"],
     "van": 236, "tot": 330, "bron": "bsl_8717821437152"},
    # Beslist 4 aanbieders, EUR 597.00-883.00
    {"merk": "Villeroy & Boch", "serie": "Squaro Infinity", "oms": "Douchebak, douchebak 120x90 Quaryl wit",
     "categorie": "douchebak", "codes": [], "ean": ["4051202851682"],
     "van": 597, "tot": 883, "bron": "bsl_4051202851682"},
    # Serie: 11 Ecora-maten in het overzicht
    {"merk": "Villeroy & Boch", "serie": "Ecora", "oms": "Douchebak Ecora 100x80 t/m 180x100 cm (serie)",
     "categorie": "douchebak", "codes": [], "ean": [],
     "van": 276, "tot": 521, "bron": "bsl_ovz_vb_douchebak"},
    # Serie: 6 Squaro Infinity-uitvoeringen; bovenkant uit de vergelijking van 120x90 wit
    {"merk": "Villeroy & Boch", "serie": "Squaro Infinity", "oms": "Douchebak Squaro Infinity Quaryl, 90x80 t/m 120x90 cm (serie)",
     "categorie": "douchebak", "codes": [], "ean": [],
     "van": 562, "tot": 883, "bron": "bsl_ovz_vb_douchebak"},
    # Serie: 6 Ultra Flat S-uitvoeringen; de Ultra Flat Solid (EUR 521-909) valt erbuiten
    {"merk": "Ideal Standard", "serie": "Ultra Flat S", "oms": "Douchebak Ultra Flat S (i.life) 70x70 t/m 160x80 cm (serie)",
     "categorie": "douchebak", "codes": [], "ean": [],
     "van": 127, "tot": 315, "bron": "bsl_ovz_is_douchebak"},
]

BRONNEN = {
    "bsl_4005176612022": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 douchemengkraan chroom (10 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-800-thermostatische-douchemengkraan-chroom/27000/4005176612022/"],
    "bsl_4005176310096": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 douchekraan EcoButton (10 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-800-douchekraan-chroom-thermostatisch-met-ecobutton/27000/4005176310096/"],
    "bsl_4005176310089": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 douchekraan EcoJoy volumegreep (8 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-800-douchekraan-chroom-thermostatisch-met-ecojoy-en-volumegreep/27000/4005176310089/"],
    "bsl_4005176612046": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 douchekraan 34767000 (5 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-800-thermostatische-douchekraan-chroom-34767000/27000/4005176612046/"],
    "bsl_4005176695728": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 1000 douchethermostaat CoolTouch (6 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-1000-douchethermostaat-chroom-cooltouch-water-saving/27000/4005176695728/"],
    "bsl_4005176698651": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 1000 Performance douchekraan (5 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-1000-performance-douchekraan-cooltouch-150mm/27000/4005176698651/"],
    "bsl_4005176309618": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 1000 douchekraan thermostatisch (5 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-1000-douchekraan-thermostatisch-chroom/27000/4005176309618/"],
    "bsl_4005176374432": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 1000 Cosmopolitan douchekraan supersteel (6 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-1000-cosmopolitan-thermostatische-douchekraan-supersteel-rvs/27000/4005176374432/"],
    "bsl_4011097799582": ["Beslist.nl prijsvergelijking: Hansgrohe Ecostat douchethermostaat opbouw (10 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-ecostat-douchethermostaat-chroom-opbouw/27000/4011097799582/"],
    "bsl_4011097678856": ["Beslist.nl prijsvergelijking: Hansgrohe Ecostat Comfort douchethermostaat opbouw (9 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-ecostat-comfort-douchethermostaat-chroom-opbouwmontage/27000/4011097678856/"],
    "bsl_4059625522400": ["Beslist.nl prijsvergelijking: Hansgrohe Ecostat Element douchethermostaat (8 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-ecostat-element-douchethermostaat-chroom/27000/4059625522400/"],
    "bsl_8720847724892": ["Beslist.nl prijsvergelijking: Hotbath Cobber X thermostatische douchemengkraan opbouw verouderd messing (4 aanbieders)",
        "https://www.beslist.nl/p/hotbath-cobber-x-thermostatische-douchemengkraan-verouderd-messing/27000/8720847724892/"],
    "vgl_kieskeurig_34558000": ["Kieskeurig.nl prijsvergelijking: Grohe Grohtherm 800 thermostatische douchemengkraan 34558000",
        "https://www.kieskeurig.nl/douchekop/product/59009839-grohe-grohtherm-800-thermostatische-douchemengkraan-34558000"],
    "bsl_4005176457586": ["Beslist.nl prijsvergelijking: Grohe Euphoria SmartControl douchesysteem Duo 310 thermostaat chroom (10 aanbieders)",
        "https://www.beslist.nl/p/grohe-euphoria-smartcontrol-doucheset-duo-310-chroom/27000/4005176457586/"],
    "bsl_4005176457623": ["Beslist.nl prijsvergelijking: Grohe Euphoria SmartControl douchesysteem 260 thermostaat chroom (10 aanbieders)",
        "https://www.beslist.nl/p/grohe-euphoria-smartcontrol-system-260-regendoucheset-glanzend-chroom/27000/4005176457623/"],
    "bsl_4005176457593": ["Beslist.nl prijsvergelijking: Grohe Euphoria SmartControl douchesysteem 310 Cube thermostaat chroom (10 aanbieders)",
        "https://www.beslist.nl/p/grohe-euphoria-smartcontrol-310-cube-regendouche-chroom-inclusief-thermostaatkraan/27000/4005176457593/"],
    "bsl_4011097775937": ["Beslist.nl prijsvergelijking: Hansgrohe Crometta S Showerpipe 240 1jet EcoSmart thermostaat (9 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-crometta-s-showerpipe-240-1jet-ecosmart-chroom-thermostaat/27000/4011097775937/"],
    "bsl_4011097775890": ["Beslist.nl prijsvergelijking: Hansgrohe Crometta E Showerpipe 240 EcoSmart thermostaat (6 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-crometta-e-240-showerpipe-chroom-ecosmart/27000/4011097775890/"],
    "bsl_4011097806297": ["Beslist.nl prijsvergelijking: Hansgrohe Croma Select S Showerpipe EcoSmart thermostaat (6 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-croma-select-s-showerpipe-chroom-ecosmart-8-l-min/27000/4011097806297/"],
    "bsl_4011097806280": ["Beslist.nl prijsvergelijking: Hansgrohe Croma Select S Showerpipe 280 thermostaat (4 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-croma-select-s-280-showerpipe-chroom-280-mm-hoofddouche/27000/4011097806280/"],
    "bsl_4059625568613": ["Beslist.nl prijsvergelijking: Hansgrohe Raindance Alive Showerpipe 300 Ecostat Element (5 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-raindance-alive-showerpipe-chroom-300-1-jet-puro-ecostat-element/27000/4059625568613/"],
    "bsl_4059625338667": ["Beslist.nl prijsvergelijking: Hansgrohe Vernis Blend Showerpipe 200 thermostaat mat zwart (10 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-vernis-blend-douchesysteem-mat-zwart/27000/4059625338667/"],
    "bsl_4059625328934": ["Beslist.nl prijsvergelijking: Hansgrohe Vernis Blend Showerpipe 1jet chroom (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-vernis-blend-doucheset-chroom-1-jet-20-5-cm-diameter/27000/4059625328934/"],
    "bsl_4059625605141": ["Beslist.nl prijsvergelijking: Hansgrohe Activera S Showerpipe 1jet EcoSmart chroom (5 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-activera-s-showerpipe-chroom-1-jet-ecosmart/27000/4059625605141/"],
    "bsl_4005176985348": ["Beslist.nl prijsvergelijking: Grohe Tempesta Cosmopolitan 210 douchesysteem met thermostaat chroom (4 aanbieders)",
        "https://www.beslist.nl/p/grohe-tempesta-cosmopolitan-210-regendouche-chroom-o-21-cm-met-thermostaat/27000/4005176985348/"],
    "bsl_4059625539125": ["Beslist.nl prijsvergelijking: Hansgrohe Pulsify S Puro douchesysteem thermostaat chroom (8 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-pulsify-s-puro-regendoucheset-chroom-thermostatisch-ronde-handdouche/27000/4059625539125/"],
    "bsl_4005176923364": ["Beslist.nl prijsvergelijking: Grohe Tempesta Cosmopolitan douchesysteem chroom (8 aanbieders)",
        "https://www.beslist.nl/p/grohe-tempesta-new-cosmopolitan-doucheset-chroom-messing/27000/4005176923364/"],
    "bsl_4015413356732": ["Beslist.nl prijsvergelijking: Ideal Standard Ceratherm T25 Ceratherm T25+ douchesysteem met thermostaat (3 aanbieders)",
        "https://www.beslist.nl/p/ideal-standard-ceratherm-t25-douchesysteem-315x531-5x1117-mm-8-0-l-min-3-bar-a7212aa/27000/4015413356732/"],
    "bsl_4005176766459": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 doucheset thermostaat+glijstang (4 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohetherm-800-doucheset-chroom-thermostatisch/27000/4005176766459/"],
    "bsl_4005176766381": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 1000 Performance doucheset thermostaat+glijstang (3 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-1000-performance-doucheset-chroom-thermostatische-douchekraan/27000/4005176766381/"],
    "bsl_4011097803265": ["Beslist.nl prijsvergelijking: Hansgrohe Crometta Crometta Vario renovatieset met Ecostat 1001 CL (8 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-crometta-vario-renovatieset-wit-chroom-inclusief-ecostat-1001-cl-thermostaat/27000/4011097803265/"],
    "bsl_4059625534496": ["Beslist.nl prijsvergelijking: Hansgrohe Pulsify Select S doucheset 105 glijstang 65 cm met thermostaat (5 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-pulsify-select-s-105-doucheset-glijstang-0-65-m-thermostaatkraan-ecosmart/27000/4059625534496/"],
    "bsl_4005176680632": ["Beslist.nl prijsvergelijking: Grohe Tempesta 110 glijstangset 60 cm chroom (3 aanbieders)",
        "https://www.beslist.nl/p/grohe-tempesta-110-glijstangset-60cm-ronde-handdouche-chroom/27000/4005176680632/"],
    "bsl_4011097537290": ["Beslist.nl prijsvergelijking: Hansgrohe Croma 100 Croma 100 Vario glijstangset 90 cm chroom (3 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-croma-100-vario-glijstangset-chroom-90cm/27000/4011097537290/"],
    "bsl_4011097736402": ["Beslist.nl prijsvergelijking: Hansgrohe Croma Select S Croma Select S Vario glijstangset 90 cm wit/chroom (5 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-croma-select-s-vario-glijstangset-wit-chroom-ecosmart-90cm/27000/4011097736402/"],
    "bsl_4059625348024": ["Beslist.nl prijsvergelijking: Hansgrohe Pulsify Select glijstangset 3jet Relaxation 90 cm chroom (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-pulsify-select-glijstangset-3jet-relaxationcm-met-glijstang-90-chroom/27000/4059625348024/"],
    "bsl_4059625534489": ["Beslist.nl prijsvergelijking: Hansgrohe Pulsify Select S thermostaat met glijstangset 65 cm mat zwart (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-pulsify-select-s-thermostaat-glijstangset-65cm-3-jet-mat-zwart/27000/4059625534489/"],
    "bsl_4011097726663": ["Beslist.nl prijsvergelijking: Hansgrohe Raindance Select S handdouche 120 wit/chroom (8 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-raindance-select-s-handdouche-wit-chroom-120-mm/27000/4011097726663/"],
    "bsl_4005176584039": ["Beslist.nl prijsvergelijking: Grohe Eurosmart Cosmopolitan wastafelkraan chroom waterbesparend (6 aanbieders)",
        "https://www.beslist.nl/p/grohe-eurosmart-cosmopolitan-wastafelkraan-chroom-waterbesparend/27000/4005176584039/"],
    "bsl_4005176472749": ["Beslist.nl prijsvergelijking: Grohe Eurosmart Cosmopolitan wastafelkraan hoge draaibare uitloop chroom (8 aanbieders)",
        "https://www.beslist.nl/p/grohe-eurosmart-cosmopolitan-wastafelkraan-chroom-hoge-draaibare-uitloop/27000/4005176472749/"],
    "bsl_4005176934278": ["Beslist.nl prijsvergelijking: Grohe BauEdge wastafelmengkraan chroom (5 aanbieders)",
        "https://www.beslist.nl/p/grohe-bauedge-wastafelmengkraan-chroom-waterbesparend/27000/4005176934278/"],
    "bsl_4011097738550": ["Beslist.nl prijsvergelijking: Hansgrohe Logis Logis 100 wastafelmengkraan chroom (9 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-logis-100-wastafelmengkraan-chroom-coolstart/27000/4011097738550/"],
    "bsl_4011097738680": ["Beslist.nl prijsvergelijking: Hansgrohe Logis Logis 70 wastafelmengkraan chroom (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-logis-70-eengreeps-wastafelmengkraan-chroom/27000/4011097738680/"],
    "bsl_4011097738413": ["Beslist.nl prijsvergelijking: Hansgrohe Logis E wastafelmengkraan draaibare uitloop chroom (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-logis-e-wastafelmengkraan-chroom-draaibare-uitloop/27000/4011097738413/"],
    "bsl_4059625460597": ["Beslist.nl prijsvergelijking: Hansgrohe Logis wastafelkraan mat zwart (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-logis-wastafelkraan-mat-zwart-eengreeps-ecosmart/27000/4059625460597/"],
    "bsl_4059625147054": ["Beslist.nl prijsvergelijking: Hansgrohe Talis E wastafelmengkraan brushed black chrome (9 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-talis-e-eengreeps-wastafelmengkraan-brushed-black-chrome/27000/4059625147054/"],
    "bsl_4011097770741": ["Beslist.nl prijsvergelijking: Hansgrohe Talis E Talis E 110 wastafelmengkraan chroom (6 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-talis-e-eengreeps-wastafelmengkraan-chroom/27000/4011097770741/"],
    "bsl_4011097770727": ["Beslist.nl prijsvergelijking: Hansgrohe Talis E Talis E wastafelmengkraan CoolStart chroom (8 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-talis-e-eengreeps-wastafelmengkraan-chroom-coolstart/27000/4011097770727/"],
    "bsl_4011097775791": ["Beslist.nl prijsvergelijking: Hansgrohe Talis Select E Talis Select E 110 wastafelkraan chroom (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-talis-select-e-110-wastafelkraan-11cm-laag-1-kraangat-zonder-waste-chroom-71751000/27000/4011097775791/"],
    "bsl_4011097679402": ["Beslist.nl prijsvergelijking: Hansgrohe Focus wastafelmengkraan chroom zonder afvoer (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-focus-eengreeps-wastafelmengkraan-chroom-zonder-afvoer/27000/4011097679402/"],
    "bsl_4011097770116": ["Beslist.nl prijsvergelijking: Hansgrohe Talis S wastafelmengkraan chroom (7 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-talis-s-wastafelmengkraan-chroom-hoogwaardig-design/27000/4011097770116/"],
    "bsl_4005176339189": ["Beslist.nl prijsvergelijking: Grohe Essence Essence wastafelkraan chroom S-size (8 aanbieders)",
        "https://www.beslist.nl/p/grohe-essence-new-wastafelkraan-chroom-eengreeps-uitloop-11-6cm/27000/4005176339189/"],
    "bsl_4005176306907": ["Beslist.nl prijsvergelijking: Grohe Essence Essence wastafelkraan hoge draaibare uitloop chroom (7 aanbieders)",
        "https://www.beslist.nl/p/grohe-essence-new-wastafelkraan-chroom-hoge-draaibare-uitloop/27000/4005176306907/"],
    "bsl_8718924072264": ["Beslist.nl prijsvergelijking: Hotbath Cobber wastafelmengkraan gebogen chroom (6 aanbieders)",
        "https://www.beslist.nl/p/hotbath-cobber-wastafelmengkraan-gebogen-chroom/27000/8718924072264/"],
    "bsl_4011097770765": ["Beslist.nl prijsvergelijking: Hansgrohe Talis E Talis E 110 wastafelmengkraan ComfortZone chroom (6 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-talis-e-eengreeps-wastafelmengkraan-chroom-comfortzone-110/27000/4011097770765/"],
    "bsl_ovz_hotbath_wastafelkraan": ["Beslist.nl overzicht Hotbath wastafelkraan",
        "https://www.beslist.nl/products/main_sanitair/r/hotbath_wastafelkraan/"],
    "bsl_4005176310157": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 badkraan thermostatisch chroom (10 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-800-badkraan-glanzend-chroom-thermostatisch/27000/4005176310157/"],
    "bsl_4005176612039": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 800 badkraan waterbesparend (9 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-800-thermostatische-badkraan-chroom-waterbesparend/27000/4005176612039/"],
    "bsl_4005176695742": ["Beslist.nl prijsvergelijking: Grohe Grohtherm 1000 badmengkraan thermostatisch (5 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-1000-thermostatische-badmengkraan-chroom-hoh-15cm/27000/4005176695742/"],
    "bsl_4011097799599": ["Beslist.nl prijsvergelijking: Hansgrohe Ecostat 1001 CL badthermostaat (10 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-ecostat-1001-cl-badthermostaat-chroom/27000/4011097799599/"],
    "bsl_4011097738260": ["Beslist.nl prijsvergelijking: Hansgrohe Logis badmengkraan opbouw eengreeps chroom (8 aanbieders)",
        "https://www.beslist.nl/p/hansgrohe-logis-badmengkraan-opbouw-eengreeps-chroom/27000/4011097738260/"],
    "bsl_4005176843082": ["Beslist.nl prijsvergelijking: Grohe Costa L badkraan chroom hoh 15 cm (6 aanbieders)",
        "https://www.beslist.nl/p/grohe-costa-l-badkraan-chroom-15cm-hartafstand/27000/4005176843082/"],
    "bsl_4005176698682": ["Beslist.nl prijsvergelijking: Grohe Grohtherm thermostatische badkraan wandmontage chroom (4 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-badmengkraan-chroom-wandmontage/27000/4005176698682/"],
    "bsl_4015413350808": ["Beslist.nl prijsvergelijking: Ideal Standard Ceratherm S200 badthermostaat chroom (4 aanbieders)",
        "https://www.beslist.nl/p/ideal-standard-ceratherm-s200-badthermostaat-chroom/27000/4015413350808/"],
    "bsl_4067393011590": ["Beslist.nl prijsvergelijking: Grohe Cubeo badmengkraan opbouw chroom (3 aanbieders)",
        "https://www.beslist.nl/p/grohe-cubeo-badmengkraan-chroom-opbouw-uitloop-16-7cm/27000/4067393011590/"],
    "bsl_4005176413810": ["Beslist.nl prijsvergelijking: Grohe Grohtherm SmartControl inbouw doucheset thermostaat met hoofddouche 31 vierkant (7 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-smartcontrol-doucheset-chroom-inbouw-regendouche-o-31-cm-vierkant-met-mengkraan/27000/4005176413810/"],
    "bsl_8720143177422": ["Beslist.nl prijsvergelijking: Hotbath Cobber IBS23 inbouw doucheset chroom 30cm hoofddouche (4 aanbieders)",
        "https://www.beslist.nl/p/hotbath-cobber-ibs23-inbouw-doucheset-chroom-30cm-hoofddouche-met-staafhanddouche/27000/8720143177422/"],
    "bsl_4005176466007": ["Beslist.nl prijsvergelijking: Grohe Grohtherm inbouw douchethermostaat (afbouwdeel) chroom (5 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-thermostatische-inbouw-douchekraan-chroom/27000/4005176466007/"],
    "bsl_4005176412240": ["Beslist.nl prijsvergelijking: Grohe Grohtherm SmartControl inbouw douchethermostaat rond chroom (afbouwdeel) (4 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-smartcontrol-douchekraan-inbouw-rond-chroom/27000/4005176412240/"],
    "bsl_4005176466403": ["Beslist.nl prijsvergelijking: Grohe Grohtherm Perfect inbouw doucheset met regendouche chroom (3 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-perfect-doucheset-inbouw-regendouche-chroom/27000/4005176466403/"],
    "bsl_4005176465994": ["Beslist.nl prijsvergelijking: Grohe Grohtherm inbouw douchethermostaat (afbouwdeel) chroom, variant 2 (9 aanbieders)",
        "https://www.beslist.nl/p/grohe-grohtherm-thermostatische-inbouw-douchekraan-chroom/27000/4005176465994/"],
    "bsl_4005176698422": ["Beslist.nl prijsvergelijking: Grohe Essence inbouw badkraan met omstel chroom (afbouwdeel) (3 aanbieders)",
        "https://www.beslist.nl/p/grohe-essence-badkraan-chroom-inbouw-met-omstel/27000/4005176698422/"],
    "bsl_ovz_sanimex": ["Beslist.nl overzicht Sanimex (210 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/sanimex/"],
    "bsl_4064746028748": ["Beslist.nl prijsvergelijking: Geberit CleanLine30 douchegoot 30-90 cm rvs (4 aanbieders)",
        "https://www.beslist.nl/p/geberit-cleanline30-douchegoot-30-90-cm-roestvrij-staal/27000/4064746028748/"],
    "bsl_4064746058028": ["Beslist.nl prijsvergelijking: Geberit CleanLine20 douchegoot 30-110 cm rvs (4 aanbieders)",
        "https://www.beslist.nl/p/geberit-cleanline20-douchegoot-30-110-cm-roestvrij-staal/27000/4064746058028/"],
    "bsl_4025416383147": ["Beslist.nl prijsvergelijking: Geberit CleanLine60 douchegoot rvs (6 aanbieders)",
        "https://www.beslist.nl/p/geberit-cleanline60-douchegoot-rvs/27000/4025416383147/"],
    "bsl_4025410736468": ["Beslist.nl prijsvergelijking: Geberit CleanLine80 douchegoot 30-130 cm (3 aanbieders)",
        "https://www.beslist.nl/p/geberit-cleanline80-douchegoot-lengte-30-130cm-kan-op-lengte-worden-gezaagd-154-441-ks-1/27000/4025410736468/"],
    "bsl_8719323039117": ["Beslist.nl prijsvergelijking: Wiesbaden Drain douchegoot met flens 90 cm mat zwart (4 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-drain-douchegoot-met-flens-90-cm-mat-zwart/27000/8719323039117/"],
    "bsl_4002626880574": ["Beslist.nl prijsvergelijking: Aco ShowerDrain C douchegoot rvs (3 aanbieders)",
        "https://www.beslist.nl/p/aco-showerdrain-c-douchegoot-roestvaststaal-rechthoekig/27000/4002626880574/"],
    "bsl_5420056905596": ["Beslist.nl prijsvergelijking: I-Drain Pro Linear 54 douchegoot rvs 600 mm (3 aanbieders)",
        "https://www.beslist.nl/p/i-drain-pro-linear-54-douchegoot-rvs-600-mm/27000/5420056905596/"],
    "bsl_5420056905619": ["Beslist.nl prijsvergelijking: I-Drain Pro Linear 54 douchegoot zonder rooster 800 mm (3 aanbieders)",
        "https://www.beslist.nl/p/idrain-pro-linear-54-douchegoot-zonder-rooster-800-mm-waterdichtingsdoek-330-mm/27000/5420056905619/"],
    "bsl_ovz_easy_drain": ["Beslist.nl overzicht Easy Drain (meerdere aanbieders)",
        "https://www.beslist.nl/products/main_sanitair/r/easy_drain/"],
    "bsl_ovz_aco_showerdrain": ["Beslist.nl overzicht Aco ShowerDrain (150 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/aco_showerdrain/"],
    "bsl_ovz_wiesbaden_douchegoot": ["Beslist.nl overzicht Wiesbaden douchegoot (336 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/wiesbaden_douchegoot/"],
    "bsl_8720847408723": ["Beslist.nl prijsvergelijking: Wiesbaden Less inloopdouche 120x200 cm 8 mm helder glas chroom (4 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-less-inloopdouche-120x200-cm-8-mm-helder-glas-chroom/27000/8720847408723/"],
    "bsl_8720847404985": ["Beslist.nl prijsvergelijking: Wiesbaden Slim inloopdouche 90x200 cm brons rookglas 8 mm (6 aanbieders)",
        "https://www.beslist.nl/p/inloopdouche-wiesbaden-slim-brons-rookglas-90x200-8mm-nano-coating/27000/8720847404985/"],
    "bsl_8718053679051": ["Beslist.nl prijsvergelijking: Wiesbaden Comfort inloopdouche 130x200 cm helder glas chroom (5 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-comfort-inloopdouche-helder-glas-chroom/27000/8718053679051/"],
    "bsl_8717821384852": ["Beslist.nl prijsvergelijking: Sealskin I AM zijwand 90x200 cm chroom (3 aanbieders)",
        "https://www.beslist.nl/p/sealskin-i-am-zijwand-chroom-zilver-90x200-cm/27000/8717821384852/"],
    "bsl_ovz_wiesbaden_inloopdouche": ["Beslist.nl overzicht Wiesbaden inloopdouche (448 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/wiesbaden_inloopdouche/"],
    "bsl_8719956087356": ["Beslist.nl prijsvergelijking: Wiesbaden Hoekinstap douchecabine hoekinstap 90x90x200 8 mm mat zwart (5 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-douchecabine-hoekinstap-90x90x200-cm-8-mm-helder-glas-mat-zwart/27000/8719956087356/"],
    "bsl_8718858072057": ["Beslist.nl prijsvergelijking: Wiesbaden Sydney kwartronde douchecabine 90x200 2 deuren (8 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-kwartrond-douchecabine-90x200cm-met-2-deurtjes-sydney/27000/8718858072057/"],
    "bsl_8718503678351": ["Beslist.nl prijsvergelijking: Wiesbaden Single douchecabine draaideur 90x90 chroom (9 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-single-douchecabine-draaideur-chroom-veiligheidsglas/27000/8718503678351/"],
    "bsl_8719323030978": ["Beslist.nl prijsvergelijking: Wiesbaden Kwartrond douchecabine kwartrond 90x90x190 helder glas (6 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-douchecabine-kwartrond-helder-glas-90x90x190-cm/27000/8719323030978/"],
    "bsl_8720195543619": ["Beslist.nl prijsvergelijking: Wiesbaden Uni douchecabine 90x90 mat zwart swingdeur (7 aanbieders)",
        "https://www.beslist.nl/p/wiesbaden-uni-douchecabine-mat-zwart-veiligheidsglas/27000/8720195543619/"],
    "bsl_8720314711479": ["Beslist.nl prijsvergelijking: Sealskin Hooked douchecabine kwartrond 90x90 schuifdeuren chroom (4 aanbieders)",
        "https://www.beslist.nl/p/sealskin-hooked-douchecabine-kwartrond-90x90-met-schuifdeuren-chroom/27000/8720314711479/"],
    "bsl_ovz_sealskin": ["Beslist.nl overzicht Sealskin douchewand (194 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/sealskin_douchewand/"],
    "bsl_8717821437183": ["Beslist.nl prijsvergelijking: Sealskin Fusion douchebak vierkant 90x90 inbouw wit (3 aanbieders)",
        "https://www.beslist.nl/p/sealskin-fusion-douchebak-vierkant-inbouw-wit/27000/8717821437183/"],
    "bsl_8014140492672": ["Beslist.nl prijsvergelijking: Ideal Standard Ultra Flat S i.life douchebak 90x90x3 carrara wit (3 aanbieders)",
        "https://www.beslist.nl/p/ideal-standard-ultra-flat-s-i-life-douchebak-vierkant-900x900x30-mm-met-afvoerdeksel-in-carrara-wit/27000/8014140492672/"],
    "bsl_8717821437152": ["Beslist.nl prijsvergelijking: Sealskin Fusion douchebak opbouw kwartrond 90x90 wit (3 aanbieders)",
        "https://www.beslist.nl/p/sealskin-fusion-douchebak-opbouw-wit-kwartrond-90x90-cm/27000/8717821437152/"],
    "bsl_4051202851682": ["Beslist.nl prijsvergelijking: Villeroy & Boch Squaro Infinity douchebak 120x90 Quaryl wit (4 aanbieders)",
        "https://www.beslist.nl/p/villeroy-boch-squaro-infinity-douchebak-wit-quaryl-120-x-90-cm/27000/4051202851682/"],
    "bsl_ovz_vb_douchebak": ["Beslist.nl overzicht Villeroy & Boch douchebak (817 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/villeroy_boch_douchebak/"],
    "bsl_ovz_is_douchebak": ["Beslist.nl overzicht Ideal Standard douchebak (331 resultaten)",
        "https://www.beslist.nl/products/main_sanitair/r/douchebak_ideal_standard/"],
}
