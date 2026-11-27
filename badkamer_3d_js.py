# -*- coding: utf-8 -*-
"""JavaScript voor de 3D-badkamer (/tools/badkamer-3d/). __DATA__ wordt in badkamer_3d.py ingevuld.

Opbouw:
- keuzes en prijs: werkt altijd, ook zonder WebGL;
- 3D: pas na een klik op "Start 3D" laden we three.js (vendor/three, lokaal) en bouwen we de scène.
  Tegels, hout en marmer tekenen we zelf op een canvas; er zijn geen extra afbeeldingen nodig.
Eenheden in de scène: meters. x = breedte (links-rechts), z = diepte (achterwand op -d/2), y = hoogte.
"""

JS = r"""(function () {
  "use strict";
  var root = document.querySelector("[data-b3]");
  if (!root) return;
  var D = __DATA__;
  var K = {};
  Object.keys(D.start).forEach(function (k) { K[k] = D.start[k]; });
  var form = root.querySelector("[data-b3-form]");
  var $ = function (s) { return root.querySelector(s); };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ------------------------------------------------------------------ prijs */
  function euro(n) { return "€ " + (Math.round(n / 100) * 100).toLocaleString("nl-NL"); }
  function posten() {
    var P = D.prijs, w = D.wand[K.wand], v = D.vloer[K.vloer];
    var r = [
      ["Wandtegels: " + w.naam.toLowerCase() + " (" + D.m2.wand + " m²)", P.wand[K.wand]],
      ["Vloertegels: " + v.naam.toLowerCase() + " (" + String(D.m2.vloer).replace(".", ",") + " m²)", P.vloer[K.vloer]],
      ["Tegels zetten, lijm en voeg", P.zetten],
      [D.indeling[K.indeling].naam + " met kraan, plaatsen en aansluiten", P.indeling[K.indeling]],
      ["Badmeubel " + D.meubel[K.meubel].naam.toLowerCase() + ", met wastafel en spiegel", P.meubel[K.meubel]],
      ["Hangtoilet met inbouwreservoir", P.toilet]
    ];
    P.vast.forEach(function (x) { r.push([x.naam, x.lh]); });
    return r;
  }
  function totaal() {
    return posten().reduce(function (a, p) { return [a[0] + p[1][0], a[1] + p[1][1]]; }, [0, 0]);
  }
  function toonPrijs() {
    var t = totaal();
    $("[data-b3-totaal]").textContent = euro(t[0]) + " – " + euro(t[1]);
    $("[data-b3-posten]").innerHTML = posten().map(function (p) {
      return "<li><span>" + p[0] + "</span><b>" + euro(p[1][0]) + " – " + euro(p[1][1]) + "</b></li>";
    }).join("");
    $("[data-b3-kraannoot]").textContent = K.kraan === "chroom"
      ? "Kranen in chroom: de meest gekozen kleur."
      : "Kranen in " + D.kraan[K.kraan].naam.toLowerCase() + " zijn vaak iets duurder dan chroom. Dat verschilt per merk, dus we tellen het niet apart.";
  }
  function beschrijving() {
    var t = totaal(), w = D.wand[K.wand], v = D.vloer[K.vloer];
    return [
      "- Wandtegels: " + w.naam + " (" + w.formaat + ")",
      "- Vloertegels: " + v.naam + " (" + v.formaat + ")",
      "- Kranen en details: " + D.kraan[K.kraan].naam.toLowerCase(),
      "- Badmeubel: " + D.meubel[K.meubel].naam.toLowerCase(),
      "- Douche of bad: " + D.indeling[K.indeling].naam.toLowerCase(),
      "",
      "Prijsindicatie uit de tool (badkamer van " + String(D.kamer.b).replace(".", ",") + " × " +
        String(D.kamer.d).replace(".", ",") + " m, incl. btw): " + euro(t[0]) + " – " + euro(t[1]) + "."
    ].join("\n");
  }
  form.addEventListener("change", function (e) {
    var n = e.target.name;
    if (!n || n.indexOf("b3-") !== 0) return;
    K[n.slice(3)] = e.target.value;
    toonPrijs();
    if (scene3d) scene3d.toepassen();
  });
  $("[data-b3-mee]").addEventListener("click", function () {
    try { sessionStorage.setItem("tb_3d", beschrijving()); } catch (x) {}
  });
  toonPrijs();

  /* ------------------------------------------------------------------ 3D */
  var scene3d = null;
  var stage = $("[data-b3-stage]");
  var melding = $("[data-b3-melding]");
  var startKnop = $("[data-b3-start]");
  function meld(t) { melding.textContent = t; melding.hidden = !t; }

  function heeftWebGL() {
    try {
      var c = document.createElement("canvas");
      return !!(window.WebGLRenderingContext && (c.getContext("webgl2") || c.getContext("webgl")));
    } catch (e) { return false; }
  }
  var imp = function (u) { return (new Function("u", "return import(u)"))(u); };
  var VENDOR = "/assets/vendor/three/";

  startKnop.addEventListener("click", function () {
    if (!heeftWebGL()) {
      $("[data-b3-startblok]").hidden = true;
      meld("Je browser kan geen 3D tonen (WebGL staat uit of wordt niet ondersteund). Je ziet een vaste afbeelding. Kiezen en de prijs bekijken werkt gewoon.");
      return;
    }
    startKnop.disabled = true;
    startKnop.lastChild.textContent = " 3D laden…";
    Promise.all([imp(VENDOR + "three.module.min.js"), imp(VENDOR + "OrbitControls.js"), imp(VENDOR + "RoomEnvironment.js")])
      .then(function (m) {
        scene3d = bouw(m[0], m[1].OrbitControls, m[2].RoomEnvironment);
        $("[data-b3-startblok]").hidden = true;
        $("[data-b3-knoppen]").hidden = false;
        var poster = stage.querySelector(".b3-poster");
        if (poster) poster.hidden = true;
        $("[data-b3-hulp]").textContent = "Sleep met je muis of vinger om rond te kijken. Zoom met het scrollwiel of door te knijpen. Je kunt ook de knoppen rechtsonder gebruiken.";
        scene3d.canvas.focus({ preventScroll: true });
      })
      .catch(function (e) {
        startKnop.disabled = false;
        startKnop.lastChild.textContent = " Start 3D";
        meld("Het laden van de 3D-weergave is niet gelukt. Probeer het nog een keer, of kies gewoon je materialen: de prijs werkt ook zonder 3D.");
        if (window.console) console.error(e);
      });
  });

  /* ---------------------------------------------------- texturen op canvas */
  function rng(seed) {
    return function () {
      seed = (seed + 0x6D2B79F5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h; }
  function rgb(hex) { var n = parseInt(hex.slice(1), 16); return [n >> 16 & 255, n >> 8 & 255, n & 255]; }
  function tint(hex, f, a) {
    var c = rgb(hex).map(function (x) { return Math.max(0, Math.min(255, Math.round(x * (1 + f)))); });
    return a === undefined ? "rgb(" + c.join(",") + ")" : "rgba(" + c.join(",") + "," + a + ")";
  }
  var TEX_M = 1.2;  // een textuur beslaat 1,2 × 1,2 meter

  function tegelCanvas(t, S) {
    var c = document.createElement("canvas"); c.width = c.height = S;
    var g = c.getContext("2d"), px = S / TEX_M;
    var tw = t.tw * px, th = t.th * px, cols = Math.round(TEX_M / t.tw), rows = Math.round(TEX_M / t.th);
    var vb = Math.max(1.5, t.vb * S / 1024), basis = hash(t.p + t.kleur);
    g.fillStyle = t.voeg; g.fillRect(0, 0, S, S);
    for (var r = 0; r < rows; r++) {
      var off = (t.offset && r % 2) ? t.offset * tw : 0;
      for (var k = -1; k <= cols; k++) {
        var x = k * tw + off;
        if (x > S || x + tw < 0) continue;
        var R = rng(basis + r * 977 + (((k % cols) + cols) % cols) * 131);
        g.save();
        g.beginPath(); g.rect(x + vb / 2, r * th + vb / 2, tw - vb, th - vb); g.clip();
        TEKEN[t.p](g, x + vb / 2, r * th + vb / 2, tw - vb, th - vb, R, t, px);
        g.restore();
      }
    }
    return c;
  }
  function vlak(g, x, y, w, h, R, t) {
    g.fillStyle = tint(t.kleur, (R() - 0.5) * 2 * (t.var || 0)); g.fillRect(x, y, w, h);
  }
  function glans(g, x, y, w, h, a) {
    var gr = g.createLinearGradient(x, y, x + w, y + h);
    gr.addColorStop(0, "rgba(255,255,255," + a + ")"); gr.addColorStop(0.5, "rgba(255,255,255,0)"); gr.addColorStop(1, "rgba(0,0,0," + a * 0.6 + ")");
    g.fillStyle = gr; g.fillRect(x, y, w, h);
  }
  var TEKEN = {
    rechthoek: function (g, x, y, w, h, R, t) { vlak(g, x, y, w, h, R, t); glans(g, x, y, w, h, 0.05); },
    metro: function (g, x, y, w, h, R, t) {
      vlak(g, x, y, w, h, R, t);
      g.lineWidth = 3;
      g.strokeStyle = "rgba(255,255,255,.7)"; g.beginPath(); g.moveTo(x + 1, y + h - 1); g.lineTo(x + 1, y + 1); g.lineTo(x + w - 1, y + 1); g.stroke();
      g.strokeStyle = "rgba(0,0,0,.10)"; g.beginPath(); g.moveTo(x + w - 1, y + 1); g.lineTo(x + w - 1, y + h - 1); g.lineTo(x + 1, y + h - 1); g.stroke();
      glans(g, x, y, w, h, 0.06);
    },
    zellige: function (g, x, y, w, h, R, t) {
      vlak(g, x, y, w, h, R, t);
      var gr = g.createRadialGradient(x + w * R(), y + h * R(), 1, x + w / 2, y + h / 2, w * 0.9);
      gr.addColorStop(0, tint(t.kleur, 0.35 + R() * 0.2, 0.55)); gr.addColorStop(1, tint(t.kleur, -0.25, 0));
      g.fillStyle = gr; g.fillRect(x, y, w, h);
      for (var i = 0; i < 3; i++) {
        g.fillStyle = tint(t.kleur, (R() - 0.5) * 0.5, 0.25);
        g.beginPath(); g.ellipse(x + w * R(), y + h * R(), w * (0.15 + R() * 0.3), h * (0.1 + R() * 0.25), R() * 3, 0, 7); g.fill();
      }
      g.lineWidth = 5; g.strokeStyle = tint(t.kleur, -0.35, 0.35); g.strokeRect(x + 1, y + 1, w - 2, h - 2);
    },
    marmer: function (g, x, y, w, h, R, t) {
      vlak(g, x, y, w, h, R, t);
      var gr = g.createLinearGradient(x, y, x + w, y + h);
      gr.addColorStop(0, "rgba(255,255,255,.35)"); gr.addColorStop(1, "rgba(200,198,192,.22)");
      g.fillStyle = gr; g.fillRect(x, y, w, h);
      g.lineCap = "round"; g.lineJoin = "round";
      // een paar zachte, schuine aders met fijne zijtakjes
      for (var i = 0; i < 4; i++) {
        var hoofd = i < 2;
        var x0 = x - w * 0.2 + w * 1.4 * R(), y0 = y - 20, x1 = x0 + (R() < 0.5 ? -1 : 1) * w * (0.5 + R() * 0.6), y1 = y + h + 20;
        var pts = [[x0, y0]];
        for (var s = 1; s <= 4; s++) { var f = s / 4; pts.push([x0 + (x1 - x0) * f + (R() - 0.5) * w * 0.18, y0 + (y1 - y0) * f]); }
        var lagen = hoofd ? [[9, 0.07, 3], [2.2, 0.32, 0]] : [[1, 0.28, 0]];
        lagen.forEach(function (l) {
          g.filter = l[2] ? "blur(" + l[2] + "px)" : "none";
          g.strokeStyle = tint(t.ader, 0, l[1]); g.lineWidth = l[0];
          g.beginPath(); g.moveTo(pts[0][0], pts[0][1]);
          for (var q = 1; q < pts.length - 1; q++) g.quadraticCurveTo(pts[q][0], pts[q][1], (pts[q][0] + pts[q + 1][0]) / 2, (pts[q][1] + pts[q + 1][1]) / 2);
          g.lineTo(pts[pts.length - 1][0], pts[pts.length - 1][1]);
          g.stroke();
        });
        g.filter = "none";
        if (hoofd) for (var tk = 0; tk < 3; tk++) {
          var p0 = pts[1 + Math.floor(R() * 3)], len = 40 + R() * 90, a = (R() - 0.5) * 1.6 + (R() < 0.5 ? 0 : Math.PI);
          g.strokeStyle = tint(t.ader, 0.1, 0.22); g.lineWidth = 0.8;
          g.beginPath(); g.moveTo(p0[0], p0[1]);
          g.quadraticCurveTo(p0[0] + Math.cos(a) * len * 0.5 + (R() - 0.5) * 20, p0[1] + Math.sin(a) * len * 0.5 + 20, p0[0] + Math.cos(a) * len, p0[1] + Math.sin(a) * len + 40);
          g.stroke();
        }
      }
    },
    beton: function (g, x, y, w, h, R, t) {
      vlak(g, x, y, w, h, R, t);
      for (var i = 0; i < 6; i++) {
        var gr = g.createRadialGradient(x + w * R(), y + h * R(), 1, x + w * R(), y + h * R(), w * (0.2 + R() * 0.4));
        gr.addColorStop(0, tint(t.kleur, (R() - 0.5) * 0.25, 0.5)); gr.addColorStop(1, tint(t.kleur, 0, 0));
        g.fillStyle = gr; g.fillRect(x, y, w, h);
      }
      for (var j = 0; j < 1400; j++) {
        g.fillStyle = R() < 0.5 ? "rgba(0,0,0,.10)" : "rgba(255,255,255,.10)";
        g.fillRect(x + w * R(), y + h * R(), 1.5, 1.5);
      }
    },
    hout: function (g, x, y, w, h, R, t) {
      vlak(g, x, y, w, h, R, t);
      g.lineWidth = 1.2;
      for (var i = 0; i < 26; i++) {
        var yy = y + h * R(), a = 0.05 + R() * 0.12, fase = R() * 6, amp = 1 + R() * 3;
        g.strokeStyle = R() < 0.7 ? "rgba(70,40,15," + a + ")" : "rgba(255,235,200," + a + ")";
        g.beginPath();
        for (var s = 0; s <= 40; s++) { var xx = x + w * s / 40; var py = yy + Math.sin(fase + s * 0.35) * amp; if (s) g.lineTo(xx, py); else g.moveTo(xx, py); }
        g.stroke();
      }
      if (R() < 0.5) {
        var kx = x + w * (0.15 + R() * 0.7), ky = y + h * (0.3 + R() * 0.4);
        g.fillStyle = "rgba(80,45,20,.35)"; g.beginPath(); g.ellipse(kx, ky, 7, 4, 0, 0, 7); g.fill();
      }
      glans(g, x, y, w, h, 0.04);
    },
    cement: function (g, x, y, w, h, R, t) {
      g.fillStyle = t.kleur; g.fillRect(x, y, w, h);
      g.fillStyle = t.kleur2;
      [[x, y], [x + w, y], [x, y + h], [x + w, y + h]].forEach(function (p) { g.beginPath(); g.arc(p[0], p[1], w * 0.3, 0, 7); g.fill(); });
      g.fillStyle = t.kleur;
      [[x, y], [x + w, y], [x, y + h], [x + w, y + h]].forEach(function (p) { g.beginPath(); g.arc(p[0], p[1], w * 0.24, 0, 7); g.fill(); });
      var cx = x + w / 2, cy = y + h / 2, s = w * 0.17;
      g.fillStyle = t.kleur2; g.beginPath(); g.moveTo(cx, cy - s); g.lineTo(cx + s, cy); g.lineTo(cx, cy + s); g.lineTo(cx - s, cy); g.closePath(); g.fill();
      g.strokeStyle = t.kleur2; g.lineWidth = 2; g.strokeRect(x + w * 0.06, y + h * 0.06, w * 0.88, h * 0.88);
      for (var j = 0; j < 220; j++) { g.fillStyle = "rgba(0,0,0,.06)"; g.fillRect(x + w * R(), y + h * R(), 2, 2); }
    },
    terrazzo: function (g, x, y, w, h, R, t) {
      vlak(g, x, y, w, h, R, t);
      for (var i = 0; i < 420; i++) {
        var groot = R() < 0.08, r = groot ? 6 + R() * 9 : 1.5 + R() * 4.5;
        var cx = x + w * R(), cy = y + h * R(), n = 5 + Math.floor(R() * 3);
        g.fillStyle = t.chips[Math.floor(R() * t.chips.length)];
        g.beginPath();
        for (var s = 0; s < n; s++) { var a = s / n * 6.283 + R() * 0.6, rr = r * (0.6 + R() * 0.5); g.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); }
        g.closePath(); g.fill();
      }
      glans(g, x, y, w, h, 0.05);
    }
  };
  function houtCanvas(S) {
    var c = document.createElement("canvas"); c.width = c.height = S;
    var g = c.getContext("2d"), R = rng(7);
    g.fillStyle = "#b9895a"; g.fillRect(0, 0, S, S);
    for (var p = 0; p < 6; p++) { g.fillStyle = tint("#b9895a", (R() - 0.5) * 0.12, 0.6); g.fillRect(p * S / 6, 0, S / 6, S); }
    for (var i = 0; i < 90; i++) {
      var xx = S * R(), a = 0.05 + R() * 0.14, fase = R() * 6, amp = 1 + R() * 4;
      g.strokeStyle = R() < 0.75 ? "rgba(70,38,12," + a + ")" : "rgba(255,230,190," + a + ")";
      g.lineWidth = 0.8 + R() * 1.6; g.beginPath();
      for (var s = 0; s <= 50; s++) { var yy = S * s / 50; var px = xx + Math.sin(fase + s * 0.25) * amp; if (s) g.lineTo(px, yy); else g.moveTo(px, yy); }
      g.stroke();
    }
    return c;
  }

  /* ---------------------------------------------------------------- scène */
  function bouw(THREE, OrbitControls, RoomEnvironment) {
    var W = D.kamer.b, Dd = D.kamer.d, H = D.kamer.h, x0 = -W / 2, z0 = -Dd / 2;
    var canvas = document.createElement("canvas");
    canvas.setAttribute("role", "img");
    canvas.setAttribute("aria-label", "3D-weergave van de badkamer met je gekozen tegels, kranen, meubel en douche of bad");
    canvas.tabIndex = 0;
    stage.insertBefore(canvas, stage.firstChild);
    var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, preserveDrawingBuffer: /poster=1/.test(location.search) });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.05;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    var scene = new THREE.Scene();
    var pmrem = new THREE.PMREMGenerator(renderer);
    scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;

    var camera = new THREE.PerspectiveCamera(40, 4 / 3, 0.05, 50);
    var aniso = renderer.capabilities.getMaxAnisotropy();

    // licht
    scene.add(new THREE.HemisphereLight(0xffffff, 0xcfc6b8, 0.55));
    var zon = new THREE.DirectionalLight(0xfff4e6, 1.6);
    zon.position.set(2.8, 5.2, 3.6);
    zon.target.position.set(-0.2, 0.6, -0.6);
    zon.castShadow = true;
    zon.shadow.mapSize.set(1024, 1024);
    var sc = zon.shadow.camera; sc.left = -3; sc.right = 3; sc.top = 3; sc.bottom = -3; sc.near = 1; sc.far = 14;
    zon.shadow.bias = -0.0004; zon.shadow.normalBias = 0.02;
    scene.add(zon, zon.target);

    // materialen
    var M = {
      wand: new THREE.MeshStandardMaterial({ roughness: 0.2, envMapIntensity: 0.7 }),
      vloer: new THREE.MeshStandardMaterial({ roughness: 0.6, envMapIntensity: 0.6 }),
      kraan: new THREE.MeshStandardMaterial({ color: 0x222222 }),
      meubel: new THREE.MeshStandardMaterial({ roughness: 0.55 }),
      keramiek: new THREE.MeshStandardMaterial({ color: 0xf8f8f6, roughness: 0.12, envMapIntensity: 0.9 }),
      binnen: new THREE.MeshStandardMaterial({ color: 0xf2f2ef, roughness: 0.18 }),
      stuc: new THREE.MeshStandardMaterial({ color: 0xf3f1ec, roughness: 0.95 }),
      glas: new THREE.MeshStandardMaterial({ color: 0xd6ecef, roughness: 0.04, metalness: 0, transparent: true, opacity: 0.2, depthWrite: false, side: THREE.DoubleSide }),
      spiegel: new THREE.MeshStandardMaterial({ color: 0xf4f8f9, roughness: 0.06, metalness: 0.92, envMapIntensity: 1.7 }),
      led: new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xfff1d6, emissiveIntensity: 1.4 }),
      handdoek: new THREE.MeshStandardMaterial({ color: 0xe1d4bf, roughness: 1 }),
      mat: new THREE.MeshStandardMaterial({ color: 0xcfc3ae, roughness: 1 }),
      pot: new THREE.MeshStandardMaterial({ color: 0xf1ede6, roughness: 0.6 }),
      blad: new THREE.MeshStandardMaterial({ color: 0x4f7a4a, roughness: 0.7, side: THREE.DoubleSide })
    };
    var houtTex = new THREE.CanvasTexture(houtCanvas(512));
    houtTex.colorSpace = THREE.SRGBColorSpace; houtTex.anisotropy = aniso;

    var texCache = {};
    function tegelTex(t) {
      var key = JSON.stringify(t);
      if (!texCache[key]) {
        var tx = new THREE.CanvasTexture(tegelCanvas(t, 1024));
        tx.wrapS = tx.wrapT = THREE.RepeatWrapping;
        tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = aniso;
        texCache[key] = tx;
      }
      return texCache[key];
    }

    // hulpjes
    function mesh(geo, mat, x, y, z, schaduw) {
      var m = new THREE.Mesh(geo, mat); m.position.set(x || 0, y || 0, z || 0);
      if (schaduw !== false) { m.castShadow = true; m.receiveShadow = true; }
      return m;
    }
    function doos(w, h, d, mat, x, y, z) { return mesh(new THREE.BoxGeometry(w, h, d), mat, x, y, z); }
    function buis(r, l, mat, x, y, z, as) {
      var m = mesh(new THREE.CylinderGeometry(r, r, l, 20), mat, x, y, z);
      if (as === "x") m.rotation.z = Math.PI / 2;
      if (as === "z") m.rotation.x = Math.PI / 2;
      return m;
    }
    function uvMeters(geo, w, h) {
      var uv = geo.attributes.uv;
      for (var i = 0; i < uv.count; i++) uv.setXY(i, uv.getX(i) * w / TEX_M, uv.getY(i) * h / TEX_M);
      return geo;
    }
    function ronding(w, d, r) {
      var s = new THREE.Shape(), x = -w / 2, y = -d / 2;
      s.moveTo(x + r, y); s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
      s.lineTo(x + w, y + d - r); s.quadraticCurveTo(x + w, y + d, x + w - r, y + d);
      s.lineTo(x + r, y + d); s.quadraticCurveTo(x, y + d, x, y + d - r);
      s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
      return s;
    }
    // bak met rand (bad, waskom): buitenvorm met gat, omhoog geëxtrudeerd, plus een bodem
    function bak(w, d, h, rand, rBuiten, rBinnen, mat) {
      var s = ronding(w, d, rBuiten);
      s.holes.push(ronding(w - 2 * rand, d - 2 * rand, rBinnen));
      var geo = new THREE.ExtrudeGeometry(s, { depth: h, bevelEnabled: true, bevelThickness: 0.006, bevelSize: 0.006, bevelSegments: 2, curveSegments: 12 });
      geo.rotateX(-Math.PI / 2);
      var g = new THREE.Group();
      g.add(mesh(geo, mat));
      var bodem = new THREE.ShapeGeometry(ronding(w - 2 * rand, d - 2 * rand, rBinnen), 12);
      bodem.rotateX(-Math.PI / 2);
      g.add(mesh(bodem, M.binnen, 0, Math.min(0.06, h * 0.35), 0));
      return g;
    }

    // kamer: vloer, wanden en per wand een groep (wordt verborgen als de camera erachter staat)
    var kamer = new THREE.Group(); scene.add(kamer);
    var vloerGeo = uvMeters(new THREE.PlaneGeometry(W, Dd), W, Dd); vloerGeo.rotateX(-Math.PI / 2);
    var vloer = mesh(vloerGeo, M.vloer, 0, 0.002, 0); vloer.castShadow = false; kamer.add(vloer);
    kamer.add(doos(W + 0.24, 0.12, Dd + 0.12, M.stuc, 0, -0.06, -0.06));
    var schaduwVlak = new THREE.Mesh(new THREE.PlaneGeometry(14, 14), new THREE.ShadowMaterial({ opacity: 0.12 }));
    schaduwVlak.rotation.x = -Math.PI / 2; schaduwVlak.position.y = -0.121; schaduwVlak.receiveShadow = true; scene.add(schaduwVlak);

    // zij: -1 = linkerwand, 1 = rechterwand (de muurdikte loopt dan alleen naar achteren door)
    function wand(lengte, zij) {
      var g = new THREE.Group();
      var vlakGeo = uvMeters(new THREE.PlaneGeometry(lengte, H), lengte, H);
      var v = mesh(vlakGeo, M.wand, 0, H / 2, 0.001); v.castShadow = false; g.add(v);
      g.add(zij ? doos(lengte + 0.12, H, 0.12, M.stuc, -zij * 0.06, H / 2, -0.06) : doos(lengte + 0.24, H, 0.12, M.stuc, 0, H / 2, -0.06));
      return g;
    }
    var achter = wand(W, 0); achter.position.set(0, 0, z0); kamer.add(achter);
    var links = wand(Dd, -1); links.rotation.y = Math.PI / 2; links.position.set(x0, 0, 0); kamer.add(links);
    var rechts = wand(Dd, 1); rechts.rotation.y = -Math.PI / 2; rechts.position.set(-x0, 0, 0); kamer.add(rechts);
    // linkerwand-groep (90° gedraaid): lokale x = wereld -z, lokale z = de kamer in. z hieronder is wereld-z.
    function opLinks(obj, z, y, uit) { obj.position.set(-z, y, uit); links.add(obj); return obj; }

    /* ---- badmeubel, kraan en spiegel tegen de achterwand */
    var mx = 0.2, mb = 0.8, md = 0.46;
    var meubel = new THREE.Group(); meubel.position.set(mx, 0, z0); kamer.add(meubel);
    meubel.add(doos(mb - 0.01, 0.44, md - 0.03, M.meubel, 0, 0.6, (md - 0.03) / 2));
    meubel.add(doos(mb - 0.006, 0.2, 0.02, M.meubel, 0, 0.712, md - 0.02));
    meubel.add(doos(mb - 0.006, 0.2, 0.02, M.meubel, 0, 0.49, md - 0.02));
    meubel.add(doos(mb + 0.02, 0.04, md + 0.01, M.keramiek, 0, 0.84, (md + 0.01) / 2));
    var kom = bak(0.5, 0.36, 0.12, 0.012, 0.05, 0.04, M.keramiek); kom.position.set(0, 0.86, 0.26); meubel.add(kom);
    // wandkraan
    meubel.add(buis(0.03, 0.012, M.kraan, 0, 1.12, 0.006, "z"));
    meubel.add(buis(0.012, 0.22, M.kraan, 0, 1.12, 0.11, "z"));
    meubel.add(buis(0.022, 0.012, M.kraan, 0.13, 1.12, 0.006, "z"));
    meubel.add(buis(0.007, 0.07, M.kraan, 0.13, 1.12, 0.04, "z"));
    // ronde spiegel met led-rand
    var spiegel = mesh(new THREE.CircleGeometry(0.31, 64), M.spiegel, 0, 1.62, 0.03, false); meubel.add(spiegel);
    var ring = mesh(new THREE.TorusGeometry(0.315, 0.008, 10, 80), M.led, 0, 1.62, 0.028, false); meubel.add(ring);
    meubel.add(mesh(new THREE.CylinderGeometry(0.30, 0.30, 0.02, 48), M.stuc, 0, 1.62, 0.015).rotateX(Math.PI / 2));
    // badmat
    kamer.add(doos(0.75, 0.012, 0.48, M.mat, mx, 0.008, z0 + md + 0.36));

    /* ---- hangtoilet met bedieningsplaat */
    var tx = 0.92;
    var toilet = new THREE.Group(); toilet.position.set(tx, 0, z0); kamer.add(toilet);
    var potGeo = new THREE.CylinderGeometry(0.18, 0.14, 0.24, 40); potGeo.scale(1, 1, 1.45);
    toilet.add(mesh(potGeo, M.keramiek, 0, 0.3, 0.3));
    toilet.add(doos(0.34, 0.26, 0.16, M.keramiek, 0, 0.3, 0.08));
    var brilGeo = new THREE.CylinderGeometry(0.183, 0.183, 0.025, 40); brilGeo.scale(1, 1, 1.45);
    toilet.add(mesh(brilGeo, M.keramiek, 0, 0.435, 0.3));
    toilet.add(doos(0.36, 0.03, 0.08, M.keramiek, 0, 0.438, 0.06));
    toilet.add(doos(0.25, 0.16, 0.012, M.kraan, 0, 1.05, 0.006));
    toilet.add(doos(0.105, 0.13, 0.006, M.keramiek, -0.058, 1.05, 0.014));
    toilet.add(doos(0.105, 0.13, 0.006, M.keramiek, 0.058, 1.05, 0.014));

    /* ---- inloopdouche */
    var douche = new THREE.Group(); kamer.add(douche);
    var doucheWand = new THREE.Group(); links.add(doucheWand);
    var gx = -0.35, gl = 0.9, gh = 2.0;
    douche.add(mesh(new THREE.BoxGeometry(0.008, gh, gl), M.glas, gx, gh / 2 + 0.01, z0 + gl / 2, false));
    douche.add(doos(0.02, gh, 0.025, M.kraan, gx, gh / 2 + 0.01, z0 + 0.012));
    douche.add(doos(0.014, 0.03, gl, M.kraan, gx, gh - 0.015, z0 + gl / 2));
    var stang = buis(0.01, -x0 + gx, M.kraan, (x0 + gx) / 2, gh - 0.1, z0 + gl - 0.02, "x");  // stabilisatiestang naar de linkerwand
    douche.add(stang);
    douche.add(doos(0.06, 0.006, 1.25, M.kraan, x0 + 0.08, 0.004, z0 + 0.7));
    // regendouche, stang en thermostaat aan de linkerwand
    var dz = z0 + 0.65;  // wereld-z: 65 cm uit de achterwand
    doucheWand.add(opLinks(buis(0.014, 1.15, M.kraan), dz, 1.6, 0.04));
    doucheWand.add(opLinks(buis(0.012, 0.36, M.kraan), dz, 2.17, 0.22).rotateX(Math.PI / 2));
    doucheWand.add(opLinks(mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.012, 48), M.kraan), dz, 2.155, 0.38));
    doucheWand.add(opLinks(buis(0.03, 0.32, M.kraan), dz, 1.03, 0.06).rotateZ(Math.PI / 2));
    doucheWand.add(opLinks(buis(0.034, 0.04, M.kraan), dz - 0.18, 1.03, 0.06).rotateZ(Math.PI / 2));
    doucheWand.add(opLinks(buis(0.034, 0.04, M.kraan), dz + 0.18, 1.03, 0.06).rotateZ(Math.PI / 2));

    /* ---- ligbad */
    var bad = new THREE.Group(); kamer.add(bad);
    var badWand = new THREE.Group(); links.add(badWand);
    var bb = 0.75, bl = 1.7;
    var badBak = bak(bb, bl, 0.56, 0.06, 0.03, 0.22, M.keramiek);
    badBak.position.set(x0 + bb / 2, 0, z0 + bl / 2); bad.add(badBak);
    var water = mesh(new THREE.ShapeGeometry(ronding(bb - 0.13, bl - 0.13, 0.2), 12).rotateX(-Math.PI / 2),
      new THREE.MeshStandardMaterial({ color: 0xbfe0e6, roughness: 0.05, transparent: true, opacity: 0.45 }), x0 + bb / 2, 0.38, z0 + bl / 2, false);
    bad.add(water);
    var bz = z0 + bl / 2;
    badWand.add(opLinks(buis(0.012, 0.17, M.kraan), bz, 0.74, 0.085).rotateX(Math.PI / 2));
    badWand.add(opLinks(buis(0.028, 0.014, M.kraan), bz, 0.74, 0.007).rotateX(Math.PI / 2));
    badWand.add(opLinks(buis(0.024, 0.05, M.kraan), bz - 0.16, 0.74, 0.025).rotateX(Math.PI / 2));
    badWand.add(opLinks(buis(0.024, 0.05, M.kraan), bz + 0.16, 0.74, 0.025).rotateX(Math.PI / 2));

    /* ---- handdoekradiator aan de linkerwand, vooraan */
    var rz = 0.85;  // wereld-z van het midden van de radiator
    [-0.23, 0.23].forEach(function (o) { opLinks(buis(0.014, 1.2, M.kraan), rz + o, 0.9, 0.06); });
    for (var i = 0; i < 11; i++) opLinks(buis(0.009, 0.46, M.kraan), rz, 0.36 + i * 0.11, 0.06).rotateZ(Math.PI / 2);
    opLinks(doos(0.4, 0.5, 0.025, M.handdoek), rz, 1.12, 0.085);

    /* ---- plant rechtsvoor */
    var plant = new THREE.Group(); plant.position.set(W / 2 - 0.25, 0, Dd / 2 - 0.3); kamer.add(plant);
    plant.add(mesh(new THREE.CylinderGeometry(0.13, 0.1, 0.32, 32), M.pot, 0, 0.16, 0));
    var R = rng(3);
    for (var b = 0; b < 11; b++) {
      var bl2 = mesh(new THREE.SphereGeometry(0.11, 12, 8), M.blad, 0, 0, 0);
      bl2.scale.set(0.35, 1.6, 0.08);
      var hoek = b / 11 * Math.PI * 2;
      bl2.position.set(Math.cos(hoek) * 0.07, 0.48 + R() * 0.12, Math.sin(hoek) * 0.07);
      bl2.rotation.set(Math.sin(hoek) * 0.5, -hoek, Math.cos(hoek) * -0.5);
      plant.add(bl2);
    }

    /* ---- keuzes toepassen */
    function toepassen() {
      var w = D.wand[K.wand].tex, v = D.vloer[K.vloer].tex, k = D.kraan[K.kraan];
      M.wand.map = tegelTex(w); M.wand.roughness = w.rough; M.wand.needsUpdate = true;
      M.vloer.map = tegelTex(v); M.vloer.roughness = v.rough; M.vloer.needsUpdate = true;
      M.kraan.color.set(k.kleur); M.kraan.metalness = k.metal; M.kraan.roughness = k.rough;
      if (K.meubel === "hout") { M.meubel.map = houtTex; M.meubel.color.set(0xffffff); M.meubel.roughness = 0.55; }
      else { M.meubel.map = null; M.meubel.color.set(0xf4f3f0); M.meubel.roughness = 0.4; }
      M.meubel.needsUpdate = true;
      var isBad = K.indeling === "bad";
      douche.visible = doucheWand.visible = !isBad;
      bad.visible = badWand.visible = isBad;
      vuil = true;
    }

    /* ---- camera en bediening */
    var controls = new OrbitControls(camera, canvas);
    var DOEL = new THREE.Vector3(0, 0.82, -0.05);
    var BEGIN = { theta: 0.5, phi: 1.1, r: 5.75 };
    controls.target.copy(DOEL);
    controls.enablePan = false;
    controls.minDistance = 2.3; controls.maxDistance = 6.8;
    controls.minPolarAngle = 0.62; controls.maxPolarAngle = 1.48;
    controls.minAzimuthAngle = -0.75; controls.maxAzimuthAngle = 1.05;
    controls.enableDamping = !reduce; controls.dampingFactor = 0.09;
    controls.rotateSpeed = 0.7; controls.zoomSpeed = 0.8;
    controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };

    function zet(theta, phi, r) {
      camera.position.set(DOEL.x + r * Math.sin(phi) * Math.sin(theta), DOEL.y + r * Math.cos(phi), DOEL.z + r * Math.sin(phi) * Math.cos(theta));
      camera.lookAt(DOEL);
    }
    function nu() {
      var o = camera.position.clone().sub(DOEL), r = o.length();
      return { theta: Math.atan2(o.x, o.z), phi: Math.acos(Math.max(-1, Math.min(1, o.y / r))), r: r };
    }
    var anim = null;
    function vlieg(naar, ms) {
      var van = nu();
      if (reduce || !ms) { zet(naar.theta, naar.phi, naar.r); controls.update(); vuil = true; return; }
      anim = { van: van, naar: naar, t0: performance.now(), ms: ms };
    }
    root.querySelectorAll("[data-b3-cam]").forEach(function (knop) {
      knop.addEventListener("click", function () {
        // loopt er nog een beweging, reken dan vanaf het eindpunt (snel klikken telt op)
        var c = anim ? { theta: anim.naar.theta, phi: anim.naar.phi, r: anim.naar.r } : nu(), a = knop.getAttribute("data-b3-cam");
        if (a === "links") c.theta -= 0.3;
        if (a === "rechts") c.theta += 0.3;
        if (a === "in") c.r *= 0.82;
        if (a === "uit") c.r /= 0.82;
        if (a === "terug") c = { theta: BEGIN.theta, phi: BEGIN.phi, r: BEGIN.r };
        c.theta = Math.max(controls.minAzimuthAngle, Math.min(controls.maxAzimuthAngle, c.theta));
        c.r = Math.max(controls.minDistance, Math.min(controls.maxDistance, c.r));
        vlieg(c, 450);
      });
    });
    canvas.addEventListener("keydown", function (e) {
      var map = { ArrowLeft: "links", ArrowRight: "rechts", "+": "in", "=": "in", "-": "uit", Home: "terug" };
      var a = map[e.key];
      if (!a) return;
      e.preventDefault();
      root.querySelector('[data-b3-cam="' + a + '"]').click();
    });

    // wanden tussen camera en kamer verbergen (poppenhuis-weergave)
    function wanden() {
      var p = camera.position;
      links.visible = p.x > x0 + 0.02;
      rechts.visible = p.x < -x0 - 0.02;
      achter.visible = p.z > z0 + 0.02;
      stang.visible = links.visible;
    }

    function maat() {
      var w = stage.clientWidth, h = stage.clientHeight;
      if (!w || !h) return;
      renderer.setSize(w, h, false);
      camera.aspect = w / h; camera.updateProjectionMatrix();
      vuil = true;
    }
    var vuil = true, zichtbaar = true;
    if (window.ResizeObserver) new ResizeObserver(maat).observe(stage); else window.addEventListener("resize", maat);
    if (window.IntersectionObserver) new IntersectionObserver(function (e) { zichtbaar = e[0].isIntersecting; }).observe(stage);
    canvas.addEventListener("webglcontextlost", function (e) {
      e.preventDefault();
      meld("De 3D-weergave is gestopt door je browser. Herlaad de pagina om verder te kijken. Je keuzes en de prijs werken nog.");
    });

    function teken() {
      requestAnimationFrame(teken);
      if (!zichtbaar || document.hidden) return;
      if (anim) {
        var f = Math.min(1, (performance.now() - anim.t0) / anim.ms), e = 1 - Math.pow(1 - f, 3);
        zet(anim.van.theta + (anim.naar.theta - anim.van.theta) * e, anim.van.phi + (anim.naar.phi - anim.van.phi) * e, anim.van.r + (anim.naar.r - anim.van.r) * e);
        if (f >= 1) anim = null;
        vuil = true;
      }
      var bewogen = controls.update();
      if (bewogen || vuil) { wanden(); renderer.render(scene, camera); vuil = false; }
    }

    toepassen();
    maat();
    if (reduce) zet(BEGIN.theta, BEGIN.phi, BEGIN.r);
    else { zet(BEGIN.theta + 0.35, BEGIN.phi - 0.12, BEGIN.r + 0.9); vlieg(BEGIN, 1400); }
    controls.update();
    teken();

    if (/poster=1/.test(location.search)) {
      window.B3poster = function (w, h) {
        anim = null; zet(BEGIN.theta, BEGIN.phi, BEGIN.r); controls.update();
        renderer.setPixelRatio(1); renderer.setSize(w, h, false);
        camera.aspect = w / h; camera.updateProjectionMatrix();
        wanden(); renderer.render(scene, camera);
        return canvas.toDataURL("image/webp", 0.86);
      };
      window.B3cam = nu;
    }
    return { canvas: canvas, toepassen: toepassen };
  }
})();
"""
