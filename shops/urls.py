# shops/urls.py

from django.urls import path
from . import views

app_name = 'shops'

urlpatterns = [
    path('', views.shop_list, name='list'),
    path('create/', views.shop_create, name='create'),
    path('<int:shop_id>/edit/', views.shop_edit, name='edit'),
    path('<int:shop_id>/delete/', views.shop_delete, name='delete'),
]