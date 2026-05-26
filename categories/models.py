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


    def __str__(self):
        lang = get_language()
        if lang == 'ky' and self.name_ky:
            return self.name_ky
        elif lang == 'ru' and self.name_ru:
            return self.name_ru
        # fallback — что есть то и вернёт
        return self.name_ky or self.name_ru or self.name or '---'