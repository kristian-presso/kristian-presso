#!/usr/bin/env python3
"""Draw one wordless cartoon panel with OpenAI's image model, keeping the brand mascot on model.

WHY THIS EXISTS (Kristian, 28/10/2026): "use ChatGPT to make these carousel images, so they look
good and like real cartoons, and then mix it up with the infographic types you can make yourself."
The hand-drawn SVG mascots in cast.py are fine for infographic slides; a story slide needs a real
cartoon scene. This draws that scene, and comic.py typesets our own words over it.

ON MODEL. The mascot sheet in ref/<brand>.png goes to the edits endpoint as a reference image, so
the sprout and the phone keep their shape, colours and face style from panel to panel. A text-only
prompt drifts: by panel three the sprout has grown a stalk and the phone has become a tablet.

NO TEXT IN THE ART. Image models misspell, and our no-invention rule forbids the model writing
copy we did not approve. Every word on a slide is ours, set by comic.py in HTML.

CACHED. An existing output is never redrawn: regenerating is where the money goes.

Usage: OPENAI_IMAGE_API_KEY=... draw.py <brand pe|co> "<scene>" <out.png> [--size 1024x1536]
"""
import base64, json, mimetypes, os, sys, urllib.error, urllib.request, uuid

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.environ.get("CARTOON_MODEL", "gpt-image-2")
QUALITY = os.environ.get("CARTOON_QUALITY", "medium")

CAST = {
    "co": ("Corey", "sprout.png",
           "a small round lime-green seed character with two leaves on top, a thick dark-green "
           "outline, rosy cheeks, simple dot eyes and two small leaf-like arms"),
    "pe": ("Phoney", "phone.png",
           "a friendly bright-blue smartphone character with a dark-navy outline, a face on its "
           "screen, a small white chevron logo low on the screen, thin arms with round hands and "
           "two short legs with oval feet"),
}

STYLE = (
    "A polished, funny 2D cartoon panel, like a great newspaper comic or a Pixar storyboard frame: "
    "bold clean outlines, bright saturated colours, cel shading, expressive exaggerated reactions "
    "and a visual gag in the background that rewards a second look. Simple bold-colour background "
    "so it pops on a phone. Leave the top quarter of the frame calm and uncluttered, because a "
    "caption will be set there. No photorealism, no 3D render."
)
BANNED = (
    "Absolutely no text, letters, words, numbers, digits, logos other than the mascot's own screen "
    "chevron, brand names, watermarks, signatures, speech bubbles or captions. Any screen, sign, "
    "paper or chart shows abstract shapes only."
)


def _multipart(fields, files):
    b = uuid.uuid4().hex
    out = []
    for k, v in fields.items():
        out += [f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()]
    for k, path in files:
        ct = mimetypes.guess_type(path)[0] or "application/octet-stream"
        out += [f"--{b}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{os.path.basename(path)}\"\r\n"
                f"Content-Type: {ct}\r\n\r\n".encode(), open(path, "rb").read(), b"\r\n"]
    out.append(f"--{b}--\r\n".encode())
    return b"".join(out), f"multipart/form-data; boundary={b}"


def draw(brand, scene, out, size="1024x1536"):
    if os.path.exists(out) and os.path.getsize(out) > 0:
        return "cached"
    key = os.environ.get("OPENAI_IMAGE_API_KEY")
    if not key:
        raise SystemExit("OPENAI_IMAGE_API_KEY is not set")
    name, ref, look = CAST[brand]
    prompt = (f"{STYLE}\n\nThe star is {name}, the character in the reference image: {look}. Keep "
              f"{name} exactly on model - same shape, colours, outline and face style as the "
              f"reference - in a new pose that fits the scene. Other people in the scene are "
              f"simple friendly cartoon humans.\n\nThe scene: {scene.strip()}\n\nHard rules: {BANNED}")
    fields = {"model": MODEL, "prompt": prompt, "size": size, "n": "1"}
    if QUALITY:
        fields["quality"] = QUALITY
    body, ctype = _multipart(fields, [("image[]", os.path.join(HERE, "ref", ref))])
    req = urllib.request.Request("https://api.openai.com/v1/images/edits", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": ctype})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except urllib.error.HTTPError as e:
        raise SystemExit(f"draw failed {e.code}: {e.read()[:400].decode(errors='replace')}")
    item = d["data"][0]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if item.get("b64_json"):
        open(out, "wb").write(base64.b64decode(item["b64_json"]))
    else:
        urllib.request.urlretrieve(item["url"], out)
    return f"{os.path.getsize(out) // 1024}KB"


if __name__ == "__main__":
    a = sys.argv[1:]
    size = "1024x1536"
    if "--size" in a:
        i = a.index("--size"); size = a[i + 1]; del a[i:i + 2]
    brand, scene, out = a
    print(f"draw: {os.path.basename(out)} {draw(brand, scene, out, size)}")
