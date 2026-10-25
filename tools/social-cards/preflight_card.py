"""Kristian's connector-preflight launch card (28/10/2026), Comic look, one 2160x2700 image.

    python3 preflight_card.py   # writes kp-connector-preflight.png (finished and look-tagged)
"""
import os
from playwright.sync_api import sync_playwright
import carousel as C
import finish

KP = C.KP
OUT = C.OUT

EXTRA = """
.find{display:flex;flex-direction:column;gap:18px;margin-top:30px}
.f{display:flex;align-items:center;border:6px solid var(--ink);box-shadow:9px 9px 0 var(--ink);background:#fff}
.f .x{background:%s;color:#fff;font-weight:900;font-size:64px;width:110px;align-self:stretch;display:flex;align-items:center;justify-content:center;border-right:6px solid var(--ink)}
.f .t{padding:16px 26px;font-size:37px;font-weight:800;line-height:1.15}
.f .t span{display:block;font-size:28px;font-weight:600;color:#333;margin-top:4px}
.mini{flex:0 0 auto;height:auto}
.mini .box{overflow:hidden}
.mini .pb{flex-direction:row;gap:18px;padding:18px 20px;justify-content:center}
.mini .pb p{font-size:38px;text-align:left}
""" % KP["red"]

body = (
    '<div class="box hdr" style="padding:34px 40px"><div class="kick">connector-preflight · free and open source</div>'
    '<h1 style="font-size:80px">My MCP servers looked ready.</h1><p>Then I ran the checker on all three.</p></div>'
    '<div class="mini">'
    f'<div class="box"><div class="ph" style="background:var(--ink)">WHAT I THOUGHT</div><div class="pb">{C.bot(KP["org"], "smile", 100)}<p>Ready to<br>submit &#11088;</p></div></div>'
    f'<div class="box"><div class="ph" style="background:{KP["red"]}">WHAT IT SAID</div><div class="pb">{C.bot(KP["blu"], "flat", 100)}<p>Two of three<br>had gaps</p></div></div>'
    '</div>'
    '<div class="find">'
    '<div class="f"><div class="x">&#10007;</div><div class="t">No offline_access scope<span>no refresh token, so people sign in again and again</span></div></div>'
    '<div class="f"><div class="x">&#10007;</div><div class="t">8 tool parameters with no description<span>Claude was guessing what to put in them</span></div></div>'
    '<div class="f"><div class="x">&#10007;</div><div class="t">Dynamic registration only<span>a new OAuth client on every fresh connection</span></div></div>'
    '</div>'
    '<div class="box hdr" style="margin-top:30px;padding:22px 36px"><h1 style="font-size:58px;letter-spacing:-2px">Check before you submit.</h1></div>'
)

html = C.comic_slide(body, 1, 1).replace('<div class="cnt"><span>1 / 1</span></div>', '').replace("</style>", EXTRA + "</style>", 1)

if __name__ == "__main__":
    path = os.path.join(OUT, "kp-connector-preflight.html")
    open(path, "w").write(html)
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        pg.goto("file://" + path)
        pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(300)
        sh = pg.evaluate("document.documentElement.scrollHeight")
        print("height", sh, "OVERFLOWS" if sh > 1350 else "fits")
        raw = os.path.join(OUT, "kp-connector-preflight-raw.png")
        pg.screenshot(path=raw)
        br.close()
    finish.main([raw, os.path.join(OUT, "kp-connector-preflight.png")])
