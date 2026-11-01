#!/usr/bin/env python3
"""Draw a wide cartoon with BOTH mascots on model (Corey the sprout and Phoney the phone).

For page banners and other pieces where the studio shows its family of apps. draw.py sends one
reference sheet; this sends both, so neither character drifts. No words in the art: any text is
set by us on top.

Usage: OPENAI_IMAGE_API_KEY=... banner_art.py "<scene>" <out.png> [--size 1536x1024]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import draw  # noqa: E402


def banner(scene, out, size="1536x1024"):
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return "cached"
    key = os.environ.get("OPENAI_IMAGE_API_KEY")
    if not key:
        raise SystemExit("OPENAI_IMAGE_API_KEY is not set")
    prompt = (f"{draw.STYLE}\n\nTwo recurring characters, shown in the two reference images, must stay exactly "
              f"on model (same shape, colours, outline and face style): Corey, {draw.CAST['co'][2]}; and "
              f"Phoney, {draw.CAST['pe'][2]}. Other people are simple friendly cartoon humans.\n\n"
              f"The scene: {scene.strip()}\n\nHard rules: {draw.BANNED}")
    fields = {"model": draw.MODEL, "prompt": prompt, "size": size, "n": "1", "quality": "high"}
    files = [("image[]", os.path.join(HERE, "ref", "sprout.png")), ("image[]", os.path.join(HERE, "ref", "phone.png"))]
    body, ctype = draw._multipart(fields, files)
    import base64, json, urllib.request, urllib.error
    req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": ctype})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"banner failed {e.code}: {e.read()[:400].decode(errors='replace')}")
    item = d["data"][0]
    raw = base64.b64decode(item["b64_json"]) if item.get("b64_json") else urllib.request.urlopen(item["url"]).read()
    open(out, "wb").write(raw)
    return f"{os.path.getsize(out) // 1024}KB"


if __name__ == "__main__":
    a = sys.argv[1:]
    size = "1536x1024"
    if "--size" in a:
        i = a.index("--size"); size = a[i + 1]; del a[i:i + 2]
    print("banner:", banner(a[0], a[1], size))
