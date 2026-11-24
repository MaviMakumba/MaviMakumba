"""Neon-noir GitHub profile asset generator (animated SVGs)."""
import math
import random
import sys
from pathlib import Path
from xml.sax.saxutils import escape as esc

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

SANS = "'Segoe UI','Inter','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code','SF Mono',Menlo,Consolas,'Courier New',monospace"
JP = "'Yu Gothic','Hiragino Sans','Noto Sans CJK JP','Meiryo',sans-serif"

PINK = "#ff2a6d"
AMBER = "#ff8a3d"
GOLD = "#ffc06b"
CYAN = "#5ef2ff"
VIOLET = "#9d4edd"
INK = "#0a0612"
TEXT = "#f3e9ff"
MUTED = "#b8a6cf"
GREEN = "#3dffa8"

BASE_CSS = f"""
.sans{{font-family:{SANS}}} .mono{{font-family:{MONO}}} .jp{{font-family:{JP}}}
@keyframes blink{{0%,55%{{opacity:1}}56%,100%{{opacity:.15}}}}
@keyframes flicker{{0%,18%,22%,25%,53%,57%,100%{{opacity:1}}20%,24%,55%{{opacity:.25}}}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
@keyframes run{{to{{stroke-dashoffset:-1000}}}}
@keyframes fall{{from{{transform:translateY(-120px)}}to{{transform:translateY(620px)}}}}
@keyframes drift{{0%,100%{{transform:translateX(-40px)}}50%{{transform:translateX(40px)}}}}
@keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY(520px)}}}}
@keyframes fadein{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
"""


def svg(w, h, body, css="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>'
            f'<style>{BASE_CSS}{css}</style>{body}</svg>')


def write(name, content):
    (OUT / name).write_text(content, encoding="utf-8")
    print(f"{name}: {len(content)/1024:.1f} KB")


def glow_filter(fid, std=4):
    return (f'<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="{std}" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')


def rain(rng, n, w, h, color="#a8d8ff", op=(0.15, 0.4)):
    out = []
    for _ in range(n):
        x = rng.uniform(0, w + 120)
        ln = rng.uniform(10, 26)
        dur = rng.uniform(0.55, 1.15)
        delay = -rng.uniform(0, 1.2)
        o = rng.uniform(*op)
        out.append(f'<line x1="{x:.0f}" y1="0" x2="{x-ln*0.22:.1f}" y2="{ln:.0f}" stroke="{color}" '
                   f'stroke-width="1" opacity="{o:.2f}" style="animation:fall {dur:.2f}s linear {delay:.2f}s infinite"/>')
    return f'<g transform="rotate(8 {w/2} {h/2})">{"".join(out)}</g>'


def palm(x, y, s, fill="#06020b", flip=False):
    """Palm silhouette rooted at (x, y), scale s."""
    d = -1 if flip else 1
    tx, ty = x + 26 * s * d, y - 150 * s  # crown
    trunk = (f'M{x-5*s:.1f},{y} Q{x+10*s*d:.1f},{y-80*s:.1f} {tx-3*s:.1f},{ty:.1f} '
             f'L{tx+3*s:.1f},{ty+2*s:.1f} Q{x+16*s*d:.1f},{y-78*s:.1f} {x+6*s:.1f},{y} Z')
    fronds = []
    for ang, ln in [(-160, 78), (-128, 70), (-95, 52), (-60, 70), (-25, 80), (5, 66), (-190, 62)]:
        a = math.radians(ang)
        ex, ey = tx + math.cos(a) * ln * s, ty + math.sin(a) * ln * s + 26 * s
        mx, my = tx + math.cos(a) * ln * s * 0.55, ty + math.sin(a) * ln * s * 0.55 - 14 * s
        nx, ny = -(ey - ty), (ex - tx)
        nl = math.hypot(nx, ny) or 1
        nx, ny = nx / nl * 7 * s, ny / nl * 7 * s
        fronds.append(f'M{tx:.1f},{ty:.1f} Q{mx+nx:.1f},{my+ny:.1f} {ex:.1f},{ey:.1f} '
                      f'Q{mx-nx*0.2:.1f},{my-ny*0.2:.1f} {tx:.1f},{ty:.1f} Z')
    sway = (f'<animateTransform attributeName="transform" type="rotate" '
            f'values="-1.6 {tx:.0f} {ty:.0f};1.6 {tx:.0f} {ty:.0f};-1.6 {tx:.0f} {ty:.0f}" dur="7s" repeatCount="indefinite"/>')
    return (f'<path d="{trunk}" fill="{fill}"/>'
            f'<g fill="{fill}">{"".join(f"<path d=\"{f}\"/>" for f in fronds)}{sway}</g>')


# ------------------------------------------------------------------ HERO
def hero():
    W, H, HZ = 1200, 460, 345
    rng = random.Random(2049)
    p = []
    p.append(f'''<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#05020c"/><stop offset=".32" stop-color="#170a2b"/>
 <stop offset=".58" stop-color="#4a1446"/><stop offset=".8" stop-color="#a8323f"/>
 <stop offset="1" stop-color="#ff8a3d"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#ffe08a"/><stop offset=".45" stop-color="{AMBER}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#1c0724"/><stop offset="1" stop-color="#030106"/></linearGradient>
<linearGradient id="title" x1="0" y1="0" x2="0" y2="1">
 <stop offset="0" stop-color="#fff8ef"/><stop offset=".55" stop-color="#ffd9b0"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>
<linearGradient id="haze" x1="0" y1="0" x2="1" y2="0">
 <stop offset="0" stop-color="{AMBER}" stop-opacity="0"/><stop offset=".5" stop-color="{AMBER}" stop-opacity=".22"/>
 <stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></linearGradient>
<linearGradient id="trail" gradientUnits="userSpaceOnUse" x1="-160" y1="0" x2="0" y2="0">
 <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".9"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75">
 <stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".28"/></pattern>
<mask id="sunmask"><rect width="{W}" height="{H}" fill="#fff"/>
''')
    y, gap = HZ - 70, 3
    while y < HZ:
        p.append(f'<rect x="0" y="{y:.0f}" width="{W}" height="{gap:.1f}" fill="#000"/>')
        y += 13 - (y - (HZ - 70)) * 0.08
        gap += 1.1
    p.append('</mask>')
    p.append(glow_filter("g4", 4) + glow_filter("g10", 10) +
             '<filter id="blur30"><feGaussianBlur stdDeviation="30"/></filter>'
             '<filter id="blur8"><feGaussianBlur stdDeviation="8"/></filter></defs>')

    p.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    # stars
    for _ in range(60):
        sx, sy = rng.uniform(0, W), rng.uniform(0, 150)
        p.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{rng.uniform(.4,1.3):.1f}" fill="#fff" '
                 f'style="animation:pulse {rng.uniform(2,5):.1f}s ease-in-out {-rng.uniform(0,5):.1f}s infinite" opacity=".6"/>')
    # sun
    p.append(f'<circle cx="600" cy="{HZ}" r="170" fill="{PINK}" opacity=".45" filter="url(#blur30)" '
             f'style="animation:pulse 4s ease-in-out infinite"/>')
    p.append(f'<circle cx="600" cy="{HZ}" r="128" fill="url(#sun)" mask="url(#sunmask)"/>')
    # haze bands
    for i, (hy, hh, dur) in enumerate([(250, 40, 18), (292, 30, 24), (322, 26, 14)]):
        p.append(f'<rect x="-100" y="{hy}" width="{W+200}" height="{hh}" fill="url(#haze)" filter="url(#blur8)" '
                 f'style="animation:drift {dur}s ease-in-out {-i*5}s infinite"/>')

    # far skyline
    x = -10
    far = []
    while x < W:
        bw, bh = rng.randint(18, 52), rng.randint(30, 120)
        if 470 < x < 730:
            bh = rng.randint(14, 46)
        far.append(f'<rect x="{x}" y="{HZ-bh}" width="{bw}" height="{bh}"/>')
        x += bw + rng.randint(-4, 3)
    p.append(f'<g fill="#3b1040" opacity=".82">{"".join(far)}</g>')

    # near skyline with windows
    x = -10
    near, wins = [], []
    colors = [GOLD, AMBER, CYAN, PINK, "#ffe9c4"]
    while x < W:
        bw = rng.randint(26, 70)
        bh = rng.randint(50, 175)
        if 440 < x < 760:
            bh = rng.randint(20, 60)
        if x < 80 or x > 1090:
            bh = rng.randint(30, 80)
        near.append(f'<rect x="{x}" y="{HZ-bh}" width="{bw}" height="{bh}"/>')
        for wy in range(HZ - bh + 8, HZ - 6, 9):
            for wx in range(x + 5, x + bw - 5, 8):
                if rng.random() < 0.22:
                    c = rng.choice(colors)
                    anim = ""
                    if rng.random() < 0.18:
                        anim = f' style="animation:blink {rng.uniform(1.5,6):.1f}s steps(1) {-rng.uniform(0,6):.1f}s infinite"'
                    wins.append(f'<rect x="{wx}" y="{wy}" width="3" height="4" fill="{c}" opacity="{rng.uniform(.35,.9):.2f}"{anim}/>')
        x += bw + rng.randint(2, 8)
    p.append(f'<g fill="#0e0414">{"".join(near)}</g>')
    p.append(f'<g>{"".join(wins)}</g>')

    # landmark towers
    def tower(tx, tw, th, sign_chars, sign_color):
        s = [f'<rect x="{tx}" y="{HZ-th}" width="{tw}" height="{th}" fill="#08020d"/>',
             f'<polygon points="{tx},{HZ-th} {tx+tw/2},{HZ-th-26} {tx+tw},{HZ-th}" fill="#08020d"/>',
             f'<line x1="{tx+tw/2}" y1="{HZ-th-26}" x2="{tx+tw/2}" y2="{HZ-th-60}" stroke="#08020d" stroke-width="3"/>',
             f'<circle cx="{tx+tw/2}" cy="{HZ-th-61}" r="3" fill="#ff3355" filter="url(#g4)" style="animation:blink 1.6s steps(1) infinite"/>']
        sx, sy = tx + tw - 4, HZ - th + 30
        sh = len(sign_chars) * 26 + 14
        s.append(f'<g filter="url(#g4)" style="animation:flicker 5s linear infinite">'
                 f'<rect x="{sx}" y="{sy}" width="30" height="{sh}" rx="3" fill="#12031a" stroke="{sign_color}" stroke-width="2"/>')
        for i, ch in enumerate(sign_chars):
            s.append(f'<text x="{sx+15}" y="{sy+30+i*26}" text-anchor="middle" class="jp" font-size="20" font-weight="700" fill="{sign_color}">{ch}</text>')
        s.append('</g>')
        return "".join(s)

    p.append(tower(150, 64, 250, "データ", PINK))
    p.append(tower(985, 58, 230, "未来", CYAN))

    # floor + grid
    p.append(f'<rect y="{HZ}" width="{W}" height="{H-HZ}" fill="url(#floor)"/>')
    p.append(f'<ellipse cx="600" cy="{HZ+18}" rx="190" ry="20" fill="{PINK}" opacity=".35" filter="url(#blur8)"/>')
    grid = []
    for i in range(-14, 15):
        bx = 600 + i * 95
        grid.append(f'<line x1="{600 + i*8}" y1="{HZ}" x2="{bx}" y2="{H}"/>')
    p.append(f'<g stroke="{PINK}" stroke-width="1" opacity=".55">{"".join(grid)}</g>')
    hl = []
    for i in range(7):
        hl.append(f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}"><animate attributeName="y1" values="{HZ};{H}" dur="3.5s" '
                  f'begin="{-i*0.5:.1f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.55 0 1 1"/>'
                  f'<animate attributeName="y2" values="{HZ};{H}" dur="3.5s" begin="{-i*0.5:.1f}s" repeatCount="indefinite" '
                  f'calcMode="spline" keyTimes="0;1" keySplines="0.55 0 1 1"/></line>')
    p.append(f'<g stroke="{PINK}" stroke-width="1.2" opacity=".6">{"".join(hl)}</g>')
    p.append(f'<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" stroke="{GOLD}" stroke-width="1.5" opacity=".8" filter="url(#g4)"/>')

    # palms
    p.append(palm(70, H, 1.25))
    p.append(palm(1135, H, 1.15, flip=True))
    p.append(palm(1040, H + 10, 0.8))

    # flying spinner
    p.append(f'''<g><path d="M0,0 L-160,0" stroke="url(#trail)" stroke-width="2"/>
<ellipse cx="0" cy="0" rx="16" ry="4.5" fill="#100516"/>
<circle cx="13" cy="0" r="2.4" fill="{CYAN}" filter="url(#g4)"/>
<circle cx="-14" cy="1" r="1.8" fill="#ff3355" style="animation:blink .8s steps(1) infinite"/>
<animateMotion dur="16s" repeatCount="indefinite" path="M-200,240 C200,205 500,255 800,215 S1200,230 1420,200"/></g>''')
    p.append(f'''<g opacity=".8"><ellipse cx="0" cy="0" rx="9" ry="2.6" fill="#100516"/>
<circle cx="-7" cy="0" r="1.6" fill="{AMBER}" filter="url(#g4)"/>
<animateMotion dur="23s" begin="-9s" repeatCount="indefinite" path="M1400,180 C1000,200 700,170 300,195 S-100,185 -260,190"/></g>''')

    # rain
    p.append(rain(rng, 150, W, H))

    # title block
    title = "EREN KARTAL"
    tstyle = f'class="sans" font-size="80" font-weight="800" letter-spacing="16" text-anchor="middle"'
    p.append(f'<text x="606" y="128" {tstyle} fill="{PINK}" opacity="0" style="animation:g1 4s steps(1) infinite">{title}</text>')
    p.append(f'<text x="594" y="128" {tstyle} fill="{CYAN}" opacity="0" style="animation:g2 4s steps(1) infinite">{title}</text>')
    p.append(f'<text x="600" y="128" {tstyle} fill="url(#title)" filter="url(#g10)" style="animation:flicker 7s linear infinite">{title}</text>')
    p.append(f'<text x="600" y="170" class="mono" font-size="16" letter-spacing="5" text-anchor="middle" fill="{CYAN}" filter="url(#g4)">'
             f'BACKEND  ·  DATA PIPELINES  ·  DISTRIBUTED SYSTEMS</text>')
    p.append(f'<text x="600" y="198" class="sans" font-size="14" letter-spacing="2" text-anchor="middle" fill="#ffd9c2" opacity=".85">'
             f'Sakarya Üniversitesi · Bilgisayar Mühendisliği · Kocaeli, TR</text>')

    # HUD
    hud = []
    for (cx, cy, dx, dy) in [(18, 18, 1, 1), (W-18, 18, -1, 1), (18, H-18, 1, -1), (W-18, H-18, -1, -1)]:
        hud.append(f'<path d="M{cx},{cy+22*dy} L{cx},{cy} L{cx+22*dx},{cy}" fill="none" stroke="{GOLD}" stroke-width="2" opacity=".8"/>')
    hud.append(f'<circle cx="46" cy="38" r="4" fill="#ff3355" style="animation:blink 1.2s steps(1) infinite"/>')
    hud.append(f'<text x="58" y="42" class="mono" font-size="11" letter-spacing="2" fill="{GOLD}">REC  SYS://MAVIMAKUMBA</text>')
    hud.append(f'<text x="{W-40}" y="42" class="mono" font-size="11" letter-spacing="2" fill="{GOLD}" text-anchor="end">40.76°N 29.92°E · KOCAELI</text>')
    hud.append(f'<text x="40" y="{H-30}" class="mono" font-size="11" letter-spacing="2" fill="{CYAN}" opacity=".85">SECTOR 41 // NEON NOIR</text>')
    hud.append(f'<text x="{W-40}" y="{H-30}" class="mono" font-size="11" letter-spacing="2" fill="{CYAN}" opacity=".85" text-anchor="end">2026 · v2.0</text>')
    p.append("".join(hud))

    # overlays
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    p.append(f'<rect width="{W}" height="40" fill="#fff" opacity=".035" style="animation:scan 6s linear infinite"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')

    css = """
@keyframes g1{0%,86%,100%{opacity:0;transform:none}87%{opacity:.85;transform:translate(-5px,2px)}89%{opacity:.7;transform:translate(4px,-1px)}91%{opacity:0}95%{opacity:.6;transform:translate(-2px,0)}96%{opacity:0}}
@keyframes g2{0%,86%,100%{opacity:0;transform:none}87%{opacity:.85;transform:translate(5px,-2px)}89%{opacity:.7;transform:translate(-4px,1px)}91%{opacity:0}95%{opacity:.6;transform:translate(3px,0)}96%{opacity:0}}
"""
    write("hero.svg", svg(W, H, "".join(p), css, "Eren Kartal — Backend · Data Pipelines · Distributed Systems"))


# ------------------------------------------------------------------ SECTION HEADERS
def header(name, label, num, jp):
    W, H = 1200, 70
    body = f'''<defs>{glow_filter("g", 3)}
<linearGradient id="ln" gradientUnits="userSpaceOnUse" x1="{100 + len(label)*25.5:.0f}" x2="1110" y1="0" y2="0"><stop offset="0" stop-color="{PINK}"/><stop offset=".5" stop-color="{AMBER}" stop-opacity=".6"/>
<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient></defs>
<rect x="0" y="16" width="5" height="38" fill="{PINK}" filter="url(#g)" style="animation:pulse 2.4s ease-in-out infinite"/>
<text x="22" y="47" class="sans" font-size="28" font-weight="800" letter-spacing="7" fill="{TEXT}" filter="url(#g)"
 style="animation:flicker 9s linear {-len(label)}s infinite">{esc(label)}</text>
<text x="{30 + len(label)*25.5:.0f}" y="47" class="mono" font-size="13" letter-spacing="3" fill="{AMBER}">// {num}</text>
<line x1="{100 + len(label)*25.5:.0f}" y1="37" x2="1110" y2="37" stroke="url(#ln)" stroke-width="1.5"/>
<circle r="3" cy="37" fill="{CYAN}" filter="url(#g)"><animate attributeName="cx" values="{100 + len(label)*25.5:.0f};1110" dur="3.2s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="1;1;0" dur="3.2s" repeatCount="indefinite"/></circle>
<text x="1198" y="45" text-anchor="end" class="jp" font-size="20" font-weight="700" fill="{PINK}" opacity=".75">{jp}</text>'''
    write(f"h-{name}.svg", svg(W, H, body, title=label))


# ------------------------------------------------------------------ IDENTITY CARD
def identity():
    W, H = 1200, 330
    rows = [
        ("SUBJECT", "EREN KARTAL", TEXT),
        ("DESIGNATION", "Backend & Data Engineer", TEXT),
        ("ORIGIN", "Sakarya University — Computer Engineering", TEXT),
        ("SPECIALTY", "event-driven systems · streaming data · APIs · IoT", TEXT),
        ("CURRENT OPS", "TÜBİTAK 2209-B research · real-time IoT analytics", TEXT),
        ("SHIPPED", "NexStream → live at nexstreamnews.com", CYAN),
        ("STATUS", "● ONLINE — open to internships & collaboration", GREEN),
    ]
    p = [f'''<defs>{glow_filter("g", 3)}{glow_filter("g8", 8)}
<radialGradient id="iris" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000"/><stop offset=".28" stop-color="#1a0a05"/>
<stop offset=".36" stop-color="{AMBER}"/><stop offset=".7" stop-color="#7a2a12"/><stop offset="1" stop-color="#2a0c10"/></radialGradient>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#120a20"/><stop offset="1" stop-color="#07040d"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".3"/></pattern>
<clipPath id="eye"><circle cx="165" cy="150" r="88"/></clipPath></defs>
<polygon points="20,0 {W},0 {W},{H-20} {W-20},{H} 0,{H} 0,20" fill="url(#panel)"/>
<polygon points="20,1 {W-1},1 {W-1},{H-20} {W-20},{H-1} 1,{H-1} 1,20" fill="none" stroke="{AMBER}" stroke-opacity=".45"/>
<polygon points="20,1 {W-1},1 {W-1},{H-20} {W-20},{H-1} 1,{H-1} 1,20" fill="none" stroke="{PINK}" stroke-width="2"
 stroke-dasharray="120 880" style="animation:run 6s linear infinite" filter="url(#g)"/>''']
    # eye scanner
    p.append(f'''<g>
<circle cx="165" cy="150" r="118" fill="none" stroke="{AMBER}" stroke-opacity=".5" stroke-dasharray="3 7">
 <animateTransform attributeName="transform" type="rotate" values="0 165 150;360 165 150" dur="30s" repeatCount="indefinite"/></circle>
<circle cx="165" cy="150" r="104" fill="none" stroke="{CYAN}" stroke-opacity=".7" stroke-width="2" stroke-dasharray="40 25 8 25">
 <animateTransform attributeName="transform" type="rotate" values="360 165 150;0 165 150" dur="14s" repeatCount="indefinite"/></circle>
<circle cx="165" cy="150" r="88" fill="url(#iris)" filter="url(#g8)"/>
<g clip-path="url(#eye)" stroke="#ffb36b" stroke-opacity=".35">''')
    for i in range(48):
        a = math.radians(i * 7.5)
        p.append(f'<line x1="{165+math.cos(a)*30:.1f}" y1="{150+math.sin(a)*30:.1f}" x2="{165+math.cos(a)*86:.1f}" y2="{150+math.sin(a)*86:.1f}"/>')
    p.append(f'''</g><circle cx="165" cy="150" r="26" fill="#000"><animate attributeName="r" values="22;32;22" dur="3.5s" repeatCount="indefinite"/></circle>
<circle cx="152" cy="137" r="6" fill="#fff" opacity=".7"/>
<rect x="60" y="0" width="210" height="2" fill="{CYAN}" filter="url(#g)" clip-path="url(#eye)">
 <animate attributeName="y" values="60;240;60" dur="3s" repeatCount="indefinite"/></rect>
<text x="165" y="296" text-anchor="middle" class="mono" font-size="11" letter-spacing="3" fill="{AMBER}">IDENT SCAN · MATCH 100%</text></g>''')
    p.append(f'<line x1="320" y1="34" x2="320" y2="{H-34}" stroke="{AMBER}" stroke-opacity=".35"/>')
    p.append(f'<text x="350" y="50" class="mono" font-size="12" letter-spacing="4" fill="{PINK}">// PERSONNEL FILE · MAVIMAKUMBA</text>')
    y0, dy = 92, 33
    for i, (k, v, col) in enumerate(rows):
        y = y0 + i * dy
        d = 0.4 + i * 0.35
        p.append('<g>'
                 f'<text x="350" y="{y}" class="mono" font-size="14" letter-spacing="2" fill="{AMBER}">{k}</text>'
                 f'<text x="505" y="{y}" class="mono" font-size="14" fill="#6b5a85">{"." * 4}</text>'
                 f'<text x="550" y="{y}" class="mono" font-size="17" fill="{col}">{esc(v)}</text></g>')
    # caret after last row
    p.append(f'<rect x="{550 + len(rows[-1][1])*10.3 + 8:.0f}" y="{y0 + (len(rows)-1)*dy - 15}" width="10" height="18" fill="{GREEN}" style="animation:blink 1s steps(1) infinite"/>')
    p.append(f'<rect x="340" y="0" width="830" height="26" fill="{CYAN}" opacity=".07">'
             f'<animate attributeName="y" dur="{len(rows)*0.9:.1f}s" repeatCount="indefinite" calcMode="discrete" '
             f'keyTimes="{";".join(f"{i/len(rows):.3f}" for i in range(len(rows)))}" '
             f'values="{";".join(str(y0 + i*dy - 19) for i in range(len(rows)))}"/></rect>')
    # waveform
    pts = []
    for x in range(350, 1170, 6):
        t = (x - 350) / 820
        yv = 312 + math.sin(t * 40) * 3 + (math.exp(-((t * 820) % 205 - 100) ** 2 / 30) * -16)
        pts.append(f"{x},{yv:.1f}")
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="40 960" '
             f'filter="url(#g)" style="animation:run 3s linear infinite"/>')
    p.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{CYAN}" stroke-opacity=".18"/>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    write("identity.svg", svg(W, H, "".join(p), title="Personnel file: Eren Kartal, Backend & Data Engineer"))


# ------------------------------------------------------------------ CARD PRIMITIVES
def frame(W, H, accent=PINK, accent2=AMBER, cut=18, speed=7):
    pts = f"{cut},1 {W-1},1 {W-1},{H-cut} {W-cut},{H-1} 1,{H-1} 1,{cut}"
    return f'''<defs>{glow_filter("g", 3)}{glow_filter("g6", 6)}
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#140b22"/><stop offset="1" stop-color="#08040e"/></linearGradient>
<linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".25"/></pattern></defs>
<polygon points="{pts}" fill="url(#panel)"/>
<polygon points="{pts}" fill="none" stroke="url(#edge)" stroke-opacity=".35"/>
<polygon points="{pts}" fill="none" stroke="url(#edge)" stroke-width="2.2" stroke-dasharray="160 840" filter="url(#g)"
 style="animation:run {speed}s linear infinite"/>'''


def pill(x, y, text, color, anchor_right=True, dot=True):
    w = len(text) * 8.1 + (32 if dot else 20)
    x0 = x - w if anchor_right else x
    s = f'<rect x="{x0:.0f}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="{color}" fill-opacity=".1" stroke="{color}" stroke-opacity=".7"/>'
    tx = x0 + (24 if dot else 9)
    if dot:
        s += f'<circle cx="{x0+13:.0f}" cy="{y+12}" r="4" fill="{color}" filter="url(#g)" style="animation:blink 1.4s steps(1) infinite"/>'
    s += f'<text x="{tx:.0f}" y="{y+16.5}" class="mono" font-size="12" font-weight="700" letter-spacing="1" fill="{color}">{esc(text)}</text>'
    return s


def tags(x, y, items, color=MUTED, maxw=None):
    out, cx = [], x
    for t in items:
        w = len(t) * 7.4 + 18
        out.append(f'<rect x="{cx:.0f}" y="{y}" width="{w:.0f}" height="22" rx="4" fill="#ffffff" fill-opacity=".04" stroke="{color}" stroke-opacity=".35"/>'
                   f'<text x="{cx+9:.0f}" y="{y+15}" class="mono" font-size="12" fill="{color}">{esc(t)}</text>')
        cx += w + 8
    return "".join(out)


# ------------------------------------------------------------------ FLAGSHIP CARD
def nexstream():
    W, H = 1200, 400
    p = [frame(W, H, PINK, CYAN, cut=22, speed=8)]
    p.append(f'<text x="36" y="46" class="mono" font-size="12" letter-spacing="3" fill="{AMBER}">MISSION 01 // FLAGSHIP · PRODUCTION</text>')
    p.append(pill(W - 32, 28, "LIVE · nexstreamnews.com", GREEN))
    p.append(f'<text x="34" y="98" class="sans" font-size="44" font-weight="800" letter-spacing="1" fill="{TEXT}" filter="url(#g)">NexStream News Engine</text>')
    p.append(f'<text x="36" y="130" class="sans" font-size="18" fill="#e7d9ff">Event-driven, AI-powered news intelligence platform — a 16-service stack running in production on AWS.</text>')
    # pipeline line
    stages = ["17 SOURCES", "SCRAPER / 10 MIN", "REDPANDA BUS", "LLM ENRICH", "HYBRID SEARCH", "WEBSOCKET FEED"]
    sx, sy, sw = 36, 156, 1128
    step = sw / len(stages)
    p.append(f'<line x1="{sx+20}" y1="{sy+14}" x2="{sx+sw-20}" y2="{sy+14}" stroke="{CYAN}" stroke-opacity=".25"/>')
    p.append(f'<line x1="{sx+20}" y1="{sy+14}" x2="{sx+sw-20}" y2="{sy+14}" stroke="{CYAN}" stroke-width="2" stroke-dasharray="6 14" '
             f'style="animation:run 12s linear infinite"/>')
    for i, s in enumerate(stages):
        cx = sx + step * i + step / 2
        w = len(s) * 7.3 + 20
        p.append(f'<rect x="{cx-w/2:.0f}" y="{sy+2}" width="{w:.0f}" height="24" rx="3" fill="#0b0614" stroke="{CYAN}" stroke-opacity=".6"/>'
                 f'<text x="{cx:.0f}" y="{sy+18}" text-anchor="middle" class="mono" font-size="11.5" letter-spacing="1" fill="{CYAN}">{s}</text>')
    p.append(f'<circle r="4" cy="{sy+14}" fill="{PINK}" filter="url(#g6)"><animate attributeName="cx" values="{sx+20};{sx+sw-20}" dur="4s" repeatCount="indefinite"/></circle>')
    # stat tiles
    stats = [
        ("~0.5 s", "AI ANALYSIS / ARTICLE", "p95 2.1 s · live Prometheus"),
        ("16", "SERVICES ON ONE t3.small", "2 vCPU · 1.9 GB RAM"),
        ("1,004", "TESTS IN ~33 s", "12× faster than before"),
        ("−67%", "DOCKER IMAGE SIZE", "1.55 GB → 516 MB"),
        ("~6 s", "COLD START", "down from 1–2 min"),
    ]
    tx0, ty, tw, th, gap = 36, 208, 216, 112, 12
    for i, (big, lab, sub) in enumerate(stats):
        x = tx0 + i * (tw + gap)
        d = 0.3 + i * 0.18
        p.append('<g>'
                 f'<rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="6" fill="#ffffff" fill-opacity=".035" stroke="{PINK}" stroke-opacity=".3"/>'
                 f'<rect x="{x}" y="{ty}" width="3" height="{th}" fill="{PINK}"/>'
                 f'<text x="{x+18}" y="{ty+50}" class="sans" font-size="38" font-weight="800" fill="{CYAN}" filter="url(#g)">{esc(big)}</text>'
                 f'<text x="{x+18}" y="{ty+76}" class="mono" font-size="11.5" font-weight="700" letter-spacing="1" fill="{GOLD}">{esc(lab)}</text>'
                 f'<text x="{x+18}" y="{ty+97}" class="mono" font-size="11.5" fill="{MUTED}">{esc(sub)}</text></g>')
    p.append(tags(36, 346, ["FastAPI", "Next.js 14", "Redpanda", "PostgreSQL", "ChromaDB", "Redis", "Groq LLM",
                            "Prometheus", "Docker", "AWS", "Stripe"], color="#d6c6f2"))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    write("card-nexstream.svg", svg(W, H, "".join(p), title="NexStream News Engine — live at nexstreamnews.com"))


# ------------------------------------------------------------------ IN-DEV CARDS
def devcard(fname, mission, title, subtitle, lines, phases, active, stack, accent, note):
    W, H = 590, 420
    p = [frame(W, H, accent, AMBER, cut=18, speed=9)]
    p.append(f'<text x="28" y="40" class="mono" font-size="11.5" letter-spacing="2" fill="{AMBER}">{esc(mission)}</text>')
    p.append(pill(W - 24, 22, "IN DEVELOPMENT", GOLD))
    p.append(f'<text x="26" y="88" class="sans" font-size="31" font-weight="800" fill="{TEXT}" filter="url(#g)">{esc(title)}</text>')
    p.append(f'<text x="28" y="114" class="sans" font-size="15" fill="{accent}">{esc(subtitle)}</text>')
    for i, ln in enumerate(lines):
        p.append(f'<text x="28" y="{150 + i*25}" class="sans" font-size="14.5" fill="#ddd0f2">'
                 f'<tspan fill="{accent}">▸ </tspan>{esc(ln)}</text>')
    # roadmap
    ry = 150 + len(lines) * 25 + 30
    p.append(f'<text x="28" y="{ry-6}" class="mono" font-size="11" letter-spacing="3" fill="{MUTED}">ROADMAP</text>')
    x0, x1 = 44, W - 44
    n = len(phases)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    ly = ry + 24
    p.append(f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="#4a3a62" stroke-width="2"/>')
    p.append(f'<line x1="{x0}" y1="{ly}" x2="{xs[active]:.0f}" y2="{ly}" stroke="{accent}" stroke-width="3" filter="url(#g)" '
             f'stroke-dasharray="{xs[active]-x0:.0f}" stroke-dashoffset="{xs[active]-x0:.0f}">'
             f'<animate attributeName="stroke-dashoffset" from="{xs[active]-x0:.0f}" to="0" dur="1.6s" begin=".3s" fill="freeze"/></line>')
    for i, (xx, ph) in enumerate(zip(xs, phases)):
        if i < active:
            p.append(f'<circle cx="{xx:.0f}" cy="{ly}" r="8" fill="{accent}" filter="url(#g)"/>'
                     f'<path d="M{xx-4:.0f},{ly} l3,3 l5,-6" stroke="#0a0612" stroke-width="2" fill="none"/>')
        elif i == active:
            p.append(f'<circle cx="{xx:.0f}" cy="{ly}" r="14" fill="none" stroke="{GOLD}" stroke-opacity=".6">'
                     f'<animate attributeName="r" values="8;18;8" dur="2s" repeatCount="indefinite"/>'
                     f'<animate attributeName="stroke-opacity" values=".8;0;.8" dur="2s" repeatCount="indefinite"/></circle>'
                     f'<circle cx="{xx:.0f}" cy="{ly}" r="8" fill="#0a0612" stroke="{GOLD}" stroke-width="2.5"/>')
        else:
            p.append(f'<circle cx="{xx:.0f}" cy="{ly}" r="7" fill="#0a0612" stroke="#6b5a85" stroke-width="2" stroke-dasharray="3 3"/>')
        col = accent if i < active else (GOLD if i == active else "#8a7aa3")
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        xt = xx - 8 if i == 0 else (xx + 8 if i == n - 1 else xx)
        p.append(f'<text x="{xt:.0f}" y="{ly+30}" text-anchor="{anchor}" class="mono" font-size="11" font-weight="700" letter-spacing="1" fill="{col}">{esc(ph)}</text>')
    p.append(tags(28, H - 50, stack, color="#d6c6f2"))
    p.append(f'<text x="{W-26}" y="{H-34}" text-anchor="end" class="mono" font-size="10" fill="#7d6c99">{esc(note)}</text>')
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    write(fname, svg(W, H, "".join(p), title=f"{title} — {subtitle}"))


# ------------------------------------------------------------------ SIDE MISSION CARDS
def sidecard(fname, idx, title, desc, stack, status, accent):
    W, H = 590, 168
    p = [frame(W, H, accent, VIOLET, cut=14, speed=10)]
    p.append(f'<text x="24" y="34" class="mono" font-size="11" letter-spacing="2" fill="{AMBER}">SIDE MISSION {idx:02d}</text>')
    p.append(pill(W - 20, 16, status, accent, dot=False))
    p.append(f'<text x="22" y="72" class="sans" font-size="24" font-weight="800" fill="{TEXT}">{esc(title)}</text>')
    for i, ln in enumerate(desc):
        p.append(f'<text x="24" y="{98 + i*21}" class="sans" font-size="14" fill="#d3c6ea">{esc(ln)}</text>')
    p.append(tags(24, H - 36, stack, color=accent))
    p.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
    write(fname, svg(W, H, "".join(p), title=title))


# ------------------------------------------------------------------ FOOTER
def footer():
    W, H = 1200, 220
    rng = random.Random(41)
    p = [f'''<defs>{glow_filter("g", 4)}
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0612" stop-opacity="0"/>
<stop offset=".35" stop-color="#140821"/><stop offset="1" stop-color="#3a1030"/></linearGradient></defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>''']
    x, bl = -5, []
    while x < W:
        bw, bh = rng.randint(20, 60), rng.randint(20, 110)
        bl.append(f'<rect x="{x}" y="{H-bh}" width="{bw}" height="{bh}"/>')
        x += bw + rng.randint(0, 5)
    p.append(f'<g fill="#07030b">{"".join(bl)}</g>')
    p.append(rain(rng, 90, W, H, op=(0.1, 0.3)))
    p.append(f'<text x="600" y="80" text-anchor="middle" class="mono" font-size="15" letter-spacing="8" fill="{PINK}" filter="url(#g)" '
             f'style="animation:flicker 6s linear infinite">END OF TRANSMISSION</text>')
    p.append(f'<text x="600" y="116" text-anchor="middle" class="sans" font-size="20" font-style="italic" fill="#ffd9c2">'
             f'"The city never sleeps — neither do the pipelines."</text>')
    p.append(f'<text x="600" y="146" text-anchor="middle" class="jp" font-size="13" letter-spacing="4" fill="{CYAN}" opacity=".8">'
             f'通信終了 · EREN KARTAL · 2026</text>')
    p.append(f'<rect x="596" y="160" width="9" height="16" fill="{CYAN}" style="animation:blink 1s steps(1) infinite"/>')
    write("footer.svg", svg(W, H, "".join(p), title="End of transmission"))


hero()
identity()
for args in [("identity", "IDENTITY", "00", "身元"), ("missions", "MAIN MISSIONS", "01", "任務"),
             ("side", "SIDE MISSIONS", "02", "副任務"), ("arsenal", "ARSENAL", "03", "武器"),
             ("telemetry", "TELEMETRY", "04", "遠隔測定"), ("trail", "SIGNAL TRAIL", "05", "軌跡")]:
    header(*args)
nexstream()
devcard("card-acikgida.svg", "MISSION 02 // TÜBİTAK 2209-B RESEARCH", "Açık Gıda",
        "Explainable AI health scoring for packaged foods",
        ["Scan a barcode → get a 0–100 health score and the reasons behind it.",
         "Built on Türkiye's official 2026 nutrition score + Open Food Facts.",
         "Explainable by design: every point traced to sugar, salt, fat, fiber…",
         "My role: backend — PostgreSQL data model, import pipeline, REST API."],
        ["DATA", "BACKEND API", "AI MODELS", "MOBILE APP"], 2,
        ["FastAPI", "PostgreSQL", "LightGBM", "SHAP", "Expo"], CYAN, "private repo")
devcard("card-iot.svg", "MISSION 03 // BIG DATA · BSM 461", "Real-Time IoT Anomaly Pipeline",
        "Streaming analytics for a 200-sensor network",
        ["Designed for 2,000 events/s sustained and 2× peak load.",
         "Goal: flag anomalous sensors within 5 seconds of the event.",
         "Resilient to 15% late data, duplicates and dirty records.",
         "Kafka → Spark Structured Streaming → Delta Lake on S3."],
        ["TOPIC DESIGN", "ANOMALY STREAM", "DELTA SINK", "CHAOS TESTS"], 1,
        ["Kafka 4", "Spark 3.5", "Delta Lake", "DuckDB", "Docker"], PINK, "group project")
sidecard("side-afet.svg", 1, "Afet Bilgilendirme Sistemi",
         ["IoT smart-building safety: NFC access control that autonomously", "unlocks exits on earthquake/fire, with live web + mobile dashboards."],
         ["C++", "NodeMCU", "MQTT", "Firebase", ".NET MVC"], "COMPLETED", CYAN)
sidecard("side-gym.svg", 2, "GymApp",
         ["Gym management platform with AI-generated, personalized", "workout plans for members and reporting tools for admins."],
         ["ASP.NET Core 8", "C#", "Gemini AI", "MVC"], "COMPLETED", PINK)
sidecard("side-planner.svg", 3, "Planlama Ajanı",
         ["Autonomous task-planning agent that breaks goals into", "actionable plans, powered by Llama-3.3-70B on Groq."],
         ["Python", "Groq", "Llama 3.3", "LLM Agent"], "COMPLETED", AMBER)
sidecard("side-tarsau.svg", 4, "tarsau",
         ["Command-line archiving tool written in C — packs and", "unpacks text files into a single .sau archive format."],
         ["C", "Makefile", "CLI", "Linux"], "COMPLETED", VIOLET)
footer()
