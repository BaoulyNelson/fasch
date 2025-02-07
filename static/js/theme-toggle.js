document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.body;

  // Récupérer les icônes
  const sunIcon = document.getElementById("icon-sun");
  const moonIcon = document.getElementById("icon-moon");

  // Vérifier si l'utilisateur a déjà une préférence de thème
  const savedTheme = localStorage.getItem('theme');
  console.log("Saved Theme: ", savedTheme);  // Débogage

  if (savedTheme) {
      body.classList.add(savedTheme);
      if (savedTheme === 'dark-theme') {
          sunIcon.style.display = 'none';  // Cacher le soleil
          moonIcon.style.display = 'inline-block';  // Afficher la lune
      } else {
          sunIcon.style.display = 'inline-block';  // Afficher le soleil
          moonIcon.style.display = 'none';  // Cacher la lune
      }
  } else {
      sunIcon.style.display = 'inline-block';  // Afficher par défaut l'icône du soleil
      moonIcon.style.display = 'none';  // Cacher l'icône de la lune
  }

  themeToggle.addEventListener("click", () => {
      console.log("Button clicked");  // Débogage
      // Vérifier si le thème sombre est déjà appliqué
      if (body.classList.contains("dark-theme")) {
          body.classList.remove("dark-theme");
          sunIcon.style.display = 'inline-block';  // Afficher le soleil
          moonIcon.style.display = 'none';  // Cacher la lune
          localStorage.setItem('theme', '');  // Sauvegarder l'état "clair"
      } else {
          body.classList.add("dark-theme");
          sunIcon.style.display = 'none';  // Cacher le soleil
          moonIcon.style.display = 'inline-block';  // Afficher la lune
          localStorage.setItem('theme', 'dark-theme');  // Sauvegarder l'état "sombre"
      }
  });
});
