from django.db import models
from django.contrib.auth.models import AbstractUser


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

    # Жаңы кошулуучу талаалар (башында бош боло алгыдай кылып null=True, blank=True кылабыз)
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон номер")
    address = models.TextField(null=True, blank=True, verbose_name="Адрес доставки")
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
