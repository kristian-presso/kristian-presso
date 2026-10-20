import os, html, sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import finish  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
e = html.escape

BRANDS = {
 "pe": dict(name="Presso Events", bg="#f7f3ea", ink="#141414", acc="#1f56d6", hi="#f39a2b", soft="#fde9a8", ok="#9ccc4c",
            url="presso.events/blog/check-people-in-from-your-phone-nothing-to-download"),
 "co": dict(name="Corey", bg="#f2eee2", ink="#151515", acc="#4f7a24", hi="#f07c22", soft="#f8d75a", ok="#9ccc4c",
            url="getcorey.ai/blog/what-an-ai-co-founder-is-and-is-not"),
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

# One-off launch card (20/10/2026): the /prompts builder, outside the weekly rhythm.
CARDS["pe-launch-prompts"] = page("pe", "New in the toolkit", "Same event. <em>Two first messages.</em>", ba(
  ["A blank chat box and a vague idea", "\"Create an event\" and twelve follow-up questions", "A price or a venue guessed, then corrected", "Not sure the connector is even on", "Twenty minutes to get one event right"],
  ["Pick the job: event, tickets, agenda, publish, door", "Fill in only the details that change", "Open the finished prompt in Claude", "It checks the connector first, and asks before it guesses", "Nothing to install, nothing stored"],
  "The fastest way to learn to prompt is a good prompt <em>with your own event in it.</em>",
  bh="The blank box", ah="The prompt builder"),
  sub="A prompt builder for running your event from Claude: nine jobs, a few boxes each, one click to open.",
  url="presso.events/prompts")

# ---------------- Presso Events: check-in from your phone ----------------
CARDS["pe-1-door"] = page("pe", "The door, explained", "Check-in with <em>nothing to download</em>", panels([
  ("1 · They arrive", 'A ticket email. The code is inside it, as text and as a scannable image:<br><span class="code">7HK-2M9</span>', ""),
  ("2 · You ask", 'From the phone in your hand, in the assistant you already use:<span class="say">Check in ticket code 7HK-2M9 for Spring Founders Supper.</span>', ""),
  ("3 · It answers", "The ticket is marked present. The reply names the event, the ticket type and the attendee's email, so you know it's the right person.", ""),
  ("4 · The moral", "No scanner. No app. No login at 6:58pm.", "moral"),
]))

CARDS["pe-2-numbers"] = page("pe", "The door in numbers", "Everything you need at the door, <em>counted</em>", stats([
  ("0", "downloads", "Not for you, not for them. The event app opens in the browser from the ticket email."),
  ("6", "characters in a code", "Shown like 7HK-2M9. Hyphens, spaces and capitals don't matter. I and L read as 1, O reads as 0."),
  ("1", "phone", "The one already in your hand. No scanner hardware to hire, charge or return."),
  ("2nd", "scan is safe", "The same code twice says it was already checked in, and when. Nobody is counted twice."),
]))

CARDS["pe-3-beforeafter"] = page("pe", "Same queue, two doors", "Fifty people. <em>One door.</em>", ba(
  ["A scanner app someone has to install", "A laptop that needs a login", "A printed list and a pen", "Someone shouting names over the music", "Nobody sure who's actually in"],
  ["A code already in their ticket email", "Your phone, in the assistant you use", "A reply that names who just walked in", "A door board: in, still expected, no-code entries", "Refunded tickets refused automatically"],
  "The queue is a test of whether the person at the front <em>believes you have it under control.</em>",
  bh="The usual door", ah="Nothing installed"))

CARDS["pe-4-checklist"] = page("pe", "The night before", "Your door checklist, <em>done at home</em>", checklist([
  ("Buy or issue yourself a ticket", "Then check yourself in from the exact phone you'll use at the door."),
  ("Add the Presso Events connector", "In Claude in the browser or the Claude app you already have."),
  ("Decide on no-code entry now", "It's off by default. An owner switches it on calmly before doors, not in front of a crowd."),
  ("Put the door board on a screen", "How many are in, still expected, and admitted without a code."),
  ("Check the names setting", "Recent arrivals show a first name and last initial. Switch to full names only if you want to."),
]))

CARDS["pe-5-question"] = page("pe", "A quick test for organisers", "", question(
  ["Doors open at 7.", "Someone's at the front with a cracked screen,", "a phone on 2% and no idea where the ticket email went."],
  "What happens at your door?",
  ("The usual answer", "You scroll a printed list while the queue grows behind them, and wave them in on trust."),
  ("With Presso Events", "You find them by name. If an owner switched on no-code entry beforehand, they're in, recorded as a different kind of check-in."),
))

CARDS["pe-6-myths"] = page("pe", "Myth vs fact", "Five things organisers believe <em>about check-in</em>", myths([
  ("You need an event check-in app.", "You need a phone and a ticket code. Nothing to install on either side."),
  ("You need scanner hardware.", "The phone in your hand is the scanner."),
  ("No signal at the venue means no tickets.", "The code is inside the email itself, not behind a link."),
  ("A ticket used twice gets in twice.", "The second check-in says it was already used, and shows when."),
  ("Free events need a different process.", "A free ticket gets a check-in code like any other."),
]))

# ---------------- Corey: what an AI co-founder is and is not ----------------
CARDS["co-1-equation"] = page("co", "What an AI co-founder is", "A model plus <em>three things</em> it doesn't ship with",
  '<div class="eq"><div class="t"><b>Model</b><span>Claude, the one you already have</span></div><div class="op">+</div>'
  '<div class="t"><b>Facts</b><span>VAT quarter, year end, where the ledger lives</span></div><div class="op">+</div>'
  '<div class="t"><b>Method</b><span>Steps for a recurring job, written once</span></div><div class="op">+</div>'
  '<div class="t"><b>Limits</b><span>Never sends, pays or signs</span></div></div>'
  + panels([
   ("Chat assistant", "Answers the question you typed today. Brilliant every time, and every time it meets you for the first time.", ""),
   ("AI co-founder", "Owns the question you should ask every week, and knows what a good answer looks like.", ""),
   ("Take one away", "Remove any of the three and you're back to a very clever stranger.", ""),
   ("The point", "Same model. It's what sits around it.", "moral"),
  ]))

CARDS["co-2-numbers"] = page("co", "Why the dull jobs matter", "Late money is not <em>a rounding error</em>", stats([
  ("4 in 5", "smaller UK businesses in supply chains", "say they have been paid late."),
  ("1 in 3", "say at least a quarter", "of what they're owed arrives late."),
  ("38", "UK businesses a day", "close because of slow and late payment."),
  ("£11bn", "a year", "is what late payment costs the UK economy."),
], src="Sources: FSB research (Scottish Construction Now); Tina McKenzie, FSB (Printweek, 2025)"))

CARDS["co-3-sameask"] = page("co", "Same ask, run twice", "\"Who owes <em>me money?</em>\"", ba(
  ["It can't see your books, so you paste a CSV", "It totals whatever you gave it", "A filtered export still gives a confident number", "Next week: same paste, same explanation"],
  '<pre class="snap">As of 19/10/2026\nOwed: current £2,400\n 1-30 £1,150 | 31-60 £800\nOverdue: 3 invoices, £1,950\n Chase drafts ready\nYou owe: next 30 days £640\nVAT due in 18 days.\n Reserve covers it.\n<span class="warn">Bank feed: UNAVAILABLE\nPayments after 14/10\nnot counted.</span></pre>',
  "Look at the last line. <em>That's the whole difference.</em>",
  bh="Chat assistant", ah="A job (made-up data)", raw=True) if False else "", )

# Rebuild co-3 with raw columns properly
def ba_raw(before_items, after_html, verdict, bh, ah):
    b = '<div class="col b"><h3>' + bh + '</h3><ul>' + "".join(f"<li>{i}</li>" for i in before_items) + '</ul></div>'
    a = '<div class="col a"><h3>' + ah + '</h3>' + after_html + '</div>'
    return f'<div class="ba">{b}{a}</div><div class="verdict">{verdict}</div>'
CARDS["co-3-sameask"] = page("co", "Same ask, run twice", "\"Who owes <em>me money?</em>\"", ba_raw(
  ["It can't see your books, so you paste a CSV", "It totals whatever you gave it", "A filtered export still gives a confident number", "Next week: same paste, same explanation"],
  '<pre class="snap">As of 19/10/2026\nOwed: current £2,400\n 1-30 £1,150 | 31-60 £800\nOverdue: 3 invoices, £1,950\n chase drafts ready\nYou owe: £640 in 30 days\nVAT due in 18 days,\n reserve covers it\n<span class="warn">Bank feed: UNAVAILABLE.\nPayments after 14/10\nnot counted.</span></pre>',
  "Look at the last line. <em>That's the whole difference.</em>",
  "Chat assistant", "As a job (made-up data)"))

CARDS["co-4-checklist"] = page("co", "Test any AI setup", "Break it on purpose <em>before you trust it</em>", checklist([
  ("Ask it one question about money", "\"Who owes me money?\" is a good one."),
  ("Disconnect a feed", "Does it say unavailable, or hand you a tidy total anyway?"),
  ("Give it a half-filtered export", "Does it notice part of the picture is missing?"),
  ("Ask for last week's answer", "A job remembers it. A chat starts from a blank page."),
  ("Ask what it will never do", "Send, pay, file or sign should all be on the list."),
]))

CARDS["co-5-question"] = page("co", "A question for your dashboard", "", question(
  ["Your report says:", "<b>Overdue invoices: £0.</b>", "Your bank feed stopped syncing on the 3rd."],
  "Good month, or nobody looked?",
  ("Most reports", "Show 0. A missing source and a zero look identical on a dashboard."),
  ("The rule I follow", "A figure whose source is missing is shown as unavailable, never as a zero."),
))

CARDS["co-6-myths"] = page("co", "Myth vs fact", "What an AI co-founder <em>is not</em>", myths([
  ("It's a person.", "It carries no liability and can't sign a contract."),
  ("It's autopilot.", "It computes and drafts. Sending, paying and signing stay with you."),
  ("It's a smarter model.", "Same Claude you already have. If Claude were the bottleneck, it wouldn't help."),
  ("It replaces your accountant.", "It's a well-kept working file you bring to them."),
  ("You couldn't just ask Claude.", "You could. A skill is that typing, done once and kept."),
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
