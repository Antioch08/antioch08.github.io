# Daniel J Lewis · Portfolio

Live at https://antioch08.github.io

## How it's built
- All copy and project data lives in `_src/content.json`; gallery images per page are in `_src/gallery.json`.
- Run `python3 _src/build.py` to regenerate `index.html` and the project pages.
- Images live in `assets/img` (WebP), PDFs in `assets/docs`.
- Playable prototypes go in `play/<name>/index.html` and get an entry in `content.json → play.items`.
