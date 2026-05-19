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
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField()
    
    # БАА ЖАНА СКИДКА ТАЛААЛАРЫ
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Текущая цена (со скидкой)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Старая цена (без скидки)")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Скидка в процентах (%)")

    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.title or self.title.strip() == '':
            raise ValidationError('Title не может быть пустым')
        
        # ИЙКЕМДҮҮ БАА ЖАНА СКИДКА ЛОГИКАСЫ
        # 1. Эгерде скидка пайызы киргизилсе жана ал 0дөн чоң болсо
        if self.discount_percent and self.discount_percent > 0:
            if self.discount_percent > 100:
                raise ValidationError('Скидка не может быть больше 100%')
            
            # Эгер бул мурунтан бар товар болсо жана базадагы баасы өзгөртүлбөсө,
            # же жаңы баа кол менен жазылбаса, алгач 'old_price' катары учурдагы бааны бекитебиз
            if not self.old_price and self.price:
                self.old_price = self.price
            
            # Эгерде сатуучу скидка учурунда негизги бааны өзгөртсө, ошол жаңы бааны 'old_price' кылабыз
            if self.pk:
                orig = Product.objects.get(pk=self.pk)
                if orig.price != self.price and orig.old_price == self.old_price:
                    self.old_price = self.price

            # Скидканы эсептөө
            if self.old_price:
                from decimal import Decimal
                discount_amount = self.old_price * (Decimal(self.discount_percent) / Decimal(100))
                self.price = self.old_price - discount_amount
        else:
            # 2. Эгерде скидка талаасы бош болсо же 0 деп жазылса (Скидка жок/Өчүрүлдү)
            # Эгер мурун скидкасы бар болуп, сатуучу аны алып салса, 'old_price' талаасын тазалайбыз
            self.old_price = None
            
            # Баа милдеттүү түрдө болушу керек
            if not self.price:
                raise ValidationError('Укажите цену товара')

        # СЛУГ ГЕНЕРАЦИЯСЫ
        if not self.slug:
            base_slug = slugify(self.title)
            if not base_slug:
                base_slug = f"product-{uuid.uuid4().hex[:8]}"
            
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        super().save(*args, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f'{self.user} -> {self.product}'