# shops/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import forms
from .models import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Магазиндин аты'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Дарек'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+996 XXX XXX XXX'}),
        }


@login_required
def shop_list(request):
    """Продавецтин өз магазиндери"""
    if request.user.role != 'seller':
        return redirect('dashboard:home')
    shops = Shop.objects.filter(owner=request.user)
    return render(request, 'shops/shop_list.html', {'shops': shops})


@login_required
def shop_create(request):
    """Жаңы магазин түзүү"""
    if request.user.role != 'seller':
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = ShopForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.owner = request.user
            shop.save()
            return redirect('shops:list')
    else:
        form = ShopForm()

    return render(request, 'shops/shop_form.html', {'form': form, 'title': 'Жаңы магазин'})


@login_required
def shop_edit(request, shop_id):
    """Магазинди түзөтүү"""
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)

    if request.method == 'POST':
        form = ShopForm(request.POST, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('shops:list')
    else:
        form = ShopForm(instance=shop)

    return render(request, 'shops/shop_form.html', {'form': form, 'title': 'Магазинди түзөтүү'})



# Seller гана өз магазиндерин өчүрө алат, жана өчүрүү үчүн confirmation барагы керек
@login_required
def shop_delete(request, shop_id):
    """Магазинди өчүрүү — confirmation page менен"""
    shop = get_object_or_404(Shop, id=shop_id, owner=request.user)

    if request.method == 'POST':
        shop.delete()
        return redirect('shops:list')

    # GET — confirmation барагын көрсөтөбүз
    return render(request, 'shops/shop_confirm_delete.html', {'shop': shop})