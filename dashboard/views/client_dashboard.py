# dashboard/views/client_dashboard.py ичиндеги ClientDashboardView классын ушул менен алмаштыр

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from favorites.models import Favorite
from ..mixins import ClientRequiredMixin


# ==============================================================================
# CLIENT DASHBOARD (КАРДАРДЫН ПАНЕЛИ)
# ==============================================================================

class ClientDashboardView(LoginRequiredMixin, ClientRequiredMixin, TemplateView):
    template_name = 'dashboard/client.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context.update({
            # Активдүү заказдар (жеткирилбегендер)
            'orders_count': Order.objects.filter(client=user).exclude(status='delivered').count(),
            # Жеткирилген заказдар
            'delivered_count': Order.objects.filter(client=user, status='delivered').count(),
            # Тандалган товарлар
            'favorites_count': Favorite.objects.filter(user=user).count(),
            # Акыркы 3 заказ
            'recent_orders': Order.objects.filter(client=user).order_by('-created_at')[:3],
        })
        return context




