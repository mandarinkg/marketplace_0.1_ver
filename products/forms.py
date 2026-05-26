# products/forms.py

from django import forms
from .models import Product
from categories.models import Category
from shops.models import Shop


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop', 'category', 'title', 'image', 'description', 'purchase_price', 'price', 'discount_percent', 'stock']
        widgets = {
            'shop': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Товардын аты'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'placeholder': 'Мисалы: 500 (канча сатып алдыңыз)'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01', 'min': '0',
                'placeholder': 'Мисалы: 700 (канча сатасыз)'
            }),
            'discount_percent': forms.NumberInput(attrs={
                'class': 'form-control', 'min': '0', 'max': '100',
                'placeholder': 'Мисалы: 10 (эгер скидка болсо)'
            }),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Канча штук бар'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            parent__isnull=False
        ).order_by('parent__name_ru', 'name_ru')
        if user:
            self.fields['shop'].queryset = Shop.objects.filter(owner=user)
        self.fields['shop'].required = True
        self.fields['purchase_price'].required = True
        self.fields['price'].required = True
        self.fields['discount_percent'].required = False
        self.fields['discount_percent'].initial = 0
        # Labelларды кыргызчалаштырабыз
        self.fields['purchase_price'].label = 'Сатып алуу баасы (сом)'
        self.fields['price'].label = 'Сатуу баасы (сом)'
        self.fields['discount_percent'].label = 'Скидка % (милдеттүү эмес)'
        self.fields['stock'].label = 'Запас (штук)'
        self.fields['title'].label = 'Товардын аты'
        self.fields['description'].label = 'Сүрөттөмө'
        self.fields['image'].label = 'Сүрөт'
        self.fields['category'].label = 'Категория'
        self.fields['shop'].label = 'Магазин'


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop', 'category', 'title', 'image', 'description', 'purchase_price', 'price', 'discount_percent', 'stock']
        widgets = {
            'shop': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            parent__isnull=False
        ).order_by('parent__name_ru', 'name_ru')
        if user:
            self.fields['shop'].queryset = Shop.objects.filter(owner=user)
        self.fields['shop'].required = True
        self.fields['purchase_price'].required = True
        self.fields['price'].required = True
        self.fields['discount_percent'].required = False
        self.fields['purchase_price'].label = 'Сатып алуу баасы (сом)'
        self.fields['price'].label = 'Сатуу баасы (сом)'
        self.fields['discount_percent'].label = 'Скидка % (милдеттүү эмес)'
        self.fields['stock'].label = 'Запас (штук)'
        self.fields['title'].label = 'Товардын аты'
        self.fields['description'].label = 'Сүрөттөмө'
        self.fields['image'].label = 'Сүрөт'
        self.fields['category'].label = 'Категория'
        self.fields['shop'].label = 'Магазин'