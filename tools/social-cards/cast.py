"""The recurring comic cast, drawn as SVG so every pose renders the same way every time.

- sprout(): Corey's mascot, the green sprout (getcorey.ai/corey-sprout.png). One Corey in
  different roles, never a crew of characters (Kristian, 26/10/2026).
- phoney(): Presso Events' mascot, the blue phone with the arrow logo (presso.events/mascot.png).
- robots: Kristian's two comic robots live in scenes.robot().

Each takes a mood and a pose, so a strip can tell a story with one character:
  moods: happy, grin, shock, worried, smug, think, sad, wink
  poses: none, wave, point, shrug, hold, cheer

Every function returns an <svg> sized by `w`; the drawing sits in its own viewBox, so a
character drops into any panel without coordinates.
"""

INK_CO = "#22361a"
INK_PE = "#0d1b47"


def _eyes(lx, rx, y, mood, ink, r=15):
    """Two eyes at (lx, y) and (rx, y). Mood changes their shape, not their place."""
    if mood == "smug":
        return (f'<path d="M{lx-16},{y} q16,-10 32,0" fill="none" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>'
                f'<path d="M{rx-16},{y} q16,-10 32,0" fill="none" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>')
    if mood == "wink":
        return (f'<ellipse cx="{lx}" cy="{y}" rx="{r-2}" ry="{r+3}" fill="{ink}"/><circle cx="{lx+5}" cy="{y-6}" r="5" fill="#fff"/>'
                f'<path d="M{rx-16},{y+2} q16,10 32,0" fill="none" stroke="{ink}" stroke-width="8" stroke-linecap="round"/>')
    if mood == "think":
        return (f'<ellipse cx="{lx}" cy="{y}" rx="{r-2}" ry="{r+3}" fill="{ink}"/><circle cx="{lx+4}" cy="{y-10}" r="5" fill="#fff"/>'
                f'<ellipse cx="{rx}" cy="{y}" rx="{r-2}" ry="{r+3}" fill="{ink}"/><circle cx="{rx+4}" cy="{y-10}" r="5" fill="#fff"/>')
    big = mood == "shock"
    ry = r + (8 if big else 3)
    rx_ = r + (3 if big else -2)
    out = ""
    for x in (lx, rx):
        if big:
            out += f'<ellipse cx="{x}" cy="{y}" rx="{rx_+4}" ry="{ry+4}" fill="#fff" stroke="{ink}" stroke-width="5"/>'
            out += f'<circle cx="{x}" cy="{y+2}" r="{r-5}" fill="{ink}"/>'
        else:
            out += f'<ellipse cx="{x}" cy="{y}" rx="{rx_}" ry="{ry}" fill="{ink}"/><circle cx="{x+5}" cy="{y-6}" r="5" fill="#fff"/>'
    if mood in ("worried", "sad"):
        out += (f'<path d="M{lx-18},{y-28} l26,-8" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
                f'<path d="M{rx+18},{y-28} l-26,-8" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>')
    return out


def _mouth(cx, y, mood, ink, tongue="#e8606a"):
    if mood in ("happy", "wink"):
        return f'<path d="M{cx-22},{y} q22,20 44,0" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'
    if mood == "grin":
        return (f'<path d="M{cx-30},{y-4} q30,44 60,0 z" fill="{ink}" stroke="{ink}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M{cx-14},{y+14} q14,12 28,0" fill="{tongue}"/>')
    if mood == "shock":
        return f'<ellipse cx="{cx}" cy="{y+8}" rx="14" ry="18" fill="{ink}"/>'
    if mood == "worried":
        return f'<path d="M{cx-24},{y+6} q8,-8 16,0 q8,8 16,0 q8,-8 16,0" fill="none" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>'
    if mood == "sad":
        return f'<path d="M{cx-20},{y+12} q20,-16 40,0" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'
    if mood == "smug":
        return f'<path d="M{cx-18},{y+4} q24,14 40,-6" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'
    if mood == "think":
        return f'<path d="M{cx-12},{y+6} h26" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'
    return f'<path d="M{cx-22},{y} q22,20 44,0" fill="none" stroke="{ink}" stroke-width="7" stroke-linecap="round"/>'


def _extras(mood, x, y, ink):
    """Sweat drop, thought dots or sparkles, drawn beside the head."""
    if mood == "worried":
        return f'<path d="M{x},{y} q-12,20 0,26 q12,-6 0,-26z" fill="#7cc4f5" stroke="{ink}" stroke-width="4"/>'
    if mood == "think":
        return "".join(f'<circle cx="{x+i*16}" cy="{y-i*18}" r="{5+i*3}" fill="#fff" stroke="{ink}" stroke-width="4"/>' for i in range(3))
    if mood in ("grin", "happy", "wink"):
        return ""
    if mood == "shock":
        return (f'<path d="M{x},{y-20} l-8,-26 M{x+20},{y-14} l8,-24 M{x+34},{y} l22,-10" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>')
    return ""


# ------------------------------------------------------------------ Corey: the sprout --------

def sprout(mood="happy", pose="none", w=260, h=None):
    ink = INK_CO
    leaf_l = (f'<path d="M150,108 C126,52 70,22 26,40 C30,92 86,124 150,108 Z" fill="#9fd04c" stroke="{ink}" stroke-width="8" stroke-linejoin="round"/>'
              f'<path d="M146,104 C116,78 82,60 46,52" fill="none" stroke="#6f9e2c" stroke-width="5" stroke-linecap="round"/>')
    leaf_r = (f'<path d="M150,108 C174,52 230,22 274,40 C270,92 214,124 150,108 Z" fill="#9fd04c" stroke="{ink}" stroke-width="8" stroke-linejoin="round"/>'
              f'<path d="M154,104 C184,78 218,60 254,52" fill="none" stroke="#6f9e2c" stroke-width="5" stroke-linecap="round"/>')
    if pose == "cheer":
        leaf_l = f'<g transform="rotate(-14 150 108)">{leaf_l}</g>'
        leaf_r = f'<g transform="rotate(14 150 108)">{leaf_r}</g>'
    body = (f'<ellipse cx="150" cy="212" rx="118" ry="96" fill="#94c843" stroke="{ink}" stroke-width="8"/>'
            f'<path d="M58,250 q92,70 184,0 q-20,52 -92,56 q-72,-4 -92,-56z" fill="#7db034" opacity=".55"/>'
            f'<ellipse cx="104" cy="168" rx="26" ry="12" fill="#c9e88f" opacity=".7"/>')
    face = (_eyes(112, 188, 206, mood, ink)
            + _mouth(150, 248, mood, ink)
            + '<ellipse cx="88" cy="240" rx="14" ry="8" fill="#f2a1a1" opacity=".55"/>'
            + '<ellipse cx="212" cy="240" rx="14" ry="8" fill="#f2a1a1" opacity=".55"/>')
    arms = _sprout_arms(pose, ink)
    extra = _extras(mood, 262, 150, ink)
    size = f'height="{h}"' if h else f'width="{w}"'
    return (f'<svg viewBox="-40 0 400 320" {size} xmlns="http://www.w3.org/2000/svg">'
            f'{arms[0]}{leaf_l}{leaf_r}<path d="M150,112 v-6" stroke="{ink}" stroke-width="8"/>{body}{face}{arms[1]}{extra}</svg>')


def _sprout_arms(pose, ink):
    """Little leaf arms. Returns (behind, in-front) layers."""
    def arm(path):
        return f'<path d="{path}" fill="#94c843" stroke="{ink}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>'
    if pose == "wave":
        return "", arm("M262,206 q36,-40 30,-88 q-24,8 -22,40 q-6,24 -26,34z")
    if pose == "point":
        return "", arm("M262,214 q48,-6 84,-26 q-6,-14 -22,-10 q-30,14 -62,10z")
    if pose == "shrug":
        return "", arm("M38,210 q-34,-10 -44,-44 q16,0 24,18 q12,14 26,10z") + arm("M262,210 q34,-10 44,-44 q-16,0 -24,18 q-12,14 -26,10z")
    if pose == "hold":
        return "", arm("M60,262 q-20,28 4,40 q18,-4 26,-24z") + arm("M240,262 q20,28 -4,40 q-18,-4 -26,-24z")
    if pose == "cheer":
        return "", arm("M42,200 q-40,-30 -36,-80 q20,4 18,34 q4,26 26,30z") + arm("M258,200 q40,-30 36,-80 q-20,4 -18,34 q-4,26 -26,30z")
    return "", ""


# ------------------------------------------------------------------ Presso Events: the phone --

def phoney(mood="happy", pose="none", w=230, h=None):
    ink = INK_PE
    blue, light = "#1f56d6", "#3b74f0"

    def limb(d, sw=22):
        return (f'<path d="{d}" fill="none" stroke="{ink}" stroke-width="{sw+10}" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<path d="{d}" fill="none" stroke="{blue}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')
    left = {"wave": "M74,190 q-40,-20 -46,-70", "shrug": "M74,190 q-40,-6 -50,-40",
            "point": "M74,200 q-34,24 -40,62", "hold": "M74,220 q-24,30 6,54",
            "cheer": "M74,180 q-36,-40 -30,-96"}.get(pose, "M74,200 q-34,24 -40,62")
    right = {"wave": "M226,180 q48,-30 46,-96", "shrug": "M226,190 q40,-6 50,-40",
             "point": "M226,200 q60,-10 100,-26", "hold": "M226,220 q24,30 -6,54",
             "cheer": "M226,180 q36,-40 30,-96"}.get(pose, "M226,200 q34,24 40,62")
    hands = ""
    for d in (left, right):
        end = d.split()[-1]
        # end point of a relative quad: start + last pair
        sx, sy = [float(v) for v in d.split()[0][1:].split(",")]
        dx, dy = [float(v) for v in end.split(",")]
        hands += f'<circle cx="{sx+dx}" cy="{sy+dy}" r="17" fill="{blue}" stroke="{ink}" stroke-width="6"/>'
    legs = limb("M120,346 v34", 26) + limb("M180,346 v34", 26)
    feet = (f'<ellipse cx="112" cy="392" rx="32" ry="16" fill="{blue}" stroke="{ink}" stroke-width="6"/>'
            f'<ellipse cx="188" cy="392" rx="32" ry="16" fill="{blue}" stroke="{ink}" stroke-width="6"/>')
    body = (f'<rect x="70" y="40" width="160" height="310" rx="36" fill="{ink}"/>'
            f'<rect x="80" y="50" width="140" height="290" rx="28" fill="{blue}"/>'
            f'<rect x="90" y="62" width="120" height="266" rx="20" fill="{light}"/>'
            f'<rect x="128" y="70" width="44" height="10" rx="5" fill="{ink}"/>'
            f'<path d="M112,96 q20,-14 46,-8" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".5"/>'
            # the arrow logo, simplified
            f'<path d="M128,284 l40,-24 v44 l-14,8 v-26 l-26,16z" fill="#fff"/><path d="M128,292 l20,-12 v34 l-20,12z" fill="#fff" opacity=".9"/>')
    face = _eyes(128, 172, 170, mood, ink, r=13) + _mouth(150, 214, mood, ink)
    extra = _extras(mood, 246, 110, ink)
    size = f'height="{h}"' if h else f'width="{w}"'
    return (f'<svg viewBox="-30 0 400 420" {size} xmlns="http://www.w3.org/2000/svg">'
            f'{legs}{feet}{limb(left)}{limb(right)}{hands}{body}{face}{extra}</svg>')


CAST = {"co": sprout, "pe": phoney}


def character(brand, mood="happy", pose="none", w=260, h=None):
    if brand in CAST:
        return CAST[brand](mood, pose, w, h)
    import scenes as S
    colour = "#3b82f6" if mood in ("happy", "smug", "think", "wink") else "#d9774f"
    size = f'height="{h}"' if h else f'width="{w}"'
    return f'<svg viewBox="-10 -4 180 270" {size}>{S.robot(0, 0, colour, "smile" if mood != "think" else "flat")}</svg>'
