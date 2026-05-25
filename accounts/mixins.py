from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class StaffRequiredMixin(UserPassesTestMixin):
    """Колдонуучу админ же менеджер экенин текшерүүчү класс"""
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.role in ['employee', 'seller', 'courier'])

    def handle_no_permission(self):
        return redirect('accounts:login')