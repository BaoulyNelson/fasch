const messages = [
  "Faculté des Sciences Humaines d'Haïti (FASCH)",
  "Former, Rechercher, Innover",
  "Excellence, Éthique, Engagement"
];

const colors = [
  "darkblue",    // Couleur pour le 1er message
  "green",       // Couleur pour le 2e
  "crimson"      // Couleur pour le 3e
];

const ticker = document.getElementById("ticker-text");
let index = 0;

function showMessage() {
  ticker.style.animation = 'none'; // Reset l'animation
  void ticker.offsetWidth;         // Force le reflow

  ticker.textContent = messages[index];
  ticker.style.color = colors[index]; // 💡 Appliquer la couleur
  ticker.style.animation = 'scroll-left 10s linear forwards';

  index = (index + 1) % messages.length;
}

showMessage();
setInterval(showMessage, 10000);
