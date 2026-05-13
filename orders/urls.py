from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_test_order, name='create'),
    path('employee/', views.employee_orders, name='employee_orders'),
    path('courier/', views.courier_orders, name='courier_orders'),
    path(
        'update/<int:order_id>/<str:new_status>/',
        views.update_order_status,
        name='update_status'
    ),
    path('my-orders/', views.client_orders, name='client_orders'),
    path('orders/', views.admin_orders, name='admin_orders'),
]