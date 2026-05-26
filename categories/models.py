from django.db import models
from django.utils.text import slugify
import uuid
from django.utils.translation import get_language


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=True, default='')
    slug = models.SlugField(unique=True, blank=True)
    
    # Ички подкатегориялар үчүн жаңы талаа
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='Родительская категория'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        if not self.slug:
            # Эгерде name кириллицада болсо, slugify бош кайтарышы мүмкүн, коопсуздук үчүн уникалдуу маани беребиз
            base_slug = slugify(self.name)
            if not base_slug:
                self.slug = slugify(str(uuid.uuid4())[:8])
            else:
                self.slug = base_slug
        super().save(*args, **kwargs)


    # categories/models.py ичиндеги __str__ методун ушул менен алмаштыр

    def __str__(self):
        lang = get_language()
        
        if lang == 'ky':
            name = self.name_ky or self.name_ru or self.name or '---'
        else:
            name = self.name_ru or self.name_ky or self.name or '---'
        
        # Эгер подкатегория болсо — "Продукты > Эт азыктары" форматта көрсөт
        if self.parent:
            if lang == 'ky':
                parent_name = self.parent.name_ky or self.parent.name_ru or self.parent.name or '---'
            else:
                parent_name = self.parent.name_ru or self.parent.name_ky or self.parent.name or '---'
            return f"{parent_name} > {name}"
        
        return name