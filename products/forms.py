from django import forms
from .models import Product


# 1. ТОВАР КИРГИЗҮҮ ФОРМАСЫ (Скидка талаалары такыр жок)
class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        # Сатуучу товарды жаңы киргизип жатканда гана керектелүүчү талаалар
        fields = ['category', 'title', 'image', 'description', 'price', 'stock']
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название товара'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание товара', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Введите цену товара'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Жаңы киргизип жатканда негизги бааны жазуу милдеттүү
        self.fields['price'].required = True


# 2. ТОВАРДЫ ӨЗГӨРТҮҮ ФОРМАСЫ (Скидка жана Эски баа талаалары кошулат)
class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'image', 'description', 'price', 'old_price', 'discount_percent', 'stock']
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'old_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Система тарабынан эсептелет'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100, 'placeholder': 'Каалоочулар үчүн (мисалы: 10)'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}), # Товар түгөнгөндө 0 жазса болот
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Бул талааларды толтуруу сатуучу үчүн милдеттүү эмес (необязательное)
        self.fields['price'].required = True  # Негизги баа дайыма болушу керек
        self.fields['discount_percent'].required = False  # Скидка милдеттүү эмес
        self.fields['old_price'].disabled = True  # Муну сатуучу өзү өзгөртө албайт