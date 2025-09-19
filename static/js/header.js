document.addEventListener("DOMContentLoaded", () => {
    // Активация текущей страницы в меню
    const currentPath = window.location.pathname;
    document.querySelectorAll(".nav a, .mobile-nav a").forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });
    
    // Мобильное меню
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNav = document.getElementById('mobileNav');
    
    if (mobileMenuToggle && mobileNav) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileNav.classList.toggle('active');
            
            // Меняем иконку гамбургера
            if (mobileNav.classList.contains('active')) {
                mobileMenuToggle.innerHTML = '✕';
            } else {
                mobileMenuToggle.innerHTML = '☰';
            }
        });
        
        // Закрываем меню при клике на ссылку
        document.querySelectorAll('.mobile-nav a').forEach(link => {
            link.addEventListener('click', () => {
                mobileNav.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
            });
        });
        
        // Закрываем меню при клике вне его
        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !mobileNav.contains(e.target)) {
                mobileNav.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
            }
        });
        
        // Закрываем меню при изменении размера экрана
        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                mobileNav.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
            }
        });
    }
});