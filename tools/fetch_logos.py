"""Downloads the logos used in the "Vorträge" and "Fernsehen & Presse" lists into images/logos/.

The site never hotlinks (GDPR), so every logo is stored locally. SVGs are kept as-is,
raster images are converted to PNG. Existing files are skipped; delete one to re-fetch it.
Usage (from the project root):  python -I tools/fetch_logos.py
"""
import io
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "logos"
UA = {"User-Agent": "linguafranca-site-build/1.0 (static site logo fetch)"}
COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/{}?width=480"  # returns a PNG render

LOGOS = {
    # Vorträge
    "dbvc-coaching27": "https://kongress.dbvc.de/wp-content/uploads/2026/09/logo_dbvc_komplett_farbe_4x_RGB.png",
    "ernst-deutsch-theater": "https://www.ernst-deutsch-theater.de/_assets/52b3d211a4f7093a176c0c5d2004bac7/Images/edt-wortmarke.svg",
    # fuko.nrw.de (Deutscher Fußverkehrskongress) only has the NRW state coat of arms as a logo, which may not be
    # used freely, so that entry is a text badge.
    "sosafe-signal": COMMONS.format("SoSafe_Logo_1.svg"),
    "ihk-muenchen": COMMONS.format("Logo_IHK_M%C3%BCnchen_und_Oberbayern.svg"),
    "hercareer": "https://www.her-career.com/wp-content/uploads/2022/05/logo-herCAREER-b310.png.webp",
    "youmecon": "https://youmecon.de/media/logos/YouMeCon-Logo.svg",
    "visitberlin": ("inline-svg", "https://www.visitberlin.de/", r'<svg[^>]*class="site-logo".*?</svg>'),
    "kulturelle-landpartie": "https://www.kulturelle-landpartie.de/img/web/logo_300.png",
    "zeit-stiftung": COMMONS.format("Logo_ZEIT-Stiftung_Ebelin_und_Gerd_Bucerius.svg"),
    # b2b-vertriebskongress.at did not respond (2026-11-10): shown as a text badge instead.
    "learntec": COMMONS.format("LEARNTEC_Logo.svg"),
    "ideenexpo": "https://www.ideenexpo.de/themes/custom/ideenexpo/images/ideenexpo_logo_RGB.svg",
    "polytechnische": "https://www.polytechnische.de/files/Mediathek/SPTG/Logos-Illustrationen-Coverbilder-Grafiken/Logos/Polytechnische/Logo-PTG-2025.svg",
    "scienceslam": "https://www.scienceslam.de/wp-content/uploads/Science-Slam_Logo_big_whitecircleback.svg",
    # frankfurter-zukunftskongress: made from images/frankfurt.jpg (event graphic), see below.
    # Fernsehen & Presse
    "zdf": COMMONS.format("ZDF_logo.svg"),
    "ndr": COMMONS.format("NDR_Logo.svg"),
    "3sat": COMMONS.format("3sat_2019.svg"),
    "sz-magazin": COMMONS.format("SZ-Magazin_logo.svg"),
    "stern": COMMONS.format("Stern_Logo_2020.svg"),
    "welt": "https://www.welt.de/assets/images/global/welt_brand-dd869f0cab.png",
    # nachtkritik's logo is white (made for its dark page): after fetching, its .cls-1 fill was changed to #1a1a1a by hand.
    "nachtkritik": "https://nachtkritik.de/images/logo2019.svg",
}


def main(only=None):
    OUT.mkdir(parents=True, exist_ok=True)
    for key, url in LOGOS.items():
        if only and key not in only:
            continue
        if list(OUT.glob(key + ".*")):
            print(f"skip  {key} (exists)")
            continue
        try:
            if isinstance(url, tuple):  # ("inline-svg", page url, regex): logo is drawn inline in the page
                import re
                _, page, pattern = url
                with urllib.request.urlopen(urllib.request.Request(page, headers=UA), timeout=30) as r:
                    svg = re.search(pattern, r.read().decode("utf-8"), re.S).group(0)
                if "xmlns=" not in svg:
                    svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
                (OUT / f"{key}.svg").write_text(svg, encoding="utf-8")
                print(f"ok    {key}.svg (inline)")
                continue
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                data = r.read()
            if data.lstrip()[:5] in (b"<?xml", b"<svg ") or b"<svg" in data[:500]:
                (OUT / f"{key}.svg").write_bytes(data)
                print(f"ok    {key}.svg")
            else:
                im = Image.open(io.BytesIO(data))
                im = im.convert("RGBA")
                im.thumbnail((480, 240))
                im.save(OUT / f"{key}.png", optimize=True)
                print(f"ok    {key}.png {im.size}")
        except Exception as e:  # keep going; missing logos fall back to a text badge on the page
            print(f"FAIL  {key}: {e}")


def frankfurt():
    """Event graphic from the old site, minus the progress bar captured at its bottom."""
    out = OUT / "frankfurter-zukunftskongress.jpg"
    if not out.exists():
        im = Image.open(ROOT / "images" / "frankfurt.jpg").convert("RGB")
        im.crop((0, 0, im.width, 176)).save(out, quality=88)
        print("ok    frankfurter-zukunftskongress.jpg")


def aurel():
    """Aurel Original (ZDF): the show's key art from its IMDb page (tt16439326), cropped to the title lettering."""
    out = OUT / "aurel-original.jpg"
    if not out.exists():
        url = ("https://m.media-amazon.com/images/M/"
               "MV5BYjBmMTYyNjgtMTVkNy00ZmM1LWFjYTgtYjFlZTkwZjM5ODRmXkEyXkFqcGc@._V1_.jpg")
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
            im = Image.open(io.BytesIO(r.read())).convert("RGB")
        im = im.crop((330, 300, 950, 560))  # 1280x720 source: "AUREL ORIGINAL" over the host
        im.thumbnail((480, 240))
        im.save(out, quality=86)
        print("ok    aurel-original.jpg")


if __name__ == "__main__":
    frankfurt()
    aurel()
    main(set(sys.argv[1:]) or None)
