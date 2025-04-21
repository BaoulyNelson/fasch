document.addEventListener('DOMContentLoaded', () => {
    const element = document.getElementById('typewriter-text');
  
    const texts = [
      "Université d’État d’Haïti",
      "Faculté des Sciences Humaines",
      "Recherche, Savoir, Progrès"
    ];
  
    const colors = [
      "#D21034",  // rouge Haïti
      "#0057A6",  // bleu FASCH
      "#28A745"   // vert pour recherche
    ];
  
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
  
    const type = () => {
      const currentText = texts[textIndex];
      const currentColor = colors[textIndex];
  
      element.style.color = currentColor; // changer couleur
      if (!isDeleting && charIndex <= currentText.length) {
        element.textContent = currentText.substring(0, charIndex++);
      } else if (isDeleting) {
        element.textContent = currentText.substring(0, charIndex--);
      }
  
      let delay = isDeleting ? 50 : 100;
  
      if (!isDeleting && charIndex === currentText.length + 1) {
        isDeleting = true;
        delay = 2000;
      }
  
      if (isDeleting && charIndex === 0) {
        isDeleting = false;
        textIndex = (textIndex + 1) % texts.length;
        delay = 1000;
      }
  
      setTimeout(type, delay);
    };
  
    type();
  });



  