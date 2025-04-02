from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem
from django.contrib.auth.models import User

@api_view(['POST'])
def create_order(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    
    # Create a new order
    order = Order.objects.create(user=user, total_price=cart.total_price)
    
    # Add cart items to order
    for cart_item in cart.items.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
    
    # Clear the user's cart after the order is placed
    cart.items.clear()
    
    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    
    return Response(OrderSerializer(order).data)

@api_view(['GET'])
def list_orders(request):
    orders = Order.objects.filter(user=request.user)
    return Response(OrderSerializer(orders, many=True).data)

# Create your views here.
