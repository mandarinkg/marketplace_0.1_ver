from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone  # Убакыт менен иштөө үчүн китепкана
from django.db.models import Sum, F  # Бааларды кошуу жана талааларды көбөйтүү үчүн
from datetime import timedelta  # Күндөрдү артка эсептөө үчүн

from .models import Order, OrderItem
from products.models import Product




# ==============================================================================
# CLIENT (КАРДАРЛАР ҮЧҮН ЛОГИКА)
# ==============================================================================

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

    # БИЗНЕС-АНАЛИТИКА: Заказ учурундагы сатып алуу жана сатуу бааларын тарыхка бекитүү
    OrderItem.objects.create(
        order=order,
        product=product,
        product_name=product.title,
        quantity=quantity,
        purchase_price=product.purchase_price,  # Купуя өздүк наркы сакталды
        sale_price=product.price                # Сайтындагы сатуу баасы сакталды
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
    order = get_object_or_404(Order, id=order_id, status='new')
    
    if request.method == 'POST':
        item_ids = request.POST.getlist('item_ids')
        quantities = request.POST.getlist('quantities')
        
        for item_id, qty in zip(item_ids, quantities):
            item = get_object_or_404(OrderItem, id=item_id, order=order)
            
            desired_qty = int(qty)
            if desired_qty <= item.product.stock and desired_qty > 0:
                item.quantity = desired_qty
                item.save()
                
        return redirect('orders:client_orders')
        
    return render(request, 'orders/client/edit_order.html', {'order': order})


# ==============================================================================
# ADMIN (АДМИНИСТРАТОР ҮЧҮН ЛОГИКА)
# ==============================================================================

@staff_member_required(login_url='accounts:login')
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    return render(
        request,
        'orders/admin/admin_orders.html',
        {'orders': orders}
    )


# ==============================================================================
# EMPLOYEE (КЫЗМАТКЕРЛЕР ҮЧҮН ЛОГИКА)
# ==============================================================================

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


# ==============================================================================
# COURIER (КУРЬЕРЛЕР ҮЧҮН ЛОГИКА)
# ==============================================================================

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


# ==============================================================================
# STATUS UPDATE (СТАТУСТАРДЫ ӨЗГӨРТҮҮ ЛОГИКАСЫ)
# ==============================================================================

@login_required
def update_order_status(request, order_id, new_status):
    order = get_object_or_404(Order, id=order_id)

    if request.user.role == 'employee':
        if order.status == 'new' and new_status == 'processing':
            order.status = 'processing'
            order.employee = request.user
            order.save()
            return redirect('orders:employee_processing_orders')

        elif order.status == 'processing' and new_status == 'delivering':
            order.status = 'delivering'
            order.save()
            return redirect('orders:employee_delivery_orders')

    elif request.user.role == 'courier':
        if order.status == 'delivering' and new_status == 'on_the_way':
            order.status = 'on_the_way'
            order.courier = request.user
            order.save()
            return redirect('orders:courier_orders')

        elif order.status == 'on_the_way' and new_status == 'delivered':
            order.status = 'delivered'
            order.save()
            return redirect('orders:courier_orders')

    return redirect('dashboard:home')


# ==============================================================================
# CART TO ORDER (КОРЗИНАДАН ЗАКАЗ ТҮЗҮҮ)
# ==============================================================================

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
        # БИЗНЕС-АНАЛИТИКА: Корзинадан буйрутма алууда да сатып алуу жана сатуу бааларын тарыхка сактоо
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.title,
            quantity=item.quantity,
            purchase_price=item.product.purchase_price,  # Купуя өздүк наркы сакталды
            sale_price=item.product.price                # Сайтындагы сатуу баасы сакталды
        )
        print('12 ITEM CREATED')

        item.product.stock -= item.quantity
        item.product.save()

    cart_items.delete()
    print('13 CART CLEARED')

    return redirect('orders:client_orders')


# ==============================================================================
# SELLER ANALYTICS (САТУУЧУНУН ЖЕКЕ АНАЛИТИКАСЫ ЖАНА ОТЧЕТУ) - ЖАҢЫ КОШУЛДУ
# ==============================================================================

@login_required
def seller_sales_analytics(request):
    if request.user.role != 'seller':
        return redirect('dashboard:home')

    period = request.GET.get('period', 'today')
    now = timezone.now()
    start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if period == 'yesterday':
        start_date = start_date - timedelta(days=1)
        end_date = start_date + timedelta(days=1)
    elif period == 'week':
        start_date = start_date - timedelta(days=7)
        end_date = now
    elif period == 'month':
        start_date = start_date - timedelta(days=30)
        end_date = now
    else:
        end_date = now

    sold_items = OrderItem.objects.filter(
        order__status='delivered',
        product__seller=request.user
    ).select_related('order', 'product')

    if period == 'yesterday':
        sold_items = sold_items.filter(order__created_at__gte=start_date, order__created_at__lt=end_date)
    else:
        sold_items = sold_items.filter(order__created_at__gte=start_date, order__created_at__lte=end_date)

    sold_items = sold_items.order_by('-order__created_at')

    # Финансылык эсептөөлөр
    total_revenue = sold_items.annotate(
        item_revenue=F('quantity') * F('sale_price')
    ).aggregate(total=Sum('item_revenue'))['total'] or 0

    total_profit = sold_items.annotate(
        item_profit=(F('sale_price') - F('purchase_price')) * F('quantity')
    ).aggregate(total=Sum('item_profit'))['total'] or 0

    for item in sold_items:
        item.single_profit = item.sale_price - item.purchase_price
        item.total_profit = item.single_profit * item.quantity
        item.is_loss = item.single_profit < 0

    return render(request, 'orders/seller/sales_analytics.html', {
        'sold_items': sold_items,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'current_period': period,
        'title': 'Финансовый отчет'
    })