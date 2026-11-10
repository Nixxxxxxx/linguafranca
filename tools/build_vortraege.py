"""Rebuilds the "Vorträge" and "Fernsehen & Presse" lists in index.html.

Edit the VORTRAEGE / MEDIEN lists below (newest first), then run from the project root:
    python -I tools/build_vortraege.py
Logos live in images/logos/ (fetch new ones with tools/fetch_logos.py). logo=None shows the
organisation name as a text badge instead. link=None shows the title without a link.
Rewrites everything between <!-- VORTRAEGE:START --> and <!-- VORTRAEGE:END --> in index.html.
"""
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (logo file in images/logos/ or None, organisation, meta line, title, description, link or None)
VORTRAEGE = [
    ("dbvc-coaching27.png", "DBVC", "16. Apr 2027 · Keynote", "Coaching '27, DBVC-Kongress, Erfurt",
     "Keynote zum Kongressmotto „Dialog stärken, Demokratie begleiten“", "https://kongress.dbvc.de/dr-franca-parianen/"),
    ("sosafe-signal.png", "SoSafe", "18. Nov 2026 · Masterclass", "Signal Security Summit, Köln",
     "„Sicheres Verhalten nachhaltig verankern: Was wir aus der Neurowissenschaft lernen können“",
     "https://signal.sosafe-awareness.com/cologne/agenda/"),
    (None, "6. Deutscher Fußverkehrskongress", "29. Sep 2026 · Science Slam", "6. Deutscher Fußverkehrskongress, Bielefeld",
     "„Warum Menschen zusammenhalten müssen, aber nicht wollen (auch im Straßenverkehr)“",
     "https://www.fuko.nrw.de/referierende/"),
    # smmdays.de answered every page with 401 on 2026-11-10, so no link and no logo for now.
    (None, "Social Media Marketing Days", "Nov 2022 · Eröffnungskeynote", "Social Media Marketing Days",
     "„83 Milliarden Neuronen gefällt das!“", None),
    ("youmecon.svg", "YouMeCon", "Okt 2022 · Podium", "YouMeCon",
     "Podiumsdiskussion: Digitale Medien", "https://youmecon.de/"),
    ("hercareer.png", "herCAREER", "Okt 2022 · Lesung", "herCAREER Expo, München",
     "Author Meet & Greet zu „Teilen und Haben“", "https://www.her-career.com/kopf/dr-franca-parianen/"),
    ("ihk-muenchen.png", "IHK für München und Oberbayern", "Keynote", "11. Bayerischer CSR-Tag",
     "„Warum wir zukünftig stärker zusammenhalten müssen, aber nicht wollen“",
     "https://www.youtube.com/watch?v=9HIz-aX5oEc"),
    ("frankfurter-zukunftskongress.jpg", "Frankfurter Zukunftskongress", "Feb 2021 · Keynote",
     "Frankfurter Zukunftskongress",
     "Keynote gemeinsam mit Richard David Precht: Zusammenleben mit 8 Milliarden Gehirnen",
     "https://www.youtube.com/watch?v=Qd2WeihcwtE"),
    ("visitberlin.svg", "visitBerlin", "2021 · Speakerin", "visitBerlin BEST-Ival", "Speakerin",
     "https://convention.visitberlin.de/speaker-beim-bestival-2021"),
    ("kulturelle-landpartie.png", "Kulturelle Landpartie", "Podium", "Kulturelle Landpartie",
     "Podiumsdiskussion: Teilen und Haben",
     "https://www.kulturelle-landpartie.de/personen.html?action=&order=punkte_dn&s_type=&s_string="),
    ("zeit-stiftung.png", "ZEIT-Stiftung", "Podium", "ZEIT-Stiftung",
     "„Was hält unsere Gesellschaft zusammen? Miteinander teilen“, mit Steffen Mau und Robert Habeck",
     "https://twitter.com/HoltzbrinckBLN/status/1200399498322817026"),
    # b2bvertriebskongress.at did not respond on 2026-11-10, so no logo.
    (None, "B2B-Vertriebskongress", "Keynote", "B2B-Vertriebskongress, Wien",
     "Lernen vom ältesten sozialen Netzwerk der Welt",
     "https://industriemagazin.at/a/das-war-der-1-b2b-vertriebskongress?img=40416"),
    ("learntec.png", "LEARNTEC", "2019 · Keynote", "LEARNTEC, Karlsruhe",
     "Soziale Bedürfnisse motivieren uns zum Lernen",
     "https://www.haufe.de/personal/hr-management/franca-parianen-soziale-beduerfnisse-motivieren-zum-lernen_80_484000.html"),
    # The programme brochure that listed this talk now returns 404.
    ("polytechnische.svg", "Polytechnische Gesellschaft", "Vortrag", "Polytechnische Gesellschaft, Frankfurt",
     "Vortragsreihe „Zukunft Mensch“", None),
    ("../hormone_gesteuert.png", "Hormongesteuert", "Bühne", "Wissens-Comedy-Premiere",
     "Hormongesteuert? Wie Männer und Frauen beeinflusst werden", "https://www.youtube.com/watch?v=TxC1amupOII"),
    ("ideenexpo.svg", "IdeenExpo", "2017 · Science Slam", "IdeenExpo, Hannover", "Science Slam, Vize-Gewinnerin",
     "https://www.ideenexpo.de/content/franca-parianen-lesemann-gewinnt-zweiten-science-slam-im-pavillon-hannover"),
    ("scienceslam.svg", "Science Slam", "2014 · Science Slam", "Deutsche Meisterschaft im Science Slam",
     "Science Slam über die Neurowissenschaft des Mitgefühls", "https://www.youtube.com/watch?v=udUKDVCFc_U"),
    ("scienceslam.svg", "Science Slam", "Science Slam", "Science Slam Berlin",
     "Seit 2014 auf Science-Slam-Bühnen", None),
]

MEDIEN = [
    ("zdf.png", "ZDF", "ZDF · Expertin", "Eckart von Hirschhausen: Der Sünde auf der Spur",
     "Interview zu sozialer Kognition und Neid",
     "https://www.zdf.de/dokumentation/dokumentation-sonstige/eckart-von-hirschhausen-der-suende-auf-der-spur-100.html"),
    ("zdf.png", "ZDF", "ZDF · 2017 · Gast", "Markus Lanz",
     "Gast in den Sendungen vom 25.04.2017 und 03.10.2017", None),
    ("zdf.png", "ZDF", "ZDF · Redaktion", "Aurel Original", "Redaktion, Recherche", None),
    ("ndr.png", "NDR", "NDR · Gast", "Tietjen und Bommes", "Talkshow-Gast", None),
    ("3sat.png", "3sat", "3sat · Gast", "Scobel: Die Magie des Spielens",
     "Durch Spielen entwickeln wir viele unserer Fähigkeiten.",
     "https://pressetreff.3sat.de/programmwochen/programmwoche///02.05.2019/02.05.2019/bc/zeige/b68a1ca6-1fe2-470b-84f4-072ed85f7c5c/"),
    ("sz-magazin.png", "SZ Magazin", "SZ Magazin · Interview", "Die Liebe ist eine Naturgewalt",
     "Interview über Hormone und Liebe",
     "https://sz-magazin.sueddeutsche.de/liebe-und-partnerschaft/hormone-liebe-franca-parianen-90822?reduced=true"),
    ("stern.png", "Stern", "Stern · Interview", "Wie der Zyklus das Liebesleben bestimmt", "Interview",
     "https://www.stern.de/familie/beziehung/wie-der-weibliche-zyklus-das-liebesleben-bestimmt--31438294.html"),
    ("welt.png", "Welt", "Welt · Interview", "Sie hat die beste Antwort auf „Du hast wohl deine Tage“",
     "Interview: Auch Männer sind hormongesteuert",
     "https://www.welt.de/icon/iconista/article206686947/Auch-Maenner-sind-hormongesteuert-Interview-mit-Wissenschaftlerin-Franca-Parianen.html"),
]


def cards(items, ind):
    e = html.escape
    out = []
    for logo, org, meta, title, desc, link in items:
        tile = (f'<img src="./images/logos/{e(logo)}" alt="Logo {e(org)}" loading="lazy">' if logo
                else f'<span class="logo-text">{e(org)}</span>')
        t = (f'<a class="title" href="{e(link)}" target="_blank" rel="noopener">{e(title)}</a>' if link
             else f'<span class="title">{e(title)}</span>')
        out.append(f'{ind}<li class="appearance">\n'
                   f'{ind}    <div class="logo">{tile}</div>\n'
                   f'{ind}    <div class="body"><span class="meta">{e(meta)}</span>{t}'
                   f'<span class="desc">{e(desc)}</span></div>\n'
                   f'{ind}</li>')
    return "\n".join(out)


def category(title, items, extra=""):
    ind = " " * 16
    return (f'{ind}<div class="category"{extra}>\n'
            f'{ind}    <h3>{html.escape(title)}</h3>\n'
            f'{ind}    <ul class="appearances">\n'
            f'{cards(items, ind + "        ")}\n'
            f'{ind}    </ul>\n'
            f'{ind}</div>')


def main():
    missing = [l for l, *_ in VORTRAEGE + MEDIEN if l and not (ROOT / "images" / "logos" / l).exists()]
    if missing:
        sys.exit(f"Missing logo files in images/logos/: {missing}")
    page = ROOT / "index.html"
    s = page.read_text(encoding="utf-8")
    start, end = "<!-- VORTRAEGE:START -->", "<!-- VORTRAEGE:END -->"
    if start not in s or end not in s:
        sys.exit("Markers not found in index.html")
    body = category("Vorträge", VORTRAEGE) + "\n\n" + category("Fernsehen & Presse", MEDIEN, ' id="medien"')
    a, b = s.index(start) + len(start), s.index(end)
    page.write_text(s[:a] + "\n" + body + "\n                " + s[b:], encoding="utf-8")
    print(f"Built {len(VORTRAEGE)} Vorträge and {len(MEDIEN)} Fernsehen & Presse entries.")


if __name__ == "__main__":
    main()
