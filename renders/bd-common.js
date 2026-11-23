// Gedeelde bouwstenen voor de badkamer-renders (bd-*.html).
// three.js r160, alles procedureel: texturen worden in een canvas getekend,
// er worden geen externe beelden geladen.
//
// Belichting: de scène wordt N keer gerenderd en gemiddeld (accumulatie).
// Per frame verschuiven de lichtbronnen een beetje: een spotje op een
// willekeurige plek in het raam (vlak raamlicht met zachte schaduwen), een
// 'kaatslicht' op een willekeurige plek op muur of vloer (indirect licht met
// contactschaduw) en de inbouwspots met een kleine uitwijking. Daarbij beweegt
// de camera subpixel mee voor anti-aliasing.
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
import { Reflector } from 'three/addons/objects/Reflector.js';
import { mergeVertices } from 'three/addons/utils/BufferGeometryUtils.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { FullScreenQuad } from 'three/addons/postprocessing/Pass.js';

export { THREE };

// Kaatslichten (decay > 2,0005) geven alleen diffuus licht: geen hooglichten, die
// bij verspringende posities als stippen op glad materiaal verschijnen.
{
  const chunk = THREE.ShaderChunk.lights_fragment_begin;
  const a = chunk.indexOf('#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )');
  const b = chunk.indexOf('RE_Direct(', a);
  const e = chunk.indexOf(';', b) + 1;
  const call = chunk.slice(b, e);
  const patched = `{
		vec3 bdSpec = reflectedLight.directSpecular;
		#ifdef USE_CLEARCOAT
		vec3 bdCoat = clearcoatSpecularDirect;
		#endif
		${call}
		if ( spotLight.decay > 2.0005 ) {
			reflectedLight.directSpecular = bdSpec;
			#ifdef USE_CLEARCOAT
			clearcoatSpecularDirect = bdCoat;
			#endif
		}
		}`;
  if (a > 0 && b > 0) THREE.ShaderChunk.lights_fragment_begin = chunk.slice(0, b) + patched + chunk.slice(e);
  else console.warn('shaderpatch niet toegepast');
}

export const RENDER_W = 2400, RENDER_H = 1600; // 1,5x supersampling voor 1600x1067 (3:2)

/* ------------------------------------------------------------------ */
/* Ruis en hulpjes                                                      */
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

export function hash2(ix, iy, seed = 0) {
  let h = (Math.imul(ix, 374761393) + Math.imul(iy, 668265263) + Math.imul(seed, 1442695041)) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967295;
}

export function noise(x, y, seed = 0) {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
  const a = hash2(ix, iy, seed), b = hash2(ix + 1, iy, seed);
  const c = hash2(ix, iy + 1, seed), d = hash2(ix + 1, iy + 1, seed);
  return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
}

// periodieke ruis: herhaalt na px x py cellen (naadloze texturen)
function pnoise(x, y, px, py, seed = 0) {
  const ix = Math.floor(x), iy = Math.floor(y);
  const fx = x - ix, fy = y - iy;
  const ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
  const m = (v, p) => ((v % p) + p) % p;
  const x0 = m(ix, px), x1 = m(ix + 1, px), y0 = m(iy, py), y1 = m(iy + 1, py);
  const a = hash2(x0, y0, seed), b = hash2(x1, y0, seed);
  const c = hash2(x0, y1, seed), d = hash2(x1, y1, seed);
  return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy;
}

// periodieke fbm; x,y in [0,1) van de textuur, freq = cellen per textuur
export function pfbm(x, y, freqX, freqY, seed = 0, oct = 4) {
  let s = 0, amp = 0.5, norm = 0, fx = freqX, fy = freqY;
  for (let i = 0; i < oct; i++) {
    s += amp * pnoise(x * fx, y * fy, fx, fy, seed + i * 17);
    norm += amp; fx *= 2; fy *= 2; amp *= 0.5;
  }
  return s / norm;
}

export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a)); return t * t * (3 - 2 * t); };
const mix = (a, b, t) => a + (b - a) * t;

function hexRGB(c) { const n = parseInt(c.slice(1), 16); return [(n >> 16) & 255, (n >> 8) & 255, n & 255]; }

function canvas(w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  return c;
}

let MAX_ANISO = 8;

function tex(c, color, sizeMeters) {
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.anisotropy = MAX_ANISO;
  if (color) t.colorSpace = THREE.SRGBColorSpace;
  if (sizeMeters) t.repeat.set(1 / sizeMeters[0], 1 / sizeMeters[1]);
  t.needsUpdate = true;
  return t;
}

// Maakt van een hoogteveld (meters) een normal map. ppm = pixels per meter.
function normalCanvas(hgt, w, h, ppm) {
  const out = canvas(w, h);
  const ctx = out.getContext('2d');
  const img = ctx.createImageData(w, h);
  const d = img.data;
  const k = ppm / 2;
  for (let y = 0; y < h; y++) {
    const ym = ((y - 1 + h) % h) * w, yp = ((y + 1) % h) * w, yr = y * w;
    for (let x = 0; x < w; x++) {
      const xm = (x - 1 + w) % w, xp = (x + 1) % w;
      const dx = (hgt[yr + xp] - hgt[yr + xm]) * k;
      const dy = (hgt[yp + x] - hgt[ym + x]) * k;
      let nx = -dx, ny = dy, nz = 1;
      const l = Math.hypot(nx, ny, nz);
      const i = (yr + x) * 4;
      d[i] = (nx / l * 0.5 + 0.5) * 255;
      d[i + 1] = (ny / l * 0.5 + 0.5) * 255;
      d[i + 2] = (nz / l * 0.5 + 0.5) * 255;
      d[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  return out;
}

function grayCanvas(arr, w, h) {
  const c = canvas(w, h), ctx = c.getContext('2d');
  const img = ctx.createImageData(w, h);
  for (let i = 0; i < w * h; i++) {
    const v = clamp(arr[i]) * 255;
    img.data[i * 4] = img.data[i * 4 + 1] = img.data[i * 4 + 2] = v;
    img.data[i * 4 + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
  return c;
}

function rgbCanvas(arr, w, h) {
  const c = canvas(w, h), ctx = c.getContext('2d');
  const img = ctx.createImageData(w, h);
  for (let i = 0; i < w * h; i++) {
    img.data[i * 4] = arr[i * 3]; img.data[i * 4 + 1] = arr[i * 3 + 1]; img.data[i * 4 + 2] = arr[i * 3 + 2];
    img.data[i * 4 + 3] = 255;
  }
  ctx.putImageData(img, 0, 0);
  return c;
}

// UV's in meters, per vlak afhankelijk van de normaal (box-mapping)
export function worldUV(geo) {
  if (!geo.attributes.normal) geo.computeVertexNormals();
  const p = geo.attributes.position, n = geo.attributes.normal;
  const uv = new Float32Array(p.count * 2);
  for (let i = 0; i < p.count; i++) {
    const ax = Math.abs(n.getX(i)), ay = Math.abs(n.getY(i)), az = Math.abs(n.getZ(i));
    let u, v;
    if (az >= ax && az >= ay) { u = p.getX(i) * Math.sign(n.getZ(i) || 1); v = p.getY(i); }
    else if (ax >= ay) { u = -p.getZ(i) * Math.sign(n.getX(i) || 1); v = p.getY(i); }
    else { u = p.getX(i); v = -p.getZ(i); }
    uv[i * 2] = u; uv[i * 2 + 1] = v;
  }
  geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  return geo;
}

// gladde normalen na vervormen van een (niet-geïndexeerde) geometrie
function smoothNormals(geo) {
  geo.deleteAttribute('uv');
  geo.deleteAttribute('normal');
  const m = mergeVertices(geo, 1e-5);
  m.computeVertexNormals();
  return m;
}

function mesh(geo, mat, cast = true) {
  const m = new THREE.Mesh(geo, mat);
  m.castShadow = cast; m.receiveShadow = true;
  return m;
}

export function box(w, h, d, mat, x = 0, y = 0, z = 0, opts = {}) {
  const g = new THREE.BoxGeometry(w, h, d);
  g.translate(x, y, z);
  if (opts.worldUV !== false) worldUV(g);
  return mesh(g, mat, opts.cast !== false);
}

// afgeronde doos; r = straal van de ronding
export function rbox(w, h, d, r, mat, x = 0, y = 0, z = 0, opts = {}) {
  const g = new RoundedBoxGeometry(w, h, d, opts.seg ?? 3, Math.min(r, w / 2 - 1e-4, h / 2 - 1e-4, d / 2 - 1e-4));
  g.translate(x, y, z);
  if (opts.worldUV) worldUV(g);
  return mesh(g, mat, opts.cast !== false);
}

export function cyl(r, h, mat, x = 0, y = 0, z = 0, opts = {}) {
  const g = new THREE.CylinderGeometry(opts.rTop ?? r, r, h, opts.seg ?? 32, 1, !!opts.open);
  if (opts.axis === 'x') g.rotateZ(Math.PI / 2);
  if (opts.axis === 'z') g.rotateX(Math.PI / 2);
  g.translate(x, y, z);
  return mesh(g, mat, opts.cast !== false);
}

export function cylBetween(a, b, r, mat, seg = 16) {
  const len = a.distanceTo(b);
  const g = new THREE.CylinderGeometry(r, r, len, seg, 1, false);
  const m = mesh(g, mat);
  m.position.copy(a).add(b).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), b.clone().sub(a).normalize());
  return m;
}

export function tube(points, r, mat, seg = 64) {
  const curve = new THREE.CatmullRomCurve3(points.map((p) => new THREE.Vector3(...p)), false, 'catmullrom', 0.2);
  return mesh(new THREE.TubeGeometry(curve, seg, r, 20, false), mat);
}

// vlakke vorm met afgeronde hoeken (in xy-vlak)
export function roundedRectShape(w, h, r, cx = 0, cy = 0) {
  const s = new THREE.Shape();
  const x = cx - w / 2, y = cy - h / 2;
  r = Math.min(r, w / 2, h / 2);
  s.moveTo(x + r, y);
  s.lineTo(x + w - r, y); s.quadraticCurveTo(x + w, y, x + w, y + r);
  s.lineTo(x + w, y + h - r); s.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  s.lineTo(x + r, y + h); s.quadraticCurveTo(x, y + h, x, y + h - r);
  s.lineTo(x, y + r); s.quadraticCurveTo(x, y, x + r, y);
  return s;
}

function roundedRectPath(w, h, r, cx = 0, cy = 0) {
  const p = new THREE.Path();
  const x = cx - w / 2, y = cy - h / 2;
  r = Math.min(r, w / 2, h / 2);
  p.moveTo(x + r, y);
  p.lineTo(x + w - r, y); p.quadraticCurveTo(x + w, y, x + w, y + r);
  p.lineTo(x + w, y + h - r); p.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  p.lineTo(x + r, y + h); p.quadraticCurveTo(x, y + h, x, y + h - r);
  p.lineTo(x, y + r); p.quadraticCurveTo(x, y, x + r, y);
  return p;
}

// Bovenaanzicht van een toiletpot: achterkant (y=0) bijna recht, voorkant rond.
function eggPoints(w, l, n = 72, back = 4) {
  const pts = [];
  for (let i = 0; i < n; i++) {
    const t = (i / n) * Math.PI * 2;
    const c = Math.cos(t), s = Math.sin(t);
    // voorste helft (s > 0) ellips, achterste helft superellips
    const e = s > 0 ? 2 : back;
    const sx = Math.sign(c) * Math.pow(Math.abs(c), 2 / e);
    const sy = Math.sign(s) * Math.pow(Math.abs(s), 2 / e);
    const yy = s > 0 ? sy * l * 0.62 : sy * l * 0.38;
    // naar voren iets smaller (eivorm)
    const narrow = 1 - 0.12 * Math.max(0, yy / (l * 0.62));
    pts.push(new THREE.Vector2(sx * w / 2 * narrow, yy + l * 0.38));
  }
  return pts;
}

function extrudeY(shape, depth, bevel = 0.004, segs = 3, curveSegs = 48) {
  const g = new THREE.ExtrudeGeometry(shape, {
    depth: depth - 2 * bevel, bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel,
    bevelSegments: segs, curveSegments: curveSegs, steps: 1,
  });
  g.translate(0, 0, bevel);
  g.rotateX(-Math.PI / 2); // vorm-y wordt -z, extrusie langs +y
  return g;
}

/* ------------------------------------------------------------------ */
/* Materialen                                                           */
/* ------------------------------------------------------------------ */

export const MAT = {
  chrome: () => new THREE.MeshStandardMaterial({ color: '#f4f6f8', metalness: 1, roughness: 0.06, envMapIntensity: 1.3 }),
  black: () => new THREE.MeshStandardMaterial({ color: '#141414', metalness: 0.35, roughness: 0.42, envMapIntensity: 0.8 }),
  brushed: () => new THREE.MeshStandardMaterial({ color: '#c9c6c0', metalness: 1, roughness: 0.28, envMapIntensity: 1.1 }),
  gold: () => new THREE.MeshStandardMaterial({ color: '#d9b77e', metalness: 1, roughness: 0.25, envMapIntensity: 1.1 }),
  ceramic: (c = '#f7f7f4') => new THREE.MeshPhysicalMaterial({ color: c, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.06, envMapIntensity: 0.8 }),
  whiteMatte: (c = '#f2f1ec') => new THREE.MeshStandardMaterial({ color: c, roughness: 0.55, envMapIntensity: 0.6 }),
  plastic: (c = '#eeeeea') => new THREE.MeshStandardMaterial({ color: c, roughness: 0.35, envMapIntensity: 0.6 }),
  rubber: (c = '#2a2a2a') => new THREE.MeshStandardMaterial({ color: c, roughness: 0.85 }),
  sealant: (c = '#f1f0ec') => new THREE.MeshStandardMaterial({ color: c, roughness: 0.32, envMapIntensity: 0.7 }),
  // glas zonder transmissie (die gaf vuurvliegjes): zie glassMesh()
  glassTint: (tint = '#b4cdc4', opacity = 0.07) => new THREE.MeshBasicMaterial({ color: tint, transparent: true, opacity, depthWrite: false }),
  // alleen omgevingsreflectie, geen hooglichten van (verspringende) puntlichten
  glassReflect: (k = 0.09) => {
    const m = new THREE.MeshBasicMaterial({ color: '#000000', combine: THREE.AddOperation, reflectivity: k, transparent: true, blending: THREE.AdditiveBlending, depthWrite: false });
    m.userData.needsEnv = true;
    return m;
  },
  glassEdge: () => new THREE.MeshStandardMaterial({ color: '#86b0a2', roughness: 0.1, transparent: true, opacity: 0.75, envMapIntensity: 1 }),
  frosted: (glow = 1.6) => new THREE.MeshStandardMaterial({ color: '#ffffff', emissive: '#f4f7fb', emissiveIntensity: glow, roughness: 0.9 }),
};

// Gips/latex op wand of plafond
export function plasterMaterial(hex = '#f1eee8', seed = 3) {
  const S = 512, ppm = 512 / 1.5;
  const col = new Uint8ClampedArray(S * S * 3), hgt = new Float32Array(S * S);
  const [r, g, b] = hexRGB(hex);
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const n = pfbm(x / S, y / S, 6, 6, seed, 5);
    const f = 1 + (n - 0.5) * 0.04 + (hash2(x, y, seed) - 0.5) * 0.015;
    const i = y * S + x;
    col[i * 3] = r * f; col[i * 3 + 1] = g * f; col[i * 3 + 2] = b * f;
    hgt[i] = (pfbm(x / S, y / S, 40, 40, seed + 5, 3) - 0.5) * 0.00015;
  }
  return new THREE.MeshStandardMaterial({
    map: tex(rgbCanvas(col, S, S), true, [1.5, 1.5]),
    normalMap: tex(normalCanvas(hgt, S, S, ppm), false, [1.5, 1.5]),
    roughness: 0.92, envMapIntensity: 0.5,
  });
}

/*
 * Tegels met voegen. Alle maten in meters.
 * tile: [breedte, hoogte] inclusief voeg; grout: voegbreedte.
 * pattern: 'stack' (recht), 'half' (halfsteens), 'third' (1/3 verband).
 * surface: 'glossy', 'matte', 'concrete', 'marble', 'terrazzo', 'zellige'.
 */
export function tileMaterial(opts = {}) {
  const {
    tile = [0.3, 0.6], grout = 0.003, color = '#efebe3', varL = 0.025, groutColor = '#d3cec4',
    pattern = 'stack', surface = 'glossy', nx = 4, ny = 2, ppm = 900, seed = 1,
    rough = null, tilt = 0.012, bevel = 0.0018, sat = 1, accent = null,
  } = opts;
  const [tw, th] = tile;
  const W = Math.round(nx * tw * ppm), H = Math.round(ny * th * ppm);
  const col = new Uint8ClampedArray(W * H * 3), hgt = new Float32Array(W * H), rgh = new Float32Array(W * H);
  const base = hexRGB(color), gc = hexRGB(groutColor), acc = accent ? hexRGB(accent) : null;
  const R = rng(seed);
  const tileRough = rough ?? ({ glossy: 0.14, zellige: 0.1, matte: 0.55, concrete: 0.62, marble: 0.22, terrazzo: 0.35 }[surface] ?? 0.4);
  // per tegel: helderheid, kanteling, toon
  const tiles = new Map();
  const tileInfo = (c, r) => {
    const key = c * 1000 + r;
    let t = tiles.get(key);
    if (!t) {
      const h = (k) => hash2(c, r, seed * 31 + k);
      t = { l: (h(1) - 0.5) * 2 * varL, tx: (h(2) - 0.5) * tilt, ty: (h(3) - 0.5) * tilt, hue: (h(4) - 0.5), ox: h(5), oy: h(6), a: acc && h(7) < 0.08 };
      tiles.set(key, t);
    }
    return t;
  };
  const off = pattern === 'half' ? 0.5 : pattern === 'third' ? 1 / 3 : 0;
  for (let py = 0; py < H; py++) {
    const v = py / ppm;
    const row = Math.floor(v / th);
    const lv = v - row * th;
    const rowOff = ((row * off) % 1) * tw;
    for (let px = 0; px < W; px++) {
      const u = px / ppm;
      let uu = u - rowOff;
      let colI = Math.floor(uu / tw);
      const lu = uu - colI * tw;
      colI = ((colI % nx) + nx) % nx;
      const d = Math.min(lu, tw - lu, lv, th - lv) - grout / 2;
      const i = py * W + px;
      const fu = px / W, fv = py / H;
      if (d < 0) {
        const n = hash2(px, py, seed + 99);
        const f = 0.93 + n * 0.1;
        col[i * 3] = gc[0] * f; col[i * 3 + 1] = gc[1] * f; col[i * 3 + 2] = gc[2] * f;
        hgt[i] = -0.0009 + n * 0.00015;
        rgh[i] = 0.92;
        continue;
      }
      const t = tileInfo(colI, row % ny);
      let L = 1 + t.l, cr = base[0], cg = base[1], cb = base[2];
      if (t.a) { cr = acc[0]; cg = acc[1]; cb = acc[2]; }
      let h = bevel * smooth(0, bevel * 1.4, d);
      let rr = tileRough;
      if (surface === 'concrete') {
        const n1 = pfbm(fu, fv, nx * 3, ny * 3 * th / tw, seed + 3, 5);
        const n2 = hash2(px, py, seed);
        L *= 1 + (n1 - 0.5) * 0.22 + (n2 - 0.5) * 0.05;
        if (n2 > 0.997) L *= 0.75; // poriën
        h += (n1 - 0.5) * 0.00025 + (n2 > 0.997 ? -0.0003 : 0);
        rr = tileRough + (n1 - 0.5) * 0.25;
      } else if (surface === 'marble') {
        // dunne grijze aders, schuin, met een zachte waas; wolkerige ondergrond
        const w = pfbm(fu, fv, nx * 2, ny * 2, seed + 7, 5);
        const w2 = pfbm(fu, fv, nx * 3, ny * 3, seed + 19, 4);
        const a1 = fu * nx * 0.7 + fv * ny * 0.35 + (w - 0.5) * 1.4 + t.ox * 2;
        const a2 = fu * nx * 1.9 - fv * ny * 1.1 + (w2 - 0.5) * 2.0;
        const v1 = 1 - Math.abs(Math.sin(a1 * Math.PI));
        const v2 = 1 - Math.abs(Math.sin(a2 * Math.PI));
        const vv = Math.pow(v1, 60) * 0.38 + Math.pow(v1, 8) * 0.06 + Math.pow(v2, 120) * 0.22 * smooth(0.45, 0.7, w2);
        L *= 1 - vv + (w - 0.5) * 0.05;
        cb = cb * (1 + vv * 0.05);
      } else if (surface === 'terrazzo') {
        const cx = u * 90, cy = v * 90;
        const ix = Math.floor(cx), iy = Math.floor(cy);
        let chip = 0;
        for (let oy = -1; oy <= 1 && !chip; oy++) for (let ox = -1; ox <= 1 && !chip; ox++) {
          const hx = ix + ox, hy = iy + oy;
          const rr2 = hash2(hx, hy, seed + 5);
          if (rr2 > (opts.chips ?? 0.4)) continue;
          const dx = cx - (hx + hash2(hx, hy, seed + 6)), dy = cy - (hy + hash2(hx, hy, seed + 8));
          if (dx * dx + dy * dy < 0.05 + rr2 * 0.22) chip = 1 + Math.floor(hash2(hx, hy, seed + 9) * 3);
        }
        if (chip === 1) { L *= 0.55; } else if (chip === 2) { L *= 0.8; cr *= 1.05; } else if (chip === 3) { L *= 1.06; }
        L *= 1 + (hash2(px, py, seed) - 0.5) * 0.06;
      } else if (surface === 'zellige') {
        const n1 = pfbm(fu, fv, nx * 4, ny * 4 * th / tw, seed + 3, 4);
        L *= 1 + (n1 - 0.5) * 0.12 + (1 - smooth(0, 0.012, d)) * 0.08;
        h += (n1 - 0.5) * 0.0012;
      } else {
        const n1 = pfbm(fu, fv, nx * 6, ny * 6, seed + 3, 3);
        L *= 1 + (n1 - 0.5) * 0.03;
        h += (n1 - 0.5) * 0.00006;
        // glazuur iets lichter aan de rand
        if (surface === 'glossy') L *= 1 + (1 - smooth(0, 0.006, d)) * 0.04;
      }
      // kanteling van de tegel (geeft per tegel een andere reflectie)
      h += (lu - tw / 2) * t.tx + (lv - th / 2) * t.ty;
      const hueShift = t.hue * 0.03 * sat;
      col[i * 3] = clamp(cr * L * (1 + hueShift) / 255) * 255;
      col[i * 3 + 1] = clamp(cg * L / 255) * 255;
      col[i * 3 + 2] = clamp(cb * L * (1 - hueShift) / 255) * 255;
      hgt[i] = h;
      rgh[i] = clamp(rr + (hash2(px, py, seed + 3) - 0.5) * 0.04, 0.04, 1);
    }
  }
  const size = [W / ppm, H / ppm];
  return new THREE.MeshPhysicalMaterial({
    map: tex(rgbCanvas(col, W, H), true, size),
    normalMap: tex(normalCanvas(hgt, W, H, ppm), false, size),
    roughnessMap: tex(grayCanvas(rgh, W, H), false, size),
    roughness: 1, envMapIntensity: 0.7,
    clearcoat: surface === 'glossy' || surface === 'zellige' ? (opts.clearcoat ?? 0.35) : 0,
    clearcoatRoughness: 0.14,
  });
}

// Houtfineer (eiken/noten), nerf langs u (horizontaal).
export function woodMaterial(opts = {}) {
  const { light = '#c9a27a', dark = '#9a7350', seed = 2, ring = 34, size = 1.2, rough = 0.6, plank = 0 } = opts;
  const W = 1536, H = 1536, ppm = W / size;
  const a = hexRGB(light), b = hexRGB(dark);
  const col = new Uint8ClampedArray(W * H * 3), hgt = new Float32Array(W * H), rgh = new Float32Array(W * H);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const fu = x / W, fv = y / H;
    let pv = fv, pid = 0;
    if (plank) { pid = Math.floor(fv * plank); pv = fv * plank - pid; }
    // lichte golving van de nerf, verder rechte lijnen langs u
    const warp = (pfbm(fu, fv, 2, 3, seed + pid, 3) - 0.5) * 0.06;
    const vv = fv + warp;
    const lines = pfbm(fu, vv, 2, ring * 4, seed + 3, 3);          // fijne jaarlijnen
    const bands = pfbm(fu, vv, 1, ring / 3, seed + 5, 3);           // brede vlammen
    const flake = pfbm(fu, vv, 24, 90, seed + 9, 2);                 // eikenspiegels
    const pore = pfbm(fu, fv, 90, 900, seed + 11, 1);
    let t = clamp(0.45 + (lines - 0.5) * 1.1 + (bands - 0.5) * 0.7 + (pore - 0.5) * 0.45 - Math.max(0, flake - 0.7) * 0.8);
    if (plank) t = clamp(t + (hash2(pid, 3, seed) - 0.5) * 0.3);
    const i = y * W + x;
    col[i * 3] = mix(a[0], b[0], t); col[i * 3 + 1] = mix(a[1], b[1], t); col[i * 3 + 2] = mix(a[2], b[2], t);
    hgt[i] = -(pore < 0.4 ? (0.4 - pore) * 0.0003 : 0) - (plank && pv < 0.004 ? 0.0006 : 0);
    rgh[i] = rough + (pore - 0.5) * 0.15;
  }
  const sz = [size, size];
  return new THREE.MeshStandardMaterial({
    map: tex(rgbCanvas(col, W, H), true, sz),
    normalMap: tex(normalCanvas(hgt, W, H, ppm), false, sz),
    roughnessMap: tex(grayCanvas(rgh, W, H), false, sz),
    roughness: 1, envMapIntensity: 0.6,
  });
}

// Microcement / beton (naadloos)
export function microcementMaterial(hex = '#bdb6ab', seed = 4, size = 2) {
  const S = 1024, ppm = S / size;
  const [r, g, b] = hexRGB(hex);
  const col = new Uint8ClampedArray(S * S * 3), hgt = new Float32Array(S * S), rgh = new Float32Array(S * S);
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const n1 = pfbm(x / S, y / S, 4, 4, seed, 6), n2 = pfbm(x / S, y / S, 24, 24, seed + 3, 3);
    const f = 1 + (n1 - 0.5) * 0.28 + (n2 - 0.5) * 0.08;
    const i = y * S + x;
    col[i * 3] = r * f; col[i * 3 + 1] = g * f; col[i * 3 + 2] = b * f;
    hgt[i] = (n2 - 0.5) * 0.0002;
    rgh[i] = 0.55 + (n1 - 0.5) * 0.3;
  }
  const sz = [size, size];
  return new THREE.MeshStandardMaterial({
    map: tex(rgbCanvas(col, S, S), true, sz),
    normalMap: tex(normalCanvas(hgt, S, S, ppm), false, sz),
    roughnessMap: tex(grayCanvas(rgh, S, S), false, sz),
    roughness: 1, envMapIntensity: 0.6,
  });
}

// RVS-rooster van een douchegoot: geborsteld met sleufjes
function drainMaterial() {
  const W = 1024, H = 64;
  const c = canvas(W, H), x = c.getContext('2d');
  x.fillStyle = '#b8b6b2'; x.fillRect(0, 0, W, H);
  for (let i = 0; i < 400; i++) { x.fillStyle = `rgba(255,255,255,${Math.random() * 0.15})`; x.fillRect(0, Math.random() * H, W, 1); }
  x.fillStyle = '#1c1c1c';
  for (let i = 0; i < 64; i++) x.fillRect(i * 16 + 3, 14, 10, 36);
  const t = tex(c, true);
  t.wrapS = THREE.RepeatWrapping;
  return new THREE.MeshStandardMaterial({ map: t, metalness: 0.9, roughness: 0.3, envMapIntensity: 1 });
}

/* ------------------------------------------------------------------ */
/* Renderer, camera, licht                                              */
/* ------------------------------------------------------------------ */

const jitterers = [];
const reflectors = [];
export function onJitter(fn) { jitterers.push(fn); }

export function setup(opts = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
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
  scene.background = new THREE.Color('#222');
  const camera = new THREE.PerspectiveCamera(opts.fov ?? 50, RENDER_W / RENDER_H, 0.03, 60);
  return { renderer, scene, camera };
}

// Camera met horizontale kijkrichting en 'shift lens': verticale lijnen blijven verticaal.
export function archCamera(camera, pos, target, shiftY = 0, fov = null) {
  camera.position.set(...pos);
  camera.lookAt(target[0], pos[1], target[2]);
  if (fov) camera.fov = fov;
  camera.userData.shift = shiftY;
  camera.setViewOffset(RENDER_W, RENDER_H, 0, -shiftY * RENDER_H, RENDER_W, RENDER_H);
  camera.updateProjectionMatrix();
}

// Gewone camera (kijkt schuin), voor close-ups
export function lookCamera(camera, pos, target, fov = null) {
  camera.position.set(...pos);
  camera.lookAt(...target);
  if (fov) camera.fov = fov;
  camera.userData.shift = 0;
  camera.setViewOffset(RENDER_W, RENDER_H, 0, 0, RENDER_W, RENDER_H);
  camera.updateProjectionMatrix();
}

function spot(color, intensity, angle, penumbra, mapSize = 1024) {
  const s = new THREE.SpotLight(color, intensity, 0, angle, penumbra, 2);
  s.castShadow = true;
  s.shadow.mapSize.set(mapSize, mapSize);
  s.shadow.bias = -0.00015;
  s.shadow.normalBias = 0.003;
  s.shadow.camera.near = 0.03;
  s.shadow.camera.far = 12;
  s.shadow.radius = 2;
  return s;
}

/*
 * Raamlicht: per frame een spot op een willekeurige plek in de raamopening,
 * gericht de kamer in. normal = richting de kamer in.
 */
export function windowLight(scene, { center, u, v, w, h, normal, intensity = 14, color = '#f3f6ff', aim = [0, -0.1] }) {
  const C = new THREE.Vector3(...center), U = new THREE.Vector3(...u), V = new THREE.Vector3(...v), N = new THREE.Vector3(...normal);
  const s = spot(color, intensity, 1.47, 1, 2048);
  s.decay = 2.001; // alleen diffuus; de reflectie van het raam komt uit de omgevingskaart
  scene.add(s, s.target);
  onJitter((R) => {
    const p = C.clone().addScaledVector(U, (R() - 0.5) * w).addScaledVector(V, (R() - 0.5) * h).addScaledVector(N, 0.02);
    s.position.copy(p);
    const dir = N.clone().addScaledVector(U, (R() - 0.5) * 0.3 + aim[0]).addScaledVector(V, aim[1] + (R() - 0.5) * 0.3);
    s.target.position.copy(p).add(dir);
  });
  return s;
}

/*
 * Kaatslicht: per frame een zwakke spot op een willekeurige plek op een van de
 * opgegeven vlakken, gericht naar het midden van de kamer. Geeft indirect licht
 * met zachte contactschaduw onder meubels.
 */
export function bounceLight(scene, { surfaces, target, intensity = 3, color = '#fff4e8', count = 2, avoid = [] }) {
  const T = new THREE.Vector3(...target);
  const lights = [];
  for (let k = 0; k < count; k++) {
    const s = spot(color, intensity / count, 1.45, 1, 1024);
    s.decay = 2.001; // markering voor de shaderpatch: alleen diffuus
    scene.add(s, s.target);
    lights.push(s);
  }
  const total = surfaces.reduce((a, s) => a + (s.weight ?? 1), 0);
  onJitter((R) => {
    for (const s of lights) {
      let r = R() * total, sf = surfaces[0];
      for (const x of surfaces) { r -= x.weight ?? 1; if (r <= 0) { sf = x; break; } }
      const n = new THREE.Vector3(...sf.normal);
      let p;
      for (let tries = 0; tries < 20; tries++) {
        p = new THREE.Vector3(...sf.origin).addScaledVector(new THREE.Vector3(...sf.u), R()).addScaledVector(new THREE.Vector3(...sf.v), R());
        p.addScaledVector(n, 0.3);
        if (!avoid.some((b) => p.x > b[0] && p.y > b[1] && p.z > b[2] && p.x < b[3] && p.y < b[4] && p.z < b[5])) break;
      }
      s.position.copy(p);
      s.color.set(sf.color ?? color);
      // richting: half naar de normaal, half naar het midden
      const dir = T.clone().sub(p).normalize().add(n).normalize();
      s.target.position.copy(p).add(dir);
    }
  });
  return lights;
}

// Inbouwspot in het plafond (armatuur + licht)
export function downlight(scene, x, z, H, opts = {}) {
  const { intensity = 5, color = '#ffe2bd', angle = 0.75, cast = true } = opts;
  const g = new THREE.Group();
  const trim = cyl(0.045, 0.006, MAT.whiteMatte('#f4f4f2'), x, H - 0.003, z, { cast: false });
  const lens = cyl(0.028, 0.004, new THREE.MeshStandardMaterial({ color: '#fff', emissive: color, emissiveIntensity: 3.5 }), x, H - 0.007, z, { cast: false });
  const ring = cyl(0.036, 0.005, MAT.whiteMatte('#dcdcd8'), x, H - 0.0055, z, { cast: false });
  g.add(trim, ring, lens);
  scene.add(g);
  if (intensity > 0) {
    const s = spot(color, intensity, angle, 0.7, 1024);
    s.castShadow = cast;
    s.position.set(x, H - 0.02, z);
    s.target.position.set(x, 0, z);
    scene.add(s, s.target);
    onJitter((R) => { s.position.set(x + (R() - 0.5) * 0.02, H - 0.02, z + (R() - 0.5) * 0.02); });
  }
  return g;
}

// Omgevingskaart uit de scène zelf (voor reflecties), vanaf een punt in de kamer.
export function captureEnvironment(renderer, scene, pos, ambient = 0.9) {
  const R = rng(7);
  for (const f of jitterers) f(R);
  const hemi = new THREE.HemisphereLight('#ffffff', '#ddd6cc', ambient);
  scene.add(hemi);
  const cubeRT = new THREE.WebGLCubeRenderTarget(512, { type: THREE.HalfFloatType });
  const cam = new THREE.CubeCamera(0.03, 30, cubeRT);
  cam.position.set(...pos);
  scene.add(cam);
  cam.update(renderer, scene);
  scene.remove(hemi);
  scene.remove(cam);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromCubemap(cubeRT.texture).texture;
  // MeshBasicMaterial pakt scene.environment niet zelf op
  scene.traverse((o) => { if (o.material?.userData?.needsEnv) { o.material.envMap = cubeRT.texture; o.material.needsUpdate = true; } });
}

/*
 * Accumulatie: N frames met verschoven licht en subpixel-camera, gemiddeld in
 * een float-buffer, daarna ACES + sRGB naar het canvas.
 */
export async function renderAccum(renderer, scene, camera, frames = 48, seed = 1) {
  const R = rng(seed);
  const opt = { type: THREE.HalfFloatType, depthBuffer: true };
  const rt = new THREE.WebGLRenderTarget(RENDER_W, RENDER_H, opt);
  // HalfFloat: blending op Float32 vraagt EXT_float_blend, dat niet overal bestaat
  const acc = new THREE.WebGLRenderTarget(RENDER_W, RENDER_H, { type: THREE.HalfFloatType, depthBuffer: false });
  const copyMat = new THREE.ShaderMaterial({
    uniforms: { tDiffuse: { value: rt.texture }, w: { value: 1 / frames } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }',
    fragmentShader: 'uniform sampler2D tDiffuse; uniform float w; varying vec2 vUv; void main(){ gl_FragColor = vec4(texture2D(tDiffuse, vUv).rgb * w, 1.0); }',
    blending: THREE.AdditiveBlending, depthTest: false, depthWrite: false, transparent: true,
  });
  const quad = new FullScreenQuad(copyMat);
  renderer.setRenderTarget(acc);
  renderer.setClearColor(0x000000, 1);
  renderer.clear();
  const shift = camera.userData.shift ?? 0;
  for (let i = 0; i < frames; i++) {
    for (const f of jitterers) f(R);
    const jx = (R() - 0.5) * 1.2, jy = (R() - 0.5) * 1.2;
    camera.setViewOffset(RENDER_W, RENDER_H, jx, -shift * RENDER_H + jy, RENDER_W, RENDER_H);
    camera.updateProjectionMatrix();
    for (const f of reflectors) f(renderer, scene, camera);
    renderer.setRenderTarget(rt);
    renderer.render(scene, camera);
    renderer.setRenderTarget(acc);
    renderer.autoClear = false; // anders wist elke quad-render de som
    quad.render(renderer);
    renderer.autoClear = true;
    if (i % 4 === 3) {
      document.title = `render ${i + 1}/${frames}`;
      await new Promise((r) => setTimeout(r, 0));
    }
  }
  camera.setViewOffset(RENDER_W, RENDER_H, 0, -shift * RENDER_H, RENDER_W, RENDER_H);
  camera.updateProjectionMatrix();
  const out = new OutputPass();
  out.renderToScreen = true;
  out.render(renderer, null, acc);
  renderer.setRenderTarget(null);
}

/* ------------------------------------------------------------------ */
/* Kamer                                                                */
/* ------------------------------------------------------------------ */

/*
 * Kamer met binnenmaat x 0..W, z 0..D, y 0..H. Achterwand op z=0.
 * walls: { back, left, right, front } materialen; floor, ceil.
 * windows: [{ wall: 'left'|'right'|'back', a0, a1, y0, y1, frame }] (a = z of x)
 * Wanden van 0,2 m dik, buiten het binnenvolume.
 */
export function room(scene, opts) {
  const { W, D, H, walls, floor, ceil, windows = [] } = opts;
  const T = 0.2;
  const g = new THREE.Group();
  g.add(box(W + 2 * T, T, D + 2 * T, floor, W / 2, -T / 2, D / 2));
  g.add(box(W + 2 * T, T, D + 2 * T, ceil, W / 2, H + T / 2, D / 2));
  const wallDefs = {
    back: { len: W, axis: 'x', make: (a0, a1, y0, y1) => box(a1 - a0, y1 - y0, T, walls.back, (a0 + a1) / 2, (y0 + y1) / 2, -T / 2) },
    front: { len: W, axis: 'x', make: (a0, a1, y0, y1) => box(a1 - a0, y1 - y0, T, walls.front ?? walls.back, (a0 + a1) / 2, (y0 + y1) / 2, D + T / 2) },
    left: { len: D, axis: 'z', make: (a0, a1, y0, y1) => box(T, y1 - y0, a1 - a0, walls.left, -T / 2, (y0 + y1) / 2, (a0 + a1) / 2) },
    right: { len: D, axis: 'z', make: (a0, a1, y0, y1) => box(T, y1 - y0, a1 - a0, walls.right, W + T / 2, (y0 + y1) / 2, (a0 + a1) / 2) },
  };
  const info = { W, D, H, windows: [] };
  for (const [name, def] of Object.entries(wallDefs)) {
    if (opts.skip?.includes(name)) continue;
    const win = windows.find((w) => w.wall === name);
    const lo = name === 'left' || name === 'right' ? -T : -T, hi = def.len + T;
    if (!win) { g.add(def.make(lo, hi, 0, H)); continue; }
    const { a0, a1, y0, y1 } = win;
    g.add(def.make(lo, a0, 0, H), def.make(a1, hi, 0, H), def.make(a0, a1, 0, y0), def.make(a0, a1, y1, H));
    g.add(windowUnit(name, win, W, D, T));
    info.windows.push(windowInfo(name, win, W, D));
  }
  scene.add(g);
  return info;
}

function windowInfo(name, win, W, D) {
  const { a0, a1, y0, y1 } = win;
  const ca = (a0 + a1) / 2, cy = (y0 + y1) / 2;
  if (name === 'left') return { center: [0, cy, ca], u: [0, 0, 1], v: [0, 1, 0], w: a1 - a0, h: y1 - y0, normal: [1, 0, 0] };
  if (name === 'right') return { center: [W, cy, ca], u: [0, 0, 1], v: [0, 1, 0], w: a1 - a0, h: y1 - y0, normal: [-1, 0, 0] };
  return { center: [ca, cy, 0], u: [1, 0, 0], v: [0, 1, 0], w: a1 - a0, h: y1 - y0, normal: [0, 0, 1] };
}

// Kozijn (wit of zwart) met matglas, halverwege de wanddikte
function windowUnit(name, win, W, D, T) {
  const { a0, a1, y0, y1, frame = '#f3f3f1', glow = 1.6 } = win;
  const fm = new THREE.MeshStandardMaterial({ color: frame, roughness: 0.4, envMapIntensity: 0.6 });
  const g = new THREE.Group();
  const w = a1 - a0, h = y1 - y0, f = 0.055, dep = 0.07;
  // in lokaal xy-vlak, daarna draaien
  const local = new THREE.Group();
  local.add(box(w, f, dep, fm, 0, -h / 2 + f / 2, 0, { worldUV: false }));
  local.add(box(w, f, dep, fm, 0, h / 2 - f / 2, 0, { worldUV: false }));
  local.add(box(f, h, dep, fm, -w / 2 + f / 2, 0, 0, { worldUV: false }));
  local.add(box(f, h, dep, fm, w / 2 - f / 2, 0, 0, { worldUV: false }));
  if (win.mullion) local.add(box(f * 0.9, h, dep, fm, 0, 0, 0, { worldUV: false }));
  // vensterbank
  local.add(box(w + 0.04, 0.02, T * 0.55, MAT.whiteMatte('#ecebe7'), 0, -h / 2 - 0.01, T * 0.3, { worldUV: false }));
  const glass = new THREE.Mesh(new THREE.PlaneGeometry(w - 2 * f, h - 2 * f), MAT.frosted(glow));
  glass.position.z = -0.005;
  local.add(glass);
  const ca = (a0 + a1) / 2, cy = (y0 + y1) / 2;
  if (name === 'left') { local.rotation.y = Math.PI / 2; local.position.set(-T * 0.55, cy, ca); }
  else if (name === 'right') { local.rotation.y = -Math.PI / 2; local.position.set(W + T * 0.55, cy, ca); }
  else { local.position.set(ca, cy, -T * 0.55); }
  g.add(local);
  return g;
}

// Plint/tegelrand: wandtegels tot hoogte h op een geschilderde wand (losse 'huid' van 6 mm)
export function wainscot(scene, wall, a0, a1, y0, y1, mat, room) {
  const t = 0.006;
  const { W, D } = room;
  let m;
  if (wall === 'back') m = box(a1 - a0, y1 - y0, t, mat, (a0 + a1) / 2, (y0 + y1) / 2, t / 2);
  else if (wall === 'left') m = box(t, y1 - y0, a1 - a0, mat, t / 2, (y0 + y1) / 2, (a0 + a1) / 2);
  else if (wall === 'right') m = box(t, y1 - y0, a1 - a0, mat, W - t / 2, (y0 + y1) / 2, (a0 + a1) / 2);
  else m = box(a1 - a0, y1 - y0, t, mat, (a0 + a1) / 2, (y0 + y1) / 2, D - t / 2);
  m.castShadow = false;
  scene.add(m);
  return m;
}

/* ------------------------------------------------------------------ */
/* Sanitair en inrichting                                               */
/* Lokaal: achterkant tegen de wand op z=0, voorkant naar +z.            */
/* place(obj, wall, a, room) zet het object tegen een wand.              */
/* ------------------------------------------------------------------ */

export function place(obj, wall, a, room, y = 0) {
  const { W, D } = room;
  if (wall === 'back') { obj.position.set(a, y, 0); }
  else if (wall === 'left') { obj.rotation.y = Math.PI / 2; obj.position.set(0, y, a); }
  else if (wall === 'right') { obj.rotation.y = -Math.PI / 2; obj.position.set(W, y, a); }
  else { obj.rotation.y = Math.PI; obj.position.set(a, y, D); }
  return obj;
}

// Hangtoilet met deksel dicht; seatH = hoogte bovenkant zitting
export function hangingToilet(opts = {}) {
  const { seatH = 0.42, mat = MAT.ceramic(), seatMat = MAT.ceramic('#f8f8f6'), w = 0.36, l = 0.54 } = opts;
  const g = new THREE.Group();
  const bodyH = 0.3;
  const shape = new THREE.Shape(eggPoints(w, l, 96, 5));
  let body = extrudeY(shape, bodyH, 0.018, 4);
  // taps naar onderen en naar achteren iets breder
  const p = body.attributes.position;
  for (let i = 0; i < p.count; i++) {
    const y = p.getY(i), t = y / bodyH;
    const s = 0.8 + 0.2 * smooth(0, 1, t);
    const z = -p.getZ(i); // diepte vanaf de wand
    p.setX(i, p.getX(i) * s);
    p.setZ(i, -(z * (0.86 + 0.14 * t)));
  }
  body = smoothNormals(body);
  body.rotateY(Math.PI); // voorkant naar +z
  body.translate(0, seatH - 0.035 - bodyH, 0);
  g.add(mesh(body, mat));
  // zitting + deksel
  const seat = extrudeY(new THREE.Shape(eggPoints(w * 0.98, l * 0.97, 96, 5)), 0.022, 0.009, 4);
  seat.rotateY(Math.PI);
  seat.translate(0, seatH - 0.036, 0.012);
  g.add(mesh(seat, seatMat));
  const lid = extrudeY(new THREE.Shape(eggPoints(w * 0.95, l * 0.93, 96, 5)), 0.016, 0.007, 4);
  lid.rotateY(Math.PI);
  lid.translate(0, seatH - 0.014, 0.02);
  g.add(mesh(lid, seatMat));
  // scharnieren
  const ch = MAT.chrome();
  g.add(cyl(0.012, 0.03, ch, -0.1, seatH - 0.012, 0.035, { axis: 'x' }), cyl(0.012, 0.03, ch, 0.1, seatH - 0.012, 0.035, { axis: 'x' }));
  return g;
}

// Bedieningsplaat; style: 'black' | 'white' | 'chrome'
export function flushPlate(opts = {}) {
  const { style = 'white', w = 0.24, h = 0.155 } = opts;
  const g = new THREE.Group();
  const pm = style === 'black' ? MAT.black() : style === 'chrome' ? MAT.brushed() : MAT.plastic('#f5f5f3');
  g.add(rbox(w, h, 0.012, 0.004, pm, 0, 0, 0.006));
  const bm = style === 'black' ? new THREE.MeshStandardMaterial({ color: '#0e0e0e', metalness: 0.2, roughness: 0.25 }) : pm;
  g.add(rbox(w * 0.6, h * 0.36, 0.006, 0.003, bm, -w * 0.08, h * 0.17, 0.014));
  g.add(rbox(w * 0.3, h * 0.36, 0.006, 0.003, bm, w * 0.33, h * 0.17, 0.014));
  g.add(rbox(w * 0.92, 0.003, 0.004, 0.001, MAT.rubber('#555'), 0, -h * 0.05, 0.013));
  return g;
}

// Wastafelmeubel, zwevend. basin: 'vessel' (rond waskom), 'rect' (opbouw rechthoekig), 'integrated'
export function vanity(opts = {}) {
  const {
    w = 1.0, d = 0.46, h = 0.48, y0 = 0.38, front, carcass = null, top = null, topT = 0.03,
    basin = 'vessel', drawers = 2, handle = 'groove', basins = 1, basinMat = MAT.ceramic(), handleMat = MAT.black(),
  } = opts;
  const g = new THREE.Group();
  const car = carcass ?? front;
  // bij een verdiepte kom blijft de korpus onder de kom, anders schijnt hij erdoorheen
  const ch = basin === 'integrated' ? h - 0.11 : h;
  g.add(rbox(w, ch, d - 0.02, 0.004, car, 0, y0 + ch / 2, (d - 0.02) / 2, { worldUV: true }));
  const gap = 0.004;
  const fh = (h - gap * (drawers - 1)) / drawers;
  for (let i = 0; i < drawers; i++) {
    const yc = y0 + fh / 2 + i * (fh + gap);
    const f = rbox(w - 0.003, fh, 0.019, 0.003, front, 0, yc, d - 0.02 + 0.0095, { worldUV: true });
    g.add(f);
    if (handle === 'bar') g.add(rbox(Math.min(0.32, w * 0.4), 0.012, 0.018, 0.005, handleMat, 0, yc + fh / 2 - 0.05, d + 0.012));
    else if (handle === 'groove') g.add(box(w - 0.003, 0.022, 0.012, new THREE.MeshStandardMaterial({ color: '#2b2622', roughness: 0.8 }), 0, yc + fh / 2 - 0.008, d - 0.004, { worldUV: false, cast: false }));
  }
  const topY = y0 + h;
  const tm = top ?? basinMat;
  if (basin === 'integrated') {
    // blad met verdiepte kom (rechthoekig met ronde hoeken)
    const bw = Math.min(0.5, w / basins - 0.16), bd = d - 0.17;
    const s = roundedRectShape(w, d, 0.006, 0, -d / 2);
    const holes = [];
    for (let k = 0; k < basins; k++) {
      const cx = -w / 2 + (w / basins) * (k + 0.5);
      const hole = roundedRectPath(bw, bd, 0.06, cx, -d / 2 - 0.02);
      s.holes.push(hole); holes.push(cx);
    }
    const slab = extrudeY(s, 0.045, 0.004, 3, 32);
    slab.translate(0, topY, 0);
    g.add(mesh(slab, tm));
    for (const cx of holes) {
      // kom: binnenkant van een afgeronde bak
      const bowl = new RoundedBoxGeometry(bw, 0.13, bd, 4, 0.05);
      const m = new THREE.Mesh(bowl, tm.clone());
      m.material.side = THREE.BackSide;
      m.position.set(cx, topY + 0.045 - 0.065, d / 2 + 0.02);
      m.receiveShadow = true;
      g.add(m);
      g.add(cyl(0.018, 0.003, MAT.chrome(), cx, topY - 0.019, d / 2 + 0.03));
    }
  } else {
    g.add(rbox(w + 0.002, topT, d, 0.003, tm, 0, topY + topT / 2, d / 2, { worldUV: true }));
    for (let k = 0; k < basins; k++) {
      const cx = basins === 1 ? (opts.basinX ?? 0) : -w / 2 + (w / basins) * (k + 0.5);
      if (basin === 'vessel') g.add(vesselBasin(basinMat, cx, topY + topT, d / 2 + 0.02));
      else g.add(rectBasin(basinMat, cx, topY + topT, d / 2 + 0.03, opts.basinW ?? 0.5, d - 0.1));
    }
  }
  g.userData = { topY: basin === 'integrated' ? topY + 0.045 : topY + topT, d, w };
  return g;
}

export function vesselBasin(mat, x, y, z, r = 0.2, h = 0.13) {
  const pts = [];
  const th = 0.009;
  // buitenkant van onder naar boven, dan binnenkant terug
  for (let i = 0; i <= 16; i++) { const t = i / 16; pts.push(new THREE.Vector2(r * (0.55 + 0.45 * Math.sin(t * Math.PI / 2)), t * h)); }
  pts.push(new THREE.Vector2(r - th * 0.5, h + th * 0.4));
  for (let i = 16; i >= 0; i--) { const t = i / 16; pts.push(new THREE.Vector2((r - th) * (0.5 + 0.5 * Math.sin(t * Math.PI / 2)) - th * (1 - t), th + t * (h - th))); }
  pts.unshift(new THREE.Vector2(0.001, 0));
  pts.push(new THREE.Vector2(0.001, th));
  const geo = new THREE.LatheGeometry(pts, 96);
  geo.translate(x, y, z);
  const g = new THREE.Group();
  g.add(mesh(geo, mat));
  g.add(cyl(0.02, 0.003, MAT.chrome(), x, y + th + 0.0015, z));
  return g;
}

export function rectBasin(mat, x, y, z, w, d, h = 0.12) {
  const s = roundedRectShape(w, d, 0.07);
  s.holes.push(roundedRectPath(w - 0.022, d - 0.022, 0.06));
  const wall = extrudeY(s, h, 0.004, 3, 40);
  wall.translate(x, y, z);
  const g = new THREE.Group();
  g.add(mesh(wall, mat));
  const bottom = extrudeY(roundedRectShape(w - 0.01, d - 0.01, 0.065), 0.012, 0.002, 2, 40);
  bottom.translate(x, y, z);
  g.add(mesh(bottom, mat));
  g.add(cyl(0.02, 0.003, MAT.chrome(), x, y + 0.0135, z));
  return g;
}

// Kraan op het blad (hoog voor waskom, laag voor inbouw). style: mat-zwart, chroom, goud
export function deckFaucet(mat, x, y, z, opts = {}) {
  const { tall = false, reach = 0.15 } = opts;
  const g = new THREE.Group();
  const h = tall ? 0.29 : 0.17;
  g.add(cyl(0.024, 0.01, mat, x, y + 0.005, z));
  g.add(cyl(0.017, h, mat, x, y + h / 2, z, { rTop: 0.016 }));
  // uitloop: gebogen buis
  g.add(tube([[x, y + h - 0.02, z], [x, y + h + 0.03, z + 0.03], [x, y + h + 0.02, z + reach * 0.75], [x, y + h - 0.035, z + reach]], 0.011, mat));
  g.add(cyl(0.012, 0.012, mat, x, y + h - 0.04, z + reach));
  // hendel
  g.add(cylBetween(new THREE.Vector3(x + 0.016, y + h * 0.72, z), new THREE.Vector3(x + 0.07, y + h * 0.76, z - 0.02), 0.0055, mat));
  g.add(cyl(0.019, 0.03, mat, x, y + h * 0.72, z, { axis: 'x' }));
  return g;
}

// Inbouwkraan in de wand boven het blad
export function wallFaucet(mat, x, y, opts = {}) {
  const { reach = 0.19, z = 0 } = opts;
  const g = new THREE.Group();
  g.add(cyl(0.03, 0.008, mat, x, y, z + 0.004, { axis: 'z' }));
  g.add(cyl(0.0115, reach, mat, x, y, z + reach / 2, { axis: 'z' }));
  g.add(cyl(0.0125, 0.012, mat, x, y - 0.002, z + reach - 0.006));
  // mengkraan: rozet met korte hendel
  g.add(cyl(0.03, 0.008, mat, x + 0.13, y, z + 0.004, { axis: 'z' }));
  g.add(cyl(0.017, 0.035, mat, x + 0.13, y, z + 0.025, { axis: 'z' }));
  g.add(cylBetween(new THREE.Vector3(x + 0.13, y, z + 0.04), new THREE.Vector3(x + 0.13, y - 0.065, z + 0.05), 0.0045, mat));
  return g;
}

// Spiegel (echte reflectie). shape: 'rect' | 'round' | 'arch'. Hangt op z=0.
export function mirror(opts = {}) {
  const { w = 0.8, h = 0.7, shape = 'rect', frameMat = null, led = false, r = 0.03 } = opts;
  const g = new THREE.Group();
  let geo;
  if (shape === 'round') geo = new THREE.CircleGeometry(w / 2, 96);
  else if (shape === 'arch') {
    const s = new THREE.Shape();
    s.moveTo(-w / 2, -h / 2); s.lineTo(w / 2, -h / 2); s.lineTo(w / 2, h / 2 - w / 2);
    s.absarc(0, h / 2 - w / 2, w / 2, 0, Math.PI, false); s.lineTo(-w / 2, -h / 2);
    geo = new THREE.ShapeGeometry(s, 64);
  } else geo = new THREE.ShapeGeometry(roundedRectShape(w, h, r), 16);
  const ref = new Reflector(geo, { textureWidth: 2048, textureHeight: 2048, color: 0x8a8d8c, clipBias: 0.003 });
  // r160 deelt de transmissiebuffer tussen camera's: de spiegel daarom vóór elke frame zelf renderen
  const orig = ref.onBeforeRender;
  ref.onBeforeRender = () => {};
  reflectors.push((r, s, c) => orig.call(ref, r, s, c));
  ref.position.z = 0.0205;
  g.add(ref);
  // achterplaat/rand
  const bm = frameMat ?? new THREE.MeshStandardMaterial({ color: '#c7cbca', metalness: 0.6, roughness: 0.25 });
  let back;
  if (shape === 'round') back = new THREE.Mesh(new THREE.CylinderGeometry(w / 2 + (frameMat ? 0.012 : 0.002), w / 2 + (frameMat ? 0.012 : 0.002), 0.02, 96).rotateX(Math.PI / 2), bm);
  else if (shape === 'arch') {
    const s = new THREE.Shape(); const fw = w + (frameMat ? 0.024 : 0.004), fh = h + (frameMat ? 0.024 : 0.004);
    s.moveTo(-fw / 2, -fh / 2); s.lineTo(fw / 2, -fh / 2); s.lineTo(fw / 2, fh / 2 - fw / 2);
    s.absarc(0, fh / 2 - fw / 2, fw / 2, 0, Math.PI, false); s.lineTo(-fw / 2, -fh / 2);
    back = new THREE.Mesh(new THREE.ExtrudeGeometry(s, { depth: 0.02, bevelEnabled: false, curveSegments: 64 }), bm);
  } else back = new THREE.Mesh(new THREE.ExtrudeGeometry(roundedRectShape(w + (frameMat ? 0.024 : 0.004), h + (frameMat ? 0.024 : 0.004), r + 0.004), { depth: 0.0195, bevelEnabled: false }), bm);
  if (shape === 'round') back.position.z = 0.01;
  back.castShadow = true; back.receiveShadow = true;
  g.add(back);
  if (led) {
    // indirecte led achter de spiegel: zachte gloed op de wand
    const glowMat = new THREE.MeshBasicMaterial({ color: '#ffe9c9', transparent: true, opacity: 0.55, depthWrite: false, toneMapped: true });
    const c = canvas(256, 256), x = c.getContext('2d');
    const gr = x.createRadialGradient(128, 128, 60, 128, 128, 128);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.55, 'rgba(255,255,255,0.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    x.fillStyle = gr; x.fillRect(0, 0, 256, 256);
    glowMat.map = new THREE.CanvasTexture(c);
    const gm = new THREE.Mesh(new THREE.PlaneGeometry(w * 1.35, (shape === 'round' ? w : h) * 1.35), glowMat);
    gm.position.z = 0.001;
    g.add(gm);
  }
  return g;
}

// Glas: lichte groenige tint plus een additieve reflectielaag
export function glassMesh(geo, x = 0, y = 0, z = 0, tint) {
  const g = new THREE.Group();
  const a = new THREE.Mesh(geo, MAT.glassTint(tint));
  const b = new THREE.Mesh(geo, MAT.glassReflect());
  a.renderOrder = 2; b.renderOrder = 3;
  g.add(a, b);
  g.position.set(x, y, z);
  return g;
}

// Glazen douchewand met profiel aan de wand en stabilisatiestang.
// Lokaal: wand staat in het yz-vlak? Nee: paneel in xy-vlak, breedte langs +x vanaf x=0 (wandkant).
export function glassPanel(opts = {}) {
  const { w = 1.0, h = 2.0, frame = 'black', grid = 0, frameAll = false } = opts;
  const g = new THREE.Group();
  const t = 0.008;
  g.add(glassMesh(new THREE.BoxGeometry(w - 0.01, h - 0.01, t), w / 2, h / 2 + 0.005, 0));
  // groene glasrand (zichtbaar aan de voorkant)
  const em = MAT.glassEdge();
  g.add(box(0.003, h - 0.01, t, em, w - 0.0065, h / 2 + 0.005, 0, { worldUV: false, cast: false }));
  g.add(box(w - 0.01, 0.003, t, em, w / 2, h + 0.0015, 0, { worldUV: false, cast: false }));
  const fm = frame === 'black' ? MAT.black() : frame === 'gold' ? MAT.gold() : MAT.chrome();
  // wandprofiel
  g.add(box(0.022, h, 0.03, fm, 0.011, h / 2, 0, { worldUV: false }));
  if (frameAll || grid) {
    g.add(box(w, 0.022, 0.024, fm, w / 2, h - 0.011, 0, { worldUV: false }));
    g.add(box(w, 0.022, 0.024, fm, w / 2, 0.011, 0, { worldUV: false }));
    g.add(box(0.022, h, 0.024, fm, w - 0.011, h / 2, 0, { worldUV: false }));
  } else {
    // vloerprofiel (dun)
    g.add(box(w, 0.012, 0.022, fm, w / 2, 0.006, 0, { worldUV: false }));
  }
  for (let k = 1; k < grid; k++) g.add(box(w, 0.012, 0.016, fm, w / 2, (h / grid) * k, 0, { worldUV: false }));
  return g;
}

// Douchegoot langs een wand: rooster in de vloer (len langs x, lokaal)
export function linearDrain(len = 0.9) {
  const g = new THREE.Group();
  const m = drainMaterial();
  m.map.repeat.set(len / 1.0, 1);
  const top = new THREE.Mesh(new THREE.BoxGeometry(len, 0.002, 0.07), m);
  top.position.y = 0.0005;
  top.receiveShadow = true;
  g.add(top);
  g.add(box(len + 0.01, 0.0012, 0.08, MAT.brushed(), 0, 0.0002, 0, { worldUV: false, cast: false }));
  return g;
}

// Regendouche aan de wand (arm vanaf z=0) met thermostaat en handdouche.
export function showerSet(mat, opts = {}) {
  const { headH = 2.12, arm = 0.38, head = 0.3, round = false, mixerH = 1.05, hand = true } = opts;
  const g = new THREE.Group();
  // stang van thermostaat naar arm
  g.add(cyl(0.011, headH - mixerH, mat, 0, (headH + mixerH) / 2, 0.055));
  g.add(cyl(0.022, 0.01, mat, 0, headH, 0.005, { axis: 'z' }));
  g.add(cyl(0.011, 0.06, mat, 0, headH, 0.03, { axis: 'z' }));
  g.add(cylBetween(new THREE.Vector3(0, headH, 0.055), new THREE.Vector3(0, headH, arm), 0.011, mat));
  // hoofddouche
  if (round) g.add(cyl(head / 2, 0.008, mat, 0, headH - 0.025, arm));
  else g.add(rbox(head, 0.008, head, 0.004, mat, 0, headH - 0.025, arm));
  g.add(cyl(0.013, 0.025, mat, 0, headH - 0.012, arm));
  // sproeivlak iets donkerder
  const nozzle = new THREE.MeshStandardMaterial({ color: '#2a2a2a', roughness: 0.6 });
  if (round) g.add(cyl(head / 2 - 0.012, 0.001, nozzle, 0, headH - 0.0295, arm, { cast: false }));
  else g.add(box(head - 0.025, 0.001, head - 0.025, nozzle, 0, headH - 0.0295, arm, { worldUV: false, cast: false }));
  // thermostaatkraan
  g.add(cyl(0.028, 0.34, mat, 0, mixerH, 0.055, { axis: 'x' }));
  g.add(cyl(0.032, 0.05, mat, -0.17, mixerH, 0.055, { axis: 'x' }));
  g.add(cyl(0.032, 0.05, mat, 0.17, mixerH, 0.055, { axis: 'x' }));
  for (const s of [-1, 1]) g.add(cylBetween(new THREE.Vector3(s * 0.11, mixerH, 0), new THREE.Vector3(s * 0.11, mixerH, 0.05), 0.01, mat));
  if (hand) {
    // handdouche in houder rechts op de stang
    g.add(cyl(0.016, 0.025, mat, 0.035, mixerH + 0.42, 0.06, { axis: 'x' }));
    g.add(cylBetween(new THREE.Vector3(0.05, mixerH + 0.36, 0.07), new THREE.Vector3(0.05, mixerH + 0.55, 0.075), 0.012, mat));
    g.add(cyl(0.032, 0.03, mat, 0.05, mixerH + 0.57, 0.077, { rTop: 0.036 }));
    // slang naar de kraan
    g.add(tube([[0.05, mixerH + 0.36, 0.07], [0.07, mixerH + 0.15, 0.09], [0.1, mixerH - 0.15, 0.1], [0.14, mixerH - 0.12, 0.07], [0.13, mixerH - 0.03, 0.055]], 0.0065, mat, 80));
  }
  return g;
}

// Handdoekradiator (ladder). Lokaal tegen z=0, onderkant op y0.
export function towelRadiator(mat, opts = {}) {
  const { w = 0.5, h = 1.2, y0 = 0.2, bars = 14 } = opts;
  const g = new THREE.Group();
  const z = 0.06;
  for (const s of [-1, 1]) {
    g.add(cyl(0.015, h, mat, s * w / 2, y0 + h / 2, z));
    for (const yy of [y0 + 0.15, y0 + h - 0.1]) g.add(cyl(0.008, z, mat, s * w / 2, yy, z / 2, { axis: 'z' }));
  }
  for (let i = 0; i < bars; i++) {
    const yy = y0 + 0.06 + (i / (bars - 1)) * (h - 0.12) * (i % 5 === 4 ? 1 : 1);
    if (i % 5 === 4) continue; // open plekken voor handdoeken
    g.add(cyl(0.01, w, mat, 0, yy, z, { axis: 'x' }));
  }
  return g;
}

// Handdoek over een radiatorstang
export function towel(color, x, y, z, w = 0.4, drop = 0.42, axis = 'x') {
  // badstof: lichte korrel in de kleur
  const c = canvas(256, 256), cx = c.getContext('2d');
  cx.fillStyle = color; cx.fillRect(0, 0, 256, 256);
  for (let i = 0; i < 9000; i++) { cx.fillStyle = `rgba(${Math.random() < 0.5 ? '0,0,0' : '255,255,255'},${Math.random() * 0.035})`; cx.fillRect(Math.random() * 256, Math.random() * 256, 1.5, 1.5); }
  cx.fillStyle = 'rgba(0,0,0,0.06)'; cx.fillRect(0, 228, 256, 10);
  const t = tex(c, true);
  const m = new THREE.MeshStandardMaterial({ map: t, roughness: 1, envMapIntensity: 0.4 });
  const g = new THREE.Group();
  const mk = (d, seed, zs) => {
    const geo = new THREE.BoxGeometry(w, d, 0.014, 40, 30, 1);
    const p = geo.attributes.position;
    for (let i = 0; i < p.count; i++) {
      const xx = p.getX(i), yy = p.getY(i), tt = 0.5 - yy / d; // 0 boven, 1 onder
      const fold = Math.sin(xx / w * Math.PI * 5 + seed) * 0.009 * (0.3 + tt) + Math.sin(xx / w * Math.PI * 2.3 + seed * 2) * 0.006 * tt;
      p.setZ(i, p.getZ(i) + fold * zs);
      p.setX(i, xx * (1 - 0.04 * tt));
    }
    geo.computeVertexNormals();
    const o = new THREE.Mesh(geo, m); o.castShadow = true; o.receiveShadow = true;
    return o;
  };
  const front = mk(drop, 1.3, 1); front.position.set(0, -drop / 2 + 0.005, 0.02);
  const back = mk(drop * 0.75, 2.1, -1); back.position.set(0, -drop * 0.375 + 0.005, -0.02);
  const top = new THREE.Mesh(new THREE.CylinderGeometry(0.024, 0.024, w * 1.0, 24, 1), m); top.rotation.z = Math.PI / 2; top.position.y = 0.004;
  top.castShadow = true; top.receiveShadow = true;
  g.add(front, back, top);
  g.position.set(x, y, z);
  if (axis === 'z') g.rotation.y = Math.PI / 2;
  return g;
}

// Ventilatieventiel in het plafond
export function ventValve(scene, x, z, H) {
  const g = new THREE.Group();
  const wm = MAT.plastic('#f3f3f1');
  g.add(cyl(0.065, 0.006, wm, x, H - 0.003, z, { cast: false }));
  g.add(cyl(0.05, 0.018, wm, x, H - 0.015, z, { rTop: 0.055 }));
  g.add(cyl(0.045, 0.003, new THREE.MeshStandardMaterial({ color: '#6f6f6c', roughness: 0.8 }), x, H - 0.007, z, { cast: false }));
  g.add(cyl(0.03, 0.006, wm, x, H - 0.027, z));
  scene.add(g);
  return g;
}

// Vrijstaand bad (ovaal); lokaal midden op x=0, z=0
export function freestandingBath(mat, opts = {}) {
  const { l = 1.7, w = 0.8, h = 0.58 } = opts;
  const g = new THREE.Group();
  let outer = extrudeY(roundedRectShape(l, w, w * 0.48), h, 0.03, 5, 64);
  const p = outer.attributes.position;
  for (let i = 0; i < p.count; i++) { const t = p.getY(i) / h; const s = 0.82 + 0.18 * Math.pow(t, 0.6); p.setX(i, p.getX(i) * (0.9 + 0.1 * s)); p.setZ(i, p.getZ(i) * s); }
  outer = smoothNormals(outer);
  g.add(mesh(outer, mat));
  const innerMat = mat.clone(); innerMat.side = THREE.BackSide;
  const inner = extrudeY(roundedRectShape(l - 0.08, w - 0.08, (w - 0.08) * 0.48), h - 0.12, 0.05, 5, 64);
  inner.translate(0, 0.13, 0);
  const im = new THREE.Mesh(inner, innerMat); im.receiveShadow = true;
  g.add(im);
  // rand: ring bovenop die binnen- en buitenkant verbindt
  const rs = roundedRectShape(l, w, w * 0.48);
  rs.holes.push(roundedRectPath(l - 0.08, w - 0.08, (w - 0.08) * 0.48));
  const rim = extrudeY(rs, 0.012, 0.005, 3, 64);
  rim.translate(0, h - 0.012, 0);
  g.add(mesh(rim, mat));
  return g;
}

// Fonteintje (klein handwasbakje) aan de wand, met kraantje
export function fontein(opts = {}) {
  const { w = 0.36, d = 0.22, y = 0.85, mat = MAT.ceramic(), tap = MAT.chrome() } = opts;
  const g = new THREE.Group();
  const s = roundedRectShape(w, d, 0.035, 0, -d / 2);
  s.holes.push(roundedRectPath(w - 0.05, d - 0.07, 0.03, 0, -d / 2 - 0.015));
  const shell = extrudeY(s, 0.11, 0.006, 3, 32);
  shell.translate(0, y - 0.11, 0);
  g.add(mesh(shell, mat));
  const bottom = extrudeY(roundedRectShape(w - 0.04, d - 0.06, 0.03, 0, -d / 2 - 0.015), 0.02, 0.003, 2, 32);
  bottom.translate(0, y - 0.1, 0);
  g.add(mesh(bottom, mat));
  g.add(cyl(0.014, 0.003, MAT.chrome(), 0, y - 0.078, d / 2 + 0.015));
  // kraantje op de achterrand
  g.add(cyl(0.014, 0.1, tap, 0, y + 0.05, 0.03));
  g.add(tube([[0, y + 0.09, 0.03], [0, y + 0.115, 0.05], [0, y + 0.1, 0.1], [0, y + 0.075, 0.11]], 0.007, tap));
  g.add(cylBetween(new THREE.Vector3(0, y + 0.08, 0.03), new THREE.Vector3(0, y + 0.13, 0.0), 0.004, tap));
  // sifon onder
  g.add(cyl(0.016, 0.12, tap, 0, y - 0.17, d / 2 + 0.015));
  g.add(tube([[0, y - 0.23, d / 2 + 0.015], [0, y - 0.27, d / 2 - 0.01], [0, y - 0.25, 0.04], [0, y - 0.24, 0]], 0.015, tap));
  return g;
}

// Kitrand: kwartrond profiel langs een lijn (van a naar b), omhoog naar de hoek
export function sealant(a, b, r, mat, rot = 0) {
  const A = new THREE.Vector3(...a), B = new THREE.Vector3(...b);
  const len = A.distanceTo(B);
  const geo = new THREE.CylinderGeometry(r, r, len, 12, 1, false, rot, Math.PI / 2);
  const m = new THREE.Mesh(geo, mat);
  m.position.copy(A).add(B).multiplyScalar(0.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), B.clone().sub(A).normalize());
  m.receiveShadow = true;
  return m;
}

// Plastic tegelkruisje (lokaal in xy-vlak, plat op een wand)
export function tileCross(size = 0.02, t = 0.003, mat = MAT.plastic('#e8e2d0'), depth = 0.01) {
  const g = new THREE.Group();
  g.add(box(size, t, depth, mat, 0, 0, 0, { worldUV: false }));
  g.add(box(t, size, depth, mat, 0, 0, 0, { worldUV: false }));
  return g;
}

// Lijmkam: blad met tanden en handvat. Lokaal plat (blad in xz-vlak).
export function notchedTrowel() {
  const g = new THREE.Group();
  const steel = new THREE.MeshStandardMaterial({ color: '#b9bcbd', metalness: 0.9, roughness: 0.35 });
  const L = 0.28, Wd = 0.12;
  const s = new THREE.Shape();
  s.moveTo(-L / 2, -Wd / 2);
  const teeth = 18;
  for (let i = 0; i < teeth; i++) {
    const x0 = -L / 2 + (i / teeth) * L, x1 = x0 + L / teeth;
    s.lineTo(x0, -Wd / 2); s.lineTo(x0, -Wd / 2 - 0.008); s.lineTo((x0 + x1) / 2, -Wd / 2 - 0.008); s.lineTo((x0 + x1) / 2, -Wd / 2);
  }
  s.lineTo(L / 2, -Wd / 2); s.lineTo(L / 2, Wd / 2); s.lineTo(-L / 2, Wd / 2); s.lineTo(-L / 2, -Wd / 2);
  const blade = new THREE.ExtrudeGeometry(s, { depth: 0.0012, bevelEnabled: false });
  blade.rotateX(-Math.PI / 2);
  g.add(mesh(blade, steel));
  const hm = new THREE.MeshStandardMaterial({ color: '#2b5f8a', roughness: 0.5 });
  g.add(box(0.2, 0.01, 0.02, new THREE.MeshStandardMaterial({ color: '#888', metalness: 0.8, roughness: 0.4 }), 0, 0.006, 0, { worldUV: false }));
  g.add(rbox(0.13, 0.032, 0.034, 0.014, hm, 0, 0.045, 0));
  g.add(box(0.01, 0.035, 0.01, hm, -0.05, 0.022, 0, { worldUV: false }));
  g.add(box(0.01, 0.035, 0.01, hm, 0.05, 0.022, 0, { worldUV: false }));
  return g;
}

// Stapel tegels (dozen of losse tegels). Lokaal: onderkant op y=0.
export function tileStack(mat, tw, th, n = 8, t = 0.009, seed = 3) {
  const g = new THREE.Group();
  const R = rng(seed);
  for (let i = 0; i < n; i++) {
    const m = rbox(tw, t, th, 0.0015, mat, (R() - 0.5) * 0.006, t / 2 + i * t, (R() - 0.5) * 0.006);
    m.rotation.y = (R() - 0.5) * 0.015;
    g.add(m);
  }
  return g;
}

// Hoekstopkraan met knop (lokaal uit de wand op z=0, uitgang naar beneden)
export function angleValve(mat, x, y) {
  const g = new THREE.Group();
  g.add(cyl(0.028, 0.01, mat, x, y, 0.005, { axis: 'z' }));
  g.add(cyl(0.009, 0.05, mat, x, y, 0.03, { axis: 'z' }));
  g.add(cyl(0.013, 0.03, mat, x, y, 0.055, { axis: 'z' }));
  g.add(cyl(0.006, 0.025, mat, x, y - 0.012, 0.055));
  g.add(cyl(0.012, 0.012, mat, x, y, 0.075, { axis: 'z' }));
  return g;
}

/* ------------------------------------------------------------------ */
/* Export                                                               */
/* ------------------------------------------------------------------ */

function shrinkTo(src, w, h) {
  const c = canvas(w, h), x = c.getContext('2d');
  x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high';
  x.drawImage(src, 0, 0, w, h);
  return c;
}

async function encode(c, maxBytes) {
  let q = 0.88, data;
  for (;;) {
    data = c.toDataURL('image/webp', q);
    const bytes = Math.round((data.length - data.indexOf(',') - 1) * 0.75);
    if (bytes <= maxBytes || q <= 0.5) return { data, q, bytes };
    q = Math.round((q - 0.02) * 100) / 100;
  }
}

export function installExport(renderer, base) {
  window.exportAll = async () => {
    const c1600 = shrinkTo(renderer.domElement, 1600, 1067);
    const c800 = shrinkTo(c1600, 800, 533);
    const c400 = shrinkTo(c800, 400, 267);
    const out = [];
    for (const [c, w, max] of [[c1600, 1600, 245 * 1024], [c800, 800, 90 * 1024], [c400, 400, 30 * 1024]]) {
      const { data, q, bytes } = await encode(c, max);
      const name = `${base}-${w}.webp`;
      const r = await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, data }) });
      out.push({ name, q, bytes, ok: (await r.json()).ok });
    }
    return out;
  };
  // proefversie (alleen 1600) om te beoordelen
  window.preview = async () => {
    const c = shrinkTo(renderer.domElement, 1600, 1067);
    const data = c.toDataURL('image/jpeg', 0.9);
    await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: `preview-${base}.webp`, data: c.toDataURL('image/webp', 0.9) }) });
    return 'ok';
  };
}

export function pageStyle() {
  const s = document.createElement('style');
  s.textContent = 'html,body{margin:0;background:#222;height:100%;display:flex;align-items:center;justify-content:center}canvas{max-width:100vw;max-height:100vh;width:auto!important;height:auto!important;aspect-ratio:3/2}';
  document.head.appendChild(s);
}

// Omgevingskaart, accumulatie en export. ?n=16 voor een snelle proef, ?auto=1 exporteert.
export async function finish(renderer, scene, camera, base, opts = {}) {
  const q = new URLSearchParams(location.search);
  const frames = +(q.get('n') ?? opts.frames ?? 64);
  const boost = opts.envBoost ?? 1;
  const seen = new Set();
  if (boost !== 1) scene.traverse((o) => { const m = o.material; if (m && !seen.has(m) && m.envMapIntensity !== undefined) { seen.add(m); m.envMapIntensity *= boost; } });
  // zwak, schaduwloos basislicht (vooral voor het plafond: de grondkleur schijnt omhoog)
  if (opts.hemi !== 0) scene.add(new THREE.HemisphereLight('#f4f1ec', '#efe9df', opts.hemi ?? 0.35));
  captureEnvironment(renderer, scene, opts.envPos ?? [1.5, 1.4, 1.5], opts.envAmbient ?? 0.9);
  window.__scene = scene;
  window.__rerender = (n = 4) => renderAccum(renderer, scene, camera, n, 1);
  const t0 = performance.now();
  await renderAccum(renderer, scene, camera, frames, opts.seed ?? 1);
  installExport(renderer, base);
  window.renderMs = Math.round(performance.now() - t0);
  if (q.get('auto')) { window.exportResult = await window.exportAll(); }
  else if (q.get('preview')) { await window.preview(); }
  window.ready = true;
  document.title = 'klaar';
}

/* ------------------------------------------------------------------ */
/* Standaardbelichting en extra objecten                                */
/* ------------------------------------------------------------------ */

// Raamlicht (eerste raam) plus kaatslicht over vloer, wanden en plafond.
export function autoLights(scene, R, opts = {}) {
  const { W, D, H } = R;
  if (R.windows[0] && opts.window !== 0) windowLight(scene, { ...R.windows[0], intensity: opts.window ?? 14 });
  const c = opts.colors ?? {};
  const surfaces = [
    { origin: [0.15, 0, 0.15], u: [W - 0.3, 0, 0], v: [0, 0, D - 0.3], normal: [0, 1, 0], color: c.floor ?? '#efe9e0', weight: 2 },
    { origin: [0, 0.2, 0.15], u: [0, 0, D - 0.3], v: [0, H - 0.4, 0], normal: [1, 0, 0], color: c.left ?? '#f1ede6', weight: 1 },
    { origin: [W, 0.2, 0.15], u: [0, 0, D - 0.3], v: [0, H - 0.4, 0], normal: [-1, 0, 0], color: c.right ?? '#f1ede6', weight: 1 },
    { origin: [0.15, 0.2, 0], u: [W - 0.3, 0, 0], v: [0, H - 0.4, 0], normal: [0, 0, 1], color: c.back ?? '#f1ede6', weight: 1 },
    { origin: [0.15, 0.2, D], u: [W - 0.3, 0, 0], v: [0, H - 0.4, 0], normal: [0, 0, -1], color: c.front ?? '#f1ede6', weight: 0.7 },
    { origin: [0.15, H, 0.15], u: [W - 0.3, 0, 0], v: [0, 0, D - 0.3], normal: [0, -1, 0], color: c.ceil ?? '#f6f4f0', weight: 1 },
  ];
  bounceLight(scene, { surfaces, target: opts.target ?? [W / 2, H * 0.42, D / 2], intensity: opts.bounce ?? 7, count: opts.count ?? 3, avoid: opts.avoid ?? [] });
}

// Ribbels (gekamde tegellijm) of glad, als textuur
export function adhesiveMaterial(hex = '#9c9a95', ribbed = true, seed = 6) {
  const S = 512, size = 0.3, ppm = S / size;
  const [r, g, b] = hexRGB(hex);
  const col = new Uint8ClampedArray(S * S * 3), hgt = new Float32Array(S * S);
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const n = pfbm(x / S, y / S, 8, 8, seed, 4);
    // horizontale ribbels, 10 mm steek, met wat golving
    const yy = y / ppm + (n - 0.5) * 0.004;
    const rib = ribbed ? Math.abs(((yy / 0.01) % 1) - 0.5) * 2 : 0.5;
    const i = y * S + x;
    const f = 0.85 + rib * 0.25 + (hash2(x, y, seed) - 0.5) * 0.08;
    col[i * 3] = r * f; col[i * 3 + 1] = g * f; col[i * 3 + 2] = b * f;
    hgt[i] = rib * 0.004 + (n - 0.5) * 0.0008;
  }
  return new THREE.MeshStandardMaterial({
    map: tex(rgbCanvas(col, S, S), true, [size, size]),
    normalMap: tex(normalCanvas(hgt, S, S, ppm), false, [size, size]),
    roughness: 0.85, envMapIntensity: 0.4,
  });
}

// Cementgebonden plaat / gipsplaat met schroeven
export function boardMaterial(hex = '#a3a9a8', seed = 2) {
  const S = 1024, size = 1.2, ppm = S / size;
  const [r, g, b] = hexRGB(hex);
  const col = new Uint8ClampedArray(S * S * 3), hgt = new Float32Array(S * S);
  for (let y = 0; y < S; y++) for (let x = 0; x < S; x++) {
    const n = pfbm(x / S, y / S, 10, 10, seed, 5);
    let f = 1 + (n - 0.5) * 0.12 + (hash2(x, y, seed) - 0.5) * 0.06;
    // schroeven elke 30 cm, 5 cm uit de rand
    const sx = ((x / ppm) % 0.3) - 0.15, sy = ((y / ppm) % 0.3) - 0.15;
    if (sx * sx + sy * sy < 0.000012) f *= 0.8;
    const i = y * S + x;
    col[i * 3] = r * f; col[i * 3 + 1] = g * f; col[i * 3 + 2] = b * f;
    hgt[i] = (n - 0.5) * 0.0004;
  }
  return new THREE.MeshStandardMaterial({
    map: tex(rgbCanvas(col, S, S), true, [size, size]),
    normalMap: tex(normalCanvas(hgt, S, S, ppm), false, [size, size]),
    roughness: 0.95, envMapIntensity: 0.4,
  });
}

// Emmer (open) met inhoud
export function bucket(fill = '#a09d97', color = '#efefec') {
  const g = new THREE.Group();
  const m = MAT.plastic(color);
  const pts = [new THREE.Vector2(0.001, 0), new THREE.Vector2(0.13, 0), new THREE.Vector2(0.155, 0.3), new THREE.Vector2(0.165, 0.305), new THREE.Vector2(0.165, 0.315), new THREE.Vector2(0.15, 0.31), new THREE.Vector2(0.125, 0.012), new THREE.Vector2(0.001, 0.012)];
  g.add(mesh(new THREE.LatheGeometry(pts, 64), m));
  const fm = adhesiveMaterial(fill, false, 9);
  g.add(cyl(0.148, 0.01, fm, 0, 0.22, 0, { cast: false }));
  // hengsel
  g.add(tube([[-0.16, 0.27, 0], [-0.12, 0.42, 0.06], [0, 0.47, 0.09], [0.12, 0.42, 0.06], [0.16, 0.27, 0]], 0.003, MAT.brushed()));
  return g;
}

// Waterpas (60 cm), lokaal langs x
export function spiritLevel() {
  const g = new THREE.Group();
  g.add(rbox(0.6, 0.055, 0.025, 0.003, new THREE.MeshStandardMaterial({ color: '#e5b52b', roughness: 0.45 }), 0, 0, 0));
  g.add(box(0.6, 0.008, 0.027, MAT.black(), 0, -0.024, 0, { worldUV: false }));
  g.add(box(0.6, 0.008, 0.027, MAT.black(), 0, 0.024, 0, { worldUV: false }));
  const vial = new THREE.MeshStandardMaterial({ color: '#b8e05a', emissive: '#304010', roughness: 0.2 });
  for (const x of [-0.2, 0, 0.2]) g.add(rbox(0.05, 0.016, 0.028, 0.006, vial, x, 0, 0));
  return g;
}

// Steeksleutel / verstelbare sleutel, plat op de vloer (lokaal langs x)
export function wrench() {
  const g = new THREE.Group();
  const m = new THREE.MeshStandardMaterial({ color: '#b7b9bb', metalness: 1, roughness: 0.3 });
  g.add(rbox(0.2, 0.008, 0.024, 0.004, m, 0, 0.004, 0));
  g.add(rbox(0.05, 0.012, 0.05, 0.006, m, 0.115, 0.006, 0));
  g.add(box(0.03, 0.013, 0.016, MAT.black(), 0.135, 0.006, 0, { worldUV: false }));
  g.add(rbox(0.09, 0.011, 0.028, 0.005, new THREE.MeshStandardMaterial({ color: '#b3261e', roughness: 0.5 }), -0.06, 0.006, 0));
  return g;
}

// Flessensifon met afvoer naar de wand (lokaal: wand op z=0). x,yTop,zDrain: onder de afvoerplug.
export function bottleTrap(mat, x, yTop, zDrain) {
  const g = new THREE.Group();
  g.add(cyl(0.016, 0.16, mat, x, yTop - 0.08, zDrain));
  g.add(cyl(0.028, 0.012, mat, x, yTop - 0.165, zDrain));
  g.add(cyl(0.026, 0.13, mat, x, yTop - 0.235, zDrain));
  g.add(cyl(0.028, 0.012, mat, x, yTop - 0.3, zDrain));
  g.add(cyl(0.016, zDrain, mat, x, yTop - 0.19, zDrain / 2, { axis: 'z' }));
  g.add(cyl(0.04, 0.008, mat, x, yTop - 0.19, 0.004, { axis: 'z' }));
  return g;
}

// Flexibele slang (gevlochten RVS) langs punten
export function hose(points) {
  const c = canvas(64, 64), x = c.getContext('2d');
  x.fillStyle = '#9a9a98'; x.fillRect(0, 0, 64, 64);
  for (let i = 0; i < 64; i += 4) { x.strokeStyle = 'rgba(255,255,255,0.5)'; x.beginPath(); x.moveTo(i, 0); x.lineTo(i + 32, 64); x.stroke(); x.strokeStyle = 'rgba(0,0,0,0.35)'; x.beginPath(); x.moveTo(i + 32, 0); x.lineTo(i, 64); x.stroke(); }
  const t = tex(c, true); t.repeat.set(30, 1);
  const m = new THREE.MeshStandardMaterial({ map: t, metalness: 0.9, roughness: 0.35 });
  return tube(points, 0.0065, m, 64);
}

// Kitrand met holle (afgestreken) vorm. Profiel in de hoek x>=0, y>=0, lengte langs +z.
// orient: 'z' (langs wand x=0 op de vloer), 'x' (langs wand z=0 op de vloer), 'y' (verticale hoek x=0,z=0)
export function sealBead(len, r, mat, orient = 'z') {
  const s = new THREE.Shape();
  s.moveTo(0, 0); s.lineTo(r, 0);
  s.quadraticCurveTo(r * 0.3, r * 0.3, 0, r);
  s.lineTo(0, 0);
  const g = new THREE.ExtrudeGeometry(s, { depth: len, bevelEnabled: false, curveSegments: 10 });
  if (orient === 'x') { g.rotateY(-Math.PI / 2); g.translate(len, 0, 0); }
  else if (orient === 'y') { g.rotateX(Math.PI / 2); g.translate(0, len, 0); }
  const m = new THREE.Mesh(g, mat);
  m.receiveShadow = true;
  m.castShadow = false;
  return m;
}
