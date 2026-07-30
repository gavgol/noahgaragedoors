"""Generate right-sized WebP versions of the customer review photos used in the
index.html reviews carousel (rendered at ~206x190 CSS px, so a 460px-wide
WebP covers 2x retina). Originals are left untouched; only new .webp files
are written alongside them.
"""
from pathlib import Path
from PIL import Image

REVIEWS_DIR = Path(__file__).resolve().parent.parent / "reviews" / "img"
TARGET_WIDTH = 460
QUALITY = 78

NAMES = [
    "ArnieAmbito", "EBONYTYREE", "GMRASER", "Gabriel", "IzzieCorrales",
    "JamesThompson", "Joe", "JoshuaMcBride", "LibroDiZinno", "MaureenMoore",
    "MitchGurule", "PatriciaWBlanco", "alejandrareule", "emadzro",
]

for name in NAMES:
    src = REVIEWS_DIR / f"{name}.jpg"
    dst = REVIEWS_DIR / f"{name}.webp"
    if not src.exists():
        print(f"SKIP missing: {src}")
        continue
    with Image.open(src) as im:
        im = im.convert("RGB")
        w, h = im.size
        if w > TARGET_WIDTH:
            new_h = round(h * (TARGET_WIDTH / w))
            im = im.resize((TARGET_WIDTH, new_h), Image.LANCZOS)
        im.save(dst, "WEBP", quality=QUALITY, method=6)
    before = src.stat().st_size
    after = dst.stat().st_size
    print(f"{name}: {before/1024:.0f}KB -> {after/1024:.0f}KB")
