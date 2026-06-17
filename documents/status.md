# YY Gallery Status

## Current State

- Static GitHub Pages art gallery using plain HTML/CSS/JS and `data/artworks.json`.
- Stage 0 and Stage 1 are complete; Stage 2 real content is in progress.
- Real biography has been added to `about.html`.
- Gallery data has been imported from `incoming/artworks/artworks.csv` into
  `data/artworks.json`.
- Dummy placeholder artworks have been removed from `data/artworks.json`.
- Home featured artworks are configured in `index.html` using `data-featured`.
- `incoming/` is intentionally ignored by git and is only for local staging.

## Local Tools

- Conda env file: `environment.yml`.
- Import helper: `scripts/import_artworks.py`.
- Main workflow:
  1. Put new images in `incoming/artworks/`.
  2. Run `python scripts/import_artworks.py incoming/artworks --update-manifest`.
  3. Edit `incoming/artworks/artworks.csv`.
  4. Run `python scripts/import_artworks.py incoming/artworks`.
  5. Commit generated files under `assets/images/artworks/`, thumbnails, and
     `data/artworks.json`.

## Important Notes

- GitHub Pages does not run Python. All image import/thumbnail generation must happen
  locally before committing.
- Site favicon references expect `assets/images/site/favicon.jpg`.
- Artist photo reference expects `assets/images/site/artist_photo.jpg`.
- `404.html` intentionally uses `/yygallery/...` paths for GitHub Pages project URL.
- Project rules require confirmation before running commands or editing files.

## Likely Next Steps

- Verify all generated artwork images and thumbnails are committed.
- Confirm whether to add the `favicon` artwork as a fourth featured item on home.
- Preview locally with `python3 -m http.server 8000`.
- Commit and push to `main`, then check GitHub Pages deployment status.
