from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

User = get_user_model()


@require_http_methods(['GET', 'POST'])
def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Login user after registration
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    return redirect('dashboard:home')
                else:
                    form.add_error(None, 'Неверный пароль')
            except User.DoesNotExist:
                form.add_error(None, 'Пользователь не найден')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='accounts:login')
def logout_view(request):
    """User logout view"""
    logout(request)
    return redirect('accounts:login')
