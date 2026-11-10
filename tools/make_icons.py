"""Builds the site icons from the chosen design (2026-11-10: row 4, column 6 of the generated sheet
"Neuroscience Icon Grid Collection.png": a coral neuron on an off-white rounded tile).

The neuron is lifted from the sheet as an alpha mask and re-drawn in exact brand colours on a clean tile, so
the icons are crisp and the sheet's off-white/sand background doesn't leak into them.
Source copy kept in images/icon-source.png. Usage (project root):  python -I tools/make_icons.py
"""
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "images" / "icon-source.png"     # the 179x179 tile cut from the sheet
CORAL, TILE = (255, 90, 54), (247, 243, 236)  # site coral, off-white


def neuron_mask(tile):
    """Alpha = how far each pixel is from the tile background toward coral."""
    bg = max(tile.quantize(8).convert("RGB").getcolors(), key=lambda c: c[0])[1]  # dominant colour = tile background
    ref = (238, 104, 64)  # coral as rendered in the sheet
    span = sum((a - b) ** 2 for a, b in zip(bg, ref)) ** .5
    m = Image.new("L", tile.size)
    px, mp = tile.load(), m.load()
    for y in range(tile.height):
        for x in range(tile.width):
            d = sum((a - b) ** 2 for a, b in zip(px[x, y], bg)) ** .5
            mp[x, y] = max(0, min(255, round((d / span - .12) / .7 * 255)))
    return m


def render(size, mask, rounded=True, pad=0.0):
    big = 1024
    out = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    tile = Image.new("L", (big, big), 0)
    ImageDraw.Draw(tile).rounded_rectangle((0, 0, big - 1, big - 1), radius=int(big * .2) if rounded else 0, fill=255)
    out.paste(TILE + (255,), (0, 0), tile)
    inner = int(big * (1 - 2 * pad))
    m = mask.resize((inner, inner), Image.LANCZOS)
    off = (big - inner) // 2
    layer = Image.new("RGBA", (inner, inner), CORAL + (255,))
    out.paste(layer, (off, off), m)
    return out.resize((size, size), Image.LANCZOS)


def main():
    tile = Image.open(SRC).convert("RGB")
    # drop the tile's own rounded corners/margin: use the central square that holds the neuron
    c = int(tile.width * .08)
    mask = neuron_mask(tile.crop((c, c, tile.width - c, tile.height - c)))
    img = ROOT / "images"
    for s in (16, 32, 48):
        # small sizes: neuron fills more of the tile so it stays readable in a browser tab
        render(s, mask, pad=-0.06).save(img / f"favicon-{s}.png", optimize=True)
    render(512, mask).save(img / "icon-512.png", optimize=True)
    render(180, mask, rounded=False).convert("RGB").save(img / "apple-touch-icon.png", optimize=True)
    render(256, mask, pad=-0.06).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("icons written")


if __name__ == "__main__":
    main()
