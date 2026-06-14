# YY Gallery — Technical Notes

This document explains **how** the site is built and **why** these choices were made.
The overarching rule is the same as the project's: **keep it simple**. See
[overview.md](overview.md) for the project plan and roadmap.

---

## 1. Technology choice

### The stack: plain HTML + CSS + a little JavaScript

The site is built with **vanilla web technologies** and **no build step**:

- **HTML** for page structure (a few static pages).
- **CSS** for styling and the child-friendly theme (one stylesheet).
- **Vanilla JavaScript** for the small amount of interactivity (loading the gallery
  data, the click-to-enlarge lightbox, the mobile menu).
- **JSON** as a tiny "database" for artwork details.

### Why not a framework or static site generator?

For a small personal gallery, frameworks (React, Vue) and generators (Jekyll, Hugo,
Astro, Eleventy) add tooling, dependencies, and a build/learning curve that we don't
need yet. Plain files mean:

- Nothing to install or compile — open the file in a browser and it works.
- Anyone can edit content without learning a framework.
- Nothing to break or keep updated; no `node_modules`.
- It deploys to GitHub Pages exactly as written.

This is a one-way-door we have intentionally left **reversible**: the data lives in
`artworks.json` and content is clean HTML, so if the site ever outgrows this approach
we can migrate to a generator (see §10) without throwing work away.

---

## 2. Hosting & deployment — GitHub Pages

- The site is hosted on **GitHub Pages**, serving static files for free.
- Source lives on the default branch; Pages is configured to publish from the repo
  root (Settings → Pages → "Deploy from a branch").
- A **`.nojekyll`** file sits at the repo root so GitHub serves our files as-is and
  does not run Jekyll over them.
- **Deploy flow:** commit → push → GitHub Pages rebuilds automatically. The live URL
  is `https://<username>.github.io/yygallery/` until/unless a custom domain is added.

### Path note (important)

Because the site is served from a sub-path (`/yygallery/`), normal page links and
asset references use **relative paths** (e.g. `assets/css/style.css`, not
`/assets/...`). This keeps the site working both locally and on GitHub Pages without
surprises.

The one current exception is `404.html`, which uses `/yygallery/...` paths. GitHub
Pages can show the same 404 file for missing nested URLs, where ordinary relative
paths would resolve from the wrong folder. If the site moves to a custom domain, this
404 path choice should be revisited.

---

## 3. Page structure (HTML)

- A small number of **standalone HTML pages**: `index.html`, `gallery.html`,
  `about.html`, and `404.html`.
- Each page shares the same simple **header (navigation)** and **footer**. Since the
  site is tiny, this markup is duplicated across pages rather than templated — the
  simplest thing that works. If duplication becomes annoying, §10 covers options.
- HTML is written **semantically** (`<header>`, `<nav>`, `<main>`, `<section>`,
  `<figure>`, `<figcaption>`, `<footer>`) for accessibility and clarity.
- Each page includes proper `<title>` and `<meta>` tags (description, viewport, and
  Open Graph tags for nice link previews when shared).

---

## 4. Styling (CSS) & the theme

One stylesheet: `assets/css/style.css`.

- **CSS custom properties (variables)** define the theme in one place, so colours and
  fonts can be tweaked easily:

  ```css
  :root {
    --color-bg: #fff7fb;        /* soft blush background */
    --color-primary: #ffb3d1;   /* candy pink            */
    --color-accent: #b5ead7;    /* mint                  */
    --color-secondary: #c7ceea; /* lavender              */
    --color-sun: #ffe7a0;       /* soft yellow           */
    --color-text: #4a4a4a;      /* gentle dark grey, not harsh black */
    --radius: 18px;             /* rounded, friendly corners */
    --font-heading: "Baloo 2", "Comic Sans MS", cursive, sans-serif;
    --font-body: "Quicksand", system-ui, sans-serif;
  }
  ```

- **Theme direction:** soft pastels (pink, lavender, mint, soft yellow), generously
  **rounded corners**, playful rounded fonts, gentle shadows, and optional hand-drawn
  doodle accents. Cheerful and storybook-like, never cluttered.
- **Layout:** **mobile-first** and responsive. The gallery uses **CSS Grid**
  (`grid-template-columns: repeat(auto-fill, minmax(...))`) so the number of columns
  adapts to screen size with no JavaScript.
- **No CSS framework** (no Bootstrap/Tailwind) — the site is small enough that custom
  CSS is shorter and fully under our control.

---

## 5. Interactivity (JavaScript)

Kept to a minimum, in two small files:

- **`assets/js/main.js`** — shared, page-wide bits: the mobile navigation toggle and
  inserting the current year in the footer.
- **`assets/js/gallery.js`** — the gallery logic:
  1. `fetch()` the `data/artworks.json` file.
  2. Build a card for each artwork (thumbnail + title) and insert it into the grid.
  3. On click, open a **lightbox** overlay showing the full image plus its details.
  4. Later: optional sorting/filtering controls.

No bundler, no dependencies — these are plain `<script>` files loaded by the pages.

> Note: `fetch()` of the JSON requires the page to be served over HTTP, not opened
> as a `file://` path. See §8 for the one-line local preview server.

---

## 6. Artwork data model

All artwork details live in **`data/artworks.json`** — the single source of truth for
the gallery. It is an array of objects:

```json
[
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
]
```

| Field | Meaning |
| --- | --- |
| `id` | Unique slug; used for links/anchors. Lowercase, hyphenated. |
| `title` | The artwork's name, shown on the card and in the lightbox. |
| `date` | When it was made (`YYYY-MM-DD`); used for display and sorting. |
| `medium` | What it's made with (crayon, watercolour, digital, …). Optional. |
| `image` | Path to the full-size picture. |
| `thumb` | Path to the small thumbnail used in the grid. |
| `alt` | A concise visual description for screen readers. |
| `description` | A sentence or two introducing the piece. |

Keeping data separate from layout means **adding art never requires touching HTML or
JavaScript**.

---

## 7. Images

Images are the most important content, so we handle them with a little care:

- **Formats:** JPG/PNG for photos of physical art. The local import helper accepts
  JPG, PNG, and SVG source files and can write JPG, PNG, or SVG outputs.
- **Two sizes per piece:** a **thumbnail** (grid, ~400px wide) and the **full image**
  (lightbox, e.g. ≤1600px wide). Thumbnails keep the gallery fast.
- **Lazy loading:** grid images use `loading="lazy"` so off-screen pictures load only
  when needed.
- **Alt text:** every artwork entry should include meaningful `alt` text describing
  the image, for accessibility and screen readers.
- **Optimisation:** images are resized/compressed before committing. This can be done
  with `scripts/import_artworks.py`, which uses Pillow and CairoSVG from the conda
  environment to create full-size images and square thumbnails.

---

## 8. Local development & preview

No build tools required. To preview the site with working JSON loading, serve the
folder over HTTP from the repo root:

```bash
# Python (usually preinstalled)
python3 -m http.server 8000
# then open http://localhost:8000

# …or Node, if preferred
npx serve .
```

Opening `index.html` directly via `file://` mostly works but **`fetch()` of the JSON
will be blocked by the browser**, so use a local server when testing the gallery.

---

## 9. Accessibility, performance & SEO

- **Accessibility:** semantic HTML, descriptive `alt` text, keyboard-operable
  lightbox (close with `Esc`, focus handling), and pastel colours checked for
  readable **contrast** against text.
- **Performance:** thumbnails + lazy loading, a single small CSS file, and minimal
  JavaScript keep the site fast even on phones.
- **SEO / sharing:** per-page `<title>` and meta description, plus basic Open Graph
  tags. Preview images can be added in Stage 2 once the real artwork/profile assets
  are chosen.

---

## 10. Future technical options (only if needed)

We adopt these **only** if the simple approach starts to hurt:

- **Reusing the header/footer:** if duplicating navigation across pages becomes
  tedious, introduce a lightweight static site generator (**Eleventy** is a good,
  minimal fit) to share layouts — while keeping the same content and data model.
- **Image pipeline:** extend `scripts/import_artworks.py` if WebP versions, true SVG
  vector tracing, or more advanced image handling are needed later.
- **Custom domain + HTTPS** via GitHub Pages settings.
- **A journal/blog:** Markdown posts compiled to pages (again, Eleventy-friendly).

### Python for sophisticated / dynamic features

The front-end deliberately stays plain static files. **When we eventually want more
sophisticated or dynamic functionality** — for example an admin page to manage
artworks, an image-optimisation pipeline, content generation, or any small back-end
service — that work will most likely be done in **Python**, which is the maintainer's
stronger language. Good fits would be:

- **Helper scripts** (e.g. `scripts/import_artworks.py` using **Pillow**) to resize
  images and regenerate thumbnails and the `artworks.json` entries.
- A small **Flask** or **FastAPI** service, if a real back-end is ever needed.

Crucially, none of this changes the published site today: GitHub Pages would still
serve static output, with Python used as a **local build/automation tool** (or a
separately hosted service) rather than something the visitor's browser runs.

These options are noted so the current simplicity is a **deliberate starting point**,
not a dead end.

---

## 11. Conventions

- **Indentation:** 2 spaces for HTML, CSS, JS, and JSON.
- **Naming:** files and `id`s are `lowercase-with-hyphens`.
- **Paths:** use **relative** paths for normal pages; `404.html` currently uses
  `/yygallery/...` paths for GitHub Pages project-site fallback behaviour.
- **Encoding:** UTF-8; `<meta charset="utf-8">` on every page.
- **Commits:** small and descriptive (e.g. `Add "Rainbow Cat" artwork`).

---

## Summary

| Concern | Choice |
| --- | --- |
| Pages | Plain static HTML |
| Styling | One custom CSS file, pastel child-friendly theme, CSS Grid |
| Interactivity | Vanilla JavaScript (gallery render + lightbox) |
| Data | `data/artworks.json` |
| Build step | **None** |
| Hosting | GitHub Pages (`.nojekyll`, relative paths) |
| Guiding rule | Keep it simple; leave room to grow |
