from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class SuperuserRequiredMixin(UserPassesTestMixin):
    """Жөн гана администраторлор (is_superuser) үчүн укук текшерүүчү класс"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('accounts:login')


class SellerRequiredMixin(UserPassesTestMixin):
    """Болгону Сатуучулар (seller) үчүн укук текшерүүчү класс"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'seller'

    def handle_no_permission(self):
        return redirect('dashboard:home')


class EmployeeRequiredMixin(UserPassesTestMixin):
    """Болгону Кызматкерлер (employee) үчүн укук текшерүүчү класс"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'employee'

    def handle_no_permission(self):
        return redirect('dashboard:home')


class CourierRequiredMixin(UserPassesTestMixin):
    """Болгону Курьерлер (courier) үчүн укук текшерүүчү класс"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'courier'

    def handle_no_permission(self):
        return redirect('dashboard:home')


class ClientRequiredMixin(UserPassesTestMixin):
    """Болгону Кардарлар (client) үчүн укук текшерүүчү класс"""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'client'

    def handle_no_permission(self):
        return redirect('dashboard:home')