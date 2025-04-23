document.addEventListener('DOMContentLoaded', function() {
    const menuItems = document.querySelectorAll('.mobile-nav-item');
    menuItems.forEach(item => {
        const link = item.querySelector('.mobile-nav-link');
        const icon = item.querySelector('.submenu-toggle-icon');

        link.addEventListener('click', function(e) {
            e.preventDefault();
            const submenu = item.querySelector('.mobile-submenu');
            if (submenu) {
                submenu.classList.toggle('hidden');
                if (icon) {
                    icon.classList.toggle('rotated');
                }
            }
        });
    });
});
