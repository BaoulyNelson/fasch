document.addEventListener("DOMContentLoaded", function () {
  // === Mobile menu toggle ===
  const mobileMenuToggle = document.getElementById("mobile-menu-toggle");
  const mobileMenu = document.getElementById("mobile-menu");

  mobileMenuToggle?.addEventListener("click", function () {
    const icon = this.querySelector("i");
    mobileMenu.classList.toggle("hidden");

    if (icon.classList.contains("fa-bars")) {
      icon.classList.remove("fa-bars");
      icon.classList.add("fa-times");
    } else {
      icon.classList.remove("fa-times");
      icon.classList.add("fa-bars");
    }
  });

  // === Mobile search toggle ===
  const searchToggle = document.getElementById("mobile-search-toggle");
  const searchForm = document.getElementById("mobile-search-form");
  const searchInput = document.getElementById("mobile-search-input");

  searchToggle?.addEventListener("click", function () {
    searchForm?.classList.toggle("hidden");
    if (!searchForm.classList.contains("hidden")) {
      searchInput?.focus();
    }
  });

  // === Mobile submenu toggle ===
  const menuItems = document.querySelectorAll(".mobile-nav-item");
  menuItems.forEach((item) => {
    const link = item.querySelector(".mobile-nav-link");
    const icon = item.querySelector(".submenu-toggle-icon");
    const submenu = item.querySelector(".mobile-submenu");

    if (submenu) {
      link?.addEventListener("click", function (e) {
        e.preventDefault();
        submenu.classList.toggle("hidden");
        icon?.classList.toggle("rotated");
      });
    }
  });

  // === Ticker texte défilant ===
  const messages = [
    "Faculté des Sciences Humaines d'Haïti (FASCH)",
    "Former, Rechercher, Innover",
    "Excellence, Éthique, Engagement"
  ];
  const colors = ["darkblue", "green", "crimson"];
  const ticker = document.getElementById("ticker-text");
  let index = 0;

  function showMessage() {
    if (!ticker) return;
    ticker.style.animation = "none";
    void ticker.offsetWidth;

    ticker.textContent = messages[index];
    ticker.style.color = colors[index];
    ticker.style.animation = "scroll-left 10s linear forwards";

    index = (index + 1) % messages.length;
  }

  showMessage();
  setInterval(showMessage, 10000);

  // === Surbrillance du mot recherché (valeur injectée par le template Django) ===
  const query = document.body.getAttribute("data-query")?.toLowerCase();
  if (query) {
    document.querySelectorAll(".result-item").forEach(function (item) {
      let content = item.innerHTML;
      const regex = new RegExp("(" + query + ")", "gi");
      content = content.replace(regex, '<span class="highlight">$1</span>');
      item.innerHTML = content;
    });
  }
});

// === Back to top button ===
const backToTopBtn = document.getElementById("backToTop");

window.addEventListener("scroll", () => {
  if (!backToTopBtn) return;
  if (window.pageYOffset > 300) {
    backToTopBtn.classList.add("visible");
  } else {
    backToTopBtn.classList.remove("visible");
  }
});

backToTopBtn?.addEventListener("click", function (e) {
  e.preventDefault();
  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
});


