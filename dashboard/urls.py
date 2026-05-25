from django.urls import path

# Ар бир ролдун файлдарынан класстарды импорттоо
from .views.admin_dashboard import (
    AdminDashboardView, AdminSellersListView, AdminEmployeesListView, 
    AdminCouriersListView, AdminChangeUserRoleView, AdminToggleUserStatusView, 
    AdminDeleteUserView
)
from .views.seller_dashboard import SellerDashboardView
from .views.employee_dashboard import EmployeeDashboardView
from .views.courier_dashboard import CourierDashboardView
from .views.client_dashboard import ClientDashboardView
from .views.base_dashboard import DashboardHomeView  # Эгер DashboardHomeView өзүнчө калса

app_name = 'dashboard'

urlpatterns = [
    # ==============================================================================
    # БАГЫТТООЧУ БАШКЫ ДАРЕК
    # ==============================================================================
    path('dashboard-home/', DashboardHomeView.as_view(), name='home'),
    
    # ==============================================================================
    # НЕГИЗГИ ПАНЕЛДЕР (РОЛДОР БОЮНЧА)
    # ==============================================================================
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('seller/', SellerDashboardView.as_view(), name='seller'),
    path('employee/', EmployeeDashboardView.as_view(), name='employee'),
    path('courier/', CourierDashboardView.as_view(), name='courier'),
    path('client/', ClientDashboardView.as_view(), name='client'),

    # ==============================================================================
    # АДМИНИСТРАТОРДУН КОЛДОНУУЧУЛАРДЫ БАШКАРУУ ДАРЕКТЕРИ
    # ==============================================================================
    path('admin/sellers/', AdminSellersListView.as_view(), name='admin_sellers_list'),
    path('admin/employees/', AdminEmployeesListView.as_view(), name='admin_employees_list'),
    path('admin/couriers/', AdminCouriersListView.as_view(), name='admin_couriers_list'),
    path('admin/change-role/<int:user_id>/', AdminChangeUserRoleView.as_view(), name='admin_change_user_role'),
    path('admin/toggle-status/', AdminToggleUserStatusView.as_view(), name='admin_toggle_user_status'),
    path('admin/delete/', AdminDeleteUserView.as_view(), name='admin_delete_user'),
]