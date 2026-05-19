from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .models import Order, OrderItem
from products.models import Product


# =========================
# CLIENT
# =========================
@login_required
def create_order_from_product(request, product_id):
    if request.method != 'POST':
        return redirect('dashboard:home')

    if request.user.role != 'client':
        return redirect('dashboard:home')

    product = get_object_or_404(Product, id=product_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        messages.error(request, 'Некорректное количество')
        return redirect('products:detail', slug=product.slug)

    if quantity < 1:
        messages.error(request, 'Количество минимум 1')
        return redirect('products:detail', slug=product.slug)

    if product.stock <= 0:
        messages.error(request, 'Товар закончился')
        return redirect('products:detail', slug=product.slug)

    if quantity > product.stock:
        messages.error(request, f'Доступно только {product.stock} шт')
        return redirect('products:detail', slug=product.slug)

    order = Order.objects.create(
        client=request.user
    )

    OrderItem.objects.create(
        order=order,
        product=product,
        product_name=product.title,
        quantity=quantity
    )

    product.stock -= quantity
    product.save()

    messages.success(request, 'Заказ создан')
    return redirect('orders:client_orders')


@login_required
def client_orders(request):
    if request.user.role != 'client':
        return redirect('dashboard:home')

    active_orders = Order.objects.filter(
        client=request.user
    ).exclude(status='delivered').order_by('-created_at')

    return render(
        request,
        'orders/client/client_orders.html',
        {'active_orders': active_orders}
    )


@login_required
def client_history(request):
    if request.user.role != 'client':
        return redirect('dashboard:home')

    orders = Order.objects.filter(
        client=request.user,
        status='delivered'
    ).order_by('-created_at')

    return render(
        request,
        'orders/client/client_history.html',
        {'orders': orders}
    )


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        client=request.user
    )

    if order.status != 'new':
        return redirect('orders:client_orders')

    for item in order.items.all():
        if item.product:
            item.product.stock += item.quantity
            item.product.save()

    order.delete()
    return redirect('orders:client_orders')


@login_required
def edit_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        client=request.user
    )

    if order.status != 'new':
        return redirect('orders:client_orders')

    item = order.items.first()

    if request.method == 'POST':
        new_qty = int(request.POST.get('quantity', 1))

        product = item.product

        if not product:
            return redirect('orders:client_orders')

        diff = new_qty - item.quantity

        if diff > 0 and diff > product.stock:
            messages.error(request, 'Недостаточно товара')
            return redirect('orders:edit_order', order_id=order.id)

        product.stock -= diff
        product.save()

        item.quantity = new_qty
        item.save()

        return redirect('orders:client_orders')

    return render(
        request,
        'orders/client/edit_order.html',
        {
            'order': order,
            'item': item
        }
    )


# =========================
# ADMIN
# =========================
@staff_member_required(login_url='accounts:login')
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    return render(
        request,
        'orders/admin/admin_orders.html',
        {'orders': orders}
    )


# =========================
# EMPLOYEE
# =========================
@login_required
def employee_new_orders(request):
    if request.user.role != 'employee':
        return redirect('dashboard:home')

    orders = Order.objects.filter(status='new')

    return render(
        request,
        'orders/employee/employee_new_orders.html',
        {'orders': orders}
    )


@login_required
def employee_processing_orders(request):
    if request.user.role != 'employee':
        return redirect('dashboard:home')

    orders = Order.objects.filter(status='processing')

    return render(
        request,
        'orders/employee/employee_processing_orders.html',
        {'orders': orders}
    )


@login_required
def employee_delivery_orders(request):
    if request.user.role != 'employee':
        return redirect('dashboard:home')

    orders = Order.objects.filter(status='delivering')

    return render(
        request,
        'orders/employee/employee_delivery_orders.html',
        {'orders': orders}
    )


# =========================
# COURIER
# =========================
@login_required
def courier_orders(request):
    if request.user.role != 'courier':
        return redirect('dashboard:home')

    return render(
        request,
        'orders/courier/courier_orders.html',
        {
            'delivery_orders': Order.objects.filter(status='delivering'),
            'route_orders': Order.objects.filter(
                courier=request.user,
                status='on_the_way'
            ),
            'completed_orders': Order.objects.filter(
                courier=request.user,
                status='delivered'
            ),
        }
    )


# =========================
# STATUS UPDATE
# =========================
@login_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)

    if request.user.role == 'employee':

        # NEW -> PROCESSING
        if order.status == 'new' and new_status == 'processing':
            order.status = 'processing'
            order.employee = request.user
            order.save()

            return redirect('orders:employee_processing_orders')

        # PROCESSING -> DELIVERING
        elif order.status == 'processing' and new_status == 'delivering':
            order.status = 'delivering'
            order.save()

            return redirect('orders:employee_delivery_orders')

    elif request.user.role == 'courier':

        # DELIVERING -> ON_THE_WAY
        if order.status == 'delivering' and new_status == 'on_the_way':
            order.status = 'on_the_way'
            order.courier = request.user
            order.save()

            return redirect('orders:courier_orders')

        # ON_THE_WAY -> DELIVERED
        elif order.status == 'on_the_way' and new_status == 'delivered':
            order.status = 'delivered'
            order.save()

            return redirect('orders:courier_orders')

    return redirect('dashboard:home')





# =========================
@login_required
def create_order_from_cart(request):
    print('1 START')

    if request.method != 'POST':
        print('2 NOT POST')
        return redirect('cart:detail')

    from cart.views import get_or_create_cart
    cart = get_or_create_cart(request)
    print('3 CART OK', cart)

    if hasattr(cart, 'items'):
        cart_items = cart.items.all()
        print('4 USING items')
    elif hasattr(cart, 'cart_items'):
        cart_items = cart.cart_items.all()
        print('5 USING cart_items')
    else:
        print('6 NO RELATION')
        return redirect('cart:detail')

    print('7 COUNT =', cart_items.count())

    if not cart_items.exists():
        print('8 EMPTY')
        return redirect('cart:detail')

    for item in cart_items:
        print('PRODUCT', item.product.title, item.quantity, item.product.stock)

        if item.quantity > item.product.stock:
            print('9 STOCK ERROR')
            return redirect('cart:detail')

    print('10 BEFORE CREATE ORDER')

    order = Order.objects.create(
        client=request.user,
        status='new'
    )

    print('11 ORDER CREATED', order.id)

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.title,
            quantity=item.quantity
        )
        print('12 ITEM CREATED')

        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()
    print('13 CART CLEARED')

    return redirect('orders:client_orders')