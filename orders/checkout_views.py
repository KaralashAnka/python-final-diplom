from rest_framework import views, permissions, status
from rest_framework.response import Response
from .models import Cart, Order, OrderItem
from users.models import Address


class OrderConfirmView(views.APIView):
    """API запрос на подтверждение заказа согласно спецификации"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Подтверждение заказа с ID корзины и ID контакта"""
        cart_id = request.data.get('cart_id')
        contact_id = request.data.get('contact_id')
        
        if not cart_id or not contact_id:
            return Response({
                'error': 'cart_id и contact_id обязательны'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Получаем корзину
            cart = Cart.objects.get(id=cart_id, user=request.user)
            
            # Получаем контакт
            contact = Address.objects.get(id=contact_id, user=request.user)
            
            # Проверяем, что корзина не пуста
            if not cart.items.exists():
                return Response({
                    'error': 'Корзина пуста'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Рассчитываем общую сумму
            total_amount = sum(item.get_total_price() for item in cart.items.all())
            
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                shipping_address=contact,
                notes=f'Контакт: {contact.first_name} {contact.last_name}',
                status='pending'
            )
            
            # Создаем элементы заказа
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price,
                    supplier=cart_item.product.supplier
                )
            
            # Очищаем корзину
            cart.items.all().delete()
            
            # Отправляем email уведомления
            from .tasks import send_order_confirmation_email, send_admin_notification_email
            send_order_confirmation_email.delay(order.id)
            send_admin_notification_email.delay(order.id)
            
            return Response({
                'message': 'Заказ успешно оформлен',
                'order_id': order.id,
                'order_number': order.order_number,
                'total_amount': float(order.total_amount),
                'status': order.status
            }, status=status.HTTP_201_CREATED)
            
        except Cart.DoesNotExist:
            return Response({
                'error': 'Корзина не найдена'
            }, status=status.HTTP_404_NOT_FOUND)
        except Address.DoesNotExist:
            return Response({
                'error': 'Контакт не найден'
            }, status=status.HTTP_404_NOT_FOUND)
