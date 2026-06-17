# 🎨 YY Gallery

A small, cheerful website that shares the artwork of a young artist.
It is a simple, static, blog-style gallery — built with plain HTML, CSS, and a little
JavaScript — hosted for free on **GitHub Pages**.

- **Home** — a warm welcome and a few featured pieces.
- **Gallery** — every artwork in a friendly grid; click a piece to see it bigger.
- **About** — an introduction to the young artist.

See [`documents/overview.md`](documents/overview.md) for the full project plan and
roadmap, and [`documents/tech.md`](documents/tech.md) for the technical details.

## Preview it locally

The gallery loads its data from a JSON file, so the site needs to be served over HTTP
(opening the HTML file directly with `file://` will block that load). From the repo
root run:

```bash
conda activate yygallery
python3 -m http.server 8000      # then visit http://localhost:8000
```

## Adding a new artwork

The easiest workflow is to use the local import helper:

1. Create `incoming/artworks/` if it does not exist.
2. Put source images in `incoming/artworks/`.
3. Add missing CSV rows:

   ```bash
   conda activate yygallery
   python scripts/import_artworks.py incoming/artworks --update-manifest
   ```

4. Edit `incoming/artworks/artworks.csv` with captions and metadata.
5. Import:

   ```bash
   conda activate yygallery
   python scripts/import_artworks.py incoming/artworks
   ```

By default, the script writes JPG files. To choose another output format, use
`--format jpg`, `--format png`, or `--format svg`:

```bash
python scripts/import_artworks.py incoming/artworks --format png
```

Supported source formats are JPG, PNG, and SVG. SVG output is an SVG wrapper around
a resized embedded image; it is not true vector tracing.

The script writes full images to `assets/images/artworks/`, creates thumbnails in
`assets/images/artworks/thumbs/`, and updates [`data/artworks.json`](data/artworks.json).

You can also edit [`data/artworks.json`](data/artworks.json) manually. Each entry
looks like this:

```json
{
  "id": "rainbow-cat",
  "title": "Rainbow Cat",
  "date": "2026-05-01",
  "medium": "Watercolour on paper",
  "image": "assets/images/artworks/rainbow-cat.jpg",
  "thumb": "assets/images/artworks/thumbs/rainbow-cat.jpg",
  "alt": "A watercolour painting of a happy cat sitting under a big rainbow.",
  "description": "A happy cat sitting under a big rainbow."
}
```

Commit and push — GitHub Pages republishes automatically.

## Updating the conda environment

Create the environment once:

```bash
conda env create -f environment.yml
```

After `environment.yml` changes, update the existing environment:

```bash
conda env update -f environment.yml --prune
```

## Deploying (GitHub Pages)

Push to the default branch, then in the repo **Settings → Pages** choose
*Deploy from a branch* and select the branch + root folder. The site appears at
`https://<username>.github.io/yygallery/`.
