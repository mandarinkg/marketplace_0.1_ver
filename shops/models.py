# shops/models.py — ушул менен алмаштыр

from django.db import models
from django.conf import settings


class Shop(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_shops',
        verbose_name='Владелец',
        null=True,  # эски маалыматтар үчүн
        blank=True
    )
    name = models.CharField(max_length=255, verbose_name="Название магазина")
    address = models.TextField(null=True, blank=True, verbose_name="Адрес магазина")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Телефон магазина")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name