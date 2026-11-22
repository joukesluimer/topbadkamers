# Top Badkamers: instructies voor Claude

Statische leadgeneratie-site voor badkamerrenovatie en badkamerspullen. Het concept is hetzelfde als Topschilder.nl (`~/Projects/topschilder`); deze code is daar op 22 november 2026 van gekopieerd.

## Begin elke sessie zo

1. Lees `PLAN.md`: concept, stand van zaken, openstaande keuzes en fases.
2. Vat kort samen waar we staan en stel de volgende stap voor.

## Werkwijze

- Alles in het Nederlands: chat, schermteksten, commits en documentatie. Namen in de code mogen blijven zoals in Topschilder.
- `python3 build.py` bouwt `site/`; `python3 verify.py` moet eindigen met "ALLES OK". Commit `site/` nooit.
- Lokaal testen: `cd site && python3 -m http.server 8765 --bind 127.0.0.1`, op 375 en 1280 px breed.
- Regels:
  - geen valse claims (geen verzonnen reviews, sterren, aantallen monteurs of projecten);
  - foto's alleen met een geldige licentie en een vermelding op /fotoverantwoording/;
  - zelfgemaakte renders eerlijk als illustratie;
  - niets live zetten, geen accounts aanmaken en geen geld uitgeven zonder akkoord van de gebruiker;
  - bevestig grote of onomkeerbare stappen eerst.
