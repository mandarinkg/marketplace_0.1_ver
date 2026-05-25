from .models import Favorite

def favorite_count(request):
    """Катталган кардарлардын тандаган товарларынын санын чыгаруу"""
    if request.user.is_authenticated and request.user.role == 'client':
        count = Favorite.objects.filter(user=request.user).count()
    else:
        count = 0
        
    return {
        'favorite_count': count
    }