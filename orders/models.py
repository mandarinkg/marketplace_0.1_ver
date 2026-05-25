from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('delivering', 'Передан курьеру'),
        ('on_the_way', 'На маршруте'),
        ('delivered', 'Доставлен'),
    ]

    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='client_orders'
    )

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employee_orders'
    )

    courier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courier_orders'
    )

    # Жаңы кошулуучу байланыш маалыматтары:
    full_name = models.CharField(max_length=255, verbose_name="ФИО клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адрес доставки")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий к заказу")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order #{self.id} - {self.status}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    
    # БИЗНЕС-АНАЛИТИКА ТАЛААЛАРЫ
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена закупки на момент заказа")
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Цена продажи на момент заказа")

    def __str__(self):
        return self.product_name