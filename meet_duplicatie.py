# -*- coding: utf-8 -*-
"""Meet de duplicatie tussen plaatspagina's en tussen dienstpagina's in site/ (na build.py).

Per groep pagina's:
- uniek: het aandeel woord-8-grammen van een pagina dat op geen enkele andere pagina
  uit dezelfde groep voorkomt (hoger is beter);
- overlap: de gemiddelde Jaccard-overeenkomst tussen twee pagina's (lager is beter).

Header, footer, nav, scripts en styles tellen niet mee. Plaatsnamen worden X en getallen 0,
zodat 'Badkamer Zwolle' tegenover 'Badkamer Kampen' of een ander bedrag niet als uniek telt.

Gebruik: python3 meet_duplicatie.py [--per-pagina]
"""
import os, re, sys, html as H
from collections import Counter
from itertools import combinations
from data import PLAATSEN, DIENSTEN

ROOT = os.path.dirname(os.path.abspath(__file__))
namen = sorted({p["naam"] for p in PLAATSEN} | {p["gemeente"] for p in PLAATSEN} | {p["provincie"] for p in PLAATSEN},
               key=len, reverse=True)
naam_re = re.compile("|".join(re.escape(n) for n in namen))


def woorden(pad):
    h = open(os.path.join(ROOT, "site", pad.strip("/"), "index.html"), encoding="utf-8").read()
    h = re.sub(r"<(script|style|header|footer|nav|form)\b.*?</\1>", " ", h, flags=re.S)
    h = H.unescape(re.sub(r"<[^>]+>", " ", h))
    h = naam_re.sub("X", h)
    h = re.sub(r"\d[\d.,]*", "0", h)
    return re.findall(r"\w+", h.lower())


def grams(w, n=8):
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}


def meet(label, paden, per_pagina=False):
    pg = {p: grams(woorden(p)) for p in paden}
    tel = Counter(g for s in pg.values() for g in s)
    uniek = {p: 100 * sum(1 for g in s if tel[g] == 1) / max(1, len(s)) for p, s in pg.items()}
    jac = [len(pg[a] & pg[b]) / max(1, len(pg[a] | pg[b])) for a, b in combinations(paden, 2)]
    woorden_gem = sum(len(s) for s in pg.values()) / len(pg)
    print(f"{label:40s} {len(paden):4d} pag.  uniek {sum(uniek.values()) / len(uniek):5.1f}%  "
          f"overlap {100 * sum(jac) / max(1, len(jac)):5.1f}%  ~{woorden_gem:5.0f} 8-grammen")
    if per_pagina:
        for p, u in sorted(uniek.items(), key=lambda x: x[1]):
            print(f"    {p:60s} {u:5.1f}%")
    return uniek


def main():
    per = "--per-pagina" in sys.argv
    top = [p for p in PLAATSEN if p["inwoners"] >= 5000]
    meet("Dienstpagina's /diensten/<slug>/", [f"/diensten/{d['slug']}/" for d in DIENSTEN], per)
    meet("Plaatspagina's (alle)", [f"/badkamerspecialist/{p['slug']}/" for p in PLAATSEN], per)
    meet("Plaatspagina's (>= 5.000 inw.)", [f"/badkamerspecialist/{p['slug']}/" for p in top])
    tot = []
    for d in DIENSTEN:
        u = meet(f"Plaats x {d['slug']} (>= 5.000)", [f"/badkamerspecialist/{p['slug']}/{d['slug']}/" for p in top])
        tot += list(u.values())
    print(f"{'Plaats x dienst, gemiddeld':40s} {len(tot):4d} pag.  uniek {sum(tot) / len(tot):5.1f}%")


if __name__ == "__main__":
    main()
