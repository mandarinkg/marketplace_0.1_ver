function getCookie(name) {

    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {

            const cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {

                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );

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
                // REMOVE CARD ON FAVORITES PAGE
                // =========================

                if (!data.is_favorite) {

                    const card = button.closest('.product-card');

                    if (card) {

                        card.remove();

                    }

                }


                // =========================
                // HEADER BADGE
                // =========================

                const badge = document.getElementById('favorite-badge');

                if (badge) {

                    badge.textContent = data.favorite_count;

                    if (data.favorite_count <= 0) {

                        badge.style.backgroundColor = '#b2bec3';

                    } else {

                        badge.style.backgroundColor = '#e74c3c';

                    }
                }


                // =========================
                // PAGE COUNT
                // =========================

                const pageCount = document.getElementById(
                    'favorite-page-count'
                );

                if (pageCount) {

                    pageCount.textContent = data.favorite_count;

                }


                // =========================
                // EMPTY FAVORITES
                // =========================

                const grid = document.getElementById('favorite-grid');

                if (
                    grid &&
                    grid.querySelectorAll('.product-card').length === 0
                ) {

                    grid.innerHTML = `
                        <div class="empty-box">
                            Тандалган товарлар жок
                        </div>
                    `;
                }

            }

        })

        .catch(error => {

            console.log('ERROR:', error);

        });

    });

});