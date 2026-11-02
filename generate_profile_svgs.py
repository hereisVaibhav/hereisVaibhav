"""Generates the animated GitHub profile SVGs. Edit the CONFIG block, then run: python3 generate.py"""
import math, os

# ================= CONFIG (edit these) =================
NAME = "Vaibhav Shingade"
ROLE = "Researcher / Developer"
EDUCATION = "M.Sc Biotech + MCA"
LOCATION = "Pune, India"
STATUS = "Freelancer"
ID_NO = "VS-2026-001"
SKILLS = [("Python", 90), ("AI / LLMs", 85), ("Data Science", 85), ("Bioinformatics", 80),
          ("JavaScript", 75), ("Research", 85), ("Web / Framer", 70), ("Biotech", 80)]
RINGS = [("Research", 88), ("Development", 90), ("AI / ML", 85), ("Learning", 95)]  # overall = average
STATS = [("3+", "Years Experience"), ("16+", "Completed Projects"), ("12+", "Technologies Mastered"), ("2", "Research Papers")]
BUILD = [("</>", "Web Apps", "Sites, dashboards, tools"), ("AI", "LLM & AI Tools", "Agents, assistants, RAG"),
         ("{ }", "Data & Research", "Analysis, models, papers"), ("DNA", "Bioinformatics", "Biotech meets code"),
         ("->", "Automation", "Save hours every week"), ("+", "Your idea?", "Let's talk about it")]
OUT = os.environ.get("OUT", "/mnt/user-data/outputs")
# =======================================================

G = "#3fb950"; BG = "#0d1117"; CARD = "#161b22"; LN = "#30363d"; TX = "#c9d1d9"; MU = "#8b949e"
SKIN = "#f1c27d"; HAIR = "#2d2a26"; PANTS = "#30363d"
FONT = "'SF Mono','Fira Code',Consolas,Menlo,monospace"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;")
def R(x, y, w, h, f, extra=""):
    end = ">" if extra.rstrip().endswith("</rect") else "/>"
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}" {extra}{end}'
def A(attr, values, dur, kt=None, begin=0, extra=""):
    k = f' keyTimes="{kt}"' if kt else ""
    return f'<animate attributeName="{attr}" values="{values}"{k} dur="{dur}s" begin="{begin}s" repeatCount="indefinite" {extra}/>'
def T(x, y, s, fill=TX, size=14, bold=False, anchor="start", extra=""):
    w = ' font-weight="bold"' if bold else ""
    return f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}"{w} text-anchor="{anchor}" {extra}>{esc(s)}</text>'
def save(name, w, h, body):
    s = (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
         f'viewBox="0 0 {w} {h}" font-family="{FONT}" font-size="14">'
         f'<rect width="{w}" height="{h}" rx="12" fill="{BG}" stroke="{LN}"/>{body}</svg>\n')
    open(os.path.join(OUT, name), "w").write(s)
def titlebar(title):
    return (f'<path d="M0 12a12 12 0 0 1 12-12h876a12 12 0 0 1 12 12v28H0z" fill="{CARD}"/>'
            '<circle cx="26" cy="20" r="7" fill="#ff5f56"/><circle cx="50" cy="20" r="7" fill="#ffbd2e"/><circle cx="74" cy="20" r="7" fill="#27c93f"/>'
            + T(450, 25, title, MU, 13, anchor="middle"))

# ---------- 1. skills ----------
def skills():
    b = titlebar("skills.sh - running")
    b += T(30, 70, "$ ./skills --show", G, 14, True)
    for i, (n, v) in enumerate(SKILLS):
        col, row = divmod(i, 4)
        x = 40 + col * 430; y = 104 + row * 42
        W = int(230 * v / 100)
        b += T(x, y + 10, n, TX, 14)
        b += R(x + 140, y, 230, 10, "#21262d", 'rx="5"')
        b += R(x + 140, y, 0, 10, G, f'rx="5">{A("width", f"0;{W};{W}", 7, "0;0.25;1", begin=round(i*0.15,2))}</rect')
        b += T(x + 380, y + 10, f"{v}%", MU, 13)
    save("skills.svg", 900, 280, b)

# ---------- 2. performance rings ----------
def ring(cx, cy, r, sw, v, color, label, big=False):
    C = round(2 * math.pi * r, 1); off = round(C * (1 - v / 100), 1)
    b = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#21262d" stroke-width="{sw}"/>'
    b += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" '
          f'stroke-dasharray="{C}" stroke-dashoffset="{C}" transform="rotate(-90 {cx} {cy})">'
          + A("stroke-dashoffset", f"{C};{off};{off}", 7, "0;0.3;1") + '</circle>')
    b += T(cx, cy + (9 if big else 7), f"{v}%", TX, 26 if big else 20, True, "middle")
    b += T(cx, cy + r + 34, label, color if big else MU, 14, big, "middle")
    return b
def performance():
    b = titlebar("performance.sh - overall") + T(30, 70, "$ ./performance --overall", G, 14, True)
    overall = round(sum(v for _, v in RINGS) / len(RINGS))
    cols = ["#3fb950", "#56d4dd", "#d2a8ff", "#ffa657"]
    order = [RINGS[0], RINGS[1], ("OVERALL", overall), RINGS[2], RINGS[3]]
    for i, (n, v) in enumerate(order):
        cx = 100 + 175 * i
        if n == "OVERALL": b += ring(cx, 170, 62, 12, v, "#e3b341", n, True)
        else: b += ring(cx, 170, 46, 10, v, cols[(i if i < 2 else i - 1)], n)
    save("performance.svg", 900, 300, b)

# ---------- 3. stats ----------
def stats():
    b = ""
    for i, (num, lab) in enumerate(STATS):
        x = 30 + i * 215
        b += R(x, 20, 195, 130, CARD, f'rx="10" stroke="{LN}"')
        b += R(x, 20, 0, 3, G, 'rx="1">' + A("width", "0;195;195;0", 5, "0;0.3;0.8;1", begin=round(i * 0.25, 2)) + '</rect')
        b += (f'<text x="{x+97}" y="82" fill="{G}" font-size="44" font-weight="bold" text-anchor="middle">{esc(num)}'
              + A("fill-opacity", "0.65;1;0.65", 3, begin=round(i * 0.4, 2)) + '</text>')
        b += T(x + 97, 118, lab, MU, 13, False, "middle")
    save("stats.svg", 900, 170, b)

# ---------- 4. ID card ----------
AV = ["............", "....HHHH....", "...HHHHHH...", "..HHHHHHHH..", "..HSSSSSSH..", "..SSESSESS..", "..SSSSSSSS..",
      "..SSSSSSSS..", "...SSMMSS...", "....SSSS....", ".TTTTTTTTTT.", "TTTTTTTTTTTT", "TTTTTTTTTTTT", "TTTTTTTTTTTT"]
def idcard():
    cx, cy, cw, ch = 170, 20, 560, 260
    b = (f'<defs><clipPath id="c"><rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16"/></clipPath>'
         f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1c2330"/><stop offset="1" stop-color="#0d1117"/></linearGradient>'
         '<linearGradient id="s" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".12"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
    b += f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="16" fill="url(#g)" stroke="{G}" stroke-opacity=".6"/>'
    b += '<g clip-path="url(#c)">'
    b += R(cx, cy, cw, 44, G)
    b += T(cx + 20, cy + 28, "DEVELOPER / RESEARCHER ID", BG, 14, True)
    b += T(cx + cw - 20, cy + 28, "ID: " + ID_NO, BG, 13, True, "end")
    b += R(cx + 20, cy + 62, 120, 140, "#21262d", 'rx="6"')
    cm = {"H": HAIR, "S": SKIN, "E": "#111", "M": "#b9854f", "T": G}
    for r, row in enumerate(AV):
        for c, ch_ in enumerate(row):
            if ch_ in cm: b += R(cx + 20 + c * 10, cy + 62 + r * 10, 10, 10, cm[ch_])
    fields = [("NAME", NAME), ("ROLE", ROLE), ("EDUCATION", EDUCATION), ("BASED IN", LOCATION), ("STATUS", STATUS)]
    for i, (k, v) in enumerate(fields):
        y = cy + 76 + i * 34
        b += T(cx + 170, y, k, MU, 11) + T(cx + 170, y + 17, v, G if k == "STATUS" else TX, 16, True)
    for i in range(40):
        w = 2 + (i * 7) % 4
        b += R(cx + 330 + i * 5, cy + 205, w, 36, MU, 'opacity=".7"')
    b += R(cx - 200, cy, 120, ch, "url(#s)", 'transform="skewX(-20)">' + f'<animateTransform attributeName="transform" type="translate" values="0 0;760 0;760 0" keyTimes="0;.5;1" dur="5s" repeatCount="indefinite" additive="sum"/></rect')
    b += '</g>'
    save("idcard.svg", 900, 300, b)

# ---------- 5. build together ----------
def build():
    b = T(40, 68, "Let's build ", TX, 34, True) + T(40 + 12 * 20.4, 68, "together", G, 34, True)
    b += R(40 + 20 * 20.4 + 8, 40, 14, 32, G, f'>{A("opacity","1;1;0;0",1.1,"0;.5;.5;1")}</rect')
    b += T(40, 98, "Open for freelance projects and research collaborations.", MU, 14)
    for i, (ic, t, s) in enumerate(BUILD):
        col, row = i % 3, i // 3
        x = 30 + col * 285; y = 125 + row * 85
        last = i == len(BUILD) - 1
        b += R(x, y, 270, 70, CARD, f'rx="10" stroke="{G if last else LN}">' + (A("stroke-opacity", "1;.25;1", 2) if last else "") + '</rect')
        b += T(x + 36, y + 42, ic, G, 18, True, "middle")
        b += T(x + 70, y + 30, t, TX, 15, True) + T(x + 70, y + 50, s, MU, 12)
    save("build.svg", 900, 320, b)

# ---------- 6. traits (original pixel figures) ----------
def panel(i, title, sub, fig):
    x = 30 + i * 215
    b = f'<g transform="translate({x} 15)">' + R(0, 0, 195, 250, CARD, f'rx="10" stroke="{LN}"') + fig
    b += T(97, 218, title, G, 15, True, "middle") + T(97, 238, sub, MU, 12, False, "middle") + '</g>'
    return b
def typist():
    f = f'<circle cx="35" cy="38" r="14" fill="none" stroke="{MU}" stroke-width="2"/>'
    f += f'<line x1="35" y1="38" x2="35" y2="28" stroke="{G}" stroke-width="2"><animateTransform attributeName="transform" type="rotate" from="0 35 38" to="360 35 38" dur="3s" repeatCount="indefinite"/></line>'
    f += f'<circle cx="160" cy="36" r="9" fill="#e3b341"/><circle cx="164" cy="33" r="8" fill="{CARD}"/>'
    for k, (sx, sy) in enumerate([(130, 24), (145, 52), (115, 46)]):
        f += R(sx, sy, 3, 3, "#e3b341", f'>{A("opacity", "1;.2;1", 1.6, begin=k*0.5)}</rect')
    f += R(25, 150, 145, 8, PANTS) + R(35, 158, 6, 28, PANTS) + R(154, 158, 6, 28, PANTS)
    f += R(48, 126, 8, 24, PANTS)
    f += R(88, 108, 44, 36, BG, f'stroke="{G}"') + R(80, 142, 60, 8, MU)
    for k, w in enumerate([26, 18, 30, 14]):
        f += R(94, 114 + k * 8, 4, 4, G) + R(100, 114 + k * 8, 0, 4, "#56d4dd", f'>{A("width", f"0;{w};{w}", 2.4, "0;.6;1", begin=k*0.3)}</rect')
    f += R(56, 92, 22, 22, SKIN) + R(56, 88, 22, 8, HAIR) + R(56, 92, 22, 4, G) + R(68, 100, 4, 4, "#111")
    f += R(54, 114, 28, 36, G)
    f += f'<g>{R(76, 124, 38, 8, SKIN)}<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="0.5s" repeatCount="indefinite"/></g>'
    return f
def lifter():
    kt = "0;.5;1"; vals = lambda a, b_: f"{a};{b_};{a}"
    f = R(80, 140, 14, 44, PANTS) + R(102, 140, 14, 44, PANTS) + R(76, 182, 20, 6, "#111") + R(100, 182, 20, 6, "#111")
    f += R(74, 92, 48, 50, G) + R(86, 62, 24, 24, SKIN) + R(86, 58, 24, 8, HAIR) + R(86, 62, 24, 4, "#ff7b72")
    f += R(92, 72, 4, 4, "#111") + R(102, 72, 4, 4, "#111") + R(94, 80, 10, 2, "#b9854f")
    for ax in (66, 122):
        f += R(ax, 90, 8, 6, SKIN, f'>{A("y", vals(90, 40), 1.6, kt)}{A("height", vals(6, 56), 1.6, kt)}</rect')
    f += R(34, 88, 128, 6, MU, f'>{A("y", vals(88, 38), 1.6, kt)}</rect')
    for px_, w in ((30, 10), (42, 8), (148, 10), (140, 8)):
        f += R(px_, 70, w, 42, "#ff7b72", f'>{A("y", vals(70, 20), 1.6, kt)}</rect')
    for k in range(3):
        f += f'<circle cx="{120 + k * 6}" cy="70" r="2.5" fill="#56d4dd">{A("cy", "70;90;90", 1.6, "0;.9;1", begin=k*0.5)}{A("opacity", "0;1;0", 1.6, begin=k*0.5)}</circle>'
    return f
def meditator():
    f = ""
    for k, r in enumerate((38, 54, 70)):
        f += f'<circle cx="97" cy="100" r="{r}" fill="none" stroke="{G}" stroke-width="2" stroke-opacity=".5">{A("r", f"{r};{r+8};{r}", 2.4, begin=k*0.4)}{A("stroke-opacity", ".6;.1;.6", 2.4, begin=k*0.4)}</circle>'
    g = (R(87, 66, 22, 22, SKIN) + R(87, 62, 22, 8, HAIR) + R(91, 78, 6, 2, "#111") + R(101, 78, 6, 2, "#111") + R(95, 71, 3, 3, "#e3b341")
         + R(80, 90, 36, 34, G) + R(70, 100, 10, 22, G) + R(116, 100, 10, 22, G) + R(68, 120, 12, 8, SKIN) + R(116, 120, 12, 8, SKIN)
         + R(64, 124, 68, 12, PANTS) + R(72, 134, 52, 10, "#21262d"))
    f += f'<g>{g}<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="3s" repeatCount="indefinite"/></g>'
    for k, px_ in enumerate((50, 140, 160, 36)):
        f += R(px_, 170, 3, 3, G, f'>{A("y", "170;60", 3, begin=k*0.7)}{A("opacity", "0;1;0", 3, begin=k*0.7)}</rect')
    return f
def researcher():
    f = R(82, 144, 12, 40, PANTS) + R(100, 144, 12, 40, PANTS) + R(78, 182, 18, 6, "#111") + R(98, 182, 18, 6, "#111")
    f += R(76, 92, 42, 54, "#e6edf3") + R(88, 92, 18, 54, "#c9d1d9") + R(68, 98, 9, 40, "#e6edf3") + R(68, 136, 9, 8, SKIN)
    f += R(86, 62, 24, 24, SKIN) + R(86, 58, 24, 8, HAIR) + R(84, 70, 28, 8, "#56d4dd", 'opacity=".55"') + R(92, 72, 4, 4, "#111") + R(102, 72, 4, 4, "#111")
    f += R(112, 102, 32, 9, "#e6edf3") + R(140, 102, 8, 9, SKIN)
    f += f'<g><polygon points="150,84 158,84 172,120 136,120" fill="#56d4dd" fill-opacity=".25" stroke="#56d4dd"/><polygon points="145,104 163,104 172,120 136,120" fill="#56d4dd" fill-opacity=".6"/><animateTransform attributeName="transform" type="rotate" values="-4 154 120;4 154 120;-4 154 120" dur="2s" repeatCount="indefinite"/></g>'
    for k, bx in enumerate((150, 156, 153)):
        f += f'<circle cx="{bx}" cy="100" r="2.5" fill="#56d4dd">{A("cy", "100;60", 2, begin=k*0.6)}{A("opacity", "1;0", 2, begin=k*0.6)}</circle>'
    return f
def traits():
    b = (panel(0, "DEDICATION", "Showing up every day", typist()) + panel(1, "HARD WORK", "Reps build results", lifter())
         + panel(2, "FOCUS", "One goal, zero noise", meditator()) + panel(3, "CURIOSITY", "Always testing ideas", researcher()))
    save("traits.svg", 900, 280, b)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    skills(); performance(); stats(); idcard(); build(); traits()
    print("done")
