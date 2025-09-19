document.addEventListener("DOMContentLoaded", () => {
    // =========================
    // Подсветка активной страницы
    // =========================
    const currentPath = window.location.pathname;
    document.querySelectorAll(".nav a, .mobile-nav a").forEach(link => {
        if (link.getAttribute("href") === currentPath) {
            link.classList.add("active");
        }
    });

    // =========================
    // Мобильное меню
    // =========================
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileNav = document.getElementById('mobileNav');

    if (mobileMenuToggle && mobileNav) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileNav.classList.toggle('active');
            mobileMenuToggle.innerHTML = mobileNav.classList.contains('active') ? '✕' : '☰';
        });

        document.querySelectorAll('.mobile-nav a').forEach(link => {
            link.addEventListener('click', () => {
                mobileNav.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
            });
        });

        document.addEventListener('click', (e) => {
            if (!mobileMenuToggle.contains(e.target) && !mobileNav.contains(e.target)) {
                mobileNav.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
            }
        });

        window.addEventListener('resize', () => {
            if (window.innerWidth > 768) {
                mobileNav.classList.remove('active');
                mobileMenuToggle.innerHTML = '☰';
            }
        });
    }

    // =========================
    // Динамическое меню после логина
    // =========================
    const connectBtn = document.getElementById("connectBtn");
    const connectBtnMobile = document.getElementById("connectBtnMobile");
    const logoutContainer = document.getElementById("logoutContainer");
    const logoutContainerMobile = document.getElementById("logoutContainerMobile");

    const updateHeader = () => {
        const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";

        if (isLoggedIn) {
            // Меняем Connect на Chat
            if (connectBtn) {
                connectBtn.href = "/chat";
                connectBtn.querySelector("span").textContent = "Chat";
            }
            if (connectBtnMobile) {
                connectBtnMobile.href = "/chat";
                connectBtnMobile.querySelector("span").textContent = "Chat";
            }

            // Добавляем кнопку Logout в десктопное меню
            if (!document.getElementById("logoutBtn")) {
                const logout = document.createElement("a");
                logout.id = "logoutBtn";
                logout.href = "#";
                logout.textContent = "Logout";
                logout.style.color = "#fff";
                logout.style.fontWeight = "bold";
                logout.addEventListener("click", () => {
                    localStorage.setItem("isLoggedIn", "false");
                    location.reload();
                });

                logoutContainer.appendChild(logout);
                if (logoutContainerMobile) logoutContainerMobile.appendChild(logout.cloneNode(true));
            }
        }
    };

    updateHeader();
});
