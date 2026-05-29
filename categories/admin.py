from django.contrib import admin
from django.utils.html import format_html

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'image_preview',
        'name',
        'parent',
        'icon',
        'slug',
    )

    list_filter = (
        'parent',
    )

    search_fields = (
        'name',
        'name_ru',
        'name_ky',
        'slug',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }

    ordering = ('name',)

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:8px; object-fit:cover;" />',
                obj.image.url
            )

        return 'Нет фото'

    image_preview.short_description = 'Фото'