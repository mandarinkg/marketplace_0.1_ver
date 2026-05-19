from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 'parent' талаасы кошулду - бул подкатегориянын башкы категориясын көрсөтөт
    list_display = ('name', 'slug', 'parent')
    
    # Администраторго издөөнү жана чыпкалоону жеңилдетүүчү кошумча куралдар:
    list_filter = ('parent',)  # Оң жака категориялар боюнча чыпкалоочу блок кошот
    search_fields = ('name', 'slug')  # Аты жана slug боюнча издөө талаасын ачат
    
    prepopulated_fields = {'slug': ('name',)}