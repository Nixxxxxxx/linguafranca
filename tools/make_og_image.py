"""Builds images/og-image.jpg (1200x630 social share preview). Re-run after changing the photo or text.
Usage: python tools/make_og_image.py   (from the project root; needs Pillow, Windows fonts)"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG, ACCENT, INK, SOFT, WARM = (250, 248, 244), (15, 76, 69), (27, 36, 34), (74, 85, 82), (200, 86, 46)
F = "C:/Windows/Fonts/"

img = Image.new("RGB", (W, H), BG)
photo = Image.open("images/franca.jpg").convert("RGB")
pw, ph = photo.size
photo = photo.crop((0, 0, pw, ph - 30))                 # drop the baked-in credit line
side = min(photo.size)
photo = photo.crop(((photo.width - side) // 2 + 40, 0, (photo.width - side) // 2 + 40 + side - 40, side))
photo = photo.resize((int(H * photo.width / photo.height), H), Image.LANCZOS)
img.paste(photo, (W - photo.width, 0))

d = ImageDraw.Draw(img)
d.rectangle((0, 0, 14, H), fill=ACCENT)
eyebrow = ImageFont.truetype(F + "segoeuib.ttf", 19)
name = ImageFont.truetype(F + "georgiab.ttf", 62)
body = ImageFont.truetype(F + "segoeui.ttf", 28)
x = 72
d.text((x, 150), "NEUROWISSENSCHAFTLERIN · AUTORIN · SPEAKERIN", font=eyebrow, fill=ACCENT)
d.text((x, 200), "Dr. Franca", font=name, fill=INK)
d.text((x, 272), "Parianen", font=name, fill=INK)
d.rectangle((x, 372, x + 70, 376), fill=WARM)
for i, line in enumerate(["Hirn, Humor und Quellenangaben.", "Bücher · Keynotes · Science Slam"]):
    d.text((x, 404 + i * 42), line, font=body, fill=SOFT)
d.text((x, 540), "parianen.com", font=eyebrow, fill=ACCENT)
img.save("images/og-image.jpg", quality=86, optimize=True, progressive=True)
print("wrote images/og-image.jpg")
