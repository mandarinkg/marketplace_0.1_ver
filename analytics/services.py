from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F, DecimalField, Case, When
from django.contrib.auth import get_user_model
from orders.models import OrderItem  

User = get_user_model()

class AdminAnalyticsService:
    @staticmethod
    def get_sellers_with_financials(target_seller_id=None, date_filter=None):
        """ 
        Ар бир сатуучунун аналитикасын өзүнчө чыпкалай турган 
        жана закупка баасы 0 болгондо пайданы 0 кылган туруктуу сервис.
        """
        sellers = User.objects.filter(role='seller').prefetch_related('shops')
        now = timezone.now()

        for seller in sellers:
            # Демейки шарт: Жеткирилген бардык маалыматтар
            base_query = {'order__status': 'delivered', 'product__seller': seller}

            # Эгер бул сатуучу тандалган болсо гана убакыт чыпкасын киргизүү
            if target_seller_id and str(seller.id) == str(target_seller_id):
                if date_filter == 'today':
                    # Ички заказдын датасына туура кайрылуу
                    base_query['order__created_at__date'] = now.date()
                elif date_filter == '3_days':
                    base_query['order__created_at__gte'] = now - timedelta(days=3)
                elif date_filter == '7_days':
                    base_query['order__created_at__gte'] = now - timedelta(days=7)
                elif date_filter == 'month':
                    base_query['order__created_at__gte'] = now - timedelta(days=30)

            seller_delivered_items = OrderItem.objects.filter(**base_query)

            # 1. Жалпы выручка (Общий оборот)
            revenue_data = seller_delivered_items.aggregate(
                total=Sum(F('sale_price') * F('quantity'), output_field=DecimalField())
            )
            seller.total_revenue = revenue_data['total'] if revenue_data['total'] is not None else Decimal('0')

            # 2. Жалпы өздүк баа (Закупка)
            cost_data = seller_delivered_items.aggregate(
                total=Sum(F('purchase_price') * F('quantity'), output_field=DecimalField())
            )
            # Түзөтүү: Агрегациядан кайткан ачкычты катасыз текшерүү
            seller.total_cost = cost_data['total'] if cost_data['total'] is not None else Decimal('0')

            # 3. Ички таблицанын маалыматтары жана "Закупка 0 болсо таза пайда 0" логикасы
            seller.sales_table = seller_delivered_items.select_related('order', 'product').annotate(
                item_total_sale=F('sale_price') * F('quantity'),
                item_total_purchase=F('purchase_price') * F('quantity'),
                item_profit=Case(
                    When(purchase_price=Decimal('0'), then=Decimal('0')),
                    default=(F('sale_price') - F('purchase_price')) * F('quantity'),
                    output_field=DecimalField()
                )
            )

            # Жалпы таза пайда
            seller.net_profit = sum(item.item_profit for item in seller.sales_table)

        return sellers