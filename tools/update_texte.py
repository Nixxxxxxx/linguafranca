"""Rebuilds the "Texte" section of index.html from Franca's torial portfolio.

- Fetches every page of https://www.torial.com/franca.dr-parianen
- Saves each card image locally as images/texte/<id>.jpg (the site never hotlinks, for GDPR reasons)
- Replaces everything between <!-- TEXTE:START --> and <!-- TEXTE:END --> in index.html:
  a rotating lead (LEAD + FEATURED), then the other texts as rows, the rest behind "Alle … Texte anzeigen"

Usage (from the project root, needs Pillow):  python -I tools/update_texte.py
Texts that are NOT on torial go in EXTRA below (shown as cards after the torial texts).
"""
import html
import io
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PROFILE = "https://www.torial.com/franca.dr-parianen"
UA = {"User-Agent": "Mozilla/5.0 (site build script)"}
VISIBLE = 8  # rows shown below the lead before the "Alle Texte" toggle

# Rotating lead ("Kurzgefasst"): these texts first (newest taz texts, not on torial yet; images stored locally),
# then the torial texts whose titles start with FEATURED. The lead switches every 7s (js/site.js).
LEAD = [
    {"id": "taz-6133816", "url": "https://taz.de/KI-und-Automatisierung-machen-uns-duemmer-ist-das-wirklich-so-schlimm/!6133816/",
     "outlet": "taz", "kicker": "Cognitive Offloading", "date": "Dez 2025",
     "title": "KI und Automatisierung machen uns denkfauler, ist das wirklich so schlimm?",
     "desc": "Wir nutzen Navis und fragen ChatGPT nach Rezepten. Das kann zu weniger kognitiver Leistung führen. "
             "Doch wie können wir die Helfer produktiv einsetzen?"},
    {"id": "taz-6214458", "url": "https://taz.de/Bindungsverhalten/!6214458/", "outlet": "taz",
     "kicker": "Bindungsverhalten", "date": "Okt 2026", "title": "Knutschen ist Trumpf",
     "desc": "Viele Säugetiere verlassen sich in Sachen Bindung nicht auf penetrativen Sex. Küssen ist nicht nur schön, "
             "sondern auch evolutionär von Vorteil."},
    {"id": "taz-6165835", "url": "https://taz.de/Kuerzere-Geburten/!6165835/", "outlet": "taz",
     "kicker": "Kürzere Geburten", "date": "Apr 2026", "title": "Alles eine Frage des Timings!",
     "desc": "Die innere Uhr lenkt viele Prozesse in unserem Körper. Eine neue Studie zeigt nun: "
             "Sie scheint auch die Geburt zu beeinflussen."},
]
FEATURED = ["Kognitionsforschung: Warum Denken", "Biases: In der Denkfalle"]

OUTLETS = {
    "taz.de": "taz",
    "www.berliner-zeitung.de": "Berliner Zeitung",
    "www.deutschlandfunkkultur.de": "Deutschlandfunk Kultur",
}

# Older texts that are NOT in the torial portfolio; added as cards after the torial texts.
# (id, outlet, title, url, preview image url or None -> placeholder card)
EXTRA = [
    ("extra-spektrum", "Spektrum Gehirn & Geist", "Gruppendenken: Die Gräben in unseren Köpfen",
     "https://www.spektrum.de/magazin/gruppendenken-die-graeben-in-unseren-koepfen/1440299", None),
    ("extra-barbara", "Barbara", "Was die Sexhormone weckt: Unsere Lust, euer Problem",
     "https://www.brigitte.de/barbara/untenrum/was-die-sexhormone-weckt--unsere-lust--euer-problem--11796496.html",
     "https://image.brigitte.de/11796498/t/za/v3/w1440/r1.7778/-/sexhormome-wecken.jpg"),
    ("extra-steady-patent", "Verstehe sich, wer kann", "Die Entdeckung des Menschen: Wie viel Patent braucht die Wissenschaft?",
     "https://steadyhq.com/de/verstehe-sich-wer-kann/posts/f30efc8d-a978-48f4-9668-15784e933506",
     "https://assets-proxy.steadyhq.com/https%3A%2F%2Fsteady.imgix.net%2Fproduction%2Fpost%2Ff30efc8d-a978-48f4-9668-15784e933506%2Fuploads%2Fimages%2Fb3qv5extqd%2FPhotograph_of_F.G._Banting_and_C.H._Best_with_a_dog_on_the_roof_of_the_Medical_Building_%2812309019434%29.jpg?auto=format&h=864&w=1536&fit=crop&fm=jpg&crop=faces&s=ea428c4462d1cbf41d9e37035b6efd32"),
    ("extra-steady-darf", "Verstehe sich, wer kann", "In den Köpfen der Leute: Was man noch darf",
     "https://steadyhq.com/de/verstehe-sich-wer-kann/posts/c3dd5fc9-456f-412f-8131-a53ad6797000",
     "https://assets.steadyhq.com/production/post/c3dd5fc9-456f-412f-8131-a53ad6797000/teaser_image/1648756086?auto=format&h=864&w=1536&fit=crop&fm=jpg&crop=faces"),
]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def clean_url(url):
    url = html.unescape(url)
    # taz search links carry "&s=franca+parianen..." before the trailing slash; drop it.
    return re.sub(r"(taz\.de/.*?!\d+)&[^/]*/?$", r"\1/", url)


def clean_title(t):
    t = re.sub(r"\s+", " ", html.unescape(t)).strip()
    return re.sub(r"^Seite \d+:\s*", "", t)


def fetch_items():
    items, seen, page = [], set(), 1
    while True:
        s = get(f"{PROFILE}?page={page}").decode("utf-8")
        found = 0
        for m in re.finditer(r'<li id="contents-(\d+)".*?</article>', s, re.S):
            cid, block = m.group(1), m.group(0)
            if cid in seen:
                continue
            seen.add(cid)
            found += 1
            href = re.search(r'<a href="([^"]+)"', block).group(1)
            img = re.search(r'<img src="([^"]+)"', block)
            title = re.search(r"<h2.*?<a[^>]*>(.*?)</a>", block, re.S).group(1)
            outlet = re.search(r'text-darkestgray">(.*?)</div>', block, re.S)
            outlet = outlet.group(1).strip() if outlet else ""
            items.append({
                "id": cid,
                "url": clean_url(href),
                "img": html.unescape(img.group(1)) if img else None,
                "title": clean_title(title),
                "outlet": OUTLETS.get(outlet, outlet.removeprefix("www.")),
            })
        if not found:
            break
        page += 1
    return items


def sort_key(it):
    # Newest first: taz article numbers rise over time; other outlets go after the taz texts.
    m = re.search(r"taz\.de/.*?!(\d+)", it["url"])
    return (0, -int(m.group(1))) if m else (1, 0)


def save_image(it):
    out = ROOT / "images" / "texte" / f"{it['id']}.jpg"
    if not out.exists() and it["img"]:
        im = Image.open(io.BytesIO(get(it["img"]))).convert("RGB")
        if im.width > 636:  # large source images: crop to card ratio, store at 2x card size
            w, h = 636, 384
            r = max(w / im.width, h / im.height)
            im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
            l, t = (im.width - w) // 2, (im.height - h) // 2
            im = im.crop((l, t, l + w, t + h))
        out.parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=85, optimize=True, progressive=True)
    return f"./images/texte/{it['id']}.jpg" if out.exists() else None


def slide(it, n, total, ind):
    e = html.escape
    kick = f'<span class="tl-kicker">{e(it["kicker"])}</span>' if it.get("kicker") else ""
    desc = f'<span class="tl-desc">{e(it["desc"])}</span>' if it.get("desc") else ""
    date = f' · {e(it["date"])}' if it.get("date") else ""
    return (f'{ind}<li class="tl-slide{" is-on" if n == 0 else ""}" id="tl-s{n}" role="tabpanel" aria-roledescription="Folie" '
            f'aria-label="{n + 1} von {total}"><a href="{e(it["url"])}" target="_blank" rel="noopener">\n'
            f'{ind}    <span class="tl-pic"><img src="{e(it["src"])}" width="1080" height="720" alt="" '
            f'loading="{"eager" if n == 0 else "lazy"}"></span>\n'
            f'{ind}    <span class="tl-text"><span class="tl-outlet">{e(it["outlet"])}{date}</span>{kick}'
            f'<span class="tl-head">{e(it["title"])}</span>{desc}<span class="tl-read">Artikel lesen →</span></span>\n'
            f'{ind}</a></li>')


def row(it, src, n, ind):
    e = html.escape
    pic = (f'<span class="t-pic"><img src="{e(src)}" width="318" height="192" alt="" loading="lazy"></span>' if src
           else f'<span class="t-pic t-ph" aria-hidden="true">{e(it["outlet"])}</span>')
    return (f'{ind}<li class="t-item"><a href="{e(it["url"])}" target="_blank" rel="noopener">'
            f'<span class="t-num" aria-hidden="true">{n:02d}</span><span class="t-text"><span class="t-outlet">{e(it["outlet"])}</span>'
            f'<span class="t-head">{e(it["title"])}</span><span class="t-read">Artikel lesen →</span></span>{pic}</a></li>')


def short(title):
    """Tab label: drop a leading "Topic: " prefix."""
    return re.sub(r"^[^:]{0,40}:\s*", "", title)


def build(items):
    e, ind = html.escape, " " * 16
    srcs = {it["id"]: save_image(it) for it in items}
    lead = [dict(it, src=f"./images/texte/{it['id']}.jpg") for it in LEAD]
    for k in FEATURED:
        m = [it for it in items if it["title"].startswith(k) and srcs[it["id"]]]
        if m:  # skipped silently if torial renamed it
            lead.append(dict(m[0], src=srcs[m[0]["id"]]))
    lead_ids = {it["id"] for it in lead}
    rest = [it for it in items if it["id"] not in lead_ids]
    total = len(LEAD) + len(items)
    tabs = "".join(
        f'<button type="button" class="tl-tab{" is-on" if n == 0 else ""}" role="tab" aria-controls="tl-s{n}" '
        f'aria-selected="{"true" if n == 0 else "false"}"><span class="tl-n">{n + 1:02d}</span>'
        f'<span class="tl-t">{e(short(it["title"]))}</span><span class="tl-bar"></span></button>'
        for n, it in enumerate(lead))
    out = [f'{ind}<div class="tl" data-ms="7000" aria-roledescription="Karussell" aria-label="Ausgewählte Texte">',
           f'{ind}    <ul class="tl-slides">', *[slide(it, n, len(lead), ind + "        ") for n, it in enumerate(lead)],
           f'{ind}    </ul>',
           f'{ind}    <div class="tl-tabs" role="tablist" aria-label="Text wählen">{tabs}</div>',
           f'{ind}    <button type="button" class="tl-pause" aria-label="Automatisches Wechseln anhalten">❚❚</button>',
           f'{ind}</div>',
           f'{ind}<ul class="t-list">', *[row(it, srcs[it["id"]], n + 1, ind + "    ") for n, it in enumerate(rest[:VISIBLE])],
           f'{ind}</ul>']
    if rest[VISIBLE:]:
        out += [f'{ind}<details class="more-texts">',
                f'{ind}    <summary><span class="closed">Alle {total} Texte anzeigen</span><span class="open">Weniger anzeigen</span></summary>',
                f'{ind}    <ul class="t-list">',
                *[row(it, srcs[it["id"]], n + 1 + VISIBLE, ind + "        ") for n, it in enumerate(rest[VISIBLE:])],
                f'{ind}    </ul>', f'{ind}</details>']
    out.append(f'{ind}<p class="source">Alle Texte auch im '
               f'<a href="{PROFILE}" target="_blank" rel="noopener">Portfolio auf torial</a>.</p>')
    return "\n".join(out)


def main():
    items = sorted(fetch_items(), key=sort_key)
    if not items:
        sys.exit("No items found on torial; page layout may have changed. index.html left unchanged.")
    items += [{"id": i, "outlet": o, "title": t, "url": u, "img": img} for i, o, t, u, img in EXTRA]
    page = ROOT / "index.html"
    s = page.read_text(encoding="utf-8")
    start, end = "<!-- TEXTE:START -->", "<!-- TEXTE:END -->"
    if start not in s or end not in s:
        sys.exit("Markers not found in index.html")
    a, b = s.index(start) + len(start), s.index(end)
    s = s[:a] + "\n" + build(items) + "\n                " + s[b:]
    page.write_text(s, encoding="utf-8")
    print(f"Texte section rebuilt: {len(LEAD) + len(items)} texts ({len(LEAD)} from LEAD, {len(EXTRA)} from EXTRA).")
    import runpy  # keep the English page (en/index.html) in sync
    runpy.run_path(str(ROOT / "tools" / "build_en.py"), run_name="__main__")


if __name__ == "__main__":
    main()
