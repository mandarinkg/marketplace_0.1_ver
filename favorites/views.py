from django.views import View
from django.views.generic import ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from products.models import Product
from .models import Favorite


# =========================
# FAVORITES LIST
# =========================
class FavoriteListView(LoginRequiredMixin, ListView):

    model = Favorite

    template_name = 'favorites/favorites_list.html'

    context_object_name = 'favorites'


    def get_queryset(self):

        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('product')


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['favorite_product_ids'] = Favorite.objects.filter(
            user=self.request.user
        ).values_list('product_id', flat=True)

        return context
        

# =========================
# TOGGLE FAVORITE
# =========================
class ToggleFavoriteView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):

        product_id = kwargs.get('product_id')

        product = get_object_or_404(
            Product,
            id=product_id
        )

        favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        ).first()

        # REMOVE
        if favorite:

            favorite.delete()

            is_favorite = False

        # ADD
        else:

            Favorite.objects.create(
                user=request.user,
                product=product
            )

            is_favorite = True

        return JsonResponse({
            'status': 'success',
            'is_favorite': is_favorite,
            'favorite_count': Favorite.objects.filter(
                user=request.user
            ).count()
        })