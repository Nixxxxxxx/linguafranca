"""Copies the generated "Vorträge/Presse" and "Texte" blocks from index.html into en/index.html, in English.

index.html stays the single source for these lists (tools/build_vortraege.py and tools/update_texte.py write it);
this script translates the labels, dates and descriptions and fixes image paths for the /en/ folder.
Both builder scripts call it at the end, so normally you never run it by hand. To run it alone:
    python -I tools/build_en.py
If a list entry has a German description or lead text without an English version below, the script stops and
names it: add the translation to DESC_EN / LEAD_EN and run it again.
Everything outside the marker blocks in en/index.html is hand-written English: edit it directly.
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EN = ROOT / "en" / "index.html"

# Card descriptions (German -> English). Event and article titles are proper names and stay as they are.
DESC_EN = {
    "Keynote zum Kongressmotto „Dialog stärken, Demokratie begleiten“":
        "Keynote on the congress theme “Strengthening dialogue, supporting democracy”",
    "„Sicheres Verhalten nachhaltig verankern: Was wir aus der Neurowissenschaft lernen können“":
        "“Making secure behaviour stick: what we can learn from neuroscience”",
    "Begrüßung mit einem Science Slam beim Festival „wider die Einsamkeit“":
        "Opening science slam at the festival “against loneliness”",
    "„Warum Menschen zusammenhalten müssen, aber nicht wollen (auch im Straßenverkehr)“":
        "“Why people have to stick together but don’t want to (in traffic, too)”",
    "Podium nach der Premiere: warum Empathie ein Gesicht und einen Namen braucht":
        "Panel after the premiere: why empathy needs a face and a name",
    "Humorvoller Pitch zum Menschen als sozialem Wesen": "A humorous pitch on humans as social beings",
    "Keynote bei der Verleihung des Deutschen Innovationspreises": "Keynote at the German Innovation Award ceremony",
    "Symposium des HarbourClub, des Netzwerks der Kommunikationschefs, zu Gast bei Roche":
        "Symposium of the HarbourClub, the network of chief communications officers, hosted by Roche",
    "Impulsvortrag beim Unternehmerinnentag der IHK München":
        "Short talk at the Women Entrepreneurs’ Day of the Munich Chamber of Industry and Commerce",
    "Keynote gemeinsam mit Richard David Precht: Zusammenleben mit 8 Milliarden Gehirnen":
        "Keynote with Richard David Precht: living together with 8 billion brains",
    "„Was hält unsere Gesellschaft zusammen? Miteinander teilen“, mit Steffen Mau und Robert Habeck":
        "“What holds our society together? Sharing with each other”, with Steffen Mau and Robert Habeck",
    "Soziale Bedürfnisse motivieren uns zum Lernen": "Social needs motivate us to learn",
    "Science Slam über die Neurowissenschaft des Mitgefühls": "Science slam on the neuroscience of compassion",
    "Mit Stephanie Rohde: wie Worte Gefühle, Entscheidungen und sogar das Gehirn verändern":
        "With Stephanie Rohde: how words change feelings, decisions and even the brain",
    "Interview zu sozialer Kognition und Neid": "Interview on social cognition and envy",
    "Gast in den Sendungen vom 25.04.2017 und 03.10.2017": "Guest on the episodes of 25 April and 3 October 2017",
    "Interview über Hormone und Liebe": "Interview on hormones and love",
    "Interview": "Interview",
    "Interview: Auch Männer sind hormongesteuert": "Interview: men are driven by hormones, too",
    "Über Frauenfreundschaften und Kooperation": "On female friendship and cooperation",
    "Gast bei Gert Scobel": "Guest on Gert Scobel’s show",
    "Beitrag des HarbourClub": "Article by the HarbourClub",
}

# Rotating lead in "Texte": kicker and teaser (the articles themselves are German).
LEAD_EN = {
    "Cognitive Offloading": "Cognitive offloading",
    "Bindungsverhalten": "Bonding behaviour",
    "Kürzere Geburten": "Shorter births",
    "Wir nutzen Navis und fragen ChatGPT nach Rezepten. Das kann zu weniger kognitiver Leistung führen. "
    "Doch wie können wir die Helfer produktiv einsetzen?":
        "We use satnavs and ask ChatGPT for recipes. That can reduce cognitive performance. "
        "So how can we put these helpers to good use?",
    "Viele Säugetiere verlassen sich in Sachen Bindung nicht auf penetrativen Sex. Küssen ist nicht nur schön, "
    "sondern auch evolutionär von Vorteil.":
        "Many mammals don’t rely on penetrative sex for bonding. Kissing isn’t just nice – "
        "it’s an evolutionary advantage.",
    "Die innere Uhr lenkt viele Prozesse in unserem Körper. Eine neue Studie zeigt nun: "
    "Sie scheint auch die Geburt zu beeinflussen.":
        "Our internal clock steers many processes in the body. A new study suggests "
        "it may influence childbirth, too.",
}

CITIES = {"Köln": "Cologne", "Nürnberg": "Nuremberg", "München": "Munich", "Wien": "Vienna"}
MONTHS = {"Jan": "Jan", "Feb": "Feb", "Mär": "Mar", "Apr": "Apr", "Mai": "May", "Jun": "Jun", "Jul": "Jul",
          "Aug": "Aug", "Sep": "Sep", "Okt": "Oct", "Nov": "Nov", "Dez": "Dec"}
WORDS = {"Podium": "Panel", "Speakerin": "Speaker", "Eröffnungsimpuls": "Opening talk", "Impulsvortrag": "Short talk", "Science Slam": "Science slam",
         "Eröffnungskeynote": "Opening keynote", "Lesung": "Reading", "Vortrag": "Talk", "Bühne": "Stage",
         "Gast": "Guest", "Expertin": "Expert", "Redaktion": "Editorial team", "Kritik": "Review",
         "Radiointerview": "Radio interview", "Buchbesprechung": "Book review", "Bericht": "Report",
         "Preisverleihung": "Award ceremony"}

LABELS = [  # fixed strings in the generated markup
    ('<h3>Vorträge</h3>', '<h3>Talks</h3>'),
    ('<h3>Presse</h3>', '<h3>Press</h3>'),
    ('Weniger anzeigen', 'Show less'),
    ('Artikel lesen →', 'Read article →'),
    ('aria-roledescription="Karussell"', 'aria-roledescription="carousel"'),
    ('aria-label="Ausgewählte Texte"', 'aria-label="Selected texts"'),
    ('aria-roledescription="Folie"', 'aria-roledescription="slide"'),
    ('aria-label="Text wählen"', 'aria-label="Choose a text"'),
    ('aria-label="Automatisches Wechseln anhalten"', 'aria-label="Pause rotation"'),
    ('src="./images/', 'src="../images/'),
]


def meta_en(text):
    def part(p):
        m = re.fullmatch(r"(\d{1,2})\. (\w{3}) (\d{4})", p)
        if m:
            return f"{int(m.group(1))} {MONTHS.get(m.group(2), m.group(2))} {m.group(3)}"
        m = re.fullmatch(r"(\w{3}) (\d{4})", p)
        if m and m.group(1) in MONTHS:
            return f"{MONTHS[m.group(1)]} {m.group(2)}"
        return WORDS.get(p, p)
    return " · ".join(part(p) for p in text.split(" · "))


def translate(block, missing):
    e, u = html.escape, html.unescape

    def lookup(table, kind):
        def f(m):
            de = u(m.group(2))
            if de not in table:
                missing.append(f"{kind}: {de}")
                return m.group(0)
            return f'{m.group(1)}{e(table[de], quote=False)}</span>'
        return f

    block = re.sub(r'(<span class="desc">)(.*?)</span>', lookup(DESC_EN, "DESC_EN"), block)
    block = re.sub(r'(<span class="tl-(?:kicker|desc)">)(.*?)</span>', lookup(LEAD_EN, "LEAD_EN"), block)
    block = re.sub(r'(<span class="(?:meta|tl-outlet)">)(.*?)</span>',
                   lambda m: f'{m.group(1)}{e(meta_en(u(m.group(2))), quote=False)}</span>', block)
    block = re.sub(r'(class="title"[^>]*>[^<]*, )(' + "|".join(CITIES) + r')<',
                   lambda m: m.group(1) + CITIES[m.group(2)] + "<", block)
    block = re.sub(r'Alle (\d+) Texte anzeigen', r'Show all \1 texts', block)
    block = re.sub(r'Alle (\d+) anzeigen', r'Show all \1', block)
    block = re.sub(r'aria-label="(\d+) von (\d+)"', r'aria-label="\1 of \2"', block)
    block = block.replace('<p class="source">Alle Texte auch im <a', '<p class="source">All texts are also available in her <a')
    block = block.replace('>Portfolio auf torial</a>.</p>', '>torial portfolio</a> (in German).</p>')
    for de, en in LABELS:
        block = block.replace(de, en)
    return block


def main():
    de = (ROOT / "index.html").read_text(encoding="utf-8")
    en = EN.read_text(encoding="utf-8")
    missing = []
    for name in ("VORTRAEGE", "TEXTE"):
        start, end = f"<!-- {name}:START -->", f"<!-- {name}:END -->"
        for page, s in (("index.html", de), ("en/index.html", en)):
            if start not in s or end not in s:
                sys.exit(f"{name} markers not found in {page}")
        block = translate(de[de.index(start) + len(start):de.index(end)], missing)
        en = en[:en.index(start) + len(start)] + block + en[en.index(end):]
    if missing:
        sys.exit("No English text yet for (add it in tools/build_en.py):\n  " + "\n  ".join(dict.fromkeys(missing)))
    EN.write_text(en, encoding="utf-8")
    print("en/index.html: Vorträge/Presse and Texte blocks updated.")


if __name__ == "__main__":
    main()
