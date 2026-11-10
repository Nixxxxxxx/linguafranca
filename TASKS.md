# lingua-franca.eu: handover

## What this is
Personal website of Dr. Franca Parianen (neuroscientist, author, speaker). Static site hosted on
GitHub Pages from `main` of https://github.com/Nixxxxxxx/linguafranca (custom domain via `CNAME`:
lingua-franca.eu). **Pushing to `main` publishes the live site.**

## History
- **2026-11-10**: User asked: "make the website more professional." Full redesign done (uncommitted at time of writing):
  - Replaced the jQuery `.load()` fragment site (bright teal, hover-zoom cards, blurred "past" cards,
    typewriter effect) with a single static one-page site: `index.html` with sections
    Über mich / Bücher / Vorträge & Medien / Texte / Kontakt, plus a standalone `impressum.html`.
  - New hand-written `css/site-style.css`: off-white background, deep teal accent (#0f4c45), serif headings.
  - Removed `main_content.html`, `termine.html`, `blog.html`, `contact.html` (their content now lives in `index.html`; old versions in git history).
  - The old 2022 "Demnächst" events were moved into the speaking list with their dates, so the site no longer shows out-of-date "upcoming" events.

- **2026-11-10 (later)**: User asked: "update for seo". Done (also uncommitted):
  - `index.html` head: sharper title/description, robots, Open Graph (`og:type=profile`) and Twitter card tags,
    and JSON-LD structured data (WebSite, ProfilePage, Person with sameAs links, and the five books).
  - `images/og-image.jpg` (1200x630 share preview), built by `python tools/make_og_image.py` (re-run if the photo or text changes).
  - Compressed `images/franca.jpg` (248 KB to 51 KB) and `images/buch2.jpg` (247 KB to 50 KB). Hero photo preloaded with `fetchpriority=high`.
  - Added `robots.txt` (blocks the unused test and old blog files), `sitemap.xml` and `404.html`. The Impressum is `noindex, follow`.

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
4. The Twitter link label is "X / Twitter"; consider removing it if the account is no longer active.
5. SEO steps only the owner can do after going live: add the site to Google Search Console and submit `sitemap.xml`;
   put lingua-franca.eu in the bio/link of Instagram, X, Rowohlt author page, Wikipedia etc. (backlinks matter most).
6. `CNAME` line 2 has a typo (`wwww.`). GitHub Pages only reads line 1, so it is harmless, but it could be removed.

## Status / next step
- Redesign + SEO finished and checked with headless-Chrome screenshots (desktop 1440px, mobile 390px). **Not committed or pushed yet:
  waiting for the user's OK** (pushing goes live).

## How to preview
- Open `index.html` directly in a browser (no build step), or run `python -m http.server 8000` in the project folder.
- Screenshots: `"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --window-size=1440,5000 --screenshot=out.png file:///C:/Users/D/Desktop/linguafranca/index.html`
- Gotcha: headless Chrome will not lay out narrower than about 500px. For a true mobile check, put the page in a 390px-wide `<iframe>` and screenshot that.

## Publish
`git add -A && git commit -m "..." && git push origin main`. GitHub Pages deploys automatically.
