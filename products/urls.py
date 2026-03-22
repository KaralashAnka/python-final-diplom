from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='categories'),
    path('categories/<int:pk>/', views.CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='category-detail'),
    path('products/', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='products'),
    path('products/<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-detail'),
    path('products/<int:pk>/add-to-cart/', views.ProductViewSet.as_view({'post': 'add_to_cart'}), name='product-add-to-cart'),
    path('attributes/', views.ProductAttributeViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-attributes'),
    path('attributes/<int:pk>/', views.ProductAttributeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='product-attribute-detail'),
    path('import/', views.ProductImportView.as_view(), name='product-import'),
    path('export/', views.ProductExportView.as_view(), name='product-export'),
]
