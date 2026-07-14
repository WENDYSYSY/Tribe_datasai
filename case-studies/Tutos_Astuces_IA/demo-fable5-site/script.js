/* Abyssale landing — interactions (vanilla JS, no dependencies) */
(function () {
  "use strict";

  /* ---------- Mobile navigation ---------- */
  const header = document.querySelector(".site-header");
  const burger = document.querySelector(".hamburger");

  burger.addEventListener("click", () => {
    const open = header.classList.toggle("nav-open");
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  });

  /* ---------- Dropdown menus (click + keyboard; hover handled in CSS) ---------- */
  const dropdownItems = Array.from(document.querySelectorAll(".has-dropdown"));

  function closeAllDropdowns(except) {
    dropdownItems.forEach((item) => {
      if (item !== except) {
        item.classList.remove("open");
        item.querySelector(".nav-link").setAttribute("aria-expanded", "false");
      }
    });
  }

  dropdownItems.forEach((item) => {
    const trigger = item.querySelector(".nav-link");
    trigger.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = item.classList.toggle("open");
      trigger.setAttribute("aria-expanded", String(open));
      closeAllDropdowns(item);
    });
  });

  document.addEventListener("click", () => closeAllDropdowns(null));
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeAllDropdowns(null);
      if (header.classList.contains("nav-open")) burger.click();
    }
  });

  /* ---------- Studio banner carousel ---------- */
  const slides = Array.from(document.querySelectorAll(".studio-slide"));
  const dots = Array.from(document.querySelectorAll(".studio-dots .dot"));
  let current = 0;

  function showSlide(index) {
    current = (index + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle("is-active", i === current));
    dots.forEach((d, i) => {
      d.classList.toggle("is-active", i === current);
      d.setAttribute("aria-selected", String(i === current));
    });
  }

  document.querySelector(".studio-arrow.prev").addEventListener("click", () => showSlide(current - 1));
  document.querySelector(".studio-arrow.next").addEventListener("click", () => showSlide(current + 1));
  dots.forEach((dot, i) => dot.addEventListener("click", () => showSlide(i)));

  /* ---------- Sidebar category filter ---------- */
  const catButtons = Array.from(document.querySelectorAll(".cat"));
  const cards = Array.from(document.querySelectorAll(".tpl"));
  const emptyMsg = document.getElementById("grid-empty");

  catButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      catButtons.forEach((b) => b.classList.remove("is-active"));
      btn.classList.add("is-active");
      const cat = btn.dataset.cat;
      let visible = 0;
      cards.forEach((card) => {
        const show = cat === "all" || card.dataset.cat === cat || card.dataset.cat === "all";
        card.hidden = !show;
        if (show) visible++;
      });
      emptyMsg.hidden = visible > 1; /* the "scratch" card is always shown */
    });
  });

  /* ---------- Scroll reveal ---------- */
  const revealables = Array.from(document.querySelectorAll("[data-reveal]"));
  const inInitialViewport = (el) => {
    const r = el.getBoundingClientRect();
    return r.top < window.innerHeight * 0.9 && r.bottom > 0;
  };
  const io =
    "IntersectionObserver" in window
      ? new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                io.unobserve(entry.target);
              }
            });
          },
          { threshold: 0.12 }
        )
      : null;
  revealables.forEach((el) => {
    /* Above-the-fold content must never wait for the observer */
    if (!io || inInitialViewport(el)) {
      el.classList.add("is-visible");
    } else {
      io.observe(el);
    }
  });

  /* ---------- Modal (sign up / request demo) ---------- */
  const modal = document.getElementById("modal");
  const modalTitle = document.getElementById("modal-title");
  const form = document.getElementById("modal-form");
  const successMsg = form.querySelector(".modal-success");

  document.querySelectorAll("[data-open-modal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      modalTitle.textContent = btn.hasAttribute("data-demo") ? "Request a demo" : "Create your account";
      successMsg.hidden = true;
      form.reset();
      form.querySelectorAll(".field").forEach((f) => f.classList.remove("invalid"));
      form.querySelectorAll(".field-error").forEach((el) => (el.textContent = ""));
      modal.showModal();
    });
  });

  modal.querySelector(".modal-close").addEventListener("click", () => modal.close());
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.close(); /* click on backdrop */
  });

  /* ---------- Client-side validation ---------- */
  function setError(input, message) {
    const field = input.closest(".field");
    field.classList.toggle("invalid", Boolean(message));
    field.querySelector(".field-error").textContent = message || "";
  }

  const nameInput = document.getElementById("f-name");
  const emailInput = document.getElementById("f-email");
  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  function validate() {
    let ok = true;
    if (!nameInput.value.trim()) {
      setError(nameInput, "Please enter your name.");
      ok = false;
    } else {
      setError(nameInput, "");
    }
    if (!emailInput.value.trim()) {
      setError(emailInput, "Please enter your e-mail address.");
      ok = false;
    } else if (!emailRe.test(emailInput.value.trim())) {
      setError(emailInput, "This e-mail address looks invalid.");
      ok = false;
    } else {
      setError(emailInput, "");
    }
    return ok;
  }

  [nameInput, emailInput].forEach((input) => {
    input.addEventListener("input", () => {
      if (input.closest(".field").classList.contains("invalid")) validate();
    });
  });

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!validate()) return;
    successMsg.hidden = false;
    setTimeout(() => modal.close(), 1600);
  });
})();
