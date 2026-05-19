from django.shortcuts import render, get_object_or_404
from .models import Category
from django.db import models 

from products.models import Product  # Сиздин товар моделиңизди чакырабыз


# Башкы категориялардын тизмеси
def category_list(request):
    """
    Тек гана башкы категорияларды тизмелейт (Электроника, Одежда ж.б.).
    Ички подкатегориялар шаблондун ичинде динамикалык түрдө чыгат.
    """
    # parent__isnull=True - бул ички эмес, эң башкы негизги категорияларды гана чыпкалайт
    main_categories = Category.objects.filter(parent__isnull=True)
    
    context = {
        'categories': main_categories
    }
    return render(request, 'categories/category_list.html', context)



# Категориянын же подкатегориянын ичине киргендеги баракча
def category_detail(request, slug):
    """
    Тандалган категориянын товарларын жана анын ички подкатегорияларын көрсөтөт.
    """
    category = get_object_or_404(Category, slug=slug)
    
    # 1. Тандалган категориянын ички подкатегорияларын табабыз
    subcategories = category.children.all()
    
    # 2. Товарларды чыпкалоо логикасы
    if category.parent is None:
        # Эгер башкы категория болсо: өзүнүн жана бардык подкатегорияларынын товарларын көрсөтүү
        products = Product.objects.filter(
            models.Q(category=category) | models.Q(category__in=subcategories)
        ).distinct().order_by('-created_at')
    else:
        # Эгер подкатегория болсо: өзүнүн товарларын гана көрсөтүү
        products = category.products.all().order_by('-created_at')
        
        # Эгер бул подкатегория болсо, анда бир тууган подкатегорияларын менюда көрсөтүү үчүн
        subcategories = category.parent.children.all()

    context = {
        'category': category,
        'subcategories': subcategories,  # Шаблондо баскычтарды чыгаруу үчүн
        'products': products
    }
    return render(request, 'categories/category_detail.html', context)