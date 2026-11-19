#!/usr/bin/env python3
"""Hybrid homepage mockup: original dark/green site + the 'design document' type, readout and game list.
Writes home-v3.html only; the live site is untouched.  Run: python3 _src/build_v3.py
"""
import importlib.util, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('base', os.path.join(HERE, 'build.py'))
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
C, S, P, e, img = b.C, b.S, b.P, b.e, b.img

READOUT = [
    ('down', '−53%', 'churn at the late-game trophy wall', 'Pocket Champs', 'pocketchamps'),
    ('up', '+40%', 'IAP ARPDAU, late-game players', 'Pocket Champs', 'pocketchamps'),
    ('up', '3×', 'player spend after shop redesign', 'Chicken Life', 'chickenlife'),
    ('', 'Top 300', 'Roblox by concurrent players', 'Train Sim World: Tycoon', 'trainsimworldtycoon'),
    ('', '1.6M', 'downloads of a solo-built mod', 'Skyrim: Undeath', 'undeath'),
]
ARROW = {'up': '▲', 'down': '▼', '': '■'}

def years(d):
    ys = re.findall(r'\b(?:19|20)\d\d\b', d)
    if 'Present' in d: return f'{ys[0]} – now'
    return ys[0] if len(set(ys)) == 1 else f'{ys[0]}–{ys[-1][2:]}'

def sechead(n, title, note=''):
    return f'<div class="sh"><span class="sh__n">{n}</span><h2 class="sh__t">{e(title)}</h2><span class="sh__note">{e(note)}</span></div>'

def home():
    feat = [P[i] for i in C['groups'][0]['projects']]
    slides = ''.join(f'<div class="reel__slide{" is-on" if n == 0 else ""}" data-slide>{img(p["banner"], "", eager=(n == 0))}</div>' for n, p in enumerate(feat))
    tiles = ''.join(f'''<a class="gt{" is-on" if n == 0 else ""}" href="{p['id']}.html" data-tile="{n}">
  <span class="gt__img">{img(p['cover'], '')}</span>
  <span class="gt__meta"><span class="gt__n">{n+1:02d}</span><span class="gt__yr">{years(p['dates'])}</span></span>
  <span class="gt__title">{e(p['title'])}</span>
  <span class="gt__sub">{e(p['studio'].split(' ×')[0])}</span>
  <span class="gt__bar"></span>
</a>''' for n, p in enumerate(feat))
    readout = ''.join(f'<a class="kpi" href="{pid}.html"><span class="kpi__v"><i class="{k}">{ARROW[k]}</i>{e(v)}</span><span class="kpi__l">{e(l)}</span><span class="kpi__s">{e(src)}</span></a>'
                      for k, v, l, src, pid in READOUT)
    pillars = ''.join(f'''<article class="pil reveal"><span class="pil__n">0{i+1}</span><h3 class="pil__t">{e(x['title'])}</h3><p>{e(x['text'])}</p>
<ul class="gl">{''.join(f'<li><a href="{pid}.html">{e(P[pid]["title"])} <span>→</span></a></li>' for pid in x['projects'])}</ul></article>''' for i, x in enumerate(C['pillars']))
    # work: featured rows + worlds cards (reuse original components)
    g0, g1 = C['groups'][0], C['groups'][1]
    feat_rows = ''.join(b.feature_row(p, i) for i, p in enumerate(feat))
    worlds = '<div class="grid grid--3">' + ''.join(b.card(P[i]) for i in g1['projects']) + '</div>'
    exp = ''.join(f'''<li class="tl__item reveal"><span class="tl__when">{e(x['when'])}</span><div class="tl__body"><h3 class="tl__org">{e(x['org'])} <span>{e(x['role'])}</span></h3><p>{e(x['text'])}</p>
{('<ul class="chips">' + ''.join(f'<li><a href="{pid}.html">{e(P[pid]["title"])}</a></li>' for pid in x.get('projects', [])) + '</ul>') if x.get('projects') else ''}</div></li>''' for x in C['experience'])
    a = C['about']
    body = f'''<div class="testbar">Layout test (hybrid) · not linked from the live site · <a href="index.html">current homepage</a> · <a href="home-v2.html">document-style test</a></div>
{b.nav(True).replace('href="index.html" aria-label', 'href="home-v3.html" aria-label')}
<main id="main">
<section class="hero hero--v3">
  <div class="reel" data-reel3 aria-hidden="true">{slides}</div>
  <div class="hero__shade"></div>
  <div class="wrap hero__in">
    <p class="hero__role">{e(S['role'])}</p>
    <h1 class="hero__name">{e(S['name'])}</h1>
    <p class="hero__focus">{' <span aria-hidden="true">/</span> '.join(f'<span>{e(f)}</span>' for f in S['focus'])}</p>
    <p class="hero__pitch">{e(S['pitch'])}</p>
    <a class="hero__now" href="{e(S['now']['href'])}"><span class="hero__dot"></span>{e(S['now']['text'])} →</a>
    <div class="btns"><a class="btn" href="#work">View my work</a><a class="btn btn--ghost" href="{e(S['cv'])}" target="_blank" rel="noopener">Download CV</a><a class="btn btn--ghost" href="{e(S['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a></div>
  </div>
  <div class="wrap games">{tiles}</div>
</section>

<section class="sec sec--v3"><div class="wrap">
  {sechead('00', 'Readout', 'Selected results')}
  <div class="kpis">{readout}</div>
</div></section>

<section class="sec sec--v3" id="expertise"><div class="wrap">
  {sechead('01', 'Systems that keep players playing', 'What I bring')}
  <div class="pils">{pillars}</div>
</div></section>

<section class="sec sec--v3" id="work"><div class="wrap">
  {sechead('02', g0['title'], g0['kicker'])}
  <div class="feats">{feat_rows}</div>
  <div class="subsec">{sechead('02.B', g1['title'], g1['kicker'])}{worlds}</div>
</div></section>

<section class="sec sec--v3" id="play"><div class="wrap">
  {sechead('03', 'Prototypes', 'Play')}
  <div class="soon reveal"><span class="soon__badge">Coming soon</span><p>{e(C['play']['intro'])} Small, focused experiments in game feel, progression and economy loops.</p></div>
</div></section>

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
{b.footer()}'''
    h = b.head(f"{S['name']} · {S['role']} (layout test)", S['pitch'], feat[0]['banner']) + body
    extra = ('<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
             '<link rel="stylesheet" href="assets/css/v3.css?v=1">\n<script src="assets/js/v3.js?v=1" defer></script>\n<meta name="robots" content="noindex">\n</head>')
    return h.replace('</head>', extra, 1)

open(os.path.join(b.ROOT, 'home-v3.html'), 'w', encoding='utf-8').write(home())
print('wrote home-v3.html')
