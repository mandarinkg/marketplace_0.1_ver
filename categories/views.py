# categories/views.py

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .models import Category
from products.models import Product


def category_list(request):

    categories = Category.objects.filter(
        parent__isnull=True
    ).prefetch_related('children')

    days_15_ago = timezone.now() - timedelta(days=15)

    recent_products = Product.objects.filter(
        created_at__gte=days_15_ago,
        stock__gt=0
    ).order_by('-created_at')[:12]

    context = {
        'categories': categories,
        'recent_products': recent_products,
    }

    return render(
        request,
        'categories/category_list.html',
        context
    )


def category_detail(request, slug):

    category = get_object_or_404(
        Category.objects.prefetch_related('children'),
        slug=slug
    )

    subcategories = category.children.all()

    # Главная категория
    if category.parent is None:

        products = Product.objects.filter(
            Q(category=category) |
            Q(category__in=subcategories)
        ).distinct()

    # Подкатегория
    else:

        products = Product.objects.filter(
            category=category
        )

        subcategories = category.parent.children.all()

    products = products.order_by('-created_at')

    favorite_product_ids = []

    if request.user.is_authenticated:

        if request.user.role == 'client':

            from favorites.models import Favorite

            favorite_product_ids = list(
                Favorite.objects.filter(
                    user=request.user
                ).values_list(
                    'product_id',
                    flat=True
                )
            )

    context = {
        'category': category,
        'subcategories': subcategories,
        'products': products,
        'favorite_product_ids': favorite_product_ids,
    }

    return render(
        request,
        'categories/category_detail.html',
        context
    )