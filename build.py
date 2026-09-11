"""Build docs/ for GitHub Pages: the original scheme at the root and each alternative in its own folder."""
import os, shutil
SRC = open('index.html').read()
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="Hand-painted wallpaper, made to order in Notting Hill.">\n')

PAPERED_CSS = """
/* papered: the prints are the wall, the content are sheets laid on it, and the wall is alive */
.paper-bg{position:fixed;inset:0;z-index:-1;background:var(--chalk)}
.paper-bg i{position:absolute;inset:0;background-repeat:repeat;background-size:min(46vw,560px) auto;opacity:0;transition:opacity 1.4s ease}
.paper-bg i.on{opacity:1}
.paper-bg::after{content:"";position:absolute;inset:0;background:rgba(246,242,234,.24)}
.critters{position:fixed;inset:0;z-index:-1;width:100%;height:100%;pointer-events:none}
.hero .wrap,.section .wrap,.footer .wrap{max-width:1000px;background:var(--plaster);padding:clamp(28px,4.5vw,72px);box-shadow:0 40px 80px -50px rgba(30,29,24,.7),0 0 0 1px rgba(30,29,24,.06)}
.hero{padding-top:calc(96px + 2vw);padding-bottom:clamp(120px,14vw,200px)}
.section{padding-top:clamp(100px,12vw,180px);padding-bottom:clamp(100px,12vw,180px)}
.footer{padding-top:clamp(100px,12vw,180px)}
.atelier,.mixer{background:transparent}
.atelier .wrap{background:var(--atelier-bg)}
.mixer .wrap{background:var(--plaster-deep)}
.footer{border-top:0}
.ticker{box-shadow:0 20px 40px -30px rgba(30,29,24,.6)}
.vert{display:none}
.nav .mark,.nav ul a{text-shadow:0 0 12px var(--plaster),0 0 24px var(--plaster)}
.nav.scrolled .mark,.nav.scrolled ul a{text-shadow:none}
.nav .btn{background:var(--plaster)}
.paper-name{position:fixed;right:16px;bottom:16px;z-index:60;background:var(--chalk);border:1px solid var(--line-strong);padding:11px 14px;font:500 10.5px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--ink-soft);display:flex;gap:10px;align-items:center;box-shadow:0 12px 30px -18px rgba(0,0,0,.6)}
.paper-name b{font-family:var(--ital);font-style:italic;font-weight:400;text-transform:none;letter-spacing:0;font-size:14px;color:var(--ink)}
@media (max-width:560px){.paper-name{display:none}}
@media (prefers-reduced-motion:reduce){.paper-bg i{transition:none}}
"""
PAPERED_HTML = """<div class="paper-bg" aria-hidden="true">
  <i data-paper="apricot" class="on" style="background-image:url(img/bg-strawberry-apricot.jpg)"></i>
  <i data-paper="ink" style="background-image:url(img/bg-strawberry-ink.jpg)"></i>
  <i data-paper="ginkgo" style="background-image:url(img/bg-ginkgo.jpg)"></i>
</div>
<canvas class="critters" id="critters" aria-hidden="true"></canvas>
<div class="paper-name" aria-live="polite"><span>On the wall</span><b id="paper-name">Portobello Strawberry, apricot</b></div>
"""
PAPERED_JS = """
/* ---------- the wall is alive: block-print countryside ---------- */
(function(){
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var cv = document.getElementById('critters'); if (!cv) return;
  var c = cv.getContext('2d'), dpr = Math.min(window.devicePixelRatio || 1, 2), W = 0, H = 0;
  function resize(){ W = window.innerWidth; H = window.innerHeight; cv.width = Math.round(W*dpr); cv.height = Math.round(H*dpr); }
  window.addEventListener('resize', resize); resize();
  var inks = { apricot:'#C97C47', ink:'#26251E', ginkgo:'#2F6673' }, ink = inks.apricot;
  window.__paperInk = function(p){ if (inks[p]) ink = inks[p]; };
  var rnd = function(a,b){ return a + Math.random()*(b-a); };
  var S = function(){ return W < 700 ? 0.72 : 1; };
  var ground = function(){ return H - 118; };
  var ents = [];

  /* shapes: local units, facing right, feet on y=0 */
  function leg(x,y,a,len,foot){ c.save(); c.translate(x,y); c.rotate(a); c.beginPath(); c.moveTo(0,0); c.lineTo(0,len); if (foot){ c.lineTo(5,len); c.moveTo(0,len); c.lineTo(-4,len); } c.stroke(); c.restore(); }
  function pheasant(t){
    var bob = Math.sin(t*6)*1.5, a = Math.sin(t*6)*0.45;
    c.beginPath(); c.moveTo(-16,-28); c.quadraticCurveTo(-50,-40,-80,-46); c.lineTo(-78,-40); c.quadraticCurveTo(-46,-30,-16,-18); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-16,-24); c.quadraticCurveTo(-44,-30,-66,-31); c.lineTo(-64,-26); c.quadraticCurveTo(-40,-24,-16,-17); c.closePath(); c.fill();
    c.save(); c.translate(0,-22); c.rotate(-0.12); c.beginPath(); c.ellipse(0,0,26,13,0,0,Math.PI*2); c.fill(); c.restore();
    c.beginPath(); c.moveTo(14,-30); c.quadraticCurveTo(24,-34,26,-44+bob); c.lineTo(32,-42+bob); c.quadraticCurveTo(28,-30,20,-20); c.closePath(); c.fill();
    c.beginPath(); c.ellipse(29,-47+bob,7.5,5.5,-0.2,0,Math.PI*2); c.fill();
    c.beginPath(); c.moveTo(35,-48+bob); c.lineTo(43,-46+bob); c.lineTo(35,-44+bob); c.closePath(); c.fill();
    c.lineWidth = 2.2; c.lineCap = 'round'; leg(4,-12,a,12,true); leg(-4,-12,-a,12,true);
  }
  function pheasantFly(t){
    var f = Math.sin(t*10)*12;
    c.beginPath(); c.moveTo(-14,-2); c.quadraticCurveTo(-50,4,-82,14); c.lineTo(-80,8); c.quadraticCurveTo(-48,-2,-14,-8); c.closePath(); c.fill();
    c.beginPath(); c.ellipse(0,-4,26,10,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(28,-9,7,5,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.moveTo(34,-10); c.lineTo(42,-8); c.lineTo(34,-6); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-4,-8); c.quadraticCurveTo(4,-30-f,24,-36-f); c.quadraticCurveTo(10,-14,8,-4); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-6,-8); c.quadraticCurveTo(-12,-26-f*0.8,-26,-30-f*0.8); c.quadraticCurveTo(-8,-14,4,-4); c.closePath(); c.fill();
  }
  function labrador(t){
    var wag = Math.sin(t*10)*5, a = Math.sin(t*7)*0.5;
    c.lineWidth = 5; c.lineCap = 'round'; c.beginPath(); c.moveTo(-34,-36); c.quadraticCurveTo(-52,-40,-60,-54+wag); c.stroke();
    c.beginPath(); c.ellipse(0,-32,38,15,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(30,-40,13,12,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(46,-51,13,10,0.15,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(60,-48,8,5.5,0.1,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(40,-50,5,9,0.3,0,Math.PI*2); c.fill();
    c.lineWidth = 6; leg(-24,-26,a,26); leg(-16,-26,-a,26); leg(20,-28,-a,28); leg(28,-28,a,28);
  }
  function hare(){
    c.beginPath(); c.ellipse(0,-22,24,14,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(-14,-18,13,10,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(24,-34,9,7,-0.2,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(24,-52,3.2,12,0.15,0,Math.PI*2); c.fill();
    c.beginPath(); c.ellipse(30,-51,3.2,12,0.45,0,Math.PI*2); c.fill();
    c.beginPath(); c.arc(-27,-24,3.5,0,Math.PI*2); c.fill();
    c.lineWidth = 5; c.lineCap = 'round';
    c.beginPath(); c.moveTo(-16,-12); c.lineTo(-30,-3); c.stroke();
    c.beginPath(); c.moveTo(14,-14); c.lineTo(20,-3); c.stroke();
  }
  function hedgehog(t){
    var b = Math.sin(t*8)*0.6, n = 16;
    c.beginPath(); c.moveTo(-18,0);
    for (var i=0;i<=n;i++){ var an = Math.PI + (i/n)*Math.PI, r = (i%2 ? 21 : 16); c.lineTo(Math.cos(an)*r, -2 + Math.sin(an)*r); }
    c.lineTo(18,0); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(14,-9); c.quadraticCurveTo(24,-9,29,-1+b); c.lineTo(14,0); c.closePath(); c.fill();
    c.lineWidth = 2.5; c.lineCap = 'round'; c.beginPath(); c.moveTo(-8,0); c.lineTo(-10,3); c.moveTo(8,0); c.lineTo(10,3); c.stroke();
  }
  function swallow(t){
    var f = Math.sin(t*9)*9;
    c.beginPath(); c.ellipse(0,0,4,10,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.moveTo(0,-3); c.quadraticCurveTo(14,-16,32,-10-f); c.quadraticCurveTo(14,-6,3,3); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(0,-3); c.quadraticCurveTo(-14,-16,-32,-10-f); c.quadraticCurveTo(-14,-6,-3,3); c.closePath(); c.fill();
    c.beginPath(); c.moveTo(-3,4); c.lineTo(-9,18); c.lineTo(-5,8); c.lineTo(0,10); c.lineTo(5,8); c.lineTo(9,18); c.lineTo(3,4); c.closePath(); c.fill();
  }
  function oakleaf(){
    c.beginPath(); c.moveTo(0,0);
    for (var i=1;i<=4;i++){ var y=-i*7; c.quadraticCurveTo(-13,y+4,-3,y-2); }
    c.quadraticCurveTo(-5,-34,0,-37);
    for (i=4;i>=1;i--){ y=-i*7; c.quadraticCurveTo(13,y-4,3,y+2); }
    c.closePath(); c.fill(); c.lineWidth = 1.5; c.beginPath(); c.moveTo(0,0); c.lineTo(0,8); c.stroke();
  }
  function acorn(){
    c.beginPath(); c.ellipse(0,4,6,8,0,0,Math.PI*2); c.fill();
    c.beginPath(); c.arc(0,-1,8,Math.PI,0); c.quadraticCurveTo(0,4,-8,-1); c.closePath(); c.fill();
    c.lineWidth = 2; c.beginPath(); c.moveTo(0,-8); c.lineTo(1,-14); c.stroke();
  }

  /* entities */
  function walker(kind, x, dir){
    var speed = { pheasant:34, labrador:62, hedgehog:12, hare:130 }[kind];
    ents.push({ kind:kind, x:x, dir:dir, speed:speed, t:rnd(0,10) });
  }
  function spawnWalker(){
    var kinds = ['pheasant','pheasant','labrador','hedgehog','hare'], kind = kinds[Math.floor(rnd(0,kinds.length))];
    var dir = Math.random() < 0.5 ? 1 : -1;
    walker(kind, dir > 0 ? -140*S() : W + 140*S(), dir);
  }
  function spawnFlock(){
    var dir = Math.random() < 0.5 ? 1 : -1, n = 3 + Math.floor(rnd(0,3)), base = rnd(H*0.12, H*0.4);
    for (var i=0;i<n;i++) ents.push({ kind:'swallow', x:(dir>0 ? -60 : W+60) - dir*i*rnd(40,90), dir:dir, speed:rnd(150,190), base: base + rnd(-40,40), phase:rnd(0,6), t:rnd(0,10) });
  }
  function spawnFlight(){
    var dir = Math.random() < 0.5 ? 1 : -1;
    ents.push({ kind:'flight', x: dir>0 ? -160 : W+160, dir:dir, speed:230, base:rnd(H*0.35,H*0.6), t:0, p:0 });
  }
  function spawnLeaf(top){
    ents.push({ kind: Math.random() < 0.8 ? 'leaf' : 'acorn', x:rnd(0,W), y: top ? -50 : rnd(0,H), vy:rnd(16,30), rot:rnd(0,6), spin:rnd(-0.8,0.8), phase:rnd(0,6), t:rnd(0,10) });
  }
  /* opening scene, so the page is alive at rest */
  walker('pheasant', W*0.22, 1); walker('labrador', W*0.82, -1); walker('hedgehog', W*0.55, 1);
  for (var i=0;i<7;i++) spawnLeaf(false);
  var timers = { walker:rnd(6,10), flock:rnd(8,14), flight:rnd(20,30), leaf:2 };

  function draw(e, s){
    c.save(); c.fillStyle = ink; c.strokeStyle = ink; c.globalAlpha = 0.92;
    if (e.kind === 'leaf' || e.kind === 'acorn'){ c.translate(e.x, e.y); c.rotate(e.rot); c.scale(s*0.9, s*0.9); (e.kind === 'leaf' ? oakleaf : acorn)(); }
    else if (e.kind === 'swallow'){ c.translate(e.x, e.y); c.rotate(e.ang); c.scale(s*0.8, s*0.8); swallow(e.t); }
    else if (e.kind === 'flight'){ c.translate(e.x, e.y); c.scale(e.dir*s, s); pheasantFly(e.t); }
    else { c.translate(e.x, e.y); c.scale(e.dir*s, s); if (e.kind === 'hare'){ c.rotate(e.tilt || 0); } ({pheasant:pheasant, labrador:labrador, hedgehog:hedgehog, hare:hare})[e.kind](e.t); }
    c.restore();
  }
  function step(dt){
    var s = S(), g = ground();
    Object.keys(timers).forEach(function(k){ timers[k] -= dt; });
    if (timers.walker <= 0){ spawnWalker(); timers.walker = rnd(7,13); }
    if (timers.flock <= 0){ spawnFlock(); timers.flock = rnd(16,28); }
    if (timers.flight <= 0){ spawnFlight(); timers.flight = rnd(30,50); }
    if (timers.leaf <= 0){ if (ents.filter(function(e){ return e.kind==='leaf'||e.kind==='acorn'; }).length < 9) spawnLeaf(true); timers.leaf = rnd(1.5,3.5); }
    for (var i = ents.length-1; i >= 0; i--){
      var e = ents[i]; e.t += dt;
      if (e.kind === 'leaf' || e.kind === 'acorn'){ e.y += e.vy*dt*s; e.x += Math.sin(e.t*1.3+e.phase)*26*dt; e.rot += e.spin*dt; if (e.y > H+60) ents.splice(i,1); continue; }
      if (e.kind === 'swallow'){ e.x += e.dir*e.speed*dt; var k = 0.012; e.y = e.base + Math.sin(e.x*k+e.phase)*38; var dy = Math.cos(e.x*k+e.phase)*38*k*e.dir; e.ang = Math.atan2(dy*e.speed, e.dir*e.speed) + Math.PI/2; }
      else if (e.kind === 'flight'){ e.x += e.dir*e.speed*dt; e.p = e.dir>0 ? e.x/W : 1 - e.x/W; e.y = e.base - Math.sin(Math.max(0,Math.min(1,e.p))*Math.PI)*90; }
      else if (e.kind === 'hare'){ e.x += e.dir*e.speed*dt; var ph = e.t*5; e.y = g - Math.abs(Math.sin(ph))*44*s; e.tilt = -Math.cos(ph)*0.28*Math.sign(Math.sin(ph)||1); }
      else { e.x += e.dir*e.speed*dt; e.y = g; }
      if (e.x < -220*s || e.x > W + 220*s) ents.splice(i,1);
    }
  }
  function render(){
    c.setTransform(dpr,0,0,dpr,0,0); c.clearRect(0,0,W,H);
    var s = S();
    ents.forEach(function(e){ draw(e, s); });
  }
  var last = performance.now();
  function frame(now){ var dt = Math.min(0.05, (now-last)/1000); last = now; step(dt); render(); requestAnimationFrame(frame); }
  step(0); render();
  if (!reduced) requestAnimationFrame(frame);
})();

(function(){
  var layers = {}, names = {apricot:'Portobello Strawberry, apricot', ink:'Portobello Strawberry, ink', ginkgo:'Westbourne Ginkgo, teal'};
  document.querySelectorAll('.paper-bg i').forEach(function(i){ layers[i.dataset.paper] = i; });
  var secs = Array.prototype.slice.call(document.querySelectorAll('[data-paper]')), current = 'apricot', label = document.getElementById('paper-name');
  function setPaper(p){ if (p === current || !layers[p]) return; current = p; Object.keys(layers).forEach(function(k){ layers[k].classList.toggle('on', k === p); }); label.textContent = names[p]; if (window.__paperInk) window.__paperInk(p); }
  var ticking = false;
  function pick(){
    ticking = false;
    var mid = window.innerHeight * 0.5, best = null;
    for (var i = 0; i < secs.length; i++){ var r = secs[i].getBoundingClientRect(); if (r.top <= mid && r.bottom >= mid) { best = secs[i]; break; } }
    if (!best) best = (secs[0].getBoundingClientRect().top > mid) ? secs[0] : secs[secs.length - 1];
    setPaper(best.dataset.paper);
  }
  window.addEventListener('scroll', function(){ if (!ticking) { ticking = true; requestAnimationFrame(pick); } }, {passive:true});
  pick();
})();
"""
def papered(s):
    s = s.replace('<section class="hero">', '<section class="hero" data-paper="apricot">')
    s = s.replace('<section class="section" id="papers">', '<section class="section" id="papers" data-paper="ink">')
    s = s.replace('<section class="section atelier" id="atelier">', '<section class="section atelier" id="atelier" data-paper="ginkgo">')
    s = s.replace('<section class="section mixer" id="colourway">', '<section class="section mixer" id="colourway" data-paper="apricot">')
    s = s.replace('<section class="section commissions" id="commissions">', '<section class="section commissions" id="commissions" data-paper="ginkgo">')
    s = s.replace('<footer class="footer" id="enquire">', '<footer class="footer" id="enquire" data-paper="ink">')
    s = s.replace('<div class="grain" aria-hidden="true"></div>', '<div class="grain" aria-hidden="true"></div>\n' + PAPERED_HTML, 1)
    s = s.replace('</script>', PAPERED_JS + '</script>', 1)
    return s

SCHEMES = [
 dict(key='', name='Plaster', css=''),
 dict(key='papered', name='Papered', css=PAPERED_CSS, transform=papered),
 dict(key='ink', name='Ink', css=""":root{--plaster:#1B1A16;--plaster-deep:#131210;--chalk:#26241F;--ink:#F1EBDD;--ink-soft:#BDB5A3;--ink-faint:#8A8476;
  --ochre:#D4AE5A;--ochre-deep:#B8923F;--ginkgo:#8FB0CC;--grass:#8A7248;--line:rgba(241,235,221,.16);--line-strong:rgba(241,235,221,.4);
  --nav-bg:rgba(27,26,22,.86);--grain-blend:screen;
  --atelier-bg:#EAE3D4;--atelier-fg:#1E1D18;--atelier-fg-soft:#55524A;--atelier-fg-faint:#8B877C;--atelier-line:rgba(30,29,24,.18)}"""),
 dict(key='duckegg', name='Duck egg', css=""":root{--plaster:#D8E3E2;--plaster-deep:#C7D7D5;--chalk:#F3F6F3;--ink:#1F2A2E;--ink-soft:#4B5A5F;--ink-faint:#7C8A8E;
  --ochre:#DE9F62;--ochre-deep:#C2804A;--ginkgo:#5E93A8;--grass:#DE9F62;--line:rgba(31,42,46,.18);--line-strong:rgba(31,42,46,.45);
  --nav-bg:rgba(216,227,226,.86)}"""),
 dict(key='grasscloth', name='Grasscloth', css=""":root{--plaster:#C8B38C;--plaster-deep:#B9A27A;--chalk:#F1E8D6;--ink:#2B2A1F;--ink-soft:#5A553F;--ink-faint:#7E7659;
  --ochre:#3F7F8E;--ochre-deep:#2F6673;--ginkgo:#3F7F8E;--grass:#C8B38C;--line:rgba(43,42,31,.22);--line-strong:rgba(43,42,31,.5);
  --nav-bg:rgba(200,179,140,.88)}"""),
]
BAR_CSS = """
.scheme-bar{position:fixed;left:16px;bottom:16px;z-index:60;background:var(--chalk);color:var(--ink);border:1px solid var(--line-strong);padding:11px 14px;font:500 10.5px/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;display:flex;gap:14px;align-items:center;box-shadow:0 12px 30px -18px rgba(0,0,0,.6)}
.scheme-bar span{color:var(--ink-faint)}
.scheme-bar a{text-decoration:none;color:var(--ink-soft);padding-bottom:2px;border-bottom:1px solid transparent}
.scheme-bar a:hover{color:var(--ink)}
.scheme-bar a[aria-current]{color:var(--ink);border-color:var(--ochre)}
@media (max-width:560px){.scheme-bar{left:8px;right:8px;bottom:8px;justify-content:center;flex-wrap:wrap;gap:10px}}
"""
def bar(current):
    up = '../' if current else ''
    links = []
    for sc in SCHEMES:
        href = up + (sc['key'] + '/' if sc['key'] else '')
        cur = ' aria-current="page"' if sc['key'] == current else ''
        links.append(f'<a href="{href}"{cur}>{sc["name"]}</a>')
    return '<div class="scheme-bar"><span>Colour scheme</span>' + ''.join(links) + '</div>\n'
shutil.rmtree('docs', ignore_errors=True); os.makedirs('docs')
shutil.copytree('img', 'docs/img')
for sc in SCHEMES:
    key = sc['key']
    s = SRC
    i = s.index('</style>')
    s = s[:i] + sc['css'] + BAR_CSS + s[i:]
    if 'transform' in sc: s = sc['transform'](s)
    if key:
        s = s.replace('src="img/', 'src="../img/').replace('url(img/', 'url(../img/')
    i = s.index('</style>') + len('</style>')
    body = s[i:].replace('<div class="grain" aria-hidden="true"></div>', '<div class="grain" aria-hidden="true"></div>\n' + bar(key), 1)
    out = HEAD + s[:i] + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n'
    d = os.path.join('docs', key) if key else 'docs'
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(out)
    print('built', d)
