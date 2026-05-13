from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, LoginForm
from orders.models import Order

from django.contrib.admin.views.decorators import staff_member_required

User = get_user_model()


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard:home')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard:home')
            else:
                form.add_error(None, 'Неверный email или пароль')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='accounts:login')
def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@staff_member_required(login_url='accounts:login')
@require_http_methods(['GET', 'POST'])
def change_user_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('dashboard:admin_dashboard')

    if request.method == 'POST':
        new_role = request.POST.get('role')
        is_staff = request.POST.get('is_staff') == 'on'
        is_superuser = request.POST.get('is_superuser') == 'on'

        if new_role in dict(User.ROLES):
            user.role = new_role
            user.is_staff = is_staff
            user.is_superuser = is_superuser
            user.save()
            return redirect('dashboard:admin_dashboard')

    return render(request, 'accounts/change_user_role.html', {
        'user': user,
        'roles': User.ROLES,
    })



@staff_member_required(login_url='accounts:login')
def sellers_list(request):
    users = User.objects.filter(role='seller')
    return render(request, 'accounts/role_list.html', {
        'users': users,
        'title': 'Продавцы'
    })


@staff_member_required(login_url='accounts:login')
def employees_list(request):
    users = User.objects.filter(role='employee')
    return render(request, 'accounts/role_list.html', {
        'users': users,
        'title': 'Сотрудники'
    })


@staff_member_required(login_url='accounts:login')
def couriers_list(request):
    users = User.objects.filter(role='courier')
    return render(request, 'accounts/role_list.html', {
        'users': users,
        'title': 'Курьеры'
    })