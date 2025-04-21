document.addEventListener("DOMContentLoaded", function () {
    const searchToggle = document.getElementById("mobile-search-toggle");
    const searchForm = document.getElementById("mobile-search-form");
    const searchInput = document.getElementById("mobile-search-input");
    searchToggle.addEventListener("click", function () {
      searchForm.classList.toggle("hidden");
      if (!searchForm.classList.contains("hidden")) {
        searchInput.focus();
      }
    });
  });