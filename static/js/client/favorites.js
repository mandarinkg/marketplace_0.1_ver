document.addEventListener('DOMContentLoaded', function() {
    const favoriteButtons = document.querySelectorAll('.toggle-favorite-btn');

    favoriteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const productId = this.getAttribute('data-id');
            const icon = this.querySelector('.action-icon');
            const badge = document.getElementById('favorite-badge');

            fetch('/favorite/' + productId + '/?ajax=1', {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Тармактык ката');
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    if (data.action === 'added') {
                        icon.classList.remove('far');
                        icon.classList.add('fas');
                        icon.style.color = '#d9534f';
                        if (badge) badge.textContent = parseInt(badge.textContent || 0) + 1;
                    } else if (data.action === 'removed') {
                        icon.classList.remove('fas');
                        icon.classList.add('far');
                        icon.style.color = '#b2bec3';
                        if (badge) {
                            const currentCount = parseInt(badge.textContent || 0) - 1;
                            badge.textContent = currentCount > 0 ? currentCount : 0;
                        }
                    }
                }
            })
            .catch(error => console.error('Ката:', error));
        });
    });
});

// Артка кайткан учурда баракты жаңылоо (бардык барактар үчүн жалпы иштейт)
window.addEventListener('pageshow', function(event) {
    if (event.persisted || (typeof window.performance != 'undefined' && window.performance.navigation.type === 2)) {
        window.location.reload();
    }
});