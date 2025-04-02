// custom.js
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("year").textContent = new Date().getFullYear();
  });
  

  document.addEventListener("DOMContentLoaded", function () {
    let btn = document.getElementById("btnScrollTop");

    // Afficher le bouton quand on scrolle vers le bas
    window.onscroll = function () {
        if (document.documentElement.scrollTop > 300) {
            btn.style.display = "block";
        } else {
            btn.style.display = "none";
        }
    };

    // Scroll vers le haut quand on clique
    btn.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Mettre à jour l'année automatiquement
    document.getElementById("current-year").textContent = new Date().getFullYear();
});