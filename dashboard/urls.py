from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('seller/', views.seller_dashboard, name='seller'),
    path('employee/', views.employee_dashboard, name='employee'),
    path('courier/', views.courier_dashboard, name='courier'),
    path('client/', views.client_dashboard, name='client'),
]
