# categories/context_processors.py

from .models import Category


def menu_categories(request):

    categories = Category.objects.filter(
        parent__isnull=True
    ).prefetch_related('children')

    return {
        'menu_categories': categories
    }