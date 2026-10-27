"""Comic carousels from a JSON spec: one story per post, one beat per slide, a mascot acting it out.

    python3 comic.py specs/<key>.json [more.json ...]
    python3 comic.py --check specs/<key>.json       # validate the spec only, render nothing

Why this exists (27/10/2026). Kristian's rule since 12-13/10/2026 is that every post on every
channel is a hook, a lesson, a laugh and a picture that teaches - a comic strip, or a toolkit card
people save. The weekly LinkedIn writer for Presso Events and Corey (19/10/2026) only had the
text-card layouts in make.py, so every post went out as a dense text card. This makes the comic
the default, as a LinkedIn carousel (document post), with the brand's own mascot as the cast:
Corey is the green sprout, Presso Events the blue phone, Kristian the two robots.

Writes into out/<key>/:
  <key>.pdf          the carousel LinkedIn shows (one 1080x1350 page per slide)
  cover.png          slide one at 2160x2700, quantised and tagged card-look:Comic (finish.py) -
                     the Buffer document thumbnail, and the card for a single-image fallback
  slide-<n>.png      every slide, finished and tagged, for X (up to 4 images per post)

SPEC
{
  "key": "co-2026-w45-1-story",          # file-safe, unique per post
  "brand": "co" | "pe" | "kp",
  "slides": [ ... 4 to 8 slides, the first must be "cover", the last should be "moral" ... ]
}
Slide types (text may use **bold**; nothing else is markup):
  cover   kicker, title, sub?, mood, pose?, say?          the whole claim on one slide: most people never swipe
  panel   label, caption, mood, pose?, say?, props?, note?   one beat of the story
  versus  title?, left{label,mood,text}, right{label,mood,text}
  list    label, items[{emoji,title,text?}] (2-5), mood?, pose?
  stat    big, caption, mood, source?
  myth    myth, fact, mood?
  moral   text, mood?, pose?, save?                        the line people quote, and "💾 Save this for ..."
moods: happy grin shock worried smug think sad wink.  poses: none wave point shrug hold cheer.
props: up to 3 emoji drawn big in the scene (☕ 💻 📱 🎟️ 🐛 📋 ⏰ 🔥 ...).

Rules carried from the social standard: no URL, logo or call to action on any slide; every fact
on a slide is in the post or its source; one idea per slide; the joke is on us or the machine.
"""
import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cast  # noqa: E402

MOODS = {"happy", "grin", "shock", "worried", "smug", "think", "sad", "wink"}
POSES = {"none", "wave", "point", "shrug", "hold", "cheer"}
TYPES = {"cover", "panel", "versus", "list", "stat", "myth", "moral"}
LOOK = "Comic"

THEME = {
    "pe": dict(bg="#f7f3ea", ink="#141414", acc="#1f56d6", hdr="#fde9a8", hi="#f39a2b", bad="#e5383b", ok="#2bb673", tint="#e4ecff", floor="#c9d7fb"),
    "co": dict(bg="#f2eee2", ink="#151515", acc="#4f7a24", hdr="#f8d75a", hi="#f07c22", bad="#e5383b", ok="#2bb673", tint="#eaf3d9", floor="#cfe3a8"),
    "kp": dict(bg="#f8f3e6", ink="#161616", acc="#3b82f6", hdr="#fdd23e", hi="#d9774f", bad="#e5383b", ok="#2bb673", tint="#fff6cf", floor="#f3df96"),
}

# Max characters per field. A slide that overflows is a slide nobody reads on a phone.
LIMITS = {"title": 70, "kicker": 40, "sub": 110, "say": 90, "caption": 120, "note": 110, "label": 32,
          "text": 120, "big": 12, "myth": 70, "fact": 110, "save": 60, "emoji": 4, "source": 90}


def fmt(s):
    s = html.escape(s or "")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{background:var(--bg);color:var(--ink);font-family:Inter,'Noto Color Emoji',sans-serif;padding:56px 56px 40px;display:flex;flex-direction:column;
 background-image:radial-gradient(rgba(0,0,0,.07) 1.4px,transparent 1.6px);background-size:18px 18px}
b{font-weight:900}
.box{border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);background:#fff}
.hdr{background:var(--hdr);padding:38px 42px}
.kick{font-weight:800;font-size:25px;letter-spacing:5px;text-transform:uppercase;margin-bottom:16px}
.hdr h1{font-weight:900;font-size:84px;line-height:1;letter-spacing:-2.5px}
.hdr p{font-size:34px;font-weight:600;margin-top:18px;line-height:1.25}
.scene{flex:1;min-height:0;margin-top:40px;display:flex;flex-direction:column}
.scene .ph{padding:18px 28px;font-weight:900;font-size:34px;letter-spacing:1px;text-transform:uppercase;color:#fff;background:var(--acc);border-bottom:6px solid var(--ink)}
.scene .ph.bad{background:var(--bad)}.scene .ph.ok{background:var(--ok)}.scene .ph.ink{background:var(--ink)}
.stage{flex:1;min-height:0;position:relative;display:flex;flex-direction:column;justify-content:flex-end;padding:30px 34px 22px;
 background:linear-gradient(var(--tint) 80%,var(--floor) 80%)}
.stage .who{flex:1;min-height:0;display:flex;justify-content:center;align-items:flex-end}
.stage .who svg{height:100%;width:auto;max-width:78%}
.say{position:relative;margin:0 6px 52px;background:#fff;border:5px solid var(--ink);border-radius:34px;padding:24px 32px;
 font-size:48px;font-weight:800;line-height:1.16;box-shadow:7px 7px 0 var(--ink)}
.say:after{content:"";position:absolute;left:50%;bottom:-40px;border-left:22px solid transparent;border-right:22px solid transparent;border-top:40px solid var(--ink)}
.props{position:absolute;bottom:26px;display:flex;gap:16px;font-size:110px;line-height:1}
.props.l{left:40px}.props.r{right:40px}
.cap{background:var(--hdr);border:5px solid var(--ink);padding:22px 30px;font-size:44px;font-weight:700;line-height:1.2;box-shadow:8px 8px 0 var(--ink)}
.cap .lab{display:block;font-weight:900;font-size:24px;letter-spacing:4px;text-transform:uppercase;margin-bottom:8px}
.note{background:var(--ink);color:#fff;padding:26px 34px;font-size:42px;font-weight:800;line-height:1.2;margin-top:34px}
.note b{color:var(--hdr)}
.vs{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:34px;margin-top:40px;min-height:0}
.vs .box{display:flex;flex-direction:column}
.vs .ph{padding:16px 22px;font-weight:900;font-size:34px;color:#fff;border-bottom:6px solid var(--ink);letter-spacing:1px}
.vs .pb{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:space-evenly;gap:12px;padding:24px 22px;text-align:center}
.vs .pb{background:var(--tint)}.vs .pb svg{height:400px;width:auto;max-width:100%}.vs .pb p{font-size:48px;font-weight:900;line-height:1.14}
.lbl{font-weight:900;font-size:28px;letter-spacing:5px;text-transform:uppercase;margin-bottom:26px}
.items{display:flex;flex-direction:column;gap:22px;flex:1;justify-content:center}
.item{display:flex;align-items:center;gap:26px;border:6px solid var(--ink);box-shadow:9px 9px 0 var(--ink);background:#fff;padding:20px 28px}
.item .em{font-size:70px;line-height:1;flex:0 0 auto}
.item .tx{font-size:46px;font-weight:900;line-height:1.1}
.item .tx span{display:block;font-size:30px;font-weight:500;margin-top:6px;color:#333;line-height:1.25}
.lhead{display:flex;align-items:flex-end;gap:24px;margin-bottom:34px}.lhead .lt{flex:1}.lhead .lt h1{font-size:68px}.lhead .mascot{flex:0 0 auto}.lhead .mascot svg{flex:0 0 auto}
.listwrap .items{flex:1}
.listwrap .mascot{flex:0 0 auto;display:flex;align-items:flex-end}
.big{font-weight:900;font-size:220px;line-height:.9;letter-spacing:-6px;color:var(--acc)}
.statcap{font-size:50px;font-weight:800;line-height:1.18;margin-top:24px}
.src{font-size:26px;color:#555;margin-top:18px}
.stat{flex:1;display:flex;align-items:center;gap:20px}
.stat .l{flex:1}
.bub{position:relative;background:#fff;border:5px solid var(--ink);border-radius:36px;padding:30px 40px 34px;font-size:56px;font-weight:800;line-height:1.12;box-shadow:9px 9px 0 var(--ink);margin:10px 70px 56px 0}
.bub:before{content:"";position:absolute;left:70px;bottom:-46px;border-right:52px solid transparent;border-top:46px solid var(--ink)}
.bub .who2{display:block;font-size:22px;font-weight:900;letter-spacing:4px;color:#777;margin-bottom:10px}
.stamp{position:absolute;right:-40px;top:-30px;transform:rotate(9deg);border:7px solid var(--bad);color:var(--bad);background:var(--bg);font-weight:900;font-size:46px;letter-spacing:5px;padding:4px 20px}
.fact{display:flex;align-items:flex-end;gap:20px;flex:1}
.fact .cap{flex:1;margin-bottom:30px;font-size:50px}.fact svg{height:470px;width:auto}.stat svg{height:470px;width:auto}.listwrap .mascot svg{height:330px;width:auto}
.moral{flex:1;display:flex;flex-direction:column;justify-content:space-between}
.moral .hdr h1{font-size:90px}
.moral .row{display:flex;align-items:flex-end;justify-content:space-between;gap:20px}.moral .row svg,.vs .pb svg,.stat svg,.listwrap .mascot svg{flex:0 0 auto}
.save{flex:1;font-size:42px;font-weight:900;background:#fff;border:5px solid var(--ink);box-shadow:8px 8px 0 var(--ink);padding:20px 28px;margin-bottom:30px;max-width:620px;line-height:1.2}
.cnt{display:flex;justify-content:space-between;margin-top:28px;font-weight:800;font-size:24px;letter-spacing:4px;color:#444}
"""


def char(brand, s, w=None, h=None):
    return cast.character(brand, s.get("mood", "happy"), s.get("pose", "none"), w or 300, h)


def props(s, side="r"):
    p = s.get("props") or []
    return f'<div class="props {side}">{"".join(html.escape(x) for x in p[:3])}</div>' if p else ""


def stage(brand, s, w=380, side="r"):
    say = f'<div class="say">{fmt(s["say"])}</div>' if s.get("say") else ""
    return f'<div class="stage">{say}<div class="who">{char(brand, s, w)}</div>{props(s, side)}</div>'


def slide_body(brand, s):
    t = s["type"]
    if t == "cover":
        sub = f'<p>{fmt(s["sub"])}</p>' if s.get("sub") else ""
        return (f'<div class="box hdr"><div class="kick">{fmt(s["kicker"])}</div><h1>{fmt(s["title"])}</h1>{sub}</div>'
                f'<div class="box scene">{stage(brand, s, 470 if brand == "co" else 400)}</div>')
    if t == "panel":
        note = f'<div class="note">{fmt(s["note"])}</div>' if s.get("note") else ""
        return (f'<div class="cap"><span class="lab">{fmt(s["label"])}</span>{fmt(s["caption"])}</div>'
                f'<div class="box scene">{stage(brand, s, (560 if brand == "co" else 470) - (90 if s.get("note") else 0))}</div>{note}')
    if t == "versus":
        title = f'<div class="lbl">{fmt(s["title"])}</div>' if s.get("title") else ""
        def half(h, cls):
            return (f'<div class="box"><div class="ph" style="background:var(--{cls})">{fmt(h["label"])}</div>'
                    f'<div class="pb"><p>{fmt(h["text"])}</p>{cast.character(brand, h.get("mood", "happy"), h.get("pose", "none"), h=380)}</div></div>')
        return f'{title}<div class="vs">{half(s["left"], "bad")}{half(s["right"], "ok")}</div>'
    if t == "list":
        items = "".join(f'<div class="item"><div class="em">{html.escape(i["emoji"])}</div><div class="tx">{fmt(i["title"])}'
                        f'{"<span>" + fmt(i["text"]) + "</span>" if i.get("text") else ""}</div></div>' for i in s["items"])
        m = f'<div class="mascot">{char(brand, s, h=250)}</div>' if s.get("mood") else ""
        return (f'<div class="lhead"><div class="box hdr lt"><div class="kick">The list</div><h1>{fmt(s["label"])}</h1></div>{m}</div>'
                f'<div class="items">{items}</div>')
    if t == "stat":
        src = f'<div class="src">{fmt(s["source"])}</div>' if s.get("source") else ""
        return (f'<div class="stat"><div class="l"><div class="big">{fmt(s["big"])}</div>'
                f'<div class="statcap">{fmt(s["caption"])}</div>{src}</div>{char(brand, s, h=460)}</div>')
    if t == "myth":
        return (f'<div class="bub"><span class="who2">PEOPLE SAY</span>&ldquo;{fmt(s["myth"])}&rdquo;<div class="stamp">MYTH</div></div>'
                f'<div class="box scene" style="margin-top:0">{stage(brand, s)}</div>'
                f'<div class="cap" style="margin-top:34px"><span class="lab">Actually</span>{fmt(s["fact"])}</div>')
    if t == "moral":
        save = f'<div class="save">{fmt(s["save"])}</div>' if s.get("save") else "<div></div>"
        return (f'<div class="moral"><div class="box hdr"><div class="kick">The moral</div><h1>{fmt(s["text"])}</h1></div>'
                f'<div class="row">{save}{char(brand, s, h=520)}</div></div>')
    raise ValueError(t)


def page(brand, s, n, total, fonts):
    th = THEME[brand]
    vars_ = ";".join(f"--{k}:{v}" for k, v in th.items())
    swipe = "<span>SWIPE &#8594;</span>" if n == 1 else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{fonts}:root{{{vars_}}}{CSS}</style></head>'
            f'<body>{slide_body(brand, s)}<div class="cnt"><span>{n} / {total}</span>{swipe}</div></body></html>')


def validate(spec):
    errs = []
    if spec.get("brand") not in THEME:
        errs.append(f"brand must be one of {sorted(THEME)}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{3,80}", spec.get("key", "")):
        errs.append("key must be lowercase letters, digits and hyphens")
    sl = spec.get("slides") or []
    if not 4 <= len(sl) <= 8:
        errs.append(f"{len(sl)} slides: a carousel has 4 to 8")
    if sl and sl[0].get("type") != "cover":
        errs.append("slide 1 must be the cover: most people never swipe")
    for i, s in enumerate(sl, 1):
        if s.get("type") not in TYPES:
            errs.append(f"slide {i}: unknown type {s.get('type')}")
            continue
        for k in ("mood",):
            if k in s and s[k] not in MOODS:
                errs.append(f"slide {i}: mood {s[k]} not in {sorted(MOODS)}")
        if "pose" in s and s["pose"] not in POSES:
            errs.append(f"slide {i}: pose {s['pose']} not in {sorted(POSES)}")
        need = {"cover": ["kicker", "title", "mood"], "panel": ["label", "caption", "mood"], "versus": ["left", "right"],
                "list": ["label", "items"], "stat": ["big", "caption", "mood"], "myth": ["myth", "fact"], "moral": ["text"]}[s["type"]]
        for k in need:
            if not s.get(k):
                errs.append(f"slide {i} ({s['type']}): missing {k}")

        def chk(obj, where):
            for k, v in obj.items():
                if isinstance(v, str):
                    if k in LIMITS and len(re.sub(r"\*\*", "", v)) > LIMITS[k]:
                        errs.append(f"{where}: {k} is {len(v)} chars, max {LIMITS[k]}")
                    if re.search(r"https?://|www\.|\.(com|ai|events|co\.uk)\b", v):
                        errs.append(f"{where}: {k} carries a URL - slides never do")
                    if "—" in v or "–" in v:
                        errs.append(f"{where}: {k} has an em or en dash")
                elif isinstance(v, dict):
                    chk(v, f"{where}.{k}")
                elif isinstance(v, list):
                    for j, x in enumerate(v):
                        if isinstance(x, dict):
                            chk(x, f"{where}.{k}[{j}]")
        chk(s, f"slide {i}")
        if s["type"] == "list" and not 2 <= len(s.get("items") or []) <= 5:
            errs.append(f"slide {i}: a list has 2 to 5 items")
    return errs


def render(spec_path, br):
    import finish
    from pypdf import PdfReader, PdfWriter
    spec = json.load(open(spec_path))
    errs = validate(spec)
    if errs:
        raise SystemExit(f"{spec_path}:\n  " + "\n  ".join(errs))
    key, brand, sl = spec["key"], spec["brand"], spec["slides"]
    out = os.path.join(HERE, "out", key)
    os.makedirs(out, exist_ok=True)
    fonts = open(os.path.join(HERE, "fonts.css")).read()
    pg = br.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
    writer, problems = PdfWriter(), []
    for n, s in enumerate(sl, 1):
        hp = os.path.join(out, f"slide-{n}.html")
        open(hp, "w").write(page(brand, s, n, len(sl), fonts))
        pg.goto("file://" + hp)
        pg.wait_for_load_state("networkidle")
        pg.wait_for_timeout(250)
        over = pg.evaluate("""() => { const b=document.body; if (b.scrollHeight>1350) return 'page '+b.scrollHeight;
            for (const el of document.querySelectorAll('.cap,.item,.hdr,.save,.statcap,.vs .pb'))
              if (el.scrollHeight>el.clientHeight+2 || el.scrollWidth>el.clientWidth+2) return el.className;
            const who=document.querySelector('.stage .who svg');
            if (who && who.getBoundingClientRect().height < 300) return 'character squeezed under 300px: shorten the bubble or caption';
            return ''; }""")
        if over:
            problems.append(f"slide {n}: overflow in {over}")
        raw = os.path.join(out, f"slide-{n}.raw.png")
        pg.screenshot(path=raw)
        finish.LOOK = LOOK
        finish.main([raw, os.path.join(out, f"slide-{n}.png")])
        if n == 1:
            finish.main([raw, os.path.join(out, "cover.png")])
        os.remove(raw)
        pdf = os.path.join(out, f"slide-{n}.pdf")
        pg.pdf(path=pdf, width="1080px", height="1350px", print_background=True, page_ranges="1")
        writer.append(PdfReader(pdf))
        os.remove(pdf)
    with open(os.path.join(out, f"{key}.pdf"), "wb") as fh:
        writer.write(fh)
    pg.close()
    if problems:
        raise SystemExit(f"{key}: " + "; ".join(problems) + " - shorten the text, then re-render")
    print(f"{key}: {len(sl)} slides -> out/{key}/{key}.pdf, cover.png")


def main(argv):
    check = argv[:1] == ["--check"]
    paths = argv[1:] if check else argv
    if not paths:
        print(__doc__)
        return 2
    if check:
        bad = 0
        for p in paths:
            e = validate(json.load(open(p)))
            print(p, "ok" if not e else "\n  " + "\n  ".join(e))
            bad += bool(e)
        return 1 if bad else 0
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        br = p.chromium.launch()
        for sp in paths:
            render(sp, br)
        br.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
