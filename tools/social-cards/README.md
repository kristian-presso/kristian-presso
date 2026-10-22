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
- First run, week 43: both myth-vs-fact posts (Saturday 24/10/2026), Presso Events and Corey.
