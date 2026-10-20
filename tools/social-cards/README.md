# Social cards

Weekly LinkedIn cards for Presso Events and Corey (and the format used for Kristian's weeks).

- `make.py` holds the brand tokens, six layouts (four-panel story, numbers, before/after, checklist, question, myth vs fact) and the week's card content in `CARDS`.
- Replace the `CARDS` entries for the new week, then run `python3 make.py` (needs Playwright with Chromium). Each card renders at 2160x2700.
- Finish each card with `python3 finish.py <rendered.png> assets/social/<brand>/<yyyy-mm>-w<week>-<n>-<format>.png`: it quantises to 128 colours and writes the `card-look:Rhythm` tag. **The tag is required.** The pre-publish review in PressoNetwork/operator (`scripts/_lib/post_review.py`) refuses an untagged card, and the daily Buffer sentinel moves its post to drafts. Commit the result on this branch.
- Public URL: `https://raw.githubusercontent.com/kristian-presso/kristian-presso/social-assets/assets/social/...`
