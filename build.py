"""Build docs/ for GitHub Pages: the original scheme at the root and each alternative in its own folder."""
import os, shutil
SRC = open('index.html').read()
HEAD = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="Hand-painted wallpaper, made to order in Notting Hill.">\n')
SCHEMES = [
 ('', 'Plaster', ''),
 ('ink', 'Ink', """:root{--plaster:#1B1A16;--plaster-deep:#131210;--chalk:#26241F;--ink:#F1EBDD;--ink-soft:#BDB5A3;--ink-faint:#8A8476;
  --ochre:#D4AE5A;--ochre-deep:#B8923F;--ginkgo:#8FB0CC;--grass:#8A7248;--line:rgba(241,235,221,.16);--line-strong:rgba(241,235,221,.4);
  --nav-bg:rgba(27,26,22,.86);--grain-blend:screen;
  --atelier-bg:#EAE3D4;--atelier-fg:#1E1D18;--atelier-fg-soft:#55524A;--atelier-fg-faint:#8B877C;--atelier-line:rgba(30,29,24,.18)}"""),
 ('duckegg', 'Duck egg', """:root{--plaster:#D8E3E2;--plaster-deep:#C7D7D5;--chalk:#F3F6F3;--ink:#1F2A2E;--ink-soft:#4B5A5F;--ink-faint:#7C8A8E;
  --ochre:#DE9F62;--ochre-deep:#C2804A;--ginkgo:#5E93A8;--grass:#DE9F62;--line:rgba(31,42,46,.18);--line-strong:rgba(31,42,46,.45);
  --nav-bg:rgba(216,227,226,.86)}"""),
 ('grasscloth', 'Grasscloth', """:root{--plaster:#C8B38C;--plaster-deep:#B9A27A;--chalk:#F1E8D6;--ink:#2B2A1F;--ink-soft:#5A553F;--ink-faint:#7E7659;
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
    for key, name, _ in SCHEMES:
        href = up + (key + '/' if key else '')
        cur = ' aria-current="page"' if key == current else ''
        links.append(f'<a href="{href}"{cur}>{name}</a>')
    return '<div class="scheme-bar"><span>Colour scheme</span>' + ''.join(links) + '</div>\n'
shutil.rmtree('docs', ignore_errors=True); os.makedirs('docs')
shutil.copytree('img', 'docs/img')
for key, name, css in SCHEMES:
    s = SRC
    i = s.index('</style>')
    s = s[:i] + css + BAR_CSS + s[i:]
    if key:
        s = s.replace('src="img/', 'src="../img/')
    i = s.index('</style>') + len('</style>')
    body = s[i:].replace('<div class="grain" aria-hidden="true"></div>', '<div class="grain" aria-hidden="true"></div>\n' + bar(key), 1)
    out = HEAD + s[:i] + '\n</head>\n<body>\n' + body + '\n</body>\n</html>\n'
    d = os.path.join('docs', key) if key else 'docs'
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(out)
    print('built', d)
