"""LinkedIn carousels (document posts) in the same Rhythm look as make.py.

    python3 carousel.py                 # every carousel in CAROUSELS
    python3 carousel.py pe-6-myths      # just one

Writes, per carousel, into this folder:
  <key>.pdf        the document LinkedIn shows as a swipeable carousel (one 1080x1350 page per slide)
  <key>-cover.png  slide one at 2160x2700, quantised and look-tagged by finish.py, used as the
                   Buffer document thumbnail and as the stand-alone fallback card

Copy them to assets/social/<brand>/ on this branch with the usual week naming.

Rules (Corey social-visuals standard, 22/10/2026):
- Slide one has to work alone. Most people never swipe, so the cover states the whole claim.
- One idea per slide. Each slide is a strip panel, never a paragraph.
- No URL, logo or call to action on any slide. The post text does the selling.
"""
import os, sys, html
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish  # noqa: E402
from make import BRANDS, CSS  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

SLIDE_CSS = """
body{padding:64px 70px 50px}
.cnt{display:flex;justify-content:space-between;align-items:center;margin-top:26px;
 font-family:'IBM Plex Mono',monospace;font-size:20px;font-weight:600;letter-spacing:3px;color:#555}
.cnt .sw{color:var(--acc)}
/* cover */
.strip{border:4px solid var(--ink);background:#fff;box-shadow:8px 8px 0 var(--ink);flex:1;display:flex;flex-direction:column}
.strip .ph{background:var(--soft);border-bottom:4px solid var(--ink);padding:14px 22px;font-family:'IBM Plex Mono',monospace;
 font-size:21px;font-weight:600;letter-spacing:2px;text-transform:uppercase}
.strip ol{list-style:none;padding:6px 26px;flex:1;display:flex;flex-direction:column;justify-content:space-around}
.strip li{font-size:36px;line-height:1.25;padding:14px 0;border-bottom:2px dashed rgba(0,0,0,.22);display:flex;gap:18px;align-items:baseline}
.strip li:last-child{border-bottom:none}
.strip li .n{font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;color:var(--acc);min-width:34px}
.strip li s{text-decoration-color:#c8102e;text-decoration-thickness:4px;color:#3a3a3a}
.verdict.c{margin-top:26px}
/* myth slide */
.pair{flex:1;display:flex;flex-direction:column;gap:30px}
.pan{position:relative}
.pan .ph{font-size:23px}
.pan .pb{padding:34px 34px;display:flex;align-items:center}
.pan.m .pb{font-size:52px;line-height:1.2}
.pan.f .pb{font-family:'Instrument Serif',serif;font-size:96px;line-height:1;letter-spacing:-.5px}
.pan.m{background:#ebe6da}
.pan.m .ph{background:#d9d3c4}
.pan.m .pb{color:#4a4a4a}
.pan.f .ph{background:var(--acc);color:#fff}
.stamp{position:absolute;right:26px;bottom:22px;transform:rotate(-8deg);border:6px solid #c8102e;color:#c8102e;
 font-family:Inter,sans-serif;font-weight:900;font-size:46px;letter-spacing:4px;padding:4px 18px;background:rgba(255,255,255,.55)}
/* end slide */
.end{flex:1;display:flex}
.end .pan{flex:1}
.end .pan.moral .pb{font-size:92px;line-height:1.02;padding:44px 40px}
"""


def slide(brand, kick, title, body, n, total, swipe=False):
    b = BRANDS[brand]
    vars_ = f"--bg:{b['bg']};--ink:{b['ink']};--acc:{b['acc']};--hi:{b['hi']};--soft:{b['soft']};--ok:{b['ok']}"
    cnt = f'<div class="cnt"><span>{n:02d} / {total:02d}</span>{"<span class=sw>SWIPE &#8594;</span>" if swipe else ""}</div>'
    h1 = f"<h1>{title}</h1>" if title else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}{SLIDE_CSS}</style></head>
<body><div class="bar"></div><div class="kick">{e(kick)}</div>{h1}
<div class="main">{body}</div>{cnt}</body></html>"""


def myth_carousel(brand, title, rows, moral, cover_head="The five", verdict=None):
    """Cover (every myth, struck through, plus the verdict) + one slide per myth + a moral slide."""
    total = len(rows) + 2
    items = "".join(f'<li><span class="n">{i:02d}</span><s>{m}</s></li>' for i, (m, _) in enumerate(rows, 1))
    cover_body = f'<div class="strip"><div class="ph">{e(cover_head)}</div><ol>{items}</ol></div>'
    if verdict:
        cover_body += f'<div class="verdict c">{verdict}</div>'
    slides = [slide(brand, "Myth vs fact", title, cover_body, 1, total, swipe=True)]
    for i, (m, f) in enumerate(rows, 1):
        body = (f'<div class="pair">'
                f'<div class="pan m" style="flex:1"><div class="ph">What people believe</div>'
                f'<div class="pb">{m}</div><div class="stamp">MYTH</div></div>'
                f'<div class="pan f" style="flex:1.25"><div class="ph">What actually happens</div>'
                f'<div class="pb">{f}</div></div></div>')
        slides.append(slide(brand, f"Myth {i} of {len(rows)}", "", body, i + 1, total))
    end = f'<div class="end"><div class="pan moral"><div class="ph">The moral</div><div class="pb">{moral}</div></div></div>'
    slides.append(slide(brand, "Myth vs fact", "", end, total, total))
    return slides


CAROUSELS = {}

CAROUSELS["pe-6-myths"] = myth_carousel(
    "pe", "Five things organisers believe <em>about check-in</em>", [
        ("You need an event check-in app.", "You need a phone and a ticket code. Nothing to install on either side."),
        ("You need scanner hardware.", "The phone in your hand is the scanner."),
        ("No signal at the venue means no tickets.", "The code is inside the email itself, not behind a link."),
        ("A ticket used twice gets in twice.", "The second check-in says it was already used, and shows when."),
        ("Free events need a different process.", "A free ticket gets a check-in code like any other."),
    ],
    "The best check-in app is the one nobody has to install, learn or find at 6:58pm.",
    cover_head="Five beliefs", verdict="None of them is true. <em>Swipe for what actually happens.</em>")

CAROUSELS["co-6-myths"] = myth_carousel(
    "co", "What an AI co-founder <em>is not</em>", [
        ("It's a person.", "It carries no liability and can't sign a contract."),
        ("It's autopilot.", "It computes and drafts. Sending, paying and signing stay with you."),
        ("It's a smarter model.", "Same Claude you already have. If Claude were the bottleneck, it wouldn't help."),
        ("It replaces your accountant.", "It's a well-kept working file you bring to them."),
        ("You couldn't just ask Claude.", "You could. A skill is that typing, done once and kept."),
    ],
    "The half people skip is the half that keeps you safe.",
    cover_head="Five things people assume", verdict="All five are wrong. <em>Swipe for what it actually is.</em>")


def render(key, slides, br):
    pg = br.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
    writer = PdfWriter()
    for i, h in enumerate(slides, 1):
        path = os.path.join(OUT, f"{key}-s{i}.html")
        open(path, "w").write(h)
        pg.goto("file://" + path)
        pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
        sh = pg.evaluate("document.documentElement.scrollHeight")
        if sh > 1350:
            print(f"{key} slide {i} overflows ({sh}px)")
        png = os.path.join(OUT, f"{key}-s{i}.png")
        pg.screenshot(path=png)
        pdf = os.path.join(OUT, f"{key}-s{i}.pdf")
        pg.pdf(path=pdf, width="1080px", height="1350px", print_background=True, page_ranges="1")
        writer.append(PdfReader(pdf))
        if i == 1:
            finish.main([png, os.path.join(OUT, f"{key}-cover.png")])
    with open(os.path.join(OUT, f"{key}.pdf"), "wb") as fh:
        writer.write(fh)
    pg.close()
    print(key, len(slides), "slides ->", f"{key}.pdf")


if __name__ == "__main__":
    only = sys.argv[1:]
    with sync_playwright() as p:
        br = p.chromium.launch()
        for k, s in CAROUSELS.items():
            if only and k not in only:
                continue
            render(k, s, br)
        br.close()
