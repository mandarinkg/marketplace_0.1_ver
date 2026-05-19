(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
        const cartBadge = document.getElementById('cart-badge');

        addToCartButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const productId = this.getAttribute('data-product-id');
                if (!productId) return;

                const url = `/cart/add/${productId}/`;
                const csrftoken = getCartCookie('csrftoken');

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrftoken,
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (!response.ok) throw new Error('Сервердик ката');
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        if (cartBadge) {
                            cartBadge.textContent = data.total_quantity;
                            cartBadge.style.backgroundColor = '#3bc574'; // Шапкадагы сан жашыл түскө өзгөрөт
                        }
                    } else {
                        console.error(data.message);
                    }
                })
                .catch(error => console.error('Сурам катасы:', error));
            });
        });

        function getCartCookie(name) {
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
    });
})();