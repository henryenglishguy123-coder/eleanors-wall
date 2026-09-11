"""Build docs/ for GitHub Pages: the original scheme at the root and each alternative in its own folder."""
import os, shutil
SRC = open('index.html').read()
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="Hand-painted wallpaper, made to order in Notting Hill.">\n')

PAPERED_CSS = """
/* papered: the prints are the wall, the content are sheets laid on it */
.paper-bg{position:fixed;inset:0;z-index:-1;background:var(--chalk)}
.paper-bg i{position:absolute;inset:0;background-repeat:repeat;background-size:min(46vw,560px) auto;opacity:0;transition:opacity 1.4s ease}
.paper-bg i.on{opacity:1}
.paper-bg::after{content:"";position:absolute;inset:0;background:rgba(246,242,234,.22)}
.hero .wrap,.section .wrap,.footer .wrap{background:var(--plaster);padding:clamp(28px,4.5vw,72px);box-shadow:0 40px 80px -50px rgba(30,29,24,.7),0 0 0 1px rgba(30,29,24,.06)}
.hero{padding-top:calc(96px + 2vw)}
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
<div class="paper-name" aria-live="polite"><span>On the wall</span><b id="paper-name">Portobello Strawberry, apricot</b></div>
"""
PAPERED_JS = """
(function(){
  var layers = {}, names = {apricot:'Portobello Strawberry, apricot', ink:'Portobello Strawberry, ink', ginkgo:'Westbourne Ginkgo, teal'};
  document.querySelectorAll('.paper-bg i').forEach(function(i){ layers[i.dataset.paper] = i; });
  var secs = Array.prototype.slice.call(document.querySelectorAll('[data-paper]')), current = 'apricot', label = document.getElementById('paper-name');
  function setPaper(p){ if (p === current || !layers[p]) return; current = p; Object.keys(layers).forEach(function(k){ layers[k].classList.toggle('on', k === p); }); label.textContent = names[p]; }
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
