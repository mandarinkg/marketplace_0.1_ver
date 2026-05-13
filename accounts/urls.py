from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('change-role/<int:user_id>/', views.change_user_role, name='change_user_role'),


    path('sellers/', views.sellers_list, name='sellers'),
    path('employees/', views.employees_list, name='employees'),
    path('couriers/', views.couriers_list, name='couriers'),
]