"""Renderserver voor de terrazzo-render van ronde 4 (renders/b6-terrazzo-badkamer.html), poort 8812.

Gebruik (vanuit de projectmap):
    python3 renders/b6-terrazzo-server.py [poort]
Headless renderen:
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --use-angle=swiftshader \
      --enable-unsafe-swiftshader --window-size=1600,1067 \
      "http://127.0.0.1:8812/renders/b6-terrazzo-badkamer.html?view=1&auto=1"
De pagina path-tracet de scène en stuurt de webp's per POST naar /save; deze server schrijft ze naar
fotos/renders/b4-terrazzo-badkamer-{1,2}-{400,800,1600}.webp. Met ?preview=1 in plaats van ?auto=1 komt er
alleen een voorbeeld in PREVIEW_DIR (standaard /tmp). POST /log schrijft voortgang naar stdout.
"""
import base64
import http.server
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOEL = os.environ.get("B6_OUT") or os.path.join(ROOT, "fotos", "renders")  # B6_OUT: testmap
PREVIEW_DIR = os.environ.get("PREVIEW_DIR", "/tmp")
TOEGESTAAN = {f"b4-terrazzo-badkamer-{v}-{w}.webp" for v in (1, 2) for w in (400, 800, 1600)}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass

    def do_POST(self):
        lengte = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(lengte)
        if self.path == "/log":
            print(raw.decode("utf-8", "replace"), flush=True)
            self.send_response(204)
            self.end_headers()
            return
        if self.path != "/save":
            self.send_error(404)
            return
        body = json.loads(raw)
        naam = os.path.basename(body["name"])
        if body.get("preview"):
            pad = os.path.join(PREVIEW_DIR, naam)
        elif naam in TOEGESTAAN:
            pad = os.path.join(DOEL, naam)
        else:
            self.send_error(400, "onbekende naam")
            return
        with open(pad, "wb") as f:
            f.write(base64.b64decode(body["data"].split(",", 1)[-1]))
        print(f"opgeslagen {pad} ({os.path.getsize(pad)} bytes)", flush=True)
        antwoord = json.dumps({"ok": True, "path": pad, "bytes": os.path.getsize(pad)}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(antwoord)))
        self.end_headers()
        self.wfile.write(antwoord)


if __name__ == "__main__":
    poort = int(sys.argv[1]) if len(sys.argv) > 1 else 8812
    http.server.ThreadingHTTPServer(("127.0.0.1", poort), Handler).serve_forever()
