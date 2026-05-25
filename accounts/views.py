from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

# Ички формаларды чакыруу
from .forms import RegistrationForm, LoginForm

User = get_user_model()

# ==============================================================================
# КОЛДОНУУЧУЛАРДЫ КАТТОО (REGISTER)
# ==============================================================================
class RegisterView(FormView):
    """ Жаңы колдонуучуларды системага коопсуз каттоо классы """
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('dashboard:home')

    def dispatch(self, request, *args, **kwargs):
        # Эгер колдонуучу мурун эле кирген болсо, каттоо баракчасын ачпайт
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Катталгандан кийин автоматтык түрдө системага киргизүү
        return super().form_valid(form)


# ==============================================================================
# СИСТЕМАНЫН КИРҮҮ ЭШИГИ (LOGIN)
# ==============================================================================
class LoginView(FormView):
    """ Колдонуучулардын тутумга кирүү (Авторизация) классы """
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('dashboard:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        # Аутентификацияны коопсуз текшерүү
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Неверный email или пароль')
            return self.form_invalid(form)


# ==============================================================================
# СИСТЕМАНЫН ЧЫГУУ ЭШИГИ (LOGOUT)
# ==============================================================================
class LogoutView(LoginRequiredMixin, View):
    """ Системадан сессияны коопсуз жаап чыгуу классы """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')