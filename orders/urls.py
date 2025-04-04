from django.urls import path, include
from . import views
from .views import place_order, order_history, OrderViewSet, OrderItemViewSet, OrderListCreateView, OrderDetailView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)

urlpatterns = [
    path('create/', views.create_order, name='create_order'),  # This is correct as it should call the `create_order` view
    path('view/<int:order_id>/', views.view_order, name='view_order'),
    path('list/', views.list_orders, name='list_orders'),
    path('place/', place_order, name='place_order'),
    path('history/', order_history, name='order_history'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('', include(router.urls)),
    path('paystack/initialize/', views.paystack_initialize, name='paystack_initialize'),
    path('paystack/verify/', views.paystack_verify, name='paystack_verify'),
]

