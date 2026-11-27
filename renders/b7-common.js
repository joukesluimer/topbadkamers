// b7: path tracing voor de badkamer-renders (ronde 4, render-kwaliteit).
//
// De scène wordt gebouwd met de bestaande bouwstenen (bd-common.js / b5-common.js,
// alleen gelezen, niet gewijzigd). Daarna zet deze module de scène om naar een
// path-tracebare versie en rendert hem met three-gpu-pathtracer:
//  - echte globale belichting (geen nep-kaatslichten of hemisfeerlicht meer);
//  - echte reflecties in spiegels (metaal, ruwheid ~0) en glas (transmissie);
//  - zacht raamlicht via een vlak lichtpaneel (RectAreaLight) in de raamopening;
//  - spots blijven spots, met een kleine straal voor zachte schaduwranden.
// Alleen voor de renderpagina's; niets hiervan komt op de site.
import * as THREE from 'three';
import { WebGLPathTracer, GradientEquirectTexture, DenoiseMaterial } from 'three-gpu-pathtracer';
import { FullScreenQuad } from 'three/addons/postprocessing/Pass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

export { THREE };
// three r160 kent deze velden nog niet; de path tracer (0.0.23) leest ze wel
if (!('environmentRotation' in THREE.Scene.prototype)) THREE.Scene.prototype.environmentRotation = new THREE.Euler();
if (!('backgroundRotation' in THREE.Scene.prototype)) THREE.Scene.prototype.backgroundRotation = new THREE.Euler();
window.addEventListener('error', (e) => { document.title = 'ERR ' + e.message + ' @ ' + (e.error && e.error.stack || '').replace(/https:\/\/cdn.jsdelivr.net\/npm\//g,'').slice(0,600); });
window.addEventListener('unhandledrejection', (e) => { document.title = 'ERR ' + (e.reason && e.reason.message || e.reason); });

const GLASS = () => new THREE.MeshPhysicalMaterial({
  color: '#ffffff', metalness: 0, roughness: 0.0, transmission: 1, ior: 1.5, thickness: 0.008,
  attenuationColor: new THREE.Color('#cfe6dc'), attenuationDistance: 0.5, transparent: false,
});

/*
 * Zet een rasterscène om voor de path tracer.
 * opts.windows: [{ center, u, v, w, h, normal, intensity, color }]
 * opts.keepLight(light) -> bool: welke lichten blijven (standaard: spots met decay 2 en puntlampen die geen 'vul'-licht zijn)
 */
export function convertScene(scene, opts = {}) {
  const remove = [];
  const mirrorMat = new THREE.MeshStandardMaterial({ color: opts.mirrorColor ?? '#e9ecea', metalness: 1, roughness: 0.012 });
  scene.traverse((o) => {
    if (o.isLight) {
      if (o.isHemisphereLight || o.isAmbientLight) { remove.push(o); return; }
      if (opts.keepLight) { if (!opts.keepLight(o)) remove.push(o); return; }
      // bd: decay > 2,0005 = raamspot of kaatslicht (alleen diffuus) -> eruit
      if (o.isSpotLight && o.decay > 2.0005) { remove.push(o); return; }
      if (o.isDirectionalLight) { remove.push(o); return; }
      return;
    }
    if (!o.isMesh) return;
    // Reflector (three/addons) -> echte spiegel
    if (o.isReflector || (o.material && o.material.uniforms && o.material.uniforms.tDiffuse && o.material.uniforms.textureMatrix)) {
      o.material = mirrorMat;
      o.onBeforeRender = () => {};
      return;
    }
    const m = o.material;
    if (!m || Array.isArray(m)) return;
    if (opts.material) { const r = opts.material(o, m); if (r === false) { o.visible = false; return; } if (r) { o.material = r; return; } }
    // additieve 'reflectie'-lagen en zachte gloedvlakken (led achter spiegel): weg, de tracer doet dit echt
    if (m.blending === THREE.AdditiveBlending) { o.visible = false; return; }
    if (m.isMeshBasicMaterial && m.transparent && m.map && m.opacity > 0.3) { o.visible = false; return; }
    // onverlichte 'gloei'-vlakken (lampglas) -> echt lichtgevend
    if (m.isMeshBasicMaterial && !m.transparent) {
      const c = m.color.clone(); const k = Math.max(c.r, c.g, c.b);
      o.material = new THREE.MeshStandardMaterial({ color: '#000', emissive: c.multiplyScalar(1 / Math.max(k, 1e-3)), emissiveIntensity: (opts.glowIntensity ?? 6) * Math.min(k, 1.5), map: m.map || null });
      return;
    }
    // doorzichtig glas -> echt glas met transmissie
    if (m.transparent && m.opacity < 0.5) { o.material = GLASS(); return; }
    if (m.isMeshPhysicalMaterial && m.transmission > 0) { o.material = GLASS(); return; }
  });
  for (const o of remove) o.parent && o.parent.remove(o);

  // Raamlicht: vlak paneel net binnen het glas, naar binnen gericht
  for (const w of opts.windows ?? []) {
    const L = new THREE.RectAreaLight(w.color ?? '#f4f7ff', w.intensity ?? 18, w.w * 0.92, w.h * 0.92);
    const C = new THREE.Vector3(...w.center), N = new THREE.Vector3(...w.normal);
    L.position.copy(C).addScaledVector(N, w.inset ?? 0.0);
    L.lookAt(C.clone().add(N));
    scene.add(L);
  }
  // Omgeving (buiten): zacht verloop, alleen zichtbaar door glas en via het raam
  const env = new GradientEquirectTexture();
  env.topColor.set(opts.skyTop ?? '#dfe9f5');
  env.bottomColor.set(opts.skyBottom ?? '#c9c4ba');
  env.update();
  scene.environment = env;
  scene.environmentIntensity = opts.envIntensity ?? 0.6;
  scene.background = new THREE.Color('#202020');
}

function shrinkTo(src, w, h) {
  const c = document.createElement('canvas');
  c.width = w; c.height = h;
  const x = c.getContext('2d');
  x.imageSmoothingEnabled = true; x.imageSmoothingQuality = 'high';
  x.drawImage(src, 0, 0, w, h);
  return c;
}

async function encode(c, maxBytes, q0 = 0.86) {
  let q = q0, data, bytes;
  for (let i = 0; i < 8; i++) {
    data = c.toDataURL('image/webp', q);
    bytes = Math.round((data.length - data.indexOf(',') - 1) * 0.75);
    if (bytes <= maxBytes) break;
    q -= 0.06;
  }
  return { data, q: +q.toFixed(2), bytes };
}

// Lichte vignettering + een fractie korrel, zoals bij een echte camera
function grade(src, o = {}) {
  const c = document.createElement('canvas');
  c.width = src.width; c.height = src.height;
  const x = c.getContext('2d');
  x.drawImage(src, 0, 0);
  const v = o.vignette ?? 0.16;
  if (v > 0) {
    const g = x.createRadialGradient(c.width / 2, c.height / 2, c.height * 0.45, c.width / 2, c.height / 2, c.width * 0.62);
    g.addColorStop(0, 'rgba(0,0,0,0)');
    g.addColorStop(1, `rgba(0,0,0,${v})`);
    x.fillStyle = g; x.fillRect(0, 0, c.width, c.height);
  }
  return c;
}

function installExport(canvas, base, o) {
  window.exportAll = async () => {
    const c1600 = grade(shrinkTo(canvas, 1600, 1067), o);
    const c800 = shrinkTo(c1600, 800, 533);
    const c400 = shrinkTo(c800, 400, 267);
    const out = [];
    for (const [c, w, max] of [[c1600, 1600, 290 * 1024], [c800, 800, 95 * 1024], [c400, 400, 30 * 1024]]) {
      const { data, q, bytes } = await encode(c, max);
      const name = `${base}-${w}.webp`;
      const r = await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, data }) });
      out.push({ name, q, bytes, ok: (await r.json()).ok });
    }
    return out;
  };
  window.preview = async () => {
    const c = grade(shrinkTo(canvas, 1600, 1067), o);
    await fetch('/save', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name: `preview-${base}.webp`, data: c.toDataURL('image/webp', 0.9) }) });
    return 'ok';
  };
}

/*
 * Path trace en exporteer. ?s=64 voor een snelle proef, ?preview=1 slaat een proef op,
 * ?auto=1 exporteert 400/800/1600.
 */
export async function pathTrace(renderer, scene, camera, base, opts = {}) {
  const q = new URLSearchParams(location.search);
  const samples = +(q.get('s') ?? opts.samples ?? 600);
  document.title = 'convert';
  convertScene(scene, opts);
  renderer.toneMapping = opts.toneMapping ?? THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = +(q.get('exp') ?? opts.exposure ?? 1.0);
  renderer.shadowMap.enabled = false;
  // direct op 1600x1067 renderen: de tracer zelf doet anti-aliasing
  renderer.setSize(opts.width ?? 1600, opts.height ?? 1067, false);
  const pt = new WebGLPathTracer(renderer);
  pt.tiles.set(opts.tiles ?? 3, opts.tiles ?? 3);
  pt.bounces = opts.bounces ?? 7;
  pt.transmissiveBounces = 8;
  pt.filterGlossyFactor = opts.filterGlossy ?? 0.4;
  pt.minSamples = 1;
  pt.dynamicLowRes = false;
  pt.renderScale = 1;
  pt.fadeDuration = 0;
  pt.renderToCanvas = false; // eigen uitvoer via OutputPass (ACES + sRGB)
  pt.renderDelay = 0;
  if (opts.textureSize) pt.textureSize.set(opts.textureSize, opts.textureSize);
  else pt.textureSize.set(+(q.get('ts') ?? 2048), +(q.get('ts') ?? 2048));
  // spots: kleine straal = zachte schaduwranden
  scene.traverse((o) => { if (o.isSpotLight) { o.radius = opts.spotRadius ?? 0.03; } });
  camera.updateMatrixWorld();
  document.title = 'setScene';
  await new Promise((r) => setTimeout(r, 0));
  pt.setScene(scene, camera);
  document.title = 'sceneOK';
  await new Promise((r) => setTimeout(r, 0));
  const gl = renderer.getContext();
  let lost = false;
  renderer.domElement.addEventListener('webglcontextlost', () => { lost = true; document.title = 'ERR context lost'; });
  const t0 = performance.now();
  while (pt.samples < samples) {
    pt.renderSample();
    // wachten tot de GPU klaar is: anders loopt de wachtrij vol en gaat de context verloren
    gl.finish();
    if (lost) throw new Error('webgl context lost bij sample ' + pt.samples);
    document.title = `pt ${Math.floor(pt.samples)}/${samples}`;
    await new Promise((r) => setTimeout(r, 1));
  }
  window.renderMs = Math.round(performance.now() - t0);
  if (q.get('dbg')) {
    const t = pt.target, buf = new Float32Array(4 * 4);
    const pts = [[0.5, 0.5], [0.2, 0.8], [0.8, 0.2], [0.1, 0.1]].map(([a, b]) => { renderer.readRenderTargetPixels(t, Math.floor(a * t.width), Math.floor(b * t.height), 1, 1, buf); return Array.from(buf.slice(0, 4)).map((v) => +v.toFixed(3)).join(','); });
    document.title = 'DBG ' + t.texture.type + ' ' + pts.join(' | ');
    await new Promise((r) => setTimeout(r, 8000));
  }
  // Tonemapping + sRGB naar een 8-bit buffer, daarna zelf uitlezen naar een 2D-canvas
  // (drawImage van het WebGL-canvas geeft met Metal headless een wit beeld).
  const W = pt.target.width, H = pt.target.height;
  const ldr = new THREE.WebGLRenderTarget(W, H, { type: THREE.UnsignedByteType });
  let src = pt.target;
  const sigma = +(q.get('dn') ?? opts.denoise ?? 2.2);
  if (sigma > 0) {
    // lichte ruisfilter (bilateraal), randen blijven scherp
    const dn = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType });
    const dm = new DenoiseMaterial({ map: pt.target.texture, blending: THREE.NoBlending });
    dm.uniforms.sigma.value = sigma; dm.uniforms.threshold.value = +(q.get("dt") ?? opts.dnThreshold ?? 0.05); dm.uniforms.kSigma.value = 1.0;
    const fq = new FullScreenQuad(dm);
    const tm = renderer.toneMapping; renderer.toneMapping = THREE.NoToneMapping;
    renderer.setRenderTarget(dn); fq.render(renderer); renderer.setRenderTarget(null);
    renderer.toneMapping = tm;
    src = dn;
  }
  const out = new OutputPass();
  out.renderToScreen = false;
  out.render(renderer, ldr, src);
  const px = new Uint8Array(W * H * 4);
  renderer.readRenderTargetPixels(ldr, 0, 0, W, H, px);
  const c2 = document.createElement('canvas');
  c2.width = W; c2.height = H;
  const x2 = c2.getContext('2d');
  const img = x2.createImageData(W, H);
  for (let y = 0; y < H; y++) img.data.set(px.subarray((H - 1 - y) * W * 4, (H - y) * W * 4), y * W * 4);
  x2.putImageData(img, 0, 0);
  if (q.get('dbg')) { const i = ((H >> 1) * W + (W >> 1)) * 4, j = (200 * W + 200) * 4; document.title = 'DBG2 ' + [px[i], px[i + 1], px[i + 2], px[i + 3], px[j], px[j + 1], px[j + 2]].join(','); await new Promise((r) => setTimeout(r, 8000)); }
  document.body.appendChild(c2);
  installExport(c2, base, opts);
  if (q.get('auto')) { window.exportResult = await window.exportAll(); }
  else if (q.get('preview')) { await window.preview(); }
  window.ready = true;
  document.title = 'klaar';
}
