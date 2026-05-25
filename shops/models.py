from django.db import models

class Shop(models.Model):
    """Дүкөндөрдүн маалыматын сактоочу өзүнчө модель"""
    name = models.CharField(max_length=255, verbose_name="Название магазина")
    address = models.TextField(null=True, blank=True, verbose_name="Адрес магазина")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Телефон магазина")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name