from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

# ==============================================================================
# DASHBOARD HOME (БАШКЫ БАГЫТТООЧУ КЛАСС)
# ==============================================================================
class DashboardHomeView(LoginRequiredMixin, View):
    """ 
    Колдонуучунун ролуна жараша тиешелүү панелге багыттайт.
    """
    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_superuser:
            return redirect('dashboard:admin_dashboard')
        elif user.role == 'seller':
            return redirect('dashboard:seller')
        elif user.role == 'employee':
            return redirect('dashboard:employee')
        elif user.role == 'courier':
            return redirect('dashboard:courier')
        else:
            return redirect('dashboard:client')