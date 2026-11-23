"""Productdata sanitair voor de offertevergelijker van Top Badkamers.

Methode
- Peildatum: november 2026 (verzameld op 23-11-2026).
- Per artikel is de productpagina van een prijsvergelijker bekeken (Beslist.nl,
  voor een artikel Kieskeurig.nl). `van` is de laagste en `tot` de hoogste
  actuele prijs bij de aanbieders op die pagina, incl. 21% btw, zonder
  verzendkosten en zonder montage. `van` is naar beneden en `tot` naar boven
  afgerond op hele euro's.
- Alleen artikelen met minstens 3 aanbieders zijn opgenomen.
- `ean` staat er alleen in als hij letterlijk op de bronpagina stond (in de
  productgegevens en in de URL van de vergelijker) en past bij het merk. Bij
  twijfel (EAN-prefix past niet bij het merk) is `ean` leeg gelaten.
- `codes` (artikelnummers van de fabrikant) staan er alleen in als ze letterlijk
  in de producttitel of de productgegevens van de bron stonden. Daarom is
  `codes` vaak leeg; herkenning gaat dan via EAN of serie.
- Wastafelmeubels en spiegelkasten hebben weinig vaste artikelnummers; die
  zijn vastgelegd met merk en serie.
- Webwinkelprijzen zijn geen installateursprijzen: een installateur rekent vaak
  een opslag voor garantie, risico en levering.
- Bronnen noemen alleen de prijsvergelijker, geen winkels.
"""

ARTIKELEN = [
    # --- Bedieningsplaten ---
    # bron: Beslist, 9 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma01", "oms": "Bedieningsplaat 2-toets, edelmessing", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025410035219"], "van": 188, "tot": 413, "bron": "vgl_beslist_4025410035219"},
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma01", "oms": "Bedieningsplaat 2-toets, glans chroom/mat chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025410035271"], "van": 69, "tot": 138, "bron": "vgl_beslist_4025410035271"},
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma20", "oms": "Bedieningsplaat 2-toets, wit/glans chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416544562"], "van": 54, "tot": 109, "bron": "vgl_beslist_4025416544562"},
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma20", "oms": "Bedieningsplaat 2-toets, zwart/chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416544654"], "van": 68, "tot": 186, "bron": "vgl_beslist_4025416544654"},
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma20", "oms": "Bedieningsplaat 2-toets, mat zwart", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416709176"], "van": 110, "tot": 154, "bron": "vgl_beslist_4025416709176"},
    # bron: Beslist, 10 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma20", "oms": "Bedieningsplaat 2-toets, mat wit", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025410635563"], "van": 110, "tot": 235, "bron": "vgl_beslist_4025410635563"},
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma20", "oms": "Bedieningsplaat 2-toets, RVS-look", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416544937"], "van": 142, "tot": 260, "bron": "vgl_beslist_4025416544937"},
    # bron: Beslist, 9 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Sigma20", "oms": "Bedieningsplaat 2-toets, chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416544555"], "van": 87, "tot": 120, "bron": "vgl_beslist_4025416544555"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Delta21", "oms": "Bedieningsplaat 2-toets, wit", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416708636"], "van": 39, "tot": 74, "bron": "vgl_beslist_4025416708636"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Delta25", "oms": "Bedieningsplaat 2-toets, mat chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416709138"], "van": 35, "tot": 119, "bron": "vgl_beslist_4025416709138"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Delta25", "oms": "Bedieningsplaat 2-toets, wit", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416709510"], "van": 48, "tot": 71, "bron": "vgl_beslist_4025416709510"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Delta50", "oms": "Bedieningsplaat 2-toets, wit", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025416511427"], "van": 55, "tot": 149, "bron": "vgl_beslist_4025416511427"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Delta50", "oms": "Bedieningsplaat 2-toets, glans chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4025410653178"], "van": 41, "tot": 119, "bron": "vgl_beslist_4025410653178"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Solido", "oms": "Bedieningsplaat 2-toets, wit", "categorie": "bedieningsplaat", "codes": [], "ean": ["4005176914522"], "van": 35, "tot": 106, "bron": "vgl_beslist_4005176914522"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Solido", "oms": "Bedieningsplaat 2-toets, chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4005176914515"], "van": 56, "tot": 124, "bron": "vgl_beslist_4005176914515"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Rapid SL", "oms": "Bedieningsplaat 2-toets, chroom", "categorie": "bedieningsplaat", "codes": [], "ean": ["4005176835469"], "van": 67, "tot": 93, "bron": "vgl_beslist_4005176835469"},
    # --- Inbouwreservoirs ---
    # bron: Kieskeurig, 4 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Duofix UP100", "oms": "Duofix Basic inbouwreservoir UP100 (Delta), 112 cm", "categorie": "inbouwreservoir", "codes": ["458.103.00.1"], "ean": ["4025416758877"], "van": 154, "tot": 279, "bron": "vgl_kieskeurig_4025416758877"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Duofix", "oms": "Duofix element voor wandcloset met inbouwreservoir, incl. isolatiemat", "categorie": "inbouwreservoir", "codes": [], "ean": ["4025410591913"], "van": 224, "tot": 264, "bron": "vgl_beslist_4025410591913"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Duofix UP720", "oms": "Duofix element met Sigma inbouwreservoir UP720 (8 cm), incl. geluidsisolatieset", "categorie": "inbouwreservoir", "codes": [], "ean": ["4064746031212"], "van": 270, "tot": 318, "bron": "vgl_beslist_4064746031212"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Rapid SL", "oms": "Rapid SL installatiesysteem voor hangtoilet, 1,00 m", "categorie": "inbouwreservoir", "codes": [], "ean": ["4005176863967"], "van": 275, "tot": 440, "bron": "vgl_beslist_4005176863967"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Rapid SL", "oms": "Rapid SL wc-element incl. bedieningsplaat chroom", "categorie": "inbouwreservoir", "codes": [], "ean": ["4005176863431"], "van": 236, "tot": 344, "bron": "vgl_beslist_4005176863431"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Rapid SL", "oms": "Rapid SL inbouwreservoir voor hangtoilet, extra laag", "categorie": "inbouwreservoir", "codes": [], "ean": ["4005176291050"], "van": 203, "tot": 269, "bron": "vgl_beslist_4005176291050"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Solido", "oms": "Solido inbouwreservoir voor hangtoilet", "categorie": "inbouwreservoir", "codes": [], "ean": ["4005176915758"], "van": 124, "tot": 204, "bron": "vgl_beslist_4005176915758"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Solido", "oms": "Solido 4-in-1 set: inbouwreservoir, bedieningsplaat chroom, geluidsisolatie, wandhoeken", "categorie": "inbouwreservoir", "codes": ["39930000"], "ean": ["4005176728105"], "van": 180, "tot": 201, "bron": "vgl_beslist_4005176728105"},
    # --- Hangtoiletten ---
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Wandcloset, wit (zonder zitting)", "categorie": "hangtoilet", "codes": [], "ean": ["4051202219598"], "van": 294, "tot": 341, "bron": "vgl_beslist_4051202219598"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Wandcloset diepspoel, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4047289521587"], "van": 275, "tot": 438, "bron": "vgl_beslist_4047289521587"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Wandcloset compact DirectFlush, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4051202346171"], "van": 292, "tot": 462, "bron": "vgl_beslist_4051202346171"},
    # bron: Beslist, 9 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 3.0", "oms": "Wandcloset randloos, glanzend wit", "categorie": "hangtoilet", "codes": [], "ean": ["4062373882092"], "van": 379, "tot": 605, "bron": "vgl_beslist_4062373882092"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Wandcloset compact, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4051202219512"], "van": 158, "tot": 299, "bron": "vgl_beslist_4051202219512"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Wandcloset verkort 49 cm, TwistFlush, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4062373945452"], "van": 225, "tot": 329, "bron": "vgl_beslist_4062373945452"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Combipack wandcloset diepspoel met zitting, CeramicPlus, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4051202219529"], "van": 270, "tot": 330, "bron": "vgl_beslist_4051202219529"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Architectura", "oms": "Wandclosetpack randloos met softclose-zitting, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4065467455936"], "van": 279, "tot": 359, "bron": "vgl_beslist_4065467455936"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Tesi", "oms": "Wandcloset, wit", "categorie": "hangtoilet", "codes": [], "ean": ["8014140435228"], "van": 174, "tot": 190, "bron": "vgl_beslist_8014140435228"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Tesi", "oms": "Wandcloset AquaBlade, mat wit", "categorie": "hangtoilet", "codes": [], "ean": ["8014140457367"], "van": 419, "tot": 578, "bron": "vgl_beslist_8014140457367"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Connect", "oms": "Wandcloset, wit", "categorie": "hangtoilet", "codes": [], "ean": ["5017830448754"], "van": 133, "tot": 277, "bron": "vgl_beslist_5017830448754"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Connect", "oms": "Wandcloset AquaBlade met softclose-zitting", "categorie": "hangtoilet", "codes": [], "ean": ["4015413027861"], "van": 316, "tot": 608, "bron": "vgl_beslist_4015413027861"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Starck 3", "oms": "Wandcloset pack met softclose-zitting, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4053424087627"], "van": 270, "tot": 655, "bron": "vgl_beslist_4053424087627"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Starck 3", "oms": "Wandcloset diepspoel, wit", "categorie": "hangtoilet", "codes": ["2202090000"], "ean": ["4021534223679"], "van": 234, "tot": 288, "bron": "vgl_beslist_4021534223679"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "iCon", "oms": "Wandclosetset randloos TurboFlush met softclose-zitting, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4064746019869"], "van": 394, "tot": 509, "bron": "vgl_beslist_4064746019869"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "ONE", "oms": "Wandcloset randloos TurboFlush, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4025416301653"], "van": 502, "tot": 643, "bron": "vgl_beslist_4025416301653"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Acanto", "oms": "Wandcloset randloos TurboFlush, glanzend wit", "categorie": "hangtoilet", "codes": [], "ean": ["4025410733115"], "van": 375, "tot": 704, "bron": "vgl_beslist_4025410733115"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Renova", "oms": "Wandcloset diepspoel 54 cm, wit", "categorie": "hangtoilet", "codes": [], "ean": ["4022009285055"], "van": 111, "tot": 164, "bron": "vgl_beslist_4022009285055"},
    # --- Staande toiletten ---
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Renova", "oms": "Staand toilet randloos, 54 cm", "categorie": "staand_toilet", "codes": [], "ean": ["4025410572998"], "van": 154, "tot": 284, "bron": "vgl_beslist_4025410572998"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Duoblokpot, wit (zonder reservoir)", "categorie": "staand_toilet", "codes": [], "ean": ["4051202324308"], "van": 226, "tot": 259, "bron": "vgl_beslist_4051202324308"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Staande toiletpot diepspoel, wit (zonder zitting)", "categorie": "staand_toilet", "codes": [], "ean": ["4051202032562"], "van": 113, "tot": 149, "bron": "vgl_beslist_4051202032562"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "No.1", "oms": "Duoblokpot, wit (zonder reservoir)", "categorie": "staand_toilet", "codes": [], "ean": ["4063382318510"], "van": 239, "tot": 312, "bron": "vgl_beslist_4063382318510"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "No.1", "oms": "Duoblokreservoir 6 l, dual flush, wit", "categorie": "staand_toilet", "codes": [], "ean": ["4053424507637"], "van": 94, "tot": 173, "bron": "vgl_beslist_4053424507637"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Plieger", "serie": "Smart/Classic", "oms": "Staande toiletpot diepspoel PK, wit", "categorie": "staand_toilet", "codes": [], "ean": [], "van": 65, "tot": 121, "bron": "vgl_beslist_4014804741065"},
    # --- Toiletzittingen ---
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Closetzitting met softclose en quickrelease, wit", "categorie": "toiletzitting", "codes": [], "ean": ["4051202033705"], "van": 101, "tot": 151, "bron": "vgl_beslist_4051202033705"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Closetzitting SlimSeat, wit", "categorie": "toiletzitting", "codes": [], "ean": ["4051202264116"], "van": 116, "tot": 182, "bron": "vgl_beslist_4051202264116"},
    # bron: Beslist, 9 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Closetzitting, wit alpin", "categorie": "toiletzitting", "codes": [], "ean": ["4051202073275"], "van": 111, "tot": 202, "bron": "vgl_beslist_4051202073275"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Closetzitting met quickrelease, wit", "categorie": "toiletzitting", "codes": [], "ean": ["4051202033897"], "van": 121, "tot": 179, "bron": "vgl_beslist_4051202033897"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Architectura", "oms": "Closetzitting met softclose, wit", "categorie": "toiletzitting", "codes": [], "ean": ["4051202374648"], "van": 153, "tot": 196, "bron": "vgl_beslist_4051202374648"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Starck 3", "oms": "Closetzitting met softclose en quickrelease, wit", "categorie": "toiletzitting", "codes": [], "ean": ["4021534386190"], "van": 94, "tot": 128, "bron": "vgl_beslist_4021534386190"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Starck 3", "oms": "Closetzitting, wit (zonder softclose)", "categorie": "toiletzitting", "codes": [], "ean": ["4021534224171"], "van": 71, "tot": 91, "bron": "vgl_beslist_4021534224171"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Tesi", "oms": "Closetzitting met deksel en softclose, wit", "categorie": "toiletzitting", "codes": [], "ean": ["8014140430315"], "van": 77, "tot": 150, "bron": "vgl_beslist_8014140430315"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Tesi", "oms": "Closetzitting met softclose, RVS-scharnieren, wit", "categorie": "toiletzitting", "codes": [], "ean": ["8014140515098"], "van": 83, "tot": 100, "bron": "vgl_beslist_8014140515098"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Ideal Standard", "serie": "Connect", "oms": "Closetzitting met softclose, wit", "categorie": "toiletzitting", "codes": [], "ean": ["5017830474807"], "van": 65, "tot": 177, "bron": "vgl_beslist_5017830474807"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "Renova", "oms": "Closetzitting D-vorm, wit", "categorie": "toiletzitting", "codes": [], "ean": ["4025410726025"], "van": 89, "tot": 125, "bron": "vgl_beslist_4025410726025"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Pressalit", "serie": "T2", "oms": "Closetzitting met softclose, wit", "categorie": "toiletzitting", "codes": [], "ean": ["5708590299839"], "van": 96, "tot": 162, "bron": "vgl_beslist_5708590299839"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Pressalit", "serie": "", "oms": "Closetzitting met RVS-scharnieren, wit", "categorie": "toiletzitting", "codes": ["776000-DA9999"], "ean": ["5708590318233"], "van": 44, "tot": 143, "bron": "vgl_beslist_5708590318233"},
    # --- Fonteinen ---
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Fontein, wit", "categorie": "fontein", "codes": [], "ean": ["4062373785218"], "van": 73, "tot": 99, "bron": "vgl_beslist_4062373785218"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Fontein, wit", "categorie": "fontein", "codes": [], "ean": ["4047289972020"], "van": 133, "tot": 190, "bron": "vgl_beslist_4047289972020"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Collaro", "oms": "Fontein 50x40 cm, wit", "categorie": "fontein", "codes": [], "ean": ["4051202918231"], "van": 198, "tot": 214, "bron": "vgl_beslist_4051202918231"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Starck 3", "oms": "Fontein / handwasbak, wit", "categorie": "fontein", "codes": [], "ean": ["4021534536243"], "van": 86, "tot": 140, "bron": "vgl_beslist_4021534536243"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Vero Air", "oms": "Fontein, glanzend wit", "categorie": "fontein", "codes": [], "ean": ["4053424509327"], "van": 182, "tot": 248, "bron": "vgl_beslist_4053424509327"},
    # --- Wastafels ---
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Subway 2.0", "oms": "Wastafel 80x47 cm, wit", "categorie": "wastafel", "codes": [], "ean": ["4047289980223"], "van": 373, "tot": 536, "bron": "vgl_beslist_4047289980223"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Wastafel klein formaat, wit", "categorie": "wastafel", "codes": [], "ean": ["4062373755990"], "van": 105, "tot": 146, "bron": "vgl_beslist_4062373755990"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "O.novo", "oms": "Onderbouwwastafel 53x32 cm, wit", "categorie": "wastafel", "codes": [], "ean": ["4051202110338"], "van": 119, "tot": 229, "bron": "vgl_beslist_4051202110338"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "D-Neo", "oms": "Wastafel, hoogglans wit", "categorie": "wastafel", "codes": [], "ean": ["4053424981918"], "van": 129, "tot": 158, "bron": "vgl_beslist_4053424981918"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "Happy D.2", "oms": "Opbouwwastafel geslepen, wit", "categorie": "wastafel", "codes": [], "ean": ["4021534843495"], "van": 304, "tot": 389, "bron": "vgl_beslist_4021534843495"},
    # --- Wastafelmeubels ---
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Cersanit", "serie": "Lara", "oms": "Hangend badmeubel 60 cm met wastafel, wit", "categorie": "wastafelmeubel", "codes": [], "ean": ["5902115729133"], "van": 148, "tot": 250, "bron": "vgl_beslist_5902115729133"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Boss & Wessing", "serie": "Aleco", "oms": "Wastafelonderkast 80 cm, 2 deuren, wit (zonder wastafel)", "categorie": "wastafelmeubel", "codes": [], "ean": ["5404024112421"], "van": 97, "tot": 219, "bron": "vgl_beslist_5404024112421"},
    # --- Spiegelkasten ---
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Differnz", "serie": "Topas", "oms": "Spiegelkast 3 deuren met verlichting, wit", "categorie": "spiegel_kast", "codes": [], "ean": [], "van": 102, "tot": 175, "bron": "vgl_beslist_4013251201023"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Differnz", "serie": "", "oms": "Spiegelkast 45x15x35 cm, wit", "categorie": "spiegel_kast", "codes": [], "ean": [], "van": 54, "tot": 69, "bron": "vgl_beslist_4013251201139"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Wiesbaden", "serie": "", "oms": "Spiegelkast aluminium met ledverlichting, 120 cm", "categorie": "spiegel_kast", "codes": [], "ean": ["8719323030213"], "van": 426, "tot": 659, "bron": "vgl_beslist_8719323030213"},
    # --- Baden ---
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Lazy", "oms": "Ligbad 170x75 cm, acryl wit", "categorie": "bad", "codes": [], "ean": ["8714148593509"], "van": 398, "tot": 506, "bron": "vgl_beslist_8714148593509"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Linares", "oms": "Ligbad 170x75 cm, acryl wit", "categorie": "bad", "codes": [], "ean": ["8714148547984"], "van": 458, "tot": 736, "bron": "vgl_beslist_8714148547984"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Still Square", "oms": "Ligbad 170x75 cm, wit", "categorie": "bad", "codes": [], "ean": ["8714148571125"], "van": 610, "tot": 854, "bron": "vgl_beslist_8714148571125"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Columbia", "oms": "Inbouwbad 140x70 cm, acryl wit", "categorie": "bad", "codes": [], "ean": ["8714148357071"], "van": 383, "tot": 560, "bron": "vgl_beslist_8714148357071"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Yukon", "oms": "Inbouw hoekbad (groot formaat), acryl wit", "categorie": "bad", "codes": [], "ean": ["8714148065419"], "van": 548, "tot": 728, "bron": "vgl_beslist_8714148065419"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Winnipeg", "oms": "Hoekbad (groot formaat), acryl wit", "categorie": "bad", "codes": [], "ean": ["8714148315057"], "van": 672, "tot": 885, "bron": "vgl_beslist_8714148315057"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Xenz", "serie": "Society", "oms": "Inbouw ligbad 170x75 cm, acryl pergamon", "categorie": "bad", "codes": [], "ean": ["8720247010748"], "van": 710, "tot": 798, "bron": "vgl_beslist_8720247010748"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Xenz", "serie": "Madeira", "oms": "Ligbad 170x75 cm met badpoten, mat wit", "categorie": "bad", "codes": [], "ean": ["8720247190716"], "van": 763, "tot": 858, "bron": "vgl_beslist_8720247190716"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Duravit", "serie": "No.1", "oms": "Inbouwbad trapezium 150x80 cm, wit", "categorie": "bad", "codes": [], "ean": ["4063382185495"], "van": 271, "tot": 565, "bron": "vgl_beslist_4063382185495"},
    # --- Vrijstaande baden ---
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Villeroy & Boch", "serie": "Loop & Friends", "oms": "Half vrijstaand bad 180x80 cm, acryl wit alpin", "categorie": "vrijstaand_bad", "codes": [], "ean": ["4062373899779"], "van": 1537, "tot": 1703, "bron": "vgl_beslist_4062373899779"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Best Design", "serie": "Double Slip", "oms": "Vrijstaand bad 175x72 cm, dubbelwandig acryl wit", "categorie": "vrijstaand_bad", "codes": [], "ean": ["8718274538403"], "van": 867, "tot": 975, "bron": "vgl_beslist_8718274538403"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Creavit", "serie": "Antik", "oms": "Vrijstaand bad 160x79 cm, acryl wit, met waste", "categorie": "vrijstaand_bad", "codes": [], "ean": [], "van": 1179, "tot": 1518, "bron": "vgl_beslist_8590913978654"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Arcqua", "serie": "Santo", "oms": "Vrijstaand bad 178x80 cm, acryl glans wit", "categorie": "vrijstaand_bad", "codes": [], "ean": ["8720104404239"], "van": 1458, "tot": 1639, "bron": "vgl_beslist_8720104404239"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Riho", "serie": "Valor", "oms": "Half vrijstaand bad 180x80 cm, solid surface mat wit", "categorie": "vrijstaand_bad", "codes": [], "ean": ["8714148593905"], "van": 3155, "tot": 4012, "bron": "vgl_beslist_8714148593905"},
    # --- Badkamerradiatoren ---
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Plieger", "serie": "Quadro", "oms": "Designradiator wit, 307 W (695x500 mm)", "categorie": "badkamerradiator", "codes": [], "ean": ["8711238071510"], "van": 86, "tot": 98, "bron": "vgl_beslist_8711238071510"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Plieger", "serie": "Quadro", "oms": "Designradiator wit, 627 W", "categorie": "badkamerradiator", "codes": [], "ean": ["8711238071527"], "van": 130, "tot": 143, "bron": "vgl_beslist_8711238071527"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Plieger", "serie": "Quadro", "oms": "Designradiator wit, 886 W", "categorie": "badkamerradiator", "codes": [], "ean": ["8711238071534"], "van": 110, "tot": 175, "bron": "vgl_beslist_8711238071534"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Plieger", "serie": "Cavallino Retto", "oms": "Designradiator wit, 817 W, 180x29,8 cm, middenaansluiting", "categorie": "badkamerradiator", "codes": [], "ean": ["8711238248172"], "van": 404, "tot": 630, "bron": "vgl_beslist_8711238248172"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Florion", "serie": "Nxt", "oms": "Designradiator dubbel wit, 140,6x60 cm", "categorie": "badkamerradiator", "codes": [], "ean": ["8711238365022"], "van": 451, "tot": 627, "bron": "vgl_beslist_8711238365022"},
    # bron: Beslist, 3 aanbieders, nov 2026
    {"merk": "Haceka", "serie": "Gobi Adoria", "oms": "Designradiator zwart", "categorie": "badkamerradiator", "codes": [], "ean": ["8718315060047"], "van": 105, "tot": 134, "bron": "vgl_beslist_8718315060047"},
    # bron: Beslist, 8 aanbieders, nov 2026
    {"merk": "Eurom", "serie": "Sani Towel", "oms": "Elektrische handdoekradiator 750 W, wit", "categorie": "badkamerradiator", "codes": [], "ean": ["8713415352474"], "van": 166, "tot": 229, "bron": "vgl_beslist_8713415352474"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Sanigoods", "serie": "Calgary", "oms": "Handdoekradiator 50x180 cm, 936 W, wit", "categorie": "badkamerradiator", "codes": [], "ean": ["5404029156505"], "van": 217, "tot": 273, "bron": "vgl_beslist_5404029156505"},
    # bron: Beslist, 5 aanbieders, nov 2026
    {"merk": "Callista", "serie": "", "oms": "Staafhanddoekradiator 150 cm, mat zwart", "categorie": "badkamerradiator", "codes": [], "ean": ["8720847407245"], "van": 140, "tot": 179, "bron": "vgl_beslist_8720847407245"},
    # --- Accessoires ---
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Essentials", "oms": "Toiletrolhouder, chroom", "categorie": "accessoires", "codes": [], "ean": ["4005176326240"], "van": 23, "tot": 56, "bron": "vgl_beslist_4005176326240"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Essentials", "oms": "Reserverolhouder, chroom", "categorie": "accessoires", "codes": [], "ean": ["4005176326356"], "van": 23, "tot": 56, "bron": "vgl_beslist_4005176326356"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Essentials", "oms": "Handdoekhouder, chroom", "categorie": "accessoires", "codes": [], "ean": ["4005176326288"], "van": 34, "tot": 62, "bron": "vgl_beslist_4005176326288"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Essentials", "oms": "Handdoekhaak rond, chroom", "categorie": "accessoires", "codes": [], "ean": ["4005176326332"], "van": 12, "tot": 31, "bron": "vgl_beslist_4005176326332"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Essentials", "oms": "Zeepdispenser 160 ml, chroom", "categorie": "accessoires", "codes": [], "ean": ["4005176326233"], "van": 18, "tot": 46, "bron": "vgl_beslist_4005176326233"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Grohe", "serie": "Essentials", "oms": "Accessoireset (rolhouder, toiletborstel, haak), supersteel", "categorie": "accessoires", "codes": [], "ean": ["4005176413179"], "van": 139, "tot": 229, "bron": "vgl_beslist_4005176413179"},
    # bron: Beslist, 7 aanbieders, nov 2026
    {"merk": "Geberit", "serie": "DuoFresh", "oms": "Stickhouder voor inbouwreservoir, glans chroom", "categorie": "accessoires", "codes": [], "ean": ["4025416351221"], "van": 48, "tot": 159, "bron": "vgl_beslist_4025416351221"},
    # bron: Beslist, 4 aanbieders, nov 2026
    {"merk": "Wiesbaden", "serie": "Alonzo", "oms": "Vrijstaande toiletborstel met houder, chroom", "categorie": "accessoires", "codes": [], "ean": ["8720847406316"], "van": 34, "tot": 46, "bron": "vgl_beslist_8720847406316"},
    # bron: Beslist, 6 aanbieders, nov 2026
    {"merk": "Wiesbaden", "serie": "", "oms": "Dubbele toiletrolhouder met plankje, mat zwart", "categorie": "accessoires", "codes": [], "ean": ["8719956085413"], "van": 127, "tot": 159, "bron": "vgl_beslist_8719956085413"},
]

BRONNEN = {
    "vgl_beslist_4025410035219": ["Beslist.nl prijsvergelijking: Geberit Sigma01 bedieningsplaat 2-toets (9 aanbieders)", "https://www.beslist.nl/p/geberit-sigma01-bedieningsplaat-edelmessing-2-toets-spoeling/27000/4025410035219/"],
    "vgl_beslist_4025410035271": ["Beslist.nl prijsvergelijking: Geberit Sigma01 bedieningsplaat 2-toets (8 aanbieders)", "https://www.beslist.nl/p/geberit-sigma01-bedieningsplaat-glans-chroom-mat-chroom/27000/4025410035271/"],
    "vgl_beslist_4025416544562": ["Beslist.nl prijsvergelijking: Geberit Sigma20 bedieningsplaat 2-toets (8 aanbieders)", "https://www.beslist.nl/p/geberit-sigma20-bedieningsplaat-wit-glansverchroomd/27000/4025416544562/"],
    "vgl_beslist_4025416544654": ["Beslist.nl prijsvergelijking: Geberit Sigma20 bedieningsplaat 2-toets (8 aanbieders)", "https://www.beslist.nl/p/geberit-sigma20-bedieningsplaat-zwart-chroom/27000/4025416544654/"],
    "vgl_beslist_4025416709176": ["Beslist.nl prijsvergelijking: Geberit Sigma20 bedieningsplaat 2-toets (8 aanbieders)", "https://www.beslist.nl/p/geberit-sigma20-bedieningsplaat-matzwart-2-toets-spoeling/27000/4025416709176/"],
    "vgl_beslist_4025410635563": ["Beslist.nl prijsvergelijking: Geberit Sigma20 bedieningsplaat 2-toets (10 aanbieders)", "https://www.beslist.nl/p/geberit-sigma20-bedieningsplaat-matwit-2-toets-spoeling/27000/4025410635563/"],
    "vgl_beslist_4025416544937": ["Beslist.nl prijsvergelijking: Geberit Sigma20 bedieningsplaat 2-toets (8 aanbieders)", "https://www.beslist.nl/p/geberit-sigma20-bedieningsplaat-rvs-look/27000/4025416544937/"],
    "vgl_beslist_4025416544555": ["Beslist.nl prijsvergelijking: Geberit Sigma20 bedieningsplaat 2-toets (9 aanbieders)", "https://www.beslist.nl/p/geberit-sigma-20-bedieningsplaat-chroom/27000/4025416544555/"],
    "vgl_beslist_4025416708636": ["Beslist.nl prijsvergelijking: Geberit Delta21 bedieningsplaat 2-toets (3 aanbieders)", "https://www.beslist.nl/p/geberit-delta-21-bedieningspaneel-wit/27000/4025416708636/"],
    "vgl_beslist_4025416709138": ["Beslist.nl prijsvergelijking: Geberit Delta25 bedieningsplaat 2-toets (5 aanbieders)", "https://www.beslist.nl/p/geberit-delta-25-bedieningsplaat-mat-chroom/27000/4025416709138/"],
    "vgl_beslist_4025416709510": ["Beslist.nl prijsvergelijking: Geberit Delta25 bedieningsplaat 2-toets (4 aanbieders)", "https://www.beslist.nl/p/geberit-delta-25-drukplaat-wit-frontbediening/27000/4025416709510/"],
    "vgl_beslist_4025416511427": ["Beslist.nl prijsvergelijking: Geberit Delta50 bedieningsplaat 2-toets (4 aanbieders)", "https://www.beslist.nl/p/geberit-delta-50-drukplaat-wit-kunststof/27000/4025416511427/"],
    "vgl_beslist_4025410653178": ["Beslist.nl prijsvergelijking: Geberit Delta50 bedieningsplaat 2-toets (3 aanbieders)", "https://www.beslist.nl/p/geberit-delta50-bedieningsplaat-glans-chroom-2-toets-spoeling/27000/4025410653178/"],
    "vgl_beslist_4005176914522": ["Beslist.nl prijsvergelijking: Grohe Solido bedieningsplaat 2-toets (7 aanbieders)", "https://www.beslist.nl/p/grohe-solido-bedieningspaneel-wit-dual-flush-2-knops/27000/4005176914522/"],
    "vgl_beslist_4005176914515": ["Beslist.nl prijsvergelijking: Grohe Solido bedieningsplaat 2-toets (5 aanbieders)", "https://www.beslist.nl/p/grohe-solido-bedieningsplaat-chroom/27000/4005176914515/"],
    "vgl_beslist_4005176835469": ["Beslist.nl prijsvergelijking: Grohe Rapid SL bedieningsplaat 2-toets (3 aanbieders)", "https://www.beslist.nl/p/grohe-rapid-sl-bedieningsplaat-chroom-abs-voor-dual-flush/27000/4005176835469/"],
    "vgl_kieskeurig_4025416758877": ["Kieskeurig.nl prijsvergelijking: Geberit Duofix UP100 duofix basic inbouwreservoir up100 (delta) (4 aanbieders)", "https://www.kieskeurig.nl/waterleiding/product/4050897-geberit-wand-wc-montage-element-duofix-basic-up100"],
    "vgl_beslist_4025410591913": ["Beslist.nl prijsvergelijking: Geberit Duofix duofix element voor wandcloset met inbouwreservoir (3 aanbieders)", "https://www.beslist.nl/p/geberit-duofix-inbouwspoelreservoir-inclusief-isolatiemat-110-90-reductiering/27000/4025410591913/"],
    "vgl_beslist_4064746031212": ["Beslist.nl prijsvergelijking: Geberit Duofix UP720 duofix element met sigma inbouwreservoir up720 (8 cm) (3 aanbieders)", "https://www.beslist.nl/p/geberit-duofix-up720-sigma-inbouwreservoir-wand-wc-ruimtebesparend-geluidsisolatieset/27000/4064746031212/"],
    "vgl_beslist_4005176863967": ["Beslist.nl prijsvergelijking: Grohe Rapid SL rapid sl installatiesysteem voor hangtoilet (4 aanbieders)", "https://www.beslist.nl/p/grohe-rapid-sl-installatiesysteem-hangend-toilet-staal-1-00-m/27000/4005176863967/"],
    "vgl_beslist_4005176863431": ["Beslist.nl prijsvergelijking: Grohe Rapid SL rapid sl wc-element incl. bedieningsplaat chroom (3 aanbieders)", "https://www.beslist.nl/p/grohe-rapid-sl-wc-element-chrome-inclusief-bedieningsplaat/27000/4005176863431/"],
    "vgl_beslist_4005176291050": ["Beslist.nl prijsvergelijking: Grohe Rapid SL rapid sl inbouwreservoir voor hangtoilet (7 aanbieders)", "https://www.beslist.nl/p/grohe-rapid-sl-inbouwreservoir-geschikt-voor-hangend-toilet-extra-laag-stalen-frame/27000/4005176291050/"],
    "vgl_beslist_4005176915758": ["Beslist.nl prijsvergelijking: Grohe Solido solido inbouwreservoir voor hangtoilet (6 aanbieders)", "https://www.beslist.nl/p/grohe-solido-wc-inbouwreservoir-staal-dual-flush-systeem/27000/4005176915758/"],
    "vgl_beslist_4005176728105": ["Beslist.nl prijsvergelijking: Grohe Solido solido 4-in-1 set: inbouwreservoir (3 aanbieders)", "https://www.beslist.nl/p/grohe-solido-4-in-1-set-voor-toilet-incl-bedieningsknop-even-geluidsisolatieset-en-wandhoek-klaar-voor-montage-chroom-39930000/27000/4005176728105/"],
    "vgl_beslist_4051202219598": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 wandcloset (8 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-wandcloset-wit/27000/4051202219598/"],
    "vgl_beslist_4047289521587": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 wandcloset diepspoel (6 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-wandcloset-diepspoel-wit/27000/4047289521587/"],
    "vgl_beslist_4051202346171": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 wandcloset compact directflush (6 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-wandcloset-directflush-compact-wit/27000/4051202346171/"],
    "vgl_beslist_4062373882092": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 3.0 wandcloset randloos (9 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-3-0-hangtoilet-glanzend-wit-porselein-randloos/27000/4062373882092/"],
    "vgl_beslist_4051202219512": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo wandcloset compact (5 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-wandcloset-compact-wit/27000/4051202219512/"],
    "vgl_beslist_4062373945452": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo wandcloset verkort 49 cm (5 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-wandcloset-verkort-49cm-twistflush-e3-wit/27000/4062373945452/"],
    "vgl_beslist_4051202219529": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo combipack wandcloset diepspoel met zitting (3 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-combipack-wandcloset-diepspoel-wit-ceramic/27000/4051202219529/"],
    "vgl_beslist_4065467455936": ["Beslist.nl prijsvergelijking: Villeroy & Boch Architectura wandclosetpack randloos met softclose-zitting (7 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-architectura-wandclosetpack-glans-wit-spoelrandloos-softclose/27000/4065467455936/"],
    "vgl_beslist_8014140435228": ["Beslist.nl prijsvergelijking: Ideal Standard Tesi wandcloset (3 aanbieders)", "https://www.beslist.nl/p/ideal-standard-tesi-hangend-toilet-wit-gehard-keramiek/27000/8014140435228/"],
    "vgl_beslist_8014140457367": ["Beslist.nl prijsvergelijking: Ideal Standard Tesi wandcloset aquablade (3 aanbieders)", "https://www.beslist.nl/p/ideal-standard-tesi-aquablade-wandcloset-mat-wit-inclusief-bevestigingset/27000/8014140457367/"],
    "vgl_beslist_5017830448754": ["Beslist.nl prijsvergelijking: Ideal Standard Connect wandcloset (3 aanbieders)", "https://www.beslist.nl/p/ideal-standard-connect-wandcloset-keramiek-wit/27000/5017830448754/"],
    "vgl_beslist_4015413027861": ["Beslist.nl prijsvergelijking: Ideal Standard Connect wandcloset aquablade met softclose-zitting (3 aanbieders)", "https://www.beslist.nl/p/ideal-standard-connect-wandcloset-aqua-blade-softclose-zitting/27000/4015413027861/"],
    "vgl_beslist_4053424087627": ["Beslist.nl prijsvergelijking: Duravit Starck 3 wandcloset pack met softclose-zitting (6 aanbieders)", "https://www.beslist.nl/p/duravit-starck-3-wandcloset-pack-wit-keramiek-softclose-zitting/27000/4053424087627/"],
    "vgl_beslist_4021534223679": ["Beslist.nl prijsvergelijking: Duravit Starck 3 wandcloset diepspoel (3 aanbieders)", "https://www.beslist.nl/p/duravit-starck-3-wandcloset-diepspoel-wit/27000/4021534223679/"],
    "vgl_beslist_4064746019869": ["Beslist.nl prijsvergelijking: Geberit iCon wandclosetset randloos turboflush met softclose-zitting (6 aanbieders)", "https://www.beslist.nl/p/geberit-icon-wandclosetset-glans-wit-diepspoel-rimless-turboflush-softclose/27000/4064746019869/"],
    "vgl_beslist_4025416301653": ["Beslist.nl prijsvergelijking: Geberit ONE wandcloset randloos turboflush (7 aanbieders)", "https://www.beslist.nl/p/geberit-one-wandcloset-wit-keramiek-rimless-met-turboflush/27000/4025416301653/"],
    "vgl_beslist_4025410733115": ["Beslist.nl prijsvergelijking: Geberit Acanto wandcloset randloos turboflush (6 aanbieders)", "https://www.beslist.nl/p/geberit-wandcloset-acanto-rimless-turboflush-keramiek-glanzend-wit/27000/4025410733115/"],
    "vgl_beslist_4022009285055": ["Beslist.nl prijsvergelijking: Geberit Renova wandcloset diepspoel 54 cm (4 aanbieders)", "https://www.beslist.nl/p/geberit-renova-wandcloset-diepspoel-wit-54cm/27000/4022009285055/"],
    "vgl_beslist_4025410572998": ["Beslist.nl prijsvergelijking: Geberit Renova staand toilet randloos (3 aanbieders)", "https://www.beslist.nl/p/geberit-renova-staand-toilet-randvrij-overbouw-54-0-cm-type-1/27000/4025410572998/"],
    "vgl_beslist_4051202324308": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo duoblokpot (3 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-duoblokpot-wit-sanitairkeramiek/27000/4051202324308/"],
    "vgl_beslist_4051202032562": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo staande toiletpot diepspoel (4 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-toiletpot-o-novo-diepspoel-exclusief-toiletbril/27000/4051202032562/"],
    "vgl_beslist_4063382318510": ["Beslist.nl prijsvergelijking: Duravit No.1 duoblokpot (4 aanbieders)", "https://www.beslist.nl/p/duravit-no-1-duoblokpot-wit-keramiek/27000/4063382318510/"],
    "vgl_beslist_4053424507637": ["Beslist.nl prijsvergelijking: Duravit No.1 duoblokreservoir 6 l (5 aanbieders)", "https://www.beslist.nl/p/duravit-no-1-duoblokreservoir-hoogglans-wit-6l-dualflush/27000/4053424507637/"],
    "vgl_beslist_4014804741065": ["Beslist.nl prijsvergelijking: Plieger Smart/Classic staande toiletpot diepspoel pk (3 aanbieders)", "https://www.beslist.nl/p/plieger-toiletpot-diepspoel-smart-classic-wit-pk/27000/4014804741065/"],
    "vgl_beslist_4051202033705": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 closetzitting met softclose en quickrelease (8 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-closetzitting-wit-quickrelease-softclose/27000/4051202033705/"],
    "vgl_beslist_4051202264116": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 closetzitting slimseat (7 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-closetzitting-slimseat-wit-duroplast/27000/4051202264116/"],
    "vgl_beslist_4051202073275": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 closetzitting (9 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-wc-bril-wit-alpine-d-vorm-duroplast/27000/4051202073275/"],
    "vgl_beslist_4051202033897": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 closetzitting met quickrelease (6 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-closetzitting-wit-quickrelease/27000/4051202033897/"],
    "vgl_beslist_4051202374648": ["Beslist.nl prijsvergelijking: Villeroy & Boch Architectura closetzitting met softclose (4 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-architectura-closetzitting-wit-duroplast-softclose/27000/4051202374648/"],
    "vgl_beslist_4021534386190": ["Beslist.nl prijsvergelijking: Duravit Starck 3 closetzitting met softclose en quickrelease (7 aanbieders)", "https://www.beslist.nl/p/duravit-starck-3-wc-zitting-glans-wit-softclose-quickrelease/27000/4021534386190/"],
    "vgl_beslist_4021534224171": ["Beslist.nl prijsvergelijking: Duravit Starck 3 closetzitting (7 aanbieders)", "https://www.beslist.nl/p/duravit-starck-3-wc-zitting-glans-wit-kunststof/27000/4021534224171/"],
    "vgl_beslist_8014140430315": ["Beslist.nl prijsvergelijking: Ideal Standard Tesi closetzitting met deksel en softclose (6 aanbieders)", "https://www.beslist.nl/p/ideal-standard-tesi-closetzitting-met-deksel-wit-softclose/27000/8014140430315/"],
    "vgl_beslist_8014140515098": ["Beslist.nl prijsvergelijking: Ideal Standard Tesi closetzitting met softclose (5 aanbieders)", "https://www.beslist.nl/p/ideal-standard-tesi-wc-bril-wit-softclosemechanisme-deksel-met-scharnieren-van-roestvrij-staal/27000/8014140515098/"],
    "vgl_beslist_5017830474807": ["Beslist.nl prijsvergelijking: Ideal Standard Connect closetzitting met softclose (6 aanbieders)", "https://www.beslist.nl/p/ideal-standard-connect-wc-bril-wit-duroplast-softclose/27000/5017830474807/"],
    "vgl_beslist_4025410726025": ["Beslist.nl prijsvergelijking: Geberit Renova closetzitting d-vorm (6 aanbieders)", "https://www.beslist.nl/p/geberit-renova-closetzitting-wit-d-vormig/27000/4025410726025/"],
    "vgl_beslist_5708590299839": ["Beslist.nl prijsvergelijking: Pressalit T2 closetzitting met softclose (3 aanbieders)", "https://www.beslist.nl/p/pressalit-t2-closetzitting-wit-duroplast-softclose/27000/5708590299839/"],
    "vgl_beslist_5708590318233": ["Beslist.nl prijsvergelijking: Pressalit closetzitting met rvs-scharnieren (3 aanbieders)", "https://www.beslist.nl/p/pressalit-776000-da9999-wc-bril-wit-rvs-scharnieren/27000/5708590318233/"],
    "vgl_beslist_4062373785218": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo fontein (5 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-fontein-wit-sanitairkeramiek/27000/4062373785218/"],
    "vgl_beslist_4047289972020": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 fontein (3 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-fontein-wit-sanitairkeramiek/27000/4047289972020/"],
    "vgl_beslist_4051202918231": ["Beslist.nl prijsvergelijking: Villeroy & Boch Collaro fontein 50x40 cm (3 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-collaro-fontein-wit-keramiek-50x40cm/27000/4051202918231/"],
    "vgl_beslist_4021534536243": ["Beslist.nl prijsvergelijking: Duravit Starck 3 fontein / handwasbak (4 aanbieders)", "https://www.beslist.nl/p/duravit-starck-3-wastafel-fontein-wit-keramiek-hangend/27000/4021534536243/"],
    "vgl_beslist_4053424509327": ["Beslist.nl prijsvergelijking: Duravit Vero Air fontein (3 aanbieders)", "https://www.beslist.nl/p/duravit-vero-air-fontein-glanzend-wit-keramiek/27000/4053424509327/"],
    "vgl_beslist_4047289980223": ["Beslist.nl prijsvergelijking: Villeroy & Boch Subway 2.0 wastafel 80x47 cm (3 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-subway-2-0-wastafel-wit-keramiek-80-x-47-cm/27000/4047289980223/"],
    "vgl_beslist_4062373755990": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo wastafel klein formaat (4 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-wastafel-wit-sanitairkeramiek/27000/4062373755990/"],
    "vgl_beslist_4051202110338": ["Beslist.nl prijsvergelijking: Villeroy & Boch O.novo onderbouwwastafel 53x32 cm (5 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-o-novo-onderbouw-wastafel-wit-sanitairkeramiek/27000/4051202110338/"],
    "vgl_beslist_4053424981918": ["Beslist.nl prijsvergelijking: Duravit D-Neo wastafel (4 aanbieders)", "https://www.beslist.nl/p/duravit-d-neo-wastafel-hoogglans-wit-keramiek/27000/4053424981918/"],
    "vgl_beslist_4021534843495": ["Beslist.nl prijsvergelijking: Duravit Happy D.2 opbouwwastafel geslepen (3 aanbieders)", "https://www.beslist.nl/p/duravit-happyd-2-opbouwwastafel-wit-geslepen-inclusief-bevestiging/27000/4021534843495/"],
    "vgl_beslist_5902115729133": ["Beslist.nl prijsvergelijking: Cersanit Lara hangend badmeubel 60 cm met wastafel (4 aanbieders)", "https://www.beslist.nl/p/cersanit-lara-60-cm-hangende-badkamerkast-met-wastafel-wit/10/5902115729133/"],
    "vgl_beslist_5404024112421": ["Beslist.nl prijsvergelijking: Boss & Wessing Aleco wastafelonderkast 80 cm (3 aanbieders)", "https://www.beslist.nl/p/boss-wessing-aleco-onderkast-wit-80-cm-2-deurs/10/5404024112421/"],
    "vgl_beslist_4013251201023": ["Beslist.nl prijsvergelijking: Differnz Topas spiegelkast 3 deuren met verlichting (3 aanbieders)", "https://www.beslist.nl/p/differnz-topas-spiegelkast-badkamerkast-met-3-deuren-inclusief-verlichting-kast-met-spiegel-wit/10/4013251201023/"],
    "vgl_beslist_4013251201139": ["Beslist.nl prijsvergelijking: Differnz spiegelkast 45x15x35 cm (4 aanbieders)", "https://www.beslist.nl/p/differnz-spiegelkast-badmeubel-wit-45x15x35cm/10/4013251201139/"],
    "vgl_beslist_8719323030213": ["Beslist.nl prijsvergelijking: Wiesbaden spiegelkast aluminium met ledverlichting (5 aanbieders)", "https://www.beslist.nl/p/wiesbaden-spiegelkast-aluminium-met-led-verlichting/10/8719323030213/"],
    "vgl_beslist_8714148593509": ["Beslist.nl prijsvergelijking: Riho Lazy ligbad 170x75 cm (5 aanbieders)", "https://www.beslist.nl/p/ligbad-riho-lazy-170x75-cm-bedieningsknop-midden-wit-glanzend/27000/8714148593509/"],
    "vgl_beslist_8714148547984": ["Beslist.nl prijsvergelijking: Riho Linares ligbad 170x75 cm (5 aanbieders)", "https://www.beslist.nl/p/ligbad-riho-linares-170x75-acryl-white/27000/8714148547984/"],
    "vgl_beslist_8714148571125": ["Beslist.nl prijsvergelijking: Riho Still Square ligbad 170x75 cm (4 aanbieders)", "https://www.beslist.nl/p/ligbad-still-square-170x75-cm-wit/27000/8714148571125/"],
    "vgl_beslist_8714148357071": ["Beslist.nl prijsvergelijking: Riho Columbia inbouwbad 140x70 cm (5 aanbieders)", "https://www.beslist.nl/p/riho-columbia-inbouwbad-wit-acryl/27000/8714148357071/"],
    "vgl_beslist_8714148065419": ["Beslist.nl prijsvergelijking: Riho Yukon inbouw hoekbad (groot formaat) (6 aanbieders)", "https://www.beslist.nl/p/riho-yukon-inbouw-hoekbad-wit-acryl/27000/8714148065419/"],
    "vgl_beslist_8714148315057": ["Beslist.nl prijsvergelijking: Riho Winnipeg hoekbad (groot formaat) (5 aanbieders)", "https://www.beslist.nl/p/riho-winnipeg-hoekbad-wit-acryl/27000/8714148315057/"],
    "vgl_beslist_8720247010748": ["Beslist.nl prijsvergelijking: Xenz Society inbouw ligbad 170x75 cm (4 aanbieders)", "https://www.beslist.nl/p/ligbad-society-170x75-cm-acryl-pergamon-inbouw/27000/8720247010748/"],
    "vgl_beslist_8720247190716": ["Beslist.nl prijsvergelijking: Xenz Madeira ligbad 170x75 cm met badpoten (4 aanbieders)", "https://www.beslist.nl/p/beterbad-xenz-madeira-ligbad-mat-wit-170x75-cm-inclusief-badpoten/27000/8720247190716/"],
    "vgl_beslist_4063382185495": ["Beslist.nl prijsvergelijking: Duravit No.1 inbouwbad trapezium 150x80 cm (4 aanbieders)", "https://www.beslist.nl/p/duravit-no-1-inbouw-bad-trapezium-1500x800mm-wit/27000/4063382185495/"],
    "vgl_beslist_4062373899779": ["Beslist.nl prijsvergelijking: Villeroy & Boch Loop & Friends half vrijstaand bad 180x80 cm (3 aanbieders)", "https://www.beslist.nl/p/villeroy-boch-loop-friends-half-vrijstaand-bad-acryl-wit-alpin-glans/27000/4062373899779/"],
    "vgl_beslist_8718274538403": ["Beslist.nl prijsvergelijking: Best Design Double Slip vrijstaand bad 175x72 cm (3 aanbieders)", "https://www.beslist.nl/p/best-design-double-slip-vrijstaand-bad-wit-dubbelwandig-acryl/27000/8718274538403/"],
    "vgl_beslist_8590913978654": ["Beslist.nl prijsvergelijking: Creavit Antik vrijstaand bad 160x79 cm (4 aanbieders)", "https://www.beslist.nl/p/creavit-antik-vrijstaand-ligbad-wit-160x79-cm-acryl-met-waste/27000/8590913978654/"],
    "vgl_beslist_8720104404239": ["Beslist.nl prijsvergelijking: Arcqua Santo vrijstaand bad 178x80 cm (4 aanbieders)", "https://www.beslist.nl/p/vrijstaand-ligbad-arcqua-santo-178x80-acryl-glans-wit/27000/8720104404239/"],
    "vgl_beslist_8714148593905": ["Beslist.nl prijsvergelijking: Riho Valor half vrijstaand bad 180x80 cm (4 aanbieders)", "https://www.beslist.nl/p/riho-valor-half-vrijstaand-ligbad-solid-surface-mat-wit-180x80x56-cm/27000/8714148593905/"],
    "vgl_beslist_8711238071510": ["Beslist.nl prijsvergelijking: Plieger Quadro designradiator wit (4 aanbieders)", "https://www.beslist.nl/p/plieger-quadro-designradiator-wit-307-watt/27000/8711238071510/"],
    "vgl_beslist_8711238071527": ["Beslist.nl prijsvergelijking: Plieger Quadro designradiator wit (5 aanbieders)", "https://www.beslist.nl/p/plieger-quadro-designradiator-wit-627-watt/27000/8711238071527/"],
    "vgl_beslist_8711238071534": ["Beslist.nl prijsvergelijking: Plieger Quadro designradiator wit (4 aanbieders)", "https://www.beslist.nl/p/plieger-quadro-designradiator-wit-886-watt/27000/8711238071534/"],
    "vgl_beslist_8711238248172": ["Beslist.nl prijsvergelijking: Plieger Cavallino Retto designradiator wit (3 aanbieders)", "https://www.beslist.nl/p/plieger-cavallino-retto-designradiator-wit-817-watt-middenaansluiting/27000/8711238248172/"],
    "vgl_beslist_8711238365022": ["Beslist.nl prijsvergelijking: Florion Nxt designradiator dubbel wit (3 aanbieders)", "https://www.beslist.nl/p/florion-nxt-dubbel-designradiator-wit-staal/27000/8711238365022/"],
    "vgl_beslist_8718315060047": ["Beslist.nl prijsvergelijking: Haceka Gobi Adoria designradiator zwart (3 aanbieders)", "https://www.beslist.nl/p/haceka-gobi-adoria-designradiator-zwart/27000/8718315060047/"],
    "vgl_beslist_8713415352474": ["Beslist.nl prijsvergelijking: Eurom Sani Towel elektrische handdoekradiator 750 w (8 aanbieders)", "https://www.beslist.nl/p/eurom-sani-towel-elektrische-handdoekradiator-wit-750w/27000/8713415352474/"],
    "vgl_beslist_5404029156505": ["Beslist.nl prijsvergelijking: Sanigoods Calgary handdoekradiator 50x180 cm (4 aanbieders)", "https://www.beslist.nl/p/sanigoods-calgary-handdoekradiator-wit-50x180cm-936w/27000/5404029156505/"],
    "vgl_beslist_8720847407245": ["Beslist.nl prijsvergelijking: Callista staafhanddoekradiator 150 cm (5 aanbieders)", "https://www.beslist.nl/p/callista-staafhanddoekradiator-mat-zwart-60-watt-150-cm/27000/8720847407245/"],
    "vgl_beslist_4005176326240": ["Beslist.nl prijsvergelijking: Grohe Essentials toiletrolhouder (6 aanbieders)", "https://www.beslist.nl/p/grohe-essentials-toiletrolhouder-verchroomd-duurzaam-ontwerp/165/4005176326240/"],
    "vgl_beslist_4005176326356": ["Beslist.nl prijsvergelijking: Grohe Essentials reserverolhouder (6 aanbieders)", "https://www.beslist.nl/p/grohe-essentials-reserve-rolhouder-chroom-voor-1-rol/165/4005176326356/"],
    "vgl_beslist_4005176326288": ["Beslist.nl prijsvergelijking: Grohe Essentials handdoekhouder (6 aanbieders)", "https://www.beslist.nl/p/grohe-essentials-handdoekhouder-chroom/165/4005176326288/"],
    "vgl_beslist_4005176326332": ["Beslist.nl prijsvergelijking: Grohe Essentials handdoekhaak rond (7 aanbieders)", "https://www.beslist.nl/p/grohe-essentials-handdoekhaak-rond-chroom/165/4005176326332/"],
    "vgl_beslist_4005176326233": ["Beslist.nl prijsvergelijking: Grohe Essentials zeepdispenser 160 ml (7 aanbieders)", "https://www.beslist.nl/p/grohe-essentials-zeepdispenser-chroom-160ml/165/4005176326233/"],
    "vgl_beslist_4005176413179": ["Beslist.nl prijsvergelijking: Grohe Essentials accessoireset (rolhouder (4 aanbieders)", "https://www.beslist.nl/p/grohe-essentials-accessoireset-toiletrolhouder-toiletborstelset-haak-supersteel/165/4005176413179/"],
    "vgl_beslist_4025416351221": ["Beslist.nl prijsvergelijking: Geberit DuoFresh stickhouder voor inbouwreservoir (7 aanbieders)", "https://www.beslist.nl/p/geberit-duofresh-toilet-stickhouder-glansverchroomd/27000/4025416351221/"],
    "vgl_beslist_8720847406316": ["Beslist.nl prijsvergelijking: Wiesbaden Alonzo vrijstaande toiletborstel met houder (4 aanbieders)", "https://www.beslist.nl/p/wiesbaden-alonzo-vrijstaande-toiletborstel-met-houder-chroom/165/8720847406316/"],
    "vgl_beslist_8719956085413": ["Beslist.nl prijsvergelijking: Wiesbaden dubbele toiletrolhouder met plankje (6 aanbieders)", "https://www.beslist.nl/p/wiesbaden-toiletrolhouder-mat-zwart-dubbel-met-plateau-legplankje/165/8719956085413/"],
}
