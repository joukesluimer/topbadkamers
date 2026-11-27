# -*- coding: utf-8 -*-
"""Zet een padvoorvoegsel voor alle root-links in site/, voor hosting in een submap.

GitHub Pages zonder eigen domein serveert de site op
https://joukesluimer.github.io/topbadkamers/, dus /assets/... moet daar
/topbadkamers/assets/... worden. Het voorvoegsel komt uit het pad van
SITE["url"] in data.py. Met een eigen domein (url zonder pad) doet dit script niets.

Gebruik (na build.py en verify.py, vlak voor het publiceren):  python3 prefix.py
"""

import os
import re
from urllib.parse import urlparse

from data import SITE

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = urlparse(SITE["url"]).path.rstrip("/")

# href="/..", src="/..", action="/..", content="/.." (niet "//" van protocol-relatieve urls)
ATTR = re.compile(r'(\b(?:href|src|action|poster|data-href)=["\'])/(?!/)')
SRCSET = re.compile(r'(\b(?:imagesrcset|srcset)=["\'])([^"\']+)(["\'])')
CSS_URL = re.compile(r'(url\(\s*["\']?)/(?!/)')
# JS-strings die een sitepad zijn: "/assets/...", "/bedankt/", '/offerte-aanvragen/' enz.
JS_PAD = re.compile(r'(["\'`])/(assets|bedankt|offerte-aanvragen|diensten|badkamerspecialist|werkgebied|prijzen|contact|cookies|privacy|voorwaarden|voor-badkamerspecialisten)/')


def _srcset(m):
    delen = []
    for item in m.group(2).split(","):
        item = item.strip()
        if item.startswith("/") and not item.startswith("//"):
            item = BASE + item
        delen.append(item)
    return m.group(1) + ", ".join(delen) + m.group(3)


def html(t):
    t = ATTR.sub(lambda m: m.group(1) + BASE + "/", t)
    t = SRCSET.sub(_srcset, t)
    t = CSS_URL.sub(lambda m: m.group(1) + BASE + "/", t)
    t = JS_PAD.sub(lambda m: m.group(1) + BASE + "/" + m.group(2) + "/", t)
    return t


def css(t):
    return CSS_URL.sub(lambda m: m.group(1) + BASE + "/", t)


def js(t):
    t = ATTR.sub(lambda m: m.group(1) + BASE + "/", t)  # HTML-fragmenten in JS, zoals de cookiebanner
    return JS_PAD.sub(lambda m: m.group(1) + BASE + "/" + m.group(2) + "/", t)


def main():
    if not BASE:
        print("Geen submap in SITE['url']; niets te doen.")
        return
    n = 0
    for dirpath, _, files in os.walk(OUT):
        for fn in files:
            pad = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1]
            if ext not in (".html", ".css", ".js") or "/vendor/" in pad:
                continue
            with open(pad, encoding="utf-8") as f:
                oud = f.read()
            nieuw = {".html": html, ".css": css, ".js": js}[ext](oud)
            if nieuw != oud:
                with open(pad, "w", encoding="utf-8") as f:
                    f.write(nieuw)
                n += 1
    print(f"✓ voorvoegsel {BASE} gezet in {n} bestanden")


if __name__ == "__main__":
    main()
