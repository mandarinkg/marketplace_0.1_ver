from django import forms
from .models import Product


# 1. ТОВАР КИРГИЗҮҮ ФОРМАСЫ
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        # 'shop' талаасы кошулду
        fields = ['shop', 'category', 'title', 'image', 'description', 'purchase_price', 'price', 'stock']
        
        widgets = {
            'shop': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание товара', 'rows': 4}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Цена закупки (Сводные данные)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Цена для продажи на сайте'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop'].required = True
        self.fields['purchase_price'].required = True
        self.fields['price'].required = True


# 2. ТОВАРДЫ ӨЗГӨРТҮҮ ФОРМАСЫ
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['shop', 'category', 'title', 'image', 'description', 'purchase_price', 'price', 'old_price', 'discount_percent', 'stock']
        
        widgets = {
            'shop': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Система тарабынан эсептелет'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'placeholder': 'Мисалы: 10'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop'].required = True
        self.fields['purchase_price'].required = True
        self.fields['price'].required = True  
        self.fields['discount_percent'].required = False  
        self.fields['old_price'].disabled = True