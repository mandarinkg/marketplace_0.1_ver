from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'seller', 'category', 'price', 'old_price', 'discount_percent', 'stock')
    list_filter = ('category', 'discount_percent', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}