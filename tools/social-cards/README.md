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
