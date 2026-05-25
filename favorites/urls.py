from django.urls import path

from .views import (
    ToggleFavoriteView,
    FavoriteListView
)

app_name = 'favorites'

urlpatterns = [

    path(
        'toggle/<int:product_id>/',
        ToggleFavoriteView.as_view(),
        name='toggle'
    ),

    path(
        'list/',
        FavoriteListView.as_view(),
        name='list'
    ),
]