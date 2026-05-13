from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('<slug:slug>/', views.product_detail, name='detail'),
    path('edit/<slug:slug>/', views.product_edit, name='edit'),
    path('delete/<slug:slug>/', views.product_delete, name='delete'),
]