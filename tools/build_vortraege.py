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
    # The theatre's own page no longer lists the July panel, so the link is nachtkritik's review, which describes it.
    ("ernst-deutsch-theater.svg", "Ernst Deutsch Theater", "11. Jul 2026 · Podium", "„Timmy – Die Hope stirbt zuletzt“, Ernst Deutsch Theater, Hamburg",
     "Podium nach der Premiere: warum Empathie ein Gesicht und einen Namen braucht",
     "https://nachtkritik.de/nachtkritiken/deutschland/hamburg-schleswig-holstein/hamburg/ernst-deutsch-theater-hamburg/timmy-die-hope-stirbt-zuletzt-ernst-deutsch-theater-hamburg-alexander-kiessinger-montiert-einen-abend-zwischen-pop-und-passion"),
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
    ("3sat.png", "3sat", "3sat · 26. Feb 2026 · Gast", "NANO Talk: Neues Sprechen – wie uns unsere Sprache verrät",
     "Mit Stephanie Rohde: wie Worte Gefühle, Entscheidungen und sogar das Gehirn verändern",
     "https://www.3sat.de/wissen/nano-talk/260226-sendung-nano-talk-mit-stephanie-rohde-neues-sprechen-wie-uns-unsere-sprache-verraet-ntk-100.html"),
    ("zdf.png", "ZDF", "ZDF · Expertin", "Eckart von Hirschhausen: Der Sünde auf der Spur",
     "Interview zu sozialer Kognition und Neid",
     "https://www.zdf.de/dokumentation/dokumentation-sonstige/eckart-von-hirschhausen-der-suende-auf-der-spur-100.html"),
    ("zdf.png", "ZDF", "ZDF · 2017 · Gast", "Markus Lanz",
     "Gast in den Sendungen vom 25.04.2017 und 03.10.2017", None),
    ("aurel-original.jpg", "Aurel Original", "ZDF · Redaktion", "Aurel Original", "Redaktion, Recherche", None),
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
    # Interviews and podcasts found by web search on 2026-11-10 (newest first). Psychologie Heute is a book review, added on
    # the user's request. Skipped: NDR "Science Slam im Podcast" (404), Frankfurter Zukunftskongress newsroom interview
    # (domain now belongs to someone else), Sheconomy (reprint of the herCAREER interview).
    ("nachtkritik.svg", "nachtkritik.de", "nachtkritik.de · Jul 2026 · Kritik", "Timmy – Die Hope stirbt zuletzt",
     "Kritik zum Abend im Ernst Deutsch Theater, die ihren Podiumsbeitrag „erhellend“ nennt",
     "https://nachtkritik.de/nachtkritiken/deutschland/hamburg-schleswig-holstein/hamburg/ernst-deutsch-theater-hamburg/timmy-die-hope-stirbt-zuletzt-ernst-deutsch-theater-hamburg-alexander-kiessinger-montiert-einen-abend-zwischen-pop-und-passion"),
    (None, "Nachgefragt Podcast", "Podcast · Mai 2026", "Hormone – Zwischen Wissenschaft und Vorurteil",
     "Wie Hormone im Gehirn wirken und wo biologische Erklärungen zu kurz greifen (NGF087)",
     "https://nachgefragt-podcast.de/2026/05/20/hormone-wissenschaft-vorurteile/"),
    (None, "PVS einblick", "PVS einblick · Feb 2024 · Interview", "Spannende Schnittstelle zwischen Herz, Hirn und Gesundheit",
     "Über Hormone, Motivation und Herzklopfen",
     "https://www.pvs-einblick.de/gesundheit/spannende-schnittstelle-zwischen-herz-hirn-und-gesundheit"),
    (None, "Nachgefragt Podcast", "Podcast · Sep 2023", "Warum hört die Politik nicht auf die Wissenschaft?",
     "Mit Sarah Hiltner über das Buch „Weltrettung braucht Wissenschaft“ (NGF65)",
     "https://nachgefragt-podcast.de/2023/09/12/ngf65-warum-hoert-die-politik-nicht-auf-die-wissenschaft/"),
    ("hercareer.png", "herCAREER", "herCAREER Voice · Podcast · Jun 2023", "Teilen und Haben",
     "Über Gemeingüter und warum Teilen keine Großzügigkeit ist",
     "https://www.her-career.com/podcast-teilen-und-haben/"),
    (None, "Radio Magic City Six", "Freie Radios · Apr 2023 · Radiointerview", "Hormone – Freund oder Feind?",
     "Über Hormone, Werdegang und Science Slams",
     "https://www.freie-radios.net/121704"),
    (None, "The Writer's Pit", "Podcast · Okt 2022", "Franca Parianen: Teilen und Haben",
     "Gespräch über das Buch „Teilen und Haben“",
     "https://www.rainerboettchers.de/podcast/franca-parianen-teilen-und-haben/"),
    ("hercareer.png", "herCAREER", "herCAREER · Aug 2022 · Interview", "„Wenn wir uns zusammentun, haben wir alle mehr.“",
     "Über Formen des Teilens und was Männer und Frauen dabei unterscheidet",
     "https://www.her-career.com/wenn-wir-uns-zusammentun-haben-wir-alle-mehr/"),
    (None, "Mildly Interesting", "Podcast · Okt 2021", "Kuschelhormone & Gerechtigkeit",
     "Über Bindungshormone und Fairness",
     "https://podcasts.apple.com/de/podcast/kuschelhormone-gerechtigkeit-mit-dr-franca-parianen/id1530095929?i=1000539212762"),
    # No Abendblatt logo on Wikimedia Commons, so a text badge.
    (None, "Hamburger Abendblatt", "Hamburger Abendblatt · Mär 2021 · Interview", "„Alle teilen das Gleiche: Frust“",
     "Über Ungerechtigkeit und das Buch „Teilen und Haben“",
     "https://www.abendblatt.de/hamburg/kultur/article401906934.ece"),
    (None, "KüchenTalk", "Podcast · Mär 2021", "Mit Hirn, Herz und Hormonen",
     "Über Stress- und Bindungshormone",
     "https://kuechentalk.podcaster.de/kuechentalk/3-mit-hirn-herz-und-hormonen-mit-franca-parianen-21-3-2021/"),
    (None, "Psychologie Heute", "Psychologie Heute · Nov 2020 · Buchbesprechung", "Hormongesteuert?",
     "Besprechung von „Hormongesteuert ist immerhin selbstbestimmt“",
     "https://www.psychologie-heute.de/gesundheit/artikel-detailansicht/40839-hormongesteuert.html"),
    (None, "Einfach ganz leben", "Podcast · Interview", "Hormon-Expertin Dr. Franca Parianen",
     "Mit Jutta Ribbrock: wie Östrogen, Testosteron, Oxytocin & Co. unser Leben beeinflussen",
     "https://www.einfachganzleben.de/gesundheit-ernaehrung/podcast-42-hormon-expertin-franca-parianen"),
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
