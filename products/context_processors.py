from favorites.models import Favorite

def favorite_count(request):
    # Эгер колдонуучу катталган болсо жана ролу 'client' болсо, анын тандагандарын эсептейбиз
    if request.user.is_authenticated and request.user.role == 'client':
        count = Favorite.objects.filter(user=request.user).count()
    else:
        count = 0
        
    # Бул өзгөрмө бардык HTML шаблондордо колдонууга даяр болот
    return {
        'favorite_count': count
    }