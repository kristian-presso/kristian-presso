"""Hand-coded SVG scenes for carousel slides.

Drawn once in code, so a scene is identical on every render: no generated art, no invented
figures. Colours come from CSS variables on the slide (--ink, --acc, --hi, --soft, --ok), so one
drawing serves every brand. Every scene uses viewBox 0 0 900 460 unless noted.

Rules from the social-visuals standard: the picture carries the answer; no figures or numbers that
are not in the post; brands without a character master (Presso Events, Corey) get objects, never a
mascot. Kristian's own comics use the two robots below, which are his existing characters.
"""

STYLE = """
.k{stroke:var(--ink);stroke-width:6;stroke-linejoin:round;stroke-linecap:round}
.k4{stroke:var(--ink);stroke-width:4;stroke-linejoin:round;stroke-linecap:round}
.fa{fill:var(--acc)}.fh{fill:var(--hi)}.fs{fill:var(--soft)}.fw{fill:#fff}.fn{fill:none}.fi{fill:var(--ink)}
.fo{fill:var(--ok)}.fg{fill:#ddd7c8}.fr{fill:#d7263d}.sr{stroke:#d7263d}
.t{font-family:Inter,sans-serif;font-weight:800;fill:var(--ink)}
.m{font-family:'IBM Plex Mono',monospace;font-weight:600;fill:var(--ink)}
.tw{fill:#fff}
"""


def svg(body, vb="0 0 900 460"):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" preserveAspectRatio="xMidYMid meet">{body}</svg>'


def phone(x, y, w=240, h=420, inner=""):
    """A phone at (x, y). `inner` is drawn in screen coordinates (0,0 = top-left of the screen)."""
    sx, sy, sw = x + 14, y + 40, w - 28
    return (f'<rect x="{x+8}" y="{y+8}" width="{w}" height="{h}" rx="34" class="fi"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" class="fi k"/>'
            f'<rect x="{sx}" y="{sy}" width="{sw}" height="{h-80}" rx="14" class="fw"/>'
            f'<rect x="{x+w/2-28}" y="{y+16}" width="56" height="10" rx="5" class="fw"/>'
            f'<g transform="translate({sx},{sy})">{inner}</g>')


def bubble(x, y, w, h, text, cls="fw", tcls="t", size=22, tail="left", lines=None):
    tx = x + 28 if tail == "left" else x + w - 52
    tail_path = f'M{tx},{y+h-2} l0,26 l24,-26 z'
    rows = lines or [text]
    t = "".join(f'<text x="{x+18}" y="{y+16+size+i*(size+8)}" class="{tcls}" font-size="{size}">{r}</text>' for i, r in enumerate(rows))
    return (f'<path d="{tail_path}" class="{cls} k4"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" class="{cls} k4"/>'
            f'<path d="M{tx+3},{y+h-3} l0,0 l18,0" class="{cls}" stroke-width="8" stroke="currentColor" style="stroke:var(--tmp,transparent)"/>'
            + t)


def envelope(x, y, w=300, h=200, code="7HK-2M9"):
    return (f'<rect x="{x+8}" y="{y+8}" width="{w}" height="{h}" class="fi"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="fw k"/>'
            f'<path d="M{x},{y} L{x+w/2},{y+h*0.42} L{x+w},{y}" class="fn k"/>'
            f'<text x="{x+w/2}" y="{y+h*0.66}" text-anchor="middle" class="m" font-size="18">YOUR TICKET</text>'
            f'<rect x="{x+w/2-110}" y="{y+h*0.72}" width="220" height="44" class="fs k4" stroke-dasharray="8 6"/>'
            f'<text x="{x+w/2}" y="{y+h*0.72+33}" text-anchor="middle" class="m" font-size="30">{code}</text>')


def arrow(x1, y, x2):
    return (f'<path d="M{x1},{y} L{x2},{y}" class="fn k" stroke-width="8"/>'
            f'<path d="M{x2-22},{y-18} L{x2+4},{y} L{x2-22},{y+18}" class="fn k" stroke-width="8"/>')


def cross(cx, cy, r=70):
    return (f'<path d="M{cx-r},{cy-r} L{cx+r},{cy+r} M{cx+r},{cy-r} L{cx-r},{cy+r}" class="fn sr" stroke-width="18" stroke-linecap="round"/>')


def tick(cx, cy, s=1.0, cls="sw"):
    return f'<path d="M{cx-22*s},{cy} L{cx-6*s},{cy+16*s} L{cx+24*s},{cy-18*s}" fill="none" stroke="#fff" stroke-width="{9*s}" stroke-linecap="round" stroke-linejoin="round"/>'


def lock(cx, cy, s=1.0):
    return (f'<path d="M{cx-14*s},{cy-4*s} v-12 a14,14 0 0 1 {28*s},0 v12" class="fn k4"/>'
            f'<rect x="{cx-22*s}" y="{cy-6*s}" width="{44*s}" height="{34*s}" rx="6" class="fi k4"/>')


def robot(x, y, colour, mood="smile", s=1.0):
    """Kristian's comic robots. mood: smile (the eager one), flat (the one that asks)."""
    mouth = (f'<path d="M{x+44*s},{y+150*s} q36,{24*s} 72,0" class="fn k" stroke-width="{7*s}"/>' if mood == "smile"
             else f'<path d="M{x+56*s},{y+152*s} h48" class="fn k" stroke-width="{7*s}"/>')
    return (f'<path d="M{x+80*s},{y+62*s} v-34" class="fn k" stroke-width="{6*s}"/>'
            f'<circle cx="{x+80*s}" cy="{y+22*s}" r="{12*s}" fill="#fdd23e" class="k4"/>'
            f'<rect x="{x}" y="{y+62*s}" width="{160*s}" height="{124*s}" rx="{24*s}" fill="{colour}" class="k"/>'
            f'<circle cx="{x+50*s}" cy="{y+112*s}" r="{12*s}" class="fi"/><circle cx="{x+110*s}" cy="{y+112*s}" r="{12*s}" class="fi"/>'
            + mouth +
            f'<rect x="{x+28*s}" y="{y+186*s}" width="{104*s}" height="{70*s}" rx="{14*s}" fill="{colour}" class="k"/>')


# ------------------------------------------------------------ Presso Events: check-in myths ---

def pe_app():
    chat = ('<rect x="10" y="30" width="180" height="88" rx="16" class="fs"/>'
            '<text x="24" y="66" class="t" font-size="24">Check in</text><text x="24" y="100" class="m" font-size="24">7HK-2M9</text>'
            '<rect x="22" y="146" width="180" height="88" rx="16" class="fa"/>'
            '<text x="36" y="182" class="t tw" font-size="24">Checked in.</text><text x="36" y="216" class="t tw" font-size="24">Welcome!</text>')
    return svg(envelope(60, 140) + arrow(400, 240, 500) + phone(560, 10, inner=chat)
               + '<text x="210" y="410" text-anchor="middle" class="m" font-size="20">IN THEIR INBOX</text>'
               + '<text x="680" y="458" text-anchor="middle" class="m" font-size="20">IN YOUR HAND</text>')


def pe_scanner():
    gun = ('<g transform="translate(60,90)" opacity=".55">'
           '<path d="M0,40 h220 a30,30 0 0 1 30,30 v40 a30,30 0 0 1 -30,30 h-120 l-30,140 h-70 l20,-140 h-20 a30,30 0 0 1 -30,-30 v-40 a30,30 0 0 1 30,-30z" class="fg k"/>'
           '<rect x="250" y="60" width="26" height="60" class="fi"/>'
           '<path d="M276,70 l90,-30 M276,90 l100,0 M276,110 l90,30" class="fn sr" stroke-width="5" stroke-dasharray="10 8"/></g>')
    scan = ('<path d="M30,60 v-30 h30 M152,30 h30 v30 M182,170 v30 h-30 M60,200 h-30 v-30" class="fn k" stroke-width="7"/>'
            '<rect x="44" y="60" width="124" height="110" class="fs k4"/>'
            '<text x="106" y="124" text-anchor="middle" class="m" font-size="21">7HK-2M9</text>'
            '<rect x="10" y="240" width="192" height="70" rx="16" class="fa"/><text x="106" y="285" text-anchor="middle" class="t tw" font-size="26">Checked in</text>')
    return svg(gun + cross(200, 230, 110) + phone(600, 20, inner=scan)
               + '<text x="200" y="440" text-anchor="middle" class="m" font-size="20">HIRE, CHARGE, RETURN</text>')


def pe_signal():
    bars = "".join(f'<rect x="{30+i*26}" y="{90-i*20}" width="18" height="{30+i*20}" rx="3" class="fg k4"/>' for i in range(4))
    nosig = (bars + cross(80, 80, 46) +
             '<text x="106" y="200" text-anchor="middle" class="t" font-size="30">No signal</text>'
             '<text x="106" y="236" text-anchor="middle" class="m" font-size="20">(it happens)</text>')
    return svg(phone(50, 20, w=230, inner=nosig) + arrow(300, 230, 380)
               + envelope(430, 110, w=400, h=250)
               + '<rect x="560" y="390" width="150" height="50" rx="25" class="fo k4"/><text x="635" y="423" text-anchor="middle" class="t" font-size="20">still works</text>')


def pe_twice():
    def row(y, reply, cls, txtcls, mark):
        return (f'<rect x="20" y="{y}" width="340" height="100" rx="20" class="fs k4"/>'
                f'<text x="44" y="{y+62}" class="t" font-size="30">Check in </text><text x="196" y="{y+62}" class="m" font-size="30">7HK-2M9</text>'
                f'<rect x="390" y="{y}" width="490" height="100" rx="20" class="{cls} k4"/>'
                f'<text x="416" y="{y+62}" class="t {txtcls}" font-size="31">{mark} {reply}</text>')
    return svg('<text x="20" y="50" class="m" font-size="24">FIRST SCAN</text>' + row(70, "Checked in. Welcome!", "fa", "tw", "✓")
               + '<text x="20" y="280" class="m" font-size="24">SAME CODE AGAIN</text>' + row(300, "Already used, at 18:42", "fh", "", "!"))


def pe_free():
    def ticket(x, label, cls):
        return (f'<g transform="translate({x},70) rotate({-4 if x < 300 else 4} 170 150)">'
                f'<path d="M8,8 h340 v100 a28,28 0 0 0 0,56 v100 h-340 v-100 a28,28 0 0 0 0,-56z" class="fi"/>'
                f'<path d="M0,0 h340 v100 a28,28 0 0 0 0,56 v100 h-340 v-100 a28,28 0 0 0 0,-56z" class="{cls} k"/>'
                f'<text x="170" y="80" text-anchor="middle" class="t" font-size="48">{label}</text>'
                f'<rect x="60" y="150" width="220" height="50" class="fw k4" stroke-dasharray="8 6"/>'
                f'<text x="170" y="186" text-anchor="middle" class="m" font-size="28">CODE ✓</text></g>')
    return svg(ticket(70, "PAID", "fs") + ticket(480, "FREE", "fo")
               + '<text x="450" y="450" text-anchor="middle" class="m" font-size="20">SAME DOOR, SAME CHECK-IN</text>')


def pe_moral():
    door = ('<rect x="330" y="60" width="240" height="390" class="fw k"/>'
            '<rect x="350" y="80" width="200" height="370" class="fs k4"/>'
            '<circle cx="520" cy="270" r="12" class="fi"/>')
    clock = ('<circle cx="170" cy="190" r="110" class="fw k"/><circle cx="170" cy="190" r="8" class="fi"/>'
             '<path d="M170,190 L170,104 M170,190 L118,158" class="fn k" stroke-width="9"/>'
             '<text x="170" y="350" text-anchor="middle" class="m" font-size="28">6:58PM</text>')
    return svg(clock + door + phone(650, 90, w=170, h=320,
               inner='<rect x="14" y="80" width="114" height="60" rx="14" class="fa"/><text x="71" y="118" text-anchor="middle" class="t tw" font-size="20">✓ In</text>'))


# ------------------------------------------------------------ Corey: what it is not ---

def co_person():
    doc = ('<rect x="208" y="48" width="380" height="400" class="fi"/>'
           '<rect x="200" y="40" width="380" height="400" class="fw k"/>'
           '<text x="390" y="100" text-anchor="middle" class="t" font-size="34">CONTRACT</text>'
           + "".join(f'<rect x="240" y="{130+i*34}" width="{300 - (i % 2) * 70}" height="12" rx="6" class="fg"/>' for i in range(5))
           + '<path d="M240,370 h300" class="fn k4"/><text x="240" y="405" class="m" font-size="20">SIGNED: YOU</text>')
    pen = ('<g transform="rotate(35 660 230)"><rect x="640" y="90" width="40" height="230" rx="8" class="fh k"/>'
           '<path d="M640,320 L660,370 L680,320z" class="fw k4"/></g>')
    tag = ('<rect x="630" y="370" width="240" height="70" rx="12" class="fs k4"/>'
           '<text x="750" y="402" text-anchor="middle" class="t" font-size="20">AI: no liability,</text>'
           '<text x="750" y="428" text-anchor="middle" class="t" font-size="20">no signature</text>')
    return svg(doc + pen + tag)


def co_autopilot():
    def btn(x, label, mine):
        cls = "fo" if mine else "fg"
        b = (f'<rect x="{x+7}" y="167" width="150" height="190" rx="18" class="fi"/>'
             f'<rect x="{x}" y="160" width="150" height="190" rx="18" class="{cls} k"/>'
             f'<text x="{x+75}" y="225" text-anchor="middle" class="t" font-size="30">{label}</text>')
        b += (f'<path d="M{x+45},{285} l20,20 l40,-42" fill="none" stroke="var(--ink)" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>'
              if mine else lock(x + 75, 290, 1.3))
        return b
    return svg('<text x="190" y="100" text-anchor="middle" class="t" font-size="34">I do</text>'
               '<path d="M30,125 h310" class="fn k"/>'
               '<text x="640" y="100" text-anchor="middle" class="t" font-size="34">You do</text>'
               '<path d="M380,125 h480" class="fn k"/>'
               + btn(30, "Compute", True) + btn(190, "Draft", True)
               + btn(380, "Send", False) + btn(540, "Pay", False) + btn(700, "Sign", False))


def co_model():
    def chip(x):
        return (f'<rect x="{x+8}" y="148" width="200" height="200" rx="20" class="fi"/>'
                f'<rect x="{x}" y="140" width="200" height="200" rx="20" class="fs k"/>'
                f'<text x="{x+100}" y="252" text-anchor="middle" class="t" font-size="38">Claude</text>'
                + "".join(f'<path d="M{x+30+i*35},140 v-24 M{x+30+i*35},340 v24" class="fn k4"/>' for i in range(5)))
    tags = "".join(f'<rect x="690" y="{90+i*100}" width="180" height="64" rx="12" class="fa k4"/>'
                   f'<text x="780" y="{132+i*100}" text-anchor="middle" class="t tw" font-size="26">{t}</text>' for i, t in enumerate(["facts", "method", "limits"]))
    return svg(chip(40) + '<text x="310" y="270" text-anchor="middle" class="t" font-size="90">=</text>' + chip(400)
               + tags + '<path d="M600,240 h86" class="fn k4" stroke-dasharray="8 8"/>'
               + '<text x="140" y="430" text-anchor="middle" class="m" font-size="20">YOURS</text>'
               + '<text x="500" y="430" text-anchor="middle" class="m" font-size="20">MINE</text>')


def co_accountant():
    folder = ('<path d="M68,128 h120 l30,30 h250 v270 h-400z" class="fi"/>'
              '<path d="M60,120 h120 l30,30 h250 v270 h-400z" class="fh k"/>'
              '<text x="260" y="230" text-anchor="middle" class="t" font-size="36">Working file</text>'
              + "".join(f'<rect x="{100+i*120}" y="270" width="104" height="44" rx="8" class="fw k4"/>'
                        f'<text x="{152+i*120}" y="300" text-anchor="middle" class="m" font-size="17">{t}</text>' for i, t in enumerate(["VAT", "YEAR END", "LEDGER"])))
    desk = ('<rect x="640" y="150" width="220" height="200" rx="18" class="fs k"/>'
            '<text x="750" y="235" text-anchor="middle" class="t" font-size="28">Your</text>'
            '<text x="750" y="270" text-anchor="middle" class="t" font-size="28">accountant</text>')
    return svg(folder + arrow(500, 250, 610) + desk)


def co_skill():
    rows = "".join(f'<g opacity="{1 - i*0.2}"><rect x="40" y="{60+i*110}" width="400" height="80" rx="18" class="fg k4"/>'
                   f'<text x="64" y="{98+i*110}" class="m" font-size="17">{d}</text>'
                   f'<text x="64" y="{124+i*110}" class="t" font-size="20">"Here\'s how we do our VAT..."</text></g>'
                   for i, d in enumerate(["MONDAY", "THE MONDAY AFTER", "THE ONE AFTER THAT"]))
    card = ('<rect x="568" y="108" width="300" height="250" rx="18" class="fi"/>'
            '<rect x="560" y="100" width="300" height="250" rx="18" class="fo k"/>'
            '<text x="710" y="170" text-anchor="middle" class="m" font-size="22">SKILL</text>'
            '<text x="710" y="225" text-anchor="middle" class="t" font-size="30">Written once.</text>'
            '<text x="710" y="268" text-anchor="middle" class="t" font-size="30">Kept.</text>')
    return svg(rows + arrow(460, 225, 530) + card)


def co_moral():
    shield = ('<path d="M458,48 l170,60 v120 c0,120 -90,190 -170,220 c-80,-30 -170,-100 -170,-220 v-120z" class="fi"/>'
              '<path d="M450,40 l170,60 v120 c0,120 -90,190 -170,220 c-80,-30 -170,-100 -170,-220 v-120z" class="fw k"/>'
              '<path d="M385,240 l45,45 l90,-95" fill="none" stroke="var(--acc)" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
    return svg(shield)
