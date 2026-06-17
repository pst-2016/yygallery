# YY Gallery — Development Routine

This document describes the normal development loop for this static site. It is meant
to keep each change small, easy to preview, and consistent with the roadmap in
`documents/overview.md`.

---

## 1. Before starting a change

1. Read the current roadmap/status in `documents/overview.md`.
2. Check `documents/tech.md` for implementation decisions.
3. Confirm the intended change and the files likely to be touched.
4. Ask for approval before running terminal commands or editing files.

Do not access AWS services, do not inspect `.env` files, and do not run `pip` or
`conda` install commands during this project unless the project rules are changed.

---

## 2. Local preview loop

The site has no build step, but the gallery fetches `data/artworks.json`, so preview
it through a local HTTP server rather than opening HTML files directly.

Create the conda environment once:

```bash
conda env create -f environment.yml
```

When `environment.yml` changes, update the existing environment:

```bash
conda env update -f environment.yml --prune
```

Run the preview from the repository root inside the project conda environment:

```bash
conda activate yygallery
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

Pages to check during the MVP/content stages:

- `http://localhost:8000/index.html`
- `http://localhost:8000/gallery.html`
- `http://localhost:8000/about.html`
- `http://localhost:8000/404.html`

For gallery changes, check that:

- Artwork cards load from `data/artworks.json`.
- Newest artwork appears first.
- Clicking an artwork opens the lightbox.
- The lightbox closes with the close button, backdrop click, and `Esc`.
- Images, titles, dates, medium text, descriptions, and `alt` text match the data.
- Mobile navigation opens and closes on a narrow viewport.

---

## 3. GitHub Pages check

After committing and pushing to the branch configured for GitHub Pages, wait for the
Pages deployment to finish. Then check the project URL:

```text
https://<username>.github.io/yygallery/
```

Check the same pages:

- `https://<username>.github.io/yygallery/index.html`
- `https://<username>.github.io/yygallery/gallery.html`
- `https://<username>.github.io/yygallery/about.html`
- `https://<username>.github.io/yygallery/404.html`

Also check a deliberately missing URL, such as:

```text
https://<username>.github.io/yygallery/not-a-real-page
```

The current `404.html` uses `/yygallery/...` paths so its CSS and home link work for
the GitHub Pages project URL. Revisit this if the site moves to a custom domain.

---

## 4. Feedback loop

1. The user previews locally or on GitHub Pages.
2. The user sends feedback with the page name, what they expected, and what they saw.
3. Update the smallest useful set of files.
4. Re-run the local preview checks.
5. At the end of each roadmap phase, review docs and code together so
   `overview.md`, `tech.md`, `README.md`, and the site remain consistent.

For Stage 2 content updates, keep the artwork workflow simple.

### Artwork Upload Workflow

1. Create `incoming/artworks/` if it does not exist.
2. Put source artwork images into `incoming/artworks/`.
3. Add missing image rows to `incoming/artworks/artworks.csv`:

   ```bash
   python scripts/import_artworks.py incoming/artworks --update-manifest
   ```

4. Edit `incoming/artworks/artworks.csv` with captions and metadata:

   - `title`: artwork title shown on cards and in the lightbox.
   - `date`: `YYYY-MM-DD` if known; leave blank if uncertain.
   - `medium`: e.g. `Pencil sketch`, `Watercolour`, `Oil painting`.
   - `description`: caption shown in the lightbox.
   - `alt`: concise visual description for screen readers.

5. Import the images into the site:

   ```bash
   python scripts/import_artworks.py incoming/artworks
   ```

6. Review `data/artworks.json` and the generated files under
   `assets/images/artworks/` and `assets/images/artworks/thumbs/`.
7. Update the home page featured artwork IDs in `index.html` if needed.
8. Update page titles, meta descriptions, favicon, and About page content as needed.

The import helper accepts JPG, PNG, and SVG source images. It writes JPG files by
default. To choose another output format, pass `--format jpg`, `--format png`, or
`--format svg`:

```bash
python scripts/import_artworks.py incoming/artworks --format png
```

SVG output is an SVG wrapper around a resized embedded image. It is not true vector
tracing.

The optional CSV uses this header:

```csv
filename,id,title,date,medium,description,alt
what-hides-in-the-dark.jpg,what-hides-in-the-dark,What Hides in the Dark,2026-05-01,Oil painting,An atmospheric painting about what might be hiding in darkness.,A dark atmospheric artwork with hidden shapes and dramatic contrast.
```

If the CSV is missing, the import script still works: it creates a title and `id`
from each filename and leaves optional text fields blank for later editing.
