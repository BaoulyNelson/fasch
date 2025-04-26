document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.mobile-nav-item');
  
    menuItems.forEach(item => {
      const link = item.querySelector('.mobile-nav-link');
      const icon = item.querySelector('.submenu-toggle-icon');
      const submenu = item.querySelector('.mobile-submenu');
  
      if (submenu) {
        // Ce lien a un sous-menu, on bloque le clic pour basculer le menu
        link.addEventListener('click', function (e) {
          e.preventDefault();
          submenu.classList.toggle('hidden');
          if (icon) {
            icon.classList.toggle('rotated');
          }
        });
      }
    });
  });
  