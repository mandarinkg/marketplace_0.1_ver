from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'slug',
        'seller',
        'category',
        'price',
        'stock',
        'created_at'
    )
    list_filter = ('category', 'seller', 'created_at')
    search_fields = ('title', 'slug', 'description')
    readonly_fields = ('slug', 'created_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Продавец и цена', {
            'fields': ('seller', 'price', 'stock')
        }),
        ('Даты', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # При редактировании существующего объекта
            return self.readonly_fields + ('seller',)
        return self.readonly_fields