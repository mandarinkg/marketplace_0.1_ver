from django.db import models
from django.utils.text import slugify
from django.utils.translation import get_language
import uuid


class Category(models.Model):

    ICON_CHOICES = [
        ('📱', 'Электроника'),
        ('🛒', 'Продукты'),
        ('👕', 'Одежда'),
        ('🏠', 'Дом'),
        ('💊', 'Аптека'),
        ('🌱', 'Сельское хозяйство'),
        ('🎒', 'Школа'),
        ('🧹', 'Чистота'),
        ('📦', 'Другое'),
    ]

    name = models.CharField(
        max_length=255,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    icon = models.CharField(
        max_length=10,
        choices=ICON_CHOICES,
        default='📦'
    )

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.name)

            if not base_slug:
                base_slug = str(uuid.uuid4())[:8]

            slug = base_slug
            counter = 1

            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    @property
    def translated_name(self):

        lang = get_language()

        if lang == 'ky':
            return getattr(self, 'name_ky', self.name)

        return getattr(self, 'name_ru', self.name)

    def __str__(self):

        if self.parent:
            return f'{self.parent.translated_name} → {self.translated_name}'

        return self.translated_name