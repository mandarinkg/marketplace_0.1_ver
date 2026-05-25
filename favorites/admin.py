from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('user__username', 'product__title')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Информация', {
            'fields': ('user', 'product')
        }),
        ('История', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
