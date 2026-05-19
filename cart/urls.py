from django.urls import path
from .views import add_to_cart_view, cart_detail_view, update_cart_item_view

app_name = 'cart'

urlpatterns = [
    path('', cart_detail_view, name='detail'),
    path('add/<int:product_id>/', add_to_cart_view, name='add_to_cart'),
    path('update/<int:item_id>/', update_cart_item_view, name='update_item'),
]