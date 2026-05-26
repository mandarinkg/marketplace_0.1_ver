// static/js/theme.js
// Күн/Түн режимин которуу

(function () {
    const body = document.documentElement;
    const btn = document.getElementById('themeToggle');
    const icon = document.getElementById('themeIcon');
    const label = document.getElementById('themeLabel');

    // Сакталган режимди жүктөө
    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        icon.className = 'fas fa-sun';
        label.textContent = 'Күн';
    }

    if (btn) {
        btn.addEventListener('click', function () {
            body.classList.toggle('dark-mode');

            if (body.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                icon.className = 'fas fa-sun';
                label.textContent = 'Күн';
            } else {
                localStorage.setItem('theme', 'light');
                icon.className = 'fas fa-moon';
                label.textContent = 'Түн';
            }
        });
    }
})();