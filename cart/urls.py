from django.urls import path
from .views import add_to_cart_view

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
]