from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from ..mixins import EmployeeRequiredMixin

# ==============================================================================
# EMPLOYEE DASHBOARD (КЫЗМАТКЕРДИН ПАНЕЛИ)
# ==============================================================================
class EmployeeDashboardView(LoginRequiredMixin, EmployeeRequiredMixin, TemplateView):
    """ Кызматкердин заказдарды башкаруу панели """
    template_name = 'dashboard/employee.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'role': 'Сотрудник',
            'new_orders': Order.objects.filter(status='new').count(),
            'processing_orders': Order.objects.filter(status='processing').count(),
            'delivering_orders': Order.objects.filter(status='delivering').count(),
        })
        return context