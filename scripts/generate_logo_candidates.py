"""Blush Matcha theme - code-drawn logo candidates.

Each candidate is drawn with Pillow at 4x supersampling, downsampled to a
512px preview, and finally assembled into a labeled contact sheet that also
shows a 64px render so small-size legibility can be judged.

Output: store-assets/icon-candidates/
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

SS = 4                     # supersample factor
OUT = 512                  # preview size
SMALL = 64                 # small-size legibility check
ROOT = Path(__file__).resolve().parent.parent
DEST = ROOT / "store-assets" / "icon-candidates"

# palette taken from manifest.json
TILE = (253, 252, 250)
BLUSH = (251, 188, 207)
BLUSH_DEEP = (243, 150, 180)
BLUSH_PALE = (253, 227, 234)
MATCHA_LT = (230, 247, 212)
MATCHA = (170, 199, 146)
MATCHA_DP = (108, 128, 96)
CREAM = (245, 240, 233)
WHITE = (255, 255, 255)


def blend(a, b, t=0.5):
    return tuple(round(a[i] * (1 - t) + b[i] * t) for i in range(3))


# ---------------------------------------------------------------- primitives

def mask_circle(S, cx, cy, r):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=255)
    return m


def mask_rounded(S, box, radius):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).rounded_rectangle(box, radius=radius, fill=255)
    return m


def mask_poly(S, pts):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).polygon(pts, fill=255)
    return m


def paint(img, color, mask):
    layer = Image.new("RGB", img.size, color)
    img.paste(layer, (0, 0), mask)


def leaf_mask(S, cx, cy, half_w, half_h, angle=0.0):
    """Pointed-oval leaf as the lens of two circles, optionally rotated."""
    d = (half_h ** 2 - half_w ** 2) / (2 * half_w)
    r = half_w + d
    a = mask_circle(S, cx - d, cy, r)
    b = mask_circle(S, cx + d, cy, r)
    m = ImageChops.darker(a, b)
    if angle:
        m = m.rotate(angle, resample=Image.BICUBIC, center=(cx, cy))
    return m


def new_tile(S, bg=TILE):
    img = Image.new("RGB", (S, S), bg)
    return img, ImageDraw.Draw(img)


# ---------------------------------------------------------------- candidates

def c01_duo_circles(S):
    """Two overlapping circles: blush | matcha."""
    img, d = new_tile(S)
    r = 0.29 * S
    cy = 0.5 * S
    left = (0.385 * S, cy)
    right = (0.615 * S, cy)
    paint(img, BLUSH, mask_circle(S, *left, r))
    paint(img, MATCHA, mask_circle(S, *right, r))
    overlap = ImageChops.darker(mask_circle(S, *left, r), mask_circle(S, *right, r))
    paint(img, blend(BLUSH, MATCHA), overlap)
    return img


def c02_split_vertical(S):
    """Rounded square split left/right."""
    img, d = new_tile(S)
    box = (0.19 * S, 0.19 * S, 0.81 * S, 0.81 * S)
    body = mask_rounded(S, box, 0.16 * S)
    paint(img, BLUSH, body)
    half = mask_poly(S, [(0.5 * S, 0), (S, 0), (S, S), (0.5 * S, S)])
    paint(img, MATCHA_LT, ImageChops.darker(body, half))
    d.line([(0.5 * S, 0.22 * S), (0.5 * S, 0.78 * S)], fill=TILE, width=int(0.018 * S))
    return img


def c03_split_diagonal(S):
    """Rounded square split on the diagonal."""
    img, d = new_tile(S)
    box = (0.19 * S, 0.19 * S, 0.81 * S, 0.81 * S)
    body = mask_rounded(S, box, 0.16 * S)
    paint(img, MATCHA_LT, body)
    lower = mask_poly(S, [(0, S), (S, S), (S, 0)])
    paint(img, BLUSH, ImageChops.darker(body, lower))
    return img


def c04_leaf(S):
    """Single matcha leaf with a blush dot at the base."""
    import math
    img, d = new_tile(S)
    cx = cy = 0.5 * S
    ang = math.radians(-28)
    axis = (math.sin(-ang), -math.cos(-ang))       # leaf long axis (y grows down)
    m = leaf_mask(S, cx, cy, 0.24 * S, 0.34 * S, angle=-28)
    paint(img, MATCHA, m)
    tip = (cx + 0.30 * S * axis[0], cy + 0.30 * S * axis[1])
    base = (cx - 0.27 * S * axis[0], cy - 0.27 * S * axis[1])
    d.line([base, tip], fill=MATCHA_LT, width=int(0.022 * S))
    dot = (cx - 0.36 * S * axis[0], cy - 0.36 * S * axis[1])
    paint(img, BLUSH, mask_circle(S, dot[0], dot[1], 0.062 * S))
    return img


def c05_blossom(S):
    """Five alternating petals around a matcha core."""
    img, d = new_tile(S)
    import math
    cx = cy = 0.5 * S
    pr = 0.16 * S
    orbit = 0.185 * S
    for i in range(5):
        a = -math.pi / 2 + i * 2 * math.pi / 5
        color = BLUSH if i % 2 == 0 else MATCHA_LT
        paint(img, color, mask_circle(S, cx + orbit * math.cos(a),
                                      cy + orbit * math.sin(a), pr))
    paint(img, MATCHA, mask_circle(S, cx, cy, 0.10 * S))
    return img


def c06_rings(S):
    """Blush ring around a matcha dot."""
    img, d = new_tile(S)
    cx = cy = 0.5 * S
    w = int(0.075 * S)
    d.ellipse([cx - 0.295 * S, cy - 0.295 * S, cx + 0.295 * S, cy + 0.295 * S],
              outline=BLUSH, width=w)
    paint(img, MATCHA, mask_circle(S, cx, cy, 0.135 * S))
    return img


def c07_yin_soft(S):
    """Soft two-tone yin-yang."""
    img, d = new_tile(S)
    cx = cy = 0.5 * S
    r = 0.32 * S
    paint(img, BLUSH, mask_circle(S, cx, cy, r))
    right = mask_poly(S, [(cx, 0), (S, 0), (S, S), (cx, S)])
    paint(img, MATCHA_LT, ImageChops.darker(mask_circle(S, cx, cy, r), right))
    paint(img, MATCHA_LT, mask_circle(S, cx, cy - r / 2, r / 2))
    paint(img, BLUSH, mask_circle(S, cx, cy + r / 2, r / 2))
    paint(img, BLUSH, mask_circle(S, cx, cy - r / 2, r / 6))
    paint(img, MATCHA_LT, mask_circle(S, cx, cy + r / 2, r / 6))
    return img


def c08_clover(S):
    """Four circles in a clover, two blush two matcha."""
    img, d = new_tile(S)
    cx = cy = 0.5 * S
    r = 0.185 * S
    off = 0.155 * S
    spots = [(-off, -off, BLUSH), (off, -off, MATCHA_LT),
             (-off, off, MATCHA_LT), (off, off, BLUSH)]
    for dx, dy, color in spots:
        paint(img, color, mask_circle(S, cx + dx, cy + dy, r))
    paint(img, WHITE, mask_circle(S, cx, cy, 0.072 * S))
    return img


def c09_arc_pair(S):
    """Ring split into a blush arc and a matcha arc."""
    img, d = new_tile(S)
    cx = cy = 0.5 * S
    r = 0.30 * S
    w = int(0.085 * S)
    box = [cx - r, cy - r, cx + r, cy + r]
    d.arc(box, start=-70, end=110, fill=BLUSH, width=w)
    d.arc(box, start=125, end=290, fill=MATCHA, width=w)
    return img


CANDIDATES = [
    ("01-duo-circles", "duo circles", c01_duo_circles),
    ("02-split-vertical", "split vertical", c02_split_vertical),
    ("03-split-diagonal", "split diagonal", c03_split_diagonal),
    ("04-leaf", "leaf", c04_leaf),
    ("05-blossom", "blossom", c05_blossom),
    ("06-rings", "rings", c06_rings),
    ("07-yin-soft", "yin soft", c07_yin_soft),
    ("08-clover", "clover", c08_clover),
    ("09-arc-pair", "arc pair", c09_arc_pair),
]


# ---------------------------------------------------------------- rendering

def render(fn, size):
    raw = fn(size * SS)
    return raw.resize((size, size), Image.LANCZOS)


def load_font(size):
    for name in ("segoeui.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    previews = []
    for slug, label, fn in CANDIDATES:
        img = render(fn, OUT)
        img.save(DEST / f"{slug}.png")
        previews.append((slug, label, img, render(fn, SMALL)))
        print(f"wrote {slug}.png")

    # contact sheet: 3 columns, big render + 64px render, labeled
    cols = 3
    cell_w, cell_h = 300, 320
    rows = (len(previews) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (255, 255, 255))
    d = ImageDraw.Draw(sheet)
    font = load_font(18)
    for i, (slug, label, big, small) in enumerate(previews):
        x = (i % cols) * cell_w
        y = (i // cols) * cell_h
        thumb = big.resize((220, 220), Image.LANCZOS)
        sheet.paste(thumb, (x + 20, y + 16))
        sheet.paste(small, (x + 248, y + 216))
        d.text((x + 20, y + 250), f"{i + 1}. {label}", fill=(40, 40, 40), font=font)
        d.text((x + 20, y + 276), "512px / 64px", fill=(150, 150, 150),
               font=load_font(14))
    sheet.save(DEST / "contact-sheet.png")
    print(f"wrote contact-sheet.png ({cols * cell_w}x{rows * cell_h})")


if __name__ == "__main__":
    main()
