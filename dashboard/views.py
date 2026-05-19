from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from products.models import Product, Favorite
from orders.models import Order


User = get_user_model()


# dashboard home
@login_required(login_url='accounts:login')
def home(request):
    user = request.user

    if user.role == 'seller':
        return redirect('dashboard:seller')
    elif user.role == 'employee':
        return redirect('dashboard:employee')
    elif user.role == 'courier':
        return redirect('dashboard:courier')
    else:
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

    return render(request, 'dashboard/seller.html', {
        'role': 'Продавец',
        'products_count': products_count,
        'orders_count': orders_count,
    })


# employee dashboard
@login_required(login_url='accounts:login')
def employee_dashboard(request):
    if request.user.role != 'employee':
        return redirect('dashboard:home')

    new_orders = Order.objects.filter(status='new').count()
    processing_orders = Order.objects.filter(status='processing').count()
    delivering_orders = Order.objects.filter(status='delivering').count()

    return render(request, 'dashboard/employee.html', {
        'role': 'Сотрудник',
        'new_orders': new_orders,
        'processing_orders': processing_orders,
        'delivering_orders': delivering_orders,
    })


# courier dashboard
@login_required(login_url='accounts:login')
def courier_dashboard(request):
    if request.user.role != 'courier':
        return redirect('dashboard:home')

    assigned_orders = Order.objects.filter(
        courier=request.user,
        status='delivering'
    ).count()

    route_orders = Order.objects.filter(
        courier=request.user,
        status='on_route'
    ).count()

    completed_orders = Order.objects.filter(
        courier=request.user,
        status='delivered'
    ).count()

    return render(request, 'dashboard/courier.html', {
        'role': 'Курьер',
        'assigned_orders': assigned_orders,
        'route_orders': route_orders,
        'completed_orders': completed_orders,
    })


# client dashboard
@login_required(login_url='accounts:login')
def client_dashboard(request):
    if request.user.role != 'client':
        return redirect('dashboard:home')

    # delivered болбогон заказдар гана
    orders_count = Order.objects.filter(
        client=request.user
    ).exclude(
        status='delivered'
    ).count()

    favorites_count = Favorite.objects.filter(
        user=request.user
    ).count()

    context = {
        'role': 'Клиент',
        'orders_count': orders_count,
        'favorites_count': favorites_count,
    }

    return render(
        request,
        'dashboard/client.html',
        context
    )