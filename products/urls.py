from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index_view, name='home'),
    path('product_list/', views.product_list, name='list'),
    path('create/', views.product_create, name='create'),
    path('edit/<slug:slug>/', views.product_edit, name='edit'),
    path('delete/<slug:slug>/', views.product_delete, name='delete'),
    
    # Деталдуу көрүү барагы ар дайым эң астында турганы туура
    path('<slug:slug>/', views.product_detail, name='detail'),
]