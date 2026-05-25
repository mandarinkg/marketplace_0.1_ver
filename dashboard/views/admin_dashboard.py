from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.models import Order
from analytics.services import AdminAnalyticsService
from ..mixins import SuperuserRequiredMixin

User = get_user_model()

# ==============================================================================
# ADMIN DASHBOARD (АДМИНИСТРАТОРДУН ПАНЕЛИ)
# ==============================================================================
class AdminDashboardView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    """ Администратор үчүн жалпы статистика жана колдонуучулардын тизмеси """
    template_name = 'dashboard/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('-date_joined')
        context['stats'] = {
            'total_users': User.objects.count(),
            'sellers': User.objects.filter(role='seller').count(),
            'employees': User.objects.filter(role='employee').count(),
            'couriers': User.objects.filter(role='courier').count(),
            'clients': User.objects.filter(role='client').count(),
            'staff_count': User.objects.filter(is_staff=True).count(),
            'total_orders': Order.objects.count(),
        }
        return context

# ==============================================================================
# ADMIN USER MANAGEMENT (КОЛДОНУУЧУЛАРДЫ БАШКАРУУ)
# ==============================================================================
class AdminSellersListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """ Сатуучулардын каржылык отчетун көрсөтүү """
    template_name = 'accounts/role_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        target_seller = self.request.GET.get('seller_id')
        date_filter = self.request.GET.get('period', 'all')
        return AdminAnalyticsService.get_sellers_with_financials(target_seller, date_filter)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Продавцы', 'current_filter': self.request.GET.get('period', 'all')})
        return context

class AdminEmployeesListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """ Кызматкерлердин тизмесин чыгаруу """
    model = User
    template_name = 'accounts/role_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(role='employee')

class AdminCouriersListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """ Курьерлердин тизмесин чыгаруу """
    model = User
    template_name = 'accounts/role_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.filter(role='courier')

class AdminChangeUserRoleView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    """ Колдонуучунун ролун өзгөртүү """
    model = User
    fields = ['role', 'is_staff', 'is_superuser']
    template_name = 'accounts/change_user_role.html'
    success_url = reverse_lazy('dashboard:admin_dashboard')
    pk_url_kwarg = 'user_id'

class AdminToggleUserStatusView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    """ Колдонуучуну блоктоо/разблокировка кылуу """
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.POST.get('user_id'))
        if user != request.user:
            user.is_active = not user.is_active
            user.save()
        return redirect(request.META.get('HTTP_REFERER', 'dashboard:admin_dashboard'))

class AdminDeleteUserView(LoginRequiredMixin, SuperuserRequiredMixin, View):
    """ Колдонуучуну кызматтан четтетүү (клиентке айлантуу) """
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.POST.get('user_id'))
        if user != request.user:
            user.role, user.is_staff, user.is_superuser = 'client', False, False
            user.save()
        return redirect(request.META.get('HTTP_REFERER', 'dashboard:admin_dashboard'))