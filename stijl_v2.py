"""Stijl v2 (ronde 4): premium woon- en interieurlook bovenop STYLE_CSS.

Inbouwen in build.py, vóór de CSS wordt weggeschreven:
    import stijl_v2
    assets.STYLE_CSS += stijl_v2.CSS

Alleen CSS, geen HTML-wijzigingen nodig. Geen webfont: koppen gebruiken een
serif-stapel van het systeem (Iowan Old Style / Palatino / Georgia).
De header-scrollklasse `is-gescrold` zet de bestaande APP_JS al.
"""

CSS = r"""
/* =====================================================================
   Stijl v2: premium woon- en interieurlook
   ===================================================================== */
:root{
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,"Times New Roman",serif;
  --bg-soft:#f7f4ef;
  --zand:#efe9df;
  --line:#e4ded3;
  --line-koel:#d9e5e7;
  --radius:14px;
  --radius-lg:20px;
  --shadow:0 1px 1px rgba(8,47,55,.04),0 2px 6px rgba(8,47,55,.04),0 12px 28px -14px rgba(8,47,55,.16);
  --shadow-lg:0 2px 4px rgba(8,47,55,.05),0 10px 20px -8px rgba(8,47,55,.10),0 30px 60px -22px rgba(8,47,55,.28);
  --focus:#0b4a56;
  --voeg:rgba(11,74,86,.045);
}
::selection{background:#f6d3c3;color:#082f37}

/* ---------- Typografie ---------- */
body{font-size:17px;line-height:1.7;text-rendering:optimizeLegibility}
h1,h2,.footer-cta-titel,.cta-midden-titel{font-family:var(--serif);font-weight:700;letter-spacing:-.012em}
h1{font-size:clamp(2.05rem,1.25rem + 3.2vw,3.4rem);line-height:1.08;text-wrap:balance}
h2{font-size:clamp(1.6rem,1.15rem + 1.75vw,2.35rem);line-height:1.14;text-wrap:balance}
h3{font-size:1.16rem;line-height:1.3;letter-spacing:-.01em;font-weight:700}
.formcard h2,.prijskaart h2{font-size:1.4rem}
p,li{text-wrap:pretty}
.lead{font-size:clamp(1.08rem,1rem + .35vw,1.2rem);line-height:1.65}
.prose{font-size:1.04rem}
.prose h2{margin-top:2.2em}
.prose h3{margin-top:1.6em}
.feit-getal,.bedrag{font-family:var(--serif);letter-spacing:-.01em}

/* Eyebrow / badge: rustiger, meer letterafstand */
.badge{background:#fff;color:#9c4019;font-size:.72rem;letter-spacing:.12em;font-weight:700;padding:6px 13px 6px 11px;
  box-shadow:inset 0 0 0 1px rgba(196,81,31,.28)}
.badge::before{content:"";display:inline-block;width:6px;height:6px;border-radius:50%;background:var(--accent);margin:0 8px 1px 0;vertical-align:middle}
.badge-dark{background:rgba(255,255,255,.08);color:#f6c9b5;box-shadow:inset 0 0 0 1px rgba(255,255,255,.2)}
.badge-dark::before{background:#f0a37f}
.hero .badge::before,.badge:has(.dot)::before{display:none}
.badge:has(svg)::before{display:none}

/* ---------- Ritme, sectie-achtergronden, tegelvoeg-textuur ---------- */
.section{padding:clamp(60px,7.5vw,104px) 0}
.section-sm{padding:clamp(40px,5vw,64px) 0}
.soft{background-color:var(--bg-soft);
  background-image:linear-gradient(var(--voeg) 1px,transparent 1px),linear-gradient(90deg,var(--voeg) 1px,transparent 1px);
  background-size:64px 64px;background-position:-1px -1px}
.soft .card,.soft .feit,.soft .formcard{background:#fff}
hr{border-top-color:var(--line)}

/* ---------- Header: glas, rustig, past op één regel ---------- */
.header{background:rgba(255,255,255,.78);-webkit-backdrop-filter:saturate(170%) blur(16px);backdrop-filter:saturate(170%) blur(16px);
  border-bottom:1px solid rgba(228,222,211,.7);transition:box-shadow .25s ease,background .25s ease}
.header.is-gescrold{background:rgba(255,255,255,.86);box-shadow:0 1px 0 rgba(8,47,55,.04),0 10px 30px -18px rgba(8,47,55,.35)}
@supports not ((backdrop-filter:blur(1px)) or (-webkit-backdrop-filter:blur(1px))){.header{background:#fff}}
.header .wrap{max-width:1240px}
.header-in{gap:20px}
.nav a:not(.btn){font-weight:600;color:#123a42;border-radius:999px;padding:8px 12px}
.nav a:not(.btn):hover{background:rgba(11,74,86,.06)}
.nav .btn{padding:10px 18px;font-size:.93rem}
@media(min-width:901px) and (max-width:1279px){
  .header-in{gap:12px}
  .nav{gap:0}
  .nav a:not(.btn){font-size:.88rem;padding:8px 8px}
  .nav .btn{margin-left:6px;padding:9px 14px;font-size:.88rem}
}
@media(min-width:901px) and (max-width:1060px){.logo img{height:32px}}
/* Mobiele menuknop en paneel */
.burger{border:1px solid var(--line);background:#fff;box-shadow:0 1px 2px rgba(8,47,55,.06);transition:background .2s,border-color .2s,color .2s}
.burger:hover{border-color:#cfc6b8}
.burger[aria-expanded="true"]{background:var(--navy);border-color:var(--navy);color:#fff}
@media(max-width:900px){
  .nav{background:rgba(255,255,255,.97);border-radius:0 0 22px 22px;box-shadow:0 24px 48px -20px rgba(8,47,55,.35);border-bottom:1px solid var(--line)}
  .nav a:not(.btn){border-radius:14px}
  .nav-ic{background:var(--bg-soft);color:var(--navy);box-shadow:inset 0 0 0 1px var(--line)}
}

/* ---------- Knoppen ---------- */
.btn{border-radius:999px;padding:13px 26px;font-weight:700;letter-spacing:.005em;line-height:1.3;vertical-align:middle}
.btn-lg{padding:16px 32px}
.btn-primary{background:linear-gradient(180deg,#c4511f,#ad461a);color:#fff;border-color:#a8431a;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.18),0 1px 2px rgba(120,45,14,.25),0 8px 20px -8px rgba(168,67,26,.6)}
.btn-primary:hover{background:linear-gradient(180deg,#b54a1c,#983c16);color:#fff;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),0 2px 4px rgba(120,45,14,.25),0 14px 28px -10px rgba(168,67,26,.65)}
.btn-primary:active{box-shadow:inset 0 2px 4px rgba(0,0,0,.18)}
.btn-dark{background:linear-gradient(180deg,#105a68,#0b4a56);border-color:#0a4350;box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 8px 20px -10px rgba(8,47,55,.6)}
.btn-ghost{background:#fff;border:1px solid var(--line);color:var(--ink);box-shadow:0 1px 2px rgba(8,47,55,.05)}
.btn-ghost:hover{border-color:#bfb5a6;color:var(--navy);background:#fff}
.dark .btn-ghost,.hero .btn-ghost{background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.28);color:#fff}

/* ---------- Kaarten ---------- */
.card{border-color:var(--line);border-radius:var(--radius-lg);box-shadow:0 1px 1px rgba(8,47,55,.03),0 2px 6px rgba(8,47,55,.035)}
a.card{box-shadow:0 1px 1px rgba(8,47,55,.03),0 2px 6px rgba(8,47,55,.035)}
a.card:hover,a.card:focus-visible,.g4 > .card:hover{border-color:#d8cfc1;box-shadow:var(--shadow-lg)}
a.card::after{height:2px;background:linear-gradient(90deg,var(--accent),#f0a37f)}
a.card > .foto img{aspect-ratio:3/2;object-fit:cover}
.card .ic{background:linear-gradient(140deg,#fbf3ee,#f6e3d8);box-shadow:inset 0 0 0 1px rgba(168,67,26,.14)}
a.card .price{background:var(--bg-soft);border-color:var(--line)}
.feit{border-color:var(--line);border-radius:var(--radius-lg)}

/* ---------- Formulieren ---------- */
.formcard{border-radius:24px;box-shadow:var(--shadow-lg);border:1px solid rgba(228,222,211,.8)}
input[type=text],input[type=email],input[type=tel],input[type=number],select,textarea{
  border-radius:12px;border:1.5px solid var(--line);background-color:#fff;min-height:48px}
textarea{min-height:120px}
input:hover:not(:focus),select:hover:not(:focus),textarea:hover:not(:focus){border-color:#cbbfae}
input:focus,select:focus,textarea:focus{border-color:var(--navy-500);box-shadow:0 0 0 4px rgba(11,74,86,.13)}
.choice label{border-radius:14px;border-color:var(--line);background:#fff}
.choice label:hover{border-color:#c9bca9}
.choice label:has(input:checked){border-color:var(--accent);background:#fdf3ee}
.steps div{height:4px}
label{color:var(--ink)}

/* ---------- Beeld: renders als ingelijste illustraties ---------- */
.foto img,.illu{border-radius:var(--radius-lg)}
.foto.render{border-radius:var(--radius-lg);isolation:isolate}
.foto.render > img{border-radius:var(--radius-lg)!important;box-shadow:0 2px 4px rgba(8,47,55,.06),0 24px 50px -24px rgba(8,47,55,.4)}
.foto.render::after{content:"";position:absolute;inset:0;border-radius:var(--radius-lg);box-shadow:inset 0 0 0 1px rgba(255,255,255,.14),inset 0 -60px 60px -40px rgba(8,30,35,.22);pointer-events:none}
.bi-fig img,.pc-fig img,.bs-ill img{border-radius:var(--radius-lg)}
a.card > .foto img,.card .bi-fig img,.bi-kaart .bi-fig img,.prijskaart > .foto img{border-radius:0}
/* Het label "Illustratie (3D-render)" */
.foto.render > figcaption,figure .bi-label,.bl-sc-ill,.bl-on-ill,.bl-hv-ill,.bl-dq-ill,.h2-ill{
  background:rgba(12,30,34,.66)!important;color:#fff!important;font-size:.64rem!important;font-weight:600;letter-spacing:.09em;text-transform:uppercase;
  padding:5px 10px 5px 9px!important;border-radius:999px!important;line-height:1.2;z-index:2;
  -webkit-backdrop-filter:blur(8px) saturate(140%);backdrop-filter:blur(8px) saturate(140%);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.16)}
.foto.render > figcaption,figure .bi-label{left:14px!important;bottom:14px!important}
.foto.render > figcaption::before,figure .bi-label::before,.bl-sc-ill::before,.bl-on-ill::before,.bl-hv-ill::before,.bl-dq-ill::before,.h2-ill::before{
  content:"";display:inline-block;width:5px;height:5px;border-radius:50%;background:#f0a37f;margin:0 7px 1px 0;vertical-align:middle}
.prose .foto img{box-shadow:var(--shadow)}

/* ---------- Tabellen en kaders ---------- */
table{border-color:var(--line)}
th{letter-spacing:.06em}

/* Pagina-intro's: warme in plaats van koele mesh, past bij de zandtint */
.section-sm:has(> .wrap > .g2 .formcard),.kosten-kop,.tool-hero{
  background:radial-gradient(620px 380px at 92% 18%,rgba(244,200,180,.5),transparent 70%),
             radial-gradient(520px 340px at 70% 100%,rgba(249,224,212,.55),transparent 70%),
             radial-gradient(460px 300px at 0% 0%,rgba(239,233,223,.95),transparent 70%),
             linear-gradient(180deg,#faf8f4 0%,#fff 85%)}
.nav .btn{border-radius:999px}

/* ---------- Footer ---------- */
.footer{background-color:#0b4a56;
  background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px),
    linear-gradient(180deg,#0b4a56 0%,#083b45 100%);
  background-size:64px 64px,64px 64px,100% 100%;color:#b4c6c9}
.footer a{color:#c3d2d4;transition:color .15s}
.footer a:hover{color:#fff;text-decoration:underline;text-underline-offset:3px;text-decoration-color:rgba(240,163,127,.7)}
.footer .fh{font-family:var(--font);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:#f3c3ad}
.footer-cta{background:linear-gradient(135deg,rgba(255,255,255,.09),rgba(255,255,255,.03));border-color:rgba(255,255,255,.14);border-radius:24px;padding:26px 30px;
  -webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
.footer-cta .footer-cta-titel{font-size:1.35rem;font-weight:700}
.footer-bot{color:#a8babd}

/* ---------- Focus: duidelijk (3:1) op licht en donker ---------- */
.dark,.hero,.footer,.cta-midden,.footer-cta,[class*="hero-foto"]{--focus:#f6b393}
:is(a,button,summary,[tabindex]):focus-visible{outline:3px solid var(--focus)!important;outline-offset:3px!important}
.choice label:has(input:focus-visible){outline:3px solid var(--focus)!important;outline-offset:2px}
input[type=file]:focus-visible,input[type=range]:focus-visible,input[type=checkbox]:focus-visible,input[type=radio]:focus-visible{outline:3px solid var(--focus);outline-offset:2px}

/* ---------- Kleine details ---------- */
.crumbs{font-size:.84rem}
.faq details{border-color:var(--line)}
.sticky-cta .btn{border-radius:999px}

@media(prefers-reduced-motion:reduce){
  .header,.burger,.footer a{transition:none}
}
"""

JS = ""
