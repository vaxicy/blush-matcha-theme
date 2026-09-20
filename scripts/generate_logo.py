"""Blush Matcha theme - final icon generator (candidate 04 "leaf").

Draws the chosen leaf mark inside a white rounded-square card at 8x
supersampling and downsamples to the single size a Chrome theme needs: 128px.
The card matches the logo plate used on the promo tile.

Output: logo/logo128.png
Preview: <tmp>/blush-matcha-logo-preview.png (outside the repo)
"""

import math
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

SS = 8                      # supersample factor
SIZE = 128                  # Chrome themes only need 128
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "logo"

BLUSH = (251, 188, 207)
MATCHA = (170, 199, 146)
MATCHA_LT = (230, 247, 212)
CARD = (255, 255, 255)
CARD_RADIUS = 0.24          # corner radius as a fraction of the icon size
MARK_SCALE = 0.76           # mark size relative to the unpadded version


def mask_circle(S, cx, cy, r):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return m


def capsule_mask(S, p0, p1, width):
    """Straight line with rounded ends (no sharp corners)."""
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    d.line([p0, p1], fill=255, width=int(round(width)))
    r = width / 2
    for px, py in (p0, p1):
        d.ellipse([px - r, py - r, px + r, py + r], fill=255)
    return m


def leaf_mask(S, cx, cy, half_w, half_h, angle):
    """Pointed-oval leaf = intersection (lens) of two circles."""
    d = (half_h ** 2 - half_w ** 2) / (2 * half_w)
    r = half_w + d
    m = ImageChops.darker(mask_circle(S, cx - d, cy, r),
                          mask_circle(S, cx + d, cy, r))
    return m.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))


def build(scale=1.18, angle=-28):
    """White rounded card with the leaf mark, at S == SIZE * SS pixels."""
    S = SIZE * SS
    card = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    plate = Image.new("L", (S, S), 0)
    ImageDraw.Draw(plate).rounded_rectangle([0, 0, S - 1, S - 1],
                                            radius=CARD_RADIUS * S, fill=255)
    card.paste(Image.new("RGBA", (S, S), CARD + (255,)), (0, 0), plate)

    mark = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    cx = cy = 0.5 * S
    k = scale * MARK_SCALE
    half_w = 0.24 * S * k
    half_h = 0.34 * S * k
    ang = math.radians(angle)
    axis = (math.sin(-ang), -math.cos(-ang))     # leaf long axis (y grows down)

    leaf = leaf_mask(S, cx, cy, half_w, half_h, angle)
    mark.paste(Image.new("RGBA", (S, S), MATCHA + (255,)), (0, 0), leaf)

    # vein, tucked inside the leaf so the rounded ends never poke through the edge
    tip = (cx + 0.255 * S * k * axis[0], cy + 0.255 * S * k * axis[1])
    base = (cx - 0.235 * S * k * axis[0], cy - 0.235 * S * k * axis[1])
    vein = capsule_mask(S, base, tip, 0.021 * S * k)
    mark.paste(Image.new("RGBA", (S, S), MATCHA_LT + (255,)), (0, 0), vein)

    dot_c = (cx - 0.36 * S * k * axis[0], cy - 0.36 * S * k * axis[1])
    dot = mask_circle(S, dot_c[0], dot_c[1], 0.062 * S * k)
    mark.paste(Image.new("RGBA", (S, S), BLUSH + (255,)), (0, 0), dot)

    # optical centring: the blush dot drags the mark down-left, so align the
    # mark's own bounding box with the middle of the card
    bbox = mark.split()[3].getbbox()
    assert bbox is not None, "nothing drawn"
    centered = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    centered.alpha_composite(mark, (int(round((S - bbox[0] - bbox[2]) / 2)),
                                    int(round((S - bbox[1] - bbox[3]) / 2))))

    # the mark must sit well inside the card, never touching the rounded edge
    final = centered.split()[3].getbbox()
    margin = 0.16 * S
    assert final[0] >= margin and final[1] >= margin, f"mark too close to card edge: {final}"
    assert final[2] <= S - margin and final[3] <= S - margin, f"mark too close to card edge: {final}"

    card.alpha_composite(centered)
    return card


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    raw = build()
    icon = raw.resize((SIZE, SIZE), Image.LANCZOS)
    icon.save(DEST / "logo128.png")
    print(f"wrote logo/logo128.png ({SIZE}x{SIZE})")

    tmp = Path(tempfile.gettempdir()) / "blush-matcha-logo-preview.png"
    raw.resize((512, 512), Image.LANCZOS).save(tmp)
    print(f"preview -> {tmp}")


if __name__ == "__main__":
    main()
