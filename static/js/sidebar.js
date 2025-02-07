document.addEventListener("DOMContentLoaded", function () {
    // Sélectionnez les éléments nécessaires
    const sidebar = document.getElementById("sidebar");
    const menuBtn = document.getElementById("menu-btn");
    const closeBtn = document.getElementById("close-btn");
  
    // Vérification des éléments avant de les manipuler
    if (sidebar && menuBtn && closeBtn) {
      menuBtn.addEventListener("click", () => {
        sidebar.classList.add("open");
      });
  
      closeBtn.addEventListener("click", () => {
        sidebar.classList.remove("open");
      });
    } else {
      console.error("Certains éléments sont manquants dans le DOM : sidebar, menu-btn ou close-btn.");
    }
  });
  