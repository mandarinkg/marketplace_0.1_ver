from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='cart'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        if self.user:
            return f"Корзина пользователя: {self.user.username}"
        return f"Корзина гостя: {self.session_key}"

    def get_total_quantity(self):
        """Себеттеги товарлардын жалпы санын эсептейт"""
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        """Себеттеги бардык товарлардын жалпы суммасын эсептейт"""
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ('cart', 'product')

    def __str__(self):
        # Бул жер оңдолду: name ордуна title колдонулду
        return f"{self.product.title} x {self.quantity}"

    def get_cost(self):
        """Бул товардын жалпы суммасын эсептейт (Баасы x Саны)"""
        return self.product.price * self.quantity