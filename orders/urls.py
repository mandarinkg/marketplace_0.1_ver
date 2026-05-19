from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # ---------------- CLIENT ----------------
    path(
        'my-orders/',
        views.client_orders,
        name='client_orders'
    ),

    path(
        'history/',
        views.client_history,
        name='client_history'
    ),

    path(
        'create-from-product/<int:product_id>/',
        views.create_order_from_product,
        name='create_from_product'
    ),

    path(
        'cancel/<int:order_id>/',
        views.cancel_order,
        name='cancel_order'
    ),

    path(
        'edit/<int:order_id>/',
        views.edit_order,
        name='edit_order'
    ),

    # ---------------- EMPLOYEE ----------------
    path(
        'employee/new/',
        views.employee_new_orders,
        name='employee_new_orders'
    ),

    path(
        'employee/processing/',
        views.employee_processing_orders,
        name='employee_processing_orders'
    ),

    path(
        'employee/delivery/',
        views.employee_delivery_orders,
        name='employee_delivery_orders'
    ),

    # ---------------- COURIER ----------------
    path(
        'courier/',
        views.courier_orders,
        name='courier_orders'
    ),

    # ---------------- ADMIN ----------------
    path(
        'admin-orders/',
        views.admin_orders,
        name='admin_orders'
    ),

    # ---------------- STATUS UPDATE ----------------
    path(
        'update/<int:order_id>/<str:new_status>/',
        views.update_order_status,
        name='update_status'
    ),

    # ---------------- CREATE FROM CART ----------------
    path(
        'create-from-cart/',
        views.create_order_from_cart,
        name='create_from_cart'
    ),
]