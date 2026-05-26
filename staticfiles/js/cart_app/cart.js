document.addEventListener('DOMContentLoaded', function () {

    const buttons = document.querySelectorAll('.add-to-cart-btn');

    buttons.forEach(button => {

        button.addEventListener('click', function () {

            const productId = this.dataset.productId;

            fetch(`/cart/add/${productId}/`, {

                method: 'POST',

                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken'),
                }

            })

            .then(response => response.json())

            .then(data => {

                if (data.status === 'success') {

                    const badge = document.getElementById('cart-badge');

                    if (badge) {
                        badge.textContent = data.total_quantity;
                    }

                }

            })

            .catch(error => {
                console.error(error);
            });

        });

    });

});


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