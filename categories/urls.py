from django.urls import path
from . import views

app_name = 'categories'

urlpatterns = [
    # Бардык категориялардын тизмеси
    path('', views.category_list, name='list'),
    
    # Категориянын же подкатегориянын ичине киргендеги баракча
    path('<slug:slug>/', views.category_detail, name='detail'),
]