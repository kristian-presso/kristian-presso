"""LinkedIn carousels (document posts), one panel per slide.

    python3 carousel.py                 # every carousel in CAROUSELS
    python3 carousel.py pe-6-myths      # just one

Two looks:
- Rhythm (Presso Events, Corey): the make.py brand tokens, with comic devices - the myth is a
  speech bubble, the scene is drawn (scenes.py), the fact is a caption box.
- Comic (Kristian): the strip look of his LinkedIn infographics - yellow header block, Inter
  Black, thick frames with offset shadows, the two robots, tick and cross tiles, chips.

Writes, per carousel, into this folder:
  <key>.pdf        the document LinkedIn shows as a swipeable carousel (one 1080x1350 page per slide)
  <key>-cover.png  slide one at 2160x2700, quantised and look-tagged by finish.py, used as the
                   Buffer document thumbnail and as the stand-alone fallback card

Rules (Corey social-visuals standard, 22/10/2026):
- Slide one has to work alone. Most people never swipe, so the cover states the whole claim.
- One idea per slide, and the picture carries it. Never a paragraph.
- No URL, logo or call to action on any slide. The post text does the selling.
"""
import os, sys, html
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish  # noqa: E402
import scenes as S  # noqa: E402
from make import BRANDS, CSS  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

# ------------------------------------------------------------------ Rhythm look ------------

RHYTHM_CSS = """
body{padding:64px 70px 46px}
.cnt{display:flex;justify-content:space-between;align-items:center;margin-top:24px;
 font-family:'IBM Plex Mono',monospace;font-size:20px;font-weight:600;letter-spacing:3px;color:#555}
.cnt .sw{color:var(--acc)}
.dots{background-color:#fff;background-image:radial-gradient(var(--soft) 2.2px,transparent 2.8px);background-size:22px 22px}
.frame{border:5px solid var(--ink);box-shadow:9px 9px 0 var(--ink)}
/* speech bubble */
.bub{position:relative;background:#fff;border:5px solid var(--ink);border-radius:36px;padding:30px 40px 34px;
 font-size:56px;font-weight:800;line-height:1.12;letter-spacing:-.5px;color:#2e2e2e;box-shadow:9px 9px 0 var(--ink);margin:0 70px 50px 0}
.bub:before{content:"";position:absolute;left:70px;bottom:-46px;border-right:52px solid transparent;border-top:46px solid var(--ink)}
.bub:after{content:"";position:absolute;left:75px;bottom:-33px;border-right:36px solid transparent;border-top:32px solid #fff}
.bub .who{display:block;font-family:'IBM Plex Mono',monospace;font-size:20px;font-weight:600;letter-spacing:3px;color:#777;margin-bottom:10px}
.stamp{position:absolute;right:-46px;top:-34px;transform:rotate(9deg);border:7px solid #d7263d;color:#d7263d;background:var(--bg);
 font-family:Inter,sans-serif;font-weight:900;font-size:48px;letter-spacing:5px;padding:4px 20px}
/* drawn scene */
.scene{flex:1;min-height:0;padding:18px 20px;display:flex}
.scene svg{flex:1}
/* caption */
.cap{margin-top:30px;background:var(--acc);color:#fff;padding:20px 30px 26px;font-family:'Instrument Serif',serif;font-size:66px;line-height:1.02}
.cap .lab{display:block;font-family:'IBM Plex Mono',monospace;font-size:20px;font-weight:600;letter-spacing:4px;color:var(--soft);margin-bottom:8px}
/* cover chatter */
.chat{flex:1;min-height:0;padding:30px 34px 120px;display:flex;flex-direction:column;justify-content:space-around;position:relative}
.cb{position:relative;background:#fff;border:4px solid var(--ink);border-radius:26px;padding:12px 24px 14px;font-size:36px;font-weight:700;
 max-width:84%;align-self:flex-start;box-shadow:5px 5px 0 var(--ink)}
.cb:nth-child(even){align-self:flex-end}
.cb s{text-decoration:line-through;text-decoration-color:#d7263d;text-decoration-thickness:5px;color:#3a3a3a}
.chat .stamp{right:40px;top:auto;bottom:30px;font-size:46px;transform:rotate(-6deg)}
.verdict.c{margin-top:28px}
/* moral */
.moral2{flex:1;display:flex;flex-direction:column;background:var(--acc);color:#fff}
.moral2 .ph{background:var(--hi);color:var(--ink);border-bottom:5px solid var(--ink);padding:14px 24px;font-family:'IBM Plex Mono',monospace;font-size:22px;font-weight:600;letter-spacing:3px;text-transform:uppercase}
.moral2 .pic{margin:28px 28px 0;height:430px;border:4px solid var(--ink);display:flex;padding:14px}
.moral2 .pic svg{flex:1}
.moral2 .txt{flex:1;display:flex;align-items:center;padding:20px 36px 30px;font-family:'Instrument Serif',serif;font-size:84px;line-height:1.0}
"""


def rhythm_slide(brand, kick, title, body, n, total, swipe=False):
    b = BRANDS[brand]
    vars_ = f"--bg:{b['bg']};--ink:{b['ink']};--acc:{b['acc']};--hi:{b['hi']};--soft:{b['soft']};--ok:{b['ok']}"
    cnt = f'<div class="cnt"><span>{n:02d} / {total:02d}</span>{"<span class=sw>SWIPE &#8594;</span>" if swipe else ""}</div>'
    h1 = f"<h1>{title}</h1>" if title else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}{RHYTHM_CSS}{S.STYLE}</style></head>
<body><div class="bar"></div><div class="kick">{e(kick)}</div>{h1}
<div class="main">{body}</div>{cnt}</body></html>"""


def myth_carousel(brand, title, rows, moral, verdict, who="Overheard"):
    """rows: (myth, fact, scene_svg). Cover (the chatter, struck through) + one slide per myth + moral."""
    total = len(rows) + 2
    chatter = "".join(f'<div class="cb"><s>&ldquo;{m}&rdquo;</s></div>' for m, _, _ in rows)
    cover = (f'<div class="chat dots frame">{chatter}<div class="stamp">ALL MYTHS</div></div>'
             f'<div class="verdict c">{verdict}</div>')
    slides = [rhythm_slide(brand, "Myth vs fact", title, cover, 1, total, swipe=True)]
    for i, (m, f, pic) in enumerate(rows, 1):
        body = (f'<div class="bub"><span class="who">{e(who)}</span>&ldquo;{m}&rdquo;<div class="stamp">MYTH</div></div>'
                f'<div class="scene dots frame">{pic}</div>'
                f'<div class="cap frame"><span class="lab">FACT</span>{f}</div>')
        slides.append(rhythm_slide(brand, f"Myth {i} of {len(rows)}", "", body, i + 1, total))
    m_body, m_pic = moral
    end = (f'<div class="moral2 frame"><div class="ph">The moral</div>'
           f'<div class="pic dots">{m_pic}</div><div class="txt">{m_body}</div></div>')
    slides.append(rhythm_slide(brand, "Myth vs fact", "", end, total, total))
    return slides


# ------------------------------------------------------------------ Comic look (Kristian) --

KP = dict(bg="#f8f3e6", ink="#161616", yel="#fdd23e", red="#e5383b", grn="#2bb673", blu="#3b82f6",
          org="#d9774f", pale="#fff6cf")

COMIC_CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px}}
body{{--ink:{KP['ink']};--acc:{KP['blu']};--hi:{KP['yel']};--soft:{KP['pale']};--ok:{KP['grn']};
 background:{KP['bg']};color:var(--ink);font-family:Inter,sans-serif;padding:56px 56px 40px;display:flex;flex-direction:column;
 background-image:radial-gradient(rgba(0,0,0,.07) 1.4px,transparent 1.6px);background-size:18px 18px}}
.box{{border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);background:#fff}}
.hdr{{background:{KP['yel']};padding:40px 44px 40px}}
.kick{{font-weight:800;font-size:25px;letter-spacing:5px;text-transform:uppercase;margin-bottom:16px}}
.hdr h1{{font-weight:900;font-size:96px;line-height:.98;letter-spacing:-3px}}
.hdr p{{font-size:34px;font-weight:600;margin-top:18px;line-height:1.25}}
.pan{{flex:1;display:flex;flex-direction:column;min-height:0;margin-top:40px}}
.pan .ph{{padding:20px 30px;font-weight:900;font-size:40px;letter-spacing:1px;text-transform:uppercase;color:#fff;border-bottom:6px solid var(--ink)}}
.ph.red{{background:{KP['red']}}}.ph.grn{{background:{KP['grn']}}}.ph.ink{{background:var(--ink)}}.ph.yel{{background:{KP['yel']};color:var(--ink)}}
.pan .pb{{flex:1;display:flex;flex-direction:column;justify-content:space-evenly;padding:40px 44px;gap:30px;min-height:0}}
.you{{align-self:flex-start;border:5px solid var(--ink);border-radius:34px;padding:20px 36px;font-size:52px;box-shadow:7px 7px 0 var(--ink);font-weight:700;background:#fff}}
.you b{{font-weight:900}}
.row{{display:flex;align-items:center;gap:36px}}
.row svg{{flex:0 0 auto}}
.said{{font-size:52px;font-weight:700;line-height:1.22}}
.said b{{font-weight:900}}
.qb{{position:relative;flex:1;background:{KP['pale']};border:5px solid var(--ink);border-radius:30px;padding:28px 32px;font-size:44px;font-weight:700;line-height:1.22}}
.qb:before{{content:"";position:absolute;left:-36px;top:60px;border-top:22px solid transparent;border-bottom:22px solid transparent;border-right:36px solid var(--ink)}}
.qb u{{text-decoration-thickness:4px}}
.tiles{{display:flex;justify-content:space-between;gap:24px}}
.tile{{flex:1;text-align:center}}
.tile .sq{{height:300px;box-shadow:8px 8px 0 var(--ink);border:6px solid var(--ink);display:flex;align-items:center;justify-content:center;font-size:130px;font-weight:900;color:#fff}}
.tile .sq.ok{{background:{KP['grn']}}}.tile .sq.no{{background:{KP['red']}}}
.tile b{{display:block;font-size:44px;font-weight:900;margin-top:16px}}.tile span{{font-size:34px}}
.note{{background:var(--ink);color:#fff;padding:32px 38px;font-size:50px;font-weight:800;line-height:1.2}}
.note em{{font-style:normal;color:{KP['yel']}}}
.steps{{display:flex;flex-direction:column;gap:30px}}
.step{{display:flex;align-items:stretch;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink);background:#fff}}
.step .n{{background:var(--ink);color:#fff;font-weight:900;font-size:90px;width:150px;display:flex;align-items:center;justify-content:center}}
.step .s{{padding:34px 34px;font-size:54px;font-weight:900;line-height:1.12}}
.step .s span{{display:block;font-size:30px;font-weight:500;margin-top:8px;color:#333}}
.chips{{display:flex;flex-wrap:wrap;gap:20px}}
.chip{{border:5px solid var(--ink);box-shadow:6px 6px 0 var(--ink);background:#fff;padding:18px 28px;font-size:42px;font-weight:800}}
.chip.y{{background:{KP['pale']}}}
.lbl{{font-weight:900;font-size:28px;letter-spacing:5px;text-transform:uppercase}}
.bars{{display:flex;flex-direction:column;gap:18px}}
.bar2{{display:flex;align-items:center;gap:20px;font-size:38px;font-weight:800}}
.bar2 .tr{{flex:1;height:84px;border:5px solid var(--ink);background:#fff;position:relative}}
.bar2 .fl{{position:absolute;left:0;top:0;bottom:0}}
.bar2 .v{{width:130px;font-size:58px;font-weight:900;text-align:right}}
.big{{font-weight:900;font-size:230px;line-height:.9;letter-spacing:-5px}}
.big s{{text-decoration-color:{KP['red']};text-decoration-thickness:14px}}
.vs{{display:flex;flex-direction:column;gap:30px}}
.vs small{{display:block;font-size:40px;letter-spacing:0;font-weight:700;letter-spacing:0;margin-top:10px}}
.cnt{{display:flex;justify-content:space-between;margin-top:30px;font-weight:800;font-size:24px;letter-spacing:4px;color:#444}}
.mini{{display:grid;grid-template-columns:1fr 1fr;gap:34px;flex:1;margin-top:40px;min-height:0}}
.mini .box{{display:flex;flex-direction:column}}
.mini .ph{{padding:16px 22px;font-weight:900;font-size:30px;color:#fff;border-bottom:6px solid var(--ink)}}
.mini .pb{{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;padding:20px;text-align:center}}
.mini .pb p{{font-size:40px;font-weight:800;line-height:1.15}}
"""


def comic_slide(body, n, total, swipe=False):
    fonts = open(os.path.join(OUT, "fonts.css")).read()
    cnt = f'<div class="cnt"><span>{n} / {total}</span>{"<span>SWIPE &#8594;</span>" if swipe else ""}</div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts}{COMIC_CSS}{S.STYLE}</style></head>
<body>{body}{cnt}</body></html>"""


def bot(colour, mood, w=230):
    return f'<svg viewBox="-10 -4 180 270" width="{w}">{S.robot(0, 0, colour, mood)}</svg>'


def pushback_carousel():
    T = 7
    s = []
    s.append(comic_slide(
        '<div class="box hdr"><div class="kick">Before / after · the pushback skill</div>'
        '<h1>2 hours of perfect work. On the wrong brief.</h1><p>Same request. Two agents. One asks first.</p></div>'
        '<div class="mini">'
        f'<div class="box"><div class="ph" style="background:{KP["red"]}">BEFORE</div><div class="pb">{bot(KP["org"], "smile", 250)}<p>Guesses.<br>2 hours. Wrong thing.</p></div></div>'
        f'<div class="box"><div class="ph" style="background:{KP["grn"]}">AFTER</div><div class="pb">{bot(KP["blu"], "flat", 250)}<p>Asks one question.<br>10 seconds.</p></div></div>'
        '</div>', 1, T, swipe=True))
    s.append(comic_slide(
        '<div class="box pan"><div class="ph red">Before: no gate</div><div class="pb">'
        '<div class="you">You: <b>&ldquo;Update pricing.&rdquo;</b></div>'
        f'<div class="row">{bot(KP["org"], "smile", 340)}<div class="said">Picks the likeliest reading.<br>Works happily for <b>2 hours.</b><br>Reports success.</div></div>'
        '</div></div>', 2, T))
    s.append(comic_slide(
        '<div class="box pan"><div class="ph red">Before: what actually changed</div><div class="pb">'
        '<div class="tiles"><div class="tile"><div class="sq ok">&#10003;</div><b>Pricing page</b><span>updated</span></div>'
        '<div class="tile"><div class="sq no">&#10007;</div><b>Billing</b><span>old price</span></div>'
        '<div class="tile"><div class="sq no">&#10007;</div><b>Docs</b><span>a third price</span></div></div>'
        '<div class="note">Nothing broke. Every check passed. <em>It built the thing you didn\'t mean.</em></div>'
        '</div></div>', 3, T))
    s.append(comic_slide(
        '<div class="box pan"><div class="ph grn">After: pushback</div><div class="pb">'
        '<div class="you">You: <b>&ldquo;Update pricing.&rdquo;</b></div>'
        f'<div class="row">{bot(KP["blu"], "flat", 260)}<div class="qb">&ldquo;Update pricing&rdquo; touches 3 places: the site calculator, billing and the docs. Very different rollback costs. <u>Which one, or all three?</u></div></div>'
        '</div></div>', 4, T))
    s.append(comic_slide(
        '<div class="box pan"><div class="ph grn">After: the answer</div><div class="pb">'
        '<div class="you">You: <b>&ldquo;All three.&rdquo;</b></div>'
        '<div class="vs"><div class="big">10 sec<small>one message, answered</small></div>'
        '<div class="big" style="color:#9a9a9a"><s>2 hrs</s><small style="color:#333">the redo you skipped</small></div></div>'
        '</div></div>', 5, T))
    s.append(comic_slide(
        '<div class="lbl" style="margin-bottom:28px">The reply always has three lines</div><div class="steps" style="flex:1;justify-content:center">'
        '<div class="step"><div class="n">1</div><div class="s">What I think you meant</div></div>'
        '<div class="step"><div class="n">2</div><div class="s">The ambiguity, clash or risk</div></div>'
        '<div class="step"><div class="n">3</div><div class="s">One question, or one path with a yes/no</div></div>'
        '</div><div class="note" style="margin-top:44px">Say &ldquo;do it anyway&rdquo; and it does. <em>It logs one line saying it disagreed.</em></div>', 6, T))
    s.append(comic_slide(
        '<div style="flex:1;display:flex;flex-direction:column;justify-content:space-evenly"><div><div class="lbl" style="margin-bottom:28px">It only fires when the brief…</div>'
        '<div class="chips"><div class="chip">has 2+ readings</div><div class="chip">contradicts a decision</div>'
        '<div class="chip">costs &gt;30 min if wrong</div><div class="chip">skips a rule</div><div class="chip y">is fashion, not a problem</div></div>'
        '</div><div><div class="lbl" style="margin-bottom:28px">Claude on these test cases</div><div class="bars">'
        f'<div class="bar2"><span style="width:200px">Without</span><div class="tr"><div class="fl" style="width:65%;background:{KP["red"]}"></div></div><span class="v">0.65</span></div>'
        f'<div class="bar2"><span style="width:200px">With</span><div class="tr"><div class="fl" style="width:94%;background:{KP["grn"]}"></div></div><span class="v">0.94</span></div></div></div></div>'
        '<div class="box hdr" style="margin-top:20px;padding:34px 40px"><h1 style="font-size:66px;letter-spacing:-2px">A gate that fires on everything is worthless.</h1></div>',
        7, T))
    return s


# ------------------------------------------------------------------ the carousels ----------

CAROUSELS = {}

CAROUSELS["pe-6-myths"] = myth_carousel(
    "pe", "Five things organisers believe <em>about check-in</em>", [
        ("You need an event check-in app.", "You need a phone and a ticket code. Nothing to install on either side.", S.pe_app()),
        ("You need scanner hardware.", "The phone in your hand is the scanner.", S.pe_scanner()),
        ("No signal at the venue means no tickets.", "The code is inside the email itself, not behind a link.", S.pe_signal()),
        ("A ticket used twice gets in twice.", "The second check-in says it was already used, and shows when.", S.pe_twice()),
        ("Free events need a different process.", "A free ticket gets a check-in code like any other.", S.pe_free()),
    ],
    ("The best check-in app is the one nobody has to install, learn or find at 6:58pm.", S.pe_moral()),
    verdict="None of them is true. <em>Swipe for what actually happens.</em>", who="Heard before doors")

CAROUSELS["co-6-myths"] = myth_carousel(
    "co", "What an AI co-founder <em>is not</em>", [
        ("It's a person.", "It carries no liability and can't sign a contract.", S.co_person()),
        ("It's autopilot.", "It computes and drafts. Sending, paying and signing stay with you.", S.co_autopilot()),
        ("It's a smarter model.", "Same Claude you already have. If Claude were the bottleneck, it wouldn't help.", S.co_model()),
        ("It replaces your accountant.", "It's a well-kept working file you bring to them.", S.co_accountant()),
        ("You couldn't just ask Claude.", "You could. A skill is that typing, done once and kept.", S.co_skill()),
    ],
    ("The half people skip is the half that keeps you safe.", S.co_moral()),
    verdict="All five are wrong. <em>Swipe for what it actually is.</em>", who="People assume")

CAROUSELS["kp-pushback"] = pushback_carousel()


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
            print(f"{key} slide {i} OVERFLOWS ({sh}px)")
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
