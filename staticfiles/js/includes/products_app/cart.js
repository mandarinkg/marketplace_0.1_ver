// static/js/cart_app/cart.js
// Корзина + Сравнение

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

document.addEventListener('DOMContentLoaded', function () {

    // ==========================================
    // КОРЗИНА
    // ==========================================
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function () {
            const productId = this.dataset.productId;

            // Анимация кнопки
            this.style.transform = 'scale(0.9)';
            setTimeout(() => this.style.transform = '', 150);

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
                    // Badge хедерде
                    const badge = document.getElementById('cart-badge');
                    if (badge) {
                        badge.textContent = data.total_quantity;
                        badge.style.backgroundColor = '#2ecc71';
                    }
                    // Мобил менюдагы badge
                    const mobileBadge = document.getElementById('mobile-cart-badge');
                    if (mobileBadge) {
                        mobileBadge.textContent = data.total_quantity;
                        mobileBadge.style.display = data.total_quantity > 0 ? 'block' : 'none';
                    }
                }
            })
            .catch(error => console.error('Cart error:', error));
        });
    });

    // ==========================================
    // СРАВНЕНИЕ (жергиликтүү, localStorage жок)
    // ==========================================
    let compareList = [];

    document.querySelectorAll('.compare-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const productId = this.dataset.id;
            const icon = this.querySelector('i');

            if (compareList.includes(productId)) {
                // Алып салуу
                compareList = compareList.filter(id => id !== productId);
                icon.style.color = '';
                showToast('Салыштыруудан алынды');
            } else {
                if (compareList.length >= 4) {
                    showToast('Макс. 4 товар салыштырылат!', 'warn');
                    return;
                }
                compareList.push(productId);
                icon.style.color = '#2ecc71';
                showToast('Салыштырууга кошулду ✓');
            }

            // Badge сравнение
            const badge = document.querySelector('.compare-badge');
            if (badge) badge.textContent = compareList.length;
        });
    });

});

// ==========================================
// TOAST УВЕДОМЛЕНИЕ
// ==========================================
function showToast(message, type = 'success') {
    let toast = document.getElementById('fine-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'fine-toast';
        toast.style.cssText = `
            position: fixed;
            bottom: 80px;
            left: 50%;
            transform: translateX(-50%) translateY(20px);
            background: #1a1a2e;
            color: #fff;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            z-index: 9999;
            opacity: 0;
            transition: all 0.3s ease;
            white-space: nowrap;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            border-left: 4px solid #2ecc71;
        `;
        document.body.appendChild(toast);
    }

    if (type === 'warn') toast.style.borderLeftColor = '#f39c12';
    else toast.style.borderLeftColor = '#2ecc71';

    toast.textContent = message;
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';

    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(20px)';
    }, 2500);
}