from django.db import models
from django.contrib.auth.models import AbstractUser
# Жаңы колдонмодон Shop моделин импорттоо
from shops.models import Shop 

class User(AbstractUser):
    """Custom User model with roles"""
    
    ROLES = [
        ('seller', 'Продавец'),
        ('employee', 'Сотрудник'),
        ('courier', 'Курьер'),
        ('client', 'Клиент'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20, 
        choices=ROLES, 
        default='client'
    )

    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон номер")
    address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    
    # Башка колдонмодогу модель менен байланыш
    shops = models.ManyToManyField(
        Shop, 
        blank=True, 
        related_name='sellers', 
        verbose_name="Магазины продавца"
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        name = self.get_full_name() if self.get_full_name() else self.username
        return f"{name} ({self.get_role_display()})"