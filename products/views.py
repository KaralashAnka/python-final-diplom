from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.uploadedfile import InMemoryUploadedFile
import tempfile
import os
from .models import Category, Product, ProductAttribute
from .serializers import CategorySerializer, ProductSerializer, ProductAttributeSerializer
from .tasks import import_products_from_yaml, export_products_to_yaml


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'supplier']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity', 1)
        
        # Add to cart logic will be implemented in orders app
        return Response({'message': f'Added {quantity} of {product.name} to cart'})


class ProductImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        supplier_id = request.data.get('supplier_id')
        
        if not supplier_id:
            return Response({'error': 'Supplier ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Сохраняем файл временно
        with tempfile.NamedTemporaryFile(delete=False, suffix='.yaml') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        # Запускаем задачу импорта
        task = import_products_from_yaml.delay(temp_file_path, supplier_id)
        
        return Response({
            'message': 'Import task started',
            'task_id': task.id
        })


class ProductExportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        supplier_id = request.query_params.get('supplier_id')
        
        # Запускаем задачу экспорта
        task = export_products_to_yaml.delay(supplier_id)
        
        return Response({
            'message': 'Export task started',
            'task_id': task.id
        })
