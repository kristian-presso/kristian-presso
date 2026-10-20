"""Finish a rendered card for Buffer: quantise to 128 colours and write the look tag.

    python3 finish.py <rendered.png> <assets/social/<brand>/<name>.png>
    python3 finish.py --tag-only <assets/social/.../*.png>   # tag cards already published

THE LOOK TAG IS NOT OPTIONAL. PressoNetwork/operator's pre-publish review
(scripts/_lib/post_review.py) refuses any card whose PNG carries no `card-look:<Look>`
comment, and the daily buffer-link-sentinel moves such a post back to drafts. On
20/10/2026 that is exactly what happened to the week-43 rhythm: these cards had no tag,
so Tuesday to Thursday on Presso Events sat in drafts and never posted. Every card made
here is the "Rhythm" look.
"""
import sys
from PIL import Image
from PIL.PngImagePlugin import PngInfo

LOOK = "Rhythm"


def save(img, dest):
    meta = PngInfo()
    meta.add_text("comment", f"card-look:{LOOK}")
    img.save(dest, pnginfo=meta, optimize=True)


def main(argv):
    if argv[:1] == ["--tag-only"]:
        for path in argv[1:]:
            save(Image.open(path), path)
            print("tagged", path)
        return 0
    src, dest = argv
    img = Image.open(src).convert("RGB").quantize(colors=128, method=Image.Quantize.MEDIANCUT)
    save(img, dest)
    print("finished", dest)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
