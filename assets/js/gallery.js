/* gallery.js
   Loads artwork data from data/artworks.json and renders it into any element
   marked with [data-gallery]. Optionally limit the count with data-limit
   (used on the home page to show only a few featured pieces).
   Clicking a card opens an accessible lightbox with the full image + details.
*/

(() => {
  const grid = document.querySelector("[data-gallery]");
  if (!grid) return; // page has no gallery

  const limit = parseInt(grid.dataset.limit || "0", 10); // 0 = show all
  const dataUrl = grid.dataset.src || "data/artworks.json";

  // ---- Helpers ----------------------------------------------------------
  const formatDate = (iso) => {
    if (!iso) return "";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const metaLine = (art) =>
    [art.medium, formatDate(art.date)].filter(Boolean).join(" · ");

  const setStatus = (message) => {
    grid.innerHTML = `<p class="gallery-status">${message}</p>`;
  };

  // ---- Lightbox (built once, reused) ------------------------------------
  let lastFocused = null;
  const lightbox = buildLightbox();
  document.body.appendChild(lightbox.root);

  function buildLightbox() {
    const root = document.createElement("div");
    root.className = "lightbox";
    root.setAttribute("role", "dialog");
    root.setAttribute("aria-modal", "true");
    root.setAttribute("aria-hidden", "true");
    root.innerHTML = `
      <div class="lightbox__panel">
        <button class="lightbox__close" type="button" aria-label="Close">&times;</button>
        <img class="lightbox__img" alt="" />
        <div class="lightbox__body">
          <h2 class="lightbox__title"></h2>
          <p class="lightbox__meta"></p>
          <p class="lightbox__desc"></p>
        </div>
      </div>`;

    const els = {
      root,
      img: root.querySelector(".lightbox__img"),
      title: root.querySelector(".lightbox__title"),
      meta: root.querySelector(".lightbox__meta"),
      desc: root.querySelector(".lightbox__desc"),
      close: root.querySelector(".lightbox__close"),
    };

    const close = () => {
      root.classList.remove("is-open");
      root.setAttribute("aria-hidden", "true");
      if (lastFocused) lastFocused.focus();
    };

    els.close.addEventListener("click", close);
    root.addEventListener("click", (e) => {
      if (e.target === root) close(); // click on backdrop
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && root.classList.contains("is-open")) close();
    });

    els.open = (art) => {
      els.img.src = art.image || art.thumb || "";
      els.img.alt = art.title || "Artwork";
      els.title.textContent = art.title || "Untitled";
      els.meta.textContent = metaLine(art);
      els.desc.textContent = art.description || "";
      root.classList.add("is-open");
      root.setAttribute("aria-hidden", "false");
      els.close.focus();
    };

    return els;
  }

  // ---- Card rendering ---------------------------------------------------
  const makeCard = (art) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "art-card";
    card.innerHTML = `
      <img class="art-card__thumb" loading="lazy"
           src="${art.thumb || art.image}" alt="${escapeHtml(art.title || "Artwork")}" />
      <div class="art-card__body">
        <h3 class="art-card__title">${escapeHtml(art.title || "Untitled")}</h3>
        <p class="art-card__meta">${escapeHtml(metaLine(art))}</p>
      </div>`;
    card.addEventListener("click", () => {
      lastFocused = card;
      lightbox.open(art);
    });
    return card;
  };

  const escapeHtml = (str) =>
    String(str).replace(/[&<>"']/g, (c) => (
      { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
    ));

  // ---- Load + render ----------------------------------------------------
  setStatus("Loading artworks…");

  fetch(dataUrl)
    .then((res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then((items) => {
      if (!Array.isArray(items) || items.length === 0) {
        setStatus("No artworks yet — check back soon! 🎨");
        return;
      }
      // Newest first.
      items.sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));
      const shown = limit > 0 ? items.slice(0, limit) : items;

      grid.innerHTML = "";
      shown.forEach((art) => grid.appendChild(makeCard(art)));
    })
    .catch((err) => {
      console.error("Could not load artworks:", err);
      setStatus("Sorry, the artworks could not be loaded right now.");
    });
})();
