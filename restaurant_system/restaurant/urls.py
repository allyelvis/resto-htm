from django.urls import path
from .views import get_menu_items, create_order, manage_stock

urlpatterns = [
    path('menu/', get_menu_items, name='menu-items'),
    path('order/', create_order, name='create-order'),
    path('stock/', manage_stock, name='manage-stock'),
]
