from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from products.models import Product

def get_or_create_cart(request):
    """Колдонуучу же конок үчүн себетти таап берет же түзөт"""
    from .models import Cart # Циклический импорт болбошу үчүн функциянын ичинде ачабыз
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
        from .models import CartItem
        
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
            'message': f'Товар "{product.title}" кошулду.' # Бул жер оңдолду
        })
        
    return JsonResponse({'status': 'error', 'message': 'Недопустимый запрос'}, status=400)