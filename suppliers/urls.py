from django.urls import path
from . import views

urlpatterns = [
    path('suppliers/', views.SupplierViewSet.as_view({'get': 'list', 'post': 'create'}), name='suppliers'),
    path('suppliers/<int:pk>/', views.SupplierViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='supplier-detail'),
    path('suppliers/<int:pk>/toggle-status/', views.SupplierViewSet.as_view({'post': 'toggle_status'}), name='supplier-toggle-status'),
    path('suppliers/<int:pk>/orders/', views.SupplierViewSet.as_view({'get': 'orders'}), name='supplier-orders'),
    path('price-lists/', views.PriceListViewSet.as_view({'get': 'list', 'post': 'create'}), name='price-lists'),
    path('price-lists/<int:pk>/', views.PriceListViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='price-list-detail'),
]
