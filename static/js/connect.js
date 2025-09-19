document.addEventListener('DOMContentLoaded', () => {
    const loginTab = document.getElementById('loginTab');
    const registerTab = document.getElementById('registerTab');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    // Создаем блоки для сообщений под формами
    const createMessageDiv = (form) => {
        let msgDiv = form.querySelector('.form-message');
        if (!msgDiv) {
            msgDiv = document.createElement('div');
            msgDiv.className = 'form-message';
            msgDiv.style.color = 'red';
            msgDiv.style.marginTop = '10px';
            form.appendChild(msgDiv);
        }
        return msgDiv;
    };

    const loginMessage = createMessageDiv(loginForm);
    const registerMessage = createMessageDiv(registerForm);

    // Switch tabs
    loginTab.addEventListener('click', () => {
        loginTab.classList.add('active');
        registerTab.classList.remove('active');
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        loginMessage.textContent = '';
        registerMessage.textContent = '';
    });

    registerTab.addEventListener('click', () => {
        registerTab.classList.add('active');
        loginTab.classList.remove('active');
        registerForm.classList.remove('hidden');
        loginForm.classList.add('hidden');
        loginMessage.textContent = '';
        registerMessage.textContent = '';
    });

    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.previousElementSibling;
            if(input.type === 'password'){
                input.type = 'text';
                btn.textContent = '🙈';
            } else {
                input.type = 'password';
                btn.textContent = '👁️';
            }
        });
    });

    // Helper functions for validation
    const isEmailValid = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

    const isPasswordValid = (password) => /^(?=.*[A-Za-z])(?=.*\d).{8,}$/.test(password);

    const isLatinUsername = (username) => /^[A-Za-z0-9]{3,}$/.test(username);

    // Register form validation
    registerForm.addEventListener('submit', e => {
        e.preventDefault();

        const username = document.getElementById('registerUsername').value.trim();
        const email = document.getElementById('registerEmail').value.trim();
        const password = document.getElementById('registerPassword').value;
        const confirm = document.getElementById('confirmPassword').value;

        registerMessage.style.color = 'red';

        if (!username || !email || !password || !confirm) {
            registerMessage.textContent = "All fields are required!";
            return;
        }

        if (!isLatinUsername(username)) {
            registerMessage.textContent = "Username must be at least 3 characters and contain only English letters and numbers!";
            return;
        }

        if (!isEmailValid(email)) {
            registerMessage.textContent = "Please enter a valid email address!";
            return;
        }

        if (!isPasswordValid(password)) {
            registerMessage.textContent = "Password must be at least 8 characters long and include letters and numbers!";
            return;
        }

        if (password !== confirm) {
            registerMessage.textContent = "Passwords do not match!";
            return;
        }

        registerMessage.style.color = 'green';
        registerMessage.textContent = "Registered successfully!";
        registerForm.reset();
    });

    // Login form validation
    loginForm.addEventListener('submit', e => {
        e.preventDefault();

        const loginOrEmail = document.getElementById('loginEmail').value.trim();
        const password = document.getElementById('loginPassword').value;

        loginMessage.style.color = 'red';

        if (!loginOrEmail || !password) {
            loginMessage.textContent = "All fields are required!";
            return;
        }

        if (loginOrEmail.includes('@')) {
            if (!isEmailValid(loginOrEmail)) {
                loginMessage.textContent = "Please enter a valid email address!";
                return;
            }
        } else {
            if (!isLatinUsername(loginOrEmail)) {
                loginMessage.textContent = "Login must be at least 3 characters and contain only English letters and numbers!";
                return;
            }
        }

        if (!isPasswordValid(password)) {
            loginMessage.textContent = "Password must be at least 8 characters long and include letters and numbers!";
            return;
        }

        loginMessage.style.color = 'green';
        loginMessage.textContent = "Logged in successfully!";
        loginForm.reset();
    });
});
