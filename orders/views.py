from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """Create an order from the user's cart."""
    user = request.user
    cart = Cart.objects.get(user=user)

    # Create a new order
    order = Order.objects.create(user=user, total_price=cart.total_price)

    # Add cart items to order
    for cart_item in cart.items.all():
        OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

    # Clear the user's cart after the order is placed
    cart.items.all().delete()

    # Update the total price in the order
    order.update_total()

    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_order(request, order_id):
    """View details of a specific order."""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    return Response(OrderSerializer(order).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    """List all orders placed by the user."""
    orders = Order.objects.filter(user=request.user)
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_orders(request):
    """List all orders for the user."""
    orders = Order.objects.filter(user=request.user)
    return Response(OrderSerializer(orders, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    """Place an order (potentially reuse code from create_order)."""
    # Logic for placing an order (can use `create_order` logic here if needed)
    return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)  # Fix the string here

