# Assets

| File | Size | Content |
|------|------|---------|
| `screenshots/en/screenshot-1-browser.png` | 1280x800 | Full-window mockup of the themed browser |
| `screenshots/en/screenshot-2-introduction.png` | 1280x800 | Theme intro with the 2x2 colour cards (white page, so the petal-white card reads) |
| `promo/440x280.png` | 440x280 | Brand tile |
| `promo/1400x560.png` | 1400x560 | Marquee with a scaled window preview |
| `../logo/logo128.png` | 128x128 | Theme mark: leaf on a white rounded card |

The four store images are rendered from one source by
`scripts/generate-store-assets.py` -> `scripts/generate-references.py` (Playwright
headless Chromium). The icon is drawn by `scripts/generate_logo.py` and embedded
in the brand tile, so re-render the assets after changing it.

## Calibration

The window is authored in a 1080x675 pixel space and rasterised at a matching
device scale factor, so the 1280x800 shot stays crisp instead of being upscaled.
Geometry was checked against the user's real 1080x650 window with this theme
installed (2026-09-20): 34px tab strip / 32px toolbar / 28px bookmark bar, the
Google mark at 191x62 starting at y=191, the new tab search field 529x40 at
(276, 283), shortcut circles 33px on a 112px pitch at y=342, and the
"Customize Chrome" pill at 12px from the right and bottom edges. The omnibox is
660x28, left aligned after the nav buttons, with the active tab last - exactly as
in that capture.

Theme-controlled colours are read from `manifest.json` on every run (frame,
toolbar, background_tab, tab_text, tab_background_text, toolbar_button_icon,
bookmark_text, omnibox_background, ntp_background, ntp_text). Everything Chrome
paints itself is hardcoded and sampled from that same capture:

- New tab Google mark `#EF6F9F` and shortcut circle fill `#F49CBD`. Chrome derives
  both from `ntp_background` (`#FEF6F9`, H337 S80%) keeping hue and saturation and
  clamping lightness - `#EF6F9F` is L69%, the circles L78%. Rule verified against
  two older installs where a near-neutral background gave L66% (`#B6B69A`, `#CEAF84`).
- Omnibox fill `#E0CAD5` - Chrome blends the omnibox against the themed toolbar
  instead of using `omnibox_background` (`#FBFFF5`) directly. No focus ring is
  drawn, matching the capture.
- "Customize Chrome" pill `#202124` with a `#8AB4F8` label; apps grid and mic
  glyphs `#444746`; placeholder grey `#5F6368`.
- The new tab top-right shows just "Images" plus the apps grid, and the search
  field carries a magnifier on the left and a mic + brand-coloured Google Lens
  glyph on the right - as in the capture.

## Regenerating

```
python3 scripts/generate_logo.py           # -> logo/logo128.png
python3 scripts/generate-store-assets.py   # -> all four store images
```

Style changes are always applied by editing the script and re-rendering the whole
set; single-image patching is not used.
