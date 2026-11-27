// Bouwstenen voor de terrazzo-render van ronde 4 (b6-terrazzo-badkamer.html): kopie van b4-common.js,
// aangepast voor path tracing met three-gpu-pathtracer (spiegel als metaal, glas met transmissie, lichtgevende
// materialen in plaats van MeshBasicMaterial). Onderaan: echte terrazzo, microcement en de path-tracing-finish.
// Alles procedureel: tegels, hout en terrazzo worden in een canvas getekend.
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { Reflector } from 'three/addons/objects/Reflector.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

// ?pt=1: path tracing met three-gpu-pathtracer (zeer traag in headless swiftshader). Standaard: raster met
// PMREM-omgeving uit de eigen kamer (CubeCamera), echte spiegel (Reflector), zachte schaduwen en GTAO.
export const PT = new URLSearchParams(location.search).has('pt');
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

export { THREE };

/* ------------------------------------------------------------------ */
/* Hulpjes                                                              */
/* ------------------------------------------------------------------ */

export function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function hash2(x, y, s) {
  let h = x * 374761393 + y * 668265263 + s * 2147483647;
  h = (h ^ (h >>> 13)) * 1274126177;
  return ((h ^ (h >>> 16)) >>> 0) / 4294967296;
}

// Tileerbare waarderuis (periode p in roostercellen)
function vnoise(x, y, p, s) {
  const xi = Math.floor(x), yi = Math.floor(y);
  const xf = x - xi, yf = y - yi;
  const f = (t) => t * t * (3 - 2 * t);
  const u = f(xf), v = f(yf);
  const m = (a) => ((a % p) + p) % p;
  const a = hash2(m(xi), m(yi), s), b = hash2(m(xi + 1), m(yi), s);
  const c = hash2(m(xi), m(yi + 1), s), d = hash2(m(xi + 1), m(yi + 1), s);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}
export function fbm2(x, y, p, s, oct = 4) {
  let a = 0.5, f = 1, r = 0;
  for (let i = 0; i < oct; i++) { r += a * vnoise(x * f, y * f, p * f, s + i * 17); f *= 2; a *= 0.5; }
  return r;
}

function canvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

let MAX_ANISO = 8;

function tex(c, color = true, period = null) {
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.anisotropy = MAX_ANISO;
  if (color) t.colorSpace = THREE.SRGBColorSpace;
  if (period) t.repeat.set(1 / period[0], 1 / period[1]);
  t.needsUpdate = true;
  return t;
}

function heightToNormal(hc, strength = 2) {
  const w = hc.width, h = hc.height;
  const src = hc.getContext('2d').getImageData(0, 0, w, h).data;
  const out = canvas(w, h);
  const ctx = out.getContext('2d');
  const img = ctx.createImageData(w, h);
  const H = (x, y) => src[(((y + h) % h) * w + ((x + w) % w)) * 4] / 255;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const dx = (H(x + 1, y) - H(x - 1, y)) * strength;
    const dy = (H(x, y + 1) - H(x, y - 1)) * strength;
    let nx = -dx, ny = dy, nz = 1;
    const l = Math.hypot(nx, ny, nz);
    const i = (y * w + x) * 4;
    img.data[i] = (nx / l * 0.5 + 0.5) * 255;
    img.data[i + 1] = (ny / l * 0.5 + 0.5) * 255;
    img.data[i + 2] = (nz / l * 0.5 + 0.5) * 255;
    img.data[i + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
  return out;
}

function hexToHsl(hex) {
  const c = new THREE.Color(hex);
  const o = {};
  c.getHSL(o, THREE.SRGBColorSpace);
  return o;
}
function hsl(h, s, l) {
  return `hsl(${(h * 360).toFixed(1)},${(Math.max(0, Math.min(1, s)) * 100).toFixed(1)}%,${(Math.max(0, Math.min(1, l)) * 100).toFixed(1)}%)`;
}

// UV's in meters, per vlak afhankelijk van de normaal (box-mapping)
export function worldUV(geo) {
  if (!geo.attributes.normal) geo.computeVertexNormals();
  const p = geo.attributes.position, n = geo.attributes.normal;
  const uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) {
    const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)), az = Math.abs(n.getZ(i));
    let u, v;
    if (az >= ax && az >= ay) { u = p.getX(i); v = p.getY(i); }
    else if (ax >= ay) { u = p.getZ(i); v = p.getY(i); }
    else { u = p.getX(i); v = p.getZ(i); }
    uv[i * 2] = u; uv[i * 2 + 1] = v;
  }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  return geo;
}

function shadowed(m, cast = true) { m.castShadow = cast; m.receiveShadow = true; return m; }

export function box(w, h, d, mat, x = 0, y = 0, z = 0, opts = {}) {
  const g = new THREE.BoxGeometry(w, h, d);
  g.translate(x, y, z);
  if (opts.worldUV !== false) worldUV(g);
  return shadowed(new THREE.Mesh(g, mat), opts.cast !== false);
}

// Box van min- tot max-hoek (handig voor wanden)
export function boxMM(x0, y0, z0, x1, y1, z1, mat, opts = {}) {
  return box(x1 - x0, y1 - y0, z1 - z0, mat, (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2, opts);
}

export function rbox(w, h, d, r, mat, x = 0, y = 0, z = 0, seg = 4) {
  const g = new RoundedBoxGeometry(w, h, d, seg, r);
  g.translate(x, y, z);
  worldUV(g);
  return shadowed(new THREE.Mesh(g, mat));
}

export function cyl(rt, rb, h, mat, x = 0, y = 0, z = 0, seg = 32) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), mat);
  m.position.set(x, y, z);
  return shadowed(m);
}

export function tube(points, r, mat, seg = 48) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)), false, 'catmullrom', 0.1);
  return shadowed(new THREE.Mesh(new THREE.TubeGeometry(curve, seg, r, 16, false), mat));
}

/* ------------------------------------------------------------------ */
/* Tegels                                                               */
/* ------------------------------------------------------------------ */

/**
 * Tegeltexturen (kleur, normal, ruwheid). Afmetingen in meters.
 * o.pattern: 'grid' | 'half' (halfsteens) | 'herring' (visgraat, 45 graden via rotation)
 * o.tw, o.th: tegelmaat · o.joint: voegbreedte · o.base: kleur · o.varL: variatie lichtheid
 * o.grout: voegkleur · o.gloss: ruwheid van het tegeloppervlak (0 = spiegel) · o.surface(ctx,x,y,w,h,R)
 * o.wobble: oneffenheid per tegel (zellige) · o.bevel: afgeschuinde rand in px
 */
export function tileTextures(o) {
  const R = rng(o.seed ?? 1);
  const joint = o.joint ?? 0.002;
  let tiles = [], period;
  if (o.pattern === 'herring') {
    const W = o.th, n = Math.round(o.tw / o.th); // tegel tw x th, tw = n * th
    period = [2 * n * W, 2 * n * W];
    for (let s = -3; s <= 3; s++) for (let k = -2 * n - 2; k <= 4 * n + 2; k++) {
      const ox = k + s * n, oy = k - s * n;
      tiles.push([ox * W, oy * W, n * W, W]);
      tiles.push([(ox + n) * W, (oy + 1 - n) * W, W, n * W]);
    }
  } else {
    const nx = o.nx ?? Math.max(1, Math.round((o.periodX ?? 1.2) / o.tw));
    const ny = o.ny ?? Math.max(2, Math.round((o.periodY ?? 1.2) / o.th / 2) * 2);
    period = [nx * o.tw, ny * o.th];
    for (let r = 0; r < ny; r++) {
      const off = o.pattern === 'half' ? (r % 2) * 0.5 : 0;
      for (let c = -1; c <= nx; c++) tiles.push([(c + off) * o.tw, r * o.th, o.tw, o.th]);
    }
  }
  const ppm = o.ppm ?? Math.min(1400, 2048 / Math.max(period[0], period[1]));
  const Wp = Math.round(period[0] * ppm), Hp = Math.round(period[1] * ppm);
  const c = canvas(Wp, Hp), hc = canvas(Wp, Hp), rc = canvas(Wp, Hp);
  const ctx = c.getContext('2d'), hx = hc.getContext('2d'), rx = rc.getContext('2d');
  ctx.fillStyle = o.grout ?? '#c9c6c0'; ctx.fillRect(0, 0, Wp, Hp);
  hx.fillStyle = '#202020'; hx.fillRect(0, 0, Wp, Hp);
  const gr = Math.round(255 * 0.85);
  rx.fillStyle = `rgb(${gr},${gr},${gr})`; rx.fillRect(0, 0, Wp, Hp);
  const base0 = hexToHsl(o.base ?? '#ffffff');
  const jp = joint * ppm;
  const bevel = o.bevel ?? 2;
  const base2 = o.base2 ? hexToHsl(o.base2) : null;
  for (const [tx, ty, tw, th] of tiles) {
    const odd = base2 && ((Math.round(tx / tw) + Math.round(ty / th)) % 2 !== 0);
    const base = odd ? base2 : base0;
    const L = base.l + (R() - 0.5) * 2 * (o.varL ?? 0.02);
    const S = base.s + (R() - 0.5) * 2 * (o.varS ?? 0.02);
    const Hh = base.h + (R() - 0.5) * 2 * (o.varH ?? 0.004);
    const tint = [R(), R(), R(), R()];
    const rough = (o.gloss ?? 0.15) * (0.8 + R() * 0.4);
    const wob = o.wobble ?? 0;
    const wseed = R() * 1000;
    for (let dx = -1; dx <= 1; dx++) for (let dy = -1; dy <= 1; dy++) {
      const x = (tx + dx * period[0]) * ppm + jp / 2, y = (ty + dy * period[1]) * ppm + jp / 2;
      const w = tw * ppm - jp, h = th * ppm - jp;
      if (x > Wp || y > Hp || x + w < 0 || y + h < 0) continue;
      ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
      ctx.fillStyle = hsl(Hh, S, L); ctx.fillRect(x, y, w, h);
      const surf = odd && o.surface2 !== undefined ? o.surface2 : o.surface;
      if (surf) surf(ctx, x, y, w, h, rng((tint[0] * 1e6) | 0), tint);
      ctx.restore();
      // hoogte: vlak met afgeschuinde rand (en golving bij zellige)
      hx.fillStyle = '#a0a0a0'; hx.fillRect(x, y, w, h);
      hx.fillStyle = '#d0d0d0'; hx.fillRect(x + bevel * 0.5, y + bevel * 0.5, w - bevel, h - bevel);
      hx.fillStyle = '#f0f0f0'; hx.fillRect(x + bevel, y + bevel, w - 2 * bevel, h - 2 * bevel);
      if (wob > 0) {
        for (let k = 0; k < 6; k++) {
          const gx = x + w * (0.15 + 0.7 * hash2(k, 1, wseed)), gy = y + h * (0.15 + 0.7 * hash2(k, 2, wseed));
          const rr = Math.max(w, h) * (0.3 + 0.4 * hash2(k, 3, wseed));
          const g = hx.createRadialGradient(gx, gy, 0, gx, gy, rr);
          const up = hash2(k, 4, wseed) < 0.5;
          g.addColorStop(0, up ? `rgba(255,255,255,${wob})` : `rgba(0,0,0,${wob * 0.7})`);
          g.addColorStop(1, 'rgba(128,128,128,0)');
          hx.save(); hx.beginPath(); hx.rect(x + bevel, y + bevel, w - 2 * bevel, h - 2 * bevel); hx.clip();
          hx.fillStyle = g; hx.fillRect(x, y, w, h); hx.restore();
        }
      }
      const rv = Math.round(255 * Math.min(1, rough));
      rx.fillStyle = `rgb(${rv},${rv},${rv})`; rx.fillRect(x, y, w, h);
    }
  }
  if (o.speck) {
    for (let i = 0; i < Wp * Hp / 30; i++) {
      ctx.fillStyle = R() < 0.5 ? `rgba(0,0,0,${R() * o.speck})` : `rgba(255,255,255,${R() * o.speck})`;
      ctx.fillRect(R() * Wp, R() * Hp, 1 + R() * 1.5, 1 + R() * 1.5);
    }
  }
  const t = {
    map: tex(c, true, period),
    normalMap: tex(heightToNormal(hc, o.normalStrength ?? 3), false, period),
    roughnessMap: tex(rc, false, period),
  };
  if (o.rotate) for (const k in t) { t[k].rotation = o.rotate; t[k].center.set(0, 0); }
  return t;
}

export function tileMaterial(o) {
  const t = tileTextures(o);
  return new THREE.MeshPhysicalMaterial({
    ...t, roughness: 1, metalness: 0,
    normalScale: new THREE.Vector2(o.normalScale ?? 0.6, o.normalScale ?? 0.6),
    clearcoat: o.clearcoat ?? 0, clearcoatRoughness: 0.12,
    envMapIntensity: o.env ?? 0.8,
  });
}

/* Oppervlakken voor tegels (per tegel aangeroepen) */
export const SURF = {
  // zachte betonlook voor donkere tegels (minder vlekkerig)
  betonZacht: (ctx, x, y, w, h, R, t) => SURF.beton(ctx, x, y, w, h, R, t, 0.35),
  // betonlook: vlekkerige wolken en poriën
  beton: (ctx, x, y, w, h, R, tint, soft = 1) => {
    for (let i = 0; i < 26; i++) {
      const gx = x + R() * w, gy = y + R() * h, r = (0.1 + R() * 0.35) * Math.max(w, h);
      const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, r * (soft < 1 ? 2.2 : 1));
      const d = R() < 0.5;
      g.addColorStop(0, d ? `rgba(60,58,54,${(0.05 + R() * 0.07) * soft})` : `rgba(255,255,250,${(0.04 + R() * 0.07) * soft})`);
      g.addColorStop(1, 'rgba(128,128,128,0)');
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    }
    for (let i = 0; i < w * h / 120; i++) {
      ctx.fillStyle = `rgba(40,38,35,${R() * 0.35})`;
      ctx.beginPath(); ctx.arc(x + R() * w, y + R() * h, 0.4 + R() * 1.1, 0, 7); ctx.fill();
    }
  },
  // marmer: zachte grijze aders
  marmer: (ctx, x, y, w, h, R) => {
    ctx.lineCap = 'round';
    for (let v = 0; v < 5; v++) {
      let px = x + R() * w, py = y - 10;
      const ang = 0.6 + R() * 0.6;
      ctx.strokeStyle = `rgba(105,108,115,${0.25 + R() * 0.4})`;
      ctx.lineWidth = 0.6 + R() * (v === 0 ? 3.5 : 1.6);
      ctx.beginPath(); ctx.moveTo(px, py);
      for (let s = 0; s < 40; s++) {
        px += Math.cos(ang) * w / 28 + (R() - 0.5) * w / 30;
        py += Math.sin(ang) * h / 28 + (R() - 0.5) * h / 40 + h / 50;
        ctx.lineTo(px, py);
      }
      ctx.stroke();
    }
    for (let i = 0; i < 8; i++) {
      const gx = x + R() * w, gy = y + R() * h, r = (0.2 + R() * 0.3) * w;
      const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, r);
      g.addColorStop(0, `rgba(200,200,205,${R() * 0.12})`); g.addColorStop(1, 'rgba(200,200,205,0)');
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    }
  },
  // terrazzo: steenslag in een paar tinten
  terrazzo: (colors) => (ctx, x, y, w, h, R) => {
    const n = w * h / 60;
    for (let i = 0; i < n; i++) {
      ctx.fillStyle = colors[(R() * colors.length) | 0];
      const cx = x + R() * w, cy = y + R() * h, r = 0.8 + Math.pow(R(), 3) * 7;
      ctx.beginPath();
      const k = 5 + ((R() * 4) | 0), rot = R() * 6;
      for (let j = 0; j < k; j++) {
        const a = rot + j / k * Math.PI * 2, rr = r * (0.6 + R() * 0.5);
        j ? ctx.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr) : ctx.moveTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr);
      }
      ctx.fill();
    }
  },
  // rijk marmer: wolken, zachte brede aders met een scherpe kern en dunne vertakkingen.
  // o.vein: aderkleur (rgb-string '90,92,98'), o.n: aantal hoofdaders, o.cloud: wolkkleur, o.warm: goudtint
  marmerRijk: (o = {}) => (ctx, x, y, w, h, R) => {
    const vc = o.vein ?? '96,98,104', cc = o.cloud ?? '190,190,196';
    const S = Math.max(w, h);
    for (let i = 0; i < 14; i++) {
      const gx = x + R() * w, gy = y + R() * h, r = (0.15 + R() * 0.45) * S;
      const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, r);
      g.addColorStop(0, `rgba(${cc},${0.05 + R() * 0.12})`); g.addColorStop(1, `rgba(${cc},0)`);
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    }
    if (o.warm) for (let i = 0; i < 6; i++) {
      const gx = x + R() * w, gy = y + R() * h, r = (0.1 + R() * 0.3) * S;
      const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, r);
      g.addColorStop(0, `rgba(${o.warm},${0.06 + R() * 0.08})`); g.addColorStop(1, `rgba(${o.warm},0)`);
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    }
    // vloeiende lijn: hoofdrichting met laagfrequente zijwaartse golving en een beetje ruis
    const flow = (px, py, ang, len, amp, steps = 90) => {
      const pts = [], f1 = 1 + R() * 2, f2 = 3 + R() * 4, p1 = R() * 6, p2 = R() * 6;
      const nx = -Math.sin(ang), ny = Math.cos(ang);
      let jit = 0;
      for (let s = 0; s <= steps; s++) {
        const t = s / steps;
        jit = jit * 0.85 + (R() - 0.5) * 0.04;
        const off = (Math.sin(t * f1 * 3.1 + p1) * 0.7 + Math.sin(t * f2 * 3.1 + p2) * 0.3 + jit) * amp;
        pts.push([px + Math.cos(ang) * len * t + nx * off, py + Math.sin(ang) * len * t + ny * off]);
      }
      return pts;
    };
    const stroke = (pts, lw, a, blur, col = vc) => {
      ctx.filter = blur ? `blur(${blur.toFixed(1)}px)` : 'none';
      ctx.strokeStyle = `rgba(${col},${a})`; ctx.lineWidth = lw; ctx.lineJoin = ctx.lineCap = 'round';
      ctx.beginPath(); pts.forEach(([a1, b1], i) => (i ? ctx.lineTo(a1, b1) : ctx.moveTo(a1, b1))); ctx.stroke();
    };
    const n = o.n ?? 3;
    for (let v = 0; v < n; v++) {
      const ang = (o.angle ?? 1.05) + (R() - 0.5) * 0.5;
      const len = S * 1.5;
      const px = x + w / 2 + (R() - 0.5) * w * 1.2 - Math.cos(ang) * len / 2, py = y + h / 2 + (R() - 0.5) * h * 0.6 - Math.sin(ang) * len / 2;
      const pts = flow(px, py, ang, len, S * (0.04 + R() * 0.08));
      const k = (o.strength ?? 1) * (v === 0 ? 1 : 0.55 + R() * 0.35);
      stroke(pts, S * 0.05 * k, 0.16 * k, S * 0.02);
      stroke(pts, S * 0.014 * k, 0.28 * k, S * 0.004);
      stroke(pts, Math.max(1, S * 0.003 * k), 0.55 * k, 0.6);
      // vertakkingen die zacht wegbuigen
      for (let b = 0; b < (o.branches ?? 4); b++) {
        const i0 = (R() * pts.length * 0.8) | 0, [bx, by] = pts[i0];
        const bang = ang + (R() < 0.5 ? -1 : 1) * (0.35 + R() * 0.5);
        const bp = flow(bx, by, bang, S * (0.15 + R() * 0.35), S * 0.02, 40);
        stroke(bp, S * 0.008, 0.14 * k, S * 0.004);
        stroke(bp, Math.max(0.7, S * 0.0016), (0.3 + R() * 0.25) * k, 0.4);
      }
    }
    // haarfijne aders
    for (let i = 0; i < (o.fine ?? 8); i++) {
      const pts = flow(x + R() * w, y + R() * h, (o.angle ?? 1.05) + (R() - 0.5) * 1.6, S * (0.2 + R() * 0.4), S * 0.02, 40);
      stroke(pts, 0.8, 0.1 + R() * 0.14, 0.3);
    }
    ctx.filter = 'none';
  },
  // fijne terrazzo: veel kleine korrels, wat grotere stukken en stof. o.dens: dichtheid, o.max: max straal (px)
  terrazzoRijk: (colors, o = {}) => (ctx, x, y, w, h, R) => {
    const n = w * h / (o.dens ?? 34);
    for (let i = 0; i < n; i++) {
      ctx.fillStyle = colors[(R() * colors.length) | 0];
      const cx = x + R() * w, cy = y + R() * h, r = 0.6 + Math.pow(R(), 4) * (o.max ?? 11);
      ctx.beginPath();
      const k = 5 + ((R() * 4) | 0), rot = R() * 6;
      for (let j = 0; j < k; j++) {
        const a = rot + j / k * Math.PI * 2, rr = r * (0.55 + R() * 0.55);
        j ? ctx.lineTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr) : ctx.moveTo(cx + Math.cos(a) * rr, cy + Math.sin(a) * rr);
      }
      ctx.closePath(); ctx.fill();
    }
    for (let i = 0; i < n * 1.5; i++) {
      ctx.fillStyle = `rgba(${R() < 0.5 ? '70,60,55' : '255,252,246'},${0.1 + R() * 0.25})`;
      ctx.fillRect(x + R() * w, y + R() * h, 0.8, 0.8);
    }
  },
  // zellige: geglazuurd, kleurverschil binnen de tegel en donkere randjes
  zellige: (ctx, x, y, w, h, R) => {
    for (let i = 0; i < 6; i++) {
      const gx = x + R() * w, gy = y + R() * h, r = (0.3 + R() * 0.6) * w;
      const g = ctx.createRadialGradient(gx, gy, 0, gx, gy, r);
      const d = R() < 0.55;
      g.addColorStop(0, d ? `rgba(10,40,30,${0.1 + R() * 0.25})` : `rgba(210,240,220,${0.06 + R() * 0.16})`);
      g.addColorStop(1, 'rgba(0,0,0,0)');
      ctx.fillStyle = g; ctx.fillRect(x, y, w, h);
    }
    ctx.strokeStyle = 'rgba(5,30,20,0.35)'; ctx.lineWidth = 2.5;
    ctx.strokeRect(x + 1, y + 1, w - 2, h - 2);
  },
  // houtlook (keramisch): nerf in de lengte
  hout: (ctx, x, y, w, h, R) => {
    const horiz = w > h;
    const len = horiz ? w : h, wid = horiz ? h : w;
    for (let i = 0; i < wid / 1.6; i++) {
      const p = (i / (wid / 1.6)) * wid + R() * 2;
      ctx.strokeStyle = R() < 0.5 ? `rgba(70,40,20,${R() * 0.22})` : `rgba(255,225,180,${R() * 0.14})`;
      ctx.lineWidth = 0.6 + R() * 1.6;
      ctx.beginPath();
      const ph = R() * 6, amp = 0.6 + R() * 1.6;
      for (let s = 0; s <= 30; s++) {
        const q = s / 30 * len, o2 = p + Math.sin(q * 0.02 + ph) * amp;
        horiz ? (s ? ctx.lineTo(x + q, y + o2) : ctx.moveTo(x + q, y + o2)) : (s ? ctx.lineTo(x + o2, y + q) : ctx.moveTo(x + o2, y + q));
      }
      ctx.stroke();
    }
    if (R() < 0.5) { // kwastje
      const kx = x + (horiz ? R() * w : w * (0.3 + R() * 0.4)), ky = y + (horiz ? h * (0.3 + R() * 0.4) : R() * h);
      ctx.fillStyle = 'rgba(60,32,15,0.35)';
      ctx.beginPath(); ctx.ellipse(kx, ky, horiz ? 5 : 2.5, horiz ? 2.5 : 5, 0, 0, 7); ctx.fill();
    }
  },
  // portugese / cementtegel-look: vierkant patroon in twee kleuren
  cement: (dark, light) => (ctx, x, y, w, h) => {
    ctx.fillStyle = light; ctx.fillRect(x, y, w, h);
    ctx.fillStyle = dark;
    const cx = x + w / 2, cy = y + h / 2, s = w / 2;
    // hoekkwarten (vormen samen cirkels over de voegen)
    for (const [ax, ay] of [[x, y], [x + w, y], [x, y + h], [x + w, y + h]]) {
      ctx.beginPath(); ctx.arc(ax, ay, s * 0.62, 0, 7); ctx.fill();
    }
    ctx.fillStyle = light;
    for (const [ax, ay] of [[x, y], [x + w, y], [x, y + h], [x + w, y + h]]) {
      ctx.beginPath(); ctx.arc(ax, ay, s * 0.42, 0, 7); ctx.fill();
    }
    ctx.fillStyle = dark;
    for (const [ax, ay] of [[x, y], [x + w, y], [x, y + h], [x + w, y + h]]) {
      ctx.beginPath(); ctx.arc(ax, ay, s * 0.2, 0, 7); ctx.fill();
    }
    // ster in het midden
    ctx.beginPath();
    for (let j = 0; j < 8; j++) {
      const a = j / 8 * Math.PI * 2, r = j % 2 ? s * 0.18 : s * 0.5;
      j ? ctx.lineTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r) : ctx.moveTo(cx + Math.cos(a) * r, cy + Math.sin(a) * r);
    }
    ctx.closePath(); ctx.fill();
    ctx.fillStyle = light; ctx.beginPath(); ctx.arc(cx, cy, s * 0.12, 0, 7); ctx.fill();
    // licht verweerd
    for (let i = 0; i < w * h / 40; i++) {
      ctx.fillStyle = `rgba(128,120,110,${Math.random() * 0.08})`;
      ctx.fillRect(x + Math.random() * w, y + Math.random() * h, 1.5, 1.5);
    }
  },
};

/* ------------------------------------------------------------------ */
/* Overige materialen                                                   */
/* ------------------------------------------------------------------ */

// Wandverf / kalkverf, licht wolkerig
export function plasterMaterial(hex, opts = {}) {
  const R = rng(opts.seed ?? 9);
  const N = 512, c = canvas(N, N), x = c.getContext('2d');
  x.fillStyle = hex; x.fillRect(0, 0, N, N);
  const img = x.getImageData(0, 0, N, N);
  const amp = opts.cloud ?? 0.05;
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const v = (fbm2(i / 64, j / 64, 8, 3) - 0.5) * 2 * amp * 255 + (R() - 0.5) * 6;
    const k = (j * N + i) * 4;
    img.data[k] += v; img.data[k + 1] += v; img.data[k + 2] += v;
  }
  x.putImageData(img, 0, 0);
  const hc = canvas(N, N), hx = hc.getContext('2d');
  const himg = hx.createImageData(N, N);
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const v = fbm2(i / 16, j / 16, 32, 5) * 255; const k = (j * N + i) * 4;
    himg.data[k] = himg.data[k + 1] = himg.data[k + 2] = v; himg.data[k + 3] = 255;
  }
  hx.putImageData(himg, 0, 0);
  return new THREE.MeshStandardMaterial({
    map: tex(c, true, [1.5, 1.5]), normalMap: tex(heightToNormal(hc, 1.2), false, [0.6, 0.6]),
    normalScale: new THREE.Vector2(0.4, 0.4), roughness: opts.roughness ?? 0.92, envMapIntensity: 0.6,
  });
}

// Massief hout of fineer met nerf. dir: 'x' = nerf horizontaal
export function woodMaterial(o = {}) {
  const R = rng(o.seed ?? 4);
  const N = 1024, c = canvas(N, N), x = c.getContext('2d');
  const base = hexToHsl(o.base ?? '#c49a6c');
  // planken van ongeveer 15 cm
  const planks = o.planks ?? 6;
  for (let p = 0; p < planks; p++) {
    const y0 = p / planks * N, hgt = N / planks;
    x.fillStyle = hsl(base.h + (R() - 0.5) * 0.01, base.s * (0.9 + R() * 0.2), base.l * (0.93 + R() * 0.14));
    x.fillRect(0, y0, N, hgt);
    const ph = R() * 10, freq = 0.004 + R() * 0.004;
    for (let i = 0; i < 70; i++) {
      const yy = y0 + R() * hgt;
      x.strokeStyle = R() < 0.6 ? `rgba(60,30,10,${0.05 + R() * (o.contrast ?? 0.16)})` : `rgba(255,230,190,${R() * 0.1})`;
      x.lineWidth = 0.5 + R() * 2.2;
      x.beginPath();
      for (let s = 0; s <= 64; s++) {
        const xx = s / 64 * N;
        const yo = yy + Math.sin(xx * freq + ph + i * 0.13) * (4 + R() * 0.6) + Math.sin(xx * freq * 3.1 + i) * 1.4;
        s ? x.lineTo(xx, yo) : x.moveTo(xx, yo);
      }
      x.stroke();
    }
    if (o.gaps) { x.fillStyle = 'rgba(40,20,8,0.5)'; x.fillRect(0, y0, N, 1.5); }
  }
  for (let i = 0; i < 20000; i++) {
    x.fillStyle = `rgba(50,25,10,${R() * 0.08})`;
    x.fillRect(R() * N, R() * N, 1 + R() * 6, 0.8);
  }
  const t = tex(c, true, [o.size ?? 1.0, o.size ?? 1.0]);
  if (o.dir === 'y') { t.rotation = Math.PI / 2; }
  return new THREE.MeshPhysicalMaterial({
    map: t, roughness: o.roughness ?? 0.55, metalness: 0, clearcoat: o.clearcoat ?? 0.15, clearcoatRoughness: 0.4,
    envMapIntensity: 0.7,
  });
}

export function metalMaterial(kind) {
  const M = {
    chroom: { color: '#f2f4f6', roughness: 0.06, metalness: 1, env: 1.3 },
    rvs: { color: '#d7d9db', roughness: 0.28, metalness: 1, env: 1.1 },
    zwart: { color: '#1b1b1c', roughness: 0.48, metalness: 0.35, env: 0.6 },
    goud: { color: '#d9b26a', roughness: 0.24, metalness: 1, env: 1.2 },
    messing: { color: '#c9a35c', roughness: 0.32, metalness: 1, env: 1.1 },
  }[kind];
  return new THREE.MeshPhysicalMaterial({ color: M.color, roughness: M.roughness, metalness: M.metalness, envMapIntensity: M.env, clearcoat: kind === 'zwart' ? 0.2 : 0 });
}

export const CERAMIC = () => new THREE.MeshPhysicalMaterial({
  color: '#f7f7f5', roughness: 0.18, metalness: 0, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 0.9,
});

export function matteMaterial(hex, roughness = 0.6, env = 0.6) {
  return new THREE.MeshPhysicalMaterial({ color: hex, roughness, metalness: 0, envMapIntensity: env, clearcoat: 0.05 });
}

export function glassMaterial(tint = '#dfeee8') {
  // Doorzichtig glas met reflectie (transmissie botst met de spiegel-reflector, dus hier met opacity)
  return new THREE.MeshPhysicalMaterial({
    color: tint, metalness: 0, roughness: 0.0, ior: 1.5, side: THREE.DoubleSide,
    ...(PT ? { transmission: 1, thickness: 0 } : { transparent: true, opacity: 0.1, depthWrite: false, envMapIntensity: 1.2, specularIntensity: 1 }),
  });
}

export function fabricMaterial(hex) {
  const R = rng(77);
  const N = 256, c = canvas(N, N), x = c.getContext('2d');
  x.fillStyle = '#808080'; x.fillRect(0, 0, N, N);
  for (let i = 0; i < 9000; i++) { x.fillStyle = `rgba(${R() < 0.5 ? 0 : 255},${R() < 0.5 ? 0 : 255},0,${R() * 0.25})`; x.fillRect(R() * N, R() * N, 1, 2); }
  return new THREE.MeshStandardMaterial({
    color: hex, roughness: 1, normalMap: tex(heightToNormal(c, 4), false, [0.05, 0.05]),
    normalScale: new THREE.Vector2(0.7, 0.7), envMapIntensity: 0.4,
  });
}

/* ------------------------------------------------------------------ */
/* Renderer, omgeving en licht                                          */
/* ------------------------------------------------------------------ */

export const RENDER_W = 2400, RENDER_H = 1600; // 1,5x supersampling voor 1600x1067 (3:2)

export function setup(opts = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1);
  renderer.setSize(RENDER_W, RENDER_H, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = opts.exposure ?? 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  MAX_ANISO = renderer.capabilities.getMaxAnisotropy();
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  scene.background = new THREE.Color('#d8d6d0');
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;

  const camera = new THREE.PerspectiveCamera(opts.fov ?? 52, RENDER_W / RENDER_H, 0.05, 60);
  return { renderer, scene, camera };
}

// Camera met horizontale kijkrichting en 'shift lens': verticale lijnen blijven verticaal.
export function archCamera(camera, pos, target, shiftY = 0) {
  camera.position.set(...pos);
  camera.lookAt(target[0], pos[1], target[2]);
  camera.setViewOffset(RENDER_W, RENDER_H, 0, -shiftY * RENDER_H, RENDER_W, RENDER_H);
  camera.updateProjectionMatrix();
}

export const KELVIN = { warm: '#ffc98f', neutraal: '#ffe2c0', koel: '#fff0e2' };

// Inbouwspot: lichtgevend schijfje in het plafond en een spotlight naar beneden
export function spot(scene, x, z, H, color, intensity = 6, opts = {}) {
  const ring = cyl(0.045, 0.045, 0.01, matteMaterial('#e9e9e6', 0.4), x, H - 0.004, z);
  const disc = new THREE.Mesh(new THREE.CircleGeometry(0.03, 24), new THREE.MeshStandardMaterial({ color: '#000000', emissive: color, emissiveIntensity: 12 }));
  disc.rotation.x = Math.PI / 2; disc.position.set(x, H - 0.0105, z);
  scene.add(ring, disc);
  const s = new THREE.SpotLight(color, intensity, 0, opts.angle ?? 0.75, 0.75, 2);
  s.position.set(x, H - 0.03, z); s.radius = opts.radius ?? 0.025;
  s.target.position.set(x + (opts.tx ?? 0), 0, z + (opts.tz ?? 0));
  if (opts.shadow) {
    s.castShadow = true; s.shadow.mapSize.set(1024, 1024); s.shadow.bias = -0.0004; s.shadow.radius = 6;
    s.shadow.camera.near = 0.05; s.shadow.camera.far = 6;
  }
  scene.add(s, s.target);
  return s;
}

/* ------------------------------------------------------------------ */
/* Ruimte: vloer, wanden met openingen, plafond, raam                   */
/* ------------------------------------------------------------------ */

/**
 * Wand als set boxen rond een of meer openingen.
 * side: 'back' (z = 0, u = x), 'left' (x = 0, u = z), 'right' (x = W, u = z)
 * holes: [{u0,u1,v0,v1}] · split: hoogte waarboven matTop geldt (tegels tot split, verf erboven)
 */
export function wall(scene, room, side, matLow, matTop, split, holes = [], T = 0.12, uSplits = []) {
  const len = side === 'back' ? room.w : room.d;
  const H = room.h;
  // verzamel horizontale banden tussen alle v-grenzen, en per band de u-intervallen die dicht zijn
  const vs = new Set([0, H, split]);
  holes.forEach((h) => { vs.add(h.v0); vs.add(h.v1); });
  const vlist = [...vs].filter((v) => v >= 0 && v <= H).sort((a, b) => a - b);
  for (let i = 0; i < vlist.length - 1; i++) {
    const v0 = vlist[i], v1 = vlist[i + 1];
    if (v1 - v0 < 1e-4) continue;
    const vm = (v0 + v1) / 2;
    let segs = [[0, len]];
    holes.filter((h) => vm > h.v0 && vm < h.v1).forEach((h) => {
      segs = segs.flatMap(([a, b]) => {
        const out = [];
        if (h.u0 > a) out.push([a, Math.min(b, h.u0)]);
        if (h.u1 < b) out.push([Math.max(a, h.u1), b]);
        return out;
      });
    });
    segs = segs.flatMap(([a, b]) => {
      const cuts = [a, ...uSplits.filter((u) => u > a && u < b), b];
      return cuts.slice(0, -1).map((c, i) => [c, cuts[i + 1]]);
    });
    for (const [a, b] of segs) {
      const pick = vm < split ? matLow : matTop;
      const mat = typeof pick === 'function' ? pick((a + b) / 2) : pick;
      if (b - a < 1e-4) continue;
      let m;
      if (side === 'back') m = boxMM(a, v0, -T, b, v1, 0, mat);
      else if (side === 'left') m = boxMM(-T, v0, a, 0, v1, b, mat);
      else m = boxMM(room.w, v0, a, room.w + T, v1, b, mat);
      scene.add(m);
    }
  }
}

// Vloer en plafond
export function floorCeil(scene, room, floorMat, ceilMat) {
  scene.add(boxMM(-0.15, -0.1, -0.15, room.w + 0.15, 0, room.d + 1.5, floorMat));
  const c = boxMM(-0.15, room.h, -0.15, room.w + 0.15, room.h + 0.1, room.d + 1.5, ceilMat);
  scene.add(c);
}

/**
 * Raam in de linker- of achterwand (opening moet al in de wand zitten).
 * Matglas dat licht doorlaat, met een zonnestraal (directional light) die schaduw geeft.
 */
export function windowLight(scene, room, side, hole, o = {}) {
  const T = 0.12;
  const frameMat = matteMaterial(o.frame ?? '#f2f1ee', 0.45);
  const revealMat = o.reveal ?? frameMat;
  const g = new THREE.Group();
  const w = hole.u1 - hole.u0, h = hole.v1 - hole.v0, uc = (hole.u0 + hole.u1) / 2;
  // dagkanten (lokale coördinaten: wand in xy-vlak, binnen = +z)
  g.add(box(w, 0.01, T, revealMat, 0, -h / 2 + 0.005, -T / 2));
  g.add(box(w, 0.01, T, revealMat, 0, h / 2 - 0.005, -T / 2));
  g.add(box(0.01, h, T, revealMat, -w / 2 + 0.005, 0, -T / 2));
  g.add(box(0.01, h, T, revealMat, w / 2 - 0.005, 0, -T / 2));
  // vensterbank
  if (o.sill) g.add(box(w + 0.04, 0.02, T + 0.03, o.sill, 0, -h / 2 - 0.01, -T / 2 + 0.015));
  // kozijn
  const fw = 0.055, fz = -T + 0.03;
  g.add(box(w, fw, 0.06, frameMat, 0, h / 2 - fw / 2, fz));
  g.add(box(w, fw, 0.06, frameMat, 0, -h / 2 + fw / 2, fz));
  g.add(box(fw, h, 0.06, frameMat, -w / 2 + fw / 2, 0, fz));
  g.add(box(fw, h, 0.06, frameMat, w / 2 - fw / 2, 0, fz));
  if (o.mullion) g.add(box(fw * 0.8, h, 0.06, frameMat, 0, 0, fz));
  // matglas: zelf lichtgevend, iets blauwig daglicht
  const glow = new THREE.Mesh(new THREE.PlaneGeometry(w - 2 * fw, h - 2 * fw),
    new THREE.MeshBasicMaterial({ color: new THREE.Color(o.glow ?? '#f4f7fb').multiplyScalar(o.glowI ?? 1.6) }));
  glow.position.set(0, 0, fz - 0.005);
  g.add(glow);
  if (side === 'left') { g.rotation.y = Math.PI / 2; g.position.set(0, (hole.v0 + hole.v1) / 2, uc); }
  else { g.position.set(uc, (hole.v0 + hole.v1) / 2, 0); }
  g.traverse((m) => { if (m.isMesh && m !== glow) { m.castShadow = true; m.receiveShadow = true; } });
  scene.add(g);

  // zonlicht door het raam
  const sun = new THREE.DirectionalLight(o.sunColor ?? '#fff1de', o.sun ?? 3.0);
  const dir = new THREE.Vector3(...(o.sunDir ?? [-1, 0.9, -0.3])).normalize();
  const c = side === 'left' ? new THREE.Vector3(0, (hole.v0 + hole.v1) / 2, uc) : new THREE.Vector3(uc, (hole.v0 + hole.v1) / 2, 0);
  sun.position.copy(c).addScaledVector(dir, 8);
  sun.target.position.copy(c).addScaledVector(dir, -2);
  sun.castShadow = true;
  sun.shadow.mapSize.set(4096, 4096);
  Object.assign(sun.shadow.camera, { left: -3, right: 3, top: 3, bottom: -3, near: 2, far: 16 });
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02; sun.shadow.radius = 8;
  scene.add(sun, sun.target);
  // zacht licht dat het raam de ruimte in geeft (geen schaduw)
  const fill = new THREE.PointLight(o.glow ?? '#eef3fb', o.fill ?? 2.2, 0, 2);
  const inward = side === 'left' ? new THREE.Vector3(0.5, 0, 0) : new THREE.Vector3(0, 0, 0.5);
  fill.position.copy(c).add(inward);
  scene.add(fill);
  return { sun, fill };
}

/* ------------------------------------------------------------------ */
/* Meubels en sanitair                                                  */
/* ------------------------------------------------------------------ */

/**
 * Wastafelmeubel tegen de wand (lokaal: achterkant op z = 0, midden x = 0).
 * o.type: 'zwevend' | 'staand' · o.w, o.d, o.h (hoogte kast), o.top (bovenkant blad), o.mat (front)
 * o.blad: materiaal blad · o.sink: 'geintegreerd' | 'opzet' · o.drawers: 1 | 2 · o.panel (klassieke kaders)
 */
export function vanity(o) {
  const g = new THREE.Group();
  const w = o.w ?? 1.2, d = o.d ?? 0.46, top = o.top ?? 0.88, bladT = o.bladT ?? 0.03;
  const kastH = o.h ?? 0.46, y0 = o.type === 'staand' ? 0.0 : top - bladT - kastH;
  const body = o.body ?? o.mat;
  // korpus
  if (o.type === 'staand') {
    // poten en een open plank onderin, of een dichte kast
    const legH = o.legs ?? 0.18;
    const legMat = o.legMat ?? body;
    for (const sx of [-1, 1]) for (const sz of [0.04, d - 0.04]) g.add(box(0.04, legH, 0.04, legMat, sx * (w / 2 - 0.04), legH / 2, sz));
    g.add(box(w, top - bladT - legH, d, body, 0, legH + (top - bladT - legH) / 2, d / 2));
    o._front0 = legH; o._frontH = top - bladT - legH;
  } else {
    g.add(box(w, kastH, d, body, 0, y0 + kastH / 2, d / 2));
    o._front0 = y0; o._frontH = kastH;
  }
  // fronten met naden
  const nd = o.drawers ?? 2, gap = 0.004;
  const fh = (o._frontH - gap * (nd + 1)) / nd;
  for (let i = 0; i < nd; i++) {
    const fy = o._front0 + gap + fh / 2 + i * (fh + gap);
    g.add(box(w - 2 * gap, fh, 0.019, o.mat, 0, fy, d + 0.0095));
    if (o.panel) { // klassieke kaders
      const pm = o.mat;
      g.add(box(w - 0.12, 0.012, 0.01, pm, 0, fy + fh / 2 - 0.05, d + 0.022));
      g.add(box(w - 0.12, 0.012, 0.01, pm, 0, fy - fh / 2 + 0.05, d + 0.022));
      g.add(box(0.012, fh - 0.1, 0.01, pm, -w / 2 + 0.06, fy, d + 0.022));
      g.add(box(0.012, fh - 0.1, 0.01, pm, w / 2 - 0.06, fy, d + 0.022));
    }
    if (o.handle) {
      const hm = o.handle;
      if (o.knobs) g.add(cyl(0.012, 0.012, 0.02, hm, 0, fy, d + 0.03).rotateX(Math.PI / 2));
      else g.add(box(Math.min(0.32, w * 0.35), 0.012, 0.02, hm, 0, fy + fh / 2 - 0.03, d + 0.03));
    } else {
      // greeplijst: donkere sleuf boven het front
      g.add(box(w - 2 * gap, 0.012, 0.01, matteMaterial('#151515', 0.8), 0, fy + fh / 2 - 0.006, d + 0.014));
    }
  }
  // blad
  const blad = o.blad ?? CERAMIC();
  const bw = w + (o.bladOver ?? 0), bd = d + 0.01;
  if (o.sink === 'geintegreerd') {
    const sw = Math.min(0.5, w * 0.42), sd = 0.3, sz = bd / 2 + 0.03, cx = o.sinkX ?? 0;
    const yb = top - bladT / 2;
    // blad rond de wasbak
    g.add(box(bw / 2 + cx - sw / 2 + 0, bladT, bd, blad, (-bw / 2 + cx - sw / 2) / 2, yb, bd / 2));
    g.add(box(bw / 2 - cx - sw / 2, bladT, bd, blad, (bw / 2 + cx + sw / 2) / 2, yb, bd / 2));
    g.add(box(sw, bladT, sz - sd / 2, blad, cx, yb, (sz - sd / 2) / 2));
    g.add(box(sw, bladT, bd - (sz + sd / 2), blad, cx, yb, (bd + sz + sd / 2) / 2));
    // kom: open bak met afgeronde bodem
    const bowlH = 0.11;
    const inner = CERAMIC();
    const bowl = new THREE.Group();
    bowl.add(box(sw, 0.012, sd, inner, 0, top - bowlH, sz));
    bowl.add(box(sw, bowlH, 0.012, inner, 0, top - bowlH / 2, sz - sd / 2 + 0.006));
    bowl.add(box(sw, bowlH, 0.012, inner, 0, top - bowlH / 2, sz + sd / 2 - 0.006));
    bowl.add(box(0.012, bowlH, sd, inner, -sw / 2 + 0.006, top - bowlH / 2, sz));
    bowl.add(box(0.012, bowlH, sd, inner, sw / 2 - 0.006, top - bowlH / 2, sz));
    bowl.position.x = cx;
    g.add(bowl);
    g.add(cyl(0.02, 0.02, 0.004, metalMaterial(o.metal ?? 'chroom'), cx, top - bowlH + 0.008, sz));
    o._tapZ = 0.06; o._sinkZ = sz;
  } else {
    g.add(box(bw, bladT, bd, blad, 0, top - bladT / 2, bd / 2));
    // opzetkom
    const r = o.bowlR ?? 0.2;
    const pts = [];
    const prof = o.bowlShape === 'rond'
      ? [[0, 0], [r * 0.45, 0], [r * 0.8, 0.03], [r * 0.97, 0.08], [r, 0.12], [r * 0.95, 0.12], [r * 0.92, 0.08], [r * 0.75, 0.035], [r * 0.4, 0.018], [0, 0.018]]
      : [[0, 0], [r * 0.7, 0], [r * 0.95, 0.01], [r, 0.03], [r, 0.12], [r * 0.95, 0.12], [r * 0.95, 0.03], [r * 0.7, 0.02], [0, 0.02]];
    for (const [px, py] of prof) pts.push(new THREE.Vector2(px, py));
    const lg = new THREE.LatheGeometry(pts, 64);
    const bowl = shadowed(new THREE.Mesh(lg, o.bowlMat ?? CERAMIC()));
    bowl.position.set(o.sinkX ?? 0, top, d / 2 + 0.02);
    if (o.bowlScale) bowl.scale.set(o.bowlScale[0], 1, o.bowlScale[1]);
    g.add(bowl);
    o._tapZ = 0.05; o._sinkZ = d / 2 + 0.02;
  }
  return g;
}

// Kraan. type: 'wand' (uitloop uit de wand), 'hoog' (opbouw, hoge uitloop), 'kruis' (klassiek, kruisgrepen)
export function tap(type, metal, x, top, zWall = 0, reach = 0.18) {
  const m = metalMaterial(metal);
  const g = new THREE.Group();
  if (type === 'wand') {
    const y = top + 0.22;
    g.add(box(0.07, 0.07, 0.008, m, x, y, zWall + 0.004)); // rozet
    g.add(cyl(0.011, 0.011, reach, m, x, y, zWall + reach / 2, 24).rotateX(Math.PI / 2));
    g.children[1].position.set(x, y, zWall + reach / 2);
    g.add(cyl(0.012, 0.012, 0.04, m, x + 0.12, y, zWall + 0.02, 24).rotateX(Math.PI / 2));
    g.children[2].position.set(x + 0.12, y, zWall + 0.02);
    g.add(box(0.035, 0.035, 0.006, m, x + 0.12, y, zWall + 0.003));
    g.add(box(0.008, 0.008, 0.05, m, x + 0.12, y + 0.022, zWall + 0.035));
  } else if (type === 'hoog' || type === 'laag') {
    const z = zWall, hgt = type === 'hoog' ? 0.28 : 0.17;
    g.add(cyl(0.017, 0.019, hgt, m, x, top + hgt / 2, z));
    g.add(tube([[x, top + hgt - 0.01, z], [x, top + hgt + 0.04, z + 0.03], [x, top + hgt + 0.03, z + reach * 0.7], [x, top + hgt - 0.03, z + reach]], 0.0115, m));
    g.add(box(0.009, 0.009, 0.06, m, x, top + hgt - 0.05, z - 0.028).rotateX(-0.25));
    g.children[2].position.set(x, top + hgt - 0.05, z - 0.03);
  } else if (type === 'kruis') {
    const z = zWall;
    g.add(cyl(0.022, 0.026, 0.12, m, x, top + 0.06, z));
    g.add(tube([[x, top + 0.1, z], [x, top + 0.2, z + 0.02], [x, top + 0.19, z + reach * 0.8], [x, top + 0.13, z + reach]], 0.013, m));
    for (const sx of [-0.09, 0.09]) {
      g.add(cyl(0.016, 0.02, 0.06, m, x + sx, top + 0.03, z));
      g.add(box(0.07, 0.008, 0.008, m, x + sx, top + 0.07, z));
      g.add(box(0.008, 0.008, 0.07, m, x + sx, top + 0.07, z));
      g.add(cyl(0.008, 0.008, 0.02, matteMaterial('#f5f5f2', 0.2), x + sx, top + 0.085, z));
    }
  }
  g.traverse((o) => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; } });
  return g;
}

// Spiegel met echte reflectie. shape: 'rect' | 'rond' | 'boog'. Lokaal: vlak in xy, voorkant +z.
export function mirror(w, h, shape = 'rect', frameMat = null, frameW = 0.02) {
  const g = new THREE.Group();
  let geo;
  if (shape === 'rond') geo = new THREE.CircleGeometry(w / 2, 96);
  else if (shape === 'boog') {
    const s = new THREE.Shape();
    s.moveTo(-w / 2, -h / 2); s.lineTo(w / 2, -h / 2); s.lineTo(w / 2, h / 2 - w / 2);
    s.absarc(0, h / 2 - w / 2, w / 2, 0, Math.PI, false); s.lineTo(-w / 2, -h / 2);
    geo = new THREE.ShapeGeometry(s, 48);
  } else geo = new THREE.PlaneGeometry(w, h);
  const ref = PT ? new THREE.Mesh(geo, new THREE.MeshPhysicalMaterial({ color: '#dfe2e1', metalness: 1, roughness: 0.015 }))
    : new Reflector(geo, { textureWidth: 2048, textureHeight: 2048, color: '#d2d5d3', clipBias: 0.003 });
  ref.position.z = 0.012;
  // achterplaat zodat de spiegel niet zweeft
  const back = new THREE.Mesh(geo, matteMaterial('#2a2826', 0.8)); back.position.z = 0.004; g.add(back);
  g.add(ref);
  // achterplaat
  if (frameMat) {
    let fg;
    if (shape === 'rond') fg = new THREE.TorusGeometry(w / 2 + frameW / 2, frameW / 2, 16, 96);
    else if (shape === 'boog') {
      const s = new THREE.Shape();
      const W2 = w / 2 + frameW, H2 = h / 2 + frameW;
      s.moveTo(-W2, -H2); s.lineTo(W2, -H2); s.lineTo(W2, h / 2 - w / 2); s.absarc(0, h / 2 - w / 2, W2, 0, Math.PI, false); s.lineTo(-W2, -H2);
      const hole = new THREE.Path();
      hole.moveTo(-w / 2, -h / 2); hole.lineTo(-w / 2, h / 2 - w / 2); hole.absarc(0, h / 2 - w / 2, w / 2, Math.PI, 0, true); hole.lineTo(w / 2, -h / 2); hole.lineTo(-w / 2, -h / 2);
      s.holes.push(hole);
      fg = new THREE.ExtrudeGeometry(s, { depth: 0.022, bevelEnabled: false, curveSegments: 48 });
    } else {
      const s = new THREE.Shape();
      const W2 = w / 2 + frameW, H2 = h / 2 + frameW;
      s.moveTo(-W2, -H2); s.lineTo(W2, -H2); s.lineTo(W2, H2); s.lineTo(-W2, H2); s.lineTo(-W2, -H2);
      const hole = new THREE.Path();
      hole.moveTo(-w / 2, -h / 2); hole.lineTo(-w / 2, h / 2); hole.lineTo(w / 2, h / 2); hole.lineTo(w / 2, -h / 2); hole.lineTo(-w / 2, -h / 2);
      s.holes.push(hole);
      fg = new THREE.ExtrudeGeometry(s, { depth: 0.022, bevelEnabled: false });
    }
    const f = shadowed(new THREE.Mesh(fg, frameMat));
    if (shape === 'rond') f.position.z = 0.012;
    g.add(f);
  }
  return g;
}

// Hangtoilet: pot (afgeronde D-vorm), zitting en deksel. Lokaal: wand op z = 0.
export function toilet(mat = CERAMIC()) {
  const g = new THREE.Group();
  const s = new THREE.Shape();
  const w = 0.36, L = 0.53;
  s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w / 2, L - w * 0.62);
  s.bezierCurveTo(w / 2, L - 0.02, 0.06, L, 0, L);
  s.bezierCurveTo(-0.06, L, -w / 2, L - 0.02, -w / 2, L - w * 0.62); s.lineTo(-w / 2, 0);
  const pot = new THREE.ExtrudeGeometry(s, { depth: 0.26, bevelEnabled: true, bevelThickness: 0.025, bevelSize: 0.025, bevelSegments: 6, curveSegments: 32 });
  pot.rotateX(Math.PI / 2);
  const pm = shadowed(new THREE.Mesh(pot, mat));
  pm.position.set(0, 0.40, 0.0);
  pm.scale.set(1, 1, 1);
  g.add(pm);
  // onderkant iets smaller: tweede, kleinere vorm
  const lid = new THREE.ExtrudeGeometry(s, { depth: 0.022, bevelEnabled: true, bevelThickness: 0.008, bevelSize: 0.008, bevelSegments: 4, curveSegments: 32 });
  lid.rotateX(Math.PI / 2);
  const lm = shadowed(new THREE.Mesh(lid, mat));
  lm.position.set(0, 0.46, 0.01);
  lm.scale.set(0.98, 1, 0.97);
  g.add(lm);
  // naad tussen pot en zitting
  g.add(box(0.33, 0.006, 0.44, matteMaterial('#b5b5b2', 0.6), 0, 0.428, 0.24));
  return g;
}

// Bedieningsplaat voor het inbouwreservoir
export function flushPlate(metal, x, y, z = 0) {
  const g = new THREE.Group();
  const m = metalMaterial(metal);
  g.add(rbox(0.24, 0.16, 0.012, 0.004, m, x, y, z + 0.006));
  g.add(rbox(0.07, 0.09, 0.006, 0.003, m, x - 0.04, y, z + 0.014));
  g.add(rbox(0.07, 0.09, 0.006, 0.003, m, x + 0.04, y, z + 0.014));
  return g;
}

// Regendouche met wandarm, thermostaat en handdouche op stang. Lokaal: wand z = 0.
export function shower(metal, x, H, o = {}) {
  const m = metalMaterial(metal);
  const g = new THREE.Group();
  const armY = o.armY ?? 2.15, reach = o.reach ?? 0.38, r = o.headR ?? 0.15;
  if (o.exposed) { // opbouw: zichtbare stijgbuis van thermostaat naar de arm
    g.add(cyl(0.013, 0.013, armY - (o.mixY ?? 1.05), m, x, ((o.mixY ?? 1.05) + armY) / 2, 0.06, 20));
    const el = new THREE.Mesh(new THREE.SphereGeometry(0.016, 16, 10), m); el.position.set(x, armY, 0.06); g.add(el);
  }
  { const ro = cyl(0.03, 0.03, 0.01, m, x, armY, 0.005); ro.rotation.x = Math.PI / 2; if (!o.exposed) g.add(ro); }
  const arm = cyl(0.01, 0.01, reach, m, x, armY, reach / 2, 20); arm.rotation.x = Math.PI / 2; g.add(arm);
  if (o.square) g.add(rbox(r * 2, 0.012, r * 2, 0.004, m, x, armY - 0.02, reach));
  else g.add(cyl(r, r, 0.012, m, x, armY - 0.02, reach, 64));
  const face = new THREE.Mesh(o.square ? new THREE.PlaneGeometry(r * 1.8, r * 1.8) : new THREE.CircleGeometry(r * 0.9, 48), matteMaterial('#2a2a2a', 0.5));
  face.rotation.x = Math.PI / 2; face.position.set(x, armY - 0.0265, reach); g.add(face);
  // thermostaat
  const ty = o.mixY ?? 1.05;
  g.add(rbox(o.mixW ?? 0.32, 0.07, 0.05, 0.02, m, x + (o.mixX ?? 0), ty, 0.025));
  for (const sx of [-0.13, 0.13]) {
    const k = cyl(0.026, 0.026, 0.035, m, x + (o.mixX ?? 0) + sx, ty, 0.06, 32); k.rotation.x = Math.PI / 2; g.add(k);
  }
  // handdouche op een glijstang
  if (o.hand !== false) {
    const hx = x + (o.handX ?? 0.28);
    g.add(cyl(0.011, 0.011, 0.8, m, hx, 1.35, 0.045, 20));
    g.add(box(0.03, 0.03, 0.045, m, hx, 1.75, 0.022)); g.add(box(0.03, 0.03, 0.045, m, hx, 0.95, 0.022));
    const hs = cyl(0.016, 0.022, 0.22, m, hx, 1.58, 0.07, 24); g.add(hs);
    g.add(cyl(0.035, 0.035, 0.02, m, hx, 1.70, 0.075, 32).rotateX(0.6));
    g.children[g.children.length - 1].position.set(hx, 1.7, 0.08);
  }
  return g;
}

// Glazen douchewand (lokaal: paneel loopt in z-richting vanaf de achterwand), met profiel en stabilisatiestang
export function glassPanel(o) {
  const g = new THREE.Group();
  const len = o.len ?? 1.0, h = o.h ?? 2.0, y0 = o.y0 ?? 0.02;
  const glass = new THREE.Mesh(new THREE.BoxGeometry(0.008, h, len), glassMaterial(o.tint ?? '#f6faf8'));
  glass.position.set(0, y0 + h / 2, len / 2);
  g.add(glass);
  // zichtbare glasrand aan de voorkant en bovenkant
  const edge = new THREE.MeshPhysicalMaterial({ color: '#a9cbbd', roughness: 0.05, ior: 1.5, ...(PT ? { transmission: 0.85, thickness: 0 } : { transparent: true, opacity: 0.5 }) });
  g.add(box(0.009, h, 0.004, edge, 0, y0 + h / 2, len - 0.002, { cast: false }));
  g.add(box(0.009, 0.004, len, edge, 0, y0 + h - 0.002, len / 2, { cast: false }));
  const pm = o.profileMat;
  if (pm) {
    const pw = o.profileW ?? 0.022;
    g.add(box(pw, pw, len, pm, 0, y0 + h - pw / 2, len / 2));
    g.add(box(pw, pw, len, pm, 0, y0 + pw / 2, len / 2));
    g.add(box(pw, h, pw, pm, 0, y0 + h / 2, pw / 2));
    g.add(box(pw, h, pw, pm, 0, y0 + h / 2, len - pw / 2));
    for (const f of (o.bars ?? [])) g.add(box(pw * 0.7, pw * 0.7, len, pm, 0, y0 + h * f, len / 2));
    for (const f of (o.vbars ?? [])) g.add(box(pw * 0.7, h, pw * 0.7, pm, 0, y0 + h / 2, len * f));
  } else if (o.wallProfile) {
    g.add(box(0.02, h, 0.025, o.wallProfile, 0, y0 + h / 2, 0.0125));
  }
  if (o.stab) {
    const s = cyl(0.009, 0.009, o.stabLen ?? 0.8, o.stab, 0, y0 + h - 0.05, len - 0.08, 16);
    s.rotation.z = Math.PI / 2; s.position.set(-(o.stabLen ?? 0.8) / 2 * (o.stabSide ?? 1), y0 + h - 0.05, len - 0.08);
    g.add(s);
  }
  return g;
}

// Douchegoot (rvs-rooster) en een licht afschot-vlak
export function drain(x, z, len, metal = 'rvs', alongX = true) {
  const m = metalMaterial(metal);
  const g = new THREE.Group();
  g.add(alongX ? box(len, 0.003, 0.07, m, x, 0.0015, z) : box(0.07, 0.003, len, m, x, 0.0015, z));
  return g;
}

// Vrijstaand bad (ovaal, via lathe en schaal). o.feet: materiaal voor pootjes · o.outer: buitenkleur
export function bath(o = {}) {
  const g = new THREE.Group();
  const L = o.L ?? 1.7, W = o.W ?? 0.78, H = o.H ?? 0.6;
  const prof = [
    [0, 0], [0.62, 0], [0.78, 0.04], [0.9, 0.22], [0.97, 0.6], [1.0, 0.98], [1.0, 1.0], [0.92, 1.0], [0.9, 0.97],
    [0.86, 0.55], [0.76, 0.22], [0.6, 0.12], [0, 0.11],
  ].map(([r, y]) => new THREE.Vector2(r, y));
  const geo = new THREE.LatheGeometry(prof, 96);
  geo.scale(L / 2, H, W / 2);
  geo.computeVertexNormals();
  const outerMat = o.outer ?? CERAMIC();
  const mesh = shadowed(new THREE.Mesh(geo, outerMat));
  // binnenkant altijd wit: tweede lathe voor het binnenste deel
  const innerProf = prof.slice(7).map((v) => new THREE.Vector2(v.x * 0.999, v.y));
  const ig = new THREE.LatheGeometry(innerProf, 96); ig.scale(L / 2, H, W / 2); ig.computeVertexNormals();
  const inner = shadowed(new THREE.Mesh(ig, CERAMIC()));
  const lift = o.feet ? 0.1 : 0;
  mesh.position.y = lift; inner.position.y = lift + 0.0005;
  g.add(mesh, inner);
  if (o.feet) {
    for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
      const f = new THREE.Group();
      f.add(cyl(0.035, 0.022, 0.11, o.feet, 0, 0.055, 0));
      f.add(new THREE.Mesh(new THREE.SphereGeometry(0.03, 20, 12), o.feet));
      f.children[1].position.y = 0.012; f.children[1].castShadow = true;
      f.position.set(sx * L * 0.33, 0, sz * W * 0.27);
      g.add(f);
    }
  }
  return g;
}

// Vrijstaande badkraan op de vloer
export function bathFiller(metal, x, z, rotY = 0) {
  const m = metalMaterial(metal);
  const g = new THREE.Group();
  g.add(cyl(0.05, 0.05, 0.01, m, 0, 0.005, 0));
  g.add(cyl(0.018, 0.018, 0.9, m, 0, 0.45, 0));
  g.add(tube([[0, 0.89, 0], [0, 0.98, 0.04], [0, 0.97, 0.2], [0, 0.9, 0.24]], 0.014, m));
  g.add(cyl(0.025, 0.025, 0.06, m, 0, 0.75, 0.0));
  g.add(cyl(0.02, 0.026, 0.2, m, 0.04, 0.63, 0.02));
  g.position.set(x, 0, z); g.rotation.y = rotY;
  return g;
}

// Handdoekradiator (lokaal: wand z = 0)
export function towelRail(metal, x, y0, w = 0.5, h = 1.2, bars = 9) {
  const m = metalMaterial(metal);
  const g = new THREE.Group();
  for (const sx of [-w / 2, w / 2]) g.add(cyl(0.014, 0.014, h, m, x + sx, y0 + h / 2, 0.06, 20));
  for (let i = 0; i < bars; i++) {
    const b = cyl(0.009, 0.009, w, m, x, y0 + 0.06 + i * (h - 0.12) / (bars - 1), 0.06, 16);
    b.rotation.z = Math.PI / 2; g.add(b);
  }
  for (const sx of [-w / 2, w / 2]) for (const yy of [y0 + 0.1, y0 + h - 0.1]) {
    const s = cyl(0.008, 0.008, 0.06, m, x + sx, yy, 0.03, 12); s.rotation.x = Math.PI / 2; g.add(s);
  }
  return g;
}

// Handdoek over een stang of opgevouwen
export function towel(mat, w, h, x, y, z, fold = false) {
  const g = new THREE.Group();
  if (fold) {
    g.add(rbox(w, h, 0.03, 0.012, mat, x, y, z));
  } else {
    // over een stang: voor- en achterpand
    g.add(rbox(w, h, 0.018, 0.008, mat, x, y - h / 2, z + 0.012));
    g.add(rbox(w, h * 0.8, 0.018, 0.008, mat, x, y - h * 0.4, z - 0.012));
    g.add(rbox(w, 0.03, 0.04, 0.012, mat, x, y, z));
  }
  return g;
}

// Stapel opgevouwen handdoeken
export function towelStack(mats, x, y, z, w = 0.3, d = 0.22) {
  const g = new THREE.Group();
  mats.forEach((m, i) => g.add(rbox(w, 0.045, d, 0.02, m, x, y + 0.0225 + i * 0.046, z)));
  return g;
}

// Sansevieria in een pot
export function plant(x, z, o = {}) {
  const g = new THREE.Group();
  const potH = o.potH ?? 0.3, potR = o.potR ?? 0.13;
  g.add(cyl(potR, potR * 0.82, potH, o.potMat ?? matteMaterial('#d8d2c6', 0.85), 0, potH / 2, 0, 40));
  g.add(cyl(potR * 0.94, potR * 0.94, 0.01, matteMaterial('#3a2c22', 1), 0, potH - 0.015, 0, 32));
  const leafMat = new THREE.MeshStandardMaterial({ color: '#2f5a3a', roughness: 0.55, side: THREE.DoubleSide, envMapIntensity: 0.6 });
  const leafMat2 = new THREE.MeshStandardMaterial({ color: '#4a7a4c', roughness: 0.55, side: THREE.DoubleSide, envMapIntensity: 0.6 });
  const R = rng(o.seed ?? 3);
  const n = o.leaves ?? 11;
  for (let i = 0; i < n; i++) {
    const hgt = (o.h ?? 0.6) * (0.55 + R() * 0.45), wd = 0.045 + R() * 0.02;
    const s = new THREE.Shape();
    s.moveTo(-wd / 2, 0); s.quadraticCurveTo(-wd * 0.7, hgt * 0.6, 0, hgt); s.quadraticCurveTo(wd * 0.7, hgt * 0.6, wd / 2, 0); s.lineTo(-wd / 2, 0);
    const geo = new THREE.ShapeGeometry(s, 12);
    // lichte kromming
    const p = geo.attributes.position;
    for (let k = 0; k < p.count; k++) p.setZ(k, Math.pow(p.getY(k) / hgt, 2) * 0.05 + Math.abs(p.getX(k)) * 0.4);
    geo.computeVertexNormals();
    const leaf = new THREE.Mesh(geo, R() < 0.5 ? leafMat : leafMat2);
    leaf.castShadow = true; leaf.receiveShadow = true;
    const a = R() * Math.PI * 2, rr = R() * potR * 0.5;
    leaf.position.set(Math.cos(a) * rr, potH - 0.02, Math.sin(a) * rr);
    leaf.rotation.set((R() - 0.5) * 0.35, a + Math.PI / 2, (R() - 0.5) * 0.35);
    g.add(leaf);
  }
  g.position.set(x, o.y ?? 0, z);
  return g;
}

// Krukje van hout
export function stool(mat, x, z, h = 0.45, r = 0.16) {
  const g = new THREE.Group();
  g.add(cyl(r, r, 0.035, mat, 0, h - 0.0175, 0, 48));
  for (let i = 0; i < 3; i++) {
    const a = i / 3 * Math.PI * 2;
    const leg = cyl(0.016, 0.014, h - 0.03, mat, Math.cos(a) * r * 0.62, (h - 0.03) / 2, Math.sin(a) * r * 0.62, 16);
    leg.rotation.set(Math.sin(a) * 0.08, 0, -Math.cos(a) * 0.08);
    g.add(leg);
  }
  g.position.set(x, 0, z);
  return g;
}

// Wandlampje (bol of cilinder) met puntlicht
export function sconce(scene, metal, x, y, zWall, color, intensity = 1.2, rotY = 0) {
  const g = new THREE.Group();
  const m = metalMaterial(metal);
  g.add(cyl(0.04, 0.04, 0.012, m, 0, 0, 0.006).rotateX(Math.PI / 2));
  g.children[0].position.set(0, 0, 0.006);
  const arm = cyl(0.008, 0.008, 0.1, m, 0, 0, 0.05); arm.rotation.x = Math.PI / 2; g.add(arm);
  const glob = new THREE.Mesh(new THREE.SphereGeometry(0.06, 32, 16), new THREE.MeshPhysicalMaterial({
    color: '#fff8f0', emissive: color, roughness: 0.7, ior: 1.4,
    ...(PT ? { emissiveIntensity: 0.6, transmission: 1, thickness: 0 } : { emissiveIntensity: 1.5 }),
  }));
  glob.position.set(0, 0.03, 0.12); g.add(glob);
  g.position.set(x, y, zWall); g.rotation.y = rotY;
  scene.add(g);
  const p = new THREE.PointLight(color, intensity, 0, 2); p.radius = 0.04;
  const off = new THREE.Vector3(0, 0.03, 0.15).applyAxisAngle(new THREE.Vector3(0, 1, 0), rotY);
  p.position.set(x + off.x, y + off.y, zWall + off.z);
  scene.add(p);
  return g;
}

// Ledstrip onder een zwevend meubel
export function ledStrip(scene, x, y, z, w, color, intensity = 1.5) {
  const strip = new THREE.Mesh(new THREE.BoxGeometry(w, 0.006, 0.012), new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(2) }));
  strip.position.set(x, y, z); scene.add(strip);
  const pl = new THREE.PointLight(color, intensity, 1.2, 2);
  pl.position.set(x, y - 0.05, z + 0.05); scene.add(pl);
  return strip;
}

// Nis in de achterwand (opening moet in de wand zitten): binnenkant met tegels
export function niche(scene, hole, mat, depth = 0.1) {
  const { u0, u1, v0, v1 } = hole;
  scene.add(boxMM(u0, v0, -depth - 0.01, u1, v1, -depth, mat));
  scene.add(boxMM(u0, v0 - 0.01, -depth, u1, v0, 0, mat));
  scene.add(boxMM(u0, v1, -depth, u1, v1 + 0.01, 0, mat));
  scene.add(boxMM(u0 - 0.01, v0, -depth, u0, v1, 0, mat));
  scene.add(boxMM(u1, v0, -depth, u1 + 0.01, v1, 0, mat));
}

// Fles of zeeppompje (decoratie)
export function bottle(mat, x, y, z, h = 0.18, r = 0.032, capMat = null) {
  const g = new THREE.Group();
  g.add(cyl(r, r, h, mat, x, y + h / 2, z, 32));
  g.add(cyl(r * 0.35, r * 0.35, 0.03, capMat ?? mat, x, y + h + 0.015, z, 16));
  return g;
}

/* ------------------------------------------------------------------ */
/* Renderen en export                                                   */
/* ------------------------------------------------------------------ */

export function makeComposer(renderer, scene, camera, o = {}) {
  const rt = new THREE.WebGLRenderTarget(RENDER_W, RENDER_H, { type: THREE.HalfFloatType, samples: 4 });
  const composer = new EffectComposer(renderer, rt);
  composer.setPixelRatio(1);
  composer.setSize(RENDER_W, RENDER_H);
  composer.addPass(new RenderPass(scene, camera));
  if (o.ao !== false) {
    const ao = new GTAOPass(scene, camera, RENDER_W, RENDER_H);
    ao.output = GTAOPass.OUTPUT.Default;
    ao.blendIntensity = o.aoIntensity ?? 1.0;
    ao.updateGtaoMaterial({ radius: o.aoRadius ?? 0.35, distanceExponent: 1.5, thickness: 1.5, scale: 1.0, samples: 16, distanceFallOff: 1, screenSpaceRadius: false });
    ao.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 6, radiusExponent: 1, rings: 2, samples: 16 });
    composer.addPass(ao);
  }
  composer.addPass(new OutputPass());
  return composer;
}

function shrinkTo(src, w, h) {
  const c = canvas(w, h), x = c.getContext('2d');
  x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high';
  x.drawImage(src, 0, 0, w, h);
  return c;
}

async function encode(c, maxBytes, q0 = 0.86) {
  let q = q0, data;
  for (;;) {
    data = c.toDataURL('image/webp', q);
    const bytes = Math.round((data.length - data.indexOf(',') - 1) * 0.75);
    if (bytes <= maxBytes || q <= 0.5) return { data, q, bytes };
    q = Math.round((q - 0.03) * 100) / 100;
  }
}

export function installExport(renderer, base) {
  window.exportAll = async () => {
    const c1600 = shrinkTo(renderer.domElement, 1600, 1067);
    const c800 = shrinkTo(c1600, 800, 533);
    const c400 = shrinkTo(c800, 400, 267);
    const out = [];
    for (const [c, w, max] of [[c1600, 1600, 245 * 1024], [c800, 800, 90 * 1024], [c400, 400, 32 * 1024]]) {
      const { data, q, bytes } = await encode(c, max);
      const name = `${base}-${w}.webp`;
      const r = await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, data }) });
      out.push({ name, q, bytes, ok: (await r.json()).ok });
    }
    return out;
  };
  // voorbeeld als dataURL (voor controle in de browser zonder op te slaan)
  window.preview = (w = 1200) => shrinkTo(renderer.domElement, w, Math.round(w / 1.5)).toDataURL('image/webp', 0.85);
}

export function pageStyle() {
  const s = document.createElement('style');
  s.textContent = 'html,body{margin:0;background:#222;height:100%;display:flex;align-items:center;justify-content:center}canvas{max-width:100vw;max-height:100vh;width:auto!important;height:auto!important;aspect-ratio:3/2}';
  document.head.appendChild(s);
}

// Gemeenschappelijk einde van elke scène: renderen, export klaarzetten, eventueel automatisch opslaan
export async function finish(renderer, scene, camera, base, o = {}) {
  if (o.envScale) {
    const seen = new Set();
    scene.traverse((m) => {
      const mats = m.material ? (Array.isArray(m.material) ? m.material : [m.material]) : [];
      mats.forEach((mt) => { if (!seen.has(mt) && 'envMapIntensity' in mt) { mt.envMapIntensity *= o.envScale; seen.add(mt); } });
    });
  }
  const composer = makeComposer(renderer, scene, camera, o);
  composer.render();
  installExport(renderer, base);
  window.ready = true;
  if (new URLSearchParams(location.search).has('auto')) {
    window.result = await window.exportAll();
  }
}


/* ------------------------------------------------------------------ */
/* Uitbreidingen ronde 3                                                */
/* ------------------------------------------------------------------ */

// Welke camera (1 = overzicht, 2 = detail) uit ?view=
export const VIEW = Number(new URLSearchParams(location.search).get('view') || 1);

// Camera met eigen brandpuntsafstand (fov in graden)
export function viewCamera(camera, pos, target, shiftY = 0, fov = null) {
  if (fov) camera.fov = fov;
  archCamera(camera, pos, target, shiftY);
}

// Houten lamellen tegen de achterwand (side 'back', u = x) of linkerwand ('left', u = z), met donkere achterplaat
export function slats(scene, side, u0, u1, v0, v1, mat, o = {}) {
  const sw = o.w ?? 0.04, gap = o.gap ?? 0.018, dep = o.depth ?? 0.028, back = o.back ?? matteMaterial('#1c1a18', 0.9);
  const B = (a0, b0, a1, b1, d0, d1, m) => side === 'left' ? boxMM(d0, b0, a0, d1, b1, a1, m) : boxMM(a0, b0, d0, a1, b1, d1, m);
  scene.add(B(u0, v0, u1, v1, 0, 0.008, back));
  for (let u = u0 + gap / 2; u + sw <= u1 + 1e-6; u += sw + gap) scene.add(B(u, v0, u + sw, v1, 0.008, 0.008 + dep, mat));
}

// Massief blok (bank, plateau) met afgeronde randen
export function slab(x0, y0, z0, x1, y1, z1, mat, r = 0.01) {
  const m = rbox(x1 - x0, y1 - y0, z1 - z0, r, mat, (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2);
  return m;
}


/* ------------------------------------------------------------------ */
/* Ronde 4: echte terrazzo, microcement, raam en path tracing           */
/* ------------------------------------------------------------------ */

// Gedempte marmerkorrels: [kleur, gewicht]. Vooral crème, grijs en wit; weinig roze, zwart en terracotta.
export const KORRELS_RUSTIG = [
  ['#ece3d4', 22], ['#f4f0e8', 16], ['#cfc6b8', 16], ['#a8a299', 12], ['#7d7872', 6],
  ['#dcbfb0', 10], ['#c9a596', 5], ['#2f2c2a', 4], ['#a9654a', 4], ['#bf8a6c', 4],
];

function pickW(list, R) {
  const tot = list.reduce((s, [, w]) => s + w, 0);
  let r = R() * tot;
  for (const [c, w] of list) { r -= w; if (r <= 0) return c; }
  return list[0][0];
}

/**
 * Terrazzotextuur: cementbasis met hoekige, gebroken marmerkorrels van 2 tot 25 mm.
 * o.period: herhaling in meters · o.tile: tegelmaat (null = naadloos blad) · o.joint: voeg in m
 * o.cover: deel van het oppervlak met korrels (0,15-0,3) · o.chips: KORRELS_RUSTIG · o.base: cementkleur
 */
export function terrazzoTextures(o = {}) {
  const R = rng(o.seed ?? 11);
  const P = o.period ?? 1.2, N = o.px ?? 2048, ppm = N / P;
  const c = canvas(N, N), x = c.getContext('2d');
  const hc = canvas(N, N), hx = hc.getContext('2d');
  const rc = canvas(N, N), rx = rc.getContext('2d');
  const base = o.base ?? '#e4ddd2';
  // 1. cementbasis met lichte wolken
  x.fillStyle = base; x.fillRect(0, 0, N, N);
  const img = x.getImageData(0, 0, N, N), d = img.data;
  const per = Math.round(P * 3);
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const v = (fbm2(i / N * per, j / N * per, per, 5, 4) - 0.5) * 2 * (o.cloud ?? 0.035) * 255 + (R() - 0.5) * 7;
    const k = (j * N + i) * 4; d[k] += v; d[k + 1] += v * 0.98; d[k + 2] += v * 0.95;
  }
  x.putImageData(img, 0, 0);
  hx.fillStyle = '#c8c8c8'; hx.fillRect(0, 0, N, N);
  rx.fillStyle = '#ffffff'; rx.fillRect(0, 0, N, N);
  // fijn zand in de cement (0,3-1,2 mm), laag contrast
  const sand = Math.round(P * P * (o.sand ?? 9000));
  for (let i = 0; i < sand; i++) {
    const s = (0.3 + R() * 0.9) / 1000 * ppm;
    const t = R();
    x.fillStyle = t < 0.5 ? `rgba(150,142,130,${0.25 + R() * 0.35})` : (t < 0.8 ? `rgba(250,247,240,${0.4 + R() * 0.4})` : `rgba(90,85,80,${0.2 + R() * 0.3})`);
    x.fillRect(R() * N, R() * N, s, s * (0.6 + R() * 0.8));
  }
  // 2. korrels: veel kleine, weinig grote (machtsverdeling), tot de dekking bereikt is
  const target = (o.cover ?? 0.2) * N * N;
  const dmin = o.dmin ?? 2, dmax = o.dmax ?? 25;
  let area = 0, guard = 0;
  const poly = (ctx, cx, cy, pts) => { ctx.beginPath(); pts.forEach(([px, py], i) => (i ? ctx.lineTo(cx + px, cy + py) : ctx.moveTo(cx + px, cy + py))); ctx.closePath(); };
  while (area < target && guard++ < 400000) {
    const dm = dmin * Math.pow(dmax / dmin, Math.pow(R(), o.skew ?? 2.6));
    const r = dm / 2000 * ppm;
    const n = 5 + Math.floor(R() * 5), rot = R() * 6.283, el = 1 + R() * 0.7;
    // hoekige vorm: willekeurige hoeken, ongelijke stralen, soms een rechte breukrand
    const angs = []; for (let k = 0; k < n; k++) angs.push(R() * 6.283); angs.sort((a, b) => a - b);
    const pts = angs.map((a) => {
      const rr = r * (0.55 + R() * 0.45);
      const px = Math.cos(a) * rr * el, py = Math.sin(a) * rr / el;
      return [px * Math.cos(rot) - py * Math.sin(rot), px * Math.sin(rot) + py * Math.cos(rot)];
    });
    const col = new THREE.Color(pickW(o.chips ?? KORRELS_RUSTIG, R));
    const hslc = {}; col.getHSL(hslc, THREE.SRGBColorSpace);
    const L = hslc.l + (R() - 0.5) * 0.07, S = hslc.s * (0.85 + R() * 0.3);
    const cx = R() * N, cy = R() * N;
    for (let ox = -1; ox <= 1; ox++) for (let oy = -1; oy <= 1; oy++) {
      const X = cx + ox * N, Y = cy + oy * N;
      if (X < -3 * r || X > N + 3 * r || Y < -3 * r || Y > N + 3 * r) continue;
      poly(x, X, Y, pts); x.fillStyle = hsl(hslc.h, S, L); x.fill();
      // licht donkerder breukrandje en een zachte ader in grote korrels
      x.strokeStyle = `rgba(60,50,40,${0.12 + R() * 0.1})`; x.lineWidth = Math.max(0.5, r * 0.06); x.stroke();
      if (r > 6) {
        x.save(); poly(x, X, Y, pts); x.clip();
        for (let v = 0; v < 2; v++) {
          x.strokeStyle = R() < 0.5 ? `rgba(255,255,255,${0.12 + R() * 0.15})` : `rgba(70,60,55,${0.08 + R() * 0.1})`;
          x.lineWidth = 0.6 + R() * r * 0.08;
          x.beginPath(); x.moveTo(X - r + R() * r * 0.5, Y - r + R() * 2 * r);
          x.quadraticCurveTo(X + (R() - 0.5) * r, Y + (R() - 0.5) * r, X + r, Y - r + R() * 2 * r); x.stroke();
        }
        const g = x.createRadialGradient(X - r * 0.3, Y - r * 0.3, 0, X, Y, r * 1.2);
        g.addColorStop(0, 'rgba(255,255,255,0.06)'); g.addColorStop(1, 'rgba(0,0,0,0.05)');
        x.fillStyle = g; x.fillRect(X - r * 1.5, Y - r * 1.5, r * 3, r * 3);
        x.restore();
      }
      poly(hx, X, Y, pts); hx.fillStyle = '#cdcdcd'; hx.fill();
      poly(rx, X, Y, pts); rx.fillStyle = `rgb(${190 + R() * 30},${190 + R() * 30},${190 + R() * 30})`; rx.fill();
    }
    area += Math.PI * r * r * 0.72;
  }
  // 3. luchtbelletjes / poriën in de cement
  for (let i = 0; i < P * P * (o.pores ?? 500); i++) {
    const px = R() * N, py = R() * N, s = (0.2 + R() * 0.5) / 1000 * ppm;
    x.fillStyle = `rgba(110,100,92,${0.3 + R() * 0.3})`; x.beginPath(); x.arc(px, py, s, 0, 7); x.fill();
    hx.fillStyle = '#707070'; hx.beginPath(); hx.arc(px, py, s, 0, 7); hx.fill();
  }
  // 4. ruwheid: gepolijst met lichte wolken (poetsbanen)
  rx.globalCompositeOperation = 'multiply';
  for (let i = 0; i < 60 * P * P; i++) {
    const gx = R() * N, gy = R() * N, rr = (0.08 + R() * 0.3) * ppm;
    const g = rx.createRadialGradient(gx, gy, 0, gx, gy, rr);
    const v = Math.round(255 * (0.75 + R() * 0.25));
    g.addColorStop(0, `rgb(${v},${v},${v})`); g.addColorStop(1, 'rgb(255,255,255)');
    rx.fillStyle = g; rx.fillRect(gx - rr, gy - rr, rr * 2, rr * 2);
  }
  rx.globalCompositeOperation = 'source-over';
  // 5. tegelvoegen of gietnaden
  if (o.tile) {
    const tp = o.tile * ppm, jp = Math.max(1.5, (o.joint ?? 0.002) * ppm);
    const nt = Math.round(P / o.tile);
    for (let t = 0; t <= nt; t++) {
      const p = t * tp;
      for (const [ctx, col] of [[x, o.grout ?? '#d2cbc0'], [hx, '#5a5a5a'], [rx, '#ffffff']]) {
        ctx.fillStyle = col; ctx.fillRect(p - jp / 2, 0, jp, N); ctx.fillRect(0, p - jp / 2, N, jp);
      }
    }
    // per tegel een heel lichte toonverschuiving
    for (let a = 0; a < nt; a++) for (let b = 0; b < nt; b++) {
      x.fillStyle = R() < 0.5 ? `rgba(255,250,240,${R() * 0.03})` : `rgba(90,80,70,${R() * 0.025})`;
      x.fillRect(a * tp + jp / 2, b * tp + jp / 2, tp - jp, tp - jp);
    }
  }
  return {
    map: tex(c, true, [P, P]),
    normalMap: tex(heightToNormal(hc, o.normalStrength ?? 1.5), false, [P, P]),
    roughnessMap: tex(rc, false, [P, P]),
  };
}

export function terrazzoMaterial(o = {}) {
  const t = terrazzoTextures(o);
  return new THREE.MeshPhysicalMaterial({
    ...t, metalness: 0, roughness: o.roughness ?? 0.3,
    normalScale: new THREE.Vector2(o.normalScale ?? 0.35, o.normalScale ?? 0.35),
    clearcoat: o.clearcoat ?? 0.25, clearcoatRoughness: o.clearcoatRoughness ?? 0.08,
  });
}

// Microcement / kalkverf: wolkerig, met zachte spaanhalen en wisselende glans
export function microcementMaterial(hex, o = {}) {
  const R = rng(o.seed ?? 21);
  const N = 1024, P = o.period ?? 2.0;
  const c = canvas(N, N), x = c.getContext('2d');
  x.fillStyle = hex; x.fillRect(0, 0, N, N);
  const img = x.getImageData(0, 0, N, N), d = img.data;
  for (let j = 0; j < N; j++) for (let i = 0; i < N; i++) {
    const v = (fbm2(i / 128, j / 128, 8, o.seed ?? 3, 5) - 0.5) * 2 * (o.cloud ?? 0.06) * 255
      + (fbm2(i / 24, j / 24, 43, 7, 2) - 0.5) * 6 + (R() - 0.5) * 4;
    const k = (j * N + i) * 4; d[k] += v; d[k + 1] += v; d[k + 2] += v * 0.97;
  }
  x.putImageData(img, 0, 0);
  const rc = canvas(N, N), rx = rc.getContext('2d');
  const rv = Math.round(255 * (o.rough ?? 0.85)); rx.fillStyle = `rgb(${rv},${rv},${rv})`; rx.fillRect(0, 0, N, N);
  const hc = canvas(N, N), hx = hc.getContext('2d'); hx.fillStyle = '#808080'; hx.fillRect(0, 0, N, N);
  // spaanhalen: brede, lage-contrast bogen
  for (let i = 0; i < (o.strokes ?? 140); i++) {
    const cx = R() * N, cy = R() * N, rr = 60 + R() * 220, a0 = R() * 6.28, a1 = a0 + 0.4 + R() * 0.9;
    const lw = 10 + R() * 40;
    for (let ox = -1; ox <= 1; ox++) for (let oy = -1; oy <= 1; oy++) {
      const light = R() < 0.5;
      x.strokeStyle = light ? `rgba(255,252,246,${0.03 + R() * 0.04})` : `rgba(80,70,60,${0.02 + R() * 0.03})`;
      x.lineWidth = lw; x.beginPath(); x.arc(cx + ox * N, cy + oy * N, rr, a0, a1); x.stroke();
      const g = Math.round(255 * ((o.rough ?? 0.85) - 0.1 - R() * 0.15));
      rx.strokeStyle = `rgba(${g},${g},${g},0.5)`; rx.lineWidth = lw * 0.7; rx.beginPath(); rx.arc(cx + ox * N, cy + oy * N, rr, a0, a1); rx.stroke();
      hx.strokeStyle = `rgba(${light ? 150 : 110},${light ? 150 : 110},${light ? 150 : 110},0.25)`; hx.lineWidth = 1.5;
      hx.beginPath(); hx.arc(cx + ox * N, cy + oy * N, rr + lw / 2, a0, a1); hx.stroke();
    }
  }
  return new THREE.MeshPhysicalMaterial({
    map: tex(c, true, [P, P]), roughnessMap: tex(rc, false, [P, P]), roughness: 1, metalness: 0,
    normalMap: tex(heightToNormal(hc, 1.0), false, [P, P]), normalScale: new THREE.Vector2(0.5, 0.5),
  });
}

// Wand aan de voorkant (achter de camera), zodat de ruimte voor de path tracer dicht is
export function frontWall(scene, room, mat) {
  scene.add(boxMM(-0.15, 0, room.d, room.w + 0.15, room.h, room.d + 0.12, mat));
}

/**
 * Open raam in de linkerwand: kozijn met roede, helder glas, en een vlakke lichtbron (RectAreaLight)
 * net buiten het glas die zacht daglicht de ruimte in stuurt. Plus optioneel zon (DirectionalLight).
 */
export function daylightWindow(scene, room, hole, o = {}) {
  const T = 0.12;
  const frameMat = o.frameMat ?? matteMaterial('#efece6', 0.5);
  const revealMat = o.reveal ?? frameMat;
  const g = new THREE.Group();
  const w = hole.u1 - hole.u0, h = hole.v1 - hole.v0, uc = (hole.u0 + hole.u1) / 2, vc = (hole.v0 + hole.v1) / 2;
  g.add(box(w, 0.01, T, revealMat, 0, -h / 2 + 0.005, -T / 2));
  g.add(box(w, 0.01, T, revealMat, 0, h / 2 - 0.005, -T / 2));
  g.add(box(0.01, h, T, revealMat, -w / 2 + 0.005, 0, -T / 2));
  g.add(box(0.01, h, T, revealMat, w / 2 - 0.005, 0, -T / 2));
  if (o.sill) g.add(box(w + 0.06, 0.025, T + 0.04, o.sill, 0, -h / 2 - 0.0125, -T / 2 + 0.02));
  const fw = 0.06, fz = -T + 0.035;
  g.add(box(w, fw, 0.07, frameMat, 0, h / 2 - fw / 2, fz));
  g.add(box(w, fw, 0.07, frameMat, 0, -h / 2 + fw / 2, fz));
  g.add(box(fw, h, 0.07, frameMat, -w / 2 + fw / 2, 0, fz));
  g.add(box(fw, h, 0.07, frameMat, w / 2 - fw / 2, 0, fz));
  g.add(box(fw * 0.7, h, 0.06, frameMat, 0, 0, fz));
  // matglas (gezandstraald): doorschijnend, laat licht door maar geen uitzicht
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(w - fw, h - fw), PT ? new THREE.MeshPhysicalMaterial({
    color: '#f6f7f6', roughness: o.glassRough ?? 0.35, transmission: 1, thickness: 0, ior: 1.5, side: THREE.DoubleSide,
  }) : new THREE.MeshBasicMaterial({ color: new THREE.Color(o.glow ?? '#f3f5f8').multiplyScalar(o.glowI ?? 1.5), toneMapped: true }));
  glass.position.set(0, 0, fz);
  g.add(glass);
  g.position.set(0, vc, uc); g.rotation.y = Math.PI / 2;
  scene.add(g);
  // vlakke lichtbron buiten het glas, naar binnen gericht (+x)
  if (!PT) RectAreaLightUniformsLib.init();
  const area = new THREE.RectAreaLight(o.color ?? '#f3f6fb', PT ? (o.intensity ?? 12) : (o.rasterIntensity ?? 6), w * 1.15, h * 1.15);
  area.position.set(PT ? -T - 0.06 : 0.01, vc, uc);
  area.lookAt(1, vc, uc);
  scene.add(area);
  if (o.sun) {
    const sun = new THREE.DirectionalLight(o.sunColor ?? '#fff0dc', o.sun);
    const dir = new THREE.Vector3(...(o.sunDir ?? [-1, 0.8, 0.4])).normalize();
    const c = new THREE.Vector3(0, vc, uc);
    sun.position.copy(c).addScaledVector(dir, 8); sun.target.position.copy(c).addScaledVector(dir, -2);
    if (!PT) {
      sun.castShadow = true; sun.shadow.mapSize.set(4096, 4096);
      Object.assign(sun.shadow.camera, { left: -3, right: 3, top: 3, bottom: -3, near: 2, far: 16 });
      sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02; sun.shadow.radius = 10;
      // zacht licht van het raam de ruimte in, zonder schaduw
      const fill = new THREE.PointLight(o.color ?? '#eef3fb', o.fill ?? 1.2, 0, 2);
      fill.position.set(0.6, vc - 0.1, uc); scene.add(fill);
    }
    scene.add(sun, sun.target);
  }
  return area;
}

// Licht naklimmen in de console én naar de server (handig in headless Chrome)
function log(msg) {
  console.log(msg);
  try { fetch('/log', { method: 'POST', body: String(msg) }); } catch (e) { /* geen server */ }
}

// Vignet en heel fijne korrel, alleen in de export
function grade(src, o = {}) {
  const W = src.width, H = src.height;
  const c = canvas(W, H), x = c.getContext('2d');
  x.drawImage(src, 0, 0);
  const g = x.createRadialGradient(W / 2, H * 0.48, Math.min(W, H) * 0.35, W / 2, H / 2, Math.hypot(W, H) * 0.55);
  g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(20,12,6,${o.vignette ?? 0.22})`);
  x.fillStyle = g; x.fillRect(0, 0, W, H);
  const img = x.getImageData(0, 0, W, H), d = img.data, R = rng(5);
  const gr = o.grain ?? 3;
  for (let i = 0; i < d.length; i += 4) { const n = (R() - 0.5) * gr * 2; d[i] += n; d[i + 1] += n; d[i + 2] += n; }
  x.putImageData(img, 0, 0);
  return c;
}

/**
 * Path-tracing-finish: rendert de scène met three-gpu-pathtracer tot `spp` samples, en zet export klaar.
 * ?spp= aantal samples · ?scale= renderformaat t.o.v. 1600x1067 · ?auto=1 slaat de webp's op.
 */
export async function finishPT(renderer, scene, camera, base, o = {}) {
  const q = new URLSearchParams(location.search);
  const scale = Number(q.get('scale') || o.scale || 1);
  const W = Math.round(1600 * scale), H = Math.round(1067 * scale);
  renderer.setSize(W, H, false);
  renderer.shadowMap.enabled = false;
  renderer.toneMapping = o.toneMapping ?? THREE.AgXToneMapping;
  if (o.exposure) renderer.toneMappingExposure = o.exposure;
  camera.aspect = W / H; camera.updateProjectionMatrix();
  // omgeving: zachte lucht buiten het raam
  const { GradientEquirectTexture } = await import('three-gpu-pathtracer');
  const env = new GradientEquirectTexture();
  env.topColor.set(o.skyTop ?? '#cfe0f5'); env.bottomColor.set(o.skyBottom ?? '#efe6d8'); env.update();
  scene.environment = env; scene.background = env; scene.environmentIntensity = o.envIntensity ?? 1.0;
  // three r160 kent environmentRotation nog niet (kwam in r162); de path tracer leest hem wel
  if (!('environmentRotation' in THREE.Scene.prototype)) {
    THREE.Scene.prototype.environmentRotation = new THREE.Euler();
    THREE.Scene.prototype.backgroundRotation = new THREE.Euler();
  }
  const { WebGLPathTracer } = await import('three-gpu-pathtracer');
  const pt = new WebGLPathTracer(renderer);
  pt.tiles.set(o.tiles ?? 2, o.tiles ?? 2);
  pt.bounces = o.bounces ?? 6;
  pt.transmissiveBounces = o.transmissiveBounces ?? 8;
  pt.filterGlossyFactor = o.filterGlossy ?? 0.4;
  pt.renderDelay = 0; pt.minSamples = 0; pt.fadeDuration = 0;
  pt.dynamicLowRes = false; pt.rasterizeScene = false;
  pt.textureSize.set(o.textureSize ?? 2048, o.textureSize ?? 2048);
  const t0 = performance.now();
  log(`[${base}] scene opbouwen ${W}x${H}`);
  pt.setScene(scene, camera);
  log(`[${base}] scene klaar na ${((performance.now() - t0) / 1000).toFixed(1)} s`);
  const spp = Number(q.get('spp') || o.spp || 64);
  let last = 0;
  while (pt.samples < spp) {
    pt.renderSample();
    const s = Math.floor(pt.samples);
    // af en toe 1 pixel teruglezen: dwingt de GPU-wachtrij leeg, zodat de voortgang klopt
    if (s !== last && s % 4 === 0) { const gl = renderer.getContext(); renderer.setRenderTarget(null); gl.readPixels(0, 0, 1, 1, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4)); }
    if (s !== last && (s % 8 === 0 || s === 1)) {
      log(`[${base}] sample ${s}/${spp} na ${((performance.now() - t0) / 1000).toFixed(0)} s`);
    }
    last = s;
    await new Promise((r) => setTimeout(r, 0));
  }
  pt.renderSample(); // laatste keer naar het canvas
  log(`[${base}] klaar: ${spp} samples in ${((performance.now() - t0) / 1000).toFixed(0)} s`);
  window.exportAll = async () => {
    const c1600 = grade(shrinkTo(renderer.domElement, 1600, 1067), o);
    const c800 = shrinkTo(c1600, 800, 533);
    const c400 = shrinkTo(c800, 400, 267);
    const out = [];
    for (const [c, w, max] of [[c1600, 1600, 290 * 1024], [c800, 800, 95 * 1024], [c400, 400, 32 * 1024]]) {
      const { data, q: qq, bytes } = await encode(c, max, 0.88);
      const name = `${base}-${w}.webp`;
      const r = await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, data }) });
      out.push({ name, q: qq, bytes, ok: (await r.json()).ok });
    }
    log(`[${base}] opgeslagen ${JSON.stringify(out)}`);
    return out;
  };
  window.ready = true;
  if (q.has('auto')) window.result = await window.exportAll();
  else if (q.has('preview')) {
    const data = grade(shrinkTo(renderer.domElement, 1600, 1067), o).toDataURL('image/webp', 0.9);
    await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: `preview-${base}.webp`, data, preview: true }) });
    log(`[${base}] preview opgeslagen`);
  }
}


/**
 * Raster-finish: omgeving uit de eigen kamer (CubeCamera -> PMREM) voor reflecties in vloer, messing en glas,
 * GTAO, AgX-tonemapping, en export met vignet en fijne korrel.
 */
export async function finishRaster(renderer, scene, camera, base, o = {}) {
  renderer.toneMapping = o.toneMapping ?? THREE.AgXToneMapping;
  renderer.toneMappingExposure = o.exposure ?? 1.0;
  renderer.shadowMap.type = THREE.VSMShadowMap;
  scene.traverse((m) => { if (m.isLight && m.shadow) { m.shadow.radius = Math.max(m.shadow.radius, 8); m.shadow.blurSamples = 16; } });
  if (o.roomEnv !== false) {
    const cubeRT = new THREE.WebGLCubeRenderTarget(512, { type: THREE.HalfFloatType });
    const cc = new THREE.CubeCamera(0.05, 20, cubeRT);
    cc.position.set(...(o.probe ?? [1.6, 1.3, 1.8]));
    scene.add(cc);
    const tm = renderer.toneMapping; renderer.toneMapping = THREE.NoToneMapping;
    cc.update(renderer, scene);
    renderer.toneMapping = tm;
    const pmrem = new THREE.PMREMGenerator(renderer);
    const roomEnv = pmrem.fromCubemap(cubeRT.texture).texture;
    scene.environment = roomEnv;
    scene.remove(cc);
  }
  if (o.envScale) {
    const seen = new Set();
    scene.traverse((m) => {
      const mats = m.material ? (Array.isArray(m.material) ? m.material : [m.material]) : [];
      mats.forEach((mt) => { if (!seen.has(mt) && 'envMapIntensity' in mt) { mt.envMapIntensity *= o.envScale; seen.add(mt); } });
    });
  }
  const composer = makeComposer(renderer, scene, camera, o);
  composer.render();
  window.exportAll = async () => {
    const c1600 = grade(shrinkTo(renderer.domElement, 1600, 1067), o);
    const c800 = shrinkTo(c1600, 800, 533);
    const c400 = shrinkTo(c800, 400, 267);
    const out = [];
    for (const [c, w, max] of [[c1600, 1600, 290 * 1024], [c800, 800, 95 * 1024], [c400, 400, 32 * 1024]]) {
      const { data, q: qq, bytes } = await encode(c, max, 0.88);
      const name = `${base}-${w}.webp`;
      const r = await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, data }) });
      out.push({ name, q: qq, bytes, ok: (await r.json()).ok });
    }
    log(`[${base}] opgeslagen ${JSON.stringify(out)}`);
    return out;
  };
  window.ready = true;
  const q = new URLSearchParams(location.search);
  if (q.has('auto')) window.result = await window.exportAll();
  else if (q.has('preview')) {
    const data = grade(shrinkTo(renderer.domElement, 1600, 1067), o).toDataURL('image/webp', 0.9);
    await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: `preview-${base}.webp`, data, preview: true }) });
    log(`[${base}] preview opgeslagen`);
  }
}

export async function finishAny(renderer, scene, camera, base, o = {}) {
  if (PT) return finishPT(renderer, scene, camera, base, { ...o, ...(o.pt || {}) });
  return finishRaster(renderer, scene, camera, base, { ...o, ...(o.raster || {}) });
}
