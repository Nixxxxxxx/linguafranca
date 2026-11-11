# Project instructions

Read `TASKS.md` first: it has the history, decisions, open questions and next step.

Standing rules:
- Static site, no build step. Keep pages free of third-party requests (no CDNs, Google Fonts or hotlinked images) for GDPR reasons.
- Site language is German, with an English version at `en/index.html`. Any change to German page text must also be
  made in `en/index.html` (the Vorträge/Presse and Texte lists sync automatically via `tools/build_en.py`).
- `main` deploys live via GitHub Pages. Do not push without the user's OK.
- Do not change the Impressum's legal wording without the user asking.
