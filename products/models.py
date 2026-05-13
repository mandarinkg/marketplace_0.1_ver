from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from categories.models import Category

import uuid


class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )

    title = models.CharField(max_length=255, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True, null=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Валидация: title не может быть пустым
        if not self.title or self.title.strip() == '':
            raise ValidationError('Title не может быть пустым')
        
        # Генерация slug если его нет
        if not self.slug:
            base_slug = slugify(self.title)
            
            # Если base_slug пустой после slugify, используем ID
            if not base_slug:
                base_slug = f"product-{uuid.uuid4().hex[:8]}"
            
            # Проверка уникальности и добавление уникального кода если нужно
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title