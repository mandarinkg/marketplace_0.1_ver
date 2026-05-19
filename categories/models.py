from django.db import models
from django.utils.text import slugify
import uuid

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
        # Башкаруу панелинде ички категория экени даана көрүнүп турушу үчүн
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name