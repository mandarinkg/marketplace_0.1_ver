from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order

from django.contrib.admin.views.decorators import staff_member_required


@login_required
def create_test_order(request):
    if request.user.role != 'client':
        return redirect('dashboard:home')

    Order.objects.create(client=request.user)
    return redirect('dashboard:home')



# admin: view all orders
@staff_member_required(login_url='accounts:login')
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/admin_orders.html', {
        'orders': orders
    })

# employee: view new and processing orders
@login_required
def employee_orders(request):
    if request.user.role != 'employee':
        return redirect('dashboard:home')

    orders = Order.objects.filter(status__in=['new', 'processing'])
    return render(request, 'orders/employee_orders.html', {'orders': orders})


@login_required
def courier_orders(request):
    if request.user.role != 'courier':
        return redirect('dashboard:home')

    orders = Order.objects.filter(status__in=['delivering', 'delivered'])
    return render(request, 'orders/courier_orders.html', {'orders': orders})



# client: view their orders
@login_required
def client_orders(request):
    if request.user.role != 'client':
        return redirect('dashboard:home')

    orders = Order.objects.filter(client=request.user)

    return render(
        request,
        'orders/client_orders.html',
        {'orders': orders}
    )



# employee: new -> processing
@login_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)

    # employee: new -> processing
    if request.user.role == 'employee':
        if order.status == 'new' and new_status == 'processing':
            order.status = 'processing'
            order.employee = request.user
        else:
            return redirect('dashboard:home')

    # courier: processing -> delivering -> delivered
    elif request.user.role == 'courier':
        if order.status == 'processing' and new_status == 'delivering':
            order.status = 'delivering'
            order.courier = request.user

        elif order.status == 'delivering' and new_status == 'delivered':
            order.status = 'delivered'

        else:
            return redirect('dashboard:home')

    else:
        return redirect('dashboard:home')

    order.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard:home'))