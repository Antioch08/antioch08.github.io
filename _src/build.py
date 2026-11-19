#!/usr/bin/env python3
"""Static site generator for the portfolio.

Edit content.json, then run:  python3 _src/build.py
Pages are written to the repo root (index.html, <project-id>.html).
Gallery images are listed in gallery.json (generated from the old Weebly site; edit freely).
"""
import json, os, html, re
from string import Template

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_src')
C = json.load(open(os.path.join(SRC, 'content.json'), encoding='utf-8'))
G = json.load(open(os.path.join(SRC, 'gallery.json'), encoding='utf-8'))   # {page: {"images": [...], "videos": [...]}}
IMG = json.load(open(os.path.join(SRC, 'images.json'), encoding='utf-8'))  # {name: [w, h]}
S = C['site']
P = {p['id']: p for p in C['projects']}
CAT = C['categories']
e = lambda s: html.escape(str(s), quote=True)
VER = '12'

def img(name, alt='', cls='', sizes='', eager=False, attrs=''):
    w, h = IMG.get(name, [1600, 900])
    load = 'eager' if eager else 'lazy'
    c = f' class="{cls}"' if cls else ''
    return f'<img src="assets/img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}" loading="{load}" decoding="async"{c}{attrs}>'

def head(title, desc, image):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<script>document.documentElement.classList.add('js')</script>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="assets/img/{image}.webp">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0b0d12">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css?v={VER}">
<script src="assets/js/main.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
'''

def nav(home=False):
    pre = '' if home else 'index.html'
    return f'''<header class="nav" data-nav>
  <div class="wrap nav__in">
    <a class="logo" href="index.html" aria-label="{e(S['name'])}, home"><span class="logo__mark">DJL</span><span class="logo__name">{e(S['name'])}</span></a>
    <button class="nav__toggle" aria-expanded="false" aria-controls="nav-links" data-nav-toggle><span></span><span></span><span class="sr">Menu</span></button>
    <nav id="nav-links" class="nav__links">
      <a href="{pre}#work">Work</a>
      <a href="{pre}#expertise">Expertise</a>
      <a href="{pre}#experience">Experience</a>
{'' if C['play'].get('hidden') else f'      <a href="{pre}#play">Play</a>\n'}      <a href="{pre}#about">About</a>
      <a class="btn btn--sm" href="{e(S['cv'])}" target="_blank" rel="noopener">CV</a>
    </nav>
  </div>
</header>
'''

def footer():
    return f'''<footer class="foot" id="contact">
  <div class="wrap foot__in">
    <div>
      <h2 class="foot__title">Let's make something players love.</h2>
      <div class="btns">
        <a class="btn" href="mailto:{e(S['email'])}">Email me</a>
        <a class="btn btn--ghost" href="{e(S['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a>
        <a class="btn btn--ghost" href="{e(S['cv'])}" target="_blank" rel="noopener">Download CV</a>
      </div>
    </div>
    <p class="foot__small">© {e(S['name'])} · {e(S['location'])}</p>
  </div>
</footer>
<div class="lb" data-lightbox hidden>
  <button class="lb__close" data-lb-close aria-label="Close">×</button>
  <button class="lb__nav lb__prev" data-lb-prev aria-label="Previous image">‹</button>
  <figure class="lb__fig"><img alt="" data-lb-img><figcaption data-lb-count></figcaption></figure>
  <button class="lb__nav lb__next" data-lb-next aria-label="Next image">›</button>
</div>
</body>
</html>
'''

def tags(p, limit=None):
    t = p['tags'][:limit] if limit else p['tags']
    return '<ul class="tags">' + ''.join(f'<li>{e(CAT[x])}</li>' for x in t) + '</ul>'

def stats_html(stats, cls='stats'):
    if not stats: return ''
    return f'<dl class="{cls}">' + ''.join(
        f'<div class="stat"><dt>{e(s["value"])}</dt><dd>{e(s["label"])}</dd></div>' for s in stats) + '</dl>'

def gallery(pages, label):
    imgs, seen = [], set()
    for pg in pages:
        for n in G.get(pg, {}).get('images', []):
            if n not in seen and n in IMG:
                seen.add(n); imgs.append(n)
    if not imgs: return ''
    slides = ''.join(
        f'<li class="car__slide{" car__slide--tall" if IMG[n][1] / IMG[n][0] > 1.25 else ""}"><button class="car__btn" data-lb-src="assets/img/{n}.webp" aria-label="Open image {i+1} of {len(imgs)} full screen">'
        f'{img(n, f"{label} screenshot {i+1}")}</button></li>' for i, n in enumerate(imgs))
    return f'''<div class="car" data-carousel>
  <div class="car__bar"><span class="car__count" data-car-count>1 / {len(imgs)}</span>
    <div class="car__ctrl"><button class="car__arrow" data-car-prev aria-label="Previous">‹</button><button class="car__arrow" data-car-next aria-label="Next">›</button></div></div>
  <ul class="car__track" data-car-track>{slides}</ul>
</div>'''

def videos(pages, title):
    vids = []
    for pg in pages:
        for v in G.get(pg, {}).get('videos', []):
            if v not in vids: vids.append(v)
    if not vids: return ''
    cells = ''.join(f'''<div class="yt" data-yt="{e(v)}"><img src="https://i.ytimg.com/vi/{e(v)}/hqdefault.jpg" alt="" loading="lazy">
<button class="yt__play" aria-label="Play video: {e(title)} {i+1}"><svg viewBox="0 0 68 48" aria-hidden="true"><path d="M66.5 7.7a8.5 8.5 0 0 0-6-6C55.2.3 34 .3 34 .3s-21.2 0-26.5 1.4a8.5 8.5 0 0 0-6 6C.1 13 .1 24 .1 24s0 11 1.4 16.3a8.5 8.5 0 0 0 6 6C12.8 47.7 34 47.7 34 47.7s21.2 0 26.5-1.4a8.5 8.5 0 0 0 6-6C67.9 35 67.9 24 67.9 24s0-11-1.4-16.3z"/><path d="M45 24 27 14v20" fill="#fff"/></svg></button></div>'''
                    for i, v in enumerate(vids))
    return f'<div class="vids vids--{min(len(vids),2)}">{cells}</div>'

def link_btns(p):
    out = ''.join(f'<a class="btn" href="{e(l["href"])}" target="_blank" rel="noopener">{e(l["label"])} <span aria-hidden="true">↗</span></a>' for l in p.get('links', []))
    return f'<div class="btns">{out}</div>' if out else ''

# ---------------------------------------------------------------- project page
def project_page(p, nxt):
    facts = [('Studio', p['studio']), ('Platform', p['platform']), ('Role', p['role']), ('When', p['dates'])]
    press = ''
    if p.get('press'):
        press = '<div class="press"><span>As seen on</span>' + ''.join(
            f'<a href="{e(x["href"])}" target="_blank" rel="noopener">{e(x["label"])}</a>' for x in p['press']) + '</div>'
    if p.get('awards'):
        press += '<div class="press"><span>Awards</span>' + ''.join(f'<span class="award">🏆 {e(a)}</span>' for a in p['awards']) + '</div>'
    sections = ''
    for i, s in enumerate(p.get('sections', [])):
        sid = s['title'].lower().replace(' & ', '-').replace(' ', '-')
        steps = ''
        if s.get('steps'):
            steps = f'<h3 class="h3">{e(s["steps_title"])}</h3><ol class="steps">' + ''.join(f'<li>{e(x)}</li>' for x in s['steps']) + '</ol>'
        sections += f'''<section class="sec reveal" id="{sid}">
  <div class="wrap">
    <div class="sh"><h2 class="sh__t">{e(s['title'])}</h2></div>
    <div class="cols"><div class="prose">{''.join(f'<p>{e(x)}</p>' for x in s['paragraphs'])}</div><div>{steps}</div></div>
    {gallery(s['pages'], p['title'] + ' ' + s['title'])}
  </div>
</section>'''
    docs = ''
    if p.get('docs'):
        docs = '<section class="sec reveal"><div class="wrap"><div class="sh"><h2 class="sh__t">Design documents</h2></div><div class="docs">' + ''.join(
            f'<a class="doc" href="{e(d["href"])}" target="_blank" rel="noopener"><span class="doc__ico">PDF</span><span><strong>{e(d["label"])}</strong><small>{e(d["text"])}</small></span></a>'
            for d in p['docs']) + '</div></div></section>'
    vids = videos(p['pages'], p['title'])
    gal = gallery(p['pages'], p['title'])
    note = f'<p class="note">{e(p["note"])}</p>' if p.get('note') else ''
    body = f'''{nav()}
<main id="main">
<section class="phero">
  <div class="phero__bg">{img(p['banner'], '', eager=True)}</div>
  <div class="wrap phero__in">
    <a class="back" href="index.html#work">← All work</a>
    <h1 class="phero__title">{e(p['title'])}</h1>
    <p class="phero__tag">{e(p['tagline'])}</p>
    <dl class="facts">{''.join(f'<div><dt>{k}</dt><dd>{e(v)}</dd></div>' for k, v in facts)}</dl>
    {link_btns(p)}
  </div>
</section>
{f'<section class="sec sec--tight"><div class="wrap">{stats_html(p["stats"], "stats stats--proj")}{press}</div></section>' if (p['stats'] or press) else ''}
<section class="sec reveal"><div class="wrap cols cols--main">
  <div class="prose">{''.join(f'<p>{e(x)}</p>' for x in p['summary'])}{note}</div>
  <aside class="card did"><h2 class="h3">What I did</h2><ul class="ticks">{''.join(f'<li>{e(x)}</li>' for x in p['did'])}</ul>{tags(p)}</aside>
</div></section>
{f'<section class="sec reveal"><div class="wrap"><div class="sh"><h2 class="sh__t">Video</h2></div>{vids}</div></section>' if vids else ''}
{f'<section class="sec reveal"><div class="wrap"><div class="sh"><h2 class="sh__t">Screens &amp; key art</h2></div>{gal}</div></section>' if gal else ''}
{sections}
{docs}
<section class="sec"><div class="wrap">
  <a class="next" href="{nxt['id']}.html">
    <span class="next__img">{img(nxt['cover'], '')}</span>
    <span class="next__txt"><span class="next__title">Next: {e(nxt['title'])} →</span></span>
  </a>
</div></section>
</main>
{footer()}'''
    return head(f"{p['title']} · {S['name']}", p['tagline'], p['cover']) + body

# ---------------------------------------------------------------- home page
READOUT = [
    ('down', '−53%', 'reduced endgame player churn', 'Pocket Champs', 'pocketchamps'),
    ('up', '+40%', 'IAP ARPDAU, late-game players', 'Pocket Champs', 'pocketchamps'),
    ('up', '3×', 'player spend after shop redesign', 'Chicken Life', 'chickenlife'),
    ('', 'Top 300', 'Roblox chart games by CCU', 'Train Sim World: Tycoon', 'trainsimworldtycoon'),
    ('', '1.6M', 'downloads of a solo-built mod', 'Skyrim: Undeath', 'undeath'),
]
ARROW = {'up': '▲', 'down': '▼', '': '■'}

def years(d):
    ys = re.findall(r'\b(?:19|20)\d\d\b', d)
    if 'Present' in d: return f'{ys[0]} – now'
    return ys[0] if len(set(ys)) == 1 else f'{ys[0]}–{ys[-1][2:]}'

def sechead(n, title, note=''):
    return f'<div class="sh"><h2 class="sh__t">{e(title)}</h2></div>'

def feature_row(p, i):
    return f'''<article class="feat reveal{' feat--flip' if i % 2 else ''}">
  <a class="feat__media" href="{p['id']}.html" tabindex="-1" aria-hidden="true">{img(p['cover'], p['title'])}</a>
  <div class="feat__body">
    <h3 class="feat__title"><a href="{p['id']}.html">{e(p['title'])}</a></h3>
    <p class="meta">{e(p['studio'])} · {e(p['platform'])}</p>
    <p class="feat__tag">{e(p['tagline'])}</p>
    {stats_html(p['stats'][:3], 'stats stats--mini')}
    <div class="feat__foot">{tags(p, 3)}<a class="link" href="{p['id']}.html">View case study →</a></div>
  </div>
</article>'''

def card(p):
    st = f'<span class="pcard__stat"><strong>{e(p["stats"][0]["value"])}</strong> {e(p["stats"][0]["label"])}</span>' if p['stats'] else ''
    return f'''<a class="pcard reveal" href="{p['id']}.html">
  <span class="pcard__img">{img(p['cover'], '')}</span>
  <span class="pcard__body"><span class="pcard__title">{e(p['title'])}</span><span class="meta">{e(p['platform'])} · {e(p['dates'])}</span>
  <span class="pcard__tag">{e(p['tagline'])}</span>{st}</span>
</a>'''

def home():
    feat = [P[i] for i in C['groups'][0]['projects']]
    slides = ''.join(f'<div class="reel__slide{" is-on" if n == 0 else ""}" data-slide>{img(p["banner"], "", eager=(n == 0))}</div>' for n, p in enumerate(feat))
    tiles = ''.join(f'''<a class="gt{" is-on" if n == 0 else ""}" href="{p['id']}.html" data-tile="{n}">
  <span class="gt__img">{img(p['cover'], '')}</span>
  <span class="gt__title">{e(p['title'])}</span>
  <span class="gt__sub">{e(p['studio'].split(' ×')[0])} · {years(p['dates'])}</span>
  <span class="gt__bar"></span>
</a>''' for n, p in enumerate(feat))
    readout = ''.join(f'<a class="kpi" href="{pid}.html"><span class="kpi__v"><i class="{k}">{ARROW[k]}</i>{e(v)}</span><span class="kpi__l">{e(l)}</span><span class="kpi__s">{e(src)}</span></a>'
                      for k, v, l, src, pid in READOUT)
    pillars = ''.join(f'''<article class="pil reveal"><h3 class="pil__t">{e(x['title'])}</h3><p>{e(x['text'])}</p>
<ul class="gl">{''.join(f'<li><a href="{pid}.html">{e(P[pid]["title"])} <span>→</span></a></li>' for pid in x['projects'])}</ul></article>''' for i, x in enumerate(C['pillars']))
    # work: featured rows + worlds cards (reuse original components)
    g0, g1 = C['groups'][0], C['groups'][1]
    feat_rows = ''.join(feature_row(p, i) for i, p in enumerate(feat))
    worlds = '<div class="grid grid--3">' + ''.join(card(P[i]) for i in g1['projects']) + '</div>'
    exp = ''.join(f'''<li class="tl__item reveal"><span class="tl__when">{e(x['when'])}</span><div class="tl__body"><h3 class="tl__org">{e(x['org'])} <span>{e(x['role'])}</span></h3><p>{e(x['text'])}</p>
{('<ul class="chips">' + ''.join(f'<li><a href="{pid}.html">{e(P[pid]["title"])}</a></li>' for pid in x.get('projects', [])) + '</ul>') if x.get('projects') else ''}</div></li>''' for x in C['experience'])
    a = C['about']
    body = f'''{nav(True)}
<main id="main">
<section class="hero hero--v3">
  <div class="reel" data-reel3 aria-hidden="true">{slides}</div>
  <div class="hero__shade"></div>
  <div class="wrap hero__in">
    <h1 class="hero__name">{e(S['name'])}</h1>
    <p class="hero__focus">{' <span aria-hidden="true">/</span> '.join(f'<span>{e(f)}</span>' for f in S['focus'])}</p>
    <p class="hero__pitch">{e(S['pitch'])}</p>
    <a class="hero__now" href="{e(S['now']['href'])}"><span class="hero__dot"></span>{e(S['now']['text'])} →</a>
    <div class="btns"><a class="btn" href="#work">View my work</a><a class="btn btn--ghost" href="{e(S['cv'])}" target="_blank" rel="noopener">Download CV</a><a class="btn btn--ghost" href="{e(S['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a></div>
  </div>
  <div class="wrap games">{tiles}</div>
</section>

<section class="sec sec--v3"><div class="wrap">
  {sechead('00', 'Highlights', 'Selected results')}
  <div class="kpis">{readout}</div>
</div></section>

<section class="sec sec--v3" id="expertise"><div class="wrap">
  {sechead('01', 'What I specialise in', 'What I bring')}
  <div class="pils">{pillars}</div>
</div></section>

<section class="sec sec--v3" id="work"><div class="wrap">
  {sechead('02', g0['title'], g0['kicker'])}
  <div class="feats">{feat_rows}</div>
  <div class="subsec">{sechead('02.B', g1['title'], g1['kicker'])}{worlds}</div>
</div></section>

{'' if C['play'].get('hidden') else f'''<section class="sec sec--v3" id="play"><div class="wrap">
  {sechead('03', 'Prototypes', 'Play')}
  <div class="soon reveal"><span class="soon__badge">Coming soon</span><p>{e(C['play']['intro'])} Small, focused experiments in game feel, progression and economy loops.</p></div>
</div></section>'''}

<section class="sec sec--v3" id="experience"><div class="wrap">
  {sechead('04', 'Experience', '2010 – now')}
  <ol class="tl">{exp}</ol>
</div></section>

<section class="sec sec--v3" id="about"><div class="wrap">
  {sechead('05', 'About', S['location'])}
  <div class="about">
    <div class="about__photo reveal">{img(a['photo'], 'Daniel J Lewis')}</div>
    <div class="about__txt reveal"><div class="prose">{''.join(f'<p>{e(x)}</p>' for x in a['paragraphs'])}</div>
      <ul class="ticks ticks--2">{''.join(f'<li>{e(x)}</li>' for x in a['highlights'])}</ul></div>
  </div>
</div></section>
</main>
{footer()}'''
    return head(f"{S['name']} · {S['role']}", f"{S['role']}: {', '.join(S['focus'])}. {S['pitch']}", feat[0]['banner']) + body


def redirect(target):
    return f'<!doctype html><meta charset="utf-8"><title>Redirecting…</title><meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"><a href="{target}">Continue</a>\n'

def main():
    order = [pid for g in C['groups'] for pid in g['projects']]
    open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8').write(home())
    for pid in P:  # hidden projects (not in a group) still get a page, just no homepage link
        nxt = P[order[(order.index(pid) + 1) % len(order)]] if pid in order else P[order[0]]
        open(os.path.join(ROOT, f'{pid}.html'), 'w', encoding='utf-8').write(project_page(P[pid], nxt))
    # keep old Weebly URLs working
    for old, new in {'lordboundquests': 'lordbound.html#quest-design', 'lordboundlevels': 'lordbound.html#world-level-design',
                     'about': 'index.html#about', 'cv': S['cv']}.items():
        open(os.path.join(ROOT, f'{old}.html'), 'w', encoding='utf-8').write(redirect(new))
    print('built', 1 + len(order), 'pages')

if __name__ == '__main__':
    main()
