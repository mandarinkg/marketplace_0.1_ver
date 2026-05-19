from .views import get_or_create_cart

# Бул кодду сиздин cart/context_processors.py (же тиешелүү) файлыңызга коюңуз

def cart_counter(request):
    """Сайттын бардык барактарында себеттеги товарлардын санын жеткиликтүү кылат"""
    # Администратордун баракчаларында себетти эсептөөнүн кажети жок
    if request.path.startswith('/admin/'):
        return {'cart_total_quantity': 0}
        
    try:
        # Импортту ушул жерде ичинен кылабыз, бул циклдик импорт катасын алдын алат
        from .views import get_or_create_cart
        
        cart = get_or_create_cart(request)
        return {'cart_total_quantity': cart.get_total_quantity()}
    except Exception:
        # Эгер кандайдыр бир ката кетсе (мисалы, база али түзүлө элек болсо), сайт кулабай, жөн гана 0 көрсөтөт
        return {'cart_total_quantity': 0}