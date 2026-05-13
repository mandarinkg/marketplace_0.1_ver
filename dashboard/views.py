
from django.contrib.admin.views.decorators import staff_member_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required


from products.models import Product
from orders.models import Order

User = get_user_model()

# dashboard home - redirect based on user role
@login_required(login_url='accounts:login')
def home(request):
    """Dashboard home - redirect based on user role"""
    user = request.user
    
    if user.role == 'seller':
        return redirect('dashboard:seller')
    elif user.role == 'employee':
        return redirect('dashboard:employee')
    elif user.role == 'courier':
        return redirect('dashboard:courier')
    else:  # client
        return redirect('dashboard:client')




# admin dashboard
@staff_member_required(login_url='accounts:login')
def admin_dashboard(request):
    users = User.objects.all().order_by('-date_joined')

    stats = {
        'total_users': User.objects.count(),
        'sellers': User.objects.filter(role='seller').count(),
        'employees': User.objects.filter(role='employee').count(),
        'couriers': User.objects.filter(role='courier').count(),
        'clients': User.objects.filter(role='client').count(),
        'staff_count': User.objects.filter(is_staff=True).count(),
        'total_orders': Order.objects.count(),
        'active_couriers': User.objects.filter(
            role='courier',
            is_active=True
        ).count(),
    }

    return render(request, 'dashboard/admin_dashboard.html', {
        'users': users,
        'stats': stats,
    })
  


# seller dashboard
@login_required(login_url='accounts:login')
def seller_dashboard(request):
    if request.user.role != 'seller':
        return redirect('dashboard:home')

    products_count = Product.objects.filter(
        seller=request.user
    ).count()

    orders_count = Order.objects.count()

    context = {
        'role': 'Продавец',
        'products_count': products_count,
        'orders_count': orders_count,
    }

    return render(request, 'dashboard/seller.html', context)


# admin dashboard
@login_required(login_url='accounts:login')
def employee_dashboard(request):
    """Employee dashboard"""
    if request.user.role != 'employee':
        return redirect('dashboard:home')
    
    context = {
        'role': 'Сотрудник'
    }
    return render(request, 'dashboard/employee.html', context)


@login_required(login_url='accounts:login')
def courier_dashboard(request):
    """Courier dashboard"""
    if request.user.role != 'courier':
        return redirect('dashboard:home')
    
    context = {
        'role': 'Курьер'
    }
    return render(request, 'dashboard/courier.html', context)


# client dashboard
@login_required(login_url='accounts:login')
def client_dashboard(request):
    """Client dashboard"""
    if request.user.role != 'client':
        return redirect('dashboard:home')
    
    context = {
        'role': 'Клиент'
    }
    return render(request, 'dashboard/client.html', context)
