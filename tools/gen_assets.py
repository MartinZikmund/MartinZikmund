"""Generates Fluent/WinUI-styled SVG assets (light + dark) for the GitHub profile README."""
import os
import sys
from html import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "light": dict(
        mica="#F3F3F3", layer="#F9F9F9", card="#FFFFFF", card2="#F6F6F6", stroke="#E5E5E5",
        fg="#1A1A1A", fg2="#5D5D5D", fg3="#8A8A8A", accent="#005FB8", onaccent="#FFFFFF",
        accentsoft="#E0EEF9", navsel="#EAEAEA", track="#D1D1D1", gold="#9D5D00", goldsoft="#FFF4CE",
    ),
    "dark": dict(
        mica="#202020", layer="#272727", card="#2D2D2D", card2="#323232", stroke="#3B3B3B",
        fg="#FFFFFF", fg2="#CFCFCF", fg3="#9A9A9A", accent="#60CDFF", onaccent="#003E5C",
        accentsoft="#1F3A4D", navsel="#333333", track="#4A4A4A", gold="#FCE100", goldsoft="#433519",
    ),
}

FONT = "'Segoe UI Variable Text','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"
DISPLAY = "'Segoe UI Variable Display','Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif"


def text_w(s, size, bold=False):
    # Rough Segoe UI advance widths, good enough for chip/wrap layout.
    w = 0
    for ch in s:
        if ch in "il.,:;'|!":
            w += 0.28
        elif ch in "mwMW":
            w += 0.85
        elif ch.isupper() or ch in "#+@":
            w += 0.66
        elif ch == " ":
            w += 0.28
        else:
            w += 0.54
    return w * size * (1.05 if bold else 1.0)


def svg(w, h, body, t, title):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
<title>{escape(title)}</title>
<style>
text{{font-family:{FONT};fill:{t['fg']}}}
.d{{font-family:{DISPLAY}}}
.s{{fill:{t['fg2']}}} .c{{fill:{t['fg3']}}} .a{{fill:{t['accent']}}} .oa{{fill:{t['onaccent']}}}
.sb{{font-weight:600}}
@keyframes slide{{0%{{transform:translateX(-160px)}}100%{{transform:translateX(620px)}}}}
@keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
.bar{{animation:slide 2.4s cubic-bezier(.4,0,.2,1) infinite}}
.caret{{animation:blink 1.1s step-end infinite}}
@media (prefers-reduced-motion: reduce){{.bar,.caret{{animation:none}}}}
</style>
{body}
</svg>
"""


def icon(kind, x, y, color):
    # 16px line icons in the spirit of Fluent System Icons.
    s = f'fill="none" stroke="{color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"'
    g = f'<g transform="translate({x},{y})">'
    if kind == "home":
        g += f'<path d="M2 7.5 8 2.5l6 5V14H10V10H6v4H2z" {s}/>'
    elif kind == "uno":
        g += f'<circle cx="8" cy="8" r="6" {s}/><circle cx="8" cy="8" r="2" {s}/>'
    elif kind == "winui":
        g += f'<rect x="2" y="2" width="5" height="5" rx="1" {s}/><rect x="9" y="2" width="5" height="5" rx="1" {s}/><rect x="2" y="9" width="5" height="5" rx="1" {s}/><rect x="9" y="9" width="5" height="5" rx="1" {s}/>'
    elif kind == "mic":
        g += f'<rect x="5.5" y="1.5" width="5" height="8" rx="2.5" {s}/><path d="M3 8a5 5 0 0 0 10 0M8 13v2" {s}/>'
    elif kind == "code":
        g += f'<path d="M5.5 4 2 8l3.5 4M10.5 4 14 8l-3.5 4" {s}/>'
    elif kind == "spark":
        g += f'<path d="M8 1.5 9.6 6.4 14.5 8 9.6 9.6 8 14.5 6.4 9.6 1.5 8 6.4 6.4z" {s}/>'
    elif kind == "gear":
        g += f'<circle cx="8" cy="8" r="2.3" {s}/><path d="M8 1.5v2M8 12.5v2M1.5 8h2M12.5 8h2M3.4 3.4l1.4 1.4M11.2 11.2l1.4 1.4M3.4 12.6l1.4-1.4M11.2 4.8l1.4-1.4" {s}/>'
    elif kind == "info":
        g += f'<circle cx="8" cy="8" r="7" fill="{color}"/><path d="M8 7v4.2" stroke="#fff" stroke-width="1.6" stroke-linecap="round"/><circle cx="8" cy="4.8" r="1" fill="#fff"/>'
    return g + "</g>"


def hero(t):
    W, H = 840, 384
    b = [f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="{t["mica"]}" stroke="{t["stroke"]}"/>']
    # Title bar
    b.append(f'<rect x="14" y="10" width="16" height="16" rx="4" fill="{t["accent"]}"/><text x="22" y="22" font-size="10" text-anchor="middle" class="sb oa">MZ</text>')
    b.append(f'<text x="40" y="22" font-size="12">Martin Zikmund</text><text x="132" y="22" font-size="12" class="c">github.com/MartinZikmund</text>')
    for i, kind in enumerate(["min", "max", "close"]):
        cx = W - 23 - (2 - i) * 46
        if kind == "min":
            b.append(f'<path d="M{cx-5} 18h10" stroke="{t["fg"]}" stroke-width="1"/>')
        elif kind == "max":
            b.append(f'<rect x="{cx-5}" y="13" width="10" height="10" rx="1.5" fill="none" stroke="{t["fg"]}"/>')
        else:
            b.append(f'<path d="M{cx-5} 13l10 10M{cx+5} 13l-10 10" stroke="{t["fg"]}" stroke-width="1"/>')
    # NavigationView pane
    items = [("home", "Home"), ("uno", "Uno Platform"), ("winui", "WinUI"), ("spark", "AI tooling"), ("mic", "Talks"), ("code", "Side projects")]
    y = 48
    for i, (k, label) in enumerate(items):
        if i == 0:
            b.append(f'<rect x="8" y="{y}" width="184" height="36" rx="4" fill="{t["navsel"]}"/><rect x="8" y="{y+10}" width="3" height="16" rx="1.5" fill="{t["accent"]}"/>')
        b.append(icon(k, 22, y + 10, t["fg"]))
        b.append(f'<text x="52" y="{y+23}" font-size="14">{label}</text>')
        y += 40
    b.append(icon("gear", 22, H - 46, t["fg"]))
    b.append(f'<text x="52" y="{H-33}" font-size="14">Settings</text>')
    # Content layer
    cx0 = 200
    b.append(f'<path d="M{cx0} 40h{W-cx0-8}a8 8 0 0 1 8 8v{H-48-1}H{cx0+8}a8 8 0 0 1-8-8z" fill="{t["layer"]}" stroke="{t["stroke"]}"/>')
    x = cx0 + 28
    b.append(f'<text x="{x}" y="96" font-size="40" class="d sb">Hi, I\'m Martin</text>')
    b.append(f'<text x="{x+256}" y="94" font-size="34">👋</text>')
    b.append(f'<text x="{x}" y="128" font-size="15" class="s">Bringing WinUI to every platform, one ported C++ file at a time.</text>')
    b.append(f'<text x="{x}" y="150" font-size="15" class="s">Senior Lead Software Engineer at Uno Platform · Prague, Czechia</text>')
    # InfoBar
    b.append(f'<rect x="{x}" y="168" width="{W-x-28}" height="44" rx="4" fill="{t["card2"]}" stroke="{t["stroke"]}"/>')
    b.append(icon("info", x + 14, 182, t["accent"]))
    b.append(f'<text x="{x+42}" y="195" font-size="14"><tspan class="sb">Microsoft MVP</tspan><tspan class="s">  ·  Developer Technologies  ·  International conference speaker</tspan></text>')
    # Stat cards
    stats = [("10,100+", "commits to Uno"), ("1,480+", "merged PRs"), ("25+", "conference talks"), ("14", "PRs to WinUI")]
    cw = (W - x - 28 - 3 * 12) / 4
    for i, (n, l) in enumerate(stats):
        sx = x + i * (cw + 12)
        b.append(f'<rect x="{sx:.1f}" y="228" width="{cw:.1f}" height="80" rx="8" fill="{t["card"]}" stroke="{t["stroke"]}"/>')
        b.append(f'<text x="{sx+16:.1f}" y="266" font-size="28" class="d sb a">{n}</text>')
        b.append(f'<text x="{sx+16:.1f}" y="290" font-size="12" class="s">{l}</text>')
    # Indeterminate ProgressBar
    b.append(f'<text x="{x}" y="338" font-size="12" class="c">Currently: porting WinUI to every platform<tspan class="caret">▍</tspan></text>')
    bw = W - x - 28
    b.append(f'<defs><clipPath id="pb"><rect x="{x}" y="350" width="{bw}" height="3" rx="1.5"/></clipPath></defs>')
    b.append(f'<rect x="{x}" y="351" width="{bw}" height="1" fill="{t["track"]}"/>')
    b.append(f'<g clip-path="url(#pb)"><g transform="translate({x},0)"><rect class="bar" x="0" y="350" width="140" height="3" rx="1.5" fill="{t["accent"]}"/></g></g>')
    return svg(W, H, "\n".join(b), t, "Hi, I'm Martin Zikmund: Senior Lead Software Engineer at Uno Platform and Microsoft MVP")


def chips_card(t, x, y, w, title, glyph, chips, min_h=0):
    out, cy = [], y + 52
    cx = x + 16
    rows = []
    for name, on in chips:
        cw = text_w(name, 13) + 24
        if cx + cw > x + w - 16:
            cx = x + 16
            cy += 36
        rows.append((cx, cy, cw, name, on))
        cx += cw + 8
    h = max(cy - y + 44, min_h)
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{t["card"]}" stroke="{t["stroke"]}"/>')
    out.append(icon(glyph, x + 16, y + 17, t["accent"]))
    out.append(f'<text x="{x+42}" y="{y+30}" font-size="16" class="sb">{title}</text>')
    for cx, cy, cw, name, on in rows:
        if on:
            out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="28" rx="4" fill="{t["accent"]}"/>')
            out.append(f'<text x="{cx+cw/2:.1f}" y="{cy+19}" font-size="13" text-anchor="middle" class="oa sb">{escape(name)}</text>')
        else:
            out.append(f'<rect x="{cx:.1f}" y="{cy}" width="{cw:.1f}" height="28" rx="4" fill="{t["card2"]}" stroke="{t["stroke"]}"/>')
            out.append(f'<text x="{cx+cw/2:.1f}" y="{cy+19}" font-size="13" text-anchor="middle">{escape(name)}</text>')
    return out, h


def skills(t):
    W = 840
    cards = [
        ("UI &amp; platforms", "winui", [("WinUI", 1), ("Uno Platform", 1), ("XAML", 0), ("Skia", 0), ("WebAssembly", 0), ("Windows App SDK", 0), (".NET MAUI", 0), ("Xamarin", 0), ("UWP", 0), ("WPF", 0), ("Win2D", 0)]),
        ("Languages", "code", [("C#", 1), ("C++", 0), ("XAML", 0), ("TypeScript", 0), ("MSBuild", 0), ("PowerShell", 0)]),
        ("Craft", "spark", [("Performance", 1), ("AI agents", 1), ("Claude Code", 0), ("MCP", 0), ("Accessibility", 0), ("Source generators", 0), ("QA & UX review", 0), ("Speaking", 0), ("DevRel", 0)]),
    ]
    cw = (W - 2 * 12) / 3
    body, hmax, parts = [], 0, []
    for i, (title, g, chips) in enumerate(cards):
        hmax = max(hmax, chips_card(t, 0, 0, cw - 1, title, g, chips)[1])
    for i, (title, g, chips) in enumerate(cards):
        out, h = chips_card(t, i * (cw + 12) + 0.5, 0.5, cw - 1, title, g, chips, hmax)
        parts.append(out)
    for p in parts:
        body += p
    return svg(W, int(hmax + 2), "\n".join(body), t, "Skills: WinUI, Uno Platform, C#, C++, performance, AI agents and more")


def project(t, name, glyph, grad, desc, tag):
    W, H = 272, 120
    b = [f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{grad[0]}"/><stop offset="1" stop-color="{grad[1]}"/></linearGradient></defs>']
    b.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="8" fill="{t["card"]}" stroke="{t["stroke"]}"/>')
    b.append(f'<rect x="16" y="16" width="44" height="44" rx="8" fill="url(#g)"/><text x="38" y="46" font-size="22" text-anchor="middle" style="fill:#fff">{glyph}</text>')
    b.append(f'<text x="72" y="36" font-size="16" class="sb">{escape(name)}</text>')
    b.append(f'<text x="72" y="56" font-size="12" class="c">{escape(tag)}</text>')
    words, lines, cur = desc.split(), [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        if text_w(test, 13) > W - 32:
            lines.append(cur)
            cur = wd
        else:
            cur = test
    lines.append(cur)
    for i, ln in enumerate(lines[:2]):
        b.append(f'<text x="16" y="{84 + i*18}" font-size="13" class="s">{escape(ln)}</text>')
    return svg(W, H, "\n".join(b), t, f"{name}: {desc}")


PROJECTS = [
    ("unodoom", "UnoDoom", "👾", ("#C42B1C", "#6B0F07"), "DOOM running on iOS, Android, macOS, Windows, Linux and the web", "C# · Uno Platform"),
    ("dailyplants", "Daily Plants", "🌱", ("#107C10", "#6CCB5F"), "Daily Dozen checklist. Private, no ads, on the Microsoft Store", "C# · Uno Platform"),
    ("awesome", "awesome-uno-platform", "★", ("#7A4FD6", "#B38BFA"), "Curated list of resources for Uno Platform developers", "81 stars · community"),
    ("wanakana", "WanaKana-net", "あ", ("#E3008C", "#FF7AC4"), ".NET port of WanaKana for Japanese transliteration", "C# · library"),
    ("aoc", "advent-of-code", "🎄", ("#C50F1F", "#F1707B"), "Advent of Code in C#, solved live on YouTube", "C# · yearly tradition"),
    ("stopwatch", "Fluent Stopwatch", "⏱", ("#0F6CBD", "#47A9F5"), "Multiple timers, laps and history on every platform", "C# · Uno Platform"),
]


def achievements(t):
    W = 840
    items = [
        ("#1 Uno Platform contributor", "Most commits since it went open source"),
        ("Microsoft MVP", "Developer Technologies"),
        ("Agent wrangler", "Built the Claude Code agent setup Uno runs on"),
        ("Bronze medal", "Central European Olympiad in Informatics"),
        ("Double national champion", "Czech Olympiads in Informatics and Linguistics"),
        ("Most Active Speaker", "Sessionize, 2022 and 2024"),
    ]
    cw, ch, gap = (W - 12) / 2, 76, 12
    b = []
    for i, (title, sub) in enumerate(items):
        x = (i % 2) * (cw + gap) + 0.5
        y = (i // 2) * (ch + gap) + 0.5
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{cw-1:.1f}" height="{ch}" rx="38" fill="{t["card"]}" stroke="{t["stroke"]}"/>')
        b.append(f'<circle cx="{x+38:.1f}" cy="{y+38}" r="24" fill="{t["goldsoft"]}"/>')
        b.append(f'<text x="{x+38:.1f}" y="{y+46}" font-size="22" text-anchor="middle">🏆</text>')
        b.append(f'<text x="{x+76:.1f}" y="{y+24}" font-size="10" class="c sb" letter-spacing="0.8">ACHIEVEMENT UNLOCKED</text>')
        b.append(f'<text x="{x+76:.1f}" y="{y+44}" font-size="15" class="sb">{escape(title)}</text>')
        b.append(f'<text x="{x+76:.1f}" y="{y+62}" font-size="12" class="s">{escape(sub)}</text>')
    H = 3 * ch + 2 * gap + 1
    return svg(W, H, "\n".join(b), t, "Achievements: top Uno Platform contributor, Microsoft MVP, AI agent tooling, olympiad medals, Most Active Speaker")


for theme, t in THEMES.items():
    files = {f"hero-{theme}.svg": hero(t), f"skills-{theme}.svg": skills(t), f"achievements-{theme}.svg": achievements(t)}
    for key, name, glyph, grad, desc, tag in PROJECTS:
        files[f"project-{key}-{theme}.svg"] = project(t, name, glyph, grad, desc, tag)
    for fn, content in files.items():
        with open(os.path.join(OUT, fn), "w", encoding="utf-8") as f:
            f.write(content)
print("ok")
