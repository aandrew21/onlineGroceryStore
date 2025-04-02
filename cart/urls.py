from django.urls import path
from .views import view_cart, add_to_cart, remove_from_cart, clear_cart

urlpatterns = [
    path('view/', view_cart, name='view-cart'),
    path('add/', add_to_cart, name='add-to-cart'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
    path('clear/', clear_cart, name='clear-cart'),
]

