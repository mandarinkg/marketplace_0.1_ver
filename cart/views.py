import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Колдонуучу же конок үчүн себетти таап берет же түзөт"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart_view(request, product_id):
    """Товарды себетке кошуу логикасы"""
    if request.method == 'POST' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            action = 'incremented'
        else:
            action = 'added'
            
        return JsonResponse({
            'status': 'success',
            'action': action,
            'total_quantity': cart.get_total_quantity(),
            'message': f'Товар "{product.title}" кошулду.'
        })
        
    return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'}, status=400)

def cart_detail_view(request):
    """Себеттин өзүнчө барагын көрсөтүү"""
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})




# AJAX аркылуу себеттеги товарларды жаңыртуу (санын көбөйтүү, азайтуу же өчүрүү)
@require_POST
def update_cart_item_view(request, item_id):
    """AJAX аркылуу корзина товарын update кылуу"""

    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'status': 'error'}, status=400)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    cart = cart_item.cart
    data = json.loads(request.body)
    action = data.get('action')

    # DELETE
    if action == 'delete':
        cart_item.delete()

        return JsonResponse({
            'status': 'success',
            'item_quantity': 0,
            'item_cost': 0,
            'cart_total_quantity': cart.get_total_quantity(),
            'cart_total_price': cart.get_total_price(),
        })

    # INCREMENT
    elif action == 'increment':

        # STOCK LIMIT CHECK
        if cart_item.quantity >= cart_item.product.stock:
            return JsonResponse({
                'status': 'error',
                'message': f'Максимум {cart_item.product.stock} шт'
            })

        cart_item.quantity += 1
        cart_item.save()

    # DECREMENT
    elif action == 'decrement':

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

            return JsonResponse({
                'status': 'success',
                'item_quantity': 0,
                'item_cost': 0,
                'cart_total_quantity': cart.get_total_quantity(),
                'cart_total_price': cart.get_total_price(),
            })

    return JsonResponse({
        'status': 'success',
        'item_quantity': cart_item.quantity,
        'item_cost': cart_item.get_cost(),
        'cart_total_quantity': cart.get_total_quantity(),
        'cart_total_price': cart.get_total_price(),
    })