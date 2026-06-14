# YY Gallery — Project Overview

## What is this?

**YY Gallery** is a small, cheerful static website that showcases the artwork of a
young girl artist. It is a personal, blog-style site whose two goals are simple:

1. **Gallery** — a friendly grid of her artworks. Visitors can glance over the
   pictures and read a short introduction for each piece (title, when it was made,
   what it is, and a sentence or two about it).
2. **About the artist** — a warm introduction to the little artist herself: who she
   is, what she loves to draw, and how her art journey is going.

The tone and visual theme are made **for a child**: soft pastel colours, playful
rounded shapes, a gentle and whimsical feel — bright and welcoming, never busy or
corporate. It should feel like flipping through a happy picture book.

The site is intentionally **kept simple**. For now it is just a place to share
artwork, hosted for free on **GitHub Pages**. Real artwork images and the artist's
introduction will be supplied later; the structure below is built so that adding a
new artwork is as easy as dropping in a picture and adding a few lines of text.

---

## Guiding principles

- **Simple over clever.** No heavy frameworks or build tooling at this stage — plain
  HTML, CSS, and a little JavaScript that runs directly in the browser.
- **Easy to add artwork.** New pieces are added by placing an image in a folder and
  adding one entry to a data file. No coding required to publish a new picture.
- **Child-friendly and kind.** Colours, fonts, and language all suit a young artist
  and a general audience.
- **Fast and free to host.** Static files only, served by GitHub Pages.
- **Room to grow.** The layout leaves clear places to add features later (see the
  Roadmap) without a rewrite.

---

## Directory structure

The tree below is the **target** layout. Folders/files are created as the relevant
roadmap stage is reached — not all of it exists on day one.

```text
yygallery/
├── index.html              # Home / landing page (welcome + a few featured pieces)
├── gallery.html            # Gallery page: grid of all artworks
├── about.html              # About the artist page
├── 404.html                # Friendly "page not found" page
│
├── assets/
│   ├── css/
│   │   └── style.css       # All site styling + the pastel theme (one stylesheet)
│   ├── js/
│   │   ├── main.js         # Shared behaviour (navigation, footer year, etc.)
│   │   └── gallery.js      # Loads artwork data, builds the grid, opens the lightbox
│   ├── images/
│   │   ├── artworks/       # Full-size artwork images (the originals to display)
│   │   │   └── thumbs/     # Smaller thumbnail versions for fast grid loading
│   │   └── site/           # Logo, favicon, artist photo, decorative doodles
│   └── fonts/              # (Optional) playful web font files, if self-hosted
│
├── data/
│   └── artworks.json       # The list of artworks: title, date, medium, description, image paths
│
├── documents/
│   ├── overview.md         # This file — project intro, plan, and roadmap
│   └── tech.md             # Technical decisions and how things are built
│
├── .nojekyll               # Tells GitHub Pages to serve files as-is (skip Jekyll)
└── README.md               # Short repo intro + how to run/preview locally
```

### Purpose of each part

| Path | Purpose |
| --- | --- |
| `index.html` | The front door. A warm welcome, the artist's name, and a small selection of featured artworks that link into the gallery. |
| `gallery.html` | The heart of the site. Shows every artwork as a grid of cards; clicking one opens a larger view with its description. |
| `about.html` | Tells the visitor about the young artist in a friendly way. |
| `404.html` | A gentle, on-theme page shown if someone follows a broken link. |
| `assets/css/style.css` | A single stylesheet holding the colour theme, fonts, layout, and responsive (mobile-friendly) rules. |
| `assets/js/main.js` | Tiny shared scripts used on every page (e.g. mobile menu, current year in footer). |
| `assets/js/gallery.js` | Reads `data/artworks.json` and renders the gallery grid + the click-to-enlarge lightbox. |
| `assets/images/artworks/` | Where the actual artwork pictures live. |
| `assets/images/artworks/thumbs/` | Smaller copies of the artworks so the gallery loads quickly. |
| `assets/images/site/` | Branding and decoration: logo, favicon, the artist's photo, doodle accents. |
| `data/artworks.json` | The single source of truth for the gallery. To add art, add an entry here. |
| `documents/` | Planning and technical notes (not part of the published site). |
| `.nojekyll` | Prevents GitHub Pages from running Jekyll, so our plain files are served untouched. |
| `README.md` | Quick orientation for anyone opening the repo, plus how to preview locally. |

---

## How adding an artwork works

This is the everyday workflow once the site is live:

1. Save the picture into `assets/images/artworks/` (and a small thumbnail into
   `assets/images/artworks/thumbs/`).
2. Add one entry to `data/artworks.json`, for example:

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

3. Commit and push. GitHub Pages republishes automatically — the new artwork appears
   in the gallery. No code changes needed.

---

## Roadmap

Each stage produces something visible and shippable. We can stop at any stage and
still have a working site.

### Stage 0 — Foundations ✅ (planning)
- Write `overview.md` and `tech.md` (this work).
- Create the repository structure and a `README.md`.
- Add a minimal `index.html` and enable **GitHub Pages** to confirm hosting works
  ("hello world" deploy).

### Stage 1 — Core site (MVP)
- Build the three pages: **Home**, **Gallery**, **About**.
- Create the pastel child-friendly theme in `style.css` (colours, fonts, layout).
- Make the gallery render from `data/artworks.json` using 3–5 **placeholder** images.
- Ensure the layout is responsive (looks good on phone, tablet, and desktop).

### Stage 2 — Real content
- Replace placeholders with the **real artwork images** provided by the user.
- Add the **artist's introduction** to the About page and a profile photo.
- Add a favicon, page titles, and basic social/preview meta tags.
- Optimise images (resize, generate thumbnails) so pages load fast.

### Stage 3 — Polish & UX
- Click-to-enlarge **lightbox** with the artwork's description.
- Optional **sorting/filtering** (e.g. newest first, or by category/medium).
- Gentle animations and nice loading/empty states.
- Accessibility pass (alt text, keyboard navigation, colour contrast).

### Stage 4 — Future / nice-to-haves
- A simple **journal/blog** of new artwork posts, if desired.
- **Custom domain** instead of the default `github.io` address.
- Share buttons / "favourite" pieces highlighted on the home page.
- Revisit tooling **only if** content grows enough to need it (e.g. a lightweight
  static site generator) — see `tech.md`.

---

## Future ideas (beyond the roadmap)

For now this stays a simple, safe, **static** showcase for a child's artwork — no
backend, no logins, no data collection. The following are **not part of the current
plan**, but are parked here as things we could explore later if the site grows:

- User accounts or a visitor guestbook / comments.
- A backend or database (e.g. to manage artworks through an admin page).
- A built-in journal/blog of new artwork posts.
- Selling prints or commissions.

When we do reach for more sophisticated, dynamic features like these, the back-end
work would most likely be done in **Python** (the maintainer's stronger language) —
see `tech.md` for how that fits alongside the static front-end.
