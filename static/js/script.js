document.addEventListener("DOMContentLoaded", function() {
    // Récupérer les éléments nécessaires
    const sidePanel = document.getElementById("side-panel");
    const hamburgerBtn = document.getElementById("hamburger-btn");
    const closePanelBtn = document.getElementById("close-panel-btn");

    // Vérification si les éléments existent avant d'ajouter les listeners
    if (hamburgerBtn && sidePanel && closePanelBtn) {
        // Ouvrir le panneau lorsqu'on clique sur le bouton hamburger
        hamburgerBtn.addEventListener("click", () => {
            sidePanel.style.transform = "translateX(0)";
        });

        // Fermer le panneau lorsqu'on clique sur le bouton "fermer"
        closePanelBtn.addEventListener("click", () => {
            sidePanel.style.transform = "translateX(-100%)";
        });
    } else {
        console.error("Certains éléments sont manquants dans le DOM.");
    }

    // Charger le header à partir du fichier header.html
    fetch('partials/header.html')
        .then(response => response.text())
        .then(data => document.getElementById('header-placeholder').innerHTML = data);
});
