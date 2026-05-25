from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from ..mixins import CourierRequiredMixin

# ==============================================================================
# COURIER DASHBOARD (КУРЬЕРДИН ПАНЕЛИ)
# ==============================================================================
class CourierDashboardView(LoginRequiredMixin, CourierRequiredMixin, TemplateView):
    """ Курьердин жеткирүү заказдарынын панели """
    template_name = 'dashboard/courier.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'role': 'Курьер',
            'assigned_orders': Order.objects.filter(courier=user, status='delivering').count(),
            'route_orders': Order.objects.filter(courier=user, status='on_the_way').count(),
            'completed_orders': Order.objects.filter(courier=user, status='delivered').count(),
        })
        return context