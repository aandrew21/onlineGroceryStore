from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    """Retrieve the user's cart details."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """Add a product to the cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += int(quantity)
    cart_item.save()

    # Update the cart's total price after adding an item
    cart.update_total_price()

    return Response({"message": "Item added to cart"}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        cart_item.delete()

        # Update the cart's total price after removing an item
        cart_item.cart.update_total_price()

        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found in cart"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """Remove all items from the cart."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()

    # Reset the total price to 0 after clearing the cart
    cart.total_price = 0.00
    cart.save()

    return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)

