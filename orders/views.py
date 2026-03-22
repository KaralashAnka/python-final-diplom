from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from decimal import Decimal
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderItemSerializer
from .tasks import send_order_confirmation_email, send_admin_notification_email


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response(CartItemSerializer(cart_item).data)
    
    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        cart = self.get_object()
        product_id = request.data.get('product_id')
        
        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            return Response({'message': 'Item removed from cart'})
        except CartItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = self.get_object()
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        shipping_address_id = request.data.get('shipping_address')
        
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not shipping_address_id:
            return Response({'error': 'Shipping address required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total amount
        total_amount = sum(item.get_total_price() for item in cart.items.all())
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address_id=shipping_address_id,
            notes=request.data.get('notes', ''),
            status='pending'
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                supplier=cart_item.product.supplier
            )
        
        # Clear cart
        cart.items.all().delete()
        
        # Send email notifications
        send_order_confirmation_email.delay(order.id)
        send_admin_notification_email.delay(order.id)
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return Response({'message': f'Order status updated to {new_status}'})
        else:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        shipping_address_id = request.data.get('shipping_address')
        notes = request.data.get('notes', '')
        
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not shipping_address_id:
            return Response({'error': 'Shipping address required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate total amount
        total_amount = sum(item.get_total_price() for item in cart.items.all())
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            shipping_address_id=shipping_address_id,
            notes=notes,
            status='pending'
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                supplier=cart_item.product.supplier
            )
        
        # Clear cart
        cart.items.all().delete()
        
        # Send email notifications
        send_order_confirmation_email.delay(order.id)
        send_admin_notification_email.delay(order.id)
        
        return Response({
            'message': 'Order created successfully',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)
