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
  except herCAREER. Psychologie Heute book review (Nov 2020) and Hamburger Abendblatt interview (30 Mar 2021) added on the user's request. Skipped: NDR Science-Slam podcast (404), Frankfurter Zukunftskongress
  newsroom interview (domain now someone else's), Sheconomy (reprint of the herCAREER interview), Dlf Kultur pieces (her own
  commentaries, not interviews). Local only, waiting for OK to push.

- 2026-11-10 Timmy (Ernst Deutsch Theater, Hamburg): user asked to add the nachtkritik review under Presse and under Talks with an Ernst Deutsch Theater icon. Vorträge: "11. Jul 2026 · Podium" (panel after the premiere of „Timmy – Die Hope stirbt zuletzt“), logo images/logos/ernst-deutsch-theater.svg (the theatre's wordmark from its site), linked to the nachtkritik review because the theatre's event page no longer lists the July panel. Fernsehen & Presse: nachtkritik.de review (Jul 2026), logo images/logos/nachtkritik.svg (their logo2019.svg, white fill changed to #1a1a1a so it shows on the light tile). Both logos in tools/fetch_logos.py. The Hamburger Abendblatt review (Hannah Mahé Crüsemann, 14 Jul 2026; the user remembers her called „extrem erhellend und angenehm“ there) could not be opened (abendblatt.de blocks the tools, paywall): add it once the user has the link. Local only, waiting for OK to push.

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
