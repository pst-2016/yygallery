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
root run any one of these, then open the printed address:

```bash
python3 -m http.server 8000      # then visit http://localhost:8000
# or
npx serve .
```

## Adding a new artwork

1. Put the picture in `assets/images/artworks/` (and a smaller copy in
   `assets/images/artworks/thumbs/`).
2. Add one entry to [`data/artworks.json`](data/artworks.json):

   ```json
   {
     "id": "rainbow-cat",
     "title": "Rainbow Cat",
     "date": "2026-05-01",
     "medium": "Watercolour on paper",
     "image": "assets/images/artworks/rainbow-cat.jpg",
     "thumb": "assets/images/artworks/thumbs/rainbow-cat.jpg",
     "description": "A happy cat sitting under a big rainbow."
   }
   ```

3. Commit and push — GitHub Pages republishes automatically.

## Deploying (GitHub Pages)

Push to the default branch, then in the repo **Settings → Pages** choose
*Deploy from a branch* and select the branch + root folder. The site appears at
`https://<username>.github.io/yygallery/`.
