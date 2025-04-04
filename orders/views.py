from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart, CartItem
from django.db.models import Sum
from rest_framework import generics, permissions, status, viewsets
import requests
from django.http import JsonResponse
from django.conf import settings
from paystackapi.paystack import Paystack

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Attach the user to the order before saving
        serializer.save(user=self.request.user)

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Calculate total price
        total_price = sum(item.price * item.quantity for item in order.items.all())
        order.total_price = total_price
        order.save()

class OrderDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

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

# Initialize Paystack API
paystack = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)

def paystack_initialize(request):
    email = request.user.email  # Use logged-in user's email or as per your requirement
    amount = 1000 * 100  # Amount in kobo (1 Naira = 100 kobo)
    
    # Set the headers for Paystack API
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json'
    }

    # Data to be sent to Paystack for payment initialization
    data = {
        'email': email,
        'amount': amount,
        'currency': 'GHC', 
        'callback_url': 'http://127.0.0.1:8000//paystack/verify/',  # Callback URL for verification
    }

    # Make the POST request to Paystack API to initialize payment
    response = requests.post(settings.PAYSTACK_PAYMENT_URL, headers=headers, json=data)
    response_data = response.json()

    # If payment initialization is successful, redirect to Paystack's payment page
    if response_data['status']:
        authorization_url = response_data['data']['authorization_url']
        return JsonResponse({"message": "Payment Initialization Successful"})

    # If there was an error with payment initialization
    return JsonResponse({'error': 'Unable to process payment'}, status=400)

def paystack_verify(request):
    reference = request.GET.get('reference')  # Get the reference passed by Paystack

    # Verify the payment by making a GET request to Paystack
    headers = {'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}'}
    verify_url = f'https://api.paystack.co/transaction/verify/{reference}'
    response = requests.get(verify_url, headers=headers)
    response_data = response.json()

    # Check if the payment is successful
    if response_data['status'] and response_data['data']['status'] == 'success':
        # Update the order status to "paid" if payment is successful
        order = Order.objects.get(reference=reference)
        order.status = 'paid'
        order.save()

        return JsonResponse({'message': 'Payment successful'})

    # If payment failed or was not successful
    return JsonResponse({'message': 'Payment verification failed'}, status=400)
