from .views import get_or_create_cart

def cart_counter(request):
    """Сайттын бардык барактарында себеттеги товарлардын санын жеткиликтүү кылат"""
    # Эгер бул администратордун баракчасы (admin) болсо, себетти эсептебейбиз
    if request.path.startswith('/admin/'):
        return {'cart_total_quantity': 0}
        
    try:
        cart = get_or_create_cart(request)
        return {'cart_total_quantity': cart.get_total_quantity()}
    except Exception:
        return {'cart_total_quantity': 0}