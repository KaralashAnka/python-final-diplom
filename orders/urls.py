from django.urls import path
from . import views
from .checkout_views import OrderConfirmView

urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('cart/', views.CartViewSet.as_view({'get': 'retrieve', 'post': 'add_item'}), name='cart'),
    path('cart/add-item/', views.CartViewSet.as_view({'post': 'add_item'}), name='cart-add-item'),
    path('cart/remove-item/', views.CartViewSet.as_view({'post': 'remove_item'}), name='cart-remove-item'),
    path('cart/clear/', views.CartViewSet.as_view({'post': 'clear'}), name='cart-clear'),
    path('orders/', views.OrderViewSet.as_view({'get': 'list', 'post': 'create'}), name='orders'),
    path('orders/<int:pk>/', views.OrderViewSet.as_view({'get': 'retrieve'}), name='order-detail'),
    path('order-confirm/', OrderConfirmView.as_view(), name='order-confirm'),
]
