from .models import Category

# Бул функция сайттын бардык баракчаларында жашыл менюга тек гана башкы категорияларды жеткирип берет
def menu_categories(request):
    """
    Бул функция сайттын бардык баракчаларындагы жашыл менюга 
    тек гана эң башкы негизги категорияларды жеткирип берет.
    """
    return {
        # parent__isnull=True - ички подкатегорияларды чыпкалап, башкыларын гана калтырат
        'menu_categories': Category.objects.filter(parent__isnull=True)
    }

