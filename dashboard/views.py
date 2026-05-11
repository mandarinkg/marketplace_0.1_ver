from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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


@login_required(login_url='accounts:login')
def seller_dashboard(request):
    """Seller dashboard"""
    if request.user.role != 'seller':
        return redirect('dashboard:home')
    
    context = {
        'role': 'Продавец'
    }
    return render(request, 'dashboard/seller.html', context)


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


@login_required(login_url='accounts:login')
def client_dashboard(request):
    """Client dashboard"""
    if request.user.role != 'client':
        return redirect('dashboard:home')
    
    context = {
        'role': 'Клиент'
    }
    return render(request, 'dashboard/client.html', context)
