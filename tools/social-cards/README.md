# Social cards

Weekly LinkedIn cards for Presso Events and Corey (and the format used for Kristian's weeks).

- `make.py` holds the brand tokens, six layouts (four-panel story, numbers, before/after, checklist, question, myth vs fact) and the week's card content in `CARDS`.
- Replace the `CARDS` entries for the new week, then run `python3 make.py` (needs Playwright with Chromium). Each card renders at 2160x2700.
- Finish each card with `python3 finish.py <rendered.png> assets/social/<brand>/<yyyy-mm>-w<week>-<n>-<format>.png`: it quantises to 128 colours and writes the `card-look:Rhythm` tag. **The tag is required.** The pre-publish review in PressoNetwork/operator (`scripts/_lib/post_review.py`) refuses an untagged card, and the daily Buffer sentinel moves its post to drafts. Commit the result on this branch.
- Public URL: `https://raw.githubusercontent.com/kristian-presso/kristian-presso/social-assets/assets/social/...`

## Carousels (LinkedIn document posts)

- `carousel.py` renders a carousel in the same look: one 1080x1350 PDF page per slide, plus `<key>-cover.png` (slide one at 2160x2700, finished and look-tagged) for the Buffer document thumbnail. Needs Playwright and pypdf.
- Slide one has to work alone (most people never swipe), one idea per slide, and no URL, logo or call to action on any slide.
- In Buffer the post carries a `document` asset (PDF url, title, cover as `thumbnailUrl`). The pre-publish review only inspects `image` assets, so a document post passes it.
- Two looks. Rhythm (Presso Events, Corey): the myth is a speech bubble, the scene is drawn, the fact is a caption box. Comic (Kristian): his strip look, one panel per slide, with the two robots.
- `scenes.py` holds the drawings as hand-written SVG, coloured by the slide's brand variables, so a scene renders identically every time. Objects only for Presso Events and Corey (no invented mascot); the robots are Kristian's existing characters.
- Done so far: both week-43 myth-vs-fact posts (24/10/2026) and Kristian's pushback post (26/10/2026, `assets/social/kristian/`).

## Comic carousels (the default from 27/10/2026)

Every post is a hook, a lesson, a laugh and a picture that teaches (operator `skills/_lib/social-engaging-format.md`). The text cards in `make.py` failed that test for a week, so the weekly rhythm now draws a comic carousel per post.

- `cast.py` draws the mascots as SVG, with moods and poses: Corey's green sprout, Presso Events' blue phone, Kristian's robots.
- `comic.py` turns a JSON spec (`specs/<key>.json`) into `out/<key>/<key>.pdf` (the LinkedIn document), `cover.png` and `slide-<n>.png` (for X, up to 4 images), all tagged `card-look:Comic`. `python3 comic.py --check specs/x.json` validates without rendering. The docstring lists the slide types.
- Slide one is the whole claim; the cast acts the story out; no URL, logo or call to action on a slide.
- Copy the PDF and cover to `assets/social/<brand>/<yyyy-mm>-w<week>-<n>-<format>-comic.pdf` and `-comic-cover.png`, commit on this branch, and post the PDF as a Buffer document asset with the cover as `thumbnailUrl`.

## Cartoon panels (OpenAI), mixed with our infographic slides

Since 28/10/2026 (Kristian: "use ChatGPT to make these carousel images so they look good and like
real cartoons, and then mix it up with the infographic types you can make yourself") every carousel
mixes real cartoon panels with slides we draw:

- Cartoons: a `cover` with a `scene`, `cartoon` slides, and `panel` / `myth` slides with a `scene`.
  The scene is a brief for the illustrator and is never shown. Every word on a slide is ours.
- Ours: `list`, `stat`, `versus` and the closing `moral`.

How the art is made:

1. Push a spec to `social-assets`.
2. The GitHub Action "Draw cartoon art" (`.github/workflows/draw-art.yml`) runs `draw.py --missing`.
   It sends each scene to OpenAI's image model (`gpt-image-2`, medium quality), with the mascot
   sheet in `ref/` as a reference image so Corey and Phoney stay on model. Then it commits
   `art/<key>/<n>.jpg`.
3. Pull, then run `comic.py`. A cartoon slide with no art stops the render.

The API key is the repo's `OPENAI_IMAGE_API_KEY` Actions secret (from Doppler `presso/prd`). It is
never in a session or a prompt. A panel is never redrawn once it exists.
