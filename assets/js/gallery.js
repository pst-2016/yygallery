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
  const featuredIds = (grid.dataset.featured || "")
    .split(",")
    .map((id) => id.trim())
    .filter(Boolean);
  const siteTimeZone = "Asia/Singapore";
  const datePartsPattern = /^(\d{4})-(\d{2})-(\d{2})$/;

  // ---- Helpers ----------------------------------------------------------
  const formatDate = (iso) => {
    if (!iso) return "";
    const value = String(iso);
    const dateParts = datePartsPattern.exec(value);
    const d = dateParts
      ? new Date(Date.UTC(
          Number(dateParts[1]),
          Number(dateParts[2]) - 1,
          Number(dateParts[3])
        ))
      : new Date(value);

    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleDateString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric",
      timeZone: siteTimeZone,
    });
  };

  const metaLine = (art) =>
    [art.medium, formatDate(art.date)].filter(Boolean).join(" · ");

  const setStatus = (message) => {
    const status = document.createElement("p");
    status.className = "gallery-status";
    status.textContent = message;
    grid.replaceChildren(status);
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
    root.setAttribute("aria-labelledby", "lightbox-title");
    root.setAttribute("aria-describedby", "lightbox-description");
    root.innerHTML = `
      <div class="lightbox__panel">
        <button class="lightbox__close" type="button" aria-label="Close">&times;</button>
        <img class="lightbox__img" alt="" />
        <div class="lightbox__body">
          <h2 class="lightbox__title" id="lightbox-title"></h2>
          <p class="lightbox__meta"></p>
          <p class="lightbox__desc" id="lightbox-description"></p>
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
      if (!root.classList.contains("is-open")) return;

      if (e.key === "Escape") {
        close();
        return;
      }

      if (e.key !== "Tab") return;

      const focusableSelector =
        "button, [href], input, select, textarea, [tabindex]:not([tabindex='-1'])";
      const focusable = Array.from(root.querySelectorAll(focusableSelector))
        .filter((el) => !el.disabled);
      if (focusable.length === 0) {
        e.preventDefault();
        return;
      }

      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    });

    els.open = (art) => {
      const imageSrc = art.image || art.thumb || "";
      if (imageSrc) {
        els.img.src = imageSrc;
      } else {
        els.img.removeAttribute("src");
      }
      els.img.alt = art.alt || art.title || "Artwork";
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

    const thumb = document.createElement("img");
    thumb.className = "art-card__thumb";
    thumb.loading = "lazy";
    thumb.alt = art.alt || art.title || "Artwork";
    if (art.thumb || art.image) thumb.src = art.thumb || art.image;

    const body = document.createElement("div");
    body.className = "art-card__body";

    const title = document.createElement("h3");
    title.className = "art-card__title";
    title.textContent = art.title || "Untitled";

    const meta = document.createElement("p");
    meta.className = "art-card__meta";
    meta.textContent = metaLine(art);

    body.append(title, meta);
    card.append(thumb, body);
    card.addEventListener("click", () => {
      lastFocused = card;
      lightbox.open(art);
    });
    return card;
  };

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
      const featured = featuredIds
        .map((id) => items.find((art) => art.id === id))
        .filter(Boolean);
      const fallbackItems = items.filter((art) => !featuredIds.includes(art.id));
      const selectedItems = featured.length > 0 ? featured.concat(fallbackItems) : items;
      const shown = limit > 0 ? selectedItems.slice(0, limit) : selectedItems;

      grid.replaceChildren();
      shown.forEach((art) => grid.appendChild(makeCard(art)));
    })
    .catch((err) => {
      console.error("Could not load artworks:", err);
      setStatus("Sorry, the artworks could not be loaded right now.");
    });
})();
