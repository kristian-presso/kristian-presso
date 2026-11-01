"""Editorial infographics: one image that teaches on its own. No cartoons, no OpenAI art.

    python3 infographic.py specs/<key>.json [more.json ...]
    python3 infographic.py --check specs/<key>.json

The look (01/11/2026) is the editorial one Kristian sent as the bar ("The self-improving harness"):
a ruled kicker with a coloured square, a huge black grotesk headline ending in a coloured full stop,
numbered section labels, hard-bordered boxes, a terminal panel, dashed loop arrows, mono source.

Why (01/11/2026, Kristian): "switch from cartoons into infographics and make super cool, nice
infographics like you have them in some of the examples that I've sent to you." The examples are
the posts that did best in the 8 weeks before: "Wrap the job, not the endpoint" (296 impressions),
"Copying software was never the hard part" (242), the Eventbrite fee table (299) and "Semi-headless
rules" (152). They share one thing: the picture is the lesson, laid out so people save it. This
renderer draws those layouts from a JSON spec, in each brand's colours, with every word ours.

Writes out/<key>/<key>.png (2160x2700, 4:5, tagged card-look:Infographic) for a Buffer image post.

SPEC
{
  "key": "pe-2026-w45-2-agents",          # file-safe, unique
  "brand": "pe" | "co" | "kp",
  "layout": "versus" | "rules" | "stats" | "poster" | "steps" | "flow",
  "kicker": "short pill label",
  "title": "Headline with **the accent part**",
  "sub": "one line under the title (optional)",
  "source": "where the facts come from (no URL)",   # required for stats
  "save": "💾 Save this for ...",                   # optional
  ... layout fields below
}
  versus  left{label, title, items[], mark?}, right{label, title, items[]}, tell{label, text}?
  rules   rows[{k, v}] 3-8
  stats   items[{big, text}] 2-4, take?            take = the one-line lesson in a dark box
  steps   items[{emoji, title, text?}] 3-6
  hub     a system diagram with connector lines: left{no, label, wire?, nodes[{icon, title, text?, wire?, hl?, dim?}]},
          hub{icon, title, small, no?, label?, size?}, right{...same as left}, top{icon, title, text?, wire?}?,
          guard{chip, text, wire?}?, height?   ("MCP in the middle, your AI on one side, your tools on the other")
  bars    items[{value 0-100, big?, text, dark?}] 2-4, take?   each number drawn against a 0-50-100% scale
  flow    stages[{label, kind, ...}] 3-4, loop?   a process diagram, numbered 01-04, top to bottom
          kind terminal{title, lines[]} (lines starting ✗ red, ✓ green, "you:" amber)
          kind circle{title, small} | cards{cards[{chip, text, dark?, dashed?}]} | stack{rows[{t, hl?, badge?}]}
  poster  left{tag, emoji, caption, items[]}, right{tag, emoji, caption, items[]},
          twist{tag, text}, punch "LINE ONE. **LINE TWO.**"
Text may use **bold** (drawn in the accent colour). No URL, logo or call to action on the image.
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))

BRANDS = {
    "pe": dict(acc="#2F45D8", ink="#111111", mute="#55555C", bg="#F2F1EC", dark="#111111", hi="#FFD23F", name="PRESSO NETWORK"),
    "co": dict(acc="#18884A", ink="#111111", mute="#55555C", bg="#F2F1EC", dark="#111111", hi="#C6F432", name="COREY"),
    "kp": dict(acc="#D7342A", ink="#111111", mute="#55555C", bg="#F2F1EC", dark="#151515", hi="#FFD23F", name="KRISTIAN PAPADAKIS"),
}
LIMITS = {"title": 70, "sub": 140, "kicker": 32, "item": 70, "k": 22, "v": 120, "big": 9,
          "text": 90, "take": 110, "tell": 150, "punch": 60, "twist": 220, "save": 70, "source": 90}


def fmt(s):
    s = html.escape(s or "")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)


def check(spec):
    errs = []
    if spec.get("brand") not in BRANDS:
        errs.append("brand must be pe, co or kp")
    lay = spec.get("layout")
    if lay not in ("versus", "rules", "stats", "poster", "steps", "flow", "hub", "bars"):
        errs.append(f"unknown layout {lay}")
    for f in ("key", "title", "kicker"):
        if not spec.get(f):
            errs.append(f"missing {f}")
    blob = json.dumps(spec, ensure_ascii=False)
    if re.search(r"https?://|www\.|\.com\b|\.ai\b", blob):
        errs.append("a URL on the image - images never carry one")
    if "—" in blob or "–" in blob:
        errs.append("em or en dash")
    for f in ("title", "sub", "kicker", "save", "source"):
        if len(spec.get(f) or "") > LIMITS[f]:
            errs.append(f"{f} is {len(spec[f])} chars, max {LIMITS[f]}")
    if lay == "stats" and not spec.get("source"):
        errs.append("a stats infographic names its source")
    return errs


CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{background:var(--bg);color:var(--ink);font-family:'Inter',sans-serif;
 background-image:repeating-linear-gradient(90deg,rgba(0,0,0,.045) 0 1.5px,transparent 1.5px 90px)}
.page{position:relative;width:1080px;height:1350px;overflow:hidden;padding:66px 64px 50px;display:flex;flex-direction:column}
.kick{display:flex;align-items:center;gap:14px;font:700 21px 'Space Grotesk',sans-serif;letter-spacing:3.5px;text-transform:uppercase;
 padding-bottom:18px;border-bottom:2.5px solid var(--ink)}
.kick:before{content:"";width:15px;height:15px;background:var(--acc)}
h1{font:900 96px/0.94 'Inter Display','Inter',sans-serif;letter-spacing:-3.5px;margin-top:40px}
h1 b{color:var(--acc);font-weight:900}
h1 .dot{color:var(--acc)}
.sub{font-size:31px;line-height:1.3;color:var(--mute);margin-top:22px;max-width:920px;font-weight:500}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;margin:34px 0 26px}
.foot{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;border-top:2px solid rgba(0,0,0,.14);padding-top:20px}
.save{font:700 25px/1.25 'Space Grotesk',sans-serif;max-width:620px;display:flex;gap:10px}
.src{font:500 18px/1.4 'IBM Plex Mono',monospace;color:var(--mute);text-align:right;max-width:440px}
b{font-weight:800}
.lbl{font:700 19px 'Space Grotesk',sans-serif;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:14px}
.lbl em{font-style:normal;color:var(--acc);margin-right:8px}
.box{background:#fff;border:2.5px solid var(--ink);box-shadow:5px 6px 0 rgba(0,0,0,.16)}
.chip{display:inline-block;font:800 17px 'Space Grotesk',sans-serif;letter-spacing:2px;text-transform:uppercase;padding:6px 11px;color:#fff;background:var(--acc)}
.chip.k{background:var(--ink)}
/* versus */
.vs{display:grid;grid-template-columns:1fr 56px 1fr;align-items:stretch}
.vs .arrow{display:grid;place-items:center;font:900 40px 'Inter';color:var(--ink)}
.vs ul{padding:6px 24px}
.vs li{list-style:none;display:flex;gap:14px;padding:17px 0;border-top:1.5px dashed #CFCFC8;font-size:26px;line-height:1.28;font-weight:500}
.vs li:first-child{border-top:0}
.vs li i{font-style:normal;font-weight:900;flex:0 0 22px;color:#9A9A92}
.vs .bad li{color:#55555A}
.vs .good{border-color:var(--acc);box-shadow:5px 6px 0 var(--acc)}
.vs .good li i{color:var(--acc)}
.vs .head{display:flex;align-items:center;gap:12px;padding:16px 24px;border-bottom:2.5px solid var(--ink);font:800 27px/1.15 'Inter'}
.vs .good .head{border-color:var(--acc)}
.tell{margin-top:30px;border:2.5px dashed var(--acc);padding:22px 26px;font-size:28px;line-height:1.35;font-weight:600;background:rgba(255,255,255,.6)}
.tell .chip{margin-right:12px;vertical-align:3px}
/* rules */
.rules{border-top:2.5px solid var(--ink)}
.row{display:grid;grid-template-columns:250px 1fr;gap:26px;padding:22px 0;border-bottom:1.5px solid rgba(0,0,0,.18);align-items:baseline}
.row .k{font:600 24px 'IBM Plex Mono',monospace;color:var(--acc)}
.row .v{font-size:29px;line-height:1.32;font-weight:500}
/* stats */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}
.st{padding:24px 28px 26px}
.st .n{font:900 108px/0.92 'Inter Display','Inter';color:var(--acc);letter-spacing:-4px}
.st p{font-size:26px;line-height:1.28;margin-top:12px;font-weight:600}
.take{margin-top:30px;background:var(--ink);color:#fff;padding:24px 30px;font:700 31px/1.25 'Space Grotesk',sans-serif;box-shadow:5px 6px 0 rgba(0,0,0,.16)}
.take b{color:var(--hi)}
/* steps */
.steps{display:flex;flex-direction:column}
.sp{display:grid;grid-template-columns:96px 1fr;align-items:center}
.sp .no{font:900 52px 'Inter Display','Inter';color:var(--acc);letter-spacing:-2px}
.sp .bx{display:flex;gap:18px;align-items:center;padding:16px 22px}
.sp .em{font-size:40px}
.sp h4{font:800 29px/1.15 'Inter'}
.sp p{font-size:23px;line-height:1.3;color:var(--mute);margin-top:3px;font-weight:500}
.sp+.sp{margin-top:16px}
/* flow */
.flow{display:grid;grid-template-columns:1fr 54px 1fr;grid-template-rows:auto 54px auto;align-items:start}
.ar{display:grid;place-items:center;font:900 36px 'Inter';height:100%;align-self:center}
.stg{display:flex;flex-direction:column}
.down{margin:6px 0 6px 200px;padding-left:20px;font:900 34px 'Inter';line-height:1}
.term{background:#151515;color:#EDEDED;font:500 18px/1.5 'IBM Plex Mono',monospace;padding:0 0 14px;box-shadow:6px 7px 0 rgba(0,0,0,.18)}
.term .tb{display:flex;gap:8px;align-items:center;padding:10px 16px;border-bottom:1px solid #333;margin-bottom:10px;color:#888;font-size:16px}
.term .tb i{width:12px;height:12px;border-radius:50%;background:#555}.term .tb i:first-child{background:var(--acc)}
.term div.l{padding:0 18px}
.term .x{color:#FF7A70}.term .ok{color:#8BE28B}.term .you{color:#F5C08A;border-top:1px dashed #444;margin-top:8px;padding-top:8px}
.cards{display:flex;flex-direction:column;gap:12px}
.cd{padding:14px 18px}
.cd p{font-size:21px;line-height:1.3;margin-top:8px;font-weight:600}
.cd.dash{border-style:dashed;box-shadow:none;background:transparent}
.stack{display:flex;flex-direction:column;gap:9px}
.stack div{border:2.5px solid var(--ink);background:#fff;padding:10px 14px;font:600 21px 'IBM Plex Mono',monospace;display:flex;justify-content:space-between}
.stack div.hl{background:var(--acc);border-color:var(--acc);color:#fff}
.circle{align-self:center;margin:14px 0;width:210px;height:210px;border-radius:50%;background:var(--acc);color:#fff;display:grid;place-items:center;text-align:center;
 outline:3px dashed var(--acc);outline-offset:12px;padding:20px}
.circle h5{font:900 33px/1 'Inter Display','Inter'}
.circle small{display:block;font:700 15px 'Space Grotesk';letter-spacing:2px;margin-top:10px;text-transform:uppercase;opacity:.9}
.loopnote{margin-top:26px;font-size:27px;font-weight:700;text-align:center;border-top:3px dashed var(--acc);padding-top:18px}
.loopnote span{color:var(--acc);font-weight:900}
.loopnote b{color:var(--acc)}
/* hub: a system diagram with real connector lines */
.dg{position:relative;flex:1;min-height:600px}
.zone{position:absolute;border:2.5px dashed rgba(0,0,0,.28);border-radius:18px}
.zone .zl{position:absolute;top:-15px;left:18px;background:var(--bg);padding:0 10px;font:700 18px 'Space Grotesk',sans-serif;letter-spacing:2.5px;text-transform:uppercase}
.zone .zl em{font-style:normal;color:var(--acc);margin-right:8px}
.nd{position:absolute;background:#fff;border:2.5px solid var(--ink);box-shadow:4px 5px 0 rgba(0,0,0,.16);display:flex;gap:12px;align-items:center;padding:12px 14px;z-index:2}
.nd .i{font-size:32px;flex:0 0 auto;line-height:1}
.nd b{display:block;font:800 21px/1.12 'Inter'}
.nd small{display:block;font:500 16px/1.25 'Inter';color:var(--mute);margin-top:3px}
.nd.hl{background:var(--acc);border-color:var(--acc);color:#fff}.nd.hl small{color:rgba(255,255,255,.85)}
.nd.dim{border-style:dashed;box-shadow:none;background:rgba(255,255,255,.55)}
.hubn{position:absolute;border-radius:50%;background:var(--acc);color:#fff;display:grid;place-items:center;text-align:center;z-index:2;
 outline:3px dashed var(--acc);outline-offset:12px;box-shadow:0 22px 50px -18px var(--acc)}
.hubn .i{font-size:44px;line-height:1}
.hno{font:700 13px 'Space Grotesk';letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;opacity:.95}
.hno em{font-style:normal;color:var(--hi);margin-right:6px}
.hubn h5{font:900 38px/0.95 'Inter Display','Inter';margin-top:6px;letter-spacing:-1px}
.hubn small{display:block;font:700 14px/1.35 'Space Grotesk';letter-spacing:1.6px;text-transform:uppercase;margin-top:8px;opacity:.92;padding:0 22px}
.wires{position:absolute;inset:0;overflow:visible;z-index:1}
.el{position:absolute;z-index:3;transform:translate(-50%,-50%);background:var(--bg);border:2px solid var(--ink);padding:3px 9px;
 font:700 14px 'IBM Plex Mono',monospace;letter-spacing:.5px;white-space:nowrap}
.el.a{background:var(--acc);border-color:var(--acc);color:#fff}
.guard{position:absolute;left:0;right:0;bottom:0;border:2.5px solid var(--ink);background:var(--ink);color:#fff;display:flex;gap:14px;align-items:center;padding:14px 20px;z-index:2;font:600 22px/1.3 'Inter'}
.guard .chip{background:var(--acc);white-space:nowrap;flex:0 0 auto}
/* bars: numbers against a 0-100 scale, the context that makes a number land */
.bars{display:flex;flex-direction:column;gap:14px}
.br .top{display:flex;justify-content:space-between;align-items:baseline;gap:20px}
.br .n{font:900 58px/1 'Inter Display','Inter';color:var(--acc);letter-spacing:-2px;flex:0 0 auto}
.br .t{font:600 25px/1.25 'Inter';text-align:right}
.track{position:relative;height:30px;margin-top:10px;background:#fff;border:2.5px solid var(--ink)}
.fill{position:absolute;left:0;top:0;bottom:0;background:var(--acc)}
.fill.k{background:var(--ink)}
.tick{position:absolute;top:-8px;bottom:-8px;width:0;border-left:2px dashed rgba(0,0,0,.45)}
.scale{display:flex;justify-content:space-between;font:500 15px 'IBM Plex Mono',monospace;color:var(--mute);margin-top:6px}
/* poster */
.poster .page{padding:46px}
.frame{flex:1;display:flex;flex-direction:column;border:6px solid var(--dark);background:var(--bg)}
.ph{background:var(--dark);color:#F7EEDC;padding:30px 36px 28px;display:flex;justify-content:space-between;align-items:flex-end;gap:20px}
.ph h1{font:400 66px/0.98 'Archivo Black',sans-serif;letter-spacing:-0.5px;text-transform:uppercase;margin:0;color:#F7EEDC}
.ph h1 b{color:var(--hi);font-weight:400}
.ph .kk{font:600 19px/1.35 'IBM Plex Mono',monospace;text-align:right;color:#F7EEDC;opacity:.85;max-width:210px}
.cols{display:grid;grid-template-columns:1fr 1fr;flex:1}
.col{padding:26px 28px;border-right:6px solid var(--dark);display:flex;flex-direction:column}
.col:last-child{border-right:0}
.tag{align-self:flex-start;font:400 23px 'Archivo Black',sans-serif;text-transform:uppercase;padding:8px 14px;border:3.5px solid var(--dark);
 box-shadow:5px 5px 0 var(--dark);background:#9FD3FF}
.col:last-child .tag{background:var(--hi)}
.big{font-size:96px;text-align:center;margin:18px 0 4px}
.cap{text-align:center;font:400 21px 'Archivo Black',sans-serif;text-transform:uppercase;margin-bottom:10px}
.col li{list-style:none;display:flex;gap:12px;padding:12px 0;border-top:2.5px dashed #A99F86;font-size:25px;font-weight:700;line-height:1.25}
.col li:first-child{border-top:0}
.col li i{font-style:normal;flex:0 0 30px;height:30px;border-radius:50%;border:3px solid var(--dark);display:grid;place-items:center;font-size:15px;margin-top:1px}
.col:first-child li i{background:#9FD3FF}.col:last-child li i{background:var(--hi)}
.bot{display:grid;grid-template-columns:1.1fr 1fr;border-top:6px solid var(--dark)}
.tw{padding:24px 28px;border-right:6px solid var(--dark)}
.tw .tag{background:#FF9AA2}
.tw p{font-size:24px;line-height:1.35;margin-top:14px;font-weight:600}
.tw p b{font-weight:900}
.pn{background:var(--dark);display:grid;place-items:center;padding:24px}
.pn div{background:#fff;border-radius:22px;border:5px solid #fff;outline:4px solid var(--dark);padding:24px 26px;
 font:400 36px/1.08 'Archivo Black',sans-serif;text-transform:uppercase;text-align:center;color:var(--dark)}
.pn div b{color:var(--acc);font-weight:400}
.psrc{font:500 16px 'IBM Plex Mono',monospace;color:#5A5241;margin-top:12px}
"""


def lis(items, mark):
    return "".join(f"<li><i>{mark}</i><span>{fmt(t)}</span></li>" for t in items)


def body(s):
    lay = s["layout"]
    if lay == "versus":
        l, r = s["left"], s["right"]
        col = lambda c, cls, m, n: (f'<div><div class="lbl"><em>{n}</em>{fmt(c.get("label", ""))}</div><div class="box {cls}"><div class="head">{fmt(c["title"])}</div>'
                                    f'<ul>{lis(c["items"], m)}</ul></div></div>')
        out = f'<div class="vs">{col(l, "bad", l.get("mark", "✕"), "01")}<div class="arrow">→</div>{col(r, "good", "✓", "02")}</div>'
        if s.get("tell"):
            out += f'<div class="tell"><span class="chip">{fmt(s["tell"]["label"])}</span>{fmt(s["tell"]["text"])}</div>'
        return out
    if lay == "rules":
        return '<div class="rules">' + "".join(
            f'<div class="row"><div class="k">{fmt(r["k"])}</div><div class="v">{fmt(r["v"])}</div></div>' for r in s["rows"]) + "</div>"
    if lay == "stats":
        out = '<div class="grid">' + "".join(
            f'<div class="box st"><div class="n">{fmt(i["big"])}</div><p>{fmt(i["text"])}</p></div>' for i in s["items"]) + "</div>"
        if s.get("take"):
            out += f'<div class="take">{fmt(s["take"])}</div>'
        return out
    if lay == "steps":
        return '<div class="steps">' + "".join(
            f'<div class="sp"><div class="no">{n:02d}</div><div class="box bx"><div class="em">{i.get("emoji","")}</div><div><h4>{fmt(i["title"])}</h4>'
            + (f'<p>{fmt(i["text"])}</p>' if i.get("text") else "") + "</div></div></div>" for n, i in enumerate(s["items"], 1)) + "</div>"
    if lay == "flow":
        parts = []
        for n, st in enumerate(s["stages"], 1):
            k = st["kind"]
            if k == "terminal":
                lines = "".join(f'<div class="l {c}">{html.escape(t)}</div>' for c, t in
                                [(("x" if t.startswith("✗") else "ok" if t.startswith("✓") else "you" if t.startswith("you:") else ""), t) for t in st["lines"]])
                inner = f'<div class="term"><div class="tb"><i></i><i></i><i></i>&nbsp; {html.escape(st.get("title","session"))}</div>{lines}</div>'
            elif k == "circle":
                inner = f'<div class="circle"><div><h5>{fmt(st["title"])}</h5><small>{fmt(st.get("small",""))}</small></div></div>'
            elif k == "cards":
                inner = '<div class="cards">' + "".join(
                    f'<div class="box cd{" dash" if c.get("dashed") else ""}"><span class="chip{" k" if c.get("dark") else ""}">{fmt(c["chip"])}</span>'
                    f'<p>{fmt(c["text"])}</p></div>' for c in st["cards"]) + "</div>"
            elif k == "stack":
                inner = '<div class="stack">' + "".join(
                    f'<div class="{"hl" if r.get("hl") else ""}"><span>{html.escape(r["t"])}</span><span>{html.escape(r.get("badge",""))}</span></div>' for r in st["rows"]) + "</div>"
            else:
                raise ValueError(k)
            parts.append(f'<div class="lbl"><em>{n:02d}</em>{fmt(st["label"])}</div>{inner}')
        pos = ["1/1", "1/3", "3/3", "3/1"]
        cells = "".join(f'<div class="stg" style="grid-area:{pos[i]}">{p}</div>' for i, p in enumerate(parts))
        arrows = '<div class="ar" style="grid-area:1/2">→</div><div class="ar" style="grid-area:2/3">↓</div>'
        if len(parts) > 3:
            arrows += '<div class="ar" style="grid-area:3/2">←</div>'
        out = f'<div class="flow">{cells}{arrows}</div>'
        if s.get("loop"):
            out += f'<div class="loopnote"><span>↺</span> {fmt(s["loop"])}</div>'
        return out
    if lay == "bars":
        out = '<div class="bars">'
        for i in s["items"]:
            v = max(0, min(100, float(i["value"])))
            out += (f'<div class="br"><div class="top"><div class="n">{fmt(i.get("big", str(i["value"]) + "%"))}</div><div class="t">{fmt(i["text"])}</div></div>'
                    f'<div class="track"><div class="fill{" k" if i.get("dark") else ""}" style="width:{v}%"></div>'
                    f'<div class="tick" style="left:50%"></div></div><div class="scale"><span>0%</span><span>50%</span><span>100%</span></div></div>')
        out += "</div>"
        if s.get("take"):
            out += f'<div class="take">{fmt(s["take"])}</div>'
        return out
    if lay == "hub":
        return hub(s)
    raise ValueError(lay)


def node(n, cls=""):
    c = cls + (" hl" if n.get("hl") else "") + (" dim" if n.get("dim") else "")
    return (f'<div class="nd {c}" id="{n["_id"]}"><span class="i">{n.get("icon","")}</span><span><b>{fmt(n["title"])}</b>'
            + (f'<small>{fmt(n["text"])}</small>' if n.get("text") else "") + "</span></div>")


def hub(s):
    """Left column -> hub -> right column, with an optional node on top and a guard strip below.
    Positions are computed here; the wires are drawn by JS from the rendered boxes (see WIRE_JS)."""
    W, H = 952, int(s.get("height", 800))
    top, guard = s.get("top"), s.get("guard")
    y0 = 150 if top else 30
    y1 = H - (120 if guard else 10)
    L, R, Hb = s["left"], s["right"], s["hub"]
    lw, rw, hd = 250, 250, int(Hb.get("size", 236))
    hx, hy = (W - hd) // 2 - 6, (y0 + y1 - hd) // 2
    parts, edges = [], []

    def column(col, x, w, side):
        ns = col["nodes"]
        zone_top, zone_h = y0, y1 - y0
        parts.append(f'<div class="zone" style="left:{x-14}px;top:{zone_top}px;width:{w+28}px;height:{zone_h}px">'
                     f'<div class="zl"><em>{col.get("no","")}</em>{fmt(col.get("label",""))}</div></div>')
        gap = min((zone_h - 30) / len(ns), 190)
        off = (zone_h - 30 - gap * len(ns)) / 2
        for i, n in enumerate(ns):
            n["_id"] = f"{side}{i}"
            nh = 92 if n.get("text") else 66
            yy = int(zone_top + 24 + off + gap * i + (gap - nh) / 2)
            parts.append(f'<div style="position:absolute;left:{x}px;top:{yy}px;width:{w}px">'
                         + node(n).replace('class="nd ', 'style="position:relative" class="nd ') + "</div>")
            lab = n.get("wire") or (col.get("wire", "") if i == len(ns) // 2 else "")
            edges.append({"a": n["_id"], "b": "hub", "label": lab, "dashed": bool(n.get("dim")), "rev": side == "r"})

    column(L, 14, lw, "l")
    column(R, W - rw - 14, rw, "r")
    hl = (f'<div class="hno"><em>{Hb["no"]}</em>{fmt(Hb.get("label",""))}</div>' if Hb.get("no") else "")
    parts.append(f'<div class="hubn" id="hub" style="left:{hx}px;top:{hy}px;width:{hd}px;height:{hd}px"><div>{hl}'
                 f'<div class="i">{Hb.get("icon","")}</div><h5>{fmt(Hb["title"])}</h5><small>{fmt(Hb.get("small",""))}</small></div></div>')
    if top:
        top["_id"] = "top"
        parts.append(f'<div style="position:absolute;left:{(W-360)//2}px;top:0;width:360px">' + node(top, "hl").replace('class="nd ', 'style="position:relative" class="nd ') + "</div>")
        edges.append({"a": "top", "b": "hub", "label": top.get("wire", ""), "dashed": False, "accent": True})
    if guard:
        parts.append(f'<div class="guard" id="guard"><span class="chip">{fmt(guard.get("chip","Rule"))}</span><span>{fmt(guard["text"])}</span></div>')
        edges.append({"a": "hub", "b": "guard", "label": guard.get("wire", ""), "dashed": True})
    data = json.dumps(edges).replace("</", "<\\/")
    return (f'<div class="dg" style="height:{H}px;flex:0 0 {H}px"><svg class="wires"></svg>{"".join(parts)}</div>'
            f'<script>window.EDGES={data};</script>')


WIRE_JS = """
(() => {
  const E = window.EDGES; if (!E) return;
  const dg = document.querySelector('.dg'), svg = dg.querySelector('.wires'), R = dg.getBoundingClientRect();
  const ns = 'http://www.w3.org/2000/svg', css = getComputedStyle(document.body);
  const ink = css.getPropertyValue('--ink').trim(), acc = css.getPropertyValue('--acc').trim();
  const defs = document.createElementNS(ns, 'defs');
  for (const [id, col] of [['ah', ink], ['aa', acc]]) {
    const m = document.createElementNS(ns, 'marker');
    m.setAttribute('id', id); m.setAttribute('viewBox', '0 0 10 10'); m.setAttribute('refX', '9'); m.setAttribute('refY', '5');
    m.setAttribute('markerWidth', '7'); m.setAttribute('markerHeight', '7'); m.setAttribute('orient', 'auto-start-reverse');
    const p = document.createElementNS(ns, 'path'); p.setAttribute('d', 'M0,0 L10,5 L0,10 z'); p.setAttribute('fill', col);
    m.appendChild(p); defs.appendChild(m);
  }
  svg.appendChild(defs);
  const box = id => { const r = document.getElementById(id).getBoundingClientRect();
    return {x: r.left - R.left, y: r.top - R.top, w: r.width, h: r.height, cx: r.left - R.left + r.width / 2, cy: r.top - R.top + r.height / 2}; };
  for (const e of E) {
    const a = box(e.a), b = box(e.b); let p1, p2, c1, c2;
    if (Math.abs(a.cx - b.cx) > Math.abs(a.cy - b.cy)) {
      const ar = a.cx < b.cx;
      p1 = {x: ar ? a.x + a.w : a.x, y: a.cy}; p2 = {x: ar ? b.x : b.x + b.w, y: b.cy};
      if (e.b === 'hub') { p2 = {x: ar ? b.x - 16 : b.x + b.w + 16, y: b.cy}; }
      const dx = (p2.x - p1.x) * 0.5; c1 = {x: p1.x + dx, y: p1.y}; c2 = {x: p2.x - dx, y: p2.y};
    } else {
      const dn = a.cy < b.cy;
      p1 = {x: a.cx, y: dn ? a.y + a.h : a.y}; p2 = {x: b.cx, y: dn ? b.y : b.y + b.h};
      if (e.a === 'hub') p1 = {x: a.cx, y: dn ? a.y + a.h + 14 : a.y};
      if (e.b === 'hub') p2 = {x: b.cx, y: dn ? b.y - 14 : b.y + b.h};
      const dy = (p2.y - p1.y) * 0.5; c1 = {x: p1.x, y: p1.y + dy}; c2 = {x: p2.x, y: p2.y - dy};
    }
    if (e.rev) { [p1, p2] = [p2, p1]; [c1, c2] = [c2, c1]; }
    const path = document.createElementNS(ns, 'path');
    path.setAttribute('d', `M${p1.x},${p1.y} C${c1.x},${c1.y} ${c2.x},${c2.y} ${p2.x},${p2.y}`);
    path.setAttribute('fill', 'none'); path.setAttribute('stroke', e.accent ? acc : ink); path.setAttribute('stroke-width', '3');
    if (e.dashed) path.setAttribute('stroke-dasharray', '9 7');
    path.setAttribute('marker-end', `url(#${e.accent ? 'aa' : 'ah'})`);
    svg.appendChild(path);
    const dot = document.createElementNS(ns, 'circle'); dot.setAttribute('cx', p1.x); dot.setAttribute('cy', p1.y); dot.setAttribute('r', '5.5');
    dot.setAttribute('fill', e.accent ? acc : ink); svg.appendChild(dot);
    if (e.label) {
      const L = path.getTotalLength(), m = path.getPointAtLength(L * 0.5), d = document.createElement('div');
      d.className = 'el' + (e.accent ? ' a' : ''); d.textContent = e.label; d.style.left = m.x + 'px'; d.style.top = m.y + 'px'; dg.appendChild(d);
    }
  }
})();
"""


def page(s):
    b = BRANDS[s["brand"]]
    vars_ = ";".join(f"--{k}:{v}" for k, v in b.items() if k != "name")
    fonts = open(os.path.join(HERE, "ig-fonts.css")).read() + open(os.path.join(HERE, "fonts.css")).read()
    if s["layout"] == "poster":
        L, R, T = s["left"], s["right"], s["twist"]
        col = lambda c, m: (f'<div class="col"><div class="tag">{fmt(c["tag"])}</div><div class="big">{c.get("emoji","")}</div>'
                            f'<div class="cap">{fmt(c.get("caption",""))}</div><ul>{lis(c["items"], m)}</ul></div>')
        inner = (f'<div class="frame"><div class="ph"><h1>{fmt(s["title"])}</h1><div class="kk">{fmt(s.get("kicker",""))}</div></div>'
                 f'<div class="cols">{col(L, "✓")}{col(R, "★")}</div>'
                 f'<div class="bot"><div class="tw"><div class="tag">{fmt(T["tag"])}</div><p>{fmt(T["text"])}</p>'
                 + (f'<div class="psrc">{fmt(s["source"])}</div>' if s.get("source") else "") +
                 f'</div><div class="pn"><div>{fmt(s["punch"])}</div></div></div></div>')
        return (f'<!doctype html><html class="poster"><head><meta charset="utf-8"><style>{fonts}{CSS}</style></head>'
                f'<body style="{vars_}" class="poster"><div class="page">{inner}</div></body></html>')
    foot = (f'<div class="foot"><div class="save">{fmt(s.get("save", ""))}</div>'
            + f'<div class="src">{("Source: " + fmt(s["source"])) if s.get("source") else ""}</div></div>')
    t = fmt(s["title"])
    t = re.sub(r"([.?!])$", r'<span class="dot">\1</span>', t)
    inner = (f'<div class="kick">{fmt(s["kicker"])}</div><h1>{t}</h1>'
             + (f'<div class="sub">{fmt(s["sub"])}</div>' if s.get("sub") else "")
             + f'<div class="body">{body(s)}</div>{foot}<script>document.fonts.ready.then(()=>{{{WIRE_JS}}})</script>')
    return (f'<!doctype html><html><head><meta charset="utf-8"><style>{fonts}{CSS}</style></head>'
            f'<body style="{vars_}"><div class="page">{inner}</div></body></html>')


def render(paths):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    from PIL.PngImagePlugin import PngInfo
    bad = 0
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for path in paths:
            s = json.load(open(path))
            errs = check(s)
            if errs:
                print(f"{path}:\n  " + "\n  ".join(errs)); bad += 1; continue
            out = os.path.join(HERE, "out", s["key"]); os.makedirs(out, exist_ok=True)
            hp = os.path.join(HERE, f".ig-{s['key']}.html")
            open(hp, "w").write(page(s))
            pg.goto("file://" + hp); pg.wait_for_timeout(900)
            over = pg.evaluate("""() => { const o=[]; const P=document.querySelector('.page');
              if (P.scrollHeight>1351) o.push('page '+P.scrollHeight);
              const f=document.querySelector('.frame'); if (f && f.scrollHeight>f.clientHeight+1) o.push('frame');
              document.querySelectorAll('.body,.cols,.col').forEach(e=>{ if(e.scrollHeight>e.clientHeight+2) o.push(e.className)});
              return o; }""")
            raw = os.path.join(out, "raw.png"); pg.screenshot(path=raw)
            os.remove(hp)
            if over:
                print(f"{s['key']}: overflow in {over} - shorten the text"); bad += 1; continue
            meta = PngInfo(); meta.add_text("comment", "card-look:Infographic")
            Image.open(raw).convert("RGB").save(os.path.join(out, f"{s['key']}.png"), pnginfo=meta, optimize=True)
            os.remove(raw)
            print(f"{s['key']}: out/{s['key']}/{s['key']}.png")
        br.close()
    return 1 if bad else 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--check"]:
        rc = 0
        for p in a[1:]:
            e = check(json.load(open(p))); print(p, "ok" if not e else "\n  " + "\n  ".join(e)); rc |= bool(e)
        sys.exit(rc)
    sys.exit(render(a))
