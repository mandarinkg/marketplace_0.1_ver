from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
# Өзгөртүлгөн формалар туура импорттолду
from .forms import ProductCreateForm, ProductUpdateForm
from django.http import JsonResponse # AJAX жооптору үчүн



# Бардык колдонуучулар сайттын башкы баракчасында бардык активдүү товарларды көрө алышат
# products/views.py ичиндеги index_view функциясын ушул менен алмаштыр
# products/views.py ичиндеги index_view функциясын ушул менен алмаштыр

def index_view(request):
    # Акциядагы товарлар гана башкы бетте
    discounted_products = Product.objects.filter(
        discount_percent__gt=0,
        stock__gt=0,
    ).order_by('-discount_percent')[:12]

    favorite_product_ids = []
    if request.user.is_authenticated and request.user.role == 'client':
        from favorites.models import Favorite
        favorite_product_ids = Favorite.objects.filter(
            user=request.user
        ).values_list('product_id', flat=True)

    context = {
        'discounted_products': discounted_products,
        'favorite_product_ids': list(favorite_product_ids),
    }
    return render(request, 'products/index.html', context)
    

# Client жана башкалар товардун деталдарын көрөт, seller өзүнүн товарларынын деталдарын гана көрөт
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    is_favorite = False

    if request.user.is_authenticated and request.user.role == 'client':
        from favorites.models import Favorite
        is_favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'is_favorite': is_favorite,
    })


# Seller өзүнүн товарларын гана көрөт, client жана башкалар бардык товарларды көрөт
# product_list функциясын ушул менен алмаштыр

@login_required(login_url='accounts:login')
def product_list(request):
    category_id = request.GET.get('category')

    if request.user.role == 'seller':
        products = Product.objects.filter(seller=request.user)
    else:
        products = Product.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)

    products = products.exclude(slug='').exclude(slug__isnull=True)

    # ← ЭНЕ ЖЕТИШПЕГЕН ЖЕРИ
    favorite_product_ids = []
    if request.user.is_authenticated and request.user.role == 'client':
        from favorites.models import Favorite
        favorite_product_ids = list(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    return render(request, 'products/product_list.html', {
        'products': products,
        'favorite_product_ids': favorite_product_ids,  # ← ЭНЕ ЖЕТИШПЕГЕН ЖЕРИ
    })


# Seller гана товарларды кошо алат
@login_required(login_url='accounts:login')
def product_create(request):
    # Ролу seller болбогон колдонуучуларды киргизбейбиз
    if request.user.role != 'seller':
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user  # Сатуучуну автоматтык түрдө каттайбыз
            product.save()
            return redirect('products:detail', slug=product.slug)
    else:
        form = ProductCreateForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Добавить товар'
    })


# Seller өзүнүн товарларын гана түзөтө алат (Ийкемдүү скидка эсептөөсү менен)
@login_required(login_url='accounts:login')
def product_edit(request, slug):
    # Коопсуздук: Колдонуучу сатуучу болушу керек
    if request.user.role != 'seller':
        return redirect('dashboard:home')
        
    # Товарды базадан издейбиз, ал тек гана ушул сураныч жиберген сатуучуга таандык болушу шарт
    product = get_object_or_404(
        Product,
        slug=slug,
        seller=request.user
    )

    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:detail', slug=product.slug)
    else:
        form = ProductUpdateForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Редактировать товар'
    })


# Seller гана товарларды өчүрө алат
@login_required(login_url='accounts:login')
def product_delete(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        seller=request.user
    )
    product.delete()
    return redirect('products:list')



