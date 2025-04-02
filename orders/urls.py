from django.urls import path
from . import views
from .views import place_order, order_history

urlpatterns = [
    path('create/', views.create_order, name='create_order'),  # This is correct as it should call the `create_order` view
    path('view/<int:order_id>/', views.view_order, name='view_order'),
    path('list/', views.list_orders, name='list_orders'),
    path('place/', place_order, name='place_order'),
    path('history/', order_history, name='order_history'),
]

