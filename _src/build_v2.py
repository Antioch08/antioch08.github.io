#!/usr/bin/env python3
"""Homepage mockup in the 'design document' style. Writes home-v2.html only; the live site is untouched.
Run: python3 _src/build_v2.py
"""
import json, os, re, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(ROOT, '_src', 'content.json'), encoding='utf-8'))
IMG = json.load(open(os.path.join(ROOT, '_src', 'images.json'), encoding='utf-8'))
S, P = C['site'], {p['id']: p for p in C['projects']}
e = lambda s: html.escape(str(s), quote=True)

# One-line key result per project for the index table (up = positive delta)
KEY = {
    'pocketchamps': ('up', '+40% late-game IAP ARPDAU'),
    'trainsimworldtycoon': ('', 'Top 300 Roblox · 2k+ CCU at launch'),
    'mobile': ('', 'TIGA 2018 · Best Puzzle Game'),
    'chickenlife': ('up', '3× player spend'),
    'clonerumble': ('', 'Soft launch · gacha economy'),
    'multiversity': ('', '4 chapters · 2.5h+ of play'),
    'undeath': ('', '1.6M downloads'),
    'lordbound': ('', '16 quests · 67 characters'),
}
READOUT = [
    ('down', '−53%', 'churn at the late-game trophy wall', 'Pocket Champs', 'pocketchamps'),
    ('up', '+40%', 'IAP ARPDAU, late-game players', 'Pocket Champs', 'pocketchamps'),
    ('up', '3×', 'player spend after shop redesign', 'Chicken Life', 'chickenlife'),
    ('', 'Top 300', 'Roblox by concurrent players', 'Train Sim World: Tycoon', 'trainsimworldtycoon'),
    ('', '1.6M', 'downloads of a solo-built mod', 'Skyrim: Undeath', 'undeath'),
]
ARROW = {'up': '▲', 'down': '▼', '': '■'}

def years(d):
    ys = re.findall(r'(19|20)\d\d', d)
    ys = re.findall(r'\b(?:19|20)\d\d\b', d)
    if 'Present' in d: return f'{ys[0]}–'
    return ys[0] if len(set(ys)) == 1 else f'{ys[0]}–{ys[-1][2:]}'

def img(name, alt=''):
    w, h = IMG.get(name, [1600, 900])
    return f'<img src="assets/img/{name}.webp" width="{w}" height="{h}" alt="{e(alt)}" loading="lazy" decoding="async">'

def rows(ids, start):
    out = ''
    for n, pid in enumerate(ids, start):
        p = P[pid]; k, txt = KEY.get(pid, ('', ''))
        out += f'''<a class="row" href="{pid}.html" data-preview="assets/img/{p['cover']}.webp">
  <span class="c-no mono">{n:02d}</span>
  <span class="c-title">{e(p['title'])}<span class="c-thumb">{img(p['cover'])}</span></span>
  <span class="c-studio">{e(p['studio'].split(' ×')[0])}</span>
  <span class="c-plat">{e(p['platform'].split(' ·')[0].replace(' (iOS & Android)', ''))}</span>
  <span class="c-year mono">{years(p['dates'])}</span>
  <span class="c-key mono"><i class="{k}">{ARROW[k]}</i> {e(txt)}</span>
</a>'''
    return out

def page():
    feat, worlds = C['groups'][0]['projects'], C['groups'][1]['projects']
    strip = ''.join(f'<a href="{pid}.html" class="strip__cell"><span>{img(P[pid]["cover"], P[pid]["title"])}</span><b class="mono">{i:02d} {e(P[pid]["title"])}</b></a>'
                    for i, pid in enumerate(feat, 1))
    readout = ''.join(f'<a class="kpi" href="{pid}.html"><span class="kpi__v mono"><i class="{k}">{ARROW[k]}</i>{e(v)}</span><span class="kpi__l">{e(l)}</span><span class="kpi__s mono">{e(src)}</span></a>'
                      for k, v, l, src, pid in READOUT)
    approach = ''.join(f'<div class="prin"><span class="mono prin__n">2.{i}</span><h3>{e(x["title"])}</h3><p>{e(x["text"])}</p></div>'
                       for i, x in enumerate(C['pillars'], 1))
    exp = ''.join(f'<tr><td class="mono">{e(x["when"] or "—")}</td><td><b>{e(x["org"])}</b></td><td>{e(x["role"])}</td><td class="muted">{e(x["text"])}</td></tr>'
                  for x in C['experience'])
    a = C['about']
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(S['name'])} · {e(S['role'])} (layout test)</title>
<meta name="robots" content="noindex">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/v2.css?v=1">
<script src="assets/js/v2.js?v=1" defer></script>
</head>
<body>
<div class="testbar mono">Layout test · not linked from the live site · <a href="index.html">compare with current homepage →</a></div>
<header class="top">
  <div class="wrap top__in">
    <a class="mono brand" href="home-v2.html">DJL / Game design</a>
    <nav class="mono">
      <a href="#work"><span>01</span> Work</a><a href="#approach"><span>02</span> Approach</a><a href="#experience"><span>03</span> Experience</a><a href="#about"><span>04</span> About</a>
      <a class="cv" href="{e(S['cv'])}" target="_blank" rel="noopener">CV ↗</a>
    </nav>
  </div>
</header>

<main>
<section class="wrap head">
  <div class="head__meta mono"><span>Portfolio</span><span>Rev. 2026</span><span>{e(S['location'])}</span></div>
  <h1 class="name">Daniel J.<br>Lewis</h1>
  <div class="head__grid">
    <p class="lede">Game design leader. I build the <em>metagame</em>, <em>systems</em> and <em>F2P monetisation</em> that keep players coming back, across more than a decade of shipping and running live games.</p>
    <table class="spec mono">
      <tr><th>Now</th><td><a href="pocketchamps.html">Senior Game Designer, Madbox</a></td></tr>
      <tr><th>Focus</th><td>Metagame · Systems · F2P Monetisation</td></tr>
      <tr><th>Record</th><td>10+ years · 13 games</td></tr>
      <tr><th>Platforms</th><td>Mobile · Roblox · Sandbox · PC</td></tr>
      <tr><th>Contact</th><td><a href="mailto:{e(S['email'])}">Email</a> · <a href="{e(S['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a></td></tr>
    </table>
  </div>
</section>

<section class="strip">{strip}</section>

<section class="wrap readout">
  <div class="sechead"><span class="mono">00</span><h2>Readout</h2><span class="mono muted">Selected results</span></div>
  <div class="kpis">{readout}</div>
</section>

<section class="wrap" id="work">
  <div class="sechead"><span class="mono">01</span><h2>Work</h2><span class="mono muted">Hover a row to preview</span></div>
  <div class="thead mono"><span>No.</span><span>Title</span><span>Studio</span><span>Platform</span><span>Year</span><span>Key result</span></div>
  <div class="index">{rows(feat, 1)}</div>
  <p class="subhead mono">1.B — Worlds &amp; narrative</p>
  <div class="index">{rows(worlds, len(feat) + 1)}</div>
  <p class="subhead mono">1.C — Play</p>
  <div class="note mono">Playable browser prototypes — in production.</div>
</section>

<section class="wrap" id="approach">
  <div class="sechead"><span class="mono">02</span><h2>Approach</h2><span class="mono muted">How I design</span></div>
  <div class="prins">{approach}</div>
</section>

<section class="wrap" id="experience">
  <div class="sechead"><span class="mono">03</span><h2>Experience</h2><span class="mono muted">2010 – now</span></div>
  <table class="exp">{exp}</table>
</section>

<section class="wrap about" id="about">
  <div class="sechead"><span class="mono">04</span><h2>About</h2><span class="mono muted">Barcelona</span></div>
  <div class="about__grid">
    <figure>{img(a['photo'], 'Daniel J Lewis')}<figcaption class="mono">Fig. 1 — Daniel</figcaption></figure>
    <div class="about__txt">{''.join(f'<p>{e(x)}</p>' for x in a['paragraphs'])}</div>
  </div>
</section>
</main>

<footer class="foot">
  <div class="wrap">
    <p class="mono muted">05 — Contact</p>
    <a class="mail" href="mailto:{e(S['email'])}">{e(S['email'])}</a>
    <div class="foot__row mono"><a href="{e(S['linkedin'])}" target="_blank" rel="noopener">LinkedIn ↗</a><a href="{e(S['cv'])}" target="_blank" rel="noopener">CV ↗</a><span>© {e(S['name'])}</span></div>
  </div>
</footer>
<div class="preview" aria-hidden="true"><img alt=""></div>
</body>
</html>
'''

open(os.path.join(ROOT, 'home-v2.html'), 'w', encoding='utf-8').write(page())
print('wrote home-v2.html')
