from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import Order
from favorites.models import Favorite
from ..mixins import ClientRequiredMixin

# ==============================================================================
# CLIENT DASHBOARD (КАРДАРДЫН ПАНЕЛИ)
# ==============================================================================
class ClientDashboardView(LoginRequiredMixin, ClientRequiredMixin, TemplateView):
    """ Кардардын активдүү заказдары жана сүйүктүү товарлары """
    template_name = 'dashboard/client.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context.update({
            'role': 'Клиент',
            'orders_count': Order.objects.filter(client=user).exclude(status='delivered').count(),
            'favorites_count': Favorite.objects.filter(user=user).count()
        })
        return context