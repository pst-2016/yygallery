/* main.js — tiny shared behaviour used on every page. */

document.addEventListener("DOMContentLoaded", () => {
  // Current year in the footer.
  const yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Mobile navigation toggle.
  const toggle = document.querySelector(".nav-toggle");
  const navList = document.querySelector(".nav-list");
  if (toggle && navList) {
    toggle.addEventListener("click", () => {
      const open = navList.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
    });
  }
});
