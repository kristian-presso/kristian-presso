# Social cards

Weekly LinkedIn cards for Presso Events and Corey (and the format used for Kristian's weeks).

- `make.py` holds the brand tokens, six layouts (four-panel story, numbers, before/after, checklist, question, myth vs fact) and the week's card content in `CARDS`.
- Replace the `CARDS` entries for the new week, then run `python3 make.py` (needs Playwright with Chromium). Each card renders at 2160x2700.
- Compress with Pillow (quantize to 128 colours) and commit to `assets/social/<brand>/<yyyy-mm>-w<week>-<n>-<format>.png` on this branch.
- Public URL: `https://raw.githubusercontent.com/kristian-presso/kristian-presso/social-assets/assets/social/...`
