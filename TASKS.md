# lingua-franca.eu: handover

## What this is
Personal website of Dr. Franca Parianen (neuroscientist, author, speaker). Static site hosted on
GitHub Pages from `main` of https://github.com/Nixxxxxxx/linguafranca (custom domain via `CNAME`:
lingua-franca.eu). **Pushing to `main` publishes the live site.**

## History
- **2026-11-10**: User asked: "make the website more professional." Full redesign done:
  - Replaced the jQuery `.load()` fragment site (bright teal, hover-zoom cards, blurred "past" cards,
    typewriter effect) with a single static one-page site: `index.html` with sections
    Über mich / Bücher / Vorträge & Medien / Texte / Kontakt, plus a standalone `impressum.html`.
  - New hand-written `css/site-style.css`: off-white background, deep teal accent (#0f4c45), serif headings.
  - Removed `main_content.html`, `termine.html`, `blog.html`, `contact.html` (their content now lives in `index.html`; old versions in git history).
  - The old 2022 "Demnächst" events were moved into the speaking list with their dates, so the site no longer shows out-of-date "upcoming" events.

- **2026-11-10 (later)**: User asked: "update for seo". Done:
  - `index.html` head: sharper title/description, robots, Open Graph (`og:type=profile`) and Twitter card tags,
    and JSON-LD structured data (WebSite, ProfilePage, Person with sameAs links, and the five books).
  - `images/og-image.jpg` (1200x630 share preview), built by `python tools/make_og_image.py` (re-run if the photo or text changes).
  - Compressed `images/franca.jpg` (248 KB to 51 KB) and `images/buch2.jpg` (247 KB to 50 KB). Hero photo preloaded with `fetchpriority=high`.
  - Added `robots.txt` (blocks the unused test and old blog files), `sitemap.xml` and `404.html`. The Impressum is `noindex, follow`.

- **2026-11-10 (later)**: User asked: link the individual texts from her torial portfolio
  (https://www.torial.com/franca.dr-parianen) under "Texte", using torial's images. Done (not pushed yet):
  - `tools/update_texte.py` fetches all torial pages, saves card images to `images/texte/<id>.jpg` and rewrites the section
    between `<!-- TEXTE:START -->` / `<!-- TEXTE:END -->` in `index.html`. **To add new texts: put them on torial, then run
    `python -I tools/update_texte.py`.** Texts not on torial go in the `EXTRA` list in the script.
  - Shows 30 texts (26 from torial), newest first (23 taz, 1 Berliner Zeitung, 2 Deutschlandfunk Kultur): 9 cards, then an "Alle 30 Texte anzeigen" toggle.
    The 4 older texts not on torial (Spektrum, Barbara, 2x Steady) are cards at the end (user asked to drop the separate
    "Weitere Veröffentlichungen" list). Their preview images come from each page's og:image; Spektrum has none (its site
    blocks scripts), so it shows a teal placeholder card with the outlet name.
  - torial gives no publication dates, so the order uses the taz article number (higher = newer); the other outlets come after the taz texts.

- **2026-11-10 (later)**: User asked: split "Bühne & Vorträge" and "Fernsehen & Presse" into two stacked categories with
  logos; web-search her keynotes and add them under "Vorträge" with link and organiser logo, no duplicates. Done (not pushed yet):
  - Lists live in `tools/build_vortraege.py` (VORTRAEGE / MEDIEN, newest first). **Edit there and run
    `python -I tools/build_vortraege.py`**; it rewrites the block between `<!-- VORTRAEGE:START/END -->` in `index.html`.
  - Logos in `images/logos/`, fetched by `python -I tools/fetch_logos.py` (sources listed in the script; Wikimedia Commons
    where possible). The Frankfurter Zukunftskongress tile is cropped from the old `images/frankfurt.jpg` event graphic.
  - New from the web search: SoSafe Signal Security Summit Köln (18 Nov 2026, masterclass, upcoming), Social Media Marketing
    Days 2022 opening keynote, 11. Bayerischer CSR-Tag keynote (IHK München), Polytechnische Gesellschaft "Zukunft Mensch",
    Deutsche Meisterschaft im Science Slam 2014. Also upgraded existing entries: Frankfurter Zukunftskongress = keynote
    with R. D. Precht (Feb 2021, now linked to the YouTube video), LEARNTEC 2019 = keynote. ZEIT-Stiftung/Holtzbrinck panel was
    one event and is listed once.
  - Without links: SMM Days (smmdays.de answers 401 on every page), Polytechnische (brochure PDF is 404).
    Text badge instead of logo: SMM Days, B2B-Vertriebskongress (site didn't respond).
  - Sources: speakerinnen.org/de/profiles/dr-franca-parianen, signal.sosafe-awareness.com/cologne/agenda,
    youtube.com/watch?v=9HIz-aX5oEc (CSR-Tag), youtube.com/watch?v=Qd2WeihcwtE (Zukunftskongress), web search results for SMM Days.
  - Not added (not a talk): LifeScienceXplained | Sartorius prize 2024 (from Rowohlt author page), which could go in the bio.
- 2026-11-10 **New main domain: parianen.com** (bought at GoDaddy; a second GoDaddy domain is still unnamed). User chose
  parianen.com as the main address (not a forward). Done locally: `CNAME` = `parianen.com` (typo line removed), all URLs in
  index.html/impressum.html/robots.txt/sitemap.xml switched, og-image regenerated with "parianen.com".
  Mail subject still says "Anfrage über parianen.com" (was lingua-franca.eu). NOT pushed.
  parianen.com DNS at GoDaddy has Microsoft 365 email records (autodiscover, msoid, lyncdiscover, sip, email, DKIM
  selector1/2): never touch them. No MX/TXT visible in the user's paste (may be cut off).
  Order of steps: (1) user sets GoDaddy DNS: delete `A @ Parked`, add A @ 185.199.108.153/109/110/111 and
  `CNAME www nixxxxxxx.github.io`; (2) after DNS resolves, push (CNAME change switches the Pages domain);
  (3) GitHub Settings → Pages: Enforce HTTPS (cert can take up to ~1h); (4) lingua-franca.eu: 301 forward to
  https://parianen.com at its registrar (once it no longer points to GitHub it stops serving the site);
  (5) Search Console: add parianen.com, use "Change of address" from lingua-franca.eu.

- 2026-11-10 Kontakt: X/Twitter link replaced by Bluesky (https://bsky.app/profile/fparianen.bsky.social) and Mastodon
  (https://mastodon.social/@Fparianen, found via the Bluesky/Mastodon search APIs; bio matches). Each has its own icon
  (Simple Icons paths, inline SVG). JSON-LD sameAs updated, twitter:site/creator meta removed, `rel="me"` link to Mastodon
  added (lets her add parianen.com as a verified link in her Mastodon profile). Pushed 2026-11-10 (user OK).

- 2026-11-10 Vorträge: added Coaching '27 DBVC-Kongress Erfurt (16 Apr 2027, keynote, title not published yet; logo
  images/logos/dbvc-coaching27.png) and 6. Deutscher Fußverkehrskongress Bielefeld (29 Sep 2026, Science Slam "Warum Menschen
  zusammenhalten müssen, aber nicht wollen (auch im Straßenverkehr)"; text badge because fuko.nrw.de only uses the NRW
  coat of arms, which is not free to use). Sources: kongress.dbvc.de/dr-franca-parianen/, fuko.nrw.de/referierende/.
  Pushed 2026-11-10 (user OK).

- 2026-11-10 Fernsehen & Presse: +10 interviews/podcasts from web search (Nachgefragt NGF087 May 2026 + NGF65 Sep 2023,
  PVS einblick Feb 2024, herCAREER Voice podcast Jun 2023, Radio Magic City Six Apr 2023, The Writer's Pit Oct 2022,
  herCAREER interview Aug 2022, Mildly Interesting Oct 2021, KüchenTalk Mar 2021, Einfach ganz leben #42). Text badges
  except herCAREER. Psychologie Heute book review (Nov 2020) and Hamburger Abendblatt interview (30 Mar 2021) added on the user's request; 3sat NANO Talk (26 Feb 2026, guest of Stephanie Rohde) added at the top of the list. Aurel Original tile now uses the show's key art from IMDb (tt16439326), cropped to the title lettering by `aurel()` in tools/fetch_logos.py (images/logos/aurel-original.jpg). Skipped: NDR Science-Slam podcast (404), Frankfurter Zukunftskongress
  newsroom interview (domain now someone else's), Sheconomy (reprint of the herCAREER interview), Dlf Kultur pieces (her own
  commentaries, not interviews). Pushed 2026-11-10 (commit 21b92f2, user OK).

- 2026-11-10 Timmy (Ernst Deutsch Theater, Hamburg): user asked to add the nachtkritik review under Presse and under Talks with an Ernst Deutsch Theater icon. Vorträge: "11. Jul 2026 · Podium" (panel after the premiere of „Timmy – Die Hope stirbt zuletzt“), logo images/logos/ernst-deutsch-theater.svg (the theatre's wordmark from its site), linked to the nachtkritik review because the theatre's event page no longer lists the July panel. Fernsehen & Presse: nachtkritik.de review (Jul 2026), logo images/logos/nachtkritik.svg (their logo2019.svg, white fill changed to #1a1a1a so it shows on the light tile). Both logos in tools/fetch_logos.py. The Hamburger Abendblatt review (Hannah Mahé Crüsemann, 14 Jul 2026; the user remembers her called „extrem erhellend und angenehm“ there) could not be opened (abendblatt.de blocks the tools, paywall): add it once the user has the link. Pushed 2026-11-10 (commit 21b92f2, user OK).

- 2026-11-10 Vorträge: + Social Design Days, Nürnberg (dated Okt 2024 on the user's instruction, "humorvoller Pitch zum Menschen als sozialem
  Wesen", bayern design logo images/logos/bayern-design.svg), source bayern-design.de/beitrag/her-mit-dem-guten-leben/
  (page description says 2024, body text says 2025). Pushed 2026-11-10 (user OK).

- 2026-11-10 User asked for 8 design variations (focus: icon vs. text placement, balance, size). Built by 8 parallel
  agents as local drafts in `design-variants/v1..v8/` (index.html + style.css each, images via ../../images/). The folder
  is in .gitignore, so it is never published. Directions: v1 editorial magazine (small greyscale logos in rows), v2 logo
  wall, v3 Swiss minimal table, v4 timeline, v5 dark bold keynote, v6 warm centered icon-on-top, v7 compact product-UI
  cards, v8 asymmetric sticky split. All 8 finished and checked (all 75 links present, no broken images, no external requests). Overview page: `design-variants/index.html` (screenshots in design-variants/_shots/). Waiting for the user to pick one or mix; then port the
  chosen design into the live index.html + css/site-style.css (keep tools/build_vortraege.py and update_texte.py markup
  in sync if card markup changes).
- 2026-11-10 **User picked v5 (dark keynote) as the base**, but its "Auf Bühnen und im Programm" section does not fit
  (42 cards with big white logo panels: a glaring checkerboard, about 5000px tall). Built 8 alternatives for just that section:
  `design-variants/v5a..v5h/` (each = v5 page + own section.css; shares ../v5/style.css). Generator:
  `python -I design-variants/_gen/make_v5_sections.py` (run from project root; parses entries from v5/index.html),
  screenshots: `sh _gen/shots.sh` from design-variants/. Overview: `design-variants/v5-sektion.html`.
  v5a highlights + rows, v5b dark logo grid, v5c tabs, v5d setlist, v5e carousel, v5f 6 highlights + "Alle anzeigen",
  v5g two year-timelines (re-sorts Medien by date), v5h logo marquee + stats + accordions.
  Logo rule learned: only plain wordmarks survive a white-silhouette filter (MONO_OK list in the generator); other logos
  go on a small light chip; text-only entries get a type icon (mic/newspaper/lectern) in small slots.
  All 35 section links and all images verified in each. **Waiting for the user to pick one (or mix).** Then port v5 +
  the chosen section to live index.html/css and update tools/build_vortraege.py to emit the new markup.
- 2026-11-10 User likes v5's header energy, but the hard black/white contrast below is tiring to read. Asked for examples
  with the header kept and the lower parts light with black text, or the same energy in other colour schemes.
  Built `design-variants/v5t1..v5t8` with `python -I design-variants/_gen/make_v5_themes.py [section, default v5f]`:
  it rewrites v5 style.css + the section css into token-only CSS (`design-variants/v5-themes/`), each theme = theme.css.
  t1 paper & coral, t2 white with dark hero/contact frame, t3 sand with dark books band, t4 light with coral contact
  finale (all dark header/hero, light sections); t5 navy & yellow, t6 aubergine & mint, t7 forest & apricot,
  t8 indigo & pink (full dark, softer off-white text). On light sections the accent is darkened (#c63f1c-ish) for text
  contrast and white logo silhouettes become dark ones. Overview: `design-variants/v5-farben.html`.
  **Waiting: user picks colour scheme + section variant.**
- 2026-11-10 User: take v5t1, with the sand colours of v5t3 for the lower part, plus v1's big "Kurzgefasst" lead
  article with the rest below; lead = new taz text „KI und Automatisierung machen uns dümmer, ist das wirklich so
  schlimm?“ (taz 15 Dec 2025, by Franca, not on torial yet; image saved as images/texte/taz-6133816.jpg, untracked
  until the port), rotating to other texts after a while or on click. Built as `design-variants/v5x/`:
  `python -I design-variants/_gen/make_v5_themes.py && python -I design-variants/_gen/make_v5_texte.py`.
  Lead rotates through 5 texts every 7s (tabs to click, pause button, pauses on hover/focus, off for
  prefers-reduced-motion; small inline script, no external requests); then 8 texts in two columns of rows, the rest
  behind "Alle 31 Texte anzeigen". Bühnen section is still v5f there. When porting: add the KI text to
  tools/update_texte.py EXTRA (or a FEATURED list) and teach the script to emit the lead + rows markup.
- 2026-11-10 Added the 2 newest taz texts from https://taz.de/Franca-Parianen/!a131503/ (not on torial):
  „Knutschen ist Trumpf“ (Bindungsverhalten, Oct 2026, !6214458) and „Alles eine Frage des Timings!“ (Kürzere
  Geburten, Apr 2026, !6165835), images images/texte/taz-6214458.jpg / taz-6165835.jpg (NEWER in make_v5_texte.py).
  Lead rotation now: KI → Knutschen → Timing → Denken → Denkfalle; 33 texts. The author page also lists 3 more texts
  missing from the site (!6126486 Homeoffice/Ben Rein interview, !6114890 Keuchhusten-Impfung, !6081724 Sexismus beim
  Intelligenzbegriff): offered to the user, not added.
- 2026-11-10 New site icon: prompt for an image generator (6x6 sheet, 36 variations in the v5x palette) saved at
  `C:\Users\D\Desktop\website-icon-prompt.txt`.
- 2026-11-10 User picked row 4, column 6 of the generated sheet (`Downloads\Neuroscience Icon Grid Collection.png`):
  coral neuron on an off-white rounded tile. `python -I tools/make_icons.py` re-draws it in exact brand colours from
  images/icon-source.png (the tile cut from the sheet) → favicon.ico (16/32/48), images/favicon-16/32/48.png,
  images/icon-512.png, images/apple-touch-icon.png (180, square, no transparency). Linked in index.html,
  impressum.html, 404.html (replaces images/icon.png, which is now unused). Pushed with the user's OK.
  Only the icon went live; the v5x redesign is still local and waiting for the Bühnen-section choice.
- 2026-11-10 **v5x with Bühnen section v5f went live** (user: "go ahead with v5f, then push").
  - index.html = previous SEO head (canonical, JSON-LD, OG, icons) + v5x body; css/site-style.css = one flat file
    (v5 base tokenised + Impressum/404 light styles + v5f section flattened, no CSS nesting + sand colours +
    Kurzgefasst); js/site.js = lead rotation (loaded with defer).
  - tools/build_vortraege.py now emits highlight cards (VORTRAEGE_HIGHLIGHTS / MEDIEN_HIGHLIGHTS) + a list behind
    "Alle … anzeigen". tools/update_texte.py now emits the rotating lead (LEAD = KI, Knutschen, Timing; FEATURED from
    torial) + rows + "Alle … Texte anzeigen". Both were re-run after the port and give identical output (78 links).
  - Impressum and 404 now render on the sand background (class .legal gets the light tokens).
  - design-variants/ stays local (gitignored); its generators are no longer the source of the live CSS. Edit
    css/site-style.css directly from now on.

- 2026-11-11 **Big content edit list from the user: done and pushed 2026-11-11 (commit a5a27c4, user OK), incl. everything below (English page, SEO).**
  - Hero "Dr." now in the display sans font (.h1-pre). About: "Über mich" eyebrow and "Kurzbio" cite removed; new bio
    (user's text, proofread: Bestsellerautorin, Studium der Neurowissenschaften, Science-Slammerin, «» quotes,
    "ins Französische und Koreanische", "in Print und Fernsehen", "im taz-Ressort Zukunft", second "regelmäßig" dropped,
    garbled "Für ihre Vorträge Speakerin erhielt die Speakerin" fixed). Fact boxes: Promotion / Ausgezeichnet /
    Bestseller + Rowohlt Verlag / Wissenschafts&shy;kommunikatorin. Photo images/sartorius-ndr-2024.jpg (from
    Downloads\grafik.png, 1200px) under the fact boxes, caption "Verleihung des Sartorius und NDR Sachbuchpreises 2024".
  - Vorträge: tools/build_vortraege.py entries now start with a sort date and are sorted newest first; the 9 newest are
    cards (VORTRAEGE_HIGHLIGHTS = 9), rest in the list. New: SUPERZART* Festival (17 Oct 2026, Schauspielhaus Hamburg),
    Deutscher Innovationspreis 2024, Harbour Symposium 2023 Basel (text badge: harbourclub.ch blocks downloads; user
    could save the logo as images/logos/harbourclub.png), 10. IHK-Unternehmerinnentag (7 Jul 2023, "Impulsvortrag" per
    user; IHK page says Science Slam). Removed YouMeCon, Wissens-Comedy-Premiere, Science Slam Berlin. Fußverkehrskongress
    = Eröffnungsimpuls. Estimated sort dates (no date shown): CSR-Tag 2023, Kulturelle Landpartie 2022, Polytechnische 2020.
    Intro text "Keynotes und andere Auftritte (exemplarisch)". "Fernsehen & Presse" → "Presse".
  - Presse: + Brigitte and IMDb entries with PLACEHOLDER titles (both sites block the fetch tools, Chrome extension
    not connected): ask the user for the real headline / show name.
  - Lead text title "dümmer" → "denkfauler" (update_texte.py LEAD + index.html; taz URL unchanged).
  - Email franca@parianen.com everywhere on index.html (incl. JSON-LD). Contact: h2 "…Podiumsdiskussion anfragen",
    intro paragraph removed, button label "Anfrage". Hero "Anfrage senden" icon = paper plane.
  - User's answers (same day), all applied: prize = "LifeScience Xplained Award 2024 | Sartorius-Preis für neue
    Kommunikation" (fact box + bio); photo credit "Foto: Sartorius AG"; Brigitte title „Kooperieren als Gesellschaft:
    Frauenfreundschaften sind buchstäblich lebensrettend“; IMDb link = "Scobel: Herz intakt?" with scobel logo
    (images/logos/scobel.png, Commons, recoloured dark); Harbour Club logo images/logos/harbourclub.png (from
    Downloads\HarbourClub.jpg) on the Vorträge card; new Presse entry HarbourClub „Adrenalin, Herzklopfen und
    geweitete Pupillen“ (harbourclub.ch/de/newsdetail/…); Innovationspreis = Keynote; impressum.html email →
    franca@parianen.com. Presse now has 9 cards (+ Brigitte, Scobel, HarbourClub).
  - Menu item "Über mich" → "Biographie" in index.html, impressum.html, 404.html (anchor #ueber-mich kept so old links work).
  - "Zu erleben bei" strip: Keynotes, Impulse, Lesungen, Science Slams, Interviews, Fernsehen.
  - New section "Vortragsthemen" (#themen, between Bücher and Vorträge, nav link added): 5 topics as <details>
    accordions (title + subtitle visible, text opens on click), CSS block "Vortragsthemen" at the end of
    css/site-style.css. Backgrounds re-alternated: themen plain, Vorträge section-alt, Texte plain. Text = user's,
    proofread (list of fixes given to the user in chat on 2026-11-11). User confirmed "Wer Wissen abspeichert" is
    intended; topic 5 subtitle changed to "86 Milliarden Neuronen gefällt das" (SMM Days 2022 entry keeps its original
    title "83 Milliarden…").
  - SEO for "speaker + topic / neuroscience" searches: title "Dr. Franca Parianen – Keynote-Speakerin
    Neurowissenschaft", new meta/OG description naming the 5 topics; JSON-LD Person: jobTitle Keynote-Speakerin first,
    topic keywords in knowsAbout (+ Gesellschaft, Transformation, Nachhaltigkeit on the user's request; they replaced Sozialpsychologie/Politikwissenschaft), alumniOf (Utrecht, Münster, Twente per Wikipedia; + Jacobs University Bremen and MPI für Kognitions- und Neurowissenschaften Leipzig per user), award, sameAs + Wikipedia
    (de.wikipedia.org/wiki/Franca_Parianen), makesOffer = 5 keynote Services; hero eyebrow "Keynote-Speakerin";
    Vortragsthemen intro sentence (added by me, user may reword); topic titles are now <h3> inside <summary>;
    sitemap lastmod 2026-11-11 + award image.
  - **English version** (user: open to talks abroad, fluent in English): `en/index.html` (= parianen.com/en/), my
    translation of all static text (British spelling; book/article/event titles stay German, books get an English gloss
    in the bio; added sentence "She speaks in English and German, in Germany and internationally."). DE | EN switch in
    both headers (.lang), hreflang de/en/x-default in both heads + sitemap.xml, og:locale pairs, English JSON-LD
    (same Person @id). German page: Vortragsthemen intro now "Auf Deutsch oder Englisch, in Deutschland und
    international."; JSON-LD knowsLanguage de/en, areaServed removed (user: open to all countries).
    **How the EN lists stay in sync:** tools/build_en.py copies the VORTRAEGE and TEXTE blocks from index.html into
    en/index.html, translating labels/dates and descriptions via DESC_EN / LEAD_EN; it stops and names any entry
    without an English text. build_vortraege.py and update_texte.py call it automatically at the end.
    Everything else in en/index.html is edited by hand: any change to German static text must be mirrored there.
    js/site.js picks pause/play labels by <html lang>. Impressum stays German-only (footer link says "(German)").
    Gotcha: the DE/EN links are "./en/" and "../", which open a folder listing when previewing via file://;
    use `python -m http.server 8000` to test the switch locally.
  - 2026-11-11 Hero surname: on phones (≤860px) "Parianen" is solid coral instead of outline (text-stroke looked broken
    with phone system fonts); desktop outline letter-spacing loosened to -0.02em so outlines no longer overlap.
  - 2026-11-11 Phone menu wraps onto two lines (no sideways scrolling, all items visible); header shrinks below 380px.
    Both mobile fixes pushed 2026-11-11 (user OK); user checks on their phone.
  - 2026-11-11 Phone: hero photo credit moved from top right (over the face) to bottom right, above the text.
  - 2026-11-11 Biography: all paragraphs same size/colour (first paragraph was a larger intro). 
  - 2026-11-11 English page rewritten less literally on the user's request (hero, quote "Humour, brains and footnotes",
    bio, facts, books intro, topics intro + all 5 topics). User then tweaked: quote "Humour, brains and footnotes", "Yet adrenaline…",
    "better to lose your composure than your ability to respond", "…in a clash of 8 billion".
  - 2026-11-11 Phone menu back to one scrollable row (user: wrapping didn't fit at a glance either), now with edge fade
    and coral arrow buttons (js/site.js wraps .nav in .nav-wrap, toggles .more-left/.more-right).
  - Pushed 2026-11-11 (user OK): caption fix, bio size fix, English rewrite + tweaks, phone menu arrows.
  - 2026-11-11 Translation review (subagent; report only) applied with the user's OK: hero restores "brain and hormone
    researcher … (Rowohlt)"; "Book her for"; "short talk(s)" instead of "impulse talk"; prize-money phrase removed;
    Overton window; English city names in event titles (CITIES in build_en.py); WORDS "Science Slam" → "Science slam";
    ~15 wording fixes in topics/bio/cards/lead teasers. Book title now ends with "?" in bio + fact box on BOTH pages.
    Pushed 2026-11-11 (commit d769b61, user OK), live. (ec997e9 sat queued ~1 h during a GitHub Actions/Pages outage, then deployed by itself.)
  - 2026-11-12 Formats strip: "Zu erleben bei" / "Book her for" label removed on both pages (.strip-label CSS removed).
    Phones (≤860px): the formats are one row that scrolls sideways (full width, faded edges, hidden scrollbar).
    Pushed 2026-11-12 (user OK).
  - 2026-11-12 Vortragsthemen reordered on both pages (user): 01 Das soziale Gehirn, 02 Resilienz, 03 KI und Gehirn,
    04 Arbeit und Motivation, 05 Digitalisierung. Pushed 2026-11-12 (user OK).
  - 2026-11-12 English bio: qualifiers "including" (Max Planck) and "roughly:" (book title gloss) removed (user).
    Pushed 2026-11-12 (user OK).
  - 2026-11-12 English bio: translation sentence now "Her books have been translated from South Korea to France." (user's wording).
    Pushed 2026-11-12 (user OK).
  - 2026-11-12 English hero intro: "bestselling author (Rowohlt)" → "bestselling author at Rowohlt publishing house" (user).
    JSON-LD description still says "(Rowohlt)". Pushed 2026-11-12 (user OK).
  - 2026-11-12 English page edits (user): "master’s degree in neuroscience"; new Max Planck / science slam sentence;
    "Berlin-based creator"; books intro now "About humans’ extraordinary social abilities… Available in Russian, French,
    Polish and Korean." German page not changed. Pushed 2026-11-12 (user OK).
  - 2026-11-12 Phone first screen calmer (user: "cramped, lots of bright orange"): on ≤860px the header "Anfrage senden"
    is an outline button, DE/EN active = off-white, menu arrow = plain white chevron, hero eyebrow off-white without the
    pulsing dot. Only the surname and the big hero CTA stay coral. Desktop unchanged. CSS block at the end of
    site-style.css. Pushed 2026-11-12 (user OK).
  - 2026-11-12 Phone hero buttons: "Anfrage senden" and "Zu den Büchern" both left-aligned (icon + text at the same
    spot; arrow stays right). Was: one left, one centred. Committed locally, NOT pushed yet.
  - Next (after going live, owner's to-dos): Search Console (submit sitemap,
    request indexing), Wikipedia "Weblinks" → parianen.com, speakerinnen.org + agency profiles → parianen.com.

## Decisions (and why)
- **No Bootstrap, jQuery, Font Awesome or Google Fonts on the pages.** System fonts plus inline SVG icons.
  Reasons: no third-party requests (German GDPR issues with Google Fonts and CDNs), faster, nothing to break.
  `vendor/`, `gulpfile.js` and `package.json` are leftovers from the old template and are now unused by the pages.
- **No hotlinked logos.** The old cards hotlinked images from ZDF, Wikipedia, Twitter and others (some broken, one was a
  Google redirect URL). They are now text entries (outlet, title, short description).
- **Bio text kept as written**, except fixing "Mes hormone, et moi" to «Mes hormones et moi» (please verify the real French title).
- Entries without a real link (old `href="#"`) are shown as plain text, not links.
- **Impressum legal text unchanged**, only reformatted.
- Left untouched: `blogAlt.html`, `blog_content/`, `testEditor.html`, `banner.jpg`, unused images.

## Open points for the user (not done, needs their input)
1. (Fixed 2026-11-10: first book is 2015, the "(2017)" removed.) Bio still dated: "Zur Zeit … (ET Feb. 2023)" / "aktuellen Essay" read as old.
2. Impressum: still cites TMG/RStV (replaced by DDG/MStV in 2024) and has Google Analytics/AdSense paragraphs although
   the site uses neither. Legal wording should be reviewed by the owner.
3. Add newer appearances, books and texts since 2023 (the newest entries are from 2022/2023).
4. (Done 2026-11-10: X/Twitter replaced by Bluesky + Mastodon icons, see history.)
5. SEO steps only the owner can do after going live: add the site to Google Search Console and submit `sitemap.xml`;
   put parianen.com in the bio/link of Instagram, X, Rowohlt author page, Wikipedia etc. (backlinks matter most).
6. (Done: CNAME rewritten to parianen.com.)

## Status / next step
- Redesign + SEO finished, checked with headless-Chrome screenshots, and **pushed to main on 2026-11-10 (commit b181dbe, live)**.
- torial Texte update, Vorträge/logos rework and domain switch to parianen.com: pushed 2026-11-10 (user OK).
- parianen.com DNS confirmed (A x4 + www CNAME). Waiting on the user: Enforce HTTPS in Settings → Pages, lingua-franca.eu 301 forward, name of the second domain.
- Next: the user answers the open points above (bio update, Impressum review, newer entries).

## How to preview
- Open `index.html` directly in a browser (no build step), or run `python -m http.server 8000` in the project folder.
- Screenshots: `"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --window-size=1440,5000 --screenshot=out.png file:///C:/Users/D/Desktop/linguafranca/index.html`
- Gotcha: headless Chrome will not lay out narrower than about 500px. For a true mobile check, put the page in a 390px-wide `<iframe>` and screenshot that.

## Publish
`git add -A && git commit -m "..." && git push origin main`. GitHub Pages deploys automatically.
