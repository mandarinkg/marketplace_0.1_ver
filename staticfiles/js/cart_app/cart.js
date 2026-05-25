(function() {
    document.addEventListener('DOMContentLoaded', function() {
        // Башкы беттеги бардык жашыл себет баскычтарын табабыз
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
                    if (!response.ok) throw new Error('Ошибка сервера');
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        if (cartBadge) {
                            // Санды реалдуу убакытта жаңылайбыз
                            cartBadge.textContent = data.total_quantity;
                            // Сиз каалаган ачык жашыл түс туруктуу күйөт
                            cartBadge.style.backgroundColor = '#62cb78'; 
                        }
                    } else {
                        console.error(data.message);
                    }
                })
                .catch(error => console.error('Ошибка запроса:', error));
            });
        });

        // CSRF Токенди коопсуз окуу функциясы
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