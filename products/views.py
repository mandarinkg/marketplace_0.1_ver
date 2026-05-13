from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'products/product_detail.html', {
        'product': product
    })


@login_required(login_url='accounts:login')
def product_list(request):
    # Продавцы видят только свои товары
    if request.user.role == 'seller':
        products = Product.objects.filter(seller=request.user).exclude(slug='').exclude(slug__isnull=True)
    else:
        # Другие роли видят пустую ленту
        products = Product.objects.none()
    
    return render(request, 'products/product_list.html', {
        'products': products
    })


@login_required(login_url='accounts:login')
def product_create(request):
    if request.user.role != 'seller':
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('products:detail', slug=product.slug)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Добавить товар'
    })


@login_required(login_url='accounts:login')
def product_edit(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        seller=request.user
    )

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:detail', slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Редактировать товар'
    })


@login_required(login_url='accounts:login')
def product_delete(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        seller=request.user
    )

    product.delete()
    return redirect('products:list')