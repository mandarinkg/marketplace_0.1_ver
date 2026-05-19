from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard-home/', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('seller/', views.seller_dashboard, name='seller'),
    path('employee/', views.employee_dashboard, name='employee'),
    path('courier/', views.courier_dashboard, name='courier'),
    path('client/', views.client_dashboard, name='client'),
]
