// custom.js
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("year").textContent = new Date().getFullYear();
  });
  

document.addEventListener("DOMContentLoaded", function () {
    let backToTopBtn = document.getElementById("back-to-top");

    // Affiche le bouton si l'utilisateur descend au-delà de 300px
    window.addEventListener("scroll", function () {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = "block";
        } else {
            backToTopBtn.style.display = "none";
        }
    });

    // Défilement fluide vers le haut
    backToTopBtn.addEventListener("click", function (e) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});