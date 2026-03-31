from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Order


@shared_task
def send_order_confirmation_email(order_id):
    """Отправка email с подтверждением заказа"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Подтверждение заказа #{order.order_number}'
        
        # В реальном проекте здесь будет HTML шаблон
        message = f'''
        Здравствуйте, {order.user.first_name}!
        
        Ваш заказ #{order.order_number} успешно оформлен.
        
        Сумма заказа: {order.total_amount} руб.
        Статус: {order.get_status_display()}
        
        Адрес доставки: {order.shipping_address}
        
        Спасибо за покупку!
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )
        
        return f'Email sent for order {order.order_number}'
    
    except Order.DoesNotExist:
        return f'Order {order_id} not found'
    except Exception as e:
        return f'Error sending email: {str(e)}'


@shared_task
def send_admin_notification_email(order_id):
    """Отправка email администратору о новом заказе"""
    try:
        order = Order.objects.get(id=order_id)
        
        subject = f'Новый заказ #{order.order_number}'
        
        message = f'''
        Получен новый заказ:
        
        Номер: {order.order_number}
        Клиент: {order.user.email}
        Сумма: {order.total_amount} руб.
        Адрес: {order.shipping_address}
        
        Товары в заказе:
        '''
        
        for item in order.items.all():
            message += f'\n- {item.product.name} x {item.quantity} = {item.get_total_price()} руб.'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        
        return f'Admin notification sent for order {order.order_number}'
    
    except Order.DoesNotExist:
        return f'Order {order_id} not found'
    except Exception as e:
        return f'Error sending admin email: {str(e)}'


@shared_task
def send_daily_reports():
    """Отправка ежедневных отчетов"""
    # Здесь можно реализовать отправку ежедневных отчетов
    # о продажах, новых заказах и т.д.
    return 'Daily reports sent'
