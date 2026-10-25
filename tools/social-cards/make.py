import os, html, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

BRANDS = {
 "pe": dict(name="Presso Events", bg="#f7f3ea", ink="#141414", acc="#1f56d6", hi="#f39a2b", soft="#fde9a8", ok="#9ccc4c",
            url="presso.events/blog/event-networking-without-an-app-download"),
 "co": dict(name="Corey", bg="#f2eee2", ink="#151515", acc="#4f7a24", hi="#f07c22", soft="#f8d75a", ok="#9ccc4c",
            url="getcorey.ai/blog/what-a-claude-skill-actually-is-and-what-it-isn-t"),
}

CSS = open(os.path.join(OUT,"fonts.css")).read() + """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{background:var(--bg);color:var(--ink);font-family:Inter,sans-serif;padding:64px 70px 56px;display:flex;flex-direction:column;
 background-image:radial-gradient(rgba(0,0,0,.05) 1px,transparent 1px);background-size:14px 14px}
.bar{position:absolute;left:0;top:0;width:1080px;height:14px;background:var(--acc)}
.kick{font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:24px;letter-spacing:4px;text-transform:uppercase;color:var(--acc);margin-bottom:22px}
h1{font-family:'Instrument Serif',serif;font-weight:400;font-size:82px;line-height:.98;letter-spacing:-.5px;margin-bottom:22px}
h1 em{font-style:normal;background:linear-gradient(transparent 58%,var(--hi) 58%,var(--hi) 92%,transparent 92%)}
.sub{font-size:27px;line-height:1.35;color:#3a3a3a;margin-bottom:30px;max-width:900px}
.main{flex:1;display:flex;flex-direction:column}
.foot{display:flex;justify-content:space-between;align-items:flex-end;border-top:2px solid var(--ink);padding-top:18px;margin-top:24px;
 font-family:'IBM Plex Mono',monospace;font-size:17px;color:#444}
.foot b{font-family:Inter;font-weight:800;font-size:24px;color:var(--ink);letter-spacing:.3px}
.mono{font-family:'IBM Plex Mono',monospace}
/* panels */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;flex:1}
.pan{border:4px solid var(--ink);background:#fff;display:flex;flex-direction:column;box-shadow:7px 7px 0 var(--ink)}
.pan .ph{background:var(--soft);border-bottom:4px solid var(--ink);padding:12px 18px;font-family:'IBM Plex Mono',monospace;font-size:19px;font-weight:600;letter-spacing:2px;text-transform:uppercase}
.pan .pb{padding:20px 22px;font-size:31px;line-height:1.3;flex:1}
.pan .pb .code{display:inline-block;font-family:'IBM Plex Mono',monospace;font-weight:600;font-size:50px;border:3px dashed var(--ink);padding:6px 14px;margin:10px 0 4px;background:var(--bg)}
.pan .pb .say{display:block;margin-top:12px;background:var(--ink);color:#fff;border-radius:16px;padding:14px 18px;font-size:27px;line-height:1.3}
.pan.moral{background:var(--acc);color:#fff}
.pan.moral .ph{background:var(--hi);color:var(--ink)}
.pan.moral .pb{font-family:'Instrument Serif',serif;font-size:62px;line-height:1.05;display:flex;align-items:center}
/* stats */
.stat{display:flex;align-items:center;gap:34px;border-top:3px solid var(--ink);padding:26px 0}
.stat:last-of-type{border-bottom:3px solid var(--ink)}
.stat .n{font-family:'Instrument Serif',serif;font-size:150px;line-height:.85;min-width:330px;color:var(--acc)}
.stat .t{font-size:30px;line-height:1.3}
.stat .t b{display:block;font-size:34px;margin-bottom:4px}
.src{font-family:'IBM Plex Mono',monospace;font-size:17px;color:#555;margin-top:14px}
/* before/after */
.ba{display:grid;grid-template-columns:1fr 1fr;gap:22px;flex:1}
.col{border:4px solid var(--ink);display:flex;flex-direction:column}
.col h3{font-family:'IBM Plex Mono',monospace;font-size:22px;letter-spacing:3px;text-transform:uppercase;padding:14px 18px;border-bottom:4px solid var(--ink)}
.col.b h3{background:#e9e4d7}.col.a h3{background:var(--ok)}
.col ul{list-style:none;padding:8px 20px 18px;flex:1}
.col li{font-size:30px;line-height:1.3;padding:14px 0;border-bottom:2px dashed rgba(0,0,0,.25)}
.col li:last-child{border-bottom:none}
.col.b li{color:#5a5a5a}
.verdict{margin-top:22px;background:var(--ink);color:#fff;padding:22px 26px;font-family:'Instrument Serif',serif;font-size:44px;line-height:1.1}
.verdict em{font-style:normal;color:var(--soft)}
pre.snap{font-family:'IBM Plex Mono',monospace;font-size:23px;line-height:1.55;white-space:pre-wrap;padding:14px 18px;flex:1}
pre.snap .warn{background:var(--hi);color:#000;font-weight:600}
/* checklist */
.chk{list-style:none;flex:1}
.chk li{display:flex;gap:24px;align-items:flex-start;padding:28px 0;border-bottom:2px solid rgba(0,0,0,.15);font-size:29px;line-height:1.3}
.chk li .box{flex:0 0 46px;height:46px;border:4px solid var(--ink);background:#fff;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:800;color:var(--acc);margin-top:2px}
.chk li b{display:block;font-size:35px;margin-bottom:4px}
.chk li span.d{color:#444;font-size:28px}
/* question */
.q{flex:1;display:flex;flex-direction:column}
.scene{border-left:10px solid var(--hi);padding:6px 0 6px 28px;margin-bottom:30px}
.scene p{font-size:38px;line-height:1.35;margin:6px 0}
.big{font-family:'Instrument Serif',serif;font-size:132px;line-height:.98;margin:10px 0 34px}
.ans{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:auto}
.ans div{border:4px solid var(--ink);padding:22px 24px;font-size:29px;line-height:1.3;background:#fff}
.ans div b{display:block;font-family:'IBM Plex Mono',monospace;font-size:20px;letter-spacing:2px;text-transform:uppercase;margin-bottom:10px}
.ans .bad{background:#e9e4d7}.ans .good{background:var(--ok)}
/* myths */
.myth{display:grid;grid-template-columns:1fr 1fr;border-top:3px solid var(--ink)}
.myth:last-of-type{border-bottom:3px solid var(--ink)}
.myth div{padding:24px 20px;font-size:29px;line-height:1.3}
.myth .m{color:#333;background:rgba(0,0,0,.035);border-right:3px solid var(--ink)}
.myth .m s{text-decoration:none}
.myth .f{background:rgba(255,255,255,.7)}
.myth .lab{display:block;font-family:'IBM Plex Mono',monospace;font-size:17px;letter-spacing:2px;font-weight:600;margin-bottom:6px}
.myth .m .lab{color:#c8102e}.myth .f .lab{color:var(--acc)}
.eq{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:6px 0 28px}
.eq .t{border:4px solid var(--ink);background:#fff;box-shadow:6px 6px 0 var(--ink);padding:16px 10px;text-align:center;flex:1}
.eq .t b{display:block;font-family:'Instrument Serif',serif;font-size:46px;font-weight:400;line-height:1}
.eq .t span{font-size:20px;color:#444;display:block;margin-top:6px;line-height:1.25}
.eq .op{font-family:'Instrument Serif',serif;font-size:60px}
.eq .t.r{background:var(--acc);color:#fff}.eq .t.r span{color:#e8f0dc}
"""

def page(brand, kick, title, body, sub="", url=None):
    b = BRANDS[brand]
    vars_ = f"--bg:{b['bg']};--ink:{b['ink']};--acc:{b['acc']};--hi:{b['hi']};--soft:{b['soft']};--ok:{b['ok']}"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>:root{{{vars_}}}{CSS}</style></head>
<body><div class="bar"></div><div class="kick">{e(kick)}</div><h1>{title}</h1>{f'<div class="sub">{sub}</div>' if sub else ''}
<div class="main">{body}</div>
<div class="foot"><span>{e(url or b['url'])}</span><b>{e(b['name'])}</b></div></body></html>"""

def panels(items):
    out = '<div class="grid">'
    for h, body, cls in items:
        out += f'<div class="pan {cls}"><div class="ph">{h}</div><div class="pb">{body}</div></div>'
    return out + '</div>'

def stats(rows, src=""):
    s = "".join(f'<div class="stat"><div class="n">{n}</div><div class="t"><b>{b}</b>{t}</div></div>' for n, b, t in rows)
    return s + (f'<div class="src">{e(src)}</div>' if src else "")

def ba(before, after, verdict, bh="Before", ah="After", raw=False):
    def col(cls, h, items):
        if raw: return f'<div class="col {cls}"><h3>{h}</h3>{items}</div>'
        return f'<div class="col {cls}"><h3>{h}</h3><ul>' + "".join(f"<li>{i}</li>" for i in items) + "</ul></div>"
    return f'<div class="ba">{col("b", bh, before)}{col("a", ah, after)}</div><div class="verdict">{verdict}</div>'

def checklist(items):
    return '<ul class="chk">' + "".join(f'<li><div class="box">&#10003;</div><div><b>{t}</b><span class="d">{d}</span></div></li>' for t, d in items) + '</ul>'

def question(scene, big, bad, good):
    sc = "".join(f"<p>{s}</p>" for s in scene)
    return f'<div class="q"><div class="scene">{sc}</div><div class="big">{big}</div><div class="ans"><div class="bad"><b>{bad[0]}</b>{bad[1]}</div><div class="good"><b>{good[0]}</b>{good[1]}</div></div></div>'

def myths(rows):
    return "".join(f'<div class="myth"><div class="m"><span class="lab">MYTH</span><s>{m}</s></div><div class="f"><span class="lab">FACT</span>{f}</div></div>' for m, f in rows)

CARDS = {}

# ---------------- Presso Events, week 44: networking without an app download ----------------
CARDS["pe-1-story"] = page("pe", "The coffee break, watched properly", "What \"Coffee and networking\" <em>actually looks like</em>", panels([
  ("Minutes 1 to 8", "The coffee queue. The most social part of the break, and nobody planned it.", ""),
  ("Minutes 8 to 12", "Colleagues find colleagues. The one person who came alone reads the agenda again.", ""),
  ("Minutes 12 to 18", "Phones out. Not to network. To answer the email from the keynote.", ""),
  ("Minutes 18 to 20", "\"Should we head back in?\" A slot is not a plan.", "moral"),
]), sub="Your agenda says \"10:30 Coffee and networking\". Your attendees read it as \"10:30 Coffee\".")

CARDS["pe-2-numbers"] = page("pe", "The download gate, counted", "Why the networking app <em>misses the room</em>", stats([
  ("20-30%", "download an event app", "without a real push."),
  ("80-95%", "is where events get to", "mostly by making the app mandatory for check-in."),
  ("30%", "the starting point", "in a native app vendor's own headline about adoption."),
  ("1 in 16", "both of you installed it", "at 25% adoption. Networking needs two people."),
], src="Sources: Nunify, Event App Adoption Rate Benchmarks, 2025; Whova blog, \"From 30% to 90%\", 2018"))

CARDS["pe-3-beforeafter"] = page("pe", "Same break, two run sheets", "A time and a room, <em>or a job</em>", ba(
  ["\"13:00 Lunch and networking. Atrium.\"", "Nobody knows who is in the room", "No reason to approach a stranger", "No first line to say", "An app a quarter of the room installed"],
  ["Who's coming, shown before the day", "Name or anonymous, and it's symmetric", "A prompt: ask someone from another industry about their worst event", "All of it on the ticket-email link", "Nothing to install"],
  "The fix is not more time. <em>It is information.</em>",
  bh="The networking slot", ah="A break with a job"))

CARDS["pe-4-checklist"] = page("pe", "Run sheet audit", "Three questions for every <em>\"networking\"</em> line", checklist([
  ("Find every line that says \"networking\"", "Open your run sheet. Search for the word. Count them."),
  ("Who is in the room?", "If attendees can't find out before the break, they spend the break finding out."),
  ("What is the first line?", "A prompt, a question or a reason. Borrowed words beat invented ones."),
  ("Where does it live?", "If it's in an app they need to install, assume a quarter of the room sees it."),
  ("No answers? Call it a coffee break", "That's fine. Just stop measuring it as networking."),
]))

CARDS["pe-5-question"] = page("pe", "A thought experiment", "", question(
  ["You came alone.", "Twenty minutes of break.", "A room full of strangers holding coffee."],
  "Who do you walk up to?",
  ("No information", "Whoever is nearest the urn. Or nobody, and back to your inbox."),
  ("A who's-coming list", "You already know there are three heads of events and one person from a museum."),
))

CARDS["pe-6-myths"] = page("pe", "Myth vs fact", "Five things organisers believe <em>about networking</em>", myths([
  ("Put networking on the agenda and people network.", "A slot is a room booking with a hopeful label."),
  ("People don't network because they're shy.", "They can't tell which stranger is worth ten of their twenty minutes."),
  ("A networking app fixes it.", "It only reaches people who installed it. Usually 20-30% (Nunify, 2025)."),
  ("More features win.", "Fewer features everyone sees beat more features a quarter of the room sees."),
  ("An attendee list kills privacy.", "Let people stay anonymous, symmetrically: hide your name, see roles, not names."),
]))

# ---------------- Corey, week 44: what a Claude skill is, and isn't ----------------
CARDS["co-1-story"] = page("co", "What a Claude skill is", "A runbook Claude <em>reads first</em>", panels([
  ("1 · A folder", "Markdown files in a GitHub repo: instructions, examples, house rules. Versioned and diffable.", ""),
  ("2 · Read at the start", "Claude reads it before the task, the way you'd hand a new hire a runbook.", ""),
  ("3 · Guessing stops", "Which repo owns which ticket. Your test command. Which error means \"check the fixture\".", ""),
  ("4 · The point", "Same Claude. It just read the manual first.", "moral"),
]), sub="No new model. No fine-tuning. Nothing running alongside Claude.")

CARDS["co-2-numbers"] = page("co", "One bug, counted", "A confident fix, <em>by the numbers</em>", stats([
  ("0", "new models", "in a Claude skill. No fine-tuning either. It's a folder of text."),
  ("4 days", "earlier", "the locale problem I \"fixed\" had already been fixed, in a different file."),
  ("2", "ways the fix was wrong", "Solved a solved problem, and the error never said locale. It said UTF-8."),
  ("1", "place to fix it", "Where a file is read from disk. Scrub the byte, with a test that writes it."),
], src="Source: Corey build log, 21/09/2026"))

CARDS["co-3-beforeafter"] = page("co", "Same error, two habits", "Reproduce <em>the exact error</em>", ba(
  ["Production: invalid byte sequence in UTF-8", "Local repro: US-ASCII", "Same neighbourhood. Must be locale", "Ship a locale fix", "Green CI. Wrong fix."],
  ["Production: invalid byte sequence in UTF-8", "Local repro must say UTF-8 too", "It doesn't. That gap is the finding", "Find where the byte comes in", "Scrub it there, test the exact byte"],
  "Wrong but shipped and right <em>look the same in green CI.</em>",
  bh="Close enough", ah="Exact match"))

CARDS["co-4-checklist"] = page("co", "Your first skill", "What to write down <em>once</em>", checklist([
  ("What you retype every session", "Which repo owns which kind of ticket. Your test command."),
  ("Which error means what", "\"Check the fixture\", not \"check the code\"."),
  ("Your house rules", "The things a new hire would get wrong in week one."),
  ("Keep it in a repo", "Versioned, diffable, and pull-requestable when it's wrong."),
  ("Add each lesson as you learn it", "Work out why you were wrong, then write it down once."),
]))

CARDS["co-5-question"] = page("co", "A thought experiment", "", question(
  ["Your local repro throws an error.", "It isn't the one in production.", "Same neighbourhood. Your fix is ready."],
  "Ship it, or stop?",
  ("The usual move", "Ship. Same neighbourhood feels like confirmation."),
  ("The rule I keep", "Stop. The gap between the two errors is the finding."),
))

CARDS["co-6-myths"] = page("co", "Myth vs fact", "What a Claude skill <em>is not</em>", myths([
  ("A skill makes Claude smarter.", "Same Claude. It stops guessing at what you already wrote down."),
  ("It's a new model or a fine-tune.", "It's a folder of markdown files in a repo."),
  ("A skill checks its own facts.", "It can't notice its instructions have gone stale."),
  ("A skill stops you being wrong.", "It means you only write down why you were wrong once."),
  ("Plausible and correct look different.", "From the inside, they read identically."),
]))

if __name__ == "__main__":
    only = sys.argv[1:]
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for k, h in CARDS.items():
            if only and k not in only: continue
            open(os.path.join(OUT, k + ".html"), "w").write(h)
            pg.goto("file://" + os.path.join(OUT, k + ".html"))
            pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(400)
            png = os.path.join(OUT, k + ".png")
            pg.screenshot(path=png)
            # Quantise and write the card-look tag here, not as a separate step someone
            # can forget: an untagged card is refused by the pre-publish review and held
            # in drafts by the link sentinel (20/10/2026, the whole week-43 rhythm).
            finish.main([png, png])
            sh = pg.evaluate("document.documentElement.scrollHeight")
            print(k, "overflow" if sh > 1350 else "ok", sh)
        br.close()
