// static/js/includes/products_app/favorites.js

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

document.querySelectorAll('.toggle-favorite-btn').forEach(button => {

    button.addEventListener('click', function(e) {
        e.preventDefault();

        const productId = this.dataset.id;
        const icon = this.querySelector('i');

        fetch(`/favorites/toggle/${productId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest',
            }
        })
        .then(response => response.json())
        .then(data => {

            if (data.status === 'success') {

                // =========================
                // HEART ICON
                // =========================
                if (data.is_favorite) {
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                    icon.classList.add('active');
                } else {
                    icon.classList.remove('fas');
                    icon.classList.remove('active');
                    icon.classList.add('far');
                }

                // =========================
                // КАРТОЧКАНЫ ӨЧҮРҮҮ — ТОЛЬКО НА СТРАНИЦЕ ИЗБРАННОГО
                // =========================
                const isFavoritesPage = window.location.pathname.includes('/favorites/');

                if (!data.is_favorite && isFavoritesPage) {
                    const card = button.closest('.product-card');
                    if (card) {
                        card.style.transition = 'opacity 0.3s, transform 0.3s';
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.95)';
                        setTimeout(() => card.remove(), 300);
                    }
                }

                // =========================
                // HEADER BADGE
                // =========================
                const badge = document.getElementById('favorite-badge');
                if (badge) {
                    badge.textContent = data.favorite_count;
                    badge.style.backgroundColor = data.favorite_count > 0 ? '#e74c3c' : '#b2bec3';
                }

                // Мобил менюдагы badge
                const mobileBadge = document.getElementById('mobile-fav-badge');
                if (mobileBadge) {
                    mobileBadge.textContent = data.favorite_count;
                    mobileBadge.style.display = data.favorite_count > 0 ? 'block' : 'none';
                }

                // =========================
                // PAGE COUNT
                // =========================
                const pageCount = document.getElementById('favorite-page-count');
                if (pageCount) {
                    pageCount.textContent = data.favorite_count;
                }

                // =========================
                // EMPTY FAVORITES
                // =========================
                const grid = document.getElementById('favorite-grid');
                if (grid && grid.querySelectorAll('.product-card').length === 0) {
                    grid.innerHTML = `
                        <div class="empty-box" style="text-align:center; padding:60px; color:#95a5a6;">
                            <i class="far fa-heart" style="font-size:48px; margin-bottom:16px; display:block;"></i>
                            Тандалган товарлар жок
                        </div>
                    `;
                }
            }
        })
        .catch(error => console.log('ERROR:', error));
    });
});